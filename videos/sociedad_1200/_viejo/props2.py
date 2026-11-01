# -*- coding: utf-8 -*-
"""Utilería noir 2: árbol de tinta que crece (red neuronal), pared de perillas, ajedrez que juega solo, túnel de números,
predicción de la siguiente palabra. Funciones puras de t (cualquier cuadro se dibuja suelto)."""
import functools
import math

import numpy as np

import noir as N
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from props import rect, rot
from toon import blob, elipse_, suave, tubo


# ---------------------------------------------------------------------- árbol de tinta / red que crece
@functools.lru_cache(maxsize=4)
def _ramas(sem=0, prof=7):
    """Ramas del árbol: lista de (a, b, nivel, t_ini relativo 0..1, grosor). Crece de abajo arriba, se abre en abanico."""
    r = np.random.default_rng(sem)
    out = []

    def crece(p, ang, largo, nivel, t0):
        if nivel > prof:
            return
        q = p + largo * np.array([math.cos(ang), math.sin(ang)])
        dur = 0.13
        out.append((p, q, nivel, t0, max(1.2, 16 * 0.68 ** nivel)))
        n = 2 if nivel < 2 else int(r.integers(2, 4))
        for k in range(n):
            da = (k - (n - 1) / 2) * r.uniform(0.35, 0.65) + r.normal(0, 0.12)
            crece(q, ang + da, largo * r.uniform(0.68, 0.86), nivel + 1, t0 + dur)
    crece(np.array([0.0, 0.0]), -math.pi / 2, 210, 0, 0.0)
    return out


def arbol_tinta(h, x, y, esc, u, sem=0, nodos=True, prof=7):
    """Dibuja el árbol en (x, y) (base) con progreso u (0..1+). Las puntas se encienden como neuronas al llegar."""
    for a, b, nivel, t0, g in _ramas(sem, prof):
        k = clamp01((u - t0) / 0.13)
        if k <= 0:
            continue
        P = np.array([a, a + (b - a) * k]) * esc + (x, y)
        h.trazo(P, g * esc, int(nivel * 31 + t0 * 1000) % 997, color=gris(12), taper=(0.0, 0.9 if k < 1 else 0.3), jit=0.6)
        if nodos and k >= 1 and nivel >= 3:
            v = 0.5 + 0.5 * math.sin(u * 9 + nivel * 3 + b[0] * 0.05)
            q = b * esc + (x, y)
            h.emitir(elipse_(q[0], q[1], 3.2 * esc, 3.2 * esc, n=8), 0.5 + 0.7 * v)


# ---------------------------------------------------------------------- pared de perillas (miles de millones de ajustes)
def perillas(h, t, t0, cols=26, filas=13, x0=80, y0=80, paso=68, sem=0):
    """Cuadrícula de perillas de baquelita; cada una gira un poquito (ajustes diminutos), cada vez más deprisa."""
    v = clamp01((t - t0) / 3.0)
    for i in range(cols):
        for j in range(filas):
            cx, cy = x0 + i * paso, y0 + j * paso
            r = 24
            ph = (i * 7.3 + j * 13.1) % 6.28
            ang = ph + math.sin(t * (1.5 + 6 * v) + ph * 3) * (0.4 + 1.2 * v)
            h.pieza(elipse_(cx, cy, r, r, n=20), 40 + (i * j) % 3 * 10, sem + i * 50 + j, w=3, luz=(0.3, -1), d=4, trama=0,
                    rim=0.8, jit=0.4)
            h.trazo(np.array([[cx, cy], [cx + math.cos(ang) * r * 0.9, cy + math.sin(ang) * r * 0.9]]), 4, sem + 3000 + i * 50 + j,
                    color=gris(235), jit=0.2, taper=(0.1, 0.1))


# ---------------------------------------------------------------------- ajedrez que juega solo
def _tablero(cx, cy, ancho, prof, inclina=0.55):
    """Función que lleva (i, j) de casillas (0..8) a pantalla en perspectiva simple."""
    def f(i, j):
        z = 1 + inclina * (1 - j / 8)                       # filas del fondo más pequeñas
        y = cy - prof * (1 - j / 8) ** 0.9
        x = cx + (i - 4) * (ancho / 8) / z
        return np.array([x, y])
    return f


