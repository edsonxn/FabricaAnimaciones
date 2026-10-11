# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «Never Kill the Spider in Your Ceiling Corner»  Motor SECUENCIA, ~9 min.
Formato ganador del canal («Never Kill», como `ciempies_casa`: 440 vistas en 2,5 días) sobre el tema que rompió la media
en 3 canales chicos (cellar spider vs. black widow: ×382 The-Wild-Discovery, ×32 Primal Roots, ×30 Garden Whispers).
Primeros ~78 s en VIDEO: 7 clips de 10 s + 1 de 8 s = 55 puntos (todo el saldo del 11-oct-2026), dos escenas por clip.
Hechos usados (Pholcus phalangioides, familia Pholcidae; UC Riverside / R. Vetter, Penn State y Univ. of Kentucky
Extension, Jackson & Brassington 1987 sobre mimetismo agresivo en Pholcus):
tres animales llamados «daddy longlegs» (opiliones = no son arañas y no tienen veneno; típulas = insectos; Pholcidae);
cuerpo de ~6-8 mm, patas 5-6 veces el cuerpo; red irregular tridimensional, no geométrica; vista pobre, caza por
vibración; araneofagia: mata viudas negras (Latrodectus) y arañas de casa más grandes; envuelve a distancia lanzando
seda con las patas traseras y muerde después; invade redes ajenas y las pulsa imitando presa (mimetismo agresivo);
defensa «whirling»: gira/vibra en la red hasta ser un borrón; mito del «más venenoso» falso (sin pruebas de veneno
fuerte, sí puede morder: prueba de TV con ardor leve de segundos); la hembra carga el saco de huevos en los quelíceros;
aguanta meses sin comer; suelta patas (autotomía); vive ~2-3 años; probable origen en Asia subtropical, hoy en edificios
de todos los continentes salvo la Antártida; muchas telarañas viejas («cobwebs») son suyas.
"""

TITULO = "Never Kill the Spider in Your Ceiling Corner"
ARCHIVO = "cellar_spider"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falsos positivos de Whisper (homófonos): «rapping» por «wrapping» y «sack» por «sac»; las tomas dicen bien la palabra
CER_MAX_POR_FRASE = {"widow_7": 0.03, "mother_1": 0.03}

SECUENCIA = dict(
    clips_s=[10] * 7 + [8],   # 7 x 10 s (7 puntos) + 1 x 8 s (6 puntos) = 55 puntos, 78 s de video
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    # marcos de tarjeta en 3, 4, 7 y 8; en el 6 Flow dibujó números de estatura en el borde izquierdo (3,5-8 % del ancho)
    recorte_por={"scene-001": 0.035, "scene-005": 0.035, "scene-003": 0.035, "scene-004": 0.035, "scene-006": 0.09, "scene-007": 0.035, "scene-008": 0.035},
    carpeta_descargas="flow-arana_techo",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "cellar": "a cartoon cellar spider with a tiny pale beige peanut-shaped body, a small round head with two big "
                  "round friendly eyes, eight extremely long hair-thin pale beige legs with thin dark bands at the knees, "
                  "and a tiny navy blue night watchman cap",
        "widow": "a cartoon black widow spider with a glossy round jet-black body, a bright red hourglass mark on its "
                 "belly, eight shorter thick black legs, narrow mean eyes and angry eyebrows",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a loose, messy, tangled three-dimensional cobweb of random crisscrossing threads with no spiral and no "
           "circular pattern, in the white corner where two walls meet the ceiling",
    epoca="present-day suburban house: bathroom, basement, garage",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Playful, curious nature documentary score for a hand-drawn cartoon about a tiny house spider: pizzicato strings, "
           "marimba, soft bassoon, celesta, felt piano, light brushed percussion and upright bass. Mischievous and warm, "
           "with moments of comic suspense. Never epic, never horror.",
    escenas={
        "hook": ("Late-night quiet: a single low bassoon note, sparse ticking pizzicato, a small mysterious celesta figure, then a bright twist.", 3),
        "who": ("Light and inquisitive: marimba ostinato starts, upright bass walks gently, a sense of introducing a character.", 4),
        "web": ("Delicate and intricate: celesta and harp-like pizzicato weaving patterns, curious and a little sneaky.", 4),
        "widow": ("Comic suspense of a duel: low pulsing strings and bassoon, slowly building tension, short dramatic pauses, ending on one triumphant chord.", 7),
        "trick": ("Sneaky and clever: tiptoeing pizzicato, muted marimba, a playful trap being set, ending with a small comic sting.", 5),
        "whirl": ("Fast and dizzy: quick swirling marimba runs and trilling flutes, a playful blur, then settling down.", 6),
        "myth": ("Playful mystery solved: questioning bassoon phrase, then a light debunking groove with pizzicato and brushes.", 4),
        "mother": ("Tender and gentle: felt piano and soft strings, warm and caring, almost a lullaby.", 2),
        "tough": ("Steady and resilient: confident walking bass, marimba, a little stubborn swagger.", 4),
        "travel": ("Wide and adventurous: flowing strings and celesta, a feeling of journeys around the world.", 5),
        "why": ("Thoughtful everyday groove: relaxed marimba and bass, a small revelation at the end.", 4),
        "tell": ("Clear and focused: a simple two-part pizzicato and bassoon pattern, light and then a little serious, like a quick lesson.", 4),
        "spray": ("A short worried turn: low muted strings and a hesitant bassoon, then hope returns.", 3),
        "deal": ("Practical and friendly: light pizzicato and piano, calm and helpful.", 3),
        "outro": ("Return to the opening night theme, now warm and resolved: celesta and felt piano, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "who", "web"],
         "Begin from near silence. End on a held suspenseful tone that can flow into the next piece. No loud ending."),
        (["widow", "trick", "whirl"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["myth", "mother", "tough", "travel"],
         "Begin gently with a held tone. End on a sustained calm chord that can flow into the next piece."),
        (["why", "tell", "spray", "deal", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is two in the morning. You get up for a glass of water.",
        "You flip on the light, and there it is, hanging in the corner of the ceiling.",
        "A tiny pale body, floating in the middle of eight impossibly long, thin legs.",
        "And a messy, dusty web that looks like it has been there for years.",
        "Your first instinct is to grab the broom.",
        "Don't.",
        "Because that fragile little spider is one of the best bodyguards your house can have.",
        "It hunts other spiders. Bigger ones. Scarier ones.",
        "Including the one spider you really do not want living in your home.",
        "The black widow.",
        "And you have probably heard a rumor about it, too. That it is secretly the most venomous spider in the world.",
        "We will get to that. Because the truth is even stranger.",
    ]},
    {"id": "who", "frases": [
        "First, which spider are we talking about?",
        "People use the name daddy longlegs for at least three completely different animals.",
        "One is the harvestman, the one you see walking across the grass outside. It is not even a spider.",
        "Another is the crane fly, a clumsy flying insect that looks like a giant mosquito.",
        "And the third is the one in your ceiling corner. The cellar spider.",
        "Its body is about the size of a grain of rice.",
        "But its legs can be five or six times longer than its body, with thin dark bands at every knee.",
    ]},
    {"id": "web", "frases": [
        "Now look at that web.",
        "It is a tangled, three dimensional mess. No neat spiral, no pattern, just threads going everywhere.",
        "It looks abandoned. It is not.",
        "That chaos is the trick.",
        "A mosquito flying into the corner hits several threads at once, from different angles, and gets tangled.",
        "And when another spider walks into it, every step shakes the threads.",
        "The cellar spider cannot see very well. It hunts by touch, feeling those vibrations through its long legs.",
        "So that ugly web is really an alarm system.",
        "And the spider hangs upside down in the middle of it, all day long, waiting.",
        "Most of its hunting happens at night, while you are asleep.",
    ]},
    {"id": "widow", "frases": [
        "So how does a spider this fragile beat a black widow?",
        "On paper, it should lose.",
        "A black widow is heavier, its venom is much stronger, and its bite can send a person to the hospital.",
        "But the cellar spider has one huge advantage. Reach.",
        "Those long legs let it fight from a distance, where the widow cannot touch it.",
        "When the widow stumbles into the tangle, the cellar spider does not rush in.",
        "It stays back, and it uses its long back legs to fling silk at its enemy, strand after strand.",
        "It keeps wrapping, faster and faster, until the widow can barely move.",
        "Only then does it step in, and deliver one careful bite.",
        "Spider experts have watched cellar spiders kill black widows, and house spiders much bigger than themselves.",
        "That is why some of them actually recommend leaving cellar spiders alone in garages and basements, right where widows like to hide.",
    ]},
    {"id": "trick", "frases": [
        "And sometimes, the cellar spider does not wait for its enemy to come.",
        "It walks right into another spider's web, and gently plucks the threads.",
        "To the owner, that vibration feels exactly like an insect that just got stuck.",
        "So the owner comes running to grab its dinner.",
        "And dinner is waiting for it.",
        "Scientists call this aggressive mimicry. It is like a hunter using a duck call, except the duck is a spider.",
    ]},
    {"id": "whirl", "frases": [
        "Of course, the cellar spider has enemies too.",
        "So it has one of the strangest defenses of any spider.",
        "When something big gets too close, like a bird, a bigger spider, or your finger, it starts to shake.",
        "It whirls its body around and around in the web, so fast that it turns into a blur.",
        "For a predator, it becomes almost impossible to tell where the spider actually is.",
        "That is why you sometimes see one vibrating wildly when the vacuum gets close.",
        "It is not attacking you. It is trying to disappear.",
    ]},
    {"id": "myth", "frases": [
        "Now, about that rumor.",
        "Maybe you heard it on the playground.",
        "Daddy longlegs are the most venomous spiders in the world, but their fangs are too short to bite you.",
        "It is one of the most famous bug myths ever. And it is wrong, twice.",
        "First, there is no evidence that its venom is unusually strong, and it is not dangerous to people.",
        "Second, its fangs are not too short.",
        "In one famous television experiment, a host let a cellar spider bite him on purpose.",
        "The result? A tiny burning feeling that faded after a few seconds.",
        "So yes, it can bite. It almost never does. And it is less painful than a mosquito.",
        "And the harvestman, the other daddy longlegs, has no venom at all.",
    ]},
    {"id": "mother", "frases": [
        "Cellar spiders are also surprisingly devoted parents.",
        "Most spiders wrap their eggs in a silk sac and leave them behind.",
        "A cellar spider mother carries her eggs in her mouth.",
        "She holds the little bundle in her jaws for weeks, wrapped in just a few threads of silk.",
        "When the babies hatch, they stay close to her in the web for a while, before they leave to find corners of their own.",
    ]},
    {"id": "tough", "frases": [
        "And they are tough little survivors.",
        "A cellar spider can go for months without a single meal.",
        "If something grabs one of its legs, it can let that leg go and escape.",
        "That is why you sometimes find one getting around on six or seven legs. It is fine.",
        "And it can live for two or three years, quietly guarding the same corner.",
    ]},
    {"id": "travel", "frases": [
        "This spider is also one of the great world travelers.",
        "It probably came from the warm parts of Asia.",
        "But for centuries, it has hitched rides with people, hidden in boxes, ships, and luggage.",
        "Today it lives inside buildings on every continent except Antarctica.",
        "It is one of the most widespread spiders on Earth, and almost all of them live with us.",
        "Those old dusty cobwebs in the corners of old houses? Many of them were built by cellar spiders.",
    ]},
    {"id": "why", "frases": [
        "So why are there so many in your house?",
        "Because a cellar spider only stays where there is food.",
        "It eats mosquitoes, gnats, moths, flies, small beetles, and of course, other spiders.",
        "If your basement is full of cellar spiders, it means there are a lot of other bugs down there.",
        "And they are being eaten, every single night.",
        "So think of them as free pest control, and a warning light at the same time.",
    ]},
    {"id": "tell", "frases": [
        "But how do you know which spider you are looking at?",
        "Here is the quick test.",
        "A cellar spider is pale, almost see through, with a tiny body and legs that seem to go on forever.",
        "It hangs high up, in corners and along the ceiling.",
        "A black widow is the opposite. A shiny black, round body, shorter, thicker legs, and a red hourglass underneath.",
        "It hides low and out of sight, under shelves, in woodpiles, in old boxes, and around the garage door.",
        "Pale and high up, let it be. Shiny black and low, keep your hands away.",
    ]},
    {"id": "spray", "frases": [
        "That is also why bug spray can backfire.",
        "Spray does not choose. It kills the hunters along with the pests.",
        "And the pests usually bounce back much faster than the spiders that were eating them.",
    ]},
    {"id": "deal", "frases": [
        "So what should you do when you find one?",
        "The easiest answer is nothing. Let it work.",
        "If you don't want it over your bed, slide a cup over it, slip a piece of paper underneath, and move it to the basement or the garage.",
        "If there are too many, vacuum the old webs, seal the cracks around windows and doors, and dry out the damp rooms.",
        "Fewer bugs means fewer cellar spiders. They will move on by themselves.",
        "And if you ever find a black widow, do not touch it. Call a professional.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So the next time you see that pale spider hanging in the corner, look at it a little differently.",
        "It is not a sign of a dirty house.",
        "It is a night guard with eight long arms, watching over a corner you never look at.",
        "It eats the mosquitoes. It fights the widows. And it has never wanted anything from you.",
        "So put the broom down, and let it keep its job.",
    ]},
]
