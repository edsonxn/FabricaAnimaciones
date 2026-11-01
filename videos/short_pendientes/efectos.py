# -*- coding: utf-8 -*-
"""Capa de EFECTOS del Short (estilo «línea blanca + neón», docs/estilo_linea_neon.md): el neón palpita en todo el video,
palabras clave en la franja negra de arriba (la imagen va en una banda centrada en y=.56) y SFX copiados de
agotado_cortisol/sfx (no se vuelven a pedir).   python fab.py short_pendientes fx --seco | fx | fx hoja
"""

CAMARA = {}
FUNDIDO = {"scene-001": 0}

_P = dict(tam=120, color="blanco", y=.15, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="PENDIENTES", en="todos tus pendientes", dur=1.9, tam=130),
    dict(_P, texto="ZEIGARNIK", en="Bluma", dur=2.2, tam=120, y=.12),
    dict(_P, texto="1927", en=("Bluma", .2), dur=2.0, tam=100, y=.19),
    dict(_P, texto="INTERRUMPIDAS", en="tareas interrumpidas", dur=1.9, tam=100),
    dict(_P, texto="PESTAÑAS", en="todas las pestañas", dur=1.9, tam=130),
    dict(_P, texto="5 MINUTOS", en="El truco toma", dur=1.9, tam=130),
    dict(_P, texto="EN PAPEL", en="escribe en papel", dur=1.8, tam=130),
    dict(_P, texto="BAYLOR 2018", en="Universidad de Baylor", dur=2.2, tam=110),
    dict(_P, texto="−9 MIN", en="Se durmieron", dur=2.4, tam=170),
    dict(_P, texto="GUARDADA", en="quedó guardada", dur=1.8, tam=130),
    dict(_P, texto="+4 TRUCOS", en="cuatro trucos más", dur=2.0, tam=130),
    dict(_P, texto="VIDEO COMPLETO", en="el video completo", dur=2.6, tam=100),
]

FX = [
    dict(tipo="neon", de=0, a=99999, fuerza=.9),
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    dict(tipo="tinte", de=0, a="todos tus pendientes|fin", color="azul", k=.12, entra=.01, sale=.8),   # la noche
    dict(tipo="destello", en="tu cabeza se enciende", fuerza=.3, color="amarillo"),
    dict(tipo="temblor", en="tu cabeza se enciende", amp=10),
    dict(tipo="zoom", de="todas las pestañas", a="para no olvidarlas|fin", cuanto=.12, entra=1.0, sale=.4),
    dict(tipo="destello", en="El truco toma", fuerza=.22, color="amarillo"),
    dict(tipo="zoom", de="Se durmieron", a="ya habían terminado|fin", cuanto=.10, entra=1.2, sale=.4),
    dict(tipo="cierra", en=("el video completo|fin", .9), dur=1.0),
]

SFX = {   # copiados de videos/agotado_cortisol/sfx (mismo prompt)
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady low hum", 3),
    "interruptor": ("Single click of a bedside lamp pull-chain switch, close and quiet", 1),
    "reloj": ("Quiet ticking of a bedside analog clock in a silent bedroom at night, steady loop", 6),
    "lapiz": ("Pencil writing quickly on a paper notepad, scribbling, close up", 4),
    "cajon": ("Metal filing cabinet drawer sliding shut with a soft click", 2),
    "ducha": ("Hot shower running water in a small tiled bathroom, steady", 5),
    "golpe": ("Soft deep cinematic hit with a subtle airy whoosh, for a title word appearing", 2),
    "campana": ("Soft warm singing bowl chime, calm, gentle long resonance", 4),
}

PISTAS = [
    dict(sfx="interruptor", en=0.25, vol=.55),
    dict(sfx="neon", en="tu cabeza se enciende", vol=.40),
    dict(sfx="reloj", de=0, a="para no olvidarlas|fin", vol=.22),
    dict(sfx="golpe", en="El truco toma", vol=.50),
    dict(sfx="lapiz", en="escribe en papel", vol=.40),
    dict(sfx="campana", en="Se durmieron", vol=.35),
    dict(sfx="cajon", en="quedó guardada", vol=.45),
    dict(sfx="ducha", en="cuatro trucos más", vol=.22),
    dict(sfx="golpe", en="el video completo", vol=.45),
]
