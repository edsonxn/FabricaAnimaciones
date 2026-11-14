# -*- coding: utf-8 -*-
"""GANCHO: tablero de corcho; papá sube desde abajo («¡HOLA OTRA VEZ, AMAYA!») → llegan volando las FOTOS REALES de su cuaderno y se
quedan clavadas con chinchetas → banda «¡TAMBIÉN TOCA ESPAÑOL!» → las fotos se van y salen seis notitas (SÍLABAS, ACENTOS,
ADVERBIOS, AUTOBIOGRAFÍA, ANÉCDOTA, CARTA INFORMAL), una por palabra → «¡CORTITAS!» se aplastan → palomita del «¿sale?» → botón de
PAUSA con «COMO EN HISTORIA» y «¡ARRANCAMOS!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import palomita, estrella
from personajes import AMARILLO, corazon, destello
from kit_amaya import (AZUL, CREMA, MORADO, ROJO, VERDE, cache, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid

T_INI = 0.0
C = "gancho"
tHola, tAmaya, tFotos, tCuad, tEsp = ww(C, 0, "hola"), ww(C, 0, "sexto"), ww(C, 0, "fotos"), ww(C, 0, "cuaderno"), ww(C, 0, "espanol")
TEMAS = [("SÍLABAS", "silabas", rgb("f6a6a0")), ("ACENTOS", "acentos", rgb("b8c7e8")), ("ADVERBIOS", "adverbios", rgb("a8d8b0")),
         ("AUTOBIOGRAFÍA", "autobiografia", rgb("f4d38a")), ("ANÉCDOTA", "anecdota", rgb("d8b8e8")),
         ("CARTA INFORMAL", "carta", rgb("f7c59f"))]
tTema = [ww(C, 1, k) for _, k, _ in TEMAS]
tCort, tSale1 = ww(C, 1, "cortitas"), ww(C, 1, "cortitas") + 0.8
tHist, tPausa, tVoz, tArr = ww(C, 2, "listos"), ww(C, 2, "pausa"), ww(C, 2, "voz"), ww(C, 2, "arrancamos")
FOTOS = [("tonica", 330, 380, -0.08), ("adverbios", 640, 350, 0.05), ("carta", 950, 390, -0.03), ("autobio", 1240, 370, 0.07)]
NOTAS = [(330, 330), (720, 300), (1110, 330), (330, 620), (720, 600), (1110, 630)]


def _fondo():
    im = papel("calido")
    _manchas(im, rgb("f2c9a0"), 6, 41, r=(260, 420), alfa=0.16)
    forma(im, rrect(740, 470, 1360, 800, 16), rgb("8a5a34"), 0, 9001, tinta=6)          # marco de madera
    forma(im, rrect(740, 470, 1300, 740, 8), rgb("c8955a"), 0, 9002, tinta=3, mota=1.0)  # corcho
    rg = np.random.default_rng(5)
    for k in range(260):                                                                # granitos del corcho
        x, y = rg.uniform(110, 1370), rg.uniform(120, 820)
        forma(im, elipse(x, y, rg.uniform(2, 5), rg.uniform(2, 4)), rgb("9a6a3a") if k % 2 else rgb("deb07a"), 0, 9100 + k, tinta=0)
    forma(im, np.array([(0, 930), (W, 910), (W, H), (0, H)], np.float32), rgb("e2c393"), 0, 9005, tinta=0)
    linea(im, [(0, 930), (W, 910)], 5, seed=9006)
    return im


def chincheta(im, x, y, t, seed, col=ROJO):
    forma(im, elipse(x + 4, y + 6, 15, 12), rgb("5a4a3a"), t, seed + 1, tinta=0, alfa=0.3)
    forma(im, elipse(x, y, 15, 15), col, t, seed, tinta=2.5, luz=(rgb("ffffff"), -5, -5, 0.5))


def cuadro_crudo(t):
    im = cache("fondo_a", _fondo).copy()
    fase_temas = t > tTema[0] - 0.5
    fase_pausa = t > tPausa - 0.6
    # 1) fotos reales del cuaderno que llegan volando y se clavan
    if t > tFotos - 0.3 and not fase_temas:
        for k, (nom, x, y, rot) in enumerate(FOTOS):
            u = e_out(pr(t, tFotos - 0.3 + 0.22 * k, tFotos + 0.35 + 0.22 * k))
            if u <= 0:
                continue
            xx, yy = x * u + (-300) * (1 - u), y * u + 1200 * (1 - u)
            polaroid(im, nom, xx, yy, 0.64, t, rot=rot + (1 - u) * 0.6, seed=9200 + k * 13, cinta=False)
            if u > 0.97:
                chincheta(im, xx, yy - 190, t, 9260 + k * 3, col=[ROJO, AZUL, VERDE, MORADO][k])
    if t > tCuad - 0.2 and not fase_temas:
        letrero(im, "SU CUADERNO", 560, 640, 54, t, col=CREMA, txt=ROSA_M, seed=9300, esc=entra(t, tCuad - 0.2), rot=-0.04)
    if t > tEsp - 0.3 and not fase_temas:
        e = entra(t, tEsp - 0.3)
        forma(im, rrect(740, 760, 1000 * e + 1, 130 * e + 1, 20, -0.03), rgb("e8559a"), t, 9310, tinta=5)
        rotulo(im, "¡REPASO DE ESPAÑOL!", 740, 766, 78 * e + 1, CREMA, t, seed=9311, rot=-0.03)
        for k in range(3):
            destello(im, 280 + 460 * k, 690 - 30 * (k % 2), entra(t, tEsp + 0.1 * k), t, seed=9315 + k)
    # 2) seis notitas: una por tema que nombra
    if fase_temas and not fase_pausa:
        aplasta = math.exp(-((t - tCort - 0.25) / 0.3) ** 2)
        for k, ((txt, _, col), (x, y)) in enumerate(zip(TEMAS, NOTAS)):
            e = entra(t, tTema[k] - 0.25)
            if e <= 0.01:
                continue
            rot = (k % 3 - 1) * 0.05
            tarjeta(im, x, y, 360 * e, 220 * e * (1 - 0.25 * aplasta), t, col, 9400 + k * 7, rot=rot)
            chincheta(im, x, y - 90 * e, t, 9450 + k * 3, col=[ROJO, AZUL, VERDE][k % 3])
            rotulo(im, txt, x, y + 10, (40 if len(txt) > 10 else 52) * e + 1, TINTA, t, seed=9401 + k * 7, tinta=False, rot=rot)
        if t > tCort - 0.25:
            rotulo(im, "¡CORTITAS!", 720, 830, 84, ROJO, t, seed=9480, esc=entra(t, tCort - 0.25), rot=0.03)
        if t > tSale1 - 0.2:
            palomita(im, 1250, 820, 1.6 * entra(t, tSale1 - 0.2), t, seed=9485, col=VERDE)
    # 3) pausa y contesta
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
    elif t > tHist - 0.3:
        letrero(im, "¿LISTOS?", 740, 200, 60, t, col=AMARILLO, seed=9620, esc=entra(t, tHist - 0.3), rot=-0.03)
    # saludo
    if t > tHola - 0.1 and t < tFotos - 0.3:
        e = entra(t, tHola - 0.1)
        rotulo(im, "¡HOLA,", 740, 380, 110, ROJO, t, seed=9700, esc=e, rot=-0.03)
        rotulo(im, "SEXTO B!", 740, 510, 130, ROSA_M, t, seed=9701, esc=entra(t, tAmaya - 0.1), rot=-0.03)
        for k in range(3):
            corazon(im, 1110 + 110 * k, 200 + 40 * (k % 2) - 30 * pr(t, tAmaya, tAmaya + 3), 2.2 * entra(t, tAmaya + 0.15 * k), t,
                    seed=1041 + k)
    if tAmaya + 1.0 < t < tFotos + 1.5:
        letrero(im, "PROFE TILDE", 1480, 330, 46, t, col=CREMA, txt=ROJO, seed=9720, esc=entra(t, tAmaya + 1.0), rot=0.04)
    # papá sube desde abajo y luego se acomoda
    sube = e_back(pr(t, 0.0, 0.7))
    al = 600 - 270 * suave(pr(t, tTema[0] - 0.8, tTema[0]))
    papa(im, t, 1640 + 130 * suave(pr(t, tTema[0] - 0.8, tTema[0])), H + 50 + (1 - sube) * 700, alto=al)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
