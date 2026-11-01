# -*- coding: utf-8 -*-
"""PRUEBA de análisis táctico de esports (sin canal, 26-oct-2026): una jugada de la Worlds 2026 de League of Legends
explicada como los análisis de la NFL: pausas, anillos sobre los campeones, flechas, rutas y un mapa táctico inclinado.
Motor SECUENCIA YT con UN solo clip (medios/_fuente/jugada.mp4 = VOD completo de la partida 2, 39:40-42:40 del reloj):
el FX `video` de efectos.py elige qué tramo se ve (vel=1 juega, vel=0 congela, vel<0 rebobina) y el kit
nucleo/mg_tactica.py dibuja encima. Fuente: «AL vs TLAW - Game 2 | Day 4 LoL Worlds 2026 Swiss Stage» (EpicSkillshot,
transmisión oficial de LoL Esports), https://youtu.be/wjoQ0ze5bJ4 desde 47:13 (reloj de juego = segundo del VOD - 453 s).

Datos verificados en la transmisión (marcador y comentaristas): minuto 40:16 TLAW 11-17 AL en asesinatos, 74,8K-71,8K de
oro (+3,0K), torres 6-2; 3.er dragón (infernal) de TL a 40:18 (AL estaba a uno del alma); oleada arriba + TP de Morgan al
inhibidor; flanco de Shanks (Annie) y Breathe (Olaf) que TL esquiva; «how dark the map is» para AL; Barón a 41:46 con
Tarzan (Nocturne) yendo al centinela de control del fondo del foso; castigo de Josedeodo; AL sin definitivas para forzar;
TL gasta Destello (Jose) y Destello + Curar (CoreJJ). TL ganó la partida y eliminó a AL (0-3 en la fase suiza).
Picks: TLAW Kled (Morgan), Pantheon (Josedeodo), Akali (Quid), Xayah (Yeon), Rakan (CoreJJ) · AL Olaf (Breathe),
Nocturne (Tarzan), Annie (Shanks), Jinx (Hope), Tahm Kench (Kael).
"""

TITULO = "Cómo Team Liquid ganó el Barón SIN PELEAR | Análisis Worlds 2026"
ARCHIVO = "lol_worlds_tl_al"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español): tono de analista deportivo
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
# Nombres en inglés como suenan (el usuario, 26-oct-2026: decía «Liquid» a la española). Llega también a ElevenLabs.
FONETICA = {"Team Liquid": "Tim Lícuid", "Liquid": "Lícuid", "Anyone's Legend": "Éniuans Léyend"}
# Whisper escribe «varón» por Barón, «John» por Yeon, «José Beodo», «Aelle» por AL: transcripciones revisadas, texto correcto
CER_MAX_POR_FRASE = {"gancho_1": .03, "dragon_1": .06, "tempo_3": .05, "baron_0": .03, "baron_2": .06, "remate_1": .03}
TAIL_MAX_POR_FRASE = {"gancho_1": .65, "baron_0": .50}   # ElevenLabs corta justo al terminar la palabra

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="fade",
    fundido=0.0,            # el cuadro lo pone entero el FX `video`: los cortes de beat no se ven
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="League of Legends Worlds 2026", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern sports broadcast analysis underscore: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={},
    tramos=[(["gancho", "contexto", "dragon", "tempo", "vision", "baron", "remate"],
             "biblioteca: mods_ia_fusion__lyria_1 (acción, percusión y sintetizador)")])

ESCENAS = [
    {"id": "gancho", "pre": 0.2, "frases": [
        "[excited] Minuto 41. Team Liquid mata al Barón… y con eso empieza a sacar del Mundial a Anyone's Legend, el primer sembrado de China.",
        "[short pause] Pero este Barón no se ganó en el foso. Se ganó noventa segundos antes. Vamos a rebobinar.",
    ]},
    {"id": "contexto", "pre": 0.3, "frases": [
        "Minuto 40. Liquid va perdiendo en asesinatos, 11 a 17… pero lleva 3 mil de oro de ventaja y seis torres contra dos.",
        "Y en juego está el tercer dragón. [short pause] Si lo toma AL, se queda con el alma.",
    ]},
    {"id": "dragon", "pre": 0.2, "frases": [
        "Liquid llega primero. Pantheon guarda el castigo, Xayah pega desde atrás, y AL todavía está entrando al foso.",
        "[excited] ¡Y es Yeon quien lo asegura! Tres dragones para Liquid, y el alma se le escapa a AL.",
    ]},
    {"id": "tempo", "pre": 0.3, "frases": [
        "Ahora mira el mapa. Mientras todos pelean abajo, una oleada de Liquid empuja sola por arriba, directo a la torre del inhibidor.",
        "AL tiene que elegir: defender su base o seguir a Liquid. [short pause] No puede hacer las dos cosas.",
        "Y Morgan lo aprovecha: teletransporte arriba con Kled para presionar el inhibidor.",
        "AL intenta un flanco con Annie y Olaf para cortarles el paso… pero Liquid no muerde el anzuelo y se retira.",
    ]},
    {"id": "vision", "pre": 0.3, "frases": [
        "Faltan 40 segundos para el Barón. Y fíjate en lo oscuro que está el mapa de AL: Liquid controla todo el lado de arriba.",
    ]},
    {"id": "baron", "pre": 0.3, "frases": [
        "Liquid empieza el Barón… y se derrite: en segundos ya va en 11 mil de vida.",
        "Nocturne entra por el fondo del foso buscando el robo, pero el resto de AL todavía viene de lejos.",
        "[excited] ¡Y Josedeodo no falla el castigo! ¡Barón para Liquid!",
    ]},
    {"id": "remate", "pre": 0.3, "frases": [
        "AL quiere pelear después, pero sin definitivas no puede forzar nada. Liquid sale con vida y solo gasta dos Destellos y una Curación.",
        "[short pause] Esa es la lección: este Barón se ganó con un dragón, una oleada y paciencia.",
        "¿Qué otra jugada del Mundial quieres que analicemos? Déjamelo en los comentarios.",
    ]},
]
