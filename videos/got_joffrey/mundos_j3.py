# -*- coding: utf-8 -*-
"""Mundos pintados (3/3) de «¿Quién envenenó al rey?» (gris Lienzo; color con NC.pegar y la rampa indicada en VER()).

    puerto_cielo · puerto_barco (la galera fondeada con faroles) · puerto_muelle      -> la huida en la niebla
    cubierta (palo, jarcia, borda, el mar detrás)                                      -> la saeta de Meñique
    torre_dia (la cámara de la anciana, años después: luz gris de mañana)              -> la confesión
    puerta_cielo · puerta_ciudad (el puente y la puerta con rastrillo al alba)         -> caso cerrado
    mantel (cenital, lino blanco) · terciopelo (cenital, cojín) · tablero (cenital, roble)   -> planos de detalle
"""
import functools
import math

import numpy as np

import noir_feudal as NF
from noir import fbm
from noir_fondos import Lienzo


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== el puerto en la niebla
@functools.lru_cache(maxsize=1)
def puerto_cielo():
    L = Lienzo(3200, 1800, origen=(-640, -900), base=0.2, sem=611)
    L.rect(-640, -900, 3200, 1800, 0.18, tex=0.05, grad=(0.34, -900, 560))
    L.elipse(1700, -260, 60, 60, 0.9, tex=0, emis=0.5)
    L.brillo(1700, -260, 400, 0.5, tono=0.75)
    L.rect(-640, 560, 3200, 340, 0.22, tex=0.08, grad=(0.12, 560, 900))          # mar
    rng = _r(612)
    for k in range(120):
        x, y = rng.uniform(-600, 2500), rng.uniform(570, 880)
        L.linea([(x, y), (x + rng.uniform(40, 140), y)], 1.4, 0.4, alfa=0.45, jit=0.3)
    for k, x in enumerate((-300, 300, 2200)):                                     # otras naves lejanas, solo siluetas
        L.poli([(x - 120, 560), (x + 140, 560), (x + 110, 590), (x - 90, 590)], 0.14, alfa=0.7)
        L.linea([(x, 560), (x, 340)], 3, 0.14, alfa=0.7)
        L.poli([(x - 60, 360), (x + 70, 370), (x + 60, 520), (x - 50, 520)], 0.2, alfa=0.5)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def puerto_barco():
    """La galera de Meñique fondeada: casco con remos recogidos, castillo de popa con faroles, dos palos y velas recogidas."""
    L = Lienzo(2600, 1600, origen=(-200, -800), sem=621)
    cx = 1300
    casco = [(cx - 620, 470), (cx + 520, 470), (cx + 660, 360), (cx + 700, 330), (cx + 420, 600), (cx - 520, 600), (cx - 700, 400)]
    L.poli(casco, 0.20, tex=0.15)
    for k in range(5):
        L.linea([(cx - 640 + k * 10, 480 + k * 24), (cx + 560 - k * 30, 480 + k * 24)], 2.0, 0.08, alfa=0.8)
    for x in np.arange(cx - 480, cx + 420, 60):                                   # remos recogidos
        L.linea([(x, 520), (x + 50, 640)], 4, 0.12)
    L.poli([(cx - 700, 400), (cx - 520, 400), (cx - 520, 260), (cx - 720, 250)], 0.24, tex=0.12)   # castillo de popa
    for k, x in enumerate((cx - 690, cx - 600)):
        L.rect(x, 300, 40, 50, 0.85, tex=0.03, emis=0.9)
        L.brillo(x + 20, 325, 50, 0.3, tono=0.85)
    L.linea(casco, 3, 0.02, cerrado=True)
    for x, al in ((cx - 200, 900), (cx + 260, 760)):                              # palos, vergas, jarcia
        L.rect(x - 10, 470 - al, 20, al, 0.18, tex=0.1)
        L.linea([(x - 260, 470 - al * 0.82), (x + 260, 470 - al * 0.82)], 8, 0.14)
        L.poli([(x - 250, 470 - al * 0.82), (x + 250, 470 - al * 0.82), (x + 200, 470 - al * 0.74), (x - 200, 470 - al * 0.74)],
               0.42, tex=0.12)
        for sx in (-1, 1):
            L.linea([(x, 470 - al), (x + sx * 400, 470)], 1.4, 0.1, alfa=0.8, jit=0.2)
            L.linea([(x, 470 - al * 0.6), (x + sx * 300, 470)], 1.2, 0.1, alfa=0.7, jit=0.2)
    L.linea([(cx + 700, 330), (cx + 900, 200)], 6, 0.14)                          # bauprés
    L.rect(cx + 100, 50, 30, 40, 0.85, emis=0.9)                                  # farol del palo
    return L.capa()


