# -*- coding: utf-8 -*-
"""Plastitube (alias pieza_oculta) — «Lo Perdió TODO y a los 48 Años Inventó la Sopa Instantánea en su Patio».
Motor SECUENCIA. 2.º de la tanda de la fórmula de marcas (canales/formula/pieza_oculta.md, 23-oct-2026): marca con giro humano.
Ficha histórica (Wikipedia «Momofuku Ando», «Instant noodle», «Cup Noodles», «Asama-Sansō incident»; Britannica «How was instant
ramen invented»; HISTORY.com 25-ago-1958; NY Sun, obituario 2007; Yokogao Mag; Nissin / Instant Ramen Museum de Ikeda; WINA vía
Kyodo, 2025; El Financiero 3-oct-2021 y tesis ETAC con cifras de WINA para México):
Momofuku Ando (Go Pek-hok), nació el 5-mar-1910 en Chiayi, Taiwán, bajo dominio japonés; huérfano, lo criaron sus abuelos, que tenían
una pequeña tienda de telas en Tainan. A los 22 años fundó su propia empresa textil en Taipéi; en 1933 se fue a Osaka. En la guerra
los bombardeos destruyeron sus negocios. Posguerra: hambre en Japón; en el mercado negro cerca de la estación de Umeda vio una fila
larguísima en el frío por un plato de ramen. 1948: condenado por evasión de impuestos (había dado becas a estudiantes, y eso se
consideró evasión), dos años de cárcel. 1957: quiebra la cooperativa de crédito que presidía; lo pierde todo menos su casa de Ikeda.
En un cobertizo detrás de su casa trabaja solo cerca de un año, con una máquina de fideos usada y una sartén honda. Cinco metas: que
supiera bien, que durara en la alacena, que se hiciera en minutos, que fuera barato y seguro. La idea: ver a su esposa Masako freír
tempura; la fritura saca el agua de la masa y deja hoyitos; los fideos fritos, al recibir agua caliente, se ablandan en minutos.
25-ago-1958: Chicken Ramen, a los 48 años; 35 yenes, unas seis veces lo que costaba un plato de udon o soba. La empresa pasa a
llamarse Nissin. 1966: viaje a Estados Unidos; en un supermercado los compradores parten los fideos en vasos de papel, les echan agua
caliente y los comen con tenedor. Tapa: la idea de un envase de nueces de macadamia con tapa de aluminio que le dieron en el avión.
Fideos suspendidos a la mitad del vaso. 18-sep-1971: Cup Noodles, a los 61 años; empezó vendiéndose poco. Febrero de 1972: el
incidente de Asama-Sansō en vivo por televisión, con los policías comiendo fideos de vaso en la nieve; las ventas se dispararon.
2000: en una encuesta los japoneses eligieron la sopa instantánea como el mejor invento japonés del siglo veinte. 2005: Space Ram,
para un astronauta japonés en el transbordador Discovery. Murió el 5-ene-2007 a los 96 años; decía que el secreto de su larga vida
era el golf y comer Chicken Ramen casi todos los días. Frases suyas: «nunca es demasiado tarde» y «la paz llegará cuando la gente
tenga suficiente para comer». WINA 2024: 123 070 millones de porciones en el mundo (récord). México: ~890 millones en 2016 y
~1 160 millones en 2020 (WINA citada por la prensa); Maruchan es de OTRA empresa japonesa (Toyo Suisan) y su nombre se volvió
genérico en México (el guion no da año de llegada: no está verificado).
Elementos prohibidos en imagen: envases modernos con marca, logotipos, letras y números; a las personas se las describe por oficio,
nunca por nombre (filtro de personas destacadas de Flow).
"""

TITULO = "Lo Perdió TODO y a los 48 Años Inventó la Sopa Instantánea en su Patio"
ARCHIVO = "sopa_instantanea"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 96
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Pronunciación para Chatterbox (solo lo que se dice en voz; subtítulos y Whisper ven la grafía real).
FONETICA = {
    "Momofuku Ando": "Momofúku Ándo",
    "Ando": "Ándo",
    "Osaka": "Ósaka",
    "Ikeda": "Ikéda",
    "Chicken Ramen": "Chíken Rámen",
    "Cup Noodles": "Cap Núdols",
    "ramen": "rámen",
    "Nissin": "Nísin",
    "Masako": "Masáko",
    "tempura": "tempúra",
    "Maruchan": "Maruchán",
    "Taiwán": "Taiuán",
    "udon": "udón",
}

