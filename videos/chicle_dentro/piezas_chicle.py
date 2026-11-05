# -*- coding: utf-8 -*-
"""Utilería del video del chicle: la bolita gris, el mapa del viaje por el cuerpo, comida que se deshace, bacterias,
vellosidades, monedas, calendario, documento, llanta, pegamento, limón, escoba, basurero, caja de chicle antigua."""
import math

import numpy as np

from acuarela import (TINTA, brillo, cinta, clamp, curva, elipse, forma, lavado, linea, mancha_pts, pr, remuestrear, rgb,
                      rotulo, rrect, suave, tr)
from personajes import AMARILLO, BLANCO, ROSA, _ojos

GRIS = rgb("b9b2a8")
GRIS_OSC = rgb("8d857b")
ROSA_CH = rgb("f39bc0")
ROJO = rgb("e35d4a")
VERDE_AC = rgb("c8d94a")
CARNE = rgb("e98f8a")
CARNE_OSC = rgb("b65a5d")
MOCO = rgb("e9f0c8")


def chicle(im, x, y, r, t, seed=7000, col=None, rot=0.0, dientes=True, cara=None):
    """La bolita de chicle masticado: mancha irregular con marcas de dientes y un brillo."""
    col = GRIS if col is None else col
    p = mancha_pts(x, y, r, seed, 0.16, ry=r * 0.82)
    forma(im, p, col, t, seed, tinta=max(2.0, r * 0.07), sombra=(col * 0.72, r * 0.25, r * 0.2, 0.6),
          luz=(BLANCO, -r * 0.3, -r * 0.3, 0.35))
    if dientes and r > 18:
        for k in range(3):
            a = rot + 0.9 + k * 0.45
            cx, cy = x + 0.45 * r * math.cos(a), y + 0.45 * r * math.sin(a)
            linea(im, curva([(cx - r * 0.13, cy), (cx, cy - r * 0.08), (cx + r * 0.13, cy)], 4), max(1.5, r * 0.045),
                  col=col * 0.55, seed=seed + 3 + k, t=t, alfa=0.7)
    brillo(im, x - r * 0.3, y - r * 0.35, r * 0.22, BLANCO, 0.5)
    if cara:
        _ojos(im, cara, [(x - r * 0.25, y - r * 0.05), (x + r * 0.25, y - r * 0.05)], 0, r / 55, t, seed + 9)


def chicle_barra(im, x, y, s, t, seed=7050, col=None, rot=0.0, envuelto=0.0):
    """Barrita/pastilla de chicle rosa (con envoltura que se abre: envuelto 1 = cerrada)."""
    col = ROSA_CH if col is None else col
    forma(im, rrect(x, y, 300 * s, 90 * s, 18 * s, rot), col, t, seed, tinta=4 * s, luz=(BLANCO, -6, -14, 0.3),
          sombra=(col * 0.75, 0, 12 * s, 0.5))
    if envuelto > 0.01:
        forma(im, rrect(x + 150 * s * (1 - envuelto) * math.cos(rot), y + 150 * s * (1 - envuelto) * math.sin(rot),
                        300 * s * envuelto + 6, 100 * s, 10 * s, rot), rgb("f3efe4"), t, seed + 1, tinta=3.6 * s)


# ------------------------------------------------------------ mapa del viaje (silueta con el tubo digestivo)
_RUTA = None


def _ruta():
    """Recorrido en coords locales (silueta de 1 unidad = 1 px a s=1; cabeza arriba en y≈-330)."""
    global _RUTA
    if _RUTA is None:
        boca = [(18, -300), (6, -268), (0, -230), (2, -150), (4, -80)]                      # boca → esófago
        est = [(10, -60), (50, -50), (78, -20), (66, 18), (30, 30)]                        # estómago (curva a la derecha)
        dl = []                                                                             # intestino delgado: espiral
        cx, cy = 0, 120
        for k in range(46):
            a = k * 0.62
            rr = 70 - k * 1.1
            dl.append((cx + rr * math.cos(a) * 0.95, cy + rr * math.sin(a) * 0.62 + 6 * math.sin(k)))
        gr = [(-70, 190), (-92, 120), (-88, 50), (-40, 34), (40, 34), (92, 50), (96, 140), (70, 200), (20, 222), (0, 262)]
        pts = np.array(boca + est + dl + gr, np.float32)
        P, L = remuestrear(curva(pts, 6), 3.0)
        _RUTA = (P, np.array([len(boca), len(boca) + len(est), len(boca) + len(est) + len(dl)]))
    return _RUTA


