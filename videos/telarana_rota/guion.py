# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «What Happens to a Spider After You Knock Down Its Web?»  Motor SECUENCIA, ~4 min.
Video 5 de la tanda de la FÓRMULA NUEVA (canales/formula/wild_next_door.md § «Revisión 22-oct»). Mismo esquema que el
éxito de Zyka «What Happens When a Wasp Comes Home but Its Nest Is Gone?» (1,1 M, ×321): «casa destruida», pero con
araña de porche. Ángulo humano: perder la casa, el refrigerador y el trabajo en el mismo minuto (la tela es las tres).
Hechos usados y fuentes:
- BBC Wildlife (Discover Wildlife), «Why do spiders eat their own webs?»: muchas arañas orbiculares rehacen la tela cada
  noche, lo que exige fabricar unos 20 metros de seda; se comen la vieja para recuperar proteína.
- Townley & Tillinghast (1988), Journal of Arachnology 16: 303: Araneus cavaticus disuelve casi toda la tela ingerida
  (marcada con radioactividad); la eficiencia de reciclaje nunca pasó de ~32 %.
- Psyche vol. 94 (Micrathena gracilis): 18 de 36 mudanzas siguieron a la destrucción de la tela; 34 de 36 a un día de
  poca comida, a la destrucción, o a ambas.
- Chmiel et al. (2000), Animal Behaviour (Argiope keyserlingi): se alejan del origen del daño; a la semana, lo que más
  pesa es cuánto comieron.
- Seda de arrastre (dragline) como cuerda de seguridad: se dejan caer y pueden volver a subir por ella (Ortlepp &
  Gosline, J. Exp. Biol.).
- Muchas arañas de casa aguantan semanas sin comer (metabolismo lento). Las telarañas polvorientas de los rincones
  suelen ser telas abandonadas. Las luces amarillas («bug lights») atraen menos insectos que las blancas.
"""

TITULO = "What Happens to a Spider After You Knock Down Its Web?"
ARCHIVO = "spider_web_gone"
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
    carpeta_descargas="flow-telarana_rota",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "spider": "a cartoon gray-brown porch orb weaver spider with a plump round abdomen with a pale leaf-shaped "
                  "pattern, eight hairy banded legs, big round expressive eyes, and a tiny yellow construction hard hat",
        "human": "a simple cartoon man with a round white head, dot eyes, short black hair, a red flannel shirt and jeans",
    },
    objeto="a round orb web with neat straight spokes and an even spiral, glistening, strung between a porch post and "
           "the porch light",
    epoca="present-day American front porch at night, a glowing porch light with moths, a wooden railing and a doormat",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 12

LYRIA = dict(
    estilo="Warm, clever cartoon nature documentary score about a porch spider rebuilding its web overnight: pizzicato "
           "strings, marimba, harp-like plucks, celesta, bassoon, soft clarinet, felt piano, light brushed percussion. "
           "Resourceful, a little bittersweet, funny. Never epic, never horror.",
    escenas={
        "hook": ("Quiet porch at night with crickets implied, a sudden comic broom swish, then a mysterious overnight celesta.", 3),
        "all": ("Reflective and a bit sad: felt piano, a small character who lost everything at once.", 2),
        "drop": ("A quick fall and a dangling pause: descending pizzicato, then a tiny bouncing recovery.", 4),
        "rebuild": ("Industrious and precise: a repeating marimba and harp pattern building up like weaving.", 4),
        "move": ("Thoughtful moving-day theme: a clarinet walking with a suitcase, wistful but hopeful.", 4),
        "cobwebs": ("Light and dusty comic interlude: a creaky bassoon and a sneeze-like pluck.", 6),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening night theme, warm and resolved, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "all", "drop"],
         "Begin from near silence. End on a held curious tone that can flow into the next piece. No loud ending."),
        (["rebuild", "move", "cobwebs"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is late. You step out on the porch, and walk face first into a spider web.",
        "You flail. You spit. You grab the broom and wipe out every thread between the post and the porch light.",
        "The spider drops out of sight. Good riddance.",
        "The next morning, you open the door, and the web is back. Same spot. Perfect circle. Like nothing happened.",
        "So what did that spider go through last night? And how did it rebuild an entire web while you were asleep?",
    ]},
    {"id": "all", "frases": [
        "First, understand what you actually destroyed.",
        "For a spider, the web is not just a house. It is the fridge, the fishing net, and the doorbell, all in one.",
        "It catches dinner. And it tells the spider, through tiny vibrations, exactly what just landed and where.",
        "So with one swipe of a broom, the spider lost its home, its food, and its job. All in the same second.",
    ]},
    {"id": "drop", "frases": [
        "But it did not lose its life.",
        "Spiders almost always trail a safety line of silk behind them, called a dragline. Like a climber's rope.",
        "When the broom came, it simply let go and dropped, paying out silk as it fell.",
        "Then it hid in a crack in the porch post, and waited for you to go inside.",
    ]},
    {"id": "rebuild", "frases": [
        "And then, in the dark, it went back to work.",
        "Many orb weaving spiders rebuild their web almost every night anyway. And a single web can take around sixty-five feet of silk.",
        "That silk is made of protein, and protein is expensive. So here is the clever part. Spiders eat their old webs.",
        "Scientists fed spiders silk marked with a radioactive tag, and then tracked where it went.",
        "The spiders digested the old silk, and some of that protein came back out as brand-new web.",
        "So that perfect circle on your porch this morning may be built partly from the web you swept away.",
    ]},
    {"id": "move", "frases": [
        "But a spider can only lose so much.",
        "In one study of orb weavers, about half of all the times a spider moved to a new spot came right after its web was destroyed.",
        "And spiders that had a bad day of hunting were even more likely to pack up and go.",
        "Another study found that spiders tend to move away from wherever the damage keeps coming from.",
        "So if you sweep the same web every single day, the spider will probably give up and move. Maybe somewhere you will never see it.",
    ]},
    {"id": "cobwebs", "frases": [
        "And what about those dusty, gray cobwebs in the corners of your ceiling?",
        "Here is a secret. Most of those are old webs that nobody lives in anymore.",
        "Once a web stops catching food, its owner moves on, and the dust moves in. Sweep those all you want.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do with a web across your front door?",
        "Take a stick, wind up the web, and let the spider ride it to a bush nearby. It will rebuild there by tonight.",
        "And here is a trick. Spiders build next to your porch light because that is where the moths are.",
        "Swap the white bulb for a yellow bug light. Fewer moths, fewer webs, and nobody gets hurt.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you walk into a web on the porch, remember who you just met.",
        "A tiny builder who lost its home, its fridge and its job in one second, and rebuilt all three before breakfast.",
        "Partly out of the old one.",
    ]},
]
