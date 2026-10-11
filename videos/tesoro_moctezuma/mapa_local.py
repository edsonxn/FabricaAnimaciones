# -*- coding: utf-8 -*-
"""Mapa local del valle de México en 1519-1521 (esquemático, en km): el lago de Texcoco, la isla-ciudad de Tenochtitlan (con Tlatelolco), las
calzadas (Tacuba al oeste, Tepeyac al norte, Iztapalapa al sur) y, en la escena del lago que se seca, la ciudad moderna encima.
Unidades del mundo: 1 km = PXKM px a zoom 1. x hacia el este, y hacia el norte (se dibuja invertido). Cámara: (cx_km, cy_km, z)."""
import math

import numpy as np

from motor import W, H, prog, lerp, smooth, circulo, elipse, rect_red, blob, catmull, bezier, h01, ruido1
import plano as P
from util import cam, K

PXKM = 120.0

# contorno esquemático del lago de Texcoco (más los brazos hacia Xochimilco y Zumpango), en km respecto a Tenochtitlan
LAGO = [(-4.6, 0.6), (-3.9, 3.6), (-2.3, 6.9), (0.6, 9.6), (4.6, 10.6), (9.6, 9.6), (14.6, 6.0), (17.6, 0.5), (16.0, -5.6), (11.6, -9.6),
        (6.0, -12.6), (1.6, -14.6), (-1.6, -11.0), (-3.4, -6.5), (-4.5, -2.6)]
CENTRO_SECO = (2.0, -1.0)           # hacia dónde se encoge el lago
CALZADAS = {
    "tacuba": [(-1.35, 0.05), (-2.9, 0.05), (-4.6, 0.1)],
    "tepeyac": [(0.2, 1.9), (0.5, 4.0), (0.9, 6.0)],
    "iztapalapa": [(0.1, -1.2), (0.6, -4.5), (2.0, -7.5), (3.6, -9.8)],
}
CIUDADES = {"tacuba": (-4.9, 0.15), "tepeyac": (1.0, 6.3), "iztapalapa": (3.8, -10.2), "chapultepec": (-4.6, -1.0), "texcoco": (14.5, 2.5)}

TIERRA_D, TIERRA_N = (222, 170, 108), (48, 40, 92)
LAGO_D, LAGO_N = (74, 152, 214), (26, 58, 128)


def km(x, y):
    return x * PXKM, -y * PXKM


def _kp(pts):
    return np.array([km(a, b) for a, b in pts], float)


def lago_pts(f=1.0, t=0.0, ola=0.0):
    """Polígono del lago escalado hacia CENTRO_SECO (f=1 completo, f→0 casi seco)."""
    c = np.array(CENTRO_SECO)
    p = np.array(LAGO, float)
    p = c + (p - c) * f
    if ola:
        p = p + np.stack([np.sin(t * 0.8 + np.arange(len(p)) * 1.7), np.cos(t * 0.7 + np.arange(len(p)) * 2.3)], 1) * ola
    return _kp(catmull(p, 10, True))


def _montana(lz, x, y, s, noche):
    c1 = P.mezcla((170, 112, 96), (58, 50, 104), noche)
    c2 = P.mezcla((128, 82, 96), (40, 34, 84), noche)
    lz.relleno(np.array([[x - s, y], [x, y - s * 1.1], [x + s, y]]), c1)
    lz.relleno(np.array([[x, y - s * 1.1], [x + s, y], [x + s * 0.1, y]]), c2)


def isla_pts():
    a = elipse(0.0, 0.1, 1.55, 1.2, 0.0, 40)
    return _kp(a)


def dibujar_valle(lz, t, c, noche=1.0, lago=1.0, luces=1.0, detalle=1.0, moderna=0.0, ciudad=1.0, calz=1.0, ola=0.05, etiquetas=0.0):
    """c = (cx_km, cy_km, z). Dibuja tierra, montañas, lago, isla-ciudad con calzadas y (opcional) la ciudad moderna."""
    cx, cy, z = c
    with cam(lz, cx * PXKM, -cy * PXKM, z):
        # tierra
        tierra = P.mezcla(TIERRA_D, TIERRA_N, noche)
        lz.relleno(np.array([[-9000, -9000], [9000, -9000], [9000, 9000], [-9000, 9000]]), tierra)
        for i in range(26):
            x, y = km(-16 + 36 * h01(21, i), -16 + 30 * h01(22, i))
            lz.relleno(blob(x, y, (120 + 300 * h01(23, i)), 30 + i, 0.35, 40, 5), P.mezcla(tierra, (255, 240, 200) if i % 2 else (90, 60, 60), 0.10), alfa=0.6)
        # montañas del entorno (Chapultepec, Peñón, Tepeyac, Estrella)
        for (mx, my, s) in ((-4.9, -1.0, 46), (1.2, 6.5, 70), (7.9, -11.2, 90), (-8.0, 5.0, 150), (-8.5, -6.0, 170), (20.0, -8.0, 200), (19.0, 8.0, 190)):
            x, y = km(mx, my)
            _montana(lz, x, y, s, noche)
        # lago
        if lago > 0.01:
            L = lago_pts(lago, t, ola)
            m = L.mean(0)
            lz.relleno(m + (L - m) * 1.018, P.mezcla(LAGO_D, (170, 226, 250), 0.25) if noche < 0.5 else P.mezcla(LAGO_N, (90, 150, 210), 0.35), alfa=0.85)
            lz.relleno(L, P.mezcla(LAGO_D, LAGO_N, noche))
            if z > 0.55:
                for i in range(40):
                    ux = -3.5 + 20 * h01(31, i)
                    uy = -12.0 + 21 * h01(32, i)
                    x, y = km(ux, uy)
                    x += 14 * math.sin(t * 0.6 + i)
                    lz.relleno(rect_red(x - 22, y, 44, 2.6, 1), (200, 230, 250), alfa=0.20 * lago)
        # ciudad moderna (por encima del lago seco)
        if moderna > 0.01:
            _ciudad_moderna(lz, t, moderna, noche)
        # isla ciudad
        if ciudad > 0.01:
            _isla(lz, t, noche, luces, detalle, ciudad, calz)
        if etiquetas > 0.01:
            pass


