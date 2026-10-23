# -*- coding: utf-8 -*-
"""Capa de EFECTOS del estilo «línea blanca + neón» (docs/estilo_linea_neon.md): el neón amarillo de cada imagen palpita
(FX `neon` en todo el video), palabras clave gigantes en blanco (solo énfasis, no karaoke; fuera del personaje y del neón
que nombran), un rótulo por peldaño de la escalera de tiempo (MINUTOS · 24 HORAS · SEMANAS · MESES · 1 AÑO), latido en la
noticia y SFX de ElevenLabs propios de este video (teléfono, puerto japonés, ambulancia, mercado, engranes, ofrenda).
Descripciones de SFX distintas de las que el canal ya oyó (freno_enojo, agotado_cortisol, estres_cuerpo, nervio_vago).
  python fab.py duelo_cuerpo fx --seco | fx | fx hoja
Anclas con palabras de timeline.json (Whisper escribe los números hablados como cifras: no anclar en ellos).
"""

CAMARA = {}
FUNDIDO = {}

_P = dict(tam=140, color="blanco", y=.5, pop=.35, sale=.25)
_C = dict(_P, tam=120, y=.11, dur=2.2)          # peldaños de la escalera de tiempo: arriba al centro

ROTULOS = [
    dict(_P, texto="CORAZÓN ROTO", en="Por qué el corazón roto", dur=2.4, tam=120, y=.12),
    dict(_C, texto="MINUTOS", en="Los primeros minutos", x=.22, y=.14),
    dict(_P, texto="ADRENALINA", en="suelta adrenalina", dur=2.4, tam=110, x=.22, y=.14),
    dict(_P, texto="CORTISOL", en="y cortisol", dur=2.2, tam=110, x=.78, y=.14),
    dict(_P, texto="DOLOR", en="no es una forma de hablar", dur=2.4, tam=150, x=.78, y=.43),
    dict(_P, texto="REAL", en="no es una forma de hablar", dur=2.4, tam=150, x=.78, y=.57),
    dict(_C, texto="24 HORAS", en="Las primeras"),
    dict(_P, texto="×21", en="se multiplicaba", dur=2.6, tam=220, x=.2, y=.5),
    dict(_P, texto="TAKOTSUBO", en="lo llamaron takotsubo", dur=2.6, tam=120, y=.12),
    dict(_P, texto="9 DE 10", en="le pasa a mujeres", dur=2.4, tam=150, y=.14),
    dict(_P, texto="URGENCIAS", en="es a urgencias", dur=2.4, tam=130, y=.88),
    dict(_C, texto="SEMANAS", en="Las primeras#2"),
    dict(_P, texto="NIEBLA", en="la niebla del duelo", dur=2.4, tam=150, x=.8, y=.16),
    dict(_P, texto="DEFENSAS", en="tus defensas bajan", dur=2.2, tam=120, x=.22, y=.14),
    dict(_C, texto="MESES", en="Los primeros#2"),
    dict(_P, texto="NO ES LOCURA", en="No te estás volviendo loco", dur=2.2, tam=110, x=.3, y=.88),
    dict(_P, texto="EL MAPA", en="lo explica con un mapa", dur=2.4, tam=140, y=.12),
    dict(_C, texto="1 AÑO", en="El primer año"),
    dict(_P, texto="EN OLAS", en="Llega en olas", dur=2.2, tam=140, x=.78, y=.14),
    dict(_P, texto="DUELO", en="duelo prolongado", dur=2.6, tam=110, x=.3, y=.4),
    dict(_P, texto="PROLONGADO", en="duelo prolongado", dur=2.6, tam=110, x=.3, y=.53),
    dict(_P, texto="1  A SALVO", en="dale a tu cuerpo señales", dur=2.4, tam=120, x=.24, y=.14),
    dict(_P, texto="2  NO SOLO", en="no lo cargues solo", dur=2.4, tam=120, x=.82, y=.09),
    dict(_P, texto="3  TU PECHO", en="escucha a tu pecho", dur=2.4, tam=120, x=.24, y=.14),
    dict(_P, texto="OFRENDA", en="ponemos una ofrenda", dur=2.4, tam=140, y=.1),
    dict(_P, texto="LO QUE AMASTE", en="del tamaño de lo que amaste", dur=3.0, tam=120, x=.3, y=.88),
]

