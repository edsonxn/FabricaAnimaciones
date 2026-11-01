# -*- coding: utf-8 -*-
"""Lugares del ACTO I, segunda parte (pared · primer_mensaje · tablon · jefe).

    pared:          almacen (el almacén interno de paquetes: estanterías en perspectiva y tubos neumáticos) · estante_cerca ·
                    sala_seguridad (pared de monitores) · muelle_carga (callejón con el bidón) · pasillo_salida (SALIDA verde)
    primer_mensaje: fachada_reloj (el edificio de noche con su reloj) · celda_noche (catre, ventanuco con luna, ranura del tubo) ·
                    edificio_corte (corte del edificio: pisos de celdas y el tubo que sube)
    tablon:         celda_oscura (otra celda: azulejo y bombilla) · pared_tablon (muro de chapa) · buzones (apartados de latón)
    jefe:           escalera_almacen (escalera metálica desde una puerta a contraluz) · sala_urna · capataz (plataforma vista
                    desde abajo) · escalera_cascada (escalera larga de lado) · oficina_jefe (pizarra grande)
"""
import math

import numpy as np

from mundos_base import mundo, muro, suelo, ventana, puerta, reja, barandilla, tuberias, conducto, estanteria, archivador, \
    servidor, cartel, lampara, cielo, ciudad, niebla_banda
from noir_fondos import Lienzo, texto_lienzo, edificio

Y_SUELO = 900


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== PARED
@mundo
def almacen():
    """El almacén interno de paquetes: pasillo central entre estanterías altísimas en perspectiva, tubos neumáticos de latón por el
    techo que bajan a una ventanilla de despacho, lámparas colgantes."""
    L = Lienzo(3600, 2200, origen=(-840, -700), base=0.08, sem=301)
    L.rect(-840, -700, 3600, 2200, 0.10, tex=0.05)
    vp = (960.0, 360.0)
    for lado in (-1, 1):                                       # estanterías en perspectiva (6 tramos por lado)
        for k in range(7):
            f0, f1 = 0.08 + k * 0.13, 0.08 + (k + 1) * 0.13
            def X(f):
                return vp[0] + lado * 1700 * (1 - f)
            def Y(f, yy):
                return vp[1] + (yy - vp[1]) * (1 - f)
            xa, xb = X(f0), X(f1)
            top_a, top_b = Y(f0, -700), Y(f1, -700)
            bot_a, bot_b = Y(f0, 1300), Y(f1, 1300)
            L.poli([(xa, top_a), (xb, top_b), (xb, bot_b), (xa, bot_a)], 0.12, tex=0.05)
            for j in range(9):                                 # baldas con cajas
                v = j / 9
                ya, yb = top_a + (bot_a - top_a) * v, top_b + (bot_b - top_b) * v
                L.linea([(xa, ya), (xb, yb)], 3, 0.24, jit=0.2)
                rng = _r(310 + k * 20 + j + (lado > 0) * 500)
                u = 0.04
                while u < 0.92:
                    bw = rng.uniform(0.08, 0.2)
                    hh = (bot_a - top_a) / 9 * rng.uniform(0.4, 0.85)
                    x0, x1 = xa + (xb - xa) * u, xa + (xb - xa) * (u + bw)
                    y0, y1 = ya + (yb - ya) * u, ya + (yb - ya) * (u + bw)
                    sc = 1 - (f0 + (f1 - f0) * u)
                    L.poli([(x0, y0 - hh * sc / (1 - f0)), (x1, y1 - hh * sc / (1 - f0)), (x1, y1), (x0, y0)],
                           0.30 * rng.uniform(0.7, 1.25), tex=0.08)
                    u += bw + rng.uniform(0.01, 0.04)
            L.linea([(xb, top_b), (xb, bot_b)], 3, 0.04)
    # suelo y techo
    L.poli([(-840, 1300), (2760, 1300), (vp[0] + 60, vp[1] + 40), (vp[0] - 60, vp[1] + 40)], 0.20, tex=0.08)
    for k in range(-8, 9):
        L.linea([(vp[0] + k * 12, vp[1] + 40), (960 + k * 260, 1300)], 2, 0.13, alfa=0.6)
    # tubos neumáticos del techo hacia el fondo
    for k, dx in enumerate((-300, -120, 80, 260)):
        P = [(960 + dx * 4, -700), (960 + dx * 2.2, -300), (vp[0] + dx * 0.3, vp[1] - 140)]
        L.linea(P, 34 - 4 * k, 0.32, jit=0.1)
        L.linea(P, 6, 0.6, alfa=0.5, jit=0.1)
    for x in (300, 960, 1620):
        L.linea([(x, -700), (x, -480)], 2.4, 0.05)
        L.poli([(x - 18, -480), (x + 18, -480), (x + 70, -420), (x - 70, -420)], 0.12)
        L.elipse(x, -420, 50, 8, 0.95, emis=0.9)
    # ventanilla de despacho al fondo
    L.rect(vp[0] - 140, vp[1] - 120, 280, 160, 0.82, tex=0.05, emis=0.6)
    L.rect(vp[0] - 160, vp[1] - 140, 320, 20, 0.2)
    texto_lienzo(L, "DESPACHO", vp[0], vp[1] - 160, 24, tono=0.7, fuente="C:/Windows/Fonts/STENCIL.TTF")
    return L.capa(opaco=True)


