# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video. Todo imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
M = F["personajes"]["mom"]
B = F["personajes"]["babies"]
H = F["personajes"]["human"]
GAR = F["objeto"]
MS = ("a cartoon wolf spider mother with a fuzzy striped gray-brown body, eight sturdy hairy legs, big shiny dark eyes, "
      "a warm motherly face and a tiny pink bandana")
KIDS = "dozens of tiny pale cartoon baby spiders with dot eyes riding piled on her back"
YARD = "an American backyard at night with grass, a garden bed, a fence and a few fallen leaves"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every box, bucket, bag, phone screen and sign is plain and unlabeled with no writing on it"

I = {
    1: f"{GAR}, {H} flipping on the garage light at evening, the bulb flickering on, {FULL}.",
    2: f"{MS} standing in the middle of the garage floor under the light, big and hairy but calm.",
    3: f"Close-up of {MS} with a strange lumpy texture on her back, little wiggle lines, mysterious.",
    4: f"{H} raising one big work boot over the spider, a dramatic shadow falling on the floor.",
    5: f"Extreme close-up of the lumps on the spider's back revealing tiny legs and tiny dot eyes, the boot frozen above.",
    6: f"{MS} with {KIDS}, hundreds of tiny faces looking up, adorable and surprising.",
    7: f"{H} frozen on one leg with the boot in the air, a big question mark above his head, sweat drop.",
    8: f"{MS} raising one leg like a teacher with a gentle knowing smile, the babies waving.",
    9: f"A clear portrait of {MS} standing on a garage floor like a museum exhibit, a soft spotlight.",
    10: f"{MS} proudly showing her babies on her back to other spiders in webs who look surprised, a little crowd.",
    11: f"{MS} walking past an empty web, shaking her head, no web for her.",
    12: f"{MS} running fast across a dark lawn at night chasing a cricket, motion lines, like a tiny wolf.",
    13: f"{MS} with a little howling pose under a full moon like a tiny wolf, comic.",
    14: f"{H} in a dark backyard sweeping a flashlight beam across the grass at night, {NOTXT}.",
    15: f"A dark lawn sparkling with tiny glowing green eye reflections in the flashlight beam, magical.",
    16: f"{MS} with a round white silk egg ball attached to the back end of her body, proud.",
    17: f"Close-up of the round silk egg sac stuck to the tip of the spider's body, like a white pearl.",
    18: f"{MS} dragging the white egg ball behind her through leaves and over twigs, determined, a calendar of weeks behind her, {NOTXT}.",
    19: f"{MS} hiding under a leaf and then running, never letting go of the egg ball, a protective face.",
    20: f"Tiny pale baby spiders climbing up their mother's legs like a staircase toward her back.",
    21: f"{MS} with babies piled on her back several layers deep like a tiny pyramid, smiling bravely.",
    22: f"{MS} walking into a cartoon grocery store with a hundred babies on her back, a shopping cart, comic, {NOTXT}.",
    23: f"An empty stroller and a parked toy car beside {MS}, who carries all the babies on her back instead.",
    24: f"Babies on their mother's back with tiny closed mouths, shaking their heads at a tiny plate of food.",
    25: f"Cutaway of a baby spider with a little glowing yellow yolk inside its belly like a lunchbox.",
    26: f"One baby spider tumbling off its mother's back onto the ground, the mother still walking on.",
    27: f"The fallen baby spider climbing back up its mother's long leg on its own, determined, a tiny flag.",
    28: f"{H} in the garage with his boot hovering again, the spider family below, a tense moment.",
    29: f"The shadow of a boot coming down over the garage floor, seen from a distance, gentle, nothing graphic shown.",
    30: f"Dozens of tiny pale baby spiders leaping off in every direction like popcorn, motion lines, comic.",
    31: f"Tiny baby spiders scattering under a workbench, between garden tools and behind a broom.",
    32: f"Baby spiders squeezing into cracks in the concrete and behind cardboard boxes, {NOTXT}.",
    33: f"{H} holding up a phone to film the garage floor, eyes wide, {NOTXT}.",
    34: f"The garage floor looking like it is exploding with tiny spiders, a comic burst effect, {H} jumping back.",
    35: f"{H} with his hands on his head, surrounded by tiny spiders hiding all over the garage.",
    36: f"A garage cutaway map showing tiny spiders spread into every corner instead of one place, dotted arrows, {NOTXT}.",
    37: f"A single tiny baby spider alone on the big concrete floor, looking around, a little brave.",
    38: f"A tiny baby spider looking at a big empty garage at night, a small backpack on, starting its journey.",
    39: f"A dry dusty garage corner with no bugs to eat, a tiny baby spider with an empty plate, sad but gentle.",
    40: f"A young wolf spider growing up, shown as three sizes in a row from tiny to big, proud.",
    41: f"A grown wolf spider chasing a cricket across the garage floor, hunter mode.",
    42: f"A grown wolf spider standing guard by a workbench while a cockroach runs away scared.",
    43: f"{YARD} in daylight, tiny spiders climbing up tall grass stems and a fence post.",
    44: f"A tiny spider on the top of a grass stem raising its body and letting out a long thin silk thread into the breeze.",
    45: f"Baby spiders floating through the blue sky on long silk threads like tiny kites, dreamy.",
    46: f"{H} peeking cautiously at {MS} from behind a garage shelf, nervous.",
    47: f"{MS} running away from {H} with her babies, a little cloud of dust, not wanting a fight.",
    48: f"{MS} curling her legs protectively over the babies on her back, a gentle mother hug.",
    49: f"A cartoon hand reaching to grab a spider with a red X over it, the spider defending itself.",
    50: f"A small cartoon bee next to a small spider, both with a tiny equal sign between them, simple comparison.",
    51: f"{H} putting the boot down and thinking, a light bulb idea above his head.",
    52: f"{H} gently setting a big clear plastic bowl over {MS} on the garage floor, {NOTXT}.",
    53: f"{H} slowly sliding a flat piece of cardboard under the bowl, the babies holding on tight to their mom.",
    54: f"{H} carrying the bowl with the cardboard out through the half-open garage door into the backyard at dusk.",
    55: f"{H} tipping the bowl next to a garden bed with fallen leaves, the spider family walking out happily.",
    56: f"{MS} running happily through the backyard grass at dusk with her babies, a cricket ahead.",
    57: f"{MS} settling into a pile of leaves in the garden with a contented smile, her babies yawning.",
    58: f"{GAR}, {H} spotting another lumpy spider on the floor and leaning in for a closer look, {FULL}.",
    59: f"{H} crouching with a magnifying glass looking at the spider, the boot safely on the floor.",
    60: f"{MS} with {KIDS}, all of them smiling and waving at {H}, a warm family portrait.",
    61: f"{MS} giving a piggyback ride to a hundred tiny babies along a garden path under the sunset, joyful.",
    62: f"A plain bucket and a piece of cardboard leaning by the garage door like heroes in a spotlight, {NOTXT}.",
    63: f"{YARD} at sunset, the spider family walking into the garden, {H} waving from the garage door, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
