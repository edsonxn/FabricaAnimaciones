# -*- coding: utf-8 -*-
"""Utilidades comunes de las escenas animadas: tiempos de la voz, claves de animación, cámara, texto, agua, lluvia."""
import math

import types

import cv2
import numpy as np

from escena_base import TL, Escena
from motor import (W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, catmull, bezier, h01, ruido1,
                   clamp01)
import plano as P
from mundo import degradado_v, llama, humo

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
BLANCO = (255, 255, 255)
ORO = (255, 206, 72)
ROJO = (226, 70, 70)
TEAL = (70, 200, 200)


def w_(eid, fr, i):
    """Tiempo (s) en que empieza la palabra i de la frase fr de la escena eid."""
    ws = _ESC[eid]["frases"][fr]["words"]
    return ws[min(i, len(ws) - 1)]["s"]


def wf(eid, fr, i):
    """Tiempo (s) en que TERMINA la palabra i."""
    ws = _ESC[eid]["frases"][fr]["words"]
    return ws[min(i, len(ws) - 1)]["e"]


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def T0(eid):
    return _ESC[eid]["t0"]


def T1(eid):
    return _ESC[eid]["t1"]


def K(t, pts, ease=e_inout):
    """Interpolación por claves [(t, v), ...] (v escalar o secuencia)."""
    if t <= pts[0][0]:
        v = pts[0][1]
        return v if np.isscalar(v) else np.array(v, float)
    for (t0, v0), (t1, v1) in zip(pts[:-1], pts[1:]):
        if t <= t1:
            u = ease(prog(t, t0, t1)) if t1 > t0 else 1.0
            if np.isscalar(v0):
                return v0 + (v1 - v0) * u
            return np.array(v0, float) + (np.array(v1, float) - np.array(v0, float)) * u
    v = pts[-1][1]
    return v if np.isscalar(v) else np.array(v, float)


def Klog(t, pts, ease=e_inout):
    """Como K pero para (x, y, z) con el zoom interpolado en escala logarítmica."""
    q = [(tt, (v[0], v[1], math.log(v[2]))) for tt, v in pts]
    r = K(t, q, ease)
    return float(r[0]), float(r[1]), math.exp(float(r[2]))


def cam(lz, cx, cy, z=1.0):
    """Contexto de cámara: el punto (cx, cy) del mundo cae en el centro de la pantalla con zoom z."""
    return lz.grupo(W / 2 - cx * z, H / 2 - cy * z, z)


def vent(t, a, b, fi=0.3, fo=0.3):
    """0..1: sube en [a, a+fi] y baja en [b-fo, b]."""
    return smooth(prog(t, a, a + fi)) * (1 - smooth(prog(t, b - fo, b)))


# ------------------------------------------------------------------ texto
def etq(lz, t, t0, t1, txt, x, y, px=38, col=None):
    a = vent(t, t0, t1)
    if a > 0.01:
        P.pastilla(lz, x, y - 8 * (1 - a), txt, px=px, alfa=a)


def gran(lz, t, t0, t1, txt, x, y, px=96, col=BLANCO):
    a = vent(t, t0, t1, 0.25, 0.4)
    if a > 0.01:
        k = 0.8 + 0.2 * e_back(prog(t, t0, t0 + 0.4))
        P.rotulo(lz, x, y, txt, px=px, k=k, color=col, alfa=a)


def cifra(lz, t, t0, txt, x, y, px=120, col=ORO, t1=None):
    if t < t0 or (t1 is not None and t > t1):
        return
    a = smooth(prog(t, t0, t0 + 0.15)) * (1 - (smooth(prog(t, t1 - 0.3, t1)) if t1 is not None else 0))
    k = 0.6 + 0.4 * e_back(prog(t, t0, t0 + 0.45))
    P.rotulo(lz, x, y, txt, px=px, k=k, color=col, alfa=a)


# ------------------------------------------------------------------ fondos numpy (cacheados)
_BG = {}


