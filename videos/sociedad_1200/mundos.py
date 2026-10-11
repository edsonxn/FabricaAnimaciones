# -*- coding: utf-8 -*-
"""Mundos pintados de «El caso de la máquina» (estilo noir). Cada función se pinta una vez por proceso (lru_cache).

CIUDAD (escenas lluvia y amanecer), coordenadas del mundo a prof 1 (la calle):
  acera: y 880 (pie de los edificios) .. 950 (bordillo); calle 950 .. 1250.
  farola del detective x = 1080 (farol en ~1020, 430); callejón oscuro x 1020..1140 detrás de él.
  hotel con letrero 1150..1700 · esquina (cruce) 2440..2720 con farola y el loco del cartel · bolsa 2780..4080.
Capas con paralaje: cielo (0.05) · lejos (0.3) · medio (0.6, con el rascacielos de cristal del laboratorio en x≈990) · calle (1.0).
Una capa de profundidad p se ve con la cámara en W/2 + (c - W/2)·p: por eso la torre de la capa media está en x≈990, y≈-900.
"""
import functools
import math

import numpy as np

from motor import H, W
from noir import fbm
from noir_fondos import (Lienzo, bolsa, edificio, escalera_incendio, farola, letrero_vertical, tanque_agua, texto_lienzo,
                         tienda, ventana)

Y_ACERA, Y_BORDILLO = 880, 950
X_FAROLA = 1080
X_ESQUINA = 2580


@functools.lru_cache(maxsize=1)
def cielo():
    """Cielo de tormenta (opaco): degradado, luna velada arriba a la izquierda y nubes con borde iluminado."""
    L = Lienzo(3400, 1500, origen=(-700, -300), base=0.0, sem=71)
    L.poli([(-700, -300), (2700, -300), (2700, 1200), (-700, 1200)], 0.30, tex=0.05, grad=(0.46, -300, 1100))
    L.brillo(380, 120, 300, 0.7, tono=0.8)
    L.elipse(380, 120, 46, 46, 0.92, tex=0.02, emis=0.6)
    n = 0.65 * fbm(L.w, L.h, 260, 5, 72) + 0.35 * fbm(L.w, L.h, 70, 3, 73)
    yy = np.arange(L.h, dtype=np.float32)[:, None]
    banda = np.clip(1 - np.abs(yy - 520) / 700, 0, 1)
    nube = np.clip((n * 0.55 + banda * 0.9 - 0.55) * 2.2, 0, 1)
    import cv2
    borde = np.clip(1 - np.abs(nube - 0.3) / 0.3, 0, 1) * np.clip(1 - np.hypot(np.arange(L.w)[None, :] - 1080, yy - 420) / 1300, 0, 1)
    borde = cv2.GaussianBlur(borde.astype(np.float32), (0, 0), 9)
    L.g = L.g * (1 - nube * 0.7) + nube * 0.18 + borde * 0.22
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def lejos():
    """Horizonte lejano: siluetas de rascacielos art déco y de ladrillo con ventanitas encendidas."""
    L = Lienzo(3600, 1900, origen=(-500, -1100), sem=81)
    rng = np.random.default_rng(81)
    x = -480
    while x < 3080:
        an = rng.uniform(140, 300)
        al = rng.uniform(380, 1000)
        tp = "deco" if rng.uniform() < 0.3 else "ladrillo"
        edificio(L, x, 760, an, al, tipo=tp, sem=int(rng.integers(1e6)), encendidas=0.12, prof_lado=20, detalle=0.3)
        x += an + rng.uniform(-40, 40)
    L.e *= 0.7
    return L.capa()


@functools.lru_cache(maxsize=1)
def medio():
    """Plano medio: edificios altos y el RASCACIELOS DE CRISTAL del laboratorio de IA (x 840..1140, corona en y≈-900)."""
    L = Lienzo(4300, 2900, origen=(-400, -1500), sem=91)
    rng = np.random.default_rng(91)
    filas = [(-380, 300, 1150, "ladrillo"), (-40, 260, 1400, "deco"), (260, 300, 1000, "ladrillo"), (560, 230, 1200, "ladrillo"),
             (1200, 280, 1300, "deco"), (1520, 320, 950, "ladrillo"), (1880, 260, 1250, "deco"), (2180, 300, 1050, "ladrillo"),
             (2520, 260, 1350, "deco"), (2820, 300, 1000, "ladrillo"), (3160, 280, 1200, "ladrillo"), (3480, 300, 1100, "deco")]
    for i, (x, an, al, tp) in enumerate(filas):
        edificio(L, x, 1000, an, al, tipo=tp, sem=200 + i, encendidas=0.16, prof_lado=30, detalle=0.7)
    edificio(L, 840, 1000, 300, 2150, tipo="cristal", sem=7, encendidas=0.30, prof_lado=36, detalle=1.0)
    return L.capa()


