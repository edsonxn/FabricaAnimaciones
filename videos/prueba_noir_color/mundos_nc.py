# -*- coding: utf-8 -*-
"""Mundos pintados de la prueba del estilo NOIR COLOR (en gris con noir_fondos; el color lo pone noir_color.pegar con una
rampa por material). Se pintan una vez por proceso (lru_cache) y se guardan como Capa uint8.

    cielo · lejos · medio · fachadas · suelo · neon_hotel      -> la calle de noche (plano A)
    afuera · neon_bar · oficina · muebles                       -> la oficina del detective (plano B)
    escritorio                                                  -> el escritorio visto desde arriba (plano C)
"""
import functools
import math

import numpy as np

from noir import fbm
from noir_fondos import Lienzo, edificio, escalera_incendio, farola, texto_lienzo, ventana

Y_ACERA = 860
Y_BORDILLO = 965
X_FAROLA = 1180                    # el farol cuelga en x = X_FAROLA - 60
X_FAROLA2 = 1700                   # la segunda farola mira al otro lado (farol en X_FAROLA2 + 60)
NEON = (604, -390)                 # esquina sup-izq del letrero HOTEL
IMPACT = "C:/Windows/Fonts/impact.ttf"


# ====================================================================== plano A: la calle
@functools.lru_cache(maxsize=1)
def cielo():
    L = Lienzo(3000, 2400, origen=(-540, -1500), base=0.08, sem=11)
    L.rect(-540, -1500, 3000, 2400, 0.05, tex=0.05, grad=(0.34, -1500, 820))
    rng = np.random.default_rng(12)
    L.elipse(1560, -760, 62, 62, 0.97, tex=0.0, emis=0.7)                      # luna velada
    L.brillo(1560, -760, 300, 0.35, tono=0.85)
    for k in range(46):                                                       # nubes de tormenta: bancos rasgados
        cx, cy = rng.uniform(-500, 2400), rng.uniform(-1400, 500)
        rx, ry = rng.uniform(160, 520), rng.uniform(26, 70)
        L.elipse(cx, cy, rx, ry, rng.uniform(0.12, 0.30), alfa=0.55, rug=1.4, blur=10, tex=0.15)
        L.elipse(cx + rx * 0.2, cy - ry * 0.4, rx * 0.6, ry * 0.45, 0.36 + 0.1 * (abs(cx - 1560) < 500), alfa=0.35, rug=1.0, blur=6)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def lejos():
    L = Lienzo(4400, 2400, origen=(-1100, -1500), sem=21)
    rng = np.random.default_rng(22)
    x = -1100
    while x < 3200:
        an = rng.uniform(170, 330)
        tipo = rng.choice(["deco", "ladrillo", "ladrillo"])
        edificio(L, x, 860, an, rng.uniform(600, 1500), tipo=str(tipo), sem=int(rng.integers(999)), encendidas=0.10, detalle=0.3)
        x += an + rng.uniform(-30, 40)
    return L.capa()


@functools.lru_cache(maxsize=1)
def medio():
    L = Lienzo(4000, 2400, origen=(-900, -1500), sem=31)
    rng = np.random.default_rng(32)
    x = -900
    while x < 3000:
        an = rng.uniform(260, 420)
        edificio(L, x, 880, an, rng.uniform(780, 1350), tipo="ladrillo" if rng.uniform() < 0.7 else "deco",
                 sem=int(rng.integers(999)), encendidas=0.16, detalle=0.6)
        x += an + rng.uniform(20, 90)
    return L.capa()


@functools.lru_cache(maxsize=1)
def fachadas():
    """Primer término: tienda, edificio del hotel, callejón con escalera de incendio, más fachadas."""
    L = Lienzo(3600, 2600, origen=(-600, -1500), sem=41)
    edificio(L, -600, Y_ACERA, 560, 1150, tipo="tienda", sem=401, encendidas=0.2)
    edificio(L, 0, Y_ACERA, 600, 1500, tipo="ladrillo", sem=402, encendidas=0.22)
    L.rect(640, -300, 150, Y_ACERA + 300, 0.03, tex=0.15)                               # callejón
    L.trama([(640, 120), (790, 120), (790, Y_ACERA), (640, Y_ACERA)], ang=70, sep=8, tono=0.0, alfa=0.5)
    escalera_incendio(L, 655, 160, Y_ACERA - 70, w=100, piso=110, tono=0.12)
    edificio(L, 790, Y_ACERA, 620, 1180, tipo="ladrillo", sem=403, encendidas=0.3)
    edificio(L, 1450, Y_ACERA, 560, 1600, tipo="ladrillo", sem=404, encendidas=0.18)
    edificio(L, 2040, Y_ACERA, 640, 1250, tipo="tienda", sem=405, encendidas=0.25)
    # brazos del letrero del hotel, anclados a la pared
    x, y = NEON
    for yy in (y + 40, y + 300):
        L.linea([(x - 6, yy), (x - 40, yy + 8)], 5, 0.03)
    return L.capa()


