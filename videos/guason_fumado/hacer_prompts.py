# -*- coding: utf-8 -*-
"""Escribe prompts.json: estilo fijo + escena (con la ficha de cada personaje la primera vez que aparece) + cierre.
Uso (desde la carpeta del video):  python hacer_prompts.py   y luego   python fab.py guason_fumado prompts"""
import json
import re

from guion import FICHA

SALA = "in a lazily scribbled gray warehouse interrogation room with one bare hanging light bulb"
ROTO = "in the same gray warehouse room, now full of smoke and rubble, with a huge jagged hole blown in the back wall"
E = {
    1: f"MURCI leans over PAYASO, who is tied to a wooden chair with rope {SALA}; MURCI jabs a giant fat index finger into his face and shouts with an enormous open mouth, spit flying.",
    2: f"Close-up of PAYASO tied to a chair {SALA}, smug, eyes closed, nose in the air, tongue sticking out, turning his head away; behind him MURCI fumes with steam coming out of his ears.",
    3: f"PAYASO tied to a chair {SALA} whistles and looks at the ceiling, bored; MURCI holds up a ridiculously huge ringing alarm clock next to his face, a vein popping on his forehead.",
    4: "Extreme close-up of PAYASO with a smug sideways grin, one eyebrow raised absurdly high above his head, half-closed eyes, plain pale yellow background.",
    5: f"PAYASO tied to a chair {SALA} laughs hysterically with his head thrown back, his mouth gigantic showing the uvula and crooked teeth, tears flying; tiny MURCI in the corner facepalms.",
    6: "Extreme close-up of the furious face of MURCI: teeth clenched and cracking, three throbbing veins, one eye twitching bigger than the other, face turning red, steam shooting from his pointy ears, plain red background with scribbled anger lines.",
    7: f"MURCI lifts PAYASO, chair and all, by the collar {SALA}; their noses squash together, MURCI glaring, PAYASO grinning nervously with sweat drops.",
    8: f"MURCI shakes PAYASO violently by the shoulders {SALA}, PAYASO's head wobbling as a blur with several faces; MURCI holds a crumpled paper with a crude stick-figure drawing of CHICO.",
    9: f"MURCI in dramatic shock {SALA}: both hands on his cheeks, jaw dropped all the way to the floor, eyes like dinner plates; PAYASO tied to the chair shrugs with a cheeky grin.",
    10: "Close-up of PAYASO with a deadpan confused face, one eye much bigger than the other, tiny mouth, a single huge sweat drop on his temple, plain light blue background.",
    11: "A rusty garbage dumpster in a scribbled alley; the skinny legs of CHICO stick straight out of the trash upside down, a banana peel on one foot, flies buzzing; in the foreground PAYASO points at it with his thumb, grinning.",
    12: f"MURCI kneels beside PAYASO tied to the chair {SALA}, one hand on his shoulder like a disappointed dad, with huge shiny sad puppy eyes and a trembling lip; PAYASO looks away bored.",
    13: f"PAYASO tied to the chair {SALA} blows a huge raspberry with his tongue out, a shower of spit hitting the face of MURCI, who stands frozen, dripping, with a dead-inside expression.",
    14: "MURCI walks carrying PAYASO under his arm like a sack of potatoes, PAYASO limp and bored with his chin in his hand, on an empty scribbled night street with a crooked moon.",
    15: "MURCI kicks PAYASO in the butt, sending him flying in an arc through the air toward a crooked spooky asylum building with barred windows on a hill, lightning bolt behind it; PAYASO waves goodbye happily in mid-air.",
    16: f"PAYASO runs away {SALA} with his legs drawn as a spinning wheel blur, sticking out his tongue and pulling down one eyelid, broken ropes flying off; MURCI chases him with stiff robot arms stretched forward.",
    17: "MURCI drawn as a goofy bat demon with tiny useless bat wings and little horns, rising out of badly drawn orange cartoon flames with a grumpy face; PAYASO points at him and laughs, plain dark red background.",
    18: "MURCI in a ridiculous heroic pose on a rooftop: one fist raised to the sky, the other hand holding a giant magnifying glass that enlarges one eye, cape flapping, sparkly determined eyes, a crooked city skyline scribbled behind.",
    19: f"MURCI frantically wraps PAYASO in an absurd amount of rope {SALA}, turning him into a fat cocoon with only his grinning head sticking out; MURCI runs around him as a blur with the rope.",
    20: f"PAYASO, wrapped in a rope cocoon, hangs upside down from the ceiling {SALA}, his green hair hanging down, still grinning; MURCI stands next to him dusting off his hands, proud, chin up.",
    21: f"PAYASO hanging upside down in a rope cocoon {SALA} wiggles like a worm; one skinny arm has slipped out holding tiny scissors, he winks at the viewer.",
    22: f"PAYASO stands free next to a pile of cut rope {SALA}, taking a theatrical bow like a magician with one arm stretched out; MURCI behind him stares with his jaw open.",
    23: "A grumpy teenage boy sidekick in a red hoodie and a black domino mask storms out through a door carrying a suitcase; MURCI, left behind, wears a safari hat over his cowl and holds a butterfly net and binoculars, looking confused, plain beige room.",
    24: "The teenage boy sidekick in a red hoodie and a black domino mask tiptoes behind MURCI raising a gigantic wooden cartoon mallet over his head with an evil grin; MURCI looks the other way, clueless, plain beige room.",
    25: "MURCI sits dizzy on the floor with an enormous throbbing red lump growing out of his cowl, crossed eyes, little yellow stars and birds circling his head; behind him the boy sidekick in a red hoodie whistles innocently hiding a mallet behind his back.",
    26: f"PAYASO {SALA} waves one hand dismissively with a bored face while picking his nose with the other hand, eyes half closed; MURCI stands with crossed arms.",
    27: "Extreme close-up of PAYASO far too close to the camera, bulging eyes with hypnotic spirals, a creepy stretched grin, both index fingers twirling beside his temples, plain purple background with scribbled swirls.",
    28: f"PAYASO and MURCI {SALA} both freeze and look back over their shoulders as the back wall begins to crack with bright orange light bursting through the cracks, small rocks flying.",
    29: "A gigantic badly drawn cartoon explosion with an orange and yellow mushroom cloud, jagged star shapes and flying bricks behind PAYASO; PAYASO stands in front with his hair blown forward and a calm knowing smile.",
    30: f"Side by side {ROTO}: PAYASO smirks and winks with a knowing face, while MURCI, covered in soot with his cowl ears bent, scratches his head completely clueless with empty dot eyes.",
    31: f"MURCI jumps straight up in fright {ROTO}: cape standing straight up, arms and legs stiff like a starfish, eyes popping out of his mask on stalks, teeth chattering.",
    32: f"MURCI points an accusing giant finger at PAYASO through the smoke {ROTO}, shouting with a huge mouth; PAYASO covered in dust looks left and right.",
    33: f"PAYASO raises both open hands innocently {ROTO}, a crooked golden halo floating over his head, angelic fake smile, big sweat drops; MURCI glares at him unconvinced.",
    34: f"PAYASO pulls both empty trouser pockets inside out to show he has nothing {ROTO}; behind them, inside the smoke of the hole, a huge dark silhouette with two glowing red eyes appears.",
    35: f"SUPER floats in through the jagged hole {ROTO}, fists clenched, cape flying, red glowing furious eyes, tiny head on a gigantic chest; MURCI turns to PAYASO with a shocked face.",
    36: f"PAYASO shakes his head so fast it is drawn as five blurred heads {ROTO}, terrified, crossing his arms in an X; the shadow of SUPER falls over him.",
    37: f"MURCI stands between SUPER and PAYASO {ROTO} with his arms spread wide like a goalkeeper, sweating; SUPER reaches over him with one gigantic arm toward PAYASO, who hides behind MURCI.",
    38: f"SUPER holds PAYASO up in the air by the collar with one hand {ROTO}; PAYASO's legs dangle and kick, both hands up pleading with a nervous grin; small MURCI hangs from SUPER's red cape pulling it.",
    39: "Close-up of MURCI trying to look gentle and understanding: an awkward forced smile, one hand raised softly, eyebrows tilted with pity, sweat on his chin, plain gray background.",
    40: f"MURCI holds up a framed photo with crude stick figures of a woman and a baby toward SUPER {ROTO}; SUPER cries two waterfalls of tears while still looking furious, lip trembling.",
    41: f"MURCI on his knees begging {ROTO}, hands clasped, with gigantic watery sparkling eyes and a quivering lip, looking up at the towering legs of SUPER.",
    42: "Extreme close-up of the furious face of SUPER: glowing red eyes, a giant throbbing vein on his tiny forehead, nostrils blowing steam like a bull, teeth grinding, plain dark blue background with red anger lines.",
    43: f"SUPER pulls back his flat hand like a karate chop aimed at the chest of PAYASO {ROTO}; PAYASO screams with his tongue waving, MURCI covers his eyes with both hands but peeks through his fingers.",
    44: "SUPER slowly raises one single index finger with an evil mischievous grin, the fingertip gleaming with a little sparkle; in front of him PAYASO, seen from behind, looks back over his shoulder with a nervous sweating face, plain pale background.",
    45: "Extreme close-up of the face of PAYASO frozen in total shock: both eyes popping out of their sockets, mouth a perfect small O, green hair standing straight up like spikes, a single tear; blurry SUPER behind him grinning; a big yellow comic impact star covers the bottom of the frame.",
    46: "PAYASO breaks the fourth wall, looking straight at the camera, offended, shaking a crumpled stack of blank script pages with one hand and pointing at it with the other; a boom microphone and a film light poke into the top of the frame, plain gray studio background.",
    47: "Close-up of MURCI horrified, pulling the skin of his own face down with both hands so his eyes and mouth stretch into long droopy ovals, plain greenish background.",
    48: f"MURCI throws up a rainbow into a metal bucket {ROTO}, on his knees, face green; far in the background SUPER holds up stiff PAYASO, with a big yellow comic impact star between them.",
    49: f"MURCI pulls the red cape of SUPER with all his strength {ROTO}, leaning back at an impossible angle, feet skidding and leaving grooves in the floor, teeth clenched; SUPER does not move at all, like a statue.",
    50: "SUPER in a glorious flashback as a noble hero: standing on a cloud with hands on his hips and a kind smile, a golden sun halo with rays behind his tiny head, white doves and sparkles around him, pastel sky.",
    51: "MURCI points a disappointed finger with a judging frown; in front of him SUPER has a wicked crooked grin, a dark purple aura and flames around him, one eyebrow raised, plain dark background.",
    52: "MURCI makes a desperate time-out T sign with both hands, eyes shut tight, sweat flying, face cringing; behind him PAYASO stiff as a wooden board with a traumatized thousand-yard stare, plain gray background.",
    53: f"MURCI lies flat on the floor hugging one red boot of SUPER and is being dragged along {ROTO}, crying a puddle of tears, leaving a trail on the dusty floor.",
    54: "MURCI screams at the sky covering his eyes with both hands, smoke and little flames coming out between his fingers, knees bent, cape twisted, plain orange background with scribbled rays.",
    55: f"SUPER lifts PAYASO high above his head with one straight arm like a waiter holding a tray {ROTO}, flexing his other bicep and smiling proudly; PAYASO is stiff as a wooden board, with a traumatized face; a big yellow comic impact star where the hand holds him.",
    56: "Wide shot: SUPER flies away into an orange sunset through a hole in the roof, carrying stiff PAYASO above his head with one arm; below, in the ruined gray warehouse, tiny MURCI kneels with both arms raised to the sky, screaming.",
}

beats = json.load(open("beats.json", encoding="utf-8"))
assert len(beats) == len(E), (len(beats), len(E))
out = {}
for k, b in enumerate(beats):
    txt, vistos = E[k + 1], set()

    def ficha(m):
        n = m.group(1)
        if n in vistos:
            return n
        vistos.add(n)
        return FICHA["personajes"][n]
    txt = re.sub(r"\b(MURCI|PAYASO|SUPER|CHICO)\b", ficha, txt)
    out[b["id"]] = f"{FICHA['estilo']}. {txt} {FICHA['cierre']}"
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts ·", max(len(v) for v in out.values()), "caracteres el más largo")
