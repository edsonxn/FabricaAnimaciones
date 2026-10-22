# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «Never Kill the Big Yellow Spider in Your Garden»  Motor SECUENCIA, ~9 min.
Vuelta al formato ganador del canal («Never Kill» de UN solo bicho: `ciempies_casa` ×37; las listas dieron ×0,49).
Variable probada: el lugar (jardín/porche en vez de dentro de la casa). Referencias: Garden Whispers «If You See This
Yellow Giant Spider on Your Porch, Do Not Kill It» (×1,8, 7 k) y la serie «Never Kill This Spider» de The-Wild-Discovery.
Primeros ~70 s en VIDEO: 7 clips de 10 s = 49 puntos (saldo leído en Flow el 22-oct-2026: 50), dos escenas por clip.
Hechos usados (Argiope aurantia, familia Araneidae; Univ. of Florida IFAS «Featured Creatures», Penn State Extension,
Univ. of Kentucky Entomology, Missouri Dept. of Conservation; Foellmer & Fairbairn 2003, muerte espontánea del macho):
nombres comunes yellow / black-and-yellow garden spider, writing spider, zipper spider, corn spider, banana spider;
EE. UU. contiguo, sur de Canadá, México y Centroamérica; hembra 19-28 mm de cuerpo, macho 5-9 mm (~1/4) y pardo;
cabeza abajo en el centro, patas juntas por pares en X; tela orbicular de hasta ~60 cm en sitios soleados; muchas
noches come y reconstruye la parte central de la tela (recicla la proteína de la seda); radios secos, espiral
pegajosa; vista pobre, caza por vibración; envuelve a la presa girándola y luego muerde; presas hasta de su tamaño o
mayores: saltamontes, moscas, polillas, escarabajos, abejas, avispas; estabilimento en zigzag (hipótesis: aviso a aves,
UV que atrae insectos, camuflaje; sin consenso); leyenda sureña del «writing spider» que escribe tu nombre; si la
molestan sacude la tela o se deja caer; el macho teje una tela pequeña junto a la de ella y punteá los hilos; el
corazón del macho se detiene durante la cópula y su cuerpo queda unido a ella (tapón); sacos de huevos pardos y
papiráceos de ~2,5 cm, cientos a más de mil huevos cada uno, varios por hembra; la hembra muere con la primera helada
(vive una temporada); las crías nacen dentro del saco, pasan el invierno ahí y en primavera se dispersan en globo de
seda; mordida no agresiva, como picadura de abeja en un adulto sano; araña Joro (Trichonephila clavata, de Asia, sureste
de EE. UU.): franjas amarillas y azuladas, mancha roja debajo, tela dorada sin zigzag; ambas inofensivas para la gente.
"""

TITULO = "Never Kill the Big Yellow Spider in Your Garden"
ARCHIVO = "yellow_garden_spider"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falsos positivos de Whisper: «sack» por «sac» y «stablementum» por «stabilimentum»; las tomas dicen bien la palabra
CER_MAX_POR_FRASE = {"zigzag_2": 0.03, "eggs_2": 0.015, "eggs_5": 0.015}

SECUENCIA = dict(
    clips_s=[10] * 7,         # 7 x 10 s (7 puntos) = 49 de los 50 puntos, 70 s de video
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={"scene-001": 0},   # el clip 1 trae tarareo y «huh?» del personaje (Whisper)
    # marco redondeado blanco al principio de los clips 1, 2, 4 y 7 (hoja previews/_clips.jpg)
    recorte_por={"scene-001": 0.035, "scene-002": 0.035, "scene-004": 0.035, "scene-007": 0.035},
    carpeta_descargas="flow-arana_amarilla",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "garden": "a cartoon yellow garden spider with a big oval abdomen striped in bright lemon yellow and glossy black, "
                  "a small silvery-white head with two big round friendly eyes, eight long legs that are black with "
                  "orange-brown bands near the body, and a tiny green straw sun hat",
        "male": "a tiny cartoon male garden spider, a quarter of her size, plain light brown with thin legs, a nervous "
                "smile and a tiny red bow tie",
        "joro": "a cartoon Joro spider with a long body striped in yellow and dark blue, a red patch under the belly, "
                "long thin legs with yellow bands, and no hat",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a big round orb web with neat straight spokes and an even spiral, and one bright white vertical zigzag band "
           "of thick silk through its center",
    epoca="present-day American backyard garden at the end of summer: tomato plants, tall sunflowers, a wooden porch, "
          "a white picket fence",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Playful, sunny nature documentary score for a hand-drawn cartoon about a big garden spider: pizzicato strings, "
           "marimba, acoustic guitar, soft clarinet, celesta, felt piano, light brushed percussion and upright bass. Warm, "
           "curious and a little mischievous, with moments of comic suspense. Never epic, never horror.",
    escenas={
        "hook": ("Bright summer morning, birds implied by flute trills, then a sudden comic freeze and a small mysterious celesta figure.", 3),
        "who": ("Light and inquisitive: marimba ostinato starts, upright bass walks gently, introducing a big character.", 4),
        "web": ("Delicate and precise: celesta and harp-like pizzicato building a pattern, round and repeating like a wheel.", 4),
        "hunt": ("Quick comic action: a sudden pizzicato burst, spinning marimba runs, then a satisfied little cadence.", 6),
        "zigzag": ("Spooky campfire tale turned playful mystery: a low clarinet legend melody, then curious questioning celesta.", 4),
        "shake": ("Wobbly and funny: trembling tremolo strings and bouncing marimba, then a quick drop.", 6),
        "males": ("Shy little serenade on plucked guitar, a tender comic moment that ends in a gentle hush.", 3),
        "eggs": ("Tender and wintry: felt piano and soft strings, a lullaby that warms into spring.", 2),
        "bite": ("Relaxed debunking groove: walking bass and brushes, reassuring and light.", 4),
        "tell": ("Clear and focused: a simple two-part pizzicato and clarinet pattern, like a quick lesson.", 4),
        "deal": ("Practical and friendly: light guitar and piano, calm and helpful.", 3),
        "outro": ("Return to the opening summer theme, now warm and resolved: celesta and felt piano, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "who", "web"],
         "Begin from near silence. End on a held suspenseful tone that can flow into the next piece. No loud ending."),
        (["hunt", "zigzag", "shake"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["males", "eggs", "bite"],
         "Begin gently with a held tone. End on a sustained calm chord that can flow into the next piece."),
        (["tell", "deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is a warm morning at the end of summer. You step outside to water the tomatoes.",
        "And right there, between two plants, you almost walk face first into it.",
        "A huge round web, nearly as wide as a bicycle wheel, glittering with dew.",
        "And in the middle, hanging head down, is the biggest spider you have ever seen in your yard.",
        "Bright yellow and black. Long striped legs. And a strange white zigzag running straight through the web.",
        "Your first thought is to grab a stick, or the hose, or the bug spray.",
        "Don't.",
        "Because that spider is one of the hardest working pest hunters in your entire garden.",
        "It catches the grasshoppers chewing your plants. The flies. The moths. Even wasps.",
        "And it really cannot hurt you.",
        "But there is an old story about this spider, told for generations in the American South.",
        "It says this spider can write. And if it ever writes your name in its web, you do not have long to live.",
        "We will get to that zigzag. Because the real reason it is there is a mystery that scientists are still arguing about.",
    ]},
    {"id": "who", "frases": [
        "First, let's meet her. And yes, it is a her.",
        "This is the yellow garden spider, also called the black and yellow garden spider.",
        "Depending on where you live, people call her the writing spider, the zipper spider, the corn spider, or the banana spider.",
        "She lives across almost all of the United States, southern Canada, Mexico, and Central America.",
        "A grown female can have a body more than an inch long. With her legs stretched out, she can cover the palm of your hand.",
        "The males? Tiny. About a quarter of her size, and plain brown. Most people never even notice them.",
        "She sits in the center of her web almost all day, head down, holding her legs together in pairs, so she looks like a big letter X.",
    ]},
    {"id": "web", "frases": [
        "Now look at that web.",
        "It is an orb web, the classic wheel with spokes and a sticky spiral, and it can be up to two feet across.",
        "She builds it in sunny, open spots. Between tall plants, along fences, under the edge of the porch, wherever insects fly through.",
        "And here is the surprising part. On many nights, she takes down the center of her web, and builds it again.",
        "She does not waste the old silk. She eats it.",
        "Silk is made of protein, and protein is precious. So she recycles it, and uses it to spin fresh threads.",
        "The spokes are dry, so she can walk on them. The spiral is sticky, so the insects cannot walk away.",
        "She cannot see very well. She hunts by touch, feeling every tiny vibration through her legs.",
        "So the whole web is a giant trap, and a giant ear, at the same time.",
    ]},
    {"id": "hunt", "frases": [
        "So what happens when something hits the web?",
        "A grasshopper jumps, misses the leaf, and lands right in the spiral.",
        "In a heartbeat, she runs across the spokes.",
        "She grabs the insect with her legs and spins it around and around, wrapping it in silk like a tiny mummy.",
        "Only then does she bite, and her venom stops the struggling.",
        "She can tackle insects as big as she is, or even bigger. Grasshoppers, moths, flies, beetles, and even bees and wasps.",
        "Then she carries the package back to the center, and saves it for later.",
        "Over a whole summer, one garden spider catches a lot of insects. Many of them are the ones that chew on your vegetables.",
        "That is why so many gardeners are happy to see her move in.",
    ]},
    {"id": "zigzag", "frases": [
        "Now, about that zigzag.",
        "Right through the center of the web, there is a thick band of white silk, going up and down like a zipper.",
        "Scientists call it a stabilimentum. And it is where the writing spider got its name.",
        "In the old Southern story, those zigzags are letters.",
        "If the spider writes your name in its web, so the story goes, you are going to die.",
        "Of course, the spider is not writing anything. It does not know your name, and it does not know how to spell.",
        "No one has ever died because of a zigzag. It is just a spooky story, passed down from grandparents to grandkids.",
        "But here is the strange part. Scientists still do not fully agree on why she makes it.",
        "One idea is that it is a warning sign for birds, like a sticker on a glass door, so they do not fly through and wreck the web.",
        "Another is that it reflects ultraviolet light, which some insects are drawn to, so it might lure dinner closer.",
        "A third idea is that it helps hide her, breaking up the outline of her body.",
        "It might do all three. For now, it is one of the most famous little mysteries in the spider world.",
    ]},
    {"id": "shake", "frases": [
        "And when something big gets too close, like a bird, a curious dog, or your hand, she has a trick.",
        "She grabs the web and shakes it, hard, until the whole thing is swinging back and forth.",
        "To a predator, she suddenly looks bigger, and she is much harder to grab.",
        "And if that does not work, she simply drops to the ground and hides in the leaves.",
    ]},
    {"id": "males", "frases": [
        "Now, remember that tiny male.",
        "In late summer, he goes looking for a female, and builds a small web right next to hers.",
        "Then he carefully plucks her threads with a special rhythm, so she knows he is not dinner.",
        "And scientists discovered something incredible about these males.",
        "During mating, his heart simply stops. He dies, and she did not even have to touch him.",
        "His body stays attached to her, which makes it harder for any other male to take his place.",
    ]},
    {"id": "eggs", "frases": [
        "By early fall, she gets to work on the most important thing she will ever build.",
        "She weaves a round, brown, papery egg sac, about an inch across, and hangs it in the web or close by.",
        "Each sac can hold hundreds of eggs, sometimes more than a thousand. And she may make several.",
        "Then she guards them, for as long as she can.",
        "When the first hard frost of the year arrives, she dies. Most yellow garden spiders live for just one summer.",
        "But the babies hatch inside the sac, and they wait there, all winter long, safe inside that ball of silk.",
        "In the spring, they climb out, let a thread of silk catch the wind, and float away to find gardens of their own.",
        "So if you find one of those brown sacs on your porch this winter, please leave it alone. That is next year's pest control.",
    ]},
    {"id": "bite", "frases": [
        "But wait. A spider this big must be dangerous, right?",
        "Not really. The yellow garden spider is not aggressive, and it would much rather run than bite.",
        "It only bites if it is grabbed or squeezed.",
        "And even then, for a healthy adult, it feels like a bee sting. A little red, a little swollen, and gone soon after.",
        "Its venom is made for grasshoppers, not for people.",
    ]},
    {"id": "tell", "frases": [
        "So how do you know you are looking at a yellow garden spider?",
        "Here is the quick check.",
        "A big round web in a sunny spot, a white zigzag in the middle, and a black and yellow spider hanging head down at the center.",
        "Lately, people in the Southeast have also started seeing another big yellow spider. The Joro spider, a newcomer from Asia.",
        "The Joro has yellow and bluish stripes, a red patch underneath, and a golden web with no zigzag.",
        "Both of them are harmless to you. And both of them eat a lot of bugs.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do when you find one?",
        "The easiest answer is nothing. Let her work.",
        "If her web is right across a doorway or a path, gently move her with a stick to a bush nearby. She will build again.",
        "Skip the bug spray. It kills the hunters along with the pests, and the pests come back much faster.",
        "And if you want more of them, leave some tall plants and flowers standing. That is all she needs.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you step into your garden and see that big yellow spider in her web, take a second look.",
        "She is not writing your name.",
        "She is guarding your tomatoes, catching the bugs you do not want, and building a fresh trap almost every night.",
        "In a few months she will be gone, and she will leave you hundreds of tiny helpers for next spring.",
        "So put down the stick, step around the web, and let her finish her summer.",
    ]},
]
