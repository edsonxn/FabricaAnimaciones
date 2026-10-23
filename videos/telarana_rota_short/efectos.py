# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de telarana_rota: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "telarana_rota", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "arana.jpg"), "REAL LIFE: Furrow orb weaver", 520),
         en="The spider dropped on a safety line", dur=3.2, x=.5, y=0.3, sale=.3, nombre="pegatina arana", ver=1.0),
    dict(tipo="temblor", en="You sweep away a spider web", amp=22),
    dict(tipo="destello", en="fewer bugs means fewer webs"),
]
ROTULOS = [
    dict(texto="65 FT", en="sixty-five feet of silk", tam=160, color="amarillo", y=.14, dur=2.6),
]
SFX = {
    "escoba_short_tel": ("Quick broom swish snapping thin silk threads, light and comic", 1),
    "hilo_short_tel": ("Fast cartoon zip of a tiny spider sliding down a silk line", 1),
}
PISTAS = [
    dict(sfx="escoba_short_tel", en="You sweep away a spider web", vol=.5),
    dict(sfx="hilo_short_tel", en="The spider dropped on a safety line", vol=.5),
]
