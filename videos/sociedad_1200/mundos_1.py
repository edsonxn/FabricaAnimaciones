# -*- coding: utf-8 -*-
"""Lugares del ACTO I, primera parte (gancho · encierro · tareas): pintados una vez en gris (noir_fondos.Lienzo) con las piezas de
mundos_base; el color lo pone noir_color.pegar con la rampa de cada material.

    gancho:   rueda (rueda de reconocimiento) · organigrama (corcho con la pirámide de 1.200 fichas y la cima vacía) ·
              bloque (el bloque de celdas de las copias, cinco pisos) · celdas_par (dos celdas vecinas en corte) ·
              calle_biblioteca (calle mojada hacia la biblioteca) · oficina_det (despacho del detective, persiana y neón)
    encierro: sf_cielo · sf_puente · sf_agua · sf_colinas (la bahía con niebla) · torre_hq (los cuarteles) · boveda ·
              lab_azulejo · pared_cajas_fuertes · gimnasio · suelo_cenital · cubiculo
    tareas:   sala_prensa · pasillo_servicio · celda_ventana · celda_puerta · pared_grieta
"""
import math

import numpy as np

import mundos_base as B
from mundos_base import mundo, muro, suelo, ventana, puerta, reja, barandilla, tuberias, conducto, estanteria, archivador, \
    servidor, cartel, lampara, cielo, ciudad, agua, colinas, niebla_banda
from noir_fondos import Lienzo, edificio, texto_lienzo, farola, letrero_vertical

Y_SUELO = 900


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== GANCHO
@mundo
def rueda():
    """Sala de la rueda de reconocimiento: pared con las líneas de estatura numeradas, focos cenitales, suelo."""
    L = Lienzo(4200, 1900, origen=(-1100, -600), base=0.3, sem=11)
    muro(L, -1100, -600, 3100, Y_SUELO, "hormigon", 0.40, sem=12)
    for k, cm in enumerate(range(140, 230, 10)):                     # líneas de estatura
        y = Y_SUELO - 40 - (cm - 140) * 5.6
        L.rect(-1100, y - 2, 4200, 5 if cm % 50 else 8, 0.10, tex=0.05, alfa=0.85)
        for x in np.arange(-1000, 3100, 520):
            texto_lienzo(L, str(cm), x, y - 22, 28, tono=0.08, fuente="C:/Windows/Fonts/courbd.ttf")
    L.rect(-1100, -600, 4200, 120, 0.12, tex=0.05)
    for x in np.arange(-1000, 3100, 300):                            # focos cenitales empotrados
        L.rect(x, -500, 160, 22, 0.95, tex=0.0, emis=0.95)
    suelo(L, -1100, 3100, Y_SUELO, 1300, "hormigon", 0.22, sem=13)
    L.rect(-1100, Y_SUELO - 6, 4200, 12, 0.16)
    return L.capa(opaco=True)


@mundo
def organigrama():
    """Corcho alto con la pirámide de fichas de las copias (de 1 a 70 por fila, ~1.200) unidas por hilos; la de arriba NO está."""
    L = Lienzo(2600, 3200, origen=(-340, -1700), base=0.25, sem=21)
    L.rect(-340, -1700, 2600, 3200, 0.22, tex=0.2)
    muro(L, -240, -1620, 2160, 1400, "corcho", 0.44, sem=22)
    L.linea([(-240, -1620), (2160, -1620), (2160, 1400), (-240, 1400)], 26, 0.18, cerrado=True, jit=0.2)
    rng = _r(23)
    filas = 26
    y = -1380
    prev = None
    for k in range(filas):
        n = 1 + int(2.6 * k)
        ancho = 150 + 2150 * (k / (filas - 1)) ** 0.85
        cw = min(120.0, ancho / max(1, n) / 1.22)
        ch = cw * 0.72
        xs = np.linspace(960 - ancho / 2, 960 + ancho / 2, n) if n > 1 else np.array([960.0])
        for x in xs:
            if k == 0:                                               # la cima: hueco más claro donde no hay nadie
                L.rect(x - cw / 2, y, cw, ch, 0.62, tex=0.05, alfa=0.55)
                L.linea([(x - cw / 2, y), (x + cw / 2, y), (x + cw / 2, y + ch), (x - cw / 2, y + ch)], 2.5, 0.25, cerrado=True,
                        alfa=0.6, jit=1.2)
                L.elipse(x, y + 8, 7, 7, 0.55)
                continue
            L.rect(x - cw / 2, y, cw, ch, 0.80 * rng.uniform(0.9, 1.05), tex=0.06)
            L.rect(x - cw * 0.3, y + ch * 0.18, cw * 0.6, ch * 0.42, 0.20, alfa=0.85)        # la «foto» (una pantalla)
            L.elipse(x, y + ch * 0.06, max(2.5, cw * 0.06), max(2.5, cw * 0.06), 0.45)
            if prev is not None and k < 12:
                j = int(np.argmin(np.abs(prev - x)))
                L.linea([(prev[j], y - 30 - k), (x, y)], 1.6, 0.45, alfa=0.55, jit=0.4)
        prev = xs
        y += ch + 26 + k * 0.6
    return L.capa(opaco=True)


