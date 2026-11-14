# -*- coding: utf-8 -*-
"""DECIMALES + PREGUNTA 1 + RESPUESTA 1.
d0: 45.23 en fichas; el PUNTO se enciende; llave rosa «PARTE ENTERA» bajo 45 y azul «PARTE DECIMAL» bajo 23.
d1: tabla de lugares: ENTEROS · DÉCIMOS · CENTÉSIMOS · MILÉSIMOS (1.º, 2.º, 3.º) cuando los nombra.
d2: TRUCO «cuenta las cifras»: 0.8 → 1 → DÉCIMOS · 0.08 → 2 → CENTÉSIMOS · 0.008 → 3 → MILÉSIMOS, con circulitos numerados.
d3: FOTO REAL de su cuaderno (0.8 / 0.08 / 0.008) + tres ochos que se hacen cada vez más chiquitos.
d4: cómo se lee: renglón REAL «45.23 cuarenta y cinco enteros veintitrés centésimos» + 45.23 con la lectura por partes.
d5: DATO CHIDO: moneda de un peso = 100 centavos; 50 centavos = 0.50 (centavos = centésimos).
preg1/resp1: 3.023 → «TRES ENTEROS, VEINTITRÉS MILÉSIMOS», cifras 1-2-3 después del punto, el cero que brinca."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, INI, T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import (AZUL, CREMA, DORADO, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from utileria import flecha
from piezas_mt import AZUL_C, LILA_C, MIEL, ROSA_C, VERDE_C, digitos

T_INI = T0("decimales")
D = "decimales"
tPrim, tPunto, tIzq, tEnt, tDer, tDec = (ww(D, 0, "primero"), ww(D, 0, "punto"), ww(D, 0, "izquierda"), ww(D, 0, "entera"),
                                         ww(D, 0, "derecha"), ww(D, 0, "parte decimal") + 0.4)
T_D1 = INI(D, 1) - 0.3
tLug = [ww(D, 1, "decimos"), ww(D, 1, "centesimos"), ww(D, 1, "milesimos")]
T_D2 = INI(D, 2) - 0.3
tTruco, tCifras = ww(D, 2, "truco"), ww(D, 2, "cifras")
tFila = [ww(D, 2, "una"), ww(D, 2, "dos"), ww(D, 2, "tres")]
tFilaN = [ww(D, 2, "decimos"), ww(D, 2, "centesimos"), ww(D, 2, "milesimos")]
T_D3 = INI(D, 3) - 0.3
tCuad = ww(D, 3, "cuaderno")
tOcho = [ww(D, 3, "decimos"), ww(D, 3, "centesimos"), ww(D, 3, "milesimos")]
tMismo, tChiq = ww(D, 3, "mismo"), ww(D, 3, "chiquito")
T_D4 = INI(D, 4) - 0.3
tEnteros, tUlt, t45 = ww(D, 4, "enteros"), ww(D, 4, "ultimo"), ww(D, 4, "cuarenta")
tL = [ww(D, 4, "cuarenta", 1), ww(D, 4, "enteros", 1), ww(D, 4, "veintitres", 1), ww(D, 4, "centesimos")]
T_D5 = INI(D, 5) - 0.3
tDato, tCentav, tPeso, tCien, tCinc, tCero = (ww(D, 5, "dato"), ww(D, 5, "centavos"), ww(D, 5, "peso"), ww(D, 5, "cien"),
                                              ww(D, 5, "cincuenta"), ww(D, 5, "cero"))
P, R = "preg1", "resp1"
T_P1 = T0(P)
tP1, tNum1, tComo1, tFinP1 = ww(P, 0, "pausa"), ww(P, 0, "tres"), ww(P, 0, "como"), FIN(P)
T_R1 = T0(R)
tR = [ww(R, 0, "tres"), ww(R, 0, "enteros"), ww(R, 0, "veintitres"), ww(R, 0, "milesimos")]
tHay, tC0, tC2, tC3, tAsi, tAunq, tEso = (ww(R, 0, "hay"), ww(R, 0, "cero"), ww(R, 0, "dos"), ww(R, 0, "tres", 2),
                                          ww(R, 0, "milesimos", 1), ww(R, 0, "aunque"), ww(R, 0, "eso"))


def llave(im, x0, x1, y, t, col, texto, e, seed, abajo=True):
    if e <= 0.01:
        return
    d = 1 if abajo else -1
    xm = (x0 + x1) / 2
    u = e
    pts = curva([(x0, y), (x0 + 10, y + 30 * d), (xm - 20, y + 30 * d), (xm, y + 60 * d)], 8)
    pts2 = curva([(xm, y + 60 * d), (xm + 20, y + 30 * d), (x1 - 10, y + 30 * d), (x1, y)], 8)
    linea(im, pts, 8, col, seed=seed, t=t, alfa=u)
    linea(im, pts2, 8, col, seed=seed + 1, t=t, alfa=u)
    letrero(im, texto, xm, y + 120 * d, 46, t, col=col, txt=CREMA, seed=seed + 2, esc=u, rot=0.02 * d)


def d0(t):
    im = cache("b_d0", lambda: papel("calido")).copy()
    letrero(im, "1. DECIMALES", 280, 110, 56, t, col=ROSA_C, seed=21000, esc=entra(t, tPrim - 0.2), rot=-0.04)
    fz = {2: clamp(pr(t, tPunto - 0.2, tPunto + 0.3))} if t < tIzq else {}
    xs = digitos(im, "45.23", 740, 430, 150, t, t_ap=T_INI + 0.8, seed=21010,
                 cols={0: ROSA_C if t > tEnt else CREMA, 1: ROSA_C if t > tEnt else CREMA,
                       3: AZUL_C if t > tDec - 0.4 else CREMA, 4: AZUL_C if t > tDec - 0.4 else CREMA})
    if tPunto - 0.2 < t:
        e = entra(t, tPunto - 0.2)
        brillo_r = 1 + 0.15 * math.sin(t * 7)
        lavado(im, elipse(xs[2], 500, 46 * brillo_r * e, 46 * brillo_r * e), AMARILLO, 0.45, 21030, humedo=6)
        rotulo(im, "PUNTO", xs[2], 250, 54 * e + 1, ROJO, t, seed=21031)
        linea(im, [(xs[2], 280), (xs[2], 380)], 6, ROJO, seed=21032, t=t, alfa=e)
    llave(im, xs[0] - 90, xs[1] + 90, 560, t, ROSA_M, "PARTE ENTERA", entra(t, tEnt - 0.3), 21040)
    llave(im, xs[3] - 90, xs[4] + 90, 560, t, AZUL, "PARTE DECIMAL", entra(t, tDec - 0.6), 21050)
    if t > tIzq - 0.2:
        rotulo(im, "IZQUIERDA", xs[0] - 40, 830, 40 * entra(t, tIzq - 0.2) + 1, ROSA_M, t, seed=21060, tinta=False)
    if t > tDer - 0.2:
        rotulo(im, "DERECHA", xs[4] + 40, 830, 40 * entra(t, tDer - 0.2) + 1, AZUL, t, seed=21061, tinta=False)
    return im


def clamp(v):
    return max(0.0, min(1.0, v))


LUG = [("ENTEROS", ROSA_C, ""), ("DÉCIMOS", AZUL_C, "1.º"), ("CENTÉSIMOS", VERDE_C, "2.º"), ("MILÉSIMOS", LILA_C, "3.º")]


def tabla(im, t, t_aps, y=330, xs=(260, 640, 960, 1280), seed=21100, digs=None, t_digs=-9, alto=420):
    for k, ((txt, col, n), x) in enumerate(zip(LUG, xs)):
        e = entra(t, t_aps[k] - 0.25)
        if e <= 0.01:
            continue
        tarjeta(im, x, y, 300 * e, 110 * e, t, col, seed + k * 6, rot=(k - 1.5) * 0.015)
        rotulo(im, txt, x, y + 4, (40 if len(txt) > 8 else 46) * e + 1, TINTA, t, seed=seed + 1 + k * 6, tinta=False)
        forma(im, rrect(x, y + 100 + alto / 2, 260 * e + 1, alto * e + 1, 16), rgb("fbf8ee"), t, seed + 2 + k * 6, tinta=3)
        if n:
            rotulo(im, n, x, y - 90, 52 * e + 1, MORADO, t, seed=seed + 3 + k * 6)
        if digs:
            ed = entra(t, t_aps[k] + 0.1)
            if ed > 0.01:
                rotulo(im, digs[k], x, y + 100 + alto / 2 + 8, 130 * ed, AZUL, t, seed=seed + 4 + k * 6)
    if len(xs) > 1 and t > t_aps[1] - 0.25:
        x = (xs[0] + xs[1]) / 2
        forma(im, elipse(x, y + 100 + alto / 2 + 50, 18, 18), ROJO, t, seed + 40, tinta=3)


def d1(t):
    im = cache("b_d1", lambda: papel("frio")).copy()
    letrero(im, "CADA LUGAR TIENE NOMBRE", 560, 110, 52, t, col=CREMA, txt=AZUL, seed=21090, esc=entra(t, T_D1), rot=-0.03)
    tabla(im, t, [T_D1 + 0.3] + tLug, alto=320, digs=["4", "5", "7", "2"])
    if t > tLug[0] - 0.2:
        u = (t - tLug[0]) * 0.6
        _ = u
    return im


def d2(t):
    im = cache("b_d2", lambda: papel("rosa")).copy()
    letrero(im, "TRUCO", 240, 110, 58, t, col=AMARILLO, seed=21200, esc=entra(t, tTruco - 0.3), rot=-0.05)
    rotulo(im, "CUENTA LAS CIFRAS DESPUÉS DEL PUNTO", 820, 120, 46 * entra(t, tCifras - 0.3) + 1, MORADO, t, seed=21201, tinta=False)
    if tCifras - 0.3 < t < tFila[0] - 0.2:
        e = entra(t, tCifras - 0.3)
        xs = digitos(im, "0.008", 740, 520, 150, t, t_ap=tCifras - 0.3, seed=21205, paso=0.05)
        for i in range(2, 5):
            ei = entra(t, tCifras + 0.25 * (i - 1))
            forma(im, elipse(xs[i], 380, 34 * ei + 1, 34 * ei + 1), ROJO, t, 21206 + i, tinta=2)
            rotulo(im, str(i - 1), xs[i], 386, 46 * ei + 1, CREMA, t, seed=21207 + i, tinta=False)
        rotulo(im, "¿CUÁNTAS HAY?", 740, 760, 64 * e + 1, MORADO, t, seed=21204)
    FIL = [("0.8", "1 CIFRA", "DÉCIMOS", AZUL_C), ("0.08", "2 CIFRAS", "CENTÉSIMOS", VERDE_C), ("0.008", "3 CIFRAS", "MILÉSIMOS", LILA_C)]
    for k, (num, nc, nom, col) in enumerate(FIL):
        y = 300 + 200 * k
        e = entra(t, tFila[k] - 0.3)
        if e <= 0.01:
            continue
        xs = digitos(im, num, 380, y, 100, t, t_ap=tFila[k] - 0.3, seed=21210 + k * 20, paso=0.04,
                     cols={i: col for i in range(2, len(num))})
        for i in range(2, len(num)):
            ei = entra(t, tFila[k] - 0.1 + 0.15 * (i - 2))
            forma(im, elipse(xs[i], y - 92, 22 * ei + 1, 22 * ei + 1), ROJO, t, 21260 + k * 5 + i, tinta=2)
            rotulo(im, str(i - 1), xs[i], y - 88, 30 * ei + 1, CREMA, t, seed=21270 + k * 5 + i, tinta=False)
        rotulo(im, nc, 830, y + 6, 46 * e + 1, TINTA, t, seed=21280 + k, tinta=False)
        flecha(im, 950, y, 950 + 90 * e, y, 10, t, MORADO, seed=21285 + k)
        en = entra(t, tFilaN[k] - 0.25)
        if en > 0.01:
            letrero(im, nom, 1220, y, 50, t, col=col, seed=21290 + k, esc=en, rot=0.02 * (k - 1))
    return im


def d3(t):
    im = cache("b_d3", lambda: papel("calido")).copy()
    letrero(im, "EN SU CUADERNO", 300, 110, 52, t, col=CREMA, txt=TURQ, seed=21300, esc=entra(t, T_D3 + 0.1), rot=-0.04)
    e = entra(t, tCuad - 0.4, 0.5)
    polaroid(im, "dec_ochos", 450, 460, 0.92 * e, t, rot=-0.03, seed=21310, alto=300)
    TAM = [(1060, 250, 200, "OCHO DÉCIMOS"), (1060, 480, 130, "OCHO CENTÉSIMOS"), (1060, 670, 70, "OCHO MILÉSIMOS")]
    for k, (x, y, px, txt) in enumerate(TAM):
        ek = entra(t, tOcho[k] - 0.5)
        if ek <= 0.01:
            continue
        enc = 1 - 0.15 * suave(pr(t, tMismo, tChiq + 0.6)) * k
        rotulo(im, "8", x - 160, y + 10, px * ek * enc, [AZUL, VERDE, MORADO][k], t, seed=21320 + k)
        rotulo(im, txt, x + 120, y + 6, 40 * ek + 1, TINTA, t, seed=21325 + k, tinta=False)
    if t > tChiq - 0.4:
        letrero(im, "¡CADA VEZ MÁS CHIQUITO!", 640, 860, 50, t, col=AMARILLO, seed=21340, esc=entra(t, tChiq - 0.4), rot=0.03)
    return im


def d4(t):
    im = cache("b_d4", lambda: papel("frio")).copy()
    letrero(im, "¿CÓMO SE LEE?", 280, 110, 52, t, col=CREMA, txt=ROJO, seed=21400, esc=entra(t, T_D4 + 0.1), rot=-0.04)
    e = entra(t, t45 - 0.4)
    if e > 0.01:
        PI_pegar_renglon(im, t, e)
    rotulo(im, "1) PARTE ENTERA + «ENTEROS»", 760, 230, 42 * entra(t, tEnteros - 0.3) + 1, ROSA_M, t, seed=21410, tinta=False)
    rotulo(im, "2) LO DEL PUNTO + NOMBRE DEL ÚLTIMO LUGAR", 760, 295, 42 * entra(t, tUlt - 0.3) + 1, AZUL, t, seed=21411, tinta=False)
    xs = digitos(im, "45.23", 640, 450, 110, t, t_ap=T_D4 + 0.5, seed=21420,
                 cols={0: ROSA_C, 1: ROSA_C, 3: AZUL_C, 4: AZUL_C}, fuertes={4: clamp(pr(t, tL[3] - 0.2, tL[3] + 0.3))})
    PAR = [("CUARENTA Y CINCO", (xs[0] + xs[1]) / 2, 600, ROSA_M), ("ENTEROS", (xs[0] + xs[1]) / 2, 665, ROSA_M),
           ("VEINTITRÉS", (xs[3] + xs[4]) / 2 + 60, 600, AZUL), ("CENTÉSIMOS", (xs[3] + xs[4]) / 2 + 60, 665, AZUL)]
    for k, (txt, x, y, col) in enumerate(PAR):
        ek = entra(t, tL[k] - 0.2)
        if ek > 0.01:
            rotulo(im, txt, x, y, 50 * ek + 1, col, t, seed=21430 + k)
    if t > tL[3]:
        rotulo(im, "2 CIFRAS", xs[4] + 170, 400, 36 * entra(t, tL[3]) + 1, MORADO, t, seed=21440, tinta=False)
    return im


def PI_pegar_renglon(im, t, e):
    polaroid(im, "dec_45", 700, 850, 0.78 * e, t, rot=0.01, seed=21450, alto=140, cinta=True)


def d5(t):
    from piezas_fj import moneda
    im = cache("b_d5", lambda: papel("rosa")).copy()
    letrero(im, "DATO CHIDO", 280, 110, 54, t, col=AMARILLO, seed=21500, esc=entra(t, tDato - 0.3), rot=-0.05)
    if t > tCentav - 0.3:
        e = entra(t, tCentav - 0.3)
        rotulo(im, "CENTAVOS = CENTÉSIMOS", 800, 130, 60 * e + 1, ROJO, t, seed=21501)
    if t > tCentav - 0.3:
        e = entra(t, tCentav - 0.3)
        moneda(im, 330, 450, 3.2 * e + 0.01, t, seed=21510)
        rotulo(im, "$1", 330, 460, 90 * e + 1, rgb("6a4a1a"), t, seed=21511)
        rotulo(im, "UN PESO", 330, 650, 46 * e + 1, TINTA, t, seed=21512, tinta=False)
    if t > tCien - 0.3:
        e = entra(t, tCien - 0.3)
        for d in (-1, 1):
            linea(im, [(530, 450 + d * 16), (590, 450 + d * 16)], 12 * e + 1, TINTA, seed=21520 + d, t=t)
        for k in range(10):
            ek = entra(t, tCien - 0.3 + 0.05 * k)
            for j in range(10):
                x, y = 700 + j * 34, 300 + k * 30
                if ek > 0.01 and (k * 10 + j) < 100:
                    col = AMARILLO if (t > tCinc - 0.2 and k < 5) else rgb("e0c890")
                    forma(im, elipse(x, y, 13 * ek, 13 * ek), col, t, 21530 + k * 10 + j, tinta=1.6)
        rotulo(im, "100 CENTAVOS", 860, 640, 46 * e + 1, TINTA, t, seed=21640, tinta=False)
    if t > tCinc - 0.3:
        e = entra(t, tCinc - 0.3)
        tarjeta(im, 1250, 420, 300 * e + 1, 360 * e + 1, t, rgb("fff2c0"), 21650, rot=0.03)
        rotulo(im, "50", 1250, 330, 90 * e + 1, MORADO, t, seed=21651)
        rotulo(im, "CENTAVOS", 1250, 410, 34 * e + 1, TINTA, t, seed=21652, tinta=False)
        if t > tCero - 0.3:
            rotulo(im, "0.50", 1250, 520, 92 * entra(t, tCero - 0.3) + 1, ROJO, t, seed=21653)
    return im


def preg1(t):
    im = cache("b_p1", lambda: papel("frio")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP1 - 0.3), t, seed=21700, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=21705, esc=entra(t, tP1 - 0.1))
    if t > tNum1 - 0.3:
        e = entra(t, tNum1 - 0.3)
        tarjeta(im, 740, 520, 760 * e, 280 * e, t, CREMA, 21710, rot=-0.02)
        digitos(im, "3.023", 700, 520, 130, t, t_ap=tNum1 - 0.3, seed=21712)
        pregunta(im, 1180, 470, 1.5 * e + 0.01, t, seed=21720)
    if t > tComo1 - 0.3:
        letrero(im, "¿CÓMO SE LEE?", 740, 800, 60, t, col=AMARILLO, seed=21725, esc=entra(t, tComo1 - 0.3), rot=0.03)
    cuenta(im, 1640, 250, t, tFinP1 + 0.15, T_R1 + 0.1, s=0.75, seed=21730)
    return im


def resp1(t):
    im = cache("b_r1", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 300, 120, 56, t, col=VERDE, txt=CREMA, seed=21800, esc=entra(t, T_R1), rot=-0.04)
    brinca = 40 * abs(math.sin((t - tAunq) * 9)) * (1 - pr(t, tAunq, tAunq + 1.6)) if t > tAunq else 0.0
    xs = digitos(im, "3.023", 640, 430, 130, t, t_ap=T_R1 - 2, seed=21712, cols={0: ROSA_C, 2: LILA_C, 3: LILA_C, 4: LILA_C},
                 sube={2: brinca})
    for k, tk in enumerate((tC0, tC2, tC3)):
        ek = entra(t, tk - 0.2)
        if ek > 0.01:
            forma(im, elipse(xs[2 + k], 300, 26 * ek, 26 * ek), ROJO, t, 21820 + k, tinta=2)
            rotulo(im, str(k + 1), xs[2 + k], 305, 34 * ek + 1, CREMA, t, seed=21825 + k, tinta=False)
    chispas(im, 640, 430, 280, t, tR[0], seed=21830, col=AMARILLO)
    TX = [("TRES", 360, 640, ROSA_M), ("ENTEROS", 360, 710, ROSA_M), ("VEINTITRÉS", 900, 640, MORADO), ("MILÉSIMOS", 900, 710, MORADO)]
    for k, (txt, x, y, col) in enumerate(TX):
        ek = entra(t, tR[k] - 0.2)
        if ek > 0.01:
            rotulo(im, txt, x, y, 60 * ek + 1, col, t, seed=21840 + k)
    if t > tAsi - 0.3:
        letrero(im, "3 CIFRAS = MILÉSIMOS", 1100, 190, 44, t, col=LILA_C, seed=21850, esc=entra(t, tAsi - 0.3), rot=0.03)
    if t > tAunq - 0.3:
        rotulo(im, "¡AUNQUE EMPIECE CON 0!", 740, 850, 52 * entra(t, tAunq - 0.3) + 1, ROJO, t, seed=21855)
    if t > tEso - 0.3:
        palomita(im, 1260, 640, 1.4 * entra(t, tEso - 0.3), t, seed=21860, col=VERDE)
    return im


TRAMOS = [(T_INI, d0), (T_D1, d1), (T_D2, d2), (T_D3, d3), (T_D4, d4), (T_D5, d5), (T_P1, preg1), (T_R1, resp1)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
