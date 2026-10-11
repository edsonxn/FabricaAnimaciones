# -*- coding: utf-8 -*-
"""Mundos pintados (1/3) de «¿Quién envenenó al rey?»: gris con noir_fondos.Lienzo + primitivas de noir_feudal; el color lo pone
noir_color.pegar con la rampa del material. Una vez por proceso (lru_cache).

    ciudad: cielo_fiesta · fortaleza (castillo rojo en la colina) · tejados · calle_fiesta (guirnaldas y faroles) · empedrado
    salón visto desde la galería: salon_muro · salon_ventanas · salon_suelo · salon_mesas (dos mesas largas en perspectiva)
    banquete de lado: tapiz_muro (pared con tapices) · mesa_larga (mantel, fuentes, jarras)
    estrado: estrado_muro · estrado (gradas, trono y dosel)
    losas: suelo de losas en contrapicado (la copa que cae)
"""
import functools
import math

import cv2
import numpy as np

import noir_feudal as NF
from noir import fbm
from noir_fondos import Lienzo

Y_CALLE = 900
VP = (960.0, 470.0)                     # punto de fuga del salón


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== la ciudad en fiesta
@functools.lru_cache(maxsize=1)
def cielo_fiesta():
    L = Lienzo(3400, 2400, origen=(-700, -1500), base=0.08, sem=211)
    L.rect(-700, -1500, 3400, 2400, 0.05, tex=0.05, grad=(0.30, -1500, 760))
    rng = _r(213)
    L.elipse(420, -360, 64, 64, 0.97, tex=0.0, emis=0.7)                         # luna alta a la izquierda
    L.brillo(420, -360, 320, 0.38, tono=0.85)
    for k in range(36):
        cx, cy = rng.uniform(-650, 2600), rng.uniform(-1400, 500)
        rx, ry = rng.uniform(180, 520), rng.uniform(24, 60)
        L.elipse(cx, cy, rx, ry, rng.uniform(0.12, 0.26), alfa=0.5, rug=1.4, blur=10, tex=0.15)
        L.elipse(cx + rx * 0.2, cy - ry * 0.4, rx * 0.6, ry * 0.45, 0.32, alfa=0.3, rug=1.0, blur=6)
    for k in range(260):                                                          # estrellas entre las nubes
        x, y = rng.uniform(-650, 2600), rng.uniform(-1450, 200)
        L.elipse(x, y, 1.4, 1.4, rng.uniform(0.5, 0.9), tex=0, blur=0.4, alfa=rng.uniform(0.3, 0.8))
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def fortaleza():
    """La fortaleza roja sobre la colina: muralla, torres de tambor, torre del homenaje y el salón del banquete encendido."""
    L = Lienzo(4200, 2200, origen=(-1100, -1400), sem=221)
    L.poli([(-1100, 760), (-700, 520), (-200, 380), (300, 250), (900, 200), (1500, 240), (2000, 360), (2600, 540), (3100, 760)],
           0.12, tex=0.18, grad=(0.06, 250, 760))
    for k in range(30):                                                           # rocas y matorral de la colina
        rng = _r(222 + k)
        x = rng.uniform(-900, 2900)
        y = 760 - (760 - 250) * max(0.0, 1 - abs(x - 900) / 1900) * rng.uniform(0.3, 0.95)
        L.elipse(x, y, rng.uniform(30, 90), rng.uniform(14, 30), 0.08, alfa=0.7, rug=1.5)
    NF.muralla(L, -200, 2100, 300, 240, tono=0.26, sem=223, encendidas=0.55)
    for cx, al, an in ((-200, 520, 190), (400, 640, 210), (1500, 600, 200), (2100, 500, 180)):
        NF.torre(L, cx, 300, an, al, techo="almenas", sem=2000 + cx, encendidas=0.6)
    NF.torre(L, 950, 280, 300, 980, techo="conico", sem=230, encendidas=0.7)      # torre del homenaje
    # el salón del banquete: nave larga con ventanales encendidos y humo de las cocinas
    NF.sillares(L, 520, -60, 760, 300, 0.27, hilada=40, sem=231)
    L.poli([(500, -60), (900, -300), (1300, -60)], 0.16, tex=0.1, grad=(0.08, -300, -60))
    L.linea([(500, -60), (900, -300), (1300, -60)], 2.6, 0.02)
    for k in range(7):
        x = 560 + k * 104
        L.poli([(x, 180), (x, 40), (x + 26, 0), (x + 52, 40), (x + 52, 180)], 0.86, tex=0.03, emis=0.95)
        L.brillo(x + 26, 100, 70, 0.25, ry=120, tono=0.8)
        L.linea([(x + 26, 10), (x + 26, 180)], 2.0, 0.08)
        L.linea([(x, 100), (x + 52, 100)], 1.6, 0.08)
    L.linea([(520, -60), (1280, -60), (1280, 240), (520, 240)], 2.6, 0.02, cerrado=True)
    return L.capa()


