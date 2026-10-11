# -*- coding: utf-8 -*-
"""Piezas comunes de dibujo (boceto) para «La historia de China»: helpers de geometría y un constructor de personajes.

Convenciones: coordenadas locales (x derecha, y abajo), origen en los PIES del personaje (la cabeza queda en y ≈ -215).
Todo devuelve `Dib` (listas de T = tinta y R = crayón) que la escena pinta como pegatina sobre el mapa.
"""
import math
from functools import lru_cache

import numpy as np

import boceto as B
from boceto import (AMARILLO, AZUL, AZUL_CL, AZUL_OSC, BLANCO, GRIS, GRIS_CL, MARRON, NARANJA, PIEL, R, ROJO, ROSA, T, VERDE,
                    VERDE_OSC, Dib, arco_, circ, curva, elip, linea, mano_poli, ondas)

# paleta china (apagada y cálida, como el guache)
ROJO_CH = (200, 66, 60)
ROJO_OSC = (150, 48, 48)
ORO = (236, 184, 64)
ORO_OSC = (196, 142, 40)
JADE = (104, 168, 136)
AZUL_IMP = (74, 112, 170)
CELESTE = (150, 196, 224)
CREMA = (246, 236, 208)
MADERA = (176, 120, 78)
MADERA_OSC = (126, 82, 54)
NEGRO = (52, 46, 52)
MORADO = (140, 104, 160)
PIEL_OSC = (224, 168, 128)
PIEL_CL = (246, 210, 176)
PIEL_ROSA = (240, 190, 160)
GRIS_OSC = (110, 110, 124)
VERDE_CL = (170, 206, 120)
MIJO = (226, 190, 92)
PIEDRA = (196, 188, 172)
ARCILLA = (190, 120, 96)


# ------------------------------------------------------------------ atajos de geometría
def cerrar(P):
    P = np.asarray(P, float)
    return np.vstack([P, P[:1]])


def pol(*pts):
    return np.asarray(pts, float)


def rect(x0, y0, x1, y1, r=8.0, n=5):
    """Rectángulo de esquinas redondeadas (polígono cerrado)."""
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    P = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        P += list(arco_(cx, cy, r, a0, a0 + 90, n))
    return cerrar(P)


def trap(xa0, xa1, ya, xb0, xb1, yb):
    """Trapecio: arriba [xa0, xa1] a la altura ya, abajo [xb0, xb1] a la altura yb."""
    return cerrar([(xa0, ya), (xa1, ya), (xb1, yb), (xb0, yb)])


def forma(P, color, w=5.0, peso=None, sp=10.0, ang=-55.0, tinta=True, cerrada=True):
    """Contorno de tinta + relleno de crayón del polígono P."""
    P = cerrar(P) if cerrada else np.asarray(P, float)
    ops = []
    if tinta:
        ops.append(T(P, w, peso=peso))
    if color is not None:
        ops.append(R(P, color, peso=(peso * 0.7 if peso else None), sp=sp, ang=ang))
    return ops


def elipse(cx, cy, rx, ry, color, w=5.0, rot=0.0, peso=None, sp=9.0, tinta=True):
    P = elip(cx, cy, rx, ry, rot, 1.0, 36)
    return forma(P, color, w, peso, sp, tinta=tinta, cerrada=False)


def trazo(*pts, w=4.5, peso=0.05):
    return T(np.asarray(pts, float), w, peso=peso)


def rayita(x0, y0, x1, y1, w=4.0):
    return T(linea((x0, y0), (x1, y1)), w, peso=0.04)


def punto(x, y, w=11.0):
    return T(linea((x, y), (x + 0.6, y + 0.4)), w, peso=0.02)


# ------------------------------------------------------------------ personajes
def _manga(sx, sy, ang, largo, ancho, lado):
    """Polígono de una manga desde el hombro (sx, sy); ang en grados desde 'hacia abajo', positivo = levantar hacia afuera."""
    a = math.radians(ang)
    dx, dy = lado * math.sin(a), math.cos(a)              # dirección del brazo
    nx, ny = -dy, dx
    ex, ey = sx + dx * largo, sy + dy * largo
    hw = ancho / 2
    P = [(sx + nx * hw * 1.05, sy + ny * hw * 1.05), (ex + nx * hw * 0.8, ey + ny * hw * 0.8), (ex - nx * hw * 0.8, ey - ny * hw * 0.8),
         (sx - nx * hw * 1.05, sy - ny * hw * 1.05)]
    return P, (ex + dx * 10, ey + dy * 10), (dx, dy)


