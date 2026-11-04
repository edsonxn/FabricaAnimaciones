# -*- coding: utf-8 -*-
"""Más personajes y utilería (kit acuarela): jorobada con boca que se abre, picos de calamar, manómetro, termómetro,
flecha pintada, bombilla, calavera, molécula de O2, vapor."""
import math

import numpy as np

from acuarela import TINTA, brillo, curva, elipse, forma, linea, rgb, rotulo, rrect, tr
from personajes import AMARILLO, BLANCO


def jorobada(im, x, y, s, t, sx=1.0, rot=0.0, abre=0.0, seed=1200, col=None, cola=1.0, ojo="abierto", dentro=None):
    """Jorobada de perfil mirando a la derecha; abre 0..1: la mandíbula superior sube y la garganta plisada se infla.
    dentro(im, T) se llama tras pintar el interior de la boca y antes de las mandíbulas (para meter algo en la boca)."""
    col = rgb("3d4656") if col is None else col
    claro = rgb("dfe1e4")
    osc = col * 0.65

    def T(p):
        return tr(p, x, y, s, rot, sx)

    hinge = np.array([160, 4], np.float32)

    def R(p, ang, esc_y=1.0):
        q = np.asarray(p, np.float32) - hinge
        q[:, 1] *= esc_y
        return tr(q, hinge[0], hinge[1], 1, ang)

    ang_c = 0.25 * math.sin(t * 1.5) * cola
    fl = np.array([(-430, 0), (-520, -40), (-600, -100), (-560, -14), (-600, 100), (-520, 40)], np.float32)
    forma(im, T(curva(tr(fl + (430, 0), -430, 0, 1, ang_c), 5, True)), osc, t, seed + 1, tinta=5 * s)
    forma(im, T(curva([(170, -66), (0, -80), (-150, -70), (-320, -34), (-440, -10), (-446, 8), (-320, 36), (-150, 68), (0, 80),
                       (170, 74)], 7, True)), col, t, seed + 2, tinta=6 * s, sombra=(osc, 0, -26, 0.6), luz=(claro, 0, 24, 0.1))
    forma(im, T(curva([(-170, -70), (-200, -96), (-240, -72)], 5, True)), col, t, seed + 3, tinta=4 * s)
    a_sup, a_inf, inflar = -0.75 * abre, 0.32 * abre, 1 + 0.55 * abre
    sup = [(160, -66), (300, -60), (440, -34), (505, -10), (478, 2), (300, 6), (160, 6)]
    inf = [(160, 6), (300, 10), (462, 8), (492, 16), (446, 52), (300, 84), (160, 78)]
    if abre > 0.02:
        ps, pi_ = R([(478, 2)], a_sup)[0], R([(470, 12)], a_inf, inflar)[0]
        forma(im, T(np.array([hinge, ps, (ps + pi_) / 2 + (40, 0), pi_], np.float32)), rgb("6e2a36"), t, seed + 4, tinta=0,
              sombra=(rgb("2d0d14"), -30, 0, 0.7))
        for k in range(14):                          # barbas colgando de la mandíbula superior
            bx = 200 + k * 20
            linea(im, T(R([(bx, 6), (bx + 3, 6 + 34 * abre)], a_sup)), 4.5 * s, col=rgb("5b4a3c"), seed=seed + 40 + k, t=t, alfa=0.85)
        if dentro is not None:
            dentro(im, T)
    forma(im, T(R(curva(inf, 6, True), a_inf, inflar)), claro, t, seed + 5, tinta=5 * s, sombra=(rgb("a7aab0"), 0, -14, 0.5))
    for k in range(6):                               # pliegues de la garganta
        yk = 22 + 10 * k
        linea(im, T(R([(186, yk), (300, yk + 6 - k), (420, 18 + 4 * k)], a_inf, inflar)), 2.4 * s, seed=seed + 20 + k, t=t, alfa=0.6)
    forma(im, T(R(curva(sup, 6, True), a_sup)), col, t, seed + 6, tinta=5 * s, luz=(claro, 0, 16, 0.1))
    for k in range(5):                               # tubérculos
        cx_, cy_ = R([(250 + 50 * k, -54 + 10 * k)], a_sup)[0]
        forma(im, T(elipse(cx_, cy_, 7, 6)), col * 1.2, t, seed + 30 + k, tinta=2.4 * s, amp=0.4)
    forma(im, T(curva([(120, 64), (40, 150), (-120, 230), (-160, 214), (-40, 120), (40, 66)], 6, True)), claro, t, seed + 7,
          tinta=4.6 * s, sombra=(rgb("a7aab0"), 8, -8, 0.5))
    ex, ey = 150, 24
    if ojo == "abierto":
        forma(im, T(elipse(ex, ey, 10, 8)), TINTA, t, seed + 8, tinta=0)
        bx_, by_ = T(np.array([(ex + 3, ey - 3)], np.float32))[0]
        brillo(im, bx_, by_, 3 * s, BLANCO, 1.0)
    else:
        linea(im, T(curva([(ex - 10, ey), (ex, ey + 5), (ex + 10, ey)], 4)), 3.6 * s, seed=seed + 8, t=t)
    return T


