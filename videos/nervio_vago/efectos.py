# -*- coding: utf-8 -*-
"""Capa de EFECTOS del estilo «línea blanca + neón» (docs/estilo_linea_neon.md): el neón amarillo de cada imagen palpita
(FX `neon` en todo el video), palabras clave gigantes en blanco (solo énfasis, no karaoke; fuera del personaje y del neón
que nombran: lección de estres_cuerpo), latido en el miedo escénico y SFX de ElevenLabs propios de este video (auditorio,
laboratorio de 1921, corazón de rana, desmayo, frío, coro).
  python fab.py nervio_vago fx --seco | fx | fx hoja
Anclas con palabras de timeline.json (Whisper escribe los números hablados como cifras: no anclar en ellos).
"""

CAMARA = {}
FUNDIDO = {}

_P = dict(tam=140, color="blanco", y=.5, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="NERVIO", en="Se llama nervio vago", dur=2.4, tam=130, x=.2, y=.43),
    dict(_P, texto="VAGO", en="Se llama nervio vago", dur=2.4, tam=130, x=.2, y=.57),
    dict(_P, texto="ERRANTE", en="significa errante", dur=2.0, y=.14),
    dict(_P, texto="DESCANSAR", en="el modo de descansar", dur=2.4, tam=110, x=.2, y=.43),
    dict(_P, texto="Y DIGERIR", en="el modo de descansar", dur=2.4, tam=110, x=.2, y=.57),
    dict(_P, texto="EL FRENO", en="el vago es el freno", dur=2.0, tam=150, x=.24, y=.18),
    dict(_P, texto="8 DE 10", en="fibras del vago", dur=2.4, tam=150, x=.2, y=.2),
    dict(_P, texto="1921", en="Austria", dur=2.2, tam=190, x=.22, y=.2),
    dict(_P, texto="ACETILCOLINA", en="la conocemos como acetilcolina", dur=2.4, tam=120, y=.14),
    dict(_P, texto="NOBEL", en="el premio Nobel", dur=2.2, tam=150, x=.8, y=.14),
    dict(_P, texto="~100", en="sin nervios, latiría", dur=2.2, tam=190, x=.22),
    dict(_P, texto="60 · 70", en="Si estás sentado con", dur=2.4, tam=180, x=.22, y=.18),
    dict(_P, texto="VARIABILIDAD", en="se le llama variabilidad", dur=2.4, tam=120, y=.16),
    dict(_P, texto="TONO VAGAL", en="lo que se llama tono vagal", dur=2.4, tam=140, x=.3, y=.16),
    dict(_P, texto="FRENAZO", en="un frenazo", dur=2.0, tam=170, x=.25, y=.18),
    dict(_P, texto="SÍNCOPE", en="Se llama síncope vasovagal", dur=2.6, tam=120, x=.72, y=.43),
    dict(_P, texto="VASOVAGAL", en="Se llama síncope vasovagal", dur=2.6, tam=120, x=.72, y=.57),
    dict(_P, texto="REFLEJO", en="Lo llamaron el reflejo inflamatorio", dur=2.6, tam=120, x=.3, y=.6),
    dict(_P, texto="INFLAMATORIO", en="Lo llamaron el reflejo inflamatorio", dur=2.6, tam=120, x=.3, y=.74),
    dict(_P, texto="2025", en="Estados Unidos aprobó", dur=2.2, tam=190, x=.22, y=.2),
    dict(_P, texto="MEDICINA REAL", en="es medicina real", dur=2.2, tam=130, y=.86),
    dict(_P, texto="NO HAY", en="No hay botón de reinicio", dur=2.4, tam=120, x=.82, y=.43),
    dict(_P, texto="BOTÓN", en="No hay botón de reinicio", dur=2.4, tam=120, x=.82, y=.57),
    dict(_P, texto="1  EXHALA", en="exhala más largo", dur=2.4, tam=120, x=.24, y=.78),
    dict(_P, texto="4 · 8", en="Toma aire en", dur=2.6, tam=180, x=.78),
    dict(_P, texto="6 POR MINUTO", en="respiraciones por minuto", dur=2.4, tam=120, y=.16),
    dict(_P, texto="2  FRÍO", en="frío en el cuello", dur=2.4, tam=130, x=.5, y=.16),
    dict(_P, texto="3  CANTA", en="Canta", dur=2.4, tam=120, x=.83),
    dict(_P, texto="4  MUÉVETE", en="Muévete", dur=2.4, tam=120, x=.74, y=.2),
    dict(_P, texto="5  LA GENTE", en="la gente", dur=2.4, tam=120, x=.24, y=.78),
    dict(_P, texto="EL FRENO", en="dónde pisarlo", dur=3.0, tam=140, x=.28, y=.3),
]

