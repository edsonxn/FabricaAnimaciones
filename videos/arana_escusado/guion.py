# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens to a Spider You Flush Down the Toilet?»  Motor SECUENCIA, ~4 min.
Primer video de la FÓRMULA NUEVA (22-oct-2026, canales/formula/wild_next_door.md § «Revisión 22-oct»): «What Happens
If/After You <acción común>?», 3:30-4:30, estructura de Zyka («What Happens to a Spider After You Vacuum It Up?» 437 K
en 4 días, ×344): escena en 2.ª persona → pregunta inquietante → experto con nombre en < 30 s → el viaje paso a paso →
excepción rara cada ~40 s → consejo práctico → giro final. El bicho en una situación humana reconocible (lo que más
comenta este público de 35-54 años). Todo imagen (0 puntos de Flow).
Hechos usados y fuentes:
- Jerome Rovner (American Arachnological Society), citado por RealClearScience: los arañas tiradas al escusado se ahogan
  si quedan sumergidas en el drenaje, pero puede tardar una hora o más por su metabolismo muy bajo.
- Pétillon, Montaigne & Renault 2009, Biology Letters, «Hypoxic coma as a strategy to survive inundation in a salt-marsh
  inhabiting spider» (DOI 10.1098/rsbl.2009.0127, verificado en Crossref): Arctosa fulvolineata (araña lobo de marisma
  francesa) aguantó sumergida ~16 h la mayoría y hasta ~40 h unas pocas; al secarse en el laboratorio volvió a moverse
  horas después (NBC News, «Drowned spiders come back from the dead», 2009).
- Pelos hidrófugos que atrapan una capa de aire; Argyroneta aquatica (araña de campana de buceo) vive bajo el agua en
  una burbuja de seda.
- Escusado: el sifón (trampa en U) siempre guarda agua contra el gas del drenaje; la descarga crea succión. EE. UU.:
  descarga máxima de 1,6 galones (≈ 6 L) desde 1994.
- Burke Museum (Rod Crawford, «Spider Myths»): no se conoce ningún caso comprobado de una araña entrando a una casa por
  la plomería; las trampas de agua lo impiden. Las arañas de la tina bajaron por sed y no pueden trepar la porcelana.
  Muchas arañas de casa viven toda su vida dentro.
