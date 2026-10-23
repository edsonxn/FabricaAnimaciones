# -*- coding: utf-8 -*-
"""Prompts de Flow de tequisquiapan (kit de historia_aguascalientes) (pegatinas con la referencia flow/ref_cronopapel.jpg como ingrediente).
python flow/prompts.py → flow/prompts.json y flow/_lote.js (para pegar en la página de Flow)."""
import json
import os

E = ("Use the attached reference image ONLY as the art style guide and copy its drawing style exactly: crude naive marker doodles, "
     "thick wobbly black outlines of uneven width drawn by hand, very simple geometric shapes (rectangles, circles, stick-like legs), "
     "almost no detail, round heads with two tiny dot eyes, a simple curved smile and pink cheek dots, flat muted fills (ochre, terracotta, "
     "cream, sage green, dusty blue, brick red, brown) covered with sparse white diagonal pencil-scribble streaks, like a child's colored "
     "marker drawing. Do NOT copy the objects of the reference, draw new ones. Never detailed, never realistic, never storybook-painted. ")
H = ("Sticker sheet on a plain flat pure white background (no paper texture, no sticker border, no shadows): 8 separate drawings "
     "arranged in two rows of four, evenly spaced with generous empty white space between them, never touching or overlapping: ")
GENTE = "Full body standing, front view, all the same height, big round heads and small boxy bodies. "
C = " No text, no letters, no numbers, no labels, no watermark."
CIC = ("Animation sprite sheet on a plain flat pure white background (no paper texture, no sticker border, no shadows): {q}. The SAME "
       "{w} drawn {n} times in a single horizontal row, strict side view facing right, full body, same size and same height, evenly spaced "
       "and not touching, each drawing a consecutive phase of one {p}; {k} identical in every drawing.")
P = {
    "01_origenes_hoja": H + "Before the Spanish, a valley of hot springs in central Mexico: 1) an Otomi man with white cotton clothes, a red sash and "
    "sandals; 2) an Otomi woman with an embroidered blouse and a blue rebozo carrying a clay water jar; 3) a Chichimec archer with a bow and a "
    "quiver; 4) two men bathing and talking in a steaming natural hot spring pool among rocks; 5) a small pile of white salt crystals in a clay "
    "bowl; 6) a paper cup of esquites (corn kernels) with a spoon, lime and red chili powder; 7) a nopal cactus and a mesquite tree; 8) hot "
    "spring water bubbling out of rocks with curls of steam." + C,
    "02_fundacion_hoja": H + "Founding of a small Otomi-Spanish town in 1551: 1) an Otomi chief with a feather headdress and a cape holding a "
    "wooden cross; 2) a Franciscan friar in a brown habit with a rope belt; 3) a big old mesquite tree with a twisted trunk; 4) a tall wooden "
    "cross planted in the ground with flowers; 5) an old charter scroll with a red wax seal; 6) a square stone water tank with an irrigation "
    "channel coming out of it; 7) an orchard of fruit trees with a little water canal; 8) a small colonial hacienda house with arches and a "
    "wooden gate." + C,
    "03_siglos_hoja": H + "A small Mexican town, 1897-1920: 1) a pink neoclassical parish church with one tall bell tower holding a big round "
    "clock; 2) an old tower clock mechanism with gears and three heavy iron weights hanging from chains; 3) a black steam locomotive puffing "
    "smoke; 4) a small yellow railway station building with a platform and a bench (no readable text); 5) a small stone dam with water spilling "
    "over it; 6) a wooden electric pole with wires and one glowing light bulb; 7) a 1920 state governor with a moustache, a dark suit and a "
    "rolled decree in his hand; 8) a revolutionary rebel on a galloping horse with a sombrero and cartridge belts." + C,
    "04_centro_hoja": H + "The 'geographic center of Mexico' monument and tourists: 1) a small stone monument in a plaza: a low round stone "
    "column with a flagpole and a Mexican flag on top; 2) Venustiano Carranza, an old man with a long white beard, round glasses and a khaki "
    "uniform; 3) a big red map pin; 4) a smiling tourist taking a selfie with a phone; 5) a magnifying glass over an old paper document; "
    "6) a compass rose; 7) a road sign post with one arrow pointing away (no readable text); 8) a family of tourists posing and waving." + C,
    "05_turismo_hoja": H + "Tourism in a Mexican town of hot springs, cheese and wine: 1) a 1950s family in a rounded vintage car with a suitcase "
    "on the roof; 2) a couple relaxing in a steaming thermal swimming pool; 3) a big wheel of cheese, a bottle of red wine and two glasses; 4) a "
    "fair stall with cheeses and wine under a striped awning; 5) an artisan sitting on a stool weaving a basket of thin wooden reeds; 6) a stack "
    "of woven reed baskets; 7) a glowing orange fire opal gemstone; 8) an opal miner with a helmet and a pickaxe." + C,
    "06_bernal_hoja": H + "The Pena de Bernal monolith and the water of the valley: 1) a huge tall rounded rock monolith with a tiny white "
    "village at its foot; 2) cross-section of the ground showing a dome of orange magma rising but staying underground; 3) rows of a vineyard "
    "with purple grapes; 4) a hiker with a backpack and a walking stick; 5) a tourist with a backpack holding an unfolded map; 6) a big sad "
    "blue water drop; 7) an old stone well with a rope and an empty bucket; 8) a dripping water tap." + C,
    "07_turista_camina": CIC.format(q="walk cycle of a simple smiling tourist doodle with a sun hat, a backpack and a camera hanging from his neck",
                                    w="tourist", n=8, p="walking step with stick-like legs",
                                    k="the hat, the backpack and the camera always the same") + C,
    "08_jinete_galope": CIC.format(q="gallop cycle of a simple revolutionary horseman doodle with a wide sombrero and cartridge belts riding a "
                                   "brown horse", w="horse and rider", n=6, p="gallop", k="the rider, the sombrero and the belts") + C,
}
D = os.path.dirname(os.path.abspath(__file__))
json.dump({k: E + v for k, v in P.items()}, open(os.path.join(D, "prompts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
js = ("window.__E=" + json.dumps(E) + ";window.__R=" + json.dumps(list(P.values()), ensure_ascii=False) + ";window.__K=" +
      json.dumps(list(P)) + ";window.__R.length")
open(os.path.join(D, "_lote.js"), "w", encoding="utf-8").write(js)
print(len(P), "prompts,", len(js), "caracteres de JS")
