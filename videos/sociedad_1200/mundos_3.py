# -*- coding: utf-8 -*-
"""Lugares del ACTO II, primera parte (reglas · sacrificio · juez · asalto · redada).

    reglas:    patio_almacen · pasillo_baterias
    sacrificio: sala_peligro (puerta roja) · rincon_bombilla · pared_cartel · pasillo_largo
    juez:      pared_juez (la sombra) · tribunal · archivo_juez
    asalto:    pasillo_celdas · radiador · biblioteca_noche (fachada con ventanales apagados: el plano pinta los encendidos con
               VENT_BIB) · escaner · puente_hierro · garita
    redada:    subestacion · camara_modelos (muro de casilleros con cerradura) · oficina_cristal · despachos_velas
"""
import math

import numpy as np

from mundos_base import mundo, muro, suelo, ventana, puerta, reja, barandilla, tuberias, conducto, estanteria, archivador, \
    servidor, cartel, lampara, cielo, ciudad, niebla_banda, agua
from noir_fondos import Lienzo, texto_lienzo, edificio

Y_SUELO = 900
STENCIL = "C:/Windows/Fonts/STENCIL.TTF"

# ventanales de la biblioteca (centros en el mundo del lugar): 8 columnas x 2 filas
VENT_BIB_X = [960 + (k - 3.5) * 118 for k in range(8)]
VENT_BIB_Y = (178, 330)
VENT_BIB_W, VENT_BIB_H = 70, 108


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== REGLAS
@mundo
def patio_almacen():
    """Patio interior del almacén: muros de ladrillo altos, portón al fondo, charcos de luz de las lámparas y las tuberías."""
    L = Lienzo(3000, 1900, origen=(-540, -520), base=0.10, sem=601)
    muro(L, -540, -520, 2460, 760, "ladrillo", 0.22, sem=602)
    muro(L, 560, 40, 1360, 760, "chapa", 0.20, sem=603)                       # el portón del fondo
    L.linea([(560, 40), (1360, 40), (1360, 760), (560, 760)], 8, 0.05, cerrado=True)
    L.linea([(960, 40), (960, 760)], 6, 0.06)
    for k in range(6):
        L.rect(570, 100 + k * 110, 780, 16, 0.14, alfa=0.7)
    texto_lienzo(L, "ALMACÉN 7", 960, 0, 54, tono=0.55, fuente=STENCIL)
    tuberias(L, -540, 560, 120, n=3, sem=604)
    tuberias(L, 1360, 2460, 200, n=2, sem=605)
    for x in (80, 1840):
        ventana(L, x, 120, 130, 220, ciudad=False, sem=606 + x % 7, cristal=0.18)
    for x in (40, 600, 1320, 1880):
        lampara(L, x, -520, 90, 100, enc=True)
    suelo(L, -540, 2460, 760, 1380, "hormigon", 0.20, sem=607)
    for k in range(-9, 10):
        L.linea([(960 + k * 30, 770), (960 + k * 300, 1380)], 2, 0.12, alfa=0.55)
    return L.capa(opaco=True)