# Whisper oye «Humeda», «Veo», «sideos», «come en contenedor» (homófono) y cifras: la voz está completa (voz/eval.json, 23-oct)
CER_MAX_POR_FRASE = {"fila_0": 0.02, "fila_1": 0.02, "tempura_4": 0.025, "america_4": 0.06, "vaso_6": 0.02}

SECUENCIA = dict(
    video_s=120,        # el usuario (23-oct): 2 min iniciales en clips de Flow
    clip_s=10,
    video_calidad="360p",
    combinar=True,      # cada clip de 10 s une dos momentos del guion con una transición dibujada
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.5,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={"scene-011": 0.0},   # un «hmm» de Flow (Whisper small, 23-oct)
    recorte_por={"scene-002": 0.10, "scene-007": 0.12},   # letterbox negro en los primeros 2-3 s (71 y 82 px de 720)
    carpeta_descargas="flow-sopa_instantanea",
)

# Ficha visual del episodio: se repite PALABRA POR PALABRA en cada prompt donde aparezca (triple anclaje).
FICHA = dict(
    estilo="Cinematic horizontal sixteen-by-nine diorama made entirely of handmade stop-motion plasticine clay, matte texture "
           "with visible fingerprints, warm window light, full-bleed scene that fills the entire frame edge to edge, no border, "
           "no frame, no vignette",
    personajes={
        "inventor": "a plasticine Japanese man about forty-eight years old, slim, with short black hair combed back, round "
                    "black-rimmed glasses, a white short-sleeved shirt with the sleeves rolled up, dark gray trousers and a "
                    "plain white cloth apron",
        "empresario": "a plasticine Japanese businessman about thirty-five years old, slim, with short black hair combed back, "
                      "round black-rimmed glasses, a dark gray double-breasted suit and a dark tie",
        "inventor_maduro": "a plasticine Japanese businessman about sixty years old, slim, with short gray hair combed back, "
                           "round black-rimmed glasses, a light gray suit and a dark blue tie",
        "anciano": "a plasticine Japanese old man about ninety-five years old, slim and smiling, with thin white hair combed "
                   "back, round black-rimmed glasses and a light gray suit",
        "esposa": "a plasticine Japanese woman about forty-five years old, with black hair in a low bun, a simple pale blue "
                  "1950s blouse, a dark skirt and a white kitchen apron",
    },
    objeto="a block of wavy golden fried plasticine noodles, square and crinkled, with tiny holes; a deep black iron frying "
           "pan of bubbling oil; and later a plain white foam cup with no printing",
    epoca="a small wooden shed in the backyard of a modest 1950s house in Ikeda, near Osaka, Japan: wooden walls, a bare light "
          "bulb, a second-hand cast-iron noodle-making machine with a hand crank, a gas burner, flour sacks without letters, "
          "bamboo baskets; no plastic packaging, no modern appliances",
    cierre="No text, no letters, no numbers or digits anywhere, no logos, no brand packaging, no modern objects.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "gancho": dict(sabor="tension"), "promesa": dict(sabor="espacio"), "origen": dict(sabor="espacio"),
    "guerra": dict(sabor="vacio"), "fila": dict(sabor="vacio"), "carcel": dict(sabor="tension"),
    "quiebra": dict(sabor="vacio"), "cobertizo": dict(sabor="tension"), "tempura": dict(sabor="esperanza"),
    "lanzamiento": dict(sabor="esperanza"), "copias": dict(sabor="tension"), "america": dict(sabor="espacio"),
    "vaso": dict(sabor="esperanza"), "nieve": dict(sabor="tension"), "espacio": dict(sabor="esperanza"),
    "mexico": dict(sabor="esperanza"), "cierre": dict(sabor="esperanza"),
}

