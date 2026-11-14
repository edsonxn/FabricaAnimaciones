# -*- coding: utf-8 -*-
"""CARTA INFORMAL + PREGUNTA 4 + RESPUESTA 4.
carta: «LA CARTA INFORMAL», la FOTO REAL de su página y tres personitas de confianza (AMIGA, ABUELA, PRIMA) → la hoja de carta se
arma de arriba a abajo mientras la voz nombra cada parte (Juchipila, 7 de nov. · «Querida Amaya:» · renglones del asunto · «Con
cariño,» · firma de Papá) con la lista 1-5 a la derecha · sopa: plato de sopa del que suben L·S·A·D·F; «LA SOPA AGUADA DA FUERZA»
palabra por palabra y debajo LUGAR · SALUDO · ASUNTO · DESPEDIDA · FIRMA · preg4: carta vacía con cinco «?» y cuenta 3-2-1 ·
resp4: la carta se vuelve a armar parte por parte, la sopa con sus letras, «¡MUY BIEN!» y palomita."""
import math

import numpy as np

from acuarela import H, W, TINTA, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from fondos_amaya import papel
from iconos_ia import palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, gente, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, carta, polaroid, sopa
from piezas_fj import base

T_INI = T0("carta")
C, P, R = "carta", "preg4", "resp4"
tCarta, tConf = ww(C, 0, "carta"), ww(C, 0, "confianza")
GENTE = [("AMIGO", ww(C, 0, "amigo"), rgb("e35d4a")), ("ABUELA", ww(C, 0, "abuela"), rgb("9b6ad1")), ("PRIMA", ww(C, 0, "prima"), AZUL)]
tCinco, tArriba = ww(C, 1, "cinco"), ww(C, 1, "arriba")
PARTES = [("LUGAR Y FECHA", ww(C, 1, "lugar")), ("SALUDO", ww(C, 1, "saludo")), ("ASUNTO (CUERPO)", ww(C, 2, "asunto")),
          ("DESPEDIDA", ww(C, 2, "despedida")), ("FIRMA", ww(C, 2, "firma"))]
T_SOPA = ww(C, 3, "truco") - 0.3
FRASE = [("LA", ww(C, 3, "la", 1)), ("SOPA", ww(C, 3, "sopa")), ("AGUADA", ww(C, 3, "aguada")), ("DA", ww(C, 3, "da")),
         ("FUERZA", ww(C, 3, "fuerza"))]
NOMS = [("LUGAR", ww(C, 3, "lugar")), ("SALUDO", ww(C, 3, "saludo")), ("ASUNTO", ww(C, 3, "asunto")),
        ("DESPEDIDA", ww(C, 3, "despedida")), ("FIRMA", ww(C, 3, "firma"))]
T_P4 = T0(P)
tP4, tCinco4, tFinP4 = ww(P, 0, "pausa"), ww(P, 0, "cinco"), FIN(P)
T_R4 = T0(R)
R_PARTES = [ww(R, 0, w) for w in ("lugar", "saludo", "asunto", "despedida", "firma")]
R_FRASE = [ww(R, 0, "la"), ww(R, 0, "sopa"), ww(R, 0, "aguada"), ww(R, 0, "da"), ww(R, 0, "fuerza")]
tMuy = ww(R, 0, "muy")
COLS = [rgb("f6a6a0"), rgb("b8c7e8"), rgb("a8d8b0"), rgb("f4d38a"), rgb("d8b8e8")]


def lista(im, t, tiempos, x=1130, y0=230, paso=125, seed=0):
    for k, ((txt, _), tk) in enumerate(zip(PARTES, tiempos)):
        e = entra(t, tk - 0.2)
        if e <= 0.01:
            continue
        y = y0 + paso * k
        tarjeta(im, x, y, 560 * e, 100 * e, t, COLS[k], seed + k * 5, rot=(k - 2) * 0.012)
        rotulo(im, f"{k + 1}. {txt}", x, y + 4, 44 * e + 1, TINTA, t, seed=seed + 1 + k * 5, tinta=False)
        if k > 0 and e > 0.5:
            linea(im, [(x - 340, y - paso + 30), (x - 340, y - 30)], 4, GRIS, seed=seed + 3 + k * 5, t=t)