def _cara(cara, mirada, cy=-215.0, r=40.0):
    ex = 15.0
    ox = 6.0 * mirada
    ops = []
    if cara in ("feliz", "normal", "serio", "enojo", "lloron"):
        ops += [punto(-ex + ox, cy - 4, 8), punto(ex + ox, cy - 4, 8)]
    if cara == "feliz":
        ops.append(T(arco_(ox * 0.5, cy + 4, 16, 25, 155, 9), 4.2, peso=0.05))
        ops += [R(elip(-28, cy + 10, 8, 5, n=14), ROSA, peso=0.03, sp=4, off=(1, -1)), R(elip(28, cy + 10, 8, 5, n=14), ROSA, peso=0.03, sp=4, off=(1, -1))]
    elif cara == "normal":
        ops.append(T(linea((-8 + ox, cy + 18), (8 + ox, cy + 18)), 4, peso=0.03))
    elif cara == "serio":
        ops.append(T(linea((-10 + ox, cy + 19), (10 + ox, cy + 19)), 4.4, peso=0.03))
        ops += [T(linea((-ex - 7 + ox, cy - 20), (-ex + 6 + ox, cy - 19)), 3.2, peso=0.03), T(linea((ex - 6 + ox, cy - 19), (ex + 7 + ox, cy - 20)), 3.2, peso=0.03)]
    elif cara == "enojo":
        ops.append(T(arco_(ox * 0.5, cy + 28, 13, 205, 335, 8), 4.4, peso=0.04))
        ops += [T(linea((-ex - 7 + ox, cy - 22), (-ex + 6 + ox, cy - 15)), 3.4, peso=0.03), T(linea((ex - 6 + ox, cy - 15), (ex + 7 + ox, cy - 22)), 3.4, peso=0.03)]
    elif cara == "lloron":
        ops.append(T(arco_(ox * 0.5, cy + 28, 12, 205, 335, 8), 4.2, peso=0.04))
        ops += [R(elip(-ex, cy + 12, 4, 10, n=10), CELESTE, peso=0.03, sp=3), R(elip(ex, cy + 12, 4, 10, n=10), CELESTE, peso=0.03, sp=3)]
    elif cara == "asombro":
        ops += [T(circ(-ex + ox, cy - 4, 8, n=14), 4, peso=0.05), T(circ(ex + ox, cy - 4, 8, n=14), 4, peso=0.05), punto(-ex + ox, cy - 4, 5), punto(ex + ox, cy - 4, 5)]
        ops.append(T(elip(ox * 0.5, cy + 22, 8, 10, n=14), 4.2, peso=0.05))
    elif cara == "miedo":
        ops += [T(circ(-ex + ox, cy - 4, 9, n=14), 4, peso=0.05), T(circ(ex + ox, cy - 4, 9, n=14), 4, peso=0.05), punto(-ex + ox, cy - 4, 4), punto(ex + ox, cy - 4, 4)]
        ops.append(T(ondas(-14 + ox, 14 + ox, cy + 22, 4, 14), 4, peso=0.05))
    elif cara == "dormido":
        ops += [T(arco_(-ex + ox, cy - 4, 8, 20, 160, 7), 4, peso=0.04), T(arco_(ex + ox, cy - 4, 8, 20, 160, 7), 4, peso=0.04)]
        ops.append(T(circ(ox * 0.5, cy + 22, 5, n=10), 3.6, peso=0.03))
    elif cara == "guiño":
        ops += [punto(-ex + ox, cy - 4, 10), T(arco_(ex + ox, cy - 4, 8, 200, 340, 7), 4, peso=0.04)]
        ops.append(T(arco_(ox * 0.5, cy + 4, 16, 25, 155, 9), 4.2, peso=0.05))
    return ops


