# -*- coding: utf-8 -*-
"""Miniaturas (python fab.py sol_apagado_8min miniatura). Estilo Kurzgesagt: pocas formas grandes, brillo,
1-2 palabras enormes amarillas con contorno negro y un personaje con cara de sorpresa."""
import math

import numpy as np

import fondos as F
import plano as P
from motor import NEGRO, circulo, rect_red

T = 0.37
WOB = 0.0
AMARILLO = (255, 214, 64)


def _texto(lz, s, x, y, px, rot=-0.03, color=AMARILLO):
    lz.texto(s, x, y, px, "geo_x", color=color, borde=NEGRO, borde_px=px * 0.11, rot=rot, capa=2, temblor=0.0)


def apagon(lz):
    """El Sol medio apagado; el pajarito lo mira sorprendido."""
    x, y, r = 620, 600, 420
    P.sol(lz, x, y, r, T)
    with lz.recorte(np.array([[x, -200], [2400, -200], [2400, 1400], [x, 1400]], float)):
        lz.relleno(circulo(x, y, r * 1.08, 160), (26, 22, 56))
        lz.relleno(circulo(x, y, r, 160), (46, 38, 78))
        P.discontinua(lz, P.arco_pts(x, y, r, -math.pi / 2, math.pi / 2, 120), (170, 160, 230), 7, 26, 18)
    P.tierra(lz, 1560, 330, 120, T, rot=1.2, ang_luz=math.pi, luz=0.6, ciudades=1.0)
    P.pajaro(lz, 1480, 1010, 2.6, T, mirar=(-1.0, -0.6), color=(126, 88, 214), voltear=True)
    _texto(lz, "¿SIN SOL?", 1360, 640, 170)
    return F.espacio(T)


def congelada(lz):
    """La Tierra oscura y congelada, termómetro en −240 °C."""
    P.tierra(lz, 700, 560, 380, T, rot=0.4, luz=0.15, hielo=1.0, nubes=0.0, ciudades=0.6)
    P.termometro(lz, 1430, 860, 1.25, 0.04, col=(120, 190, 255))
    P.pajaro(lz, 380, 1060, 1.9, T, mirar=(0.9, -0.8), tiritar=0.0, escarcha=1.0, color=(126, 88, 214))
    _texto(lz, "−240 °C", 1370, 210, 190, rot=0.02, color=(160, 220, 255))
    return F.espacio(T, tono=1)


def ocho(lz):
    """El Sol ya no está, su última luz viaja hacia la Tierra: 8:20."""
    x, y = 430, 560
    P.discontinua(lz, P.arco_pts(x, y, 230, 0, 2 * math.pi, 160), (170, 160, 230), 7, 26, 18)
    P.onda(lz, x, y, 760, 60, (255, 196, 110), alfa=1.0)
    for j in range(3):
        P.onda(lz, x, y, 700 - 50 * j, 12, (170, 130, 255), alfa=0.7, frente=0.6, estela=0.6)
    P.tierra(lz, 1520, 620, 190, T, rot=0.8, ang_luz=math.pi, luz=1.0)
    _texto(lz, "8:20", 1480, 250, 230)
    return F.espacio(T)


VARIANTES = {"apagon": apagon, "congelada": congelada, "ocho": ocho}
