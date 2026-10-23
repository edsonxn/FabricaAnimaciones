# -*- coding: utf-8 -*-
"""Descripción visual de CADA FRASE del Short (vertical), por clave «escena_índice»; varias variantes = la frase cae en varios
beats (se usan en orden). hacer_prompts.py (copiado de videos/corn_flakes) cruza beats y frases por tiempo."""
from guion import FICHA

P = FICHA["personajes"]
MED, CON, EMP = P["medico"], P["contador"], P["empresario"]
FLK = "thin wavy golden plasticine cereal flakes, toasted at the edges"
ROD = "a machine with two steel rollers and an iron hand crank, no electric motor"
COC = ("an 1890s health sanitarium kitchen with cast-iron stoves, copper pots, wooden tables, glass jars of grain and gas lamps")
TRIGO = "a large copper pot of boiled whole wheat grains"

D = {
    "hook_0": [f"close-up of a white bowl overflowing with {FLK}, flakes flying upward, and behind it, ghostly and forgotten, "
               f"{TRIGO} on an old cast-iron stove",
               f"{TRIGO} sitting alone on a cast-iron stove in {COC}, a single beam of window light on it, dust floating"],
    "olla_0": [f"{MED} and {CON} in linen aprons stirring {TRIGO} on a cast-iron stove in {COC}, seen from below",
               f"close-up of a wooden spoon stirring boiled wheat grains in a copper pot, steam rising"],
    "olla_1": [f"a nurse at the kitchen door calling urgently while {MED} and {CON} untie their aprons and hurry out",
               f"{TRIGO} left alone on a table in the empty kitchen, the window light turning from afternoon gold to night blue"],
    "olla_2": [f"{CON} poking the dry clumped wheat with a wooden spoon and making a face, {MED} leaning in curious",
               f"{MED} and {CON} pouring the old wheat between the steel rollers of {ROD}",
               f"close-up of {MED}'s hands turning the iron crank of {ROD}"],
    "olla_3": [f"extreme close-up of single wheat grains coming out of the steel rollers as separate {FLK}, falling like golden leaves",
               f"{MED} and {CON} with wide amazed eyes holding up one golden flake against the window light"],
    "pelea_0": [f"{MED} standing proudly in {COC} holding a bowl of plain pale flakes, pushing away a sugar bowl with a stern face"],
    "pelea_1": [f"extreme close-up of a spoon pouring sparkling white sugar over a bowl of {FLK}",
                f"{EMP} smiling in front of his own brick cereal factory with a smoking chimney, a crowd lining up with plain boxes"],
    "pelea_2": [f"{MED} and {EMP} pulling a plain cereal box in opposite directions in a tug of war inside an old wood-paneled "
                "supreme court room, three judges watching from the high bench"],
    "cierre_0": [f"a modern kitchen breakfast table with a bowl of {FLK} and milk, and two tiny plasticine figurines beside it: one "
                 f"is {MED} in miniature and the other is {EMP} in miniature, standing back to back"],
    "cierre_1": [f"{MED} and {EMP} as small plasticine figures sitting on the rim of a giant plain white ceramic bowl filled with {FLK} and milk, looking up at the viewer, warm kitchen light"],
}
