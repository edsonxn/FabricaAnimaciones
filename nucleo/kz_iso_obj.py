# -*- coding: utf-8 -*-
"""Objetos del mundo isométrico (estilo Kurzgesagt): vegetación mexicana, roca, cercas, fuego, humo, carretas, barriles, banderas…
Todos: fn(lz, iso, x, y, ...) con (x, y) = posición en el suelo del mundo. Las copas, nopales y demás son «carteles» en pantalla (como en el original)."""
import math

import numpy as np

from motor import circulo, elipse, rect_red, h01, catmull
import plano as P
from kz_iso import tint, tonos, sombra_elipse, caja, techo_dos_aguas, cilindro, C30, S30

VERDES = [(78, 172, 96), (96, 184, 92), (62, 150, 98), (120, 190, 84), (70, 160, 116)]
TRONCO = (186, 108, 70)


def _k(iso):
    return iso.z


# ------------------------------------------------------------------------------------------------ árboles
def arbol(lz, iso, x, y, h=46, color=None, seed=0, t=0.0, sombra=True, tronco=TRONCO):
    """Árbol de copa redonda hecha de racimos de círculos en 3 tonos (luz arriba a la izquierda)."""
    col = color or VERDES[int(h01(seed, 3) * len(VERDES)) % len(VERDES)]
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    if sombra:
        sombra_elipse(lz, iso, x + h * 0.12, y + h * 0.04, h * 0.34, h * 0.20, 0.20)
    tw = max(2.6, h * 0.085)
    lz.relleno(rect_red(sx - tw * k / 2, sy - h * 0.52 * k, tw * k, h * 0.52 * k, 1.2 * k), tint(tronco))
    lz.relleno(rect_red(sx - tw * k / 2, sy - h * 0.52 * k, tw * k * 0.38, h * 0.52 * k, 1.0 * k), tint(P.aclarar(tronco, 0.22)))
    n = 3 + int(h01(seed, 5) * 3)
    r0 = h * 0.30
    sw = 1.2 * math.sin(t * 1.6 + h01(seed, 8) * 6.28)
    lobos = []
    for i in range(n):
        a = h01(seed, 10 + i) * 6.28
        d = r0 * (0.45 + 0.4 * h01(seed, 20 + i)) * (0 if i == 0 else 1)
        lobos.append((math.cos(a) * d, -h * 0.66 + math.sin(a) * d * 0.55, r0 * (0.72 + 0.3 * h01(seed, 30 + i))))
    for (dx, dy, r) in lobos:
        lz.relleno(circulo(sx + (dx + sw) * k, sy + dy * k, r * k, 16), tint(P.oscurecer(col, 0.24)))
    for (dx, dy, r) in lobos:
        lz.relleno(circulo(sx + (dx - r * 0.12 + sw) * k, sy + (dy - r * 0.14) * k, r * 0.86 * k, 16), tint(col))
    for (dx, dy, r) in lobos:
        lz.relleno(circulo(sx + (dx - r * 0.34 + sw) * k, sy + (dy - r * 0.38) * k, r * 0.42 * k, 12), tint(P.aclarar(col, 0.28)))


def arbusto(lz, iso, x, y, r=11, color=None, seed=0, flores=None):
    col = color or VERDES[int(h01(seed, 4) * len(VERDES)) % len(VERDES)]
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    sombra_elipse(lz, iso, x + r * 0.2, y + r * 0.05, r * 0.9, r * 0.6, 0.18)
    for (dx, dy, rr, c) in ((-0.55, -0.45, 0.75, P.oscurecer(col, 0.22)), (0.55, -0.4, 0.7, P.oscurecer(col, 0.22)), (0.0, -0.7, 0.85, P.oscurecer(col, 0.22)),
                            (-0.5, -0.5, 0.62, col), (0.5, -0.45, 0.58, col), (0.0, -0.78, 0.7, col), (-0.55, -0.85, 0.34, P.aclarar(col, 0.28)), (-0.12, -1.0, 0.3, P.aclarar(col, 0.28))):
        lz.relleno(circulo(sx + dx * r * k, sy + dy * r * k, rr * r * k, 12), tint(c))
    if flores:
        for i in range(5):
            lz.relleno(circulo(sx + (h01(seed, 60 + i) - 0.5) * 1.5 * r * k, sy - (0.3 + 0.8 * h01(seed, 70 + i)) * r * k, 0.16 * r * k, 6), tint(flores))


