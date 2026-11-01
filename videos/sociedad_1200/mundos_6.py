# -*- coding: utf-8 -*-
"""Lugares del ACTO V (filosofia_peligro · dos_reglas · ironia_metr · tablero_final · cierre).

    filosofia_peligro: oxford (agujas góticas y la cúpula de la Radcliffe bajo la lluvia) · estudio_oxford (el despacho del filósofo:
                       estantes de libros, escalera, lámpara de pantalla verde)
    ironia_metr:       sala_cajas (la sala del informe: pilas de cajas de archivo y una mesa larga bajo un fluorescente)
    tablero_final:     despacho_noche (el despacho del detective: corcho enorme, ventana con neón, escritorio con lámpara)
    cierre:            ciudad_noche (el skyline completo desde la ventana, con miles de ventanas)
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


# ====================================================================== FILOSOFIA
@mundo
def oxford():
    """Oxford de noche bajo la lluvia: la cúpula redonda de la Radcliffe Camera, agujas góticas con pináculos, ventanales
    ojivales encendidos y adoquines mojados."""
    L = Lienzo(3600, 2200, origen=(-840, -1100), base=0.08, sem=701)
    rng = _r(702)
    cielo(L, -840, -1100, 2760, 560, 0.12, sem=703, estrellas=0, nubes=34)
    # fachada gótica larga de fondo
    L.rect(-840, 330, 3600, 700, 0.27, tex=0.2)
    for k in range(18):
        x = -820 + k * 205
        L.rect(x, 330, 24, 700, 0.34, tex=0.1)
        # ventanal ojival encendido
        enc = rng.uniform() < 0.55
        L.poli([(x + 40, 760), (x + 40, 520), (x + 100, 440), (x + 160, 520), (x + 160, 760)], 0.88 if enc else 0.10, tex=0.05,
               emis=0.7 if enc else 0.0)
        L.linea([(x + 100, 440), (x + 100, 760)], 3, 0.04)
        L.linea([(x + 40, 600), (x + 160, 600)], 3, 0.04)
    # almenas
    for k in range(60):
        L.rect(-840 + k * 62, 292, 38, 40, 0.18, tex=0.1)
    # agujas / torres con pináculos
    for cx, alto, an in ((60, 760, 190), (560, 560, 150), (1380, 820, 200), (1860, 620, 160), (2300, 700, 170)):
        L.rect(cx - an / 2, 1000 - alto, an, alto, 0.32, tex=0.2)
        L.poli([(cx - an / 2 - 10, 1000 - alto), (cx, 1000 - alto - 360), (cx + an / 2 + 10, 1000 - alto)], 0.26, tex=0.15)
        for dx in (-an / 2, an / 2):
            L.poli([(cx + dx - 12, 1000 - alto), (cx + dx, 1000 - alto - 90), (cx + dx + 12, 1000 - alto)], 0.17)
        for j in range(4):
            L.poli([(cx - 20, 1000 - alto + 80 + j * 150), (cx, 1000 - alto + 30 + j * 150), (cx + 20, 1000 - alto + 80 + j * 150),
                    (cx + 20, 1000 - alto + 190 + j * 150), (cx - 20, 1000 - alto + 190 + j * 150)], 0.9 if (j + cx) % 3 else 0.1, emis=0.6 if (j + cx) % 3 else 0.0, tex=0.05)
    # la cúpula de la Radcliffe Camera
    bx, by = 960, 780
    L.rect(bx - 340, by - 120, 680, 250, 0.36, tex=0.2)
    for k in range(9):
        L.rect(bx - 320 + k * 76, by - 100, 30, 220, 0.26, tex=0.1)
        L.poli([(bx - 306 + k * 76, by + 10), (bx - 306 + k * 76, by - 60), (bx - 282 + k * 76, by - 90), (bx - 258 + k * 76, by - 60),
                (bx - 258 + k * 76, by + 10)], 0.9, emis=0.6, tex=0.05)
    n = 36
    dom = [(bx - 340 + 680 * i / n, by - 120 - 270 * math.sin(math.pi * i / n) ** 0.8) for i in range(n + 1)]
    L.poli(dom, 0.42, tex=0.2)
    for i in range(1, 8):
        a = i / 8
        L.linea([(bx, by - 120 - 270), (bx - 340 + 680 * a, by - 120)], 2.2, 0.08, alfa=0.7)
    L.rect(bx - 22, by - 440, 44, 60, 0.30, tex=0.1)
    L.poli([(bx - 22, by - 440), (bx, by - 520), (bx + 22, by - 440)], 0.3)
    L.brillo(bx, by - 200, 600, 0.35, ry=400, tono=0.7)
    suelo(L, -840, 2760, 1000, 1100, "baldosa", 0.15, sem=704, vp=(960, 300), paso=170)
    for x in (140, 1780):
        farola(L, x, 1090, alto=700)
    for cx, cy, rx in ((520, 1060, 220), (1400, 1060, 300), (960, 1080, 200)):
        L.elipse(cx, cy, rx, 14, 0.45, alfa=0.7, blur=2)
    return L.capa(opaco=True)


@mundo
def estudio_oxford():
    """Despacho universitario: estantes de libros a los dos lados, escalera de biblioteca, ventanal ojival con lluvia y una
    lámpara de pantalla verde sobre el escritorio."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.14, sem=711)
    muro(L, -500, -340, 2400, Y_SUELO, "paneles", 0.24, sem=712)
    for x0 in (-100, 1520):
        estanteria(L, x0, Y_SUELO - 10, 480, 1000, niveles=6, tono=0.20, sem=713 + x0 % 7, rotulos=False, tono_caja=0.38)
    # ventanal ojival al centro
    L.poli([(660, 760), (660, 260), (760, 100), (860, 40), (960, 20), (1060, 40), (1160, 100), (1260, 260), (1260, 760)], 0.09, tex=0.05)
    L.poli([(690, 740), (690, 270), (780, 120), (960, 50), (1140, 120), (1230, 270), (1230, 740)], 0.20, tex=0.05, grad=(0.34, 50, 740))
    for x in (810, 960, 1110):
        L.linea([(x, 50), (x, 740)], 5, 0.07)
    for y in (260, 420, 580):
        L.linea([(690, y), (1230, y)], 5, 0.07)
    # escalera de biblioteca apoyada
    L.linea([(420, 880), (500, 150)], 14, 0.12)
    L.linea([(520, 880), (580, 150)], 14, 0.12)
    for k in range(10):
        y = 200 + k * 68
        L.linea([(500 - (y - 150) * 0.0 + (880 - y) * -0.1, y), (520 + (880 - y) * -0.1 + 60, y)], 8, 0.14)
    suelo(L, -500, 2400, Y_SUELO, 1360, "tablones", 0.18, sem=714, vp=(960, 300))
    # escritorio y lámpara
    L.rect(560, 760, 800, 34, 0.40, tex=0.1)
    L.rect(560, 794, 800, 150, 0.22, tex=0.12)
    L.rect(1180, 650, 14, 112, 0.08)
    L.poli([(1130, 650), (1244, 650), (1220, 590), (1154, 590)], 0.50, tex=0.1, emis=0.35)
    return L.capa(opaco=True)


