# -*- coding: utf-8 -*-
"""ETAPA 2 · ORGANIZACIÓN (1811-1815, Morelos): «2 ORGANIZACIÓN» → Morelos alumno de Hidalgo (flecha maestro → alumno), el
pañuelo en la cabeza y el «¡AY!» del dolor → ejército entrenado en filas + el sitio de Cuautla con el contador de días (72) →
pergamino de los Sentimientos de la Nación 1813 (LIBRES · SIN ESCLAVITUD · SIN CASTAS) y la Constitución de Apatzingán 1814 →
«SIERVO DE LA NACIÓN» y 1815 fusilado → Leona Vicario: monedas y una carta secreta que vuelan a los insurgentes, «¡ESPÍA!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import palomita
from personajes import AMARILLO, destello, mareo
from utileria import flecha
from kit_amaya import AZUL, CAFE, CREMA, DORADO, GRIS, ROJO, VERDE, cache, cam, chispas, entra, gente, letrero, papa, tarjeta
from piezas_fj import base, cabecera, fuerte, moneda, pergamino, sobre

T_INI = T0("organizacion")
C = "organizacion"
tDos, tOrg, tMor, tMil, tAlumno, tHid, tPan, tDolia = (ww(C, 0, "dos"), ww(C, 0, "organizacion"), ww(C, 0, "jose"),
                                                       ww(C, 0, "mil"), ww(C, 0, "alumno"), ww(C, 0, "hidalgo"),
                                                       ww(C, 0, "panuelo"), ww(C, 0, "dolia"))
tBien, tEjer, tEntr, tAguanto, tDosM, tSitio, tCuautla = (ww(C, 1, "organizado"), ww(C, 1, "ejercito"), ww(C, 1, "entrenado"),
                                                          ww(C, 1, "aguanto"), ww(C, 1, "dos"), ww(C, 1, "sitio"),
                                                          ww(C, 1, "cuautla"))
t1813, tSent, tLibres, tEscl, tCastas, t1814, tConst, tApatz = (ww(C, 2, "mil"), ww(C, 2, "sentimientos"), ww(C, 2, "libres"),
                                                               ww(C, 2, "esclavitud"), ww(C, 2, "castas"), ww(C, 2, "mil", 1),
                                                               ww(C, 2, "constitucion"), ww(C, 2, "apatzingan"))
tPidio, tSiervo, t1815, tFus = ww(C, 3, "pidio"), ww(C, 3, "siervo"), ww(C, 3, "mil"), ww(C, 3, "fusilaron")
tLeona, tDinero, tInsurg, tInfo, tSecreto, tEspia = (ww(C, 4, "leona"), ww(C, 4, "dinero"), ww(C, 4, "insurgentes"),
                                                    ww(C, 4, "informacion"), ww(C, 4, "secreto"), ww(C, 4, "espia"))
T_EJ = tBien - 0.6
T_SENT = t1813 - 0.5
T_SIER = tPidio - 0.5
T_LEO = tLeona - 0.7
COL = rgb("b8c7e8")


def cab(im, t):
    cabecera(im, t, "2 · ORGANIZACIÓN · 1811-1815", COL, 14000)


def morelos(t):
    im = cache("f_mor", lambda: papel("frio")).copy()
    cab(im, t)
    # «2 ORGANIZACIÓN» grande mientras lo dice
    if t < tAlumno - 0.3:
        e = entra(t, tDos - 0.3)
        rotulo(im, "2", 1150, 400, 300, COL, t, seed=14010, esc=e)
        rotulo(im, "ORGANIZACIÓN", 1150, 660, 120, AZUL, t, seed=14011, esc=entra(t, tOrg - 0.2))
        letrero(im, "1811 – 1815", 1150, 820, 60, t, col=CREMA, seed=14012, esc=entra(t, tMil - 0.2))
    em = entra(t, tMor - 0.3, 0.45)
    cam(im, "morelos", 420, 470, 1.0 * em, t, "JOSÉ MARÍA MORELOS", seed=60)
    if t > tAlumno - 0.4:
        # Hidalgo maestro (chico, arriba a la derecha) → flecha → Morelos alumno
        eh = entra(t, tAlumno - 0.4)
        cam(im, "hidalgo", 1180, 330, 0.55 * eh, t, "HIDALGO", seed=61)
        if eh > 0.5:
            letrero(im, "MAESTRO", 1180, 560, 44, t, col=AMARILLO, seed=14020, esc=eh, rot=0.04)
            u = suave(pr(t, tAlumno, tAlumno + 0.6))
            if u > 0.05:
                flecha(im, 1020, 360, 1020 - 330 * u, 400 + 40 * u, 34, t, ROJO, seed=14025)
            letrero(im, "ALUMNO", 760, 780, 50, t, col=CREMA, txt=AZUL, seed=14030, esc=entra(t, tAlumno + 0.2), rot=-0.04)
    if t > tPan - 0.3:
        ep = entra(t, tPan - 0.3)
        # anillo que señala el pañuelo y su etiqueta
        linea(im, curva([(330, 300), (420, 255), (520, 300), (500, 345), (420, 360), (340, 345)], 8, True), 7 * ep + 0.1, ROJO,
              seed=14040, t=t, cerrado=True, punta=False)
        letrero(im, "EL PAÑUELO", 690, 230, 48, t, col=CREMA, txt=ROJO, seed=14045, esc=ep, rot=-0.05)
        if t > tDolia - 0.3:
            ed = entra(t, tDolia - 0.3)
            rotulo(im, "¡AY!", 160, 250, 96, ROJO, t, seed=14050, esc=ed, rot=-0.15)
            mareo(im, 420, 270, 1.6, t, seed=14055)
    return im


def ejercito(t):
    im = cache("f_ej", lambda: papel("calido")).copy()
    forma(im, np.array([(0, 860), (W, 850), (W, H), (0, H)], np.float32), rgb("d9c08e"), 0, 14100, tinta=0)
    cab(im, t)
    letrero(im, "BIEN ORGANIZADO", 520, 200, 60, t, col=AMARILLO, seed=14105, esc=entra(t, tBien - 0.3))
    # filas de soldados que marchan al mismo paso (todos con el mismo uniforme)
    ee = entra(t, tEjer - 0.3)
    if ee > 0.01:
        paso = abs(math.sin(t * 6))
        for fila in range(3):
            for c in range(5):
                x = 170 + 150 * c + 40 * fila
                y = 470 + 140 * fila - 14 * paso
                gente(im, x, y, 2.0 * ee + 0.01, t, seed=140 + fila * 5 + c, col=rgb("3f6a8f"), cara="normal")
                linea(im, [(x + 50, y + 70), (x + 58, y - 70)], 7, CAFE, seed=14110 + fila * 5 + c, t=t)
        letrero(im, "EJÉRCITO ENTRENADO", 520, 940, 54, t, col=CREMA, seed=14130, esc=entra(t, tEntr - 0.2))
    # el sitio de Cuautla: el pueblo amurallado aguanta y el contador de días sube hasta 72
    es = entra(t, tAguanto - 0.4, 0.45)
    if es > 0.01:
        fuerte(im, 1220, 720, 0.85 * es, t, seed=14140)
        if t > tSitio - 0.3:
            letrero(im, "SITIO DE CUAUTLA", 1220, 210, 56, t, col=CREMA, txt=AZUL, seed=14150, esc=entra(t, tSitio - 0.3))
        dia = int(1 + 71 * suave(pr(t, tAguanto, tCuautla + 0.4)))
        tarjeta(im, 1220, 360, 300 * es, 110 * es, t, CREMA, 14160, rot=0.03)
        rotulo(im, f"DÍA {dia}", 1220, 364, 70 * es + 1, ROJO, t, seed=14161, tinta=False, rot=0.03)
        if t > tDosM - 0.2:
            rotulo(im, "¡+ DE 2 MESES!", 1220, 920, 76, ROJO, t, seed=14170, esc=entra(t, tDosM - 0.2))
    return im


def sentimientos(t):
    im = cache("f_sent", lambda: papel("sepia")).copy()
    cab(im, t)
    e = entra(t, tSent - 0.5, 0.45)
    pergamino(im, 600, 560, 760, 640, t, 14200, esc=e)
    if e > 0.5:
        letrero(im, "1813", 260, 230, 56, t, col=ROJO, txt=CREMA, seed=14205, esc=entra(t, t1813 - 0.2), rot=-0.06)
        rotulo(im, "SENTIMIENTOS", 600, 330, 64, CAFE, t, seed=14210, esc=entra(t, tSent - 0.2), tinta=False)
        rotulo(im, "DE LA NACIÓN", 600, 400, 56, CAFE, t, seed=14211, esc=entra(t, tSent + 0.2), tinta=False)
        for k, (txt, tk) in enumerate((("LIBRES", tLibres), ("SIN ESCLAVITUD", tEscl), ("SIN CASTAS", tCastas))):
            if t > tk - 0.25:
                ek = entra(t, tk - 0.25)
                y = 520 + 110 * k
                palomita(im, 330, y, 0.55 * ek, t, seed=14220 + k, col=VERDE)
                rotulo(im, txt, 640, y + 4, 60, TINTA, t, seed=14225 + k, esc=ek, tinta=False)
                if t < tk + 0.6:
                    destello(im, 330, y - 30, 0.8, t, seed=14230 + k, col=AMARILLO)
    # Morelos lo escribe (a la derecha) hasta que sale el libro de 1814
    if tSent - 0.4 < t < t1814 - 0.1:
        em = entra(t, tSent - 0.4) * (1 - pr(t, t1814 - 0.5, t1814 - 0.1))
        cam(im, "morelos", 1230, 470, 0.8 * em, t, "LO ESCRIBIÓ MORELOS", seed=64)
        if em > 0.5:
            a = t * 9
            px, py = 1400 + 18 * math.sin(a), 700 + 8 * math.cos(a * 1.3)
            linea(im, [(px, py), (px + 70, py - 150)], 9, rgb("f4f0e6"), seed=14260, t=t)
            linea(im, [(px, py), (px + 6, py - 14)], 4, TINTA, seed=14261, t=t)
    # 1814: el libro de la Constitución de Apatzingán
    if t > t1814 - 0.3:
        ec = entra(t, t1814 - 0.3, 0.45)
        tarjeta(im, 1250, 560, 360 * ec, 470 * ec, t, rgb("8a3a3a"), 14240, rot=0.06)
        forma(im, rrect(1250, 560, 300 * ec, 410 * ec, 10, 0.06), rgb("a54a44"), t, 14241, tinta=2.5)
        rotulo(im, "1814", 1250, 420, 70 * ec + 1, DORADO, t, seed=14242, rot=0.06, tinta=False)
        if t > tConst - 0.2:
            rotulo(im, "CONSTITUCIÓN", 1250, 540, 46 * ec + 1, CREMA, t, seed=14243, rot=0.06, tinta=False)
            rotulo(im, "DE", 1250, 600, 40 * ec + 1, CREMA, t, seed=14244, rot=0.06, tinta=False)
        if t > tApatz - 0.2:
            letrero(im, "APATZINGÁN", 1250, 860, 58, t, col=AMARILLO, seed=14245, esc=entra(t, tApatz - 0.2), rot=-0.03)
            chispas(im, 1250, 560, 300, t, tApatz, seed=14250, col=AMARILLO)
    return im


def siervo(t):
    im = cache("f_sier", lambda: papel("frio")).copy()
    cab(im, t)
    cam(im, "morelos", 520, 500, 1.05, t, "MORELOS", seed=62)
    if t > tSiervo - 0.3:
        es = entra(t, tSiervo - 0.3)
        # banda cruzada con el apodo que pidió
        forma(im, rrect(1080, 330, 720 * es + 1, 120 * es + 1, 20, -0.05), AZUL, t, 14300, tinta=4.5)
        rotulo(im, "«SIERVO DE LA NACIÓN»", 1080, 334, 52 * es + 1, CREMA, t, seed=14301, rot=-0.05)
        for k in range(3):
            destello(im, 760 + 300 * k, 230 + 20 * (k % 2), 0.7 * es, t, seed=14305 + k, col=AMARILLO)
    if t > t1815 - 0.3:
        letrero(im, "1815", 1080, 560, 72, t, col=CREMA, seed=14310, esc=entra(t, t1815 - 0.3), rot=0.04)
    if t > tFus - 0.3:
        letrero(im, "TAMBIÉN FUSILADO", 1080, 720, 64, t, col=CREMA, txt=ROJO, seed=14315, esc=entra(t, tFus - 0.3), rot=-0.03)
    return im


def leona(t):
    im = cache("f_leo", lambda: papel("rosa")).copy()
    _manchas(im, rgb("f3b8c8"), 0, 1)
    cab(im, t)
    letrero(im, "¡NO LA OLVIDES!", 420, 200, 52, t, col=AMARILLO, seed=14400, esc=entra(t, tLeona - 0.6), rot=-0.04)
    cam(im, "leona", 420, 530, 0.95 * entra(t, tLeona - 0.3, 0.45), t, "LEONA VICARIO", seed=63)
    # los insurgentes, a la derecha
    for k in range(4):
        gente(im, 1130 + 110 * k, 680 + 30 * (k % 2), 2.2, t, seed=170 + k, col=rgb("6a8a4a"))
    letrero(im, "INSURGENTES", 1290, 870, 48, t, col=CREMA, txt=VERDE, seed=14410, esc=entra(t, tInsurg - 0.3))
    # monedas que vuelan de Leona a una bolsa de los insurgentes
    if t > tDinero - 0.3:
        eb = entra(t, tDinero - 0.3)
        llena = pr(t, tDinero + 0.5, tDinero + 1.6)
        forma(im, curva([(930, 820), (910, 740), (960, 700), (1020, 700), (1070, 740), (1050, 820)], 8, True) * 1.0
              if eb > 0.99 else elipse(990, 770, 70 * eb + 1, 60 * eb + 1), rgb("c9a46a"), t, 14415, tinta=4)
        if llena > 0:
            rotulo(im, "$", 990, 778, 60 * (0.7 + 0.3 * llena), rgb("8a6a1e"), t, seed=14416, tinta=False)
        for k in range(5):
            u = pr(t, tDinero - 0.3 + 0.15 * k, tDinero + 0.8 + 0.15 * k)
            if 0 < u:
                x = 640 + (340 + 14 * k) * e_out(u)
                y = 520 - 260 * math.sin(math.pi * u) + 230 * u
                if u < 1:
                    moneda(im, x, y, 1.0, t, seed=14420 + k)
        if t < tInfo - 0.4:
            letrero(im, "DINERO", 860, 330, 46, t, col=DORADO, seed=14430, esc=entra(t, tDinero - 0.2), rot=0.05)
    # y una carta secreta
    if t > tInfo - 0.4:
        u = e_out(pr(t, tInfo - 0.4, tSecreto + 0.3))
        sobre(im, 660 + 640 * u, 470 - 200 * math.sin(math.pi * u), 1.1, t, seed=14440, rot=0.4 * math.sin(t * 3))
        if t > tSecreto - 0.2:
            letrero(im, "EN SECRETO", 1300, 230, 50, t, col=CREMA, txt=ROJO, seed=14450, esc=entra(t, tSecreto - 0.2))
    if t > tEspia - 0.3:
        ee = entra(t, tEspia - 0.3)
        forma(im, rrect(820, 860, 520 * ee + 1, 140 * ee + 1, 14, -0.12), ROJO, t, 14460, tinta=5, alfa=0.92)
        rotulo(im, "¡ESPÍA!", 820, 866, 100 * ee + 1, CREMA, t, seed=14461, rot=-0.12)
    return im


TRAMOS = [(T_INI, morelos), (T_EJ, ejercito), (T_SENT, sentimientos), (T_SIER, siervo), (T_LEO, leona)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
