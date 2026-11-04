# -*- coding: utf-8 -*-
"""Fondos cacheados de «¿Cómo VE una IA?» (uno por proceso; se copian en cada cuadro).
    cuarto()      el cuarto de la niña al atardecer: pared con ventana y cielo, repisa con libros, planta, lámpara,
                  escritorio en primer plano (≥ 3 planos de profundidad)
    papel(nombre) hojas de color para los planos «de pizarrón» (calido, frio, noche)
    cabeza()      el interior de la cabeza de Kuri: azul-verde profundo con circuitos pintados y lucecitas
    neuronas(...) la red de farolitos con hilos que se encienden (animada; va encima de cabeza())
"""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, degradado, elipse, forma, lavado, linea, mancha_pts, rgb, rrect)
from comun import cache
from personajes import AMARILLO, BLANCO, OJO_K

PARED = rgb("f1dfc0")
PARED_OSC = rgb("dcc29a")
MADERA = rgb("b98352")
MADERA_OSC = rgb("8a5a34")
Y_MESA = 820                       # borde delantero del escritorio en el cuarto


def _cuarto():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, PARED, PARED_OSC)
    rg = np.random.default_rng(5)
    for k in range(9):
        lavado(im, mancha_pts(rg.uniform(0, W), rg.uniform(0, H * 0.8), rg.uniform(200, 380), 50 + k, 0.3), PARED_OSC, 0.22,
               50 + k, humedo=16)
    # ventana con cielo de atardecer y casas lejanas (plano lejano)
    vx, vy, vw, vh = 1380, 300, 520, 420
    sub = im[vy - vh // 2:vy + vh // 2, vx - vw // 2:vx + vw // 2]
    u = np.linspace(0, 1, vh, dtype=np.float32)[:, None, None]
    sub[:] = rgb("8fc3df") * (1 - u) + rgb("f7c58a") * u
    lavado(im, mancha_pts(vx - 120, vy - 90, 90, 70, 0.4, ry=34), BLANCO, 0.5, 70, humedo=10)
    lavado(im, mancha_pts(vx + 140, vy - 40, 70, 71, 0.4, ry=26), BLANCO, 0.45, 71, humedo=10)
    for k in range(7):                                                                    # tejados lejanos
        bx = vx - vw / 2 + 20 + k * 74
        bh = 60 + 40 * ((k * 37) % 5) / 5
        lavado(im, np.array([(bx, vy + vh / 2), (bx, vy + vh / 2 - bh), (bx + 34, vy + vh / 2 - bh - 30),
                             (bx + 68, vy + vh / 2 - bh), (bx + 68, vy + vh / 2)], np.float32), rgb("8a7fa8"), 0.55, 80 + k)
    for d in (-1, 1):                                                                     # marco y cruz
        forma(im, rrect(vx + d * (vw / 2 + 10), vy, 26, vh + 46, 6), rgb("f6efe2"), 0, 91 + d, tinta=4)
        forma(im, rrect(vx, vy + d * (vh / 2 + 10), vw + 46, 26, 6), rgb("f6efe2"), 0, 93 + d, tinta=4)
    forma(im, rrect(vx, vy, 18, vh, 4), rgb("f6efe2"), 0, 95, tinta=3)
    forma(im, rrect(vx, vy, vw, 18, 4), rgb("f6efe2"), 0, 96, tinta=3)
    for d in (-1, 1):                                                                     # cortinas
        cx = vx + d * (vw / 2 + 40)
        forma(im, curva([(cx - 40, vy - vh / 2 - 40), (cx + 40, vy - vh / 2 - 40), (cx + 30 * d + 20, vy + vh / 2 + 60),
                         (cx - 10, vy + vh / 2 + 80), (cx - 46, vy + vh / 2 + 50)], 7, True), rgb("6f9fc9"), 0, 97 + d,
              tinta=4, sombra=(rgb("4d7aa4"), 10 * d, 0, 0.5))
    # repisa con libros (plano medio)
    rx, ry = 420, 330
    forma(im, rrect(rx, ry, 560, 26, 6), MADERA, 0, 120, tinta=4, sombra=(MADERA_OSC, 0, -8, 0.5))
    cols = ["d9603b", "3f78c8", "e8b53e", "5aa06a", "9a5bb5", "e35d4a", "40a3a0", "d9603b"]
    x = rx - 250
    for k, c in enumerate(cols):
        bw, bh = 36 + (k * 13) % 20, 120 + (k * 29) % 50
        inc = 0.18 if k == 5 else 0.0
        forma(im, rrect(x + bw / 2, ry - 13 - bh / 2, bw, bh, 5, inc), rgb(c), 0, 130 + k, tinta=3.6,
              sombra=(rgb(c) * 0.7, 6, 0, 0.5))
        x += bw + 6
    forma(im, elipse(rx + 200, ry - 60, 46, 46), rgb("e9dcb2"), 0, 150, tinta=3.6)       # globo terráqueo
    lavado(im, mancha_pts(rx + 190, ry - 70, 26, 151, 0.4), rgb("5aa06a"), 0.8, 151)
    # cuadro en la pared
    forma(im, rrect(860, 260, 230, 170, 6), rgb("8a5a34"), 0, 160, tinta=4)
    forma(im, rrect(860, 260, 196, 136, 4), rgb("bfe0e6"), 0, 161, tinta=2.6)
    lavado(im, np.array([(770, 320), (840, 220), (900, 290), (950, 240), (950, 320)], np.float32), rgb("6e8a5a"), 0.8, 162)
    # planta en el suelo (plano medio)
    px_, py_ = 1180, 760
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.32
        p = [(px_, py_ - 60), (px_ + 70 * math.cos(a), py_ - 60 + 110 * math.sin(a)),
             (px_ + 130 * math.cos(a), py_ - 60 + 190 * math.sin(a))]
        forma(im, curva([p[0], (p[1][0] - 16, p[1][1]), p[2], (p[1][0] + 16, p[1][1])], 6, True), rgb("5aa06a"), 0, 170 + k,
              tinta=3.4, sombra=(rgb("3f7a4a"), 6, 0, 0.5))
    forma(im, np.array([(px_ - 60, py_ - 70), (px_ + 60, py_ - 70), (px_ + 46, py_ + 40), (px_ - 46, py_ + 40)], np.float32),
          rgb("d9603b"), 0, 180, tinta=4, sombra=(rgb("a8452a"), 12, 0, 0.5))
    # escritorio (primer plano)
    forma(im, np.array([(-40, Y_MESA - 60), (W + 40, Y_MESA - 90), (W + 40, H + 40), (-40, H + 40)], np.float32), MADERA, 0, 190,
          tinta=5, sombra=(MADERA_OSC, 0, -40, 0.45))
    for k in range(5):
        linea(im, curva([(-20, Y_MESA - 20 + 50 * k), (W / 2, Y_MESA - 40 + 52 * k), (W + 20, Y_MESA - 60 + 54 * k)], 8), 2.4,
              col=MADERA_OSC, seed=200 + k, t=0, alfa=0.45, punta=False)
    # lámpara de escritorio (brillo cálido)
    lx, ly = 250, Y_MESA - 40
    forma(im, elipse(lx, ly, 70, 18), rgb("3c5f7a"), 0, 210, tinta=3.6)
    linea(im, curva([(lx, ly), (lx + 30, ly - 160), (lx + 120, ly - 230)], 6), 12, col=rgb("3c5f7a"), seed=211, t=0, punta=False)
    forma(im, np.array([(lx + 80, ly - 270), (lx + 170, ly - 240), (lx + 200, ly - 160), (lx + 90, ly - 190)], np.float32),
          rgb("3c5f7a"), 0, 212, tinta=4)
    brillo(im, lx + 180, ly - 140, 200, rgb("ffd98a"), 0.22)
    # tazas y lápices
    forma(im, rrect(1640, Y_MESA - 10, 70, 80, 14), rgb("f6efe2"), 0, 220, tinta=4)
    for k in range(3):
        linea(im, [(1625 + k * 14, Y_MESA - 40), (1615 + k * 22, Y_MESA - 130)], 10, col=rgb(["e35d4a", "3f78c8", "e8b53e"][k]),
              seed=221 + k, t=0, punta=False)
    return im


def cuarto():
    return cache("cuarto", _cuarto).copy()


def _papel(col_a, col_b, seed):
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, col_a, col_b)
    rg = np.random.default_rng(seed)
    for k in range(10):
        lavado(im, mancha_pts(rg.uniform(0, W), rg.uniform(0, H), rg.uniform(220, 420), seed + k, 0.3), col_b, 0.25, seed + k,
               humedo=16)
    return im


