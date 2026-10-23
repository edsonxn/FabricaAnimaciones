# -*- coding: utf-8 -*-
"""Kit de Los Duos (anuncio vertical 1080x1920): la identidad de su póster de Facebook (negro + DORADO, logo en cursiva de
pincel, píldoras de colores por género, luces de escenario) dibujada por código encima de sus VIDEOS REALES.

Sobre el pintor `P` de pix.py:
    texto_oro(p, "1,200", x, y, 300)        texto con degradado metálico dorado, contorno oscuro, sombra y brillo que corre
    emoji(p, "🎹", x, y, 90)                 emoji de color (Segoe UI Emoji)
    clip_lleno / clip_borroso / tarjeta     video real a pantalla completa, de fondo difuso o en tarjeta girada con marco de oro
    escenario(p, t)                         fondo de escenario: degradado, haces de luz, bokeh de colores en 3 planos
    notas / destellos / confeti             utilería ambiente
    pildora(p, ...)                         género musical con icono en anillo de color (como el póster)
    logo(p, cx, cy, k, t, t0)               «Los Duos» en Kaushan Script dorado, subrayado de pincel, notas y lema
    mapa_* / pin                            mapa con relieve REAL (ETOPO1 de nucleo/datos/relieve_mx.npz) en tonos oscuros con
                                            curvas de nivel doradas y ríos calculados del propio relieve
    acabado(img, t, ...)                    bloom cálido + viñeta + grano fino + sacudida en los golpes
"""
import functools
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from pix import (BLANCO, ESC, FIN, H, INI, NEGRO, TL, TOTAL, W, Clip, P, _sprite, clamp, e_back, e_in, e_out, golpe,  # noqa: F401
                 lerp, mix, pop, pr, rnd, smooth, ww)

# ------------------------------------------------------------------ paleta (del póster)
ORO = (1.00, 0.79, 0.30)
ORO_CLARO = (1.00, 0.95, 0.70)
ORO_OSC = (0.58, 0.34, 0.06)
TINTA = (0.030, 0.022, 0.016)
CAFE = (0.13, 0.08, 0.04)
CREMA = (1.00, 0.95, 0.85)
VERDE_WA = (0.15, 0.80, 0.40)
ROJO = (0.96, 0.18, 0.20)
GENEROS = [  # texto, color del anillo, emoji
    ("CUMBIAS", (0.96, 0.27, 0.45), "💃"),
    ("NORTEÑO", (1.00, 0.55, 0.15), "🤠"),
    ("ZAPATEADO", (1.00, 0.84, 0.20), "👢"),
    ("BANDA", (0.28, 0.86, 0.46), "🎺"),
    ("GRUPERA", (0.62, 0.38, 0.98), "🎤"),
    ("BALADAS", (0.96, 0.32, 0.76), "💗"),
    ("MARIACHI", (0.22, 0.80, 0.84), "🎻"),
    ("ROCK", (0.85, 0.87, 0.92), "🎸"),
]
AQUI = os.path.dirname(os.path.abspath(__file__))


def cuadro_clip(nombre, seg):
    """Cuadro del clip (uint8 RGB 1080x1920); `seg` se pliega en ida y vuelta si se pasa del final."""
    c = Clip._abiertos.get(nombre)
    if c is not None:
        dur = c.n / c.fps
        if seg > dur - 0.05:
            seg = (dur - 0.05) - ((seg - dur) % max(dur - 0.1, 0.1))
    return Clip.cuadro(nombre, max(0.0, seg))


# ------------------------------------------------------------------ texto dorado
@functools.lru_cache(maxsize=32)
def _degradado_oro(h):
    v = np.linspace(0, 1, h, dtype=np.float32)
    xs, cs = [0.0, 0.30, 0.52, 0.60, 0.80, 1.0], [ORO_CLARO, ORO, ORO, ORO_OSC, ORO, ORO_CLARO]
    col = np.stack([np.interp(v, xs, [c[i] for c in cs]) for i in range(3)], 1)
    return col[:, None, :].astype(np.float32)


def _colocar(p, sp, x, y, anchor):
    h, w = sp.shape
    c = p._t([(x, y)])[0]
    rx = int(round(c[0] - w * {"l": 0, "m": 0.5, "r": 1.0}[anchor[0]]))
    ry = int(round(c[1] - h * {"t": 0, "m": 0.5, "b": 1.0}[anchor[1]]))
    return rx, ry