@mundo
def bloque():
    """El bloque de celdas: cinco pisos de celdas con rejas y pasarelas; en cada celda brilla la pantalla de una copia."""
    L = Lienzo(5000, 3000, origen=(-1600, -1500), base=0.10, sem=31)
    muro(L, -1600, -1500, 3400, 1500, "hormigon", 0.16, sem=32)
    rng = _r(33)
    alto, ancho = 330, 250
    for piso in range(6):
        ytop = -1340 + piso * (alto + 40)
        for c in range(-6, 14):
            x = 960 + c * (ancho + 20) - ancho / 2
            L.rect(x, ytop, ancho, alto, 0.13, tex=0.05)
            L.rect(x, ytop + alto - 60, ancho, 60, 0.18, tex=0.05)
            L.rect(x + 14, ytop + alto - 120, ancho * 0.5, 22, 0.24, tex=0.05)          # catre
            L.rect(x + 14, ytop + alto - 140, ancho * 0.5, 22, 0.40, tex=0.1)
            foco = c in (-1, 0, 1) and piso in (2, 3, 4)                  # esas copias se dibujan vivas por cuadro
            # la copia dentro: monitor encendido (emisión) que ilumina su celda, casi siempre
            if rng.uniform() < 0.92 and not foco:
                cx, cy = x + ancho * rng.uniform(0.35, 0.65), ytop + alto * 0.36
                L.brillo(cx, cy, 70, 0.45, tono=0.55)
                L.rect(cx - 40, cy + 32, 80, 150, 0.12, tex=0.05)
                L.rect(cx - 34, cy - 30, 68, 60, 0.45, tex=0.0)
                L.rect(cx - 28, cy - 25, 56, 46, 0.80, tex=0.0, emis=0.6)
                L.rect(cx - 16, cy - 10, 8, 12, 0.98, tex=0.0, emis=1.0)
                L.rect(cx + 8, cy - 10, 8, 12, 0.98, tex=0.0, emis=1.0)
            reja(L, x, x + ancho, ytop, ytop + alto, sep=34, w=7, tono=0.10)
        barandilla(L, -1600, 3400, ytop + alto + 34, alto=90, sep=26, tono=0.12)
        L.rect(-1600, ytop + alto, 5000, 40, 0.14, tex=0.06)
    for k in range(5):                                               # escaleras en zigzag
        y0 = -1340 + k * 370 + 330
        L.poli([(2900, y0), (3000, y0), (3260, y0 + 370), (3160, y0 + 370)], 0.12, tex=0.1)
    suelo(L, -1600, 3400, 1100, 1500, "baldosa", 0.16, sem=34, vp=(960, -200))
    return L.capa(opaco=True)


