# -*- coding: utf-8 -*-
"""Dibujos de boceto para la historia de España (3/4): conquista de América, Imperio y Siglo de Oro.
Conquistador (morrión), guerrero águila mexica, aliado tlaxcalteca, inca (mascaipacha), Templo Mayor, Cerro Rico de Potosí,
real de a ocho, galeón, galeras de Lepanto, Felipe II, el sol que nunca se pone, Cervantes, don Quijote y los molinos,
Velázquez y Las Meninas, bancarrota, Carlos II y la cuna vacía, Felipe V de Borbón, el Peñón de Gibraltar."""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
import obj_es1  # noqa: F401
import obj_es2  # noqa: F401
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_es1 import BLANCO_R, HIERRO, NEGRO_R, OCRE, PIEL_BRONCE, ROCA, ROCA_OSC
from obj_es2 import _montado, caballo2

PLATA = (210, 214, 222)
PLATA_OSC = (160, 166, 178)
ROJO_POTOSI = (178, 90, 70)
TURQUESA = (64, 170, 160)
PLUMA_V = (60, 150, 90)
AZUL_BORBON = (60, 90, 170)
NEGRO_TERC = (50, 46, 56)

_orig = OB.sombrero


def _sombrero(nombre, cy=-215.0):
    if nombre == "morrion":           # morrión de conquistador: cresta y ala curvada en punta
        ops = forma(curva([(-70, cy - 20), (-50, cy - 30), (-36, cy - 66), (0, cy - 78), (36, cy - 66), (50, cy - 30), (70, cy - 20), (40, cy - 36), (-40, cy - 36)], 6),
                    HIERRO, 4.8, sp=8)
        ops += forma(curva([(-30, cy - 70), (-10, cy - 102), (16, cy - 104), (32, cy - 70)], 5).tolist() + [(0, cy - 76)], HIERRO, 4.2, sp=5)
        return ops + forma(pol((-4, cy - 104), (2, cy - 130), (12, cy - 104)), ROJO_CH, 3, sp=3)
    if nombre == "aguila":            # yelmo de guerrero águila (cabeza de águila con pico)
        ops = forma(curva([(-48, cy + 6), (-52, cy - 40), (-30, cy - 74), (14, cy - 80), (44, cy - 60), (56, cy - 30), (54, cy + 6)], 6), (150, 110, 70), 4.8, sp=7)
        ops += forma(pol((44, cy - 50), (88, cy - 44), (74, cy - 26), (52, cy - 24)), (240, 190, 70), 4, sp=4)
        ops += [punto(30, cy - 52, 9)]
        for k in range(4):
            ops += forma(elip(-40 + 8 * k, cy - 92 - 6 * k, 8, 24, -0.5 + 0.2 * k, 1.0, 12), PLUMA_V if k % 2 else (230, 80, 70), 3, sp=3)
        return ops
    if nombre == "tlaxcala":          # cinta roja y blanca con plumas
        ops = forma(rect(-44, cy - 40, 44, cy - 26, 4), (220, 60, 60), 3.8, sp=4) + forma(elip(0, cy - 20, 43, 30, math.pi, 0.5, 20), NEGRO_R, 4, cerrada=False, sp=6)[1:]
        return ops + forma(elip(30, cy - 70, 8, 26, 0.3, 1.0, 12), BLANCO_R, 3, sp=3)
    if nombre == "mascaipacha":       # borla roja del Inca con plumas
        ops = forma(elip(0, cy - 14, 43, 34, math.pi, 0.5, 26), NEGRO_R, 4.4, cerrada=False, sp=7)[1:]
        ops += forma(rect(-44, cy - 40, 44, cy - 28, 3), (230, 190, 70), 3.6, sp=4)
        ops += forma(rect(-20, cy - 28, 20, cy - 4, 2), (210, 40, 50), 3.4, sp=3)
        for k in range(3):
            ops += forma(elip(-14 + 14 * k, cy - 66, 6, 22, 0.25 * (k - 1), 1.0, 12), BLANCO_R if k != 1 else (40, 40, 40), 3, sp=3)
        return ops
    if nombre == "gorra_negra":       # gorra de terciopelo negro (Felipe II)
        return forma(pol((-46, cy - 26), (-52, cy - 48), (-30, cy - 64), (30, cy - 64), (52, cy - 48), (46, cy - 26)), NEGRO_TERC, 4.6, sp=7) + \
            [R(circ(30, cy - 52, 6, n=10), (220, 220, 230), peso=0.01, sp=3)]
    if nombre == "bacia":             # bacía de barbero (el «yelmo de Mambrino» de don Quijote)
        return forma(curva([(-50, cy - 30), (-40, cy - 58), (0, cy - 70), (40, cy - 58), (50, cy - 30)], 5).tolist() + [(64, cy - 26), (-64, cy - 26)], (220, 180, 90), 4.4, sp=6)
    if nombre == "peluca":            # peluca empolvada borbónica: copete y rizos a los lados, coleta atrás
        ops = forma(curva([(-46, cy - 6), (-50, cy - 34), (-30, cy - 58), (0, cy - 64), (30, cy - 58), (50, cy - 34), (46, cy - 6), (34, cy - 26), (0, cy - 36),
                           (-34, cy - 26)], 6), (236, 232, 222), 4.4, sp=7)
        for lado in (-1, 1):
            for k in range(2):
                ops += forma(elip(lado * 50, cy - 6 + 22 * k, 13, 11, 0, 1.0, 14), (236, 232, 222), 3.6, sp=4)
        return ops + forma(pol((-8, cy + 40), (8, cy + 40), (6, cy + 80), (-6, cy + 80)), (60, 50, 50), 3, sp=3)
    if nombre == "melena_carlos":     # melena larga y lacia (Carlos II)
        return forma(curva([(-50, cy + 70), (-54, cy - 10), (-40, cy - 52), (0, cy - 60), (40, cy - 52), (54, cy - 10), (50, cy + 70), (38, cy + 60), (36, cy - 24),
                            (0, cy - 34), (-36, cy - 24), (-38, cy + 60)], 6), (190, 160, 110), 4.4, sp=7)
    if nombre == "pelo_rizo":
        return forma(curva([(-46, cy + 6), (-50, cy - 30), (-30, cy - 54), (0, cy - 58), (30, cy - 54), (50, cy - 30), (46, cy + 6), (36, cy - 18), (0, cy - 28),
                            (-36, cy - 18)], 6), (70, 56, 50), 4.4, sp=7)
    return _orig(nombre, cy)


