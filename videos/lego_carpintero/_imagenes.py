# -*- coding: utf-8 -*-
"""Descripción visual de CADA FRASE del guion, por clave «escena_índice» (no por número de beat): sobrevive a cualquier
corte de `beats`. Una lista con 2-3 variantes = la frase puede caer en varios beats (se usan en orden y sin repetir).
hacer_prompts.py arma prompts.json: beat de imagen → la frase que más suena en él; clip combinado → A = [t0, t_medio], B = [t_medio, t1]."""
from guion import FICHA

P = FICHA["personajes"]
CAR, MAY, NINO, HIJO, ESP, ING = (P["carpintero"], P["carpintero_mayor"], P["nino"], P["hijo"], P["esposa"], P["ingles"])
JOVEN = ("a plasticine Danish teenage boy about fourteen years old, thin, with short light brown hair, a white collarless "
         "shirt, braces and a small leather carpenter's apron")
NINOS = ("two plasticine Danish little boys about four and six years old with short blond hair, gray wool sweaters and short "
         "trousers")
LAD = "small plain plasticine toy bricks in bright red, yellow, blue and white with round studs on top and no letters"
PATO = "a wooden pull-along toy duck painted red, yellow and white on four small wooden wheels"
TALLER = ("a small 1920s carpentry workshop in a Danish village: wooden workbenches, hand saws, planes, piles of birch wood and "
          "curly shavings, a cast-iron stove, small-paned windows, flat green fields outside")
TALLERX = "a small red-brick carpentry workshop with a tiled roof next to a white farmhouse in a flat Danish village of green fields"
PUEBLO = "a tiny Danish farming village of white farmhouses with red tiled roofs among flat green fields and windmills"
FABRICA = ("a 1940s-1950s small Danish toy factory: wooden workbenches, shelves of wooden toys, a big green cast-iron plastic "
           "injection moulding machine with levers and gauges, bare light bulbs")
ESTACION = "a small 1930s Danish village railway station with a wooden platform, a steam freight wagon and wooden crates"
OFICINA = "a 1950s Danish company office with wooden desks, a black telephone, filing cabinets and a window to the factory"
FERRY = "the wooden deck of a 1950s ferry crossing the gray North Sea, seagulls, a white railing and deck chairs"
CIUDAD = (f"a big colorful toy town built of {LAD} on a play mat with tiny plastic-like plasticine trees, small houses, streets "
          "and little cars")
FUEGO = "huge orange and yellow plasticine flames and dark smoke"
NL = ("a huge modern white factory building with blue trim in a dry valley in northern Mexico with tall rugged mountains behind, "
      "palm trees and a big parking lot, no signs, no letters")