@mundo
def celdas_par():
    """Dos celdas vecinas vistas en corte, separadas por un muro grueso (el que no los deja hablar)."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.2, sem=41)
    muro(L, -440, -300, 910, Y_SUELO, "azulejo", 0.42, sem=42)
    muro(L, 1010, -300, 2360, Y_SUELO, "azulejo", 0.38, sem=43)
    L.rect(880, -300, 160, Y_SUELO + 300, 0.26, tex=0.25)                     # el muro de en medio
    muro(L, 880, -300, 1040, Y_SUELO, "hormigon", 0.26, sem=44, manchas=False)
    L.linea([(880, -300), (880, Y_SUELO)], 3, 0.04)
    L.linea([(1040, -300), (1040, Y_SUELO)], 3, 0.04)
    for x0 in (-300, 1180):                                              # catre y estante en cada celda
        L.rect(x0, 620, 420, 40, 0.30, tex=0.1)
        L.rect(x0 + 10, 660, 20, 240, 0.14)
        L.rect(x0 + 390, 660, 20, 240, 0.14)
        L.rect(x0, 560, 420, 64, 0.62, tex=0.2)                          # colchón
        L.rect(x0 + 40, 140, 300, 14, 0.24)
        for k in range(3):
            L.rect(x0 + 60 + k * 80, 80, 50, 60, 0.5, tex=0.15)
    for x in (300, 1630):                                               # ventanuco alto con rejas
        L.rect(x, -140, 180, 110, 0.14, tex=0.05)
        reja(L, x, x + 180, -140, -30, sep=36, w=8, tono=0.08, travesanos=(0.5,))
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.24, sem=45)
    return L.capa(opaco=True)


@mundo
def calle_biblioteca():
    """Calle mojada de noche: fachadas a los lados en perspectiva y, al fondo, la gran biblioteca de columnas iluminada."""
    L = Lienzo(3600, 2200, origen=(-840, -1100), base=0.08, sem=51)
    cielo(L, -840, -1100, 2760, 400, 0.10, sem=52, estrellas=60, nubes=24)
    # la biblioteca al fondo (centro): frontón, columnas, escalinata y ventanales encendidos
    bx, by = 960, 380
    L.poli([(bx - 520, by - 300), (bx, by - 470), (bx + 520, by - 300)], 0.30, tex=0.15)
    L.rect(bx - 540, by - 300, 1080, 34, 0.40, tex=0.1)
    L.rect(bx - 500, by - 266, 1000, 420, 0.26, tex=0.15)
    for k in range(8):
        x = bx - 440 + k * 125
        L.rect(x - 22, by - 266, 44, 420, 0.46, tex=0.12)
        L.linea([(x - 22, by - 266), (x - 22, by + 154)], 2, 0.1, alfa=0.7)
        if k < 7:
            L.rect(x + 40, by - 200, 40, 150, 0.9, tex=0.0, emis=0.85)
            L.rect(x + 40, by - 20, 40, 120, 0.9, tex=0.0, emis=0.7)
    for k in range(6):
        L.rect(bx - 560 - k * 20, by + 154 + k * 18, 1120 + k * 40, 18, 0.32 - k * 0.02, tex=0.1)
    texto_lienzo(L, "BIBLIOTECA PÚBLICA DE MODELOS", bx, by - 283, 26, tono=0.06)
    # fachadas a los lados en perspectiva
    vp = (bx, by + 60)
    for lado in (-1, 1):
        for k in range(5):
            f0, f1 = 0.15 + k * 0.17, 0.15 + (k + 1) * 0.17
            xa, xb = vp[0] + lado * 1500 * (1 - f0), vp[0] + lado * 1500 * (1 - f1)
            top_a, top_b = vp[1] - 1300 * (1 - f0), vp[1] - 1300 * (1 - f1)
            bot_a, bot_b = vp[1] + 700 * (1 - f0), vp[1] + 700 * (1 - f1)
            L.poli([(xa, top_a), (xb, top_b), (xb, bot_b), (xa, bot_a)], 0.16 + 0.03 * (k % 2), tex=0.2)
            L.linea([(xb, top_b), (xb, bot_b)], 2.5, 0.03)
            rng = _r(60 + k * 2 + (lado > 0))
            for j in range(6):
                for i in range(3):
                    u = (i + 0.3) / 3
                    x0 = xa + (xb - xa) * u
                    x1 = xa + (xb - xa) * (u + 0.18)
                    ya = top_a + (top_b - top_a) * u
                    yb_ = bot_a + (bot_b - bot_a) * u
                    y = ya + (yb_ - ya) * (0.1 + j * 0.12)
                    hh = (yb_ - ya) * 0.07
                    enc = rng.uniform() < 0.3
                    L.poli([(x0, y), (x1, y + (top_b - top_a) * 0.18), (x1, y + hh + (top_b - top_a) * 0.18), (x0, y + hh)],
                           0.85 if enc else 0.10, tex=0.05, emis=0.6 if enc else 0.0)
    suelo(L, -840, 2760, vp[1] + 160, 1100, "baldosa", 0.14, sem=53, vp=vp, paso=200)
    for x in (bx - 760, bx + 760):
        farola(L, x, vp[1] + 470, alto=640)
    return L.capa(opaco=True)


@mundo
def oficina_det():
    """El despacho del detective: paneles de madera, ventana con persiana a la ciudad (neón), archivador, perchero y diplomas."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.2, sem=71)
    muro(L, -500, -340, 2400, 1000, "paneles", 0.30, sem=72)
    L.rect(-500, 940, 2900, 400, 0.22, tex=0.2)
    ventana(L, 1080, 40, 820, 640, persiana=0.55, sem=73, luna=None, encendidas=0.3)
    archivador(L, 180, 940, 260, 640, 4, tono=0.26)
    for k in range(2):
        L.rect(-260 + k * 210, 120 + k * 40, 160, 200, 0.62, tex=0.2)
        L.rect(-244 + k * 210, 136 + k * 40, 128, 168, 0.34, tex=0.2)
    L.linea([(800, 200), (800, 940)], 9, 0.08)                         # perchero con sombrero y abrigo
    L.elipse(800, 200, 50, 12, 0.10)
    L.poli([(760, 230), (840, 230), (870, 620), (730, 620)], 0.18, tex=0.2)
    return L.capa(opaco=True)


