# -*- coding: utf-8 -*-
"""REPASO EXPRÉS + CIERRE.
repaso1: tres tarjetas AGUDA = ÚLTIMA, GRAVE = PENÚLTIMA, ESDRÚJULA = ANTEPENÚLTIMA (+ «¡SIEMPRE CON TILDE!»).
repaso2: ADVERBIOS (¿DÓNDE? ¿CUÁNDO? ¿CÓMO? ¿CUÁNTO? + SÍ · NO · QUIZÁ), AUTOBIOGRAFÍA = TODA TU VIDA CON «YO» (tira de película),
ANÉCDOTA = UN CLIP + 5 PREGUNTAS, CARTA = sopa L·S·A·D·F.
cierre: dos cuadernos HISTORIA y ESPAÑOL con sus trucos («HOY ME GUSTA IR» · «LA SOPA AGUADA DA FUERZA»), luna «ANTES DE DORMIR»;
papá crece al centro, corazones, «¡TÚ PUEDES, AMAYA!» y «¡MUCHO ÉXITO!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel
from iconos_ia import estrella, palomita
from personajes import AMARILLO, corazon, destello
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, entra, letrero, papa, tarjeta)
from piezas_es import ROSA_M, TURQ, sopa, tira
from piezas_fj import base, luna

T_INI = T0("repaso")
E, C = "repaso", "cierre"
tRep, tAg, tGr, tEs, tSiem = ww(E, 0, "repaso"), ww(E, 0, "agudas"), ww(E, 0, "graves"), ww(E, 0, "esdrujulas"), ww(E, 0, "siempre")
T_R2 = ww(E, 1, "adverbios") - 0.3
tAdv, tAuto, tAnec, tCarta = ww(E, 1, "adverbios"), ww(E, 1, "autobiografia"), ww(E, 1, "anecdota"), ww(E, 1, "carta")
T_C = T0(C)
tHist, tEsp, tHoy, tSopa, tDormir = ww(C, 0, "logro"), ww(C, 0, "cuaderno"), ww(C, 0, "olviden"), ww(C, 0, "sopa"), ww(C, 0, "dormir")
tGanas, tPuedes, tQuiero, tExito = ww(C, 1, "ganas"), ww(C, 1, "pueden"), ww(C, 1, "pueden") + 0.6, ww(C, 1, "exito")


def repaso1(t):
    im = cache("h_r1", lambda: papel("calido")).copy()
    letrero(im, "REPASO EXPRÉS", 760, 120, 70, t, col=AMARILLO, seed=18000, esc=entra(t, tRep - 0.3), rot=-0.02)
    for k, (a, b, col, tk) in enumerate((("AGUDA", "ÚLTIMA", rgb("f6a6a0"), tAg), ("GRAVE", "PENÚLTIMA", rgb("b8c7e8"), tGr),
                                         ("ESDRÚJULA", "ANTEPENÚLTIMA", rgb("a8d8b0"), tEs))):
        e = entra(t, tk - 0.25)
        if e <= 0.01:
            continue
        x = 330 + 430 * k
        tarjeta(im, x, 480, 390 * e, 360 * e, t, col, 18010 + k * 6, rot=(k - 1) * 0.025)
        rotulo(im, a, x, 400, (60 if k < 2 else 50) * e + 1, TINTA, t, seed=18011 + k * 6, tinta=False)
        rotulo(im, "=", x, 470, 40 * e + 1, GRIS, t, seed=18012 + k * 6, tinta=False)
        rotulo(im, b, x, 540, (44 if k < 2 else 34) * e + 1, ROJO, t, seed=18013 + k * 6, tinta=False)
    if t > tSiem - 0.3:
        letrero(im, "¡SIEMPRE CON TILDE!", 1190, 760, 50, t, col=rgb("fde0dc"), txt=ROJO, seed=18030, esc=entra(t, tSiem - 0.3), rot=0.04)
    return im


def repaso2(t):
    im = cache("h_r2", lambda: papel("frio")).copy()
    letrero(im, "REPASO EXPRÉS", 300, 90, 54, t, col=AMARILLO, seed=18100, esc=entra(t, T_R2), rot=-0.03)
    if t > tAdv - 0.3:
        e = entra(t, tAdv - 0.3)
        tarjeta(im, 420, 330, 700 * e, 330 * e, t, rgb("a8d8b0"), 18110, rot=-0.015)
        rotulo(im, "ADVERBIOS", 420, 215, 52 * e + 1, TINTA, t, seed=18111, tinta=False)
        rotulo(im, "¿DÓNDE? ¿CUÁNDO?", 420, 300, 40 * e + 1, MORADO, t, seed=18112, tinta=False)
        rotulo(im, "¿CÓMO? ¿CUÁNTO?", 420, 360, 40 * e + 1, MORADO, t, seed=18113, tinta=False)
        rotulo(im, "SÍ · NO · QUIZÁ", 420, 430, 40 * e + 1, ROJO, t, seed=18114, tinta=False)
    if t > tAuto - 0.3:
        e = entra(t, tAuto - 0.3)
        tarjeta(im, 1130, 330, 640 * e, 330 * e, t, rgb("f4d38a"), 18120, rot=0.015)
        rotulo(im, "AUTOBIOGRAFÍA", 1130, 215, 48 * e + 1, TINTA, t, seed=18121, tinta=False)
        tira(im, 1130, 320, 520 * e + 10, 100, t, n=5, seed=18122)
        rotulo(im, "TODA TU VIDA, CON «YO»", 1130, 430, 36 * e + 1, MORADO, t, seed=18123, tinta=False)
    if t > tAnec - 0.3:
        e = entra(t, tAnec - 0.3)
        tarjeta(im, 420, 760, 700 * e, 300 * e, t, rgb("d8b8e8"), 18130, rot=0.015)
        rotulo(im, "ANÉCDOTA", 420, 655, 52 * e + 1, TINTA, t, seed=18131, tinta=False)
        tira(im, 270, 770, 150 * e + 10, 100, t, n=1, seed=18132, avanza=False)
        rotulo(im, "UN CLIP", 520, 740, 44 * e + 1, ROJO, t, seed=18133, tinta=False)
        rotulo(im, "+ 5 PREGUNTAS", 520, 800, 36 * e + 1, MORADO, t, seed=18134, tinta=False)
    if t > tCarta - 0.3:
        e = entra(t, tCarta - 0.3)
        tarjeta(im, 1080, 760, 560 * e, 300 * e, t, rgb("f7c59f"), 18140, rot=-0.015)
        rotulo(im, "CARTA", 1080, 640, 52 * e + 1, TINTA, t, seed=18141, tinta=False)
        sopa(im, 1080, 870, 0.55 * e + 0.01, t, sale=pr(t, tCarta, tCarta + 1.2), seed=18142, vapor_=False)
    return im


def cuaderno(im, x, y, t, titulo, truco, col, e, seed, rot):
    if e <= 0.01:
        return
    tarjeta(im, x, y, 460 * e, 330 * e, t, col, seed, rot=rot)
    forma(im, rrect(x - 200 * e, y, 24 * e, 300 * e, 6), rgb("8f8f96"), t, seed + 1, tinta=2)
    rotulo(im, titulo, x + 10, y - 90 * e, 60 * e + 1, CREMA, t, seed=seed + 2, rot=rot)
    rotulo(im, truco, x + 10, y + 40 * e, 30 * e + 1, TINTA, t, seed=seed + 3, tinta=False, rot=rot)


def logro(im, x, y, t, l1, l2, col, e, seed, rot):
    """Aviso de «logro desbloqueado» de videojuego: placa oscura con trofeo dorado."""
    if e <= 0.01:
        return
    tarjeta(im, x, y, 470 * e, 260 * e, t, col, seed, rot=rot, tinta=5)
    forma(im, elipse(x - 150 * e, y, 55 * e, 55 * e), rgb("d9a93e"), t, seed + 1, tinta=3, luz=(rgb("fff2c0"), -10, -10, 0.5))
    rotulo(im, "★", x - 150 * e, y + 6 * e, 60 * e + 1, rgb("fff2c0"), t, seed=seed + 2, tinta=False)
    rotulo(im, l1, x + 60 * e, y - 40 * e, 50 * e + 1, rgb("f2c14e"), t, seed=seed + 3, rot=rot)
    rotulo(im, l2, x + 60 * e, y + 30 * e, 40 * e + 1, CREMA, t, seed=seed + 4, rot=rot)


def cierre(t):
    im = cache("h_ci", lambda: papel("rosa")).copy()
    ex = entra(t, tGanas - 0.4)
    fuera = 1 - suave(pr(t, tGanas - 0.6, tGanas))
    if fuera > 0.01:
        logro(im, 330, 330, t, "¡LOGRO", "DESBLOQUEADO!", rgb("2b2f45"), entra(t, tHist - 0.3) * fuera, 18200, -0.04)
        cuaderno(im, 840, 330, t, "ESPAÑOL", "LA SOPA AGUADA DA FUERZA", AZUL, entra(t, tEsp - 0.3) * fuera, 18210, 0.04)
        if t > tHoy - 0.2:
            palomita(im, 330, 520, 1.0 * entra(t, tHoy - 0.2) * fuera, t, seed=18220, col=VERDE)
        if t > tSopa - 0.2:
            palomita(im, 840, 520, 1.0 * entra(t, tSopa - 0.2) * fuera, t, seed=18221, col=VERDE)
        if t > tDormir - 0.4:
            ed = entra(t, tDormir - 0.4) * fuera
            luna(im, 560, 780, 90 * ed + 1, t, seed=18230)
            rotulo(im, "REPÁSALO ANTES DE DORMIR", 560, 940, 52 * ed + 1, MORADO, t, seed=18231)
    if tGanas - 0.3 < t < tPuedes - 0.4:
        eg = entra(t, tGanas - 0.3)
        rotulo(im, "¡ÉCHENLE", 560, 380, 110 * eg, VERDE, t, seed=18290, rot=-0.03)
        rotulo(im, "GANAS!", 560, 510, 130 * eg, ROSA_M, t, seed=18291, rot=-0.03)
    if ex > 0.01 and t >= tPuedes - 0.4:
        rotulo(im, "¡USTEDES PUEDEN,", 600, 330, 80 * entra(t, tPuedes - 0.4), ROJO, t, seed=18300, rot=-0.03)
        rotulo(im, "SEXTO B!", 560, 470, 150 * entra(t, tPuedes - 0.2), ROSA_M, t, seed=18301, rot=-0.03)
        if t > tQuiero - 0.3:
            for k in range(7):
                a = k / 7 * math.pi * 2 + t * 0.5
                corazon(im, 560 + 420 * math.cos(a), 420 + 230 * math.sin(a), 2.4 * entra(t, tQuiero - 0.3 + 0.08 * k), t,
                        seed=18310 + k)
        if t > tExito - 0.3:
            letrero(im, "¡MUCHO ÉXITO EN SU EXAMEN!", 560, 760, 56, t, col=AMARILLO, seed=18320, esc=entra(t, tExito - 0.3), rot=0.03)
            for k in range(5):
                estrella(im, 200 + 180 * k, 900 + 20 * math.sin(t * 4 + k), 26 * entra(t, tExito + 0.1 * k) + 1, t, AMARILLO,
                         seed=18330 + k)
    return im


TRAMOS = [(T_INI, repaso1), (T_R2, repaso2), (T_C, cierre)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    u = suave(pr(t, T_C, T_C + 1.2))           # en el cierre papá crece a la derecha
    papa(im, t, 1770 - 330 * u, H + 30, alto=330 + 430 * u)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
