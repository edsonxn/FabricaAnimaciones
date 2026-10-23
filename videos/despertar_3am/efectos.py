# -*- coding: utf-8 -*-
"""Capa de EFECTOS del estilo «línea blanca + neón» (docs/estilo_linea_neon.md): el neón amarillo de cada imagen palpita
(FX `neon` en todo el video), palabras clave gigantes en blanco (solo énfasis, no karaoke; fuera del personaje y del neón
que nombran), un rótulo por peldaño de la noche (11 PM · 1 AM · 3 AM · 3:15 AM), tinte azul en el sueño hondo, latido al
despertar y SFX de ElevenLabs propios de este video (reloj, grillos, mar hondo, cuerda de reloj, ronquido, chimenea…).
Descripciones de SFX distintas de las que el canal ya oyó (freno_enojo, agotado_cortisol, estres_cuerpo, nervio_vago,
duelo_cuerpo).
  python fab.py despertar_3am fx --seco | fx | fx hoja
Anclas con palabras de timeline.json (Whisper escribe los números hablados como cifras: «11 de la noche», «los 50»).
"""

CAMARA = {}
FUNDIDO = {}

_P = dict(tam=140, color="blanco", y=.5, pop=.35, sale=.25)
_C = dict(_P, tam=120, y=.11, dur=2.2)          # peldaños de la noche: arriba al centro

ROTULOS = [
    dict(_P, texto="1 DE CADA 3", en="se despertaba de noche", dur=2.6, tam=130, x=.24, y=.14),
    dict(_C, texto="11 PM", en="11 de la noche"),
    dict(_P, texto="SUEÑO PROFUNDO", en="Ahí está el sueño profundo", dur=2.6, tam=110, y=.11),
    dict(_C, texto="1 AM", en="1 de la mañana"),
    dict(_P, texto="CORTISOL", en="la hormona del estrés", dur=2.4, tam=130, x=.24, y=.14),
    dict(_C, texto="3 AM", en="3 de la mañana"),
    dict(_P, texto="DESPERTADOR", en="Es tu despertador interno", dur=2.6, tam=88, x=.18, y=.44),
    dict(_P, texto="INTERNO", en="Es tu despertador interno", dur=2.6, tam=88, x=.18, y=.56),
    dict(_P, texto="+50", en="después de los 50", dur=2.4, tam=220, x=.8, y=.5),
    dict(_P, texto="NADA ESTÁ MAL", en="No es que algo esté mal", dur=2.2, tam=110, y=.88),
    dict(_C, texto="3:15 AM", en="Las 3 y cuarto", x=.22),
    dict(_P, texto="MÁS GRAVE", en="todo parece más grave", dur=2.4, tam=140, x=.78, y=.14),
    dict(_P, texto="ABISMO", en="parece un abismo", dur=2.2, tam=150, x=.74, y=.14),
    dict(_P, texto="PENDIENTE", en="es solo un pendiente", dur=2.4, tam=130, x=.24, y=.86),
    dict(_P, texto="ALCOHOL", en="El alcohol te ayuda", dur=2.4, tam=130, x=.78, y=.14),
    dict(_P, texto="APNEA", en="puede ser apnea", dur=2.6, tam=150, x=.5, y=.11),
    dict(_P, texto="PRIMER SUEÑO", en="el primer sueño", dur=2.0, tam=110, y=.12),
    dict(_P, texto="SEGUNDO SUEÑO", en="el segundo sueño", dur=2.2, tam=110, y=.88),
    dict(_P, texto="1  NO MIRES LA HORA", en="no mires el reloj", dur=2.6, tam=95, x=.3, y=.11),
    dict(_P, texto="2  LEVÁNTATE", en="levántate.", dur=2.4, tam=100, x=.77, y=.12),
    dict(_P, texto="3  LA LISTA", en="vacía la cabeza", dur=2.4, tam=120, x=.76, y=.12),
    dict(_P, texto="NO TE ESTÁS ROMPIENDO", en="no te estás rompiendo", dur=2.8, tam=95, y=.88),
    dict(_P, texto="¿A QUÉ HORA?", en="a qué hora te despiertas", dur=2.8, tam=125, x=.71, y=.86),
]

FX = [
    dict(tipo="abre", en=0, dur=1.0),
    dict(tipo="neon", de=0, a=97.0, fuerza=.9),           # el neón respira todo el video…
    # …menos en el despertador grueso de «3 AM» (scene-011): con .9 el halo lo volvía una mancha (rigor del MASTER, 23-oct)
    dict(tipo="neon", de=97.0, a=99.4, fuerza=.25, radio=4),
    dict(tipo="neon", de=99.4, a=99999, fuerza=.9),
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    # despertar de golpe
    dict(tipo="latido", de="Abres los ojos", a="son las tres|fin", bpm=96, color="negro", fuerza=.20, zoom=.015),
    dict(tipo="destello", en="otra vez son las tres", fuerza=.25, color="amarillo"),
    # el sueño hondo: noche azul
    dict(tipo="tinte", de="11 de la noche", a="ya no regresa igual|fin", color="azul", k=.12, entra=1.0, sale=.8),
    dict(tipo="tinte", de="1 de la mañana", a="no se queda apagada|fin", color="azul", k=.14, entra=.8, sale=.8),
    # 3 AM: el despertador interno
    dict(tipo="destello", en="Es tu despertador interno", fuerza=.28, color="amarillo"),
    dict(tipo="latido", de="Abres los ojos del todo", a="Abres los ojos del todo|fin", bpm=104, color="negro", fuerza=.18, zoom=.012),
    # 3:15: la cabeza
    dict(tipo="temblor", en="parece un abismo", amp=7, dur=.7),
    dict(tipo="vineta", de="parece un abismo", a="parece un abismo|fin", color="negro", fuerza=.6, entra=.6, sale=.8),
    dict(tipo="destello", en="es solo un pendiente", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="puede ser apnea", fuerza=.25, color="amarillo"),
    # las tres cosas
    dict(tipo="destello", en="no mires el reloj", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="levántate.", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="vacía la cabeza", fuerza=.22, color="amarillo"),
    # cierre al amanecer
    dict(tipo="destello", en="no te estás rompiendo", fuerza=.28, color="amarillo"),
    dict(tipo="zoom", de="para volver a dormir#2", a="para volver a dormir#2|fin", cuanto=.10, entra=1.5, sale=.5),
    dict(tipo="cierra", en=("para volver a dormir#2|fin", 1.2), dur=1.6),
]

