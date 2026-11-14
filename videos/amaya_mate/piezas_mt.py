# -*- coding: utf-8 -*-
"""Piezas de MATEMÁTICAS en acuarela (amaya_mate): números en fichas, fracciones, pizza en rebanadas, plano cartesiano con el barco
del cuaderno, triángulos con marcas de lados iguales, compás, tenis/chancla, escalera chueca, camisetas de equipo, mariposa."""
import math

import numpy as np

from acuarela import TINTA, curva, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, entra, tarjeta
from piezas_es import ROSA_M, TURQ, ficha

AMARILLO = rgb("f2c14e")
NARANJA = rgb("f2a13c")
ROSA_C = rgb("f6a6a0")
AZUL_C = rgb("b8c7e8")
VERDE_C = rgb("a8d8b0")
LILA_C = rgb("d8b8e8")
MIEL = rgb("f4d38a")


def clamp01(v):
    return max(0.0, min(1.0, v))


# ------------------------------------------------------------ números en fichas
def ancho_car(c, px):
    return px * (0.55 if c in ".," else 1.55)


def digitos(im, txt, x, y, px, t, t_ap=-9.0, seed=0, col=CREMA, cols=None, fuertes=None, paso=0.07, sube=None, txt_col=TINTA):
    """Cifra con una ficha por dígito, centrada en x. cols {i: color}, fuertes {i: 0..1}, sube {i: px}. Devuelve las x de cada carácter."""
    ws = [ancho_car(c, px) for c in txt]
    x0 = x - sum(ws) / 2
    xs = []
    for i, (c, w) in enumerate(zip(txt, ws)):
        cx = x0 + w / 2
        x0 += w
        xs.append(cx)
        e = entra(t, t_ap + paso * i)
        if e <= 0.01:
            continue
        yy = y - (sube or {}).get(i, 0.0)
        if c in ".,":
            forma(im, elipse(cx, yy + px * 0.42, px * 0.13 * e, px * 0.13 * e), ROJO, t, seed + i * 3, tinta=2)
            if c == ",":
                linea(im, [(cx + px * 0.08, yy + px * 0.48), (cx - px * 0.08, yy + px * 0.72)], px * 0.1, ROJO, seed=seed + i * 3 + 1, t=t)
            continue
        ficha(im, c, cx, yy, px * 0.92, t, (cols or {}).get(i, col), seed + i * 3, esc=e, fuerte=(fuertes or {}).get(i, 0.0),
              txt_col=txt_col)
    return xs


def fraccion(im, n, d, x, y, px, t, col=TINTA, seed=0, esc=1.0, linea_col=None):
    """Fracción vertical pintada: numerador, raya y denominador centrados en (x, y)."""
    if esc <= 0.02:
        return
    p = px * esc
    rotulo(im, str(n), x, y - p * 0.62, p, col, t, seed=seed)
    w = p * (0.55 * max(len(str(n)), len(str(d))) + 0.35)
    linea(im, [(x - w / 2, y + p * 0.02), (x + w / 2, y - p * 0.02)], p * 0.1, linea_col if linea_col is not None else col,
          seed=seed + 1, t=t)
    rotulo(im, str(d), x, y + p * 0.68, p, col, t, seed=seed + 2)


# ------------------------------------------------------------ pizza
def _cuna(cx, cy, r, a0, a1, n=14):
    a = np.linspace(a0, a1, n)
    return np.concatenate([[[cx, cy]], np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)]).astype(np.float32)


