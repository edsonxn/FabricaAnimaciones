# -*- coding: utf-8 -*-
"""Capa de EFECTOS del estilo «línea blanca + neón» (docs/estilo_linea_neon.md): el neón amarillo de cada imagen palpita
(FX `neon` en todo el video), palabras clave gigantes en blanco al centro (solo énfasis, no karaoke), golpes de cámara en
la alarma del cortisol y SFX de ElevenLabs propios de este video (noche, reloj, arena, ducha, lápiz).
  python fab.py agotado_cortisol fx --seco | fx | fx hoja
Anclas con palabras de timeline.json (Whisper escribe «Uno.» como «1.»: no anclar en los números hablados).
"""

CAMARA = {}
FUNDIDO = {}

_P = dict(tam=140, color="blanco", y=.5, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="DOS RELOJES", en="hay dos relojes", dur=2.0),
    dict(_P, texto="ADENOSINA", en="Se llama adenosina", dur=2.0),
    dict(_P, texto="5 HORAS", en="horas en bajar", dur=1.8, tam=160),
    dict(_P, texto="MELATONINA", en="ordena soltar melatonina", dur=2.0),
    dict(_P, texto="CORTISOL", en=("el villano de la historia|fin", .4), dur=2.2, tam=160),
    dict(_P, texto="ALARMA", en="Pero la alarma", dur=1.8),
    dict(_P, texto="PENDIENTES", en="te asaltan los pendientes", dur=1.8),
    dict(_P, texto="1  LA LISTA", en="Saca los pendientes", dur=2.2),
    dict(_P, texto="−9 MIN", en="minutos más rápido", dur=2.0, tam=170),
    dict(_P, texto="2  AGUA CALIENTE", en="Agua caliente, una hora", dur=2.2, tam=130),
    dict(_P, texto="−1 °C", en="bajar casi un grado", dur=2.0, tam=170),
    dict(_P, texto="3  APAGA LA LUZ", en="Apaga la luz de arriba", dur=2.2, tam=130),
    dict(_P, texto="−90 MIN", en="a la melatonina cerca", dur=2.2, tam=170),
    dict(_P, texto="4  BARAJA", en="Baraja tus pensamientos", dur=2.2),
    dict(_P, texto="PAN", en="Por ejemplo", dur=1.8, tam=180),
    dict(_P, texto="5  LEVÁNTATE", en=("scene-051", .3), dur=2.2),
    dict(_P, texto="ARENA", en="es el de arena", dur=3.0, tam=160),
]

FX = [
    dict(tipo="abre", en=0, dur=1.0),
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    # la cabeza que se enciende
    dict(tipo="destello", en="y tu cabeza se enciende", fuerza=.30, color="amarillo"),
    # el villano y la alarma que no se apaga
    dict(tipo="temblor", en=("el villano de la historia|fin", .4), amp=22),
    dict(tipo="latido", de="Pero con un estrés", a="Pero la alarma, encendida|fin", bpm=104, color="negro", fuerza=.22, zoom=.02),
    dict(tipo="temblor", en="Pero la alarma", amp=14, dur=1.0),
    dict(tipo="vineta", de="te asaltan los pendientes", a="para no olvidarlas|fin", color="negro", fuerza=.6, entra=1.0, sale=.8),
    # las cinco formas
    dict(tipo="destello", en="Saca los pendientes", fuerza=.25, color="amarillo"),
    dict(tipo="destello", en="Agua caliente, una hora", fuerza=.25, color="amarillo"),
    dict(tipo="tinte", de="Por ahí se escapa el calor", a="unos 10 minutos antes|fin", color="azul", k=.15, entra=.8, sale=.8),
    dict(tipo="destello", en="Apaga la luz de arriba", fuerza=.25, color="amarillo"),
    dict(tipo="oscurecer", de="usa lámparas bajas", a="aleja el celular de tu cara|fin", k=.25, entra=.8, sale=.6),
    dict(tipo="destello", en="Baraja tus pensamientos", fuerza=.25, color="amarillo"),
    dict(tipo="destello", en=("scene-051", .3), fuerza=.25, color="amarillo"),
    dict(tipo="zoom", de="es el de arena", a="es el de arena|fin", cuanto=.10, entra=1.5, sale=.5),
    dict(tipo="cierra", en=("es el de arena|fin", 1.2), dur=1.6),
]

