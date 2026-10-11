# -*- coding: utf-8 -*-
"""Mundos pintados (2/3) de «¿Quién envenenó al rey?» (gris Lienzo; color con NC.pegar y la rampa indicada en VER()).

    celda_muro · celda_suelo · celda_reja (barrotes en primer plano)         -> el acusado en la mazmorra
    botica_estantes · botica_mesa                                            -> el veneno (mesa del maestre)
    jardin_cielo · jardin_arboles · jardin_suelo                             -> Dontos le regala el collar (jardín de noche)
    terraza_fondo · terraza_balaustrada                                      -> la anciana le acomoda el collar (terraza de la boda)
    rosal_cielo · rosal                                                      -> la Reina de las Espinas (rosaleda al atardecer)
    contaduria                                                               -> Meñique entre libros de cuentas y monedas
"""
import functools
import math

import numpy as np

import noir_feudal as NF
from noir import fbm
from noir_fondos import Lienzo


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== la mazmorra
@functools.lru_cache(maxsize=1)
def celda_muro():
    L = Lienzo(2800, 1600, origen=(-440, -300), base=0.18, sem=411)
    NF.sillares(L, -440, -300, 2800, 1600, 0.2, hilada=70, largo=(120, 220), sem=412, var=0.07)
    rng = _r(413)
    for k in range(26):                                                           # humedad y musgo que chorrea
        x = rng.uniform(-400, 2300)
        L.poli([(x - 20, -300), (x + 20, -300), (x + rng.uniform(-10, 10), rng.uniform(100, 700))], 0.1, alfa=0.45, rug=1.0, blur=4)
    # ventanuco con barrotes arriba (la luna entra)
    L.rect(1240, -120, 220, 130, 0.62, tex=0.04, emis=0.45)
    for x in np.arange(1262, 1460, 40):
        L.rect(x, -120, 9, 130, 0.05)
    L.linea([(1240, -120), (1460, -120), (1460, 10), (1240, 10)], 3, 0.02, cerrado=True)
    # argollas y cadenas en la pared
    for x in (300, 760):
        L.elipse(x, 260, 22, 22, 0.04, alfa=0.0)
        L.linea(np.array([(x + 22 * math.cos(a), 260 + 22 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 20)]), 6, 0.08,
                cerrado=True)
        for j in range(9):
            y = 290 + j * 26
            L.linea(np.array([(x - 8 + 3 * math.sin(j), y), (x + 8, y + 14)]), 5, 0.08)
    # banco de piedra y cántaro
    L.rect(-200, 700, 900, 80, 0.30, tex=0.12)
    L.rect(-200, 780, 900, 200, 0.14, tex=0.12)
    L.linea([(-200, 700), (700, 700), (700, 780), (-200, 780)], 2.4, 0.02, cerrado=True)
    L.poli([(1500, 940), (1490, 860), (1520, 820), (1580, 820), (1610, 860), (1600, 940)], 0.30, tex=0.15)
    L.linea([(1500, 940), (1490, 860), (1520, 820), (1580, 820), (1610, 860), (1600, 940)], 2.2, 0.02, cerrado=True)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def celda_suelo():
    L = Lienzo(2800, 600, origen=(-440, 900), sem=421)
    L.rect(-440, 900, 2800, 600, 0.16, tex=0.15)
    rng = _r(422)
    for k in range(260):                                                          # paja
        x, y = rng.uniform(-400, 2300), rng.uniform(910, 1400)
        a = rng.uniform(-0.6, 0.6)
        L.linea([(x, y), (x + 40 * math.cos(a), y + 10 * math.sin(a))], 1.6, rng.uniform(0.35, 0.55), alfa=0.8, jit=0.2)
    return L.capa()


