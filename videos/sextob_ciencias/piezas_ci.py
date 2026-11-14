# -*- coding: utf-8 -*-
"""Piezas pintadas del video 3 de sexto B (CIENCIAS): globo y balanza, banca, vaso, piedra, gas que se reparte, tanque de gas,
JERINGA con partículas que se aprietan, Tierra con su atmósfera, salón de 100, castillo con murallas, microbios (virus, bacteria,
hongo), glóbulos blancos con trucos (gato = granulocito, mono = monocito, león = linfocito), anticuerpo en Y, calcomanía «¡ESTE ES!»,
cancha con portería (vacuna = partido de práctica; autoinmune = autogol), plato saludable."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_out, elipse, forma, lavado, linea, mancha_pts, pr, rgb, rotulo, rrect,
                      suave)
from kit_amaya import AMAR, AZUL, CAFE, CREMA, GRIS, MORADO, ROJO, VERDE, entra, tarjeta

BLANCO = rgb("fbfaf4")
CIELO = rgb("8fc3e8")
N2 = rgb("5b8fd6")          # nitrógeno (azul)
O2 = rgb("e05a50")          # oxígeno (rojo)
AR = rgb("9a6ad0")          # argón (morado)
CO2 = rgb("8f8f96")         # otros (gris)
PIEL = rgb("f1c7a3")
ROSA = rgb("f3a6b8")
MOCO = rgb("a9d36a")


def _ojos(im, x, y, s, t, seed, cara="feliz", sep=0.38):
    """Ojitos y boca chibi para células y microbios (cara de radio ~60·s)."""
    parp = ((t + seed * 0.37) % 3.7) < 0.12
    for d in (-1, 1):
        ex, ey = x + d * 60 * s * sep, y - 6 * s
        if parp:
            linea(im, [(ex - 8 * s, ey), (ex + 8 * s, ey)], 3 * s, seed=seed + 5 + d, t=t, punta=False)
        else:
            forma(im, elipse(ex, ey, 7 * s, 10 * s), TINTA, t, seed + 5 + d, tinta=0)
            forma(im, elipse(ex + 2 * s, ey - 4 * s, 2.5 * s, 2.5 * s), BLANCO, t, seed + 8 + d, tinta=0)
        if cara == "enojo":
            linea(im, [(ex - d * 12 * s, ey - 20 * s), (ex + d * 10 * s, ey - 12 * s)], 3.5 * s, seed=seed + 11 + d, t=t)
        if cara == "dormido":
            forma(im, elipse(ex, ey - 3 * s, 10 * s, 7 * s), None if False else rgb("ffffff"), t, seed + 13 + d, tinta=0, alfa=0.0)
    my = y + 18 * s
    if cara in ("enojo",):
        linea(im, curva([(x - 14 * s, my + 6 * s), (x, my - 2 * s), (x + 14 * s, my + 6 * s)], 5), 3.5 * s, seed=seed + 15, t=t,
              punta=False)
    elif cara == "boca":
        forma(im, elipse(x, my + 4 * s, 16 * s, 14 * s), rgb("8a3a3a"), t, seed + 15, tinta=2.5 * s)
    elif cara == "susto":
        forma(im, elipse(x, my + 4 * s, 8 * s, 11 * s), rgb("8a3a3a"), t, seed + 15, tinta=2.5 * s)
    elif cara == "flojo":
        linea(im, [(x - 12 * s, my + 2 * s), (x + 12 * s, my + 4 * s)], 3.5 * s, seed=seed + 15, t=t, punta=False)
    else:
        linea(im, curva([(x - 14 * s, my), (x, my + 10 * s), (x + 14 * s, my)], 5), 3.5 * s, seed=seed + 15, t=t, punta=False)


# ------------------------------------------------------------ materia
def globo(im, x, y, s, t, infla=1.0, col=None, seed=0):
    """Globo; infla 0 (desinflado, arrugado) → 1 (redondo)."""
    col = ROJO if col is None else col
    r = (30 + 80 * infla) * s
    bx, by = x, y + 4 * math.sin(t * 2 + seed) * s
    forma(im, elipse(bx, by, r * (0.6 + 0.3 * infla), r), col, t, seed, tinta=4 * s, luz=(rgb("ffffff"), -r * 0.3, -r * 0.4, 0.5))
    forma(im, np.array([(bx - 9 * s, by + r + 10 * s), (bx + 9 * s, by + r + 10 * s), (bx, by + r - 2 * s)], np.float32), col, t,
          seed + 1, tinta=2.5 * s)
    linea(im, curva([(bx, by + r + 10 * s), (bx + 12 * s, by + r + 60 * s), (bx - 8 * s, by + r + 120 * s)], 6), 2.5 * s, seed=seed + 2,
          t=t, punta=False)


def balanza(im, x, y, s, t, inclina=0.0, seed=0, izq=None, der=None):
    """Balanza de dos platos; inclina > 0 baja el plato izquierdo. izq/der(im, x, y) dibujan lo que va encima."""
    a = 0.22 * inclina
    linea(im, [(x, y), (x, y + 260 * s)], 10 * s, CAFE, seed=seed, t=t)
    forma(im, rrect(x, y + 270 * s, 200 * s, 26 * s, 8 * s), CAFE, t, seed + 1, tinta=3 * s)
    dx, dy = 230 * s * math.cos(a), 230 * s * math.sin(a)
    linea(im, [(x - dx, y + dy), (x + dx, y - dy)], 9 * s, rgb("6a4a2a"), seed=seed + 2, t=t)
    forma(im, elipse(x, y, 16 * s, 16 * s), AMAR, t, seed + 3, tinta=3 * s)
    for k, (px, py, f) in enumerate(((x - dx, y + dy, izq), (x + dx, y - dy, der))):
        for d in (-1, 1):
            linea(im, [(px, py), (px + d * 70 * s, py + 110 * s)], 2.5 * s, seed=seed + 4 + k * 2 + d, t=t, punta=False)
        forma(im, elipse(px, py + 112 * s, 90 * s, 16 * s), rgb("c9c2b0"), t, seed + 8 + k, tinta=3 * s)
        if f is not None:
            f(im, px, py + 100 * s)


def banca(im, x, y, s, t, seed=0):
    """Pupitre escolar (base en y)."""
    for d in (-1, 1):
        linea(im, [(x + d * 110 * s, y - 120 * s), (x + d * 120 * s, y)], 8 * s, GRIS, seed=seed + d, t=t)
    forma(im, rrect(x, y - 130 * s, 290 * s, 34 * s, 6 * s, -0.03), rgb("c8955a"), t, seed + 3, tinta=4 * s)
    forma(im, rrect(x + 40 * s, y - 60 * s, 170 * s, 22 * s, 6 * s), rgb("b07a44"), t, seed + 4, tinta=3 * s)
    linea(im, [(x + 120 * s, y - 60 * s), (x + 130 * s, y)], 7 * s, GRIS, seed=seed + 5, t=t)


def vaso(im, x, y, s, t, nivel=0.65, seed=0, col=None):
    """Vaso de vidrio con agua (base en y)."""
    col = CIELO if col is None else col
    w0, w1, h = 120 * s, 90 * s, 190 * s
    vid = np.array([(x - w0 / 2, y - h), (x + w0 / 2, y - h), (x + w1 / 2, y), (x - w1 / 2, y)], np.float32)
    hn = h * nivel
    wn = w1 + (w0 - w1) * nivel
    agua = np.array([(x - wn / 2 + 4 * s, y - hn + 3 * math.sin(t * 3) * s), (x + wn / 2 - 4 * s, y - hn - 3 * math.sin(t * 3) * s),
                     (x + w1 / 2 - 4 * s, y - 4 * s), (x - w1 / 2 + 4 * s, y - 4 * s)], np.float32)
    lavado(im, vid, rgb("dfeff7"), 0.5, seed)
    forma(im, agua, col, t, seed + 1, tinta=0, alfa=0.85)
    linea(im, vid, 4 * s, seed=seed + 2, t=t, cerrado=True, punta=False)
    linea(im, [(x - w0 / 2 + 16 * s, y - h + 20 * s), (x - w1 / 2 + 14 * s, y - 30 * s)], 5 * s, BLANCO, seed=seed + 3, t=t, alfa=0.7)


def piedra(im, x, y, s, t, seed=0):
    forma(im, mancha_pts(x, y, 90 * s, seed, 0.22, ry=62 * s), rgb("9a948a"), t, seed, tinta=4 * s,
          sombra=(rgb("5a5450"), 14 * s, 14 * s, 0.4), luz=(rgb("ffffff"), -20 * s, -18 * s, 0.35))


def particulas(im, x0, y0, x1, y1, n, t, seed=0, col=None, r=10.0, vel=1.0, alfa=1.0):
    """n partículas que se mueven solas dentro de la caja (x0, y0, x1, y1); si la caja se achica, se aprietan."""
    if x1 - x0 < 2 * r or y1 - y0 < 2 * r or alfa <= 0.01:
        return
    col = N2 if col is None else col
    rg = np.random.default_rng(seed)
    fa, fb = rg.uniform(0.6, 1.6, (n, 2)), rg.uniform(0, 6.28, (n, 2))
    for k in range(n):
        u = 0.5 + 0.5 * math.sin(fa[k, 0] * t * vel + fb[k, 0]) * math.cos(0.37 * fa[k, 1] * t * vel + fb[k, 1])
        v = 0.5 + 0.5 * math.sin(fa[k, 1] * t * vel * 1.13 + fb[k, 1]) * math.cos(0.29 * fa[k, 0] * t * vel + fb[k, 0])
        px, py = x0 + r + (x1 - x0 - 2 * r) * u, y0 + r + (y1 - y0 - 2 * r) * v
        c = col[k % len(col)] if isinstance(col, (list, tuple)) else col
        forma(im, elipse(px, py, r, r), c, t, seed + 31 * k, tinta=2.2, alfa=alfa, luz=(rgb("ffffff"), -r * 0.3, -r * 0.3, 0.4))


def tanque(im, x, y, s, t, abierto=0.0, seed=0):
    """Tanque de gas de la casa (cilindro), base en y; abierto 0..1 = sale gas por la válvula."""
    forma(im, rrect(x, y - 190 * s, 210 * s, 380 * s, 70 * s), rgb("e9e6dc"), t, seed, tinta=5 * s,
          sombra=(rgb("8a8478"), 26 * s, 0, 0.45), luz=(rgb("ffffff"), -40 * s, -20 * s, 0.4))
    forma(im, rrect(x, y - 190 * s, 214 * s, 40 * s, 6 * s), rgb("c8473f"), t, seed + 1, tinta=3 * s)
    rotulo(im, "GAS", x, y - 186 * s, 30 * s, CREMA, t, seed=seed + 2, tinta=False)
    forma(im, rrect(x, y - 395 * s, 70 * s, 40 * s, 8 * s), GRIS, t, seed + 3, tinta=3 * s)
    forma(im, rrect(x + 30 * s, y - 420 * s, 60 * s, 18 * s, 6 * s), rgb("6a6a72"), t, seed + 4, tinta=3 * s,
          )
    if abierto > 0.01:
        for k in range(9):
            a = ((t * 0.9 + k / 9) % 1)
            px = x + 70 * s + a * (260 + 40 * math.sin(k)) * s * (1 if k % 2 else 0.6)
            py = y - 440 * s - a * (220 + 30 * k % 3) * s + 30 * math.sin(t * 3 + k) * s
            lavado(im, elipse(px, py, (16 + 60 * a) * s, (14 + 50 * a) * s), rgb("9fc0d8"), 0.75 * (1 - a) * abierto, seed + 10 + k)


# ------------------------------------------------------------ jeringa
def jeringa(im, x, y, s, t, emb=0.0, dedo=1.0, seed=0, n=14, ay=0.0, jala=0.0):
    """Jeringa horizontal; la punta a la izquierda (x, y = centro del cuerpo). Devuelve la x de la cabeza del émbolo.
    emb 0 = émbolo a la mitad (aire adentro) → 1 = empujado hasta donde se puede; jala 0..1 = émbolo jalado hacia afuera.
    dedo = el dedo que tapa la punta (0 = lejos); ay > 0 = el dedo se pone rojo."""
    L, Hh = 560 * s, 130 * s
    xi, xd = x - L / 2, x + L / 2
    pos = xi + L * (0.55 - 0.30 * emb + 0.37 * jala)
    R = L * 0.5 + 120 * s                                       # largo de la varilla
    lavado(im, rrect(x, y + 12 * s, L, Hh, 18 * s), rgb("6a5a4a"), 0.18, seed)
    forma(im, rrect(x, y, L, Hh, 18 * s), rgb("eaf4f8"), t, seed + 1, tinta=0, alfa=0.6)
    particulas(im, xi + 6 * s, y - Hh / 2 + 8 * s, pos - 18 * s, y + Hh / 2 - 8 * s, n, t, seed + 50,
               col=[N2, N2, N2, O2], r=11 * s, vel=1.0 + 1.5 * emb)
    for k in range(1, 8):                                                                     # marcas de mililitros
        mx = xi + L * k / 8
        linea(im, [(mx, y - Hh / 2 + 2), (mx, y - Hh / 2 + 22 * s)], 2.2 * s, seed=seed + 3 + k, t=t, punta=False, alfa=0.7)
    forma(im, rrect(pos + R / 2, y, R, 30 * s, 6 * s), rgb("f4f4f0"), t, seed + 16, tinta=3.5 * s)          # varilla
    forma(im, rrect(pos, y, 26 * s, Hh - 8 * s, 6 * s), rgb("3a3a44"), t, seed + 15, tinta=3 * s)              # goma del émbolo
    forma(im, rrect(pos + R, y, 30 * s, Hh + 40 * s, 8 * s), rgb("f4f4f0"), t, seed + 17, tinta=4 * s)         # donde va el pulgar
    linea(im, rrect(x, y, L, Hh, 18 * s), 5 * s, seed=seed + 12, t=t, cerrado=True, punta=False)
    forma(im, rrect(xi - 40 * s, y, 80 * s, 34 * s, 8 * s), rgb("eaf4f8"), t, seed + 13, tinta=4 * s)          # punta
    forma(im, rrect(xd + 10 * s, y, 26 * s, Hh + 90 * s, 8 * s), rgb("eaf4f8"), t, seed + 14, tinta=4 * s)     # aletas
    if dedo > 0.01:                                                                           # dedo que tapa la punta
        dx = xi - 80 * s - (1 - dedo) * 260 * s
        c = PIEL * (1 - 0.45 * ay) + ROJO * 0.45 * ay
        forma(im, rrect(dx - 60 * s, y, 170 * s, 74 * s, 34 * s), c, t, seed + 20, tinta=4 * s)
        forma(im, elipse(dx + 4 * s, y - 2 * s, 22 * s, 26 * s), rgb("f7dcc8"), t, seed + 21, tinta=2.5 * s)     # uña
    return pos, pos + R


def flecha_empuje(im, x0, y0, x1, y1, t, col=ROJO, ancho=14.0, seed=0, u=1.0):
    if u <= 0.02:
        return
    xe, ye = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    d = np.array([x1 - x0, y1 - y0], np.float32)
    d /= np.hypot(*d) + 1e-6
    nn = np.array([-d[1], d[0]])
    linea(im, [(x0, y0), (xe - d[0] * 20, ye - d[1] * 20)], ancho, col, seed=seed, t=t)
    a = np.array([xe, ye])
    forma(im, np.array([a + d * 18, a - d * 30 + nn * 26, a - d * 30 - nn * 26], np.float32), col, t, seed + 1, tinta=2.5)


# ------------------------------------------------------------ atmósfera
def tierra(im, x, y, r, t, seed=0, atm=1.0, cobija=0.0):
    """La Tierra con su atmósfera (halo azul); cobija 0..1 = la capa se vuelve una cobija de cuadritos."""
    if atm > 0.01:
        for k in range(3):
            rr = r * (1.12 + 0.09 * k) * (0.9 + 0.1 * atm)
            lavado(im, elipse(x, y, rr, rr), rgb("a9d4f2"), 0.32 * atm, seed + k, humedo=14)
    if cobija > 0.01:
        n = 18
        for k in range(n):
            a0 = 2 * math.pi * k / n + t * 0.05
            px, py = x + r * 1.13 * math.cos(a0), y + r * 1.13 * math.sin(a0)
            forma(im, rrect(px, py, r * 0.36 * cobija, r * 0.14 * cobija, 6, a0 + math.pi / 2), [ROSA, AMAR, rgb("a8d8b0")][k % 3], t,
                  seed + 20 + k, tinta=2.2, alfa=0.85)
    forma(im, elipse(x, y, r, r), rgb("3f7fd0"), t, seed + 5, tinta=5, luz=(rgb("ffffff"), -r * 0.35, -r * 0.35, 0.35),
          sombra=(rgb("1f3f80"), r * 0.25, r * 0.25, 0.4))
    for k, (dx, dy, rr) in enumerate(((-0.35, -0.25, 0.42), (0.3, 0.2, 0.36), (0.15, -0.5, 0.22), (-0.2, 0.5, 0.25))):
        forma(im, mancha_pts(x + dx * r, y + dy * r, rr * r, seed + 40 + k, 0.35), rgb("5fae5a"), t, seed + 40 + k, tinta=2.5)


def flecha_abajo(im, x, y, largo, t, col=MORADO, seed=0, u=1.0):
    flecha_empuje(im, x, y, x, y + largo, t, col=col, ancho=10, seed=seed, u=u)


def salon(im, x, y, lado, t, n_col, t0, seed=0, vel=0.012):
    """Salón de 100: cuadrícula 10×10 de cabecitas pintadas por grupos [(n, col), …], una a una desde t0."""
    k = 0
    for (n, col) in n_col:
        for _ in range(n):
            if t < t0 + k * vel:
                return
            i, j = k % 10, k // 10
            cx, cy = x + (i - 4.5) * lado, y + (j - 4.5) * lado
            e = e_back(pr(t, t0 + k * vel, t0 + k * vel + 0.25))
            forma(im, elipse(cx, cy, lado * 0.38 * e, lado * 0.38 * e), col, t, seed + k, tinta=2)
            k += 1


# ------------------------------------------------------------ defensa
def castillo(im, x, y, s, t, seed=0, abre=0.0):
    """Castillo (base en y) con murallas y dos torres."""
    for d in (-1, 1):
        forma(im, rrect(x + d * 300 * s, y - 230 * s, 150 * s, 460 * s, 6 * s), rgb("c9b89a"), t, seed + d, tinta=5 * s,
              sombra=(rgb("8a7a5a"), 20 * s, 0, 0.35))
        for k in range(3):
            forma(im, rrect(x + d * 300 * s + (k - 1) * 50 * s, y - 470 * s, 34 * s, 40 * s, 3 * s), rgb("c9b89a"), t,
                  seed + 5 + k + 3 * d, tinta=3 * s)
        forma(im, np.array([(x + d * 300 * s, y - 640 * s), (x + d * 300 * s + 70 * s, y - 520 * s), (x + d * 300 * s - 70 * s, y - 520 * s)],
                           np.float32), ROJO, t, seed + 12 + d, tinta=4 * s)
    forma(im, rrect(x, y - 170 * s, 460 * s, 340 * s, 6 * s), rgb("d8c8a8"), t, seed + 20, tinta=5 * s)
    for k in range(6):
        forma(im, rrect(x + (k - 2.5) * 76 * s, y - 360 * s, 40 * s, 40 * s, 3 * s), rgb("d8c8a8"), t, seed + 21 + k, tinta=3 * s)
    forma(im, rrect(x, y - 90 * s, 130 * s, 180 * s * (1 - 0.0 * abre), 60 * s), rgb("6a4a2a"), t, seed + 30, tinta=4 * s)
    linea(im, [(x + d * 300 * s, y - 640 * s) for d in (-1,)] + [(x - 300 * s, y - 720 * s)], 4 * s, seed=seed + 31, t=t)
    forma(im, np.array([(x - 300 * s, y - 720 * s), (x - 220 * s, y - 700 * s), (x - 300 * s, y - 680 * s)], np.float32), VERDE, t,
          seed + 32, tinta=3 * s)


def virus(im, x, y, s, t, seed=0, cara="enojo", col=None, flojo=0.0):
    """Virus: bolita con picos; flojo 0..1 = debilitado (pálido, ojeras, curita)."""
    col = rgb("8fc85a") if col is None else col
    col = col * (1 - 0.45 * flojo) + rgb("d8d8c8") * 0.45 * flojo
    r = 60 * s
    for k in range(10):
        a = 2 * math.pi * k / 10 + 0.3 * math.sin(t * 2 + seed)
        linea(im, [(x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a)), (x + r * 1.35 * math.cos(a), y + r * 1.35 * math.sin(a))],
              5 * s, seed=seed + k, t=t)
        forma(im, elipse(x + r * 1.42 * math.cos(a), y + r * 1.42 * math.sin(a), 11 * s, 11 * s), rgb("e05a8a") if not flojo else GRIS,
              t, seed + 20 + k, tinta=2 * s)
    forma(im, elipse(x, y, r, r), col, t, seed + 40, tinta=4.5 * s, luz=(rgb("ffffff"), -r * 0.3, -r * 0.35, 0.35))
    _ojos(im, x, y, s, t, seed + 50, "flojo" if flojo > 0.5 else cara)
    if flojo > 0.5:
        forma(im, rrect(x + 26 * s, y - 34 * s, 50 * s, 18 * s, 6 * s, 0.6), rgb("f2d0a8"), t, seed + 60, tinta=2 * s)


def bacteria(im, x, y, s, t, seed=0, cara="enojo", rot=0.0):
    c, sn = math.cos(rot), math.sin(rot)
    for k in range(4):
        bx = x - 110 * s * c
        by = y - 110 * s * sn
        pts = [(bx - (j * 22 * s) * c + 10 * s * math.sin(t * 6 + j + k) * (-sn) + (k - 1.5) * 14 * s * (-sn),
                by - (j * 22 * s) * sn + 10 * s * math.sin(t * 6 + j + k) * c + (k - 1.5) * 14 * s * c) for j in range(6)]
        linea(im, pts, 3 * s, seed=seed + k, t=t, punta=True)
    forma(im, rrect(x, y, 230 * s, 110 * s, 55 * s, rot), rgb("e8a050"), t, seed + 10, tinta=4.5 * s,
          luz=(rgb("ffffff"), -30 * s, -20 * s, 0.35))
    _ojos(im, x + 20 * s, y, s, t, seed + 20, cara)


def hongo(im, x, y, s, t, seed=0, cara="enojo"):
    forma(im, rrect(x, y + 50 * s, 70 * s, 110 * s, 20 * s), rgb("f4e6c8"), t, seed, tinta=4 * s)
    forma(im, np.array(curva([(x - 120 * s, y + 10 * s), (x - 100 * s, y - 80 * s), (x, y - 110 * s), (x + 100 * s, y - 80 * s),
                              (x + 120 * s, y + 10 * s)], 10)), MORADO, t, seed + 1, tinta=4.5 * s)
    for k, (dx, dy) in enumerate(((-55, -50), (20, -75), (70, -30))):
        forma(im, elipse(x + dx * s, y + dy * s, 14 * s, 11 * s), CREMA, t, seed + 3 + k, tinta=1.5 * s)
    _ojos(im, x, y + 45 * s, s * 0.8, t, seed + 10, cara)


def celula(im, x, y, s, t, seed=0, tipo="gato", cara="feliz", col=None, granos=0.0, come=0.0, letra=""):
    """Glóbulo blanco chibi con el truco: gato (granulocito, orejas de gato y granitos), mono (monocito, orejas redondas de mono;
    come = boca enorme de macrófago), leon (linfocito, melena). letra = 'T' o 'B' en el pecho."""
    col = BLANCO if col is None else col
    r = 80 * s * (1 + 0.5 * come)
    yy = y + 3 * s * math.sin(t * 3 + seed)
    if tipo == "leon":
        for k in range(14):
            a = 2 * math.pi * k / 14 + 0.05 * math.sin(t * 2 + k)
            forma(im, elipse(x + r * 1.05 * math.cos(a), yy + r * 1.05 * math.sin(a), r * 0.36, r * 0.3, a), rgb("e0a040"), t,
                  seed + 60 + k, tinta=2.5 * s)
    if tipo == "gato":
        for d in (-1, 1):
            forma(im, np.array([(x + d * r * 0.25, yy - r * 0.85), (x + d * r * 0.85, yy - r * 1.25), (x + d * r * 0.8, yy - r * 0.45)],
                               np.float32), col, t, seed + 70 + d, tinta=3.5 * s)
            forma(im, np.array([(x + d * r * 0.42, yy - r * 0.8), (x + d * r * 0.76, yy - r * 1.05), (x + d * r * 0.72, yy - r * 0.6)],
                               np.float32), ROSA, t, seed + 73 + d, tinta=0)
    if tipo == "mono":
        for d in (-1, 1):
            forma(im, elipse(x + d * r * 0.98, yy - r * 0.1, r * 0.3, r * 0.34), rgb("c8956a"), t, seed + 70 + d, tinta=3.5 * s)
            forma(im, elipse(x + d * r * 0.98, yy - r * 0.1, r * 0.16, r * 0.2), ROSA, t, seed + 73 + d, tinta=0)
    forma(im, mancha_pts(x, yy, r, seed, 0.08), col, t, seed + 1, tinta=4.5 * s, luz=(rgb("ffffff"), -r * 0.3, -r * 0.3, 0.5),
          sombra=(rgb("b8b8d8"), r * 0.2, r * 0.25, 0.5))
    lavado(im, mancha_pts(x + r * 0.42, yy + r * 0.45, r * 0.2, seed + 2, 0.3), rgb("b8a8e8"), 0.4, seed + 2)    # núcleo
    if granos > 0.01:
        rg = np.random.default_rng(seed + 5)
        for k in range(int(12 * min(1, granos))):
            a, d_ = rg.uniform(0, 6.28), rg.uniform(0.25, 0.8)
            forma(im, elipse(x + r * d_ * math.cos(a), yy + r * d_ * math.sin(a) + r * 0.1, 7 * s, 7 * s), rgb("e05a8a"), t,
                  seed + 80 + k, tinta=1.2 * s)
    _ojos(im, x, yy - r * 0.12, s * (1 + 0.3 * come), t, seed + 30, "boca" if come > 0.4 else cara)
    if letra:
        forma(im, elipse(x - r * 0.45, yy + r * 0.5, 26 * s, 26 * s), AZUL if letra == "T" else ROJO, t, seed + 90, tinta=2.5 * s)
        rotulo(im, letra, x - r * 0.45, yy + r * 0.5 + 3 * s, 34 * s, CREMA, t, seed=seed + 91, tinta=False)


def anticuerpo(im, x, y, s, t, seed=0, rot=0.0, col=None):
    """Anticuerpo en forma de Y."""
    col = AMAR if col is None else col
    c, sn = math.cos(rot), math.sin(rot)

    def P(dx, dy):
        return (x + dx * c - dy * sn, y + dx * sn + dy * c)
    linea(im, [P(0, 60 * s), P(0, 0)], 16 * s, col, seed=seed, t=t, punta=False)
    for d in (-1, 1):
        linea(im, [P(0, 0), P(d * 45 * s, -50 * s)], 16 * s, col, seed=seed + 2 + d, t=t, punta=False)
    for p in ([P(0, 60 * s), P(0, 0)], [P(0, 0), P(-45 * s, -50 * s)], [P(0, 0), P(45 * s, -50 * s)]):
        linea(im, p, 3 * s, seed=seed + 9, t=t, punta=False, alfa=0.8)


def calcomania(im, x, y, s, t, texto="¡ESTE ES!", seed=0, rot=0.0):
    if s <= 0.02:
        return
    forma(im, rrect(x, y, 230 * s, 80 * s, 14 * s, rot), AMAR, t, seed, tinta=3.5 * s)
    rotulo(im, texto, x, y + 3 * s, 40 * s, ROJO, t, seed=seed + 1, tinta=False, rot=rot)


# ------------------------------------------------------------ futbol y salud
def cancha(im, x, y, w, h, t, seed=0):
    forma(im, rrect(x, y, w, h, 20), rgb("6fb35f"), t, seed, tinta=4)
    for k in range(5):
        lavado(im, rrect(x - w / 2 + w * (k + 0.5) / 5, y, w / 10, h - 20, 4), rgb("5a9a4c"), 0.35, seed + 1 + k)
    linea(im, rrect(x, y, w - 40, h - 40, 10), 4, BLANCO, seed=seed + 8, t=t, cerrado=True, punta=False)
    linea(im, [(x, y - h / 2 + 20), (x, y + h / 2 - 20)], 4, BLANCO, seed=seed + 9, t=t, punta=False)
    linea(im, elipse(x, y, 70, 70), 4, BLANCO, seed=seed + 10, t=t, cerrado=True, punta=False)


def porteria(im, x, y, s, t, seed=0, lado=1):
    """Portería vista de frente (base en y)."""
    w, h = 260 * s, 150 * s
    for k in range(7):
        linea(im, [(x - w / 2 + w * k / 6, y - h), (x - w / 2 + w * k / 6, y)], 1.6 * s, rgb("dddddd"), seed=seed + k, t=t, punta=False,
              alfa=0.7)
    for k in range(4):
        linea(im, [(x - w / 2, y - h + h * k / 3), (x + w / 2, y - h + h * k / 3)], 1.6 * s, rgb("dddddd"), seed=seed + 10 + k, t=t,
              punta=False, alfa=0.7)
    linea(im, [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)], 9 * s, BLANCO, seed=seed + 20, t=t, punta=False)


def balon(im, x, y, r, t, seed=0, gira=0.0):
    forma(im, elipse(x, y, r, r), BLANCO, t, seed, tinta=3)
    for k in range(5):
        a = gira + 2 * math.pi * k / 5
        forma(im, elipse(x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), r * 0.22, r * 0.22), TINTA, t, seed + 1 + k, tinta=0)
    forma(im, elipse(x, y, r * 0.25, r * 0.25), TINTA, t, seed + 7, tinta=0)


def plato(im, x, y, s, t, seed=0):
    """Plato saludable: verduras, fruta y frijoles."""
    forma(im, elipse(x, y, 180 * s, 70 * s), BLANCO, t, seed, tinta=4 * s)
    forma(im, elipse(x, y + 4 * s, 140 * s, 48 * s), rgb("eeeae0"), t, seed + 1, tinta=0)
    forma(im, elipse(x - 60 * s, y - 10 * s, 45 * s, 30 * s), rgb("5fae5a"), t, seed + 2, tinta=3 * s)    # brócoli
    forma(im, elipse(x + 10 * s, y - 20 * s, 34 * s, 34 * s), ROJO, t, seed + 3, tinta=3 * s,
          luz=(rgb("ffffff"), -8 * s, -10 * s, 0.4))                                                 # manzana
    linea(im, [(x + 10 * s, y - 52 * s), (x + 16 * s, y - 66 * s)], 4 * s, CAFE, seed=seed + 4, t=t)
    forma(im, rrect(x + 75 * s, y - 4 * s, 70 * s, 26 * s, 12 * s, 0.4), rgb("f08a3a"), t, seed + 5, tinta=3 * s)   # zanahoria
    for k in range(6):
        forma(im, elipse(x - 20 * s + (k % 3) * 18 * s, y + 18 * s + (k // 3) * 10 * s, 9 * s, 6 * s), rgb("6a3a2a"), t, seed + 6 + k,
              tinta=1 * s)


def corredor(im, x, y, s, t, seed=0, col=None):
    """Personita chibi que trota en su lugar."""
    from kit_amaya import gente
    b = abs(math.sin(t * 8)) * 14 * s
    for d in (-1, 1):
        a = math.sin(t * 8) * 0.6 * d
        linea(im, [(x, y + 20 * s - b), (x + 40 * s * math.sin(a), y + 75 * s - b)], 9 * s, rgb("3f5f8f"), seed=seed + d, t=t)
    gente(im, x, y - b, 1.6 * s, t, seed=seed + 5, col=col)
