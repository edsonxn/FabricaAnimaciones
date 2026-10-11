# -*- coding: utf-8 -*-
"""Mapa continuo (estilo Kurzgesagt): de Mesoamérica al valle de México y hasta la cuadrícula de la ciudad vista
desde arriba. Coordenadas del mapa: X = (lon + 99) * K, Y = -(lat - 19.6) * K (px a zoom 1).
Cámara: (lon, lat, z) -> el punto cae en el centro de la pantalla (960, 540) con zoom z."""
import math

import numpy as np

from motor import (W, H, prog, lerp, smooth, e_out, circulo, elipse, rect_red, blob, h01, catmull, bezier, ruido1)
import plano as P

K = 400.0
TEO = (-98.845, 19.692)
CDMX = (-99.133, 19.433)
UNIT = 0.36                    # px de mapa por unidad de ciudad (100 m)
ROT_CIUDAD = math.radians(15.5)

MAR_A = (18, 40, 104)
MAR_B = (34, 92, 164)
TIERRA = (214, 160, 100)
TIERRA_S = (170, 108, 96)
TIERRA_L = (236, 190, 128)
SELVA = (104, 164, 112)
LAGO = (70, 150, 214)
LAGO_L = (122, 196, 240)

PLACA_MEX = [(-105.4, 23.0), (-106.4, 24.8), (-106.0, 27.5), (-98.0, 27.5), (-97.4, 25.4), (-97.8, 23.4),
             (-97.3, 21.6), (-96.5, 20.2), (-95.8, 18.9), (-94.6, 18.2), (-93.2, 18.4), (-91.6, 18.7), (-90.6, 19.6),
             (-90.3, 21.0), (-89.3, 21.4), (-88.0, 21.6), (-86.8, 21.1), (-87.4, 19.7), (-87.9, 18.5), (-88.3, 17.4),
             (-88.9, 15.9), (-87.8, 15.8), (-86.8, 15.9), (-86.2, 14.0), (-87.4, 13.0), (-89.0, 13.4), (-90.4, 13.8),
             (-91.8, 14.4), (-93.1, 15.3), (-94.3, 16.2), (-95.5, 15.9), (-97.2, 15.8), (-98.5, 16.2), (-99.9, 16.8),
             (-101.0, 17.3), (-102.2, 17.9), (-103.6, 18.4), (-104.9, 19.1), (-105.6, 20.2), (-105.3, 21.3)]

SELVAS = [(-89.7, 17.2, 2.2), (-91.8, 17.4, 1.6), (-95.2, 17.9, 1.0), (-88.6, 19.1, 1.3), (-93.0, 16.1, 1.0)]

LUGARES = {
    "teo": (TEO[0], TEO[1]),
    "pachuca": (-98.74, 20.12),
    "oaxaca": (-96.72, 17.06),
    "golfo": (-96.13, 19.18),
    "tikal": (-89.62, 17.22),
}


def XY(lon, lat):
    return (lon + 99.0) * K, -(lat - 19.6) * K


def lonlat_ciudad(u, v):
    """Coordenadas (lon, lat) del punto de la ciudad (u este, v norte, en unidades de 100 m)."""
    x, y = u * UNIT, -v * UNIT
    c, s_ = math.cos(ROT_CIUDAD), math.sin(ROT_CIUDAD)
    xr, yr = x * c - y * s_, x * s_ + y * c
    return TEO[0] + xr / K, TEO[1] - yr / K


def scr(cam, lon, lat):
    lo, la, z = cam
    x, y = XY(lon, lat)
    x0, y0 = XY(lo, la)
    return 960 + (x - x0) * z, 540 + (y - y0) * z


def _poly(lonlat):
    return np.array([XY(a, b) for a, b in lonlat], float)


def alfa_lod(z, z0, z1):
    """0 con z<=z0 y 1 con z>=z1 (en escala logarítmica)."""
    return smooth(prog(math.log(z), math.log(z0), math.log(z1)))


def alfa_lod_inv(z, z0, z1):
    return 1.0 - alfa_lod(z, z0, z1)


def _rect(x0, y0, x1, y1):
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float)


