# -*- coding: utf-8 -*-
"""SHORT vertical de Cuerpo en Neón (21-oct-2026, pedido del usuario: un Short por video largo, una técnica, ~45 s, con
«video relacionado» al largo). Short derivado de `estres_cuerpo` (lugar 3: la quijada; la posición de descanso). Fuentes: ver docstring de videos/estres_cuerpo/guion.py.
Las frases marcadas «toma de …» reutilizan la toma de voz del largo (copiada a voz/cands); las «nueva» se piden a ElevenLabs.
Las imágenes son las del largo reencuadradas a 9:16 (recorte centrado en el neón + fundido a negro arriba y abajo):
ver `medios_del_largo.py` y docs/estilo_linea_neon.md § «Shorts derivados».
"""

TITULO = "¿Tus dientes se están tocando ahora mismo?"
ARCHIVO = "short_dientes"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160                 # solo cuantiza la línea de tiempo: bloques de 1,5 s (con 80 sobraban hasta 3 s de silencio por escena)
GAP = 0.16
LARGO = dict(video="estres_cuerpo", id="rdzUobc1UAM")   # el Short enlaza a este video (video relacionado)

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

TRANSICIONES = [("continua", 0.1)] * 30

LYRIA = dict(
    estilo="Calm modern science-explainer score drawn in white chalk lines on black with glowing yellow neon: warm analog pads, soft felt piano, light pulsing bass. Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "prueba": ("Curious and playful: a light plucked motif that asks a question, a soft tick.", 2),
        "tension": ("Tight and tense: a muted pulsing bass, clenched, a little uneasy.", 3),
        "truco": ("Release: the tension opens into warm pads and a relaxed piano melody.", 4),
        "cierre": ("Warm resolution: a final soft chord fading to silence.", 2),
    },
    tramos=[(["prueba", "tension", "truco", "cierre"], "Begin curious, tighten with a tense pulse, release into warm calm pads, end fading to silence.")])

ESCENAS = [
    {"id": "prueba", "pre": 0.2, "frases": [
        "Haz una prueba ahora mismo. ¿Tus dientes se están tocando? ¿Tus hombros están cerca de tus orejas?",   # toma de estres_cuerpo:mandibula_1
        "[short pause] Si dijiste que sí, no eres el único.",   # toma de estres_cuerpo:mandibula_2
    ]},
    {"id": "tension", "frases": [
        "Mucha gente aprieta los dientes de día sin darse cuenta, frente a la pantalla, en el tráfico, leyendo un mensaje.",   # toma de estres_cuerpo:mandibula_4
        "Esa tensión sube por las sienes y la nuca. Y se vuelve el dolor de cabeza más común del mundo: el de tipo tensional.",   # toma de estres_cuerpo:mandibula_5
    ]},
    {"id": "truco", "frases": [
        "[curious] El arreglo: aprende la posición de descanso de tu quijada. Labios juntos, dientes separados, y la lengua tocando suavemente el paladar.",   # nueva
        "Los dientes solo deberían tocarse para masticar y tragar. El resto del día, deberían estar separados.",   # toma de estres_cuerpo:mandibula_13
        "Pega una nota pequeña en tu monitor o en el espejo. Cada vez que la veas, revisa: ¿dientes separados? ¿hombros abajo?",   # toma de estres_cuerpo:mandibula_14
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "[thoughtful] Y la quijada es solo uno de los cinco lugares donde se esconde el estrés. El recorrido completo está en el video.",   # nueva
    ]},
]
