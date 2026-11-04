# -*- coding: utf-8 -*-
"""Plastitube (alias pieza_oculta) — Short vertical de `sopa_instantanea`. Fórmula del canal (canales/formula/pieza_oculta.md):
cada largo lleva su Short de 40-60 s, con «Vídeo relacionado» = el largo. Hechos y fuentes: docstring de
videos/sopa_instantanea/guion.py (quiebra de la cooperativa en 1957 con 47 años; cobertizo en Ikeda casi un año; la tempura de su
esposa Masako; fideos fritos con poros que se ablandan en un par de minutos; Chicken Ramen el 25-ago-1958; WINA 2024: 123 070
millones de porciones). Imágenes NUEVAS de Flow en 9:16 con las mismas fichas del largo (la esposa con la ficha que pasa el filtro
de Flow: «cheerful plasticine housewife figure», hallazgo del largo); voz Dan."""

TITULO = "La Sopa Instantánea Nació Mirando a su Esposa Freír TEMPURA #Shorts"
ARCHIVO = "sopa_short"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 150
GAP = 0.18
LARGO = dict(video="sopa_instantanea", id="iJ7QsuU1nUA")
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

FONETICA = {"Momofuku Ando": "Momofúku Ándo", "Ando": "Ándo", "Masako": "Masáko", "tempura": "tempúra"}

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-sopa_short")

# Mismas fichas que el largo (videos/sopa_instantanea/guion.py), en vertical.
FICHA = dict(
    estilo="Cinematic vertical nine-by-sixteen diorama made entirely of handmade stop-motion plasticine clay, matte texture "
           "with visible fingerprints, warm window light, full-bleed scene that fills the entire frame edge to edge, no border, "
           "no frame, no vignette, the main subject large in the center with space above and below",
    personajes={
        "inventor": "a plasticine Japanese man about forty-eight years old, slim, with short black hair combed back, round "
                    "black-rimmed glasses, a white short-sleeved shirt with the sleeves rolled up, dark gray trousers and a "
                    "plain white cloth apron",
        "esposa": "a cheerful plasticine housewife figure with black hair in a low bun, a simple pale blue 1950s blouse, a dark "
                  "skirt and a white kitchen apron",
    },
    objeto="a block of wavy golden fried plasticine noodles, square and crinkled, with tiny holes; a deep black iron frying "
           "pan of bubbling oil",
    epoca="a small wooden shed in the backyard of a modest 1950s house in Ikeda, near Osaka, Japan: wooden walls, a bare light "
          "bulb, a second-hand cast-iron noodle-making machine with a hand crank, a gas burner, flour sacks without letters, "
          "bamboo baskets; and the small 1950s Japanese home kitchen next to it; no plastic packaging, no modern appliances",
    cierre="No text, no letters, no numbers or digits anywhere, no logos, no brand packaging, no modern objects.",
)

TRANSICIONES = [("continua", 0.1)] * 3
MUSICA = {"hook": dict(sabor="tension"), "ruina": dict(sabor="vacio"), "tempura": dict(sabor="esperanza"),
          "cierre": dict(sabor="esperanza")}

LYRIA = dict(
    estilo="Warm handmade documentary score for a stop-motion short about a ruined man who invents instant noodles in his "
           "backyard: koto plucks, shakuhachi breath, marimba, soft taiko pulse, pizzicato strings and upright bass. Curious, "
           "intimate, then hopeful. Instrumental only, never loud under the voice.",
    escenas={},
    tramos=[(["hook", "ruina", "tempura", "cierre"],
             "Start instantly with a curious plucked koto hook, sink into a sparse lonely passage, then a bubbling marimba "
             "rhythm like hot oil that builds into a warm, hopeful ending that fades out.")],
)

ESCENAS = [
    {"id": "hook", "pre": 0.1, "frases": [
        "La sopa instantánea nació en una cocina, mirando a una mujer freír tempura.",
    ]},
    {"id": "ruina", "frases": [
        "En mil novecientos cincuenta y siete, Momofuku Ando lo había perdido todo.",
        "Tenía cuarenta y siete años, y solo le quedaba su casa.",
        "En el patio construyó un cobertizo de madera.",
        "Y durante casi un año, cada intento terminó en la basura.",
    ]},
    {"id": "tempura", "frases": [
        "Hasta que una noche vio a su esposa Masako freír tempura.",
        "El aceite hirviendo sacaba el agua de la masa, y dejaba miles de hoyitos.",
        "Ando frió un bloque de fideos. Quedaron secos, y llenos de poros.",
        "Con agua hirviendo, en un par de minutos estaban blandos otra vez.",
    ]},
    {"id": "cierre", "post": 0.6, "frases": [
        "Hoy se comen más de ciento veinte mil millones de porciones al año.",
        "Y cómo la hicieron famosa unos policías en la nieve, está en el video relacionado.",
    ]},
]
