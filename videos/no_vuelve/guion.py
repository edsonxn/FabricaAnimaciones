# -*- coding: utf-8 -*-
"""No vuelve a pasar — corto (~4 min) para el taller «Bájate de la rueda» sobre el círculo de la violencia
(3.º de secundaria, Jalpa, Zacatecas; mismo público que «La seña»). Estilo pegatina Flow.

Plan completo, intención de cada escena y diapositivas en PLAN_TALLER.md (21-oct-2026).
Narra Diego (14). Los diálogos van con otra voz vía VOZ_POR_FRASE (clave «escena_índice», docs/voz.md).
ElevenLabs: corchetes de actuación en inglés, escritura normal (cifras en número).
Las escenas cortas («clima»/«silencio», «corredor»/«cara») existen para dejar huecos con sonido entre frases:
el frenón de la troca es el «post» de «clima», el golpe a la pared es el «post» de «corredor».
La frase que se repite tres veces (papá → Diego → Xime con las muñecas) es «No vuelve a pasar»; al final cambia de sentido.
"""

TITULO = "No vuelve a pasar"
ESTILO_VISUAL = "pegatina_flow"   # Flow pinta, el código mueve (docs/estilo_pegatina_flow.md)
DURACION = None
BPM = 70

# Voces (biblioteca pública de ElevenLabs, 21-oct-2026; distintas de las de «La seña», que vio el mismo salón)
DIEGO = "OBZYgl3mMau7WE6jCWvm"    # Daniel - Engaging, Warm (mexicano, joven, suave): Diego de 14, el narrador
PAPA = "t6ftGMMsNKPJUzbnYoOU"     # Marvin - Mexican accent (hombre de mediana edad): el papá
LUPE = "akOBlaKhFd59YlK6xz9u"     # Lucia - Warm Conversational (mexicana): la mamá
FER = "WJvDlvlNQAsEW1JX0xFc"      # Barbara - Young, Sweet and Playful (mexicana): Fer, la novia
XIME = "CPv3Zr3CQCqE4ZzuCgBP"     # Lulu - Adorable, Bright & Playful (voz infantil): Xime de 9

VOZ = dict(motor="elevenlabs", voice_id=DIEGO, modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)
VOZ_POR_FRASE = {
    "feria_1": PAPA,
    "silencio_1": PAPA, "silencio_2": LUPE,
    "flores_0": PAPA,
    "fer_1": FER,
    "perdon_2": FER,
    "munecas_0": XIME, "munecas_1": XIME, "munecas_2": XIME,
    "patio_1": LUPE, "patio_3": LUPE,
}
MEZCLA = dict(musica=-20.0, sfx=-22.0, fx=-8.0)
SUBTITULOS = False
ALIAS_QA = {"papa": "apa", "mama": "ama", "jime": "xime", "ximena": "xime", "sel": "cel", "fair": "fer", "tima": "clima"}   # Whisper normaliza el habla
MUSICA = {}