@functools.lru_cache(maxsize=1)
def celda_reja():
    """Barrotes de hierro remachados en primer plano (la cámara está fuera de la celda)."""
    L = Lienzo(2800, 1800, origen=(-440, -400), sem=431)
    for x in np.arange(-300, 2300, 230):
        L.rect(x, -400, 34, 1800, 0.26, tex=0.08)
        L.rect(x + 22, -400, 12, 1800, 0.12)
        L.linea([(x, -400), (x, 1400)], 2.4, 0.02)
        L.linea([(x + 34, -400), (x + 34, 1400)], 2.4, 0.02)
    for y in (-60, 980):
        L.rect(-440, y, 2800, 40, 0.24, tex=0.08)
        L.linea([(-440, y), (2360, y)], 2.4, 0.02)
        for x in np.arange(-300, 2300, 230):
            L.elipse(x + 17, y + 20, 8, 8, 0.4)
    return L.capa()


# ====================================================================== la botica del maestre
@functools.lru_cache(maxsize=1)
def botica_estantes():
    L = Lienzo(2800, 1400, origen=(-440, -300), base=0.16, sem=441)
    for x in np.arange(-440, 2360, 300):                                          # tablones del muro
        L.rect(x, -300, 300, 1400, 0.18 + 0.03 * math.sin(x), tex=0.12)
        L.linea([(x, -300), (x, 1100)], 2, 0.05)
    rng = _r(442)
    for k, y in enumerate((-180, 80, 340)):                                       # tres baldas llenas de frascos y libros
        L.rect(-440, y + 160, 2800, 22, 0.32, tex=0.1)
        L.linea([(-440, y + 160), (2360, y + 160)], 2.2, 0.02)
        x = -400
        while x < 2300:
            tipo = rng.integers(3)
            if tipo == 0:                                                         # frasco
                w = rng.uniform(40, 80)
                hh = rng.uniform(70, 140)
                L.poli([(x, y + 160), (x, y + 160 - hh * 0.7), (x + w * 0.3, y + 160 - hh * 0.8), (x + w * 0.3, y + 160 - hh),
                        (x + w * 0.7, y + 160 - hh), (x + w * 0.7, y + 160 - hh * 0.8), (x + w, y + 160 - hh * 0.7), (x + w, y + 160)],
                       rng.uniform(0.3, 0.55), tex=0.05)
                L.linea([(x + w * 0.2, y + 160 - hh * 0.6), (x + w * 0.2, y + 150)], 2.0, 0.75, alfa=0.5)
                L.rect(x + w * 0.15, y + 160 - hh * 0.45, w * 0.7, hh * 0.22, 0.7, tex=0.04)      # etiqueta
                x += w + rng.uniform(6, 20)
            elif tipo == 1:                                                       # libros
                for j in range(int(rng.integers(3, 8))):
                    w = rng.uniform(18, 34)
                    hh = rng.uniform(100, 150)
                    L.rect(x, y + 160 - hh, w, hh, rng.uniform(0.15, 0.4), tex=0.1)
                    L.linea([(x, y + 160 - hh), (x + w, y + 160 - hh), (x + w, y + 160), (x, y + 160)], 1.4, 0.03, cerrado=True)
                    L.linea([(x + 3, y + 160 - hh * 0.8), (x + w - 3, y + 160 - hh * 0.8)], 1.6, 0.6, alfa=0.6)
                    x += w + 2
                x += 14
            else:                                                                 # mortero y cráneo de animal
                L.poli([(x, y + 160), (x + 10, y + 100), (x + 90, y + 100), (x + 100, y + 160)], 0.34, tex=0.1)
                L.linea([(x + 70, y + 110), (x + 120, y + 40)], 8, 0.4)
                x += 140
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def botica_mesa():
    L = Lienzo(2800, 700, origen=(-440, 700), sem=451)
    L.rect(-440, 760, 2800, 640, 0.30, tex=0.12, grad=(0.20, 760, 1400))
    rng = _r(452)
    for j in range(40):
        y = rng.uniform(770, 1380)
        L.linea([(-440, y), (2360, y + rng.uniform(-6, 6))], rng.uniform(0.8, 1.8), 0.15, alfa=0.5)
    L.linea([(-440, 760), (2360, 760)], 2.4, 0.02)
    # libro abierto con láminas de plantas, balanza y pergaminos
    L.poli([(-260, 900), (60, 880), (80, 1060), (-240, 1080)], 0.70, tex=0.05)
    L.poli([(60, 880), (380, 900), (360, 1080), (80, 1060)], 0.68, tex=0.05)
    for j in range(8):
        L.linea([(-220, 920 + j * 18), (20, 906 + j * 18)], 1.2, 0.3, alfa=0.6)
    L.elipse(240, 980, 60, 40, 0.5, alfa=0.6, rug=1.0)
    for j in range(5):
        L.linea([(240, 1000), (200 + j * 20, 940)], 1.6, 0.25)
    L.linea([(-260, 900), (60, 880), (380, 900), (360, 1080), (80, 1060), (-240, 1080)], 2.0, 0.02, cerrado=True)
    L.linea([(60, 880), (80, 1060)], 1.6, 0.05)
    return L.capa()


