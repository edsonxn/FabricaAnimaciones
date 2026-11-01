# -*- coding: utf-8 -*-
"""Kit del estilo PEGATINA FLOW (20-oct-2026, prueba `videos/jalpa/`): Flow (Nano Banana 2.1) pinta los ESCENARIOS vacíos y HOJAS de
personajes, ciclos de movimiento (caminar, correr, galopar: los N cuadros en la MISMA imagen, así el personaje sale idéntico) y
utilería sobre fondo blanco; aquí se recortan como piezas con alfa y se animan por código como pegatinas de papel con movimiento.

RECORTE (una vez por video, desde C:\\FabricaAnimaciones):
  python nucleo/pegaflow.py recortar <video> [hoja ...]   hojas de videos/<v>/hd/ (2K de Flow) o hojas/ (1K) cuyo nombre acaba en _a
      → videos/<v>/piezas/<hoja>/NN.png (orden de lectura: filas de arriba abajo, izquierda a derecha) + _indice.jpg numerado.
      Hojas cuyo nombre contiene «camina|corre|galope|ciclo|aleteo|marcha|danza» → además ciclo_NN.png alineados por los pies (mismo lienzo).
  Alfa: color del fondo = mediana del borde; fondo = zonas casi de ese color conectadas al borde (relleno por inundación, así el
  algodón blanco encerrado por la tinta NO se pierde); huecos interiores (entre brazo y cuerpo) = zona plana del color del fondo que
  rembg `isnet-anime` también da por fondo; borde antialias con descontaminación del blanco.

ANIMACIÓN (en las escenas del video, cwd = carpeta del video):
  Plano(fondo, t0, t1, z0, z1, c0, c1, par)   cámara sobre un escenario con parallax por profundidad (imagenes/depth/<fondo>.png)
      .fondo(lz, t)  dibuja el escenario      .P(t, x, y) → (X, Y, s) pantalla de un punto (x, y) normalizado del escenario
  actor(lz, nombre, X, Y, alto, ...)          pieza con ancla en los pies, giro, espejo, aplastamiento, sombra de contacto
  ciclo_n(nombre) / cuadro_ciclo(dist, paso, n)  cuadro del ciclo según la distancia recorrida (los pies no patinan)
  humo / brillo / chispas / destellos / rotulo / acabado   ambiente continuo y texto de énfasis en papel recortado
"""
import functools
import glob
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CICLO_PAL = ("camina", "corre", "galope", "ciclo", "aleteo", "marcha", "danza")


