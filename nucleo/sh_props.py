# -*- coding: utf-8 -*-
"""Props compartidos de los Shorts de ciencia (boceto + guache): se suman a nucleo/sh_kit.py.
Todos son `Dib` en coordenadas locales (y hacia abajo, origen en el centro). Ver videos/*/_props_hoja.py para la hoja de pruebas."""
import math
from functools import lru_cache

import numpy as np

import boceto as B
from boceto import R, T, Dib, arco_, circ, curva, elip, linea
from sh_kit import (AMARILLO, AZUL_CL, CAFE, FUEGO, GRIS, GRIS_CL, LIMA, ORO, ORO_OSC, PIEL, PIEL_OSC, ROSA, TURQ, VIOLETA, _cara, _mejillas,
                    _tubo)

cos, sin, pi = math.cos, math.sin, math.pi
BLANCO = (252, 250, 244)
VERDE = (96, 188, 112)
ROJO = (232, 70, 66)
AZUL = (96, 150, 240)
CIELO = (150, 200, 250)
NARANJA = (250, 150, 60)


# ================================================================== plátano y radiactividad
@lru_cache(maxsize=None)
def platano(ojos="grandes", boca="sonrisa", mejillas=True):
    cx, cy, Rr = 0.0, -135.0, 185.0
    a = np.linspace(math.radians(28), math.radians(152), 40)
    t = np.linspace(0, 1, 40)
    th = 50 * np.sin(pi * t) ** 0.85 + 2
    out = np.stack([cx + (Rr + th) * np.cos(a), cy + (Rr + th) * np.sin(a)], 1)
    inn = np.stack([cx + (Rr - th) * np.cos(a), cy + (Rr - th) * np.sin(a)], 1)
    body = np.vstack([out, inn[::-1], out[:1]])
    e0, e1 = out[0], out[-1]
    tip = np.array([(e0[0] - 2, e0[1] - 6), (e0[0] + 14, e0[1] + 8), (e0[0] + 2, e0[1] + 18), (e0[0] - 10, e0[1] + 6)])
    stem = np.array([(e1[0] + 4, e1[1] - 2), (e1[0] - 14, e1[1] - 12), (e1[0] - 6, e1[1] - 52), (e1[0] + 16, e1[1] - 50), (e1[0] + 14, e1[1] - 16)])
    ridge = np.stack([cx + Rr * np.cos(a[5:-5]), cy + Rr * np.sin(a[5:-5])], 1)
    ops = [R(stem, (150, 130, 60), peso=0.1, sp=6), T(np.vstack([stem, stem[:1]]), 4.6, peso=0.2),
           R(body, (254, 226, 70), peso=0.5, sp=9), T(body, 6.4, peso=0.6),
           R(tip, (120, 84, 56), peso=0.05, sp=5), T(np.vstack([tip, tip[:1]]), 4.4, peso=0.1), T(ridge, 3.2, peso=0.2)]
    ops += _cara(ojos, boca, ex=24, ye=36, ym=64, k=1.15, grueso=11)
    if mejillas:
        ops += _mejillas(42, 56, 1.1)
    return Dib(ops)


@lru_cache(maxsize=None)
def trebol(r=70):
    """Símbolo de radiactividad (trébol)."""
    c = circ(0, 0, r, n=40)
    ops = [R(c, (252, 214, 60), peso=0.4, sp=8), T(c, 6.0, peso=0.5)]
    for k in range(3):
        a0 = -pi / 2 + k * 2 * pi / 3 - pi / 6
        P = [(0.0, 0.0)] + [(r * 0.86 * cos(a0 + u), r * 0.86 * sin(a0 + u)) for u in np.linspace(0, pi / 3, 8)] + [(0.0, 0.0)]
        ops += [R(P, (40, 38, 46), peso=0.2, sp=6), T(linea(*P), 4, peso=0.2)]
    ops += [R(circ(0, 0, r * 0.2, n=14), (40, 38, 46), peso=0.1, sp=5), T(circ(0, 0, r * 0.2, n=14), 4, peso=0.1)]
    return Dib(ops)