# ====================================================================== ENCIERRO
@mundo
def sf_cielo():
    L = Lienzo(5200, 2600, origen=(-1600, -1700), base=0.08, sem=81)
    cielo(L, -1600, -1700, 3600, 900, 0.16, sem=82, estrellas=220, nubes=30, luna=(1250, 60))
    L.brillo(1250, 60, 800, 0.45, tono=0.75)
    return L.capa(opaco=True)


@mundo
def sf_colinas():
    L = Lienzo(5200, 1600, origen=(-1600, -300), sem=83)
    colinas(L, -1600, 3600, 700, 420, 0.10, sem=84)
    rng = _r(85)
    for k in range(1100):                                           # luces de la ciudad en la colina
        x = rng.uniform(900, 3600)
        y = rng.uniform(380 + max(0, 1500 - x) * 0.1, 700)
        L.elipse(x, y, 2.4, 2.4, 0.9, tex=0, emis=0.8 * rng.uniform(0.4, 1.0))
    return L.capa()


@mundo
def sf_puente():
    """Puente colgante de art déco: dos torres, cables principales en catenaria, péndolas, tablero con luces."""
    L = Lienzo(5600, 2400, origen=(-1800, -1500), sem=86)
    yt = 560
    torres = (230, 1690)
    top = -1000
    for tx in torres:
        for sx in (-1, 1):
            L.poli([(tx + sx * 74 - 26, top), (tx + sx * 74 + 26, top), (tx + sx * 84 + 30, yt + 200), (tx + sx * 84 - 30, yt + 200)],
                   0.34, tex=0.06)
            L.linea([(tx + sx * 74 + (22 if sx < 0 else -22), top), (tx + sx * 84 + (26 if sx < 0 else -26), yt + 200)], 2.0, 0.6,
                    alfa=0.5)
        for k in range(4):
            y = top + 90 + k * 360
            L.rect(tx - 100, y, 200, 44, 0.32, tex=0.06)
            L.rect(tx - 60, y + 44, 120, 30, 0.10)
        L.rect(tx - 108, top - 40, 216, 50, 0.34, tex=0.06)
        L.elipse(tx, top - 70, 9, 9, 0.98, emis=1.0)
    a, b = torres
    xs = np.linspace(a, b, 90)
    ys = top + 30 + (yt - 70 - top - 30) * (1 - ((xs - (a + b) / 2) / ((b - a) / 2)) ** 2)
    L.linea(list(zip(xs, ys)), 9, 0.36, jit=0.2)
    for x, y in zip(xs[2:-2:3], ys[2:-2:3]):
        L.linea([(x, y), (x, yt)], 1.6, 0.34, alfa=0.8, jit=0.1)
    for lado, (xa, xb) in ((-1, (-1800, a)), (1, (b, 3800))):
        xs2 = np.linspace(xa, xb, 40)
        if lado < 0:
            ys2 = top + 30 + (yt - top - 30) * ((b if False else a) - xs2) / (a - xa)
        else:
            ys2 = top + 30 + (yt - top - 30) * (xs2 - b) / (xb - b)
        ys2 = np.clip(ys2, top + 30, yt)
        L.linea(list(zip(xs2, ys2)), 9, 0.36, jit=0.2)
        for x, y in zip(xs2[::3], ys2[::3]):
            L.linea([(x, y), (x, yt)], 1.6, 0.34, alfa=0.8, jit=0.1)
    L.rect(-1800, yt, 5600, 50, 0.30, tex=0.06)
    L.rect(-1800, yt + 50, 5600, 26, 0.12)
    for x in np.arange(-1700, 3800, 110):
        L.elipse(x, yt + 10, 3.5, 3.5, 0.95, emis=0.9)
    return L.capa()


