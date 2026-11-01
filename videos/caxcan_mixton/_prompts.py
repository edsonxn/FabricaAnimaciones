"""Prompts de Flow (Nano Banana 2.1 · 16:9 · x2) para «El llamado del Mixtón» (pegatina Flow CINEMATOGRÁFICO).

Escribe prompts.json (clave → prompt). Todos empiezan con FICHA (lo valida `flow_integrado.py paquete`).
Receta: docs/estilo_pegatina_flow.md §1. Escenarios vacíos (el código pone a la gente), hojas en fondo blanco puro,
ciclos mirando a la DERECHA. Objetos blancos/claros (algodón, humo, nubes) → hoja en fondo GRIS MEDIO (§9).
Escenarios 1K, hojas 2K (regla del 21-oct). Variante b = segundo encuadre del mismo lugar.
"""
import json
import os

FICHA = ("Cinematic hand-painted 2D cut-out animation art for an animated feature film, a painted storybook brought to the big "
         "screen: bold dark-brown ink outlines, rich layered gouache with painterly shading, dramatic cinematic lighting (golden "
         "rim light, deep soft shadows, atmospheric haze, strong depth), visible paper grain, earthy palette (ochre, terracotta, "
         "sand, sage and olive green, deep teal river, dusk violet, ember orange). The Juchipila canyon in southern Zacatecas, "
         "Mexico, between 1525 and 1541: reddish canyon walls, mesquite and huizache trees, nopal, maguey and organ cactus, "
         "flat-topped rocky mesas with sheer cliffs. Caxcan people (indigenous, related to the Nahua) wear white cotton loincloths, "
         "capes and headbands; women wear white cotton huipil blouses and indigo wrapped skirts. Historically accurate and "
         "respectful, never Plains-Indian feather bonnets.")

FIN = "No people, no animals. No text, no letters, no numbers, no watermark."

# ── Fichas físicas (iguales en todas las hojas y ciclos) ──
TECUANI = ("TECUANI, a 27-year-old Caxcan farmer and father: lean and strong, warm brown skin, long straight black hair tied back "
           "with a white cotton headband, kind serious eyes, white cotton loincloth and a knotted white cotton cape over one "
           "shoulder, a smooth green river stone pendant on a cord at his chest, simple leather sandals")
TECUANI_G = ("TECUANI at 42 as a Caxcan warrior: the same lean strong man, now with a weathered face and a few gray strands in his "
             "long black hair, white cotton headband, two red ochre war-paint stripes across the cheeks, sleeveless quilted cotton "
             "armor vest over a white loincloth, a green river stone pendant on a cord at his chest, leather sandals, a wooden bow, "
             "a quiver of arrows on his back and a wooden war club")
CITLALI = ("CITLALI, a 26-year-old Caxcan woman: brown skin, long black hair in two braids wrapped with red cords, gentle strong "
           "face, white cotton huipil blouse with a narrow ochre geometric border, indigo wrapped skirt, barefoot, a shell necklace")
OLLIN_N = ("OLLIN as a 5-year-old Caxcan boy: small and round-cheeked, brown skin, black hair with straight bangs, big curious eyes, "
           "only a small white cotton loincloth, barefoot")
OLLIN_J = ("OLLIN at 15, a lean Caxcan teenage boy: brown skin, shoulder-length black hair with a white cotton headband, bright eager "
           "eyes, white cotton loincloth and a short cape knotted on one shoulder, leather sandals, a small bow")
ABUELO = ("the GRANDFATHER, an old Caxcan man: thin and wrinkled, long white hair loose to the shoulders, white wispy beard, "
          "kind laughing eyes, worn white cotton cape, loincloth, a walking staff of mesquite wood")
PROFETA = ("the PROPHET-MESSENGER, a wiry man from the northern sierra: dark skin painted with white clay dots and stripes, wild "
           "long black hair with two hawk feathers, a deerskin loincloth, a gourd rattle and a short staff hung with shells")
CORREDOR = ("the RUNNER, a young Caxcan messenger: slim and sweating, covered in dust, white headband, loincloth, sandals, a "
            "small cotton bag across his chest")
TENAMAXTLI = ("TENAMAXTLI, the Caxcan lord of Nochistlan and war leader: tall, powerful, about 40, brown skin, long black hair "
              "tied on top with a red cord and a small crest of green and red feathers, jade ear spools, a white cotton cape with "
              "a red stepped-fret border over a quilted cotton armor vest, a heavy wooden war club, a round shield with a "
              "blue and yellow stepped design")
