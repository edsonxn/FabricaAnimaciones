# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 11 (Tenamaxtli): orden de búsqueda con su retrato a tinta, interior de piedra de Valladolid con ventana a la ciudad,
pluma que escribe sobre el memorial, y la ventana con lluvia del final."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H


def orden_busqueda(lz, x, y, s, t, k, sello_k=0.0, rot=-0.04):
    """Papel de orden con el rostro de Tenamaxtli dibujado a tinta (busto en sepia), texto simulado y sello rojo."""
    if k <= 0.01:
        return
    w, h = 520 * s * k, 660 * s * k
    with lz.grupo(x, y, 1.0, rot):
        lz.relleno(rect_red(-w / 2 + 12, -h / 2 + 16, w, h, 10), (20, 10, 30), alfa=0.35, capa=1)
        lz.relleno(rect_red(-w / 2, -h / 2, w, h, 10), (244, 232, 204), capa=1)
        lz.relleno(rect_red(-w / 2, -h / 2, w, 70 * s * k, 10), (214, 196, 160), capa=1)
        P.rotulo(lz, 0, -h / 2 + 36 * s * k, "SE BUSCA", px=int(46 * s * k) + 1, color=(110, 60, 50), alfa=1.0, sombra=0.0)
        with lz.recorte(rect_red(-w * 0.32, -h * 0.36, w * 0.64, h * 0.5, 8)):
            lz.relleno(rect_red(-w * 0.32, -h * 0.36, w * 0.64, h * 0.5, 8), (232, 214, 180), capa=1)
            spec = dict(K2.TIPOS["jefe_caxcan"], ropa=(150, 110, 80), ropa2=(190, 150, 110), collar=(150, 110, 80), pintura=False)
            K2.busto(lz, 0, h * 0.10, 66 * s * k, spec, t, yaw=0.1, emocion="serio", ojos="abiertos", seed=31, alfa=0.85)
            lz.relleno(rect_red(-w * 0.32, -h * 0.36, w * 0.64, h * 0.5, 8), (170, 120, 70), alfa=0.25, capa=1)
        for i in range(5):
            ww = w * (0.7 - 0.08 * (i % 3))
            lz.relleno(rect_red(-ww / 2, h * 0.2 + i * 34 * s * k, ww, 10 * s * k, 5), (150, 110, 90), alfa=0.6, capa=1)
        if sello_k > 0.01:
            lz.relleno(circulo(w * 0.28, h * 0.36, 56 * s * sello_k, 30), (196, 40, 50), capa=1)
            lz.relleno(circulo(w * 0.28, h * 0.36, 40 * s * sello_k, 26), (220, 70, 70), capa=1)


def sala_valladolid(lz, t, luz=1.0):
    """Interior de piedra castellana: muro de sillares, arco con ventana que da a las torres de Valladolid, mesa con libros."""
    lz.relleno(rect_red(0, 0, W, H, 0), (150, 126, 118), capa=0)
    for f in range(14):                                                # sillares
        for c in range(14):
            x = c * 150 + (75 if f % 2 else 0) - 40
            y = f * 74
            lz.relleno(rect_red(x + 3, y + 3, 144, 68, 6), (164, 140, 130) if (f + c) % 3 else (156, 132, 124), capa=0)
    # ventana con arco
    cx, cy = 960, 470
    lz.relleno(rect_red(cx - 250, cy - 260, 500, 560, 250), (110, 88, 90), capa=0)
    with lz.recorte(rect_red(cx - 220, cy - 230, 440, 520, 220)):
        lz.relleno(rect_red(cx - 220, cy - 230, 440, 520, 0), (170, 200, 236), capa=0)
        lz.relleno(rect_red(cx - 220, cy + 60, 440, 300, 0), (196, 170, 150), capa=0)
        for i, (dx, hh) in enumerate(((-150, 200), (-60, 260), (40, 180), (130, 240))):        # torres de la ciudad
            lz.relleno(rect_red(cx + dx - 26, cy + 60 - hh, 52, hh, 3), (210, 186, 166), capa=0)
            lz.relleno(np.array([(cx + dx - 32, cy + 60 - hh), (cx + dx, cy + 60 - hh - 50), (cx + dx + 32, cy + 60 - hh)]), (110, 110, 140), capa=0)
        lz.relleno(rect_red(cx - 6, cy - 230, 12, 520, 0), (90, 70, 74), capa=0)
        lz.relleno(rect_red(cx - 220, cy + 20, 440, 12, 0), (90, 70, 74), capa=0)
    lz.halo(cx, cy, 520, (255, 236, 200), alfa=0.25 * luz, capa=0)
    # mesa
    lz.relleno(rect_red(-20, 880, W + 40, 220, 0), (110, 70, 54), capa=1)
    lz.relleno(rect_red(-20, 870, W + 40, 26, 4), (140, 92, 70), capa=1)
    for i, (x, w, col) in enumerate(((240, 140, (150, 50, 50)), (250, 120, (70, 90, 130)), (1560, 160, (120, 90, 60)))):
        lz.relleno(rect_red(x, 840 - 26 * i, w, 30, 4), col, capa=1)


