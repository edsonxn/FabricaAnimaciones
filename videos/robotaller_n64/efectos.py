# -*- coding: utf-8 -*-
"""Efectos de robotaller_n64: rótulos (solo énfasis, en el piso), golpes y SFX. La cámara y las transiciones van en toma.py (nucleo/montaje_real.py).
Copiado del piloto (videos/robotaller_mes1/efectos.py) y reanclado. SFX con prompts y nombres NUEVOS: ninguno repite un archivo del piloto.
Formato: nucleo/secuencia_fx.py."""
import json
import os

_tl = json.load(open("timeline.json", encoding="utf-8"))
_W = {f["key"]: f["words"] for e in _tl["escenas"] for f in e["frases"]}
ESCUCHA = _W["sonido_2"][-1]["e"] + .08          # justo al acabar «Escucha.»: suena la OST de verdad, con la voz callada (post 2,6 s)

_P = dict(tam=140, color="blanco", y=.885, pop=.35, sale=.25)
_C = dict(_P, tam=96)                             # el nombre de lo que se ve
_F = dict(_C, color="amarillo")
_N = dict(_P, tam=150, color="amarillo")          # cifras
_R = dict(_P, tam=150, color="rosa")              # cifras de fallos

ROTULOS = [
    dict(_N, texto="9 PALABRAS", en="nueve palabras", dur=2.3),
    dict(_N, texto="4 HORAS", en="Cuatro horas", dur=2.0),
    dict(_N, texto="24:19", en="veinticuatro minutos", dur=1.9, tam=170),
    dict(_C, texto="170 CLIPS", en="ciento setenta clips", dur=1.6),
    dict(_C, texto="36 CANCIONES DE N64", en="treinta y seis canciones", dur=2.2),
    dict(_N, texto="1 106 ACCIONES", en="mil ciento seis acciones", dur=2.4),
    dict(_F, texto="GRABACIÓN REAL", en="lo demás es real", dur=2.2),
    dict(_C, texto="1 · INVESTIGAR", en="Paso uno", dur=2.4),
    dict(_N, texto="68 BÚSQUEDAS", en="sesenta y ocho", dur=2.4),
    dict(_F, texto="LA FUENTE DE CADA DATO", en="la fuente de cada dato", dur=2.4),
    dict(_C, texto="2 · GUION", en="Paso dos", dur=2.2),
    dict(_N, texto="30 → 1", en="del treinta al uno", dur=2.0, tam=170),
    dict(_C, texto="3 · VOZ", en="Paso tres", dur=2.2),
    dict(_R, texto="8 RECHAZADAS", en="Ocho frases", dur=2.2),
    dict(_R, texto="3 REESCRITAS", en="cambié el guion", dur=2.2),
    dict(_C, texto="4 · IMÁGENES", en="Paso cuatro", dur=2.4),
    dict(_R, texto="36 REHECHOS", en="treinta y seis los tuve", dur=2.2),
    dict(_N, texto="VOZ = IMAGEN", en="La regla es una", dur=3.0),
    dict(_C, texto="90 PEGATINAS", en="Noventa imágenes reales", dur=2.4),
    dict(_C, texto="MAPAS REALES", en="Mapas de verdad", dur=2.2),
    dict(_C, texto="18 ANIMACIONES NUEVAS", en="dieciocho animaciones", dur=2.6),
    dict(_N, texto="220 EFECTOS", en="Doscientos veinte efectos", dur=2.4),
    dict(_C, texto="5 · SONIDO", en="Paso cinco", dur=2.2),
    dict(_N, texto="36 PISTAS ORIGINALES", en="Treinta y seis pistas originales", dur=1.8, tam=120),
    dict(_F, texto="♪ MARIO KART 64 · YOSHI VALLEY", en=ESCUCHA, dur=3.3),
    dict(_R, texto="180 000 TOKENS", en="ciento ochenta mil tokens", dur=2.6),
    dict(_N, texto="6 SESIONES", en="Seis sesiones", dur=1.9),
    dict(_N, texto="5 AYUDANTES", en="cinco ayudantes", dur=1.9),
    dict(_C, texto="6 · REVISAR", en="Paso seis", dur=2.2),
    dict(_R, texto="27 ERRORES", en="veintisiete veces", dur=2.4),
    dict(_F, texto="19:19", en="siete y diecinueve", dur=2.2),
    dict(_N, texto="3 H 59 MIN", en="tres horas y cincuenta", dur=2.8, tam=170),
    dict(_R, texto="+1 MIN 19 S", en="Se pasó por un minuto", dur=2.4),
    dict(_N, texto="3 PALABRAS", en="Tres palabras", dur=1.8),
    dict(_N, texto="17 NOV", en="diecisiete de noviembre", dur=1.3, tam=170),
    dict(_F, texto="CRÓNICAS DEL GAMING", en="Crónicas del gaming#2", dur=2.6),
    dict(_F, texto="TÚ DECIDES QUÉ SIGUE", en="dime en los comentarios", dur=3.6),
]

