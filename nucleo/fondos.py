# -*- coding: utf-8 -*-
"""Fondos psicodélicos procedurales. Se calculan a 960x540 y se escalan a 1080p."""
import math
from functools import lru_cache

import cv2
import numpy as np

from motor import W, H, VERTICAL

BW, BH = (540, 960) if VERTICAL else (960, 540)
_yy, _xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
X = (_xx - BW / 2) / (BH / 2)
Y = (_yy - BH / 2) / (BH / 2)
R = np.sqrt(X * X + Y * Y) + 1e-4
A = np.arctan2(Y, X)
TAU = 2 * np.pi

# Paletas cosenoidales (a, b, c, d): color(v) = a + b*cos(2π(c*v + d))
PALETAS = {
    "arcoiris": ((.5, .5, .5), (.5, .5, .5), (1, 1, 1), (0, .33, .67)),
    "fuego":    ((.55, .4, .3), (.45, .4, .35), (1, 1, .5), (0, .12, .2)),
    "acido":    ((.5, .5, .5), (.5, .5, .5), (1, 1, .5), (.8, .9, .3)),
    "chicle":   ((.6, .45, .6), (.4, .4, .4), (1, 1, 1), (.9, .2, .45)),
    "oceano":   ((.3, .5, .6), (.3, .4, .4), (1, 1, 1), (.55, .6, .7)),
    "lima":     ((.5, .6, .4), (.5, .4, .4), (1, 1, 1), (.25, .5, .75)),
    "ocaso":    ((.6, .4, .45), (.4, .35, .35), (1, 1, 1), (0, .08, .6)),
    "cosmos":   ((.25, .2, .4), (.25, .2, .35), (1, 1, 1), (.6, .7, .8)),
    "ocre":     ((.62, .42, .28), (.28, .22, .16), (1, 1, 1), (0, .05, .1)),
    "neon":     ((.5, .3, .6), (.5, .4, .4), (1, 1, 1), (.75, .25, .5)),
}


def paleta(v, nombre):
    a, b, c, d = (np.array(x, np.float32) for x in PALETAS[nombre])
    return a + b * np.cos(TAU * (c * v[..., None] + d))


def color_pal(v, nombre):
    a, b, c, d = (np.array(x, np.float32) for x in PALETAS[nombre])
    return a + b * np.cos(TAU * (c * v + d))


def _aa_rayas(v, suav=0.08):
    """Rayas antialias a partir de la fase v (periodo 1)."""
    s = np.sin(TAU * v)
    return np.clip(0.5 + s / (2 * suav), 0, 1)


def _final(img, oscuro_centro=0.0, vign=0.35):
    if oscuro_centro:
        img = img * (1 - oscuro_centro * np.exp(-R * R * 3))[..., None]
    if vign:
        img = img * (1 - vign * np.clip(R / 2.0, 0, 1) ** 2)[..., None]
    img = cv2.resize(np.clip(img, 0, 1).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    return np.clip(img, 0, 1)


# ---------------------------------------------------------------- patrones
def rayos(t, pal="arcoiris", n=14, vel=0.08, pulso=0.0, cx=0.0, cy=0.0, sat=1.0):
    a = np.arctan2(Y - cy, X - cx)
    r = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2) + 1e-4
    v = a / TAU * n + t * vel * n
    m = _aa_rayas(v, 0.05)[..., None]
    c1 = color_pal(t * 0.04, pal)
    c2 = color_pal(t * 0.04 + 0.5, pal)
    img = c1 * m + c2 * (1 - m)
    img = img * (0.8 + 0.25 * np.exp(-r * 1.2))[..., None] * (1 + 0.12 * pulso)
    img = _desat(img, sat)
    return _final(img, vign=0.45)


