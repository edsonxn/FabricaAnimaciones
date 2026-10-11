# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «Why Spiders "Invade" Your House Every Fall (They Don't)»  Motor SECUENCIA.
Fuente principal: Rod Crawford, curador de arácnidos del Burke Museum («Myth: Spiders come indoors in the fall»,
«Myth: Putting house spiders outside», «Myth: Spiders come up through drains»). Hechos usados: las arañas de casa son
especies adaptadas al interior y viven ahí toda su vida; menos del cinco por ciento ha estado afuera; no buscan calor
(sangre fría); lo que se ve a fines de verano y otoño son machos adultos que dejan su tela para buscar pareja; las de
la tina cayeron buscando agua y no pueden trepar; sacarlas al jardín suele matarlas; comen plagas de la casa.
Todo en imagen (Flow sin puntos de video el 6-oct-2026).
"""

TITULO = "Why Spiders \"Invade\" Your House Every Fall (They Don't)"
ARCHIVO = "spiders_fall"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=0,          # sin puntos de video en Flow: todo imagen
    clip_s=8,
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-aranas_otono",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "male": "a cartoon male house spider with a small round brown fuzzy body, eight long thin legs, two big round "
                "expressive eyes and a tiny red bow tie",
        "female": "a cartoon female house spider with a big round brown fuzzy body, eight thin legs, two big round "
                  "expressive eyes with long eyelashes, sitting in a messy web",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a messy funnel-shaped cobweb tucked in a dark corner",
    epoca="present-day suburban house interior",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "hook": dict(sabor="tension"), "myth": dict(sabor="espacio"), "cold": dict(sabor="vacio"),
    "locals": dict(sabor="espacio"), "hidden": dict(sabor="tension"), "males": dict(sabor="esperanza"),
    "walk": dict(sabor="tension"), "tub": dict(sabor="espacio"), "outside": dict(sabor="vacio"),
    "job": dict(sabor="esperanza"), "outro": dict(sabor="esperanza"),
}

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "Every fall, it happens again.",
        "A huge spider sprints across your living room floor.",
        "Then another one shows up in the bathtub.",
        "And everybody says the same thing: it's getting cold, so the spiders are coming inside.",
        "It sounds obvious. It is also completely wrong.",
        "Those spiders did not just move in. They have been living with you the whole time.",
    ]},
    {"id": "myth", "frases": [
        "The idea is simple. Summer ends, the nights get chilly, and spiders sneak indoors to stay warm.",
        "There is just one problem with that story.",
        "Spiders don't care about being warm.",
    ]},
    {"id": "cold", "frases": [
        "A spider is cold blooded.",
        "When the temperature drops, it does not shiver, and it does not go looking for a heater.",
        "It simply slows down, and when it gets cold enough, it stops moving and waits.",
        "Outdoor spiders are built for this.",
        "Many of them spend the winter under bark or dead leaves, perfectly fine.",
        "A warm house is not a rescue for them. It is the wrong planet.",
    ]},
    {"id": "locals", "frases": [
        "So who are the spiders in your house?",
        "They are a completely different crowd.",
        "House spiders belong to a small group of species that are specialists at living indoors.",
        "They can handle steady temperatures, very little food, and almost no water.",
        "Some of these species have been living inside human homes since the days of ancient Rome.",
        "They usually arrive as tiny eggs, hidden inside furniture, boxes, or building materials.",
        "Then they hatch, grow up, and spend their entire lives inside your walls.",
        "According to spider experts, fewer than five out of every hundred spiders you see indoors have ever been outside.",
    ]},
    {"id": "hidden", "frases": [
        "So if they are always there, why don't you see them all year?",
        "Because a house spider's whole strategy is to stay out of sight.",
        "It builds a web in a quiet corner, behind a shelf, under the stairs, down in the basement.",
        "And then it sits there and waits, sometimes for months, without moving more than a few inches.",
        "You have probably walked past the same spider hundreds of times without ever knowing it.",
    ]},
    {"id": "males", "frases": [
        "Then late summer arrives, and something changes.",
        "The young males finally become adults.",
        "And an adult male spider has exactly one thing on his mind.",
        "He abandons his web. He stops hunting. He barely eats.",
        "And he starts walking, across floors, up walls, anywhere, looking for a female.",
    ]},
    {"id": "walk", "frases": [
        "That is the spider you see running across the carpet at night.",
        "He is not invading. He is not hunting you. He is lost, and he is on a date.",
        "The females stay hidden in their webs, exactly where they have always been.",
        "So the spider season is not an invasion at all.",
        "It is the few weeks each year when the males come out of hiding.",
        "And for most of them, it is the last thing they ever do. After the mating season, the males die.",
    ]},
    {"id": "tub", "frases": [
        "What about the one in your bathtub?",
        "People think it crawled up through the drain. It didn't.",
        "A drain is full of water, and a spider can't swim through that.",
        "He was wandering, he got thirsty, and he climbed down for a drink.",
        "Then he found out the walls of a bathtub are too smooth to climb.",
        "He is not waiting for you. He is stuck.",
    ]},
    {"id": "outside", "frases": [
        "So should you do the kind thing and carry him outside?",
        "Here is the twist nobody expects.",
        "For a true house spider, the outdoors is not home. It never was.",
        "It has never faced cold, rain, or the hunters that live out there.",
        "Putting a house spider in the garden usually does not save it. It kills it.",
    ]},
    {"id": "job", "frases": [
        "And it has been working for you the whole time.",
        "House spiders eat flies, mosquitoes, moths, and even other spiders.",
        "They are free pest control that never asks for anything.",
        "Almost none of them can hurt you, and they want nothing to do with you.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time a big spider crosses your floor in the fall, remember what you are really looking at.",
        "Not an invader from the cold.",
        "Just a neighbor who has lived in your house longer than you thought, finally leaving his room.",
        "And he is having a much more stressful night than you are.",
    ]},
]
