# -*- coding: utf-8 -*-
"""La seña — corto (~4 min) para el taller «Antes de decir que sí» (3.º de secundaria, Jalpa, Zacatecas). Estilo pegatina Flow.

Guion aprobado por el usuario el 20-oct-2026; plan completo, intención de cada escena y diapositivas en PLAN_TALLER.md.
Narra Ángel (14). Los diálogos van con otra voz vía VOZ_POR_FRASE (clave «escena_índice», docs/voz.md).
ElevenLabs: corchetes de actuación en inglés, escritura normal (cifras en número).
Los silencios con música van en «pre»/«post» de la escena: la gotera (sin voz) es el «pre» de «bendicion»;
el vals, el certificado y la reja son el «pre» de «graduacion»; el negro de 3 s es su «post».
"""

TITULO = "La seña"
ESTILO_VISUAL = "pegatina_flow"   # Flow pinta, el código mueve (docs/estilo_pegatina_flow.md)
DURACION = None
BPM = 70

# Voces (biblioteca pública de ElevenLabs, 20-oct-2026)
ANGEL = "p7cwnUviDFhhX9y8sG2Q"    # Sebastian - Lively Teenager (latinoamericano): Ángel de 14, el narrador
TONO13 = "I1n8B4pOly0qmOu46LFX"   # Alejandro - Energic & Friendly (mexicano, joven): Toño de 13, un grito
TONO = "7uSWXMmzGnsyxZwYFfmK"     # Alexander-Clear - Warm and Young (mexicano): Toño de 19
ROSA = "0TMU0XAYky7JI2rdHId5"     # Laura D - Expressive & Friendly (mexicana, emotiva): la mamá
PAPA = "2Vpgw9VLLMQfZcOYVGxD"     # Carlos Mestre - hombre mexicano de mediana edad: el papá

VOZ = dict(motor="elevenlabs", voice_id=ANGEL, modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)
VOZ_POR_FRASE = {
    "cuesta_3": TONO13,
    "puerta_1": PAPA,
    "azotea_2": TONO, "azotea_3": TONO, "azotea_5": TONO, "azotea_6": ROSA,
    "bendicion_0": ROSA,
    "mensaje_0": TONO, "mensaje_2": TONO, "mensaje_3": TONO,
}
MEZCLA = dict(musica=-20.0, sfx=-22.0, fx=-8.0)
SUBTITULOS = False
ALIAS_QA = {"papa": "apa", "mama": "ama", "seku": "secu", "pues": "pos"}   # Whisper normaliza el habla del rancho
MUSICA = {}

