# -*- coding: utf-8 -*-
"""IMÁGENES VIVAS del motor SECUENCIA: las imágenes fijas de Flow dejan de ser fotos quietas (19-oct-2026).
  · parallax 2.5D: el fondo se desplaza por su mapa de profundidad (Depth Anything V2 Small, preparar_profundidad.py; mismo
    remuestreo que docu.foto_parallax), lo cercano más que lo lejano, en la dirección en que ya va la cámara del beat;
  · recorte vivo: el personaje (o 2-3 personajes / un objeto: lupa, matamoscas) se separa con rembg, el hueco del fondo se
    rellena (cv2.inpaint TELEA, máscara dilatada para que el contorno negro se vaya con el personaje) y el recorte se mueve
    ENCIMA con pivote en los pies: respira, baile, flota, balanceo o solo parallax. Movimientos pequeños (2-4°, pocos px,
    squash leve) y el recorte un 4 % más grande (`escala`, idea del usuario) para que tape el borde del hueco.

Caché en medios/capas/<beat>/ (se rehace sola si cambia la imagen):
  prof.png (profundidad 0..255, 255 = cerca) · mask_<modelo>.png (alfa de rembg) · rec_<modelo>_<n>.png (recorte RGBA) ·
  fondo_<modelo>_<capas>.jpg + proff_<modelo>_<capas>.png (fondo sin esos recortes y su profundidad) · info.json

  python fab.py <v> vivo                      = candidatos
  python fab.py <v> vivo candidatos [--todas]  prepara TODAS las imágenes y propone las vivas: máscara entre el 8 y el 55 % del
                                               cuadro con 1-3 componentes; imprime líneas FX para efectos.py y la hoja previews/vivo_NN.jpg
  python fab.py <v> vivo preparar [ids] [--solo-prof] [--forzar] [--modelo isnet-anime]   solo la caché
  python fab.py <v> vivo hoja scene-032 scene-037 ...   hoja antes/después de esas (aunque no sean candidatas)
Modelos de rembg: primero `isnet-general-use` y, si no da un recorte candidato, `isnet-anime` (probados en doce_animales:
el general recorta mejor este dibujo de tinta; el anime se come el suelo o el dedo). `modelo=` en el FX fuerza uno.
Uso en efectos.py: FX = [dict(tipo="vivo", beat="scene-045", anim="baile", capa=None, amp=1.0), ...]  y  VIVO_AUTO = 12
(parallax suave de 12 px en TODAS las imágenes sin FX vivo). Detalle: docs/estilo_secuencia_flow.md § «Imágenes vivas».
"""
import json
import math
import os
import sys

import cv2
import numpy as np

CARPETA = os.path.join("medios", "capas")
VERSION = 2                      # súbela al cambiar cómo se recorta: la caché rehace recortes y fondos (no rembg ni profundidad)
MODELOS = ("isnet-general-use", "isnet-anime")
AREA_MIN, AREA_MAX, COMP_MIN, COMP_MAX = 0.08, 0.55, 0.008, 3   # candidata: máscara del 8-55 % del cuadro, 1-3 componentes
ESCALA = 1.04                    # el recorte, un poco más grande que el original: tapa el borde del hueco rellenado
PAR_AUTO, PAR_VIVO = 12.0, 16.0  # px de pantalla entre lo más cerca y lo más lejos (parallax del fondo)
GIRO_ALTO = 300                  # un recorte de más de 300 px de alto gira proporcionalmente menos (3° en 300 px ≈ 16 px de vaivén)
ANIMS = ("respira", "baile", "flota", "balanceo", "parallax")
TAU = 2 * math.pi
EXT_IMG = (".jpg", ".jpeg", ".png", ".webp")


# ---------------------------------------------------------------- disco
def _leer(r, fl=cv2.IMREAD_COLOR):
    im = cv2.imdecode(np.fromfile(r, np.uint8), fl)
    if im is None:
        raise SystemExit(f"vivo: no pude leer {r}")
    return im


def _escribir(r, im):
    ext = os.path.splitext(r)[1]
    ok, buf = cv2.imencode(ext, im, [cv2.IMWRITE_JPEG_QUALITY, 95] if ext == ".jpg" else [])
    buf.tofile(r)


def _dir(i):
    d = os.path.join(CARPETA, i)
    os.makedirs(d, exist_ok=True)
    return d


def _firma(r):
    st = os.stat(r)
    return [st.st_size, round(st.st_mtime)]