# =================================================================== RECORTE
def _alfa_hoja(rgb, tol=34.0, sesion=None):
    """RGB uint8 de una hoja sobre fondo liso → (rgb descontaminado uint8, alfa float32 0..1)."""
    h, w = rgb.shape[:2]
    b = 6
    borde = np.concatenate([rgb[:b].reshape(-1, 3), rgb[-b:].reshape(-1, 3), rgb[:, :b].reshape(-1, 3), rgb[:, -b:].reshape(-1, 3)])
    bg = np.median(borde, 0).astype(np.float32)
    f = rgb.astype(np.float32)
    dist = np.abs(f - bg).max(-1)
    near = (dist < tol).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(near, connectivity=4)
    ed = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    ed = set(int(e) for e in ed if e > 0)
    fondo = np.isin(lab, list(ed))
    # huecos interiores: zona plana del color del fondo encerrada por la figura, confirmada por rembg
    cand = [k for k in range(1, n) if k not in ed and st[k, cv2.CC_STAT_AREA] >= 150]
    if cand:
        if sesion is None:
            from rembg import new_session
            sesion = new_session("isnet-anime")
        from rembg import remove
        m_rb = np.asarray(remove(Image.fromarray(rgb), session=sesion, only_mask=True), np.float32) / 255.0
        for k in cand:
            x, y, ww, hh = st[k, :4]
            sub = lab[y:y + hh, x:x + ww] == k
            dd = dist[y:y + hh, x:x + ww][sub]
            p90 = np.percentile(dd, 90)
            plano_puro = p90 < tol * 0.22 and dd.mean() < tol * 0.12      # el color exacto del fondo (entre arco y cuerda)
            if plano_puro or (p90 < tol * 0.5 and m_rb[y:y + hh, x:x + ww][sub].mean() < 0.35):
                fondo[y:y + hh, x:x + ww] |= sub
    fg = ~fondo
    a = fg.astype(np.float32)
    anillo = cv2.dilate(fg.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & fondo
    a[anillo] = np.clip(dist[anillo] / tol, 0, 1) ** 0.8
    # descontaminar el halo blanco del borde: c = bg + (obs - bg) / a
    dec = f.copy()
    aa = np.maximum(a[anillo], 0.08)[:, None]
    dec[anillo] = np.clip(bg + (f[anillo] - bg) / aa, 0, 255)
    return dec.astype(np.uint8), a


def _filas(cajas):
    """Ordena cajas (x, y, w, h) en orden de lectura agrupando por filas."""
    if not cajas:
        return []
    hmed = float(np.median([c[3] for c in cajas]))
    idx = sorted(range(len(cajas)), key=lambda i: cajas[i][1] + cajas[i][3] / 2)
    filas, act, cy0 = [], [], None
    for i in idx:
        cy = cajas[i][1] + cajas[i][3] / 2
        if cy0 is not None and cy - cy0 > 0.5 * hmed:
            filas.append(act)
            act = []
        act.append(i)
        cy0 = cy if cy0 is None else (cy0 * (len(act) - 1) + cy) / len(act)
    filas.append(act)
    return [i for fila in filas for i in sorted(fila, key=lambda j: cajas[j][0])]


def _indice(piezas, ruta, ancho=1600):
    """Hoja de contacto numerada sobre gris (para elegir piezas sin abrir cada PNG)."""
    cel = 200
    cols = max(1, ancho // cel)
    filas = (len(piezas) + cols - 1) // cols
    M = Image.new("RGB", (cols * cel, filas * cel), (92, 96, 104))
    dr = ImageDraw.Draw(M)
    for i, p in enumerate(piezas):
        im = Image.fromarray(p)
        im.thumbnail((cel - 12, cel - 26))
        x, y = (i % cols) * cel, (i // cols) * cel
        M.paste(im, (x + (cel - im.size[0]) // 2, y + 22 + (cel - 26 - im.size[1]) // 2), im)
        dr.rectangle([x, y, x + 30, y + 18], fill=(0, 0, 0))
        dr.text((x + 4, y + 3), f"{i:02d}", fill=(255, 230, 0))
    M.save(ruta, quality=88)


def _grupos(a, junta, min_area):
    """Etiquetas de piezas: componentes con una junta fina; los trozos chicos (plumas, flechas sueltas) se unen al grande más
    cercano si está a < 4 juntas; los demás chicos se descartan (motas)."""
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * junta + 1, 2 * junta + 1))
    grp = cv2.dilate((a > 0.5).astype(np.uint8), k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(grp, connectivity=8)
    if n <= 1:
        return lab, []
    areas = np.bincount(lab[a > 0.5].ravel(), minlength=n)
    areas[0] = 0
    grande = areas >= max(min_area, 0.10 * areas[1:].max())
    vivos = [j for j in range(1, n) if grande[j]]
    remap = np.arange(n)
    sueltos = []
    r = 4 * junta + 1
    for j in range(1, n):
        if grande[j] or areas[j] < 30:
            continue
        x, y, ww, hh = st[j, :4]
        # distancia por píxeles, no por cajas: unas flechas en el suelo caen dentro de la caja de dos figuras a la vez
        # (21-oct, h15_gente en 2K se las daba a la niña en vez de al anciano sentado sobre ellas)
        y0, x0 = max(y - r, 0), max(x - r, 0)
        ven = lab[y0:y + hh + r, x0:x + ww + r]
        dist = cv2.distanceTransform((ven != j).astype(np.uint8), cv2.DIST_L2, 3)
        mejor, dmin = None, r
        for g in vivos:
            sel = ven == g
            if sel.any():
                d = float(dist[sel].min())
                if d < dmin:
                    mejor, dmin = g, d
        if mejor is not None:
            remap[j] = mejor
        elif areas[j] >= min_area:
            sueltos.append(j)                       # pieza chica pero propia (un ave, una flecha suelta)
    return remap[lab], vivos + sueltos


def _partir(al, n):
    """Parte una pieza ancha (figuras que se tocan) en `n` por los valles de la suma de alfa por columnas."""
    perfil = cv2.GaussianBlur(al.sum(0).astype(np.float32).reshape(1, -1), (0, 0), 3).ravel()
    w = al.shape[1]
    cortes = [0]
    for i in range(1, n):
        c = i * w / n
        r = int(0.28 * w / n)
        lo, hi = int(max(c - r, cortes[-1] + 5)), int(min(c + r, w - 5))
        cortes.append(lo + int(np.argmin(perfil[lo:hi])) if hi > lo else int(c))
    cortes.append(w)
    return [(cortes[i], cortes[i + 1]) for i in range(n)]


def recortar_hoja(ruta, dst, junta=None, min_area=None, sesion=None, n_esperado=None):
    """Hoja → piezas RGBA en `dst` (NN.png) + _indice.jpg; si es de ciclo, además ciclo_NN.png alineados por los pies.
    `n_esperado`: cuántas figuras hay (filas de ciclo): si salen menos, se parten las más anchas por sus valles."""
    rgb = np.asarray(Image.open(ruta).convert("RGB"))
    h, w = rgb.shape[:2]
    dec, a = _alfa_hoja(rgb, sesion=sesion)
    min_area = min_area or int(0.0006 * h * w)
    junta = junta or max(2, int(round(w / 600)))
    lab, vivos = _grupos(a, junta, min_area)
    trozos = []                                   # (x, y, w, h, alfa recortado, color recortado)
    for j in vivos:
        ys, xs = np.nonzero((lab == j) & (a > 0.02))
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        al = a[y0:y1, x0:x1] * (lab[y0:y1, x0:x1] == j)
        trozos.append([x0, y0, x1 - x0, y1 - y0, al, dec[y0:y1, x0:x1]])
    while n_esperado and len(trozos) < n_esperado and trozos:
        i = max(range(len(trozos)), key=lambda q: trozos[q][2])
        x0, y0, ww, hh, al, col = trozos.pop(i)
        wmed = np.median([t[2] for t in trozos]) if trozos else ww / (n_esperado - len(trozos))
        partes = max(2, min(n_esperado - len(trozos), int(round(ww / max(wmed, 1)))))
        for c0, c1 in _partir(al, partes):
            trozos.append([x0 + c0, y0, c1 - c0, hh, al[:, c0:c1], col[:, c0:c1]])
    cajas, recs = [], []
    for x0, y0, ww, hh, al, col in trozos:
        ys, xs = np.nonzero(al > 0.02)
        if len(xs) == 0:
            continue
        yy0, yy1, xx0, xx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        p = 3
        sub_a = np.pad(al[yy0:yy1, xx0:xx1], p)
        sub_c = np.pad(col[yy0:yy1, xx0:xx1], ((p, p), (p, p), (0, 0)), mode="edge")
        recs.append(np.dstack([sub_c, (sub_a * 255).round().astype(np.uint8)]))
        cajas.append((x0 + xx0, y0 + yy0, xx1 - xx0, yy1 - yy0))
    orden = _filas(cajas)
    os.makedirs(dst, exist_ok=True)
    for f in glob.glob(os.path.join(dst, "*.png")):
        os.remove(f)
    piezas = [recs[i] for i in orden]
    meta = []
    for i, p in enumerate(piezas):
        Image.fromarray(p).save(os.path.join(dst, f"{i:02d}.png"))
        meta.append(dict(n=i, w=int(p.shape[1]), h=int(p.shape[0]), caja=[int(v) for v in cajas[orden[i]]]))
    _indice(piezas, os.path.join(dst, "_indice.jpg"))
    nombre = os.path.basename(dst)
    if any(c in nombre for c in CICLO_PAL):
        meta_c = _alinear_ciclo(piezas, dst)
    else:
        meta_c = None
    json.dump(dict(fuente=os.path.basename(ruta), tam=[w, h], piezas=meta, ciclo=meta_c),
              open(os.path.join(dst, "meta.json"), "w", encoding="utf-8"), indent=1)
    return len(piezas)


def _alinear_ciclo(piezas, dst):
    """Cuadros de un ciclo (ya en orden) → mismo lienzo, pies abajo, eje del torso al centro."""
    datos = []
    for p in piezas:
        al = p[..., 3].astype(np.float32) / 255.0
        ys, xs = np.nonzero(al > 0.5)
        top, bot = ys.min(), ys.max()
        alto = bot - top
        sel = ys < top + 0.55 * alto                 # cabeza y torso: el eje no baila con las piernas
        cx = float(np.average(xs[sel], weights=al[ys[sel], xs[sel]]))
        datos.append((cx, top, bot))
    izq = max(cx for cx, _, _ in datos)
    der = max(p.shape[1] - cx for p, (cx, _, _) in zip(piezas, datos))
    mitad = int(math.ceil(max(izq, der))) + 4
    alto = max(bot for _, _, bot in datos) + 4
    Wc, Hc = 2 * mitad, int(alto) + 4
    for i, (p, (cx, top, bot)) in enumerate(zip(piezas, datos)):
        lienzo = np.zeros((Hc, Wc, 4), np.uint8)
        ox, oy = int(round(mitad - cx)), int(Hc - 4 - bot)
        y0, x0 = max(oy, 0), max(ox, 0)
        sy0, sx0 = y0 - oy, x0 - ox
        hh = min(p.shape[0] - sy0, Hc - y0)
        ww = min(p.shape[1] - sx0, Wc - x0)
        lienzo[y0:y0 + hh, x0:x0 + ww] = p[sy0:sy0 + hh, sx0:sx0 + ww]
        Image.fromarray(lienzo).save(os.path.join(dst, f"ciclo_{i:02d}.png"))
    return dict(n=len(piezas), w=Wc, h=Hc)


def recortar_video(v, hojas=None):
    """`hojas`: nombres a rehacer; «nombre=N» fija cuántas figuras tiene (se guarda en piezas/cuantas.json para la próxima)."""
    d = os.path.join(RAIZ, "videos", v)
    from rembg import new_session
    ses = new_session("isnet-anime")
    pc = os.path.join(d, "piezas", "cuantas.json")
    cuantas = json.load(open(pc, encoding="utf-8")) if os.path.exists(pc) else {}
    sel = []
    for h_ in hojas or []:
        nom, _, n = h_.partition("=")
        sel.append(nom)
        if n:
            cuantas[nom] = int(n)
    hojas = sel or None
    os.makedirs(os.path.dirname(pc), exist_ok=True)
    json.dump(cuantas, open(pc, "w", encoding="utf-8"), indent=1)
    rutas = {}
    for carp in ("hojas", "hd"):                       # hd (2K) pisa a hojas (1K)
        for f in sorted(glob.glob(os.path.join(d, carp, "*_a.jpg"))):
            nom = os.path.basename(f)[:-6]
            if os.path.exists(os.path.join(d, "imagenes", nom + "_a.jpg")):
                continue                               # es un escenario, no una hoja
            rutas[nom] = f
    for nom, f in rutas.items():
        if hojas and nom not in hojas:
            continue
        n = recortar_hoja(f, os.path.join(d, "piezas", nom), sesion=ses, n_esperado=cuantas.get(nom))
        print(f"{nom:20s} {n:3d} piezas  ({os.path.basename(os.path.dirname(f))})")


# =================================================================== ANIMACIÓN
from motor import H, W, clamp01, e_back, e_inout, e_out, lerp, prog, smooth  # noqa: E402

_GRID = {}


def _grid():
    if "g" not in _GRID:
        _GRID["g"] = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return _GRID["g"]


def _ruta_fondo(nombre):
    for p in (os.path.join("hd", nombre + "_a.jpg"), os.path.join("imagenes", nombre + "_a.jpg"), os.path.join("imagenes", nombre + ".jpg")):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(nombre)


@functools.lru_cache(maxsize=6)
def _fondo_rgb(nombre):
    return np.asarray(Image.open(_ruta_fondo(nombre)).convert("RGB"))


@functools.lru_cache(maxsize=6)
def _fondo_depth(nombre, hs, ws):
    p = os.path.join("imagenes", "depth", nombre + "_a.png")
    if not os.path.exists(p):                       # escenario ya nombrado con su variante («espacio_tierra_a», asteroide_invisible)
        p = os.path.join("imagenes", "depth", nombre + ".png")
    if not os.path.exists(p):
        return None
    d = cv2.imread(p, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    return cv2.resize(d, (ws, hs), interpolation=cv2.INTER_LINEAR)


class Plano:
    """Cámara sobre un escenario: zoom z y centro c (relativo 0..1) de t0 a t1, parallax por profundidad `par` (px de pantalla
    que se desplaza lo más cercano respecto de lo lejano) y deriva leve de cámara en mano."""

    def __init__(self, fondo, t0, t1, z0=1.0, z1=1.08, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(28.0, 6.0), ease=e_inout, mano=1.0,
                 semilla=0, tono=None):
        self.f, self.t0, self.t1 = fondo, t0, t1
        self.z0, self.z1, self.c0, self.c1, self.par, self.ease, self.mano, self.sem = z0, z1, c0, c1, par, ease, mano, semilla
        self.tono = tono

    def _st(self, t):
        rgb = _fondo_rgb(self.f)
        hs, ws = rgb.shape[:2]
        u = self.ease(clamp01((t - self.t0) / max(self.t1 - self.t0, 1e-3)))
        z = lerp(self.z0, self.z1, u)
        cx = lerp(self.c0[0], self.c1[0], u) * ws
        cy = lerp(self.c0[1], self.c1[1], u) * hs
        m, s = self.mano, self.sem
        s0 = max(W / ws, H / hs) * z
        cx += m * (4.0 * math.sin(0.8 * t + s) + 2.0 * math.sin(2.1 * t + 2 * s)) / s0
        cy += m * (3.0 * math.sin(0.6 * t + 1.7 + s) + 1.5 * math.sin(2.7 * t + s)) / s0
        ph = math.sin(u * math.pi) * 0.5 + 0.5 * (2 * u - 1)
        return rgb, hs, ws, s0, cx, cy, ph

    def fondo(self, lz, t):
        rgb, hs, ws, s0, cx, cy, ph = self._st(t)
        X, Y = _grid()
        sx = cx + (X - W / 2) / s0
        sy = cy + (Y - H / 2) / s0
        d = _fondo_depth(self.f, hs, ws)
        if d is not None and (self.par[0] or self.par[1]):
            dd = cv2.remap(d, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            k = dd - 0.5
            sx = sx - k * (self.par[0] * ph) / s0
            sy = sy - k * (self.par[1] * ph) / s0
        out = cv2.remap(rgb, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255.0
        if self.tono is not None:
            out *= np.float32(self.tono)
        lz[:] = out

    def P(self, t, x, y, capa=1.0):
        """Punto (x, y) normalizado del escenario → (X, Y, s) en pantalla; s = escala de 1 px del escenario. `capa` > 1 = más cerca
        que el suelo (primer plano: se mueve y crece más)."""
        rgb, hs, ws, s0, cx, cy, ph = self._st(t)
        px, py = x * ws, y * hs
        d = _fondo_depth(self.f, hs, ws)
        k = 0.0
        if d is not None:
            k = float(d[int(np.clip(py, 0, hs - 1)), int(np.clip(px, 0, ws - 1))]) - 0.5
        if capa != 1.0:
            k = 0.5 + (capa - 1.0)
        X = W / 2 + (px - cx) * s0 * capa + k * self.par[0] * ph
        Y = H / 2 + (py - cy) * s0 * capa + k * self.par[1] * ph
        return X, Y, s0 * capa

    def alto_px(self, t, frac):
        """Altura en pantalla de algo que mide `frac` del alto del escenario."""
        rgb, hs, ws, s0, *_ = self._st(t)
        return frac * hs * s0

    def en(self, t, x, y, frac, capa=1.0):
        """(X, Y, alto px) de algo con los pies en (x, y) del escenario que mide `frac` del alto del escenario."""
        X, Y, s = self.P(t, x, y, capa)
        return X, Y, frac * _fondo_rgb(self.f).shape[0] * s

    def fg(self, t, x, y, frac, capa=1.3):
        """Primer plano en coordenadas de PANTALLA (x, y relativos al cuadro en t0, `frac` del alto de pantalla): se desplaza
        `capa` veces lo que el plano medio y crece con el zoom elevado a `capa` (más cerca que el suelo)."""
        X0, Y0, s0 = self.P(self.t0, 0.5, 0.5)
        X1, Y1, s1 = self.P(t, 0.5, 0.5)
        k = (s1 / s0) ** capa
        return (W / 2 + (x * W - W / 2) * k + (X1 - X0) * capa,
                H / 2 + (y * H - H / 2) * k + (Y1 - Y0) * capa, frac * H * k)

    def ancho_mundo(self, t):
        """Píxeles de pantalla por unidad normalizada en x (para medir distancias recorridas)."""
        rgb, hs, ws, s0, *_ = self._st(t)
        return ws * s0


# ---------------------------------------------------------------- piezas
BORDE_PAPEL = 0.0065            # borde de pegatina (fracción del lado mayor de la pieza); 0 = sin borde
PAPEL = (247, 241, 226)


def _con_borde(im):
    """Borde de papel crema alrededor de la pieza (la calcomanía recortada): alfa dilatado y suavizado bajo la pieza."""
    a = np.asarray(im, np.uint8)
    b = max(2, int(round(BORDE_PAPEL * max(a.shape[:2]))))
    pad = b + 2
    a = np.pad(a, ((pad, pad), (pad, pad), (0, 0)))
    al = a[..., 3].astype(np.float32) / 255.0
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * b + 1, 2 * b + 1))
    ab = cv2.GaussianBlur(cv2.dilate((al > 0.35).astype(np.float32), k), (0, 0), 0.8)
    rgb = a[..., :3].astype(np.float32) * al[..., None] + np.float32(PAPEL) * (1 - al[..., None])
    out = np.dstack([np.clip(rgb, 0, 255), np.maximum(al, ab) * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


@functools.lru_cache(maxsize=400)
def _pieza(nombre, nivel=0, sombra=True, tono=None):
    """Pieza recortada como Sprite (alfa premultiplicado, sombra de papel). `tono` (r, g, b) la tiñe con la luz de la escena
    (noche azul, mañana fría): sin eso la pegatina parece pegada encima del fondo."""
    import docu as D
    p = os.path.join("piezas", nombre + ".png")
    im = Image.open(p).convert("RGBA")
    if BORDE_PAPEL:
        im = _con_borde(im)
    if nivel:
        im = im.resize((max(2, im.size[0] >> nivel), max(2, im.size[1] >> nivel)), Image.LANCZOS)
    a = np.asarray(im, np.uint8)
    rgb = a[..., :3].copy()
    if tono is not None:
        rgb = np.clip(rgb.astype(np.float32) * np.float32(tono), 0, 255).astype(np.uint8)
    return D.Sprite(rgb, a[..., 3].astype(np.float32) / 255.0, sombra=sombra, sr=4, off=(4, 6), sop=0.30)


@functools.lru_cache(maxsize=64)
def ciclo_n(nombre):
    return len(glob.glob(os.path.join("piezas", nombre, "ciclo_*.png")))


def cuadro_ciclo(dist, paso, n):
    """Índice del cuadro según la distancia recorrida (px de pantalla); `paso` = distancia de un ciclo completo."""
    return int(math.floor(dist / max(paso, 1e-3) * n)) % n


def sombra_suelo(lz, X, Y, rx, ry, op=0.32):
    """Sombra de contacto (elipse difusa) que pega la pieza al suelo: sin ella la pegatina «flota»."""
    rx, ry = max(rx, 2.0), max(ry, 1.5)
    x0, x1 = int(max(X - 2 * rx, 0)), int(min(X + 2 * rx, W))
    y0, y1 = int(max(Y - 2 * ry, 0)), int(min(Y + 2 * ry, H))
    if x1 <= x0 or y1 <= y0:
        return
    xx = (np.arange(x0, x1, dtype=np.float32) - X) / rx
    yy = (np.arange(y0, y1, dtype=np.float32) - Y) / ry
    g = np.exp(-(yy[:, None] ** 2 + xx[None, :] ** 2) * 1.6)
    lz[y0:y1, x0:x1] *= (1.0 - op * g)[..., None]


def actor(lz, nombre, X, Y, alto, rot=0.0, flip=False, op=1.0, sx=1.0, sy=1.0, ancla=(0.5, 1.0), suelo=0.30, sombra=True,
          tono=None):
    """Dibuja la pieza `nombre` (p. ej. "petacatl_hoja/02" o "petacatl_camina/ciclo_03") con el ancla (por defecto los pies) en
    (X, Y) de pantalla, `alto` px, giro `rot` (grados, alrededor del ancla), espejo, aplastamiento sx/sy, sombra de contacto y
    tono de la luz de la escena."""
    import docu as D
    if op <= 0.003 or alto < 2:
        return
    tono = tuple(tono) if tono is not None else None
    base = _pieza(nombre, 0, sombra, tono)
    s_full = alto / base.h
    nivel = 0 if s_full > 0.55 else (1 if s_full > 0.28 else 2)
    spr = _pieza(nombre, nivel, sombra, tono) if nivel else base
    s = alto / spr.h
    if suelo and ancla[1] >= 0.99:
        sombra_suelo(lz, X, Y, 0.30 * spr.w * s * sx, 0.035 * alto, op=suelo * op)
    a = math.radians(rot)
    T1 = np.array([[1, 0, -ancla[0] * spr.w], [0, 1, -ancla[1] * spr.h], [0, 0, 1]], np.float64)
    S = np.diag([s * sx * (-1.0 if flip else 1.0), s * sy, 1.0])
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]], np.float64)
    T2 = np.array([[1, 0, X], [0, 1, Y], [0, 0, 1]], np.float64)
    D.pegar(lz, spr, T2 @ R @ S @ T1, op)


def respira(t, f=0.35, a=0.012, fase=0.0):
    """Factor de escala vertical para la respiración/espera de un personaje quieto."""
    return 1.0 + a * math.sin(2 * math.pi * f * t + fase)


def entra(t, t0, dur=0.45):
    """0→1 con rebote (la pegatina «se pega»)."""
    return e_back(clamp01((t - t0) / dur)) if t >= t0 else 0.0


# ---------------------------------------------------------------- ambiente
@functools.lru_cache(maxsize=8)
def _gauss(n=64):
    x = np.linspace(-2, 2, n, dtype=np.float32)
    return np.exp(-(x[:, None] ** 2 + x[None, :] ** 2))


def _blob(lz, X, Y, r, color, op, aditivo=False):
    r = max(r, 1.0)
    n = int(max(4, min(2 * r, 400)))
    g = cv2.resize(_gauss(), (n, n)) * op
    x0, y0 = int(X - n / 2), int(Y - n / 2)
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + n, W), min(y0 + n, H)
    if xb <= xa or yb <= ya:
        return
    gg = g[ya - y0:yb - y0, xa - x0:xb - x0][..., None]
    c = np.float32(color)
    if aditivo:
        lz[ya:yb, xa:xb] += gg * c
    else:
        lz[ya:yb, xa:xb] = lz[ya:yb, xa:xb] * (1 - gg) + c * gg


def humo(lz, t, X, Y, s=1.0, n=7, color=(0.86, 0.84, 0.80), op=0.30, sem=0, alto=260.0):
    """Columna de humo que sube y se abre desde (X, Y)."""
    for i in range(n):
        u = (t * 0.16 + i / n + 0.137 * sem) % 1.0
        x = X + (math.sin(u * 3.1 + i * 1.7 + sem) * 14 + u * 46) * s
        y = Y - u * alto * s
        _blob(lz, x, y, (12 + u * 58) * s, color, op * (1 - u) * smooth(clamp01(u * 5)))


def brillo(lz, X, Y, r, color=(1.0, 0.55, 0.18), inten=0.5, t=0.0, sem=0):
    """Halo aditivo que titila (fogatas, antorchas)."""
    fl = 0.78 + 0.14 * math.sin(t * 11.3 + sem) + 0.08 * math.sin(t * 23.7 + 2 * sem)
    _blob(lz, X, Y, r, color, inten * fl, aditivo=True)


def chispas(lz, t, X, Y, s=1.0, n=10, sem=0):
    for i in range(n):
        u = (t * 0.55 + i / n + 0.31 * sem) % 1.0
        x = X + math.sin(i * 2.3 + u * 6 + sem) * 22 * s
        y = Y - u * 160 * s
        _blob(lz, x, y, 3.2 * s, (1.0, 0.70, 0.25), 0.9 * (1 - u), aditivo=True)


def arena_viento(lz, t, fuerza=1.0, y0=0.62, y1=1.0, n=90, sem=0, color=(0.93, 0.80, 0.58)):
    """Granos de arena que el viento arrastra por la franja baja de la pantalla (y0..y1 relativos)."""
    if fuerza <= 0.01:
        return
    r = np.random.default_rng(sem)
    base = r.random((n, 4))
    for bx, by, bv, bs in base:
        vel = 380 + 520 * bv
        x = (bx * (W + 300) + t * vel) % (W + 300) - 150
        y = H * (y0 + (y1 - y0) * by) + math.sin(t * 3 + bx * 20) * 12
        _blob(lz, x, y, 2.0 + 3.5 * bs, color, 0.55 * fuerza)
        _blob(lz, x - 18 - 30 * bv, y, 1.6 + 2.5 * bs, color, 0.22 * fuerza)


def destellos(lz, t, pts, s=1.0, color=(1.0, 0.98, 0.90)):
    """Brillos del agua en puntos de pantalla `pts` [(X, Y, fase)]."""
    for X, Y, f in pts:
        v = max(0.0, math.sin(t * 2.4 + f * 6.283)) ** 6
        if v > 0.02:
            _blob(lz, X, Y, 7 * s, color, 0.55 * v, aditivo=True)


@functools.lru_cache(maxsize=8)
def puntos_agua(fondo, n=70, sem=3):
    """Puntos (x, y) normalizados sobre el río (píxeles turquesa) del escenario, para los destellos."""
    rgb = _fondo_rgb(fondo)
    hsv = cv2.cvtColor(cv2.resize(rgb, (rgb.shape[1] // 4, rgb.shape[0] // 4)), cv2.COLOR_RGB2HSV)
    m = (hsv[..., 0] > 78) & (hsv[..., 0] < 100) & (hsv[..., 1] > 70) & (hsv[..., 2] > 70)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return ()
    r = np.random.default_rng(sem)
    sel = r.choice(len(xs), size=min(n, len(xs)), replace=False)
    hh, ww = m.shape
    return tuple((float(xs[i]) / ww, float(ys[i]) / hh, float(r.random())) for i in sel)


# ---------------------------------------------------------------- texto de énfasis: tira de papel recortado
@functools.lru_cache(maxsize=64)
def _tira(txt, px, tinta=(48, 30, 22), papel=(246, 236, 212), fnt="serif"):
    import docu as D
    f = D.fuente(fnt, px)
    x0, y0, x1, y1 = f.getbbox(txt)
    pw, ph = int(px * 0.55), int(px * 0.30)
    w, h = x1 - x0 + 2 * pw, y1 - y0 + 2 * ph
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    r = np.random.default_rng(len(txt) * 7 + px)
    pol = [(r.uniform(0, 6), r.uniform(0, 5)), (w - r.uniform(0, 6), r.uniform(0, 5)),
           (w - r.uniform(0, 6), h - r.uniform(0, 5)), (r.uniform(0, 6), h - r.uniform(0, 5))]
    dr.polygon(pol, fill=papel + (255,))
    dr.text((pw - x0, ph - y0), txt, font=f, fill=tinta + (255,))
    a = np.asarray(im, np.uint8)
    grano = (r.normal(0, 5, a.shape[:2])).astype(np.float32)
    rgb = np.clip(a[..., :3].astype(np.float32) + grano[..., None], 0, 255).astype(np.uint8)
    return D.Sprite(rgb, a[..., 3].astype(np.float32) / 255.0, sombra=True, sr=6, off=(6, 9), sop=0.45)


def rotulo(lz, txt, X, Y, px, t, t0, t1=None, rot=-2.0, op=1.0, salida=0.3, **kw):
    """Tira de papel con texto que se pega con rebote en t0 y se despega en t1."""
    import docu as D
    if t < t0:
        return
    u = entra(t, t0, 0.42)
    o = op
    if t1 is not None:
        o *= 1.0 - smooth(clamp01((t - t1) / salida))
    if o <= 0.01:
        return
    spr = _tira(txt, px, **kw)
    s = 0.55 + 0.45 * u
    a = math.radians(rot + (1 - u) * 9)
    T1 = np.array([[1, 0, -spr.w / 2], [0, 1, -spr.h / 2], [0, 0, 1]], np.float64)
    S = np.diag([s, s, 1.0])
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]], np.float64)
    T2 = np.array([[1, 0, X], [0, 1, Y], [0, 0, 1]], np.float64)
    D.pegar(lz, spr, T2 @ R @ S @ T1, o * clamp01(u * 3))


def acabado(img, t, vineta=0.42, grano=0.028, calido=0.03):
    import docu as D
    return D.acabado(img, t, fuerza_vineta=vineta, grano=grano, polvo=0.10, teal=0.0, calido=calido, sat=1.0)


# ---------------------------------------------------------------- tiempos de la voz
def T(TL, eid, pref, frase=None, n=0, fin=False):
    """Tiempo (s) de la n-ésima palabra que empieza por `pref` en la escena `eid` (opcionalmente en la frase `frase`)."""
    pref = pref.lower()
    for e in TL["escenas"]:
        if e["id"] != eid:
            continue
        k = 0
        for i, fr in enumerate(e["frases"]):
            if frase is not None and i != frase:
                continue
            for w in fr["words"]:
                lw = w["w"].lower().strip(".,;:¡!¿?«»\"'")
                if lw.startswith(pref):
                    if k == n:
                        return w["e"] if fin else w["s"]
                    k += 1
    raise KeyError((eid, pref, frase, n))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "recortar":
        recortar_video(sys.argv[2], sys.argv[3:] or None)
    else:
        print(__doc__)
