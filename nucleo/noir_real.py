# -*- coding: utf-8 -*-
"""Medios REALES en el estilo noir (regla del usuario, 8-oct-2026; docs/estilo_noir.md § «Medios reales»): las personas de las que
habla el guion salen con su FOTO REAL, y el video real (yt-dlp, Pexels, Pixabay) entra donde ayuda; todo convertido a blanco y negro
de tinta y aguada para que viva dentro del dibujo y no parezca pegado.

    import noir_real as R
    R.retrato_noir(h, "alan_turing", x, y, 520, t, t0, rotulo="ALAN TURING", leyenda="1912 - 1954")   # ficha: foto pegada con cinta
    R.foto_noir(h, "sala_servidores", t, t_ini, dur=6)          # foto de archivo a pantalla completa (Ken Burns), como clip_noir
    R.clip_real(h, "entrevista_1", t, t_ini, recorte=(0, 0, 1, .85), credito="ARCHIVO: Canal X")   # video real con recorte y crédito
    R.credito_fijo(h, "FOTO: Autor / Wikimedia Commons", t, t0)   # línea de crédito fija en pantalla (obligatoria con yt-dlp)

De dónde salen los archivos (todos se piden desde la carpeta del video, que es el directorio de trabajo del render):
  fotos   python nucleo/imagenes_web.py persona "Nombre en Wikipedia" 3 --dir imagenes --descargar   ->  imagenes/<slug>.jpg + creditos.json
  video   python nucleo/videos_stock.py buscar|bajar (Pexels/Pixabay)  y  ytbuscar|ytbajar (yt-dlp)  ->  clips/<nombre>.mp4
Las fichas y fotos buscan en imagenes/, retratos/ y fotos/ (jpg, png, webp). La cara se detecta sola para centrar el encuadre.
"""
import functools
import math
import os

import cv2
import numpy as np

from motor import H, W, clamp01, e_inout, e_out, mat_r, mat_s, mat_t
import noir as N

CARPETAS = ("imagenes", "retratos", "fotos")
EXTS = ("", ".jpg", ".jpeg", ".png", ".webp")
TONO_FOTO = (0.04, 0.62)        # rango de grises de la foto ANTES del acabado: la cara queda ~0,46 (medio de la curva S) y no quema


def ruta_foto(nombre):
    """Ruta de la foto `nombre` (con o sin extensión) en imagenes/, retratos/ o fotos/ del video."""
    if os.path.isabs(nombre) and os.path.isfile(nombre):
        return nombre
    for c in CARPETAS:
        for e in EXTS:
            p = os.path.join(os.getcwd(), c, nombre + e)
            if os.path.isfile(p):
                return p
    raise FileNotFoundError(f"foto real «{nombre}» no está en imagenes/ (python nucleo/imagenes_web.py persona \"<nombre>\" 3 --dir imagenes --descargar)")


