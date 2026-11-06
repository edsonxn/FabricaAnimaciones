# -*- coding: utf-8 -*-
"""Efectos de robotaller_4apps: rótulos (solo énfasis, en el piso), golpes y SFX. La cámara y las transiciones van en toma.py (nucleo/montaje_real.py).
Copiado de videos/robotaller_n64/efectos.py y reanclado. SFX con prompts y nombres NUEVOS: ninguno repite un archivo de los videos anteriores del canal.
«Escucha:» (fin de puente_3) → suena la tele real del 4-nov 12:35 (sfx/tele_1235.mp3, caché de Puente TV) con la voz callada (post 4,6 s);
el robot de la tele simulada sale en ese mismo instante (toma.py: tele_aviso empieza en ESCUCHA − 3,4). Formato: nucleo/secuencia_fx.py."""
import json
import os

_tl = json.load(open("timeline.json", encoding="utf-8"))
_W = {f["key"]: f["words"] for e in _tl["escenas"] for f in e["frases"]}
ESCUCHA = _W["puente_3"][-1]["e"] + .08

_P = dict(tam=140, color="blanco", y=.885, pop=.35, sale=.25)
_C = dict(_P, tam=96)                             # el nombre de lo que se ve
_F = dict(_C, color="amarillo")
_N = dict(_P, tam=150, color="amarillo")          # cifras
_R = dict(_P, tam=150, color="rosa")              # cifras de fallos

ROTULOS = [
    dict(_N, texto="4 APPS · < 24 H", en="Menos de veinticuatro horas", dur=2.6),
    dict(_F, texto="CONVERSACIONES REALES", en="con las conversaciones reales", dur=2.4),
    dict(_F, texto="GRABACIÓN REAL", en="lo demás es real", dur=2.0),
    dict(_R, texto="0 LÍNEAS DE CÓDIGO", en="ni una línea", dur=2.4, tam=120),
    dict(_C, texto="1 · ESCÁNER DEL CARRO", en="Aplicación uno", dur=2.2),
    dict(_F, texto="3-NOV · 16:58", en="cinco de la tarde", dur=2.0),
    dict(_N, texto="24 MIN", en="Veinticuatro minutos", dur=1.9, tam=170),
    dict(_R, texto="NO FUNCIONÓ", en="Y no funcionó", dur=1.8),
    dict(_R, texto="×3", en="Tres veces", dur=1.4, tam=190),
    dict(_N, texto="4 VERSIONES · 36 MIN", en="Cuatro versiones", dur=2.6, tam=120),
    dict(_F, texto="18:03", en="seis y tres", dur=2.0, tam=150),
    dict(_C, texto="ALERTAS CON VOZ", en="alertas con voz", dur=2.2),
    dict(_C, texto="2 · MICWIFI", en="Aplicación dos", dur=2.2),
    dict(_F, texto="4-NOV · 9:30", en="nueve y media", dur=2.0),
    dict(_R, texto="RED «PÚBLICA»", en="marcada como pública", dur=2.0, tam=120),
    dict(_N, texto="18 MIN", en="Dieciocho minutos", dur=1.9, tam=170),
    dict(_C, texto="3 · RAYO", en="Aplicación tres", dur=2.2),
    dict(_F, texto="SIN CABLE · SIN NUBE", en="sin cable", dur=2.4, tam=110),
    dict(_N, texto="22 MIN", en="Veintidós minutos", dur=1.9, tam=170),
    dict(_F, texto="ENVIAR A TELÉFONO", en="clic derecho", dur=2.4, tam=110),
    dict(_C, texto="4 · PUENTE TV", en="Aplicación cuatro", dur=2.4),
    dict(_R, texto="51 MIN ESPERANDO", en="cincuenta y un minutos", dur=2.4, tam=120),
    dict(_F, texto="4-NOV · 12:35", en="doce y treinta y cinco", dur=2.2),
    dict(_F, texto="♪ LA TELE, DE VERDAD", en=ESCUCHA, dur=3.4),
    dict(_C, texto="SALA DE REVISIÓN", en="sala de revisión", dur=2.4),
    dict(_C, texto="PROTECTOR DE PANTALLA", en="protector de pantalla", dur=2.4),
    dict(_N, texto="23 H 57 MIN", en="veintitrés horas", dur=3.0, tam=170),
    dict(_N, texto="838 ACCIONES", en="ochocientas treinta", dur=2.4),
    dict(_R, texto="0 EN TIENDAS", en="Ninguna está en una tienda", dur=2.0),
    dict(_F, texto="¿QUÉ TE ESTORBA?", en="qué te estorba", dur=2.4),
    dict(_F, texto="TÚ ELIGES LA SIGUIENTE APP", en="dime en los comentarios", dur=3.6, tam=88),
]