@mundo
def sf_agua():
    L = Lienzo(5600, 1200, origen=(-1800, 600), base=0.08, sem=88)
    agua(L, -1800, 3800, 600, 1800, 0.10, sem=89, reflejos=90)
    return L.capa(opaco=False)


@mundo
def torre_hq():
    """Los cuarteles: torre de vidrio y acero de noche con pocos pisos encendidos, vestíbulo iluminado y garita."""
    L = Lienzo(3000, 3200, origen=(-540, -2100), base=0.08, sem=91)
    cielo(L, -540, -2100, 2460, 600, 0.09, sem=92, estrellas=90, nubes=22)
    ciudad(L, -540, 2460, 700, alto=(500, 1300), sem=93, encendidas=0.12, tipos=("cristal", "deco"), detalle=0.5)
    x0, x1 = 360, 1560
    L.rect(x0, -1900, x1 - x0, 2800, 0.12, tex=0.08)
    rng = _r(94)
    for j, y in enumerate(np.arange(-1860, 660, 60)):
        L.rect(x0, y, x1 - x0, 6, 0.20, alfa=0.9)
        enc = rng.uniform() < 0.18
        for x in np.arange(x0 + 10, x1 - 10, 60):
            if enc and rng.uniform() < 0.7:
                L.rect(x, y + 10, 50, 40, 0.9, tex=0, emis=0.7)
            else:
                L.rect(x, y + 10, 50, 40, 0.15, tex=0.1)
    for x in np.arange(x0, x1 + 1, 240):
        L.rect(x - 6, -1900, 12, 2800, 0.22)
    L.rect(x0 - 40, 660, x1 - x0 + 80, 240, 0.20, tex=0.1)                 # vestíbulo
    L.rect(x0 + 200, 700, x1 - x0 - 400, 200, 0.92, tex=0.0, emis=0.8)
    for x in np.arange(x0 + 200, x1 - 200, 80):
        L.rect(x, 700, 8, 200, 0.2)
    L.rect(x0 - 200, 900, x1 - x0 + 400, 24, 0.3)
    suelo(L, -540, 2460, 920, 1100, "baldosa", 0.14, sem=95, vp=(960, 300))
    L.rect(1700, 760, 200, 160, 0.22, tex=0.1)                                # garita
    L.rect(1720, 780, 160, 70, 0.85, emis=0.6)
    return L.capa(opaco=True)


