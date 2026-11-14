# -*- coding: utf-8 -*-
"""Amaya 3: Matemáticas — ACUARELA PINTADA A MANO POR CÓDIGO (kit acuarela.py) + el profe Tilde (kit_amaya.papa).
Un solo plano secuencia: `Mundo` dibuja el cuadro entero en función del tiempo global; cada plano_*.py cubre un tramo.
    a gancho · b decimales+preg1 · c números grandes · d trampa 7,735,923 · e triángulos+preg3 · f plano cartesiano+preg4 · g fracciones · h preg5+repaso+cierre"""
import importlib

from escena_base import Escena, TL

PLANOS = []
for nombre in ("plano_a", "plano_b", "plano_c", "plano_d", "plano_e", "plano_f", "plano_g", "plano_h", ):
    try:
        PLANOS.append(importlib.import_module(nombre))
    except ModuleNotFoundError as e:
        if e.name != nombre:
            raise
PLANOS.sort(key=lambda m: getattr(m, "T_INI", 0.0))

TRANS = 0.8      # cada plano entra sobre el anterior como acuarela que se desborda


def cuadro(t):
    from acuarela import H, W, pr, terminar
    from comun import desborde
    i = 0
    for k, p in enumerate(PLANOS):
        if t >= getattr(p, "T_INI", 0.0):
            i = k
    m = PLANOS[i]
    t0 = getattr(m, "T_INI", 0.0)
    if i > 0 and t < t0 + TRANS and getattr(m, "DESBORDE", True):
        return terminar(desborde(PLANOS[i - 1].cuadro_crudo(t), m.cuadro_crudo(t), pr(t, t0, t0 + TRANS), W / 2, H / 2), t)
    return m.cuadro(t)


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
