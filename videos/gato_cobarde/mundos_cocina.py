# -*- coding: utf-8 -*-
"""Fondo de la COCINA de noche: el refri de los años 50 (menta) a la izquierda con su interior pintado (estantes, pastel, leche, un pescado
en espinas) que se ve cuando la puerta (dibujada con tinta en la escena) gira sobre las bisagras de la izquierda; mesón con tarja y grifo que
gotea, ventana con luna, gabinetes, lámpara colgante y suelo de baldosas en perspectiva."""
import math

import cv2
import numpy as np

from motor import rect_red as _rr
from mundos import H, W, _capa, cacheado
from toon_fondos import plano_persp

FRIDGE = dict(x0=80, x1=540, y0=340, y1=1560)      # puerta cerrada: de la bisagra (izquierda) al borde libre (derecha)
SUELO_Y = 1500
ESTANTES = None            # se calcula abajo (y de cada estante del refri)
LAMPARA = (800, 150)
GRIFO = (868, 1010)        # punta del grifo (de aquí cae la gota)
RELOJ_GATO = (310, 238, 70)
OJO_COSA = (310, 940)      # centro del ojo gigante que se asoma en el refri
PUERTA = dict(bx=80, y0=356, y1=1544)
SH = [530.0, 767.5, 1005.0, 1242.5, 1480.0]       # y de cada estante del refri
POS_TARTA = (300.0, SH[2] - 2)
POS_PESCADO = (360.0, SH[3] - 2)


def quad(*pts):
    return np.array(pts, float)


def rr(x, y, w, h, r, n=8):
    return _rr(x, y, w, h, r, n)