@mundo
def boveda():
    """Dentro de la bóveda: paredes de chapa remachada y, al centro, la cámara de cristal iluminada sobre una tarima."""
    L = Lienzo(2900, 1700, origen=(-500, -320), base=0.12, sem=101)
    muro(L, -500, -320, 2400, 1380, "chapa", 0.22, sem=102)
    tuberias(L, -500, 2400, -240, n=2, tono=0.2, sem=104)
    L.rect(480, 40, 960, 800, 0.18, tex=0.05)
    L.rect(520, 80, 880, 720, 0.42, tex=0.03, alfa=0.5)
    for x in np.arange(520, 1401, 220):
        L.rect(x - 6, 80, 12, 720, 0.6)
    L.rect(480, 800, 960, 70, 0.30, tex=0.05)
    L.rect(440, 860, 1040, 30, 0.36)
    suelo(L, -500, 2400, 880, 1380, "rejilla", 0.18, sem=103, vp=(960, 200))
    return L.capa(opaco=True)


@mundo
def boveda_aro():
    """La puerta circular de la bóveda vista desde fuera: aro de acero con pernos y la hoja abierta a la izquierda; el centro es
    un hueco TRANSPARENTE (por él se ve la cámara del prototipo)."""
    L = Lienzo(3600, 2400, origen=(-840, -660), sem=105)
    L.rect(-840, -660, 3600, 2400, 0.16, tex=0.05)
    cx, cy, r = 960, 520, 520
    for k in range(28):
        a = k / 28 * 2 * math.pi
        L.rect(cx + (r + 50) * math.cos(a) - 14, cy + (r + 50) * math.sin(a) - 14, 28, 28, 0.42)
    L.elipse(cx, cy, r + 26, r + 26, 0.30, tex=0.05, alfa=0.0)
    L.linea([(cx + (r + 18) * math.cos(a), cy + (r + 18) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 120)], 30, 0.34)
    L.linea([(cx + (r + 90) * math.cos(a), cy + (r + 90) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 120)], 8, 0.08)
    yy, xx = np.mgrid[0:L.h, 0:L.w].astype(np.float32)
    d = np.sqrt((xx + L.ox - cx) ** 2 + (yy + L.oy - cy) ** 2)
    hueco = np.clip((r - d) / 3.0, 0, 1)
    L.a *= 1 - hueco
    L.g *= 1 - hueco
    L.e *= 1 - hueco
    L.elipse(cx - r - 260, cy + 20, 150, r + 20, 0.36, tex=0.08)                  # la hoja abierta, de canto
    for k in range(9):
        L.rect(cx - r - 330, cy - 400 + k * 100, 90, 26, 0.55)
    texto_lienzo(L, "ACCESO RESTRINGIDO", cx + r + 420, cy - 300, 40, tono=0.7, fuente="C:/Windows/Fonts/STENCIL.TTF")
    return L.capa()


@mundo
def lab_azulejo():
    L = Lienzo(2700, 1600, origen=(-400, -300), base=0.3, sem=111)
    muro(L, -400, -300, 2300, 860, "azulejo", 0.50, sem=112)
    tuberias(L, -400, 2300, -200, n=3, tono=0.24, sem=113)
    conducto(L, 1700, -300, 860, 18, 0.26)
    L.rect(-400, 860, 2700, 440, 0.28, tex=0.15)
    return L.capa(opaco=True)