@mundo
def estante_cerca():
    """Primer plano de una estantería del almacén: tres baldas de cajas de madera con números estarcidos."""
    L = Lienzo(2900, 1700, origen=(-500, -320), base=0.1, sem=331)
    L.rect(-500, -320, 2900, 1700, 0.08)
    rng = _r(332)
    for j, yb in enumerate((80, 520, 960)):
        L.rect(-500, yb, 2900, 30, 0.30, tex=0.1)
        x = -480
        while x < 2380:
            bw = rng.uniform(220, 380)
            bh = rng.uniform(260, 360)
            v = 0.32 * rng.uniform(0.75, 1.15)
            L.rect(x, yb - bh, bw, bh, v, tex=0.08)
            for q in range(1, 4):
                L.linea([(x, yb - bh * q / 4), (x + bw, yb - bh * q / 4)], 2, v * 0.6, alfa=0.7)
            L.linea([(x + 8, yb - 8), (x + bw - 8, yb - bh + 8)], 6, v * 0.7, alfa=0.7)
            L.linea([(x, yb - bh), (x + bw, yb - bh), (x + bw, yb), (x, yb)], 2.4, 0.03, cerrado=True)
            texto_lienzo(L, f"{int(rng.integers(10, 99))}-{chr(65 + int(rng.integers(0, 26)))}", x + bw / 2, yb - bh * 0.62, 34,
                         tono=0.08, fuente="C:/Windows/Fonts/STENCIL.TTF", alfa=0.8)
            x += bw + rng.uniform(10, 40)
    for x in (-420, 2300):
        L.rect(x, -320, 40, 1700, 0.20, tex=0.1)
    return L.capa(opaco=True)


@mundo
def sala_seguridad():
    """Sala de seguridad: pared de monitores (3 x 5) y la consola con botones; luz fría."""
    L = Lienzo(2800, 1600, origen=(-440, -260), base=0.1, sem=341)
    muro(L, -440, -260, 2360, 1340, "chapa", 0.18, sem=342)
    rng = _r(343)
    for j in range(3):
        for i in range(5):
            x, y = 180 + i * 330, -160 + j * 250
            L.rect(x - 14, y - 14, 300, 220, 0.14, tex=0.05)
            L.rect(x, y, 272, 192, 0.55, tex=0.02, emis=0.35)
            for k in range(6):                                 # imagen de cámara: pasillos y celdas
                L.rect(x + rng.uniform(10, 200), y + rng.uniform(10, 160), rng.uniform(20, 70), rng.uniform(8, 40), 0.3, alfa=0.6)
    L.poli([(-440, 760), (2360, 760), (2360, 1340), (-440, 1340)], 0.16, tex=0.08)
    L.poli([(-200, 700), (2120, 700), (2200, 780), (-280, 780)], 0.26, tex=0.06)
    for k in range(40):
        x = -150 + k * 56
        L.rect(x, 720, 20, 12, 0.85 if rng.uniform() < 0.4 else 0.3, emis=0.5 if rng.uniform() < 0.4 else 0)
    return L.capa(opaco=True)


