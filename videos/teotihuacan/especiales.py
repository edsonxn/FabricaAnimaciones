# -*- coding: utf-8 -*-
"""Planos en coordenadas de pantalla: el conjunto habitacional en corte, el mito del Quinto Sol y el portal
circular que une un plano con otro sin cortes."""
import math
from contextlib import contextmanager

import numpy as np

from motor import (W, H, prog, lerp, smooth, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, h01)
import plano as P
import mundo as M


# ======================================================================== portal circular
@contextmanager
def portal(lz, cx, cy, r, s=1.0):
    """Lo que se dibuje dentro aparece recortado a un círculo (r) con anillo blanco; s = zoom interior."""
    lz.relleno(circulo(cx, cy, r + 9, 90), (255, 255, 255), alfa=0.9)
    with lz.recorte(circulo(cx, cy, r, 90)):
        with lz.grupo(cx, cy, s):
            with lz.grupo(-cx, -cy, 1.0):
                yield


def rect_pant():
    return np.array([[-10, -10], [W + 10, -10], [W + 10, H + 10], [-10, H + 10]], float)


# ======================================================================== conjunto habitacional en corte
def _mural(lz, x0, x1, y, alto, t, tono=0):
    lz.relleno(np.array([[x0, y], [x1, y], [x1, y + alto], [x0, y + alto]], float), (206, 70, 78))
    n = int((x1 - x0) / 52)
    for i in range(n):
        cx = x0 + 26 + i * 52
        lz.relleno(np.array([[cx, y + 8], [cx + 20, y + alto / 2], [cx, y + alto - 8], [cx - 20, y + alto / 2]]),
                   (255, 214, 110) if (i + tono) % 2 else (66, 170, 190))
        lz.relleno(circulo(cx, y + alto / 2, 5, 10), (206, 70, 78))


def _jaguar(lz, x, y, s, t):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-64, -34, 100, 44, 20, 8), (255, 190, 70))
        lz.relleno(circulo(48, -30, 26, 24), (255, 190, 70))
        lz.relleno(circulo(38, -52, 8, 10), (255, 190, 70))
        lz.relleno(circulo(58, -50, 8, 10), (255, 190, 70))
        lz.relleno(circulo(56, -34, 3, 8), (44, 30, 56))
        for k in range(6):
            lz.relleno(circulo(-50 + k * 16, -20 + 10 * math.sin(k * 2.1), 5, 10), (44, 30, 56))
        pata = math.sin(t * 5) * 8
        for dx in (-56, -30, 10, 26):
            lz.relleno(rect_red(dx, 6, 12, 26 + (pata if dx in (-30, 26) else -pata) * 0.3, 5, 6), (240, 170, 60))
        lz.relleno(np.array([[-64, -20], [-96, -40 + 10 * math.sin(t * 4)], [-92, -30], [-62, -8]]), (255, 190, 70))


