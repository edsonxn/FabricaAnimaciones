# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video. Todo imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
M = F["personajes"]["moth"]
H = F["personajes"]["human"]
BAT = F["personajes"]["bat"]
LAMP = F["objeto"]
MS = ("a cartoon fluffy tan moth with soft brown patterned wings, feathery antennae, big round dizzy eyes and tiny "
      "aviator goggles pushed up on its head")
MANY = "dozens of small cartoon fluffy tan moths with feathery antennae"
PORCH = "an American front porch on a warm summer night with a wooden house wall, a dark blue sky and a garden of white night flowers"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every screen, chart, bulb box, switch and sign is plain and unlabeled with no writing on it"

I = {
    1: f"{PORCH}, {H} flipping on a light switch by the front door, {LAMP} turning on, {FULL}.",
    2: f"{MANY} arriving out of the dark garden toward the glowing porch light, a little parade.",
    3: f"{MANY} spinning in circles around {LAMP} with swirling motion lines, chaotic and comic.",
    4: f"{MS} bonking its head against the glass lantern with tiny stars, dizzy, still circling.",
    5: f"Morning light on a pale wooden house wall with a few tired moths flattened against it, still and sleepy, gentle.",
    6: f"{MS} circling the porch light with a tired face and droopy wings, a tiny clock showing late night, {NOTXT}.",
    7: f"{H} in the doorway in pajamas looking up at the moths circling the light, puzzled, a question mark.",
    8: f"An old storybook-style scene of a moth hugging a candle flame with little hearts around it, romantic and silly.",
    9: f"A dark cartoon lab tent with several cameras on tripods pointed at a glowing bulb, red recording dots, {NOTXT}.",
    10: f"{MS} shaking its head no with a big red X over a heart symbol next to the bulb.",
    11: f"{MS} caught in a glowing circular orbit around the bulb like a tiny planet on a track, worried face.",
    12: f"{MS} flying under a big full moon in a dark night sky, a dotted line showing a straight flight path.",
    13: f"A simple diagram drawing of a moth flying straight with the moon always at the same angle, dashed guide lines, {NOTXT}.",
    14: f"{MS} mistaking a porch bulb for the moon, a dotted path spiraling inward toward the bulb.",
    15: f"A cartoon scientist with a round white head scratching her chin in front of a chalkboard with a spiral drawn on it, {NOTXT}.",
    16: f"A cartoon field team at night in a meadow with tripods, cameras and a glowing lamp, insects around it, {NOTXT}.",
    17: f"Glowing 3D flight paths of insects drawn as colored ribbons looping around a lamp, seen on a simple screen, {NOTXT}.",
    18: f"{MS} leaning toward the viewer to tell a secret, one wing raised, wide eyes.",
    19: f"A starry glowing night sky above a dark prehistoric forest with ferns, the sky the brightest thing in the scene.",
    20: f"{MS} flying level with its back facing up toward the bright starry sky, a tiny arrow pointing up.",
    21: f"Several cartoon flying insects, a moth, a dragonfly and a beetle, all flying level with their backs turned to the bright sky.",
    22: f"{MS} sitting in a tiny airplane cockpit with an autopilot dial showing a little horizon, goggles on, relaxed.",
    23: f"{MS} flying next to a bright porch bulb, the bulb so bright it outshines the moon behind it.",
    24: f"{MS} tilting sideways in mid-air with its back facing the bright bulb, confused, the real sky above ignored.",
    25: f"{MS} flying in a perfect circle around the porch light with a circular motion trail, stuck.",
    26: f"{MS} orbiting the bulb like a tiny satellite around a planet, a dotted circular orbit line, dizzy.",
    27: f"{MS} flipping upside down right above the bulb, legs in the air, a surprised face.",
    28: f"{MS} flying upside down with the dark sky below it and the bright bulb above, utterly confused.",
    29: f"A moth, a dragonfly and a small beetle all circling the same porch light together, comic chaos.",
    30: f"{H} driving a small car at night on a dark road, a dashboard navigation screen showing only a curved left arrow, {NOTXT}.",
    31: f"{H}'s small car driving in endless circles around a roundabout at night, dizzy swirl lines, comic.",
    32: f"{MS} circling the light again and again, sweat drops flying, an energy bar draining above it, {NOTXT}.",
    33: f"{MS} looking sadly at a distant flower and another moth waving from the dark garden, out of reach.",
    34: f"An exhausted moth gently drifting down from the light toward the porch floor, eyes closed, soft and not grim.",
    35: f"Moths resting frozen on the pale porch wall under the light, stiff like little statues, waiting for morning.",
    36: f"Dawn over the porch, a pale moth sitting on a bright white wall in plain view, nervous, sweat drop.",
    37: f"A cartoon robin and a small green lizard peeking around the corner of the wall, eyeing the moth hungrily.",
    38: f"The porch light at night shown as a buffet table with moths, little forks and plates around it, comic.",
    39: f"{BAT} swooping through the moths around the porch light with a grin, motion lines.",
    40: f"A cartoon orb web spider waiting in a web right next to the porch light, licking its lips at the moths.",
    41: f"{MS} looking out from the porch at a dark empty garden where white flowers wait with no visitors.",
    42: f"{MS} standing seriously with its wings folded, a big important face, a dramatic spotlight.",
    43: f"{MS} wearing a tiny night shift worker vest and a lantern, flying to a white night flower under the moon.",
    44: f"{MS} carrying golden pollen dust from one white flower to another in the moonlight, sleeping bees in a hive nearby.",
    45: f"A cartoon English countryside at night with hedges and wildflowers, scientists with flashlights watching moths.",
    46: f"A whole moonlit field of wildflowers with moths carrying sparkly pollen trails between them, dreamy.",
    47: f"A Swiss alpine meadow at night under mountains, with a row of streetlights shining on one half of the field.",
    48: f"The lit half of the meadow with almost no moths and the dark half full of moths visiting flowers, a clear contrast.",
    49: f"A big cartoon chart made of moth icons, a tall stack on the dark side and a much shorter stack on the lit side, {NOTXT}.",
    50: f"A cartoon thistle plant with fewer seed heads and fruits on the lit side than on the dark side, simple comparison.",
    51: f"A single glaring streetlight over a sad quiet meadow, a lonely flower drooping.",
    52: f"{H} on the porch with hands on hips, smiling with a determined look, ready to help.",
    53: f"{H} switching off the porch light, and a small motion sensor on the wall, {NOTXT}.",
    54: f"{H} on a step stool swapping a white bulb for a warm yellow bulb in the porch lantern, {NOTXT}.",
    55: f"{PORCH} lit by a warm yellow bulb with only one or two moths calmly flying past, peaceful.",
    56: f"A porch lamp with a downward shade throwing a cone of light onto the steps, the sky above dark and starry.",
    57: f"{MS} flying happily under a starry sky with the porch light shining only on the ground below it.",
    58: f"{H} closing the curtains of a lit living room window at night, the yard staying dark.",
    59: f"A dark garden with fireflies and moths visiting flowers, a house with curtains closed in the background.",
    60: f"{PORCH}, {H} looking up at {MS} circling the light, a gentle understanding smile, {FULL}.",
    61: f"{MS} shaking its head shyly with a tiny broken heart next to the bulb, it was never love.",
    62: f"{MS} spinning in tired circles around the bulb, holding a tiny compass that spins wildly.",
    63: f"{H} flipping the switch off, the porch going dark and the moth looking up at the real moon and stars.",
    64: f"{MS} flying off happily toward a glowing full moon over the garden, goggles down, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
