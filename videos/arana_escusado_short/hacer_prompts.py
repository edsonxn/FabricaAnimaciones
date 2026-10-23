# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat, 9:16) con la FICHA de guion.py. Correr desde la carpeta del video."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
S = F["personajes"]["spider"]
H = F["personajes"]["human"]
SP = ("a cartoon brown house spider with a round tan abdomen with dark chevrons, big round worried eyes, thin banded "
      "legs and a tiny blue and white striped nightcap with a pom-pom")
BATH = "a small tidy bathroom at night with light blue tiles and warm yellow light"
PIPE = "a tall vertical cutaway of curving gray plumbing pipes going down under a house floor, like a clean diagram drawing"
SEWER = "a dark cartoon sewer tunnel with round brick walls, murky green water and dim blue light"
LAB = "a bright tidy biology lab with a glass tank of water"

I = {
    1: f"Seen from above, {H}'s hand pressing the silver flush handle while {S} spins in the swirling water of the toilet bowl below, big and close.",
    2: f"An empty white toilet bowl with the last swirl of water draining away, a single tiny striped nightcap floating on the surface, {BATH}.",
    3: f"{H} staring down into the toilet bowl with a big question mark floating above his head, {BATH}.",
    4: f"Looking up from inside the toilet bowl: {SP} peeking over the white porcelain rim, climbing out toward the viewer, comic suspense.",
    5: f"{PIPE}: the U-shaped bend full of blue water, a tiny {SP} shooting through it.",
    6: f"{SP} screaming happily while sliding down a giant dark twisting water slide tunnel, splashing water, stars painted on the tunnel walls.",
    7: f"Extreme close-up of a spider leg covered in tiny fine hairs with water droplets beading up and rolling off.",
    8: f"{SP} wrapped in a shimmering silver bubble of air, floating in dark water, eyes wide with wonder.",
    9: f"{SP} floating on the water surface like a little cork, relaxed, lying on its back with legs crossed, in {SEWER}.",
    10: f"{SP} slowly drifting down under murky green water, calm, a few air bubbles rising above it.",
    11: f"{LAB}: several cartoon gray marsh wolf spiders resting on the bottom of the tank, a scientist with a round white head, glasses and a lab coat watching with a stopwatch with no numbers.",
    12: f"Close-up of a cartoon gray marsh wolf spider lying perfectly still underwater with its eyes closed, peaceful.",
    13: f"A cartoon gray marsh wolf spider on a white paper towel under a desk lamp, suddenly twitching one leg with small motion lines.",
    14: f"Several cartoon gray marsh wolf spiders walking away across a lab bench in a little line while a scientist drops a clipboard in amazement.",
    15: f"{SP} at the bottom of a very tall pipe looking up at the long climb, shaking its head no with a calm smile.",
    16: f"{PIPE}: the U-shaped bend full of blue water acting like a door, {SP} pushed back by the water, a big friendly blue wall.",
    17: f"{H} holding a clear plastic cup and a sheet of plain white paper, smiling, while {S} waves at him from the toilet rim, {BATH}.",
    18: f"{H} gently carrying a clear cup with {SP} inside out of the bathroom, the spider waving goodbye, warm yellow light.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