GUZMAN = ("CHIRINOS, a cruel Spanish conquistador captain of 1530 serving Nuno de Guzman: middle-aged, black pointed beard, cold eyes, polished "
          "steel rounded steel cabasset helmet with a red plume, steel breastplate over a black doublet, black cape, high boots, sword")
HERALDO = ("a Spanish NOTARY of 1530: thin, clean-shaven, black doublet and black cap, white ruff-less shirt collar, reading "
           "aloud from an unrolled parchment with a red wax seal")
ENCOMENDERO = ("the ENCOMENDERO, a fat Spanish landowner of the 1530s: red face, brown beard, wide-brimmed black hat, brown "
               "leather doublet, a short whip, high boots")
FRAILE = ("a FRANCISCAN FRIAR of the 1530s: tonsured head, gray-brown hooded habit with a knotted rope belt, bare feet in "
          "sandals, a small wooden cross, a clay bowl of water")
ALVARADO = ("PEDRO DE ALVARADO in 1541: proud Spanish conquistador of about 55, reddish-blond hair and beard, ornate engraved "
            "steel armor with gold trim, open steel burgonet helmet with white plumes, red sash, sword")
MENDOZA = ("viceroy ANTONIO DE MENDOZA in 1541: dignified Spanish nobleman of about 50, short gray beard, black velvet doublet "
           "under a half-armor breastplate, black hat with a feather, gold chain, on a white horse")
OLLIN_V = ("OLLIN as an old man of 75: thin, deeply wrinkled brown face, long white hair tied with a faded headband, white "
           "cotton cape, a smooth green river stone pendant on a cord at his chest, a walking staff")


def fondo(desc, fin=FIN):
    return f"{FICHA} {desc} {fin}"


def hoja(ficha, poses, quien="character", gris=False):
    n = len(poses)
    bg = "plain flat medium-gray background" if gris else "plain flat pure white background"
    return (f"{FICHA} Character model sheet on a {bg}: {ficha}. The SAME {quien} drawn {n} times, full body, evenly spaced in "
            f"one row with generous empty space between them, never touching or overlapping: " + "; ".join(poses) +
            ". No ground, no cast shadows. No text, no letters, no watermark.")


def grupo(desc, figuras, gris=False):
    bg = "plain flat medium-gray background" if gris else "plain flat pure white background"
    return (f"{FICHA} Character sheet on a {bg}: {desc}, {len(figuras)} DIFFERENT figures, full body, evenly spaced in one row "
            f"with generous empty space, never touching or overlapping: " + "; ".join(figuras) +
            ". No ground, no cast shadows. No text, no letters, no watermark.")


def ciclo(ficha, tipo, n, paso, quien="character"):
    return (f"{FICHA} Animation sprite sheet on a plain flat pure white background: {tipo} cycle of {ficha}. The SAME {quien} "
            f"drawn {n} times in a single horizontal row, strict side view facing right, full body, same size and same height, "
            f"evenly spaced with wide gaps and never touching, weapons held close to the body, each drawing a consecutive phase "
            f"of one {paso}. No ground line, no cast shadows. No text, no letters, no watermark.")


def rejilla(n, objetos, gris=False):
    bg = "plain flat medium-gray background" if gris else "plain flat pure white background"
    return (f"{FICHA} Prop sheet on a {bg}: {n} separate objects arranged in an even grid with generous space, never "
            f"touching or overlapping, each drawn whole: " + "; ".join(objetos) + ". No cast shadows. No text, no letters, "
            f"no watermark.")