@mundo
def pared_cajas():
    """Pared de cajas fuertes con teclado (las «cerraduras digitales» del gimnasio)."""
    L = Lienzo(2900, 1800, origen=(-500, -360), base=0.15, sem=121)
    muro(L, -500, -360, 2400, 1440, "chapa", 0.20, sem=122)
    rng = _r(123)
    for j in range(6):
        for i in range(11):
            x, y = -420 + i * 260, -300 + j * 280
            L.rect(x, y, 230, 250, 0.32, tex=0.12)
            L.rect(x + 14, y + 14, 202, 222, 0.26, tex=0.1)
            L.elipse(x + 115, y + 110, 40, 40, 0.5)
            L.elipse(x + 115, y + 110, 26, 26, 0.3)
            L.rect(x + 160, y + 170, 46, 56, 0.12)
            L.rect(x + 166, y + 176, 34, 14, 0.85 if rng.uniform() < 0.6 else 0.3, emis=0.5 if rng.uniform() < 0.6 else 0)
            for k in range(3):
                L.rect(x + 20, y + 30 + k * 70, 10, 30, 0.55)
    return L.capa(opaco=True)


@mundo
def gimnasio():
    """Gimnasio de hackeo: nave alta con ventanales, puestos numerados con una caja fuerte cada uno y carriles en el suelo."""
    L = Lienzo(3600, 2000, origen=(-840, -560), base=0.12, sem=131)
    muro(L, -840, -560, 2760, 760, "ladrillo", 0.24, sem=132)
    for k in range(6):
        ventana(L, -700 + k * 590, -460, 380, 520, noche=True, ciudad=True, sem=133 + k, encendidas=0.15)
    texto_lienzo(L, "SALA 7 · ENTRENAMIENTO", 960, 160, 64, tono=0.65, fuente="C:/Windows/Fonts/STENCIL.TTF", alfa=0.8)
    suelo(L, -840, 2760, 760, 1440, "tablones", 0.26, sem=134, vp=(960, -300), paso=190)
    for k in range(-3, 4):                                                    # carriles pintados
        L.linea([(960 + k * 120, 760), (960 + k * 520, 1440)], 6, 0.62, alfa=0.6, jit=0.3)
    for k in range(7):                                                        # puestos: jaula + caja fuerte
        x = -560 + k * 430
        L.rect(x, 380, 300, 380, 0.08, tex=0.05, alfa=0.6)
        reja(L, x, x + 300, 380, 760, sep=30, w=4, tono=0.16, travesanos=(0.05, 0.5))
        L.rect(x + 90, 560, 120, 160, 0.36, tex=0.1)
        L.elipse(x + 150, 630, 26, 26, 0.55)
        texto_lienzo(L, str(k + 1), x + 150, 410, 40, tono=0.9, fuente="C:/Windows/Fonts/impact.ttf")
    for x in np.arange(-700, 2700, 420):
        lampara(L, x, -560, 160, 140, enc=True)
    return L.capa(opaco=True)


@mundo
def suelo_cenital():
    L = Lienzo(5800, 3600, origen=(-1940, -1260), base=0.24, sem=141)
    L.rect(-1940, -1260, 5800, 3600, 0.24, tex=0.3)
    for x in np.arange(-1940, 3860, 280):
        L.linea([(x, -1260), (x, 2340)], 3, 0.36, alfa=0.5, jit=0.2)
    for y in np.arange(-1260, 2340, 200):
        L.linea([(-1940, y), (3860, y)], 3, 0.36, alfa=0.5, jit=0.2)
    return L.capa(opaco=True)


@mundo
def cubiculo():
    L = Lienzo(2600, 1500, origen=(-340, -220), base=0.2, sem=151)
    muro(L, -340, -220, 2260, 1280, "celosia", 0.30, sem=152, manchas=False)
    for x in (-340, 2000):
        L.rect(x, 100, 260, 1180, 0.36, tex=0.35)
    L.rect(-340, 100, 2600, 30, 0.42)
    L.rect(-340, 840, 2600, 440, 0.26, tex=0.2)
    return L.capa(opaco=True)