def _isla(lz, t, noche, luces, detalle, alfa, calz):
    # calzadas
    if calz > 0.01:
        for nom, pts in CALZADAS.items():
            q = _kp(catmull(pts, 12))
            for i in range(len(q) - 1):
                x0, y0 = q[i]
                x1, y1 = q[i + 1]
                dx, dy = x1 - x0, y1 - y0
                L = math.hypot(dx, dy) + 1e-6
                nx, ny = -dy / L * 7.0, dx / L * 7.0
                lz.relleno(np.array([[x0 - nx, y0 - ny], [x0 + nx, y0 + ny], [x1 + nx, y1 + ny], [x1 - nx, y1 - ny]]),
                           P.mezcla((214, 186, 150), (96, 84, 120), noche), alfa=calz)
    I = isla_pts()
    lz.relleno(I * 1.02, (250, 240, 214) if noche < 0.5 else (110, 96, 130), alfa=alfa)
    lz.relleno(I, P.mezcla((238, 214, 172), (64, 54, 100), noche), alfa=alfa)
    # tlatelolco
    lz.relleno(_kp(elipse(0.1, 1.5, 0.75, 0.62, 0.0, 30)), P.mezcla((238, 214, 172), (64, 54, 100), noche), alfa=alfa)
    if detalle > 0.02:
        for gx in range(-8, 9):
            for gy in range(-7, 8):
                ux, uy = gx * 0.17, gy * 0.15 + 0.1
                if (ux / 1.5) ** 2 + ((uy - 0.1) / 1.15) ** 2 > 0.86:
                    continue
                if abs(ux) < 0.11 and abs(uy) < 0.17:
                    continue
                x, y = km(ux, uy)
                col = P.mezcla((250, 244, 230), (96, 84, 128), noche) if (gx + gy) % 3 else P.mezcla((226, 196, 156), (80, 66, 110), noche)
                lz.relleno(rect_red(x - 9, y - 8, 18, 15, 2), col, alfa=detalle * alfa)
                if noche > 0.4 and luces > 0.05 and h01(gx, gy, 3) > 0.55:
                    lz.relleno(rect_red(x - 2, y - 3, 4, 4, 1), (255, 226, 130), alfa=luces * 0.9 * detalle)
        if detalle > 0.5:
            # templo mayor (icono cenital: cuadrados concéntricos) y palacios
            x, y = km(0.0, 0.0)
            for i in range(4):
                h = 24 - i * 5
                lz.relleno(rect_red(x - h, y - h, 2 * h, 2 * h, 0), (250, 236, 210) if i % 2 == 0 else (206, 176, 150), alfa=detalle)
            lz.relleno(rect_red(x - 5, y - 5, 10, 10, 0), (222, 70, 78), alfa=detalle)
    if noche > 0.4 and luces > 0.05:
        lz.halo(0, 0, 260, (255, 210, 130), alfa=0.35 * luces * alfa)


def _ciudad_moderna(lz, t, a, noche):
    """Retícula de calles y luces sobre el antiguo lecho: se llena desde el centro hacia afuera."""
    rng = np.random.RandomState(7)
    n = 900
    pts = []
    for i in range(n):
        r = abs(rng.normal(0, 7.5))
        ang = rng.uniform(0, 6.283)
        x, y = math.cos(ang) * r * 1.15, math.sin(ang) * r * 0.9 - 1.0
        pts.append((x, y))
    col = (255, 214, 120) if noche > 0.4 else (176, 172, 196)
    for (x, y) in pts:
        px, py = km(round(x / 0.25) * 0.25, round(y / 0.25) * 0.25)
        lz.relleno(rect_red(px - 6, py - 5, 12, 10, 1), P.mezcla((120, 116, 150), (90, 84, 130), noche), alfa=0.9 * a)
    for k in range(-30, 31):
        lz.relleno(rect_red(km(k * 0.5, 0)[0] - 1.2, -PXKM * 12, 2.4, PXKM * 24, 0), (200, 196, 226), alfa=0.16 * a)
        lz.relleno(rect_red(-PXKM * 15, -km(0, k * 0.5)[1] * 0 - k * 0.5 * PXKM - 1.2, PXKM * 32, 2.4, 0), (200, 196, 226), alfa=0.16 * a)
    lz.halo(0, 0, 900, col, alfa=0.16 * a * (0.6 + 0.4 * noche))