P = {}
# ── ESCENARIOS (vacíos, 16:9, con primer plano / plano medio / fondo) ─────────────────────────────────────────────────
E = {
 "e01_mixton_noche": "Night on the summit of a rocky mesa fortress: in the foreground a rough dry-stone parapet wall and boulders "
     "lit by a small dying campfire glow; beyond the edge, far below, a vast dark valley covered with hundreds of tiny orange "
     "enemy campfires all the way to the horizon; deep blue night sky full of stars and a pale moon, cold mist in the canyon. "
     "Open flat rock ground across the lower third. Epic, quiet, ominous.",
 "e02_canon_amanecer": "Epic wide establishing shot of the Juchipila canyon at sunrise: a winding turquoise river in the valley "
     "floor, small maize fields and a Caxcan village of adobe and stone houses with thatched roofs along the banks, smoke from "
     "cooking fires, mesquite trees, reddish canyon walls and flat-topped mesas glowing gold, mist in the hollows. Foreground: "
     "maguey and nopal on a ridge, open dirt path across the lower third.",
 "e03_milpa_rio": "Riverbank maize field (milpa) in the green rainy season: tall maize plants with squash vines and bean "
     "tendrils, the river sparkling behind, mesquite trees, canyon wall in the distance, warm late-morning light. Open "
     "earth path across the lower third.",
 "e04_casa_madrugada": "Interior of a humble Caxcan adobe house before dawn: low thatched roof beams, a stone hearth with "
     "glowing embers and a clay comal, a stone metate on the floor, clay pots and baskets of corn, woven palm mats, a doorway "
     "showing deep blue pre-dawn light. Warm orange firelight against cold blue. Open floor across the lower third.",
 "e05_rio_piedras": "Shallow clear river crossing with smooth round green and gray stones, reeds and river grass, sunlight "
     "dappled through a big mesquite tree, small fish shadows, warm afternoon. Sandy bank across the lower third.",
 "e06_plaza_fiesta": "Night village plaza of a Caxcan town during a harvest festival: a large stone ring for a bonfire in the "
     "middle (unlit), adobe houses with thatched roofs around it, garlands of maize cobs and squash hanging on poles, a low "
     "stone platform, warm torch glow, starry sky and dark canyon walls. Open beaten-earth ground across the lower third.",
 "e07_teul_cima": "Summit of a sacred mountain at golden hour: an ancient stone stepped platform and a small stone shrine with "
     "offerings of maize and flowers, wide view over the whole canyon, rivers and distant villages, glowing clouds, long "
     "shadows. Open rock ground across the lower third.",
 "e08_camino_mercaderes": "Dusty footpath along the river at dusk where traders rest: a big shady mesquite tree, a flat stone "
     "seat, a small campfire ring, bundles place, reddish cliffs, violet sky with the first star. Open path across the lower third.",
 "e09_canon_polvo": "The same canyon in the dry season at harsh midday: dry yellow grass, leafless huizache, and on the far road "
     "along the river a huge rising dust cloud coming toward the village, ominous, small glints of metal inside the dust. "
     "Foreground: dry rocks and agave on a hilltop lookout. Open ground across the lower third.",
 "e10_pueblo_entrada": "Entrance of a Caxcan village at midday: a beaten-earth road coming in between adobe houses with "
     "thatched roofs, a big ceremonial mesquite tree, granaries on stilts, clay pots at doorways, canyon walls behind, harsh "
     "white sunlight and short shadows. Open road across the lower third.",
 "e11_pueblo_quemado": "A Caxcan village burning at dusk: thatched roofs on fire, black smoke columns, ruined adobe walls, "
     "trampled maize fields, embers flying, a red-orange sky, the river reflecting the fire. Open scorched ground across the "
     "lower third. Dramatic and sad, no gore.",
 "e12_campamento": "A Spanish conquistador military camp of 1530 in the canyon at dusk: canvas tents, a rope corral, piled "
     "saddles and lances, a burning iron brazier with branding irons glowing in the coals, a tall banner pole with a "
     "red-and-white flag, campfires. Open ground across the lower third.",
 "e13_camino_cargadores": "A long dusty road leaving the canyon along the river at sunset, disappearing into the distant hills, "
     "trampled by many feet, an abandoned basket by the roadside, long shadows, melancholic orange-violet sky. Open road across "
     "the lower third.",
 "e14_granero": "A Spanish encomienda yard under a hard sun: a half-built adobe granary with wooden scaffolding, stacks of "
     "adobe bricks, sacks of maize, a wooden cart, a small adobe house with a tiled roof for the Spaniard, dust in the air. "
     "Open yard across the lower third.",
 "e15_capilla": "A humble open-air chapel of the 1530s: a ramada of mesquite posts and palm thatch, a rough wooden cross, a "
     "carved stone baptismal font full of water, a small bell hung on a beam, candles, canyon behind in morning light. Open "
     "packed-earth floor across the lower third.",
 "e16_guadalajara_nochistlan": "A small brand-new Spanish frontier town of 1532 on a high plateau: a few adobe houses with "
     "tiled roofs, a wooden palisade, a little church with a bell gable, a plaza with a wooden cross, horses' corral, blue "
     "mountains behind, morning light. Open plaza ground across the lower third.",
 "e17_barranca_arco": "A hidden ravine in late afternoon: steep rock walls with ferns, a lone old mesquite tree used as an "
     "archery target with a woven straw disk tied to the trunk, golden light beams, dust motes, a dry stream bed. Open sandy "
     "ground across the lower third.",
 "e18_camino_norte": "View from a canyon ridge of a long road heading north into vast dry plains, a distant dust cloud of a "
     "departing army disappearing on the horizon, big empty sky, the canyon below quiet and almost empty. Open ridge ground "
     "across the lower third.",
 "e19_fogata_tlatol": "A night clearing in the hills prepared for a secret ritual dance: a big stone ring for a bonfire "
     "(unlit), a circle of trampled earth, offerings of maize and copal on a flat rock, dark pine-oak and mesquite silhouettes, "
     "the mountains of the sierra against a deep violet starry sky. Open dance ground across the lower third.",
 "e20_rio_niebla": "The river at dawn with thick mist floating on the water, cold blue and pink light, smooth stones, reeds, "
     "a calm wide pool, the canyon walls fading in the haze. Open riverbank across the lower third.",
 "e21_casa_puerta": "Exterior of a humble Caxcan adobe house in the afternoon: a doorway with a hanging woven mat, a clay water "
     "jar, drying chiles and maize cobs hanging from the eaves, a small yard with a turkey pen, a mesquite tree, canyon walls. "
     "Open yard across the lower third.",
 "e22_casa_noche": "Interior of the same humble adobe house at night: a small fire in the stone hearth throwing warm flickering "
     "light and long shadows, a sleeping mat, clay pots, a bow hanging on the wall, a doorway to the dark blue night. Open "
     "floor across the lower third.",
 "e23_subida_mixton": "A steep narrow trail zigzagging up the side of a huge rocky mesa with sheer cliffs, boulders and organ "
     "cactus, the Juchipila canyon far below, morning light and long shadows. Open trail ground across the lower third.",
 "e24_mixton_cima_dia": "The summit plateau of a mountain fortress (peñol) by day: low dry-stone defensive walls along the "
     "cliff edge, piles of round rocks ready to throw, simple shelters of branches and palm, clay water jars, smoke of cooking "
     "fires, a breathtaking view down into the canyon. Open rocky ground across the lower third.",
 "e25_mixton_ladera": "Looking down from behind a stone parapet over a very steep rocky slope that drops toward the valley: the "
     "only narrow path climbing up through boulders and cactus, dust, harsh afternoon light, the valley far below. The "
     "parapet runs along the bottom of the image.",
 "e26_nochistlan_lluvia": "A rocky mesa fortress under heavy summer rain: dark storm clouds, sheets of rain, muddy slopes with "
     "rivulets of water, slippery red mud and boulders, flashes of lightning, gray-green light. Open muddy slope across the "
     "lower third.",
 "e27_barranca_lodo": "Close view of a steep muddy ravine slope in the rain: red mud, broken branches, loose stones, a narrow "
     "slippery path at the edge of the drop, gray light. Open mud across the lower third.",
 "e28_guadalajara_amanecer": "A small Spanish frontier town of 1541 at dawn seen from outside: adobe houses with tiled roofs, a "
     "wooden palisade and a gate, a little church tower, cold blue light with the first orange on the horizon, mist, fields "
     "outside the walls. Open field across the lower third.",
 "e29_guadalajara_fuego": "Inside the streets of a small Spanish frontier town during an attack: adobe houses with tiled roofs "
     "on fire, smoke, a broken wooden fence, a church bell tower at the end of the street, flying embers, chaos lighting. Open "
     "street across the lower third. No gore.",
 "e30_mixton_noche_fuego": "On the mountain fortress at night: a small campfire between two big boulders, a flat rock to sit on, "
     "a stone wall, the vast dark canyon below with a few distant fires, stars, cold blue moonlight against warm firelight. "
     "Open rock ground across the lower third.",
 "e31_valle_ejercito": "A huge army camp filling the whole valley below the mesas by day: hundreds of tents, banners of many "
     "colors, columns of marching troops as tiny dots, cannons, horse lines, smoke of many fires, dust, seen from high above. "
     "Foreground: rocks of the mountain fortress edge.",
 "e32_penoles_humo": "Distant rocky mesas on the horizon with tall black smoke columns rising from their summits, a gray "
     "sky, the canyon in shadow, seen from the summit of another mesa. Foreground: a stone wall and dry grass.",
 "e33_mixton_cerco": "The summit of the mountain fortress during a long siege: empty cracked stone water basins, empty clay jars, "
     "torn shelters, ash of old fires, exhausted dry grass, a merciless white sun, heat haze. Open rocky ground across the "
     "lower third.",
 "e34_vereda_barranca": "A narrow deer trail descending a deep steep ravine at the blue hour before dawn: rocks, ferns, "
     "hanging roots, a thin waterfall trickle, deep shadows, the first faint light above the ridge. The trail runs along the "
     "lower third and disappears into the dark.",
 "e35_mixton_asalto": "The stone walls of the mountain fortress at sunrise under attack: smoke drifting across, scattered "
     "arrows stuck in the ground, broken shields, a fallen banner, dust and orange light. Open ground across the lower third. "
     "No people, no gore.",
 "e36_precipicio": "The edge of a sheer cliff at sunrise: a vertiginous drop into a deep canyon full of mist, black vultures "
     "circling far below, rocks and dry grass at the edge, solemn golden light. Open rock edge across the lower third.",
 "e37_sierra_escondite": "A hidden refuge in the pine-oak forest of the high sierra: a small hut of stones and branches, a "
     "tiny maize patch, a spring with a clay jar, blue mountains layered into the distance, soft afternoon light, years later.",
 "e38_mixton_hoy": "Same art style, but this picture is set in the present day: the great rocky mesa of the Mixton seen from "
     "the valley of Apozol, Zacatecas at golden hour, rows of blue agave fields, a small white church tower of a modern town "
     "in the distance, a paved road, power poles. Open field across the lower third.",
 "e39_galeon": "A 16th-century Spanish galleon sailing on a vast dark ocean at dusk, big square sails, a storm on the horizon, "
     "gray-green waves, a long trail of foam, loneliness.",
 "e40_consejo": "A solemn hall of the Spanish royal council in Valladolid in the 1550s: dark wooden coffered ceiling, red "
     "velvet drapes, a long table with papers, ink and candles, a royal coat of arms tapestry, tall windows with dusty light. "
     "Open stone floor across the lower third.",
 "e41_casa_vieja_noche": "Interior of a humble rural adobe house in the canyon decades later (1590s) at night: a fire in the "
     "hearth, a wooden bench, clay pots, a wooden cross on the wall next to an old bow, a doorway to a starry night. Open "
     "floor across the lower third.",
}
for k, v in E.items():
    P[k] = fondo(v)

