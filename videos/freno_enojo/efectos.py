# -*- coding: utf-8 -*-
"""Capa de EFECTOS del estilo «línea blanca + neón» (docs/estilo_linea_neon.md): el neón amarillo de cada imagen palpita
(FX `neon` en todo el video), palabras clave gigantes en blanco al centro (solo énfasis, no karaoke: decisión del usuario,
16-oct-2026), golpes de cámara en los momentos de alarma y SFX de ElevenLabs.
  python fab.py freno_enojo fx --seco | fx | fx hoja
"""

CAMARA = {}
FUNDIDO = {}

# Palabra clave al centro, como en las referencias (PEOPLE, BACK, HUNTING): blanca, Poppins Black, con sombra
_P = dict(tam=140, color="blanco", y=.5, pop=.35, sale=.25)


ROTULOS = [
    dict(_P, texto="QUÍMICA", en="Es química", dur=1.6),
    dict(_P, texto="AMÍGDALA", en="amígdala", dur=1.8),
    dict(_P, texto="ADRENALINA", en="Y sueltan adrenalina", dur=2.0, tam=150),
    dict(_P, texto="GLUCOSA", en="libera glucosa", dur=1.8),
    dict(_P, texto="TÚNEL", en="un túnel", dur=1.6),
    dict(_P, texto="NERVIO VAGO", en="es el nervio vago", dur=2.0),
    dict(_P, texto="QUEMAR", en="Quemar el combustible", dur=1.6),
    dict(_P, texto="FRENAR", en="o frenar poco a poco", dur=1.6),
    dict(_P, texto="1  SUSPIRO", en="Uno. El suspiro", dur=2.2),
    dict(_P, texto="× 2", en="el doble de largo", dur=1.6, tam=170),
    dict(_P, texto="2  TENSIÓN", en="Dos. Tensión", dur=2.2),
    dict(_P, texto="10 SEGUNDOS", en="Diez segundos al máximo", dur=1.8),
    dict(_P, texto="3  FRÍO", en="Tres. El reflejo", dur=2.2),
    dict(_P, texto="−25 %", en="entre un diez", dur=2.4, tam=170),
    dict(_P, texto="4  SACÚDETE", en="Cuatro. Sacudirte", dur=2.2),
    dict(_P, texto="5  MIRADA", en="Cinco. Abre la mirada", dur=2.2),
    dict(_P, texto="CALMA", en="desde la calma", dur=3.0, tam=160),
]

FX = [
    dict(tipo="abre", en=0, dur=1.0),
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    # alarma: el cuerpo se acelera
    dict(tipo="latido", de="El corazón se acelera", a="Los puños se cierran|fin", bpm=120, color="negro", fuerza=.25, zoom=.025),
    dict(tipo="temblor", en="Y sueltan adrenalina", amp=26),
    dict(tipo="destello", en="Y sueltan adrenalina", fuerza=.35, color="amarillo"),
    dict(tipo="zoom", de="la vista se cierra en un túnel", a="la vista se cierra en un túnel|fin", cuanto=.22, entra=1.2, sale=.6),
    dict(tipo="vineta", de="la vista se cierra en un túnel", a="no haces ninguna de las dos|fin", color="negro", fuerza=.7, entra=1.0, sale=.8),
    # rebote: frenazo
    dict(tipo="temblor", en="el cerebro pisa el freno de golpe", amp=20),
    dict(tipo="desaturar", de="la garganta y los ojos", a="la garganta y los ojos|fin", k=.6, entra=.5, sale=.6),
    # métodos
    dict(tipo="destello", en="Uno. El suspiro", fuerza=.25, color="amarillo"),
    dict(tipo="destello", en="Dos. Tensión", fuerza=.25, color="amarillo"),
    dict(tipo="temblor", en="Diez segundos al máximo", amp=10, dur=1.2),
    dict(tipo="destello", en="Tres. El reflejo", fuerza=.25, color="blanco"),
    dict(tipo="tinte", de="Tres. El reflejo", a="veinticinco por ciento|fin", color="azul", k=.18, entra=.8, sale=.8),
    dict(tipo="destello", en="Cuatro. Sacudirte", fuerza=.25, color="amarillo"),
    dict(tipo="destello", en="Cinco. Abre la mirada", fuerza=.25, color="amarillo"),
    dict(tipo="zoom", de="con el rabillo del ojo", a="con el rabillo del ojo|fin", cuanto=-.12, entra=1.5, sale=.5),
    dict(tipo="cierra", en=("desde la calma|fin", 1.2), dur=1.5),
]

SFX = {
    "boom": ("Deep soft cinematic sub boom with a long airy reverb tail, dark and calm", 4),
    "latido": ("Slow deep human heartbeat, muffled, inside the chest, steady loop", 6),
    "latido_rapido": ("Fast pounding human heartbeat, muffled, tense, steady loop", 6),
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady hum", 3),
    "zumbido": ("Low tense electric drone rising in pitch, adrenaline rush, cinematic riser", 4),
    "freno": ("Deep whoosh that suddenly stops, like a heavy brake, followed by silence", 3),
    "inhala": ("Calm deep human inhale through the nose followed by a short second sniff of air", 3),
    "exhala": ("Long slow relaxed human exhale through the mouth", 4),
    "agua": ("Splash of cold water on a face over a bathroom sink, close up", 3),
    "tension": ("Muscles straining, low creaking tension sound, rising then sudden release whoosh", 3),
    "pasos": ("Brisk footsteps walking quickly on a wooden floor, a few seconds", 4),
    "campana": ("Soft warm singing bowl chime, calm, gentle resonance", 4),
    "golpe": ("Soft deep cinematic hit with a subtle whoosh, for a title word appearing", 2),
}

PISTAS = [
    dict(sfx="neon", en=0.4, vol=.45),
    dict(sfx="latido", de="Estás en medio", a="se te cierra la garganta|fin", vol=.30),
    dict(sfx="boom", en="Es química", vol=.55),
    dict(sfx="zumbido", en="Avisa al hipotálamo", vol=.35),
    dict(sfx="golpe", en="Y sueltan adrenalina", vol=.6),
    dict(sfx="latido_rapido", de="El corazón se acelera", a="no haces ninguna de las dos|fin", vol=.32),
    dict(sfx="freno", en="el cerebro pisa el freno de golpe", vol=.5),
    dict(sfx="boom", en="es el nervio vago", vol=.45),
    dict(sfx="golpe", en="Uno. El suspiro", vol=.5),
    dict(sfx="inhala", en="Inhala profundo", vol=.40),
    dict(sfx="exhala", en="Luego suelta todo", vol=.40),
    dict(sfx="golpe", en="Dos. Tensión", vol=.5),
    dict(sfx="tension", en="Diez segundos al máximo", vol=.45),
    dict(sfx="golpe", en="Tres. El reflejo", vol=.5),
    dict(sfx="agua", en="échate agua bien fría", vol=.5),
    dict(sfx="golpe", en="Cuatro. Sacudirte", vol=.5),
    dict(sfx="pasos", en="camina rápido", vol=.35),
    dict(sfx="golpe", en="Cinco. Abre la mirada", vol=.5),
    dict(sfx="boom", en="El combo para la vida real", vol=.45),
    dict(sfx="latido", de="Pasan cinco minutos#2", a="drenó la tormenta|fin", vol=.22),
    dict(sfx="campana", en="desde la calma", vol=.45),
]
