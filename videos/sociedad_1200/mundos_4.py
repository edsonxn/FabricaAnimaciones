# -*- coding: utf-8 -*-
"""Lugares del ACTO II, segunda parte (caso_2017 · dialecto · desconexion · diplomacia · traicion).

    caso_2017:   bar_humo (reservado con botellas y neón) · archivo_sotano (bóveda de ladrillo con estantes de cajas) ·
                 menlo_park (campus de noche con palmeras) · laboratorio_2017 (mesa de pruebas con tableros de corcho)
    desconexion: sala_observacion (cuarto con gran luna de cristal) · bajo_mesa (patas y suelo vistos desde abajo) ·
                 sala_juntas (mesa larga en perspectiva)
    diplomacia:  escalera_baja (peldaños que bajan a la sombra) · escenario (tablado con telón al fondo) · salon_juego (club con mesa) ·
                 mapa_europa(estilo) (tablero de Diplomacy: Europa REAL, relieve ETOPO1 + países Natural Earth)
    traicion:    fachada_corte (edificio en corte con siete cuartos) · sala_analistas (gran marcador y gradas)
"""
import json
import math
import os

import cv2
import numpy as np

from mundos_base import mundo, muro, suelo, ventana, puerta, reja, barandilla, tuberias, conducto, estanteria, archivador, \
    servidor, cartel, lampara, cielo, ciudad, niebla_banda, agua
from noir_fondos import Lienzo, texto_lienzo, edificio

Y_SUELO = 900
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, "nucleo", "datos")
STENCIL = "C:/Windows/Fonts/STENCIL.TTF"


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== CASO 2017
@mundo
def bar_humo():
    """Bar de madrugada: muro de ladrillo con estantes de botellas, espejo y neón; reservado tapizado y suelo de tablones."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.08, sem=801)
    rng = _r(802)
    muro(L, -540, -420, 2460, 780, "ladrillo", 0.19, sem=803)
    # barra del fondo con estantes de botellas
    for r_, y in enumerate((60, 210, 360)):
        L.rect(260, y + 70, 1500, 16, 0.30, tex=0.1)
        for k in range(26):
            x = 280 + k * 56 + rng.uniform(-6, 6)
            al = rng.uniform(70, 120)
            tn = rng.uniform(0.20, 0.52)
            L.rect(x, y + 70 - al, 22, al, tn, tex=0.05)
            L.rect(x + 6, y + 70 - al - 22, 10, 22, tn, tex=0.05)
            L.rect(x + 3, y + 70 - al * 0.7, 6, al * 0.5, min(0.95, tn + 0.3), alfa=0.5, emis=0.2)
    L.rect(-150, -40, 380, 560, 0.10, tex=0.1)                                  # espejo
    L.poli([(-110, 480), (-40, 40), (60, 40), (-30, 480)], 0.30, alfa=0.35, blur=4)
    L.poli([(1900, -40), (2300, -40), (2300, 560), (1900, 560)], 0.08)           # ventana a la calle
    ventana(L, 1960, 40, 280, 420, ciudad=True, sem=804, cristal=0.12)
    # neón del bar
    L.rect(1010, -130, 380, 120, 0.12, tex=0.1)
    texto_lienzo(L, "OPEN BAR", 1200, -70, 70, tono=0.96, fuente="C:/Windows/Fonts/impact.ttf", track=6)
    L.brillo(1200, -70, 340, 0.55, ry=120, tono=0.95)
    suelo(L, -540, 2460, 780, 1380, "tablones", 0.20, sem=805)
    # reservado: respaldo tapizado capitoné
    L.rect(-540, 540, 3000, 300, 0.10, tex=0.14)
    for j in range(3):
        for i in range(34):
            x = -500 + i * 90 + (45 if j % 2 else 0)
            L.elipse(x, 590 + j * 90, 9, 9, 0.22, alfa=0.8)
    L.linea([(-540, 540), (2460, 540)], 5, 0.04)
    for x in (160, 1000, 1840):
        lampara(L, x, -420, 360, 150, enc=True)
    return L.capa(opaco=True)


@mundo
def archivo_sotano():
    """Sótano de archivo: bóveda de ladrillo, estantes de cajas con fecha, tuberías y una bombilla desnuda."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.06, sem=811)
    rng = _r(812)
    muro(L, -540, -420, 2460, 900, "ladrillo", 0.15, sem=813)
    # bóveda
    for k in range(9):
        a = k / 8
        L.linea([(-540 + a * 3000, -420), (960 + (a - 0.5) * 900, -160)], 3, 0.05, alfa=0.6)
    L.poli([(-540, -420), (2460, -420), (2460, -150), (1500, -250), (960, -280), (420, -250), (-540, -150)], 0.07, tex=0.12)
    tuberias(L, -540, 2460, -80, n=3, sem=814)
    # estantes de cajas a ambos lados y al fondo
    for x0, w in ((-300, 520), (1500, 520)):
        estanteria(L, x0, 900, w, 800, niveles=5, tono=0.14, sem=int(x0) % 90 + 815, rotulos=False, tono_caja=0.30)
    estanteria(L, 520, 880, 880, 620, niveles=4, tono=0.12, sem=816, tono_caja=0.28)
    for k in range(18):
        x, y = rng.uniform(600, 1300), rng.uniform(280, 860)
        L.rect(x, y, 70, 38, 0.82, alfa=0.55, tex=0.1)                              # etiquetas
    texto_lienzo(L, "ARCHIVO  2013-2019", 960, 140, 54, tono=0.60, fuente=STENCIL)
    suelo(L, -540, 2460, 900, 1380, "hormigon", 0.16, sem=817)
    for x in (260, 1660):
        lampara(L, x, -150, 320, 120, enc=True)
    return L.capa(opaco=True)


