# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens to the Colony After You Squish the Ants on Your Counter?»  SECUENCIA, ~4 min.
Video 4 de la tanda de la FÓRMULA NUEVA (canales/formula/wild_next_door.md § «Revisión 22-oct»). Ángulo humano: los
repartidores de comida a domicilio; aplastas a unos cuantos, pero el pedido sigue en la app (el rastro) y el restaurante
manda más. Ref.: Clem Reveals «The Ant Colony Inside Your Walls Is Growing Bigger Every Single Day» 695 K (×228).
Hechos usados y fuentes:
- Utah State University Extension, «Odorous house ant»: Tapinoma sessile, olor a coco podrido al aplastarla; varias reinas;
  forma subcolonias por gemación (budding); no se pelean con las subcolonias emparentadas.
- Oregon State University (materiales de extensión sobre hormigas): los tratamientos de acción rápida, como los
  piretroides, suelen fracturar el nido; se recomiendan cebos.
- Proporción de forrajeras: en hormigas cosechadoras sudamericanas, 7-15 % de las obreras (marcaje-recaptura y
  excavación de colonias); en muchas especies las obreras pasan de tareas internas a forrajear al final de su vida.
- Rastro de feromonas: las obreras marcan el camino al alimento y las demás lo siguen; limpiarlo con agua y jabón lo borra.
- Wilson, Durlach & Roth (1958), Psyche 65: «Chemical releasers of necrophoric behavior in ants» (DOI 10.1155/1958/69391, Crossref): el ácido oleico de los
  cadáveres hace que las obreras los lleven al basurero; objetos untados con él también; reportaron que incluso obreras
  vivas untadas eran llevadas al basurero (Gordon 1983 lo discute).
- Los cebos lentos funcionan porque las obreras los cargan al nido y los comparten boca a boca (trofalaxia) con reinas
  y larvas.
"""

TITULO = "What Happens to the Colony After You Squish the Ants on Your Counter?"
ARCHIVO = "ants_counter"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falso positivo de Whisper: «E.O. Wilson» / «1950s»; la toma dice bien la frase
CER_MAX_POR_FRASE = {"dead_1": 0.03}

SECUENCIA = dict(
    video_s=0,
    clip_s=8,
    img_s=3.5,
    rapido_hasta=300,
    img_s_lento=4.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-hormigas_cocina",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "ant": "a cartoon small dark brown house ant with a shiny round head, big round determined eyes, bent antennae, "
               "six thin legs, and a tiny orange delivery cap",
        "queen": "a cartoon queen ant, bigger and dark brown, with a long shiny abdomen, big kind eyes and a tiny golden "
                 "crown",
        "human": "a simple cartoon woman with a round white head, dot eyes, a brown ponytail, a yellow apron and pink "
                 "rubber gloves",
    },
    objeto="a bright American kitchen counter with a sugar bowl, a sticky spoon, a few crumbs, a sink and a window",
    epoca="present-day American home kitchen in the morning, warm sunlight",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

LYRIA = dict(
    estilo="Busy, clever cartoon nature documentary score about an ant colony behind a kitchen wall: pizzicato strings, "
           "marimba, xylophone, bassoon, soft clarinet, felt piano, light brushed percussion and upright bass. Bustling, "
           "witty and warm. Never epic, never horror.",
    escenas={
        "hook": ("A busy morning kitchen, a marching pizzicato line of tiny steps, then a comic squish sting and silence.", 6),
        "trail": ("A sneaky following melody: clarinet leading, pizzicato copying it step by step.", 4),
        "few": ("Revealing scale: a small melody that keeps adding layers until it becomes a big busy city.", 4),
        "smell": ("Funny and odd: a squelchy bassoon and a tropical coconut marimba hint.", 6),
        "split": ("Comic chaos: the march breaks into many smaller marches going in different directions.", 6),
        "dead": ("Gentle and curious funeral march, light and strange, ending with a surprised plink.", 3),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening marching theme, warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "trail", "few"],
         "Begin from near silence. End on a held curious tone that can flow into the next piece. No loud ending."),
        (["smell", "split", "dead"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is seven in the morning. You walk into the kitchen, and there they are again.",
        "A perfect line of tiny ants, marching from a crack by the window, straight to the sugar bowl.",
        "So you do what everyone does. You squish them. All of them. Thumb, paper towel, done.",
        "By lunch, the line is back. Same crack. Same sugar bowl.",
        "So what actually happens to the colony when you squish the ants on your counter? And why does it never work?",
        "The short answer is, the ants you see are not the colony. Not even close.",
    ]},
    {"id": "trail", "frases": [
        "First, how did they find your sugar in the first place?",
        "One scout wandered out, found it, and walked home, dragging her belly on the counter to leave an invisible scent trail.",
        "Every ant that follows the trail and finds food adds more scent. So the trail gets stronger and stronger.",
        "Think of it like a food delivery app. The order is on the screen, and the drivers just follow the map.",
        "Squishing a few drivers does not cancel the order. The map is still there, and the restaurant sends more.",
    ]},
    {"id": "few", "frases": [
        "And the restaurant is huge.",
        "In some ant species, scientists have counted the foragers, and found they are only seven to fifteen percent of all the workers.",
        "In many species, the ones sent outside are the older workers, near the end of their lives. To the colony, they are the most expendable.",
        "Meanwhile, deep inside your wall, there are nurses, builders, baby ants, and the queen. Sometimes many queens.",
        "So when you squish twenty ants on the counter, the colony barely notices.",
    ]},
    {"id": "smell", "frases": [
        "Now, here is a weird test. Next time, smell your fingers.",
        "If it smells like rotten coconut, you just met the odorous house ant, one of the most common kitchen ants in America.",
        "That smell comes from defensive chemicals in its body. And to other ants, chemicals like that can mean danger.",
    ]},
    {"id": "split", "frases": [
        "And here is where it gets worse. Say you lose patience and blast the line with bug spray.",
        "With some house ants, a fast-acting spray can make the colony do something strange. It splits.",
        "A few queens and a crowd of workers pack up and move out, and start new nests somewhere else.",
        "Odorous house ants are famous for this. One colony in your wall can quietly turn into three.",
        "And since they are all relatives, they do not fight each other. They just share your kitchen.",
    ]},
    {"id": "dead", "frases": [
        "So what happens to the ants you squished? Their sisters come and carry them away.",
        "In the nineteen fifties, the famous ant scientist E. O. Wilson figured out how they know a nestmate is dead.",
        "A dead ant gives off a fatty acid called oleic acid. Ants smell it, and haul the body to the colony trash pile.",
        "His team even reported that a living ant, painted with that acid, got carried out to the trash, kicking and very much alive.",
    ]},
    {"id": "deal", "frases": [
        "So what actually works?",
        "First, wipe the trail with soapy water. That erases the map, so new ants cannot follow it.",
        "Then put the sugar in a sealed jar. No order, no delivery.",
        "And if they keep coming, use a slow ant bait instead of spray.",
        "The workers carry it home and share it mouth to mouth, all the way to the queens. That is how you reach the colony you never see.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you see that perfect line on your counter, remember what you are looking at.",
        "Not the army. Just a few delivery drivers, following a map.",
        "Erase the map, and close the restaurant.",
    ]},
]
