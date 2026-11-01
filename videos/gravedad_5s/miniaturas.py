# -*- coding: utf-8 -*-
"""Miniaturas (python fab.py gravedad_5s miniatura). Kuriox = por código, estilo Kurzgesagt:
formas grandes y limpias, planeta Tierra + objetos flotando / grietas de lava, 2 palabras enormes amarillas y Kuri."""
import math

import numpy as np

import fondos as F
import plano as P
from motor import NEGRO, circulo, rect_red
import kit_grav as KG
import ui_base as UB
import gente as G

T = 0.37
WOB = 0.0
AMARILLO = (255, 214, 64)


FUENTE = "geo_x"


ESCALA_TXT = {"mini_luckiest": 1.3, "mini_impact": 1.45, "mini_gotham": 1.05}


def _texto(lz, s, x, y, px, rot=-0.03, color=AMARILLO):
    if FUENTE != "geo_x":     # rótulo de miniatura: más grande, contorno grueso y sombra 3D desplazada
        px *= ESCALA_TXT.get(FUENTE, 1.0)
        for k in range(1, 4):
            lz.texto(s, x + 5 * k, y + 6 * k, px, FUENTE, color=(14, 8, 30), borde=(14, 8, 30), borde_px=px * 0.13,
                     rot=rot, capa=2, temblor=0.0)
        lz.texto(s, x, y, px, FUENTE, color=color, borde=NEGRO, borde_px=px * 0.13, rot=rot, capa=2, temblor=0.0)
        return
    lz.texto(s, x, y, px, FUENTE, color=color, borde=NEGRO, borde_px=px * 0.11, rot=rot, capa=2, temblor=0.0)


def _kuri_casco(lz, x, y, s, rot=-0.22):
    with lz.capa(2):
        with lz.grupo(x, y, s, rot):
            P.kuri(lz, 0, 70, 1.0, T, mirar=(-1.0, -0.3), aleteo=1.0, boca=1.0)
            lz.relleno(circulo(0, -5, 110, 60), (200, 230, 255), alfa=0.18)
            lz.relleno(P.borde_luz(0, -5, 110, -math.pi * 0.75, 0.07), (255, 255, 255), alfa=0.5)


def tierra(lz):
    """La Tierra perdiendo gravedad: coches, burbujas de océano y flechas radiales saliendo al espacio; Kuri flotando."""
    x, y, r = 510, 560, 355
    P.tierra(lz, x, y, r, T, rot=1.85, ang_luz=math.pi * 1.15)
    # Flechas radiales hacia afuera
    for ang in (-1.35, -0.65, 0.35, 1.15, 2.25, -2.35):
        p0 = (x + (r + 18) * math.cos(ang), y + (r + 18) * math.sin(ang))
        p1 = (x + (r + 120) * math.cos(ang), y + (r + 120) * math.sin(ang))
        UB.flecha(lz, p0, p1, col=(118, 226, 255), ancho=10.0, punta=30.0)
    # Burbujas gigantes de océano, coche y taza flotando fuera del planeta
    KG.burbuja_agua(lz, 200, 240, 74, T, seed=1)
    KG.burbuja_agua(lz, 690, 145, 56, T, seed=2)
    KG.burbuja_agua(lz, 920, 785, 68, T, seed=3)
    with lz.grupo(185, 760, 1.18, -0.45):
        KG.coche_urbano(lz, 0, 0, 1.0, T, col=(238, 84, 96))
    with lz.grupo(950, 560, 1.45, 0.32):
        KG.taza_cafe(lz, 0, 0, 1.0, T, ingravidez=1.0)
    _kuri_casco(lz, 1545, 795, 1.75, rot=-0.25)
    _texto(lz, "SIN GRAVEDAD", 1390, 225, 124)
    _texto(lz, "5 SEGUNDOS", 1390, 405, 114, color=(255, 120, 120))
    return F.espacio(T)


def _estela(lz, x, y, ang, largo, col=(160, 230, 255)):
    """Tres rayas de movimiento detrás de un objeto que sale disparado en dirección `ang`."""
    for k, d in enumerate((-26, 0, 26)):
        ox, oy = -math.sin(ang) * d, math.cos(ang) * d
        l = largo * (0.7 if k != 1 else 1.0)
        p0 = (x + ox - math.cos(ang) * (60 + l), y + oy - math.sin(ang) * (60 + l))
        p1 = (x + ox - math.cos(ang) * 60, y + oy - math.sin(ang) * 60)
        UB.flecha(lz, p0, p1, col=col, ancho=9.0, punta=0.0, alfa=0.75)


def flotan(lz):
    """Horizonte de la Tierra enorme abajo y todo saliendo disparado hacia el espacio: coche, perro, bici, taza y
    burbujas de océano a tamaño grande; Kuri asustado arriba a la derecha y dos palabras gigantes a la izquierda."""
    P.tierra(lz, 960, 1820, 1180, T, rot=1.2, ang_luz=math.pi * 1.25)
    objetos = [
        (300, 500, -1.95, 1.9, lambda: KG.coche_urbano(lz, 0, 0, 1.0, T, col=(238, 84, 96))),
        (780, 590, -1.55, 2.3, lambda: G.perro_parque(lz, 0, 0, 1.0, T, flotando=1.0)),
        (1170, 560, -1.2, 1.6, lambda: KG.bicicleta(lz, 0, 0, 1.0, T, giro=1.0)),
        (560, 650, -1.7, 2.8, lambda: KG.taza_cafe(lz, 0, 0, 1.0, T, ingravidez=1.0)),
    ]
    for i, (x, y, ang, s, dib) in enumerate(objetos):
        _estela(lz, x, y + 40, ang, 90)
        with lz.grupo(x, y, s, 0.35 * (-1) ** i):
            dib()
    KG.burbuja_agua(lz, 120, 820, 82, T, seed=1)
    KG.burbuja_agua(lz, 1000, 830, 64, T, seed=2)
    KG.burbuja_agua(lz, 1400, 880, 96, T, seed=3)
    _kuri_casco(lz, 1610, 640, 2.1, rot=0.3)
    _texto(lz, "5 SEGUNDOS", 560 if FUENTE == "geo_x" else 565, 135 if FUENTE == "geo_x" else 150, 140, rot=-0.035)
    _texto(lz, "SIN GRAVEDAD", 1360 if FUENTE == "geo_x" else 1300, 300 if FUENTE == "geo_x" else 340, 128, rot=0.03, color=(255, 120, 120))
    return F.espacio(T)


def _con_fuente(nombre):
    def fn(lz):
        global FUENTE
        FUENTE = nombre
        try:
            return flotan(lz)
        finally:
            FUENTE = "geo_x"
    return fn


VARIANTES = {"tierra": tierra, "flotan": flotan, "luckiest": _con_fuente("mini_luckiest"),
             "gotham": _con_fuente("mini_gotham"), "impact": _con_fuente("mini_impact")}
