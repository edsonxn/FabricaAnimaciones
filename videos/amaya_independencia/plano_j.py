# -*- coding: utf-8 -*-
"""CIERRE: papá grande a la derecha le habla a Amaya → «¡LISTA PARA EL LUNES!» → noche: luna, estrellas y la cama con «REPASO
ANTES DE DORMIR» (Zzz) y «SE TE QUEDA MEJOR» → «¡TÚ PUEDES, AMAYA!» → corazones que suben con «TE QUIERO MUCHO, HIJA» → «¡MUCHO
ÉXITO EN TU EXAMEN!» con chispas."""
import math

import numpy as np

from acuarela import H, W, TINTA, brillo, degradado, e_out, elipse, forma, pr, rgb, rotulo, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import palomita, estrella
from personajes import AMARILLO, corazon, destello
from kit_amaya import CREMA, MORADO, ROJO, VERDE, cache, chispas, entra, letrero, papa, tarjeta
from piezas_fj import base, cama, luna, zzz

T_INI = T0("cierre")
C = "cierre"
tAmaya, tLunes, tLista, tAntes, tDormir, tRepaso, tQueda = (ww(C, 0, "amaya"), ww(C, 0, "lunes"), ww(C, 0, "lista"),
                                                          ww(C, 0, "antes"), ww(C, 0, "dormir"), ww(C, 0, "repaso"),
                                                          ww(C, 0, "queda"))
tGanas, tPuedes, tQuiero, tHija, tExito, tExamen = (ww(C, 1, "echale"), ww(C, 1, "puedes"), ww(C, 1, "quiero"), ww(C, 1, "hija"),
                                                    ww(C, 1, "mucho", 1), ww(C, 1, "examen"))
T_NOCHE = tAntes - 0.5
T_ANIMO = tGanas - 0.5
ROSA_F = rgb("f3a7b8")


def _noche():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("1f2850"), rgb("3a3f78"))
    _manchas(im, rgb("4a4f90"), 8, 77, r=(240, 420), alfa=0.25)
    return im


def lista(t):
    im = cache("j_lis", lambda: papel("rosa")).copy()
    letrero(im, "AMAYA", 560, 260, 110, t, col=AMARILLO, seed=18000, esc=entra(t, tAmaya - 0.3), rot=-0.04)
    if t > tLunes - 0.3:
        rotulo(im, "EL LUNES...", 560, 500, 90, MORADO, t, seed=18005, esc=entra(t, tLunes - 0.3))
    if t > tLista - 0.3:
        el = entra(t, tLista - 0.3)
        rotulo(im, "¡VAS A ESTAR LISTA!", 560, 680, 92, VERDE, t, seed=18010, esc=el, rot=-0.03)
        palomita(im, 560, 880, 1.3 * el, t, seed=18015, col=VERDE)
        for k in range(5):
            destello(im, 160 + 200 * k, 400 + 90 * (k % 2), 0.6 * el, t, seed=18020 + k, col=AMARILLO)
    return im


