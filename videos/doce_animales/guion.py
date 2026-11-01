# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «12 Animals You Should NEVER Kill Around Your House (And 2 You Should)»  Motor SECUENCIA, ~14 min.
Fórmula «Never Kill» en lista (como `cinco_bichos`) ampliada de bichos a ANIMALES del patio. Referencia: Curious Kids Discover
«5 Animals You Shouldn't Kill Around Your House» (×70, 11 min, 210 k vistas); mismo canal ×47 y ×18 con el formato.
Clips (50 puntos dichos por el usuario, 18-oct-2026): 4 x 10 s al inicio (motor, 28 pts) + 3 clips de clímax (10+10+6 s,
19 pts) puestos como FX `video` a cuadro entero en efectos.py: n.º 1 (zarigüeya hace el muerto), «los 2 que sí» y el cierre.
Foto REAL de cada animal como pegatina al presentarlo (regla del usuario, 18-oct; `pegatinas/`, Wikimedia Commons).

Ficha de hechos (fuentes de extensión/agencias; verificar DOI con Crossref antes de la descripción):
- Zarigüeya de Virginia: único marsupial de EE. UU./Canadá; 50 dientes; «playing possum» = tanatosis; rabia muy rara, se cree
  que por su temperatura corporal baja (~94-97 °F; Mass.gov, Iowa DNR). Mito de 5 000 garrapatas: Keesing et al. 2009 (Cary
  Institute, 5 zarigüeyas en laboratorio, extrapolado); Ticks and Tick-borne Diseases 2021 (Eureka College): 0 garrapatas en
  el estómago de 32 zarigüeyas silvestres de Illinois (Illinois Extension, 2024: hace falta más investigación).
- Lagartija de cerca occidental (Sceloporus occidentalis): Lane & Quistad 1998 (UC Berkeley): una proteína de su sangre mata a
  Borrelia en el intestino de la ninfa de garrapata; posible razón de menos Lyme en California.
- Libélula: atrapa hasta ~95 % de las presas que persigue (Rachel Crane, UC Davis, SICB 2023); intercepta prediciendo; ninfas
  acuáticas comen larvas de mosquito. Mito «devil's darning needle».
- Murciélagos: Boyles et al. 2011, Science 332 (3,7 a 53 mil millones de USD/año en control de plagas); CDC: los murciélagos son
  la principal fuente de rabia humana en EE. UU.; no tocarlos; despertar con un murciélago en el cuarto = llamar al médico.
- Mosca sírfida: imita avispas, no pica, 2 alas (avispa 4), larvas comen áfidos (NC State biocontrol).
- Abejorro: polinización por vibración (tomate; Cornell CCE, UMD Extension, Clemson); machos sin aguijón.
- Sapo americano: verrugas = mito (VPH humano; Maryland DNR); glándulas parótidas con bufotoxina (Missouri Conservationist);
  bebe por la piel del vientre.
- Araña amarilla de jardín (Argiope aurantia): se come la tela y la rehace cada noche (Univ. of Arkansas, OSU BYGL); zigzag =
  estabilimento, función debatida; no peligrosa.
- Milpiés: detritívoro; Eumillipes persephone (Australia, 2021) con 1 306 patas; muere seco dentro de casa.
- Escarabajo de suelo (Carabidae): caza nocturna de babosas, orugas, gusanos cortadores; escarabajo bombardero.
- Mariquita: áfidos; sangrado reflejo por las patas; larvas «caimán».
- Culebra rayada: inofensiva, almizcle, crías vivas, hibernáculos compartidos.
- Linterna moteada: invasora, Pensilvania 2014; PA Dept. of Agriculture «Kill it! Squash it, smash it…»; masas de huevos
  (Penn State Extension: raspar a alcohol).