@mundo
def menlo_park():
    """Campus de Menlo Park de noche: cielo con luna sobre el crepúsculo, edificio bajo de paneles de cristal con luz cálida,
    palmeras altas en primer plano, césped con farolas y un sendero."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.06, sem=821)
    rng = _r(822)
    L.rect(-540, -420, 3000, 1300, 0.30, tex=0.05, grad=(0.58, -420, 760))               # cielo de crepúsculo (más claro al horizonte)
    for k in range(150):
        L.elipse(rng.uniform(-540, 2460), rng.uniform(-420, 300), 1.4, 1.4, rng.uniform(0.7, 0.98), tex=0, blur=0.4, alfa=rng.uniform(0.4, 0.9))
    for k in range(9):
        L.elipse(rng.uniform(-540, 2460), rng.uniform(-100, 480), rng.uniform(200, 520), rng.uniform(20, 56), 0.50, alfa=0.35, rug=1.4, blur=10, tex=0.15)
    L.elipse(1560, 20, 54, 54, 0.98, tex=0.0, emis=0.7)
    L.brillo(1560, 20, 300, 0.4, tono=0.9)
    pts = [(-540, 800)]
    for k in range(26):
        pts.append((-540 + k * 125, 640 + 70 * math.sin(k * 0.7) + rng.uniform(-30, 30)))
    pts += [(2460, 800)]
    L.poli(pts, 0.17, tex=0.1)                                                            # cerros lejanos
    # el edificio principal: paneles de cristal con luz cálida y parteluces
    X0, X1, Y0, Y1 = 180, 1700, 380, 800
    L.rect(X0, Y0, X1 - X0, Y1 - Y0, 0.10, tex=0.08)
    L.rect(X0 - 30, Y0 - 40, X1 - X0 + 60, 50, 0.22, tex=0.08)
    for fila in range(2):
        y = Y0 + 50 + fila * 170
        for i in range(11):
            x = X0 + 28 + i * 138
            L.rect(x, y, 112, 130, 0.78 if (i * 7 + fila * 3) % 5 else 0.55, tex=0.05, emis=0.75)
            L.rect(x + 54, y, 5, 130, 0.12)
            L.rect(x, y + 62, 112, 5, 0.12)
    L.rect(660, 720, 240, 80, 0.60, tex=0.05, emis=0.7)                                    # entrada
    L.rect(X0, Y1 - 4, X1 - X0, 8, 0.05)
    L.rect(X0 + 500, Y0 - 90, 520, 70, 0.08, tex=0.1)
    texto_lienzo(L, "FACEBOOK AI RESEARCH", X0 + 760, Y0 - 55, 34, tono=0.88, fuente="C:/Windows/Fonts/BOD_B.TTF", track=5)
    # edificios laterales más bajos
    for x, an, al in ((-480, 600, 250), (1760, 700, 300)):
        L.rect(x, 800 - al, an, al, 0.09, tex=0.08)
        for i in range(int(an // 110)):
            L.rect(x + 24 + i * 110, 800 - al + 50, 70, 90, 0.7, tex=0.05, emis=0.6)
    L.rect(-540, 800, 3000, 600, 0.11, tex=0.1)
    L.poli([(-540, 900), (2460, 900), (2460, 1380), (-540, 1380)], 0.15, tex=0.14)         # césped
    L.poli([(760, 800), (1000, 800), (1500, 1380), (240, 1380)], 0.26, tex=0.1)            # sendero
    # palmeras
    def palmera(x, base, alto, ancho=230):
        L.poli([(x - 14, base), (x + 14, base), (x + 8, base - alto), (x - 8, base - alto)], 0.03, tex=0.05)
        for q in range(10):
            a = math.pi * (1.02 + 0.96 * q / 9)
            ex, ey = x + math.cos(a) * ancho, base - alto + math.sin(a) * 120 + 90
            mx, my = x + (ex - x) * 0.5, base - alto + (ey - base + alto) * 0.5 - 50
            L.poli([(x, base - alto), (mx, my), (ex, ey), (mx, my + 16)], 0.03, tex=0.05)
    for x, base, al, an in ((60, 1000, 780, 260), (1640, 990, 700, 240), (2160, 1010, 820, 280), (-300, 1010, 760, 260), (1000, 880, 460, 190)):
        palmera(x, base, al, an)
    for x in (480, 1180, 1900):
        L.linea([(x, 960), (x, 700)], 6, 0.04)
        L.elipse(x, 690, 22, 15, 0.98, emis=0.95)
        L.brillo(x, 700, 200, 0.5, tono=0.95)
    return L.capa(opaco=True)


@mundo
def laboratorio_2017():
    """Laboratorio de investigación de 2017: muro con pizarras y corchos de papeles, ventanal y un mostrador de pruebas."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.10, sem=841)
    rng = _r(842)
    muro(L, -540, -420, 2460, 840, "azulejo", 0.26, sem=843)
    L.rect(-300, -160, 820, 540, 0.10, tex=0.08)                         # pizarra con fórmulas
    L.linea([(-300, -160), (520, -160), (520, 380), (-300, 380)], 6, 0.04, cerrado=True)
    for k in range(7):
        y = -110 + k * 72
        pts = [(-270, y)]
        for q in range(16):
            pts.append((-270 + q * 32, y + rng.uniform(-12, 12)))
        L.linea(pts, 2.0, 0.68, alfa=0.55, jit=1.0)
    L.rect(680, -120, 540, 420, 0.30, tex=0.16)                          # corcho con papeles
    for k in range(10):
        L.rect(rng.uniform(700, 1120), rng.uniform(-100, 200), rng.uniform(70, 110), rng.uniform(90, 140), 0.78, alfa=0.7, tex=0.1)
    ventana(L, 1480, -140, 760, 440, ciudad=True, sem=844, cristal=0.14, encendidas=0.4)
    suelo(L, -540, 2460, 840, 1380, "baldosa", 0.20, sem=845)
    # mostrador de pruebas
    L.rect(-540, 820, 3000, 60, 0.44, tex=0.1)
    L.rect(-540, 880, 3000, 500, 0.14, tex=0.1)
    L.linea([(-540, 820), (2460, 820)], 4, 0.05)
    for x in (220, 1000, 1780):
        lampara(L, x, -420, 330, 140, enc=True)
    return L.capa(opaco=True)