def noche(t):
    im = cache("j_noc", _noche).copy()
    for k in range(18):
        x, y = (97 * k * 7) % 1180 + 40, (53 * k * 11) % 360 + 60
        estrella(im, x, y, 5 + 3 * (k % 3), t, rgb("fff6c8"), f=0.5 + 0.5 * math.sin(t * 3 + k), seed=18100 + k)
    luna(im, 1250, 230, 110, t, seed=18120)
    ec = entra(t, tDormir - 0.6, 0.45)
    cama(im, 600, 760, 1.1 * ec, t, seed=18130)
    if ec > 0.5:
        # Amaya dormida en la almohada
        from personajes_ia import PELO_N
        from personajes import PIEL
        from acuarela import linea, curva
        hx, hy = 600 - 200 * 1.1 * ec, 760 - 70 * 1.1 * ec
        forma(im, elipse(hx, hy, 62, 58), PELO_N, t, 18170, tinta=3.5)
        forma(im, elipse(hx + 8, hy + 8, 46, 44), PIEL, t, 18171, tinta=3.5)
        for d in (-1, 1):
            linea(im, curva([(hx + 8 + d * 18 - 9, hy + 8), (hx + 8 + d * 18, hy + 14), (hx + 8 + d * 18 + 9, hy + 8)], 4), 3,
                  seed=18172 + d, t=t, punta=False)
        forma(im, elipse(hx + 8, hy + 30, 6, 4 + 2 * math.sin(t * 2)), rgb("8a3a3a"), t, 18175, tinta=0)
    if t > tDormir - 0.3:
        zzz(im, hx + 60 if ec > 0.5 else 420, 640, t, 2.0, seed=18140)
        letrero(im, "ANTES DE DORMIR", 600, 380, 62, t, col=CREMA, txt=MORADO, seed=18145, esc=entra(t, tDormir - 0.3), rot=-0.03)
    if t > tRepaso - 0.3:
        # el repaso en una tableta junto a la cama
        er = entra(t, tRepaso - 0.3)
        tarjeta(im, 1120, 600, 300 * er, 200 * er, t, rgb("2a2f40"), 18150, rot=0.05)
        forma(im, elipse(1120, 600, 110 * er + 1, 70 * er + 1, 0.05), rgb("fbf3df"), t, 18151, tinta=0, alfa=0.85)
        rotulo(im, "REPASO", 1120, 606, 48 * er + 1, ROJO, t, seed=18152, rot=0.05, tinta=False)
        brillo(im, 1120, 600, 220 * er, rgb("bfe0ff"), 0.4)
    if t > tQueda - 0.3:
        rotulo(im, "¡SE TE QUEDA MEJOR!", 760, 990, 80, AMARILLO, t, seed=18160, esc=entra(t, tQueda - 0.3))
    return im


def animo(t):
    im = cache("j_ani", lambda: papel("calido")).copy()
    _manchas(im, ROSA_F, 0, 1)
    if t > tQuiero - 0.3:
        for k in range(9):
            v = ((t - tQuiero) * 0.35 + k / 9) % 1
            x = 130 + 140 * k + 30 * math.sin(t * 2 + k)
            corazon(im, x, 1000 - 900 * v, (1.4 + 0.6 * (k % 3)) * min(1, (t - tQuiero) * 2 + 0.1), t, seed=18210 + k,
                    col=(ROSA_F, rgb("e35d6a"), rgb("f08a9a"))[k % 3])
    ep = entra(t, tPuedes - 0.4, 0.45)
    if ep > 0.01:
        rotulo(im, "¡TÚ PUEDES,", 620, 300, 120, ROJO, t, seed=18200, esc=ep, rot=-0.04)
        rotulo(im, "AMAYA!", 620, 460, 150, MORADO, t, seed=18201, esc=entra(t, tPuedes - 0.2), rot=0.03)
    else:
        rotulo(im, "¡ÉCHALE GANAS!", 620, 380, 110, VERDE, t, seed=18205, esc=entra(t, tGanas - 0.3))
    if t > tQuiero - 0.3:
        letrero(im, "TE QUIERO MUCHO, HIJA", 620, 650, 64, t, col=CREMA, txt=ROJO, seed=18230, esc=entra(t, tQuiero - 0.3))
    if t > tExito - 0.3:
        ee = entra(t, tExito - 0.3)
        letrero(im, "¡MUCHO ÉXITO EN TU EXAMEN!", 640, 860, 66, t, col=AMARILLO, seed=18240, esc=ee, rot=-0.02)
        chispas(im, 640, 860, 420, t, tExamen, seed=18245, col=AMARILLO, n=10)
    return im


TRAMOS = [(T_INI, lista), (T_NOCHE, noche), (T_ANIMO, animo)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    # papá grande a la derecha (se despide de cerca); en la noche se hace chico para no tapar la luna
    noche_ = pr(t, T_NOCHE, T_NOCHE + 0.6) * (1 - pr(t, T_ANIMO, T_ANIMO + 0.6))
    g = suave(pr(t, T_INI, T_INI + 1.0)) * (1 - suave(noche_))     # crece al empezar el cierre
    papa(im, t, 1770 - 210 * g, H + 30 + 10 * g, alto=330 + 430 * g)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