# ====================================================================== el jardín de noche (Dontos y el collar)
@functools.lru_cache(maxsize=1)
def jardin_cielo():
    L = Lienzo(3200, 1800, origen=(-640, -900), base=0.1, sem=461)
    L.rect(-640, -900, 3200, 1800, 0.06, grad=(0.34, -900, 700))
    L.elipse(1500, -300, 90, 90, 0.97, tex=0, emis=0.75)
    L.brillo(1500, -300, 420, 0.42, tono=0.85)
    rng = _r(462)
    for k in range(18):
        cx, cy = rng.uniform(-600, 2500), rng.uniform(-850, 300)
        L.elipse(cx, cy, rng.uniform(200, 500), rng.uniform(20, 50), rng.uniform(0.12, 0.3), alfa=0.5, rug=1.3, blur=10)
    NF.muralla(L, -640, 2560, 640, 260, tono=0.2, sem=463, encendidas=0.3)
    NF.torre(L, 300, 640, 160, 640, techo="conico", sem=464, encendidas=0.5)
    return L.capa(opaco=True)


def _arbol(L, x, base, alto, sem, tono=0.24):
    rng = _r(sem)
    L.poli([(x - 40, base), (x - 24, base - alto * 0.5), (x - 10, base - alto * 0.62), (x + 14, base - alto * 0.62),
            (x + 26, base - alto * 0.5), (x + 50, base)], tono + 0.04, tex=0.2)
    for k in range(7):                                                            # ramas
        a = -math.pi / 2 + rng.uniform(-1.1, 1.1)
        x0, y0 = x + rng.uniform(-14, 14), base - alto * rng.uniform(0.45, 0.62)
        L.linea([(x0, y0), (x0 + math.cos(a) * alto * 0.3, y0 + math.sin(a) * alto * 0.3)], rng.uniform(6, 14), tono, jit=1.5)
    for k in range(16):                                                           # copa en masas de hojas
        L.elipse(x + rng.uniform(-alto * 0.32, alto * 0.32), base - alto * rng.uniform(0.62, 1.0), rng.uniform(60, 130),
                 rng.uniform(40, 90), tono + rng.uniform(-0.04, 0.08), alfa=0.95, rug=1.6, blur=1.5, tex=0.25)
    for k in range(40):
        L.elipse(x + rng.uniform(-alto * 0.35, alto * 0.35), base - alto * rng.uniform(0.6, 1.05), rng.uniform(8, 16),
                 rng.uniform(5, 10), tono + 0.2, alfa=0.6, rug=1.0)


@functools.lru_cache(maxsize=1)
def jardin_arboles():
    L = Lienzo(3600, 2000, origen=(-840, -1100), sem=471)
    for k, (x, al) in enumerate(((-500, 1300), (200, 1000), (1700, 1200), (2400, 1400))):
        _arbol(L, x, 900, al, 472 + k)
    rng = _r(479)
    for k in range(14):                                                           # setos
        x = rng.uniform(-800, 2700)
        L.elipse(x, 880, rng.uniform(100, 180), rng.uniform(50, 80), 0.26, alfa=0.95, rug=1.5, tex=0.25)
    # fuente de piedra en el centro
    L.elipse(980, 860, 220, 40, 0.34, tex=0.1)
    L.rect(760, 860, 440, 70, 0.30, tex=0.1)
    L.elipse(980, 860, 190, 30, 0.6, tex=0.03, emis=0.2)
    L.rect(960, 700, 40, 160, 0.34, tex=0.1)
    L.elipse(980, 700, 70, 16, 0.36)
    L.linea([(760, 860), (760, 930), (1200, 930), (1200, 860)], 2.4, 0.02)
    return L.capa()


