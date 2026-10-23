# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video.
Todo imagen (video_s=0): 74 beats de beats.json, escritos desde su texto exacto."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
S = F["personajes"]["spider"]
H = F["personajes"]["human"]
W = F["personajes"]["wolf"]
D = F["personajes"]["diver"]
T = F["objeto"]
SP = ("a cartoon brown house spider with a round tan abdomen with dark chevrons, big round worried eyes, thin banded "
      "legs and a tiny blue and white striped nightcap with a pom-pom")
BATH = "a small tidy bathroom at night with light blue tiles and warm yellow light"
PIPE = "a cutaway view of curving gray plumbing pipes under a house floor, shown like a clean diagram drawing"
SEWER = "a dark cartoon sewer tunnel with round brick walls, a stream of murky green water and dim blue light"
LAB = "a bright tidy French biology lab with glass tanks of water, a window and potted plants"
SCI = "a cartoon scientist with a round white head, dot eyes, glasses and a white lab coat"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every box, bottle, jar and sign is plain and unlabeled with no writing on it"

I = {
    1: f"{H} shuffling sleepily into {BATH}, rubbing one eye, a dark hallway behind him, a clock on the wall with no numbers, {FULL}.",
    2: f"{H} stopping in the bathroom doorway, eyes suddenly wide open, frozen mid-step, looking toward the toilet.",
    3: f"Close-up of {S} sitting on the white rim of the toilet seat, staring straight at the viewer with big eyes, {BATH} behind.",
    4: f"Many cartoon houses at night seen from above, each with a small lit bathroom window and a tiny silhouette of a person pointing at a toilet, playful.",
    5: f"{H} pushing {SP} gently into the toilet bowl with a folded piece of toilet paper, the spider sliding down the white porcelain with flailing legs.",
    6: f"{H} smiling smugly and dusting off his hands next to the toilet with a closed lid, the bathroom calm, little sparkles in the air.",
    7: f"{H} brushing his teeth at the sink, suddenly pausing with the toothbrush in his mouth and glancing at the toilet with a thought bubble showing only a question mark.",
    8: f"{H} sitting on the closed toilet in pajamas looking nervously down between his knees at the toilet, imagining {SP} climbing up from below.",
    9: f"{SCI} standing proudly with a magnifying glass in front of a big friendly drawing of a spider on a wooden easel, like a nature expert on TV, no words.",
    10: f"{SP} floating on its back in dark water with crossed little x eyes, looking dramatic but cartoonish and not gross.",
    11: f"A big cartoon hourglass with sand slowly falling next to {SP} floating calmly in water, a small round clock with no numbers above it.",
    12: f"{SP} relaxing underwater inside a shiny air bubble like an astronaut helmet, giving a thumbs up with one leg.",
    13: f"{SP} wearing a tiny swimming mask and holding its nose with one leg at the edge of a spinning whirlpool in a toilet bowl, ready to dive.",
    14: f"Close-up of {H}'s hand pressing down the silver flush handle on a white toilet tank, water starting to swirl in the bowl below.",
    15: f"{SP} spinning around and around in a swirling toilet whirlpool, legs flailing, water drops flying, seen from above.",
    16: f"{PIPE}: the toilet bowl connected to a U-shaped bend in the pipe filled with blue water, a tiny {SP} riding into the bend.",
    17: f"{PIPE}, the U-shaped bend full of blue water blocking a cartoon puff of green smelly sewer gas from coming up, the gas making a grumpy face.",
    18: f"{SP} sliding down a giant twisting water slide inside a dark pipe like at a water park, mouth open screaming, lit only by a faint glow.",
    19: f"An empty lifeguard chair with a red float hanging on it inside a dark pipe tunnel, {SP} zooming past in the water with motion lines.",
    20: f"{PIPE}: a long pipe running under the wooden floor of a house toward the street, a tiny {SP} shooting along it in a rush of water.",
    21: f"{SP} popping up to the surface of the water in a pipe with a surprised happy face, bobbing like a cork.",
    22: f"Extreme close-up of a spider leg covered in tiny fine hairs, water droplets beading up and rolling off them like on a raincoat.",
    23: f"{SP} floating on dark water wrapped in a thin shimmering silver layer of air around its body like a glowing coat.",
    24: f"{SP} bobbing on the water wearing a tiny orange life jacket, relaxed, little ripples around it.",
    25: f"{SP} floating inside a bubble on the water, breathing calmly with a contented face, small air bubbles around it.",
    26: f"{D} under the clear water of a green European pond among water plants, next to a silvery dome of air held by silk.",
    27: f"Cozy cutaway of {D} inside its silvery underwater air bubble home among pond weeds, like a little diving bell, a few fish swimming past.",
    28: f"{SP} drifting out of a big pipe into a dark sewer tunnel, looking around nervously, {SEWER}.",
    29: f"{SEWER}, cold and gloomy, the current flowing fast, {SP} small on the water surface shivering.",
    30: f"{SP} in tiny pajamas waking up on a floating piece of cardboard in a flooded subway tunnel with old train tracks underwater, blinking in confusion.",
    31: f"{SP} looking up in wonder at a strange underground city of pipes, tunnels and dim lights, feeling lost and very small.",
    32: f"{SP} sitting on a bottle cap boat drifting through {SEWER}, holding a tiny candle, the night feeling long.",
    33: f"{SP} slowly sinking under the murky water, a few last air bubbles rising from it, eyes calm, not scary.",
    34: f"{SP} underwater moving in slow motion, a tiny battery gauge above it barely draining, calm and patient.",
    35: f"A big cartoon snail-shaped clock and {SP} underwater dozing peacefully, showing how slowly time passes.",
    36: f"{SP} rising from the water like a cartoon zombie with arms raised, but with a goofy friendly face, comic and not scary.",
    37: f"{SCI} in {LAB} gently placing several {W} into a clear glass tank of water, curious and careful.",
    38: f"A clear glass tank of water in {LAB}, several {W} resting underwater on the bottom, a scientist watching with a stopwatch with no numbers.",
    39: f"The glass tank in {LAB} at night under a desk lamp, the {W} still underwater, a scientist yawning with a cup of coffee, a window showing the moon.",
    40: f"Close-up of the {W} lying perfectly still underwater in the tank, legs curled, eyes closed, peaceful.",
    41: f"{SCI} looking sadly at the motionless {W} lifted out on a small white paper towel.",
    42: f"Several {W} on paper towels on a lab bench drying under a desk lamp, one of them twitching a leg with small motion lines.",
    43: f"The {W} getting up and walking away across the lab bench in a little line, the scientist dropping a clipboard in amazement.",
    44: f"{SP} curled up underwater in a deep sleep with closed eyes and a tiny dream bubble above it showing a warm cozy bathroom.",
    45: f"A huge dark sewer map with tiny {SP} as a dot far away from a small glowing house in the corner, very far from home.",
    46: f"{H} sitting nervously on the toilet in pajamas, gripping the seat, peeking between his legs at the water with wide eyes.",
    47: f"{SP} at the bottom of a tall pipe looking up at a long climb, shaking its head no, with a calm smile.",
    48: f"{PIPE}: {SP} trying to swim upstream against a strong current toward the water-filled U-bend, getting pushed back.",
    49: f"{SP} slipping down a very shiny smooth white porcelain wall like on ice, legs splayed, comic.",
    50: f"A cartoon natural history museum hall with spider exhibits in glass cases and a spider expert with a round white head, dot eyes and a green sweater shrugging with an open notebook.",
    51: f"A cartoon house cut in half showing all its pipes, with no spiders anywhere inside the pipes, a magnifying glass looking at them.",
    52: f"{H} in the morning finding {SP} sitting at the bottom of a white bathtub next to the drain, both looking surprised.",
    53: f"{SP} climbing down the bathroom wall toward a few shiny drops of water at the bottom of the bathtub, thirsty, tongue out.",
    54: f"{SP} trying again and again to climb the slippery white side of the bathtub and sliding back down, frustrated.",
    55: f"{SP} turning to face the viewer with one raised leg like it is about to share a secret, a soft spotlight on it, {BATH}.",
    56: f"{SP} standing at the edge of a tiny cozy home made in the corner behind the toilet, like a little apartment with a tiny rug.",
    57: f"A cutaway of a cozy house showing {SP} living happily in different quiet corners: behind a bookshelf, in a closet, under the stairs.",
    58: f"{SP} hunting in a corner of a room at night, catching a cartoon fly in its web, satisfied.",
    59: f"{SP} in its corner web next to a small pile of caught gnats and a mosquito, wiping its mouth with a napkin.",
    60: f"{SP} waving hello from its little corner home next to the toilet, with a small welcome mat, friendly and harmless.",
    61: f"A toilet flushing with a huge amount of clean blue water swirling away, the swirl drawn big and dramatic.",
    62: f"A row of clean drinking water jugs with no labels lined up next to a toilet, comparing the size of one flush.",
    63: f"{H} drinking a glass of water at a kitchen table with three days of calendar pages with no numbers torn off beside him, thoughtful.",
    64: f"{H} holding up a clear plastic cup and a sheet of plain white paper like tools, ready and confident, in the bathroom.",
    65: f"{H} placing a cup over {SP} on the floor and carefully sliding a sheet of paper underneath it, gentle and calm.",
    66: f"{H} releasing {SP} from the cup onto a shelf in a tidy garage with garden tools and a broom, {NOTXT}.",
    67: f"{SP} looking shivery and unhappy outdoors in a cold windy open yard with fallen leaves, hugging itself with its legs.",
    68: f"{H} relaxed on the sofa reading a book while {SP} sits in a corner web high on the wall, both calm, a cozy living room at night.",
    69: f"{SP} wearing a tiny security guard cap and holding a tiny flashlight, patrolling a dark kitchen at night, a caught fly beside it.",
    70: f"Back in {BATH} at midnight, {SP} on the toilet rim and {H} in the doorway looking at each other, {FULL}.",
    71: f"{H} pausing with his finger above the flush handle, a thought bubble showing the dark curving pipes and the sewer below.",
    72: f"{SP} riding a dark winding water slide into the night, small and brave, stars painted on the tunnel ceiling.",
    73: f"{H} smiling and holding a clear cup and a sheet of white paper in the bathroom while {SP} waves at him from the toilet rim.",
    74: f"{H} gently carrying the cup with {SP} inside out of the bathroom, the spider waving goodbye, warm yellow light, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(I), (len(bs), len(I))
out = {}
for k, b in enumerate(bs, 1):
    assert b["tipo"] != "video", b["id"]
    out[b["id"]] = E + I[k] + C
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts")
