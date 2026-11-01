# -*- coding: utf-8 -*-
"""Capa de EFECTOS del estilo «línea blanca + neón» (docs/estilo_linea_neon.md): el neón amarillo de cada imagen palpita
(FX `neon` en todo el video), palabras clave gigantes en blanco al centro (solo énfasis, no karaoke), golpe de cámara en la
alarma y SFX de ElevenLabs propios de este video (camión, alarma, respiración, tripas, agua fría, abrazo).
  python fab.py estres_cuerpo fx --seco | fx | fx hoja
Anclas con palabras de timeline.json (Whisper escribe los números hablados como cifras: no anclar en ellos; los cinco
«Lugar número …» se distinguen con #1..#5).
"""

CAMARA = {}
FUNDIDO = {}

_P = dict(tam=140, color="blanco", y=.5, pop=.35, sale=.25)

ROTULOS = [
    dict(_P, texto="AMÍGDALA", en="la amígdala", dur=2.0),
    dict(_P, texto="ADRENALINA", en="sueltan adrenalina", dur=2.0),
    dict(_P, texto="CORTISOL", en="llega la segunda ola", dur=2.2, tam=160),
    # rigor 20-oct: los rótulos que tapaban la cara o el neón que presentan van al hueco vacío de su imagen (x/y)
    dict(_P, texto="NERVIO", en="hasta la panza", dur=2.2, tam=130, x=.2, y=.43),
    dict(_P, texto="VAGO", en="hasta la panza", dur=2.2, tam=130, x=.2, y=.57),
    dict(_P, texto="ERRANTE", en="significa errante", dur=1.8),
    dict(_P, texto="DESCANSA Y DIGIERE", en="Descansa y digiere", dur=2.0, tam=110),
    dict(_P, texto="1  EL PECHO", en="Lugar número#1", dur=2.2, tam=120, x=.22),
    dict(_P, texto="CO2", en="sacas demasiado", dur=2.0, tam=170),
    dict(_P, texto="URGENCIAS", en="Es para urgencias", dur=2.0),
    dict(_P, texto="EL FRENO", en="pisa el freno", dur=1.8, tam=130, x=.2, y=.17),
    dict(_P, texto="SUSPIRO", en="el suspiro fisiológico", dur=2.4, tam=100, x=.18, y=.24),
    dict(_P, texto="FISIOLÓGICO", en="el suspiro fisiológico", dur=2.4, tam=100, x=.18, y=.36),
    dict(_P, texto="5 MIN AL DÍA", en="minutos al día, por un mes", dur=2.0),
    dict(_P, texto="2  LA PANZA", en="Lugar número#2", dur=2.2, tam=110, x=.2),
    dict(_P, texto="500 MILLONES", en="millones de neuronas", dur=2.2, tam=150),
    dict(_P, texto="SEGUNDO CEREBRO", en="el segundo cerebro", dur=2.0, tam=120),
    dict(_P, texto="SEROTONINA", en="parte de la serotonina", dur=2.0),
    dict(_P, texto="8 DE 10", en="fibras de ese nervio", dur=2.2, tam=170),
    dict(_P, texto="MARIPOSAS", en="Las famosas mariposas", dur=2.0),
    dict(_P, texto="4 · 6", en="Inhala contando hasta", dur=2.4, tam=180),
    dict(_P, texto="3  QUIJADA", en="Lugar número#3", dur=2.2, tam=110, x=.21),
    dict(_P, texto="PELEAR O HUIR", en="para pelear o huir", dur=2.0, tam=120),
    dict(_P, texto="TENSIONAL", en="el de tipo tensional", dur=2.0),
    dict(_P, texto="TENSA", en="tensa para soltar", dur=2.2, tam=110, x=.17, y=.43),
    dict(_P, texto="Y SUELTA", en="tensa para soltar", dur=2.2, tam=110, x=.17, y=.57),
    dict(_P, texto="DIENTES SEPARADOS", en="labios juntos, dientes separados", dur=2.4, tam=110),
    dict(_P, texto="27 ESTUDIOS", en="Un análisis de", dur=2.0),
    dict(_P, texto="4  FUERA", en="Lugar número#4", dur=2.4, tam=110, x=.22, y=.43),
    dict(_P, texto="DEL CUERPO", en="Lugar número#4", dur=2.4, tam=110, x=.22, y=.57),
    dict(_P, texto="DESPERSONALIZACIÓN", en="Se llama despersonalización", dur=2.6, tam=100),
    dict(_P, texto="FUSIBLE", en="Funciona como un fusible", dur=2.0, tam=160),
    dict(_P, texto="AGUA FRÍA", en="agua fría en la cara", dur=2.2, tam=160),
    dict(_P, texto="REFLEJO DE INMERSIÓN", en="Es el reflejo de inmersión", dur=2.4, tam=100),
    dict(_P, texto="5 · 4 · 3 · 2 · 1", en="ancla tus sentidos", dur=2.6, tam=130),
    dict(_P, texto="5  DEFENSAS", en="Lugar número#5", dur=2.2, tam=100, x=.46, y=.09),
    dict(_P, texto="394", en="Reunieron a", dur=2.0, tam=180),
    dict(_P, texto="+9 DÍAS", en="la misma herida les", dur=2.2, tam=170),
    dict(_P, texto="ABRAZOS", en="En serio", dur=2.2, tam=160),
    dict(_P, texto="404", en="llamó a", dur=2.0, tam=180),
    dict(_P, texto="5 FRENOS", en="Recapitulemos", dur=2.4, tam=140, x=.22),
    dict(_P, texto="EL FRENO", en="dónde está el freno", dur=3.0, tam=140, x=.73, y=.86),
]

