# -*- coding: utf-8 -*-
"""Fondo del PASILLO (plano lateral largo por el que la cámara acompaña al gato, de derecha a izquierda): papel pintado oscuro, lambrín,
tablas del suelo, puerta cerrada, mesita con florero, perchero con sombrero y tres retratos SIN OJOS (los ojos se dibujan con tinta en la
escena y siguen al gato). A la izquierda, el hueco de la cocina con luz fría; a la derecha, la puerta de la sala."""
import math

import numpy as np

from motor import rect_red as _rr
from mundos import H, _capa, cacheado
from toon_fondos import Pintor

X0, X1 = -300, 3300          # el mundo pintado va de X0 a X1
SUELO_Y = 1590               # línea del suelo (pies del gato)
PUERTA_COCINA = (330, 650)   # x0, x1 del hueco de la cocina (izquierda)
PUERTA_SALA = (2860, 3120)
# retratos: (x, y, ancho, alto, ojo izq (dx, dy), ojo der (dx, dy), radio) relativos al centro del cuadro
RETRATOS = [
    dict(x=2150, y=720, w=250, h=330, oi=(-38, -30), od=(38, -30), r=19, tipo="vieja"),
    dict(x=1500, y=700, w=270, h=330, oi=(-44, -22), od=(44, -22), r=21, tipo="bigote"),
    dict(x=1000, y=760, w=230, h=290, oi=(-34, -18), od=(34, -18), r=20, tipo="lobo"),
]


def quad(*pts):
    return np.array(pts, float)


def rr(x, y, w, h, r, n=8):
    return _rr(x, y, w, h, r, n)


def _canvas(ancho, alto, mx_izq, my, seed):
    p = Pintor(ancho, alto, (0, 0, 0), seed)
    p.o = np.array([float(mx_izq), float(my)])
    return p


def marco(q, x, y, w, h, oval=False):
    if oval:
        q.elipse(x, y, w / 2 + 22, h / 2 + 22, (160, 118, 52), blur=0.8, rug=0.5, tex=0.06)
        q.elipse(x, y, w / 2 + 6, h / 2 + 6, (96, 66, 34), blur=0.8, rug=0.3, tex=0.04)
        q.elipse(x, y, w / 2 - 6, h / 2 - 6, (40, 34, 44), blur=0.8, rug=0.2, tex=0.03)
    else:
        q.poli(rr(x - w / 2 - 20, y - h / 2 - 20, w + 40, h + 40, 12), (160, 118, 52), blur=0.8, rug=0.5, tex=0.06)
        q.poli(rr(x - w / 2 - 6, y - h / 2 - 6, w + 12, h + 12, 6), (96, 66, 34), blur=0.8, rug=0.3, tex=0.04)
        q.poli(rr(x - w / 2, y - h / 2, w, h, 4), (44, 38, 52), blur=0.8, rug=0.2, tex=0.03)


