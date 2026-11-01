# -*- coding: utf-8 -*-
"""WARCRAFT (1983) · Los Páramos de Poniente — «Estofado de Poniente».
Corto de ~72 s para Crónicas de Warcraft (16:9), SIN VOZ: montaje con música Lyria + foley, como si fuera una película de
fantasía de 1983 (35 mm, efectos prácticos). Criaturas de plastilina, peluche y animatrónicos junto a actores reales.
Referencia: https://youtu.be/3tNWWl7_NsI («WARCRAFT (1982): The Warrior», endroxia; 416 mil vistas en 9 días).
Misión real del juego: «Westfall Stew» de Salma Saldean (granja de los Saldean): carne de buitre, ojo de múrloc,
hocico de jabalí Colmillosangriento y quimbombó (okra), con los Vigías de la cosecha rondando los campos.

Presupuesto Flow: 50 puntos → 7 clips de 10 s en 360p (7 puntos c/u = 49) con combinar=True → 14 escenas, 70 s.
Rótulos de pergamino y la ficha del héroe = imágenes (gratis). Prompts de Flow en inglés.
"""

TITULO = "WARCRAFT (1983): El Guerrero y el Estofado de Poniente"
ARCHIVO = "warcraft_1983_estofado_poniente"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
SIN_VOZ = True          # `secuencia` lo soporta desde el 15-oct-2026: un beat por clip y prompts desde PLANOS
SUBTITULOS = False
DURACION = 72.0
BPM = 100               # 1 compás = 2,4 s

SECUENCIA = dict(
    clips_s=[10] * 7,   # 7 × 7 puntos = 49 de 50
    video_calidad="360p",
    combinar=True,      # cada clip une DOS escenas (A 0-5 s, B 5-10 s) con una transición en el estilo
    fundido=0.0,        # cortes secos entre clips, como montaje ochentero; la transición va dentro del clip
    ambiente=0.7,       # sin voz: el sonido propio del clip pesa más (foley); callar el que meta voces
    ambiente_por={},
    # marco de película que Flow pinta (esquinas redondeadas, letras de Kodak en el borde), medido el 16-oct
    recorte_por={"scene-001": 0.035, "scene-002": 0.035, "scene-004": 0.035, "scene-005": 0.04, "scene-007": 0.05},
    carpeta_descargas="flow-wow_estofado_poniente",
)

# Ficha visual: se repite PALABRA POR PALABRA en cada prompt donde aparezca.
FICHA = dict(
    estilo="A moving scene from a 1983 live-action dark fantasy movie, shot on grainy 35mm Kodak film, soft diffusion haze, "
           "warm amber color grading, slight gate weave, practical effects only: real actors and real sets combined with "
           "claymation and stop-motion creatures, felt puppets and animatronics, like an early-80s Jim Henson and Ray "
           "Harryhausen production, sixteen by nine",
    personajes={
        "guerrero": "a human warrior in his thirties played by a real actor, long messy chestnut hair, thick mustache, "
                    "worn chainmail shirt over a faded red tunic with a small golden lion patch, brown leather bracers "
                    "and belt, scuffed knee-high boots, a huge two-handed sword strapped to his back",
        "salma": "a sturdy farm woman in her fifties played by a real actress, grey-streaked hair in a bun, rolled-up "
                 "sleeves, long brown apron, kind but impatient face",
        "buitre": "a scruffy stop-motion vulture puppet with patchy grey feathers and a bald pink neck, jerky "
                  "frame-by-frame movement",
        "jabali": "a plush felt boar puppet the size of a pony, with button eyes, bristly brown fur and oversized "
                  "yellowed tusks, moving in jerky stop-motion",
        "murloc": "a glossy green claymation murloc, a fish-frog creature with huge wet black eyes, an orange fin crest "
                  "and tiny teeth, visible fingerprints in the clay",
        "vigia": "a harvest watcher: a towering scarecrow golem animatronic made of rusty iron plates and planks, a "
                 "burlap sack head with stitched glowing yellow eyes, straw bursting from the joints, scythe blades "
                 "for hands",
    },
    nombres={"guerrero": "The warrior", "salma": "Salma", "buitre": "The vulture", "jabali": "The boar",
             "murloc": "Each murloc", "vigia": "The harvest watcher"},
    objeto="a black iron cauldron of bubbling brown stew over a wood fire",
    epoca="Westfall, a dry golden farmland of wheat fields, broken wooden fences, a creaking wooden windmill, "
          "red-roofed farmhouses and a rocky coast with shipwrecks; medieval fantasy, no guns, no modern objects",
    cierre="No text, no letters, no logos, no modern objects. No dialogue, no voices.",
)