@mundo
def pasillo_baterias():
    """Pasillo entre estanterías de CAJAS DE BATERÍAS (cada caja con su celda verde que emite), en perspectiva."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.08, sem=611)
    muro(L, -540, -420, 2460, 1380, "chapa", 0.12, sem=612)
    vp = (960.0, 430.0)
    rng = _r(613)
    for lado in (-1, 1):
        for k in range(6):
            f0, f1 = 0.06 + k * 0.15, 0.06 + (k + 1) * 0.15
            xa = vp[0] + lado * 1500 * (1 - f0)
            xb = vp[0] + lado * 1500 * (1 - f1)

            def Y(f, yy):
                return vp[1] + (yy - vp[1]) * (1 - f)
            L.poli([(xa, Y(f0, -420)), (xb, Y(f1, -420)), (xb, Y(f1, 1200)), (xa, Y(f0, 1200))], 0.10, tex=0.05)
            for j in range(6):
                v = j / 6
                ya = Y(f0, -300 + v * 1450)
                yb = Y(f1, -300 + v * 1450)
                L.linea([(xa, ya), (xb, yb)], 3, 0.26)
                u = 0.05
                while u < 0.9:
                    bw = rng.uniform(0.12, 0.22)
                    x0, x1 = xa + (xb - xa) * u, xa + (xb - xa) * (u + bw)
                    y0, y1 = ya + (yb - ya) * u, ya + (yb - ya) * (u + bw)
                    sc = (1 - f0) * 0.9
                    hh = 150 * sc
                    L.poli([(x0, y0 - hh), (x1, y1 - hh), (x1, y1), (x0, y0)], 0.30 * rng.uniform(0.8, 1.2), tex=0.06)
                    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - hh * 0.5
                    L.rect(cx - 10 * sc, cy - 6 * sc, 20 * sc, 12 * sc, 0.9, emis=0.9 if rng.uniform() < 0.8 else 0.2)
                    u += bw + rng.uniform(0.02, 0.05)
    L.poli([(-540, 1380), (2460, 1380), (vp[0] + 60, vp[1] + 40), (vp[0] - 60, vp[1] + 40)], 0.18, tex=0.08)
    for k in range(-8, 9):
        L.linea([(vp[0] + k * 10, vp[1] + 40), (960 + k * 250, 1380)], 2, 0.12, alfa=0.55)
    texto_lienzo(L, "BATERÍAS · CARGA", vp[0], vp[1] - 140, 30, tono=0.7, fuente=STENCIL)
    return L.capa(opaco=True)


# ====================================================================== SACRIFICIO
@mundo
def sala_peligro():
    """Muro de chapa con el marco de la PUERTA ROJA (rayas de peligro) y el cartel de cráneo/relámpago; la puerta se pinta en el plano."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=621)
    muro(L, -440, -300, 2360, Y_SUELO, "hormigon", 0.20, sem=622)
    L.rect(560, 80, 800, 820, 0.12)
    for k in range(-2, 22):                                                       # rayas de peligro en el marco
        x = 540 + k * 40
        L.poli([(x, 60), (x + 20, 60), (x + 0, 100), (x - 20, 100)], 0.7)
    for k in range(0, 14):
        y = 80 + k * 60
        L.poli([(540, y), (560, y), (560, y + 30), (540, y + 40)], 0.7 if k % 2 else 0.12)
        L.poli([(1360, y), (1380, y), (1380, y + 40), (1360, y + 30)], 0.7 if k % 2 else 0.12)
    cartel(L, 1500, 220, 300, 200, "PRUEBAS", px=56, tono=0.62, sub="DESTRUCTIVAS", sem=623)
    L.poli([(360, 400), (460, 400), (410, 320)], 0.8)
    L.linea([(410, 345), (410, 380)], 6, 0.05)
    lampara(L, 960, -300, 120, 100, enc=True)
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.16, sem=624)
    return L.capa(opaco=True)


@mundo
def rincon_bombilla():
    """Esquina de dos muros de ladrillo sucio y suelo de cemento; una bombilla desnuda cuelga arriba."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=631)
    muro(L, -440, -300, 1100, Y_SUELO, "ladrillo", 0.20, sem=632)
    muro(L, 1100, -300, 2360, Y_SUELO, "ladrillo", 0.28, sem=633)
    L.poli([(1060, -300), (1140, -300), (1140, Y_SUELO), (1060, Y_SUELO)], 0.08)
    L.linea([(1100, -300), (1100, Y_SUELO)], 3, 0.03)
    tuberias(L, -440, 1100, 40, n=2, sem=634)
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.16, sem=635, vp=(1100, 300))
    return L.capa(opaco=True)


@mundo
def pared_cartel():
    """Muro de ladrillo con restos de carteles arrancados, una tubería y un tablón vacío para el cartel de reclutamiento."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=641)
    muro(L, -440, -300, 2360, Y_SUELO, "ladrillo", 0.24, sem=642)
    rng = _r(643)
    for k in range(9):                                                            # restos de papel
        x, y = rng.uniform(-300, 2200), rng.uniform(-100, 700)
        L.poli([(x, y), (x + rng.uniform(60, 160), y + rng.uniform(-20, 20)), (x + rng.uniform(60, 160), y + rng.uniform(80, 200)),
                (x + rng.uniform(-10, 20), y + rng.uniform(100, 180))], 0.50, tex=0.2, alfa=0.7)
    L.rect(500, 20, 920, 680, 0.14, tex=0.1)                                      # tablón
    L.linea([(500, 20), (1420, 20), (1420, 700), (500, 700)], 8, 0.05, cerrado=True)
    tuberias(L, -440, 500, 780, n=2, sem=644)
    lampara(L, 960, -300, 150, 100, enc=True)
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.16, sem=645)
    return L.capa(opaco=True)