FX = [
    dict(tipo="abre", en=0, dur=1.0),
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    # la noticia: latido negro
    dict(tipo="latido", de="algo se te cae por dentro", a="el aire no alcanza|fin", bpm=118, color="negro", fuerza=.22, zoom=.02),
    dict(tipo="destello", en="Por qué el corazón roto", fuerza=.25, color="amarillo"),
    # la alarma del cuerpo
    dict(tipo="latido", de="El corazón se acelera", a="los músculos se tensan|fin", bpm=110, color="negro", fuerza=.18, zoom=.015),
    dict(tipo="destello", en="se multiplicaba", fuerza=.30, color="amarillo"),
    dict(tipo="temblor", en="Ante una noticia terrible", amp=8, dur=.8),
    dict(tipo="vineta", de="Se siente igual que un infarto", a="falta de aire|fin", color="negro", fuerza=.6, entra=1.0, sale=.8),
    # semanas: la noche y la niebla
    dict(tipo="tinte", de="Las primeras#2", a="no puedes levantarte|fin", color="azul", k=.12, entra=.8, sale=.8),
    dict(tipo="tinte", de="la niebla del duelo", a="la niebla del duelo|fin", color="azul", k=.10, entra=.6, sale=.8),
    # meses: el mapa que se atora
    dict(tipo="temblor", en="ese mapa se atora", amp=7, dur=.7),
    dict(tipo="destello", en="encendía el circuito", fuerza=.25, color="amarillo"),
    # las tres cosas
    dict(tipo="destello", en="dale a tu cuerpo señales", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="no lo cargues solo", fuerza=.22, color="amarillo"),
    dict(tipo="destello", en="escucha a tu pecho", fuerza=.22, color="amarillo"),
    # cierre en la ofrenda
    dict(tipo="destello", en="del tamaño de lo que amaste", fuerza=.28, color="amarillo"),
    dict(tipo="zoom", de="un lugar para ellos", a="un lugar para ellos|fin", cuanto=.10, entra=1.5, sale=.5),
    dict(tipo="cierra", en=("un lugar para ellos|fin", 1.2), dur=1.6),
]

SFX = {
    "telefono": ("Old landline telephone ringing twice in a quiet kitchen at night, then the receiver lifted with a click", 4),
    "neon_tubo": ("Old neon sign flickering on with a soft electric tick and a warm low buzz", 3),
    "latido_susto": ("Heartbeat suddenly speeding up, deep muffled chest thumps getting faster and louder", 5),
    "titulo": ("Deep soft low piano boom with a breathy rising swell, gentle, for a chapter title", 2),
    "ola": ("Big ocean wave rising and crashing on rocks, deep roar and foam hiss", 4),
    "puerto": ("Small fishing harbor at dawn, water lapping on wooden boats, creaking ropes, distant gulls", 5),
    "ambulancia": ("Ambulance siren passing quickly down a town street at night, doppler fade", 4),
    "noche": ("Quiet bedroom at night, soft wall clock ticking, a distant dog barking once", 4),
    "niebla": ("Soft airy wind drifting through thick fog, muffled distant town sounds", 4),
    "mercado": ("Busy Mexican street market crowd murmur, vendors calling softly, footsteps on stone", 4),
    "platos": ("Two ceramic plates set gently on a wooden table with a soft cutlery clink", 2),
    "engranes": ("Old iron gears grinding slowly and jamming with a heavy metallic clunk", 3),
    "faro": ("Lighthouse at night, slow sea swell and wind, a low foghorn far away", 4),
    "risas_mesa": ("Older women laughing warmly together around a kitchen table, coffee cups clinking", 3),
    "sopa": ("Spoon stirring a bowl of hot soup on a table, soft clink, quiet kitchen", 2),
    "parque": ("Sunny morning park with birds singing and a small fountain splashing", 4),
    "velas": ("A match struck and candles lit one after another, soft crackle of flames in a quiet room", 3),
    "campana": ("Single soft distant church bell toll at dusk, long gentle decay", 4),
}

PISTAS = [
    dict(sfx="telefono", en=0.3, vol=.35),
    dict(sfx="neon_tubo", en="algo se te cae por dentro", vol=.30),
    dict(sfx="latido_susto", de="algo se te cae por dentro", a="el aire no alcanza|fin", vol=.22),
    dict(sfx="titulo", en="Los primeros minutos", vol=.40),
    dict(sfx="latido_susto", en="El corazón se acelera", vol=.20),
    dict(sfx="titulo", en="Las primeras", vol=.40),
    dict(sfx="ola", en="la oleada de adrenalina", vol=.30),
    dict(sfx="puerto", en="En Japón", vol=.28),
    dict(sfx="ambulancia", en="es a urgencias", vol=.25),
    dict(sfx="titulo", en="Las primeras#2", vol=.40),
    dict(sfx="noche", en="el sueño se rompe", vol=.30),
    dict(sfx="niebla", en="la niebla del duelo", vol=.28),
    dict(sfx="titulo", en="Los primeros#2", vol=.40),
    dict(sfx="mercado", en="oyes una voz parecida", vol=.25),
    dict(sfx="platos", en="Pones dos platos", vol=.40),
    dict(sfx="engranes", en="ese mapa se atora", vol=.30),
    dict(sfx="faro", en="seguía buscando a esa persona", vol=.25),
    dict(sfx="titulo", en="El primer año", vol=.40),
    dict(sfx="risas_mesa", en="a reírse sin culpa", vol=.25),
    dict(sfx="sopa", en="Come algo caliente", vol=.35),
    dict(sfx="parque", en="Sal a caminar", vol=.25),
    dict(sfx="ambulancia", en="Ve a urgencias", vol=.20),
    dict(sfx="velas", en="ponemos una ofrenda", vol=.35),
    dict(sfx="campana", en="un lugar para ellos", vol=.35),
]