SOMBREROS = {}


def sombrero(nombre, cy=-215.0):
    """Ops del sombrero/peinado de `nombre` sobre la cabeza (centro (0, cy), radio 40)."""
    top = cy - 38
    if nombre == "moño":          # peinado con moño (campesino, mujer)
        return forma(elip(0, top - 12, 15, 14, 0, 1.0, 20), NEGRO, 4, sp=6) + forma(elip(0, cy - 12, 41, 30, 0, 0.5, 26)[::1], NEGRO, 4, cerrada=False, sp=7)[1:]
    if nombre == "paja":          # sombrero cónico de campesino
        return forma([(-78, cy - 16), (0, cy - 84), (78, cy - 16), (40, cy - 26), (-40, cy - 26)], MIJO, 5, sp=8)
    if nombre == "corona":        # corona/mianguan de rey: tabla plana con borlas
        ops = forma(rect(-44, cy - 66, 44, cy - 50, 4), NEGRO, 4.5, sp=6)
        ops += forma(rect(-26, cy - 52, 26, cy - 30, 5), NEGRO, 4.5, sp=6)
        ops += [rayita(-40 + 16 * k, cy - 50, -40 + 16 * k, cy - 26, 3) for k in range(6)]
        ops += [R(elip(-40 + 16 * k, cy - 23, 4.5, 6, n=8), ROJO_CH, peso=0.02, sp=3) for k in range(6)]
        return ops
    if nombre == "mianguan":
        ops = forma(rect(-48, cy - 72, 48, cy - 54, 4), NEGRO, 4.5, sp=6)
        ops += forma(rect(-30, cy - 56, 30, cy - 34, 5), NEGRO, 4.5, sp=6)
        for k in range(7):
            x = -42 + 14 * k
            ops += [rayita(x, cy - 54, x, cy - 20, 2.6), R(elip(x, cy - 16, 4, 6, n=8), JADE, peso=0.02, sp=3)]
        return ops
    if nombre == "funcionario":   # sombrero negro con alas (Han/Song)
        ops = forma(rect(-28, cy - 70, 28, cy - 36, 8), NEGRO, 4.5, sp=6)
        ops += forma(pol((-28, cy - 50), (-96, cy - 54), (-96, cy - 44), (-28, cy - 40)), NEGRO, 4, sp=6)
        ops += forma(pol((28, cy - 50), (96, cy - 54), (96, cy - 44), (28, cy - 40)), NEGRO, 4, sp=6)
        return ops
    if nombre == "gorro":         # gorro de invierno / mongol
        ops = forma([(-42, cy - 18), (-34, cy - 62), (0, cy - 76), (34, cy - 62), (42, cy - 18)], ROJO_OSC, 4.5, sp=8)
        ops += forma(rect(-46, cy - 28, 46, cy - 12, 6), CREMA, 4, sp=7)
        return ops
    if nombre == "manchu":        # gorro redondo manchú con borla roja
        ops = forma([(-38, cy - 20), (-32, cy - 54), (0, cy - 64), (32, cy - 54), (38, cy - 20)], NEGRO, 4.5, sp=8)
        ops += forma(elip(0, cy - 70, 7, 7, 0, 1.0, 14), ROJO_CH, 3.6, sp=4)
        return ops
    if nombre == "letrado":       # gorro de letrado (Confucio)
        ops = forma(rect(-32, cy - 62, 32, cy - 34, 8), MORADO, 4.5, sp=7)
        ops += forma(rect(-40, cy - 40, 40, cy - 30, 4), MORADO, 4, sp=6)
        return ops
    if nombre == "casco":         # casco de soldado
        ops = forma([(-44, cy - 14), (-40, cy - 54), (0, cy - 70), (40, cy - 54), (44, cy - 14), (0, cy - 32)], GRIS_OSC, 4.5, sp=8)
        ops += [rayita(0, cy - 70, 0, cy - 90, 4.5), R(elip(0, cy - 92, 6, 8, n=10), ROJO_CH, peso=0.02, sp=3)]
        return ops
    if nombre == "gorra":         # gorra con estrella (siglo XX)
        ops = forma(rect(-44, cy - 56, 44, cy - 30, 10), (108, 122, 100), 4.5, sp=8)
        ops += forma(rect(-44, cy - 34, 44, cy - 24, 4), (88, 100, 84), 4, sp=6)
        ops += [R(circ(0, cy - 44, 8, n=12), ROJO_CH, peso=0.02, sp=4)]
        return ops
    if nombre == "bombin":        # sombrero de copa (británico)
        ops = forma(rect(-30, cy - 92, 30, cy - 34, 4), NEGRO, 4.5, sp=8)
        ops += forma(rect(-52, cy - 40, 52, cy - 28, 4), NEGRO, 4.5, sp=8)
        return ops
    if nombre == "pelo":
        return forma(elip(0, cy - 10, 43, 40, 0, 0.5, 26), NEGRO, 4.5, cerrada=False, sp=7)[1:] + forma(elip(0, cy - 10, 43, 40, 0, 0.5, 26), NEGRO, 4, cerrada=True, sp=7)[:0]
    if nombre == "calvo":
        return []
    if nombre == "diadema":
        return forma(rect(-44, cy - 50, 44, cy - 38, 6), ROJO_CH, 4, sp=6)
    return []