FX = [
    dict(tipo="abre", en=0, dur=.4),
    dict(tipo="temblor", en="Y no funcionó", amp=20),
    dict(tipo="destello", en="Tres veces", color="rosa", fuerza=.22),
    dict(tipo="temblor", en="bloqueaba al teléfono", amp=16),
    dict(tipo="temblor", en="Prioridades", amp=14),
    dict(tipo="oscurecer", de=_tl["total"] - .9, a=_tl["total"] + 1, k=1, entra=.6, sale=0),
]

SFX = {
    "motor_viejo": ("Old car engine cranking twice and starting, then a short idle, close and dry", 2),
    "bloop_fallo": ("Short descending synth bloop, gentle comic failure sound, dry", 1),
    "moneda": ("Bright arcade coin pickup with a short sparkle tail", 1),
    "notifica": ("Smartphone notification double chime, clean modern, short", 1),
    "chasquido": ("Small electric zap, quick lightning crackle, short and crisp", 1),
    "tele_enciende": ("Old television switching on, soft click and a rising electric hum, short", 1),
    "aplauso": ("Short burst of enthusiastic small crowd applause with a whistle", 2),
    "cronometro": ("Mechanical stopwatch ticking fast for two seconds, then a single click", 2),
    "ronquido": ("Cartoon snore, one comic inhale and a whistling exhale", 2),
    "tecleo_rapido": ("Quick flurry of soft mechanical keyboard typing, six keystrokes, dry", 1),
    "silbido": ("Fast whip whoosh through the air, very short, crisp", 1),
    "silbido2": ("Short swish of a thin stick cutting air, bright, very short", 1),
    "lupa": ("Short sci-fi zoom-in blip rising in pitch, ending in a tiny click", 1),
    "lupa2": ("Quick airy rising swell into a soft digital pop", 1),
    "desliza": ("Sheet of paper sliding fast across a wooden table, short", 1),
    "desliza2": ("Soft interface card swipe whoosh, very short and clean", 1),
    "estatica": ("Brief digital glitch stutter, bitcrushed, very short", 1),
    "brillo": ("Soft magical shimmer swell, very short, bright", 1),
    "jefe_sale": ("Spring-loaded cardboard figure popping up with a comic wobble, short", 1),
}

PISTAS = [
    dict(sfx="tecleo_rapido", en="Mi jefe me pidió", vol=.3),
    dict(sfx="moneda", en="las cuatro funcionaban", vol=.4),
    dict(sfx="tecleo_rapido", en="Escribió lo que necesitaba", vol=.3),
    dict(sfx="motor_viejo", en="tiene un carro", vol=.35),
    dict(sfx="bloop_fallo", en="Y no funcionó", vol=.45),
    dict(sfx="bloop_fallo", en="Tres veces", vol=.35),
    dict(sfx="moneda", en="Cuatro versiones", vol=.35),
    dict(sfx="notifica", en="alertas con voz", vol=.45),
    dict(sfx="bloop_fallo", en="bloqueaba al teléfono", vol=.4),
    dict(sfx="aplauso", en="ovación de pie", vol=.45),
    dict(sfx="chasquido", en="por este rayo", vol=.5),
    dict(sfx="notifica", en="enviar a teléfono", vol=.4),
    dict(sfx="tele_enciende", en="Aplicación cuatro", vol=.4),
    dict(sfx="tele_1235", en=ESCUCHA, vol=1.0, voz=True),      # «Escucha:»: la primera frase real de la tele, con la voz callada
    dict(sfx="cronometro", en="Haz la cuenta", vol=.35),
    dict(sfx="ronquido", en="mi jefe durmió", vol=.45),
    dict(sfx="moneda", en="ochocientas treinta", vol=.35),
    dict(sfx="tecleo_rapido", en="escríbela con más palabras", vol=.3),
]

# cada transición y cada entrada del Jefe suenan: toma.py deja sus segundos en medios/golpes.json
_SON = dict(latigo=(("silbido", "silbido2"), .32), zoom=(("lupa", "lupa2"), .3), deslizar=(("desliza", "desliza2"), .3), glitch=(("estatica",), .34),
            destello=(("brillo",), .22), jefe=(("jefe_sale",), .4))
if os.path.exists("medios/golpes.json"):
    for i, (tipo, t) in enumerate(json.load(open("medios/golpes.json", encoding="utf-8"))):
        if tipo in _SON:
            nombres, vol = _SON[tipo]
            PISTAS.append(dict(sfx=nombres[i % len(nombres)], en=round(max(0, t - .12), 3), vol=vol))
