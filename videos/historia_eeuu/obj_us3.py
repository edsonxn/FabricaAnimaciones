# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de Estados Unidos en 6 minutos» (3/3): OBJETOS, EDIFICIOS y VEHÍCULOS de 1860 a hoy.
Origen en la BASE (y = 0 abajo, x centrado). Vehículos de perfil HACIA LA DERECHA (flip=True para la izquierda);
los animados reciben `pose` 0..3 (ruedas, hélices, humo, oleaje en bucle)."""
import math
from functools import lru_cache

import numpy as np

from obj_base import *  # noqa: F401,F403
from pal_us import *  # noqa: F401,F403

HUMO = (214, 210, 204)
HUMO_OSC = (92, 88, 90)
FUEGO = (240, 140, 52)
FUEGO_CL = (250, 206, 92)
AGUA_US = (92, 150, 196)
COBRE_V = (112, 176, 152)
CEMENTO = (186, 184, 176)
OLIVA_OSC = (92, 100, 64)
CROMO = (206, 212, 220)
CRISTAL = (176, 214, 232)


# ------------------------------------------------------------------ helpers propios
def _rot(P, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    P = np.asarray(P, float)
    return np.stack([cx + (P[:, 0] - cx) * c - (P[:, 1] - cy) * s, cy + (P[:, 0] - cx) * s + (P[:, 1] - cy) * c], 1)


def _rueda(cx, cy, r, pose, col=NEGRO_US, buje=LATON, rayos=6, w=4.6):
    """Rueda con radios que giran 15° por pose (4 poses = 60°: bucle exacto con 6 radios)."""
    ops = forma(circ(cx, cy, r, n=26), col, w, sp=5)
    a0 = math.radians(pose * 60.0 / 4 * (6 / rayos))
    for k in range(rayos):
        a = a0 + 2 * math.pi * k / rayos
        ops += [T(linea((cx, cy), (cx + r * 0.86 * math.cos(a), cy + r * 0.86 * math.sin(a))), 3.0, peso=0.02)]
    ops += forma(circ(cx, cy, r * 0.28, n=12), buje, 3.4, sp=3)
    return ops


def _nube(circulos, col=HUMO, w=3.6):
    """Nube de círculos solapados: relleno de crayón de cada uno y UN solo contorno de tinta por fuera (contorno de la unión)."""
    import cv2
    circulos = [(float(x), float(y), float(r)) for x, y, r in circulos]
    ops = [R(circ(x, y, r, n=20), col, peso=0.02, sp=5) for x, y, r in circulos]
    x0 = min(x - r for x, y, r in circulos) - 4
    y0 = min(y - r for x, y, r in circulos) - 4
    x1 = max(x + r for x, y, r in circulos) + 4
    y1 = max(y + r for x, y, r in circulos) + 4
    k = 2.0
    m = np.zeros((int((y1 - y0) * k) + 2, int((x1 - x0) * k) + 2), np.uint8)
    for x, y, r in circulos:
        cv2.circle(m, (int((x - x0) * k), int((y - y0) * k)), int(r * k), 255, -1)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cs:
        c = c[:, 0, :].astype(float) / k + (x0, y0)
        if len(c) > 6:
            c = c[np.linspace(0, len(c) - 1, min(len(c), 70)).astype(int)]
            ops.append(T(cerrar(c), w, peso=0.04))
    return ops


def _humo(x, y, pose, n=3, col=HUMO, paso=40.0, r0=16.0, dr=8.0, deriva=-0.6):
    """Bocanadas que suben (bucle exacto: cada pose sube paso/4)."""
    cs = []
    for k in range(n):
        h = paso * k + paso * (pose % 4) / 4
        cs.append((x + deriva * h, y - h, r0 + dr * h / paso))
    return _nube(cs, col, 3.2)


def _olas(x0, x1, y, pose, amp=6, lam=46, w=3.6):
    ph = (pose % 4) * math.pi / 2
    return [T(ondas(x0, x1, y, amp, lam, ph), w, peso=0.03), T(ondas(x0 + 20, x1 - 20, y + 16, amp * 0.7, lam * 0.8, -ph), 3.0, peso=0.03)]


def _agua(x0, x1, y0, y1, pose):
    return [R(pol((x0, y0), (x1, y0), (x1, y1), (x0, y1)), AGUA_US, peso=0.04, sp=8)] + _olas(x0, x1, y0, pose)


def _estrella(cx, cy, r, rot=-math.pi / 2):
    P = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = rot + k * math.pi / 5
        P.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pol(*P)


def _destello(x, y, r0=14, r1=32, n=8, w=3.0):
    return [T(linea((x + r0 * math.cos(a), y + r0 * math.sin(a)), (x + r1 * math.cos(a), y + r1 * math.sin(a))), w, peso=0.02)
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def _ventanas(x0, y0, x1, y1, nx, ny, col=CRISTAL, m=0.28, w=2.4):
    ops = []
    dx, dy = (x1 - x0) / nx, (y1 - y0) / ny
    for i in range(nx):
        for j in range(ny):
            a, b = x0 + dx * i + dx * m / 2, y0 + dy * j + dy * m / 2
            P = pol((a, b), (a + dx * (1 - m), b), (a + dx * (1 - m), b + dy * (1 - m)), (a, b + dy * (1 - m)))
            ops += [R(P, col, peso=0.01, sp=3)]
            if w:
                ops += [T(cerrar(P), w, peso=0.01)]
    return ops


def _helice(cx, cy, r, pose, w=5.0):
    """Hélice vista de lado: la pala se acorta y alarga al girar."""
    a = (pose % 4) * math.pi / 4
    L = r * abs(math.cos(a)) + 6
    ops = [T(linea((cx, cy - L), (cx, cy + L)), w, peso=0.03)]
    ops += [T(arco_(cx, cy, r, -60, 60, 10), 2.2, peso=0.02)]
    return ops


# ------------------------------------------------------------------ ferrocarril e industria
@lru_cache(maxsize=None)
def locomotora_us(pose=0):
    """Locomotora de vapor del Oeste (tipo 4-4-0): chimenea de embudo, faro, campana, quitapiedras rojo y humo en bucle."""
    ops = forma(rect(-178, -78, 150, -62, 2), NEGRO_US, 4.4, sp=5)                              # bastidor
    ops += forma(rect(-90, -158, 112, -78, 18), VERDE_US, 5.4, peso=0.5, sp=9)                  # caldera
    ops += forma(pol((112, -158), (124, -150), (124, -86), (112, -78)), LATON, 4.4, sp=4)        # frente de la caldera
    for x in (-50, 10, 70):
        ops += forma(rect(x - 5, -160, x + 5, -76, 2), LATON, 3.2, sp=3)                         # aros de latón
    ops += forma(pol((40, -252), (110, -252), (86, -206), (84, -158), (66, -158), (64, -206)), NEGRO_US, 4.8, sp=6)   # chimenea de embudo
    ops += forma(rect(38, -262, 112, -248, 3), LATON, 3.8, sp=3)
    ops += forma(curva([(-20, -158), (-18, -186), (0, -194), (18, -186), (20, -158)], 4), LATON, 4.0, sp=4)  # domo de vapor
    ops += forma(rect(110, -196, 150, -160, 4), NEGRO_US, 4.2, sp=4) + forma(circ(150, -178, 12, n=12), FUEGO_CL, 3.4, sp=3)  # faro
    ops += forma(rect(-178, -224, -88, -62, 4), ROJO_OSC_US, 5.0, sp=7)                          # cabina
    ops += forma(rect(-188, -238, -78, -222, 4), NEGRO_US, 4.4, sp=5)                            # techo
    ops += forma(rect(-160, -204, -110, -164, 3), CRISTAL, 3.6, sp=3)
    ops += forma(pol((150, -70), (206, -6), (142, -6)), ROJO_US, 4.6, sp=5)                      # quitapiedras
    ops += [rayita(150 + 12 * k, -64, 152 + 12 * k + 16, -8, 2.6) for k in range(3)]
    for x, r in ((-120, 46), (-20, 46)):                                                         # ruedas motrices
        ops += _rueda(x, -48, r, pose, ROJO_US, LATON)
    for x in (70, 124):
        ops += _rueda(x, -28, 26, pose, ROJO_US, LATON)
    a = math.radians(pose * 90)
    pa_, pb = (-120 + 30 * math.cos(a), -48 + 30 * math.sin(a)), (-20 + 30 * math.cos(a), -48 + 30 * math.sin(a))
    ops += [T(linea(pa_, pb), 6.4, peso=0.03), T(linea(pb, (52, -92)), 5.4, peso=0.03)]          # biela
    ops += _humo(70, -284, pose, n=3, col=HUMO, paso=44, r0=18, dr=9, deriva=-0.9)
    return Dib(ops)


@lru_cache(maxsize=None)
def vagon_tren(pose=0):
    """Vagón de pasajeros de madera roja con ventanillas y techo curvo."""
    ops = forma(rect(-176, -186, 176, -60, 6), ROJO_OSC_US, 5.2, peso=0.5, sp=9)
    ops += forma(curva([(-186, -184), (-150, -206), (0, -214), (150, -206), (186, -184)], 6).tolist() + [(186, -180), (-186, -180)], NEGRO_US, 4.6, sp=6)
    ops += forma(rect(-176, -104, 176, -92, 2), LATON, 3.4, sp=3)
    ops += _ventanas(-150, -170, 150, -118, 7, 1, CRISTAL, m=0.34)
    ops += forma(rect(-190, -66, 190, -54, 2), NEGRO_US, 4.0, sp=4)
    for x in (-130, -80, 80, 130):
        ops += _rueda(x, -28, 26, pose, NEGRO_US, ACERO)
    return Dib(ops)


@lru_cache(maxsize=None)
def clavo_oro():
    """El clavo de oro de Promontory (1869) hundido en una traviesa de madera."""
    ops = forma(rect(-150, -46, 150, 0, 6), MADERA_US, 5.0, sp=8)
    ops += [rayita(-130, -30, -40, -32, 2.4), rayita(30, -20, 130, -18, 2.4)]
    ops += forma(rect(-170, -58, 170, -46, 2), ACERO, 4.2, sp=4)                               # riel
    ops += forma(pol((-16, -300), (16, -300), (12, -80), (0, -40), (-12, -80)), ORO_US, 5.0, peso=0.4, sp=6)
    ops += forma(rect(-34, -322, 34, -298, 5), ORO_US, 4.8, sp=5)
    ops += [rayita(-5, -280, -4, -100, 3.0)]
    ops += _destello(48, -300, 10, 30, 8, 3.0) + _destello(-50, -180, 8, 22, 6, 2.6)
    return Dib(ops)


@lru_cache(maxsize=None)
def aceria():
    """Acería: naves de techo en diente de sierra, alto horno, chimeneas humeantes y boca de fuego naranja."""
    ops = []
    for k, (x, h) in enumerate(((-120, 300), (-70, 340), (-20, 300))):                         # chimeneas
        ops += forma(rect(x - 12, -h, x + 12, -150, 2), ROJO_OSC_US, 4.2, sp=4)
        ops += _nube(((x - 8, -h - 22, 18), (x - 26, -h - 50, 24), (x - 50, -h - 70, 20)), HUMO_OSC if k == 1 else HUMO, 3.2)
    saw = [(-180, 0), (-180, -150)]
    for k in range(4):
        x = -180 + 60 * k
        saw += [(x + 40, -190), (x + 60, -150)]
    saw += [(60, 0)]
    ops += forma(saw, GRIS_OSC_US, 5.0, peso=0.5, sp=9)
    ops += _ventanas(-170, -130, 50, -90, 5, 1, (230, 200, 120), m=0.34)
    ops += forma(curva([(-110, 0), (-110, -60), (-80, -78), (-50, -60), (-50, 0)], 5), FUEGO, 4.4, sp=5)   # boca de fuego
    ops += forma(curva([(-96, 0), (-96, -44), (-80, -56), (-64, -44), (-64, 0)], 5), FUEGO_CL, 3.4, sp=4)
    ops += forma(pol((76, 0), (86, -220), (150, -220), (160, 0)), ACERO_OSC, 5.0, sp=8)        # alto horno
    for y in (-60, -120, -180):
        ops += [rayita(80, y, 156, y, 3.0)]
    ops += forma(rect(96, -250, 140, -218, 3), ACERO_OSC, 4.0, sp=4)
    ops += _nube(((118, -262, 16), (126, -290, 22), (140, -316, 18)), HUMO, 3.2) + [R(elip(118, -252, 14, 8, n=12), FUEGO, peso=0.01, sp=2)]
    ops += [T(linea((60, -100), (90, -100)), 6, peso=0.03), R(pol((56, -110), (86, -96), (90, -88), (60, -100)), FUEGO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def viga_acero():
    """Viga de acero en I (con su cara frontal) y remaches."""
    ops = forma(pol((-170, -96), (150, -96), (178, -110), (-142, -110)), ACERO, 4.4, sp=5)    # ala superior vista desde arriba
    ops += forma(rect(-170, -96, 150, -80, 2), ACERO_OSC, 4.4, sp=5)
    ops += forma(rect(-170, -80, 150, -18, 2), ACERO, 4.8, peso=0.4, sp=7)
    ops += forma(rect(-170, -18, 150, 0, 2), ACERO_OSC, 4.4, sp=5)
    # cara del extremo (I)
    ops += forma(pol((150, -96), (178, -110), (178, -94), (166, -88), (166, -24), (178, -18), (178, 0), (150, 0)), ACERO_OSC, 4.2, sp=4)
    for x in range(-150, 150, 34):
        ops += [punto(x, -88, 8), punto(x, -9, 8)]
    return Dib(ops)


@lru_cache(maxsize=None)
def torre_petroleo_us():
    """Torre de perforación de madera (derrick) con un chorro de petróleo negro que brota por arriba."""
    ops = []
    for a, b in (((-100, 0), (-22, -270)), ((100, 0), (22, -270)), ((-60, 0), (-12, -270)), ((60, 0), (12, -270))):
        ops += forma(pol((a[0] - 5, a[1]), (b[0] - 3, b[1]), (b[0] + 3, b[1]), (a[0] + 5, a[1])), MADERA_US, 3.8, sp=3)
    for y0, y1 in ((0, -70), (-70, -140), (-140, -205), (-205, -270)):
        w0, w1 = 100 - 78 * (-y0) / 270, 100 - 78 * (-y1) / 270
        ops += [T(linea((-w0, y0), (w1, y1)), 3.4, peso=0.02), T(linea((w0, y0), (-w1, y1)), 3.4, peso=0.02),
                T(linea((-w1, y1), (w1, y1)), 4.0, peso=0.02)]
    ops += forma(rect(-30, -284, 30, -268, 2), MADERA_OSC_US, 4.0, sp=3)
    chorro = curva([(-10, -284), (-16, -330), (-44, -372), (-90, -380), (-120, -350), (-100, -350), (-70, -360), (-30, -340), (0, -300),
                    (30, -340), (70, -360), (100, -350), (120, -350), (90, -380), (44, -372), (16, -330), (10, -284)], 4)
    ops += forma(chorro, NEGRO_US, 4.6, sp=6)
    for x, y in ((-130, -310), (-112, -270), (130, -310), (110, -260), (-150, -240), (150, -232)):
        ops += forma(elip(x, y, 7, 11, 0, 1.0, 12), NEGRO_US, 2.8, sp=2)
    ops += forma(curva([(-150, 0), (-110, -16), (0, -20), (110, -16), (150, 0)], 5), NEGRO_US, 4.0, sp=5)     # charco
    return Dib(ops)


@lru_cache(maxsize=None)
def barril_petroleo():
    """Barril de petróleo de madera con aros de hierro y un chorreón negro."""
    cuerpo = curva([(-74, -10), (-90, -110), (-74, -210), (74, -210), (90, -110), (74, -10)], 6)
    ops = forma(np.vstack([cuerpo, [(0, 0)]]), MADERA_US, 5.2, peso=0.5, sp=9)
    ops += forma(elip(0, -210, 74, 20, 0, 1.0, 26), MADERA_OSC_US, 4.6, sp=5)
    for y, w in ((-40, 80), (-90, 89), (-130, 89), (-180, 80)):
        ops += forma(rect(-w, y - 6, w, y + 6, 2), NEGRO_US, 3.8, sp=3)
    for x in (-40, 0, 40):
        ops += [rayita(x, -196, x * 1.08, -20, 2.4)]
    ops += forma(curva([(-20, -222), (-30, -200), (-26, -150), (-34, -120), (-20, -126), (-14, -180), (8, -212)], 4), NEGRO_US, 3.6, sp=3)
    ops += forma(elip(0, -214, 50, 10, 0, 1.0, 18), NEGRO_US, 3.2, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def bombilla(f=1.0):
    """La bombilla de Edison: globo de cristal, filamento en herradura, casquillo de rosca y rayos de luz (f = encendido 0..1)."""
    f = max(0.0, min(1.0, float(f)))
    col = tuple(int(round(a + (b - a) * f)) for a, b in zip(CREMA_US, (255, 236, 132)))
    globo = curva([(-36, -110), (-46, -150), (-88, -210), (-92, -270), (-60, -328), (0, -346), (60, -328), (92, -270), (88, -210), (46, -150), (36, -110)], 6)
    ops = []
    if f > 0.05:
        ops += forma(circ(0, -250, 110 + 26 * f, n=30), (255, 244, 186), 0.0, tinta=False, sp=12)
        for k in range(12):
            a = 2 * math.pi * k / 12
            r0, r1 = 118, 128 + 50 * f
            ops += [T(linea((r0 * math.cos(a), -250 + r0 * math.sin(a)), (r1 * math.cos(a), -250 + r1 * math.sin(a))), 4.0, peso=0.02)]
    ops += forma(globo, col, 5.0, peso=0.5, sp=9)
    ops += [T(linea((-14, -112), (-14, -226)), 2.6, peso=0.02), T(linea((14, -112), (14, -226)), 2.6, peso=0.02)]
    fil = arco_(0, -236, 14, 180, 360, 10)
    ops += [T(fil, 3.4 + 1.4 * f, peso=0.02)]
    if f > 0.4:
        ops += [R(elip(0, -242, 22, 12, n=14), FUEGO, peso=0.01, sp=3)]
    ops += forma(rect(-38, -112, 38, -40, 5), ACERO, 4.6, sp=6)
    for y in (-98, -82, -66, -52):
        ops += [T(linea((-40, y), (40, y - 6)), 3.0, peso=0.02)]
    ops += forma(pol((-24, -40), (24, -40), (10, -10), (-10, -10)), NEGRO_US, 4.0, sp=3)
    ops += [T(arco_(-40, -270, 30, 200, 260, 8), 3.6, peso=0.02)]                               # reflejo
    return Dib(ops)


@lru_cache(maxsize=None)
def fonografo():
    """Fonógrafo de bocina: caja de madera, cilindro, brazo y bocina de latón."""
    ops = forma(rect(-140, -90, 70, 0, 6), MADERA_US, 5.0, peso=0.4, sp=8)
    ops += [T(rect(-130, -80, 60, -10, 4), 3.0, peso=0.02)]
    ops += forma(circ(-60, -46, 14, n=12), LATON, 3.4, sp=3)
    ops += forma(rect(-110, -126, -10, -90, 10), NEGRO_US, 4.4, sp=4)                           # cilindro
    for x in range(-100, -14, 14):
        ops += [rayita(x, -122, x, -94, 2.0)]
    ops += [T(linea((-40, -126), (10, -160)), 5.0, peso=0.03)]
    bocina = curva([(4, -150), (60, -190), (120, -250), (150, -320), (190, -280), (170, -240), (90, -190), (20, -150)], 5)
    ops += forma(bocina, LATON, 5.0, peso=0.4, sp=7)
    ops += forma(elip(170, -300, 18, 42, -0.85, 1.0, 22), (176, 128, 52), 4.4, sp=4)
    ops += [T(curva([(30, -158), (100, -212), (150, -280)], 5), 2.6, peso=0.02)]
    # notas musicales
    for x, y in ((200, -360), (240, -320)):
        ops += forma(elip(x, y, 12, 9, -0.4, 1.0, 12), NEGRO_US, 3.0, sp=2) + [T(linea((x + 11, y - 2), (x + 11, y - 46)), 3.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def estatua_libertad():
    """La Estatua de la Libertad (1886): cobre verde, corona de rayos, antorcha encendida y tablilla, sobre su pedestal."""
    ops = forma(trap(-110, 110, -40, -130, 130, 0), (196, 182, 156), 5.0, sp=8)                # base
    ops += forma(trap(-74, 74, -150, -100, 100, -40), (212, 198, 170), 5.0, peso=0.4, sp=8)    # pedestal
    for x in (-50, 0, 50):
        ops += forma(rect(x - 12, -128, x + 12, -66, 3), (186, 170, 142), 3.2, sp=3)
    ops += forma(rect(-84, -162, 84, -148, 2), (196, 182, 156), 4.2, sp=4)
    tunica = curva([(-46, -162), (-50, -230), (-40, -300), (-28, -336), (0, -344), (26, -336), (40, -300), (48, -230), (52, -162)], 6)
    ops += forma(np.vstack([tunica, [(-46, -162)]]), COBRE_V, 5.4, peso=0.6, sp=9)
    for x in (-24, 0, 22):
        ops += [T(curva([(x, -320), (x + 4, -250), (x - 2, -170)], 5), 2.6, peso=0.02)]
    # brazo alzado con antorcha
    ops += forma(pol((18, -330), (40, -340), (66, -432), (50, -436)), COBRE_V, 4.4, sp=5)
    ops += forma(pol((46, -436), (72, -436), (66, -452), (52, -452)), COBRE_V, 4.0, sp=3)
    ops += forma(curva([(48, -452), (52, -486), (62, -500), (70, -484), (72, -452)], 5), FUEGO_CL, 4.0, sp=4)
    ops += [R(elip(60, -470, 7, 14, n=12), FUEGO, peso=0.01, sp=2)]
    # tablilla
    ops += forma(pol((-74, -300), (-44, -312), (-24, -238), (-54, -226)), (128, 186, 162), 4.2, sp=4)
    # cabeza y corona
    ops += forma(circ(0, -364, 22, n=18), COBRE_V, 4.6, sp=5)
    for k in range(7):
        a = math.radians(-160 + k * 23.3)
        x0, y0 = 22 * math.cos(a), -372 + 22 * math.sin(a)
        x1, y1 = 52 * math.cos(a), -372 + 52 * math.sin(a)
        ops += forma(pol((x0 - 4, y0), (x1, y1), (x0 + 4, y0)), COBRE_V, 2.8, sp=2)
    ops += [punto(-8, -366, 6), punto(8, -366, 6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def vapor_inmigrantes(pose=0):
    """Transatlántico de inmigrantes: casco negro con línea roja, cubiertas blancas, tres chimeneas con humo y oleaje."""
    ops = []
    for x in (-60, 10, 80):
        ops += _humo(x - 6, -334, pose, n=2, col=HUMO, paso=40, r0=22, dr=9, deriva=-1.2)
    for x in (-60, 10, 80):
        ops += forma(pol((x - 18, -196), (x - 14, -290), (x + 18, -290), (x + 18, -196)), (222, 132, 60), 4.6, sp=5)
        ops += forma(rect(x - 15, -298, x + 19, -270, 2), NEGRO_US, 3.8, sp=3)
    ops += forma(rect(-130, -196, 130, -160, 3), BLANCO_US, 4.6, sp=6)
    ops += forma(rect(-160, -164, 160, -120, 3), BLANCO_US, 4.8, sp=6)
    ops += _ventanas(-120, -190, 120, -168, 9, 1, CRISTAL, m=0.4, w=1.8)
    casco = [(-200, -122), (212, -126), (190, -60), (170, -30), (-176, -30), (-194, -70)]
    ops += forma(casco, NEGRO_US, 5.4, peso=0.5, sp=9)
    ops += [R(pol((-184, -52), (180, -52), (170, -30), (-176, -30)), ROJO_US, peso=0.02, sp=5)]
    for x in range(-160, 170, 30):
        ops += forma(circ(x, -96, 6, n=10), CRISTAL, 2.4, sp=2)
    ops += [T(linea((-100, -196), (-110, -250)), 3.4, peso=0.02), T(linea((150, -160), (156, -230)), 3.4, peso=0.02)]
    ops += _agua(-230, 240, -36, 0, pose)
    return Dib(ops)


@lru_cache(maxsize=None)
def maleta():
    """Maleta de inmigrante de cuero con correas, esquinas de latón y etiquetas de viaje."""
    ops = forma(rect(-130, -170, 130, 0, 12), CUERO, 5.4, peso=0.5, sp=9)
    ops += [T(arco_(0, -170, 36, 180, 360, 12), 7.0, peso=0.03)]
    for x in (-70, 70):
        ops += forma(rect(x - 12, -172, x + 12, 2, 2), CUERO_OSC, 3.6, sp=3)
        ops += forma(rect(x - 16, -96, x + 16, -80, 2), LATON, 3.2, sp=2)
    for x, y in ((-130, -170), (130, -170), (-130, 0), (130, 0)):
        ops += forma(circ(x - 2 * np.sign(x), y + (10 if y < -1 else -10), 13, n=10), LATON, 3.0, sp=2)
    ops += forma(_rot(rect(-36, -136, 20, -100, 4)[:-1], -0.2, -8, -118), ROJO_US, 3.0, sp=3)
    ops += forma(_rot(rect(10, -60, 56, -24, 10)[:-1], 0.15, 33, -42), AZUL_US, 3.0, sp=3)
    ops += forma(_rot(rect(-50, -54, -10, -22, 4)[:-1], 0.1, -30, -38), CREMA_US, 2.8, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def acorazado_maine(pose=0):
    """El acorazado USS Maine (1898): casco blanco, superestructura ocre, dos chimeneas, mástiles y torretas."""
    ops = forma(rect(-60, -212, -40, -140, 2), (206, 170, 110), 4.2, sp=4) + forma(rect(0, -212, 20, -140, 2), (206, 170, 110), 4.2, sp=4)
    ops += _humo(-52, -252, pose, n=3, col=HUMO, paso=38, r0=20, dr=9, deriva=-1.2)
    ops += [T(linea((-120, -140), (-120, -290)), 4.4, peso=0.03), T(linea((80, -140), (80, -270)), 4.4, peso=0.03),
            T(linea((-144, -260), (-96, -260)), 3.4, peso=0.02), T(linea((60, -240), (100, -240)), 3.4, peso=0.02)]
    ops += forma(rect(-110, -150, 100, -110, 3), (214, 184, 128), 4.6, sp=6)
    ops += _ventanas(-96, -144, 90, -122, 7, 1, NEGRO_US, m=0.5, w=0)
    for x, d in ((-150, -1), (140, 1)):
        ops += forma(elip(x, -110, 30, 18, 0, 1.0, 16), BLANCO_US, 4.2, sp=4)
        ops += [T(linea((x + 20 * d, -114), (x + 76 * d, -122)), 6.0, peso=0.03)]
    casco = [(-210, -110), (220, -114), (200, -40), (-190, -36)]
    ops += forma(casco, BLANCO_US, 5.4, peso=0.5, sp=9)
    ops += [R(pol((-196, -54), (204, -56), (200, -40), (-190, -36)), ROJO_OSC_US, peso=0.02, sp=4)]
    ops += _agua(-240, 250, -40, 0, pose)
    return Dib(ops)


@lru_cache(maxsize=None)
def avion_wright(pose=0):
    """El Flyer de los hermanos Wright (1903): biplano de lona, timón doble atrás, timón de profundidad delante y dos hélices."""
    ops = []
    # timón trasero doble
    ops += forma(rect(-280, -238, -258, -146, 3), CREMA_US, 3.8, sp=3) + forma(rect(-252, -232, -232, -150, 3), CREMA_US, 3.8, sp=3)
    ops += [T(linea((-232, -200), (-140, -230)), 2.8, peso=0.02), T(linea((-232, -170), (-140, -150)), 2.8, peso=0.02)]
    # hélices detrás de las alas
    ops += _helice(-160, -190, 46, pose)
    # alas
    sup = pol((-170, -256), (170, -262), (220, -236), (-120, -230))
    inf = pol((-170, -156), (170, -162), (220, -136), (-120, -130))
    ops += forma(inf, CREMA_US, 4.6, sp=7)
    for x in (-130, -60, 10, 80, 150):
        ops += [T(linea((x, -236 - (x + 170) * 0.017), (x, -136 - (x + 170) * 0.017)), 3.2, peso=0.02)]
        ops += [T(linea((x + 40, -232), (x + 40, -132)), 2.6, peso=0.02)]
    ops += forma(sup, CREMA_US, 4.8, sp=7)
    for x in (-110, -40, 30, 100, 170):
        ops += [rayita(x, -258, x + 34, -232, 2.0)]
    # piloto tumbado sobre el ala inferior
    ops += forma(elip(40, -158, 40, 9, 0, 1.0, 14), NEGRO_US, 3.4, sp=3) + forma(circ(88, -162, 11, n=12), PIEL_A, 3.2, sp=3)
    ops += forma(rect(-10, -176, 20, -160, 2), ACERO_OSC, 3.2, sp=2)                            # motor
    # timón de profundidad delantero (doble)
    ops += [T(linea((200, -186), (270, -210)), 2.8, peso=0.02), T(linea((200, -150), (270, -170)), 2.8, peso=0.02)]
    ops += forma(pol((256, -216), (310, -222), (322, -210), (268, -204)), CREMA_US, 3.6, sp=3)
    ops += forma(pol((256, -186), (310, -192), (322, -180), (268, -174)), CREMA_US, 3.6, sp=3)
    # patines
    ops += [T(curva([(-120, -128), (-60, -40), (120, -36), (250, -50), (290, -80)], 6), 4.0, peso=0.03)]
    for x in (-60, 40, 140):
        ops += [T(linea((x, -132), (x, -40)), 2.6, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def modelo_t(pose=0):
    """Ford Modelo T (1908): negro, alto, radiador de latón, faros, capota y ruedas de radios."""
    ops = forma(pol((-170, -110), (40, -110), (40, -70), (-170, -70)), NEGRO_US, 5.0, sp=7)      # carrocería trasera
    ops += forma(pol((40, -140), (138, -130), (138, -80), (40, -76)), NEGRO_US, 5.0, sp=7)        # capó
    ops += forma(rect(136, -150, 156, -70, 3), LATON, 4.4, sp=4)                                  # radiador
    for y in range(-142, -76, 10):
        ops += [rayita(140, y, 152, y, 1.8)]
    ops += forma(circ(160, -110, 12, n=12), LATON, 3.6, sp=3)                                    # faro
    ops += [T(linea((-160, -110), (-160, -236)), 4.4, peso=0.02), T(linea((20, -110), (20, -236)), 4.4, peso=0.02),
            T(linea((40, -140), (30, -230)), 4.0, peso=0.02)]
    ops += forma(curva([(-176, -226), (-120, -250), (20, -248), (40, -232), (-176, -226)], 5), NEGRO_US, 4.6, sp=5)   # capota
    ops += forma(pol((22, -228), (40, -224), (44, -150), (26, -150)), CRISTAL, 3.4, sp=3)         # parabrisas
    ops += forma(rect(-130, -150, -60, -110, 6), CUERO_OSC, 3.8, sp=4)                            # asiento
    for x in (-110, 110):                                                                         # guardabarros
        ops += [T(arco_(x, -40, 54, 190, 350, 12), 6.0, peso=0.03)]
    ops += [T(linea((-56, -64), (56, -64)), 5.0, peso=0.02)]
    for x in (-110, 110):
        ops += _rueda(x, -40, 40, pose, NEGRO_US, LATON, rayos=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def cadena_montaje():
    """Cadena de montaje: cinta con rodillos, dos chasis de coche en fila, ganchos colgantes y engranajes."""
    ops = [T(linea((-200, -330), (200, -330)), 5.0, peso=0.03)]
    for x in (-120, 0, 120):
        ops += [T(linea((x, -330), (x, -250)), 3.0, peso=0.02), T(arco_(x + 8, -246, 10, 180, 450, 10), 3.0, peso=0.02)]
    ops += forma(rect(-200, -90, 200, -60, 12), GRIS_OSC_US, 4.8, sp=6)
    for x in range(-180, 200, 40):
        ops += forma(circ(x, -75, 11, n=10), ACERO, 2.6, sp=2)
    ops += forma(rect(-180, -60, -170, 0, 2), GRIS_OSC_US, 3.4, sp=2) + forma(rect(170, -60, 180, 0, 2), GRIS_OSC_US, 3.4, sp=2)
    for cx in (-90, 90):
        ops += forma(pol((cx - 70, -130), (cx - 30, -130), (cx - 10, -160), (cx + 40, -160), (cx + 50, -130), (cx + 76, -126), (cx + 76, -96), (cx - 70, -96)),
                     NEGRO_US, 4.4, sp=5)
        ops += forma(circ(cx - 42, -96, 18, n=12), GRIS_OSC_US, 3.6, sp=3) + forma(circ(cx + 46, -96, 18, n=12), GRIS_OSC_US, 3.6, sp=3)
    # engranaje
    P = []
    for k in range(24):
        r = 46 if k % 2 == 0 else 36
        a = 2 * math.pi * k / 24
        P.append((-150 + r * math.cos(a), -200 + r * math.sin(a)))
    ops += forma(P, ACERO, 4.2, sp=4) + forma(circ(-150, -200, 12, n=12), ACERO_OSC, 3.2, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def trompeta():
    """Trompeta de jazz de latón con notas musicales."""
    ops = [T(linea((-170, -100), (60, -100)), 9.0, peso=0.03), R(pol((-170, -104), (60, -104), (60, -96), (-170, -96)), LATON, peso=0.02, sp=3)]
    ops += [T(curva([(-110, -100), (-120, -150), (-60, -160), (40, -156), (64, -124)], 6), 7.0, peso=0.03)]
    ops += forma(pol((60, -110), (150, -140), (176, -150), (176, -50), (150, -60), (60, -90)), LATON, 5.0, peso=0.4, sp=6)
    ops += forma(elip(176, -100, 14, 50, 0, 1.0, 20), (190, 140, 56), 4.4, sp=4)
    for x in (-40, -14, 12):
        ops += forma(rect(x - 8, -142, x + 8, -96, 3), LATON, 3.6, sp=3) + forma(circ(x, -148, 9, n=10), LATON, 3.0, sp=2)
    ops += forma(rect(-190, -108, -166, -92, 3), ACERO, 3.4, sp=2)
    for x, y in ((120, -230), (176, -270), (220, -210)):
        ops += forma(elip(x, y, 13, 9, -0.4, 1.0, 12), NEGRO_US, 3.0, sp=2) + [T(linea((x + 12, y - 2), (x + 12, y - 50)), 3.4, peso=0.02)]
    ops += [T(linea((132, -280), (188, -320)), 5.0, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def urna_voto():
    """Urna de votación de madera con ranura y una papeleta marcada que entra."""
    ops = forma(pol((-120, -200), (120, -200), (150, -230), (-90, -230)), MADERA_OSC_US, 4.4, sp=5)
    ops += forma(rect(-120, -200, 120, 0, 4), MADERA_US, 5.2, peso=0.5, sp=9)
    ops += forma(pol((120, -200), (150, -230), (150, -30), (120, 0)), MADERA_OSC_US, 4.6, sp=6)
    ops += forma(pol((-30, -218), (40, -218), (44, -212), (-26, -212)), NEGRO_US, 3.6, sp=2)
    ops += forma(_rot(rect(-40, -330, 50, -214, 3)[:-1], 0.08, 5, -270), BLANCO_US, 4.0, sp=5)
    ops += [T(linea((-14, -282), (2, -262), (34, -310)), 6.0, peso=0.03)]
    ops += forma(_estrella(0, -110, 40), AZUL_US, 4.0, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def grafico_crash():
    """Gráfica de la bolsa en 1929: sube y se desploma, con una gran flecha roja hacia abajo."""
    ops = forma(rect(-190, -330, 190, 0, 6), CREMA_US, 4.6, sp=8)
    for y in (-260, -190, -120, -50):
        ops += [T(linea((-170, y), (170, y)), 1.8, peso=0.01)]
    ops += [T(linea((-170, -310), (-170, -20), (176, -20)), 4.6, peso=0.03)]
    curva_ = [(-170, -120), (-130, -140), (-100, -130), (-70, -180), (-40, -170), (-10, -240), (20, -230), (40, -290), (60, -200), (80, -150),
              (100, -90), (130, -60), (160, -40)]
    ops += [T(np.asarray(curva_, float), 6.0, peso=0.05)]
    ops += forma(pol((70, -250), (150, -100), (176, -116), (166, -26), (88, -66), (114, -80), (40, -230)), ROJO_US, 4.6, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def fila_pan():
    """Fila del pan en la Gran Depresión: cinco hombres con abrigos y gorras, cabizbajos."""
    ops = []
    cols = ((112, 104, 96), (92, 96, 110), (130, 112, 88), (96, 92, 84), (120, 120, 116))
    for k in range(5):
        x = 150 - 75 * k
        h = 230 + (k % 2) * 14
        ops += forma(pol((x - 34, -h + 70), (x + 34, -h + 70), (x + 40, -20), (x - 40, -20)), cols[k], 4.4, sp=6)
        ops += forma(rect(x - 30, -20, x - 6, 0, 3), NEGRO_US, 3.2, sp=2) + forma(rect(x + 6, -20, x + 30, 0, 3), NEGRO_US, 3.2, sp=2)
        ops += forma(circ(x - 4, -h + 44, 26, n=16), PIEL_A if k % 2 else PIEL_B, 4.0, sp=4)
        ops += forma(pol((x - 30, -h + 30), (x - 24, -h + 14), (x + 20, -h + 14), (x + 26, -h + 30), (x - 46, -h + 34)), GRIS_OSC_US, 3.6, sp=3)
        ops += [punto(x - 13, -h + 44, 5), punto(x + 3, -h + 44, 5)]
        ops += [T(linea((x - 14, -h + 52), (x - 2, -h + 52)), 2.6, peso=0.01)]
        ops += [T(linea((x - 4, -h + 72), (x - 4, -40)), 2.0, peso=0.01)]
    return Dib(ops)


@lru_cache(maxsize=None)
def aguila_new_deal():
    """El águila azul del New Deal (NRA): alas abiertas, engranaje en una garra y rayos en la otra."""
    ops = []
    for lado in (-1, 1):
        ala = [(lado * 20, -230), (lado * 80, -290), (lado * 150, -320), (lado * 190, -300), (lado * 170, -270), (lado * 196, -250),
               (lado * 164, -222), (lado * 180, -200), (lado * 140, -180), (lado * 150, -160), (lado * 100, -160), (lado * 30, -170)]
        ops += forma(ala, AZUL_US, 5.0, peso=0.4, sp=8)
        for k in range(4):
            ops += [T(linea((lado * (60 + 26 * k), -200 - 6 * k), (lado * (110 + 22 * k), -260 - 10 * k)), 2.4, peso=0.02)]
    ops += forma(elip(0, -190, 42, 70, 0, 1.0, 26), AZUL_US, 5.0, sp=7)
    ops += forma(circ(0, -284, 30, n=18), AZUL_US, 4.6, sp=4)
    ops += forma(pol((22, -290), (54, -282), (24, -270)), ORO_US, 3.6, sp=2) + [punto(10, -292, 7)]
    ops += forma(pol((-30, -130), (30, -130), (40, -100), (-40, -100)), AZUL_US, 4.2, sp=4)      # cola
    # engranaje (garra izquierda) y rayos (garra derecha)
    P = []
    for k in range(20):
        r = 44 if k % 2 == 0 else 34
        a = 2 * math.pi * k / 20
        P.append((-70 + r * math.cos(a), -60 + r * math.sin(a)))
    ops += forma(P, ACERO, 4.2, sp=4) + forma(circ(-70, -60, 12, n=10), CREMA_US, 3.0, sp=2)
    for k in range(3):
        dx = 50 + 26 * k
        ops += forma(pol((dx, -110), (dx + 20, -72), (dx + 6, -72), (dx + 26, -20), (dx - 8, -68), (dx + 6, -68), (dx - 6, -106)), ROJO_US, 3.4, sp=3)
    ops += [T(linea((-24, -128), (-60, -100)), 4.0, peso=0.02), T(linea((24, -128), (70, -106)), 4.0, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def avion_caza(pose=0):
    """Caza de hélice de la Segunda Guerra Mundial (tipo P-51) con la estrella blanca en el fuselaje."""
    ops = forma(pol((-200, -170), (-176, -250), (-150, -250), (-140, -176)), ACERO, 4.4, sp=4)  # deriva
    fus = curva([(-200, -168), (-120, -184), (0, -196), (120, -196), (176, -186), (190, -170), (176, -154), (120, -146), (0, -144),
                 (-120, -150), (-200, -160)], 6)
    ops += forma(fus, ACERO, 5.2, peso=0.5, sp=9)
    ops += forma(pol((-210, -168), (-150, -172), (-150, -160), (-210, -158)), ACERO_OSC, 3.6, sp=3)     # estabilizador
    ops += forma(curva([(10, -196), (24, -226), (70, -230), (96, -198)], 5).tolist() + [(10, -196)], CRISTAL, 4.0, sp=4)  # cabina
    ops += forma(pol((-40, -150), (90, -150), (60, -120), (-60, -124)), ACERO_OSC, 4.4, sp=5)        # ala
    ops += forma(curva([(-30, -146), (10, -126), (40, -146)], 4).tolist() + [(-30, -146)], ACERO_OSC, 3.4, sp=3)
    ops += forma(circ(-70, -170, 20, n=16), AZUL_US, 3.6, sp=3) + forma(_estrella(-70, -170, 16), BLANCO_US, 2.4, sp=2)
    ops += forma(curva([(176, -186), (204, -178), (210, -170), (204, -162), (176, -154)], 4), ROJO_US, 3.8, sp=3)   # cono
    ops += _helice(212, -170, 54, pose, w=6.0)
    ops += [T(linea((40, -120), (34, -60)), 3.6, peso=0.02), T(linea((-20, -122), (-26, -60)), 3.6, peso=0.02)]   # tren
    ops += forma(circ(34, -48, 14, n=12), NEGRO_US, 3.4, sp=2) + forma(circ(-26, -48, 14, n=12), NEGRO_US, 3.4, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def acorazado_arizona(pose=0):
    """Acorazado gris en llamas en Pearl Harbor: mástiles trípode, torretas, humo negro y fuego."""
    ops = []
    ops += _nube([(-10 - 1.4 * h, -250 - h, 30 + 0.5 * h) for h in (40 * k + 10 * (pose % 4) for k in range(3))] + [(-10, -220, 26)], HUMO_OSC, 3.6)
    for x in (-80, 60):
        ops += [T(linea((x - 20, -150), (x, -280)), 3.8, peso=0.02), T(linea((x + 20, -150), (x, -280)), 3.8, peso=0.02),
                T(linea((x, -150), (x, -280)), 3.8, peso=0.02)]
        ops += forma(rect(x - 22, -300, x + 22, -276, 3), GRIS_OSC_US, 3.8, sp=3)
    ops += forma(rect(-110, -170, 100, -120, 3), GRIS_OSC_US, 4.6, sp=6)
    ops += forma(rect(-30, -210, 0, -168, 2), GRIS_OSC_US, 4.0, sp=3)
    for x, d in ((-170, -1), (-125, -1), (130, 1), (175, 1)):
        ops += forma(rect(x - 22, -136, x + 22, -112, 4), ACERO_OSC, 4.0, sp=3)
        ops += [T(linea((x + 18 * d, -126), (x + 64 * d, -132)), 5.0, peso=0.02)]
    casco = [(-230, -116), (226, -120), (200, -50), (-210, -46)]
    ops += forma(casco, ACERO_OSC, 5.4, peso=0.5, sp=9)
    for x, s in ((-40, 1.0), (40, 0.8), (110, 0.6)):
        ops += forma(curva([(x - 34 * s, -120), (x - 20 * s, -170 - (pose % 2) * 10), (x - 4 * s, -150), (x + 6 * s, -200 + (pose % 2) * 8),
                            (x + 22 * s, -150), (x + 34 * s, -120)], 4), FUEGO, 3.8, sp=4)
        ops += [R(elip(x, -132, 14 * s, 14, n=12), FUEGO_CL, peso=0.01, sp=2)]
    ops += _agua(-250, 250, -56, 0, pose)
    return Dib(ops)


@lru_cache(maxsize=None)
def lancha_desembarco(pose=0):
    """Lancha de desembarco Higgins (Normandía): caja gris con rampa delantera, cascos de soldados y salpicaduras."""
    ops = []
    for k in range(5):
        x = -90 + 40 * k
        ops += forma(arco_(x, -140, 20, 180, 360, 10).tolist() + [(x - 20, -140)], VERDE_OLIVA, 3.6, sp=2)
    ops += forma(pol((-170, -140), (130, -140), (130, -60), (-160, -50)), ACERO, 5.2, peso=0.5, sp=8)
    ops += forma(pol((130, -150), (176, -130), (176, -54), (130, -60)), ACERO_OSC, 4.6, sp=5)   # rampa
    ops += [rayita(140, -130, 168, -120, 2.6), rayita(140, -100, 168, -92, 2.6)]
    ops += forma(rect(-170, -170, -130, -140, 3), ACERO_OSC, 3.8, sp=3)
    ops += [T(linea((-150, -170), (-150, -210)), 3.4, peso=0.02)]
    ops += forma(pol((-150, -210), (-110, -202), (-150, -192)), AZUL_US, 2.8, sp=2)
    a = (pose % 4) * math.pi / 2
    for k in range(4):
        x = 180 + 16 * k
        ops += forma(circ(x, -70 - 18 * abs(math.sin(a + k)), 9 + 3 * k, n=10), (214, 232, 240), 2.8, sp=2)
    ops += _agua(-210, 230, -56, 0, pose)
    return Dib(ops)


@lru_cache(maxsize=None)
def hongo_atomico():
    """Hongo atómico: columna, sombrero de nubes con brillo naranja dentro y anillo de condensación."""
    ops = forma(curva([(-200, 0), (-150, -40), (-60, -56), (60, -56), (150, -40), (200, 0)], 6), (170, 156, 140), 4.6, sp=7)
    ops += forma(curva([(-40, -50), (-30, -160), (-46, -230), (46, -230), (30, -160), (40, -50)], 6), (196, 186, 176), 5.0, sp=8)
    for y in (-110, -170):
        ops += [T(arco_(0, y, 36, 200, 340, 10), 2.6, peso=0.02)]
    circulos = ((-110, -280, 56), (-50, -310, 66), (30, -316, 70), (104, -286, 58), (0, -262, 64), (-150, -250, 40), (150, -256, 40))
    ops += _nube(circulos, (214, 204, 192), 4.4)
    ops += [R(elip(0, -270, 90, 34, n=22), FUEGO, peso=0.03, sp=5), R(elip(0, -270, 50, 18, n=18), FUEGO_CL, peso=0.02, sp=4)]
    ops += forma(elip(0, -200, 110, 16, 0, 1.0, 26), (230, 224, 216), 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def misil_nuclear():
    """Misil balístico de la Guerra Fría en su rampa: cuerpo blanco con anillos negros, cono rojo y aletas."""
    ops = forma(rect(-110, -40, 110, 0, 4), GRIS_OSC_US, 4.6, sp=6)
    ops += [T(linea((-80, -40), (-50, -300)), 3.6, peso=0.02), T(linea((80, -40), (50, -300)), 3.6, peso=0.02)]
    for y in (-100, -180, -260):
        ops += [T(linea((-80 + (-y - 40) * 0.115, y), (80 - (-y - 40) * 0.115, y)), 2.6, peso=0.02)]
    ops += forma(rect(-30, -330, 30, -50, 8), BLANCO_US, 5.2, peso=0.5, sp=8)
    ops += forma(curva([(-30, -330), (-24, -370), (0, -404), (24, -370), (30, -330)], 6), ROJO_US, 4.8, sp=5)
    for y in (-110, -200, -290):
        ops += forma(rect(-30, y - 10, 30, y + 10, 2), NEGRO_US, 3.6, sp=3)
    for lado in (-1, 1):
        ops += forma(pol((lado * 30, -110), (lado * 66, -54), (lado * 30, -54)), NEGRO_US, 4.0, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def sputnik():
    """El Sputnik (1957): esfera metálica pulida con cuatro antenas largas hacia atrás."""
    ops = []
    for a, L in ((150, 320), (162, 300), (198, 300), (210, 320)):
        r = math.radians(a)
        ops += [T(linea((60 * math.cos(r) + 120, -180 + 60 * math.sin(r) * 0.4), (120 + L * math.cos(r), -180 + L * math.sin(r) * 0.42)), 3.8, peso=0.03)]
    ops += forma(circ(120, -180, 66, n=30), CROMO, 5.2, peso=0.5, sp=8)
    ops += [T(arco_(120, -180, 66, 90, 270, 12, ry=22), 2.6, peso=0.02)]
    ops += [R(elip(96, -206, 20, 12, -0.5, 1.0, 12), BLANCO_US, peso=0.01, sp=2)]
    ops += forma(circ(52, -180, 8, n=10), ACERO_OSC, 2.6, sp=2)
    for x, y in ((-160, -320), (-100, -60), (200, -320), (230, -60), (-200, -170)):
        ops += _destello(x, y, 3, 14, 4, 2.4)
    return Dib(ops)


@lru_cache(maxsize=None)
def cohete_saturno():
    """Cohete Saturno V (Apolo 11): fases blancas con bandas negras, aletas, torre de escape y llamarada."""
    ops = []
    ops += forma(curva([(-50, -96), (-70, -50), (-40, 0), (0, -30), (40, 0), (70, -50), (50, -96)], 5), FUEGO, 4.4, sp=5)
    ops += forma(curva([(-28, -96), (-30, -60), (0, -34), (30, -60), (28, -96)], 4), FUEGO_CL, 3.4, sp=3)
    ops += forma(rect(-40, -260, 40, -96, 3), BLANCO_US, 5.2, peso=0.5, sp=8)                   # primera fase
    ops += forma(rect(-40, -150, 0, -120, 2), NEGRO_US, 3.0, sp=2) + forma(rect(0, -230, 40, -200, 2), NEGRO_US, 3.0, sp=2)
    for lado in (-1, 1):
        ops += forma(pol((lado * 40, -136), (lado * 64, -96), (lado * 40, -96)), NEGRO_US, 3.6, sp=3)
    ops += forma(rect(-40, -276, 40, -260, 2), NEGRO_US, 3.6, sp=2)
    ops += forma(rect(-38, -380, 38, -276, 3), BLANCO_US, 5.0, sp=7)                            # segunda fase
    ops += forma(trap(-26, 26, -410, -38, 38, -380), BLANCO_US, 4.4, sp=5)
    ops += forma(rect(-26, -470, 26, -410, 3), BLANCO_US, 4.6, sp=5)                            # tercera fase
    ops += forma(rect(-26, -440, 26, -428, 2), NEGRO_US, 3.0, sp=2)
    ops += forma(pol((-18, -470), (18, -470), (0, -500)), ACERO, 4.0, sp=3)                     # módulo de mando
    ops += [T(linea((0, -500), (0, -540)), 3.4, peso=0.02), T(linea((-8, -506), (8, -530)), 2.6, peso=0.02),
            T(linea((8, -506), (-8, -530)), 2.6, peso=0.02)]
    ops += forma(rect(-30, -330, 30, -318, 2), (200, 60, 56), 2.8, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def modulo_lunar():
    """Módulo lunar del Apolo: etapa de descenso dorada, cuatro patas con platos y etapa de ascenso gris con ventana."""
    ops = []
    for lado in (-1, 1):
        ops += [T(linea((lado * 70, -110), (lado * 150, -20)), 5.0, peso=0.03), T(linea((lado * 40, -80), (lado * 150, -20)), 3.4, peso=0.02)]
        ops += forma(elip(lado * 152, -12, 30, 10, 0, 1.0, 16), ACERO, 3.6, sp=3)
    ops += [T(linea((0, -96), (0, -20)), 4.0, peso=0.02)] + forma(elip(0, -12, 26, 8, 0, 1.0, 14), ACERO, 3.2, sp=2)
    ops += forma(pol((-90, -190), (90, -190), (100, -96), (-100, -96)), ORO_US, 5.2, peso=0.5, sp=8)
    for x in (-60, -20, 20, 60):
        ops += [T(curva([(x, -188), (x + 6, -150), (x - 4, -100)], 4), 2.2, peso=0.01)]
    ops += forma(pol((-80, -190), (-70, -270), (-30, -300), (50, -300), (80, -260), (80, -190)), ACERO, 5.0, sp=8)
    ops += forma(pol((-50, -268), (-20, -284), (-20, -240)), NEGRO_US, 3.4, sp=2)
    ops += forma(rect(-16, -232, 16, -192, 2), ACERO_OSC, 3.4, sp=2)
    ops += [T(linea((50, -300), (80, -340)), 3.4, peso=0.02)] + forma(arco_(90, -350, 26, 120, 300, 10).tolist() + [(90, -350)], BLANCO_US, 3.2, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def luna():
    """La Luna: disco gris con mares oscuros y cráteres."""
    ops = forma(circ(0, -170, 168, n=48), (204, 202, 196), 5.4, peso=0.6, sp=10)
    for cx, cy, rx, ry in ((-50, -230, 60, 40), (40, -150, 50, 36), (-60, -110, 34, 26), (70, -250, 30, 22)):
        ops += [R(elip(cx, cy, rx, ry, 0.3, 1.0, 20), (158, 156, 152), peso=0.03, sp=5)]
    for cx, cy, r in ((-100, -170, 18), (90, -90, 22), (0, -60, 14), (110, -200, 12), (-20, -290, 16), (30, -220, 10), (-110, -260, 10)):
        ops += [T(circ(cx, cy, r, n=16), 3.0, peso=0.02), R(arco_(cx, cy, r, 200, 340, 8), (150, 148, 144), peso=0.01, sp=2)]
    return Dib(ops)


@lru_cache(maxsize=None)
def huella_bota():
    """La huella de la bota de Armstrong en el polvo lunar (vista desde arriba)."""
    ops = forma(elip(0, -150, 180, 130, 0, 1.0, 36), (196, 194, 188), 3.6, sp=10)
    for x, y in ((-140, -100), (120, -230), (150, -90), (-120, -230)):
        ops += [T(circ(x, y, 10, n=12), 2.4, peso=0.01)]
    suela = curva([(-46, -40), (-56, -120), (-54, -200), (-40, -260), (0, -280), (40, -262), (54, -200), (50, -130), (40, -60), (20, -30),
                   (-20, -28)], 6, cerrado=True)
    ops += forma(suela, (150, 148, 142), 5.0, peso=0.5, sp=7)
    for k in range(10):
        y = -60 - 21 * k
        w = 40 if 1 < k < 9 else 30
        ops += [T(linea((-w, y), (w, y)), 4.6, peso=0.02)]
    ops += [T(linea((-44, -140), (44, -140)), 6.0, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def helicoptero_huey(pose=0):
    """Helicóptero UH-1 «Huey» de Vietnam: verde oliva, cola larga, rotor principal y de cola en bucle, patines."""
    a = (pose % 4) * math.pi / 4
    L = 60 + 170 * abs(math.cos(a))
    ops = forma(pol((-220, -180), (-60, -170), (-60, -150), (-210, -166)), OLIVA_OSC, 4.4, sp=5)     # cola
    ops += forma(pol((-226, -220), (-206, -220), (-196, -166), (-218, -166)), OLIVA_OSC, 4.0, sp=3)
    ops += _helice(-226, -200, 30, pose + 1, w=4.0)
    cuerpo = curva([(-70, -200), (40, -210), (110, -186), (130, -140), (100, -108), (-60, -104), (-80, -150)], 6, cerrado=True)
    ops += forma(cuerpo, VERDE_OLIVA, 5.2, peso=0.5, sp=9)
    ops += forma(curva([(52, -200), (110, -180), (124, -144), (64, -146)], 5).tolist() + [(52, -200)], CRISTAL, 4.0, sp=4)
    ops += forma(rect(-30, -180, 30, -118, 3), OLIVA_OSC, 3.6, sp=3)
    ops += forma(rect(-30, -226, 40, -206, 4), OLIVA_OSC, 4.0, sp=3)
    ops += [T(linea((4, -226), (4, -250)), 5.0, peso=0.02), T(linea((4 - L, -252), (4 + L, -248)), 6.0, peso=0.03)]
    ops += [T(linea((-50, -104), (-60, -70)), 4.0, peso=0.02), T(linea((70, -106), (80, -70)), 4.0, peso=0.02),
            T(curva([(-100, -70), (100, -70), (130, -84)], 4), 5.0, peso=0.02)]
    ops += forma(_estrella(-120, -168, 12), BLANCO_US, 2.4, sp=2)
    return Dib(ops)


def _ola_pt(x, y, x0=0.0, amp=9.0):
    return (x, y + amp * math.sin((x - x0) / 46.0) * min(1.0, (x - x0) / 60.0))


@lru_cache(maxsize=None)
def bandera_eeuu():
    """Bandera de Estados Unidos ondeando en su asta: 13 franjas y 50 estrellas."""
    x0, x1, y0, h = -116, 150, -370, 150
    ops = forma(rect(-132, -392, -116, 0, 4), MADERA_US, 4.4, sp=3) + forma(circ(-124, -398, 11, n=12), LATON, 3.2, sp=2)
    xs = np.linspace(x0, x1, 16)
    for k in range(13):
        ya, yb = y0 + h * k / 13, y0 + h * (k + 1) / 13
        P = [_ola_pt(x, ya, x0) for x in xs] + [_ola_pt(x, yb, x0) for x in xs[::-1]]
        ops += [R(pol(*P), ROJO_US if k % 2 == 0 else BLANCO_US, peso=0.01, sp=4)]
    cx1 = x0 + (x1 - x0) * 0.42
    xs2 = np.linspace(x0, cx1, 8)
    yc = y0 + h * 7 / 13
    P = [_ola_pt(x, y0, x0) for x in xs2] + [_ola_pt(x, yc, x0) for x in xs2[::-1]]
    ops += [R(pol(*P), AZUL_US, peso=0.02, sp=4)]
    for j in range(9):
        n = 6 if j % 2 == 0 else 5
        for i in range(n):
            x = x0 + 9 + (i + (0.5 if n == 5 else 0)) * (cx1 - x0 - 18) / 5.5
            px, py = _ola_pt(x, y0 + 7 + j * (yc - y0 - 12) / 8.6, x0)
            ops += [R(circ(px, py, 2.6, n=6), BLANCO_US, peso=0.003, sp=1.2)]
    borde = [_ola_pt(x, y0, x0) for x in xs] + [_ola_pt(x, y0 + h, x0) for x in xs[::-1]]
    ops += [T(cerrar(pol(*borde)), 4.4, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera_urss():
    """Bandera de la Unión Soviética ondeando: roja con la hoz y el martillo dorados y la estrella."""
    x0, x1, y0, h = -116, 150, -370, 160
    ops = forma(rect(-132, -392, -116, 0, 4), MADERA_US, 4.4, sp=3) + forma(circ(-124, -398, 11, n=12), LATON, 3.2, sp=2)
    xs = np.linspace(x0, x1, 16)
    borde = [_ola_pt(x, y0, x0) for x in xs] + [_ola_pt(x, y0 + h, x0) for x in xs[::-1]]
    ops += forma(pol(*borde), ROJO_US, 4.4, sp=6)
    cx, cy = -66, -310
    ops += [T(arco_(cx + 4, cy, 24, 200, 470, 14), 5.0, peso=0.02), R(arco_(cx + 4, cy, 24, 200, 470, 14), ORO_US, peso=0.01, sp=1)]
    ops += [T(linea((cx - 16, cy + 22), (cx + 18, cy - 14)), 6.0, peso=0.02), T(linea((cx + 10, cy - 24), (cx + 28, cy - 4)), 7.0, peso=0.02)]
    ops += [T(cerrar(_estrella(cx + 2, cy - 44, 11)), 2.4, peso=0.01)]
    return Dib(ops)


# letras de bloque para el letrero de Hollywood (rejilla de 3×5)
_GLIFOS = {
    "H": ((0, 0, 1, 5), (2, 0, 3, 5), (1, 2, 2, 3)),
    "O": ((0, 0, 3, 1), (0, 4, 3, 5), (0, 0, 1, 5), (2, 0, 3, 5)),
    "L": ((0, 0, 1, 5), (0, 4, 3, 5)),
    "Y": (((0, 0), (1, 0), (1.5, 1.7), (2, 0), (3, 0), (2, 2.7), (2, 5), (1, 5), (1, 2.7)),),
    "W": ((0, 0, 0.8, 5), (1.1, 2, 1.9, 5), (2.2, 0, 3, 5), (0, 4.2, 3, 5)),
    "D": ((0, 0, 1, 5), (0, 0, 2.2, 1), (0, 4, 2.2, 5), (2, 0.7, 3, 4.3)),
}


@lru_cache(maxsize=None)
def letrero_hollywood():
    """Colinas de Hollywood con el letrero de letras blancas."""
    ops = forma(curva([(-215, 0), (-196, -90), (-120, -170), (0, -196), (120, -178), (196, -100), (220, 0)], 6), (150, 136, 92), 5.0, sp=9)
    ops += [R(curva([(-150, -30), (-80, -80), (30, -96), (150, -60), (180, -20)], 5), (122, 132, 82), peso=0.03, sp=6)]
    for x, y in ((-170, -14), (-90, -18), (40, -16), (170, -12)):
        ops += forma(circ(x, y, 12, n=12), VERDE_US, 2.8, sp=3)
    u = 10.0
    for i, ch in enumerate("HOLLYWOOD"):
        bx = -170 + i * 38
        by = -36 - 50 * math.sin(math.pi * (i + 0.5) / 9)
        for g in _GLIFOS[ch]:
            if isinstance(g[0], tuple):
                P = cerrar([(bx + gx * u, by - 64 + gy * u * 1.16) for gx, gy in g])
            else:
                a, b, c, d = g
                P = rect(bx + a * u, by - 64 + b * u * 1.16, bx + c * u, by - 64 + d * u * 1.16, 0.5, 2)
            ops += [R(P, BLANCO_US, peso=0.004, sp=1.5), T(P, 1.8, peso=0.004)]
    return Dib(ops)


@lru_cache(maxsize=None)
def guitarra_electrica():
    """Guitarra eléctrica roja de rock and roll con golpeador blanco, pastillas, mástil y clavijero."""
    cuerpo = curva([(-30, -150), (-60, -170), (-92, -150), (-96, -100), (-80, -60), (-100, -20), (-80, 10), (0, 18), (80, 10), (100, -24),
                    (84, -70), (100, -130), (82, -168), (54, -160), (30, -150)], 6, cerrado=True)
    ops = forma(rect(-14, -400, 14, -130, 4), MADERA_US, 4.6, sp=5)
    for y in range(-380, -140, 26):
        ops += [rayita(-14, y, 14, y, 1.8)]
    ops += forma(pol((-18, -400), (18, -400), (24, -460), (-10, -470)), MADERA_OSC_US, 4.4, sp=4)
    for k in range(3):
        ops += forma(circ(-20, -414 - 18 * k, 5, n=8), CROMO, 2.4, sp=1) + forma(circ(26, -418 - 18 * k, 5, n=8), CROMO, 2.4, sp=1)
    ops += forma(cuerpo, ROJO_US, 5.4, peso=0.5, sp=9)
    ops += forma(curva([(-40, -150), (-70, -140), (-74, -96), (-50, -50), (-60, -10), (20, -6), (60, -50), (40, -110), (20, -150)], 5, cerrado=True),
                 BLANCO_US, 3.8, sp=5)
    for y in (-120, -90, -60):
        ops += forma(rect(-24, y - 8, 24, y + 8, 3), NEGRO_US, 3.0, sp=2)
    ops += forma(rect(-20, -30, 20, -18, 2), CROMO, 2.8, sp=1)
    for x in (-9, -4.5, 0, 4.5, 9):
        ops += [T(linea((x, -400), (x, -24)), 1.2, peso=0.01)]
    ops += forma(circ(56, -40, 8, n=10), CROMO, 2.6, sp=1) + forma(circ(66, -14, 8, n=10), CROMO, 2.6, sp=1)
    return Dib(ops)


@lru_cache(maxsize=None)
def disco_vinilo():
    """Disco de vinilo negro con surcos y etiqueta roja."""
    ops = forma(circ(0, -160, 160, n=48), NEGRO_US, 5.2, peso=0.5, sp=9)
    for r in (140, 122, 104, 86, 70):
        ops += [T(arco_(0, -160, r, 10, 340, 26), 1.4, peso=0.01, v=200)]
    ops += forma(circ(0, -160, 52, n=24), ROJO_US, 4.0, sp=4)
    ops += [T(linea((-30, -176), (30, -176)), 2.0, peso=0.01), T(linea((-24, -144), (24, -144)), 2.0, peso=0.01)]
    ops += forma(circ(0, -160, 7, n=10), CREMA_US, 2.6, sp=1)
    ops += [T(arco_(0, -160, 120, 210, 250, 8), 4.0, peso=0.01, v=120)]
    return Dib(ops)


@lru_cache(maxsize=None)
def autobus_montgomery():
    """Autobús urbano de los años 50 (Montgomery, 1955): verde abajo, crema arriba, ventanillas y puerta delantera."""
    ops = forma(curva([(-200, -40), (-204, -170), (-180, -200), (170, -204), (204, -170), (210, -40)], 6).tolist() + [(-200, -40)],
                (226, 214, 160), 5.4, peso=0.5, sp=9)
    ops += [R(pol((-202, -110), (208, -110), (210, -40), (-200, -40)), (92, 150, 102), peso=0.02, sp=6)]
    ops += [T(linea((-202, -110), (208, -110)), 3.6, peso=0.02)]
    ops += _ventanas(-180, -184, 120, -124, 6, 1, CRISTAL, m=0.18)
    ops += forma(rect(140, -186, 196, -50, 3), CRISTAL, 4.0, sp=4)
    ops += [T(linea((168, -186), (168, -50)), 2.6, peso=0.02)]
    ops += forma(rect(196, -78, 214, -56, 2), CROMO, 3.0, sp=2)
    ops += forma(circ(206, -96, 9, n=10), (250, 220, 120), 2.6, sp=1)
    ops += forma(rect(-210, -52, 214, -36, 3), CROMO, 3.4, sp=3)
    for x in (-130, 130):
        ops += forma(circ(x, -36, 34, n=22), NEGRO_US, 4.6, sp=4) + forma(circ(x, -36, 13, n=12), CROMO, 3.0, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def microfono_antiguo():
    """Micrófono de los años 60 en pie (discursos de la marcha sobre Washington)."""
    ops = forma(elip(0, -10, 90, 18, 0, 1.0, 24), NEGRO_US, 4.4, sp=5)
    ops += forma(rect(-7, -270, 7, -14, 3), CROMO, 4.0, sp=3)
    ops += [T(linea((0, -270), (24, -290)), 5.0, peso=0.02)]
    cab = curva([(-24, -296), (-42, -330), (-40, -370), (0, -392), (40, -370), (42, -330), (24, -296)], 6, cerrado=True)
    ops += forma(_rot(cab, 0.25, 0, -340), CROMO, 5.0, peso=0.4, sp=7)
    for k in range(5):
        y = -360 + 14 * k
        ops += [T(_rot(linea((-30, y), (30, y)), 0.25, 0, -340), 2.0, peso=0.01)]
    ops += [T(curva([(0, -20), (60, -10), (120, -30), (180, -20)], 6), 3.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def monumento_lincoln():
    """Monumento a Lincoln: templo griego blanco con escalinata, columnata y la estatua sentada en sombra."""
    ops = forma(rect(-190, -40, 190, 0, 2), (226, 222, 210), 4.6, sp=6)
    ops += forma(rect(-170, -64, 170, -40, 2), (236, 232, 220), 4.4, sp=6)
    ops += [rayita(-190, -20, 190, -20, 2.2)]
    ops += forma(rect(-150, -206, 150, -64, 2), (180, 176, 168), 4.6, sp=7)
    ops += forma(curva([(-30, -64), (-34, -120), (-20, -140), (20, -140), (34, -120), (30, -64)], 5), (236, 232, 222), 3.6, sp=4)
    ops += forma(circ(0, -156, 14, n=12), (236, 232, 222), 3.0, sp=2)
    for k in range(10):
        x = -150 + 300 * k / 9
        if abs(x) < 30:
            continue
        ops += forma(rect(x - 11, -206, x + 11, -64, 2), (244, 240, 230), 3.6, sp=4)
        ops += [rayita(x - 4, -200, x - 4, -70, 1.6)]
    ops += forma(rect(-170, -236, 170, -206, 2), (240, 236, 226), 4.6, sp=5)
    ops += forma(rect(-150, -266, 150, -236, 2), (232, 228, 218), 4.4, sp=5)
    for k in range(12):
        ops += [punto(-140 + 280 * k / 11, -222, 6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def trozo_muro_berlin():
    """Trozo del Muro de Berlín (1989): losa de hormigón con remate redondo, grafitis de colores y grietas."""
    ops = forma(pol((-140, 0), (-140, -300), (-120, -330), (120, -330), (140, -300), (140, 0)), CEMENTO, 5.4, peso=0.5, sp=9)
    ops += forma(elip(0, -334, 150, 18, 0, 1.0, 24), (204, 202, 194), 4.6, sp=5)
    ops += forma(rect(-170, -14, 170, 0, 2), (150, 146, 138), 3.8, sp=3)
    graf = (((-100, -250), (-40, -290), (20, -240), (-30, -200), ROJO_US), ((0, -160), (90, -220), (110, -140), (40, -110), AZUL_US),
            ((-110, -120), (-50, -150), (-20, -60), (-100, -40), ORO_US), ((50, -80), (110, -90), (120, -30), (60, -24), VERDE_US))
    for a, b, c, d, col in graf:
        ops += forma(curva([a, b, c, d], 5, cerrado=True), col, 3.6, sp=4)
    ops += [T(curva([(-120, -170), (-60, -186), (10, -170), (80, -190), (120, -170)], 6), 4.0, peso=0.02)]
    ops += [T(linea((60, -320), (40, -270), (70, -230), (50, -190)), 2.6, peso=0.02), T(linea((-120, -300), (-100, -260)), 2.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def ordenador_personal():
    """Ordenador personal de los 80: caja beige con pantalla encendida, ranura de disquete, teclado y ratón."""
    ops = forma(rect(-100, -330, 100, -90, 12), (226, 216, 190), 5.2, peso=0.5, sp=9)
    ops += forma(rect(-76, -308, 76, -176, 6), (52, 62, 78), 4.6, sp=5)
    ops += forma(rect(-66, -298, 66, -186, 4), (130, 196, 214), 3.2, sp=4)
    for x, y, c in ((-46, -270, ORO_US), (-6, -270, ROJO_US), (34, -270, VERDE_US), (-46, -226, AZUL_US)):
        ops += forma(rect(x, y, x + 24, y + 20, 3), c, 2.4, sp=2)
    ops += forma(rect(14, -150, 74, -138, 2), NEGRO_US, 2.8, sp=2)
    ops += forma(trap(-80, 80, -90, -100, 100, -70), (210, 200, 174), 4.4, sp=5)
    ops += forma(pol((-170, -40), (110, -40), (130, 0), (-190, 0)), (226, 216, 190), 4.8, sp=6)
    for j in range(3):
        for i in range(10):
            x = -170 + i * 28 + j * 6
            ops += [T(cerrar(rect(x, -34 + j * 11, x + 20, -26 + j * 11, 1, 2)), 1.6, peso=0.01)]
    ops += forma(elip(170, -14, 22, 16, 0, 1.0, 16), (226, 216, 190), 3.8, sp=3)
    ops += [T(curva([(170, -30), (160, -60), (130, -60)], 4), 2.4, peso=0.01)]
    return Dib(ops)


@lru_cache(maxsize=None)
def telefono_movil():
    """Teléfono inteligente: marco negro, pantalla con iconos de colores."""
    ops = forma(rect(-80, -320, 80, 0, 22), NEGRO_US, 5.2, peso=0.5, sp=8)
    ops += forma(rect(-68, -296, 68, -24, 10), (140, 196, 226), 3.4, sp=5)
    cols = (ROJO_US, ORO_US, VERDE_US, AZUL_US, (170, 110, 200), (240, 150, 90))
    for j in range(4):
        for i in range(3):
            x, y = -50 + i * 38, -276 + j * 44
            ops += forma(rect(x, y, x + 26, y + 26, 6), cols[(i + j * 3) % 6], 2.2, sp=2)
    ops += forma(rect(-20, -312, 20, -304, 3), GRIS_OSC_US, 2.0, sp=1)
    return Dib(ops)


@lru_cache(maxsize=None)
def globo_internet():
    """Internet conecta el planeta: globo con continentes, red de nodos luminosos y órbitas de datos."""
    c, r = (0, -180), 160
    ops = forma(circ(*c, r, n=48), (110, 166, 210), 5.2, peso=0.5, sp=9)
    for P in (((-120, -260), (-70, -300), (-40, -250), (-70, -210), (-110, -200)), ((-50, -170), (-10, -150), (-30, -80), (-70, -110)),
              ((30, -280), (110, -270), (130, -210), (80, -190), (40, -220)), ((50, -150), (110, -140), (90, -80), (50, -100))):
        ops += forma(curva(list(P), 4, cerrado=True), (128, 170, 100), 3.2, sp=4)
    nodos = ((-110, -230), (-60, -280), (-30, -130), (60, -250), (100, -170), (70, -100), (10, -200), (-90, -150), (120, -230), (-20, -60))
    for a, b in ((0, 1), (1, 6), (6, 3), (3, 8), (8, 4), (4, 5), (5, 9), (9, 2), (2, 7), (7, 0), (6, 2), (6, 4), (1, 3)):
        ops += [T(linea(nodos[a], nodos[b]), 2.4, peso=0.01)]
    for x, y in nodos:
        ops += forma(circ(x, y, 9, n=10), ORO_US, 2.6, sp=2)
    ops += [T(arco_(c[0], c[1], 200, 160, 380, 30, ry=56), 3.0, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def torres_gemelas():
    """Las Torres Gemelas del World Trade Center con fachada de líneas verticales y antena en la torre norte."""
    ops = forma(rect(-180, -60, -100, 0, 3), (196, 190, 180), 4.0, sp=5) + forma(rect(100, -80, 180, 0, 3), (186, 184, 178), 4.0, sp=5)
    ops += _ventanas(-176, -54, -104, -6, 4, 2, CRISTAL, m=0.4, w=0)
    for x0, h in ((-90, 360), (10, 350)):
        ops += forma(rect(x0, -h, x0 + 80, 0, 2), (176, 182, 192), 5.2, peso=0.5, sp=8)
        for k in range(1, 12):
            ops += [T(linea((x0 + 80 * k / 12, -h + 4), (x0 + 80 * k / 12, -4)), 1.4, peso=0.01)]
        ops += [rayita(x0, -h + 30, x0 + 80, -h + 30, 2.2), rayita(x0, -40, x0 + 80, -40, 2.2)]
    ops += [T(linea((-50, -360), (-50, -430)), 4.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def casa_blanca():
    """La Casa Blanca: pórtico con columnas y frontón, alas con ventanas, balaustrada y bandera en el tejado."""
    ops = forma(rect(-190, -30, 190, 0, 2), (120, 160, 96), 3.6, sp=6)
    ops += forma(rect(-180, -160, 180, -30, 2), BLANCO_US, 5.0, peso=0.5, sp=8)
    ops += _ventanas(-170, -140, -60, -50, 4, 2, CRISTAL, m=0.42) + _ventanas(60, -140, 170, -50, 4, 2, CRISTAL, m=0.42)
    ops += forma(rect(-186, -176, 186, -160, 2), BLANCO_US, 4.0, sp=4)
    for k in range(20):
        ops += [rayita(-180 + 18.9 * k, -174, -180 + 18.9 * k, -162, 1.6)]
    ops += forma(pol((-64, -200), (64, -200), (0, -248)), BLANCO_US, 4.6, sp=5)
    ops += forma(rect(-60, -200, 60, -186, 2), BLANCO_US, 3.6, sp=3)
    for k in range(6):
        x = -52 + 104 * k / 5
        ops += forma(rect(x - 6, -186, x + 6, -30, 2), (250, 248, 242), 3.0, sp=2)
    ops += forma(rect(-14, -80, 14, -30, 6), MADERA_OSC_US, 3.4, sp=2)
    ops += [T(linea((0, -248), (0, -300)), 3.4, peso=0.02)]
    ops += forma(pol((0, -300), (40, -294), (40, -276), (0, -280)), ROJO_US, 2.6, sp=2)
    ops += forma(rect(0, -300, 16, -290, 1), AZUL_US, 1.6, sp=1)
    return Dib(ops)


@lru_cache(maxsize=None)
def capitolio():
    """El Capitolio: cúpula blanca sobre tambor de columnas, linterna con la estatua, alas y escalinata."""
    ops = forma(rect(-200, -24, 200, 0, 2), (226, 222, 210), 4.4, sp=5)
    for lado in (-1, 1):
        ops += forma(rect(min(lado * 60, lado * 200), -120, max(lado * 60, lado * 200), -24, 2), BLANCO_US, 4.8, sp=7)
        ops += _ventanas(min(lado * 70, lado * 190), -106, max(lado * 70, lado * 190), -40, 6, 2, CRISTAL, m=0.5, w=0)
    ops += forma(rect(-64, -150, 64, -24, 2), BLANCO_US, 4.8, sp=6)
    ops += forma(pol((-64, -150), (64, -150), (0, -176)), BLANCO_US, 4.2, sp=4)
    for k in range(7):
        x = -54 + 108 * k / 6
        ops += [rayita(x, -146, x, -30, 2.2)]
    ops += forma(rect(-80, -210, 80, -176, 2), BLANCO_US, 4.4, sp=5)                             # tambor
    for k in range(11):
        ops += [rayita(-72 + 14.4 * k, -206, -72 + 14.4 * k, -180, 1.8)]
    ops += forma(arco_(0, -210, 74, 180, 360, 24).tolist() + [(-74, -210)], BLANCO_US, 5.0, peso=0.4, sp=7)   # cúpula
    for a in (210, 240, 270, 300, 330):
        r = math.radians(a)
        ops += [T(linea((74 * math.cos(r) * 0.3, -210 + 74 * math.sin(r) * 0.3), (74 * math.cos(r), -210 + 74 * math.sin(r))), 1.8, peso=0.01)]
    ops += forma(rect(-14, -310, 14, -282, 2), BLANCO_US, 3.6, sp=2)
    ops += forma(circ(0, -322, 9, n=10), (170, 160, 140), 3.0, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def skyline_nyc():
    """Perfil de Nueva York: rascacielos con ventanas, el Empire State escalonado con aguja y una torre art déco."""
    ops = []
    edif = ((-190, 140, (150, 160, 178)), (-150, 200, (176, 168, 156)), (-108, 160, (140, 150, 170)), (60, 180, (170, 162, 150)),
            (104, 230, (148, 158, 176)), (150, 150, (180, 172, 160)))
    for x, h, col in edif:
        ops += forma(rect(x, -h, x + 44, 0, 2), col, 4.4, sp=6)
        ops += _ventanas(x + 4, -h + 10, x + 40, -10, 3, max(3, h // 34), (236, 216, 150), m=0.45, w=0)
    # torre art déco (tipo Chrysler)
    ops += forma(rect(-64, -250, -18, 0, 2), (190, 186, 178), 4.6, sp=6)
    for k in range(4):
        y = -250 - 18 * k
        w = 23 - 5 * k
        ops += forma(curva([(-41 - w, y), (-41 - w + 3, y - 14), (-41, y - 20), (-41 + w - 3, y - 14), (-41 + w, y)], 4), CROMO, 3.2, sp=2)
    ops += [T(linea((-41, -322), (-41, -370)), 3.2, peso=0.02)]
    # Empire State
    ops += forma(rect(-12, -240, 52, 0, 2), (200, 192, 172), 5.0, peso=0.5, sp=8)
    ops += forma(rect(-2, -300, 42, -240, 2), (204, 196, 178), 4.6, sp=6)
    ops += forma(rect(6, -340, 34, -300, 2), (210, 202, 184), 4.4, sp=5)
    ops += forma(rect(12, -364, 28, -340, 2), (216, 208, 190), 4.0, sp=3)
    ops += [T(linea((20, -364), (20, -420)), 3.6, peso=0.02)]
    for x in (0, 10, 20, 30, 40):
        ops += [T(linea((x, -232), (x, -8)), 1.4, peso=0.01)]
    ops += [R(pol((-200, -6), (200, -6), (200, 0), (-200, 0)), GRIS_OSC_US, peso=0.01, sp=2)]
    return Dib(ops)


@lru_cache(maxsize=None)
def golden_gate():
    """El puente Golden Gate: dos torres rojas con portales, cable principal colgante, tirantes, tablero y la bahía."""
    rojo = (206, 88, 58)
    ops = [R(pol((-210, -40), (210, -40), (210, 0), (-210, 0)), AGUA_US, peso=0.03, sp=8)]
    ops += [T(ondas(-200, 200, -26, 4, 40), 3.0, peso=0.02)]
    ops += forma(rect(-210, -96, 210, -82, 2), rojo, 4.4, sp=4)
    for x in (-110, 110):
        ops += forma(rect(x - 16, -290, x - 6, -40, 2), rojo, 4.0, sp=3) + forma(rect(x + 6, -290, x + 16, -40, 2), rojo, 4.0, sp=3)
        for y in (-280, -230, -170, -120):
            ops += forma(rect(x - 16, y, x + 16, y + 10, 1), rojo, 3.0, sp=2)
    xs = np.linspace(-110, 110, 30)
    cable = [(x, -284 + 190 * (1 - (x / 110) ** 2)) for x in xs]
    ops += [T(np.asarray(cable, float), 4.4, peso=0.03)]
    ops += [T(np.asarray([(-210, -110), (-160, -200), (-110, -284)], float), 4.4, peso=0.02),
            T(np.asarray([(110, -284), (160, -200), (210, -110)], float), 4.4, peso=0.02)]
    for x, y in cable[2:-2:2]:
        ops += [T(linea((x, y), (x, -96)), 1.4, peso=0.01)]
    return Dib(ops)


@lru_cache(maxsize=None)
def saguaro():
    """Cactus saguaro del desierto del suroeste, con brazos, costillas y flores blancas."""
    ops = forma(curva([(-150, 0), (-100, -24), (0, -30), (100, -24), (150, 0)], 5), ADOBE, 4.0, sp=6)
    tronco = curva([(-26, -20), (-30, -260), (-20, -320), (0, -330), (20, -320), (30, -260), (26, -20)], 6)
    ops += forma(np.vstack([tronco, [(-26, -20)]]), VERDE_US, 5.2, peso=0.5, sp=8)
    for lado, y0, y1, dx in ((-1, -120, -230, 80), (1, -160, -270, 74)):
        brazo = [(lado * 26, y0), (lado * (dx - 10), y0 + 4), (lado * dx, y0 - 30), (lado * dx, y1), (lado * (dx - 20), y1 - 10),
                 (lado * (dx - 34), y1), (lado * (dx - 34), y0 - 34), (lado * 26, y0 - 30)]
        ops += forma(curva(brazo, 4, cerrado=True), VERDE_US, 4.6, sp=6)
    for x in (-14, 0, 14):
        ops += [T(linea((x, -310), (x * 1.3, -30)), 2.0, peso=0.01)]
    for x, y in ((-6, -330), (12, -326), (-72, -246), (70, -286)):
        ops += forma(circ(x, y, 8, n=10), BLANCO_US, 2.4, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def casa_embargo():
    """Casa embargada en la crisis de 2008: casa de madera con un cartel rojo clavado y torcido en el jardín."""
    ops = forma(rect(-180, -16, 140, 0, 2), (120, 160, 96), 3.4, sp=5)
    ops += forma(rect(-140, -180, 80, -16, 3), (190, 206, 220), 5.0, peso=0.5, sp=8)
    for y in range(-170, -20, 18):
        ops += [rayita(-140, y, 80, y, 1.4)]
    ops += forma(pol((-160, -176), (-30, -270), (100, -176)), ROJO_OSC_US, 4.8, sp=6)
    ops += forma(rect(-30, -100, 10, -16, 3), MADERA_OSC_US, 3.6, sp=3)
    ops += _ventanas(-120, -150, -50, -100, 2, 1, CRISTAL, m=0.2) + _ventanas(30, -150, 70, -100, 1, 1, CRISTAL, m=0.2)
    ops += [T(linea((-100, -150), (-60, -110)), 3.0, peso=0.01), T(linea((-60, -150), (-100, -110)), 3.0, peso=0.01)]
    ops += [T(linea((150, -10), (140, -150)), 5.0, peso=0.02)]
    cartel = _rot(rect(90, -230, 210, -150, 4)[:-1], 0.16, 150, -190)
    ops += forma(cartel, ROJO_US, 4.6, sp=5)
    ops += [T(_rot(linea((106, -210), (194, -170)), 0.16, 150, -190), 7.0, peso=0.02, v=60)]
    ops += [T(_rot(linea((106, -170), (194, -210)), 0.16, 150, -190), 7.0, peso=0.02, v=60)]
    return Dib(ops)


@lru_cache(maxsize=None)
def avion_comercial(pose=0):
    """Avión comercial a reacción: fuselaje blanco con franja azul y ventanillas, alas, motores y estela."""
    ops = []
    for k in range(4):
        x = -260 - 40 * k - 10 * (pose % 4)
        ops += forma(circ(x, -160, 10 + 3 * k, n=12), (236, 238, 242), 2.4, sp=3)
    ops += forma(pol((-220, -150), (-200, -260), (-170, -260), (-150, -156)), AZUL_US, 4.4, sp=4)
    fus = curva([(-226, -150), (-160, -176), (100, -180), (180, -170), (214, -150), (190, -132), (100, -124), (-160, -124), (-220, -140)], 6, cerrado=True)
    ops += forma(fus, BLANCO_US, 5.2, peso=0.5, sp=9)
    ops += [R(pol((-200, -142), (200, -142), (196, -132), (-200, -132)), AZUL_US, peso=0.01, sp=3)]
    for x in range(-150, 150, 18):
        ops += forma(circ(x, -158, 4, n=8), CRISTAL, 1.8, sp=1)
    ops += forma(pol((170, -170), (196, -164), (182, -156), (164, -160)), CRISTAL, 2.8, sp=2)
    ops += forma(pol((-210, -150), (-160, -152), (-200, -126)), AZUL_US, 3.2, sp=2)
    ops += forma(pol((-40, -140), (60, -140), (-10, -60), (-50, -60)), (210, 214, 222), 4.4, sp=5)
    ops += forma(rect(-30, -110, 30, -86, 10), ACERO, 3.8, sp=3) + forma(rect(-46, -82, 10, -62, 9), ACERO, 3.6, sp=3)
    return Dib(ops)