def _info(i):
    p = os.path.join(CARPETA, i, "info.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def _guardar(i, info):
    json.dump(info, open(os.path.join(_dir(i), "info.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def ruta_de(i):
    for ext in EXT_IMG:
        r = os.path.join("medios", i + ext)
        if os.path.exists(r) and os.path.getsize(r) > 2000:
            return r
    return None


# ---------------------------------------------------------------- modelos (perezosos)
_IA = {}


def _pipe_prof():
    if "prof" not in _IA:
        os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
        os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
        import preparar_profundidad as P
        from transformers.utils import logging as tlog
        tlog.disable_progress_bar()
        _IA["prof"] = P.modelo()
    return _IA["prof"]


def _rembg(modelo):
    if modelo not in _IA:
        from rembg import new_session
        _IA[modelo] = new_session(modelo)
    return _IA[modelo]


# ---------------------------------------------------------------- preparación
def _llenar(c):
    """Rellena los huecos interiores de un componente. En el dibujo de tinta y color plano rembg marca el CONTORNO y deja fuera
    el relleno de color (camisa, pantalón, el vidrio de la lupa): sin esto el recorte sale hueco y deja ver el fondo rellenado.
    Los lados que tocan el borde de la imagen se sellan antes (la camisa cortada por abajo también es un hueco)."""
    s = c.astype(np.uint8)
    for lc, ls in ((c[0], s[0]), (c[-1], s[-1]), (c[:, 0], s[:, 0]), (c[:, -1], s[:, -1])):
        nz = np.flatnonzero(lc)
        if nz.size:
            ls[nz.min():nz.max() + 1] = 1
    inv = (s == 0).astype(np.uint8)
    _, l2 = cv2.connectedComponents(inv, connectivity=4)
    fuera = np.unique(np.concatenate([l2[0], l2[-1], l2[:, 0], l2[:, -1]]))
    return (s > 0) | ((inv > 0) & ~np.isin(l2, fuera))


def _componentes(mask):
    """Máscara 0..255 -> (etiquetas, [(etiqueta, x, y, w, h, área relativa)]) de los componentes que cuentan (ya rellenos), de
    mayor a menor. Un componente que cae dentro de otro ya relleno (la mosca dentro del aro de la lupa) se queda en ese."""
    b = cv2.morphologyEx((mask > 100).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(b, connectivity=8)
    N = mask.shape[0] * mask.shape[1]
    out, cs = np.zeros(mask.shape, np.int32), []
    for j in sorted(range(1, n), key=lambda j: -st[j, 4]):
        if st[j, 4] / N < COMP_MIN / 3:                # piezas sueltas (rayas del suelo): se quedan en el fondo
            break
        x, y, ww, hh = map(int, st[j, :4])
        cj = lab[y:y + hh, x:x + ww] == j
        if (out[y:y + hh, x:x + ww][cj] > 0).mean() > 0.5:
            continue
        for c in _partir(_llenar(lab == j) & (out == 0), N):
            ys, xs = np.nonzero(c)
            out[c] = len(cs) + 1
            cs.append((len(cs) + 1, int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1),
                       c.sum() / N))
    return out, sorted(cs, key=lambda c: -c[5])


def _partir(c, N):
    """Separa piezas sólidas unidas por trazos finos (la mariquita, la uña y la cabeza unidas por el contorno del dedo): abre la
    forma; cada trazo fino que quedó fuera vuelve a la ÚNICA pieza que toca (patas, antenas, mango del matamoscas) y, si toca
    dos o más, es un puente y se queda en el fondo."""
    k = max(5, round(0.005 * c.shape[1])) | 1
    c2 = cv2.morphologyEx(c.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    n, l, st, _ = cv2.connectedComponentsWithStats(c2, connectivity=8)
    piezas = [s for s in range(1, n) if st[s, 4] / N >= COMP_MIN]
    if not piezas:
        return []
    l = np.where(np.isin(l, piezas), l, 0)
    fino = (c & (l == 0)).astype(np.uint8)
    nf, lf, sf, _ = cv2.connectedComponentsWithStats(fino, connectivity=8)
    lv = cv2.dilate(l.astype(np.float32), np.ones((3, 3), np.uint8)).astype(np.int32)     # vecindad de cada pieza
    lv2 = -cv2.dilate(-np.where(l > 0, l, 1 << 20).astype(np.float32), np.ones((3, 3), np.uint8)).astype(np.int32)
    corto = 0.06 * c.shape[1]
    for f in range(1, nf):
        x, y, w, h = sf[f, :4]
        diag = math.hypot(w, h)
        if diag > corto and (sf[f, 4] / (w * h) < 0.2 or sf[f, 4] / diag < 0.008 * c.shape[1]):
            continue                                   # línea larga, rala o delgada (contorno de la mesa o del dedo): es del fondo
        m = lf[y:y + h, x:x + w] == f
        toca = set(np.unique(lv[y:y + h, x:x + w][m])) | set(np.unique(lv2[y:y + h, x:x + w][m]))
        toca = {t for t in toca if t in piezas}
        if len(toca) == 1:
            l[y:y + h, x:x + w][m] = toca.pop()
    return [l == s for s in piezas]


def _resumen(mask, prof):
    h, w = mask.shape
    lab, cs = _componentes(mask)
    out = []
    for j, x, y, ww, hh, a in cs:
        toca = "".join(c for c, si in (("i", x <= 2), ("d", x + ww >= w - 2), ("a", y <= 2), ("b", y + hh >= h - 2)) if si)
        out.append(dict(area=round(a, 4), caja=[x, y, ww, hh], toca=toca,
                        prof=round(float(prof[lab == j].mean()) / 255, 3) if prof is not None else 0.7))
    return out


def es_candidata(comps):
    tot = sum(c["area"] for c in comps)
    return AREA_MIN <= tot <= AREA_MAX and 1 <= len(comps) <= COMP_MAX


def sugerir(comps, alto):
    """Animación propuesta según la forma de la máscara."""
    if len(comps) >= 2:
        return "baile"
    c = comps[0]
    x, y, w, h = c["caja"]
    if "b" not in c["toca"] and (y + h) / alto < 0.88:
        return "flota"
    return "respira" if c["area"] > 0.3 else "balanceo"


def preparar(i, modelos=None, forzar=False, solo_prof=False):
    """Profundidad + máscaras de rembg de la imagen del beat `i`. Devuelve info (con 'elegido' = modelo candidato o None)."""
    ruta = ruta_de(i)
    if ruta is None:
        return None
    d, info = _dir(i), _info(i)
    if forzar or info.get("firma") != _firma(ruta):
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
        info = dict(firma=_firma(ruta), mascaras={}, v=VERSION)
    elif info.get("v") != VERSION:                     # cambió la lógica del kit: rehace recortes y fondos, no rembg ni profundidad
        for f in os.listdir(d):
            if f.startswith(("rec_", "fondo_", "proff_")):
                os.remove(os.path.join(d, f))
        pp = os.path.join(d, "prof.png")
        prof = _leer(pp, cv2.IMREAD_GRAYSCALE) if os.path.exists(pp) else None
        info = dict(firma=info["firma"], v=VERSION, mascaras={mo: _resumen(_leer(os.path.join(d, f"mask_{mo}.png"),
                                                                                    cv2.IMREAD_GRAYSCALE), prof)
                                                              for mo in info.get("mascaras", {})})
    im = None
    pp = os.path.join(d, "prof.png")
    if not os.path.exists(pp):
        from PIL import Image
        import preparar_profundidad as P
        im = _leer(ruta)
        m = P.mapa(_pipe_prof(), Image.fromarray(im[..., ::-1]))
        _escribir(pp, (cv2.resize(m, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_LINEAR) * 255).astype(np.uint8))
    if not solo_prof:
        prof = _leer(pp, cv2.IMREAD_GRAYSCALE)
        for mo in (modelos or MODELOS):
            if mo not in info["mascaras"]:
                from PIL import Image
                from rembg import remove
                im = _leer(ruta) if im is None else im
                mask = np.asarray(remove(Image.fromarray(im[..., ::-1]), session=_rembg(mo), only_mask=True))
                _escribir(os.path.join(d, f"mask_{mo}.png"), mask)
                info["mascaras"][mo] = _resumen(mask, prof)
            if es_candidata(info["mascaras"][mo]) and not modelos:
                break                                   # el primero que da un recorte candidato gana: no gastes el siguiente
        info["elegido"] = next((mo for mo in MODELOS if mo in info["mascaras"] and es_candidata(info["mascaras"][mo])), None)
    _guardar(i, info)
    return info


def _recorte(i, im, mask, prof, modelo, n, lab, comp):
    """Recorte RGBA del componente n (con el contorno negro) + su caja y pivotes. Cacheado en rec_<modelo>_<n>.png."""
    d = os.path.join(CARPETA, i)
    p = os.path.join(d, f"rec_{modelo}_{n}.png")
    info = _info(i)
    clave = f"{modelo}_{n}"
    if os.path.exists(p) and clave in info.get("recortes", {}):
        return _leer(p, cv2.IMREAD_UNCHANGED), info["recortes"][clave]
    h, w = mask.shape
    j, x, y, ww, hh, _ = comp
    c = (lab == j).astype(np.uint8)
    el = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    # alfa casi binario: lo semitransparente de rembg (brazos blancos, alas) dejaba ver el relleno borroso a través del recorte
    oscuro = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) < 85                    # la tinta del contorno que rembg deja fuera
    banda = cv2.dilate(c, el(max(3, round(0.004 * w)))).astype(bool)
    alfa = (cv2.dilate(c, el(1)).astype(bool) | (oscuro & banda)).astype(np.float32)
    alfa = cv2.GaussianBlur(alfa, (0, 0), 0.8)
    ys, xs = np.nonzero(alfa > 0.02)
    x0, y0, x1, y1 = max(xs.min() - 3, 0), max(ys.min() - 3, 0), min(xs.max() + 4, w), min(ys.max() + 4, h)
    rgba = np.dstack([im[y0:y1, x0:x1], (alfa[y0:y1, x0:x1] * 255).astype(np.uint8)])
    pie = c[y + int(hh * .82):y + hh].nonzero()[1]                         # pies: centro de la franja baja del componente
    datos = dict(origen=[int(x0), int(y0)], caja=[x, y, ww, hh], pies=[float(pie.mean()) if pie.size else x + ww / 2, y + hh],
                 centro=[x + ww / 2, y + hh / 2], prof=float(prof[c > 0].mean()) / 255,
                 toca="".join(s for s, si in (("i", x0 <= 0), ("d", x1 >= w), ("a", y0 <= 0), ("b", y1 >= h)) if si))
    _escribir(p, rgba)
    info.setdefault("recortes", {})[clave] = datos
    _guardar(i, info)
    return rgba, datos


def capas(i, sel=None, modelo=None):
    """Capas del beat en la resolución original: fondo sin los recortes `sel`, su profundidad y la lista de recortes."""
    ruta = ruta_de(i)
    info = _info(i)
    if not info or info.get("firma") != _firma(ruta) or not info.get("mascaras"):
        raise SystemExit(f"vivo: falta preparar {i} (python fab.py <v> vivo preparar {i})")
    if info.get("v") != VERSION:
        info = preparar(i)
    modelo = modelo or info.get("elegido") or next(iter(info["mascaras"]))
    if modelo not in info["mascaras"]:
        info = preparar(i, modelos=[modelo])
    d = os.path.join(CARPETA, i)
    im, prof = _leer(ruta), _leer(os.path.join(d, "prof.png"), cv2.IMREAD_GRAYSCALE)
    mask = _leer(os.path.join(d, f"mask_{modelo}.png"), cv2.IMREAD_GRAYSCALE)
    lab, cs = _componentes(mask)
    if not cs:
        raise SystemExit(f"vivo: {i} no tiene ningún recorte con {modelo} (prueba modelo= o déjalo solo con parallax)")
    sel = list(range(len(cs))) if sel is None else ([sel] if isinstance(sel, int) else list(sel))
    if any(n >= len(cs) for n in sel):
        raise SystemExit(f"vivo: {i} solo tiene {len(cs)} capas con {modelo} (capa={sel}); mira previews/vivo_NN.jpg")
    recs = [_recorte(i, im, mask, prof, modelo, n, lab, cs[n]) for n in sel]
    clave = f"{modelo}_{'-'.join(map(str, sel))}"
    pf, pd = os.path.join(d, f"fondo_{clave}.jpg"), os.path.join(d, f"proff_{clave}.png")
    if os.path.exists(pf) and os.path.exists(pd):
        return _leer(pf), _leer(pd, cv2.IMREAD_GRAYSCALE), recs
    h, w = mask.shape
    hueco = np.zeros((h, w), np.uint8)
    for rgba, dt in recs:
        x0, y0 = dt["origen"]
        hueco[y0:y0 + rgba.shape[0], x0:x0 + rgba.shape[1]] |= (rgba[..., 3] > 10).astype(np.uint8)
    r = max(4, round(0.006 * w))
    hueco = cv2.dilate(hueco, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
    fondo = _rellenar(im, hueco)
    pr = cv2.inpaint(cv2.resize(prof, (w // 4, h // 4), interpolation=cv2.INTER_AREA),
                     cv2.resize(hueco, (w // 4, h // 4), interpolation=cv2.INTER_NEAREST), 5, cv2.INPAINT_TELEA)
    pr = np.where(hueco > 0, cv2.resize(pr, (w, h), interpolation=cv2.INTER_LINEAR), prof).astype(np.uint8)
    _escribir(pf, fondo)
    _escribir(pd, pr)
    return fondo, pr, recs


def _rellenar(im, hueco):
    """Fondo sin el personaje: TELEA a media resolución (rápido aunque el hueco sea la mitad del cuadro) y un suavizado dentro
    del hueco para que no queden vetas; fuera del hueco, los píxeles originales."""
    h, w = hueco.shape
    s = cv2.resize(im, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    m = cv2.dilate(cv2.resize(hueco, (w // 2, h // 2), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
    r = cv2.inpaint(s, m, 7, cv2.INPAINT_TELEA)
    r = np.where(m[..., None] > 0, cv2.GaussianBlur(r, (0, 0), 2.5), r)
    up = cv2.resize(r, (w, h), interpolation=cv2.INTER_CUBIC)
    k = cv2.GaussianBlur(hueco.astype(np.float32), (0, 0), 1.5)[..., None]
    return (im * (1 - k) + up * k).astype(np.uint8)


# ---------------------------------------------------------------- render
_GRID = {}


def _grid(W, H):
    if (W, H) not in _GRID:
        _GRID[(W, H)] = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return _GRID[(W, H)]


def _caja_cubrir(iw, ih, W, H):
    """La misma caja que secuencia._cubrir: (x, y, w, h) del recorte al aspecto W:H."""
    if iw * H > ih * W:
        nw = int(round(ih * W / H))
        return (iw - nw) // 2, 0, nw, ih
    nh = int(round(iw * H / W))
    return 0, (ih - nh) // 2, iw, nh


def mov(anim, s, fase, A):
    """(giro °, escala x, escala y, dx px, dy px) del recorte a los s segundos. Todo pequeño: el hueco casi no se ve."""
    if anim == "respira":
        w = math.sin(TAU * s / 2.8 + fase)
        return 0.7 * A * math.sin(TAU * s / 5.6 + fase), 1 - 0.008 * A * w, 1 + 0.018 * A * w, 0.0, 0.0
    if anim == "balanceo":
        return 3.0 * A * math.sin(TAU * s / 2.6 + fase), 1.0, 1 + 0.006 * A * math.sin(2 * TAU * s / 2.6 + fase), 0.0, 0.0
    if anim == "baile":                                  # vaivén + rebote (squash) dos veces por vaivén, sin despegar los pies
        w, b = math.sin(TAU * s / 1.3 + fase), math.sin(2 * (TAU * s / 1.3 + fase))
        return 3.2 * A * w, 1 + 0.014 * A * b, 1 - 0.022 * A * b, 2.5 * A * w, 0.0
    if anim == "flota":
        return (1.6 * A * math.sin(TAU * s / 3.9 + fase), 1.0, 1.0, 3.0 * A * math.sin(TAU * s / 4.7 + fase),
                -6.0 * A * math.sin(TAU * s / 3.2 + fase))
    return 0.0, 1.0, 1.0, 0.0, 0.0


class Vivo:
    """Fuente del motor secuencia (como Imagen): fondo con parallax por profundidad + recortes animados encima, con la MISMA
    cámara que tendría la imagen fija (`base.matriz(t)`). d = el FX de efectos.py (tipo vivo) o dict(auto=True, par=N)."""

    def __init__(self, base, b, d):
        import secuencia as S
        self.base, self.b, self.d = base, b, d
        self.W, self.H, self.SW, self.SH = S.W, S.H, base.SW, base.SH
        i = b["id"]
        ruta = ruta_de(i)
        ih, iw = _leer(ruta).shape[:2]
        cx, cy, cw, ch = _caja_cubrir(iw, ih, self.W, self.H)
        self.sx, self.sy, self.c0 = self.SW / cw, self.SH / ch, (cx, cy)
        a_sw = lambda im, inter: cv2.resize(im[cy:cy + ch, cx:cx + cw], (self.SW, self.SH), interpolation=inter)
        self.anim = d.get("anim", "parallax")
        if self.anim not in ANIMS:
            raise SystemExit(f"efectos.py: anim «{self.anim}» no existe (hay {', '.join(ANIMS)})")
        self.amp, self.esc = float(d.get("amp", 1.0)), float(d.get("escala", ESCALA))
        auto = d.get("auto")
        self.par = float(d.get("par", PAR_AUTO if auto else PAR_VIVO))
        self.recs = []
        if auto:                                         # solo parallax: la imagen original y su profundidad
            fondo, prof = base.im, None
            pp = os.path.join(CARPETA, i, "prof.png")
            prof = a_sw(_leer(pp, cv2.IMREAD_GRAYSCALE), cv2.INTER_LINEAR)
        else:
            fondo0, prof0, recs = capas(i, d.get("capa"), d.get("modelo"))
            fondo = a_sw(fondo0, cv2.INTER_LANCZOS4 if cw < self.SW else cv2.INTER_AREA)
            prof = a_sw(prof0, cv2.INTER_LINEAR)
            piv = d.get("pivote", "centro" if self.anim == "flota" else "pies")
            for n, (rgba, dt) in enumerate(sorted(recs, key=lambda r: r[1]["prof"])):    # lo más cercano, encima
                self.recs.append(self._rec_sw(rgba, dt, piv, n))
        self.fondo = fondo
        self.prof = cv2.GaussianBlur(prof.astype(np.float32) / 255, (0, 0), 0.012 * self.SW)   # sin escalones: no dobla la tinta
        self.dir = self._direccion()
        self.t0, self.dur = b["t0"], max(0.5, b["t1"] - b["t0"])
        self.de, self.a = d.get("de", b["t0"]), d.get("a", b["t1"])
        self.entra = d.get("entra", 0.5) if self.de > b["t0"] + 0.05 else 0.0   # anclado a una palabra: entra suave
        self.sale = d.get("sale", 0.4) if self.a < b["t1"] - 0.05 else 0.0

    def _rec_sw(self, rgba, dt, piv, n):
        """Recorte llevado a la imagen ampliada (SW) con relleno repetido en los lados que tocan el borde de la imagen."""
        x0, y0 = dt["origen"]
        h, w = rgba.shape[:2]
        nw, nh = max(1, round(w * self.sx)), max(1, round(h * self.sy))
        r = cv2.resize(rgba, (nw, nh), interpolation=cv2.INTER_LANCZOS4 if nw > w else cv2.INTER_AREA)
        ox, oy = (x0 - self.c0[0]) * self.sx, (y0 - self.c0[1]) * self.sy
        P = int(0.05 * self.SW)
        t, b_, l, d_ = (P if s in dt["toca"] else 0 for s in "abid")
        if t or b_ or l or d_:                        # el cuerpo sigue más allá del borde: al girar no asoma el hueco
            r = cv2.copyMakeBorder(r, t, b_, l, d_, cv2.BORDER_REPLICATE)
            ox, oy = ox - l, oy - t
        px, py = dt["centro"] if piv == "centro" else dt["pies"] if piv == "pies" else (
            dt["caja"][0] + piv[0] * dt["caja"][2], dt["caja"][1] + piv[1] * dt["caja"][3])
        alto = dt["caja"][3] * self.sy * self.W / self.SW            # alto en pantalla (sin zoom)
        return dict(im=r, o=(ox, oy), piv=((px - self.c0[0]) * self.sx, (py - self.c0[1]) * self.sy), prof=dt["prof"],
                    fase=n * (math.pi if self.anim == "baile" else 1.7), giro=min(1.0, GIRO_ALTO / max(alto, 1)))

    def _direccion(self):
        """Hacia dónde empuja el parallax: la deriva de la cámara (lo cercano se adelanta) o, si solo hay zoom, radial."""
        bs = self.base
        if bs.cam:
            (z0, x0, y0), (z1, x1, y1) = bs.cam["a"], bs.cam["b"]
            v, dz = (-(x1 - x0), -(y1 - y0)), z1 - z0
        else:
            v, dz = (bs.d[2] - bs.d[0], bs.d[3] - bs.d[1]), bs.z[1] - bs.z[0]
        n = math.hypot(*v)
        if n > 0.05:
            return ("lineal", v[0] / n, v[1] / n)
        return ("radial", 1.0 if dz >= 0 else -1.0, 0.0)

    def _env(self, t):
        e = min(1.0, max(0.0, (t - self.de) / self.entra)) if self.entra else (1.0 if t >= self.de else 0.0)
        if self.sale:
            e *= min(1.0, max(0.0, (self.a - t) / self.sale))
        elif t >= self.a:
            e = 0.0
        return e * e * (3 - 2 * e)

    def cuadro(self, t):
        W, H = self.W, self.H
        M = self.base.matriz(t)
        esc, tx, ty = float(M[0, 0]), float(M[0, 2]), float(M[1, 2])
        X, Y = _grid(W, H)
        ph = (t - self.t0) / self.dur - 0.5               # va de -0.5 a 0.5 con la cámara (lineal, como ella)
        Sx, Sy = (X - tx) / esc, (Y - ty) / esc
        k = cv2.remap(self.prof, Sx, Sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) - 0.5
        modo, a1, a2 = self.dir
        if modo == "lineal":
            dx, dy = self.par * ph * a1, self.par * ph * a2
            Sx, Sy = Sx - k * dx / esc, Sy - k * dy / esc
        else:
            g = self.par * ph * a1 / (W / 2)
            Sx, Sy = Sx - k * g * (X - W / 2) / esc, Sy - k * g * (Y - H / 2) / esc
        f = cv2.remap(self.fondo, Sx, Sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if not self.recs:
            return f
        e, s = self._env(t), t - self.de
        mult = 1.8 if self.anim == "parallax" else 1.0
        for r in self.recs:
            giro, ex, ey, mx, my = mov(self.anim, max(0.0, s), r["fase"], self.amp * e)
            giro *= r["giro"]                             # lo grande gira menos: su borde no se aleja más que en uno chico
            px, py = r["piv"]
            c, sn = math.cos(math.radians(giro)), math.sin(math.radians(giro))
            ex, ey = ex * self.esc, ey * self.esc
            A = np.array([[c * ex, sn * ey, 0], [-sn * ex, c * ey, 0], [0, 0, 1]], np.float64)   # giro + escala sobre el pivote
            A[0, 2], A[1, 2] = px - A[0, 0] * px - A[0, 1] * py, py - A[1, 0] * px - A[1, 1] * py
            kc = r["prof"] - 0.5
            sxp, syp = esc * px + tx, esc * py + ty                                   # el pivote en pantalla
            if modo == "lineal":
                dx, dy = self.par * ph * a1 * kc * mult, self.par * ph * a2 * kc * mult
            else:
                g = self.par * ph * a1 / (W / 2) * kc * mult
                dx, dy = g * (sxp - W / 2), g * (syp - H / 2)
            C = np.vstack([M.astype(np.float64), [0, 0, 1]]) @ A @ np.array([[1, 0, r["o"][0]], [0, 1, r["o"][1]], [0, 0, 1]])
            C[0, 2] += dx + mx
            C[1, 2] += dy + my
            h, w = r["im"].shape[:2]
            esq = C[:2] @ np.array([[0, w, 0, w], [0, 0, h, h], [1, 1, 1, 1]], np.float64)
            x0, y0 = max(int(esq[0].min()) - 2, 0), max(int(esq[1].min()) - 2, 0)
            x1, y1 = min(int(esq[0].max()) + 3, W), min(int(esq[1].max()) + 3, H)
            if x1 <= x0 or y1 <= y0:
                continue
            C[0, 2] -= x0
            C[1, 2] -= y0
            p = cv2.warpAffine(r["im"], C[:2].astype(np.float32), (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            al = p[..., 3:4].astype(np.float32) / 255
            f[y0:y1, x0:x1] = (f[y0:y1, x0:x1] * (1 - al) + p[..., :3] * al).astype(np.uint8)
        return f


def auto(base, b, par):
    """Parallax suave sin recorte (VIVO_AUTO de efectos.py) si la imagen tiene su profundidad; si no, la imagen de siempre."""
    r = ruta_de(b["id"])
    info = _info(b["id"])
    if r is None or info.get("firma") != _firma(r) or not os.path.exists(os.path.join(CARPETA, b["id"], "prof.png")):
        return None
    return Vivo(base, b, dict(auto=True, par=par))


# ---------------------------------------------------------------- selector y hoja
def _ids_imagen():
    import secuencia as S
    return [(k, b) for k, b in enumerate(S.cargar_beats()) if ruta_de(b["id"])]


PICO = dict(respira=0.7, balanceo=0.65, baile=0.33, flota=0.8, parallax=0.0)


def _mini(f, txt=None):
    m = cv2.resize(f, (480, 270), interpolation=cv2.INTER_AREA)
    if txt:
        cv2.rectangle(m, (0, 0), (480, 24), (20, 18, 18), -1)
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, 17), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1, cv2.LINE_AA)
    return m


def _fila(k, b, info, anim=None):
    import secuencia as S
    i = b["id"]
    ruta = ruta_de(i)
    mo = info.get("elegido") or next(iter(info["mascaras"]))
    comps = info["mascaras"][mo]
    im = _leer(ruta)
    anim = anim or (sugerir(comps, im.shape[0]) if comps else "parallax")
    mask = _leer(os.path.join(CARPETA, i, f"mask_{mo}.png"), cv2.IMREAD_GRAYSCALE)
    lab, cs = _componentes(mask)
    col = [(60, 60, 255), (255, 160, 40), (60, 220, 60)]
    ver = im.copy()
    for n, c in enumerate(cs):
        ver[lab == c[0]] = (ver[lab == c[0]] * .45 + np.float32(col[n % 3]) * .55).astype(np.uint8)
        cv2.putText(ver, str(n), (c[1] + c[3] // 2, c[2] + c[4] // 2), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 6, cv2.LINE_AA)
    tot = sum(c["area"] for c in comps)
    base = S.Imagen(ruta, b, k)
    if comps:
        fondo, _, _ = capas(i, None, mo)
        dv = dict(anim=anim, de=b["t0"], a=b["t1"])
    else:
        fondo, dv = im, dict(auto=True, par=PAR_VIVO)
    v = Vivo(base, b, dv)
    t = b["t0"] + PICO.get(anim, 0.5)
    cand = "CANDIDATA" if es_candidata(comps) else "no"
    return [_mini(im, f"{i}  original"), _mini(ver, f"{mo[:10]} {len(cs)} capas {tot * 100:.0f}%  {cand}"),
            _mini(fondo, "fondo rellenado"), _mini(v.cuadro(t), f"vivo: {anim}  t+{t - b['t0']:.2f}s")]


def hoja(ids=None, anims=None):
    """previews/vivo_NN.jpg: por imagen, original | capas numeradas | fondo rellenado | cuadro vivo en su pico (5 por hoja)."""
    pares = _ids_imagen()
    if ids:
        pares = [p for p in pares if p[1]["id"] in ids]
    os.makedirs("previews", exist_ok=True)
    filas = []
    for k, b in pares:
        info = preparar(b["id"])
        filas.append(np.hstack(_fila(k, b, info, (anims or {}).get(b["id"]))))
        print(f"  hoja: {b['id']}", flush=True)
    for h in range(0, len(filas), 5):
        r = f"previews/vivo_{h // 5 + 1:02d}.jpg"
        _escribir(r, np.vstack(filas[h:h + 5]))
        print(r)


def puntos(comps, dur, modelo):
    """Cuánto destaca el personaje: tamaño de la pieza principal (hasta 40 %), + dos personajes frente a frente, + beat largo,
    − si el recorte es del respaldo isnet-anime (en doce_animales 4 de sus 5 recomendadas arrastraban media escena)."""
    p = min(comps[0]["area"], 0.4)
    if len(comps) >= 2 and comps[1]["area"] >= 0.025:
        p += 0.12
    return p + (0.08 if dur >= 3.5 else 0.0) - (0.15 if modelo != MODELOS[0] else 0.0)


def candidatos(todas=False, cuota=0.2):
    """Prepara todas las imágenes, puntúa las candidatas y RECOMIENDA las que más destacan (no todas: ~20 % de las imágenes,
    nunca dos beats seguidos, pieza principal >= 12 %); el resto sale comentado por si se quiere alguna."""
    pares = _ids_imagen()
    print(f"vivo: preparando {len(pares)} imágenes (profundidad + rembg; caché en medios/capas/)", flush=True)
    sel = []
    for n, (k, b) in enumerate(pares):
        info = preparar(b["id"])
        mo = info.get("elegido")
        if mo:
            comps = info["mascaras"][mo]
            sel.append(dict(k=k, id=b["id"], mo=mo, comps=comps, anim=sugerir(comps, _leer(ruta_de(b["id"])).shape[0]),
                            p=puntos(comps, b["t1"] - b["t0"], mo)))
        if n % 10 == 9:
            print(f"  {n + 1}/{len(pares)}  candidatas: {len(sel)}", flush=True)
    tope, usados, rec = max(8, round(cuota * len(pares))), set(), []
    for s in sorted(sel, key=lambda s: -s["p"]):
        if len(rec) < tope and s["comps"][0]["area"] >= 0.12 and not ({s["k"] - 1, s["k"] + 1} & usados):
            rec.append(s)
            usados.add(s["k"])
    linea = lambda s: (f'dict(tipo="vivo", beat="{s["id"]}", anim="{s["anim"]}"'
                       + ("" if s["mo"] == MODELOS[0] else f', modelo="{s["mo"]}"') + f'),   # {len(s["comps"])} capa(s), '
                       f'{sum(c["area"] for c in s["comps"]) * 100:.0f} %, puntos {s["p"]:.2f}')
    print(f"\n{len(sel)} candidatas de {len(pares)} imágenes; RECOMENDADAS {len(rec)} (las que más destacan, sin dos seguidas).")
    print("Para efectos.py (revisa antes previews/vivo_NN.jpg; capa=N si una pieza es una cabeza cortada por el cuello):")
    for s in sorted(rec, key=lambda s: s["k"]):
        print("    " + linea(s))
    print("    # también candidatas (sin recomendar):")
    for s in sel:
        if s not in rec:
            print("    # " + linea(s))
    hoja(None if todas else [s["id"] for s in sorted(rec, key=lambda s: s["k"])])


if __name__ == "__main__":
    a = sys.argv[1:]
    op = a[0] if a and not a[0].startswith(("scene-", "-")) else "candidatos"
    ids = [x for x in a if x.startswith("scene-")]
    if op == "preparar":
        mo = [a[a.index("--modelo") + 1]] if "--modelo" in a else None
        todos = ids or [b["id"] for _, b in _ids_imagen()]
        for n, i in enumerate(todos):
            info = preparar(i, mo, forzar="--forzar" in a, solo_prof="--solo-prof" in a)
            print(f"  {i}: " + ("solo profundidad" if "--solo-prof" in a else f"candidata con {info.get('elegido')}"
                                 if info.get("elegido") else "sin recorte candidato (solo parallax)"), flush=True)
    elif op == "hoja":
        hoja(ids or None)
    else:
        candidatos(todas="--todas" in a)