def ajedrez(h, t, movs, cx=W / 2, cy=930, ancho=1300, prof=520, sem=0):
    """Tablero con piezas. movs = lista de (t_mov, pieza, (i0, j0), (i1, j1)). Las piezas se desplazan solas (con salto)."""
    f = _tablero(cx, cy, ancho, prof)
    for i in range(8):
        for j in range(8):
            P = np.array([f(i, j), f(i + 1, j), f(i + 1, j + 1), f(i, j + 1)])
            h.pieza(P, 190 if (i + j) % 2 else 40, sem + i * 9 + j, w=1.5, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, jit=0.2)
    h.pieza(np.array([f(0, 0), f(8, 0), f(8, 0) + (0, 40), f(0, 0) + (0, 40)]), 30, sem + 99, w=3, luz=(0, -1), d=2, trama=0.3)
    fijas = [("peon", (1, 1)), ("peon", (2, 1)), ("peon", (5, 1)), ("rey", (4, 0)), ("torre", (0, 0)), ("peon", (3, 6)),
             ("peon", (6, 6)), ("rey", (4, 7)), ("alfil", (2, 7)), ("torre", (7, 7))]
    piezas = []
    for tipo, c in fijas:
        piezas.append([tipo, np.array(c, float), 0.0])
    for tm, tipo, a, b in movs:
        u = clamp01((t - tm) / 0.7)
        e = e_inout(u)
        c = np.array(a, float) + (np.array(b, float) - np.array(a, float)) * e
        piezas.append([tipo, c, math.sin(math.pi * u) * (60 if tipo == "caballo" else 20)])
    piezas.sort(key=lambda p: -p[1][1])
    for tipo, c, salto in piezas:
        base = f(c[0] + 0.5, c[1] + 0.5)
        esc = 1 / (1 + 0.55 * (1 - c[1] / 8))
        _pieza_ajedrez(h, base[0], base[1] - salto, esc * 1.35, tipo, sem + int(c[0] * 10 + c[1]), blanca=c[1] < 4)


def _pieza_ajedrez(h, x, y, s, tipo, sem, blanca=True):
    tono = 215 if blanca else 30
    h.pieza(elipse_(x, y, 40 * s, 12 * s, n=20), tono - 20, sem, w=3 * s, luz=(0.3, -1), d=4, trama=0, rim=0.6)
    if tipo == "peon":
        P = [(-30, 0), (30, 0), (18, -20), (12, -60), (22, -70), (20, -96), (0, -106), (-20, -96), (-22, -70), (-12, -60), (-18, -20)]
    elif tipo == "rey":
        P = [(-34, 0), (34, 0), (20, -30), (14, -120), (26, -132), (12, -146), (6, -146), (6, -160), (14, -160), (14, -170), (6, -170),
             (6, -180), (-6, -180), (-6, -170), (-14, -170), (-14, -160), (-6, -160), (-6, -146), (-12, -146), (-26, -132), (-14, -120),
             (-20, -30)]
    elif tipo == "torre":
        P = [(-32, 0), (32, 0), (22, -24), (20, -100), (28, -104), (28, -130), (14, -130), (14, -118), (6, -118), (6, -130), (-6, -130),
             (-6, -118), (-14, -118), (-14, -130), (-28, -130), (-28, -104), (-20, -100), (-22, -24)]
    elif tipo == "alfil":
        P = [(-30, 0), (30, 0), (18, -24), (12, -80), (24, -110), (8, -138), (0, -146), (-8, -138), (-24, -110), (-12, -80), (-18, -24)]
    else:                                                   # caballo
        P = [(-30, 0), (30, 0), (20, -24), (22, -70), (30, -110), (8, -150), (-20, -138), (-36, -110), (-30, -98), (-8, -104), (-18, -60),
             (-20, -24)]
    P = np.array(P, float) * s + (x, y)
    h.pieza(P, tono, sem + 1, w=3.5 * s, luz=(0.3, -1), d=10 * s, trama=0.4 if not blanca else 0.2, rim=0.9)


# ---------------------------------------------------------------------- túnel de números (lo que hay dentro)
def tunel_numeros(h, t, cx, cy, k=1.0, sem=0, vel=1.0):
    """Marcos que se alejan sin fin, tapizados de cifras: la caja negra por dentro."""
    for n in range(14):
        z = ((n + t * 0.35 * vel) % 14) / 14
        esc = 0.04 + 1.6 * (1 - z) ** 2.4
        ww, hh = 900 * esc, 560 * esc
        alfa = clamp01((1 - z) * 1.6) * clamp01(z * 6) * k
        if alfa < 0.03 or esc < 0.05:
            continue
        h.anillo(h.tf(rect(cx - ww / 2, cy - hh / 2, ww, hh)), 2.0 + 4 * esc, sem + n, color=(170, 170, 170), alfa=alfa, jit=0.8)
        if esc > 0.15:
            r = np.random.default_rng(int((n + math.floor(t * 0.35 * vel / 1.0)) * 37) % 10000)
            for j in range(10):
                fila = "".join(str(x) for x in r.integers(0, 10, 16))
                N.texto_maquina(h, fila, cx - ww / 2 + 14 * esc, cy - hh / 2 + 20 * esc + j * hh / 10.5, max(6, 34 * esc), t, -99,
                                cps=1e9, tono=0.8, alfa=0.6 * alfa, fuente=N.FUENTE_MAQ_R)