# ====================================================================== DESCONEXIÓN
@mundo
def sala_observacion():
    """Cuarto de observación a media luz: gran luna de cristal (con marco y reflejos) hacia el laboratorio iluminado."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.07, sem=851)
    muro(L, -540, -420, 2460, 900, "chapa", 0.13, sem=852)
    # el laboratorio visto a través de la luna: más claro
    L.rect(180, 0, 1560, 640, 0.34, tex=0.08, grad=(0.20, 0, 640))
    for k in range(6):
        L.rect(220 + k * 250, 280, 190, 120, 0.15, tex=0.05)
        L.rect(232 + k * 250, 292, 166, 84, 0.52, emis=0.5, tex=0.05)
    L.linea([(180, 0), (1740, 0), (1740, 640), (180, 640)], 14, 0.04, cerrado=True)
    for x in (700, 1220):
        L.linea([(x, 0), (x, 640)], 10, 0.04)
    L.poli([(300, 0), (420, 0), (240, 640), (120, 640)], 0.9, alfa=0.08, blur=6)
    L.poli([(1100, 0), (1200, 0), (1020, 640), (920, 640)], 0.9, alfa=0.06, blur=6)
    suelo(L, -540, 2460, 900, 1380, "baldosa", 0.12, sem=853)
    L.rect(-540, 640, 3000, 260, 0.10, tex=0.12)                           # repisa y consolas
    for k in range(8):
        L.rect(-300 + k * 380, 600, 240, 40, 0.18, tex=0.1)
        L.rect(-280 + k * 380, 612, 200, 14, 0.62, emis=0.3)
    lampara(L, 1840, -420, 330, 150, enc=True)
    return L.capa(opaco=True)


@mundo
def bajo_mesa():
    """Vista a ras de suelo bajo una mesa de juntas: tablero oscuro arriba, patas, manteles y sombras en el suelo de moqueta."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.05, sem=861)
    rng = _r(862)
    L.rect(-540, -420, 3000, 780, 0.07, tex=0.12, grad=(0.03, -420, 360))        # canto inferior de la mesa
    L.rect(-540, 300, 3000, 90, 0.16, tex=0.1)
    L.rect(-540, 390, 3000, 40, 0.05)
    for x in (-60, 700, 1500, 2160):                                          # patas
        L.poli([(x - 40, 430), (x + 40, 430), (x + 30, 960), (x - 30, 960)], 0.15, tex=0.1)
        L.linea([(x - 40, 430), (x - 30, 960)], 3, 0.05)
    L.rect(-540, 430, 3000, 560, 0.08, tex=0.1)
    L.rect(-540, 960, 3000, 420, 0.11, tex=0.14)                              # moqueta
    for k in range(60):
        x, y = rng.uniform(-540, 2460), rng.uniform(970, 1380)
        L.linea([(x, y), (x + rng.uniform(-30, 30), y + rng.uniform(-6, 6))], 1.2, 0.06, alfa=0.5)
    L.poli([(-540, 960), (2460, 960), (2460, 1000), (-540, 1000)], 0.04, blur=6)
    for x in (300, 1100, 1900):                                               # cables por el suelo
        L.linea([(x, 960), (x + 90, 1090), (x - 60, 1220), (x + 160, 1380)], 6, 0.04)
    return L.capa(opaco=True)


