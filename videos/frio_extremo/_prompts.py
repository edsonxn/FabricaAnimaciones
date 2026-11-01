# -*- coding: utf-8 -*-
"""Escribe prompts.json (escenarios + hojas de Flow) con la FICHA de guion.py. Ejecutar desde la carpeta del video.
Una sola tanda (21-oct-2026): 37 escenarios (uno por lugar/hora; la variante b = segundo encuadre) + 18 hojas."""
import json
import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
PJ = F["personajes"]
VACIO = " Strong depth: foreground, midground and background layers. Open empty ground across the lower third. No people, no animals."
INTERIOR = " Strong depth: foreground, midground and background layers. Open empty floor across the lower third. No people."
FILA = " full body, evenly spaced in one row with generous empty white space between them, never touching or overlapping"
HOJA = " on a plain flat pure white background"
GRIS = " on a plain flat medium-grey background"         # para piezas BLANCAS (nieve, hielo): en blanco se pierden al recortar
NOSOMBRA = " Every figure has a continuous dark ink outline. No ground, no cast shadows."
HOY = "Same art style, but this picture is set in the present day: "
CICLO = (" The SAME {q} drawn {n} times in a single horizontal row, strict side view facing right, full body, same size and same "
         "height, evenly spaced with wide gaps and not touching, each drawing a consecutive phase of one {acc}.")