@cacheado
def cocina():
    capas = []
    mx, my = 300, 300
    # ---------------------------------------------------------- pared, techo y suelo (opaco)
    p = _capa(mx, my, 81)
    p.degradado([(0.0, (26, 22, 24)), (0.35, (92, 72, 52)), (0.68, (112, 88, 60)), (0.78, (34, 30, 30)), (1.0, (22, 22, 24))], y0=0, y1=p.h, tex=0.03)
    pared = quad((-mx, -my), (W + mx, -my), (W + mx, SUELO_Y), (-mx, SUELO_Y))
    p.pinceladas(pared, (170, 130, 80), ang=90, n=500, largo=260, ancho=22, alfa=0.10)
    p.pinceladas(pared, (24, 14, 14), ang=90, n=700, largo=300, ancho=24, alfa=0.16)
    p.manchas(-mx, 100, W + mx, 1400, (14, 16, 12), 50, 90, 300, 0.2)
    # techo y moldura
    p.poli(quad((-mx, -my), (W + mx, -my), (W + mx, 150), (-mx, 168)), (18, 20, 18), blur=1, rug=0, tex=0.03)
    p.poli(quad((-mx, 150), (W + mx, 150), (W + mx, 182), (-mx, 202)), (140, 108, 70), blur=1, rug=0.2, tex=0.04)
    # azulejos del salpicadero (derecha)
    for r_ in range(0, 7):
        for c_ in range(0, 12):
            x, y = 600 + c_ * 64, 850 + r_ * 64 - 0
            if y > 1160:
                continue
            p.poli(rr(x + 3, y + 3, 58, 58, 6), (176, 200, 196) if (r_ + c_) % 2 else (150, 178, 176), alfa=0.9, blur=0.6, rug=0.2, tex=0.04)
    # suelo de baldosas en perspectiva (textura de ajedrez proyectada)
    tex = np.zeros((960, 960, 3), np.float32)
    for i in range(8):
        for j in range(8):
            tex[i * 120:(i + 1) * 120, j * 120:(j + 1) * 120] = (0.80, 0.82, 0.78) if (i + j) % 2 == 0 else (0.10, 0.11, 0.14)
    tex = cv2.GaussianBlur(tex, (0, 0), 1.2)
    ys, xs = np.mgrid[0:960, 0:960]
    tex *= (1 + 0.05 * np.sin(xs * 0.05 + ys * 0.03))[..., None]
    dst = quad((-120 + mx, SUELO_Y + my), (1200 + mx, SUELO_Y + my), (2100 + mx, 2300 + my), (-1020 + mx, 2300 + my))
    img, mk = plano_persp(tex, dst, (p.w, p.h))
    m = mk[..., None]
    p.c = p.c * (1 - m) + img * m * np.array([0.68, 0.76, 0.76], np.float32)
    p.glow(W / 2, SUELO_Y + 20, 900, (70, 90, 90), 0.20, ry=70, pot=1.4)
    # rodapié
    p.poli(quad((-mx, SUELO_Y - 40), (W + mx, SUELO_Y - 40), (W + mx, SUELO_Y + 6), (-mx, SUELO_Y + 6)), (130, 100, 70), blur=0.8, rug=0.2, tex=0.04)
    # luz de luna por la ventana sobre la pared
    p.luz_poli(quad((700, 420), (980, 420), (1180, 1300), (520, 1300)), (120, 150, 230), 0.12, 40)
    p.viñeta(0.35, 2.0)
    capas.append((p.rgb(), -mx, -my, 1.0))

    # ---------------------------------------------------------- muebles, ventana, refri (rgba)
    q = _capa(mx, my, 82)
    # ventana sobre la tarja
    wx0, wy0, ww, wh = 690, 420, 280, 380
    q.poli(quad((wx0 - 24, wy0 - 24), (wx0 + ww + 24, wy0 - 24), (wx0 + ww + 24, wy0 + wh + 24), (wx0 - 24, wy0 + wh + 24)), (110, 120, 96), blur=0.7, rug=0.3, tex=0.05)
    q.poli(quad((wx0, wy0), (wx0 + ww, wy0), (wx0 + ww, wy0 + wh), (wx0, wy0 + wh)), (20, 24, 70), blur=0.7, rug=0.2, tex=0.03, grad=((70, 80, 150), wy0, wy0 + wh))
    q.elipse(wx0 + 190, wy0 + 110, 52, 52, (240, 234, 196), blur=1.0, rug=0.2, tex=0.03)
    q.glow(wx0 + 190, wy0 + 110, 180, (140, 150, 230), 0.4, pot=2.0)
    for xx in (wx0 + ww / 2,):
        q.poli(quad((xx - 7, wy0), (xx + 7, wy0), (xx + 7, wy0 + wh), (xx - 7, wy0 + wh)), (110, 120, 96), blur=0.5, rug=0.2, tex=0.03)
    q.poli(quad((wx0, wy0 + wh * 0.5), (wx0 + ww, wy0 + wh * 0.5), (wx0 + ww, wy0 + wh * 0.5 + 14), (wx0, wy0 + wh * 0.5 + 14)), (110, 120, 96), blur=0.5, rug=0.2, tex=0.03)
    q.poli(quad((wx0 - 36, wy0 + wh + 20), (wx0 + ww + 36, wy0 + wh + 20), (wx0 + ww + 44, wy0 + wh + 48), (wx0 - 44, wy0 + wh + 48)), (136, 146, 118), blur=0.7, rug=0.3, tex=0.05)
    # cortinitas a cuadros
    for sg, (cx0, cx1) in enumerate(((wx0 - 20, wx0 + 90), (wx0 + ww - 90, wx0 + ww + 20))):
        q.poli(quad((cx0, wy0 - 10), (cx1, wy0 - 10), (cx1 + (10 if sg else -10), wy0 + 190), (cx0 + (10 if sg else -10), wy0 + 190)), (176, 70, 70), blur=0.8, rug=0.6, tex=0.05)
        for k in range(5):
            q.poli(quad((cx0, wy0 + k * 40), (cx1, wy0 + k * 40), (cx1, wy0 + k * 40 + 14), (cx0, wy0 + k * 40 + 14)), (236, 226, 210), alfa=0.35, blur=0.7, rug=0.3, tex=0)
    # gabinetes altos y bajos (derecha)
    q.poli(rr(1000, 380, 220, 520, 14), (116, 90, 62), blur=0.8, rug=0.4, tex=0.06, grad=((76, 58, 44), 380, 900))
    q.poli(rr(1016, 396, 188, 488, 10), (146, 114, 78), alfa=0.6, blur=0.8, rug=0.4, tex=0.05)
    q.poli(rr(640, 1190, 600, 320, 8), (104, 82, 58), blur=0.8, rug=0.4, tex=0.06, grad=((72, 56, 44), 1190, 1510))
    for k, xx in enumerate((650, 850, 1050)):
        q.poli(rr(xx + 10, 1210, 170, 280, 10), (138, 108, 76), alfa=0.8, blur=0.8, rug=0.4, tex=0.05)
        q.elipse(xx + 150, 1330, 9, 9, (210, 180, 90), blur=0.5, rug=0, tex=0.0)
    q.poli(quad((620, 1170), (1260, 1170), (1260, 1198), (620, 1198)), (176, 184, 170), blur=0.8, rug=0.3, tex=0.05)         # mesón
    q.poli(quad((780, 1170), (960, 1170), (940, 1186), (800, 1186)), (60, 70, 70), blur=0.8, rug=0.3, tex=0.03)               # tarja
    gx, gy = GRIFO
    q.poli(quad((gx - 70, 1170), (gx - 54, 1170), (gx - 54, 960), (gx - 70, 960)), (186, 196, 200), blur=0.6, rug=0.2, tex=0.03)
    q.poli(quad((gx - 70, 960), (gx, 944), (gx, 972), (gx - 54, 982)), (186, 196, 200), blur=0.6, rug=0.2, tex=0.03)
    q.poli(quad((gx - 14, 972), (gx + 4, 972), (gx + 4, gy), (gx - 14, gy)), (170, 182, 188), blur=0.6, rug=0.2, tex=0.03)
    # estante con frascos sobre el salpicadero
    # refri: cuerpo y marco
    f = FRIDGE
    q.sombra_poli(quad((f["x0"] - 20, f["y1"] - 10), (f["x1"] + 120, f["y1"] - 10), (f["x1"] + 150, f["y1"] + 50), (f["x0"] - 40, f["y1"] + 50)), 0.55, 20)
    cuerpo = rr(f["x0"] - 16, f["y0"] - 16, f["x1"] - f["x0"] + 32, f["y1"] - f["y0"] + 22, 96, 10)
    q.poli(cuerpo, (96, 148, 126), blur=0.9, rug=0.4, tex=0.05, grad=((54, 92, 82), f["y0"], f["y1"]))
    # interior (se ve al abrir la puerta)
    ix0, ix1, iy0, iy1 = f["x0"] + 34, f["x1"] - 34, f["y0"] + 40, f["y1"] - 60
    q.poli(rr(ix0, iy0, ix1 - ix0, iy1 - iy0, 40, 8), (196, 232, 232), blur=0.8, rug=0.3, tex=0.04, grad=((150, 200, 206), iy0, iy1))
    q.glow((ix0 + ix1) / 2, iy0 + 40, 380, (200, 255, 250), 0.55, ry=260, pot=1.6)
    nsh = 5
    for k in range(nsh):
        yy = iy0 + 150 + k * (iy1 - iy0 - 170) / (nsh - 1)
        q.poli(quad((ix0, yy), (ix1, yy), (ix1, yy + 14), (ix0, yy + 14)), (230, 246, 246), blur=0.6, rug=0.2, tex=0.03)
        q.poli(quad((ix0, yy + 14), (ix1, yy + 14), (ix1, yy + 26), (ix0, yy + 26)), (130, 170, 176), alfa=0.8, blur=2.0, rug=0.2, tex=0)
    sh = [iy0 + 150 + k * (iy1 - iy0 - 170) / (nsh - 1) for k in range(nsh)]
    # contenido: leche, frasco, pastel, pescado en espinas, huevos, lechuga, botella
    q.poli(rr(ix0 + 22, sh[0] - 120, 70, 120, 6), (240, 240, 244), blur=0.6, rug=0.2, tex=0.04)
    q.poli(quad((ix0 + 22, sh[0] - 120), (ix0 + 92, sh[0] - 120), (ix0 + 74, sh[0] - 150), (ix0 + 40, sh[0] - 150)), (210, 214, 224), blur=0.6, rug=0.2, tex=0.04)
    q.poli(quad((ix0 + 30, sh[0] - 80), (ix0 + 84, sh[0] - 80), (ix0 + 84, sh[0] - 36), (ix0 + 30, sh[0] - 36)), (86, 120, 206), blur=0.5, rug=0.2, tex=0.03)
    q.poli(rr(ix0 + 250, sh[0] - 96, 66, 96, 14), (90, 150, 80), blur=0.6, rug=0.2, tex=0.04, grad=((60, 110, 56), sh[0] - 96, sh[0]))
    q.poli(rr(ix0 + 254, sh[0] - 120, 58, 26, 6), (220, 200, 90), blur=0.5, rug=0.2, tex=0.03)
    for k in range(6):
        q.elipse(ix0 + 60 + k * 36, sh[3] - 26, 17, 22, (240, 226, 190), blur=0.6, rug=0.2, tex=0.04)
    q.elipse(ix1 - 100, sh[3] - 44, 60, 44, (90, 168, 70), blur=0.8, rug=0.6, tex=0.06)
    q.poli(rr(ix0 + 250, sh[3] - 130, 44, 130, 12), (76, 130, 200), blur=0.6, rug=0.2, tex=0.04)
    q.poli(quad((ix0, sh[4] + 30), (ix1, sh[4] + 30), (ix1, iy1), (ix0, iy1)), (210, 238, 238), blur=0.6, rug=0.2, tex=0.03)
    # bandeja de verduras
    q.poli(rr(ix0 + 10, sh[4] + 40, ix1 - ix0 - 20, iy1 - sh[4] - 56, 14), (160, 200, 206), alfa=0.8, blur=0.8, rug=0.3, tex=0.04)
    # sombra interior para dar fondo
    q.sombra_poli(quad((ix0, iy0), (ix1, iy0), (ix1, iy0 + 50), (ix0, iy0 + 50)), 0.25, 14, (40, 70, 80))
    capas.append((q.rgba_auto(), -mx, -my, 1.0))
    return capas