def espiral(t, pal="acido", brazos=3, giro=2.2, vel=0.35, pulso=0.0, sat=1.0):
    v = A / TAU * brazos + np.log(R) * giro - t * vel
    m = _aa_rayas(v, 0.07)
    # v salta 'brazos' enteros en el corte de ángulo: v/brazos mantiene la paleta periódica
    u = 0.5 * np.sin(TAU * v / brazos) + 0.25 * np.log(R) + t * 0.06   # continuo en el corte angular
    img = paleta(u, pal) * (0.55 + 0.45 * m[..., None])
    img = img * (1 + 0.15 * pulso)
    img = _desat(img, sat)
    return _final(img, oscuro_centro=0.5, vign=0.4)


def tunel(t, pal="neon", vel=0.9, pulso=0.0, giro=0.15, sat=1.0):
    u = 0.32 / R + t * vel
    v = (A + t * giro) / TAU * 10
    ch = np.sign(np.sin(TAU * u) * np.sin(TAU * v))
    s = 0.5 + 0.5 * np.clip(np.sin(TAU * u) * np.sin(TAU * v) * 6, -1, 1)
    img = paleta(u * 0.25 + t * 0.05, pal) * (0.45 + 0.55 * s[..., None])
    img = img * np.clip(R * 1.4, 0, 1)[..., None] * (1 + 0.15 * pulso)
    img = _desat(img, sat)
    return _final(img, vign=0.3)


def plasma(t, pal="chicle", vel=1.0, pulso=0.0, esc=1.0, sat=1.0):
    tt = t * vel
    x, y = X * esc, Y * esc
    v = (np.sin(x * 3.0 + tt) + np.sin(y * 4.0 - tt * 1.3) + np.sin((x + y) * 2.5 + tt * 0.7)
         + np.sin(np.sqrt((x + 0.5 * np.sin(tt * 0.5)) ** 2 + (y + 0.5 * np.cos(tt * 0.33)) ** 2) * 6 - tt * 2))
    img = paleta(v * 0.22 + t * 0.05, pal) * (1 + 0.12 * pulso)
    img = _desat(img, sat)
    return _final(img, vign=0.35)


def anillos(t, pal="arcoiris", vel=0.6, pulso=0.0, cx=0.0, cy=0.0, sat=1.0):
    r = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    v = r * 3.2 - t * vel - pulso * 0.15
    m = _aa_rayas(v, 0.1)[..., None]
    img = paleta(np.floor(v * 2) * 0.13 + t * 0.03, pal) * (0.75 + 0.25 * m)
    img = _desat(img, sat)
    return _final(img, vign=0.4)


def ondas(t, pal="ocaso", vel=0.5, pulso=0.0, sat=1.0):
    v = Y * 3.0 + 0.55 * np.sin(X * 2.2 + t * 1.1) + 0.2 * np.sin(X * 5.3 - t * 1.7) - t * vel
    m = _aa_rayas(v * 2, 0.12)[..., None]
    img = paleta(np.floor(v * 2) * 0.17, pal) * (0.82 + 0.18 * m) * (1 + 0.1 * pulso)
    img = _desat(img, sat)
    return _final(img, vign=0.35)


def caleido(t, pal="lima", n=8, vel=0.25, pulso=0.0, sat=1.0):
    seg = TAU / n
    a = np.abs(((A + t * vel) % seg) - seg / 2)
    x, y = R * np.cos(a), R * np.sin(a)
    v = (np.sin(x * 5 + t) + np.sin(y * 7 - t * 1.4) + np.sin((x * 3 + y * 4) + t * 0.6)
         + np.sin(R * 5 - t * 1.8))
    img = paleta(v * 0.25 + t * 0.04, pal) * (1 + 0.14 * pulso)
    img = _desat(img, sat)
    return _final(img, oscuro_centro=0.25, vign=0.4)


def puntos(t, pal="chicle", celda=0.09, pulso=0.0, sat=1.0):
    gx = (X + t * 0.05) / celda
    gy = (Y + t * 0.03) / celda
    fx, fy = gx - np.floor(gx) - 0.5, gy - np.floor(gy) - 0.5
    cxv, cyv = (np.floor(gx) + 0.5) * celda, (np.floor(gy) + 0.5) * celda
    v = 0.5 + 0.5 * np.sin(cxv * 3 + t * 1.2) * np.cos(cyv * 3 - t)
    rad = 0.12 + 0.34 * v + 0.05 * pulso
    d = np.sqrt(fx * fx + fy * fy)
    m = np.clip((rad - d) * 22, 0, 1)[..., None]
    c1 = color_pal(t * 0.05, pal)
    c2 = color_pal(t * 0.05 + 0.45, pal)
    img = c1 * m + c2 * (1 - m)
    img = _desat(img, sat)
    return _final(img, vign=0.35)


