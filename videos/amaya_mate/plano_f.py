# -*- coding: utf-8 -*-
"""PLANO CARTESIANO + PREGUNTA 4 + RESPUESTA 4 (todo sobre la misma cuadrícula a la izquierda; a la derecha lo que se explica).
f0: «4. PLANO CARTESIANO» + renglón REAL de su cuaderno («Es una hoja cuadriculada donde podemos ubicar…»); la cuadrícula se pinta,
    brotan puntos, salen los ejes X (azul) y Y (rojo).
f1: X = ACOSTADO = ABSCISAS (el eje azul brilla, un monito acostado) · Y = PARADO = ORDENADAS (el rojo brilla, monito parado).
f2: ( X , Y ): primero X, luego Y; el abecedario V W X Y Z con X antes que Y.
f3: TRUCO «PRIMERO CAMINAS, LUEGO SUBES» + FOTO REAL del barco de su cuaderno; un monito camina 1 y sube 4 → A(1,4) y el barco.
f4: D(9,4): camina 9, sube 4 → la otra punta; al revés (4,9) un fantasma cae fuera del barco con una X; «¡EL ORDEN SÍ IMPORTA!».
preg4: el barco con todos sus puntos y B «?»; «( ? , ? )»; cuenta 3-2-1.  resp4: (3, 2), el monito camina 3 y sube 2 hasta B."""
import math

import numpy as np

