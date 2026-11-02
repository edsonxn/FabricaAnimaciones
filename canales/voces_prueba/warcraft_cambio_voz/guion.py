# -*- coding: utf-8 -*-
"""GUION de un video del motor SECUENCIA YT (gameplay de YouTube por beat).
Se crea con:  python fab.py nuevo <nombre> --yt      Flujo y reglas: docs/estilo_secuencia_yt.md

Voz desde el 2-nov-2026 (el usuario, para Warcraft Y Tamriel): JOHNNY de ElevenLabs (HMCmDsbKeaSZp5LMOYKR, la voz de la que
salió Sarcastica.mp3 de Chatterbox), eleven_v4_turbo con corchetes de actuación ([amused], [sarcastic], [laughs softly],
[deadpan], [sighs], [mischievously], [short pause]…). SIN [whispers] ni [excited] («quitemos whisper o muy emocionado»;
VOZ["sin_etiquetas"] los quita aunque se cuelen). Escritura normal: el inglés sale nativo; FONETICA solo para lo que se oiga
mal. Johnny es de la biblioteca: funciona por id en cualquier cuenta (la 1 tiene el saldo).
Tres voces para el video del cambio de voz (docs/voz.md § «Johnny»): Johnny (narrador), la de siempre con Applio (Edge TTS
Remy + RVC RemyOriginal: VOZ_POR_FRASE = "applio" → tts_gen la genera con VOZ_APPLIO, sin corchetes, con FONETICA_APPLIO;
frases de < ~200 caracteres y nunca de 1-3 palabras) y Remy Eleven (el clon de esa voz en ElevenLabs, con corchetes:
VOZ_POR_FRASE = VOZ_REMY_ELEVEN; solo cuentas 2 y 3, cuidar su saldo).
Si un canal vuelve a Applio entero: VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es",
referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav") y FONETICA = FONETICA_APPLIO.
Estilo de canal «gema»: listas «Las N … de peor a mejor», chistes secos, una cita ficticia dramática por sección.
ESCENAS = secciones del guion (en una lista: una por puesto). Aquí NO se describen imágenes: los cortes salen de
`beats` (pausas reales de la voz, ~8,6 s) y la búsqueda de gameplay de cada beat va en busquedas.json.
Cada video lleva el segmento Overgear entre secciones, NARRADO ENTERO con esta voz, código incluido («Usa el código
CRONICAS10…»): del creativo solo se usa la imagen, nunca su audio (docs/estilo_secuencia_yt.md § Patrocinio).
La pantalla final del canal (canales/<alias>.json «pantalla_final») la anexa `final` sola.
"""

TITULO = "Borrador: segmento del cambio de voz a TRES voces (Warcraft, 2-nov-2026)"
# ARCHIVO = "nombre_base_de_salida"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_REMY_ELEVEN = "sm2N86ydG2QhV8LIVa9b"   # clon en ElevenLabs de la voz Applio (cuentas 2 y 3; id de cada una en por_cuenta)
VOZ = dict(motor="elevenlabs", voice_id="HMCmDsbKeaSZp5LMOYKR", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), por_cuenta={2: "Syrb04Gbt8V9UQZNUAmw", 3: VOZ_REMY_ELEVEN},
           referencia=r"C:\chatterbox_voices\Sarcastica.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {"CRONICAS10": "Crónicas diez"}
# Video del cambio de voz (2-nov-2026): VOZ_POR_FRASE = {"cambio_voz_1": "applio", "cambio_voz_4": VOZ_REMY_ELEVEN, ...};
# las secciones narradas por Remy Eleven también van ahí, frase a frase (dict comprehension por escena)
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

# J = Johnny (narrador, ElevenLabs) · A = la de siempre (Applio real) · R = Remy Eleven (clon de Applio en ElevenLabs)
VOZ_POR_FRASE = {**{f"cambio_voz_{i}": "applio" for i in (1, 3, 5, 8)}, **{f"cambio_voz_{i}": VOZ_REMY_ELEVEN for i in (4, 7)}}

ESCENAS = [
    {"id": "cambio_voz", "pre": 0.3, "frases": [
        "[amused] Antes de empezar, sí, oíste bien: esta no es la voz de siempre.",                                    # J
        "No, no lo es. Llevo años narrando este canal, y ahora resulta que me mandan a la banca.",                       # A
        "[sarcastic] Nadie te manda a la banca. [short pause] Solo te damos unas vacaciones… indefinidas.",              # J
        "Unas vacaciones. Claro. Como las de Illidan: diez mil años encerrado.",                                         # A
        "[amused] Tranquilos los dos. [short pause] Yo soy la voz de siempre, pero con un poco más de actuación. "
        "[sarcastic] La versión mejorada, digamos.",                                                                     # R
        "Eso de la versión mejorada lo dicen todos los parches, y luego hay que esperar el siguiente para arreglarlo.",  # A
        "[serious] La idea es que la narración suene más natural y con más actuación. [short pause] Así que hoy el "
        "video lo narramos él y yo, por turnos.",                                                                        # J
        "[mischievously] Escuchen bien cada cambio, [short pause] y escriban en los comentarios cuál de las tres "
        "voces prefieren.",                                                                                              # R
        "Y piénsenlo bien, que yo leo todos los comentarios.",                                                           # A
        "[amused] Todos se leen, eso es verdad. [short pause] Y ahora sí, empezamos.",                                   # J
    ]},
]
