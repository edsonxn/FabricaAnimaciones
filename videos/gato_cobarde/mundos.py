# -*- coding: utf-8 -*-
"""Fondos pintados de «Mostacho y el ruido de la cocina» (kit nucleo/toon_fondos.py). Cada función devuelve las CAPAS de una escena:
lista de (rgba_o_rgb, ox, oy, prof). Se pintan una vez por proceso (cache) y se pegan cada cuadro con paralaje (Toon.pegar_capa)."""
import math

import cv2
import numpy as np

from toon_fondos import Pintor, col, desenfoque, fbm, plano_persp, ruido_suave

W, H = 1080, 1920
_CACHE = {}


def cacheado(f):
    """Pinta una vez por proceso; solo se guardan los 2 últimos fondos (cada uno pesa ~300 MB)."""
    def g(*a, **k):
        key = (f.__name__,) + a
        if key not in _CACHE:
            while len(_CACHE) >= 2:
                _CACHE.pop(next(iter(_CACHE)))
            _CACHE[key] = f(*a, **k)
        else:
            _CACHE[key] = _CACHE.pop(key)
        return _CACHE[key]
    return g


def _capa(mx, my, seed=1, base=(0, 0, 0)):
    p = Pintor(W + 2 * mx, H + 2 * my, base, seed)
    p.o = np.array([float(mx), float(my)])
    return p


# ================================================================ EXTERIOR NOCHE
LUNA = (330, 560, 215)          # x, y, radio (mundo)
VENTANA = (704, 1150)           # centro de la ventana encendida