SFX = {
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady low hum", 3),
    "reloj": ("Quiet ticking of a bedside analog clock in a silent bedroom at night, steady loop", 6),
    "interruptor": ("Single click of a bedside lamp pull-chain switch, close and quiet", 1),
    "foco": ("Light bulb buzzing on suddenly with a bright electric hum, magical rising shimmer", 2),
    "vibra": ("Phone vibrating once on a wooden nightstand, short buzz", 2),
    "arena": ("Fine sand trickling softly through an hourglass, gentle continuous hiss", 5),
    "villano": ("Low ominous cinematic sting, deep brass swell with a dark rumble", 3),
    "alarma": ("Muffled distant alarm bell ringing in another room, tense, steady loop", 6),
    "lapiz": ("Pencil writing quickly on a paper notepad, scribbling, close up", 4),
    "cajon": ("Metal filing cabinet drawer sliding shut with a soft click", 2),
    "ducha": ("Hot shower running water in a small tiled bathroom, steady", 5),
    "gallo": ("A confused rooster crowing once in the distance at night", 3),
    "baraja": ("Deck of playing cards being shuffled and riffled quickly", 2),
    "almohada": ("Soft punches on a fluffy pillow, muffled thumps, comedic", 2),
    "pantuflas": ("Soft slippers shuffling slowly on a wooden floor at night", 3),
    "golpe": ("Soft deep cinematic hit with a subtle airy whoosh, for a title word appearing", 2),
    "campana": ("Soft warm singing bowl chime, calm, gentle long resonance", 4),
}

PISTAS = [
    dict(sfx="neon", en=0.4, vol=.40),
    dict(sfx="reloj", de=0.5, a="te arrastras a la cama|fin", vol=.20),
    dict(sfx="interruptor", en="Apagas la luz", vol=.55),
    dict(sfx="foco", en="y tu cabeza se enciende", vol=.45),
    dict(sfx="vibra", en="Ese mensaje que no contestaste", vol=.40),
    dict(sfx="arena", de="Se llama adenosina", a="que se acumula como arena|fin", vol=.22),
    dict(sfx="villano", en=("el villano de la historia|fin", .3), vol=.55),
    dict(sfx="alarma", de="Pero con un estrés", a="Pero la alarma, encendida|fin", vol=.16),
    dict(sfx="golpe", en="Saca los pendientes", vol=.45),
    dict(sfx="lapiz", en="escribe en papel", vol=.40),
    dict(sfx="cajon", en="la pestaña quedó guardada", vol=.45),
    dict(sfx="golpe", en="Agua caliente, una hora", vol=.45),
    dict(sfx="ducha", de="Una ducha caliente", a="a las manos y a los pies|fin", vol=.22),
    dict(sfx="golpe", en="Apaga la luz de arriba", vol=.45),
    dict(sfx="gallo", en="no sabe de focos", vol=.35),
    dict(sfx="golpe", en="Baraja tus pensamientos", vol=.45),
    dict(sfx="baraja", en="Cuando te aburras", vol=.40),
    dict(sfx="golpe", en=("scene-051", .3), vol=.45),
    dict(sfx="almohada", en="no pelear con la almohada", vol=.40),
    dict(sfx="pantuflas", en="Ve a otro cuarto", vol=.35),
    dict(sfx="reloj", de=("Las 11 de la noche#2", -.3), a="es el de arena|fin", vol=.14),
    dict(sfx="arena", de="La alarma, apagada", a="es el de arena|fin", vol=.20),
    dict(sfx="campana", en="es el de arena", vol=.45),
]
