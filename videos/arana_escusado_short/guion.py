# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `arana_escusado` («What Happens to a Spider You Flush Down the Toilet?»).
Regla de la tanda (22-oct-2026): cada largo lleva su Short de 30-45 s, publicado ~12 h después, con «Vídeo relacionado» =
su largo (Studio, cuando el largo ya sea público). Hechos y fuentes: docstring de videos/arana_escusado/guion.py.
Imágenes NUEVAS de Flow en 9:16 (mismas fichas que el largo; 0 puntos). Voz EnglishComic.
"""

TITULO = "What Happens to a Spider You Flush? #Shorts"
ARCHIVO = "spider_flush_short"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160                 # bloques de 1,5 s: sin silencios largos entre escenas
GAP = 0.18
LARGO = dict(video="arana_escusado", id="WQu7K19q7u8")   # el Short enlaza a este video (id al subir el largo)
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=0,
    clip_s=8,
    img_s=2.6,               # Short: cortes muy rápidos
    rapido_hasta=300,
    img_s_lento=2.6,
    fundido=0.15,
    ambiente=0.0,
    ambiente_por={},
    carpeta_descargas="flow-arana_escusado_short",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, vertical nine by sixteen composition with the main subject large in the center, full-bleed "
           "scene that fills the entire frame edge to edge, no border, no frame, no vignette",
    personajes={
        "spider": "a cartoon brown house spider with a round tan abdomen marked with dark brown chevrons, a small brown "
                  "head with two big round worried eyes, eight thin legs with light and dark bands, and a tiny blue and "
                  "white striped nightcap with a white pom-pom",
        "human": "a simple cartoon man with a round white head, dot eyes, messy hair, a green bathrobe and fuzzy slippers",
    },
    objeto="a plain white porcelain toilet with a white tank and a silver flush handle, in a small tidy bathroom with "
           "light blue tiles, a fluffy bath mat and a roll of toilet paper",
    epoca="present-day American home bathroom at night, warm yellow light",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo="Playful, curious cartoon score about a tiny house spider swept into the plumbing: pizzicato strings, marimba, "
           "bassoon, celesta, light brushed percussion. Comic suspense. Instrumental only, never loud under the voice.",
    escenas={},
    tramos=[(["flush", "ride", "coma", "cierre"],
             "Start instantly with a comic gulp and swirling marimba, a quick water-slide chase, a magical wake-up sparkle, "
             "then a warm resolved ending that fades out.")],
)

ESCENAS = [
    {"id": "flush", "pre": 0.1, "frases": [
        "You flush a spider. Whoosh. Gone.",
        "But where does it actually go? And can it come back up?",
    ]},
    {"id": "ride", "frases": [
        "First, it shoots through the toilet's water trap. The biggest water slide on Earth, in total darkness.",
        "Tiny water-repelling hairs wrap it in a bubble of air, so it can float.",
    ]},
    {"id": "coma", "frases": [
        "And drowning is slow. Scientists kept spiders underwater for sixteen hours. They looked dead.",
        "Then they dried off, and walked away.",
    ]},
    {"id": "cierre", "post": 0.6, "frases": [
        "Can it climb back up? Almost certainly not. The water in the trap stops it.",
        "So next time, skip the flush. A cup and a piece of paper does the job.",
    ]},
]
