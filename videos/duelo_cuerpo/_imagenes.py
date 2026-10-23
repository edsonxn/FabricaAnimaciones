# -*- coding: utf-8 -*-
"""Lista ORDENADA de imágenes: una por beat desde scene-010 hasta scene-074 (65). El número del comentario es el beat."""
from guion import FICHA

SE = FICHA["personajes"]["la señora"]
ES = FICHA["personajes"]["el esposo"]
NEON = "glowing yellow neon"
HEART = "an anatomical human heart drawn in thin white engraving lines, no labels"
BRAIN = "a white line-art human brain seen from the side, drawn in fine engraving lines, no labels"
MAPA = "an old hand-drawn paper town map with winding streets, little houses, trees and a plaza, drawn in white lines"
OFRENDA = ("a Mexican Day of the Dead altar (ofrenda) with three steps, papel picado banners, marigold flowers, pan de muerto, "
           "a plate of food, sugar skulls and candles")

I = [
    f"close-up of a long wooden shelf in an old Mexican kitchen with clay pots, jars and hanging utensils, on it a row of seven small clay oil lamps whose flames get smaller from left to right, the first flame {NEON}",  # 010
    f"an old magnifying glass hovering over a small heart lying on a dark velvet cloth, the rim of the magnifying glass {NEON}",  # 011
    f"{HEART}, a jagged crack running down its middle {NEON}",  # 012
    f"a giant ocean wave curling toward a small heart standing alone like a rock on a beach, the crest of the wave {NEON}",  # 013
    f"{HEART}, its lower tip swollen round like a balloon while the top stays narrow, the swollen tip {NEON}",  # 014
    f"a small Japanese fishing harbor at dawn with wooden boats, fishermen mending nets and a stack of round clay pots on the pier, one pot {NEON}",  # 015
    f"a round-bottomed clay octopus trap pot with a narrow neck tied to a rope on the sea floor, a small octopus peeking out of it, the pot {NEON}",  # 016
    f"{SE} standing in her kitchen pressing both hands on her chest, mouth open, breathing hard, a small heart shape {NEON} on her chest",  # 017
    f"a row of ten simple stick figures standing side by side, nine of them older women wearing shawls and one older man with a hat, a tiny heart {NEON} on each of the nine women",  # 018
    f"three older women friends wearing shawls chatting on a bench in a Mexican town plaza with a bandstand kiosk and trees, a small heart {NEON} on the chest of the woman in the middle",  # 019
    f"{HEART} back in its normal shape, beside it a faint dotted outline of the swollen balloon shape it had before, the heart {NEON}",  # 020
    f"the emergency entrance of a hospital at night with an ambulance parked outside and automatic glass doors, a simple cross-shaped sign above the door {NEON}",  # 021
    f"a quiet bedroom at night seen from the doorway, a window with a crescent moon, an old wall calendar with blank pages, the moon {NEON}",  # 022
    f"{SE} lying awake in bed at night staring at the ceiling, on the nightstand an old twin-bell alarm clock still trembling as if ringing, the alarm bells {NEON}",  # 023
    f"{SE} sitting on the edge of her bed in the dark before dawn with slippers on her feet, shoulders slumped, a small bedside clock without numbers {NEON}",  # 024
    f"an open refrigerator seen from the front with a milk bottle, eggs and vegetables, and a bunch of house keys left on the middle shelf, the keys {NEON}",  # 025
    f"{SE} walking slowly through a thick fog on a cobblestone street, the houses barely visible, a small lantern in her hand {NEON}",  # 026
    f"an old castle wall at night with the gate half open and two guards asleep leaning on their spears, a torch on the wall {NEON}",  # 027
    f"an English town street with red-brick terraced houses and a lamppost, two groups of older people sitting on benches facing each other, a researcher with a clipboard between them, the clipboard {NEON}",  # 028
    f"a circular microscope view of round white blood cells with lobed nuclei floating among red blood cells, one white blood cell {NEON}",  # 029
    f"a tired little round white blood cell drawn as a tiny knight with a drooping sword facing a crowd of rod-shaped bacteria, the knight's sword {NEON}",  # 030
    f"an old brass balance scale tipped heavily to one side, the heavy pan holding a large droplet {NEON}, the light pan almost empty",  # 031
    f"{SE} sick in bed under a thick blanket with a cup of tea, a box of tissues and a thermometer on the nightstand, the thermometer {NEON}",  # 032
    f"an old night watchman asleep sitting against the wall of a lighthouse at dawn, his lantern {NEON} resting beside him",  # 033
    f"an old empty movie theater with rows of velvet seats, the beam of light from the projector {NEON} falling on a blank screen",  # 034
    f"{SE} at a busy Mexican street market turning her head quickly toward the back of a man with a hat walking away in the crowd, the outline of the man {NEON}",  # 035
    f"a small kitchen table set for two with two plates, two cups and two chairs, one chair empty, the empty plate {NEON}",  # 036
    f"{SE} looking at her own reflection in an old oval mirror with a calm tender expression, a small heart {NEON} on the chest of her reflection",  # 037
    f"two hands unfolding {MAPA} on a wooden table, one little house on the map {NEON}",  # 038
    f"{BRAIN}, inside it a tiny town map with winding streets and little houses, one little house {NEON} with a pin",  # 039
    f"the front door of a small house in the evening, a man's hat hanging on a hook beside the door and a dinner table set beyond it, the hat {NEON}",  # 040
    f"a hand holding a pencil slowly redrawing the streets of {MAPA}, the tip of the pencil {NEON}",  # 041
    f"{MAPA} caught and crumpled between the teeth of big old iron gears that have jammed, one gear {NEON}",  # 042
    f"an Arizona desert landscape with tall saguaro cacti, mountains and a university building with a dome in the distance, the sun {NEON}",  # 043
    f"a framed photograph standing on a lace tablecloth showing {ES}, the photo frame {NEON}",  # 044
    f"{BRAIN}, one small spot deep inside it near the base {NEON}, beside the brain a slice of cake and a cup of hot chocolate drawn in white lines",  # 045
    f"a lighthouse at night on a rocky coast sweeping its long beam across a dark sea as if searching, the beam {NEON}",  # 046
    f"a lone small figure kneeling in a vast desert reaching out toward an old stone well in the distance, the well {NEON}",  # 047
    f"one large tree drawn across four seasons from left to right, bare winter branches turning into spring leaves, one new bud {NEON}",  # 048
    f"close-up of a birthday cake with lit candles on a lace tablecloth in a family dining room with framed photos on the wall and one empty chair at the table, the candle flames {NEON}",  # 049
    f"an old wooden radio on a kitchen shelf playing music, small musical notes {NEON} floating out of it",  # 050
    f"{SE} laughing with three friends around a table full of food and cups of coffee, a small heart {NEON} on her chest",  # 051
    f"medium close-up from the knees up of {SE} sitting still in an armchair in a dim living room with closed curtains, dusty shelves and a stopped wall clock, a small dim heart {NEON} on her chest",  # 052
    f"a heavy iron anchor chained to the leg of an old armchair in an empty room, the chain {NEON}",  # 053
    f"a thick medical book lying open on a doctor's desk beside a stethoscope and a pair of glasses, the page edges {NEON}",  # 054
    f"{SE} sitting in a cozy office across from a kind older therapist in an armchair, holding a framed photograph on her lap, the photograph {NEON}",  # 055
    f"a sunrise over the flat rooftops of a Mexican town with water tanks, clotheslines and a church dome, the rising sun {NEON}",  # 056
    f"three simple objects on a wooden table: a steaming bowl of soup, an old alarm clock and a pair of walking shoes, the steam of the soup {NEON}",  # 057
    f"{SE} sitting at her kitchen table eating a steaming bowl of soup with a spoon, the steam {NEON}",  # 058
    f"{SE} walking along a path in a sunny park with tall trees, a fountain and pigeons, the sun {NEON} in the sky",  # 059
    f"an old alarm bell resting quietly on a table beside a small white flag of peace, the bell glowing softly {NEON}",  # 060
    f"{SE} and an old friend sitting together on a bench, carrying a heavy basket between them, the handle of the basket {NEON}",  # 061
    f"{SE} and her grown son sitting on a sofa looking at an open photo album together, one photograph in the album {NEON}",  # 062
    f"{MAPA} with a new road drawn around one little house that stays in place, the little house {NEON}",  # 063
    f"medium close-up from the waist up of {SE} standing in her kitchen at dawn beside the window, eyes closed and one hand on her chest as if listening to it, a small heart {NEON} under her hand",  # 064
    f"{HEART} beside a long irregular heartbeat line like a hospital monitor trace, the heartbeat line {NEON}",  # 065
    f"an ambulance driving fast down a town street at night, its roof siren light {NEON}",  # 066
    f"{OFRENDA} in a family living room, the candle flames {NEON}",  # 067
    f"close-up of the ofrenda: a framed photograph of {ES}, a plate of mole, pan de muerto, an old guitar and marigolds, the photo frame {NEON}",  # 068
    f"family members of all ages scattering marigold petals on the floor to make a path toward the ofrenda, the path of petals {NEON}",  # 069
    f"{SE} and her family sitting around the ofrenda at night telling stories and smiling, one tall candle {NEON}",  # 070
    f"medium close-up from the waist up of {SE} in her living room beside the ofrenda with candles and marigolds, hugging a framed photograph to her chest with her eyes closed, a small heart {NEON} on her chest",  # 071
    f"a huge heart outline {NEON} filling the night sky above a small house, {SE} standing tiny at the door looking up at it",  # 072
    f"a long table in the dark covered with many small lit candles in a row, each candle flame {NEON}",  # 073
    f"a wide view of {OFRENDA} in a dark room with an empty chair beside it, a single candle {NEON}",  # 074
]