def persona(ropa=ROJO_CH, piel=PIEL, sombrero_=None, cara="feliz", brazos=(18, 18), pose=0, barba=None, bigote=False, trenza=False,
            traje="tunica", faja=None, mirada=0, acc_d=None, acc_i=None, alto=1.0, cuello=None, pelo_largo=None):
    """Personaje de pie. `brazos` = (ángulo brazo izq, ángulo brazo der) en grados desde 'hacia abajo' (positivo = levantar hacia afuera).
    traje: tunica (larga) | corta | armadura | vestido. `pose` 0/1 = paso alternado (ciclo de caminata)."""
    cy = -215.0
    ops = []
    paso = (1 if pose % 2 else -1) * 9
    # pies
    ops += forma(elip(-22 + paso, -6, 22, 11, 0, 1.0, 16), NEGRO, 4, sp=6)
    ops += forma(elip(22 - paso, -6, 22, 11, 0, 1.0, 16), NEGRO, 4, sp=6)
    # túnica
    if traje == "tunica":
        body = curva([(-46, -166), (-64, -60), (-70, -10), (0, -2), (70, -10), (64, -60), (46, -166)], 5)
    elif traje == "vestido":
        body = curva([(-44, -166), (-56, -100), (-88, -8), (0, -2), (88, -8), (56, -100), (44, -166)], 5)
    elif traje == "armadura":
        body = curva([(-48, -166), (-56, -80), (-54, -16), (0, -10), (54, -16), (56, -80), (48, -166)], 5)
    else:
        body = curva([(-46, -166), (-52, -90), (-50, -14), (0, -8), (50, -14), (52, -90), (46, -166)], 5)
    body = np.vstack([body, [(-46, -166)]])
    ops += forma(np.vstack([[(-46, -176)], body, [(46, -176)]]), ropa, 5.5, peso=0.7, sp=10)
    # cuello (escote) y faja
    ops += [T(linea((-18, -172), (0, -150), (18, -172)), 4, peso=0.05)]
    if cuello:
        ops += [R(pol((-22, -176), (0, -146), (22, -176)), cuello, peso=0.04, sp=5)]
    if faja:
        ops += forma(rect(-56, -106, 56, -84, 4), faja, 4.2, sp=7)
    if traje == "armadura":
        ops += [T(linea((-40, -130), (40, -130)), 3.5, peso=0.04), T(linea((-40, -100), (40, -100)), 3.5, peso=0.04)]
        ops += [rayita(-20 + 20 * k, -160, -20 + 20 * k, -90, 3) for k in range(3)]
    # brazos
    manos = []
    for lado, ang in ((-1, brazos[0]), (1, brazos[1])):
        ps, mano, d = _manga(lado * 46, -160, ang, 86, 28, lado)
        ops += forma(ps, ropa, 4.8, peso=0.25, sp=8)
        ops += forma(elip(mano[0], mano[1], 13, 13, 0, 1.0, 14), piel, 4, sp=5)
        manos.append((mano, d))
    # cabeza
    cabeza = elip(0, cy, 41, 42, 0, 1.0, 40)
    ops += forma(cabeza, piel, 5.5, peso=0.55, sp=9)
    if pelo_largo:
        ops += forma(pol((-42, cy - 6), (-50, cy + 60), (-30, cy + 70), (-36, cy + 10)), pelo_largo, 4, sp=7)
        ops += forma(pol((42, cy - 6), (50, cy + 60), (30, cy + 70), (36, cy + 10)), pelo_largo, 4, sp=7)
    ops += _cara(cara, mirada, cy)
    if barba:
        b = curva([(-34, cy + 18), (-30, cy + 60), (-12, cy + 96), (0, cy + 112), (12, cy + 96), (30, cy + 60), (34, cy + 18)], 6)
        ops += forma(np.vstack([b, [(0, cy + 14)]]), barba, 4.5, sp=8)
    if bigote:
        ops += [T(curva([(-28, cy + 14), (-10, cy + 10), (0, cy + 14)], 5), 5, peso=0.06), T(curva([(28, cy + 14), (10, cy + 10), (0, cy + 14)], 5), 5, peso=0.06)]
    if sombrero_:
        ops += sombrero(sombrero_, cy)
    if trenza:
        ops += [T(curva([(30, cy - 16), (52, cy + 10), (46, cy + 60), (58, cy + 110)], 6), 6, peso=0.1)]
    for acc, (mano, d) in zip((acc_i, acc_d), manos):
        if acc:
            ops += ACC[acc](mano, d)
    d = Dib(ops)
    d.manos = [m for m, _ in manos]
    return d


