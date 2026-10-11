# -*- coding: utf-8 -*-
"""Mundos pintados de la prueba NOIR FEUDAL (gris con noir_fondos + primitivas de nucleo/noir_feudal.py; el color lo pone
noir_color.pegar con la rampa del material). Una vez por proceso (lru_cache).

    cielo · castillo · villa (casas al fondo) · frente (casas de la calle) · suelo   -> plano A, la villa amurallada de noche
    exterior · camara · ventanal                                                    -> plano B, la cámara de la torre
    mesa                                                                            -> plano C, la mesa del pesquisidor
"""
import functools
import math

import cv2
import numpy as np

import noir_feudal as NF
from noir import fbm
from noir_fondos import Lienzo

Y_CALLE = 880
ANTORCHA_A = (1300, 560)             # antorcha de la calle (base de la llama)
ESTANDARTE_A = (1360, 250)           # asta del estandarte (esquina sup-izq de la tela)


# ====================================================================== plano A
@functools.lru_cache(maxsize=1)
def cielo():
    L = Lienzo(3000, 2400, origen=(-540, -1500), base=0.08, sem=11)
    L.rect(-540, -1500, 3000, 2400, 0.05, tex=0.05, grad=(0.32, -1500, 760))
    rng = np.random.default_rng(13)
    L.elipse(1240, 150, 70, 70, 0.97, tex=0.0, emis=0.7)                       # luna llena junto al castillo
    L.brillo(1240, 150, 340, 0.4, tono=0.85)
    for k in range(40):
        cx, cy = rng.uniform(-500, 2400), rng.uniform(-1400, 400)
        rx, ry = rng.uniform(160, 520), rng.uniform(24, 64)
        cerca = abs(cx - 1240) < 520 and abs(cy - 150) < 400
        L.elipse(cx, cy, rx, ry, rng.uniform(0.12, 0.28), alfa=0.55, rug=1.4, blur=10, tex=0.15)
        L.elipse(cx + rx * 0.2, cy - ry * 0.4, rx * 0.6, ry * 0.45, 0.34 + 0.18 * cerca, alfa=0.35, rug=1.0, blur=6)
    for k in range(9):                                                         # bandada de cuervos lejanos (fijos, diminutos)
        x, y = 900 + k * 38 + rng.uniform(-10, 10), -760 + rng.uniform(-30, 30)
        L.linea([(x - 8, y - 3), (x, y + 2), (x + 8, y - 3)], 1.6, 0.03, jit=0)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def castillo():
    """El castillo sobre la colina: lienzo de muralla, torre del homenaje almenada y torres de techo cónico."""
    L = Lienzo(4200, 2000, origen=(-1000, -1300), sem=21)
    L.poli([(-1000, 700), (-600, 520), (-100, 430), (300, 330), (900, 300), (1500, 340), (2000, 450), (2600, 560), (3200, 700),
            (3200, 700), (-1000, 700)], 0.10, tex=0.15, grad=(0.06, 300, 700))
    NF.muralla(L, 150, 1550, 360, 210, tono=0.24, sem=22, encendidas=0.5)
    NF.torre(L, 170, 380, 150, 470, techo="conico", sem=23)
    NF.torre(L, 820, 340, 300, 760, techo="almenas", sem=24, encendidas=0.6)
    NF.torre(L, 1180, 350, 140, 520, techo="conico", sem=25)
    NF.torre(L, 1560, 380, 170, 430, techo="conico", sem=26)
    return L.capa()


@functools.lru_cache(maxsize=1)
def villa():
    """Tejados y casas de la villa entre la calle y el castillo."""
    L = Lienzo(4200, 2000, origen=(-1000, -900), sem=31)
    rng = np.random.default_rng(32)
    x = -1000
    while x < 3100:
        an = rng.uniform(200, 300)
        NF.casa_entramado(L, x, 900, an, rng.uniform(300, 480), sem=int(rng.integers(999)), encendidas=0.35)
        x += an + rng.uniform(10, 50)
    return L.capa()


@functools.lru_cache(maxsize=1)
def frente():
    """La calle: casas de entramado a los dos lados con la antorcha y el soporte del estandarte."""
    L = Lienzo(3600, 2600, origen=(-700, -1500), sem=41)
    NF.casa_entramado(L, -700, Y_CALLE, 640, 820, sem=401, encendidas=0.4)
    NF.casa_entramado(L, -40, Y_CALLE, 560, 700, sem=402, encendidas=0.5)
    NF.casa_entramado(L, 1240, Y_CALLE, 620, 860, sem=403, encendidas=0.35)
    NF.casa_entramado(L, 1880, Y_CALLE, 640, 760, sem=404, encendidas=0.4)
    NF.soporte_antorcha(L, ANTORCHA_A[0], ANTORCHA_A[1] + 20)
    x, y = ESTANDARTE_A
    L.linea([(x - 34, y - 3), (x - 60, y - 3)], 5, 0.04)                       # brazo del asta, clavado a la pared
    # un bando clavado en la puerta (el aviso que el pesquisidor mira)
    L.rect(1310, 690, 70, 92, 0.70, tex=0.06)
    for j in range(5):
        L.linea([(1318, 708 + j * 14), (1372 - (j % 2) * 14, 708 + j * 14)], 1.2, 0.25, alfa=0.8, jit=0.2)
    L.elipse(1345, 696, 4, 4, 0.04)
    return L.capa()


