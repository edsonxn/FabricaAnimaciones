# -*- coding: utf-8 -*-
"""Fondos cacheados del video del chicle (uno por proceso; se copian en cada cuadro).
    patio()        parque al atardecer: cielo, árboles lejanos, columpio, banca y pasto en primer plano (3 planos)
    selva()        selva del sureste: troncos lejanos azulados, lianas, helechos al frente y un chicozapote grande
    papel(nombre)  hojas de color para los planos «de pizarrón»
    perfil()       corte lateral de la cabeza y el cuello (boca, lengua, tráquea, esófago) sobre papel rosado
    estomago()     el interior del estómago: pliegues, luz cálida y el lago de jugo gástrico
    tunel(nombre)  interior del intestino (delgado: rosado con vellosidades al fondo · grueso: más oscuro y ancho)
"""
import math

import numpy as np

from acuarela import H, W, brillo, cinta, curva, degradado, elipse, forma, lavado, linea, mancha_pts, rgb, rrect
from comun import cache
from personajes import BLANCO


def _manchas(im, col, n, seed, r=(200, 380), alfa=0.22, y=(0, H)):
    rg = np.random.default_rng(seed)
    for k in range(n):
        lavado(im, mancha_pts(rg.uniform(0, W), rg.uniform(*y), rg.uniform(*r), seed + k, 0.3), col, alfa, seed + k, humedo=16)


def _arbol(im, x, y, s, col, seed, tronco=None):
    tronco = rgb("7a5636") if tronco is None else tronco
    forma(im, cinta([(x, y), (x + 6 * s, y - 120 * s), (x - 4 * s, y - 220 * s)], 34 * s, 20 * s), tronco, 0, seed, tinta=3.4 * s)
    for k in range(5):
        a = k * 1.25
        forma(im, mancha_pts(x + 70 * s * math.cos(a), y - 260 * s + 50 * s * math.sin(a), 90 * s, seed + 1 + k, 0.2),
              col, 0, seed + 1 + k, tinta=3.4 * s, sombra=(col * 0.72, 10, 10, 0.5))


def _patio():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("9cc9e3"), rgb("f8d39a"), 0, 700)
    for k, (x, y, r) in enumerate([(300, 160, 110), (900, 110, 80), (1560, 190, 130)]):
        lavado(im, mancha_pts(x, y, r, 30 + k, 0.35, ry=r * 0.4), BLANCO, 0.6, 30 + k, humedo=10)
    lavado(im, np.array([(0, 640), (300, 560), (700, 610), (1100, 540), (1500, 600), (1920, 560), (1920, 760), (0, 760)],
                        np.float32), rgb("8fa6c8"), 0.6, 40)                                        # cerros lejanos
    for k in range(9):                                                                              # árboles lejanos
        _arbol(im, 80 + k * 230, 700, 0.55 + 0.1 * (k % 3), rgb("7fae7a"), 60 + 7 * k)
    im[700:] = rgb("9bc46a")
    _manchas(im, rgb("6f9a4a"), 8, 120, (160, 300), 0.3, (720, H))
    # columpio (plano medio, a la derecha)
    cx = 1560
    for d in (-1, 1):
        linea(im, [(cx + d * 170, 740), (cx + d * 120, 380)], 14, col=rgb("c0504a"), seed=140 + d, t=0, punta=False)
    linea(im, [(cx - 140, 380), (cx + 140, 380)], 16, col=rgb("c0504a"), seed=143, t=0, punta=False)
    for d in (-1, 1):
        linea(im, [(cx + d * 50, 380), (cx + d * 50, 600)], 4, seed=150 + d, t=0, punta=False)
    forma(im, rrect(cx, 606, 140, 18, 6), rgb("a86e3c"), 0, 153, tinta=3.4)
    # banca (primer plano izquierdo) y pasto delantero
    forma(im, rrect(330, 830, 520, 34, 8), rgb("a86e3c"), 0, 160, tinta=4, sombra=(rgb("7a4a2a"), 0, 8, 0.5))
    forma(im, rrect(330, 760, 520, 30, 8), rgb("b97e48"), 0, 161, tinta=4)
    for d in (-1, 1):
        forma(im, rrect(330 + d * 220, 900, 22, 120, 4), rgb("4b4b4b"), 0, 162 + d, tinta=3.4)
    for k in range(40):
        x = (k * 53) % W
        linea(im, [(x, H + 10), (x + 10 * math.sin(k), H - 40 - 30 * ((k * 7) % 3))], 6, col=rgb("5e8a3a"), seed=200 + k, t=0)
    return im


def patio():
    return cache("patio", _patio).copy()