def pico_calamar(im, x, y, s, t, rot=0.0, seed=1300):
    def T(p):
        return tr(p, x, y, s, rot)
    c = rgb("4a2f22")
    forma(im, T(curva([(0, -40), (34, -30), (40, 6), (16, 30), (22, 2), (8, -18)], 5, True)), c, t, seed, tinta=3 * s,
          luz=(rgb("d8b28a"), -4, 6, 0.35))
    forma(im, T(curva([(-4, -20), (-34, -6), (-30, 26), (-6, 34), (-14, 10)], 5, True)), c * 1.15, t, seed + 1, tinta=3 * s,
          luz=(rgb("d8b28a"), 4, 6, 0.3))


def manometro(im, x, y, r, t, valor, seed=1400, etiqueta="AIRE"):
    """Manómetro del tanque: valor 1 = lleno (verde) → 0 = vacío (rojo)."""
    forma(im, elipse(x, y, r + 14, r + 14), rgb("c9ced6"), t, seed, tinta=5, sombra=(rgb("7e8794"), 8, 8, 0.6))
    forma(im, elipse(x, y, r, r), BLANCO, t, seed + 1, tinta=3.5)
    a0, a1 = math.radians(220), math.radians(-40)
    for k, c in enumerate((rgb("e0574a"), rgb("f2bf35"), rgb("6fbf5a"))):
        u0, u1 = k / 3, (k + 1) / 3
        aa = np.linspace(a0 + (a1 - a0) * u0, a0 + (a1 - a0) * u1, 12)
        pts = np.concatenate([np.stack([x + r * 0.86 * np.cos(aa), y - r * 0.86 * np.sin(aa)], 1),
                              np.stack([x + r * 0.62 * np.cos(aa[::-1]), y - r * 0.62 * np.sin(aa[::-1])], 1)])
        forma(im, pts, c, t, seed + 2 + k, tinta=0, amp=0.5)
    a = a0 + (a1 - a0) * float(np.clip(valor, 0, 1))
    linea(im, [(x, y), (x + r * 0.8 * math.cos(a), y - r * 0.8 * math.sin(a))], 7, col=rgb("c23a2e"), seed=seed + 6, t=t, punta=False)
    forma(im, elipse(x, y, 11, 11), TINTA, t, seed + 7, tinta=0)
    rotulo(im, etiqueta, x, y + r * 0.42, int(r * 0.26), rgb("3a3330"), t, seed + 8, tinta=False)


def termometro(im, x, y, s, t, nivel, seed=1500):
    forma(im, rrect(x, y - 90 * s, 44 * s, 200 * s, 22 * s), BLANCO, t, seed, tinta=4 * s)
    forma(im, elipse(x, y + 20 * s, 34 * s, 34 * s), rgb("e0574a"), t, seed + 1, tinta=4 * s)
    h = 170 * s * nivel
    if h > 4:
        forma(im, rrect(x, y - h / 2, 18 * s, h + 10 * s, 9 * s), rgb("e0574a"), t, seed + 2, tinta=0)
    for k in range(5):
        linea(im, [(x + 10 * s, y - 40 * s - 30 * s * k), (x + 22 * s, y - 40 * s - 30 * s * k)], 2.4 * s, seed=seed + 3 + k, t=t)