@functools.lru_cache(maxsize=1)
def tejados():
    L = Lienzo(4400, 1800, origen=(-1200, -700), sem=241)
    rng = _r(242)
    x = -1200
    while x < 3200:
        an = rng.uniform(220, 320)
        NF.casa_entramado(L, x, 900, an, rng.uniform(320, 520), sem=int(rng.integers(999)), encendidas=0.55)
        x += an + rng.uniform(6, 40)
    return L.capa()


@functools.lru_cache(maxsize=1)
def calle_fiesta():
    """La calle de la fiesta: casas altas con guirnaldas de banderines y faroles colgados (emisión ámbar)."""
    L = Lienzo(4000, 2800, origen=(-900, -1700), sem=251)
    NF.casa_entramado(L, -900, Y_CALLE, 700, 900, sem=501, encendidas=0.55)
    NF.casa_entramado(L, -170, Y_CALLE, 560, 760, sem=502, encendidas=0.6)
    NF.casa_entramado(L, 1360, Y_CALLE, 640, 880, sem=503, encendidas=0.5)
    NF.casa_entramado(L, 2020, Y_CALLE, 700, 800, sem=504, encendidas=0.55)
    # guirnaldas entre las casas (cuelgan en catenaria) con banderines y faroles
    rng = _r(252)
    for (xa, ya), (xb, yb) in (((-200, 120), (1380, 160)), ((-200, 300), (1380, 260)), ((1980, 200), (2700, 240))):
        P = [(xa + (xb - xa) * u, ya + (yb - ya) * u + 120 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 60)]
        L.linea(P, 2.2, 0.05, jit=0.3)
        for u in np.linspace(0.04, 0.96, 22):
            px = xa + (xb - xa) * u
            py = ya + (yb - ya) * u + 120 * math.sin(math.pi * u)
            L.poli([(px - 14, py), (px + 14, py), (px, py + 34)], rng.choice([0.55, 0.35, 0.7]), tex=0.05)
        for u in (0.2, 0.5, 0.8):
            px = xa + (xb - xa) * u
            py = ya + (yb - ya) * u + 120 * math.sin(math.pi * u)
            L.linea([(px, py), (px, py + 30)], 1.6, 0.04)
            L.rect(px - 14, py + 30, 28, 40, 0.85, tex=0.03, emis=0.9)
            L.brillo(px, py + 50, 60, 0.35, tono=0.8)
            L.linea([(px - 14, py + 30), (px + 14, py + 30), (px + 14, py + 70), (px - 14, py + 70)], 1.8, 0.03, cerrado=True)
    # barriles, una carreta de flores y ramas de laurel en las puertas
    for bx in (420, 520, 1900):
        L.rect(bx - 40, Y_CALLE - 110, 80, 110, 0.30, tex=0.15)
        for yy in (Y_CALLE - 90, Y_CALLE - 24):
            L.linea([(bx - 42, yy), (bx + 42, yy)], 4, 0.06)
        L.linea([(bx - 40, Y_CALLE - 110), (bx + 40, Y_CALLE - 110), (bx + 40, Y_CALLE), (bx - 40, Y_CALLE)], 2.2, 0.03, cerrado=True)
    return L.capa()


