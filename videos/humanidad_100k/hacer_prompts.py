# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video."""
import json
import os
import sys

# Agregar la carpeta del video a sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
S = F["personajes"]["sapiens"]
NEAN = F["personajes"]["neanderthal"]
DENIS = F["personajes"]["denisovan"]
CHILD = F["personajes"]["child"]
SPEAR = F["objeto"]

P = {
    1: "A busy modern city street with diverse cartoon people walking on the sidewalk in modern casual clothes, skyscrapers in the background, warm daylight, all smiling and minding their day.",
    2: "A glowing cartoon portal or magical swirling time-vortex in the middle of a city street, with an arrow pointing backward toward a misty primeval prehistoric horizon.",
    3: "A breathtaking vast wild prehistoric landscape untouched by civilization, towering glaciers in the far distance, lush green river valleys, and a massive herd of mammoths grazing peacefully.",
    4: "An ancient world map drawn like a primitive parchment, showing prehistoric continents with five distinct cartoon silhouettes of human faces placed across different regions.",
    5: "Five different cartoon archaic human figures standing in a circle in the wilderness, each with unique features, looking toward each other with curiosity.",
    6: "Panoramic split scene showing four distinct ancient biomes: an African savanna, a snowy European forest, a rocky Siberian mountain range, and a lush tropical jungle.",
    7: f"In an African savanna under a golden sun, {S} standing proudly beside an acacia tree, holding {SPEAR}, looking out at a herd of wild antelopes.",
    8: f"A snowy pine valley in Ice Age Europe with heavy snow falling, {NEAN} walking through deep snow carrying a bundle of firewood.",
    9: f"In a snowy clearing, {NEAN} kneeling behind a frosted rock, skillfully aiming a heavy wooden thrusting spear at a distant herd of wild reindeer.",
    10: f"Close-up portrait of {NEAN} wrapped in thick layers of warm furry mammoth pelts, breath steaming in the frosty air, smiling warmly with rosy cheeks.",
    11: f"High in the rugged rocky Altai mountains of Siberia under a violet dusk sky, {DENIS} standing outside a deep limestone cave entrance holding a flaming torch.",
    12: "A vibrant tropical rainforest with giant ferns and lush vines on the island of Flores, with sunlight streaming through the jungle canopy.",
    13: "A tiny cartoon Homo floresiensis hunter, less than one meter tall, walking past giant tropical mushrooms and watching a miniature pygmy elephant in the ferns.",
    14: "An old-fashioned stereotypical museum drawing of an ape-like caveman with hunched back and a clumsy club, crossed out with a large bold red X.",
    15: "A modern archeologist in a field jacket examining a stone artifact with a magnifying glass, next to a detailed anatomical chart showing complex human brains.",
    16: "A cozy prehistoric campsite nestled under a natural rock overhang, with a small nomadic clan of twenty early humans resting together around several small fires.",
    17: "Close view of two early humans carefully feeding dry twigs into a bright glowing campfire, sparks floating up into the twilight air.",
    18: "Early humans roasting fresh meat on wooden skewers over glowing red embers, delicious steam rising, smiling hungrily together.",
    19: "Close-up hands of an early craftsman carefully binding a sharp pointed flint blade onto a straight wooden shaft using sinew cord and dark tree resin glue.",
    20: "An early human using a smooth round river stone to grind a piece of bright red ochre mineral into vibrant red powder inside a flat stone mortar.",
    21: f"A soft animal hide blanket decorated with hand-painted red geometric patterns, and {S} painting red stripes onto their forearms with a wooden stick.",
    22: "Close-up hands carefully threading tiny pierced sea-snail shells onto a thin cord of plant fiber, creating a delicate decorative bead necklace.",
    23: "A whimsical split image: on the left a prehistoric human hunter holding a spear, on the right a modern person in jeans holding a cup, both looking identical in face and eyes.",
    24: "Two cartoon figures side by side with identical friendly faces, one in leather wraps and the other in a casual modern hoodie, comparing their hands.",
    25: "An early human kneeling on a grassy ridge, looking up at a starry night sky with big curious wide eyes, full of wonder and reflection.",
    26: f"A time machine cradle softly glowing with light, holding {CHILD} wrapped in a cozy modern baby blanket, smiling sweetly.",
    27: f"{CHILD} now a cheerful schoolkid in a colorful classroom, raising their hand eagerly at a wooden school desk with a notebook and pencils.",
    28: f"{CHILD} now a young adult wearing glasses and a lab coat, holding a smartphone in one hand while sketching a technical blueprint on a digital tablet.",
    29: "A tender ancient burial scene inside a cave, where clan members gently place colorful wild flowers and bead ornaments beside a resting ancestor.",
    30: "A clan gathered tightly around a crackling campfire at night under an immense crystal-clear night sky overflowing with millions of glowing stars and the Milky Way.",
    31: "A tiny group of four early humans walking across an immense empty grassland, looking fragile and tiny against the vast endless plains.",
    32: "High aerial view of a wide winding river cutting through wild steppes, with just one lone curl of campfire smoke in hundreds of miles.",
    33: "Three menacing prehistoric predators in the shadows of the tall grass: a sabertooth cat with long curved canine fangs, a giant cave hyena, and a massive woolly mammoth.",
    34: "A cold windy blizzard howling outside a cave, with early humans huddled close under fur blankets by dying embers, looking anxious.",
    35: "A lone abandoned stone spear point sticking out of frozen snowy ground, covered in light frost, quiet and haunting.",
    36: "A symbolic evolutionary timeline showing Neanderthals, Denisovans, and island humans fading into soft glowing silhouettes, leaving Homo sapiens standing forward.",
    37: "A dynamic map of the Earth with golden footprints spreading across Africa, Europe, Asia, Australia, and the Americas, showing humanity expanding.",
    38: "Two shadowy friendly figures—a Neanderthal and a Denisovan—standing behind a modern human like protective ancient guardians in the mist.",
    39: "A glowing cartoon DNA double-helix spiral, with bright golden segments labeled with subtle ancient bone and flint symbols shining brightly.",
    40: "A warm glowing campfire where a Homo sapiens and a Neanderthal sit together on logs, sharing roasted food and smiling under the stars.",
    41: "A modern person looking into a quiet mirror, and their reflection shows the gentle eyes of an ancient hunter by a campfire, warm and alive.",
}

beats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beats.json")
beats = json.load(open(beats_path, encoding="utf-8"))
assert len(beats) == len(P), f"Discrepancia: {len(beats)} beats vs {len(P)} prompts"

out = {b["id"]: E + P[k + 1] + C for k, b in enumerate(beats)}
prompts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.json")
json.dump(out, open(prompts_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"Generados exitosamente {len(out)} prompts en prompts.json")