OB.sombrero = _sombrero


def _acc_macuahuitl(m, d):
    x, y = m
    ops = forma(pol((x - 8, y + 20), (x + 8, y + 20), (x + 12, y - 120), (x - 4, y - 120)), (160, 110, 70), 4.2, sp=4)
    for k in range(6):
        yy = y - 10 - 20 * k
        ops += forma(pol((x - 6, yy), (x - 18, yy - 6), (x - 6, yy - 12)), (40, 40, 50), 2.6, sp=2) + forma(pol((x + 10, yy), (x + 22, yy - 6), (x + 10, yy - 12)), (40, 40, 50), 2.6, sp=2)
    return ops


def _acc_chimalli(m, d):
    x, y = m
    ops = forma(elip(x, y, 38, 38, 0, 1.0, 26), (240, 220, 160), 4.6, sp=7) + forma(elip(x, y, 18, 18, 0, 1.0, 16), TURQUESA, 3.4, sp=4)
    for k in range(5):
        ops += forma(elip(x - 24 + 12 * k, y + 46, 5, 14, 0, 1.0, 10), PLUMA_V if k % 2 else (230, 80, 70), 2.6, sp=2)
    return ops


def _acc_pluma(m, d):
    x, y = m
    return forma(curva([(x, y + 6), (x + 16, y - 40), (x + 40, y - 90), (x + 30, y - 40), (x + 6, y + 4)], 5), BLANCO_R, 3.4, sp=3)


def _acc_paleta(m, d):
    x, y = m
    ops = forma(curva([(x - 40, y - 10), (x - 30, y - 50), (x + 20, y - 54), (x + 46, y - 20), (x + 30, y + 16), (x - 20, y + 20)], 6), (210, 170, 120), 4, sp=5)
    for k, c in enumerate(((220, 60, 50), (240, 200, 70), (60, 100, 170), BLANCO_R)):
        ops += [R(circ(x - 20 + 16 * k, y - 30 + 6 * (k % 2), 7, n=10), c, peso=0.01, sp=3)]
    return ops


