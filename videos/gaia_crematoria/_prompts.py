# -*- coding: utf-8 -*-
"""Escribe prompts.json (escenarios + hojas de Flow) con la FICHA de guion.py. Ejecutar desde la carpeta del video.
Un escenario por lugar/hora (nada repetido entre escenas); hojas de personajes con poses, ciclos (galope, correr, caminar, aleteo)
y utilería. Las claves llevan prefijo numérico para ordenarlas (paquete las envía en orden alfabético)."""
import json
import guion

E = guion.FICHA["estilo"] + ". "
C = guion.FICHA["cierre"]
VACIO = " Strong depth: foreground, midground and background layers. Open empty ground across the lower third. No people, no animals."
INTERIOR = " Strong depth: foreground, midground and background layers. Open empty floor across the lower third. No people."
FILA = " full body, evenly spaced in one row with generous empty white space between them, never touching or overlapping"
HOJA = " on a plain flat pure white background"
NOSOMBRA = " No ground, no cast shadows."
CALIDO = " Same art style but warm and hopeful colours: soft gold, warm green, clear blue."
CICLO = (" drawn 8 times in a single horizontal row, strict side view facing right, full body, same size and same height, evenly "
         "spaced with wide gaps and not touching, each drawing a consecutive phase of one")

ALEX = ("Alexandros Mograine, a tall heroic human paladin in his fifties: long dark-brown hair with grey streaks to the shoulders, "
        "short beard, stern noble face, heavy ornate silver and gold plate armor of the Silver Hand with a white tabard bearing a "
        "golden hand emblem, a long blue cape")
ESPADA = ("the Ashbringer, a long silver-white greatsword with a winged skull crossguard holding a glowing golden crystal")
CORRUPTA = ("the Corrupted Ashbringer, the same greatsword turned black with sickly green glowing runes and a green crystal")
DARION = ("Darion Mograine, a young human man of 20, wild shoulder-length black hair, earnest face, light silver paladin armor with "
          "a purple and white Argent Dawn tabard")
RENAULT = ("Renault Mograine, a young human man of 25 with slick black hair, a thin moustache and a cold proud face")
TIRION_J = ("Tirion Fordring in his forties: brown hair and a short brown beard, kind strong face, shining silver plate armor of the "
            "Silver Hand with a blue tabard and a golden hand emblem")
TIRION_V = ("old Tirion Fordring as a hermit: long white hair, long white beard, weathered face, patched brown hunting leathers and "
            "a fur cloak")
TAELAN = ("Taelan Fordring, a human man of 30 with short brown hair and a short beard, the red and white tabard of a Scarlet "
          "Crusade highlord over silver plate armor, a red cape")