# ======================================================================== ciudad vista desde arriba
def cuadrado_conc(lz, cx, cy, lado, n, col_a, col_b, prof=0.0):
    """Pirámide vista desde arriba: n cuadrados concéntricos, con sombra hacia abajo-derecha."""
    for i in range(n):
        f = 1 - i / (n + 0.6) * 0.86
        h = lado * f / 2
        off = prof * (i + 1)
        lz.relleno(_rect(cx - h + off * 0.9, cy - h + off, cx + h + off * 0.9, cy + h + off), (96, 48, 96), alfa=0.6)
    for i in range(n):
        f = 1 - i / (n + 0.6) * 0.86
        h = lado * f / 2
        off = prof * i
        lz.relleno(_rect(cx - h + off * 0.3, cy - h + off * 0.3, cx + h + off * 0.3, cy + h + off * 0.3),
                   col_a if i % 2 == 0 else col_b)


def ciudad_arriba(lz, t, est, z):
    """Dibuja la ciudad en unidades de 100 m (u hacia el este, y = -v hacia el norte)."""
    a_det = est.get("ciudad_alfa", 1.0)
    if a_det <= 0.01:
        return
    a_gr = alfa_lod(z, 6, 30)                     # manzanas y calles
    a_pi = alfa_lod(z, 25, 90)                    # pirámides y plazas
    a_dt = alfa_lod(z, 130, 320)                  # detalle de escalones
    # mancha de la ciudad
    lz.halo(0, 0, 40, (255, 226, 170), alfa=0.35 * a_det * alfa_lod_inv(z, 4, 20))
    huella = blob(0, -0.5, 23.5, 3, 0.05, 90, 6)
    lz.relleno(huella, (252, 226, 184), alfa=a_det)
    if a_gr > 0.01:
        # manzanas: calles finas opacas (color ya mezclado con la huella) recortadas a la mancha de la ciudad
        col_calle = P.mezcla((252, 226, 184), (214, 148, 116), 0.6 * a_gr * a_det)
        R = 22.3                                     # radio seguro dentro de la mancha (sin recorte: mucho más rápido)
        for k in range(-22, 23):
            c = math.sqrt(max(R * R - k * k, 0.0))
            if c > 0.5:
                lz.relleno(_rect(k - 0.06, -0.5 - c, k + 0.06, -0.5 + c), col_calle)
        for k in range(-22, 22):
            c = math.sqrt(max(R * R - (k + 0.5) ** 2, 0.0))
            if c > 0.5:
                lz.relleno(_rect(-c, k - 0.06, c, k + 0.06), col_calle)
    # Calzada de los Muertos (v de -25 a 24 -> y de 25 a -24)
    lz.relleno(_rect(-0.22, -24.5, 0.22, 25), (252, 230, 196), alfa=a_det)
    lz.relleno(_rect(-22.5, 10.75, 22.5, 11.25), (252, 230, 196), alfa=0.9 * a_det * a_gr)
    # Ciudadela (este de la calzada, v = -11)
    if a_pi > 0.01:
        with lz.grupo(0, 0, 1.0):
            lz.relleno(_rect(0.8, 8.9, 5.2, 13.3), (250, 208, 150), alfa=a_pi)
            lz.relleno(_rect(0.8, 8.9, 5.2, 9.2), (200, 130, 110), alfa=a_pi)
            lz.relleno(_rect(1.1, 9.5, 4.9, 9.7), (200, 130, 110), alfa=0.8 * a_pi)
            cuadrado_conc(lz, 3.0, 11.0, 1.4, 3, (226, 110, 90), (255, 170, 120), 0.03)
        # Pirámide del Sol (este, v = 7 -> y = -7)
        cuadrado_conc(lz, 1.9, -7.0, 2.2, 5, (226, 104, 88), (255, 176, 124), 0.05 if a_dt > 0.1 else 0.03)
        # Pirámide de la Luna (v = 21.5) y su plaza
        lz.relleno(_rect(-1.4, -23.4, 1.4, -19.9), (250, 214, 160), alfa=a_pi)
        cuadrado_conc(lz, 0.0, -21.4, 1.5, 4, (226, 104, 88), (255, 176, 124), 0.04)
        # plataformas a lo largo de la calzada
        for i in range(-9, 9):
            for sgn in (-1, 1):
                v = -1.2 + i * 2.6
                if abs(v - 7) < 2.4 or abs(v + 11) < 3.2 or abs(v - 21) < 2:
                    continue
                lz.relleno(_rect(sgn * 0.8 - 0.35, -v - 0.35, sgn * 0.8 + 0.35, -v + 0.35), (230, 130, 100), alfa=a_pi)
    # gente: puntos que se mueven por la calzada
    g = est.get("gente_top", 0.0)
    if g > 0.02:
        n = 500
        us = (np.array([h01(4, i) for i in range(n)]) - 0.5) * 0.36
        vs = np.array([h01(5, i) for i in range(n)])
        vel = 0.6 + np.array([h01(6, i) for i in range(n)])
        vv = -24.0 + ((vs * 49.0 + vel * t * 2.2) % 49.0)
        pts = np.stack([us, vv], 1)
        lz.puntos(pts[: int(n * g)], 0.09, (255, 244, 220))