@mundo
def sala_juntas():
    """Sala de juntas en sombra: mesa larga en perspectiva, sillas de respaldo alto, ventanal con luna al fondo."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.06, sem=871)
    muro(L, -540, -420, 2460, 700, "madera", 0.14, sem=872)
    ventana(L, 520, -60, 880, 560, ciudad=True, sem=873, cristal=0.16, encendidas=0.3, luna=None)
    for x in (810, 1100):
        L.linea([(x, -60), (x, 500)], 8, 0.05)
    suelo(L, -540, 2460, 700, 1380, "tablones", 0.12, sem=874)
    vp = (960.0, 560.0)
    # mesa: trapecio en perspectiva
    L.poli([(vp[0] - 330, 740), (vp[0] + 330, 740), (vp[0] + 1020, 1340), (vp[0] - 1020, 1340)], 0.24, tex=0.08, grad=(0.12, 740, 1340))
    L.linea([(vp[0] - 330, 740), (vp[0] - 1020, 1340)], 4, 0.05)
    L.linea([(vp[0] + 330, 740), (vp[0] + 1020, 1340)], 4, 0.05)
    L.poli([(vp[0] - 330, 740), (vp[0] + 330, 740), (vp[0] + 340, 770), (vp[0] - 340, 770)], 0.34, tex=0.05)
    for lado in (-1, 1):                                                      # sillas de respaldo alto
        for k in range(5):
            f = 0.15 + k * 0.17
            x = vp[0] + lado * (430 + 700 * f)
            y = 780 + 520 * f
            s = 0.4 + 0.9 * f
            L.poli([(x - 40 * s, y - 330 * s), (x + 40 * s, y - 330 * s), (x + 46 * s, y - 40 * s), (x - 46 * s, y - 40 * s)], 0.10, tex=0.1)
            L.linea([(x - 40 * s, y - 330 * s), (x + 40 * s, y - 330 * s)], 3 * s + 1, 0.04)
    L.poli([(-540, -420), (700, -420), (480, 180), (-540, 330)], 0.04, alfa=0.5, blur=14)
    return L.capa(opaco=True)


# ====================================================================== DIPLOMACIA
@mundo
def escalera_baja():
    """Escalera que baja a la oscuridad vista de frente y un poco desde arriba: cada peldaño más estrecho y oscuro."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.05, sem=881)
    muro(L, -540, -420, 2460, 1000, "ladrillo", 0.14, sem=882)
    vp = (960.0, 360.0)
    n = 12
    for k in range(n):
        f0, f1 = k / n, (k + 1) / n
        ya, yb = 1380 - (1380 - vp[1]) * f0 ** 0.8, 1380 - (1380 - vp[1]) * f1 ** 0.8
        sc = 1 - f0 * 0.9
        xa0, xa1 = 960 - 1400 * sc, 960 + 1400 * sc
        tono = 0.30 * (1 - f0 * 0.85)
        L.poli([(xa0, ya), (xa1, ya), (xa1 - 60 * sc, yb), (xa0 + 60 * sc, yb)], tono, tex=0.08)
        L.linea([(xa0, ya), (xa1, ya)], 3 + 3 * sc, 0.03)
        L.rect(xa0, yb - 20 * sc, xa1 - xa0, 26 * sc, tono * 0.5, alfa=0.7)
    for lado in (-1, 1):                                                      # barandas y muros laterales
        L.poli([(960 + lado * 1500, -420), (960 + lado * 1500, 1380), (960 + lado * 140, 380), (960 + lado * 140, -100)], 0.08, tex=0.1,
               grad=(0.02, -420, 1380))
    L.poli([(760, 300), (1160, 300), (1160, 420), (760, 420)], 0.01, blur=10)           # el pozo oscuro al fondo
    lampara(L, 960, -420, 300, 120, enc=True)
    return L.capa(opaco=True)


