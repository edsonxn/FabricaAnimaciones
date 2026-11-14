# -*- coding: utf-8 -*-
"""PREGUNTA TRAMPA (túnel) + RESPUESTA 2.
preg2: PAUSA, señal amarilla «¡OJO: TRAMPA!» que se balancea, tarjeta «TÚNEL ?» y los tres botones; cuenta 3-2-1 en el silencio.
resp2: se enciende GRAVE → TÚ-NEL con TÚ encerrada (PENÚLTIMA · ÚLTIMA) y «SOLO 2 SÍLABAS» → la L final: «NO ES N, S NI VOCAL →
LLEVA TILDE» → la FOTO REAL del renglón de su cuaderno («3.- Túnel ... Esdrújula»), se tacha «Esdrújula» y se escribe GRAVE a
mano, «¡CORRÍGELO!» → truco: tres casillas «MÍNIMO 3 SÍLABAS» y TÚ-NEL, que solo llena dos."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from fondos_amaya import papel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import (CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, ficha, hoja, palabra
from piezas_fj import base
from plano_c import opciones
import personajes_ia as PI

T_INI = T0("preg2")
P, R = "preg2", "resp2"
tP2, tOjo, tTrampa, tTunel, tFinP2 = ww(P, 0, "pausa"), ww(P, 0, "ojo"), ww(P, 0, "trampa"), ww(P, 0, "tunel"), FIN(P)
tOp = [ww(P, 0, w) for w in ("aguda", "grave", "esdrujula")]
T_R2 = T0(R)
tGrave, tTu, tDos, tPen, tLleva, tEle, tVocal = (ww(R, 0, "grave"), ww(R, 0, "tu"), ww(R, 0, "dos"), ww(R, 0, "penultima"),
                                                 ww(R, 0, "lleva"), ww(R, 0, "ele"), ww(R, 0, "vocal"))
T_CUAD = ww(R, 1, "ojo") - 0.3
tCuad, tEsdr, tCorr, tTruco, tMin, tTres = (ww(R, 1, "cuaderno"), ww(R, 1, "esdrujula"), ww(R, 1, "corrijanlo"), ww(R, 1, "truco"),
                                            ww(R, 1, "minimo"), ww(R, 1, "tres"))


def senal(im, x, y, s, t, seed):
    rot = 0.12 * math.sin(t * 3)
    c, sn = math.cos(rot), math.sin(rot)
    pts = np.array([(0, -150), (140, 95), (-140, 95)], np.float32) * s
    pts = np.stack([x + pts[:, 0] * c - pts[:, 1] * sn, y + pts[:, 0] * sn + pts[:, 1] * c], 1)
    forma(im, pts, AMARILLO, t, seed, tinta=6 * s)
    rotulo(im, "!", x - 10 * s * sn, y + 10 * s, 150 * s, TINTA, t, seed=seed + 1, rot=rot)


def preg2(t):
    im = cache("d_p2", lambda: papel("rosa")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP2 - 0.3), t, seed=14000, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=14005, esc=entra(t, tP2 - 0.1))
    if t > tOjo - 0.3:
        e = entra(t, tOjo - 0.3)
        senal(im, 1340, 440, 0.9 * e + 0.01, t, 14010)
        rotulo(im, "¡OJO: TRAMPA!", 1340, 640, 52 * entra(t, tTrampa - 0.2) + 1, ROJO, t, seed=14012, rot=0.04)
    if t > tTunel - 0.3:
        e = entra(t, tTunel - 0.3)
        tarjeta(im, 640, 460, 560 * e, 230 * e, t, CREMA, 14020, rot=-0.02)
        rotulo(im, "TÚNEL", 590, 468, 120 * e + 1, MORADO, t, seed=14021, rot=-0.02)
        pregunta(im, 850, 460, 1.6 * e + 0.01, t, seed=14022)
    opciones(im, t, 790, tOp, seed=14030)
    cuenta(im, 1640, 250, t, tFinP2 + 0.15, T_R2 + 0.1, s=0.75, seed=14040)
    return im


def resp2(t):
    im = cache("d_r2", lambda: papel("rosa")).copy()
    letrero(im, "RESPUESTA", 300, 140, 56, t, col=VERDE, txt=CREMA, seed=14100, esc=entra(t, T_R2), rot=-0.04)
    opciones(im, t, 860, [T_R2 - 2] * 3, ok=1, t_ok=tGrave, seed=14030)
    chispas(im, 760, 860, 200, t, tGrave, seed=14105, col=AMARILLO)
    palabra(im, ["TÚ", "NEL"], 560, 400, 120, t, tonica=0, t_ap=[tTu - 0.2, tTu + 0.4], t_ton=tTu + 0.1, seed=14110,
            etiquetas=["PENÚLTIMA", "ÚLTIMA"], t_eti=tPen - 0.4)
    if t > tDos - 0.3:
        letrero(im, "¡SOLO 2 SÍLABAS!", 560, 730, 52, t, col=AMARILLO, seed=14120, esc=entra(t, tDos - 0.3), rot=0.03)
    if t > tEle - 0.4:
        e = entra(t, tEle - 0.4)
        ficha(im, "L", 1100, 360, 90, t, rgb("fff2c0"), 14130, esc=e)
        rotulo(im, "TERMINA EN L", 1100, 230, 50 * e + 1, MORADO, t, seed=14131, tinta=False)
        if t > tEle + 0.5:
            rotulo(im, "NO ES N, S NI VOCAL", 1100, 500, 44 * entra(t, tEle + 0.5) + 1, ROJO, t, seed=14132, tinta=False)
        if t > tVocal + 0.2:
            letrero(im, "→ LLEVA TILDE", 1100, 600, 46, t, col=VERDE, txt=CREMA, seed=14133, esc=entra(t, tVocal + 0.2), rot=-0.03)
    return im


def cuaderno(t):
    im = cache("d_cu", lambda: papel("calido")).copy()
    letrero(im, "EN EL CUADERNO", 330, 120, 54, t, col=CREMA, txt=TURQ, seed=14200, esc=entra(t, T_CUAD), rot=-0.04)
    e = entra(t, tCuad - 0.4, 0.5)
    esc = 1.7
    PI.pegar(im, hoja("tunel"), 760, 330, esc * e, -0.015, marco=14, t=t, seed=14210)
    if t > tEsdr + 0.2:
        u = suave(pr(t, tEsdr + 0.2, tEsdr + 0.6))
        x0, x1, y = 760 - 400 * esc + 505 * esc, 760 - 400 * esc + 700 * esc, 330.0
        linea(im, [(x0, y + 4), (x0 + (x1 - x0) * u, y - 6)], 12, ROJO, seed=14220, t=t)
        linea(im, [(x0, y + 22), (x0 + (x1 - x0) * u, y + 12)], 9, ROJO, seed=14221, t=t)
    if t > tCorr - 0.4:
        e2 = entra(t, tCorr - 0.4)
        rotulo(im, "GRAVE", 1150, 175, 84 * e2 + 1, ROJO, t, seed=14230, rot=-0.08, fuente="segoeprb.ttf", tinta=False)
        rotulo(im, "¡CORRÍJANLO!", 600, 520, 72 * e2 + 1, ROJO, t, seed=14231, rot=0.03)
    if t > tTruco - 0.4:
        letrero(im, "TRUCO", 300, 640, 52, t, col=AMARILLO, seed=14240, esc=entra(t, tTruco - 0.4), rot=-0.04)
        rotulo(im, "ESDRÚJULA = MÍNIMO 3 SÍLABAS", 820, 650, 54 * entra(t, tMin - 0.3) + 1, MORADO, t, seed=14241, tinta=False)
        for k in range(3):
            e3 = entra(t, tTres - 0.3 + 0.15 * k)
            forma(im, rrect(560 + 200 * k, 830, 170 * e3 + 1, 120 * e3 + 1, 14), CREMA, t, 14250 + k, tinta=4)
            if k < 2 and t > tTres + 0.6:
                ficha(im, ["TÚ", "NEL"][k], 560 + 200 * k, 830, 54, t, rgb("fde0dc") if k == 0 else CREMA, 14260 + k * 4,
                      esc=entra(t, tTres + 0.6 + 0.2 * k))
        if t > tTres + 1.2:
            rotulo(im, "?", 960, 838, 90, GRIS, t, seed=14270)
            marca_x(im, 1180, 830, 1.1 * entra(t, tTres + 1.2), t, seed=14271)
    return im


TRAMOS = [(T_INI, preg2), (T_R2, resp2), (T_CUAD, cuaderno)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
