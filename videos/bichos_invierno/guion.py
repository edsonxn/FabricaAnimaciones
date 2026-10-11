# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «Where Do All the Bugs Go in Winter?»  Motor SECUENCIA, ~9 min.
Los primeros ~70 s en VIDEO (7 clips de 10 s en 360p, 7 puntos cada uno; el usuario tenía 55 puntos el 7-oct-2026),
dos escenas por clip con transición dibujada; el resto imagen por beat.
Hechos usados (extensiones universitarias, Xerces Society, Monarch Joint Venture, USDA Forest Service):
monarca del este: hasta 3000 millas a los bosques de oyamel del centro de México, la generación migratoria vive ~8 meses;
libélula «green darner» también migra; abejas melíferas: racimo de invierno, tiemblan con los músculos de vuelo, centro
a ~90 °F, rotan, expulsan a los zánganos en otoño; mariquitas: se agrupan por miles; chinche apestosa marmoleada entra a
las casas y no come ni se reproduce; oruga «woolly bear»: se congela, glicerol, corazón detenido, revive en primavera;
mariposa «mourning cloak»: inverna adulta en grietas de árboles, primera en volar; mosquitos: hembras fecundadas invernan
en sótanos, troncos y alcantarillas, otros dejan huevos que aguantan el hielo; hormigas: bajo la línea de helada, entrada
sellada; luciérnagas: larvas bajo tierra uno o dos años; ninfas de libélula cazan bajo el hielo; grillos, saltamontes y
mantis: mueren los adultos, quedan los huevos (ooteca de espuma con hasta ~200); colémbolos («snow fleas») caminan sobre
la nieve; cierre: «leave the leaves», tallos huecos, no limpiar el jardín hasta primavera.
"""

TITULO = "Where Do All the Bugs Go in Winter?"
ARCHIVO = "bugs_winter"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falsos positivos de Whisper: escribe cifras («3,000», «17», «200») y «morning» por «mourning»
CER_MAX_POR_FRASE = {"monarch_3": 0.2, "cloak_1": 0.05, "cicada_3": 0.2, "eggs_4": 0.2}

SECUENCIA = dict(
    video_s=70,         # 7 clips de 10 s = 49 puntos de los 55 disponibles
    clip_s=10,
    combinar=True,      # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    recorte_por={"scene-004": 0.035},   # la primera escena del clip trae un marco fino
    carpeta_descargas="flow-bichos_invierno",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
        "bug": "small cartoon insects with big round expressive eyes",
    },
    objeto="a suburban backyard with a wooden fence, one big oak tree, a small pond and a flower bed",
    epoca="present-day suburban backyard through the seasons",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 30
MUSICA = {
    "hook": dict(sabor="tension"), "plans": dict(sabor="espacio"), "monarch": dict(sabor="esperanza"),
    "bees": dict(sabor="espacio"), "ladybugs": dict(sabor="esperanza"), "stink": dict(sabor="tension"),
    "woolly": dict(sabor="vacio"), "cloak": dict(sabor="esperanza"), "mosquito": dict(sabor="tension"),
    "ants": dict(sabor="espacio"), "queen": dict(sabor="vacio"), "chrysalis": dict(sabor="espacio"), "cicada": dict(sabor="tension"), "firefly": dict(sabor="vacio"), "pond": dict(sabor="espacio"),
    "eggs": dict(sabor="vacio"), "snow": dict(sabor="esperanza"), "leaves": dict(sabor="espacio"),
    "outro": dict(sabor="esperanza"),
}

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "In summer, your backyard is loud.",
        "Bees in the flowers. Crickets in the grass. Mosquitoes on your arm.",
        "Millions of tiny animals, all buzzing, crawling, and flying at the same time.",
        "Then the first hard frost arrives.",
        "And in a single night, all of it goes silent.",
        "No buzzing. No chirping. Nothing.",
        "It looks like every bug on Earth just died.",
        "But a few months later, on the first warm day of spring, they are all back.",
        "So where did they go?",
        "The answer is stranger than you think.",
        "Some of them fly across a continent.",
        "Some turn into ice.",
        "And some are hiding closer to you than you would like.",
    ]},
    {"id": "plans", "frases": [
        "An insect cannot make its own body heat.",
        "When the air gets cold, the insect gets cold, and a frozen insect is usually a dead insect.",
        "So every species needs a plan.",
        "And over millions of years, they have come up with some truly wild ones.",
        "Run away. Huddle together. Dig down. Hide in a house. Or just freeze, and hope for the best.",
        "Let's go through them, one by one.",
    ]},
    {"id": "monarch", "frases": [
        "Plan number one: leave.",
        "Every fall, monarch butterflies from the United States and Canada start flying south.",
        "They weigh less than a paper clip.",
        "And they travel as far as three thousand miles, to a few mountain forests in central Mexico.",
        "There, millions of them cover the trees like orange leaves.",
        "The strangest part is that none of them has ever made the trip before.",
        "A summer monarch lives for a few weeks.",
        "But the generation born at the end of summer lives for eight months, just to make this journey.",
        "And they are not the only travelers.",
        "Some dragonflies migrate too, flying south in huge swarms that can show up on weather radar.",
    ]},
    {"id": "bees", "frases": [
        "Honey bees chose the opposite plan. They stay, and they make their own heat.",
        "When it gets cold, the whole colony packs into a tight ball around the queen.",
        "Then the bees shiver, flexing their flight muscles without moving their wings.",
        "That shivering keeps the center of the ball as warm as a summer day, even when it is snowing outside.",
        "The bees take turns, slowly rotating from the cold outside edge to the warm middle.",
        "And all that honey they made in summer? That is the fuel for the heater.",
    ]},
    {"id": "queen", "frases": [
        "Bumble bees do it very differently.",
        "When the cold comes, the entire colony dies. The workers, the males, and the old queen.",
        "Only the young queens survive.",
        "Each one digs a small hole in the ground, just a few inches deep, and sleeps there alone for six months.",
        "In spring, she wakes up and starts a whole new colony by herself.",
        "So if you see a huge bumble bee flying low over the grass in early spring, that is a queen looking for a home.",
    ]},
    {"id": "ladybugs", "frases": [
        "Ladybugs prefer a sleepover.",
        "In fall, they gather by the thousands, under bark, under rocks, and inside cracks in old logs.",
        "Packed together, they stay a little warmer and lose less water.",
        "Then they simply shut down and wait, living off the fat they stored in summer.",
    ]},
    {"id": "stink", "frases": [
        "And some bugs have discovered an even better shelter. Yours.",
        "Stink bugs, cluster flies, and some lady beetles squeeze in through tiny gaps around windows and siding.",
        "They are not there to eat, and they are not there to breed.",
        "They just want a dry wall to sleep inside until spring.",
        "That is why you sometimes find a confused stink bug walking across your ceiling in January.",
    ]},
    {"id": "woolly", "frases": [
        "Now for the strangest plan of all.",
        "This is the woolly bear caterpillar.",
        "It does not fly south, and it does not look for a warm place.",
        "It curls up under a leaf, and it freezes solid.",
        "Its heart stops. Its body turns hard as a rock.",
        "But before the cold arrives, it fills its body with a natural antifreeze that protects its cells from the ice.",
        "When spring comes, the caterpillar thaws out, and it walks away like nothing happened.",
    ]},
    {"id": "cloak", "frases": [
        "One butterfly uses a similar trick.",
        "The mourning cloak spends the whole winter as an adult, wedged into a crack in a tree.",
        "That is why it is often the first butterfly you see in spring, sometimes while there is still snow on the ground.",
    ]},
    {"id": "chrysalis", "frases": [
        "Other butterflies and moths spend the winter in disguise.",
        "A swallowtail turns into a chrysalis that looks exactly like a broken twig.",
        "A giant silk moth wraps itself in a cocoon and hangs from a branch like a dead leaf.",
        "You have probably looked right at one and never noticed.",
        "Inside, the animal is alive, and it is slowly being rebuilt into something with wings.",
    ]},
    {"id": "mosquito", "frases": [
        "And what about mosquitoes? Sadly, they do not all die.",
        "In some species, the females spend the winter hiding in hollow logs, storm drains, and basements.",
        "Others leave their eggs behind, and those eggs can survive being frozen for months.",
        "They hatch as soon as the ice melts.",
        "That is how mosquitoes show up so fast, the very first warm week of the year.",
    ]},
    {"id": "ants", "frases": [
        "Ants go down.",
        "As the soil gets cold, the whole colony moves deeper, below the level where the ground freezes.",
        "They seal the entrance, huddle around the queen, and barely move for months.",
        "The ant hill in your lawn is not empty. It is just closed for the season.",
    ]},
    {"id": "firefly", "frases": [
        "Fireflies are underground too.",
        "The glowing adults you see in summer only live for a few weeks.",
        "Most of a firefly's life is spent as a larva, down in the soil or under bark.",
        "It can stay there for one or two winters before it ever flies.",
        "And even the larvae glow.",
    ]},
    {"id": "cicada", "frases": [
        "And deeper still, there are the cicadas.",
        "A young cicada lives underground, drinking sap from tree roots.",
        "Winter passes over its head, again and again.",
        "Some kinds stay down there for seventeen years before they finally climb out and sing.",
        "So right now, under an ordinary lawn, there may be thousands of them, just waiting.",
    ]},
    {"id": "pond", "frases": [
        "Even a frozen pond is full of life.",
        "Under the ice, young dragonflies are still awake.",
        "They have no wings yet. They live underwater, and they keep hunting all winter long.",
        "Water at the bottom of a pond stays just above freezing, so for them, winter is only a slower season.",
    ]},
    {"id": "eggs", "frases": [
        "And then there are the ones that really do die.",
        "Crickets, grasshoppers, and praying mantises do not survive the frost.",
        "But before they go, they leave their eggs behind.",
        "A praying mantis wraps hers in a foam case that hardens like a tiny sleeping bag.",
        "It can hold up to two hundred babies, waiting on a twig all winter.",
        "The adults are gone. The next generation is already there.",
    ]},
    {"id": "snow", "frases": [
        "A few bugs do not hide at all.",
        "On a sunny winter day, look closely at the snow near the base of a tree.",
        "Those tiny black specks that look like pepper are alive.",
        "They are called snow fleas, and they walk around on the snow like it is nothing.",
        "Their bodies make a special protein that stops ice crystals from growing inside them.",
        "Scientists are studying it to help protect human organs for transplants.",
    ]},
    {"id": "leaves", "frases": [
        "So your backyard in winter is not empty.",
        "It is full of sleeping animals.",
        "And most of them are in the places we clean up.",
        "The pile of dead leaves. The hollow flower stems. The old log by the fence.",
        "When we rake everything and bag it in the fall, we throw away next year's butterflies, fireflies, and bees.",
        "So here is the easiest thing you can do for them. Leave some leaves on the ground, and wait until spring to tidy up.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "Winter does not kill the bugs.",
        "It only hides them.",
        "They are in the soil, under the bark, inside the walls, and under the ice.",
        "All of them are waiting for the same signal.",
        "One warm morning, and the whole noisy world wakes up again.",
    ]},
]
