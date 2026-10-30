# -*- coding: utf-8 -*-
"""Efectos del piloto v3: rótulos (solo énfasis, en el piso), golpes y SFX. La cámara y las transiciones van en toma.py (nucleo/montaje_real.py); aquí nada de `zoom`. Formato: nucleo/secuencia_fx.py."""
import json
import os

_tl = json.load(open("timeline.json", encoding="utf-8"))
FIN = max(w["e"] for e in _tl["escenas"] for f in e["frases"] if f["key"] == "junta_7" for w in f["words"])   # donde se corta la voz: «…ciento ochenta mil to-»

_P = dict(tam=140, color="blanco", y=.885, pop=.35, sale=.25)
_C = dict(_P, tam=96)                                            # el nombre de lo que se ve
_F = dict(_C, color="amarillo")                                  # las fechas de la trayectoria

ROTULOS = [
    dict(_P, texto="51 358 COSAS", en="cincuenta y un mil", dur=3.0, color="amarillo", tam=150),
    dict(_P, texto="1 300 MAL", en="Mil trescientas me salieron", dur=2.4, color="rosa", tam=150),
    dict(_P, texto="TOKEN · LA IA", en="Soy Token", dur=2.6, color="amarillo"),
    dict(_F, texto="GRABACIÓN REAL", en="grabaciones de verdad", dur=2.6),
    dict(_F, texto="2017 · UNITY", en="En dos mil diecisiete", dur=3.2),
    dict(_F, texto="2018 · PLAY STORE", en="Un año después", dur=3.6),
    dict(_F, texto="2021 · 79 000 VISTAS", en="El avance de un juego", dur=3.2),
    dict(_F, texto="ENERO 2023 · VR", en="En enero de dos mil", dur=3.2),
    dict(_F, texto="FEBRERO 2023 · 32 MIN", en="Y en febrero subió", dur=3.6),
    dict(_P, texto="325 PERSONAS", en="Lo vieron", dur=2.4, color="rosa", tam=150),
    dict(_C, texto="PANEL", en="Este es el panel", dur=2.6),
    dict(_C, texto="LA ALDEA", en="Esta es una aldea", dur=2.6),
    dict(_C, texto="FÁBRICA 3D", en="Esta es una fábrica", dur=2.2),
    dict(_C, texto="APP DEL TELÉFONO", en="Esta es una aplicación", dur=2.6),
    dict(_C, texto="VIDEO ANIMADO", en="Y esto, un video animado", dur=2.8),
    dict(_P, texto="4 PALABRAS", en="Cuatro palabras", dur=2.0, color="amarillo", tam=150),
    dict(_C, texto="1 · PLAN", en="Primero, un plan", dur=2.4),
    dict(_C, texto="2 · LEER LO QUE EXISTE", en="Luego leo lo que ya existe", dur=2.6),
    dict(_C, texto="3 · CÓDIGO", en="Escribo el código", dur=2.4),
    dict(_C, texto="4 · PROBAR Y MIRAR", en="Lo pruebo, y miro", dur=2.8),
    dict(_F, texto="EL CÓDIGO DE TOKEN", en="este código me dibuja a mí", dur=2.8),
    dict(_P, texto="CASI 50 A 1", en="yo hago casi cincuenta", dur=3.0, color="amarillo", tam=170),
    dict(_P, texto="SABER QUÉ PEDIR", en="Hizo falta saber qué pedir", dur=3.0, color="amarillo", tam=150),
    dict(_P, texto="VERSIÓN 2", en="esta es la versión dos", dur=2.2, tam=150),
    dict(_P, texto="4 975 EN UN DÍA", en="cuatro mil novecientas", dur=3.2, color="amarillo"),
    dict(_P, texto="180 000 TOKENS", en="a los ciento ochenta mil tokens", dur=3.0, color="rosa", tam=150),
    dict(_P, texto="−40 %", en="cerca de cuarenta", dur=2.6, color="amarillo", tam=170),
    dict(_F, texto="PASÓ DE VERDAD", en="Y eso pasó haciendo este video", dur=3.0),
    dict(_P, texto="JUNTA DIRECTIVA", en="la junta directiva", dur=3.0, color="amarillo", tam=150),
    dict(_F, texto="TÚ DECIDES QUÉ SIGUE", en="Escribe en los comentarios", dur=4.0),
    dict(_P, texto="SESIÓN NUEVA…", en=FIN + .35, dur=2.3, color="amarillo", tam=130, y=.5),
]

