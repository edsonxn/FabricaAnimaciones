# -*- coding: utf-8 -*-
"""NOVELA CON IA · piloto «La muerta en el altar», Capítulo 1 (~92 s, vertical 9:16).
Microdrama telenovelero (investigación en docs/formato_novela_ia.md, 23-oct-2026): herencia + suegra villana + la
amante con el anillo + el regreso de la «muerta», en Día de Muertos. Sin canal todavía (cuenta nueva de TikTok/Facebook).

Motor SECUENCIA en modo SIN_VOZ con `dialogo=True`: cada clip de Flow trae su propio diálogo con labios sincronizados
(no hay narrador). Consistencia: hojas de personaje y del escenario hechas en Flow (imágenes, 0 puntos) pegadas como
ingredientes antes de cada clip, y la ficha de vestuario repetida palabra por palabra en cada prompt.
Presupuesto: 10 clips en 360p (4 de 8 s = 6 pts, 6 de 10 s = 7 pts) = 66 puntos + repeticiones; descarga «720p mejorada».
"""

TITULO = "La muerta en el altar · Capítulo 1"
ARCHIVO = "la_muerta_en_el_altar_cap1"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
SIN_VOZ = True          # sin narrador: el diálogo vive en el audio de cada clip
SUBTITULOS = False
DURACION = 99.0
BPM = 80                # 1 compás = 3 s

SECUENCIA = dict(
    clips_s=[8, 10, 8, 10, 8, 10, 10, 10, 10, 10],  # 94 s (la 6 salió de 10 s)
    video_calidad="360p",
    combinar=False,     # un plano y su diálogo por clip: cortar a mitad de frase rompe el lipsync
    dialogo=True,       # NO añadir «sin diálogo»: los personajes hablan
    fundido=0.0,        # cortes secos, como telenovela
    ambiente=1.0,       # el audio del clip ES el diálogo
    ambiente_por={},
    carpeta_descargas="flow-novela_altar",
)

# Ficha visual: se repite PALABRA POR PALABRA en cada prompt donde aparezca (y las hojas van de ingrediente).
FICHA = dict(
    estilo="Vertical nine by sixteen shot from a modern prestige Mexican telenovela, photorealistic live action, shot on "
           "ARRI Alexa with a 35mm lens, shallow depth of field, warm flickering candlelight with deep shadows, rich orange "
           "marigold and purple Day of the Dead colors, natural skin texture, subtle film grain, dramatic soap opera acting",
    personajes={
        "ximena": "a 32-year-old Mexican woman with warm brown skin, long dark wavy hair loose and tangled, "
                  "almond-shaped dark eyes, a white gauze bandage on the left side of her forehead, a faint healing scratch "
                  "on her cheek, wearing a dusty torn mustard-yellow knit cardigan over a cream blouse and dark jeans, "
                  "a small gold Virgin of Guadalupe medal on a thin chain",
        "mauricio": "a 35-year-old Mexican man, short black hair combed back with gel, neatly trimmed black beard, "
                    "black slim dress shirt with the top button open, silver wristwatch",
        "refugio": "a stout 62-year-old Mexican woman, grey hair pulled into a tight bun, thick dark eyebrows, "
                   "gold hoop earrings, a black mourning dress with a white lace collar, a black rebozo shawl over her "
                   "shoulders, a wooden-bead rosary wrapped around her hand, stern face",
        "daniela": "a slim 28-year-old woman with long straight dyed honey-blonde hair, red lipstick, a tight red "
                   "satin dress, gold bangles, and on her ring finger a gold wedding ring with three small diamonds",
        "sofi": "a 6-year-old Mexican girl with two dark braids tied with orange marigold ribbons, half of her face "
                "painted as a little sugar-skull catrina, a white cotton dress with colorful embroidered flowers",
    },
    nombres={"ximena": "Ximena", "mauricio": "Mauricio", "refugio": "Doña Refugio", "daniela": "Daniela", "sofi": "Sofi"},
    objetos={
        "foto": "The photo is a framed portrait of Ximena smiling in a yellow sundress, in a carved wooden frame",
        "anillo": "The ring is a gold wedding ring with three small diamonds",
        "sobre": "The envelope is a white insurance company envelope with a printed check sticking out",
        "dibujo": "The drawing is a child's crayon drawing of a mother and a little girl holding hands among orange "
                  "marigolds",
    },
    epoca="the living room of a traditional family house in Guadalajara, Mexico, on the night of the Day of the Dead, "
          "today: a three-tier ofrenda altar covered with orange cempasúchil marigolds, purple and orange papel picado, "
          "dozens of lit candles, sugar skulls, pan de muerto and copal smoke, terracotta tile floor, an arched doorway "
          "open to an inner courtyard with a stone fountain and potted plants",
    cierre="No on-screen text, no subtitles, no captions, no logos, no watermark. Only the spoken lines written here, "
           "clear Mexican Spanish accent, no background music.",
)