def _selva():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("cfe3c4"), rgb("7fa874"))
    for k in range(12):                                                                             # troncos lejanos
        x = 60 + k * 170 + 30 * math.sin(k * 3)
        lavado(im, rrect(x, H / 2, 40 + 10 * (k % 3), H + 100, 10), rgb("6f8a86"), 0.45, 300 + k)
    _manchas(im, rgb("4f7f4a"), 10, 320, (180, 320), 0.35, (0, 400))
    for k in range(6):                                                                              # lianas
        x = 200 + k * 300
        linea(im, curva([(x, -20), (x + 40, 300), (x - 20, 600)], 8), 6, col=rgb("4f6f3a"), seed=340 + k, t=0, alfa=0.7)
    # chicozapote grande a la derecha con corteza rugosa
    forma(im, curva([(1300, H + 40), (1330, 600), (1350, 200), (1340, -40), (1620, -40), (1600, 220), (1610, 640), (1660, H + 40)],
                    8, True), rgb("8a6a4e"), 0, 360, tinta=5, sombra=(rgb("5a4030"), 30, 0, 0.6), luz=(BLANCO, -40, 0, 0.12))
    for k in range(16):
        y = 40 + k * 64
        linea(im, curva([(1360, y), (1440, y + 10 + 6 * math.sin(k)), (1590, y - 4)], 5), 2.6, col=rgb("5a4030"), seed=370 + k,
              t=0, alfa=0.5, punta=False)
    # helechos al frente
    for k in range(9):
        bx = k * 240 - 40
        for j in range(5):
            a = -math.pi / 2 + (j - 2) * 0.45
            forma(im, cinta([(bx, H + 20), (bx + 140 * math.cos(a), H - 120 + 60 * math.sin(a) * 2),
                             (bx + 220 * math.cos(a), H - 170 + 90 * math.sin(a))], 36, 6), rgb("4f8a46"), 0, 400 + 9 * k + j,
                  tinta=3, sombra=(rgb("356a32"), 6, 0, 0.5))
    return im


def selva():
    return cache("selva", _selva).copy()


def _papel(col_a, col_b, seed):
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, col_a, col_b)
    _manchas(im, col_b, 10, seed, (220, 420), 0.25)
    return im


def papel(nombre):
    cols = {"calido": (rgb("f7ecd4"), rgb("ecd6ae")), "frio": (rgb("e6f0ec"), rgb("c9ddd8")),
            "rosa": (rgb("f8e6dc"), rgb("efcdbd")), "sepia": (rgb("efe0c0"), rgb("d9c08e"))}
    a, b = cols[nombre]
    return cache(("papel", nombre), lambda: _papel(a, b, 40 + len(nombre))).copy()


# ------------------------------------------------------------ dentro del cuerpo
PIEL_C = rgb("f4cfae")
CARNE = rgb("e98f8a")
CARNE_OSC = rgb("b65a5d")


def _perfil():
    """Corte lateral de cabeza y cuello mirando a la DERECHA. Boca en (1180, 470); esófago baja por x≈930."""
    im = _papel(rgb("f8e6dc"), rgb("efcdbd"), 90)
    cab = curva([(760, 120), (1040, 60), (1250, 180), (1330, 360), (1350, 470), (1290, 560), (1240, 620), (1150, 660),
                 (1050, 700), (1040, 1120), (720, 1120), (700, 700), (620, 520), (640, 280)], 8, True)
    forma(im, cab, PIEL_C, 0, 500, tinta=6, sombra=(rgb("d9967a"), 30, 0, 0.5))
    # cavidad de la boca y faringe (rosa oscuro)
    cav = curva([(1300, 440), (1150, 410), (1000, 420), (930, 470), (900, 600), (900, 1120), (980, 1120), (990, 640),
                 (1030, 540), (1150, 520), (1290, 520)], 8, True)
    forma(im, cav, CARNE_OSC, 0, 510, tinta=4.4)
    # tráquea (delante del esófago, hacia la derecha) en azul pálido
    forma(im, curva([(1000, 640), (1060, 640), (1060, 1120), (1000, 1120)], 4, True), rgb("bcd3e6"), 0, 520, tinta=3.6)
    for k in range(8):
        linea(im, [(1004, 700 + k * 52), (1056, 700 + k * 52)], 3, col=rgb("8aa6c0"), seed=521 + k, t=0, alfa=0.7)
    # lengua
    forma(im, curva([(1270, 520), (1150, 500), (1040, 520), (1000, 600), (1040, 650), (1160, 610), (1270, 560)], 7, True),
          rgb("e86f7a"), 0, 530, tinta=4.2, luz=(BLANCO, -10, -14, 0.25))
    # paladar y dientes
    for k in range(4):
        forma(im, rrect(1270 - k * 30, 436, 26, 30, 8), BLANCO, 0, 540 + k, tinta=2.6)
        forma(im, rrect(1270 - k * 30, 528, 26, 26, 8), BLANCO, 0, 545 + k, tinta=2.6)
    # cerebro tenue y oreja (contexto)
    lavado(im, mancha_pts(900, 260, 180, 560, 0.15, ry=110), rgb("f2b6c0"), 0.45, 560)
    forma(im, elipse(820, 430, 34, 54), PIEL_C, 0, 561, tinta=3.6)
    forma(im, elipse(1220, 300, 16, 22), rgb("2a2220"), 0, 562, tinta=0)                     # ojo
    linea(im, curva([(1185, 255), (1220, 245), (1255, 258)], 4), 6, seed=563, t=0)              # ceja
    forma(im, curva([(1320, 330), (1385, 400), (1330, 410)], 5, True), PIEL_C, 0, 564, tinta=4)  # nariz
    lavado(im, elipse(1190, 380, 40, 22), rgb("f08a9a"), 0.5, 565)                              # chapeta
    return im