@functools.lru_cache(maxsize=1)
def empedrado():
    L = Lienzo(4200, 1300, origen=(-900, 700), sem=261)
    NF.adoquines(L, -900, 3300, Y_CALLE, 2000, tono=0.22, sem=262)
    L.rect(-900, Y_CALLE - 6, 4200, 12, 0.30, tex=0.05)
    rng = _r(263)
    for k in range(40):                                                           # pétalos y confeti pisados
        L.elipse(rng.uniform(-800, 3200), rng.uniform(Y_CALLE + 20, 1900), rng.uniform(4, 9), rng.uniform(2, 4),
                 rng.choice([0.6, 0.45]), rot=rng.uniform(0, 3), alfa=0.7)
    return L.capa()


# ====================================================================== el gran salón desde la galería
def _ojiva(x0, y0, x1, y1, n=30):
    w = x1 - x0
    r = w * 0.85
    ya = y0 + w * 0.62
    izq = []
    for a in np.linspace(0, 1, n):
        ang = a * math.acos((r - w / 2) / r)
        izq.append((x0 + r * (1 - math.cos(ang)), ya - r * math.sin(ang)))
    der = [(x1 - (px - x0), py) for px, py in izq]
    return np.array([(x0, y1)] + izq + der[::-1] + [(x1, y1)])