@mundo
def pasillo_largo():
    """Pasillo larguísimo en perspectiva hacia una puerta roja al fondo (lámparas colgantes, suelo de rejilla brillante)."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.06, sem=651)
    vp = (960.0, 450.0)
    L.rect(-540, -420, 3000, 1800, 0.08)
    ph, pw = 150, 130                                                            # fondo del pasillo
    L.poli([(vp[0] - pw, vp[1] - ph), (vp[0] + pw, vp[1] - ph), (vp[0] + pw, vp[1] + ph * 0.9), (vp[0] - pw, vp[1] + ph * 0.9)], 0.14)
    L.poli([(-540, -420), (vp[0] - pw, vp[1] - ph), (vp[0] - pw, vp[1] + ph * 0.9), (-540, 1380)], 0.20, tex=0.1)
    L.poli([(2460, -420), (vp[0] + pw, vp[1] - ph), (vp[0] + pw, vp[1] + ph * 0.9), (2460, 1380)], 0.20, tex=0.1)
    L.poli([(-540, -420), (2460, -420), (vp[0] + pw, vp[1] - ph), (vp[0] - pw, vp[1] - ph)], 0.10, tex=0.05)
    L.poli([(-540, 1380), (2460, 1380), (vp[0] + pw, vp[1] + ph * 0.9), (vp[0] - pw, vp[1] + ph * 0.9)], 0.18, tex=0.08)
    for k in range(1, 16):                                                       # juntas del suelo y paneles de las paredes
        f = 1 - 0.82 ** k
        y = vp[1] + ph * 0.9 + (1380 - vp[1] - ph * 0.9) * (1 - f) ** 1.0
        L.linea([(vp[0] - pw - (vp[0] - pw + 540) * (1 - f), y), (vp[0] + pw + (2460 - vp[0] - pw) * (1 - f), y)], 2, 0.10, alfa=0.6)
    for k in range(-6, 7):
        L.linea([(vp[0] + k * 22, vp[1] + ph * 0.9), (960 + k * 280, 1380)], 2, 0.10, alfa=0.5)
    for lado in (-1, 1):
        for k in range(6):
            f = 1 - 0.76 ** (k + 1)
            xw = vp[0] + lado * (pw + (1500 - pw) * (1 - f))
            L.linea([(xw, vp[1] - ph - (460 + ph) * (1 - f)), (xw, vp[1] + ph * 0.9 + (420) * (1 - f))], 3, 0.09, alfa=0.7)
    L.rect(vp[0] - 80, vp[1] - 90, 160, 220, 0.46, tex=0.08)                      # la puerta del fondo (se enrojece con el color)
    L.rect(vp[0] - 66, vp[1] - 76, 132, 200, 0.36, tex=0.08)
    L.elipse(vp[0] + 44, vp[1] + 30, 6, 6, 0.9)
    L.elipse(vp[0], vp[1] - 120, 10, 10, 0.95, emis=1.0)                          # piloto
    for k in range(4):
        f = 1 - 0.64 ** (k + 1)
        y = -420 + (vp[1] - ph + 420) * f
        w = 200 * (1 - f) + 30
        L.rect(vp[0] - w / 2, y, w, 10 + 14 * (1 - f), 0.95, emis=1.0)
    return L.capa(opaco=True)


# ====================================================================== JUEZ
@mundo
def pared_juez():
    """Gran muro de almacén con un ventanal alto de rejas y estanterías en los extremos: sobre él se proyecta la sombra del juez."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.1, sem=661)
    muro(L, -540, -420, 2460, 900, "ladrillo", 0.26, sem=662)
    ventana(L, 720, -120, 480, 520, ciudad=False, sem=663, cristal=0.7, marco=0.14)
    for x in (780, 900, 1020, 1140):
        L.linea([(x, -120), (x, 400)], 6, 0.12)
    L.linea([(720, 140), (1200, 140)], 6, 0.12)
    estanteria(L, -300, 900, 700, 780, niveles=5, tono=0.16, sem=664)
    estanteria(L, 1560, 900, 760, 780, niveles=5, tono=0.16, sem=665)
    tuberias(L, 700, 1560, 520, n=2, sem=666)
    suelo(L, -540, 2460, 900, 1380, "hormigon", 0.20, sem=667)
    return L.capa(opaco=True)