SFX = {
    "reloj_cama": ("Small wind-up alarm clock ticking loudly on a wooden nightstand in a silent bedroom", 4),
    "ojos": ("Soft sharp intake of breath and bed sheets rustling as someone wakes suddenly in the dark", 2),
    "grillos": ("Crickets chirping outside an open window on a warm quiet night, very calm", 5),
    "gato": ("Cat purring softly while asleep, close and gentle", 3),
    "peldano": ("Soft low felt-piano note with a shimmering glassy tail, gentle chapter marker", 2),
    "lampara": ("Small bedside lamp switched off with a soft plastic click", 1),
    "mar_hondo": ("Slow deep ocean swell heard from underwater, muffled low rumble and soft bubbles", 5),
    "arroyo": ("Gentle stream of water trickling over smooth stones, close and calm", 4),
    "arena": ("Fine sand pouring slowly through an hourglass, soft continuous hiss", 3),
    "laboratorio": ("Old hospital ward at night, faint electric hum, soft footsteps and a clipboard page turning", 4),
    "cuerda": ("Old clock being wound by hand, ratcheting brass spring clicks speeding up", 3),
    "almohada": ("Pillow being turned over and fluffed, soft fabric rustle and a sleepy sigh", 2),
    "trueno": ("Distant soft thunder rolling far away at night, no rain", 4),
    "papeles": ("Envelopes and paper bills shuffled nervously on a wooden table", 2),
    "canon": ("Cold wind blowing across a deep empty canyon at night, hollow and lonely", 4),
    "cafe_manana": ("Morning kitchen, coffee poured into a ceramic cup, birds chirping outside", 3),
    "copa": ("Wine poured into a glass, then the glass set down gently on wood", 3),
    "abanico": ("Hand fan flapping quickly in a quiet room at night", 2),
    "pasillo": ("Slippers shuffling down a wooden hallway at night, a door creaking softly", 3),
    "ronquido": ("Older man snoring loudly and then catching his breath with a short gasp, comic but gentle", 3),
    "pueblo_viejo": ("Medieval village at night, wind through wooden shutters, a distant owl", 4),
    "chimenea": ("Log placed on a crackling fireplace, embers popping softly", 3),
    "susurros": ("Two people whispering softly in bed by candlelight, words not understandable", 3),
    "pantuflas": ("Feet sliding into slippers on a wooden floor, then a few quiet steps", 2),
    "pagina": ("Book page turned slowly in a quiet room, a cup of tea set on a saucer", 2),
    "lapiz": ("Pencil writing quickly on paper in a notebook, a short list being scribbled", 3),
    "amanecer": ("Early dawn over a small town: a distant rooster, first birds and a soft breeze", 5),
}

PISTAS = [
    dict(sfx="reloj_cama", en=0.2, vol=.30),
    dict(sfx="ojos", en="Abres los ojos", vol=.35),
    dict(sfx="grillos", en="No hay ruido", vol=.25),
    dict(sfx="gato", en="nadie te habló", vol=.22),
    dict(sfx="peldano", en="11 de la noche", vol=.40),
    dict(sfx="lampara", en="Te acuestas", vol=.45),
    dict(sfx="mar_hondo", en="como olas que suben", vol=.28),
    dict(sfx="arroyo", en="limpia el cerebro", vol=.25),
    dict(sfx="arena", en="se gasta en las primeras", vol=.30),
    dict(sfx="peldano", en="1 de la mañana", vol=.40),
    dict(sfx="laboratorio", en="la midieron", vol=.25),
    dict(sfx="peldano", en="3 de la mañana", vol=.40),
    dict(sfx="cuerda", en="Es tu despertador interno", vol=.35),
    dict(sfx="almohada", en="Te acomodas la almohada", vol=.40),
    dict(sfx="reloj_cama", en="Abres los ojos del todo", vol=.28),
    dict(sfx="peldano", en="Las 3 y cuarto", vol=.40),
    dict(sfx="trueno", en="empieza lo peor", vol=.28),
    dict(sfx="papeles", en="Las deudas", vol=.35),
    dict(sfx="canon", en="parece un abismo", vol=.30),
    dict(sfx="cafe_manana", en="con luz", vol=.25),
    dict(sfx="copa", en="La copa de la noche", vol=.35),
    dict(sfx="abanico", en="Los bochornos", vol=.35),
    dict(sfx="pasillo", en="Y la vejiga", vol=.30),
    dict(sfx="ronquido", en="Y si roncas fuerte", vol=.30),
    dict(sfx="pueblo_viejo", en="de hace siglos", vol=.25),
    dict(sfx="susurros", en="platicaban con su pareja", vol=.25),
    dict(sfx="chimenea", en="cuidaban el fuego", vol=.30),
    dict(sfx="pantuflas", en="levántate.", vol=.35),
    dict(sfx="pagina", en="haz algo tranquilo", vol=.30),
    dict(sfx="lapiz", en="escribieron 5 minutos", vol=.35),
    dict(sfx="amanecer", en="no te estás rompiendo", vol=.25),
]
