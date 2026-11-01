# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat, 111) con la FICHA de guion.py. Correr desde la carpeta del video.
Beats de VIDEO 1-7: dos escenas por clip (combinar=True), 10 s cada uno ("first five seconds"). Resto: IMAGEN.
Reglas: sin cifras ni rótulos (pictogramas con siluetas llenas y siluetas pálidas punteadas); Sapi es el «tú» del espectador."""
import json

import guion

F = guion.FICHA
P = F["personajes"]
E = F["estilo"] + ". "
C = " " + F["cierre"]
S, NE, NI = P["sapi"], P["neandertal"], P["nino"]
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
EDGE = "the drawing runs off all four edges of the image, with no black outline, no frame and no border around it"
NOTXT = "every box, jar and bag is plain and unlabeled with no writing on it, no speech bubbles"
ARQ = "a cartoon archaeologist with a wide tan hat, round glasses, a khaki vest and a soft brush"
RAK = ("a cartoon orangutan with shaggy orange-red fur, a big round face with wide cheek pads, and a small red cut on one "
       "cheek just below the eye")
HOM = ("a cartoon Copper Age mountain man in a brown fur cap, a grass cape, a patched leather coat and leggings, with small "
       "dark tattoo lines on both knees")
ANDE = ("an ancient Andean healer in a colorful woven poncho and a headband with one feather, holding a small sharp "
        "obsidian blade")
DOC = "a friendly cartoon doctor with a white coat, round glasses and a stethoscope"
GHOST = "ten small round-headed figures standing in a row on a plain light background"


def clip(a, trans, b, n="five"):
    return f"Scene one, first {n} seconds: {a} Then {trans}. Scene two, last {n} seconds: {b}"


V = {
    1: clip(f"{S} sitting on a couch holding his swollen cheek with a pained face, a bandage on his knee and a thermometer "
            "in his mouth.",
            "a splash of black ink spreads across the frame and washes away to reveal scene two",
            f"{S} walking out of a bright pharmacy with a smile, holding up one small white-and-pink capsule pill, the "
            "pharmacy has only a plain green cross symbol and no writing."),
    2: clip(f"{S} standing alone on a snowy Ice Age hill holding his cheek, with a woolly mammoth in the far distance and "
            "an empty horizon with no buildings.",
            "the scene peels away like a turning sketchbook page, revealing scene two drawn underneath",
            f"close-up of {S} squinting at his own knee wound while a crowd of tiny cute green germs throws a party on it "
            "behind his back, unnoticed."),
    3: clip(f"{S} sitting with a group of Stone Age people around a campfire at dusk, while a stern elder points a stick at "
            "a skull drawn on the cave wall with a row of tally marks beside it.",
            "the ink lines of the scene come loose, swirl like ribbons and redraw themselves into scene two",
            f"{S} looking straight at the viewer with one raised eyebrow and crossed arms, one big question mark floating "
            "above his head, the question mark is the only symbol in the picture."),
    4: clip(f"{S} proudly pointing a thumb at his own chest with a big grin, standing on a sunny hill.",
            "the camera pulls back and his silhouette becomes the last one in a long line of silhouettes",
            f"a very long line of Stone Age ancestor silhouettes holding hands, stretching from the foreground over the "
            f"hills to the far horizon, from ape-like ones to people like {S}, golden light."),
    5: clip(f"{S} with an arm in a splint made of sticks and a leaf bandage on his knee, shrugging, next to a pill capsule "
            "inside a red circle with a diagonal slash.",
            "a giant eraser rubs out the scene and a pencil quickly sketches scene two in its place",
            f"inside a cave, {S} pointing with a stick at four glowing cave paintings in a row on the wall: a tooth, a "
            "skull, a leg bone and a green plant."),
    6: clip(f"two archaeologists in hats kneeling in a cave dig pit and gently brushing the leg bones of an ancient skeleton "
            "by torchlight.",
            "a splash of black ink spreads across the frame and washes away to reveal scene two",
            f"{S} swinging a big wooden mallet and smashing a cracked stone slab with a row of thirty tally marks carved "
            "on it, stone chips flying."),
    7: clip("a smiling old Stone Age woman with white hair and a walking stick surrounded by laughing kids on a grassy hill.",
            "the camera pushes into the round hole in the stone wall until the dark circle becomes the round scale pan of scene two",
            f"{S} holding out a few tiny babies on one hand and many white-haired adults on the other with a puzzled "
            "look, an empty blank chart axis drawn behind him."),
}

I = {
    8: f"A band of Stone Age hunter-gatherers walking across a golden savanna with spears, baskets, children and elders, "
       f"a big sun on the horizon, {FULL}.",
    9: f"A newborn baby wrapped in fur held in its mother's arms in a cave, a big golden sun rising behind them, soft glow, {FULL}.",
    10: f"{GHOST}: six are solid colored and smiling, four are pale dotted ghost outlines, children with round heads, {EDGE}.",
    11: f"A big hand-drawn weighing scale tipped far down on one side, the heavy pan holding four tiny baby faces and the "
        f"other pan holding many grown-ups, the pointer swinging low, no numbers, {EDGE}.",
    12: f"A teenage Stone Age girl with a spear standing on a hilltop looking at a long winding path ahead that leads to a "
        f"golden sunset, tiny figures along the path growing older until a white-haired woman at the end, {FULL}.",
    13: f"A white-haired elder telling a story by a campfire to wide-eyed grandchildren sitting around, warm firelight, {FULL}.",
    14: f"Close-up portrait of a cheerful old Stone Age man with a long white beard, deep wrinkles and a walking stick, "
        f"smiling, mountains behind, {FULL}.",
    15: f"{S} with a bandage on his forehead giving a thumbs up, shrugging, among cave dwellers who carry water and mend "
        f"hides, {FULL}.",
    16: f"{S} picking green plants and mushrooms in a lush forest with a wicker basket, sunbeams through the trees, {FULL}.",
    17: f"Wide landscape of green hills in northern Spain with a cave entrance in a limestone cliff, a small stream and "
        f"morning mist, {FULL}.",
    18: f"A group of {NE} figures gathered around a fire inside the cave: a mother, children and men, warm light, {FULL}.",
    19: f"A giant magnifying lens held over a row of big yellowish teeth with hard tartar buildup on them, {FULL}.",
    20: f"{S} lying back in a modern dentist chair while a cartoon dentist in a white coat and mask scrapes his teeth with "
        f"a tiny hook, bright clean clinic, {NOTXT}, {FULL}.",
    21: f"{NE} chewing a twig with a swollen red cheek, and enlarged crumbs of food stuck between his teeth drawn like "
        f"little bubbles, {FULL}.",
    22: f"A young {NE} curled up holding his swollen jaw with one hand and his belly with the other, sweat drops, a glowing "
        f"cutaway of his belly shows a tiny worm, {FULL}.",
    23: f"A tall poplar tree with fluttering green-and-silver leaves and a glowing double helix DNA strand floating above "
        f"it, {FULL}.",
    24: f"A poplar leaf on the left and a plain white round tablet on the right connected by a glowing curved arrow, soft "
        f"background, {EDGE}.",
    25: f"Close-up of fuzzy blue-green mold growing on a piece of old bread, with a tiny magnifying lens beside it, {FULL}.",
    26: f"A group of healthy {NE} figures standing in a cave grinning with empty hands, while one sick young {NE} sits apart "
        f"in the foreground chewing a twig, {FULL}.",
    27: f"Two archaeologists in a lab with a microscope, chins in hands, looking skeptical, one raising a finger to say "
        f"wait, {FULL}.",
    28: f"{NE} holding a bitter poplar twig with a disgusted face and tongue out, next to a pile of tasty nuts and berries "
        f"that he is ignoring, {FULL}.",
    29: f"Wide view of a misty Sumatran rainforest canopy with a huge tree and sunbeams through the leaves, {FULL}.",
    30: f"Close-up portrait of {RAK} looking sad, in a green forest, {FULL}.",
    31: f"{RAK} chewing green leaves from a thick vine hanging from a tree, with a thoughtful face, {FULL}.",
    32: f"{RAK} pressing a green paste of chewed leaves onto the cut on his cheek with one finger, {FULL}.",
    33: f"Three heads of {RAK} in a row on a plain light background: the first with an open cut, the second with a smaller "
        f"cut, the third fully healed and smiling, {EDGE}.",
    34: f"{RAK} sitting proudly on a branch like a little doctor with a green leaf compress on his cheek, giving a thumbs "
        f"up, {FULL}.",
    35: f"A big old tree whose roots glow, with {RAK}, {NE} and {S} sitting on its branches, each holding a green leaf, "
        f"{FULL}.",
    36: f"A vast blue glacier high in the Alps under a clear sky, with a tiny dark shape frozen deep in the ice, {FULL}.",
    37: f"Two hikers in nineteen-nineties outdoor clothes with backpacks pointing at a dark shape in the ice, snowy peaks "
        f"around them, {FULL}.",
    38: f"A frozen man in a block of clear blue ice with scientists chipping carefully around him with ice axes, {FULL}.",
    39: f"{HOM} holding a string of round brown bracket mushrooms on a leather cord, a white birch tree behind him, {FULL}.",
    40: f"A cutaway of the belly of {HOM} with a few tiny thin worms inside that look guilty, {FULL}.",
    41: f"A Stone Age healer woman in furs slicing a bracket mushroom on a flat stone beside bundles of herbs, {NOTXT}, {FULL}.",
    42: f"{HOM} striking a flint against a dry mushroom to make sparks, with two thought clouds above him, one showing a "
        f"green leaf and the other a flame, {FULL}.",
    43: f"Back view of {HOM} standing in the snow, small dark tattoo lines on the knees and along his lower back, {FULL}.",
    44: f"A cutaway of an aching knee joint with small glowing red pain starbursts exactly over the tattoo marks, {FULL}.",
    45: f"{S} shrugging with both palms up and a puzzled face in front of a big question mark, plain light background, {EDGE}.",
    46: f"{S} running toward a modern dentist office with a tooth-shaped sign, holding his cheek, with speed lines, {FULL}.",
    47: f"An Ice Age camp in a snowy tundra with a woolly mammoth in the background and one lonely man sitting with a "
        f"toothache, nobody around to help, {FULL}.",
    48: f"A rock shelter under a limestone overhang at the foot of snowy Alpine mountains, with a small campfire, hide tents "
        f"and pine trees, {FULL}.",
    49: f"A giant cartoon molar tooth resting on a rock with a big dark cavity hole, an archaeologist's hand holding "
        f"tweezers beside it, {FULL}.",
    50: f"Extreme close-up of the cavity of the tooth with tiny scratch marks inside, circled by a glowing magnifier ring, {EDGE}.",
    51: f"An archaeologist in a lab scratching a model tooth with a tiny flint tool while looking through a microscope, {FULL}.",
    52: f"A young Stone Age man sitting with his mouth wide open and a nervous face while another person carefully reaches "
        f"in with a tiny sharp flint point, onlookers watching, {FULL}.",
    53: f"Portrait of a proud Ice Age dentist in furs holding a tiny flint pick, a polished shell worn like a head mirror, "
        f"and a leather roll of little flint tools, {FULL}.",
    54: f"A sunny Neolithic village with round thatched huts, wheat fields, a river and a goat, {FULL}.",
    55: f"Close-up of a canine tooth with a small crack filled with yellow beeswax, a honeycomb and a bee beside it, {FULL}.",
    56: f"A smiling Stone Age man with a golden glint on one tooth holding a piece of honeycomb, {FULL}.",
    57: f"The same smiling Stone Age man biting happily into a big roasted drumstick with a delighted face, {FULL}.",
    58: f"{S} tapping a giant tooth thoughtfully with a small glowing spark above his head, relief on his face, {FULL}.",
    59: f"A hooded healer silhouette standing against an orange sunset over the Andes mountains, mysterious, {FULL}.",
    60: f"{S} hiding behind a stone wall with wide nervous eyes and sweat drops, peeking at an ancient skull on a table, {FULL}.",
    61: f"A close view of an ancient skull on a wooden table with one neat round hole in it, an archaeologist pointing at "
        f"the hole, {FULL}.",
    62: f"A long wooden table with a row of six ancient skulls each with a round hole, an archaeologist walking by taking "
        f"notes, {FULL}.",
    63: f"Extreme close-up of the smooth, rounded healed edge of a hole in a skull highlighted by a soft glowing ring, {EDGE}.",
    64: f"The south coast of Peru: sand dunes meeting the Pacific ocean, an adobe village, llamas and morning fog, {FULL}.",
    65: f"Ten small Andean patients sitting in two rows of five with white head bandages: four are smiling and colored, "
        f"six are pale dotted outlines, {EDGE}.",
    66: f"A stone Inca city of terraces on a green mountain with llamas and clouds below, grand and sunny, {FULL}.",
    67: f"Ten small Andean patients with little woven hats sitting in two rows of five: seven are smiling and colored, three "
        f"are pale dotted outlines, {EDGE}.",
    68: f"A field hospital tent from the American Civil War with a surgeon in a blue coat, and ten soldier figures in blue "
        f"caps in front of it: five solid and five pale dotted outlines, {FULL}.",
    69: f"{ANDE} standing proudly with a bundle of herbs and a cotton cloth bandage, mountains behind him, {FULL}.",
    70: f"{ANDE} carefully treating a patient lying down with a white head bandage, a cup of herbs beside them, calm light, {FULL}.",
    71: f"Two Andean warriors with clubs and slings facing off on a hill, one helmet with a dent, dust in the air, {FULL}.",
    72: f"{S} standing between a green plant on the left and a stone knife on the right, shaking his head with a smile, a "
        f"big glowing heart above him, {FULL}.",
    73: f"A Stone Age woman gently tucking a fur blanket over a sleeping injured man in a cave, tender firelight, {FULL}.",
    74: f"A mountain cave in a rocky valley in northern Iraq with a lone bandaged {NE} sitting at the entrance, {FULL}.",
    75: f"{NE} sitting with a bruised eye, one arm in a sling made of hide and one leg in a splint of sticks, {FULL}.",
    76: f"{NE} cupping a hand behind his ear with a confused face, while hunters with spears walk away in the distance, {FULL}.",
    77: f"An older {NE} with gray in his beard smiling by a fire while little kids climb on him, {FULL}.",
    78: f"A {NE} woman handing a piece of roasted meat to the injured man, while others bring water and firewood, {FULL}.",
    79: f"Rolling hills of Georgia in the Caucasus with an archaeological dig on a hillside above a river, {FULL}.",
    80: f"An ancient early-human skull resting on a rock in warm light, with dust floating in the air, {FULL}.",
    81: f"Close-up front view of the jaw of the skull with a single lonely tooth remaining, highlighted by a magnifier ring, {EDGE}.",
    82: f"An early hairy heavy-browed human chewing a root and carefully handing the soft mashed food to a toothless old "
        f"companion, {FULL}.",
    83: f"Two silhouettes walking hand in hand toward a sunset, one limping and leaning on the other, {FULL}.",
    84: f"{S} pulling open a leather curtain at a cave entrance that reveals a lush green jungle beyond, {FULL}.",
    85: f"A lush tropical rainforest in Borneo with a limestone karst cliff, a hornbill bird and mist, {FULL}.",
    86: f"Archaeologists in hats and headlamps working in a cave excavation pit marked with a string grid, soft brushes in hand, {FULL}.",
    87: f"Top-down view of a skeleton laid in a burial pit in cave soil, with brushes beside it, {FULL}.",
    88: f"Close view of the skeleton's legs: the right leg complete, and the left leg bone ending below the knee, ochre soil, {FULL}.",
    89: f"Close-up of the smooth rounded end of the left shin bone under a magnifier, with a thought cloud showing a "
        f"crocodile and a tiger each crossed out by a red slash, {FULL}.",
    90: f"A Stone Age healer holding up a razor-sharp stone blade in the firelight, calm and focused, with a bowl of herbs "
        f"beside, {FULL}.",
    91: f"{NI} as a small child lying on a bed of leaves with the lower left leg wrapped in big green leaves and bark cloth, "
        f"a healer woman tending him and family around, {FULL}.",
    92: f"{NI} walking proudly through a sunny forest with a wooden crutch, {FULL}.",
    93: f"{NI} as a teenager crossing a fallen log over a jungle river with his crutch while other kids cheer, {FULL}.",
    94: f"A Neolithic farmer with a bandaged stump of a forearm hoeing a wheat field under a sunny sky, {FULL}.",
    95: f"A long ink timeline drawn like a rope: a wheat sheaf at the right end, a small cave with a child at the far left "
        f"end, and a big curved arrow showing a giant jump between them, {EDGE}.",
    96: f"A healer pointing a stick at a leg-bone drawing on a cave wall made with ochre while apprentices listen, {FULL}.",
    97: f"A healer binding a leaf poultice around a child's leg while the mother holds the child's hand, {FULL}.",
    98: f"A group of Stone Age people standing around a grave inside the cave, a hand placing a flower on it, soft light, {FULL}.",
    99: f"{S} opening a modern bathroom medicine cabinet with plain unlabeled boxes and bottles, looking thoughtful, {NOTXT}, {FULL}.",
    100: f"A willow tree with long drooping branches beside a river, and a plain white tablet resting on a rock in front, {FULL}.",
    101: f"A cozy nineteen-twenties laboratory with a scientist in a white coat and round glasses looking at a dish with "
         f"blue mold, an old brass microscope on the desk, {FULL}.",
    102: f"A jar of golden honey with a wooden dipper dripping, a roll of bandage and a bee, plain unlabeled jar, {FULL}.",
    103: f"An elder holding up a plant by a campfire while a circle of people nod and listen, children in front, {FULL}.",
    104: f"A Stone Age person who ate a red-spotted mushroom with a green face, swirly eyes and a hand on the tummy, {FULL}.",
    105: f"{DOC} examining {S} with a stethoscope in a clean, warm clinic, both smiling, {NOTXT}, {FULL}.",
    106: f"Prehistoric people helping each other: a strong man carrying a limping friend and a woman sharing herbs, {FULL}.",
    107: f"{S} holding up a small white-and-pink capsule pill between two fingers and looking at it closely, with a glass "
         f"of water on a kitchen counter, {FULL}.",
    108: f"{S} holding a pill while ghostly translucent figures rise behind it: {NE} chewing bark and an Ice Age dentist "
         f"with a flint pick, {FULL}.",
    109: f"{NI} with his crutch smiling, surrounded by Stone Age kids helping him walk, golden light, {FULL}.",
    110: f"A long chain of silhouettes holding hands from the deep past across the hills to {S} at the front, who waves at "
         f"the viewer at sunrise, {FULL}.",
    111: f"{S} sitting by a campfire holding a smartphone with big glowing wifi arcs radiating above him, a cave behind, "
         f"smiling at the viewer, {FULL}.",
}

# 12-oct-2026: el saldo de Flow dio para 6 clips; el beat 7 (2 escenas) pasa a DOS imágenes y el resto se corre +1.
A7 = f"A smiling old Stone Age woman with white hair and a walking stick surrounded by laughing kids on a grassy hill, {FULL}."
B7 = (f"{S} holding out a few tiny babies on one hand and many white-haired adults on the other with a puzzled look, "
      f"an empty blank chart axis drawn behind him, {FULL}.")
I = {**{k + 1: v for k, v in I.items()}, 7: A7, 8: B7}
V.pop(7)

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(V) + len(I), (len(bs), len(V) + len(I))
out = {}
for k, b in enumerate(bs, 1):
    assert (b["tipo"] == "video") == (k in V), (b["id"], b["tipo"])
    out[b["id"]] = E + (V[k] if k in V else I[k]) + C
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts ({len(V)} video + {len(I)} imagen)")