def pizza(im, x, y, r, t, n=1, seed=0, color_reb=None, comidas=(), u_cortes=1.0, esc=1.0, rot=0.0, separa=None):
    """Pizza vista desde arriba con n rebanadas. color_reb {i: color} tiñe rebanadas; comidas = rebanadas que ya no están (plato)."""
    if esc <= 0.02:
        return
    r = r * esc
    lavado(im, elipse(x + 14 * esc, y + 18 * esc, r * 1.12, r * 1.08), rgb("6a5a4a"), 0.3, seed + 1, humedo=8)
    forma(im, elipse(x, y, r * 1.12, r * 1.12), rgb("f7f4ea"), t, seed + 2, tinta=4 * esc)                        # plato
    forma(im, elipse(x, y, r, r), rgb("d9984a"), t, seed + 3, tinta=5 * esc, luz=(rgb("ffe0a8"), -20, -20, 0.4))  # orilla
    forma(im, elipse(x, y, r * 0.86, r * 0.86), rgb("f6d06a"), t, seed + 4, tinta=0, mota=0.9)                     # queso
    rg = np.random.default_rng(seed)
    for k in range(int(10 + r / 18)):                                                                               # pepperoni
        a, d = rg.uniform(0, 2 * math.pi), r * 0.72 * math.sqrt(rg.uniform(0.04, 1))
        forma(im, elipse(x + d * math.cos(a), y + d * math.sin(a), r * 0.09, r * 0.09), rgb("c8473f"), t, seed + 10 + k,
              tinta=1.8 * esc)
    paso = 2 * math.pi / n
    for i in range(n):
        a0 = rot - math.pi / 2 + i * paso
        if i in comidas:
            forma(im, _cuna(x, y, r * 1.01, a0, a0 + paso), rgb("f7f4ea"), t, seed + 200 + i, tinta=0)
            for k in range(3):                                                                                       # migajas
                aa = a0 + paso * (0.3 + 0.2 * k)
                forma(im, elipse(x + r * 0.6 * math.cos(aa), y + r * 0.6 * math.sin(aa), 5 * esc, 4 * esc), rgb("d9984a"), t,
                      seed + 220 + i * 3 + k, tinta=0)
        elif color_reb and i in color_reb:
            lavado(im, _cuna(x, y, r * 0.98, a0, a0 + paso), color_reb[i], 0.55, seed + 300 + i, humedo=4)
    if n > 1 and u_cortes > 0:
        for i in range(n):
            a = rot - math.pi / 2 + i * paso
            linea(im, [(x, y), (x + r * u_cortes * math.cos(a), y + r * u_cortes * math.sin(a))], 4 * esc, rgb("8a5a34"),
                  seed=seed + 400 + i, t=t)


# ------------------------------------------------------------ plano cartesiano
class Plano:
    """Cuadrícula con origen (ox, oy) en px y lado `paso`; P(x, y) da la posición en pantalla."""

    def __init__(self, ox, oy, paso, nx=9, ny=8):
        self.ox, self.oy, self.paso, self.nx, self.ny = ox, oy, paso, nx, ny

    def P(self, x, y):
        return self.ox + x * self.paso, self.oy - y * self.paso

    def dibujar(self, im, t, seed=0, u=1.0, col_x=AZUL, col_y=ROJO, numeros=True, u_ejes=1.0):
        ox, oy, p = self.ox, self.oy, self.paso
        forma(im, rrect(ox + self.nx * p / 2 + 10, oy - self.ny * p / 2 - 10, self.nx * p + 120, self.ny * p + 120, 14),
              rgb("fbf8ee"), t, seed, tinta=4)
        for i in range(self.nx + 1):
            if u * self.nx >= i:
                linea(im, [(ox + i * p, oy), (ox + i * p, oy - self.ny * p * u)], 2.2, rgb("9ab6c8"), seed=seed + 1 + i, t=t, alfa=0.8)
        for j in range(self.ny + 1):
            if u * self.ny >= j:
                linea(im, [(ox, oy - j * p), (ox + self.nx * p * u, oy - j * p)], 2.2, rgb("9ab6c8"), seed=seed + 30 + j, t=t, alfa=0.8)
        if u_ejes > 0:
            ex = ox + (self.nx + 0.6) * p * u_ejes
            linea(im, [(ox, oy), (ex, oy)], 9, col_x, seed=seed + 60, t=t)
            forma(im, np.array([(ex + 26, oy), (ex - 6, oy - 18), (ex - 6, oy + 18)], np.float32), col_x, t, seed + 61, tinta=3)
            ey = oy - (self.ny + 0.6) * p * u_ejes
            linea(im, [(ox, oy), (ox, ey)], 9, col_y, seed=seed + 62, t=t)
            forma(im, np.array([(ox, ey - 26), (ox - 18, ey + 6), (ox + 18, ey + 6)], np.float32), col_y, t, seed + 63, tinta=3)
        if numeros and u_ejes > 0.6:
            for i in range(self.nx + 1):
                rotulo(im, str(i), ox + i * p, oy + 34, 30, TINTA, t, seed=seed + 70 + i, tinta=False)
            for j in range(1, self.ny + 1):
                rotulo(im, str(j), ox - 30, oy - j * p + 4, 30, TINTA, t, seed=seed + 90 + j, tinta=False)
            rotulo(im, "X", ox + (self.nx + 0.9) * p, oy + 40, 54, col_x, t, seed=seed + 99)
            rotulo(im, "Y", ox - 40, oy - (self.ny + 0.9) * p, 54, col_y, t, seed=seed + 98)

    def punto(self, im, x, y, t, nombre="", seed=0, e=1.0, col=None, dx=-26, dy=-26):
        if e <= 0.01:
            return
        px, py = self.P(x, y)
        forma(im, elipse(px, py, 13 * e, 13 * e), col if col is not None else AMARILLO, t, seed, tinta=3)
        if nombre:
            rotulo(im, nombre, px + dx, py + dy, 40 * e + 1, MORADO, t, seed=seed + 1)