FX = [
    dict(tipo="abre", en=0, dur=.4),
    dict(tipo="temblor", en="Con una falta", amp=18),
    dict(tipo="temblor", en="No hay botón", amp=22),
    dict(tipo="destello", en="Ocho frases", color="rosa", fuerza=.25),
    dict(tipo="temblor", en="veintisiete veces", amp=20),
    dict(tipo="temblor", en="Se nota", amp=16),
    dict(tipo="temblor", en="me cortan", amp=22),
    dict(tipo="oscurecer", de=_tl["total"] - .9, a=_tl["total"] + 1, k=1, entra=.6, sale=0),
]

SFX = {
    "teclas": ("Fast burst of typing on a laptop keyboard, eight quick keystrokes, close and dry", 2),
    "error": ("Cartoon computer error honk, two short low beeps, dry", 1),
    "reloj": ("Clock ticking fast and speeding up, then a single bright bell ding", 2),
    "palomita": ("Soft positive interface confirmation ding, warm and short", 1),
    "cambio": ("Electronic power-down blip then a quick power-up chirp, small device, dry", 1),
    "fanfarria": ("Short triumphant chiptune jingle, three rising notes, 8-bit", 2),
    "barrido": ("Swift airy camera whip swoosh, bright and very short", 1),
    "barrido2": ("Short wind gust whoosh panning left to right, crisp", 1),
    "acerca": ("Short rising digital zoom sweep ending in a soft click", 1),
    "acerca2": ("Quick synthetic swell whoosh into a tiny pop, clean", 1),
    "pasa": ("Plastic card sliding fast across a desk, short swipe", 1),
    "pasa2": ("Smooth interface panel slide whoosh, gentle and very short", 1),
    "chispa": ("Tiny digital static crackle burst, short data corruption, dry", 1),
    "flash": ("Short bright camera flash shimmer, soft sparkle hit", 1),
    "jefe_pop": ("Comic cardboard cutout springing up with a short boing, dry", 1),
}

PISTAS = [
    dict(sfx="teclas", en="nueve palabras", vol=.35),
    dict(sfx="error", en="Con una falta", vol=.4),
    dict(sfx="reloj", en="Cuatro horas", vol=.35),
    dict(sfx="palomita", en="Y lo es", vol=.4),
    dict(sfx="error", en="Ocho frases", vol=.35),
    dict(sfx="palomita", en="Este video también la cumple", vol=.4),
    dict(sfx="ost_tetris", en=_W["gancho_3"][-1]["e"] + .08, vol=.8, voz=True),  # «treinta y seis canciones»: se oye una (Tetris 64) en el hueco
    dict(sfx="ost_yoshi", en=ESCUCHA, vol=.9, voz=True),        # «Escucha.»: la banda sonora real, música Lyria agachada debajo
    dict(sfx="cambio", en="me cortan", vol=.5),
    dict(sfx="error", en="veintisiete veces", vol=.4),
    dict(sfx="fanfarria", en="salió el video", vol=.3),
    dict(sfx="error", en="Se nota", vol=.35),
    dict(sfx="palomita", en="Tres palabras", vol=.35),
    dict(sfx="teclas", en="escríbelo bien", vol=.3),
]

# cada transición y cada entrada del Jefe suenan: toma.py deja sus segundos en medios/golpes.json
_SON = dict(latigo=(("barrido", "barrido2"), .32), zoom=(("acerca", "acerca2"), .3), deslizar=(("pasa", "pasa2"), .3), glitch=(("chispa",), .34),
            destello=(("flash",), .22), jefe=(("jefe_pop",), .4))
if os.path.exists("medios/golpes.json"):
    for i, (tipo, t) in enumerate(json.load(open("medios/golpes.json", encoding="utf-8"))):
        if tipo in _SON:
            nombres, vol = _SON[tipo]
            PISTAS.append(dict(sfx=nombres[i % len(nombres)], en=round(max(0, t - .12), 3), vol=vol))
