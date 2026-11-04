# -*- coding: utf-8 -*-
"""Fondos cacheados de la playa (día y tarde) y del corte, pintados en acuarela."""
import math

import numpy as np

from acuarela import H, W, degradado, elipse, forma, lavado, linea, mancha_pts, rgb
from comun import cache

Y_MAR, Y_ORILLA, Y_SECA = 640, 860, 1010          # horizonte, orilla mojada, arena seca


def _playa(tarde, seed=5):
    im = np.zeros((H, W, 3), np.float32)
    cielo_a = rgb("a6d8ea") if not tarde else rgb("6a6aa4")
    cielo_b = rgb("f6ecd0") if not tarde else rgb("f4a463")
    degradado(im, cielo_a, cielo_b, 0, Y_MAR)
    rg = np.random.default_rng(seed)
    for k in range(5):                                               # nubes
        cx, cy = rg.uniform(80, W - 80), rg.uniform(120, 460)
        col = rgb("ffffff") if not tarde else rgb("f7c3a0")
        lavado(im, mancha_pts(cx, cy, rg.uniform(90, 160), seed + k, 0.3, ry=rg.uniform(30, 55)), col, 0.55, seed + k, humedo=10)
    mar = np.zeros_like(im)
    degradado(mar, rgb("3d93b6") if not tarde else rgb("4a6a9a"), rgb("7cc4cf") if not tarde else rgb("d98a6a"), Y_MAR, Y_ORILLA)
    im[Y_MAR:Y_ORILLA] = mar[Y_MAR:Y_ORILLA]
    for k in range(7):
        y = Y_MAR + 26 + k * 30
        xs = np.linspace(-20, W + 20, 30)
        linea(im, np.stack([xs, y + 6 * np.sin(xs / (60 + 9 * k) + k)], 1), 3.0, col=rgb("eaf6f4"), seed=seed + 30 + k, t=0,
              alfa=0.35, punta=False, hierve=False)
    are = np.zeros_like(im)
    degradado(are, rgb("efd8a4") if not tarde else rgb("e2b383"), rgb("d7b479") if not tarde else rgb("b88a62"), Y_ORILLA, H)
    im[Y_ORILLA:] = are[Y_ORILLA:]
    xs = np.linspace(-20, W + 20, 30)
    pol = np.concatenate([np.stack([xs, Y_ORILLA + 4 * np.sin(xs / 70)], 1), np.stack([xs[::-1], Y_SECA + 14 * np.sin(xs[::-1] / 110)], 1)])
    lavado(im, pol.astype(np.float32), rgb("b8925e"), 0.45, seed + 50, humedo=12)
    linea(im, np.stack([xs, Y_ORILLA + 4 * np.sin(xs / 70)], 1), 7, col=rgb("ffffff"), seed=seed + 51, t=0, alfa=0.8, punta=False,
          hierve=False)
    for k in range(70):                                              # granos y conchitas
        x, y = rg.uniform(0, W), rg.uniform(Y_SECA, H)
        lavado(im, elipse(x, y, rg.uniform(3, 8), rg.uniform(2, 5)), rgb("a98653"), 0.4, seed + 60 + k)
    for k in range(6):
        x, y = rg.uniform(60, W - 60), rg.uniform(Y_SECA + 300, H - 60)
        forma(im, elipse(x, y, 16, 11, rot=rg.uniform(-1, 1)), rgb("f4d6c8"), 0, seed + 140 + k, tinta=2.4)
    return im


def playa(tarde=0.0):
    """Playa de día (0) a tarde (1): mezcla de dos fondos cacheados."""
    a = cache(("playa", 0), lambda: _playa(False))
    if tarde <= 0:
        return a.copy()
    b = cache(("playa", 1), lambda: _playa(True))
    return a * (1 - tarde) + b * tarde


def _papel(col_a, col_b, seed):
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, col_a, col_b)
    rg = np.random.default_rng(seed)
    for k in range(8):
        lavado(im, mancha_pts(rg.uniform(0, W), rg.uniform(0, H), rg.uniform(220, 420), seed + k, 0.3), col_b, 0.25, seed + k,
               humedo=16)
    return im


def papel(nombre):
    cols = {"calido": (rgb("f7ecd4"), rgb("ecd6ae")), "cine": (rgb("3b2e28"), rgb("1d1715")),
            "cielo": (rgb("a6d8ea"), rgb("f6ecd0"))}
    a, b = cols[nombre]
    return cache(("papel", nombre), lambda: _papel(a, b, 40 + len(nombre))).copy()


def sepia(im, x0, y0, x1, y1, t, f=1.0):
    """Convierte un rectángulo a sepia de película vieja con parpadeo y rayas."""
    R = im[y0:y1, x0:x1]
    g = R @ np.array([0.3, 0.59, 0.11], np.float32)
    tono = np.stack([g * 1.07 + 0.04, g * 0.9 + 0.02, g * 0.66], -1)
    fl = 1 + 0.06 * math.sin(t * 47) + 0.04 * math.sin(t * 31)
    R[:] = R * (1 - f) + np.clip(tono * fl, 0, 1) * f
    rg = np.random.default_rng(int(t * 12))
    for k in range(3):
        x = int(rg.uniform(0, x1 - x0))
        R[:, max(0, x - 1):x + 1] *= 0.75 + 0.15 * rg.random()
    for k in range(5):
        x, y = int(rg.uniform(0, x1 - x0 - 4)), int(rg.uniform(0, y1 - y0 - 4))
        R[y:y + 4, x:x + 4] *= 0.4
