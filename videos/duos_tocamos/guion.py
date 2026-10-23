# -*- coding: utf-8 -*-
"""«Así tocamos» — Los Duos (tecladista y dos voces). Video vertical SIN NARRADOR para mandar por WhatsApp/Facebook a quien
pida videos de cómo toca el grupo (el usuario, 22-oct-2026): una secuencia de sus videos reales con 4 de sus canciones
(tramos de ~26-28 s cortados en frases completas), con los mismos elementos del anuncio videos/duos_promo/: marca negro +
dorado, logo «Los Duos» en Kaushan Script, «● EN VIVO», ecualizador que baila con la música real, notas y destellos.
Kit copiado de duos_promo (pix.py + duos.py); escenas propias en escenas.py; cortes al pulso de cada canción en cortes.json
(plan_cortes.py); música = audio/musica.wav (musica_medley.py, canciones completas con voz, sin Lyria). Sin subtítulos.
"""

TITULO = "Los Duos — así tocamos"
ARCHIVO = "los_duos_asi_tocamos"
FORMATO = "vertical"     # 1080x1920
ESTILO_VISUAL = "documental"     # motion graphics propios por código sobre video real
SIN_VOZ = True
BPM = 480                # NO es el tempo real: un «compás» = 0,5 s, para dar a cada tramo su duración exacta
DURACION = None
SUBTITULOS = False
TRANSICIONES = [("continua", 0.04)] * 5
MEZCLA = dict(musica=-14.0, fx=-6.0)

STEMS = "E:/FabricaAnimaciones/videos/duos_promo/audio/stems"     # canciones del grupo (A1..A4) y su separación Demucs
# Tramo de cada canción: (pieza, segundo de la pieza donde empieza, rótulo = primera frase que se canta en el tramo).
# Frases ubicadas con Whisper (ver videos/duos_promo/ESTADO.md).
CANCION = {
    "indita": ("A1", 27.30, "CHIQUITA Y BONITA"),           # cumbia: «…nadie la consuela / Yo le di mi amor…»
    "ojos": ("A4", 27.50, "MIS OJOS ME DENUNCIAN"),         # hasta «…de qué será de mi destino»
    "amor": ("A2", 89.60, "ES TU AMOR"),                    # balada: hasta «…la noche eterna que nunca amaneció»
    "teodora": ("A3", 17.00, "TEODORA"),                    # corrido: las primeras estrofas
}

ESCENAS = [
    {"id": "intro", "compases": 7, "frases": []},        # 3,5 s: el logo nace sobre el escenario (instrumental de La indita)
    {"id": "indita", "compases": 53, "frases": []},      # 26,5 s
    {"id": "ojos", "compases": 52, "frases": []},        # 26 s
    {"id": "amor", "compases": 57, "frases": []},        # 28,5 s
    {"id": "teodora", "compases": 57, "frases": []},     # 28,5 s
    {"id": "cierre", "compases": 16, "frases": []},      # 8 s: logo, WhatsApp, precio y zona
]
