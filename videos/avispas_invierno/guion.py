# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens to Wasps When Winter Comes?»  Motor SECUENCIA (docs/estilo_secuencia_flow.md).
Fuentes: NDSU Extension (yellowjackets), University of Idaho Extension, Iowa State Yard and Garden, Colonial Pest
(«Yellowjacket nests don't survive the winter»); nidos perennes de Alabama 2006 (Alabama Cooperative Extension).
Hechos usados: solo las reinas nuevas ya apareadas pasan el invierno (diapausa, glicerol); obreras, machos y reina vieja
mueren con las heladas; el nido no se reutiliza; en primavera la reina funda sola; en climas cálidos hay nidos perennes.
"""

TITULO = "What Happens to Wasps When Winter Comes?"
ARCHIVO = "wasps_winter"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=60,         # el usuario pidió 1 minuto inicial en video
    clip_s=8,
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    recorte_por={"scene-001": 0.035, "scene-002": 0.055, "scene-003": 0.035},   # los clips salieron con marco de viñeta
    carpeta_descargas="flow-avispas_invierno",
)

# Ficha visual: se copia palabra por palabra en los prompts (en inglés: el canal y el texto de Flow van en inglés).
FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "queen": "a cartoon yellowjacket wasp queen with a plump yellow and black striped body, a narrow waist, big "
                 "round expressive eyes, two bent antennae, clear wings and a tiny gold crown",
        "worker": "small cartoon yellowjacket worker wasps with yellow and black striped bodies, big round eyes and no crown",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a gray papery wasp nest shaped like an upside-down teardrop with a single round hole at the bottom",
    epoca="present-day suburban backyard and wooden house",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "hook": dict(sabor="tension"), "promise": dict(sabor="espacio"), "summer": dict(sabor="esperanza"),
    "sugar": dict(sabor="tension"), "frost": dict(sabor="vacio"), "queens": dict(sabor="espacio"),
    "hiding": dict(sabor="tension"), "sleep": dict(sabor="vacio"), "odds": dict(sabor="tension"),
    "spring": dict(sabor="esperanza"), "south": dict(sabor="tension"), "outro": dict(sabor="esperanza"),
}

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "Every autumn, a wasp nest the size of a basketball goes completely silent.",
        "Thousands of wasps, gone in a matter of days.",
        "No bodies on your porch. No swarm flying south. Nothing.",
        "So where did they all go?",
        "The answer is stranger than you think, and one of them might be sleeping inside your house right now.",
    ]},
    {"id": "promise", "frases": [
        "Most people believe wasps hibernate together inside the nest, like bears in a cave.",
        "They don't.",
        "Almost the entire colony is about to die, and the wasps have known it for weeks.",
        "Only one kind of wasp is built to see the spring.",
        "To understand who survives, we have to go back to the best days of summer.",
    ]},
    {"id": "summer", "frases": [
        "In July, a yellowjacket nest is a booming city.",
        "At the center is one queen, and her only job is laying eggs.",
        "Around her, thousands of workers hunt flies, caterpillars and other insects all day long.",
        "But the workers can't eat that meat themselves.",
        "An adult wasp cannot digest solid food.",
        "So they chew it up and feed it to the larvae, the hungry babies of the colony.",
        "In return, each larva pays them with a drop of sugary liquid.",
        "Meat goes in, sugar comes out. That trade keeps the whole city running.",
    ]},
    {"id": "sugar", "frases": [
        "Then, near the end of summer, the queen changes the plan.",
        "She stops making workers.",
        "The last eggs she lays grow into something different: males, and brand new queens.",
        "When those leave the nest, there are no more babies to feed.",
        "And no babies means no sugar.",
        "Thousands of workers are suddenly unemployed and starving.",
        "That is why wasps crash your picnic in September.",
        "They are not angry. They are desperate for anything sweet, like your soda, your fruit, your ice cream.",
    ]},
    {"id": "frost", "frases": [
        "And then the cold arrives.",
        "Worker wasps have no way to store fat and no way to stay warm.",
        "After the first hard frosts, they slow down, fall, and die.",
        "The males die too, usually right after mating.",
        "Even the old queen, the mother of the whole city, does not make it.",
        "By early winter, the nest is an empty paper shell.",
        "And it will never be used again.",
    ]},
    {"id": "queens", "frases": [
        "But remember those brand new queens.",
        "Before the cold came, each one flew away from home and mated.",
        "Then she did something no worker ever does. She got fat.",
        "She packed her body with enough fuel to last half a year without a single meal.",
        "Each of these young queens now carries the future of an entire colony inside her.",
        "All she needs is a place to hide.",
    ]},
    {"id": "hiding", "frases": [
        "She looks for somewhere dry, dark, and out of the wind.",
        "Under loose tree bark. Inside a rotting log. Deep in a pile of firewood.",
        "And very often, inside your house.",
        "In the attic. Behind the siding. In the shed. Even in the folds of a curtain.",
        "She tucks her wings and antennae under her body and holds on with her jaws.",
        "And then, she simply stops.",
    ]},
    {"id": "sleep", "frases": [
        "Scientists call this state diapause.",
        "Her heartbeat slows. She does not eat. She does not move.",
        "Her body even fills with a natural antifreeze, so ice crystals can't tear her cells apart.",
        "She will hang there for months, alone, in the dark.",
        "A whole wasp city, folded into a single sleeping insect.",
    ]},
    {"id": "odds", "frases": [
        "But sleeping through winter is a terrible gamble.",
        "Spiders find the queens and eat them. Mold grows over them.",
        "And, strangely, a warm winter is worse than a freezing one.",
        "A warm spell wakes her up too early, she burns through her fat, and there is nothing outside to eat.",
        "Most of the queens that go to sleep in autumn never wake up.",
        "So what happens to the few that do?",
    ]},
    {"id": "spring", "frases": [
        "On the first warm days of spring, a survivor crawls out into the light.",
        "She is alone. No workers. No nest. No help.",
        "She scrapes wood from a fence, chews it into paper, and builds a nest no bigger than a golf ball.",
        "She lays a few eggs, and then she does every job herself.",
        "She hunts. She feeds the babies. She guards the door.",
        "About a month later, her first daughters hatch and take over the work.",
        "From that day on, the queen never leaves the nest again.",
        "By midsummer, one sleepy insect from your attic has become a city of thousands.",
    ]},
    {"id": "south", "frases": [
        "Unless winter never really comes.",
        "In warm places like Florida and southern Alabama, some nests don't die at all.",
        "They keep growing for years, with many queens laying eggs at the same time.",
        "One of those giant nests completely filled the inside of an abandoned car.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So that silent gray nest under your roof is not sleeping.",
        "It is empty, and it is safe to take down in the middle of winter.",
        "But if you find one slow, sleepy wasp in your attic in January, look closer.",
        "You are not looking at a leftover. You are looking at a queen.",
        "And she is carrying next summer's entire city.",
    ]},
]
