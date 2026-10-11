# -*- coding: utf-8 -*-
"""Escena 2 · el valle: el cañón en isométrico (altura, sierra de Morones, río Juchipila hacia el sur), viaje en el tiempo a los caxcanes en sus
terrazas al poniente, el tributo a Tlatlán (hoy Juchipila) y el nombre del lugar: agua + espuma."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_deco as DC
import kz_abstracto as AB
import plano as P
import paisajes as PA
import mundos_1 as M1
import mundos_2 as M2
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E2 = "valle"
CANON = M2.Canon()
t_estamos, t_suroeste, t_zac, t_fondo, t_canon, t_juch, t_mil, t_cinco, t_metros, t_altura = (
    T(E2, "estamos", frase=0), T(E2, "suroeste", frase=0), T(E2, "zacatecas", frase=0), T(E2, "fondo", frase=0), T(E2, "canon", frase=0),
    T(E2, "juchipila", frase=0), T(E2, "mil", frase=0), T(E2, "cinco", frase=0), T(E2, "metros", frase=0), T(E2, "altura", frase=0))
t_aqui, t_sierra, t_morones, t_rio, t_baja, t_sur, t_cerros = (T(E2, "aqui", frase=1), T(E2, "sierra", frase=1), T(E2, "morones", frase=1), T(E2, "rio", frase=1),
                                                                T(E2, "baja", frase=1), T(E2, "sur", frase=1), T(E2, "cerros", frase=1))
t_antes, t_esp, t_caxc, t_pueblo, t_nah = (T(E2, "antes", frase=2), T(E2, "espanoles", frase=2), T(E2, "caxcanes", frase=2), T(E2, "pueblo", frase=2),
                                           T(E2, "hablaba", frase=2))
t_vivian, t_laderas, t_poniente, t_hoy = T(E2, "vivian", frase=3), T(E2, "laderas", frase=3), T(E2, "poniente", frase=3), T(E2, "hoy", frase=3)
t_pagaban, t_tributo, t_senorio, t_tlatlan, t_conocemos, t_juch2 = (T(E2, "pagaban", frase=4), T(E2, "tributo", frase=4), T(E2, "senorio", frase=4),
                                                                    T(E2, "tlatlan", frase=4), T(E2, "conocemos", frase=4), T(E2, "juchipila", frase=4))
t_nombre, t_apozol, t_mezcla, t_agua, t_espuma = (T(E2, "nombre", frase=5), T(E2, "apozol", frase=5), T(E2, "mezcla", frase=5), T(E2, "agua", frase=5), T(E2, "espuma", frase=5))
T_A = T0(E2)
T_B = INI(E2, 1) - 0.12
T_C = INI(E2, 2) - 0.2
T_D = INI(E2, 4) - 0.2
T_E = INI(E2, 5) - 0.2


def _pie(lz, iso, x, y, z, texto, color, t, t0, t1, px=40, dy=-70, cola="abajo"):
    """Etiqueta con cola anclada a un punto del mundo isométrico."""
    k = U.pop(t, t0) * U.salida(t, t1)
    if k > 0.01:
        sx, sy = iso.P(x, y, z)
        U.llamada(lz, float(sx), float(sy) + dy, texto, color=color, px=px, k=k, cola=cola)


# ------------------------------------------------------------------------------------------------ A. el cañón y la altura
def cam_a(t):
    return K(t, [(T_A, (160, 180, 0, 0.66)), (t_fondo, (190, 190, 0, 0.74)), (T_B, (200, 200, 0, 0.82))])


@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.5))
def a_canon(lz, t):
    cx, cy, cz, zm = cam_a(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_A), 0.0, y0=330, capas=3, semilla=41)
    DC.aves(lz, t, n=6, seed=2)
    CANON.suelo(lz, iso, t)
    CANON.camino(lz, iso)
    m = CANON.objetos(t, "hoy")
    m.dibujar(lz, iso)
    k = U.pop(t, t_suroeste) * U.salida(t, t_canon - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "suroeste de Zacatecas", color=U.COL["morado"], px=54, k=k, cola=None)
    _pie(lz, iso, 330, 150, 0, "cañón de Juchipila", U.COL["teal"], t, t_canon, T_B - 0.2, px=46, dy=-260)
    # altímetro: sube hasta 1 265 m
    ka = U.pop(t, t_mil - 0.2) * U.salida(t, T_B - 0.15)
    if ka > 0.01:
        v = lerp(0, 1265, e_inout(prog(t, t_mil, t_cinco + 0.5)))
        x0, yb, yt = 1640, 900, 330
        lz.relleno(rect_red(x0 - 26, yt - 20, 52, yb - yt + 40, 26), (30, 14, 70), alfa=0.65 * ka, capa=2)
        yy = yb - (yb - yt) * v / 1400.0
        lz.relleno(rect_red(x0 - 14, yy, 28, yb - yy, 14), (255, 190, 60), alfa=ka, capa=2)
        lz.relleno(circulo(x0, yy, 22, 20), (255, 236, 150), alfa=ka, capa=2)
        U.llamada(lz, x0, yt - 70, "altura", color=U.COL["morado"], px=34, k=ka, cola=None)
        U.llamada(lz, x0 - 130, yy, f"{int(round(v)):,} m".replace(",", " "), color=U.COL["naranja"], px=48, k=ka, cola=None)
        U._registrar(lz, x0 - 130, yy, 260, 70)
    snd(t_suroeste, "pop", 0.4)
    snd(t_canon, "pop", 0.4)
    snd(t_mil, "subida", 0.4)


# ------------------------------------------------------------------------------------------------ B. la sierra y el río
def cam_b(t):
    return K(t, [(T_B, (200, 200, 0, 0.82)), (t_morones + 0.2, (-10, 150, 0, 0.9)), (t_rio, (330, 80, 0, 0.9)), (t_cerros + 0.2, (400, 360, 0, 0.9))])


@shot(T_B, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.5))
def b_sierra_rio(lz, t):
    cx, cy, cz, zm = cam_b(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_A), 0.0, y0=330, capas=3, semilla=41)
    DC.aves(lz, t, n=6, seed=2)
    CANON.suelo(lz, iso, t)
    CANON.camino(lz, iso)
    m = CANON.objetos(t, "hoy")
    m.dibujar(lz, iso)
    _pie(lz, iso, -80, 120, 214, "sierra de Morones", U.COL["morado"], t, t_sierra, t_rio - 0.2, px=50, dy=-40)
    _pie(lz, iso, 440, 20, 0, "río Juchipila", U.COL["azul"], t, t_rio, T_C - 0.3, px=50, dy=-70)
    # flechas de corriente sobre el río, de norte a sur (hacia la pantalla abajo-izquierda)
    ka = U.pop(t, t_baja) * U.salida(t, T_C - 0.3)
    if ka > 0.01:
        for i in range(4):
            u = ((t - t_baja) * 0.25 + i / 4.0) % 1.0
            y = -150 + 640 * u
            x = 440 + 14 * math.sin(u * 5)
            sx, sy = iso.P(x, y, 2)
            lz.relleno(np.array([(sx, sy + 22), (sx - 18, sy - 8), (sx + 18, sy - 8)]), (255, 255, 255), alfa=0.85 * ka * min(1, u * 6) * (1 - u), capa=2)
    k = U.pop(t, t_sur) * U.salida(t, T_C - 0.3)
    if k > 0.01:
        U.llamada(lz, 1640, 880, "hacia el sur", color=U.COL["azul"], px=52, k=k, cola=None)
    snd(t_sierra, "pop", 0.4)
    snd(t_rio, "chorro", 0.35)


# ------------------------------------------------------------------------------------------------ C. los caxcanes, en las laderas del poniente
def cam_c(t):
    return K(t, [(T_C, (110, 70, 0, 1.0)), (t_laderas, (10, 80, 0, 1.3)), (t_poniente - 0.3, (0, 90, 0, 1.4)), (INI(E2, 4) - 0.3, (30, 130, 0, 1.2))])


@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.8))
def c_caxcanes(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_C), 0.0, y0=330, capas=3, semilla=47)
    DC.aves(lz, t, n=5, seed=6)
    CANON.suelo(lz, iso, t)
    CANON.camino(lz, iso)
    modo = "caxcan"
    m = CANON.objetos(t, modo)
    m.dibujar(lz, iso)
    # el reloj retrocede: de 2026 a antes de los españoles
    yr = int(lerp(2026, 1500, e_inout(prog(t, T_C + 0.1, T_C + 1.9))))
    kc = U.pop(t, T_C + 0.1) * U.salida(t, t_caxc - 0.2)
    if kc > 0.01:
        AB.contador_atras(lz, W / 2, 190, yr, px=170, k=kc)
        U.llamada(lz, W / 2, 330, "antes de los españoles", color=U.COL["naranja"], px=46, k=U.pop(t, t_antes) * U.salida(t, t_caxc - 0.2), cola=None)
    _pie(lz, iso, -20, 40, 40, "los caxcanes", U.COL["morado"], t, t_caxc, t_laderas - 0.1, px=54, dy=-130)
    k = U.pop(t, t_nah) * U.salida(t, t_laderas - 0.1)
    if k > 0.01:
        U.llamada(lz, 1500, 250, "hablaban náhuatl", color=U.COL["teal"], px=48, k=k, cola=None)
    _pie(lz, iso, -90, 100, 30, "en las laderas", U.COL["teal"], t, t_laderas, t_poniente - 0.1, px=46, dy=-160)
    # el pueblo de hoy, en contorno; la flecha apunta al poniente
    _pie(lz, iso, 150, 120, 4, "hoy: Apozol", U.COL["oscuro"], t, t_hoy - 0.1, INI(E2, 4) - 0.3, px=44, dy=-60, cola="abajo")
    _pie(lz, iso, -90, 60, 70, "al poniente", U.COL["morado"], t, t_poniente, INI(E2, 4) - 0.3, px=52, dy=-110)
    snd(t_caxc, "pop", 0.4)
    snd(t_laderas, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ D. el tributo a Tlatlán
def cam_d(t):
    return K(t, [(T_D, (60, 120, 0, 0.8)), (t_tributo + 0.4, (170, 300, 0, 0.78)), (t_tlatlan + 0.2, (260, 520, 0, 0.9)), (T1(E2) - 7.0, (260, 560, 0, 0.95))])


@shot(T_D, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def d_tlatlan(lz, t):
    cx, cy, cz, zm = cam_d(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_D), 0.0, y0=330, capas=3, semilla=47)
    DC.aves(lz, t, n=5, seed=8)
    CANON.suelo(lz, iso, t)
    CANON.camino(lz, iso)
    m = CANON.objetos(t, "caxcan", ciudad=True, tributo=1.0)
    m.dibujar(lz, iso)
    _pie(lz, iso, 150, 300, 20, "tributo", U.COL["naranja"], t, t_tributo, t_senorio - 0.1, px=50, dy=-70)
    k = U.pop(t, t_senorio) * U.salida(t, t_tlatlan - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "señorío de Tlatlán", color=U.COL["morado"], px=58, k=k, cola=None)
    _pie(lz, iso, 215, 575, 84, "Tlatlán", U.COL["morado"], t, t_tlatlan, t_conocemos, px=54, dy=-120)
    kj = U.pop(t, t_conocemos)
    if kj > 0.01:
        sx, sy = iso.P(215, 575, 84)
        U.llamada(lz, float(sx), float(sy) - 120, "hoy: Juchipila", color=U.COL["naranja"], px=54, k=kj, cola="abajo")
    snd(t_tributo, "pop", 0.35)
    snd(t_tlatlan, "gong", 0.4)
    snd(t_conocemos, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ E. el nombre: agua + espuma
def _rapidos(lz, t):
    # roca grande y escalones del río con espuma
    lz.halo(1500, 180, 320, (255, 236, 190), alfa=0.35, dureza=1.1, capa=0)
    PA.sierras(lz, t, 10 * (t - T_E), 0.0, y0=560, capas=3, semilla=53, verde=0.8)
    # agua que cae por escalones
    for j, (y0, c0, c1) in enumerate(((560, (130, 214, 244), (60, 160, 232)), (700, (96, 188, 240), (40, 124, 216)), (850, (70, 160, 232), (26, 90, 190)))):
        x0 = -40 + 0 * j
        pts = [(x, y0 + 6 * math.sin(x * 0.012 + t * (1.2 + 0.2 * j) + j)) for x in np.linspace(-60, W + 60, 34)]
        lz.degradado(np.array(pts + [(W + 60, H + 20), (-60, H + 20)]), c0, c1, (0, y0), (0, H), capa=1)
        for q in range(30):
            u = (h01(60 + j, q, 1) + t * (0.03 + 0.012 * j)) % 1.0
            x = -40 + (W + 80) * u
            yc = y0 + 6 * math.sin(x * 0.012 + t * (1.2 + 0.2 * j) + j)
            r = 9 + 16 * h01(60 + j, q, 2)
            lz.relleno(circulo(x, yc - r * 0.2, r, 14), (244, 252, 255), alfa=0.95, capa=2)
            lz.relleno(circulo(x - r * 0.3, yc - r * 0.5, r * 0.32, 10), (255, 255, 255), alfa=0.9, capa=2)
    for (x, y, s) in ((300, 840, 1.0), (1080, 930, 1.3), (1690, 800, 0.9)):         # rocas que parten el agua
        lz.relleno(elipse(x, y + 18 * s, 120 * s, 26 * s, 0, 28), (30, 60, 120), alfa=0.35, capa=1)
        lz.relleno(np.array([(x - 110 * s, y + 10 * s), (x - 70 * s, y - 56 * s), (x + 10 * s, y - 80 * s), (x + 84 * s, y - 40 * s), (x + 118 * s, y + 10 * s)]), (118, 100, 124), capa=1)
        lz.relleno(np.array([(x + 10 * s, y - 80 * s), (x + 84 * s, y - 40 * s), (x + 118 * s, y + 10 * s), (x + 30 * s, y + 10 * s)]), (86, 70, 100), capa=1)
        M1.espuma(lz, x, y + 12 * s, 240 * s, t, k=1.0, n=18, seed=int(x) % 17, capa=2)


@shot(T_E, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def e_nombre(lz, t):
    _rapidos(lz, t)
    a = U.pop(t, t_apozol - 0.1)
    AB.titulo_textura(lz, "APOZOL", W / 2, 190, 170, t, paleta=((40, 110, 230), (30, 170, 170), (110, 226, 236), (240, 130, 36), (255, 204, 70)), k=1.0, alfa=min(1.0, a * 1.5))
    k = U.pop(t, t_nombre)
    if k > 0.01:
        U.llamada(lz, W / 2, 340, "un nombre en náhuatl", color=U.COL["morado"], px=42, k=k * U.salida(t, t_mezcla - 0.1), cola=None)
    ka = pk(t, t_agua - 0.15, 0.5)
    if ka > 0.01:
        M1.gota(lz, 600, 560, 70, t, k=ka)
        U.llamada(lz, 600, 700, "atl = agua", color=U.COL["azul"], px=54, k=ka, cola=None)
    ke = pk(t, t_espuma - 0.15, 0.5)
    if ke > 0.01:
        M1.espuma(lz, 1320, 640, 200, t, k=ke * 1.3, n=14, seed=8, capa=2)
        U.llamada(lz, 1320, 700, "pozolli = espuma", color=U.COL["teal"], px=54, k=ke, cola=None)
    kp = U.pop(t, t_agua + 0.2)
    if kp > 0.01:
        P.rotulo(lz, 960, 600, "+", px=150, k=kp, color=(255, 255, 255), alfa=min(1.0, kp * 1.5))
    snd(t_apozol, "pop", 0.45)
    snd(t_agua, "gota", 0.4)
    snd(t_espuma, "burbujas", 0.4)