@functools.lru_cache(maxsize=4)
def _cargar(ruta):
    """Gris float32 0..1 con niveles automáticos (percentiles 1,5-99,2) y la cara más grande (cx, cy, ancho en px) o None."""
    im = cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_COLOR)
    if im is None:
        raise ValueError(f"no se pudo leer la imagen {ruta}")
    k = 1800.0 / max(im.shape[:2])          # suficiente para 1080p y ligero en memoria (hay ~12 procesos de render)
    if k < 1:
        im = cv2.resize(im, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
    g8 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    g = g8.astype(np.float32) / 255.0
    lo, hi = np.percentile(g, 1.5), np.percentile(g, 99.2)
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    return g, _cara(g8)


def _cara(g8):
    ks = 800.0 / max(g8.shape)
    peq = cv2.equalizeHist(cv2.resize(g8, None, fx=ks, fy=ks, interpolation=cv2.INTER_AREA) if ks < 1 else g8)
    ks = min(ks, 1.0)
    for f, voltear in (("haarcascade_frontalface_default.xml", False), ("haarcascade_profileface.xml", False),
                       ("haarcascade_profileface.xml", True)):
        img = cv2.flip(peq, 1) if voltear else peq
        r = cv2.CascadeClassifier(cv2.data.haarcascades + f).detectMultiScale(img, 1.1, 5, minSize=(max(40, peq.shape[1] // 14),) * 2)
        if len(r):
            x, y, w, hh = max(r, key=lambda q: q[2])
            if voltear:
                x = peq.shape[1] - x - w
            return ((x + w / 2) / ks, (y + hh / 2) / ks, w / ks)
    return None


def cara_de(nombre):
    """(cx, cy, ancho) de la cara detectada en px de la foto, o None (para comprobar un encuadre)."""
    return _cargar(ruta_foto(nombre))[1]


def _recorte(g, cara, aspecto, foco=None, cara_rel=0.40):
    """Recorta g al `aspecto` (ancho/alto) centrado en la cara (o en `foco`=(fx, fy) fracciones); acerca hasta que la cara mida ~cara_rel."""
    hh, ww = g.shape
    cw, ch = (ww, ww / aspecto) if ww / aspecto <= hh else (hh * aspecto, hh)
    if foco is not None:
        fx, fy, fw = foco[0] * ww, foco[1] * hh, (foco[2] * ww if len(foco) > 2 else None)
    elif cara is not None:
        fx, fy, fw = cara[0], cara[1], cara[2]
    else:
        fx, fy, fw = ww / 2, hh * (0.36 if hh > ww else 0.5), None
    if fw:
        cw = min(cw, fw / cara_rel)
        ch = cw / aspecto
    x0 = float(np.clip(fx - 0.5 * cw, 0, ww - cw))
    y0 = float(np.clip(fy - (0.44 if fw else 0.5) * ch, 0, hh - ch))
    return g[int(y0):int(y0 + ch), int(x0):int(x0 + cw)]


def _tinta_g(g, tinta, poster, trama, fase, esc):
    """Como noir.tinta_de_foto pero para un gris de cualquier tamaño (esc = píxeles por unidad del mundo): suavizado que conserva
    bordes, aguada en 5 tonos, contorno de pluma y tramado de plumilla en las sombras."""
    hh, ww = g.shape
    s = cv2.bilateralFilter(g, 7, 0.08, 4)
    if poster > 0:
        n = 5.0
        q = np.floor(s * n) / n
        f = s * n - np.floor(s * n)
        q = q + N.smooth_arr(np.clip((f - 0.75) / 0.25, 0, 1)) / n
        s = s * (1 - poster) + q * poster
    gx = cv2.Sobel(s, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(s, cv2.CV_32F, 0, 1, ksize=3)
    e = np.clip((np.sqrt(gx * gx + gy * gy) - 0.10) * 3.5, 0, 1)
    s = s * (1 - tinta * e)
    if trama > 0:
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        u = (xx + yy + fase * 2.3 * esc) / (6.5 * esc)
        lin = np.clip(1.0 - np.abs((u - np.floor(u)) - 0.5) * 2 / 0.32, 0, 1)
        osc = np.clip((0.42 - s) / 0.3, 0, 1) * np.clip(s / 0.06, 0, 1)
        s = s * (1 - trama * 0.55 * osc * lin)
    return s


# ================================================================ la ficha: foto real pegada con cinta
@functools.lru_cache(maxsize=9)
def _ficha(ruta, ancho, zs, aspecto, foco, fase, con_rotulo, con_leyenda, fijacion, tinta, poster, trama, expo, gamma, local):
    """Sprite uint8 HxWx2 (gris premultiplicado, alfa) de la ficha: foto en tinta + marco de papel + cinta; y su geometría en unidades del mundo."""
    g, cara = _cargar(ruta)
    A = float(ancho)
    ph = A / aspecto
    b = 0.06 * A
    bb = b + (0.21 * A if con_rotulo else 0.0) + (0.085 * A if con_leyenda else 0.0)
    PWt, PHt = A + 2 * b, ph + b + bb
    m = 0.10 * A                                              # margen para la cinta que sobresale del papel
    sw, sh = int(round((PWt + 2 * m) * zs)), int(round((PHt + 2 * m) * zs))
    pw, phh = int(round(A * zs)), int(round(ph * zs))
    # --- la foto, en tinta y aguada
    rec = _recorte(g, cara, aspecto, foco)
    f = cv2.resize(rec, (pw, phh), interpolation=cv2.INTER_AREA if rec.shape[1] > pw else cv2.INTER_CUBIC)
    f = np.clip(f, 0, 1) ** gamma * expo
    if local > 0:                                             # claroscuro: contraste local que levanta los rasgos de la cara
        cl = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(6, 6)).apply((np.clip(f, 0, 1) * 255).astype(np.uint8)).astype(np.float32) / 255.0
        f = f * (1 - local) + cl * local
    f = _tinta_g(f, tinta, poster, trama, fase, zs)
    yy, xx = np.mgrid[0:phh, 0:pw].astype(np.float32)
    vin = 1 - 0.35 * np.clip((((xx / pw - 0.5) * 2) ** 2 + ((yy / phh - 0.5) * 2) ** 2) - 0.35, 0, 1)
    f = TONO_FOTO[0] + (TONO_FOTO[1] - TONO_FOTO[0]) * np.clip(f, 0, 1) * vin
    # --- el papel
    rng = np.random.default_rng(len(ruta) + fase)
    ruido = cv2.resize(rng.standard_normal((sh // 24 + 2, sw // 24 + 2)).astype(np.float32), (sw, sh), interpolation=cv2.INTER_CUBIC)
    lienzo = np.full((sh, sw), 0.86, np.float32) * (1 + 0.035 * ruido)
    px0, py0 = int(round(m * zs)), int(round(m * zs))
    pxw, pyh = int(round(PWt * zs)), int(round(PHt * zs))
    mask = np.zeros((sh, sw), np.uint8)
    esq = np.array([[px0, py0], [px0 + pxw, py0], [px0 + pxw, py0 + pyh], [px0, py0 + pyh]], np.float32)
    esq += rng.uniform(-0.006 * A * zs, 0.006 * A * zs, esq.shape).astype(np.float32)
    cv2.fillConvexPoly(mask, np.round(esq * 16).astype(np.int32), 255, cv2.LINE_AA, 4)
    cols = np.arange(sw, dtype=np.float32)[None, :]
    filas = np.arange(sh, dtype=np.float32)[:, None]
    d = np.minimum(np.minimum(cols - px0, px0 + pxw - cols), np.minimum(filas - py0, py0 + pyh - filas))
    lienzo *= 1 - 0.20 * np.clip(1 - d / (0.05 * A * zs), 0, 1)           # borde gastado
    # ventana de la foto + su línea de tinta
    bx, by = px0 + int(round(b * zs)), py0 + int(round(b * zs))
    lienzo[by:by + phh, bx:bx + pw] = f
    cv2.rectangle(lienzo, (bx - 1, by - 1), (bx + pw, by + phh), 0.05, max(2, int(round(1.6 * zs))), cv2.LINE_AA)
    g8 = np.clip(lienzo, 0, 1)
    # --- cinta / chincheta
    alfa = mask.astype(np.float32) / 255.0
    if fijacion == "cinta":
        ta = np.zeros((sh, sw), np.uint8)
        L, an = 0.36 * A * zs, 0.105 * A * zs
        for cx, cy, ang in ((px0 + 0.03 * pxw, py0 + 0.02 * pyh, -38.0), (px0 + 0.97 * pxw, py0 + 0.02 * pyh, 36.0)):
            pts = cv2.boxPoints(((cx, cy), (L, an), ang))
            cv2.fillConvexPoly(ta, np.round(pts * 16).astype(np.int32), 255, cv2.LINE_AA, 4)
        ta = ta.astype(np.float32) / 255.0
        ta *= 0.55 + 0.20 * np.clip(ruido, -1, 1)
        g8 = g8 * (1 - ta * 0.75) + 0.84 * ta * 0.75
        alfa = np.maximum(alfa, ta * 0.92)
    elif fijacion == "chincheta":
        cx, cy, r = px0 + pxw / 2, py0 + 0.045 * A * zs, 0.030 * A * zs
        for dx, dy, rr, tono, al in ((r * 0.35, r * 0.5, r * 1.05, 0.0, 0.35), (0, 0, r, 0.30, 1.0), (-r * 0.28, -r * 0.30, r * 0.32, 0.92, 0.9)):
            tmp = np.zeros((sh, sw), np.uint8)
            cv2.circle(tmp, (int(round((cx + dx) * 16)), int(round((cy + dy) * 16))), int(round(rr * 16)), 255, -1, cv2.LINE_AA, 4)
            t_ = tmp.astype(np.float32) / 255.0 * al
            g8 = g8 * (1 - t_) + tono * t_
            alfa = np.maximum(alfa, t_)
    pm = g8 * alfa
    spr = np.stack([pm, alfa], axis=-1)
    geo = dict(PWt=PWt, PHt=PHt, A=A, ph=ph, b=b, bb=bb, sw=sw / zs, sh=sh / zs)
    return (np.clip(spr, 0, 1) * 255).astype(np.uint8), geo


def _a_mundo(cx, cy, ang, esc, lx, ly):
    p = mat_t(cx, cy) @ mat_r(ang) @ mat_s(esc) @ np.array([lx, ly, 1.0])
    return float(p[0]), float(p[1])


def _poner_sprite(h, spr, zs, cx, cy, esc, ang, alfa, sombra, desv):
    """Pega el sprite (uint8 HxWx2: gris premultiplicado + alfa) en el lienzo con la cámara actual, con sombra proyectada."""
    hs, ws = spr.shape[:2]
    Mw = h.M @ mat_t(cx, cy) @ mat_r(ang) @ mat_s(esc) @ mat_t(-ws / zs / 2, -hs / zs / 2) @ mat_s(1.0 / zs)
    esq = np.array([[0, 0, 1], [ws, 0, 1], [0, hs, 1], [ws, hs, 1]], float) @ Mw[:2].T
    pad = int(70 * h.zoom * max(1.0, esc))
    x0, y0 = int(max(0, math.floor(esq[:, 0].min()) - pad)), int(max(0, math.floor(esq[:, 1].min()) - pad))
    x1, y1 = int(min(W, math.ceil(esq[:, 0].max()) + pad)), int(min(H, math.ceil(esq[:, 1].max()) + pad))
    if x1 <= x0 or y1 <= y0:
        return
    M2 = Mw[:2].copy()
    M2[0, 2] -= x0
    M2[1, 2] -= y0
    out = cv2.warpAffine(spr, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    pm = out[..., 0].astype(np.float32) / 255.0
    a = out[..., 1].astype(np.float32) / 255.0
    roi = h.img[y0:y1, x0:x1]
    if sombra > 0:                                            # luz arriba-izquierda: la sombra cae abajo-derecha, más lejos mientras la ficha "vuela"
        z = h.zoom * desv
        sh = cv2.GaussianBlur(a, (0, 0), max(1.0, 9.0 * z))
        sh = cv2.warpAffine(sh, np.float32([[1, 0, 11.0 * z], [0, 1, 17.0 * z]]), (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
        roi *= (1 - sombra * alfa * sh)[..., None]
    k = (a * alfa)[..., None]
    roi *= 1 - k
    roi += (pm * alfa)[..., None]
    if h._E is not None:
        h._E[y0:y1, x0:x1] *= 1 - a * alfa


def retrato_noir(h, nombre, x, y, ancho, t, t0, *, rotulo=None, leyenda=None, aspecto=0.78, ang=-3.0, foco=None, fijacion="cinta",
                 entrada="golpe", dur_ent=0.30, sale=None, flota=True, k_luz=0.95, tinta=0.38, poster=0.15, trama=0.30, expo=1.0,
                 gamma=1.0, local=0.55, sombra=0.62, cps=20.0, sem=0):
    """FICHA con la foto REAL de un personaje: la foto (imagenes/<nombre>.jpg) convertida a tinta y aguada, con marco de papel de
    foto, cinta o chincheta, sombra y una levísima deriva (nada queda quieto). Aparece en t0 (entrada = golpe | fundido | desliza) y
    el rótulo se escribe a máquina en el borde inferior (paralelo al papel, vía noir.soporte). (x, y) = centro en el MUNDO, `ancho` =
    ancho de la FOTO en px del mundo (el papel es ~12 % mayor), ang en grados, foco=(fx, fy[, ancho_cara]) fracciones de la foto si la cara
    no se detecta, sale=(t1, dur) para retirarla, k_luz = luz fija del papel (None = recibe la luz de la escena), local = contraste local
    (claroscuro de la cara; 0 = foto tal cual), tinta/poster/trama = cuánto se «dibuja» la foto (bajarlos si la cara pierde parecido).
    Devuelve dict(centro, ang, quad, rotulo=(x, y)) o None antes de t0; úsalo para poner un sello encima (N.sello) o ligar un hilo."""
    if t < t0:
        return None
    ruta = ruta_foto(nombre)
    u = clamp01((t - t0) / max(1e-3, dur_ent))
    esc, alfa, desv, dx = 1.0, 1.0, 1.0, 0.0
    if entrada == "golpe":                                    # cae sobre la mesa: escala 1,28 -> 1 con un rebote mínimo
        esc = 1.0 + 0.28 * (1 - e_out(u)) ** 2 - 0.012 * math.sin(clamp01((u - 0.7) / 0.3) * math.pi)
        alfa = clamp01(u * 5)
        desv = 1.0 + 3.0 * (1 - e_out(u))
    elif entrada == "desliza":
        dx = -ancho * 0.7 * (1 - e_out(u))
        alfa = clamp01(u * 3)
    else:
        alfa = u
    if sale is not None and t > sale[0]:
        v = clamp01((t - sale[0]) / max(1e-3, sale[1]))
        alfa *= 1 - v
        esc *= 1 - 0.04 * v
    if alfa <= 0.001:
        return None
    if flota:
        dx += ancho * 0.006 * math.sin(t * 0.8 + sem)
        dy = ancho * 0.005 * math.sin(t * 0.63 + 1.0 + sem)
        a = math.radians(ang + 0.5 * math.sin(t * 0.5 + sem))
    else:
        dy, a = 0.0, math.radians(ang)
    zs = max(1.0, round(h.zoom * 2) / 2)
    fk = None if foco is None else tuple(foco)
    spr, geo = _ficha(ruta, int(round(ancho)), zs, round(aspecto, 3), fk, h.dib % 3, bool(rotulo), bool(leyenda), fijacion,
                      tinta, poster, trama, expo, gamma, local)
    cx, cy = x + dx, y + dy
    if k_luz is not None:                                     # el papel se lee: luz fija sobre el rectángulo del papel
        Q = [_a_mundo(cx, cy, a, esc, sx * geo["PWt"] / 2, sy * geo["PHt"] / 2) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        h.luz_fija(Q, k_luz)
    _poner_sprite(h, spr, zs, cx, cy, esc, a, alfa, sombra, desv)
    N.soporte(h, cx, cy, geo["PWt"], geo["PHt"], a, esc)
    ax = ay = None
    y_fin = geo["PHt"] / 2 - geo["bb"]                        # borde inferior de la foto; debajo: zona del rótulo, zona de la leyenda, margen
    px = geo["A"] * 0.080
    if rotulo:
        ax, ay = _a_mundo(cx, cy, a, esc, 0.0, y_fin + 0.115 * geo["A"])
        N.texto_maquina(h, rotulo, ax, ay, px * esc, t, t0 + dur_ent * 0.7, cps=cps, tono=0.07, centro=True, encuadrar=False,
                        ancho_max=geo["PWt"] * 0.9 * esc, ang=a)
    if leyenda:
        lx, ly = _a_mundo(cx, cy, a, esc, 0.0, y_fin + (0.21 * geo["A"] if rotulo else 0.0) + 0.045 * geo["A"])
        N.texto_maquina(h, leyenda, lx, ly, px * 0.62 * esc, t, t0 + dur_ent * 0.7 + (len(rotulo or "") / cps) * 0.8, cps=cps * 1.3,
                        tono=0.16, centro=True, encuadrar=False, fuente=N.FUENTE_MAQ_R, ancho_max=geo["PWt"] * 0.9 * esc, ang=a)
    quad = [_a_mundo(cx, cy, a, esc, sx * geo["PWt"] / 2, sy * geo["PHt"] / 2) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return dict(centro=(cx, cy), ang=a, quad=quad, rotulo=(ax, ay))


# ================================================================ foto de archivo a pantalla completa
def _ken_burns(g, h, t, t_ini, dur, z0, z1, c0, c1, rot, voltear, tinta, poster, trama, expo, gamma, fino=0.0):
    u = clamp01((t - t_ini) / max(0.01, dur))
    e = e_inout(u)
    gw, gh = g.shape[1], g.shape[0]
    z = z0 + (z1 - z0) * e
    cx = (c0[0] + (c1[0] - c0[0]) * e) * gw
    cy = (c0[1] + (c1[1] - c0[1]) * e) * gh
    esc = max(W / gw, H / gh) * z
    M = cv2.getRotationMatrix2D((cx, cy), rot, esc)
    M[0, 2] += W / 2 - cx
    M[1, 2] += H / 2 - cy
    if voltear:
        M[0] = -M[0]
        M[0, 2] += W
    g = np.clip(g, 0, 1) ** gamma * expo
    g = cv2.warpAffine(g, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if fino > 0:                                              # foto fija: contraste local + tinta a resolución completa (conserva el parecido)
        cl = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8, 8)).apply((np.clip(g, 0, 1) * 255).astype(np.uint8)).astype(np.float32) / 255.0
        g = _tinta_g(g * (1 - fino) + cl * fino, tinta, poster, trama, h.dib % 3, 1.0)
        g = TONO_FOTO[0] + (TONO_FOTO[1] + 0.12 - TONO_FOTO[0]) * np.clip(g, 0, 1)
    else:
        g = N.tinta_de_foto(g, tinta, poster, trama, h.dib % 3)
    h.img[:] = g[..., None]


def foto_noir(h, nombre, t, t_ini, *, dur=6.0, z0=1.0, z1=1.1, c0=None, c1=None, tinta=0.40, poster=0.15, trama=0.30, expo=1.0, gamma=1.0,
              voltear=False, rot=0.0, local=0.5):
    """Foto real (imagenes/<nombre>) a pantalla completa en tinta y aguada con un Ken Burns (zoom z0->z1, centro c0->c1 en fracciones de la
    foto; si no se dan, se centra en la cara detectada o en el tercio superior). Igual que N.clip_noir pero con una imagen fija: úsalo
    para lugares, documentos y fotos de archivo; para PERSONAS usa retrato_noir (la cara en grande a pantalla completa pierde resolución)."""
    g, cara = _cargar(ruta_foto(nombre))
    if c0 is None:
        c0 = (cara[0] / g.shape[1], cara[1] / g.shape[0]) if cara else (0.5, 0.42 if g.shape[0] > g.shape[1] else 0.5)
    _ken_burns(g, h, t, t_ini, dur, z0, z1, c0, c1 or c0, rot, voltear, tinta, poster, trama, expo, gamma, fino=local)


# ================================================================ video real con recorte y crédito
def clip_real(h, nombre, t, t_ini, *, vel=1.0, inicio=0.0, z0=1.0, z1=1.08, c0=(0.5, 0.5), c1=(0.5, 0.5), dur=6.0, tinta=0.7, poster=0.45,
              trama=0.5, expo=1.0, gamma=1.0, voltear=False, rot=0.0, recorte=None, credito=None, t_cred=0.4, dur_cred=3.2):
    """Como N.clip_noir (clips/<nombre>.mp4 de yt-dlp, Pexels o Pixabay a B/N de tinta, con Ken Burns) más:
    recorte=(x0, y0, x1, y1) en fracciones del cuadro original (quita logos, rótulos de noticiero y barras negras de la fuente) y
    credito="ARCHIVO: Canal" que sale a los t_cred s y se queda dur_cred s (obligatorio con extractos de YouTube)."""
    from docu_fx import Clip
    clip = Clip.abrir(nombre)
    lo, hi = N._niveles(nombre, clip)
    idx = int((inicio + max(0.0, t - t_ini) * vel) * clip.fps)
    f = clip.frame(idx)
    if recorte:
        fh, fw = f.shape[:2]
        f = f[int(recorte[1] * fh):int(recorte[3] * fh), int(recorte[0] * fw):int(recorte[2] * fw)]
    g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    _ken_burns(g, h, t, t_ini, dur, z0, z1, c0, c1, rot, voltear, tinta, poster, trama, expo, gamma)
    if credito:
        credito_fijo(h, credito, t, t_ini + t_cred, dur_cred)


def credito_fijo(h, texto, t, t0, dur=3.2, px=24, esquina="izq"):
    """Línea de crédito fija en pantalla (no se mueve con la cámara), a máquina sobre una franja oscura: «FOTO: Autor / Commons · CC BY»,
    «ARCHIVO: Canal». Se va con un fundido a los `dur` s."""
    if t < t0 or t > t0 + dur:
        return
    a = 1 - clamp01((t - (t0 + dur - 0.4)) / 0.4)
    M0, z0 = h.M, h.zoom
    h.M, h.zoom = np.eye(3), 1.0
    try:
        y0 = H - int(px * 6)                                  # franja oscura que sube desde el borde: el texto queda sobre negro real
        y1 = H
        franja = (np.clip((np.arange(y0, y1, dtype=np.float32) - y0) / (px * 3.0), 0, 1) ** 0.8)[:, None, None]
        h.img[y0:y1] *= 1 - 0.92 * a * franja
        ancho = len(texto) * px * 0.62
        x = 54 if esquina == "izq" else W - 54 - ancho
        h.luz_fija([(x - 14, H - px * 2.4), (x + ancho + 14, H - px * 2.4), (x + ancho + 14, H - px * 0.7), (x - 14, H - px * 0.7)], 1.0, mundo=False)
        N.texto_maquina(h, texto, x, H - px * 2.2, px, t, t0, cps=48, tono=0.97, alfa=a, encuadrar=True, ancho_max=W - 108)
    finally:
        h.M, h.zoom = M0, z0