# ====================================================================== METR
@mundo
def sala_cajas():
    """Sala de archivo: pilas de cajas con etiquetas contra las paredes, una mesa larga bajo un fluorescente y la puerta."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.15, sem=721)
    muro(L, -500, -340, 2400, Y_SUELO, "hormigon", 0.22, sem=722)
    rng = _r(723)
    for x0, n in ((-80, 5), (1440, 5)):
        for fila in range(6):
            for c in range(n):
                x = x0 + c * 90 + (fila % 2) * 40
                y = Y_SUELO - 10 - (fila + 1) * 100
                L.rect(x, y, 86, 96, 0.34 * rng.uniform(0.8, 1.2), tex=0.25)
                L.rect(x + 14, y + 36, 58, 26, 0.74, alfa=0.9)
                L.linea([(x, y), (x + 86, y), (x + 86, y + 96), (x, y + 96)], 1.6, 0.05, cerrado=True, alfa=0.8)
    puerta(L, 1000, 140, 340, 760, tono=0.20, metal=True, sem=724)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.17, sem=725, vp=(960, 300))
    L.rect(300, 760, 1280, 36, 0.46, tex=0.1)
    L.rect(300, 796, 1280, 140, 0.22, tex=0.12)
    L.rect(560, 60, 800, 24, 0.80, emis=0.8)                                      # fluorescente
    return L.capa(opaco=True)


# ====================================================================== TABLERO FINAL
@mundo
def despacho_noche():
    """El despacho de noche, visto de frente: un corcho enorme cubre la pared, a la izquierda la ventana con persiana y neón,
    a la derecha el perchero y el escritorio con la lámpara."""
    L = Lienzo(3200, 1800, origen=(-640, -380), base=0.14, sem=731)
    muro(L, -640, -380, 2560, Y_SUELO, "paneles", 0.22, sem=732)
    # corcho
    L.rect(130, 60, 1900, 760, 0.07, tex=0.1)
    L.rect(150, 80, 1860, 720, 0.34, tex=0.22)
    rng = _r(733)
    for k in range(260):
        L.elipse(rng.uniform(160, 2000), rng.uniform(90, 790), rng.uniform(2, 6), rng.uniform(2, 6), 0.22, alfa=0.5)
    # ventana a la izquierda
    ventana(L, -420, 140, 420, 560, persiana=0.5, sem=734, luna=None, encendidas=0.35)
    suelo(L, -640, 2560, Y_SUELO, 1400, "tablones", 0.17, sem=735, vp=(960, 300))
    # escritorio a la derecha
    L.rect(1240, 800, 700, 36, 0.40, tex=0.1)
    L.rect(1240, 836, 700, 170, 0.22, tex=0.12)
    L.linea([(2150, 160), (2150, 900)], 9, 0.08)                              # perchero
    L.poli([(2100, 200), (2200, 200), (2230, 620), (2070, 620)], 0.18, tex=0.2)
    return L.capa(opaco=True)


# ====================================================================== CIERRE
@mundo
def ciudad_noche():
    """El skyline completo de noche visto desde una ventana alta: miles de ventanas, torres con antenas y la bahía al fondo."""
    L = Lienzo(3600, 2400, origen=(-840, -1200), base=0.07, sem=741)
    cielo(L, -840, -1200, 2760, 380, 0.14, sem=742, estrellas=140, nubes=18, luna=(1500, -300))
    colinas(L, -840, 2760, 520, alto=240, tono=0.07, sem=3)
    for k, (base, alto) in enumerate(((560, (300, 700)), (700, (420, 980)), (900, (520, 1200)))):
        ciudad(L, -840, 2760, base, alto=alto, sem=743 + k, encendidas=0.30 + 0.06 * k, detalle=0.9)
    rng = _r(748)
    for k in range(7):                                                      # antenas con luz roja
        x = rng.uniform(-700, 2600)
        L.linea([(x, 40 + rng.uniform(0, 300)), (x, -200 - rng.uniform(0, 200))], 3, 0.1)
        L.elipse(x, -200 - rng.uniform(0, 100), 5, 5, 0.9, emis=0.9)
    agua(L, -840, 2760, 900, 1200, 0.12, sem=749, reflejos=90)
    niebla_banda(L, -840, 2760, 640, 160, tono=0.4, alfa=0.3, sem=750)
    return L.capa(opaco=True)


@mundo
def deposito():
    """Depósito de la sala de máquinas: muro de hormigón, fila de bastidores de servidores al fondo, jaulas de metal y suelo de rejilla."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.14, sem=761)
    muro(L, -500, -340, 2400, Y_SUELO, "hormigon", 0.22, sem=762)
    for k in range(9):
        servidor(L, -300 + k * 260, Y_SUELO - 10, w=220, hh=560 + 60 * (k % 3), tono=0.12, sem=763 + k, leds=0.5)
    tuberias(L, -500, 2400, 20, n=3, sep=30, tono=0.20, sem=772)
    suelo(L, -500, 2400, Y_SUELO, 1360, "rejilla", 0.17, sem=773, vp=(960, 300))
    lampara(L, 480, -340, 560, 200)
    lampara(L, 1440, -340, 560, 200)
    return L.capa(opaco=True)