def bg_grad(top, bot, mid=None, ym=0.55):
    """Fondo vertical (H, W, 3) float32 en [0, 1]."""
    clave = (top, bot, mid, ym)
    if clave not in _BG:
        ys = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        c0, c1 = np.float32(top) / 255, np.float32(bot) / 255
        if mid is None:
            col = c0 * (1 - ys[..., None]) + c1 * ys[..., None]
        else:
            cm = np.float32(mid) / 255
            u1 = np.clip(ys / ym, 0, 1)[..., None]
            u2 = np.clip((ys - ym) / (1 - ym), 0, 1)[..., None]
            col = np.where(ys[..., None] < ym, c0 * (1 - u1) + cm * u1, cm * (1 - u2) + c1 * u2)
        _BG[clave] = np.repeat(col, W, axis=1).astype(np.float32)
    return _BG[clave]


def bg_plano(c):
    clave = ("p", c)
    if clave not in _BG:
        _BG[clave] = np.broadcast_to(np.float32(c) / 255, (H, W, 3)).copy()
    return _BG[clave]


# ------------------------------------------------------------------ agua
def agua(lz, x0, x1, y0, y1, t, c_top=(40, 96, 170), c_bot=(14, 30, 92), amp=6.0, capas=3, seed=0, luna=None, brillo=0.35):
    """Masa de agua vista de lado: degradado, crestas onduladas, destellos y (opcional) camino de luna en x = luna."""
    degradado_v(lz, x0, x1, y0, y1, c_top, c_bot, y0, y1, paso=12.0)
    n = max(8, int((x1 - x0) / 60))
    xs = np.linspace(x0, x1, n)
    for k in range(capas):
        yb = y0 + (y1 - y0) * (0.05 + 0.25 * k)
        ph = t * (0.9 + 0.3 * k) + k * 2.1 + seed
        top = [(x, yb + amp * (0.6 + 0.5 * k) * math.sin(x * 0.011 + ph) + 0.6 * amp * math.sin(x * 0.027 - ph * 1.3)) for x in xs]
        bot = [(x, yb + 26 + 10 * k) for x in xs[::-1]]
        lz.relleno(np.array(top + bot), P.mezcla(c_top, (255, 255, 255), 0.10 + 0.05 * k), alfa=0.55)
    if luna is not None:
        for i in range(16):
            yy = y0 + 8 + i * (y1 - y0) * 0.055
            ww = 10 + i * 9 * (1 + 0.5 * math.sin(t * 2 + i))
            xx = luna + 12 * math.sin(t * 1.7 + i * 1.3)
            lz.relleno(rect_red(xx - ww, yy, 2 * ww, 3 + i * 0.25, 2), (255, 244, 210), alfa=brillo * (1 - i / 18))


def ondas(lz, x, y, t, t0, dur=1.6, r1=60, col=(255, 255, 255), n=3, alfa=0.7):
    """Ondas concéntricas (elipses aplanadas) en la superficie del agua a partir de t0."""
    for k in range(n):
        u = prog(t - k * 0.25, t0, t0 + dur)
        if 0 < u < 1:
            lz.trazo(elipse(x, y, r1 * u + 6, (r1 * u + 6) * 0.22, 0, 40), col, 3.0, cerrado=True, temblor=0.0, capa=2)


def chapoteo(lz, x, y, t, t0, s=1.0, col=(230, 246, 255)):
    """Salpicadura: gotas en parábola + anillo de ondas desde t0."""
    u = t - t0
    if u < 0 or u > 1.1:
        return
    for i in range(9):
        a = -math.pi / 2 + (i - 4) * 0.28 + 0.2 * (h01(3, i) - 0.5)
        v = 250 * s * (0.7 + 0.5 * h01(4, i))
        px = x + math.cos(a) * v * u * 0.6
        py = y + math.sin(a) * v * u + 520 * s * u * u
        lz.relleno(circulo(px, py, 5.5 * s * (1 - 0.5 * u), 8), col, alfa=1 - u / 1.1)
    ondas(lz, x, y + 6, t, t0, 1.1, 70 * s, col, 2)