def papel(nombre):
    cols = {"calido": (rgb("f7ecd4"), rgb("ecd6ae")), "frio": (rgb("e6f0ec"), rgb("c9ddd8")),
            "noche": (rgb("26314a"), rgb("141a2a")), "rosa": (rgb("f8e6dc"), rgb("efcdbd"))}
    a, b = cols[nombre]
    return cache(("papel", nombre), lambda: _papel(a, b, 40 + len(nombre))).copy()


# ------------------------------------------------------------ dentro de la cabeza de Kuri
FONDO_A = rgb("16323c")
FONDO_B = rgb("0b1a22")
CIRCUITO = rgb("2f6f74")


def _cabeza():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, FONDO_A, FONDO_B)
    rg = np.random.default_rng(9)
    for k in range(12):
        brillo(im, rg.uniform(0, W), rg.uniform(0, H), rg.uniform(120, 260), rgb("1f4a52"), 0.25)
    for k in range(26):                                                                   # pistas de circuito pintadas
        x, y = rg.uniform(0, W), rg.uniform(0, H)
        pts = [(x, y)]
        for j in range(3):
            if j % 2 == 0:
                x += rg.choice([-1, 1]) * rg.uniform(80, 260)
            else:
                y += rg.choice([-1, 1]) * rg.uniform(60, 180)
            pts.append((x, y))
        linea(im, pts, 3, col=CIRCUITO, seed=320 + k, t=0, alfa=0.55, punta=False)
        forma(im, elipse(x, y, 7, 7), CIRCUITO * 1.3, 0, 360 + k, tinta=0, alfa=0.7)
    return im


