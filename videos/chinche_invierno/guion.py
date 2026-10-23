# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens If You Let a Stink Bug Live in Your House All Winter?»  SECUENCIA, ~4 min.
Video 3 de la tanda de la FÓRMULA NUEVA (canales/formula/wild_next_door.md § «Revisión 22-oct»). Ángulo humano: el
compañero de cuarto que no paga renta, duerme todo el invierno y se va en primavera. Temporada: oct-nov. Refs.: Fields of
Return «Never Kill the Stink Bug on Your Window» 660 K (×1711); Frank Taylor «Stink Bugs in Your House?» 2,6 M.
Giro honesto: dentro de casa es inofensiva, pero fuera es una plaga de cultivos; el consejo es el frasco con agua y jabón.
Hechos usados y fuentes:
- Inkley, D. B. (2012), Journal of Entomological Science 47(2): 125-130, «Characteristics of Home Invasion by the Brown
  Marmorated Stink Bug»: 26 205 adultos recogidos dentro de UNA casa de Maryland en 181 días; salían de los huecos de las
  paredes a las habitaciones en los días más cálidos de lo normal. (DOI 10.18474/0749-8004-47.2.125, verificar en Crossref)
- Mental Floss / Penn State: Halyomorpha halys, nativa del este de Asia; primeros ejemplares en Allentown, Pensilvania, en
  1998; hoy hasta 47 estados; adultos de hasta ~2/3 de pulgada, antenas y patas con bandas blancas; viven hasta ocho meses;
  olor de trans-2-octenal y trans-2-decenal (este también da su olor al cilantro); más de 100 cultivos; 37 millones de
  dólares en manzanas del Atlántico medio en 2010; entran por rendijas de más de 7 mm; diapausa; no se aparean dentro ni
  dañan la casa; no pican ni muerden; el olor puede irritar a algunas personas y hacer babear o vomitar a las mascotas;
  trampa de Virginia Tech: bandeja con agua jabonosa bajo una luz en un cuarto oscuro, 14 veces más que las comerciales;
  avispa samurái (Trissolcus japonicus) parasita 60-90 % de sus huevos en Asia; apareció en Maryland en 2014.
- University of Kentucky Extension (ENTFACT-326): olor parecido al cilantro; llegan de fines de septiembre a mediados de
  octubre.
