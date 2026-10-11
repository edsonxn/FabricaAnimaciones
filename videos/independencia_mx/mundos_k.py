# -*- coding: utf-8 -*-
"""Mundos de la escena 10 (Morelos): la carpintería del padre de Morelos y Cuautla sitiada (casas de adobe con trincheras y un anillo de campamentos realistas, palmeras y mangos)."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import W, H, h01, circulo, elipse, rect_red
import mundos_e as me


# ------------------------------------------------------------------------------------------------ carpintería (interior)
def carpinteria(lz, iso, t, W_=300, D_=240, H_=140):
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(186, 140, 100), pared_a=(236, 218, 184), pared_b=(224, 204, 170), friso=(130, 92, 70))
    for i in range(int(W_ / 34)):
        for j in range(int(D_ / 34)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 8 + i * 34, 8 + j * 34, 34, 34, (164, 120, 86), z=0.1, alfa=0.5)
    N.ventana_vista(lz, iso, c, "yi", 120, 200, 40, 118, t=t, cielo=(160, 206, 250), marco=(236, 218, 184), cortinas=(150, 100, 70), vista="ciudad")
    I.cara_arco(lz, iso, c, "xi", 150, 204, 0, 98, (110, 74, 54))
    # herramientas colgadas: sierra, martillo, escuadra (siluetas en la pared izquierda)
    for k, (a, col) in enumerate(((30, (170, 176, 190)), (60, (120, 90, 70)), (86, (150, 156, 170)))):
        I.cara_rect(lz, iso, c, "yi", a, a + 4, 50, 104, col)
    I.cara_rect(lz, iso, c, "yi", 26, 94, 100, 104, (170, 176, 190))
    return c


def amueblar_carpinteria(m, t):
    # banco de trabajo largo con tablones, caballetes, virutas, barriles y un montón de madera
    m.add(40, 90, 150, 120, 26, lambda lz, iso: _banco(lz, iso, 40, 90, t), clave=210)
    for i in range(4):
        m.add(190, 20 + 14 * i, 250, 30 + 14 * i, 30, (lambda i: (lambda lz, iso: I.caja(lz, iso, 190, 20 + 14 * i, 60, 11, 8, (196, 150, 104 + 8 * (i % 2)), z0=8 * 0)))(i), clave=250 + i)
    m.add(180, 140, 200, 160, 30, lambda lz, iso: O.barril(lz, iso, 190, 150, 1.3), clave=340)
    m.add(10, 190, 30, 210, 40, lambda lz, iso: N.maceta(lz, iso, 20, 200, 1.4, t), clave=210)
    for i in range(14):                                   # virutas en el piso
        x, y = 30 + 150 * h01(51, i), 130 + 80 * h01(52, i)
        m.add(x - 2, y - 2, x + 2, y + 2, 2, (lambda x, y: (lambda lz, iso: lz.relleno(iso.pts([(x, y, 0.4), (x + 6, y + 2, 0.4), (x + 5, y + 5, 0.4), (x - 1, y + 3, 0.4)]), tint((236, 206, 150)))))(x, y), clave=x + y - 400)


def _banco(lz, iso, x, y, t):
    B.mesa(lz, iso, x, y, 110, 30, 22, color=(150, 108, 76))
    I.caja(lz, iso, x + 10, y + 6, 70, 8, 3, (216, 170, 118), z0=22)           # tablón sobre el banco
    sx, sy = iso.P(x + 90, y + 12, 26)
    lz.relleno(rect_red(float(sx) - 2 * iso.z, float(sy) - 5 * iso.z, 16 * iso.z, 3 * iso.z, 1 * iso.z), tint((176, 182, 196)))   # serrucho


# ------------------------------------------------------------------------------------------------ Cuautla sitiada
class Cuautla:
    """Cuautla de Morelos (tierra caliente): plaza con el convento de Santo Domingo, casas de adobe con trincheras en las bocacalles, palmeras y mangos; fuera, el anillo de campamentos realistas con cañones."""
    CENTRO = (200.0, 200.0)

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -240, -240, 640, 640, color_top=(168, 190, 104), t=t, seed=171, esp=44)
        DC.parches(lz, iso, -240, -240, 640, 640, (168, 190, 104), n=30, var=24, seed=172, alfa=0.55, tam=(60, 120))
        I.suelo_curvo(lz, iso, [(40, 60), (360, 60), (380, 340), (20, 350)], (222, 202, 160), n=4)
        I.suelo_rect(lz, iso, 110, 120, 180, 150, (238, 220, 184))
        I.cuadricula(lz, iso, 110, 120, 290, 270, 24, color=(255, 255, 255), alfa=0.2)
        I.camino(lz, iso, [(-240, 200), (40, 200)], 40, (226, 204, 156))
        I.camino(lz, iso, [(360, 200), (640, 200)], 40, (226, 204, 156))
        I.camino(lz, iso, [(200, 350), (200, 640)], 40, (226, 204, 156))
        I.camino(lz, iso, [(200, 60), (200, -240)], 40, (226, 204, 156))

    def objetos(self, t, ring=True):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            A.iglesia(m, 150, 60, w=70, largo=90, h_nave=54, muro=(236, 214, 170), techo=A.TEJA2, torres=1, cupula_c=False)
            pal = [A.CAL, A.OCRE, A.ROSA, A.AZUL, A.VERDE_CAL]
            for i in range(4):
                A.casa_colonial(m, 40, 90 + i * 62, 60, 46, 40, muro=pal[i], techo=A.TEJA, eje="x", ventanas=1, seed=i + 410)
                A.casa_colonial(m, 300, 100 + i * 60, 60, 46, 40, muro=pal[(i + 2) % 5], techo=A.TEJA, eje="x", ventanas=1, seed=i + 420)
            for (x, y, w, d) in ((120, 100, 60, 8), (230, 100, 60, 8), (96, 270, 110, 8), (210, 270, 100, 8)):
                m.add(x, y, x + w, y + d, 10, (lambda x, y, w, d: (lambda lz, iso: O2.trinchera(lz, iso, x, y, w, d)))(x, y, w, d), clave=x + y)
            for (x, y) in ((70, 76), (330, 76), (70, 340), (330, 340)):
                m.add(x - 10, y - 10, x + 10, y + 10, 60, (lambda x, y: (lambda lz, iso: O.palmera(lz, iso, x, y, h=64, seed=int(x + y), t=self._t)))(x, y), clave=x + y)
            DC.bosque(m, -240, -240, 640, 640, n=40, seed=173, evitar=((0, 40, 400, 360),), t_fn=lambda: self._t, tipos=("palma", "arbol", "arbol"), min_d=32)
            if ring:
                for k in range(16):
                    a = 2 * math.pi * k / 16
                    x, y = 200 + 330 * math.cos(a), 200 + 270 * math.sin(a)
                    B.tienda_campana(m, x - 15, y - 11, color=(250, 244, 232), franja=(206, 70, 70), bandera=(206, 56, 70), t_fn=lambda: self._t)
                for k in range(8):
                    a = 2 * math.pi * (k + 0.5) / 8
                    B.canon(m, 200 + 290 * math.cos(a), 200 + 236 * math.sin(a), dir=1 if math.cos(a) < 0 else -1, t_fn=lambda: self._t)
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m