# ── HOJAS DE PERSONAJES ───────────────────────────────────────────────────────────────────────────────────────────
P["h01_tecuani"] = hoja(TECUANI, [
    "standing calm, front view", "kneeling and lifting a smooth stone from the water, side view facing right",
    "holding a newborn baby wrapped in white cotton, tender", "laughing while dancing, arms open, side view",
    "carrying a heavy stone block on his shoulder, bent, side view facing right",
    "kneeling with head lowered while water is poured on him, side view facing left"], "man")
P["h02_tecuani_g"] = hoja(TECUANI_G, [
    "standing at a wall looking into the distance, side view facing left", "drawing the bow and aiming, side view facing right",
    "raising the war club and shouting, front three-quarter", "sitting on a rock with arms resting on knees, tired, side view facing right",
    "kneeling and taking off the green stone pendant to give it, three-quarter", "throwing a big rock with both hands over his head"], "warrior")
P["h03_citlali"] = hoja(CITLALI, [
    "kneeling at a stone metate grinding maize, side view facing right", "standing holding a baby against her chest",
    "dancing with a joyful laugh, skirt swirling", "crying with hands covering her mouth, front view",
    "walking with a clay water jar on her shoulder, side view facing right", "hugging a child protectively, crouching, front three-quarter"], "woman")