@functools.lru_cache(maxsize=1)
def calle():
    """La calle (prof 1): fachadas, acera mojada, bordillo, asfalto, farolas, hotel, esquina y la bolsa de valores."""
    L = Lienzo(5400, 2000, origen=(-300, -750), sem=101)
    rng = np.random.default_rng(101)
    # fachadas
    edificio(L, -300, Y_ACERA, 380, 1000, tipo="tienda", sem=301)
    edificio(L, 120, Y_ACERA, 420, 1250, tipo="ladrillo", sem=302)
    edificio(L, 580, Y_ACERA, 440, 980, tipo="tienda", sem=303)
    # callejón detrás de la farola: muros oscuros, cubo de basura, escalera
    L.rect(1020, -200, 120, Y_ACERA + 200, 0.03, tex=0.15)
    L.trama([(1020, 200), (1140, 200), (1140, Y_ACERA), (1020, Y_ACERA)], ang=70, sep=8, tono=0.0, alfa=0.5)
    escalera_incendio(L, 1030, 300, Y_ACERA - 60, w=90, piso=110, tono=0.12)
    edificio(L, 1140, Y_ACERA, 560, 1150, tipo="tienda", sem=304, encendidas=0.25)
    letrero_vertical(L, 1660, 120, "HOTEL", ancho=74, px=60)
    edificio(L, 1760, Y_ACERA, 640, 1050, tipo="ladrillo", sem=305)
    # esquina: el cruce deja ver la ciudad del fondo (sin pintar = transparente)
    edificio(L, 2760, Y_ACERA, 1360, 820, tipo="ladrillo", sem=306, encendidas=0.05)
    bolsa(L, 2800, Y_ACERA, ancho=1240, alto=780)
    edificio(L, 4120, Y_ACERA, 520, 1100, tipo="tienda", sem=307)
    edificio(L, 4660, Y_ACERA, 460, 1300, tipo="ladrillo", sem=308)
    # acera, bordillo y asfalto (con el cruce)
    L.poli([(-300, Y_ACERA), (5100, Y_ACERA), (5100, Y_BORDILLO), (-300, Y_BORDILLO)], 0.30, tex=0.1, grad=(0.22, Y_ACERA, Y_BORDILLO))
    for bx in np.arange(-300, 5100, 110):
        L.linea([(bx, Y_ACERA), (bx - 30, Y_BORDILLO)], 1.2, 0.08, alfa=0.5, jit=0.3)
    L.rect(-300, Y_BORDILLO - 6, 5400, 14, 0.42, tex=0.05)
    L.linea([(-300, Y_BORDILLO - 6), (5100, Y_BORDILLO - 6)], 2, 0.6, alfa=0.6)
    L.poli([(-300, Y_BORDILLO + 8), (5100, Y_BORDILLO + 8), (5100, 1250), (-300, 1250)], 0.10, tex=0.14, grad=(0.06, 960, 1250))
    for k in range(18):                                             # charcos (más claros: reflejan el cielo)
        cx, cy = rng.uniform(-200, 5000), rng.uniform(980, 1220)
        L.elipse(cx, cy, rng.uniform(60, 220), rng.uniform(8, 22), 0.20, alfa=0.7, rug=1.0, tex=0.05)
    for k in range(40):                                             # raya discontinua del carril
        L.poli([(k * 140 - 300, 1130), (k * 140 - 220, 1130), (k * 140 - 222, 1138), (k * 140 - 302, 1138)], 0.32, alfa=0.7)
    # boca de incendios, cubos, buzón
    for hx in (420, 2300):
        L.poli([(hx - 14, Y_BORDILLO - 4), (hx + 14, Y_BORDILLO - 4), (hx + 12, Y_BORDILLO - 50), (hx - 12, Y_BORDILLO - 50)], 0.16)
        L.elipse(hx, Y_BORDILLO - 52, 16, 9, 0.22)
        L.rect(hx - 22, Y_BORDILLO - 36, 44, 9, 0.14)
        L.linea([(hx - 14, Y_BORDILLO - 4), (hx - 12, Y_BORDILLO - 50)], 2, 0.6, alfa=0.5)
    for cx in (1050, 1100):
        L.poli([(cx - 20, Y_ACERA + 4), (cx + 20, Y_ACERA + 4), (cx + 16, Y_ACERA - 52), (cx - 16, Y_ACERA - 52)], 0.12)
        L.elipse(cx, Y_ACERA - 54, 22, 6, 0.18)
        for k in range(3):
            L.linea([(cx - 18 + k * 2, Y_ACERA - 40 + k * 14), (cx + 18 - k * 2, Y_ACERA - 40 + k * 14)], 1.5, 0.03, jit=0)
    # farolas (la del detective y la de la esquina)
    farola(L, X_FAROLA, Y_ACERA + 40, alto=520, brazo=60)
    farola(L, X_ESQUINA - 120, Y_ACERA + 40, alto=520, brazo=-60)
    # semáforo/poste de la esquina con el letrero de la calle
    L.rect(2700, Y_ACERA - 340, 10, 380, 0.06)
    L.rect(2650, Y_ACERA - 340, 110, 26, 0.75)
    texto_lienzo(L, "AV. CENTRAL", 2705, Y_ACERA - 327, 20, tono=0.06, fuente="C:/Windows/Fonts/courbd.ttf", track=1)
    return L.capa()


