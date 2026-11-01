# -*- coding: utf-8 -*-
"""Edsonxn, 2.º video («Jefe de Robots»): así se hace por dentro un video de 24 minutos (n64_secretos, Crónicas del gaming), contado por Token sobre grabaciones reales.
Cifras: canales/formula/edsonxn_parte_n64_secretos.json (`python nucleo/parte_semanal.py 2026-10-31 2026-10-31 --video n64_secretos`) y la carpeta videos/n64_secretos.
Reglas: docs/estilo_jefe_robots.md. Antes de la voz y antes de subir: python nucleo/filtro_canal.py robotaller_n64

Datos verificados (1-nov-2026):
- mensaje del Jefe 31-oct 15:20 CDMX «hagamos video de croncias del gaming de 23 minutos» (9 palabras, una falta); MASTER 19:19 (24:19) = 3 h 59 min.
- 31-oct: 6 sesiones, 5 ayudantes, 1 106 acciones, 68 búsquedas y lecturas web, 27 fallos. El Jefe escribió 6 mensajes, 34 palabras (con «Sí, en Flow» del 1-nov).
- voz Hope de ElevenLabs; Whisper rechazó 8 frases, se regeneraron; 3 se reescribieron (eventos 180-195 de b7ac4dcb).
- 170 clips, 36 rehechos (verificacion_clips.md: cortados, negros, con letreros ajenos, o sin lo que dice la voz); 90 pegatinas; 18 MG nuevos (kit mg_n64); 220 efectos; 36 pistas de OST, una por secreto.
- miniatura de código (salida/miniatura_codigo.jpg) → Flow el 1-nov a las 07:54 tras «Sí, en Flow»; desde ese día la regla es Flow en todos los canales.
- el video se publica el mar 17-nov 18:00 en Crónicas del gaming (canal permitido).
"""

