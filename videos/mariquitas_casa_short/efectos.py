# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short vertical de mariquitas_casa: foto real como pegatina, un rótulo de énfasis y dos SFX propios.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "..", "mariquitas_casa", "pegatinas")

CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 0

FX = [
    dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, "asiatica.jpg"), "REAL LIFE: Asian lady beetle", 520),
         en="See the little M on the head", dur=3.2, x=.5, y=.40, sale=.3, nombre="pegatina asiatica", ver=1.0),
    dict(tipo="temblor", en="Do not squish them", amp=22),
    dict(tipo="destello", en="seal the gaps"),
]
ROTULOS = [
    dict(texto="ALL WINTER", en="For the whole winter", tam=160, color="amarillo", y=.14, dur=2.4),
]
SFX = {
    "enjambre_short_mar": ("Soft rustle of hundreds of tiny beetles crawling on a sunny wooden wall, light clicking", 2),
    "aspira_short_mar": ("Short handheld vacuum cleaner whir that sucks something up with a little pop", 2),
}
PISTAS = [
    dict(sfx="enjambre_short_mar", en="Hundreds of ladybugs on your house", vol=.45),
    dict(sfx="aspira_short_mar", en="Vacuum them up", vol=.5),
]