BARCO_CASCO = [(1, 4), (3, 2), (7, 2), (9, 4)]                       # A B C D
BARCO_CHIM = [(6, 4), (6, 6), (5, 6), (5, 7), (4, 7), (4, 4)]        # E F G H I J
BARCO_PUNTOS = {"A": (1, 4), "B": (3, 2), "C": (7, 2), "D": (9, 4), "E": (6, 4), "F": (6, 6), "G": (5, 6), "H": (5, 7),
                "I": (4, 7), "J": (4, 4)}


def barco(im, pl, t, seed=0, e=1.0, alfa=1.0):
    """El barco del cuaderno dibujado sobre el plano (mismas coordenadas)."""
    if e <= 0.01:
        return
    casco = np.array([pl.P(*p) for p in BARCO_CASCO], np.float32)
    chim = np.array([pl.P(*p) for p in BARCO_CHIM], np.float32)
    yb = pl.P(0, 1.5)[1]
    ola = np.array([pl.P(0.2, 1.5), pl.P(8.8, 1.5), pl.P(8.8, 1.0), pl.P(0.2, 1.0)], np.float32)
    lavado(im, ola, rgb("8fb4e0"), 0.55 * alfa * e, seed + 1, humedo=6)
    forma(im, chim, rgb("c8473f"), t, seed + 2, tinta=8, alfa=alfa * e)
    forma(im, casco, rgb("9fb59a"), t, seed + 3, tinta=7, alfa=alfa * e, mota=0.9)
    linea(im, [pl.P(2.7, 2.5), pl.P(7.3, 2.5)], 12, TINTA, seed=seed + 4, t=t, alfa=0.9 * alfa * e)
    for k in range(3):                                                                                   # humo
        a = (t * 0.4 + k / 3) % 1
        hx, hy = pl.P(4.5 + 0.5 * a, 7.3 + 1.2 * a)
        lavado(im, elipse(hx, hy, 18 + 30 * a, 14 + 24 * a), rgb("b8b8c0"), 0.5 * (1 - a) * e, seed + 10 + k, humedo=8)
    _ = yb


# ------------------------------------------------------------ triángulos
def marca_lado(im, a, b, n, t, seed, col=ROJO, s=1.0):
    """n rayitas perpendiculares al centro del lado a-b (lados iguales = mismas rayitas)."""
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    L = math.hypot(x1 - x0, y1 - y0) + 1e-6
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    for k in range(n):
        off = (k - (n - 1) / 2) * 16 * s
        cx, cy = mx + ux * off, my + uy * off
        linea(im, [(cx - nx * 20 * s, cy - ny * 20 * s), (cx + nx * 20 * s, cy + ny * 20 * s)], 6 * s, col, seed=seed + k, t=t)


