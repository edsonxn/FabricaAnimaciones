# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de Estados Unidos en 6 minutos» (2/3): OBJETOS, LUGARES, ANIMALES y VEHÍCULOS hasta ~1890
(de las huellas de White Sands y Cahokia a la Guerra Civil). Origen en la BASE (y = 0 abajo, x centrado).
Lo que se mueve (`andar` llama fn(pose) con pose 0..3) mira a la DERECHA."""
import math
from functools import lru_cache

import numpy as np

from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from pal_us import *  # noqa: F401,F403

PIEDRA_US = (186, 176, 160)
PIEDRA_OSC = (140, 130, 118)
COQUINA = (214, 200, 168)
SILEX = (172, 150, 122)
LANA_MAMUT = (128, 86, 56)
LANA_OSC = (92, 60, 40)
MARFIL = (242, 232, 206)
PAJA = (214, 182, 112)
CORTEZA = (140, 108, 80)
MORADO_W = (104, 70, 120)
LADRILLO = (176, 88, 66)
BRONCE = (178, 132, 70)
BRONCE_OSC = (116, 98, 70)
LONA = (240, 234, 216)
HIERRO_US = (82, 84, 92)
VERDE_HOJA = (96, 146, 76)
VERDE_OSC_H = (66, 112, 60)
AGUA_US = (120, 176, 206)
ARENA_US = (232, 214, 172)
PERGAMINO = (238, 222, 182)
CERA = (186, 40, 44)


# ------------------------------------------------------------------ ayudas de geometría
def _seg(ax, ay, bx, by, wa, wb):
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / n, dx / n
    return [(ax + nx * wa, ay + ny * wa), (bx + nx * wb, by + ny * wb), (bx - nx * wb, by - ny * wb), (ax - nx * wa, ay - ny * wa)]


def _pierna(x0, y0, a1, a2, col, l1=60, l2=60, w1=16, w2=10, pezuna=NEGRO_US):
    """Pata articulada desde la cadera (x0, y0); ángulos en grados desde 'hacia abajo' (positivo = hacia delante, a la derecha)."""
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x0 + l1 * math.sin(r1), y0 + l1 * math.cos(r1)
    fx, fy = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    ops = forma(_seg(x0, y0, kx, ky, w1, w2 * 1.1), col, 4.2, sp=6) + forma(_seg(kx, ky, fx, fy, w2, w2 * 0.9), col, 4.0, sp=5)
    if pezuna is not None:
        ops += forma(pol((fx - w2 - 2, fy - 7), (fx + w2 + 3, fy - 7), (fx + w2 + 5, fy + 6), (fx - w2 - 3, fy + 6)), pezuna, 3.2, sp=3)
    return ops


def _paso(pose, ph):
    """Oscilación de una pata en el ciclo de 4 poses (−1..1)."""
    return math.sin(pose * math.pi / 2 + ph)


def _tubo(P, w0, w1, n=6):
    """Polígono de un tubo que sigue la curva P con ancho de w0 a w1 (trompas, colmillos, cuernos)."""
    C = curva(P, n)
    L = len(C)
    izq, der = [], []
    for i in range(L):
        a = C[max(0, i - 1)]
        b = C[min(L - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / m, dx / m
        w = (w0 + (w1 - w0) * i / max(1, L - 1)) / 2
        izq.append((C[i][0] + nx * w, C[i][1] + ny * w))
        der.append((C[i][0] - nx * w, C[i][1] - ny * w))
    return np.array(izq + der[::-1], float)


def _estrella(cx, cy, r, rot=-math.pi / 2):
    P = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = rot + k * math.pi / 5
        P.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return cerrar(P)


def _destellos(x, y, r0=12, r1=28, n=8, w=3.0):
    return [T(linea((x + r0 * math.cos(a), y + r0 * math.sin(a)), (x + r1 * math.cos(a), y + r1 * math.sin(a))), w, peso=0.02)
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def _anillo(cx, cy, rx, ry, g, rot=0.0, col=ACERO):
    """Eslabón (anillo): relleno de la banda entre dos elipses + tinta de ambas."""
    a = elip(cx, cy, rx, ry, rot, 1.0, 30)
    b = elip(cx, cy, rx - g, ry - g, rot, 1.0, 30)[::-1]
    banda_ = np.vstack([a, b])
    return [R(banda_, col, peso=0.03, sp=4, off=(2, -2)), T(a, 4.4, peso=0.04), T(b, 3.4, peso=0.03)]


def _humo(x, y, pose, n=3, r=20, col=(204, 202, 200), dx=-26):
    ops = []
    for k in range(n):
        d = (pose % 4) * 6
        ops += forma(circ(x + dx * k - d, y - 26 * k - d * 0.6, r + 7 * k, n=16), col, 3.6, sp=4)
    return ops


def _olas(ancho, y, pose, amp=5, lam=34):
    return [T(ondas(-ancho, ancho, y, amp, lam, ph=pose * math.pi / 2), 3.4, peso=0.03),
            T(ondas(-ancho * 0.8, ancho * 0.7, y + 16, amp * 0.7, lam * 1.2, ph=pose * math.pi / 2 + 1.3), 2.8, peso=0.03)]


def _rueda(cx, cy, r, pose, col=MADERA_US, rayos=10, buje=HIERRO_US, w=4.6):
    ops = forma(circ(cx, cy, r, n=28), None, w) + [T(circ(cx, cy, r - 7, n=28), 3.2, peso=0.03)]
    ops += [R(np.vstack([circ(cx, cy, r, n=28), circ(cx, cy, r - 7, n=28)[::-1]]), col, peso=0.03, sp=4, off=(2, -2))]
    a0 = pose * math.pi / (rayos / 2) / 2
    for k in range(rayos):
        a = a0 + k * 2 * math.pi / rayos
        ops += [T(linea((cx + 8 * math.cos(a), cy + 8 * math.sin(a)), (cx + (r - 7) * math.cos(a), cy + (r - 7) * math.sin(a))), 3.4, peso=0.02)]
    ops += forma(circ(cx, cy, 9, n=12), buje, 3.4, sp=3)
    return ops


def _sub(P, n=8):
    """Subdivide los lados de un polígono cerrado (para deformarlo con la ondulación de una bandera)."""
    P = np.asarray(P, float)
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        for k in range(n):
            out.append(a + (b - a) * k / n)
    return np.array(out)


def _bandera(regiones, ancho=230, alto=150, asta=400, amp=9.0, contorno=True):
    """Bandera ondeando en su asta. `regiones` = [(polígono en (u, v) 0..1, color), ...] (la primera suele ser el fondo)."""
    xp = -ancho / 2
    ytop = -asta + 18

    def m(P):
        P = np.asarray(P, float)
        u, v = P[:, 0], P[:, 1]
        return np.stack([xp + u * ancho, ytop + v * alto + amp * np.sin(u * 4.2) * u], 1)

    ops = forma(rect(xp - 8, -asta, xp + 2, 0, 3), MADERA_OSC_US, 4.2, sp=4)
    ops += forma(circ(xp - 3, -asta - 10, 11, n=14), ORO_US, 3.6, sp=3)
    for P, col in regiones:
        Q = m(_sub(P, 10))
        ops.append(R(Q, col, peso=0.02, sp=5, off=(2, -2)))
    if contorno:
        ops.append(T(cerrar(m(_sub([(0, 0), (1, 0), (1, 1), (0, 1)], 16))), 4.2, peso=0.05))
    ops += [T(linea((xp + 2, ytop + 4), (xp + 2, ytop + alto - 4)), 3.0, peso=0.02)]
    return ops, m


def _banda_diag(a, b, w):
    """Banda recta de ancho w (en u,v) entre a y b, como polígono (u, v)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    return [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]


def _pegar(d, dx=0.0, dy=0.0, s=1.0, flip=False):
    return colocar(list(d.ops), dx, dy, s, 0.0, flip)


# ------------------------------------------------------------------ PRIMEROS POBLADORES Y PUEBLOS ORIGINARIOS
def _huella(x, y, s, lado, rot):
    ops = []
    pl = elip(x, y, 13 * s, 30 * s, rot, 1.0, 22)
    ops += forma(pl, BLANCO_US, 3.6, sp=4)
    c, sn = math.cos(rot), math.sin(rot)
    for k in range(5):
        tx = (-12 + 6 * k) * s * lado
        ty = (-38 + abs(k - 1.5) * 2.4) * s
        ops += forma(circ(x + tx * c - ty * sn, y + tx * sn + ty * c, (5.2 - 0.5 * k) * s, n=10), BLANCO_US, 2.6, sp=2)
    return ops


@lru_cache(maxsize=None)
def huellas_pie():
    """Huellas humanas fósiles de White Sands (≈ 21 000-23 000 años): placa de yeso con una fila de pisadas."""
    ops = forma(curva([(-190, -10), (-176, -96), (-60, -132), (90, -128), (192, -88), (186, -6), (40, 4), (-120, 2)], 6, cerrado=True),
                ARENA_US, 5.2, peso=0.5, sp=9)
    ops += [T(ondas(-170, 170, -20, 3, 40), 2.6, peso=0.02)]
    for k in range(6):
        lado = 1 if k % 2 else -1
        x = -138 + 54 * k
        y = -50 - 12 * k * 0.6 + lado * 14
        ops += _huella(x, y, 0.95, lado, math.radians(78))
    return Dib(ops)


@lru_cache(maxsize=None)
def punta_clovis():
    """Punta de proyectil Clovis de sílex, con la acanaladura central y los lascados."""
    P = [(-44, 0), (-56, -70), (-50, -160), (-28, -236), (0, -272), (28, -236), (50, -160), (56, -70), (44, 0), (22, -14), (0, -20), (-22, -14)]
    ops = forma(curva(P, 5, cerrado=True), SILEX, 5.4, peso=0.5, sp=8)
    ops += forma(curva([(-14, -16), (-18, -70), (0, -112), (18, -70), (14, -16), (0, -22)], 5, cerrado=True), (204, 186, 160), 3.2, sp=4)
    for k in range(7):
        y = -40 - 30 * k
        w = 50 - abs(k - 2) * 7
        ops += [rayita(-w, y, -w + 22, y - 20, 2.6), rayita(w, y, w - 22, y - 20, 2.6)]
    return Dib(ops)


def mamut(pose=0):
    """Mamut lanudo caminando (4 poses)."""
    ops = []
    patas = ((-104, -150, 0.0, True), (70, -150, math.pi, True), (-80, -150, math.pi, False), (96, -150, 0.0, False))
    for x, y, ph, lejos in patas:
        if lejos:
            a = 16 * _paso(pose, ph)
            ops += _pierna(x, y, a, a * 0.4 - 4, LANA_OSC, 80, 70, 28, 24, pezuna=(70, 60, 54))
    cuerpo = [(-180, -170), (-176, -246), (-120, -300), (-30, -322), (50, -330), (110, -352), (160, -330), (196, -270), (196, -214),
              (150, -168), (60, -140), (-60, -132), (-150, -140)]
    ops += forma(curva(cuerpo, 6, cerrado=True), LANA_MAMUT, 6.0, peso=0.7, sp=11)
    for k in range(12):
        x = -160 + 28 * k
        ops += [T(linea((x, -150 + 4 * (k % 3)), (x - 6, -112 + 6 * (k % 2))), 3.0, peso=0.02)]
    ops += [T(curva([(-170, -230), (-110, -268), (-40, -288)], 6), 2.8, peso=0.02), T(curva([(-60, -300), (20, -306)], 4), 2.6, peso=0.02)]
    ops += forma(elip(108, -280, 34, 46, 0.25, 1.0, 20), LANA_OSC, 4.2, sp=5)
    trompa = _tubo([(186, -246), (212, -190), (214, -120), (196, -70), (178, -66)], 50, 18)
    ops += forma(trompa, LANA_MAMUT, 4.8, sp=7)
    for y in (-200, -160, -120):
        ops += [rayita(194, y, 226, y + 4, 2.6)]
    col1 = _tubo([(176, -206), (214, -170), (262, -168), (294, -206), (300, -246)], 26, 10)
    ops += forma(col1, MARFIL, 4.6, sp=6)
    ops += [punto(168, -284, 9)]
    a = 10 * _paso(pose, 0.6)
    ops += forma(_tubo([(-176, -224), (-198 + a, -190), (-204 + a, -156)], 12, 6), LANA_OSC, 3.6, sp=4)
    for x, y, ph, lejos in patas:
        if not lejos:
            a = 16 * _paso(pose, ph)
            ops += _pierna(x, y, a, a * 0.4 - 4, LANA_MAMUT, 80, 70, 30, 25, pezuna=(70, 60, 54))
    return Dib(ops)


