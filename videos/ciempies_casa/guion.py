# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — «Never Kill a House Centipede. Here's Why»  Motor SECUENCIA.
Hechos usados (Scutigera coleoptrata; Penn State Extension, University of Minnesota Extension, Animal Diversity Web):
origen mediterráneo; adulto con 15 pares de patas, nace con 4 y gana pares en cada muda; corre ~40 cm por segundo;
patas traseras largas que parecen antenas; puede soltar patas para escapar; ojos compuestos (raro en ciempiés);
caza de noche cucarachas, pececillos de plata, termitas, chinches, moscas, hormigas y arañas; inyecta veneno con el
primer par de patas modificado; sujeta varias presas con las patas; se limpia las patas una por una; pierde agua con
facilidad (por eso baños y sótanos); vive de 3 a 7 años; la picadura a personas es rara y leve; no hace nido ni telaraña,
no daña madera, comida ni ropa; verlo seguido indica humedad y otras plagas.
Todo en imagen (Flow sin puntos de video el 7-oct-2026).
"""

TITULO = "Never Kill a House Centipede. Here's Why"
ARCHIVO = "house_centipede"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

CER_MAX_POR_FRASE = {"legs_1": 0.2}   # Whisper escribe «15 pairs» con cifras; la toma está bien

SECUENCIA = dict(
    video_s=0,          # sin puntos de video en Flow: todo imagen
    clip_s=8,
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-ciempies_casa",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "centipede": "a cartoon house centipede with a long flat yellowish-tan body with three dark stripes along its "
                     "back, fifteen pairs of very long thin striped legs fanning out on both sides, two long antennae, "
                     "two big round expressive eyes and a tiny blue detective hat",
        "human": "a simple cartoon person with a round white head, dot eyes, a red baseball cap and a blue t-shirt",
    },
    objeto="a rolled up newspaper",
    epoca="present-day suburban house interior",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "hook": dict(sabor="tension"), "who": dict(sabor="espacio"), "legs": dict(sabor="esperanza"),
    "speed": dict(sabor="tension"), "hunter": dict(sabor="tension"), "menu": dict(sabor="espacio"),
    "clean": dict(sabor="esperanza"), "danger": dict(sabor="espacio"), "why": dict(sabor="vacio"),
    "deal": dict(sabor="esperanza"), "outro": dict(sabor="esperanza"),
}

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "It is late at night. You turn on the bathroom light.",
        "And something with way too many legs shoots across the wall.",
        "It might be the scariest looking thing that lives in your house.",
        "Your first instinct is to grab a shoe.",
        "Don't.",
        "Because that little monster is the best roommate you will ever have.",
    ]},
    {"id": "who", "frases": [
        "This is the house centipede.",
        "It originally came from the warm coasts of the Mediterranean.",
        "But it followed people around the world, and today it lives in homes on almost every continent.",
        "And it has probably been in your house for years without you noticing.",
    ]},
    {"id": "legs", "frases": [
        "Let's start with those legs.",
        "A grown house centipede walks on fifteen pairs of legs.",
        "But it is not born that way.",
        "A baby hatches with only eight legs.",
        "Every time it sheds its skin, it grows a few more, until it finally has the full set.",
        "The last pair is so long that it looks like a second pair of antennae.",
        "That makes it very hard for an enemy to tell which end is the head.",
    ]},
    {"id": "speed", "frases": [
        "All those legs are built for one thing: speed.",
        "A house centipede can run more than a foot every second.",
        "For an animal that small, that is like a person running as fast as a car on the highway.",
        "It can sprint across floors, straight up walls, and even upside down along the ceiling.",
        "And if something grabs one of its legs, it just lets that leg go and keeps running.",
    ]},
    {"id": "hunter", "frases": [
        "But that speed is not for running away from you.",
        "It is for hunting.",
        "The house centipede does not build a web, and it does not wait in a trap.",
        "It goes out every night and chases its food.",
        "Unlike most centipedes, it has large eyes, and it uses its long antennae to smell and feel its prey.",
        "When it catches up, it pounces and grabs the victim with its front legs.",
        "Then it delivers a quick dose of venom, and the hunt is over.",
    ]},
    {"id": "menu", "frases": [
        "So what is it hunting inside your house?",
        "Pretty much everything you hate.",
        "Cockroaches. Silverfish. Termites. Bed bugs. Flies. Ants. And spiders too.",
        "It can even hold several victims at once, trapped between its legs, while it eats another one.",
        "Many bug experts consider it one of the most helpful animals that can live in a home.",
    ]},
    {"id": "clean", "frases": [
        "And it is surprisingly clean.",
        "After a meal, a house centipede carefully grooms itself, pulling each leg through its mouth, one at a time.",
        "It does not make a nest. It does not spin webs.",
        "It does not chew on wood, and it does not touch your food or your clothes.",
    ]},
    {"id": "danger", "frases": [
        "But can it hurt you?",
        "Technically, it does have venom.",
        "But it is made for insects, and its tiny jaws can barely get through human skin.",
        "Bites are extremely rare, and they usually happen only when someone grabs one with a bare hand.",
        "Even then, it feels like a mild bee sting.",
        "A house centipede that sees you has only one plan: run and hide.",
    ]},
    {"id": "why", "frases": [
        "So why is it in your bathroom?",
        "Its body loses water very easily, so it needs damp air to survive.",
        "That is why you find it in bathrooms, basements, and under the kitchen sink.",
        "And here is the part most people miss.",
        "A house centipede only stays where there is food.",
        "If you keep seeing them, it means your house has other bugs, and they are eating them for you.",
    ]},
    {"id": "deal", "frases": [
        "If you really don't want them around, don't reach for the spray.",
        "Dry out the damp rooms, seal the cracks, and deal with the pests they are feeding on.",
        "When the food and the moisture are gone, the centipedes leave on their own.",
        "And if you find one in the sink, slide a glass over it and move it to the basement.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "A house centipede can live for up to seven years.",
        "That is seven years of quiet night shifts, hunting the things that really cause problems.",
        "So the next time one races across your wall, take a breath, and put the shoe down.",
        "It was never after you. It is just late for work.",
    ]},
]