"""

TITULO = "What Happens to a Spider You Flush Down the Toilet?"
ARCHIVO = "spider_flush"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=0,          # todo imagen (0 puntos de Flow), como el ciempiés que funcionó
    clip_s=8,
    img_s=3.5,          # cortes rápidos: formato de 4 min, más dinámico
    rapido_hasta=300,
    img_s_lento=4.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-arana_escusado",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "spider": "a cartoon brown house spider with a round tan abdomen marked with dark brown chevrons, a small brown "
                  "head with two big round worried eyes, eight thin legs with light and dark bands, and a tiny blue and "
                  "white striped nightcap with a white pom-pom",
        "human": "a simple cartoon man with a round white head, dot eyes, messy hair, a green bathrobe and fuzzy slippers",
        "wolf": "a cartoon gray-brown marsh wolf spider with a fuzzy striped body, big shiny dark eyes and no hat",
        "diver": "a cartoon dark brown water spider with a silvery air bubble wrapped around its belly, and no hat",
    },
    objeto="a plain white porcelain toilet with a white tank and a silver flush handle, in a small tidy bathroom with "
           "light blue tiles, a fluffy bath mat and a roll of toilet paper",
    epoca="present-day American home bathroom at night, warm yellow light",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Playful, curious cartoon nature documentary score about a tiny house spider swept into the plumbing: "
           "pizzicato strings, marimba, bassoon, soft clarinet, celesta, felt piano, light brushed percussion and upright "
           "bass. Comic suspense and gentle wonder. Never epic, never horror.",
    escenas={
        "hook": ("Quiet late-night bathroom, a ticking pizzicato, then a comic gulp and a swirl of descending marimba.", 3),
        "ride": ("A fast twisting water-slide chase: rushing tremolo strings, tumbling marimba runs, a bassoon bump.", 6),
        "float": ("Sudden calm: a silvery celesta bubble theme, floating and fragile, a little hopeful.", 4),
        "sewer": ("Dark tunnel stroll: low clarinet and plucked bass, echoing drips, lonely but comic.", 4),
        "coma": ("Mysterious stillness, then a soft magical wake-up sparkle and a surprised little cadence.", 4),
        "back": ("Investigative groove: walking bass, curious bassoon, a myth being busted with a wink.", 4),
        "home": ("Tender and a bit sad: felt piano and soft strings, a small character who lost its home.", 2),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening late-night theme, now warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "ride", "float"],
         "Begin from near silence. End on a held suspenseful tone that can flow into the next piece. No loud ending."),
        (["sewer", "coma", "back"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["home", "deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is almost midnight. You shuffle into the bathroom, half asleep.",
        "And there it is. A spider, sitting on the rim of the toilet, staring right back at you.",
        "You do what millions of people do. You give it one quick push, into the bowl, and you flush.",
        "Whoosh. Gone. Problem solved.",
        "But is it?",
        "Where does that spider actually go? Is it dead? And could it ever climb back up, while you are sitting there?",
        "Here is the short answer from spider expert Jerome Rovner. Flushed spiders usually drown.",
        "But not quickly. It can take an hour or more.",
        "And some spiders can survive underwater for more than a day. So let's follow this one, all the way down.",
    ]},
    {"id": "ride", "frases": [
        "You push the handle, the water spins, and the spider gets pulled into a dark, curving tunnel.",
        "That curve is the trap. A bend in the pipe that always holds water, so sewer gas cannot come up into your house.",
        "For a spider, it is the biggest water slide on Earth. In total darkness. With no lifeguard.",
        "Seconds later, it is under your floor, heading for the street.",
    ]},
    {"id": "float", "frases": [
        "And here is the first surprise. A lot of spiders do not sink.",
        "Their bodies are covered in tiny water-repelling hairs that hold a thin silver layer of air.",
        "So the spider can bob on the surface like a little life jacket, breathing from its own private bubble.",
        "One European spider, the diving bell spider, lives its whole life underwater, inside a bubble of air held in silk.",
    ]},
    {"id": "sewer", "frases": [
        "Now it is in the sewer. Cold, dark, and moving.",
        "Imagine falling asleep in your pajamas and waking up in a flooded subway tunnel, in a city you have never seen.",
        "That is the spider's night.",
        "If the current pushes it under, its air starts to run out. But a spider burns energy so slowly that drowning takes a long, long time.",
        "That is why so many spiders seem to come back from the dead.",
    ]},
    {"id": "coma", "frases": [
        "In two thousand nine, scientists in France dunked marsh wolf spiders underwater, to see how long they could last.",
        "Most held on for about sixteen hours. A few lasted around forty.",
        "After a while, they stopped moving completely. They looked dead.",
        "But when the researchers laid them out to dry, they started twitching, and hours later, they walked away.",
        "They had slipped into a kind of coma.",
        "So the spider you flushed might not be dead yet. But it is very far from home.",
    ]},
    {"id": "back", "frases": [
        "So can it climb back up into your toilet?",
        "The answer is almost certainly no.",
        "It would have to swim back against the flow, through the water in the trap, and up a slippery porcelain wall.",
        "Spider experts at the Burke Museum know of no proven case of a spider getting into a house through the pipes.",
        "And the spider you find in your bathtub in the morning? It did not come up the drain.",
        "It climbed down, looking for a drink of water. And then it could not climb back out of the slippery tub.",
    ]},
    {"id": "home", "frases": [
        "And here is the twist.",
        "That spider on your toilet was probably not an intruder from outside.",
        "Many house spiders spend their entire lives indoors, in quiet corners, eating flies, gnats and even mosquitoes.",
        "It was not breaking in. It lived there. You just met it for the first time.",
        "And to send it away, you used about a gallon and a half of clean water. Roughly what you drink in two or three days.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do next time?",
        "Grab a cup and a piece of paper. Put the cup over the spider, slide the paper underneath, and carry it out.",
        "A garage or a porch is perfect. Many house spiders struggle out in the open cold.",
        "Or, honestly, just let it be. It is one more hunter in the house, working the night shift for free.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you meet a spider on the toilet at midnight, remember where the flush really sends it.",
        "Not into thin air. Into a long, dark water slide, and a very bad night.",
        "A cup and a piece of paper. That is all it takes.",
    ]},
]
