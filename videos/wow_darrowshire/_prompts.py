# -*- coding: utf-8 -*-
"""Escribe prompts.json (escenarios + hojas de Flow) con la FICHA de guion.py. Ejecutar desde la carpeta del video.
Tanda 1 (20-oct-2026): lo que piden gancho, pueblo, plaga, asedio y el arranque de horgus (0:00-3:00). Las tandas siguientes
añaden claves nuevas (numeración 40+ para escenarios y 70+ para hojas) sin tocar estas."""
import json
import guion

E = guion.FICHA["estilo"] + ". "
C = guion.FICHA["cierre"]
VACIO = " Strong depth: foreground, midground and background layers. Open empty ground across the lower third. No people, no animals."
INTERIOR = " Strong depth: foreground, midground and background layers. Open empty floor across the lower third. No people."
FILA = (" full body, evenly spaced in one row with generous empty white space between them, never touching or overlapping")
HOJA = " on a plain flat pure white background"
NOSOMBRA = " No ground, no cast shadows."
LUGAR = ("Darrowshire, a humble medieval human farming village of the southern hills of Lordaeron (World of Warcraft): half-timbered "
         "cottages with steep dark slate roofs, stone chimneys, wooden fences, a small chapel")

ESC = {
    "01_posada_camino": "Wide background at night of a lonely two-story medieval roadside inn on the dirt road to the walled city of "
        "Stratholme (World of Warcraft), half-timbered walls, a hanging wooden sign with no letters, ONE warm candle-lit window on the "
        "upper floor, the distant pale towers and walls of Stratholme on the horizon under a cold moon, bare trees, a wooden cart "
        "by the road." + VACIO,
    "02_posada_cuarto": "Wide background of the upper-floor bedroom of a medieval roadside inn at night: low wooden beams, a simple "
        "wooden bed with a wool blanket on the right, a small rag rug on the wooden floor, a chest, a stool with a single burning "
        "candle casting warm orange light, a small window with cold blue moonlight. Open empty floor across the lower third, the bed "
        "empty. No people.",
    "03_peste_este": "Wide background of the Eastern Plaguelands of World of Warcraft at dusk: rotting hills, twisted dead black trees, "
        "sickly yellow-green grass, a ruined stone watchtower, thick low plague-green fog in the hollows, a winding empty dirt road "
        "going down into a valley, sickly green-grey sky." + VACIO,
    "04_ruinas_noche": "Wide background at night of the ruins of " + LUGAR + ": burnt roofless cottages with broken black beams, a "
        "collapsed chapel tower, broken fences, dead trees, pale green ghostly mist creeping between the ruins, a cold full moon "
        "behind thin clouds." + VACIO,
    "05_ruinas_puerta": "Close wide background at night: the burnt doorway and broken front wall of a ruined half-timbered cottage in "
        "the ruins of Darrowshire, a fallen roof beam, ash and broken pottery on the ground, faint ghostly blue-green mist, cold "
        "moonlight from the left. Open empty ground across the lower third in front of the doorway. No people, no animals.",
    "06_ruinas_camino": "Wide background at dusk: a dirt road that passes beside the ruins of Darrowshire without stopping, the ruined "
        "village on a slope on the right, a weathered wooden signpost with no letters at a fork, crows on a dead tree, a grey-green "
        "Plaguelands sky." + VACIO,
    "07_villa_lago": "Wide background of " + LUGAR + " ALIVE and peaceful on a bright autumn morning, before the war: smoke rising from "
        "the chimneys, orange and golden autumn trees, the wide blue lake Darrowmere behind the village with a small island and a "
        "distant castle on it, gentle green hills. Same art style but warm and hopeful colours: soft gold, warm green, clear blue." + VACIO,
    "08_villa_calle": "Wide background of the main street of " + LUGAR + " on a sunny autumn day before the war: cottages on both "
        "sides, a well, barrels and baskets of apples, flower boxes, a blacksmith's open forge glowing, laundry hanging between "
        "houses. Warm hopeful colours." + VACIO,
    "09_casa_rutagrana": "Wide background of the house of the village militia captain in Darrowshire on a sunny autumn afternoon: a "
        "sturdy two-story half-timbered cottage with a small fenced yard, a wooden practice dummy and a weapon rack with spears in "
        "the yard, an apple tree, the lake shimmering behind. Warm hopeful colours." + VACIO,
    "10_casa_interior": "Wide background inside a cosy medieval family cottage on an autumn afternoon: a stone hearth with a "
        "crackling fire and a cooking pot, a long wooden table with bread and cups, a captain's sword and round shield hanging over "
        "the fireplace, dried herbs, warm window light." + INTERIOR,
    "11_pergamino_mesa": "Wide background of an old empty parchment sheet pinned flat on a dark wooden table, seen from straight "
        "above, filling most of the frame, stained and worn edges, a guttering candle and a quill in one corner, dark shadows at "
        "the borders. The parchment is completely BLANK.",
    "12_plaza_tarde": "Wide background of the small village square of " + LUGAR + " at golden sunset: a stone well in the center, a "
        "tall oak tree, the chapel, long warm shadows, the sky fading from gold to dusky violet, the first cold blue creeping in at "
        "the edges." + VACIO,
    "13_graneros_andorhal": "Wide background of the great granaries of the town of Andorhal (World of Warcraft) on an overcast day: "
        "huge wooden barns and grain silos, stacked burlap grain sacks, wooden carts loaded with sacks leaving on the road, a faint "
        "sickly green glow leaking from inside one open barn door, grey heavy clouds." + VACIO,
    "14_casa_enfermo": "Wide background of a dim peasant bedroom during the plague: a straw bed with rumpled stained sheets on the "
        "right, a bowl of grain porridge on a stool, a bucket, a single dying candle, sickly green light coming through the shutters, "
        "deep shadows." + INTERIOR,
    "15_mapa_lordaeron": "Wide background: an old hand-painted fantasy parchment map of the northern human kingdom of Lordaeron "
        "(World of Warcraft) seen from straight above: the coastline and the sea on the west, mountain ranges drawn as little "
        "peaks, forests, rivers, a large lake in the south-east, small drawn castles and towns as dots, compass rose, aged "
        "parchment with burnt edges. Absolutely NO text, no labels, no names on the map.",
    "16_stratholme_arde": "Wide background at night: the great walled city of Stratholme (World of Warcraft) burning, tall gothic "
        "towers and cathedral spires silhouetted against enormous orange flames and black smoke, the city gate, embers in the sky, "
        "a dark hill in the foreground." + VACIO,
    "17_puerta_pueblo": "Wide background at cold dusk: the wooden palisade gate at the edge of Darrowshire, open, looking OUT onto an "
        "empty road that winds away through grey hills toward a darkening horizon, a lone lantern on the gate post, a crow on the "
        "fence, the first plague-green tint in the sky." + VACIO,
    "18_plaza_reunion": "Wide background of the village square of Darrowshire on a grey overcast day before a battle: a stone well, "
        "the chapel with its bell tower, a wooden platform with a Lordaeron banner (blue and gold, no letters), pitchforks and "
        "spears leaning on barrels, cold wind." + VACIO,
    "19_barricadas": "Wide background of the main street of Darrowshire at cold dusk turned into a defensive line: overturned carts, "
        "barrels, wooden barricades with sharpened stakes across the street, burning braziers, shuttered windows, banners of "
        "Lordaeron and of the Knights of the Silver Hand (no letters), the street empty." + VACIO,
    "20_colinas_noche": "Wide background at night: the dark hills above Darrowshire, dead twisted trees on the ridges, a narrow path "
        "coming down the slope toward the viewer, thick plague-green fog flowing down from the hilltops, a sickly moon, the faint "
        "lights of the village at the bottom of the frame." + VACIO,
    "21_barricada_noche": "Wide background at night: close view of a village barricade of carts, barrels and sharpened stakes lit "
        "by torches and a burning brazier, the dark street of half-timbered houses behind it, green fog beyond the barricade, "
        "sparks in the air." + VACIO,
    "22_alba_pueblo": "Wide background of " + LUGAR + " at a cold misty dawn after a night battle: thin smoke rising from a few "
        "chimneys, a broken barricade in the street, scattered arrows, a pale pink-grey sky with the first sunlight touching the "
        "chapel tower." + VACIO,
    "23_casa_marlene": "Wide background at dusk: the small half-timbered cottage of an aunt at the edge of Darrowshire, a warm lit "
        "window, a wooden front door with a small porch, a flower box, the lane empty, the first green fog in the distance, cold "
        "blue light." + VACIO,
    "24_escondite": "Wide background at night inside a small cottage bedroom: a big wooden wardrobe with one door slightly open "
        "showing darkness inside, a bed with a heavy quilt hanging to the floor, a child's small chair, a single candle on the "
        "floor, cold moonlight through the shutters, deep blue darkness." + INTERIOR,
}

