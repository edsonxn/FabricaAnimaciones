# -*- coding: utf-8 -*-
"""Elementos animados con tinta (se redibujan cada cuadro): murciélagos, aspas, matorral rodante, humo, estrellas, polvo, luces."""
import math

import numpy as np

import toon as TN
from toon import blob, bezier2, elipse_, estrella, suave
from motor import clamp01, e_out, prog, ruido1

NEGRO_NOCHE = (16, 12, 32)


def murcielago(h, x, y, s, t, fase=0.0, dir=1, alfa=1.0, sem=0):
    """Murciélago en silueta con las alas que baten (6 Hz): membrana con festones, orejas y ojito."""
    fl = math.sin(2 * math.pi * 5.8 * t + fase)
    fl2 = math.sin(2 * math.pi * 5.8 * t + fase - 0.7)
    cuerpo = elipse_(0, 2, 12, 20, n=14)
    h.forma(_tr(cuerpo, x, y, s, dir), NEGRO_NOCHE, None, w=0, jit=0.5, alfa=alfa, tex=0)
    cab = elipse_(0, -22, 10, 9, n=12)
    h.forma(_tr(cab, x, y, s, dir), NEGRO_NOCHE, None, w=0, jit=0.4, alfa=alfa, tex=0)
    for sg in (-1, 1):
        oreja = np.array([(sg * 3, -28), (sg * 11, -42), (sg * 12, -26)])
        h.forma(_tr(oreja, x, y, s, dir), NEGRO_NOCHE, None, w=0, jit=0.3, alfa=alfa, tex=0)
        punta = (sg * (88 - 18 * abs(fl)), -60 * fl - 8)
        codo = (sg * 48, -46 * fl - 22)
        borde = bezier2((sg * 6, -12), codo, punta, 10)
        # trailing edge: festones entre la punta y el cuerpo
        f1 = (sg * 66, -22 * fl2 + 14)
        f2 = (sg * 44, -10 * fl2 + 24)
        f3 = (sg * 24, 22)
        P = np.vstack([borde, [f1, (sg * 62, -18 * fl2 + 6), f2, (sg * 40, 14), f3, (sg * 18, 14), (sg * 6, 10)]])
        h.forma(_tr(P, x, y, s, dir), NEGRO_NOCHE, None, w=0, jit=0.5, alfa=alfa, tex=0)


def _tr(P, x, y, s, dir):
    P = np.asarray(P, float)
    return np.stack([x + P[:, 0] * s * dir, y + P[:, 1] * s], 1)


def aspas(h, cx, cy, ang, largo=170, ancho=30, color=(52, 40, 74), sem=0):
    """Molino de viento: 4 aspas con travesaños, giran con `ang`."""
    for k in range(4):
        a = ang + k * math.pi / 2
        c, s_ = math.cos(a), math.sin(a)
        n = np.array([-s_, c])
        d = np.array([c, s_])
        c0 = np.array([cx, cy])
        pts = np.array([c0 + d * 22 + n * 5, c0 + d * largo + n * ancho * 0.5, c0 + d * largo - n * ancho * 0.5, c0 + d * 22 - n * 5])
        h.forma(pts, color, None, w=4.0, sem=sem + k, jit=0.8, tex=0)
        for q in (0.35, 0.58, 0.8):
            a0 = c0 + d * largo * q + n * ancho * 0.45
            a1 = c0 + d * largo * q - n * ancho * 0.45
            h.trazo(np.array([a0, a1]), 3.0, sem + 10 + k, color=(90, 80, 130), taper=(0.1, 0.1), jit=0.4)
    h.disco(cx, cy, 11, (74, 60, 96), sem=sem + 20, w=3.5)


def matorral(h, x, y, r, ang, sem=0):
    """Matorral rodante dibujado a garabatos: arcos pardos que giran, con la tinta oscura debajo."""
    rng = np.random.default_rng(sem + 3)
    for p_, (col, w) in enumerate((((44, 28, 24), 8.5), ((186, 134, 74), 4.2))):
        for k in range(7):
            rr = r * (0.45 + 0.55 * ((k * 0.37 + 0.1) % 1.0))
            sq = 0.55 + 0.45 * math.sin(k * 1.3 + 0.5)
            a0 = ang * (1 + 0.15 * k) + k * 0.9
            L = 2.2 + 1.2 * ((k * 0.61) % 1.0)
            u = np.linspace(a0, a0 + L, 22)
            pts = np.stack([x + rr * np.cos(u), y + rr * np.sin(u) * sq + (np.sin(u * 3 + k) * 4)], 1)
            h.trazo(pts, w * (0.7 + 0.3 * (k % 3) / 2), sem + k + p_ * 20, color=col, taper=(0.15, 0.2), jit=1.4)


def humo(h, x, y, t, vel=1.0, sem=0):
    """Volutas de humo que suben y se deshacen (chimenea)."""
    for k in range(5):
        u = ((t * 0.28 * vel + k / 5.0) % 1.0)
        r = 14 + 40 * u
        px = x + 34 * u + 16 * math.sin(u * 5 + k * 1.7)
        py = y - 170 * u
        a = (1 - u) * 0.34 * min(1.0, u * 8)
        h.forma(blob(px, py, r, r * 0.9, rad=[1, 1.1, 0.9, 1.05, 0.95, 1.08], n=6, sub=6), (118, 108, 160), None, w=0, jit=1.5,
                alfa=a, tex=0, sem=sem + k)


def estrella_brillo(h, x, y, r, t, ph, sem=0):
    k = 0.55 + 0.45 * math.sin(2 * math.pi * 0.9 * t + ph)
    h.forma(estrella(x, y, r * k, r * 0.18 * k, 4), (255, 248, 206), None, w=0, jit=0.3, tex=0, alfa=0.55 + 0.45 * k)


def polvo(h, x0, x1, y0, y1, t, n=26, sem=0, color=(210, 220, 255), alfa=0.5, r=2.6):
    """Motas de polvo que flotan en un haz de luz."""
    rng = np.random.default_rng(sem + 17)
    for i in range(n):
        ph = rng.uniform(0, 1)
        sp = rng.uniform(0.04, 0.12)
        u = (t * sp + ph) % 1.0
        x = x0 + (x1 - x0) * ((rng.uniform(0, 1) + 0.06 * math.sin(t * 0.7 + i)) % 1.0)
        y = y1 - (y1 - y0) * u
        k = math.sin(math.pi * u) * alfa
        h.forma(elipse_(x, y, r * (0.6 + rng.uniform(0, 0.8)), r * (0.6 + rng.uniform(0, 0.8)), n=10), color, None, w=0, jit=0.0,
                tex=0, alfa=k, sem=sem + i)
