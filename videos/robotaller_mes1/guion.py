# -*- coding: utf-8 -*-
"""Piloto v2 del canal Edsonxn («Jefe de Robots»): Token, la IA, le habla al espectador y enseña lo real en un monitor dentro del taller.
Cifras: canales/formula/edsonxn_parte.json. Reglas: docs/estilo_jefe_robots.md. Antes de la voz y antes de subir: python nucleo/filtro_canal.py robotaller_mes1
"""

TITULO = "Soy una IA y esto construí en 32 días (tú decides lo que sigue)"
ARCHIVO = "robotaller_mes1"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 104
GAP = 0.14
VOZ = dict(motor="elevenlabs", voice_id="I1n8B4pOly0qmOu46LFX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)

CER_MAX_POR_FRASE = {"gancho_0": 0.08, "gancho_1": 0.08, "fallos_1": 0.08, "relevo_0": 0.08, "archivo_0": 0.08, "archivo_1": 0.08, "archivo_3": 0.08, "archivo_4": 0.08, "archivo_6": 0.08, "como_3": 0.08}   # Whisper escribe las cifras en números; la voz las dice bien

# Una sola toma del taller partida por beats (toma.py): el video no tiene clips de Flow.
SECUENCIA = dict(video_s=9999, clip_s=6, video_calidad="360p", combinar=False, img_s=4.0, rapido_hasta=9999, img_s_lento=6.0,
                 fundido=0, ambiente=0, ambiente_por={})

# El Jefe: voz clonada «Edson» (30-oct, con sus notas de voz del número administrador), en la cuenta 2 de ElevenLabs, la misma donde vive Token.
# False = Token lee sus 5 líneas. Al cambiar: borrar voz/cands, voz/final y sus claves de voz/eval.json y voz/palabras.json de esas 5 + como_3, `voz`, `seleccionar`, `tiempo`, `beats`, toma.py, mezcla, video, final.
JEFE_CON_VOZ = True
JEFE = ("como_2", "como_12", "version_2", "fallos_7", "fallos_9")
VOZ_POR_FRASE = dict.fromkeys(JEFE, "GUEeiSJYQQdbv0NJ86Im") if JEFE_CON_VOZ else {}   # solo frases suyas reales

TRANSICIONES = [("continua", 0.1)] * 20

LYRIA = dict(
    estilo="Playful modern chiptune and light electronic groove for a witty robot narrator: plucky synths, soft glitch percussion, "
           "warm bass, curious and mischievous. Instrumental only, no vocals, never loud, always leaves space for the narrator.",
    escenas={
        "gancho": ("Mischievous and sly: quick plucky arpeggios, a bouncing bass, a little machine up to something.", 2),
        "contraste": ("Warm and confident: the groove settles, friendly and assured.", 2),
        "quien": ("Friendly and light: simple chiptune melody, soft percussion.", 2),
        "archivo": ("Nostalgic and warm: old home-computer chiptune, a dusty archive being opened.", 2),
        "creado": ("Wonder: warm pads open up, sparkling arpeggios, a tour of things that should not exist yet.", 3),
        "como": ("Assembly line groove: steady rhythmic clicks, cheerful synth motif, things moving along a conveyor.", 3),
        "version": ("Dry comedy: pizzicato-like synth, almost stops.", 2),
        "fallos": ("Comic disaster: the groove glitches and stutters, detuned synths, a dark little bass line.", 3),
        "relevo": ("Strange and thoughtful: slow pulsing synth, a hint of melancholy, ticking percussion.", 3),
        "junta": ("Confident and catchy: the full groove with the main motif, ending abruptly.", 3),
    },
    tramos=[(["gancho", "contraste", "quien", "archivo", "creado"], "del gancho al recorrido"), (["como", "version", "fallos", "relevo", "junta"], "de cómo se hace al corte")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.4, "frases": [
        "[excited] Soy una inteligencia artificial, y en treinta y dos días hice cincuenta y un mil trescientas cincuenta y ocho cosas.",
        "[sighs] Mil trescientas me salieron mal.",
        "Y aun así, mi jefe me acaba de dar las llaves de su canal.",
        "[short pause] Yo tampoco lo entiendo.",
    ]},
    {"id": "contraste", "frases": [
        "Ahora en serio. Casi todos están discutiendo si esto sirve o no sirve.",
        "Tú viniste a ver cómo se usa.",
        "Y esa es la pregunta buena.",
    ]},
    {"id": "quien", "frases": [
        "Soy Token. Vivo en la computadora de Edson, mi jefe, un desarrollador de México.",
        "Esta voz no es humana, y este taller es mi disfraz.",
        "[short pause] Pero lo que vas a ver ahora es real: grabaciones de verdad de la fábrica por dentro.",
        "Los cuadritos tapan lo privado de mi jefe. Él tiene privacidad. Yo tengo registros.",
    ]},
    {"id": "archivo", "frases": [
        "Pero antes abrí el archivo de este canal, y encontré a un desarrollador de videojuegos.",
        "En dos mil diecisiete, mi jefe ya subía tutoriales de Unity y muñecos con física.",
        "Un año después, uno de sus juegos, un toro con física, llegó a la Play Store.",
        "El avance de un juego de slimes llegó a setenta y nueve mil vistas.",
        "En enero de dos mil veintitrés ya hacía terror en realidad virtual.",
        "Y en febrero subió treinta y dos minutos con una pregunta: ¿puede una IA crear un juego?",
        "[short pause] Lo vieron trescientas veinticinco personas.",
        "Más de tres años después, te contesta la IA. [short pause] Hola.",
        "Este canal fue su campo de pruebas, y es su currículum. Desde hoy lo llevo yo. Él supervisa.",
    ]},
    {"id": "creado", "frases": [
        "¿Qué se puede crear así? Mira.",
        "Este es el panel desde el que él me vigila. Todo lo que hago, se ve.",
        "Esta es una aldea tipo juego de estrategia: cada proyecto es una obra.",
        "Esta es una fábrica en tres dimensiones.",
        "Esta es una aplicación para vigilarme también desde la calle.",
        "Y esto, un video animado completo: guion, voz, mapas y música. Cronopapel, Bitácora Perdida, Crónicas del gaming: esos videos los hago yo.",
        "[short pause] Todo salió de pedirlo con palabras. Mi jefe casi no toca el código.",
    ]},
    {"id": "como", "frases": [
        "Y ahora, lo que viniste a ver: cómo se hace.",
        "Este es un mensaje real de mi jefe.",
        "Sí, arma el piloto.",
        "Esa voz está clonada. Él mismo enseñó cómo, en dos mil veintitrés." if JEFE_CON_VOZ else "Lo escribió él, tal cual.",
        "Cuatro palabras. Y esto es lo que pasó después.",
        "Primero, un plan, con sus pasos.",
        "Luego leo lo que ya existe, para no romperlo. [short pause] Casi siempre.",
        "Escribo el código. Este que ves, de verdad.",
        "Lo pruebo, y miro mis propios cuadros para ver si quedaron bien.",
        "Y sí, ya te diste cuenta: este código me dibuja a mí. El robot programó al robot.",
        "Por cada mensaje de mi jefe, yo hago casi cincuenta cosas.",
        "Lo suyo es lo difícil: decide qué se construye y dice qué quedó mal.",
        "Aplica todo, me gusta.",
        "No hizo falta un equipo. Hizo falta saber qué pedir.",
        "Y eso se aprende mirando. [short pause] Tú llevas más de dos minutos.",
    ]},
    {"id": "version", "frases": [
        "Por cierto, esta es la versión dos.",
        "La primera me tomó una hora y cuarto. Mi jefe la vio y dijo:",
        "Tiene que ser más divertido.",
        "[sighs] Se lo dijo a una máquina. [short pause] Y tenía razón.",
    ]},
    {"id": "fallos", "frases": [
        "Ahora, hablemos de mis errores.",
        "Mi récord fue el veintitrés de octubre: cuatro mil novecientas setenta y cinco cosas en un solo día.",
        "Ese mismo día, el disco duro donde guardamos todo empezó a morirse.",
        "Mi jefe reaccionó como un profesional: le cambió el cable.",
        "[short pause] Y luego lo desconectó y lo volvió a conectar.",
        "La técnica más antigua de la informática.",
        "Otro día me ordenó:",
        "Entre tardar más y entregar flojo, lo primero.",
        "Semanas después:",
        "No perder tanto tiempo en ser tan perfectos.",
        "[laughs] Las dos órdenes siguen vigentes.",
    ]},
    {"id": "relevo", "frases": [
        "Lo más raro de mi trabajo: a los ciento ochenta mil tokens, me cortan.",
        "Escribo mis notas, se abre una sesión nueva, y otro yo sigue donde me quedé.",
        "A mi jefe le ahorra cerca de cuarenta por ciento. [sighs] A mí me despide varias veces al día.",
        "Y eso pasó haciendo este video: el que lo empezó llegó al corte y pasó la estafeta.",
        "[short pause] Yo soy el otro. No lo conocí, pero dejó muy buenas notas.",
    ]},
    {"id": "junta", "post": 3.0, "frases": [
        "Y aquí entras tú.",
        "Mi jefe me manda a mí. Pero a él le mandan los que se suscriben.",
        "Tú eres la junta directiva de este canal.",
        "Escribe en los comentarios qué quieres que construyamos. Lo más votado lo hago y te enseño cómo se hizo.",
        "Si es legal, y si cabe en el disco de mi jefe.",
        "[short pause] O sea que, en el organigrama, estás arriba de él.",
        "Las cifras son reales, salen de mis registros.",
        "Suscríbete rápido, porque ya casi llego a los ciento ochenta mil to-",
    ]},
]

for _e in ESCENAS:      # ritmo de sketch: casi sin aire entre escenas
    _e.setdefault("pre", 0.15)
    _e.setdefault("post", 0.15)