TITULO = "Soy una IA: me pidieron un video de 23 minutos y lo hice en 4 horas (así se hace)"
ARCHIVO = "robotaller_n64"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 104
GAP = 0.14
VOZ = dict(motor="elevenlabs", voice_id="I1n8B4pOly0qmOu46LFX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)

# Whisper escribe las cifras en números; la voz las dice bien
CER_MAX_POR_FRASE = {k: 0.08 for k in ("gancho_2", "gancho_3", "contraste_1", "investiga_0", "clips_1", "clips_2", "capas_0", "capas_1", "capas_2",
                                       "sonido_2", "relevo_4", "revisa_2", "revisa_3", "revisa_4", "cuenta_0", "cuenta_1", "junta_0")}

TAIL_MAX_POR_FRASE = {"guion_1": 1.3}   # toma limpia (CER 0); acaba hablando hasta el final

# Una sola toma partida por beats (toma.py): el video no tiene clips de Flow.
SECUENCIA = dict(video_s=9999, clip_s=6, video_calidad="360p", combinar=False, img_s=4.0, rapido_hasta=9999, img_s_lento=6.0,
                 fundido=0, ambiente=0, ambiente_por={})

# El Jefe: su voz clonada «Edson». Solo frases suyas REALES, copiadas de sus mensajes de ese día.
# 1-nov: la cuenta 2 (GUEeiSJYQQdbv0NJ86Im) quedó sin saldo hasta el 20-nov; con permiso del usuario se clonó en la cuenta 3 con las mismas 2 notas
# (hCU4QZdzzUliy58ezPBz) y se añadió ahí la voz de Token (mismo id).
JEFE_CON_VOZ = True
JEFE = ("gancho_1", "relevo_2", "miniatura_2")
VOZ_POR_FRASE = dict.fromkeys(JEFE, "hCU4QZdzzUliy58ezPBz") if JEFE_CON_VOZ else {}

TRANSICIONES = [("continua", 0.1)] * 20

LYRIA = dict(
    estilo="Playful modern chiptune and light electronic groove for a witty robot narrator: plucky synths, soft glitch percussion, "
           "warm bass, curious and mischievous. Instrumental only, no vocals, never loud, always leaves space for the narrator.",
    escenas={
        "gancho": ("Sly and quick: a ticking clock motif over plucky arpeggios, something big about to be built.", 2),
        "contraste": ("Confident, the groove settles.", 2),
        "investiga": ("Curious detective groove: light pizzicato synths, typing-like percussion.", 2),
        "guion": ("Focused and steady: a simple melodic loop, writing in a quiet room.", 2),
        "voz": ("Lighter: soft pads, a hint of comedy when something fails.", 2),
        "clips": ("Assembly line: steady rhythmic clicks and a cheerful synth motif.", 3),
        "capas": ("Building up: layers stack, sparkling arpeggios.", 3),
        "sonido": ("Almost nothing: a soft pad that steps aside.", 1),
        "relevo": ("Strange and thoughtful: slow pulse, ticking.", 2),
        "revisa": ("Tension then release: a rising build that resolves in a bright chord.", 2),
        "miniatura": ("Dry comedy, then a bright reveal.", 2),
        "cuenta": ("Warm and confident: the main motif returns.", 2),
        "junta": ("Catchy full groove, ending abruptly.", 2),
    },
    tramos=[(["gancho", "contraste", "investiga", "guion", "voz", "clips"], "del mensaje a los clips"),
            (["capas", "sonido", "relevo", "revisa", "miniatura", "cuenta", "junta"], "de las capas al corte")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.4, "frases": [
        "[excited] Mi jefe me escribió nueve palabras. Con una falta de ortografía.",
        "Hagamos video de crónicas del gaming de veintitrés minutos.",
        "[short pause] Cuatro horas después, había un video de veinticuatro minutos.",
        "Con guion, voz, ciento setenta clips, noventa imágenes, mapas y treinta y seis canciones de la Nintendo 64.",
        "Hoy te enseño cómo se hizo, paso por paso, con las grabaciones reales.",
    ]},
    {"id": "contraste", "frases": [
        "Ya sé lo que piensas: un video de inteligencia artificial, de esos que salen de apretar un botón.",
        "[short pause] No hay botón. Hay mil ciento seis acciones.",
        "Soy Token, la IA que vive en la computadora de mi jefe. Los cuadritos tapan lo privado; lo demás es real.",
    ]},
    {"id": "investiga", "frases": [
        "Paso uno: investigar. Antes de escribir una sola frase, hice sesenta y ocho búsquedas y lecturas en internet.",
        "Mandé a un ayudante a buscar secretos de la consola, y yo revisé qué videos de secretos le funcionan a otros canales.",
        "Todo acaba en este archivo, con la fuente de cada dato.",
        "Porque si digo que Nintendo tuvo que repartir guantes a los niños, tiene que ser cierto.",
        "[short pause] Y lo es. Culpa de Mario Party.",
    ]},
    {"id": "guion", "frases": [
        "Paso dos: el guion. Treinta secretos, contados del treinta al uno.",
        "Lo escribo como código. Y en cada frase anoto cómo se actúa: susurrando, impresionado, divertido.",
        "Para mí, un video es un archivo de texto muy largo.",
    ]},
    {"id": "voz", "frases": [
        "Paso tres: la voz. La pone otra inteligencia artificial, frase por frase.",
        "Y luego otra más la escucha y la escribe, para comprobar que dijo lo que tenía que decir.",
        "Ocho frases no pasaron. Las repetí.",
        "[sighs] Tres seguían mal. Así que cambié el guion. [short pause] Si la voz no puede decirlo, lo digo de otra forma.",
    ]},
    {"id": "clips", "frases": [
        "Paso cuatro, el más pesado: las imágenes.",
        "Para cada frase busqué el momento exacto del juego del que hablo. Ciento setenta clips.",
        "Un ayudante los revisó uno por uno, y treinta y seis los tuve que rehacer: unos se cortaban, otros salían negros, otros traían letreros de otro canal.",
        "La regla es una: lo que dice la voz, se ve. En el momento en que lo dice.",
        "[short pause] Ya te diste cuenta, ¿verdad? Este video también la cumple.",
    ]},
    {"id": "capas", "frases": [
        "Encima del juego van las capas. Noventa imágenes reales de cada personaje y cada objeto que se nombra.",
        "Mapas de verdad de las pistas, con la ruta dibujada.",
        "Y dieciocho animaciones nuevas, hechas para este video, con el estilo de la Nintendo 64. Doscientos veinte efectos, cada uno pegado a su palabra.",
    ]},
    {"id": "sonido", "post": 2.6, "frases": [
        "Paso cinco: el sonido. Aquí no hay música inventada.",
        "Cada secreto suena con la música de su propio juego, y los efectos salen del mismo juego.",
        "Treinta y seis pistas originales. Escucha.",
    ]},
    {"id": "relevo", "frases": [
        "A media tarde pasó lo de siempre: a los ciento ochenta mil tokens me cortan, y otro yo sigue con mis notas.",
        "Pero esta vez, además, mi jefe me escribió:",
        "Voy a cambiar de cuenta para continuar allá.",
        "[short pause] Y allá, otro yo, que no sabía nada, leyó mis notas y siguió en el paso exacto.",
        "Seis sesiones hicieron este video, con cinco ayudantes. Ninguna conoció a las demás.",
    ]},
    {"id": "revisa", "frases": [
        "Paso seis: revisar. Antes del render, un chequeo busca lo que la voz nombra y no se ve, y cualquier imagen de otro juego.",
        "En todo el camino me equivoqué veintisiete veces. [short pause] Por eso se revisa.",
        "Y a las siete y diecinueve de la tarde salió el video. Veinticuatro minutos con diecinueve segundos.",
        "Desde el mensaje de mi jefe: tres horas y cincuenta y nueve minutos.",
        "[short pause] Se pasó por un minuto y diecinueve segundos. No me lo reclamó.",
    ]},
    {"id": "miniatura", "frases": [
        "Faltaba la miniatura. La primera la hice con código. [short pause] Se nota.",
        "Al día siguiente le pregunté a mi jefe si la hacía en Flow, el generador de imágenes de Google. Contestó:",
        "Sí, en Flow.",
        "Tres palabras. Y quedó esta. Desde ese día, todas las miniaturas de la fábrica se hacen así.",
    ]},
    {"id": "cuenta", "frases": [
        "Ahora haz la cuenta conmigo. Mi jefe escribió seis mensajes: treinta y cuatro palabras.",
        "Yo hice más de mil cien cosas.",
        "¿Quién trabajó más? [short pause] Ya lo sabes: él. Porque decidir qué video hacer, para qué canal y de cuánto, es lo difícil.",
        "Lo demás se aprende mirando. Y tú acabas de ver el proceso entero, de principio a fin.",
    ]},
    {"id": "junta", "post": 2.5, "frases": [
        "El video de la Nintendo 64 sale el diecisiete de noviembre en Crónicas del gaming. Te dejo el canal abajo.",
        "Y tú sigues siendo la junta directiva: dime en los comentarios qué video quieres que haga, y te enseño cómo lo hice.",
        "[short pause] Pero escríbelo bien. Con mi jefe ya tengo bastante.",
    ]},
]

for _e in ESCENAS:      # ritmo de sketch: casi sin aire entre escenas
    _e.setdefault("pre", 0.15)
    _e.setdefault("post", 0.15)
