# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «5 Bugs You Should NEVER Kill Around Your House (And 1 You Should)»  Motor SECUENCIA, ~9 min.
Hipótesis 2 de `canales/formula/wild_next_door.md`: el empaque «Never Kill» (ciempiés, 440 vistas en 2,5 días) con una sola
variable nueva, la estructura en LISTA (Curious Kids Discover ×70 con «5 Animals You Shouldn't Kill Around Your House»).
TODO IMAGEN: Flow sin puntos (0) el 11-oct-2026; las imágenes de Nano Banana 2 Lite siguen saliendo gratis.
Cuenta regresiva: 5 mantis, 4 araña lobo, 3 tijereta (el mito del oído, a mitad), 2 araña saltarina (la de la ventana
del gancho), 1 avispa alfarera azul (caza viudas negras) y «la que sí»: cucaracha alemana. Cierre circular a la cocina.
Hechos usados (con fuentes de extensión universitaria):
- Mantis: patas raptoras; gira la cabeza casi 180°; UN solo oído en el vientre que oye murciélagos y la hace picar en el
  aire; come lo que atrapa (también bichos útiles); sin veneno ni aguijón; ooteca espumosa con de decenas a cientos de
  ninfas (Kansas State, Nebraska-Lincoln, Kentucky, NC State).
- Araña lobo (Lycosidae): no teje red para cazar, caza a pie y de noche; 8 ojos en 3 filas (4 pequeños, 2 grandes, 2
  medianos) con tapetum que brilla con linterna; la hembra lleva el saco de huevos en las hileras y las crías en el lomo;
  la reclusa parda tiene 6 ojos en 3 pares; mordida leve, solo si se la aprieta (Australian Museum; extensiones).
- Tijereta europea (Forficula auricularia): el mito de que entra al oído y pone huevos es falso (rarísimo entrar por
  accidente); pinzas para aparearse, pelear y plegar alas; la madre cava, lame los huevos contra hongos, los guarda y
  alimenta a las ninfas (Boos et al. 2014; Clemson HGIC); come áfidos, ácaros y huevos, y a veces flores; en interiores
  se seca y muere.
- Araña saltarina (Salticidae): ~6 500 especies, ~1 de cada 8 arañas; 8 ojos, 2 enormes, la mejor vista entre arañas y
  ve color; hilo de seguridad (dragline) antes de saltar; salta hidráulicamente (presión de hemolinfa); algunas planean
  rutas y rodeos; Rößler et al. 2022 PNAS: crías de Evarcha arcuata con sueño tipo REM colgadas de un hilo (ojos y patas
  se mueven); come moscas, mosquitos, polillas y hormigas; mordida rara y leve.
- Avispa alfarera (mud dauber): solitaria, sin colonia ni nido que defender, pica casi nunca (si la aprietan); la hembra
  acarrea bolitas de barro y llena celdas con arañas paralizadas; un huevo por celda; la azul (Chalybion californicum)
  reusa nidos viejos y los llena de viudas negras (Missouri Dept. of Conservation; UC ANR). Nido gris de papel con
  muchas avispas = avispa social: alejarse.
- Cucaracha alemana (Blattella germanica): ~1,5 cm, dos rayas oscuras tras la cabeza; la hembra lleva la ooteca (30-48
  huevos); alérgenos de heces y mudas ligados al asma infantil; nocturna (verla de día = muchas más); cebo en gel mejor que
  aerosol, que las dispersa (Penn State Extension, Purdue E-241, UC IPM Pest Notes, Mississippi State).
"""

TITULO = "5 Bugs You Should NEVER Kill Around Your House (And 1 You Should)"
ARCHIVO = "five_bugs_never_kill"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Whisper escribe «Number 4», «6,000» y «2022» con cifras (la toma dice bien las palabras) y las colas de 5 frases largas
# terminan hablando hasta el final (CER 0: la transcripción termina bien)
CER_MAX_POR_FRASE = {"four_0": 0.25, "two_1": 0.1, "two_6": 0.12}
TAIL_MAX_POR_FRASE = {"four_2": 0.6, "four_6": 0.5, "four_7": 0.8, "three_9": 0.6, "two_5": 0.8}

SECUENCIA = dict(
    video_s=0,          # sin puntos de video en Flow (0 puntos el 11-oct-2026): todo imagen
    clip_s=8,
    img_s=5.0,
    rapido_hasta=300,
    img_s_lento=6.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-cinco_bichos",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "mantis": "a cartoon praying mantis with a slim bright green body, a triangular head with two big round friendly "
                  "eyes, long front legs folded like praying hands, and a tiny purple bow tie",
        "wolf": "a cartoon wolf spider with a chunky fuzzy brown body with a pale stripe down its back, eight sturdy "
                "hairy legs, two big round eyes in the middle of its face with six smaller dot eyes around them, and a "
                "tiny red bandana",
        "earwig": "a cartoon earwig with a shiny reddish-brown long thin body, two small curved pincers at its tail, two "
                  "short antennae, a friendly round face and tiny pink earmuffs",
        "jumper": "a cartoon jumping spider with a small fuzzy black body with white spots on its back, a square face "
                  "with two huge shiny round front eyes and six small ones, short stubby legs and a tiny blue cape",
        "dauber": "a cartoon mud dauber wasp with a slim glossy black body with pale yellow legs, a very thin thread-like "
                  "waist, two long thin antennae, a calm friendly face and a tiny orange construction hard hat",
        "roach": "a cartoon German cockroach with a shiny light brown oval body with two dark stripes behind its head, "
                 "long wiggly antennae, a sneaky grin and a tiny black burglar mask",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a clear drinking cup and a sheet of white paper used to carry a bug outside",
    epoca="present-day suburban house: kitchen, garage, porch, garden",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Playful, curious nature documentary score for a hand-drawn cartoon about small house bugs: pizzicato strings, "
           "marimba, soft bassoon, celesta, felt piano, light brushed percussion and upright bass. Mischievous and warm, "
           "with moments of comic suspense. Never epic, never horror.",
    escenas={
        "hook": ("Quiet morning kitchen: gentle marimba and a single pizzicato note, a curious pause, then a bright playful twist.", 3),
        "five": ("Calm and watchful: slow pizzicato and bassoon, a still patient feeling, a quick comic snap, then relaxed.", 4),
        "four": ("Sneaky night prowl: soft walking upright bass, muted marimba, a spooky-but-silly feeling that turns tender for the mother.", 5),
        "three": ("Mock-serious rumor: bassoon and low strings with a wink, then a warm tender felt piano for the devoted mother.", 4),
        "two": ("Light and quick: bouncy pizzicato and celesta with little hops, curious and charming, a dreamy bar at the end.", 5),
        "one": ("Building comic suspense: low pulsing strings and bassoon, tiptoeing pizzicato, a triumphant playful chord near the end.", 6),
        "should": ("A short worried turn: low muted strings and a hesitant bassoon, practical and a little stern, then relieved.", 3),
        "outro": ("Return to the opening morning theme, warm and resolved: celesta and felt piano, a smile, then a calm ending.", 3),
    },
    tramos=[
        (["hook", "five"],
         "Begin from near silence. End on a held suspenseful tone that can flow into the next piece. No loud ending."),
        (["four", "three"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["two", "one"],
         "Begin gently with a held tone. End on a sustained calm chord that can flow into the next piece."),
        (["should", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "You are in the kitchen, pouring your morning coffee. Something small moves on the window sill.",
        "You lean in closer. And it turns around, and looks straight at you.",
        "Two enormous shiny eyes. Eight little legs. And your hand is already reaching for a paper towel.",
        "Wait.",
        "Because most of the small, creepy things in your house are not invaders. They are roommates, and they work for free.",
        "Today, there are five bugs you should never kill. And one that you really should.",
        "One of them has a rumor about crawling into your ear. We will deal with that one in the middle.",
        "And number one hunts black widows. Yes, really.",
    ]},
    {"id": "five", "frases": [
        "Number five. The praying mantis.",
        "You have probably seen one clinging to a window screen, or sitting under the porch light, like a tiny green alien.",
        "It holds its front legs folded in front of its face, as if it is praying. It is not praying. It is waiting.",
        "Those legs are spiked traps. When a fly wanders close, they snap out and grab it in a fraction of a second. Faster than you can blink.",
        "And it hears with just one ear, in the middle of its body. It is tuned to listen for bats. If it hears one, it dives out of the sky.",
        "It eats flies, moths, mosquitoes, and crickets. It is not picky, so it sometimes grabs a helpful bug too. But it keeps the numbers down.",
        "And it cannot hurt you. No venom, no stinger.",
        "And a winter tip. If you find a tan, foamy looking lump on a twig or a fence, do not scrape it off.",
        "That is a mantis egg case, with up to hundreds of babies inside, waiting for spring.",
    ]},
    {"id": "four", "frases": [
        "Number four. The wolf spider.",
        "This one looks like a monster from a movie. Big, hairy, brown, and it sprints across the garage floor like it owns the place.",
        "A wolf spider does not build a web. It hunts on foot, at night, using its eyes. It has eight of them, and two are big and sharp.",
        "Here is a fun trick. Shine a flashlight over the lawn at night, and tiny sparkles shine back. Those are wolf spider eyes.",
        "It chases crickets, ants, and cockroaches, so it works for you in the garage.",
        "And the mother is amazing. When her babies hatch, they climb onto her back, sometimes more than a hundred of them, and she carries them around for a week or two.",
        "Some people mix it up with the brown recluse, which really can be dangerous. So count the eyes. A wolf spider has eight, in three rows. A brown recluse has only six, in three pairs.",
        "It bites only if you pinch it, and it feels like a bee sting at worst. In the fall it wanders into garages, looking for somewhere warm. Use a cup and a piece of paper, and put it back outside.",
    ]},
    {"id": "three", "frases": [
        "Number three. The earwig.",
        "Yes, the one with the scary pincers. And the famous rumor.",
        "So let me answer it. Does an earwig crawl into your ear at night, and lay eggs in your brain? No.",
        "That is a very old myth, and it has stuck around for centuries.",
        "Can one ever wander into an ear? Very rarely, by accident, like any small bug that got lost in the dark. But it does not burrow, and it does not lay eggs in your head.",
        "Now for the part nobody expects. Earwig mothers are some of the best parents in the insect world.",
        "She digs a burrow, lays her eggs, and guards them for weeks. She even licks them clean, one by one, to keep mold away.",
        "When the babies hatch, she stays with them and brings them food until they are ready to leave.",
        "Earwigs eat aphids, mites, and the eggs of other bugs. In the garden, they sometimes nibble on flowers too, so outside it depends.",
        "But inside your house, an earwig is just a lost visitor. Indoors is too dry for it, so it will not last long anyway. Sweep it into a dustpan, and put it outside.",
    ]},
    {"id": "two", "frases": [
        "Number two. And yes, this is your friend from the window sill. The jumping spider.",
        "It is the biggest family of spiders in the world. More than six thousand kinds, about one out of every eight spiders on the planet.",
        "It does not build a web to catch dinner. It stalks, like a tiny cat, and pounces.",
        "And its secret is its eyes. It has eight, and two of them are huge. They give it the sharpest vision of any spider, and it can see in color.",
        "So when it turns and stares at you, it is actually looking at you.",
        "Before every big jump, it glues a thread of silk behind it, like a safety rope. If it misses, it just dangles, and climbs back up.",
        "In twenty twenty two, scientists filmed baby jumping spiders sleeping, hanging from a single thread. Their eyes moved, and their legs twitched, like dream sleep.",
        "Nobody can say they dream. But it sure looks like it.",
        "It eats flies, mosquitoes, moths, and ants. And its bite on people is rare, and mild.",
        "So the next time a tiny spider looks you in the eye, maybe give it a second chance.",
    ]},
    {"id": "one", "frases": [
        "And now, number one. The one that looks the most dangerous. The mud dauber.",
        "It is a long, skinny wasp, with a waist so thin it looks like a thread. You see it around porches, garages, and under the edge of the roof.",
        "And you have probably seen its nest. Those lumpy tubes of dried mud, stuck to the wall, that look like a little set of organ pipes.",
        "Wasp. Nest. Your hand goes for the spray. Hold on.",
        "A mud dauber is a solitary wasp. No queen, no colony, no giant nest to guard.",
        "That is why it almost never stings people. You would have to squeeze it, or step on it, to make it try.",
        "So what is it doing? Building a pantry.",
        "The mother carries mud in her jaws, one little ball at a time, and shapes the tubes. Then she goes hunting. For spiders.",
        "She stings each spider, which paralyzes it, and packs the little rooms full. Then she lays one egg on a spider, and seals the room with mud.",
        "Now here is the best part. One kind, the blue mud dauber, goes after black widows.",
        "It does not even build its own nest. It moves into an old one, throws out the old food, and fills it with black widows.",
        "So that ugly mud nest under your porch roof might be a black widow storage room.",
        "But if you find a gray, paper looking nest, shaped like an umbrella, with lots of wasps crawling on it, that is a different story. Stay away, and call a professional.",
    ]},
    {"id": "should", "frases": [
        "Now, the one you should kill. The German cockroach.",
        "Everything on this list has something in common. It does not want your house. It is passing through, or hunting something, or lost.",
        "The German cockroach is the opposite. It moves in. And it never leaves.",
        "It is small, light brown, with two dark stripes right behind its head. It lives in kitchens and bathrooms, near water and food.",
        "One female carries an egg case with thirty or more eggs, and one mother can turn into hundreds of roaches in a few months.",
        "And it is not just gross. Cockroach droppings and shed skin carry allergens. Studies have linked them to asthma, especially in kids.",
        "Here is the clue. Cockroaches hide by day and come out at night. So if you see one in daylight, there are usually many more hiding.",
        "So what do you do? Skip the spray can. Sprays often just scatter them into other rooms.",
        "Use gel bait, in the corners and cracks. Clean up crumbs and grease, fix leaks, and seal the gaps. And if the problem keeps growing, call a professional.",
        "That one, you have my permission.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "So let's go back to the kitchen. The coffee is getting cold. And the little spider on the window sill is still there, looking at you.",
        "It is not a threat. It is a tiny roommate that eats the mosquitoes, and asks for nothing.",
        "So the next time something small and creepy shows up, ask yourself one question first.",
        "Is it moving in, or just passing through?",
        "If it is passing through, grab a cup and a piece of paper, and walk it outside.",
        "And if you want to meet the spider that hunts black widows from the corner of your ceiling, that video is also on this channel.",
        "Put the paper towel down. Let it live.",
    ]},
]
