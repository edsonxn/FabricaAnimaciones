# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
M = F["personajes"]["male"]
FE = F["personajes"]["female"]
H = F["personajes"]["human"]
WEB = F["objeto"]
SP = "a small cartoon house spider with a round brown fuzzy body, eight thin legs and two big round expressive eyes"
OUT = "a cartoon garden spider with a round orange and yellow striped body, eight thin legs and two big round expressive eyes"

P = {
    1: f"A cozy suburban house seen from the street on an autumn evening, orange and red trees, falling leaves, warm light in the windows, a carved pumpkin on the porch.",
    2: f"Inside a living room at night, {M} sprinting fast across a wooden floor with speed lines behind him, while {H} sitting on a sofa lifts both feet in alarm, the room filling the whole image to every edge with no white margin and no panel outline.",
    3: f"A white bathtub seen from above with {SP} sitting alone at the bottom, and {H} peeking over the edge of the tub with a shocked face.",
    4: f"A cold windy autumn night outside a wooden house, a line of several small cartoon spiders wearing tiny scarves marching toward the front door carrying tiny suitcases, as people imagine it.",
    5: f"The same line of small cartoon spiders with tiny scarves and suitcases at the front door of a house, with a big bold red cross drawn over the whole scene to show the idea is wrong.",
    6: f"Cutaway view of a wooden suburban house like a dollhouse, showing every room, with small cartoon house spiders already living quietly in corners of the attic, the living room, the bathroom and the basement.",
    7: f"{H} sitting comfortably on a sofa reading a book, completely unaware of {SP} resting in a web in the ceiling corner right above him.",
    8: f"A chilly autumn night in a backyard with a full moon and bare trees, {SP} shivering on a leaf and looking toward the warm glowing window of a house, as people imagine it.",
    9: f"{H} standing in a living room scratching his head with a doubtful face, next to a simple drawing board showing a spider walking toward a house with a big question mark above it.",
    10: f"{SP} sitting calmly right next to a glowing warm fireplace and completely ignoring it, looking bored, with a tiny shrug.",
    11: f"Simple diagram on a plain off-white background: {SP} seen from the side next to a large cartoon thermometer colored blue, with small snowflakes around.",
    12: f"A cold outdoor scene with frost on the grass: {SP} standing calmly without shivering, and next to it a small electric heater crossed out with a red circle and slash.",
    13: f"Three small panels in one image showing the same small brown cartoon spider on a twig: walking normally, then walking very slowly, then barely moving, with the background getting colder and bluer in each panel.",
    14: f"{SP} sitting completely still and frozen in place on a frosty branch, eyes half closed, a few snowflakes falling, calm and peaceful.",
    15: f"Cutaway view of a tree trunk in winter with snow outside, and under a piece of loose bark {OUT} tucked in and sleeping peacefully.",
    16: f"A pile of dead brown leaves on snowy ground cut open to show {OUT} curled up underneath, smiling in its sleep, snow falling above.",
    17: f"{OUT} standing confused in the middle of a warm tidy living room, drawn wearing a tiny astronaut helmet as if it had landed on a strange planet, with a sofa and a lamp behind it.",
    18: f"Close view of a dark ceiling corner inside a house with {SP} peeking out shyly from {WEB}, and a magnifying glass held by {H} pointing at it.",
    19: f"Split scene: on the left a sunny garden with {OUT} on a big round web between flowers, on the right a dim house interior with {SP} in {WEB}; the two spiders look clearly different.",
    20: f"{SP} proudly wearing a tiny graduation cap and holding a tiny diploma, standing on a bookshelf inside a house.",
    21: f"Simple diagram on a plain off-white background: {SP} in the center with three small icons around it, a thermometer showing a steady middle temperature, a single tiny crumb on a plate, and one single small water drop.",
    22: f"Inside an ancient Roman house with stone columns, clay jars and an oil lamp, {SP} sitting in a web in the corner while a cartoon Roman person in a white toga walks past.",
    23: f"A side by side scene: on the left an ancient Roman room with columns and a small brown cartoon spider in the corner, on the right a modern living room with a television and the very same kind of spider in the same corner.",
    24: f"A cardboard moving box and a wooden chair being carried into a house by {H}, and hidden under the chair seat a small round white silk egg sac drawn with a tiny dotted circle around it.",
    25: f"Cutaway view of the inside of a house wall between two rooms, with dozens of tiny baby cartoon spiders hatching from a white silk ball and spreading out along the wooden beams.",
    26: f"A row of one hundred tiny identical small brown cartoon spiders arranged in a neat grid on a plain off-white background, ninety five of them colored brown and only five colored bright green.",
    27: f"{H} standing in a living room next to an open window and pointing at five small bright green cartoon spiders sitting in a row on the windowsill, while a dozen small brown cartoon spiders sit calmly on the far wall and on a bookshelf, away from the window, the room filling the whole image to every edge with no white margin and no panel outline.",
    28: f"{SP} standing at an open front door and looking out nervously at a big scary outdoors with wind and rain, refusing to step outside.",
    29: f"{H} standing in the middle of a tidy living room looking around with a hand over his eyes like searching, with no spiders visible anywhere, and a wall calendar showing a sun for summer.",
    30: f"{SP} hiding behind a row of colorful books with completely plain blank spines and no writing on them, on a shelf, with only its two big eyes and two legs visible, holding one leg up to its mouth in a hush gesture.",
    31: f"Three hiding places shown together inside a house: {WEB} behind a wooden shelf, another one under a staircase, and a small brown cartoon spider sitting in each.",
    32: f"A dark basement with a water heater, stored boxes and a small window, and {SP} sitting perfectly still in {WEB} near the ceiling.",
    33: f"{SP} sitting in the exact same spot in its web while a wall calendar next to it has many pages flying off to show months passing, cobwebs growing on a nearby clock.",
    34: f"{H} walking down a hallway carrying a laundry basket, passing right under {SP} sitting in a ceiling corner web, the spider giving a tiny friendly wave that he does not notice.",
    35: f"A comic sequence in one image: {H} walking past the same ceiling corner four times in different clothes, a small brown cartoon spider always in the same spot above him, unnoticed.",
    36: f"A window showing late summer outside with golden light and the first yellow leaves, and inside on the windowsill {SP} looking up as if sensing something new.",
    37: f"A small young brown cartoon spider on the left transforming into {M} on the right, shown with a sparkle and an arrow between them, the adult standing taller and proud.",
    38: f"{M} with big heart-shaped eyes and small red hearts floating above his head, standing on a floorboard.",
    39: f"{M} walking away from an old empty web in a corner, waving goodbye to it, and ignoring a house fly that buzzes right past him.",
    40: f"{M} marching with determination up a living room wall, tiny dotted footprints behind him tracing a long wandering path across the floor and up the wall.",
    41: f"{M} standing on top of a table lamp like a lookout, shading his eyes with one leg and scanning the room.",
    42: f"A dark living room at night lit by a television, {M} running across the carpet in the glow, and {H} on the sofa pulling a blanket up to his eyes.",
    43: f"{M} standing in the middle of a hallway looking lost and holding a tiny map upside down in one leg and a tiny bouquet of flowers in another.",
    44: f"{FE} tucked away behind a bookshelf, calmly waiting and looking unimpressed.",
    45: f"Front view of a house in early autumn with a big red cross drawn over a cartoon army of tiny spiders charging at the door, showing that no invasion is happening.",
    46: f"Cutaway dollhouse view of a house interior at night with four of {M} each coming out of a different hiding corner at the same time, all starting to walk.",
    47: f"{M} finally arriving at the web of {FE}, offering her a tiny bouquet of flowers, both smiling shyly.",
    48: f"A single empty tiny red bow tie lying on a wooden floor in a quiet corner of a house, a few autumn leaves visible through a window, calm and a little sad.",
    49: f"{M} sitting alone at the bottom of a large white bathtub and looking up, with the bathtub drain visible nearby and {H} staring down from above.",
    50: f"Cutaway diagram of a bathtub drain pipe under the tub showing the curved pipe section filled with blue water, and a small brown cartoon spider at the bottom of the pipe stopped by the water, with a red cross.",
    51: f"{M} walking along the rim of a white bathtub with his tongue out, looking thirsty and tired, a single water drop glistening at the bottom of the tub.",
    52: f"{M} carefully climbing down the smooth white inside wall of a bathtub toward a small puddle of water near the drain, drinking happily.",
    53: f"{M} trying to climb up the smooth white wall of a bathtub and sliding back down, small slip lines drawn behind his legs, looking frustrated.",
    54: f"{M} sitting at the bottom of a white bathtub with a tired sigh, his legs folded, a tiny thought of an escape ladder imagined above him.",
    55: f"{H} gently holding a clear drinking glass upside down over {M} on a floor, with a postcard in his other hand, looking kind and careful, the front door open to a garden behind him.",
    56: f"{H} standing at an open back door holding a glass with a small brown cartoon spider inside, pausing with a thoughtful face, a cold rainy autumn garden outside.",
    57: f"{M} standing alone on wet grass in a big cold rainy autumn garden at dusk, looking tiny and scared, the warm lit house far behind him.",
    58: f"A cold rainy garden at night where {M} looks up nervously at a big cartoon bird on a branch and a large cartoon garden spider on a web watching him.",
    59: f"A small sad scene on frosty garden grass at dawn: a tiny red bow tie left on a frozen leaf, the house in the background, quiet and still.",
    60: f"{SP} in {WEB} in a kitchen corner wearing a tiny tool belt like a worker, giving a confident thumbs up with one leg.",
    61: f"{SP} in a web that has caught a cartoon house fly, a cartoon mosquito and a small cartoon moth, all wrapped neatly in silk.",
    62: f"{SP} sitting proudly in a tidy web in a kitchen corner next to a small hanging sign shaped like a blank badge, with several silk-wrapped insect bundles lined up like finished work.",
    63: f"{SP} politely refusing a tiny coin offered by {H}, shaking its head with a friendly smile.",
    64: f"{H} and {SP} at opposite ends of a long sofa, the spider keeping its distance and looking the other way, both calm and relaxed.",
    65: f"A living room in autumn with orange leaves outside the window, {M} walking across the wooden floor while {H} watches from the sofa, this time calm and curious instead of scared.",
    66: f"Close portrait of {M} looking friendly and a little shy, standing on a wooden floor with warm lamp light behind him.",
    67: f"Cutaway view of a house wall showing a tiny cozy spider apartment inside it with a little bed, a lamp and framed pictures, and {M} standing at its tiny door with a small suitcase.",
    68: f"{M} stepping out of a small dark gap under a baseboard into a big bright living room, looking nervous and wiping sweat from his forehead with one leg.",
    69: f"{H} relaxed on a sofa with a cup of tea and a small smile, while across the room {M} hurries along the wall looking stressed with tiny sweat drops flying off him.",
}

beats = json.load(open("beats.json", encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
out = {b["id"]: E + P[k + 1] + C for k, b in enumerate(beats)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts")
