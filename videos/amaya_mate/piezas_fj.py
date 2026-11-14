# -*- coding: utf-8 -*-
"""Piezas pintadas compartidas por los planos f-j (organización, resistencia, consumación, repaso, cierre):
cabecera de etapa, pergamino, moneda, sobre secreto, fuerte de Cuautla, montañas, bandera trigarante, pastel, regalo, cama y luna."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave)
from comun import desborde
from kit_amaya import CAFE, CREMA, DORADO, GRIS, ROJO, VERDE, tarjeta

BLANCO_B = rgb("f7f4ea")
VERDE_B = rgb("2f8a4e")
ROJO_B = rgb("c8473f")


def base(TRAMOS, t, d=0.6):
    """Elige el tramo de t; el siguiente entra como gota de acuarela durante d s."""
    i = max(k for k, (t0, _) in enumerate(TRAMOS) if t >= t0 or k == 0)
    t0, f = TRAMOS[i]
    if i > 0 and t < t0 + d:
        return desborde(TRAMOS[i - 1][1](t), f(t), pr(t, t0, t0 + d), W / 2, H / 2)
    return f(t)


def cabecera(im, t, texto, col, seed, w=640):
    forma(im, rrect(30 + w / 2, 70, w, 90, 20), col, t, seed, tinta=4)
    rotulo(im, texto, 30 + w / 2, 74, 46, TINTA, t, seed=seed + 1, tinta=False)


def pergamino(im, x, y, w, h, t, seed, esc=1.0, col=None):
    if esc <= 0.02:
        return
    col = rgb("f3e3b8") if col is None else col
    w, h = w * esc, h * esc
    tarjeta(im, x, y, w, h, t, col, seed, tinta=4)
    for d in (-1, 1):
        forma(im, rrect(x, y + d * h / 2, w + 40 * esc, 46 * esc, 22 * esc), rgb("e2c98e"), t, seed + 3 + d, tinta=4,
              luz=(rgb("ffffff"), 0, -8, 0.3))


def moneda(im, x, y, s, t, seed=0):
    forma(im, elipse(x, y, 40 * s, 40 * s), DORADO, t, seed, tinta=3.5 * s, luz=(rgb("fff2c0"), -10, -10, 0.5))
    rotulo(im, "$", x, y + 3 * s, int(50 * s) + 2, rgb("8a6a1e"), t, seed=seed + 1, tinta=False)


def sobre(im, x, y, s, t, seed=0, rot=0.0):
    forma(im, rrect(x, y, 170 * s, 110 * s, 8 * s, rot), CREMA, t, seed, tinta=3.5 * s)
    c, sn = math.cos(rot), math.sin(rot)

    def P(px, py):
        return (x + px * c - py * sn, y + px * sn + py * c)
    linea(im, [P(-85 * s, -55 * s), P(0, 10 * s), P(85 * s, -55 * s)], 3 * s, seed=seed + 1, t=t, punta=False)
    forma(im, elipse(*P(0, 10 * s), 18 * s, 18 * s), ROJO, t, seed + 2, tinta=2.5 * s)


def fuerte(im, x, y, s, t, seed=0):
    """Pueblo amurallado (Cuautla): muralla con almenas, casitas y torre de iglesia detrás."""
    for k, (dx, hh, col) in enumerate(((-150, 150, rgb("e8c9a0")), (0, 220, rgb("f0d9b0")), (150, 130, rgb("e3bf96")))):
        forma(im, rrect(x + dx * s, y - (60 + hh / 2) * s, 140 * s, hh * s, 6 * s), col, t, seed + k, tinta=3.5)
        forma(im, np.array([(x + (dx - 80) * s, y - (60 + hh) * s), (x + dx * s, y - (110 + hh) * s),
                            (x + (dx + 80) * s, y - (60 + hh) * s)], np.float32), ROJO, t, seed + 4 + k, tinta=3.5)
    forma(im, rrect(x, y - 360 * s, 50 * s, 120 * s, 6 * s), rgb("f0d9b0"), t, seed + 8, tinta=3)  # campanario
    forma(im, rrect(x, y, 560 * s, 150 * s, 6 * s), rgb("c9b088"), t, seed + 9, tinta=5, sombra=(rgb("9a8460"), 20, 0, 0.5))
    for k in range(7):
        forma(im, rrect(x + (-240 + 80 * k) * s, y - 95 * s, 44 * s, 40 * s, 4 * s), rgb("c9b088"), t, seed + 10 + k, tinta=3)
    forma(im, rrect(x, y + 20 * s, 90 * s, 110 * s, 40 * s), rgb("5a3a22"), t, seed + 20, tinta=3.5)


def montanas(im, t, seed=0, y0=900):
    for k, (cx, w, h, col) in enumerate(((260, 620, 520, rgb("9fbf9a")), (900, 760, 640, rgb("8db08a")), (1560, 700, 560, rgb("a9c4a2")),
                                         (560, 640, 420, rgb("7ea07c")), (1240, 700, 470, rgb("769a76")))):
        forma(im, curva([(cx - w / 2, y0), (cx - w * 0.18, y0 - h * 0.8), (cx, y0 - h), (cx + w * 0.2, y0 - h * 0.75),
                         (cx + w / 2, y0)], 8), col, t, seed + k, tinta=4, sombra=(col * 0.75, 30, 0, 0.5))
        forma(im, curva([(cx - w * 0.09, y0 - h * 0.88), (cx, y0 - h), (cx + w * 0.1, y0 - h * 0.86), (cx, y0 - h * 0.8)], 5, True),
              rgb("f4f4ee"), t, seed + 10 + k, tinta=2.5) if h > 500 else None
    forma(im, np.array([(0, y0 - 10), (W, y0 - 20), (W, H), (0, H)], np.float32), rgb("8faa6e"), t, seed + 20, tinta=0)


def bandera_trigarante(im, x, y, w, h, t, seed=0, u=1.0, ondea=True):
    """Bandera de las Tres Garantías en diagonal: blanco, verde, rojo (u = cuánto se ha pintado, 0..1, franja a franja)."""
    if u <= 0.01:
        return
    linea(im, [(x - w / 2 - 14, y - h / 2 - 30), (x - w / 2 - 14, y + h / 2 + 260)], 12, CAFE, seed=seed, t=t)
    cols = (BLANCO_B, VERDE_B, ROJO_B)
    n = 18
    for k in range(3):
        v = pr(u, k / 3, (k + 1) / 3)
        if v <= 0:
            continue
        x0 = x - w / 2 + w * k / 3
        x1 = x0 + w / 3 * v
        xs = np.linspace(x0, x1, n)
        ond = (lambda xx: 14 * np.sin(xx / 90 - t * 5)) if ondea else (lambda xx: 0 * xx)
        top = np.stack([xs, y - h / 2 + ond(xs)], 1)
        bot = np.stack([xs[::-1], y + h / 2 + ond(xs[::-1])], 1)
        forma(im, np.vstack([top, bot]).astype(np.float32), cols[k], t, seed + 1 + k, tinta=4)
    if u >= 0.99:
        for k in range(3):
            cx = x - w / 2 + w * (k + 0.5) / 3
            forma(im, elipse(cx, y + 14 * math.sin(cx / 90 - t * 5), 26, 26), DORADO, t, seed + 6 + k, tinta=2.5)


def pastel(im, x, y, s, t, seed=0, velas=5):
    forma(im, rrect(x, y + 60 * s, 420 * s, 130 * s, 20 * s), rgb("f3b8c8"), t, seed, tinta=4)
    forma(im, rrect(x, y - 50 * s, 320 * s, 110 * s, 18 * s), rgb("fbe3c8"), t, seed + 1, tinta=4)
    linea(im, curva([(x - 210 * s, y + 10 * s), (x - 140 * s, y + 40 * s), (x - 70 * s, y + 10 * s), (x, y + 40 * s),
                     (x + 70 * s, y + 10 * s), (x + 140 * s, y + 40 * s), (x + 210 * s, y + 10 * s)], 6), 9 * s, CREMA,
          seed=seed + 2, t=t)
    forma(im, rrect(x, y + 140 * s, 500 * s, 26 * s, 12 * s), rgb("e9e4da"), t, seed + 3, tinta=3)
    for k in range(velas):
        vx = x + (-120 + 60 * k) * s
        forma(im, rrect(vx, y - 135 * s, 18 * s, 60 * s, 4 * s), [rgb("9dd0f0"), rgb("f2c14e"), rgb("a8d8b0")][k % 3], t,
              seed + 4 + k, tinta=2.5)
        fl = 1 + 0.15 * math.sin(t * 13 + k)
        forma(im, curva([(vx - 9 * s, y - 168 * s), (vx, y - (200 * fl) * s), (vx + 9 * s, y - 168 * s), (vx, y - 160 * s)], 5, True),
              rgb("f6b040"), t, seed + 10 + k, tinta=2)
        brillo(im, vx, y - 180 * s, 40 * s, rgb("ffcf70"), 0.5)


def regalo(im, x, y, s, t, seed=0, texto="", abre=0.0):
    forma(im, rrect(x, y, 300 * s, 240 * s, 10 * s), VERDE_B, t, seed, tinta=4.5)
    forma(im, rrect(x, y, 50 * s, 240 * s, 4 * s), ROJO_B, t, seed + 1, tinta=3)
    tapa_y = y - 140 * s - 120 * s * e_out(abre)
    forma(im, rrect(x, tapa_y, 330 * s, 60 * s, 10 * s, 0.2 * abre), VERDE_B, t, seed + 2, tinta=4.5)
    for d in (-1, 1):
        forma(im, elipse(x + d * 50 * s, tapa_y - 50 * s, 55 * s, 30 * s, d * 0.5), ROJO_B, t, seed + 3 + d, tinta=3.5)
    if texto:
        rotulo(im, texto, x, y + 20 * s, int(54 * s) + 2, CREMA, t, seed=seed + 6)


def luna(im, x, y, r, t, seed=0):
    brillo(im, x, y, r * 2.4, rgb("fff3c0"), 0.5)
    forma(im, elipse(x, y, r, r), rgb("fbeeb8"), t, seed, tinta=3.5)
    forma(im, elipse(x + r * 0.45, y - r * 0.2, r * 0.8, r * 0.8), rgb("2c3560"), t, seed + 1, tinta=0)


def cama(im, x, y, s, t, seed=0):
    forma(im, rrect(x - 300 * s, y - 60 * s, 40 * s, 260 * s, 10 * s), rgb("b98352"), t, seed, tinta=4)
    forma(im, rrect(x, y + 20 * s, 620 * s, 110 * s, 16 * s), rgb("b98352"), t, seed + 1, tinta=4)
    forma(im, rrect(x - 200 * s, y - 50 * s, 160 * s, 70 * s, 30 * s), CREMA, t, seed + 2, tinta=3.5)
    forma(im, rrect(x + 50 * s, y - 40 * s, 470 * s, 90 * s, 30 * s), rgb("9b8ad1"), t, seed + 3, tinta=4)
    for k in range(5):
        forma(im, elipse(x - 80 * s + 90 * k * s, y - 40 * s, 14 * s, 14 * s), rgb("f2c14e"), t, seed + 5 + k, tinta=0)


def zzz(im, x, y, t, s=1.0, seed=0):
    for k in range(3):
        u = (t * 0.6 + k / 3) % 1
        rotulo(im, "Z", x + 50 * k * s + 30 * u * s, y - 70 * k * s - 60 * u * s, int((40 + 18 * k) * s), rgb("dfe6ff"), t,
               seed=seed + k, alfa=1 - u)
