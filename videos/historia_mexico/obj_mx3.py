# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de México en 5 minutos» (3/3): CABALLOS, JINETES, CANOAS, GALEONES, LOCOMOTORA, CAÑÓN, ANIMALES y FLORA.
Todo de perfil HACIA LA DERECHA (flip=True para la izquierda); origen en la base."""
import math
from functools import lru_cache

import numpy as np

import obj_mx1 as M1
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_mx1 import (AZUL_EEUU, AZUL_FR, CAQUI_REV, CHARRO_OS, GRANA, HIERRO_MX, JADE_MX, MANTA, OBSIDIANA, OCRE_MX, ORO_MX,
                     PIEL_MESO, PLATA_MX, ROJO_BAND, TURQ_MX, VERDE_BAND)

MADERA_C = (176, 122, 76)
MADERA_O = (128, 86, 54)


def _seg(ax, ay, bx, by, wa, wb):
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / n, dx / n
    return [(ax + nx * wa, ay + ny * wa), (bx + nx * wb, by + ny * wb), (bx - nx * wb, by - ny * wb), (ax - nx * wa, ay - ny * wa)]


def _pata(x0, y0, a1, a2, col, l1=56, l2=56, w1=16, w2=10, casco=OBSIDIANA):
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x0 + l1 * math.sin(r1), y0 + l1 * math.cos(r1)
    fx, fy = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    ops = forma(_seg(x0, y0, kx, ky, w1, w2 * 1.1), col, 4.2, sp=6) + forma(_seg(kx, ky, fx, fy, w2, w2 * 0.85), col, 4.0, sp=5)
    if casco is not None:
        ops += forma(pol((fx - 11, fy - 6), (fx + 12, fy - 6), (fx + 14, fy + 7), (fx - 12, fy + 7)), casco, 3.2, sp=3)
    return ops


_GALOPE = [
    ((-26, 6), (20, -4), (36, 18), (-10, -30)),
    ((-10, -26), (32, 8), (10, -30), (28, 12)),
    ((22, -8), (-26, 6), (-14, -32), (36, 18)),
    ((32, 8), (-10, -26), (28, 12), (10, -30)),
]


@lru_cache(maxsize=None)
def caballo(pose=0, col=(168, 114, 72), crin=(64, 46, 38)):
    """Caballo de perfil hacia la derecha (galope en 4 poses)."""
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
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if not lejos:
            ops += _pata(x, y, a1, a2, col)
    return Dib(ops)


_JINETES = {
    "cortes": (lambda p: M1.cortes(p, "serio"), (142, 94, 62), GRANA),
    "insurgente": (lambda p: M1.morelos(p, "enojo"), (168, 118, 76), VERDE_BAND),
    "trigarante": (lambda p: M1.iturbide(p, "serio"), (234, 228, 218), ORO_MX),
    "eeuu": (lambda p: M1.soldado_eeuu(p, "enojo"), (156, 108, 70), AZUL_EEUU),
    "frances": (lambda p: M1.soldado_frances(p, "enojo"), (132, 92, 62), AZUL_FR),
    "villa": (lambda p: M1.pancho_villa(p, "enojo"), (174, 120, 74), ORO_MX),
    "zapata": (lambda p: M1.zapata(p, "enojo"), (232, 226, 214), GRANA),
}


@lru_cache(maxsize=None)
def jinete(pose=0, quien="villa"):
    """Jinete a caballo en galope (4 poses)."""
    fn, c_cab, c_manta = _JINETES.get(quien, _JINETES["villa"])
    cab = caballo(pose, c_cab)
    jin = fn(pose)
    ops = list(cab.ops)
    ops += forma(rect(-48, -182, 36, -138, 6), c_manta, 4.0, sp=5)
    ops += colocar(list(jin.ops), -6, -158, 0.58)
    return Dib(ops)


@lru_cache(maxsize=None)
def canoa_mexica(pose=0):
    """Canoa de madera navegando con guerrero/remero mexica."""
    dy = 4 * math.sin(pose * math.pi / 2)
    ops = forma(curva([(-148, -32 + dy), (-112, 4 + dy), (112, 4 + dy), (152, -36 + dy), (108, -24 + dy), (-108, -24 + dy)], 6),
                MADERA_C, 5.0, sp=7)
    rem = M1.campesino_pre(pose, "serio")
    ops += colocar(list(rem.ops), -12, -20 + dy, 0.52)
    a = 18 * math.sin(pose * math.pi / 2)
    ops += [T(linea((10 + a * 0.4, -74 + dy), (36 - a, 24 + dy)), 5.0, peso=0.04)]
    ops += [T(B.ondas(-140, 140, 8, 5, 28), 3.4, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def galeon(pose=0):
    """Galeón español / Nao de China con velas hinchadas y cruz de Borgoña."""
    f = pose * 0.8
    ops = forma(curva([(-190, -136), (-176, -36), (-108, 6), (104, 6), (174, -36), (216, -88), (172, -82), (118, -68), (-100, -72), (-136, -152)], 6),
                MADERA_O, 5.6, peso=0.6, sp=9)
    ops += forma(rect(-194, -176, -114, -126, 4), MADERA_C, 4.6, sp=6)
    for x, h, w in ((-142, 220, 44), (-24, 290, 58), (92, 246, 50)):
        ops += [T(linea((x, -72), (x, -72 - h)), 5.2, peso=0.10)]
        sw = 6 * math.sin(f + x * 0.01)
        vela = [(x - w, -72 - h * 0.88), (x + w, -72 - h * 0.88), (x + w * 0.95 + sw, -72 - h * 0.28), (x - w * 0.95 + sw, -72 - h * 0.28)]
        ops += forma(curva(vela + [vela[0]], 4), MANTA, 4.4, sp=7)
        if w >= 54:
            cx, cy = x + sw * 0.5, -72 - h * 0.56
            ops += [T(linea((cx - 24, cy - 20), (cx + 24, cy + 20)), 6.0, peso=0.03),
                    T(linea((cx + 24, cy - 20), (cx - 24, cy + 20)), 6.0, peso=0.03)]
    ops += forma(pol((-24, -362), (34, -352), (-24, -338)), GRANA, 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def locomotora(pose=0):
    """Locomotora de vapor del Porfiriato y la Revolución con humo animado."""
    ops = forma(rect(-176, -138, 92, -46, 6), OBSIDIANA, 5.2, sp=8)
    ops += forma(rect(-182, -212, -68, -134, 4), (72, 66, 64), 4.8, sp=7)
    ops += forma(rect(-154, -194, -96, -152, 3), (186, 214, 232), 3.8, sp=4)
    ops += forma(pol((44, -138), (34, -222), (82, -222), (72, -138)), OBSIDIANA, 4.6, sp=5)
    ops += forma(pol((92, -98), (156, -34), (92, -34)), GRANA, 4.4, sp=5)
    ops += forma(rect(-168, -104, 84, -90, 2), ORO_MX, 3.6, sp=4)
    for x, r in ((-128, 38), (-36, 38), (48, 30)):
        ops += forma(circ(x, -38, r, n=22), GRANA, 4.6, sp=5)
        ops += forma(circ(x, -38, r * 0.35, n=12), ORO_MX, 3.6, sp=3)
        a = pose * math.pi / 2
        ops += [T(linea((x, -38), (x + r * 0.8 * math.cos(a), -38 + r * 0.8 * math.sin(a))), 3.8, peso=0.02)]
    for k in range(3):
        dx = -28 * k - (pose % 4) * 6
        dy = -252 - 24 * k
        ops += forma(circ(58 + dx, dy, 22 + 8 * k, n=16), (218, 214, 208), 3.8, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def canon(pose=0):
    """Cañón de artillería sobre cureña de ruedas de madera."""
    ops = forma(pol((-96, -68), (88, -108), (94, -76), (-86, -32)), (92, 98, 108), 5.0, sp=7)
    ops += forma(circ(-98, -50, 14, n=12), (92, 98, 108), 4.0, sp=3)
    ops += forma(pol((-126, -12), (-20, -56), (16, -42), (-96, 0)), MADERA_C, 4.6, sp=6)
    ops += forma(circ(-12, -44, 44, n=24), MADERA_O, 5.0, sp=6) + forma(circ(-12, -44, 12, n=12), HIERRO_MX, 3.8, sp=3)
    for k in range(6):
        a = math.radians(k * 60 + pose * 15)
        ops += [T(linea((-12, -44), (-12 + 42 * math.cos(a), -44 + 42 * math.sin(a))), 3.4, peso=0.02)]
    if pose % 2 == 1:
        ops += forma(circ(128, -98, 26, n=16), (242, 184, 68), 3.8, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def nopal(variante=0):
    """Nopal mexicano con pencas espinosas y tunas rojas."""
    ops = forma(elip(0, -34, 24, 36, 0, 1.0, 18), VERDE_BAND, 4.4, sp=5)
    ops += forma(elip(-36, -68, 20, 32, -0.45, 1.0, 16), VERDE_BAND, 4.2, sp=5)
    ops += forma(elip(36, -68, 20, 32, 0.45, 1.0, 16), VERDE_BAND, 4.2, sp=5)
    ops += forma(elip(-12, -96, 18, 28, -0.15, 1.0, 16), (72, 158, 96), 4.2, sp=5)
    if variante % 2 == 0:
        ops += forma(elip(26, -112, 16, 24, 0.25, 1.0, 14), (72, 158, 96), 4.0, sp=4)
    for x, y in ((-48, -96), (48, -96), (-14, -126)):
        ops += forma(circ(x, y, 7, n=10), GRANA, 3.2, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def maguey():
    """Agave / maguey azul de pencas largas en roseta."""
    ops = []
    for ang, L in ((-1.1, 88), (-0.75, 108), (-0.38, 124), (0.0, 132), (0.38, 124), (0.75, 108), (1.1, 88)):
        x1, y1 = L * math.sin(ang), -L * math.cos(ang)
        nx, ny = math.cos(ang) * 14, math.sin(ang) * 14
        ops += forma(pol((-nx, 0), (x1, y1), (nx, 0)), JADE_MX, 4.0, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def palmera_selva(h=210):
    """Palmera tropical de las costas de Veracruz, Tabasco y el Caribe."""
    ops = forma(curva([(-12, 0), (-6, -h * 0.5), (6, -h), (16, -h), (8, -h * 0.5), (12, 0)], 5), MADERA_C, 4.4, sp=6)
    for a in (-2.3, -1.7, -1.1, -0.4, 0.4, 1.1, 1.7, 2.3):
        x1, y1 = 10 + 82 * math.sin(a), -h + 44 * abs(math.sin(a)) - 28 * math.cos(a)
        ops += forma(curva([(10, -h), ((10 + x1) / 2, -h - 24), (x1, y1), ((10 + x1) / 2, -h - 6)], 4), VERDE_BAND, 3.8, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def jaguar(pose=0):
    """Jaguar mesoamericano caminando de perfil."""
    p = _GALOPE[pose % 4]
    col = ORO_MX
    osc = (188, 138, 42)
    patas = ((-56, -68), (-70, -68), (52, -68), (66, -68))
    ops = []
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if lejos:
            ops += _pata(x, y, a1 * 0.7, a2 * 0.7, osc, l1=36, l2=34, w1=13, w2=9, casco=None)
    ops += [T(curva([(-82, -88), (-124, -76), (-142, -98)], 5), 6.0, peso=0.04)]
    ops += forma(elip(0, -88, 84, 32, 0, 1.0, 28), col, 5.0, sp=8)
    ops += forma(circ(92, -108, 28, n=20), col, 4.8, sp=6)
    ops += forma(circ(82, -134, 9, n=10), col, 3.4, sp=2) + forma(circ(102, -132, 9, n=10), col, 3.4, sp=2)
    ops += [punto(102, -112, 6), punto(118, -104, 5)]
    for x, y in ((-46, -92), (-18, -98), (12, -86), (38, -96), (-28, -76), (18, -74)):
        ops += [R(circ(x, y, 6, n=8), OBSIDIANA, peso=0.02, sp=2)]
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if not lejos:
            ops += _pata(x, y, a1 * 0.7, a2 * 0.7, col, l1=36, l2=34, w1=13, w2=9, casco=None)
    return Dib(ops)


@lru_cache(maxsize=None)
def buque_carga(pose=0):
    """Buque portacontenedores del comercio exterior moderno."""
    ops = forma(pol((-210, -56), (-184, 0), (184, 0), (222, -62)), (62, 88, 134), 5.0, sp=8)
    ops += forma(rect(-162, -118, -104, -56, 3), MANTA, 4.4, sp=5)
    for k, (x, col) in enumerate(((-82, GRANA), (-18, ORO_MX), (46, VERDE_BAND), (110, (74, 128, 186)))):
        ops += forma(rect(x, -104, x + 58, -56, 2), col, 4.2, sp=5)
    return Dib(ops)
