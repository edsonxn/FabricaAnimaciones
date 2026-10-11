# -*- coding: utf-8 -*-
"""Base común de las escenas cartoon90 de «Mostacho»: lienzo compartido, clase Base y transiciones de luz."""
import math

import numpy as np

from escena_base import Escena
from motor import FPS, H, W, clamp01, e_in, e_inout, e_out, lerp, prog, smooth
import toon as TN
from toon import Toon, Pista, muelle, pulso, tiembla

_H = None


def lienzo():
    global _H
    if _H is None:
        _H = Toon()
    return _H


class Base(Escena):
    """Escena cartoon90: dibujar(h, t, u) pinta sobre el lienzo compartido; post() puede retocar el cuadro final."""
    GRANO = 0.045
    VIN = 0.5
    BLOOM = 0.0

    def preparar(self):
        self.sonidos()

    def sonidos(self):
        pass

    def render(self, lz, t):
        h = lienzo()
        u = t - self.t0
        h.nuevo(t, None)
        self.dibujar(h, t, u)
        img = h.final(t, grano=self.GRANO, vin=self.VIN, bloom=self.BLOOM)
        return self.post(img, h, t, u)

    def post(self, img, h, t, u):
        return img

    def dibujar(self, h, t, u):
        pass


def inundar(img, h, cx, cy, r, color, k=1.0):
    """Luz que se desborda desde (cx, cy) hasta cubrir el cuadro (transición de la ventana encendida)."""
    if r <= 1:
        return img
    yy, xx = np.mgrid[0:H:3, 0:W:3].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    a = np.clip((1 - d) * 2.2, 0, 1)
    a = a * a * (3 - 2 * a) * k
    import cv2
    a = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    c = np.asarray(color, np.float32) / 255.0
    return img * (1 - a) + c * a


