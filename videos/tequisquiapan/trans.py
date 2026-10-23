# -*- coding: utf-8 -*-
"""Cambios de escena PROCEDURALES (sin cortes): barridos de pintura que tapan el mapa y lo destapan.

Cada transición es un campo de distancia con signo de pantalla (negativo = cubierto) que se pinta con el mismo pincel de guache
que el mapa (`M.pintar`). Debajo, el mundo sigue siendo continuo: la cámara vuela y el estado cambia mientras está tapado.
Fase «in» (p 0→1): la pintura cubre todo. Fase «out» (p 0→1): se descubre la escena nueva.
"""
import math

import numpy as np

import mapa as M
from motor import H, W, e_in, e_inout, e_out, lerp, prog

Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
DIAG = math.hypot(W, H)


def _ruido1(v, seed, n=4):
    """Ruido suave 1D (suma de senos con fases de la semilla), valores ~[-1, 1]."""
    r = np.random.default_rng(seed)
    out = np.zeros_like(v, dtype=np.float32)
    for k in range(n):
        out += np.sin(v * (0.011 * (k + 1) * (1.0 + 0.3 * r.random())) + r.uniform(0, 6.28)) / (k + 1) ** 0.7
    return out / 1.6


# ------------------------------------------------------------------ campos por tipo: devuelven S (negativo = pintura)
def _tinta(fase, p, a, b, seed):
    """Mancha de tinta: círculo irregular que crece desde `a` (cubre) y se abre como agujero en `b` (descubre)."""
    c = a if fase == "in" else b
    dx, dy = X - c[0], Y - c[1]
    d = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    wob = (np.sin(5 * th + seed) * 0.55 + np.sin(9 * th + 2.3 * seed) * 0.3 + np.sin(14 * th + 1.7 * seed) * 0.15)
    R = DIAG * e_inout(p) * 1.02
    S = d - (R + 38 * wob * np.sin(math.pi * min(1.0, p * 1.02)) ** 0.5)
    return S if fase == "in" else -S


def _pincel(fase, p, a, b, seed):
    """Pinceladas anchas en diagonal que barren la pantalla."""
    ang = math.radians(-18 + 8 * math.sin(seed))
    s = X * math.cos(ang) + Y * math.sin(ang)
    t = -X * math.sin(ang) + Y * math.cos(ang)
    fila = np.floor(t / 96.0)
    off = (np.sin(fila * 12.9898 + seed) * 43758.5453) % 1.0 * 340.0
    borde = 54 * np.sin(t / 37.0 + seed) + 34 * np.sin(t / 91.0 + 2 * seed)
    L = float(s.max() - s.min()) + 700
    f = s.min() - 420 + L * e_inout(p)
    if fase == "in":
        return s - (f - off + borde)
    return -(s - (f - off + borde))


def _papel(fase, p, a, b, seed):
    """Papel que se rasga: frente vertical con borde desgarrado."""
    x0 = -80 + (W + 160) * e_inout(p)
    rasgo = 46 * _ruido1(Y, seed, 5) + 10 * np.sin(Y / 9.0 + seed)
    S = X - (x0 + rasgo)
    return S if fase == "in" else -S


def _portal(fase, p, a, b, seed):
    """Iris: el círculo de imagen se cierra sobre `a` y se abre en `b`."""
    c = a if fase == "in" else b
    d = np.hypot(X - c[0], Y - c[1])
    r = DIAG * (1 - e_inout(p)) if fase == "in" else DIAG * e_inout(p)
    return r - d          # negativo fuera del círculo (cubierto)


def _puntos(fase, p, a, b, seed):
    """Media tinta: puntos que crecen hasta juntarse (y se encogen al destapar)."""
    esp = 58.0
    cx = (X % esp) - esp / 2
    cy = (Y % esp) - esp / 2
    d = np.hypot(cx, cy)
    retraso = (X / W * 0.55 + Y / H * 0.35)
    u = np.clip(p * 1.9 - retraso, 0, 1)
    Rm = esp * 0.78
    if fase == "in":
        return d - Rm * u
    return d - Rm * (1 - np.clip(p * 1.9 - retraso, 0, 1))