TRAMOS_RUTA = dict(boca=(0.0, 0.07), esofago=(0.0, 0.12), estomago=(0.12, 0.22), delgado=(0.22, 0.78), grueso=(0.78, 1.0))


def mapa_cuerpo(im, x, y, s, t, u=0.0, resalta=None, rastro=True, alfa=1.0, seed=7100, kuri_en=False):
    """Silueta de la niña en papel claro con el tubo digestivo; la bolita va en la fracción u del recorrido."""
    def T(p):
        return tr(np.asarray(p, np.float32), x, y, s)
    sil_cab = elipse(0, -320, 92, 86)
    sil_cuerpo = curva([(-70, -236), (70, -236), (130, -180), (128, 120), (110, 300), (-110, 300), (-128, 120), (-130, -180)],
                       8, True)
    lavado(im, T(sil_cuerpo), rgb("f6d9c2"), 0.85 * alfa, seed, humedo=10)
    lavado(im, T(sil_cab), rgb("f6d9c2"), 0.85 * alfa, seed + 1, humedo=10)
    linea(im, T(sil_cuerpo), 3.0 * s, seed=seed + 2, t=t, cerrado=True, alfa=0.55 * alfa, punta=False)
    linea(im, T(sil_cab), 3.0 * s, seed=seed + 3, t=t, cerrado=True, alfa=0.55 * alfa, punta=False)
    P, _ = _ruta()
    n = len(P)
    # el tubo (ancho distinto por tramo), resaltado si toca
    for nombre, (a, b) in TRAMOS_RUTA.items():
        if nombre == "boca":
            continue
        i0, i1 = int(a * (n - 1)), int(b * (n - 1)) + 1
        w = {"esofago": 12, "estomago": 30, "delgado": 9, "grueso": 22}[nombre]
        col = {"esofago": rgb("e8a39a"), "estomago": rgb("e48c8c"), "delgado": rgb("eaa08e"), "grueso": rgb("d7907a")}[nombre]
        on = resalta == nombre
        forma(im, T(cinta(P[i0:i1], w, w)), col * (1.0 if on or resalta is None else 0.85) + (0.08 if on else 0),
              t, seed + 10 + len(nombre), tinta=2.6 * s * (1.6 if on else 1), alfa=alfa)
        if on:
            brillo_tubo = P[(i0 + i1) // 2]
            brillo(im, *T([brillo_tubo])[0], 90 * s, AMARILLO, 0.18 * alfa)
    if rastro and u > 0:
        k = int(clamp(u) * (n - 1))
        linea(im, T(P[:k + 1:3]), 3.4 * s, col=AMARILLO * 0.85, seed=seed + 40, t=t, punta=False, alfa=0.9 * alfa)
    k = int(clamp(u) * (n - 1))
    gx, gy = T([P[k]])[0]
    chicle(im, gx, gy, 17 * s, t, seed=seed + 50, dientes=False)
    return gx, gy


# ------------------------------------------------------------ comida, ácido, enzimas
def pan(im, x, y, s, t, seed=7200, deshace=0.0):
    a = 1 - deshace
    if a <= 0.02:
        return
    forma(im, mancha_pts(x, y, 70 * s * (0.4 + 0.6 * a), seed, 0.12 + 0.3 * deshace, ry=50 * s * (0.4 + 0.6 * a)),
          rgb("e1b06a"), t, seed, tinta=3.4 * s, alfa=a, sombra=(rgb("b97b3a"), 0, 10 * s, 0.5))
    if a > 0.4:
        forma(im, mancha_pts(x, y + 6 * s, 48 * s * a, seed + 1, 0.15, ry=30 * s * a), rgb("f6e2b4"), t, seed + 1,
              tinta=0, alfa=a)


def bistec(im, x, y, s, t, seed=7210, deshace=0.0):
    a = 1 - deshace
    if a <= 0.02:
        return
    forma(im, mancha_pts(x, y, 80 * s * (0.4 + 0.6 * a), seed, 0.14 + 0.3 * deshace, ry=52 * s * (0.4 + 0.6 * a)),
          rgb("b5473f"), t, seed, tinta=3.6 * s, alfa=a, luz=(BLANCO, -8, -8, 0.2))
    if a > 0.4:
        linea(im, curva([(x - 50 * s * a, y - 10 * s), (x, y + 8 * s), (x + 46 * s * a, y - 4 * s)], 6), 7 * s,
              col=rgb("f3d6c8"), seed=seed + 1, t=t, alfa=a)


def enzima(im, x, y, s, t, seed=7220, abre=0.5):
    """Pepsina: tijerita-pac-man con ojos."""
    ab = 0.15 + 0.55 * abre
    a = np.linspace(ab, 2 * math.pi - ab, 30)
    pts = np.vstack([[(x, y)], np.stack([x + 30 * s * np.cos(a), y + 30 * s * np.sin(a)], 1)])
    forma(im, pts.astype(np.float32), rgb("8fc2e6"), t, seed, tinta=3 * s)
    forma(im, elipse(x + 2 * s, y - 15 * s, 4.5 * s, 5.5 * s), TINTA, t, seed + 1, tinta=0)


def proteina(im, x, y, s, t, n=7, seed=7230, corte=None, sep=0.0):
    """Cadena de cuentas; corte = índice donde se separa (sep = cuánto)."""
    for k in range(n):
        dx = 0 if corte is None or k < corte else sep * 40 * s
        cx, cy = x + (k - n / 2) * 26 * s + dx, y + 8 * s * math.sin(k * 1.3 + t * 2)
        forma(im, elipse(cx, cy, 11 * s, 11 * s), [rgb("f2a65a"), rgb("e7d35a"), rgb("8fd18a")][k % 3], t, seed + k,
              tinta=2.4 * s)


def bacteria(im, x, y, s, t, seed=7300, col=None, cara="normal", rot=0.0, boca="sonrisa"):
    col = rgb(["9ad07a", "b78fe0", "f2c45a", "7fc7d9"][seed % 4]) if col is None else col
    pts = tr(cinta([(-30, 0), (30, 0)], 36, 36), x, y, s, rot + 0.3 * math.sin(t * 2 + seed))
    forma(im, pts, col, t, seed, tinta=3.2 * s, luz=(BLANCO, -6, -8, 0.3))
    for k in range(4):                                                     # pelitos
        a = rot + k * 1.6 + 0.4 * math.sin(t * 5 + k)
        linea(im, [(x + 34 * s * math.cos(a), y + 22 * s * math.sin(a)), (x + 48 * s * math.cos(a), y + 32 * s * math.sin(a))],
              2.2 * s, seed=seed + 10 + k, t=t)
    _ojos(im, cara, [(x - 9 * s, y - 4 * s), (x + 9 * s, y - 4 * s)], 0, s * 0.7, t, seed + 20)
    if boca == "o":
        forma(im, elipse(x, y + 9 * s, 4 * s, 5 * s), rgb("6a2b2b"), t, seed + 30, tinta=1.6 * s)
    else:
        linea(im, curva([(x - 6 * s, y + 7 * s), (x, y + 11 * s), (x + 6 * s, y + 7 * s)], 4), 2 * s, seed=seed + 30, t=t)


def vellosidad(im, x0, y0, largo, t, seed=7400, col=None, ancho=34, ang=-math.pi / 2):
    col = CARNE if col is None else col
    pts = []
    for k in range(7):
        u = k / 6
        sw = 10 * u * math.sin(t * 1.8 + seed * 0.7 + u * 2)
        pts.append((x0 + math.cos(ang) * largo * u + sw, y0 + math.sin(ang) * largo * u))
    forma(im, cinta(pts, ancho, ancho * 0.75), col, t, seed, tinta=3.0, luz=(BLANCO, -5, -5, 0.22),
          sombra=(col * 0.7, 6, 0, 0.45))


def moneda(im, x, y, r, t, seed=7500, rot=0.0):
    forma(im, elipse(x, y, r, r * 0.92, rot), rgb("d9b45a"), t, seed, tinta=3, luz=(BLANCO, -4, -6, 0.4),
          sombra=(rgb("a07b2a"), 4, 4, 0.5))
    linea(im, elipse(x, y, r * 0.72, r * 0.66, rot), 2.0, seed=seed + 1, t=t, cerrado=True, alfa=0.5, punta=False)


def calendario(im, x, y, s, t, arriba, abajo, seed=7600, col=None):
    col = ROJO if col is None else col
    forma(im, rrect(x, y, 200 * s, 220 * s, 18 * s), BLANCO, t, seed, tinta=4 * s, sombra=(rgb("d8d0c0"), 8, 8, 0.5))
    forma(im, rrect(x, y - 80 * s, 200 * s, 60 * s, 14 * s), col, t, seed + 1, tinta=4 * s)
    for d in (-1, 1):
        linea(im, [(x + d * 50 * s, y - 120 * s), (x + d * 50 * s, y - 88 * s)], 7 * s, seed=seed + 2 + d, t=t)
    rotulo(im, arriba, x, y - 80 * s, int(34 * s), BLANCO, t, seed=seed + 4, tinta=False)
    rotulo(im, abajo, x, y + 30 * s, int(96 * s), TINTA, t, seed=seed + 5, tinta=False)


def documento(im, x, y, w, h, lineas_txt, t, seed=7700, rot=0.0, px=34, sello=None, alfa=1.0):
    forma(im, rrect(x, y, w, h, 10, rot), rgb("fbf6ea"), t, seed, tinta=3.4, sombra=(rgb("d8cfb8"), 8, 10, 0.55), alfa=alfa)
    yy = y - h / 2 + 50
    for k, s_ in enumerate(lineas_txt):
        if s_ == "~":
            for j in range(3):
                linea(im, [(x - w * 0.38, yy + j * 26), (x + w * (0.38 - 0.1 * (j == 2)), yy + j * 26)], 4, col=GRIS_OSC,
                      seed=seed + 30 + k * 3 + j, t=t, alfa=0.6 * alfa, punta=False)
            yy += 90
        else:
            rotulo(im, s_, x, yy, px if k else int(px * 1.15), TINTA if k else rgb("2f4f86"), t, seed=seed + 10 + k,
                   tinta=False, rot=rot, alfa=alfa)
            yy += px * 1.45
    if sello:
        rotulo(im, sello, x + w * 0.22, y + h * 0.33, 40, ROJO, t, seed=seed + 60, rot=-0.25, alfa=alfa)


# ------------------------------------------------------------ objetos
def llanta(im, x, y, r, t, seed=7800):
    forma(im, elipse(x, y, r, r), rgb("3d3a3a"), t, seed, tinta=4, luz=(BLANCO, -r * 0.2, -r * 0.2, 0.15))
    forma(im, elipse(x, y, r * 0.55, r * 0.55), rgb("efe6d2"), t, seed + 1, tinta=3.6)
    for k in range(8):
        a = k * math.pi / 4
        linea(im, [(x + r * 0.62 * math.cos(a), y + r * 0.62 * math.sin(a)), (x + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a))],
              4, col=rgb("6e6a68"), seed=seed + 2 + k, t=t, alfa=0.8)


