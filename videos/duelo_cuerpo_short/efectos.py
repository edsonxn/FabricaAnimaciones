# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short (estilo «línea blanca + neón», docs/estilo_linea_neon.md): el neón palpita en todo el video,
palabras clave en la franja negra de arriba (la imagen va en una banda centrada en y=.56) y SFX copiados de
duelo_cuerpo/sfx (no se vuelven a pedir).   python fab.py duelo_cuerpo_short fx --seco | fx | fx hoja
"""

CAMARA = {}
FUNDIDO = {"scene-001": 0}

# Rótulo arriba, encima de la banda de imagen y por encima de la interfaz de Shorts (que tapa ~20 % de abajo)
_P = dict(tam=120, color="blanco", y=.15, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="¿ROTO?", en="romper un corazón", dur=1.8, tam=170),
    dict(_P, texto="SÍ", en="Sí", dur=1.4, tam=190),
    dict(_P, texto="ADRENALINA", en="la oleada de adrenalina", dur=2.0, tam=110),
    dict(_P, texto="UN GLOBO", en="se infla como un globo", dur=1.8, tam=120, y=.07),
    dict(_P, texto="TAKOTSUBO", en="lo llamaron takotsubo", dur=2.4, tam=110, y=.07),
    dict(_P, texto="INFARTO", en="igual que un infarto", dur=1.8, tam=140),
    dict(_P, texto="9 DE 10", en="le pasa a mujeres", dur=2.0, tam=160),
    dict(_P, texto="+50", en="sobre todo después", dur=1.8, tam=170),
    dict(_P, texto="URGENCIAS", en="es a urgencias", dur=2.0, tam=120),
    dict(_P, texto="VIDEO COMPLETO", en="el video completo", dur=2.6, tam=100),
]

FX = [
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    dict(tipo="zoom", de=0, a="de verdad|fin", cuanto=.10, entra=.01, sale=.6),     # arranca cerca: el 1.er cuadro manda
    dict(tipo="latido", de=0, a="en una pantalla|fin", bpm=110, color="negro", fuerza=.22, zoom=.02),
    dict(tipo="destello", en="Sí", fuerza=.25, color="amarillo"),
    dict(tipo="temblor", en="Ante una noticia terrible", amp=16),
    dict(tipo="zoom", de="se infla como un globo", a="se infla como un globo|fin", cuanto=.12, entra=.6, sale=.5),
    dict(tipo="vineta", de="Se siente igual que un infarto", a="falta de aire|fin", color="negro", fuerza=.6, entra=.8, sale=.6),
    dict(tipo="destello", en="es a urgencias", fuerza=.22, color="amarillo"),
    dict(tipo="cierra", en=("el video completo|fin", .9), dur=1.0),
]

SFX = {
    "latido_susto": ("Heartbeat suddenly speeding up, deep muffled chest thumps getting faster and louder", 5),
    "neon_tubo": ("Old neon sign flickering on with a soft electric tick and a warm low buzz", 3),
    "ola": ("Big ocean wave rising and crashing on rocks, deep roar and foam hiss", 4),
    "puerto": ("Small fishing harbor at dawn, water lapping on wooden boats, creaking ropes, distant gulls", 5),
    "ambulancia": ("Ambulance siren passing quickly down a town street at night, doppler fade", 4),
    "titulo": ("Deep soft low piano boom with a breathy rising swell, gentle, for a chapter title", 2),
}

PISTAS = [
    dict(sfx="latido_susto", de=0, a="en una pantalla|fin", vol=.22),
    dict(sfx="neon_tubo", en="Sí", vol=.30),
    dict(sfx="ola", en="la oleada de adrenalina", vol=.30),
    dict(sfx="puerto", en="En Japón", vol=.28),
    dict(sfx="ambulancia", en="es a urgencias", vol=.25),
    dict(sfx="titulo", en="el video completo", vol=.40),
]
