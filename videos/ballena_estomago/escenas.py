# -*- coding: utf-8 -*-
"""¿Qué pasaría si una ballena te tragara? — Short vertical en ACUARELA PINTADA A MANO POR CÓDIGO (kit acuarela.py).
Un solo plano secuencia: `Mundo` dibuja el cuadro entero en función del tiempo global.
    plano_gancho.py   0-10,8 s  buceo → la boca sube → negro → por fuera, ¡GLUP!
    plano_resto.py    10,8-75 s garganta, jorobada 2021, cachalote, estómago, ácido, inmersión, presión, vómito, cierre"""
import numpy as np

import plano_gancho as G
from escena_base import Escena, TL

try:
    import plano_resto as R
except ImportError:                      # mientras se escribe
    R = None


def cuadro(t):
    if R is None or t < R.T_INI:
        return G.cuadro(t)
    return R.cuadro(t, G)


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