# textura de roca fija (fbm)
def _fbm_tex(seed=3):
    rng = np.random.default_rng(seed)
    acc = np.zeros((BH, BW), np.float32)
    amp = 1.0
    for oct_ in range(6):
        n = 4 * 2 ** oct_
        g = rng.random((n * 9 // 16 + 2, n + 2)).astype(np.float32)
        acc += amp * cv2.resize(g, (BW, BH), interpolation=cv2.INTER_CUBIC)
        amp *= 0.55
    acc = (acc - acc.min()) / (acc.max() - acc.min())
    return acc


_ROCA = _fbm_tex()
_GRIETAS = np.clip(1 - np.abs(_fbm_tex(9) - 0.5) * 18, 0, 1)


def cueva(t, tinte=0.0, fuego=1.0, pulso=0.0, pal="ocre"):
    base = color_pal(np.float32(0.0), "ocre")
    v = _ROCA
    img = np.array([0.46, 0.30, 0.19], np.float32) * (0.62 + 0.55 * v[..., None])
    # grietas con brillo psicodélico
    g = _GRIETAS[..., None]
    psy = paleta(v * 2 + t * 0.15, "arcoiris")
    img = img * (1 - 0.55 * g) + psy * g * 0.55 * tinte
    # luz de antorcha temblorosa
    fl = 0.86 + 0.1 * math.sin(t * 13.1) * math.sin(t * 7.3 + 1) + 0.05 * math.sin(t * 23.7)
    luz = np.exp(-((X + 0.2) ** 2 * 0.35 + (Y - 0.35) ** 2 * 0.6))[..., None]
    img = img * (0.55 + 0.6 * luz * fl * fuego) * (1 + 0.08 * pulso)
    return _final(img, vign=0.6)


def rejilla(t, pal="neon", vel=0.8, pulso=0.0):
    """Horizonte synthwave: sol a rayas + rejilla en perspectiva (el 'hoy')."""
    img = np.zeros((BH, BW, 3), np.float32)
    hz = 0.12
    cielo = Y < hz
    grad = np.clip((Y + 1) / (1 + hz), 0, 1)[..., None]
    top = np.array([0.08, 0.02, 0.2], np.float32)
    bot = np.array([0.95, 0.25, 0.55], np.float32)
    img[:] = top * (1 - grad) + bot * grad
    # sol
    sr = 0.55
    ds = np.sqrt(X ** 2 + (Y + 0.25) ** 2)
    franjas = (np.sin((Y + t * 0.05) * 60) > np.clip((Y + 0.2) * 3, -1, 1)) | (Y < -0.2)
    sol = (ds < sr) & franjas & cielo
    solc = np.array([1.0, 0.85, 0.3], np.float32) * (1 - 0.5 * np.clip((Y + 0.8) / 1.0, 0, 1))[..., None] \
        + np.array([0.0, -0.3, 0.2], np.float32) * np.clip((Y + 0.8), 0, 1)[..., None]
    img = np.where(sol[..., None], solc, img)
    # suelo
    yy = np.maximum(Y - hz, 1e-3)
    z = 0.5 / yy
    gx = X * z
    gz = z + t * vel * 3
    lx = np.abs(gx - np.round(gx))
    lz = np.abs(gz - np.round(gz))
    ancho = 0.035 * z
    linea = np.clip(1 - np.minimum(lx, lz) / np.maximum(ancho, 1e-3), 0, 1)
    suelo = np.array([0.1, 0.0, 0.18], np.float32) * np.ones_like(img)
    lc = np.array([0.2, 0.95, 1.0], np.float32) * (1 + 0.3 * pulso)
    fade = np.clip(yy * 3, 0, 1)[..., None]
    suelo = suelo + lc * linea[..., None] * fade
    img = np.where(cielo[..., None], img, suelo)
    # resplandor de horizonte
    img += np.array([1.0, 0.3, 0.7], np.float32) * np.exp(-np.abs(Y - hz) * 25)[..., None] * 0.5
    return _final(img, vign=0.3)


def cosmos(t, pal="cosmos", pulso=0.0):
    v = (np.sin(X * 1.7 + t * 0.2) + np.sin(Y * 2.3 - t * 0.15) + np.sin((X - Y) * 1.3 + t * 0.1)
         + 0.6 * _ROCA * 3)
    img = paleta(v * 0.18 + t * 0.01, pal) * 0.8
    st = (_ROCA_ST > 0.9965)
    tw = 0.6 + 0.4 * np.sin(t * 3 + _ROCA * 50)
    img = img + st[..., None] * tw[..., None] * 0.9
    return _final(img, vign=0.5)


_ROCA_ST = np.random.default_rng(5).random((BH, BW)).astype(np.float32)


def liso(t, color=(0.98, 0.93, 0.82), lineas=True):
    """Papel de cuaderno (para momentos de lectura)."""
    img = np.ones((BH, BW, 3), np.float32) * np.array(color, np.float32)
    if lineas:
        l = np.clip(1 - np.abs(((_yy + 0.5) % 27) - 13.5) / 0.9, 0, 1)
        img = img - l[..., None] * np.array([0.25, 0.12, 0.0], np.float32) * 0.35
    img = img * (0.93 + 0.07 * _ROCA[..., None])
    return _final(img, vign=0.25)


def pizarra(t, tono=0, pulso=0.0, pal=None):
    """Pizarra de tiza: verde (tono=0) o gris pizarra (tono=1), con manchas de borrado."""
    base = np.array([0.15, 0.25, 0.2] if tono == 0 else [0.17, 0.19, 0.23], np.float32)
    mancha = cv2.GaussianBlur(_ROCA, (0, 0), 6)
    borrado = np.clip(np.sin(X * 2.1 + Y * 0.7 + 1.3) * 0.5 + np.sin(X * 0.8 - Y * 2.4) * 0.5, 0, 1) * 0.05
    img = base * (0.85 + 0.25 * mancha[..., None]) + borrado[..., None] + 0.03 * pulso
    return _final(img, vign=0.45)


def kraft(t, tono=0, pulso=0.0, pal=None):
    """Papel kraft (tono=0) o cartulina gris-azulada (tono=1) con fibras."""
    base = np.array([0.72, 0.58, 0.42] if tono == 0 else [0.62, 0.66, 0.7], np.float32)
    fib = np.clip(1 - np.abs(_GRIETAS - 0.5) * 2, 0, 1) * 0.06
    img = base * (0.9 + 0.14 * _ROCA[..., None]) - fib[..., None] + 0.02 * pulso
    return _final(img, vign=0.3)


def cartulina(t, pal="arcoiris", pulso=0.0, claro=0):
    """Cartulina de color (fijo por paleta) con fibras de papel; claro=1 la aclara (para la fase B)."""
    c = color_pal(np.float32(0.15), pal)
    c = 0.62 * c + 0.38 * np.array([0.95, 0.93, 0.88], np.float32)
    if claro:
        c = 0.55 * c + 0.45 * np.array([0.97, 0.96, 0.93], np.float32)
    fib = np.clip(1 - np.abs(_GRIETAS - 0.5) * 2, 0, 1) * 0.05
    img = np.ones((BH, BW, 3), np.float32) * c * (0.94 + 0.08 * _ROCA[..., None]) - fib[..., None] + 0.015 * pulso
    return _final(img, vign=0.3)


def plano(t, pal="arcoiris", pulso=0.0):
    """Color plano suave que cambia lento de tono, con degradado radial leve (estilo limpio)."""
    c = color_pal(np.float32(t * 0.02), pal)
    c = 0.55 * c + 0.45 * np.array([0.96, 0.96, 0.97], np.float32)
    img = np.ones((BH, BW, 3), np.float32) * c * (1.02 - 0.08 * R[..., None] / 2) * (1 + 0.03 * pulso)
    return _final(img, vign=0.0)


_EST_RNG = np.random.default_rng(314)
_EST_N = 900
_EST = dict(x=_EST_RNG.random(_EST_N) * W, y=_EST_RNG.random(_EST_N) * H,
            r=0.55 + 1.6 * _EST_RNG.random(_EST_N) ** 5, fase=_EST_RNG.random(_EST_N) * 6.28,
            vel=0.6 + 2.2 * _EST_RNG.random(_EST_N), prof=0.25 + 0.75 * _EST_RNG.random(_EST_N),
            tinte=_EST_RNG.random(_EST_N))
_NEB = cv2.GaussianBlur(np.random.default_rng(21).normal(0, 1, (BH // 8, BW // 8)).astype(np.float32), (0, 0), 3.2)
_NEB = cv2.resize((_NEB - _NEB.min()) / (_NEB.max() - _NEB.min()), (BW * 2, BH * 2), interpolation=cv2.INTER_CUBIC)


def estrellas(img, t, brillo=1.0, dx=0.0, dy=0.0, densidad=1.0):
    """Dibuja estrellas titilantes (a 1080p) sobre img. dx, dy: paralaje en px (las lejanas se mueven menos)."""
    if brillo <= 0.01:
        return img
    n = int(_EST_N * min(1.0, densidad))
    xs = (_EST["x"][:n] + dx * _EST["prof"][:n]) % W
    ys = (_EST["y"][:n] + dy * _EST["prof"][:n]) % H
    tw = 0.55 + 0.45 * np.sin(t * _EST["vel"][:n] + _EST["fase"][:n])
    capa = np.zeros((H, W), np.float32)
    col = np.zeros((H, W, 3), np.float32)
    for x, y, r, a, u in zip(xs, ys, _EST["r"][:n], tw, _EST["tinte"][:n]):
        c = (1.0, 0.93, 0.8) if u < 0.18 else ((0.78, 0.86, 1.0) if u > 0.8 else (1.0, 1.0, 1.0))
        cv2.circle(capa, (int(x * 4), int(y * 4)), max(1, int(r * 4)), float(a), -1, cv2.LINE_AA, 2)
        if r > 1.5:   # las grandes, con cruz de destello
            L = int(r * 4 * 3.2 * a)
            cv2.line(capa, (int(x * 4) - L, int(y * 4)), (int(x * 4) + L, int(y * 4)), float(a) * 0.55, 1, cv2.LINE_AA, 2)
            cv2.line(capa, (int(x * 4), int(y * 4) - L), (int(x * 4), int(y * 4) + L), float(a) * 0.55, 1, cv2.LINE_AA, 2)
        cv2.circle(col, (int(x), int(y)), max(1, int(r + 2)), c, -1)
    capa = capa[..., None] * brillo
    return img * (1 - capa) + col * capa


@lru_cache(maxsize=6)
def _espacio_base(tono, ox):
    arriba = np.array([0.045, 0.06, 0.17] if tono == 0 else [0.05, 0.035, 0.12], np.float32)
    abajo = np.array([0.15, 0.085, 0.29] if tono == 0 else [0.12, 0.05, 0.2], np.float32)
    v = np.clip((Y + 1) / 2, 0, 1)[..., None]
    img = arriba * (1 - v) + abajo * v
    neb = _NEB[:BH, ox:ox + BW]
    img = img + neb[..., None] ** 2.2 * np.array([0.16, 0.07, 0.24], np.float32) * 0.9
    img = img + np.exp(-((X + 0.9) ** 2 + (Y - 0.6) ** 2) * 1.2)[..., None] * np.array([0.03, 0.06, 0.14], np.float32)
    img = _final(img, vign=0.25)
    img.setflags(write=False)
    return img


def espacio(t, tono=0, pulso=0.0, pal=None, brillo_est=1.0, dx=0.0, dy=0.0):
    """Espacio estilo Kurzgesagt: degradado azul noche -> violeta, nebulosa suave y estrellas titilantes.
    tono=1: más violeta/oscuro. La base (sin estrellas) se cachea."""
    img = _espacio_base(int(tono), int((t * 3) % BW))
    return estrellas(img, t, brillo_est, dx, dy)


def degradado(t, arriba=(0.35, 0.62, 0.95), abajo=(0.75, 0.88, 1.0), pulso=0.0, pal=None):
    """Degradado vertical liso (cielos, agua)."""
    v = np.clip((Y + 1) / 2, 0, 1)[..., None]
    img = np.array(arriba, np.float32) * (1 - v) + np.array(abajo, np.float32) * v
    return _final(img, vign=0.0)


def _desat(img, sat):
    if sat >= 0.999:
        return img
    g = img.mean(-1, keepdims=True)
    return g + (img - g) * sat


FONDOS = dict(rayos=rayos, espiral=espiral, tunel=tunel, plasma=plasma, anillos=anillos, ondas=ondas,
              caleido=caleido, puntos=puntos, cueva=cueva, rejilla=rejilla, cosmos=cosmos, liso=liso,
              pizarra=pizarra, kraft=kraft, plano=plano, cartulina=cartulina, espacio=espacio, degradado=degradado)


# ---------------------------------------------------------------- papel (estilo Vox)
@lru_cache(maxsize=2)
def _papel_base():
    """Textura de papel crema a resolución de pantalla: motas suaves + fibras cortas. (H+pad, W+pad) para paralaje."""
    pad = 160
    h, w = H + pad, W + pad
    rng = np.random.default_rng(64)
    lo = cv2.resize(rng.normal(0, 1, (h // 90 + 2, w // 90 + 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    mid = cv2.resize(rng.normal(0, 1, (h // 14 + 2, w // 14 + 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    fib = np.zeros((h, w), np.float32)
    for _ in range(int(h * w / 2600)):
        x, y = rng.random() * w, rng.random() * h
        L, a = 6 + rng.random() * 22, rng.random() * np.pi
        cv2.line(fib, (int(x), int(y)), (int(x + L * np.cos(a)), int(y + L * np.sin(a))),
                 float(rng.random() * 0.8 + 0.2), 1, cv2.LINE_AA)
    fib = cv2.GaussianBlur(fib, (0, 0), 0.6)
    g = 0.014 * lo + 0.012 * mid + 0.05 * fib
    base = np.array([0.925, 0.885, 0.79], np.float32)
    img = base[None, None, :] * (1 + g[..., None]) + (fib[..., None] > 0.5) * 0.012
    img.setflags(write=False)
    return img


def papel(t, tinte=(1.0, 1.0, 1.0), oscuro=0.0, dx=0.0, dy=0.0, pulso=0.0, pal=None):
    """Mesa de papel crema (estilo Vox). tinte multiplica el color; oscuro 0..1 lo apaga; dx, dy: paralaje en px."""
    b = _papel_base()
    ox, oy = int(dx) % 160, int(dy) % 160
    img = b[oy:oy + H, ox:ox + W]
    img = img * np.array(tinte, np.float32) * (1 - 0.86 * oscuro)
    return np.ascontiguousarray(img)


def cielo_fondo(colores, alfa=1.0, papel_img=None):
    """Degradado vertical (arriba, abajo) a pantalla completa; se mezcla con el papel según alfa."""
    a = np.array(colores[0], np.float32) / 255
    b = np.array(colores[1], np.float32) / 255
    v = np.clip(np.linspace(0, 1, H, dtype=np.float32) / 0.72, 0, 1)[:, None, None]
    col = a * (1 - v) + b * v
    img = np.broadcast_to(col, (H, W, 3))
    if papel_img is not None:
        return papel_img * (1 - alfa) + img * alfa
    return np.ascontiguousarray(img)


FONDOS["papel"] = papel