def perfil():
    return cache("perfil", _perfil).copy()


def _estomago():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("d97a7c"), rgb("8e3f4a"))
    _manchas(im, rgb("6e2c3a"), 9, 600, (200, 380), 0.3)
    for k in range(9):                                                                       # pliegues (rugosidades)
        y = 120 + k * 70
        linea(im, curva([(-40, y), (400, y - 40 + 20 * math.sin(k)), (900, y + 30), (1400, y - 30), (W + 40, y + 10)], 8),
              22 - k, col=rgb("f0a0a0"), seed=610 + k, t=0, alfa=0.35)
        linea(im, curva([(-40, y + 14), (400, y - 26 + 20 * math.sin(k)), (900, y + 44), (1400, y - 16), (W + 40, y + 24)], 8),
              8, col=rgb("6e2c3a"), seed=620 + k, t=0, alfa=0.35)
    # lago de jugo gástrico
    forma(im, curva([(-40, 760), (500, 730), (1000, 770), (1500, 735), (W + 40, 760), (W + 40, H + 40), (-40, H + 40)], 8, True),
          rgb("c7c24a"), 0, 640, tinta=5, luz=(BLANCO, 0, -30, 0.25), sombra=(rgb("8a8a2a"), 0, 40, 0.5))
    brillo(im, W / 2, 300, 600, rgb("ffcf9a"), 0.12)
    # la salida (píloro) a la derecha: anillo oscuro
    forma(im, elipse(1790, 470, 120, 170), rgb("5a1f2c"), 0, 650, tinta=5)
    lavado(im, elipse(1800, 470, 70, 120), rgb("1e0a10"), 0.8, 651)
    return im


def estomago():
    return cache("estomago", _estomago).copy()


def _tunel(nombre):
    grueso = nombre == "grueso"
    im = np.zeros((H, W, 3), np.float32)
    a, b = (rgb("b9776a"), rgb("5e3530")) if grueso else (rgb("f0a39a"), rgb("a8505a"))
    # túnel en perspectiva: anillos concéntricos hacia el punto de fuga
    degradado(im, a, b)
    cx, cy = 980, 520
    for k in range(10, 0, -1):
        r = 80 + k * 110
        col = b * (0.6 + 0.04 * k) + a * (0.04 * k)
        forma(im, elipse(cx, cy, r * 1.25, r * 0.85), col, 0, 700 + k + (50 if grueso else 0), tinta=3 + 0.3 * k,
              alfa=0.55)
    lavado(im, elipse(cx, cy, 90, 60), rgb("1e0a10"), 0.85, 720)
    if not grueso:                                                                          # vellosidades del fondo
        rg = np.random.default_rng(730)
        for anillo in range(4):
            r0 = 230 + anillo * 150
            for j in range(22):
                ang = j * 2 * math.pi / 22 + anillo * 0.4 + rg.uniform(-0.05, 0.05)
                x0, y0 = cx + r0 * 1.25 * math.cos(ang), cy + r0 * 0.85 * math.sin(ang)
                L = 26 + r0 * 0.1
                pts = [(x0, y0), (x0 - L * math.cos(ang), y0 - L * 0.8 * math.sin(ang))]
                forma(im, cinta(pts, 14 + r0 * 0.04, 9 + r0 * 0.03), rgb("f6b2a6"), 0, 740 + anillo * 30 + j, tinta=1.4 + r0 * 0.002,
                      alfa=0.9, luz=(BLANCO, -2, -2, 0.25))
    else:
        _manchas(im, rgb("3a2018"), 8, 760, (150, 280), 0.3)
    brillo(im, cx, cy + 300, 500, rgb("ffcf9a"), 0.08)
    return im


def tunel(nombre):
    return cache(("tunel", nombre), lambda: _tunel(nombre)).copy()