FX = [
    dict(tipo="abre", en=0, dur=1.0),
    dict(tipo="neon", de=0, a=99999, fuerza=.9),                      # el neón respira todo el video
    dict(tipo="vineta", de=0, a=99999, color="negro", fuerza=.35),
    # la alarma: latido negro y golpe de cámara
    dict(tipo="temblor", en="Dispara igual", amp=20),
    dict(tipo="latido", de="En segundos", a="la alarma encendida|fin", bpm=104, color="negro", fuerza=.22, zoom=.02),
    # los cinco lugares
    dict(tipo="destello", en="Lugar número#1", fuerza=.25, color="amarillo"),
    dict(tipo="latido", de="Y aquí viene la trampa", a="se alimenta solo|fin", bpm=112, color="negro", fuerza=.18, zoom=.015),
    dict(tipo="destello", en="Lugar número#2", fuerza=.25, color="amarillo"),
    dict(tipo="destello", en="Lugar número#3", fuerza=.25, color="amarillo"),
    dict(tipo="temblor", en="Aprieta los puños", amp=10, dur=1.0),
    dict(tipo="destello", en="Lugar número#4", fuerza=.25, color="amarillo"),
    dict(tipo="vineta", de="parecen de otra persona", a="se siente como estar lejos|fin", color="negro", fuerza=.6, entra=1.0, sale=.8),
    dict(tipo="tinte", de="Llena un recipiente", a="a tu piel|fin", color="azul", k=.15, entra=.8, sale=.8),
    dict(tipo="destello", en="Lugar número#5", fuerza=.25, color="amarillo"),
    dict(tipo="destello", en="Recapitulemos", fuerza=.20, color="amarillo"),
    dict(tipo="zoom", de="dónde está el freno", a="dónde está el freno|fin", cuanto=.10, entra=1.5, sale=.5),
    dict(tipo="cierra", en=("dónde está el freno|fin", 1.2), dur=1.6),
]

