# -*- coding: utf-8 -*-
"""SHORT vertical de Cuerpo en Neón (23-oct-2026), derivado de `despertar_3am` (fórmula nueva: un Short por largo, una
sola idea, ~45 s, «video relacionado» = el largo). Idea: por qué a las 3 de la mañana todo parece peor («The Mind After
Midnight»). Hechos y fuentes: ver el docstring de videos/despertar_3am/guion.py (Tubbs et al. 2022).
Las frases marcadas «toma de …» reutilizan la toma de voz del largo (copiada a voz/cands); las «nueva» se piden a ElevenLabs.
Las imágenes son las del largo reencuadradas a 9:16: ver `medios_del_largo.py` y docs/estilo_linea_neon.md § «Shorts derivados».
"""

TITULO = "¿Por qué a las 3 de la mañana todo parece peor?"
ARCHIVO = "despertar_3am_short"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160                 # solo cuantiza la línea de tiempo (lección de short_suspiro)
GAP = 0.16
LARGO = dict(video="despertar_3am", id="xnRw-_gBtMs")   # el Short enlaza a este video (video relacionado); id al subir el largo

CER_MAX_POR_FRASE = {}
TAIL_MAX_POR_FRASE = {}
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    video_s=0,                # todo imagen: medios del largo reencuadrados (sin gastar puntos de Flow)
    img_s=3.2,
    rapido_hasta=300,
    img_s_lento=3.2,
    fundido=0.25,
    ambiente=0.0,
    ambiente_por={},
)

FICHA = dict(estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined in glowing bright yellow neon light with a soft golden glow; vertical nine by sixteen composition, full-bleed scene that fills the entire frame edge to edge, no border, no frame", personajes={}, objeto="", epoca="",
             cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.")

TRANSICIONES = [("continua", 0.1)] * 20

LYRIA = dict(
    estilo="Calm nocturnal ambient score for a science explainer drawn in white chalk lines on black with glowing neon: soft felt piano, a music-box, slow pads, a faint clock tick. Instrumental only, no vocals, never loud.",
    escenas={
        "gancho": ("Awake at 3 a.m.: a single soft piano note and a ticking clock.", 2),
        "mente": ("Dark looping thoughts: a minor piano figure that loops, slightly uneasy, then calmer.", 5),
        "cierre": ("Morning light: a soft warm piano phrase and a final gentle chord.", 2),
    },
    tramos=[(["gancho", "mente", "cierre"], "Begin with a ticking clock and one piano note, grow a little uneasy, end with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.3, "frases": [
        "[curious] ¿Por qué a las 3 de la mañana todo parece peor?",   # nueva
    ]},
    {"id": "mente", "frases": [
        "Ya estás despierto, y empieza lo peor: la cabeza. Las deudas, la salud, los hijos, aquella frase que dijiste hace años.",   # toma de despertar_3am:mente_1
        "[thoughtful] A esa hora, todo parece más grave. Y tiene explicación.",   # toma de despertar_3am:mente_2
        "En 2022, investigadores de Harvard y Arizona propusieron una idea: la mente despierta después de la medianoche se inclina hacia lo negativo.",   # toma de despertar_3am:mente_3
        "La parte del cerebro que pone freno y perspectiva está cansada, y el cuerpo está programado para dormir, no para pensar.",   # toma de despertar_3am:mente_4
        "[short pause] Por eso, un problema a las 3 de la mañana parece un abismo. Y a las 9, con luz, es solo un pendiente.",   # toma de despertar_3am:mente_5
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "[thoughtful] Y por qué tu cuerpo te despierta justo a esa hora, y cómo volver a dormir, te lo cuento en el video completo.",   # nueva
    ]},
]