def cipres(lz, iso, x, y, h=52, seed=0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    sombra_elipse(lz, iso, x + 4, y + 1, 6, 4, 0.2)
    lz.relleno(elipse(sx, sy - h * 0.5 * k, h * 0.13 * k, h * 0.5 * k, 0, 18), tint((68, 146, 92)))
    lz.relleno(elipse(sx - h * 0.025 * k, sy - h * 0.53 * k, h * 0.10 * k, h * 0.45 * k, 0, 18), tint((96, 176, 100)))
    lz.relleno(elipse(sx - h * 0.05 * k, sy - h * 0.62 * k, h * 0.04 * k, h * 0.26 * k, 0, 12), tint((140, 204, 110)))
    lz.relleno(elipse(sx, sy - 2 * k, h * 0.10 * k, 3 * k, 0, 10), tint((226, 140, 80)))


def palmera(lz, iso, x, y, h=64, seed=0, t=0.0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    sombra_elipse(lz, iso, x + 6, y + 2, 11, 6, 0.2)
    inc = 0.07 * math.sin(t * 1.2 + seed)
    tx, ty = sx + h * 0.14 * k, sy - h * k
    lz.relleno(np.array([[sx - 2.6 * k, sy], [sx + 2.6 * k, sy], [tx + 2.0 * k, ty], [tx - 2.0 * k, ty]]), tint((176, 128, 92)))
    for i in range(8):
        a = -math.pi / 2 + (i - 3.5) * 0.52 + inc
        L = h * 0.46 * (0.85 + 0.2 * h01(seed, i))
        ex, ey = tx + math.cos(a) * L * k, ty + (math.sin(a) * L * 0.8 + L * 0.35 * (abs(math.cos(a)))) * k
        mx, my = tx + math.cos(a) * L * 0.55 * k, ty + (math.sin(a) * L * 0.6 - 6) * k
        col = (72, 164, 92) if i % 2 else (96, 184, 100)
        lz.relleno(np.array([[tx, ty], [mx - 3 * k * math.sin(a), my + 3 * k * math.cos(a)], [ex, ey], [mx + 3 * k * math.sin(a), my - 3 * k * math.cos(a)]]), tint(col))
    lz.relleno(circulo(tx, ty + 2 * k, 3 * k, 8), tint((176, 128, 92)))


def pino(lz, iso, x, y, h=64, seed=0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    sombra_elipse(lz, iso, x + 5, y + 1, 9, 5, 0.2)
    lz.relleno(rect_red(sx - 2 * k, sy - h * 0.2 * k, 4 * k, h * 0.2 * k, 1), tint((150, 100, 76)))
    for i in range(4):
        w = h * (0.34 - 0.07 * i)
        yb = sy - h * (0.16 + 0.2 * i) * k
        lz.relleno(np.array([[sx - w * k, yb], [sx + w * k, yb], [sx, yb - h * 0.34 * k]]), tint((54, 128, 92)))
        lz.relleno(np.array([[sx - w * k, yb], [sx + w * 0.1 * k, yb], [sx, yb - h * 0.34 * k]]), tint((84, 164, 104)))


def nopal(lz, iso, x, y, s=1.0, seed=0, tunas=True, t=0.0):
    """Nopal: palas ovaladas apiladas con espinas y tunas rojas."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 5 * s, y + 2 * s, 11 * s, 6 * s, 0.18)
    palas = [(0, -14, 11, 15, 0.0), (-12, -34, 9, 13, -0.5), (12, -36, 9, 13, 0.5), (-18, -52, 7, 10, -0.3), (9, -55, 8, 11, 0.2), (-2, -50, 8, 12, 0.0)]
    for (dx, dy, rx, ry, a) in palas:
        lz.relleno(elipse(sx + dx * k, sy + dy * k, rx * k, ry * k, a, 18), tint((60, 150, 96)))
    for (dx, dy, rx, ry, a) in palas:
        lz.relleno(elipse(sx + (dx - 1.5) * k, sy + (dy - 1.5) * k, rx * 0.8 * k, ry * 0.8 * k, a, 18), tint((86, 176, 108)))
        for j in range(3):
            lz.relleno(circulo(sx + (dx + (j - 1) * rx * 0.4) * k, sy + (dy + (j % 2 - 0.5) * ry * 0.7) * k, 0.8 * k, 5), tint((232, 226, 196)))
    if tunas:
        for (dx, dy) in ((-18, -62), (-8, -66), (12, -66), (18, -48)):
            lz.relleno(circulo(sx + dx * k, sy + dy * k, 3.0 * k, 8), tint((214, 64, 96)))


def maguey(lz, iso, x, y, s=1.0, seed=0, t=0.0):
    """Maguey (agave): roseta de pencas azul-verdosas."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 6 * s, y + 2 * s, 13 * s, 7 * s, 0.2)
    n = 11
    for i in range(n):
        a = -math.pi + math.pi * (i + 0.5) / n
        L = (24 + 6 * h01(seed, i)) * (0.7 + 0.5 * abs(math.sin(a)))
        ex, ey = sx + math.cos(a) * L * k, sy - 6 * k + math.sin(a) * L * 0.9 * k
        w = 3.6 * k
        px, py = -math.sin(a) * w, math.cos(a) * w
        col = (92, 156, 150) if i % 2 else (72, 138, 140)
        lz.relleno(np.array([[sx - px * 0.6, sy - 4 * k - py * 0.6], [sx + px * 0.6, sy - 4 * k + py * 0.6], [ex, ey]]), tint(col))
        lz.relleno(np.array([[sx - px * 0.1, sy - 4 * k - py * 0.1], [sx + px * 0.6, sy - 4 * k + py * 0.6], [ex, ey]]), tint(P.oscurecer(col, 0.2)))
    lz.relleno(circulo(sx, sy - 6 * k, 3.6 * k, 8), tint((120, 176, 160)))


def organo(lz, iso, x, y, h=44, seed=0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    sombra_elipse(lz, iso, x + 4, y + 2, 7, 4, 0.18)
    for (dx, hh, w) in ((0, h, 5.2), (-8, h * 0.62, 4.2), (8, h * 0.52, 4.2)):
        lz.relleno(rect_red(sx + (dx - w / 2) * k, sy - hh * k, w * k, hh * k, w * 0.5 * k), tint((64, 150, 96)))
        lz.relleno(rect_red(sx + (dx - w / 2) * k, sy - hh * k, w * 0.38 * k, hh * k, w * 0.3 * k), tint((100, 184, 112)))
    lz.relleno(rect_red(sx - 8 * k, sy - h * 0.3 * k, 16 * k, 3.4 * k, 1), tint((64, 150, 96)))


def milpa(lz, iso, x, y, w, d, t=0.0, seed=0, color=(88, 168, 84)):
    """Campo de maíz: surcos de tierra con plantas altas que se mecen."""
    from kz_iso import suelo_rect
    suelo_rect(lz, iso, x, y, w, d, (170, 118, 84))
    n = max(2, int(d / 13))
    m = max(3, int(w / 11))
    for j in range(n):
        yy = y + (j + 0.5) * d / n
        suelo_rect(lz, iso, x + 2, yy - 2.0, w - 4, 4.0, (146, 98, 72))
    for j in range(n):
        for i in range(m):
            xx = x + (i + 0.5) * w / m
            yy = y + (j + 0.5) * d / n
            sx, sy = iso.P(xx, yy, 0)
            k = iso.z
            sw = 1.4 * math.sin(t * 1.8 + i * 0.7 + j * 1.3)
            for a, L in ((-0.5, 16), (0.45, 18), (0.0, 22), (-0.2, 14)):
                ex, ey = sx + (math.sin(a) * L + sw) * k, sy - math.cos(a) * L * k
                lz.relleno(np.array([[sx - 1.0 * k, sy], [sx + 1.0 * k, sy], [ex, ey]]), tint(color if (i + j) % 2 else P.aclarar(color, 0.15)))
            lz.relleno(circulo(sx + sw * k, sy - 22 * k, 1.6 * k, 5), tint((246, 214, 96)))


def hileras(lz, iso, x, y, w, d, color=(110, 184, 96), t=0.0, tierra=(176, 124, 88), planta="redonda"):
    """Cultivo en hileras (verduras): montículos de tierra con plantitas."""
    from kz_iso import suelo_rect
    suelo_rect(lz, iso, x, y, w, d, tierra)
    n = max(2, int(d / 12))
    m = max(2, int(w / 9))
    for j in range(n):
        suelo_rect(lz, iso, x + 1, y + (j + 0.5) * d / n - 2.2, w - 2, 4.4, P.oscurecer(tierra, 0.18))
        for i in range(m):
            xx, yy = x + (i + 0.5) * w / m, y + (j + 0.5) * d / n
            sx, sy = iso.P(xx, yy, 0)
            k = iso.z
            lz.relleno(circulo(sx, sy - 3 * k, 3.4 * k, 8), tint(color))
            lz.relleno(circulo(sx - 1.0 * k, sy - 4.2 * k, 1.6 * k, 6), tint(P.aclarar(color, 0.3)))
            if planta == "zanahoria":
                lz.relleno(np.array([[sx - 1.4 * k, sy - 2 * k], [sx + 1.4 * k, sy - 2 * k], [sx, sy + 2 * k]]), tint((236, 150, 70)))


# ------------------------------------------------------------------------------------------------ roca, cerca, barril…
def roca(lz, iso, x, y, s=1.0, seed=0, color=(150, 126, 120)):
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 4 * s, y + 1 * s, 10 * s, 6 * s, 0.2)
    pts = np.array([(-10, 0), (-12, -7), (-6, -14), (3, -15), (11, -8), (12, 0)], float) * k + [sx, sy]
    lz.relleno(pts, tint(P.oscurecer(color, 0.25)))
    lz.relleno(np.array([(-10, 0), (-12, -7), (-6, -14), (0, -11), (-1, 0)], float) * k + [sx, sy], tint(color))
    lz.relleno(np.array([(-12, -7), (-6, -14), (-3, -12), (-9, -6)], float) * k + [sx, sy], tint(P.aclarar(color, 0.26)))


def barril(lz, iso, x, y, s=1.0, color=(170, 108, 70)):
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 3 * s, y + 1 * s, 7 * s, 4 * s, 0.2)
    lz.relleno(elipse(sx, sy, 6.4 * k, 3.2 * k, 0, 14), tint(P.oscurecer(color, 0.3)))
    lz.relleno(rect_red(sx - 6.4 * k, sy - 14 * k, 12.8 * k, 14 * k, 2.4 * k), tint(color))
    lz.relleno(rect_red(sx + 0.8 * k, sy - 14 * k, 5.6 * k, 14 * k, 2.4 * k), tint(P.oscurecer(color, 0.22)))
    for yy in (-4, -10):
        lz.relleno(rect_red(sx - 6.6 * k, sy + yy * k - 0.8 * k, 13.2 * k, 1.8 * k, 0.6 * k), tint((92, 64, 56)))
    lz.relleno(elipse(sx, sy - 14 * k, 6.4 * k, 3.2 * k, 0, 14), tint(P.aclarar(color, 0.18)))


def caja_madera(lz, iso, x, y, s=1.0, color=(190, 140, 90)):
    sombra_elipse(lz, iso, x + 3 * s, y + 2 * s, 8 * s, 5 * s, 0.18)
    caja(lz, iso, x - 5 * s, y - 5 * s, 10 * s, 10 * s, 9 * s, color)


def costal(lz, iso, x, y, s=1.0, color=(226, 206, 156)):
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 3 * s, y + 1 * s, 7 * s, 4 * s, 0.18)
    lz.relleno(np.array([(-6, 0), (-7, -8), (-4, -13), (-1.5, -15), (1.5, -15), (4, -13), (7, -8), (6, 0)], float) * k + [sx, sy], tint(P.oscurecer(color, 0.2)))
    lz.relleno(np.array([(-6, 0), (-7, -8), (-4, -13), (-1.5, -15), (0, -14), (0, 0)], float) * k + [sx, sy], tint(color))
    lz.relleno(rect_red(sx - 2.2 * k, sy - 15.8 * k, 4.4 * k, 2.0 * k, 0.6 * k), tint(P.oscurecer(color, 0.4)))


def cerca(lz, iso, pts_xy, h=14, color=(176, 124, 84), poste_cada=14):
    """Cerca de postes y travesaños a lo largo de una polilínea del suelo."""
    p = np.asarray(pts_xy, float)
    for a, b in zip(p[:-1], p[1:]):
        L = float(np.hypot(*(b - a)))
        n = max(1, int(L / poste_cada))
        for z, ancho in ((h * 0.35, 1.8), (h * 0.75, 1.8)):
            q = iso.pts([(a[0], a[1], z), (b[0], b[1], z)])
            _tira(lz, q, tint(color), ancho * max(1.0, iso.z))
        for i in range(n + 1):
            u = i / n
            xx, yy = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            sx, sy = iso.P(xx, yy, 0)
            sy2 = iso.P(xx, yy, h)[1]
            k = iso.z
            lz.relleno(rect_red(sx - 1.6 * k, sy2, 3.2 * k, sy - sy2, 0.8 * k), tint(P.oscurecer(color, 0.15)))


def _tira(lz, seg, color, ancho):
    (xa, ya), (xb, yb) = seg
    d = np.array([xb - xa, yb - ya])
    L = float(np.hypot(*d))
    if L < 1e-6:
        return
    n = np.array([-d[1], d[0]]) / L * ancho / 2
    lz.relleno(np.array([[xa, ya] + n, [xb, yb] + n, [xb, yb] - n, [xa, ya] - n]), color)


def empalizada(lz, iso, pts_xy, h=34, color=(196, 92, 52), grosor=5.2):
    """Muro de troncos con punta redondeada (como la empalizada del diorama de referencia, pero original: troncos de mezquite)."""
    p = np.asarray(pts_xy, float)
    for a, b in zip(p[:-1], p[1:]):
        L = float(np.hypot(*(b - a)))
        n = max(1, int(L / grosor))
        for i in range(n):
            u = (i + 0.5) / n
            xx, yy = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            sx, sy = iso.P(xx, yy, 0)
            k = iso.z
            hh = h * (0.92 + 0.14 * h01(i, int(a[0] + a[1])))
            w = grosor * C30 * 1.15 * k
            lz.relleno(rect_red(sx - w, sy - hh * k, w * 2, hh * k + 1.5 * k, w * 0.9), tint(color))
            lz.relleno(rect_red(sx - w, sy - hh * k, w * 0.8, hh * k + 1.5 * k, w * 0.5), tint(P.aclarar(color, 0.22)))
            lz.relleno(rect_red(sx + w * 0.5, sy - hh * k + w, w * 0.5, hh * k - w, w * 0.2), tint(P.oscurecer(color, 0.22)))


def muro_piedra(lz, iso, x, y, w, d, h, color=(206, 192, 176)):
    c = caja(lz, iso, x, y, w, d, h, color)
    from kz_iso import cara_rect, _linea
    for k in range(1, int(h / 8)):
        cara_rect(lz, iso, c, "y", 0, c.w, k * 8 - 0.5, k * 8 + 0.5, P.oscurecer(color, 0.14), tono=False)
    return c


# ------------------------------------------------------------------------------------------------ fuego, humo, luz
def fuego(lz, iso, x, y, s=1.0, t=0.0, seed=0, z=0.0, halo=True):
    sx, sy = iso.P(x, y, z)
    k = iso.z * s
    f = 0.5 + 0.5 * math.sin(t * 17 + seed * 2.1)
    g = 0.5 + 0.5 * math.sin(t * 11.5 + seed * 5.3)
    if halo:
        lz.halo(sx, sy - 8 * k, 46 * k, (255, 156, 70), alfa=0.35 + 0.1 * f, capa=2)
    for (hh, w, col) in ((17 + 4 * f, 7.2, (232, 70, 40)), (13 + 3 * g, 5.4, (252, 142, 40)), (8 + 2 * f, 3.2, (255, 226, 110))):
        sw = 1.3 * math.sin(t * 9 + seed + hh)
        lz.relleno(np.array([[sx - w * k, sy], [sx - w * 0.5 * k + sw * k, sy - hh * 0.55 * k], [sx + sw * 1.5 * k, sy - hh * k], [sx + w * 0.55 * k + sw * k, sy - hh * 0.5 * k],
                             [sx + w * k, sy]]), tint(col))


def humo(lz, iso, x, y, z, t, n=6, s=1.0, color=(236, 238, 248), vel=14.0, seed=0, alfa=0.7):
    """Bocanadas de humo: círculos que suben, se agrandan y se desvanecen (ciclo continuo)."""
    k = iso.z * s
    for i in range(n):
        u = (t * 0.35 + i / n + h01(seed, i) * 0.3) % 1.0
        sx, sy = iso.P(x, y, z + vel * u * 3.0)
        r = (3.2 + 9.0 * u) * k
        a = alfa * (1 - u) ** 1.4 * min(1.0, u * 8)
        lz.relleno(circulo(sx + 5 * k * math.sin(t * 1.3 + i * 1.9) * u, sy, r, 10), tint(color), alfa=a, capa=2)


def chispas(lz, iso, x, y, z, t, n=8, seed=0, color=(255, 214, 110)):
    sx, sy = iso.P(x, y, z)
    k = iso.z
    for i in range(n):
        u = (t * 0.9 + h01(seed, i) * 3.7) % 1.0
        ox = (h01(seed, i + 40) - 0.5) * 22 * k * u
        lz.relleno(circulo(sx + ox, sy - 36 * u * k, 1.4 * k * (1 - u * 0.6), 5), tint(color), alfa=(1 - u), capa=2)


def antorcha(lz, iso, x, y, t=0.0, h=22, seed=0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    lz.relleno(rect_red(sx - 1.4 * k, sy - h * k, 2.8 * k, h * k, 0.8 * k), tint((150, 100, 70)))
    fuego(lz, iso, x, y, 0.5, t, seed, z=h)


def farol(lz, iso, x, y, h=36, t=0.0, color=(255, 214, 120), encendido=1.0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    lz.relleno(rect_red(sx - 1.2 * k, sy - h * k, 2.4 * k, h * k, 0.6 * k), tint((92, 70, 110)))
    if encendido > 0.02:
        lz.halo(sx, sy - (h + 4) * k, 34 * k, color, alfa=0.45 * encendido, capa=2)
    lz.relleno(rect_red(sx - 4 * k, sy - (h + 9) * k, 8 * k, 10 * k, 2 * k), tint(color if encendido > 0.02 else (200, 190, 170)))


def bandera(lz, iso, x, y, h=64, w=34, alto=22, color=(226, 70, 70), t=0.0, seed=0, escudo=None, franjas=None):
    """Asta con tela que ondea (ola senoidal). franjas = [(color, fracción), ...] horizontal; escudo: callable(lz, cx, cy, k)."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    lz.relleno(rect_red(sx - 1.2 * k, sy - h * k, 2.4 * k, h * k, 0.6 * k), tint((130, 96, 70)))
    lz.relleno(circulo(sx, sy - h * k, 2.2 * k, 8), tint((250, 208, 90)))
    n = 14
    top = sy - h * k + 2 * k
    cols = franjas or [(color, 1.0)]
    y0 = 0.0
    for col, fr in cols:
        ya, yb = alto * y0, alto * (y0 + fr)
        up, dn = [], []
        for i in range(n + 1):
            u = i / n
            off = (3.0 * math.sin(t * 5.5 - u * 5.0 + seed) * u)
            up.append((sx + 1.2 * k + u * w * k, top + (ya + off) * k))
            dn.append((sx + 1.2 * k + u * w * k, top + (yb + off) * k))
        lz.relleno(np.array(up + dn[::-1]), tint(col))
        y0 += fr
    # sombreado de pliegues
    for i in range(1, n, 3):
        u = i / n
        off = 3.0 * math.sin(t * 5.5 - u * 5.0 + seed) * u
        lz.relleno(np.array([(sx + 1.2 * k + u * w * k, top + off * k), (sx + 1.2 * k + (u + 0.09) * w * k, top + 3.0 * math.sin(t * 5.5 - (u + 0.09) * 5 + seed) * (u + 0.09) * k),
                             (sx + 1.2 * k + (u + 0.09) * w * k, top + (alto + 3.0 * math.sin(t * 5.5 - (u + 0.09) * 5 + seed) * (u + 0.09)) * k), (sx + 1.2 * k + u * w * k, top + (alto + off) * k)]),
                   (20, 10, 60), alfa=0.10)
    if escudo is not None:
        off = 3.0 * math.sin(t * 5.5 - 0.5 * 5.0 + seed) * 0.5
        escudo(lz, sx + 1.2 * k + w * 0.5 * k, top + (alto * 0.5 + off) * k, k)


def carreta(lz, iso, x, y, t=0.0, mov=0.0, carga=(214, 180, 96), s=1.0, bultos=False):
    """Carreta de bueyes: caja de madera, dos ruedas grandes, yugo. `mov` > 0 hace girar las ruedas."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 8 * s, y + 3 * s, 24 * s, 11 * s, 0.2)
    rot = t * mov * 3.0
    for dx in (-11, 9):
        lz.relleno(circulo(sx + dx * k, sy - 7 * k, 8.0 * k, 16), tint((126, 84, 62)))
        lz.relleno(circulo(sx + dx * k, sy - 7 * k, 5.6 * k, 14), tint((176, 126, 88)))
        for j in range(4):
            a = rot + j * math.pi / 4
            lz.relleno(np.array([[sx + dx * k + math.cos(a) * 5.6 * k, sy - 7 * k + math.sin(a) * 5.6 * k], [sx + dx * k - math.cos(a) * 5.6 * k, sy - 7 * k - math.sin(a) * 5.6 * k],
                                 [sx + dx * k - math.cos(a) * 5.6 * k + 1.2 * k, sy - 7 * k - math.sin(a) * 5.6 * k], [sx + dx * k + math.cos(a) * 5.6 * k + 1.2 * k, sy - 7 * k + math.sin(a) * 5.6 * k]]), tint((126, 84, 62)))
    lz.relleno(rect_red(sx - 18 * k, sy - 22 * k, 36 * k, 10 * k, 1.2 * k), tint((166, 112, 78)))
    lz.relleno(rect_red(sx - 18 * k, sy - 22 * k, 14 * k, 10 * k, 1.2 * k), tint((196, 140, 96)))
    lz.relleno(elipse(sx, sy - 25 * k, 17 * k, 6 * k, 0, 16), tint(carga))
    lz.relleno(elipse(sx - 4 * k, sy - 27 * k, 9 * k, 3 * k, 0, 12), tint(P.aclarar(carga, 0.25)))
    if bultos:       # mudanza: colchón enrollado, costales, caja y silla que se mecen con el camino
        bz = 1.4 * math.sin(t * 7 + x * 0.1) * k
        lz.relleno(rect_red(sx - 15 * k, sy - 38 * k + bz, 12 * k, 14 * k, 2 * k), tint((196, 110, 90)))
        lz.relleno(rect_red(sx - 15 * k, sy - 38 * k + bz, 5 * k, 14 * k, 2 * k), tint((226, 150, 120)))
        lz.relleno(rect_red(sx - 1 * k, sy - 36 * k - bz, 12 * k, 11 * k, 2 * k), tint((236, 214, 160)))
        lz.relleno(circulo(sx + 15 * k, sy - 33 * k + bz, 6 * k, 10), tint((150, 100, 70)))
        lz.relleno(rect_red(sx - 6 * k, sy - 46 * k + bz, 14 * k, 10 * k, 1.6 * k), tint((120, 150, 190)))
        lz.relleno(rect_red(sx + 4 * k, sy - 52 * k - bz, 2 * k, 14 * k, 0.6 * k), tint((140, 96, 70)))
        lz.relleno(rect_red(sx + 4 * k, sy - 52 * k - bz, 9 * k, 2 * k, 0.6 * k), tint((140, 96, 70)))


def pozo(lz, iso, x, y, s=1.0):
    cilindro(lz, iso, x, y, 9 * s, 10 * s, (196, 178, 160))
    sx, sy = iso.P(x, y, 10 * s)
    k = iso.z * s
    lz.relleno(elipse(sx, sy, 6.6 * k, 3.4 * k, 0, 14), tint((70, 120, 170)))
    for dx in (-8, 8):
        lz.relleno(rect_red(sx + dx * k - 1.2 * k, sy - 24 * k, 2.4 * k, 24 * k, 0.6 * k), tint((136, 96, 70)))
    lz.relleno(np.array([[sx - 11 * k, sy - 22 * k], [sx + 11 * k, sy - 22 * k], [sx, sy - 31 * k]]), tint((196, 92, 74)))


def fuente(lz, iso, x, y, t=0.0, s=1.0):
    """Fuente de plaza: pila octogonal, columna y chorros."""
    from kz_iso import suelo_curvo
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    th = np.linspace(0, 2 * math.pi, 8, endpoint=False)
    for r, z, col in ((16, 0, (226, 214, 198)), (14, 5, (92, 190, 208))):
        lz.relleno(iso.pts(np.column_stack([x + r * s * np.cos(th + 0.39), y + r * s * np.sin(th + 0.39), np.full(8, z * s)])), tint(col))
    lz.relleno(rect_red(sx - 1.8 * k, sy - 22 * k, 3.6 * k, 20 * k, 1), tint((226, 214, 198)))
    lz.relleno(elipse(sx, sy - 22 * k, 7 * k, 3 * k, 0, 12), tint((226, 214, 198)))
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * 0.34
        u = (t * 1.1 + i * 0.17) % 1.0
        for j in range(5):
            uu = (u + j * 0.14) % 1.0
            px = sx + math.cos(a) * 18 * uu * k
            py = sy - 22 * k - math.sin(-a) * 0 - (math.sin(math.pi * uu) * 14 - 8 * uu) * k
            lz.relleno(circulo(px, py, 1.2 * k, 5), tint((226, 246, 255)), alfa=0.9, capa=2)
    lz.halo(sx, sy - 6 * k, 30 * k, (150, 230, 240), alfa=0.18, capa=2)


# ------------------------------------------------------------------------------------------------ agua
def agua(lz, iso, pts_xy, t, c1=(58, 150, 220), c2=(40, 112, 200), espuma=(236, 248, 255), z=-1.0, seed=0):
    """Masa de agua sobre el suelo: relleno plano, franjas claras que se desplazan y borde de espuma."""
    from kz_iso import suelo
    suelo(lz, iso, pts_xy, c1, z)
    a = np.asarray(pts_xy, float)
    x0, y0, x1, y1 = a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()
    q = iso.pts(np.column_stack([a[:, 0], a[:, 1], np.full(len(a), z)]))
    with lz.recorte(q):
        n = int((y1 - y0) / 22) + 2
        for i in range(n):
            yy = y0 + i * 22 + 6 * math.sin(t * 0.9 + i)
            for j in range(3):
                xx = x0 + ((j * 0.37 + i * 0.173 + t * 0.012 * (1 + 0.4 * (i % 3)) + h01(seed, i, j) * 0.3) % 1.0) * (x1 - x0)
                L = 26 + 20 * h01(seed, i + 7, j)
                p = iso.pts([(xx, yy, z), (xx + L, yy, z), (xx + L, yy + 2.2, z), (xx, yy + 2.2, z)])
                lz.relleno(p, tint(c2 if (i + j) % 2 else P.aclarar(c1, 0.22)), alfa=0.55)
    lz.trazo(q, (*espuma, 150), 3.0 * iso.z, cerrado=True, afinar=False, temblor=0.0)


class Caravana:
    """n burros con arriero que recorren un trayecto en fila (todo función de t)."""

    def __init__(self, trayecto, n=4, vel=14.0, fase=0.0, carga=True, seed=0, arriero=True):
        self.p = np.asarray(trayecto, float)
        self.d = np.r_[0, np.cumsum(np.hypot(*np.diff(self.p, axis=0).T))]
        self.n, self.vel, self.fase, self.carga, self.seed, self.arriero = n, vel, fase, carga, seed, arriero

    def _en(self, s):
        L = self.d[-1]
        m = s % (2 * L)
        sentido = 1 if m <= L else -1
        s = m if m <= L else 2 * L - m
        i = int(np.clip(np.searchsorted(self.d, s, side="right") - 1, 0, len(self.p) - 2))
        seg = self.p[i + 1] - self.p[i]
        f = (s - self.d[i]) / max(self.d[i + 1] - self.d[i], 1e-6)
        dr = seg / max(np.hypot(*seg), 1e-6) * sentido
        return self.p[i] + seg * f, dr

    def dibujar(self, mundo, t):
        import kz_gente_iso as G
        for k in range(self.n):
            s = (t * self.vel + self.fase * self.d[-1]) - k * 22
            pos, dr = self._en(s)
            lado = 1 if ((dr[0] - dr[1]) >= 0) else -1
            mundo.add(pos[0] - 6, pos[1] - 6, pos[0] + 6, pos[1] + 6, 24, (lambda pos, lado, k: (lambda lz, iso: G.burro(lz, iso, pos[0], pos[1], t, dir=lado, carga=self.carga, seed=self.seed + k)))(pos, lado, k),
                      fijo=False, clave=pos[0] + pos[1])
        if self.arriero:
            pos, dr = self._en(t * self.vel + self.fase * self.d[-1] + 16)
            mundo.add(pos[0] - 4, pos[1] - 4, pos[0] + 4, pos[1] + 4, 36, lambda lz, iso: G.persona(lz, iso, pos[0], pos[1], t, "arriero", dir=tuple(dr), vel=self.vel / 18.0, seed=self.seed + 99), fijo=False,
                      clave=pos[0] + pos[1])



def bahia(lz, iso, pts_xy, t, seed=0, c_orilla=(112, 214, 222), c_medio=(58, 156, 220), c_hondo=(36, 104, 196), z=-1.0, espuma=(240, 250, 255), olas=True):
    """Bahía/lago orgánico: tres anillos concéntricos (orilla turquesa -> azul -> profundo), crestas de ola que avanzan hacia la orilla y espuma que respira en el borde."""
    from kz_iso import suelo_curvo
    p = np.asarray(pts_xy, float)
    c = p.mean(0)
    def anillo(f):
        return c + (p - c) * f
    suelo_curvo(lz, iso, p, c_orilla, z, n=8)
    suelo_curvo(lz, iso, anillo(0.82), c_medio, z, n=8)
    suelo_curvo(lz, iso, anillo(0.55), c_hondo, z, n=8)
    q = iso.pts(np.column_stack([*(np.array(catmull(p, 8, True)).T), np.full(len(catmull(p, 8, True)), z)]))
    if olas:
        with lz.recorte(q):
            x0, y0, x1, y1 = p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()
            n = int((y1 - y0) / 18) + 2
            for i in range(n):
                for j in range(3):
                    xx = x0 + ((j * 0.34 + i * 0.211 + t * 0.016 * (1 + 0.5 * ((i + j) % 3)) + h01(seed, i, j) * 0.4) % 1.0) * (x1 - x0)
                    yy = y0 + i * 18 + 5 * math.sin(t * 0.9 + i + j)
                    L = 22 + 22 * h01(seed, i + 7, j)
                    arco = [(xx + L * u, yy + 3.0 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 7)]
                    for a, b in zip(arco[:-1], arco[1:]):
                        _tira(lz, iso.pts([(a[0], a[1], z), (b[0], b[1], z)]), tint(espuma), max(1.0, 1.8 * iso.z)) if False else None
                    lz.relleno(iso.pts([(xx, yy, z), (xx + L, yy, z), (xx + L, yy + 2.0, z), (xx, yy + 2.0, z)]), tint(P.aclarar(c_medio, 0.5)), alfa=0.7)
    # espuma que respira en la orilla
    alfa = 0.55 + 0.35 * math.sin(t * 1.6 + seed)
    lz.trazo(q, (*espuma, int(255 * alfa)), 3.4 * iso.z, cerrado=True, afinar=False, temblor=0.0)
    lz.trazo(iso.pts(np.column_stack([*(np.array(catmull(anillo(0.96), 8, True)).T), np.full(len(catmull(anillo(0.96), 8, True)), z)])), (*espuma, int(120 * alfa)), 2.0 * iso.z, cerrado=True, afinar=False, temblor=0.0)