@functools.lru_cache(maxsize=1)
def salon_muro():
    """Muro del fondo y muros laterales en perspectiva, columnas con capiteles y arcos, vigas del techo."""
    L = Lienzo(2400, 1500, origen=(-240, -300), base=0.18, sem=271)
    vx, vy = VP
    # muro del fondo
    NF.sillares(L, 520, 120, 880, 460, 0.24, hilada=30, largo=(40, 80), sem=272)
    # muros laterales (trapecios hacia el punto de fuga) con hiladas convergentes
    for sx in (-1, 1):
        xe = 520 if sx < 0 else 1400
        xo = -240 if sx < 0 else 2160
        P = [(xo, -300), (xe, 120), (xe, 580), (xo, 1200)]
        L.poli(P, 0.20, tex=0.12)
        for k in range(1, 16):
            f = k / 16
            L.linea([(xo, -300 + 1500 * f), (xe, 120 + 460 * f)], 1.4, 0.06, alfa=0.7)
        for k in range(1, 9):
            f = k / 9
            x = xo + (xe - xo) * (1 - (1 - f) ** 1.6)
            ya = -300 + (120 + 300) * (x - xo) / (xe - xo)
            yb = 1200 + (580 - 1200) * (x - xo) / (xe - xo)
            L.linea([(x, ya), (x, yb)], 1.2, 0.07, alfa=0.5)
        L.trama(P, ang=60 if sx < 0 else 120, sep=10, tono=0.02, alfa=0.25)
    # columnas con arcos apuntados a lo largo de cada muro
    for sx in (-1, 1):
        for k, f in enumerate((0.0, 0.32, 0.56, 0.74, 0.87)):
            xo = -100 if sx < 0 else 2020
            xe = 560 if sx < 0 else 1360
            x = xo + (xe - xo) * f
            s = 1 - 0.72 * f
            top = vy + (-620 - vy) * s
            bot = vy + (900 - vy) * s
            w = 90 * s
            L.rect(x - w / 2, top, w, bot - top, 0.32, tex=0.1)
            L.poli([(x - w / 2 + w * 0.6, top), (x + w / 2, top), (x + w / 2, bot), (x - w / 2 + w * 0.6, bot)], 0.16, alfa=0.7)
            L.rect(x - w * 0.75, top - 26 * s, w * 1.5, 26 * s, 0.36, tex=0.06)
            L.rect(x - w * 0.75, bot - 24 * s, w * 1.5, 24 * s, 0.30, tex=0.06)
            L.linea([(x - w / 2, top), (x + w / 2, top), (x + w / 2, bot), (x - w / 2, bot)], 2.0 * s + 0.6, 0.02, cerrado=True)
    # vigas del techo
    for k in range(7):
        f = k / 7
        y = -300 + (120 + 300) * (1 - (1 - f) ** 1.5)
        x0 = -240 + (520 + 240) * (y + 300) / 420
        x1 = 2160 - (2160 - 1400) * (y + 300) / 420
        L.poli([(x0, y), (x1, y), (x1, y + 30 * (1 - f) + 8), (x0, y + 30 * (1 - f) + 8)], 0.10, tex=0.1)
    L.linea([(520, 120), (1400, 120), (1400, 580), (520, 580)], 2.6, 0.02, cerrado=True)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def salon_ventanas():
    """Los ventanales ojivales del muro del fondo con la luna (emisión fría) y el rosetón."""
    L = Lienzo(2400, 1500, origen=(-240, -300), sem=281)
    for k, x in enumerate((600, 1230)):
        O = _ojiva(x, 180, x + 90, 470)
        L.poli(O, 0.62, tex=0.04, emis=0.55)
        L.linea([(x + 45, 220), (x + 45, 470)], 3, 0.08)
        for yy in np.arange(240, 470, 26):
            L.linea([(x, yy), (x + 90, yy)], 1.0, 0.1, alfa=0.7, jit=0)
        L.linea(O, 3.0, 0.02, cerrado=True)
    c = (960, 200)
    L.elipse(c[0], c[1], 70, 70, 0.6, tex=0.03, emis=0.5)
    for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        L.linea([c, (c[0] + 70 * math.cos(a), c[1] + 70 * math.sin(a))], 2.4, 0.08)
    L.linea(np.array([(c[0] + 70 * math.cos(a), c[1] + 70 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]), 3, 0.02,
            cerrado=True)
    return L.capa()


@functools.lru_cache(maxsize=1)
def salon_suelo():
    L = Lienzo(2400, 900, origen=(-240, 560), base=0.22, sem=291)
    vx, vy = VP
    L.rect(-240, 560, 2400, 900, 0.22, tex=0.12, grad=(0.30, 560, 1460))
    for k in range(-16, 17):                                                      # juntas hacia el punto de fuga
        xb = vx + k * 150
        L.linea([(vx + (xb - vx) * 0.04, 580), (xb, 1460)], 1.6, 0.07, alfa=0.7)
    y = 580.0
    d = 10.0
    while y < 1460:
        L.linea([(-240, y), (2160, y)], 1.4, 0.07, alfa=0.7)
        y += d
        d *= 1.28
    # alfombra roja por el pasillo central hacia el estrado
    L.poli([(930, 580), (990, 580), (1240, 1460), (680, 1460)], 0.42, tex=0.06)
    L.linea([(930, 580), (680, 1460)], 2.0, 0.02)
    L.linea([(990, 580), (1240, 1460)], 2.0, 0.02)
    return L.capa()


@functools.lru_cache(maxsize=1)
def salon_mesas():
    """Dos mesas largas con mantel que corren hacia el estrado (izquierda y derecha) y el estrado al fondo."""
    L = Lienzo(2400, 1500, origen=(-240, -300), sem=301)
    vx, vy = VP
    for sx in (-1, 1):
        xf_in, xf_out = (760, 200) if sx < 0 else (1160, 1720)
        xb_in, xb_out = (900, 820) if sx < 0 else (1020, 1100)
        top = [(xb_out, 600), (xb_in, 600), (xf_in, 1300), (xf_out, 1300)]
        L.poli(top, 0.62, tex=0.05)                                               # mantel
        for k in range(1, 14):                                                    # pliegues del mantel
            f = k / 14
            L.linea([(xb_in + (xb_out - xb_in) * f, 600), (xf_in + (xf_out - xf_in) * f, 1300)], 1.0, 0.45, alfa=0.35, jit=0.3)
        caida = [(xb_in, 600), (xb_in, 616), (xf_in, 1380), (xf_in, 1300)]
        L.poli(caida, 0.42, tex=0.05)
        L.linea(top, 2.2, 0.02, cerrado=True)
        L.linea([(xb_in, 616), (xf_in, 1380)], 2.0, 0.02)
        rng = _r(302 + sx)
        for k in range(26):                                                       # platos, fuentes y copas
            f = rng.uniform(0.05, 0.95)
            g = rng.uniform(0.2, 0.8)
            y = 600 + 700 * f
            x = (xb_out + (xf_out - xb_out) * f) + ((xb_in + (xf_in - xb_in) * f) - (xb_out + (xf_out - xb_out) * f)) * g
            s = 0.3 + 0.9 * f
            L.elipse(x, y, 26 * s, 9 * s, 0.75, tex=0.03)
            L.elipse(x, y - 2 * s, 18 * s, 6 * s, rng.choice([0.25, 0.35, 0.18]), tex=0.1)
            L.linea(np.array([(x + 26 * s * math.cos(a), y + 9 * s * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 18)]), 1.0,
                    0.03, cerrado=True, jit=0)
    # el estrado al fondo: gradas, mesa alta y el trono vacío con dosel
    L.poli([(760, 590), (1160, 590), (1180, 610), (740, 610)], 0.30, tex=0.08)
    L.poli([(800, 520), (1120, 520), (1120, 590), (800, 590)], 0.60, tex=0.05)
    L.linea([(800, 520), (1120, 520), (1120, 590), (800, 590)], 2.0, 0.02, cerrado=True)
    L.poli([(930, 380), (990, 380), (996, 520), (924, 520)], 0.34, tex=0.08)
    L.poli([(900, 330), (1020, 330), (1040, 360), (880, 360)], 0.40, tex=0.06)
    L.linea([(930, 380), (990, 380), (996, 520), (924, 520)], 2.0, 0.02, cerrado=True)
    return L.capa()


# ====================================================================== el banquete visto de lado
@functools.lru_cache(maxsize=1)
def tapiz_muro():
    """Pared del salón con tapices de caza bordados, antorchas y un arco hacia las cocinas (para el banquete de lado)."""
    L = Lienzo(3600, 1500, origen=(-700, -360), base=0.2, sem=311)
    NF.sillares(L, -700, -360, 3600, 1500, 0.22, hilada=52, largo=(90, 170), sem=312)
    O = _ojiva(1080, -200, 1420, 560)                                             # arco a las cocinas (luz cálida)
    L.poli(O, 0.5, tex=0.06, emis=0.32)
    L.brillo(1250, 300, 220, 0.18, tono=0.8)
    L.linea(O, 4, 0.02, cerrado=True)
    for x in (300, 2240):
        NF.soporte_antorcha(L, x, 160)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def tapices():
    """Los tapices de caza bordados de la pared del banquete (capa aparte: su rampa es la del estandarte)."""
    L = Lienzo(3600, 1500, origen=(-700, -360), sem=314)
    for k, x in enumerate((-460, 560, 1580, 2400)):
        if 1000 < x < 1500:
            continue
        L.rect(x, -260, 380, 600, 0.30, tex=0.18)                                 # tapiz
        L.rect(x + 20, -240, 340, 560, 0.36, tex=0.2)
        rng = _r(313 + k)
        L.elipse(x + 190, 40, 130, 90, 0.24, alfa=0.7, rug=1.2)                   # escena bordada: árbol y venado
        L.poli([(x + 120, 200), (x + 150, 120), (x + 230, 110), (x + 260, 200)], 0.20, alfa=0.8)
        for j in range(5):
            L.linea([(x + 140 + j * 20, 120), (x + 120 + j * 26, 60 - rng.uniform(0, 40))], 2.0, 0.14, alfa=0.8)
        for j in range(18):
            L.linea([(x + 20 + j * 19, 320), (x + 20 + j * 19, 352)], 2.0, 0.40, alfa=0.9)   # flecos
        L.linea([(x - 20, -270), (x + 400, -270)], 9, 0.08)                     # barra
        L.linea([(x, -260), (x + 380, -260), (x + 380, 340), (x, 340)], 2.4, 0.02, cerrado=True)
        for j in range(3):
            L.linea([(x + 60 + j * 130, -250), (x + 70 + j * 130, 320)], 2.0, 0.12, alfa=0.5)
    return L.capa()


@functools.lru_cache(maxsize=1)
def mesa_larga():
    """Mesa del banquete de lado: mantel con pliegues, fuentes con el jabalí asado, panes, frutas, jarras y candelabros."""
    L = Lienzo(3600, 700, origen=(-700, 560), sem=321)
    L.rect(-700, 600, 3600, 34, 0.66, tex=0.04)
    L.rect(-700, 634, 3600, 480, 0.56, tex=0.05, grad=(0.40, 634, 1100))
    for x in np.arange(-700, 2900, 70):
        L.linea([(x, 640), (x + 10, 1100)], 1.4, 0.40, alfa=0.45)
    L.linea([(-700, 634), (2900, 634)], 2.4, 0.02)
    rng = _r(322)
    for k in range(8):
        x = -500 + k * 440 + rng.uniform(-40, 40)
        tipo = k % 4
        if tipo == 0:                                                             # fuente con jabalí
            L.elipse(x, 600, 150, 24, 0.70, tex=0.03)
            L.poli(np.array([(x - 110, 596), (x - 90, 540), (x - 20, 520), (x + 70, 528), (x + 110, 560), (x + 130, 590)]), 0.36,
                   tex=0.12)
            L.elipse(x + 120, 560, 28, 20, 0.34)
            L.elipse(x + 146, 566, 10, 8, 0.5)
            L.linea([(x - 100, 594), (x - 90, 540), (x - 20, 520), (x + 70, 528), (x + 110, 560)], 2.2, 0.03)
        elif tipo == 1:                                                           # panes y frutas
            for j in range(5):
                L.elipse(x - 80 + j * 40, 588 - (j % 2) * 14, 30, 18, rng.choice([0.5, 0.42, 0.3]), tex=0.1)
                L.linea(np.array([(x - 80 + j * 40 + 30 * math.cos(a), 588 - (j % 2) * 14 + 18 * math.sin(a))
                                  for a in np.linspace(0, 2 * math.pi, 16)]), 1.4, 0.03, cerrado=True, jit=0)
        elif tipo == 2:                                                           # jarra y copas
            L.poli([(x - 30, 600), (x - 36, 520), (x - 22, 490), (x + 22, 490), (x + 36, 520), (x + 30, 600)], 0.46, tex=0.08)
            L.linea([(x + 34, 510), (x + 60, 520), (x + 50, 570), (x + 32, 570)], 6, 0.10)
            for dx in (-110, 90):
                L.poli([(x + dx - 16, 560), (x + dx + 16, 560), (x + dx + 10, 584), (x + dx - 10, 584)], 0.62, tex=0.05)
                L.rect(x + dx - 3, 584, 6, 12, 0.5)
                L.elipse(x + dx, 598, 12, 3, 0.5)
        else:                                                                     # fuente de aves y racimos
            L.elipse(x, 600, 120, 20, 0.66)
            for j in range(4):
                L.elipse(x - 60 + j * 40, 574, 26, 20, 0.40, tex=0.12)
            for j in range(9):
                L.elipse(x + 70 + (j % 3) * 10, 560 + (j // 3) * 12, 7, 7, 0.22)
    return L.capa()


# ====================================================================== el estrado del rey
@functools.lru_cache(maxsize=1)
def estrado_muro():
    """Muro tras el estrado: gran arco con el dosel rojo, dos estandartes (emblema sol) y candelabros de hierro de pared."""
    L = Lienzo(3000, 1700, origen=(-540, -500), base=0.2, sem=331)
    NF.sillares(L, -540, -500, 3000, 1700, 0.23, hilada=60, largo=(110, 200), sem=332)
    O = _ojiva(560, -420, 1360, 820)
    L.poli(O, 0.12, tex=0.1)
    L.trama(O, ang=70, sep=9, tono=0.02, alfa=0.3)
    L.linea(O, 6, 0.02, cerrado=True)
    L.linea(_ojiva(530, -450, 1390, 820)[1:-1], 10, 0.34, jit=0.3)
    # dosel: cortinas recogidas
    for sx in (-1, 1):
        x0 = 600 if sx < 0 else 1320
        P = [(x0, -340), (x0 + sx * -160, -320), (x0 + sx * -60, 200), (x0 + sx * -90, 820), (x0, 820)]
        L.poli(P, 0.36, tex=0.1)
        for j in range(5):
            L.linea([(x0 + sx * -30 * j, -330), (x0 + sx * -(10 + 12 * j), 200), (x0 + sx * -(16 * j), 820)], 1.6, 0.12, alfa=0.7)
        L.linea(P, 2.4, 0.02, cerrado=True)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def estrado():
    """Gradas de piedra, la mesa alta con mantel y el trono de madera tallada con respaldo alto."""
    L = Lienzo(3000, 1000, origen=(-540, 300), sem=341)
    for k in range(3):                                                            # gradas
        y = 820 + k * 70
        L.rect(-540, y, 3000, 70, 0.30 - 0.03 * k, tex=0.1)
        L.linea([(-540, y), (2460, y)], 2.4, 0.02)
        L.linea([(-540, y + 3), (2460, y + 3)], 1.6, 0.5, alfa=0.4)
    L.rect(-540, 1030, 3000, 300, 0.24, tex=0.12)
    # trono
    L.poli([(830, 260 + 60), (1090, 260 + 60), (1100, 820), (820, 820)], 0.34, tex=0.12)
    L.poli([(860, 120), (960, 40), (1060, 120), (1060, 560), (860, 560)], 0.38, tex=0.12)
    L.linea([(860, 120), (960, 40), (1060, 120), (1060, 560), (860, 560)], 3.0, 0.02, cerrado=True)
    for j in range(4):
        L.linea([(880 + j * 50, 140), (880 + j * 50, 540)], 2.0, 0.18, alfa=0.7)
    L.elipse(960, 150, 40, 40, 0.6, tex=0.04)                                      # sol tallado (emblema propio)
    for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        L.linea([(960 + 44 * math.cos(a), 150 + 44 * math.sin(a)), (960 + 66 * math.cos(a), 150 + 66 * math.sin(a))], 4, 0.55)
    L.rect(840, 560, 240, 50, 0.5, tex=0.06)
    L.linea([(830, 320), (1090, 320), (1100, 820), (820, 820)], 2.6, 0.02, cerrado=True)
    return L.capa()


# ====================================================================== suelo de losas (la copa que cae)
@functools.lru_cache(maxsize=1)
def losas():
    L = Lienzo(2600, 1500, origen=(-340, -200), base=0.2, sem=351)
    rng = _r(352)
    vx, vy = 960, -900
    L.rect(-340, -200, 2600, 1500, 0.22, tex=0.14, grad=(0.30, -200, 1300))
    for k in range(-12, 13):
        xb = vx + k * 220
        L.linea([(vx + (xb - vx) * 0.45, -200), (xb, 1300)], 2.0, 0.06, alfa=0.85)
    y = -200.0
    d = 120.0
    while y < 1300:
        L.linea([(-340, y), (2260, y)], 2.0, 0.06, alfa=0.85)
        y += d
        d *= 1.14
    for k in range(60):
        x, y = rng.uniform(-300, 2200), rng.uniform(-150, 1250)
        L.elipse(x, y, rng.uniform(6, 30), rng.uniform(3, 10), rng.uniform(0.14, 0.32), alfa=0.5, rug=1.2)
    for k in range(30):                                                           # pétalos y migas del banquete
        L.elipse(rng.uniform(-300, 2200), rng.uniform(-150, 1250), rng.uniform(5, 10), rng.uniform(2, 4), 0.55,
                 rot=rng.uniform(0, 3), alfa=0.8)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 300, 3, 353))
    L.g *= (0.8 + 0.3 * n).astype(np.float32)
    return L.capa(opaco=True)