@lru_cache(maxsize=None)
def detector(aguja=0.0):
    """Detector de radiación de mano; aguja -1..1."""
    cuerpo = np.array([(-100, -130), (100, -130), (110, -118), (110, 150), (96, 160), (-96, 160), (-110, 150), (-110, -118), (-100, -130)], float)
    dial = np.vstack([arco_(0, -10, 78, 180, 360, 20), [(78, -10), (-78, -10)]])
    ang = -pi / 2 + aguja * 1.1
    ops = [T(linea((60, -130), (84, -250)), 8, peso=0.1), T(circ(84, -258, 10, n=10), 5, peso=0.05),
           T(cuerpo, 7, peso=0.9), R(cuerpo, (250, 188, 60), peso=0.8, sp=11),
           R(dial, (252, 248, 232), peso=0.4, sp=8), T(np.vstack([dial, dial[:1]]), 5, peso=0.4),
           T(linea((0, -10), (78 * cos(ang) * 0.95, -10 + 78 * sin(ang) * 0.95)), 5.4, peso=0.1), T(circ(0, -10, 6, n=8), 5, peso=0.02)]
    for k in range(7):
        a = pi + k * pi / 6
        ops.append(T(linea((64 * cos(a), -10 + 64 * sin(a)), (74 * cos(a), -10 + 74 * sin(a))), 3.4, peso=0.02))
    for k in range(4):
        ops.append(T(linea((-70, 60 + 16 * k), (70, 60 + 16 * k)), 3.8, peso=0.04))
    ops += [R(circ(70, 128, 12, n=12), ROJO, peso=0.05, sp=5), T(circ(70, 128, 12, n=12), 4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def diente(ojos="grandes", boca="sonrisa"):
    P = curva([(-70, -80), (-30, -96), (30, -96), (70, -80), (82, -20), (60, 40), (50, 110), (30, 120), (14, 60), (0, 56), (-14, 60), (-30, 120), (-50, 110), (-60, 40), (-82, -20)], 8, True)
    P = np.vstack([P, P[:1]])
    return Dib([R(P, (232, 242, 252), peso=0.5, sp=9), T(P, 6.4, peso=0.7)] + _cara(ojos, boca, ex=22, ye=-44, ym=-14, k=1.1, grueso=11) + _mejillas(40, -22, 1.0))


@lru_cache(maxsize=None)
def balanza(a=0.0, L=250):
    """Balanza de brazos (a = ángulo del brazo en rad, + = baja la derecha). Los platos van en los extremos: ver `balanza_puntas`."""
    c, s = cos(a), sin(a)
    ops = [T(linea((0, 0), (0, 180)), 10, peso=0.2)]
    base = np.array([(-90, 200), (90, 200), (60, 170), (-60, 170), (-90, 200)], float)
    ops += [R(base, (170, 120, 80), peso=0.2, sp=8), T(base, 5.4, peso=0.2)]
    beam = np.array([(-L * c - 8 * s, -L * s + 8 * c), (L * c - 8 * s, L * s + 8 * c), (L * c + 8 * s, L * s - 8 * c), (-L * c + 8 * s, -L * s - 8 * c)], float)
    beam = np.vstack([beam, beam[:1]])
    ops += [R(beam, (210, 160, 90), peso=0.3, sp=8), T(beam, 5.4, peso=0.3), R(circ(0, 0, 18, n=14), (230, 190, 80), peso=0.05, sp=5), T(circ(0, 0, 18, n=14), 5, peso=0.05)]
    for sg in (-1, 1):
        ex, ey = sg * L * c, sg * L * s
        plato = np.array([(ex - 90, ey + 120), (ex + 90, ey + 120), (ex + 70, ey + 140), (ex - 70, ey + 140), (ex - 90, ey + 120)], float)
        ops += [T(linea((ex, ey), (ex - 80, ey + 120)), 3.4, peso=0.1), T(linea((ex, ey), (ex + 80, ey + 120)), 3.4, peso=0.1),
                R(plato, (190, 196, 210), peso=0.2, sp=8), T(plato, 5, peso=0.2)]
    return Dib(ops)


def balanza_puntas(a, L=250):
    """Centro de los platos (sobre ellos se apoyan los objetos) respecto al origen de la balanza."""
    c, s = cos(a), sin(a)
    return (-L * c, -L * s + 116), (L * c, L * s + 116)


@lru_cache(maxsize=None)
def aureola():
    e = elip(0, 0, 70, 18, n=30)
    return Dib([T(e, 9, peso=0.6), R(np.vstack([elip(0, 0, 70, 18, n=30), elip(0, 0, 54, 10, n=30)[::-1]]), ORO, peso=0.2, sp=6)])


@lru_cache(maxsize=None)
def tache(r=34):
    return Dib([T(linea((-r, -r), (r, r)), 14, peso=0.15), T(linea((-r, r), (r, -r)), 14, peso=0.15)])


@lru_cache(maxsize=None)
def palomita(r=34):
    P = linea((-r, 0), (-r * 0.3, r * 0.8), (r, -r * 0.7))
    return Dib([T(P, 16, peso=0.25)])


@lru_cache(maxsize=None)
def medalla(n="1"):
    c = circ(0, 0, 54, n=34)
    cinta = np.array([(-30, 40), (-6, 40), (-26, 110), (-52, 90), (-30, 40)], float)
    cinta2 = np.array([(30, 40), (6, 40), (26, 110), (52, 90), (30, 40)], float)
    return Dib([R(cinta, ROJO, peso=0.1, sp=6), T(cinta, 4.4, peso=0.1), R(cinta2, ROJO, peso=0.1, sp=6), T(cinta2, 4.4, peso=0.1),
                R(c, ORO, peso=0.4, sp=8), T(c, 6, peso=0.5), T(circ(0, 0, 40, n=30), 3.4, peso=0.3),
                T(linea((-6, -22), (6, -30), (6, 22)), 7, peso=0.1)])


# ================================================================== espacio: Luna, Tierra, astronauta, eclipse
@lru_cache(maxsize=None)
def luna(ojos="grandes", boca="sonrisa", r=88):
    c = circ(0, 0, r, n=44)
    ops = [R(c, (236, 232, 214), peso=0.5, sp=9), T(c, 6.4, peso=0.6)]
    for (x, y, rr) in [(-48, -42, 16), (44, -50, 11), (52, 28, 18), (-60, 30, 10), (6, 62, 12)]:
        cr = circ(x * r / 88, y * r / 88, rr * r / 88, n=14)
        ops += [R(cr, (206, 200, 180), peso=0.05, sp=5), T(cr, 3.4, peso=0.1)]
    ops += _cara(ojos, boca, ex=24 * r / 88, ye=-8, ym=20, k=1.1 * r / 88, grueso=11) + _mejillas(40 * r / 88, 14, 1.0)
    return Dib(ops)


@lru_cache(maxsize=None)
def tierra(ojos="grandes", boca="sonrisa", r=96):
    c = circ(0, 0, r, n=44)
    k = r / 96.0
    cont = [curva([(-52, -40), (-18, -66), (14, -44), (4, -12), (-26, 8), (-60, -10)], 6, True),
            curva([(24, 14), (58, 8), (70, 36), (46, 62), (20, 44)], 6, True)]
    ops = [T(c, 6.4, peso=0.6), R(c, (104, 162, 240), peso=0.5, sp=9)]
    ops += [R(np.asarray(x) * k, (126, 204, 112), peso=0.15, sp=6) for x in cont] + [T(np.asarray(x) * k, 3.4, peso=0.1) for x in cont]
    ops += _cara(ojos, boca, ex=26 * k, ye=-6, ym=22, k=1.2 * k, grueso=11) + _mejillas(46 * k, 16, 1.1)
    return Dib(ops)


@lru_cache(maxsize=None)
def astronauta(ojos="grandes", boca="sonrisa", brazo="abajo"):
    casco = circ(0, -110, 62, n=36)
    visor = elip(0, -108, 46, 38, n=26)
    cuerpo = curva([(-50, -52), (50, -52), (58, 60), (-58, 60)], 8, True)
    pl = np.array([(-40, 60), (-8, 60), (-10, 150), (-44, 150), (-40, 60)], float)
    pr = np.array([(8, 60), (40, 60), (44, 150), (10, 150), (8, 60)], float)
    bl = np.array([(-48, 150), (-8, 150), (-8, 168), (-52, 168), (-48, 150)], float)
    br = np.array([(8, 150), (48, 150), (52, 168), (8, 168), (8, 150)], float)
    ops = [R(pl, BLANCO, peso=0.2, sp=8), T(pl, 5, peso=0.2), R(pr, BLANCO, peso=0.2, sp=8), T(pr, 5, peso=0.2),
           R(bl, (130, 134, 150), peso=0.1, sp=6), T(bl, 5, peso=0.1), R(br, (130, 134, 150), peso=0.1, sp=6), T(br, 5, peso=0.1)]
    mochila = np.array([(-74, -40), (-52, -40), (-52, 36), (-74, 36), (-74, -40)], float)
    ops += [R(mochila, GRIS_CL, peso=0.1, sp=7), T(mochila, 5, peso=0.1)]
    arms = {"abajo": ([(-52, -36), (-84, 4), (-90, 56)], [(52, -36), (84, 4), (90, 56)]),
            "arriba": ([(-52, -36), (-92, -70), (-96, -130)], [(52, -36), (92, -70), (96, -130)]),
            "dcha": ([(-52, -36), (-84, 4), (-90, 56)], [(52, -36), (96, -40), (122, -90)])}[brazo]
    for A in arms:
        tubo = _tubo(A, 28, 24)
        ops += [R(tubo, BLANCO, peso=0.2, sp=8), T(tubo, 5, peso=0.3), R(circ(A[-1][0], A[-1][1], 14, n=12), (232, 150, 70), peso=0.05, sp=5),
                T(circ(A[-1][0], A[-1][1], 14, n=12), 4, peso=0.1)]
    ops += [T(np.vstack([cuerpo, cuerpo[:1]]), 6, peso=0.6), R(np.vstack([cuerpo, cuerpo[:1]]), BLANCO, peso=0.5, sp=10),
            R(np.array([(-24, -20), (24, -20), (24, 10), (-24, 10), (-24, -20)], float), (232, 120, 100), peso=0.1, sp=6),
            T(np.array([(-24, -20), (24, -20), (24, 10), (-24, 10), (-24, -20)], float), 4, peso=0.1),
            T(casco, 6.4, peso=0.7), R(casco, BLANCO, peso=0.6, sp=10), R(visor, (110, 168, 232), peso=0.4, sp=7), T(visor, 5, peso=0.4)]
    ops += _cara(ojos, boca, ex=15, ye=-112, ym=-96, k=0.75, grueso=8)
    return Dib(ops)


@lru_cache(maxsize=None)
def espejo_lunar():
    P = np.array([(-90, -70), (90, -70), (90, 70), (-90, 70), (-90, -70)], float)
    ops = [T(linea((-60, 70), (-70, 160)), 7, peso=0.1), T(linea((60, 70), (70, 160)), 7, peso=0.1), T(linea((0, 70), (0, 160)), 7, peso=0.1),
           T(P, 6.4, peso=0.7), R(P, (186, 196, 214), peso=0.6, sp=9)]
    for i in range(4):
        for j in range(3):
            c = circ(-63 + i * 42, -42 + j * 42, 15, n=12)
            ops += [R(c, (230, 240, 252), peso=0.05, sp=5), T(c, 3.4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def regla(cm=8, w=34):
    L = cm * w
    P = np.array([(0, -26), (L, -26), (L, 26), (0, 26), (0, -26)], float)
    ops = [R(P, (252, 226, 120), peso=0.5, sp=9), T(P, 5.6, peso=0.6)]
    for k in range(cm + 1):
        ops.append(T(linea((k * w, -26), (k * w, -6 - (6 if k % 2 == 0 else 0))), 3.4, peso=0.03))
    return Dib(ops)


@lru_cache(maxsize=None)
def dedo_una(una=0.0):
    """Dedo vertical (punta arriba) con uña; una = largo extra de la uña que crece (px)."""
    dedo = _tubo([(0, 200), (0, 20)], 70)
    punta = arco_(0, 20, 35, 180, 360, 14)
    cuerpo = np.vstack([np.stack([[-35, 200]]).reshape(1, 2), punta, [(35, 200)]])
    u0, u1 = -10 - una, 12
    nail = np.array([(-22, u1 - 4), (22, u1 - 4), (24, u0 + 20), (0, u0 - 6), (-24, u0 + 20), (-22, u1 - 4)], float)
    return Dib([R(cuerpo, PIEL, peso=0.6, sp=9), T(np.vstack([[(-35, 200)], punta, [(35, 200)]]), 6.4, peso=0.7),
                R(nail, (252, 214, 206), peso=0.1, sp=6), T(nail, 4.4, peso=0.15)])


@lru_cache(maxsize=None)
def reloj_cara(hora=0.0, ojos="grandes", boca="sonrisa", n=24):
    c = circ(0, 0, 100, n=44)
    ops = [T(c, 7, peso=0.7), R(c, (250, 246, 232), peso=0.6, sp=10)]
    for k in range(n):
        a = -pi / 2 + 2 * pi * k / n
        ln = 14 if k % 6 == 0 else 7
        ops.append(T(linea((86 * cos(a), 86 * sin(a)), ((86 - ln) * cos(a), (86 - ln) * sin(a))), 3.6 if k % 6 == 0 else 2.6, peso=0.02))
    ops += _cara(ojos, boca, ex=22, ye=-26, ym=-6, k=0.9, grueso=9)
    a = -pi / 2 + 2 * pi * hora
    ops += [T(linea((0, 0), (62 * cos(a), 62 * sin(a))), 6, peso=0.1), T(circ(0, 0, 6, n=8), 5, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def sol_disco(r=110, corona=0.0):
    c = circ(0, 0, r, n=48)
    ops = []
    if corona > 0:
        for i in range(16):
            a = 2 * pi * i / 16
            r1 = r * (1.55 if i % 2 == 0 else 1.35)
            tri = [((r * 1.02) * cos(a - 0.12), (r * 1.02) * sin(a - 0.12)), (r1 * cos(a), r1 * sin(a)), ((r * 1.02) * cos(a + 0.12), (r * 1.02) * sin(a + 0.12))]
            ops += [R(tri, ORO_OSC, peso=0.05, sp=6), T(linea(*tri), 4, peso=0.05)]
    ops += [R(c, (255, 226, 90), peso=0.5, sp=9), T(c, 6.4, peso=0.6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def disco(r=90, col=(120, 120, 140), borde=7):
    c = circ(0, 0, r, n=44)
    return Dib([R(c, col, peso=0.5, sp=9), T(c, borde, peso=0.6)])


# ================================================================== nube y lluvia
def _nube_poly(circulos, base):
    pts, _ = B.union_circulos(circulos, base, (0.0, 0.0))
    th = np.arctan2(-(pts[:, 1]), pts[:, 0])
    th = np.where(th < -pi / 2, th + 2 * pi, th)
    pts = pts[np.argsort(th)]
    xs = np.linspace(pts[-1, 0], pts[0, 0], 22)
    bl = np.stack([xs, base + 5 * np.sin(xs / 50)], 1)
    return np.vstack([pts, bl, pts[:1]])


@lru_cache(maxsize=None)
def nube(ojos="grandes", boca="sonrisa", gris=False, k=1.0):
    circ_ = [(-170, 40, 80, 100), (-80, -30, 100, -4), (40, -50, 115, -4), (160, 0, 90, 60), (225, 52, 55, 90)]
    P = _nube_poly([tuple(v * k for v in c) for c in circ_], 106 * k)
    col = (178, 186, 204) if gris else (226, 238, 252)
    ops = [T(P, 6.4, peso=1.0), R(P, col, peso=0.9, sp=12)]
    ops += _cara(ojos, boca, ex=34 * k, ye=-6 * k, ym=24 * k, k=1.5 * k, grueso=12) + _mejillas(62 * k, 22 * k, 1.5 * k)
    return Dib(ops)


@lru_cache(maxsize=None)
def gotita(ojos="grandes", boca="sonrisa", k=1.0):
    d = 55.0
    ang = math.degrees(math.acos(40 / d))
    arc = arco_(0, 14, 40, -90 + ang, 270 - ang, 28)
    P = np.vstack([[(0, -66)], arc, [(0, -66)]])
    ops = [R(P, (122, 180, 244), peso=0.3, sp=8), T(P, 5.4, peso=0.5)]
    if ojos:
        ops += _cara(ojos, boca, ex=13, ye=8, ym=26, k=0.55, grueso=7)
    return Dib([(op[0], op[1] * k, *op[2:]) for op in ops])


@lru_cache(maxsize=None)
def elefante(ojos="grandes", boca="sonrisa"):
    gris = (160, 172, 198)
    cont = np.array([(-130, -84), (-176, -72), (-198, -34), (-208, 18), (-228, 70), (-224, 112), (-200, 128), (-184, 104), (-188, 62), (-172, 34), (-150, 44),
                     (-128, 60), (-112, 70), (-108, 130), (-70, 130), (-66, 74), (-34, 76), (-30, 130), (8, 130), (12, 76), (60, 80), (64, 130), (104, 130),
                     (110, 80), (134, 76), (138, 128), (172, 128), (170, 62), (190, 22), (192, -30), (184, -56), (140, -88), (60, -102), (-20, -102),
                     (-80, -96), (-130, -84)], float)
    oreja = elip(-118, -8, 42, 62, rot=0.15, n=26)
    colmillo = np.array([(-178, 40), (-206, 52), (-214, 80), (-198, 66), (-176, 52)], float)
    ops = [R(cont, gris, peso=1.0, sp=10), T(cont, 6.4, peso=1.0),
           R(oreja, (190, 200, 224), peso=0.3, sp=8), T(oreja, 5.4, peso=0.4),
           R(colmillo, (252, 246, 232), peso=0.05, sp=5), T(colmillo, 3.6, peso=0.1),
           T(linea((190, -14), (214, 10), (210, 56)), 6, peso=0.15), R(circ(210, 62, 9, n=8), (110, 120, 150), peso=0.02, sp=4),
           T(linea((-60, 76), (-62, 118)), 3, peso=0.03), T(linea((60, 80), (62, 120)), 3, peso=0.03)]
    ops += _cara(ojos, boca, ex=14, ye=-34, ym=-8, k=0.6, grueso=8)
    ops += [R(elip(-150, -12, 9, 6, n=10), ROSA, peso=0.02, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def flecha_arriba(col=(250, 130, 60), largo=200):
    P = np.array([(-22, 0), (-22, -largo + 50), (-50, -largo + 50), (0, -largo), (50, -largo + 50), (22, -largo + 50), (22, 0), (-22, 0)], float)
    return Dib([R(P, col, peso=0.4, sp=8), T(P, 5.4, peso=0.5)])


@lru_cache(maxsize=None)
def paraguas():
    arc = arco_(0, 0, 150, 180, 360, 24, ry=90)
    sc = []
    for k in range(4):
        x0 = -150 + k * 75
        sc.append(arco_(x0 + 37.5, 0, 37.5, 0, 180, 8, ry=22))
    P = np.vstack([arc, np.vstack(sc[::-1])[::-1] if False else np.vstack([s[::-1] for s in sc[::-1]]), arc[:1]])
    mango = curva([(0, 0), (0, 130), (14, 160), (34, 150)], 8)
    return Dib([T(mango, 8, peso=0.2), R(P, (240, 90, 100), peso=0.6, sp=9), T(P, 6, peso=0.7), T(linea((0, -90), (0, 0)), 4, peso=0.05),
                T(linea((-75, -80), (-50, 0)), 3.6, peso=0.05), T(linea((75, -80), (50, 0)), 3.6, peso=0.05)])


# ================================================================== manos, agua, piel
@lru_cache(maxsize=None)
def mano(arrugas=0, ojos="", boca=""):
    """Mano abierta vista de frente (dedos arriba, ~330 px de alto). arrugas 0/1/2 = yemas lisas / arrugadas / muy arrugadas."""
    palma = curva([(-70, 10), (-60, -40), (60, -40), (70, 10), (62, 110), (30, 150), (-30, 150), (-62, 110)], 8, True)
    ops = []
    fingers = [([(-48, -30), (-58, -100), (-62, -150)], 30), ([(-18, -40), (-20, -120), (-22, -186)], 32), ([(16, -40), (18, -124), (20, -192)], 32),
               ([(46, -34), (54, -108), (58, -156)], 30), ([(-62, 40), (-110, 10), (-134, -30)], 34)]
    for (pts, w) in fingers:
        tubo = _tubo(pts, w, w * 0.88)
        ops += [R(tubo, PIEL, peso=0.3, sp=8), T(tubo, 5.4, peso=0.4)]
    ops += [R(np.vstack([palma, palma[:1]]), PIEL, peso=0.6, sp=10), T(np.vstack([palma, palma[:1]]), 6.2, peso=0.8)]
    tips = [fp[0][-1] for fp in fingers]
    for ti, (x, y) in enumerate(tips):
        w = 13 if ti < 4 else 15
        if arrugas == 0:
            ops.append(T(arco_(x, y + 6, w * 0.6, 30, 150, 6), 2.4, peso=0.02))
        else:
            for k in range(2 + arrugas):
                yy = y + 18 - k * 13
                P = [(x - w * 0.8 + j * w * 1.6 / 7, yy + (1.5 + arrugas) * (-1) ** j) for j in range(8)]
                ops.append(T(curva(P, 4), 2.4, peso=0.05))
    if ojos:
        ops += _cara(ojos, boca, ex=26, ye=40, ym=76, k=1.1, grueso=11) + _mejillas(46, 62, 1.0)
    return Dib(ops)


@lru_cache(maxsize=None)
def neumatico():
    c = circ(0, 0, 96, n=44)
    ops = [R(c, (70, 74, 88), peso=0.8, sp=9), T(c, 7.4, peso=0.8)]
    for k in range(18):
        a = 2 * pi * k / 18
        P = [(80 * cos(a - 0.1), 80 * sin(a - 0.1)), (96 * cos(a - 0.1), 96 * sin(a - 0.1)), (96 * cos(a + 0.1), 96 * sin(a + 0.1)), (80 * cos(a + 0.1), 80 * sin(a + 0.1))]
        ops.append(T(linea(*P), 4, peso=0.04))
    ops += [R(circ(0, 0, 50, n=26), (210, 214, 224), peso=0.3, sp=8), T(circ(0, 0, 50, n=26), 5.4, peso=0.3), T(circ(0, 0, 8, n=8), 5, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def cerebro(ojos="grandes", boca="sonrisa"):
    P = curva([(-100, 10), (-96, -50), (-50, -90), (10, -96), (66, -80), (100, -30), (96, 30), (60, 70), (10, 78), (-50, 72)], 8, True)
    P = np.vstack([P, P[:1]])
    ops = [R(P, (246, 160, 176), peso=0.7, sp=9), T(P, 6.4, peso=0.8)]
    for pts in [[(-70, -40), (-40, -60), (-20, -30), (10, -56)], [(20, -76), (30, -40), (60, -52), (70, -20)], [(-80, 20), (-50, 4), (-30, 30)],
                [(30, 40), (50, 16), (80, 36)], [(-20, 56), (0, 30), (20, 50)]]:
        ops.append(T(curva(pts, 6), 3.6, peso=0.2))
    ops += _cara(ojos, boca, ex=26, ye=-4, ym=26, k=1.1, grueso=10)
    return Dib(ops)


@lru_cache(maxsize=None)
def pez(ojos="grandes", boca="o"):
    cuerpo = elip(0, 0, 100, 56, n=36)
    cola = np.array([(92, 0), (150, -50), (140, 0), (150, 50), (92, 0)], float)
    ops = [R(cola, NARANJA, peso=0.2, sp=7), T(cola, 5.4, peso=0.25), R(cuerpo, (250, 170, 90), peso=0.6, sp=9), T(np.vstack([cuerpo, cuerpo[:1]]), 6.2, peso=0.7)]
    ops += [T(arco_(-30, 0, 54, -50, 50, 8), 3.4, peso=0.1)]
    ops += [T(circ(-58, -10, 12, n=14), 4.6, peso=0.05), T(circ(-58, -10, 2, n=6), 8, peso=0.02)]
    ops.append(T(circ(-92, 12, 7, n=12) if boca == "o" else arco_(-88, 12, 12, 20, 160, 8), 4.4, peso=0.04))
    return Dib(ops)


@lru_cache(maxsize=None)
def roca(ojos=""):
    P = curva([(-90, 40), (-80, -20), (-30, -56), (30, -50), (84, -10), (90, 40)], 8, True)
    P = np.vstack([P, P[:1]])
    ops = [R(P, (150, 154, 170), peso=0.7, sp=9), T(P, 6, peso=0.8), T(curva([(-40, -10), (0, -24), (30, -14)], 6), 3.4, peso=0.1)]
    return Dib(ops)


@lru_cache(maxsize=None)
def ojo(dx=0.0, dy=0.0, color=(96, 150, 240)):
    e = np.vstack([arco_(0, 0, 110, 200, 340, 18, ry=70), arco_(0, 0, 110, 20, 160, 18, ry=70)])
    e = np.vstack([e, e[:1]])
    ops = [T(e, 7, peso=0.8), R(e, (252, 250, 244), peso=0.6, sp=10)]
    ic = circ(dx * 30, dy * 20, 36, n=26)
    ops += [R(ic, color, peso=0.3, sp=7), T(ic, 5, peso=0.3), T(circ(dx * 30, dy * 20, 5, n=8), 18, peso=0.02)]
    for k in range(-3, 4):
        ops.append(T(linea((k * 28, -62 + abs(k) * 6), (k * 34, -84 + abs(k) * 6)), 4, peso=0.03))
    return Dib(ops)


@lru_cache(maxsize=None)
def prisma():
    P = np.array([(0, -110), (100, 60), (-100, 60), (0, -110)], float)
    return Dib([R(P, (200, 230, 250), peso=0.6, sp=9), T(P, 7, peso=0.7), T(linea((-20, -10), (30, 40)), 3, peso=0.05)])


@lru_cache(maxsize=None)
def marte(ojos="grandes", boca="sonrisa"):
    c = circ(0, 0, 90, n=44)
    ops = [R(c, (226, 120, 80), peso=0.5, sp=9), T(c, 6.4, peso=0.6)]
    for (x, y, rr) in [(-50, -44, 14), (46, -50, 10), (54, 30, 16), (-56, 36, 9)]:
        cr = circ(x, y, rr, n=12)
        ops += [R(cr, (190, 90, 60), peso=0.05, sp=5), T(cr, 3.2, peso=0.1)]
    ops += _cara(ojos, boca, ex=24, ye=-8, ym=20, k=1.1, grueso=11) + _mejillas(42, 16, 1.0)
    return Dib(ops)


@lru_cache(maxsize=None)
def cazador(ojos="grandes", boca="sonrisa"):
    """Antepasado peludo: la persona de kit con pelaje (melena y taparrabos) para el cierre de dedos_arrugados."""
    from sh_kit import persona
    return persona(ojos, boca, "tele", (60, 40, 30))


@lru_cache(maxsize=None)
def cuenco():
    P = np.vstack([arco_(0, 0, 150, 0, 180, 24, ry=96), [(150, 0)]])
    borde = elip(0, 0, 156, 20, n=34)
    return Dib([T(np.vstack([P, P[:1]]), 6.4, peso=0.8), R(np.vstack([P, P[:1]]), (214, 120, 90), peso=0.7, sp=10),
                T(arco_(0, 40, 90, 20, 160, 10), 3.6, peso=0.1),
                T(borde, 6, peso=0.5), R(borde, (240, 170, 130), peso=0.2, sp=8)])


@lru_cache(maxsize=None)
def biceps(ojos="", boca=""):
    """Brazo flexionado (músculo) con puño."""
    arm = np.vstack([curva([(-130, 70), (-120, 0), (-70, -50), (-10, -50), (50, -70), (100, -130)], 8),
                     curva([(130, -100), (80, -20), (40, 20), (0, 60), (-40, 80), (-90, 100)], 8)])
    P = np.vstack([arm, arm[:1]])
    bola = circ(-4, -86, 40, n=22)
    puno = elip(112, -142, 40, 34, n=22)
    ops = [R(P, PIEL, peso=0.8, sp=9), T(P, 6.4, peso=0.9), R(puno, PIEL, peso=0.2, sp=7), T(puno, 5.4, peso=0.3), T(linea((92, -128), (130, -128)), 3.4, peso=0.03),
           T(arco_(-10, -60, 44, 200, 340, 10), 3.6, peso=0.1)]
    return Dib(ops)


@lru_cache(maxsize=None)
def bola_k(radiactivo=False):
    c = circ(0, 0, 42, n=28)
    col = (140, 230, 120) if radiactivo else (150, 200, 250)
    return Dib([R(c, col, peso=0.4, sp=8), T(c, 5.4 if not radiactivo else 7, peso=0.5)])


@lru_cache(maxsize=None)
def gafas_eclipse():
    """Gafas de eclipse (cartón con lentes oscuras), centradas en el puente de la nariz."""
    P = np.array([(-86, -26), (86, -26), (86, 26), (-86, 26), (-86, -26)], float)
    l1, l2 = elip(-44, 0, 34, 20, n=20), elip(44, 0, 34, 20, n=20)
    return Dib([R(P, (232, 200, 150), peso=0.3, sp=8), T(P, 5.4, peso=0.3), R(l1, (40, 36, 52), peso=0.2, sp=5), T(l1, 4, peso=0.2),
                R(l2, (40, 36, 52), peso=0.2, sp=5), T(l2, 4, peso=0.2)])


@lru_cache(maxsize=None)
def bola_cara(col=(160, 100, 230), r=80, ojos="grandes", boca="sonrisa"):
    c = circ(0, 0, r, n=36)
    k = r / 80.0
    return Dib([R(c, col, peso=0.5, sp=9), T(c, 6.4, peso=0.6)] + _cara(ojos, boca, ex=24 * k, ye=-8 * k, ym=20 * k, k=1.1 * k, grueso=11) + _mejillas(40 * k, 14 * k, 1.0))