def pegamento(im, x, y, s, t, seed=7820):
    forma(im, rrect(x, y, 110 * s, 190 * s, 22 * s), BLANCO, t, seed, tinta=4 * s, sombra=(rgb("d8d0c0"), 10, 0, 0.5))
    forma(im, curva([(x - 22 * s, y - 95 * s), (x + 22 * s, y - 95 * s), (x + 8 * s, y - 140 * s), (x - 8 * s, y - 140 * s)], 4, True),
          rgb("e9a33a"), t, seed + 1, tinta=3.4 * s)
    forma(im, rrect(x, y + 10 * s, 86 * s, 70 * s, 10 * s), rgb("4f86c6"), t, seed + 2, tinta=2.6 * s)
    rotulo(im, "PEGA", x, y + 10 * s, int(30 * s), BLANCO, t, seed=seed + 3, tinta=False)


def limon(im, x, y, s, t, seed=7840):
    forma(im, elipse(x, y, 70 * s, 54 * s, 0.2), rgb("a9cf45"), t, seed, tinta=3.8 * s, luz=(BLANCO, -12, -10, 0.35),
          sombra=(rgb("6f9a2a"), 8, 8, 0.5))
    forma(im, elipse(x + 66 * s, y + 14 * s, 10 * s, 8 * s), rgb("8cb83a"), t, seed + 1, tinta=2.6 * s)