@functools.lru_cache(maxsize=1)
def suelo():
    L = Lienzo(3800, 1200, origen=(-700, 700), sem=61)
    NF.adoquines(L, -700, 3100, Y_CALLE, 1900, tono=0.22, sem=62)
    L.rect(-700, Y_CALLE - 6, 3800, 12, 0.30, tex=0.05)
    # pozo de piedra a la izquierda y un carro sin caballo (vida de la villa)
    NF.sillares(L, 120, 760, 190, 130, 0.24, hilada=26, largo=(30, 60), sem=63)
    L.elipse(215, 760, 98, 18, 0.30)
    L.elipse(215, 762, 80, 12, 0.03)
    for xx in (128, 300):
        L.rect(xx, 600, 12, 162, 0.16, tex=0.1)
    L.linea([(120, 600), (310, 600)], 7, 0.10)
    L.linea([(215, 600), (215, 700)], 1.4, 0.4, alfa=0.7, jit=0)
    L.rect(200, 700, 30, 26, 0.18)
    cx = 2050
    L.poli([(cx, 820), (cx + 260, 820), (cx + 250, 870), (cx + 10, 870)], 0.20, tex=0.12)
    for j in range(5):
        L.linea([(cx + 4 + j * 52, 820), (cx + 4 + j * 52, 868)], 1.2, 0.05, alfa=0.7)
    for wx in (cx + 50, cx + 210):
        L.elipse(wx, 880, 46, 46, 0.03, alfa=0.0)
        L.linea(np.array([(wx + 46 * math.cos(a), 880 + 46 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 30)]), 6, 0.10,
                cerrado=True)
        for a in np.linspace(0, math.pi, 4, endpoint=False):
            L.linea([(wx - 44 * math.cos(a), 880 - 44 * math.sin(a)), (wx + 44 * math.cos(a), 880 + 44 * math.sin(a))], 3, 0.10)
    L.linea([(cx + 260, 845), (cx + 420, 900)], 6, 0.10)
    return L.capa()


# ====================================================================== plano B: la cámara de la torre
VENT = (1180, 90, 1760, 860)          # caja de la ventana ojival (x0, y0, x1, y1)


def _ojiva(x0, y0, x1, y1, n=40):
    """Contorno de un arco apuntado: jambas rectas y dos arcos que se cruzan arriba."""
    w = x1 - x0
    r = w * 0.85
    ya = y0 + w * 0.62
    izq, der = [], []
    for a in np.linspace(0, 1, n):
        ang = a * math.acos((r - w / 2) / r)
        izq.append((x0 + r * (1 - math.cos(ang)), ya - r * math.sin(ang)))
    der = [(x1 - (px - x0), py) for px, py in izq]
    return np.array([(x0, y1)] + izq + der[::-1] + [(x1, y1)])


@functools.lru_cache(maxsize=1)
def exterior():
    L = Lienzo(1600, 1400, origen=(800, -200), base=0.08, sem=71)
    L.rect(800, -200, 1600, 1400, 0.05, grad=(0.28, -200, 900))
    L.elipse(1620, 230, 56, 56, 0.97, tex=0.0, emis=0.7)
    L.brillo(1620, 230, 260, 0.45, tono=0.85)
    rng = np.random.default_rng(72)
    for k in range(14):
        cx, cy = rng.uniform(900, 2300), rng.uniform(-150, 600)
        L.elipse(cx, cy, rng.uniform(120, 300), rng.uniform(16, 40), rng.uniform(0.14, 0.32), alfa=0.5, rug=1.2, blur=8)
    L.poli([(800, 900), (1100, 760), (1400, 720), (1800, 700), (2100, 760), (2400, 900), (2400, 1200), (800, 1200)], 0.08, tex=0.15)
    NF.torre(L, 1350, 760, 90, 300, techo="conico", sem=73, encendidas=0.7)
    NF.torre(L, 1900, 740, 120, 380, techo="almenas", sem=74, encendidas=0.7)
    NF.muralla(L, 1400, 1850, 760, 110, tono=0.22, sem=75, encendidas=0.6)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def camara():
    """Muro de sillería de la torre con el hueco de la ventana ojival (transparente) y su derrame en sombra."""
    L = Lienzo(2600, 1500, origen=(-340, -220), sem=91)
    NF.sillares(L, -340, -220, 2600, 1500, 0.26, hilada=54, largo=(90, 170), sem=92)
    x0, y0, x1, y1 = VENT
    der = _ojiva(x0 - 56, y0 - 50, x1 + 56, y1 + 40)
    L.poli(der, 0.10, tex=0.12)                                                    # derrame (el grosor del muro)
    L.linea(der, 3, 0.02, cerrado=True)
    L.trama(der, ang=60, sep=8, tono=0.02, alfa=0.4)
    # repisa de la ventana
    L.poli([(x0 - 90, y1 + 40), (x1 + 90, y1 + 40), (x1 + 110, y1 + 80), (x0 - 110, y1 + 80)], 0.34, tex=0.08)
    L.linea([(x0 - 90, y1 + 40), (x1 + 90, y1 + 40), (x1 + 110, y1 + 80), (x0 - 110, y1 + 80)], 2.4, 0.02, cerrado=True)
    m = np.zeros((L.h, L.w), np.uint8)
    hueco = _ojiva(x0, y0, x1, y1) - (L.ox, L.oy)
    cv2.fillPoly(m, [np.rint(hueco).astype(np.int32)], 1)
    L.a[m > 0] = 0
    L.g[m > 0] = 0
    return L.capa()