def _acc_lanza_q(m, d):          # lanza larga, inclinada hacia delante
    x, y = m
    return [T(linea((x - 40, y + 30), (x + 200, y - 60)), 5, peso=0.1), R(pol((x + 196, y - 66), (x + 236, y - 76), (x + 204, y - 52)), GRIS_CL, peso=0.02, sp=3)]


def _acc_libro_q(m, d):
    x, y = m
    return forma(rect(x - 28, y - 46, x + 28, y + 20, 4), (180, 60, 50), 4.2, sp=5) + [rayita(x - 16, y - 30, x + 16, y - 30, 3)]


OB.ACC.update({"macuahuitl": _acc_macuahuitl, "chimalli": _acc_chimalli, "pluma": _acc_pluma, "paleta": _acc_paleta, "lanza_q": _acc_lanza_q, "libro_q": _acc_libro_q})


def gorguera(ops, cy=-215.0):
    """Gorguera blanca plisada bajo la cabeza."""
    out = list(ops)
    out += forma(elip(0, cy + 46, 52, 14, 0, 1.0, 26), BLANCO_R, 3.6, sp=4)
    out += [T(linea((-40 + 10 * k, cy + 38), (-40 + 10 * k, cy + 54)), 2, peso=0.01) for k in range(9)]
    return out


# ------------------------------------------------------------------ conquista
@lru_cache(maxsize=None)
def conquistador(pose=0, cara="serio", color=(160, 60, 50), barba=(120, 86, 60)):
    return persona(color, PIEL_ROSA, "morrion", cara, (16, 60), pose, traje="armadura", faja=ORO, barba=barba, acc_d="espada")


@lru_cache(maxsize=None)
def conquistador_caballo(pose=0, color=(160, 60, 50)):
    r = persona(color, PIEL_ROSA, "morrion", "serio", (40, 80), pose, traje="armadura", faja=ORO, barba=(120, 86, 60), acc_d="espada")
    return Dib(_montado(caballo2(pose, (110, 74, 52)), r, color=color))


@lru_cache(maxsize=None)
def guerrero_aguila(pose=0, cara="enojo"):
    d = persona((200, 170, 110), (196, 130, 90), "aguila", cara, (16, 60), pose, traje="armadura", faja=(220, 70, 60), acc_d="macuahuitl", acc_i="chimalli")
    return d


@lru_cache(maxsize=None)
def tlaxcalteca(pose=0, cara="serio"):
    return persona((240, 236, 222), (196, 130, 90), "tlaxcala", cara, (16, 40), pose, traje="armadura", faja=(220, 60, 60), acc_d="lanza", acc_i="chimalli")


