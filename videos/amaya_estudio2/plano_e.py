# -*- coding: utf-8 -*-
"""ADVERBIOS + PREGUNTA 3 + RESPUESTA 3.
defin: «LOS ADVERBIOS», tarjeta VERBO (CORRE) con la tarjeta ADVERBIO que se le pega y las cuatro preguntas ¿CÓMO? ¿CUÁNDO? ¿DÓNDE?
¿CUÁNTO? alrededor · ejemplos: la FOTO REAL de las 4 oraciones de su cuaderno + las mismas oraciones con el adverbio en color ·
verbo: «PREGÚNTALE AL VERBO» → 4 tarjetas pregunta → TIPO (LUGAR, TIEMPO, MODO, CANTIDAD) · opinan: AFIRMACIÓN ✓, NEGACIÓN ✗, DUDA ? ·
mente: «-MENTE» en RÁPIDAMENTE / CUIDADOSAMENTE y un cerebro tachado · ronca: cama con Zzz, MUCHO = CANTIDAD, SIEMPRE = TIEMPO,
«¡Y ES VERDAD!» · preg3: «JUAN LLEGÓ AYER» con «?» y cuenta · resp3: AYER encerrado → ¿CUÁNDO? → TIEMPO ✓."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from fondos_amaya import papel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, gente, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, ficha, polaroid
from piezas_fj import base, cama, zzz

T_INI = T0("adverbios")
A, P, R = "adverbios", "preg3", "resp3"
tAdv, tVerbo, tQs = ww(A, 0, "adverbios"), ww(A, 0, "verbo"), [ww(A, 0, w) for w in ("como", "cuando", "donde", "cuanto")]
T_EJ = ww(A, 1, "como") - 0.3
tCuad = ww(A, 1, "cuaderno")
EJ = [("SANTIAGO CORRE", "RÁPIDAMENTE", ww(A, 1, "santiago"), ww(A, 1, "rapidamente")),
      ("JUAN LLEGÓ", "AYER", ww(A, 1, "juan"), ww(A, 1, "ayer")),
      ("NATALIA ESTUDIA", "MUCHO", ww(A, 1, "natalia"), ww(A, 1, "mucho")),
      ("LOS NIÑOS ESTUDIAN", "AQUÍ", ww(A, 1, "ninos") - 0.3, ww(A, 1, "aqui"))]
T_VB = ww(A, 2, "truco") - 0.3
tPreg = ww(A, 2, "pregunten")
TIPOS = [("¿DÓNDE?", "LUGAR", "aquí, lejos", rgb("f6a6a0"), ww(A, 2, "donde"), ww(A, 2, "lugar")),
         ("¿CUÁNDO?", "TIEMPO", "ayer, hoy", rgb("b8c7e8"), ww(A, 2, "cuando"), ww(A, 2, "tiempo")),
         ("¿CÓMO?", "MODO", "bien, rápido", rgb("a8d8b0"), ww(A, 2, "como"), ww(A, 2, "modo")),
         ("¿CUÁNTO?", "CANTIDAD", "mucho, poco", rgb("f4d38a"), ww(A, 2, "cuanto"), ww(A, 2, "cantidad"))]
T_OP = ww(A, 3, "y") - 0.3
tOpinan = ww(A, 3, "opinan")
OPI = [("SÍ · TAMBIÉN", "AFIRMACIÓN", ww(A, 3, "si"), ww(A, 3, "afirmacion"), "ok"),
       ("NO · NUNCA", "NEGACIÓN", ww(A, 3, "no"), ww(A, 3, "negacion"), "x"),
       ("QUIZÁ · PROBABLEMENTE", "DUDA", ww(A, 3, "quiza"), ww(A, 3, "duda"), "?")]
T_MEN = ww(A, 4, "dato") - 0.3
tMente, tRap, tCuid, tTienen, tCerebro = (ww(A, 4, "mente"), ww(A, 4, "rapidamente"), ww(A, 4, "cuidadosamente"), ww(A, 4, "tienen"),
                                          ww(A, 4, "cerebro"))
T_RON = ww(A, 5, "ejemplo") - 0.3
tRonca, tMucho, tCant, tSiempre, tTiempo, tVerdad = (ww(A, 5, "ladra"), ww(A, 5, "mucho"), ww(A, 5, "cantidad"), ww(A, 5, "siempre"),
                                                     ww(A, 5, "tiempo"), ww(A, 5, "tiempo") + 0.8)
T_P3 = T0(P)
tP3, tJuan, tCual, tTipo, tFinP3 = ww(P, 0, "pausa"), ww(P, 0, "juan"), ww(P, 0, "adverbio"), ww(P, 0, "tipo"), FIN(P)
T_R3 = T0(R)
tAyer, tCuando, tTiem, tEso = ww(R, 0, "ayer"), ww(R, 0, "cuando"), ww(R, 0, "tiempo"), ww(R, 0, "eso")


def defin(t):
    im = cache("e_de", lambda: papel("frio")).copy()
    letrero(im, "LOS ADVERBIOS", 760, 120, 66, t, col=AMARILLO, seed=15000, esc=entra(t, tAdv - 0.3), rot=-0.02)
    if t > tVerbo - 0.4:
        e = entra(t, tVerbo - 0.4)
        tarjeta(im, 600, 480, 360 * e, 200 * e, t, rgb("f6a6a0"), 15010, rot=-0.03)
        rotulo(im, "VERBO", 600, 420, 34 * e + 1, TINTA, t, seed=15011, tinta=False)
        rotulo(im, "CORRE", 600, 500, 80 * e + 1, ROJO, t, seed=15012, rot=-0.03)
        u = suave(pr(t, tVerbo + 0.2, tVerbo + 0.8))
        xa = 1300 - 380 * u
        tarjeta(im, xa, 480, 360, 200, t, rgb("a8d8b0"), 15015, rot=0.03, alfa=min(1, u * 3))
        rotulo(im, "ADVERBIO", xa, 420, 34, TINTA, t, seed=15016, tinta=False, alfa=min(1, u * 3))
        rotulo(im, "RÁPIDO", xa, 500, 72, VERDE, t, seed=15017, rot=0.03, alfa=min(1, u * 3))
    for k, (txt, (x, y)) in enumerate(zip(("¿CÓMO?", "¿CUÁNDO?", "¿DÓNDE?", "¿CUÁNTO?"), ((330, 760), (640, 820), (950, 820), (1260, 760)))):
        e = entra(t, tQs[k] - 0.2)
        if e > 0.01:
            letrero(im, txt, x, y, 50, t, col=CREMA, txt=MORADO, seed=15020 + k * 4, esc=e, rot=(k - 1.5) * 0.04)
    return im


def ejemplos(t):
    im = cache("e_ej", lambda: papel("calido")).copy()
    polaroid(im, "adv_ejemplos", 1220, 580, 0.7 * entra(t, tCuad - 0.4), t, rot=0.04, seed=15100)
    letrero(im, "COMO EN SU CUADERNO", 420, 110, 50, t, col=CREMA, txt=TURQ, seed=15105, esc=entra(t, tCuad - 0.3), rot=-0.03)
    for k, (fr, adv, t0, t1) in enumerate(EJ):
        e = entra(t, t0 - 0.2)
        if e <= 0.01:
            continue
        y = 300 + 160 * k
        x0 = 120
        w = len(fr) * 50 * 0.58
        rotulo(im, fr, x0 + w / 2, y, 50 * e + 1, TINTA, t, seed=15110 + k * 5, tinta=False)
        if t > t1 - 0.25:
            letrero(im, adv, x0 + w + 40 + len(adv) * 15, y, 50, t, col=rgb("fff2c0"), txt=rgb("e08a1e"), seed=15112 + k * 5,
                    esc=entra(t, t1 - 0.25), rot=0.03)
    return im


def verbo(t):
    im = cache("e_vb", lambda: papel("rosa")).copy()
    letrero(im, "PREGÚNTENLE AL VERBO", 760, 120, 62, t, col=AMARILLO, seed=15200, esc=entra(t, tPreg - 0.3), rot=-0.02)
    for k, (q, tipo, ej, col, tq, tt) in enumerate(TIPOS):
        x = 260 + 340 * k
        e = entra(t, tq - 0.25)
        if e <= 0.01:
            continue
        tarjeta(im, x, 500, 300 * e, 560 * e, t, col, 15210 + k * 7, rot=(k - 1.5) * 0.02)
        rotulo(im, q, x, 300, 50 * e + 1, MORADO, t, seed=15211 + k * 7, tinta=False)
        if t > tt - 0.25:
            et = entra(t, tt - 0.25)
            linea(im, [(x, 350), (x, 420 * 1 + 0 * et)], 5, GRIS, seed=15212 + k * 7, t=t)
            rotulo(im, "DE", x, 470, 36 * et + 1, TINTA, t, seed=15213 + k * 7, tinta=False)
            rotulo(im, tipo, x, 540, (48 if k < 3 else 40) * et + 1, ROJO, t, seed=15214 + k * 7)
            rotulo(im, ej, x, 650, 30 * et + 1, TINTA, t, seed=15215 + k * 7, tinta=False, fuente="segoeprb.ttf")
            chispas(im, x, 540, 120, t, tt, seed=15216 + k * 7, col=AMARILLO)
    return im


def opinan(t):
    im = cache("e_op", lambda: papel("frio")).copy()
    letrero(im, "TRES QUE OPINAN", 760, 120, 62, t, col=AMARILLO, seed=15300, esc=entra(t, tOpinan - 0.3), rot=-0.02)
    for k, (pal, tipo, tp, tt, ic) in enumerate(OPI):
        x = 330 + 430 * k
        e = entra(t, tp - 0.25)
        if e <= 0.01:
            continue
        tarjeta(im, x, 520, 390 * e, 560 * e, t, CREMA, 15310 + k * 7, rot=(k - 1) * 0.02)
        if ic == "ok":
            palomita(im, x, 380, 1.5 * e, t, seed=15311 + k * 7, col=VERDE)
        elif ic == "x":
            marca_x(im, x, 380, 1.3 * e, t, seed=15311 + k * 7)
        else:
            pregunta(im, x, 380, 2.0 * e + 0.01, t, seed=15311 + k * 7)
        rotulo(im, pal, x, 540, (40 if k < 2 else 28) * e + 1, TINTA, t, seed=15312 + k * 7, tinta=False)
        if t > tt - 0.25:
            rotulo(im, tipo, x, 660, (46 if k < 2 else 56) * entra(t, tt - 0.25) + 1, ROJO, t, seed=15313 + k * 7)
    return im


def cerebro(im, x, y, s, t, seed):
    forma(im, elipse(x, y, 170 * s, 125 * s), rgb("f3a7b8"), t, seed, tinta=5 * s)
    for k in range(6):
        a = np.linspace(0, math.pi * 2, 14)
        cx, cy = x + (-110 + 44 * k) * s, y + (-30 + 40 * (k % 2)) * s
        linea(im, np.stack([cx + 26 * s * np.cos(a) * (0.5 + a / 12), cy + 22 * s * np.sin(a) * (0.5 + a / 12)], 1), 4 * s,
              rgb("c86a84"), seed=seed + 1 + k, t=t, punta=False)


def mente(t):
    im = cache("e_me", lambda: papel("calido")).copy()
    letrero(im, "DATO CHIDO", 300, 110, 54, t, col=AMARILLO, seed=15400, esc=entra(t, T_MEN + 0.3), rot=-0.04)
    if t > tMente - 0.3:
        rotulo(im, "...MENTE = MODO", 760, 240, 90 * entra(t, tMente - 0.3) + 1, MORADO, t, seed=15405)
    for k, (base_, tk) in enumerate((("RÁPIDA", tRap), ("CUIDADOSA", tCuid))):
        e = entra(t, tk - 0.3)
        if e <= 0.01:
            continue
        y = 430 + 150 * k
        w = len(base_) * 70 * 0.58
        rotulo(im, base_, 700 - w / 2, y, 70 * e + 1, TINTA, t, seed=15410 + k * 3, tinta=False)
        letrero(im, "MENTE", 700 + 150, y, 66, t, col=rgb("fde0dc"), txt=ROJO, seed=15412 + k * 3, esc=e, rot=0.03)
    if t > tTienen - 0.3:
        e = entra(t, tTienen - 0.3)
        cerebro(im, 1250, 470, 0.9 * e + 0.01, t, 15420)
        if t > tCerebro - 0.2:
            marca_x(im, 1250, 470, 2.0 * entra(t, tCerebro - 0.2), t, seed=15430)
            rotulo(im, "¡PERO NO CEREBRO!", 760, 860, 76, ROJO, t, seed=15431, esc=entra(t, tCerebro - 0.2), rot=0.02)
    return im


def ronca(t):
    im = cache("e_ro", lambda: papel("frio")).copy()
    letrero(im, "OTRO EJEMPLO", 330, 110, 54, t, col=AMARILLO, seed=15500, esc=entra(t, T_RON + 0.3), rot=-0.04)
    from iconos_ia import perro
    late = math.exp(-((t - tRonca - 0.1) % 0.9 / 0.15) ** 2) if t > tRonca - 0.2 else 0.0
    perro(im, 470, 640 - 20 * late, 2.2, t, seed=15505)
    if late > 0.3:
        rotulo(im, "¡GUAU!", 760, 330, 90 * late + 1, ROJO, t, seed=15506, rot=-0.1)
    for k, (fr, adv, tipo, ta, tt) in enumerate((("EL PERRO LADRA", "MUCHO", "CANTIDAD", tMucho, tCant),
                                                 ("EL PERRO LADRA", "SIEMPRE", "TIEMPO", tSiempre, tTiempo))):
        e = entra(t, ta - 0.4)
        if e <= 0.01:
            continue
        y = 300 + 220 * k
        rotulo(im, fr, 1080, y, 48 * e + 1, TINTA, t, seed=15520 + k * 5, tinta=False)
        letrero(im, adv, 1080, y + 75, 52, t, col=rgb("fff2c0"), txt=rgb("e08a1e"), seed=15521 + k * 5, esc=e, rot=0.03)
        if t > tt - 0.25:
            rotulo(im, "= " + tipo, 1080, y + 150, 44 * entra(t, tt - 0.25) + 1, ROJO, t, seed=15523 + k * 5)
    return im


def preg3(t):
    im = cache("e_p3", lambda: papel("rosa")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP3 - 0.3), t, seed=15600, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=15605, esc=entra(t, tP3 - 0.1))
    if t > tJuan - 0.3:
        e = entra(t, tJuan - 0.3)
        tarjeta(im, 700, 470, 860 * e, 200 * e, t, CREMA, 15610, rot=-0.02)
        rotulo(im, "JUAN LLEGÓ AYER", 700, 478, 90 * e + 1, TINTA, t, seed=15611, rot=-0.02, tinta=False)
    if t > tCual - 0.3:
        letrero(im, "¿CUÁL ES EL ADVERBIO?", 560, 720, 52, t, col=AMARILLO, seed=15620, esc=entra(t, tCual - 0.3), rot=-0.03)
    if t > tTipo - 0.3:
        letrero(im, "¿DE QUÉ TIPO?", 1060, 840, 52, t, col=CREMA, txt=MORADO, seed=15625, esc=entra(t, tTipo - 0.3), rot=0.03)
    cuenta(im, 1640, 250, t, tFinP3 + 0.15, T_R3 + 0.1, s=0.75, seed=15630)
    return im


def resp3(t):
    im = cache("e_r3", lambda: papel("rosa")).copy()
    letrero(im, "RESPUESTA", 300, 140, 56, t, col=VERDE, txt=CREMA, seed=15700, esc=entra(t, T_R3), rot=-0.04)
    tarjeta(im, 700, 400, 860, 200, t, CREMA, 15610, rot=-0.02)
    rotulo(im, "JUAN LLEGÓ", 560, 408, 90, TINTA, t, seed=15611, rot=-0.02, tinta=False)
    f = suave(pr(t, tAyer - 0.2, tAyer + 0.3))
    ficha(im, "AYER", 990, 390, 80, t, rgb("fff2c0"), 15710, fuerte=f)
    if t > tCuando - 0.3:
        e = entra(t, tCuando - 0.3)
        letrero(im, "¿CUÁNDO?", 560, 700, 64, t, col=rgb("b8c7e8"), txt=MORADO, seed=15720, esc=e, rot=-0.03)
        linea(im, [(760, 700), (760 + 150 * suave(pr(t, tCuando, tCuando + 0.5)), 700)], 8, GRIS, seed=15721, t=t)
    if t > tTiem - 0.3:
        letrero(im, "DE TIEMPO", 1120, 700, 70, t, col=VERDE, txt=CREMA, seed=15725, esc=entra(t, tTiem - 0.3), rot=0.03)
        chispas(im, 1120, 700, 220, t, tTiem, seed=15726, col=AMARILLO)
    if t > tEso - 0.3:
        palomita(im, 1420, 420, 1.5 * entra(t, tEso - 0.3), t, seed=15730, col=VERDE)
    return im


TRAMOS = [(T_INI, defin), (T_EJ, ejemplos), (T_VB, verbo), (T_OP, opinan), (T_MEN, mente), (T_RON, ronca), (T_P3, preg3),
          (T_R3, resp3)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
