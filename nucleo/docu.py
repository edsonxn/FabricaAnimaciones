# -*- coding: utf-8 -*-
"""Kit del estilo DOCUMENTAL de misterio (referencia: "Detrás del Enigma"): fotos y escaneos con parallax 2.5D, polaroids y folios
como láminas 3D con sombra, tablero de corcho con hilo rojo, texto serif amarillo/blanco palabra por palabra, rótulos de nombre,
sellos, infografías y acabado de película (viñeta, grano, polvo, gradación teal/naranja).

Todo se dibuja sobre un lienzo `np.float32` (H, W, 3) en RGB 0..1; las láminas usan alfa premultiplicado.
Piezas:
  Sprite(rgb_u8, alfa, sombra)      lámina con sombra; `pegar(lienzo, sprite, M, op)` la dibuja con una matriz 3x3
  poner(w, h, x, y, s, rz, ry, rx)  matriz sprite->mundo con giro 3D (perspectiva)   |  camara(z, cx, cy, rot) mundo->pantalla
  Foto(nombre) + foto_parallax(...)  foto a pantalla completa con cámara y parallax por mapa de profundidad
  polaroid(img) / tablero() / pin() / hilo()   utilería del "tablero de evidencias"
  palabra_img / bloque_texto / dibujar_bloque   texto cinético (cada palabra aparece en su tiempo de voz)
  tag_nombre / numero / estampa / marcador_mano  rótulos, cifras grandes, sellos y marcas de rotulador
  grafica_zipf / linea_tiempo               infografías animadas con datos reales
  acabado(img, t)                           gradación, viñeta, polvo, grano, destello
  Mundo (en escenas.py del video) compone tomas con transiciones (fundido, látigo, negro, corte).
"""
import functools
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from motor import FPS, H, W, clamp01, e_back, e_in, e_inout, e_out, lerp, prog, smooth

cv2.setNumThreads(1)

# ------------------------------------------------------------------ paleta y fuentes
AMARILLO = (0.91, 0.94, 0.16)        # amarillo-limón de los rótulos de la referencia
BLANCO = (0.98, 0.97, 0.94)
ROJO = (0.86, 0.10, 0.10)
NEGRO = (0.05, 0.04, 0.03)
PAPEL = (0.96, 0.94, 0.88)
_FD = os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts")
FUENTES = dict(
    serif=os.path.join(_FD, "Baskervville-Bold.ttf"),
    serif_i=os.path.join(_FD, "Baskervville-BoldItalic.ttf"),
    serif_sb=os.path.join(_FD, "Baskervville-SemiBold.ttf"),
    abril=os.path.join(_FD, "AbrilFatface-Regular.ttf"),
    sans=os.path.join(_FD, "Poppins-SemiBold.ttf"),
    sans_i=os.path.join(_FD, "Poppins-SemiBoldItalic.ttf"),
    sans_b=os.path.join(_FD, "Poppins-Bold.ttf"),
    sans_l=os.path.join(_FD, "Poppins-Medium.ttf"),
    mono=os.path.join(_FD, "IBMPlexMono-Regular.ttf"),
)
FUENTES["serif_cond"] = FUENTES["serif"]          # versión condensada (ancho x0,80) del serif de la referencia
FUENTES["abril_cond"] = FUENTES["abril"]
COND = {"serif_cond": 0.70, "abril_cond": 0.72}
FUENTES_RESPALDO = "C:/Windows/Fonts/georgiab.ttf"


@functools.lru_cache(maxsize=96)
def fuente(nombre, px):
    ruta = FUENTES.get(nombre, nombre)
    try:
        return ImageFont.truetype(ruta, int(px))
    except Exception:
        return ImageFont.truetype(FUENTES_RESPALDO, int(px))


def titulo(s):
    """Cada Palabra En Mayúscula Inicial, como los rótulos de la referencia."""
    peq = {"de", "del", "la", "el", "en", "y", "a", "que", "un", "una", "los", "las", "por", "al", "con", "o", "se"}
    out = []
    for i, w in enumerate(s.split(" ")):
        out.append(w if (w.lower() in peq and 0 < i and False) else (w[:1].upper() + w[1:] if w else w))
    return " ".join(out)


# ------------------------------------------------------------------ mezcla de capas
def _roi(lz, x0, y0, w, h):
    """Recorta (x0, y0, w, h) a la imagen; devuelve (sx0, sy0, dx0, dy0, dx1, dy1) o None."""
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(lz.shape[1], x0 + w), min(lz.shape[0], y0 + h)
    if dx1 <= dx0 or dy1 <= dy0:
        return None
    return dx0 - x0, dy0 - y0, dx0, dy0, dx1, dy1


def mezclar_pm(lz, pm, a, x0, y0, op=1.0, aditivo=False):
    """Mezcla una capa premultiplicada `pm` (h,w,3) con alfa `a` (h,w) en (x0, y0)."""
    r = _roi(lz, x0, y0, pm.shape[1], pm.shape[0])
    if r is None or op <= 0:
        return
    sx, sy, dx0, dy0, dx1, dy1 = r
    h, w = dy1 - dy0, dx1 - dx0
    P = pm[sy:sy + h, sx:sx + w]
    A = a[sy:sy + h, sx:sx + w]
    dst = lz[dy0:dy1, dx0:dx1]
    if aditivo:
        dst += P * op
    else:
        dst *= (1.0 - A * op)[..., None]
        dst += P * op


class Sprite:
    """Lámina con alfa (premultiplicada) y sombra difusa opcional."""

    def __init__(self, rgb, alfa=None, sombra=True, sr=16, off=(10, 16), sop=0.55, max_lado=None):
        if max_lado and max(rgb.shape[:2]) > max_lado:
            k = max_lado / max(rgb.shape[:2])
            rgb = cv2.resize(rgb, (int(rgb.shape[1] * k), int(rgb.shape[0] * k)), interpolation=cv2.INTER_AREA)
            if alfa is not None:
                alfa = cv2.resize(alfa, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_AREA)
        h, w = rgb.shape[:2]
        self.w, self.h = w, h
        a = np.ones((h, w), np.float32) if alfa is None else alfa.astype(np.float32)
        self.a = a
        self.pm = (rgb.astype(np.float32) / 255.0) * a[..., None]
        self.sh = None
        if sombra:
            self.pad = int(sr * 3)
            ap = np.pad(a, self.pad)
            self.sh = cv2.GaussianBlur(ap, (0, 0), sr)
            self.off = off
            self.sop = sop


