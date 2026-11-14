# -*- coding: utf-8 -*-
"""GANCHO: tablero de corcho; el profe Tilde sube desde abajo («¡HOLA OTRA VEZ, SEXTO B!») → llegan volando las 5 FOTOS REALES del
cuaderno de mate y se clavan con chinchetas → banda «¡REPASO DE MATE!» → cinco notitas (DECIMALES 0.8 · NÚMEROS GRANDES 7,735,923 ·
TRIÁNGULOS · PLANO CARTESIANO · FRACCIONES ¼), una por palabra → «¡Y SÍ: PIZZA!» con una pizza que cae → PAUSA Y CONTESTA,
«¡EN VOZ ALTA!», «¿LISTOS?», «¡ARRANCAMOS!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import ww
from fondos_amaya import papel, _manchas
from iconos_ia import palomita
from personajes import AMARILLO, corazon, destello
from kit_amaya import (AZUL, CREMA, MORADO, ROJO, VERDE, cache, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, polaroid
from piezas_mt import AZUL_C, LILA_C, MIEL, ROSA_C, VERDE_C, fraccion, pizza, triangulo

T_INI = 0.0
C = "gancho"
tHola, tSexto, tProfe, tFotos, tCuad, tMate = (ww(C, 0, "hola"), ww(C, 0, "sexto"), ww(C, 0, "profe"), ww(C, 0, "fotos"),
                                               ww(C, 0, "cuaderno"), ww(C, 0, "matematicas"))
tTema = [ww(C, 1, "decimales"), ww(C, 1, "numeros grandes"), ww(C, 1, "triangulos"), ww(C, 1, "plano"), ww(C, 1, "fracciones")]
tPizza = ww(C, 1, "pizza")
tPausa, tVoz, tListos, tArr = ww(C, 2, "pausa"), ww(C, 2, "voz"), ww(C, 2, "listos"), ww(C, 2, "arrancamos")
FOTOS = [("decimales", 330, 320, -0.07, 250), ("numeros", 770, 300, 0.05, 250), ("plano", 1180, 400, 0.04, 420),
         ("triangulos", 450, 640, 0.06, 230), ("fracciones", 860, 650, -0.05, 230)]
TEMAS = [("DECIMALES", ROSA_C), ("NÚMEROS GRANDES", AZUL_C), ("TRIÁNGULOS", VERDE_C), ("PLANO CARTESIANO", MIEL),
         ("FRACCIONES", LILA_C)]
NOTAS = [(320, 320), (740, 300), (1160, 330), (520, 620), (960, 620)]


def _fondo():
    im = papel("calido")
    _manchas(im, rgb("f2c9a0"), 6, 41, r=(260, 420), alfa=0.16)
    forma(im, rrect(740, 470, 1360, 800, 16), rgb("8a5a34"), 0, 9001, tinta=6)
    forma(im, rrect(740, 470, 1300, 740, 8), rgb("c8955a"), 0, 9002, tinta=3, mota=1.0)
    rg = np.random.default_rng(5)
    for k in range(260):
        x, y = rg.uniform(110, 1370), rg.uniform(120, 820)
        forma(im, elipse(x, y, rg.uniform(2, 5), rg.uniform(2, 4)), rgb("9a6a3a") if k % 2 else rgb("deb07a"), 0, 9100 + k, tinta=0)
    forma(im, np.array([(0, 930), (W, 910), (W, H), (0, H)], np.float32), rgb("e2c393"), 0, 9005, tinta=0)
    linea(im, [(0, 930), (W, 910)], 5, seed=9006)
    return im


def chincheta(im, x, y, t, seed, col=ROJO):
    forma(im, elipse(x + 4, y + 6, 15, 12), rgb("5a4a3a"), t, seed + 1, tinta=0, alfa=0.3)
    forma(im, elipse(x, y, 15, 15), col, t, seed, tinta=2.5, luz=(rgb("ffffff"), -5, -5, 0.5))


def icono(im, k, x, y, t, e, seed):
    """Dibujito de cada tema dentro de su notita."""
    if k == 0:
        rotulo(im, "0.8", x, y, 64 * e + 1, ROJO, t, seed=seed)
    elif k == 1:
        rotulo(im, "7,735,923", x, y, 44 * e + 1, AZUL, t, seed=seed)
    elif k == 2:
        s = 46 * e
        triangulo(im, [(x, y - s), (x + s * 1.1, y + s * 0.8), (x - s * 1.1, y + s * 0.8)], t, rgb("fde0dc"), seed, marcas=(1, 1, 1))
    elif k == 3:
        linea(im, [(x - 70 * e, y + 30 * e), (x + 70 * e, y + 30 * e)], 6, AZUL, seed=seed, t=t)
        linea(im, [(x - 70 * e, y + 30 * e), (x - 70 * e, y - 50 * e)], 6, ROJO, seed=seed + 1, t=t)
        forma(im, elipse(x + 10 * e, y - 14 * e, 10 * e, 10 * e), AMARILLO, t, seed + 2, tinta=2.5)
        rotulo(im, "(3, 2)", x + 30 * e, y - 46 * e, 30 * e + 1, TINTA, t, seed=seed + 3, tinta=False)
    else:
        fraccion(im, 1, 4, x, y, 44, t, col=MORADO, seed=seed, esc=e)


def cuadro_crudo(t):
    im = cache("fondo_a", _fondo).copy()
    fase_temas = t > tTema[0] - 0.5
    fase_pausa = t > tPausa - 0.6
    if t > tFotos - 0.3 and not fase_temas:
        for k, (nom, x, y, rot, alto) in enumerate(FOTOS):
            u = e_out(pr(t, tFotos - 0.3 + 0.18 * k, tFotos + 0.35 + 0.18 * k))
            if u <= 0:
                continue
            xx, yy = x * u + (-300) * (1 - u), y * u + 1200 * (1 - u)
            polaroid(im, nom, xx, yy, 1.0, t, rot=rot + (1 - u) * 0.6, seed=9200 + k * 13, alto=alto, cinta=False)
            if u > 0.97:
                chincheta(im, xx, yy - alto / 2 - 14, t, 9260 + k * 3, col=[ROJO, AZUL, VERDE, MORADO, ROJO][k])
    if t > tCuad - 0.2 and not fase_temas:
        letrero(im, "SU CUADERNO", 1250, 150, 50, t, col=CREMA, txt=ROSA_M, seed=9300, esc=entra(t, tCuad - 0.2), rot=0.04)
    if t > tMate - 0.3 and not fase_temas:
        e = entra(t, tMate - 0.3)
        forma(im, rrect(740, 820, 1000 * e + 1, 130 * e + 1, 20, -0.03), rgb("e8559a"), t, 9310, tinta=5)
        rotulo(im, "¡REPASO DE MATE!", 740, 826, 84 * e + 1, CREMA, t, seed=9311, rot=-0.03)
        for k in range(3):
            destello(im, 280 + 460 * k, 750 - 30 * (k % 2), entra(t, tMate + 0.1 * k), t, seed=9315 + k)
    if fase_temas and not fase_pausa:
        for k, ((txt, col), (x, y)) in enumerate(zip(TEMAS, NOTAS)):
            e = entra(t, tTema[k] - 0.25)
            if e <= 0.01:
                continue
            rot = (k % 3 - 1) * 0.05
            tarjeta(im, x, y, 380 * e, 240 * e, t, col, 9400 + k * 7, rot=rot)
            chincheta(im, x, y - 100 * e, t, 9450 + k * 3, col=[ROJO, AZUL, VERDE][k % 3])
            rotulo(im, txt, x, y - 50 * e, (34 if len(txt) > 11 else 46) * e + 1, TINTA, t, seed=9401 + k * 7, tinta=False, rot=rot)
            icono(im, k, x, y + 40 * e, t, e, 9500 + k * 11)
        if t > tPizza - 0.6:
            u = e_back(pr(t, tPizza - 0.6, tPizza))
            pizza(im, 1250, 790 - 500 * (1 - u), 130, t, n=8, seed=9550, rot=t * 0.4)
            rotulo(im, "¡Y SÍ: PIZZA!", 1230, 600, 76 * entra(t, tPizza - 0.1) + 1, ROJO, t, seed=9560, rot=0.05)
    if fase_pausa:
        pausa(im, 450, 450, 1.5 * entra(t, tPausa - 0.6), t, seed=9600, texto=False)
        rotulo(im, "PAUSA Y CONTESTA", 740, 760, 92, ROJO, t, seed=9605, esc=entra(t, tPausa - 0.2))
        if t > tVoz - 0.2:
            ev = pr(t, tVoz - 0.2, tVoz + 1.2)
            for k in range(3):
                a = (t * 1.4 + k / 3) % 1
                linea(im, curva([(640 + 280 * a, 330), (690 + 280 * a, 450), (640 + 280 * a, 570)], 6), 9 * (1 - a) + 1, AMARILLO,
                      seed=9610 + k, t=t, alfa=min(1, ev * 2) * (1 - a))
            letrero(im, "¡EN VOZ ALTA!", 1050, 450, 56, t, col=CREMA, txt=MORADO, seed=9615, esc=entra(t, tVoz - 0.2), rot=0.04)
        if t > tArr - 0.2:
            rotulo(im, "¡ARRANCAMOS!", 740, 200, 104, VERDE, t, seed=9630, esc=entra(t, tArr - 0.2))
        elif t > tListos - 0.3:
            letrero(im, "¿LISTOS?", 740, 200, 60, t, col=AMARILLO, seed=9620, esc=entra(t, tListos - 0.3), rot=-0.03)
    if t > tHola - 0.1 and t < tFotos - 0.3:
        e = entra(t, tHola - 0.1)
        rotulo(im, "¡HOLA OTRA VEZ,", 700, 380, 96, ROJO, t, seed=9700, esc=e, rot=-0.03)
        rotulo(im, "SEXTO B!", 700, 510, 130, ROSA_M, t, seed=9701, esc=entra(t, tSexto - 0.1), rot=-0.03)
        for k in range(3):
            corazon(im, 1110 + 110 * k, 220 + 40 * (k % 2) - 30 * pr(t, tSexto, tSexto + 3), 2.2 * entra(t, tSexto + 0.15 * k), t,
                    seed=1041 + k)
    if tProfe - 0.3 < t < tFotos + 1.5:
        letrero(im, "PROFE TILDE", 1480, 330, 46, t, col=CREMA, txt=ROJO, seed=9720, esc=entra(t, tProfe - 0.3), rot=0.04)
    sube = e_back(pr(t, 0.0, 0.7))
    al = 600 - 270 * suave(pr(t, tTema[0] - 0.8, tTema[0]))
    papa(im, t, 1640 + 130 * suave(pr(t, tTema[0] - 0.8, tTema[0])), H + 50 + (1 - sube) * 700, alto=al)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