# ------------------------------------------------------------------ accesorios que sostienen los personajes (en la mano)
def _rotar(P, ang, cx, cy):
    c, s = math.cos(ang), math.sin(ang)
    P = np.asarray(P, float)
    return np.stack([cx + (P[:, 0] - cx) * c - (P[:, 1] - cy) * s, cy + (P[:, 0] - cx) * s + (P[:, 1] - cy) * c], 1)


def _acc_rollo(m, d):
    x, y = m
    return forma(rect(x - 30, y - 12, x + 30, y + 12, 6), CREMA, 4, sp=6) + [R(circ(x - 30, y, 12, n=12), MADERA, peso=0.03, sp=4), R(circ(x + 30, y, 12, n=12), MADERA, peso=0.03, sp=4),
                                                                             rayita(x - 16, y - 4, x + 16, y - 4, 2.5), rayita(x - 16, y + 4, x + 10, y + 4, 2.5)]


def _acc_pincel(m, d):
    x, y = m
    return [T(linea((x, y + 10), (x + 26, y - 70)), 5.5, peso=0.05), R(pol((x + 22, y - 62), (x + 34, y - 90), (x + 40, y - 60)), NEGRO, peso=0.03, sp=4)]


def _acc_espada(m, d):
    x, y = m
    return [T(linea((x, y + 14), (x + 8, y - 110)), 5, peso=0.08), R(pol((x - 4, y - 20), (x + 4, y - 112), (x + 14, y - 20)), GRIS_CL, peso=0.05, sp=4),
            T(linea((x - 16, y - 18), (x + 26, y - 20)), 6, peso=0.04)]


def _acc_lanza(m, d):
    x, y = m
    return [T(linea((x, y + 80), (x + 4, y - 190)), 5, peso=0.15), R(pol((x - 10, y - 190), (x + 6, y - 246), (x + 20, y - 190)), GRIS_CL, peso=0.04, sp=4)]


def _acc_copa(m, d):
    x, y = m
    return forma(pol((x - 16, y - 30), (x + 16, y - 30), (x + 10, y + 2), (x - 10, y + 2)), CREMA, 4, sp=6) + [T(linea((x, y + 2), (x, y + 14)), 4, peso=0.02)]


