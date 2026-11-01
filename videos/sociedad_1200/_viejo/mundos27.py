# -*- coding: utf-8 -*-
"""Mundos nuevos de «El informante que le puso fecha al final» (estilo noir). Se pintan una vez por proceso (lru_cache).
Todos: Lienzo 2520 x 1500 con origen (-300, -200) (cubre la pantalla con margen para derivas de cámara).

    laboratorio()   nave de servidores en perspectiva (pasillo central, punto de fuga 960, 470), techo con regletas, puerta al fondo
    sala_comite()   sala de juntas: ventanales con la ciudad, paneles de madera, retratos; la mesa va aparte (mesa_comite)
    capitolio()     la cúpula de noche, escalinata y alas; cielo cargado
    fabrica()       nave industrial: cerchas, lámparas, máquinas al fondo y la cinta transportadora (borde y≈840)
    redaccion()     pared de redacción de periódico: relojes de ciudades, archiveros, ventanal con persiana
    despacho()      despacho de empresa moderna (salida de Daniel): pared de vidrio con la ciudad, estantes, la puerta a la derecha
"""
import functools
import math

import numpy as np

from noir_fondos import Lienzo, texto_lienzo

OX, OY, LW, LH = -300, -200, 2520, 1500
FX, FY = 960.0, 470.0            # punto de fuga del laboratorio


def P3(x, y, z, k=0.55):
    """Proyección de un punto (x, y a profundidad 0; z = pasos hacia el fondo) al punto de fuga."""
    s = 1.0 / (1.0 + z * k)
    return (FX + (x - FX) * s, FY + (y - FY) * s)


