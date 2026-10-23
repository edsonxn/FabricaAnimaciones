# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short (estilo «línea blanca + neón», docs/estilo_linea_neon.md): el neón palpita en todo el video,
palabras clave en la franja negra de arriba (la imagen va en una banda centrada en y=.56) y SFX copiados de
despertar_3am/sfx (no se vuelven a pedir).   python fab.py despertar_3am_short fx --seco | fx | fx hoja
"""

CAMARA = {}
FUNDIDO = {"scene-001": 0}

# Rótulo arriba, encima de la banda de imagen y por encima de la interfaz de Shorts (que tapa ~20 % de abajo)
_P = dict(tam=120, color="blanco", y=.15, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="3 AM", en="todo parece", dur=1.8, tam=190),
    dict(_P, texto="LA CABEZA", en="empieza lo peor", dur=2.0, tam=130),
    dict(_P, texto="MÁS GRAVE", en="todo parece más grave", dur=2.0, tam=140),
    dict(_P, texto="NEGATIVO", en="se inclina hacia lo negativo", dur=2.2, tam=130),
    dict(_P, texto="SIN FRENO", en="pone freno", dur=2.0, tam=130),
    dict(_P, texto="ABISMO", en="parece un abismo", dur=1.8, tam=160),
    dict(_P, texto="PENDIENTE", en="es solo un pendiente", dur=2.0, tam=130),
    dict(_P, texto="VIDEO COMPLETO", en="el video completo", dur=2.6, tam=100),
]

FX = [
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    dict(tipo="zoom", de=0, a="parece peor|fin", cuanto=.10, entra=.01, sale=.6),     # arranca cerca: el 1.er cuadro manda
    dict(tipo="latido", de=0, a="parece peor|fin", bpm=96, color="negro", fuerza=.20, zoom=.015),
    dict(tipo="destello", en="todo parece más grave", fuerza=.22, color="amarillo"),
    dict(tipo="temblor", en="parece un abismo", amp=14, dur=.7),
    dict(tipo="vineta", de="parece un abismo", a="parece un abismo|fin", color="negro", fuerza=.6, entra=.5, sale=.6),
    dict(tipo="destello", en="es solo un pendiente", fuerza=.22, color="amarillo"),
    dict(tipo="cierra", en=("el video completo|fin", .9), dur=1.0),
]

SFX = {
    "reloj_cama": ("Small wind-up alarm clock ticking loudly on a wooden nightstand in a silent bedroom", 4),
    "trueno": ("Distant soft thunder rolling far away at night, no rain", 4),
    "papeles": ("Envelopes and paper bills shuffled nervously on a wooden table", 2),
    "canon": ("Cold wind blowing across a deep empty canyon at night, hollow and lonely", 4),
    "cafe_manana": ("Morning kitchen, coffee poured into a ceramic cup, birds chirping outside", 3),
    "cuerda": ("Old clock being wound by hand, ratcheting brass spring clicks speeding up", 3),
    "peldano": ("Soft low felt-piano note with a shimmering glassy tail, gentle chapter marker", 2),
}

PISTAS = [
    dict(sfx="reloj_cama", en=0.1, vol=.30),
    dict(sfx="trueno", en="empieza lo peor", vol=.28),
    dict(sfx="papeles", en="Las deudas", vol=.35),
    dict(sfx="canon", en="parece un abismo", vol=.30),
    dict(sfx="cafe_manana", en="con luz", vol=.25),
    dict(sfx="cuerda", en="tu cuerpo te despierta", vol=.32),
    dict(sfx="peldano", en="el video completo", vol=.40),
]
