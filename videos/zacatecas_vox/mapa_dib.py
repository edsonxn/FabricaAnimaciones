# -*- coding: utf-8 -*-
"""Dibujo del mapa de papel recortado (Vox): mar, tierra, sierras, nopales, Gran Chichimeca, ciudades y ruta."""
import math

import numpy as np

import geo as G
import vox as V
from motor import prog, e_out, e_back, e_inout, h01, clamp01, rect_red

TIERRA_MX = (226, 200, 148)
TIERRA_EU = (214, 196, 150)
TIERRA_FR = (206, 190, 146)
MAR_C = (170, 198, 202)

_POLI = {n: G.poli(v) for n, v in dict(MEXICO=G.MEXICO, BAJA=G.BAJA, EEUU=G.EEUU, CENTRO=G.CENTROAMERICA, CUBA=G.CUBA,
                                     IBERIA=G.IBERIA, FRANCIA=G.FRANCIA, AFRICA=G.AFRICA_N,
                                     CHICH=G.CHICHIMECA).items()}


def _puntos_linea(linea, n, seed, dispersion=14.0):
    P = G.poli(linea)
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0], np.cumsum(seg)])
    out = []
    for i in range(n):
        L = d[-1] * (i + 0.5) / n
        x, y = np.interp(L, d, P[:, 0]), np.interp(L, d, P[:, 1])
        out.append((x + (h01(seed, i, 1) - .5) * dispersion * 2, y + (h01(seed, i, 2) - .5) * dispersion * 2, i))
    return out


SIERRAS = (_puntos_linea(G.SIERRA_OCC, 15, 3) + _puntos_linea(G.SIERRA_OR, 12, 4, 10) + _puntos_linea(G.EJE_VOLC, 9, 5, 8))

# nopales: dispersos dentro de la Gran Chichimeca (semilla fija)
def _nopales(n=26):
    P = _POLI["CHICH"]
    x0, y0 = P.min(0)
    x1, y1 = P.max(0)
    out = []
    i = 0
    while len(out) < n and i < 600:
        x, y = x0 + (x1 - x0) * h01(9, i, 1), y0 + (y1 - y0) * h01(9, i, 2)
        # dentro del polígono (ray casting)
        dentro = False
        j = len(P) - 1
        for k in range(len(P)):
            if (P[k][1] > y) != (P[j][1] > y) and x < (P[j][0] - P[k][0]) * (y - P[k][1]) / (P[j][1] - P[k][1] + 1e-9) + P[k][0]:
                dentro = not dentro
            j = k
        if dentro:
            out.append((x, y, len(out)))
        i += 1
    return out


NOPALES = _nopales()


def olas_mar(lz, alfa, z):
    """Marcas de oleaje (trazos cortos claros) repartidas por el océano; se dibujan solo si son visibles."""
    if z > 0.5:
        return
    for i in range(140):
        x = -800 + 7400 * h01(31, i, 1)
        y = -2000 + 3600 * h01(31, i, 2)
        with lz.capa(0):
            lz.trazo(np.array([[x - 46, y], [x - 16, y - 12], [x + 12, y], [x + 40, y - 10]]), (196, 224, 226), 8, afinar=False,
                     temblor=0.0, capa=0, paso=14.0) if alfa > 0.5 else None


def mar(lz, alfa=1.0, color=MAR_C, z=1.0):
    with lz.capa(0):
        lz.relleno(np.array([[-40000, -40000], [60000, -40000], [60000, 40000], [-40000, 40000]]), color, alfa=alfa, temblor=0.0)
    olas_mar(lz, alfa, z)


def tierra(lz, alfa=1.0, detalle=1.0):
    """Recortes de tierra (capa 1: borde crema + sombra)."""
    if alfa <= 0.01:
        return
    orden = [("AFRICA", TIERRA_FR, 1), ("FRANCIA", TIERRA_FR, 2), ("IBERIA", TIERRA_EU, 3), ("EEUU", TIERRA_EU, 4),
             ("CENTRO", TIERRA_EU, 5), ("CUBA", TIERRA_EU, 6), ("BAJA", TIERRA_MX, 7), ("MEXICO", TIERRA_MX, 8)]
    for n, col, sd in orden:
        lz.relleno(V.corte(_POLI[n], sd, 3.0, 1), col, seed=sd, temblor=0.0, capa=1, alfa=alfa)