# ======================================================================== valle
LAGOS = [(-98.99, 19.44, 0.20, 0.30, 1), (-99.08, 19.27, 0.16, 0.10, 2), (-99.07, 19.32, 0.12, 0.09, 3),
         (-99.14, 19.76, 0.10, 0.12, 4), (-99.0, 19.66, 0.09, 0.10, 5), (-98.96, 19.62, 0.08, 0.08, 6)]
MONTES = [(-98.63, 19.03, 46, 5), (-98.64, 19.18, 40, 6), (-98.62, 19.4, 22, 7), (-99.25, 19.2, 26, 8),
          (-99.34, 19.4, 24, 9), (-99.30, 19.6, 22, 10), (-99.10, 19.6, 14, 11), (-98.80, 19.56, 16, 12),
          (-98.83, 19.76, 20, 13), (-98.55, 19.7, 20, 14), (-99.4, 19.15, 22, 15), (-98.6, 19.9, 20, 16),
          (-99.35, 19.85, 20, 17), (-98.95, 19.95, 20, 18), (-99.15, 19.98, 18, 19), (-98.4, 19.5, 20, 20)]


def montana(lz, x, y, s, semilla):
    lz.relleno(np.array([[x - s, y], [x, y - s * 1.1], [x + s, y]]), (170, 112, 96))
    lz.relleno(np.array([[x, y - s * 1.1], [x + s, y], [x + s * 0.1, y]]), (128, 82, 96))
    lz.relleno(np.array([[x - s * 0.22, y - s * 0.84], [x, y - s * 1.1], [x + s * 0.22, y - s * 0.84]]), (250, 244, 240))


def valle(lz, t, est, z):
    a = alfa_lod(z, 0.9, 2.2)
    if a <= 0.01:
        return
    # parcelas y relieve suave para que el suelo no quede liso
    for i in range(46):
        lo = -100.0 + 2.6 * h01(61, i)
        la = 18.5 + 2.0 * h01(62, i)
        x, y = XY(lo, la)
        col = (226, 176, 112) if i % 2 else (196, 140, 92)
        lz.relleno(blob(x, y, 30 + 60 * h01(63, i), 70 + i, 0.35, 40, 5), col, alfa=0.55 * a)
    # lagos
    for (lo, la, w, h, sd) in LAGOS:
        x, y = XY(lo, la)
        b = blob(x, y, 1.0, sd, 0.28, 60, 4)
        b[:, 0] = x + (b[:, 0] - x) * w * K * 0.6
        b[:, 1] = y + (b[:, 1] - y) * h * K * 0.6
        lz.relleno(b, LAGO_L, alfa=a * 0.55)
        b2 = b.copy()
        b2[:, 0] = x + (b[:, 0] - x) * 0.88
        b2[:, 1] = y + (b[:, 1] - y) * 0.88
        lz.relleno(b2, LAGO, alfa=a)
        if est.get("lago_brillo", 0):
            lz.halo(x, y, w * K * 0.7, LAGO_L, alfa=0.25 * a)
    # montañas
    for (lo, la, s, sd) in MONTES:
        x, y = XY(lo, la)
        montana(lz, x, y + 8, s * (1.0 + 0.0), sd)
    # Ciudad de México (hoy)
    x, y = XY(*CDMX)
    ah = est.get("cdmx", 0.0) * a
    if ah > 0.01:
        lz.relleno(blob(x, y, 26, 21, 0.3, 60, 6), (120, 116, 158), alfa=0.9 * ah)
        lz.relleno(blob(x, y, 15, 22, 0.3, 60, 6), (168, 166, 206), alfa=0.9 * ah)