@functools.lru_cache(maxsize=1)
def laboratorio():
    L = Lienzo(LW, LH, origen=(OX, OY), base=0.0, sem=501)
    r = np.random.default_rng(502)
    L.rect(OX, OY, LW, LH, 0.05, tex=0.06)
    XI, XD, YT, YS, ZF = 330, 1590, -120, 1180, 7
    # suelo y techo
    L.poli([P3(XI, YS, 0), P3(XD, YS, 0), P3(XD, YS, ZF), P3(XI, YS, ZF)], 0.22, tex=0.10, grad=(0.10, FY, 1180))
    L.poli([(OX, 1180), (OX + LW, 1180), (OX + LW, OY + LH), (OX, OY + LH)], 0.20, tex=0.10)
    L.poli([P3(XI, YT, 0), P3(XD, YT, 0), P3(XD, YT, ZF), P3(XI, YT, ZF)], 0.08, tex=0.06)
    for z in np.arange(0, ZF + 0.01, 0.5):                           # juntas de las losetas
        a, b = P3(XI, YS, z), P3(XD, YS, z)
        L.linea([a, b], 1.6, 0.04, alfa=0.6, jit=0.2)
    for x in np.linspace(XI, XD, 8):
        L.linea([P3(x, YS, 0), P3(x, YS, ZF)], 1.4, 0.04, alfa=0.5, jit=0.2)
    for x in (XI + 330, XD - 330):                                   # regletas de luz en el techo
        for z in np.arange(0.1, ZF, 1.0):
            Q = [P3(x - 46, YT, z), P3(x + 46, YT, z), P3(x + 46, YT, z + 0.62), P3(x - 46, YT, z + 0.62)]
            L.poli(Q, 0.95, tex=0.0, emis=0.75)
    # fondo: muro con la puerta de seguridad
    a, b = P3(XI, YT, ZF), P3(XD, YS, ZF)
    L.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], 0.10, tex=0.08)
    L.rect(FX - 34, b[1] - 120, 68, 120, 0.04, tex=0.02)
    L.rect(FX - 26, b[1] - 112, 52, 40, 0.8, emis=0.5, tex=0.0)
    # filas de armarios (cara al pasillo) a izquierda y derecha
    for lado, x in ((-1, XI), (1, XD)):
        for k in range(ZF):
            z0, z1 = k + 0.04, k + 0.96
            Q = [P3(x, YT + 60, z0), P3(x, YT + 60, z1), P3(x, YS, z1), P3(x, YS, z0)]
            L.poli(Q, 0.13 + 0.02 * (k % 2), tex=0.10, grad=(0.06, FY - 300, FY + 500))
            L.linea(Q + [Q[0]], 2.2, 0.02, alfa=0.9, jit=0.3)
            # puerta de rejilla y luces
            for j in range(26):
                v = (j + 1.5) / 29
                ya0 = YT + 60 + (YS - YT - 60) * v
                p0, p1 = P3(x, ya0, z0 + 0.08), P3(x, ya0, z1 - 0.08)
                L.linea([p0, p1], 1.0, 0.03, alfa=0.55, jit=0.1)
                for q in range(3):
                    if r.uniform() < 0.34:
                        zz = z0 + 0.14 + q * 0.26 + r.uniform(0, 0.08)
                        c = P3(x, ya0 - 8, zz)
                        sc = 1.0 / (1.0 + zz * 0.55)
                        L.rect(c[0] - 4 * sc, c[1] - 3 * sc, max(2.0, 8 * sc), max(2.0, 6 * sc), 0.95, emis=r.uniform(0.5, 1.0), tex=0.0)
        # frente del primer armario (lo más cercano a cámara)
        xa, xb = (OX, x) if lado < 0 else (x, OX + LW)
        L.rect(xa, YT + 60, xb - xa, YS - YT - 60, 0.07, tex=0.10, grad=(0.03, 0, 1100))
        L.linea([(x, YT + 60), (x, YS)], 3.0, 0.4, alfa=0.5, jit=0.3)
        for j in range(20):
            yy = YT + 120 + j * 62
            L.linea([(xa + 30, yy), (xb - 30, yy)], 1.4, 0.16, alfa=0.5, jit=0.3)
    # bandejas de cables en el techo
    for x in (XI + 110, XD - 110):
        L.linea([P3(x, YT + 30, 0), P3(x, YT + 30, ZF)], 5.0, 0.02, alfa=0.9, jit=0.4)
        for z in np.arange(0.3, ZF, 0.7):
            a = P3(x, YT + 30, z)
            b = P3(x + 40 * math.sin(z * 3), YT + 120, z)
            L.linea([a, b], 1.6, 0.02, alfa=0.7, jit=0.6)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def sala_comite():
    L = Lienzo(LW, LH, origen=(OX, OY), base=0.0, sem=521)
    r = np.random.default_rng(522)
    L.rect(OX, OY, LW, LH, 0.16, tex=0.10, grad=(0.08, -200, 900))
    for k in range(4):                                               # ventanales con la ciudad
        x = -220 + k * 620
        L.rect(x, -120, 440, 700, 0.07, tex=0.04, grad=(0.17, -120, 580))
        xx = x
        while xx < x + 440:
            an, al = r.uniform(50, 110), r.uniform(160, 560)
            an = min(an, x + 440 - xx)
            L.rect(xx, 580 - al, an, al, r.uniform(0.09, 0.15), tex=0.06)
            for j in range(int(al // 24)):
                for i in range(int(an // 16)):
                    if r.uniform() < 0.22:
                        L.rect(xx + 4 + i * 16, 580 - al + 6 + j * 24, 8, 12, r.uniform(0.6, 1.0), emis=r.uniform(0.3, 0.6), tex=0.0)
            xx += an + r.uniform(2, 14)
        L.linea([(x, -120), (x + 440, -120), (x + 440, 580), (x, 580), (x, -120)], 6, 0.03, jit=0.3)
        for q in (1, 2):
            L.linea([(x + 440 * q / 3, -120), (x + 440 * q / 3, 580)], 3, 0.03, jit=0.2)
        L.linea([(x, 230), (x + 440, 230)], 3, 0.03, jit=0.2)
    for k in range(5):                                               # entrepaños de madera entre ventanas
        x = -400 + k * 620
        L.rect(x, -200, 180, 800, 0.12, tex=0.14, grad=(0.07, -200, 600))
        if 0 < k < 4:
            L.rect(x + 40, 60, 100, 140, 0.26, tex=0.05)             # retrato enmarcado
            L.elipse(x + 90, 118, 22, 28, 0.10, tex=0.03)
            L.rect(x + 58, 150, 64, 44, 0.08, tex=0.03)
            L.linea([(x + 40, 60), (x + 140, 60), (x + 140, 200), (x + 40, 200), (x + 40, 60)], 5, 0.03, jit=0.3)
            L.rect(x + 76, 320, 28, 60, 0.5, emis=0.35, tex=0.0)     # aplique
    L.rect(OX, 600, LW, 60, 0.06, tex=0.08)                          # zócalo alto
    L.rect(OX, 660, LW, LH, 0.11, tex=0.14, grad=(0.05, 660, 1300))  # alfombra
    for k in range(26):
        L.linea([(OX + k * 100, 660), (OX + k * 100 - 160, 1300)], 1.5, 0.03, alfa=0.35, jit=0.4)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def capitolio():
    from noir import fbm
    L = Lienzo(LW, LH, origen=(OX, OY), base=0.0, sem=541)
    L.rect(OX, OY, LW, LH, 0.20, tex=0.05, grad=(0.42, -200, 900))
    n = 0.6 * fbm(L.w, L.h, 260, 5, 542) + 0.4 * fbm(L.w, L.h, 70, 3, 543)
    L.g = L.g * (0.7 + 0.55 * n)
    cx, base = 960, 900
    # alas
    for lado in (-1, 1):
        x0 = cx + lado * 330 if lado > 0 else cx - 330 - 760
        L.rect(x0, base - 300, 760, 300, 0.56, tex=0.08, grad=(0.34, base - 300, base))
        L.rect(x0 - 10, base - 322, 780, 26, 0.66, tex=0.05)
        for k in range(15):
            xx = x0 + 22 + k * 50
            L.rect(xx, base - 280, 22, 250, 0.72, tex=0.04, grad=(0.5, base - 280, base - 30))
            L.rect(xx + 28, base - 240, 14, 120, 0.9, emis=0.45, tex=0.0)
    # cuerpo central con frontón y columnata
    L.rect(cx - 340, base - 380, 680, 380, 0.60, tex=0.08, grad=(0.36, base - 380, base))
    L.poli([(cx - 370, base - 380), (cx, base - 500), (cx + 370, base - 380)], 0.68, tex=0.06)
    L.linea([(cx - 370, base - 380), (cx, base - 500), (cx + 370, base - 380), (cx - 370, base - 380)], 4, 0.05, jit=0.3)
    for k in range(10):
        xx = cx - 310 + k * 66
        L.rect(xx, base - 370, 28, 330, 0.80, tex=0.03, grad=(0.55, base - 370, base - 40))
        L.linea([(xx + 20, base - 370), (xx + 20, base - 40)], 1.5, 0.2, alfa=0.5, jit=0.2)
        L.rect(xx + 34, base - 300, 24, 220, 0.95, emis=0.5, tex=0.0)
    # tambor y cúpula
    L.rect(cx - 190, base - 640, 380, 150, 0.62, tex=0.06, grad=(0.42, base - 640, base - 490))
    for k in range(13):
        xx = cx - 180 + k * 29
        L.rect(xx, base - 630, 12, 130, 0.84, tex=0.03)
        L.rect(xx + 14, base - 610, 10, 80, 0.95, emis=0.55, tex=0.0)
    L.rect(cx - 205, base - 660, 410, 22, 0.70, tex=0.04)
    dome = [(cx - 180, base - 660)]
    for a in np.linspace(math.pi, 0, 30):
        dome.append((cx + 180 * math.cos(a), base - 660 - 250 * math.sin(a) ** 0.85))
    L.poli(dome, 0.66, tex=0.07, grad=(0.40, base - 910, base - 660))
    for k in range(-5, 6):
        P = [(cx + k * 34, base - 662)]
        for v in np.linspace(0, 1, 12):
            P.append((cx + k * 34 * (1 - v ** 1.6), base - 662 - 246 * v))
        L.linea(P, 1.6, 0.12, alfa=0.6, jit=0.3)
    L.rect(cx - 40, base - 990, 80, 84, 0.70, tex=0.05)
    for k in range(5):
        L.rect(cx - 34 + k * 15, base - 980, 7, 64, 0.95, emis=0.6, tex=0.0)
    L.poli([(cx - 46, base - 990), (cx, base - 1050), (cx + 46, base - 990)], 0.6, tex=0.05)
    L.rect(cx - 5, base - 1100, 10, 54, 0.5, tex=0.02)
    L.brillo(cx, base - 700, 900, 0.5, tono=0.75)
    # escalinata y explanada
    for k in range(9):
        L.rect(cx - 420 - k * 26, base + k * 16, 840 + k * 52, 18, 0.50 - 0.03 * k, tex=0.06)
        L.linea([(cx - 420 - k * 26, base + k * 16), (cx + 420 + k * 26, base + k * 16)], 1.5, 0.08, alfa=0.6, jit=0.2)
    L.rect(OX, base + 144, LW, LH, 0.16, tex=0.12, grad=(0.07, base + 144, 1300))
    for x in (-120, 320, 1600, 2040):                                # farolas de globo
        L.rect(x - 5, base - 60, 10, 210, 0.05)
        L.elipse(x, base - 80, 22, 22, 0.95, emis=0.8, tex=0.0)
        L.brillo(x, base - 80, 240, 0.5, tono=0.85)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def fabrica():
    L = Lienzo(LW, LH, origen=(OX, OY), base=0.0, sem=561)
    r = np.random.default_rng(562)
    L.rect(OX, OY, LW, LH, 0.13, tex=0.10, grad=(0.06, -200, 900))
    for k in range(9):                                               # ventanales industriales altos (cuadrícula)
        x = -280 + k * 290
        L.rect(x, -150, 220, 420, 0.30, tex=0.04, grad=(0.16, -150, 270))
        for i in range(1, 4):
            L.linea([(x + i * 55, -150), (x + i * 55, 270)], 2.2, 0.03, jit=0.2)
        for j in range(1, 6):
            L.linea([(x, -150 + j * 70), (x + 220, -150 + j * 70)], 2.2, 0.03, jit=0.2)
        L.linea([(x, -150), (x + 220, -150), (x + 220, 270), (x, 270), (x, -150)], 5, 0.03, jit=0.3)
    for k in range(6):                                               # cerchas del techo
        x = -300 + k * 500
        L.linea([(x, -200), (x + 250, -60), (x + 500, -200)], 9, 0.03, jit=0.4)
        L.linea([(x + 250, -60), (x + 250, -200)], 6, 0.03, jit=0.3)
        L.linea([(x + 125, -130), (x + 125, -200)], 4, 0.03, jit=0.3)
        L.linea([(x + 375, -130), (x + 375, -200)], 4, 0.03, jit=0.3)
    L.linea([(OX, -60), (OX + LW, -60)], 12, 0.03, jit=0.4)
    for k in range(7):                                               # máquinas al fondo: prensas y depósitos
        x = -260 + k * 370 + r.uniform(-20, 20)
        al = r.uniform(220, 380)
        L.rect(x, 640 - al, 250, al, r.uniform(0.07, 0.11), tex=0.10)
        L.rect(x + 30, 640 - al + 30, 80, 60, 0.6, emis=0.3, tex=0.0)
        for q in range(4):
            L.elipse(x + 150 + q * 22, 640 - al + 60, 7, 7, 0.9, emis=r.uniform(0.3, 0.9), tex=0.0)
        L.linea([(x + 125, 640 - al), (x + 125, 640 - al - 160), (x + 300, 640 - al - 160)], 14, 0.04, jit=0.3)
    L.rect(OX, 640, LW, 30, 0.04)
    L.rect(OX, 670, LW, LH, 0.17, tex=0.12, grad=(0.07, 670, 1300))  # suelo
    for k in range(30):
        L.poli([(OX + k * 90, 1010), (OX + k * 90 + 45, 1010), (OX + k * 90 + 15, 1050), (OX + k * 90 - 30, 1050)], 0.5, alfa=0.55, tex=0.05)
    # cinta transportadora (el tablero: y 840..880; faldón debajo)
    L.rect(OX, 880, LW, 110, 0.07, tex=0.08)
    L.rect(OX, 836, LW, 46, 0.24, tex=0.08, grad=(0.14, 836, 882))
    L.linea([(OX, 836), (OX + LW, 836)], 3, 0.5, alfa=0.6, jit=0.3)
    for k in range(18):
        L.rect(OX + 40 + k * 140, 990, 22, 130, 0.05)
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def redaccion():
    L = Lienzo(LW, LH, origen=(OX, OY), base=0.0, sem=581)
    r = np.random.default_rng(582)
    L.rect(OX, OY, LW, LH, 0.20, tex=0.12, grad=(0.10, -200, 900))
    L.rect(1250, -140, 900, 620, 0.10, tex=0.04, grad=(0.24, -140, 480))            # ventanal con persiana
    for j in range(24):
        L.rect(1250, -140 + j * 26, 900, 12, 0.34, tex=0.04)
    L.linea([(1250, -140), (2150, -140), (2150, 480), (1250, 480), (1250, -140)], 8, 0.03, jit=0.3)
    for k, c in enumerate(("NUEVA YORK", "LONDRES", "PEKÍN", "TOKIO")):               # relojes de las corresponsalías
        cx = -120 + k * 320
        L.elipse(cx, 40, 92, 92, 0.05, tex=0.02)
        L.elipse(cx, 40, 80, 80, 0.80, tex=0.03)
        for q in range(12):
            a = q * math.pi / 6
            L.linea([(cx + 66 * math.cos(a), 40 + 66 * math.sin(a)), (cx + 76 * math.cos(a), 40 + 76 * math.sin(a))], 3, 0.05, jit=0)
        a1, a2 = r.uniform(0, 6.28), r.uniform(0, 6.28)
        L.linea([(cx, 40), (cx + 44 * math.cos(a1), 40 + 44 * math.sin(a1))], 6, 0.04, jit=0)
        L.linea([(cx, 40), (cx + 64 * math.cos(a2), 40 + 64 * math.sin(a2))], 3.5, 0.04, jit=0)
        texto_lienzo(L, c, cx, 168, 30, tono=0.75, track=2)
    for k in range(6):                                                                # archiveros
        x = -280 + k * 250
        L.rect(x, 330, 220, 430, 0.13 + 0.02 * (k % 2), tex=0.12, grad=(0.07, 330, 760))
        for j in range(4):
            L.linea([(x, 330 + j * 108), (x + 220, 330 + j * 108)], 3, 0.03, jit=0.3)
            L.rect(x + 84, 368 + j * 108, 52, 14, 0.5, tex=0.02)
        L.linea([(x, 330), (x + 220, 330), (x + 220, 760), (x, 760), (x, 330)], 4, 0.03, jit=0.3)
    for k in range(5):                                                                # pilas de periódicos sobre los archiveros
        x = -240 + k * 250 + r.uniform(0, 60)
        for j in range(int(r.integers(3, 8))):
            L.rect(x + r.uniform(-6, 6), 318 - j * 11, 130, 10, r.uniform(0.55, 0.8), tex=0.05)
    L.rect(OX, 760, LW, 26, 0.05)
    L.rect(OX, 786, LW, LH, 0.15, tex=0.14, grad=(0.06, 786, 1300))
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def despacho():
    L = Lienzo(LW, LH, origen=(OX, OY), base=0.0, sem=601)
    r = np.random.default_rng(602)
    L.rect(OX, OY, LW, LH, 0.17, tex=0.10, grad=(0.09, -200, 900))
    L.rect(-300, -140, 1240, 760, 0.07, tex=0.04, grad=(0.18, -140, 620))            # pared de vidrio: la ciudad
    x = -300
    while x < 940:
        an, al = r.uniform(80, 170), r.uniform(240, 700)
        an = min(an, 940 - x)
        L.rect(x, 620 - al, an, al, r.uniform(0.10, 0.16), tex=0.07)
        for j in range(int(al // 26)):
            for i in range(int(an // 18)):
                if r.uniform() < 0.2:
                    L.rect(x + 5 + i * 18, 620 - al + 8 + j * 26, 9, 13, r.uniform(0.6, 1.0), emis=r.uniform(0.3, 0.6), tex=0.0)
        x += an + r.uniform(4, 24)
    for k in range(6):
        xa = -300 + k * 248
        L.rect(xa - 6, -140, 12, 760, 0.04, tex=0.02)
    L.rect(-300, 240, 1240, 8, 0.04)
    for j in range(4):                                                                # estantería empotrada
        L.rect(1010, -60 + j * 170, 520, 150, 0.08, tex=0.06)
        xx = 1022
        while xx < 1500:
            an = r.uniform(18, 44)
            al = r.uniform(80, 138)
            if r.uniform() < 0.8:
                L.rect(xx, -60 + j * 170 + 150 - al, an, al, r.uniform(0.14, 0.5), tex=0.08)
                L.linea([(xx, -60 + j * 170 + 150 - al), (xx, -60 + j * 170 + 150)], 1.5, 0.03, jit=0.2)
            xx += an + 2
        L.linea([(1010, -60 + j * 170 + 150), (1530, -60 + j * 170 + 150)], 5, 0.03, jit=0.3)
    L.rect(OX, 620, LW, 30, 0.05)
    L.rect(OX, 650, LW, LH, 0.13, tex=0.14, grad=(0.06, 650, 1300))
    for k in range(20):
        L.linea([(OX + k * 130, 650), (OX + k * 130 - 200, 1300)], 1.4, 0.03, alfa=0.35, jit=0.4)
    return L.capa(opaco=True)
