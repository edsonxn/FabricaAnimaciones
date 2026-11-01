# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short (estilo «línea blanca + neón», docs/estilo_linea_neon.md): el neón palpita en todo el video,
palabras clave en la franja negra de arriba (la imagen va en una banda centrada en y=.56; el personaje nunca queda debajo
del rótulo) y SFX copiados de freno_enojo/sfx (no se vuelven a pedir).   python fab.py short_suspiro fx --seco | fx | fx hoja
"""

CAMARA = {}
FUNDIDO = {"scene-001": 0}

# Rótulo arriba, encima de la banda de imagen y por encima de la interfaz de Shorts (que tapa ~20 % de abajo)
_P = dict(tam=120, color="blanco", y=.15, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="LÁGRIMAS", en="las lágrimas", dur=1.8, tam=140),
    dict(_P, texto="NO ES DEBILIDAD", en="No es debilidad", dur=1.8, tam=100),
    dict(_P, texto="FRENAZO", en="frenando de golpe", dur=1.8, tam=140),
    dict(_P, texto="SUSPIRO", en="Se llama suspiro", dur=2.6, tam=140, y=.12),
    dict(_P, texto="FISIOLÓGICO", en=("Se llama suspiro", .25), dur=2.35, tam=100, y=.19),
    dict(_P, texto="× 2", en="un segundo jalón", dur=1.8, tam=170),
    dict(_P, texto="ALVÉOLOS", en="los alvéolos", dur=1.8),
    dict(_P, texto="EL DOBLE", en="el doble de largo", dur=1.8, tam=140),
    dict(_P, texto="NERVIO VAGO", en="el nervio vago frena", dur=2.0),
    dict(_P, texto="STANFORD 2023", en="un estudio de Stanford", dur=2.2, tam=100),
    dict(_P, texto="2 O 3", en="Con dos o tres", dur=1.8, tam=170),
    dict(_P, texto="+4 FORMAS", en="cuatro formas más", dur=2.0, tam=130),
    dict(_P, texto="VIDEO COMPLETO", en="el video completo", dur=2.6, tam=100),
]

FX = [
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    dict(tipo="zoom", de=0, a="cuando te enojas|fin", cuanto=.10, entra=.01, sale=.6),     # arranca cerca: el 1.er cuadro manda
    dict(tipo="latido", de=0, a="prepararse para pelear|fin", bpm=110, color="negro", fuerza=.22, zoom=.02),
    dict(tipo="temblor", en="frenando de golpe", amp=18),
    dict(tipo="destello", en="Se llama suspiro", fuerza=.25, color="amarillo"),
    dict(tipo="zoom", de="un segundo jalón", a="un segundo jalón corto de aire|fin", cuanto=.12, entra=.6, sale=.5),
    dict(tipo="zoom", de="Exhalar largo", a="es frenar largo|fin", cuanto=-.10, entra=1.0, sale=.5),
    dict(tipo="destello", en="Con dos o tres", fuerza=.2, color="amarillo"),
    dict(tipo="tinte", de="drenar el coraje", a="drenar el coraje|fin", color="azul", k=.15, entra=.5, sale=.6),
    dict(tipo="cierra", en=("el video completo|fin", .9), dur=1.0),
]

SFX = {   # copiados de videos/freno_enojo/sfx (mismo prompt)
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady hum", 3),
    "latido": ("Slow deep human heartbeat, muffled, inside the chest, steady loop", 6),
    "freno": ("Deep whoosh that suddenly stops, like a heavy brake, followed by silence", 3),
    "inhala": ("Calm deep human inhale through the nose followed by a short second sniff of air", 3),
    "exhala": ("Long slow relaxed human exhale through the mouth", 4),
    "agua": ("Splash of cold water on a face over a bathroom sink, close up", 3),
    "boom": ("Deep soft cinematic sub boom with a long airy reverb tail, dark and calm", 4),
    "golpe": ("Soft deep cinematic hit with a subtle whoosh, for a title word appearing", 2),
    "campana": ("Soft warm singing bowl chime, calm, gentle resonance", 4),
}

PISTAS = [
    dict(sfx="neon", en=0.1, vol=.40),
    dict(sfx="latido", de=0, a="prepararse para pelear|fin", vol=.30),
    dict(sfx="freno", en="frenando de golpe", vol=.50),
    dict(sfx="golpe", en="Se llama suspiro", vol=.50),
    dict(sfx="inhala", en="Inhala profundo", vol=.40),
    dict(sfx="exhala", en="Luego suelta todo", vol=.40),
    dict(sfx="boom", en="el nervio vago frena", vol=.42),
    dict(sfx="campana", en="el golpe baja", vol=.40),
    dict(sfx="agua", en="drenar el coraje", vol=.35),
    dict(sfx="golpe", en="el video completo", vol=.45),
]