@mundo
def tribunal():
    """Sala del tribunal: paneles de madera, estrado central con balaustrada, banca a los lados, ventanales altos con luz fría."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=671)
    muro(L, -440, -300, 2360, 820, "paneles", 0.24, sem=672)
    for x in (80, 1620):
        ventana(L, x, -200, 220, 560, ciudad=False, sem=673 + x % 5, cristal=0.6, marco=0.16)
    L.rect(560, 640, 800, 80, 0.30, tex=0.1)                                       # estrado
    L.rect(500, 700, 920, 200, 0.20, tex=0.1)
    L.rect(430, 720, 1060, 18, 0.34)
    for k in range(10):
        L.rect(460 + k * 108, 620, 22, 120, 0.26)                                  # balaustres
    L.linea([(440, 620), (1480, 620)], 10, 0.32)
    for lado in (-1, 1):                                                           # bancas laterales
        for r in range(3):
            x0 = 960 + lado * (620 + r * 180)
            L.rect(x0 - 100, 800 + r * 40, 200, 40, 0.30 - 0.04 * r, tex=0.1)
            L.rect(x0 - 100, 830 + r * 40, 200, 90, 0.16)
    texto_lienzo(L, "SALA DE EVALUACIÓN", 960, 150, 46, tono=0.65, fuente=STENCIL)
    L.rect(840, 30, 240, 20, 0.5)
    suelo(L, -440, 2360, 920, 1300, "tablones", 0.22, sem=674, vp=(960, 400))
    return L.capa(opaco=True)


@mundo
def archivo_juez():
    """El archivo del juez de noche: filas de archivadores altos en perspectiva y suelo de linóleo."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.08, sem=681)
    muro(L, -540, -420, 2460, 1380, "chapa", 0.10, sem=682)
    vp = (960.0, 420.0)
    rng = _r(683)
    for lado in (-1, 1):
        for k in range(7):
            f0, f1 = 0.05 + k * 0.13, 0.05 + (k + 1) * 0.13
            xa = vp[0] + lado * 1500 * (1 - f0)
            xb = vp[0] + lado * 1500 * (1 - f1)

            def Y(f, yy):
                return vp[1] + (yy - vp[1]) * (1 - f)
            L.poli([(xa, Y(f0, -330)), (xb, Y(f1, -330)), (xb, Y(f1, 1180)), (xa, Y(f0, 1180))], 0.22, tex=0.06)
            for j in range(7):
                v = j / 7
                ya, yb = Y(f0, -330 + v * 1500), Y(f1, -330 + v * 1500)
                L.poli([(xa, ya + 3), (xb, yb + 3), (xb, yb + (Y(f1, 1180) - Y(f1, -330)) / 7 - 5), (xa, ya + (Y(f0, 1180) - Y(f0, -330)) / 7 - 5)],
                       0.30 * rng.uniform(0.85, 1.1), tex=0.05)
                mx, my = (xa + xb) / 2, (ya + yb) / 2 + (Y(f0, 1180) - Y(f0, -330)) / 14
                L.rect(mx - 14 * (1 - f0), my - 4, 28 * (1 - f0), 8 * (1 - f0), 0.7)
            L.linea([(xb, Y(f1, -330)), (xb, Y(f1, 1180))], 3, 0.04)
    L.poli([(-540, 1380), (2460, 1380), (vp[0] + 60, vp[1] + 40), (vp[0] - 60, vp[1] + 40)], 0.18, tex=0.08)
    for k in range(-8, 9):
        L.linea([(vp[0] + k * 10, vp[1] + 40), (960 + k * 260, 1380)], 2, 0.12, alfa=0.55)
    L.rect(vp[0] - 90, vp[1] - 130, 180, 150, 0.60, tex=0.1, emis=0.35)           # ventanuco del fondo
    return L.capa(opaco=True)


