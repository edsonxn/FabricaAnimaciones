# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de hormigas_cocina: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "hormigas_cocina", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "hormiga.jpg"), "REAL LIFE: Odorous house ant", 520),
         en="And the ants you see may be", dur=3.2, x=.5, y=0.3, sale=.3, nombre="pegatina hormiga", ver=1.0),
    dict(tipo="temblor", en="Squish a few drivers", amp=22),
    dict(tipo="destello", en="Erase the map"),
]
ROTULOS = [
    dict(texto="x3", en="the colony can split into three", tam=160, color="amarillo", y=.14, dur=2.6),
]
SFX = {
    "pisa_short_hor": ("Small cartoon squish with a squeaky rub of a paper towel on a counter", 1),
    "esponja_short_hor": ("Wet soapy sponge wiping a kitchen counter with little bubble pops", 2),
}
PISTAS = [
    dict(sfx="pisa_short_hor", en="You squish the ants", vol=.5),
    dict(sfx="esponja_short_hor", en="Wipe the trail with soapy water", vol=.5),
]
