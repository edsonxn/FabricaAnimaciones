# -*- coding: utf-8 -*-
"""EL TRUCO: línea 1810 → 1821 («11 AÑOS») y cuatro tarjetas (INICIO, ORGANIZACIÓN, RESISTENCIA, CONSUMACIÓN) → el líder de cada
una en camafeo → letras gigantes H · M · G · I → «HOY ME GUSTA IR» debajo → «repítelo conmigo»: cada palabra brinca cuando papá
la dice y Kuri festeja."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from personajes import AMARILLO, destello, kuri, corazon
from utileria import flecha
from kit_amaya import (AZUL, CAFE, CREMA, DORADO, MORADO, ROJO, VERDE, cache, cam, entra, letrero, papa, tarjeta)

T_INI = T0("truco")
C = "truco"
tTruco, tOnce, tCuatro = ww(C, 0, "truco"), ww(C, 0, "once"), ww(C, 0, "cuatro")
tEt = [ww(C, 0, "inicio"), ww(C, 0, "organizacion"), ww(C, 0, "resistencia"), ww(C, 0, "consumacion")]
tLider = ww(C, 1, "lider")
tLid = [ww(C, 1, "hidalgo"), ww(C, 1, "morelos"), ww(C, 1, "guerrero"), ww(C, 1, "iturbide")]
tHache = ww(C, 1, "hache")
tPegue = ww(C, 1, "pegue")
tFrase = [ww(C, 1, "hoy"), ww(C, 1, "me", 0), ww(C, 1, "gusta"), ww(C, 1, "ir")]
tRep = ww(C, 2, "repitelo")
tDice = [ww(C, 2, "hoy"), ww(C, 2, "me"), ww(C, 2, "gusta"), ww(C, 2, "ir")]

ETAPAS = [("INICIO", "hidalgo", "HIDALGO", "H", "HOY", rgb("f6a6a0")),
          ("ORGANIZACIÓN", "morelos", "MORELOS", "M", "ME", rgb("b8c7e8")),
          ("RESISTENCIA", "guerrero", "GUERRERO", "G", "GUSTA", rgb("a8d8b0")),
          ("CONSUMACIÓN", "iturbide", "ITURBIDE", "I", "IR", rgb("f4d38a"))]
XS = [250, 610, 970, 1330]


def _fondo():
    im = papel("calido")
    _manchas(im, rgb("f2c9a0"), 7, 61, r=(260, 420), alfa=0.16)
    return im


def cuadro_crudo(t):
    im = cache("fondo_d", _fondo).copy()
    lider = t > tLider - 0.4
    # arriba: el truco y la línea de tiempo (luego, el título de los líderes)
    if not lider:
        letrero(im, "EL TRUCO MÁS IMPORTANTE", 790, 90, 56, t, col=AMARILLO, seed=12000, esc=entra(t, tTruco - 0.2))
        if t > tTruco + 0.2:
            u = suave(pr(t, tTruco + 0.2, tOnce + 0.3))
            linea(im, [(240, 200), (240 + 1100 * u, 200)], 10, ROJO, seed=12001, t=t)
            letrero(im, "1810", 200, 200, 44, t, col=CREMA, seed=12002, esc=entra(t, tTruco + 0.2))
            if u > 0.95:
                letrero(im, "1821", 1380, 200, 44, t, col=CREMA, seed=12003)
            letrero(im, "11 AÑOS", 790, 200, 50, t, col=ROJO, txt=CREMA, seed=12004, esc=entra(t, tOnce))
    else:
        letrero(im, "CADA ETAPA, SU LÍDER", 790, 90, 56, t, col=AMARILLO, seed=12010, esc=entra(t, tLider - 0.4))
    for k, (etapa, foto_, nom, letra, palabra, col) in enumerate(ETAPAS):
        x = XS[k]
        e = entra(t, tEt[k] - 0.3)
        if e <= 0.01:
            continue
        brinca = 0.0
        if t > tRep:
            brinca = math.exp(-((t - tDice[k] - 0.15) / 0.25) ** 2)
        tarjeta(im, x, 600 - 30 * brinca, 330 * e, 600 * e, t, col, 12100 + k * 9, rot=(k - 1.5) * 0.025)
        rotulo(im, str(k + 1), x - 120, 340, 64 * e + 1, ROJO, t, seed=12101 + k * 9)
        rotulo(im, etapa, x, 840 - 30 * brinca, (40 if len(etapa) > 9 else 50) * e + 1, TINTA, t, seed=12102 + k * 9, tinta=False)
        if t > tLid[k] - 0.3:
            cam(im, foto_, x, 560 - 30 * brinca, 0.62 * entra(t, tLid[k] - 0.3), t, "", seed=40 + k)
        if t > tHache - 0.3 + 0.35 * k:
            el = entra(t, tHache - 0.3 + 0.35 * k)
            forma(im, elipse(x + 120, 340 - 30 * brinca, 62 * el + 1, 62 * el + 1), ROJO, t, 12105 + k * 9, tinta=4)
            rotulo(im, letra, x + 120, 346 - 30 * brinca, 80 * el + 1, CREMA, t, seed=12106 + k * 9)
        if t > tFrase[k] - 0.25:
            ep = entra(t, tFrase[k] - 0.25)
            rotulo(im, palabra, x, 990 - 40 * brinca, (96 + 40 * brinca) * ep + 1, rgb("c84a3a") if k % 2 == 0 else VERDE, t,
                   seed=12107 + k * 9, rot=(k - 1.5) * 0.03)
            if brinca > 0.5:
                destello(im, x + 110, 930, 0.9, t, seed=12108 + k * 9)
    if t > tPegue - 0.3 and t < tRep - 0.2:
        rotulo(im, "PARA QUE", 1720, 380, 46, TINTA, t, seed=12200, esc=entra(t, tPegue - 0.3), tinta=False)
        rotulo(im, "SE TE PEGUE:", 1720, 440, 46, TINTA, t, seed=12201, esc=entra(t, tPegue - 0.2), tinta=False)
    if t > tRep - 0.3:
        letrero(im, "¡REPÍTELO", 1720, 300, 48, t, col=VERDE, txt=CREMA, seed=12210, esc=entra(t, tRep - 0.3), rot=0.05)
        letrero(im, "CONMIGO!", 1720, 390, 48, t, col=VERDE, txt=CREMA, seed=12215, esc=entra(t, tRep - 0.1), rot=0.05)
        kuri(im, 1720, 540 + 12 * math.sin(t * 8), 1.5 * entra(t, tRep), t, cara="feliz",
             brazos=(1.6 + 0.3 * math.sin(t * 9), 1.6 - 0.3 * math.sin(t * 9)))
    papa(im, t, 1750, H + 30, alto=410)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
