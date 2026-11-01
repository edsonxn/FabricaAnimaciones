# -*- coding: utf-8 -*-
"""SHORT vertical de Cuerpo en Neón (21-oct-2026, pedido del usuario: un Short por video largo, una técnica, ~45 s, con
«video relacionado» al largo). Short derivado de `freno_enojo` (técnica 1: el suspiro fisiológico). Hechos y fuentes: ver docstring de videos/freno_enojo/guion.py (Balban et al. 2023, Cell Reports Medicine).
Las frases marcadas «toma de …» reutilizan la toma de voz del largo (copiada a voz/cands); las «nueva» se piden a ElevenLabs.
Las imágenes son las del largo reencuadradas a 9:16 (recorte centrado en el neón + fundido a negro arriba y abajo):
ver `medios_del_largo.py` y docs/estilo_linea_neon.md § «Shorts derivados».
"""

TITULO = "Si lloras cuando te enojas, haz esto"
ARCHIVO = "short_suspiro"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160                 # solo cuantiza la línea de tiempo: bloques de 1,5 s (con 80 sobraban hasta 3 s de silencio por escena)
GAP = 0.16
LARGO = dict(video="freno_enojo", id="-zNE22UIjko")   # el Short enlaza a este video (video relacionado)

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
    estilo="Intimate, cinematic ambient score for a calm science explainer drawn in white chalk lines on black with glowing neon: warm analog synth pads, soft felt piano, subtle pulsing bass, airy textures. Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("Tense and suspended: low drone, a muffled heartbeat pulse, a single repeated piano note.", 2),
        "suspiro": ("Breathing and slowing: long swelling pads that inhale and exhale, tempo gently decelerating, calm.", 6),
        "cierre": ("Warm resolution: soft piano melody in a major key, a final gentle chord.", 2),
    },
    tramos=[(["gancho", "suspiro", "cierre"], "Begin with a tense heartbeat pulse, open into slow breathing pads, end with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.3, "frases": [
        "[curious] ¿Te ganan las lágrimas cuando te enojas?",   # nueva
        "[serious] No es debilidad. Es tu cuerpo frenando de golpe, después de prepararse para pelear.",   # nueva
    ]},
    {"id": "suspiro", "frases": [
        "[curious] La próxima vez, haz esto. Se llama suspiro fisiológico.",   # nueva
        "Inhala profundo por la nariz, y con los pulmones llenos, mete un segundo jalón corto de aire.",   # toma de freno_enojo:suspiro_1
        "Ese jalón vuelve a inflar los alvéolos que se habían cerrado.",   # toma de freno_enojo:suspiro_2
        "[exhales] Luego suelta todo despacio por la boca, el doble de largo.",   # toma de freno_enojo:suspiro_3
        "Cada vez que exhalas, el nervio vago frena un poco el corazón. Exhalar largo es frenar largo.",   # toma de freno_enojo:suspiro_4
        "En 2023, un estudio de Stanford vio que este suspiro mejoraba el ánimo más que la meditación. Con dos o tres, el golpe baja.",   # toma de freno_enojo:suspiro_5
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "[thoughtful] Y hay cuatro formas más de drenar el coraje. Te las dejo en el video completo.",   # nueva
    ]},
]