def _pegar_mascara(p, m, rx, ry, color, op):
    h, w = m.shape
    x0, y0 = max(p.rec[0], rx), max(p.rec[1], ry)
    x1, y1 = min(p.rec[2], rx + w), min(p.rec[3], ry + h)
    if x1 <= x0 or y1 <= y0:
        return
    col = color[y0 - ry:y1 - ry, x0 - rx:x1 - rx] if isinstance(color, np.ndarray) and color.ndim == 3 else color
    p._blend(np.ascontiguousarray(m[y0 - ry:y1 - ry, x0 - rx:x1 - rx]), x0, y0, col, op)


def texto_oro(p, txt, x, y, px, fnt="anton", op=1.0, anchor="mm", esp=0.0, brillo=None, contorno=0.08, sombra=0.75,
              color=None):
    """Texto con degradado metálico dorado (o `color` plano), contorno oscuro de `contorno`·px, sombra difusa y, si `brillo`
    (0..1) se da, una franja de luz diagonal que cruza el texto."""
    if op <= 0.004 or not txt:
        return
    pxs = max(6, int(round(px * p.s)))
    sp = _sprite(txt, pxs, fnt, esp)
    pad = int(pxs * (contorno + 0.25)) + 6
    m = cv2.copyMakeBorder(sp, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    h, w = m.shape
    rx, ry = _colocar(p, sp, x, y, anchor)
    rx, ry = rx - pad, ry - pad
    if sombra > 0:
        k = (int(pxs * 0.18) | 1)
        s = cv2.GaussianBlur(cv2.dilate(m, np.ones((5, 5), np.uint8)), (k * 2 + 1, k * 2 + 1), 0)
        _pegar_mascara(p, s, rx + int(pxs * 0.03), ry + int(pxs * 0.06), NEGRO, sombra * op)
    if contorno > 0:
        r = max(1, int(pxs * contorno))
        ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
        _pegar_mascara(p, cv2.GaussianBlur(cv2.dilate(m, ker), (3, 3), 0), rx, ry, TINTA, 0.92 * op)
    if color is None:
        g = _degradado_oro(h)
        col = np.broadcast_to(g, (h, w, 3)).copy()
        if brillo is not None and 0 < brillo < 1:
            gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
            d = (gx + gy * 0.45) / (w + h * 0.45) - (brillo * 1.4 - 0.2)
            col += (np.exp(-(d / 0.045) ** 2) * 0.85)[..., None]
        col = np.clip(col, 0, 1.3)
    else:
        col = color
    _pegar_mascara(p, m, rx, ry, col, op)


def texto(p, txt, x, y, px, color=BLANCO, fnt="anton", op=1.0, anchor="mm", esp=0.0, sombra=0.75, contorno=0.06):
    """Texto plano con el mismo contorno y sombra que el dorado (blanco, crema, verde…)."""
    texto_oro(p, txt, x, y, px, fnt, op, anchor, esp, None, contorno, sombra, color=np.float32(color))


def ancho(txt, px, fnt="anton", esp=0.0):
    return _sprite(txt, max(6, int(round(px))), fnt, esp).shape[1] - 8


# ------------------------------------------------------------------ emoji e imágenes con alfa
@functools.lru_cache(maxsize=64)
def _emoji(ch):
    f = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
    a = np.asarray(im)
    ys, xs = np.nonzero(a[..., 3] > 8)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()


def pegar_rgba(p, rgba, cx, cy, alto, op=1.0, ang=0.0):
    """Pega una imagen RGBA uint8 centrada en (cx, cy) con altura `alto` (px de diseño) y giro `ang` (grados)."""
    if op <= 0.004:
        return
    ih, iw = rgba.shape[:2]
    k = alto * p.s / ih
    c = p._t([(cx, cy)])[0]
    rad = max(iw, ih) * k * 0.75 + 4
    bb = p._bb(np.float32([[c[0] - rad, c[1] - rad], [c[0] + rad, c[1] + rad]]), pad=0)
    if bb is None:
        return
    x0, y0, x1, y1 = bb
    M = cv2.getRotationMatrix2D((iw / 2, ih / 2), -ang, k)
    M[0, 2] += c[0] - iw / 2 - x0
    M[1, 2] += c[1] - ih / 2 - y0
    reg = cv2.warpAffine(rgba, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    p._blend(reg[..., 3], x0, y0, reg[..., :3].astype(np.float32) / 255.0, op)


def emoji(p, ch, cx, cy, alto, op=1.0, ang=0.0):
    pegar_rgba(p, _emoji(ch), cx, cy, alto, op, ang)


# ------------------------------------------------------------------ video real
def clip_lleno(p, nombre, seg, z=1.0, dx=0.0, dy=0.0, op=1.0, brillo=1.0):
    """Clip a pantalla completa con zoom `z` alrededor del centro (más dx, dy)."""
    hw, hh = W / 2 * z, H / 2 * z
    p.imagen(cuadro_clip(nombre, seg), W / 2 + dx - hw, H / 2 + dy - hh, W / 2 + dx + hw, H / 2 + dy + hh, op, 0, brillo)


def clip_borroso(p, nombre, seg, brillo=0.45, op=1.0):
    """El mismo clip, difuso y oscuro, como fondo (barato: se difumina a 1/8 de resolución)."""
    f = cuadro_clip(nombre, seg)
    ch = cv2.GaussianBlur(cv2.resize(f, (W // 8, H // 8), interpolation=cv2.INTER_AREA), (0, 0), 3.5)
    p.imagen(cv2.resize(ch, (W // 2, H // 2), interpolation=cv2.INTER_LINEAR), 0, 0, W, H, op, 0, brillo)


def _rot(pts, cx, cy, ang):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def tarjeta(p, nombre, seg, cx, cy, w, h, ang=0.0, op=1.0, marco=14, brillo=1.0, enfoque=0.5, enfoque_x=0.5):
    """Video real en una tarjeta girada `ang` grados con marco dorado, sombra y reflejo. `enfoque` = altura (0..1) del clip
    que queda al centro de la tarjeta (los clips son 9:16 y la tarjeta suele ser más ancha)."""
    if op <= 0.004:
        return
    esq = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    m2 = marco
    ext = _rot([(cx - w / 2 - m2, cy - h / 2 - m2), (cx + w / 2 + m2, cy - h / 2 - m2), (cx + w / 2 + m2, cy + h / 2 + m2),
                (cx - w / 2 - m2, cy + h / 2 + m2)], cx, cy, ang)
    # sombra
    sh = [(x + 18, y + 30) for x, y in ext]
    a = p._t(sh)
    bb = p._bb(a, pad=60)
    if bb is not None:
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(m, [np.round((a - (x0, y0)) * 4).astype(np.int32)], 255, cv2.LINE_AA, shift=2)
        m = cv2.GaussianBlur(m, (0, 0), 22 * p.s)
        p._blend(m, x0, y0, NEGRO, 0.65 * op)
    # marco de oro (degradado vertical) + filete claro
    p.poly(ext, None, op, grad=(ORO_CLARO, ORO_OSC))
    p.polilinea(ext, 2.5, ORO_CLARO, 0.9 * op, cerrado=True)
    # imagen girada
    f = cuadro_clip(nombre, seg)
    ih, iw = f.shape[:2]
    k = max(w / iw, h / ih) * p.s
    c = p._t([(cx, cy)])[0]
    a = p._t(_rot(esq, cx, cy, ang))
    bb = p._bb(a, pad=2)
    if bb is None:
        return
    x0, y0, x1, y1 = bb
    oy = (enfoque - 0.5) * max(0.0, ih * k - h * p.s) / k            # desplaza el recorte vertical
    ox = (enfoque_x - 0.5) * max(0.0, iw * k - w * p.s) / k          # y el horizontal
    M = cv2.getRotationMatrix2D((iw / 2 + ox, ih / 2 + oy), -ang, k)
    M[0, 2] += c[0] - (iw / 2 + ox) - x0
    M[1, 2] += c[1] - (ih / 2 + oy) - y0
    reg = cv2.warpAffine(f, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    reg = reg.astype(np.float32) * (brillo / 255.0)
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    cv2.fillPoly(m, [np.round((a - (x0, y0)) * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
    p._blend(m, x0, y0, reg, op)
    # reflejo de vidrio: franja diagonal tenue
    p.poly(_rot([(cx - w / 2, cy - h / 2), (cx - w / 2 + w * 0.32, cy - h / 2), (cx - w / 2, cy - h / 2 + h * 0.42)], cx, cy, ang),
           BLANCO, 0.07 * op, aditivo=True)


# ------------------------------------------------------------------ ambiente
def escenario(p, t, calido=1.0, fuerza=1.0):
    """Fondo de escenario: degradado oscuro, haces de luz que barren, bokeh de colores en 3 planos y polvo dorado."""
    p.fondo((0.020, 0.014, 0.012), (0.075, 0.040, 0.020))
    luces = [(0.18, ORO), (0.50, (0.95, 0.35, 0.55)), (0.82, (0.35, 0.55, 1.0))]
    for i, (xf, col) in enumerate(luces):                     # haces de luz desde arriba
        ang = math.sin(t * (0.45 + 0.13 * i) + i * 2.1) * 0.32
        x0 = W * xf
        L = 2300
        pts = [(x0 - 18, -40), (x0 + 18, -40), (x0 + L * math.sin(ang) + 260, L), (x0 + L * math.sin(ang) - 260, L)]
        p.poly(pts, col, 0.045 * fuerza, aditivo=True)
        p.glow(x0, -10, 260, col, 0.30 * fuerza, 1.6)
    for i in range(34):                                       # bokeh: lejano (chico, lento) a cercano (grande, rápido)
        z = 0.25 + 0.75 * rnd(i, 7)
        x = (rnd(i, 1) * W + math.sin(t * 0.3 + i) * 40 * z + t * 12 * z * (1 if i % 2 else -1)) % (W + 200) - 100
        y = (rnd(i, 2) * H - t * (10 + 30 * z)) % (H + 200) - 100
        col = [ORO, (0.95, 0.35, 0.55), (0.35, 0.55, 1.0), (1.0, 0.55, 0.2)][i % 4]
        tw = 0.6 + 0.4 * math.sin(t * (0.8 + rnd(i, 4) * 2) + i)
        p.circ(x, y, 14 + 70 * z, col, (0.035 + 0.06 * z) * tw * fuerza, aditivo=True)
        p.glow(x, y, 30 + 120 * z, col, 0.05 * z * tw * fuerza, 2.0)
    polvo(p, t, 40, 0.8 * fuerza)


def polvo(p, t, n=40, fuerza=1.0, semilla=11):
    for i in range(n):
        z = 0.3 + 0.7 * rnd(i, semilla)
        x = (rnd(i, semilla + 1) * W + math.sin(t * 0.7 + i * 1.7) * 30) % W
        y = (rnd(i, semilla + 2) * H - t * (20 + 50 * z)) % H
        tw = 0.5 + 0.5 * math.sin(t * (2 + 3 * rnd(i, semilla + 3)) + i)
        p.glow(x, y, 4 + 10 * z, ORO_CLARO, 0.35 * z * tw * fuerza, 1.8)


def velo(p, y0, y1, op=0.75, arriba=False):
    """Degradado negro para que el texto se lea sobre el video (de y0 transparente a y1 opaco)."""
    a, b = (y1, y0) if arriba else (y0, y1)
    ya, yb = int(max(0, min(a, b))), int(min(H, max(a, b)))
    if yb <= ya:
        return
    u = np.linspace(0, 1, yb - ya, dtype=np.float32)
    if arriba:
        u = u[::-1]
    u = (smooth_np(u) * op)[:, None, None]
    p.im[ya:yb] *= 1 - u
    if not arriba:
        p.im[yb:] *= 1 - op
    else:
        p.im[:ya] *= 1 - op


def smooth_np(u):
    return u * u * (3 - 2 * u)


def oscurecer(p, k):
    p.im *= 1 - k


def nota(p, x, y, px, op, ang=0.0, doble=False):
    ch = "♫" if doble else "♪"
    texto_oro(p, ch, x, y, px, "simb", op, contorno=0.04, sombra=0.4)


def notas(p, t, n=9, fuerza=1.0, semilla=3, y_min=0, y_max=H):
    """Notas musicales doradas que suben meciéndose (plano medio)."""
    for i in range(n):
        z = 0.4 + 0.6 * rnd(i, semilla)
        per = 7 + 5 * rnd(i, semilla + 1)
        u = ((t / per) + rnd(i, semilla + 2)) % 1.0
        x = rnd(i, semilla + 3) * (W - 160) + 80 + math.sin(u * 6.3 * 1.5 + i) * 40
        y = y_max + 80 - u * (y_max - y_min + 160)
        op = math.sin(u * math.pi) ** 0.7 * fuerza
        nota(p, x, y, 60 + 70 * z, 0.7 * op, doble=bool(i % 2))


def _estrella(p, x, y, r, op, color=ORO_CLARO, ang=0.0):
    pts = []
    for k in range(8):
        rr = r if k % 2 == 0 else r * 0.22
        a = ang + k * math.pi / 4
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    p.poly(pts, color, op, aditivo=True)
    p.glow(x, y, r * 1.6, ORO, 0.35 * op, 2.0)


def destellos(p, t, t0, cx, cy, n=14, radio=300, dur=1.1, semilla=5):
    """Estallido de estrellitas doradas desde (cx, cy) en t0."""
    u = (t - t0) / dur
    if not 0 <= u <= 1:
        return
    for i in range(n):
        a = rnd(i, semilla) * 6.283
        d = radio * (0.35 + 0.65 * rnd(i, semilla + 1)) * e_out(u)
        r = (16 + 26 * rnd(i, semilla + 2)) * (1 - u) ** 0.6
        _estrella(p, cx + d * math.cos(a), cy + d * math.sin(a) * 0.8, r, (1 - u) ** 1.2, ang=u * 2)


def chispas(p, t, cx, cy, w, h, n=10, semilla=9, fuerza=1.0):
    """Estrellitas que titilan quietas alrededor de un rótulo."""
    for i in range(n):
        x = cx + (rnd(i, semilla) - 0.5) * w
        y = cy + (rnd(i, semilla + 1) - 0.5) * h
        tw = max(0.0, math.sin(t * (2.0 + 2.5 * rnd(i, semilla + 2)) + i * 2.3)) ** 3
        _estrella(p, x, y, 10 + 16 * rnd(i, semilla + 3), tw * fuerza, ang=t * 0.8 + i)


def confeti(p, t, t0, n=70, dur=3.2, semilla=21, fuerza=1.0):
    u = t - t0
    if not 0 <= u <= dur:
        return
    cols = [ORO, ORO_CLARO, (0.96, 0.27, 0.45), (0.28, 0.86, 0.46), (0.35, 0.55, 1.0), (0.62, 0.38, 0.98)]
    for i in range(n):
        x0 = rnd(i, semilla) * W
        vy = 380 + 420 * rnd(i, semilla + 1)
        y = -60 + vy * u - 260 * (1 - rnd(i, semilla + 2)) * max(0.0, 0.5 - u) * 2
        x = x0 + math.sin(u * (2 + 3 * rnd(i, semilla + 3)) + i) * 60
        a = u * (4 + 6 * rnd(i, semilla + 4)) + i
        sz = 12 + 12 * rnd(i, semilla + 5)
        fl = abs(math.cos(a * 1.3))
        pts = _rot([(x - sz, y - sz * 0.45 * fl), (x + sz, y - sz * 0.45 * fl), (x + sz, y + sz * 0.45 * fl),
                    (x - sz, y + sz * 0.45 * fl)], x, y, math.degrees(a))
        op = fuerza * (1 if u < dur - 0.6 else (dur - u) / 0.6)
        p.poly(pts, cols[i % len(cols)], 0.95 * op)


# ------------------------------------------------------------------ piezas de marca
def cinta(p, cx, cy, w, h, op=1.0, k=1.0, color=None, inclina=-3.0):
    """Banda inclinada estilo póster (dorada por defecto) con bordes de pincel."""
    if op <= 0.004:
        return
    w, h = w * k, h * k
    pts = []
    n = 18
    for i in range(n + 1):
        x = cx - w / 2 + w * i / n
        pts.append((x, cy - h / 2 + (rnd(i, 3) - 0.5) * 8))
    for i in range(n, -1, -1):
        x = cx - w / 2 + w * i / n
        pts.append((x, cy + h / 2 + (rnd(i, 4) - 0.5) * 8))
    pts = _rot(pts, cx, cy, inclina)
    p.poly([(x + 10, y + 16) for x, y in pts], NEGRO, 0.45 * op)
    if color is None:
        p.poly(pts, None, op, grad=(ORO_CLARO, ORO_OSC))
    else:
        p.poly(pts, color, op)


def pildora(p, cx, cy, txt, color, ch, k=1.0, op=1.0, w=440, t=0.0):
    """Píldora oscura con anillo de color + emoji a la izquierda y el género en blanco (como el póster)."""
    if op <= 0.004 or k <= 0.01:
        return
    with p.pivote(cx, cy, k):
        h = 118
        x0, x1 = cx - w / 2, cx + w / 2
        p.glow(cx, cy, w * 0.62, color, 0.10 * op)
        p.rrect(x0 + 6, cy - h / 2 + 12, x1 + 6, cy + h / 2 + 12, h / 2, NEGRO, 0.45 * op)
        p.rrect(x0, cy - h / 2, x1, cy + h / 2, h / 2, None, 0.93 * op, grad=((0.10, 0.07, 0.06), (0.03, 0.02, 0.02)))
        p.rrect(x0, cy - h / 2, x1, cy + h / 2, h / 2, None, op, borde=mix(color, BLANCO, 0.15), w=3.5)
        ix = x0 + h / 2
        p.circ(ix, cy, h / 2 - 8, mix(color, NEGRO, 0.55), op)
        p.circ(ix, cy, h / 2 - 8, color, op, w=6)
        emoji(p, ch, ix, cy + 1, 58, op, ang=math.sin(t * 3 + cx) * 6)
        texto(p, txt, ix + h / 2 + 12, cy + 2, 66, BLANCO, "anton", op, "lm", esp=0.02, sombra=0.4, contorno=0.03)


def subrayado(p, x0, x1, y, u, op=1.0, grosor=16):
    """Trazo de pincel dorado que se dibuja de izquierda a derecha (u = 0..1), afilado en las puntas."""
    if u <= 0.01 or op <= 0.004:
        return
    n = 40
    pts_a, pts_b = [], []
    for i in range(int(n * u) + 1):
        s = i / n
        x = x0 + (x1 - x0) * s
        yy = y + math.sin(s * math.pi * 1.1 - 0.4) * -18
        g = grosor * math.sin(math.pi * min(1.0, s * 1.02)) ** 0.6 + 1.5
        pts_a.append((x, yy - g / 2))
        pts_b.append((x, yy + g / 2))
    p.poly(pts_a + pts_b[::-1], None, op, grad=(ORO_CLARO, ORO_OSC))


def logo(p, cx, cy, k, t, t0, op=1.0, lema=True, t_lema=None):
    """«Los Duos» en cursiva de pincel dorada que se revela con un barrido, subrayado, dos notas y el lema."""
    if op <= 0.004 or k <= 0.01:
        return
    u = clamp((t - t0) / 0.55)
    with p.pivote(cx, cy, k):
        p.glow(cx, cy, 520, ORO, 0.12 * op * smooth(u))
        x_cort = cx - 420 + 900 * e_out(u)
        with p.clip(cx - 460, cy - 260, x_cort, cy + 200):
            br = clamp((t - t0 - 0.35) / 0.9)
            texto_oro(p, "Los Duos", cx, cy - 20, 250, "logo", op, brillo=br if br < 1 else None, contorno=0.05)
        subrayado(p, cx - 300, cx + 330, cy + 105, clamp((t - t0 - 0.25) / 0.5), op, 18)
        for j, (dx, dy, px) in enumerate(((345, -150, 90), (415, -95, 70))):
            v = clamp((t - t0 - 0.45 - 0.12 * j) / 0.35)
            if v > 0:
                nota(p, cx + dx, cy + dy + math.sin(t * 2.2 + j) * 8, px * e_back(v), op * v, doble=j == 0)
        if lema:
            tl = t0 + 0.7 if t_lema is None else t_lema
            v = clamp((t - tl) / 0.5)
            texto(p, "MÚSICA QUE ALEGRA TUS MOMENTOS", cx, cy + 165, 36, CREMA, "mont", op * v, esp=0.12, sombra=0.6)


def marca_agua(p, t, op=1.0):
    """Logo chico arriba al centro (desde que el grupo se presenta)."""
    if op <= 0.004:
        return
    texto_oro(p, "Los Duos", W / 2, 118, 92, "logo", op, contorno=0.05, sombra=0.8)


def pin(p, x, y, t, t0, op=1.0, k=1.0, color=ORO):
    """Pin de mapa dorado que cae con rebote, con onda en el suelo."""
    u = clamp((t - t0) / 0.45)
    if u <= 0 or op <= 0.004:
        return
    caida = (1 - e_back(u, 2.4)) * -140
    onda = clamp((t - t0 - 0.3) / 1.2)
    if 0 < onda < 1:
        p.elip(x, y, 30 + 120 * onda, (30 + 120 * onda) * 0.42, color, op * (1 - onda) * 0.8, w=4)
    p.elip(x, y, 26 * k, 10 * k, NEGRO, 0.5 * op * u)
    with p.pivote(x, y, k):
        yy = y + caida
        p.glow(x, yy - 70, 120, color, 0.25 * op)
        pts = [(x, yy)]
        for a in range(-40, 221, 10):
            r = 0.0
            an = math.radians(a + 180)
            pts.append((x + 38 * math.cos(an), yy - 78 + 38 * math.sin(an)))
        p.poly(pts, None, op, grad=(ORO_CLARO, ORO_OSC))
        p.circ(x, yy - 78, 15, TINTA, op)


# ------------------------------------------------------------------ mapa con relieve real
MAPA_LON = (-103.75, -101.75)
MAPA_LAT = (20.85, 22.75)
MAPA_PPG = 900.0           # px por grado de longitud en la imagen base (la latitud se estira por 1/cos)
_KLAT = 1.0 / math.cos(math.radians(21.8))


def geo_px(lon, lat):
    """Lon/lat → px de la imagen base del mapa."""
    return (lon - MAPA_LON[0]) * MAPA_PPG, (MAPA_LAT[1] - lat) * MAPA_PPG * _KLAT


@functools.lru_cache(maxsize=1)
def mapa_base():
    """Imagen float32 del mapa (oscuro cálido + sombreado + curvas de nivel doradas + ríos), cacheada en disco."""
    cache = os.path.join(AQUI, "audio", "_mapa_base.npy")
    if os.path.exists(cache):
        return np.load(cache)
    d = np.load(os.path.join(AQUI, "..", "..", "nucleo", "datos", "relieve_mx.npz"))
    alt, acc = d["alt"].astype(np.float32), d["acc"].astype(np.float32)
    lat0, lon0, paso = float(d["lat0"]), float(d["lon0"]), float(d["paso"])
    i0, i1 = int((MAPA_LAT[0] - lat0) / paso) - 2, int((MAPA_LAT[1] - lat0) / paso) + 3
    j0, j1 = int((MAPA_LON[0] - lon0) / paso) - 2, int((MAPA_LON[1] - lon0) / paso) + 3
    a = alt[i0:i1, j0:j1][::-1]
    ac = acc[i0:i1, j0:j1][::-1]
    Wm = int((MAPA_LON[1] - MAPA_LON[0]) * MAPA_PPG)
    Hm = int((MAPA_LAT[1] - MAPA_LAT[0]) * MAPA_PPG * _KLAT)
    # remuestreo exacto a la ventana
    lat_top = lat0 + (i1 - 1) * paso
    xs = (np.arange(Wm) / MAPA_PPG + MAPA_LON[0] - (lon0 + j0 * paso)) / paso
    ys = (lat_top - (MAPA_LAT[1] - np.arange(Hm) / (MAPA_PPG * _KLAT))) / paso
    mx, my = np.meshgrid(xs.astype(np.float32), ys.astype(np.float32))
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    z = cv2.remap(a, mx, my, cv2.INTER_CUBIC)
    z = cv2.GaussianBlur(z, (0, 0), 4.5)
    ac = cv2.remap(cv2.GaussianBlur(ac, (0, 0), 0.6), mx, my, cv2.INTER_LINEAR)
    # sombreado (luz del noroeste)
    gy, gx = np.gradient(z)
    esc = 0.26
    nx, ny = -gx * esc, -gy * esc
    nz = np.ones_like(z)
    nrm = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    lx, ly, lz = -0.6, -0.6, 0.55
    ll = math.sqrt(lx * lx + ly * ly + lz * lz)
    som = np.clip((nx * lx + ny * ly + nz * lz) / (nrm * ll), 0, 1)
    # color por altitud: valles cálidos oscuros → sierras café claro
    u = np.clip((z - 1400) / 1500, 0, 1)[..., None]
    base = np.float32((0.15, 0.095, 0.055)) * (1 - u) + np.float32((0.44, 0.31, 0.18)) * u
    img = base * (0.22 + 1.15 * som[..., None] ** 1.3)
    # curvas de nivel cada 150 m (doradas, más marcadas cada 600 m)
    for paso_m, op, w in ((150, 0.16, 1.2), (600, 0.42, 2.2)):
        f = (z / paso_m) % 1.0
        g = np.sqrt(gx ** 2 + gy ** 2) / paso_m + 1e-4
        line = np.clip(1 - np.minimum(f, 1 - f) / (g * w), 0, 1)
        img += line[..., None] * np.float32(ORO) * op
    # ríos del propio relieve (acumulación de flujo)
    rio = np.clip((np.log1p(ac) - 6.2) / 2.0, 0, 1)
    rio = cv2.GaussianBlur(rio, (0, 0), 1.2)
    img = img * (1 - rio[..., None] * 0.7) + rio[..., None] * np.float32((0.30, 0.62, 0.78)) * 0.7
    img = np.clip(img, 0, 1).astype(np.float32)
    np.save(cache, img)
    return img


def mapa(p, lon, lat, z, op=1.0):
    """Pinta el mapa con la cámara centrada en (lon, lat) y zoom `z` (1 = MAPA_PPG px por grado)."""
    img = mapa_base()
    cx, cy = geo_px(lon, lat)
    M = np.float32([[z, 0, W / 2 - cx * z], [0, z, H / 2 - cy * z]])
    reg = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if op >= 0.999:
        p.im[:] = reg
    else:
        p.im[:] = p.im * (1 - op) + reg * op


def geo_pant(lon, lat, cam):
    clon, clat, z = cam
    x, y = geo_px(lon, lat)
    cx, cy = geo_px(clon, clat)
    return W / 2 + (x - cx) * z, H / 2 + (y - cy) * z


# ------------------------------------------------------------------ acabado
@functools.lru_cache(maxsize=1)
def _vineta():
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    d = np.sqrt(((gx - W / 2) / (W * 0.75)) ** 2 + ((gy - H / 2) / (H * 0.62)) ** 2)
    v = 1 - 0.50 * np.clip(d - 0.38, 0, 1) ** 1.5
    return np.dstack([v, v * 0.985, v * 0.96]).astype(np.float32)


@functools.lru_cache(maxsize=1)
def _grano():
    rng = np.random.default_rng(7)
    g = rng.normal(0, 1, (H // 2 + 64, W // 2 + 64)).astype(np.float32)
    return cv2.GaussianBlur(g, (0, 0), 0.6)


def acabado(im, t, flash=0.0, sacudida=0.0, bloom=1.0, grano=0.022):
    ch = cv2.resize(im, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    luz = np.clip(ch - 0.55, 0, None)
    b = cv2.GaussianBlur(luz, (0, 0), 6) * 0.55 + cv2.GaussianBlur(luz, (0, 0), 22) * 0.6
    b *= np.float32((1.0, 0.86, 0.62))
    im = im + cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR) * bloom
    if sacudida > 0.01:
        k = int(t * 30)
        dx, dy = (rnd(k, 1) - 0.5) * 40 * sacudida, (rnd(k, 2) - 0.5) * 40 * sacudida
        s = 1 + 0.035 * sacudida
        M = np.float32([[s, 0, dx - W * (s - 1) / 2], [0, s, dy - H * (s - 1) / 2]])
        im = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    im = im * _vineta()
    if grano > 0:
        g = _grano()
        k = int(t * 24)
        ox, oy = int(rnd(k, 3) * 60), int(rnd(k, 4) * 60)
        gg = cv2.resize(g[oy:oy + H // 2, ox:ox + W // 2], (W, H), interpolation=cv2.INTER_LINEAR)
        im = im + (gg * grano)[..., None]
    if flash > 0.003:
        im = im + flash * np.float32((1.0, 0.95, 0.85))
    return np.clip(im, 0, 1).astype(np.float32)


# ------------------------------------------------------------------ ecualizador al ritmo de la música real
EQ_BANDAS = 20


@functools.lru_cache(maxsize=1)
def _eq():
    """Energía por banda (EQ_BANDAS bandas logarítmicas, 0..1) de audio/musica.wav a 30 cuadros por segundo, cacheada."""
    ruta = os.path.join(AQUI, "audio", "musica.wav")
    cache = os.path.join(AQUI, "audio", "_eq.npy")
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(ruta):
        return np.load(cache)
    import soundfile as sf
    x, sr = sf.read(ruta, dtype="float32", always_2d=True)
    x = x.mean(1)
    hop, win = sr // 30, 4096
    xs = np.pad(x, (win // 2, win))
    n = len(x) // hop + 1
    f = np.fft.rfftfreq(win, 1 / sr)
    bordes = np.geomspace(60, 9000, EQ_BANDAS + 1)
    idx = [np.where((f >= a) & (f < b))[0] for a, b in zip(bordes, bordes[1:])]
    ven = np.hanning(win).astype(np.float32)
    out = np.zeros((n, EQ_BANDAS), np.float32)
    for i in range(n):
        s = np.abs(np.fft.rfft(xs[i * hop:i * hop + win] * ven))
        out[i] = [20 * np.log10(s[j].mean() + 1e-6) if len(j) else -120 for j in idx]
    out = np.clip((out - np.percentile(out, 30, axis=0)) / 28.0, 0, 1)
    for i in range(1, n):                                      # caída suave, como un vúmetro
        out[i] = np.maximum(out[i], out[i - 1] * 0.82)
    np.save(cache, out)
    return out


def ecualizador(p, cx, cy, w, h, t, op=1.0, crece=1.0):
    """Barras doradas que bailan con la música real (con reflejo tenue debajo)."""
    if op <= 0.004:
        return
    e = _eq()
    v = e[min(len(e) - 1, max(0, int(t * 30)))]
    paso = w / EQ_BANDAS
    for i, a in enumerate(v):
        x = cx - w / 2 + paso * (i + 0.5)
        bh = max(8.0, h * (0.12 + 0.88 * float(a)) * crece)
        bw = paso * 0.62
        p.rrect(x - bw / 2, cy - bh, x + bw / 2, cy, bw / 2.5, None, op, grad=(ORO_CLARO, ORO_OSC))
        p.rrect(x - bw / 2, cy + 6, x + bw / 2, cy + 6 + bh * 0.35, bw / 2.5, ORO, 0.16 * op)
    p.glow(cx, cy - h * 0.3, w * 0.55, ORO, 0.10 * op)
