# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat, 96 imágenes) con la FICHA de guion.py. Correr desde la carpeta del video.
Todo imagen (Flow sin puntos de video). Tarjetas con número (beats 9, 22, 36, 50, 63): llevan UN dígito como único texto."""
import json

import guion

F = guion.FICHA
P = F["personajes"]
E = F["estilo"] + ". "
C = " " + F["cierre"]
CN = " The only text in the picture is that single numeral, no letters, no other words, no logos, no watermark."
M, WO, EA, J, D, R, H = (P[k] for k in ("mantis", "wolf", "earwig", "jumper", "dauber", "roach", "human"))
DB = ("a cartoon blue mud dauber wasp with a shiny metallic blue-black body, pale legs, a very thin thread-like waist, two "
      "long thin antennae, a calm friendly face and a tiny orange construction hard hat")
BW = ("a cartoon black widow spider with a glossy round jet-black body, a bright red hourglass mark on its belly, eight "
      "shorter thick black legs, narrow mean eyes and angry eyebrows")
BR = ("a thin tan cartoon brown recluse spider with long thin legs and exactly six small round eyes arranged in three pairs")
CS = ("a cartoon cellar spider with a tiny pale beige peanut-shaped body, a small round head with two big round friendly "
      "eyes, eight extremely long hair-thin pale beige legs with thin dark bands at the knees, and a tiny navy blue night "
      "watchman cap")
WEB = ("a loose, messy, tangled three-dimensional cobweb of random crisscrossing threads with no spiral and no circular "
       "pattern, in the white corner where two walls meet the ceiling")
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every box, crate, jar, can and machine is plain and unlabeled with no writing on it, no speech bubbles"
EDGE = "the drawing runs off all four edges of the image, with no black outline, no frame and no border around it"


def card(n, who):
    return (f"A huge hand-drawn red numeral \"{n}\" with a thick black outline on the left third of the frame, and on the "
            f"right {who}, on a plain light background, {EDGE}.")


N = {}   # beats con tarjeta de número
N[9] = card(5, f"{M} standing tall and proud with its praying hands folded")
N[22] = card(4, f"{WO} looking tough and proud with its legs spread")
N[36] = card(3, f"{EA} showing off its pincers with a goofy grin")
N[50] = card(2, f"{J} sitting on a sunny window sill waving one leg at the viewer")
N[63] = card(1, f"{D} hovering in the air with a mysterious calm look")

V = {
    1: f"A cozy sunlit morning kitchen, {H} in a bathrobe pouring coffee into a mug, and on the window sill behind him a tiny "
       f"dark shape moves with small motion lines, {FULL}.",
    2: f"{H} leaning in close to a window sill with raised eyebrows, and {J} on the sill has turned its whole body to face him, "
       f"the two staring at each other nose to nose, {FULL}.",
    3: f"Extreme close-up of the face of {J}: two enormous shiny round eyes with white highlights and six smaller eyes above "
       f"them, its eight little legs spread around the frame, {EDGE}.",
    4: f"{H}'s hand reaching toward a roll of paper towels on a kitchen counter, then freezing with the other hand raised "
       f"like a stop sign and a startled face, {J} watching from the window sill, {FULL}.",
    5: f"A cutaway of a cozy suburban house with small bugs living like roommates: {M} reading a plain book on the sofa, "
       f"{WO} sweeping the floor with a tiny broom and {J} washing a tiny dish in the kitchen sink, {NOTXT}, {FULL}.",
    6: f"Five friendly cartoon bugs standing proudly in a row on a white kitchen counter, looking at the viewer: {M}, {WO}, "
       f"{EA}, {J} and {D}, {FULL}.",
    7: f"On the left, a lonely {R} standing apart on a kitchen counter with a glowing red circle-and-slash mark over it; on the "
       f"right, {H} asleep in bed with a thought bubble above his head showing a small earwig near a big ear, {FULL}.",
    8: f"{D} flying heroically across a sunny sky dragging a tiny {BW} by one leg, with a proud smile and a determined face "
       f"and motion lines, {FULL}.",
    10: f"Close-up of {M} clinging to a window screen at dusk, looking curiously at the viewer, a soft glow of a lamp inside "
        f"the room behind it, {FULL}.",
    11: f"{M} sitting on a wall under a glowing porch light at night with moths flying around, and its long shadow on the "
        f"wall behind it looks like a tiny alien, {FULL}.",
    12: f"Side view of {M} perched on a green leaf with its front legs folded together in front of its face like praying "
        f"hands and its eyes closed peacefully, {FULL}.",
    13: f"{M} perched on a leaf with one eye open wide, its folded front legs showing sharp little spikes like a trap, while "
        f"a fat cartoon fly buzzes closer in the distance, {FULL}.",
    14: f"The spiked front legs of {M} snapping out and grabbing a surprised fly, with fast speed lines and a small burst of "
        f"dust, next to a giant human eye in the corner of the frame mid-blink, {FULL}.",
    15: f"Underside view of {M} lying on its back, a magnifying glass over one small ear shape in the middle of its body "
        f"glowing with little sound waves, {FULL}.",
    16: f"A night sky with a full moon where a cartoon bat swoops toward {M} flying with spread wings, and {M} tucks its wings "
        f"and dives straight down in a dramatic spiral with a startled face, {FULL}.",
    17: f"{M} sitting at a table with a napkin tucked into its collar and a plate full of flies, moths, mosquitoes and a "
        f"cricket, ready to eat with a happy face, {NOTXT}, {FULL}.",
    18: f"{M} holding a surprised ladybug in its front legs by mistake with an embarrassed shrug, a thin cloud of mosquitoes "
        f"behind it, {FULL}.",
    19: f"{H} gently holding out one finger while {M} climbs calmly onto it, both looking at each other peacefully, a bright "
        f"window with a few snowflakes behind them, {FULL}.",
    20: f"A bare winter garden fence post with a twig, frost and a bit of snow, and on the twig a tan, foamy looking lump the "
        f"size of a walnut, while {H} in a winter coat holds a putty knife near it and hesitates, {FULL}.",
    21: f"Cutaway cross section of the tan foamy lump on the twig, showing hundreds of tiny pale mantis babies curled up "
        f"inside in neat little rows, {FULL}.",
    23: f"A dramatic movie-poster style close-up of {WO} filling the frame, its fuzzy brown body and thick hairy legs lit "
        f"from below like a monster, with a funny proud face, {EDGE}.",
    24: f"A garage floor with a workbench, a bicycle and a car tire, {WO} sprinting toward the viewer with speed lines like it "
        f"owns the place, and {H} peeking from behind a car door in the background, {NOTXT}, {FULL}.",
    25: f"A night scene on bare ground under a big moon with no web anywhere, {WO} walking alone on its eight feet leaving "
        f"little footprints and looking around with big alert eyes, {FULL}.",
    26: f"Extreme close-up of the face of {WO} showing two big round shiny eyes in the middle and six small dot eyes arranged "
        f"around them, with a magnifying glass over them, {EDGE}.",
    27: f"A dark night lawn where {H} crouches holding a flashlight whose beam sweeps across the grass, and many tiny glowing "
        f"sparkle dots shine back from the grass like little jewels, {FULL}.",
    28: f"{WO} chasing a fleeing cricket, a cockroach and a line of ants across a garage floor, comic action with speed "
        f"lines, {FULL}.",
    29: f"{WO} as a mother with a small silky round ball attached to her rear end, and tiny spiderlings just breaking out of "
        f"it like little dots, with a warm gentle look, {FULL}.",
    30: f"{WO} walking calmly through grass with her whole back covered in dozens of tiny baby spiders riding on her like a "
        f"fuzzy backpack, {FULL}.",
    31: f"{H} holding a magnifying glass over two spiders on a garage shelf, puzzled and scratching his head: {WO} and {BR}, "
        f"which look a bit alike, {NOTXT}, {FULL}.",
    32: f"Extreme close-up face of {WO} with eight eyes in three rows (four small ones in the bottom row, two big ones in the "
        f"middle, two medium ones on top), clearly countable, on a plain off-white background, {EDGE}.",
    33: f"Extreme close-up face of {BR} with exactly six small round eyes arranged in three pairs, clearly countable, on a "
        f"plain off-white background, {EDGE}.",
    34: f"A human finger and thumb clumsily pinching one leg of {WO}, which looks annoyed, next to a small drawing of a "
        f"cartoon bee, on a plain garage wall, {FULL}.",
    35: f"An autumn evening at an open garage door with orange leaves blowing in, {H} kneeling and gently sliding a clear cup "
        f"over {WO} with a sheet of paper underneath it, {FULL}.",
    37: f"Close-up of {EA} proudly showing off its two curved pincers with a goofy grin, a sparkle on each pincer, {FULL}.",
    38: f"{H} asleep in bed at night with a big dream cloud above his head showing a cartoon earwig crawling into a giant ear, "
        f"while {EA} stands on the pillow next to him shaking its head and holding up one tiny hand in a clear no, {FULL}.",
    39: f"An old yellowed parchment style drawing of medieval villagers whispering rumors to each other around a big drawing "
        f"of an ear with a small earwig near it, no writing on the parchment, {FULL}.",
    40: f"{EA} lost in a dark bedroom at night, standing on the edge of a pillow near a sleeping person's ear and looking "
        f"small and confused, with a puzzled swirl above its head, {FULL}.",
    41: f"{EA} turning away from a sleeping person's ear with a shrug and walking off along the pillow, with a tiny red X "
        f"mark over a small cluster of eggs, {FULL}.",
    42: f"{EA} wearing a big golden first-place rosette ribbon pinned to its chest, standing proudly with its pincers on its "
        f"hips, with a warm glow, {FULL}.",
    43: f"A cutaway view of a cozy underground burrow in the soil, {EA} as a mother curled protectively around a heap of tiny "
        f"round pale eggs, guarding them with her pincers raised, {FULL}.",
    44: f"Close-up of {EA} gently cleaning one tiny egg with its mouth, with small grey mold spots floating away, a tidy row "
        f"of shiny clean eggs beside it, {FULL}.",
    45: f"{EA} the mother in her burrow with a group of tiny baby earwigs gathered around her, bringing a small green leaf "
        f"piece and a tiny aphid to feed them, everyone smiling, {FULL}.",
    46: f"{EA} munching happily on a plump green aphid on a rose stem, next to a small cluster of tiny round bug eggs, {FULL}.",
    47: f"A garden bed split into two halves: on one side aphids on a stem being eaten by {EA}, on the other side a flower "
        f"with a few nibbled petals, and {EA} in the middle shrugging with open palms, {FULL}.",
    48: f"{EA} wandering alone across a clean kitchen floor with a tiny suitcase, looking around confused, a refrigerator and "
        f"table legs in the background, {FULL}.",
    49: f"{H} gently sweeping {EA} into a dustpan with a small brush and carrying it to an open back door that leads to a "
        f"green garden, {FULL}.",
    51: f"A big family portrait of many different cartoon jumping spiders in many colors and patterns, striped, spotted, "
        f"red, blue and green, all with huge eyes, crowded together in a group photo, {FULL}.",
    52: f"A grid of eight spider shapes in two rows of four, seven of them plain light grey outlines and one in full bright "
        f"color with a golden glow, on a plain off-white background, {EDGE}.",
    53: f"{J} crouching low behind a green leaf stalking a fly with its eyes locked on target and its rear end wiggling like "
        f"a cat about to pounce, {FULL}.",
    54: f"{J} leaping through the air in a graceful arc toward a surprised fly, with motion arcs and a tiny blue cape flying "
        f"behind it, {FULL}.",
    55: f"Extreme close-up of the face of {J} with two huge shiny main eyes and six smaller eyes, with thin sparkling lines "
        f"radiating from the big eyes like a sharp focus beam, {EDGE}.",
    56: f"{J} on a window sill turning its head to look up at a giant human eye looking down from above, a little rainbow of "
        f"colors reflecting in its big eyes, {FULL}.",
    57: f"{J} mid jump off the edge of a leaf with a thin shiny silk thread trailing behind it, attached to the leaf like a "
        f"safety rope, {FULL}.",
    58: f"{J} dangling from its silk thread below a ledge with a sheepish grin, one leg wiping its brow, a leaf above it, {FULL}.",
    59: f"A night scene with a crescent moon: a tiny baby {J} hanging asleep from a single silk thread under a leaf with legs "
        f"curled and eyes closed, and in the corner a cartoon scientist in a white lab coat watching it through a video "
        f"camera on a tripod, {FULL}.",
    60: f"Close-up of a sleeping baby {J} hanging from its thread, its little legs twitching with small motion lines, and a "
        f"dream cloud above it showing a fly floating, {FULL}.",
    61: f"{J} sitting in front of a little buffet of flies, mosquitoes, moths and ants lined up on a leaf, thoughtful with a "
        f"dream cloud above it, {NOTXT}, {FULL}.",
    62: f"{H} holding out his open palm with {J} sitting calmly on his hand, both looking each other in the eye with gentle "
        f"smiles, {FULL}.",
    64: f"{D} flying toward the viewer with its long skinny body and spread transparent wings, looking dangerous at first "
        f"but with a calm friendly smile, {FULL}.",
    65: f"Close-up of the very thin thread-like waist of {D} highlighted with a small magnifying circle, and in the "
        f"background a porch and a garage roof edge, {FULL}.",
    66: f"Under a porch roof edge, several lumpy tubes of dried grey-brown mud stuck side by side on a wall like organ pipes, "
        f"a few plain holes at the ends, {D} nearby, {FULL}.",
    67: f"{H}'s hand reaching up toward the mud tubes holding a plain unlabeled spray can, with a determined face, {NOTXT}, {FULL}.",
    68: f"{D} sitting alone on top of its mud tube with a tiny empty crown next to it marked by a small red X, and no other "
        f"wasps anywhere around, {FULL}.",
    69: f"{D} calmly walking along a wall while {H} sits nearby reading a book and ignoring it completely, both relaxed, {FULL}.",
    70: f"{D} wearing its orange hard hat standing in front of a pantry shelf with many little empty compartments, rubbing its "
        f"front legs together, {NOTXT}, {FULL}.",
    71: f"{D} flying with a small ball of mud in her jaws toward a wall where she shapes a mud tube with her feet, bits of mud "
        f"on her hard hat, {FULL}.",
    72: f"{D} gently stinging a spider that goes limp with spiral eyes, then carrying it into a mud tube with a few more limp "
        f"spiders stacked neatly inside, not scary, {FULL}.",
    73: f"Cutaway of a mud tube with little rooms: each room holds paralyzed spiders with a small white egg resting on the top "
        f"one, and the last room being sealed with a mud cap by {D}, {FULL}.",
    74: f"{DB} flying proudly with a nervous {BW} in the background hiding behind a stack of plain boxes, {NOTXT}, {FULL}.",
    75: f"{DB} carrying a small suitcase into an old mud tube nest and tossing out old items, then dragging a paralyzed {BW} "
        f"inside with a heroic grin, {FULL}.",
    76: f"Cutaway of an old mud tube nest under a porch roof showing neat little rooms full of paralyzed black widows like "
        f"shelves in a storage room, and {H} looking up from below in amazement, {FULL}.",
    77: f"A gray papery umbrella shaped wasp nest hanging from an eave with many angry cartoon paper wasps crawling all over "
        f"it, buzzing, with {H} backing away in alarm, {FULL}.",
    78: f"Split picture with a thick vertical line down the middle: on the left {H} backing away from a wasp nest while talking "
        f"on a phone; on the right {R} alone in a bright spotlight looking guilty and nervous, with a stern red X mark "
        f"glowing on the wall behind it, {FULL}.",
    79: f"The five friendly bugs {M}, {WO}, {EA}, {J} and {D} walking away in a line along the baseboard toward a small open "
        f"door to the garden, leaving the house, with {R} watching from a crack in the wall, {FULL}.",
    80: f"A split picture: on the left {D} flying through an open window, passing through the room; on the right {R} unpacking "
        f"a suitcase, with a tiny armchair, a tiny lamp and a tiny TV in a kitchen cupboard, moving in, {FULL}.",
    81: f"Close-up of {R} lounging in a recliner chair inside an open kitchen cupboard with its feet up and a crumb as a "
        f"snack, the two dark stripes behind its head clearly visible, {FULL}.",
    82: f"A cartoon kitchen sink corner with a dripping faucet and a damp spot, a few crumbs and a dirty plate nearby, and {R} "
        f"peeking out from behind the pipe, {NOTXT}, {FULL}.",
    83: f"{R} as a mother carrying a small light brown egg capsule on her rear end, and next to her a growing crowd of tiny "
        f"cockroaches multiplying row by row from a few to dozens to hundreds, {FULL}.",
    84: f"Tiny floating glowing particles and specks drifting up from a kitchen floor corner into the air, with {R} standing "
        f"in the middle of them, a hazy dusty look, {FULL}.",
    85: f"A cartoon child in pajamas sitting up in bed coughing with a worried face, a tiny cloud of dust specks floating "
        f"above the bed, and a plain nightlight glowing, {FULL}.",
    86: f"Cutaway of a kitchen wall in daytime: one lone {R} on the bright counter, and inside the dark wall behind it, "
        f"hundreds of tiny glowing eyes peeking from the cracks, {FULL}.",
    87: f"A plain unlabeled spray can spraying a cloud in a kitchen while many cockroaches scatter in all directions and run "
        f"through doorways into other rooms of the house, seen as a cutaway floor plan, {NOTXT}, {FULL}.",
    88: f"A tidy kitchen where {H} places a tiny dab of gel bait with a syringe into a corner crack, then wipes the counter "
        f"clean, with a repaired faucet and a freshly sealed gap along the wall, {FULL}.",
    89: f"{H} standing at his front door shaking hands with a friendly pest control worker in a plain cap and uniform with no "
        f"logo, a plain white van with no lettering at the curb, {NOTXT}, {FULL}.",
    90: f"{H} sitting at the kitchen table in the morning sun with a mug of coffee, a little steam fading, looking at the "
        f"window sill with a thoughtful smile, {FULL}.",
    91: f"{J} on the window sill next to a potted plant and a mosquito it has caught, looking back at {H} who sits at the "
        f"table with his coffee, both smiling, soft morning sunlight, {FULL}.",
    92: f"{J} lounging in a tiny hammock between two small potted plants on the window sill, completely relaxed with its legs "
        f"crossed, {FULL}.",
    93: f"A split picture on a kitchen wall: on the left a small bug entering a front door with a suitcase and a moving box, "
        f"and on the right a small bug walking along a window sill toward an open window, with {H} in the middle looking at "
        f"both with a hand on his chin, {FULL}.",
    94: f"{H} carrying a clear cup with a bug inside and a sheet of white paper over its top, walking out the front door "
        f"toward a green garden in morning light, {FULL}.",
    95: f"The white ceiling corner of a living room with {CS} hanging in {WEB}, and below it {BW} wrapped in white silk, {FULL}.",
    96: f"{H} setting a roll of paper towels back on the counter with a smile, and {J} on the sunny window sill waving one "
        f"leg goodbye, {FULL}.",
}

# Ronda 2 (11-oct-2026, rehechas en `medios/_ronda1/`): marco en 11, 6 ojos en 33, una sola tijereta en 37, niño realista en
# 40/41 (usar H), rosetón sin número en 42, sin caras humanas en 65, nido de barro visible en 67
V.update({
    11: f"{M} sitting on a stone wall under a glowing porch light at night with moths flying around, and its long shadow on the "
        f"wall behind it looks like a tiny alien, the drawing runs off all four edges of the image with no black outline, no "
        f"frame and no border around it, no margin.",
    33: f"Extreme close-up face of {BR} on a plain off-white background: exactly six round black eyes arranged as three pairs, "
        f"one pair in the center top, one pair on the left and one pair on the right, six eyes in total and no more, clearly "
        f"countable, {EDGE}.",
    37: f"Close-up portrait of one single {EA} alone, proudly showing off its two big curved pincers with a goofy grin and a "
        f"sparkle on each pincer, only one earwig in the whole picture, {FULL}.",
    40: f"{H} asleep on a pillow in a dark bedroom at night, and {EA} standing on the edge of the pillow near his ear, looking "
        f"small and confused with a puzzled swirl above its head, {FULL}.",
    41: f"{EA} turning away from the ear of the sleeping {H} with a shrug and walking off along the pillow, {FULL}.",
    42: f"{EA} standing proudly with its pincers on its hips, wearing a plain blank gold rosette ribbon with no number and no "
        f"writing on it pinned to its chest, a warm glow, {FULL}.",
    65: f"Side view of {D} flying near a porch roof edge, with a small round magnifying lens highlighting its very thin "
        f"thread-like waist, no people anywhere in the picture, {FULL}.",
    67: f"Outdoors under a porch roof edge, a row of lumpy grey-brown mud tubes stuck to the wall like organ pipes, and {H} "
        f"standing below reaching up toward them holding a plain unlabeled spray can with a determined face, {NOTXT}, {FULL}.",
})

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(V) + len(N), (len(bs), len(V) + len(N))
out = {}
for k, b in enumerate(bs, 1):
    assert b["tipo"] == "imagen", (b["id"], b["tipo"])
    assert (k in N) != (k in V), k
    out[b["id"]] = E + (N[k] + CN if k in N else V[k] + C)
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts ({len(N)} tarjetas con número)")