def cabeza():
    return cache("cabeza", _cabeza).copy()


def neuronas(im, t, n=60, seed=7, luz=1.0, cx=W / 2, cy=H / 2, rx=860, ry=430, ondas=1.0, alfa=1.0):
    """Red de farolitos (neuronas) unidos por hilos; las ondas de luz viajan de izquierda a derecha."""
    rg = np.random.default_rng(seed)
    P = np.stack([cx + rg.uniform(-rx, rx, n), cy + rg.uniform(-ry, ry, n)], 1)
    for i in range(n):
        d = np.hypot(*(P - P[i]).T)
        for j in np.argsort(d)[1:3]:
            if j > i:
                linea(im, [P[i], P[j]], 2.2, col=OJO_K * 0.55, seed=seed * 100 + i * 3 + int(j) % 3, t=t, alfa=0.5 * alfa,
                      punta=False)
    for i in range(n):
        x, y = P[i]
        onda = 0.5 + 0.5 * math.sin(t * 3.2 - x / 160) if ondas else 0.0
        f = luz * (0.25 + 0.75 * onda ** 3)
        forma(im, elipse(x, y, 11, 11), rgb("1e3c44") + OJO_K * 0.6 * f, t, seed * 100 + 500 + i, tinta=2.6, alfa=alfa)
        brillo(im, x, y, 22 + 18 * f, OJO_K, 0.35 * f * alfa)
    return P
