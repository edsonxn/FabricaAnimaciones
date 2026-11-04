# -*- coding: utf-8 -*-
"""Descripción visual de CADA FRASE del Short (vertical), por clave «escena_índice»; varias variantes = la frase cae en varios
beats (se usan en orden). hacer_prompts.py (copiado de videos/corn_flakes_short) cruza beats y frases por tiempo."""
from guion import FICHA

P = FICHA["personajes"]
INV, ESP = P["inventor"], P["esposa"]
FID = "a block of wavy golden fried plasticine noodles, square and crinkled, with tiny holes"
SAR = "a deep black iron frying pan of bubbling golden oil"
COB = ("a small wooden shed in the backyard of a modest 1950s Japanese house: wooden walls, a bare light bulb, a second-hand "
       "cast-iron noodle-making machine with a hand crank, a gas burner, flour sacks without letters, bamboo baskets")
COC = "a small 1950s Japanese home kitchen at night: wooden shelves, ceramic bowls, a gas burner, a paper lantern glow"

D = {
    "hook_0": [f"{ESP} in {COC}, dipping battered vegetables into {SAR}, and behind her, peeking through the doorway with wide "
               f"amazed eyes behind his glasses, {INV}",
               f"extreme close-up of battered vegetables bubbling in {SAR}, thousands of tiny bubbles, steam rising"],
    "ruina_0": [f"{INV} sitting alone on a wooden step in front of a closed office door with an empty wooden desk and a toppled "
                "chair, holding his glasses in his hand, head down, gray rainy light",
                f"{INV} carrying a single cardboard box down an empty street at dusk, looking back over his shoulder"],
    "ruina_1": [f"{INV} standing in front of a modest 1950s Japanese wooden house with a small backyard, the only thing left, "
                "a single tree, soft evening light"],
    "ruina_2": [f"{INV} hammering wooden planks to build {COB.split(':')[0]}, seen from below, morning light",
                f"wide view of {COB}, {INV} oiling the crank of the noodle machine"],
    "ruina_3": [f"{INV} dropping a lump of sticky failed noodles into an overflowing bamboo trash basket inside {COB}",
                f"{INV} asleep with his head on the table inside {COB} at night under the bare light bulb, piles of failed "
                "noodles around him",
                f"close-up of a row of failed noodle blocks on a wooden shelf: crumbled, moldy green, burnt black"],
    "tempura_0": [f"{ESP} smiling in {COC}, dipping a piece of battered sweet potato into {SAR}, {INV} watching from the "
                  "doorway",
                  f"{INV} and {ESP} side by side at the stove in {COC}, he leans in very close to the frying pan"],
    "tempura_1": [f"extreme close-up of a battered vegetable in {SAR}: water escaping as bubbles and steam, the batter puffing "
                  "with thousands of tiny holes",
                  f"macro close-up of a golden crispy tempura piece broken in half, its inside full of tiny air holes, "
                  "held by wooden chopsticks"],
    "tempura_2": [f"{INV} running across the dark backyard toward {COB.split(':')[0]} with a lit bare light bulb, excited",
                  f"{INV} lowering {FID} with a wire basket into {SAR} inside {COB}, oil bubbling hard",
                  f"close-up of {FID} lifted out of the oil, dry and crispy, light shining through its tiny pores"],
    "tempura_3": [f"{INV} pouring hot water from an iron kettle over {FID} in a plain white ceramic bowl, steam rising",
                  f"{INV} lifting soft steaming noodles with chopsticks from a plain white ceramic bowl, eyes wide with joy, "
                  f"{ESP} clapping behind him"],
    "cierre_0": [f"a huge mountain of plain white bowls of steaming noodles stacked to the sky over a city at night, tiny "
                 "plasticine people eating everywhere",
                 f"a tiny {INV} in miniature standing on the rim of a giant plain white ceramic bowl of steaming noodles, "
                 "arms raised in triumph, warm light"],
    "cierre_1": [f"three plasticine policemen in 1970s dark winter uniforms and helmets eating steaming noodles from plain white "
                 "foam cups in deep mountain snow, falling snowflakes, a wooden mountain lodge far behind",
                 f"close-up of a plasticine policeman with frosty cheeks blowing on a plain white foam cup of hot noodles in the snow"],
}
