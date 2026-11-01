# -*- coding: utf-8 -*-
"""Base común del plano secuencia «oxígeno 5 s»: anclas (tiempo global de las palabras), interpolación por claves,
cámara de la superficie `Sup` (paisaje plano o doblado sobre el planeta, con paralaje) y utilidades de tiempo.
Copiado de `videos/dos_lunas/mundo_comun.py` y ampliado: Sup se dobla alrededor de X0 y tiene `par(f)` (capas lejanas)."""
import math
import types
from contextlib import contextmanager

import numpy as np

from escena_base import TL, Escena
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, remuestrear

# ======================================================================== anclas
_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]


def T(eid, texto, **kw):
    """Tiempo global en que se dice `texto` en la escena `eid` (KeyError si no existe)."""
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def ESC0(eid):
    return _ESC[eid]["t0"]


def ESC1(eid):
    return _ESC[eid]["t1"]


# ======================================================================== claves e interpolación
def kf(t, claves, ease=e_inout):
    """Interpolación por claves [(t, v)] (v escalar o secuencia); entre dos claves suaviza con `ease`."""
    if t <= claves[0][0]:
        v = claves[0][1]
        return v if np.isscalar(v) else np.asarray(v, float)
    for (a, va), (b, vb) in zip(claves[:-1], claves[1:]):
        if t <= b:
            u = ease(prog(t, a, b))
            if np.isscalar(va):
                return va + (vb - va) * u
            return np.asarray(va, float) + (np.asarray(vb, float) - np.asarray(va, float)) * u
    v = claves[-1][1]
    return v if np.isscalar(v) else np.asarray(v, float)


def cam_kf(t, claves, ease=e_inout):
    """claves [(t, Xc, Hc, k)] -> (Xc, Hc, k) con el zoom interpolado en escala log."""
    if t <= claves[0][0]:
        return claves[0][1:]
    for a, b in zip(claves[:-1], claves[1:]):
        if t <= b[0]:
            u = ease(prog(t, a[0], b[0]))
            return (lerp(a[1], b[1], u), lerp(a[2], b[2], u), math.exp(lerp(math.log(a[3]), math.log(b[3]), u)))
    return claves[-1][1:]


# ======================================================================== superficie
class Sup:
    """Plano de la superficie (X derecha, H arriba) -> pantalla. El punto (X0, 0) cae en (hx, hy); escala k (px por unidad)
    y curvatura kappa (1/radio del planeta en px). Con kappa > 0 el paisaje se dobla sobre el planeta alrededor de X0."""

    def __init__(self, hx, hy, k=1.0, kappa=0.0, X0=0.0):
        self.hx, self.hy, self.k, self.kappa, self.X0 = hx, hy, k, kappa, X0

    @staticmethod
    def centrada(Xc, Hc, k):
        """Cámara de la superficie: el punto (Xc, Hc) en el centro de la pantalla."""
        return Sup(W / 2, H / 2 + k * Hc, k, 0.0, Xc)

    def par(self, f):
        """Capa lejana con paralaje f (< 1 se mueve y se ve más pequeña)."""
        return Sup(self.hx, self.hy, self.k * f, self.kappa, self.X0)

    def p(self, X, Hh):
        a = self.k * (np.asarray(X, float) - self.X0)
        h = self.k * np.asarray(Hh, float)
        kap = self.kappa
        if kap < 1e-9:
            return self.hx + a, self.hy - h
        phi = kap * a
        return (self.hx + np.sin(phi) / kap + h * np.sin(phi),
                self.hy + (1 - np.cos(phi)) / kap - h * np.cos(phi))

    def pt(self, X, Hh):
        x, y = self.p(X, Hh)
        return float(x), float(y)

    def ang(self, X):
        return self.kappa * self.k * (X - self.X0)

    def poly(self, pts):
        Q = np.asarray(pts, float)
        if self.kappa > 1e-9:
            Q = remuestrear(Q, 40.0, True)
        x, y = self.p(Q[:, 0], Q[:, 1])
        return np.stack([x, y], 1)

    @contextmanager
    def en(self, lz, X, Hh, s=1.0, rot=0.0):
        x, y = self.p(X, Hh)
        with lz.grupo(float(x), float(y), s * self.k, self.ang(X) + rot):
            yield

    def vis(self, X0, X1, H0=-1e9, H1=1e9, margen=80):
        """¿Puede verse algo del rectángulo [X0, X1] x [H0, H1]?"""
        if self.kappa > 2e-4:
            return True
        x0 = self.hx + self.k * (X0 - self.X0)
        x1 = self.hx + self.k * (X1 - self.X0)
        if x1 < -margen or x0 > W + margen:
            return False
        y_arr = self.hy - self.k * H1
        y_ab = self.hy - self.k * H0
        return y_ab > -margen and y_arr < H + margen

    def rango_x(self, margen=200):
        """Rango de X visible (aprox.)."""
        if self.kappa > 2e-4:
            return -1e9, 1e9
        return self.X0 + (-margen - self.hx) / self.k, self.X0 + (W + margen - self.hx) / self.k


def smooth_arr(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def campana(t, a, b):
    if t <= a or t >= b:
        return 0.0
    return math.sin(math.pi * (t - a) / (b - a))


def pop(t, t0, dur=0.35):
    """0 -> 1 con rebote a partir de t0."""
    return 0.0 if t < t0 else e_back(prog(t, t0, t0 + dur))


def ventana(t, a, b, fi=0.35, fo=0.35):
    """Opacidad de algo visible entre a y b con entradas/salidas suaves."""
    return e_out(prog(t, a - fi, a)) * (1 - e_in(prog(t, b, b + fo)))


def vpop(t, a, b, dur=0.35, fo=0.3):
    """Escala de algo que entra con rebote en a y se desvanece (no encoge) tras b: (escala, alfa)."""
    return pop(t, a, dur), 1 - e_in(prog(t, b, b + fo))
