# -*- coding: utf-8 -*-
"""PROBLEMAS CON FRACCIONES (la pizza del cuaderno) + LA MARIPOSA.
g0: «5. FRACCIONES» + FOTO REAL del problema de su cuaderno; la pizza entera = 1 ENTERO; Ana (rosa) 1/4, Luis (azul) 1/3.
g1: ¿QUÉ PARTE QUEDÓ? → una pizza en cuartos y otra en tercios: rebanadas de DISTINTO TAMAÑO → «¡ASÍ NO SE PUEDEN SUMAR!».
g2: rebanadas del MISMO TAMAÑO: 4 × 3 = 12 y la pizza se corta en 12.
g3: 1/4 = 3/12 (3 rebanadas rosas) · 1/3 = 4/12 (4 azules) → 3/12 + 4/12 = 7/12.
g4: 12/12 = 1 ENTERO; 12 − 7 = 5 → se comen 7 y QUEDAN 5/12; «los demás» llegan tarde corriendo.
g5: LA MARIPOSA 1/4 + 1/5: alas, 1×5 = 5, 1×4 = 4, 5 + 4 = 9, abajo 4×5 = 20 → 9/20 + el renglón REAL de su cuaderno."""
import math

import numpy as np

from acuarela import H, TINTA, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, INI, T0, ww
from fondos_amaya import papel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, gota, pregunta
from kit_amaya import (AZUL, CREMA, MORADO, ROJO, VERDE, cache, chispas, entra, gente, letrero, papa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from piezas_mt import AZUL_C, MIEL, ROSA_C, fraccion, mariposa, pizza
from utileria import flecha

T_INI = T0("fracciones")
F = "fracciones"
tUlt, tRico, tCuad, tPizza, tEntero, tAna, tCuarto, tLuis, tTercio = (
    ww(F, 0, "ultimo"), ww(F, 0, "rico"), ww(F, 0, "cuaderno"), ww(F, 0, "pizza"), ww(F, 0, "entero"), ww(F, 0, "ana"),
    ww(F, 0, "cuarto"), ww(F, 0, "luis"), ww(F, 0, "tercio"))
T_G1 = INI(F, 1) - 0.3
tQue, tCuartos, tTercios, tDist, tNoSe = ww(F, 1, "que"), ww(F, 1, "cuartos"), ww(F, 1, "tercios"), ww(F, 1, "distinto"), ww(F, 1, "no se")
T_G2 = INI(F, 2) - 0.3
tMismo, tMult, tCuatro, tDoce, tAhora, tDoceReb = (ww(F, 2, "mismo"), ww(F, 2, "multiplicamos"), ww(F, 2, "cuatro"), ww(F, 2, "doce"),
                                                    ww(F, 2, "ahora"), ww(F, 2, "doce", 1))
T_G3 = INI(F, 3) - 0.3
tTres3, tCuatro3, tSiete = ww(F, 3, "tres"), ww(F, 3, "cuatro"), ww(F, 3, "siete")
T_G4 = INI(F, 4) - 0.3
tDoceD, tMenos, tQuedaron, tCinco, tTarde = (ww(F, 4, "doce"), ww(F, 4, "menos"), ww(F, 4, "quedaron"), ww(F, 4, "cinco"),
                                             ww(F, 4, "llegaron"))
T_G5 = INI(F, 5) - 0.3
tMari, tUnoC, tUnoC2, tCincoMas, tAbajo, tRes = (ww(F, 5, "mariposa"), ww(F, 5, "uno por"), ww(F, 5, "uno por", 1),
                                                 ww(F, 5, "cinco mas"), ww(F, 5, "abajo"), ww(F, 5, "resultado"))

ROSA_P = rgb("f06aa0")
AZUL_P = rgb("4f8fe0")


def g0(t):
    im = cache("g_g0", lambda: papel("calido")).copy()
    letrero(im, "5. FRACCIONES", 300, 100, 56, t, col=MIEL, seed=26000, esc=entra(t, tUlt - 0.2), rot=-0.04)
    if t > tRico - 0.3:
        rotulo(im, "¡EL MÁS RICO!", 700, 105, 46 * entra(t, tRico - 0.3) + 1, ROJO, t, seed=26001, tinta=False)
    e = entra(t, tCuad - 0.4, 0.5)
    polaroid(im, "fra_hoja", 1140, 330, 0.72 * e, t, rot=0.02, seed=26010, alto=440)
    ep = entra(t, tPizza - 0.4, 0.5)
    pizza(im, 400, 540, 230, t, n=1, seed=26020, esc=ep)
    if t > tEntero - 0.3:
        letrero(im, "1 PIZZA = 1 ENTERO", 400, 850, 48, t, col=AMARILLO, seed=26030, esc=entra(t, tEntero - 0.3), rot=0.02)
    for k, (nom, tn, tf, col, d) in enumerate((("ANA", tAna, tCuarto, ROSA_P, 4), ("LUIS", tLuis, tTercio, AZUL_P, 3))):
        en = entra(t, tn - 0.3)
        if en <= 0.01:
            continue
        x = 900 + 340 * k
        gente(im, x, 670 - 6 * abs(math.sin(t * 6 + k)), 2.2 * en, t, seed=26040 + k, cara="normal", col=col)
        rotulo(im, nom, x, 885, 46 * en + 1, col, t, seed=26045 + k)
        fraccion(im, 1, d, x + 150, 720, 70, t, col=col, seed=26050 + k * 4, esc=entra(t, tf - 0.2))
    return im


def g1(t):
    im = cache("g_g1", lambda: papel("rosa")).copy()
    letrero(im, "¿QUÉ PARTE QUEDÓ?", 360, 100, 52, t, col=CREMA, txt=MORADO, seed=26100, esc=entra(t, tQue - 0.3), rot=-0.04)
    for k, (n, tk, col, txt, d) in enumerate(((4, tCuartos, ROSA_P, "CUARTOS", 4), (3, tTercios, AZUL_P, "TERCIOS", 3))):
        e = entra(t, tk - 0.4, 0.5)
        if e <= 0.01:
            continue
        x = 400 + 560 * k
        pizza(im, x, 480, 200, t, n=n, seed=26110 + k * 500, color_reb={0: col}, esc=e)
        rotulo(im, txt, x, 740, 56 * e + 1, col, t, seed=26115 + k)
        fraccion(im, 1, d, x + 250, 300, 60, t, col=col, seed=26120 + k * 4, esc=e)
    if t > tDist - 0.3:
        e = entra(t, tDist - 0.3)
        rotulo(im, "=", 680, 480, 110 * e + 1, MORADO, t, seed=26130)
        linea(im, [(650, 530), (710, 430)], 10, ROJO, seed=26131, t=t, alfa=e)
        letrero(im, "DISTINTO TAMAÑO", 680, 860, 48, t, col=AMARILLO, seed=26135, esc=e, rot=0.02)
    if t > tNoSe - 0.3:
        e = entra(t, tNoSe - 0.3)
        marca_x(im, 1340, 470, 1.4 * e, t, seed=26140)
        rotulo(im, "¡ASÍ NO SE", 1340, 650, 50 * e + 1, ROJO, t, seed=26141)
        rotulo(im, "PUEDEN SUMAR!", 1340, 710, 50 * e + 1, ROJO, t, seed=26142)
    return im


def g2(t):
    im = cache("g_g2", lambda: papel("frio")).copy()
    letrero(im, "REBANADAS DEL MISMO TAMAÑO", 560, 100, 50, t, col=AMARILLO, seed=26200, esc=entra(t, tMismo - 0.4), rot=-0.03)
    if t > tMult - 0.3:
        e = entra(t, tMult - 0.3)
        rotulo(im, "LOS DE ABAJO", 1150, 230, 44 * e + 1, MORADO, t, seed=26205, tinta=False)
        fraccion(im, 1, 4, 980, 420, 80, t, col=ROSA_M, seed=26210, esc=e)
        fraccion(im, 1, 3, 1300, 420, 80, t, col=AZUL, seed=26214, esc=e)
        for k, x in enumerate((980, 1300)):
            lavado(im, elipse(x, 476, 50 * e + 1, 46 * e + 1), AMARILLO, 0.45, 26218 + k, humedo=4)
    if t > tCuatro - 0.3:
        e = entra(t, tCuatro - 0.3)
        rotulo(im, "4 x 3", 1140, 640, 80 * e + 1, MORADO, t, seed=26220)
        if t > tDoce - 0.3:
            rotulo(im, "= 12", 1140, 750, 100 * entra(t, tDoce - 0.3) + 1, ROJO, t, seed=26221)
    uc = suave(pr(t, tAhora - 0.2, tDoceReb + 0.4))
    ep = entra(t, T_G2 + 0.2, 0.5)
    pizza(im, 470, 540, 260, t, n=12 if uc > 0 else 1, seed=26230, esc=ep, u_cortes=uc)
    if t > tDoceReb - 0.3:
        letrero(im, "¡12 REBANADAS!", 470, 880, 50, t, col=CREMA, txt=ROJO, seed=26240, esc=entra(t, tDoceReb - 0.3), rot=0.03)
    return im


def g3(t):
    im = cache("g_g3", lambda: papel("calido")).copy()
    reb = {}
    if t > tTres3 - 0.3:
        for i in range(3):
            if t > tTres3 - 0.3 + 0.2 * i:
                reb[i] = ROSA_P
    if t > tCuatro3 - 0.3:
        for i in range(4):
            if t > tCuatro3 - 0.3 + 0.2 * i:
                reb[3 + i] = AZUL_P
    pizza(im, 470, 500, 280, t, n=12, seed=26230, color_reb=reb)
    for k, (tk, a, b, col, y) in enumerate(((tTres3, (1, 4), (3, 12), ROSA_M, 260), (tCuatro3, (1, 3), (4, 12), AZUL, 500))):
        e = entra(t, tk - 0.3)
        if e <= 0.01:
            continue
        fraccion(im, *a, 980, y, 70, t, col=col, seed=26300 + k * 10, esc=e)
        rotulo(im, "=", 1090, y + 6, 70 * e + 1, MORADO, t, seed=26304 + k * 10)
        fraccion(im, *b, 1220, y, 70, t, col=col, seed=26306 + k * 10, esc=e)
        rotulo(im, ["ANA", "LUIS"][k], 1390, y, 44 * e + 1, col, t, seed=26309 + k * 10, tinta=False)
    if t > tSiete - 0.4:
        e = entra(t, tSiete - 0.4)
        tarjeta(im, 1150, 760, 560 * e + 1, 190 * e + 1, t, rgb("fff2c0"), 26330, rot=-0.02)
        rotulo(im, "COMIERON", 980, 765, 40 * e + 1, TINTA, t, seed=26331, tinta=False)
        fraccion(im, 7, 12, 1270, 760, 64, t, col=VERDE, seed=26332, esc=e)
        chispas(im, 1270, 760, 120, t, tSiete, seed=26336, col=AMARILLO)
    return im


def g4(t):
    im = cache("g_g4", lambda: papel("rosa")).copy()
    comidas = tuple(i for i in range(7) if t > tQuedaron - 0.4 + 0.1 * i)
    reb = {i: (ROSA_P if i < 3 else AZUL_P) for i in range(7) if i not in comidas}
    pizza(im, 470, 500, 280, t, n=12, seed=26230, color_reb=reb, comidas=comidas)
    if t > tDoceD - 0.3:
        e = entra(t, tDoceD - 0.3)
        fraccion(im, 12, 12, 960, 270, 64, t, col=MORADO, seed=26400, esc=e)
        rotulo(im, "= 1 ENTERO", 1180, 280, 52 * e + 1, MORADO, t, seed=26404)
    if t > tMenos - 0.4:
        rotulo(im, "12 - 7 = 5", 1100, 450, 80 * entra(t, tMenos - 0.4) + 1, ROJO, t, seed=26410)
    if t > tCinco - 0.3:
        e = entra(t, tCinco - 0.3)
        tarjeta(im, 1100, 630, 460 * e + 1, 190 * e + 1, t, rgb("fff2c0"), 26420, rot=0.02)
        rotulo(im, "QUEDAN", 980, 635, 44 * e + 1, TINTA, t, seed=26421, tinta=False)
        fraccion(im, 5, 12, 1220, 630, 64, t, col=VERDE, seed=26422, esc=e)
    if t > tTarde - 0.6:
        u = suave(pr(t, tTarde - 0.6, tTarde + 0.8))
        for k in range(3):
            x = 1620 - 520 * u + 110 * k
            gente(im, x, 800 - 10 * abs(math.sin(t * 12 + k)), 1.5, t, seed=26430 + k, cara="triste")
        if t > tTarde + 0.2:
            letrero(im, "¡LLEGARON TARDE!", 1100, 950, 46, t, col=CREMA, txt=ROJO, seed=26440, esc=entra(t, tTarde + 0.2), rot=-0.03)
            gota(im, 1180, 780, 1.0, t, seed=26445)
    return im


def g5(t):
    im = cache("g_g5", lambda: papel("frio")).copy()
    letrero(im, "TRUCO: LA MARIPOSA", 360, 100, 52, t, col=rgb("d8b8e8"), seed=26500, esc=entra(t, tMari - 0.4), rot=-0.04)
    mariposa(im, 600, 500, (1, 4), (1, 5), t, tMari, tUnoC, tUnoC2, seed=26510, px=125, res=(9, 20), t_res=tRes, t_abajo=tAbajo,
             abajo="4 x 5 = 20")
    if t > tCincoMas - 0.3:
        letrero(im, "5 + 4 = 9", 600, 220, 54, t, col=CREMA, txt=ROJO, seed=26560, esc=entra(t, tCincoMas - 0.3), rot=0.02)
    if t > tRes - 0.2:
        e = entra(t, tRes - 0.2, 0.5)
        polaroid(im, "suma_9_20", 1250, 760, 0.95 * e, t, rot=-0.02, seed=26570, alto=110)
        rotulo(im, "¡COMO EN SU CUADERNO!", 1250, 900, 40 * e + 1, TURQ, t, seed=26575, tinta=False)
    return im


TRAMOS = [(T_INI, g0), (T_G1, g1), (T_G2, g2), (T_G3, g3), (T_G4, g4), (T_G5, g5)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
