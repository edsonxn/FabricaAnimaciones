# -*- coding: utf-8 -*-
"""«Batman vs. el Guasón (animación fumada)» — video SIN CANAL, motor SECUENCIA con efectos (docs/estilo_secuencia_fx.md).
El audio NO se genera: es el sketch de doblaje improvisado de Sociedad Nokkoi (fuente/sociedad_nokkoi.mp4, 3:00), tal cual.
Estilo pedido por el usuario (7-oct-2026): dibujos exagerados y MAL HECHOS a propósito, como las parodias «Dragon Ball sin
presupuesto / animación fumada» (trazo negro tembloroso tipo MS Paint, fondo casi vacío, caras deformes, color plano a medias).
Los cortes salen de las pausas del audio (`beats`); los golpes, rótulos y SFX, de efectos.py.
"""

TITULO = "Batman vs. el Guasón (animación fumada)"
ARCHIVO = "guason_fumado"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_fx"
AUDIO_EXTERNO = "fuente/sociedad_nokkoi.mp4"     # `tiempo` lo transcribe (voz/transcripcion.json) y `mezcla` lo usa tal cual
DURACION = None
BPM = 100
VOZ = dict(idioma="es")

SECUENCIA = dict(
    video_s=0,          # todo imagen
    img_s=3.2,          # comedia: un dibujo cada ~3 s
    rapido_hasta=9999,
    img_s_lento=3.2,
    fundido=0.0,        # corte seco: es animación «sin presupuesto»
    ambiente=0.0,
)

# Ficha visual: se repite PALABRA POR PALABRA en cada prompt (hacer_prompts.py). Sin nombres de marca: se describen.
FICHA = dict(
    estilo="Intentionally terrible low-budget parody cartoon frame, drawn in MS Paint with a computer mouse by an amateur: "
           "wobbly uneven thick black outlines, crooked anatomy, wildly exaggerated ugly-funny facial expressions, off-model "
           "characters, lazy flat color fills that miss the lines, plain almost empty flat-colored background with a few scribbled details, "
           "crude meme animation style, horizontal 16:9, the drawing is a full-bleed scene whose background color fills the "
           "entire image edge to edge, no white margin, no paper border, no panel frame, no window frame",
    personajes={
        "MURCI": "MURCI, a badly drawn muscular vigilante hero in a dark gray bodysuit with a black pointy-eared cowl mask, "
                 "black cape, a lumpy black bat scribble on his chest, yellow belt, enormous square chin, tiny angry white eyes",
        "PAYASO": "PAYASO, a badly drawn skinny clown villain with a chalk-white face, messy green hair, a huge red lipstick "
                  "grin full of crooked teeth, purple suit with an orange shirt and a green bow tie, bulging crazy eyes",
        "SUPER": "SUPER, a badly drawn huge flying strongman in a bright blue bodysuit with a red cape and red boots, a wobbly "
                 "red-and-yellow diamond shape on his chest, tiny head with one black hair curl, glowing red furious eyes",
        "CHICO": "CHICO, a badly drawn small boy sidekick with a black domino mask, red vest, green shorts and a tiny yellow cape",
    },
    cierre="NO TEXT, no letters, no words, no numbers, no speech bubbles, no logos, no watermark, no blood, no nudity.",
)

TRANSICIONES = []
MUSICA = {}
ESCENAS = [{"id": "audio", "frases": []}]