@functools.lru_cache(maxsize=1)
def jardin_suelo():
    L = Lienzo(3600, 800, origen=(-840, 880), sem=481)
    L.rect(-840, 900, 3600, 700, 0.18, tex=0.2, grad=(0.24, 900, 1500))
    rng = _r(482)
    for k in range(500):                                                          # hierba
        x, y = rng.uniform(-800, 2700), rng.uniform(900, 1500)
        L.linea([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(10, 26))], 1.4, rng.uniform(0.25, 0.4), alfa=0.8, jit=0)
    L.poli([(700, 900), (1260, 900), (1600, 1600), (380, 1600)], 0.34, tex=0.15)  # sendero de grava
    return L.capa()


# ====================================================================== la terraza de la boda
@functools.lru_cache(maxsize=1)
def terraza_fondo():
    """La ciudad de noche abajo, con la bahía y sus luces, vista desde la terraza; guirnaldas de faroles."""
    L = Lienzo(3200, 1800, origen=(-640, -800), base=0.08, sem=491)
    L.rect(-640, -800, 3200, 1800, 0.06, grad=(0.30, -800, 500))
    L.elipse(400, -400, 50, 50, 0.95, tex=0, emis=0.7)
    L.brillo(400, -400, 240, 0.35, tono=0.85)
    L.rect(-640, 380, 3200, 620, 0.14, tex=0.1, grad=(0.08, 380, 1000))          # bahía
    rng = _r(492)
    for k in range(60):
        x = rng.uniform(-600, 2500)
        L.linea([(x, rng.uniform(400, 900)), (x + rng.uniform(30, 90), rng.uniform(400, 900))], 1.4, 0.4, alfa=0.5)
    for k in range(320):                                                          # tejados de la ciudad con ventanas
        x, y = rng.uniform(-600, 2500), rng.uniform(260, 520)
        L.rect(x, y, rng.uniform(30, 70), 300, rng.uniform(0.1, 0.18), tex=0.1)
        if rng.uniform() < 0.3:
            L.rect(x + 8, y + 16, 7, 10, 0.8, emis=0.8)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def terraza_balaustrada():
    L = Lienzo(3200, 1200, origen=(-640, 500), sem=501)
    L.rect(-640, 600, 3200, 40, 0.42, tex=0.08)
    L.rect(-640, 860, 3200, 50, 0.40, tex=0.08)
    for x in np.arange(-620, 2560, 70):                                          # balaustres
        L.poli([(x + 14, 640), (x + 36, 640), (x + 44, 700), (x + 30, 760), (x + 40, 860), (x + 10, 860), (x + 20, 760), (x + 6, 700)],
               0.36, tex=0.1)
        L.linea([(x + 14, 640), (x + 6, 700), (x + 20, 760), (x + 10, 860)], 1.4, 0.03)
        L.linea([(x + 36, 640), (x + 44, 700), (x + 30, 760), (x + 40, 860)], 1.4, 0.03)
    L.linea([(-640, 600), (2560, 600)], 2.4, 0.02)
    L.linea([(-640, 640), (2560, 640)], 2.0, 0.02)
    L.rect(-640, 910, 3200, 400, 0.26, tex=0.12)                                 # suelo de la terraza
    for x in np.arange(-640, 2560, 160):
        L.linea([(x, 910), (x - 60, 1310)], 1.4, 0.08, alfa=0.7)
    return L.capa()


