# -*- coding: utf-8 -*-
"""GANCHO: papá sube desde abajo («¡HOLA, AMAYA!»), pizarrón con EXAMEN · LUNES y calendario, notitas 1810/1821 que se le pegan
a la cabeza → el robot tachado, globos de chisme, estrella de trucos, «JA JA JA» de chiste malo (Kuri se ríe) → botón de PAUSA,
ondas de voz alta, palomita de «¿sale?» y salida con «¡ARRANCAMOS!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import marca_x, palomita, estrella
from personajes import AMARILLO, corazon, kuri, destello, exclama
from personajes_ia import globo
from kit_amaya import (CREMA, ROJO, VERDE, DORADO, AZUL, cache, entra, fecha, letrero, papa, pausa, tarjeta)

T_INI = 0.0
C = "gancho"
tHola, tAmaya, tLunes, tExamen, tInd = ww(C, 0, "hola"), ww(C, 0, "amaya"), ww(C, 0, "lunes"), ww(C, 0, "examen"), ww(C, 0, "independencia")
tCinco, tPegada = ww(C, 0, "cinco"), ww(C, 0, "pegada")
tRobot, tChisme, tTrucos, tChistes = ww(C, 1, "robot"), ww(C, 1, "chisme"), ww(C, 1, "trucos"), ww(C, 1, "chistes")
tPausa, tVoz, tSale, tArranc = ww(C, 2, "pausa"), ww(C, 2, "voz"), ww(C, 2, "sale"), ww(C, 2, "arrancamos")


def _fondo():
    im = papel("calido")
    _manchas(im, rgb("f2c9a0"), 7, 31, r=(260, 420), alfa=0.18)
    # pizarrón verde con marco de madera (pared del salón)
    forma(im, rrect(640, 430, 980, 600, 18), rgb("8a5a34"), 0, 9001, tinta=6)
    forma(im, rrect(640, 430, 930, 550, 12), rgb("2f5d4a"), 0, 9002, tinta=4, mota=0.9)
    lavado(im, rrect(560, 380, 600, 260, 40), rgb("f0f0e8"), 0.08, 9003)
    forma(im, rrect(640, 740, 1000, 30, 8), rgb("a97848"), 0, 9004, tinta=4)
    # piso del salón
    forma(im, np.array([(0, 900), (W, 880), (W, H), (0, H)], np.float32), rgb("e2c393"), 0, 9005, tinta=0)
    linea(im, [(0, 900), (W, 880)], 5, seed=9006)
    return im


def gis(im, texto, x, y, px, t, t0, seed):
    """Letras de gis que se van escribiendo."""
    n = int(len(texto) * pr(t, t0, t0 + 0.6 + 0.04 * len(texto)))
    if n > 0:
        rotulo(im, texto[:n], x - (len(texto) - n) * px * 0.28, y, px, rgb("f4f1e6"), t, seed=seed, tinta=False)


def robot(im, x, y, s, t, seed=9100):
    forma(im, rrect(x, y + 90 * s, 120 * s, 120 * s, 18 * s), rgb("9aa4b0"), t, seed, tinta=4)
    forma(im, rrect(x, y, 150 * s, 110 * s, 22 * s), rgb("b8c2cc"), t, seed + 1, tinta=4)
    for d in (-1, 1):
        forma(im, elipse(x + d * 35 * s, y, 16 * s, 16 * s), rgb("4fb3e8"), t, seed + 2 + d, tinta=2.5)
    linea(im, [(x, y - 55 * s), (x, y - 95 * s)], 4 * s, seed=seed + 5, t=t)
    forma(im, elipse(x, y - 100 * s, 12 * s, 12 * s), ROJO, t, seed + 6, tinta=2.5)


def cuadro_crudo(t):
    im = cache("fondo_a", _fondo).copy()
    # pizarrón: EXAMEN / LUNES / INDEPENDENCIA DE MÉXICO
    if t > tExamen - 0.3:
        gis(im, "EXAMEN:", 470, 290, 84, t, tExamen - 0.3, 9200)
        gis(im, "INDEPENDENCIA", 640, 430, 82, t, tInd, 9201)
        gis(im, "DE MÉXICO", 640, 540, 82, t, tInd + 0.5, 9202)
        linea(im, [(330, 600), (330 + 620 * suave(pr(t, tInd + 0.9, tInd + 1.5)), 604)], 6, rgb("f2c14e"), seed=9203, t=t)
    if tLunes - 0.2 < t < tRobot - 0.4:
        fecha(im, 1010, 300, 0.62 * entra(t, tLunes - 0.2), t, "LUN", "NOV", "EXAMEN", seed=9210)
    # papá sube desde abajo
    sube = e_back(pr(t, 0.0, 0.7))
    papa(im, t, 1590, H + 50 + (1 - sube) * 700, alto=600)
    # notitas que vuelan a pegarse en la cabeza de papá
    if tPegada - 0.2 < t < tRobot - 0.4:
        for k, (txt, col, dx, dy) in enumerate((("1810", AMARILLO, -190, -720), ("1821", rgb("9ad3a8"), 170, -730),
                                                 ("HIDALGO", rgb("f6a6a0"), -10, -800))):
            u = e_out(pr(t, tPegada - 0.2 + 0.18 * k, tPegada + 0.25 + 0.18 * k))
            x = 1590 + dx * 0.79 * u + (1 - u) * (-700 + 200 * k)
            y = 1130 + dy * 0.79 * u + (1 - u) * (-500)
            rot = (k - 1) * 0.18 * u
            tarjeta(im, x, y, 190 + 30 * (k == 2), 110, t, col, seed=9300 + k * 5, rot=rot)
            rotulo(im, txt, x, y + 4, 44 if k < 2 else 36, rgb("2a2420"), t, seed=9302 + k * 5, tinta=False, rot=rot)
    if t > tHola - 0.1 and t < tRobot - 0.4:
        e = entra(t, tHola - 0.1)
        rotulo(im, "¡HOLA, AMAYA!", 640, 820, 112, ROJO, t, seed=9400, esc=e, rot=-0.03)
        for k in range(3):
            corazon(im, 1100 + 120 * k, 160 + 40 * (k % 2) - 30 * pr(t, tAmaya, tAmaya + 3), 2.2 * entra(t, tAmaya + 0.15 * k),
                    t, seed=1041 + k)
    if t > tCinco - 0.1 and t < tRobot - 0.4:
        letrero(im, "5 MINUTOS", 1010, 600, 52, t, col=AMARILLO, seed=9410, esc=entra(t, tCinco - 0.1), rot=0.05)
    # frase 1: robot tachado, chisme, trucos, chistes malos
    if tRobot - 0.4 <= t < tPausa - 0.5:
        forma(im, rrect(640, 430, 930, 550, 12), rgb("2f5d4a"), t, 9002, tinta=4, mota=0.9)    # se borra el pizarrón
        er = entra(t, tRobot - 0.4)
        robot(im, 330, 420, 1.3 * er + 0.01, t)
        if t > tRobot + 0.2:
            marca_x(im, 330, 450, 1.3 * entra(t, tRobot + 0.2), t, seed=9500)
        if t > tChisme - 0.3:
            ec = entra(t, tChisme - 0.3)
            globo(im, 660, 330, 300, 120, "", t, px=38, lineas=["¿YA SUPISTE?"], seed=9510, cola=(-1, 1), alfa=min(1, ec * 1.5))
            globo(im, 720, 520, 260, 110, "", t, px=38, lineas=["¡NOOO!"], seed=9520, cola=(1, 1),
                  alfa=min(1, entra(t, tChisme) * 1.5))
        if t > tTrucos - 0.2:
            et = entra(t, tTrucos - 0.2)
            estrella(im, 970, 360, 70 * et + 1, t, AMARILLO, seed=9530)
            destello(im, 1040, 290, et, t, seed=9531)
            rotulo(im, "TRUCOS", 970, 480, 48, rgb("f4f1e6"), t, seed=9532, esc=et, tinta=False)
        if t > tChistes - 0.2:
            ej = entra(t, tChistes - 0.2)
            for k in range(3):
                rotulo(im, "JA", 300 + 260 * k, 820 + 18 * math.sin(t * 9 + k), 120, AMARILLO, t, seed=9540 + k,
                       esc=entra(t, tChistes - 0.2 + 0.15 * k), rot=0.12 * (k - 1))
            kuri(im, 1180, 700 + 10 * math.sin(t * 8), 2.2 * ej + 0.01, t, cara="feliz", brazos=(1.5, 1.5 + 0.3 * math.sin(t * 9)))
    # frase 2: pausa y contesta
    if t >= tPausa - 0.5:
        forma(im, rrect(640, 430, 930, 550, 12), rgb("2f5d4a"), t, 9002, tinta=4, mota=0.9)
        pausa(im, 560, 420, 1.6 * entra(t, tPausa - 0.5), t, seed=9600, texto=False)
        rotulo(im, "PAUSA Y CONTESTA", 640, 820, 96, ROJO, t, seed=9605, esc=entra(t, tPausa - 0.2))
        if t > tVoz - 0.2:
            ev = pr(t, tVoz - 0.2, tVoz + 1.2)
            for k in range(3):
                a = ((t * 1.4 + k / 3) % 1)
                linea(im, curva([(760 + 90 * a * 3, 320), (800 + 90 * a * 3, 420), (760 + 90 * a * 3, 520)], 6), 7 * (1 - a) + 1,
                      AMARILLO, seed=9610 + k, t=t, alfa=min(1, ev * 2) * (1 - a))
            rotulo(im, "¡EN VOZ ALTA!", 870, 640, 58, rgb("f4f1e6"), t, seed=9615, esc=entra(t, tVoz - 0.2), tinta=False)
        if t > tSale - 0.2:
            palomita(im, 1260, 330, 2.4 * entra(t, tSale - 0.2), t, seed=9620, col=VERDE)
        if t > tArranc - 0.2:
            rotulo(im, "¡ARRANCAMOS!", 960, 160, 100, VERDE, t, seed=9630, esc=entra(t, tArranc - 0.2))
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