@functools.lru_cache(maxsize=1)
def puerto_muelle():
    L = Lienzo(3400, 900, origen=(-740, 560), sem=631)
    for x in np.arange(-700, 600, 90):                                            # pilotes y tablones del muelle a la izquierda
        L.rect(x, 640, 24, 600, 0.2, tex=0.12)
        L.linea([(x, 640), (x, 1240)], 2, 0.02)
    L.poli([(-740, 620), (640, 620), (700, 680), (-740, 680)], 0.32, tex=0.12)
    for x in np.arange(-740, 640, 50):
        L.linea([(x, 620), (x + 6, 680)], 1.4, 0.08)
    L.linea([(-740, 620), (640, 620), (700, 680)], 2.4, 0.02)
    for k, x in enumerate((-400, 200)):                                           # norays con cabos y un farol de muelle
        L.rect(x, 560, 40, 60, 0.3, tex=0.1)
        L.linea([(x + 20, 580), (x + 260, 900)], 2.0, 0.15, jit=0.3)
    L.linea([(500, 620), (500, 380)], 6, 0.08)
    L.rect(480, 360, 40, 50, 0.85, emis=0.9)
    L.brillo(500, 385, 70, 0.35, tono=0.85)
    return L.capa()


# ====================================================================== la cubierta
@functools.lru_cache(maxsize=1)
def cubierta():
    L = Lienzo(3000, 1700, origen=(-540, -500), base=0.2, sem=641)
    L.rect(-540, -500, 3000, 1100, 0.26, tex=0.05, grad=(0.36, -500, 560))       # niebla clara del mar abierto
    L.rect(-540, 520, 3000, 120, 0.22, tex=0.08)
    rng = _r(642)
    for k in range(50):
        x, y = rng.uniform(-500, 2400), rng.uniform(530, 620)
        L.linea([(x, y), (x + rng.uniform(40, 120), y)], 1.2, 0.36, alfa=0.5)
    L.rect(-540, 600, 3000, 90, 0.22, tex=0.12)                                   # borda
    for x in np.arange(-540, 2460, 140):
        L.rect(x, 540, 22, 150, 0.18)
    L.linea([(-540, 600), (2460, 600)], 2.4, 0.02)
    L.rect(-540, 690, 3000, 600, 0.30, tex=0.12, grad=(0.22, 690, 1290))         # tablazón de la cubierta
    for y in np.arange(700, 1290, 46):
        L.linea([(-540, y), (2460, y)], 1.6, 0.1, alfa=0.8)
    for k in range(80):
        L.linea([(rng.uniform(-500, 2400), y0 := rng.uniform(700, 1280)), (rng.uniform(-500, 2400), y0)], 0.01, 0.1, alfa=0)
    L.rect(1500, -500, 40, 1200, 0.18, tex=0.1)                                   # palo mayor
    L.linea([(1500, -500), (1500, 700)], 2, 0.02)
    L.linea([(1540, -500), (1540, 700)], 2, 0.02)
    for sx in (-1, 1):
        L.linea([(1520, -480), (1520 + sx * 700, 600)], 2.0, 0.08, jit=0.3)
        L.linea([(1520, -200), (1520 + sx * 500, 600)], 1.6, 0.08, jit=0.3)
    for j in range(6):                                                            # flechastes
        y = -100 + j * 110
        L.linea([(1520 - (y + 480) / 1080 * 700, y), (1520 + (y + 480) / 1080 * 700, y)], 1.2, 0.08, alfa=0.7)
    L.rect(300, 640, 160, 120, 0.26, tex=0.15)                                    # barriles y rollos de cabo
    L.elipse(700, 760, 90, 30, 0.3, tex=0.1)
    for r in (80, 60, 40):
        L.linea(np.array([(700 + r * math.cos(a), 760 + r * 0.33 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 30)]), 3, 0.12,
                cerrado=True)
    return L.capa(opaco=True)