HOJAS = {
    "50_pamela_hoja": "Character model sheet" + HOJA + ": Pamela Redpath, a little human girl of about 7 from World of Warcraft, "
        "freckled pale face, long ginger-red hair in two side ponytails, simple brown peasant dress with a cream-white apron, "
        "barefoot, holding a small handmade rag doll with button eyes. The SAME girl drawn 6 times," + FILA + ": sitting on the "
        "floor playing with two rag dolls; standing hugging her doll; waving hello with a shy smile; crouching hidden, hugging her "
        "doll, scared; standing looking up sad and lonely; walking holding her doll by the hand." + NOSOMBRA,
    "51_joseph_hoja": "Character model sheet" + HOJA + ": Captain Joseph Redpath of World of Warcraft, a broad human man of about 40, "
        "short brown hair and a thick brown beard, steel breastplate over a red-brown gambeson, a captain's blue and gold sash, a "
        "longsword and a round wooden shield. The SAME man drawn 6 times," + FILA + ": lying asleep on his back, side view, arms "
        "relaxed; standing proud with hands on his sword hilt; kneeling on one knee talking gently to a child at his side; raising "
        "his sword high and shouting a rallying cry; pointing forward giving orders; walking in full armour, side view facing "
        "right." + NOSOMBRA,
    "52_familia_hoja": "Character sheet" + HOJA + ": members of the Redpath family of World of Warcraft," + FILA + ": Jessica, a "
        "teenage girl of 16 with long red hair in a braid and a green travelling dress; aunt Marlene, a kind blonde woman of about "
        "35 in a long white dress and an orange shawl, standing with her hands clasped; aunt Marlene kneeling with her arms open; "
        "uncle Carlin, a bald man of about 45 with a short beard in a dark tabard with a silver sun emblem and grey armour, holding "
        "a sword; Jessica waving goodbye; Carlin with his arms crossed." + NOSOMBRA,
    "53_aldeanos_hoja": "Character sheet" + HOJA + ": 6 different medieval peasants of a human village of Lordaeron," + FILA + ": "
        "a farmer carrying a sack of grain on his shoulder; a woman carrying a basket of apples; a burly blacksmith with a hammer; an "
        "old man leaning on a cane; a boy running with a stick; a man pulling a small handcart." + NOSOMBRA,
    "54_defensores_hoja": "Character sheet" + HOJA + ": 6 different defenders of a medieval village of Lordaeron (World of Warcraft), "
        + FILA + ": a Lordaeron footman in steel armour with a blue and gold tabard and a spear; a paladin of the Silver Hand in "
        "heavy silver and gold plate holding a glowing warhammer raised; a militia farmer with a pitchfork and a leather cap; an "
        "archer drawing a longbow; two militiamen carrying a heavy wooden plank together; a young militiaman with a torch and a "
        "short sword." + NOSOMBRA,
    "55_plaga_hoja": "Character sheet" + HOJA + ": the plague of the undead Scourge of World of Warcraft, 6 separate figures" + FILA +
        ": a sick peasant man lying in bed pale and sweating, side view; the same man rising as a grey rotting zombie with glowing "
        "green eyes; a shambling rotting zombie in torn peasant clothes; a burlap grain sack leaking glowing sickly green grain; a "
        "small wooden cart loaded with grain sacks; a plague rat." + NOSOMBRA,
    "56_esqueletos_hoja": "Character sheet" + HOJA + ": 6 different undead skeleton warriors of the Scourge of World of Warcraft, "
        + FILA + ": skeleton with a rusty sword and a broken shield; skeleton with an axe; skeleton archer; a crawling half "
        "skeleton; a skeleton falling apart, bones flying, struck down; a skeleton with a torn grey banner. Bones are yellowed "
        "ivory, never white, with faint green eye glow." + NOSOMBRA,
    "57_esqueleto_camina": "Animation sprite sheet" + HOJA + ": walk cycle of an undead skeleton warrior of World of Warcraft with a "
        "rusty sword, yellowed ivory bones, faint green eye glow, shambling. The SAME character drawn 8 times in a single horizontal "
        "row, strict side view facing right, full body, same size and same height, evenly spaced and not touching, each drawing a "
        "consecutive phase of one walking step." + NOSOMBRA,
    "58_necrofago_corre": "Animation sprite sheet" + HOJA + ": run cycle of a ghoul of the Scourge of World of Warcraft: hunched grey-"
        "green rotting flesh, long claws, exposed ribs, torn loincloth, glowing green eyes, running on legs and knuckles like a "
        "beast. The SAME creature drawn 8 times in a single horizontal row, strict side view facing right, full body, same size, "
        "evenly spaced and not touching, each drawing a consecutive phase of one running stride." + NOSOMBRA,
    "59_jinete_galope": "Animation sprite sheet" + HOJA + ": gallop cycle of a World of Warcraft adventurer in plate armour with a "
        "red cloak riding a brown horse. The SAME horse and rider drawn 6 times in a single horizontal row, strict side view facing "
        "right, same size, evenly spaced and not touching, each drawing a consecutive phase of one gallop stride." + NOSOMBRA,
    "60_cuervos_aleteo": "Animation sprite sheet" + HOJA + ": a row of 6 drawings of the same black crow showing a wing-flap cycle, "
        "side view facing right, flying, evenly spaced and not touching." + NOSOMBRA,
    "61_utileria": "Prop sheet" + HOJA + ", 16 separate medieval objects evenly spaced in a 4x4 grid, never touching or "
        "overlapping: a small handmade rag doll with button eyes and red yarn hair; a burning candle on a clay holder; a wooden "
        "barricade of sharpened stakes; a burlap grain sack; a round wooden shield with a red-brown rim; a longsword; a pitchfork; a "
        "burning torch; an old leather-bound book; a hanging iron lantern glowing; a blue and gold Lordaeron banner on a pole with "
        "no letters; a burning iron brazier; a wooden water bucket; a broken wooden cart wheel; a small wooden toy horse; a bundle "
        "of arrows." + NOSOMBRA,
    "62_fx_hoja": "Effects sheet" + HOJA + ", 9 separate painted effects evenly spaced in a 3x3 grid, never touching: three different "
        "tongues of orange fire; two columns of dark grey smoke; one drifting patch of plague-green fog; one cloud of pale ghostly "
        "blue mist; a burst of orange embers; a splash of dark green ichor." + NOSOMBRA,
}

