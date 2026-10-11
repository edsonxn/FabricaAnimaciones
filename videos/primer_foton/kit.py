# -*- coding: utf-8 -*-
"""Kit de dibujos del Short «¿Cómo nació el primer fotón?» (boceto + guache).
Todos los dibujos son `Dib` (coordenadas locales, y hacia abajo) y se pegan como PEGATINAS (recorte de papel con borde y sombra)
sobre fondos pintados a guache. Mascota: Foti, el fotón."""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import boceto as B
from boceto import (AMARILLO, AZUL, AZUL_CL, AZUL_OSC, GRIS, GRIS_CL, MARRON, NARANJA, PIEL, R, ROJO, ROSA, T, VERDE,
                    VERDE_OSC, Dib, arco_, circ, curva, elip, linea)
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

cos, sin, pi = math.cos, math.sin, math.pi

ORO = (255, 214, 66)
ORO_OSC = (255, 168, 40)
CIELO = (120, 176, 238)
VIOLETA = (160, 120, 220)
TURQ = (88, 196, 190)
LIMA = (176, 214, 96)
CAFE = (150, 104, 70)
FUEGO = (244, 98, 52)
PIEL_OSC = (222, 160, 120)


# ------------------------------------------------------------------ caras
def _cara(ojos, boca, ex=19, ye=-6, ym=16, k=1.0, grueso=11):
    ops = []
    L, Rr = (-ex * k, ye), (ex * k, ye)
    if ojos == "abiertos":
        for (x, y) in (L, Rr):
            ops.append(T(linea((x, y - 10), (x, y + 8)), grueso, peso=0.03))
    elif ojos == "grandes":                                    # ojos redondos con pupila
        for (x, y) in (L, Rr):
            ops += [T(circ(x, y, 12, n=18), 4.5, peso=0.07), T(linea((x + 1, y - 2), (x + 1, y + 3)), 9, peso=0.02)]
    elif ojos == "feliz":
        for (x, y) in (L, Rr):
            ops.append(T(arco_(x, y + 8, 11, 200, 340, 8), 5, peso=0.05))
    elif ojos == "cerrados":
        for (x, y) in (L, Rr):
            ops.append(T(arco_(x, y - 2, 11, 20, 160, 8), 5, peso=0.05))
    elif ojos == "miedo":
        for (x, y) in (L, Rr):
            ops += [T(circ(x, y, 13, n=16), 4.5, peso=0.07), T(circ(x, y + 1, 1.5, n=6), 7, peso=0.02)]
    elif ojos == "enojado":
        for (x, y), sg in ((L, 1), (Rr, -1)):
            ops += [T(linea((x, y - 5), (x, y + 9)), grueso, peso=0.03),
                    T(linea((x - 12 * sg, y - 17), (x + 10 * sg, y - 8)), 5.4, peso=0.04)]
    elif ojos == "mareado":
        for (x, y) in (L, Rr):
            a = np.linspace(0, 4.2 * pi, 28)
            r = 2 + 12 * a / (4.2 * pi)
            ops.append(T(np.stack([x + r * np.cos(a), y + r * np.sin(a)], 1), 3.6, peso=0.14))
    elif ojos == "estrellas":
        for (x, y) in (L, Rr):
            for ang in (0, pi / 2, pi / 4, 3 * pi / 4):
                ops.append(T(linea((x - 12 * cos(ang), y - 12 * sin(ang)), (x + 12 * cos(ang), y + 12 * sin(ang))), 4.2, peso=0.03))
    elif ojos == "guino":
        ops += [T(linea((L[0], L[1] - 10), (L[0], L[1] + 8)), grueso, peso=0.03), T(arco_(Rr[0], Rr[1] + 8, 11, 200, 340, 8), 5, peso=0.05)]
    elif ojos == "esfuerzo":
        for (x, y), sg in ((L, 1), (Rr, -1)):
            ops.append(T(linea((x - 11 * sg, y - 9), (x + 3 * sg, y), (x - 11 * sg, y + 9)), 5, peso=0.05))
    elif ojos == "dormido":
        for (x, y) in (L, Rr):
            ops.append(T(arco_(x, y - 4, 11, 20, 160, 8), 4.5, peso=0.05))
    if boca == "sonrisa":
        ops.append(T(arco_(0, ym - 8, 15 * k, 28, 152, 10), 5, peso=0.05))
    elif boca == "abierta":
        P = arco_(0, ym - 10, 17 * k, 5, 175, 12)
        ops += [R(P, ROSA, peso=0.04, sp=5, off=(2, -2)), T(P, 4.8, peso=0.07)]
    elif boca == "o":
        ops.append(T(circ(0, ym + 2, 8 * k, n=14), 4.6, peso=0.05))
    elif boca == "grito":
        a = np.linspace(0, pi, 14)
        P = np.vstack([[(-15 * k, ym - 6)], np.stack([-15 * k * np.cos(a), ym - 6 + 21 * k * np.sin(a)], 1)])
        P = np.vstack([P, P[:1]])
        ops += [R(P, ROSA, peso=0.04, sp=5, off=(2, -2)), T(P, 4.8, peso=0.08)]
    elif boca == "triste":
        ops.append(T(arco_(0, ym + 12, 14 * k, 208, 332, 10), 5, peso=0.05))
    elif boca == "zigzag":
        ops.append(T(linea((-16, ym + 2), (-9, ym - 4), (-3, ym + 4), (4, ym - 4), (10, ym + 4), (16, ym - 3)), 4.6, peso=0.06))
    elif boca == "lengua":
        ops += [R(elip(5, ym + 8, 8, 10, n=14), ROSA, peso=0.03, sp=4), T(arco_(0, ym - 8, 15 * k, 28, 152, 10), 5, peso=0.05),
                T(arco_(5, ym + 6, 8, 20, 160, 8), 3.6, peso=0.03)]
    elif boca == "recta":
        ops.append(T(linea((-11, ym + 2), (11, ym + 2)), 5, peso=0.04))
    elif boca == "dientes":
        P = np.array([(-16, ym - 4), (16, ym - 4), (14, ym + 10), (-14, ym + 10), (-16, ym - 4)], float)
        ops += [T(P, 4.6, peso=0.1)] + [T(linea((x, ym - 4), (x, ym + 10)), 2.8, peso=0.02) for x in (-8, 0, 8)]
    return ops