D = {
    # --- gancho
    "gancho_0": [f"an endless torrent of {LAD} pouring out of a giant machine chute into a mountain of bricks, the camera flying over it",
                 f"extreme close-up of {LAD} snapping together one after another very fast, building a tower that grows past the camera"],
    "gancho_1": [f"{CAR} standing alone in the middle of a dirt road of {PUEBLO}, holding a hand plane, looking at the camera, dusk light"],
    "gancho_2": [f"{TALLER} on fire at night, {FUEGO} coming out of the small-paned windows, the roof collapsing"],
    "gancho_3": [f"{CAR} sitting alone on a wooden bench in an empty workshop with the tools hanging still, a single bare bulb, head down"],
    "gancho_4": [f"{CAR} at a farmhouse kitchen table in front of two stern plasticine Danish relatives in dark 1930s suits, one "
                 f"sliding a small cloth money bag across the table while pointing firmly at a {PATO} on the table"],
    "gancho_5": [f"close-up of {CAR} pulling the {PATO} back toward himself and shaking his head with a calm, stubborn face"],
    # --- promesa
    "promesa_0": [f"three small fires side by side on a dark plasticine table like three candles, each one burning a tiny wooden workshop"],
    "promesa_1": [f"a row of {PATO}s lined up on the wooden platform of {ESTACION}, a boy running toward them"],
    "promesa_2": [f"a toy shop counter of the 1950s piled high with plain cardboard boxes of {LAD} being pushed back by a frowning shopkeeper"],
    "promesa_3": [f"a pair of plasticine children's hands building a whole colorful city of {LAD} that spreads across a globe"],
    "promesa_4": [f"{CAR} in his workshop holding up one red {LAD.split(' in ')[0].replace('small plain plasticine toy bricks', 'small plain plasticine toy brick')} "
                  f"in one hand and a {PATO} in the other, smiling proudly, warm window light"],
    # --- origen
    "origen_0": [f"wide aerial view of {PUEBLO} in 1891, a small poor farmhouse with smoke from the chimney, morning mist"],
    "origen_1": [f"a crowded poor Danish farmhouse kitchen with thirteen plasticine children of all ages around a long wooden "
                 "table sharing one pot of porridge, a tired mother and father"],
    "origen_2": [f"{JOVEN} sawing a plank on a workbench while an older plasticine Danish carpenter brother about thirty with a "
                 "beard and a leather apron guides his hands"],
    "origen_3": [f"close-up of plasticine hands fitting a wooden dovetail joint together perfectly, curly shavings around",
                 f"{JOVEN} pushing a hand plane along a board, long curly shavings flying"],
    "origen_4": [f"{CAR} as a young soldier in a 1910s Danish army uniform and cap, then studying technical drawings at a school desk"],
    "origen_5": [f"{CAR} counting a few coins in his palm in front of {TALLERX}, a small wooden sign without letters over the door"],
    "origen_6": [f"{CAR} and {ESP} on their wedding day in front of {TALLERX}, simple 1916 clothes, flowers"],
    "origen_7": [f"{CAR} carrying a wooden door on his shoulder toward a farmhouse while a plasticine farmer waves",
                 f"{CAR} building a wooden chair inside {TALLER}"],
    "origen_8": [f"{CAR} and {ESP} at the door of {TALLERX} with four small plasticine Danish children with blond hair, sunny day"],
    # --- fuego1
    "fuego1_0": [f"{TALLER} on a quiet sunny morning in 1924, a calendar-less wall, everything calm and orderly"],
    "fuego1_1": [f"{NINOS} crouching next to a small cast-iron glue-heating machine inside {TALLER}, striking a match"],
    "fuego1_2": [f"extreme close-up of a tiny spark falling onto a pile of curly wood shavings, which start to glow"],
    "fuego1_3": [f"{TALLER} engulfed by {FUEGO}, workbenches and planks burning"],
    "fuego1_4": [f"the white farmhouse next to the workshop burning at night, {FUEGO}, neighbors with buckets"],
    "fuego1_5": [f"{CAR} standing in front of black smoking ashes and charred beams at dawn, holding one of his sons by the hand"],
    "fuego1_6": [f"{CAR} raising the wooden frame of a new bigger workshop, hammer in hand, sunny sky, new house behind"],
    # --- crisis
    "crisis_0": [f"a 1930s Danish village street in gray rain with closed shops, farmers in worn coats with empty pockets"],
    "crisis_1": [f"a plasticine farmer turning his empty pockets inside out in front of {CAR}, who holds a finished wooden table"],
    "crisis_2": [f"{CAR} shaking hands goodbye with a sad plasticine worker at the workshop door, the last worker leaving",
                 f"an empty {TALLER} with tools hanging still and dust in the light"],
    "crisis_3": [f"{CAR} in a dark suit holding his hat at a simple village churchyard with a plain wooden cross, gray sky, flowers"],
    "crisis_4": [f"{CAR} sitting at a kitchen table at night with four plasticine Danish children of different ages, all quiet, one candle"],
    # --- juguetes
    "juguetes_0": [f"{CAR} picking up a small leftover piece of birch wood from the floor of {TALLER} and looking at it with a spark of an idea"],
    "juguetes_1": [f"{CAR} carving and painting small wooden toys at his workbench: little horses, toy trucks and animals on wheels",
                   f"a shelf in {TALLER} filled with colorful small wooden toys: animals, cars, yo-yos and pull-along figures"],
    "juguetes_2": [f"a happy plasticine farmer father giving a small wooden toy truck to his little son in front of a farmhouse"],
    "juguetes_3": [f"two stern plasticine Danish relatives in dark 1930s suits counting money onto a table in front of {CAR}"],
    "juguetes_4": [f"one stern relative pointing angrily at a pile of small wooden toys on the table, the other holding a wooden chair"],
    "juguetes_5": [f"close-up of {CAR} crossing his arms in front of his wooden toys with a calm stubborn smile"],
    "juguetes_6": [f"{CAR} painting a new plain wooden sign without letters to hang over the door of {TALLERX}"],
    "juguetes_7": [f"two plasticine children playing happily on a wooden floor with wooden toys while {CAR} watches from a chair, smiling"],
    "juguetes_8": [f"{CAR} hanging the plain wooden sign over the workshop door, the whole family looking up, sunny day"],
    "juguetes_9": [f"an old leather-bound Latin book open on a wooden desk next to a {PATO}, a magnifying glass and a candle"],
    "juguetes_10": [f"{CAR} shrugging with a puzzled smile, holding a single wooden toy that has nothing to assemble"],
    # --- pato
    "pato_0": [f"a {PATO} being pulled on a string across a wooden floor by a laughing plasticine toddler, the duck's beak opening"],
    "pato_1": [f"close-up of a brush applying shiny clear varnish to a {PATO}, three small varnish pots in a row",
               f"rows of glossy {PATO}s drying on a wooden rack in {TALLER}"],
    "pato_2": [f"{NINO} in {TALLER} with a varnish brush, a sly look, holding up two fingers"],
    "pato_3": [f"{NINO} pushing a wooden handcart full of crates of ducks toward {ESTACION}"],
    "pato_4": [f"{CAR} pointing sternly toward the door while {NINO} looks down ashamed, in {TALLER}",
               f"{NINO} running back from {ESTACION} carrying a heavy crate of ducks, sweating"],
    "pato_5": [f"{NINO} at night in {TALLER} under a lamp, carefully giving a third coat of varnish to a long row of ducks"],
    "pato_6": [f"{NINO} grown a bit older carving words into a plank of wood with a chisel, only wood shavings visible, no readable letters"],
    "pato_7": [f"a carved wooden plaque with an abstract carved ornament, no letters, hanging on the workshop wall above workbenches"],
    # --- fuego2
    "fuego2_0": [f"sparks bursting from an old electrical fuse box on a factory wall at night, then {FUEGO} spreading"],
    "fuego2_1": [f"burning shelves of wooden toys and rolled paper blueprints curling in {FUEGO}"],
    "fuego2_2": [f"the smoking ruins of the toy factory at dawn, charred wooden toys in the ashes, a melted duck"],
    "fuego2_3": [f"{CAR} with graying hair sweeping ashes and picking up a single unburned wooden toy, determined look"],
    # --- plastico
    "plastico_0": [f"close-up of colorful plastic-looking plasticine granules pouring from a sack into a hopper, curious plasticine workers watching"],
    "plastico_1": [f"{CAR} with graying hair and {HIJO} standing in front of a big green cast-iron plastic injection moulding machine still in its wooden crate"],
    "plastico_2": [f"wide view of {FABRICA}, workers gathering around the new machine as it starts, steam and a warm glow"],
    "plastico_3": [f"{CAR} with graying hair signing a large paper at a desk, a tall stack of coins on one side and a tiny stack on the other"],
    "plastico_4": [f"{HIJO} opening a small parcel and taking out a few bright plastic building bricks, examining them under a lamp"],
    "plastico_5": [f"{ING} in a small 1940s English toy workshop showing a stack of his plastic building bricks with round studs"],
    "plastico_6": [f"the injection moulding machine opening and dropping freshly moulded {LAD} into a tray, plasticine workers smiling"],
    # --- fracaso
    "fracaso_0": [f"{CAR} with graying hair looking at a tall pile of returned cardboard boxes in {FABRICA}, sad"],
    "fracaso_1": [f"a 1950s delivery truck unloading stacks of plain returned boxes at the factory door, a worker shaking his head"],
    "fracaso_2": [f"a stern plasticine man in glasses reading a 1950s trade magazine with only pictures of wooden toys, scoffing"],
    "fracaso_3": [f"a child's tower of {LAD} wobbling and collapsing, bricks bouncing on a table"],
    "fracaso_4": [f"plasticine townspeople in a village street pointing and laughing at a cart of plastic bricks pushed by {CAR}"],
    "fracaso_5": [f"a single red toy brick standing alone in a spotlight on a dark wooden floor, with a huge shadow"],
    "fracaso_6": [f"{HIJO} with a small suitcase walking up the gangway of a 1950s ferry at a harbor"],
    # --- sistema
    "sistema_0": [f"{HIJO} standing at the white railing on {FERRY}, looking out at the sea"],
    "sistema_1": [f"{HIJO} talking with a plasticine Danish department store buyer in a gray coat and hat on {FERRY}, both holding coffee cups"],
    "sistema_2": [f"close-up of the buyer gesturing with open hands, explaining, {HIJO} listening intently"],
    "sistema_3": [f"a lonely toy thrown in a dusty corner of a child's room, forgotten under a bed"],
    "sistema_4": [f"{HIJO} sketching on a notepad on {FERRY}, the drawing shows bricks connecting into houses, no letters"],
    "sistema_5": [f"several plain boxes of bricks opening and their bricks flying out to join together into one growing toy town"],
    "sistema_6": [f"{CIUDAD}, a plasticine boy and girl kneeling beside it, amazed"],
    "sistema_7": [f"low angle close-up inside {CIUDAD}: tiny streets and houses towering like a real city"],
    # --- patente
    "patente_0": [f"two stacked {LAD} slipping apart and falling, in close-up"],
    "patente_1": [f"a cutaway view of a big red plasticine toy brick showing three hollow round tubes inside, glowing softly"],
    "patente_2": [f"macro close-up of a toy brick pressing down onto another, the studs gripping between the tubes, a satisfying click"],
    "patente_3": [f"{MAY} and {HIJO} at a desk stamping a technical drawing of a brick, no letters, warm lamp light"],
    "patente_4": [f"an old faded red brick and a shiny new red brick snapping together perfectly on a wooden table"],
    "patente_5": [f"{MAY} holding a single red toy brick up to the window light, smiling with tears in his eyes"],
    "patente_6": [f"an empty office chair at a wooden desk with round glasses resting on a single red toy brick, a winter window behind"],
    # --- page
    "page_0": [f"{ING} standing alone on a rainy 1950s English street in front of his small toy shop"],
    "page_1": [f"{ING} looking out of a rain-streaked window, his bricks on the sill behind him"],
    "page_2": [f"{ING} at a cluttered desk covered in unpaid bills under a single lamp at night, head in his hands, rain outside"],
    "page_3": [f"a plasticine English widow in a black 1950s dress holding a framed picture without a face, sitting by a window"],
    "page_4": [f"two plasticine lawyers in 1980s suits shaking hands over a desk with documents, a small toy brick on the desk"],
    # --- fuego3
    "fuego3_0": [f"a single match lying on the floor of a dark warehouse, a sense of dread"],
    "fuego3_1": [f"a big warehouse full of shelves of wooden toys and ducks burning at night in February snow, {FUEGO}"],
    "fuego3_2": [f"{HIJO} standing in the snow at dawn in front of the smoking warehouse ruins, jaw clenched"],
    "fuego3_3": [f"{HIJO} placing one red plastic brick on the desk and pushing away a wooden duck, decisive"],
    "fuego3_4": [f"two plasticine Danish brothers in suits putting on their hats and walking out of the office door, unhappy"],
    "fuego3_5": [f"an old empty carpentry workbench with a dusty {PATO} on it, a single beam of light, melancholic"],
    "fuego3_6": [f"{HIJO} sitting alone at the head of a long boardroom table, handing over papers to two departing brothers"],
    # --- legoland
    "legoland_0": [f"crowds of plasticine tourists with cameras and children arriving at the small toy factory gate in the village"],
    "legoland_1": [f"plasticine children pressing their faces against the factory window watching bricks pour out of the machines"],
    "legoland_2": [f"the opening day of a theme park in the Danish countryside in 1968, flags and balloons, families walking in"],
    "legoland_3": [f"a miniature landscape of harbors, ships, airplanes and towns entirely built of {LAD}, tiny plasticine visitors walking among them"],
    "legoland_4": [f"wide aerial view of {PUEBLO} now with a colorful theme park next to it, cars arriving from everywhere"],
    # --- hoy
    "hoy_0": [f"a line of tiny plasticine yellow-faced toy minifigures marching across a table with little helmets and hats"],
    "hoy_1": [f"a giant tower of {LAD} cracking and wobbling, the camera low"],
    "hoy_2": [f"a 2000s corporate boardroom in gray light, plasticine executives staring at a downward red arrow chart drawn with no numbers"],
    "hoy_3": [f"a plasticine Danish businessman about fifty-five with gray hair and glasses, the grandson, walking away from a desk and handing a folder to a younger man in a dark suit"],
    "hoy_4": [f"plasticine workers taking down colorful theme park flags, and on a desk a single classic red brick under a lamp"],
    "hoy_5": [f"a plasticine executive smiling as a tall tower of {LAD} rises again, warm light"],
    "hoy_6": [f"{CIUDAD} that spreads to the horizon, with mountains and seas built of bricks"],
    "hoy_7": [f"a river of {LAD} flowing out of a modern factory like a waterfall, millions of bricks"],
    "hoy_8": [f"six red two-by-four {LAD.split(' in ')[0].replace('small plain plasticine toy bricks', 'toy bricks')} floating in the air and rearranging into many different shapes"],
    # --- mexico
    "mexico_0": [f"a world globe made of plasticine spinning and stopping on Mexico, bricks raining onto the north of Mexico"],
    "mexico_1": [f"{NL}, bright sunny day"],
    "mexico_2": [f"inside a huge modern factory hall in Mexico: long rows of white injection moulding machines and robots, plasticine Mexican workers in blue shirts and safety glasses, no letters"],
    "mexico_3": [f"conveyor belts in the Mexican factory carrying thousands of plain cardboard toy boxes with no letters, the hall stretching far away"],
    "mexico_4": [f"construction cranes building a new wing next to {NL}, plasticine workers in hard hats"],
    "mexico_5": [f"a plasticine Mexican worker in a blue shirt and safety glasses smiling and holding a red brick, and a plasticine child at home building with bricks"],
    # --- cierre
    "cierre_0": [f"{CAR} in his first small workshop, alone, looking at the camera, curly shavings around his feet"],
    "cierre_1": [f"three small fires reflected in the round glasses of {MAY}"],
    "cierre_2": [f"{CAR} pulling a {PATO} on a string down a dirt road toward the sunset, calm and stubborn"],
    "cierre_3": [f"a split scene: on the left {CAR} building a plain wooden chair, on the right a colorful city of {LAD}"],
    "cierre_4": [f"a plasticine family at a kitchen table building with {LAD} together, warm evening light"],
    "cierre_5": [f"a wooden pull-along toy duck and a red toy brick side by side on a workbench in warm light, slow push-in"],
}