@functools.lru_cache(maxsize=1)
def documento():
    """Primer plano: la hoja mojada del prospecto (2400 x 1400, centrada en 0, 0), con los renglones de letra pequeña ya impresos."""
    L = Lienzo(2400, 1400, origen=(-1200, -700), sem=111)
    L.poli([(-1200, -700), (1200, -700), (1200, 700), (-1200, 700)], 0.05, tex=0.2)                  # asfalto mojado
    for k in range(30):
        r = np.random.default_rng(k)
        L.elipse(r.uniform(-1200, 1200), r.uniform(-700, 700), r.uniform(30, 160), r.uniform(10, 40), 0.12, alfa=0.6, rug=1.0)
    hoja = [(-560, -640), (590, -660), (610, 650), (-580, 670)]
    L.poli([(p[0] + 18, p[1] + 22) for p in hoja], 0.0, alfa=0.6, blur=10)                         # sombra
    L.poli(hoja, 0.86, tex=0.05, grad=(0.78, -660, 670))
    L.linea(hoja, 2.0, 0.25, cerrado=True)
    texto_lienzo(L, "PROSPECTO DE OFERTA PÚBLICA", -10, -560, 34, tono=0.12, fuente="C:/Windows/Fonts/courbd.ttf", track=3)
    L.linea([(-480, -520), (480, -524)], 2.0, 0.2)
    texto_lienzo(L, "FACTORES DE RIESGO", -10, -440, 56, tono=0.06, fuente="C:/Windows/Fonts/courbd.ttf", track=4)
    rng = np.random.default_rng(5)
    for k in range(22):                                             # letra pequeña
        y = -360 + k * 40
        if -60 < y < 120:
            continue
        x0 = -480
        while x0 < 470:
            wl = rng.uniform(30, 110)
            L.rect(x0, y, min(wl, 480 - x0), 10, 0.30, alfa=0.85, tex=0.2)
            x0 += wl + rng.uniform(10, 18)
    texto_lienzo(L, "pág. 34 de 261", 380, 600, 24, tono=0.25, fuente="C:/Windows/Fonts/cour.ttf", track=1)
    return L.capa()


# ====================================================================== INTERIORES (prof 1; suelo en y = 900)
Y_SUELO = 900