@lru_cache(maxsize=None)
def inca(pose=0, cara="serio"):
    d = persona((200, 60, 60), (190, 128, 90), "mascaipacha", cara, (16, 50), pose, traje="tunica", faja=(230, 190, 70), cuello=(230, 190, 70), acc_d="cetro")
    ops = list(d.ops)
    for k in range(3):                                                   # tocapus del unku
        for j in range(3):
            ops += [R(rect(-36 + 26 * j, -130 + 26 * k, -18 + 26 * j, -112 + 26 * k, 2), ((230, 190, 70), BLANCO_R, (40, 40, 40))[(j + k) % 3], peso=0.01, sp=3)]
    ops += forma(elip(-44, -205, 9, 9, 0, 1.0, 10), ORO, 3, sp=3) + forma(elip(44, -205, 9, 9, 0, 1.0, 10), ORO, 3, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def templo_mayor():
    """Templo Mayor de Tenochtitlan: pirámide escalonada con escalinata doble y los dos templos (Tláloc azul, Huitzilopochtli rojo)."""
    ops = []
    for k in range(5):
        w = 200 - 30 * k
        ops += forma(rect(-w, -50 * (k + 1), w, -50 * k, 3), (214, 196, 160) if k % 2 else (200, 182, 146), 4.8, peso=0.3, sp=9)
    ops += forma(pol((-50, 0), (-10, 0), (-6, -250), (-34, -250)), (236, 226, 200), 3.8, sp=5)
    ops += forma(pol((10, 0), (50, 0), (34, -250), (6, -250)), (236, 226, 200), 3.8, sp=5)
    ops += [T(linea((-48 + 4 * k * 0.0, -20 - 40 * k), (48, -20 - 40 * k)), 2.4, peso=0.02, v=160) for k in range(6)]
    ops += forma(rect(-90, -330, -10, -250, 3), (90, 140, 200), 4.6, sp=7) + forma(rect(10, -330, 90, -250, 3), (200, 70, 60), 4.6, sp=7)
    ops += forma(pol((-96, -330), (-50, -370), (-4, -330)), (90, 140, 200), 4, sp=5) + forma(pol((4, -330), (50, -370), (96, -330)), (200, 70, 60), 4, sp=5)
    ops += forma(rect(-64, -296, -36, -250, 2), NEGRO_R, 3, sp=3) + forma(rect(36, -296, 64, -250, 2), NEGRO_R, 3, sp=3)
    ops += forma(pol((-260, 0), (-240, 20), (240, 20), (260, 0)), (120, 180, 210), 3.6, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def epidemia(f=0):
    """Nube gris de la enfermedad, con puntos."""
    circs = [(-90, -100, 60), (-20, -140, 72), (60, -110, 62), (110, -70, 46), (-130, -60, 44), (10, -70, 60)]
    P, _ = B.union_circulos(circs, -20, centro=(0.0, -100.0))
    ops = forma(P, (150, 146, 156), 5, peso=0.4, sp=9)
    rng = np.random.default_rng(5)
    for k in range(14):
        x, y = rng.uniform(-150, 140), rng.uniform(-180, -50)
        ops += forma(elip(x + 4 * math.sin(f + k), y, 7, 7, 0, 1.0, 10), (120, 70, 90), 2.6, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def cerro_rico():
    """Cerro Rico de Potosí: montaña cónica rojiza con bocaminas y vetas de plata."""
    ops = forma(curva([(-260, 0), (-150, -120), (-60, -250), (0, -290), (60, -250), (150, -120), (260, 0)], 7), ROJO_POTOSI, 5.8, peso=0.6, sp=11)
    for x, y in ((-60, -120), (40, -170), (-10, -60), (90, -70)):
        ops += forma(curva([(x - 16, y + 10), (x - 16, y - 8), (x, y - 18), (x + 16, y - 8), (x + 16, y + 10)], 4), NEGRO_R, 3.6, sp=3)
    for k in range(5):
        ops += [T(curva([(-120 + 50 * k, -40 - 20 * k), (-90 + 50 * k, -90 - 20 * k), (-70 + 46 * k, -130 - 18 * k)], 4), 3, peso=0.03, v=150)]
        ops += [R(circ(-80 + 46 * k, -110 - 18 * k, 8, n=10), PLATA, peso=0.01, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def lingotes():
    ops = []
    for (x, y) in ((-70, 0), (0, 0), (70, 0), (-35, -36), (35, -36), (0, -72)):
        ops += forma(pol((x - 34, y), (x + 34, y), (x + 26, y - 34), (x - 26, y - 34)), PLATA, 4.4, sp=5)
        ops += [T(linea((x - 18, y - 26), (x + 4, y - 26)), 3, peso=0.01, v=160)]
    return Dib(ops)


@lru_cache(maxsize=None)
def real_de_a_ocho():
    """Real de a ocho (la primera moneda global): las dos columnas del Plus Ultra sobre las olas."""
    ops = forma(elip(0, -100, 100, 100, 0, 1.0, 40), PLATA, 5.4, peso=0.5, sp=8) + [T(elip(0, -100, 86, 86, 0, 1.0, 36), 3, peso=0.04)]
    for cx in (-36, 36):
        ops += forma(rect(cx - 9, -150, cx + 9, -60, 2), PLATA_OSC, 3.6, sp=3) + forma(rect(cx - 15, -160, cx + 15, -150, 2), PLATA_OSC, 3.2, sp=3)
        ops += forma(pol((cx - 14, -176), (cx - 10, -186), (cx, -196), (cx + 10, -186), (cx + 14, -176), (cx - 14, -176)), ORO, 3, sp=3)
    ops += [T(B.ondas(-70, 70, -48, 6, 30), 3.4, peso=0.03), T(B.ondas(-60, 60, -34, 5, 26), 3, peso=0.03)]
    ops += forma(curva([(-60, -110), (-20, -96), (20, -110), (60, -96), (60, -84), (20, -96), (-20, -84), (-60, -96)], 4), BLANCO_R, 3, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def galeon(f=0, tam=1.0, color=(150, 100, 66)):
    """Galeón español: castillo de popa alto y decorado, cuatro palos, velas con la cruz de Borgoña, bandera roja y blanca."""
    ops = forma(curva([(-210, -150), (-196, -40), (-120, 6), (110, 6), (190, -40), (236, -96), (190, -90), (130, -76), (-110, -80), (-150, -170)], 6),
                color, 5.8, peso=0.6, sp=10)
    ops += forma(rect(-214, -196, -126, -140, 4), (176, 120, 72), 4.8, sp=6) + forma(rect(-206, -188, -134, -168, 2), ORO, 3, sp=3)
    ops += forma(rect(130, -126, 196, -86, 3), (176, 120, 72), 4.6, sp=6)
    ops += [T(linea((-196, -50), (180, -50)), 3.2, peso=0.04), T(linea((-190, -84), (150, -84)), 3, peso=0.03)]
    for k in range(8):
        ops += forma(rect(-150 + 38 * k, -70, -136 + 38 * k, -58, 2), NEGRO_R, 2.4, sp=2)
    for x, h, w in ((-160, 250, 48), (-30, 330, 64), (100, 280, 56)):
        ops += [T(linea((x, -80), (x, -80 - h)), 5.4, peso=0.12)]
        sw = 7 * math.sin(f * 1.3 + x * 0.01)
        for (a, b) in ((0.92, 0.62), (0.56, 0.30)):
            vela = [(x - w * (1.0 if a < 0.9 else 0.8), -80 - h * a), (x + w * (1.0 if a < 0.9 else 0.8), -80 - h * a), (x + w * 0.95 + sw, -80 - h * b), (x - w * 0.95 + sw, -80 - h * b)]
            ops += forma(curva(vela + [vela[0]], 4), BLANCO_R, 4.4, peso=0.25, sp=8)
        if w >= 56:
            cy, cx = -80 - h * 0.45, x + sw * 0.5
            ops += [T(linea((cx - 26, cy - 22), (cx + 26, cy + 22)), 7, peso=0.03), T(linea((cx + 26, cy - 22), (cx - 26, cy + 22)), 7, peso=0.03)]
            ops += [R(pol((cx - 30, cy - 22), (cx - 22, cy - 26), (cx + 30, cy + 22), (cx + 22, cy + 26)), ROJO_CH, peso=0.01, sp=3),
                    R(pol((cx + 30, cy - 22), (cx + 22, cy - 26), (cx - 30, cy + 22), (cx - 22, cy + 26)), ROJO_CH, peso=0.01, sp=3)]
    ops += forma(pol((-150, -330), (-90, -322 + 6 * math.sin(f)), (-150, -306)), BLANCO_R, 3, sp=3)
    ops += [T(linea((-150, -330), (-96, -310)), 3, peso=0.01), T(linea((-96, -330), (-150, -310)), 3, peso=0.01)]
    return Dib(colocar(ops, 0, 0, tam) if tam != 1.0 else ops)


@lru_cache(maxsize=None)
def galera(f=0, color=(196, 70, 50), vela=(240, 220, 120)):
    """Galera de Lepanto: casco largo y bajo, muchos remos, vela latina."""
    ops = forma(curva([(-220, -60), (-190, -16), (0, 0), (190, -16), (250, -50), (190, -40), (-190, -44)], 6), color, 5.4, peso=0.5, sp=9)
    ops += forma(pol((250, -50), (300, -46), (250, -40)), (150, 110, 70), 3.4, sp=3)
    for k in range(13):
        a = 0.3 * math.sin(f * 1.6 + k * 0.5)
        x = -170 + 28 * k
        ops += [T(linea((x, -16), (x - 22 + 34 * a, 50)), 3.2, peso=0.015)]
    ops += [T(linea((-10, -44), (-10, -220)), 5, peso=0.08), T(linea((-120, -100), (120, -250)), 4.4, peso=0.06)]
    ops += forma(pol((-120, -100), (120, -250), (60, -60)), vela, 4.4, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def felipe2(pose=0, cara="serio"):
    d = persona(NEGRO_TERC, PIEL_ROSA, "gorra_negra", cara, (16, 40), pose, traje="tunica", faja=(80, 76, 86), barba=(200, 170, 120), acc_d="cetro")
    ops = gorguera(d.ops)
    ops += forma(pol((-10, -150), (10, -150), (14, -120), (0, -104), (-14, -120)), ORO, 3, sp=3)          # toisón de oro
    return Dib(ops)


@lru_cache(maxsize=None)
def sol_cara(f=0):
    ops = []
    for k in range(12):
        a = k * math.pi / 6 + 0.1 * math.sin(f)
        ops += forma(pol((70 * math.cos(a - 0.12), -110 + 70 * math.sin(a - 0.12)), (112 * math.cos(a), -110 + 112 * math.sin(a)),
                         (70 * math.cos(a + 0.12), -110 + 70 * math.sin(a + 0.12))), (250, 190, 60), 3.6, sp=4)
    ops += forma(elip(0, -110, 68, 68, 0, 1.0, 36), (252, 214, 80), 5.2, peso=0.4, sp=8)
    ops += [punto(-22, -122, 10), punto(22, -122, 10), T(arco_(0, -100, 28, 25, 155, 10), 4.6, peso=0.04)]
    ops += [R(elip(-38, -96, 12, 7, n=12), (240, 140, 120), peso=0.01, sp=3), R(elip(38, -96, 12, 7, n=12), (240, 140, 120), peso=0.01, sp=3)]
    return Dib(ops)


# ------------------------------------------------------------------ Siglo de Oro
@lru_cache(maxsize=None)
def cervantes(pose=0, cara="feliz"):
    d = persona(NEGRO_TERC, PIEL_ROSA, "pelo_rizo", cara, (16, 90), pose, traje="tunica", faja=(110, 90, 70), barba=(150, 120, 90), bigote=True, acc_d="pluma",
                acc_i="libro_q")
    return Dib(gorguera(d.ops))


@lru_cache(maxsize=None)
def rocinante(pose=0):
    """Caballo flaco (Rocinante): el caballo de siempre, más estrecho y con costillas."""
    h = caballo2(pose, (196, 176, 150), (150, 130, 110))
    ops = colocar(list(h.ops), 0, 0, 1.0)
    ops = [(op[0], op[1] * (1, 1.0)) + tuple(op[2:]) for op in ops]
    ops += [T(curva([(-30 + 18 * k, -160), (-26 + 18 * k, -130), (-30 + 18 * k, -110)], 3), 2.6, peso=0.01) for k in range(4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def quijote(pose=0):
    """Don Quijote sobre Rocinante, con la bacía por yelmo y la lanza en ristre."""
    r = persona((150, 140, 130), PIEL_ROSA, "bacia", "enojo", (40, 90), pose, traje="armadura", faja=(150, 110, 70), barba=(200, 196, 190), bigote=True,
                acc_d="lanza_q", alto=1.0)
    ops = _montado(rocinante(pose), r, dy=-120, s=0.6)
    return Dib(ops)


@lru_cache(maxsize=None)
def molino(f=0.0):
    """Molino de viento de La Mancha: torre blanca, tejado cónico y cuatro aspas que giran (f = ángulo)."""
    ops = forma(pol((-56, 0), (-44, -230), (44, -230), (56, 0)), BLANCO_R, 5.4, peso=0.5, sp=9)
    ops += forma(pol((-56, -226), (0, -290), (56, -226)), (100, 90, 90), 5, sp=7)
    ops += forma(curva([(-16, 0), (-16, -50), (0, -64), (16, -50), (16, 0)], 4), (120, 90, 70), 4, sp=4)
    ops += forma(rect(-10, -160, 10, -134, 2), NEGRO_R, 3, sp=3)
    cx, cy = 0, -250
    for k in range(4):
        a = f + k * math.pi / 2
        u = np.array([math.cos(a), math.sin(a)])
        n = np.array([-u[1], u[0]])
        p0 = np.array([cx, cy]) + u * 20
        p1 = np.array([cx, cy]) + u * 170
        ops += [T(np.array([p0, p1]), 4.4, peso=0.03)]
        ops += forma(np.array([p0 + u * 30, p1, p1 + n * 34, p0 + u * 30 + n * 34]), (220, 200, 160), 3.4, sp=5)
    ops += forma(elip(cx, cy, 12, 12, 0, 1.0, 12), (100, 90, 90), 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def velazquez(pose=0, cara="serio"):
    d = persona(NEGRO_TERC, PIEL_ROSA, "pelo_rizo", cara, (16, 80), pose, traje="tunica", faja=(70, 66, 76), bigote=True, acc_d="pincel", acc_i="paleta")
    ops = list(d.ops)
    ops += forma(pol((-8, -150), (8, -150), (8, -136), (20, -136), (20, -124), (8, -124), (8, -100), (-8, -100), (-8, -124), (-20, -124), (-20, -136), (-8, -136)),
                 ROJO_CH, 3, sp=3)                                         # cruz de Santiago
    ops += forma(rect(-36, -176, 36, -160, 3), BLANCO_R, 3.2, sp=3)        # golilla
    return Dib(ops)


@lru_cache(maxsize=None)
def meninas():
    """Cuadro enmarcado: la infanta Margarita con su gran guardainfante, una menina y el pintor al fondo (evocación de Las Meninas, 1656)."""
    ops = forma(rect(-170, -360, 170, 0, 4), (160, 120, 60), 6, peso=0.4, sp=9)
    ops += forma(rect(-148, -338, 148, -22, 3), (90, 80, 70), 4, peso=0.3, sp=9)
    ops += forma(rect(-136, -330, -60, -120, 2), (120, 104, 90), 3, sp=6)                       # el lienzo al fondo
    ops += forma(curva([(-40, -36), (-56, -96), (-30, -150), (30, -150), (56, -96), (40, -36)], 5), (236, 226, 210), 4.4, sp=6)     # guardainfante
    ops += forma(rect(-16, -196, 16, -150, 4), (236, 226, 210), 3.6, sp=4)
    ops += forma(elip(0, -216, 20, 22, 0, 1.0, 20), PIEL_ROSA, 3.8, sp=4) + forma(elip(0, -230, 24, 14, math.pi, 0.5, 14), (230, 200, 120), 3.4, cerrada=False, sp=4)[1:]
    ops += forma(curva([(60, -36), (52, -90), (74, -130), (100, -90), (96, -36)], 5), (200, 160, 150), 3.6, sp=5)
    ops += forma(elip(78, -150, 14, 16, 0, 1.0, 14), PIEL_ROSA, 3.2, sp=3)
    ops += forma(rect(-96, -250, -70, -150, 2), NEGRO_TERC, 3.2, sp=3) + forma(elip(-83, -262, 12, 13, 0, 1.0, 12), PIEL_ROSA, 3, sp=3)
    ops += forma(rect(84, -320, 130, -260, 2), (230, 220, 180), 3, sp=3)                         # la puerta luminosa del fondo
    return Dib(ops)


@lru_cache(maxsize=None)
def bancarrota():
    """Bolsa de dinero vacía con un parche, unas monedas que caen y una grieta."""
    ops = forma(curva([(-70, -150), (-100, -60), (-80, 0), (80, 0), (100, -60), (70, -150), (30, -170), (-30, -170)], 6), (190, 160, 110), 5.4, peso=0.4, sp=9)
    ops += [T(linea((-30, -170), (30, -170)), 6, peso=0.04)] + forma(rect(-40, -100, 0, -60, 3), (150, 120, 80), 3.4, sp=4)
    ops += [T(linea((20, -140), (30, -110), (14, -90), (30, -60), (20, -30)), 4, peso=0.04)]
    for x, y in ((-140, -200), (120, -230), (150, -120)):
        ops += forma(elip(x, y, 18, 18, 0, 1.0, 14), ORO, 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def carlos2(pose=0, cara="lloron"):
    """Carlos II «el Hechizado»: melena larga, mentón prominente, enfermizo."""
    d = persona(NEGRO_TERC, (240, 220, 200), "melena_carlos", cara, (16, 30), pose, traje="tunica", faja=(80, 76, 86))
    ops = gorguera(d.ops)
    ops += forma(curva([(-20, -186), (-14, -170), (0, -164), (14, -170), (20, -186)], 4), (240, 220, 200), 3.4, sp=3)
    ops += sombrero("corona_real", -215.0)
    return Dib(ops)


@lru_cache(maxsize=None)
def cuna_vacia():
    ops = forma(curva([(-110, -120), (-100, -40), (-60, 0), (60, 0), (100, -40), (110, -120)], 5).tolist() + [(-110, -120)], (176, 120, 72), 5.4, peso=0.4, sp=8)
    ops += forma(curva([(-110, -120), (-110, -180), (-60, -220), (0, -230), (0, -120)], 5), (200, 70, 70), 4.6, sp=6)
    ops += forma(pol((-120, 0), (-80, 30), (80, 30), (120, 0), (100, 10), (-100, 10)), (176, 120, 72), 4.4, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def felipe5(pose=0, cara="feliz"):
    d = persona(AZUL_BORBON, PIEL_ROSA, "peluca", cara, (16, 50), pose, traje="tunica", faja=ORO, cuello=BLANCO_R, acc_d="cetro")
    ops = list(d.ops)
    for (x, y) in ((-24, -130), (24, -130), (0, -80)):
        ops += forma(pol((x, y - 16), (x + 6, y - 4), (x + 14, y - 8), (x + 6, y + 8), (x, y + 4), (x - 6, y + 8), (x - 14, y - 8), (x - 6, y - 4)), ORO, 2.4, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def archiduque(pose=0, cara="enojo"):
    d = persona(BLANCO_R, PIEL_ROSA, "peluca", cara, (16, 60), pose, traje="tunica", faja=ROJO_CH, cuello=ROJO_CH, acc_d="espada")
    return d


@lru_cache(maxsize=None)
def penon(bandera=True, f=0):
    """El Peñón de Gibraltar (la roca caliza que cae a pico por el norte) con la bandera británica."""
    ops = forma(curva([(-220, 0), (-200, -60), (-150, -190), (-110, -250), (-60, -236), (40, -170), (140, -100), (220, -40), (240, 0)], 6), (214, 206, 186), 5.6, peso=0.5, sp=10)
    ops += [T(curva([(-150, -180), (-120, -110), (-100, -40)], 4), 3, peso=0.03, v=150), T(curva([(-60, -230), (-40, -150)], 3), 3, peso=0.03, v=150)]
    ops += forma(curva([(-30, -160), (60, -130), (160, -80), (220, -30), (240, 0), (0, 0)], 5), (150, 170, 100), 4, sp=7)
    if bandera:
        x, y = -100, -248
        ops += [T(linea((x, y), (x, y - 120)), 4.4, peso=0.05)]
        fl = [(x, y - 120), (x + 110, y - 118 + 6 * math.sin(f)), (x + 110, y - 52 + 6 * math.sin(f)), (x, y - 56)]
        ops += forma(fl, (40, 60, 130), 3.6, sp=6)
        ops += [R(pol((x, y - 92), (x + 110, y - 90), (x + 110, y - 80), (x, y - 82)), BLANCO_R, peso=0.01, sp=3),
                R(pol((x + 48, y - 120), (x + 62, y - 120), (x + 62, y - 54), (x + 48, y - 54)), BLANCO_R, peso=0.01, sp=3)]
        ops += [R(pol((x, y - 89), (x + 110, y - 87), (x + 110, y - 83), (x, y - 85)), ROJO_CH, peso=0.01, sp=2),
                R(pol((x + 52, y - 120), (x + 58, y - 120), (x + 58, y - 54), (x + 52, y - 54)), ROJO_CH, peso=0.01, sp=2)]
        ops += [T(linea((x, y - 120), (x + 110, y - 54)), 3, peso=0.01), T(linea((x + 110, y - 118), (x, y - 56)), 3, peso=0.01)]
    return Dib(ops)