@mundo
def celdas_alba():
    """El bloque de celdas al amanecer, VACÍO: tres pisos de celdas con la reja abierta, catres deshechos, pantallas apagadas y
    la luz fría de la mañana entrando por los ventanales del fondo."""
    L = Lienzo(4200, 2600, origen=(-1200, -1300), base=0.16, sem=781)
    muro(L, -1200, -1300, 3000, 1400, "hormigon", 0.24, sem=782)
    rng = _r(783)
    alto, ancho = 330, 250
    for piso in range(5):
        ytop = -1160 + piso * (alto + 40)
        for c in range(-5, 12):
            x = 960 + c * (ancho + 20) - ancho / 2
            L.rect(x, ytop, ancho, alto, 0.20, tex=0.05)
            L.rect(x, ytop + alto - 60, ancho, 60, 0.26, tex=0.05)
            L.rect(x + 14, ytop + alto - 120, ancho * 0.5, 22, 0.30, tex=0.05)
            L.rect(x + 14, ytop + alto - 140, ancho * 0.5, 22, 0.44, tex=0.1)
            if rng.uniform() < 0.6:                                                    # monitor apagado en el suelo
                L.rect(x + ancho * 0.62, ytop + alto - 100, 60, 44, 0.12, tex=0.05)
            # la reja, abierta de par en par (dos hojas pegadas a los lados)
            L.rect(x, ytop, 16, alto, 0.12, tex=0.05)
            L.rect(x + ancho - 16, ytop, 16, alto, 0.12, tex=0.05)
        barandilla(L, -1200, 3000, ytop + alto + 34, alto=90, sep=26, tono=0.18)
        L.rect(-1200, ytop + alto, 4200, 40, 0.22, tex=0.06)
    # ventanales del fondo con la luz del amanecer
    for k in range(4):
        L.rect(-300 + k * 700, -1250, 300, 360, 0.80, tex=0.0, emis=0.7)
    suelo(L, -1200, 3000, 1000, 1400, "baldosa", 0.22, sem=784, vp=(960, -200))
    return L.capa(opaco=True)