@functools.lru_cache(maxsize=1)
def ventanal():
    """Parteluz de piedra, tracería y la rejilla de plomo de la vidriera (con vidrios rotos que dejan pasar la luna)."""
    L = Lienzo(2600, 1500, origen=(-340, -220), sem=95)
    x0, y0, x1, y1 = VENT
    xm = (x0 + x1) / 2
    O = _ojiva(x0, y0, x1, y1)
    L.linea(O, 14, 0.30, cerrado=False, jit=0.3)
    L.rect(xm - 14, y0 + 200, 28, y1 - y0 - 200, 0.30, tex=0.1)                    # parteluz
    for xc in (x0 + (xm - x0) / 2, xm + (x1 - xm) / 2):                            # arquillos
        L.linea(np.array([(xc + (xm - x0) / 2 * math.cos(a), y0 + 250 - 90 * math.sin(a)) for a in np.linspace(0, math.pi, 20)]),
                10, 0.30, jit=0.2)
    L.linea(np.array([(xm + 70 * math.cos(a), y0 + 150 + 70 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 30)]), 9, 0.30,
            cerrado=True)
    for yy in np.arange(y0 + 260, y1, 52):                                         # plomo en rombos
        for xx in np.arange(x0, x1, 52):
            if np.random.default_rng(int(xx * 7 + yy)).uniform() < 0.82:
                L.linea([(xx, yy), (xx + 26, yy + 26), (xx + 52, yy)], 1.4, 0.05, alfa=0.85, jit=0)
                L.linea([(xx, yy + 52), (xx + 26, yy + 26)], 1.4, 0.05, alfa=0.85, jit=0)
    return L.capa()


# ====================================================================== plano C: la mesa
@functools.lru_cache(maxsize=1)
def mesa():
    L = Lienzo(2600, 1600, origen=(-340, -260), base=0.26, sem=101)
    rng = np.random.default_rng(101)
    for xx in np.arange(-340, 2260, 260):                                          # tablones gruesos de roble con clavos
        L.rect(xx, -260, 260, 1600, 0.26 + rng.uniform(-0.05, 0.04), tex=0.1)
        L.linea([(xx, -260), (xx, 1340)], 3.0, 0.04, alfa=0.9, jit=0.4)
        for j in range(18):
            x0 = xx + rng.uniform(12, 248)
            P = np.array([(x0 + 8 * math.sin(y * 0.008 + j), y) for y in np.linspace(-260, 1340, 40)])
            L.linea(P, rng.uniform(0.8, 2.0), 0.13, alfa=0.5, jit=0.3)
        for yy in (-120, 1200):
            for dx in (30, 230):
                L.elipse(xx + dx, yy, 7, 7, 0.08)
                L.elipse(xx + dx - 2, yy - 2, 2.5, 2.5, 0.5)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 220, 3, 102))
    L.g *= (0.85 + 0.25 * n).astype(np.float32)
    for k in range(6):                                                             # manchas de vino y cera viejas
        cx, cy = rng.uniform(100, 1900), rng.uniform(0, 1100)
        L.elipse(cx, cy, rng.uniform(20, 70), rng.uniform(16, 50), 0.16, alfa=0.35, rug=1.2)
    for k in range(5):                                                             # cortes de cuchillo
        x, y = rng.uniform(0, 1900), rng.uniform(0, 1100)
        L.linea([(x, y), (x + rng.uniform(30, 90), y + rng.uniform(-20, 20))], 1.2, 0.06, alfa=0.7)
    return L.capa(opaco=True)
