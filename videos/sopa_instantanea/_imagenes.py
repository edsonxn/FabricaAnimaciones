# -*- coding: utf-8 -*-
"""Descripción visual de CADA FRASE del guion, por clave «escena_índice» (no por número de beat): sobrevive a cualquier
corte de `beats`. Una lista con 2-3 variantes = la frase puede caer en varios beats (se usan en orden y sin repetir).
hacer_prompts.py arma prompts.json: beat de imagen → la frase que más suena en él; clip combinado → A = [t0, t_medio], B = [t_medio, t1]."""
from guion import FICHA

P = FICHA["personajes"]
INV, EMP, MAD, ANC, ESP = P["inventor"], P["empresario"], P["inventor_maduro"], P["anciano"], P["esposa"]
NINO = "a plasticine Taiwanese boy about eight years old, with short black hair and a simple white cotton shirt"
JOVEN = "a plasticine Taiwanese young man about twenty-two years old, slim, with short black hair, round black-rimmed glasses and a white shirt with a vest"
ABUELOS = "a plasticine Taiwanese grandmother and grandfather in their sixties, in simple dark cotton clothes"
NOOD = "a block of wavy golden fried plasticine noodles, square and crinkled, with tiny holes"
PAN = "a deep black iron frying pan of bubbling oil"
CUP = "a plain white foam cup with no printing"
SHED = ("a small wooden shed in the backyard of a modest 1950s Japanese house: wooden walls, a bare light bulb, a second-hand "
        "cast-iron noodle-making machine with a hand crank, a gas burner, flour sacks without letters, bamboo baskets")
SHEDX = "a small wooden shed with a tin roof in the backyard of a modest 1950s Japanese house with a tiled roof, a few trees around"
COCINA = "a small 1950s Japanese home kitchen with a wooden counter, a gas stove, paper sliding doors and a warm hanging lamp"
TELAS = "a tiny 1910s Taiwanese family fabric shop with rolls of colorful cloth on wooden shelves and a wooden counter"
OSAKA = "a 1930s Osaka street of wooden two-story shops and early brick buildings with streetcars"
RUINAS = "the burned ruins of 1945 Osaka: blackened wooden beams, collapsed roofs, smoke and ash under a gray sky"
MERCADO = ("a crowded 1946 black market of wooden stalls and canvas tarps beside a railway station at night in winter, paper "
           "lanterns, breath steam in the cold air")
PUESTO = "a tiny wooden ramen stall with a steaming pot and a paper lantern"
FILA = "a very long line of thin people in worn winter coats, caps and scarves, shivering in the cold night"
CARCEL = "a bare 1948 Japanese prison cell with gray walls, a small barred window with light falling in and a thin futon"
OFICINA = "a 1950s Japanese small bank office with wooden desks, ledgers, an abacus and a black telephone"
TIENDA = "a small 1958 Japanese grocery store with wooden shelves of plain paper packets without letters and a wooden counter"
SUPER = "a bright 1966 American supermarket aisle with chrome carts and shelves of blank cans and plain boxes"
AVION = "the cabin of a 1966 propeller airliner with wide seats, small round windows and clouds outside"
FABRICA = "a 1971 Japanese food factory with a conveyor belt, steel machines and workers in white caps"
NIEVE = "a snowy mountain forest in Japan in winter 1972 around a wooden lodge, deep snow, pine trees"
POLICIAS = "plasticine riot policemen in dark blue uniforms, white helmets and tall metal shields"
TELE = "a 1972 Japanese living room with a wooden television set on legs, a low table, tatami mats and a family sitting in front of it"
ESPACIO = "the inside of a space shuttle cabin with white panels and switches, Earth visible through the window"
TIENDITA = ("a Mexican corner shop with a bright painted façade, a metal roll-up door, shelves packed with colorful plain "
            "packets without letters and a glass counter")
OFI_MX = "a modern Mexican office desk with a computer, papers and a coffee mug"