# ================================================================ MESA (escena final): mantel de cuadros que cae hasta el piso
MESA = dict(x0=120.0, x1=1010.0, y_top=1392.0)


@cacheado
def mesa():
    """Capa por DELANTE de los personajes sentados: tablero y mantel a cuadros (esconde sus piernas)."""
    mx, my = 300, 300
    q = _capa(mx, my, 91)
    x0, x1, yt = MESA["x0"], MESA["x1"], MESA["y_top"]
    q.sombra_poli(quad((x0 - 30, 1690), (x1 + 50, 1690), (x1 + 90, 1760), (x0 - 40, 1760)), 0.55, 24)
    # tablero
    q.poli(quad((x0 - 30, yt - 6), (x1 + 30, yt - 6), (x1 + 40, yt + 30), (x0 - 40, yt + 30)), (150, 106, 70), blur=0.8, rug=0.4, tex=0.06, grad=((106, 74, 54), yt, yt + 30))
    # mantel (rojo con cuadros blancos) con borde ondulado
    ancho = x1 - x0
    base = quad((x0, yt + 24), (x1, yt + 24), (x1 + 16, 1692), (x0 - 16, 1692))
    q.poli(base, (176, 44, 56), blur=0.8, rug=0.5, tex=0.05, grad=((120, 28, 44), yt + 24, 1692))
    n = 56
    for r_ in range(0, 7):
        for c_ in range(0, int(ancho / n) + 1):
            if (r_ + c_) % 2:
                xx, yy = x0 + c_ * n, yt + 28 + r_ * n
                q.poli(quad((xx, yy), (xx + n, yy), (xx + n, yy + n), (xx, yy + n)), (244, 236, 226), alfa=0.78, blur=0.7, rug=0.3, tex=0.03)
    for k in range(0, int(ancho / 60) + 1):                        # festón del borde
        cx_ = x0 + 30 + k * 60
        q.elipse(cx_, 1692, 32, 22, (176, 44, 56) if k % 2 else (244, 236, 226), blur=0.8, rug=0.2, tex=0.04)
    q.poli(quad((x0 - 16, yt + 24), (x0 + 120, yt + 24), (x0 + 60, 1692), (x0 - 16, 1692)), (20, 10, 24), alfa=0.18, blur=18, rug=0.3, tex=0)
    return [(q.rgba_auto(), -mx, -my, 1.0)]