# ====================================================================== la rosaleda al atardecer
@functools.lru_cache(maxsize=1)
def rosal_cielo():
    L = Lienzo(3000, 1700, origen=(-540, -600), base=0.4, sem=511)
    L.rect(-540, -600, 3000, 1700, 0.55, tex=0.05, grad=(0.22, -600, 900))       # atardecer: claro abajo
    L.elipse(1500, 520, 120, 120, 0.95, tex=0, emis=0.55)
    L.brillo(1500, 520, 520, 0.5, tono=0.95)
    rng = _r(512)
    for k in range(16):
        cx, cy = rng.uniform(-500, 2400), rng.uniform(-550, 400)
        L.elipse(cx, cy, rng.uniform(220, 520), rng.uniform(18, 40), rng.uniform(0.3, 0.5), alfa=0.6, rug=1.2, blur=8)
    L.poli([(-540, 760), (200, 640), (900, 690), (1500, 620), (2460, 720), (2460, 1100), (-540, 1100)], 0.2, tex=0.12)  # colinas
    for k in range(40):                                                           # cipreses lejanos
        x = rng.uniform(-500, 2400)
        y = 680 + rng.uniform(-30, 30)
        L.elipse(x, y - 60, 14, 70, 0.12, alfa=0.9)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def rosal():
    """Arco de rosas trepadoras con espinas y tallos retorcidos (las rosas se tiñen por cuadro)."""
    L = Lienzo(3000, 1800, origen=(-540, -700), sem=521)
    rng = _r(522)
    for sx in (-1, 1):
        x0 = 80 if sx < 0 else 1840
        for k in range(14):                                                       # tallos retorcidos
            pts = [(x0 + rng.uniform(-80, 80), 1100)]
            for j in range(10):
                px, py = pts[-1]
                pts.append((px + rng.uniform(-60, 60) - sx * 18, py - rng.uniform(100, 170)))
            L.linea(pts, rng.uniform(4, 9), 0.10, jit=2.0)
            for (px, py) in pts[1::2]:                                            # espinas
                L.poli([(px - 6, py), (px + 6, py), (px + sx * 22, py - 14)], 0.08)
        for k in range(110):                                                      # hojas
            x = x0 + rng.uniform(-260, 260)
            y = rng.uniform(-600, 1080)
            L.elipse(x, y, rng.uniform(14, 26), rng.uniform(7, 12), rng.uniform(0.14, 0.26), rot=rng.uniform(0, 3), alfa=0.95, tex=0.2)
    for k in range(40):                                                           # el arco que une los dos rosales
        a = math.pi * k / 39
        x = 960 - 900 * math.cos(a)
        y = -380 - 340 * math.sin(a)
        L.elipse(x + rng.uniform(-30, 30), y + rng.uniform(-30, 30), rng.uniform(40, 80), rng.uniform(28, 50), 0.16, alfa=0.95,
                 rug=1.4, tex=0.2)
    return L.capa()


