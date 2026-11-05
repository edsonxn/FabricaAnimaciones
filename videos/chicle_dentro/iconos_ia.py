# -*- coding: utf-8 -*-
"""Iconos y utilería pintados a pincel para los planos e-k: la TORRE de pisos dentro de la cabeza de Kuri, las piezas que
arma cada piso (esquina, curva, rayado, ojo, oreja, nariz, bigotes, cara de gato, rueda, letrero de alto), perillas en
rejilla, tostadora, perro/lobo, panda, tarjeta gráfica, trofeo, gente chibi, estrella y marcadores."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect, suave)
from personajes import AMARILLO, BLANCO, OJO_K

NARANJA = rgb("f2a13c")
ROSA = rgb("f3a7b8")
PISOS_COL = [rgb("cfe8ea"), rgb("d9e9c8"), rgb("f6e2b4"), rgb("f3cfd6")]
PISOS_NOM = ["BORDES", "TEXTURAS", "PARTES", "OBJETOS"]


# ------------------------------------------------------------ piezas
def esquina(im, x, y, s, t, seed=0, col=TINTA):
    linea(im, [(x - 40 * s, y - 40 * s), (x - 40 * s, y + 36 * s), (x + 40 * s, y + 36 * s)], 8 * s, col=col, seed=seed, t=t, punta=False)


def curvita(im, x, y, s, t, seed=0, col=TINTA):
    linea(im, curva([(x - 44 * s, y + 30 * s), (x - 10 * s, y - 40 * s), (x + 44 * s, y - 10 * s)], 8), 8 * s, col=col, seed=seed, t=t)


def rayado(im, x, y, s, t, seed=0):
    forma(im, rrect(x, y, 100 * s, 90 * s, 14 * s), NARANJA, t, seed, tinta=3 * s)
    for k in range(4):
        linea(im, curva([(x - 40 * s + 22 * k * s, y - 38 * s), (x - 32 * s + 22 * k * s, y), (x - 40 * s + 22 * k * s, y + 38 * s)], 6),
              6 * s, col=rgb("b0601e"), seed=seed + 1 + k, t=t, punta=True)


def ojo(im, x, y, s, t, seed=0):
    forma(im, elipse(x, y, 58 * s, 38 * s), rgb("cfe08a"), t, seed, tinta=5 * s)
    forma(im, elipse(x, y, 12 * s, 32 * s), TINTA, t, seed + 1, tinta=0)
    brillo(im, x + 10 * s, y - 12 * s, 6 * s, BLANCO, 1.2)


def oreja(im, x, y, s, t, seed=0, cabeza=False):
    """Oreja de gato: lados curvos, punta redondeada, interior rosa con pelitos; cabeza=True añade el arco de la cabeza."""
    if cabeza:
        forma(im, elipse(x + 20 * s, y + 92 * s, 120 * s, 56 * s), NARANJA, t, seed + 4, tinta=5 * s)
    forma(im, curva([(x - 52 * s, y + 50 * s), (x - 36 * s, y - 6 * s), (x - 4 * s, y - 62 * s), (x + 10 * s, y - 64 * s),
                     (x + 34 * s, y - 8 * s), (x + 54 * s, y + 50 * s)], 8, True), NARANJA, t, seed, tinta=5 * s,
          sombra=(rgb("c87428"), 6 * s, 6 * s, 0.4))
    forma(im, curva([(x - 30 * s, y + 40 * s), (x - 18 * s, y - 2 * s), (x + 2 * s, y - 38 * s), (x + 20 * s, y - 2 * s),
                     (x + 32 * s, y + 40 * s)], 8, True), ROSA, t, seed + 1, tinta=0)
    for k in range(3):
        linea(im, [(x - 12 * s + 12 * k * s, y + 40 * s), (x - 16 * s + 14 * k * s, y + 8 * s)], 3 * s, col=BLANCO * 0.95,
              seed=seed + 2 + k, t=t)


def nariz(im, x, y, s, t, seed=0):
    forma(im, np.array([(x - 30 * s, y - 18 * s), (x + 30 * s, y - 18 * s), (x, y + 22 * s)], np.float32), ROSA, t, seed, tinta=5 * s)


def bigotes(im, x, y, s, t, seed=0):
    for k in range(3):
        for d in (-1, 1):
            linea(im, curva([(x + d * 10 * s, y + (k - 1) * 14 * s), (x + d * 50 * s, y + (k - 1) * 20 * s - 4 * s),
                             (x + d * 80 * s, y + (k - 1) * 28 * s)], 5), 4 * s, seed=seed + k * 2 + (d > 0), t=t)


def cara_gato(im, x, y, s, t, seed=0):
    for d in (-1, 1):
        forma(im, np.array([(x + d * 30 * s, y - 50 * s), (x + d * 70 * s, y - 110 * s), (x + d * 86 * s, y - 30 * s)], np.float32),
              NARANJA, t, seed + 5 + (d > 0), tinta=4.4 * s)
    forma(im, elipse(x, y, 100 * s, 80 * s), NARANJA, t, seed, tinta=5 * s, sombra=(rgb("c87428"), 0, 10 * s, 0.4))
    for d in (-1, 1):
        forma(im, elipse(x + d * 36 * s, y - 10 * s, 14 * s, 18 * s), rgb("cfe08a"), t, seed + 8 + (d > 0), tinta=3 * s)
        forma(im, elipse(x + d * 36 * s, y - 10 * s, 5 * s, 14 * s), TINTA, t, seed + 10 + (d > 0), tinta=0)
    nariz(im, x, y + 18 * s, 0.45 * s, t, seed + 12)
    bigotes(im, x, y + 30 * s, 0.8 * s, t, seed + 14)


def rueda(im, x, y, s, t, seed=0):
    forma(im, elipse(x, y, 80 * s, 80 * s), rgb("4a4a52"), t, seed, tinta=5 * s)
    forma(im, elipse(x, y, 62 * s, 62 * s), rgb("eef0f2"), t, seed + 1, tinta=3 * s)
    for k in range(8):
        a = k / 8 * math.pi + t * 0.4
        linea(im, [(x - 60 * s * math.cos(a), y - 60 * s * math.sin(a)), (x + 60 * s * math.cos(a), y + 60 * s * math.sin(a))],
              2.4 * s, col=rgb("8a8f98"), seed=seed + 2 + k, t=t, punta=False)
    forma(im, elipse(x, y, 10 * s, 10 * s), rgb("8a8f98"), t, seed + 12, tinta=2 * s)


def alto(im, x, y, s, t, seed=0):
    pts = np.array([(x + 80 * s * math.cos(math.pi / 8 + k * math.pi / 4), y + 80 * s * math.sin(math.pi / 8 + k * math.pi / 4))
                    for k in range(8)], np.float32)
    forma(im, pts, rgb("d8433a"), t, seed, tinta=5 * s, luz=(BLANCO, -10 * s, 12 * s, 0.25))
    rotulo(im, "ALTO", x, y, int(46 * s) + 2, BLANCO, t, seed=seed + 1, tinta=False)


PIEZAS = {"esquina": esquina, "curva": curvita, "rayado": rayado, "ojo": ojo, "oreja": oreja, "nariz": nariz, "bigotes": bigotes,
          "cara": cara_gato, "rueda": rueda, "alto": alto}


def trazo(im, x, y, s, t, ang, col, seed=0):
    """Un filtro del piso 1: rayita de color con cierta inclinación."""
    linea(im, [(x - 26 * s * math.cos(ang), y + 26 * s * math.sin(ang)), (x + 26 * s * math.cos(ang), y - 26 * s * math.sin(ang))],
          7 * s, col=col, seed=seed, t=t, punta=False)


# ------------------------------------------------------------ la torre
def torre(im, t, x=760, y0=960, w=760, alto_p=180, crece=1.0, activo=(1, 1, 1, 1), contenido=True, foco=-1, seed=6000):
    """Torre de 4 pisos (de abajo arriba) con ventanas por las que se ve lo que arma cada piso.
    crece 0..1 = cuánto se ha levantado; activo[k] 0..1 = cuánto brilla el piso k; foco = piso señalado (marco amarillo).
    Devuelve [(cx, cy, w, h)] de cada piso."""
    out = []
    for k in range(4):
        e = e_back(clamp(crece * 4 - k))
        y = y0 - alto_p / 2 - k * alto_p
        wk = w - 70 * k
        out.append((x, y, wk, alto_p))
        if e <= 0.02:
            continue
        a = activo[k]
        col = PISOS_COL[k] * (0.55 + 0.45 * a)
        forma(im, rrect(x, y + alto_p * (1 - e) / 2, wk, (alto_p - 14) * e, 14), col, 0, seed + k, tinta=4.6,
              sombra=(col * 0.7, 0, 12, 0.45))
        if a > 0.05:
            brillo(im, x, y, wk * 0.55, PISOS_COL[k], 0.35 * a)
        rotulo(im, f"PISO {k + 1}", x - wk / 2 + 80, y - alto_p / 2 + 30, 26, TINTA * 1.0, t, seed=seed + 10 + k, tinta=False,
               esc=e, alfa=0.8)
        if contenido and e > 0.6 and a > 0.2:
            _contenido(im, k, x, y, wk, t, a, seed + 20 * k)
        if foco == k:
            linea(im, rrect(x, y, wk + 24, alto_p + 8, 18), 7, col=AMARILLO, seed=seed + 90 + k, t=t, cerrado=True, punta=False)
    # techo con antena (es la cabeza de Kuri por dentro)
    if crece >= 1:
        ty = y0 - 4 * alto_p - 10
        forma(im, np.array([(x - (w - 280) / 2 - 30, ty + 10), (x, ty - 70), (x + (w - 280) / 2 + 30, ty + 10)], np.float32),
              rgb("5fb7c0"), 0, seed + 80, tinta=4.6)
        linea(im, [(x, ty - 70), (x, ty - 130)], 6, seed=seed + 81, t=t)
        forma(im, elipse(x, ty - 140, 16, 16), AMARILLO, t, seed + 82, tinta=3)
        brillo(im, x, ty - 140, 50, AMARILLO, 0.4 + 0.3 * math.sin(t * 5))
    return out


def _contenido(im, k, x, y, wk, t, a, seed):
    if k == 0:
        for i in range(14):
            for j in range(2):
                ang = (i * 0.9 + j * 1.7) % math.pi
                col = [rgb("e8a33a"), rgb("4fa3c0"), rgb("d0607a"), rgb("6aa84f")][(i + j) % 4]
                trazo(im, x - wk / 2 + 150 + i * (wk - 200) / 13, y - 26 + 52 * j, 0.55, t, ang, col * (0.6 + 0.4 * a), seed + i * 2 + j)
    elif k == 1:
        for i, n in enumerate(("esquina", "curva", "rayado", "esquina", "curva")):
            PIEZAS[n](im, x - wk / 2 + 170 + i * (wk - 240) / 4, y + 4, 0.55, t, seed=seed + 3 * i)
    elif k == 2:
        for i, n in enumerate(("ojo", "oreja", "nariz", "bigotes")):
            PIEZAS[n](im, x - wk / 2 + 170 + i * (wk - 240) / 3, y + 6, 0.62, t, seed=seed + 5 * i)
    else:
        for i, n in enumerate(("cara", "rueda", "alto")):
            PIEZAS[n](im, x - wk / 2 + 150 + i * (wk - 300) / 2, y + 14, 0.5, t, seed=seed + 20 * i)


# ------------------------------------------------------------ perillas
def perilla(im, x, y, r, t, valor, seed=0, col=None):
    col = col if col is not None else rgb("e8b53e")
    forma(im, elipse(x, y, r, r), col, t, seed, tinta=max(1.6, r / 14), luz=(BLANCO, -r * 0.15, r * 0.2, 0.3))
    a = -math.pi / 2 + valor * 2.2
    linea(im, [(x, y), (x + 0.8 * r * math.cos(a), y + 0.8 * r * math.sin(a))], max(2, r / 9), seed=seed + 1, t=t)


def rejilla_perillas(im, t, x0, y0, cols, filas, paso, r, valores, tinte=None, seed=0):
    """valores(i, j) → −1..1; tinte(i, j) → color o None."""
    for j in range(filas):
        for i in range(cols):
            c = tinte(i, j) if tinte else None
            perilla(im, x0 + i * paso, y0 + j * paso, r, t, valores(i, j), seed=seed + i + cols * j, col=c)


# ------------------------------------------------------------ utilería
def tostadora(im, x, y, s, t, seed=0):
    forma(im, rrect(x, y, 220 * s, 150 * s, 40 * s), rgb("c9cfd6"), t, seed, tinta=5 * s, luz=(BLANCO, -20 * s, 20 * s, 0.45))
    for d in (-1, 1):
        forma(im, rrect(x + d * 45 * s, y - 75 * s, 60 * s, 16 * s, 6 * s), rgb("3a3a40"), t, seed + 1 + (d > 0), tinta=2 * s)
        forma(im, rrect(x + d * 45 * s, y - 92 * s, 52 * s, 34 * s, 10 * s), rgb("e6b06a"), t, seed + 3 + (d > 0), tinta=3 * s)
    forma(im, rrect(x + 122 * s, y + 10 * s, 20 * s, 50 * s, 6 * s), rgb("3a3a40"), t, seed + 5, tinta=2 * s)


def perro(im, x, y, s, t, seed=0, col=None, sx=1.0, lobo=False):
    """Can sentado de perfil (husky o lobo): cuerpo, cabeza, orejas, hocico; sx=-1 mira a la izquierda."""
    col = col if col is not None else rgb("9aa3ad")
    cl = rgb("eef1f4")
    X = lambda dx: x + dx * s * sx                                   # noqa: E731
    forma(im, curva([(X(-60), y + 90 * s), (X(-70), y - 10 * s), (X(-20), y - 60 * s), (X(40), y - 40 * s), (X(60), y + 90 * s)],
                    8, True), col, t, seed, tinta=4.6 * s)
    forma(im, curva([(X(-10), y + 90 * s), (X(0), y - 10 * s), (X(40), y - 30 * s), (X(50), y + 90 * s)], 8, True), cl, t, seed + 1,
          tinta=0, alfa=0.9)
    hx, hy = X(30), y - 90 * s
    forma(im, elipse(hx, hy, 52 * s, 44 * s), col, t, seed + 2, tinta=4.4 * s)
    forma(im, elipse(X(80), hy + 14 * s, 38 * s, 22 * s, 0.1 * sx), cl if not lobo else col * 1.1, t, seed + 3, tinta=4 * s)
    forma(im, elipse(X(114), hy + 8 * s, 9 * s, 7 * s), TINTA, t, seed + 4, tinta=0)
    for d, dx in enumerate((0, 30)):
        forma(im, np.array([(X(dx - 22), hy - 26 * s), (X(dx - 10), hy - 84 * s), (X(dx + 10), hy - 30 * s)], np.float32), col, t,
              seed + 5 + d, tinta=4 * s)
    forma(im, elipse(X(48), hy - 6 * s, 6 * s, 7 * s), rgb("6aa7d8") if not lobo else rgb("e3b13c"), t, seed + 8, tinta=2 * s)
    linea(im, curva([(X(-60), y + 60 * s), (X(-110), y + 20 * s), (X(-120), y - 40 * s)], 6), 16 * s, col=col, seed=seed + 9, t=t)


def panda(im, x, y, s, t, seed=0):
    forma(im, elipse(x, y + 70 * s, 110 * s, 90 * s), BLANCO, t, seed, tinta=5 * s)
    for d in (-1, 1):
        forma(im, elipse(x + d * 70 * s, y - 70 * s, 32 * s, 32 * s), TINTA, t, seed + 1 + (d > 0), tinta=0)
        forma(im, elipse(x + d * 80 * s, y + 90 * s, 34 * s, 50 * s), TINTA, t, seed + 3 + (d > 0), tinta=0)
    forma(im, elipse(x, y - 20 * s, 90 * s, 76 * s), BLANCO, t, seed + 5, tinta=5 * s)
    for d in (-1, 1):
        forma(im, elipse(x + d * 32 * s, y - 24 * s, 20 * s, 26 * s, d * 0.5), TINTA, t, seed + 6 + (d > 0), tinta=0)
        brillo(im, x + d * 32 * s + 4 * s, y - 28 * s, 5 * s, BLANCO, 1.3)
    forma(im, elipse(x, y + 6 * s, 14 * s, 10 * s), TINTA, t, seed + 8, tinta=0)


def gpu(im, x, y, s, t, seed=0):
    """Tarjeta gráfica de videojuegos: placa verde con dos ventiladores que giran."""
    forma(im, rrect(x, y, 420 * s, 170 * s, 16 * s), rgb("3a3f48"), t, seed, tinta=5 * s, luz=(BLANCO, -20 * s, 20 * s, 0.2))
    forma(im, rrect(x, y + 98 * s, 300 * s, 26 * s, 4 * s), rgb("d9b04a"), t, seed + 1, tinta=3 * s)
    for d in (-1, 1):
        cx = x + d * 100 * s
        forma(im, elipse(cx, y, 66 * s, 66 * s), rgb("23272e"), t, seed + 2 + (d > 0), tinta=3 * s)
        for k in range(5):
            a = k / 5 * 2 * math.pi + t * 9 * d
            linea(im, curva([(cx, y), (cx + 30 * s * math.cos(a + 0.4), y + 30 * s * math.sin(a + 0.4)),
                             (cx + 58 * s * math.cos(a), y + 58 * s * math.sin(a))], 5), 9 * s, col=rgb("7a8290"), seed=seed + 5 + k,
                  t=t, punta=True)
    linea(im, [(x - 190 * s, y - 70 * s), (x + 190 * s, y - 70 * s)], 6 * s, col=rgb("6ccf6a"), seed=seed + 12, t=t, punta=False)


def trofeo(im, x, y, s, t, seed=0):
    brillo(im, x, y - 40 * s, 160 * s, AMARILLO, 0.35)
    forma(im, curva([(x - 80 * s, y - 120 * s), (x + 80 * s, y - 120 * s), (x + 60 * s, y - 20 * s), (x, y + 20 * s), (x - 60 * s, y - 20 * s)],
                    8, True), rgb("e9b949"), t, seed, tinta=5 * s, luz=(BLANCO, -20 * s, 20 * s, 0.45))
    for d in (-1, 1):
        linea(im, curva([(x + d * 76 * s, y - 100 * s), (x + d * 120 * s, y - 80 * s), (x + d * 66 * s, y - 40 * s)], 6), 9 * s,
              col=rgb("c4922a"), seed=seed + 1 + (d > 0), t=t)
    forma(im, rrect(x, y + 50 * s, 30 * s, 60 * s, 6 * s), rgb("e9b949"), t, seed + 3, tinta=4 * s)
    forma(im, rrect(x, y + 100 * s, 130 * s, 40 * s, 8 * s), rgb("8a5a34"), t, seed + 4, tinta=4 * s)


def personita(im, x, y, s, t, seed=0, col=None, piel=None):
    """Persona chibi diminuta (para multitudes): cabeza, cuerpo de color, se mece."""
    r = np.random.default_rng(seed)
    col = col if col is not None else rgb(["e35d4a", "3f78c8", "6aa84f", "e8b53e", "9b6ad1", "4fb3b0"][seed % 6])
    piel = piel if piel is not None else rgb(["f2c9a4", "d9a77c", "a8754c", "f5d8be", "7a5236"][seed % 5])
    dy = 3 * s * math.sin(t * 5 + seed)
    forma(im, rrect(x, y + 34 * s + dy, 44 * s, 52 * s, 16 * s), col, t, seed, tinta=2.6 * s)
    forma(im, elipse(x, y + dy, 24 * s, 24 * s), piel, t, seed + 1, tinta=2.6 * s)
    forma(im, elipse(x, y - 14 * s + dy, 24 * s, 12 * s), rgb(["3a2a20", "1e1e22", "8a5a2a", "c9a25a"][seed % 4]), t, seed + 2, tinta=0)


def estrella(im, x, y, r, t, col, f=1.0, seed=0):
    brillo(im, x, y, r * 3, col, 0.45 * f)
    forma(im, elipse(x, y, r, r), col, t, seed, tinta=1.6)


def marca_x(im, x, y, s, t, seed=0, col=None):
    col = col if col is not None else rgb("e35d4a")
    linea(im, [(x - 60 * s, y - 60 * s), (x + 60 * s, y + 60 * s)], 18 * s, col=col, seed=seed, t=t)
    linea(im, [(x + 60 * s, y - 60 * s), (x - 60 * s, y + 60 * s)], 18 * s, col=col, seed=seed + 1, t=t)


def palomita(im, x, y, s, t, seed=0, col=None):
    col = col if col is not None else rgb("2e8b4a")
    linea(im, [(x - 60 * s, y), (x - 15 * s, y + 50 * s), (x + 70 * s, y - 60 * s)], 18 * s, col=col, seed=seed, t=t)


def volcan(im, x, y, s, t, seed=0):
    forma(im, np.array([(x - 160 * s, y + 90 * s), (x - 40 * s, y - 80 * s), (x + 40 * s, y - 80 * s), (x + 160 * s, y + 90 * s)],
                       np.float32), rgb("7a5a48"), t, seed, tinta=4 * s, sombra=(rgb("4a3428"), 20 * s, 0, 0.5))
    forma(im, curva([(x - 40 * s, y - 80 * s), (x - 20 * s, y - 40 * s), (x + 10 * s, y - 60 * s), (x + 40 * s, y - 80 * s)], 6),
          rgb("e8693a"), t, seed + 1, tinta=0)
    for k in range(3):
        forma(im, elipse(x + (k - 1) * 30 * s + 10 * s * math.sin(t + k), y - 120 * s - 40 * k * s, (40 + 12 * k) * s, (28 + 8 * k) * s),
              rgb("b9b4ae"), t, seed + 2 + k, tinta=2.4 * s, alfa=0.85)


def bici(im, x, y, s, t, seed=0):
    for d in (-1, 1):
        rueda(im, x + d * 90 * s, y + 30 * s, 0.75 * s, t, seed=seed + 10 * (d > 0))
    linea(im, [(x - 90 * s, y + 30 * s), (x - 20 * s, y - 40 * s), (x + 50 * s, y - 40 * s), (x + 90 * s, y + 30 * s)], 9 * s,
          col=rgb("d8433a"), seed=seed + 30, t=t, punta=False)
    linea(im, [(x - 20 * s, y - 40 * s), (x, y + 30 * s), (x + 50 * s, y - 40 * s)], 9 * s, col=rgb("d8433a"), seed=seed + 31, t=t,
          punta=False)


_FONDOS = {"perro": ("bfe0a8", "8cc06f"), "tostadora": ("f6e3c9", "d9b48a"), "volcan": ("bcd8ee", "c9b79a"),
           "bici": ("d6e6f2", "b9c3cc"), "panda": ("cfe8b8", "86b86a"), "husky": ("cfe8b8", "8cc06f"), "lobo": ("dfe9e2", "f4f8fb"),
           "husky_nieve": ("dfe9e2", "f4f8fb")}


def foto_cosa(nombre, t=0.0, w=360, h=270):
    """Foto pintada (recorte w×h) de una cosa: perro, tostadora, volcan, bici, panda, husky, lobo."""
    from personajes_ia import lienzo

    def pintar(im, x0, y0, w_, h_, tt):
        a, b = _FONDOS[nombre]
        u = np.linspace(0, 1, h_, dtype=np.float32)[:, None, None]
        im[y0:y0 + h_, x0:x0 + w_] = rgb(a) * (1 - u) + rgb(b) * u
        cx, cy = x0 + w_ / 2, y0 + h_ / 2
        if nombre in ("husky_nieve", "lobo"):                            # nieve
            forma(im, rrect(cx, y0 + h_ * 0.85, w_ * 1.1, h_ * 0.4, 30), BLANCO, tt, 77, tinta=0)
        {"perro": lambda: perro(im, cx - 20, cy + 20, 0.9, tt, seed=71, col=rgb("c98a4a")),
         "husky": lambda: perro(im, cx - 20, cy + 20, 0.9, tt, seed=72, col=rgb("8f98a3")),
         "husky_nieve": lambda: perro(im, cx - 20, cy + 20, 0.9, tt, seed=72, col=rgb("8f98a3")),
         "lobo": lambda: perro(im, cx - 20, cy + 20, 0.9, tt, seed=73, col=rgb("7d7468"), lobo=True),
         "tostadora": lambda: tostadora(im, cx, cy + 20, 0.9, tt, seed=74),
         "volcan": lambda: volcan(im, cx, cy + 30, 0.9, tt, seed=75),
         "bici": lambda: bici(im, cx, cy, 0.95, tt, seed=76),
         "panda": lambda: panda(im, cx, cy, 0.8, tt, seed=78)}[nombre]()
    return lienzo(("cosa", nombre, w, h), w, h, pintar, t)