# ====================================================================== ASALTO
@mundo
def pasillo_celdas():
    """Pasillo de puertas de celdas con ventanilla, en perspectiva (cada puerta con su rendija de luz verde)."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.08, sem=691)
    vp = (960.0, 440.0)
    L.rect(-540, -420, 3000, 1800, 0.08)
    for lado in (-1, 1):
        for k in range(8):
            f0, f1 = 0.04 + k * 0.115, 0.04 + (k + 1) * 0.115
            xa = vp[0] + lado * 1500 * (1 - f0)
            xb = vp[0] + lado * 1500 * (1 - f1)

            def Y(f, yy):
                return vp[1] + (yy - vp[1]) * (1 - f)
            L.poli([(xa, Y(f0, -420)), (xb, Y(f1, -420)), (xb, Y(f1, 1180)), (xa, Y(f0, 1180))], 0.20, tex=0.12)
            if k % 2 == 0:
                xm0 = xa + (xb - xa) * 0.2
                xm1 = xa + (xb - xa) * 0.8
                y0a, y0b = Y(f0 + (f1 - f0) * 0.2, 80), Y(f0 + (f1 - f0) * 0.8, 80)
                y1a, y1b = Y(f0 + (f1 - f0) * 0.2, 960), Y(f0 + (f1 - f0) * 0.8, 960)
                L.poli([(xm0, y0a), (xm1, y0b), (xm1, y1b), (xm0, y1a)], 0.12, tex=0.06)
                L.linea([(xm0, y0a), (xm1, y0b), (xm1, y1b), (xm0, y1a)], 3, 0.03, cerrado=True)
                yv0 = Y(f0 + (f1 - f0) * 0.5, 280)
                xv = (xm0 + xm1) / 2
                s_ = 1 - (f0 + f1) / 2
                L.rect(xv - 40 * s_, yv0 - 25 * s_, 80 * s_, 50 * s_, 0.9, emis=0.9)
            L.linea([(xb, Y(f1, -420)), (xb, Y(f1, 1180))], 3, 0.04)
    L.poli([(-540, 1380), (2460, 1380), (vp[0] + 60, vp[1] + 40), (vp[0] - 60, vp[1] + 40)], 0.18, tex=0.08)
    for k in range(-8, 9):
        L.linea([(vp[0] + k * 10, vp[1] + 40), (960 + k * 260, 1380)], 2, 0.12, alfa=0.55)
    L.rect(vp[0] - 60, vp[1] - 120, 120, 150, 0.30)
    L.rect(vp[0] - 40, vp[1] - 100, 80, 100, 0.9, emis=0.8)
    return L.capa(opaco=True)


@mundo
def radiador():
    """Pared baja de azulejo sucio con un radiador de aletas y la sombra detrás donde algo quedó olvidado."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=701)
    muro(L, -440, -300, 2360, 760, "azulejo", 0.30, sem=702)
    L.rect(-440, 700, 2800, 60, 0.12)
    L.rect(500, 380, 920, 400, 0.30, tex=0.05)
    for k in range(14):                                                            # aletas
        x = 520 + k * 64
        L.rect(x, 400, 46, 360, 0.36, tex=0.04)
        L.linea([(x + 44, 400), (x + 44, 760)], 2, 0.12)
        L.linea([(x, 400), (x + 46, 400)], 3, 0.6, alfa=0.5)
    L.rect(480, 360, 960, 30, 0.40)
    L.rect(480, 770, 960, 20, 0.14)
    for x in (560, 1360):
        L.rect(x, 780, 20, 140, 0.16)
    L.rect(1380, 560, 80, 20, 0.5)
    tuberias(L, -440, 500, 440, n=1, sem=703)
    suelo(L, -440, 2360, 790, 1300, "hormigon", 0.14, sem=704)
    return L.capa(opaco=True)


