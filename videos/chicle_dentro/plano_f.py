# -*- coding: utf-8 -*-
"""PELIGRO: «uno solo, no» (palomita) → «EXCEPCIÓN» → el artículo real (Pediatrics, 1998) con hospital → el niño de 4½ años
y el contador de chicles al día + «2 AÑOS» → corte del intestino donde muchos chicles se funden en una BOLA (bezoar) →
radiografía azul de la niña de año y medio con 4 monedas pegadas con chicle → lección: 1 = palomita; muchos + cosas = X."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, desborde, ww
from fondos_chicle import papel
from iconos_ia import marca_x, palomita, personita
from personajes import AMARILLO, BLANCO, exclama, kuri, nube_lluvia
from personajes_ia import nina
from piezas_chicle import GRIS, ROJO, calendario, chicle, documento, hospital, moneda

T_INI = T0("peligro")
P = "peligro"
tNada, tUno, tExc = ww(P, 0, "nada"), ww(P, 0, "uno"), ww(P, 0, "excepcion")
tAnio, tMedicos, tPublic, tHosp = ww(P, 1, "mil"), ww(P, 1, "medicos"), ww(P, 1, "publicaron"), ww(P, 1, "hospital")
tCuatro, tCinco, tDias, tDos, tEstr = (ww(P, 2, "cuatro"), ww(P, 2, "cinco"), ww(P, 2, "dias"), ww(P, 2, "dos"),
                                       ww(P, 2, "estrenido"))
tTanta, tBola, tBezoar, tQuitar = ww(P, 3, "tanta"), ww(P, 3, "bola"), ww(P, 3, "bezoar"), ww(P, 3, "quitarsela")
tNina, tMonedas, tEsof, tPegadas = ww(P, 4, "nina"), ww(P, 4, "monedas"), ww(P, 4, "esofago"), ww(P, 4, "pegadas")
tLeccion, tAcc, tMuchos, tAhi = ww(P, 5, "leccion"), ww(P, 5, "accidente"), ww(P, 5, "muchos"), ww(P, 5, "ahi")
T_NINO = tCuatro - 0.6
T_RX = tNina - 0.5
T_LEC = tLeccion - 0.4


def intro(t):
    im = papel("frio")
    en = e_back(pr(t, T_INI + 0.2, T_INI + 0.6))
    nina(im, 330, 600 + 4 * math.sin(t * 2), 1.4 * en + 0.01, t, cara="normal" if t < tExc else "abiertos",
         boca="duda" if t < tUno else ("sonrisa" if t < tExc else "o"), mira=0.8)
    if T_INI + 0.3 < t < tExc - 0.2:
        rotulo(im, "¿NO HACE NADA?", 800, 180, 96, AMARILLO, t, seed=10099, rot=-0.04, esc=e_back(pr(t, T_INI + 0.3, T_INI + 0.7)))
    if t > tUno - 0.3:
        e = e_back(pr(t, tUno - 0.3, tUno))
        chicle(im, 860, 580, 120 * e + 1, t, seed=10100, cara="feliz")
        palomita(im, 1060, 430, 1.2 * e, t, seed=10101)
        rotulo(im, "UNO SOLO", 860, 800, 84, rgb("2e8b4a"), t, seed=10102, esc=e)
    if t > tExc - 0.3 and t < tAnio:
        e = e_back(pr(t, tExc - 0.3, tExc))
        rotulo(im, "PERO HAY UNA EXCEPCIÓN", 1240, 200, 80, ROJO, t, seed=10103, rot=-0.04, esc=e)
        exclama(im, 1700, 420, 1.5 * e, t)
    kuri(im, 1560, 600 + 14 * math.sin(t * 1.5), 1.8, t, cara="normal" if t < tExc else "susto")
    if t > tAnio - 0.3:                                                    # el artículo real
        e = e_back(pr(t, tAnio - 0.3, tAnio))
        lavado(im, rrect(960, 540, 1920, 1080, 0), rgb("e6f0ec"), 0.9 * e, 10104)
        documento(im, 700, 540, 900 * e + 2, 760 * e + 2,
                  ["PEDIATRICS · 1998", "Chewing Gum Bezoars of the", "Gastrointestinal Tract", "~",
                   "Milov, Andres, Erhart y Bailey", "~"], t, seed=10110, px=int(48 * e) + 2, alfa=e)
        rotulo(im, "1998", 1500, 240, 150, ROJO, t, seed=10119, esc=e_back(pr(t, tAnio, tAnio + 0.3)))
        if t > tMedicos - 0.2:
            rotulo(im, "MÉDICOS DE ESTADOS UNIDOS", 1500, 400, 50, rgb("2f4f86"), t, seed=10120,
                   esc=e_back(pr(t, tMedicos - 0.2, tMedicos + 0.1)))
        if t > tHosp - 0.3:
            hospital(im, 1500, 700, 2.1 * e_back(pr(t, tHosp - 0.3, tHosp)), t)
    return im


def nino(t):
    im = papel("frio")
    x, y = 520, 520
    personita(im, x, y, 6.5, t, seed=1, col=rgb("3f78c8"), piel=rgb("f2c9a4"))
    dy = 3 * 6.5 * math.sin(t * 5 + 1)
    triste = t > tEstr - 0.2
    for d in (-1, 1):
        forma(im, elipse(x + d * 52, y + 14 + dy, 13, 18), TINTA, t, 10190 + d, tinta=0)
        brillo(im, x + d * 52 - 4, y + 8 + dy, 5, BLANCO, 0.9)
        brillo(im, x + d * 88, y + 58 + dy, 26, rgb("f08c8c"), 0.5)
        if triste:
            linea(im, [(x + d * 30, y - 18 + dy), (x + d * 72, y - 30 + dy)], 5, seed=10193 + d, t=t, punta=False)
    mast = 0.5 + 0.5 * math.sin(t * 11) if t < tDos else 0.0
    if triste:
        linea(im, curva([(x - 34, y + 90 + dy), (x, y + 76 + dy), (x + 34, y + 90 + dy)], 5), 5, seed=10196, t=t, punta=False)
    else:
        forma(im, elipse(x, y + 80 + dy, 26, 8 + 12 * mast), rgb("8a3a3a"), t, 10197, tinta=3)
    rotulo(im, "4½ AÑOS", x, 120, 80, rgb("2f4f86"), t, seed=10200, esc=e_back(pr(t, tCuatro - 0.2, tCuatro + 0.1)))
    # chicles que caen a su boca y contador
    if t > tCinco - 0.4:
        n = int(1 + 6.99 * pr(t, tCinco - 0.3, tDias + 0.3))
        for k in range(3):
            v = ((t - tCinco) * 1.6 + k / 3) % 1
            if t < tDos:
                chicle(im, x + 10, lerp(-60, y + 60, v), 40, t, seed=10210 + k, col=rgb("f39bc0"), dientes=False)
        forma(im, rrect(1000, 300, 360, 150, 24), BLANCO, t, 10220, tinta=4)
        rotulo(im, f"{min(n, 7)} AL DÍA", 1000, 300, 80, ROJO, t, seed=10221, tinta=False)
        if t < tTanta - 0.4:
            for k in range(min(n, 7)):
                chicle(im, 790 + k * 75, 450, 30, t, seed=10222 + k, col=rgb("f39bc0"), dientes=False)
    if t > tDos - 0.3 and t < tTanta:
        calendario(im, 1560, 330, 1.6 * e_back(pr(t, tDos - 0.3, tDos)), t, "AÑOS", "2")
        if t > tEstr - 0.2:
            nube_lluvia(im, x + 220, y - 230, e_back(pr(t, tEstr - 0.2, tEstr + 0.1)), t)
            rotulo(im, "ESTREÑIDO", 1150, 640, 90, rgb("8a6040"), t, seed=10230, esc=e_back(pr(t, tEstr - 0.2, tEstr + 0.1)))
    # corte del intestino: los chicles se funden en una bola
    if t > tTanta - 0.4:
        e = e_back(pr(t, tTanta - 0.4, tTanta))
        cx, cy = 1350, 620
        forma(im, rrect(cx, cy, 900 * e + 2, 300 * e + 2, 140 * e), rgb("eaa08e"), t, 10240, tinta=5,
              sombra=(rgb("b65a5d"), 0, 30, 0.5))
        lavado(im, rrect(cx, cy, 860 * e + 2, 220 * e + 2, 110 * e), rgb("f6c8b8"), 0.7, 10241)
        f = e_out(pr(t, tTanta, tBola + 0.4))
        for k in range(7):
            a = k * 0.9
            r = lerp(300, 40, f)
            chicle(im, cx + r * math.cos(a), cy + r * 0.3 * math.sin(a), lerp(34, 50, f) * e + 1, t, seed=10250 + k,
                   dientes=False, col=GRIS * lerp(1.0, 0.8, f))
        if f > 0.8:
            chicle(im, cx, cy, 120 * e, t, seed=10260, col=GRIS * 0.78, cara="triste")
        if t > tBezoar - 0.3:
            rotulo(im, "BEZOAR", cx, cy - 250, 110, ROJO, t, seed=10270, esc=e_back(pr(t, tBezoar - 0.3, tBezoar)))
        if t > tQuitar - 0.3:
            hospital(im, cx + 380, cy - 230, 0.9 * e_back(pr(t, tQuitar - 0.3, tQuitar)), t)
    return im


def rx(t):
    im = np.zeros((H, W, 3), np.float32)
    im[:] = rgb("16304a")
    lavado(im, rrect(960, 540, 1700, 940, 40), rgb("2a5a7e"), 0.6, 10300)
    # silueta de cabeza y cuello en «radiografía»
    sil = curva([(700, 150), (980, 100), (1150, 220), (1180, 420), (1100, 560), (1080, 1100), (760, 1100), (760, 560), (640, 420)], 8, True)
    lavado(im, sil, rgb("8fb8d8"), 0.35, 10301)
    linea(im, sil, 3, col=rgb("cfe6f6"), seed=10302, t=t, cerrado=True, alfa=0.6, punta=False)
    for d in (-1, 1):
        linea(im, [(920 + d * 45, 560), (920 + d * 45, 1100)], 4, col=rgb("cfe6f6"), seed=10303 + d, t=t, alfa=0.7, punta=False)
    rotulo(im, "1½ AÑOS", 400, 160, 80, AMARILLO, t, seed=10310, esc=e_back(pr(t, tNina - 0.1, tNina + 0.2)))
    if t > tMonedas - 0.4:
        e = e_back(pr(t, tMonedas - 0.4, tMonedas))
        if t > tPegadas - 0.3:
            lavado(im, mancha_(920, 800, 85, 10320), rgb("f39bc0"), 0.75 * pr(t, tPegadas - 0.3, tPegadas + 0.3), 10320)
        for k in range(4):
            moneda(im, 920 + 6 * math.sin(k), 700 + k * 66, 46 * e + 1, t, seed=10330 + k, rot=0.3)
        rotulo(im, "4 MONEDAS", 1420, 640, 80, AMARILLO, t, seed=10340, esc=e)
    if t > tEsof - 0.2:
        rotulo(im, "ESÓFAGO", 1400, 780, 60, BLANCO, t, seed=10341, esc=e_back(pr(t, tEsof - 0.2, tEsof + 0.1)))
        linea(im, [(1240, 780), (980, 760)], 3, col=BLANCO, seed=10342, t=t, alfa=0.6, punta=False)
    if t > tPegadas - 0.2:
        rotulo(im, "+ CHICLE", 1420, 900, 70, rgb("f39bc0"), t, seed=10343, esc=e_back(pr(t, tPegadas - 0.2, tPegadas + 0.1)))
    return im


def mancha_(x, y, r, seed):
    from acuarela import mancha_pts
    return mancha_pts(x, y, r, seed, 0.25, ry=r * 1.6)


def leccion(t):
    im = papel("calido")
    rotulo(im, "LA LECCIÓN", 960, 120, 100, rgb("2f4f86"), t, seed=10400, esc=e_back(pr(t, tLeccion - 0.2, tLeccion + 0.1)))
    kuri(im, 960, 620 + 12 * math.sin(t * 1.6), 1.05 * e_back(pr(t, T_LEC + 0.4, T_LEC + 0.8)) + 0.01, t,
         cara="feliz" if t < tMuchos else "susto", aura=False)
    if t > T_LEC + 0.5:
        e = e_back(pr(t, T_LEC + 0.5, T_LEC + 0.9))
        forma(im, rrect(500, 560, 640, 600, 30), BLANCO, t, 10410, tinta=4, alfa=e)
        chicle(im, 500, 540, 100 * e + 1, t, seed=10411, cara="feliz")
        palomita(im, 500, 740, 1.0 * e, t, seed=10412)
        rotulo(im, "1 POR ACCIDENTE", 500, 340, 56, rgb("2e8b4a"), t, seed=10413, esc=e)
    if t > tMuchos - 0.4:
        e = e_back(pr(t, tMuchos - 0.4, tMuchos))
        forma(im, rrect(1420, 560, 640, 600, 30), BLANCO, t, 10420, tinta=4, alfa=e)
        for k in range(9):
            chicle(im, 1300 + (k % 3) * 120, 470 + (k // 3) * 90, 48 * e + 1, t, seed=10421 + k, dientes=False)
        for k in range(3):
            moneda(im, 1330 + k * 110, 720, 30 * e + 1, t, seed=10431 + k)
        rotulo(im, "MUCHOS + OTRAS COSAS", 1420, 340, 52, ROJO, t, seed=10440, esc=e)
        if t > tAhi - 0.2:
            marca_x(im, 1420, 560, 1.8 * e_back(pr(t, tAhi - 0.2, tAhi + 0.1)), t, seed=10441)
    return im


def cuadro_crudo(t):
    pasos = [(T_INI, intro), (T_NINO, nino), (T_RX, rx), (T_LEC, leccion)]
    for i in range(len(pasos) - 1, -1, -1):
        t0, f = pasos[i]
        if t >= t0:
            if i > 0 and t < t0 + 0.8:
                return desborde(pasos[i - 1][1](t), f(t), pr(t, t0, t0 + 0.8), W / 2, H / 2)
            return f(t)
    return intro(t)


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