P["h04_ollin_nino"] = hoja(OLLIN_N, [
    "standing holding up a smooth green stone with both hands, proud", "sitting on the ground playing with pebbles",
    "pointing excitedly", "hugging a leg (as if hugging his father), side view facing left",
    "carrying a small clay water jar with effort, side view facing right", "crying with fists rubbing his eyes"], "boy")
P["h05_ollin_joven"] = hoja(OLLIN_J, [
    "drawing a small bow and aiming, side view facing right", "standing proud with the bow, front three-quarter",
    "shouting with joy, arms raised", "crying and clenching his fists, front view",
    "sitting on a rock hugging his knees, worried, side view facing right", "holding a green stone pendant in his open hands, looking at it"], "teenage boy")
P["h06_abuelo"] = hoja(ABUELO, [
    "standing pointing far away with his staff, side view facing right", "laughing with his head thrown back",
    "walking bent under a huge bundle tied with a tumpline to his forehead, a rope around his neck, side view facing right",
    "whispering, leaning forward, front three-quarter", "sitting on a rock telling a story with an open hand",
    "standing with both hands on his staff, looking at the horizon, back three-quarter view"], "old man")
P["h07_profeta"] = hoja(PROFETA, [
    "shouting with both arms raised to the sky, front view", "dancing wildly shaking the gourd rattle, side view facing right",
    "whispering with a finger on his lips, three-quarter", "pointing to the mountains with his staff, side view facing left",
    "spinning in a trance, hair flying"], "man")
P["h08_tenamaxtli"] = hoja(TENAMAXTLI, [
    "speaking to a crowd with an open raised hand, front view", "pointing down into the valley with the war club, side view facing left",
    "standing with arms crossed, stern, front view", "raising the war club and the shield, battle cry",
    "walking, side view facing right"], "man")