"""

TITULO = "What Happens If You Let a Stink Bug Live in Your House All Winter?"
ARCHIVO = "stinkbug_winter"
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
    carpeta_descargas="flow-chinche_invierno",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "bug": "a cartoon brown marmorated stink bug with a mottled brown shield-shaped body, small white bands on its "
               "antennae and legs, big round sleepy eyes, and a tiny gray knitted beanie hat",
        "human": "a simple cartoon man with a round white head, dot eyes, a short gray beard, glasses and a plaid flannel "
                 "shirt",
        "wasp": "a tiny cartoon samurai wasp, shiny black, with a small white headband and big determined eyes",
    },
    objeto="a cozy American living room in winter with a reading lamp, a sofa, a window with frost, and a warm radiator",
    epoca="present-day American suburban home in late autumn and winter",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

LYRIA = dict(
    estilo="Cozy, wry cartoon nature documentary score about a clumsy stink bug spending the winter in a house: "
           "pizzicato strings, bassoon, tuba, marimba, felt piano, soft clarinet, light brushed percussion. Comic, warm, "
           "a little grumpy. Never epic, never horror.",
    escenas={
        "hook": ("Quiet winter evening by a lamp, then a clumsy buzzing bassoon flying in circles and a comic bump.", 3),
        "who": ("A brisk travelling theme with a slight Asian pentatonic color, arriving on a busy cargo ship rhythm.", 4),
        "invade": ("A growing march of tiny footsteps: pizzicato that multiplies, comic and a bit overwhelming.", 6),
        "winter": ("Sleepy hibernation lullaby: felt piano, slow tuba breathing, very still.", 2),
        "warm": ("A warm sunny day melody that wakes up clumsily, buzzing and bumping into things.", 6),
        "smell": ("Funny and gross: squelchy bassoon, a sneaky clarinet, a surprised sting.", 6),
        "spring": ("Spring awakening that turns a little worrying: bright marimba, then a low tuba note for the farms.", 4),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the cozy winter theme, warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "who", "invade"],
         "Begin from near silence. End on a held curious tone that can flow into the next piece. No loud ending."),
        (["winter", "warm", "smell"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["spring", "deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is a cold night in November. You are reading by the lamp, and something starts buzzing around the shade.",
        "A brown, shield-shaped bug. It flies like a drunk helicopter, bonks into the lamp, and lands on your sleeve.",
        "Your first thought is to squish it, or flush it.",
        "But what if you just let it be? What happens to a stink bug that spends the whole winter in your house?",
        "The short answer is, almost nothing. And that is the strange part.",
    ]},
    {"id": "who", "frases": [
        "This is the brown marmorated stink bug. Look for the little white bands on its antennae and legs.",
        "It is not from here. It comes from East Asia.",
        "The first ones in America were collected in Allentown, Pennsylvania, in nineteen ninety-eight. Probably stowaways in a shipping container.",
        "Today they live in as many as forty-seven states.",
    ]},
    {"id": "invade", "frases": [
        "Every fall, when the nights get cold, they go looking for a place to spend the winter.",
        "And a warm house, full of tiny gaps around windows, doors and air conditioners, is perfect.",
        "Once a few find a good spot, they give off a chemical signal that invites their friends.",
        "One man in Maryland collected every stink bug he found inside his home, every single day, for six months.",
        "His final count was more than twenty-six thousand. In one house.",
    ]},
    {"id": "winter", "frases": [
        "So what do they do in there? Mostly, they sleep.",
        "They tuck themselves into wall spaces, attics and behind the siding, and slip into a deep winter rest called diapause.",
        "They do not eat your food. They do not mate. They do not lay eggs. They do not chew your house.",
        "It is like having a roommate who pays no rent, never cooks, never talks, and sleeps from Halloween to Easter.",
    ]},
    {"id": "warm", "frases": [
        "The trouble starts on warm days.",
        "When the sun heats the walls, or the furnace runs, some of them wake up, confused, and wander out into your rooms.",
        "The Maryland study found the same thing. More bugs came out on days that were warmer than normal.",
        "So they buzz toward your lamps and windows, slow and clumsy, because their bodies still think it is winter.",
        "Inside a dry, heated house, many of them simply run out of energy. They are found on windowsills in spring.",
    ]},
    {"id": "smell", "frases": [
        "And then there is the smell.",
        "Squeeze one, and it sprays a defensive chemical from glands on its body.",
        "Here is the weird part. One of those chemicals is the same one that gives cilantro its smell.",
        "So if cilantro tastes like soap to you, this bug is your worst nightmare.",
        "It cannot bite and it cannot sting. But the spray can irritate some people, and make a curious dog drool.",
    ]},
    {"id": "spring", "frases": [
        "When spring arrives, the survivors climb toward the light, and head back outside to mate.",
        "And this is where the story turns.",
        "Outside, this bug feeds on more than a hundred kinds of crops. Apples, peaches, tomatoes, peppers, sweet corn.",
        "In twenty ten, it damaged an estimated thirty-seven million dollars' worth of apples in the mid-Atlantic alone.",
        "Scientists have a hope, though. A tiny wasp from Asia, called the samurai wasp, that lays its eggs inside stink bug eggs.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do with the one on your sleeve?",
        "Do not squish it. Grab a jar with some soapy water, and nudge the bug in. It cannot climb out.",
        "For a crowd, try the trick from Virginia Tech. A pan of soapy water under a lamp, in a dark room, at night.",
        "And before next September, seal the gaps around your windows, doors and air conditioner.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So what happens if you let a stink bug live in your house all winter?",
        "It sleeps. It wakes up confused. And in spring, it leaves to go eat your neighbor's peaches.",
        "The perfect roommate. Until it moves out.",
    ]},
]
