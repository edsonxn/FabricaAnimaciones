# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
Z = F["personajes"]["centipede"]
H = F["personajes"]["human"]
ZS = ("a cartoon house centipede with a long flat yellowish-tan body with three dark stripes, many very long thin "
      "striped legs fanning out on both sides, two long antennae and two big round expressive eyes")
FULL = "the room filling the whole image to every edge with no white margin and no panel outline"

P = {
    1: f"A dark bathroom at night seen from the doorway, a hand of {H} flipping a light switch, warm light just turning on over a sink, a bathtub and a tiled wall, {FULL}.",
    2: f"A tiled bathroom wall with {Z} racing across it at high speed with long speed lines behind it, while {H} in pajamas jumps back with a shocked face, {FULL}.",
    3: f"Extreme close-up portrait of {Z} on a tiled wall drawn to look dramatic and spooky, lit from below with a long shadow of many legs stretching up the wall behind it.",
    4: f"{H} in a bathroom raising a sneaker high above his head with a determined face, looking at a small house centipede on the wall across the room, {FULL}.",
    5: f"A big red stop hand sign held up in front of {H}, who freezes with a sneaker in his hand, while {Z} on the wall beside him waves several legs in a friendly hello, in a tiled bathroom, {FULL}.",
    6: f"{Z} and {H} sitting side by side on a sofa like roommates watching television at night, the centipede holding a tiny bowl of popcorn, {FULL}.",
    7: f"A sunny Mediterranean coast with blue sea, white stone houses with terracotta roofs, olive trees and warm rocks, and {Z} sunbathing happily on a warm rock in the foreground.",
    8: f"A simple round cartoon globe of the Earth with a dotted travel line going around it, and {Z} riding on top of a wooden shipping crate on an old sailing ship crossing the ocean.",
    9: f"Cutaway view of a wooden suburban house like a dollhouse showing every room, with {ZS} hidden in the basement, another behind the bathtub and another under the kitchen sink.",
    10: f"{H} brushing his teeth at a bathroom sink, completely unaware of {Z} peeking out from behind the mirror right next to him, with a wall calendar whose pages are flying off.",
    11: f"Simple diagram on a plain off-white background: {Z} seen from directly above, perfectly symmetrical, with all fifteen long legs on each side spread out neatly like the teeth of a comb.",
    12: f"A tiny white egg on damp soil under a floorboard cracking open, with two tiny round eyes peeking out of the shell, soft light.",
    13: f"A tiny baby cartoon house centipede with a very short yellowish-tan body and only four pairs of short legs, big round eyes, looking proud and wobbly next to a broken eggshell.",
    14: f"A row of five cartoon house centipedes on a plain off-white background growing from left to right, each one longer and with more legs than the last, with a thin empty shed skin lying behind each one and small arrows between them.",
    15: f"Side view of {Z} on a wooden floor showing its two rear legs, which are extremely long and trail far behind its body like a second pair of antennae.",
    16: f"{ZS} seen from above on a plain off-white background with long antennae at the front and equally long rear legs at the back, so both ends look the same, with two big question marks, one over each end.",
    17: f"A cartoon brown spider looking very confused, scratching its head with one leg, staring at {ZS} whose front end and back end look exactly alike.",
    18: f"{Z} in a sprinter starting position on a wooden floor with a tiny racing number pinned to its back, all legs tensed, dust puffs behind it.",
    19: f"{Z} running at full speed along a wooden floor beside a long yellow measuring ruler lying on the floor, its legs a blur of motion lines, a small stopwatch in the corner.",
    20: f"A cartoon running track with {H} sprinting so fast his legs are a spinning blur and his cap flies off, with speed lines and dust clouds.",
    21: f"A highway with a red cartoon car driving fast, and {H} running in the next lane keeping up with the car, the driver looking out the window amazed.",
    22: f"A room corner shown with the floor, a wall and the ceiling, and three of {ZS} running at once: one across the floor, one straight up the wall and one upside down on the ceiling.",
    23: f"A big cartoon bird beak pinching one single long striped leg, while {Z} sprints away unharmed with a cheeky look back over its shoulder.",
    24: f"{Z} standing on a bathroom floor looking up calmly at {H}, who is standing on top of a toilet seat in fear, {FULL}.",
    25: f"A dark kitchen at night lit by moonlight through the window, {Z} crouched low on the floor like a prowling predator with narrowed focused eyes.",
    26: f"Split scene: on the left a cartoon spider sitting lazily in a web in a corner, crossed out with a big red cross, on the right {Z} running freely across an open floor.",
    27: f"A dark hallway at night with a wall clock showing midnight, {Z} leaving a crack under a baseboard and marching out with a tiny lunchbox like going to work.",
    28: f"Extreme close-up of the face of {Z}, showing two large shiny dark compound eyes with a honeycomb pattern and the base of its two long antennae.",
    29: f"{Z} on a dark kitchen floor sweeping its two very long antennae forward, with small wavy scent lines drifting from a cartoon cockroach hiding behind a table leg.",
    30: f"{Z} leaping through the air with all its legs spread wide like a net, about to land on a startled cartoon cockroach on a kitchen floor.",
    31: f"{Z} holding a cartoon cockroach wrapped tightly in its long front legs, the cockroach with dizzy spiral eyes and small stars above its head, a tiny green droplet symbol beside them.",
    32: f"{Z} standing on a kitchen floor at night holding a tiny magnifying glass and inspecting tiny footprints, like a detective on a case.",
    33: f"A cartoon wanted poster board on a wall with blank picture frames, and in the largest frame a guilty-looking brown cartoon cockroach, with {Z} pointing at it.",
    34: f"Six small cartoon pests lined up in a row against a height chart like a police lineup: a silverfish, a termite, a bed bug, a house fly, an ant and a cockroach, all looking nervous.",
    35: f"{Z} staring down at a small nervous brown cartoon spider that is backing away into a corner with its legs raised.",
    36: f"{Z} holding three small cartoon insects at once trapped between different pairs of its long legs, a fly, an ant and a silverfish, while calmly eating a fourth one.",
    37: f"A cartoon scientist with a round white head, dot eyes, glasses and a white lab coat proudly hanging a gold medal with a blue ribbon around the neck of {Z}.",
    38: f"{Z} sparkling clean with small shine stars around it, standing in a tidy bathroom next to a tiny towel on a tiny hook.",
    39: f"{Z} sitting after dinner with a tiny napkin tucked under its chin and a tiny empty plate in front of it, starting to clean itself.",
    40: f"Close-up of {Z} carefully pulling one of its long striped legs through its mouth to clean it, eyes closed in concentration, while the other legs wait in a neat line.",
    41: f"Two small icons crossed out with red circles and slashes on a plain off-white background, a bird nest and a spider web, with {Z} standing between them shrugging.",
    42: f"A kitchen with a wooden table, a loaf of bread, a bowl of fruit and a folded sweater on a chair, all untouched and clean, while {Z} walks past them with its nose in the air, ignoring everything.",
    43: f"{H} looking closely and nervously at {Z} sitting on the back of his hand, a big question mark above his head.",
    44: f"Simple diagram on a plain off-white background: a small green venom droplet with an arrow pointing to a small cartoon fly, and a second arrow pointing to a huge human hand crossed out with a red cross.",
    45: f"Extreme close-up of {Z} trying to nibble a giant human fingertip that looks as big and tough as a wall, with tiny bounce lines showing nothing happens, the centipede looking embarrassed.",
    46: f"A large human hand reaching down to grab {Z} on a floor, the centipede looking up alarmed with all its legs raised.",
    47: f"{H} holding up one finger with a single tiny red dot on it, looking mildly annoyed but fine, with a small adhesive bandage in his other hand.",
    48: f"A small friendly cartoon honey bee hovering next to a human finger with a tiny red dot on it, the bee shrugging apologetically.",
    49: f"{Z} on a bathroom wall noticing {H} in the doorway, its eyes wide and a small exclamation mark above its head.",
    50: f"{Z} diving at full speed into a narrow crack under a bathroom baseboard, only its long rear legs still sticking out, dust puffs behind it.",
    51: f"Simple diagram on a plain off-white background: {ZS} with many small blue water drops evaporating upward from its body, looking thirsty with its tongue out.",
    52: f"A steamy bathroom after a shower with a foggy mirror and water drops on the tiles, and {Z} lounging happily on the edge of the bathtub like at a spa.",
    53: f"The open cabinet under a kitchen sink with pipes, a bucket and one slow drip of water, and {Z} resting comfortably beside the pipe.",
    54: f"{Z} sitting at a tiny dining table with a tiny knife and fork and an empty plate, looking around a room expectantly.",
    55: f"Cutaway view of a kitchen wall and floor showing several small cartoon cockroaches and silverfish hiding inside the wall, while {H} stands in the kitchen above, unaware.",
    56: f"Cutaway view of the inside of a kitchen wall at night with {Z} chasing a group of small cartoon cockroaches that run away in panic.",
    57: f"{H} holding a bug spray can and about to press it, with a big red cross drawn over the spray can.",
    58: f"Three small scenes in one image without panel borders: a dehumidifier machine drying a damp basement, a hand sealing a wall crack with a caulking gun, and an empty clean kitchen floor.",
    59: f"A dry clean bright basement with no bugs and no puddles, and {Z} standing in the middle looking around disappointed, holding an empty tiny plate.",
    60: f"{Z} walking out through a small gap under a door carrying a tiny suitcase and a bindle stick, waving goodbye with several legs.",
    61: f"{H} gently lowering a clear drinking glass over {Z} sitting in a white kitchen sink, with a postcard ready in his other hand, looking calm and kind.",
    62: f"{Z} wearing a tiny party hat next to a tiny birthday cake with seven lit candles, on a basement floor.",
    63: f"A dark quiet house at night seen in cutaway, everyone asleep upstairs in bed, while downstairs {Z} patrols the kitchen floor with a tiny flashlight like a night guard.",
    64: f"{Z} racing across a living room wall at night above a sofa, and {H} on the sofa taking a deep calm breath with his eyes closed, holding a sneaker in his lap, {FULL}.",
    65: f"{H} gently placing a sneaker down on the floor with a small smile, while {Z} on the wall behind him wipes its forehead with relief.",
    66: f"{Z} hurrying along a baseboard at night carrying a tiny briefcase and checking a tiny wristwatch on one leg, looking late and stressed, tiny sweat drops flying off.",
}

beats = json.load(open("beats.json", encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
out = {b["id"]: E + P[k + 1] + C for k, b in enumerate(beats)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts")
