# -*- coding: utf-8 -*-
"""¿Cómo VE una IA? — largo horizontal en ACUARELA PINTADA A MANO POR CÓDIGO (kit acuarela.py).
Un solo plano secuencia: `Mundo` dibuja el cuadro entero en función del tiempo global; cada plano_*.py cubre un tramo.
    plano_a.py  gancho     la foto del gato, dibujo/radiografía/meme, «no tiene ojos», zoom al interior de Kuri
    plano_b.py  pixeles    zoom a los píxeles, R/V/A, 36 millones de números, la tabla, los números cambian, reglas a mano
    (siguientes: gato 1959, neurona y filtros, capas, aprender, ImageNet, parches, palabras, trucos, cierre)"""
import importlib

from escena_base import Escena, TL

PLANOS = []
for nombre in ("plano_a", "plano_b", "plano_c", "plano_d", "plano_e", "plano_f", "plano_g", "plano_h", "plano_i", "plano_j",
               "plano_k"):
    try:
        PLANOS.append(importlib.import_module(nombre))
    except ModuleNotFoundError as e:
        if e.name != nombre:
            raise
PLANOS.sort(key=lambda m: getattr(m, "T_INI", 0.0))


def cuadro(t):
    m = PLANOS[0]
    for p in PLANOS:
        if t >= getattr(p, "T_INI", 0.0):
            m = p
    return m.cuadro(t)


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