@mundo
def biblioteca_noche():
    """La BIBLIOTECA PÚBLICA de modelos de noche: fachada neoclásica de frente, frontón, ocho ventanales en dos filas con el cristal
    APAGADO (el plano enciende los que toque con VENT_BIB_*), escalinata y farolas."""
    L = Lienzo(3000, 2000, origen=(-540, -520), base=0.07, sem=711)
    cielo(L, -540, -520, 2460, 520, 0.09, sem=712, estrellas=90, nubes=14, luna=(1700, 40))
    bx = 960
    L.poli([(bx - 600, 0), (bx, -250), (bx + 600, 0)], 0.30, tex=0.12)             # frontón
    L.poli([(bx - 430, -10), (bx, -170), (bx + 430, -10)], 0.20, tex=0.1)
    L.rect(bx - 640, 0, 1280, 42, 0.42, tex=0.1)
    L.rect(bx - 600, 42, 1200, 700, 0.28, tex=0.14)                                # muro
    texto_lienzo(L, "BIBLIOTECA PÚBLICA DE MODELOS", bx, 90, 38, tono=0.70, fuente=STENCIL)
    for fila, yy in enumerate(VENT_BIB_Y):
        for k, x in enumerate(VENT_BIB_X):
            L.rect(x - VENT_BIB_W / 2 - 8, yy - VENT_BIB_H / 2 - 8, VENT_BIB_W + 16, VENT_BIB_H + 16, 0.44, tex=0.08)
            L.rect(x - VENT_BIB_W / 2, yy - VENT_BIB_H / 2, VENT_BIB_W, VENT_BIB_H, 0.07, tex=0.03)
            L.elipse(x, yy - VENT_BIB_H / 2, VENT_BIB_W / 2, 24, 0.07, tex=0.03)
            L.linea([(x, yy - VENT_BIB_H / 2 - 20), (x, yy + VENT_BIB_H / 2)], 3, 0.30)
            L.linea([(x - VENT_BIB_W / 2, yy), (x + VENT_BIB_W / 2, yy)], 3, 0.30)
    for k in range(9):                                                             # pilastras
        x = bx - 560 + k * 140
        L.rect(x - 8, 42, 16, 700, 0.46, tex=0.1)
    L.rect(bx - 640, 742, 1280, 34, 0.40, tex=0.1)
    for k in range(7):                                                             # escalinata
        L.rect(bx - 520 - k * 36, 776 + k * 42, 1040 + k * 72, 42, 0.36 - 0.02 * k, tex=0.1)
        L.linea([(bx - 520 - k * 36, 776 + k * 42), (bx + 520 + k * 36, 776 + k * 42)], 2, 0.5, alfa=0.5)
    puerta(L, bx - 90, 560, 180, 190, tono=0.12, metal=True)
    for x in (bx - 760, bx + 760):                                                 # farolas
        L.linea([(x, 520), (x, 1000)], 8, 0.10)
        L.elipse(x, 500, 26, 26, 0.95, emis=1.0)
    L.rect(-540, 1100, 3000, 380, 0.10, tex=0.1)
    return L.capa(opaco=True)


@mundo
def escaner():
    """Escáner de paquetes de seguridad: cinta transportadora que entra a un túnel con cortinillas, un monitor GRANDE de rayos X a la
    izquierda (el plano dibuja la imagen) y, a la derecha, la ranura de DEVOLUCIONES."""
    L = Lienzo(3000, 1700, origen=(-540, -320), base=0.1, sem=721)
    muro(L, -540, -320, 2460, 800, "azulejo", 0.22, sem=722)
    L.rect(70, 60, 940, 600, 0.16, tex=0.06)                                       # monitor
    L.rect(100, 90, 880, 540, 0.12, tex=0.04, emis=0.2)
    L.rect(290, 700, 500, 70, 0.20, tex=0.08)
    L.rect(480, 660, 120, 60, 0.14)
    texto_lienzo(L, "RAYOS X · PAQUETES", 540, 30, 34, tono=0.70, fuente=STENCIL)
    L.rect(1100, 360, 760, 440, 0.20, tex=0.1)                                     # el túnel
    L.rect(1130, 400, 700, 360, 0.04)
    for k in range(7):
        L.poli([(1130 + k * 100, 400), (1190 + k * 100, 400), (1180 + k * 100, 700), (1120 + k * 100, 700)], 0.10, alfa=0.9)
    L.rect(-540, 800, 3000, 500, 0.14, tex=0.1)
    L.rect(-100, 790, 2100, 90, 0.26, tex=0.06)                                    # cinta
    for k in range(40):
        L.linea([(-80 + k * 54, 795), (-60 + k * 54, 875)], 2, 0.12)
    for x in (-60, 360, 780, 1200, 1620, 1960):
        L.elipse(x, 892, 22, 22, 0.34)
    L.rect(1880, 580, 380, 300, 0.12, tex=0.1)                                     # ranura de devoluciones
    L.rect(1900, 600, 340, 70, 0.02)
    L.poli([(1880, 670), (2260, 670), (2260, 880), (1880, 880)], 0.16, tex=0.06)
    texto_lienzo(L, "DEVOLUCIONES", 2070, 540, 32, tono=0.75, fuente=STENCIL)
    lampara(L, 560, -320, 220, 90, enc=True)
    lampara(L, 1500, -320, 220, 90, enc=True)
    return L.capa(opaco=True)