D = {
    # --- gancho
    "gancho_0": [f"a giant plasticine globe of the Earth surrounded by a swirling river of thousands of {CUP}s and steaming noodle bowls",
                 f"close-up of {CUP} with steam rising and wavy noodles inside, a fork resting on it, on a kitchen table"],
    "gancho_1": [f"{INV} sitting alone on the steps of a modest 1950s Japanese house at dusk, head in his hands, empty pockets turned out"],
    "gancho_2": [f"{EMP} standing behind the bars of a gray 1948 prison cell, looking down, a small barred window behind him",
                 f"{INV} looking at an empty wallet and a closed office door with a padlock"],
    "gancho_3": [f"wide shot of {SHEDX}, a warm light bulb glowing through its small window at night"],
    "gancho_4": [f"{INV} inside {SHED}, turning the crank of the noodle machine while a {PAN} sizzles on the burner",
                 f"close-up of hands holding {NOOD} over {PAN}, golden bubbles rising"],
    # --- promesa
    "promesa_0": [f"{FILA} in {MERCADO}, waiting in front of {PUESTO}"],
    "promesa_1": [f"{EMP} handing envelopes of money to grateful students in school uniforms, while a stern official watches from a doorway"],
    "promesa_2": [f"close-up of golden tempura pieces frying in {PAN}, with a thousand tiny bubbles, in {COCINA}"],
    "promesa_3": [f"{CUP} with a lid floating weightless inside {ESPACIO}, noodles drifting out slowly"],
    "promesa_4": [f"{INV} standing proudly in front of {SHEDX}, holding up {NOOD} in both hands, warm morning light"],
    # --- origen
    "origen_0": [f"wide view of a 1910 Taiwanese town with tiled roofs, palm trees, rice fields and a small temple, morning mist"],
    "origen_1": [f"{NINO} standing alone at a doorway looking at the rain, with an old family altar of candles behind him"],
    "origen_2": [f"{ABUELOS} with {NINO} inside {TELAS}, the grandmother folding cloth and the grandfather smiling"],
    "origen_3": [f"{NINO} behind the counter of {TELAS} measuring cloth for a customer and counting coins with an abacus"],
    "origen_4": [f"{NINO} running through a busy market street carrying rolls of fabric to sell, looking for buyers"],
    "origen_5": [f"{JOVEN} standing proudly in front of his own small textile workshop with weaving looms and workers"],
    "origen_6": [f"{EMP} stepping off a steamship onto the busy docks of Osaka in the 1930s, holding a leather suitcase",
                 f"{EMP} walking confidently along {OSAKA}"],
    # --- guerra
    "guerra_0": [f"dark sky over {OSAKA} with searchlight beams and distant planes, people looking up in fear"],
    "guerra_1": [f"{RUINAS}, a burned factory sign-less doorway and broken machines among the ashes",
                 f"{EMP} standing among {RUINAS}, his suit dusty, looking at the remains of his factory"],
    "guerra_2": [f"{EMP} sitting on a burned beam among {RUINAS}, rolling up his sleeves with determination"],
    "guerra_3": [f"wide shot of a ruined 1945 Japanese city with makeshift shacks and smoke, hungry families in the streets"],
    "guerra_4": [f"close-up of an almost empty rice bowl in thin hands, a family sharing a tiny meal on a tatami floor"],
    # --- fila
    "fila_0": [f"{EMP} in a dark overcoat and hat walking through {MERCADO}"],
    "fila_1": [f"{FILA} stretching into the darkness in {MERCADO}", f"low angle of the long line of shivering people under paper lanterns, snow starting to fall"],
    "fila_2": [f"close-up of a steaming bowl of noodles handed over the counter of {PUESTO} to cold grateful hands"],
    "fila_3": [f"{EMP} in a dark overcoat and hat standing still on the side of the street, watching {FILA}, deep in thought"],
    "fila_4": [f"close-up of {EMP} in a dark overcoat and hat, his glasses fogged by the steam of a noodle stall, eyes thoughtful"],
    "fila_5": [f"a dreamy thought bubble of plasticine above {EMP}: a bowl of noodles and a kettle pouring hot water, glowing warmly"],
    "fila_6": [f"{EMP} closing a small wooden box with a glowing light inside and putting it on a high shelf"],
    # --- carcel
    "carcel_0": [f"{EMP} at a desk in a 1947 Osaka office, shaking hands with a client, a busy office behind him"],
    "carcel_1": [f"{EMP} handing envelopes to happy university students in black school uniforms and caps"],
    "carcel_2": [f"two stern plasticine tax inspectors in dark suits examining ledgers with magnifying glasses in an office"],
    "carcel_3": [f"a stern plasticine tax inspector pointing at a ledger while {EMP} looks surprised across the desk"],
    "carcel_4": [f"a 1948 Japanese courtroom of dark wood, a judge at a high bench, {EMP} standing before him with his head bowed"],
    "carcel_5": [f"{EMP} sitting on the thin futon in {CARCEL}, light falling through the bars",
                 f"close-up of tally marks scratched on a gray prison wall next to a barred window"],
    # --- quiebra
    "quiebra_0": [f"{EMP} entering {OFICINA}, greeted by bowing employees"],
    "quiebra_1": [f"{EMP} sitting at the head of a long meeting table in {OFICINA}, men in suits listening"],
    "quiebra_2": [f"a crowd of angry depositors in coats pressing against the closed wooden door of a small 1957 Japanese bank"],
    "quiebra_3": [f"{EMP} alone in an empty {OFICINA}, papers scattered on the floor, the chairs pushed back"],
    "quiebra_4": [f"two plasticine movers carrying furniture out of an office while {EMP} watches silently"],
    "quiebra_5": [f"{INV} standing in front of a modest 1950s Japanese house with a tiled roof and a small garden in Ikeda, autumn leaves"],
    "quiebra_6": [f"{INV} sitting on the wooden porch of his house at night, looking at the empty garden"],
    "quiebra_7": [f"close-up of {INV} with his eyes closed, a faint memory of {FILA} glowing behind him in the night"],
    # --- cobertizo
    "cobertizo_0": [f"{INV} hammering wooden planks to build {SHEDX}, sawdust in the air"],
    "cobertizo_1": [f"{INV} pushing a wheelbarrow carrying a heavy second-hand cast-iron noodle-making machine with a hand crank and a deep black iron frying pan"],
    "cobertizo_2": [f"{INV} writing five short lines with a brush on a sheet of paper pinned to the wall of {SHED}, the lines are only abstract ink strokes"],
    "cobertizo_3": [f"{INV} tasting noodles with chopsticks in {SHED}, with a row of jars on a shelf behind him"],
    "cobertizo_4": [f"{INV} timing a bowl of noodles with a big round pocket watch in {SHED}, coins stacked on the table"],
    "cobertizo_5": [f"{INV} working by the light of a bare bulb in {SHED} at midnight, the moon visible through the small window",
                    f"{INV} at dawn in {SHED}, rolling dough while the first sunlight enters through the cracks"],
    "cobertizo_6": [f"{INV} sitting tired at a table covered with failed noodle experiments in {SHED}"],
    "cobertizo_7": [f"close-up of a clump of soggy, broken plasticine noodles stuck together on a plate, and a moldy batch in a basket"],
    "cobertizo_8": [f"{INV} laying noodles on bamboo trays to dry in the sun in the backyard, and a small smoking box nearby"],
    "cobertizo_9": [f"{INV} throwing a failed batch of noodles into a bucket at dawn, then tying his apron again"],
    # --- tempura
    "tempura_0": [f"{ESP} frying tempura in {PAN} in {COCINA} at night, while {INV} watches from the doorway"],
    "tempura_1": [f"close-up of {ESP}'s hands dipping vegetables into batter and then into {PAN} in {COCINA}"],
    "tempura_2": [f"extreme close-up of tempura bubbling in hot oil, hundreds of tiny bubbles, {INV}'s glasses reflecting them"],
    "tempura_3": [f"cutaway diagram made of plasticine: a piece of fried batter cut in half showing thousands of tiny holes, steam escaping"],
    "tempura_4": [f"{INV} running across the backyard at night toward the lit {SHEDX}, his apron flying",
                  f"{INV} lowering {NOOD} into {PAN} in {SHED}, bubbles exploding around it"],
    "tempura_5": [f"close-up of {NOOD} cooling on a bamboo rack, dry and crunchy, light shining through its tiny holes"],
    "tempura_6": [f"{INV} pouring boiling water from a kettle over {NOOD} in a bowl, steam rising"],
    "tempura_7": [f"{INV} lifting soft noodles with chopsticks from the bowl, smiling with amazement, {ESP} beside him"],
    "tempura_8": [f"{INV} and {ESP} celebrating in {SHED}, raising a bowl of noodles, warm golden light"],
    # --- lanzamiento
    "lanzamiento_0": [f"a 1958 Japanese summer street with a delivery tricycle loaded with plain paper packets, cicadas and sunshine"],
    "lanzamiento_1": [f"close-up of {NOOD} next to a small plasticine chicken figurine on a wooden counter"],
    "lanzamiento_2": [f"{INV} in a clean white shirt standing behind the counter of {TIENDA}, proud and nervous"],
    "lanzamiento_3": [f"a plasticine shopkeeper frowning at a plain paper packet of noodles and a pile of coins on the counter of {TIENDA}"],
    "lanzamiento_4": [f"a simple street noodle stall with a cheap bowl of noodles next to a tall stack of six coins, comparison on a wooden table"],
    "lanzamiento_5": [f"two plasticine shopkeepers laughing and shaking their heads behind the counter of {TIENDA}"],
    "lanzamiento_6": [f"{INV} handing out small steaming cups of noodles to curious shoppers inside {TIENDA}"],
    "lanzamiento_7": [f"a crowd of happy shoppers in {TIENDA} grabbing plain paper packets from the shelves, the shelves almost empty"],
    "lanzamiento_8": [f"{INV} in a suit standing in front of a new small factory building with a chimney and workers arriving"],
    # --- copias
    "copias_0": [f"dozens of small plasticine factories popping up like mushrooms across a 1960s Japanese town, smoke from every chimney"],
    "copias_1": [f"rows of identical noodle blocks coming out of many rival machines, plasticine workers copying each other"],
    "copias_2": [f"close-up of a bad batch of noodle blocks, greasy and moldy, in a crate, with a disappointed customer"],
    "copias_3": [f"{EMP} with slightly graying temples signing official papers with a fountain pen and a red stamp, in a 1960s office"],
    "copias_4": [f"{EMP} with slightly graying temples looking out of an office window over the factory roofs, thoughtful"],
    "copias_5": [f"a plasticine airplane taking off from a 1960s Japanese airport toward the ocean at sunset"],
    # --- america
    "america_0": [f"{MAD} with a suitcase walking out of a 1966 American airport into a sunny street with big cars"],
    "america_1": [f"{MAD} standing in {SUPER}, surprised, holding a plain packet of noodles"],
    "america_2": [f"{MAD} in {SUPER} looking at shoppers who hold chopsticks clumsily and have no bowls"],
    "america_3": [f"plasticine American shoppers in {SUPER} breaking a noodle block into plain white paper cups and pouring hot water from a kettle"],
    "america_4": [f"close-up of a plasticine American shopper eating noodles from a plain paper cup with a metal fork"],
    "america_5": [f"a plasticine family in a 1960s American kitchen eating noodles quickly from paper cups at the counter"],
    "america_6": [f"close-up of {MAD} watching, a glowing light bulb of plasticine lighting up above his head"],
    "america_7": [f"{MAD} holding up a plain white paper cup like a treasure, looking at it from below"],
    # --- vaso
    "vaso_0": [f"{MAD} in {AVION} receiving a small container of macadamia nuts with a peel-off aluminum lid from a stewardess"],
    "vaso_1": [f"close-up of {MAD}'s hands peeling back a shiny aluminum lid and slipping it into his jacket pocket in {AVION}"],
    "vaso_2": [f"{MAD} at a drawing table sketching a cup, with several plain white foam cups on the table"],
    "vaso_3": [f"cutaway plasticine diagram of {CUP} showing a noodle block suspended in the middle, wider at the top, empty space below"],
    "vaso_4": [f"a delivery truck bumping on a road, inside it the cups stay intact; then hot water pouring into a cup, surrounding the noodles"],
    "vaso_5": [f"close-up of a shiny aluminum lid being pressed onto {CUP} in {FABRICA}"],
    "vaso_6": [f"{MAD} standing proudly in {FABRICA} beside a conveyor belt full of {CUP}s with lids"],
    "vaso_7": [f"a 1971 Japanese store shelf full of {CUP}s with dust on them, a bored clerk yawning"],
    # --- nieve
    "nieve_0": [f"wide shot of {NIEVE}, heavy snow falling, dark clouds"],
    "nieve_1": [f"{NIEVE}, the wooden lodge with closed shutters, a faint shadow of armed men behind a window"],
    "nieve_2": [f"{TELE}, the screen showing the snowy lodge, everyone leaning forward anxiously"],
    "nieve_3": [f"close-up of a frozen lunch box with icy rice in a policeman's gloved hands in the snow"],
    "nieve_4": [f"{POLICIAS} eating steaming noodles from {CUP}s with forks in the falling snow, warming their hands"],
    "nieve_5": [f"{TELE}, the whole family pointing at the screen, which shows policemen eating from foam cups in the snow"],
    "nieve_6": [f"a long line of shoppers outside a 1972 Japanese store, everyone leaving with stacks of {CUP}s"],
    # --- espacio
    "espacio_0": [f"a plasticine globe of the Earth with tiny {CUP}s traveling along glowing routes to every continent"],
    "espacio_1": [f"a plasticine trophy shaped like {CUP} on a stage under spotlights, an audience applauding"],
    "espacio_2": [f"a plasticine karaoke machine with a microphone looking small next to a giant {CUP} on a podium"],
    "espacio_3": [f"{ANC} looking up at a starry night sky through a big window, smiling"],
    "espacio_4": [f"a plasticine astronaut in a white spacesuit inside {ESPACIO}, catching floating noodle balls with a fork",
                  f"a space shuttle launching from a launch pad with a huge plume of smoke, made of plasticine"],
    "espacio_5": [f"a quiet plasticine garden in Ikeda in winter, an empty bench with a pair of round black-rimmed glasses on it"],
    "espacio_6": [f"{ANC} swinging a golf club on a green golf course, then smiling at a bowl of noodles on a picnic table"],
    "espacio_7": [f"a bright museum hall with a replica of {SHEDX} inside it, visitors looking through its door"],
    # --- mexico
    "mexico_0": [f"a warm Mexican home kitchen with colorful talavera tiles, a clay pot and {CUP} steaming on the table"],
    "mexico_1": [f"a mountain of {CUP}s and noodle packets piled in the shape of a map of Mexico, children climbing it"],
    "mexico_2": [f"a plasticine Mexican shopkeeper arranging rows of colorful foam cups without letters on a shelf in {TIENDITA}"],
    "mexico_3": [f"a plasticine Mexican customer asking for a soup at the counter of {TIENDITA}, the shopkeeper handing him a foam cup"],
    "mexico_4": [f"a plasticine Mexican office worker at {OFI_MX} eating noodles from {CUP} with a fork, a wall calendar without numbers behind"],
    "mexico_5": [f"a plasticine Mexican student pouring hot water into {CUP} in a small kitchen and timing it with a phone turned face down"],
    "mexico_6": [f"cutaway plasticine diagram of {CUP} on a Mexican kitchen table: the porous noodle block soaking up hot water"],
    # --- cierre
    "cierre_0": [f"{ANC} sharing bowls of noodles with smiling people of many countries around a long table"],
    "cierre_1": [f"{INV} opening the door of {SHEDX} at sunrise, light flooding in"],
    "cierre_2": [f"{INV} alone inside {SHED} at night, turning the crank of the noodle machine with determination"],
    "cierre_3": [f"close-up of {CUP} with steam rising on a table, and in the steam the faint shapes of {FILA} on a winter night"],
    "cierre_4": [f"{INV} standing at the door of {SHEDX}, looking straight at the camera with a small smile, holding {NOOD}"],
    "cierre_5": [f"a cozy plasticine living room at night with a family eating from foam cups and laughing on the sofa"],
    "cierre_6": [f"a tiny plasticine {INV} waving from inside a giant {CUP} on a table"],
    "cierre_7": [f"plasticine hands molding a new piece of clay on a workbench, tools and lumps of colored clay around"],
}
