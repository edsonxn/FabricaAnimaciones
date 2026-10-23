# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video. Todo imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
S = F["personajes"]["spider"]
H = F["personajes"]["human"]
WEB = F["objeto"]
SS = ("a cartoon gray-brown porch spider with a plump round abdomen, eight banded legs, big round expressive eyes "
      "and a tiny yellow construction hard hat")
PORCH = "an American front porch at night with a wooden railing, a doormat, a porch post and a glowing porch light with moths"
DAY = "the same American front porch in soft morning light, a wooden railing, a doormat and a porch post"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every box, bulb, chart and sign is plain and unlabeled with no writing on it"

I = {
    1: f"{PORCH}, {H} stepping out of the front door at night, {FULL}.",
    2: f"{H} walking face first into a spider web, silk threads stretched across his face, arms flailing, comic.",
    3: f"{H} spitting and swiping at his face, then grabbing a broom by the door, determined.",
    4: f"{H} sweeping the broom through {WEB}, threads snapping and flying between the post and the porch light.",
    5: f"{SS} dropping straight down out of sight on a thin silk thread, a little worried, into the dark.",
    6: f"{DAY}, {H} opening the front door in a bathrobe with a coffee mug, and {WEB} back in place, {FULL}.",
    7: f"Close-up of a perfect new round orb web glistening with dew in the morning sun, {SS} sitting in the center proudly.",
    8: f"{H} staring at the new web with his jaw dropped, coffee spilling a little, a big question mark.",
    9: f"{SS} working in the dark under the porch light, spinning silk at high speed with motion lines, a tiny moon above.",
    10: f"{H} asleep in bed snoring under a blanket while through the window the spider works on the porch at night.",
    11: f"{SS} standing in front of the ruins of a broken web, hands on hips, looking at the damage.",
    12: f"A cartoon diagram-like drawing of {WEB} shown as a little house, a fridge and a fishing net at once, {NOTXT}.",
    13: f"A moth caught in the sticky spiral of an orb web, {SS} grinning and tying a tiny napkin around its neck.",
    14: f"{SS} with one leg resting on a web thread, little vibration waves rippling along the silk toward it.",
    15: f"Glowing ripples on the threads of a web pointing to a tiny fly stuck in one corner, the spider's eyes turning toward it.",
    16: f"A broom sweeping through a web, the home, the fridge and the net flying apart as three little cartoon icons, {NOTXT}.",
    17: f"{SS} standing in an empty spot between the post and the light with tiny broken threads around it, stunned.",
    18: f"{SS} hanging safely from a thin silk line, giving a relieved sigh and a small thumbs up.",
    19: f"{SS} walking along a porch railing with a thin silk line trailing behind it like a rope.",
    20: f"{SS} as a tiny mountain climber with a helmet and a silk rope anchored to a rock, rappelling, playful.",
    21: f"{SS} letting go and dropping quickly on its silk line as the broom swooshes above it, motion lines.",
    22: f"{SS} paying out silk as it falls, then tucking itself into a small crack in a wooden porch post.",
    23: f"{SS} peeking out of a crack in the porch post, watching the front door close and the light inside turn on.",
    24: f"{PORCH} late at night, quiet, {SS} climbing back out of the crack under the moths and the porch light.",
    25: f"Several cartoon orb weaver spiders in tiny hard hats building webs on porches along a street at night.",
    26: f"{SS} building the first spokes of a new web like a construction worker, a tiny tape measure, focused.",
    27: f"A very long silk thread stretched along the porch floor from the post all the way down the steps and across the lawn.",
    28: f"{SS} looking at a tiny glowing silk spool like a precious treasure, a little coin purse beside it.",
    29: f"{SS} rolling up an old broken web into a ball like spaghetti and eating it with a fork, satisfied.",
    30: f"A cartoon scientist with a round white head in a lab coat feeding a spider a tiny glowing green silk thread, {NOTXT}.",
    31: f"The scientist watching glowing green dots travel through a spider's body on a simple screen, curious, {NOTXT}.",
    32: f"A spider with glowing green silk inside its belly, now spinning a new web with faint glowing green threads.",
    33: f"{DAY} with a perfect new web, a few threads gently glowing green to show recycled silk.",
    34: f"{H} looking at the web with a raised eyebrow, the broom leaning against the wall next to him.",
    35: f"{SS} looking tired with droopy eyes, holding a tiny empty silk spool upside down.",
    36: f"A cartoon field researcher with a clipboard watching orb weaver spiders on a meadow fence, {NOTXT}.",
    37: f"{SS} carrying a tiny suitcase away from a ruined web toward a new bush, glancing back.",
    38: f"{SS} with an empty plate and a growling tummy next to an empty web, deciding to leave.",
    39: f"{SS} hitchhiking with one leg raised on a twig by the road toward a far-away garden.",
    40: f"A porch map seen from above with a broom icon on one side and the spider walking off toward the other side, {NOTXT}.",
    41: f"{H} sweeping the same corner day after day, a stack of calendar pages flying, {NOTXT}.",
    42: f"{SS} waving goodbye from the porch railing with a tiny bindle on a stick, heading out.",
    43: f"{SS} settling into a hidden spot behind a garden shed where no one can see it, happy and relaxed.",
    44: f"The corner of a living room ceiling with dusty gray tangled old cobwebs, {H} looking up with a frown.",
    45: f"{SS} leaning in to whisper a secret, one leg beside its mouth, eyes wide.",
    46: f"An old dusty cobweb in a ceiling corner with a tiny empty mailbox and nobody home, abandoned.",
    47: f"{SS} walking away from an old web as dust bunnies move in and settle on the threads.",
    48: f"{H} happily sweeping dusty cobwebs from the ceiling corner with a broom, dust puffs everywhere.",
    49: f"{DAY}, a web stretched across the front door frame, {H} stopping in the doorway thinking.",
    50: f"{H} winding the web gently around a stick like cotton candy, the spider sitting on the end.",
    51: f"{H} carrying the stick with {SS} riding on it to a green bush beside the porch, the spider waving.",
    52: f"{SS} building a new web in the bush at dusk, and {H} giving it a nod from the porch.",
    53: f"{SS} sitting under a bright white porch light while lots of moths swirl around it, licking its lips.",
    54: f"{H} on a step stool swapping a white bulb for a warm yellow bug light bulb, {NOTXT}.",
    55: f"{PORCH} lit by a warm yellow bulb with only a couple of moths, the spider in the bush nearby, everyone calm, {FULL}.",
    56: f"{H} walking out the door at night and stopping just before a web, smiling this time.",
    57: f"{SS} face to face with {H}, both a little surprised, a friendly moment.",
    58: f"{SS} standing proudly in front of its home, a tiny fridge and a fishing net, hard hat on, smiling.",
    59: f"{SS} finishing a perfect web as the sunrise begins, a cup of coffee in one leg, before breakfast.",
    60: f"{DAY}, the finished web glowing in the sunrise, {SS} winking, {H} smiling at the door, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {b["id"]: E + I[k] + C for k, b in enumerate(bs, 1)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
