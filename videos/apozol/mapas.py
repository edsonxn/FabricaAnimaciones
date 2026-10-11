# -*- coding: utf-8 -*-
"""Rutas gruesas y legibles sobre el mapa con relieve (el `MD.ruta` del kit es fino y se confunde con los ríos del mapa)."""
import math

import numpy as np

import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import catmull

MP = KM.MAPA


def _pts(cam, pts):
    ll = [MD.CIUDADES[p] if isinstance(p, str) else p for p in pts]
    x, y = MP.proy(cam, np.array([p[0] for p in ll]), np.array([p[1] for p in ll]))
    q = np.stack([x, y], 1)
    if len(q) > 2:
        q = np.array(catmull(q, 12), float)
    elif len(q) == 2:
        q = np.linspace(q[0], q[1], 40)
    return q


def tramo(q, frac):
    seg = np.hypot(*np.diff(q, axis=0).T)
    d = np.r_[0, np.cumsum(seg)]
    s = d[-1] * float(np.clip(frac, 0, 1))
    i = int(np.clip(np.searchsorted(d, s, side="right") - 1, 0, len(q) - 2))
    f = (s - d[i]) / max(d[i + 1] - d[i], 1e-6)
    cab = q[i] + (q[i + 1] - q[i]) * f
    return np.vstack([q[:i + 1], cab]), cab, (q[i + 1] - q[i]) / max(np.hypot(*(q[i + 1] - q[i])), 1e-6)


def ruta_gruesa(lz, cam, pts, frac=1.0, t=0.0, color=(255, 90, 90), ancho=12.0, borde=(255, 255, 255), dash=False, flecha=True, alfa=1.0, capa=2):
    """Ruta con halo claro, cuerpo de color y flecha. dash=True añade guiones blancos que avanzan. Devuelve el punto de la cabeza (px) o None."""
    if frac <= 0.003:
        return None
    q = _pts(cam, pts)
    z = max(0.8, cam[2] ** 0.3)
    qq, cab, v = tramo(q, frac)
    if len(qq) < 2:
        return None
    lz.trazo(qq, (*borde, int(210 * alfa)), ancho * 1.7 * z, afinar=False, temblor=0.0, capa=capa)
    lz.trazo(qq, (*color, int(255 * alfa)), ancho * z, afinar=False, temblor=0.0, capa=capa)
    if dash:
        P.discontinua(lz, qq, (255, 255, 255), ancho=ancho * 0.35 * z, largo=26 * z, hueco=22 * z, fase=-t * 60 * z, capa=capa)
    if flecha:
        nn = np.array([-v[1], v[0]])
        L = 26 * z
        lz.relleno(np.array([cab + v * L, cab - v * L * 0.4 + nn * L * 0.7, cab - v * L * 0.4 - nn * L * 0.7]), color, alfa=alfa, capa=capa)
    return float(cab[0]), float(cab[1])


def proy(cam, lugar):
    ll = MD.CIUDADES[lugar] if isinstance(lugar, str) else lugar
    p = MP.proy(cam, *ll)
    return float(p[0]), float(p[1])


def flecha_pantalla(lz, x0, y0, x1, y1, color=(255, 255, 255), ancho=14.0, alfa=1.0, capa=2):
    """Flecha recta gruesa en coordenadas de pantalla."""
    v = np.array([x1 - x0, y1 - y0], float)
    L = np.hypot(*v) + 1e-6
    u = v / L
    n = np.array([-u[1], u[0]])
    cab = ancho * 2.4
    base = np.array([x1, y1]) - u * cab
    lz.relleno(np.array([[x0, y0] + n * ancho / 2, base + n * ancho / 2, base + n * cab * 0.7, [x1, y1], base - n * cab * 0.7, base - n * ancho / 2, np.array([x0, y0]) - n * ancho / 2]), color, alfa=alfa, capa=capa)
