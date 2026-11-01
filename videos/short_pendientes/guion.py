# -*- coding: utf-8 -*-
"""SHORT vertical de Cuerpo en Neón (21-oct-2026, pedido del usuario: un Short por video largo, una técnica, ~45 s, con
«video relacionado» al largo). Short derivado de `agotado_cortisol` (técnica 1: la lista de pendientes en papel). Fuentes: Zeigarnik 1927; Scullin et al. 2018, J. Exp. Psychol. Gen. (Baylor).
Las frases marcadas «toma de …» reutilizan la toma de voz del largo (copiada a voz/cands); las «nueva» se piden a ElevenLabs.
Las imágenes son las del largo reencuadradas a 9:16 (recorte centrado en el neón + fundido a negro arriba y abajo):
ver `medios_del_largo.py` y docs/estilo_linea_neon.md § «Shorts derivados».
"""

TITULO = "Si tu mente no se apaga de noche, haz esto"
ARCHIVO = "short_pendientes"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160                 # solo cuantiza la línea de tiempo: bloques de 1,5 s (con 80 sobraban hasta 3 s de silencio por escena)
GAP = 0.16
CER_MAX_POR_FRASE = {"pendientes_0": 0.03}   # Whisper: «Zeigarnik» -> «Seygarnik» (igual que en agotado_cortisol)
LARGO = dict(video="agotado_cortisol", id="fLmNcI235FU")   # el Short enlaza a este video (video relacionado)

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
    estilo="Soft nocturnal ambient score for a calm sleep-science explainer drawn in white chalk lines on black with glowing neon: warm pads, gentle music-box and felt piano, slow tempo. Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("Restless night: a ticking clock pulse, a few anxious piano notes, unresolved.", 2),
        "pendientes": ("Busy mind: light overlapping plucks like many open browser tabs, a little cluttered.", 3),
        "lista": ("Relief: the clutter clears, slow warm pads, a gentle lullaby melody on felt piano.", 4),
        "cierre": ("Drifting off to sleep: soft pad and music box fading to silence.", 2),
    },
    tramos=[(["gancho", "pendientes", "lista", "cierre"], "Begin restless with a ticking pulse, settle into a calm lullaby, end fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.3, "frases": [
        "[curious] ¿Apagas la luz… y tu cabeza se enciende con todos tus pendientes?",   # nueva
    ]},
    {"id": "pendientes", "frases": [
        "En 1927, la psicóloga Bluma Zeigarnik notó que recordamos mejor las tareas interrumpidas que las terminadas.",   # toma de agotado_cortisol:pendientes_1
        "De día, el ruido las tapa. En el silencio de la noche, el cerebro abre todas las pestañas pendientes para no olvidarlas.",   # toma de agotado_cortisol:pendientes_2
    ]},
    {"id": "lista", "frases": [
        "[curious] El truco toma 5 minutos: saca los pendientes de tu cabeza.",   # nueva
        "Antes de acostarte, escribe en papel todo lo que tienes que hacer mañana. Con detalle.",   # toma de agotado_cortisol:lista_1
        "En 2018, en la Universidad de Baylor, un grupo escribió su lista de pendientes 5 minutos antes de dormir.",   # toma de agotado_cortisol:lista_2
        "Se durmieron unos 9 minutos más rápido que quienes anotaron lo que ya habían terminado. Y entre más detallada la lista, mejor.",   # toma de agotado_cortisol:lista_3
        "Al cerebro le basta con saber que la pestaña quedó guardada.",   # toma de agotado_cortisol:lista_4
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "[thoughtful] Y hay cuatro trucos más para apagar la mente de noche. Están en el video completo.",   # nueva
    ]},
]