- Garrapata de patas negras: CDC — pinzas finas, tirar recto; nada de calor/esmalte; alcohol o inodoro; fiebre/sarpullido = médico.
"""

TITULO = "12 Animals You Should NEVER Kill Around Your House (And 2 You Should)"
ARCHIVO = "twelve_animals"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falsos positivos de Whisper (18-oct): escribe cifras con dígitos («Number 12», «2021», «95%», «1990s», «5,000») y oye
# «to» por «two» y «sack» por «sac»; la mejor toma de cada una dice bien las palabras (comparado hyp vs. texto).
CER_MAX_POR_FRASE = {"hook_8": 0.16, "hook_9": 0.03, "hook_10": 0.16, "n12_0": 0.24, "n11_0": 0.22, "n11_5": 0.31,
                     "n10_0": 0.08, "n9_0": 0.06, "n8_7": 0.02, "n7_5": 0.14, "n4_0": 0.18, "n2_0": 0.09,
                     "n2_4": 0.24, "n1_4": 0.11, "n1_12": 0.12, "n1_15": 0.26, "n1_17": 0.11}

SECUENCIA = dict(
    clips_s=[10] * 4,         # 4 x 10 s al inicio (28 puntos). Los 3 de clímax (10+10+6 s) van como FX `video` en efectos.py
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=4.5,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={"scene-004": 0.0},   # Flow metió una voz («Whoa…», Whisper 19-oct); clip_linterna trae una risa: silenciar en efectos.py
    recorte_por={"scene-001": 0.03},   # marco blanco fino + línea negra (~12 px); clip_desmayo también lo trae: recortar 0.03 en efectos.py
    carpeta_descargas="flow-doce_animales",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "possum": "a cartoon Virginia opossum with a pale white pointy face, a pink nose, beady black eyes, small round "
                  "black ears, scruffy gray fur, a long bare pink tail, and a tiny green knitted scarf",
        "lizard": "a cartoon western fence lizard with spiky gray-brown scales, a bright blue patch on each side of its "
                  "belly, a long tail, and tiny round sunglasses pushed up on its head",
        "bat": "a cartoon little brown bat with soft brown fur, big rounded ears, thin dark leathery wings, a tiny pink "
               "nose, and a small red bandana around its neck",
        "snake": "a cartoon garter snake, long and thin, dark olive green with three pale yellow stripes running down its "
                 "body, a friendly round face, and a small blue bow tie",
        "toad": "a cartoon American toad, plump and brown with bumpy skin, two big oval bumps behind its golden eyes, "
                "and a tiny yellow rain hat",
        "bumble": "a cartoon fuzzy bumblebee, round and chubby with black and yellow fur, small clear wings, and tiny "
                  "orange goggles on its forehead",
        "dragon": "a cartoon dragonfly with a long slim bright blue body, four long clear wings, huge round green eyes "
                  "that cover most of its head, and a tiny aviator scarf",
        "garden": "a cartoon yellow garden spider with a big egg-shaped black and bright yellow body, eight long black "
                  "and orange-banded legs, and a tiny straw sun hat",
        "beetle": "a cartoon ground beetle with a shiny jet-black body, long fast legs, long antennae, strong small "
                  "jaws, and a tiny red headlamp",
        "hover": "a cartoon hover fly, a small slim fly with yellow and black stripes like a wasp, ONE pair of clear "
                 "wings, huge red-brown eyes that cover most of its head, very short antennae, and a tiny fake "
                 "black mustache",
        "milli": "a cartoon millipede with a long round shiny dark brown body made of many segments, many tiny pale "
                 "legs, short antennae, and a tiny gray knitted beanie",
        "lady": "a cartoon ladybug with a shiny round red shell with black spots, a black head with two small white "
                "patches, six short black legs, and a tiny silver knight helmet",
        "lantern": "a cartoon spotted lanternfly with gray-beige wings covered in black spots, bright red hind wings "
                   "with black spots peeking out, and sneaky narrow eyes",
        "tick": "a cartoon blacklegged deer tick, a tiny flat oval body, reddish-orange with a dark black shield near "
                "its head, eight short black legs, and sneaky narrow eyes",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a suburban backyard at night with a porch light, metal trash cans, a vegetable garden with tomato plants, "
           "a wooden fence, and a flower bed",
    epoca="present-day North American suburban house and backyard",
    cierre="No text, no letters, no words, no logos, no watermark. Absolutely no numbers, digits or numerals anywhere "
           "in the picture. No speech bubbles. Every box, can, jar and tool is plain and unlabeled.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
# Tramos de <= 170 s: recalcular con los tiempos reales tras `tiempo` (estimados a ~2,7 palabras/s).
LYRIA = dict(
    estilo="Playful, curious nature documentary score for a hand-drawn cartoon about the animals living around a house: "
           "pizzicato strings, marimba, soft bassoon, celesta, felt piano, light brushed percussion and upright bass. "
           "Mischievous and warm, with moments of comic suspense. Never epic, never horror.",
    escenas={
        "hook": ("Late-night quiet by the trash cans: a single low bassoon note, sparse ticking pizzicato, a sudden comic hiss-like sting, then a bright, curious twist.", 4),
        "n12": ("Light and cheerful: a bouncy marimba and pizzicato theme, like a tiny armored hero.", 4),
        "n11": ("Slow and earthy: low plucked bass and soft woodblocks, a calm rolling feeling, a little humorous.", 4),
        "n10": ("Buzzing and tricky: fast tremolo strings that suddenly freeze in place, a playful bluff revealed.", 4),
        "n9": ("Night patrol: tiptoeing staccato bassoon and muted marimba, quick little runs.", 4),
        "n8": ("Delicate and a bit suspenseful: celesta weaving patterns over soft pizzicato, a big reveal that turns gentle.", 4),
        "n7": ("Fast and precise: swooping flute and marimba runs, darting and confident.", 4),
        "n6": ("Warm and fuzzy: humming low strings and felt piano, a cozy buzzing groove.", 4),
        "n5": ("Rainy night: soft plinking marimba like raindrops, a questioning bassoon, then a light debunking groove.", 5),
        "n4": ("Slithering comic suspense: low sliding bass and clarinet-like bassoon, turning friendly.", 4),
        "n3": ("Dusk flight: fluttering high strings and celesta, quick swoops, then one serious, careful low phrase.", 5),
        "n2": ("Sunny and proud: a strutting pizzicato and marimba groove, then a small scientific wonder moment.", 4),
        "n1": ("The big finale of the countdown: the opening night theme returns, a comic fainting pause, a mystery investigated, then warm triumph.", 7),
        "should": ("A sudden mood shift: a tense but playful march, muted brass-like low strings and snappy percussion, determined.", 4),
        "tick": ("Careful and precise: quiet ticking pizzicato and a steady, focused rhythm, like a calm instruction.", 4),
        "deal": ("Practical and friendly: light pizzicato and felt piano, calm and helpful.", 3),
        "outro": ("Return to the opening night theme, now warm and resolved: celesta and felt piano, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "n12"], "Begin from near silence. End on a held tone that can flow into the next piece. No loud ending."),
        (["n11", "n10"], "Begin softly with a held tone. End on a sustained chord that can flow into the next piece."),
        (["n9", "n8"], "Begin softly with a held tone. End on a sustained chord that can flow into the next piece."),
        (["n7", "n6"], "Begin gently with a held tone. End on a sustained chord that can flow into the next piece."),
        (["n5", "n4"], "Begin gently with a held tone. End on a sustained chord that can flow into the next piece."),
        (["n3", "n2"], "Begin gently with a held tone. End on a sustained chord that can flow into the next piece."),
        (["n1"], "Begin gently with a held tone. End on a sustained warm chord that can flow into the next piece."),
        (["should", "tick", "deal", "outro"], "Begin with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is eleven at night. You carry the trash out to the curb.",
        "And something in the dark hisses at you.",
        "A pale, pointy face. Beady black eyes. A mouth full of tiny, sharp teeth.",
        "It is a possum. And your first thought is to grab the shovel.",
        "Don't.",
        "That strange little animal is one of the best neighbors you will ever have.",
        "Around your house, right now, there are animals that look creepy, slimy, or dangerous.",
        "And they are quietly working for you, for free.",
        "Today we are counting down twelve of them. Twelve animals you should never kill.",
        "And at the very end, two that, honestly, you should.",
        "Plus one famous number you have probably seen online. Five thousand ticks a summer.",
        "Stay with me, because that number might be completely wrong.",
    ]},
    {"id": "n12", "frases": [
        "Number twelve. The ladybug.",
        "Nobody wants to kill a ladybug. But a lot of people spray them by accident, along with the aphids on their roses.",
        "And that is a mistake, because a ladybug is a tiny tank built to eat aphids.",
        "One ladybug can eat dozens of them in a single day, and thousands in its life.",
        "Its babies are even hungrier. They look like tiny, spiky alligators, so people squish them, thinking they are pests.",
        "And if you pick one up and it leaves a yellow drop on your finger, that is not pee.",
        "It is bitter blood that it squeezes out of its own knees, so that birds spit it out.",
        "Gross. And brilliant.",
    ]},
    {"id": "n11", "frases": [
        "Number eleven. The millipede.",
        "In the fall, you might find dozens of them curled up in the garage or the basement, and it feels like an invasion.",
        "But a millipede has no venom, no stinger, and its tiny jaws are too weak to hurt you.",
        "It does not even hunt. It eats dead leaves and rotting wood.",
        "And no, most of them do not have a thousand legs. Most have far fewer.",
        "But in twenty twenty one, scientists in Australia found one with more than thirteen hundred legs.",
        "Inside your house, it dries out and dies on its own. Just sweep it into a dustpan and put it outside.",
    ]},
    {"id": "n10", "frases": [
        "Number ten. The one that looks like a wasp, but is not.",
        "You are eating lunch on the porch, and a little striped insect hovers right in front of your face.",
        "Your hand goes for the fly swatter. But look closer. It is a hover fly.",
        "It is dressed up as a wasp, but it is a fly. It has no stinger at all. The costume is a bluff to scare off birds.",
        "Here is how to tell. A wasp has two pairs of wings and long antennae.",
        "A hover fly has just one pair of wings, tiny antennae, and huge eyes that cover most of its head.",
        "Adult hover flies pollinate flowers. Their babies are small green maggots that crawl over leaves, eating aphids one after another.",
    ]},
    {"id": "n9", "frases": [
        "Number nine. The black beetle that runs across the patio at night.",
        "This is a ground beetle, and it is one of the best friends a gardener can have.",
        "Ground beetles hunt at night on the soil, eating slugs, snails, caterpillars, and the eggs of other pests.",
        "A lot of the cutworms that would chop your seedlings down in the dark never make it, because a ground beetle found them first.",
        "And one kind, the bombardier beetle, fires a boiling hot spray out of its rear end, with a tiny pop.",
        "If one gets inside, pick it up with a cup, and let it go by the garden.",
    ]},
    {"id": "n8", "frases": [
        "Number eight. The big yellow spider in your garden.",
        "Late in summer, it shows up between the tomato plants. A huge black and yellow spider, sitting head down in a giant web.",
        "It looks terrifying. It is a yellow garden spider, and it is not dangerous to people.",
        "It only bites if you grab it, and the bite is milder than a bee sting.",
        "Now look at the middle of the web. There is a thick white zigzag going up and down.",
        "Nobody knows for sure why. Maybe to warn birds not to fly through it.",
        "And every night, the spider eats most of its own web, and builds a fresh one, often in the same spot.",
        "In the fall, she makes a round brown egg sac, like a little paper ball, and hangs it near the web.",
    ]},
    {"id": "n7", "frases": [
        "Number seven. The dragonfly.",
        "A long time ago, people called it the devil's darning needle. Some said it could sew your mouth shut while you slept.",
        "It cannot. It has no stinger, and it almost never bites people.",
        "But for a mosquito, the dragonfly really is a monster.",
        "It does not just chase its prey. It predicts where the bug is going to be, and flies to that spot to meet it.",
        "Scientists who study dragonflies say they catch up to ninety five percent of the prey they go after.",
        "A lion is lucky to win one chase out of four.",
        "And before it can even fly, a young dragonfly lives underwater in a pond, for months or even years, eating mosquito larvae.",
    ]},
    {"id": "n6", "frases": [
        "Number six. The bumblebee.",
        "It is big, it is loud, and when it bumps into your window, it sounds furious.",
        "But bumblebees are some of the gentlest bees there are. They only sting if you grab them, or attack their nest.",
        "And the males cannot sting at all. They do not even have a stinger.",
        "Here is their superpower. Tomato flowers keep their pollen locked inside, like salt in a salt shaker.",
        "A bumblebee grabs the flower and vibrates its flight muscles so fast that the pollen shakes right out.",
        "It is called buzz pollination. And honeybees cannot do it.",
        "If you grow tomatoes, peppers, or blueberries, there is a good chance a bumblebee helped make them.",
    ]},
    {"id": "n5", "frases": [
        "Number five. The toad.",
        "You step outside on a rainy night, and there it is on the sidewalk. Bumpy, brown, and staring at you.",
        "And you probably heard this one as a kid. Touch a toad, and you get warts.",
        "So let's settle it right now. You do not.",
        "Warts on people come from a human virus. Toads do not carry it.",
        "Those bumps on its skin are not warts at all. They are tiny glands.",
        "And the two big bumps behind its eyes are its real defense. They make a bitter poison that burns the mouth of anything that bites it.",
        "So a toad cannot hurt you. But it can hurt your dog.",
        "If your dog grabs a toad and starts drooling or pawing at its mouth, rinse its mouth with water and call the vet.",
        "So why keep it? Because a toad eats almost anything small that moves.",
        "Beetles, slugs, cutworms, ants, and spiders. A single toad can eat thousands of insects in one summer.",
    ]},
    {"id": "n4", "frases": [
        "Number four. The snake in the garden.",
        "A long, thin snake with stripes down its back slides out from under the bushes.",
        "But this is most likely a garter snake, one of the most common snakes in North America. And it is harmless to people.",
        "It eats slugs, earthworms, insects, frogs, and even small mice.",
        "If you grab it, it might bite. And it will do something worse. It will cover your hands with a terrible smelling musk.",
        "That is its whole plan. Smell so bad that you let go.",
        "Of course, not every snake is harmless. If you are not sure which one you are looking at, do not touch it. Just give it space.",
        "It wants to get away from you even more than you want it gone.",
    ]},
    {"id": "n3", "frases": [
        "Number three. The bat.",
        "At dusk, something flutters over the yard, too fast to see clearly. Swooping, turning, diving.",
        "It is not attacking you. It is eating.",
        "Most bats in the United States eat only insects. Moths, beetles, and mosquitoes, caught in the air, in total darkness.",
        "They find them by shouting, and listening for the echo.",
        "A single little brown bat can catch hundreds of small insects in one hour.",
        "Scientists have estimated that bats save American farmers billions of dollars every year, just by eating crop pests.",
        "But here is the one rule that really matters. Never touch a bat with your bare hands.",
        "Most bats are healthy, but in the United States, bats are the main source of rabies in people. And you cannot tell by looking.",
        "If a bat gets inside, close the room, open a window, and let it fly out on its own.",
        "And if you wake up with a bat in your bedroom, call your doctor.",
        "Outside, just let them hunt. A bat over your yard is pest control with wings.",
    ]},
    {"id": "n2", "frases": [
        "Number two. The little lizard on your fence.",
        "In the western United States, it does push ups on top of the fence post, flashing a bright blue belly.",
        "It is the western fence lizard. Most people just call it the blue belly.",
        "Those push ups are a message to other males. This fence is taken.",
        "But it has a secret that scientists discovered in the nineteen nineties.",
        "Young ticks love to feed on these lizards.",
        "And when a tick carrying the germ that causes Lyme disease drinks the lizard's blood, something in that blood kills the germ.",
        "The tick walks away clean.",
        "Researchers think this may be one reason why Lyme disease is so much less common in California than in the Northeast.",
        "So if you see a blue belly doing push ups on your fence, let it keep its post.",
    ]},
    {"id": "n1", "frases": [
        "And now, number one. The animal from the beginning. The possum.",
        "To be exact, the Virginia opossum. The only marsupial in the United States and Canada.",
        "Like a kangaroo, the mother carries her babies in a pouch.",
        "When they get too big for the pouch, they ride on her back. Sometimes more than ten of them at once.",
        "It has fifty teeth, more than any other land mammal in North America. That is why the hissing looks so scary.",
        "But the hissing is mostly a bluff. And if the bluff does not work, it does something even stranger. It faints.",
        "It falls over, its tongue hangs out, and it gives off a smell like rotting meat.",
        "That is where the phrase playing possum comes from. And it is not really acting. The fear switches it off.",
        "A possum eats almost anything. Snails, slugs, beetles, mice, rotten fruit under your trees, even roadkill.",
        "And it is very rarely found with rabies. One idea is that its body runs cooler than most mammals.",
        "Which brings us back to that famous number.",
        "Possums eat five thousand ticks every summer. You have probably seen it on a meme.",
        "It came from a real study in twenty oh nine. Scientists put ticks on a few possums in a lab, and most of the ticks disappeared.",
        "They figured the possums had groomed them off and eaten them. Then they multiplied that out to a whole season.",
        "And the number exploded online.",
        "But in twenty twenty one, another team looked inside the stomachs of thirty two wild possums.",
        "They did not find a single tick.",
        "So, does a possum eat ticks? Maybe a few. The honest answer is, we do not know yet. But five thousand is probably way too high.",
        "Either way, the possum is the night cleanup crew of your neighborhood. Leave it alone, and it will move on in a few days.",
    ]},
    {"id": "should", "frases": [
        "Now, I promised you two animals that you should not let go.",
        "The first one. The spotted lanternfly.",
        "It looks almost pretty. Gray wings with black spots, and when it jumps, a flash of bright red underneath.",
        "But it does not belong here. It came from Asia, and it was first found in Pennsylvania in twenty fourteen.",
        "It sucks the sap of grapevines and trees, and leaves behind a sticky mess that grows black mold.",
        "That is why officials in Pennsylvania gave a very unusual order. Kill it. Squash it, smash it, just get rid of it.",
        "In the fall, look for its eggs, too. They look like a smear of gray mud on trees, fences, and even cars.",
        "Scrape them into a bag with rubbing alcohol. And check your car before you drive somewhere new, because they love to hitch a ride.",
    ]},
    {"id": "tick", "frases": [
        "The second one. The tick.",
        "Specifically, the blacklegged tick, also called the deer tick.",
        "The young ones are about the size of a poppy seed. And they can carry the germ that causes Lyme disease.",
        "If you find one stuck on your skin, do not burn it, do not smother it with nail polish, and do not twist it.",
        "Take fine tweezers, grab it as close to the skin as you can, and pull straight up, slowly and steadily.",
        "Then drop it in rubbing alcohol, or flush it down the toilet. Never crush it with your fingers.",
        "Wash the bite. And if you get a rash or a fever in the next few weeks, tell your doctor.",
        "And notice something. The blue belly lizard, and maybe the possum, are fighting the tick for you.",
    ]},
    {"id": "deal", "frases": [
        "So how do you keep the helpers around?",
        "Go easy on the bug spray. It kills the hunters along with the pests, and the pests usually come back first.",
        "Leave a pile of leaves or a few flat rocks in one corner of the yard. Toads, beetles, and millipedes will move in.",
        "And when one of the small ones ends up inside, use the cup trick. Slide a cup over it, slip a paper underneath, and carry it outside.",
        "Bats and snakes are the exception. Those, you leave to a professional.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So, back to that night by the trash cans.",
        "The hiss. The teeth. The beady little eyes.",
        "Now you know what is really standing there. A tired mother with a pouch full of babies, eating the snails off your sidewalk.",
        "So put the shovel down. Go back inside. And let the night shift do its job.",
        "If you want to meet more of the strange neighbors living around your house, subscribe. I will see you next time.",
    ]},
]