SFX = {
    "neon": ("Electric neon tube buzzing and flickering on, short crackle then steady low hum", 3),
    "camion": ("Crowded city bus interior ambience, diesel engine rumble, air brakes hiss, muffled chatter", 6),
    "estornudo": ("A single human sneeze, close, slightly comedic", 1),
    "alarma": ("Old mechanical fire alarm bell ringing, sharp short burst", 3),
    "rugido": ("Big lion roar in the distance, cinematic", 2),
    "correo": ("Single soft email notification ping", 1),
    "latido": ("Fast heartbeat thumping, close and muffled, tense", 5),
    "jadeo": ("Fast shallow anxious breathing through the mouth, close", 4),
    "suspiro": ("Two quick sniffs of air through the nose followed by one long slow relieved exhale through the mouth", 4),
    "tripas": ("Stomach gurgling and rumbling, close, slightly comedic", 3),
    "mariposas": ("Soft fluttering of butterfly wings, light and magical", 2),
    "punos": ("Leather creaking as fists clench tight, tension", 2),
    "suelta": ("Soft airy whoosh of release, like air leaving a cushion", 2),
    "vidrio": ("Muffled distant city sounds as if heard through thick glass or underwater, dreamy", 5),
    "fusible": ("Electric fuse popping with a spark and a short buzz", 2),
    "agua": ("Splash of cold water in a bowl with ice cubes clinking", 3),
    "delfin": ("Underwater bubbles with soft dolphin clicks, deep and calm", 3),
    "gota": ("Single water drop falling from a glass dropper, clean plink", 1),
    "abrazo": ("Warm soft clothing rustle of a hug with a gentle happy sigh", 2),
    "golpe": ("Soft deep cinematic hit with a subtle airy whoosh, for a title word appearing", 2),
    "campana": ("Soft warm singing bowl chime, calm, gentle long resonance", 4),
}

PISTAS = [
    dict(sfx="neon", en=0.4, vol=.40),
    dict(sfx="camion", de=0.5, a="sientes el pecho apretado|fin", vol=.22),
    dict(sfx="estornudo", en="te enfermas", vol=.45),
    dict(sfx="alarma", en="la amígdala", vol=.30),
    dict(sfx="rugido", en="un león", vol=.35),
    dict(sfx="correo", en="un correo de tu jefe", vol=.40),
    dict(sfx="latido", de="En segundos", a="la alarma encendida|fin", vol=.20),
    dict(sfx="golpe", en="Lugar número#1", vol=.45),
    dict(sfx="jadeo", de="respiras rápido y alto", a="como si fueras a correr|fin", vol=.25),
    dict(sfx="suspiro", en="Ahora sácalo lento", vol=.45),
    dict(sfx="golpe", en="Lugar número#2", vol=.45),
    dict(sfx="tripas", en="la comida como piedra", vol=.40),
    dict(sfx="mariposas", en="Las famosas mariposas", vol=.35),
    dict(sfx="golpe", en="Lugar número#3", vol=.45),
    dict(sfx="punos", en="Aprieta los puños", vol=.40),
    dict(sfx="suelta", en="Y suelta de golpe", vol=.40),
    dict(sfx="suelta", en="déjalos caer", vol=.35),
    dict(sfx="golpe", en="Lugar número#4", vol=.45),
    dict(sfx="vidrio", de="El mundo se ve plano", a="como una película|fin", vol=.25),
    dict(sfx="fusible", en="Funciona como un fusible", vol=.40),
    dict(sfx="agua", en="Llena un recipiente", vol=.40),
    dict(sfx="delfin", en="los delfines y las focas", vol=.30),
    dict(sfx="golpe", en="Lugar número#5", vol=.45),
    dict(sfx="gota", en="gotas con virus", vol=.45),
    dict(sfx="estornudo", en="resfriado de vacaciones", vol=.40),
    dict(sfx="abrazo", en="En serio", vol=.40),
    dict(sfx="gota", en="otra vez, gotas", vol=.40),
    dict(sfx="abrazo", en="Un abrazo largo", vol=.35),
    dict(sfx="golpe", en="Recapitulemos", vol=.45),
    dict(sfx="camion", de=("Un martes cualquiera#2", -.3), a="sientes el pecho apretado#2|fin", vol=.18),
    dict(sfx="suspiro", en="lo sueltas despacio", vol=.40),
    dict(sfx="campana", en="dónde está el freno", vol=.45),
]