ESC = {
    # ---- hook
    "01_sala_moderna": HOY + "Wide background of a cozy modern living room on a snowy winter night: a big window with falling snow "
        "and a dark blue night outside, a radiator heater under the window, a sofa with a blanket, a coat rack with a puffer jacket, "
        "a warm floor lamp, a rug, a houseplant." + INTERIOR,
    "02_ventisca_noche": "Wide background of an endless Ice Age tundra at night in a howling blizzard: snow blowing sideways, "
        "drifts and frozen grass, a dark blue-black sky, a faint cold moon behind the storm, nowhere to shelter, a single frozen "
        "dead shrub." + VACIO,
    "03_sabana_africa": "Same art style, but warm: Wide background of the hot African savanna about 200,000 years ago under a "
        "blazing sun: golden grass, acacia trees, a shimmering heat haze, distant blue hills, a dry riverbed, a big pale-yellow sky."
        + VACIO,
    "04_mapa_mundo": "Wide background: a hand-painted old world map on a big stretched animal hide seen from straight above, filling "
        "the whole frame, showing the real continents during the Ice Age: Africa, Europe, Asia, the Americas and Australia in warm "
        "sand colours, huge white ice sheets over northern North America and northern Europe, Siberia joined to Alaska by a land "
        "bridge, pale blue painted oceans. No routes, no lines, no labels.",
    "05_cueva_fondo": "Wide background of the deep dark back of a cave: damp rock walls, dripping stalactites, a puddle, cold "
        "blue-black shadows, a small weak fire's glow at the centre of the floor, nothing else." + INTERIOR,
    # ---- hielo
    "06_glaciar_canada": "Wide background of the edge of a colossal Ice Age ice sheet: a towering wall of blue-white glacier ice "
        "kilometres high, cracked and layered, filling the horizon, meltwater streams and gravel at its foot, a tiny frozen lake, "
        "an overcast cold sky. A feeling of enormous scale." + VACIO,
    "07_costa_mar_bajo": "Wide background of an Ice Age coastline where the sea has drawn far back: a wide exposed sandy plain with "
        "old stranded seashells and rocks, the sea a thin blue line far away on the horizon, snowy hills, a grey-blue sky."
        + VACIO,
    "08_estepa_mamut": "Wide background of the Ice Age mammoth steppe on a bright cold day: endless dry golden-grey grassland with "
        "snow patches, gentle hills, a frozen river winding, a distant white glacier on the horizon, big pale-blue sky with long "
        "clouds." + VACIO,
    "09_estepa_atardecer": "Wide background of the Ice Age mammoth steppe at cold dusk: dry grass bending in the wind, snow drifts, "
        "the last orange glow of the sun on the horizon and a deep blue night coming down, the first stars." + VACIO,
    # ---- cuerpo
    "10_campamento_viento": "Wide background of a small Ice Age camp on a windy grey snowy day: two simple hide tents, a cold "
        "unlit hearth ring of stones, a wooden drying rack with hides, footprints in the snow, a low hill behind." + VACIO,
    "11_bosque_neandertal": "Wide background of a snowy pine forest in Ice Age Europe about 60,000 years ago: dark green pines "
        "heavy with snow, a limestone cliff with a shallow rock shelter, a frozen stream, soft falling snow." + VACIO,
    "12_groenlandia_costa": "Wide background of the Arctic coast of Greenland: deep blue sea with floating icebergs, snowy dark "
        "mountains, a pebble shore with two skin kayaks pulled up, drying racks with fish, a pale pink-blue polar sky." + VACIO,
    # ---- fuego
    "13_cueva_sudafrica": "Same art style, but warm: Wide background of the wide entrance of a big cave in a red-brown rocky hill of "
        "South Africa, the cave mouth opening into darkness, scrubland and a warm evening sky outside, an old ash-covered hearth "
        "spot on the floor near the entrance." + VACIO,
    "14_campamento_fuego": "Wide background of an open-air Ice Age camp at night: a big stone-ringed hearth in the middle with a "
        "bright campfire, hide tents glowing orange around it, snowy ground, a dark starry sky, the dark steppe beyond." + VACIO,
    "15_estepa_sin_arboles": "Wide background of a treeless frozen steppe in winter: flat snowy plain, not a single tree in sight, "
        "low grey sky, old bleached mammoth bones and a big skull half-buried in the snow." + VACIO,
    "16_cueva_pinturas": "Wide background inside a decorated cave: rock walls and ceiling covered with red, black and ochre "
        "prehistoric paintings of horses, bulls and deer, dim warm flickering light, a flat rock ledge in front." + INTERIOR,
    "17_refugio_camas": "Same art style, but warm: Wide background of a rock shelter in South Africa at evening: a shallow overhang "
        "of warm sandstone, a hearth with glowing embers, a grey layer of ash on the floor, bundles of dry grass, the valley "
        "below." + INTERIOR,
    # ---- ropa
    "18_taller_pieles": "Wide background of an Ice Age camp workshop on a clear cold morning: animal hides stretched on wooden "
        "frames to dry, a flat stone work table with scrapers, a pile of furs, hide tents, snowy ground, blue sky." + VACIO,
    "19_bosque_pelo": "Wide background: a giant close-up macro view of human hair like a fantastic forest, tall brown hair strands "
        "rising like tree trunks from a soft peach-coloured skin ground, warm soft light, funny and a little cute." + VACIO,
    "20_cueva_siberia": "Wide background of the entrance of a cave in a rocky cliff of the snowy Altai mountains of Siberia: birch "
        "trees, a river valley below, snowy peaks, a cold clear sky." + VACIO,
    "21_excavacion_rusia": "Same art style, but in the present day: Wide background of an archaeological excavation in a birch "
        "forest in Russia: a rectangular dig pit with string grid lines, a trowel and brushes on the edge, a wooden ladder, "
        "buckets, soft autumn light." + VACIO,
    "22_campamento_sol": "Wide background of a busy-looking but empty Ice Age winter camp on a sunny day: round hide huts, a "
        "drying rack, a hearth with thin smoke, sparkling snow, birch trees, a bright blue sky." + VACIO,
    # ---- cuevas
    "23_abrigo_entrada": "Wide background of a big rock shelter at the edge of a valley in Ice Age France: a wide overhanging "
        "limestone roof, daylight pouring in, a hearth near the edge with smoke going out, a view of a snowy valley and a river."
        + VACIO,
    "24_cueva_humeda": "Wide background of the cold damp inside of a cave: wet glistening rock walls, water drops, total darkness "
        "at the back, a little grey daylight from far behind, puddles on the floor." + INTERIOR,
    "25_rio_don": "Wide background of the wide valley of the river Don in Russia during the Ice Age, winter: a broad frozen river, "
        "low chalky banks, an endless snowy plain without trees, a pale low sun." + VACIO,
    "26_casa_mamut": "Wide background of a large round prehistoric house built from mammoth bones on a snowy plain: walls of "
        "stacked mammoth skulls, jawbones and leg bones laid like bricks, huge curved tusks arching over the doorway, animal hides "
        "stretched over the roof, thin smoke rising, the frozen Don valley behind. Open empty snow across the lower third. No "
        "people, no animals.",
    "27_casa_mamut_dentro": "Wide background inside a round mammoth-bone house: walls of stacked mammoth bones and skulls, hides "
        "covering the roof, a fire pit in the middle glowing, furs on the floor, a pile of bones for fuel, warm orange light."
        + INTERIOR,
    # ---- noche
    "28_choza_noche": "Wide background of a small round hide hut on the open steppe at night in a snowstorm: snow hitting the hides, "
        "a warm orange glow leaking from the doorway flap, wind-blown snow, a dark blue night." + VACIO,
    "29_choza_dentro": "Wide background inside a small hide hut at night: a crackling fire in a stone hearth, furs and hides on the "
        "floor, a wooden rack with fur clothes and boots drying near the fire, a leather water bag, a bone pot, warm orange light "
        "and cold blue shadows at the edges." + INTERIOR,
    # ---- artico
    "30_artico_noche": "Wide background of an Ice Age hunters' camp on a frozen river in the Arctic in the long polar night: green "
        "and violet northern lights in the sky, hide tents with orange glow, snow, a frozen river with ice ridges, dark hills."
        + VACIO,
    "31_puente_bering": "Wide background of the Bering land bridge in the Ice Age: a wide grassy and snowy plain joining two "
        "continents, cold sea visible on both sides far away, low hills, a pale sun low on the horizon." + VACIO,
    # ---- iglu
    "32_iglu_fuera": "Wide background of a snow igloo standing alone on Arctic sea ice at blue twilight: a perfect dome of snow "
        "blocks with a low entrance tunnel, a sled beside it, a warm glow from a small ice window, snowdrifts, pastel pink and "
        "blue sky." + VACIO,
    "33_iglu_corte": "Wide background: a cutaway cross-section side view of an igloo on the sea ice, like a cozy educational "
        "illustration: the snow-block dome cut in half showing the inside, a low entrance tunnel that dips BELOW the floor level, a "
        "raised sleeping platform covered in furs at the back, a small stone oil lamp, a small vent hole at the top. Empty, no "
        "people.",
    "34_iglu_dentro": "Wide background inside an igloo: a curved dome of snow blocks glowing warm, a raised sleeping platform "
        "covered with thick caribou furs, a soapstone seal-oil lamp with a small flame, drying mittens, the low dark tunnel "
        "entrance at the side." + INTERIOR,
    # ---- tu / outro
    "35_casa_moderna_dia": HOY + "Wide background of a bright modern apartment on a winter morning: a bed with a thick mattress and "
        "duvet, a radiator heater, a coat hook with a puffer jacket, a window with snowy rooftops outside." + INTERIOR,
    "36_calle_helada": HOY + "Wide background of a quiet modern town street on a freezing winter evening: snow on parked cars and "
        "rooftops, icicles, warm lit windows, a bus stop shelter, street lamps." + VACIO,
    "37_ventana_nieve": HOY + "Wide background of a window seat at night: a big window with frost at the corners, soft snow "
        "falling outside over a city of lit windows, a cushion and a cup of hot tea on the sill, a warm lamp glow inside." + INTERIOR,
}