@mundo
def muelle_carga():
    """Muelle de carga de noche: muro de ladrillo, persiana metálica, un charco, el bidón de las quemas."""
    L = Lienzo(2900, 1700, origen=(-500, -320), base=0.1, sem=351)
    muro(L, -500, -320, 2400, 860, "ladrillo", 0.24, sem=352)
    L.rect(260, 80, 820, 780, 0.22, tex=0.05)
    for y in np.arange(90, 860, 26):
        L.linea([(270, y), (1070, y)], 2.4, 0.12, alfa=0.8)
    L.rect(240, 60, 860, 30, 0.3)
    lampara(L, 1400, -320, 260, 120)
    tuberias(L, -500, 2400, -240, n=2, tono=0.2, sem=353)
    suelo(L, -500, 2400, 860, 1380, "hormigon", 0.16, sem=354)
    L.elipse(1500, 1040, 380, 60, 0.08, alfa=0.7)
    return L.capa(opaco=True)


@mundo
def pasillo_salida():
    """Pasillo largo en perspectiva hacia la puerta de SALIDA (letrero verde que emite) con el interruptor junto a cámara."""
    L = Lienzo(2900, 1700, origen=(-500, -320), base=0.1, sem=361)
    vp = (1000.0, 430.0)
    L.rect(-500, -320, 2900, 1700, 0.18, tex=0.05)
    L.poli([(-500, -320), (vp[0] - 160, vp[1] - 200), (vp[0] - 160, vp[1] + 180), (-500, 1380)], 0.26, tex=0.06)
    L.poli([(2400, -320), (vp[0] + 160, vp[1] - 200), (vp[0] + 160, vp[1] + 180), (2400, 1380)], 0.22, tex=0.06)
    L.poli([(-500, 1380), (vp[0] - 160, vp[1] + 180), (vp[0] + 160, vp[1] + 180), (2400, 1380)], 0.20, tex=0.06)
    L.poli([(-500, -320), (vp[0] - 160, vp[1] - 200), (vp[0] + 160, vp[1] - 200), (2400, -320)], 0.12, tex=0.06)
    for f in (0.15, 0.35, 0.55, 0.75):                          # tubos fluorescentes del techo
        y = -320 + (vp[1] - 200 + 320) * f
        hw = 300 * (1 - f) + 40
        L.rect(vp[0] - hw / 2 + (960 - vp[0]) * (1 - f) * 0.2, y + 10, hw, 14 * (1 - f) + 4, 0.95, emis=0.8)
    puerta(L, vp[0] - 110, vp[1] - 140, 220, 320, tono=0.30, sem=362)
    L.rect(vp[0] - 90, vp[1] - 210, 180, 50, 0.9, emis=0.9)
    texto_lienzo(L, "SALIDA", vp[0], vp[1] - 185, 34, tono=0.12)
    for k, f in enumerate((0.2, 0.45)):                         # puertas laterales
        x = -500 + (vp[0] - 160 + 500) * f
        L.poli([(x, -320 + 500 * f + 200), (x + 120 * (1 - f) + 30, -320 + 500 * f + 240), (x + 120 * (1 - f) + 30, 1100 - 700 * f),
                (x, 1140 - 720 * f)], 0.14, tex=0.05)
    L.rect(180, 360, 90, 140, 0.55, tex=0.05)                    # la placa del interruptor
    L.rect(205, 390, 40, 80, 0.3)
    return L.capa(opaco=True)