def _acc_azada(m, d):
    x, y = m
    return [T(linea((x - 10, y + 70), (x + 14, y - 120)), 6, peso=0.1), R(pol((x + 4, y - 122), (x + 54, y - 108), (x + 42, y - 88), (x + 10, y - 98)), GRIS_CL, peso=0.04, sp=4)]


def _acc_saco(m, d):
    x, y = m
    return forma(curva([(x - 32, y - 10), (x - 40, y + 30), (x, y + 44), (x + 40, y + 30), (x + 32, y - 10)], 6), (214, 170, 100), 4.5, sp=8) + [T(linea((x - 14, y - 14), (x + 14, y - 14)), 4, peso=0.03),
                                                                                                                                 R(elip(x, y + 16, 12, 12, n=12), ORO, peso=0.02, sp=4)]


def _acc_abanico(m, d):
    x, y = m
    P = [(x, y)] + list(arco_(x, y, 64, -150, -30, 12))
    return forma(P, CREMA, 4, sp=7) + [rayita(x, y, x + 64 * math.cos(math.radians(a)), y + 64 * math.sin(math.radians(a)), 2.5) for a in (-120, -90, -60)]


def _acc_tazon(m, d):
    x, y = m
    return forma([(x - 24, y - 14), (x + 24, y - 14), (x + 16, y + 16), (x - 16, y + 16)], CREMA, 4.2, sp=6)


def _acc_mijo(m, d):
    x, y = m
    ops = [T(linea((x, y + 10), (x + 2, y - 100)), 4, peso=0.05)]
    for k in range(6):
        ops.append(R(elip(x + 4 * (k % 2), y - 30 - 13 * k, 7, 11, math.radians(18 * (1 if k % 2 else -1)), 1.0, 10), MIJO, peso=0.02, sp=3))
    return ops


def _acc_hoja(m, d):
    x, y = m
    return forma(rect(x - 34, y - 46, x + 34, y + 10, 3), BLANCO, 3.8, sp=6) + [rayita(x - 20, y - 30 + 10 * k, x + 20, y - 30 + 10 * k, 2.5) for k in range(4)]


def _acc_tetera(m, d):
    x, y = m
    return forma(elip(x, y - 6, 26, 22, 0, 1.0, 22), (210, 140, 100), 4.2, sp=6) + [T(arco_(x + 26, y - 6, 12, -90, 90, 8), 4, peso=0.04), T(linea((x - 24, y - 12), (x - 40, y - 26)), 4.2, peso=0.03)]


def _acc_bandera(m, d):
    x, y = m
    return [T(linea((x, y + 40), (x + 4, y - 170)), 5, peso=0.12)] + forma(pol((x + 4, y - 170), (x + 100, y - 150), (x + 4, y - 110)), ROJO_CH, 4, sp=7)


def _acc_frasco(m, d):
    x, y = m
    return forma(elip(x, y - 16, 26, 26, 0, 1.0, 20), CELESTE, 4.2, sp=6) + forma(rect(x - 9, y - 54, x + 9, y - 30, 3), CELESTE, 4, sp=5) + [R(elip(x, y - 6, 20, 14, n=14), (138, 210, 110), peso=0.02, sp=4)]


def _acc_antorcha(m, d):
    x, y = m
    return [T(linea((x, y + 14), (x + 4, y - 70)), 6, peso=0.05), R(pol((x - 14, y - 70), (x + 4, y - 120), (x + 22, y - 70)), NARANJA, peso=0.03, sp=4)]


def _acc_cuenco(m, d):
    x, y = m
    return forma(arco_(x, y - 22, 28, 0, 180, 12).tolist() + [(x - 28, y - 22)], CREMA, 4.2, sp=6)


ACC = {"rollo": _acc_rollo, "pincel": _acc_pincel, "espada": _acc_espada, "lanza": _acc_lanza, "copa": _acc_copa, "azada": _acc_azada,
       "saco": _acc_saco, "abanico": _acc_abanico, "tazon": _acc_tazon, "mijo": _acc_mijo, "hoja": _acc_hoja, "tetera": _acc_tetera,
       "bandera": _acc_bandera, "frasco": _acc_frasco, "antorcha": _acc_antorcha, "cuenco": _acc_cuenco}
