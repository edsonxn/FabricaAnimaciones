# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video. Todo imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
B = F["personajes"]["bug"]
H = F["personajes"]["human"]
W = F["personajes"]["wasp"]
ROOM = F["objeto"]
BS = ("a cartoon brown shield-shaped stink bug with small white bands on its antennae and legs, big round sleepy eyes "
      "and a tiny gray knitted beanie hat")
MANY = "dozens of small cartoon brown shield-shaped stink bugs with tiny gray beanies"
HOUSE = "a cozy two-story American suburban house with siding, windows and a window air conditioner"
FARM = "a sunny American orchard and vegetable farm with apple trees, peach trees and rows of tomatoes and corn"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every box, jar, label, sign and calendar is plain and unlabeled with no writing on it"

I = {
    1: f"{ROOM} on a cold November night, frost on the window, {H} reading a book in an armchair under the reading lamp, {FULL}.",
    2: f"Close-up of a glowing lamp shade with {BS} buzzing in clumsy circles around it, motion lines.",
    3: f"{BS} flying wobbly through the air like a drunk tiny helicopter, dizzy eyes, zigzag motion lines.",
    4: f"{BS} bonking into a lamp shade with little stars, then landing on the plaid flannel sleeve of {H}.",
    5: f"{H} raising a tissue to squish {BS} on his sleeve while glancing toward a bathroom door, thinking.",
    6: f"{H} pausing with the tissue in the air, a thoughtful face, {BS} on his sleeve looking up hopefully.",
    7: f"A cutaway of {HOUSE} in winter snow, with {BS} sleeping inside a wall space, cozy.",
    8: f"{BS} shrugging with a calm smile, nothing happening around it, a quiet room.",
    9: f"{H} scratching his head, puzzled, looking at {BS} who is just sitting there calmly.",
    10: f"A clear portrait of {BS} standing on a windowsill like a museum exhibit, a soft spotlight.",
    11: f"Extreme close-up of the striped antennae and legs of {BS}, a magnifying glass showing the little white bands.",
    12: f"A simple cartoon globe turning to East Asia, {BS} waving from a map of China, Korea and Japan, no labels.",
    13: f"A cartoon brick town in Pennsylvania in the late nineteen nineties, a man in a cap holding a small jar with a stink bug, puzzled, {NOTXT}.",
    14: f"{BS} peeking out of a big shipping container on a cargo ship arriving at a harbor, sneaky, {NOTXT}.",
    15: f"A simple cartoon map of the United States with tiny stink bugs spreading across most of the states like dots, no labels.",
    16: f"The same map of the United States almost fully covered with tiny stink bug dots, a few states clear, no labels.",
    17: f"An autumn evening with falling orange leaves, {MANY} flying through the cold air looking for shelter, shivering.",
    18: f"{HOUSE} in late autumn, warm golden light from the windows, stink bugs flying toward it.",
    19: f"Close-up of tiny gaps around a window frame, a door frame and a window air conditioner, stink bugs squeezing through each gap.",
    20: f"{BS} standing in a cozy wall space waving a tiny flag, others arriving behind it.",
    21: f"{BS} giving off wavy colored scent lines like a radio signal, more stink bugs following the lines toward it.",
    22: f"A cartoon man with a round white head, dot eyes and a cardigan collecting stink bugs into a big glass jar inside his home, determined, {NOTXT}.",
    23: f"The same man with the jar, a stack of blank calendar pages flying away behind him as days pass, {NOTXT}.",
    24: f"An enormous mountain of jars filled with stink bugs stacked in a living room, the man standing next to it amazed, {NOTXT}.",
    25: f"{HOUSE} seen from outside at night with a huge cartoon stink bug shadow glowing in every window, comic.",
    26: f"{BS} yawning and pulling up a tiny blanket inside a wall space, sleepy.",
    27: f"A cutaway of a house wall and attic with stink bugs tucked into the spaces between boards and insulation.",
    28: f"Stink bugs hiding behind the edge of house siding from outside, only their beanies peeking out.",
    29: f"{BS} in a deep sleep inside a wall space, very still, a few soft sleep bubbles, dim cozy light.",
    30: f"{BS} sleeping and ignoring a tiny plate of food, a tiny crib and a piece of wood beside it, peaceful.",
    31: f"{BS} lounging on a tiny sofa inside a wall like a roommate, a bill with no writing on it ignored on the floor.",
    32: f"{BS} asleep with a sleep mask while an unused tiny stove and a quiet phone sit nearby, {NOTXT}.",
    33: f"A carved pumpkin on one side and a basket of colorful eggs on the other, {BS} sleeping in between them.",
    34: f"Winter sun shining on the outside wall of {HOUSE}, warm light waves soaking into the siding.",
    35: f"A furnace in a basement glowing warm, heat rising up through the house walls, a stink bug stirring.",
    36: f"{BS} stumbling out of a crack in a living room wall, confused, rubbing its eyes.",
    37: f"The cartoon man with a cardigan looking at a chart drawn as simple wavy lines and a thermometer, nodding, {NOTXT}.",
    38: f"A big thermometer next to a window on a sunny winter day, more stink bugs crawling out of the baseboards as it warms.",
    39: f"{BS} flying slowly and clumsily toward a glowing lamp and a bright window, motion lines.",
    40: f"{BS} shivering on a windowsill wearing a scarf and beanie, snow outside, confused about the season.",
    41: f"{BS} looking tired and drained next to a warm radiator, a tiny empty battery symbol above it.",
    42: f"A spring windowsill with sunlight and a few still stink bugs lying quietly, gentle and soft, not gross.",
    43: f"{BS} with wavy green smell lines rising around it, a cartoon nose nearby wrinkling.",
    44: f"A human hand squeezing {BS}, which releases a puff of green cartoon smell cloud.",
    45: f"{BS} holding up one finger like a teacher about to reveal a secret, a chalkboard with no writing behind it.",
    46: f"A bunch of fresh green cilantro on a cutting board next to {BS}, both with identical wavy smell lines.",
    47: f"{H} tasting a taco with cilantro and making a face like he tasted soap, little bubbles around his mouth.",
    48: f"{H} recoiling from {BS} with a horrified face, a cilantro leaf in his hand.",
    49: f"{BS} with tiny shrugging legs, no fangs and no stinger, while a cartoon man sneezes a little nearby.",
    50: f"A curious cartoon dog sniffing a stink bug on the floor and drooling with a silly face.",
    51: f"Spring sunlight through a window, {BS} climbing up the glass toward the light, stretching.",
    52: f"{BS} flying out of an open window into a green spring garden, then turning to look back with a sly grin.",
    53: f"{FARM}, peaceful and green, with a few stink bugs arriving from the sky.",
    54: f"Stink bugs on apples, peaches and tomatoes on the farm, each fruit with tiny dimples where they fed.",
    55: f"Stink bugs on peppers and sweet corn in the farm field, a cartoon farmer in a straw hat frowning.",
    56: f"A cartoon apple farmer with a round white head, dot eyes and a straw hat holding up a dimpled damaged apple, sad.",
    57: f"Crates full of damaged apples piled high in a mid-Atlantic orchard, a sad farmer beside them, {NOTXT}.",
    58: f"{W} landing on a leaf with a heroic pose, sunlight behind it.",
    59: f"{W} standing next to a cluster of tiny round stink bug eggs on a leaf, determined, a few tiny wasp eggs inside them.",
    60: f"Back in the living room: {H} looking at {BS} still on his sleeve, deciding what to do.",
    61: f"{H} lowering his tissue, a big red X over the squish, {BS} relieved.",
    62: f"{H} nudging {BS} with a pencil into a clear jar of soapy water with bubbles on top, {NOTXT}.",
    63: f"A cartoon university lab bench with a scientist holding up a simple foil pan, {NOTXT}.",
    64: f"A foil roasting pan of soapy water under a desk lamp, glowing in a dark room, stink bugs flying toward the light.",
    65: f"The lamp-and-pan trap in a dark room at night catching many stink bugs, the man nodding approvingly.",
    66: f"{H} sealing gaps around a window frame with a caulk gun in late summer, stink bugs outside looking annoyed.",
    67: f"{H} adding foam weatherstripping around a window air conditioner, the house sealed tight.",
    68: f"{ROOM} at night, {H} in his armchair looking at {BS} on his sleeve with a gentle smile, {FULL}.",
    69: f"{BS} asleep in the wall, then waking up confused on the windowsill, two small scenes side by side.",
    70: f"{BS} flying happily over a fence toward a neighbor's peach tree full of ripe peaches, licking its lips.",
    71: f"{BS} waving goodbye with a tiny suitcase at the front door like a roommate moving out.",
    72: f"{H} shaking his head with a smile as {BS} flies off toward the neighbor's orchard, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