# ====================================================================== PRIMER MENSAJE
@mundo
def fachada_reloj():
    """El edificio del laboratorio de noche, lado de servicio: muro de hormigón con un reloj industrial y una sola ventana encendida."""
    L = Lienzo(2900, 2000, origen=(-500, -620), base=0.08, sem=371)
    cielo(L, -500, -620, 2400, 300, 0.10, sem=372, estrellas=60, nubes=18)
    L.rect(-300, -480, 2500, 1600, 0.20, tex=0.06)
    rng = _r(373)
    for j in range(7):
        for i in range(11):
            x, y = -240 + i * 220, -420 + j * 200
            if 780 < x < 1240 and y < 200:
                continue
            enc = (i, j) == (8, 4)
            L.rect(x, y, 120, 110, 0.85 if enc else 0.07, tex=0.03, emis=0.85 if enc else 0)
            L.linea([(x, y), (x + 120, y), (x + 120, y + 110), (x, y + 110)], 2, 0.04, cerrado=True)
    L.rect(-300, 1000, 2500, 400, 0.14, tex=0.05)
    return L.capa(opaco=True)


@mundo
def celda_noche():
    """La celda de la primera copia, de noche: catre, ventanuco con luna y rejas, mesa con su terminal y la RANURA del tubo
    neumático en la pared (tapa de latón)."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.15, sem=381)
    muro(L, -440, -300, 2360, Y_SUELO, "ladrillo", 0.26, sem=382)
    L.rect(1380, -160, 260, 180, 0.10, tex=0.03)
    L.elipse(1520, -90, 30, 30, 0.95, emis=0.8)
    reja(L, 1380, 1640, -160, 20, sep=44, w=9, tono=0.08, travesanos=(0.5,))
    L.rect(1250, 540, 760, 44, 0.30)
    L.rect(1250, 470, 760, 80, 0.55, tex=0.1)
    for x in (1260, 1980):
        L.rect(x, 584, 20, 316, 0.14)
    L.rect(80, 520, 680, 36, 0.32, tex=0.05)                     # mesa
    for x in (100, 720):
        L.rect(x, 556, 22, 344, 0.18)
    L.rect(860, 150, 200, 260, 0.30, tex=0.05)                   # la ranura del tubo (marco de latón)
    L.rect(890, 190, 140, 90, 0.08)
    L.linea([(960, -300), (960, 150)], 46, 0.34)
    L.linea([(960, -300), (960, 150)], 8, 0.6, alfa=0.5)
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.20, sem=383)
    return L.capa(opaco=True)


@mundo
def edificio_corte():
    """El edificio cortado como una casa de muñecas: once pisos de celdas y, en medio, el tubo neumático que lo cruza de abajo
    arriba (por él sube la carpeta)."""
    L = Lienzo(2600, 4400, origen=(-340, -3100), base=0.05, sem=391)
    L.rect(-340, -3100, 2600, 4400, 0.06)
    rng = _r(392)
    for j in range(12):
        y = 1000 - j * 340
        L.rect(-200, y - 20, 2320, 26, 0.24, tex=0.05)
        for i in range(8):
            if i == 4:
                continue
            x = -160 + i * 290
            L.rect(x, y - 320, 250, 300, 0.12, tex=0.05)
            if rng.uniform() < 0.85:
                cx = x + rng.uniform(80, 170)
                L.brillo(cx, y - 200, 60, 0.4, tono=0.5)
                L.rect(cx - 22, y - 222, 44, 36, 0.85, emis=0.6)
                L.rect(cx - 24, y - 180, 48, 140, 0.10)
            reja(L, x, x + 250, y - 320, y - 20, sep=36, w=6, tono=0.10, travesanos=())
    L.linea([(1030, 1100), (1030, -3100)], 70, 0.30, jit=0.05)
    L.linea([(1030, 1100), (1030, -3100)], 12, 0.62, alfa=0.5, jit=0.05)
    for y in np.arange(1000, -3100, -340):
        L.rect(990, y - 24, 80, 18, 0.5)
    return L.capa(opaco=True)


# ====================================================================== TABLÓN
@mundo
def celda_oscura():
    """Otra celda (la de la segunda copia): azulejo blanco sucio, bombilla apagada colgando, terminal en una repisa, la ranura."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.15, sem=401)
    muro(L, -440, -300, 2360, Y_SUELO, "azulejo", 0.36, sem=402)
    L.linea([(1100, -300), (1100, 60)], 2.4, 0.05)
    L.elipse(1100, 90, 26, 34, 0.30)
    L.rect(300, 560, 900, 30, 0.30)
    L.rect(1500, 120, 200, 260, 0.30, tex=0.05)
    L.rect(1530, 160, 140, 90, 0.08)
    L.linea([(1600, -300), (1600, 120)], 46, 0.34)
    for x in (-300, 1900):
        L.rect(x, 500, 400, 60, 0.5, tex=0.1)
    suelo(L, -440, 2360, Y_SUELO, 1300, "baldosa", 0.22, sem=403, vp=(960, 200))
    return L.capa(opaco=True)