# ====================================================================== la contaduría de Meñique
@functools.lru_cache(maxsize=1)
def contaduria():
    L = Lienzo(2800, 1500, origen=(-440, -300), base=0.16, sem=531)
    for x in np.arange(-440, 2360, 120):                                          # muro de paneles de madera oscura
        L.rect(x, -300, 120, 1500, 0.17 + 0.02 * math.sin(x * 0.7), tex=0.1)
        L.linea([(x, -300), (x, 1200)], 1.6, 0.05)
        L.rect(x + 14, -200, 92, 300, 0.2, tex=0.08)
        L.linea([(x + 14, -200), (x + 106, -200), (x + 106, 100), (x + 14, 100)], 1.4, 0.06, cerrado=True)
    # estantería de libros de cuentas detrás a la derecha
    rng = _r(532)
    for k, y in enumerate((120, 360)):
        L.rect(1200, y + 200, 1100, 20, 0.3, tex=0.1)
        x = 1220
        while x < 2280:
            w = rng.uniform(30, 50)
            hh = rng.uniform(150, 190)
            L.rect(x, y + 200 - hh, w, hh, rng.uniform(0.16, 0.34), tex=0.1)
            L.linea([(x, y + 200 - hh), (x + w, y + 200 - hh), (x + w, y + 200), (x, y + 200)], 1.4, 0.03, cerrado=True)
            for j in (0.2, 0.8):
                L.linea([(x + 3, y + 200 - hh * j), (x + w - 3, y + 200 - hh * j)], 2.0, 0.55, alfa=0.6)
            x += w + 3
    # mesa de cuentas con monedas apiladas, balanza y el libro mayor abierto
    L.rect(-440, 760, 2800, 600, 0.26, tex=0.12, grad=(0.18, 760, 1360))
    L.linea([(-440, 760), (2360, 760)], 2.4, 0.02)
    for k in range(9):
        x = 1300 + k * 70 + rng.uniform(-10, 10)
        n = int(rng.integers(4, 12))
        for j in range(n):
            L.elipse(x, 880 - j * 9, 26, 8, 0.6 + 0.1 * (j % 2), tex=0.05)
            L.linea([(x - 26, 880 - j * 9), (x + 26, 880 - j * 9)], 1.2, 0.2, alfa=0.7)
    L.poli([(200, 860), (560, 830), (600, 1000), (220, 1030)], 0.70, tex=0.05)
    L.poli([(560, 830), (900, 850), (880, 1010), (600, 1000)], 0.68, tex=0.05)
    for j in range(9):
        L.linea([(240, 880 + j * 15), (540, 852 + j * 15)], 1.2, 0.25, alfa=0.7)
        L.linea([(610, 852 + j * 15), (860, 870 + j * 15)], 1.2, 0.25, alfa=0.7)
    L.linea([(200, 860), (560, 830), (900, 850), (880, 1010), (600, 1000), (220, 1030)], 2.0, 0.02, cerrado=True)
    n = 0.5 + 0.5 * np.tanh(fbm(L.w, L.h, 260, 3, 533))
    L.g *= (0.85 + 0.25 * n).astype(np.float32)
    return L.capa(opaco=True)


def VER(h, amb):
    import noir_color as NC

    def celda():
        h.camara(1.0, 960, 540)
        NC.pegar(celda_muro(), h, 0.8, rampa="muralla", col_emis=h.pal["luna"])
        NC.pegar(celda_suelo(), h, 0.9, rampa="cera")
        NC.pegar(celda_reja(), h, 1.2, rampa="hierro")
        amb(0.4)
        h.luz_radial(1350, 0, 900, h.pal["luna"], k=0.8)
        h.luz_radial(600, 500, 900, h.pal["antorcha"], k=1.0)

    def botica():
        h.camara(1.0, 960, 540)
        NC.pegar(botica_estantes(), h, 0.8, rampa="madera")
        NC.pegar(botica_mesa(), h, 1.0, rampa="madera")
        amb(0.35)
        h.luz_radial(960, 700, 1000, h.pal["vela"], k=1.2)

    def jardin():
        h.camara(1.0, 960, 400)
        NC.pegar(jardin_cielo(), h, 0.1, rampa="cielo")
        NC.pegar(jardin_arboles(), h, 0.7, rampa="tela_verde", bruma=0.12)
        NC.pegar(jardin_suelo(), h, 1.0, rampa="tela_verde")
        amb(0.9)

    def terraza():
        h.camara(1.0, 960, 540)
        NC.pegar(terraza_fondo(), h, 0.2, rampa="cielo")
        NC.pegar(terraza_balaustrada(), h, 1.0, rampa="muralla")
        amb(0.7)
        h.luz_radial(960, 300, 900, h.pal["antorcha"], k=0.9)

    def rosaleda():
        h.camara(1.0, 960, 540)
        NC.pegar(rosal_cielo(), h, 0.2, rampa="whisky")
        NC.pegar(rosal(), h, 1.0, rampa="tela_verde")
        amb(0.7)
        h.luz_radial(1500, 520, 1300, h.pal["antorcha"], k=0.8)

    def conta():
        h.camara(1.0, 960, 540)
        NC.pegar(contaduria(), h, 1.0, rampa="madera")
        amb(0.3)
        h.luz_radial(700, 700, 900, h.pal["vela"], k=1.3)
    return dict(celda=celda, botica=botica, jardin=jardin, terraza=terraza, rosaleda=rosaleda, conta=conta)