def flecha(im, x0, y0, x1, y1, ancho, t, col, seed=1600):
    d = np.array([x1 - x0, y1 - y0], np.float32)
    L = float(np.linalg.norm(d)) + 1e-6
    d /= L
    n = np.array([-d[1], d[0]], np.float32)
    p0, p1 = np.array([x0, y0], np.float32), np.array([x1, y1], np.float32)
    cab = min(L * 0.45, ancho * 2.2)
    b = p1 - d * cab
    pts = np.array([p0 + n * ancho / 2, b + n * ancho / 2, b + n * ancho * 1.25, p1, b - n * ancho * 1.25, b - n * ancho / 2,
                    p0 - n * ancho / 2], np.float32)
    forma(im, pts, col, t, seed, tinta=4.4, sombra=(np.asarray(col) * 0.6, float(n[0] * 8), float(n[1] * 8), 0.5))


def bombilla(im, x, y, s, t, seed=1700):
    brillo(im, x, y, 90 * s, AMARILLO, 0.45)
    cuerpo = curva([(0, -46), (34, -24), (28, 14), (14, 30), (-14, 30), (-28, 14), (-34, -24)], 6, True) * s + np.array([x, y], np.float32)
    forma(im, cuerpo, AMARILLO, t, seed, tinta=3.4 * s, luz=(BLANCO, -6, 8, 0.4))
    forma(im, rrect(x, y + 40 * s, 30 * s, 20 * s, 5 * s), rgb("9aa1ab"), t, seed + 1, tinta=3 * s)
    for k in range(5):
        a = math.radians(-160 + 35 * k)
        linea(im, [(x + 58 * s * math.cos(a), y - 6 * s + 58 * s * math.sin(a)), (x + 80 * s * math.cos(a), y - 6 * s + 80 * s * math.sin(a))],
              3.4 * s, col=AMARILLO * 0.9, seed=seed + 2 + k, t=t)


def calavera(im, x, y, s, t, col=None, seed=1800):
    col = BLANCO if col is None else col
    c = curva([(0, -44), (38, -26), (40, 10), (22, 24), (22, 40), (-22, 40), (-22, 24), (-40, 10), (-38, -26)], 6, True)
    forma(im, c * s + np.array([x, y], np.float32), col, t, seed, tinta=3.6 * s)
    for d in (-1, 1):
        forma(im, elipse(x + d * 16 * s, y - 4 * s, 11 * s, 12 * s), TINTA, t, seed + 2 + d, tinta=0, amp=0.4)
    forma(im, curva([(0, 8), (6, 18), (-6, 18)], 3, True) * s + np.array([x, y], np.float32), TINTA, t, seed + 5, tinta=0, amp=0.3)
    for k in range(3):
        linea(im, [(x + (-10 + 10 * k) * s, y + 28 * s), (x + (-10 + 10 * k) * s, y + 38 * s)], 2.4 * s, seed=seed + 6 + k, t=t)


def molecula_o2(im, x, y, s, t, veneno=0.0, seed=1900):
    c = rgb("8fd0f2") * (1 - veneno) + rgb("8fe26a") * veneno
    brillo(im, x, y, 120 * s, c, 0.25 + 0.25 * veneno)
    for d in (-1, 1):
        forma(im, elipse(x + d * 38 * s, y, 48 * s, 48 * s), c, t, seed + d, tinta=4 * s, luz=(BLANCO, -10, 10, 0.3))
        rotulo(im, "O", x + d * 38 * s, y, int(46 * s), BLANCO, t, seed + 3 + d)


def vapor(im, x, y, s, t, n=3, seed=2000, alfa=0.8):
    for k in range(n):
        u = (t * 0.9 + k / n) % 1
        pts = [(x + (k - n / 2) * 18 * s + 14 * s * math.sin(6 * v + t * 3 + k), y - 30 * s - 120 * s * u - 60 * s * v)
               for v in np.linspace(0, 1, 8)]
        linea(im, pts, 6 * s * (1 - u * 0.5), col=BLANCO, seed=seed + k, t=t, alfa=alfa * (1 - u) * 0.85, seco=0.3)