# Música con Lyria adaptada al guion (antes: python fab.py biblioteca sugerir sopa_instantanea).
LYRIA = dict(
    estilo="Warm, handmade documentary score for a stop-motion story about a ruined man who invents a meal in his backyard: "
           "koto and shamisen plucks blended with pizzicato strings, marimba, felt piano, soft shakuhachi flute, light hand "
           "percussion and an upright bass. Curious and human, never epic, never cliché.",
    escenas={
        "gancho": ("A single questioning felt piano figure with a soft koto pluck over a low held tone, curious and a little ironic.", 3),
        "promesa": ("A gentle marimba pulse begins with an upright bass, the feeling of a life story about to unfold.", 4),
        "origen": ("Tender and nostalgic: koto and felt piano, a child's world in a small family shop, warm and simple.", 3),
        "guerra": ("Dark and hollow: low drones and distant taiko, the sound of loss, sparse and heavy.", 2),
        "fila": ("Cold winter night: shakuhachi over thin strings, hungry and patient, a small spark of an idea at the end.", 3),
        "carcel": ("Stern and cold: slow low strings, a ticking pulse, closed walls.", 3),
        "quiebra": ("Everything falls: a slow descending piano line, silence between notes, then a small stubborn held tone.", 2),
        "cobertizo": ("Stubborn tinkering through the night: plucked shamisen, ticking marimba, small comic failures and restarts.", 4),
        "tempura": ("Delighted discovery: bright marimba and glockenspiel flourish with sizzling texture, a warm eureka.", 6),
        "lanzamiento": ("Hopeful bustle: a lively pizzicato and koto groove, a small shop filling with people.", 6),
        "copias": ("Tension and rivalry: busy low strings, a nervous pulse, many hands copying.", 5),
        "america": ("Wide and curious: a gentle travelling groove with piano and brushed drums, a new world.", 4),
        "vaso": ("Inventive and playful: pizzicato and marimba building a clever little machine, light and bright.", 6),
        "nieve": ("Cold and tense live broadcast: low strings and soft taiko under falling snow, then warmth breaking through.", 5),
        "espacio": ("Floating and wondrous: soft pads, glockenspiel and koto harmonics, weightless and proud.", 5),
        "mexico": ("Warm and wide: flowing piano arpeggios with a soft guitar and koto, a sunny everyday feeling.", 6),
        "cierre": ("Return to the opening piano figure, now warm and resolved, a small smile, then a calm ending.", 4),
    },
    tramos=[
        (["gancho", "promesa", "origen"],
         "Begin from near silence. End on a held tone that can flow into the next piece. No loud ending."),
        (["guerra", "fila", "carcel", "quiebra"],
         "Begin softly with a low held tone. End on a sustained low tone that can flow into the next piece."),
        (["cobertizo", "tempura", "lanzamiento"],
         "Begin softly with a held tone. End on a bright sustained tone that can flow into the next piece."),
        (["copias", "america", "vaso", "nieve"],
         "Begin gently with a held tone. End on a sustained tone that can flow into the next piece."),
        (["espacio", "mexico", "cierre"],
         "Begin very softly. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Cada año, el mundo se come más de ciento veinte mil millones de estas sopas.",
        "Y la inventó un hombre que, a los cuarenta y siete años, lo había perdido todo.",
        "Sin empresa, sin dinero y con dos años de cárcel a cuestas.",
        "Lo único que le quedaba era su casa, y un cobertizo de madera en el patio.",
        "Ahí, solo, con una máquina de fideos usada y la sartén de su esposa, cambió la forma de comer del planeta.",
    ]},
    {"id": "promesa", "frases": [
        "Es una historia de hambre, de una fila larguísima en una noche helada.",
        "De una cárcel por regalar dinero.",
        "De un plato de tempura que le dio la respuesta.",
        "Y de un vaso que terminó en el espacio.",
        "Esta es la historia de la sopa instantánea, y de Momofuku Ando.",
    ]},
    {"id": "origen", "frases": [
        "Nace en mil novecientos diez, en Taiwán, que entonces era territorio japonés.",
        "Pierde a sus padres siendo muy pequeño.",
        "Lo crían sus abuelos, que tienen una tiendita de telas.",
        "Ahí aprende a vender, a contar y a regatear.",
        "Es un muchacho que no se queda quieto: siempre está buscando qué vender.",
        "A los veintidós años ya tiene su propia empresa textil.",
        "Y poco después se muda a Osaka, en Japón, a hacer negocios en grande.",
    ]},
    {"id": "guerra", "frases": [
        "Pero llega la Segunda Guerra Mundial.",
        "Las bombas caen sobre Osaka, y sus fábricas y oficinas quedan en cenizas.",
        "Cuando termina la guerra, Ando tiene treinta y cinco años, y tiene que empezar de cero.",
        "Japón está en ruinas, y lo peor es el hambre.",
        "Falta arroz, falta pan, y miles de personas comen lo que pueden.",
    ]},
    {"id": "fila", "frases": [
        "Una noche de invierno, Ando pasa por un mercado negro cerca de la estación de Umeda.",
        "Ve una fila larguísima de gente, temblando de frío en la oscuridad.",
        "Todos esperan lo mismo: un plato de fideos caliente.",
        "Ando se queda mirando esa fila.",
        "Piensa que la gente haría lo que fuera por un plato de fideos.",
        "¿Y si se pudieran preparar en casa, en minutos, solo con agua caliente?",
        "Pero la idea se queda guardada. Todavía no es su momento.",
    ]},
    {"id": "carcel", "frases": [
        "Ando sigue haciendo negocios, y le va bien.",
        "Tan bien, que empieza a darles becas a estudiantes pobres.",
        "Pero las autoridades de la posguerra ven ese dinero de otra forma.",
        "Dicen que regalar becas es una manera de no pagar impuestos.",
        "En mil novecientos cuarenta y ocho lo condenan por evasión fiscal.",
        "Y pasa dos años en la cárcel.",
    ]},
    {"id": "quiebra", "frases": [
        "Al salir, lo invitan a presidir una cooperativa de crédito, un pequeño banco local.",
        "Es un puesto de prestigio.",
        "Hasta que en mil novecientos cincuenta y siete, la cooperativa quiebra.",
        "Y Ando, como presidente, lo pierde todo.",
        "Le quitan casi todo lo que tiene, para pagar las deudas.",
        "Tiene cuarenta y siete años. Le queda una sola cosa: su casa en Ikeda, cerca de Osaka.",
        "Cualquier otro se habría rendido.",
        "Pero él se acuerda de aquella fila en la noche helada.",
    ]},
    {"id": "cobertizo", "frases": [
        "En el patio de su casa construye un cobertizo de madera, no más grande que un cuarto.",
        "Consigue una máquina de fideos de segunda mano y una sartén honda.",
        "Y se pone cinco metas.",
        "La sopa tiene que saber bien. Tiene que durar meses en la alacena.",
        "Tiene que estar lista en minutos. Tiene que ser barata, y segura.",
        "Trabaja solo, desde el amanecer hasta pasada la medianoche, sin un solo día de descanso.",
        "Durante casi un año, todo le sale mal.",
        "Los fideos se pegan, se deshacen, o se echan a perder en pocos días.",
        "Secarlos al sol no funciona. Ahumarlos, tampoco.",
        "Cada fracaso termina en la basura, y cada mañana vuelve a empezar.",
    ]},
    {"id": "tempura", "frases": [
        "Hasta que una noche, en la cocina, ve a su esposa Masako preparar tempura.",
        "Ella sumerge los vegetales en masa, y luego en aceite hirviendo.",
        "Ando ve las burbujas, y entiende algo.",
        "El aceite caliente saca el agua de la masa, y deja miles de hoyitos diminutos.",
        "Corre al cobertizo y fríe un bloque de fideos ya sazonados.",
        "El agua se escapa. Los fideos quedan secos, crujientes, y llenos de poros.",
        "Les echa agua hirviendo, y en un par de minutos esos poros se llenan.",
        "Los fideos se ablandan, como recién hechos.",
        "Había nacido la sopa instantánea.",
    ]},
    {"id": "lanzamiento", "frases": [
        "El veinticinco de agosto de mil novecientos cincuenta y ocho sale a la venta.",
        "Se llama Chicken Ramen: fideos con sabor a pollo.",
        "Ando tiene cuarenta y ocho años.",
        "Y hay un problema: cuesta treinta y cinco yenes.",
        "Unas seis veces lo que costaba un plato de fideos en un puesto de la calle.",
        "Los comerciantes creen que nadie va a pagar eso por un bloque seco.",
        "Ando organiza pruebas en las tiendas, para que la gente lo pruebe ahí mismo.",
        "Y los comerciantes se equivocan. La gente prueba, y vuelve.",
        "Al poco tiempo, su empresa cambia de nombre: Nissin.",
    ]},
    {"id": "copias", "frases": [
        "Y en cuanto el invento triunfa, empiezan las copias.",
        "Aparecen decenas de fábricas que hacen fideos fritos idénticos.",
        "Algunos venden fideos mal hechos, que se echan a perder.",
        "Ando registra su método y pelea por él.",
        "Pero entiende que copiar un invento es fácil. Lo difícil es inventar el siguiente.",
        "Y el siguiente le espera muy lejos de Japón.",
    ]},
    {"id": "america", "frases": [
        "En mil novecientos sesenta y seis, Ando viaja a Estados Unidos a vender sus fideos.",
        "Ahí se da cuenta de algo que nunca había pensado.",
        "En un supermercado ve que ahí no hay tazones para fideos, ni nadie que use palillos.",
        "Así que los compradores parten el bloque, lo meten en vasos de papel y le echan agua caliente.",
        "Y se lo comen con tenedor.",
        "Para ellos no es un platillo japonés. Es comida rápida.",
        "Ando lo ve, y se le ocurre la segunda gran idea de su vida.",
        "El vaso no es el problema. El vaso es la solución.",
    ]},
    {"id": "vaso", "frases": [
        "En el avión de regreso le sirven nueces en un envase con tapa de aluminio, que se despega.",
        "Esa tapa se la queda.",
        "Diseña un vaso de espuma, ligero y que no quema las manos.",
        "Y resuelve un detalle genial: los fideos van suspendidos a la mitad del vaso.",
        "Así no se rompen en el camino, y el agua caliente los cubre por todos lados.",
        "Encima, la tapa de aluminio, como aquella del avión.",
        "En mil novecientos setenta y uno, con sesenta y un años, lanza su sopa de vaso: Cup Noodles.",
        "Y al principio, casi nadie la compra.",
    ]},
    {"id": "nieve", "frases": [
        "Hasta febrero de mil novecientos setenta y dos.",
        "En las montañas de Japón, unos guerrilleros se atrincheran en una cabaña con una rehén.",
        "Todo el país sigue el asedio en vivo por televisión, durante diez días.",
        "Hace tanto frío, que la comida de los policías se congela.",
        "Y en la pantalla aparecen los policías, en medio de la nieve, comiendo fideos calientes de un vaso.",
        "Millones de personas lo ven.",
        "Al día siguiente, todos quieren la sopa de los policías.",
    ]},
    {"id": "espacio", "frases": [
        "La sopa de Ando le da la vuelta al mundo.",
        "En el año dos mil, los japoneses la eligen como el mejor invento japonés del siglo veinte.",
        "Por encima del karaoke.",
        "Y a los noventa y cinco años, Ando cumple un último sueño.",
        "Crea una sopa para comer sin gravedad, y la manda al espacio con un astronauta japonés.",
        "Muere en dos mil siete, a los noventa y seis años.",
        "Hoy, en Ikeda, hay un museo con una réplica de aquel cobertizo.",
        "Decía que su secreto era jugar golf, y comer su sopa casi todos los días.",
    ]},
    {"id": "mexico", "frases": [
        "Y su invento llegó hasta nuestras cocinas.",
        "En México se comen más de mil millones de sopas instantáneas al año.",
        "Las más famosas aquí son de otra empresa japonesa: Maruchan.",
        "Tan famosas, que en México mucha gente le dice maruchan a cualquier sopa de vaso.",
        "La de la tiendita, la de la oficina, la de la quincena flaca.",
        "Con un vaso en la mano, cualquiera come caliente en tres minutos.",
        "Todas usan la misma idea de aquel cobertizo: fideos fritos, porosos, que reviven con agua caliente.",
    ]},
    {"id": "cierre", "frases": [
        "Ando decía que la paz llega cuando la gente tiene suficiente para comer.",
        "Y que nunca es demasiado tarde para empezar.",
        "Él empezó a los cuarenta y siete, sin nada, en un cobertizo.",
        "Así que la próxima vez que esperes tres minutos frente a tu vaso, acuérdate de aquella fila en la noche helada.",
        "Ahora dime tú: ¿te habrías atrevido a empezar de cero a los cuarenta y siete años, o te habrías rendido?",
        "Te leo en los comentarios.",
        "Y si te gustan las historias de las marcas que tienes en tu cocina, suscríbete.",
        "La próxima ya se está moldeando.",
    ]},
]
