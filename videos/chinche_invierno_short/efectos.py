# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de chinche_invierno: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "chinche_invierno", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "chinche.jpg"), "REAL LIFE: Brown marmorated stink bug", 520),
         en="No eating, no eggs", dur=3.2, x=.5, y=.27, sale=.3, nombre="pegatina chinche", ver=1.0),
    dict(tipo="temblor", en="Squeeze one, and it sprays", amp=22),
    dict(tipo="destello", en="Drop it in a jar"),
]
ROTULOS = [
    dict(texto="26,000+", en="counted more than twenty-six thousand", tam=170, color="amarillo", y=.14, dur=2.6),
]
SFX = {
    "aterriza_short_chi": ("Tiny clumsy beetle landing on soft flannel fabric, a soft cartoon thump with a short buzz", 1),
    "pfft_short_chi": ("Short comic spray puff, a squeaky cartoon pfft of a smelly gas cloud", 1),
}
PISTAS = [
    dict(sfx="aterriza_short_chi", en="lands on your sleeve", vol=.6),
    dict(sfx="pfft_short_chi", en="it sprays a chemical", vol=.6),
]
