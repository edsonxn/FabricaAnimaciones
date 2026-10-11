# -*- coding: utf-8 -*-
"""Elementos de pantalla (espacio de pantalla 1080x1920): placa del año con odómetro, contadores, tarjetas de papel."""
import math

import numpy as np

import vox as V
from motor import W, H, clamp01, e_back, e_out, e_inout, prog, smooth, rect_red, ancho_texto, lerp

DIG_PX = 138
CELDA_H = DIG_PX * 1.02


def placa(lz, cx, cy, w, h, alfa=1.0, rot=0.0, color=V.CREMA, capa=2):
    with lz.capa(capa):
        with lz.grupo(cx, cy, 1.0, rot):
            lz.relleno(rect_red(-w / 2 + 4, -h / 2 + 8, w, h, 22), (24, 16, 12), alfa=0.30 * alfa, temblor=0.0)
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, 22), color, alfa=alfa, temblor=0.0)


def odometro(lz, valor, cx=W / 2, cy=210, alfa=1.0, rot=-0.012, color=V.TINTA, sufijo=None):
    """Placa con el año; los dígitos ruedan como un odómetro (valor real)."""
    if alfa <= 0.01:
        return
    ndig = 4
    cw = ancho_texto("0", "vox_x", DIG_PX) * 1.02
    w = ndig * cw + 90
    h = 200
    placa(lz, cx, cy, w, h, alfa, rot)
    v = float(valor)
    with lz.capa(2):
        with lz.grupo(cx, cy, 1.0, rot):
            for k in range(ndig):
                p = 10 ** (ndig - 1 - k)
                x = v / p
                d = int(math.floor(x)) % 10
                if p == 1:
                    roll = e_inout(x - math.floor(x))
                else:      # un dígito superior solo rueda cuando el acarreo de los inferiores está en marcha
                    roll = max(0.0, (v % p) - (p - 1))
                xx = (k - (ndig - 1) / 2) * cw
                celda = np.array([[xx - cw / 2, -h / 2 + 10], [xx + cw / 2, -h / 2 + 10], [xx + cw / 2, h / 2 - 10],
                                  [xx - cw / 2, h / 2 - 10]])
                with lz.recorte(celda):
                    lz.texto(str(d), xx, DIG_PX * 0.05 - roll * CELDA_H * 0.9, DIG_PX, "vox_x", color=color, borde=None,
                             alfa=alfa * (1 - roll), temblor=0.0)
                    if roll > 0.001:
                        lz.texto(str((d + 1) % 10), xx, DIG_PX * 0.05 + (1 - roll) * CELDA_H * 0.9, DIG_PX, "vox_x",
                                 color=color, borde=None, alfa=alfa * roll, temblor=0.0)
            lz.relleno(np.array([[-w / 2 + 20, h / 2 - 9], [w / 2 - 20, h / 2 - 9], [w / 2 - 20, h / 2 - 5], [-w / 2 + 20, h / 2 - 5]]),
                       V.ROJO, alfa=alfa, temblor=0.0)


def placa_texto(lz, texto, cx=W / 2, cy=210, px=120, alfa=1.0, rot=-0.012, color=V.TINTA):
    if alfa <= 0.01:
        return
    w = ancho_texto(texto, "vox_x", px) + 90
    placa(lz, cx, cy, w, 200, alfa, rot)
    with lz.capa(2):
        lz.texto(texto, cx, cy + px * 0.05, px, "vox_x", color=color, borde=None, alfa=alfa, temblor=0.0, rot=rot)


def contador(lz, valor, texto, cx, cy, px=170, alfa=1.0, color=V.AMARILLO, sufijo="", fuente="vox_x", color2=V.CREMA):
    """Número grande con sombra y rótulo debajo (p. ej. 300 · PERSONAS)."""
    if alfa <= 0.01:
        return
    s = f"{int(round(valor))}{sufijo}"
    V.rotulo(lz, s, cx, cy, px, color=color, fuente=fuente, alfa=alfa, sombra=0.5)
    V.rotulo(lz, texto, cx, cy + px * 0.72, px * 0.27, color=color2, fuente="vox_b", alfa=alfa, sombra=0.0)


def frase_grande(lz, lineas, cx, cy, px=88, k=1.0, alfa=1.0, color=V.CREMA, interlinea=1.08, marcador=None, rot=0.0,
                 fuente="vox_x"):
    """Rotulación cinética de varias líneas centradas; marcador = índice de línea con barrido amarillo."""
    if k <= 0.01 or alfa <= 0.01:
        return
    for i, ln in enumerate(lineas):
        y = cy + (i - (len(lineas) - 1) / 2) * px * interlinea
        w = ancho_texto(ln, fuente, px)
        if marcador is not None and i == marcador:
            V.marcador(lz, cx - w / 2 - 10, y + px * 0.08, w + 20, px * 0.86, prog_marca(k), V.AMARILLO, seed=i)
            V.rotulo(lz, ln, cx, y, px * k, color=V.TINTA, fuente=fuente, alfa=alfa, sombra=0.0, rot=rot)
        else:
            V.rotulo(lz, ln, cx, y, px * k, color=color, fuente=fuente, alfa=alfa, rot=rot)


def prog_marca(k):
    return clamp01((k - 0.4) / 0.6)


def tarjeta(lz, cx, cy, w, h, alfa=1.0, rot=0.0, color=V.CREMA, capa=2, sombra=True):
    """Tarjeta de papel con sombra (contenedor de datos)."""
    with lz.capa(capa):
        with lz.grupo(cx, cy, 1.0, rot):
            if sombra:
                lz.relleno(rect_red(-w / 2 + 5, -h / 2 + 9, w, h, 18), (24, 16, 12), alfa=0.30 * alfa, temblor=0.0)
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, 18), color, alfa=alfa, temblor=0.0)


def fila_puntos(lz, n, cols, x0, y0, dx, dy, r, color, prog_n, alfa=1.0, seed=0, capa=2):
    """Matriz de puntos (cada punto = una persona): aparecen de a poco hasta prog_n (0..n)."""
    pts = []
    for i in range(int(min(n, prog_n))):
        pts.append((x0 + (i % cols) * dx, y0 + (i // cols) * dy))
    if pts:
        lz.puntos(pts, r, color, capa=capa)
