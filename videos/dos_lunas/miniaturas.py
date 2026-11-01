# -*- coding: utf-8 -*-
"""Miniaturas (python fab.py dos_lunas miniatura). Estilo Kurzgesagt/Kuriox: pocas formas grandes, brillo,
1-2 palabras enormes amarillas con contorno negro y Kuri con cara de sorpresa."""
import math

import fondos as F
import plano as P
import kz_espacio as K
from motor import NEGRO

T = 0.37
AMARILLO = (255, 214, 64)
LUZ = math.pi * 1.15


def _texto(lz, s, x, y, px, rot=-0.03, color=AMARILLO):
    lz.texto(s, x, y, px, "geo_x", color=color, borde=NEGRO, borde_px=px * 0.11, rot=rot, capa=2, temblor=0.0)


def _ang(a, b):
    return math.atan2(b[1] - a[1], b[0] - a[0])


def dos(lz):
    """La Tierra abajo con sus mares estirados hacia DOS lunas grandes; Kuri encima, boquiabierto."""
    E, rE = (470, 900), 400
    L1, r1 = (1150, 330), 215
    L2, r2 = (1630, 500), 150
    K.tierra_marea(lz, E[0], E[1], rE, T, [(_ang(E, L1), 0.6), (_ang(E, L2), 0.4)], rot=0.9, ang_luz=LUZ, amp=0.07)
    lz.halo(L1[0], L1[1], r1 * 2.2, (200, 210, 255), alfa=0.25, r0=0.4)
    lz.halo(L2[0], L2[1], r2 * 2.2, (255, 200, 170), alfa=0.22, r0=0.4)
    K.cuerpo_rocoso(lz, L1[0], L1[1], r1, "luna", seed=1, ang_luz=LUZ, sombra=-0.1)
    K.cuerpo_rocoso(lz, L2[0], L2[1], r2, "luna", seed=7, ang_luz=LUZ, sombra=-0.1, tinte=(236, 196, 170))
    P.kuri(lz, 520, 520, 2.3, T, mirar=(0.9, -0.5), boca=1.0)
    _texto(lz, "¿DOS LUNAS?", 1330, 880, 170)
    return F.espacio(T)


def choque(lz):
    """Las dos lunas a punto de chocar, con un destello; la Tierra pequeña abajo y Kuri asustado."""
    L1, r1 = (820, 420), 230
    L2, r2 = (1230, 360), 150
    lz.halo(1050, 390, 380, (255, 210, 150), alfa=0.45, r0=0.15)
    K.cuerpo_rocoso(lz, L1[0], L1[1], r1, "luna", seed=1, ang_luz=LUZ, sombra=-0.1)
    K.cuerpo_rocoso(lz, L2[0], L2[1], r2, "luna", seed=7, ang_luz=LUZ, sombra=-0.1, tinte=(236, 196, 170))
    K.destello(lz, 1060, 380, 120, 0.0, alfa=1.0)
    K.tierra_marea(lz, 1620, 900, 210, T, [(_ang((1620, 900), L1), 0.5), (_ang((1620, 900), L2), 0.5)], rot=0.4, ang_luz=LUZ,
                   amp=0.08)
    P.kuri(lz, 200, 1040, 1.7, T, mirar=(0.8, -0.8), boca=1.0, tiritar=0.0)
    _texto(lz, "¿Y SI CHOCAN?", 1000, 930, 150, rot=0.02)
    return F.espacio(T, tono=1)


VARIANTES = {"dos": dos, "choque": choque}