def triangulo(im, pts, t, col, seed=0, marcas=(0, 0, 0), e=1.0, medidas=None, col_m=ROJO, px_m=40, s_m=1.6):
    if e <= 0.01:
        return
    pts = np.asarray(pts, np.float32)
    c = pts.mean(0)
    pts = c + (pts - c) * e
    forma(im, pts, col, t, seed, tinta=6, luz=(rgb("ffffff"), -10, -10, 0.25))
    for k in range(3):
        a, b = pts[k], pts[(k + 1) % 3]
        if marcas[k]:
            marca_lado(im, a, b, marcas[k], t, seed + 10 + k * 4, col=col_m, s=s_m)
        if medidas:
            mx, my = (a + b) / 2
            dx, dy = (a + b) / 2 - c
            d = math.hypot(dx, dy) + 1e-6
            rotulo(im, medidas[k], mx + dx / d * 50, my + dy / d * 50, px_m * e + 1, TINTA, t, seed=seed + 30 + k)


def compas(im, x, y, alto, abre, ang, t, seed=0):
    """Compás: bisagra arriba en (x, y) girado `ang`; `abre` = separación de las puntas en px."""
    half = math.asin(clamp01(abre / 2 / alto)) if alto > 0 else 0
    for d, col in ((-1, GRIS), (1, rgb("6f7a8a"))):
        a = ang + math.pi / 2 + d * half
        linea(im, [(x, y), (x + alto * math.cos(a), y + alto * math.sin(a))], 11, col, seed=seed + d, t=t)
    a = ang + math.pi / 2 + half
    linea(im, [(x + alto * math.cos(a), y + alto * math.sin(a)), (x + (alto + 26) * math.cos(a), y + (alto + 26) * math.sin(a))],
          6, AMARILLO, seed=seed + 3, t=t)
    forma(im, elipse(x, y, 18, 18), ROJO, t, seed + 4, tinta=3)
    linea(im, [(x, y - 18), (x, y - 50)], 9, rgb("8a5a34"), seed=seed + 5, t=t)


def tenis(im, x, y, s, t, seed=0, col=None, sx=1.0):
    col = col if col is not None else rgb("e8559a")
    pts = np.array([(-70, 20), (-62, -20), (-20, -34), (10, -16), (60, -6), (74, 18), (70, 30), (-70, 30)], np.float32)
    pts[:, 0] *= sx
    forma(im, pts * s + (x, y), col, t, seed, tinta=4 * s)
    linea(im, (np.array([(-74, 30), (74, 30)], np.float32) * s + (x, y)), 10 * s, CREMA, seed=seed + 1, t=t)
    for k in range(3):
        linea(im, np.array([(-34 + 12 * k, -24 + 4 * k), (-14 + 12 * k, -10 + 4 * k)], np.float32) * (s, s) * (sx, 1) + (x, y),
              4 * s, CREMA, seed=seed + 2 + k, t=t)


def chancla(im, x, y, s, t, seed=0):
    forma(im, elipse(x, y + 12 * s, 78 * s, 26 * s), rgb("3f78c8"), t, seed, tinta=4 * s)
    linea(im, curva([(x - 30 * s, y + 6 * s), (x, y - 30 * s), (x + 30 * s, y + 6 * s)], 8), 9 * s, AMARILLO, seed=seed + 1, t=t)


def camiseta(im, x, y, s, t, col, num="", seed=0):
    pts = np.array([(-40, -50), (-14, -58), (0, -48), (14, -58), (40, -50), (66, -24), (48, -6), (34, -18), (34, 56), (-34, 56),
                    (-34, -18), (-48, -6), (-66, -24)], np.float32)
    forma(im, pts * s + (x, y), col, t, seed, tinta=4 * s)
    if num:
        rotulo(im, num, x, y + 12 * s, 46 * s, CREMA, t, seed=seed + 1)