def pluma(lz, x, y, s, t, capa=2):
    """Pluma de ave que escribe (la punta en x, y)."""
    with lz.grupo(x, y, 1.0, -0.7 + 0.05 * math.sin(t * 9)):
        q = [(0, 0), (-0.15 * s, -1.0 * s), (0.25 * s, -3.6 * s), (0.9 * s, -5.6 * s), (0.6 * s, -3.2 * s), (0.25 * s, -1.0 * s)]
        lz.relleno(np.array(catmull(np.array(q, float), 6, True)), (250, 248, 240), capa=capa)
        lz.trazo(np.array([(0, 0), (0.75 * s, -5.4 * s)]), (180, 170, 170), 0.08 * s, afinar=False, temblor=0.0, capa=capa)


def ventana_lluvia(lz, t, k=1.0):
    """Ventana de noche con lluvia, una silla vacía y una flor de xúchitl que se marchita sobre la mesa (el final de Tenamaxtli)."""
    lz.relleno(rect_red(0, 0, W, H, 0), (52, 44, 70), capa=0)
    cx, cy = 1180, 430
    lz.relleno(rect_red(cx - 260, cy - 300, 520, 600, 40), (36, 30, 52), capa=0)
    with lz.recorte(rect_red(cx - 230, cy - 270, 460, 540, 30)):
        lz.relleno(rect_red(cx - 230, cy - 270, 460, 540, 0), (40, 50, 96), capa=0)
        for i in range(60):
            x = cx - 230 + 460 * h01(3, i)
            y = cy - 270 + ((t * 600 + 900 * h01(4, i)) % 600)
            lz.trazo(np.array([(x, y), (x - 6, y + 30)]), (150, 170, 230), 2.0, afinar=False, temblor=0.0, capa=0)
        lz.relleno(rect_red(cx - 6, cy - 270, 12, 540, 0), (30, 24, 44), capa=0)
        lz.relleno(rect_red(cx - 230, cy - 6, 460, 12, 0), (30, 24, 44), capa=0)
    lz.halo(cx, cy, 380, (120, 140, 220), alfa=0.18, capa=0)
    # silla vacía
    x0, y0 = 620, 1000
    lz.relleno(rect_red(x0 - 90, y0 - 330, 26, 330, 4), (90, 60, 50), capa=1)
    lz.relleno(rect_red(x0 + 64, y0 - 330, 26, 330, 4), (90, 60, 50), capa=1)
    lz.relleno(rect_red(x0 - 100, y0 - 180, 200, 30, 6), (110, 74, 58), capa=1)
    for j in range(3):
        lz.relleno(rect_red(x0 - 80, y0 - 320 + 40 * j, 160, 16, 4), (110, 74, 58), capa=1)
    lz.relleno(rect_red(x0 - 90, y0 - 150, 22, 150, 4), (80, 54, 44), capa=1)
    lz.relleno(rect_red(x0 + 68, y0 - 150, 22, 150, 4), (80, 54, 44), capa=1)
    # mesa con vela
    lz.relleno(rect_red(900, 880, 700, 30, 6), (110, 74, 58), capa=1)
    lz.relleno(rect_red(940, 910, 26, 190, 4), (90, 60, 50), capa=1)
    lz.relleno(rect_red(1540, 910, 26, 190, 4), (90, 60, 50), capa=1)
    lz.relleno(rect_red(1400, 800, 26, 80, 6), (240, 232, 214), capa=1)
    f = 0.85 + 0.15 * math.sin(t * 11)
    lz.halo(1413, 780, 200 * f, (255, 200, 120), alfa=0.35, capa=1)
    lz.relleno(elipse(1413, 784, 9, 18 * f, 0, 12), (255, 220, 140), capa=1)