P["h09_corredor"] = hoja(CORREDOR, [
    "running, side view facing right", "standing bent forward panting with hands on knees",
    "speaking urgently with an open hand, front three-quarter", "pointing behind him toward the mountain"], "young man")
P["h10_guzman"] = hoja(GUZMAN + ", riding a big black horse with a red saddle cloth", [
    "on horseback standing still, side view facing right", "on horseback pointing forward with his sword, side view facing right",
    "on horseback, the horse rearing, side view facing right"], "rider")
P["h11_espanoles_a_pie"] = grupo("Spanish people of the 1530s, all facing right or front", [
    HERALDO, ENCOMENDERO + ", shouting and raising the whip", FRAILE + ", holding up the bowl of water",
    "a Spanish soldier with a rounded steel cabasset helmet and steel breastplate holding a glowing red-hot branding iron",
    "a Spanish soldier with a rounded steel cabasset helmet and steel breastplate pulling a rope",
    "a Spanish soldier with a rounded steel cabasset helmet aiming a crossbow"])
P["h12_soldados"] = grupo("Spanish conquistador soldiers of 1530-1541, all facing right", [
    "a pikeman with a long pike and rounded steel cabasset helmet", "an arquebusier holding a matchlock arquebus with smoking fuse",
    "a swordsman with a round steel shield (rodela) and sword", "a crossbowman reloading",
    "a soldier holding a big war mastiff on a leash", "a standard bearer with a red-and-white flag"])
P["h13_aliados"] = grupo("indigenous allies of the Spaniards from central Mexico (Tlaxcalans and Mexica) in 1541, all facing right", [
    "a Tlaxcalan warrior in white quilted cotton armor with a wooden sword edged with obsidian blades and a round feather shield",
    "a Mexica warrior in a jaguar-pattern suit with a spear", "a warrior carrying a white heron banner on a pole",
    "a porter carrying a huge load with a tumpline", "an archer in quilted armor", "a warrior with a sling and a shield"])
P["h14_guerreros"] = grupo("Caxcan warriors of 1541, mixed poses", [
    "a warrior throwing a big stone with both arms", "an archer shooting upward", "a warrior with a sling spinning it",
    "a warrior with a war club and a round reed shield, shouting", "a warrior blowing a conch shell trumpet",
    "a young warrior rolling a boulder"])
P["h15_gente"] = grupo("Caxcan villagers and refugee families, white cotton clothes", [
    "an old woman carrying firewood", "a mother carrying a baby in a shawl on her back", "two small children holding hands",
    "a man carrying a bundle and a clay jar on his back", "a girl carrying a basket of maize on her head",
    "an old man sharpening an arrow, sitting"], gris=True)
P["h16_alvarado"] = hoja(ALVARADO + ", riding a big gray horse with a gold-trimmed saddle", [
    "on horseback laughing proudly, side view facing right", "on horseback charging with lance, side view facing right",
    "on horseback, the horse slipping and falling backward in mud, side view facing left"], "rider")
P["h17_mendoza"] = hoja(MENDOZA, [
    "on horseback, standing still, side view facing right", "on horseback pointing forward with a baton, side view facing right",
    "on foot, standing with a hand on his sword, front three-quarter"], "man")
P["h18_ollin_viejo"] = hoja(OLLIN_V, [
    "sitting by a fire telling a story with an open hand, side view facing right", "standing looking at the horizon, back three-quarter",
    "holding the green stone pendant in his palm, looking at it", "walking slowly with the staff, side view facing right"], "old man")
P["h19_tenamaxtli_espana"] = hoja("TENAMAXTLI in the 1550s, older and gray-haired, dressed in a simple dark Spanish-style cloak "
    "over a white cotton shirt, still wearing his jade ear spools", [
    "standing before a council holding a written petition, front three-quarter", "speaking with an open hand, side view facing right",
    "standing in chains, head high, front view"], "man")

# ── CICLOS (mirando a la DERECHA) ──
P["c01_tecuani_camina"] = ciclo(TECUANI, "walk", 8, "walking step", "man")
P["c02_guerrero_corre"] = ciclo(TECUANI_G, "run", 8, "running stride", "warrior")
P["c03_ollin_corre"] = ciclo(OLLIN_J, "run", 8, "running stride", "teenage boy")
P["c04_caxcan_corre"] = ciclo("a generic Caxcan warrior with a white headband, loincloth and a war club", "run", 8, "running stride", "warrior")
P["c05_soldado_marcha"] = ciclo("a Spanish conquistador soldier of 1530 with a rounded steel cabasset helmet, steel breastplate and a pike on "
                                "his shoulder", "march", 8, "marching step", "soldier")