def sierras(lz, alfa=1.0, esc=1.0, t=0.0, aparece=None):
    """Cerritos de papel a lo largo de las sierras. aparece(i) -> escala 0..1 (para animarlos)."""
    for (x, y, i) in SIERRAS:
        k = 1.0 if aparece is None else aparece(i)
        if k <= 0.01:
            continue
        s = 26 * esc * k * (0.8 + 0.5 * h01(2, i))
        col = V.mezcla((176, 124, 84), (150, 96, 70), h01(3, i))
        with lz.grupo(x, y, 1.0):
            lz.relleno(V.corte([[-s, 0], [-s * 0.15, -s * 1.5], [s * 0.3, -s * 1.15], [s, 0]], i, 1.5, 1), col, seed=i,
                       temblor=0.0, capa=1, alfa=alfa)
            lz.relleno(np.array([[s * 0.3, -s * 1.15], [s, 0], [s * 0.1, 0], [-s * 0.15, -s * 1.5]]) * [1, 1],
                       V.oscurecer(col, 0.18), seed=i, temblor=0.0, capa=1, alfa=alfa)


def nopal(lz, x, y, s, capa=1, alfa=1.0, seed=0):
    verde, vosc = (104, 148, 84), (70, 112, 68)
    with lz.grupo(x, y, s):
        lz.relleno(V.elipse_pts(0, -34, 13, 34), verde, seed=seed, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(V.elipse_pts(-22, -60, 10, 20, -0.5), vosc, seed=seed + 1, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(V.elipse_pts(20, -66, 10, 20, 0.5), verde, seed=seed + 2, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(V.elipse_pts(0, -76, 9, 16), vosc, seed=seed + 3, temblor=0.0, capa=capa, alfa=alfa)
        # tunas (frutos rojos)
        for dx, dy in ((-22, -78), (20, -84), (0, -92)):
            lz.puntos([(dx, dy)], 3.6, (206, 66, 82), capa=capa)


def nopales(lz, alfa=1.0, esc=1.0, aparece=None):
    for (x, y, i) in NOPALES:
        k = 1.0 if aparece is None else aparece(i)
        if k > 0.01:
            nopal(lz, x, y + 6, 0.62 * esc * k, 1, alfa, i)


def chichimeca(lz, alfa=1.0, pulso=0.0, frac=1.0):
    """Zona de la Gran Chichimeca: recorte naranja con trama de puntos."""
    if alfa <= 0.01:
        return
    P = V.corte(_POLI["CHICH"], 21, 5.0, 3)
    c = (236, 156, 92)
    lz.relleno(P, c, seed=21, temblor=0.0, capa=1, alfa=alfa * clamp01(frac))
    if frac > 0.98 and alfa > 0.5:
        V.semitono(lz, P, (206, 110, 60), esp=22.0, r=3.4, ang=0.6, capa=1)


def estrella(lz, x, y, r, alfa=1.0, capa=2, color=V.ROJO):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    lz.relleno(np.array(pts), color, temblor=0.0, capa=capa, alfa=alfa)


def marcador_ciudad(lz, x, y, escala=1.0, color=V.ROJO, alfa=1.0, capa=2):
    lz.puntos([(x, y)], 9 * escala, V.CREMA, capa=capa)
    lz.puntos([(x, y)], 6 * escala, color, capa=capa)


def edificio_mexico(lz, x, y, s=1.0, alfa=1.0):
    """Pirámide escalonada sencilla (México-Tenochtitlan / Ciudad de México)."""
    with lz.grupo(x, y, s):
        for i, (w, h) in enumerate([(70, 14), (54, 14), (38, 14), (22, 14)]):
            lz.relleno(np.array([[-w, -i * 14], [w, -i * 14], [w - 6, -i * 14 - h], [-w + 6, -i * 14 - h]]),
                       V.mezcla((214, 180, 130), (180, 140, 100), i / 3), temblor=0.0, capa=1, alfa=alfa)


def ruta(lz, frac, color=V.ROJO, ancho=7.0, fase=0.0, ruta_ll=None, alfa=1.0):
    """Ruta discontinua que se dibuja poco a poco."""
    P = G.poli(ruta_ll or G.RUTA_PLATA)
    if frac <= 0.001:
        return
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0], np.cumsum(seg)])
    L = d[-1] * clamp01(frac)
    k = int(np.searchsorted(d, L))
    sub = list(P[:k])
    if 0 < k < len(P):
        u = (L - d[k - 1]) / max(1e-9, d[k] - d[k - 1])
        sub.append(P[k - 1] + (P[k] - P[k - 1]) * u)
    sub = np.array(sub)
    if len(sub) < 2:
        return
    # discontinua: trozos alternos a lo largo de la polilínea
    ds = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(sub, axis=0).T))])
    per, largo = ancho * 4.6, ancho * 2.6
    s0 = -(fase % per)
    ini = np.arange(s0, ds[-1], per)
    for a in ini:
        b = min(a + largo, ds[-1])
        a = max(a, 0.0)
        if b - a < 0.5:
            continue
        xs = np.interp([a, (a + b) / 2, b], ds, sub[:, 0])
        ys = np.interp([a, (a + b) / 2, b], ds, sub[:, 1])
        lz.trazo(np.stack([xs, ys], 1), color, ancho, afinar=False, temblor=0.0, capa=2, paso=6.0)