def _bbox_warp(M, w, h):
    c = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    d = cv2.perspectiveTransform(c, M).reshape(-1, 2)
    return d[:, 0].min(), d[:, 1].min(), d[:, 0].max(), d[:, 1].max()


def _warp_mezclar(lz, pm, a, M, op, color_sombra=None):
    h, w = a.shape
    x0, y0, x1, y1 = _bbox_warp(M, w, h)
    ix0, iy0 = int(math.floor(max(x0, 0))), int(math.floor(max(y0, 0)))
    ix1, iy1 = int(math.ceil(min(x1, lz.shape[1]))), int(math.ceil(min(y1, lz.shape[0])))
    if ix1 <= ix0 or iy1 <= iy0 or (x1 - x0) > 20000:
        return
    T = np.array([[1, 0, -ix0], [0, 1, -iy0], [0, 0, 1]], np.float64)
    Mr = T @ M
    sz = (ix1 - ix0, iy1 - iy0)
    aw = cv2.warpPerspective(a, Mr, sz, flags=cv2.INTER_LINEAR, borderValue=0)
    if color_sombra is not None:
        pw = aw[..., None] * np.float32(color_sombra)
    else:
        pw = cv2.warpPerspective(pm, Mr, sz, flags=cv2.INTER_LINEAR, borderValue=0)
    mezclar_pm(lz, pw, aw, ix0, iy0, op)


def pegar(lz, spr, M, op=1.0):
    """Dibuja el sprite con la matriz 3x3 `M` (píxel del sprite -> píxel de pantalla), con su sombra."""
    if op <= 0.003:
        return
    if spr.sh is not None:
        Msh = np.array([[1, 0, spr.off[0]], [0, 1, spr.off[1]], [0, 0, 1]], np.float64) @ M @ \
            np.array([[1, 0, -spr.pad], [0, 1, -spr.pad], [0, 0, 1]], np.float64)
        _warp_mezclar(lz, None, spr.sh, Msh, op * spr.sop, color_sombra=(0, 0, 0))
    _warp_mezclar(lz, spr.pm, spr.a, M, op)


# ------------------------------------------------------------------ geometría 3D sencilla
def poner(w, h, x, y, s=1.0, rz=0.0, ry=0.0, rx=0.0, f=1600.0):
    """Matriz sprite->mundo: lámina de w×h centrada en (x, y), escala s, giros (grados) z (plano), y (bisagra vertical)
    y x (bisagra horizontal), con perspectiva de distancia focal f."""
    hw, hh = w / 2.0, h / 2.0
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    pts = np.array([[-hw, -hh, 0], [hw, -hh, 0], [hw, hh, 0], [-hw, hh, 0]], np.float64) * s
    a, b, c = map(math.radians, (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    p = pts @ (Rz @ Ry @ Rx).T
    k = f / (f + p[:, 2])
    dst = np.float32([[x + p[i, 0] * k[i], y + p[i, 1] * k[i]] for i in range(4)])
    return cv2.getPerspectiveTransform(src, dst).astype(np.float64)


def camara(z=1.0, cx=W / 2, cy=H / 2, rot=0.0):
    """Matriz mundo->pantalla: el punto (cx, cy) del mundo queda en el centro, con zoom z y giro rot (grados)."""
    a = math.radians(rot)
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]], np.float64)
    S = np.diag([z, z, 1.0])
    T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]], np.float64)
    T2 = np.array([[1, 0, W / 2], [0, 1, H / 2], [0, 0, 1]], np.float64)
    return T2 @ R @ S @ T1


def tf(M, x, y):
    v = M @ np.array([x, y, 1.0])
    return v[0] / v[2], v[1] / v[2]


class Cam:
    """Trayectoria de cámara entre dos poses (z, cx, cy, rot) con easing y una deriva de cámara en mano."""

    def __init__(self, a, b, dur, ease=e_inout, mano=1.0, semilla=0):
        self.a, self.b, self.dur, self.ease, self.mano, self.sem = a, b, max(dur, 1e-3), ease, mano, semilla

    def __call__(self, t):
        u = self.ease(clamp01(t / self.dur))
        z, cx, cy, rot = [lerp(p, q, u) for p, q in zip(self.a, self.b)]
        m = self.mano
        s = self.sem
        cx += m * (5.0 * math.sin(0.9 * t + s) + 2.5 * math.sin(2.3 * t + 2 * s))
        cy += m * (4.0 * math.sin(0.7 * t + 1.7 + s) + 2.0 * math.sin(2.9 * t + s))
        rot += m * 0.12 * math.sin(0.55 * t + s)
        return camara(z, cx, cy, rot)


# ------------------------------------------------------------------ imágenes y profundidad
RAIZ_IMG = os.path.join(os.getcwd(), "imagenes")


@functools.lru_cache(maxsize=10)
def cargar(ruta, lado=None):
    """Imagen RGB uint8; `lado` limita el lado mayor."""
    im = Image.open(ruta).convert("RGB")
    if lado and max(im.size) > lado:
        k = lado / max(im.size)
        im = im.resize((int(im.size[0] * k), int(im.size[1] * k)), Image.LANCZOS)
    return np.asarray(im)


def ruta_img(nombre):
    if os.path.isabs(nombre) and os.path.exists(nombre):
        return nombre
    for base in (RAIZ_IMG, os.path.join(RAIZ_IMG, "folios")):
        for ext in ("", ".jpg", ".png", ".jpeg"):
            p = os.path.join(base, nombre + ext)
            if os.path.isfile(p):
                return p
    raise FileNotFoundError(nombre)


