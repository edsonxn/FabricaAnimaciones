# -*- coding: utf-8 -*-
"""PREGUNTA 5 + RESPUESTA 5 + REPASO EXPRÉS + CIERRE.
preg5: PAUSA, 1/2 + 1/3 = ? con pizzas chiquitas; cuenta 3-2-1.
resp5: 5/6 grande; la mariposa con 1/2 + 1/3: 1 x 3 = 3, 1 x 2 = 2, 3 + 2 = 5, abajo 2 x 3 = 6 → 5/6; «¡MUY BIEN!».
repaso1: DECIMALES (1-2-3 cifras = DÉCIMOS · CENTÉSIMOS · MILÉSIMOS) · NÚMEROS GRANDES (grupitos de 3 desde la derecha, MILLONES · MIL).
repaso2: TRIÁNGULOS (3 · 2 · 0 iguales) · PLANO (primero caminas, luego subes) · FRACCIONES (mismo tamaño o la mariposa).
cierre: «¡NIVEL COMPLETADO!» con los 5 temas palomeados, luna «REPÁSENLO ANTES DE DORMIR»; el profe crece, ¡ÉCHENLE GANAS!,
corazones, «¡USTEDES PUEDEN, SEXTO B!» y «¡MUCHO ÉXITO EN SU EXAMEN!»."""
import math

import numpy as np

from acuarela import H, TINTA, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, INI, T0, ww
from fondos_amaya import papel
from iconos_ia import estrella, palomita
from personajes import AMARILLO, corazon, destello, pregunta
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ
from piezas_fj import base, luna
from piezas_mt import AZUL_C, LILA_C, MIEL, ROSA_C, VERDE_C, digitos, fraccion, mariposa, pizza, triangulo

T_INI = T0("preg5")
P, R = "preg5", "resp5"
tP5, tMedio, tTercio, tCuanto, tFinP5 = ww(P, 0, "pausa"), ww(P, 0, "medio"), ww(P, 0, "tercio"), ww(P, 0, "cuanto"), FIN(P)
T_R5 = T0(R)
tCinco, tMari, tC1, tC2, tSuma, tAbajo, tSeis, tBien = (
    ww(R, 0, "cinco"), ww(R, 0, "mariposa"), ww(R, 0, "uno por"), ww(R, 0, "uno por", 1), ww(R, 0, "tres mas"), ww(R, 0, "abajo"),
    ww(R, 0, "seis"), ww(R, 0, "muy"))
E, C = "repaso", "cierre"
T_REP = T0(E)
tRep, tDec, tCif, tNum, tGrup, tMll = (ww(E, 0, "repaso"), ww(E, 0, "decimales"), ww(E, 0, "cifras"), ww(E, 0, "numeros"),
                                       ww(E, 0, "grupitos"), ww(E, 0, "millones"))
T_REP2 = INI(E, 1) - 0.3
tTri, tEqui, tIso, tEsc, tPlano, tCam, tFra, tMis, tMar = (
    ww(E, 1, "triangulos"), ww(E, 1, "equilatero"), ww(E, 1, "isosceles"), ww(E, 1, "escaleno"), ww(E, 1, "plano"),
    ww(E, 1, "primero"), ww(E, 1, "fracciones"), ww(E, 1, "mismo"), ww(E, 1, "mariposa"))
T_C = T0(C)
tNivel, tTodo, tCuad, tDormir = ww(C, 0, "nivel"), ww(C, 0, "todo"), ww(C, 0, "cuaderno"), ww(C, 0, "dormir")
tGanas, tPueden, tExito = ww(C, 1, "ganas"), ww(C, 1, "pueden"), ww(C, 1, "exito")


def preg5(t):
    im = cache("h_p5", lambda: papel("calido")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP5 - 0.3), t, seed=27000, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=27005, esc=entra(t, tP5 - 0.1))
    em, et = entra(t, tMedio - 0.3), entra(t, tTercio - 0.3)
    if em > 0.01:
        tarjeta(im, 700, 520, 980 * em, 320 * em, t, CREMA, 27010, rot=-0.015)
        pizza(im, 330, 520, 110, t, n=2, seed=27020, color_reb={0: rgb("f06aa0")}, esc=em)
        fraccion(im, 1, 2, 520, 520, 90, t, col=ROSA_M, seed=27030, esc=em)
    if et > 0.01:
        rotulo(im, "+", 640, 526, 90 * et + 1, ROJO, t, seed=27034)
        fraccion(im, 1, 3, 760, 520, 90, t, col=AZUL, seed=27036, esc=et)
        pizza(im, 950, 520, 110, t, n=3, seed=27040, color_reb={0: rgb("4f8fe0")}, esc=et)
    if t > tCuanto - 0.3:
        e = entra(t, tCuanto - 0.3)
        rotulo(im, "= ?", 1110, 526, 100 * e + 1, MORADO, t, seed=27050)
        letrero(im, "¿CUÁNTO NOS DA?", 700, 800, 58, t, col=AMARILLO, seed=27055, esc=e, rot=0.03)
        pregunta(im, 1240, 470, 1.3 * e + 0.01, t, seed=27058)
    cuenta(im, 1640, 250, t, tFinP5 + 0.15, T_R5 + 0.1, s=0.75, seed=27060)
    return im