def _rollo(fase, p, a, b, seed):
    """Un rollo de pergamino que baja por la pantalla."""
    y0 = -60 + (H + 140) * e_inout(p)
    onda = 12 * np.sin(X / 70.0 + seed)
    S = Y - (y0 + onda)
    return S if fase == "in" else -S


def _ola(fase, p, a, b, seed):
    """Ola que sube por la pantalla."""
    y0 = H + 120 - (H + 240) * e_inout(p)
    onda = 52 * np.sin(X / 130.0 + seed + p * 5) + 20 * np.sin(X / 47.0 - p * 7)
    S = (y0 + onda) - Y
    return S if fase == "in" else -S


def _persianas(fase, p, a, b, seed):
    """Persianas horizontales que se cierran y se abren."""
    h = 96.0
    ym = (Y % h) - h / 2
    u = e_inout(p) if fase == "in" else 1 - e_inout(p)
    return np.abs(ym) - (h / 2 + 4) * u


TIPOS = dict(tinta=_tinta, pincel=_pincel, papel=_papel, portal=_portal, puntos=_puntos, rollo=_rollo, ola=_ola, persianas=_persianas)
SFX = dict(tinta="splat", pincel="pincel", papel="papel", portal="iris", puntos="persianas", rollo="zoom_whoosh", ola="ola", persianas="persianas")


class Transicion:
    """Barrido entre dos escenas centrado en t_c: cubre en [t_c - dur/2, t_c], descubre en [t_c, t_c + dur/2]."""

    def __init__(self, t_c, tipo, color, a=(W // 2, H // 2), b=(W // 2, H // 2), dur=0.8, seed=1, borde=(40, 30, 40)):
        self.t_c, self.tipo, self.color, self.a, self.b, self.dur, self.seed = t_c, tipo, color, a, b, dur, seed
        self.borde = borde

    def activa(self, t):
        return self.t_c - self.dur / 2 - 0.02 <= t <= self.t_c + self.dur / 2 + 0.02

    def aplicar(self, img, t, fase_boil=0):
        f = TIPOS[self.tipo]
        h = self.dur / 2
        if t <= self.t_c:
            p = prog(t, self.t_c - h, self.t_c)
            if p <= 0.0:
                return
            S = f("in", p, self.a, self.b, self.seed)
        else:
            p = prog(t, self.t_c, self.t_c + h)
            if p >= 1.0:
                return
            S = f("out", p, self.a, self.b, self.seed)
        S = S.astype(np.float32)
        if self.tipo == "portal":                                  # anillo de luz en el borde del iris
            c = self.a if t <= self.t_c else self.b
            d = np.hypot(X - c[0], Y - c[1])
            r = DIAG * (1 - e_inout(p)) if t <= self.t_c else DIAG * e_inout(p)
            anillo = (np.abs(d - r) - 11).astype(np.float32)
            M.pintar(img, S, self.color, 1.0, fase_boil, borde=1.4)
            M.pintar(img, anillo, (250, 214, 110), 1.0, fase_boil, sombra=0.1)
            return
        M.pintar(img, S, self.color, 1.0, fase_boil, borde=1.4)
        if self.tipo == "rollo":                                   # cilindro de madera en el borde del pergamino
            y0 = -60 + (H + 140) * e_inout(prog(t, self.t_c - self.dur / 2, self.t_c)) if t <= self.t_c else -60 + (H + 140) * e_inout(prog(t, self.t_c, self.t_c + self.dur / 2))
            rod = (np.abs(Y - y0) - 20).astype(np.float32)
            M.pintar(img, rod, (170, 116, 80), 1.0, fase_boil, sombra=0.3)