P["c06_aliado_marcha"] = ciclo("a Tlaxcalan allied warrior in white quilted cotton armor with an obsidian-edged wooden sword "
                               "and a round feather shield", "march", 8, "marching step", "warrior")
P["c07_jinete_galope"] = ciclo("a Spanish conquistador rider in rounded steel cabasset helmet and breastplate with a lance on a brown horse",
                               "gallop", 6, "gallop stride", "horse and rider")
P["c08_perro_corre"] = ciclo("a big brown Spanish war mastiff with a spiked leather collar", "run", 6, "running stride", "dog")
P["c09_zopilote"] = (f"{FICHA} Animation sprite sheet on a plain flat pure white background: a row of 6 drawings of the same "
                     "black vulture (zopilote) in flight seen from the side facing right, showing a wing-flap cycle, evenly spaced "
                     "and not touching. No text, no letters, no watermark.")
P["c10_danza"] = ciclo("a Caxcan dancer with a white headband, loincloth, shell anklets and a gourd rattle", "ritual dance", 8,
                       "stomping dance step", "dancer")
P["c11_tameme"] = ciclo(ABUELO + ", bent under a huge bundle on his back held by a tumpline across his forehead, a rope around "
                        "his neck", "slow tired walk", 8, "walking step", "old man")
P["c12_citlali_camina"] = ciclo(CITLALI, "walk", 8, "walking step", "woman")

# ── UTILERÍA Y NATURALEZA ──
P["u01_utileria"] = rejilla(16, [
    "a stone metate with its grinding stone", "a clay comal with tortillas", "a big clay olla", "a basket of maize cobs",
    "a wooden bow", "a quiver of arrows", "a wooden war club", "a round reed shield with a blue and yellow stepped design",
    "a smooth green river stone on a cord", "a glowing red-hot branding iron", "a coiled rope", "a big bundle with a tumpline",
    "a rough wooden cross", "an unrolled parchment with a red wax seal", "a lit torch", "a conch shell trumpet"])
P["u02_utileria_guerra"] = rejilla(12, [
    "a pile of round throwing rocks", "a segment of dry-stone wall", "a Spanish rounded steel cabasset helmet", "a steel breastplate",
    "a Spanish sword", "a crossbow", "a matchlock arquebus", "a small bronze cannon on a wooden carriage",
    "a broken lance", "a fallen red-and-white Spanish flag", "a clay water jar, cracked", "a two-headed teponaztli log drum"])
P["u03_naturaleza"] = rejilla(12, [
    "a mesquite tree", "a huizache tree with yellow flowers", "a nopal cactus with red tunas", "a big maguey plant",
    "an organ pipe cactus", "a tall maize plant with ears", "a clump of dry grass", "a big round boulder",
    "a cluster of reddish rocks", "a blue agave plant", "a pine-oak tree", "a reed clump"])
P["u04_fuego_humo"] = rejilla(12, [
    "a campfire with tall flames", "a small campfire", "a big bonfire", "a column of black smoke",
    "a puff of gray smoke", "a burst of dust", "a dust cloud", "a gray rain cloud", "a dark storm cloud",
    "a flying ember spark cluster", "a burning thatched roof chunk", "a splash of muddy water"], gris=True)

# ── 2.º pedido (21-oct): BANDO ESPAÑOL, narrador y fechas ─────────────────────────────────────────────────────────
E2 = {
 "e42_tienda_chirinos": "Interior of a Spanish conquistador captain's canvas tent at night in 1530: a hanging iron lantern, a "
     "folding wooden table with a rough hand-drawn map, a quill and ink, an open wooden chest with chains and iron shackles, "
     "a steel breastplate on a stand, the tent flap open to a dark camp with a glowing brazier. Cold menacing light. Open "
     "ground across the lower third.",
 "e43_palacio_virrey": "The council chamber of the viceroy's palace in Mexico City in 1541: thick stone walls and arches, a "
     "long dark wooden table with documents, wax seals, an inkwell and candles, a carved high-backed chair, a royal Spanish "
     "coat of arms on a tapestry, a tall window showing the new colonial city and volcanoes. Cold solemn light. Open stone "
     "floor across the lower third.",
 "e44_casa_onate": "A room in a Spanish frontier town house of 1541: whitewashed adobe walls, wooden beams, a table with a "
     "map and a steel helmet, swords and crossbows on a wall rack, a small window with afternoon light, dust in the air. "
     "Open tiled floor across the lower third.",
 "e45_iglesia_refugio": "Interior of a small adobe frontier church of 1541 under attack: candlelight, a simple wooden altar "
     "and crucifix, wooden benches pushed against the heavy barred door, smoke seeping under the door, orange firelight "
     "through a high window. Open floor across the lower third.",
 "e46_lecho_alvarado": "A dim room in a frontier town in July 1541: a wooden cot with rumpled blankets, a single candle, a "
     "crucifix on the whitewashed wall, an engraved steel armor and a plumed helmet lying abandoned on the floor, rain on "
     "the small window. Melancholic, heavy shadows. Open floor across the lower third.",
 "e47_campamento_virrey": "The viceroy's siege camp at the foot of a huge rocky mesa in December 1541: a big command tent with "
     "royal banners, a row of small bronze cannons on wooden carriages aimed up at the mesa, piles of cannonballs, smoke, "
     "thousands of tents in the valley behind, cold winter light. Open ground across the lower third.",
 "e48_plaza_hoy": "Same art style, but this picture is set in the present day: the main plaza of a small town in the "
     "Juchipila canyon of southern Zacatecas at golden hour, an old stone parish church, a wrought-iron kiosk, Indian laurel "
     "trees, colorful houses, the great rocky mesa of the Mixton rising behind the town. Open plaza ground across the lower third.",
}
for k, v in E2.items():
    P[k] = fondo(v)

