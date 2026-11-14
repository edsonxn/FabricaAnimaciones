# -*- coding: utf-8 -*-
"""NÚMEROS GRANDES.
c0: 681092012 sin comas que tiembla («¡DAN MIEDO!») → TRUCO: se parte en grupitos de 3 desde la derecha (las comas caen una a una).
c1: 25,980,634: la 1.ª coma = MIL, la 2.ª = MILLONES; cada grupito en su caja y su «apellido» en gafete (MILLONES · MIL).
c2: renglón REAL de su cuaderno (25,980,634) + la lectura por grupitos, cada uno cuando la voz lo dice.
c3: OJO CON LOS CEROS: renglón REAL 681,092,012 + lectura; los ceros de enfrente se tapan la boca («NO SE DICE») y luego
    un lápiz los escribe («PERO SE ESCRIBE»)."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import INI, T0, ww
from fondos_amaya import papel
from personajes import AMARILLO, destello, exclama
from kit_amaya import (AZUL, CREMA, MORADO, ROJO, VERDE, cache, entra, letrero, papa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from piezas_mt import AZUL_C, LILA_C, MIEL, ROSA_C, VERDE_C, ancho_car, digitos
from utileria import flecha

T_INI = T0("numeros")
N = "numeros"
tLeer, tMiedo, tTruco, tGrup, tEmp, tDer = (ww(N, 0, "leer"), ww(N, 0, "miedo"), ww(N, 0, "truco"), ww(N, 0, "grupitos"),
                                            ww(N, 0, "empezando"), ww(N, 0, "derecha"))
T_C1 = INI(N, 1) - 0.3
tPrimera, tMiles, tSegunda, tMillones, tCada, tSolito, tApell, tMll2, tMil2 = (
    ww(N, 1, "primera"), ww(N, 1, "miles"), ww(N, 1, "segunda"), ww(N, 1, "millones"), ww(N, 1, "cada"), ww(N, 1, "solito"),
    ww(N, 1, "apellido"), ww(N, 1, "millones", 1), ww(N, 1, "o mil") + 0.3)
T_C2 = INI(N, 2) - 0.3
tCuad2, tLee = ww(N, 2, "cuaderno"), ww(N, 2, "lee")
tG2 = [ww(N, 2, "veinticinco", 1), ww(N, 2, "novecientos", 1), ww(N, 2, "seiscientos", 1)]
T_C3 = INI(N, 3) - 0.3
tOjo, tCeros = ww(N, 3, "ojo"), ww(N, 3, "ceros")
tG3 = [ww(N, 3, "seiscientos"), ww(N, 3, "noventa"), ww(N, 3, "doce")]
tCero, tNoDice, tEscrito = ww(N, 3, "cero de"), ww(N, 3, "no se"), ww(N, 3, "escrito")
GCOL = [LILA_C, AZUL_C, MIEL]           # de derecha a izquierda: unidades, miles, millones


def colores_grupos(txt):
    """{i: color} por grupito de 3 contando desde la derecha (saltando comas)."""
    cols, g, n = {}, 0, 0
    for i in range(len(txt) - 1, -1, -1):
        if txt[i] == ",":
            g += 1
            continue
        cols[i] = GCOL[min(g, 2)]
        n += 1
    return cols


def grupos_x(txt, x, px):
    """Centro x de cada grupito (de izquierda a derecha) y su ancho."""
    ws = [ancho_car(c, px) for c in txt]
    x0 = x - sum(ws) / 2
    out, ini, acc = [], x0, x0
    for c, w in zip(txt + ",", ws + [0]):
        if c == ",":
            out.append(((ini + acc) / 2, acc - ini))
            ini = acc + w
        acc += w
    return out


def c0(t):
    im = cache("c_c0", lambda: papel("frio")).copy()
    letrero(im, "2. NÚMEROS GRANDES", 330, 110, 54, t, col=AZUL_C, seed=22000, esc=entra(t, tLeer - 0.3), rot=-0.04)
    partido = t > tGrup - 0.3
    txt = "681,092,012" if partido else "681092012"
    tiembla = (8 * math.sin(t * 40) if tMiedo - 0.2 < t < tTruco else 0.0)
    comas_ok = {3: tEmp + 0.6, 7: tEmp}            # la de la derecha cae primero
    xs = digitos(im, txt, 720 + tiembla, 470, 88, t, t_ap=T_INI + 0.6, seed=22010, paso=0.04,
                 cols=colores_grupos(txt) if partido else None)
    if partido:
        for i, tc in comas_ok.items():
            if t < tc:
                forma(im, rrect(xs[i], 500, 40, 60, 6), rgb("e6f0ec"), t, 22030 + i, tinta=0)    # todavía sin coma
    if tMiedo - 0.3 < t < tTruco:
        e = entra(t, tMiedo - 0.3)
        rotulo(im, "¡DAN MIEDO!", 720, 700, 90 * e + 1, ROJO, t, seed=22040, rot=0.04)
        for k in range(3):
            exclama(im, 330 + 390 * k, 300 - 20 * (k % 2), 1.2 * e + 0.01, t, seed=22045 + k)
    if t > tTruco - 0.3:
        letrero(im, "TRUCO", 240, 240, 58, t, col=AMARILLO, seed=22050, esc=entra(t, tTruco - 0.3), rot=-0.05)
        rotulo(im, "GRUPITOS DE 3", 720, 700, 80 * entra(t, tGrup - 0.2) + 1, MORADO, t, seed=22051)
    if t > tDer - 0.4:
        e = entra(t, tDer - 0.4)
        flecha(im, 1330, 600, 1330 - 900 * e, 600, 12, t, ROJO, seed=22060)
        rotulo(im, "DESDE LA DERECHA", 1080, 640 + 120, 46 * e + 1, ROJO, t, seed=22061, tinta=False)
    return im


def c1(t):
    im = cache("c_c1", lambda: papel("calido")).copy()
    txt = "25,980,634"
    xs = digitos(im, txt, 700, 430, 100, t, t_ap=T_C1, seed=22100, paso=0.03, cols=colores_grupos(txt))
    for i, tt, nom, col in ((6, tMiles - 0.3, "MIL", AZUL), (2, tMillones - 0.3, "MILLONES", MORADO)):
        e = entra(t, tt)
        if e > 0.01:
            lavado(im, elipse(xs[i], 480, 40 * e, 40 * e), AMARILLO, 0.5, 22110 + i, humedo=5)
            linea(im, [(xs[i], 330), (xs[i], 250)], 6, col, seed=22115 + i, t=t, alfa=e)
            letrero(im, ("1.ª COMA: " if i == 6 else "2.ª COMA: ") + nom, xs[i], 200, 44, t, col=CREMA, txt=col, seed=22120 + i,
                    esc=e, rot=0.02)
    gx = grupos_x(txt, 700, 100)
    if t > tCada - 0.3:
        for k, (cx, w) in enumerate(gx):
            e = entra(t, tCada - 0.3 + 0.2 * k)
            linea(im, rrect(cx, 430, (w + 30) * e + 1, 150 * e + 1, 16), 6, [MORADO, AZUL, VERDE][k], seed=22130 + k, t=t,
                  cerrado=True, punta=False)
        if t > tSolito - 0.3:
            rotulo(im, "CADA UNO SOLITO", 700, 610, 54 * entra(t, tSolito - 0.3) + 1, VERDE, t, seed=22140)
    if t > tApell - 0.3:
        rotulo(im, "+ SU APELLIDO", 700, 690, 54 * entra(t, tApell - 0.3) + 1, ROSA_M, t, seed=22145)
        for k, (nom, tt) in enumerate((("MILLONES", tMll2), ("MIL", tMil2))):
            e = entra(t, tt - 0.25)
            if e > 0.01:
                cx = gx[k][0]
                tarjeta(im, cx, 820, 260 * e + 1, 90 * e + 1, t, [MIEL, AZUL_C][k], 22150 + k * 4, rot=(k - 0.5) * 0.06)
                rotulo(im, nom, cx, 826, 42 * e + 1, TINTA, t, seed=22151 + k * 4, tinta=False)
                linea(im, [(cx, 775), (cx, 520)], 3, GRIS_T, seed=22153 + k * 4, t=t, alfa=0.6 * e)
    return im


GRIS_T = rgb("8f8f96")


def lectura(im, t, txt, x, y, px, piezas, tiempos, seed, ylect=640):
    """Número por grupitos y, debajo de cada grupito, su lectura (piezas: lista de 3 textos, puede haber 2 renglones con |)."""
    gx = grupos_x(txt, x, px)
    for k, ((cx, w), pz, tk) in enumerate(zip(gx, piezas, tiempos)):
        e = entra(t, tk - 0.2)
        if e <= 0.01:
            continue
        lavado(im, rrect(cx, y, w + 30, px * 1.5, 14), AMARILLO, 0.35 * e, seed + k, humedo=4)
        for j, ren in enumerate(pz.split("|")):
            rotulo(im, ren, cx, ylect + 58 * j, 46 * e + 1, [MORADO, AZUL, VERDE][k], t, seed=seed + 10 + k * 3 + j)


def c2(t):
    im = cache("c_c2", lambda: papel("rosa")).copy()
    letrero(im, "EN SU CUADERNO", 300, 110, 52, t, col=CREMA, txt=TURQ, seed=22200, esc=entra(t, T_C2 + 0.1), rot=-0.04)
    e = entra(t, tCuad2 - 0.4, 0.5)
    polaroid(im, "num_25", 720, 270, 0.9 * e, t, rot=-0.01, seed=22210, alto=140)
    txt = "25,980,634"
    digitos(im, txt, 700, 520, 90, t, t_ap=tCuad2 + 1.2, seed=22100, paso=0.03, cols=colores_grupos(txt))
    if t > tLee - 0.3:
        letrero(im, "SE LEE:", 200, 640, 44, t, col=AMARILLO, seed=22220, esc=entra(t, tLee - 0.3), rot=-0.05)
    lectura(im, t, txt, 700, 520, 90, ["VEINTICINCO|MILLONES", "NOVECIENTOS|OCHENTA MIL", "SEISCIENTOS|TREINTA Y CUATRO"], tG2,
            22230, ylect=660)
    return im


def c3(t):
    im = cache("c_c3", lambda: papel("frio")).copy()
    letrero(im, "¡OJO CON LOS CEROS!", 360, 110, 54, t, col=ROJO, txt=CREMA, seed=22300, esc=entra(t, tOjo - 0.3), rot=-0.04)
    e = entra(t, tCeros - 0.3, 0.5)
    polaroid(im, "num_681", 900, 260, 0.62 * e, t, rot=0.015, seed=22310, alto=200)
    txt = "681,092,012"
    dice = suave(pr(t, tCero - 0.2, tCero + 0.3)) * (1 - suave(pr(t, tEscrito - 0.4, tEscrito + 0.2)))
    ceros = (4, 8)
    xs = digitos(im, txt, 700, 520, 86, t, t_ap=T_C3 + 0.3, seed=22320, paso=0.03,
                 cols={**colores_grupos(txt), **({i: rgb("fde0dc") for i in ceros} if t > tCero - 0.2 else {})},
                 fuertes={i: dice for i in ceros})
    lectura(im, t, txt, 700, 520, 86, ["SEISCIENTOS OCHENTA|Y UN MILLONES", "NOVENTA Y|DOS MIL", "DOCE"], tG3, 22330, ylect=670)
    if t > tCero - 0.3 and t < tEscrito - 0.4:
        for i in ceros:
            linea(im, [(xs[i] - 30, 390), (xs[i] + 30, 390)], 10, ROJO, seed=22350 + i, t=t)        # «shh»
        rotulo(im, "¡NO SE DICE!", 700, 860, 64 * entra(t, tNoDice - 0.3) + 1, ROJO, t, seed=22360)
    if t > tEscrito - 0.5:
        ee = entra(t, tEscrito - 0.5)
        rotulo(im, "¡PERO SE ESCRIBE!", 700, 860, 64 * ee + 1, VERDE, t, seed=22361)
        for i in ceros:
            lx, ly = xs[i] + 40, 450 - 20 * math.sin(t * 9)
            linea(im, [(lx, ly), (lx + 70, ly - 110)], 16, AMARILLO, seed=22370 + i, t=t, alfa=ee)
            linea(im, [(lx, ly), (lx + 12, ly - 18)], 8, TINTA, seed=22372 + i, t=t, alfa=ee)
    return im


TRAMOS = [(T_INI, c0), (T_C1, c1), (T_C2, c2), (T_C3, c3)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