def escalera(im, x, y, s, t, seed=0, alturas=(40, 95, 60, 120)):
    """Escalera chueca: escalones de distinta altura y ancho."""
    xx = x
    for k, h in enumerate(alturas):
        w = (60 + 25 * (k % 2)) * s
        forma(im, rrect(xx + w / 2, y - h * s / 2, w, h * s, 4), [MIEL, ROSA_C, AZUL_C, VERDE_C][k % 4], t, seed + k, tinta=3.5 * s)
        xx += w


def mariposa(im, x, y, fr1, fr2, t, t_alas, t_cruz1, t_cruz2, seed=0, px=90, res=None, t_res=1e9, t_abajo=1e9, abajo=None):
    """Método de la mariposa para a/b + c/d: alas de acuarela, dos flechas cruzadas (a×d, c×b) y la multiplicación de abajo."""
    (a, b), (c, d) = fr1, fr2
    x1, x2 = x - px * 1.3, x + px * 1.3
    ea = entra(t, t_alas - 0.3)
    if ea > 0.01:
        for dd, col in ((-1, ROSA_C), (1, LILA_C)):
            lavado(im, elipse(x + dd * px * 1.35, y - px * 0.25, px * 1.0 * ea, px * 1.15 * ea, rot=dd * 0.5), col, 0.55, seed + 1 + dd,
                   humedo=7)
            lavado(im, elipse(x + dd * px * 1.15, y + px * 0.85, px * 0.7 * ea, px * 0.6 * ea, rot=-dd * 0.4), col, 0.45, seed + 5 + dd,
                   humedo=7)
        linea(im, [(x, y - px * 1.1), (x, y + px * 1.1)], 10, TINTA, seed=seed + 9, t=t)
        for dd in (-1, 1):
            linea(im, curva([(x, y - px * 1.1), (x + dd * 18, y - px * 1.5), (x + dd * 40, y - px * 1.65)], 6), 4, seed=seed + 10 + dd, t=t)
    fraccion(im, a, b, x1, y, px, t, col=MORADO, seed=seed + 20)
    rotulo(im, "+", x, y + 6, px * 0.9, ROJO, t, seed=seed + 24)
    fraccion(im, c, d, x2, y, px, t, col=MORADO, seed=seed + 26)
    for k, (t0, p0, p1, txt, col) in enumerate(((t_cruz1, (x1 + px * 0.35, y - px * 0.6), (x2 - px * 0.2, y + px * 0.6),
                                                 f"{a} x {d} = {a * d}", ROJO),
                                                (t_cruz2, (x2 - px * 0.35, y - px * 0.6), (x1 + px * 0.2, y + px * 0.6),
                                                 f"{c} x {b} = {c * b}", AZUL))):
        u = suave(pr(t, t0 - 0.2, t0 + 0.5))
        if u <= 0:
            continue
        q = (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u)
        linea(im, [p0, q], 8, col, seed=seed + 40 + k, t=t)
        rotulo(im, txt, x + (-1 if k == 0 else 1) * px * 2.6, y - px * 1.35, px * 0.5 * entra(t, t0) + 1, col, t, seed=seed + 44 + k)
    if abajo and t > t_abajo - 0.2:
        rotulo(im, abajo, x, y + px * 1.75, px * 0.5 * entra(t, t_abajo - 0.2) + 1, VERDE, t, seed=seed + 50)
    if res and t > t_res - 0.3:
        e = entra(t, t_res - 0.3)
        rotulo(im, "=", x + px * 2.5, y + 6, px * 0.9 * e + 1, MORADO, t, seed=seed + 52)
        tarjeta(im, x + px * 3.55, y, px * 1.5 * e + 1, px * 2.4 * e + 1, t, rgb("fff2c0"), seed + 53, rot=0.03)
        fraccion(im, res[0], res[1], x + px * 3.55, y, px, t, col=VERDE, seed=seed + 54, esc=e)