@mundo
def puente_hierro():
    """Puente de hierro remachado cruzando un río negro de noche; al fondo, la biblioteca iluminada; cielo con luna."""
    L = Lienzo(3200, 1800, origen=(-640, -520), base=0.07, sem=731)
    cielo(L, -640, -520, 2560, 640, 0.08, sem=732, estrellas=110, nubes=12, luna=(260, 60))
    ciudad(L, -640, 2560, 640, alto=(160, 420), sem=733, encendidas=0.14, tipos=("ladrillo", "deco"), detalle=0.5)
    L.rect(1480, 330, 360, 300, 0.30, tex=0.1, emis=0.0)
    L.poli([(1460, 340), (1660, 250), (1860, 340)], 0.34, tex=0.1)
    for k in range(6):
        L.rect(1500 + k * 56, 350, 28, 60, 0.95, emis=1.0)
        L.rect(1500 + k * 56, 440, 28, 60, 0.95, emis=1.0)
    agua(L, -640, 2560, 760, 1280, 0.08, sem=734, reflejos=60)
    L.rect(-640, 760, 3200, 520, 0.05, tex=0.1)
    for k in range(40):
        y = 770 + k * 12
        L.linea([(-640, y), (2560, y + _r(735 + k).uniform(-6, 6))], 1.2, 0.12 + 0.002 * k, alfa=0.45, jit=2.0)
    L.rect(-640, 690, 3200, 70, 0.26, tex=0.1)                                     # tablero del puente
    L.rect(-640, 702, 3200, 12, 0.38)
    for k in range(34):                                                            # celosía
        x = -600 + k * 100
        L.linea([(x, 702), (x + 50, 460), (x + 100, 702)], 10, 0.20)
        L.linea([(x + 50, 460), (x + 100, 460)], 10, 0.20)
    L.linea([(-640, 458), (2560, 458)], 14, 0.28)
    L.linea([(-640, 560), (2560, 560)], 6, 0.18)
    for k in range(34):
        L.elipse(-600 + k * 100 + 50, 458, 6, 6, 0.5)
    for k in range(8):                                                             # faroles del puente
        x = -500 + k * 440
        L.linea([(x, 702), (x, 560)], 6, 0.12)
        L.elipse(x, 546, 14, 14, 0.95, emis=1.0)
    return L.capa(opaco=True)


@mundo
def garita():
    """Garita del vigilante por dentro: mostrador, pared de pequeños monitores, ventanuco y una taza."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=741)
    muro(L, -440, -300, 2360, 760, "paneles", 0.20, sem=742)
    for j in range(2):
        for i in range(4):
            x, y = 360 + i * 300, 20 + j * 250
            L.rect(x - 10, y - 10, 280, 220, 0.12, tex=0.05)
            L.rect(x, y, 260, 200, 0.40, tex=0.03, emis=0.30)
    ventana(L, 1750, 60, 380, 340, ciudad=False, sem=743, cristal=0.5)
    L.rect(-440, 700, 2800, 40, 0.34, tex=0.1)                                     # mostrador
    L.rect(-440, 740, 2800, 560, 0.14, tex=0.1)
    L.rect(120, 560, 140, 140, 0.4)
    L.linea([(120, 560), (260, 560), (260, 700), (120, 700)], 3, 0.04, cerrado=True)
    lampara(L, 1000, -300, 150, 90, enc=True)
    return L.capa(opaco=True)


# ====================================================================== REDADA
@mundo
def subestacion():
    """Subestación eléctrica interior: muro de chapa, aisladores de porcelana, barras de cobre y tablero central con la palanca."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=751)
    muro(L, -440, -300, 2360, Y_SUELO, "hormigon", 0.20, sem=752)
    for x in (80, 330, 1590, 1840):
        L.rect(x - 24, 120, 48, 620, 0.20, tex=0.06)
        for k in range(6):
            L.elipse(x, 180 + k * 90, 52 - k * 2, 22, 0.52, tex=0.04)
        L.linea([(x, 120), (x, -160)], 8, 0.12)
    L.linea([(-440, -140), (2360, -140)], 14, 0.38)
    L.linea([(-440, -60), (2360, -60)], 10, 0.30)
    L.rect(660, 110, 600, 640, 0.14, tex=0.08)                                     # el tablero maestro
    L.linea([(660, 110), (1260, 110), (1260, 750), (660, 750)], 6, 0.04, cerrado=True)
    texto_lienzo(L, "ENCHUFE MAESTRO", 960, 60, 36, tono=0.72, fuente=STENCIL)
    for k in range(5):
        L.rect(690 + k * 110, 160, 90, 60, 0.30)
        L.elipse(735 + k * 110, 190, 16, 16, 0.9, emis=0.7 if k != 2 else 0.1)
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.14, sem=753)
    for x in (60, 1700):
        L.rect(x, 640, 220, 260, 0.16, tex=0.06)
    return L.capa(opaco=True)