def _suelo_tablas(L, x0, x1, y0, y1, tono=0.26, sem=0):
    L.poli([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], tono, tex=0.12, grad=(tono * 0.6, y0, y1))
    for k in range(int((x1 - x0) // 90) + 4):
        xa = x0 + k * 90
        L.linea([(xa, y0), (xa + (xa - (x0 + x1) / 2) * 0.6, y1)], 1.6, 0.06, alfa=0.7, jit=0.4, sem=k)
    for k in range(6):
        yy = y0 + (y1 - y0) * (k / 6) ** 1.6
        L.linea([(x0, yy), (x1, yy)], 1.0, 0.08, alfa=0.35, jit=0.3)


def _zocalo(L, x0, x1, y_suelo, alto=260, tono=0.22):
    L.rect(x0, y_suelo - alto, x1 - x0, alto, tono, tex=0.12, grad=(tono * 0.7, y_suelo - alto, y_suelo))
    for k in range(int((x1 - x0) // 220) + 1):
        xa = x0 + k * 220 + 20
        L.rect(xa, y_suelo - alto + 26, 180, alto - 60, tono * 1.15, tex=0.1)
        L.linea([(xa, y_suelo - alto + 26), (xa + 180, y_suelo - alto + 26), (xa + 180, y_suelo - 34), (xa, y_suelo - 34)], 1.6, 0.05,
                cerrado=True)
    L.rect(x0, y_suelo - alto - 14, x1 - x0, 16, tono * 1.4)
    L.linea([(x0, y_suelo - alto - 14), (x1, y_suelo - alto - 14)], 1.6, 0.6, alfa=0.5)
    L.rect(x0, y_suelo - 20, x1 - x0, 20, tono * 0.6)


@functools.lru_cache(maxsize=1)
def sala_rueda():
    """Sala de rueda de reconocimiento: pared con líneas de estatura numeradas, focos en el techo, suelo de cemento."""
    L = Lienzo(3000, 1700, origen=(-500, -600), base=0.0, sem=121)
    L.poli([(-500, -600), (2500, -600), (2500, Y_SUELO), (-500, Y_SUELO)], 0.44, tex=0.1, grad=(0.30, -600, Y_SUELO))
    for k, cm in enumerate(range(140, 215, 5)):                     # escala de estatura (5 cm = 33 px)
        y = Y_SUELO - (cm - 100) * 6.6
        mayor = cm % 10 == 0
        L.linea([(-500, y), (2500, y)], 3.0 if mayor else 1.4, 0.08, alfa=0.9 if mayor else 0.5, jit=0.2, sem=k)
        if mayor:
            for xx in (-380, 420, 1220, 2020):
                texto_lienzo(L, f"{cm}", xx, y - 24, 34, tono=0.08, fuente="C:/Windows/Fonts/impact.ttf", track=2)
    for k in range(4):                                             # números del puesto en el suelo
        xx = 200 + k * 420
        texto_lienzo(L, str(k + 1), xx, Y_SUELO + 110, 120, tono=0.55, fuente="C:/Windows/Fonts/impact.ttf")
    L.poli([(-500, Y_SUELO), (2500, Y_SUELO), (2500, 1100), (-500, 1100)], 0.22, tex=0.16, grad=(0.12, Y_SUELO, 1100))
    L.rect(-500, Y_SUELO - 8, 3000, 10, 0.12)
    for k in range(4):                                             # focos de techo
        xx = 200 + k * 420
        L.rect(xx - 60, -600, 120, 40, 0.10)
        L.poli([(xx - 70, -560), (xx + 70, -560), (xx + 50, -530), (xx - 50, -530)], 0.85, emis=0.8, tex=0.0)
    for k in range(40):                                            # manchas y desconchones de la pared
        r = np.random.default_rng(k + 400)
        L.elipse(r.uniform(-500, 2500), r.uniform(-500, Y_SUELO - 40), r.uniform(10, 90), r.uniform(8, 50), 0.32, alfa=0.35, rug=1.0)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def sala_interrogatorio():
    """Sala de interrogatorio: cemento manchado, espejo falso a la izquierda, puerta con vidrio esmerilado, tuberías."""
    L = Lienzo(3200, 1800, origen=(-700, -700), base=0.0, sem=131)
    L.poli([(-700, -700), (2500, -700), (2500, Y_SUELO), (-700, Y_SUELO)], 0.30, tex=0.16, grad=(0.20, -700, Y_SUELO))
    for k in range(int(3200 // 160)):                              # bloques de cemento
        for j in range(int(1600 // 80)):
            xx = -700 + k * 160 + (80 if j % 2 else 0)
            yy = -700 + j * 80
            L.linea([(xx, yy), (xx + 160, yy)], 1.2, 0.12, alfa=0.45, jit=0.3)
            L.linea([(xx, yy), (xx, yy + 80)], 1.2, 0.12, alfa=0.45, jit=0.3)
    for k in range(30):
        r = np.random.default_rng(k + 500)
        cx = r.uniform(-700, 2500)
        L.poli([(cx - 8, r.uniform(-300, 200)), (cx + 8, r.uniform(-300, 200)), (cx + 4, Y_SUELO), (cx - 4, Y_SUELO)], 0.16, alfa=0.25,
               blur=6)
    # espejo falso (izquierda)
    L.rect(-560, -360, 760, 700, 0.07, tex=0.05, grad=(0.03, -360, 340))
    L.poli([(-520, -330), (-300, -330), (-560, 120)], 0.22, alfa=0.35, tex=0.0)
    L.linea([(-560, -360), (200, -360), (200, 340), (-560, 340)], 6, 0.03, cerrado=True)
    L.rect(-580, 340, 800, 18, 0.18)
    # puerta con vidrio esmerilado
    L.rect(1900, -260, 380, Y_SUELO + 260, 0.18, tex=0.1)
    L.rect(1950, -200, 280, 300, 0.62, tex=0.05, emis=0.25)
    texto_lienzo(L, "INTERROGATORIO", 2090, -60, 30, tono=0.12, fuente="C:/Windows/Fonts/courbd.ttf", track=1, alfa=0.85)
    L.linea([(1900, -260), (2280, -260), (2280, Y_SUELO), (1900, Y_SUELO)], 3, 0.03, cerrado=True)
    L.elipse(1930, 400, 14, 14, 0.6)
    # tuberías del techo
    for yy, ww in ((-650, 30), (-600, 18)):
        L.rect(-700, yy, 3200, ww, 0.20, tex=0.06)
        L.linea([(-700, yy + ww), (2500, yy + ww)], 1.5, 0.03)
        L.linea([(-700, yy + 3), (2500, yy + 3)], 1.5, 0.55, alfa=0.5)
    _suelo_tablas(L, -700, 2500, Y_SUELO, 1100, tono=0.18)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def oficina():
    """Oficina del detective: zócalo de madera, papel pintado, ventana con persiana (ciudad detrás), archivero, perchero."""
    L = Lienzo(3000, 1700, origen=(-500, -600), base=0.0, sem=141)
    L.poli([(-500, -600), (2500, -600), (2500, Y_SUELO), (-500, Y_SUELO)], 0.30, tex=0.1, grad=(0.22, -600, Y_SUELO))
    for k in range(0, 3000, 60):                                   # papel pintado: rombos tenues
        for j in range(0, 1300, 80):
            x, y = -500 + k + (30 if (j // 80) % 2 else 0), -600 + j
            L.poli([(x, y - 14), (x + 9, y), (x, y + 14), (x - 9, y)], 0.36, alfa=0.35, tex=0.0, blur=0.8)
    _zocalo(L, -500, 2500, Y_SUELO, alto=300, tono=0.18)
    # ventana grande con la ciudad de noche detrás (se pinta la noche; la persiana es luz en la escena)
    L.rect(1100, -460, 900, 860, 0.10, tex=0.08)
    for k in range(9):
        r = np.random.default_rng(k + 600)
        bx = 1110 + k * 100
        L.rect(bx, -200 + r.uniform(0, 300), 90, 700, 0.14, tex=0.1)
        for j in range(10):
            if r.uniform() < 0.3:
                L.rect(bx + 14 + (j % 3) * 24, -150 + r.uniform(0, 500), 10, 14, 0.8, emis=0.5)
    L.linea([(1100, -460), (2000, -460), (2000, 400), (1100, 400)], 8, 0.03, cerrado=True)
    L.linea([(1550, -460), (1550, 400)], 6, 0.03)
    L.linea([(1100, -30), (2000, -30)], 6, 0.03)
    L.rect(1080, 400, 940, 24, 0.24)
    # archivero
    L.rect(-300, 360, 260, Y_SUELO - 360, 0.20, tex=0.1, grad=(0.12, 360, Y_SUELO))
    for k in range(4):
        L.rect(-286, 376 + k * 128, 232, 112, 0.24)
        L.rect(-196, 420 + k * 128, 52, 12, 0.6)
    # perchero con sombrero y gabardina de repuesto
    L.rect(400, -200, 12, Y_SUELO + 200, 0.08)
    L.elipse(406, -210, 70, 14, 0.12)
    L.poli([(406, -150), (360, 40), (380, 420), (440, 420), (452, 40)], 0.20, tex=0.1)
    texto_lienzo(L, "DETECTIVE PRIVADO", 760, -300, 40, tono=0.12, fuente="C:/Windows/Fonts/courbd.ttf", track=2, alfa=0.8)
    _suelo_tablas(L, -500, 2500, Y_SUELO, 1100, tono=0.22)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def escritorio():
    """Escritorio de madera visto desde arriba (pantalla completa, origen 0, 0): vetas, cerco de café, cenicero, pluma."""
    L = Lienzo(W + 400, H + 300, origen=(-200, -150), base=0.0, sem=151)
    L.poli([(-200, -150), (W + 200, -150), (W + 200, H + 150), (-200, H + 150)], 0.24, tex=0.12)
    r = np.random.default_rng(5)
    for k in range(70):
        y = r.uniform(-150, H + 150)
        P = [(-200, y)]
        for j in range(12):
            P.append((P[-1][0] + 200, y + 18 * math.sin(j * 0.7 + k) + r.uniform(-4, 4)))
        L.linea(P, r.uniform(0.8, 2.2), 0.10, alfa=0.5, jit=0.6, sem=k)
    for k in range(3):                                               # cercos de taza
        cx, cy = r.uniform(100, W - 100), r.uniform(100, H - 100)
        L.elipse(cx, cy, 70, 70, 0.12, alfa=0.3, rug=0.5, blur=2)
        L.elipse(cx, cy, 62, 62, 0.24, alfa=0.3, blur=2)
    L.elipse(W / 2 + 720, H / 2 - 300, 110, 110, 0.40, tex=0.05)     # cenicero
    L.elipse(W / 2 + 720, H / 2 - 300, 80, 80, 0.12, tex=0.1)
    L.poli([(W / 2 + 640, H / 2 - 290), (W / 2 + 720, H / 2 - 300), (W / 2 + 720, H / 2 - 290), (W / 2 + 640, H / 2 - 282)], 0.8)
    L.poli([(W / 2 - 760, H / 2 + 300), (W / 2 - 520, H / 2 + 120), (W / 2 - 510, H / 2 + 130), (W / 2 - 750, H / 2 + 312)], 0.08)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def corcho():
    """Tablero de corcho grande (2600 x 1500, origen -330, -210) con marco de madera, papeles viejos y huecos de chinchetas."""
    L = Lienzo(2600, 1500, origen=(-330, -210), base=0.0, sem=161)
    L.poli([(-330, -210), (2270, -210), (2270, 1290), (-330, 1290)], 0.22, tex=0.1)
    L.poli([(-280, -160), (2220, -160), (2220, 1240), (-280, 1240)], 0.46, tex=0.25, gran=0.12)
    r = np.random.default_rng(3)
    for k in range(900):                                             # granulado del corcho
        x, y = r.uniform(-280, 2220), r.uniform(-160, 1240)
        L.elipse(x, y, r.uniform(1, 4), r.uniform(1, 3), 0.30 if k % 2 else 0.58, alfa=0.7, blur=0.4)
    for k in range(14):                                              # recortes viejos clavados al fondo
        x, y = r.uniform(-200, 2100), r.uniform(-100, 1150)
        w_, h_ = r.uniform(140, 300), r.uniform(100, 220)
        a = r.uniform(-0.15, 0.15)
        c, s = math.cos(a), math.sin(a)
        P = [(x + dx * c - dy * s, y + dx * s + dy * c) for dx, dy in ((0, 0), (w_, 0), (w_, h_), (0, h_))]
        L.poli(P, r.uniform(0.62, 0.78), tex=0.06)
        for j in range(int(h_ // 22) - 1):
            L.linea([(P[0][0] + 14, P[0][1] + 20 + j * 22), (P[0][0] + w_ * 0.8, P[0][1] + 20 + j * 22)], 3, 0.35, alfa=0.6, jit=0.2)
    L.linea([(-280, -160), (2220, -160), (2220, 1240), (-280, 1240)], 8, 0.05, cerrado=True)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def cafeteria():
    """Cafetería nocturna (estilo «Nighthawks»): barra, cafeteras, estantes, menú, globos de luz y la ventana con lluvia y el letrero
    de neón al revés. Mundo: barra delantera en y = 700..900, suelo 900; ventana x -200..500."""
    L = Lienzo(2800, 1700, origen=(-400, -600), base=0.0, sem=171)
    L.poli([(-400, -600), (2400, -600), (2400, 900), (-400, 900)], 0.36, tex=0.1, grad=(0.26, -600, 900))
    for k in range(0, 2800, 46):                                     # azulejos
        L.linea([(-400 + k, 200), (-400 + k, 700)], 1.2, 0.2, alfa=0.5, jit=0.2)
    for j in range(200, 700, 46):
        L.linea([(-400, j), (2400, j)], 1.2, 0.2, alfa=0.5, jit=0.2)
    # ventana a la calle con lluvia (oscura) y letrero de neón visto al revés
    L.rect(-300, -420, 760, 560, 0.08, tex=0.1, grad=(0.04, -420, 140))
    for k in range(9):
        L.rect(-280 + k * 85, -200 + (k % 3) * 40, 60, 340, 0.12)
    texto_lienzo(L, "ÉFAC", 80, -320, 120, tono=0.92, fuente="C:/Windows/Fonts/impact.ttf", track=8)
    L.brillo(80, -320, 260, 0.5, ry=90, tono=0.9)
    L.linea([(-300, -420), (460, -420), (460, 140), (-300, 140)], 8, 0.03, cerrado=True)
    L.linea([(80, -420), (80, 140)], 6, 0.03)
    # estantes con tazas, cafeteras y el menú
    for yy in (-260, -120):
        L.rect(620, yy, 900, 14, 0.18)
        for k in range(10):
            L.poli([(650 + k * 86, yy), (690 + k * 86, yy), (686 + k * 86, yy - 40), (654 + k * 86, yy - 40)], 0.72, tex=0.05)
    for k, cx in enumerate((1640, 1820)):
        L.rect(cx - 70, -40, 140, 300, 0.62, tex=0.06, grad=(0.40, -40, 260))
        L.elipse(cx, -40, 70, 16, 0.75)
        L.rect(cx - 12, 200, 24, 40, 0.2)
        L.linea([(cx - 70, -40), (cx - 70, 260)], 2, 0.03)
        L.linea([(cx + 70, -40), (cx + 70, 260)], 2, 0.03)
        L.linea([(cx - 50, -30), (cx - 50, 250)], 3, 0.95, alfa=0.7)
    L.rect(1000, -520, 620, 220, 0.10, tex=0.08)
    texto_lienzo(L, "CAFÉ ........ 5¢", 1310, -470, 36, tono=0.85, fuente="C:/Windows/Fonts/courbd.ttf", track=2)
    texto_lienzo(L, "PAY ......... 10¢", 1310, -415, 36, tono=0.85, fuente="C:/Windows/Fonts/courbd.ttf", track=2)
    texto_lienzo(L, "ABIERTO TODA LA NOCHE", 1310, -355, 28, tono=0.85, fuente="C:/Windows/Fonts/courbd.ttf", track=2)
    # globos de luz
    for cx in (200, 900, 1600, 2200):
        L.linea([(cx, -600), (cx, -520)], 3, 0.05)
        L.elipse(cx, -480, 46, 46, 0.96, tex=0.0, emis=0.9)
    # barra: frente de lamas y tablero
    L.poli([(-400, 700), (2400, 700), (2400, 900), (-400, 900)], 0.22, tex=0.1, grad=(0.12, 700, 900))
    for k in range(0, 2800, 34):
        L.linea([(-400 + k, 712), (-400 + k, 890)], 2, 0.06, alfa=0.7, jit=0.2)
    L.rect(-400, 660, 2800, 44, 0.66, tex=0.06)
    L.linea([(-400, 660), (2400, 660)], 2.5, 0.95, alfa=0.8)
    L.linea([(-400, 704), (2400, 704)], 3, 0.03)
    L.poli([(-400, 900), (2400, 900), (2400, 1100), (-400, 1100)], 0.2, tex=0.14)
    for k in range(0, 2800, 120):                                    # suelo de damero
        for j in range(2):
            L.rect(-400 + k + 60 * j, 900 + 60 * j, 60, 60, 0.42, alfa=0.8)
    # enchufe en la pared (x 2100, y 380)
    L.rect(2050, 300, 100, 150, 0.8, tex=0.05)
    L.linea([(2050, 300), (2150, 300), (2150, 450), (2050, 450)], 2, 0.05, cerrado=True)
    return L.capa(opaco=True)