HOJAS = {
    "50_sapi_hoja": "Character model sheet" + HOJA + ": " + PJ["sapi"] + ". The SAME character drawn 6 times," + FILA + ": standing "
        "calm and smiling; talking with one hand open; pointing to the side; shivering and hugging himself with chattering teeth; "
        "surprised with his mouth open; holding up a burning torch proudly." + NOSOMBRA,
    "51_sapi_camina": "Animation sprite sheet" + HOJA + ": walk cycle of " + PJ["sapi"] + "." + CICLO.format(q="character", n=8,
        acc="walking step") + NOSOMBRA,
    "52_neandertal_hoja": "Character model sheet" + HOJA + ": " + PJ["neandertal"] + ". The SAME man drawn 6 times," + FILA + ": "
        "standing strong with arms crossed; kneeling and striking a flint hand-axe against a pyrite stone making sparks; crouching "
        "and blowing on a small fire; wrapped in a big loose hide cape like a blanket; carrying a big piece of meat on his shoulder; "
        "shivering with a loose hide on his shoulders and the wind blowing it open." + NOSOMBRA,
    "53_cazadora_hoja": "Character model sheet" + HOJA + ": " + PJ["cazadora"] + ". The SAME woman drawn 6 times," + FILA + ": "
        "sitting and sewing a fur with a bone needle; standing holding a spear; carrying a bundle of bones in her arms; kneeling "
        "and feeding a fire; scraping a hide with a stone tool; smiling and pointing up explaining." + NOSOMBRA,
    "54_cazadora_camina": "Animation sprite sheet" + HOJA + ": walk cycle of " + PJ["cazadora"] + ", walking through deep snow."
        + CICLO.format(q="woman", n=8, acc="walking step") + NOSOMBRA,
    "55_inuit_hoja": "Character model sheet" + HOJA + ": " + PJ["inuit"] + ". The SAME man drawn 6 times," + FILA + ": lifting a "
        "big snow block with both hands; cutting snow with a long bone snow knife; crawling on hands and knees; sitting cross-legged "
        "beside a small oil lamp; waving and smiling; holding a harpoon." + NOSOMBRA,
    "56_mamut_camina": "Animation sprite sheet" + HOJA + ": walk cycle of a cartoon woolly mammoth with shaggy reddish-brown fur, "
        "small ears, a hump and long curved tusks." + CICLO.format(q="mammoth", n=6, acc="walking step") + NOSOMBRA,
    "57_fauna_hoja": "Character sheet" + HOJA + ": 8 different cartoon Ice Age animals, each standing in side view," + FILA +
        ": a woolly rhinoceros; a reindeer with big antlers; a steppe bison; a stocky wild horse; a grey wolf; a brown cave bear; "
        "an arctic hare; a harbour seal lying down." + NOSOMBRA,
    "58_renos_camina": "Animation sprite sheet" + HOJA + ": walk cycle of a cartoon reindeer with big antlers and a grey-brown coat."
        + CICLO.format(q="reindeer", n=6, acc="walking step") + NOSOMBRA,
    "59_gente_hoja": "Character sheet" + HOJA + ": 6 different Ice Age people in brown and grey fur clothes," + FILA + ": an old "
        "grandmother with white hair holding a bone cup; a small child in a fur hood; a mother carrying a baby in a fur sling; a "
        "teenage boy carrying a leather water bag; a bearded man adding a bone to a fire; a young man yawning and stretching."
        + NOSOMBRA,
    "60_grupo_dormir": "Character sheet" + HOJA + ": 4 separate drawings," + FILA + ": a whole family of five Ice Age people "
        "sleeping huddled together under one big fur blanket with two children in the middle; three people sitting close together "
        "around nothing, hands out as if warming them at a fire; a man sitting awake hugging his knees keeping watch; two children "
        "giggling under a fur." + NOSOMBRA,
    "61_cazador_corre": "Animation sprite sheet" + HOJA + ": run cycle of an Ice Age hunter in a hooded grey fur parka with a spear "
        "held close to the body." + CICLO.format(q="hunter", n=8, acc="running stride") + NOSOMBRA,
    "62_cuervos_aleteo": "Animation sprite sheet" + HOJA + ": a row of 6 drawings of the same black raven showing a wing-flap cycle, "
        "side view facing right, evenly spaced and not touching." + NOSOMBRA,
    "63_utileria_fuego": "Prop sheet" + HOJA + ", 16 separate Ice Age objects evenly spaced in a 4x4 grid, never touching or "
        "overlapping: a small campfire with orange flames on a ring of stones; a big campfire; a grey flint hand-axe; a shiny "
        "golden pyrite stone; a carved sandstone oil lamp with a small flame; a big mammoth leg bone; a broken bone showing yellow "
        "marrow; a bundle of dry grass tied with a cord; a bed of green grass on grey ash; a pile of burning bones; a leather "
        "water bag; a bone cup; a stone pot with melting snow; a raw slab of fat; a roasted piece of meat on a stick; a pile of "
        "small burning embers." + NOSOMBRA,
    "64_utileria_ropa": "Prop sheet" + HOJA + ", 16 separate objects evenly spaced in a 4x4 grid, never touching or overlapping: a "
        "long bone needle with an eye; a coil of sinew thread; a string of small ivory beads; a hooded fur parka; a pair of fur "
        "trousers; a pair of fur boots; a fur cap decorated with ivory beads; a loose rough animal hide; a small ivory figurine of "
        "a person wearing a hooded suit; a pair of fur mittens; a stone scraper; a caribou fur parka with a big hood; a tiny brown "
        "cartoon louse with big eyes and six little legs; a second tiny grey cartoon louse with big eyes; a single magnified hair "
        "strand; a piece of stitched leather showing the seams." + NOSOMBRA,
    "65_huesos_mamut": "Prop sheet" + HOJA + ", 12 separate mammoth bones evenly spaced in a 4x3 grid, never touching: a mammoth "
        "skull front view; a mammoth skull side view; a lower jawbone; a long curved tusk; a second tusk curving the other way; a "
        "big leg bone; a shoulder blade; a pelvis; a vertebra; a rib; a stack of three jawbones; a hide cover rolled up." + NOSOMBRA,
    "66_iglu_utileria": "Prop sheet" + GRIS + ", 12 separate Arctic objects evenly spaced in a 4x3 grid, never touching or "
        "overlapping: a rectangular block of packed white snow; a second snow block; a small white snow-block igloo dome; a long "
        "bone snow knife; a carved soapstone seal-oil lamp with a flame; a thick caribou fur blanket; a wooden sled; a harpoon; a "
        "pair of sealskin boots; a fur-trimmed hood; a stack of three snow blocks; a white puff of breath vapour." + NOSOMBRA,
    "67_moderno_hoja": HOY + "Prop sheet" + HOJA + ", 12 separate modern objects evenly spaced in a 4x3 grid, never touching or "
        "overlapping: a red puffer jacket; a white radiator heater; a thick mattress; a big glass thermometer; a smartphone with a "
        "blank screen; a steel sewing needle with thread; a wool scarf; a pair of winter boots; a hot water bottle; a light bulb "
        "glowing; a steaming mug of tea; a knitted winter hat." + NOSOMBRA,
}

P = {k: E + v + C for k, v in {**ESC, **HOJAS}.items()}
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(ESC), "escenarios +", len(HOJAS), "hojas =", len(P), "prompts")
