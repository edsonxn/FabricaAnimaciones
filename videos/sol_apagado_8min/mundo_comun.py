# -*- coding: utf-8 -*-
"""Base común del plano secuencia de 8 minutos: anclas (tiempo global), tiempo real tau desde la desaparición del
Sol, sistema solar esquemático, cámara (punto del mundo -> punto de pantalla, zoom en escala log) y la
transformación de superficie `Sup` (paisaje plano o doblado sobre el planeta)."""
import math
import types
from contextlib import contextmanager

import numpy as np

from escena_base import TL, Escena
from motor import W, H, mat_t, mat_s, prog, clamp01, lerp, e_in, e_out, e_inout, remuestrear

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


# ======================================================================== sistema solar esquemático
SOL = np.array([0.0, 0.0])
SOL_R = 300.0
# nombre: (UA real, radio de órbita esquemático, radio del planeta, ángulo inicial)
PLANETAS = {
    "mercurio": (0.387, 540.0, 34.0, 2.2),
    "venus": (0.723, 820.0, 72.0, -0.1),
    "tierra": (1.0, 1250.0, 100.0, 0.88),
    "marte": (1.524, 1750.0, 56.0, 1.2),
    "jupiter": (5.203, 2900.0, 210.0, 0.45),
    "saturno": (9.58, 4000.0, 170.0, 2.7),
    "urano": (19.19, 5000.0, 120.0, -2.0),
    "neptuno": (30.07, 5900.0, 115.0, 0.9),
}
LUZ_UA = 499.0          # s que tarda la luz en recorrer 1 UA


def omega(radio):
    return 0.03 * (1250.0 / radio) ** 1.5


# radio de la burbuja de luz (mundo) en función del tiempo real tau
_TAU_R = [(0.0, SOL_R)] + sorted((ua * LUZ_UA, rr) for ua, rr, _, _ in PLANETAS.values())


def radio_de_tau(tau):
    xs = [a for a, _ in _TAU_R]
    ys = [b for _, b in _TAU_R]
    if tau <= xs[-1]:
        return float(np.interp(tau, xs, ys))
    pend = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
    return ys[-1] + pend * (tau - xs[-1])


def formato_tau(tau):
    s = int(tau)
    if s < 3600:
        return f"{s // 60}:{s % 60:02d}"
    return f"{s // 3600} h {(s % 3600) // 60:02d} min"


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

    def matriz(self):
        c, s = math.cos(self.rot), math.sin(self.rot)
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])
        return mat_t(*self.pant) @ R @ mat_s(self.z) @ mat_t(-self.ancla[0], -self.ancla[1])

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
    return Cam(c1.ancla + (c2.ancla - c1.ancla) * u, c1.pant + (c2.pant - c1.pant) * u, z,
               lerp(c1.rot, c2.rot, u))


def camino(t, tramos):
    """tramos: [(t_ini, t_fin, fn(t) -> Cam)], en orden. Dentro de un tramo manda su fn; entre el final de uno y
    el inicio del siguiente se mezclan con suavidad (e_inout)."""
    if t <= tramos[0][1]:
        return tramos[0][2](t)
    for (a0, a1, f1), (b0, b1, f2) in zip(tramos[:-1], tramos[1:]):
        if t <= b0:
            u = e_inout(prog(t, a1, b0))
            return mezclar_cam(f1(t), f2(t), u)
        if t <= b1:
            return f2(t)
    return tramos[-1][2](t)


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
    from motor import e_back
    return 0.0 if t < t0 else e_back(prog(t, t0, t0 + dur))


def ventana(t, a, b, fi=0.35, fo=0.35):
    """Opacidad de algo visible entre a y b con entradas/salidas suaves."""
    return e_out(prog(t, a - fi, a)) * (1 - e_in(prog(t, b, b + fo)))