# Un clip por plano. `dialogo` = (personaje, tono, línea) -> «X says in Mexican Spanish, <tono>: "…"».
PLANOS = [
    dict(clip=1, personajes=["ximena"], objetos=["foto"],
         a="Extreme close-up of the photo of Ximena standing in the center of the ofrenda between flickering candles and "
           "marigolds; a trembling hand with dirty fingernails and a scraped knuckle enters the frame and slowly lifts "
           "the photo; the camera tilts up to Ximena's shocked face lit by the candles, a tear running down her cheek.",
         dialogo=[("ximena", "in a shaky whisper", "¿Por qué está mi foto en el altar?")]),
    dict(clip=2, personajes=["refugio", "mauricio", "daniela"],
         a="Medium shot from behind the candles of the ofrenda: Doña Refugio kneels praying with her rosary, eyes half "
           "closed; behind her, Mauricio and Daniela stand holding hands; Daniela hides a smirk.",
         dialogo=[("refugio", "with false solemnity, then correcting herself",
                   "Que Dios la tenga lejos… digo, en su santa gloria.")]),
    dict(clip=3, personajes=["ximena"],
         a="Ximena hides behind the half-open wooden door of the inner courtyard at night, her face half in shadow and "
           "half lit by orange candlelight from the living room; she presses her hand over her mouth to hold back a sob.",
         dialogo=[("ximena", "in a broken whisper to herself",
                   "Tres meses en esa barranca… y ni siquiera me buscaron.")]),
    dict(clip=4, personajes=["refugio", "mauricio", "daniela"], objetos=["sobre", "anillo"],
         a="At the dining table next to the ofrenda, Doña Refugio pulls the envelope out of her black dress and waves the "
           "check in front of Mauricio with greedy eyes; Daniela lifts her hand to show off the ring, smiling.",
         dialogo=[("refugio", "greedy and proud", "Dos millones del seguro, mijo. Ahora sí, la casa es tuya."),
                  ("daniela", "sweet and venomous", "Y mía, suegrita.")]),
    dict(clip=5, personajes=["ximena", "daniela"], objetos=["anillo"],
         a="Close-up through the doorway: Ximena's eyes fill with tears as she stares; reverse close-up of the ring "
           "sparkling on Daniela's finger in the candlelight; back to Ximena clenching her jaw.",
         dialogo=[("ximena", "barely audible, devastated", "Mi anillo…")]),
    dict(clip=6, personajes=["ximena"],
         escenario="a dark two-lane mountain road with sharp curves above a deep wooded ravine near Tapalpa, Jalisco, at "
                   "night, three months earlier",
         a="Flashback with cold desaturated blue tones: at night Ximena drives a small car on a winding mountain road "
           "above a deep ravine near Tapalpa, a phone on speaker on the dashboard; she presses the brake pedal again and "
           "again but the car does not slow down, headlights sweeping a sharp curve.",
         dialogo=[("mauricio", "calm voice from the phone speaker", "¿Ya vas por la curva de la barranca?"),
                  ("ximena", "panicking", "¡No frena… Mauricio, no frena!")]),
    dict(clip=7, personajes=["sofi"], objetos=["dibujo"],
         a="Sofi walks up to the ofrenda holding the drawing and a round pan de muerto, places them carefully under the "
           "photo frame, and looks up at the empty frame spot with big hopeful eyes.",
         dialogo=[("sofi", "softly, with a small sad smile", "Mami, te traje tu pan de muerto. Ya vuelve, ¿sí?")]),
    dict(clip=8, personajes=["refugio", "sofi"], objetos=["dibujo"],
         a="Doña Refugio snatches the drawing from the ofrenda and crumples it in her fist in front of Sofi; Sofi bursts "
           "into tears and shouts back; Doña Refugio raises her open hand threateningly over the girl.",
         dialogo=[("refugio", "cold and cruel", "Ya deja de llorarle a esa. Tu nueva mamá es Daniela."),
                  ("sofi", "crying and shouting", "¡No es mi mamá!")]),
    dict(clip=9, personajes=["ximena", "refugio", "mauricio", "daniela"],
         a="A hand with a scraped knuckle grabs Doña Refugio's raised wrist mid-air; a gust of wind blows out all the "
           "candles of the ofrenda at once, petals fly; everyone turns: Ximena stands there in the doorway, bandaged; "
           "Doña Refugio turns pale and crosses herself, Daniela drops her wine glass, Mauricio freezes.",
         dialogo=[("refugio", "screaming in terror", "¡Jesús, María y José!")]),
    dict(clip=10, personajes=["ximena", "mauricio"],
         a="Slow push-in on Ximena's face lit only by the smoking candle wicks and moonlight, cold and calm, staring at "
           "Doña Refugio; then a quick cut to Mauricio, pale and sweating, looking down at his phone screen as it lights "
           "up his face.",
         dialogo=[("ximena", "slow, icy and calm",
                   "Tranquila, suegra. Los muertos venimos una noche… pero yo me voy a quedar.")]),
]