def retrato(q, d):
    x, y, w, h = d["x"], d["y"], d["w"], d["h"]
    tipo = d["tipo"]
    oval = tipo == "vieja"
    marco(q, x, y, w, h, oval)
    # fondo del cuadro con degradado
    if oval:
        q.elipse(x, y, w / 2 - 6, h / 2 - 6, (70, 66, 60), blur=0.8, rug=0.3, tex=0.04, grad=((34, 30, 30), y - h / 2, y + h / 2))
    else:
        q.poli(rr(x - w / 2, y - h / 2, w, h, 4), (74, 64, 52), blur=0.8, rug=0.3, tex=0.04, grad=((34, 30, 30), y - h / 2, y + h / 2))
    # hombros
    q.poli(quad((x - w / 2 + 6, y + h / 2 - 4), (x - w * 0.34, y + h * 0.22), (x - w * 0.12, y + h * 0.12), (x + w * 0.12, y + h * 0.12),
                (x + w * 0.34, y + h * 0.22), (x + w / 2 - 6, y + h / 2 - 4)), (24, 22, 34), blur=0.8, rug=0.5, tex=0.04)
    if tipo == "vieja":
        q.poli(quad((x - 30, y + h * 0.1), (x + 30, y + h * 0.1), (x + 40, y + h * 0.3), (x - 40, y + h * 0.3)), (210, 200, 180), blur=0.8, rug=0.4, tex=0.04)
        q.elipse(x, y - 8, 66, 84, (214, 184, 156), blur=0.8, rug=0.3, tex=0.04, grad=((178, 146, 124), y - 90, y + 80))
        q.elipse(x, y - 78, 74, 40, (170, 168, 176), blur=0.8, rug=0.5, tex=0.05)            # pelo gris
        q.elipse(x, y - 118, 28, 24, (170, 168, 176), blur=0.8, rug=0.5, tex=0.05)             # moño
        q.poli(quad((x - 8, y + 4), (x + 8, y + 4), (x + 4, y + 26), (x - 4, y + 26)), (190, 148, 124), blur=0.8, rug=0.2, tex=0.0)
        q.poli(quad((x - 22, y + 46), (x + 22, y + 46), (x + 14, y + 52), (x - 14, y + 52)), (120, 50, 60), blur=0.6, rug=0.2, tex=0.0)   # boca fruncida
        for sx in (-1, 1):
            q.poli(quad((x + sx * 24, y - 62), (x + sx * 56, y - 54), (x + sx * 56, y - 48), (x + sx * 24, y - 56)), (90, 82, 84), blur=0.6, rug=0.2, tex=0.0)   # cejas
    elif tipo == "bigote":
        q.elipse(x, y - 10, 70, 88, (224, 176, 140), blur=0.8, rug=0.3, tex=0.04, grad=((186, 134, 106), y - 96, y + 80))
        q.elipse(x, y - 86, 70, 24, (214, 168, 134), blur=0.8, rug=0.3, tex=0.04)             # calva
        for sx in (-1, 1):
            q.elipse(x + sx * 74, y - 6, 12, 28, (60, 50, 50), blur=0.8, rug=0.4, tex=0.04)      # patillas
            q.elipse(x + sx * 76, y - 6, 12, 28, (214, 168, 134), alfa=0.0)
        q.poli(quad((x - 10, y + 8), (x + 10, y + 8), (x + 8, y + 30), (x - 8, y + 30)), (196, 140, 114), blur=0.8, rug=0.2, tex=0.0)   # nariz
        for sx in (-1, 1):
            q.poli(quad((x, y + 36), (x + sx * 36, y + 28), (x + sx * 74, y + 14), (x + sx * 70, y + 48), (x + sx * 34, y + 50), (x, y + 44)),
                   (40, 30, 34), blur=0.7, rug=0.6, tex=0.04)                             # bigote enorme
        for sx in (-1, 1):
            q.poli(quad((x + sx * 22, y - 56), (x + sx * 60, y - 50), (x + sx * 60, y - 42), (x + sx * 22, y - 48)), (60, 50, 52), blur=0.6, rug=0.2, tex=0.0)
        q.elipse(x - 44, y - 22, 34, 34, (210, 220, 240), alfa=0.0)
    else:  # lobo
        q.elipse(x, y - 6, 78, 92, (128, 112, 100), blur=0.8, rug=0.8, tex=0.05, grad=((92, 80, 76), y - 96, y + 80))
        for sx in (-1, 1):
            q.poli(quad((x + sx * 40, y - 74), (x + sx * 78, y - 118), (x + sx * 88, y - 56)), (110, 96, 88), blur=0.7, rug=0.5, tex=0.05)
            q.poli(quad((x + sx * 50, y - 72), (x + sx * 76, y - 104), (x + sx * 80, y - 62)), (200, 130, 130), blur=0.7, rug=0.3, tex=0.03)
        q.elipse(x, y + 30, 46, 40, (170, 156, 140), blur=0.8, rug=0.6, tex=0.05)            # hocico
        q.elipse(x, y + 8, 14, 10, (24, 20, 26), blur=0.6, rug=0.2, tex=0.0)                  # nariz
        q.poli(quad((x - 26, y + 40), (x + 26, y + 40), (x + 18, y + 62), (x - 18, y + 62)), (70, 20, 34), blur=0.6, rug=0.3, tex=0.0)
        for k in (-14, -4, 6, 16):
            q.poli(quad((x + k - 3, y + 40), (x + k + 3, y + 40), (x + k, y + 52)), (240, 236, 224), blur=0.4, rug=0.0, tex=0.0)
        q.poli(quad((x - 70, y + 30), (x - 98, y + 56), (x - 56, y + 60)), (128, 112, 100), blur=0.7, rug=0.5, tex=0.05)
        q.poli(quad((x + 70, y + 30), (x + 98, y + 56), (x + 56, y + 60)), (128, 112, 100), blur=0.7, rug=0.5, tex=0.05)
    # cuencas de los ojos (oscuras) donde se dibujan los ojos animados
    for ex, ey in (d["oi"], d["od"]):
        q.elipse(x + ex, y + ey, d["r"] + 5, d["r"] + 4, (30, 22, 30), blur=0.8, rug=0.2, tex=0.0)
    # brillo del barniz
    q.poli(quad((x - w / 2, y - h / 2), (x - w / 2 + 70, y - h / 2), (x - w / 2 + 20, y + h / 2), (x - w / 2, y + h / 2)), (255, 255, 255), alfa=0.05, blur=3, rug=0.2, tex=0.0)


