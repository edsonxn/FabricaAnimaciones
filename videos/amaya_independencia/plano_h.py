# -*- coding: utf-8 -*-
"""ETAPA 4 · CONSUMACIÓN (1821, Iturbide): «4 CONSUMACIÓN» → Iturbide «REALISTA» contra los insurgentes → cambia de bando (cruza
la línea), se junta con Guerrero y el ABRAZO DE ACATEMPAN (corazones) → PLAN DE IGUALA: tres garantías RELIGIÓN · INDEPENDENCIA ·
UNIÓN → «EJÉRCITO TRIGARANTE» → las tres tarjetas se vuelven la bandera blanco/verde/rojo → TRUCO: R · I · U = «riu riu riu» (Kuri
se ríe bajito) → TRATADOS DE CÓRDOBA y 27 SEP 1821: el Ejército Trigarante entra a la Ciudad de México → pastel de cumpleaños de
Iturbide y «¡SE REGALÓ UN PAÍS!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from personajes import AMARILLO, corazon, destello, kuri
from utileria import flecha
from kit_amaya import (AZUL, CAFE, CREMA, DORADO, GRIS, MORADO, ROJO, VERDE, cache, cam, chispas, entra, fecha, flecha_curva,
                       gente, letrero, papa, tarjeta)
from piezas_fj import BLANCO_B, ROJO_B, VERDE_B, bandera_trigarante, base, cabecera, pastel, pergamino, regalo

T_INI = T0("consumacion")
C = "consumacion"
tCuatro, tCons, tMil, tAgus, tCur, tRealista, tPeleaba = (ww(C, 0, "cuatro"), ww(C, 0, "consumacion"), ww(C, 0, "mil"),
                                                         ww(C, 0, "agustin"), ww(C, 0, "curioso"), ww(C, 0, "realista"),
                                                         ww(C, 0, "peleaba"))
tCambio, tBando, tJunto, tGue, tAbrazo, tAcat = (ww(C, 1, "cambio"), ww(C, 1, "bando"), ww(C, 1, "junto"), ww(C, 1, "guerrero"),
                                                 ww(C, 1, "abrazo"), ww(C, 1, "acatempan"))
tPlan, tIguala, tTres, tRel, tInd, tUni, tTrig, tCol, tBand, tBl, tVe, tRo = (
    ww(C, 2, "plan"), ww(C, 2, "iguala"), ww(C, 2, "tres"), ww(C, 2, "religion"), ww(C, 2, "independencia"), ww(C, 2, "union"),
    ww(C, 2, "ejercito"), ww(C, 2, "colores"), ww(C, 2, "bandera"), ww(C, 2, "blanco"), ww(C, 2, "verde"), ww(C, 2, "rojo"))
tTruco, tErre, tU, tRies, tRiu = ww(C, 3, "truco"), ww(C, 3, "erre"), ww(C, 3, "u"), ww(C, 3, "ries"), ww(C, 3, "riu")
tTrat, tCord, t27, tTrig2, tEntro, tCiudad = (ww(C, 4, "tratados"), ww(C, 4, "cordoba"), ww(C, 4, "veintisiete"),
                                              ww(C, 4, "ejercito"), ww(C, 4, "entro"), ww(C, 4, "ciudad"))
tCumple, tItur2, tRegalo, tPais = ww(C, 5, "cumpleanos"), ww(C, 5, "iturbide"), ww(C, 5, "regalo"), ww(C, 5, "pais")
T_BANDO = tCambio - 0.5
T_PLAN = tPlan - 0.6
T_TRUCO = tTruco - 0.5
T_TRAT = tTrat - 0.5
T_CUMPLE = tCumple - 0.7
COL = rgb("f4d38a")
GAR = [("RELIGIÓN", BLANCO_B, TINTA), ("INDEPENDENCIA", VERDE_B, CREMA), ("UNIÓN", ROJO_B, CREMA)]


def cab(im, t):
    cabecera(im, t, "4 · CONSUMACIÓN · 1821", COL, 16000, w=560)


def realista(t):
    im = cache("h_real", lambda: papel("calido")).copy()
    cab(im, t)
    if t < tAgus - 0.3:
        rotulo(im, "4", 960, 400, 300, rgb("e3b04a"), t, seed=16010, esc=entra(t, tCuatro - 0.3))
        rotulo(im, "CONSUMACIÓN", 960, 660, 120, rgb("c8873a"), t, seed=16011, esc=entra(t, tCons - 0.2))
        letrero(im, "1821", 960, 820, 64, t, col=CREMA, seed=16012, esc=entra(t, tMil - 0.2))
        return im
    cam(im, "iturbide", 420, 480, 1.0 * entra(t, tAgus - 0.3, 0.45), t, "AGUSTÍN DE ITURBIDE", seed=80)
    if t > tCur - 0.3:
        letrero(im, "LO CURIOSO...", 1000, 220, 54, t, col=AMARILLO, seed=16020, esc=entra(t, tCur - 0.3), rot=-0.04)
    if t > tRealista - 0.3:
        er = entra(t, tRealista - 0.3)
        forma(im, rrect(420, 210, 420 * er + 1, 110 * er + 1, 16, -0.08), AZUL, t, 16025, tinta=5)
        rotulo(im, "REALISTA", 420, 214, 78 * er + 1, CREMA, t, seed=16026, rot=-0.08)
    if t > tPeleaba - 0.3:
        ep = entra(t, tPeleaba - 0.3)
        rotulo(im, "VS", 860, 520, 120, ROJO, t, seed=16030, esc=ep)
        for k in range(4):
            gente(im, 1060 + 110 * k, 520 + 30 * (k % 2), 2.2 * ep + 0.01, t, seed=200 + k, col=rgb("6a8a4a"), cara="enojo")
        letrero(im, "INSURGENTES", 1230, 720, 50, t, col=CREMA, txt=VERDE, seed=16035, esc=ep)
    return im


def bando(t):
    im = cache("h_bando", lambda: papel("frio")).copy()
    cab(im, t)
    # dos lados: realistas (azul) | insurgentes (verde)
    linea(im, [(960, 200), (960, 980)], 8, GRIS, seed=16100, t=t, alfa=0.6)
    rotulo(im, "REALISTAS", 480, 230, 60, AZUL, t, seed=16101)
    rotulo(im, "INSURGENTES", 1300, 230, 60, VERDE, t, seed=16102)
    u = suave(pr(t, tCambio - 0.1, tBando + 0.5))
    abr = suave(pr(t, tAbrazo - 0.5, tAbrazo + 0.3))
    xi = 480 + (560 * u) + 40 * abr
    if tCambio < t < tBando + 0.6:
        flecha_curva(im, [(520, 760), (960, 650), (1040, 760)], t, ROJO, 9, seed=16110, u=pr(t, tCambio, tBando + 0.4))
        rotulo(im, "¡CAMBIÓ DE BANDO!", 960, 880, 72, ROJO, t, seed=16115, esc=entra(t, tCambio))
    eg = entra(t, tGue - 0.3)
    xg = 1440 - 140 * abr
    if eg > 0.01:
        cam(im, "guerrero", xg, 520, 0.85 * eg, t, "VICENTE GUERRERO", seed=81, rot=-0.15 * abr)
    cam(im, "iturbide", xi, 520, 0.85, t, "ITURBIDE", seed=82, rot=0.15 * abr)
    if abr > 0.3:
        for k in range(4):
            v = ((t - tAbrazo) * 0.7 + k * 0.25) % 1
            corazon(im, (xi + xg) / 2 + 90 * math.sin(k * 2.1 + t), 380 - 260 * v, 1.6 * (1 - v) + 0.3, t, seed=16120 + k)
        letrero(im, "ABRAZO DE ACATEMPAN", 1180, 880, 62, t, col=AMARILLO, seed=16125, esc=entra(t, tAbrazo + 0.3))
    return im


def plan(t):
    im = cache("h_plan", lambda: papel("calido")).copy()
    cab(im, t)
    bandera = pr(t, tBand - 0.2, tRo + 0.5)
    if bandera < 1:
        letrero(im, "PLAN DE IGUALA", 760, 220, 66, t, col=CREMA, txt=CAFE, seed=16200, esc=entra(t, tPlan - 0.3) * (1 - bandera))
        if t > tTres - 0.3:
            rotulo(im, "3 GARANTÍAS", 760, 340, 64, ROJO, t, seed=16205, esc=entra(t, tTres - 0.3) * (1 - bandera))
    for k, ((txt, col, tc), tk) in enumerate(zip(GAR, (tRel, tInd, tUni))):
        if t > tk - 0.25:
            e = entra(t, tk - 0.25) * (1 - suave(pr(t, tBand - 0.2, tBand + 0.4)))
            if e > 0.02:
                x = 360 + 400 * k
                tarjeta(im, x, 590, 360 * e, 260 * e, t, col, 16210 + k * 5, rot=(k - 1) * 0.04)
                rotulo(im, txt, x, 596, (44 if len(txt) > 9 else 56) * e + 1, tc, t, seed=16211 + k * 5, rot=(k - 1) * 0.04,
                       tinta=False)
                rotulo(im, "RIU"[k], x, 470, 80 * e + 1, ROJO, t, seed=16212 + k * 5)
    if tTrig - 0.3 < t < tBand - 0.2:
        letrero(im, "EJÉRCITO TRIGARANTE", 760, 860, 62, t, col=AMARILLO, seed=16230, esc=entra(t, tTrig - 0.3))
        rotulo(im, "(TRI = 3)", 760, 960, 46, CAFE, t, seed=16231, esc=entra(t, tTrig + 0.4), tinta=False)
    if bandera > 0:
        ub = 1 / 3 * pr(t, tBl - 0.2, tBl + 0.3) + 1 / 3 * pr(t, tVe - 0.2, tVe + 0.3) + 1 / 3 * pr(t, tRo - 0.2, tRo + 0.3)
        bandera_trigarante(im, 780, 520, 900, 480, t, seed=16240, u=max(ub, 0.02))
        rotulo(im, "LA BANDERA TRIGARANTE", 760, 900, 64, CAFE, t, seed=16245, esc=entra(t, tBand - 0.2))
        for k, (tk, txt) in enumerate(((tBl, "BLANCO"), (tVe, "VERDE"), (tRo, "ROJO"))):
            if t > tk - 0.2:
                rotulo(im, txt, 480 + 300 * k, 820, 46, (CAFE, VERDE_B, ROJO_B)[k], t, seed=16250 + k, esc=entra(t, tk - 0.2),
                       tinta=False)
    return im


def truco(t):
    im = cache("h_truco", lambda: papel("rosa")).copy()
    cab(im, t)
    letrero(im, "TRUCO", 760, 210, 70, t, col=AMARILLO, seed=16300, esc=entra(t, tTruco - 0.3), rot=-0.04)
    ts = (tErre, tErre + 0.15, tU)
    for k, (letra, tk) in enumerate(zip("RIU", ts)):
        if t > tk - 0.2:
            e = entra(t, tk - 0.2)
            x = 420 + 340 * k
            brinca = math.exp(-((t - tRiu - 0.25 * k - 0.1) / 0.18) ** 2) if t > tRiu - 0.4 else 0.0
            forma(im, elipse(x, 470 - 40 * brinca, 130 * e + 1, 130 * e + 1), GAR[k][1], t, 16310 + k, tinta=5)
            rotulo(im, letra, x, 480 - 40 * brinca, 170 * e + 1, GAR[k][2] if k else ROJO, t, seed=16311 + k)
            rotulo(im, GAR[k][0], x, 660, (40 if k == 1 else 50) * e + 1, TINTA, t, seed=16315 + k, tinta=False)
    if t > tRies - 0.3:
        ek = entra(t, tRies - 0.3)
        rie = math.sin(t * 16)
        kuri(im, 1360, 470 + 10 * rie, 1.6 * ek, t, cara="feliz", brazos=(0.9 + 0.2 * rie, 0.9 - 0.2 * rie))
        if t > tRiu - 0.3:
            for k in range(3):
                tk = tRiu - 0.2 + 0.28 * k
                if t > tk:
                    rotulo(im, "riu", 520 + 280 * k, 880 - 20 * k, 110, MORADO, t, seed=16330 + k, esc=entra(t, tk),
                           rot=(k - 1) * 0.1, fuente="LuckiestGuy-Regular.ttf")
    return im


def tratados(t):
    im = cache("h_trat", lambda: papel("sepia")).copy()
    cab(im, t)
    entra_ = t > tTrig2 - 0.6
    if not entra_:
        pergamino(im, 560, 560, 600, 520, t, 16400, esc=entra(t, tTrat - 0.3, 0.45))
        rotulo(im, "TRATADOS", 560, 450, 64, CAFE, t, seed=16405, esc=entra(t, tTrat - 0.1), tinta=False)
        rotulo(im, "DE CÓRDOBA", 560, 530, 56, CAFE, t, seed=16406, esc=entra(t, tCord - 0.2), tinta=False)
        if t > tCord:
            linea(im, curva([(420, 700), (480, 660), (540, 720), (620, 650), (700, 700)], 8), 5, AZUL, seed=16407, t=t)
        fecha(im, 1190, 560, 1.15 * entra(t, t27 - 0.3, 0.45), t, "27", "SEP", "1821", seed=16410, col=VERDE_B)
        return im
    # el Ejército Trigarante entra a la Ciudad de México
    ec = entra(t, tTrig2 - 0.6, 0.45)
    forma(im, rrect(1150, 600, 520 * ec + 1, 360 * ec + 1, 8), rgb("e3cfa4"), t, 16420, tinta=5)       # catedral
    for d in (-1, 1):
        forma(im, rrect(1150 + d * 200 * ec, 330, 110 * ec + 1, 260 * ec + 1, 8), rgb("e8d6ae"), t, 16421 + d, tinta=4)
        forma(im, elipse(1150 + d * 200 * ec, 190, 56 * ec + 1, 40 * ec + 1), rgb("d9b77a"), t, 16424 + d, tinta=3.5)
    forma(im, rrect(1150, 690, 140 * ec + 1, 180 * ec + 1, 60), rgb("5a3a22"), t, 16427, tinta=4)
    letrero(im, "CIUDAD DE MÉXICO", 1150, 860, 52, t, col=CREMA, seed=16430, esc=entra(t, tCiudad - 0.3))
    u = pr(t, tEntro - 0.6, tCiudad + 1.2)
    for k in range(6):
        x = -100 + 160 * k + 520 * u
        if x < 1080:
            y = 700 + 10 * abs(math.sin(t * 7 + k))
            gente(im, x, y, 2.0, t, seed=210 + k, col=(VERDE_B, BLANCO_B, ROJO_B)[k % 3])
            if k % 2 == 0:
                linea(im, [(x + 40, y + 60), (x + 40, y - 150)], 6, CAFE, seed=16440 + k, t=t)
                bandera_trigarante(im, x + 110, y - 110, 130, 80, t, seed=16450 + k * 10, ondea=True)
    letrero(im, "EJÉRCITO TRIGARANTE", 520, 300, 56, t, col=AMARILLO, seed=16460, esc=entra(t, tTrig2 - 0.3))
    letrero(im, "27 SEP 1821", 520, 410, 50, t, col=CREMA, txt=ROJO, seed=16465, esc=entra(t, tTrig2))
    return im


def cumple(t):
    im = cache("h_cum", lambda: papel("rosa")).copy()
    _manchas(im, rgb("f6c6d6"), 0, 1)
    cab(im, t)
    pastel(im, 500, 640, 1.1 * entra(t, tCumple - 0.4, 0.45), t, seed=16500)
    if t > tCumple - 0.2:
        letrero(im, "¡FELIZ CUMPLEAÑOS!", 500, 240, 56, t, col=AMARILLO, seed=16505, esc=entra(t, tCumple - 0.2), rot=-0.04)
    if t > tItur2 - 0.3:
        cam(im, "iturbide", 1200, 400, 0.7 * entra(t, tItur2 - 0.3), t, "ITURBIDE", seed=83, rot=0.08)
        # gorrito de fiesta
        e = entra(t, tItur2)
        forma(im, np.array([(1130, 210), (1270, 210), (1200, 210 - 150 * e)], np.float32), MORADO, t, 16510, tinta=4)
        forma(im, elipse(1200, 210 - 150 * e, 18 * e + 1, 18 * e + 1), AMARILLO, t, 16511, tinta=2.5)
    if t > tRegalo - 0.4:
        er = entra(t, tRegalo - 0.4)
        regalo(im, 960, 820, 0.7 * er, t, seed=16520, texto="MÉXICO", abre=pr(t, tPais, tPais + 0.5))
        if t > tPais - 0.2:
            rotulo(im, "¡SE REGALÓ UN PAÍS!", 760, 990, 80, ROJO, t, seed=16530, esc=entra(t, tPais - 0.2))
            chispas(im, 960, 720, 240, t, tPais, seed=16535, col=AMARILLO)
    return im


TRAMOS = [(T_INI, realista), (T_BANDO, bando), (T_PLAN, plan), (T_TRUCO, truco), (T_TRAT, tratados), (T_CUMPLE, cumple)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