@functools.lru_cache(maxsize=1)
def neon_hotel():
    """Letrero vertical de neón del hotel: caja oscura, letras de tubo (emisivas) y bombillas."""
    L = Lienzo(220, 460, origen=(NEON[0] - 40, NEON[1] - 40), sem=51)
    x, y = NEON
    ancho, px = 84, 60
    alto = 5 * px * 1.05 + 46
    L.rect(x, y, ancho, alto, 0.07, tex=0.08)
    L.linea([(x, y), (x + ancho, y), (x + ancho, y + alto), (x, y + alto)], 3, 0.02, cerrado=True)
    for k, c in enumerate("HOTEL"):
        texto_lienzo(L, c, x + ancho / 2, y + 30 + k * px * 1.05, px, tono=0.95, fuente=IMPACT)
    for k in range(int(alto // 20)):
        for bx in (x + 9, x + ancho - 9):
            L.elipse(bx, y + 12 + k * 20, 3, 3, 0.9, emis=0.8)
    m = (L.g > 0.8) & (L.a > 0.5)
    L.e[m] = 1.0
    return L.capa()


@functools.lru_cache(maxsize=1)
def suelo():
    """Acera, bordillo, asfalto mojado con charcos, boca de incendios, cubos y la farola."""
    L = Lienzo(3800, 1600, origen=(-700, 200), sem=61)
    rng = np.random.default_rng(61)
    L.poli([(-700, Y_ACERA), (3100, Y_ACERA), (3100, Y_BORDILLO), (-700, Y_BORDILLO)], 0.30, tex=0.1,
           grad=(0.22, Y_ACERA, Y_BORDILLO))
    for bx in np.arange(-700, 3100, 120):
        L.linea([(bx, Y_ACERA), (bx - 36, Y_BORDILLO)], 1.2, 0.08, alfa=0.5, jit=0.3)
    L.rect(-700, Y_BORDILLO - 6, 3800, 14, 0.42, tex=0.05)
    L.linea([(-700, Y_BORDILLO - 6), (3100, Y_BORDILLO - 6)], 2, 0.6, alfa=0.6)
    L.poli([(-700, Y_BORDILLO + 8), (3100, Y_BORDILLO + 8), (3100, 1800), (-700, 1800)], 0.10, tex=0.14,
           grad=(0.05, 990, 1400))
    for k in range(22):
        cx, cy = rng.uniform(-600, 3000), rng.uniform(1000, 1300)
        L.elipse(cx, cy, rng.uniform(70, 240), rng.uniform(8, 24), 0.20, alfa=0.7, rug=1.0, tex=0.05)
    for k in range(30):
        L.poli([(k * 140 - 700, 1160), (k * 140 - 620, 1160), (k * 140 - 622, 1168), (k * 140 - 702, 1168)], 0.32, alfa=0.7)
    hx = 380
    L.poli([(hx - 14, Y_BORDILLO - 4), (hx + 14, Y_BORDILLO - 4), (hx + 12, Y_BORDILLO - 50), (hx - 12, Y_BORDILLO - 50)], 0.16)
    L.elipse(hx, Y_BORDILLO - 52, 16, 9, 0.22)
    L.rect(hx - 22, Y_BORDILLO - 36, 44, 9, 0.14)
    for cx in (690, 742):
        L.poli([(cx - 22, Y_ACERA + 4), (cx + 22, Y_ACERA + 4), (cx + 18, Y_ACERA - 58), (cx - 18, Y_ACERA - 58)], 0.12)
        L.elipse(cx, Y_ACERA - 60, 24, 7, 0.18)
        for k in range(3):
            L.linea([(cx - 20 + k * 2, Y_ACERA - 44 + k * 15), (cx + 20 - k * 2, Y_ACERA - 44 + k * 15)], 1.5, 0.03, jit=0)
    for xf, br in ((X_FAROLA, 60), (X_FAROLA2, -60)):
        base = Y_ACERA + 40
        farola(L, xf, base, alto=520, brazo=br)
        L.linea([(xf - 6, base - 44), (xf - 4, base - 516)], 2.6, 0.62, alfa=0.75, jit=0.2)      # filo de luna en el fuste
        L.linea([(xf + 5, base - 60), (xf + 4, base - 500)], 1.6, 0.38, alfa=0.5, jit=0.2)       # y el reflejo del farol
        L.linea([(xf, base - 512), (xf - br * 0.3, base - 548), (xf - br, base - 538)], 2.0, 0.55, alfa=0.7, jit=0.2)
    return L.capa()


# ====================================================================== plano B: la oficina
VENT = (1160, 110, 1800, 830)        # hueco de la ventana (x0, y0, x1, y1) en el mundo del plano B


@functools.lru_cache(maxsize=1)
def afuera():
    """Lo que se ve por la ventana: cielo de lluvia y edificios con ventanas encendidas."""
    L = Lienzo(1400, 1300, origen=(900, -150), base=0.10, sem=71)
    L.rect(900, -150, 1400, 1300, 0.06, grad=(0.24, -150, 900))
    rng = np.random.default_rng(72)
    x = 900
    while x < 2300:
        an = rng.uniform(120, 230)
        edificio(L, x, 1150, an, rng.uniform(500, 1050), tipo="ladrillo", sem=int(rng.integers(999)), encendidas=0.3, detalle=0.4)
        x += an + rng.uniform(10, 60)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def neon_bar():
    """Neón de enfrente, grande y cortado por el marco: «BAR» en tubo."""
    L = Lienzo(700, 400, origen=(1350, 260), sem=81)
    L.rect(1420, 300, 520, 230, 0.06, tex=0.1)
    texto_lienzo(L, "BAR", 1680, 330, 170, tono=0.95, fuente=IMPACT, track=8)
    m = (L.g > 0.8) & (L.a > 0.5)
    L.e[m] = 1.0
    return L.capa()


@functools.lru_cache(maxsize=1)
def oficina():
    """Pared empapelada (rayas) con zócalo; el hueco de la ventana queda transparente."""
    L = Lienzo(2600, 1500, origen=(-340, -220), sem=91)
    x0, y0, x1, y1 = VENT
    pared = [(-340, -220), (2260, -220), (2260, 1280), (-340, 1280)]
    L.poli(pared, 0.24, tex=0.12, grad=(0.15, -220, 1280))
    for xx in np.arange(-340, 2260, 52):
        L.rect(xx, -220, 14, 1500, 0.19, alfa=0.55, tex=0.05)
        L.linea([(xx + 7, -220), (xx + 7, 1280)], 1.0, 0.30, alfa=0.25, jit=0.2)
    for xx in np.arange(-340, 2260, 104):                       # motivo de flor de lis entre rayas
        for yy in np.arange(-180, 760, 120):
            L.elipse(xx + 33, yy + (xx // 104 % 2) * 60, 6, 10, 0.30, alfa=0.35)
    L.rect(-340, 790, 2600, 490, 0.14, tex=0.14, grad=(0.10, 790, 1280))   # zócalo de madera oscura
    L.rect(-340, 780, 2600, 18, 0.30, tex=0.05)
    for xx in np.arange(-300, 2260, 260):
        L.linea([(xx, 820), (xx + 200, 820), (xx + 200, 1240), (xx, 1240)], 2, 0.05, cerrado=True, alfa=0.7)
    # mancha de humedad y desconchado (vida del lugar)
    L.elipse(120, 120, 180, 120, 0.12, alfa=0.35, rug=1.5, blur=14)
    # el hueco de la ventana: se borra el alfa
    a0, b0 = x0 - L.ox, y0 - L.oy
    L.a[int(b0):int(b0 + (y1 - y0)), int(a0):int(a0 + (x1 - x0))] = 0
    return L.capa()


@functools.lru_cache(maxsize=1)
def muebles():
    """Marco de la ventana, persiana de listones a medio abrir, perchero con fedora y gabardina."""
    L = Lienzo(2600, 1500, origen=(-340, -220), sem=95)
    x0, y0, x1, y1 = VENT
    for k, yy in enumerate(np.arange(y0 + 4, y0 + (y1 - y0) * 0.62, 34)):     # persiana: listones con hueco
        L.poli([(x0, yy), (x1, yy + 2), (x1, yy + 17), (x0, yy + 15)], 0.40, tex=0.08, grad=(0.30, yy, yy + 16))
        L.linea([(x0, yy + 15), (x1, yy + 17)], 1.4, 0.03, jit=0.2)
    yb = y0 + (y1 - y0) * 0.62
    L.rect(x0, yb, x1 - x0, 22, 0.34, tex=0.06)                                  # barra inferior de la persiana
    for xc in (x0 + 140, x1 - 140):
        L.linea([(xc, y0), (xc, yb + 10)], 1.6, 0.6, alfa=0.7, jit=0)
    L.linea([(x1 - 60, yb + 22), (x1 - 56, yb + 150)], 2.0, 0.55, jit=0.4)        # cordón
    L.elipse(x1 - 56, yb + 156, 7, 10, 0.5)
    for P in ([(x0 - 40, y0 - 40), (x1 + 40, y0 - 40), (x1 + 40, y0), (x0 - 40, y0)],
              [(x0 - 40, y0 - 40), (x0, y0 - 40), (x0, y1 + 40), (x0 - 40, y1 + 40)],
              [(x1, y0 - 40), (x1 + 40, y0 - 40), (x1 + 40, y1 + 40), (x1, y1 + 40)],
              [(x0 - 60, y1), (x1 + 60, y1), (x1 + 70, y1 + 34), (x0 - 70, y1 + 34)]):
        L.poli(P, 0.30, tex=0.1)
        L.linea(P, 2.2, 0.02, cerrado=True)
    xm = (x0 + x1) / 2
    L.rect(xm - 10, y0, 20, y1 - y0, 0.30, tex=0.08)                              # parteluz
    L.rect(x0, (y0 + y1) / 2 - 8, x1 - x0, 16, 0.30, tex=0.08)
    # perchero con la fedora y la gabardina colgadas (izquierda)
    px = 90
    L.rect(px - 9, 60, 18, 1220, 0.22, tex=0.1, grad=(0.12, 60, 1280))
    for a in (-1, 1):
        L.linea([(px, 120), (px + a * 70, 90)], 6, 0.10)
    L.poli([(px - 120, 140), (px + 80, 140), (px + 110, 760), (px + 40, 790), (px - 60, 770), (px - 150, 790)], 0.33, tex=0.14,
           rug=0.6)
    for xx in (-70, -10, 50):
        L.linea([(px + xx, 160), (px + xx + 12, 770)], 2.0, 0.08, alfa=0.7)
    L.elipse(px - 10, 92, 130, 20, 0.16)                                          # ala de la fedora
    L.poli([(px - 90, 92), (px - 76, 20), (px + 60, 20), (px + 74, 92)], 0.18, tex=0.1)
    L.rect(px - 86, 70, 156, 16, 0.05)
    return L.capa()


# ====================================================================== plano C: el escritorio desde arriba
@functools.lru_cache(maxsize=1)
def escritorio():
    L = Lienzo(2600, 1600, origen=(-340, -260), base=0.3, sem=101)
    rng = np.random.default_rng(101)
    for k, xx in enumerate(np.arange(-340, 2260, 230)):                       # tablones con veta
        L.rect(xx, -260, 230, 1600, 0.30 + rng.uniform(-0.05, 0.04), tex=0.08)
        L.linea([(xx, -260), (xx, 1340)], 2.0, 0.05, alfa=0.8, jit=0.3)
        for j in range(16):
            x0 = xx + rng.uniform(12, 218)
            P = np.array([(x0 + 6 * math.sin(y * 0.01 + j), y) for y in np.linspace(-260, 1340, 40)])
            L.linea(P, rng.uniform(0.8, 1.8), 0.16, alfa=0.45, jit=0.2)
        for j in range(2):                                                    # nudos
            cx, cy = xx + rng.uniform(40, 190), rng.uniform(-200, 1300)
            L.elipse(cx, cy, 14, 34, 0.14, alfa=0.7)
            L.elipse(cx, cy, 24, 50, 0.20, alfa=0.35)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 220, 3, 102))
    L.g *= (0.85 + 0.25 * n).astype(np.float32)                               # desgaste: zonas más claras por el uso
    for k in range(4):                                                        # cercos de vasos viejos
        cx, cy = rng.uniform(200, 1800), rng.uniform(100, 1000)
        L.elipse(cx, cy, 70, 70, 0.20, alfa=0.25)
        L.elipse(cx, cy, 62, 62, 0.30, alfa=0.25)
    return L.capa(opaco=True)
