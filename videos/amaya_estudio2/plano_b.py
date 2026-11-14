# -*- coding: utf-8 -*-
"""SÍLABAS + CLASIFICACIÓN.
silabas: «LAS SÍLABAS» → ondita de voz (golpecito) → dos manos aplauden en «es, cue, la» y en cada aplauso cae una ficha → «3» →
CUE crece y se encierra con plumón rosa («SÍLABA TÓNICA») → globo «¡PA-PÁ!» con PÁ encerrada → las etiquetas ÚLTIMA / PENÚLTIMA /
ANTEPENÚLTIMA aparecen de derecha a izquierda, junto a la FOTO REAL de su cuaderno con el mismo esquema (es-cue-la).
clasif: tres columnas AGUDA · GRAVE · ESDRÚJULA, cada una con su «medidor» de tres cuadritos (el rojo = dónde cae la fuerza) y
las palabras que dice la voz con la tónica encerrada; A-MA-YA con corazones → ES-DRÚ-JU-LA gigante («¡SE PONE DE EJEMPLO
SOLITA!») → camión de reversa (¡BIP!) que va dejando ÚLTIMA=AGUDA, PENÚLTIMA=GRAVE, ANTEPENÚLTIMA=ESDRÚJULA."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from personajes import AMARILLO, corazon, destello, kuri
from personajes_ia import globo
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, entra, letrero, papa, tarjeta)
from piezas_es import ROSA_M, TURQ, aplauso, camion, ficha, palabra, polaroid
from piezas_fj import base

T_INI = T0("silabas")
S, C = "silabas", "clasif"
tSil, tGolpe = ww(S, 0, "silabas"), ww(S, 0, "golpecito")
tEs, tCue, tLa, tTres = ww(S, 0, "es", 1), ww(S, 0, "cue"), ww(S, 0, "la", 1), ww(S, 0, "tres")
tFuerte, tTonica, tEscuela, tGritas, tPapa, tPa = (ww(S, 1, "fuerte"), ww(S, 1, "tonica"), ww(S, 1, "escuela"), ww(S, 1, "gritan"),
                                                  ww(S, 1, "campeon"), ww(S, 1, "on"))
tFinal, tUlt, tPen, tAnte = ww(S, 2, "final"), ww(S, 2, "ultima"), ww(S, 2, "penultima"), ww(S, 2, "antepenultima")
ETI = ["ANTEPENÚLTIMA", "PENÚLTIMA", "ÚLTIMA"]

T_C = T0(C)
tAguda, tCamaron, tCarton = ww(C, 0, "aguda"), ww(C, 0, "camaron"), ww(C, 0, "carton")
tGrave, tArbol, tCaballo, tVentana, tAmaya = (ww(C, 1, "grave"), ww(C, 1, "arbol"), ww(C, 1, "caballo"), ww(C, 1, "ventana"),
                                             ww(C, 1, "juchipila"))
tEsdr, tMaq, tRel, tMex = ww(C, 2, "esdrujula"), ww(C, 2, "maquina"), ww(C, 2, "relampago"), ww(C, 2, "mexico")
T_TRUCO = ww(C, 3, "truco") - 0.4
tDru, tJu, tSolita = ww(C, 3, "dru"), ww(C, 3, "ju"), ww(C, 3, "solita")
tEs3 = tDru - 0.75
T_CAM = ww(C, 4, "otro") - 0.4
tReversa, tU4, tAg4, tP4, tGr4, tA4, tEs4 = (ww(C, 4, "reversa"), ww(C, 4, "ultima"), ww(C, 4, "aguda"), ww(C, 4, "penultima"),
                                             ww(C, 4, "grave"), ww(C, 4, "antepenultima"), ww(C, 4, "esdrujula"))

COLS = [("AGUDA", 2, rgb("f6a6a0"), 300), ("GRAVE", 1, rgb("b8c7e8"), 760), ("ESDRÚJULA", 0, rgb("a8d8b0"), 1220)]
PALABRAS = [[(["CA", "MA", "RÓN"], 2, tCamaron), (["CAR", "TÓN"], 1, tCarton)],
            [(["ÁR", "BOL"], 0, tArbol), (["CA", "BA", "LLO"], 1, tCaballo), (["VEN", "TA", "NA"], 1, tVentana)],
            [(["MÁ", "QUI", "NA"], 0, tMaq), (["RE", "LÁM", "PA", "GO"], 1, tRel), (["MÉ", "XI", "CO"], 0, tMex)]]
T_COL = [tAguda, tGrave, tEsdr]


def ondita(im, x, y, t, t0, seed):
    u = pr(t, t0, t0 + 0.9)
    if 0 < u:
        n = 60
        xs = np.linspace(x - 260, x + 260, n)
        env = np.exp(-((xs - x) / 120) ** 2) * min(1, u * 3)
        ys = y + 70 * env * np.sin(xs / 14 - t * 20)
        linea(im, np.stack([xs, ys], 1), 7, TURQ, seed=seed, t=t, punta=False)


def silabas(t):
    im = cache("b_sil", lambda: papel("calido")).copy()
    letrero(im, "LAS SÍLABAS", 330, 110, 60, t, col=AMARILLO, seed=11000, esc=entra(t, tSil - 0.3), rot=-0.03)
    if t < tGolpe - 0.2:
        rotulo(im, "SÍ - LA - BAS", 760, 450, 130 * entra(t, tSil), ROSA_M, t, seed=11003, rot=-0.02)
    if tGolpe - 0.2 < t < tEs - 0.3:
        ondita(im, 760, 450, t, tGolpe - 0.2, 11005)
        rotulo(im, "UN GOLPECITO DE VOZ", 760, 620, 58, MORADO, t, seed=11006, esc=entra(t, tGolpe - 0.2))
    if t > tEs - 1.2:
        aplauso(im, 760, 800 if t < tTres + 0.8 else 2000, 1.7, t, [tEs, tCue, tLa], seed=11010)
        xs = palabra(im, ["ES", "CUE", "LA"], 760, 430, 92, t, tonica=1, t_ap=[tEs - 0.12, tCue - 0.12, tLa - 0.12], t_ton=tTonica - 0.2, seed=11020,
                     etiquetas=ETI, t_eti=tUlt - 0.2)
        # cada ficha entra con su aplauso (las tapamos con papel hasta su golpe: se pinta encima la ficha solo si ya sonó)
    if t > tTres - 0.2 and t < tFuerte - 0.3:
        rotulo(im, "3 APLAUSOS = 3 SÍLABAS", 760, 610, 64, ROJO, t, seed=11040, esc=entra(t, tTres - 0.2))
    if t > tTonica - 0.3 and t < tFinal - 0.3:
        letrero(im, "SÍLABA TÓNICA", 760, 230, 54, t, col=rgb("fde0dc"), txt=ROJO, seed=11045, esc=entra(t, tTonica - 0.3), rot=0.03)
        rotulo(im, "= LA MÁS FUERTE", 760, 640, 56, MORADO, t, seed=11046, esc=entra(t, tTonica), tinta=False)
    if t > tGritas - 0.3 and t < tFinal - 0.3:
        e = entra(t, tGritas - 0.3)
        globo(im, 1230, 300, 470, 150, "", t, px=44, lineas=[""], seed=11050, cola=(-1, 1), alfa=min(1, e * 1.5))
        if t > tPapa - 0.2:
            palabra(im, ["CAM", "PE", "ÓN"], 1230, 300, 50, t, tonica=2, t_ap=tPapa - 0.25, t_ton=tPa - 0.1, seed=11060, col=CREMA)
    if t > tFinal - 0.4:
        polaroid(im, "tonica", 1350, 560, 0.62 * entra(t, tFinal - 0.4), t, rot=0.06, seed=11070)
        letrero(im, "¡COMO EN TU CUADERNO!", 1270, 150, 40, t, col=CREMA, txt=TURQ, seed=11075, esc=entra(t, tFinal), rot=-0.03)
        if t > tUlt - 0.3:
            rotulo(im, "SE CUENTAN DESDE EL FINAL", 600, 230, 50, MORADO, t, seed=11080, esc=entra(t, tUlt - 0.3), tinta=False)
            flecha_atras(im, t, 860, 330, 340, entra(t, tUlt - 0.3), 11085)
    return im


def flecha_atras(im, t, x0, y, largo, e, seed):
    if e < 0.05:
        return
    linea(im, [(x0, y), (x0 - largo * e, y)], 8, ROSA_M, seed=seed, t=t)
    xa = x0 - largo * e
    forma(im, np.array([(xa - 26, y), (xa + 6, y - 20), (xa + 6, y + 20)], np.float32), ROSA_M, t, seed + 1, tinta=2)


def medidor(im, x, y, pos, t, seed, e=1.0):
    """Tres cuadritos (antepenúltima, penúltima, última); el de `pos` va en rojo y brinca."""
    for k in range(3):
        on = k == pos
        b = 8 * abs(math.sin(t * 5)) if on else 0
        forma(im, rrect(x + (k - 1) * 62, y - b, 50 * e, 50 * e, 8), ROJO if on else CREMA, t, seed + k, tinta=3)


def columnas(im, t, hasta=3):
    for c, (tit, pos, col, x) in enumerate(COLS[:hasta]):
        e = entra(t, T_COL[c] - 0.4)
        if e <= 0.01:
            continue
        tarjeta(im, x, 520, 430 * e, 760 * e, t, col, 11200 + c * 11, rot=(c - 1) * 0.015)
        rotulo(im, tit, x, 200, (60 if c < 2 else 52) * e + 1, TINTA, t, seed=11201 + c * 11, tinta=False)
        medidor(im, x, 290, pos, t, 11202 + c * 11, e)
        for k, (sils, ton, tk) in enumerate(PALABRAS[c]):
            if t > tk - 0.3:
                palabra(im, sils, x, 410 + k * 150, 38, t, tonica=ton, t_ap=tk - 0.3, t_ton=tk + 0.15, seed=11220 + c * 40 + k * 9,
                        paso=0.06)


def clasif(t):
    im = cache("b_cla", lambda: papel("frio")).copy()
    columnas(im, t)
    if t < tAguda - 0.4:
        e = entra(t, T_C + 0.2)
        rotulo(im, "¿DÓNDE CAE", 760, 380, 110 * e, MORADO, t, seed=11190)
        rotulo(im, "LA FUERZA?", 760, 520, 110 * e, ROJO, t, seed=11191)
        medidor(im, 760, 700, int(t * 2) % 3, t, 11195, 1.0)
    if t > tAmaya - 0.3:
        e = entra(t, tAmaya - 0.3)
        tarjeta(im, 760, 860, 560 * e, 130 * e, t, rgb("fde0dc"), 11300, rot=-0.02)
        palabra(im, ["JU", "CHI", "PI", "LA"], 760, 860, 44, t, tonica=2, t_ap=tAmaya - 0.3, t_ton=tAmaya + 0.3, seed=11310)
        for k in range(3):
            corazon(im, 560 + 400 * (k == 2) - 20 * k, 800 - 40 * pr(t, tAmaya, tAmaya + 3), 1.6 * entra(t, tAmaya + 0.3 + 0.15 * k), t,
                    seed=1060 + k)
    return im


def truco(t):
    im = cache("b_tru", lambda: papel("rosa")).copy()
    letrero(im, "TRUCO", 300, 110, 60, t, col=AMARILLO, seed=11400, esc=entra(t, T_TRUCO), rot=-0.04)
    rotulo(im, "«ESDRÚJULA» ES ESDRÚJULA", 760, 230, 70, MORADO, t, seed=11405, esc=entra(t, T_TRUCO + 0.6))
    palabra(im, ["ES", "DRÚ", "JU", "LA"], 760, 520, 110, t, tonica=1, t_ap=[tEs3 - 0.15, tDru - 0.15, tJu - 0.15, tJu + 0.25], t_ton=tDru, seed=11410,
            etiquetas=["ANTEPENÚLTIMA", "PENÚLTIMA", "ÚLTIMA"], t_eti=tDru + 0.1)
    if t > tSolita - 0.4:
        rotulo(im, "¡SE PONE DE EJEMPLO SOLITA!", 700, 880, 60, ROJO, t, seed=11420, esc=entra(t, tSolita - 0.4), rot=0.02)
        kuri(im, 1350, 800 + 10 * math.sin(t * 8), 1.4 * entra(t, tSolita - 0.2), t, cara="feliz", brazos=(1.5, 1.5))
    return im


def reversa(t):
    im = cache("b_rev", _fondo_calle).copy()
    letrero(im, "CUENTA DE REVERSA", 420, 110, 58, t, col=AMARILLO, seed=11500, esc=entra(t, T_CAM), rot=-0.03)
    # el camión va de derecha a izquierda (de reversa) mientras la voz dice última → penúltima → antepenúltima
    u = suave(pr(t, tReversa - 0.3, tEs4 + 0.6))
    xc = 1250 - 900 * u
    for k, (xs, eti, tipo, col, tE, tT) in enumerate(((1250, "ÚLTIMA", "AGUDA", rgb("f6a6a0"), tU4, tAg4),
                                                      (830, "PENÚLTIMA", "GRAVE", rgb("b8c7e8"), tP4, tGr4),
                                                      (410, "ANTEPENÚLTIMA", "ESDRÚJULA", rgb("a8d8b0"), tA4, tEs4))):
        e = entra(t, tE - 0.25)
        if e > 0.01:
            tarjeta(im, xs, 330, 380 * e, 200 * e, t, col, 11510 + k * 7, rot=(k - 1) * 0.03)
            rotulo(im, eti, xs, 300, (36 if k == 2 else 44) * e + 1, TINTA, t, seed=11511 + k * 7, tinta=False)
            rotulo(im, "=", xs, 345, 34 * e + 1, GRIS, t, seed=11512 + k * 7, tinta=False)
            et = entra(t, tT - 0.2)
            rotulo(im, tipo, xs, 395, 50 * et + 1, ROJO, t, seed=11513 + k * 7, tinta=False)
    camion(im, xc, 740, 1.05, t, seed=11550, bip=1.0 if tReversa - 0.3 < t < tEs4 + 0.6 else 0.0)
    return im


def _fondo_calle():
    im = papel("calido")
    _manchas(im, rgb("bcd8ee"), 5, 77, r=(260, 420), alfa=0.2, y=(0, 600))
    forma(im, np.array([(0, 820), (W, 800), (W, H), (0, H)], np.float32), rgb("8f8f96"), 0, 11590, tinta=3)
    for k in range(8):
        forma(im, rrect(120 + 250 * k, 940, 140, 18, 6), rgb("f2e6b8"), 0, 11591 + k, tinta=0)
    return im


TRAMOS = [(T_INI, silabas), (T_C, clasif), (T_TRUCO, truco), (T_CAM, reversa)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