def _mejillas(x, y, k=1.0):
    return [R(elip(-x, y, 9 * k, 6 * k, n=14), ROSA, peso=0.03, sp=5, off=(2, -2)),
            R(elip(x, y, 9 * k, 6 * k, n=14), ROSA, peso=0.03, sp=5, off=(2, -2))]


# ------------------------------------------------------------------ FOTI, el fotón
@lru_cache(maxsize=None)
def foti(ojos="abiertos", boca="sonrisa", mejillas=True, rayos=12, frio=False):
    c_cuerpo, c_ray = ((176, 212, 252), (120, 170, 232)) if frio else (ORO, ORO_OSC)
    ops = []
    for i in range(rayos):
        a = 2 * pi * i / rayos + pi / rayos
        r0, r1 = 46.0, (82.0 if i % 2 == 0 else 66.0)
        w = 0.19 if i % 2 == 0 else 0.16
        tri = [(r0 * cos(a - w), r0 * sin(a - w)), (r1 * cos(a), r1 * sin(a)), (r0 * cos(a + w), r0 * sin(a + w))]
        ops += [R(tri, c_ray, peso=0.05, sp=6, off=(1, -1)), T(linea(*tri), 4.2, peso=0.06)]
    body = circ(0, 0, 52, n=40)
    ops += [T(body, 6.8, peso=0.5), R(body, c_cuerpo, peso=0.4, sp=9)]
    ops += _cara(ojos, boca, ex=19, ye=-6, ym=17)
    if mejillas:
        ops += _mejillas(33, 12)
    if frio:                                              # bufanda roja
        buf = np.array([(-46, 30), (-22, 44), (22, 44), (46, 30), (50, 52), (22, 64), (-22, 64), (-50, 52), (-46, 30)], float)
        cola_ = np.array([(14, 56), (40, 60), (48, 104), (26, 108), (14, 56)], float)
        ops += [R(buf, (232, 70, 66), peso=0.2, sp=6), T(buf, 4.6, peso=0.2), R(cola_, (232, 70, 66), peso=0.1, sp=6), T(cola_, 4.2, peso=0.1)]
    return Dib(ops)


