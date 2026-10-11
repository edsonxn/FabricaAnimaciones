# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video:
   python hacer_prompts.py  ->  luego  python fab.py avispas_invierno prompts"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
Q = F["personajes"]["queen"]
W = F["personajes"]["worker"]
H = F["personajes"]["human"]
N = F["objeto"]
YQ = Q.replace("a cartoon yellowjacket wasp queen", "a young cartoon yellowjacket wasp queen")
OLD = Q.replace("a cartoon yellowjacket wasp queen", "an old tired cartoon yellowjacket wasp queen").replace("a tiny gold crown", "a tiny dull crooked gold crown")
MALE = "cartoon male yellowjacket wasps with slim yellow and black striped bodies, long curved antennae and no crown"
LARVA = "fat white cartoon wasp larvae with tiny smiling faces, each sitting in a six-sided paper cell"

P = {
    1: f"Wide view of {N}, the size of a basketball, hanging under the roof edge of a wooden house on a gray autumn day, completely still and silent, orange leaves drifting past, not a single wasp in sight.",
    2: f"A wooden house porch in autumn with {N} hanging above it, the porch floor completely clean and empty, {H} standing below looking up at the silent nest with a puzzled face, bare tree branches and a cold pale sky.",
    3: f"Inside a dark dusty attic of a wooden house, a flashlight beam held by {H} sweeps across the rafters, and in a far corner {Q} is tucked motionless against a wooden beam, fast asleep.",
    4: f"Cutaway view of the inside of {N} in winter, imagined as a cozy cave: {W} sleeping in tiny beds with blankets and nightcaps, snow falling outside, a big red cross drawn over the whole scene to show the idea is wrong.",
    5: f"Inside a paper wasp nest with rows of six-sided cells, a crowd of {W} looking worried and tired, some staring at a small wall calendar with autumn leaves drawn on it, cold blue light coming through the entrance hole.",
    6: f"A single {YQ} standing proudly on a green leaf in bright warm summer sunlight, a flowering backyard garden and a wooden fence behind her, blue sky.",
    7: f"Cutaway view of the inside of a huge busy paper wasp nest in summer, built like a city with many floors of six-sided cells, hundreds of {W} rushing around, and in the center {Q} laying a small white egg into a cell.",
    8: f"A sunny summer backyard garden, several {W} flying fast, one grabbing a house fly in midair, another carrying a green caterpillar away from a tomato plant, a wooden fence and blue sky behind.",
    9: f"Close view of one of the {W} holding a piece of green caterpillar in its front legs and looking at it sadly, unable to eat it, inside a paper nest with six-sided cells.",
    10: f"Simple side view diagram of one of the {W}, its tiny narrow waist circled in red, a chunk of solid food stuck in front of the waist with a small red stop sign next to it, plain off-white background.",
    11: f"Inside a paper wasp nest, one of the {W} chewing food into a green paste ball and offering it to {LARVA} with wide open mouths.",
    12: f"Close view inside a paper wasp nest: {LARVA}, one larva giving a shiny golden drop of sugary liquid to one of the {W}, who drinks it happily.",
    13: f"Simple trade diagram on a plain off-white background: on the left one of the {W} hands a green ball of chewed meat to a fat white cartoon wasp larva, on the right the larva hands back a shiny golden drop, two curved arrows forming a circle between them.",
    14: f"Wide cutaway view of a giant paper wasp nest glowing warmly like a city at night, every floor full of {W} working and feeding {LARVA}.",
    15: f"Inside a paper wasp nest in late summer, {Q} sitting still with her arms crossed next to a row of empty six-sided cells, a few confused {W} looking at her.",
    16: f"Close view of special larger six-sided paper cells inside a wasp nest, each holding a bigger white egg glowing softly, different from the small normal cells around them, {Q} watching over them.",
    17: f"At the round entrance hole of {N}, a group of {MALE} and several {YQ} flying out of the nest into a golden late summer sky.",
    18: f"Inside a paper wasp nest, rows and rows of completely empty six-sided cells with cobwebs, a few {W} standing around holding food with nobody to give it to.",
    19: f"A crowd of {W} sitting on a branch outside {N}, looking hungry and bored, one holding an empty cup, late summer backyard behind them.",
    20: f"A backyard picnic table in September with a checkered cloth, sandwiches and a soda can, a swarm of {W} diving toward the food while {H} leans back in alarm.",
    21: f"Close view of one of the {W} with big pleading hungry eyes and a rumbling thin belly, hovering near the rim of a glass of lemonade on a picnic table.",
    22: f"Close view of a picnic table with an open orange soda can, a slice of watermelon and a melting ice cream cone, several {W} happily drinking and licking the sweet drops.",
    23: f"Wide view of a suburban backyard on a cold gray morning, the first white frost covering the grass, the fence and the last leaves, {N} hanging under the roof of the wooden house.",
    24: f"Close view of several {W} huddled together and shivering on the outside of {N}, tiny puffs of cold breath, frost crystals on the paper.",
    25: f"On frosty grass in a backyard, a few {W} crawling very slowly with drooping wings and half-closed eyes, white frost on the blades of grass around them.",
    26: f"Frosty ground covered with fallen brown leaves in a backyard, a few {W} and {MALE} lying still on their backs with their legs curled up, a cold pale sunrise.",
    27: f"Inside a dim cold paper wasp nest, {OLD} sitting alone and weak among empty six-sided cells.",
    28: f"Inside a dark cold paper wasp nest, {OLD} lying still on her side among empty six-sided cells, a single snowflake drifting in through the entrance hole.",
    29: f"{N} hanging under a snowy roof edge of a wooden house in winter, torn open on one side to show it is completely empty inside, snow falling, nobody around.",
    30: f"Three {YQ} flying together through an autumn backyard with orange trees, looking determined, the old gray nest small in the distance behind them.",
    31: f"On a tree branch with yellow autumn leaves, {YQ} sitting next to one of the {MALE}, small red hearts floating between them, soft golden evening light.",
    32: f"{YQ} sitting at a flower full of nectar and drinking greedily, her cheeks full, while two thin {W} in the background stare at her in surprise.",
    33: f"{YQ} looking very round and chubby, patting her big full belly with a satisfied smile, sitting on an autumn leaf.",
    34: f"Simple diagram on a plain off-white background: {YQ} seen from the side with her round body drawn like a fuel tank filled to the top with glowing golden fuel, next to a row of exactly six small calendar pages, six pages in total, each with a snowflake on it.",
    35: f"{YQ} hovering in the air, and inside her round belly a tiny glowing drawing of a whole miniature wasp nest city full of tiny wasps.",
    36: f"{YQ} flying alone across a windy autumn backyard, looking left and right for shelter, dark rain clouds gathering, leaves blowing past a wooden fence.",
    37: f"Close view of the trunk of an old tree with a piece of loose bark lifted away, and {YQ} squeezing into the dry dark gap underneath, wind and rain outside.",
    38: f"A tall pile of split firewood stacked next to a rotting mossy log in a backyard, and {YQ} peeking out from a dark gap between two logs.",
    39: f"Wide view of a cozy wooden suburban house at dusk in late autumn with warm light in the windows, and a tiny {YQ} flying toward a small gap under the roof.",
    40: f"Cutaway view of a wooden house showing three hiding places at once: the dusty attic under the roof, the hollow space behind the wooden siding, and a small garden shed next to the house, a small yellow arrow pointing at each spot.",
    41: f"Inside a living room, close view of a heavy red curtain by a window, one fold of the curtain pulled back to reveal {YQ} hiding inside the fold.",
    42: f"Extreme close view of {YQ} with her wings and antennae folded tightly under her body, gripping the edge of a wooden beam with her jaws, eyes closing, the wooden attic filling the whole image with no white margin and no panel outline.",
    43: f"{YQ} hanging completely motionless from a wooden attic beam, eyes closed, a few dust specks floating in a thin ray of light, everything still.",
    44: f"Close view of {YQ} asleep on a wooden attic beam, a small red heart drawn inside her chest beating very slowly with a faint pulse line next to it, an untouched crumb of food beside her.",
    45: f"Simple cutaway diagram of {YQ} asleep, her body filled with a glowing blue liquid like antifreeze, small snowflakes bouncing off her, plain cold blue background.",
    46: f"Close diagram view: sharp pointed ice crystals stopping at the edge of a round cartoon cell protected by a glowing blue shield of liquid, the cell smiling and safe.",
    47: f"Wide view of a dark empty attic in the middle of winter, snow piled against a small round window, and far away on a beam a tiny {YQ} hanging alone, a calendar on the wall showing winter months crossed off.",
    48: f"{YQ} asleep and curled up small, and above her a dreamy thought cloud showing a whole giant paper wasp nest city full of tiny wasps.",
    49: f"{YQ} asleep on a wooden beam in a dark attic, and next to her two large playing dice tumbling in the air, dramatic shadows.",
    50: f"In a dark attic corner, a large hairy cartoon house spider with eight eyes creeping along a web toward a sleeping {YQ} tucked against a wooden beam.",
    51: f"Close view of a sleeping {YQ} tucked in a damp dark corner of a wooden shed, patches of fuzzy gray-green mold slowly spreading over the wood toward her.",
    52: f"Split scene: on the left a freezing snowy backyard with {YQ} sleeping safely under tree bark, on the right a strangely warm sunny winter backyard with melting snow and {YQ} awake and confused.",
    53: f"{YQ} awake and thin, flying over a bare brown winter garden with no flowers and no insects, looking hungry, a nearly empty fuel gauge drawn on her belly.",
    54: f"Wide view of a dark attic with a long wooden beam, a row of several {YQ} tucked along it, most of them gray and faded like ghosts, only one still bright yellow and alive.",
    55: f"One bright yellow {YQ} still asleep on a wooden attic beam while a first thin ray of warm golden sunlight comes through a window and touches her.",
    56: f"{YQ} crawling out of a gap under the roof of a wooden house into bright spring sunlight, stretching her wings, green buds and pink blossoms on the trees.",
    57: f"{YQ} standing completely alone on a wooden fence post in a wide empty spring backyard, looking small, green grass and a few dandelions.",
    58: f"Close view of {YQ} scraping thin curls of wood from a weathered wooden fence board with her jaws, tiny wood shavings falling.",
    59: f"Under the edge of a wooden shed roof, {YQ} building a tiny gray paper nest no bigger than a golf ball, with a real white golf ball drawn next to it for size.",
    60: f"Cutaway view of a tiny gray paper nest with only five six-sided cells, each holding one small white egg, and {YQ} carefully watching over them alone.",
    61: f"Three small panels side by side in one image: {YQ} catching a fly in a garden, the same queen feeding a tiny white larva in a paper cell, and the same queen standing guard at the nest entrance with a stern face.",
    62: f"Inside a small paper nest, the first few {W}, young and fresh, climbing out of their six-sided cells and stretching, while {Q} watches them proudly.",
    63: f"Inside a growing paper wasp nest, {Q} sitting comfortably in the center laying eggs while several {W} fly in and out of the entrance hole carrying food.",
    64: f"Wide view of a sunny midsummer backyard with a large {N} hanging under the roof of a wooden house, dozens of {W} flying in and out.",
    65: f"Cutaway view of a giant paper wasp nest packed with thousands of tiny {W} on many floors, glowing like a busy city, summer sunlight outside.",
    66: f"A simple cartoon map of the southeastern United States with Florida and southern Alabama colored warm orange, a bright sun and palm trees drawn over them, and a small paper wasp nest symbol in each.",
    67: f"A green warm southern backyard in winter with palm trees and no snow, a large {N} hanging from a tree, still busy with {W} flying around it.",
    68: f"Cutaway view of an enormous paper wasp nest with several {Q} each laying eggs on a different floor at the same time, surrounded by crowds of {W}.",
    69: f"An old rusty abandoned car in an overgrown southern field, its entire inside filled from seat to roof with a gigantic gray papery wasp nest bulging out of the open windows, {H} staring at it from a safe distance with his mouth open.",
    70: f"{N} hanging silently under the snowy roof edge of a wooden house in winter, seen from below, soft snowfall.",
    71: f"{H} wearing a warm scarf and standing on a short ladder in the snow, calmly lifting the empty {N} off the roof edge with both hands.",
    72: f"Inside a dusty attic in winter, {H} holding a flashlight and leaning in close to look at one slow sleepy {YQ} resting on a wooden beam.",
    73: f"Extreme close portrait of {YQ} on a wooden attic beam, half-opening one eye, her tiny gold crown catching a glint of light.",
    74: f"{YQ} asleep on a wooden attic beam with snow falling outside the window, and inside her round belly a glowing miniature summer wasp nest city full of tiny wasps.",
}

beats = json.load(open("beats.json", encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
out = {b["id"]: E + P[k + 1] + C for k, b in enumerate(beats)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts · largo medio", sum(map(len, out.values())) // len(out))
