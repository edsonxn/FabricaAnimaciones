# -*- coding: utf-8 -*-
"""¿Cómo nació el primer fotón? — Short vertical de ~1 min, estilo BOCETO + GUACHE (pegatinas de boceto sobre fondos pintados a guache).
Canal: Cronopapel/por decidir. Mascota: «Foti», el fotón (cuerpo amarillo con cola ondulada, ojos grandes).

Datos y fuentes (NASA / ESA Planck, CERN, Particle Data Group, Britannica):
  - Big Bang: hace ~13 800 millones de años (Planck 2018: 13,787 ± 0,020).
  - Ruptura de la simetría electrodébil (mecanismo de Higgs): ~1e-12 s tras el Big Bang (T ~ 100 GeV). Los bosones W y Z ganan masa y
    el fotón queda sin masa: aquí el fotón existe como partícula propia. (Antes de eso, los campos que lo forman ya existían, mezclados.)
  - Relación fotones/bariones ~ 1,6e9 (≈ 1 600 millones de fotones por cada protón o neutrón; WMAP/Planck, η ≈ 6e-10): «más de mil millones».
  - Plasma opaco: los fotones se dispersaban con electrones libres (dispersión Thomson) → universo opaco ~380 000 años.
  - Recombinación (z ≈ 1100, T ≈ 3 000 K, t ≈ 380 000 años): electrones se unen a núcleos y el universo se vuelve transparente.
    Esa luz liberada es el fondo cósmico de microondas (CMB), hoy a 2,725 K (microondas, invisibles al ojo).
  - ~411 fotones del CMB por cm³; atraviesan todo, también el cuerpo humano. Una parte de la «nieve» de la TV analógica sintonizada entre
    canales es CMB (alrededor del 1 %; NASA/Penzias y Wilson, 1965).
"""

TITULO = "¿Cómo nació el primer fotón?"
ARCHIVO = "primer_foton_short"
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = 59.0
BPM = 110
GAP = 0.2
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.75, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.0)
ALIAS_QA = {"higs": "higgs", "jigs": "higgs", "hicks": "higgs", "hix": "higgs", "jix": "higgs", "higss": "higgs", "higgz": "higgs",
            "bigbang": "big bang", "bigban": "big bang", "bing bang": "big bang", "big ban": "big bang"}
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 8
MUSICA = {}
LYRIA = dict(
    estilo=("Playful, curious and wonder-filled score for a one-minute animated science short for kids and adults: warm glockenspiel and celesta, "
            "pizzicato strings, soft marimba, a light ticking pulse, tiny synth sparkles, and a gentle bass; a cut-paper, hand-made feel. "
            "Keeps moving, with short stingers at scene changes. Melodies low and sparse so a narrator can speak over it. Instrumental only."),
    escenas={
        "gancho": ("Hook: a curious mysterious rise, sparkling celesta over a ticking pulse, a bright cosmic hit at the end.", 6),
        "calor": ("Silence-then-heat: a hollow low drone, then a rising bubbling boil of marimba and pizzicato, comic tension.", 5),
        "higgs": ("Frantic busy chaos with fast marimba, then a big switch click, heavy slow low brass-like plods for the weights, then a light feather-like flute twirl.", 7),
        "multitud": ("Joyful multiplication: sparkling arpeggios multiplying and stacking up, a wonder-filled swell and a big bright chime.", 7),
        "niebla": ("Trapped and dizzy: pinball-like plucks bouncing around, then a slow sad bass and ticking clock.", 5),
        "libre": ("Cooling down: icy glockenspiel, then warm hugging chords as atoms form, then a huge liberating release and a triumphant whoosh upward.", 8),
        "hoy": ("Quiet cold space travel: soft airy pad and a lonely celesta, then a cozy retro TV hum.", 3),
        "cierre": ("Zooming into static: building tension, then a final bright big-bang chord and sparkles with a magical ending.", 7),
    })

ESCENAS = [
    {"id": "gancho", "pre": 0.35, "frases": [
        "Hay luz del Big Bang atravesándote ahora mismo.",
        "Esta es la historia de cómo nació su primer fotón.",
    ]},
    {"id": "calor", "frases": [
        "Al principio no había luz. Solo un calor imposible y una sopa de partículas.",
    ]},
    {"id": "higgs", "frases": [
        "Una billonésima de segundo después, se encendió el campo de Higgs.",
        "Casi todas las partículas ganaron peso. Pero una no: el fotón.",
    ]},
    {"id": "multitud", "frases": [
        "Y no nació uno solo. Por cada átomo que existe hoy, nacieron más de mil millones de fotones.",
    ]},
    {"id": "niebla", "frases": [
        "Pero el universo era una niebla ardiente, y la luz chocaba con electrones una y otra vez.",
        "Atrapada trescientos ochenta mil años.",
    ]},
    {"id": "libre", "frases": [
        "Hasta que todo se enfrió. Los electrones se unieron a los núcleos, nacieron los átomos, y la niebla se despejó.",
        "Por fin, la luz escapó.",
    ]},
    {"id": "hoy", "frases": [
        "Hoy viaja tan fría que no la ves, pero parte de la estática de una tele vieja es esa luz.",
    ]},
    {"id": "cierre", "post": 1.0, "frases": [
        "La próxima vez que veas estática, estás viendo el Big Bang.",
    ]},
]