ESC = {
    # gancho / cierre: la Capilla de la Esperanza de la Luz
    "e01_capilla_noche": "Wide background at night of Light's Hope Chapel in the Eastern Plaguelands of World of Warcraft: a small "
        "white stone chapel with a tall bell tower on a low hill, surrounded by dead grey earth and leafless black trees, a faint "
        "warm golden glow from its windows, dark red storm clouds above, blood-red rain falling." + VACIO,
    "e02_capilla_espada": "Close wide background at night: bare blighted dead earth in front of a small white stone chapel (Light's "
        "Hope Chapel), a single long greatsword planted point-down in the ground in the center glowing faint gold, blood-red rain, "
        "puddles reflecting the light, the chapel blurred behind." + " Strong depth. No people, no animals.",
    "e03_hogar_fuego": "Wide background inside a cosy wooden cabin at night: a big stone fireplace with a crackling fire, a "
        "comfortable armchair, a small table with an old open leather book, a candle and a steaming mug, a fur rug, a window with "
        "falling snow and blue night outside. Warm amber light." + INTERIOR,
    # Rémol
    "e04_remol_casa": "Wide background at night of a sturdy two-story stone and timber family house at the edge of the village of "
        "Brill in Tirisfal Glades (World of Warcraft), moody purple-blue twilight, tall dark pines, a few lit windows, a small "
        "stream with thin ice beside the house, a low stone wall." + VACIO,
    "e05_arroyo_helado": "Wide background of a frozen forest stream at night in winter: dark water flowing between snowy banks and thin "
        "broken ice, snow-covered pines, cold blue moonlight, breath-mist atmosphere, the warm window of a house far behind." + VACIO,
    "e06_alcoba_parto": "Wide background of a medieval bedroom at night lit by candles: a large wooden bed with rumpled white sheets, "
        "a wooden cradle beside it, a stone wall with a small window, a basin of water, linen cloths, deep shadows." + INTERIOR,
    "e07_tumba_elena": "Wide background at dusk of a single carved stone gravestone with no letters under an old tree beside a stone "
        "family house in Tirisfal Glades, fallen autumn leaves, low purple mist, sad quiet mood." + VACIO,
    # orbe
    "e08_roca_negra": "Wide background of the siege of Blackrock Spire (World of Warcraft) during the Second War: a jagged black "
        "volcanic mountain fortress with orcish spikes and red banners without symbols, rivers of lava, smoke and burning sky, "
        "wooden siege ballistas of the Alliance in the foreground, scorched rocks." + VACIO,
    "e09_casa_cofre": "Wide background inside the stone hall of a paladin's family house: a heavy iron-bound chest with a big lock in a "
        "corner under a staircase, weapon racks, a shield on the wall, a small staircase going up on the left, dim candlelight." + INTERIOR,
    # Lordaeron / Mano de Plata
    "e10_lordaeron_campos": "Wide background of the Kingdom of Lordaeron (World of Warcraft) in peace on a golden summer afternoon: "
        "endless golden wheat fields, windmills, a white walled city with tall spires and a cathedral far on the horizon, a road "
        "with carts." + CALIDO + VACIO,
    "e11_catedral_orden": "Wide background inside a grand white stone cathedral in Lordaeron: tall stained-glass windows without "
        "figures casting golden light, an altar with candles, blue and gold banners of the Silver Hand, polished floor." + CALIDO + INTERIOR,
    "e12_graneros_andorhal": "Wide background of the great granaries of the town of Andorhal (World of Warcraft) on an overcast day: "
        "huge wooden barns and grain silos, stacked burlap grain sacks, carts loaded with sacks on the road, a sickly green glow "
        "leaking from one open barn door, heavy grey clouds." + VACIO,
    # Costasur
    "e13_costasur_noche": "Wide background at night of the small coastal town of Southshore (World of Warcraft): timber houses with "
        "steep roofs by a calm moonlit sea, a wooden pier, an inn with warm lit windows, lanterns." + VACIO,
    "e14_posada_mesa": "Wide background inside the common room of a medieval inn at night: a long heavy wooden table in the center "
        "with candles, a stone fireplace, wooden beams, a wooden staircase on the right side going up to a dark landing, barrels." + INTERIOR,
    # Forja
    "e15_gran_yunque": "Wide background of the Great Forge of Ironforge (World of Warcraft): a colossal dwarven hall carved into the "
        "mountain, a giant anvil on a stone platform in the center, rivers of molten metal, huge stone pillars, glowing orange "
        "furnaces, sparks." + VACIO,
    "e16_vega_ataque": "Wide background at dusk of the village of Hearthglen (World of Warcraft) with a great stone keep on a hill, "
        "half-timbered houses, a palisade, burning fields, plague-green fog rolling in from the forest, an ominous sunset." + VACIO,
    # Tirion y Eitrigg
    "e17_bosque_vega": "Wide background of a dense northern forest near Hearthglen in late autumn: tall pines and golden birches, "
        "mossy rocks, shafts of morning light, a narrow hunting trail." + CALIDO + VACIO,
    "e18_torre_ruinas": "Wide background of an old ruined round stone watchtower overgrown with ivy deep in a forest, its top half "
        "collapsed, rubble and fallen stones around, a campfire pit with a small cooking pot, morning mist." + VACIO,
    "e19_alcoba_tirion": "Wide background of a lord's bedroom in a stone keep: a big bed with blue blankets, a window with daylight, a "
        "painted family portrait on the wall left blank, a suit of armor on a stand, a chair." + CALIDO + INTERIOR,
    # juicio
    "e20_sala_juicio": "Wide background inside the great judgement hall of the city of Stratholme before the plague: a raised wooden "
        "judges' table on a dais with tall chairs, blue and gold banners, a crowd balcony, cold grey light from high windows, a "
        "single empty spot for the accused in the center." + INTERIOR,
    "e21_tumba_falsa": "Wide background on a grey drizzly day: a small lonely grave mound with a simple wooden marker with no letters "
        "in a quiet field of the Undercroft, a few wild flowers, distant hills, low clouds." + VACIO,
    "e22_plaza_ejecucion": "Wide background of a city square in Stratholme with a wooden execution scaffold, guard towers, timber and "
        "stone houses, a grey sky, torches, an empty cobbled square." + VACIO,
    "e23_colina_horda": "Wide background of rocky hills outside a city at dusk, a small orc war camp with brown tents and spiked "
        "banners without symbols on the ridge, smoke of campfires, orange sky." + VACIO,
    # la Plaga
    "e24_stratholme_arde": "Wide background of the great walled city of Stratholme (World of Warcraft) burning at night, seen from "
        "outside: tall towers on fire, plague-green smoke, the main gate, dead trees and a road with abandoned carts." + VACIO,
    "e25_stratholme_calle": "Wide background inside a ruined street of plague-ridden Stratholme at night: burning timber houses, "
        "collapsed buildings and rubble, green plague fog, broken carts, scattered weapons." + VACIO,
    "e26_sala_sombra": "Wide background inside a dark stone chapel room at night: a single candle, an altar, long purple-green "
        "shadows on the walls, a red Scarlet Crusade banner without symbols, an ominous demonic purple glow from the floor." + INTERIOR,
    # complot y traición
    "e27_pasillo_vega": "Wide background of a long dark corridor in a stone keep at night: tall arched windows with moonlight, red "
        "banners without symbols, suits of armor, a single torch, deep shadows." + INTERIOR,
    "e28_camino_monasterio": "Wide background of a muddy road through dark Tirisfal forest at dusk, an old stone monastery with red "
        "roofs far away on a hill, purple-grey sky, crows on branches." + VACIO,
    "e29_puertas_stratholme": "Wide background of the huge main gate of the city of Stratholme at grey dawn: massive stone walls and "
        "towers, the iron portcullis half open, a wide open dirt field in front, plague-green fog, dark clouds." + VACIO,
    "e30_campo_cenizas": "Wide background of a battlefield before city gates after a massacre: a wide field covered in grey ash and "
        "broken weapons, smoke rising, a cold pale sunrise behind the walls, crows." + VACIO,
    "e31_cadaveres_lluvia": "Wide background under heavy night rain: a muddy field with mounds of broken undead remains and armor, "
        "pools of dark water, lightning far away, oppressive mood." + VACIO,
    "e32_camara_secreta": "Wide background of a hidden stone chamber behind a bookcase inside a monastery: dust, cobwebs, a narrow "
        "slit of light, an old wooden bench, red candles melted, a forgotten cloak on the floor." + INTERIOR,
    # Naxxramas
    "e33_naxx_cielo": "Wide background of Naxxramas, a huge dark floating necropolis ziggurat of black stone with green glowing runes, "
        "hovering in a sickly green sky over a rotting forest of the Eastern Plaguelands, chains hanging, gargoyles circling." + VACIO,
    "e34_naxx_sala": "Wide background inside Naxxramas: a vast dark hall of black stone and iron with green flames in braziers, "
        "chains, bones, tall pillars, a platform with four empty thrones in the background." + INTERIOR,
    "e35_naxx_ritual": "Wide background of a necromantic ritual chamber: a stone slab altar in the center under a cold blue-green "
        "light from above, runic circles on the floor, frost on the walls, floating dust." + INTERIOR,
    "e36_vacio_espada": "Wide background of a dark otherworldly void: swirling black smoke and sickly green mist, faint ghostly "
        "shapes in the fog, a single dim green light in the center." + " No people, no animals.",
    # culpa / Cruzada
    "e37_catedral_escarlata": "Wide background inside the Scarlet Monastery cathedral (World of Warcraft): a crimson and gold "
        "cathedral nave with red banners without symbols, stained glass windows, a long red carpet to an altar, rows of pews, "
        "candle light." + INTERIOR,
    "e38_tumba_rota": "Wide background at night of a broken shattered gravestone beside a family house in Tirisfal Glades, cracked "
        "stone pieces on the ground, a cold wind, purple-black sky." + VACIO,
    "e39_casa_arde": "Wide background at night of a stone and timber family house in flames, fire roaring from the windows and the "
        "roof, sparks and smoke against a purple night sky, tall dark pines." + VACIO,
    "e40_taberna_libro": "Wide background of a quiet corner of a cosy tavern at night: a wooden table with an open storybook and a "
        "lantern, shelves with jars, a small fire, warm amber light." + INTERIOR,
    # Darion busca
    "e41_taberna_oscura": "Wide background of a gloomy tavern at night: rough tables with empty mugs, a smoky hearth, a troll voodoo "
        "mask on the wall, bottles, dim green and orange light." + INTERIOR,
    "e42_campamento_orvallo": "Wide background of Chillwind Camp in the Western Plaguelands: a small military camp of tents and "
        "wooden palisades with purple Argent Dawn banners without symbols, a campfire, cold misty pine forest." + VACIO,
    "e43_naxx_pasillo": "Wide background of a long dark corridor inside a necropolis: black stone, ribs of bone as arches, green "
        "glowing runes, webs, a green mist on the floor." + INTERIOR,
    # Monasterio
    "e44_monasterio_ext": "Wide background of the Scarlet Monastery (World of Warcraft) in Tirisfal Glades at dusk: a great stone "
        "monastery with red roofs and a tall cathedral tower, red banners, a courtyard, purple sky, dark forest." + VACIO,
    "e45_catedral_altar": "Close wide background of the altar area of a crimson cathedral: a raised altar with tall candles, a huge "
        "red stained glass window, red banners, steps, smoke of incense, green fire reflections." + INTERIOR,
    # misterio
    "e46_escritorio": "Wide background of an old desk at night seen slightly from above: scattered parchments, an old map pinned with "
        "daggers, a candle, a quill and ink, a magnifying glass, books." + " Strong depth. No people.",
    # ermitaño
    "e47_cabana_rio": "Wide background of a lonely hermit's log cabin beside a dark river in the Eastern Plaguelands: a wooden porch, a "
        "woodpile, a horse hitching post, a smoking chimney, dead trees and grey fog around, a sliver of light from the door." + VACIO,
    "e48_cabana_dentro": "Wide background inside a hermit's small log cabin: a rough table with bread and cheese, a fireplace, a war "
        "hammer leaning on the wall, a cot with furs, a small window." + INTERIOR,
    # Taelan
    "e49_mardenholde": "Wide background of Mardenholde Keep in Hearthglen occupied by the Scarlet Crusade: a great grey stone fortress "
        "with crimson banners without symbols, a gate, guards' braziers, a grey cloudy sky." + VACIO,
    "e50_mirador_bosque": "Wide background of the edge of a forest on a hill overlooking a distant stone fortress with red banners, "
        "seen from behind bushes and trees, morning fog." + VACIO,
    # recuerdos
    "e51_vallenorte": "Wide background of the ruined farmland of Northdale in the Eastern Plaguelands: broken fences, a ruined barn, "
        "a dead field, plague fog." + VACIO,
    "e52_castel_darrow": "Wide background of the beach of Caer Darrow at dusk: a calm lake, a sandy shore, a castle on an island in "
        "the distance, soft golden light, a faint ghostly blue mist." + CALIDO + VACIO,
    "e53_bastion_cuadros": "Wide background inside a ruined Scarlet bastion hall in Stratholme: walls with several hanging framed "
        "paintings with blank canvases, a big painting of two moons, broken furniture, dust, candlelight." + INTERIOR,
    "e54_tumba_uther": "Wide background of Uther's Tomb in the Western Plaguelands (World of Warcraft): a white stone mausoleum with "
        "columns and a statue of a paladin on top, a calm lake, a grey sky." + VACIO,
    "e55_mardenholde_sala": "Wide background inside the great hall of Mardenholde Keep at night: a long hall with crimson banners, a "
        "throne-like chair, a table with a small wrapped gift box, torches, stone floor." + INTERIOR,
    "e56_camino_torre": "Wide background of a forest road at night leading to a small stone watchtower at the forest edge, torches "
        "on the tower, moonlight through the trees." + VACIO,
    "e57_torre_vigia": "Wide background in front of a small round stone watchtower beside a forest road at night: a wooden door, "
        "torches, a red banner without symbols, open ground in front." + VACIO,
    # Capilla primera batalla
    "e58_capilla_asedio": "Wide background at night of Light's Hope Chapel on its hill under siege: the chapel with warm golden "
        "windows, wooden barricades, a dead plain in front full of green fog, gargoyles in a dark green sky, two dark armies far on "
        "the horizon." + VACIO,
    "e59_capilla_luz": "Wide background of the ground around Light's Hope Chapel erupting with hundreds of tall columns of brilliant "
        "golden holy light shooting up into the night sky, glowing cracks in the earth, ash floating." + VACIO,
    # Acherus
    "e60_acherus": "Wide background of Acherus the Ebon Hold, a dark floating death knight necropolis with spikes and runes hovering "
        "over the Eastern Plaguelands, ice-blue glow, a dark sky." + VACIO,
    "e61_enclave_arde": "Wide background of the Scarlet Enclave burning: a coastal town with red-roofed houses and a church on fire, "
        "black smoke, a death knight banner, a dark sea." + VACIO,
    # La luz del alba
    "e62_fosa_sangre": "Wide background of a huge battlefield at night before Light's Hope Chapel: a pit of corpses, a dark plain "
        "covered with undead silhouettes far away, blood-red rain, lightning, the small chapel glowing gold on the hill." + VACIO,
    "e63_capilla_alba": "Wide background of Light's Hope Chapel at dawn after the battle: golden sunrise light breaking through red "
        "clouds, rays of light on the white chapel, mist on the dead plain turning gold." + VACIO,
    # epílogo
    "e64_trono_helado": "Wide background of the top of Icecrown Citadel (World of Warcraft): the Frozen Throne on a spire of ice "
        "under a dark stormy sky, icy platform, blue frost glow, snowstorm." + VACIO,
    "e65_costa_abrupta": "Wide background of the Broken Shore: a ruined coast with broken temples, green fel fire, a burning sky with "
        "green comets, dark sea." + VACIO,
    "e66_santuario": "Wide background of a quiet underground stone crypt beneath a chapel: a stone tomb with a sword carved on the lid, "
        "candles, golden light falling from above, peaceful mood." + INTERIOR,
}

