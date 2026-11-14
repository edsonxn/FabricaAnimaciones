# -*- coding: utf-8 -*-
"""AUTOBIOGRAFÍA + ANÉCDOTA.
auto: «DOS TEXTOS QUE CUENTAN LA VIDA» → AUTO + BIO + GRAFÍA (uno mismo · vida · escribir, cada una con su dibujito) → «= ESCRIBIR
TU PROPIA VIDA» · yo: «YO» gigante (primera persona), la FOTO REAL del renglón «Yo nací en Juchipila» de su cuaderno, y tres
casillas HECHOS REALES ✓, EN ORDEN 1-2-3, SUEÑOS Y METAS ★ · clip: la anécdota = relato breve; tira de película larga
(AUTOBIOGRAFÍA = TODA LA PELÍCULA) contra un solo cuadro (ANÉCDOTA = UN CLIP) con «JA JA» · preguntas: las cinco preguntas, una por
palabra, junto a la foto real de su página · hotcake: cocina; el sartén lanza el hot cake, se queda pegado en el techo; la familia
se ríe; etiquetas CUÁNDO/DÓNDE/QUÉ/QUIÉNES/CÓMO ME SENTÍ que se van marcando → «¡AHÍ ESTÁN LAS 5!»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import estrella, palomita
from personajes import AMARILLO, corazon, destello
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, entra, gente, letrero, papa, tarjeta)
from piezas_es import ROSA_M, TURQ, ficha, hotcake, polaroid, sarten, tira
from piezas_fj import base

T_INI = T0("autobio")
A, N = "autobio", "anecdota"
tTextos, tAuto, tA, tB, tG, tEsc, tPropia = (ww(A, 0, "textos"), ww(A, 0, "autobiografia"), ww(A, 0, "auto", 1), ww(A, 0, "bio"),
                                             ww(A, 0, "grafia"), ww(A, 0, "escribir"), ww(A, 0, "propia"))
T_YO = ww(A, 1, "se") - 0.3
tPrim, tYo, tCuad, tJuchi, tHechos, tOrden, tSuenos = (ww(A, 1, "primera"), ww(A, 1, "yo"), ww(A, 1, "cuaderno"), ww(A, 1, "juchipila"),
                                                       ww(A, 1, "hechos"), ww(A, 1, "orden"), ww(A, 1, "suenos"))
T_CLIP = T0(N)
tAnec, tRelato, tCurioso, tPeli, tClip = ww(N, 0, "anecdota"), ww(N, 0, "relato"), ww(N, 0, "curioso"), ww(N, 0, "pelicula"), ww(N, 0, "clip")
T_PREG = ww(N, 1, "para") - 0.3
tCinco = ww(N, 1, "cinco")
PREGS = [("¿QUÉ OCURRIÓ?", ww(N, 1, "que")), ("¿DÓNDE?", ww(N, 1, "donde")), ("¿CUÁNDO?", ww(N, 1, "cuando")),
         ("¿QUIÉNES ESTABAN?", ww(N, 1, "quienes")), ("¿CÓMO ME SENTÍ?", ww(N, 1, "como"))]
T_HOT = ww(N, 2, "imaginense") - 0.3
tDom, tCoc, tPapa, tHot, tPeg, tTecho, tTodos, tRisa, tCinco2 = (ww(N, 2, "domingo"), ww(N, 2, "cocina"), ww(N, 2, "primo"),
                                                                 ww(N, 2, "hot"), ww(N, 2, "pegado"), ww(N, 2, "techo"),
                                                                 ww(N, 2, "todos"), ww(N, 2, "risa"), ww(N, 2, "cinco"))


def lapiz(im, x, y, s, t, seed):
    forma(im, np.array([(x - 120 * s, y - 18 * s), (x + 80 * s, y - 18 * s), (x + 130 * s, y), (x + 80 * s, y + 18 * s),
                        (x - 120 * s, y + 18 * s)], np.float32), AMARILLO, t, seed, tinta=3 * s)
    forma(im, np.array([(x + 80 * s, y - 18 * s), (x + 130 * s, y), (x + 80 * s, y + 18 * s)], np.float32), rgb("f4cfae"), t, seed + 1,
          tinta=2 * s)
    forma(im, rrect(x - 130 * s, y, 24 * s, 36 * s, 4 * s), rgb("f3a7b8"), t, seed + 2, tinta=2 * s)


def auto(t):
    im = cache("f_au", lambda: papel("calido")).copy()
    letrero(im, "DOS TEXTOS QUE CUENTAN LA VIDA", 760, 120, 54, t, col=AMARILLO, seed=16000, esc=entra(t, tTextos - 0.3), rot=-0.02)
    if t > tAuto - 0.3:
        rotulo(im, "AUTOBIOGRAFÍA", 760, 260, 96 * entra(t, tAuto - 0.3) + 1, ROSA_M, t, seed=16005)
    for k, (pz, sig, tk, x, col) in enumerate((("AUTO", "UNO MISMO", tA, 330, rgb("f6a6a0")), ("BIO", "VIDA", tB, 760, rgb("a8d8b0")),
                                              ("GRAFÍA", "ESCRIBIR", tG, 1190, rgb("b8c7e8")))):
        e = entra(t, tk - 0.2)
        if e <= 0.01:
            continue
        tarjeta(im, x, 560, 360 * e, 380 * e, t, col, 16010 + k * 9, rot=(k - 1) * 0.03)
        rotulo(im, pz, x, 430, 64 * e + 1, [ROJO, VERDE, AZUL][k], t, seed=16011 + k * 9)
        rotulo(im, "= " + sig, x, 715, 40 * e + 1, MORADO, t, seed=16012 + k * 9, tinta=False)
        if k == 0:
            gente(im, x, 540, 2.1 * e + 0.01, t, seed=16013, cara="normal", col=rgb("e35d4a"))
        elif k == 1:
            corazon(im, x, 560, 4.0 * e, t, seed=16014)
        else:
            lapiz(im, x, 560, 1.0 * e, t, 16015)
    if t > tPropia - 0.4:
        rotulo(im, "= ESCRIBIR TU PROPIA VIDA", 760, 860, 72, ROJO, t, seed=16030, esc=entra(t, tPropia - 0.4), rot=-0.02)
    return im


def yo(t):
    im = cache("f_yo", lambda: papel("rosa")).copy()
    letrero(im, "PRIMERA PERSONA", 380, 120, 54, t, col=AMARILLO, seed=16100, esc=entra(t, tPrim - 0.3), rot=-0.03)
    e = entra(t, tYo - 0.3)
    forma(im, elipse(380, 400, 190 * e + 1, 190 * e + 1), rgb("fde0dc"), t, 16105, tinta=6)
    rotulo(im, "YO", 380, 415, 180 * e + 1, ROSA_M, t, seed=16106)
    if t > tCuad - 0.4:
        polaroid(im, "juchipila", 1050, 330, 0.95 * entra(t, tCuad - 0.4), t, rot=-0.03, seed=16110)
        if t > tJuchi - 0.2:
            letrero(im, "«YO NACÍ EN JUCHIPILA»", 1050, 520, 46, t, col=CREMA, txt=TURQ, seed=16115, esc=entra(t, tJuchi - 0.2), rot=0.02)
    for k, (txt, tk) in enumerate((("HECHOS REALES", tHechos), ("EN ORDEN", tOrden), ("SUEÑOS Y METAS", tSuenos))):
        ek = entra(t, tk - 0.25)
        if ek <= 0.01:
            continue
        x = 300 + 450 * k
        tarjeta(im, x, 800, 400 * ek, 150 * ek, t, CREMA, 16120 + k * 6, rot=(k - 1) * 0.02)
        rotulo(im, txt, x + 30, 806, 40 * ek + 1, TINTA, t, seed=16121 + k * 6, tinta=False)
        if k == 0:
            palomita(im, x - 165, 800, 0.8 * ek, t, seed=16122, col=VERDE)
        elif k == 1:
            rotulo(im, "1·2·3", x - 150, 806, 34 * ek + 1, ROJO, t, seed=16128, tinta=False)
        else:
            estrella(im, x - 175, 800, 30 * ek + 1, t, AMARILLO, seed=16134)
    return im


def clip(t):
    im = cache("f_cl", lambda: papel("frio")).copy()
    letrero(im, "LA ANÉCDOTA", 330, 120, 60, t, col=AMARILLO, seed=16200, esc=entra(t, tAnec - 0.3), rot=-0.03)
    if t > tRelato - 0.3:
        rotulo(im, "RELATO BREVE DE ALGO", 900, 230, 50 * entra(t, tRelato - 0.3) + 1, TINTA, t, seed=16205, tinta=False)
    if t > tCurioso - 0.3:
        rotulo(im, "CURIOSO O DIVERTIDO", 900, 300, 56 * entra(t, tCurioso - 0.3) + 1, ROJO, t, seed=16206)
    if t > tPeli - 0.5:
        e = entra(t, tPeli - 0.5)
        tira(im, 760, 500, 1300 * e + 10, 170, t, n=9, seed=16210)
        letrero(im, "AUTOBIOGRAFÍA = TODA LA PELÍCULA", 760, 640, 42, t, col=CREMA, txt=MORADO, seed=16215, esc=e, rot=-0.02)
    if t > tClip - 0.4:
        e = entra(t, tClip - 0.4)
        tira(im, 560, 820, 300 * e + 10, 170, t, n=1, seed=16220, avanza=False)
        letrero(im, "ANÉCDOTA = UN CLIP", 1030, 820, 46, t, col=rgb("fde0dc"), txt=ROJO, seed=16225, esc=e, rot=0.02)
        for k in range(2):
            rotulo(im, "JA", 300, 770 + 110 * k + 14 * math.sin(t * 9 + k), 70, AMARILLO, t, seed=16230 + k,
                   esc=entra(t, tClip + 0.3 + 0.15 * k), rot=0.12 * (k - 0.5))
    return im


def preguntas(t):
    im = cache("f_pr", lambda: papel("calido")).copy()
    letrero(im, "5 PREGUNTAS", 330, 120, 60, t, col=AMARILLO, seed=16300, esc=entra(t, tCinco - 0.3), rot=-0.03)
    polaroid(im, "anecdota", 1230, 420, 0.8 * entra(t, T_PREG + 0.2), t, rot=0.05, seed=16305)
    for k, (txt, tk) in enumerate(PREGS):
        e = entra(t, tk - 0.2)
        if e <= 0.01:
            continue
        y = 260 + 135 * k
        tarjeta(im, 470, y, 640 * e, 110 * e, t, [rgb("f6a6a0"), rgb("b8c7e8"), rgb("a8d8b0"), rgb("f4d38a"), rgb("d8b8e8")][k],
                16310 + k * 5, rot=(k - 2) * 0.015)
        rotulo(im, f"{k + 1}. {txt}", 470, y + 4, 46 * e + 1, TINTA, t, seed=16311 + k * 5, tinta=False)
    return im


def _cocina():
    im = papel("calido")
    forma(im, np.array([(0, 0), (W, 0), (W, 120), (0, 140)], np.float32), rgb("f7f1e3"), 0, 16400, tinta=0)   # techo
    linea(im, [(0, 140), (W, 120)], 6, seed=16401)
    for k in range(10):                                                                                     # azulejos
        for j in range(3):
            forma(im, rrect(90 + 190 * k, 560 + 110 * j, 170, 95, 8), rgb("cfe8ea") if (k + j) % 2 else rgb("e6f2f0"), 0,
                  16410 + k * 3 + j, tinta=2)
    forma(im, rrect(760, 900, 1700, 70, 10), rgb("b98352"), 0, 16450, tinta=5)                               # barra
    forma(im, rrect(520, 860, 360, 40, 8), rgb("5a5a62"), 0, 16451, tinta=3)                                 # estufa
    return im


def hotcake_sc(t):
    im = cache("f_hc", _cocina).copy()
    # trayectoria del hot cake: sale del sartén, sube girando y se queda pegado en el techo
    u = pr(t, tHot - 0.2, tPeg - 0.1)
    rot_s = -0.35 * math.exp(-((t - tHot + 0.1) / 0.25) ** 2)
    if u <= 0:
        hotcake(im, 560, 780, 1.0, t, seed=16460)
    elif u < 1:
        x = 560 + 140 * u
        y = 780 - 640 * e_out(u)
        hotcake(im, x, y, 1.0, t, seed=16460, rot=u * 7)
    else:
        hotcake(im, 700, 160, 1.0, t, seed=16460, rot=0.0)
        for k in range(3):                                                          # gotitas de miel que cuelgan
            yy = 180 + 30 * min(1, (t - tPeg) * 0.8) + 8 * math.sin(t * 2 + k)
            forma(im, elipse(650 + 50 * k, yy, 8, 12), rgb("d9973f"), t, 16470 + k, tinta=1.5)
        if t < tPeg + 0.6:
            for k in range(5):
                destello(im, 700 + 140 * math.cos(k * 1.25), 170 + 50 * math.sin(k * 1.25), 0.7, t, seed=16475 + k)
    gente(im, 330, 700, 2.8, t, seed=16485, cara="susto" if t > tPeg else "normal", col=rgb("3f8f5a"))
    sarten(im, 560, 820, 1.0, t, seed=16480, rot=rot_s)
    if t > tTodos - 0.4:
        for k, (x, col) in enumerate(((1000, rgb("e35d4a")), (1180, AZUL), (1360, rgb("9b6ad1")))):
            ek = entra(t, tTodos - 0.4 + 0.12 * k)
            gente(im, x, 700 + 10 * math.sin(t * 9 + k), 2.6 * ek + 0.01, t, seed=16490 + k, cara="grito", col=col)
        if t > tRisa - 0.3:
            for k in range(3):
                rotulo(im, "JA", 1000 + 180 * k, 545 + 16 * math.sin(t * 10 + k), 80, ROJO, t, seed=16495 + k,
                       esc=entra(t, tRisa - 0.3 + 0.12 * k), rot=0.1 * (k - 1))
    # las cinco respuestas, como etiquetas
    for k, (q, r, tk) in enumerate((("¿CUÁNDO?", "EL DOMINGO", tDom), ("¿DÓNDE?", "EN LA COCINA", tCoc),
                                    ("¿QUÉ?", "HOT CAKE EN EL TECHO", tTecho), ("¿QUIÉNES?", "TODOS", tTodos),
                                    ("¿CÓMO?", "¡DE RISA!", tRisa))):
        e = entra(t, tk - 0.2)
        if e <= 0.01:
            continue
        x, y = [(1180, 230), (1180, 320), (380, 330), (1180, 410), (1180, 500)][k] if k != 2 else (300, 300)
        if k == 2:
            letrero(im, r, 330, 420, 40, t, col=rgb("fff2c0"), txt=ROJO, seed=16500 + k * 4, esc=e, rot=-0.03)
            continue
        letrero(im, f"{q} {r}", 1180, 200 + 80 * (k if k < 2 else k - 1), 38, t, col=CREMA, txt=MORADO, seed=16500 + k * 4, esc=e,
                rot=0.02 * (k % 2 * 2 - 1))
    if t > tCinco2 - 0.3:
        rotulo(im, "¡AHÍ ESTÁN LAS 5!", 760, 960, 76, VERDE, t, seed=16530, esc=entra(t, tCinco2 - 0.3), rot=-0.02)
        palomita(im, 1180, 960, 1.0 * entra(t, tCinco2), t, seed=16535, col=VERDE)
    return im


TRAMOS = [(T_INI, auto), (T_YO, yo), (T_CLIP, clip), (T_PREG, preguntas), (T_HOT, hotcake_sc)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
