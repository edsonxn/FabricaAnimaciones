# -*- coding: utf-8 -*-
"""Subsuelo (corte de la mina), patio de beneficio, vaca y escudo. Unidades locales (ver locales.py)."""
import math

import numpy as np

import vox as V
from locales import MADERA, ROJIZO, chispa
from motor import clamp01, e_back, h01, lerp, rect_red

ESTRATOS = [(0, (176, 112, 84)), (230, (216, 172, 122)), (620, (150, 124, 120)), (1150, (124, 102, 118)),
            (1750, (98, 86, 110)), (2400, (72, 66, 94)), (3100, (54, 50, 76))]
POZO_X = -40.0
ROCA_MIN = (128, 120, 118)


def _borde_onda(x0, x1, y, seed, amp=22.0):
    xs = np.linspace(x0, x1, 22)
    return np.stack([xs, y + amp * np.sin(xs / 130.0 + seed) + 0.5 * amp * np.sin(xs / 47.0 + seed * 1.7)], 1)


def seccion(lz, x0=-620, x1=620, alfa=1.0, capa=1, oscuridad=0.0):
    """Corte de tierra con estratos de papel, desde la superficie (y=0) hasta y=3500."""
    n = len(ESTRATOS)
    for i, (y, col) in enumerate(ESTRATOS):
        ynext = ESTRATOS[i + 1][0] if i + 1 < n else 3500
        arriba = _borde_onda(x0, x1, y, i + 1, 18 if i else 0)
        abajo = _borde_onda(x0, x1, ynext, i + 2, 18)[::-1]
        lz.relleno(np.vstack([arriba, abajo]), V.oscurecer(col, oscuridad), temblor=0.0, capa=capa, alfa=alfa, seed=i)