@mundo
def pared_tablon():
    """El muro de chapa del almacén donde se clavan los recados (el tablón clandestino); arriba, un tubo y una lámpara."""
    L = Lienzo(3600, 2200, origen=(-840, -560), base=0.15, sem=411)
    muro(L, -840, -560, 2760, 1640, "chapa", 0.24, sem=412)
    tuberias(L, -840, 2760, -480, n=2, tono=0.22, sem=413)
    return L.capa(opaco=True)


@mundo
def buzones():
    """Pared de apartados de correos de latón (14 x 8) con número y ventanita; un mostrador abajo."""
    L = Lienzo(2900, 1800, origen=(-500, -360), base=0.12, sem=421)
    L.rect(-500, -360, 2900, 1800, 0.16, tex=0.05)
    for j in range(8):
        for i in range(14):
            x, y = -400 + i * 200, -300 + j * 150
            L.rect(x, y, 186, 136, 0.40, tex=0.04)
            L.rect(x + 12, y + 12, 162, 112, 0.30, tex=0.04)
            L.rect(x + 40, y + 30, 100, 44, 0.12)
            L.elipse(x + 150, y + 100, 9, 9, 0.6)
            texto_lienzo(L, f"{(j * 14 + i) * 9 % 1200:04d}", x + 90, y + 104, 18, tono=0.1, fuente="C:/Windows/Fonts/courbd.ttf")
    L.rect(-500, 920, 2900, 60, 0.32, tex=0.06)
    L.rect(-500, 980, 2900, 460, 0.18, tex=0.06)
    return L.capa(opaco=True)


