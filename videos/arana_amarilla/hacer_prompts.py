# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video.
Beats de VIDEO (1-7): plantilla de dos escenas por clip de 10 s (combinar=True)."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
G = F["personajes"]["garden"]
M = F["personajes"]["male"]
J = F["personajes"]["joro"]
H = F["personajes"]["human"]
WEB = F["objeto"]
GS = ("a cartoon yellow garden spider with a big oval yellow and black striped abdomen, a silvery-white head, big round "
      "friendly eyes and long black and orange-banded legs, wearing a tiny green straw sun hat")
GH = "a cartoon green grasshopper with big round goofy eyes and long folded back legs"
GRAN = "a cartoon grandmother with a round white head, dot eyes, grey hair in a bun, round glasses and a lavender cardigan"
KIDS = "two small cartoon kids with round white heads and dot eyes, one in a yellow t-shirt and one in a green t-shirt"
YARD = "a sunny American backyard garden with tomato plants, tall sunflowers, a white picket fence and a wooden porch"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
NOTXT = "every can, box, sign and jar is plain and unlabeled with no writing on it"


def clip(a, trans, b):
    return f"Scene one, first five seconds: {a} Then {trans}. Scene two, last five seconds: {b}"


V = {
    1: clip(f"{YARD} on a warm late-summer morning, {H} stepping out of the back door holding a green watering can, "
            "humming, sunlight and morning dew everywhere.",
            "the camera follows him as he walks forward between the tomato plants",
            f"{H} stopping suddenly with a jolt, his nose just a few inches from a huge glittering spider web stretched "
            "between two tomato plants, his eyes wide."),
    2: clip(f"a close view of {WEB} stretched between two tomato plants, covered in tiny sparkling dew drops in the "
            "morning sun, gently swaying.",
            "the camera slowly glides toward the center of the web",
            f"{G} hanging head down in the very center of the web, enormous and close, slowly turning her head to look "
            "at the camera."),
    3: clip(f"extreme close-up of {G}, her bright yellow and black stripes shining, her long striped legs flexing one "
            "by one.",
            "the camera pulls back and tilts along one long leg",
            f"the full {WEB}, with the white zigzag band of silk running straight up and down through the middle, the "
            "spider sitting on it, sunflowers behind."),
    4: clip(f"{H} reaching for a long stick lying in the grass, a green garden hose and an unlabeled bug spray can lying "
            "next to it, a determined frown on his face.",
            "the stick freezes in mid air and the scene peels away like a turning sketchbook page",
            f"{G} standing proudly in the center of her web like a tiny garden guard, chest out, with the sunny "
            "vegetable garden behind her."),
    5: clip(f"{GH} leaping off a tomato leaf and flying straight into the sticky spiral of the web, legs flailing, "
            "while a fly buzzes nearby.",
            "a gust of wind blows a few leaves across the frame and when they pass we are in scene two",
            f"a fluffy brown moth and a striped wasp stuck side by side in the web, {G} walking toward them calmly, "
            f"while {H} in the background slowly lowers his stick."),
    6: clip(f"an old wooden porch in the American South at dusk with fireflies, {GRAN} in a rocking chair telling a "
            f"story to {KIDS} who sit at her feet with big scared eyes.",
            "the ink lines of the scene come loose, swirl like ribbons and redraw themselves into scene two",
            f"a spooky moonlit garden with {WEB} glowing white in the dark, its zigzag band wiggling like a squiggly "
            "scribble, a cold blue light, mysterious mood, no readable letters."),
    7: clip(f"a cartoon scientist with a round white head, dot eyes, glasses and a white lab coat studying {WEB} through "
            "a big magnifying glass, scratching his head.",
            "the camera pushes in quickly through the magnifying glass",
            f"two cartoon scientists arguing in front of a giant drawing of a zigzag web pinned to a board, waving "
            f"their arms, while {G} watches them from the corner with a tiny smile."),
}