def cola(t, largo=170.0, amp=15.0, lam=54.0, vel=5.0, ancho=11.0):
    """Cola ondulada de Foti (la onda de luz) que sale hacia la izquierda desde el cuerpo (x = -48)."""
    x = np.linspace(0, largo, 64)
    env = np.minimum(1.0, x / 30.0 + 0.2) * (1 - 0.35 * x / largo)
    yc = amp * env * np.sin(x / lam * 2 * pi - t * vel)
    w = ancho * (1 - x / largo) ** 0.8 + 1.0
    up = np.stack([-48 - x, yc - w], 1)
    dn = np.stack([-48 - x, yc + w], 1)
    poly = np.vstack([up, dn[::-1]])
    return Dib([R(poly, ORO, peso=0.30, sp=8), T(up, 4.4, peso=0.3), T(dn, 4.4, peso=0.3)])


def chispa(n=4, r=60):
    """Destello de cuatro (o más) puntas."""
    P = []
    for i in range(2 * n):
        a = pi * i / n - pi / 2
        rr = r if i % 2 == 0 else r * 0.28
        P.append((rr * cos(a), rr * sin(a)))
    P.append(P[0])
    return Dib([R(P, ORO, peso=0.2, sp=7), T(linea(*P), 4.2, peso=0.25)])


CHISPA = chispa()
CHISPA5 = chispa(5, 50)


# ------------------------------------------------------------------ partículas
@lru_cache(maxsize=None)
def electron(ojos="grandes", boca="o"):
    body = circ(0, 0, 36, n=34)
    return Dib([T(body, 6, peso=0.5), R(body, (112, 170, 250), peso=0.4, sp=9),
                T(linea((-11, -22), (11, -22)), 7.5, peso=0.05)] + _cara(ojos, boca, ex=14, ye=-3, ym=14, k=0.75, grueso=9)
               + _mejillas(24, 11, 0.7))


@lru_cache(maxsize=None)
def proton(ojos="abiertos", boca="sonrisa"):
    body = circ(0, 0, 48, n=36)
    return Dib([T(body, 6.4, peso=0.5), R(body, (244, 112, 92), peso=0.4, sp=9),
                T(linea((-12, -29), (12, -29)), 7.5, peso=0.05), T(linea((0, -41), (0, -17)), 7.5, peso=0.05)]
               + _cara(ojos, boca, ex=17, ye=-4, ym=16, k=0.9) + _mejillas(29, 12, 0.85))


@lru_cache(maxsize=None)
def neutron(ojos="abiertos", boca="sonrisa"):
    body = circ(0, 0, 45, n=36)
    return Dib([T(body, 6.2, peso=0.5), R(body, (170, 176, 192), peso=0.4, sp=9)]
               + _cara(ojos, boca, ex=16, ye=-4, ym=15, k=0.85) + _mejillas(27, 11, 0.8))


@lru_cache(maxsize=None)
def quark(color="rojo", ojos="miedo", boca="o"):
    col = {"rojo": (240, 98, 92), "verde": (112, 200, 108), "azul": (96, 150, 240)}[color]
    body = circ(0, 0, 27, n=26)
    return Dib([T(body, 5, peso=0.4), R(body, col, peso=0.3, sp=8)] + _cara(ojos, boca, ex=10, ye=-2, ym=10, k=0.55, grueso=7))


