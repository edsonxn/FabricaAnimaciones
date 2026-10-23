# -*- coding: utf-8 -*-
"""Escribe prompts.json (9:16, un prompt por beat) de los Shorts de la tanda de Wild Next Door con la FICHA de su guion.
Uso: python videos/_shorts_prompts_wnd.py <v>_short   (luego fab.py <v>_short prompts y flow_integrado paquete)"""
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

ESC = {
    "mariquitas_casa_short": [
        "{H} stepping outside and staring at a light wooden house wall completely covered with hundreds of small orange lady beetles, autumn trees.",
        "The same house wall a week later, clean and empty, a few orange leaves falling, quiet.",
        "{H} looking around the empty wall with a puzzled face and a big question mark above her head.",
        "A vertical cutaway of a house wall and attic with hundreds of lady beetles hidden inside the wall spaces, cozy.",
        "{B} asleep inside the wall under a tiny blanket, snow falling outside a small window.",
        "{B} standing proudly and peeling off a red ladybug costume mask, sly.",
        "Close-up of the white head of {B} with a bold black M-shaped mark, a magnifying glass in front of it.",
        "A sunny light-colored house wall in autumn sunlight, {B} looking at it dreamily.",
        "A pale sunny rocky cliff in the mountains of Asia with lady beetles tucked into cracks, side by side with a light house wall.",
        "Lady beetles with tiny suitcases walking into a gap in a house wall like snowbirds arriving at a condo.",
        "A cluster of lady beetles sleeping deeply in the attic with tiny blankets, still and peaceful.",
        "Warm winter sun shining through a window onto a wall, a lady beetle waking up and yawning.",
        "Many lady beetles crawling onto the inside of a frosty window, looking out at the snow.",
        "A human finger about to squish {B}, the beetle looking alarmed, a big red X between them.",
        "{B} with tiny yellow drops at its leg joints and wavy green smell lines, comic.",
        "{H} vacuuming lady beetles gently from a window frame with a hose.",
        "{H} opening a window in spring and lady beetles flying out into a blooming garden.",
        "{H} sealing a gap around a window with a caulk gun while lady beetles watch from outside, autumn leaves.",
    ],
    "chinche_invierno_short": [
        "{B} landing on the plaid flannel sleeve of {H} under a glowing reading lamp at night, big and close.",
        "{H} looking down at {B} on his sleeve, thinking, a winter window behind him.",
        "{B} asleep inside a wall space under a tiny blanket, snow outside a small window.",
        "A vertical cutaway of a house wall with many stink bugs sleeping in the wall spaces for months, calm.",
        "{B} sleeping next to an untouched tiny plate of food and a piece of wood, peaceful.",
        "A cartoon man with a round white head, dot eyes and a cardigan standing next to a towering pile of jars full of stink bugs in a living room, amazed, every jar plain and unlabeled.",
        "The same man sitting exhausted on the floor surrounded by jars of stink bugs, every jar plain and unlabeled.",
        "A human hand squeezing {B}, which releases a big puff of green cartoon smell cloud.",
        "A bunch of fresh green cilantro next to {B}, both with identical wavy smell lines.",
        "{H} biting a taco with cilantro and making a face like he tasted soap, little bubbles around his mouth.",
        "{H} recoiling from {B} with a horrified face, holding a cilantro leaf.",
        "{B} flying over a fence into a sunny orchard full of ripe apples and peaches, licking its lips.",
        "{H} lowering his tissue with a calm smile, a big red X over the squish.",
        "{H} nudging {B} into a clear jar of soapy water with bubbles on top, the jar plain and unlabeled.",
    ],
    "hormigas_cocina_short": [
        "{H} pressing her thumb down on a line of tiny ants on a kitchen counter with a paper towel, little dust puffs.",
        "A kitchen clock showing noon and the same neat line of ants marching back to a sugar bowl, {H} glaring.",
        "{B} sniffing a glowing dotted green scent trail on the counter, curious.",
        "Many tiny ants in orange delivery caps following a glowing green trail across the counter like a road.",
        "A big smartphone propped on the counter showing a simple map with a glowing route, ants on tiny scooters, the phone screen plain with no writing.",
        "A pink-gloved thumb squishing one tiny delivery ant while more scooters keep coming along the glowing route.",
        "The glowing route still shining on the counter, more delivery ants arriving, unbothered.",
        "A vertical cutaway of a kitchen wall with a huge ant nest inside, a few ants on the counter at the top.",
        "A cartoon queen ant with a tiny golden crown sitting safely on a soft throne deep inside the wall, sipping tiny tea.",
        "{H} blasting the ant line with a can of bug spray, a big white cloud, the can plain and unlabeled.",
        "A crowd of worker ants and two queens carrying tiny suitcases out of a tunnel on moving day.",
        "Three small ant nests in a flower pot, under a fridge and behind a dishwasher, arrows between them.",
        "{H} wiping the glowing trail away with a soapy sponge and closing a sealed jar of sugar, the jar plain and unlabeled.",
        "Ants staring at a blank clean counter with question marks, {H} smiling with her arms crossed.",
    ],
    "telarana_rota_short": [
        "{H} sweeping a big round spider web off a porch at night with a broom, threads snapping, a porch light glowing.",
        "The same porch in the morning light with a perfect new round web between the post and the light, {H} in a bathrobe stunned.",
        "{H} scratching his head next to the new web, a big question mark above him.",
        "{B} dropping down on a thin silk safety line as a broom swooshes above it, motion lines.",
        "{B} peeking out of a crack in a wooden porch post at night, watching the front door close.",
        "The porch at night with the door closed and a light on inside, {B} climbing back out under the porch light.",
        "{B} spinning a new web at high speed under the porch light at night, motion lines, a tiny moon.",
        "A very long silk thread stretching down the porch steps and across the lawn, {B} holding the end proudly.",
        "{B} rolling up an old broken web like spaghetti and eating it with a tiny fork, satisfied.",
        "{B} with a glowing belly spinning new silk that sparkles, recycling, happy.",
        "A perfect new web glowing in the sunrise with {B} in the middle, proud.",
        "{B} carrying a tiny suitcase and a bindle away from a ruined web toward a bush, glancing back.",
        "{H} on a step stool swapping a white bulb for a warm yellow bulb in the porch lantern, the bulb plain and unlabeled.",
        "The porch lit by a warm yellow bulb with only one moth, {B} relaxing in a bush nearby, everyone calm.",
    ],
    "polilla_foco_short": [
        "{B} circling a glowing porch light with dizzy spiral eyes and a heart with a big red X next to it.",
        "{B} caught in a glowing circular orbit around a bulb like a tiny planet, worried face.",
        "A starry glowing night sky over a dark ancient forest of ferns, the sky the brightest thing.",
        "{B} flying level under a bright starry sky with its back toward the sky, a tiny arrow pointing up.",
        "{B} in a tiny airplane cockpit with an autopilot dial showing a level horizon, goggles on, relaxed.",
        "{B} flying next to a bright porch bulb that outshines the moon behind it.",
        "{B} flying in endless circles around a porch bulb with a circular motion trail, dizzy.",
        "{B} flipping upside down right above a glowing bulb, legs in the air, surprised.",
        "{B} exhausted at dawn, drooping wings, a little sweat drop, a tired face.",
        "{B} resting stiff on a pale bright porch wall at sunrise, in plain view, nervous.",
        "A cartoon robin and a small green lizard peeking around the corner of the wall, eyeing the moth.",
        "{H} on a step stool swapping a white bulb for a warm yellow bulb in the porch lantern, the bulb plain and unlabeled.",
        "{H} flipping the porch light switch off, and {B} flying happily toward the real full moon.",
    ],
    "arana_crias_short": [
        "{H} flipping on a garage light and spotting a big hairy spider in the middle of the concrete floor.",
        "Close-up of {B} with a strange lumpy texture on her back, wiggle lines, mysterious.",
        "{H} raising one big work boot over the spider, a dramatic shadow, then freezing.",
        "Extreme close-up of the lumps on the spider's back: dozens of tiny pale baby spiders with dot eyes looking up.",
        "{B} with dozens of tiny pale baby spiders piled on her back in layers, proud and smiling.",
        "{B} walking with babies piled on her back like a tiny pyramid, the babies shaking their heads at a tiny plate of food.",
        "Cutaway of a tiny baby spider with a little glowing yellow yolk in its belly like a lunchbox.",
        "The shadow of a boot over the garage floor from a distance, gentle, nothing graphic shown.",
        "Dozens of tiny baby spiders leaping off in every direction like popcorn, motion lines, comic.",
        "Tiny baby spiders scattering under a workbench and behind boxes, the boxes plain and unlabeled.",
        "{H} putting the boot down and thinking, a light bulb idea above his head.",
        "{H} carrying a clear bowl over a piece of cardboard out into a backyard garden at sunset, {B} and her babies riding inside and waving.",
    ],
}


def cargar(v):
    sp = importlib.util.spec_from_file_location("g_" + v, os.path.join(AQUI, v, "guion.py"))
    g = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(g)
    return g


v = sys.argv[1]
g = cargar(v)
F = g.FICHA
P = F["personajes"]
alias = {"H": P.get("human", "")}
alias["B"] = next(t for k, t in P.items() if k != "human")
lista = ESC[v]
bs = json.load(open(os.path.join(AQUI, v, "beats.json"), encoding="utf-8"))
assert len(bs) == len(lista), (len(bs), len(lista))
out = {b["id"]: F["estilo"] + ". " + t.format(**alias) + " " + F["cierre"] for b, t in zip(bs, lista)}
json.dump(out, open(os.path.join(AQUI, v, "prompts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(v, len(out), "prompts", sum(len(x) for x in out.values()))