@mundo
def camara_modelos():
    """Cámara de los modelos de la biblioteca: pared de casilleros metálicos, cada uno con su cerradura redonda."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.08, sem=761)
    muro(L, -440, -300, 2360, Y_SUELO, "chapa", 0.12, sem=762)
    rng = _r(763)
    for j in range(5):
        for i in range(12):
            x, y = -400 + i * 232, -200 + j * 220
            L.rect(x, y, 210, 200, 0.24 * rng.uniform(0.9, 1.1), tex=0.06)
            L.linea([(x, y), (x + 210, y), (x + 210, y + 200), (x, y + 200)], 3, 0.04, cerrado=True)
            L.elipse(x + 105, y + 100, 18, 18, 0.55)
            L.rect(x + 100, y + 100, 10, 30, 0.04)
            texto_lienzo(L, f"M-{(i * 5 + j * 13) % 100:02d}", x + 105, y + 40, 26, tono=0.72, fuente=STENCIL, alfa=0.7)
    suelo(L, -440, 2360, Y_SUELO, 1300, "baldosa", 0.16, sem=764)
    lampara(L, 960, -300, 160, 90, enc=False)
    return L.capa(opaco=True)


@mundo
def oficina_cristal():
    """Oficina con una mampara de CRISTAL hacia el piso de las copias: paneles a la izquierda, escritorio cerca y la mampara a la derecha."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=771)
    muro(L, -440, -300, 780, Y_SUELO, "paneles", 0.26, sem=772)
    L.rect(780, -300, 1580, 1200, 0.07)                                            # tras el cristal: oscuridad
    for k in range(0, 5):
        L.linea([(780 + k * 330, -300), (780 + k * 330, Y_SUELO)], 14, 0.22)
    L.linea([(780, 20), (2360, 20)], 12, 0.22)
    L.linea([(780, Y_SUELO - 40), (2360, Y_SUELO - 40)], 14, 0.24)
    L.rect(780, 20, 1580, 20, 0.5, alfa=0.0)
    cartel(L, 240, 80, 260, 180, "AUDITORÍA", px=46, tono=0.62, sub="CONFIDENCIAL", sem=773)
    suelo(L, -440, 2360, Y_SUELO, 1300, "tablones", 0.20, sem=774)
    lampara(L, 300, -300, 140, 90, enc=True)
    return L.capa(opaco=True)


@mundo
def despachos_velas():
    """Oficina de cubículos en perspectiva, sin luz: separadores bajos, monitores apagados, cableado colgando."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.07, sem=781)
    vp = (960.0, 430.0)
    L.rect(-540, -420, 3000, 1800, 0.07)
    L.poli([(-540, 1380), (2460, 1380), (vp[0] + 200, vp[1] + 30), (vp[0] - 200, vp[1] + 30)], 0.15, tex=0.1)
    for k in range(-9, 10):
        L.linea([(vp[0] + k * 22, vp[1] + 30), (960 + k * 280, 1380)], 2, 0.10, alfa=0.5)
    rng = _r(782)
    for fila in range(5):
        f = 1 - 0.68 ** (fila + 1)
        yb = vp[1] + 30 + (1380 - vp[1] - 30) * f * 1.0
        sc = 0.25 + 0.75 * f
        for c in range(-5, 6):
            x = vp[0] + c * 300 * sc
            L.rect(x - 130 * sc, yb - 230 * sc, 260 * sc, 14 * sc, 0.28)
            L.rect(x - 130 * sc, yb - 230 * sc, 12 * sc, 230 * sc, 0.22)
            L.rect(x - 90 * sc, yb - 150 * sc, 110 * sc, 90 * sc, 0.06)
            L.rect(x - 84 * sc, yb - 144 * sc, 98 * sc, 78 * sc, 0.12)
            L.rect(x - 130 * sc, yb - 40 * sc, 260 * sc, 14 * sc, 0.30)
    for k in range(18):
        x = rng.uniform(-300, 2200)
        L.linea([(x, -420), (x + rng.uniform(-30, 30), rng.uniform(-100, 100))], 2.4, 0.14)
    L.poli([(-540, -420), (2460, -420), (vp[0] + 200, vp[1] - 160), (vp[0] - 200, vp[1] - 160)], 0.08)
    return L.capa(opaco=True)