@lru_cache(maxsize=None)
def mancuerna():
    plate_l = [(-62, -34), (-42, -34), (-42, 34), (-62, 34), (-62, -34)]
    plate_r = [(42, -34), (62, -34), (62, 34), (42, 34), (42, -34)]
    ops = [R(plate_l, (96, 100, 116), peso=0.15, sp=7), T(linea(*plate_l), 5, peso=0.15),
           R(plate_r, (96, 100, 116), peso=0.15, sp=7), T(linea(*plate_r), 5, peso=0.15),
           T(linea((-42, 0), (42, 0)), 9, peso=0.1),
           T(linea((-72, -20), (-72, 20)), 5, peso=0.05), T(linea((72, -20), (72, 20)), 5, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def pesa_rusa():
    """Pesa rusa (kettlebell) de 'MASA'."""
    body = np.array([(-50, 38), (-44, 8), (-24, -6), (24, -6), (44, 8), (50, 38), (40, 56), (-40, 56), (-50, 38)], float)
    asa = arco_(0, -6, 24, 180, 360, 14, ry=30)
    return Dib([T(asa, 9, peso=0.2), T(body, 5.6, peso=0.5), R(body, (80, 84, 100), peso=0.3, sp=8),
                T(arco_(-22, 34, 11, 150, 260, 6), 3.4, peso=0.05)])


@lru_cache(maxsize=None)
def corazon(r=22):
    P = []
    for a in np.linspace(0, 2 * pi, 36):
        x = 16 * sin(a) ** 3
        y = -(13 * cos(a) - 5 * cos(2 * a) - 2 * cos(3 * a) - cos(4 * a))
        P.append((x * r / 17, y * r / 17))
    P.append(P[0])
    return Dib([R(P, (240, 92, 120), peso=0.2, sp=6), T(linea(*P), 4.4, peso=0.25)])


# ------------------------------------------------------------------ interruptor del campo de Higgs
@lru_cache(maxsize=None)
def placa_interruptor():
    P = np.array([(-96, -180), (96, -180), (104, -172), (104, 172), (96, 180), (-96, 180), (-104, 172), (-104, -172), (-96, -180)], float)
    ranura = np.array([(-34, -128), (34, -128), (34, 128), (-34, 128), (-34, -128)], float)
    return Dib([T(P, 7, peso=0.7), R(P, (236, 230, 214), peso=0.6, sp=14),
                R(ranura, (62, 58, 76), peso=0.3, sp=9), T(ranura, 5.4, peso=0.3),
                T(circ(0, -156, 8, n=10), 4, peso=0.05), T(linea((-6, -156), (6, -156)), 3, peso=0.02),
                T(circ(0, 156, 8, n=10), 4, peso=0.05), T(linea((-6, 156), (6, 156)), 3, peso=0.02)])


@lru_cache(maxsize=None)
def palanca(a=0.0):
    """Palanca del interruptor: a = -1 (abajo, apagado) .. 1 (arriba, encendido). Mango rojo con perilla."""
    y = -a * 96
    P = np.array([(-17, 0), (-13, y), (13, y), (17, 0), (-17, 0)], float)
    knob = circ(0, y, 30, n=24)
    return Dib([R(P, (176, 180, 196), peso=0.2, sp=7), T(linea((-17, 0), (-13, y), (13, y), (17, 0)), 5, peso=0.2),
                R(knob, (240, 82, 70), peso=0.2, sp=8), T(knob, 5.6, peso=0.3), T(arco_(-6, y - 4, 16, 200, 280, 6), 3.4, peso=0.03)])


# ------------------------------------------------------------------ calor: termómetro, olla, llama
@lru_cache(maxsize=None)
def termometro(nivel=0.5, ojos="", boca=""):
    tubo = np.array([(-22, -250), (22, -250), (22, 120), (-22, 120), (-22, -250)], float)
    bulbo = circ(0, 150, 54, n=36)
    ops = [T(tubo, 6, peso=0.4), T(bulbo, 6, peso=0.5), R(bulbo, (232, 50, 56), peso=0.3, sp=8)]
    top = 120 - (120 + 235) * nivel
    col = np.array([(-11, top), (11, top), (11, 128), (-11, 128), (-11, top)], float)
    ops += [R(col, (232, 50, 56), peso=0.3, sp=6), T(linea((-11, top), (11, top)), 3.4, peso=0.03)]
    for k in range(8):
        ops.append(T(linea((22, -230 + 44 * k), (40 if k % 2 == 0 else 34, -230 + 44 * k)), 3.8, peso=0.03))
    if ojos:
        cara = _cara(ojos, boca, ex=19, ye=140, ym=162, k=1.0, grueso=10)
        ops += cara
    return Dib(ops)


@lru_cache(maxsize=None)
def olla():
    cuerpo = np.vstack([arco_(0, 0, 150, 0, 180, 26, ry=135), [(-150, 0)]])                 # media luna inferior
    borde = elip(0, 0, 160, 38, n=40)
    sopa = elip(0, 4, 144, 30, n=40)
    ops = [T(linea((-110, 118), (-130, 170)), 9, peso=0.1), T(linea((110, 118), (130, 170)), 9, peso=0.1),
           T(linea((0, 135), (0, 175)), 9, peso=0.08),
           T(np.vstack([cuerpo, cuerpo[:1]]), 7, peso=0.8), R(np.vstack([cuerpo, cuerpo[:1]]), (74, 76, 92), peso=0.7, sp=11),
           T(arco_(-150, 4, 26, 180, 340, 8), 7, peso=0.1), T(arco_(150, 4, 26, 200, 360, 8), 7, peso=0.1),
           T(borde, 7, peso=0.5), R(borde, (110, 112, 128), peso=0.3, sp=9),
           R(sopa, (252, 148, 64), peso=0.4, sp=9, ang=20), T(sopa, 4, peso=0.3),
           T(arco_(-92, 78, 34, 150, 250, 8), 4, peso=0.05)]
    return Dib(ops)


def llama(t, x, y, s=1.0, ph=0.0):
    """Una llama (Dib por cuadro, danza)."""
    w = 1 + 0.12 * sin(t * 11 + ph)
    h = 1 + 0.2 * sin(t * 8.5 + ph * 1.7)
    P = curva([(0, 0), (-44 * w, -30), (-34 * w, -92 * h), (-8, -130 * h), (6 * w, -170 * h), (26, -118 * h), (46 * w, -60 * h), (36, -8), (0, 0)], 8)
    Q = curva([(0, -4), (-22 * w, -22), (-14, -58 * h), (4, -80 * h), (22, -46 * h), (18, -14), (0, -4)], 8)
    return Dib([R(P, FUEGO, peso=0.15, sp=7), T(P, 4.5, peso=0.3), R(Q, ORO, peso=0.1, sp=5), T(Q, 3, peso=0.15)])


# ------------------------------------------------------------------ gente y casa
def _tubo(P, w0, w1=None, n=10):
    """Polígono cerrado alrededor de la polilínea P (brazos, piernas, colas) con ancho w0 -> w1."""
    P = curva(P, n) if len(P) > 2 else np.asarray(P, float)
    w1 = w0 if w1 is None else w1
    d = np.gradient(P, axis=0)
    d /= np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    w = np.linspace(w0, w1, len(P))[:, None] / 2
    return np.vstack([P + nrm * w, (P - nrm * w)[::-1]])


@lru_cache(maxsize=None)
def persona(ojos="grandes", boca="o", brazos="abajo", pelo_col=(96, 66, 54)):
    """Un chaval en pijama visto de frente (~370 px de alto; pies en y = 190). Cabeza grande, cuerpo corto."""
    cabeza = circ(0, -118, 68, n=44)
    pelo = np.vstack([arco_(0, -122, 72, 190, 350, 22), [(62, -156), (40, -176), (14, -158), (-10, -180), (-36, -158), (-62, -150), (-70, -130)]])
    cuerpo = curva([(-52, -52), (-30, -62), (30, -62), (52, -52), (60, 52), (-60, 52)], 8, True)
    ops = []
    for sx in (-1, 1):
        pierna = _tubo([(sx * 24, 46), (sx * 26, 120), (sx * 27, 176)], 32)
        zapato = np.array([(sx * 27 - 20, 176), (sx * 27 + 20, 176), (sx * 27 + 30, 198), (sx * 27 - 30, 198), (sx * 27 - 20, 176)], float)
        ops += [R(pierna, (96, 128, 214), peso=0.25, sp=8), T(pierna, 5, peso=0.35),
                R(zapato, (214, 90, 80), peso=0.1, sp=6), T(zapato, 4.6, peso=0.15)]
    arms = {"abajo": ([(-58, -40), (-92, -6), (-100, 46)], [(58, -40), (92, -6), (100, 46)]),
            "arriba": ([(-58, -40), (-98, -90), (-106, -150)], [(58, -40), (98, -90), (106, -150)]),
            "mejillas": ([(-58, -40), (-100, -20), (-72, -84)], [(58, -40), (100, -20), (72, -84)]),
            "tele": ([(-58, -40), (-104, -34), (-134, -76)], [(58, -40), (104, -34), (134, -76)])}[brazos]
    for A in arms:
        tubo = _tubo(A, 28, 24)
        mano = circ(A[-1][0], A[-1][1] + (6 if brazos == "abajo" else 0), 15, n=14)
        ops += [R(tubo, TURQ, peso=0.3, sp=8), T(tubo, 5, peso=0.35), R(mano, PIEL, peso=0.1, sp=6), T(mano, 4.4, peso=0.12)]
    ops += [T(cuerpo, 6, peso=0.6), R(cuerpo, TURQ, peso=0.5, sp=10),
            T(linea((-56, -12), (56, -12)), 4, peso=0.1), T(linea((-58, 22), (58, 22)), 4, peso=0.1)]
    ops += [T(cabeza, 6.4, peso=0.7), R(cabeza, PIEL, peso=0.6, sp=10),
            R(pelo, pelo_col, peso=0.4, sp=8), T(pelo, 5.5, peso=0.3)]
    ops += _cara(ojos, boca, ex=26, ye=-120, ym=-90, k=1.35, grueso=13) + _mejillas(46, -96, 1.3)
    return Dib(ops)


@lru_cache(maxsize=None)
def espalda():
    """Cabeza y hombros de alguien visto de espaldas (mirando la tele)."""
    cabeza = circ(0, -74, 62, n=40)
    pelo = circ(0, -80, 64, n=40)
    hombros = curva([(-190, 120), (-172, 28), (-120, -14), (0, -26), (120, -14), (172, 28), (190, 120)], 10)
    cuerpo = np.vstack([hombros, [(190, 200), (-190, 200)], hombros[:1]])
    oreja_i, oreja_d = elip(-62, -68, 11, 17, n=12), elip(62, -68, 11, 17, n=12)
    return Dib([T(np.vstack([hombros]), 7, peso=0.7), R(cuerpo, (210, 96, 90), peso=0.7, sp=12),
                R(oreja_i, PIEL, peso=0.05, sp=5), T(oreja_i, 3.6, peso=0.05), R(oreja_d, PIEL, peso=0.05, sp=5), T(oreja_d, 3.6, peso=0.05),
                T(pelo, 6.4, peso=0.7), R(pelo, (80, 56, 50), peso=0.6, sp=9),
                T(arco_(-6, -74, 40, 20, 80, 8), 3.4, peso=0.05), T(arco_(14, -64, 34, 40, 110, 8), 3.4, peso=0.05)])


@lru_cache(maxsize=None)
def tele():
    """Tele de tubo con antena de «orejas de conejo». Pantalla en x∈[-132,62], y∈[-98,78]."""
    caja = np.array([(-168, -128), (168, -128), (168, 126), (-168, 126), (-168, -128)], float)
    pant = np.array([(-132, -98), (62, -98), (62, 78), (-132, 78), (-132, -98)], float)
    ops = [T(linea((-60, -134), (-130, -250)), 6, peso=0.2), T(linea((-30, -134), (46, -262)), 6, peso=0.2),
           R(circ(-132, -254, 9, n=12), (240, 90, 74), peso=0.05, sp=5), T(circ(-132, -254, 9, n=12), 4, peso=0.05),
           R(circ(48, -266, 9, n=12), (240, 90, 74), peso=0.05, sp=5), T(circ(48, -266, 9, n=12), 4, peso=0.05),
           T(caja, 7, peso=0.9), R(caja, (170, 120, 80), peso=0.8, sp=12),
           T(pant, 6, peso=0.5), R(pant, (60, 66, 76), peso=0.4, sp=9),
           T(circ(106, -62, 20, n=18), 5, peso=0.2), R(circ(106, -62, 20, n=18), (232, 224, 204), peso=0.1, sp=6),
           T(linea((106, -62), (106, -78)), 4, peso=0.03),
           T(circ(106, -8, 17, n=18), 5, peso=0.2), R(circ(106, -8, 17, n=18), (232, 224, 204), peso=0.1, sp=6),
           T(linea((106, -8), (115, -16)), 4, peso=0.03)]
    for k in range(5):
        ops.append(T(linea((86, 40 + 12 * k), (128, 40 + 12 * k)), 3.6, peso=0.03))
    ops += [T(linea((-130, 128), (-142, 176)), 9, peso=0.1), T(linea((130, 128), (142, 176)), 9, peso=0.1)]
    return Dib(ops)


TELE_PANT = (-132, -98, 62, 78)


@lru_cache(maxsize=None)
def tierra():
    c = circ(0, 0, 70, n=40)
    cont = [curva([(-36, -34), (-12, -52), (10, -34), (2, -10), (-20, 6), (-44, -8)], 6, True),
            curva([(18, 12), (44, 6), (54, 30), (34, 54), (14, 38)], 6, True)]
    return Dib([T(c, 6, peso=0.4), R(c, (96, 156, 236), peso=0.4, sp=9)]
               + [R(x, (118, 198, 110), peso=0.15, sp=6) for x in cont] + [T(x, 3.4, peso=0.1) for x in cont])


@lru_cache(maxsize=None)
def hoja_calendario(texto=""):
    P = np.array([(-70, -86), (70, -86), (70, 86), (-70, 86), (-70, -86)], float)
    top = np.array([(-70, -86), (70, -86), (70, -48), (-70, -48), (-70, -86)], float)
    ops = [R(P, (252, 250, 240), peso=0.2, sp=14), T(P, 5.4, peso=0.7), R(top, (236, 70, 70), peso=0.15, sp=8), T(linea(*top), 4.4, peso=0.2),
           T(circ(-34, -86, 6, n=10), 3.6, peso=0.03), T(circ(34, -86, 6, n=10), 3.6, peso=0.03)]
    for k in range(3):
        ops.append(T(linea((-48, -22 + 26 * k), (48 - 14 * (k == 2), -22 + 26 * k)), 4.4, peso=0.1))
    return Dib(ops)


@lru_cache(maxsize=None)
def nave_sol_estrella(r=40):
    return chispa(8, r)


# ------------------------------------------------------------------ texto de papel recortado
_FUENTES_TXT = [os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts/LuckiestGuy-Regular.ttf"),
                os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Black.ttf"), "C:/Windows/Fonts/ariblk.ttf"]


@lru_cache(maxsize=32)
def _fnt(px):
    for p in _FUENTES_TXT:
        if os.path.exists(p):
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()


@lru_cache(maxsize=256)
def _masc(txt, px):
    f = _fnt(px)
    bb = f.getbbox(txt)
    w, h = bb[2] + 24, int(px * 1.45) + 16
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((12, 6), txt, font=f, fill=255)
    return np.asarray(im, np.uint8)


def ancho_txt(txt, px):
    return _masc(txt, px).shape[1]


def rotulo(h, txt, x, y, px=96, rot=0.0, color=(238, 70, 62), s=1.0, u=1.0, tira=False, tinta_borde=True, sombra=True):
    """Letras de papel recortado centradas en (x, y): relleno de crayón + contorno de tinta + pegatina. u = fracción visible (escritura).
    tira=True añade una tira de papel detrás (cinta)."""
    if u <= 0 or s <= 0.02:
        return
    m = _masc(txt, int(px))
    if s != 1.0 or rot:
        hh, ww = m.shape
        Mx = cv2.getRotationMatrix2D((ww / 2, hh / 2), -math.degrees(rot), s)
        nw, nh = int(ww * s * 1.1 + hh * abs(sin(rot)) * s + 4), int(hh * s * 1.1 + ww * abs(sin(rot)) * s + 4)
        Mx[0, 2] += nw / 2 - ww / 2
        Mx[1, 2] += nh / 2 - hh / 2
        m = cv2.warpAffine(m, Mx, (nw, nh), flags=cv2.INTER_LINEAR)
    hh, ww = m.shape
    x0, y0 = int(round(x - ww / 2)), int(round(y - hh / 2))
    cols = ww if u >= 1 else int(ww * u)
    if tira:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
        ys, xs = np.nonzero(m[::2, ::2])
        if len(xs):
            xa, xb, ya, yb = xs.min() * 2 - 14, xs.max() * 2 + 14, ys.min() * 2 - 8, ys.max() * 2 + 8
            strip = np.zeros_like(m)
            cv2.rectangle(strip, (max(0, xa), max(0, ya)), (min(ww - 1, xb), min(hh - 1, yb)), 255, -1)
            h.peg_mascara(strip, x0, y0, cols)
            h.sello(strip, x0, y0, (252, 246, 224), 255)
    h.peg_mascara(m, x0, y0, cols)
    borde = cv2.dilate(m, np.ones((5, 5), np.uint8)) - m if tinta_borde else None
    h.sello(m, x0, y0, color, 255)
    if borde is not None:
        h.pegar_mascara(borde, x0, y0, cols)


def poner(h, d, x, y, s=1.0, rot=0.0, flip=False, u=1.0, fs=0, sem=0, te=0.0, vida=1.0, sq=0.0, lapiz=0.0, peg=True):
    if s <= 0.02 or u <= 0.001:
        return
    d.dibujar(h, x, y, s, rot, flip, u, fs, sem, sq=sq, lapiz=lapiz, tv=te, vida=vida, peg=peg)


def entrada(t, t0, modo="pop", dur=0.38):
    """Efecto de aparición -> (multiplicador de escala, u de dibujo, squash, lápiz, dy). Antes de t0: nada (sm=0)."""
    if t < t0:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    v = prog(t, t0, t0 + dur)
    if modo == "pop":
        return max(0.02, e_back(v, 2.4)), 1.0, 0.28 * (1 - v) * sin(v * 12), 0.0, 0.0
    if modo == "pluma":
        return 1.0, v, 0.0, 0.0, 0.0
    if modo == "lt":
        u = prog(t, t0 + 0.12, t0 + 0.12 + dur)
        return 1.0, max(u, 0.001), 0.0, 1 - u, 0.0
    if modo == "sube":
        return 1.0, 1.0, 0.0, 0.0, 260 * (1 - e_out(v))
    if modo == "cae":
        h = 1 - e_out(v)
        return 1.0, 1.0, -0.15 * h, 0.0, -520 * h
    return 1.0, 1.0, 0.0, 0.0, 0.0


@lru_cache(maxsize=None)
def bombilla(ojos="dormido", boca="recta", brillo=0):
    """Bombilla de papel. brillo 0 = apagada (vidrio gris), 1 = encendida."""
    vidrio = np.vstack([arco_(0, -40, 70, 140, 400, 34), [(26, 66), (-26, 66)]])
    base = np.array([(-28, 66), (28, 66), (28, 118), (-28, 118), (-28, 66)], float)
    col = (255, 232, 130) if brillo else (206, 212, 222)
    ops = [R(vidrio, col, peso=0.5, sp=9), T(np.vstack([vidrio, vidrio[:1]]), 6.4, peso=0.6),
           R(base, (150, 150, 164), peso=0.15, sp=7), T(base, 5, peso=0.15),
           T(linea((-28, 82), (28, 82)), 3.4, peso=0.03), T(linea((-28, 98), (28, 98)), 3.4, peso=0.03),
           T(circ(0, 126, 9, n=10, vuelta=0.5, a0=0.0), 4.4, peso=0.05),
           T(linea((-16, 66), (-12, 20), (-4, 8), (0, 24), (4, 8), (12, 20), (16, 66)), 3.4, peso=0.2)]
    ops += _cara(ojos, boca, ex=24, ye=-50, ym=-22, k=1.1, grueso=11)
    return Dib(ops)


def cronometro(ang=0.0):
    c = circ(0, 0, 70, n=40)
    ops = [T(linea((-14, -82), (14, -82)), 9, peso=0.05), T(linea((0, -70), (0, -82)), 8, peso=0.03),
           T(c, 6.4, peso=0.6), R(c, (244, 240, 226), peso=0.5, sp=10)]
    for k in range(12):
        a = k * pi / 6
        ops.append(T(linea((56 * cos(a), 56 * sin(a)), (64 * cos(a), 64 * sin(a))), 3.6, peso=0.02))
    ops += [T(linea((0, 0), (50 * sin(ang), -50 * cos(ang))), 5, peso=0.1), T(circ(0, 0, 5, n=8), 5, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def gota_sudor():
    P = np.vstack([[(0, -22)], arco_(0, 6, 12, 120, 420, 16), [(0, -22)]])
    return Dib([R(P, (130, 190, 250), peso=0.1, sp=5), T(P, 3.6, peso=0.2)])