def bisonte(pose=0):
    """Bisonte americano al paso (4 poses)."""
    ops = []
    pelo_d = (96, 64, 44)
    pelo_c = (146, 102, 66)
    patas = ((-112, -120, 0.0, True), (80, -118, math.pi, True), (-88, -120, math.pi, False), (104, -118, 0.0, False))
    for x, y, ph, lejos in patas:
        if lejos:
            a = 20 * _paso(pose, ph)
            ops += _pierna(x, y, a, a * 0.5 - 6, (78, 52, 36), 58, 58, 16, 10)
    cuerpo = [(-160, -130), (-166, -196), (-120, -230), (-20, -238), (50, -290), (110, -292), (152, -250), (176, -190), (196, -138),
              (176, -104), (130, -96), (60, -104), (-60, -104), (-140, -108)]
    ops += forma(curva(cuerpo, 6, cerrado=True), pelo_c, 5.8, peso=0.6, sp=10)
    delante = [(-10, -236), (50, -290), (110, -292), (152, -250), (176, -190), (196, -138), (176, -104), (130, -94), (60, -100), (20, -150)]
    ops += forma(curva(delante, 6, cerrado=True), pelo_d, 4.6, sp=8)
    ops += forma(curva([(150, -224), (196, -214), (224, -176), (222, -136), (200, -118), (172, -132), (156, -176)], 5, cerrado=True), pelo_d, 4.6, sp=6)
    ops += forma(curva([(184, -132), (196, -96), (178, -70), (166, -100)], 4, cerrado=True), pelo_d, 3.6, sp=4)
    ops += forma(_tubo([(186, -214), (196, -246), (178, -260)], 12, 4), MARFIL, 3.4, sp=3)
    ops += [punto(206, -182, 8)]
    for k in range(6):
        x = 40 + 20 * k
        ops += [T(linea((x, -110), (x - 4, -84)), 2.6, peso=0.02)]
    a = 8 * _paso(pose, 0.9)
    ops += [T(curva([(-162, -180), (-182 + a, -150), (-178 + a, -112)], 5), 4.4, peso=0.03)]
    ops += forma(elip(-178 + a, -108, 7, 12, 0, 1.0, 10), pelo_d, 3.0, sp=2)
    for x, y, ph, lejos in patas:
        if not lejos:
            a = 20 * _paso(pose, ph)
            ops += _pierna(x, y, a, a * 0.5 - 6, pelo_d, 58, 58, 17, 11)
    return Dib(ops)


@lru_cache(maxsize=None)
def monks_mound():
    """Monks Mound (Cahokia): gran plataforma de tierra en terrazas, rampa y templo de madera con techo de paja en la cima."""
    tierra = TIERRA_US
    cesped = (138, 152, 88)
    ops = forma(rect(-200, -18, 200, 0, 4), (176, 160, 110), 4.0, sp=6)
    ops += forma(trap(-170, 150, -110, -196, 192, -14), tierra, 5.4, peso=0.6, sp=10)
    ops += forma(trap(-150, 136, -122, -170, 150, -108), cesped, 4.2, sp=6)
    ops += forma(trap(-110, 90, -190, -140, 120, -120), tierra, 5.0, sp=9)
    ops += forma(trap(-96, 80, -200, -110, 90, -188), cesped, 4.0, sp=5)
    ops += forma(pol((-20, -14), (20, -14), (8, -120), (-8, -120)), (190, 150, 104), 3.8, sp=5)
    for k in range(9):
        y = -24 - 11 * k
        w = 19 - 1.2 * k
        ops += [rayita(-w, y, w, y, 2.4)]
    ops += forma(rect(-56, -268, 44, -200, 3), MADERA_US, 4.6, sp=6)
    for k in range(5):
        ops += [rayita(-46 + 20 * k, -264, -46 + 20 * k, -204, 2.4)]
    ops += forma(pol((-76, -262), (-6, -330), (64, -262)), PAJA, 4.8, sp=7)
    for k in range(7):
        ops += [rayita(-60 + 18 * k, -268, -18 + 8 * k, -316, 2.2)]
    ops += forma(rect(-14, -232, 6, -200, 2), NEGRO_US, 3.2, sp=3)
    ops += [T(linea((80, -200), (82, -300)), 4.4, peso=0.04)]
    ops += forma(pol((82, -298), (128, -290), (82, -276)), ROJO_US, 3.2, sp=3)
    return Dib(ops)


def _choza(x, y, s=1.0, col=PAJA):
    ops = forma(rect(x - 34 * s, y - 46 * s, x + 34 * s, y, 3), ADOBE, 3.8, sp=5)
    ops += forma(curva([(x - 46 * s, y - 40 * s), (x - 30 * s, y - 84 * s), (x, y - 104 * s), (x + 30 * s, y - 84 * s), (x + 46 * s, y - 40 * s)], 5),
                 col, 4.2, sp=6)
    ops += [rayita(x - 20 * s, y - 50 * s, x - 8 * s, y - 90 * s, 2.2), rayita(x + 16 * s, y - 50 * s, x + 6 * s, y - 92 * s, 2.2)]
    ops += forma(rect(x - 8 * s, y - 30 * s, x + 8 * s, y, 2), NEGRO_US, 2.8, sp=2)
    return ops