I = {
    8: f"{G} giving a friendly wave with one leg in the center of her web, a soft spotlight on her as if she is being introduced on stage, {FULL}.",
    9: f"A proud portrait of {G} in her web among tomato plants and sunflowers, like an official nature guide photo, {FULL}.",
    10: f"{G} sitting at a tiny school desk writing with a feather quill on her web like a chalkboard of silk, the silk showing only a squiggly zigzag, no letters.",
    11: f"Three funny costume portraits of {GS} in a row: one dressed with a zipper on her belly, one hugging a corn cob, one holding a banana, on a plain off-white background.",
    12: f"A simple cartoon map of North America with the whole United States painted sunny yellow and dotted with tiny spider webs, plain blue ocean around it, no labels.",
    13: f"The same simple cartoon map of North America now with Mexico and Central America also painted sunny yellow with tiny spider webs, and southern Canada lightly tinted, no labels.",
    14: f"Close-up of {G} next to a plain wooden ruler with no numbers lying on a garden table, her body as long as one wide segment of the ruler.",
    15: f"{G} sitting in the open palm of a cartoon human hand, her long legs stretched out to the edges of the palm, the hand trembling slightly.",
    16: f"{G} large in the center of her web, and next to her {M} so small that he is barely a dot, with a magnifying glass circle showing him up close.",
    17: f"{H} walking past a garden web without noticing {M} sitting at the edge of the web, while {G} rests in the center.",
    18: f"{G} hanging head down in the center of her web, her eight legs held together in four neat pairs, calm and still, sunny garden behind.",
    19: f"{G} seen straight on in her web with her legs held together in pairs so her whole silhouette makes a big bold X shape, a few sparkles around her.",
    20: f"A wide view of {WEB} glowing in the morning sun between two sunflowers, {G} small in its center, {FULL}.",
    21: f"A big cartoon bicycle wheel leaning against a fence next to {WEB}, both the same round shape with spokes, the spider looking at the wheel with interest.",
    22: f"{H} holding his arms apart measuring the width of {WEB} in a sunny garden, impressed, while {G} sits in the middle.",
    23: f"Three garden spots with spider webs in one wide sunny backyard: a web between tall plants, a web along a white picket fence, and a web under the edge of a wooden porch roof.",
    24: f"Moths, flies and a grasshopper flying through a sunny garden toward a waiting web, {G} rubbing two legs together in anticipation.",
    25: f"A garden at night under a crescent moon, {G} rolling up the center of her web into a ball of silk like rolling up a carpet.",
    26: f"{G} at night spinning a fresh new spiral in the center of her web, moving around in circles, a thin silk thread trailing behind her.",
    27: f"{G} happily eating a ball of old silk like cotton candy, with a tiny napkin around her neck, under the moonlight.",
    28: f"Simple diagram on a plain off-white background: an arrow going from a ball of old silk into {GS} and another arrow going from her to a shiny new web, in a circle like a recycling loop.",
    29: f"{G} strolling confidently along one dry straight spoke of her web, like a tightrope walker, sunny garden behind.",
    30: f"A fly stuck on the sticky spiral threads of the web, trying to pull its feet free with glue-like strings stretching, looking frustrated.",
    31: f"{G} with her eyes squinting, wearing tiny thick glasses that are too big, while her legs rest on the threads of her web feeling them.",
    32: f"Close-up of {G}'s leg tips resting on silk threads, with small wavy vibration lines traveling along the threads toward her.",
    33: f"{G} in the center of her web wearing big cartoon headphones, listening carefully, with wavy vibration lines coming from the web all around her.",
    34: f"A sunny garden with {WEB}, and a small dark shape flying fast toward it with motion lines, {G} turning her head alert.",
    35: f"{GH} jumping from a tomato leaf, missing it, and flying through the air toward the sticky web with a surprised face.",
    36: f"{G} sprinting across the spokes of her web at top speed with motion lines behind her legs.",
    37: f"{G} spinning {GH} around and around with her legs, swirl lines showing the spin, silk wrapping around it.",
    38: f"A grasshopper wrapped completely in white silk like a tiny mummy hanging in the web, only its big goofy eyes peeking out, {G} beside it.",
    39: f"The silk-wrapped grasshopper mummy with dizzy spiral eyes and small stars above it, now still and calm, {G} looking satisfied.",
    40: f"{G} in her web facing a huge grasshopper bigger than she is, both measuring each other, the spider looking confident.",
    41: f"A wide garden web catching several insects: a moth, a fly, a beetle, a bee and a wasp, each stuck on a different part of the spiral, {G} in the center.",
    42: f"{G} carrying a silk-wrapped package on her back back toward the center of her web like a delivery worker.",
    43: f"{YARD} seen through a summer from early to late, sunflowers growing taller, {G} always in her web in the middle.",
    44: f"A tomato plant with healthy leaves next to a web full of caught grasshoppers and beetles, a pile of chewed leaves only on the other side of the fence where there is no web.",
    45: f"A cartoon gardener with a round white head, dot eyes and a straw hat smiling and giving a thumbs up to {G} in her web among the tomatoes.",
    46: f"{G} unpacking a tiny suitcase in the center of her web like moving into a new home, a small welcome mat on the web.",
    47: f"Close-up of the center of {WEB}, the white zigzag silk band shining in the sun.",
    48: f"Close-up of the thick white zigzag band of silk running up and down through the center of the web, next to a big cartoon zipper for comparison.",
    49: f"{G} pointing proudly with one leg at the white zigzag band in her web like a museum guide, a scientist with glasses taking notes.",
    50: f"{GRAN} on a porch rocking chair at dusk telling a story with a dramatic hand gesture, {KIDS} leaning in.",
    51: f"The zigzag in the web drawn in a spooky blue moonlight so its squiggles look a little like mysterious handwriting, but no real letters at all.",
    52: f"{KIDS} hiding behind a porch post with terrified faces, peeking at a moonlit garden web, goosebumps lines around them.",
    53: f"{G} in her web shrugging with a confused smile while a giant question mark floats next to her.",
    54: f"{G} holding a tiny pencil upside down and scratching her head, an empty silk web in front of her, totally clueless.",
    55: f"{KIDS} laughing and relieved on the porch while {GRAN} winks, a sunny morning now.",
    56: f"{GRAN} reading a big storybook to {KIDS}, while behind them a faded old family photo shows a younger grandmother being told the same story by her own grandmother.",
    57: f"Two cartoon scientists in lab coats looking puzzled at {WEB}, scratching their heads, with three empty thought bubbles above them.",
    58: f"A cartoon blue bird flying toward a web and swerving away at the last moment after seeing the bright white zigzag, {G} waving at it.",
    59: f"A glass patio door with a simple white bird-shaped sticker on it and a cartoon bird turning away from it, next to a web with a white zigzag, side by side.",
    60: f"A cartoon bird crashing through a spider web without a zigzag, the web torn and flapping, the spider hanging on by one thread looking annoyed.",
    61: f"The web shown in a glowing purple ultraviolet view, the zigzag shining brightly, with flies and bees turning toward it like moths to a lamp.",
    62: f"A small cartoon fly drawn toward the bright zigzag like a moth to a porch light, flying closer and closer, {G} waiting with a tiny fork.",
    63: f"{G} hiding behind the white zigzag band in her web, only parts of her stripes showing, a bird looking around confused.",
    64: f"Three small circles on a plain off-white background showing a bird, a fly and a hidden spider, all connected by lines to a white zigzag in the center.",
    65: f"{G} in her web dressed as a mysterious detective in a trench coat, a magnifying glass in one leg, a faint question mark in the zigzag behind her.",
    66: f"A curious cartoon dog sniffing toward a garden web, a bird landing nearby and a human hand reaching in, all getting close to {G}.",
    67: f"{G} gripping her web with all her legs and shaking it hard, the web blurred with wobble lines.",
    68: f"The whole web swinging back and forth like a trampoline, {G} a blurred big shape in the middle, a surprised bird leaning back.",
    69: f"A cartoon bird trying to grab the spider in the shaking web and missing, its beak snapping at empty air, motion lines everywhere.",
    70: f"{G} dropping straight down from her web on a thin silk line and landing in a pile of dry leaves below, only her hat sticking out.",
    71: f"{M} walking through tall grass carrying a tiny bouquet of flowers, looking nervous and hopeful.",
    72: f"{M} building a small, wobbly little web right next to the big web of {G}, like a tiny tent beside a mansion.",
    73: f"{M} gently plucking one thread of the big web like a guitar string, little music notes floating up, {G} listening.",
    74: f"Two cartoon scientists with round white heads, dot eyes, glasses and lab coats looking through a magnifying glass at {M}, amazed.",
    75: f"A simple soft-colored drawing of a tiny cartoon heart with a calm stop symbol next to it, and {M} lying peacefully asleep with closed eyes and a small halo, gentle and not scary.",
    76: f"{G} in her web with {M} still holding onto her side asleep with a halo, while another tiny male spider in the distance turns away disappointed.",
    77: f"Early fall in the garden, the sunflowers drooping, orange leaves falling, {G} rolling up her sleeves with a determined face.",
    78: f"{G} weaving a round brown papery egg sac, spinning it with her legs, among dry autumn leaves.",
    79: f"A round brown papery egg sac hanging in the web among autumn leaves, next to a cartoon wooden ruler with no numbers for size.",
    80: f"A cutaway drawing of a round brown egg sac showing many many tiny eggs packed inside like a pomegranate, a few more sacs hanging behind it.",
    81: f"{G} standing guard beside her egg sac in the web, holding a tiny shield, in the cool autumn evening.",
    82: f"The first frost on the garden at dawn, white frosty leaves and icicles, the web covered in frost, an empty spot in the center where the spider used to be, soft and peaceful.",
    83: f"A cutaway of the egg sac in winter snow, showing tiny baby spiders hatched inside, snuggled together asleep.",
    84: f"Spring in the garden with blooming flowers, tiny baby spiders climbing out of an open egg sac and looking around in wonder.",
    85: f"Tiny baby spiders floating through a blue spring sky on long silk threads like tiny kites, over gardens and rooftops.",
    86: f"{H} in a winter coat finding a brown egg sac stuck under a snowy porch railing, gently stepping back with a kind smile.",
    87: f"A brown egg sac on a porch with a tiny cartoon sign that has a drawing of a bug crossed out, no writing, and a happy garden in spring behind it.",
    88: f"{H} looking nervously at {G} with a worried thought bubble showing a giant scary monster spider.",
    89: f"{G} running away along her web with a nervous face as a big human finger approaches, little sweat drops flying.",
    90: f"A human hand squeezing a garden spider with two fingers, the spider looking offended, a tiny warning symbol above.",
    91: f"{H} holding up a finger with a tiny red dot and a slight swelling, looking mildly annoyed but fine, a cartoon honeybee shrugging next to him.",
    92: f"Simple diagram on a plain off-white background: a small green venom drop with an arrow to a cartoon grasshopper, and a crossed out arrow to a big human.",
    93: f"{H} holding a magnifying glass up to a garden web, with a simple checklist clipboard in his other hand that has only checkmarks and no words.",
    94: f"A sunny garden spot with {WEB}, the zigzag clearly visible, a bright sun shining.",
    95: f"{G} hanging head down in the center of her web, a big green checkmark floating next to her.",
    96: f"A cartoon map of the southeastern United States coast with orange trees, magnolias and pine trees, and {J} arriving with a tiny suitcase, no labels.",
    97: f"{J} in a large golden web, showing off its yellow and dark blue stripes, side by side with {GS} in her own web, both looking at each other.",
    98: f"{J} hanging in a shimmering golden web with no zigzag, showing a red patch under its belly, sunlight making the web glow gold.",
    99: f"{G} and {J} sitting side by side sharing a big pile of caught flies like a picnic, smiling.",
    100: f"{H} standing in his garden looking at {G} in her web, shrugging calmly with a relaxed smile.",
    101: f"{G} working happily in her web, wrapping a fly, while {H} walks past along a garden path that is blocked by her web across it.",
    102: f"{H} gently carrying {G} on the end of a stick toward a big bush, the spider holding on and waving.",
    103: f"An unlabeled bug spray can with a big red cross over it, and next to it {G} and a ladybug hugging each other in relief.",
    104: f"A wild garden with tall sunflowers, cosmos flowers and tall grasses left standing, many small webs glittering among them.",
    105: f"{G} relaxing in a hammock made of her web between two tall flowers, sunglasses on, happy.",
    106: f"{H} back in the morning garden from the beginning, watering can in hand, looking at {G} in her web with a curious gentle smile, {FULL}.",
    107: f"{G} in her web shaking her head with a little smile, the zigzag in her web just a simple squiggle, no letters.",
    108: f"{G} as a tiny garden guard with a tiny flashlight in her web at night, protecting ripe red tomatoes, a caught moth wrapped beside her.",
    109: f"An autumn garden at sunset with falling leaves, a round brown egg sac hanging alone in the web, warm and peaceful.",
    110: f"{H} setting the stick down in the grass and stepping carefully around the web, while tiny baby spiders float in the spring sky above.",
    111: f"{G} waving goodbye from the center of her web in the golden late-summer evening light over the tomato garden, {FULL}.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(V) + len(I), (len(bs), len(V) + len(I))
out = {}
for k, b in enumerate(bs, 1):
    assert (b["tipo"] == "video") == (k in V), (b["id"], b["tipo"])
    out[b["id"]] = E + (V[k] if k in V else I[k]) + C
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts ({len(V)} video + {len(I)} imagen)")