def casa_corte(lz, t, est):
    """Corte de un conjunto de viviendas: cocina, patio central y taller de obsidiana. est: casa (aparición 0..1)."""
    a = est.get("casa", 1.0)
    M.degradado_v(lz, -10, W + 10, -10, H + 10, (62, 34, 78), (110, 58, 96), 0, H, paso=14.0)
    y_suelo = 840
    # paredes y techos
    for (x0, x1, col) in ((200, 730, (252, 214, 168)), (1190, 1720, (252, 214, 168))):
        lz.relleno(np.array([[x0, 250], [x1, 250], [x1, y_suelo], [x0, y_suelo]], float), col)
        lz.relleno(np.array([[x0, y_suelo - 60], [x1, y_suelo - 60], [x1, y_suelo], [x0, y_suelo]], float), (214, 150, 118))
    lz.relleno(np.array([[730, 250], [1190, 250], [1190, y_suelo], [730, y_suelo]], float), (250, 226, 190))
    # cielo por el patio
    lz.degradado(np.array([[760, 250], [1160, 250], [1160, 520], [760, 520]], float), (78, 160, 236), (255, 226, 184),
                 (0, 250), (0, 520))
    lz.relleno(circulo(1040, 340, 34, 24), (255, 244, 190))
    lz.halo(1040, 340, 120, (255, 226, 150), alfa=0.4)
    lz.relleno(np.array([[730, 520], [1190, 520], [1190, y_suelo], [730, y_suelo]], float), (246, 214, 176))
    # techos con banda roja
    for (x0, x1) in ((180, 750), (1170, 1740)):
        lz.relleno(np.array([[x0, 200], [x1, 200], [x1, 250], [x0, 250]], float), (214, 72, 78))
        lz.relleno(np.array([[x0, 250], [x1, 250], [x1, 262], [x0, 262]], float), (150, 44, 84))
    # murales
    _mural(lz, 226, 704, 300, 76, t, 0)
    _mural(lz, 1216, 1694, 300, 76, t, 1)
    _jaguar(lz, 470, 470, 1.0, t)
    # piso
    lz.relleno(np.array([[160, y_suelo], [1760, y_suelo], [1760, y_suelo + 40], [160, y_suelo + 40]], float), (150, 86, 100))
    # cocina: comal, fuego y tortillas
    lz.relleno(rect_red(300, 770, 150, 70, 10, 6), (150, 96, 100))
    lz.relleno(elipse(375, 764, 78, 16, 0, 24), (60, 50, 74))
    M.llama(lz, 375, 800, 0.5, t, seed=3)
    for k in range(3):
        lz.relleno(circulo(340 + k * 34, 754, 15, 16), (250, 210, 120))
    M.humo(lz, 375, 700, t, 0.0, n=4, s=0.6, alfa=0.35, seed=1, col=(210, 190, 200))
    p = e_back(prog(a, 0.1, 0.5))
    M.persona(lz, 520, y_suelo, 1.9 * p, t, ropa=1, piel=1, sentado=True, lado=-1, seed=1)
    M.persona(lz, 640, y_suelo, 1.4 * p, t + 0.4, ropa=3, piel=0, paso=0.0, lado=-1, seed=2)
    # patio: altar y una vasija
    lz.relleno(np.array([[900, y_suelo], [1020, y_suelo], [1000, y_suelo - 60], [920, y_suelo - 60]], float), (226, 150, 110))
    lz.relleno(rect_red(910, y_suelo - 78, 100, 20, 4, 4), (214, 72, 78))
    M.persona(lz, 1100, y_suelo, 1.7 * p, t, ropa=4, piel=2, paso=0.0, lado=-1, carga="vasija", seed=3)
    # taller de obsidiana
    for k in range(9):
        px = 1310 + h01(3, k) * 90
        py = y_suelo - 10 - h01(4, k) * 26
        lz.relleno(np.array([[px, py], [px + 14, py - 22 - 8 * h01(5, k)], [px + 24, py - 4]]), (40, 34, 62))
        lz.relleno(np.array([[px + 8, py - 8], [px + 14, py - 22 - 8 * h01(5, k)], [px + 19, py - 10]]), (120, 110, 176))
    for k in range(4):
        tt = (t * 1.4 + k * 0.6) % 2.4
        lz.puntos(np.array([[1496 + 30 * k - 40, 736 - tt * 18]]), 3.2 * (1 - tt / 2.4), (200, 190, 255))
    M.persona(lz, 1500, y_suelo, 1.9 * p, t, ropa=0, piel=3, sentado=True, lado=1, seed=5)
    M.persona(lz, 1640, y_suelo, 1.6 * p, t, ropa=4, piel=1, paso=0.0, lado=-1, tocado="plumas", seed=6)
    # marco de la casa (aro de sombra)
    lz.halo(960, 560, 1200, (20, 8, 40), alfa=0.25, r0=0.6)