@functools.lru_cache(maxsize=4)
def profundidad(nombre, forma):
    """Mapa de profundidad 0..1 (1 = cerca) precalculado por preparar_profundidad.py, remuestreado a `forma`=(h, w)."""
    p = os.path.join(RAIZ_IMG, "depth", os.path.splitext(os.path.basename(ruta_img(nombre)))[0] + ".png")
    if not os.path.exists(p):
        return None
    d = cv2.imread(p, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    return cv2.resize(d, (forma[1], forma[0]), interpolation=cv2.INTER_LINEAR)


_GRID = {}


def _grid():
    if "g" not in _GRID:
        _GRID["g"] = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return _GRID["g"]


def foto_parallax(lz, nombre, t, dur, z0=1.05, z1=1.18, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(30.0, 0.0), lado=2600,
                  op=1.0, giro=0.0, tono=None, ease=e_inout, z_extra=1.0):
    """Foto a pantalla completa (cover) con cámara (zoom z, centro relativo c) y parallax por profundidad.
    `par` = (px, py) desplazamiento máximo (en píxeles de pantalla) del primer plano respecto del fondo."""
    rgb = cargar(ruta_img(nombre), lado)
    hs, ws = rgb.shape[:2]
    d = profundidad(nombre, (hs, ws)) if (par[0] or par[1]) else None
    u = ease(clamp01(t / max(dur, 1e-3)))
    z = lerp(z0, z1, u) * z_extra
    cx = lerp(c0[0], c1[0], u) * ws
    cy = lerp(c0[1], c1[1], u) * hs
    s0 = max(W / ws, H / hs) * z
    X, Y = _grid()
    sx = cx + (X - W / 2) / s0
    sy = cy + (Y - H / 2) / s0
    if d is not None:
        dd = cv2.remap(d, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        k = (dd - 0.5)
        ph = math.sin(u * math.pi) * 0.5 + 0.5 * (2 * u - 1)          # el parallax va y viene con la cámara
        sx = sx - k * (par[0] * ph) / s0
        sy = sy - k * (par[1] * ph) / s0
    if giro:
        pass
    out = cv2.remap(rgb, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255.0
    if tono is not None:
        out *= np.float32(tono)
    if op >= 0.999:
        lz[:] = out
    else:
        lz *= (1 - op)
        lz += out * op


# ------------------------------------------------------------------ utilería: polaroid, tablero, pin, hilo
def polaroid(rgb, ancho=520, aspecto=0.78, foco=(0.5, 0.5), borde=0.055, pie=0.17, sombra=True, sr=18, leyenda=None):
    """Foto instantánea: recorta `rgb` a `aspecto` (alto/ancho) alrededor de `foco` y añade marco blanco de papel."""
    h, w = rgb.shape[:2]
    if h / w > aspecto:
        nh = int(w * aspecto)
        y0 = int(np.clip(foco[1] * h - nh / 2, 0, h - nh))
        rgb = rgb[y0:y0 + nh]
    else:
        nw = int(h / aspecto)
        x0 = int(np.clip(foco[0] * w - nw / 2, 0, w - nw))
        rgb = rgb[:, x0:x0 + nw]
    bw = int(ancho * (1 - 2 * borde))
    foto = cv2.resize(rgb, (bw, int(bw * aspecto)), interpolation=cv2.INTER_AREA)
    b = int(ancho * borde)
    alto = b + foto.shape[0] + int(ancho * pie)
    lienzo = np.empty((alto, ancho, 3), np.float32)
    lienzo[:] = np.array([247, 245, 238], np.float32)
    rng = np.random.default_rng(3)
    lienzo += rng.normal(0, 1.6, lienzo.shape[:2])[..., None]
    g = np.linspace(0, 1, alto)[:, None, None]
    lienzo *= (0.985 + 0.015 * g)
    f = foto.astype(np.float32)
    # ligera viñeta interior de la foto, como las instantáneas viejas
    yy, xx = np.mgrid[0:f.shape[0], 0:f.shape[1]].astype(np.float32)
    r = ((xx / f.shape[1] - 0.5) ** 2 + (yy / f.shape[0] - 0.5) ** 2) * 1.6
    f *= (1 - 0.28 * r)[..., None]
    lienzo[b:b + f.shape[0], b:b + f.shape[1]] = f
    im8 = np.clip(lienzo, 0, 255).astype(np.uint8)
    if leyenda:
        pil = Image.fromarray(im8)
        d = ImageDraw.Draw(pil)
        fy = int(ancho * pie * 0.52)
        d.text((ancho / 2, b + f.shape[0] + ancho * pie * 0.5), leyenda, font=fuente("C:/Windows/Fonts/segoepr.ttf", fy),
               fill=(40, 34, 30), anchor="mm")
        im8 = np.asarray(pil)
    return Sprite(im8, None, sombra=sombra, sr=sr, off=(12, 18), sop=0.6)


def hoja_papel(rgb, alto=900, sombra=True, sr=20):
    """Folio/escaneo como lámina (bordes con ligera transparencia gradual para que no parezcan recortados a tijera)."""
    h, w = rgb.shape[:2]
    k = alto / h
    rgb = cv2.resize(rgb, (int(w * k), alto), interpolation=cv2.INTER_AREA)
    return Sprite(rgb, None, sombra=sombra, sr=sr, off=(14, 20), sop=0.62)


@functools.lru_cache(maxsize=2)
def tablero(w=3400, h=2000, semilla=5):
    """Corcho oscuro procedural (RGB uint8) con viñeta y manchas; fondo de los 'tableros de evidencias'."""
    rng = np.random.default_rng(semilla)
    base = np.zeros((h, w), np.float32)
    for esc, amp in ((6, 0.5), (18, 0.32), (60, 0.24), (200, 0.2)):
        n = rng.random((h // esc + 2, w // esc + 2)).astype(np.float32)
        base += amp * cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
    base = (base - base.min()) / (base.max() - base.min())
    sp = (rng.random((h, w)) > 0.9975).astype(np.float32)
    sp = cv2.GaussianBlur(sp, (0, 0), 2.2) * 9
    col = np.array([0.36, 0.27, 0.18], np.float32)
    img = (0.34 + 0.6 * base)[..., None] * col[None, None, :] * 1.35
    img -= sp[..., None] * 0.25
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= np.clip(1.05 - 0.55 * r ** 1.8, 0.06, 1)[..., None]
    return np.clip(img * 255, 0, 255).astype(np.uint8)


@functools.lru_cache(maxsize=4)
def _pin_sprite(color):
    d = 46
    im = np.zeros((d, d, 4), np.float32)
    yy, xx = np.mgrid[0:d, 0:d].astype(np.float32)
    r = np.hypot(xx - d / 2, yy - d / 2)
    a = np.clip(d * 0.32 - r + 0.5, 0, 1)
    sh = np.clip(1 - np.hypot((xx - d * 0.42) / 9, (yy - d * 0.38) / 9), 0, 1)
    col = np.array(color, np.float32)[None, None, :] * (0.55 + 0.45 * np.clip(1 - r / (d * 0.32), 0, 1)[..., None])
    col = col + sh[..., None] * 0.55
    rgb = np.clip(col * 255, 0, 255).astype(np.uint8)
    return Sprite(rgb, a, sombra=True, sr=4, off=(5, 7), sop=0.6)


def pin(lz, M, x, y, color=(0.85, 0.12, 0.1), s=1.0, op=1.0):
    """Chincheta en el punto (x, y) del mundo (M = matriz de cámara del mundo)."""
    sp = _pin_sprite(tuple(color))
    px, py = tf(M, x, y)
    z = float(np.sqrt(abs(np.linalg.det(M[:2, :2]))))
    pegar(lz, sp, np.array([[z * s, 0, px - sp.w / 2 * z * s], [0, z * s, py - sp.h / 2 * z * s], [0, 0, 1]], np.float64), op)


def linea_aa(lz, pts, color, grosor=3.0, op=1.0, sombra=True):
    """Polilínea suavizada con sombra (para hilos y marcas). pts en pantalla."""
    pts = np.asarray(pts, np.float32)
    x0, y0 = np.floor(pts.min(0) - grosor * 4 - 20).astype(int)
    x1, y1 = np.ceil(pts.max(0) + grosor * 4 + 20).astype(int)
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    q = np.round((pts - [x0, y0]) * 16).astype(np.int32)
    cv2.polylines(m, [q], False, 255, max(1, int(round(grosor))), cv2.LINE_AA, shift=4)
    a = m.astype(np.float32) / 255.0
    if sombra:
        sh = cv2.GaussianBlur(a, (0, 0), grosor * 1.2)
        M = np.array([[1, 0, 4], [0, 1, 6], [0, 0, 1]], np.float64)
        sh = cv2.warpPerspective(sh, M, (a.shape[1], a.shape[0]))
        mezclar_pm(lz, np.zeros(sh.shape + (3,), np.float32), sh * 0.5, x0, y0, op)
    pm = a[..., None] * np.float32(color)
    mezclar_pm(lz, pm, a, x0, y0, op)


def hilo(lz, M, p, q, u=1.0, color=(0.75, 0.08, 0.08), holgura=0.05, grosor=3.0, op=1.0):
    """Hilo rojo entre dos puntos del mundo, con un poco de caída; `u` (0..1) lo va tendiendo desde p hacia q."""
    (x0, y0), (x1, y1) = tf(M, *p), tf(M, *q)
    n = 24
    ts = np.linspace(0, clamp01(u), max(2, int(n * clamp01(u)) + 2))
    dist = math.hypot(x1 - x0, y1 - y0)
    pts = [(lerp(x0, x1, s), lerp(y0, y1, s) + 4 * holgura * dist * s * (1 - s)) for s in ts]
    linea_aa(lz, pts, color, grosor, op)


# ------------------------------------------------------------------ texto
@functools.lru_cache(maxsize=800)
def palabra_img(txt, fnt, px, color, borde=(0.04, 0.03, 0.02), stroke=0.075, glow=0.55):
    """Palabra con contorno oscuro y resplandor suave -> (pm float32, a float32, margen). Se cachea."""
    f = fuente(fnt, px)
    sw = max(1, int(round(px * stroke)))
    m = int(px * 0.55)
    bb = f.getbbox(txt, stroke_width=sw)
    w, h = bb[2] - bb[0] + 2 * m, bb[3] - bb[1] + 2 * m
    L = Image.new("L", (w, h), 0)
    ImageDraw.Draw(L).text((m - bb[0], m - bb[1]), txt, font=f, fill=255, stroke_width=sw + 2)
    g = np.asarray(L.filter(ImageFilter.GaussianBlur(px * 0.16)), np.float32) / 255.0 * glow
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((m - bb[0], m - bb[1]), txt, font=f, fill=tuple(int(c * 255) for c in color) + (255,),
                            stroke_width=sw, stroke_fill=tuple(int(c * 255) for c in borde) + (255,))
    a_t = np.asarray(im, np.float32) / 255.0
    rgb = a_t[..., :3]
    at = a_t[..., 3]
    a = at + g * (1 - at)
    pm = rgb * at[..., None]                                   # el resplandor es negro (premultiplicado = 0)
    c = COND.get(fnt, 1.0)
    if c != 1.0:                                               # condensado: se estrecha el ancho y se rellena para conservar el margen `m`
        nw = max(1, int(pm.shape[1] * c))
        pm = cv2.resize(pm, (nw, pm.shape[0]), interpolation=cv2.INTER_AREA)
        a = cv2.resize(a, (nw, a.shape[0]), interpolation=cv2.INTER_AREA)
        pad = m - int(m * c)
        pm = np.pad(pm, ((0, 0), (pad, pad), (0, 0)))
        a = np.pad(a, ((0, 0), (pad, pad)))
    return pm, a, m


def _ancho_palabra(txt, fnt, px):
    return fuente(fnt, px).getlength(txt) * COND.get(fnt, 1.0)


def bloque_texto(lineas, cx, cy, fnt="serif", px=64, color=AMARILLO, alinear="centro", interlinea=1.12, espacio=0.26):
    """Distribuye líneas de palabras. `lineas`: lista de listas de (palabra, t_aparicion[, color]). Devuelve lista de
    (palabra, t, color, x, y) con (x, y) = esquina sup-izq del glifo; la altura de línea es px*interlinea."""
    sp = px * espacio
    filas = []
    for ln in lineas:
        ws = [_ancho_palabra(w[0], fnt, px) for w in ln]
        filas.append((ws, sum(ws) + sp * (len(ln) - 1)))
    alto = px * interlinea * len(lineas)
    y = cy - alto / 2
    out = []
    for ln, (ws, total) in zip(lineas, filas):
        if alinear == "centro":
            x = cx - total / 2
        elif alinear == "izq":
            x = cx
        else:
            x = cx - total
        for w, aw in zip(ln, ws):
            out.append((w[0], w[1], w[2] if len(w) > 2 else color, x, y))
            x += aw + sp
        y += px * interlinea
    return out


def dibujar_bloque(lz, pal, t, fnt="serif", px=64, op=1.0, salida=None, deriva=14.0, grosor_borde=0.075, rot=0.0):
    """Dibuja las palabras ya dichas (t >= t_aparicion) con entrada suave (sube + aparece). `salida` = t en que empieza a
    desvanecerse todo el bloque (dura 0.35 s)."""
    o = op
    if salida is not None:
        o *= 1 - smooth(prog(t, salida, salida + 0.35))
    if o <= 0.003:
        return
    for w, ta, col, x, y in pal:
        if t < ta:
            continue
        u = prog(t, ta, ta + 0.22)
        pm, a, m = palabra_img(w, fnt, px, tuple(col), stroke=grosor_borde)
        dy = (1 - e_out(u)) * deriva
        if rot:
            dx0, dy0 = x - W / 2, y - H / 2
            x += -math.sin(math.radians(rot)) * dy0 * 0.0
        mezclar_pm(lz, pm, a, int(x - m), int(y - m + dy), o * smooth(u))


def karaoke(fr, i0, i1, cap=True, sep=0.0):
    """Palabras [i0:i1] de la frase `fr` (dict de timeline con 'words') como [(texto, t_inicio)], con Mayúscula Inicial."""
    ws = fr["words"][i0:i1]
    out = []
    for w in ws:
        s = w["w"].strip(".,;:¿?¡!…\"()")
        out.append((s[:1].upper() + s[1:] if cap else s, w["s"] + sep))
    return out


# ------------------------------------------------------------------ rótulos
@functools.lru_cache(maxsize=32)
def _tag_sprite(txt, px, chico):
    f = fuente("serif_i", px)
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + int(px * 0.9), bb[3] - bb[1] + int(px * 0.7)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(250, 248, 242, 255))
    d.text((int(px * 0.45) - bb[0], int(px * 0.32) - bb[1]), txt, font=f, fill=(12, 10, 8, 255),
           stroke_width=max(1, px // 28), stroke_fill=(12, 10, 8, 255))
    a = np.asarray(im, np.float32)[..., 3] / 255.0
    return Sprite(np.asarray(im)[..., :3].copy(), a, sombra=True, sr=6, off=(4, 6), sop=0.6)


def tag_nombre(lz, txt, x, y, t, t0, px=40, rot=-3.0, salida=None, op=1.0):
    """Rótulo blanco con nombre en cursiva negra (estilo 'PAUL KOSOK' de la referencia), entra deslizándose."""
    if t < t0:
        return
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    u = e_out(prog(t, t0, t0 + 0.35))
    sp = _tag_sprite(txt.upper(), px, False)
    M = poner(sp.w, sp.h, x - (1 - u) * 90, y, 1.0, rot)
    pegar(lz, sp, M, o * smooth(prog(t, t0, t0 + 0.2)))


def numero(lz, txt, cx, cy, px, t, t0, color=BLANCO, fnt="sans", salida=None, op=1.0, pop=True):
    """Cifra/fecha grande con brillo (p. ej. '1912', '240'); entra con rebote."""
    if t < t0:
        return
    pm, a, m = palabra_img(txt, fnt, px, tuple(color), stroke=0.03, glow=0.75)
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    s = e_back(prog(t, t0, t0 + 0.4)) if pop else 1.0
    if s <= 0.01:
        return
    if abs(s - 1) > 0.004:
        pm2 = cv2.resize(pm, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
        a2 = cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
    else:
        pm2, a2 = pm, a
    mezclar_pm(lz, pm2, a2, int(cx - pm2.shape[1] / 2), int(cy - pm2.shape[0] / 2), o * smooth(prog(t, t0, t0 + 0.2)))


@functools.lru_cache(maxsize=16)
def _estampa_sprite(txt, px, color):
    f = fuente("sans_b", px)
    bb = f.getbbox(txt)
    pad = int(px * 0.35)
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    d.text((pad - bb[0], pad - bb[1]), txt, font=f, fill=255)
    d.rectangle([2, 2, w - 3, h - 3], outline=255, width=max(3, px // 9))
    a = np.asarray(im, np.float32) / 255.0
    rng = np.random.default_rng(11)
    ruido = cv2.GaussianBlur(rng.random(a.shape).astype(np.float32), (0, 0), 1.2)
    a *= np.clip((ruido - 0.35) * 5, 0.25, 1)                 # tinta desgastada
    rgb = np.empty(a.shape + (3,), np.uint8)
    rgb[:] = (np.array(color) * 255).astype(np.uint8)
    return Sprite(rgb, a * 0.92, sombra=False)


def estampa(lz, txt, x, y, t, t0, px=64, color=(0.78, 0.08, 0.08), rot=-8.0, op=1.0, salida=None):
    """Sello de tinta que cae con golpe (escala 2.4 -> 1) y queda ligeramente torcido."""
    if t < t0:
        return
    u = prog(t, t0, t0 + 0.16)
    s = lerp(2.4, 1.0, e_out(u)) + 0.04 * math.sin(prog(t, t0 + 0.16, t0 + 0.5) * math.pi) * (1 - prog(t, t0 + .16, t0 + .5))
    o = op * u * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    sp = _estampa_sprite(txt, px, tuple(color))
    pegar(lz, sp, poner(sp.w, sp.h, x, y, s, rot), o)


def marcador_mano(lz, kind, x, y, w, h, u, color=(0.9, 0.12, 0.1), grosor=7.0, op=1.0, semilla=0):
    """Marca de rotulador (círculo / subrayado / tachado) que se dibuja de 0 a u (0..1)."""
    if u <= 0:
        return
    rng = np.random.default_rng(semilla)
    if kind == "circulo":
        n = 60
        ang = np.linspace(-0.3, 2 * math.pi * 1.06, n)
        r = 1 + 0.06 * np.sin(ang * 2.3 + rng.random() * 6) + 0.05 * (ang / (2 * math.pi))
        pts = np.c_[x + w / 2 * r * np.cos(ang), y + h / 2 * r * np.sin(ang)]
    elif kind == "subrayado":
        xs = np.linspace(x - w / 2, x + w / 2, 30)
        pts = np.c_[xs, y + 4 * np.sin(xs * 0.05 + rng.random() * 3) + np.linspace(0, 6, 30)]
    else:  # tachado
        xs = np.linspace(x - w / 2, x + w / 2, 20)
        pts = np.c_[xs, np.linspace(y - h / 2, y + h / 2, 20)]
    k = max(2, int(len(pts) * clamp01(u)))
    linea_aa(lz, pts[:k], color, grosor, op, sombra=False)


# ------------------------------------------------------------------ infografías con datos reales
def _panel(w, h, alfa=0.72):
    im = Image.new("RGBA", (w, h), (8, 8, 10, int(255 * alfa)))
    return im


def grafica_zipf(lz, datos, t, t0, cx, cy, w=1180, h=640, dur=3.4, salida=None, op=1.0):
    """Gráfica log-log rango-frecuencia de las palabras del Voynich frente a un texto español (Don Quijote), con las
    MISMAS 37 945 palabras cada uno. Las curvas se dibujan de izquierda a derecha."""
    if t < t0:
        return
    u = clamp01((t - t0) / dur)
    o = op * smooth(prog(t, t0, t0 + 0.3)) * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    im = _panel(w, h)
    d = ImageDraw.Draw(im)
    mx, my, mb, mt = 96, 64, 84, 70
    px0, py0, px1, py1 = mx, mt, w - my, h - mb
    d.rectangle([px0, py0, px1, py1], outline=(200, 200, 200, 110), width=1)
    n = 1000
    lx = lambda r: px0 + (math.log10(r) / math.log10(n)) * (px1 - px0)
    fmax = max(datos["voynich"][0], datos["quijote"][0]) * 1.4
    ly = lambda f: py1 - (math.log10(max(f, 1)) / math.log10(fmax)) * (py1 - py0)
    for r in (1, 10, 100, 1000):
        x = lx(r)
        d.line([x, py0, x, py1], fill=(160, 160, 160, 60), width=1)
        d.text((x, py1 + 10), str(r), font=fuente("sans_l", 24), fill=(230, 230, 225, 230), anchor="mt")
    for f in (1, 10, 100, 1000):
        y = ly(f)
        d.line([px0, y, px1, y], fill=(160, 160, 160, 60), width=1)
        d.text((px0 - 12, y), str(f), font=fuente("sans_l", 24), fill=(230, 230, 225, 230), anchor="rm")
    d.text((px0 + (px1 - px0) / 2, h - 16), "Rango de la palabra (1 = la más común)", font=fuente("sans_l", 26),
           fill=(235, 235, 230, 255), anchor="mb")
    d.text((px0, 8), "Veces que aparece cada palabra", font=fuente("sans_l", 26), fill=(235, 235, 230, 255), anchor="lt")
    rmax = max(2, int(n * u))
    for clave, col in (("quijote", (120, 190, 255, 255)), ("voynich", (232, 240, 40, 255))):
        f = datos[clave]
        pts = [(lx(r), ly(f[r - 1])) for r in range(1, rmax + 1)]
        d.line(pts, fill=col, width=5, joint="curve")
    d.text((px1 - 8, py0 + 14), "Voynich", font=fuente("serif", 40), fill=(232, 240, 40, 255), anchor="ra")
    d.text((px1 - 8, py0 + 64), "Don Quijote (español)", font=fuente("serif", 40), fill=(120, 190, 255, 255), anchor="ra")
    a = np.asarray(im, np.float32) / 255.0
    pm = a[..., :3] * a[..., 3:4]
    mezclar_pm(lz, pm, a[..., 3], int(cx - w / 2), int(cy - h / 2), o)


def linea_tiempo(lz, t, t0, cx, cy, a_ini, a_fin, r0, r1, w=1500, dur=2.6, marcas=(), salida=None, op=1.0, etiqueta=""):
    """Eje de años [a_ini, a_fin] con una franja resaltada r0-r1 que se abre desde r0; `marcas` = [(año, texto)]."""
    if t < t0:
        return
    o = op * smooth(prog(t, t0, t0 + 0.3)) * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    h = 380
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = lambda yr: 60 + (yr - a_ini) / (a_fin - a_ini) * (w - 120)
    yy = 210
    d.line([60, yy, w - 60, yy], fill=(235, 235, 230, 255), width=5)
    for yr in range(int(math.ceil(a_ini / 10) * 10), int(a_fin) + 1, 10):
        big = yr % 50 == 0
        d.line([x(yr), yy - (18 if big else 9), x(yr), yy + (18 if big else 9)], fill=(235, 235, 230, 255), width=3 if big else 2)
        if big:
            d.text((x(yr), yy + 30), str(yr), font=fuente("sans", 34), fill=(235, 235, 230, 255), anchor="mt")
    u = e_inout(clamp01((t - t0 - 0.3) / dur))
    xa = x(r0)
    xb = lerp(xa, x(r1), u)
    d.rectangle([xa, yy - 34, max(xb, xa + 2), yy + 34], fill=(232, 240, 40, 235))
    for yr, txt in marcas:
        d.line([x(yr), yy - 20, x(yr), yy - 90], fill=(190, 190, 185, 255), width=3)
        d.text((x(yr), yy - 100), txt, font=fuente("sans_l", 30), fill=(215, 215, 210, 255), anchor="mb")
    if u > 0.02:
        d.text((xa, yy + 82), str(r0), font=fuente("serif", 58), fill=(232, 240, 40, 255), anchor="ma")
        if u > 0.98:
            d.text((x(r1), yy + 82), str(r1), font=fuente("serif", 58), fill=(232, 240, 40, 255), anchor="ma")
    if etiqueta:
        d.text((w / 2, 20), etiqueta, font=fuente("sans_l", 34), fill=(235, 235, 230, 255), anchor="mt")
    a = np.asarray(im, np.float32) / 255.0
    mezclar_pm(lz, a[..., :3] * a[..., 3:4], a[..., 3], int(cx - w / 2), int(cy - h / 2), o)


# ------------------------------------------------------------------ acabado de película
_FX = {}


def _vineta(fuerza):
    k = ("v", round(fuerza, 2))
    if k not in _FX:
        X, Y = _grid()
        r = np.sqrt(((X - W / 2) / (W / 2)) ** 2 + ((Y - H / 2) / (H / 2)) ** 2)
        _FX[k] = np.clip(1.0 - fuerza * np.clip(r - 0.25, 0, None) ** 1.7, 0.08, 1.0).astype(np.float32)[..., None]
    return _FX[k]


def _polvo(t, n=70):
    """Partículas de polvo (posición determinista en función de t) -> capa aditiva reducida (H/2, W/2)."""
    if "polvo" not in _FX:
        rng = np.random.default_rng(21)
        _FX["polvo"] = dict(x=rng.random(n), y=rng.random(n), vx=(rng.random(n) - 0.35) * 0.018, vy=(rng.random(n) - 0.7) * 0.02,
                            r=rng.random(n) * 2.4 + 0.8, b=rng.random(n) * 0.6 + 0.3, ph=rng.random(n) * 6.28)
    p = _FX["polvo"]
    capa = np.zeros((H // 2, W // 2), np.float32)
    x = ((p["x"] + p["vx"] * t) % 1.0) * (W // 2)
    y = ((p["y"] + p["vy"] * t) % 1.0) * (H // 2)
    for i in range(n):
        br = p["b"][i] * (0.55 + 0.45 * math.sin(t * 1.3 + p["ph"][i]))
        cv2.circle(capa, (int(x[i]), int(y[i])), int(p["r"][i]), float(br), -1, cv2.LINE_AA)
    return cv2.GaussianBlur(capa, (0, 0), 1.4)


def acabado(img, t, fuerza_vineta=0.62, grano=0.035, polvo=0.22, teal=0.05, calido=0.04, destello=0.0, sat=0.94, tinte=None):
    """Gradación de película: curva S suave, sombras teal / luces cálidas, viñeta fuerte, polvo, grano y parpadeo tenue."""
    img = np.clip(img, 0, 1)
    img = img * img * (3 - 2 * img) * 0.35 + img * 0.65                                    # contraste
    lum = (img * np.array([0.299, 0.587, 0.114], np.float32)).sum(-1, keepdims=True)
    img = lum + (img - lum) * sat
    sombra = np.array([-0.4, 0.15, 0.55], np.float32) * teal
    luz = np.array([0.5, 0.22, -0.4], np.float32) * calido
    img = img + (1 - lum) * sombra * (1 - lum) * 2 + lum * luz * lum * 2
    if tinte is not None:
        img = img * np.float32(tinte)
    img *= _vineta(fuerza_vineta)
    if polvo > 0:
        pv = cv2.resize(_polvo(t), (W, H), interpolation=cv2.INTER_LINEAR)
        img += pv[..., None] * polvo * np.array([1.0, 0.95, 0.85], np.float32)
    if destello > 0:
        X, Y = _grid()
        g = np.clip(1 - np.hypot((X - W * 0.92) / (W * 0.6), (Y - H * 0.05) / (H * 0.7)), 0, 1) ** 2
        img += g[..., None] * destello * np.array([1.0, 0.6, 0.25], np.float32) * (0.75 + 0.25 * math.sin(t * 0.8))
    if grano > 0:
        rng = np.random.default_rng(int(t * FPS) + 7)
        g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
        g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
        img += g[..., None] * grano
    img *= 1.0 + 0.012 * math.sin(t * 47.0) * math.sin(t * 13.0)                          # parpadeo de proyector
    return np.clip(img, 0, 1)


# ------------------------------------------------------------------ transiciones entre tomas
def mezcla_tomas(A, B, p, tipo):
    """Mezcla las imágenes A (sale) y B (entra) con progreso p 0..1."""
    p = float(np.clip(p, 0, 1))
    if tipo == "negro":                       # A -> negro -> B
        if p < 0.5:
            return A * (1 - smooth(p * 2))
        return B * smooth((p - 0.5) * 2)
    if tipo == "latigo":                      # barrido horizontal con desenfoque de movimiento
        s = e_inout(p)
        dx = int(W * 0.55 * s)
        k = int(20 + 90 * math.sin(math.pi * p))
        ker = np.zeros((1, k | 1), np.float32)
        ker[:] = 1.0 / ker.size
        Am = cv2.filter2D(np.roll(A, -dx, 1), -1, ker)
        Bm = cv2.filter2D(np.roll(B, int(W * 0.55 * (1 - s)), 1), -1, ker)
        return Am * (1 - smooth(p)) + Bm * smooth(p)
    if tipo == "desenfoque":                  # fundido con desenfoque de enfoque
        s = math.sin(math.pi * p) * 14
        a = cv2.GaussianBlur(A, (0, 0), max(0.1, s)) if s > 0.5 else A
        b = cv2.GaussianBlur(B, (0, 0), max(0.1, s)) if s > 0.5 else B
        return a * (1 - smooth(p)) + b * smooth(p)
    if tipo == "destello":                    # fundido pasando por un destello cálido (solo local, nunca a pantalla completa fuerte)
        m = A * (1 - smooth(p)) + B * smooth(p)
        return m + 0.10 * math.sin(math.pi * p) * np.array([1.0, 0.85, 0.6], np.float32)
    if tipo == "corte":
        return B if p >= 0.5 else A
    return A * (1 - smooth(p)) + B * smooth(p)   # fundido


# ------------------------------------------------------------------ fondos y paneles varios
@functools.lru_cache(maxsize=8)
def pozo_luz(cx=0.5, cy=0.42, r=0.62, color=(0.30, 0.20, 0.11), base=(0.015, 0.012, 0.010)):
    """Fondo oscuro con un 'pozo' de luz cálida (mesa de investigador en penumbra). Devuelve float32 (H, W, 3)."""
    X, Y = _grid()
    d = np.hypot((X / W - cx) * 1.25, (Y / H - cy)) / r
    g = np.clip(1 - d, 0, 1) ** 1.6
    img = np.array(base, np.float32) + g[..., None] * np.array(color, np.float32)
    rng = np.random.default_rng(4)
    n = cv2.resize(rng.random((H // 8, W // 8)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    return (img * (0.85 + 0.3 * n[..., None])).astype(np.float32)


def panel_analisis(lz, palabras, t, t0, cx, cy, w=980, h=560, dur=6.0, salida=None, op=1.0, titulo_panel="ANÁLISIS AUTOMÁTICO"):
    """Panel tipo terminal: columnas de palabras reales del manuscrito que se desplazan mientras un contador de 'coincidencias' sube.
    `palabras` = lista de palabras (transliteración EVA)."""
    if t < t0:
        return
    o = op * smooth(prog(t, t0, t0 + 0.25)) * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    im = Image.new("RGBA", (w, h), (6, 10, 8, 225))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(232, 240, 40, 160), width=2)
    d.text((22, 16), titulo_panel, font=fuente("mono", 26), fill=(232, 240, 40, 255))
    f = fuente("mono", 30)
    cols, filas = 4, 11
    tt = t - t0
    for c in range(cols):
        off = (tt * (2.6 + 0.9 * c)) % 1.0
        base = int(tt * (2.6 + 0.9 * c)) + c * 97
        for r in range(filas):
            wd = palabras[(base + r * 5 + c * 131) % len(palabras)]
            y = 70 + (r - off) * 40
            if y < 60 or y > h - 30:
                continue
            hit = ((base + r) % 7 == 0)
            col = (232, 240, 40, 255) if hit else (150, 170, 150, 190)
            d.text((28 + c * (w - 56) / cols, y), wd, font=f, fill=col)
    n = int(min(1.0, tt / dur) * 37945)
    d.text((22, h - 46), f"palabras analizadas: {n:,}".replace(",", " "), font=fuente("mono", 26), fill=(230, 235, 225, 255))
    d.text((w - 22, h - 46), "resultado: sin significado", font=fuente("mono", 26), fill=(230, 80, 70, 255) if tt > dur else (90, 100, 90, 255), anchor="ra")
    a = np.asarray(im, np.float32) / 255.0
    mezclar_pm(lz, a[..., :3] * a[..., 3:4], a[..., 3], int(cx - w / 2), int(cy - h / 2), o)


def marca_chartreuse(lz, x, y, r, t, t0, u_max=1.0, op=1.0, salida=None):
    """Círculo amarillo-verde translúcido (marcador de mapa de la referencia) con pulso."""
    if t < t0:
        return
    s = e_back(prog(t, t0, t0 + 0.4))
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    rr = r * s * (1 + 0.04 * math.sin((t - t0) * 4))
    if rr < 2:
        return
    x0, y0 = int(x - rr - 4), int(y - rr - 4)
    n = int(rr * 2 + 8)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    dd = np.hypot(xx - n / 2, yy - n / 2)
    a = np.clip(rr - dd, 0, 1) * 0.62
    pm = a[..., None] * np.array([0.72, 0.92, 0.10], np.float32)
    mezclar_pm(lz, pm, a, x0, y0, o)


@functools.lru_cache(maxsize=8)
def tarjeta_perforada(texto, semilla=0, w=1180, h=500):
    """Tarjeta perforada de 80 columnas (esquina cortada, 12 filas de agujeros rectangulares transparentes) con el texto impreso
    arriba; cada columna se perfora según el carácter (patrón determinista)."""
    im = Image.new("RGB", (w, h), (232, 220, 186))
    al = Image.new("L", (w, h), 255)
    d, da = ImageDraw.Draw(im), ImageDraw.Draw(al)
    da.polygon([(0, 0), (70, 0), (0, 70)], fill=0)                     # esquina cortada
    d.polygon([(0, 0), (70, 0), (0, 70)], fill=(0, 0, 0))
    mx, my = 44, 82
    cw = (w - 2 * mx) / 80.0
    rh = (h - my - 40) / 12.0
    f = fuente("mono", 15)
    d.rectangle([0, 0, w, 6], fill=(205, 60, 50))                      # franja roja superior
    txt = (texto.upper() + " " * 80)[:80]
    rng = np.random.default_rng(semilla)
    for c in range(80):
        ch = txt[c]
        d.text((mx + c * cw + cw / 2, 60), ch, font=f, fill=(60, 40, 30), anchor="mm")
        if ch == " ":
            continue
        h0 = (ord(ch) * 2654435761) % 4096
        for r in range(12):
            if (h0 >> r) & 1 and (r % 3 != 1 or (h0 >> 5) & 1):
                x0, y0 = mx + c * cw + cw * 0.22, my + r * rh + rh * 0.18
                da.rectangle([x0, y0, x0 + cw * 0.56, y0 + rh * 0.64], fill=0)
                d.rectangle([x0, y0, x0 + cw * 0.56, y0 + rh * 0.64], fill=(0, 0, 0))
    a = np.asarray(al, np.float32) / 255.0
    rgb = np.asarray(im).astype(np.float32)
    rgb += rng.normal(0, 2.0, rgb.shape[:2])[..., None]
    return Sprite(np.clip(rgb, 0, 255).astype(np.uint8), a, sombra=True, sr=14, off=(10, 16), sop=0.6)


def linea_punteada(lz, pts, u, dash=18, hueco=13, grosor=3, color=(1.0, 0.98, 0.94), op=1.0, glow=1.0):
    """Trazo punteado luminoso (como el contorno del colibrí en la apertura de la referencia) que avanza de 0 a `u` (0..1)
    a lo largo de la polilínea `pts` (pantalla, puede cerrarse repitiendo el primer punto)."""
    pts = np.asarray(pts, np.float32)
    if len(pts) < 2 or u <= 0 or op <= 0:
        return
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.r_[0.0, np.cumsum(seg)]
    L = float(cum[-1])
    x0, y0 = np.floor(pts.min(0) - 40).astype(int)
    x1, y1 = np.ceil(pts.max(0) + 40).astype(int)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0:
        return

    def punto(s):
        i = int(np.clip(np.searchsorted(cum, s, side="right") - 1, 0, len(seg) - 1))
        f = (s - cum[i]) / max(seg[i], 1e-6)
        return pts[i] + (pts[i + 1] - pts[i]) * f

    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    s, meta = 0.0, L * clamp01(u)
    while s < meta:
        a, b = punto(s), punto(min(s + dash, meta))
        cv2.line(m, (int(round((a[0] - x0) * 16)), int(round((a[1] - y0) * 16))),
                 (int(round((b[0] - x0) * 16)), int(round((b[1] - y0) * 16))), 255, grosor, cv2.LINE_AA, shift=4)
        s += dash + hueco
    a = m.astype(np.float32) / 255.0
    g = cv2.GaussianBlur(a, (0, 0), 7) * glow
    pm = (a + g)[..., None] * np.float32(color)
    mezclar_pm(lz, pm, np.clip(a + g, 0, 1), x0, y0, op, aditivo=True)
