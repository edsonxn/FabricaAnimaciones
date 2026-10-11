# -*- coding: utf-8 -*-
"""Fondo de la SALA de noche (la tele encendida queda fuera de cuadro): pared de papel pintado, lambrín, suelo de tablas, alfombra,
ventana con luna, cuadro torcido, reloj de las 3:00, sillón capitoné (respaldo detrás del gato, frente por delante) y puerta al pasillo."""
import math

import numpy as np

from motor import rect_red as _rr
from mundos import W, H, _capa, arbol_seco, cacheado

SILLON_X = 650          # centro del sillón (mundo)
RELOJ = (840, 420, 96)  # x, y, radio
PUERTA_PASILLO = (-250, -40)   # x0, x1 del hueco de la puerta al pasillo (a la izquierda)


def rr(x, y, w, h, r, n=8):
    return _rr(x, y, w, h, r, n)


def quad(*pts):
    return np.array(pts, float)


@cacheado
def sala():
    capas = []
    mx, my = 300, 300
    # ---------------------------------------------------------- pared + suelo (opaco)
    p = _capa(mx, my, 61)
    p.degradado([(0.0, (30, 40, 52)), (0.45, (52, 66, 74)), (0.62, (66, 74, 76)), (0.70, (50, 38, 34)), (1.0, (40, 30, 30))],
                y0=0, y1=p.h, tex=0.03)
    pared = quad((-mx, -my), (W + mx, -my), (W + mx, 1562), (-mx, 1562))
    for i, x in enumerate(range(-mx, W + mx, 96)):
        if i % 2 == 0:
            p.poli(quad((x, -my), (x + 48, -my), (x + 48, 1562), (x, 1562)), (74, 90, 92), alfa=0.18, blur=0.8, rug=0.0, tex=0.0)
    for r_, y in enumerate(range(-100, 1300, 130)):
        for c_, x in enumerate(range(-mx + (48 if r_ % 2 else 0), W + mx, 96)):
            if c_ % 2 == 1:
                continue
            P = quad((x + 24, y - 22), (x + 40, y), (x + 24, y + 22), (x + 8, y))
            p.poli(P, (96, 118, 112), alfa=0.30, blur=0.8, rug=0.3, tex=0.0)
            p.elipse(x + 24, y, 5, 5, (150, 110, 90), alfa=0.35, blur=0.6, rug=0.0, tex=0.0)
    p.pinceladas(pared, (20, 26, 40), ang=90, n=500, largo=300, ancho=22, alfa=0.14)
    p.manchas(-mx, -my, W + mx, 1200, (18, 22, 36), 40, 80, 300, 0.22)
    # cornisa del techo
    p.poli(quad((-mx, -my), (W + mx, -my), (W + mx, 150), (-mx, 168)), (24, 30, 44), blur=1, rug=0, tex=0.03)
    p.poli(quad((-mx, 150), (W + mx, 150), (W + mx, 178), (-mx, 196)), (96, 78, 66), blur=1, rug=0.2, tex=0.04)
    # lambrín de madera
    p.poli(quad((-mx, 1256), (W + mx, 1256), (W + mx, 1562), (-mx, 1562)), (92, 64, 52), blur=0.8, rug=0.2, tex=0.05,
           grad=((62, 42, 38), 1256, 1562))
    for x in range(-mx, W + mx, 180):
        p.poli(rr(x + 14, 1290, 150, 220, 8), (70, 48, 42), alfa=0.8, blur=0.8, rug=0.3, tex=0.04)
        p.poli(rr(x + 22, 1298, 134, 204, 6), (100, 72, 58), alfa=0.5, blur=0.8, rug=0.3, tex=0.04)
    p.poli(quad((-mx, 1244), (W + mx, 1244), (W + mx, 1270), (-mx, 1270)), (140, 108, 84), blur=0.8, rug=0.2, tex=0.04)
    p.poli(quad((-mx, 1540), (W + mx, 1540), (W + mx, 1574), (-mx, 1574)), (60, 42, 38), blur=0.8, rug=0.2, tex=0.04)
    # suelo de tablas en perspectiva
    suelo = quad((-mx, 1574), (W + mx, 1574), (W + mx, H + my), (-mx, H + my))
    p.poli(suelo, (84, 56, 46), blur=0.6, rug=0, tex=0.05, grad=((46, 30, 30), 1574, H + 120))
    for x in range(-1400, W + 1400, 150):
        xb = SILLON_X + (x - SILLON_X) * 0.46
        p.poli(quad((x, H + my), (x + 4, H + my), (xb + 2, 1574), (xb - 2, 1574)), (28, 18, 20), alfa=0.6, blur=0.7, rug=0.2, tex=0)
    for k in range(7):
        y = 1574 + 24 * (1.55 ** k) - 24
        p.poli(quad((-mx, y), (W + mx, y), (W + mx, y + 4 + k), (-mx, y + 4 + k)), (24, 16, 18), alfa=0.5, blur=0.8, rug=0.3, tex=0)
    p.pinceladas(suelo, (130, 92, 70), ang=2, n=500, largo=260, ancho=12, alfa=0.10)
    # alfombra ovalada con cenefas
    p.elipse(SILLON_X, 1820, 520, 150, (30, 16, 22), alfa=0.6, blur=10, rug=0, tex=0)
    p.elipse(SILLON_X, 1806, 500, 140, (110, 44, 52), blur=1.2, rug=0.5, tex=0.06, grad=((70, 28, 40), 1670, 1950))
    a = np.linspace(0, 2 * math.pi, 90)
    for rx_, ry_, c_ in ((470, 126, (170, 120, 70)), (400, 104, (150, 100, 66)), (330, 84, (120, 52, 60))):
        p.poli(np.vstack([np.stack([SILLON_X + rx_ * np.cos(a), 1806 + ry_ * np.sin(a)], 1),
                          np.stack([SILLON_X + (rx_ - 12) * np.cos(a[::-1]), 1806 + (ry_ - 4) * np.sin(a[::-1])], 1)]),
               c_, alfa=0.6, blur=0.8, rug=0.4, tex=0.03)
    # puerta al pasillo (hueco oscuro a la izquierda) con marco
    x0, x1 = PUERTA_PASILLO
    p.poli(quad((x0 - 40, 480), (x1 + 40, 480), (x1 + 40, 1562), (x0 - 40, 1562)), (112, 88, 70), blur=0.8, rug=0.3, tex=0.05)
    p.poli(quad((x0, 520), (x1, 520), (x1, 1562), (x0, 1562)), (8, 10, 22), blur=0.8, rug=0.2, tex=0.02)
    p.glow((x0 + x1) / 2, 1500, 220, (90, 190, 160), 0.18, ry=420, pot=1.6)
    # haz de luna que entra por la ventana
    p.luz_poli(quad((336, 600), (336, 1040), (1000, 1720), (640, 1780)), (150, 170, 255), 0.20, 34)
    p.viñeta(0.35, 2.0)
    capas.append((p.rgb(), -mx, -my, 0.9))

    # ---------------------------------------------------------- muebles de atrás (rgba)
    q = _capa(mx, my, 62)
    vx0, vy0, vw, vh = 70, 520, 270, 560
    q.poli(quad((vx0 - 26, vy0 - 30), (vx0 + vw + 26, vy0 - 30), (vx0 + vw + 26, vy0 + vh + 30), (vx0 - 26, vy0 + vh + 30)),
           (130, 108, 92), blur=0.7, rug=0.3, tex=0.05)
    q.poli(quad((vx0, vy0), (vx0 + vw, vy0), (vx0 + vw, vy0 + vh), (vx0, vy0 + vh)), (22, 24, 76), blur=0.7, rug=0.2, tex=0.03,
           grad=((60, 70, 130), vy0, vy0 + vh))
    q.elipse(vx0 + 190, vy0 + 130, 60, 60, (236, 230, 190), blur=1.2, rug=0.2, tex=0.03)
    q.glow(vx0 + 190, vy0 + 130, 200, (150, 160, 230), 0.4, pot=2.0)
    arbol_seco(q, vx0 + 70, vy0 + vh, 0.55)
    xm = vx0 + vw / 2
    q.poli(quad((xm - 7, vy0), (xm + 7, vy0), (xm + 7, vy0 + vh), (xm - 7, vy0 + vh)), (130, 108, 92), blur=0.5, rug=0.2, tex=0.03)
    q.poli(quad((vx0, vy0 + vh * 0.46), (vx0 + vw, vy0 + vh * 0.46), (vx0 + vw, vy0 + vh * 0.46 + 14), (vx0, vy0 + vh * 0.46 + 14)),
           (130, 108, 92), blur=0.5, rug=0.2, tex=0.03)
    q.poli(quad((vx0 - 44, vy0 + vh + 22), (vx0 + vw + 44, vy0 + vh + 22), (vx0 + vw + 52, vy0 + vh + 54), (vx0 - 52, vy0 + vh + 54)),
           (150, 124, 100), blur=0.7, rug=0.3, tex=0.05)
    # cortinas con pliegues
    for sg, (cx0, cx1) in enumerate(((vx0 - 40, vx0 + 70), (vx0 + vw - 56, vx0 + vw + 40))):
        d = 14 if sg else -14
        q.poli(quad((cx0, vy0 - 50), (cx1, vy0 - 50), (cx1 + d, vy0 + vh + 40), (cx0 + d, vy0 + vh + 40)), (120, 46, 58),
               blur=0.8, rug=0.8, tex=0.05)
        for k in range(1, 5):
            xx = cx0 + (cx1 - cx0) * k / 5
            e = 10 if sg else -10
            q.poli(quad((xx - 3, vy0 - 40), (xx + 3, vy0 - 40), (xx + 8 + e, vy0 + vh + 30), (xx + 1 + e, vy0 + vh + 30)), (60, 20, 36),
                   alfa=0.55, blur=2.0, rug=0.4, tex=0.0)
    q.poli(quad((vx0 - 70, vy0 - 74), (vx0 + vw + 70, vy0 - 74), (vx0 + vw + 70, vy0 - 52), (vx0 - 70, vy0 - 52)), (96, 66, 52),
           blur=0.7, rug=0.3, tex=0.05)
    # cuadro torcido sobre el sillón
    fx, fy = 590, 560
    q.poli(quad((fx - 118, fy - 128), (fx + 112, fy - 142), (fx + 120, fy + 126), (fx - 112, fy + 138)), (156, 112, 50),
           blur=0.7, rug=0.4, tex=0.06)
    q.poli(quad((fx - 98, fy - 108), (fx + 94, fy - 120), (fx + 100, fy + 106), (fx - 92, fy + 116)), (28, 56, 74),
           blur=0.7, rug=0.2, tex=0.04, grad=((70, 100, 120), fy - 110, fy + 110))
    q.elipse(fx + 40, fy - 50, 26, 26, (236, 230, 190), blur=1, rug=0.2, tex=0.03)
    q.poli(quad((fx - 94, fy + 80), (fx - 30, fy + 20), (fx + 30, fy + 70), (fx + 96, fy + 10), (fx + 100, fy + 106), (fx - 92, fy + 116)),
           (20, 40, 56), blur=0.8, rug=0.8, tex=0.03)
    # reloj de pared con caja del péndulo
    rx_, ry_, rr_ = RELOJ
    q.poli(quad((rx_ - 40, ry_ + rr_ * 0.9), (rx_ + 40, ry_ + rr_ * 0.9), (rx_ + 30, ry_ + 330), (rx_ - 30, ry_ + 330)), (82, 58, 46),
           blur=0.8, rug=0.4, tex=0.05)
    q.poli(quad((rx_ - 22, ry_ + rr_ * 1.05), (rx_ + 22, ry_ + rr_ * 1.05), (rx_ + 18, ry_ + 300), (rx_ - 18, ry_ + 300)), (30, 22, 30),
           blur=0.8, rug=0.3, tex=0.0)
    q.elipse(rx_, ry_, rr_ + 20, rr_ + 20, (88, 62, 48), blur=0.8, rug=0.5, tex=0.05)
    q.elipse(rx_, ry_, rr_, rr_, (226, 214, 176), blur=0.8, rug=0.3, tex=0.04, grad=((176, 164, 132), ry_ - rr_, ry_ + rr_))
    for k in range(12):
        a_ = k * math.pi / 6
        rd = 5 if k % 3 else 8
        q.elipse(rx_ + (rr_ - 14) * math.sin(a_), ry_ - (rr_ - 14) * math.cos(a_), rd, rd, (40, 30, 34), blur=0.5, rug=0, tex=0)
    # sillón: respaldo con capitoné
    sx = SILLON_X
    q.poli(rr(sx - 305, 860, 610, 700, 90, 10), (46, 64, 56), blur=1.0, rug=0.5, tex=0.05, grad=((84, 108, 94), 860, 1560))
    q.poli(rr(sx - 270, 900, 540, 640, 70, 10), (68, 92, 78), blur=1.0, rug=0.5, tex=0.05, grad=((98, 126, 108), 900, 1500))
    for k in range(-5, 8):
        xk = sx - 260 + k * 76
        if xk > sx + 240 or xk + 440 < sx - 260:
            continue
        q.poli(quad((xk, 900), (xk + 5, 900), (xk + 5 + 440, 1340), (xk + 440, 1340)), (36, 52, 46), alfa=0.45, blur=1.2, rug=0.4, tex=0.0)
        q.poli(quad((xk + 520, 900), (xk + 525, 900), (xk + 85, 1340), (xk + 80, 1340)), (36, 52, 46), alfa=0.45, blur=1.2, rug=0.4, tex=0.0)
    for i in range(6):
        for j in range(8):
            xb = sx - 230 + i * 92 + (46 if j % 2 else 0)
            yb = 960 + j * 70
            if sx - 270 < xb < sx + 270:
                q.elipse(xb, yb, 9, 9, (40, 56, 50), blur=0.5, rug=0, tex=0)
                q.elipse(xb - 2, yb - 2, 3, 3, (120, 150, 130), blur=0.4, rug=0, tex=0)
    q.sombra_poli(quad((sx - 300, 1520), (sx + 310, 1520), (sx + 340, 1620), (sx - 330, 1620)), 0.5, 18)
    # mesita con lámpara apagada (derecha)
    q.poli(quad((980, 1380), (1160, 1380), (1160, 1396), (980, 1396)), (110, 80, 62), blur=0.7, rug=0.3, tex=0.05)
    for xx in (1016, 1112):
        q.poli(quad((xx, 1396), (xx + 14, 1396), (xx + 16, 1572), (xx + 2, 1572)), (70, 50, 44), blur=0.7, rug=0.3, tex=0.05)
    q.poli(quad((1052, 1230), (1086, 1230), (1090, 1380), (1048, 1380)), (130, 108, 70), blur=0.7, rug=0.3, tex=0.05)
    q.poli(quad((986, 1040), (1152, 1040), (1190, 1232), (948, 1232)), (176, 148, 104), blur=1.0, rug=0.5, tex=0.05,
           grad=((120, 100, 80), 1040, 1232))
    q.sombra_poli(quad((120, 1560), (1100, 1560), (1100, 1600), (120, 1600)), 0.25, 12)
    capas.append((q.rgba_auto(), -mx, -my, 1.0))

    # ---------------------------------------------------------- frente del sillón (por delante del gato)
    f = _capa(mx, my, 63)
    f.poli(quad((sx - 310, 1500), (sx + 310, 1500), (sx + 350, 1596), (sx - 350, 1596)), (104, 132, 112), blur=1.0, rug=0.5, tex=0.05,
           grad=((78, 104, 90), 1500, 1596))
    f.poli(rr(sx - 352, 1590, 704, 170, 34, 10), (66, 92, 76), blur=1.0, rug=0.5, tex=0.05, grad=((84, 112, 94), 1590, 1760))
    f.poli(quad((sx - 350, 1596), (sx + 350, 1596), (sx + 348, 1608), (sx - 348, 1608)), (150, 182, 150), blur=0.8, rug=0.4, tex=0.03)
    f.pinceladas(rr(sx - 352, 1590, 704, 170, 34, 10), (150, 190, 156), ang=-4, n=200, largo=160, ancho=12, alfa=0.10)
    for k in range(-2, 3):
        f.poli(quad((sx + k * 130 - 3, 1612), (sx + k * 130 + 3, 1612), (sx + k * 130 + 3, 1750), (sx + k * 130 - 3, 1750)), (44, 62, 54),
               alfa=0.5, blur=1.2, rug=0.4, tex=0)
    for sg, xc in ((-1, sx - 400), (1, sx + 400)):
        f.poli(rr(xc - 82, 1190, 164, 570, 60, 10), (62, 86, 72), blur=1.0, rug=0.5, tex=0.05, grad=((92, 120, 100), 1190, 1760))
        f.elipse(xc, 1210, 92, 64, (102, 132, 110), blur=1.0, rug=0.5, tex=0.05, grad=((124, 154, 130), 1160, 1270))
        f.poli(rr(xc - 70, 1330, 140, 380, 40, 8), (52, 74, 62), alfa=0.8, blur=1.2, rug=0.4, tex=0.04)
        f.sombra_poli(quad((xc - 90, 1700), (xc + 90, 1700), (xc + 100, 1780), (xc - 100, 1780)), 0.5, 14)
    f.poli(rr(sx + 360, 1480, 80, 90, 10, 6), (176, 84, 52), blur=0.7, rug=0.4, tex=0.05)
    for k in range(6):
        yy = 1488 + k * 14
        f.poli(quad((sx + 358, yy), (sx + 366, yy), (sx + 366, yy + 5), (sx + 358, yy + 5)), (30, 20, 24), blur=0.4, rug=0, tex=0)
    for xc in (sx - 330, sx + 330):
        f.poli(quad((xc - 22, 1750), (xc + 22, 1750), (xc + 16, 1830), (xc - 16, 1830)), (82, 56, 44), blur=0.8, rug=0.3, tex=0.05)
    capas.append((f.rgba_auto(), -mx, -my, 1.0))
    return capas