# ---------------------------------------------------------------- TANDA 2 (20-oct-2026): horgus (desde 3:06) … cierre
# Claves «T2_…» = van DESPUÉS de las 37 de la tanda 1 al ordenar (índices 37+ en _bundle.js).
RUINA = "the ruins of " + LUGAR + " years after the massacre: burnt roofless cottages, broken black beams, collapsed fences, dead trees"
ESC2 = {
    "T2_01_batalla_calle": "Wide background at night of the main street of Darrowshire during a losing battle: a broken barricade "
        "torn apart, overturned burning carts, scattered shields and spears on the ground, a cottage roof on fire, thick green fog "
        "pouring in from the end of the street, orange firelight against cold blue night." + VACIO,
    "T2_02_colina_refuerzos": "Wide background at night: the crest of a hill above Darrowshire where a road comes over the top, "
        "storm clouds tearing open behind the hill and a column of warm golden holy light breaking through, the burning village "
        "small in the valley below on the left." + VACIO,
    "T2_03_plaza_batalla": "Wide background at night of the village square of Darrowshire in the middle of a battle: the stone well, "
        "the chapel with its bell tower lit by fires, smashed barrels, a fallen Lordaeron banner (no letters), embers and smoke in "
        "the air, green fog at the edges." + VACIO,
    "T2_04_duelo_fuego": "Wide background at night: a burning wooden chapel collapsing in the background with huge orange flames and "
        "black smoke, a muddy open yard in front covered with ash and broken weapons, a single dead tree on the left, sparks "
        "falling." + VACIO,
    "T2_05_puerta_humo": "Wide background at night: the broken wooden palisade gate of Darrowshire seen from inside the village, "
        "the gate doors smashed open, a wall of thick black smoke and sickly green mist pouring through the gate from outside, a "
        "dead crow on a post, torches knocked down and burning on the ground." + VACIO,
    "T2_06_plaza_marduk": "Wide background at night of the village square of Darrowshire under a black sky with a swirling vortex "
        "of sickly green clouds above it, the chapel bell tower burning with eerie green flames, the stone well cracked, bodies "
        "hidden under fallen banners, cold green light everywhere." + VACIO,
    "T2_07_sombra_vortice": "Wide background at night: a narrow cobbled lane of Darrowshire swallowed by a creeping darkness, black "
        "smoke and shadow tendrils crawling over the walls of the cottages, a single green-glowing window, the moon hidden, deep "
        "dark violet and plague-green tones." + VACIO,
    "T2_08_calle_casas": "Wide background at night: a row of small half-timbered cottages of Darrowshire with closed wooden doors "
        "and shuttered windows with faint candlelight leaking through the cracks, green fog in the lane, a cat-sized dark gap "
        "under one door, the street empty and silent." + VACIO,
    "T2_09_pueblo_ardiendo": "Wide background at night seen from a dark hill: the whole village of Darrowshire burning in the "
        "valley below by the black lake, columns of smoke rising into a sickly green sky, the chapel tower in flames, dead trees "
        "silhouetted in the foreground." + VACIO,
    "T2_10_escritorio_vela": "Wide background seen from straight above: an old dark wooden writing desk at night, a large OPEN "
        "blank leather-bound book in the centre with empty cream pages, a guttering candle in a brass holder, a quill and an ink "
        "pot, a few dried autumn leaves, a small rag doll at the edge, deep shadows at the borders. The pages are completely BLANK.",
    "T2_11_camino_plaga": "Wide background at a grey sunless dawn: a muddy road leading away from the smoking ruins of Darrowshire "
        "toward dark hills, deep wheel ruts and footprints in the mud, broken spears stuck in the ground, a dead tree with crows, "
        "drifting green mist, cold ashen colours." + VACIO,
    "T2_12_granja_gahrron": "Wide background of a plague-ridden farmstead in the Western Plaguelands (World of Warcraft) on an "
        "overcast day: a large old rotting wooden barn with a sagging roof, a broken windmill, dead fields of sickly yellow grain, a "
        "rotten fence, a single tilted scarecrow, sickly green clouds." + VACIO,
    "T2_13_ruinas_plaza_noche": "Wide background at night of the square of " + RUINA + ", the stone well cracked and dry, a burnt "
        "chapel without roof, weeds and ash, pale green ghostly mist, a cold moon." + VACIO,
    "T2_14_ruinas_calle": "Wide background at night of a ruined street of " + RUINA + ", rubble and fallen beams across the "
        "street, a rusted helmet on the ground, blue-green ghostly mist flowing low between the ruins, faint will-o-wisp lights."
        + VACIO,
    "T2_15_ruinas_casa_pamela": "Wide background at night: a small ruined half-timbered cottage standing alone at the edge of the "
        "ruins of Darrowshire, half of its roof gone, one window frame still whole with a faint cold blue light inside, a small "
        "broken fence and a dead apple tree in the yard, mist, a pale moon." + VACIO,
    "T2_16_casa_marlene_ruina": "Wide background on an overcast grey day in the Western Plaguelands (World of Warcraft): a lonely "
        "abandoned farmhouse on a low hill south of the ruined town of Andorhal (broken towers on the horizon), boarded windows, an "
        "overgrown yard, a broken cart, dead trees, sickly green-grey sky." + VACIO,
    "T2_17_casa_marlene_dentro": "Wide background inside a dusty abandoned farmhouse: broken chairs, a table covered in dust and "
        "cobwebs, a cold fireplace full of ash, an old portrait frame on the wall with the picture faded to nothing, pale grey "
        "daylight through broken shutters, floating dust." + INTERIOR,
    "T2_18_casa_pamela_dentro": "Wide background inside a small ruined cottage at night: a broken wooden table with two little "
        "stools, a child's straw bed in the corner, burnt beams above showing the night sky, a small cracked window with cold "
        "moonlight, ash on the floor, a little shelf with a cracked teapot and cups." + INTERIOR,
    "T2_19_ruinas_vista_alta": "Wide background at dusk seen from high above at an angle: the whole ruined village of Darrowshire "
        "below, burnt roofless cottages and lanes, the dry square with the well, the chapel ruins, the black lake at the edge, "
        "pale green mist pooling in the lanes, like an old painted map." + " No people, no animals.",
    "T2_20_ventana_fria": "Wide background at night seen from inside a ruined child's room: a broken window frame with cracked glass "
        "covered in white frost patterns, cold blue moonlight falling across the dusty floor, frost on the window sill, a small "
        "empty chair, breath-cold blue darkness." + INTERIOR,
    "T2_21_cementerio_andorhal": "Wide background on an overcast day of the cemetery of the ruined town of Andorhal (World of "
        "Warcraft): rows of crooked gravestones and stone crosses, one taller weathered stone monument in the middle, an iron "
        "fence, dead trees, the broken towers of Andorhal behind, sickly green-grey sky and low mist." + VACIO,
    "T2_22_posada_andorhal": "Wide background inside a ruined inn of Andorhal: half-collapsed wooden beams, a long table piled with "
        "old books, scrolls, maps and a golden hourglass, a few candles, a bar counter with broken bottles, a fallen chandelier, "
        "warm candle light mixed with cold grey light from a hole in the roof." + INTERIOR,
    "T2_23_cavernas_tiempo": "Wide background inside the Caverns of Time (World of Warcraft): an immense sandy cavern with "
        "swirling golden sand in the air, giant floating hourglasses, glowing bronze-gold portals in the rock walls, sand dunes on "
        "the floor. Same art style but warm golden sand and bronze tones." + VACIO,
    "T2_24_ayuntamiento_andorhal": "Wide background inside the ruined town hall of Andorhal at night: tall bookshelves full of old "
        "books, some books floating in the air glowing with sickly purple-green light, scattered papers, a big cracked stone "
        "staircase, cobwebs, a broken stained-glass window." + INTERIOR,
    "T2_25_capilla_esperanza": "Wide background of Light's Hope Chapel (World of Warcraft) on a grey day: a white stone chapel with "
        "a tall bell tower on a hill in the Eastern Plaguelands, tents and banners of the Argent Dawn (no letters), a warm golden "
        "light glowing from the chapel door, the blighted land all around." + VACIO,
    "T2_26_lago_fantasmas": "Wide background at night: a dark still lake in the Western Plaguelands with dead reeds and black "
        "water, pale ghostly blue mist on the shore, broken weapons half sunk in the mud, a dead tree leaning over the water, the "
        "moon reflected." + VACIO,
    "T2_27_vega_amparo": "Wide background on a cold grey day of Hearthglen (World of Warcraft), the fortified town of the Scarlet "
        "Crusade: tall white stone walls and towers with crimson red banners (no letters), a heavy gate, a gallows, pine trees "
        "with snow patches, a stern cold atmosphere." + VACIO,
    "T2_28_plaza_fantasmas": "Wide background at night of the ruined square of Darrowshire glowing with ghostly light: the cracked "
        "well in the middle, broken barricades still standing like in the old battle, the burnt chapel, pale blue-green spectral "
        "light rising from the ground, swirling mist." + VACIO,
    "T2_29_ruinas_alba": "Wide background at a cold pale dawn of " + RUINA + ", the first grey light on the broken roofs, thin "
        "mist, silent and empty, a single crow on a beam." + VACIO,
    "T2_30_casa_pamela_alba": "Wide background at a soft pale dawn: a small ruined half-timbered cottage at the edge of "
        "Darrowshire, the door frame still standing, a broken fence, a dead apple tree, a faint warm light glowing inside the "
        "window, mist lifting, the first pink light in the sky." + VACIO,
    "T2_31_cofre_detras": "Wide background at dawn: the back yard behind a small ruined cottage, a crooked dead tree, a small "
        "patch of earth by the stone wall, broken barrels, a pale mist, soft pink-grey morning light." + VACIO,
    "T2_32_lago_darrowmere_noche": "Wide background at night: the shore of the big lake Darrowmere with the ruins of Darrowshire on "
        "the hill above, a full moon and its long silver reflection on the still black water, reeds, a small broken wooden pier, "
        "a few faint ghostly lights over the water." + VACIO,
    "T2_33_casa_pamela_vela": "Wide background at night: the ruined cottage where a ghost girl waits, seen close from outside, a "
        "single window with one small candle burning on the sill and a little rag doll sitting next to it, cracked walls, ivy, mist."
        + VACIO,
}