ESCENAS = [
    {"id": "cuesta", "pre": 2.0, "post": 3.0, "frases": [
        "[thoughtful] Mi carnal me enseñó a andar en bici… en la cuesta de la casa.",
        "Me soltó sin avisarme.",
        "Cuando volteé, ya no me estaba agarrando… [short pause] pero seguía ahí.",
        "[shouts] ¡¿Ya ves, menso?! ¡Sí podías!",
        "Ese día inventamos la seña: dos dedos a los ojos… [short pause] y luego a ti.",
        "Quiere decir: te estoy viendo.",
    ]},
    {"id": "puerta", "frases": [
        "[sad] Ese mismo año, mi apá se fue al norte.",
        "[whispers] Te encargo a tu amá y a tu hermano, mijo.",
        "Toño tenía 13. [short pause] Desde esa noche, el que se quedó en la puerta… fue él.",
    ]},
    {"id": "azotea", "post": 8.0, "frases": [
        "Ahora Toño tiene 19. Trabaja en la obra de lunes a sábado.",
        "Casi todo lo que gana es para la casa. [sighs] Mi apá cada vez manda menos.",
        "Yo me salí en segundo de secu. [short pause] Tú no, ¿eh?",
        "Tú vas a ser el primero de esta casa con papel.",
        "¿Y si no, qué?",
        "[laughs] Pos te vuelvo a soltar en la cuesta.",
        "[shouts] ¡Ya bájense a cenar, que se enfría!",
    ]},
    {"id": "bendicion", "pre": 24.0, "frases": [
        "[whispers] Que Diosito te acompañe, mijo.",
        "Dijo que era una chamba en Jalisco. [short pause] Que pagaban bien.",
    ]},
    {"id": "tenis", "post": 3.0, "frases": [
        "Regresaba de vez en cuando. Con tenis nuevos.",
        "Ya no se mojaba la cocina.",
        "[sad] Pero ya no se reía igual… [short pause] y siempre se sentaba viendo a la puerta.",
    ]},
    {"id": "mensaje", "pre": 7.0, "frases": [
        "[serious] Tú no. ¿Me oíste? [short pause] Tú no.",
        "[angry] ¿Y por qué tú sí?",
        "[sad] Porque yo ya no me puedo regresar.",
        "[whispers] Tú vas a ser el primero con papel. [short pause] Me lo prometiste.",
    ]},
    {"id": "recamara", "pre": 2.5, "frases": [
        "Al otro día ya no estaba.",
    ]},
    {"id": "graduacion", "pre": 20.0, "post": 4.0, "frases": [
        "[sad] Cuando volteé… ya no me estaba agarrando.",
        "[whispers] Pero seguía ahí.",
    ]},
    {"id": "epilogo", "pre": 6.0, "post": 5.0, "frases": [
        "[thoughtful] Ahora me toca a mí.",
    ]},
]
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Intimate, heartbreaking score for a short animated film about two brothers in a poor small town in a dry canyon: "
            "a gentle whistled four-note motif, warm nylon-string folk requinto guitar, soft felt piano, later a small string "
            "ensemble and cello. Tender and nostalgic, never melodramatic; lots of space so dialogue and narration sit on top. "
            "No drum kit, no pop, no electronic beats."),
    escenas={
        "cuesta": ("Golden childhood memory: a boy whistles a simple four-note motif, answered by a warm solo guitar, light and playful.", 4),
        "puerta": ("Night farewell: the same motif slowed on solo guitar, crickets-like quiet, a soft low piano note, sadness.", 3),
        "azotea": ("Warm sunset with brothers laughing: guitar and soft piano, gentle rhythm, the happiest moment of the film.", 5),
        "bendicion": ("Rainy night then dawn: near silence (only room tone) for the first seconds, then a fragile piano and the motif on guitar, worried farewell.", 2),
        "tenis": ("Something is wrong: guitar with one held dissonant note, uneasy but restrained, no horror.", 3),
        "mensaje": ("Rooftop at night, confrontation: low cello drone rising, the music breaks off for a silence, then a tender broken piano.", 6),
        "recamara": ("Empty bed at dawn: a single sustained cello note and a lonely piano phrase.", 2),
        "graduacion": ("Graduation waltz turning into emotion: a slow simple small-town folk waltz on guitar and strings, then the whistled motif returns on full strings and swells, then silence.", 9),
        "epilogo": ("Hopeful ending: the four-note motif whistled alone, then a soft guitar chord, warm and quiet.", 4),
    },
    tramos=[      # Lyria no pasa de ~100 s con este pedido: 3 tramos (20-oct)
        (["cuesta", "puerta", "azotea"],
         "Begin from near silence with the whistled four-note motif. Childhood warmth, a night farewell, then the happiest "
         "sunset; end softly as the sun goes down."),
        (["bendicion"],
         "A rainy night: almost silence, only a very soft low drone for the first twenty seconds, then a fragile piano and the "
         "whistled motif on guitar at dawn, a worried farewell, ending on a held note."),
        (["tenis", "mensaje", "recamara", "graduacion", "epilogo"],
         "Begin uneasy and restrained, rise to a confrontation that breaks into silence, a lonely cello, then the slow folk "
         "waltz that swells into the full-strings return of the whistled motif, a moment of total silence, and the motif "
         "whistled alone to close."),
    ],
)


# ── Flow (pegatina Flow): la FICHA y las fichas de personajes viven en _prompts.py (una sola fuente) ──
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _prompts as _PR
FICHA = dict(
    estilo=_PR.FICHA[:-1],
    cierre=" No text, no letters, no watermark.",
    personajes=dict(angel8=_PR.ANGEL8, tono13=_PR.TONO13, angel14=_PR.ANGEL14, angel_grad=_PR.ANGEL_GRAD,
                    tono19=_PR.TONO19, tono19b=_PR.TONO19B, rosa=_PR.ROSA, papa=_PR.PAPA),
)
