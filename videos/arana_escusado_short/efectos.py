# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de arana_escusado: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "arana_escusado", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="temblor", en="You flush a spider", amp=26),
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "casa.jpg"), "REAL LIFE: House spider", 520),
         en="Gone. But where does", dur=3.0, x=.5, y=.40, sale=.3, nombre="pegatina casa", ver=1.0),
    dict(tipo="destello", en="Then they dried off"),
]
ROTULOS = [
    dict(texto="16 HOURS", en="kept spiders underwater for sixteen hours", tam=170, color="amarillo", y=.14, dur=2.6),
]
SFX = {
    "flush_short_esc": ("Quick toilet flush whoosh with a bright gurgle, short and punchy", 2),
    "tobogan_short_esc": ("Fast cartoon water slide swish with splashes", 2),
}
PISTAS = [
    dict(sfx="flush_short_esc", en="You flush a spider", vol=.7),
    dict(sfx="tobogan_short_esc", en="The biggest water slide on Earth", vol=.55),
]
