# -*- coding: utf-8 -*-
"""GANCHO: corcho; el profe Tilde sube desde abajo con BATA («¡HOLA OTRA VEZ, SEXTO B!») → letrero «BATA DE CIENTÍFICO» → llegan
volando 4 FOTOS REALES de su cuaderno de Ciencias y se clavan → banda «¡REPASO DE CIENCIAS!» → 4 notitas (MATERIA Y GASES,
JERINGA, ATMÓSFERA, SISTEMA INMUNITARIO + escudo del «ejército») → PAUSA con «¡EN VOZ ALTA!» y «¡ARRANCAMOS!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import ww
from fondos_amaya import papel, _manchas
from personajes import AMARILLO, corazon, destello
from kit_amaya import AZUL, CREMA, MORADO, ROJO, VERDE, cache, entra, letrero, papa, pausa, tarjeta, flecha_curva
from piezas_es import ROSA_M, polaroid

T_INI = 0.0
C = "gancho"
tHola, tSexto, tBata, tFotos, tCuad, tCien = (ww(C, 0, "hola"), ww(C, 0, "sexto"), ww(C, 0, "bata"), ww(C, 0, "fotos"),
                                              ww(C, 0, "cuaderno"), ww(C, 0, "ciencias"))
TEMAS = [("MATERIA Y GASES", "materia", rgb("f6a6a0")), ("LA JERINGA", "jeringa", rgb("b8c7e8")),
         ("LA ATMÓSFERA", "atmosfera", rgb("a8d8b0")), ("SISTEMA INMUNITARIO", "inmunitario", rgb("f4d38a"))]
tTema = [ww(C, 1, k) for _, k, _ in TEMAS]
tEjer = ww(C, 1, "ejercito")
tPasada, tPausa, tVoz, tListos, tArr = ww(C, 2, "igual"), ww(C, 2, "pausa"), ww(C, 2, "voz"), ww(C, 2, "listos"), ww(C, 2, "arrancamos")
FOTOS = [("materia", 400, 320, -0.06), ("atmosfera", 1040, 330, 0.05), ("jeringa", 420, 650, 0.04), ("inmune1", 1060, 660, -0.05)]
NOTAS = [(420, 330), (1060, 330), (420, 650), (1060, 650)]


def _fondo():
    im = papel("calido")
    _manchas(im, rgb("f2c9a0"), 6, 41, r=(260, 420), alfa=0.16)
    forma(im, rrect(740, 490, 1400, 820, 16), rgb("8a5a34"), 0, 9001, tinta=6)
    forma(im, rrect(740, 490, 1340, 760, 8), rgb("c8955a"), 0, 9002, tinta=3, mota=1.0)
    rg = np.random.default_rng(5)
    for k in range(260):
        x, y = rg.uniform(90, 1390), rg.uniform(130, 850)
        forma(im, elipse(x, y, rg.uniform(2, 5), rg.uniform(2, 4)), rgb("9a6a3a") if k % 2 else rgb("deb07a"), 0, 9100 + k, tinta=0)
    forma(im, np.array([(0, 940), (W, 920), (W, H), (0, H)], np.float32), rgb("e2c393"), 0, 9005, tinta=0)
    linea(im, [(0, 940), (W, 920)], 5, seed=9006)
    return im


def chincheta(im, x, y, t, seed, col=ROJO):
    forma(im, elipse(x + 4, y + 6, 15, 12), rgb("5a4a3a"), t, seed + 1, tinta=0, alfa=0.3)
    forma(im, elipse(x, y, 15, 15), col, t, seed, tinta=2.5, luz=(rgb("ffffff"), -5, -5, 0.5))


def escudo(im, x, y, s, t, seed):
    forma(im, np.array(curva([(x - 60 * s, y - 70 * s), (x + 60 * s, y - 70 * s), (x + 55 * s, y + 10 * s), (x, y + 75 * s),
                              (x - 55 * s, y + 10 * s)], 8, True)), AZUL, t, seed, tinta=4 * s, luz=(rgb("ffffff"), -15 * s, -20 * s, 0.4))
    linea(im, [(x, y - 50 * s), (x, y + 50 * s)], 10 * s, CREMA, seed=seed + 1, t=t)
    linea(im, [(x - 35 * s, y - 10 * s), (x + 35 * s, y - 10 * s)], 10 * s, CREMA, seed=seed + 2, t=t)


def cuadro_crudo(t):
    im = cache("fondo_a", _fondo).copy()
    fase_temas = t > tTema[0] - 0.5
    fase_pausa = t > tPasada - 0.4
    if t > tFotos - 0.3 and not fase_temas:
        for k, (nom, x, y, rot) in enumerate(FOTOS):
            u = e_out(pr(t, tFotos - 0.3 + 0.2 * k, tFotos + 0.35 + 0.2 * k))
            if u <= 0:
                continue
            xx, yy = x * u + (-300) * (1 - u), y * u + 1200 * (1 - u)
            polaroid(im, nom, xx, yy, 1.0, t, rot=rot + (1 - u) * 0.6, seed=9200 + k * 13, alto=250, cinta=False)
            if u > 0.97:
                chincheta(im, xx, yy - 150, t, 9260 + k * 3, col=[ROJO, AZUL, VERDE, MORADO][k])
    if t > tCuad - 0.2 and not fase_temas:
        letrero(im, "SU CUADERNO", 740, 490, 54, t, col=CREMA, txt=ROSA_M, seed=9300, esc=entra(t, tCuad - 0.2), rot=-0.04)
    if t > tCien - 0.3 and not fase_temas:
        e = entra(t, tCien - 0.3)
        forma(im, rrect(740, 800, 1000 * e + 1, 130 * e + 1, 20, -0.03), rgb("2fb5a0"), t, 9310, tinta=5)
        rotulo(im, "¡REPASO DE CIENCIAS!", 740, 806, 76 * e + 1, CREMA, t, seed=9311, rot=-0.03)
        for k in range(3):
            destello(im, 280 + 460 * k, 730 - 30 * (k % 2), entra(t, tCien + 0.1 * k), t, seed=9315 + k)
    if fase_temas and not fase_pausa:
        for k, ((txt, _, col), (x, y)) in enumerate(zip(TEMAS, NOTAS)):
            e = entra(t, tTema[k] - 0.25)
            if e <= 0.01:
                continue
            rot = (k % 3 - 1) * 0.04
            tarjeta(im, x, y, 520 * e, 230 * e, t, col, 9400 + k * 7, rot=rot)
            chincheta(im, x, y - 100 * e, t, 9450 + k * 3, col=[ROJO, AZUL, VERDE, MORADO][k])
            rotulo(im, txt, x, y + 14, (44 if len(txt) > 14 else 56) * e + 1, TINTA, t, seed=9401 + k * 7, tinta=False, rot=rot)
        if t > tEjer - 0.3:
            e = entra(t, tEjer - 0.3)
            escudo(im, 1330, 800, 0.75 * e + 0.01, t, 9470)
            rotulo(im, "¡EJÉRCITO!", 1160, 820, 42 * e + 1, AZUL, t, seed=9475, rot=0.05)
    if fase_pausa:
        if t < tPausa - 0.4:
            letrero(im, "COMO LA VEZ PASADA", 740, 300, 60, t, col=AMARILLO, seed=9590, esc=entra(t, tPasada - 0.4), rot=-0.03)
        else:
            pausa(im, 450, 450, 1.5 * entra(t, tPausa - 0.6), t, seed=9600, texto=False)
            rotulo(im, "PAUSA Y CONTESTA", 740, 760, 92, ROJO, t, seed=9605, esc=entra(t, tPausa - 0.2))
            if t > tVoz - 0.2:
                ev = pr(t, tVoz - 0.2, tVoz + 1.2)
                for k in range(3):
                    a = (t * 1.4 + k / 3) % 1
                    linea(im, curva([(640 + 280 * a, 330), (690 + 280 * a, 450), (640 + 280 * a, 570)], 6), 9 * (1 - a) + 1, AMARILLO,
                          seed=9610 + k, t=t, alfa=min(1, ev * 2) * (1 - a))
                letrero(im, "¡EN VOZ ALTA!", 1050, 450, 56, t, col=CREMA, txt=MORADO, seed=9615, esc=entra(t, tVoz - 0.2), rot=0.04)
            if t > tListos - 0.2 and t < tArr - 0.2:
                letrero(im, "¿LISTOS?", 740, 200, 60, t, col=AMARILLO, seed=9620, esc=entra(t, tListos - 0.2), rot=-0.03)
            if t > tArr - 0.2:
                rotulo(im, "¡ARRANCAMOS!", 740, 200, 104, VERDE, t, seed=9630, esc=entra(t, tArr - 0.2))
    if t > tHola - 0.1 and t < tFotos - 0.3:
        e = entra(t, tHola - 0.1)
        rotulo(im, "¡HOLA OTRA VEZ,", 700, 330, 96, ROJO, t, seed=9700, esc=e, rot=-0.03)
        rotulo(im, "SEXTO B!", 700, 470, 140, ROSA_M, t, seed=9701, esc=entra(t, tSexto - 0.1), rot=-0.03)
        for k in range(3):
            corazon(im, 1130 + 100 * k, 200 + 40 * (k % 2) - 30 * pr(t, tSexto, tSexto + 3), 2.0 * entra(t, tSexto + 0.15 * k), t,
                    seed=1041 + k)
        if t > tBata - 0.3:
            e = entra(t, tBata - 0.3)
            letrero(im, "¡CON BATA DE CIENTÍFICO!", 820, 680, 50, t, col=CREMA, txt=AZUL, seed=9710, esc=e, rot=0.03)
            flecha_curva(im, [(1180, 700), (1350, 760), (1480, 820)], t, col=AZUL, ancho=8, seed=9712, u=pr(t, tBata, tBata + 0.5))
    if tSexto + 1.0 < t < tFotos + 1.5:
        letrero(im, "PROFE TILDE", 1520, 300, 46, t, col=CREMA, txt=ROJO, seed=9720, esc=entra(t, tSexto + 1.0), rot=0.04)
    sube = e_back(pr(t, 0.0, 0.7))
    al = 600 - 270 * suave(pr(t, tTema[0] - 0.8, tTema[0]))
    papa(im, t, 1660 + 110 * suave(pr(t, tTema[0] - 0.8, tTema[0])), H + 50 + (1 - sube) * 700, alto=al)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