from acuarela import H, TINTA, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, INI, T0, ww
from fondos_amaya import papel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import (AZUL, CREMA, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, gente, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from piezas_mt import AZUL_C, BARCO_PUNTOS, MIEL, ROSA_C, Plano, barco, digitos

T_INI = T0("plano")
F = "plano"
tAhora, tCuad, tHoja, tPuntos, tEjes, tEqX, tEqY = (ww(F, 0, "ahora"), ww(F, 0, "cuaderno"), ww(F, 0, "hoja"), ww(F, 0, "puntos"),
                                                     ww(F, 0, "ejes"), ww(F, 0, "equis"), ww(F, 0, "ye"))
T_F1 = INI(F, 1) - 0.3
tAcost, tAbsc, tParado, tOrd = ww(F, 1, "acostado"), ww(F, 1, "abscisas"), ww(F, 1, "parado"), ww(F, 1, "ordenadas")
T_F2 = INI(F, 2) - 0.3
tParen, tPrimX, tLuegoY, tAbc, tAntes = (ww(F, 2, "parentesis"), ww(F, 2, "primero"), ww(F, 2, "luego"), ww(F, 2, "abecedario"),
                                          ww(F, 2, "antes"))
T_F3 = INI(F, 3) - 0.3
tTruco, tCamin, tSubes, tBarco, tPA, tCam1, tSub4, tAhi = (
    ww(F, 3, "truco"), ww(F, 3, "caminas"), ww(F, 3, "subes"), ww(F, 3, "barco"), ww(F, 3, "punto a"), ww(F, 3, "caminas", 1),
    ww(F, 3, "subes", 1), ww(F, 3, "ahi"))
T_F4 = INI(F, 4) - 0.3
tPD, tCam9, tSub4b, tLlegas, tVolt, tCaes, tOrden = (ww(F, 4, "punto d"), ww(F, 4, "caminas"), ww(F, 4, "subes"), ww(F, 4, "llegas"),
                                                     ww(F, 4, "volteas"), ww(F, 4, "caes"), ww(F, 4, "orden"))
P, R = "preg4", "resp4"
T_P4 = T0(P)
tP4, tBarcoP, tCoord, tFinP4 = ww(P, 0, "pausa"), ww(P, 0, "barco"), ww(P, 0, "coordenadas"), FIN(P)
T_R4 = T0(R)
tTres, tDos, tCam3, tSub2, tPrimR, tBien = (ww(R, 0, "tres"), ww(R, 0, "dos"), ww(R, 0, "caminas"), ww(R, 0, "subes"),
                                            ww(R, 0, "primero"), ww(R, 0, "bien"))

PL = Plano(300, 940, 64, nx=9, ny=9)
XT = 1210          # centro de la columna de la derecha


def grid(im, t, u=1.0, u_ejes=1.0, seed=25000, brilla_x=0.0, brilla_y=0.0):
    PL.dibujar(im, t, seed=seed, u=u, u_ejes=u_ejes)
    if brilla_x > 0.01:
        lavado(im, rrect(PL.ox + PL.nx * PL.paso / 2 + 20, PL.oy, PL.nx * PL.paso + 90, 34, 12), AMARILLO, 0.55 * brilla_x, seed + 200,
               humedo=5)
    if brilla_y > 0.01:
        lavado(im, rrect(PL.ox, PL.oy - PL.ny * PL.paso / 2 - 20, 34, PL.ny * PL.paso + 90, 12), AMARILLO, 0.55 * brilla_y, seed + 201,
               humedo=5)
    if brilla_x > 0.01 or brilla_y > 0.01:
        PL.dibujar(im, t, seed=seed, u=0.0, u_ejes=u_ejes)


def caminante(im, t, x, y, t_c0, t_c1, t_s0, t_s1, seed, col=None, fantasma=False):
    """Monito que sale del (0,0), camina x (azul) y luego sube y (rojo), dejando su rastro."""
    if t < t_c0 - 0.3:
        return None
    uc = suave(pr(t, t_c0, t_c1))
    us = suave(pr(t, t_s0, t_s1))
    cx, cy = x * uc, y * us
    alfa = 0.55 if fantasma else 1.0
    if uc > 0:
        linea(im, [PL.P(0, 0), PL.P(cx, 0)], 12, AZUL, seed=seed, t=t, alfa=0.8 * alfa, punta=False)
    if us > 0:
        linea(im, [PL.P(x, 0), PL.P(x, cy)], 12, ROJO, seed=seed + 1, t=t, alfa=0.8 * alfa, punta=False)
    px, py = PL.P(cx, cy)
    bote = 8 * abs(math.sin(t * 12)) if (t_c0 < t < t_c1 or t_s0 < t < t_s1) else 0.0
    if fantasma:
        forma(im, elipse(px, py - 40 - bote, 22, 30), rgb("e8e8f0"), t, seed + 2, tinta=3, alfa=0.85)
        for d in (-1, 1):
            forma(im, elipse(px + d * 8, py - 46 - bote, 3, 5), TINTA, t, seed + 3 + d, tinta=0)
    else:
        gente(im, px, py - 66 - bote, 1.1, t, seed=seed % 6 + 2, cara="feliz", col=col)
    return px, py


def f0(t):
    im = cache("f_f0", lambda: papel("frio")).copy()
    letrero(im, "4. PLANO CARTESIANO", 360, 100, 54, t, col=AZUL_C, seed=25300, esc=entra(t, tAhora - 0.2), rot=-0.04)
    e = entra(t, tCuad - 0.4, 0.5)
    polaroid(im, "plano_def", 1130, 200, 0.88 * e, t, rot=0.02, seed=25310, alto=170)
    u = suave(pr(t, tHoja - 0.2, tHoja + 1.2))
    if u > 0:
        grid(im, t, u=u, u_ejes=suave(pr(t, tEjes - 0.3, tEjes + 0.4)))
    if t > tHoja:
        rotulo(im, "HOJA CUADRICULADA", XT, 470, 50 * entra(t, tHoja) + 1, MORADO, t, seed=25320)
    if t > tPuntos - 0.3:
        for k, (x, y) in enumerate(((2, 6), (5, 3), (7, 7), (8, 2))):
            ek = entra(t, tPuntos - 0.3 + 0.12 * k) * (1 - suave(pr(t, tEjes, tEjes + 0.5)))
            PL.punto(im, x, y, t, seed=25330 + k * 3, e=ek, col=MIEL)
    if t > tEjes - 0.3:
        rotulo(im, "2 EJES", XT, 580, 60 * entra(t, tEjes - 0.3) + 1, VERDE, t, seed=25350)
    for k, (txt, tk, col) in enumerate((("EJE X", tEqX, AZUL), ("EJE Y", tEqY, ROJO))):
        if t > tk - 0.3:
            letrero(im, txt, XT - 150 + 300 * k, 700, 52, t, col=CREMA, txt=col, seed=25360 + k * 4, esc=entra(t, tk - 0.3),
                    rot=(k - 0.5) * 0.06)
    return im


def acostado(im, x, y, t, seed, parado=False):
    if parado:
        gente(im, x, y - 60, 1.3, t, seed=seed, cara="feliz")
    else:
        forma(im, rrect(x + 10, y, 120, 50, 18), rgb("3f78c8"), t, seed, tinta=3)
        forma(im, elipse(x - 70, y - 4, 30, 30), rgb("f2c9a4"), t, seed + 1, tinta=3)
        for k in range(3):
            rotulo(im, "z", x + 40 + 22 * k, y - 60 - 18 * k - 6 * math.sin(t * 3 + k), 26 + 8 * k, MORADO, t, seed=seed + 3 + k,
                   tinta=False)


def f1(t):
    im = cache("f_f1", lambda: papel("frio")).copy()
    bx = suave(pr(t, tAcost - 0.3, tAcost + 0.3)) * (1 - suave(pr(t, tParado - 0.6, tParado - 0.2)))
    by = suave(pr(t, tParado - 0.3, tParado + 0.3))
    grid(im, t, brilla_x=bx, brilla_y=by)
    if t > tAcost - 0.3:
        e = entra(t, tAcost - 0.3)
        letrero(im, "X = ACOSTADO", XT, 200, 54, t, col=AZUL_C, seed=25400, esc=e, rot=-0.03)
        acostado(im, XT, 340, t, 25405)
        if t > tAbsc - 0.4:
            rotulo(im, "EJE DE LAS ABSCISAS", XT, 440, 46 * entra(t, tAbsc - 0.4) + 1, AZUL, t, seed=25410)
    if t > tParado - 0.3:
        e = entra(t, tParado - 0.3)
        letrero(im, "Y = PARADO", XT, 560, 54, t, col=ROSA_C, seed=25420, esc=e, rot=0.03)
        acostado(im, XT, 730, t, 25425, parado=True)
        if t > tOrd - 0.4:
            rotulo(im, "EJE DE LAS ORDENADAS", XT, 820, 46 * entra(t, tOrd - 0.4) + 1, ROJO, t, seed=25430)
    return im


def f2(t):
    im = cache("f_f1", lambda: papel("frio")).copy()
    grid(im, t)
    e = entra(t, tParen - 0.5)
    rotulo(im, "(", XT - 240, 270, 150 * e + 1, MORADO, t, seed=25500)
    rotulo(im, ")", XT + 240, 270, 150 * e + 1, MORADO, t, seed=25501)
    rotulo(im, ",", XT, 300, 110 * e + 1, MORADO, t, seed=25502)
    ex = entra(t, tPrimX - 0.3)
    ey = entra(t, tLuegoY - 0.3)
    rotulo(im, "X", XT - 120, 275, 150 * ex + 1, AZUL, t, seed=25503)
    rotulo(im, "Y", XT + 120, 275, 150 * ey + 1, ROJO, t, seed=25504)
    if ex > 0.01:
        rotulo(im, "1.º", XT - 120, 130, 50 * ex + 1, AZUL, t, seed=25505, tinta=False)
    if ey > 0.01:
        rotulo(im, "2.º", XT + 120, 130, 50 * ey + 1, ROJO, t, seed=25506, tinta=False)
    if t > tAbc - 0.4:
        letrero(im, "COMO EN EL ABECEDARIO", XT, 520, 44, t, col=AMARILLO, seed=25510, esc=entra(t, tAbc - 0.4), rot=-0.02)
        sube = {2: 20 * abs(math.sin(t * 8)) * pr(t, tAntes - 0.6, tAntes + 0.2) * (1 - pr(t, tAntes + 0.8, tAntes + 1.2)),
                3: 0.0}
        digitos(im, "VWXYZ", XT, 680, 70, t, t_ap=tAbc - 0.3, seed=25520, paso=0.06, cols={2: AZUL_C, 3: ROSA_C}, sube=sube)
        if t > tAntes - 0.3:
            rotulo(im, "LA X VA ANTES QUE LA Y", XT, 820, 44 * entra(t, tAntes - 0.3) + 1, MORADO, t, seed=25530, tinta=False)
    return im


def f3(t):
    im = cache("f_f3", lambda: papel("calido")).copy()
    grid(im, t)
    letrero(im, "TRUCO", 1000, 110, 52, t, col=AMARILLO, seed=25600, esc=entra(t, tTruco - 0.3), rot=-0.04)
    if t > tCamin - 0.3:
        rotulo(im, "1) CAMINAS", 1300, 90, 44 * entra(t, tCamin - 0.3) + 1, AZUL, t, seed=25601)
    if t > tSubes - 0.3:
        rotulo(im, "2) SUBES", 1300, 150, 44 * entra(t, tSubes - 0.3) + 1, ROJO, t, seed=25602)
    e = entra(t, tBarco - 0.4, 0.5)
    polaroid(im, "barco", XT, 520, 0.68 * e * (1 - 0.25 * suave(pr(t, tPA - 0.3, tPA + 0.4))), t, rot=0.025, seed=25610, alto=520)
    if t > tPA - 0.3:
        letrero(im, "A ( 1 , 4 )", XT, 820, 54, t, col=CREMA, txt=MORADO, seed=25620, esc=entra(t, tPA - 0.3), rot=0.02)
    barco(im, PL, t, seed=25630, e=entra(t, tAhi - 0.3), alfa=0.55)
    caminante(im, t, 1, 4, tCam1 - 0.1, tCam1 + 0.5, tSub4 - 0.1, tSub4 + 0.5, 25650)
    if t > tSub4 + 0.4:
        PL.punto(im, 1, 4, t, "A", seed=25660, e=entra(t, tSub4 + 0.4), col=AMARILLO)
    if t > tAhi - 0.2:
        destello(im, *PL.P(1, 4), 0.9 * entra(t, tAhi - 0.2), t, seed=25665)
    return im


def f4(t):
    im = cache("f_f3", lambda: papel("calido")).copy()
    grid(im, t)
    barco(im, PL, t, seed=25630, e=1.0, alfa=0.55)
    PL.punto(im, 1, 4, t, "A", seed=25660, col=AMARILLO)
    if t > tPD - 0.3:
        letrero(im, "D ( 9 , 4 )", XT, 230, 54, t, col=CREMA, txt=MORADO, seed=25700, esc=entra(t, tPD - 0.3), rot=-0.02)
    caminante(im, t, 9, 4, tCam9 - 0.1, tCam9 + 0.7, tSub4b - 0.1, tSub4b + 0.5, 25710)
    if t > tSub4b + 0.4:
        PL.punto(im, 9, 4, t, "D", seed=25720, e=entra(t, tSub4b + 0.4), col=AMARILLO, dx=26)
        rotulo(im, "LA OTRA PUNTA", XT, 330, 44 * entra(t, tLlegas - 0.3) + 1, VERDE, t, seed=25725, tinta=False)
    if t > tVolt - 0.3:
        letrero(im, "AL REVÉS: ( 4 , 9 )", XT, 470, 50, t, col=rgb("fde0dc"), txt=ROJO, seed=25730, esc=entra(t, tVolt - 0.3), rot=0.03)
        caminante(im, t, 4, 9, tVolt + 0.4, tVolt + 0.9, tVolt + 1.1, tCaes + 0.2, 25740, fantasma=True)
    if t > tCaes:
        ec = entra(t, tCaes)
        marca_x(im, *PL.P(4, 9), 0.9 * ec, t, seed=25750)
        rotulo(im, "¡FUERA DEL BARCO!", XT, 580, 46 * ec + 1, ROJO, t, seed=25755)
    if t > tOrden - 0.4:
        letrero(im, "¡EL ORDEN SÍ IMPORTA!", XT, 740, 52, t, col=AMARILLO, seed=25760, esc=entra(t, tOrden - 0.4), rot=-0.03)
    return im


def puntos_barco(im, t, e=1.0, oculto="", seed=25800):
    for k, (n, (x, y)) in enumerate(BARCO_PUNTOS.items()):
        if n == oculto:
            continue
        PL.punto(im, x, y, t, n, seed=seed + k * 3, e=e, col=AMARILLO, dx=26 if x >= 6 else -26)


def preg4(t):
    im = cache("f_p4", lambda: papel("rosa")).copy()
    grid(im, t)
    eb = entra(t, tBarcoP - 0.4)
    barco(im, PL, t, seed=25630, e=eb, alfa=0.6)
    puntos_barco(im, t, e=eb, oculto="B")
    pausa(im, 1000, 120, 0.55 * entra(t, tP4 - 0.3), t, seed=25850, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 1330, 120, 56, ROJO, t, seed=25855, esc=entra(t, tP4 - 0.1))
    if t > tCoord - 0.4:
        e = entra(t, tCoord - 0.4)
        bx, by = PL.P(3, 2)
        forma(im, elipse(bx, by, 22 * e + 1, 22 * e + 1), ROJO, t, 25860, tinta=3)
        rotulo(im, "B", bx - 30, by + 40, 46 * e + 1, ROJO, t, seed=25861)
        pregunta(im, bx + 60, by - 50, 0.9 * e + 0.01, t, seed=25862)
        letrero(im, "B ( ? , ? )", XT, 450, 70, t, col=CREMA, txt=MORADO, seed=25870, esc=e, rot=-0.02)
        rotulo(im, "¿COORDENADAS?", XT, 600, 52 * e + 1, MORADO, t, seed=25871)
    cuenta(im, 1640, 300, t, tFinP4 + 0.15, T_R4 + 0.1, s=0.7, seed=25880)
    return im


def resp4(t):
    im = cache("f_p4", lambda: papel("rosa")).copy()
    grid(im, t)
    barco(im, PL, t, seed=25630, e=1.0, alfa=0.6)
    puntos_barco(im, t, oculto="B")
    letrero(im, "RESPUESTA", 1080, 110, 56, t, col=VERDE, txt=CREMA, seed=25900, esc=entra(t, T_R4), rot=-0.04)
    e3, e2 = entra(t, tTres - 0.3), entra(t, tDos - 0.3)
    rotulo(im, "B (", XT - 170, 330, 90, MORADO, t, seed=25905)
    rotulo(im, "3", XT - 20, 330, 110 * e3 + 1, AZUL, t, seed=25906)
    rotulo(im, ",", XT + 50, 350, 90, MORADO, t, seed=25907)
    rotulo(im, "2", XT + 120, 330, 110 * e2 + 1, ROJO, t, seed=25908)
    rotulo(im, ")", XT + 200, 330, 90, MORADO, t, seed=25909)
    chispas(im, XT, 330, 200, t, tTres, seed=25910, col=AMARILLO)
    caminante(im, t, 3, 2, tCam3 - 0.1, tCam3 + 0.5, tSub2 - 0.1, tSub2 + 0.5, 25920)
    if t > tSub2 + 0.4:
        PL.punto(im, 3, 2, t, "B", seed=25930, e=entra(t, tSub2 + 0.4), col=VERDE)
        destello(im, *PL.P(3, 2), 0.9 * entra(t, tSub2 + 0.4), t, seed=25931)
    if t > tCam3 - 0.3:
        rotulo(im, "CAMINAS 3", XT, 500, 46 * entra(t, tCam3 - 0.3) + 1, AZUL, t, seed=25940)
    if t > tSub2 - 0.3:
        rotulo(im, "SUBES 2", XT, 570, 46 * entra(t, tSub2 - 0.3) + 1, ROJO, t, seed=25941)
    if t > tPrimR - 0.3:
        letrero(im, "PRIMERO X, LUEGO Y", XT, 710, 46, t, col=AMARILLO, seed=25950, esc=entra(t, tPrimR - 0.3), rot=0.03)
    if t > tBien - 0.3:
        palomita(im, XT + 260, 560, 1.2 * entra(t, tBien - 0.3), t, seed=25960, col=VERDE)
    return im


TRAMOS = [(T_INI, f0), (T_F1, f1), (T_F2, f2), (T_F3, f3), (T_F4, f4), (T_P4, preg4), (T_R4, resp4)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