@cacheado
def pasillo():
    capas = []
    ancho = X1 - X0
    my = 200
    p = _canvas(ancho, H + 2 * my, -X0, my, 71)
    # ------------------------------------------------ pared + suelo opacos
    p.degradado([(0.0, (22, 26, 40)), (0.45, (46, 56, 66)), (0.68, (58, 64, 70)), (0.74, (44, 32, 30)), (1.0, (30, 22, 24))], y0=0, y1=p.h, tex=0.03)
    pared = quad((X0, -my), (X1, -my), (X1, SUELO_Y), (X0, SUELO_Y))
    for i, x in enumerate(range(X0, X1, 110)):
        if i % 2 == 0:
            p.poli(quad((x, -my), (x + 55, -my), (x + 55, SUELO_Y), (x, SUELO_Y)), (70, 54, 82), alfa=0.20, blur=0.8, rug=0.0, tex=0.0)
    for r_, y in enumerate(range(-80, 1350, 150)):
        for c_, x in enumerate(range(X0 + (55 if r_ % 2 else 0), X1, 110)):
            if c_ % 2:
                continue
            p.poli(quad((x + 27, y - 20), (x + 42, y), (x + 27, y + 20), (x + 12, y)), (110, 96, 130), alfa=0.22, blur=0.8, rug=0.3, tex=0.0)
    p.pinceladas(pared, (14, 18, 34), ang=90, n=900, largo=300, ancho=24, alfa=0.14)
    p.manchas(X0, -my, X1, 1300, (14, 18, 32), 90, 90, 320, 0.2)
    # cornisa y lambrín
    p.poli(quad((X0, -my), (X1, -my), (X1, 130), (X0, 150)), (20, 24, 38), blur=1, rug=0, tex=0.03)
    p.poli(quad((X0, 130), (X1, 130), (X1, 158), (X0, 176)), (92, 76, 66), blur=1, rug=0.2, tex=0.04)
    p.poli(quad((X0, 1250), (X1, 1250), (X1, SUELO_Y), (X0, SUELO_Y)), (88, 62, 52), blur=0.8, rug=0.2, tex=0.05, grad=((58, 40, 36), 1250, SUELO_Y))
    for x in range(X0, X1, 190):
        p.poli(rr(x + 16, 1290, 158, 250, 8), (66, 46, 40), alfa=0.8, blur=0.8, rug=0.3, tex=0.04)
        p.poli(rr(x + 24, 1298, 142, 234, 6), (100, 72, 58), alfa=0.5, blur=0.8, rug=0.3, tex=0.04)
    p.poli(quad((X0, 1236), (X1, 1236), (X1, 1262), (X0, 1262)), (138, 106, 84), blur=0.8, rug=0.2, tex=0.04)
    p.poli(quad((X0, SUELO_Y - 40), (X1, SUELO_Y - 40), (X1, SUELO_Y + 4), (X0, SUELO_Y + 4)), (56, 40, 36), blur=0.8, rug=0.2, tex=0.04)
    # suelo de tablas (vista lateral, baja): juntas verticales y vetas horizontales
    suelo = quad((X0, SUELO_Y), (X1, SUELO_Y), (X1, H + my), (X0, H + my))
    p.poli(suelo, (90, 60, 48), blur=0.6, rug=0, tex=0.05, grad=((44, 28, 28), SUELO_Y, H + 100))
    for k in range(9):
        y = SUELO_Y + 14 * (1.5 ** k) - 14
        p.poli(quad((X0, y), (X1, y), (X1, y + 3 + k * 1.4), (X0, y + 3 + k * 1.4)), (24, 16, 18), alfa=0.55, blur=0.8, rug=0.3, tex=0)
    for x in range(X0, X1, 230):
        k = (x // 230) % 3
        p.poli(quad((x + 60 * k, SUELO_Y), (x + 60 * k + 5, SUELO_Y), (x + 60 * k + 16, H + my), (x + 60 * k + 6, H + my)), (24, 16, 18), alfa=0.5, blur=0.7, rug=0.3, tex=0)
    p.pinceladas(suelo, (140, 98, 72), ang=0, n=700, largo=300, ancho=14, alfa=0.10)
    # alfombra larga de pasillo
    p.poli(quad((X0, SUELO_Y + 80), (X1, SUELO_Y + 80), (X1, SUELO_Y + 260), (X0, SUELO_Y + 260)), (100, 36, 46), blur=1.0, rug=0.4, tex=0.06, grad=((70, 24, 38), SUELO_Y + 80, SUELO_Y + 260))
    for x in range(X0, X1, 90):
        p.poli(quad((x, SUELO_Y + 96), (x + 40, SUELO_Y + 96), (x + 40, SUELO_Y + 104), (x, SUELO_Y + 104)), (160, 110, 70), alfa=0.5, blur=0.6, rug=0.2, tex=0)
        p.poli(quad((x, SUELO_Y + 236), (x + 40, SUELO_Y + 236), (x + 40, SUELO_Y + 244), (x, SUELO_Y + 244)), (160, 110, 70), alfa=0.5, blur=0.6, rug=0.2, tex=0)
    # hueco de la cocina (izquierda): oscuro con luz fría que se derrama
    a, b = PUERTA_COCINA
    p.poli(quad((a - 44, 470), (b + 44, 470), (b + 44, SUELO_Y + 4), (a - 44, SUELO_Y + 4)), (112, 88, 70), blur=0.8, rug=0.3, tex=0.05)
    p.poli(quad((a, 520), (b, 520), (b, SUELO_Y + 4), (a, SUELO_Y + 4)), (36, 80, 78), blur=0.8, rug=0.2, tex=0.02, grad=((8, 20, 30), 520, SUELO_Y))
    p.glow((a + b) / 2, 1200, 330, (110, 230, 200), 0.36, ry=620, pot=1.5)
    p.luz_poli(quad((a, SUELO_Y), (b + 420, SUELO_Y), (b + 880, H + my), (a - 120, H + my)), (90, 220, 190), 0.20, 30)
    # puerta de la sala (derecha): marco y hueco azulado
    a, b = PUERTA_SALA
    p.poli(quad((a - 44, 470), (b + 44, 470), (b + 44, SUELO_Y + 4), (a - 44, SUELO_Y + 4)), (112, 88, 70), blur=0.8, rug=0.3, tex=0.05)
    p.poli(quad((a, 520), (b, 520), (b, SUELO_Y + 4), (a, SUELO_Y + 4)), (24, 36, 70), blur=0.8, rug=0.2, tex=0.02, grad=((10, 14, 34), 520, SUELO_Y))
    p.glow((a + b) / 2, 1200, 300, (70, 120, 220), 0.22, ry=560, pot=1.6)
    p.viñeta(0.30, 2.0)
    capas.append((p.rgb(), X0, -my, 1.0))

    # ------------------------------------------------ muebles, puerta, retratos (rgba)
    oy = 300
    q = _canvas(ancho, 1500, -X0, -oy, 72)
    for d in RETRATOS:
        retrato(q, d)
    # puerta cerrada
    dx = 1830
    q.poli(quad((dx - 130, 560), (dx + 130, 560), (dx + 130, SUELO_Y + 2), (dx - 130, SUELO_Y + 2)), (96, 66, 50), blur=0.8, rug=0.3, tex=0.05, grad=((66, 44, 40), 560, SUELO_Y))
    q.poli(quad((dx - 138, 548), (dx + 138, 548), (dx + 138, 566), (dx - 138, 566)), (130, 100, 76), blur=0.8, rug=0.3, tex=0.05)
    for yy in (610, 900):
        q.poli(rr(dx - 94, yy, 188, 240, 10), (72, 48, 40), alfa=0.8, blur=0.8, rug=0.4, tex=0.05)
        q.poli(rr(dx - 84, yy + 10, 168, 220, 8), (110, 78, 60), alfa=0.5, blur=0.8, rug=0.4, tex=0.05)
    q.elipse(dx + 90, 1150, 16, 16, (200, 160, 70), blur=0.6, rug=0, tex=0.04)
    q.poli(quad((dx - 126, 1176), (dx + 126, 1176), (dx + 130, SUELO_Y + 2), (dx - 130, SUELO_Y + 2)), (20, 14, 20), alfa=0.35, blur=1, rug=0.2, tex=0)
    q.poli(rr(dx - 40, 460, 80, 56, 6), (166, 130, 66), blur=0.6, rug=0.3, tex=0.04)      # placa con número
    # mesita con florero seco (derecha)
    mx_ = 2560
    q.poli(quad((mx_ - 110, 1330), (mx_ + 110, 1330), (mx_ + 110, 1352), (mx_ - 110, 1352)), (118, 84, 64), blur=0.7, rug=0.3, tex=0.05)
    for sx in (-1, 1):
        q.poli(quad((mx_ + sx * 92 - 8, 1352), (mx_ + sx * 92 + 8, 1352), (mx_ + sx * 92 + 6, SUELO_Y + 2), (mx_ + sx * 92 - 6, SUELO_Y + 2)), (78, 54, 44), blur=0.7, rug=0.3, tex=0.05)
    q.elipse(mx_, 1250, 54, 82, (60, 90, 110), blur=0.8, rug=0.3, tex=0.05, grad=((100, 130, 150), 1170, 1330))
    q.poli(quad((mx_ - 20, 1180), (mx_ + 20, 1180), (mx_ + 14, 1130), (mx_ - 14, 1130)), (60, 90, 110), blur=0.7, rug=0.2, tex=0.04)
    for k, ang in enumerate((-0.7, -0.25, 0.15, 0.55)):
        a1 = (mx_, 1130)
        L = 120 + 30 * (k % 2)
        a2 = (mx_ + math.sin(ang) * L, 1130 - math.cos(ang) * L)
        q.poli(quad((a1[0] - 3, a1[1]), (a1[0] + 3, a1[1]), (a2[0] + 2, a2[1]), (a2[0] - 2, a2[1])), (40, 30, 34), blur=0.6, rug=0.2, tex=0)
        q.elipse(a2[0], a2[1], 10, 8, (90, 50, 60), blur=0.6, rug=0.3, tex=0.04)
    q.sombra_poli(quad((mx_ - 120, SUELO_Y - 4), (mx_ + 140, SUELO_Y - 4), (mx_ + 150, SUELO_Y + 30), (mx_ - 110, SUELO_Y + 30)), 0.45, 10)
    # perchero con sombrero y bufanda (parece alguien parado)
    px = 1250
    q.poli(quad((px - 8, 720), (px + 8, 720), (px + 10, SUELO_Y + 2), (px - 10, SUELO_Y + 2)), (40, 30, 34), blur=0.7, rug=0.3, tex=0.04)
    q.poli(quad((px - 50, SUELO_Y - 6), (px + 50, SUELO_Y - 6), (px + 60, SUELO_Y + 10), (px - 60, SUELO_Y + 10)), (40, 30, 34), blur=0.7, rug=0.3, tex=0.04)
    for sx in (-1, 1):
        q.poli(quad((px, 730), (px + sx * 70, 690), (px + sx * 74, 698), (px + 4 * sx, 742)), (40, 30, 34), blur=0.7, rug=0.3, tex=0.04)
    q.elipse(px, 700, 66, 14, (24, 20, 30), blur=0.7, rug=0.3, tex=0.03)                    # sombrero
    q.poli(rr(px - 36, 640, 72, 62, 12), (24, 20, 30), blur=0.7, rug=0.4, tex=0.03)
    q.poli(quad((px - 36, 676), (px + 36, 676), (px + 36, 690), (px - 36, 690)), (150, 40, 50), blur=0.6, rug=0.2, tex=0.03)
    q.poli(quad((px - 70, 760), (px - 40, 760), (px - 34, 1080), (px - 60, 1090)), (80, 70, 130), blur=0.8, rug=0.6, tex=0.05)   # bufanda
    q.poli(quad((px + 40, 820), (px + 100, 800), (px + 120, 1200), (px + 54, 1220)), (30, 26, 40), blur=0.8, rug=0.7, tex=0.04)      # abrigo
    # sombras de contacto bajo todo
    q.sombra_poli(quad((X0, SUELO_Y - 6), (X1, SUELO_Y - 6), (X1, SUELO_Y + 26), (X0, SUELO_Y + 26)), 0.20, 8)
    capas.append((q.rgba_auto(), X0, oy, 1.0))

    # ------------------------------------------------ primer plano: helecho y barandilla muy oscuros y desenfocados
    from toon_fondos import desenfoque
    f = _canvas(ancho + 1200, H + 2 * my, -(X0 - 600), my, 73)
    rng = np.random.default_rng(31)
    for cx in (2300, 4300):
        base = H + 40
        f.poli(quad((cx - 70, base), (cx + 70, base), (cx + 50, base - 90), (cx - 50, base - 90)), (10, 8, 16), blur=1, rug=0.5, tex=0.02)
        for k in range(14):
            a = math.radians(-90 + rng.uniform(-70, 70))
            L = rng.uniform(230, 480)
            p0 = (cx + rng.uniform(-30, 30), base - 120)
            p1 = (p0[0] + math.cos(a) * L * 0.5, p0[1] + math.sin(a) * L * 0.55 - 40)
            p2 = (p0[0] + math.cos(a) * L, p0[1] + math.sin(a) * L * 0.9 + 60)
            from toon import bezier2
            c = bezier2(p0, p1, p2, 14)
            d = np.gradient(c, axis=0)
            nr = np.stack([-d[:, 1], d[:, 0]], 1) / (np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9)
            w = np.linspace(22, 2, len(c))
            f.poli(np.vstack([c + nr * w[:, None], (c - nr * w[:, None])[::-1]]), (10, 8, 18), blur=1.2, rug=0.6, tex=0.02)
    capas.append((desenfoque(f.rgba_auto(), 5.0), -(X0 - 600), -my, 1.35))
    return capas
