# -*- coding: utf-8 -*-
"""REPASO EXPRÉS + PREGUNTAS 2 y 3: dos calendarios (16 SEP 1810 → 27 SEP 1821) con «SEP» encerrado en los dos y «MES PATRIO» con
papel picado → PREGUNTA 2 (pausa, cuatro tarjetas con «?», cuenta regresiva en el silencio) → RESPUESTA 2 (las cuatro etapas, HOY
ME GUSTA IR y los cuatro líderes, palomita) → PREGUNTA 3 (pausa, la conspiración y las tres garantías, cuenta regresiva) →
RESPUESTA 3 (Josefa Ortiz de Domínguez, R·I·U, «¡BIEN!»)."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import palomita
from personajes import AMARILLO, destello, kuri, pregunta
from utileria import flecha
from kit_amaya import (AZUL, CAFE, CREMA, DORADO, MORADO, ROJO, VERDE, cache, cam, chispas, cuenta, entra, fecha, letrero, papa,
                       pausa, tarjeta)
from piezas_fj import BLANCO_B, ROJO_B, VERDE_B, base

T_INI = T0("repaso")
tRep, t16, t27, tDos, tPatrio = ww("repaso", 0, "repaso"), ww("repaso", 0, "dieciseis"), ww("repaso", 0, "veintisiete"), \
    ww("repaso", 0, "dos"), ww("repaso", 0, "patrio")
T_P2, T_R2, T_P3, T_R3 = T0("preg2"), T0("resp2"), T0("preg3"), T0("resp3")
tP2, tEtapas, tQuien2, tFinP2 = ww("preg2", 0, "pausa"), ww("preg2", 0, "cuatro"), ww("preg2", 0, "quien"), FIN("preg2")
tR2 = [ww("resp2", 0, w) for w in ("inicio", "organizacion", "resistencia", "consumacion")]
tHMGI = [ww("resp2", 0, w) for w in ("hoy", "me", "gusta", "ir")]
tLid = [ww("resp2", 0, w) for w in ("hidalgo", "morelos", "guerrero", "iturbide")]
tP3, tQuien3, tGar3, tFinP3 = ww("preg3", 0, "otra"), ww("preg3", 0, "quien"), ww("preg3", 0, "cuales"), FIN("preg3")
tJos, tGarR, tRel, tInd, tUni, tBien = (ww("resp3", 0, "josefa"), ww("resp3", 0, "garantias"), ww("resp3", 0, "religion"),
                                        ww("resp3", 0, "independencia"), ww("resp3", 0, "union"), ww("resp3", 0, "bien"))
ETAPAS = [("INICIO", "hidalgo", "HIDALGO", "HOY", rgb("f6a6a0")), ("ORGANIZACIÓN", "morelos", "MORELOS", "ME", rgb("b8c7e8")),
          ("RESISTENCIA", "guerrero", "GUERRERO", "GUSTA", rgb("a8d8b0")), ("CONSUMACIÓN", "iturbide", "ITURBIDE", "IR", rgb("f4d38a"))]
XS = [240, 590, 940, 1290]
GAR = [("RELIGIÓN", BLANCO_B, TINTA), ("INDEPENDENCIA", VERDE_B, CREMA), ("UNIÓN", ROJO_B, CREMA)]


def picado(im, t, y=150, seed=17000):
    cols = [rgb("e35d4a"), rgb("f2c14e"), rgb("3f8f5a"), rgb("f3a7b8"), rgb("3f78c8"), rgb("9b6ad1")]
    linea(im, curva([(0, y - 60), (480, y - 30), (960, y - 20), (1440, y - 30), (1920, y - 60)], 10), 3, seed=seed, t=t)
    for k in range(13):
        x = 70 + 145 * k
        yy = y - 50 + 22 * math.sin(k * 0.48) * -1 + 6 * math.sin(t * 3 + k)
        forma(im, np.array([(x - 55, yy), (x + 55, yy), (x + 55, yy + 110), (x + 30, yy + 95), (x, yy + 115), (x - 30, yy + 95),
                            (x - 55, yy + 110)], np.float32), cols[k % 6], t, seed + 1 + k, tinta=2.5)
        forma(im, elipse(x, yy + 50, 16, 16), CREMA, t, seed + 20 + k, tinta=0)


def repaso(t):
    im = cache("i_rep", lambda: papel("calido")).copy()
    patrio = t > tPatrio - 0.4
    if patrio:
        picado(im, t)
    else:
        letrero(im, "REPASO EXPRÉS", 760, 140, 72, t, col=AMARILLO, seed=17100, esc=entra(t, tRep - 0.3), rot=-0.03)
    if t < t16 + 0.2:
        ek = entra(t, tRep - 0.2) * (1 - pr(t, t16 - 0.3, t16 + 0.2))
        kuri(im, 770, 540 + 14 * math.sin(t * 5), 2.0 * ek, t, cara="feliz", brazos=(1.4, 1.4))
        rotulo(im, "¡RÁPIDO!", 770, 820, 80, MORADO, t, seed=17105, esc=ek)
    e1 = entra(t, t16 - 0.3, 0.45)
    fecha(im, 400, 560, 1.15 * e1, t, "16", "SEP", "1810", seed=17110, col=rgb("e35d4a"))
    if e1 > 0.5:
        letrero(im, "EMPEZÓ", 400, 840, 54, t, col=CREMA, seed=17115, esc=e1)
    if t > t16 + 0.6:
        u = suave(pr(t, t16 + 0.6, t27 - 0.2))
        flecha(im, 620, 560, 620 + 300 * u + 1, 560, 40, t, rgb("8a7a5a"), seed=17120)
        if u > 0.6:
            letrero(im, "11 AÑOS", 770, 440, 46, t, col=CREMA, txt=ROJO, seed=17125, esc=entra(t, t16 + 1.2))
    e2 = entra(t, t27 - 0.3, 0.45)
    fecha(im, 1140, 560, 1.15 * e2, t, "27", "SEP", "1821", seed=17130, col=VERDE_B)
    if e2 > 0.5:
        letrero(im, "TERMINÓ", 1140, 840, 54, t, col=CREMA, seed=17135, esc=e2)
    if t > tDos - 0.3:
        u = pr(t, tDos - 0.3, tDos + 0.4)
        for k, x in enumerate((400, 1140)):
            n = max(2, int(40 * u))
            a = np.linspace(-0.5, -0.5 + 2 * math.pi * u, n)
            linea(im, np.stack([x + 230 * np.cos(a), 428 + 80 * np.sin(a)], 1), 8, MORADO, seed=17140 + k, t=t, punta=False)
    if patrio:
        rotulo(im, "¡SEPTIEMBRE, MES PATRIO!", 770, 990, 76, ROJO, t, seed=17150, esc=entra(t, tPatrio - 0.4))
    return im


def tarjetas_q(im, t, t_ap, revela=None, seed=17200):
    """Las cuatro tarjetas de las etapas: con «?» hasta que revela[k] las voltea."""
    for k, (et, foto_, nom, pal, col) in enumerate(ETAPAS):
        e = entra(t, t_ap + 0.12 * k)
        if e <= 0.01:
            continue
        x = XS[k]
        r = pr(t, revela[k] - 0.2, revela[k] + 0.15) if revela else 0.0
        sx = abs(math.cos(math.pi * r))                       # se voltea como carta
        cara = r > 0.5
        tarjeta(im, x, 560, 310 * e * sx + 2, 480 * e, t, col if cara else CREMA, seed + k * 7, rot=(k - 1.5) * 0.025)
        if not cara:
            pregunta(im, x, 580, 2.2 * e * sx + 0.01, t, seed=seed + 1 + k * 7)
        else:
            rotulo(im, str(k + 1), x, 370, 60 * sx + 1, ROJO, t, seed=seed + 2 + k * 7)
            rotulo(im, et, x, 768, (36 if len(et) > 9 else 46) * sx + 1, TINTA, t, seed=seed + 3 + k * 7, tinta=False)


def pregunta2(t):
    im = cache("i_p2", lambda: papel("frio")).copy()
    pausa(im, 300, 220, 0.75 * entra(t, tP2 - 0.3), t, seed=17300, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 70, ROJO, t, seed=17305, esc=entra(t, tP2 - 0.1))
    if t > tEtapas - 0.3:
        tarjetas_q(im, t, tEtapas - 0.3)
        letrero(im, "¿LAS 4 ETAPAS?", 560, 870, 56, t, col=CREMA, seed=17310, esc=entra(t, tEtapas - 0.3), rot=-0.03)
    if t > tQuien2 - 0.3:
        letrero(im, "¿Y SUS LÍDERES?", 1080, 960, 56, t, col=AMARILLO, seed=17315, esc=entra(t, tQuien2 - 0.3), rot=0.03)
    cuenta(im, 1640, 240, t, tFinP2 + 0.15, T_R2 + 0.1, s=0.75, seed=17320)
    return im


def respuesta2(t):
    im = cache("i_r2", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 300, 140, 56, t, col=VERDE, txt=CREMA, seed=17400, esc=entra(t, T_R2), rot=-0.04)
    tarjetas_q(im, t, T_R2 - 1.0, revela=tR2)
    for k, (et, foto_, nom, pal, col) in enumerate(ETAPAS):
        x = XS[k]
        if t > tHMGI[k] - 0.25:
            ep = entra(t, tHMGI[k] - 0.25)
            rotulo(im, pal, x, 880, 100 * ep + 1, rgb("c84a3a") if k % 2 == 0 else VERDE, t, seed=17410 + k, rot=(k - 1.5) * 0.03)
        if t > tLid[k] - 0.3:
            el = entra(t, tLid[k] - 0.3)
            cam(im, foto_, x, 540, 0.6 * el, t, nom, seed=90 + k)
            chispas(im, x, 560, 180, t, tLid[k], seed=17420 + k * 3, col=AMARILLO)
    if t > tLid[3] + 0.4:
        palomita(im, 1640, 300, 1.6 * entra(t, tLid[3] + 0.4), t, seed=17430, col=VERDE)
    return im


def pregunta3(t):
    im = cache("i_p3", lambda: papel("rosa")).copy()
    pausa(im, 300, 220, 0.75 * entra(t, tP3 - 0.3), t, seed=17500, texto=False)
    rotulo(im, "OTRA: PAUSA Y CONTESTA", 880, 200, 64, ROJO, t, seed=17505, esc=entra(t, tP3 - 0.1))
    if t > tQuien3 - 0.3:
        e = entra(t, tQuien3 - 0.3)
        tarjeta(im, 480, 560, 600 * e, 420 * e, t, CREMA, 17510, rot=-0.03)
        pregunta(im, 480, 520, 2.6 * e + 0.01, t, seed=17511)
        rotulo(im, "¿QUIÉN AVISÓ", 480, 690, 44 * e + 1, TINTA, t, seed=17512, tinta=False, rot=-0.03)
        rotulo(im, "DE LA CONSPIRACIÓN?", 480, 740, 40 * e + 1, TINTA, t, seed=17513, tinta=False, rot=-0.03)
    if t > tGar3 - 0.3:
        for k, (txt, col, tc) in enumerate(GAR):
            e = entra(t, tGar3 - 0.3 + 0.12 * k)
            x = 960 + 170 * k
            forma(im, elipse(x, 520, 75 * e + 1, 75 * e + 1), col, t, 17520 + k, tinta=4)
            rotulo(im, "?", x, 530, 100 * e + 1, ROJO if k == 0 else CREMA, t, seed=17523 + k)
        letrero(im, "¿LAS 3 GARANTÍAS?", 1130, 720, 50, t, col=AMARILLO, seed=17530, esc=entra(t, tGar3 - 0.2), rot=0.03)
    cuenta(im, 1130, 920, t, tFinP3 + 0.15, T_R3 + 0.1, s=0.7, seed=17540)
    return im


def respuesta3(t):
    im = cache("i_r3", lambda: papel("rosa")).copy()
    letrero(im, "RESPUESTA", 300, 140, 56, t, col=VERDE, txt=CREMA, seed=17600, esc=entra(t, T_R3), rot=-0.04)
    ej = entra(t, tJos - 0.3, 0.45)
    cam(im, "josefa", 420, 520, 0.95 * ej, t, "JOSEFA ORTIZ DE DOMÍNGUEZ", seed=95)
    chispas(im, 420, 520, 280, t, tJos, seed=17610, col=AMARILLO)
    if t > tJos + 1.0:
        letrero(im, "«LA CORREGIDORA»", 420, 900, 44, t, col=CREMA, txt=ROJO, seed=17615, esc=entra(t, tJos + 1.0), rot=0.03)
    for k, ((txt, col, tc), tk) in enumerate(zip(GAR, (tRel, tInd, tUni))):
        if t > tk - 0.25:
            e = entra(t, tk - 0.25)
            x = 950 + 190 * k
            forma(im, elipse(x, 480, 85 * e + 1, 85 * e + 1), col, t, 17620 + k, tinta=4)
            rotulo(im, "RIU"[k], x, 490, 110 * e + 1, ROJO if k == 0 else CREMA, t, seed=17623 + k)
            rotulo(im, txt, x, 620 + 50 * (k % 2), (34 if k == 1 else 42) * e + 1, TINTA, t, seed=17626 + k, tinta=False)
            chispas(im, x, 480, 140, t, tk, seed=17630 + k * 3, col=AMARILLO)
    if t > tBien - 0.3:
        eb = entra(t, tBien - 0.3)
        rotulo(im, "¡BIEN!", 1140, 860, 150, VERDE, t, seed=17640, esc=eb, rot=-0.05)
        palomita(im, 1420, 300, 1.4 * eb, t, seed=17645, col=VERDE)
    return im


TRAMOS = [(T_INI, repaso), (T_P2, pregunta2), (T_R2, respuesta2), (T_P3, pregunta3), (T_R3, respuesta3)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
