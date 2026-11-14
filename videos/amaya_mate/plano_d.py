# -*- coding: utf-8 -*-
"""PREGUNTA TRAMPA 2 (7,735,923) + RESPUESTA 2.
preg2: PAUSA, señal amarilla «¡OJO: TRAMPA!» que se balancea; el número entra grupito por grupito cuando la voz lo dice
       (7 · 735 · 923); «¿CÓMO SE LEE COMPLETO?»; cuenta 3-2-1 en el silencio.
resp2: el número por grupitos con su lectura debajo (SIETE MILLONES · SETECIENTOS TREINTA Y CINCO MIL · NOVECIENTOS VEINTITRÉS)
       y sus gafetes MILLONES · MIL · SOLITO.
cuad2: el RENGLÓN REAL de su cuaderno; «treinta dos» se tacha y se escribe «TREINTA Y CINCO» a mano, «¡CORRÍJANLO!»; truco
       «LÉANLO EN VOZ ALTA» con una boquita que dice cada grupito."""
import math

import numpy as np

from acuarela import H, TINTA, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, INI, T0, ww
from fondos_amaya import papel
from iconos_ia import palomita
from personajes import AMARILLO, pregunta
from kit_amaya import (AZUL, CREMA, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from piezas_mt import AZUL_C, MIEL, ancho_car, digitos
from plano_c import colores_grupos, grupos_x, lectura

T_INI = T0("preg2")
P, R = "preg2", "resp2"
tP2, tOjo, tTrampa, tComo, tFinP2 = ww(P, 0, "pausa"), ww(P, 0, "ojo"), ww(P, 0, "trampa"), ww(P, 0, "como"), FIN(P)
tGr = [ww(P, 0, "siete"), ww(P, 0, "setecientos"), ww(P, 0, "novecientos")]
T_R2 = T0(R)
tL = [ww(R, 0, "siete"), ww(R, 0, "setecientos"), ww(R, 0, "novecientos")]
tTres, tMll, tMil, tSol = ww(R, 0, "tres"), ww(R, 0, "millones", 1), ww(R, 0, "mil y"), ww(R, 0, "solito")
T_CU = INI(R, 1) - 0.3
tCuad, tDos, tDice, tCinco, tCorr, tTruco, tVoz, tGrup, tEscr = (
    ww(R, 1, "cuaderno"), ww(R, 1, "treinta dos"), ww(R, 1, "dice"), ww(R, 1, "cinco"), ww(R, 1, "corrijanlo"),
    ww(R, 1, "truco"), ww(R, 1, "voz"), ww(R, 1, "grupito"), ww(R, 1, "escribirla"))
NUM = "7,735,923"


def senal(im, x, y, s, t, seed):
    rot = 0.12 * math.sin(t * 3)
    c, sn = math.cos(rot), math.sin(rot)
    pts = np.array([(0, -150), (140, 95), (-140, 95)], np.float32) * s
    pts = np.stack([x + pts[:, 0] * c - pts[:, 1] * sn, y + pts[:, 0] * sn + pts[:, 1] * c], 1)
    forma(im, pts, AMARILLO, t, seed, tinta=6 * s)
    rotulo(im, "!", x - 10 * s * sn, y + 10 * s, 150 * s, TINTA, t, seed=seed + 1, rot=rot)


def por_grupitos(im, txt, x, y, px, t, tiempos, seed, cols=None):
    """El número entra en trozos («7,» · «735,» · «923»), cada uno en su segundo, sin mover los demás."""
    ws = [ancho_car(c, px) for c in txt]
    x0 = x - sum(ws) / 2
    piezas, ini = [], 0
    for i, c in enumerate(txt):
        if c == ",":
            piezas.append((ini, i + 1))
            ini = i + 1
    piezas.append((ini, len(txt)))
    for k, ((a, b), tk) in enumerate(zip(piezas, tiempos)):
        sub = txt[a:b]
        cx = x0 + sum(ws[:a]) + sum(ws[a:b]) / 2
        cc = {i - a: v for i, v in (cols or {}).items() if a <= i < b}
        digitos(im, sub, cx, y, px, t, t_ap=tk - 0.25, seed=seed + 20 * k, paso=0.05, cols=cc)


def preg2(t):
    im = cache("d_p2", lambda: papel("rosa")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP2 - 0.3), t, seed=23000, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=23005, esc=entra(t, tP2 - 0.1))
    if t > tOjo - 0.3:
        e = entra(t, tOjo - 0.3)
        senal(im, 1340, 440, 0.8 * e + 0.01, t, 23010)
        rotulo(im, "¡OJO: TRAMPA!", 1340, 640, 52 * entra(t, tTrampa - 0.2) + 1, ROJO, t, seed=23012, rot=0.04)
    if t > tGr[0] - 0.4:
        e = entra(t, tGr[0] - 0.4)
        tarjeta(im, 640, 490, 1060 * e, 250 * e, t, CREMA, 23020, rot=-0.015)
        por_grupitos(im, NUM, 620, 490, 88, t, tGr, 23030)
    if t > tComo - 0.3:
        e = entra(t, tComo - 0.3)
        letrero(im, "¿CÓMO SE LEE COMPLETO?", 640, 760, 56, t, col=AMARILLO, seed=23060, esc=e, rot=0.03)
        pregunta(im, 1170, 470, 1.3 * e + 0.01, t, seed=23065)
    cuenta(im, 1640, 250, t, tFinP2 + 0.15, T_R2 + 0.1, s=0.75, seed=23070)
    return im


