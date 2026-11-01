# -*- coding: utf-8 -*-
"""Miniaturas (python fab.py oxigeno_5s miniatura). Kuriox = por código, estilo Kurzgesagt como la del Sol (×9,8):
pocas formas grandes, brillo, 1-2 palabras enormes amarillas con contorno y Kuri con cara de sorpresa."""
import math

import numpy as np

import fondos as F
import plano as P
from motor import NEGRO, circulo, rect_red
import kit_oxi as KO
import kit_bio as KB

T = 0.37
WOB = 0.0
AMARILLO = (255, 214, 64)


def _texto(lz, s, x, y, px, rot=-0.03, color=AMARILLO):
    lz.texto(s, x, y, px, "geo_x", color=color, borde=NEGRO, borde_px=px * 0.11, rot=rot, capa=2, temblor=0.0)


def _kuri_casco(lz, x, y, s):
    with lz.capa(2):
        with lz.grupo(x, y, s):
            P.kuri(lz, 0, 70, 1.0, T, mirar=(-1.0, -0.4), boca=1.0)
            lz.relleno(circulo(0, -5, 110, 60), (200, 230, 255), alfa=0.18)
            lz.relleno(P.borde_luz(0, -5, 110, -math.pi * 0.75, 0.07), (255, 255, 255), alfa=0.5)


def tierra(lz):
    """La Tierra con su O2 (puntos rojos) que se apaga por la mitad; Kuri asustado."""
    x, y, r = 660, 560, 380
    P.tierra(lz, x, y, r, T, rot=1.9, ang_luz=math.pi * 1.15)
    for i in range(70):
        a = i / 70 * 2 * math.pi
        rr = r * (1.06 + 0.07 * ((i * 37) % 5) / 4)
        px, py = x + rr * math.cos(a), y + rr * math.sin(a)
        if math.cos(a) < 0.1:
            lz.relleno(circulo(px, py, 9, 12), (255, 96, 110))
        else:
            KO.fantasma(lz, px, py, 9, (255, 255, 255), alfa=0.8, ancho=2.5)
    _kuri_casco(lz, 1580, 820, 1.7)
    _texto(lz, "SIN OXÍGENO", 1390, 220, 150)
    _texto(lz, "5 SEGUNDOS", 1390, 420, 120, color=(255, 120, 120))
    return F.espacio(T)


def reloj(lz):
    """Cronómetro con el 5 y la Tierra detrás."""
    P.tierra(lz, 1450, 640, 330, T, rot=1.6, ang_luz=math.pi * 1.15)
    KB.cronometro(lz, 600, 560, 330, frac=0.62, numero=5, col=(236, 72, 84))
    _kuri_casco(lz, 1700, 300, 1.2)
    _texto(lz, "¿SIN O2?", 1300, 170, 150)
    return F.espacio(T, tono=1)


def ciudad(lz):
    """Un edificio que se deshace en polvo dejando el acero; Kuri con las manos pegadas."""
    lz.relleno(np.array([[0, 820], [1920, 820], [1920, 1080], [0, 1080]], float), (120, 86, 84))
    for i, (x, w, h, col) in enumerate(((330, 260, 560, (232, 178, 196)), (760, 220, 420, (150, 172, 226)))):
        corte = 820 - h * (0.45 + 0.2 * i)
        lz.relleno(rect_red(x - w / 2, corte, w, 820 - corte, 6), col)
        for c in np.linspace(x - w / 2 + 14, x + w / 2 - 14, 4):
            lz.trazo(np.array([[c, 820], [c, 820 - h]]), (150, 156, 186), 9, afinar=False)
        for j in range(1, int(h // 90) + 1):
            lz.trazo(np.array([[x - w / 2 + 14, 820 - j * 90], [x + w / 2 - 14, 820 - j * 90]]), (150, 156, 186), 7, afinar=False)
        for k in range(30):
            px = x - w / 2 + (k * 37) % w
            py = corte + (k * 53) % 260
            lz.relleno(circulo(px, py, 8 + (k % 4) * 3, 12), (226, 206, 186), alfa=0.9)
        lz.relleno(np.array([[x - w / 2 - 60, 822], [x, 760 - 40 * i], [x + w / 2 + 60, 822]], float), (214, 190, 170))
    with lz.capa(2):
        P.kuri(lz, 1520, 1000, 2.4, T, mirar=(0.0, -1.0), aleteo=1.0, tiritar=0.0, boca=1.0)
        lz.halo(1520, 1000 - 205 * 2.4 * 0.95, 140, (255, 236, 170), alfa=0.9)
    _texto(lz, "SIN OXÍGENO", 1330, 200, 150)
    _texto(lz, "5 s", 1720, 420, 150, color=(255, 120, 120))
    return F.degradado(T, (92 / 255, 64 / 255, 110 / 255), (214 / 255, 150 / 255, 140 / 255))


VARIANTES = {"tierra": tierra, "reloj": reloj, "ciudad": ciudad}