@lru_cache(maxsize=None)
def aldea_cahokia():
    """Aldea de Cahokia: chozas de techo de paja detrás de la gran empalizada de troncos con bastiones."""
    ops = []
    for x, y, s in ((-130, -110, 0.9), (-30, -126, 1.0), (80, -112, 0.85), (150, -98, 0.7)):
        ops += _choza(x, y, s)
    ops += forma(rect(-200, -12, 200, 0, 3), (176, 160, 110), 3.8, sp=6)
    for k in range(25):
        x = -192 + 16 * k
        alto = 112 + 6 * math.sin(k * 1.7)
        ops += forma(pol((x - 8, -6), (x - 8, -alto), (x, -alto - 16), (x + 8, -alto), (x + 8, -6)), MADERA_US if k % 2 else MADERA_OSC_US, 3.2, sp=3)
    for bx in (-120, 40):
        ops += forma(rect(bx - 24, -150, bx + 24, -6, 3), MADERA_OSC_US, 4.2, sp=5)
        for k in range(3):
            ops += forma(pol((bx - 24 + 16 * k, -150), (bx - 16 + 16 * k, -168), (bx - 8 + 16 * k, -150)), MADERA_US, 2.8, sp=2)
    ops += [rayita(-196, -48, 196, -48, 3.0), rayita(-196, -86, 196, -86, 2.6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def casa_acantilado():
    """Cliff Palace (Mesa Verde): aldea de adobe y torres dentro de una alcoba del acantilado de arenisca."""
    roca = ARENISCA
    borde = [(-210, 0), (-212, -300), (-170, -334), (-120, -322), (-60, -352), (10, -340), (70, -364), (140, -338), (186, -346), (212, -306), (210, 0)]
    ops = forma(curva(borde, 4), roca, 5.6, peso=0.6, sp=11)
    ops += forma(curva([(-212, -300), (-170, -334), (-120, -322), (-60, -352), (10, -340), (70, -364), (140, -338), (186, -346), (212, -306),
                        (190, -290), (120, -300), (40, -306), (-60, -300), (-150, -292)], 4, cerrado=True), (178, 168, 96), 3.6, sp=6)
    alcoba = curva([(-190, -60), (-180, -150), (-120, -224), (0, -250), (120, -226), (184, -150), (192, -60)], 7)
    ops += forma(np.vstack([alcoba, [(192, -50), (-190, -50)]]), (122, 82, 60), 4.6, sp=8)
    for y in (-290, -320, -30):
        ops += [T(ondas(-200, 200, y, 3, 60), 2.6, peso=0.02)]
    for k in range(5):
        ops += [rayita(-200 + 90 * k, -270, -170 + 90 * k, -300, 2.4)]
    casas = ((-170, -62, -110, -130), (-114, -62, -50, -150), (-48, -62, 40, -122), (44, -62, 110, -146), (112, -62, 176, -110))
    for x0, y0, x1, y1 in casas:
        ops += forma(rect(x0, y1, x1, y0, 3), ADOBE, 4.0, sp=6)
        for wx in np.linspace(x0 + 14, x1 - 14, max(1, int((x1 - x0) / 34))):
            ops += forma(pol((wx - 7, y1 + 22), (wx + 7, y1 + 22), (wx + 7, y1 + 30), (wx + 4, y1 + 30), (wx + 4, y1 + 42), (wx - 4, y1 + 42),
                             (wx - 4, y1 + 30), (wx - 7, y1 + 30)), NEGRO_US, 2.4, sp=2)
        ops += [rayita(x0, y1 + 10, x1, y1 + 10, 2.0)]
    ops += forma(rect(-36, -200, 0, -122, 3), ADOBE, 4.2, sp=5)
    ops += forma(rect(-30, -186, -6, -176, 1), NEGRO_US, 2.2, sp=2)
    ops += forma(curva([(60, -146), (60, -196), (78, -204), (96, -196), (96, -146)], 4), ADOBE, 4.0, sp=5)
    ops += forma(rect(-210, -62, 210, -44, 3), roca, 4.2, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def vasija_pueblo():
    """Vasija de los pueblos ancestrales, negro sobre blanco con grecas escalonadas."""
    cuerpo = curva([(-50, -6), (-110, -70), (-118, -130), (-80, -186), (-50, -210), (-54, -244), (54, -244), (50, -210), (80, -186), (118, -130),
                    (110, -70), (50, -6)], 6, cerrado=True)
    ops = forma(cuerpo, BLANCO_US, 5.2, peso=0.5, sp=8)
    ops += [T(curva([(-104, -170), (0, -182), (104, -170)], 6), 3.0, peso=0.02), T(curva([(-116, -96), (0, -106), (116, -96)], 6), 3.0, peso=0.02)]
    for k in range(6):
        x = -92 + 37 * k
        ops += [R(pol((x, -110), (x + 18, -110), (x + 18, -130), (x + 30, -130), (x + 30, -152), (x, -152)), NEGRO_US, peso=0.02, sp=3, off=(1, -1))]
        ops += [T(linea((x, -110), (x + 18, -110), (x + 18, -130), (x + 30, -130), (x + 30, -152), (x, -152), (x, -110)), 2.4, peso=0.02)]
    for k in range(8):
        x = -84 + 24 * k
        ops += [T(linea((x, -60), (x + 12, -80), (x + 24, -60)), 3.0, peso=0.02)]
    ops += [T(linea((-50, -228), (50, -228)), 4.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def casa_larga():
    """Casa larga iroquesa (Haudenosaunee): bóveda de corteza de olmo sobre varas, puerta al extremo y humo de los fogones."""
    ops = forma(rect(-200, -12, 200, 0, 3), (150, 160, 100), 3.8, sp=6)
    boveda = curva([(-190, -6), (-192, -110), (-150, -168), (0, -184), (150, -168), (192, -110), (190, -6)], 7)
    ops += forma(boveda, CORTEZA, 5.6, peso=0.6, sp=10)
    for k in range(8):
        x = -170 + 48 * k
        ops += [T(curva([(x, -8), (x + 2, -110), (x + 6, -170)], 4), 2.6, peso=0.02)]
    for y in (-60, -110, -150):
        ops += [T(curva([(-188, y), (0, y - 8), (188, y)], 6), 2.4, peso=0.02)]
    ops += forma(curva([(140, -6), (140, -78), (160, -96), (180, -78), (180, -6)], 4), NEGRO_US, 3.6, sp=4)
    for x in (-90, 30):
        ops += forma(rect(x - 14, -196, x + 14, -180, 2), (96, 70, 50), 3.0, sp=2)
        ops += forma(circ(x - 8, -224, 15, n=14), (204, 202, 200), 3.0, sp=3) + forma(circ(x - 22, -256, 21, n=14), (204, 202, 200), 3.0, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def cinturon_wampum():
    """Cinturón de wampum de Hiawatha: las cinco naciones iroquesas unidas (cuentas moradas y blancas)."""
    ops = forma(rect(-200, -126, 200, -24, 6), MORADO_W, 5.2, peso=0.5, sp=8)
    for k in range(10):
        ops += [rayita(-200 + 40 * k + 20, -124, -200 + 40 * k + 20, -26, 1.8)]
    for y in (-100, -75, -50):
        ops += [rayita(-198, y, 198, y, 1.6)]
    ops += [R(rect(-180, -79, 180, -71, 2), BLANCO_US, peso=0.02, sp=3, off=(1, -1))]
    for x in (-150, -80, 80, 150):
        ops += forma(rect(x - 18, -96, x + 18, -54, 2), BLANCO_US, 3.2, sp=3)
        ops += forma(rect(x - 8, -84, x + 8, -66, 1), MORADO_W, 2.4, sp=2)
    arbol = [(0, -106), (-26, -60), (-8, -60), (-8, -48), (8, -48), (8, -60), (26, -60)]
    ops += forma(arbol, BLANCO_US, 3.2, sp=3)
    ops += forma(pol((0, -114), (-18, -84), (18, -84)), BLANCO_US, 3.0, sp=3)
    for x in (-200, 200):
        for k in range(4):
            yy = -110 + 24 * k
            ops += [T(curva([(x, yy), (x + (14 if x > 0 else -14), yy + 30), (x + (8 if x > 0 else -8), yy + 60)], 4), 2.8, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tipi():
    """Tipi de las praderas: lona de piel de bisonte sobre varas, banda pintada y puerta abierta."""
    ops = []
    for dx in (-30, -14, 4, 22, 36):
        ops += [T(linea((dx * 0.25, -300), (dx * 1.3, -380)), 4.0, peso=0.03)]
    cono = [(-160, 0), (-8, -300), (8, -300), (160, 0)]
    ops += forma(cono, GAMUZA, 5.6, peso=0.6, sp=10)
    ops += forma(pol((-112, -90), (112, -90), (128, -60), (-128, -60)), ROJO_US, 3.6, sp=4)
    for k in range(7):
        x = -96 + 32 * k
        ops += forma(pol((x - 9, -60), (x, -42), (x + 9, -60)), AZUL_US, 2.4, sp=2)
    ops += forma(curva([(-36, 0), (-30, -80), (0, -104), (30, -80), (36, 0)], 4), (96, 64, 40), 4.0, sp=5)
    ops += forma(pol((30, -84), (46, 0), (80, 0)), (226, 196, 140), 3.4, sp=3)
    for y in (-150, -200, -244):
        ops += [punto(-4, y, 6), punto(8, y + 6, 6)]
    ops += forma(circ(-50, -200, 18, n=14), ORO_US, 3.0, sp=3)
    ops += _destellos(-50, -200, 22, 34, 8, 2.4)
    return Dib(ops)


# ------------------------------------------------------------------ COLONIAS
def _cruz_borgona(m, a, b, w):
    """Aspa de Borgoña (troncos cruzados con nudos) en coordenadas (u, v)."""
    regs = [(_banda_diag(a[0], a[1], w), ROJO_US), (_banda_diag(b[0], b[1], w), ROJO_US)]
    return regs


@lru_cache(maxsize=None)
def bandera_borgona():
    """Bandera de la Cruz de Borgoña (España): blanca con aspa roja de troncos."""
    regs = [([(0, 0), (1, 0), (1, 1), (0, 1)], BLANCO_US)]
    regs += [(_banda_diag((0.08, 0.06), (0.92, 0.94), 0.12), ROJO_US), (_banda_diag((0.92, 0.06), (0.08, 0.94), 0.12), ROJO_US)]
    for (u, v) in ((0.3, 0.3), (0.7, 0.7), (0.7, 0.3), (0.3, 0.7)):
        regs.append(([(u - 0.06, v - 0.03), (u + 0.02, v - 0.1), (u + 0.06, v - 0.06), (u - 0.02, v + 0.01)], ROJO_US))
    ops, m = _bandera(regs)
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera_francia_real():
    """Bandera real francesa: blanca con flores de lis doradas."""
    regs = [([(0, 0), (1, 0), (1, 1), (0, 1)], BLANCO_US)]
    ops, m = _bandera(regs)
    for (u, v) in ((0.28, 0.32), (0.72, 0.32), (0.5, 0.72)):
        lis = [(u, v - 0.2), (u + 0.04, v - 0.08), (u + 0.02, v + 0.02), (u + 0.1, v - 0.02), (u + 0.13, v - 0.12), (u + 0.16, v - 0.02),
               (u + 0.1, v + 0.06), (u + 0.03, v + 0.06), (u + 0.04, v + 0.14), (u - 0.04, v + 0.14), (u - 0.03, v + 0.06), (u - 0.1, v + 0.06),
               (u - 0.16, v - 0.02), (u - 0.13, v - 0.12), (u - 0.1, v - 0.02), (u - 0.02, v + 0.02), (u - 0.04, v - 0.08)]
        Q = m(lis)
        ops += [R(cerrar(Q), ORO_US, peso=0.02, sp=3, off=(1, -1)), T(cerrar(Q), 2.6, peso=0.02)]
        ops += [T(m([(u - 0.07, v + 0.03), (u + 0.07, v + 0.03)]), 3.4, peso=0.02)]
    return Dib(ops)


def _union_jack_regs(fondo=(0, 0, 1, 1)):
    regs = [([(0, 0), (1, 0), (1, 1), (0, 1)], AZUL_OSC_US)]
    regs += [(_banda_diag((0, 0), (1, 1), 0.2), BLANCO_US), (_banda_diag((1, 0), (0, 1), 0.2), BLANCO_US)]
    regs += [([(0.38, 0), (0.62, 0), (0.62, 1), (0.38, 1)], BLANCO_US), ([(0, 0.36), (1, 0.36), (1, 0.64), (0, 0.64)], BLANCO_US)]
    regs += [([(0.43, 0), (0.57, 0), (0.57, 1), (0.43, 1)], ROJO_US), ([(0, 0.41), (1, 0.41), (1, 0.59), (0, 0.59)], ROJO_US)]
    return regs


@lru_cache(maxsize=None)
def bandera_britanica():
    """Union Jack de 1707 (cruces de San Jorge y San Andrés, sin la de San Patricio)."""
    ops, m = _bandera(_union_jack_regs())
    return Dib(ops)


@lru_cache(maxsize=None)
def castillo_san_marcos():
    """Castillo de San Marcos (San Agustín): fuerte abaluartado de coquina con garitas y la bandera de Borgoña."""
    ops = forma(rect(-210, -20, 210, 0, 3), AGUA_US, 3.8, sp=6)
    ops += [T(ondas(-200, 200, -10, 3, 30), 2.4, peso=0.02)]
    ops += forma(rect(-130, -150, 130, -16, 3), COQUINA, 5.4, peso=0.5, sp=9)
    for k in range(9):
        ops += forma(rect(-128 + 30 * k, -166, -114 + 30 * k, -148, 1), COQUINA, 2.6, sp=2)
    for sx in (-1, 1):
        b = [(sx * 110, -16), (sx * 110, -170), (sx * 160, -196), (sx * 210, -170), (sx * 210, -16)]
        ops += forma(b, (226, 214, 184), 5.2, sp=8)
        gx = sx * 210
        ops += forma(rect(gx - 14 - sx * 8, -226, gx + 14 - sx * 8, -184, 3), COQUINA, 3.6, sp=4)
        ops += forma(curva([(gx - 18 - sx * 8, -224), (gx - sx * 8, -250), (gx + 18 - sx * 8, -224)], 4), COQUINA, 3.4, sp=3)
        ops += forma(rect(gx - 5 - sx * 8, -214, gx + 5 - sx * 8, -200, 1), NEGRO_US, 2.0, sp=2)
        for y in (-60, -110):
            ops += [rayita(sx * 120, y, sx * 200, y, 2.2)]
    for y in (-50, -90, -130):
        ops += [T(ondas(-126, 126, y, 2, 50), 2.2, peso=0.02)]
    ops += forma(curva([(-30, -16), (-30, -70), (0, -92), (30, -70), (30, -16)], 4), MADERA_OSC_US, 4.0, sp=5)
    ops += [rayita(0, -88, 0, -18, 2.4)]
    bd, m = _bandera([([(0, 0), (1, 0), (1, 1), (0, 1)], BLANCO_US),
                      (_banda_diag((0.08, 0.08), (0.92, 0.92), 0.13), ROJO_US), (_banda_diag((0.92, 0.08), (0.08, 0.92), 0.13), ROJO_US)],
                     ancho=110, alto=72, asta=180)
    ops += colocar(bd, 50, -166, 1.0)
    return Dib(ops)


def _casco_barco(L, cola, proa, alto, col, banda=None, castillo=True, dy=0.0):
    """Casco de velero de perfil a la derecha. Devuelve ops."""
    P = [(-L, -alto - cola + dy), (-L + 10, -40 + dy), (-L * 0.6, 4 + dy), (L * 0.55, 4 + dy), (L * 0.9, -30 + dy), (L + proa, -alto * 0.9 + dy),
         (L * 0.8, -alto * 0.72 + dy), (L * 0.5, -alto * 0.62 + dy), (-L * 0.55, -alto * 0.62 + dy), (-L * 0.75, -alto - cola + dy)]
    ops = forma(curva(P, 5, cerrado=True), col, 5.6, peso=0.6, sp=9)
    if banda:
        ops += [R(pol((-L + 6, -alto * 0.42 + dy), (L * 0.86, -alto * 0.42 + dy), (L * 0.8, -alto * 0.3 + dy), (-L + 12, -alto * 0.3 + dy)), banda,
                  peso=0.02, sp=4, off=(2, -2))]
    ops += [T(linea((-L + 10, -alto * 0.36 + dy), (L * 0.84, -alto * 0.36 + dy)), 3.0, peso=0.02)]
    for k in range(5):
        ops += forma(rect(-L * 0.5 + k * L * 0.25 - 7, -alto * 0.26 + dy, -L * 0.5 + k * L * 0.25 + 7, -alto * 0.14 + dy, 2), NEGRO_US, 2.6, sp=2)
    if castillo:
        ops += forma(rect(-L - 6, -alto - cola - 40 + dy, -L * 0.62, -alto - cola + 4 + dy, 3), col, 4.4, sp=6)
        ops += [rayita(-L - 2, -alto - cola - 20 + dy, -L * 0.66, -alto - cola - 20 + dy, 2.4)]
    ops += [T(linea((L + proa - 4, -alto * 0.9 + dy), (L + proa + 70, -alto * 1.25 + dy)), 4.2, peso=0.04)]
    return ops


def _velas(mastiles, base_y, pose, col=LONA, cruz=False, cruz_col=ROJO_US):
    ops = []
    for x, h, w in mastiles:
        ops += [T(linea((x, base_y), (x, base_y - h)), 5.0, peso=0.08)]
        sw = 7 * math.sin(pose * math.pi / 2 + x * 0.02)
        for k, (f0, f1, ww) in enumerate(((0.92, 0.6, w * 0.78), (0.56, 0.2, w))):
            y0, y1 = base_y - h * f0, base_y - h * f1
            vela = [(x - ww, y0), (x + ww, y0), (x + ww * 0.95 + sw, y1), (x - ww * 0.95 + sw, y1)]
            ops += [T(linea((x - ww - 6, y0), (x + ww + 6, y0)), 3.6, peso=0.02)]
            ops += forma(curva(vela + [vela[0]], 4), col, 4.2, sp=7)
            if cruz and k == 1:
                cx, cy = x + sw * 0.5, (y0 + y1) / 2
                hh = (y1 - y0) * 0.36
                ops += [R(np.array(_seg(cx - ww * 0.55, cy - hh, cx + ww * 0.55, cy + hh, 6, 6)), cruz_col, peso=0.02, sp=3, off=(1, -1)),
                        R(np.array(_seg(cx + ww * 0.55, cy - hh, cx - ww * 0.55, cy + hh, 6, 6)), cruz_col, peso=0.02, sp=3, off=(1, -1))]
    return ops


def _gallardete(x, y, col, pose, largo=56):
    a = 6 * math.sin(pose * math.pi / 2)
    return forma(pol((x, y), (x + largo, y + 8 + a), (x, y + 18)), col, 3.0, sp=3)


def galeon_es(pose=0):
    """Galeón español con velas de la cruz de Borgoña, cabeceando sobre las olas (4 poses)."""
    dy = 4 * math.sin(pose * math.pi / 2)
    ops = _velas(((-120, 250, 46), (-10, 310, 62), (98, 260, 52)), -110 + dy, pose, cruz=True)
    ops += _casco_barco(170, 36, 30, 130, MADERA_OSC_US, banda=ORO_US, dy=dy)
    ops += forma(pol((-176, -300 + dy), (-120, -360 + dy), (-120, -300 + dy)), LONA, 3.4, sp=3)
    ops += _gallardete(-10, -420 + dy, ROJO_US, pose)
    ops += _olas(200, 2, pose)
    return Dib(ops)


def barco_ingles(pose=0):
    """Velero inglés (Susan Constant, 1607) con la cruz de San Jorge (4 poses)."""
    dy = 3 * math.sin(pose * math.pi / 2 + 0.7)
    ops = _velas(((-90, 220, 40), (10, 270, 52), (100, 200, 40)), -96 + dy, pose)
    ops += _casco_barco(150, 24, 26, 110, (132, 94, 62), banda=(62, 88, 120), dy=dy)
    fx, fy = 10, -366 + dy
    ops += forma(rect(fx, fy, fx + 70, fy + 44, 2), BLANCO_US, 3.4, sp=3)
    ops += [R(rect(fx + 28, fy, fx + 42, fy + 44, 1), ROJO_US, peso=0.02, sp=3, off=(1, -1)),
            R(rect(fx, fy + 16, fx + 70, fy + 28, 1), ROJO_US, peso=0.02, sp=3, off=(1, -1))]
    ops += _olas(180, 2, pose)
    return Dib(ops)


def mayflower(pose=0):
    """El Mayflower (1620): mercante de popa alta, casco rojizo con franja ocre y la bandera del rey en el palo mayor (4 poses)."""
    dy = 5 * math.sin(pose * math.pi / 2 + 1.4)
    ops = _velas(((-110, 240, 44), (4, 300, 60), (112, 226, 46)), -120 + dy, pose, col=(236, 226, 200))
    ops += forma(pol((-196, -300 + dy), (-150, -350 + dy), (-150, -300 + dy)), (236, 226, 200), 3.4, sp=3)
    ops += _casco_barco(176, 50, 34, 140, (150, 84, 58), banda=(206, 160, 76), dy=dy)
    ops += forma(rect(-190, -246 + dy, -160, -226 + dy, 2), ORO_US, 3.0, sp=2)
    for x in (-174, -146):
        ops += forma(rect(x - 6, -214 + dy, x + 6, -200 + dy, 1), (236, 200, 120), 2.2, sp=2)
    fl, m = _bandera(_union_jack_regs(), ancho=76, alto=48, asta=40, amp=4)
    ops += colocar(fl, 44, -420 + dy, 1.0)
    ops += _olas(210, 2, pose)
    return Dib(ops)


@lru_cache(maxsize=None)
def mision_espanola():
    """Misión española de adobe con campanario, campana, cruz y portón de madera."""
    ops = forma(rect(-200, -10, 200, 0, 3), (196, 176, 130), 3.8, sp=6)
    nave = [(-150, -6), (-150, -200), (-120, -230), (60, -230), (60, -6)]
    ops += forma(nave, ADOBE, 5.4, peso=0.6, sp=10)
    ops += forma(curva([(-150, -200), (-110, -250), (-46, -270), (14, -250), (60, -214)], 6).tolist() + [(60, -200), (-150, -200)], (226, 184, 140), 4.4, sp=6)
    ops += forma(rect(60, -320, 150, -6, 3), ADOBE, 5.2, sp=9)
    ops += forma(curva([(84, -300), (84, -268), (105, -250)], 4).tolist() + curva([(105, -250), (126, -268), (126, -300)], 4).tolist(), (96, 70, 50), 3.6, sp=3)
    ops += forma(curva([(88, -296), (88, -278), (105, -270), (122, -278), (122, -296)], 4), ORO_US, 3.4, sp=3)
    ops += forma(curva([(52, -320), (105, -352), (158, -320)], 5), (226, 184, 140), 4.4, sp=5)
    ops += [T(linea((105, -352), (105, -404)), 5.0, peso=0.03), T(linea((88, -386), (122, -386)), 5.0, peso=0.03)]
    ops += forma(curva([(-80, -6), (-80, -120), (-46, -150), (-12, -120), (-12, -6)], 5), MADERA_OSC_US, 4.4, sp=6)
    ops += [rayita(-46, -146, -46, -8, 2.4)]
    for k in range(5):
        ops += [rayita(-76, -110 + 22 * k, -16, -110 + 22 * k, 1.8)]
    ops += forma(circ(-46, -186, 14, n=14), (96, 70, 50), 3.2, sp=3)
    for k in range(6):
        ops += forma(circ(-140 + 36 * k, -218, 6, n=8), MADERA_US, 2.2, sp=2)
    for x in (90, 120):
        ops += forma(curva([(x - 10, -100), (x - 10, -140), (x, -152), (x + 10, -140), (x + 10, -100)], 3), (96, 70, 50), 2.8, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def fuerte_jamestown():
    """Fuerte de Jamestown (1607): empalizada triangular de troncos con baluartes redondos, casas dentro y la cruz de San Jorge."""
    ops = []
    fl = [([(0, 0), (1, 0), (1, 1), (0, 1)], BLANCO_US), ([(0.42, 0), (0.58, 0), (0.58, 1), (0.42, 1)], ROJO_US),
          ([(0, 0.38), (1, 0.38), (1, 0.62), (0, 0.62)], ROJO_US)]
    bd, m = _bandera(fl, ancho=100, alto=66, asta=330, amp=6)
    ops += colocar(bd, 40, 0, 1.0)
    for x, y, s in ((-70, -96, 0.8), (40, -104, 0.9), (110, -84, 0.6)):
        ops += forma(rect(x - 34 * s, y - 50 * s, x + 34 * s, y, 2), (186, 150, 108), 3.6, sp=5)
        ops += forma(pol((x - 44 * s, y - 46 * s), (x, y - 92 * s), (x + 44 * s, y - 46 * s)), PAJA, 3.8, sp=5)
        ops += forma(rect(x - 8 * s, y - 28 * s, x + 8 * s, y, 1), NEGRO_US, 2.4, sp=2)
    ops += forma(curva([(-210, -40), (0, 2), (210, -40), (210, -30), (0, 12), (-210, -30)], 4, cerrado=True), (150, 150, 96), 3.0, sp=5)
    for lado in (-1, 1):
        for k in range(14):
            u = k / 13
            x = lado * (8 + 180 * u)
            yb = -2 - 40 * u
            alto = 100 - 22 * u
            ops += forma(pol((x - 7, yb), (x - 7, yb - alto), (x, yb - alto - 14), (x + 7, yb - alto), (x + 7, yb)), MADERA_US if k % 2 else MADERA_OSC_US, 2.8, sp=2)
    for x, y, r in ((0, -4, 30), (-196, -42, 24), (196, -42, 24)):
        ops += forma(curva([(x - r, y), (x - r, y - 100), (x, y - 118), (x + r, y - 100), (x + r, y)], 4), MADERA_OSC_US, 4.0, sp=5)
        for k in range(3):
            ops += [rayita(x - r + 8 + k * r * 0.7, y - 6, x - r + 8 + k * r * 0.7, y - 100, 2.0)]
    return Dib(ops)


@lru_cache(maxsize=None)
def planta_tabaco():
    """Planta de tabaco: tallo alto, grandes hojas anchas y flores rosas arriba."""
    ops = [T(linea((0, 0), (0, -330)), 6.4, peso=0.08)]
    for y, lado, L in ((-50, -1, 130), (-80, 1, 136), (-130, -1, 118), (-170, 1, 110), (-215, -1, 92), (-250, 1, 78)):
        P = curva([(0, y), (lado * L * 0.4, y - 46), (lado * L, y - 30), (lado * L * 0.8, y + 14), (lado * L * 0.3, y + 16)], 6, cerrado=True)
        ops += forma(P, TABACO, 4.4, sp=7)
        ops += [T(curva([(0, y), (lado * L * 0.5, y - 18), (lado * L * 0.9, y - 18)], 5), 2.6, peso=0.02)]
    for dx, dy in ((-24, -340), (0, -356), (22, -342), (-10, -322), (14, -318)):
        ops += forma(pol((dx - 8, dy + 14), (dx - 12, dy - 6), (dx, dy - 2), (dx + 12, dy - 6), (dx + 8, dy + 14)), (226, 132, 160), 2.8, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def barril_tabaco():
    """Tonel (hogshead) de tabaco de Virginia, con duelas, aros y hojas secas asomando."""
    ops = []
    for k in range(6):
        ops += forma(pol((-50 + 18 * k, -230), (-30 + 18 * k, -290), (-20 + 18 * k, -230)), (176, 136, 66), 3.0, sp=3)
    cuerpo = curva([(-100, -4), (-122, -120), (-100, -236), (100, -236), (122, -120), (100, -4)], 6)
    ops += forma(cuerpo, MADERA_US, 5.6, peso=0.6, sp=10)
    ops += forma(elip(0, -236, 100, 22, 0, 1.0, 26), MADERA_OSC_US, 4.2, sp=6)
    for k in range(7):
        x = -84 + 28 * k
        ops += [T(curva([(x * 0.84, -8), (x * 1.04, -120), (x * 0.84, -228)], 4), 2.6, peso=0.02)]
    for y in (-40, -84, -160, -204):
        w = 104 + 16 * math.cos((y + 120) / 120 * 1.2)
        ops += forma(rect(-w, y - 7, w, y + 7, 2), HIERRO_US, 3.0, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def cabana_troncos():
    """Cabaña colonial de troncos con chimenea de piedra humeante, dos ventanas y cerca."""
    ops = forma(rect(-200, -10, 200, 0, 3), (150, 160, 100), 3.8, sp=6)
    ops += forma(rect(110, -290, 160, -150, 3), PIEDRA_US, 4.2, sp=6)
    for k in range(5):
        ops += [rayita(112, -270 + 28 * k, 158, -270 + 28 * k, 2.0)]
    ops += forma(circ(120, -320, 20, n=14), (204, 202, 200), 3.0, sp=3) + forma(circ(100, -352, 26, n=14), (204, 202, 200), 3.0, sp=3)
    ops += forma(rect(-150, -170, 130, -6, 3), MADERA_US, 5.2, sp=9)
    for k in range(7):
        y = -18 - 23 * k
        ops += [T(linea((-152, y), (132, y)), 2.6, peso=0.02)]
        ops += forma(circ(-152, y - 10, 10, n=10), MADERA_OSC_US, 2.4, sp=2)
    ops += forma(pol((-176, -164), (-10, -280), (156, -164)), (120, 92, 70), 5.0, sp=8)
    for k in range(6):
        ops += [rayita(-150 + 50 * k, -170, -40 + 30 * k, -250, 2.0)]
    ops += forma(rect(-30, -110, 20, -6, 2), MADERA_OSC_US, 3.8, sp=4)
    for x in (-110, 60):
        ops += forma(rect(x - 22, -126, x + 22, -82, 2), (240, 214, 140), 3.4, sp=3)
        ops += [rayita(x, -126, x, -82, 2.2), rayita(x - 22, -104, x + 22, -104, 2.2)]
    for x in (-196, -176):
        ops += forma(rect(x - 4, -70, x + 4, -6, 1), MADERA_US, 2.6, sp=2)
    ops += [rayita(-198, -56, -150, -56, 2.6), rayita(-198, -30, -150, -30, 2.6)]
    return Dib(ops)


# ------------------------------------------------------------------ REVOLUCIÓN Y REPÚBLICA
@lru_cache(maxsize=None)
def cofre_te():
    """Cofre de té de madera (Motín del té de Boston) con su sello de la compañía y hojas derramadas."""
    ops = forma(pol((-130, -6), (100, -6), (150, -46), (150, -226), (-80, -226), (-130, -186)), MADERA_US, 5.4, peso=0.5, sp=9)
    ops += forma(pol((-130, -186), (-80, -226), (150, -226), (100, -186)), (196, 146, 96), 4.4, sp=6)
    ops += forma(pol((100, -6), (150, -46), (150, -226), (100, -186)), MADERA_OSC_US, 4.4, sp=6)
    ops += [T(linea((-130, -186), (100, -186), (100, -6)), 4.0, peso=0.03)]
    for y in (-50, -140):
        ops += [rayita(-128, y, 98, y, 2.2)]
    ops += forma(circ(-14, -96, 34, n=20), ROJO_US, 3.8, sp=4)
    ops += forma(_estrella(-14, -96, 18), ROJO_OSC_US, 2.4, sp=2)
    for k in range(4):
        ops += [rayita(-110, -170 + 12 * k, -60, -170 + 12 * k, 2.0)]
    for dx, dy, a in ((-160, -8, 0.4), (-180, -18, -0.5), (-150, -26, 1.2), (130, -6, 0.2), (170, -10, -0.8)):
        ops += forma(elip(dx, dy, 14, 6, a, 1.0, 12), (96, 104, 56), 2.4, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def sello_timbre():
    """Estampilla roja de la Ley del Timbre (1765), con borde dentado y la corona del rey."""
    P = []
    for k in range(64):
        a = k / 64
        if a < 0.25:
            x, y = -110 + 880 * a, -290
        elif a < 0.5:
            x, y = 110, -290 + 1120 * (a - 0.25)
        elif a < 0.75:
            x, y = 110 - 880 * (a - 0.5), -10
        else:
            x, y = -110, -10 - 1120 * (a - 0.75)
        rr = 6 if k % 2 else 0
        P.append((x + (rr if x == -110 else -rr if x == 110 else 0), y + (rr if y == -290 else -rr if y == -10 else 0)))
    ops = forma(P, BLANCO_US, 4.6, peso=0.5, sp=8)
    ops += forma(rect(-88, -268, 88, -32, 4), ROJO_US, 4.0, sp=6)
    ops += forma(circ(0, -150, 64, n=28), BLANCO_US, 3.6, sp=4)
    cor = [(-40, -126), (-46, -176), (-24, -156), (0, -190), (24, -156), (46, -176), (40, -126)]
    ops += forma(cor, ROJO_OSC_US, 3.4, sp=3)
    ops += forma(rect(-42, -128, 42, -114, 2), ROJO_OSC_US, 3.0, sp=2)
    for k in range(3):
        ops += [rayita(-60, -64 + 10 * k * 0, 60, -64, 2.0)] if k == 0 else []
    ops += [rayita(-60, -250, 60, -250, 2.4), rayita(-50, -60, 50, -60, 2.4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mosquete():
    """Mosquete de chispa (Brown Bess / mosquete continental) apoyado de culata, con baqueta y llave de chispa."""
    a = math.radians(14)
    c, s = math.cos(a), math.sin(a)

    def rot(P):
        return [(x * c - y * s, x * s + y * c) for x, y in P]
    ops = forma(rot([(-40, 0), (-26, -100), (-8, -128), (6, -128), (10, -100), (0, -6)]), MADERA_US, 4.8, sp=6)
    ops += forma(rot([(-6, -128), (-2, -320), (10, -320), (8, -128)]), MADERA_US, 4.2, sp=5)
    ops += forma(rot([(-2, -300), (0, -400), (8, -400), (10, -300)]), ACERO, 4.0, sp=4)
    ops += [T(np.array(rot([(14, -140), (16, -392)])), 2.6, peso=0.02)]
    ops += forma(rot([(-14, -140), (14, -140), (14, -168), (-14, -168)]), ACERO_OSC, 3.4, sp=3)
    ops += [T(np.array(rot([(14, -160), (26, -182), (20, -192)])), 3.4, peso=0.02)]
    ops += [T(np.array(rot([(-2, -380), (-2, -394)])), 5.0, peso=0.02)]
    for y in (-210, -270):
        ops += forma(rot([(-6, y), (12, y), (12, y - 8), (-6, y - 8)]), LATON, 2.4, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def canon_rev():
    """Cañón de bronce de la Revolución sobre cureña de madera, con balas apiladas."""
    ops = forma(pol((-150, -20), (-40, -84), (10, -84), (-110, -4)), MADERA_US, 4.6, sp=6)
    ops += forma(pol((-120, -80), (150, -126), (156, -96), (-110, -46)), BRONCE, 5.2, peso=0.5, sp=8)
    ops += forma(circ(-124, -64, 16, n=12), BRONCE, 3.6, sp=3)
    for x in (-40, 40, 110):
        ops += [T(linea((x, -94 - (x + 120) * 0.17 + 14), (x + 4, -64 - (x + 120) * 0.17 + 14)), 3.0, peso=0.02)]
    ops += _rueda(-30, -50, 48, 0, MADERA_OSC_US, 10)
    for x, y in ((90, -18), (126, -18), (108, -48)):
        ops += forma(circ(x, y, 18, n=14), HIERRO_US, 3.4, sp=3)
    return Dib(ops)


def _pergamino(ancho, alto, col=PERGAMINO):
    x0, x1 = -ancho / 2, ancho / 2
    ops = forma(curva([(x0, -18), (x0 + 6, -alto * 0.5), (x0, -alto + 18), (x1, -alto + 18), (x1 - 6, -alto * 0.5), (x1, -18)], 5, cerrado=True),
                col, 5.0, peso=0.5, sp=9)
    for y in (-alto + 18, -18):
        ops += forma(elip(0, y, ancho / 2 + 10, 16, 0, 1.0, 26), (226, 206, 160), 4.2, sp=5)
        ops += forma(circ(x0 - 8, y, 12, n=12), (226, 206, 160), 3.4, sp=3) + forma(circ(x1 + 8, y, 12, n=12), (226, 206, 160), 3.4, sp=3)
    return ops


@lru_cache(maxsize=None)
def declaracion():
    """Declaración de Independencia: pergamino con el texto en renglones y las firmas (la de Hancock, grande)."""
    ops = _pergamino(250, 360)
    ops += [T(curva([(-96, -312), (-60, -322), (-20, -308), (20, -322), (60, -310), (96, -318)], 5), 5.6, peso=0.03)]
    for k in range(11):
        y = -282 + 15 * k
        w = 100 - (8 if k % 3 == 2 else 0)
        ops += [T(ondas(-w, w - (30 if k == 10 else 0), y, 1.6, 14), 2.0, peso=0.02)]
    ops += [T(curva([(-100, -96), (-70, -112), (-40, -84), (-10, -110), (20, -88), (60, -104), (94, -94), (40, -78), (-60, -80)], 6), 4.0, peso=0.03)]
    for k in range(4):
        for j in range(3):
            x = -96 + 64 * k
            y = -64 + 13 * j
            ops += [T(ondas(x, x + 44, y, 2.2, 10), 2.0, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def constitucion():
    """La Constitución (1787): pergamino con el gran encabezado caligráfico y los artículos en columnas."""
    ops = _pergamino(270, 370)
    ops += [T(curva([(-110, -300), (-96, -330), (-80, -296), (-62, -326), (-46, -298), (-24, -318), (-6, -300)], 6), 7.0, peso=0.04),
            T(curva([(10, -300), (26, -328), (44, -298), (64, -322), (82, -296), (100, -318), (112, -302)], 6), 7.0, peso=0.04)]
    for col in (-1, 1):
        x0 = -110 if col < 0 else 8
        for k in range(14):
            y = -268 + 15 * k
            if k in (0, 6, 10):
                ops += [T(linea((x0, y), (x0 + 50, y)), 3.6, peso=0.02)]
            else:
                ops += [T(ondas(x0, x0 + 98, y, 1.4, 12), 1.8, peso=0.02)]
    ops += forma(circ(96, -54, 16, n=14), CERA, 3.0, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def pluma_tintero():
    """Tintero de cristal con la pluma de ave."""
    ops = forma(curva([(-60, -4), (-70, -50), (-50, -96), (-30, -110), (30, -110), (50, -96), (70, -50), (60, -4)], 5), (70, 78, 96), 5.0, sp=8)
    ops += forma(rect(-30, -132, 30, -106, 4), (90, 96, 112), 4.0, sp=4)
    ops += [T(curva([(-40, -60), (-20, -86)], 3), 3.0, peso=0.02)]
    pl = curva([(0, -110), (40, -200), (96, -300), (150, -380), (120, -300), (84, -220), (30, -140)], 6, cerrado=True)
    ops += forma(pl, BLANCO_US, 4.4, sp=6)
    ops += [T(curva([(4, -116), (60, -230), (146, -376)], 6), 3.0, peso=0.02)]
    for k in range(6):
        y = -170 - 30 * k
        x = 30 + 20 * k
        ops += [rayita(x, y, x + 24, y - 6, 1.8)]
    return Dib(ops)


@lru_cache(maxsize=None)
def campana_libertad():
    """La Campana de la Libertad (Filadelfia) colgada de su yugo de madera, con la famosa grieta."""
    ops = forma(rect(-130, -360, 130, -320, 6), MADERA_OSC_US, 4.8, sp=6)
    ops += forma(rect(-24, -324, 24, -296, 4), BRONCE_OSC, 3.8, sp=3)
    cuerpo = curva([(-150, -14), (-128, -40), (-104, -120), (-90, -220), (-60, -286), (0, -300), (60, -286), (90, -220), (104, -120), (128, -40), (150, -14)], 6)
    ops += forma(np.vstack([cuerpo, [(0, -6)]]), (150, 116, 84), 6.0, peso=0.7, sp=11)
    ops += forma(elip(0, -14, 150, 18, 0, 1.0, 30), (120, 92, 66), 4.4, sp=6)
    ops += [T(curva([(-88, -236), (0, -244), (88, -236)], 6), 3.0, peso=0.02), T(curva([(-96, -206), (0, -214), (96, -206)], 6), 3.0, peso=0.02)]
    for k in range(9):
        x = -80 + 20 * k
        ops += [rayita(x, -230 + abs(k - 4) * 0.6, x + 12, -230 + abs(k - 4) * 0.6, 2.0)]
    grieta = [(-16, -6), (-8, -40), (-24, -70), (-12, -104), (-26, -134), (-14, -166)]
    ops += [T(np.array(grieta), 6.0, peso=0.04), T(np.array([(-24, -70), (-40, -84)]), 3.2, peso=0.02)]
    ops += [T(curva([(-110, -110), (-96, -60)], 3), 3.0, peso=0.02)]
    return Dib(ops)


def _franjas(n=13, v0=0.0, u0=0.0):
    regs = []
    for k in range(n):
        if k % 2 == 0:
            regs.append(([(u0, k / n), (1, k / n), (1, (k + 1) / n), (u0, (k + 1) / n)], ROJO_US))
    return regs


@lru_cache(maxsize=None)
def bandera_13():
    """Bandera de Betsy Ross (1777): 13 franjas y 13 estrellas en círculo sobre azul."""
    regs = [([(0, 0), (1, 0), (1, 1), (0, 1)], BLANCO_US)] + _franjas() + [([(0, 0), (0.42, 0), (0.42, 7 / 13), (0, 7 / 13)], AZUL_US)]
    ops, m = _bandera(regs, ancho=250, alto=160)
    for k in range(13):
        a = k * 2 * math.pi / 13
        u, v = 0.21 + 0.13 * math.cos(a), 3.5 / 13 + 0.19 * math.sin(a)
        x, y = m([(u, v)])[0]
        ops += [R(_estrella(x, y, 8), BLANCO_US, peso=0.01, sp=2, off=(0, 0))]
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera_union():
    """Bandera de la Unión en la Guerra Civil (1861): 13 franjas y 34 estrellas."""
    regs = [([(0, 0), (1, 0), (1, 1), (0, 1)], BLANCO_US)] + _franjas() + [([(0, 0), (0.42, 0), (0.42, 7 / 13), (0, 7 / 13)], AZUL_US)]
    ops, m = _bandera(regs, ancho=250, alto=160)
    filas = (7, 7, 6, 7, 7)
    for j, nf in enumerate(filas):
        for i in range(nf):
            u = 0.04 + (0.34 if nf == 7 else 0.30) * i / (nf - 1) + (0.02 if nf == 6 else 0)
            v = 0.06 + 0.11 * j
            x, y = m([(u, v)])[0]
            ops += [R(_estrella(x, y, 5.5), BLANCO_US, peso=0.01, sp=2, off=(0, 0))]
    return Dib(ops)


@lru_cache(maxsize=None)
def salon_independencia():
    """Independence Hall (Filadelfia): edificio georgiano de ladrillo con ventanas blancas y torre del reloj con chapitel."""
    ops = forma(rect(-210, -12, 210, 0, 3), (150, 160, 100), 3.8, sp=6)
    ops += forma(rect(-200, -170, 200, -8, 3), LADRILLO, 5.4, peso=0.6, sp=10)
    ops += forma(pol((-210, -170), (-190, -196), (190, -196), (210, -170)), (110, 84, 72), 4.2, sp=5)
    for fila, y in enumerate((-150, -80)):
        for k in range(8):
            x = -176 + 50 * k
            if fila == 1 and k in (3, 4):
                continue
            ops += forma(rect(x - 12, y, x + 12, y + 44, 2), BLANCO_US, 3.0, sp=3)
            ops += [rayita(x, y, x, y + 44, 1.6), rayita(x - 12, y + 22, x + 12, y + 22, 1.6)]
    ops += forma(curva([(-24, -8), (-24, -60), (0, -78), (24, -60), (24, -8)], 4), (240, 236, 222), 3.8, sp=4)
    ops += forma(rect(-46, -280, 46, -170, 3), LADRILLO, 4.8, sp=7)
    ops += forma(rect(-36, -330, 36, -280, 3), BLANCO_US, 4.2, sp=5)
    ops += forma(circ(0, -305, 18, n=16), BLANCO_US, 3.4, sp=3)
    ops += [T(linea((0, -305), (0, -317)), 2.6, peso=0.02), T(linea((0, -305), (9, -305)), 2.6, peso=0.02)]
    ops += forma(rect(-28, -370, 28, -330, 3), BLANCO_US, 4.0, sp=4)
    ops += forma(rect(-20, -400, 20, -370, 3), BLANCO_US, 3.8, sp=4)
    ops += forma(pol((-14, -400), (0, -450), (14, -400)), (226, 214, 190), 3.6, sp=3)
    ops += forma(curva([(-26, -224), (-26, -250), (0, -262), (26, -250), (26, -224)], 4), BLANCO_US, 3.0, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def corona_britanica():
    """Corona de San Eduardo: aro de oro con joyas, arcos, gorro púrpura, cruz y armiño."""
    ops = forma(curva([(-130, -150), (-110, -240), (-60, -280), (0, -290), (60, -280), (110, -240), (130, -150)], 6), (128, 60, 120), 4.8, sp=8)
    for sx in (-1, 1):
        ops += forma(_tubo([(sx * 126, -140), (sx * 116, -240), (sx * 60, -292), (0, -296)], 22, 16), ORO_US, 4.0, sp=4)
    ops += forma(_tubo([(0, -140), (0, -296)], 22, 18), ORO_US, 4.0, sp=4)
    ops += forma(circ(0, -310, 20, n=16), ORO_US, 3.8, sp=3)
    ops += forma(pol((-8, -330), (-8, -350), (-22, -350), (-22, -364), (-8, -364), (-8, -380), (8, -380), (8, -364), (22, -364), (22, -350),
                     (8, -350), (8, -330)), ORO_US, 3.4, sp=3)
    ops += forma(rect(-140, -150, 140, -84, 6), ORO_US, 5.2, peso=0.5, sp=8)
    for k, col in enumerate((ROJO_US, VERDE_US, AZUL_US, ROJO_US, VERDE_US)):
        ops += forma(elip(-100 + 50 * k, -117, 12, 16, 0, 1.0, 12), col, 3.2, sp=3)
    ops += forma(rect(-150, -86, 150, -30, 10), BLANCO_US, 4.6, sp=6)
    for k in range(9):
        ops += [R(pol((-128 + 32 * k, -66), (-122 + 32 * k, -48), (-116 + 32 * k, -66)), NEGRO_US, peso=0.01, sp=2, off=(0, 0))]
    return Dib(ops)


# ------------------------------------------------------------------ EXPANSIÓN AL OESTE
@lru_cache(maxsize=None)
def bolsa_dolares():
    """Saco de dinero atado con el signo del dólar (la compra de Luisiana, 15 millones)."""
    ops = forma(curva([(-40, -230), (-60, -260), (-30, -270), (0, -252), (30, -270), (60, -260), (40, -230)], 5), (204, 172, 116), 4.2, sp=5)
    cuerpo = curva([(-40, -222), (-120, -150), (-140, -60), (-100, -6), (100, -6), (140, -60), (120, -150), (40, -222)], 6)
    ops += forma(cuerpo, (204, 172, 116), 5.6, peso=0.6, sp=10)
    ops += forma(rect(-48, -236, 48, -216, 4), CUERO_OSC, 3.8, sp=3)
    ops += [T(curva([(46, -142), (20, -158), (-30, -150), (-40, -118), (-10, -100), (30, -90), (46, -60), (30, -36), (-20, -34), (-48, -52)], 6), 10.0, peso=0.05),
            T(linea((0, -172), (0, -18)), 8.0, peso=0.04)]
    for x, y in ((-150, -10), (-118, -14), (150, -10)):
        ops += forma(elip(x, y, 22, 9, 0, 1.0, 16), ORO_US, 3.0, sp=3)
    return Dib(ops)


def _remero(pose, ropa, gorro_col, dx, fase):
    p = persona(ropa, PIEL_A, None, "serio", (40 + 18 * _paso(pose, fase), 70 - 20 * _paso(pose, fase)), 0, traje="corta")
    ops = colocar(list(p.ops), dx, -40, 0.5)
    cy = -40 + 0.5 * -215
    ops += forma(curva([(dx - 22, cy - 2), (dx - 20, cy - 24), (dx, cy - 30), (dx + 20, cy - 24), (dx + 22, cy - 2)], 4), gorro_col, 3.4, sp=3)
    ops += forma(_tubo([(dx - 20, cy - 8), (dx - 38, cy + 6), (dx - 44, cy + 26)], 9, 6), gorro_col, 2.6, sp=2)
    a = 0.5 * _paso(pose, fase)
    hx, hy = dx + 26, cy + 56
    ops += [T(linea((hx - 30 * math.sin(a) - 10, hy - 50), (hx + 30 * math.sin(a) + 10, hy + 70)), 4.4, peso=0.03)]
    ops += forma(elip(hx + 30 * math.sin(a) + 14, hy + 84, 8, 20, -0.3, 1.0, 12), MADERA_US, 2.8, sp=2)
    return ops


def canoa_lc(pose=0):
    """Canoa de la expedición de Lewis y Clark con dos remeros de gorro de piel (4 poses)."""
    dy = 3 * math.sin(pose * math.pi / 2)
    ops = _remero(pose, GAMUZA, (110, 80, 56), -60, 0.0) + _remero(pose, (110, 120, 86), (96, 70, 50), 50, 0.6)
    ops = colocar(ops, 0, dy, 1.0)
    casco = curva([(-200, -60 + dy), (-160, -4 + dy), (150, -4 + dy), (204, -64 + dy), (150, -40 + dy), (-150, -40 + dy)], 6, cerrado=True)
    ops += forma(casco, MADERA_US, 5.0, sp=7)
    ops += [T(curva([(-176, -40 + dy), (0, -32 + dy), (178, -46 + dy)], 5), 2.6, peso=0.02)]
    ops += forma(rect(-10, -64 + dy, 30, -40 + dy, 3), (150, 120, 80), 3.0, sp=3)
    ops += _olas(210, 4, pose)
    return Dib(ops)


def _buey(pose, x0, col, ph=0.0):
    ops = []
    patas = ((x0 - 60, -90, 0.0 + ph, True), (x0 + 50, -90, math.pi + ph, True), (x0 - 44, -90, math.pi + ph, False), (x0 + 64, -90, ph, False))
    osc = tuple(int(c * 0.8) for c in col)
    for x, y, a_ph, lejos in patas:
        if lejos:
            a = 14 * _paso(pose, a_ph)
            ops += _pierna(x, y, a, a * 0.5 - 4, osc, 44, 42, 12, 8)
    ops += forma(curva([(x0 - 90, -100), (x0 - 92, -150), (x0 - 40, -170), (x0 + 60, -172), (x0 + 96, -150), (x0 + 96, -98), (x0 + 40, -80),
                        (x0 - 50, -80)], 5, cerrado=True), col, 5.0, sp=8)
    ops += forma(curva([(x0 + 86, -150), (x0 + 130, -146), (x0 + 142, -114), (x0 + 124, -96), (x0 + 96, -108)], 4, cerrado=True), col, 4.4, sp=5)
    ops += forma(_tubo([(x0 + 104, -146), (x0 + 112, -172), (x0 + 128, -178)], 8, 3), MARFIL, 2.6, sp=2)
    ops += [punto(x0 + 120, -130, 6)]
    ops += forma(rect(x0 + 74, -186, x0 + 92, -140, 3), MADERA_OSC_US, 3.2, sp=2)
    for x, y, a_ph, lejos in patas:
        if not lejos:
            a = 14 * _paso(pose, a_ph)
            ops += _pierna(x, y, a, a * 0.5 - 4, col, 44, 42, 13, 9)
    return ops


def carreta_cubierta(pose=0):
    """Carreta Conestoga de lona blanca tirada por bueyes, camino del oeste (4 poses)."""
    ops = _buey(pose, 170, (140, 96, 62), 0.0)
    ops += [T(linea((40, -110), (186, -150)), 4.4, peso=0.03)]
    ops += forma(curva([(-170, -100), (-186, -150), (-150, -146), (100, -146), (130, -150), (118, -100)], 5, cerrado=True), AZUL_US, 5.0, sp=8)
    lona = curva([(-178, -146), (-200, -230), (-160, -280), (-60, -296), (40, -296), (110, -280), (140, -232), (126, -146)], 6)
    ops += forma(lona, LONA, 5.4, peso=0.5, sp=9)
    for k in range(5):
        x = -150 + 62 * k
        ops += [T(curva([(x - 6, -148), (x - 4, -240), (x + 4, -292)], 4), 2.6, peso=0.02)]
    ops += _rueda(-120, -70, 62, pose, (196, 70, 60), 12)
    ops += _rueda(70, -60, 52, pose, (196, 70, 60), 10)
    ops += _buey(pose, 290, (176, 130, 90), 0.8)
    return Dib(ops)


_GALOPE = [((-30, 8), (24, -6), (40, 22), (-12, -34)), ((-12, -30), (36, 10), (12, -34), (32, 14)),
           ((26, -10), (-30, 8), (-16, -36), (40, 22)), ((36, 10), (-12, -30), (32, 14), (12, -34))]


def caballo_us(pose=0, col=(150, 98, 60), crin=(56, 40, 34)):
    """Caballo de la frontera ensillado, al galope (4 poses)."""
    p = _GALOPE[pose % 4]
    osc = tuple(int(c * 0.78) for c in col)
    patas = ((-80, -124), (-96, -124), (70, -124), (88, -124))
    ops = []
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if lejos:
            ops += _pierna(x, y, a1, a2, osc, 60, 60, 15, 9)
    ops += forma(_tubo([(-110, -158), (-150, -150), (-176, -110), (-180, -78)], 26, 12), crin, 4.0, sp=5)
    ops += forma(elip(-6, -152, 118, 46, 0.0, 1.0, 36), col, 5.6, peso=0.6, sp=10)
    cuello = [(56, -176), (90, -222), (124, -262), (156, -282), (186, -270), (204, -232), (198, -214), (176, -218), (152, -232), (130, -200), (104, -140)]
    ops += forma(curva(cuello, 6, cerrado=True), col, 5.2, peso=0.4, sp=8)
    ops += forma(curva([(118, -256), (92, -230), (66, -190), (54, -172), (80, -184), (104, -216), (132, -256)], 5, cerrado=True), crin, 3.8, sp=5)
    ops += forma(pol((148, -276), (156, -306), (166, -278)), col, 3.4, sp=3)
    ops += [punto(170, -252, 8), punto(198, -224, 5)]
    ops += [T(linea((196, -228), (150, -210), (110, -186)), 3.0, peso=0.02)]
    ops += forma(curva([(-44, -196), (-30, -212), (30, -212), (44, -196), (40, -168), (-40, -168)], 4, cerrado=True), CUERO_OSC, 4.2, sp=5)
    ops += forma(rect(-30, -170, 20, -110, 4), (176, 64, 56), 3.6, sp=4)
    ops += [T(linea((0, -170), (0, -96)), 3.0, peso=0.02)]
    ops += forma(rect(-8, -100, 10, -88, 2), ACERO, 2.4, sp=2)
    for (x, y), (a1, a2), lejos in zip(patas, p, (True, False, True, False)):
        if not lejos:
            ops += _pierna(x, y, a1, a2, col, 60, 60, 16, 10)
    return Dib(ops)


@lru_cache(maxsize=None)
def el_alamo():
    """La misión del Álamo (San Antonio): fachada de piedra caliza con el remate curvo, portón arqueado, columnas y hornacinas."""
    caliza = (226, 214, 186)
    ops = forma(rect(-210, -10, 210, 0, 3), (196, 176, 130), 3.8, sp=6)
    fach = [(-180, -6), (-180, -230), (-110, -230), (-84, -262), (-50, -268), (-30, -300), (0, -312), (30, -300), (50, -268), (84, -262),
            (110, -230), (180, -230), (180, -6)]
    ops += forma(curva(fach, 4), caliza, 5.6, peso=0.6, sp=10)
    ops += [T(linea((-180, -150), (180, -150)), 3.0, peso=0.02)]
    ops += forma(curva([(-40, -8), (-40, -100), (0, -136), (40, -100), (40, -8)], 5), MADERA_OSC_US, 4.4, sp=6)
    ops += [rayita(0, -132, 0, -8, 2.4)]
    for sx in (-1, 1):
        for x in (sx * 62, sx * 100):
            ops += forma(rect(x - 7, -146, x + 7, -8, 2), (236, 228, 206), 3.0, sp=2)
        ops += forma(curva([(sx * 81 - 14, -60), (sx * 81 - 14, -110), (sx * 81, -122), (sx * 81 + 14, -110), (sx * 81 + 14, -60)], 3), (150, 132, 108), 2.8, sp=2)
        ops += forma(curva([(sx * 81 - 12, -170), (sx * 81 - 12, -204), (sx * 81, -214), (sx * 81 + 12, -204), (sx * 81 + 12, -170)], 3), (150, 132, 108), 2.6, sp=2)
        ops += forma(rect(sx * 150 - 16, -200, sx * 150 + 16, -160, 2), (90, 74, 60), 2.8, sp=2)
    ops += forma(rect(-26, -214, 26, -176, 2), (90, 74, 60), 3.0, sp=2)
    for k in range(6):
        ops += [rayita(-170 + 20 * k, -40 - 18 * (k % 2), -150 + 20 * k, -40 - 18 * (k % 2), 1.8)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tratado_1848():
    """Tratado de Guadalupe Hidalgo (1848): hoja con el texto, dos firmas y el sello de lacre con cinta."""
    ops = forma(pol((-120, -8), (-126, -330), (110, -340), (124, -14)), PERGAMINO, 5.0, peso=0.5, sp=9)
    ops += forma(pol((110, -340), (124, -300), (84, -306)), (214, 196, 156), 3.2, sp=3)
    ops += [T(linea((-80, -300), (60, -304)), 4.4, peso=0.03)]
    for k in range(10):
        y = -272 + 17 * k
        ops += [T(ondas(-96, 96 - (40 if k == 9 else 0), y, 1.5, 13), 1.9, peso=0.02)]
    ops += [T(curva([(-100, -86), (-80, -100), (-58, -76), (-36, -96), (-14, -80)], 5), 3.4, peso=0.02),
            T(curva([(10, -84), (30, -102), (52, -78), (74, -98), (96, -82)], 5), 3.4, peso=0.02)]
    ops += forma(pol((38, -40), (20, 30), (36, 22), (46, 40), (52, -30)), (60, 120, 80), 2.8, sp=2)
    ops += forma(pol((64, -40), (84, 26), (68, 20), (60, 38), (50, -30)), (60, 120, 80), 2.8, sp=2)
    ops += forma(curva([(50, -80), (80, -70), (86, -40), (64, -18), (34, -24), (22, -52), (32, -76)], 4, cerrado=True), CERA, 4.0, sp=4)
    ops += forma(_estrella(54, -48, 14), (150, 30, 34), 2.4, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def batea_oro():
    """Batea de buscador de oro con agua, grava y pepitas brillantes."""
    ops = forma(curva([(-180, -70), (-150, -20), (-60, 0), (60, 0), (150, -20), (180, -70)], 6).tolist() + [(0, -84)], HIERRO_US, 5.4, sp=8)
    ops += forma(elip(0, -72, 180, 34, 0, 1.0, 36), (110, 112, 120), 4.6, sp=7)
    ops += forma(elip(0, -66, 150, 24, 0, 1.0, 32), AGUA_US, 3.6, sp=6)
    for x, y in ((-90, -64), (-50, -58), (-10, -70), (30, -60), (70, -66), (100, -60)):
        ops += forma(circ(x, y, 6, n=8), (150, 140, 124), 2.0, sp=2)
    for x, y, r in ((-30, -68, 13), (16, -62, 10), (54, -72, 15), (-70, -60, 9)):
        ops += forma(curva([(x - r, y), (x - r * 0.4, y - r * 0.9), (x + r * 0.6, y - r * 0.7), (x + r, y + r * 0.2), (x, y + r * 0.6)], 3, cerrado=True), ORO_US, 2.8, sp=2)
    ops += _destellos(54, -96, 14, 34, 8, 2.6) + _destellos(-30, -100, 10, 24, 6, 2.2)
    return Dib(ops)


@lru_cache(maxsize=None)
def pico_pala():
    """Pico y pala del minero, cruzados."""
    ops = forma(_tubo([(-120, -10), (90, -330)], 16, 14), MADERA_US, 4.2, sp=4)
    ops += forma(curva([(10, -330), (70, -364), (140, -360), (180, -330), (130, -334), (90, -320), (110, -296), (70, -300)], 5, cerrado=True), ACERO, 4.4, sp=4)
    ops += forma(_tubo([(120, -10), (-60, -260)], 14, 12), MADERA_US, 4.2, sp=4)
    ops += forma(curva([(-50, -240), (-110, -300), (-150, -340), (-120, -370), (-70, -340), (-40, -280)], 5, cerrado=True), ACERO, 4.4, sp=4)
    ops += forma(_tubo([(-46, -248), (-66, -276)], 22, 18), ACERO_OSC, 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def campamento_mineros():
    """Campamento de la fiebre del oro: tiendas de lona, fogata humeante, batea y pico."""
    ops = forma(rect(-210, -14, 210, 0, 3), (196, 176, 130), 3.8, sp=6)
    for x, y, s in ((-130, -40, 0.8), (40, -56, 0.7), (140, -20, 1.0)):
        ops += forma(pol((x - 90 * s, y), (x, y - 150 * s), (x + 90 * s, y)), LONA, 4.8, sp=7)
        ops += forma(pol((x - 18 * s, y), (x, y - 100 * s), (x + 18 * s, y)), (96, 82, 66), 3.4, sp=3)
        ops += [T(linea((x, y - 150 * s), (x, y - 166 * s)), 4.0, peso=0.02), T(linea((x - 90 * s, y), (x - 116 * s, y + 8)), 2.2, peso=0.02)]
    fx, fy = -30, -8
    for a in (-0.6, 0.6, 0.0):
        ops += forma(_tubo([(fx - 30 * math.cos(a), fy), (fx + 30 * math.cos(a), fy - 10)], 10, 10), MADERA_OSC_US, 2.8, sp=2)
    ops += forma(pol((fx - 20, fy - 6), (fx - 8, fy - 46), (fx, fy - 22), (fx + 10, fy - 58), (fx + 22, fy - 6)), (240, 150, 60), 3.0, sp=3)
    ops += forma(circ(fx - 6, fy - 90, 16, n=12), (204, 202, 200), 2.6, sp=2) + forma(circ(fx - 22, fy - 124, 22, n=12), (204, 202, 200), 2.6, sp=2)
    ops += forma(elip(-200 + 30, -20, 34, 10, 0, 1.0, 16), HIERRO_US, 3.0, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def planta_algodon():
    """Planta de algodón con las cápsulas abiertas, blancas y esponjosas."""
    ops = [T(curva([(0, 0), (-4, -120), (6, -240)], 5), 6.0, peso=0.06)]
    ramas = [((0, -70), (-110, -150)), ((0, -100), (110, -170)), ((-2, -150), (-90, -240)), ((2, -180), (96, -260)), ((4, -230), (10, -300))]
    for (a, b) in ramas:
        ops += [T(curva([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 10), b], 4), 4.2, peso=0.03)]
    for x, y, a in ((-60, -100, -0.6), (70, -130, 0.6), (-40, -210, -0.4), (50, -220, 0.5)):
        ops += forma(elip(x, y, 28, 12, a, 1.0, 14), VERDE_HOJA, 3.0, sp=3)
    for (a, b) in ramas:
        x, y = b
        ops += forma(pol((x - 22, y + 18), (x, y + 30), (x + 22, y + 18), (x + 6, y + 6), (x - 6, y + 6)), (130, 90, 56), 2.6, sp=2)
        for dx, dy in ((-18, -4), (16, -6), (0, -24), (-6, 8), (12, 10)):
            ops += forma(circ(x + dx, y + dy, 17, n=14), ALGODON, 3.0, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def fardo_algodon():
    """Fardo de algodón en arpillera con flejes de hierro y copos asomando."""
    ops = forma(pol((-140, -6), (120, -6), (160, -40), (160, -220), (-100, -220), (-140, -186)), (210, 192, 150), 5.4, peso=0.5, sp=9)
    ops += forma(pol((-140, -186), (-100, -220), (160, -220), (120, -186)), (228, 214, 180), 4.0, sp=6)
    ops += forma(pol((120, -6), (160, -40), (160, -220), (120, -186)), (184, 164, 124), 4.0, sp=6)
    for x in (-90, -20, 50):
        ops += forma(pol((x - 6, -6), (x + 6, -6), (x + 6, -186), (x + 40, -220), (x + 28, -220), (x - 6, -186)), HIERRO_US, 2.8, sp=2)
    for k in range(10):
        ops += [rayita(-130 + 25 * k, -170 + 13 * (k % 4), -120 + 25 * k, -150 + 13 * (k % 4), 1.6)]
    for x, y in ((-140, -100), (-136, -50), (160, -150), (160, -96), (-20, -222), (90, -222)):
        for dx, dy in ((-10, 0), (10, -4), (0, -14)):
            ops += forma(circ(x + dx, y + dy, 13, n=12), ALGODON, 2.6, sp=2)
        ops += [R(circ(x, y - 2, 8, n=10), (214, 210, 200), peso=0.01, sp=2, off=(0, 0))]
    return Dib(ops)


@lru_cache(maxsize=None)
def mansion_plantacion():
    """Casa grande de plantación del sur, de estilo neoclásico: pórtico de columnas blancas, frontón y contraventanas verdes."""
    ops = forma(rect(-210, -14, 210, 0, 3), (150, 160, 100), 3.8, sp=6)
    ops += forma(rect(-200, -220, 200, -10, 3), (236, 226, 210), 5.2, peso=0.5, sp=9)
    ops += forma(pol((-214, -220), (-170, -270), (170, -270), (214, -220)), (120, 110, 110), 4.6, sp=6)
    ops += forma(pol((-120, -236), (0, -300), (120, -236)), BLANCO_US, 4.6, sp=6)
    ops += forma(circ(0, -260, 12, n=12), (200, 196, 188), 2.6, sp=2)
    ops += forma(rect(-126, -240, 126, -226, 2), BLANCO_US, 3.6, sp=3)
    for fila, y in enumerate((-196, -110)):
        for x in (-176, -150, 150, 176):
            pass
        for x in (-170, 170):
            ops += forma(rect(x - 16, y, x + 16, y + 56, 2), (120, 140, 160), 3.0, sp=3)
            ops += forma(rect(x - 30, y, x - 18, y + 56, 1), VERDE_OSC_H, 2.4, sp=2) + forma(rect(x + 18, y, x + 30, y + 56, 1), VERDE_OSC_H, 2.4, sp=2)
    ops += [rayita(-196, -130, 196, -130, 3.0)]
    ops += forma(rect(-110, -132, 110, -120, 2), BLANCO_US, 3.0, sp=2)
    ops += forma(rect(-24, -86, 24, -10, 2), MADERA_OSC_US, 3.4, sp=3)
    for k in range(6):
        x = -110 + 44 * k
        ops += forma(rect(x - 9, -226, x + 9, -10, 2), BLANCO_US, 3.8, sp=3)
        ops += [rayita(x - 13, -226, x + 13, -226, 3.0), rayita(x - 13, -12, x + 13, -12, 3.0)]
    return Dib(ops)


def vapor_misisipi(pose=0):
    """Vapor de rueda trasera del Misisipi: cubiertas blancas, dos chimeneas negras con corona y la rueda de paletas roja (4 poses)."""
    dy = 2 * math.sin(pose * math.pi / 2)
    ops = []
    for x in (40, 96):
        ops += _humo(x, -400 + dy, pose, 3, 18)
        ops += forma(rect(x - 12, -380 + dy, x + 12, -150 + dy, 2), NEGRO_US, 4.0, sp=4)
        ops += forma(pol((x - 22, -380 + dy), (x - 14, -400 + dy), (x - 4, -388 + dy), (x + 4, -404 + dy), (x + 14, -388 + dy), (x + 22, -400 + dy), (x + 22, -376 + dy),
                         (x - 22, -376 + dy)), NEGRO_US, 3.4, sp=3)
    ops += forma(pol((-160, -56 + dy), (190, -56 + dy), (220, -84 + dy), (210, -10 + dy), (-150, -10 + dy)), BLANCO_US, 5.2, sp=8)
    ops += [R(rect(-150, -36 + dy, 206, -20 + dy, 2), ROJO_US, peso=0.02, sp=3, off=(1, -1))]
    for k, (x0, x1, y0, y1) in enumerate(((-150, 186, -130, -56), (-110, 150, -196, -130), (-40, 110, -246, -196))):
        ops += forma(rect(x0, y0 + dy, x1, y1 + dy, 2), BLANCO_US, 4.4, sp=6)
        ops += [rayita(x0 - 8, y0 + dy, x1 + 8, y0 + dy, 3.4)]
        for x in np.linspace(x0 + 12, x1 - 12, max(2, int((x1 - x0) / 26))):
            ops += [rayita(x, y0 + 10 + dy, x, y1 - 4 + dy, 1.8)]
    ops += forma(rect(-20, -280 + dy, 50, -246 + dy, 3), BLANCO_US, 3.6, sp=3)
    cx, cy = -186, -64 + dy
    ops += forma(circ(cx, cy, 64, n=28), ROJO_US, 4.8, sp=6)
    for k in range(8):
        a = pose * math.pi / 16 + k * math.pi / 4
        ops += [T(linea((cx, cy), (cx + 62 * math.cos(a), cy + 62 * math.sin(a))), 3.6, peso=0.02)]
    ops += forma(circ(cx, cy, 12, n=12), ROJO_OSC_US, 3.0, sp=2)
    ops += _olas(230, 2, pose)
    return Dib(ops)


@lru_cache(maxsize=None)
def cadenas_rotas():
    """Cadenas rotas de la esclavitud (la emancipación): dos tramos de eslabones con el eslabón partido en el centro."""
    ops = []
    for k in range(4):
        x = -190 + 40 * k
        y = -120 + 10 * k
        ops += _anillo(x, y, 30, 18, 9, rot=0.25 if k % 2 == 0 else 0.25, col=ACERO) if k % 2 == 0 else _anillo(x, y, 30, 12, 7, 0.25, ACERO_OSC)
    for k in range(4):
        x = 190 - 40 * k
        y = -160 + 10 * k
        ops += _anillo(x, y, 30, 18, 9, -0.25, ACERO) if k % 2 == 0 else _anillo(x, y, 30, 12, 7, -0.25, ACERO_OSC)
    ops += [T(arco_(-26, -86, 30, 200, 340, 12, ry=18), 7.0, peso=0.04), T(arco_(26, -128, 30, 20, 160, 12, ry=18), 7.0, peso=0.04)]
    ops += _destellos(0, -108, 22, 62, 12, 3.6)
    ops += forma(_estrella(0, -108, 16), ORO_US, 2.6, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def canon_civil():
    """Cañón de campaña de la Guerra Civil (Napoleón de 12 libras) con grandes ruedas de radios y la contera en el suelo."""
    ops = forma(pol((-210, -8), (-180, -18), (10, -96), (20, -74), (-170, 4)), (92, 104, 84), 4.6, sp=6)
    ops += forma(pol((-40, -110), (190, -150), (194, -122), (-36, -76)), (88, 110, 92), 5.4, peso=0.5, sp=8)
    ops += forma(circ(-48, -92, 18, n=12), (88, 110, 92), 3.6, sp=3)
    ops += [T(linea((60, -130), (62, -96)), 3.0, peso=0.02), T(linea((150, -146), (152, -120)), 3.0, peso=0.02)]
    ops += _rueda(-4, -76, 74, 0, (120, 104, 72), 14)
    return Dib(ops)


@lru_cache(maxsize=None)
def tienda_campana():
    """Tienda de campaña militar de lona en A, con la puerta abierta, vientos y estacas."""
    ops = forma(rect(-210, -10, 210, 0, 3), (150, 160, 100), 3.8, sp=6)
    ops += forma(pol((-170, -6), (-60, -250), (100, -250), (190, -6)), (232, 224, 200), 5.4, peso=0.5, sp=9)
    ops += forma(pol((-170, -6), (-60, -250), (20, -6)), LONA, 4.6, sp=7)
    ops += forma(pol((-90, -6), (-60, -170), (-20, -6)), (70, 62, 56), 3.6, sp=3)
    ops += forma(pol((-60, -170), (-120, -6), (-150, -6)), (220, 210, 180), 3.0, sp=3)
    ops += [T(linea((-60, -250), (-60, -282)), 4.4, peso=0.03), T(linea((-60, -250), (-200, -10)), 2.2, peso=0.02), T(linea((100, -250), (206, -10)), 2.2, peso=0.02)]
    for k in range(4):
        ops += [rayita(-30 + 50 * k, -230 + 4 * k, 10 + 50 * k, -20, 1.6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tambor_militar():
    """Tambor de la Guerra Civil: caja azul con el águila dorada, aros rojos, cuerdas en zigzag y dos baquetas."""
    ops = forma(elip(0, -40, 130, 34, 0, 1.0, 30), ROJO_US, 4.4, sp=6)
    ops += forma(rect(-130, -230, 130, -40, 4), AZUL_US, 5.2, peso=0.5, sp=9)
    ops += forma(rect(-132, -240, 132, -214, 4), ROJO_US, 4.2, sp=5)
    ops += forma(rect(-132, -64, 132, -38, 4), ROJO_US, 4.2, sp=5)
    for k in range(8):
        x0 = -120 + 30 * k
        ops += [T(linea((x0, -214), (x0 + 15, -64), (x0 + 30, -214)), 2.6, peso=0.02)]
    ops += forma(elip(0, -240, 132, 30, 0, 1.0, 30), BLANCO_US, 4.4, sp=6)
    ag = [(-50, -150), (-30, -140), (-14, -150), (-8, -128), (0, -110), (8, -128), (14, -150), (30, -140), (50, -150), (30, -170), (8, -164), (0, -186), (-8, -164),
          (-30, -170)]
    ops += forma(ag, ORO_US, 3.4, sp=3)
    for a in (-0.5, 0.5):
        ops += forma(_tubo([(-120 * math.copysign(1, a), -250), (90 * math.copysign(1, a), -330)], 12, 9), MADERA_US, 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def cabana_lincoln():
    """Cabaña de troncos de Kentucky donde nació Lincoln (1809): un cuarto, chimenea de piedra al costado y hacha en el tocón."""
    ops = forma(rect(-210, -10, 210, 0, 3), (150, 160, 100), 3.8, sp=6)
    ops += forma(rect(-176, -300, -126, -8, 3), PIEDRA_OSC, 4.4, sp=6)
    for k in range(9):
        ops += [rayita(-174, -280 + 32 * k, -128, -280 + 32 * k, 2.0), rayita(-150 + 12 * (k % 2), -280 + 32 * k, -150 + 12 * (k % 2), -248 + 32 * k, 1.8)]
    ops += forma(rect(-130, -170, 110, -6, 3), (132, 98, 66), 5.2, sp=9)
    for k in range(7):
        y = -18 - 23 * k
        ops += [T(linea((-130, y), (112, y)), 2.6, peso=0.02)]
        ops += forma(circ(112, y - 10, 10, n=10), MADERA_OSC_US, 2.4, sp=2)
    ops += forma(pol((-150, -166), (-10, -250), (130, -166)), (104, 84, 70), 5.0, sp=8)
    for k in range(5):
        ops += [rayita(-130 + 52 * k, -170, -60 + 30 * k, -228, 2.0)]
    ops += forma(rect(-40, -116, 10, -6, 2), MADERA_OSC_US, 3.8, sp=4)
    ops += forma(rect(40, -124, 84, -84, 2), (240, 214, 140), 3.4, sp=3)
    ops += [rayita(62, -124, 62, -84, 2.0)]
    ops += forma(curva([(150, -6), (146, -60), (196, -64), (200, -6)], 4), MADERA_US, 4.0, sp=4)
    ops += forma(elip(172, -62, 26, 8, 0, 1.0, 16), (206, 170, 120), 3.0, sp=2)
    ops += [T(linea((170, -64), (196, -150)), 4.4, peso=0.03)]
    ops += forma(pol((188, -150), (220, -164), (214, -130), (196, -136)), ACERO, 3.2, sp=2)
    ops += forma(circ(-166, -334, 18, n=12), (204, 202, 200), 2.6, sp=2)
    return Dib(ops)