# ====================================================================== TAREAS
@mundo
def sala_prensa():
    """Sala de prensa: telón de pliegues, tarima con atril vacío y micrófonos, banderolas."""
    L = Lienzo(3000, 1700, origen=(-540, -320), base=0.1, sem=161)
    L.rect(-540, -320, 3000, 1100, 0.20)
    for x in np.arange(-540, 2460, 60):                                       # telón
        L.rect(x, -320, 30, 1100, 0.26, tex=0.15)
        L.linea([(x, -320), (x + 4, 780)], 2.0, 0.08, alfa=0.6)
    L.rect(-540, 640, 3000, 140, 0.30, tex=0.1)                               # tarima
    L.rect(860, 360, 200, 300, 0.34, tex=0.15)                                # atril
    L.rect(830, 340, 260, 40, 0.42)
    for k, (dx, a) in enumerate(((-60, -0.3), (0, 0.0), (60, 0.3))):
        L.linea([(960 + dx * 0.4, 340), (960 + dx + 30 * math.sin(a), 230)], 4, 0.08)
        L.elipse(960 + dx + 30 * math.sin(a), 222, 16, 22, 0.12)
    L.rect(-540, 780, 3000, 600, 0.12, tex=0.2)
    return L.capa(opaco=True)


@mundo
def pasillo_servicio():
    L = Lienzo(2900, 1600, origen=(-500, -300), base=0.2, sem=171)
    muro(L, -500, -300, 2400, Y_SUELO, "hormigon", 0.28, sem=172)
    tuberias(L, -500, 2400, -180, n=4, tono=0.22, sem=173)
    conducto(L, 300, -300, Y_SUELO, 20, 0.24)
    conducto(L, 1700, -300, Y_SUELO, 14, 0.22)
    L.rect(560, 40, 820, 860, 0.16, tex=0.1)                                  # marco de la puerta (por detrás)
    suelo(L, -500, 2400, Y_SUELO, 1300, "hormigon", 0.20, sem=174)
    return L.capa(opaco=True)


@mundo
def celda_ventana():
    """Celda con ventanuco alto (por él pasan el sol y la luna) y la pared donde se marcan los días."""
    L = Lienzo(2700, 1600, origen=(-400, -300), base=0.2, sem=181)
    muro(L, -400, -300, 2300, Y_SUELO, "ladrillo", 0.34, sem=182)
    L.rect(700, -120, 380, 260, 0.12, tex=0.05)
    reja(L, 700, 1080, -120, 140, sep=48, w=10, tono=0.08, travesanos=(0.5,))
    L.rect(1400, 560, 620, 50, 0.30)
    L.rect(1400, 500, 620, 70, 0.62, tex=0.2)
    for x in (1410, 1990):
        L.rect(x, 600, 20, 300, 0.14)
    suelo(L, -400, 2300, Y_SUELO, 1300, "hormigon", 0.22, sem=183)
    return L.capa(opaco=True)


@mundo
def celda_puerta():
    """Interior de una celda mirando a la puerta de acero (con mirilla) donde cuelga el candado imposible."""
    L = Lienzo(2700, 1600, origen=(-400, -300), base=0.2, sem=191)
    muro(L, -400, -300, 2300, Y_SUELO, "ladrillo", 0.30, sem=192)
    puerta(L, 700, 60, 520, 840, tono=0.26, metal=True, sem=193)
    L.rect(860, 160, 200, 70, 0.08)
    reja(L, 860, 1060, 160, 230, sep=40, w=6, tono=0.2, travesanos=())
    suelo(L, -400, 2300, Y_SUELO, 1300, "baldosa", 0.22, sem=194, vp=(960, 200))
    return L.capa(opaco=True)


@mundo
def pared_grieta():
    L = Lienzo(2800, 1700, origen=(-440, -310), base=0.2, sem=201)
    L.rect(-440, -310, 2800, 1700, 0.30, tex=0.2)
    rng = _r(202)
    bw, bh = 260, 100
    for j, y in enumerate(np.arange(-310, 1390, bh)):
        off = bw / 2 if j % 2 else 0
        for x in np.arange(-440 - off, 2360, bw):
            L.rect(x + 5, y + 5, bw - 10, bh - 10, 0.34 * rng.uniform(0.85, 1.12), tex=0.08)
            for k in range(3):
                L.elipse(x + rng.uniform(20, bw - 20), y + rng.uniform(15, bh - 15), rng.uniform(4, 12), rng.uniform(2, 6), 0.22,
                         alfa=0.6)
    return L.capa(opaco=True)