HOJAS = {
    "h01_alexandros_hoja": "Character model sheet" + HOJA + ": " + ALEX + ". The SAME man drawn 6 times," + FILA + ": standing "
        "proud holding " + ESPADA + " point down; swinging the greatsword overhead in a heroic strike; holding a crying newborn baby "
        "wrapped in a cloth in his arms; kneeling exhausted on one knee, empty-handed; walking side view facing right; reaching out "
        "a hand toward something, worried." + NOSOMBRA,
    "h02_alexandros_dk": "Character model sheet" + HOJA + ": Highlord Mograine as a death knight: the same tall man now undead, pale "
        "grey-blue skin, glowing ice-blue eyes, long dark hair, spiked black and silver death knight plate armor with skulls, a "
        "tattered black cape, holding " + CORRUPTA + ". The SAME figure drawn 5 times," + FILA + ": standing menacing; raising the "
        "black sword; pointing at the viewer; floating as a translucent ghost with arms open; kneeling in chains." + NOSOMBRA,
    "h03_renault_hoja": "Character model sheet" + HOJA + ": " + RENAULT + ", in a silver paladin breastplate and a dark grey cloak. "
        "The SAME man drawn 6 times," + FILA + ": standing with arms crossed, jealous; whispering, hand by his mouth; running and "
        "pointing back, alarmed; raising a big greatsword with both hands to stab downward; standing frozen staring in horror; "
        "walking side view facing right." + NOSOMBRA,
    "h04_renault_escarlata": "Character model sheet" + HOJA + ": " + RENAULT + ", now Scarlet Commander: red and white tabard of the "
        "Scarlet Crusade over silver plate, a red cape, a big war hammer. The SAME man drawn 5 times," + FILA + ": standing proudly; "
        "kneeling begging with his hands together, crying; smashing down with his war hammer; lying in bed awake with fear (only "
        "the figure, no bed); covering his face with his hands." + NOSOMBRA,
    "h05_darion_hoja": "Character model sheet" + HOJA + ": " + DARION + ". The SAME young man drawn 6 times," + FILA + ": standing "
        "determined; sitting slumped holding a mug, defeated; walking side view facing right; holding " + CORRUPTA + " with both "
        "hands; lying on the ground hurt, leaning on one elbow; kneeling and stabbing a sword into his own chest with eyes closed "
        "(no blood)." + NOSOMBRA,
    "h06_darion_dk": "Character model sheet" + HOJA + ": Darion Mograine as a death knight: pale grey skin, glowing ice-blue eyes, "
        "wild black hair, black spiked runic plate armor, a dark cape, holding " + CORRUPTA + ". The SAME figure drawn 6 times," + FILA
        + ": standing commanding with the sword raised; shouting with one arm raised to the sky; struggling as the sword pulls "
        "away from his hands; kneeling trapped, head down; throwing the sword forward with all his strength; standing calm with a "
        "fist on his chest, swearing an oath." + NOSOMBRA,
    "h07_darion_nino": "Character sheet" + HOJA + ": young Darion Mograine at 12 and his father " + ALEX + "," + FILA + ": the boy "
        "hugging his father; the father kneeling with his hand on the boy's shoulder; the boy holding a wooden practice sword; the boy "
        "peeking from behind a staircase railing, curious; Renault Mograine as a boy of 15 with slick black hair, peeking and "
        "jealous; the two boys whispering together." + NOSOMBRA,
    "h08_tirion_joven": "Character model sheet" + HOJA + ": " + TIRION_J + ". The SAME man drawn 6 times," + FILA + ": standing "
        "proudly; on his knees in shame with his head bowed; fighting with a war hammer; laying his glowing golden hands on someone "
        "(healing pose, kneeling); walking side view facing right; holding out an open hand, pleading." + NOSOMBRA,
    "h09_tirion_viejo": "Character model sheet" + HOJA + ": " + TIRION_V + ". The SAME old man drawn 6 times," + FILA + ": standing "
        "with a heavy war hammer on his shoulder, grumpy; sitting and eating bread; holding a big sword with both hands, eyes closed, "
        "praying; kneeling and crying, hugging someone (arms forming an embrace); watching from behind a tree, sad; walking side "
        "view facing right with his hammer." + NOSOMBRA,
    "h10_tirion_highlord": "Character model sheet" + HOJA + ": old Tirion Fordring with long white hair and a white beard in shining "
        "golden-white highlord plate armor with a blue tabard, wielding " + ESPADA + " glowing with holy golden light. The SAME old "
        "man drawn 6 times," + FILA + ": catching the sword in the air with one hand; charging forward with the sword; standing tall "
        "raising the sword to the sky; kneeling crushed by dark magic; laying his glowing hands on someone; standing on a frozen "
        "platform breaking out of ice." + NOSOMBRA,
    "h11_taelan_hoja": "Character model sheet" + HOJA + ": " + TAELAN + ". The SAME man drawn 6 times," + FILA + ": standing stiff and "
        "proud; kneeling with an open gift box, screaming in grief; holding a small wooden toy hammer in both hands, tears in his "
        "eyes; riding pose sitting (no horse); falling backwards struck by light; lying dead on the ground, peaceful." + NOSOMBRA,
    "h12_familias_hoja": "Character sheet" + HOJA + ", 6 different figures," + FILA + ": Elena Mograine, a gentle woman with long "
        "auburn hair in a green dress, smiling; Elena pale in bed clothes holding a newborn baby; Karandra Fordring, a woman of 30 "
        "with a long brown braid in a blue noble dress, worried; Karandra holding the hand of a little boy of 7 with brown hair in a "
        "blue tunic holding a small wooden toy hammer; the same little boy kneeling burying the toy hammer; Elena as a pale ghost "
        "pointing accusingly." + NOSOMBRA,
    "h13_eitrigg_hoja": "Character model sheet" + HOJA + ": Eitrigg, an old orc warrior: green skin, long white hair in a topknot, a "
        "white braided beard, tusks, a scarred face, heavy orcish leather and iron armor, a big axe. The SAME orc drawn 6 times,"
        + FILA + ": standing wary with the axe; carrying an unconscious man in armor on his shoulder; sitting by a fire telling a "
        "story; in chains, kneeling; lying wounded on the ground; placing a fist on his heart, solemn." + NOSOMBRA,
    "h14_isillien_hoja": "Character model sheet" + HOJA + ": Grand Inquisitor Isillien, an old bald human with a cruel thin face and a "
        "white goatee, crimson and white inquisitor robes with gold trim, a red mantle, a golden staff. The SAME man drawn 5 times,"
        + FILA + ": standing arrogantly; laughing cruelly; casting a beam of golden holy light from his hand; raising his hands at a "
        "glowing orb; falling defeated." + NOSOMBRA,
    "h15_villanos_hoja": "Character sheet" + HOJA + ", 6 different figures," + FILA + ": Kel'Thuzad, a floating lich with a skeletal "
        "body in dark blue and purple robes, a crowned skull with glowing blue eyes and an icy aura; Kel'Thuzad raising bony hands "
        "casting green-blue necromantic magic; the Lich King, a tall figure in spiked dark steel armor with a horned skull helm and "
        "glowing blue eyes, holding Frostmourne, a huge runeblade with blue runes; the Lich King raising Frostmourne casting; "
        "Grand Crusader Dathrohan, an old grey-haired paladin in red and gold Scarlet armor; Balnazzar, a huge purple-skinned "
        "dreadlord demon with bat wings, horns and hooves." + NOSOMBRA,
    "h16_consejo_hoja": "Character sheet" + HOJA + ", 6 different human figures of Lordaeron," + FILA + ": Uther the Lightbringer, a "
        "bald paladin with a white beard in silver armor with a hammer; Archbishop Alonsus Faol, an old priest in white and gold "
        "robes with a tall mitre; Archmage Antonidas, an old mage with a long white beard in purple robes; young Prince Arthas, "
        "blond, in silver and blue princely armor; High Inquisitor Fairbanks, a bald priest in white robes with red trim; "
        "Barthilas, a sly human lieutenant with black hair and a pointed beard in a grey uniform." + NOSOMBRA,
    "h17_magni_hoja": "Character sheet" + HOJA + "," + FILA + ": King Magni Bronzebeard, a huge dwarf with a long braided red-brown "
        "beard and a golden crown, heavy dwarven armor, hammering on an anvil with a giant smithing hammer; Magni sad with his head "
        "bowed; Magni holding up a finished shining greatsword proudly; Zabra Hexx, a thin blue-skinned troll priest with tusks and "
        "voodoo robes, pointing up mysteriously; Myranda the Hag, an old hooded woman in grey robes casting a purple illusion spell; "
        "Artist Renfray, a ghostly woman painter with a brush and palette." + NOSOMBRA,
    "h18_dk_hoja": "Character sheet" + HOJA + ", 6 death knights of World of Warcraft," + FILA + ": Koltira Deathweaver, a blood elf "
        "death knight with long white hair and black runic armor; Thassarian, a human death knight with two swords; Orbaz Bloodbane, "
        "a scarred death knight running away; a generic death knight on one knee; a death knight raising a runeblade; a death "
        "knight trapped kneeling in a sphere of golden light." + NOSOMBRA,
    "h19_cruzados_hoja": "Character sheet" + HOJA + ", 6 soldiers of the Scarlet Crusade in red and white tabards over silver armor "
        "with red capes," + FILA + ": a crusader with a sword and shield; an archer; a crusader kneeling in prayer; a crusader "
        "holding a red banner; a fanatic priest in red robes; a crusader charging with a spear." + NOSOMBRA,
    "h20_defensores_hoja": "Character sheet" + HOJA + ", 6 defenders of the Argent Dawn in purple and white tabards over silver armor,"
        + FILA + ": a soldier with a spear and shield; a priest in white robes with glowing hands; an archer; Lord Maxwell Tyrosus, an "
        "old grey-bearded commander in heavy armor; a woman mage in purple robes casting frost; a young volunteer with a pitchfork, "
        "scared." + NOSOMBRA,
    "h21_plaga_hoja": "Character sheet" + HOJA + ", 6 different undead monsters of the Scourge (World of Warcraft)," + FILA + ": a "
        "hunched ghoul with long claws; a huge stitched abomination with hooks and a cleaver; a skeleton warrior with a rusty sword; "
        "a floating pale banshee with long white hair; a skeletal mage casting green magic; a necromancer in black robes." + NOSOMBRA,
    "h22_necrofago_corre": "Animation sprite sheet" + HOJA + ": run cycle of a hunched grey-green undead ghoul with long claws and "
        "torn rags. The SAME ghoul" + CICLO + " running stride." + NOSOMBRA,
    "h23_esqueleto_camina": "Animation sprite sheet" + HOJA + ": walk cycle of an undead skeleton warrior with a rusty sword and a "
        "broken shield held close to the body. The SAME skeleton" + CICLO + " walking step." + NOSOMBRA,
    "h24_mirador_galope": "Animation sprite sheet" + HOJA + ": gallop cycle of old Tirion Fordring (long white hair and white beard, "
        "fur cloak) riding his strong white warhorse Mirador with blue barding. The SAME horse and rider drawn 6 times in a single "
        "horizontal row, strict side view facing right, full body, same size, evenly spaced with wide gaps and not touching, each "
        "drawing a consecutive phase of one gallop stride." + NOSOMBRA,
    "h25_caballo_muerte_galope": "Animation sprite sheet" + HOJA + ": gallop cycle of a death knight in spiked black armor riding a "
        "skeletal undead horse with glowing blue eyes and black barding. The SAME horse and rider drawn 6 times in a single "
        "horizontal row, strict side view facing right, full body, same size, evenly spaced with wide gaps and not touching, each "
        "drawing a consecutive phase of one gallop stride." + NOSOMBRA,
    "h26_gargola_aleteo": "Animation sprite sheet" + HOJA + ": a row of 6 drawings of the same grey stone gargoyle of the Scourge with "
        "bat wings, side view facing right, showing a wing-flap cycle, evenly spaced and not touching." + NOSOMBRA,
    "h27_taelan_galope": "Animation sprite sheet" + HOJA + ": gallop cycle of " + TAELAN + " riding a brown warhorse with red "
        "barding. The SAME horse and rider drawn 6 times in a single horizontal row, strict side view facing right, full body, same "
        "size, evenly spaced with wide gaps and not touching, each drawing a consecutive phase of one gallop stride." + NOSOMBRA,
    "h28_utileria": "Prop sheet" + HOJA + ", 16 separate objects evenly spaced in a 4x4 grid, never touching or overlapping: a dark "
        "orb crackling with black and purple energy; a pure shining golden-white crystal; a heavy iron-bound chest; " + ESPADA + "; "
        + CORRUPTA + "; Frostmourne, a huge runeblade with blue runes; a small wooden toy hammer; a blue and gold banner of the "
        "Silver Hand with a golden hand; a framed painted family portrait of a man, a woman and a little boy on a beach; a small "
        "wrapped gift box with a ribbon; a cracked broken gravestone; a lit candle; an old leather-bound book; a glowing blue soul "
        "gem shard; a dwarven anvil; a big smithing hammer." + NOSOMBRA,
    "h29_utileria2": "Prop sheet" + HOJA + ", 16 separate objects evenly spaced in a 4x4 grid, never touching or overlapping: a "
        "wooden baby cradle; a wooden siege ballista; a wooden barricade of sharpened stakes; a red Scarlet Crusade banner; a purple "
        "Argent Dawn banner; a black death knight banner with a skull; a burning torch; a tankard of ale; bread and cheese on a "
        "plate; a goblet; an iron helm of domination with spikes; iron chains; a wooden practice sword; an orcish axe; a silver "
        "paladin war hammer; a round shield with a golden hand." + NOSOMBRA,
    "h30_fx_hoja": "Element sheet" + HOJA + ", 8 separate painted elements evenly spaced, never touching: a column of golden holy "
        "light; a burst of golden holy light; a swirl of sickly green necromantic fire; a cloud of green plague fog; a puff of grey "
        "ash; a big orange fire flame; a crack of ice-blue frost; a dark purple shadow smoke." + NOSOMBRA,
}

P = {k: E + v + C for k, v in {**ESC, **HOJAS}.items()}
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(ESC), "escenarios +", len(HOJAS), "hojas =", len(P), "prompts")
