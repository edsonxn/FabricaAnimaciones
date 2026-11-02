# -*- coding: utf-8 -*-
"""GUION de un video del motor SECUENCIA YT (gameplay de YouTube por beat).
Se crea con:  python fab.py nuevo <nombre> --yt      Flujo y reglas: docs/estilo_secuencia_yt.md

Voz desde el 2-nov-2026 (el usuario, para Warcraft Y Tamriel): JOHNNY de ElevenLabs (HMCmDsbKeaSZp5LMOYKR, la voz de la que
salió Sarcastica.mp3 de Chatterbox), eleven_v4_turbo con corchetes de actuación ([amused], [sarcastic], [laughs softly],
[deadpan], [sighs], [mischievously], [short pause]…). SIN [whispers] ni [excited] («quitemos whisper o muy emocionado»;
VOZ["sin_etiquetas"] los quita aunque se cuelen). Escritura normal: el inglés sale nativo; FONETICA solo para lo que se oiga
mal. Johnny es de la biblioteca: funciona por id en cualquier cuenta (la 1 tiene el saldo).
La voz VIEJA de Warcraft (Applio: Edge TTS Remy + RVC RemyOriginal) puede decir frases sueltas en un video de ElevenLabs:
VOZ_POR_FRASE = {"<escena>_<i>": "applio"} → tts_gen las genera con VOZ_APPLIO (sin corchetes, con FONETICA_APPLIO); se usa
en el segmento del cambio de voz (docs/voz.md § «Johnny»). Applio: frases de < ~200 caracteres y nunca de 1-3 palabras.
Si un canal vuelve a Applio entero: VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es",
referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav") y FONETICA = FONETICA_APPLIO.
Estilo de canal «gema»: listas «Las N … de peor a mejor», chistes secos, una cita ficticia dramática por sección.
ESCENAS = secciones del guion (en una lista: una por puesto). Aquí NO se describen imágenes: los cortes salen de
`beats` (pausas reales de la voz, ~8,6 s) y la búsqueda de gameplay de cada beat va en busquedas.json.
Cada video lleva el segmento Overgear entre secciones, NARRADO ENTERO con esta voz, código incluido («Usa el código
CRONICAS10…»): del creativo solo se usa la imagen, nunca su audio (docs/estilo_secuencia_yt.md § Patrocinio).
La pantalla final del canal (canales/<alias>.json «pantalla_final») la anexa `final` sola.
"""

TITULO = "Título del video"
# ARCHIVO = "nombre_base_de_salida"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HMCmDsbKeaSZp5LMOYKR", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), referencia=r"C:\chatterbox_voices\Sarcastica.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {"CRONICAS10": "Crónicas diez"}
# La voz de siempre de Warcraft, para VOZ_POR_FRASE = {"cambio_voz_1": "applio", ...} (solo en el video del cambio de voz)
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md)
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "Battle punto net": "Bátel punto net", "Hardcore": "Jardcor", "Vanilla": "Vanila", "retail": "ritéil",
    "Burning Crusade": "Bérnin Kruséid", "Arthas": "Ársas", "Illidan": "Ilidán", "Hyjal": "Jáyal", "CRONICAS10": "Crónicas diez",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # por defecto solo imagen; el audio del juego va donde conviene oírlo (regla del 26-oct-2026):
    ambiente_por={},        # {"scene-012": .7}: ese beat baja CON su audio (música del juego, gritos, SFX); la OST se aparta ahí
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
