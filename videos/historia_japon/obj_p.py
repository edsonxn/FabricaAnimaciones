# -*- coding: utf-8 -*-
"""Objetos propios de «La historia de Irán» (boceto). Todos son `Dib`; el origen está en la base del objeto."""
import math
from functools import lru_cache

import numpy as np

from obj_base import *  # noqa: F401,F403
from obj_a import colocar

PURPURA = (140, 84, 140)
AZUL_TILE = (54, 120, 184)
TURQUESA = (64, 176, 172)
ARENA = (226, 196, 140)
NIEVE = (250, 250, 252)
PETROLEO = (44, 40, 46)


# ------------------------------------------------------------------ orígenes
@lru_cache(maxsize=None)
def montanas():
    """Tres picos nevados (la meseta rodeada de montañas)."""
    ops = []
    for x0, h, w, c in ((-150, 210, 170, (150, 130, 112)), (150, 240, 190, (140, 120, 104)), (0, 290, 210, (166, 142, 120))):
        ops += forma(pol((x0 - w, 0), (x0 - w * 0.12, -h), (x0 + w * 0.06, -h + 18), (x0 + w, 0)), c, 5.4, peso=0.7, sp=9)
        ops += forma(pol((x0 - w * 0.26, -h * 0.72), (x0 - w * 0.12, -h), (x0 + w * 0.06, -h + 18), (x0 + w * 0.22, -h * 0.74), (x0 + w * 0.02, -h * 0.66),
                         (x0 - w * 0.1, -h * 0.74)), NIEVE, 4.2, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def tablilla():
    """Tablilla de arcilla con signos en forma de cuña."""
    ops = forma(rect(-90, -130, 90, 0, 14), (206, 160, 112), 5.6, peso=0.7, sp=9)
    rng = np.random.default_rng(11)
    for fila in range(5):
        y = -108 + 22 * fila
        x = -66
        while x < 62:
            ops += [rayita(x, y, x + 12, y - 4, 3.4), rayita(x + 6, y - 8, x + 6, y + 6, 3.0)]
            x += 15 + 6 * rng.random()
    return Dib(ops)


@lru_cache(maxsize=None)
def qanat(f=0):
    """Corte de una ladera: pozos verticales y un túnel subterráneo por donde corre el agua hasta la aldea."""
    f = f % 4
    ops = forma(pol((-260, 0), (-260, -150), (-140, -230), (0, -140), (130, -90), (240, -80), (260, 0)), (192, 152, 104), 5.6, peso=0.8, sp=10)
    ops += forma(pol((-260, -150), (-140, -230), (-96, -200), (-180, -130)), NIEVE, 4.0, sp=6)
    # túnel
    ops += forma(pol((-150, -70), (250, -24), (250, -6), (-150, -50)), (92, 70, 54), 4.4, sp=6)
    for k in range(6):
        x = -110 + 62 * k + 28 * ((f + k) % 2) * 0
        y0 = -56 + 7.5 * k * 0.8
        ytop = -158 + 18 * k * 0.55 - 8 * max(0, k - 3)
        ops += [T(linea((x - 9, ytop), (x - 9, y0 - 14)), 4.2, peso=0.04), T(linea((x + 9, ytop), (x + 9, y0 - 14)), 4.2, peso=0.04)]
        ops += forma(elip(x, ytop, 12, 4, 0, 1.0, 10), (92, 70, 54), 3.6, sp=4)
    # gotas de agua que avanzan por el túnel
    for k in range(6):
        xx = -130 + ((k * 62 + f * 26) % 380)
        yy = -60 + (xx + 150) * 0.1
        ops += [R(elip(xx, yy, 7, 4, 0, 1.0, 10), (110, 184, 226), peso=0.02, sp=3)]
    # aldea y verde al final
    ops += [R(elip(214, -8, 46, 12, 0, 1.0, 16), VERDE_CL, peso=0.05, sp=5)]
    return Dib(ops)


@lru_cache(maxsize=None)
def cilindro():
    """Cilindro de arcilla de Ciro con la escritura en filas."""
    P = elip(0, -70, 130, 66, 0, 1.0, 36)
    ops = forma(P, (200, 152, 104), 5.8, peso=0.8, sp=9)
    ops += forma(elip(-120, -70, 20, 64, 0, 1.0, 20), (178, 130, 88), 4.6, sp=6)
    rng = np.random.default_rng(5)
    for fila in range(6):
        y = -106 + 14 * fila
        x = -96
        while x < 92:
            ops += [rayita(x, y, x + 8, y - 3, 3.0), rayita(x + 4, y - 6, x + 4, y + 4, 2.6)]
            x += 10 + 4 * rng.random()
    return Dib(ops)


@lru_cache(maxsize=None)
def columna(alto=1.0):
    """Columna de Persépolis: fuste estriado y capitel con volutas."""
    h = 300 * alto
    ops = forma(rect(-44, -22, 44, 0, 4), PIEDRA, 5, peso=0.5, sp=8)
    ops += forma(pol((-30, -22), (-26, -h + 70), (26, -h + 70), (30, -22)), (214, 204, 184), 5.4, peso=0.6, sp=9)
    ops += [T(linea((x, -28), (x * 0.86, -h + 76)), 3.0, peso=0.03) for x in (-15, 0, 15)]
    ops += forma(rect(-40, -h + 70, 40, -h + 50, 4), PIEDRA, 5, sp=7)
    ops += forma(pol((-62, -h + 50), (-66, -h + 10), (-32, -h + 4), (-8, -h + 44)), (204, 192, 170), 4.8, sp=7)
    ops += forma(pol((62, -h + 50), (66, -h + 10), (32, -h + 4), (8, -h + 44)), (204, 192, 170), 4.8, sp=7)
    ops += [T(circ(-46, -h + 28, 14, n=16), 3.6, peso=0.05), T(circ(46, -h + 28, 14, n=16), 3.6, peso=0.05)]
    ops += forma(rect(-56, -h + 4, 56, -h - 16, 4), PIEDRA, 5, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def carta():
    ops = forma(rect(-46, -62, 46, 0, 4), CREMA, 4.6, peso=0.5, sp=7)
    ops += [T(linea((-46, -62), (0, -24), (46, -62)), 3.6, peso=0.04)] + [R(circ(0, -30, 9, n=10), ROJO_CH, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def gota_oro(r=40):
    """Gran moneda (dárico) con un arquero."""
    ops = forma(circ(0, 0, r, n=36), ORO, 5.4, peso=0.6, sp=8)
    ops += [T(circ(0, 0, r * 0.8, n=30), 3.2, peso=0.25)]
    ops += [T(linea((-r * 0.3, r * 0.3), (r * 0.3, -r * 0.3)), 3.6, peso=0.04), T(arco_(r * 0.08, -r * 0.06, r * 0.36, -70, 70, 10), 3.4, peso=0.04)]
    return Dib(ops)


# ------------------------------------------------------------------ partos, sasánidas
@lru_cache(maxsize=None)
def altar_fuego(f=0):
    """Altar del fuego sagrado (zoroastrismo)."""
    f = f % 3
    ops = forma(pol((-50, 0), (-40, -60), (40, -60), (50, 0)), PIEDRA, 5.2, peso=0.6, sp=8)
    ops += forma(rect(-62, -82, 62, -60, 4), (214, 204, 184), 5, sp=7)
    ops += forma(pol((-56, -82), (-40, -94), (40, -94), (56, -82)), PIEDRA, 4.6, sp=6)
    a, b = (0, 10, -8)[f], (0, -12, 8)[f]
    P = curva([(-34, -92), (-42 + a, -150), (-16, -206 + b), (-10, -176), (6, -270 + a * 2), (20, -190), (38, -228 + b), (46, -150), (38, -92)], 6)
    Q = curva([(-16, -92), (-18, -130), (-2, -170 + b), (6, -210 + a), (18, -150), (22, -92)], 6)
    ops += forma(np.vstack([P, P[:1]]), NARANJA, 5, peso=0.6, sp=8) + forma(np.vstack([Q, Q[:1]]), AMARILLO, 4, peso=0.4, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def tablero_ajedrez():
    ops = []
    c0, c1 = (236, 216, 176), (150, 104, 76)
    for i in range(4):
        for j in range(4):
            x, y = -100 + 50 * i, -100 + 50 * j
            ops += forma(rect(x, y, x + 50, y + 50, 1), c0 if (i + j) % 2 == 0 else c1, 3.6, sp=6)
    # rey y torre
    ops += forma(pol((-58, -2), (-52, -56), (-44, -82), (-44, -112), (-26, -112), (-26, -82), (-18, -56), (-12, -2)), (250, 240, 214), 4.6, sp=7)
    ops += [T(linea((-35, -140), (-35, -112)), 4, peso=0.03), T(linea((-46, -128), (-24, -128)), 4, peso=0.03)]
    ops += forma(pol((30, -2), (34, -56), (30, -86), (28, -116), (40, -116), (50, -104), (60, -116), (72, -116), (70, -86), (66, -56), (70, -2)), (62, 50, 56), 4.6, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def arco_ctesifonte():
    """El gran arco de ladrillo de Ctesifonte."""
    ops = forma(rect(-180, -40, 180, 0, 4), (196, 150, 112), 5.4, peso=0.5, sp=9)
    ops += forma(pol((-150, -40), (-150, -190), (-90, -250), (0, -290), (90, -250), (150, -190), (150, -40), (96, -40), (96, -180), (0, -232), (-96, -180), (-96, -40)),
                 (204, 158, 118), 5.6, peso=0.7, sp=9)
    ops += [T(linea((-96, -40), (-96, -180), (0, -232), (96, -180), (96, -40)), 4.2, peso=0.08)]
    return Dib(ops)


# ------------------------------------------------------------------ edad de oro y safávidas
@lru_cache(maxsize=None)
def libro(abierto=True):
    ops = forma(pol((-110, -20), (-110, -110), (0, -96), (0, 0)), CREMA, 5.2, peso=0.5, sp=8)
    ops += forma(pol((110, -20), (110, -110), (0, -96), (0, 0)), (250, 244, 224), 5.2, peso=0.5, sp=8)
    for k in range(4):
        ops += [T(linea((-96, -86 + 16 * k - 3 * k * 0), (-14, -76 + 16 * k)), 2.8, peso=0.03), T(linea((14, -76 + 16 * k), (96, -86 + 16 * k)), 2.8, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mezquita():
    """Cúpula de azulejos azules con dos minaretes y puerta en arco."""
    ops = forma(rect(-170, -150, 170, 0, 4), (232, 214, 172), 5.6, peso=0.6, sp=9)
    ops += forma(pol((-90, -150), (-96, -230), (-50, -300), (0, -330), (50, -300), (96, -230), (90, -150)), AZUL_TILE, 5.6, peso=0.8, sp=8)
    ops += [T(linea((0, -150), (0, -330)), 2.8, peso=0.05)] + [T(arco_(0, -150, r, 180, 360, 14), 2.8, peso=0.05) for r in (34, 62)]
    ops += forma(rect(-7, -362, 7, -330, 2), ORO, 3.6, sp=4)
    for lado in (-1, 1):
        x = lado * 140
        ops += forma(rect(x - 14, -290, x + 14, -150, 3), (232, 214, 172), 5, peso=0.4, sp=8)
        ops += forma(pol((x - 18, -290), (x, -330), (x + 18, -290)), TURQUESA, 4.6, sp=6)
        ops += [rayita(x - 14, -240, x + 14, -240, 3.2), rayita(x - 14, -200, x + 14, -200, 3.2)]
    ops += forma(pol((-30, 0), (-30, -74), (0, -104), (30, -74), (30, 0)), (92, 70, 54), 4.6, sp=7)
    for k in range(5):
        ops += [R(circ(-120 + 60 * k, -120, 9, n=10), TURQUESA if k % 2 == 0 else AZUL_TILE, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def alfombra():
    ops = forma(rect(-130, -150, 130, 0, 6), ROJO_CH, 5.4, peso=0.5, sp=9)
    ops += forma(rect(-108, -128, 108, -22, 3), (230, 196, 120), 4.2, sp=7)
    ops += forma(pol((0, -116), (72, -75), (0, -34), (-72, -75)), AZUL_IMP, 4.4, sp=7)
    ops += forma(pol((0, -96), (40, -75), (0, -54), (-40, -75)), CREMA, 3.6, sp=6)
    ops += [R(circ(-90, -110, 7, n=8), AZUL_IMP, peso=0.02, sp=3), R(circ(90, -110, 7, n=8), AZUL_IMP, peso=0.02, sp=3),
            R(circ(-90, -40, 7, n=8), AZUL_IMP, peso=0.02, sp=3), R(circ(90, -40, 7, n=8), AZUL_IMP, peso=0.02, sp=3)]
    ops += [rayita(-130 + 13 * k, 0, -130 + 13 * k, 14, 3) for k in range(21)] + [rayita(-130 + 13 * k, -150, -130 + 13 * k, -164, 3) for k in range(21)]
    return Dib(ops)


@lru_cache(maxsize=None)
def trono_pavo():
    """Trono del Pavo Real: asiento dorado y abanico de cola de colores."""
    ops = []
    cols = [(64, 140, 190), (64, 176, 172), (110, 170, 100), (64, 140, 190), (64, 176, 172), (110, 170, 100), (64, 140, 190)]
    for k in range(7):
        a = math.radians(-150 + 20 * k)
        ops += forma(pol((0, -120), (150 * math.cos(a) - 24 * math.sin(a), -120 + 150 * math.sin(a) + 24 * math.cos(a)),
                         (150 * math.cos(a) + 24 * math.sin(a), -120 + 150 * math.sin(a) - 24 * math.cos(a))), cols[k], 4.2, sp=6)
        ops += [R(circ(150 * math.cos(a) * 0.86, -120 + 150 * math.sin(a) * 0.86, 10, n=10), ORO, peso=0.02, sp=3)]
    ops += forma(rect(-74, -150, 74, -96, 10), ORO, 5.4, peso=0.6, sp=9)
    ops += forma(rect(-92, -102, 92, -58, 6), ORO_OSC, 5.2, peso=0.5, sp=9)
    ops += forma(rect(-84, -58, 84, 0, 4), (176, 120, 40), 5, peso=0.5, sp=9)
    ops += [R(circ(-40 + 40 * k, -30, 9, n=10), ROJO_CH if k != 1 else JADE, peso=0.02, sp=3) for k in range(3)]
    return Dib(ops)


# ------------------------------------------------------------------ petróleo y siglo XX
@lru_cache(maxsize=None)
def torre_petroleo(f=0):
    """Torre de perforación con un chorro negro que brota."""
    ops = [T(linea((-60, 0), (-14, -240)), 5.6, peso=0.1), T(linea((60, 0), (14, -240)), 5.6, peso=0.1), T(linea((-14, -240), (14, -240)), 5.0, peso=0.05)]
    for k in range(1, 5):
        y = -48 * k
        w = 60 - 11 * k
        ops += [T(linea((-w, y), (w, y)), 4.0, peso=0.04), T(linea((-w, y), (w - 10, y - 48)), 3.2, peso=0.03)]
    ops += forma(rect(-56, -12, 56, 0, 3), GRIS_OSC, 4.4, sp=6)
    f = f % 3
    h = (150, 190, 170)[f]
    P = curva([(-14, 0), (-18, -h * 0.5), (-28 + 6 * f, -h - 10), (-4, -h - 40), (18, -h - 12), (22 - 6 * f, -h * 0.5), (14, 0)], 6)
    ops += forma(np.vstack([P, P[:1]]), PETROLEO, 5, peso=0.6, sp=8)
    for k in range(5):
        ops += [R(elip(-56 + 28 * k + 10 * f, -h - 20 - 18 * (k % 3), 7, 10, 0, 1.0, 10), PETROLEO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def barril():
    ops = forma(rect(-44, -96, 44, 0, 10), PETROLEO, 5.4, peso=0.6, sp=9)
    ops += [T(linea((-44, -64), (44, -64)), 3.6, peso=0.04), T(linea((-44, -30), (44, -30)), 3.6, peso=0.04)]
    ops += [R(elip(0, -48, 16, 10, 0, 1.0, 12), ORO, peso=0.04, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def parlamento():
    ops = forma(rect(-150, -60, 150, 0, 4), (226, 208, 172), 5.4, peso=0.6, sp=9)
    ops += forma(pol((-170, -150), (0, -236), (170, -150)), (240, 226, 190), 5.4, peso=0.7, sp=8)
    ops += forma(rect(-150, -160, 150, -132, 3), (226, 208, 172), 4.6, sp=7)
    for k in range(6):
        x = -120 + 48 * k
        ops += forma(rect(x - 11, -140, x + 11, -60, 2), (244, 236, 214), 4.2, sp=7)
    ops += [R(circ(0, -176, 14, n=14), ORO, peso=0.04, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def haft_sin():
    """Mesa de Nowruz: hierba germinada, pecera con pez, huevos pintados y vela."""
    ops = forma(rect(-210, -70, 210, -46, 4), (214, 204, 184), 5.2, peso=0.5, sp=8)
    ops += forma(rect(-194, -46, 194, 0, 3), (172, 92, 70), 5, peso=0.4, sp=8)
    # hierba
    ops += forma(rect(-150, -110, -90, -70, 6), ARCILLA, 4.4, sp=6)
    for k in range(9):
        x = -144 + 7 * k
        ops += [T(linea((x, -110), (x + 3 * ((k % 3) - 1), -156 - 6 * (k % 3))), 3.6, peso=0.03)]
    # pecera
    ops += forma(circ(-20, -114, 44, n=26), (190, 226, 240), 4.6, sp=8)
    ops += forma(elip(-26, -114, 18, 10, 0, 1.0, 14), NARANJA, 3.8, sp=5) + forma(pol((-8, -114), (4, -124), (4, -104)), NARANJA, 3.4, sp=4)
    # huevos
    for k, c in enumerate((ROJO_CH, AZUL_IMP, ORO)):
        ops += forma(elip(50 + 30 * k, -92, 13, 20, 0, 1.0, 14), c, 4.0, sp=5)
    # vela
    ops += forma(rect(142, -132, 160, -70, 3), CREMA, 4.4, sp=6)
    ops += forma(pol((150, -134), (142, -150), (151, -176), (160, -150)), NARANJA, 3.6, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def pancarta(txt_color=(200, 66, 60)):
    ops = [T(linea((0, 0), (0, -250)), 5.6, peso=0.06)]
    ops += forma(rect(-110, -250, 110, -170, 4), CREMA, 5, peso=0.4, sp=8)
    ops += [T(linea((-84 + 14 * k, -222), (-74 + 14 * k, -196)), 4.2, peso=0.03) for k in range(12)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tablilla_mapa():
    """Mapa pequeño con una flecha (de 'ruta')."""
    ops = forma(rect(-100, -80, 100, 0, 6), CREMA, 5, peso=0.5, sp=8)
    ops += [T(curva([(-70, -20), (-20, -60), (40, -30), (76, -62)], 8), 4.2, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def estandarte_persa():
    """Estandarte dorado con un sol (emblema simplificado)."""
    ops = [T(linea((0, 0), (0, -270)), 5.6, peso=0.06)]
    ops += forma(rect(2, -270, 130, -170, 4), PURPURA, 5, peso=0.4, sp=8)
    ops += forma(circ(66, -220, 24, n=20), ORO, 4.2, sp=6)
    ops += [rayita(66 + 30 * math.cos(a), -220 + 30 * math.sin(a), 66 + 40 * math.cos(a), -220 + 40 * math.sin(a), 3.2) for a in np.linspace(0, 6.28, 9)[:-1]]
    return Dib(ops)
