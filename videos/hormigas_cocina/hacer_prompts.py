# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video. Todo imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
A = F["personajes"]["ant"]
Q = F["personajes"]["queen"]
H = F["personajes"]["human"]
KIT = F["objeto"]
AS = "a small cartoon dark brown ant with big round determined eyes and a tiny orange delivery cap"
MANY = "a long neat line of tiny cartoon dark brown ants with tiny orange delivery caps"
WALL = "a cutaway of a kitchen wall showing a big cozy ant nest inside with tunnels and chambers"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every jar, box, phone screen, can and sign is plain and unlabeled with no writing on it"

I = {
    1: f"{KIT} at seven in the morning, warm sunrise light, {H} walking in with a sleepy face and a coffee mug, {FULL}.",
    2: f"{H} freezing in the doorway, staring at {MANY} marching across the counter, wide eyes.",
    3: f"Close-up of {MANY} coming out of a small crack by the kitchen window and marching straight to a sugar bowl.",
    4: f"{H} rolling up her sleeves with a determined face, pink rubber gloves on, ready for battle.",
    5: f"{H} pressing her thumb down on the ant line with a paper towel, little comic dust puffs, ants scattering.",
    6: f"A clean empty counter with a kitchen clock showing noon, and the ant line already back from the same crack, {NOTXT}.",
    7: f"{H} with hands on hips glaring at the ant line reaching the same sugar bowl again, deadpan.",
    8: f"{AS} standing on the rim of the sugar bowl, saluting proudly, a sugar cube on its back.",
    9: f"{H} scratching her head next to a crumpled paper towel, a big question mark over the counter.",
    10: f"A cartoon iceberg in the sea, the tiny tip above water is a line of ants, the huge part below water is a giant ant nest.",
    11: f"An enormous underground ant city behind a wall, hundreds of ants busy in chambers, a tiny counter far above.",
    12: f"{AS} as a lonely scout with a tiny flashlight exploring a huge dark kitchen counter at night.",
    13: f"{AS} discovering a mountain of sugar crystals, eyes sparkling, jumping with joy.",
    14: f"{AS} walking home dragging its belly on the counter, leaving a glowing dotted green trail behind it.",
    15: f"Many ants following the glowing green dotted trail, each one adding more glow to it.",
    16: f"The glowing green trail on the counter now thick and bright like a highway with ants marching on it.",
    17: f"A big cartoon smartphone propped on the counter showing a simple map with a glowing route and a food icon, {NOTXT}.",
    18: f"Tiny ants in orange delivery caps riding tiny scooters along a glowing route on the counter.",
    19: f"A giant pink-gloved thumb squishing one tiny delivery ant while more scooters keep coming along the glowing route.",
    20: f"A busy restaurant kitchen inside an ant nest, a chef ant ringing a bell and sending out more delivery ants.",
    21: f"{WALL}, enormous, with countless rooms and ants everywhere, the counter tiny at the top, {FULL}.",
    22: f"A cartoon scientist with a round white head kneeling at a dirt ant mound with a clipboard and a tiny counter clicker, {NOTXT}.",
    23: f"A big pie chart made of ants, a small orange slice of foragers and a huge brown slice of workers staying home, {NOTXT}.",
    24: f"Old ants with tiny gray eyebrows and walking canes heading out of the nest door on a delivery run.",
    25: f"An old ant with a cane and an orange cap waving goodbye at the nest door, the young ants waving back.",
    26: f"A colony map with tiny old delivery ants at the edge and a young crowd safely inside, the old ones shrugging cheerfully.",
    27: f"{WALL} showing nurse ants feeding white larvae, builder ants carrying tiny crumbs of dirt, busy and cozy.",
    28: f"{Q} sitting on a soft throne in the royal chamber surrounded by eggs, and two more queens waving beside her.",
    29: f"Twenty squished ant outlines on the counter, {H} looking satisfied, and behind the wall a huge colony untouched.",
    30: f"{Q} in her chamber yawning and not even looking up, sipping tiny tea, unbothered.",
    31: f"{H} sniffing her fingertips with a curious face, wavy smell lines rising.",
    32: f"{H} pulling a disgusted face, a cartoon rotten coconut with green fumes floating next to her.",
    33: f"A clear portrait of {AS} standing on a kitchen tile like a museum exhibit under a soft spotlight.",
    34: f"A cutaway of {AS} with a tiny glowing chemical gland near the back of its body, a magnifying glass.",
    35: f"Ants sniffing a wavy warning smell in the air and raising their antennae in alarm.",
    36: f"A line of ants turning around with alarm, little exclamation marks over their heads, scattering.",
    37: f"{H} tapping her foot impatiently at the counter, a clock spinning, steam coming from her ears.",
    38: f"{H} blasting the ant line with a can of bug spray, a big cartoon cloud, ants running, {NOTXT}.",
    39: f"The spray cloud seeping through the crack into the wall, ants inside coughing and looking at each other.",
    40: f"An ant nest splitting in two like a cell dividing, ants pointing in two directions, comic surprise.",
    41: f"A crowd of worker ants and a queen with tiny suitcases and bundles moving out through a tunnel like a moving day.",
    42: f"Ants setting up new tiny nests in a flower pot, under the fridge and behind the dishwasher, three little camps.",
    43: f"A cutaway of a kitchen showing one ant nest in the wall turning into three nests in different spots, arrows between them.",
    44: f"Three ant queens hugging like a family reunion, their colonies around them.",
    45: f"Ants from three colonies sharing a picnic of crumbs on the floor together, friendly, no fighting.",
    46: f"{KIT} seen wide with three ant lines coming from three directions, {H} standing in the middle stunned, {FULL}.",
    47: f"Two ants carrying a squished ant away on a tiny stretcher, solemn, along the counter.",
    48: f"A black and white style cartoon of a nineteen fifties laboratory with ant farms in glass boxes, {NOTXT}.",
    49: f"A friendly cartoon scientist with round glasses and a short side-parted hairstyle looking into a glass ant farm, curious.",
    50: f"A still ant lying on its back with a faint wavy yellow smell cloud rising from it, gentle and comic, not gross.",
    51: f"Ants sniffing the yellow smell cloud with their antennae, then nodding to each other.",
    52: f"Ants carrying a body to a small pile of trash at the edge of the nest, the colony garbage dump.",
    53: f"The scientist painting a tiny drop of yellow liquid on a living ant with a fine brush.",
    54: f"Two ants carrying a protesting living ant to the trash pile, the living ant kicking its legs with an outraged face.",
    55: f"The living ant sitting on top of the trash pile with crossed arms, offended, the others walking away.",
    56: f"{H} wiping the counter with a sponge and soapy water, the glowing green trail fading away under the bubbles.",
    57: f"Ants arriving at the edge of a clean counter, confused, looking at a blank map with no route, question marks.",
    58: f"{H} pouring sugar into a sealed glass jar and clicking the lid shut, {NOTXT}.",
    59: f"A delivery ant on a scooter staring sadly at a tightly closed glass jar of sugar, comic.",
    60: f"{H} placing a small plain round ant bait station by the crack instead of a spray can, {NOTXT}.",
    61: f"Ants carrying tiny drops from the bait into the nest and passing them mouth to mouth in a long line.",
    62: f"A chain of ants passing a tiny drop deep into the nest all the way to {Q} and the larvae.",
    63: f"{WALL} getting quiet and empty, a few ants sleeping, the tunnels still, a calm ending, gentle and not grim.",
    64: f"{KIT} the next morning, {H} with coffee looking at a short ant line on the counter, calm and knowing, {FULL}.",
    65: f"A row of tiny ants in orange delivery caps looking up at {H}, holding tiny phones, polite.",
    66: f"{H} wiping the glowing trail away with one swipe of a soapy sponge, the ants looking at their blank phones.",
    67: f"An ant restaurant door behind the wall with a closed shutter pulled down, the chef ant shrugging, {H} smiling at the counter.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
