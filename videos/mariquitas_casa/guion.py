# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens to the Ladybugs Hiding in Your House This Winter?»  Motor SECUENCIA, ~4 min.
Video 2 de la tanda de la FÓRMULA NUEVA (canales/formula/wild_next_door.md § «Revisión 22-oct»): pregunta «What
Happens…», ~4 min, estructura de Zyka, el bicho en una situación humana reconocible (aquí: «snowbirds» que vuelven cada
invierno a la misma casa). Temporada: las invasiones de oct-nov. Ref.: Miniminuteman «Why Your House Is Full of
Ladybugs» (3,6 M, Short). Todo imagen (0 puntos de Flow).
Hechos usados y fuentes:
- University of Kentucky Entomology, ENTFACT-416 (Potter et al.), «Asian Lady Beetle Infestation of Structures»: llegan
  sept-nov (sobre todo octubre), tardes soleadas tras días frescos (≥ mediados de 60 °F); prefieren lados soleados que
  miran al suroeste, contraste claro-oscuro y casas junto a bosques o campos; entran por rendijas de 1/8 de pulgada; se
  juntan en áticos y huecos de pared; reaparecen en días templados y a finales del invierno cerca de ventanas y lámparas;
  no se reproducen dentro, no dañan madera, comida ni ropa; muerden como un pinchazo; líquido amarillo maloliente de las
  articulaciones de las patas que mancha; aspirarlas con un pañuelo entre la manguera y la bolsa para soltarlas fuera;
  sellar en verano; no insecticidas dentro; primeras poblaciones en EE. UU. en Luisiana en 1988; liberaciones del USDA
  desde los 60 hasta los 90; quizá llegaron también en un carguero de Japón a Nueva Orleans.
- Clemson HGIC y University of Maine Extension: se agregan en octubre-noviembre; no se alimentan ni ponen huevos dentro.
- Ohio State Extension: decenas de miles liberadas por el USDA-ARS a fines de los 70 y 80; ya en 1916 hubo liberaciones.
- En Asia pasan el invierno en grietas de acantilados y rocas soleadas (Penn State Extension).
- Marca en «M» o «W» detrás de la cabeza; color de canela a rojo; las mariquitas nativas suelen invernar fuera, en la
  hojarasca. Señales químicas que quedan de años anteriores (Journal of Entomological Science, 2000) pueden guiar a las
  nuevas a los mismos sitios.
