# -*- coding: utf-8 -*-
"""Mundos de la escena 8 (Guadalajara y Calderón): la plaza de Guadalajara con catedral y palacio, la imprenta (interior con prensa) y el campo de batalla del puente de Calderón."""
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


# ------------------------------------------------------------------------------------------------ Guadalajara
class Guadalajara:
    """Plaza de Armas de Guadalajara: catedral al norte, Palacio de Gobierno a un lado, portales con arcos al sur, fuente, jardines con fresnos, casas de cantera y calles."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -120, 560, 480, color_top=(190, 190, 128), t=t, seed=131, esp=40)
        DC.parches(lz, iso, -120, -120, 560, 480, (190, 190, 128), n=20, var=22, seed=132, alfa=0.55, tam=(50, 100))
        I.suelo_curvo(lz, iso, [(-60, 120), (500, 120), (520, 420), (-70, 430)], (230, 208, 170))
        I.suelo_rect(lz, iso, 80, 150, 280, 230, (244, 226, 190))
        I.cuadricula(lz, iso, 80, 150, 360, 380, 26, color=(255, 255, 255), alfa=0.22)
        I.camino(lz, iso, [(-120, 300), (80, 300)], 50, (234, 214, 176))
        I.camino(lz, iso, [(360, 300), (560, 300)], 50, (234, 214, 176))
        I.camino(lz, iso, [(220, 380), (220, 500)], 46, (234, 214, 176))
        # jardines con cuadros de flores
        for (x, y) in ((100, 170), (270, 170), (100, 300), (270, 300)):
            I.suelo_rect(lz, iso, x, y, 70, 60, (130, 190, 110))
            I.suelo_rect(lz, iso, x + 6, y + 6, 58, 48, (236, 120, 150), alfa=0.35)

    def objetos(self, t, gente=1.0):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.catedral(m, 80, -70, w=130, largo=170, h=82)
            B.palacio(m, 250, -30, w=250, d=70, h=70, campana=False)
            A.portal_arcos(m, 70, 392, 10, paso=24, d=16, h=42, muro=A.CAL)
            pal = [A.OCRE, A.ROSA, A.CAL, A.AZUL, A.VERDE_CAL]
            for i in range(4):
                A.casa_colonial(m, -100, 140 + i * 58, 64, 44, 46 + 6 * (i % 2), muro=pal[i], techo=A.TEJA2, eje="x", ventanas=2, balcon=(i % 2 == 0), seed=i + 330)
            for i in range(4):
                A.casa_colonial(m, 430, 150 + i * 62, 60, 48, 48, muro=pal[(i + 2) % 5], techo=A.TEJA, eje="x", ventanas=2, balcon=(i % 2 == 1), seed=i + 340)
            m.add(206, 256, 234, 284, 40, lambda lz, iso: O.fuente(lz, iso, 220, 270, t=self._t, s=1.3), clave=490)
            for (x, y) in ((90, 160), (350, 160), (90, 370), (350, 370), (220, 170), (220, 360)):
                m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=0.0)))(x, y), clave=x + y)
            for (x, y) in ((92, 200), (350, 200), (92, 340), (350, 340), (160, 190), (280, 190)):
                m.add(x - 8, y - 8, x + 8, y + 8, 60, (lambda x, y: (lambda lz, iso: O.arbol(lz, iso, x, y, h=50, color=(80, 160, 90), seed=int(x + y))))(x, y), clave=x + y + 5)
            DC.bosque(m, -120, -120, 560, 480, n=10, seed=133, evitar=((-120, 100, 560, 440), (60, -80, 520, 90)), t_fn=lambda: self._t, tipos=("arbol", "cipres"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        if gente > 0.01:
            mu = G.Multitud()
            tipos = ("campesino", "campesina", "comerciante", "mestizo", "noble", "dama", "arriero", "indigena", "nino")
            for i in range(int(16 * gente)):
                mu.ronda((130 + 14 * i, 250 + 18 * (i % 4)), 50, tipos[i % 9], n=1, seed=3600 + i * 5, h=40 if tipos[i % 9] != "nino" else 28)
            mu.camina([(-120, 304), (220, 304), (560, 304)], "arriero", vel=13, seed=3, bucle="ida_vuelta")
            mu.dibujar(m, t)
        return m


# ------------------------------------------------------------------------------------------------ imprenta (interior)
def imprenta(lz, iso, t, W_=300, D_=240, H_=140):
    """Taller de imprenta del siglo XIX en corte: ventana con la calle, estantes con cajas de tipos, cuerdas con pliegos colgados, barriles de tinta."""
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(170, 130, 98), pared_a=(240, 228, 200), pared_b=(228, 212, 184), friso=(130, 96, 76))
    for i in range(int(W_ / 34)):
        for j in range(int(D_ / 34)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 8 + i * 34, 8 + j * 34, 34, 34, (146, 106, 80), z=0.1, alfa=0.5)
    N.ventana_vista(lz, iso, c, "yi", 120, 200, 40, 118, t=t, cielo=(160, 206, 250), marco=(240, 226, 200), cortinas=(70, 110, 150), vista="ciudad")
    N.cuadro_retrato(lz, iso, c, "yi", 28, 66, 30, 38, fondo=(90, 110, 150))
    I.cara_arco(lz, iso, c, "xi", 160, 214, 0, 98, (110, 74, 54))
    # cuerdas con pliegos colgados (en la pared izquierda)
    for k in range(2):
        z = 92 - 14 * k
        for j in range(9):
            a = 220 + j * 9 if False else 215 + j * 8.5
            I.cara_rect(lz, iso, c, "yi", 214 + j * 9.4, 214 + j * 9.4 + 6.6, z - 16, z, (252, 248, 236) if (j + k) % 2 else (246, 238, 220))
        I.cara_rect(lz, iso, c, "yi", 210, 300, z, z + 0.9, (120, 96, 80), tono=False)
    return c


def amueblar_imprenta(m, t, k_prensa=0.0):
    m.add(40, 70, 120, 140, 70, lambda lz, iso: prensa(lz, iso, 60, 80, t, k_prensa), clave=200)
    m.add(150, 20, 214, 36, 60, lambda lz, iso: B.estante(lz, iso, 150, 8, 60, 14, 74), clave=190)
    m.add(10, 150, 40, 180, 30, lambda lz, iso: O.barril(lz, iso, 22, 164, 1.2, (60, 70, 100)), clave=190)
    m.add(10, 120, 40, 150, 30, lambda lz, iso: O.barril(lz, iso, 22, 134, 1.2, (60, 70, 100)), clave=160)
    m.add(10, 200, 30, 220, 40, lambda lz, iso: N.maceta(lz, iso, 20, 210, 1.4, t), clave=230)


def prensa(lz, iso, x, y, t, k):
    """Prensa de tornillo de madera: bastidor, platina, barra que gira (k=1: en pleno trabajo) y pilas de papel."""
    I.sombra_suelo(lz, iso, x, y, 60, 46, 56)
    I.caja(lz, iso, x, y, 60, 46, 8, (120, 82, 62))
    for dx in (2, 52):
        I.caja(lz, iso, x + dx, y + 6, 6, 34, 56, (146, 100, 70))
    I.caja(lz, iso, x, y + 4, 60, 38, 6, (130, 90, 66), z0=54)
    I.caja(lz, iso, x + 10, y + 12, 40, 22, 4, (230, 226, 216), z0=8)       # platina con el pliego
    for j in range(3):
        lz.relleno(iso.pts([(x + 14, y + 16 + 5 * j, 12.2), (x + 46, y + 16 + 5 * j, 12.2), (x + 46, y + 17.4 + 5 * j, 12.2), (x + 14, y + 17.4 + 5 * j, 12.2)]), tint((50, 50, 70)), alfa=0.85)
    # tornillo y barra giratoria
    a = (math.sin(t * 5.0) if k > 0.01 else 0.0) * 0.9 * k
    sx, sy = iso.P(x + 30, y + 23, 60)
    kz = iso.z
    lz.relleno(rect_red(float(sx) - 3 * kz, float(sy) - 4 * kz, 6 * kz, 26 * kz, 2 * kz), tint((90, 90, 104)))
    lz.relleno(rect_red(float(sx) - 30 * kz * math.cos(a), float(sy) - 6 * kz - 8 * kz * math.sin(a), 60 * kz * math.cos(a), 4.6 * kz, 2 * kz), tint((176, 130, 90)))
    lz.relleno(circulo(float(sx) + 30 * kz * math.cos(a), float(sy) - 6 * kz - 8 * kz * math.sin(a) + 2 * kz, 4 * kz, 8), tint((120, 82, 62)))
    for j in range(3):
        lz.relleno(iso.pts([(x + 66, y + 10 + 9 * j, 0), (x + 82, y + 10 + 9 * j, 0), (x + 82, y + 17 + 9 * j, 0), (x + 66, y + 17 + 9 * j, 0)]), tint((250, 246, 234)), alfa=0.0)
    I.caja(lz, iso, x + 66, y + 10, 16, 26, 7, (252, 248, 236))
    I.caja(lz, iso, x + 66, y + 10, 16, 26, 2, (230, 220, 200), z0=7)


# ------------------------------------------------------------------------------------------------ campo de batalla de Calderón
class CampoCalderon:
    """Llanura con un río que cruza un puente de piedra (el de Calderón): al oeste el terreno donde se amontona la multitud insurgente, al este las lomas donde se forma el ejército realista; ríos, milpas y encinos."""
    PUENTE = (270, 196)

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -260, -140, 860, 480, color_top=(176, 192, 112), t=t, seed=141, esp=44)
        DC.parches(lz, iso, -260, -140, 860, 480, (176, 192, 112), n=30, var=24, seed=142, alfa=0.55, tam=(60, 120))
        DC.campos(lz, iso, -240, 260, 80, 460, nx=2, ny=2, seed=3, t=t)
        DC.campos(lz, iso, 440, -120, 800, 60, nx=3, ny=1, seed=9, t=t)
        I.camino(lz, iso, [(-260, 210), (60, 205), (270, 206), (480, 190), (860, 170)], 40, (222, 198, 150), borde=(196, 170, 126))
        # el río (agua con corriente) corre de norte a sur entre x=300 y x=346
        O.agua(lz, iso, [(300, -140), (346, -140), (350, 480), (296, 480)], t, seed=3)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.puente_piedra(m, 250, 188, largo=120, ancho=34, h=22, arcos=4)
            DC.bosque(m, -260, -140, 860, 480, n=60, seed=143, evitar=((-260, 150, 860, 270), (290, -140, 360, 480)), t_fn=lambda: self._t, tipos=("arbol", "arbol", "roca", "nopal"), min_d=30)
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m