# ======================================================================== mapa completo
def mapa(lz, t, cam, est):
    """Dibuja el mapa. Devuelve nada; etiquetas en capa 2 (pantalla)."""
    lo, la, z = cam
    from mundo import degradado_v
    degradado_v(lz, -10, W + 10, -10, H + 10, MAR_A, MAR_B, 0, H, paso=14.0)
    cx, cy = XY(lo, la)
    with lz.grupo(960 - cx * z, 540 - cy * z, z):
        land = _poly(PLACA_MEX)
        # costa: aureola clara de aguas someras
        for k, al in ((26, 0.10), (14, 0.16), (6, 0.22)):
            m = land.mean(0)
            lz.relleno(m + (land - m) * (1 + k / 1500.0), (80, 170, 220), alfa=al)
        lz.relleno(land + np.array([0, 9 / max(z, 0.2) ** 0.4]), TIERRA_S)
        with lz.recorte(land):                       # tierra con degradado por bandas (solo la franja visible)
            degradado_v(lz, cx - 1000 / z, cx + 1000 / z, cy - 560 / z, cy + 560 / z, TIERRA_L, TIERRA,
                        XY(0, 27)[1], XY(0, 14)[1], paso=max(3.0, 12.0 / z))
        for (a, b, r) in SELVAS:
            x, y = XY(a, b)
            lz.relleno(blob(x, y, r * K * 0.30, int(a * 10), 0.3, 60, 5), SELVA, alfa=0.85)
        valle(lz, t, est, z)
        # ciudad vista desde arriba, en el sitio de Teotihuacán
        tx, ty = XY(*TEO)
        with lz.grupo(tx, ty, UNIT, ROT_CIUDAD):
            ciudad_arriba(lz, t, est, z)
        # rutas comerciales
        rr = est.get("rutas", 0.0)
        if rr > 0.01:
            for k, (nom, col, curv) in enumerate((("pachuca", (120, 230, 170), 0.1), ("oaxaca", (255, 214, 96), 0.2),
                                                   ("golfo", (255, 150, 110), -0.15), ("tikal", (255, 110, 170), -0.12))):
                fr = e_out(prog(rr, k * 0.2, k * 0.2 + 0.55))
                if fr <= 0.001:
                    continue
                x0, y0 = XY(*TEO)
                x1, y1 = XY(*LUGARES[nom])
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                nx, ny = -(y1 - y0), (x1 - x0)
                c = (mx + nx * curv, my + ny * curv)
                pts = bezier((x0, y0), c, c, (x1, y1), 60)
                P.discontinua(lz, pts, col, ancho=9.0 / z ** 0.5, largo=40 / z ** 0.5, hueco=26 / z ** 0.5,
                              fase=-t * 30 / z ** 0.5, frac=fr)
    return None


def marcador(lz, cam, lugar, texto, alfa=1.0, dx=0.0, dy=-56.0, color=(255, 214, 96), px=40, punto=True):
    """Punto brillante + etiqueta (en pantalla)."""
    lo, la = LUGARES[lugar] if isinstance(lugar, str) else lugar
    x, y = scr(cam, lo, la)
    if alfa <= 0.01 or x < -200 or x > W + 200 or y < -100 or y > H + 100:
        return
    with lz.capa(2):
        if punto:
            lz.halo(x, y, 34, color, alfa=0.7 * alfa)
            lz.relleno(circulo(x, y, 9, 20), (255, 255, 255), alfa=alfa)
        P.pastilla(lz, x + dx, y + dy, texto, px=px, alfa=alfa)
