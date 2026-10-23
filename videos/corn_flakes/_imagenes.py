# -*- coding: utf-8 -*-
"""Descripción visual de CADA FRASE del guion, por clave «escena_índice» (no por número de beat): sobrevive a cualquier
corte de `beats`. Una lista con 2-3 variantes = la frase puede caer en varios beats (se usan en orden y sin repetir).
hacer_prompts.py arma prompts.json: beat de imagen → la frase donde empieza (y la siguiente variante si ya se usó);
clip combinado → escena A = frase de texto_a, escena B = frase de texto_b."""
from guion import FICHA

P = FICHA["personajes"]
MED, VIE, CON, EMP, ANC = P["medico"], P["medico_viejo"], P["contador"], P["empresario"], P["anciano"]
FLK = "thin wavy golden plasticine cereal flakes, toasted at the edges"
ROD = "a machine with two steel rollers and an iron hand crank, no electric motor"
COC = ("the experimental kitchen of an 1890s health sanitarium: cast-iron stoves, copper pots, wooden tables, glass jars of "
       "grain and gas lamps")
SAN = ("a huge five-story Victorian sanitarium building of pale brick with long white verandas and a dome, lawns and trees "
       "around it, in a small Michigan town")
TRIGO = "a large copper pot of boiled whole wheat grains"
CAJA = "a plain cardboard cereal box with no printing at all"
NY = "a busy New York street of 1907 with brick buildings, horse-drawn wagons, early streetcars and a small grocery store"
TIENDA = "the inside of a small 1907 New York grocery store: wooden shelves of blank tins and plain boxes, a counter and a brass scale"
CORTE = "an old wood-paneled state supreme court room with a high judges' bench, wooden railings and tall windows"

