# -*- coding: utf-8 -*-
"""GUION de un video del motor SECUENCIA YT (gameplay de YouTube por beat; Crónicas de Warcraft).
Se crea con:  python fab.py nuevo <nombre> --yt      Flujo y reglas: docs/estilo_secuencia_yt.md

Voz Applio (Edge TTS Remy -> RVC RemyOriginal): frases cortas (< ~200 caracteres), escritura normal.
Estilo de canal «gema»: listas «Las N … de peor a mejor», chistes secos, una cita ficticia dramática por sección.
ESCENAS = secciones del guion (en una lista: una por puesto). Aquí NO se describen imágenes: los cortes salen de
`beats` (pausas reales de la voz, ~8,6 s) y la búsqueda de gameplay de cada beat va en busquedas.json.
Cada video lleva el segmento Overgear (CRONICAS10) entre secciones: ver docs/migracion_googleimagenes.md.
"""

TITULO = "Título del video"
# ARCHIVO = "nombre_base_de_salida"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # el audio del gameplay no se usa (se bajan solo imágenes)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),   # canales que salen con cara/overlay y ensucian el plano
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore in the style of World of Warcraft: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        # "intro": ("adventurous and curious, light percussion", 4),
    })

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Gancho: la promesa de la lista y por qué importa hoy.",
    ]},
    {"id": "cierre", "frases": [
        "Cierre y pregunta para comentarios.",
    ]},
]