HOJAS2 = {
    "T2_50_davil_hoja": "Character model sheet" + HOJA + ": Davil Lightfire, a young blond human paladin of the Knights of the Silver "
        "Hand of World of Warcraft, clean-shaven, short blond hair, shining silver-and-gold plate armour with big round pauldrons, a "
        "white tabard with a golden emblem, a kite shield and a warhammer glowing with golden holy light. The SAME man drawn 6 times,"
        + FILA + ": raising his glowing warhammer high and shouting a rallying cry; swinging the warhammer in a mighty blow; bracing "
        "behind his shield; kneeling wounded clutching his side, hammer on the ground; lying on his back dying, side view, eyes "
        "closed; walking in full armour, side view facing right." + NOSOMBRA,
    "T2_51_horgus_hoja": "Character model sheet" + HOJA + ": Horgus the Ravager, a huge hulking ghoul lord of the Scourge of World "
        "of Warcraft: grey-green rotting muscular body twice the size of a man, a wild mane of long black hair, huge claws, exposed "
        "ribs and spine, torn loincloth, glowing green eyes, drooling jaws. The SAME monster drawn 5 times," + FILA + ": stalking "
        "forward crouched; roaring with arms spread wide; slashing with his claws; falling backwards struck down; lying dead face "
        "down." + NOSOMBRA,
    "T2_52_marduk_hoja": "Character model sheet" + HOJA + ": Marduk the Black, a death knight of the Scourge of World of Warcraft: "
        "tall, in black spiked plate armour with bone-white trims, a horned black helmet hiding the face with two icy glowing eyes, "
        "a tattered black cape, a long dark runeblade glowing with icy green runes. The SAME knight drawn 5 times," + FILA + ": "
        "standing pointing his runeblade forward; holding out one clawed gauntlet casting swirling dark green-violet magic; laughing "
        "with arms spread wide; walking side view facing right; holding up his shattered broken runeblade." + NOSOMBRA,
    "T2_53_marduk_galope": "Animation sprite sheet" + HOJA + ": gallop cycle of Marduk the Black, a death knight in black spiked "
        "armour and tattered black cape riding a skeletal undead warhorse with glowing green eyes and green flames at its hooves. "
        "The SAME horse and rider drawn 6 times in a single horizontal row, strict side view facing right, same size, evenly spaced "
        "and not touching, each drawing a consecutive phase of one gallop stride." + NOSOMBRA,
    "T2_54_rutagrana_hoja": "Character model sheet" + HOJA + ": Redpath the Corrupted of World of Warcraft, the twisted undead "
        "shadow of a village captain: a broad bearded man with a longsword and a round shield, but his body made of dark smoky "
        "shadow, translucent black and plague-green, glowing sickly green eyes, green wisps trailing from his armour. The SAME "
        "figure drawn 5 times," + FILA + ": standing menacing with sword and shield; shouting with arms spread wide; reaching out "
        "a clawed hand spreading green corruption; collapsing to his knees struck down; dissolving upward into black smoke."
        + NOSOMBRA,
    "T2_55_cromi_hoja": "Character model sheet" + HOJA + ": Chromie, a tiny female gnome of World of Warcraft (a bronze dragon in "
        "disguise): pale blonde hair in two short pigtails, big green eyes, white and gold robes with bronze pauldrons, a golden "
        "staff topped with a small hourglass. The SAME gnome drawn 5 times," + FILA + ": sitting on a stack of books reading; "
        "leaning forward squinting curiously; pointing up with one finger explaining; holding out a tied cloth bundle with both "
        "arms; raising her staff casting golden time magic with sand swirling. Then a sixth separate drawing of a bronze dragon "
        "with golden-bronze scales and cream wings, flying, side view facing right." + NOSOMBRA,
    "T2_56_aventurero_hoja": "Character model sheet" + HOJA + ": a World of Warcraft adventurer, a human warrior in steel plate "
        "armour with a red cloak and a longsword. The SAME man drawn 6 times," + FILA + ": walking side view facing right; kneeling "
        "and digging in the ground with his hands; swinging his sword in a strike; holding a small object up in one hand; standing "
        "still listening, head tilted; crouching to place a cloth bundle on the ground." + NOSOMBRA,
    "T2_57_pamela_corre": "Animation sprite sheet" + HOJA + ": run cycle of Pamela Redpath, a little human girl of about 7 with long "
        "ginger-red hair in two side ponytails, brown peasant dress with a cream-white apron, barefoot, running with her arms "
        "open. The SAME girl drawn 8 times in a single horizontal row, strict side view facing right, full body, same size and same "
        "height, evenly spaced with wide gaps and not touching, each drawing a consecutive phase of one running stride." + NOSOMBRA,
    "T2_58_reencuentro_hoja": "Character sheet" + HOJA + ": Captain Joseph Redpath (broad man, brown beard, steel breastplate, "
        "blue and gold sash) and his little daughter Pamela (7, ginger-red ponytails, brown dress, cream apron)," + FILA + ": "
        "Joseph kneeling and hugging Pamela tightly; Joseph and Pamela walking away hand in hand seen from behind; Pamela jumping "
        "with joy with her arms up; Pamela holding a small teapot carefully; Pamela holding out a small brass key with both hands; "
        "Joseph kneeling with his arms open wide." + NOSOMBRA,
    "T2_59_monstruos_hoja": "Character sheet" + HOJA + ": 6 different figures of the Plaguelands of World of Warcraft," + FILA + ": "
        "a decrepit guardian, an undead skeletal librarian in rotten purple robes holding a glowing book; a Scarlet Crusade soldier "
        "in a white tabard with a red emblem, red cape and sword; a Scarlet Crusade archer; a huge stitched undead abomination with "
        "hooks; a floating pale banshee with long white hair; a plague-ridden peasant zombie with a scythe." + NOSOMBRA,
    "T2_60_utileria2": "Prop sheet" + HOJA + ", 16 separate objects evenly spaced in a 4x4 grid, never touching or overlapping: the "
        "head of a small rag doll with button eyes and red yarn hair; the torn left half of the rag doll's body; the torn right "
        "half of the rag doll's body; a simple gold wedding ring; an old thick leather-bound book with brass corners; a huge "
        "monstrous ghoul skull with long fangs; a broken black runeblade sword with icy green runes; a rolled parchment treatise "
        "tied with a red ribbon and a wax seal; a cloth bundle of relics tied with rope; a small blue ceramic teapot; a tea cup; a "
        "small sugar bowl; a brass key; a small wooden treasure chest with iron bands; a golden hourglass; a brown leather bag "
        "with a drawstring." + NOSOMBRA,
}

P = {k: E + v + C for k, v in {**ESC, **HOJAS, **ESC2, **HOJAS2}.items()}
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(ESC), "escenarios +", len(HOJAS), "hojas =", len(P), "prompts")
