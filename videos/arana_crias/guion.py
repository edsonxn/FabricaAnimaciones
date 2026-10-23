# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens If You Squish a Spider Carrying Babies?»  Motor SECUENCIA, ~4 min.
Video 7 de la tanda de la FÓRMULA NUEVA (canales/formula/wild_next_door.md § «Revisión 22-oct»). Referencias: Science
Channel «Bug Spray Kills Spider, Spawns Nightmare» (23 M); CBC «Hundreds of baby spiders explode from mother's egg sac
after man hits her with a broom» (viral). Ángulo humano: la mamá que carga a cien niños sin carriola.
Hechos usados y fuentes:
- Museums Victoria (Lycosidae, «wolf spiders»): la madre carga el saco de huevos pegado a las hileras; las crías trepan
  por sus patas y viajan en su lomo unas semanas, a veces en varias capas.
- Northern Woodlands, «Spider Moms» / BugGuide: decenas a cientos de crías; las crías emergen 3-6 semanas después; casi
  nunca comen hasta dispersarse (viven de la yema), una semana o hasta un mes después de la primera muda; no comparten la
  presa de la madre; si se caen, ella no las rescata.
- CBC (2015): un hombre golpea a una araña lobo con una escoba y cientos de crías se dispersan.
- Las arañas lobo cazan de noche sin tela; sus ojos reflejan la luz de una linterna (tapetum lucidum: brillo de ojos
  verde-plateado). Su mordida en un adulto sano es como una picadura de abeja.
- Las crías se dispersan caminando o «en globo» con un hilo de seda que atrapa el viento.
"""

TITULO = "What Happens If You Squish a Spider Carrying Babies?"
ARCHIVO = "spider_babies"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=0,
    clip_s=8,
    img_s=3.5,
    rapido_hasta=300,
    img_s_lento=4.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-arana_crias",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "mom": "a cartoon brown wolf spider mother with a fuzzy striped gray-brown body, eight sturdy hairy legs, a row of "
               "big shiny dark eyes, a warm motherly face, and a tiny pink bandana tied around her head",
        "babies": "dozens of tiny pale cartoon baby spiders with dot eyes, piled in layers on their mother's back",
        "human": "a simple cartoon man with a round white head, dot eyes, a baseball cap, a gray hoodie and work boots",
    },
    objeto="a garage floor with a workbench, garden tools, a broom, and a half-open garage door to the backyard",
    epoca="present-day American home in early autumn, evening",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

LYRIA = dict(
    estilo="Tender, slightly suspenseful cartoon nature documentary score about a wolf spider mother carrying her babies: "
           "pizzicato strings, marimba, celesta, soft clarinet, felt piano, bassoon, light brushed percussion. Warm, "
           "surprising and a little funny. Never epic, never horror.",
    escenas={
        "hook": ("Quiet garage evening, a tense held note, then a burst of tiny scattering pizzicato everywhere.", 6),
        "who": ("A warm lullaby for a hard-working mother, felt piano and clarinet.", 2),
        "ride": ("A bouncy piggyback ride theme: marimba and pizzicato hopping along, crowded and cheerful.", 4),
        "squish": ("Comic chaos: scattering runs in every direction, then a quiet confused pause.", 6),
        "after": ("Thoughtful and a bit sad: sparse celesta, small lonely footsteps, then a hopeful wind.", 2),
        "bite": ("Relaxed debunking groove: walking bass and brushes, reassuring and light.", 4),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening lullaby, warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "who", "ride"],
         "Begin from near silence. End on a held curious tone that can flow into the next piece. No loud ending."),
        (["squish", "after", "bite"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "You flip on the garage light, and there it is. A big, hairy spider, right in the middle of the floor.",
        "Something about its back looks strange. Lumpy. Almost like it is moving.",
        "You raise your boot. And just before you bring it down, you see it.",
        "Those lumps have legs. Dozens of them. Maybe hundreds.",
        "So what actually happens if you squish a spider carrying babies? It is not what most people imagine.",
    ]},
    {"id": "who", "frases": [
        "This is a wolf spider. And that is a mother, doing something almost no other spider does.",
        "Wolf spiders do not build webs to catch food. They hunt on the ground at night, running down insects like tiny wolves.",
        "And here is a trick. Shine a flashlight across your yard at night, and their eyes glow back at you, like little green sparkles.",
    ]},
    {"id": "ride", "frases": [
        "Before her babies hatch, she carries her eggs in a round silk ball, attached to the back end of her body.",
        "She drags it everywhere for weeks. Hunting, hiding, running. She does not let it go.",
        "When the babies finally hatch, they climb up her legs, and pile onto her back. Sometimes several layers deep.",
        "Think of a mom carrying a hundred kids to the grocery store. No stroller. No car. Just her back.",
        "And they do not even eat during the ride. They live off the yolk they were born with.",
        "If one falls off, she does not stop to pick it up. It has to scramble back up her legs on its own.",
    ]},
    {"id": "squish", "frases": [
        "So now, back to your boot.",
        "If you stomp on her, the mother dies. But the babies do not all go with her.",
        "Most of them jump off and run. In every direction. Under the workbench, behind the boxes, into the cracks.",
        "And that is the moment people film and post online, because it looks like the floor is exploding with spiders.",
        "So squishing the mother does not get rid of the spiders. It just spreads them out.",
    ]},
    {"id": "after", "frases": [
        "And then what happens to them?",
        "Without their mother, the babies are on their own, a little earlier than planned.",
        "In a dry garage, with almost nothing to eat, many of them will not make it.",
        "The ones that do will grow up into wolf spiders. And then they get to work, hunting crickets, roaches, and other bugs, right there in your garage.",
        "Outside, many baby spiders leave home in a stranger way. They climb up high, let out a thread of silk, and float away on the wind.",
    ]},
    {"id": "bite", "frases": [
        "But wait. Is a mother wolf spider dangerous?",
        "Not really. Wolf spiders would much rather run than fight, and she is busy protecting her babies.",
        "They only bite if they are grabbed or pinned. And for a healthy adult, it feels about like a bee sting.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do instead of the boot?",
        "Grab a big bowl or a bucket, set it over her, and slide a piece of cardboard underneath. Slowly. Her babies will hold on.",
        "Then carry the whole family outside, to a garden bed or a pile of leaves, and let them go.",
        "Wolf spiders are outdoor hunters, so outside is exactly where they want to be.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you spot a lumpy spider in the garage, take a closer look before the boot comes down.",
        "That is not one spider. It is a mom with a hundred kids, on the longest piggyback ride of their lives.",
        "A bucket and a piece of cardboard. And the whole family goes home.",
    ]},
]