D = {
    # --- gancho
    "gancho_0": [f"medium shot of {MED} in {COC}, holding up a spoonful of plain pale flakes and frowning at it with satisfaction, "
                 "a bowl of bland flakes and a glass of water on the table",
                 f"close-up of a plain white bowl of pale unsweetened {FLK} on a wooden table, a doctor's hand pushing away a sugar bowl"],
    "gancho_1": [f"{MED} lecturing with one finger raised in front of a chalkboard covered only with drawings of grains and a calm "
                 "heart, rows of patients in white robes listening seriously",
                 "a calm patient in a white robe eating a bowl of plain flakes, small swirling red clouds of passion above his head "
                 "fading away into soft blue mist"],
    "gancho_2": [f"{EMP} standing proudly in front of a long factory line where thousands of {FLK} pour out of steel rollers "
                 "into plain boxes", f"a world globe made of plasticine surrounded by flying {FLK}, tiny breakfast bowls on every continent"],
    "gancho_3": [f"{MED} riding a bicycle on a sanitarium path while {CON} jogs beside him tired and sweaty, scribbling in a notebook"],
    "gancho_4": [f"close-up of {TRIGO} forgotten on a cast-iron stove in {COC}, steam gone, flies of dust in the light",
                 f"a forgotten pot of wheat on a stove at night, a single gas lamp, a wall clock without numbers"],
    # --- promesa
    "promesa_0": [f"close-up of {TRIGO}, the grains dry and clumped, a trash bucket waiting next to it"],
    "promesa_1": [f"a towering stack of plain cereal boxes reaching the ceiling of a huge warehouse, workers looking up amazed"],
    "promesa_2": [f"{MED} and {EMP} pulling a cereal box in opposite directions in a tug of war inside {CORTE}"],
    "promesa_3": [f"close-up of an old folded handwritten letter on a desk under a dim lamp, sealed with red wax, gathering dust"],
    "promesa_4": [f"{MED} and {CON} standing back to back in {COC}, both with arms crossed, a bowl of {FLK} between them"],
    # --- sanatorio
    "sanatorio_0": [f"wide establishing shot of {SAN} on a sunny morning, carriages arriving at the entrance"],
    "sanatorio_1": [f"closer view of the grand entrance of {SAN}, nurses in white uniforms greeting elegant visitors"],
    "sanatorio_2": [f"inside the sanitarium: a bright hall with potted palms, guests in white robes doing gentle exercises with wooden "
                    "dumbbells, nurses with clipboards"],
    "sanatorio_3": ["wealthy guests in top hats and long dresses relaxing in rows of wicker chairs on a long veranda, one taking a "
                    "steam bath in a wooden cabinet with only his head showing"],
    "sanatorio_4": [f"heroic medium shot of {MED} standing at the top of a grand staircase, all in white, hands behind his back"],
    "sanatorio_5": [f"{MED} at a dining table pushing away a plate of ham, a bottle of whiskey and a coffee pot with a stern 'no' gesture"],
    "sanatorio_6": ["a heavy 1890s breakfast table: fried meat, fried potatoes, bread with lard and greasy eggs, a stout man in "
                    "suspenders eating"],
    "sanatorio_7": ["a row of men and women in a waiting room holding their stomachs with pained faces, a doctor's sign without letters"],
    "sanatorio_8": [f"{MED} at a laboratory table with scales and glass jars of wheat, oats and corn, taking notes, thoughtful"],
    # --- granos
    "granos_0": [f"{MED} looking disappointed at a tray of burnt lumpy brown biscuits in {COC}"],
    "granos_1": [f"close-up of hard whole-wheat biscuits coming out of a cast-iron oven for the second time, so hard that one "
                 "cracks the wooden board when dropped"],
    "granos_2": [f"{MED} grinding the hard biscuits into small crumbs with a heavy hand grinder, a bowl filling with brown crumbs"],
    "granos_3": ["an angry elderly rival doctor with long white side whiskers and a black frock coat waving a rolled paper at "
                 f"{MED} in front of a small courthouse"],
    "granos_4": ["close-up of a rustic bowl of brown crunchy crumb cereal with milk, a wooden spoon beside it"],
    "granos_5": [f"a sanitarium dining room: a nurse serving plates of very hard dark toast to patients who look at it nervously"],
    "granos_6": ["an elegant elderly woman patient biting into a hard toast, her false teeth cracking with a comic little spark, "
                 "the other diners shocked"],
    "granos_7": [f"the elderly woman, offended, holding up her broken false teeth in front of {CON}, who sighs and opens the cash box"],
    "granos_8": [f"{MED} pacing in {COC}, hands behind his back, an idea cloud above his head with a gentle soft grain"],
    # --- hermano
    "hermano_0": [f"{MED} striding down a long sanitarium corridor, nurses stepping aside"],
    "hermano_1": [f"{CON} walking one step behind {MED}, carrying a tall stack of ledgers"],
    "hermano_2": [f"close-up of {CON} at a small desk with an abacus and open ledgers full of tidy columns of ink lines"],
    "hermano_3": [f"{CON} in a cramped office juggling tasks: paying a worker, signing papers, answering a candlestick telephone",
                  f"{CON} handing out pay envelopes to a line of kitchen workers in aprons"],
    "hermano_4": [f"{CON} working late at night by a single oil lamp, the sanitarium windows dark behind him, a tiny coin purse on the desk"],
    "hermano_5": [f"{MED} pointing at {CON} and scolding him in front of nurses, {CON} looking down silently"],
    "hermano_6": [f"wide shot of {MED} riding an old safety bicycle along the sanitarium garden path, dictating with one hand raised"],
    "hermano_7": [f"{MED} riding an old bicycle along a garden path while beside him {CON} jogs out of breath, writing in his small notebook as he runs",
                  f"close-up of {CON}'s hands writing fast in a small notebook while running, ink splashing"],
    "hermano_8": ["the same sanitarium garden path seen through the seasons: autumn leaves, snow and spring flowers, the bicycle "
                  "tracks always there", f"{CON} older, with a few gray hairs, still standing one step behind the doctor"],
    # --- olvido
    "olvido_0": [f"a calendar page of August on a kitchen wall with no numbers, summer light through the window of {COC}"],
    "olvido_1": [f"{MED} and {CON} in linen aprons stirring {TRIGO} on a cast-iron stove in {COC}"],
    "olvido_2": [f"close-up of {ROD}, a lump of dough going through it, the doctor's hands turning the crank"],
    "olvido_3": [f"a nurse at the kitchen door calling urgently, {MED} and {CON} untying their aprons and hurrying out"],
    "olvido_4": [f"{TRIGO} left alone on the table in {COC}, the light changing from afternoon to night through the window",
                 "a wall clock without numbers in the empty kitchen, its hands spinning fast"],
    "olvido_5": [f"{CON} poking the dry clumped wheat with a wooden spoon, making a face at the smell, {MED} leaning in"],
    "olvido_6": [f"{CON} holding the pot over a trash bucket, hesitating, a small cash ledger peeking from his pocket"],
    "olvido_7": [f"{MED} and {CON} pouring the old wheat between the steel rollers of {ROD}"],
    "olvido_8": [f"close-up of the steel rollers of {ROD} as the first golden flakes start coming out, {MED} and {CON} leaning in amazed behind the machine"],
    # --- hojuelas
    "hojuelas_0": [f"extreme close-up of single wheat grains coming out of the rollers as separate {FLK}, falling like leaves"],
    "hojuelas_1": [f"a black iron baking tray of {FLK} coming out of a cast-iron oven, golden and crisp, steam rising"],
    "hojuelas_2": [f"{MED} and {CON} looking at a flake against the window light with wide eyes, like jewelers with a diamond"],
    "hojuelas_3": [f"a long line of identical flaking roller machines in a factory, flakes pouring like a golden waterfall"],
    "hojuelas_4": [f"patients in white robes in a sanitarium dining room tasting bowls of {FLK} and smiling with delight"],
    "hojuelas_5": [f"a post office counter piled high with letters and parcels addressed to the sanitarium, a clerk overwhelmed",
                   f"{CON} reading a stack of letters asking for more flakes"],
    "hojuelas_6": [f"{MED} and {CON} feeding golden corn kernels into {ROD}"],
    "hojuelas_7": [f"close-up of a bowl of crispy golden corn flakes in {COC}, sunlight hitting them, a jug of milk beside it"],
    # --- patente
    "patente_0": [f"{MED} at a government patent office counter of 1895, a clerk in sleeve garters stamping a document"],
    "patente_1": [f"close-up of a large old patent document with drawings of rollers and flakes and a red wax seal, no readable words"],
    "patente_2": [f"close-up of {MED}'s gloved hand signing alone at the bottom of the patent with a fountain pen"],
    "patente_3": [f"{CON} standing alone outside the patent office in the rain, looking at the closed door"],
    "patente_4": [f"{CON} older, sitting in a dark office telling his story to a young reporter who takes notes, a framed flake on the wall"],
    # --- fiebre
    "fiebre_0": [f"{FLK} slipping through {MED}'s fingers and flying away out of an open window"],
    "fiebre_1": [f"a confident patient with a sharp mustache and a top hat sitting in a sanitarium wicker chair, eyeing a bowl of flakes"],
    "fiebre_2": [f"the confident man with the top hat proudly cutting a ribbon in front of his own small cereal factory with a smoking chimney"],
    "fiebre_3": [f"the confident man with the top hat smoking a cigar on a pile of gold coins and plain cereal boxes"],
    "fiebre_4": ["a crowd of men in bowler hats and suits rushing into a small town with suitcases full of grain"],
    "fiebre_5": ["a small Michigan town seen from above packed with dozens of little cereal factories with smoking chimneys",
                 "a shop window crammed with plain cereal boxes of every size and color, all without any letters"],
    "fiebre_6": [f"{CON} alone at his desk doing accounts while through the window the factory chimneys of the town smoke"],
    # --- azucar
    "azucar_0": [f"{CON} in {COC} holding a bowl of flakes and looking at it with a sly idea"],
    "azucar_1": [f"extreme close-up of a spoon pouring sparkling white sugar over a bowl of {FLK}, the sugar shining like snow"],
    "azucar_2": [f"{CON} tasting a plain flake and making a bored face"],
    "azucar_3": ["a family at a 1900s breakfast table, the child secretly adding a big spoon of sugar to his bowl and smiling"],
    "azucar_4": [f"{MED} furious, slamming the lid of a sugar bowl shut in front of {CON}"],
    "azucar_5": [f"{MED} preaching from a small stage at the sanitarium, pointing angrily at a giant sugar bowl crossed out on a "
                 "painted banner without letters"],
    "azucar_6": [f"{MED} pointing at the door, {CON} holding his bowler hat"],
    "azucar_7": [f"{CON} standing at a crossroads of two paths at dusk: one toward the warm lit sanitarium, the other toward a dark "
                 "empty factory lot"],
    "azucar_8": [f"{CON} counting a very small pile of coins on his desk, a mirror behind him showing a few gray hairs"],
    "azucar_9": [f"close-up of {CON}'s face in shadow, hesitating, the sanitarium lights reflected in his round glasses"],
    # --- salto
    "salto_0": [f"{CON} placing a letter of resignation on {MED}'s desk and walking out, winter snow outside the window"],
    "salto_1": [f"{CON} shaking hands with {MED} across a desk over a contract, the doctor smug, a stack of share certificates beside him",
                f"{EMP} standing proudly in front of a new brick factory with a smoking chimney on a snowy morning"],
    "salto_2": [f"{EMP} pouring golden malt syrup and sugar into a giant copper mixing vat in his factory"],
    "salto_3": [f"{EMP} at a desk covered with drawings of newspaper ads and posters without letters, an artist sketching beside him"],
    "salto_4": [f"close-up of {EMP}'s hand signing with a fountain pen on top of a plain cereal box, a big flourish of ink"],
    "salto_5": [f"a row of plain cereal boxes on a store shelf, each with the same ink signature flourish and nothing else"],
    # --- guiño
    "guino_0": [f"wide view of {NY}"],
    "guino_1": [f"{EMP} in his office holding up a fresh newspaper page with a big drawing of a winking eye, no letters"],
    "guino_2": [f"a giant drawing of a winking eye painted on a brick wall above the New York street, people pointing at it"],
    "guino_3": [f"in {TIENDA}, a young woman in a 1907 hat winking playfully at a surprised grocer with a big mustache, who hands her a box"],
    "guino_4": ["two very serious elderly ladies in black dresses and hats gasping and covering their mouths outside the store"],
    "guino_5": ["a long line of women in 1907 hats waiting outside the grocery store, laughing and winking at each other"],
    "guino_6": ["a steam train arriving at a big city station with freight cars overflowing with plain cereal boxes"],
    "guino_7": [f"{EMP} in a big office with a window overlooking his factory, standing tall and calm, a small smile"],
    # --- pleito
    "pleito_0": [f"{MED} entering {EMP}'s office without knocking, the door swinging open dramatically"],
    "pleito_1": [f"{MED} proudly showing a plain cereal box in his own white factory, workers in white packing boxes"],
    "pleito_2": ["a confused shopper in a grocery store holding two identical plain cereal boxes, one in each hand"],
    "pleito_3": [f"{EMP} and {MED} each slamming a thick stack of legal papers on a lawyer's desk, glaring at each other"],
    "pleito_4": [f"{CORTE}, {EMP} on one side and {MED} on the other, lawyers in black coats arguing"],
    "pleito_5": [f"three elderly judges in black robes at the high bench of {CORTE} raising a wooden gavel toward {EMP}"],
    "pleito_6": [f"{MED} grudgingly counting out a pile of banknotes onto a court table"],
    "pleito_7": [f"close-up of the bottom of a plain cereal box with a very tiny signature in a corner, a magnifying glass over it"],
    "pleito_8": [f"{EMP} and {MED} walking away from the courthouse in opposite directions down a long snowy street"],
    # --- carta
    "carta_0": [f"{VIE} at a desk by a window, slowly writing a letter by hand under a green lamp"],
    "carta_1": [f"close-up of {VIE}'s trembling hand writing, a single tear on the paper"],
    "carta_2": ["a strict secretary with a tight bun and a high-collared dress reading the letter with a frown, then putting it in a drawer"],
    "carta_3": ["a desk drawer closing slowly in the dark, the folded letter inside"],
    "carta_4": [f"{ANC} sitting in an armchair by a window, holding the opened letter close to his dark glasses"],
    "carta_5": [f"{ANC} turning his face toward the window, almost blind, the letter resting on his lap"],
    "carta_6": [f"{ANC} alone in a quiet room, an empty armchair opposite him, soft afternoon light"],
    # --- méxico
    "mexico_0": [f"{EMP} older, with gray hair, in a big office giving away a heavy bag of coins"],
    "mexico_1": [f"{EMP} older, standing among happy schoolchildren in a sunny playground of the 1930s, a small clinic behind them"],
    "mexico_2": ["two empty wooden rocking chairs side by side on a porch at sunset, one with a white suit jacket and one with a gray jacket"],
    "mexico_3": [f"a bowl of {FLK} traveling on a little paper boat across a plasticine ocean map toward Mexico"],
    "mexico_4": ["a 1950s Mexican city street with colorful colonial houses, a small corner store and a delivery truck with blank plain boxes"],
    "mexico_5": ["an enormous modern cereal factory with tall white silos in a sunny valley of central Mexico, mountains behind"],
    "mexico_6": [f"{MED}'s ghost, translucent, floating over the Mexican factory with a horrified face"],
    "mexico_7": [f"close-up of a bowl of corn flakes glazed with sparkling frosted sugar, shining in morning light"],
    "mexico_8": ["a Mexican family at a breakfast table in the 1980s, children laughing over bowls of frosted flakes with milk"],
    # --- cierre
    "cierre_0": [f"{MED} in {COC} holding up a bowl of plain pale flakes, calm and serious, as in the beginning"],
    "cierre_1": ["a huge long table across the world with people of many countries eating bowls of flakes at sunrise"],
    "cierre_2": [f"a modern-looking but simple kitchen with a bowl of flakes being served, and in the background, ghostly, {TRIGO} on an old stove"],
    "cierre_3": [f"{MED} and {CON} as young men, laughing together in {COC} with a tray of flakes, a warm memory in soft light"],
    "cierre_4": [f"{CON} standing one step behind {MED}, looking straight at the camera with a quiet question in his eyes"],
    "cierre_5": ["a bowl of flakes on a table with a small pile of handwritten paper notes beside it, warm light"],
    "cierre_6": [f"a kitchen shelf with a bowl of {FLK} and two small plasticine figurines standing beside it: one is {MED} in miniature and the other is {CON} in miniature"],
    "cierre_7": [f"{FLK} slowly being shaped by plasticine hands into a new mysterious object under a cloth, workshop light"],
}