def resp5(t):
    im = cache("h_r5", lambda: papel("calido")).copy()
    letrero(im, "RESPUESTA", 300, 110, 56, t, col=VERDE, txt=CREMA, seed=27100, esc=entra(t, T_R5), rot=-0.04)
    e = entra(t, tCinco - 0.3)
    tarjeta(im, 1300, 300, 330 * e + 1, 300 * e + 1, t, rgb("fff2c0"), 27110, rot=0.03)
    fraccion(im, 5, 6, 1300, 290, 100, t, col=VERDE, seed=27112, esc=e)
    rotulo(im, "CINCO SEXTOS", 1300, 500, 48 * e + 1, VERDE, t, seed=27116)
    chispas(im, 1300, 300, 220, t, tCinco, seed=27118, col=AMARILLO)
    mariposa(im, 560, 520, (1, 2), (1, 3), t, tMari, tC1, tC2, seed=27120, px=120, res=(5, 6), t_res=tSeis, t_abajo=tAbajo,
             abajo="2 x 3 = 6")
    if t > tSuma - 0.3:
        letrero(im, "3 + 2 = 5", 560, 250, 54, t, col=CREMA, txt=ROJO, seed=27160, esc=entra(t, tSuma - 0.3), rot=0.02)
    if t > tBien - 0.3:
        eb = entra(t, tBien - 0.3)
        letrero(im, "¡MUY BIEN!", 1300, 680, 60, t, col=AMARILLO, seed=27170, esc=eb, rot=-0.04)
        palomita(im, 1300, 820, 1.2 * eb, t, seed=27175, col=VERDE)
    return im


def tarjeta_tema(im, t, x, y, w, h, col, titulo, e, seed, rot=0.0):
    if e <= 0.01:
        return False
    tarjeta(im, x, y, w * e, h * e, t, col, seed, rot=rot)
    rotulo(im, titulo, x, y - h / 2 + 55, 50 * e + 1, TINTA, t, seed=seed + 1, tinta=False, rot=rot)
    return e > 0.6


def repaso1(t):
    im = cache("h_rp1", lambda: papel("frio")).copy()
    letrero(im, "REPASO EXPRÉS", 760, 100, 66, t, col=AMARILLO, seed=27200, esc=entra(t, tRep - 0.3), rot=-0.02)
    if tarjeta_tema(im, t, 400, 520, 640, 560, ROSA_C, "DECIMALES", entra(t, tDec - 0.3), 27210, rot=-0.015):
        xs = digitos(im, "0.008", 400, 420, 80, t, t_ap=tDec, seed=27215, paso=0.05)
        for k, (n, nom, col) in enumerate(((1, "DÉCIMOS", AZUL), (2, "CENTÉSIMOS", VERDE), (3, "MILÉSIMOS", MORADO))):
            ek = entra(t, tCif + 0.4 + 0.6 * k)
            if ek > 0.01:
                forma(im, elipse(xs[1 + n], 330, 22 * ek, 22 * ek), ROJO, t, 27220 + k, tinta=2)
                rotulo(im, str(n), xs[1 + n], 334, 30 * ek + 1, CREMA, t, seed=27223 + k, tinta=False)
                rotulo(im, f"{n} = {nom}", 400, 560 + 70 * k, 44 * ek + 1, col, t, seed=27226 + k, tinta=False)
    if tarjeta_tema(im, t, 1100, 520, 640, 560, AZUL_C, "NÚMEROS GRANDES", entra(t, tNum - 0.3), 27250, rot=0.015):
        from plano_c import colores_grupos
        txt = "25,980,634"
        digitos(im, txt, 1100, 430, 44, t, t_ap=tGrup - 0.3, seed=27255, paso=0.03,
                cols=colores_grupos(txt) if t > tGrup else None)
        if t > tGrup - 0.2:
            rotulo(im, "GRUPITOS DE 3", 1100, 560, 50 * entra(t, tGrup - 0.2) + 1, MORADO, t, seed=27270, tinta=False)
            rotulo(im, "DESDE LA DERECHA", 1100, 625, 40 * entra(t, tGrup) + 1, ROJO, t, seed=27271, tinta=False)
        if t > tMll - 0.3:
            letrero(im, "MILLONES · MIL", 1100, 730, 44, t, col=CREMA, txt=AZUL, seed=27275, esc=entra(t, tMll - 0.3), rot=-0.02)
    return im