# ======================================================================== mito del Quinto Sol
def _piramide_sil(lz, x, w, h, n, col, luz):
    for i in range(n):
        wb = w * (1 - 0.66 * i / n)
        yb = 800 - i * h / n
        yt = 800 - (i + 1) * h / n
        lz.relleno(np.array([[x - wb / 2, yb], [x + wb / 2, yb], [x + wb * 0.43, yt], [x - wb * 0.43, yt]]), col)
        lz.relleno(np.array([[x - wb / 2, yb], [x - wb / 2 + 12, yb], [x - wb * 0.43 + 12, yt], [x - wb * 0.43, yt]]),
                   luz, alfa=0.35)


def mito(lz, t, est):
    """Plano del mito: noche, hoguera, dos dioses. est: alba, llama (0..1.8), duda (0..4), salto (0..1), sol (0..1)."""
    alba = est.get("alba", 0.0)
    top = P.mezcla((8, 10, 34), (52, 60, 150), alba)
    bot = P.mezcla((52, 34, 96), (255, 152, 112), alba)
    M.degradado_v(lz, -10, W + 10, -10, H + 10, top, bot, 0, 820, paso=12.0)
    M.estrellas(lz, 1.0 - alba, t, semilla=9)
    fl = est.get("llama", 0.3)
    col_sil = P.mezcla((34, 20, 66), (120, 84, 130), alba * 0.6)
    _piramide_sil(lz, 380, 760, 380, 5, col_sil, (255, 160, 90))
    _piramide_sil(lz, 1580, 520, 300, 4, col_sil, (255, 160, 90))
    # sol que nace de la hoguera
    su = est.get("sol", 0.0)
    if su > 0.001:
        y = lerp(760, 300, e_out(su))
        r = lerp(30, 150, e_out(su))
        P.sol(lz, 960, y, r, t, brillo=1.0)
    # plaza
    M.degradado_v(lz, -10, W + 10, 800, H + 10, P.mezcla((84, 52, 92), (196, 130, 100), alba), (46, 26, 66), 800, H,
                  paso=12.0)
    lz.halo(960, 800, 900, (255, 150, 60), alfa=min(0.8, 0.25 * fl))
    # hoguera
    lz.relleno(elipse(960, 812, 170, 34, 0, 36), (136, 90, 110))
    lz.relleno(elipse(960, 806, 146, 26, 0, 36), (34, 16, 40))
    for dx in (-60, 0, 60):
        M.llama(lz, 960 + dx, 810, 1.2 * fl * (1.0 if dx == 0 else 0.8), t, seed=dx)
    # dios rico: avanza y duda cuatro veces
    d = est.get("duda", 0.0)
    if d < 4.0:
        k = int(d)
        f = d - k
        xr = 560 + (150 + 30 * k) * math.sin(math.pi * f) ** 0.8
    else:
        xr = 560
    M.persona(lz, xr, 830, 2.3, t, ropa=3, piel=1, paso=0.0, lado=1, tocado="plumas", seed=1)
    lz.halo(xr, 640, 150, (255, 214, 96), alfa=0.35)
    # dios humilde: corre y salta a la hoguera
    s = est.get("salto", 0.0)
    if s < 0.93:
        xh = lerp(1480, 960, e_inout(s))
        yh = 830 - 300 * math.sin(math.pi * min(1.0, s / 0.93)) ** 1.1 * (1.0 if s > 0.15 else 0.0)
        M.persona(lz, xh, yh, 1.75, t, ropa=0, piel=2, paso=1.0 if s < 0.15 else 0.0, lado=-1, brazos=0.9 if s > 0.15 else 0.0, seed=2)
        for k in range(7):     # llagas
            lz.relleno(circulo(xh + (h01(8, k) - 0.5) * 30, yh - 80 * 1.75 + h01(9, k) * 60, 3, 8), (176, 70, 82))
    else:
        lz.halo(960, 700, 500 * (1 - prog(s, 0.93, 1.0)) + 260, (255, 240, 190), alfa=0.9 * (1 - prog(s, 0.93, 1.0)) + 0.1)