ESCENAS = [
    {"id": "feria", "pre": 2.5, "post": 1.5, "frases": [
        "[warm] De chiquito, mi apá me subía a la rueda de la fortuna… en la feria de Jalpa.",
        "[laughs] ¡Mira, mijo! Desde aquí arriba, todo se ve chiquito.",
        "[thoughtful] Y yo pensaba que mi apá era el hombre más grande del mundo.",
    ]},
    {"id": "clima", "post": 2.4, "frases": [
        "En mi casa aprendimos a leer el clima.",
        "Si la troca de mi apá se estacionaba despacito, era día bueno.",
        "[short pause] Si frenaba duro…",
    ]},
    {"id": "silencio", "post": 1.2, "frases": [
        "[whispers] …mi amá apagaba el radio, y todos hablábamos bajito.",
        "[cold] ¿Otra vez frijoles?",
        "[nervous] Ahorita te hago unos huevitos.",
    ]},
    {"id": "mesa", "pre": 4.5, "post": 3.5, "frases": [
        "[whispers] Cuando se soltaba la tormenta, yo me metía debajo de la mesa con mi hermanita.",
        "[whispers] Le tapaba las orejas… y le cantaba bajito lo que nos cantaba mi amá.",
    ]},
    {"id": "flores", "pre": 1.5, "frases": [
        "[softly] Perdóname, vieja. [short pause] No vuelve a pasar.",
        "Y le traía flores. Y pan. Y a nosotros nos llevaba a la feria.",
        "[sad] Y no volvía a pasar… [long pause] hasta que volvía a pasar.",
    ]},
    {"id": "rueda", "post": 2.0, "frases": [
        "Mi casa era como la rueda de la fortuna.",
        "Subía con flores… arriba, todo bonito… luego bajaba despacito…",
        "y abajo… la tormenta.",
        "Y otra vez para arriba. Cada vuelta, más rápido.",
        "[sad] Y en la pared… cada vez había menos platos.",
    ]},
    {"id": "fer", "pre": 1.5, "frases": [
        "[warm] Ahora tengo 14. Y tengo novia. [happy] Fer.",
        "[laughs] ¡Esa canción no, Diego! ¡Ponle otra!",
        "Al principio le revisaba el cel porque la quería. [short pause] Eso pensaba.",
        "Que los celos eran amor.",
    ]},
    {"id": "corredor", "pre": 1.0, "post": 2.2, "frases": [
        "[angry, shouting] ¿Por qué te ríes con él? ¡¿Eh?!",
    ]},
    {"id": "cara", "post": 1.0, "frases": [
        "[shaky] Fer se tapó la cara. [short pause] Igualito que mi amá.",
    ]},
    {"id": "perdon", "pre": 2.0, "post": 3.0, "frases": [
        "[softly, guilty] Perdóname, Fer. [short pause] No vuelve a pasar.",
        "[whispers] Y lo oí. [short pause] No era mi voz. Era la de mi apá.",
        "[quiet, firm] Eso mismo me dijiste el viernes.",
    ]},
    {"id": "munecas", "pre": 2.0, "post": 2.0, "frases": [
        "[playful, deep voice] ¿Otra vez frijoles?",
        "[sweet] Perdóname, vieja. No vuelve a pasar.",
        "[innocent] ¿Así se juega a los novios, verdad?",
        "[voice breaking] No, Xime. [short pause] Así no.",
    ]},
    {"id": "patio", "pre": 2.0, "post": 3.0, "frases": [
        "[crying] Amá… le grité a Fer. Y le dije lo mismo que mi apá.",
        "[crying softly] ¿Sabes qué, mijo? Tu apá, de chiquito, también se metía debajo de la mesa.",
        "[whispers] ¿Y entonces yo…?",
        "[tender] Tú te diste cuenta, mijo. [short pause] Él nunca.",
    ]},
    {"id": "alba", "pre": 1.0, "post": 2.0, "frases": [
        "Al otro día, toqué la puerta de orientación.",
        "Y esa misma semana, mi amá, mi hermana y yo… [short pause] nos bajamos de la rueda.",
    ]},
    {"id": "epilogo", "pre": 3.0, "post": 6.0, "frases": [
        "[warm] Mira, Xime. Desde aquí arriba, todo se ve chiquito.",
        "[thoughtful] La rueda no se para sola. [short pause] Alguien se tiene que bajar.",
        "[whispers] Conmigo… no vuelve a pasar.",
    ]},
]
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Intimate, heartbreaking score for a short animated film about a boy, his little sister and their mother in a "
            "small Mexican canyon town: a tender lullaby melody (a mother's hummed cradle song) on music box and soft felt "
            "piano, warm nylon-string guitar, later a small string ensemble and cello. A distant small-town fair waltz played by "
            "a brass band for the fair scenes. Tender and nostalgic, never melodramatic; lots of space for dialogue and "
            "narration. No drum kit, no pop, no electronic beats."),
    escenas={
        "feria": ("Night fair memory: a distant small-town brass band waltz, warm and magical, a boy's happiest moment.", 5),
        "clima": ("Domestic dusk: gentle guitar and music box lullaby, then it thins out and stops, waiting.", 3),
        "silencio": ("Tension: almost silence, a single low held cello note, a ticking feeling, no melody.", 3),
        "mesa": ("Under the table: muffled, the lullaby on a fragile music box, very quiet, trembling.", 2),
        "flores": ("Next morning: a sweet but slightly false bright guitar, then a sad piano phrase.", 4),
        "rueda": ("The cycle repeating: the fair waltz returns but keeps speeding up and becomes unsettling, then stops on one note.", 6),
        "fer": ("First love, today: light warm guitar and piano, sweet; then a subtle shadow creeps in.", 4),
        "corredor": ("A shout: the music cuts out abruptly.", 1),
        "cara": ("Shock: a single low piano note and silence.", 2),
        "perdon": ("Realization: a cold low cello drone, the lullaby distorted far away, then silence.", 3),
        "munecas": ("A child's game: the music box lullaby, innocent and heartbreaking.", 3),
        "patio": ("Confession at night: tender piano and strings, the lullaby melody grows, deeply emotional, crying.", 8),
        "alba": ("Dawn, a decision: guitar and strings rise with hope, the lullaby in a major key.", 7),
        "epilogo": ("Hopeful ending at the fair at dusk: the brass-band waltz returns warm and slow, then the lullaby alone on music box, quiet.", 5),
    },
    tramos=[      # Lyria no pasa de ~100 s por pieza (la_sena): 3 tramos de 69, 72 y 93 s
        (["feria", "clima", "silencio", "mesa"],
         "Begin with a distant, warm small-town brass band waltz at a night fair, then a tender music-box lullaby in a kitchen at "
         "dusk that thins out into tense near-silence with one low held cello note, then the lullaby very quiet and trembling "
         "on a lone music box, as if heard from under a table."),
        (["flores", "rueda", "fer", "corredor", "cara"],
         "Begin with a sweet but slightly false bright guitar morning, then the fair waltz returns and keeps speeding up until "
         "it becomes dizzy and unsettling and stops on one note; then a light warm guitar for first love with a subtle shadow; "
         "end with an abrupt cut to silence and one low piano note."),
        (["perdon", "munecas", "patio", "alba", "epilogo"],
         "Begin with a cold low cello drone and the lullaby distorted far away, then the innocent music-box lullaby of a child "
         "playing, then tender piano and strings that grow into a deeply emotional climax built on the lullaby melody, then "
         "hopeful guitar and strings at dawn in a major key, and end with the warm slow fair waltz and the lullaby alone on a "
         "music box, quiet."),
    ],
)


# ── Flow (pegatina Flow): la FICHA y las fichas de personajes viven en _prompts.py (una sola fuente) ──
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _prompts as _PR
FICHA = dict(
    estilo=_PR.FICHA[:-1],
    cierre=" No text, no letters, no watermark.",
    personajes=dict(diego8=_PR.DIEGO8, diego14=_PR.DIEGO14, xime3=_PR.XIME3, xime9=_PR.XIME9, fer=_PR.FER,
                    lupe=_PR.LUPE, papa=_PR.PAPA),
)