def veta(lz, t, alfa=1.0, brillo=1.0, capa=1, hasta=1.0):
    """Veta de plata: cinta clara diagonal entre las rocas, con nódulos y destellos."""
    pts = np.array([[-520, 560], [-380, 900], [-210, 1240], [-60, 1600], [120, 1980], [300, 2330], [460, 2640]])
    k = max(2, int(2 + (len(pts) - 2) * clamp01(hasta)))
    lz.relleno(np.vstack([pts[:k] + [-16, 0], (pts[:k] + [16, 0])[::-1]]), (214, 188, 150), temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(np.vstack([pts[:k] + [-6, 0], (pts[:k] + [6, 0])[::-1]]), V.PLATA, temblor=0.0, capa=capa, alfa=alfa)
    for i in range(1, k - 1):
        x, y = pts[i]
        lz.relleno(V.poligono_reg(x, y, 20, 6, i), V.aclarar(V.PLATA, 0.5), temblor=0.0, capa=capa, alfa=alfa, seed=i)
        chispa(lz, x + 30, y - 24, 16 * brillo, t + i, seed=i, capa=2, alfa=alfa * 0.9)


def pozo(lz, y0=20, y1=2800, alfa=1.0, capa=1):
    x = POZO_X
    lz.relleno(np.array([[x - 56, y0], [x + 56, y0], [x + 56, y1], [x - 56, y1]]), (34, 26, 30), temblor=0.0, capa=capa, alfa=alfa)
    for y in np.arange(y0 + 60, y1, 190):
        lz.relleno(rect_red(x - 62, y, 124, 14, 4), MADERA, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(rect_red(x - 62, y - 100, 12, 100, 3), V.oscurecer(MADERA, 0.15), temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(rect_red(x + 50, y - 100, 12, 100, 3), V.oscurecer(MADERA, 0.15), temblor=0.0, capa=capa, alfa=alfa)


def galeria(lz, y, x_a, x_b, alto=120, alfa=1.0, capa=1):
    xa, xb = min(x_a, x_b), max(x_a, x_b)
    lz.relleno(np.array([[xa, y - alto], [xb, y - alto], [xb, y], [xa, y]]), (30, 24, 28), temblor=0.0, capa=capa, alfa=alfa)
    for x in np.arange(xa + 40, xb, 150):
        lz.relleno(rect_red(x - 8, y - alto, 16, alto, 3), MADERA, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(rect_red(x - 30, y - alto - 2, 60, 14, 3), V.oscurecer(MADERA, 0.12), temblor=0.0, capa=capa, alfa=alfa)


def escala_tronco(lz, p0, p1, alfa=1.0, capa=1):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    lz.relleno(V.capsula(p0, p1, 24, 24), (154, 112, 76), temblor=0.0, capa=capa, alfa=alfa)
    d = p1 - p0
    L = np.hypot(*d)
    for k in range(1, int(L / 34)):
        q = p0 + d * (k * 34 / L)
        lz.trazo(np.array([q + [-10, 0], q + [10, 0]]), (96, 66, 44), 4, afinar=False, temblor=0.0, capa=capa)


ESCALERA = [(-40, 2200), (-70, 2050), (10, 1900), (-70, 1750), (10, 1600), (-70, 1450), (10, 1300), (-70, 1150),
            (10, 1000), (-70, 850), (10, 700), (-70, 550), (10, 400), (-70, 250), (10, 100), (-40, 20)]


def punto_escalera(u):
    """Posición (x, y), dirección de mirada y tramo de un cargador que sube por las escalas (u 0..1)."""
    P = np.array(ESCALERA, float)
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0], np.cumsum(seg)])
    L = d[-1] * clamp01(u)
    k = min(len(seg) - 1, int(np.searchsorted(d, L, side="right") - 1))
    f = (L - d[k]) / max(1e-9, seg[k])
    p = P[k] + (P[k + 1] - P[k]) * f
    return p, (1 if P[k + 1][0] > P[k][0] else -1), k


def escaleras(lz, alfa=1.0, capa=1):
    P = np.array(ESCALERA, float)
    for i in range(len(P) - 1):
        escala_tronco(lz, P[i], P[i + 1], alfa, capa)


def luz_vela(lz, x, y, r, t, alfa=1.0, seed=0):
    f = 1 + 0.06 * math.sin(t * 13 + seed) + 0.04 * math.sin(t * 31 + seed * 2)
    lz.halo(x, y, r * f, (255, 190, 90), alfa=0.55 * alfa, dureza=1.4, capa=2)
    lz.halo(x, y, r * 0.35 * f, (255, 226, 150), alfa=0.6 * alfa, dureza=1.2, capa=2)


def mineral(lz, x, y, s=1.0, capa=1, plata=False, seed=0):
    with lz.grupo(x, y, s):
        for i in range(5):
            lz.relleno(V.poligono_reg(-40 + i * 20, -8 - (i % 2) * 14, 18 + (i * 7) % 8, 5, i),
                       ROCA_MIN if i % 2 else (96, 90, 90), temblor=0.0, capa=capa, seed=seed + i)
        if plata:
            lz.relleno(V.poligono_reg(0, -26, 12, 5, 0.4), V.PLATA, temblor=0.0, capa=capa)


def patio(lz, x, y, rx, ry, t, alfa=1.0, capa=1, mezcla_prog=0.0):
    """Patio de beneficio en 3/4: empedrado, torta de lodo (mineral + sal + mercurio)."""
    lz.relleno(V.elipse_pts(x, y + 18, rx * 1.04, ry * 1.06), (96, 66, 50), temblor=0.0, capa=capa, alfa=alfa * 0.8)
    lz.relleno(V.elipse_pts(x, y, rx, ry), (188, 156, 118), temblor=0.0, capa=capa, alfa=alfa)
    for i in range(34):
        a = i * 2.399
        r = math.sqrt((i + 0.5) / 34)
        lz.relleno(V.elipse_pts(x + rx * 0.93 * r * math.cos(a), y + ry * 0.93 * r * math.sin(a), 20, 10),
                   V.mezcla((168, 138, 104), (204, 176, 138), h01(6, i)), temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(V.elipse_pts(x, y, rx * 0.62, ry * 0.6), (92, 82, 84), temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(V.elipse_pts(x - rx * 0.06, y - ry * 0.05, rx * 0.5, ry * 0.46), (118, 108, 110), temblor=0.0, capa=capa, alfa=alfa)
    n = int(24 * clamp01(mezcla_prog))
    for i in range(n):
        a = i * 2.9 + 0.7
        r = 0.9 * math.sqrt((i + 1) / 24)
        px, py = x + rx * 0.5 * r * math.cos(a), y + ry * 0.46 * r * math.sin(a)
        lz.relleno(V.elipse_pts(px, py, 8, 6), V.PLATA, temblor=0.0, capa=capa, alfa=alfa)
        lz.puntos([(px - 2, py - 2)], 2.2, (255, 255, 255), capa=capa)


def monton_sal(lz, x, y, s=1.0, capa=1):
    with lz.grupo(x, y, s):
        lz.relleno(np.array([[-46, 0], [-8, -60], [10, -50], [46, 0]]), (246, 244, 240), temblor=0.0, capa=capa)
        lz.relleno(np.array([[10, -50], [46, 0], [18, 0]]), (206, 206, 210), temblor=0.0, capa=capa)


def vaca(lz, x, y, s=1.0, dir=1, capa=1):
    with lz.grupo(x, y, s * dir, sy=s):
        c = (230, 216, 190)
        for dx in (-46, -22, 30, 54):
            lz.relleno(V.capsula([dx, -60], [dx, 0], 14, 11), V.oscurecer(c, 0.12) if dx in (-22, 54) else c, temblor=0.0, capa=capa)
        lz.relleno(V.elipse_pts(0, -78, 70, 34), c, temblor=0.0, capa=capa)
        lz.relleno(V.elipse_pts(-14, -84, 20, 14), (150, 96, 70), temblor=0.0, capa=capa)
        lz.relleno(V.capsula([50, -92], [96, -104], 30, 22), c, temblor=0.0, capa=capa)
        lz.relleno(V.capsula([90, -108], [108, -120], 6, 3), (90, 70, 60), temblor=0.0, capa=capa)
        lz.puntos([(92, -100)], 3, V.TINTA, capa=capa)


def escudo(lz, x, y, s=1.0, k=1.0, capa=1, seed=0):
    """Escudo de armas estilizado (cerro plateado sobre campo rojo y azul). Simplificado, no heráldico exacto."""
    if k <= 0.01:
        return
    with lz.grupo(x, y, s * e_back(clamp01(k), 1.6)):
        E = np.array([[-110, -140], [110, -140], [110, 20], [0, 150], [-110, 20]])
        lz.relleno(E * 1.1, (212, 166, 62), temblor=0.0, capa=capa)
        lz.relleno(E, (176, 44, 52), temblor=0.0, capa=capa)
        lz.relleno(np.array([[-110, 20], [110, 20], [0, 150]]), (60, 100, 150), temblor=0.0, capa=capa)
        lz.relleno(np.array([[-84, 10], [-30, -64], [-4, -40], [30, -84], [84, 10]]), V.PLATA, temblor=0.0, capa=capa)
        lz.relleno(np.array([[30, -84], [84, 10], [50, 10]]), V.PLATA_OSC, temblor=0.0, capa=capa)
        lz.relleno(V.elipse_pts(0, -110, 16, 16), (252, 214, 96), temblor=0.0, capa=capa)