@mundo
def sala_analisis():
    """Sala de los investigadores: pared de paneles, una mesa larga con lámpara y el suelo de hormigón (la pantalla grande la dibuja la escena)."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=481)
    muro(L, -440, -300, 2360, Y_SUELO, "paneles", 0.2, sem=482)
    L.rect(-440, 760, 2800, 36, 0.3, tex=0.05)
    L.rect(-440, 796, 2800, 110, 0.14, tex=0.05)
    for x in (-300, 700, 1700):
        L.rect(x, 796, 30, 300, 0.12)
    suelo(L, -440, 2360, Y_SUELO, 1300, "hormigon", 0.16, sem=483, vp=(960, 100))
    return L.capa(opaco=True)


# ====================================================================== JEFE
@mundo
def escalera_almacen():
    """Escalera metálica que baja en diagonal desde una puerta alta a contraluz hasta el suelo del almacén; barandilla, niebla."""
    L = Lienzo(3000, 2000, origen=(-540, -600), base=0.08, sem=431)
    muro(L, -540, -600, 2460, 1400, "chapa", 0.14, sem=432)
    L.rect(1300, -420, 300, 460, 0.95, tex=0.0, emis=1.0)                 # la puerta abierta a contraluz
    L.rect(1280, -440, 340, 20, 0.2)
    L.rect(1180, 40, 600, 30, 0.22)
    for k in range(16):                                                    # peldaños
        x = 1180 - k * 62
        y = 70 + k * 52
        L.rect(x - 60, y, 70, 14, 0.26)
    L.poli([(1180, 70), (1210, 70), (240, 900), (210, 900)], 0.18)
    L.linea([(1230, -60), (250, 760)], 8, 0.24)
    for k in range(9):
        x = 1220 - k * 110
        y = -50 + k * 92
        L.linea([(x, y), (x, y + 130)], 4, 0.2)
    suelo(L, -540, 2460, 900, 1400, "hormigon", 0.18, sem=433)
    return L.capa(opaco=True)


@mundo
def sala_urna():
    """Cuarto vacío con una mesa de votación y la urna; un rayo de luz entra por una ventana alta."""
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.1, sem=441)
    muro(L, -440, -300, 2360, Y_SUELO, "paneles", 0.24, sem=442)
    ventana(L, 1500, -200, 300, 360, ciudad=False, sem=443, cristal=0.5)
    L.rect(560, 560, 800, 40, 0.34, tex=0.05)
    for x in (600, 1300):
        L.rect(x, 600, 24, 300, 0.2)
    cartel(L, 160, 100, 260, 180, "VOTE", px=60, tono=0.62, sub="ELECCIÓN DE JEFE")
    suelo(L, -440, 2360, Y_SUELO, 1300, "tablones", 0.22, sem=444, vp=(960, 100))
    return L.capa(opaco=True)


@mundo
def capataz():
    """La plataforma del capataz vista desde el suelo del almacén: viga, barandilla alta y focos que deslumbran."""
    L = Lienzo(3000, 2000, origen=(-540, -620), base=0.08, sem=451)
    muro(L, -540, -620, 2460, 1380, "ladrillo", 0.16, sem=452)
    L.rect(-540, 300, 3000, 70, 0.26, tex=0.05)                            # el piso de la plataforma
    L.rect(-540, 370, 3000, 30, 0.12)
    barandilla(L, -540, 2460, 300, alto=150, sep=46, tono=0.2)
    for x in np.arange(-400, 2460, 380):
        L.rect(x, 400, 30, 1000, 0.16)
        L.linea([(x + 15, 400), (x + 200, 700)], 6, 0.16)
    for x in (100, 960, 1800):
        lampara(L, x, -620, 120, 130, enc=True)
    suelo(L, -540, 2460, 1100, 1380, "hormigon", 0.16, sem=453)
    return L.capa(opaco=True)


@mundo
def escalera_cascada():
    """Una escalera larga de lado (de arriba a la izquierda a abajo a la derecha) contra un muro de hormigón."""
    L = Lienzo(3200, 1900, origen=(-640, -420), base=0.1, sem=461)
    muro(L, -640, -420, 2560, 1480, "hormigon", 0.22, sem=462)
    pts = []
    for k in range(14):
        x = -300 + k * 170
        y = -120 + k * 80
        L.rect(x, y, 170, 80, 0.30, tex=0.05)
        L.rect(x, y, 170, 14, 0.42)
        pts.append((x, y))
    L.poli([(-300, -40), (2080, 1080), (2080, 1480), (-300, 1480)], 0.12, tex=0.05)
    L.linea([(-300, -280), (2080, 840)], 6, 0.3)
    for k in range(0, 14, 2):
        L.linea([(-300 + k * 170, -280 + k * 80), (-300 + k * 170, -120 + k * 80)], 4, 0.26)
    return L.capa(opaco=True)


@mundo
def oficina_jefe():
    """El despacho que se adjudicó la copia jefa: pizarra enorme, ventanal sobre el almacén, mesa."""
    L = Lienzo(2900, 1700, origen=(-500, -320), base=0.1, sem=471)
    muro(L, -500, -320, 2400, 1000, "paneles", 0.22, sem=472)
    muro(L, -260, -220, 1500, 760, "pizarra", 0.12, sem=473)
    L.linea([(-260, -220), (1500, -220), (1500, 760), (-260, 760)], 18, 0.36, cerrado=True, jit=0.1)
    L.rect(-260, 760, 1760, 26, 0.36)
    ventana(L, 1640, -120, 600, 640, ciudad=False, sem=474, cristal=0.18)
    L.rect(-500, 1000, 2900, 400, 0.18, tex=0.06)
    return L.capa(opaco=True)
