# -*- coding: utf-8 -*-
"""Utilidades de coreografía compartidas: claves, rebotes, fotones (estelas ondulantes), humo/niebla, ondas."""
import math

import cv2
import numpy as np

from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
ORO = (255, 214, 66)
CREMA = (255, 246, 214)


def kf(t, claves, ease=None):
    """Interpola claves [(t0, v0), (t1, v1), ...] (v puede ser tupla). ease: función 0..1 -> 0..1 aplicada por tramo."""
    if t <= claves[0][0]:
        return claves[0][1]
    for (ta, va), (tb, vb) in zip(claves, claves[1:]):
        if t <= tb:
            u = (t - ta) / max(1e-9, tb - ta)
            u = ease(u) if ease else u
            if isinstance(va, (tuple, list, np.ndarray)):
                return tuple(a + (b - a) * u for a, b in zip(va, vb))
            return va + (vb - va) * u
    return claves[-1][1]


def bump(t, t0, dur=0.35, amp=0.12):
    """Pulso de escala: 0 antes de t0, sube y vuelve a 0 (rebote)."""
    u = (t - t0) / dur
    if u < 0 or u > 1:
        return 0.0
    return amp * math.sin(u * pi) * (1 - u * 0.4)


def pulso(t, t0, dur=0.3):
    """1 en t0 que decae a 0 en `dur`."""
    u = (t - t0) / dur
    return 0.0 if (u < 0 or u > 1) else (1 - u) ** 2


def balistica(t, t0, t1, p0, p1, alto):
    """Salto parabólico de p0 a p1 entre t0 y t1 (alto en px hacia arriba)."""
    u = prog(t, t0, t1)
    return lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u) - alto * 4 * u * (1 - u)


def estela(img, x, y, ang, largo, amp, lam, fase, col, grosor, cabeza=True):
    """Fotón: onda corta (sinusoide) que sigue la dirección `ang`, con cabeza brillante. img uint8 RGB."""
    n = 16
    s = np.linspace(0, largo, n)
    off = amp * np.sin(s / lam * 2 * pi - fase) * np.minimum(1.0, 0.25 + s / 20.0)
    c, sn = math.cos(ang), math.sin(ang)
    X = x - c * s - sn * off
    Y = y - sn * s + c * off
    pts = np.rint(np.stack([X, Y], 1) * 4).astype(np.int32)
    pl = pts.reshape(-1, 1, 2)
    cv2.polylines(img, [pl], False, (255, 160, 56), max(1, int(round(grosor)) + 4), cv2.LINE_AA, 2)
    cv2.polylines(img, [pl], False, col, max(1, int(round(grosor))), cv2.LINE_AA, 2)
    if cabeza:
        cv2.circle(img, (int(round(x * 4)), int(round(y * 4))), int(round(grosor * 0.95 * 4)), (255, 252, 235), -1, cv2.LINE_AA, 2)


def humo(img, x, y, t, n=7, ancho=60, alto=260, col=(255, 240, 220), a=0.5, vel=60.0, semilla=0):
    import pintura as P
    for i in range(n):
        ph = (t * vel / alto + i / n + semilla * 0.13) % 1.0
        yy = y - ph * alto
        xx = x + math.sin(ph * 5 + i * 1.7 + semilla) * ancho * 0.5
        r = 30 + 56 * ph
        P.mancha_din(img, xx, yy, r, r * 0.8, col, a * (1 - ph) ** 0.8 * min(1, ph * 6), seed=i + semilla, t=t)
