# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 12 (la Revolución): la calle de Juchipila en 1909 con la tienda «El Nuevo Mundo» de Crispín Robles y la reunión
del club antirreeleccionista; la penitenciaría de Lecumberri (vista aérea radial) y la celda; tipos de personaje de 1910."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H

ROBLES = dict(K2.TIPOS["comerciante"], ropa=(60, 70, 96), ropa2=(250, 244, 230), pelo=(40, 30, 32), bigote=True, piel="trigueña")
ROBLES_REV = dict(K2.TIPOS["revolucionario"], ropa=(214, 200, 170), ropa2=(130, 80, 60), bigote=True, piel="trigueña")
RURAL = dict(K2.TIPOS["revolucionario"], ropa=(84, 70, 60), ropa2=(200, 170, 110), torso="levita", tocado="sombrero_ala", bigote=True, piel="clara")
VECINO = lambda seed: dict(K2.variar("hombre", seed), tocado="sombrero_palma" if seed % 2 else None, torso="camiseta")


def calle_1909(lz, t, cx=0.0, y=860, noche=0.0):
    """Calle empedrada con portales, casas de colores con balcones y, al centro, la tienda «El Nuevo Mundo» con su letrero y la manta del club."""
    lz.relleno(rect_red(-20, y, W + 40, H - y + 20, 0), (196, 176, 150), capa=0)
    for k in range(14):                                                    # empedrado
        for j in range(4):
            xx = ((k * 150 + 75 * (j % 2) - cx) % (W + 300)) - 150
            lz.relleno(elipse(xx, y + 40 + 55 * j, 60, 14, 0, 14), (180, 160, 136), alfa=0.8, capa=0)
    cols = [(236, 196, 120), (214, 120, 110), (150, 190, 170), (226, 170, 150), (190, 170, 220)]
    for i in range(8):                                                     # fachadas
        x = 260 * i - (cx % 260) - 140
        c = cols[i % 5]
        lz.relleno(rect_red(x, y - 420, 262, 420, 0), c, capa=0)
        lz.relleno(rect_red(x, y - 420, 262, 26, 0), P.oscurecer(c, 0.15), capa=0)
        for j in range(2):
            wx = x + 50 + 110 * j
            lz.relleno(rect_red(wx, y - 330, 60, 110, 30), (80, 60, 70), capa=0)
            lz.relleno(rect_red(wx - 10, y - 220, 80, 12, 3), (70, 60, 70), capa=0)          # balcón
            for b in range(5):
                lz.relleno(rect_red(wx - 6 + 17 * b, y - 250, 4, 30, 1), (70, 60, 70), capa=0)
        lz.relleno(rect_red(x + 90, y - 150, 80, 150, 40), (110, 76, 60), capa=0)
    # la tienda (fija en el centro de la calle, x = 960 - cx * 0.0 para que la cámara se acerque a ella)
    tx = 960 - cx * 0.6
    lz.relleno(rect_red(tx - 330, y - 470, 660, 470, 0), (240, 226, 200), capa=0)
    lz.relleno(rect_red(tx - 330, y - 470, 660, 30, 0), (200, 180, 150), capa=0)
    lz.relleno(rect_red(tx - 260, y - 420, 520, 80, 10), (60, 90, 120), capa=0)
    P.rotulo(lz, tx, y - 380, "EL NUEVO MUNDO", px=46, color=(255, 236, 190), alfa=1.0, sombra=0.0)
    for j in range(3):                                                     # puertas/escaparates
        lz.relleno(rect_red(tx - 270 + 190 * j, y - 300, 150, 300, 70), (90, 60, 52), capa=0)
        lz.relleno(rect_red(tx - 260 + 190 * j, y - 290, 130, 150, 60), (250, 220, 150), alfa=0.35 + 0.5 * noche, capa=0)
    # mercancía en la entrada: costales, cajas, rollos de tela
    for j, (dx, col) in enumerate(((-300, (200, 160, 100)), (-250, (214, 90, 80)), (260, (80, 140, 190)), (310, (226, 196, 120)))):
        lz.relleno(rect_red(tx + dx - 22, y - 60, 44, 60, 8), col, capa=1)


def manta_club(lz, x, y, k, t):
    """Manta del club antirreeleccionista colgada sobre la tienda."""
    if k <= 0.01:
        return
    w = 820 * k
    ond = [(x - w / 2 + w * u, y + 10 * math.sin(math.pi * u) + 4 * math.sin(t * 3 + u * 6)) for u in np.linspace(0, 1, 12)]
    lz.relleno(np.array(ond + [(p[0], p[1] + 80 * k) for p in ond[::-1]]), (250, 246, 236), capa=1)
    lz.relleno(np.array([(p[0], p[1] + 8 * k) for p in ond] + [(p[0], p[1] + 20 * k) for p in ond[::-1]]), (60, 140, 90), capa=1)
    lz.relleno(np.array([(p[0], p[1] + 62 * k) for p in ond] + [(p[0], p[1] + 74 * k) for p in ond[::-1]]), (200, 60, 60), capa=1)
    P.rotulo(lz, x, y + 42 * k, "CLUB ANTIRREELECCIONISTA", px=int(38 * k) + 1, color=(60, 50, 60), alfa=1.0, sombra=0.0)


def lecumberri(lz, x, y, r, t, k=1.0):
    """La penitenciaría de Lecumberri vista desde arriba: torre central y crujías en estrella (panóptico), muro perimetral."""
    if k <= 0.01:
        return
    r = r * k
    lz.relleno(circulo(x, y, r * 1.25, 8), (110, 96, 110), capa=1)
    lz.relleno(circulo(x, y, r * 1.18, 8), (176, 160, 150), capa=1)
    for i in range(7):
        a = -math.pi / 2 + i * 2 * math.pi / 7
        c, s = math.cos(a), math.sin(a)
        n = (-s, c)
        p = [(x + n[0] * r * 0.09, y + n[1] * r * 0.09), (x + c * r + n[0] * r * 0.09, y + s * r + n[1] * r * 0.09),
             (x + c * r - n[0] * r * 0.09, y + s * r - n[1] * r * 0.09), (x - n[0] * r * 0.09, y - n[1] * r * 0.09)]
        lz.relleno(np.array(p), (210, 190, 176), capa=1)
        lz.relleno(np.array([p[0], p[1], ((p[1][0] + p[2][0]) / 2, (p[1][1] + p[2][1]) / 2), (x, y)]), (180, 150, 140), alfa=0.8, capa=1)
    lz.relleno(circulo(x, y, r * 0.18, 20), (150, 120, 120), capa=1)
    lz.relleno(circulo(x, y, r * 0.1, 16), (196, 170, 160), capa=1)


def barrotes(lz, x0, y0, x1, y1, n=8, capa=2):
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        lz.relleno(rect_red(x - 9, y0, 18, y1 - y0, 6), (60, 56, 72), capa=capa)
        lz.relleno(rect_red(x - 9, y0, 6, y1 - y0, 3), (110, 104, 126), capa=capa)
    for yy in (y0, (y0 + y1) / 2, y1):
        lz.relleno(rect_red(x0 - 20, yy - 10, x1 - x0 + 40, 20, 6), (60, 56, 72), capa=capa)
