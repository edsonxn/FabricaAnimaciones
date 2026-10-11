# -*- coding: utf-8 -*-
"""Mundos de la escena 11 (el Congreso): el salón del Congreso de Chilpancingo (interior) y utilería 2D para infografías (cadena que se rompe, escalera de castas)."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import plano as P
from motor import W, H, h01, circulo, elipse, rect_red
import mundos_e as me


def salon_congreso(lz, iso, t, W_=320, D_=260, H_=140):
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(176, 138, 104), pared_a=(246, 236, 212), pared_b=(234, 220, 192), friso=(130, 92, 72))
    for i in range(int(W_ / 36)):
        for j in range(int(D_ / 36)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 8 + i * 36, 8 + j * 36, 36, 36, (150, 110, 82), z=0.1, alfa=0.5)
    N.ventana_vista(lz, iso, c, "yi", 120, 200, 40, 120, t=t, cielo=(160, 206, 250), marco=(246, 236, 212), cortinas=(60, 130, 100), vista="ciudad")
    N.cuadro_pared if False else None
    B.cuadro_pared(lz, iso, c, "yi", 40, 70, 40, 44, color=(70, 120, 170))
    B.cuadro_pared(lz, iso, c, "yi", 250, 70, 40, 44, color=(150, 80, 80))
    I.cara_arco(lz, iso, c, "xi", 160, 214, 0, 100, (110, 74, 54))
    N.cortina(lz, iso, c, "xi", 40, 54, 0, 112, (60, 130, 100), t)
    return c


def amueblar_congreso(m, t):
    # estrado con mesa y pergamino; bancas en dos bloques
    m.add(110, 20, 220, 50, 26, lambda lz, iso: _estrado(lz, iso, t), clave=130)
    for r in range(3):
        for sg, x0 in ((0, 30), (1, 190)):
            m.add(x0, 110 + 40 * r, x0 + 100, 120 + 40 * r, 14, (lambda x0, r: (lambda lz, iso: (I.caja(lz, iso, x0, 112 + 40 * r, 100, 8, 9, (130, 90, 66)), I.caja(lz, iso, x0, 124 + 40 * r, 100, 3, 18, (146, 100, 72)))))(x0, r), clave=x0 + 112 + 40 * r)


def _estrado(lz, iso, t):
    I.caja(lz, iso, 100, 14, 130, 40, 6, (176, 136, 100))
    B.mesa(lz, iso, 120, 22, 90, 26, 20, color=(122, 82, 60), mantel=(60, 130, 100))
    me.libro(lz, iso, 134, 28, 21.4, 1.0, (150, 60, 60))
    lz.relleno(iso.pts([(160, 28, 21.6), (190, 28, 21.6), (190, 40, 21.6), (160, 40, 21.6)]), tint((252, 238, 200)))
    B.candelabro(lz, iso, 200, 36, 21, t, n=3)


# ------------------------------------------------------------------------------------------------ utilería 2D de infografías
def cadena(lz, x, y, n=6, t=0.0, rota=0.0, color=(150, 156, 176), ancho=60):
    """Cadena horizontal de n eslabones centrada en (x, y); con rota>0 se parte por la mitad y las dos mitades se separan."""
    sep = 150 * rota
    for i in range(n):
        lado = -1 if i < n / 2 else 1
        cx = x + (i - (n - 1) / 2) * ancho * 0.78 + lado * sep
        cy = y + (10 * rota * math.sin(rota * 8 + i) if rota > 0 else 0) + lado * 0 + (40 * rota * rota if rota > 0 else 0) * (1 if lado > 0 else 0.4)
        rot = 0.5 * rota * lado
        lz.trazo(elipse(cx, cy, ancho * 0.5, ancho * 0.30, rot if i % 2 == 0 else rot + 0.0, 24), color if i % 2 == 0 else P.oscurecer(color, 0.2), ancho * 0.16, cerrado=True, afinar=False, temblor=0.0, capa=2)
    if rota > 0.02:
        for k in range(8):
            a = k * 0.79 + rota * 6
            lz.relleno(circulo(x + math.cos(a) * 60 * rota, y + math.sin(a) * 40 * rota, 5 + 4 * h01(7, k), 8), (255, 236, 170), alfa=max(0.0, 1 - rota * 0.9), capa=2)


def escalera_castas(lz, x, y, t, aplana=0.0, k=1.0):
    """Cinco barras apiladas de distinto ancho (la jerarquía de castas) que, con aplana 0->1, se igualan en un solo bloque con degradado."""
    cols = [(236, 196, 90), (226, 130, 100), (196, 120, 170), (110, 170, 210), (120, 190, 130)]
    nombres = ["españoles", "criollos", "mestizos", "indígenas", "esclavos"]
    for i in range(5):
        w0 = 760 - 130 * i
        w = w0 + (760 - w0) * aplana
        h = 70
        yy = y + i * (h + 8 * (1 - aplana))
        xx = x + (i - 2) * 30 * (1 - aplana) * 0
        c = cols[i]
        c = tuple(int(a + (b - a) * aplana) for a, b in zip(c, (236, 220, 170)))
        lz.relleno(rect_red(xx - w / 2, yy - h / 2, w, h * k, 14), c, capa=2)
        if aplana < 0.9:
            lz.texto(nombres[i], xx, yy, 36, "geo", color=(60, 40, 90), borde=None, alfa=1.0 - aplana, temblor=0.0)
