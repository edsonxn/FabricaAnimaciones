# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de arana_crias: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "arana_crias", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "mama.jpg"), "REAL LIFE: Wolf spider mom with babies", 520),
         en="Those lumps are babies", dur=3.2, x=.5, y=0.3, sale=.3, nombre="pegatina mama", ver=1.0),
    dict(tipo="temblor", en="Stomp on her", amp=22),
    dict(tipo="destello", en="carry the whole family outside"),
]
ROTULOS = [
    dict(texto="100+", en="carries them on her back", tam=160, color="amarillo", y=.14, dur=2.6),
]
SFX = {
    "foco_short_cri": ("Garage light switching on with a fluorescent buzz and click", 1),
    "corren_short_cri": ("Many tiny legs scurrying in every direction on concrete, quick and comic", 2),
}
PISTAS = [
    dict(sfx="foco_short_cri", en="You see a big spider in the garage", vol=.5),
    dict(sfx="corren_short_cri", en="They run. In every direction", vol=.5),
]