# ====================================================================== la cámara de la anciana, años después
@functools.lru_cache(maxsize=1)
def torre_dia():
    L = Lienzo(2800, 1500, origen=(-440, -300), base=0.3, sem=651)
    NF.sillares(L, -440, -300, 2800, 1500, 0.34, hilada=56, largo=(100, 190), sem=652)
    # ventana geminada con luz gris de mañana y un tapiz verde con flores
    for x in (1180, 1420):
        L.poli([(x, 520), (x, 40), (x + 90, -40), (x + 180, 40), (x + 180, 520)], 0.8, tex=0.03, emis=0.6)
        L.linea([(x, 520), (x, 40), (x + 90, -40), (x + 180, 40), (x + 180, 520)], 4, 0.02, cerrado=True)
        for yy in np.arange(60, 520, 50):
            L.linea([(x, yy), (x + 180, yy)], 1.2, 0.2, alfa=0.6)
    L.rect(1160, 520, 460, 40, 0.42, tex=0.08)
    L.rect(-200, -200, 520, 760, 0.36, tex=0.18)
    rng = _r(653)
    for k in range(40):
        L.elipse(-180 + rng.uniform(0, 480), -180 + rng.uniform(0, 720), 14, 14, rng.choice([0.6, 0.5]), alfa=0.8)
    L.linea([(-200, -200), (320, -200), (320, 560), (-200, 560)], 2.4, 0.02, cerrado=True)
    # suelo, alfombra, mesa con jarra y la silla de respaldo alto
    L.rect(-440, 820, 2800, 500, 0.30, tex=0.12)
    L.poli([(200, 880), (1500, 880), (1700, 1200), (0, 1200)], 0.36, tex=0.15)
    L.rect(500, 640, 520, 30, 0.36, tex=0.1)
    L.rect(520, 670, 30, 220, 0.2)
    L.rect(970, 670, 30, 220, 0.2)
    L.linea([(500, 640), (1020, 640), (1020, 670), (500, 670)], 2.2, 0.02, cerrado=True)
    L.poli([(640, 640), (634, 570), (650, 540), (690, 540), (706, 570), (700, 640)], 0.42, tex=0.08)
    return L.capa(opaco=True)


# ====================================================================== la puerta de la ciudad al alba
@functools.lru_cache(maxsize=1)
def puerta_cielo():
    L = Lienzo(3200, 1800, origen=(-640, -900), base=0.4, sem=661)
    L.rect(-640, -900, 3200, 1800, 0.3, tex=0.05, grad=(0.62, -900, 600))
    L.brillo(1700, 500, 700, 0.55, tono=0.95)
    rng = _r(662)
    for k in range(16):
        cx, cy = rng.uniform(-600, 2500), rng.uniform(-850, 300)
        L.elipse(cx, cy, rng.uniform(240, 520), rng.uniform(16, 40), rng.uniform(0.4, 0.6), alfa=0.5, rug=1.2, blur=8)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def puerta_ciudad():
    L = Lienzo(3600, 2200, origen=(-840, -1100), sem=671)
    NF.muralla(L, -840, 2760, 820, 520, tono=0.26, sem=672, encendidas=0.2)
    for cx in (560, 1360):
        NF.torre(L, cx, 820, 300, 900, techo="almenas", sem=673 + cx, encendidas=0.3)
    # arco de la puerta con el rastrillo medio alzado
    x0, x1 = 760, 1160
    L.poli([(x0, 820), (x0, 560), (960, 420), (x1, 560), (x1, 820)], 0.06, tex=0.1)
    for x in np.arange(x0 + 20, x1, 44):
        L.rect(x, 440, 10, 260, 0.2)
    for y in np.arange(460, 700, 44):
        L.rect(x0, y, x1 - x0, 8, 0.2)
    L.linea([(x0, 820), (x0, 560), (960, 420), (x1, 560), (x1, 820)], 4, 0.02)
    # puente de piedra con pretiles y el foso
    L.poli([(-840, 820), (2760, 820), (2760, 1100), (-840, 1100)], 0.14, tex=0.1)
    L.poli([(700, 820), (1220, 820), (1500, 1100), (420, 1100)], 0.34, tex=0.12)
    L.linea([(700, 820), (420, 1100)], 3, 0.02)
    L.linea([(1220, 820), (1500, 1100)], 3, 0.02)
    return L.capa()


