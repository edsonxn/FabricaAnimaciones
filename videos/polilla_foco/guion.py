# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens to a Moth That Circles Your Porch Light All Night?»  SECUENCIA, ~4 min.
Video 6 de la tanda de la FÓRMULA NUEVA (canales/formula/wild_next_door.md § «Revisión 22-oct»). Pregunta universal sin
dueño en formato largo. Ángulo humano: el GPS atascado en «gira a la izquierda» / el piloto con el horizonte roto.
Enlaza con `telarana_rota` (las arañas tejen junto al foco).
Hechos usados y fuentes (DOIs verificados en Crossref el 22-oct-2026):
- Fabian, S. T. et al. (2024), Nature Communications, «Why flying insects gather at artificial light»
  (10.1038/s41467-024-44785-3; Imperial College London, cámaras de captura de movimiento en 3D en Costa Rica y laboratorio):
  los insectos no van directo a la luz; inclinan el DORSO hacia la fuente más brillante (reflejo de «luz dorsal» que de
  día los mantiene nivelados porque el cielo es lo más brillante); cerca de una lámpara eso los hace orbitar, quedarse
  atascados, y voltearse panza arriba al pasar justo encima.
- Teoría vieja: navegaban por la Luna con un ángulo fijo (orientación transversa); el estudio de 2024 no la apoya.
- Knop, E. et al. (2017), Nature, «Artificial light at night as a new threat to pollination» (10.1038/nature23288):
  en praderas suizas iluminadas de noche, las visitas de polinizadores nocturnos a las flores cayeron 62 % y una planta
  dio 13 % menos frutos.
- Walton, R. E. et al. (2020), Biology Letters, «Nocturnal pollinators strongly contribute to pollen transport of wild
  flowers in an agricultural landscape» (10.1098/rsbl.2019.0877).
- Agotamiento al girar; al amanecer quedan posadas en paredes claras sin camuflaje → aves y lagartijas; las luces
  concentran insectos y dificultan esquivar murciélagos (Boise State University, cobertura). LED cálidos/amarillos
  atraen menos insectos que los blancos.
"""

TITULO = "What Happens to a Moth That Circles Your Porch Light All Night?"
ARCHIVO = "moth_porch_light"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# «fliers» / «flyers» (Whisper); hook_4 y myth_2 terminan hablando hasta el final (CER 0): cola alta aceptada
CER_MAX_POR_FRASE = {"trap_6": 0.02}
TAIL_MAX_POR_FRASE = {"hook_4": 0.42, "myth_2": 0.40}

SECUENCIA = dict(
    video_s=0,
    clip_s=8,
    img_s=3.5,
    rapido_hasta=300,
    img_s_lento=4.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-polilla_foco",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "moth": "a cartoon fluffy tan moth with soft brown patterned wings, feathery antennae, big round dizzy eyes, a "
                "fuzzy body, and a tiny pair of aviator goggles pushed up on its head",
        "human": "a simple cartoon woman with a round white head, dot eyes, curly red hair, glasses and a cozy green "
                 "sweater",
        "bat": "a small cartoon brown bat with big ears, tiny fangs and a mischievous grin",
    },
    objeto="a bright white glowing porch light in a glass lantern on a wooden house wall, with a halo of light",
    epoca="present-day American front porch on a warm summer night, dark blue sky, a garden with white night flowers",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

LYRIA = dict(
    estilo="Dreamy, curious cartoon nature documentary score about moths circling a porch light at night: celesta, "
           "vibraphone, pizzicato strings, soft clarinet, felt piano, light brushed percussion and upright bass. "
           "Nocturnal, gently comic and a little bittersweet. Never epic, never horror.",
    escenas={
        "hook": ("Warm summer night, crickets implied, a twinkling celesta circling around and around like a moth.", 4),
        "myth": ("An old-fashioned storybook theme, then a modern investigative pulse as cameras roll.", 4),
        "trap": ("Dizzy looping waltz that keeps going round, then flips upside down with a comic wobble.", 6),
        "night": ("Tired and slow: the loop winds down, a long yawn on clarinet, the first birds at dawn.", 2),
        "cost": ("Gentle and tender: night flowers opening, soft strings and felt piano, a little sad.", 2),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening night theme, warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "myth", "trap"],
         "Begin from near silence. End on a held dizzy tone that can flow into the next piece. No loud ending."),
        (["night", "cost", "deal", "outro"],
         "Begin softly with a low held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is a warm summer night. You flip on the porch light, and within minutes, they arrive.",
        "Moths. Dozens of them. Spinning around the bulb, bumping into the glass, never landing, never leaving.",
        "In the morning, a few are still there, stuck flat against the wall.",
        "So what happens to a moth that circles your porch light all night long? And why can't it just fly away?",
        "For centuries, people said moths love the light. In twenty twenty-four, scientists finally filmed it in three dimensions. And it turns out, they don't.",
        "They are not attracted. They are trapped.",
    ]},
    {"id": "myth", "frases": [
        "The old idea was that moths steer by the moon.",
        "Keep the moon at the same angle, and you fly in a straight line. Mistake a bulb for the moon, and you spiral into it.",
        "It sounded smart. But when researchers from Imperial College London tracked insects around lights with motion capture cameras, that is not what they saw.",
    ]},
    {"id": "trap", "frases": [
        "Here is what really happens.",
        "For millions of years, the brightest thing in the night was the sky. So the brightest direction meant up.",
        "To stay level, flying insects tilt their backs toward the brightest light. It is like an autopilot that keeps them right side up.",
        "Now put a bright bulb next to a moth. Its autopilot says the sky is over there, sideways. So it tilts its back toward the bulb.",
        "And it ends up flying in circles around it. Orbiting. Stuck.",
        "When it passes right over the top, it can even flip upside down, because now the sky seems to be below it.",
        "The researchers saw the same thing in moths, dragonflies and other night fliers.",
        "Imagine driving home at night with your GPS stuck on turn left. Forever.",
    ]},
    {"id": "night", "frases": [
        "So the moth circles. And circles. Burning energy it needed for finding food and finding a mate.",
        "Some fall out of the air, exhausted. Others finally land on the wall, and freeze until morning.",
        "And at dawn, a pale moth on a bright wall has nowhere to hide. Birds and lizards know exactly where to look.",
        "Even at night, a light full of moths is a buffet. Bats swoop in. And spiders build their webs right next to the bulb.",
        "And every moth stuck at your porch is a moth that is not out there doing its job.",
    ]},
    {"id": "cost", "frases": [
        "And this matters more than it seems.",
        "Moths are the night shift of pollination. While bees sleep, moths carry pollen from flower to flower.",
        "In England, another team found that moths visit a huge variety of wild flowers, carrying pollen across whole fields in the dark.",
        "In one experiment in Switzerland, meadows lit up at night got sixty-two percent fewer visits from night pollinators.",
        "And one of the plants there made thirteen percent less fruit. Just because of the lights.",
    ]},
    {"id": "deal", "frases": [
        "So what can you do? It is surprisingly easy.",
        "Turn the porch light off when nobody needs it, or put it on a motion sensor.",
        "Swap the bright white bulb for a warm yellow one. Fewer insects get caught in its spell.",
        "And point your lights down, toward the ground, not up into the sky. That keeps the fake sky out of their eyes.",
        "Even closing the curtains helps, so the lights inside your house do not spill out into the yard.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you see a moth spinning around your porch light, you will know the truth.",
        "It is not in love with the light. It is lost, flying in circles, trying to keep the sky on top.",
        "Flip the switch, and let it find the real one.",
    ]},
]