def repaso2(t):
    im = cache("h_rp2", lambda: papel("rosa")).copy()
    letrero(im, "REPASO EXPRÉS", 300, 90, 52, t, col=AMARILLO, seed=27300, esc=entra(t, T_REP2), rot=-0.03)
    if tarjeta_tema(im, t, 290, 540, 470, 640, VERDE_C, "TRIÁNGULOS", entra(t, tTri - 0.3), 27310, rot=-0.015):
        for k, (tk, pts, marcas, nom, n) in enumerate((
                (tEqui, [(150, 400), (250, 400), (200, 313)], (1, 1, 1), "EQUILÁTERO", "3 IGUALES"),
                (tIso, [(165, 570), (235, 570), (200, 450)], (0, 1, 1), "ISÓSCELES", "2 IGUALES"),
                (tEsc, [(140, 730), (250, 730), (225, 640)], (1, 2, 3), "ESCALENO", "NINGUNO"))):
            ek = entra(t, tk - 0.3)
            if ek > 0.01:
                triangulo(im, pts, t, [ROSA_C, AZUL_C, MIEL][k], seed=27320 + k * 40, e=ek, marcas=marcas, s_m=0.9)
                rotulo(im, nom, 380, [370, 520, 690][k], 34 * ek + 1, TINTA, t, seed=27330 + k * 40, tinta=False)
                rotulo(im, n, 380, [415, 565, 735][k], 32 * ek + 1, ROJO, t, seed=27331 + k * 40, tinta=False)
    if tarjeta_tema(im, t, 780, 540, 470, 640, AZUL_C, "PLANO", entra(t, tPlano - 0.3), 27450, rot=0.015):
        x0, y0 = 650, 700
        for i in range(6):
            linea(im, [(x0 + 50 * i, y0), (x0 + 50 * i, y0 - 250)], 2, rgb("9ab6c8"), seed=27455 + i, t=t, alfa=0.8)
            linea(im, [(x0, y0 - 50 * i), (x0 + 250, y0 - 50 * i)], 2, rgb("9ab6c8"), seed=27462 + i, t=t, alfa=0.8)
        u = suave(pr(t, tCam - 0.2, tCam + 0.8))
        v = suave(pr(t, tCam + 0.8, tCam + 1.6))
        linea(im, [(x0, y0), (x0 + 150 * u + 1, y0)], 10, AZUL, seed=27470, t=t, punta=False)
        if v > 0:
            linea(im, [(x0 + 150, y0), (x0 + 150, y0 - 200 * v)], 10, ROJO, seed=27471, t=t, punta=False)
        rotulo(im, "1) CAMINAS", 780, 330, 40 * entra(t, tCam - 0.3) + 1, AZUL, t, seed=27475, tinta=False)
        rotulo(im, "2) SUBES", 780, 385, 40 * entra(t, tCam + 0.6) + 1, ROJO, t, seed=27476, tinta=False)
        rotulo(im, "( X , Y )", 780, 790, 50 * entra(t, tCam) + 1, MORADO, t, seed=27477)
    if tarjeta_tema(im, t, 1270, 540, 470, 640, MIEL, "FRACCIONES", entra(t, tFra - 0.3), 27500, rot=-0.015):
        em = entra(t, tMis - 0.3)
        pizza(im, 1270, 420, 110, t, n=12, seed=27510, esc=em, color_reb={0: rgb("f06aa0"), 1: rgb("f06aa0"), 2: rgb("4f8fe0")})
        if em > 0.01:
            rotulo(im, "MISMO TAMAÑO", 1270, 590, 40 * em + 1, ROJO, t, seed=27520, tinta=False)
        ep = entra(t, tMar - 0.3)
        if ep > 0.01:
            rotulo(im, "O LA MARIPOSA", 1270, 660, 40 * ep + 1, MORADO, t, seed=27525, tinta=False)
            for d, col in ((-1, ROSA_C), (1, LILA_C)):
                lavado(im, elipse(1270 + d * 50, 760, 46 * ep, 56 * ep, rot=d * 0.5), col, 0.6, 27530 + d, humedo=5)
            linea(im, [(1270, 720), (1270, 800)], 7, TINTA, seed=27533, t=t)
    return im


