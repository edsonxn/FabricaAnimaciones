# -*- coding: utf-8 -*-
"""Base común del plano secuencia «dos lunas»: anclas (tiempo global de las palabras), interpolación por claves,
cámara (punto del mundo -> punto de pantalla, zoom en escala log) y la transformación de superficie `Sup` (paisaje plano
o doblado sobre el planeta). Copiado de `videos/sol_apagado_8min/mundo_comun.py` sin lo del Sol."""
import math
import types
from contextlib import contextmanager

import numpy as np

from escena_base import TL, Escena
from motor import W, H, mat_t, mat_s, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, remuestrear

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
        return np.asarray(claves[0][1], float) if not np.isscalar(claves[0][1]) else claves[0][1]
    for (a, va), (b, vb) in zip(claves[:-1], claves[1:]):
        if t <= b:
            u = ease(prog(t, a, b))
            if np.isscalar(va):
                return va + (vb - va) * u
            return np.asarray(va, float) + (np.asarray(vb, float) - np.asarray(va, float)) * u
    v = claves[-1][1]
    return np.asarray(v, float) if not np.isscalar(v) else v


def interp_log(t, claves):
    """claves: [(t, valor>0)]; interpola linealmente en escala log (para zooms)."""
    ts = [a for a, _ in claves]
    vs = [math.log(b) for _, b in claves]
    return math.exp(float(np.interp(t, ts, vs)))


# ======================================================================== cámara
class Cam:
    """El punto del mundo `ancla` cae en `pant` (pantalla) con zoom `z`."""

    def __init__(self, ancla, pant, z, rot=0.0):
        self.ancla = np.asarray(ancla, float)
        self.pant = np.asarray(pant, float)
        self.z = float(z)
        self.rot = rot

    def a_pant(self, p):
        return self.pant + self.z * (np.asarray(p, float) - self.ancla)

    def visible(self, p, r, margen=60):
        q = self.a_pant(p)
        rr = r * self.z
        return -margen - rr < q[0] < W + margen + rr and -margen - rr < q[1] < H + margen + rr


def mezclar_cam(c1, c2, u):
    """Mezcla dos cámaras: el zoom en escala log; ancla/pantalla de forma que no haya saltos."""
    if u <= 0:
        return c1
    if u >= 1:
        return c2
    z = math.exp(lerp(math.log(c1.z), math.log(c2.z), u))
    return Cam(c1.ancla + (c2.ancla - c1.ancla) * u, c1.pant + (c2.pant - c1.pant) * u, z, lerp(c1.rot, c2.rot, u))


def cam_claves(t, claves, ease=e_inout):
    """claves: [(t, (ax, ay), (px, py), z)]: entre dos claves el punto del mundo `a` cae en `p` con zoom log, suavizado."""
    if t <= claves[0][0]:
        k = claves[0]
        return Cam(k[1], k[2], k[3])
    for k0, k1 in zip(claves[:-1], claves[1:]):
        if t <= k1[0]:
            u = ease(prog(t, k0[0], k1[0]))
            return mezclar_cam(Cam(k0[1], k0[2], k0[3]), Cam(k1[1], k1[2], k1[3]), u)
    k = claves[-1]
    return Cam(k[1], k[2], k[3])


# ======================================================================== superficie
class Sup:
    """Plano de la superficie (X, H: H hacia arriba) -> pantalla, con escala k y curvatura kappa
    (1/radio del planeta en px de pantalla). Con kappa > 0 el paisaje se dobla sobre el planeta cuyo punto
    más alto está en (hx, hy)."""

    def __init__(self, hx, hy, k=1.0, kappa=0.0):
        self.hx, self.hy, self.k, self.kappa = hx, hy, k, kappa

    def p(self, X, Hh):
        a = self.k * np.asarray(X, float)
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
        return self.kappa * self.k * X

    def poly(self, pts):
        Q = np.asarray(pts, float)
        if self.kappa > 1e-9:
            Q = remuestrear(Q, 40.0, True)
        x, y = self.p(Q[:, 0], Q[:, 1])
        return np.stack([x, y], 1)

    @contextmanager
    def en(self, lz, X, Hh, s=1.0):
        x, y = self.p(X, Hh)
        with lz.grupo(float(x), float(y), s * self.k, self.ang(X)):
            yield

    def visible_y(self, H0, H1):
        """¿Se ve alguna parte de la franja de alturas [H1, H0] (planas)?"""
        y0 = self.hy - self.k * H0
        y1 = self.hy - self.k * H1
        return y1 > -50 and y0 < H + 50


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
