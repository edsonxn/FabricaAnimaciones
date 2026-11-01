# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short (estilo «línea blanca + neón», docs/estilo_linea_neon.md): el neón palpita en todo el video,
palabras clave en la franja negra de arriba (la imagen va en una banda centrada en y=.56) y SFX copiados de
estres_cuerpo/sfx (no se vuelven a pedir).   python fab.py short_dientes fx --seco | fx | fx hoja
"""

CAMARA = {}
FUNDIDO = {"scene-001": 0}

_P = dict(tam=120, color="blanco", y=.15, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="¿DIENTES?", en="Tus dientes se están", dur=1.9, tam=140),
    dict(_P, texto="¿HOMBROS?", en="Tus hombros", dur=1.9, tam=140),
    dict(_P, texto="SIN DARTE CUENTA", en="sin darse cuenta", dur=2.0, tam=90),
    dict(_P, texto="TENSIONAL", en="tipo tensional", dur=2.0, tam=130),
    dict(_P, texto="DESCANSO", en="posición de descanso", dur=1.9, tam=130),
    dict(_P, texto="SEPARADOS", en="dientes separados", dur=1.3, tam=130),      # acaba antes de «LENGUA ARRIBA»
    dict(_P, texto="LENGUA ARRIBA", en="la lengua tocando", dur=2.0, tam=110),
    dict(_P, texto="SOLO AL COMER", en="masticar y tragar", dur=2.0, tam=110),
    dict(_P, texto="UNA NOTA", en="Pega una nota", dur=1.9, tam=130),
    dict(_P, texto="1 DE 5", en="solo uno de", dur=2.0, tam=170),
    dict(_P, texto="VIDEO COMPLETO", en="en el video", dur=2.6, tam=100),
]

FX = [
    dict(tipo="neon", de=0, a=99999, fuerza=.9),
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    dict(tipo="zoom", de="Tus dientes se están", a="Tus dientes se están tocando|fin", cuanto=.12, entra=.5, sale=.5),
    dict(tipo="temblor", en="aprieta los dientes", amp=10),
    dict(tipo="latido", de="Esa tensión", a="tipo tensional|fin", bpm=100, color="negro", fuerza=.22, zoom=.02),
    dict(tipo="destello", en="El arreglo", fuerza=.25, color="amarillo"),
    dict(tipo="zoom", de="dientes separados", a="suavemente el paladar|fin", cuanto=.10, entra=1.0, sale=.5),
    dict(tipo="destello", en="solo uno de", fuerza=.2, color="amarillo"),
    dict(tipo="cierra", en=("en el video|fin", .9), dur=1.0),
]

SFX = {   # copiados de videos/estres_cuerpo/sfx (mismo prompt)
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady low hum", 3),
    "correo": ("Single soft email notification ping", 1),
    "latido": ("Fast heartbeat thumping, close and muffled, tense", 5),
    "punos": ("Leather creaking as fists clench tight, tension", 2),
    "suelta": ("Soft airy whoosh of release, like air leaving a cushion", 2),
    "golpe": ("Soft deep cinematic hit with a subtle airy whoosh, for a title word appearing", 2),
    "campana": ("Soft warm singing bowl chime, calm, gentle long resonance", 4),
}

PISTAS = [
    dict(sfx="neon", en=0.1, vol=.40),
    dict(sfx="golpe", en="Tus dientes se están", vol=.45),
    dict(sfx="punos", en="aprieta los dientes", vol=.45),
    dict(sfx="correo", en="leyendo un mensaje", vol=.40),
    dict(sfx="latido", de="Esa tensión", a="tipo tensional|fin", vol=.28),
    dict(sfx="suelta", en="El arreglo", vol=.45),
    dict(sfx="campana", en="dientes separados", vol=.35),
    dict(sfx="golpe", en="solo uno de", vol=.45),
    dict(sfx="golpe", en="en el video", vol=.40),
]