def logro(im, x, y, t, l1, l2, col, e, seed, rot):
    """Aviso de «logro desbloqueado» de videojuego: placa oscura con trofeo dorado."""
    if e <= 0.01:
        return
    tarjeta(im, x, y, 560 * e, 240 * e, t, col, seed, rot=rot, tinta=5)
    forma(im, elipse(x - 190 * e, y, 60 * e, 60 * e), rgb("d9a93e"), t, seed + 1, tinta=3, luz=(rgb("fff2c0"), -10, -10, 0.5))
    estrella(im, x - 190 * e, y, 34 * e + 1, t, rgb("fff2c0"), seed=seed + 2)
    rotulo(im, l1, x + 60 * e, y - 40 * e, 56 * e + 1, rgb("f2c14e"), t, seed=seed + 3, rot=rot)
    rotulo(im, l2, x + 60 * e, y + 34 * e, 46 * e + 1, CREMA, t, seed=seed + 4, rot=rot)


TEMAS = [("DECIMALES", ROSA_C), ("NÚMEROS", AZUL_C), ("TRIÁNGULOS", VERDE_C), ("PLANO", LILA_C), ("FRACCIONES", MIEL)]


def cierre(t):
    im = cache("h_ci", lambda: papel("rosa")).copy()
    fuera = 1 - suave(pr(t, tGanas - 0.6, tGanas))
    if fuera > 0.01:
        logro(im, 470, 210, t, "¡NIVEL", "COMPLETADO!", rgb("2b2f45"), entra(t, tNivel - 0.3) * fuera, 27600, -0.03)
        for k, (nom, col) in enumerate(TEMAS):
            ek = entra(t, tTodo - 0.3 + 0.18 * k) * fuera
            if ek <= 0.01:
                continue
            x, y = 200 + 260 * (k % 3) + (130 if k >= 3 else 0), 430 + 150 * (k // 3)
            tarjeta(im, x, y, 240 * ek, 110 * ek, t, col, 27610 + k * 5, rot=(k - 2) * 0.03)
            rotulo(im, nom, x, y + 4, (32 if len(nom) > 8 else 38) * ek + 1, TINTA, t, seed=27611 + k * 5, tinta=False)
            palomita(im, x + 100, y - 45, 0.8 * entra(t, tCuad - 0.2 + 0.12 * k) * fuera, t, seed=27613 + k * 5, col=VERDE)
        if t > tDormir - 0.6:
            ed = entra(t, tDormir - 0.6) * fuera
            luna(im, 250, 800, 70 * ed + 1, t, seed=27650)
            rotulo(im, "REPÁSENLO", 620, 770, 52 * ed + 1, MORADO, t, seed=27651)
            rotulo(im, "ANTES DE DORMIR", 620, 835, 46 * ed + 1, MORADO, t, seed=27652)
    if tGanas - 0.3 < t < tPueden - 0.4:
        eg = entra(t, tGanas - 0.3)
        rotulo(im, "¡ÉCHENLE", 560, 380, 110 * eg, VERDE, t, seed=27690, rot=-0.03)
        rotulo(im, "GANAS!", 560, 510, 130 * eg, ROSA_M, t, seed=27691, rot=-0.03)
    if t >= tPueden - 0.4:
        rotulo(im, "¡USTEDES PUEDEN,", 600, 330, 80 * entra(t, tPueden - 0.4), ROJO, t, seed=27700, rot=-0.03)
        rotulo(im, "SEXTO B!", 560, 470, 150 * entra(t, tPueden - 0.2), ROSA_M, t, seed=27701, rot=-0.03)
        for k in range(7):
            a = k / 7 * math.pi * 2 + t * 0.5
            corazon(im, 560 + 420 * math.cos(a), 420 + 230 * math.sin(a), 2.4 * entra(t, tPueden + 0.3 + 0.08 * k), t, seed=27710 + k)
        if t > tExito - 0.3:
            letrero(im, "¡MUCHO ÉXITO EN SU EXAMEN!", 560, 760, 56, t, col=AMARILLO, seed=27720, esc=entra(t, tExito - 0.3), rot=0.03)
            for k in range(5):
                estrella(im, 200 + 180 * k, 900 + 20 * math.sin(t * 4 + k), 26 * entra(t, tExito + 0.1 * k) + 1, t, AMARILLO,
                         seed=27730 + k)
    return im


TRAMOS = [(T_INI, preg5), (T_R5, resp5), (T_REP, repaso1), (T_REP2, repaso2), (T_C, cierre)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    u = suave(pr(t, T_C, T_C + 1.2))           # en el cierre el profe crece a la derecha
    papa(im, t, 1770 - 330 * u, H + 30, alto=330 + 430 * u)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
