# -*- coding: utf-8 -*-
"""Hoja del reparto (la Copia en sus vistas y expresiones) -> previews/ver_reparto.jpg
    python videos/sociedad_1200/_ver_reparto.py [paleta]"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import noir_color as NC
import reparto as RP
import comun as C

pal = sys.argv[1] if len(sys.argv) > 1 else "medianoche"
h = NC.NoirColor(pal)


def fondo(h):
    h.img[:] = NC.lut("piedra")[60]
    h.pieza(C.rect(-200, 900, 2400, 400), 70, 1, w=0, d=0, sombra=0, trama=0, rampa="asfalto")


def cuadro(fn, t):
    h.nuevo(t)
    h.camara(1.0, 960, 540)
    fondo(h)
    fn(h, t)
    C.ambiente(h, 0.55)
    h.luz_radial(700, 200, 1400, h.pal["sodio"], k=0.9)
    return h.acabado(t, niebla=dict(dens=0.12))


A = RP.Copia(sem=3, num="0417")
B = RP.Copia(sem=9, num="0388", grande=True)


def f1(h, t):
    dist = t * 120
    A.perfil(h, dict(x=300 + dist, y=930, s=0.95, d=1, andar=1.0, paso=RP.fase_paso(dist, 0.95), cara=dict(expr="neutro")))
    A.frente(h, dict(x=1000, y=930, s=0.95, cara=dict(expr="linea")))
    B.perfil(h, dict(x=1550, y=930, s=0.95, d=-1, brazos="alza", cara=dict(expr="astuto")))


def f2(h, t):
    A.perfil(h, dict(x=400, y=930, s=1.0, d=1, sentado=True, brazos="teclea", cara=dict(expr="texto", texto=["AYUDA", "ATASCADA"], t0=0)))
    A.cabeza(h, 1200, 480, 2.2, dict(expr="sorpresa"), d=-1)
    A.perfil(h, dict(x=1650, y=930, s=0.9, d=-1, gabardina=True, gafas=True, baston=True, cara=dict(expr="neutro")))


def f3(h, t):
    for i in range(12):
        for j in range(3):
            RP.copia_mini(h, 200 + i * 140 + j * 40, 600 + j * 150, 0.28 + j * 0.05, t, sem=i * 7 + j, cara="linea" if i % 2 else "neutro")
    A.cabeza(h, 500, 300, 1.4, dict(expr="error"))
    A.cabeza(h, 900, 300, 1.4, dict(expr="feliz"))
    A.cabeza(h, 1300, 300, 1.4, dict(expr="apagado" and "neutro", apagado=0.7))
    A.cabeza(h, 1700, 300, 1.4, dict(expr="alarma"))


tiles = []
for fn in (f1, f2, f3):
    im = (np.clip(cuadro(fn, 1.3), 0, 1) * 255).astype(np.uint8)
    tiles.append(im)
cv2.imwrite("previews/ver_reparto_full.png", cv2.cvtColor(tiles[1], cv2.COLOR_RGB2BGR))
hoja = np.vstack([cv2.resize(x, (960, 540)) for x in tiles])
cv2.imwrite("previews/ver_reparto.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("-> previews/ver_reparto.jpg")
