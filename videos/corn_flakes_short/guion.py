# -*- coding: utf-8 -*-
"""Plastitube (alias pieza_oculta) — Short vertical de `corn_flakes`. Fórmula del canal (canales/formula/pieza_oculta.md, 23-oct-2026):
cada largo lleva su Short de 40-60 s al día siguiente, con «Vídeo relacionado» = el largo. Hechos y fuentes: docstring de
videos/corn_flakes/guion.py (accidente de agosto de 1894, patente de 1896, azúcar y compañía de Will en 1906, Suprema Corte de
Michigan en 1920). Imágenes NUEVAS de Flow en 9:16 con las mismas fichas del largo; voz Dan."""

TITULO = "Los Corn Flakes Nacieron de un Trigo OLVIDADO #Shorts"
ARCHIVO = "corn_flakes_short"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video="corn_flakes", id="4GLQgAKPQBg")
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

FONETICA = {"Kellogg": "Kélog", "Corn Flakes": "Corn Fléiks"}

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-corn_flakes_short")

# Mismas fichas que el largo (videos/corn_flakes/guion.py), en vertical.
FICHA = dict(
    estilo="Cinematic vertical nine-by-sixteen diorama made entirely of handmade stop-motion plasticine clay, matte texture "
           "with visible fingerprints, warm window light, full-bleed scene that fills the entire frame edge to edge, no border, "
           "no frame, no vignette, the main subject large in the center with space above and below",
    personajes={
        "medico": "a plasticine doctor about forty-five years old, short and stocky, with short brown hair, a thick mustache and "
                  "a short goatee, round gold-rimmed glasses, an all-white three-piece suit and a white tie",
        "contador": "a plasticine bookkeeper about thirty-five years old, thin and serious, with short brown hair parted on the "
                    "side, a thick mustache and small round metal-rimmed glasses, a charcoal gray suit with vest, a black bow "
                    "tie, holding a small notebook",
        "empresario": "a plasticine businessman about fifty years old, thin and serious, with short graying hair parted on the "
                      "side, a thick gray mustache and small round metal-rimmed glasses, a charcoal gray three-piece suit and a "
                      "black bow tie",
    },
    objeto="thin wavy golden plasticine cereal flakes, toasted at the edges; and a machine with two steel rollers and an iron "
           "hand crank, no electric motor",
    epoca="experimental kitchen of an 1890s health sanitarium in Michigan: cast-iron stoves, copper pots, wooden tables, glass "
          "jars of grain, gas lamps; no plastic, no modern cereal boxes, no electric appliances",
    cierre="No text, no letters, no numbers or digits anywhere, no logos, no modern objects.",
)

TRANSICIONES = [("continua", 0.1)] * 6
MUSICA = {"hook": dict(sabor="tension"), "olla": dict(sabor="espacio"), "pelea": dict(sabor="tension"),
          "cierre": dict(sabor="esperanza")}

LYRIA = dict(
    estilo="Playful handmade documentary score for a stop-motion short about an accidental breakfast and two feuding brothers: "
           "pizzicato strings, marimba, a touch of old ragtime piano, glockenspiel and upright bass. Quick, curious and warm. "
           "Instrumental only, never loud under the voice.",
    escenas={},
    tramos=[(["hook", "olla", "pelea", "cierre"],
             "Start instantly with a curious plucked hook, a bouncy ragtime pulse under the voice, a tense little turn in the "
             "middle, then a warm resolved ending that fades out.")],
)

ESCENAS = [
    {"id": "hook", "pre": 0.1, "frases": [
        "Los Corn Flakes nacieron de una olla de trigo que alguien olvidó.",
    ]},
    {"id": "olla", "frases": [
        "En mil ochocientos noventa y cuatro, dos hermanos cocían trigo en la cocina de un sanatorio.",
        "Tuvieron que salir, y el trigo se quedó reposando durante horas.",
        "Cuando volvieron, estaba duro y rancio. Lo pasaron por los rodillos de todos modos.",
        "Y en lugar de masa, salieron hojuelas.",
    ]},
    {"id": "pelea", "frases": [
        "El hermano mayor, médico, las quería sin azúcar.",
        "El menor les puso azúcar, fundó su propia empresa, y se hizo millonario.",
        "Terminaron peleando por su apellido hasta la Suprema Corte.",
    ]},
    {"id": "cierre", "post": 0.6, "frases": [
        "Ese apellido, Kellogg, sigue en tu caja de cereal.",
        "La historia completa está en el video relacionado.",
    ]},
]