# 14 escenas en 7 clips combinados (A = primeros 5 s, B = últimos 5 s). Personajes: claves de FICHA["personajes"].
PLANOS = [
    dict(clip=1, personajes=["guerrero", "salma"],
         a="Low-angle wide shot at golden hour: endless wheat fields of Westfall, a creaking windmill and a broken fence; "
           "the warrior walks out of the shimmering heat haze on a dusty road, sword on his back, wind in his hair.",
         transicion="a strong gust bends the wheat across the whole frame and when it passes we are in scene two",
         b="On the porch of a red-roofed farmhouse, Salma hands the warrior a long rolled parchment scroll; he unrolls "
           "it, it drops to the floor, and he looks into the camera with an exaggerated confident grin."),
    dict(clip=2, personajes=["guerrero", "buitre"],
         a="On a rocky hill under a hard sun, the warrior swings his huge sword at the stop-motion vulture, which hops "
           "aside in jerky frame-by-frame motion and pecks the top of his head.",
         transicion="the vulture flaps straight at the camera, its ragged wings cover the frame, and it flies away to "
                    "reveal scene two",
         b="The dishevelled warrior, feathers stuck in his hair, proudly holds up a tiny scrawny drumstick while a "
           "single grey feather drifts down in front of his face."),
    dict(clip=3, personajes=["guerrero", "jabali"],
         a="In dry golden grass, the plush felt boar paws the ground and charges in jerky stop-motion straight at the "
           "warrior, who plants his feet and raises his sword.",
         transicion="the impact throws up a thick cloud of golden dust that fills the frame and settles into scene two",
         b="The dazed warrior sits in the grass with his hair standing up, holding a big pink felt boar snout like a "
           "trophy, while the plush boar trots away offended, now with a little cloth bandage on its face. No blood."),
    dict(clip=4, personajes=["guerrero", "murloc"],
         a="A rocky coast at sunset beside a half-sunken wooden shipwreck: three glossy claymation murlocs rise from "
           "the foamy surf in stop-motion, gurgling, fin crests flaring.",
         transicion="a big wave crashes over the camera, the frame turns to water and foam, and drains away into scene two",
         b="The warrior lies on the wet sand buried under a wriggling pile of small claymation murlocs, one arm sticking "
           "out, triumphantly holding up a small glass jar with a glowing round murloc eye inside."),
    dict(clip=5, personajes=["guerrero", "vigia"],
         a="Night, a field of tall okra plants under a huge full moon: the warrior tiptoes between the plants filling a "
           "burlap sack with green okra pods, looking over his shoulder.",
         transicion="the camera pushes into the round full moon until it fills the frame, and that glowing circle "
                    "becomes the round glowing yellow eye of the harvest watcher in scene two",
         b="Behind the frozen warrior, the harvest watcher animatronic rises slowly from the field with creaking rusty "
           "joints, straw falling from its body, raising its scythe hands against the moonlight."),
    dict(clip=6, personajes=["guerrero", "vigia", "salma"],
         a="Moonlit chase: the warrior sprints through the okra field clutching his sack while the harvest watcher stomps "
           "after him in stop-motion, scythes slicing plants, straw and leaves flying.",
         transicion="the warrior dives head-first through the open farmhouse door toward the camera, the door slams "
                    "into black, and firelight blooms into scene two",
         b="Inside the warm farmhouse lit by a crackling fireplace, the battered warrior slams the sack, the drumstick, "
           "the snout and the jar on a wooden table; Salma inspects each item, unimpressed."),
    dict(clip=7, personajes=["guerrero", "salma"],
         a="Salma tips everything into the bubbling cauldron over the fire; the warrior, exhausted and smiling, lifts a "
           "wooden spoon of stew to his mouth.",
         transicion="a thick cloud of steam rises from the cauldron and fills the frame, then clears into scene two",
         b="Close-up of the cauldron: a small glossy claymation creature made of stew and okra rises out of the broth "
           "and blinks at the warrior, who freezes with the spoon at his lips, eyes wide."),
]

# Rótulos (imagen de pergamino + letra serif amarilla, por código; texto solo para énfasis).
ROTULOS = [
    dict(t=0.0, dur=2.4, texto="WARCRAFT (1983)\nLos Páramos de Poniente"),
    dict(t=12.0, dur=2.0, texto="Misión: Estofado de Poniente\nCarne de buitre · Hocico de jabalí\nOjo de múrloc · Quimbombó"),
    dict(t=69.6, dur=2.4, texto="Continuará…"),
]

LYRIA = dict(
    estilo="Early-1980s fantasy film score: warm analog synthesizer pads with a small orchestra, folk flute and lute, "
           "heroic but playful, light comic stingers, 100 BPM.",
    escenas={
        "intro": ("A single heroic brass and synth fanfare over a held pad, like a film title card.", 5),
        "dia": ("Sunny pastoral flute and lute theme over wheat fields, growing into a bouncy adventure rhythm with "
                "comic orchestral hits every ten seconds: a squawk-like woodwind, a charging timpani run, a gurgling "
                "bassoon.", 6),
        "noche": ("Night: eerie low strings and creaking wooden percussion, a slow menacing rise, then a frantic "
                  "chase with fast strings and pounding drums.", 8),
        "cierre": ("Cosy tavern fireplace tune on lute and flute, warm and relieved, that stops dead on a single comic "
                   "synth sting, then silence.", 4),
    },
    tramos=[(["intro", "dia", "noche", "cierre"], "Begin with the fanfare and end on the comic sting followed by silence.")],
)

MEZCLA = dict(musica=-15.0)   # SIN_VOZ: la música lleva el montaje (el valor general, -20, es cama bajo narración)
TRANSICIONES = [("corte", 0.0)] * 8
MUSICA = {"intro": dict(sabor="esperanza"), "noche": dict(sabor="tension"), "cierre": dict(sabor="esperanza")}

ESCENAS = [   # secciones musicales (SIN_VOZ): 30 compases ≈ 72 s
    {"id": "intro", "compases": 1, "frases": []},       # rótulo de título
    {"id": "dia", "compases": 16, "frases": []},        # clips 1-4: campo, buitre, jabalí, múrlocs
    {"id": "noche", "compases": 8, "frases": []},       # clips 5-6: quimbombó, Vigía, persecución
    {"id": "cierre", "compases": 5, "frases": []},      # clip 7 + «Continuará…»
]
