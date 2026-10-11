# -*- coding: utf-8 -*-
"""Mundos de la escena 9 (la captura): el desierto del norte con rocas donde espera la emboscada y el patio de piedra donde ejecutan a los jefes (sin mostrar el momento)."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import W, H, h01, circulo, elipse, rect_red

CAMINO_D = [(-180, 310), (-20, 280), (110, 236), (240, 206), (370, 176), (560, 126)]
ROCAS_D = [(280, 150), (310, 140), (340, 130), (262, 262), (300, 276), (236, 140), (400, 230), (430, 214)]


def pos_camino_d(s):
    p = np.asarray(CAMINO_D, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    s = float(np.clip(s, 0, d[-1] - 1e-3))
    i = int(np.clip(np.searchsorted(d, s, side="right") - 1, 0, len(p) - 2))
    f = (s - d[i]) / (d[i + 1] - d[i])
    q = p[i] + (p[i + 1] - p[i]) * f
    dr = (p[i + 1] - p[i]) / np.hypot(*(p[i + 1] - p[i]))
    return float(q[0]), float(q[1]), dr


class Desierto:
    """Desierto del norte de Coahuila: dunas pálidas, nopales, órganos, magueyes, rocas grandes junto al camino, cerros lejanos y un camino de tierra."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -240, -160, 640, 440, color_top=(230, 202, 148), c_tierra=(176, 130, 92), t=t, seed=151, esp=40)
        DC.parches(lz, iso, -240, -160, 640, 440, (230, 202, 148), n=40, var=26, seed=152, alfa=0.6, tam=(50, 120))
        for (x, y, r) in ((-120, 60, 90), (120, -60, 120), (460, 330, 100), (-60, 360, 110)):
            I.suelo_curvo(lz, iso, [(x - r, y), (x, y - r * 0.5), (x + r, y), (x, y + r * 0.5)], (240, 216, 166), alfa=0.8)
        I.camino(lz, iso, CAMINO_D, 36, (214, 186, 136), borde=(190, 160, 114))

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            for i, (x, y) in enumerate(ROCAS_D):
                m.add(x - 12, y - 12, x + 12, y + 12, 40, (lambda x, y, i: (lambda lz, iso: O.roca(lz, iso, x, y, s=2.0 + 0.7 * (i % 3), seed=i + 7, color=(176, 140, 120))))(x, y, i), clave=x + y)
            DC.bosque(m, -240, -160, 640, 440, n=70, seed=153, evitar=((-240, 200, 640, 330), (200, 100, 460, 300)), t_fn=lambda: self._t, tipos=("nopal", "organo", "maguey", "roca", "nopal"), min_d=26)
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m


def patio_ejecucion(lz, iso, t):
    """Patio de piedra con un muro alto al fondo y arcos; suelo de lajas (escena sobria)."""
    I.isla(lz, iso, -60, -40, 360, 300, color_top=(196, 186, 170), c_tierra=(130, 120, 110), t=t, seed=161, esp=30)
    I.suelo_rect(lz, iso, -40, 0, 380, 280, (212, 202, 184))
    I.cuadricula(lz, iso, -40, 0, 340, 280, 24, color=(120, 110, 100), alfa=0.25)


def objetos_patio(t):
    m = I.Mundo()
    m.add(-50, -30, 350, -10, 100, lambda lz, iso: _muro_patio(lz, iso), clave=-20)
    for (x, y) in ((-30, 90), (330, 90), (-30, 220), (330, 220)):
        m.add(x - 4, y - 4, x + 4, y + 4, 60, (lambda x, y: (lambda lz, iso: O.cipres(lz, iso, x, y, h=52, seed=int(x + y))))(x, y), clave=x + y)
    return m


def _muro_patio(lz, iso):
    c = I.caja(lz, iso, -50, -30, 400, 20, 90, (200, 184, 160))
    I.caja(lz, iso, -52, -32, 404, 24, 5, (224, 210, 188), z0=90)
    for i in range(6):
        I.cara_arco(lz, iso, c, "y", 20 + i * 64, 54 + i * 64, 0, 56, (96, 86, 90))
    I.cara_rect(lz, iso, c, "y", 0, 400, 0, 8, (170, 154, 132))