FX = [
    dict(tipo="abre", en=0, dur=1.0),
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    # miedo escénico: latido negro
    dict(tipo="latido", de=0.6, a="la voz empieza a temblar|fin", bpm=112, color="negro", fuerza=.22, zoom=.02),
    dict(tipo="destello", en="Se llama nervio vago", fuerza=.25, color="amarillo"),
    # el sueño de Loewi y el segundo corazón que se frena
    dict(tipo="tinte", de="Austria", a="la idea regresa|fin", color="azul", k=.12, entra=.8, sale=.8),
    dict(tipo="destello", en="también se frena", fuerza=.30, color="amarillo"),
    # el frenazo vasovagal
    dict(tipo="vineta", de="el freno se pisa con todo", a="por unos segundos|fin", color="negro", fuerza=.65, entra=1.2, sale=.8),
    dict(tipo="temblor", en="No hay botón de reinicio", amp=10, dur=.8),
    # las cinco técnicas
    dict(tipo="destello", en="exhala más largo", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="frío en el cuello", fuerza=.22, color="amarillo"),
    dict(tipo="tinte", de="frío en el cuello", a="pregunta antes|fin", color="azul", k=.12, entra=.8, sale=.8),
    dict(tipo="destello", en="Canta", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="Muévete", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="la gente", fuerza=.22, color="amarillo"),
    dict(tipo="zoom", de="dónde pisarlo", a="dónde pisarlo|fin", cuanto=.10, entra=1.5, sale=.5),
    dict(tipo="cierra", en=("dónde pisarlo|fin", 1.2), dur=1.6),
]

SFX = {
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady low hum", 3),
    "auditorio": ("Quiet school auditorium ambience, people shuffling in seats, a single nervous cough, microphone hum", 6),
    "latido": ("Fast heartbeat thumping, close and muffled, tense", 5),
    "golpe": ("Soft deep cinematic hit with a subtle airy whoosh, for a title word appearing", 2),
    "reloj": ("Old mechanical alarm clock ticking in a quiet bedroom at night", 4),
    "lapiz": ("Pencil scribbling quickly on paper in the dark", 2),
    "laboratorio": ("1920s laboratory: glass flasks clinking, a bubbling liquid, a small electrical buzz", 5),
    "chispa": ("Small electric spark zap from an old brass apparatus", 1),
    "gota": ("Liquid poured gently from a glass beaker into another, clean trickle", 2),
    "latido_lento": ("Single slow calm heartbeat thump, deep and soft, repeating slowly", 4),
    "desmayo": ("Low dull whoosh dropping in pitch, like hearing fade before fainting, muffled", 3),
    "notificacion": ("Several overlapping phone notification pings and short social-video sounds, busy", 2),
    "frio": ("Cold wet towel pressed on skin with ice cubes clinking in a bowl", 2),
    "coro": ("Small choir humming one warm sustained note together, soft, no words", 4),
    "pasos": ("Running footsteps on a park path, steady breathing", 3),
    "risas": ("Friends laughing softly together around a table, warm", 3),
    "campana": ("Soft warm singing bowl chime, calm, gentle long resonance", 4),
}

PISTAS = [
    dict(sfx="neon", en=0.4, vol=.40),
    dict(sfx="auditorio", de=0.5, a="la voz empieza a temblar|fin", vol=.22),
    dict(sfx="latido", de=0.6, a="la voz empieza a temblar|fin", vol=.20),
    dict(sfx="golpe", en="Se llama nervio vago", vol=.45),
    dict(sfx="golpe", en="el vago es el freno", vol=.40),
    dict(sfx="reloj", en="Austria", vol=.30),
    dict(sfx="lapiz", en="La apunta en un papelito", vol=.40),
    dict(sfx="laboratorio", en="se va directo al laboratorio", vol=.28),
    dict(sfx="chispa", en="con electricidad", vol=.40),
    dict(sfx="gota", en="lo pasa al segundo", vol=.40),
    dict(sfx="latido_lento", en="también se frena", vol=.35),
    dict(sfx="golpe", en="el premio Nobel", vol=.40),
    dict(sfx="latido_lento", en="frenando tu corazón ahora mismo", vol=.30),
    dict(sfx="golpe", en="un frenazo", vol=.45),
    dict(sfx="desmayo", en="el freno se pisa con todo", vol=.40),
    dict(sfx="notificacion", en="en redes", vol=.35),
    dict(sfx="golpe", en="exhala más largo", vol=.40),
    dict(sfx="golpe", en="frío en el cuello", vol=.40),
    dict(sfx="frio", en="Una toalla fría", vol=.40),
    dict(sfx="golpe", en="Canta", vol=.40),
    dict(sfx="coro", en="cantando juntos", vol=.30),
    dict(sfx="golpe", en="Muévete", vol=.40),
    dict(sfx="pasos", en="Caminar rápido", vol=.30),
    dict(sfx="golpe", en="la gente", vol=.40),
    dict(sfx="risas", en="una risa", vol=.30),
    dict(sfx="auditorio", de="Así que la próxima vez", a="hazle caso|fin", vol=.18),
    dict(sfx="campana", en="dónde pisarlo", vol=.45),
]