@mundo
def escenario():
    """Tablado de teatro: suelo de tablones, fondo negro con tubos de luz y ARCO con proscenio."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.04, sem=891)
    L.rect(-540, -420, 3000, 1300, 0.05, tex=0.1, grad=(0.10, -420, 880))
    for k in range(7):
        L.rect(-300 + k * 460, -420, 90, 1300, 0.07, alfa=0.7)
    suelo(L, -540, 2460, 880, 1380, "tablones", 0.22, sem=892)
    L.linea([(-540, 880), (2460, 880)], 5, 0.05)
    for k in range(-6, 7):
        L.linea([(960 + k * 40, 880), (960 + k * 340, 1380)], 2, 0.06, alfa=0.7)
    for x in (110, 820, 1100, 1810):
        L.rect(x - 90, -420, 180, 70, 0.10, tex=0.1)                         # focos en la barra
    L.rect(-540, -420, 3000, 80, 0.03)
    return L.capa(opaco=True)


@mundo
def mapa_europa(estilo="tablero"):
    """Europa occidental REAL: relieve ETOPO1 con sombreado, países Natural Earth con borde y capitales. Proyección: lon/lat →
    X = 960 + (lon - 2.5) * 79, Y = 540 - (lat - 44) * 110 (ver XY_EU). estilo = tablero (visión general) | frente (zonas calientes)."""
    z = np.load(os.path.join(DATOS, "relieve_eu.npz"))
    alt = z["alt"].astype(np.float32)
    lat0, lon0, paso = float(z["lat0"]), float(z["lon0"]), float(z["paso"])
    ox, oy, w, hh = -240, -360, 2400, 1800
    L = Lienzo(w, hh, origen=(ox, oy), base=0.1, sem=901)
    xs = (np.arange(w, dtype=np.float32) + ox - 960) / 79.0 + 2.5            # lon por columna
    ys = 44.0 - (np.arange(hh, dtype=np.float32) + oy - 540) / 110.0         # lat por fila
    mx = ((xs - lon0) / paso)[None, :] * np.ones((hh, 1), np.float32)
    my = ((ys - lat0) / paso)[:, None] * np.ones((1, w), np.float32)
    a = cv2.remap(alt, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    a = cv2.GaussianBlur(a, (0, 0), 1.6)
    gx = cv2.Sobel(a, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(a, cv2.CV_32F, 0, 1, ksize=3)
    luz = np.clip(-(gx * 0.7 + gy * 0.7) / 900.0, -1, 1)                       # luz desde arriba-izquierda
    tierra = a > 0
    t_t = 0.30 + 0.16 * np.clip(a / 2400.0, 0, 1) + 0.12 * luz
    t_m = 0.095 + 0.03 * np.clip(-a / 3000.0, 0, 1)
    g = np.where(tierra, t_t, t_m)
    cost = cv2.GaussianBlur(tierra.astype(np.float32), (0, 0), 10)              # halo de costa en el mar
    g = np.where(tierra, g, g + 0.07 * cost ** 2)
    L.g[:] = g.astype(np.float32)
    L.a[:] = 1.0
    # países: tono propio suave + borde
    P = json.load(open(os.path.join(DATOS, "paises.json"), encoding="utf-8"))
    nombres = {"France": "FRANCIA", "United Kingdom": "INGLATERRA", "Germany": "ALEMANIA", "Italy": "ITALIA", "Spain": "ESPAÑA",
               "Austria": "AUSTRIA"}
    cap = {"LONDRES": (-0.12, 51.5), "PARÍS": (2.35, 48.86), "MADRID": (-3.7, 40.42), "ROMA": (12.5, 41.9), "VIENA": (16.37, 48.2),
           "MUNICH": (11.58, 48.14), "BRUSELAS": (4.35, 50.85), "MARSELLA": (5.37, 43.3), "BERLÍN": (13.4, 52.52)}

    def xy(lo, la):
        return 960 + (lo - 2.5) * 79.0, 540 - (la - 44.0) * 110.0
    gen = _r(902)
    for nom, anillos in P.items():
        for ring in anillos:
            Q = np.array(ring, float)
            if len(Q) < 4 or Q[:, 0].max() < -13 or Q[:, 0].min() > 18 or Q[:, 1].max() < 35 or Q[:, 1].min() > 53:
                continue
            Pm = np.array([xy(lo, la) for lo, la in Q])
            tono = 0.5 + 0.07 * (hash(nom) % 7) / 7
            L.poli(Pm, 0.30 + 0.04 * ((hash(nom) % 5) - 2), alfa=0.14 if estilo == "tablero" else 0.10, tex=0.0, blur=0.6)
            L.linea(Pm, 3.2, 0.68 if nom in nombres else 0.5, alfa=0.85, jit=0.4, cerrado=True)
    # capitales
    for nom, (lo, la) in cap.items():
        x, y = xy(lo, la)
        L.elipse(x, y, 9, 9, 0.95, emis=0.7, tex=0)
        L.elipse(x, y, 16, 16, 0.10, alfa=0.0)
        texto_lienzo(L, nom, x, y - 30, 28, tono=0.88, fuente="C:/Windows/Fonts/BOD_B.TTF", track=4)
    for nom, (lo, la) in {"MAR DEL NORTE": (3.0, 53.7), "OCÉANO ATLÁNTICO": (-9.5, 46.0), "MEDITERRÁNEO": (6.0, 38.4),
                          "CANAL": (-1.2, 50.2)}.items():
        x, y = xy(lo, la)
        texto_lienzo(L, nom, x, y, 30, tono=0.40, fuente="C:/Windows/Fonts/BOD_B.TTF", track=9, alfa=0.9)
    # cuadrícula de tablero
    for lo in range(-12, 18, 2):
        x0, y0 = xy(lo, 36)
        x1, y1 = xy(lo, 52)
        L.linea([(x0, y0), (x1, y1)], 1.3, 0.6, alfa=0.14, jit=0)
    for la in range(36, 53, 2):
        x0, y0 = xy(-12, la)
        x1, y1 = xy(17, la)
        L.linea([(x0, y0), (x1, y1)], 1.3, 0.6, alfa=0.14, jit=0)
    return L.capa(opaco=True)


def xy_eu(lon, lat):
    """Coordenada del MUNDO en el lugar mapa_europa."""
    return 960 + (lon - 2.5) * 79.0, 540 - (lat - 44.0) * 110.0


@mundo
def salon_juego():
    """Salón de juegos de un club: pared con boiserie de madera, cuadros, ventana con cortinas y una mesa larga delante."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.08, sem=931)
    rng = _r(932)
    muro(L, -540, -420, 2460, 840, "madera", 0.16, sem=933)
    for k in range(9):                                                          # paneles de boiserie
        x = -500 + k * 340
        L.rect(x, 360, 300, 440, 0.12, tex=0.1)
        L.linea([(x, 360), (x + 300, 360), (x + 300, 800), (x, 800)], 3, 0.05, cerrado=True)
    for x, y, w, hh in ((-80, -80, 360, 280), (1400, -100, 420, 320), (380, 20, 240, 170)):                  # cuadros con marco dorado
        L.rect(x - 14, y - 14, w + 28, hh + 28, 0.40, tex=0.1)
        L.rect(x, y, w, hh, 0.12, tex=0.1)
        L.poli([(x + 20, y + hh - 20), (x + w * 0.4, y + hh * 0.4), (x + w * 0.7, y + hh * 0.7), (x + w - 20, y + hh * 0.3), (x + w - 20, y + hh - 20)],
               0.18, tex=0.1)
    ventana(L, 820, -100, 440, 440, ciudad=True, sem=934, cristal=0.14, encendidas=0.3)
    for sx in (-1, 1):                                                          # cortinas
        x = 1040 + sx * 280
        L.poli([(x - 80, -140), (x + 80, -140), (x + 60 * sx + 40, 560), (x - 60 * sx - 40, 560)], 0.20, tex=0.1)
        for q in range(5):
            L.linea([(x - 60 + q * 30, -130), (x - 50 + q * 30 + 10 * sx, 550)], 3, 0.08, alfa=0.7)
    suelo(L, -540, 2460, 840, 1380, "tablones", 0.14, sem=935)
    L.poli([(-540, 800), (2460, 800), (2460, 1000), (-540, 1000)], 0.30, tex=0.1, grad=(0.18, 800, 1000))   # mesa
    L.linea([(-540, 800), (2460, 800)], 4, 0.05)
    L.rect(-540, 1000, 3000, 380, 0.08, tex=0.1)
    lampara(L, 960, -420, 520, 260, enc=True)
    return L.capa(opaco=True)