"""

TITULO = "What Happens to the Ladybugs Hiding in Your House This Winter?"
ARCHIVO = "ladybugs_winter"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falso positivo de Whisper: oye «packed together» por «pack together»; las tomas dicen bien la frase
CER_MAX_POR_FRASE = {"inside_2": 0.04}

SECUENCIA = dict(
    video_s=0,
    clip_s=8,
    img_s=3.5,
    rapido_hasta=300,
    img_s_lento=4.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-mariquitas_casa",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "beetle": "a cartoon Asian lady beetle with a shiny round orange shell with black spots, a white head with a small "
                  "black M-shaped mark, big round cheerful eyes, short black legs, and a tiny red and white knitted "
                  "winter scarf",
        "native": "a cartoon native ladybug with a bright red shell, seven black spots, a black head with two white "
                  "cheek spots, big round eyes, and no scarf",
        "human": "a simple cartoon woman with a round white head, dot eyes, round glasses, short gray hair and a "
                 "lavender cardigan",
    },
    objeto="a light-colored two-story wooden house with dark green shutters, next to a wooded field",
    epoca="present-day American countryside home in autumn, orange and yellow trees, late afternoon sun",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

LYRIA = dict(
    estilo="Cozy, curious cartoon nature documentary score about ladybugs moving into a house for the winter: pizzicato "
           "strings, marimba, glockenspiel, soft clarinet, felt piano, light brushed percussion and upright bass. Warm, "
           "autumnal and a little mischievous. Never epic, never horror.",
    escenas={
        "hook": ("Golden autumn afternoon, a busy buzzing pizzicato swarm, then a comic pause and a curious glockenspiel question.", 3),
        "who": ("A playful reveal with a slightly exotic pentatonic marimba hint, then a brisk travelling theme.", 4),
        "choose": ("A house-hunting tune: bouncy upright bass and clarinet, picky and funny.", 4),
        "inside": ("Sleepy and cozy: felt piano, soft strings, slow breathing rhythm, a winter lullaby.", 2),
        "wake": ("Gentle confusion: a warm sunny melody that stumbles, then fades to a lonely quiet tone.", 3),
        "defense": ("Funny and a bit gross: a squelchy bassoon, a sneaky pizzicato, a comic sting.", 6),
        "spring": ("Bright spring awakening: flute-like celesta and marimba, hopeful and light.", 4),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening autumn theme, warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "who", "choose"],
         "Begin from near silence. End on a held curious tone that can flow into the next piece. No loud ending."),
        (["inside", "wake", "defense"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["spring", "deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is a sunny afternoon in October. You walk outside, and the whole side of your house is moving.",
        "Hundreds of little orange beetles, crawling on the siding, buzzing around the window frames.",
        "A week later, they are gone. Except for the one walking across your ceiling. And the three on your kitchen window.",
        "So where did all the others go? What are they doing inside your walls all winter? And why did they pick your house?",
        "Here is the first surprise. Those are probably not ladybugs at all.",
    ]},
    {"id": "who", "frases": [
        "Look closely at the head. See that little black mark, shaped like an M?",
        "That is an Asian lady beetle. A cousin of the ladybug, from China, Korea and Japan.",
        "Its shell can be tan, orange or red, with lots of spots, or no spots at all.",
        "And it is here partly because of us. For decades, the United States Department of Agriculture released them on purpose, to eat crop pests.",
        "The first wild population turned up in Louisiana in nineteen eighty-eight. Now they live in almost every state.",
    ]},
    {"id": "choose", "frases": [
        "So why your house?",
        "Back home in Asia, these beetles spend the winter in cracks in sunny, rocky cliffs.",
        "And to a lady beetle, your house looks a lot like a cliff.",
        "They love the sunny side that faces southwest. Light siding with dark shutters. A house next to woods or fields.",
        "And many scientists think the scent left behind by last year's beetles helps lead new ones to the very same spots.",
        "In other words, they are snowbirds. And your house is their winter condo.",
    ]},
    {"id": "inside", "frases": [
        "Getting in is easy. A gap thinner than a pencil lead around a window, a vent, or under the siding is plenty.",
        "Then they crawl deep into the attic and the hollow spaces inside your walls.",
        "There, they pack together in big clusters, and shut almost everything down.",
        "They do not eat. They do not lay eggs. They do not chew your wood. They just wait, barely moving, for months.",
    ]},
    {"id": "wake", "frases": [
        "But your house has a problem. It is warm.",
        "On a mild winter day, or when the heat comes on, some of them wake up too early.",
        "They think spring is here. So they crawl toward the light, out of the baseboards, the ceiling lights, and onto your windows.",
        "And that is the sad part. Inside a heated house, there is nothing to eat, and the air is very dry.",
        "Many of those early risers never make it to spring.",
    ]},
    {"id": "defense", "frases": [
        "Now, before you grab one, a warning.",
        "When a lady beetle is squeezed or scared, it bleeds a yellow liquid from its knees.",
        "It smells terrible, it tastes awful to birds, and it can stain your curtains and walls.",
        "And yes, these beetles can bite. It feels like a tiny pinprick. Annoying, but not dangerous.",
    ]},
    {"id": "spring", "frases": [
        "The ones that do survive wait for real spring.",
        "When the days get longer, they head for the windows again, this time to get out.",
        "They fly back to the trees and the fields, and go right back to work, eating aphids, the tiny bugs that suck the life out of plants.",
        "That is why farmers wanted them in the first place. Outside, they are great at their job.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do with the beetles on your window?",
        "Do not squish them, and do not sweep them. That is how you get the smell and the stains.",
        "Vacuum them up instead. Tuck a handkerchief between the hose and the bag, and you can shake them out outside.",
        "And the real fix comes in summer. Seal the little gaps around windows, vents and siding, before October comes back.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you see one walking across your ceiling in the middle of winter, remember what it is.",
        "Not an invader. A snowbird that woke up too early, looking for the way out.",
        "Open the window for it in spring. It has aphids to catch.",
    ]},
]
