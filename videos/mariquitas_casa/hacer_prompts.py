# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video. Todo imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
B = F["personajes"]["beetle"]
N = F["personajes"]["native"]
H = F["personajes"]["human"]
HOUSE = F["objeto"]
BS = ("a cartoon orange Asian lady beetle with black spots, a white head with a small black M mark, big round eyes and a "
      "tiny red and white knitted scarf")
MANY = "dozens of small cartoon orange lady beetles with tiny red and white scarves"
FALL = "an American countryside yard in autumn with orange and yellow trees and late afternoon sun"
WIN = "a cozy American home interior in winter with snow outside the window"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every box, jar, sign and calendar is plain with no writing on it"

I = {
    1: f"{FALL}, {HOUSE} glowing in warm sunlight, a peaceful October afternoon, {FULL}.",
    2: f"{H} stepping out of the back door and freezing in surprise, staring at the side of {HOUSE} which is covered with tiny moving orange dots.",
    3: f"Close view of white wooden house siding covered with {MANY} crawling in every direction.",
    4: f"{MANY} buzzing around a white window frame in the afternoon sun, small motion lines around them.",
    5: f"{WIN}: {BS} walking upside down across a white living room ceiling, {H} looking up at it from the sofa.",
    6: f"Three tiny cartoon orange lady beetles with scarves sitting on a kitchen window above the sink, looking out at snow.",
    7: f"Cutaway of {HOUSE} showing the hollow spaces inside the walls and the attic, with question marks floating in them.",
    8: f"{HOUSE} with a giant cartoon target painted around it by tiny lady beetles flying toward it, playful.",
    9: f"{BS} peeking out from behind a classic red ladybug costume mask it just took off, sly and funny.",
    10: f"Extreme close-up of the white head of {BS}, showing clearly its black M-shaped mark, a big magnifying glass in front.",
    11: f"A magnifying glass showing the white head of a lady beetle with a bold black M-shaped mark, {H} squinting through it.",
    12: f"{BS} and {N} standing side by side like cousins at a family reunion, smiling.",
    13: f"A simple cartoon map of East Asia with China, Korea and Japan in soft colors, tiny lady beetles waving from it, no labels.",
    14: f"A row of five cartoon Asian lady beetles with tiny scarves, their shells tan, orange, red, some with many spots and some with none.",
    15: f"{BS} with a completely spotless plain orange shell looking at its reflection in a puddle in surprise.",
    16: f"An old-fashioned 1980s cartoon government scientist in a lab coat and glasses releasing a cloud of lady beetles from a jar over a crop field, {NOTXT}.",
    17: f"{MANY} landing on crop plants and happily eating tiny green aphids, a sunny farm field.",
    18: f"A cartoon Louisiana bayou with cypress trees and Spanish moss, a few lady beetles sitting on a branch, no labels.",
    19: f"A retro 1980s scene: a tiny boombox and roller skates next to a group of lady beetles on a Louisiana porch at sunset.",
    20: f"A simple cartoon map of the United States covered with tiny orange lady beetle dots from coast to coast, no labels.",
    21: f"{BS} standing with a little suitcase, pointing at {HOUSE}, considering it.",
    22: f"Sunny rocky cliffs in the Asian mountains with many lady beetles tucked into cracks in the rock, cozy and warm.",
    23: f"Side by side: a pale sunny cliff with cracks and {HOUSE} with light siding, the lady beetle comparing them with a squint.",
    24: f"{HOUSE} with its sunny side glowing in late afternoon sunlight, a big arrow of lady beetles flying toward that sunny wall.",
    25: f"Close view of light house siding next to a dark green shutter, lady beetles gathering exactly where light meets dark.",
    26: f"{HOUSE} at the edge of woods and a harvested field, swarms of lady beetles rising from the field toward it.",
    27: f"A faint glowing scent trail drawn as wavy lines on the house wall, leading new lady beetles to a corner of the window frame.",
    28: f"New lady beetles sniffing the wavy scent lines left on a window frame and following them, like following footprints.",
    29: f"{MANY} wearing tiny sunglasses and sun hats arriving with little suitcases, like retired snowbirds on vacation.",
    30: f"A cozy cutaway of the attic of {HOUSE} decorated like a little winter condo for lady beetles, tiny beds and a tiny rug.",
    31: f"{BS} squeezing easily through a thin gap at the edge of a window frame, smiling.",
    32: f"Close-up of a thin crack around a window frame next to a pencil tip for comparison, lady beetles slipping through the crack.",
    33: f"Lady beetles crawling under the edge of house siding and through a roof vent, one after another.",
    34: f"Cutaway of a house wall and attic: lady beetles crawling deep into the dark hollow spaces between the wall boards.",
    35: f"A big tight cluster of {MANY} packed together in a corner of the attic, like a huddle.",
    36: f"The cluster of lady beetles asleep with closed eyes and a few tiny round sleep bubbles, dim cozy attic light.",
    37: f"Sleeping lady beetles ignoring a crumb of food and a piece of wood next to them, totally still.",
    38: f"A wall calendar with blank pages flipping by in the attic while the sleeping lady beetles do not move, {NOTXT}.",
    39: f"{WIN}: a warm living room with a glowing radiator and fireplace, cozy and toasty.",
    40: f"Winter sun shining through a window onto a wall while heat waves rise from a radiator below.",
    41: f"{BS} waking up in the dark wall space, stretching and yawning, a little sun symbol shining in its imagination.",
    42: f"Lady beetles crawling out of a baseboard gap and from around a ceiling light fixture into a living room.",
    43: f"{MANY} gathered on the inside of a frosty window, looking out at the snow longingly.",
    44: f"{BS} sitting alone on a windowsill next to an empty tiny plate, looking hungry.",
    45: f"{BS} looking tired and thirsty under dry warm air from a radiator, a tiny empty water glass beside it.",
    46: f"A quiet windowsill in winter with a few lady beetles resting still with closed eyes, gentle and soft, not gross.",
    47: f"{H} reaching toward a lady beetle on the window, then pausing with a raised finger as if hearing a warning.",
    48: f"A human finger gently squeezing {BS}, the beetle looking alarmed.",
    49: f"{BS} with a few tiny yellow drops coming from its leg joints, and wavy green smell lines around it, comic.",
    50: f"A cartoon bird tasting a lady beetle and making a disgusted face, sticking out its tongue.",
    51: f"A white lace curtain with small yellow stains on it, {H} holding it up with a frown.",
    52: f"{BS} giving a tiny nip on the finger of {H}, who flinches slightly.",
    53: f"{H} looking at her finger with a tiny pink dot, shrugging with a calm face.",
    54: f"Lady beetles waiting patiently on a windowsill as the snow outside starts to melt, early spring light.",
    55: f"{MANY} gathered at a window in spring sunshine, pressing against the glass to get out.",
    56: f"{H} opening a window in spring while lady beetles fly out happily into the garden.",
    57: f"Lady beetles flying back to green trees and fields in spring, landing on leaves full of tiny green aphids.",
    58: f"Close-up of a plant stem covered with tiny green aphids sucking on it, the leaf drooping, a lady beetle arriving.",
    59: f"A cartoon farmer with a round white head and a straw hat giving a thumbs up to lady beetles on his crops.",
    60: f"{BS} with a tiny trophy standing on a healthy green leaf, proud.",
    61: f"{H} standing at a window full of lady beetles holding a vacuum cleaner, thinking.",
    62: f"A broom and a squishing hand crossed out with a big red X next to a yellow stain on a wall.",
    63: f"{H} gently vacuuming lady beetles from a window frame with a hose attachment.",
    64: f"Close-up of a handkerchief tucked between a vacuum hose and its bag, then {H} shaking the handkerchief outside to free the lady beetles.",
    65: f"{FALL} in summer instead, green trees, {H} on a ladder with a caulk gun near a window.",
    66: f"{H} sealing gaps around a window frame and a vent with a caulk gun, lady beetles outside watching in dismay.",
    67: f"{HOUSE} in autumn with all its gaps sealed, lady beetles bouncing off the walls and flying back to the woods.",
    68: f"{WIN}: {BS} walking across the ceiling while {H} watches it from her armchair with a gentle smile, {FULL}.",
    69: f"{BS} looking down from the ceiling with innocent eyes, a tiny suitcase beside it.",
    70: f"{BS} in tiny sunglasses and a scarf looking out a frosty window, waiting for spring like a snowbird.",
    71: f"{H} opening a window in spring and holding out her finger with {BS} on it, ready to fly.",
    72: f"{BS} flying happily out into a sunny spring garden full of plants, waving goodbye, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
