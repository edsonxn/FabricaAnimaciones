# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de polilla_foco: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "polilla_foco", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "polilla.jpg"), "REAL LIFE: Banded tussock moth", 520),
         en="They are trapped", dur=3.2, x=.5, y=0.3, sale=.3, nombre="pegatina polilla", ver=1.0),
    dict(tipo="temblor", en="It can even flip upside down", amp=22),
    dict(tipo="destello", en="or just flip the switch"),
]
ROTULOS = [
    dict(texto="TRAPPED", en="ends up flying in circles", tam=160, color="amarillo", y=.14, dur=2.6),
]
SFX = {
    "aleteo_short_pol": ("Soft papery flutter of a moth bumping a glass lamp, tiny taps", 2),
    "interruptor_short_pol": ("Single crisp click of a light switch turning off, a soft electric hum stopping", 1),
}
PISTAS = [
    dict(sfx="aleteo_short_pol", en="Moths circling your porch light", vol=.5),
    dict(sfx="interruptor_short_pol", en="just flip the switch", vol=.5),
]