FX = [
    dict(tipo="abre", en=0, dur=.4),
    dict(tipo="temblor", en="Mil trescientas me salieron", amp=26),
    dict(tipo="destello", en="Mil trescientas me salieron", color="rosa", fuerza=.35),
    dict(tipo="temblor", en="las llaves", amp=30),
    dict(tipo="temblor", en="empezó a morirse", amp=30),
    dict(tipo="oscurecer", de="desconectó", a="conectar", k=1, entra=.03, sale=.03),   # el apagón del desconectar: se va la imagen de verdad
    dict(tipo="temblor", en="me cortan", amp=22),
    dict(tipo="oscurecer", de=FIN, a=FIN + 3.2, k=1, entra=.01, sale=0),
]

SFX = {
    "fallo": ("Short digital error buzz, comic robot failure beep, dry", 1),
    "disco": ("Failing hard drive clicking and grinding, mechanical ticking, close up", 3),
    "logro": ("Cheerful retro video game achievement chime, bright", 2),
    "golpe": ("Soft cartoon metallic clank of a small robot, dry", 1),
    "corte": ("Electronic power down, a small robot shutting off abruptly with a descending blip", 1),
    "encendido": ("Retro computer power on: relay click, rising hum and a soft start-up beep", 2),
    "llaves": ("Heavy ring of metal keys falling and bonking a small metal robot on the head, cartoon clonk, keys jingling as they bounce on the floor", 1),
    "latigo": ("Fast whip pan whoosh, airy and short, no reverb", 1),
    "latigo2": ("Quick cloth swish whoosh passing the camera, dry and snappy", 1),
    "zum": ("Quick zoom-in whoosh rising in pitch, short digital swell", 1),
    "zum2": ("Short reversed swoosh rushing into a soft thump, digital", 1),
    "desliza": ("Soft quick swipe of a screen sliding up, short and clean", 1),
    "desliza2": ("Light paper-like slide with a tiny click at the end, short", 1),
    "tic": ("Short digital data glitch burst, tiny stutter, dry", 1),
    "jefe": ("Small cartoon pop as a paper cutout character jumps into frame, short and dry", 1),
}

PISTAS = [
    dict(sfx="fallo", en="Mil trescientas me salieron", vol=.5),
    dict(sfx="llaves", en="las llaves", vol=.7),
    dict(sfx="golpe", en="Primero, un plan", vol=.3),
    dict(sfx="golpe", en="Luego leo lo que ya existe", vol=.3),
    dict(sfx="golpe", en="Escribo el código", vol=.3),
    dict(sfx="golpe", en="Lo pruebo, y miro", vol=.3),
    dict(sfx="fallo", en="Casi siempre", vol=.4),
    dict(sfx="disco", en="empezó a morirse", vol=.5),
    dict(sfx="corte", en="desconectó", vol=.6),
    dict(sfx="encendido", en="conectar", vol=.55),
    dict(sfx="fallo", en="me cortan", vol=.45),
    dict(sfx="logro", en="la junta directiva", vol=.35),
    dict(sfx="fallo", en="cabe en el disco", vol=.35),
    dict(sfx="corte", en=FIN - .05, vol=.7),
]

# cada transición y cada entrada del Jefe suenan: toma.py deja sus segundos en medios/golpes.json
_SON = dict(latigo=(("latigo", "latigo2"), .32), zoom=(("zum", "zum2"), .3), deslizar=(("desliza", "desliza2"), .3), glitch=(("tic",), .34), destello=(("zum2",), .22), jefe=(("jefe",), .4))
if os.path.exists("medios/golpes.json"):
    for i, (tipo, t) in enumerate(json.load(open("medios/golpes.json", encoding="utf-8"))):
        if tipo in _SON:
            nombres, vol = _SON[tipo]
            PISTAS.append(dict(sfx=nombres[i % len(nombres)], en=round(max(0, t - .12), 3), vol=vol))
