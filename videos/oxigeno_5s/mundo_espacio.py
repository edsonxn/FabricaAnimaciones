# -*- coding: utf-8 -*-
"""La Tierra vista desde el espacio: intro y reglas del juego (el O2 del aire como puntos rojos en la atmósfera que se
apagan), final de la versión B (destellos por todo el planeta) y «realidad» (la Tierra antigua sin oxígeno, las
cianobacterias y el fitoplancton). Kuri flota a su lado con escafandra."""
import math

import numpy as np

import fondos as F
import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from mundo_comun import pop, ventana, campana, kf
from anclas import A, Z1, Z2, Z3, Z4
import kit_oxi as KO

ROT0 = 1.9          # giro de la Tierra (deja América a la vista)


def fondo(t, ex=960.0, ey=560.0):
    return F.espacio(t, brillo_est=1.0, dx=-(ex - 960) * 0.05, dy=-(ey - 560) * 0.05)


def antigua(t):
    """0..1: la Tierra de hace 2 400 millones de años (sin oxígeno) durante «realidad»."""
    return ventana(t, A.millones_r - 0.6, A.bacterias + 0.4, 0.8, 2.4)


def puntos_o2(lz, t, x, y, r, alfa):
    """Moléculas de O2 de la atmósfera: anillo de puntitos rojos alrededor del planeta."""
    if alfa <= 0.01:
        return
    for i in range(90):
        a = i / 90 * 2 * math.pi + 0.02 * math.sin(t + i)
        rr = r * (1.03 + 0.09 * h01(i, 2) + 0.01 * math.sin(t * 2 + i))
        px, py = x + rr * math.cos(a), y + rr * math.sin(a)
        lz.relleno(circulo(px, py, max(1.5, r * 0.012), 10), (255, 96, 110), alfa=alfa * (0.6 + 0.4 * h01(i, 4)))


def tierra(lz, t, x, y, r, extra=True):
    ant = antigua(t)
    rot = ROT0 + t * 0.035
    P.tierra(lz, x, y, r, t, rot=rot, ang_luz=math.pi * 1.15, luz=1.0, nubes=1.0 - 0.6 * ant, atmosfera=1.0 - 0.3 * ant)
    if ant > 0.01:   # sin oxígeno: cielo anaranjado de metano, océanos verdosos
        lz.relleno(circulo(x, y, r, 140), (210, 130, 70), alfa=0.45 * ant)
        lz.halo(x, y, r * 1.3, (255, 150, 80), alfa=0.5 * ant, r0=0.75)
    if not extra:
        return
    # O2 del aire en la intro (se apaga cuando «desaparece»)
    a_o2 = 0.0
    if t < Z2[0] + 0.5:
        a_o2 = ventana(t, Z1[1] - 0.6, A.desaparece, 0.5, 0.2) + ventana(t, A.deja - 0.2, A.vuelve_r - 0.2, 0.2, 0.1) * 0.0
        a_o2 = max(a_o2, ventana(t, A.vuelve_r, Z2[0], 0.3, 0.4))
    if a_o2 > 0.01:
        puntos_o2(lz, t, x, y, r, a_o2)
    if Z1[1] - 0.2 < t < A.desaparece + 1.0:
        u = prog(t, A.desaparece - 0.05, A.desaparece + 0.8)
        if 0 < u < 1:
            for i in range(30):
                a = i / 30 * 2 * math.pi
                rr = r * (1.06 + 0.25 * u)
                lz.relleno(circulo(x + rr * math.cos(a), y + rr * math.sin(a), r * 0.02 * (1 - u), 10), (255, 140, 150),
                           alfa=1 - u)
    # versión B: destellos de hidrógeno ardiendo por todo el planeta
    fb = ventana(t, Z3[0], A.suerte - 0.4, 0.4, 1.2)
    if fb > 0.01:
        for i in range(22):
            ph = (t * 0.9 + h01(i, 3)) % 1
            a = h01(i, 1) * 2 * math.pi
            d = r * 0.9 * math.sqrt(h01(i, 2))
            px, py = x + d * math.cos(a), y + d * math.sin(a)
            lz.halo(px, py, r * (0.1 + 0.25 * ph), (255, 190, 110), alfa=fb * math.sin(ph * math.pi) * 0.9)
        lz.halo(x, y, r * 1.5, (255, 150, 90), alfa=0.35 * fb, r0=0.7)


def kuri_espacio(lz, t, x, y, s, mirar=(0.0, 0.0), feliz=0.0, aleteo=0.0, alfa=1.0):
    """Kuri flotando con escafandra de cristal."""
    if alfa <= 0.01:
        return
    bob = 10 * math.sin(t * 1.4)
    rot = 0.08 * math.sin(t * 0.9)
    with lz.grupo(x, y + bob, s, rot):
        P.kuri(lz, 0, 70, 1.0, t, mirar=mirar, feliz=feliz, aleteo=aleteo)
        lz.relleno(circulo(0, -5, 110, 60), (200, 230, 255), alfa=0.18)
        lz.relleno(P.borde_luz(0, -5, 110, -math.pi * 0.75, 0.07), (255, 255, 255), alfa=0.5)
        lz.relleno(rect_red(-50, 72, 100, 22, 10), (200, 206, 230))


def dibujar(lz, t, x, y, r):
    tierra(lz, t, x, y, r)