def resp2(t):
    im = cache("d_r2", lambda: papel("rosa")).copy()
    letrero(im, "RESPUESTA", 300, 110, 56, t, col=VERDE, txt=CREMA, seed=23100, esc=entra(t, T_R2), rot=-0.04)
    digitos(im, NUM, 700, 340, 100, t, t_ap=T_R2 - 2, seed=23110, cols=colores_grupos(NUM))
    chispas(im, 700, 340, 300, t, tL[0], seed=23120, col=AMARILLO)
    lectura(im, t, NUM, 700, 340, 100, ["SIETE|MILLONES", "SETECIENTOS|TREINTA Y|CINCO MIL", "NOVECIENTOS|VEINTITRÉS"], tL, 23130,
            ylect=490)
    if t > tTres - 0.3:
        letrero(im, "3 GRUPITOS", 1180, 120, 46, t, col=MIEL, seed=23150, esc=entra(t, tTres - 0.3), rot=0.03)
    gx = grupos_x(NUM, 700, 100)
    for k, (nom, tk, col) in enumerate((("MILLONES", tMll, MIEL), ("MIL", tMil, AZUL_C), ("SOLITO", tSol, rgb("d8b8e8")))):
        e = entra(t, tk - 0.25)
        if e > 0.01:
            tarjeta(im, gx[k][0], 790, 250 * e + 1, 86 * e + 1, t, col, 23160 + k * 4, rot=(k - 1) * 0.05)
            rotulo(im, nom, gx[k][0], 796, 40 * e + 1, TINTA, t, seed=23161 + k * 4, tinta=False)
    return im


# renglón real: 1228×150; «treinta dos» ocupa x ≈ 1075..1228, y ≈ 10..45 de la foto
RX, RY, RE = 735, 290, 1.15


def foto_xy(ix, iy):
    return RX - 1228 / 2 * RE + ix * RE, RY - 150 / 2 * RE + iy * RE


def cuad2(t):
    im = cache("d_cu", lambda: papel("calido")).copy()
    letrero(im, "EN EL CUADERNO", 330, 100, 52, t, col=CREMA, txt=TURQ, seed=23200, esc=entra(t, T_CU + 0.1), rot=-0.04)
    e = entra(t, tCuad - 0.4, 0.5)
    polaroid(im, "renglon_735", RX, RY, RE * e, t, rot=0.0, seed=23210, alto=150, cinta=True)
    if t > tDos - 0.3:
        u = suave(pr(t, tDos - 0.2, tDos + 0.4))
        (x0, y0), (x1, _) = foto_xy(1070, 30), foto_xy(1228, 30)
        linea(im, [(x0, y0 + 6), (x0 + (x1 - x0) * u, y0 - 4)], 11, ROJO, seed=23220, t=t)
        linea(im, [(x0, y0 + 22), (x0 + (x1 - x0) * u, y0 + 12)], 8, ROJO, seed=23221, t=t)
    if t > tDice - 0.3:
        e2 = entra(t, tDice - 0.3)
        xa, ya = foto_xy(1150, 30)
        rotulo(im, "treinta y cinco", xa - 40, ya - 120, 66 * e2 + 1, ROJO, t, seed=23230, rot=-0.05, fuente="segoeprb.ttf", tinta=False)
        linea(im, [(xa - 20, ya - 80), (xa, ya - 26)], 6, ROJO, seed=23231, t=t, alfa=e2)
    if t > tCinco - 0.3:
        e3 = entra(t, tCinco - 0.3)
        digitos(im, "735", 380, 540, 90, t, t_ap=tCinco - 0.3, seed=23240, paso=0.05, cols={1: rgb("fde0dc"), 2: rgb("fde0dc")},
                fuertes={2: suave(pr(t, tCinco - 0.1, tCinco + 0.4))})
        rotulo(im, "= SETECIENTOS TREINTA Y CINCO", 990, 548, 44 * e3 + 1, MORADO, t, seed=23245, tinta=False)
    if t > tCorr - 0.4:
        rotulo(im, "¡CORRÍJANLO!", 980, 660, 70 * entra(t, tCorr - 0.4) + 1, ROJO, t, seed=23250, rot=0.03)
    if t > tTruco - 0.4:
        letrero(im, "TRUCO", 230, 800, 50, t, col=AMARILLO, seed=23260, esc=entra(t, tTruco - 0.4), rot=-0.04)
        rotulo(im, "LÉANLO EN VOZ ALTA", 700, 800, 56 * entra(t, tVoz - 0.3) + 1, MORADO, t, seed=23261)
        if t > tGrup - 0.3:
            # una boquita dice cada grupito, uno tras otro
            k = min(2, int(max(0.0, t - tGrup) / 0.8))
            ab = abs(math.sin(t * 11)) * entra(t, tGrup - 0.3)
            gx = [980, 1150, 1320]
            for j, g in enumerate(("7", "735", "923")):
                ej = entra(t, tGrup - 0.3 + 0.2 * j)
                tarjeta(im, gx[j], 900, 160 * ej + 1, 92 * ej + 1, t, rgb("fff2c0") if j == k else CREMA, 23270 + j * 3)
                rotulo(im, g, gx[j], 906, 54 * ej + 1, ROJO if j == k else TINTA, t, seed=23271 + j * 3, tinta=False)
            forma(im, elipse(gx[k], 830, 34, 8 + 16 * ab), ROSA_M, t, 23290, tinta=3)
        if t > tEscr - 0.3:
            palomita(im, 1400, 760, 1.0 * entra(t, tEscr - 0.3), t, seed=23295, col=VERDE)
    return im


TRAMOS = [(T_INI, preg2), (T_R2, resp2), (T_CU, cuad2)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
