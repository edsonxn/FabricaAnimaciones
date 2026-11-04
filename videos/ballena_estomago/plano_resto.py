# -*- coding: utf-8 -*-
"""Despachador de 10,8-75 s: plano_b (garganta, jorobada, cachalote) y plano_c (estómago, ácido, inmersión, presión, vómito,
cierre), con sus transiciones de desborde. `sonidos(S)` devuelve los SFX sintetizados de este tramo (S = módulo sfx_proc)."""
from acuarela import pr
from comun import desborde

import plano_b as B

try:
    import plano_c as C
except ImportError:
    C = None

T_INI = B.T_INI


def cuadro(t, G):
    if t < B.T_INI + 0.55:
        return B.entrada(t, G)
    if C is None or t < C.T_INI:
        return B.cuadro(t)
    if t < C.T_INI + 0.6:
        return desborde(B.cuadro(t), C.cuadro(t), pr(t, C.T_INI, C.T_INI + 0.6), cx=540, cy=200, borde=(0.15, 0.05, 0.08))
    return C.cuadro(t)


def sonidos(S):
    P = []
    import sonidos_resto
    P += sonidos_resto.lista(S)
    return P