# ------------------------------------------------------------------ post-procesos numpy
def post_lluvia(img, t, dens=1.0, ang=0.35, largo=46, alfa=0.42, seed=1):
    n = int(220 * dens)
    ov = np.zeros((H, W), np.float32)
    v = 1500.0
    for i in range(n):
        x0 = h01(seed, i) * (W + 400) - 200
        ciclo = (t * v / (H + 200) + h01(seed, i, 3)) % 1.0
        y0 = ciclo * (H + 200) - 100
        xx = x0 + math.sin(ang) * (ciclo * (H + 200))
        cv2.line(ov, (int(xx), int(y0)), (int(xx + math.sin(ang) * largo), int(y0 + math.cos(ang) * largo)), 1.0, 1, cv2.LINE_AA)
    return img + ov[..., None] * np.float32((0.62, 0.72, 0.9)) * alfa


def post_viñeta(img, fuerza=0.35):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
    return img * (1 - fuerza * np.clip(r - 0.4, 0, 1) ** 1.5)[..., None]


def post_fundido_negro(img, t, t0, t1):
    a = smooth(prog(t, t0, t1))
    return img * (1 - a)


# ------------------------------------------------------------------ tarjetas con imágenes históricas (fuentes reales, una vez cada una)
_SPR = {}


def sprite_img(nombre, ancho=420, aspecto=None, foco=(0.5, 0.5), borde=9, radio=16):
    """Imagen de imagenes/ como sprite RGBA premultiplicado (uint8) con borde blanco y esquinas redondeadas (ancho*2 px de ancho)."""
    import os
    from PIL import Image
    clave = (nombre, ancho, aspecto, foco)
    if clave in _SPR:
        return _SPR[clave]
    ruta = None
    for ext in (".jpg", ".png", ".jpeg"):
        p = os.path.join("imagenes", nombre + ext)
        if os.path.isfile(p):
            ruta = p
            break
    im = Image.open(ruta).convert("RGB")
    w0, h0 = im.size
    if aspecto is not None:
        hh = int(min(h0, w0 * aspecto))
        ww = int(min(w0, hh / aspecto))
        x0 = int(np.clip(foco[0] * w0 - ww / 2, 0, w0 - ww))
        y0 = int(np.clip(foco[1] * h0 - hh / 2, 0, h0 - hh))
        im = im.crop((x0, y0, x0 + ww, y0 + hh))
    Wp = ancho * 2
    Hp = int(Wp * im.size[1] / im.size[0])
    im = np.asarray(im.resize((Wp - 2 * borde * 2, Hp - 2 * borde * 2), Image.LANCZOS))
    out = np.full((Hp, Wp, 3), 255, np.uint8)
    out[borde * 2:Hp - borde * 2, borde * 2:Wp - borde * 2] = im
    m = np.zeros((Hp, Wp), np.uint8)
    cv2.rectangle(m, (radio * 2, 0), (Wp - radio * 2, Hp), 255, -1)
    cv2.rectangle(m, (0, radio * 2), (Wp, Hp - radio * 2), 255, -1)
    for cx, cy in ((radio * 2, radio * 2), (Wp - radio * 2, radio * 2), (radio * 2, Hp - radio * 2), (Wp - radio * 2, Hp - radio * 2)):
        cv2.circle(m, (cx, cy), radio * 2, 255, -1, cv2.LINE_AA)
    a = m.astype(np.float32) / 255.0
    rgba = np.dstack([(out.astype(np.float32) * a[..., None]).astype(np.uint8), m])
    _SPR[clave] = rgba
    return rgba


def tarjeta(lz, nombre, x, y, ancho=420, aspecto=None, rot=0.0, alfa=1.0, foco=(0.5, 0.5), capa=2, pie=None, px_pie=26):
    spr = sprite_img(nombre, ancho, aspecto, foco)
    lz.pegar(spr, x, y, k=ancho / spr.shape[1], rot=rot, alfa=alfa, capa=capa)
    if pie and alfa > 0.02:
        hh = spr.shape[0] * ancho / spr.shape[1]
        P.pastilla(lz, x, y + hh / 2 + 24, pie, px=px_pie, alfa=alfa)


def T(eid, texto, **kw):
    """Instante (s) en que se dice `texto` dentro de la escena `eid` (coincide por prefijo; frase= fija la frase; n= la enésima aparición)."""
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def pk(t, t0, d=0.4):
    """Escala de entrada con rebote (0 antes de t0)."""
    return e_back(prog(t, t0, t0 + d)) if t >= t0 else 0.0