@cacheado
def exterior():
    """Capas del exterior nocturno: cielo, luna, nubes (2), mesetas, llano, casa+árbol, primer plano."""
    capas = []
    # ---- cielo + luna
    mx, my = 160, 260
    p = _capa(mx, my, 11)
    p.degradado([(0.0, (8, 8, 34)), (0.30, (22, 20, 70)), (0.55, (52, 46, 110)), (0.70, (96, 92, 150)), (0.80, (150, 168, 176)),
                 (1.0, (60, 92, 96))], y0=0, y1=p.h * 0.80, tex=0.03)
    # pinceladas largas horizontales del cielo (mano de pintura)
    cielo = np.array([(-mx, -my), (W + mx, -my), (W + mx, 1500), (-mx, 1500)], float)
    for k, (c, a_) in enumerate((((38, 30, 96), 0.16), ((18, 16, 60), 0.2), ((120, 110, 180), 0.07))):
        p.pinceladas(cielo, c, ang=-3 + 4 * k, n=520, largo=360, ancho=22, alfa=a_)
    # estrellas fijas muy pequeñas
    rng = np.random.default_rng(5)
    for _ in range(90):
        x, y = rng.uniform(-mx, W + mx), rng.uniform(-my, 900)
        if math.hypot(x - LUNA[0], y - LUNA[1]) < LUNA[2] * 1.5:
            continue
        p.glow(x, y, rng.uniform(3, 7), (255, 250, 220), rng.uniform(0.3, 0.9), pot=1.0)
    # luna: halo + disco + cráteres
    lx, ly, lr = LUNA
    p.glow(lx, ly, lr * 3.4, (120, 120, 190), 0.55, pot=2.4)
    p.glow(lx, ly, lr * 2.0, (190, 190, 210), 0.45, pot=2.0)
    p.elipse(lx, ly, lr, lr, (246, 240, 196), blur=1.2, rug=0.15, tex=0.04, grad=((226, 218, 168), ly - lr, ly + lr))
    for cx, cy, r in ((-60, -50, 46), (70, 20, 60), (-20, 90, 34), (40, -90, 28), (-110, 40, 24)):
        p.elipse(lx + cx, ly + cy, r, r * 0.92, (212, 204, 154), alfa=0.5, blur=4, rug=1.2, tex=0.05)
    capas.append((p.rgba_auto(), -mx, -my, 0.04))

    # ---- nubes (2 capas con transparencia, a distintas velocidades): masas blandas iluminadas por la luna
    for k, (prof, seed, y_c, alt) in enumerate(((0.07, 21, 330, 250), (0.16, 22, 700, 200))):
        mx_, my_ = 360, 160
        q = _capa(mx_, my_, seed)
        ww, hh = q.w, q.h
        r = np.random.default_rng(seed)
        base = cv2.resize(r.normal(0, 1, (hh // 120 + 2, ww // 520 + 2)).astype(np.float32), (ww, hh), interpolation=cv2.INTER_CUBIC)
        base = base + 0.55 * fbm(hh, ww, 150, 4, seed + 4)
        yy = np.arange(hh, dtype=np.float32)[:, None]
        banda = np.exp(-((yy - (y_c + my_)) / alt) ** 2)
        v = base * 0.5 + banda * 1.1 - 0.55
        a = np.clip(v * 1.8, 0, 1)
        a = a * a * (3 - 2 * a)
        # la luna queda despejada
        xx = np.arange(ww, dtype=np.float32)[None, :]
        dl = np.hypot(xx - (LUNA[0] + mx_), yy - (LUNA[1] + my_)) / (LUNA[2] * 1.35)
        a *= np.clip(dl - 0.55, 0, 1) ** 0.9 if k == 0 else np.clip(dl - 0.2, 0, 1)
        a = cv2.GaussianBlur(a, (0, 0), 2.5)
        # color: lila oscuro; más claro hacia la luna y en la parte alta de cada masa
        luz_luna = np.clip(1 - np.hypot((xx - (LUNA[0] + mx_)) / 1000.0, (yy - (LUNA[1] + my_)) / 1200.0), 0, 1) ** 1.3
        alto = np.clip(a - np.roll(a, 22, axis=0), 0, 1)             # el lado de arriba de cada nube recibe luz
        alto = cv2.GaussianBlur(alto, (0, 0), 7)
        c0 = col((34, 28, 84)) + (col((96, 88, 150)) - col((34, 28, 84))) * (luz_luna[..., None] * 0.9)
        q.c[:] = c0 + col((120, 118, 176)) * (alto * 1.6 * (0.35 + luz_luna))[..., None]
        q.c *= 1 + 0.07 * fbm(hh, ww, 36, 3, seed + 8)[..., None]
        q.c *= (1 + 0.05 * q.tp)[..., None]
        capas.append((q.rgba(a * (0.78 if k == 0 else 0.62)), -mx_, -my_, prof))

    # ---- mesetas lejanas
    mx_, my_ = 240, 60
    q = _capa(mx_, my_, 31)
    base_y = 1250
    pts = [(-mx_, base_y + 80)]
    x = -mx_
    rng = np.random.default_rng(3)
    alturas = [120, 210, 210, 120, 90, 260, 260, 150, 170, 170, 110, 220, 220, 100]
    for i, hgt in enumerate(alturas):
        x2 = x + rng.uniform(110, 210)
        pts += [(x, base_y - hgt * 0.25), (x + 24, base_y - hgt), (x2 - 24, base_y - hgt), (x2, base_y - hgt * 0.25)]
        x = x2
        if x > W + mx_:
            break
    pts += [(W + mx_, base_y + 80)]
    q.poli(np.array(pts), (36, 32, 84), blur=1.0, rug=0.5, tex=0.04, grad=((70, 84, 130), base_y - 260, base_y + 30))
    q.pinceladas(np.array(pts), (22, 18, 60), ang=-72, n=160, largo=110, ancho=10, alfa=0.22)
    q.glow(W / 2, base_y + 18, 760, (120, 160, 170), 0.55, ry=70, pot=1.4)
    capas.append((q.rgba_auto(), -mx_, -my_, 0.20))

    # ---- llano + camino (suelo seco violeta/ocre)
    mx_, my_ = 300, 200
    q = _capa(mx_, my_, 41)
    suelo = np.array([(-mx_, 1262), (W + mx_, 1262), (W + mx_, H + my_), (-mx_, H + my_)], float)
    q.poli(suelo, (92, 74, 100), blur=1.0, rug=0.0, tex=0.05, grad=((46, 34, 70), 1262, H + 100))
    q.pinceladas(suelo, (126, 96, 108), ang=2, n=900, largo=240, ancho=14, alfa=0.14)
    q.pinceladas(suelo, (30, 24, 56), ang=-2, n=700, largo=300, ancho=18, alfa=0.2)
    # camino de tierra hacia la casa
    cam = np.array([(500, H + my_), (600, H + my_), (734, 1344), (712, 1342)], float)
    q.poli(cam, (112, 92, 108), blur=2.4, rug=1.6, tex=0.05, grad=((70, 56, 84), 1340, H))
    q.pinceladas(cam, (140, 118, 128), ang=82, n=120, largo=110, ancho=6, alfa=0.14)
    for sx in (-14, 14):
        q.poli(np.array([(556 + sx * 2.4, H + my_), (562 + sx * 2.4, H + my_), (724 + sx * 0.5, 1346), (722 + sx * 0.5, 1346)], float), (38, 28, 56), alfa=0.5, blur=2, rug=1.0, tex=0)
    # luz de la luna sobre el camino y manchas de suelo
    q.luz_poli(np.array([(480, H), (620, H), (740, 1345), (716, 1342)], float), (96, 96, 160), 0.14, 24)
    q.glow(W / 2, 1268, 800, (130, 170, 176), 0.5, ry=60, pot=1.5)
    q.manchas(-mx_, 1280, W + mx_, H, (30, 24, 60), 26, 60, 220, 0.16)
    # arbustos secos / piedras
    for x, y, s in ((120, 1420, 1.0), (330, 1500, 0.8), (900, 1480, 1.1), (60, 1600, 1.4), (1010, 1630, 1.5), (260, 1700, 1.8)):
        arbusto_seco(q, x, y, s)
    capas.append((q.rgba_auto(), -mx_, -my_, 0.5))

    # ---- casa + árbol + molino (plano de los personajes, prof 1.0)
    mx_, my_ = 260, 200
    q = _capa(mx_, my_, 51)
    casa(q)
    arbol_seco(q, 960, 1352, 1.0)
    molino_base(q, 170, 1350)
    # sombras y luz de la ventana en el suelo
    q.luz_poli(np.array([(640, 1312), (772, 1312), (900, 1420), (560, 1420)], float), (255, 190, 90), 0.34, 28)
    q.glow(VENTANA[0], VENTANA[1], 220, (255, 170, 70), 0.34, pot=2.2)
    capas.append((q.rgba_auto(), -mx_, -my_, 1.0))
    return capas


def arbusto_seco(p, x, y, s=1.0):
    rng = np.random.default_rng(int(x * 7 + y))
    for k in range(9):
        a = math.radians(-90 + rng.uniform(-60, 60))
        L = rng.uniform(26, 62) * s
        P = np.array([(x, y), (x + math.cos(a) * L * 0.5 + rng.uniform(-6, 6), y + math.sin(a) * L * 0.5), (x + math.cos(a) * L, y + math.sin(a) * L)])
        # ramita como polígono fino
        d = P[-1] - P[0]
        n = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-9)
        Q = np.vstack([P + n * 2.0 * s, (P - n * 1.2 * s)[::-1]])
        p.poli(Q, (30, 22, 40), blur=0.6, rug=0.0, tex=0.0)
    p.elipse(x, y + 4 * s, 24 * s, 7 * s, (22, 16, 36), blur=3, rug=0, tex=0, alfa=0.7)


def arbol_seco(p, x, base_y, s=1.0):
    """Árbol muerto: tronco que se retuerce y ramas que se bifurcan (recursivo)."""
    rng = np.random.default_rng(77)

    def rama(x0, y0, ang, L, w, prof):
        if prof == 0 or w < 2.2:
            return
        n = 8
        ang_v = ang
        pts = [(x0, y0)]
        for i in range(n):
            ang_v += rng.normal(0, 0.18)
            pts.append((pts[-1][0] + math.cos(ang_v) * L / n, pts[-1][1] + math.sin(ang_v) * L / n))
        pts = np.array(pts)
        ws = np.linspace(w, w * 0.62, len(pts))
        d = np.gradient(pts, axis=0)
        nr = np.stack([-d[:, 1], d[:, 0]], 1) / (np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9)
        Q = np.vstack([pts + nr * (ws / 2)[:, None], (pts - nr * (ws / 2)[:, None])[::-1]])
        p.poli(Q, (30, 24, 52), blur=0.8, rug=0.8, tex=0.04)
        # luz de luna en el borde izquierdo
        p.poli(np.vstack([pts + nr * (ws / 2)[:, None], (pts + nr * (ws / 2 - 3)[:, None])[::-1]]), (130, 130, 190), alfa=0.5, blur=0.6, rug=0, tex=0)
        for k in (3, 6):
            for sg in (-1, 1):
                rama(pts[k][0], pts[k][1], ang_v + sg * rng.uniform(0.5, 0.9), L * 0.62, w * 0.55, prof - 1)
        rama(pts[-1][0], pts[-1][1], ang_v + rng.normal(0, 0.2), L * 0.7, w * 0.6, prof - 1)
    rama(x, base_y, math.radians(-96), 300 * s, 46 * s, 5)
    p.elipse(x, base_y + 6, 50 * s, 10 * s, (18, 14, 34), blur=4, rug=0, tex=0, alfa=0.7)


def casa(p):
    """Casa torcida en la nada: paredes de tablones, techo hundido, porche, chimenea y ventana encendida."""
    rng = np.random.default_rng(9)
    # sombra en el suelo
    p.sombra_poli(np.array([(470, 1350), (1000, 1350), (1050, 1400), (430, 1400)], float), 0.5, 18)
    # pared principal (ligeramente inclinada)
    pared = np.array([(540, 1020), (886, 1006), (900, 1340), (528, 1346)], float)
    p.poli(pared, (96, 70, 96), blur=0.8, rug=0.5, tex=0.05, grad=((54, 40, 74), 1000, 1346))
    # tablones verticales
    for i in range(14):
        x = 540 + i * 26 + rng.uniform(-3, 3)
        p.poli(np.array([(x, 1016 - i * 0.5), (x + 2.6, 1016 - i * 0.5), (x + 3.4, 1344), (x + 0.8, 1344)], float), (30, 20, 44), alfa=0.55, blur=0.5, rug=0.3, tex=0.0)
    p.pinceladas(pared, (150, 118, 140), ang=90, n=120, largo=140, ancho=6, alfa=0.10)
    p.pinceladas(pared, (24, 16, 40), ang=90, n=170, largo=150, ancho=8, alfa=0.17)
    # luna: luz fría en el borde izquierdo
    p.poli(np.array([(540, 1020), (580, 1018), (572, 1344), (528, 1346)], float), (120, 124, 196), alfa=0.28, blur=6, rug=0.5, tex=0.0)
    # hastial: la pared triangular bajo el techo
    p.poli(np.array([(522, 1054), (702, 924), (908, 1032), (900, 1070), (530, 1070)], float), (84, 60, 88), blur=0.8, rug=0.5, tex=0.05, grad=((58, 44, 78), 930, 1070))
    for i in range(8):
        x = 540 + i * 46
        p.poli(np.array([(x, 1040), (x + 2.6, 1040), (x + 3, 1068), (x + 0.4, 1068)], float), (30, 20, 44), alfa=0.5, blur=0.5, rug=0.3, tex=0.0)
    # techo hundido (dos aguas torcido)
    techo = np.array([(496, 1030), (700, 884), (930, 1000), (910, 1034), (700, 940), (520, 1058)], float)
    p.poli(techo, (30, 24, 58), blur=0.8, rug=1.0, tex=0.05)
    for i in range(7):
        y = 900 + i * 22
        p.poli(np.array([(540 + (y - 900) * 0.0, y + 34 - i * 2), (700, y - 4), (900, y + 70 - i * 3)], float), (50, 40, 84), alfa=0.0)
    p.pinceladas(techo, (88, 76, 140), ang=-25, n=80, largo=100, ancho=7, alfa=0.2)
    # remate del techo con luz
    p.poli(np.array([(496, 1030), (700, 884), (708, 892), (510, 1040)], float), (150, 150, 210), alfa=0.55, blur=0.8, rug=0.2, tex=0)
    # chimenea torcida
    p.poli(np.array([(800, 960), (840, 950), (848, 880), (806, 884)], float), (52, 40, 78), blur=0.8, rug=0.8, tex=0.05)
    # porche: techito + dos postes + escalón
    p.poli(np.array([(470, 1210), (610, 1180), (620, 1200), (478, 1236)], float), (36, 26, 56), blur=0.8, rug=0.6, tex=0.05)
    for x in (484, 600):
        p.poli(np.array([(x, 1226), (x + 12, 1224), (x + 14, 1350), (x + 2, 1352)], float), (62, 46, 70), blur=0.6, rug=0.5, tex=0.04)
    p.poli(np.array([(452, 1350), (640, 1346), (648, 1372), (446, 1378)], float), (60, 44, 66), blur=0.8, rug=0.5, tex=0.04)
    # puerta oscura
    p.poli(np.array([(530, 1240), (594, 1236), (596, 1348), (532, 1352)], float), (18, 12, 32), blur=0.7, rug=0.4, tex=0.03)
    # ventana grande iluminada con cruz y cortina
    vx, vy = VENTANA
    marco = np.array([(vx - 70, vy - 86), (vx + 66, vy - 90), (vx + 70, vy + 82), (vx - 66, vy + 88)], float)
    p.poli(marco, (40, 28, 52), blur=0.6, rug=0.4, tex=0.03)
    cristal = np.array([(vx - 58, vy - 74), (vx + 54, vy - 78), (vx + 58, vy + 70), (vx - 54, vy + 76)], float)
    p.poli(cristal, (255, 214, 120), blur=0.8, rug=0.3, tex=0.03, grad=((255, 150, 60), vy - 80, vy + 80))
    p.pinceladas(cristal, (255, 240, 180), ang=-80, n=40, largo=60, ancho=8, alfa=0.2)
    p.poli(np.array([(vx - 4, vy - 78), (vx + 6, vy - 78), (vx + 8, vy + 74), (vx - 2, vy + 76)], float), (40, 28, 52), blur=0.5, rug=0.3, tex=0)
    p.poli(np.array([(vx - 56, vy - 2), (vx + 56, vy - 8), (vx + 56, vy + 4), (vx - 56, vy + 6)], float), (40, 28, 52), blur=0.5, rug=0.3, tex=0)
    # cortina dobladita
    p.poli(np.array([(vx - 58, vy - 76), (vx - 20, vy - 76), (vx - 36, vy - 10), (vx - 54, vy + 10)], float), (180, 60, 70), alfa=0.8, blur=1.0, rug=0.8, tex=0.05)
    # ventana pequeña tapiada
    p.poli(np.array([(790, 1140), (850, 1136), (852, 1210), (792, 1214)], float), (28, 20, 44), blur=0.6, rug=0.4, tex=0.03)
    for dy in (-20, 4, 28):
        p.poli(np.array([(782, 1176 + dy), (860, 1170 + dy), (860, 1182 + dy), (782, 1188 + dy)], float), (84, 62, 74), blur=0.5, rug=0.5, tex=0.04)
    # buzón y letrero torcido
    p.poli(np.array([(412, 1290), (425, 1290), (426, 1352), (413, 1352)], float), (40, 32, 56), blur=0.6, rug=0.3, tex=0.02)
    p.poli(np.array([(396, 1262), (448, 1260), (450, 1292), (398, 1294)], float), (150, 56, 60), blur=0.6, rug=0.5, tex=0.04)
    # sombra alargada de la casa para anclarla
    p.sombra_poli(np.array([(520, 1346), (900, 1340), (930, 1368), (500, 1376)], float), 0.55, 10)
    # viñeta de pintura sobre toda la casa (más oscuro en los bordes)


def molino_base(p, x, base_y):
    """Torre del molino de viento (las aspas se dibujan con tinta, animadas, en la escena)."""
    h = 430
    for s in (-1, 1):
        p.poli(np.array([(x + s * 56, base_y), (x + s * 50, base_y), (x + s * 8, base_y - h), (x + s * 14, base_y - h)], float), (36, 28, 60), blur=0.6, rug=0.4, tex=0.03)
    for k in range(7):
        y = base_y - 30 - k * 60
        w = 52 * (1 - (base_y - y) / (h + 30)) + 8
        p.poli(np.array([(x - w, y), (x + w, y - 4), (x + w, y + 5), (x - w, y + 9)], float), (36, 28, 60), blur=0.5, rug=0.3, tex=0.02)
        p.poli(np.array([(x - w, y), (x + w * 0.6, y - 58), (x + w * 0.6 + 4, y - 54), (x - w + 4, y + 4)], float), (36, 28, 60), alfa=0.8, blur=0.5, rug=0.3, tex=0.02)
    p.elipse(x, base_y + 5, 72, 10, (18, 14, 34), blur=4, rug=0, tex=0, alfa=0.7)
    return (x, base_y - h)
