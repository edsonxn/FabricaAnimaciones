# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de Egipto» (v2) 3/3: ANIMALES, CARROS, JINETES, BARCOS y PLANTAS.
Caballo (4 poses de galope), carro de guerra egipcio / hicso / hitita, camello (4 poses) y jinete árabe, jinetes mameluco, mongol y cruzado,
cocodrilo, hipopótamo, ibis, gata, buey arando, palmera datilera, papiro, loto, algodón; barca de papiro, barco de la expedición a Punt,
barco de los Pueblos del Mar, trirreme griego, galera romana, barco de Cleopatra, barco del grano, falúa, vapor del Canal de Suez
y buque portacontenedores. Todo de perfil HACIA LA DERECHA (flip=True para la izquierda); origen en la base."""
import math
from functools import lru_cache

import numpy as np

import obj_eg1 as E1
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_eg1 import (ARENISCA, BLANCO_EG, BRONCE, HIERRO, LAPIS, LINO, NEGRO_EG, OCRE_R, ORO_EG, PIEL_EG, TURQ, VERDE_NILO)

MADERA_C = (176, 124, 78)
MADERA_O = (130, 88, 58)
PAPIRO_V = (130, 170, 100)


def _seg(ax, ay, bx, by, wa, wb):
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / n, dx / n
    return [(ax + nx * wa, ay + ny * wa), (bx + nx * wb, by + ny * wb), (bx - nx * wb, by - ny * wb), (ax - nx * wa, ay - ny * wa)]


def _pata(x0, y0, a1, a2, col, l1=56, l2=56, w1=16, w2=10, casco=NEGRO_EG):
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x0 + l1 * math.sin(r1), y0 + l1 * math.cos(r1)
    fx, fy = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    ops = forma(_seg(x0, y0, kx, ky, w1, w2 * 1.1), col, 4.2, sp=6) + forma(_seg(kx, ky, fx, fy, w2, w2 * 0.85), col, 4.0, sp=5)
    if casco is not None:
        ops += forma(pol((fx - 11, fy - 6), (fx + 12, fy - 6), (fx + 14, fy + 7), (fx - 12, fy + 7)), casco, 3.2, sp=3)
    return ops


_GALOPE = [((-26, 6), (20, -4), (36, 18), (-10, -30)), ((-10, -26), (32, 8), (10, -30), (28, 12)),
           ((22, -8), (-26, 6), (-14, -32), (36, 18)), ((32, 8), (-10, -26), (28, 12), (10, -30))]


@lru_cache(maxsize=None)
def caballo(pose=0, col=(176, 120, 76), crin=(70, 50, 40), penacho=None):
    """Caballo de perfil hacia la derecha (galope en 4 poses), cuello arqueado, crin, cola; penacho opcional (caballos de carro)."""
    p = _GALOPE[pose % 4]
    osc = tuple(int(c * 0.8) for c in col)
    patas = ((-70, -110), (-88, -110), (64, -110), (82, -110))
    ops = []
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if lejos:
            ops += _pata(x, y, a1, a2, osc)
    ops += forma(curva([(-100, -140), (-128, -146), (-156, -120), (-164, -84), (-146, -96), (-136, -122)], 5), crin, 4.2, sp=5)
    ops += forma(elip(-4, -136, 108, 42, 0.0, 1.0, 36), col, 5.6, peso=0.6, sp=10)
    cuello = [(54, -162), (84, -204), (112, -240), (142, -258), (166, -246), (186, -210), (182, -192), (162, -196), (142, -210), (122, -182), (100, -126)]
    ops += forma(curva(cuello, 6), col, 5.2, peso=0.4, sp=8)
    ops += forma(curva([(106, -232), (84, -210), (62, -176), (50, -156), (72, -166), (96, -196), (120, -232)], 5), crin, 3.8, sp=5)
    ops += forma(pol((136, -254), (142, -282), (152, -256)), col, 3.4, sp=3)
    ops += [punto(154, -232, 8), punto(180, -202, 5)]
    if penacho:
        ops += forma(curva([(140, -262), (128, -300), (144, -330), (160, -300), (150, -262)], 5), penacho, 3.6, sp=4)
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if not lejos:
            ops += _pata(x, y, a1, a2, col)
    return Dib(ops)


_CONDUCTOR = {
    "egipcio": lambda pose: E1.arquero_eg(pose, "enojo"),
    "ahmose": lambda pose: E1.ahmose(pose, "enojo"),
    "ramses": lambda pose: E1.ramses(pose, "enojo"),
    "tutmosis": lambda pose: E1.tutmosis(pose, "serio"),
    "hicso": lambda pose: E1.hicso(pose, "enojo"),
    "hitita": lambda pose: E1.soldado_hitita(pose, "enojo"),
}


@lru_cache(maxsize=None)
def carro(pose=0, quien="egipcio", col=(196, 150, 90), caballo_col=(176, 120, 76), penacho=(200, 60, 50)):
    """Carro de guerra ligero de dos ruedas de seis radios, tirado por un caballo (con otro detrás asomando) y su conductor."""
    ops = colocar(list(caballo(pose + 1, tuple(int(c * 0.85) for c in caballo_col), penacho=penacho).ops), 46, -6, 0.86)
    ops += colocar(list(caballo(pose, caballo_col, penacho=penacho).ops), 70, 0, 0.9)
    ops += [T(curva([(-110, -120), (-40, -130), (40, -140), (110, -160)], 5), 5, peso=0.04)]                       # lanza del carro
    ops += forma(pol((-210, -170), (-120, -172), (-110, -100), (-200, -90)), col, 5, sp=7)                           # caja
    ops += [T(curva([(-210, -170), (-160, -200), (-120, -172)], 4), 4.4, peso=0.03)]
    ops += forma(rect(-196, -138, -130, -120, 3), OCRE_R if quien != "hitita" else (110, 120, 170), 3.6, sp=4)
    conductor = _CONDUCTOR.get(quien, _CONDUCTOR["egipcio"])(pose)
    ops += colocar(list(conductor.ops), -164, -100, 0.62)
    r = 52
    cx, cy = -150, -56
    ops += forma(circ(cx, cy, r, n=30), None, 5.6) + [T(circ(cx, cy, 10, n=12), 4, peso=0.02)]
    for k in range(6):
        a = math.radians(k * 60 + pose * 15)
        ops.append(T(linea((cx + 10 * math.cos(a), cy + 10 * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))), 3.6, peso=0.02))
    ops += [R(circ(cx, cy, r, n=30), (214, 176, 110), peso=0.02, sp=6)]
    return Dib(ops)


_PASO_C = [((-16, 4), (14, -4), (22, 8), (-8, -16)), ((-6, -14), (20, 6), (6, -18), (16, 10)),
           ((14, -4), (-16, 4), (-8, -16), (22, 8)), ((20, 6), (-6, -14), (16, 10), (6, -18))]


@lru_cache(maxsize=None)
def camello(pose=0, col=(206, 170, 112), carga=True):
    """Dromedario de perfil hacia la derecha (4 poses de paso), con joroba y carga opcional."""
    p = _PASO_C[pose % 4]
    osc = tuple(int(c * 0.82) for c in col)
    patas = ((-70, -130), (-84, -130), (60, -130), (74, -130))
    ops = []
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if lejos:
            ops += _pata(x, y, a1, a2, osc, l1=68, l2=66, w1=14, w2=9, casco=None)
    ops += forma(curva([(-120, -150), (-110, -200), (-60, -230), (-10, -280), (40, -236), (90, -200), (110, -160), (80, -124), (-100, -124)], 6), col, 5.4, peso=0.6, sp=9)
    ops += forma(curva([(96, -176), (136, -210), (150, -270), (170, -300), (206, -300), (222, -284), (206, -268), (178, -262), (166, -220), (126, -150)], 5),
                 col, 5, sp=7)
    ops += [punto(196, -290, 7), T(curva([(220, -282), (214, -272)], 2), 3, peso=0.02), T(curva([(-120, -150), (-136, -120), (-130, -96)], 4), 3.6, peso=0.02)]
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if not lejos:
            ops += _pata(x, y, a1, a2, col, l1=68, l2=66, w1=14, w2=9, casco=None)
    if carga:
        ops += forma(rect(-100, -260, -40, -200, 6), (150, 80, 70), 4.2, sp=5) + forma(rect(30, -250, 86, -196, 6), (80, 110, 150), 4.2, sp=5)
        ops += [T(linea((-70, -260), (60, -250)), 3, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def jinete_camello(pose=0):
    """Guerrero árabe del siglo VII a lomos de un dromedario."""
    jin = E1.amr(pose, "serio")
    return Dib(list(camello(pose, carga=False).ops) + colocar(list(jin.ops), -10, -246, 0.6) +
               forma(curva([(-70, -244), (-50, -210), (40, -206), (60, -240), (0, -256)], 5), (200, 60, 50), 4, sp=5))


_JINETES = {"mameluco": (lambda p: E1.mameluco(p, "enojo"), (220, 214, 200), (200, 120, 60)),
            "mongol": (lambda p: E1.mongol(p, "enojo"), (120, 90, 66), (110, 104, 92)),
            "cruzado": (lambda p: E1.cruzado(p, "enojo"), (226, 222, 214), (230, 230, 220)),
            "saladino": (lambda p: E1.saladino(p, "serio"), (236, 232, 222), (214, 160, 60)),
            "frances": (lambda p: E1.napoleon(p, "serio"), (90, 70, 56), (60, 82, 150))}


@lru_cache(maxsize=None)
def jinete(pose=0, quien="mameluco"):
    fn, cab, manta = _JINETES[quien]
    r = fn(pose)
    ops = list(caballo(pose, cab).ops) + colocar(list(r.ops), 0, -128, 0.6)
    ops += forma(curva([(-70, -176), (-56, -118), (44, -112), (66, -176), (0, -188)], 5), manta, 4.2, sp=6)
    return Dib(ops)


# ------------------------------------------------------------------ animales del Nilo
@lru_cache(maxsize=None)
def cocodrilo(pose=0):
    ondula = 6 * math.sin(pose * 1.6)
    P = curva([(-200, -20 + ondula), (-140, -30), (-60, -44), (20, -46), (90, -40), (150, -36), (220, -30), (226, -18), (150, -12), (20, -8), (-80, -10), (-200, -12 + ondula)], 7)
    ops = forma(P, (110, 140, 90), 5, sp=8)
    for k in range(10):
        x = -110 + 24 * k
        ops += forma(pol((x - 8, -42), (x, -56), (x + 8, -42)), (90, 120, 76), 3, sp=2)
    ops += [punto(150, -46, 8), T(linea((150, -26), (222, -24)), 3, peso=0.02)]
    for x in (-40, 70):
        ops += forma(pol((x - 10, -12), (x - 24, 6), (x + 6, 6), (x + 6, -12)), (110, 140, 90), 3.6, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def hipopotamo():
    ops = forma(curva([(-130, -40), (-120, -110), (-40, -146), (60, -140), (120, -110), (150, -80), (160, -40), (100, -30), (-110, -30)], 6), (150, 130, 150), 5.2, sp=8)
    ops += forma(elip(140, -84, 40, 36, 0, 1.0, 20), (160, 140, 160), 4.6, sp=6) + [punto(130, -108, 8), punto(166, -86, 5), punto(156, -86, 5)]
    ops += forma(elip(110, -130, 8, 10, 0, 1.0, 10), (160, 140, 160), 3.4, sp=3)
    ops += [T(ondas(-160, 190, -30, 5, 30), 3.4, peso=0.02), T(ondas(-140, 170, -14, 4, 26, 1.0), 3, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def ibis(pose=0):
    ops = forma(elip(0, -150, 46, 30, -0.2, 1.0, 22), BLANCO_EG, 4.6, sp=6)
    ops += forma(curva([(-40, -156), (-62, -150), (-50, -136)], 3), NEGRO_EG, 3.6, sp=3)
    ops += [T(curva([(30, -166), (46, -200), (54, -226)], 4), 5, peso=0.03)] + forma(elip(58, -232, 12, 11, 0, 1.0, 12), NEGRO_EG, 3.6, sp=3)
    ops += [T(curva([(66, -232), (94, -220), (110, -196)], 4), 4.4, peso=0.03)]
    l = 18 * math.sin(pose * 1.4)
    ops += [T(linea((-6, -124), (-10 - l, 0)), 3.6, peso=0.02), T(linea((10, -124), (14 + l, 0)), 3.6, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def gata():
    """Gata sentada (Bastet) con collar dorado."""
    ops = forma(curva([(-40, 0), (-50, -60), (-36, -130), (-20, -170), (20, -170), (36, -130), (50, -60), (40, 0)], 6), (70, 64, 66), 5, sp=7)
    ops += forma(elip(0, -196, 34, 30, 0, 1.0, 22), (70, 64, 66), 4.8, sp=6)
    ops += forma(pol((-30, -210), (-28, -250), (-8, -222)), (70, 64, 66), 4, sp=3) + forma(pol((30, -210), (28, -250), (8, -222)), (70, 64, 66), 4, sp=3)
    ops += [R(elip(-12, -198, 6, 5, n=10), (220, 200, 90), peso=0.02, sp=2), R(elip(12, -198, 6, 5, n=10), (220, 200, 90), peso=0.02, sp=2)]
    ops += [T(arco_(0, -172, 30, 20, 160, 10), 4, peso=0.02), R(circ(0, -146, 7, n=10), ORO_EG, peso=0.02, sp=2)]
    ops += [T(curva([(40, -10), (80, -20), (90, -60), (70, -80)], 4), 6, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def buey(pose=0, arado=True):
    col = (200, 170, 130)
    p = _PASO_C[pose % 4]
    patas = ((-60, -90), (-74, -90), (50, -90), (64, -90))
    ops = []
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if lejos:
            ops += _pata(x, y, a1 * 0.6, a2 * 0.6, tuple(int(c * 0.82) for c in col), l1=46, l2=44, w1=14, w2=10)
    ops += forma(curva([(-100, -110), (-96, -150), (-40, -166), (50, -164), (100, -150), (110, -110), (60, -86), (-80, -86)], 6), col, 5.2, sp=8)
    ops += forma(elip(130, -140, 36, 28, 0.3, 1.0, 20), col, 4.6, sp=6) + [punto(128, -150, 7)]
    ops += [T(curva([(118, -164), (106, -196), (124, -208)], 3), 5, peso=0.03), T(curva([(140, -164), (150, -196), (168, -202)], 3), 5, peso=0.03)]
    ops += [R(elip(-20, -130, 26, 16, n=14), (170, 130, 100), peso=0.02, sp=4)]
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if not lejos:
            ops += _pata(x, y, a1 * 0.6, a2 * 0.6, col, l1=46, l2=44, w1=14, w2=10)
    if arado:
        ops += [T(linea((90, -160), (-200, -90)), 5, peso=0.04), T(linea((-200, -90), (-230, -10)), 6, peso=0.03), T(linea((-210, -60), (-260, -110)), 5, peso=0.03)]
        ops += colocar(list(E1.campesino(pose, "feliz", None).ops), -290, 0, 0.6)
    return Dib(ops)


@lru_cache(maxsize=None)
def palmera(h=300, inclin=0.0):
    ops = []
    tronco = [(0 + inclin * k * 10, -k * h / 10) for k in range(11)]
    ops += forma(np.vstack([np.array(tronco) + (-10, 0), (np.array(tronco) + (10, 0))[::-1]]), (150, 110, 70), 4.4, sp=5)
    for k in range(10):
        ops += [T(linea((tronco[k][0] - 10, tronco[k][1]), (tronco[k][0] + 10, tronco[k][1] - 6)), 2.4, peso=0.01)]
    tx, ty = tronco[-1]
    for k in range(7):
        a = math.radians(-170 + 26 * k)
        ex, ey = tx + 110 * math.cos(a), ty + 70 * math.sin(a) + 40
        mx, my = tx + 60 * math.cos(a), ty + 40 * math.sin(a) - 20
        P = curva([(tx, ty), (mx, my), (ex, ey)], 6)
        ops += forma(np.vstack([P + (0, -8), P[::-1] + (0, 8)]), (110, 160, 90), 3.6, sp=4)
    ops += [R(elip(tx - 8, ty + 18, 12, 10, n=10), (200, 120, 60), peso=0.02, sp=3), R(elip(tx + 10, ty + 20, 12, 10, n=10), (200, 120, 60), peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def papiro_planta():
    ops = []
    for k in range(5):
        a = (k - 2) * 0.16
        x1, y1 = 180 * math.sin(a), -220 * math.cos(a) + abs(k - 2) * 20
        ops += [T(linea((0, 0), (x1, y1)), 3.6, peso=0.03)]
        ops += forma(pol((x1, y1), (x1 - 34, y1 - 40), (x1 + 34, y1 - 40)), PAPIRO_V, 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def loto():
    ops = forma(elip(0, -20, 90, 16, 0, 1.0, 24), (110, 160, 100), 4, sp=5)
    for k in range(5):
        a = (k - 2) * 0.4
        ops += forma(curva([(0, -30), (60 * math.sin(a) - 18, -30 - 80 * math.cos(a) * 0.9), (60 * math.sin(a), -40 - 100 * math.cos(a)),
                            (60 * math.sin(a) + 18, -30 - 80 * math.cos(a) * 0.9)], 5, cerrado=True), (236, 190, 210) if k % 2 else (226, 150, 190), 3.8, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def algodon():
    ops = [T(curva([(0, 0), (4, -80), (-6, -160)], 4), 4, peso=0.03), T(curva([(2, -90), (40, -130)], 2), 3.4, peso=0.02), T(curva([(-2, -60), (-44, -100)], 2), 3.4, peso=0.02)]
    for x, y in ((-6, -170), (44, -140), (-48, -110)):
        ops += forma(curva([(x - 22, y), (x - 20, y - 22), (x, y - 30), (x + 20, y - 22), (x + 22, y), (x, y + 12)], 5, cerrado=True), BLANCO_EG, 3.6, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ barcos (de perfil hacia la derecha)
def _remos(n, x0, dx, y0, largo, fase):
    ops = []
    for k in range(n):
        a = 0.28 * math.sin(fase * 1.4 + k * 0.6)
        x = x0 + dx * k
        ops.append(T(linea((x, y0), (x - 16 + 40 * a, y0 + largo)), 3.4, peso=0.02))
    return ops


@lru_cache(maxsize=None)
def barca_papiro(f=0):
    """Barca de haces de papiro con proa y popa altas, cabina de esteras y remo timón."""
    casco = np.vstack([curva([(-150, -70), (-120, -26), (-60, -6), (0, 0), (60, -6), (120, -26), (150, -70)], 10),
                       curva([(150, -70), (106, -26), (50, -14), (0, -12), (-50, -14), (-106, -26), (-150, -70)], 10)])
    ops = forma(casco, PAPIRO_V, 5, sp=8)
    for x in (-150, 150):
        ops += forma(elip(x, -78, 12, 16, 0, 1.0, 14), ORO_EG, 3.8, sp=4)
    ops += [rayita(x, -14, x, -4, 3.2) for x in (-90, -60, -30, 0, 30, 60, 90)]
    ops += forma(trap(-40, 40, -60, -44, 44, -14), (222, 196, 150), 4.4, sp=6) + forma(rect(-46, -66, 46, -58, 2), MADERA_C, 3.8, sp=4)
    ops += [T(linea((110, -30), (164, 10 + 6 * math.sin(f))), 4.4, peso=0.03)]
    return Dib(ops + [T(ondas(-160, 160, 10, 5, 26, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def barco_punt(f=0):
    """Barco de la expedición de Hatshepsut al país de Punt: casco largo, gran vela ancha, remeros, árboles de incienso a bordo."""
    casco = np.vstack([curva([(-220, -70), (-190, -20), (-100, -4), (0, 0), (100, -4), (190, -20), (240, -76)], 10),
                       curva([(240, -76), (180, -40), (100, -32), (0, -30), (-100, -32), (-180, -40), (-220, -70)], 10)])
    ops = forma(casco, MADERA_C, 5.4, peso=0.6, sp=9)
    ops += forma(elip(244, -84, 12, 14, 0, 1.0, 12), ORO_EG, 3.6, sp=3)
    ops += [T(linea((0, -30), (0, -300)), 5, peso=0.08)]
    vela = curva([(-150, -290), (0, -300), (150, -290)], 6).tolist() + [(140, -120), (0, -112), (-140, -120)]
    ops += forma(np.array(vela), LINO, 5, peso=0.4, sp=8)
    ops += [T(linea((-150, -290), (150, -290)), 5, peso=0.04), T(linea((-140, -120), (140, -120)), 4.4, peso=0.03)]
    for x in (-150, 150):
        ops += [T(linea((x, -290), (x * 1.3, -60)), 2.4, peso=0.02)]
    for x in (-150, -90, 60, 120):
        ops += forma(rect(x - 16, -66, x + 16, -34, 4), (176, 110, 70), 3.6, sp=3) + forma(elip(x, -86, 22, 20, 0, 1.0, 14), (110, 160, 90), 3.6, sp=4)
    ops += _remos(9, -170, 40, -30, 70, f)
    return Dib(ops + [T(ondas(-240, 260, 40, 6, 30, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def barco_pueblos_mar(f=0):
    """Barco de los Pueblos del Mar: casco recto con proa y popa en cabeza de pájaro y guerreros con plumas."""
    casco = pol((-200, -60), (-170, -10), (170, -10), (200, -60), (160, -40), (-160, -40))
    ops = forma(casco, (150, 110, 80), 5.2, sp=8)
    for s_ in (-1, 1):
        ops += forma(curva([(s_ * 190, -56), (s_ * 214, -110), (s_ * 240, -120), (s_ * 226, -96), (s_ * 214, -80)], 4), (150, 110, 80), 4.4, sp=4) + [punto(s_ * 226, -110, 6)]
    ops += [T(linea((0, -40), (0, -230)), 5, peso=0.06)] + forma(rect(-90, -226, 90, -120, 4), (232, 220, 190), 4.6, sp=6)
    ops += [T(linea((-90, -226), (90, -226)), 4.4, peso=0.03)]
    for k, x in enumerate((-120, -60, 60, 120)):
        ops += colocar(list(E1.pueblo_mar(k, "enojo", "plumas" if k % 2 else "cuernos").ops), x, -40, 0.4)
    return Dib(ops + [T(ondas(-220, 220, 0, 6, 30, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def trirreme(f=0, vela=(236, 214, 170), escudos=(70, 110, 170)):
    """Trirreme/galera griega: espolón, ojo pintado en la proa, tres filas de remos."""
    casco = np.vstack([curva([(-220, -80), (-200, -30), (-100, -10), (100, -10), (200, -24), (240, -16)], 8),
                       curva([(240, -16), (200, -56), (100, -66), (-100, -66), (-200, -76), (-220, -80)], 8)])
    ops = forma(casco, (70, 70, 80), 5.2, sp=8)
    ops += forma(curva([(-220, -80), (-250, -130), (-226, -150), (-214, -112)], 4), (70, 70, 80), 4.4, sp=4)
    ops += forma(elip(176, -44, 14, 9, 0, 1.0, 12), BLANCO_EG, 3.4, sp=2) + [punto(178, -44, 7)]
    ops += [T(linea((0, -66), (0, -280)), 5, peso=0.08)] + forma(rect(-110, -270, 110, -130, 4), vela, 4.8, sp=7)
    for k in range(7):
        ops += forma(elip(-150 + 50 * k, -76, 16, 16, 0, 1.0, 12), escudos if k % 2 else (200, 70, 60), 3.4, sp=3)
    ops += _remos(10, -180, 38, -20, 60, f) + _remos(10, -170, 38, -40, 76, f + 1)
    return Dib(ops + [T(ondas(-240, 260, 34, 6, 30, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def galera_romana(f=0):
    return Dib(list(trirreme(f, (220, 120, 100), (186, 52, 46)).ops) +
               [T(linea((140, -66), (140, -150)), 4, peso=0.03)] + forma(pol((140, -150), (190, -140), (140, -126)), (186, 52, 46), 3.4, sp=3))


@lru_cache(maxsize=None)
def barco_cleopatra(f=0):
    """Nave capitana de Cleopatra: casco dorado, vela púrpura, toldo y popa en flor de papiro."""
    casco = np.vstack([curva([(-230, -100), (-200, -30), (-100, -10), (100, -10), (200, -30), (240, -90)], 8),
                       curva([(240, -90), (200, -60), (100, -66), (-100, -66), (-200, -64), (-230, -100)], 8)])
    ops = forma(casco, ORO_EG, 5.4, sp=8)
    ops += forma(elip(-234, -112, 16, 20, 0, 1.0, 14), PAPIRO_V, 4, sp=4) + forma(elip(244, -98, 12, 14, 0, 1.0, 12), PAPIRO_V, 3.6, sp=3)
    ops += [T(linea((0, -66), (0, -300)), 5, peso=0.08)] + forma(rect(-120, -290, 120, -140, 4), (130, 70, 130), 4.8, sp=7)
    ops += forma(pol((-170, -130), (-60, -130), (-70, -66), (-160, -66)), (200, 70, 60), 4, sp=5)
    ops += colocar(list(E1.cleopatra(0, "feliz").ops), -116, -66, 0.36)
    ops += _remos(10, -180, 40, -24, 64, f)
    return Dib(ops + [T(ondas(-250, 260, 34, 6, 30, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def barco_grano(f=0):
    """Gran barco mercante romano cargado de sacos de trigo («el granero de Roma»)."""
    casco = np.vstack([curva([(-200, -90), (-180, -30), (-80, -6), (80, -6), (180, -30), (210, -70)], 8),
                       curva([(210, -70), (170, -60), (80, -64), (-80, -64), (-180, -70), (-200, -90)], 8)])
    ops = forma(casco, MADERA_C, 5.2, sp=8)
    ops += forma(curva([(-200, -90), (-224, -130), (-206, -150), (-190, -116)], 4), MADERA_C, 4, sp=4)
    for k in range(5):
        ops += colocar(list(E2_saco().ops), -120 + 50 * k, -62, 0.32)
    ops += [T(linea((40, -64), (40, -300)), 5, peso=0.08)] + forma(rect(-60, -290, 140, -150, 4), (226, 200, 160), 4.8, sp=7)
    ops += forma(pol((-50, -200), (130, -200), (130, -170), (-50, -170)), (186, 52, 46), 3, sp=3)
    return Dib(ops + [T(ondas(-220, 230, 20, 6, 30, f * 0.8), 3.4, peso=0.04)])


def E2_saco():
    import obj_eg2
    return obj_eg2.saco_grano()


@lru_cache(maxsize=None)
def falua(f=0):
    """Falúa del Nilo con su vela latina triangular."""
    casco = np.vstack([curva([(-120, -40), (-100, -10), (0, 0), (100, -10), (130, -44)], 8), curva([(130, -44), (90, -30), (0, -26), (-100, -30), (-120, -40)], 8)])
    ops = forma(casco, (90, 120, 160), 5, sp=7)
    ops += [T(linea((-10, -26), (-10, -200)), 4.4, peso=0.05)]
    ops += forma(pol((-150, -40), (60, -330), (20, -46)), BLANCO_EG, 4.6, sp=7) + [T(linea((-150, -40), (60, -330)), 4.4, peso=0.04)]
    return Dib(ops + [T(ondas(-140, 150, 12, 5, 26, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def vapor_suez(f=0):
    """Vapor de rueda de 1869 con banderas, dos chimeneas humeantes y su rueda de paletas."""
    ops = []
    for k in range(3):
        ops += forma(elip(-20 + 30 * k + 6 * math.sin(f + k), -330 - 40 * k, 20 + 8 * k, 16 + 6 * k, 0, 1.0, 16), (200, 196, 190), 3, sp=4)
    casco = pol((-230, -90), (-200, -10), (200, -10), (250, -96))
    ops += forma(casco, (60, 66, 80), 5.2, sp=8)
    ops += forma(rect(-150, -150, 150, -90, 4), BLANCO_EG, 4.6, sp=6)
    for k in range(6):
        ops += forma(elip(-120 + 46 * k, -120, 9, 9, 0, 1.0, 10), (150, 190, 220), 3, sp=2)
    for x in (-40, 40):
        ops += forma(rect(x - 16, -270, x + 16, -150, 3), (180, 60, 50), 4.4, sp=5) + forma(rect(x - 16, -270, x + 16, -250, 2), NEGRO_EG, 3.6, sp=3)
    ops += forma(elip(0, -70, 60, 60, 0, 0.5, 20), (160, 120, 80), 4.4, cerrada=False, sp=5)
    for k in range(5):
        a = math.radians(200 + 35 * k + f * 30)
        ops.append(T(linea((0, -70), (60 * math.cos(a), -70 + 60 * math.sin(a))), 3, peso=0.02))
    ops += [T(linea((-200, -90), (-200, -260)), 3.6, peso=0.04), T(linea((200, -90), (200, -240)), 3.6, peso=0.04)]
    ops += forma(rect(-200, -260, -140, -224, 2), (200, 50, 46), 3.4, sp=3) + forma(rect(200, -240, 256, -206, 2), (60, 82, 150), 3.4, sp=3)
    return Dib(ops + [T(ondas(-250, 260, 0, 6, 30, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def buque_moderno(f=0):
    """Buque portacontenedores de hoy (cruza el canal)."""
    ops = forma(pol((-300, -100), (-280, -10), (260, -10), (310, -100)), (60, 80, 110), 5.2, sp=8)
    cols = [(200, 70, 60), (70, 130, 170), (230, 180, 70), (110, 160, 110), (200, 120, 70)]
    for f_ in range(3):
        for c in range(9):
            x = -240 + 50 * c
            ops += forma(rect(x, -150 - 40 * f_, x + 46, -112 - 40 * f_, 2), cols[(c + f_ * 2) % 5], 3.2, sp=3)
    ops += forma(rect(210, -260, 260, -100, 3), BLANCO_EG, 4.4, sp=5) + [T(linea((220, -230), (250, -230)), 2.6, peso=0.02)]
    return Dib(ops + [T(ondas(-320, 320, 0, 6, 34, f * 0.8), 3.4, peso=0.04)])


# ------------------------------------------------------------------ añadidos (Punt, Napoleón)
@lru_cache(maxsize=None)
def babuino():
    col = (150, 140, 120)
    ops = forma(curva([(-40, 0), (-50, -60), (-30, -110), (20, -116), (44, -70), (40, 0)], 6), col, 5, sp=7)
    ops += forma(elip(10, -140, 32, 30, 0, 1.0, 20), col, 4.6, sp=6) + forma(elip(30, -134, 18, 14, 0, 1.0, 14), (220, 150, 140), 3.6, sp=4)
    ops += [punto(6, -148, 7), punto(22, -148, 7), T(curva([(-40, -30), (-70, -50), (-80, -90)], 4), 5, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def jirafa():
    col = (230, 186, 100)
    ops = []
    for x in (-50, -30, 30, 50):
        ops += forma(rect(x - 8, -150, x + 8, 0, 4), col, 4.2, sp=4)
    ops += forma(curva([(-80, -150), (-70, -200), (60, -210), (80, -150)], 5), col, 5, sp=7)
    ops += forma(pol((40, -200), (80, -380), (104, -376), (70, -190)), col, 4.6, sp=5)
    ops += forma(elip(104, -390, 30, 18, 0.3, 1.0, 16), col, 4.4, sp=4) + [punto(104, -396, 6), T(linea((90, -406), (88, -426)), 3, peso=0.02)]
    for x, y in ((-40, -180), (0, -186), (30, -172), (66, -260), (80, -320), (-60, -166)):
        ops += [R(elip(x, y, 10, 8, n=10), (160, 100, 50), peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def arbol_incienso():
    ops = forma(trap(-36, 36, -50, -28, 28, 0), (176, 110, 70), 4.2, sp=4)
    ops += [T(curva([(0, -50), (-6, -100), (4, -140)], 4), 5, peso=0.03)]
    for x, y in ((-30, -140), (20, -150), (0, -180), (-40, -110), (36, -114)):
        ops += forma(elip(x, y, 34, 24, 0, 1.0, 16), (110, 160, 90), 3.8, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def navio(f=0, bandera_fr=True):
    """Navío de línea de 1798 (tres palos, velas cuadras, portas de cañón) con la bandera tricolor."""
    ops = forma(pol((-230, -120), (-200, -10), (190, -10), (250, -110), (-230, -110)), (110, 76, 56), 5.2, sp=8)
    ops += forma(rect(-210, -80, 220, -64, 2), (230, 200, 120), 3.6, sp=3)
    for k in range(9):
        ops += forma(rect(-180 + 44 * k, -78, -168 + 44 * k, -66, 1), NEGRO_EG, 2.4, sp=2)
    for x, h in ((-120, 300), (20, 340), (150, 280)):
        ops += [T(linea((x, -110), (x, -110 - h)), 5, peso=0.06)]
        for j in range(3):
            y0 = -130 - j * h / 3.2
            ops += forma(pol((x - 70 + 12 * j, y0 - h / 4.2), (x + 70 - 12 * j, y0 - h / 4.2), (x + 64 - 12 * j, y0), (x - 64 + 12 * j, y0)), BLANCO_EG, 3.6, sp=5)
    if bandera_fr:
        ops += forma(rect(-230, -200, -206, -160, 1), (60, 82, 150), 3, sp=2) + forma(rect(-206, -200, -182, -160, 1), BLANCO_EG, 3, sp=2)
        ops += forma(rect(-182, -200, -158, -160, 1), (200, 50, 46), 3, sp=2)
        ops += [T(linea((-230, -200), (-230, -110)), 3, peso=0.02)]
    return Dib(ops + [T(ondas(-250, 270, 0, 6, 30, f * 0.8), 3.4, peso=0.04)])


@lru_cache(maxsize=None)
def paloma(f=0):
    """Paloma de la paz con una ramita de olivo (2 poses de aleteo)."""
    a = 70 if f % 2 == 0 else -20
    ops = forma(curva([(-70, -40), (-30, -66), (30, -64), (70, -50), (90, -58), (80, -40), (40, -24), (-40, -24), (-90, -20), (-80, -36)], 6, cerrado=True),
                BLANCO_EG, 4.6, sp=5)
    ops += forma(curva([(-20, -56), (-40, -56 - a), (10, -60 - a * 1.1), (30, -60)], 5), (236, 236, 246), 4.2, sp=4)
    ops += [punto(70, -54, 6), T(linea((88, -54), (104, -52)), 4, peso=0.02)]
    ops += [T(curva([(100, -52), (130, -44), (150, -30)], 4), 3.4, peso=0.02)]
    for k in range(3):
        ops += forma(elip(116 + 14 * k, -46 + 6 * k, 8, 4, 0.5, 1.0, 10), (110, 160, 90), 2.6, sp=2)
    return Dib(ops)