# ====================================================================== TRAICIÓN
@mundo
def fachada_corte():
    """Edificio de oficinas en corte: tres pisos, siete cuartos con su ventana y su mesa; la noche y la calle fuera."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.05, sem=911)
    cielo(L, -540, -420, 2460, 700, tono=0.09, sem=912, estrellas=90, nubes=8)
    ciudad(L, -540, 2460, 700, alto=(260, 700), sem=913, encendidas=0.3, detalle=0.6)
    L.rect(-540, 700, 3000, 680, 0.05)
    # el edificio en corte
    X0, X1, Y0, Y1 = 60, 1860, -120, 1100
    L.rect(X0 - 24, Y0 - 24, X1 - X0 + 48, Y1 - Y0 + 24, 0.08, tex=0.1)
    cuartos = []
    pisos = ((Y0, 3), (Y0 + 410, 2), (Y0 + 820, 2))
    for yy, n in pisos:
        an = (X1 - X0) / n
        for i in range(n):
            x = X0 + i * an
            L.rect(x + 8, yy + 8, an - 16, 394, 0.17, tex=0.07)
            L.rect(x + 8, yy + 8, an - 16, 394, 0.22, alfa=0.0)
            L.poli([(x + 8, yy + 330), (x + an - 8, yy + 330), (x + an - 8, yy + 402), (x + 8, yy + 402)], 0.11, tex=0.1)   # suelo
            vw = min(260.0, an * 0.34)
            ventana(L, x + an * 0.5 - vw / 2, yy + 50, vw, 190, ciudad=False, sem=914 + i + int(yy) % 7, cristal=0.28, marco=0.30,
                    encendidas=0.0)
            L.rect(x + an * 0.18, yy + 262, an * 0.62, 20, 0.32, tex=0.08)                     # mesa
            L.rect(x + an * 0.20, yy + 282, 14, 52, 0.10)
            L.rect(x + an * 0.76, yy + 282, 14, 52, 0.10)
            cuartos.append((x + an * 0.5, yy + 330, an))
    for yy, n in pisos[1:]:
        L.rect(X0 - 24, yy - 4, X1 - X0 + 48, 14, 0.04)
    L.rect(X0 - 24, Y1, X1 - X0 + 48, 40, 0.06)
    suelo(L, -540, 2460, 1140, 1380, "hormigon", 0.12, sem=915)
    return L.capa(opaco=True)


def cuartos_fachada(n=7):
    """Centros (x, y_suelo, ancho) de los 7 cuartos de fachada_corte (mismo cálculo que el lugar)."""
    X0, X1, Y0 = 60, 1860, -120
    out = []
    for yy, n in ((Y0, 3), (Y0 + 410, 2), (Y0 + 820, 2)):
        an = (X1 - X0) / n
        for i in range(n):
            out.append((X0 + i * an + an * 0.5, yy + 330, an))
    return out


@mundo
def sala_analistas():
    """Sala de análisis: gran marcador apagado en el muro, mesas de mando y gradas de butacas en sombra."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.06, sem=921)
    muro(L, -540, -420, 2460, 880, "chapa", 0.12, sem=922)
    L.rect(260, -40, 1400, 640, 0.07, tex=0.05)
    L.linea([(260, -40), (1660, -40), (1660, 600), (260, 600)], 12, 0.04, cerrado=True)
    suelo(L, -540, 2460, 880, 1380, "baldosa", 0.12, sem=923)
    for f in range(3):                                                        # gradas
        y = 760 + f * 150
        L.rect(-540, y, 3000, 150, 0.08 + 0.02 * f, tex=0.1)
        L.linea([(-540, y), (2460, y)], 4, 0.04)
        for k in range(22):
            x = -500 + k * 150 + (60 if f % 2 else 0)
            L.poli([(x, y + 24), (x + 90, y + 24), (x + 80, y + 120), (x + 10, y + 120)], 0.05 + 0.02 * f, tex=0.08)
    lampara(L, 960, -420, 300, 160, enc=True)
    return L.capa(opaco=True)