# ====================================================================== fondos de detalle (cenitales)
@functools.lru_cache(maxsize=1)
def mantel():
    L = Lienzo(2600, 1600, origen=(-340, -260), base=0.7, sem=681)
    rng = _r(682)
    for k in range(30):
        x = rng.uniform(-300, 2200)
        L.linea([(x, -260), (x + rng.uniform(-60, 60), 1340)], rng.uniform(2, 6), 0.55, alfa=0.35, jit=1.0)
    L.rect(-340, 500, 2600, 24, 0.6, alfa=0.5)                                    # dobladillo bordado
    for x in np.arange(-340, 2260, 40):
        L.elipse(x, 512, 8, 8, 0.5, alfa=0.6)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 240, 3, 683))
    L.g *= (0.9 + 0.15 * n).astype(np.float32)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def terciopelo():
    L = Lienzo(2600, 1600, origen=(-340, -260), base=0.3, sem=691)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 380, 3, 692))
    L.g[:] = (0.22 + 0.2 * n).astype(np.float32)
    rng = _r(693)
    for k in range(12):                                                           # pliegues del cojín
        x = rng.uniform(-200, 2100)
        L.linea([(x, -260), (x + rng.uniform(-200, 200), 1340)], rng.uniform(10, 30), 0.14, alfa=0.35, jit=4)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def tablero():
    L = Lienzo(2600, 1600, origen=(-340, -260), base=0.24, sem=701)
    rng = _r(702)
    for xx in np.arange(-340, 2260, 280):
        L.rect(xx, -260, 280, 1600, 0.24 + rng.uniform(-0.04, 0.04), tex=0.1)
        L.linea([(xx, -260), (xx, 1340)], 3.0, 0.04, alfa=0.9)
        for j in range(16):
            x0 = xx + rng.uniform(12, 268)
            P = np.array([(x0 + 8 * math.sin(y * 0.008 + j), y) for y in np.linspace(-260, 1340, 40)])
            L.linea(P, rng.uniform(0.8, 2.0), 0.13, alfa=0.5, jit=0.3)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 220, 3, 703))
    L.g *= (0.85 + 0.25 * n).astype(np.float32)
    return L.capa(opaco=True)


def VER(h, amb):
    import noir_color as NC

    def puerto():
        h.camara(1.0, 960, 400)
        NC.pegar(puerto_cielo(), h, 0.1, rampa="lejos")
        NC.pegar(puerto_barco(), h, 0.5, rampa="madera", bruma=0.35)
        NC.pegar(puerto_muelle(), h, 1.0, rampa="madera")
        amb(0.8)

    def cubierta_():
        h.camara(1.0, 960, 540)
        NC.pegar(cubierta(), h, 1.0, rampa="madera")
        amb(0.6)
        h.luz_radial(900, 500, 900, h.pal["antorcha"], k=0.9)

    def torre():
        h.camara(1.0, 960, 540)
        NC.pegar(torre_dia(), h, 1.0, rampa="muralla", col_emis=h.pal["luna"])
        amb(0.9)
        h.luz_radial(1400, 300, 1100, h.pal["luna"], k=0.9)

    def puerta():
        h.camara(1.0, 960, 400)
        NC.pegar(puerta_cielo(), h, 0.1, rampa="whisky")
        NC.pegar(puerta_ciudad(), h, 0.8, rampa="muralla", bruma=0.15)
        amb(0.9)

    def det():
        h.camara(1.0, 960, 540)
        NC.pegar(mantel(), h, 1.0, rampa="papel")
        amb(0.5)
        h.luz_radial(960, 400, 900, h.pal["vela"], k=1.0)

    def det2():
        h.camara(1.0, 960, 540)
        NC.pegar(terciopelo(), h, 1.0, rampa="purpura")
        amb(0.5)
        h.luz_radial(960, 400, 900, h.pal["vela"], k=1.0)
    return dict(puerto=puerto, cubierta=cubierta_, torre=torre, puerta=puerta, mantel=det, terciopelo=det2)
