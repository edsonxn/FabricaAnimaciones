# -*- coding: utf-8 -*-
"""Mundos de la escena 13 (la guerrilla): la sierra del sur (cerros empinados, palmas, rocas, vereda de arrieros) y la selva de Veracruz (vegetación densa, helechos, un fuego pequeño)."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import W, H, h01, circulo, elipse, rect_red

VEREDA = [(-120, 330), (20, 290), (120, 240), (190, 160), (270, 120), (360, 140), (450, 100), (560, 40)]


def pos_vereda(s):
    p = np.asarray(VEREDA, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    s = float(np.clip(s, 0, d[-1] - 1e-3))
    i = int(np.clip(np.searchsorted(d, s, side="right") - 1, 0, len(p) - 2))
    f = (s - d[i]) / (d[i + 1] - d[i])
    q = p[i] + (p[i + 1] - p[i]) * f
    dr = (p[i + 1] - p[i]) / np.hypot(*(p[i + 1] - p[i]))
    return float(q[0]), float(q[1]), dr


class SierraSur:
    """Sierra del sur: vereda de arrieros que serpentea entre rocas grandes y palmas, barrancas oscuras, cerros de fondo."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -200, -140, 660, 440, color_top=(96, 150, 96), c_roca=(100, 90, 120), t=t, seed=181, esp=50)
        DC.parches(lz, iso, -200, -140, 660, 440, (96, 150, 96), n=30, var=26, seed=182, alfa=0.6, tam=(50, 110))
        for (x, y, r) in ((60, 40, 80), (360, 300, 90), (480, 200, 70)):
            I.suelo_curvo(lz, iso, [(x - r, y), (x, y - r * 0.5), (x + r, y), (x, y + r * 0.5)], (80, 128, 86), alfa=0.8)
        I.camino(lz, iso, VEREDA, 28, (206, 180, 132), borde=(176, 150, 108))
        DC.acequia(lz, iso, [(-200, 400), (100, 370), (300, 400), (660, 360)], t, ancho=14.0)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            for i, (x, y) in enumerate(((150, 300), (230, 80), (330, 200), (420, 40), (60, 200), (500, 160), (300, 60))):
                m.add(x - 14, y - 14, x + 14, y + 14, 50, (lambda x, y, i: (lambda lz, iso: O.roca(lz, iso, x, y, s=2.4 + 0.7 * (i % 3), seed=i + 3, color=(150, 140, 150))))(x, y, i), clave=x + y)
            DC.bosque(m, -200, -140, 660, 440, n=90, seed=183, evitar=((-200, 220, 600, 360),), t_fn=lambda: self._t, tipos=("palma", "arbol", "pino", "roca"), h=(50, 92), min_d=26)
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m


class Selva:
    """Selva de Veracruz: árboles altos y densos, palmas, helechos y arbustos con flores, claro con una hoguera y una choza de ramas, arroyo."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -160, -160, 520, 420, color_top=(74, 138, 84), c_roca=(90, 84, 110), t=t, seed=191, esp=44)
        DC.parches(lz, iso, -160, -160, 520, 420, (74, 138, 84), n=34, var=28, seed=192, alfa=0.65, tam=(40, 100))
        I.suelo_curvo(lz, iso, [(110, 120), (250, 110), (270, 220), (140, 240)], (150, 120, 84), n=6)
        DC.acequia(lz, iso, [(-160, 300), (60, 280), (300, 320), (520, 290)], t, ancho=14.0)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.choza(m, 170, 130, r=16, h=18, seed=4)
            DC.bosque(m, -160, -160, 520, 420, n=130, seed=193, evitar=((100, 100, 290, 260), (-160, 270, 520, 340)), t_fn=lambda: self._t, tipos=("arbol", "palma", "arbol", "arbusto", "arbusto", "palma"), h=(60, 110), min_d=22)
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m
