# -*- coding: utf-8 -*-
"""Utilería noir 4: brazo mecánico de la cafetería · enchufe con clavija y cable · taza de café · cámara de vigilancia."""
import math

import numpy as np

import noir as N
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from props import rect, rot
from toon import blob, elipse_, suave, tubo


def _seg(h, a, b, ancho, tono, sem, rim=0.95):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    L = float(np.hypot(*d)) + 1e-9
    n = np.array([-d[1], d[0]]) / L * ancho / 2
    P = np.array([a + n, b + n * 0.85, b - n * 0.85, a - n])
    h.pieza(P, tono, sem, w=5, luz=(0.4, -1), d=10, trama=0.35, rim=rim, rim_tono=235)
    for k in (0.3, 0.7):                                  # remaches
        q = a + d * k
        h.disco(q[0] + n[0] * 0.5, q[1] + n[1] * 0.5, 4, gris(200))


def brazo_robot(h, bx, by, ang1, ang2, ang3, s=1.0, pinza=0.5, sem=0, tono=96):
    """Brazo articulado (base en (bx, by)); ángulos en rad desde la vertical hacia la derecha. Devuelve la punta de la pinza."""
    h.pieza(rect(bx - 70 * s, by - 40 * s, 140 * s, 40 * s), tono - 30, sem, w=5, luz=(0.4, -1), d=8, trama=0.3, rim=0.9)
    h.pieza(elipse_(bx, by - 60 * s, 46 * s, 30 * s, n=24), tono - 10, sem + 1, w=5, luz=(0.4, -1), d=8, trama=0.3, rim=0.9)
    p0 = np.array([bx, by - 60 * s])
    p1 = p0 + 260 * s * np.array([math.sin(ang1), -math.cos(ang1)])
    p2 = p1 + 230 * s * np.array([math.sin(ang1 + ang2), -math.cos(ang1 + ang2)])
    p3 = p2 + 70 * s * np.array([math.sin(ang1 + ang2 + ang3), -math.cos(ang1 + ang2 + ang3)])
    _seg(h, p0, p1, 54 * s, tono, sem + 2)
    _seg(h, p1, p2, 44 * s, tono + 10, sem + 3)
    for q, r in ((p0, 30), (p1, 26), (p2, 22)):
        h.pieza(elipse_(q[0], q[1], r * s, r * s, n=20), tono - 20, sem + 4 + int(r), w=4, luz=(0.4, -1), d=5, trama=0, rim=0.9)
    _seg(h, p2, p3, 30 * s, tono - 10, sem + 9)
    a = ang1 + ang2 + ang3
    u = np.array([math.sin(a), -math.cos(a)])
    n = np.array([-u[1], u[0]])
    for sx in (-1, 1):                                    # pinza de dos dedos
        q0 = p3 + n * sx * 14 * s
        q1 = q0 + u * 50 * s + n * sx * 26 * s * pinza
        q2 = q1 + u * 34 * s - n * sx * 18 * s
        h.trazo(np.array([q0, q1, q2]), 12 * s, sem + 12 + sx, color=gris(40), jit=0.4, taper=(0.1, 0.4))
    return p3 + u * 70 * s


def taza(h, x, y, s=1.0, sem=0, humo_t=None):
    h.pieza(elipse_(x, y + 6 * s, 70 * s, 14 * s, n=28), 210, sem, w=4 * s, luz=(0.3, -1), d=4, trama=0, rim=0.5)       # plato
    P = np.array([(-42, -70), (42, -70), (34, 0), (-34, 0)], float) * s + (x, y)
    h.pieza(P, 225, sem + 1, w=4 * s, luz=(0.3, -1), d=10 * s, trama=0.3, rim=0.6)
    h.pieza(elipse_(x, y - 70 * s, 42 * s, 9 * s, n=24), 30, sem + 2, w=3 * s, luz=(0, -1), d=2, trama=0)
    h.trazo(np.array([[x + 40 * s, y - 56 * s], [x + 66 * s, y - 46 * s], [x + 62 * s, y - 22 * s], [x + 36 * s, y - 18 * s]]), 8 * s,
            sem + 3, color=gris(225))
    if humo_t is not None:
        N.humo(h, humo_t, x, y - 80 * s, k=0.8, ancho=1.2, viento=(6, -60), vida=2.2, hebras=2, sem=sem)


def enchufe(h, x, y, s=1.0, clavija=1.0, sem=0):
    """Placa de enchufe en la pared (x, y centro) y la clavija con su cable (clavija 1 = enchufada, 0 = fuera, a la izq)."""
    h.pieza(rect(x - 90 * s, y - 130 * s, 180 * s, 260 * s), 205, sem, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0, rim=0.5)
    h.disco(x, y - 100 * s, 6 * s, gris(120))
    h.disco(x, y + 100 * s, 6 * s, gris(120))
    for sx in (-1, 1):
        h.pieza(rect(x + sx * 26 * s - 6 * s, y - 30 * s, 12 * s, 40 * s), 15, sem + 1 + sx, w=2, luz=(0, -1), d=1, sombra=0, trama=0)
    cx = x - 260 * s * (1 - clavija)
    h.pieza(rect(cx - 60 * s, y - 52 * s, 120 * s, 104 * s), 40, sem + 5, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0.3, rim=0.9)
    h.trazo(np.array([[cx, y + 52 * s], [cx - 20 * s, y + 200 * s], [cx - 160 * s, y + 360 * s], [cx - 500 * s, y + 420 * s]]),
            22 * s, sem + 6, color=gris(20), jit=0.5, taper=(0.0, 0.0))
    return np.array([cx, y])


def camara_vigilancia(h, x, y, s=1.0, ang=0.0, led=1.0, t=0.0, sem=0):
    def T(P):
        return rot(np.asarray(P, float) * s + (x, y), ang, np.array([x, y]))
    h.pieza(T(rect(-40, -140, 30, 140)), 40, sem, w=4 * s, luz=(0.3, -1), d=6, trama=0.3, rim=0.8)
    h.pieza(T([(-60, -200), (200, -220), (220, -150), (-50, -130)]), 70, sem + 1, w=5 * s, luz=(0.3, -1), d=12 * s, trama=0.4, rim=0.9)
    h.pieza(T([(200, -224), (250, -232), (258, -140), (214, -146)]), 30, sem + 2, w=5 * s, luz=(0.3, -1), d=6, trama=0, rim=0.8)
    h.pieza(T(elipse_(236, -186, 22, 34, n=20)), 8, sem + 3, w=4 * s, luz=(0.3, -1), d=3, trama=0, rim=0.9)
    v = led * (0.5 + 0.5 * (int(t * 2) % 2))
    q = T([[-30, -190]])[0]
    h.emitir(elipse_(q[0], q[1], 6 * s, 6 * s, n=10), 1.4 * v)
