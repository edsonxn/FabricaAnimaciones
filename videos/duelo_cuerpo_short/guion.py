# -*- coding: utf-8 -*-
"""SHORT vertical de Cuerpo en Neón (22-oct-2026), derivado de `duelo_cuerpo` (fórmula nueva: un Short por largo, una
sola idea, ~45 s, «video relacionado» = el largo). Idea: el síndrome del corazón roto (takotsubo). Hechos y fuentes: ver
el docstring de videos/duelo_cuerpo/guion.py (Wittstein et al. 2005, Templin et al. 2015).
Las frases marcadas «toma de …» reutilizan la toma de voz del largo (copiada a voz/cands); las «nueva» se piden a ElevenLabs.
Las imágenes son las del largo reencuadradas a 9:16: ver `medios_del_largo.py` y docs/estilo_linea_neon.md § «Shorts derivados».
"""

TITULO = "¿Se puede romper un corazón de verdad?"
ARCHIVO = "duelo_cuerpo_short"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160                 # solo cuantiza la línea de tiempo (lección de short_suspiro)
GAP = 0.16
LARGO = dict(video="duelo_cuerpo", id="Mb8umuTXxf4")   # el Short enlaza a este video (video relacionado); id al subir el largo

CER_MAX_POR_FRASE = {"corazon_2": 0.06}     # «9 de cada 10», «50»: cifras (falso positivo de Whisper)
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
    estilo="Tender, intimate ambient score for a science explainer drawn in white chalk lines on black with glowing neon: soft felt piano, warm cello, slow pads, a faint heartbeat pulse. Instrumental only, no vocals, never loud.",
    escenas={
        "gancho": ("A question in the dark: a single low piano note and a muffled heartbeat.", 2),
        "corazon": ("The broken heart: a serious cello line, a pulse that falters and then steadies.", 5),
        "cierre": ("Warm resolution: a soft piano phrase and a final gentle chord.", 2),
    },
    tramos=[(["gancho", "corazon", "cierre"], "Begin with a muffled heartbeat, open into a tender cello line, end with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.3, "frases": [
        "[curious] ¿Se puede romper un corazón de verdad?",   # nueva
        "[serious] Sí. Y los médicos lo pueden ver en una pantalla.",   # nueva
    ]},
    {"id": "corazon", "frases": [
        "Ante una noticia terrible, la oleada de adrenalina puede ser tan fuerte que la punta del corazón se queda casi sin moverse, y se infla como un globo.",   # toma de duelo_cuerpo:horas_5
        "En Japón lo llamaron takotsubo, porque el corazón toma la forma de una vasija que usan los pescadores para atrapar pulpos.",   # toma de duelo_cuerpo:horas_6
        "Se siente igual que un infarto: dolor en el pecho y falta de aire. Y en 9 de cada 10 casos, le pasa a mujeres, sobre todo después de los 50.",   # toma de duelo_cuerpo:horas_7
        "[short pause] En la mayoría, el corazón recupera su forma en unas semanas. Pero no es inofensivo: si te duele el pecho, es a urgencias, siempre.",   # toma de duelo_cuerpo:horas_8
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "[thoughtful] Y eso es solo el primer día. Lo que le pasa a tu cuerpo en las semanas y los meses siguientes, te lo cuento en el video completo.",   # nueva
    ]},
]