def carta_sc(t):
    im = cache("g_ca", lambda: papel("calido")).copy()
    letrero(im, "LA CARTA INFORMAL", 420, 110, 60, t, col=AMARILLO, seed=17000, esc=entra(t, tCarta - 0.3), rot=-0.03)
    if t < tCinco - 0.3:
        polaroid(im, "carta", 1200, 450, 0.85 * entra(t, tCarta - 0.2), t, rot=0.05, seed=17005)
        if t > tConf - 0.3:
            rotulo(im, "A ALGUIEN DE CONFIANZA", 480, 330, 50 * entra(t, tConf - 0.3) + 1, MORADO, t, seed=17010, tinta=False)
        for k, (nom, tk, col) in enumerate(GENTE):
            e = entra(t, tk - 0.2)
            if e > 0.01:
                gente(im, 220 + 250 * k, 580, 3.0 * e + 0.01, t, seed=17020 + k, cara="normal", col=col)
                letrero(im, nom, 220 + 250 * k, 800, 40, t, col=CREMA, txt=col, seed=17025 + k * 3, esc=e, rot=(k - 1) * 0.04)
        return im
    u = [suave(pr(t, tk - 0.2, tk + 0.8)) for _, tk in PARTES]
    carta(im, 470, 560, 0.95 * entra(t, tCinco - 0.3), t, u, seed=17040)
    lista(im, t, [tk for _, tk in PARTES], seed=17060)
    if t > tArriba - 0.2 and t < PARTES[0][1] - 0.2:
        rotulo(im, "DE ARRIBA A ABAJO ↓", 1130, 500, 54, MORADO, t, seed=17090, esc=entra(t, tArriba - 0.2), tinta=False)
    return im


def sopa_sc(t):
    im = cache("g_so", lambda: papel("rosa")).copy()
    letrero(im, "TRUCO", 300, 110, 56, t, col=AMARILLO, seed=17100, esc=entra(t, T_SOPA + 0.2), rot=-0.04)
    sale = pr(t, FRASE[0][1] - 0.2, FRASE[-1][1] + 0.3)
    sopa(im, 760, 760, 1.15, t, sale=sale, seed=17110)
    x = 180
    for k, (w_, tk) in enumerate(FRASE):
        e = entra(t, tk - 0.15)
        wd = len(w_) * 74 * 0.6 + 40
        if e > 0.01:
            rotulo(im, w_, x + wd / 2, 240, 74 * e + 1, [ROJO, rgb("e08a1e"), VERDE, AZUL, MORADO][k], t, seed=17120 + k)
        x += wd + 20
    for k, (w_, tk) in enumerate(NOMS):
        e = entra(t, tk - 0.2)
        if e > 0.01:
            xx = 760 + (k - 2) * 105 * 1.15
            rotulo(im, w_, xx, 410 + 46 * (k % 2), 34 * e + 1, TINTA, t, seed=17130 + k, tinta=False)
    return im


def preg4(t):
    im = cache("g_p4", lambda: papel("frio")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP4 - 0.3), t, seed=17200, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=17205, esc=entra(t, tP4 - 0.1))
    if t > tCinco4 - 0.4:
        e = entra(t, tCinco4 - 0.4)
        carta(im, 560, 640, 0.7 * e, t, [0, 0, 0, 0, 0], seed=17210, rot=-0.02)
        for k in range(5):
            pregunta(im, 560, 420 + 105 * k, 0.9 * entra(t, tCinco4 + 0.1 * k) + 0.01, t, seed=17220 + k)
        letrero(im, "¿LAS 5 PARTES?", 1150, 560, 58, t, col=AMARILLO, seed=17230, esc=e, rot=0.03)
    cuenta(im, 1640, 250, t, tFinP4 + 0.15, T_R4 + 0.1, s=0.75, seed=17240)
    return im


def resp4(t):
    im = cache("g_r4", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 300, 120, 56, t, col=VERDE, txt=CREMA, seed=17300, esc=entra(t, T_R4), rot=-0.04)
    u = [suave(pr(t, tk - 0.2, tk + 0.5)) for tk in R_PARTES]
    carta(im, 430, 600, 0.8, t, u, seed=17310)
    lista(im, t, R_PARTES, x=1050, y0=250, paso=100, seed=17330)
    if t > R_FRASE[0] - 0.3:
        e = entra(t, R_FRASE[0] - 0.3)
        rotulo(im, "LA SOPA AGUADA DA FUERZA", 1090, 830, 50 * e + 1, rgb("e08a1e"), t, seed=17360, rot=-0.02)
    if t > tMuy - 0.3:
        rotulo(im, "¡MUY BIEN!", 1000, 960, 90, VERDE, t, seed=17370, esc=entra(t, tMuy - 0.3), rot=-0.03)
        palomita(im, 1400, 950, 1.2 * entra(t, tMuy), t, seed=17375, col=VERDE)
        chispas(im, 1000, 940, 260, t, tMuy, seed=17380, col=AMARILLO)
    return im


TRAMOS = [(T_INI, carta_sc), (T_SOPA, sopa_sc), (T_P4, preg4), (T_R4, resp4)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
