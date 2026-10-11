# -*- coding: utf-8 -*-
"""Contexto común del plano secuencia: anclas de tiempo, cámara por fotogramas clave, año (odómetro), hora del día."""
import math
import types

import numpy as np

from escena_base import TL, Escena
from motor import clamp01, lerp, e_inout, e_out, smooth, prog

LOC = 1.0 / 40.0        # 1 unidad local = LOC unidades de mundo (el mundo está en unidades del mapa)
_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]


def T(eid, texto, **kw):
    """Tiempo global (s) en que se dice `texto` dentro de la escena `eid`."""
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


# ------------------------------------------------------------------ cámara
def KL(t, lx, ly, zl, rot=0.0):
    """Fotograma clave en coordenadas LOCALES (zl = zoom local: 1 = pantalla de 1080 unidades locales de ancho)."""
    return (t, lx * LOC, ly * LOC, zl / LOC, rot)


def KM(t, wx, wy, z, rot=0.0):
    """Fotograma clave en coordenadas de MAPA (mundo)."""
    return (t, wx, wy, z, rot)


class Camara:
    """Interpola fotogramas clave con zoom exponencial y paneo corregido (el punto de interés se mueve lineal en
    pantalla). Entre dos claves iguales mantiene la vista (con un leve 'respirar' opcional)."""

    def __init__(self, claves, respira=0.0):
        self.k = sorted(claves, key=lambda c: c[0])
        self.respira = respira

    def __call__(self, t):
        k = self.k
        if t <= k[0][0]:
            cx, cy, z, r = k[0][1:]
        elif t >= k[-1][0]:
            cx, cy, z, r = k[-1][1:]
        else:
            i = 0
            while k[i + 1][0] < t:
                i += 1
            t0, x0, y0, z0, r0 = k[i]
            t1, x1, y1, z1, r1 = k[i + 1]
            u = e_inout(prog(t, t0, t1))
            z = z0 * (z1 / z0) ** u
            if abs(z1 - z0) < 1e-9 * z0:
                s = u
            else:
                s = (1 / z - 1 / z0) / (1 / z1 - 1 / z0)
            cx, cy, r = lerp(x0, x1, s), lerp(y0, y1, s), lerp(r0, r1, u)
        if self.respira:
            a = self.respira / z
            cx += a * math.sin(t * 0.7) * 6
            cy += a * math.sin(t * 0.53 + 1) * 6
        return cx, cy, z, r


# ------------------------------------------------------------------ año (odómetro): valor real que rueda
class Anios:
    def __init__(self, hitos):
        """hitos: [(t, año[, dur])]: el valor rueda hacia `año` durante `dur` s (0.7 por defecto) que terminan en t."""
        self.h = sorted(hitos, key=lambda x: x[0])

    def __call__(self, t):
        v = self.h[0][1]
        for i in range(1, len(self.h)):
            h = self.h[i]
            ti, vi = h[0], h[1]
            dur = h[2] if len(h) > 2 else 0.7
            prev = self.h[i - 1][1]
            if t >= ti:
                v = vi
            elif t > ti - dur:
                v = prev + (vi - prev) * e_inout((t - (ti - dur)) / dur)
                break
            else:
                break
        return v


def lerp_color(a, b, u):
    return tuple(int(x + (y - x) * u) for x, y in zip(a, b))