def escoba(im, x, y, s, t, rot=0.0, seed=7860):
    forma(im, tr(cinta([(0, -200), (0, 60)], 14, 14), x, y, s, rot), rgb("a86e3c"), t, seed, tinta=3 * s)
    cerdas = curva([(-60, 60), (60, 60), (90, 170), (-90, 170)], 4, True)
    forma(im, tr(cerdas, x, y, s, rot), rgb("e6c06a"), t, seed + 1, tinta=3.4 * s)
    for k in range(7):
        xx = -70 + k * 23
        linea(im, tr([(xx * 0.7, 80), (xx, 162)], x, y, s, rot), 2.2 * s, seed=seed + 2 + k, t=t, alfa=0.6)


def basurero(im, x, y, s, t, seed=7880):
    forma(im, curva([(-80, -100), (80, -100), (64, 110), (-64, 110)], 4, True) * s + np.array([x, y], np.float32),
          rgb("5e9c6e"), t, seed, tinta=4 * s, sombra=(rgb("3d6e4a"), 12, 0, 0.5))
    forma(im, rrect(x, y - 108 * s, 190 * s, 28 * s, 10 * s), rgb("4b7f59"), t, seed + 1, tinta=4 * s)


def caja_antigua(im, x, y, s, t, seed=7900, rot=-0.05):
    forma(im, rrect(x, y, 380 * s, 230 * s, 14 * s, rot), rgb("e8d3a2"), t, seed, tinta=4.4 * s, sombra=(rgb("b99a5e"), 10, 10, 0.5))
    forma(im, rrect(x, y, 330 * s, 180 * s, 10 * s, rot), rgb("2f4f86"), t, seed + 1, tinta=2.6 * s)
    rotulo(im, "ADAMS'", x, y - 50 * s, int(42 * s), AMARILLO, t, seed=seed + 2, rot=rot, tinta=False)
    rotulo(im, "NEW YORK GUM", x, y + 4 * s, int(40 * s), BLANCO, t, seed=seed + 3, rot=rot, tinta=False)
    rotulo(im, "No. 1", x, y + 54 * s, int(34 * s), rgb("f3b3c8"), t, seed=seed + 4, rot=rot, tinta=False)


def hospital(im, x, y, s, t, seed=7920):
    forma(im, rrect(x, y, 140 * s, 140 * s, 30 * s), BLANCO, t, seed, tinta=4 * s)
    forma(im, rrect(x, y, 34 * s, 100 * s, 6 * s), ROJO, t, seed + 1, tinta=0)
    forma(im, rrect(x, y, 100 * s, 34 * s, 6 * s), ROJO, t, seed + 2, tinta=0)


def gota_agua(im, x, y, s, t, seed=7940):
    forma(im, curva([(0, -26), (14, 0), (10, 14), (0, 18), (-10, 14), (-14, 0)], 5, True) * s + np.array([x, y], np.float32),
          rgb("8cc8ee"), t, seed, tinta=2.4 * s, luz=(BLANCO, -3, -5, 0.5))
