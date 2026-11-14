# -*- coding: utf-8 -*-
"""CAUSAS: «MÉXICO» tachado → NUEVA ESPAÑA, el rey (Fernando VII) al otro lado del mar → pirámide de castas que se arma piso por
piso → el criollo con título y dinero frente a la puerta cerrada («MEGA INJUSTO») → foco de ideas con banderas 1776/1789 →
Napoleón le quita la silla al rey (1808) → tarjeta del truco: INJUSTICIA · IDEAS · NAPOLEÓN."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_back, e_in, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import marca_x, palomita, estrella
from personajes import AMARILLO, destello, exclama, gota
from utileria import bombilla, flecha
from kit_amaya import (AZUL, CAFE, CREMA, DORADO, GRIS, ROJO, VERDE, cache, cam, entra, gente, letrero, papa, tarjeta)

T_INI = T0("causas")
C = "causas"
tPorque, tFijate, tDoscientos, tMexico, tNueva, tRey = (ww(C, 0, "por"), ww(C, 0, "fijate"), ww(C, 0, "doscientos"),
                                                       ww(C, 0, "mexico"), ww(C, 0, "nueva"), ww(C, 0, "rey"))
tPiramide, tPenins, tCriollos = ww(C, 1, "piramide"), ww(C, 1, "peninsulares"), ww(C, 1, "criollos")
tMestizos, tIndig, tEsclavos, tTrabajan, tGanan = (ww(C, 2, "mestizos"), ww(C, 2, "indigenas"), ww(C, 2, "esclavos"),
                                                   ww(C, 2, "trabajaban"), ww(C, 2, "ganaban"))
tEstudios, tDinero, tPuestos, tMega = ww(C, 3, "estudios"), ww(C, 3, "dinero"), ww(C, 3, "puestos"), ww(C, 3, "mega")
tIdeas, tEEUU, tFrancia = ww(C, 4, "ideas"), ww(C, 4, "estados"), ww(C, 4, "francia")
tMil, tNapo, tTrono, tJuego, tEjer = ww(C, 5, "mil"), ww(C, 5, "napoleon"), ww(C, 5, "trono"), ww(C, 5, "juego"), ww(C, 5, "ejercito")
tTruco, tInj, tIde, tNap = ww(C, 6, "truco"), ww(C, 6, "injusticia"), ww(C, 6, "ideas"), ww(C, 6, "napoleon")

T_PIR = tPiramide - 0.9
T_CRI = ww(C, 3, "los") - 0.5
T_IDE = ww(C, 4, "ademas") - 0.5
T_NAP = tMil - 0.5
T_TRU = tTruco - 0.5


def _fondo(nombre, seed):
    im = papel(nombre)
    _manchas(im, rgb("e8c79a") if nombre != "frio" else rgb("bcd7d0"), 7, seed, r=(240, 420), alfa=0.16)
    return im


def mar(im, t, y=640):
    lavado(im, rrect(960, y + 120, 760, 330, 120), rgb("7fb3d5"), 0.55, 9701)
    for k in range(5):
        x0 = 640 + 130 * k + 25 * math.sin(t * 1.5 + k)
        linea(im, curva([(x0, y + 60 + 40 * (k % 2)), (x0 + 30, y + 40 + 40 * (k % 2)), (x0 + 60, y + 60 + 40 * (k % 2))], 5), 4,
              rgb("3f6f9a"), seed=9710 + k, t=t)


def corona(im, x, y, s, t, seed=9720):
    pts = [(-60, 30), (-60, -20), (-30, 5), (0, -40), (30, 5), (60, -20), (60, 30)]
    forma(im, np.array([(x + px * s, y + py * s) for px, py in pts], np.float32), DORADO, t, seed, tinta=3.5 * s + 1)
    for dx in (-30, 0, 30):
        forma(im, elipse(x + dx * s, y + 15 * s, 7 * s, 7 * s), ROJO, t, seed + 1 + dx, tinta=1.5)


def silla(im, x, y, s, t, seed=9730, rot=0.0, col=CAFE):
    c, sn = math.cos(rot), math.sin(rot)

    def T(px, py):
        return (x + (px * c - py * sn) * s, y + (px * sn + py * c) * s)
    forma(im, np.array([T(-70, -20), T(70, -20), T(70, 10), T(-70, 10)], np.float32), col, t, seed, tinta=3.5)
    forma(im, np.array([T(-70, -200), T(-45, -200), T(-45, -20), T(-70, -20)], np.float32), col, t, seed + 1, tinta=3.5)
    for px in (-60, 55):
        forma(im, np.array([T(px, 10), T(px + 14, 10), T(px + 14, 120), T(px, 120)], np.float32), col, t, seed + 2 + px, tinta=3)


def bandera_eeuu(im, x, y, s, t, seed=9740):
    forma(im, rrect(x, y, 220 * s, 140 * s, 6), CREMA, t, seed, tinta=3)
    for k in range(4):
        forma(im, rrect(x, y - 52 * s + k * 35 * s, 216 * s, 16 * s, 2), ROJO, t, seed + 1 + k, tinta=0)
    forma(im, rrect(x - 60 * s, y - 38 * s, 96 * s, 64 * s, 3), AZUL, t, seed + 6, tinta=0)


def bandera_francia(im, x, y, s, t, seed=9750):
    for k, c in enumerate((AZUL, CREMA, ROJO)):
        forma(im, rrect(x + (k - 1) * 72 * s, y, 74 * s, 140 * s, 3), c, t, seed + k, tinta=3)


def bicornio(im, x, y, s, t, seed=9760):
    forma(im, curva([(x - 120 * s, y + 20 * s), (x, y - 70 * s), (x + 120 * s, y + 20 * s), (x, y + 5 * s)], 8, True), rgb("2a2a33"),
          t, seed, tinta=4)
    forma(im, elipse(x + 30 * s, y - 15 * s, 16 * s, 16 * s), ROJO, t, seed + 1, tinta=2)


def nueva_espana(t):
    im = cache(("fb", "calido"), lambda: _fondo("calido", 41)).copy()
    mar(im, t)
    e = entra(t, T_INI + 0.1)
    if t > tFijate - 0.2:
        letrero(im, f"+ DE 200 AÑOS", 960, 170, 62, t, col=AMARILLO, seed=9800, esc=entra(t, tDoscientos - 0.2))
    # el letrero del lado de acá: MÉXICO → tachado → NUEVA ESPAÑA
    tarjeta(im, 470, 520, 560, 300 * e + 1, t, CREMA, 9810, rot=-0.03)
    if t < tNueva - 0.2:
        rotulo(im, "MÉXICO", 470, 520, 96, VERDE, t, seed=9811, esc=e)
        if t > tMexico + 0.3:
            marca_x(im, 470, 520, 2.4 * entra(t, tMexico + 0.3), t, seed=9812, col=ROJO)
    else:
        rotulo(im, "NUEVA", 470, 470, 92, ROJO, t, seed=9813, esc=entra(t, tNueva - 0.2))
        rotulo(im, "ESPAÑA", 470, 580, 92, ROJO, t, seed=9814, esc=entra(t, tNueva))
    # el rey al otro lado del mar
    er = entra(t, tNueva + 0.3)
    cam(im, "fernando", 1440, 470, 0.85 * er, t, "REY DE ESPAÑA", seed=1)
    if er > 0.3:
        corona(im, 1440, 270 - 6 * math.sin(t * 3), 1.1 * er, t)
    if t > tRey - 0.3:
        flecha(im, 1260, 560, 790, 600, 26, t, ROJO, seed=9820)
        rotulo(im, "MANDA", 1020, 520, 56, ROJO, t, seed=9821, esc=entra(t, tRey - 0.3))
    return im


PISOS = [  # (palabra que lo enciende, etiqueta, color, ancho, gente)
    ("pen", "PENINSULARES", DORADO, 300, 2),
    ("cri", "CRIOLLOS", AZUL, 520, 3),
    ("mes", "MESTIZOS", VERDE, 740, 5),
    ("ind", "INDÍGENAS Y ESCLAVOS", CAFE, 960, 7),
]


def piramide(t):
    im = cache(("fb", "frio"), lambda: _fondo("frio", 43)).copy()
    tiempos = [tPenins - 0.2, tCriollos - 0.2, tMestizos - 0.2, tIndig - 0.2]
    cx, ybase = 830, 980
    lavado(im, np.array([(cx - 520, ybase + 20), (cx + 520, ybase + 20), (cx, 140)], np.float32), rgb("5a4a3a"), 0.12, 9900)
    linea(im, [(cx - 500, ybase), (cx, 150), (cx + 500, ybase)], 5, seed=9901, t=t, alfa=0.6 * suave(pr(t, T_PIR, tPiramide + 0.4)))
    for i, (_, etq, col, ancho, n) in enumerate(PISOS):
        e = entra(t, tiempos[i])
        if e <= 0.01:
            continue
        y = 300 + i * 190
        forma(im, rrect(cx, y, ancho * e, 150, 12), col, t, 9910 + i, tinta=4.5, luz=(rgb("ffffff"), -20, -30, 0.25))
        for k in range(n):
            px = cx - ancho / 2 + ancho * (k + 0.5) / n
            cara = "triste" if i >= 2 and t > tTrabajan else "normal"
            gente(im, px, y - 30, 1.6 * e, t, seed=20 + i * 9 + k, cara=cara)
            if i >= 2 and t > tTrabajan:
                gota(im, px + 28, y - 60 + 10 * ((t * 2 + k) % 1), 0.6, t, seed=9930 + i * 9 + k)
        letrero(im, etq, cx + ancho / 2 + 60 + len(etq) * 15, y, 44, t, col=CREMA, seed=9940 + i * 5, esc=e)
    if t < tPenins - 0.2:
        rotulo(im, "LA PIRÁMIDE", cx, 600, 90, rgb("3f6f6a"), t, seed=9905, esc=entra(t, T_PIR + 0.3))
    if t > tPenins:
        for k in range(2):
            corona(im, cx - 75 + 150 * k, 215, 0.45, t, seed=9950 + k)
    if t > tTrabajan - 0.2:
        letrero(im, "TRABAJAN MÁS", 1600, 230, 50, t, col=rgb("f6a6a0"), seed=9960, esc=entra(t, tTrabajan - 0.2), rot=0.04)
    if t > tGanan - 0.2:
        letrero(im, "GANAN MENOS", 1600, 340, 50, t, col=rgb("f6a6a0"), seed=9965, esc=entra(t, tGanan - 0.2), rot=-0.04)
    return im


def criollo(t):
    im = cache(("fb", "rosa"), lambda: _fondo("rosa", 45)).copy()
    e = entra(t, T_CRI)
    # la puerta de los puestos importantes
    forma(im, rrect(1240, 560, 420, 640, 14), rgb("7a4a2a"), t, 10000, tinta=5)
    forma(im, rrect(1240, 600, 340, 540, 10), rgb("9a6a3a"), t, 10001, tinta=4)
    letrero(im, "PUESTOS IMPORTANTES", 1240, 210, 40, t, col=DORADO, seed=10002)
    forma(im, elipse(1340, 620, 18, 18), DORADO, t, 10003, tinta=2.5)
    if t > tPuestos + 0.3:
        el = entra(t, tPuestos + 0.3)
        forma(im, rrect(1240, 620, 120 * el, 100 * el, 14), GRIS, t, 10004, tinta=4)       # candado
        linea(im, curva([(1205, 580), (1205, 520), (1275, 520), (1275, 580)], 8), 12 * el, seed=10005, t=t)
        letrero(im, "SOLO PENINSULARES", 1240, 790, 40, t, col=CREMA, txt=ROJO, seed=10006, esc=el, rot=-0.08)
    # el criollo
    cara = "enojo" if t > tMega - 0.3 else "normal"
    gente(im, 560, 520, 6.5 * e + 0.01, t, seed=21, cara=cara, col=AZUL)
    if t > tEstudios - 0.2:
        es = entra(t, tEstudios - 0.2)
        forma(im, rrect(330, 520, 190 * es, 60 * es, 28 * es, 0.3), CREMA, t, 10010, tinta=3.5)
        forma(im, rrect(330, 520, 26 * es, 66 * es, 4, 0.3), ROJO, t, 10011, tinta=0)
        rotulo(im, "ESTUDIOS", 330, 610, 46, TINTA, t, seed=10012, esc=es, tinta=False)
    if t > tDinero - 0.2:
        ed = entra(t, tDinero - 0.2)
        forma(im, elipse(800, 700, 80 * ed, 90 * ed), rgb("c9a45a"), t, 10020, tinta=4)
        rotulo(im, "$", 800, 710, 90 * ed, rgb("5a4020"), t, seed=10021, tinta=False)
    if t > tMega - 0.3:
        rotulo(im, "¡MEGA INJUSTO!", 760, 960, 104, ROJO, t, seed=10030, esc=entra(t, tMega - 0.3), rot=-0.03)
        exclama(im, 560, 150, 1.3, t, seed=10031)
    return im


def ideas(t):
    im = cache(("fb", "calido2"), lambda: _fondo("calido", 47)).copy()
    e = entra(t, tIdeas - 0.3)
    brillo_r = 1 + 0.1 * math.sin(t * 5)
    from acuarela import brillo
    brillo(im, 960, 420, 340 * e * brillo_r, rgb("ffe9a0"), 0.6)
    bombilla(im, 960, 430, 3.2 * e + 0.01, t, seed=10100)
    rotulo(im, "IDEAS DE LIBERTAD", 960, 860, 90, rgb("c27a1e"), t, seed=10101, esc=entra(t, tIdeas))
    if t > tEEUU - 0.2:
        ee = entra(t, tEEUU - 0.2)
        bandera_eeuu(im, 420, 420, 1.6 * ee + 0.01, t)
        letrero(im, "1776", 420, 640, 54, t, col=CREMA, seed=10110, esc=ee)
        rotulo(im, "ESTADOS UNIDOS", 420, 230, 44, AZUL, t, seed=10111, esc=ee)
    if t > tFrancia - 0.2:
        ef = entra(t, tFrancia - 0.2)
        bandera_francia(im, 1500, 420, 1.5 * ef + 0.01, t)
        letrero(im, "1789", 1500, 640, 54, t, col=CREMA, seed=10120, esc=ef)
        rotulo(im, "FRANCIA", 1500, 230, 44, ROJO, t, seed=10121, esc=ef)
    return im


def napoleon(t):
    im = cache(("fb", "sepia"), lambda: _fondo("sepia", 49)).copy()
    letrero(im, "1808", 960, 130, 70, t, col=AMARILLO, seed=10200, esc=entra(t, T_NAP + 0.1))
    # la silla del rey: se la jalan y el rey cae
    jalon = e_in(pr(t, tTrono - 0.4, tTrono + 0.1))
    sx = 1180 + 520 * jalon
    silla(im, sx, 720, 1.5, t, rot=0.25 * jalon)
    cae = e_in(pr(t, tTrono - 0.1, tTrono + 0.5))
    fx, fy = 1180 - 60 * cae, 520 + 300 * cae
    cam(im, "fernando", fx, fy, 0.62, t, "FERNANDO VII", seed=2, rot=-0.9 * cae)
    if cae > 0.9:
        for k in range(3):
            destello(im, fx - 120 + 120 * k, fy + 150, 0.8, t, seed=10210 + k)
    # Napoleón entra marchando
    en = e_out(pr(t, tNapo - 0.4, tNapo + 0.5))
    nx = -300 + 820 * en
    cam(im, "napoleon", nx, 500 + 12 * abs(math.sin(t * 6)) * (en < 1), 0.72, t, "NAPOLEÓN", seed=3)
    if en > 0.3:
        bicornio(im, nx, 300, 1.0, t)
        for k in range(4):
            gente(im, nx - 260 - 110 * k, 860 + 8 * math.sin(t * 8 + k), 2.2, t, seed=60 + k, col=AZUL, cara="enojo")
    if t > tJuego - 0.3:
        rotulo(im, "JUEGO DE LAS SILLAS", 960, 980, 76, ROJO, t, seed=10220, esc=entra(t, tJuego - 0.3))
    return im


def truco(t):
    im = cache(("fb", "calido3"), lambda: _fondo("calido", 51)).copy()
    letrero(im, "TRUCO: LAS 3 CAUSAS", 960, 150, 66, t, col=AMARILLO, seed=10300, esc=entra(t, T_TRU + 0.1))
    datos = [(tInj, "INJUSTICIA", rgb("f6a6a0"), 420), (tIde, "IDEAS", rgb("ffe9a0"), 960), (tNap, "NAPOLEÓN", rgb("b8c7e8"), 1500)]
    for k, (tk, txt, col, x) in enumerate(datos):
        e = entra(t, tk - 0.3)
        if e <= 0.01:
            continue
        tarjeta(im, x, 560, 430 * e, 520 * e, t, col, 10310 + k * 7, rot=(k - 1) * 0.04)
        if k == 0:
            for j, (w, c) in enumerate(((90, DORADO), (170, AZUL), (250, CAFE))):
                forma(im, rrect(x, 440 + j * 70, w * e, 56 * e, 8), c, t, 10320 + j, tinta=3)
        elif k == 1:
            bombilla(im, x, 500, 1.7 * e + 0.01, t, seed=10330)
        else:
            bicornio(im, x, 520, 1.4 * e, t, seed=10340)
        rotulo(im, txt, x, 740, 60 * e + 1, TINTA, t, seed=10350 + k, tinta=False)
        rotulo(im, str(k + 1), x - 170, 330, 70 * e + 1, ROJO, t, seed=10360 + k)
    return im


TRAMOS = [(T_INI, nueva_espana), (T_PIR, piramide), (T_CRI, criollo), (T_IDE, ideas), (T_NAP, napoleon), (T_TRU, truco)]


def _base(t):
    from comun import desborde
    i = max(k for k, (t0, _) in enumerate(TRAMOS) if t >= t0 or k == 0)
    t0, f = TRAMOS[i]
    if i > 0 and t < t0 + 0.7:
        return desborde(TRAMOS[i - 1][1](t), f(t), pr(t, t0, t0 + 0.7), W / 2, H / 2)
    return f(t)


def cuadro_crudo(t):
    im = _base(t)
    izq = T_PIR <= t < T_CRI
    papa(im, t, 160 if izq else 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