# Rótulos por código (énfasis, no subtítulos): título, el mensaje del celular y el gancho al capítulo 2.
ROTULOS = [
    dict(t=0.3, dur=2.6, texto="LA MUERTA EN EL ALTAR\nCapítulo 1"),
    dict(t=91.6, dur=3.0, texto="«¿Ya confirmaste que no sobrevivió?»"),
    dict(t=94.2, dur=4.8, texto="Capítulo 2:\n¿Quién cortó los frenos?"),
]

LYRIA = dict(
    estilo="Mexican telenovela dramatic score: lush strings, solo piano, soft nylon guitar and a distant Day of the Dead "
           "choir, slow tempo 80 BPM, cinematic and melodramatic, mixed low under dialogue.",
    escenas={
        "gancho": ("A single eerie low string note and a fragile music-box-like piano motif, suspenseful.", 3),
        "traicion": ("Tense pizzicato strings and a dark piano ostinato, growing anger and injustice.", 12),
        "flashback": ("Cold reverberant piano and a rising string tremolo that ends in a sudden silence.", 3),
        "nina": ("Heartbreaking tender theme on solo piano and nylon guitar, then stabbing strings when the "
                 "grandmother turns cruel.", 6),
        "climax": ("A huge orchestral hit with choir, then a slow ominous drone and one final dramatic sting.", 7),
    },
    tramos=[(["gancho", "traicion", "flashback", "nina", "climax"],
             "Keep it as a bed under dialogue; end on the final sting.")],
)

MEZCLA = dict(musica=-22.0)   # la música va bajo el diálogo de los clips
TRANSICIONES = [("corte", 0.0)] * 6
MUSICA = {"gancho": dict(sabor="tension"), "traicion": dict(sabor="tension"), "climax": dict(sabor="tension")}

ESCENAS = [   # secciones musicales (SIN_VOZ): 33 compases = 99 s
    {"id": "gancho", "compases": 3, "frases": []},       # clip 1: la foto en el altar
    {"id": "traicion", "compases": 12, "frases": []},    # clips 2-5: suegra, seguro, anillo
    {"id": "flashback", "compases": 3, "frases": []},    # clip 6: los frenos
    {"id": "nina", "compases": 6, "frases": []},         # clips 7-8: Sofi
    {"id": "climax", "compases": 9, "frases": []},       # clips 9-10: la muerta vuelve
]