P["h20_chirinos_pie"] = hoja(GUZMAN.replace("riding", ""), [
    "standing with a cold smirk, arms crossed, front three-quarter", "pointing with a gloved finger, giving an order, side view facing left",
    "leaning over a table looking down, side view facing right", "holding a lantern, side view facing right"], "man")
P["h17_mendoza"] = hoja(MENDOZA, [
    "on horseback, standing still, side view facing right", "on horseback pointing forward with a baton, side view facing right",
    "on foot, standing with a hand on his sword, front three-quarter", "seated at a table signing a document with a quill, side view facing right",
    "standing, cold expression, one hand raised giving an order, side view facing left"], "man")
P["h21_espanoles_1541"] = grupo("Spanish men of 1541 in a frontier war, each a different person", [
    "CRISTOBAL DE ONATE, a worried Spanish captain of about 40 with a brown beard, steel breastplate, no helmet, hands open pleading, facing right",
    "the same CRISTOBAL DE ONATE standing with arms crossed, worried, front view",
    "MIGUEL DE IBARRA, a Spanish captain with a gray beard and a rounded steel helmet, on a brown horse, shouting with a raised hand, facing left",
    "BALTASAR DE MONTOYA, a young Spanish scribe in a dark doublet, kneeling and crying, hands reaching forward, facing left",
    "a Spanish soldier with a rounded steel helmet unrolling a long parchment to read aloud, facing left"])
P["h22_alvarado_pie"] = hoja(ALVARADO, [
    "standing laughing arrogantly with a hand on his hip, front three-quarter", "pointing scornfully, side view facing left",
    "lying on his back on a wooden cot, wounded and pale, eyes half closed, side view, head to the left",
    "carried on a shield-stretcher, wounded, side view, head to the right"], "man")
P["h23_beatriz"] = hoja("BEATRIZ HERNANDEZ, a brave Spanish settler woman of 1541: about 35, dark hair under a cream linen "
    "head cloth, dark brown wool dress with a laced bodice, a fierce determined face", [
    "shouting with one arm raised, rallying people, front three-quarter", "holding a sword and a torch, side view facing right",
    "pushing a heavy bench against a door, side view facing left", "standing protecting two children behind her, front view"], "woman")
P["h24_lascasas"] = hoja("fray BARTOLOME DE LAS CASAS in 1555: an old Dominican friar of about 70, white habit with a black "
    "hooded cloak, thin face, tonsured gray hair, holding a bundle of papers", [
    "standing and speaking with an open hand, side view facing right", "holding up papers, front three-quarter",
    "hand on the shoulder of someone beside him, side view facing right", "walking with papers under his arm, side view facing right"],
    "old friar", gris=True)
P["h25_oidores"] = grupo("members of the Spanish Council of the Indies in 1555, seated or standing, black robes and black caps", [
    "an old councillor with a white beard seated, listening sternly, facing left", "a councillor seated writing with a quill, facing left",
    "a councillor standing with a document, facing left", "a young secretary holding a candle, facing left",
    "a councillor whispering to another, seated, facing left"])


if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    for k, v in P.items():
        assert v.startswith(FICHA), k
    json.dump(P, open(os.path.join(d, "prompts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    esc = sum(1 for k in P if k.startswith("e")); print(f"prompts.json: {len(P)} prompts ({esc} escenarios, {len(P) - esc} hojas)")
