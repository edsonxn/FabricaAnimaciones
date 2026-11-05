# -*- coding: utf-8 -*-
"""ORIGEN: ¿de qué está hecho? (la barrita se desenvuelve, «¿COMIDA?» tachado) → selva: el chicozapote con cortes en
zigzag que sueltan savia blanca + FOTO REAL del chiclero → el maya que mastica («tzictli» → «CHICLE») → papel sepia:
camafeos REALES de Santa Anna y Thomas Adams, el hule (llanta), la olla que fracasa, «ñam» → caja «Adams' New York Gum»
≈1870 → hoy: GOMA BASE (llanta + pegamento) → el azúcar y el sabor se van, queda la bolita gris."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, desborde, ww
from fondos_chicle import papel, selva
from iconos_ia import marca_x, personita
from personajes import AMARILLO, BLANCO, destello, gota, kuri, nube_lluvia, pregunta
from utileria import vapor
from personajes_ia import camafeo, nina, pegar, retrato
from piezas_chicle import (GRIS, ROJO, ROSA_CH, caja_antigua, chicle, chicle_barra, llanta, pegamento)

T_INI = T0("origen")
O = "origen"
tHecho, tComida = ww(O, 0, "hecho"), ww(O, 0, "comida")
tArbol, tChico, tCortas, tSavia = ww(O, 1, "arbol"), ww(O, 1, "chicozapote"), ww(O, 1, "cortas"), ww(O, 1, "savia")
tMayas, tTzic, tChicle2 = ww(O, 2, "mayas"), ww(O, 2, "tzictli"), ww(O, 2, "chicle")
tRaro, tEEUU, tSanta = ww(O, 3, "raro"), ww(O, 3, "estados"), ww(O, 3, "santa")
tDester, tHule, tAdams, tFracaso, tNoto, tMastica = (ww(O, 4, "desterrado"), ww(O, 4, "hule"), ww(O, 4, "thomas"),
                                                     ww(O, 4, "fracaso"), ww(O, 4, "noto"), ww(O, 4, "masticaba"))
tNacio, tTienda = ww(O, 5, "nacio"), ww(O, 5, "tienda")
tHoy, tFabrica, tLlanta, tPega = ww(O, 6, "hoy"), ww(O, 6, "fabrica"), ww(O, 6, "llanta"), ww(O, 6, "pegamento")
tAzucar, tSabor, tQueda, tGris, tTragaste = (ww(O, 7, "azucar"), ww(O, 7, "sabor"), ww(O, 7, "queda"), ww(O, 7, "gris"),
                                             ww(O, 7, "tragaste"))
T_SELVA = tArbol - 0.5
T_SEPIA = tRaro - 0.4
T_HOY = tHoy - 0.4


# ------------------------------------------------------------ 1. ¿de qué está hecho?
def mesa(t):
    im = papel("rosa")
    abre = 1 - e_out(pr(t, T_INI + 0.3, tHecho + 0.4))
    chicle_barra(im, 900, 620, 2.7, t, envuelto=abre, rot=-0.08)
    kuri(im, 360, 470 + 15 * math.sin(t * 1.6), 2.3, t, cara="normal")
    pregunta(im, 540, 210, 1.3 * e_back(pr(t, T_INI + 0.4, T_INI + 0.7)), t)
    if t > tComida - 0.3:
        e = e_back(pr(t, tComida - 0.3, tComida))
        forma(im, elipse(1500, 430, 210 * e + 1, 84 * e + 1), BLANCO, t, 9000, tinta=4)                 # platito
        linea(im, [(1260, 330), (1260, 530)], 10 * e + 1, seed=9001, t=t, punta=False)
        linea(im, [(1740, 330), (1740, 530)], 10 * e + 1, seed=9002, t=t, punta=False)
        rotulo(im, "¿COMIDA?", 1500, 230, 110, AMARILLO, t, seed=9003, esc=e)
        if t > tComida + 0.35:
            marca_x(im, 1500, 430, 1.8 * e_back(pr(t, tComida + 0.35, tComida + 0.6)), t, seed=9004)
    return im


# ------------------------------------------------------------ 2. selva, chicozapote, chiclero y mayas
def _zigzag(t, u):
    """Cortes en zigzag sobre el tronco (x 1340..1600); u = cuánto se han hecho."""
    pts = []
    for k in range(9):
        y = 180 + k * 85
        x = 1380 if k % 2 == 0 else 1560
        pts.append((x, y))
    n = int(len(pts) * u)
    return pts[:max(2, n + 1)] if u > 0 else []


def bosque(t):
    im = selva()
    rotulo(im, "CHICOZAPOTE", 1470, 120, 74, AMARILLO, t, seed=9100, esc=e_back(pr(t, tChico - 0.1, tChico + 0.2)))
    if t > T_SELVA + 0.4:
        rotulo(im, "SURESTE DE MÉXICO Y CENTROAMÉRICA", 700, 1010, 46, BLANCO, t, seed=9101,
               esc=e_back(pr(t, T_SELVA + 0.4, T_SELVA + 0.7)), alfa=1 - pr(t, tMayas - 0.4, tMayas))
    # cortes y savia
    u = e_out(pr(t, tCortas - 0.1, tCortas + 1.0))
    z = _zigzag(t, u)
    if len(z) >= 2:
        linea(im, z, 9, col=rgb("3a2414"), seed=9110, t=t, punta=False)
        linea(im, z, 4, col=rgb("f2ead8"), seed=9111, t=t, punta=False, alfa=pr(t, tSavia - 0.2, tSavia + 0.6))
    if t > tSavia - 0.2:
        v = pr(t, tSavia - 0.2, tSavia + 2.5)
        for k in range(4):                                                       # gotas de savia que bajan
            y = 860 + ((t * 120 + k * 50) % 120)
            forma(im, elipse(1470, y, 9, 13), rgb("f7f2e6"), t, 9120 + k, tinta=2, alfa=v)
        forma(im, curva([(1410, 950), (1530, 950), (1510, 1060), (1430, 1060)], 4, True), rgb("c9a25a"), t, 9130, tinta=3.6)
        forma(im, elipse(1470, 955, 60, 14), rgb("f7f2e6"), t, 9131, tinta=2, alfa=v)
        rotulo(im, "SAVIA", 1700, 900, 60, BLANCO, t, seed=9132, esc=e_back(pr(t, tSavia, tSavia + 0.25)))
    # foto real del chiclero
    if t > T_SELVA + 0.3:
        img = retrato("chiclero", 400, 540)
        sale = pr(t, tMayas - 0.3, tMayas + 0.2)
        pegar(im, img, lerp(560, -300, e_in(sale)), 470, e_back(pr(t, T_SELVA + 0.3, T_SELVA + 0.7)), -0.05, t=t, seed=9140)
        if sale < 0.5:
            rotulo(im, "CHICLERO PICANDO UN CHICOZAPOTE", 560, 870, 38, BLANCO, t, seed=9141,
                   esc=e_back(pr(t, tChico + 0.2, tChico + 0.5)), alfa=1 - 2 * sale)
    # el maya que mastica
    if t > tMayas - 0.3:
        e = e_back(pr(t, tMayas - 0.3, tMayas + 0.1))
        mx, my = 560, 560
        personita(im, mx, my, 4.2 * e + 0.01, t, seed=3, col=rgb("e8b53e"), piel=rgb("a8754c"))
        for k in range(5):                                                        # penacho
            a = -math.pi / 2 + (k - 2) * 0.35
            forma(im, elipse(mx + 120 * e * math.cos(a), my - 70 * e + 120 * e * math.sin(a), 18 * e + 1, 52 * e + 1, a + math.pi / 2),
                  rgb(["3f9a6a", "e35d4a", "3f78c8"][k % 3]), t, 9150 + k, tinta=3)
        forma(im, elipse(mx, my - 14 * 4.2 * e, 24 * 4.2 * e + 1, 12 * 4.2 * e + 1), rgb("1e1e22"), t, 9158, tinta=0)
        for sx_ in (-1, 1):
            forma(im, elipse(mx + sx_ * 34 * e, my - 4 * e, 9 * e + 1, 12 * e + 1), TINTA, t, 9159 + sx_, tinta=0)
            brillo(im, mx + sx_ * 34 * e - 3 * e, my - 9 * e, 4 * e + 1, BLANCO, 0.9)
        mand = 0.5 + 0.5 * math.sin(t * 9)                                        # mastica
        forma(im, elipse(mx, my + 30 * e, 22 * e + 1, (6 + 10 * mand) * e + 1), rgb("6a2b2b"), t, 9160, tinta=2.4)
        if t < tTzic - 0.2:
            rotulo(im, "ÑAM", mx + 190, my - 40, 56, BLANCO, t, seed=9161, esc=e * (0.8 + 0.2 * mand))
    if t > tTzic - 0.2:
        e = e_back(pr(t, tTzic - 0.2, tTzic + 0.15))
        forma(im, rrect(900, 300, 380 * e + 1, 120 * e + 1, 20), rgb("f7ecd4"), t, 9170, tinta=4)
        rotulo(im, "TZICTLI", 900, 300, 78, rgb("8a5a34"), t, seed=9171, esc=e, tinta=False)
    if t > tChicle2 - 0.2:
        e = e_back(pr(t, tChicle2 - 0.2, tChicle2 + 0.15))
        linea(im, [(900, 380), (900, 470)], 8, seed=9172, t=t)
        rotulo(im, "CHICLE", 900, 540, 96, AMARILLO, t, seed=9173, esc=e)
    return im


# ------------------------------------------------------------ 3. Santa Anna y Thomas Adams
def sepia(t):
    im = papel("sepia")
    ea = e_back(pr(t, tSanta - 0.3, tSanta + 0.1))
    sx = lerp(960, 480, suave(pr(t, tAdams - 0.6, tAdams)))
    if t < tNacio:
        camafeo(im, retrato("santa_anna", 300, 380), sx, 450, ea, t, nombre="ANTONIO LÓPEZ DE SANTA ANNA", seed=9200)
    if t < tDester:
        al = 1 - pr(t, tSanta + 0.2, tSanta + 0.8)
        ruta = [(lerp(330, 1450, k / 30), 760 - 520 * (k / 30) - 260 * math.sin(math.pi * k / 30)) for k in range(31)]
        rotulo(im, "MÉXICO", 330, 860, 64, rgb("3f7a4a"), t, seed=9203, esc=e_back(pr(t, T_SEPIA + 0.3, T_SEPIA + 0.6)), alfa=al)
        uu = e_out(pr(t, tRaro, tEEUU + 0.6))
        n = max(2, int(31 * uu))
        for k in range(0, n - 1, 2):
            linea(im, ruta[k:k + 2], 6, col=rgb("8a5a34"), seed=9204 + k, t=t, punta=False, alfa=0.8 * al)
        if al > 0.02:
            chicle(im, ruta[n - 1][0], ruta[n - 1][1], 72, t, seed=9205, col=rgb("efe6cf"), cara="feliz")
            kuri(im, 1650, 760 + 12 * math.sin(t * 1.6), 1.9 * al + 0.01, t, cara="susto" if t < tEEUU else "normal")
            pregunta(im, 1760, 600, al * e_back(pr(t, tRaro, tRaro + 0.3)), t)
    if t > tEEUU - 0.2 and t < tDester:
        rotulo(im, "ESTADOS UNIDOS", 1450, 200, 60, rgb("8a5a34"), t, seed=9201, esc=e_back(pr(t, tEEUU - 0.2, tEEUU + 0.1)))
    if t > tDester - 0.2:
        rotulo(im, "DESTERRADO EN NUEVA YORK", W / 2, 110, 64, rgb("8a5a34"), t, seed=9202,
               esc=e_back(pr(t, tDester - 0.2, tDester + 0.1)), alfa=1 - pr(t, tNacio - 0.4, tNacio))
    if tHule - 0.2 < t < tAdams + 0.4:
        e = e_back(pr(t, tHule - 0.2, tHule + 0.1)) * (1 - pr(t, tAdams, tAdams + 0.4))
        llanta(im, 1450, 520, 170 * e + 1, t)
        rotulo(im, "HULE", 1450, 780, 70, BLANCO, t, seed=9210, esc=e)
    if tAdams - 0.3 < t < tNacio:
        e = e_back(pr(t, tAdams - 0.3, tAdams + 0.1))
        camafeo(im, retrato("adams", 300, 380), 1440, 450, e, t, nombre="THOMAS ADAMS", seed=9220)
    if tFracaso - 1.2 < t < tNoto:                                                  # la olla que no funciona
        e = e_back(pr(t, tFracaso - 1.2, tFracaso - 0.9))
        ox, oy = 960, 820
        forma(im, curva([(ox - 110 * e, oy - 60 * e), (ox + 110 * e, oy - 60 * e), (ox + 90 * e, oy + 70 * e), (ox - 90 * e, oy + 70 * e)],
                        4, True), rgb("4b4b55"), t, 9230, tinta=4)
        forma(im, elipse(ox, oy - 60 * e, 110 * e + 1, 22 * e + 1), rgb("f2ead8"), t, 9231, tinta=3)
        vapor(im, ox, oy - 100, e, t, seed=9232)
        if t > tFracaso - 0.1:
            nube_lluvia(im, ox, oy - 260, 1.1 * e_back(pr(t, tFracaso - 0.1, tFracaso + 0.2)), t)
            marca_x(im, ox + 170, oy - 30, 0.8, t, seed=9233)
    if t > tMastica - 0.3 and t < tNacio:
        mand = 0.5 + 0.5 * math.sin(t * 10)
        rotulo(im, "ÑAM ÑAM", 480, 860, 70 * (0.85 + 0.15 * mand), AMARILLO, t, seed=9240,
               esc=e_back(pr(t, tMastica - 0.3, tMastica)))
        chicle(im, 640, 300, 40 * e_back(pr(t, tMastica - 0.3, tMastica)) + 1, t, seed=9241, col=rgb("efe6cf"))
    if t > tNacio - 0.4:
        e = e_back(pr(t, tNacio - 0.4, tNacio))
        lavado(im, rrect(960, 560, 1920, 1100, 0), rgb("efe0c0"), 0.85 * e, 9250)
        caja_antigua(im, 960, 560, 1.7 * e + 0.01, t)
        rotulo(im, "≈ 1870", 960, 860, 90, rgb("8a5a34"), t, seed=9251, esc=e_back(pr(t, tNacio, tNacio + 0.3)))
        rotulo(im, "EL CHICLE DE TIENDA", 960, 170, 80, ROJO, t, seed=9252, esc=e_back(pr(t, tTienda - 0.2, tTienda + 0.1)))
    return im


# ------------------------------------------------------------ 4. hoy: goma base, azúcar y sabor que se van
def hoy(t):
    im = papel("frio")
    pasa = suave(pr(t, tAzucar - 0.3, tGris))                                    # barrita rosa → bolita gris
    if pasa < 0.98:
        col = ROSA_CH * (1 - pasa) + GRIS * pasa
        if pasa < 0.5:
            chicle_barra(im, 960, 540, 2.4 * (1 - pasa * 0.6), t, col=col, envuelto=0)
        else:
            chicle(im, 960, 540, lerp(220, 175, pasa), t, seed=9300, col=col)
    else:
        chicle(im, 960, 540, 175, t, seed=9300, cara="normal" if t < tTragaste else "susto")
    if t < tAzucar - 0.3:
        rotulo(im, "HOY", 960, 150, 90, ROJO, t, seed=9309, esc=e_back(pr(t, tHoy - 0.2, tHoy + 0.1)), alfa=1 - pr(t, tFabrica - 0.4, tFabrica - 0.2))
        rotulo(im, "GOMA BASE", 960, 220, 110, rgb("2f4f86"), t, seed=9310, esc=e_back(pr(t, tFabrica - 0.2, tFabrica + 0.15)))
        if t > tHoy - 0.2:                                                       # árbol tachado
            e = e_back(pr(t, tHoy - 0.2, tHoy + 0.1))
            forma(im, rrect(300, 400, 70 * e + 1, 260 * e + 1, 8), rgb("8a6a4e"), t, 9320, tinta=3.4)
            forma(im, elipse(300, 240, 190 * e + 1, 150 * e + 1), rgb("5e9c56"), t, 9321, tinta=4)
            marca_x(im, 300, 320, 1.9 * e_back(pr(t, tHoy + 0.4, tHoy + 0.6)), t, seed=9322)
        if t > tFabrica - 0.4:                                                   # la fábrica
            e = e_back(pr(t, tFabrica - 0.4, tFabrica))
            fx, fy = 1470, 330
            forma(im, rrect(fx, fy + 40 * e, 360 * e + 1, 180 * e + 1, 6), rgb("c9b9a6"), t, 9323, tinta=4)
            for k in range(3):
                forma(im, np.array([(fx - 180 * e + k * 120 * e, fy - 50 * e), (fx - 60 * e + k * 120 * e, fy - 50 * e),
                                    (fx - 60 * e + k * 120 * e, fy - 110 * e)], np.float32), rgb("b08f7a"), t, 9324 + k, tinta=3)
            forma(im, rrect(fx + 130 * e, fy - 150 * e, 44 * e + 1, 200 * e + 1, 4), rgb("8d857b"), t, 9328, tinta=3)
            vapor(im, fx + 130 * e, fy - 270 * e, e, t, seed=9329)
            for k in range(3):
                forma(im, rrect(fx - 110 * e + k * 110 * e, fy + 60 * e, 50 * e + 1, 50 * e + 1, 4), AMARILLO, t, 9330 + k, tinta=2.4)
        if t > tLlanta - 0.3:
            llanta(im, 420, 800, 190 * e_back(pr(t, tLlanta - 0.3, tLlanta)) + 1, t)
        if t > tPega - 0.3:
            pegamento(im, 1480, 790, 1.8 * e_back(pr(t, tPega - 0.3, tPega)) + 0.01, t)
        if t > tLlanta:
            rotulo(im, "PARIENTES", 960, 920, 80, ROJO, t, seed=9330, esc=e_back(pr(t, tLlanta, tLlanta + 0.3)))
    else:
        u = pr(t, tAzucar - 0.2, tQueda)
        for k in range(14):                                                     # azúcar y sabor que se van
            a = k * 0.9
            d = 230 + 560 * u
            x, y = 960 + d * math.cos(a), 520 + d * 0.6 * math.sin(a) - 200 * u
            al = 1 - pr(t, tQueda - 0.6, tQueda)
            if k % 2 == 0:
                forma(im, rrect(x, y, 54, 54, 8, a), BLANCO, t, 9340 + k, tinta=2.8, alfa=al)
            elif t > tSabor - 0.3:
                forma(im, elipse(x, y, 34, 34), rgb(["e35d4a", "f39bc0", "8fd18a"][k % 3]), t, 9340 + k, tinta=2, alfa=al)
        rotulo(im, "AZÚCAR", 520, 200, 70, BLANCO, t, seed=9350, esc=e_back(pr(t, tAzucar - 0.1, tAzucar + 0.2)),
               alfa=1 - pr(t, tQueda - 0.4, tQueda))
        rotulo(im, "SABOR", 1400, 200, 70, rgb("e35d4a"), t, seed=9351, esc=e_back(pr(t, tSabor - 0.1, tSabor + 0.2)),
               alfa=1 - pr(t, tQueda - 0.4, tQueda))
        if t > tGris - 0.6:                                                    # la niña que se la va a tragar
            en = e_back(pr(t, tGris - 0.6, tGris - 0.2))
            nina(im, 360, 600 + 4 * math.sin(t * 2), 1.45 * en + 0.01, t, cara="susto" if t > tTragaste - 0.2 else "normal",
                 boca="abierta" if t > tTragaste - 0.2 else "sonrisa", brazos=(1.9, 1.9) if t > tTragaste - 0.2 else (0.3, 0.3),
                 mira=0.9)
        if t > tGris - 0.2:
            rotulo(im, "LA BOLITA GRIS", 960, 860, 100, rgb("6e6a68"), t, seed=9360, esc=e_back(pr(t, tGris - 0.2, tGris + 0.1)))
        if t > tTragaste - 0.3:
            rotulo(im, "¡LA QUE TE TRAGASTE!", 960, 190, 90, AMARILLO, t, seed=9361, rot=-0.04,
                   esc=e_back(pr(t, tTragaste - 0.3, tTragaste)))
    kuri(im, 1760, 560 + 14 * math.sin(t * 1.5), 1.5, t, cara="feliz" if t < tGris else "susto")
    return im


def cuadro_crudo(t):
    pasos = [(T_INI, mesa), (T_SELVA, bosque), (T_SEPIA, sepia), (T_HOY, hoy)]
    for i in range(len(pasos) - 1, -1, -1):
        t0, f = pasos[i]
        if t >= t0:
            if i > 0 and t < t0 + 0.8:
                return desborde(pasos[i - 1][1](t), f(t), pr(t, t0, t0 + 0.8), W / 2, H / 2)
            return f(t)
    return mesa(t)


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
