# -*- coding: utf-8 -*-
"""Plastitube (alias pieza_oculta) — «El Carpintero que lo Perdió Todo… e Inventó LEGO».
Motor SECUENCIA. 3.º de la tanda de la fórmula de marcas (canales/formula/pieza_oculta.md): marca con giro humano; 10-12 min.
Ficha histórica (Wikipedia «Ole Kirk Christiansen», «Lego», «History of Lego», «The Lego Group», «Godtfred Kirk Christiansen»,
«Hilary Page»; lego.com/history «The beginning of the LEGO Group», «Godtfred Kirk Christiansen», «LEGO System in Play»; Brick
Fanatics, entrevista sobre el pato de madera 40501; LEGO newsroom 2022 y prensa mexicana 2023-2026 sobre la planta de Nuevo León):
Ole Kirk Christiansen nació el 7-abr-1891 en Filskov, Dinamarca, uno de 13 hijos de una familia pobre; a los 14 años (1905), aprendiz
de carpintero con su hermano mayor. 1916: compra con sus ahorros un taller de carpintería en Billund y se casa con Kirstine; hace
casas y muebles para los granjeros. Cuatro hijos: Johannes, Karl Georg, Godtfred (n. 8-jul-1920) y Gerhardt. 1924: Karl Georg y
Godtfred, niños, prenden unas virutas al intentar encender una máquina de cola caliente; arden el taller y la casa familiar. Reconstruye.
Principios de los años 30: la Gran Depresión hunde los precios del campo; los granjeros dejan de comprar; despide a sus empleados hasta
el último. 1932: muere Kirstine; él queda con cuatro hijos. Empieza a hacer juguetes baratos de madera para vender algo; sus hermanos le
prestan dinero con la condición de que deje los juguetes, y él se niega. 1932 = fundación oficial; 1934: nombre LEGO, de «leg godt»,
«juega bien». Desde 1935, el pato de madera con ruedas, de abedul con tres capas de barniz. Anécdota (lego.com, recuerdo de Godtfred):
para un pedido de la Co-op, Godtfred les dio solo dos capas para ahorrar; su padre le ordenó ir por los patos a la estación, darles la
tercera capa y volver a mandarlos. Lema «solo lo mejor es suficientemente bueno» (1936), que Godtfred talló en letreros de madera.
Godtfred ayudaba en el taller desde los 12 años. 1942: un cortocircuito incendia la fábrica; se pierden existencias y planos. 1947: LEGO
es la primera juguetera danesa en comprar una máquina de moldeo por inyección de plástico, que cuesta más del doble de las ganancias del
año anterior; ese año consiguen muestras de los ladrillos Kiddicraft del inglés Hilary Page (patente de 1939). 1949: «Automatic Binding
Bricks», basados en los de Kiddicraft. Ventas pobres en los 50: muchos envíos devueltos; una revista danesa del ramo predijo que el
plástico nunca reemplazaría a la madera. 1954: Godtfred, subdirector; en un viaje a Inglaterra habla con el comprador de juguetes de
Magasin du Nord (Copenhague): a los juguetes les falta un sistema. Febrero de 1955: «LEGO System i Leg», Plan de Ciudad n.º 1, en la feria
de Núremberg (reseñas mixtas). 28-ene-1958: patente danesa del ladrillo con tubos por dentro (agarre). Ole Kirk muere el 11-mar-1958 a los
66 años (paro cardiaco). Hilary Page murió el 24-jun-1957, a los 52, temiendo que su empresa se hundiera (se quitó la vida: no se dice en
el video); su viuda dijo que nunca supo de LEGO; en 1981 LEGO compró a sus herederos los derechos restantes (≈ 45 000 libras). Febrero de
1960: un incendio destruye el almacén de juguetes de madera; al día siguiente Godtfred decide dejar la madera; sus hermanos Karl Georg y
Gerhardt no están de acuerdo y se van; él les compra su parte. Agosto de 1978: la minifigura. 2004: pérdida de 1 931 millones de coronas,
«casi en quiebra» (Mads Nipper); se recupera en 2005. Hoy: la juguetera más grande del mundo por ventas (desde 2015); ~36 000 millones de
piezas al año (~1 140 por segundo); seis ladrillos de 2x4 se combinan de 915 103 765 maneras. Ingresos 2024: 74 300 millones de coronas.
México: planta en Ciénega de Flores, Nuevo León (zona de Monterrey), operando desde 2008; la más grande de LEGO por empleados (> 7 000
en 2026); más de 149 millones de sets en 2025; en septiembre de 2026 anunció 400 millones de dólares para ampliarla (2026-2029).
Elementos prohibidos en imagen: ladrillos con letras o logotipo, cajas modernas con marca, letras y números; a las personas se las
describe por oficio, nunca por nombre (filtro de personas destacadas de Flow); mujer = «cheerful plasticine housewife figure…»
(hallazgo de sopa_instantanea: con nacionalidad y edad exacta Flow la rechaza).
"""

TITULO = "El Carpintero que lo Perdió Todo… e Inventó LEGO"
ARCHIVO = "lego_carpintero"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 96
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Pronunciación para Chatterbox (solo lo que se dice en voz; subtítulos y Whisper ven la grafía real).
FONETICA = {
    "Ole Kirk Christiansen": "Óle Kirk Kristiansen",
    "Ole Kirk": "Óle Kirk",
    "Christiansen": "Kristiansen",
    "Billund": "Bílund",
    "Godtfred": "Gótfred",
    "Kirstine": "Kirstíne",
    "Kiddicraft": "Kídicraft",
    "Hilary Page": "Jílari Péich",
    "Page": "Péich",
    "LEGO": "Lego",
    "leg godt": "leg got",
    "Núremberg": "Núremberg",
    "Filskov": "Fílskou",
}

# Whisper escribe «Godfred», «2x4» y «el ego» (= «sale Lego»); umbral por frase SOLO donde la transcripción dice eso (4-nov-2026)
CER_MAX_POR_FRASE = {"juguetes_7": 0.025, "pato_2": 0.025, "fuego2_3": 0.025, "fracaso_5": 0.015,
                     "sistema_4": 0.025, "fuego3_2": 0.025, "fuego3_6": 0.025, "hoy_8": 0.035}

SECUENCIA = dict(
    video_s=180,        # el usuario (3-nov): los 3 primeros minutos en clips de Flow
    clip_s=10,
    video_calidad="360p",
    combinar=True,      # cada clip de 10 s une dos momentos del guion con una transición dibujada
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.5,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={"scene-016": 0.0},   # Whisper oyó «Heck» (4-nov)
    recorte_por={"scene-002": 0.075, "scene-003": 0.12, "scene-004": 0.09, "scene-007": 0.09, "scene-012": 0.115,
                 "scene-014": 0.12, "scene-015": 0.09, "scene-016": 0.09, "scene-017": 0.115},   # letterbox medido 4-nov
    carpeta_descargas="flow-lego_carpintero",
)

# Ficha visual del episodio: se repite PALABRA POR PALABRA en cada prompt donde aparezca (triple anclaje).
FICHA = dict(
    estilo="Cinematic horizontal sixteen-by-nine diorama made entirely of handmade stop-motion plasticine clay, matte texture "
           "with visible fingerprints, warm window light, full-bleed scene that fills the entire frame edge to edge, no border, "
           "no frame, no vignette",
    personajes={
        "carpintero": "a plasticine Danish carpenter about forty years old, tall and lean, clean-shaven, with short light brown "
                      "hair combed back, round dark-rimmed glasses, a white collarless shirt with rolled sleeves, a dark brown waistcoat, dark trousers "
                      "and a worn leather carpenter's apron",
        "carpintero_mayor": "a plasticine Danish businessman about sixty-five years old, tall and lean, clean-shaven, with thin "
                            "gray hair combed back, thick round dark-rimmed glasses, a gray three-piece suit and a dark tie",
        "nino": "a plasticine Danish boy about twelve years old with short blond hair, a gray wool sweater, short trousers, "
                "knee socks and a small canvas apron",
        "hijo": "a plasticine Danish man about thirty-five years old, clean-shaven, with short dark blond hair combed back, no glasses, a light gray suit, a "
                "white shirt and a dark blue tie",
        "esposa": "a cheerful plasticine housewife figure with fair hair in a low bun, a long dark blue 1920s dress and a white "
                  "apron",
        "ingles": "a plasticine English toymaker about fifty years old, slim, with dark wavy hair, a neat mustache, a tweed "
                  "jacket and a bow tie",
    },
    objeto="small plain plasticine toy bricks in bright red, yellow, blue and white with round studs on top and no letters; a "
           "wooden pull-along toy duck painted red, yellow and white on four small wooden wheels",
    epoca="a small 1920s-1930s carpentry workshop in a Danish village: wooden workbenches, hand saws, planes, piles of birch "
          "wood and curly shavings, a cast-iron stove, small-paned windows, flat green fields outside; no plastic, no modern "
          "tools, no electric lights except a bare bulb",
    cierre="No text, no letters, no numbers or digits anywhere, no logos, no brand packaging, no modern objects.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "gancho": dict(sabor="tension"), "promesa": dict(sabor="espacio"), "origen": dict(sabor="espacio"),
    "fuego1": dict(sabor="tension"), "crisis": dict(sabor="vacio"), "juguetes": dict(sabor="esperanza"),
    "pato": dict(sabor="espacio"), "fuego2": dict(sabor="tension"), "plastico": dict(sabor="esperanza"),
    "fracaso": dict(sabor="vacio"), "sistema": dict(sabor="esperanza"), "patente": dict(sabor="vacio"),
    "page": dict(sabor="vacio"), "fuego3": dict(sabor="tension"), "legoland": dict(sabor="esperanza"), "hoy": dict(sabor="esperanza"),
    "mexico": dict(sabor="esperanza"), "cierre": dict(sabor="esperanza"),
}

# Música con Lyria adaptada al guion (antes: python fab.py biblioteca sugerir lego_carpintero).
LYRIA = dict(
    estilo="Warm, handmade documentary score for a stop-motion story about a village carpenter who loses everything and "
           "invents a toy: wooden percussion, marimba, felt piano, pizzicato strings, a little accordion and celesta, clarinet "
           "and upright bass. Nordic, playful and human, never epic, never cliché.",
    escenas={
        "gancho": ("A single questioning felt piano figure with soft wooden clicks like bricks snapping, curious and a little ironic.", 3),
        "promesa": ("A gentle marimba pulse begins with an upright bass, a life story about to unfold.", 4),
        "origen": ("Tender and rustic: accordion and felt piano, a Danish village workshop, sawing rhythm, warm and simple.", 4),
        "fuego1": ("Sudden alarm: tense tremolo strings and low drums, crackling texture, then a hollow silence.", 3),
        "crisis": ("Grief and hard times: slow clarinet over sparse piano, empty and cold, a small stubborn held tone at the end.", 2),
        "juguetes": ("A small hopeful spark: celesta and pizzicato like a music box, wooden toys coming to life.", 5),
        "pato": ("Gentle and wise: warm strings with a playful clarinet, a father teaching his son.", 4),
        "fuego2": ("Fire again: dark low strings and pounding timpani, then ashes and a long held note.", 2),
        "plastico": ("Bold and modern: a clockwork marimba groove with a new bright synth-free shimmer, a risky bet.", 5),
        "fracaso": ("Disappointment: a slow descending bassoon line, boxes coming back, quiet and sad.", 2),
        "sistema": ("Eureka on a ferry: rising strings and marimba building a clever little machine, light and bright.", 6),
        "patente": ("Bittersweet: a triumphant figure that turns soft and sad, a farewell.", 3),
        "page": ("Melancholic and quiet: lonely piano in a minor key, rain-like pizzicato.", 2),
        "fuego3": ("The last fire: tense drums that resolve into a firm decision, a single brave chord.", 4),
        "legoland": ("Amazed and playful: a carousel-like waltz on celesta and accordion, crowds of visitors, a small miracle.", 5),
        "hoy": ("Wide and joyful: a full playful orchestra-lite groove, colorful and proud.", 6),
        "mexico": ("Warm and sunny: flowing guitar and marimba, a festive everyday feeling.", 6),
        "cierre": ("Return to the opening piano figure, now warm and resolved, a small smile, then a calm ending.", 4),
    },
    tramos=[
        (["gancho", "promesa", "origen"],
         "Begin from near silence. End on a held tone that can flow into the next piece. No loud ending."),
        (["fuego1", "crisis", "juguetes", "pato"],
         "Begin softly with a low held tone. End on a sustained tone that can flow into the next piece."),
        (["fuego2", "plastico", "fracaso", "sistema"],
         "Begin softly with a held tone. End on a bright sustained tone that can flow into the next piece."),
        (["patente", "page", "fuego3", "legoland"],
         "Begin gently with a held tone. End on a sustained tone that can flow into the next piece."),
        (["hoy", "mexico", "cierre"],
         "Begin very softly. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Cada segundo, en el mundo se fabrican más de mil cien piezas de LEGO.",
        "Y todo empezó con un carpintero de pueblo que lo perdió todo, no una vez, sino una y otra vez.",
        "Se le quemó el taller con su casa adentro.",
        "Se quedó sin clientes, sin empleados, y sin su esposa.",
        "Su propia familia le prestó dinero con una condición: que dejara de hacer juguetes.",
        "Él dijo que no.",
    ]},
    {"id": "promesa", "frases": [
        "Esta es una historia de tres incendios.",
        "De un pato de madera que tuvo que regresar de la estación del tren.",
        "De unos ladrillos de plástico que las tiendas devolvían en cajas.",
        "Y de una idea que casi nadie entendió, hasta que cambió la forma de jugar del planeta.",
        "Esta es la historia de LEGO, y de Ole Kirk Christiansen.",
    ]},
    {"id": "origen", "frases": [
        "Nace en mil ochocientos noventa y uno, en un pueblito del campo de Dinamarca.",
        "Es uno de trece hermanos, en una familia muy pobre.",
        "A los catorce años entra como aprendiz de carpintero, con su hermano mayor.",
        "Aprende a cortar, a cepillar y a ensamblar sin un solo clavo de más.",
        "Después hace el servicio militar, y estudia en una escuela técnica.",
        "En mil novecientos dieciséis junta sus ahorros y compra un taller en Billund, un pueblo rodeado de granjas.",
        "Ese mismo año se casa con Kirstine.",
        "Hace casas, puertas, ventanas y muebles para los granjeros de la zona.",
        "Tiene cuatro hijos, un taller lleno de trabajo, y un futuro que parece seguro.",
    ]},
    {"id": "fuego1", "frases": [
        "Hasta un día de mil novecientos veinticuatro.",
        "Dos de sus hijos, todavía niños, intentan encender una máquina para calentar pegamento.",
        "Una chispa cae sobre las virutas de madera.",
        "En minutos, el fuego se come el taller entero.",
        "Y con el taller, se quema también la casa de la familia.",
        "Ole Kirk mira las cenizas, y decide hacer lo único que sabe: volver a construir.",
        "Levanta un taller más grande que el anterior, y una casa nueva.",
    ]},
    {"id": "crisis", "frases": [
        "Pero en los años treinta llega la Gran Depresión.",
        "Los precios del campo se desploman, y los granjeros ya no tienen con qué pagar una mesa o una puerta.",
        "El trabajo se acaba. Ole Kirk despide a sus empleados, uno por uno, hasta el último.",
        "Y en mil novecientos treinta y dos, cuando parece que no puede ir peor, muere su esposa Kirstine.",
        "Se queda solo, con cuatro hijos y un taller vacío.",
    ]},
    {"id": "juguetes", "frases": [
        "Entonces se le ocurre algo pequeño.",
        "Con los restos de madera empieza a hacer juguetes baratos: animales, carritos, figuras con ruedas.",
        "Si la gente no puede comprar una mesa, quizá pueda comprarle un juguete a sus hijos.",
        "Para sobrevivir, sus hermanos le prestan dinero.",
        "Pero le ponen una condición: que deje esos juguetes y vuelva a la carpintería seria.",
        "Ole Kirk se niega.",
        "En mil novecientos treinta y cuatro le pone nombre a su pequeña empresa.",
        "Junta dos palabras danesas, leg godt, que significan juega bien.",
        "Y de esas dos palabras sale el nombre de su marca: LEGO.",
        "Años después, alguien les hizo notar una coincidencia: en latín, lego quiere decir yo junto, o yo armo.",
        "Ole Kirk no lo sabía. Todavía no fabricaba nada que se armara.",
    ]},
    {"id": "pato", "frases": [
        "Su juguete estrella es un pato de madera con ruedas, que se jala con una cuerda.",
        "Cada pato lleva tres capas de barniz.",
        "Un día, su hijo Godtfred, que ayuda en el taller desde los doce años, decide ahorrar.",
        "A un pedido grande le da solo dos capas, y lo manda a la estación del tren.",
        "Cuando su padre se entera, le ordena ir a la estación, recoger todos los patos, darles la tercera capa, y volver a mandarlos.",
        "Su hijo nunca lo olvidó.",
        "Con su propia mano talló en madera el lema de su padre: solo lo mejor es suficientemente bueno.",
        "Y lo colgó en las paredes del taller.",
    ]},
    {"id": "fuego2", "frases": [
        "En mil novecientos cuarenta y dos, en plena Segunda Guerra Mundial, un cortocircuito incendia la fábrica.",
        "Se queman los juguetes, la madera, y hasta los planos de cada modelo.",
        "Es el segundo incendio.",
        "Ole Kirk tiene cincuenta y un años, y otra vez empieza desde el suelo.",
    ]},
    {"id": "plastico", "frases": [
        "Después de la guerra, aparece un material nuevo que casi nadie toma en serio: el plástico.",
        "En mil novecientos cuarenta y siete, Ole Kirk hace la apuesta más loca de su vida.",
        "Compra una máquina para moldear plástico, la primera de una juguetera en toda Dinamarca.",
        "Le cuesta más del doble de lo que la empresa había ganado el año anterior.",
        "Ese mismo año llegan a sus manos unos ladrillos de plástico ingleses, de una marca llamada Kiddicraft.",
        "Los inventó un juguetero llamado Hilary Page, y tienen unos botones arriba para encajar uno sobre otro.",
        "En mil novecientos cuarenta y nueve, LEGO saca sus propios ladrillos, muy parecidos a esos.",
    ]},
    {"id": "fracaso", "frases": [
        "Y son un fracaso.",
        "Las tiendas no los quieren. Muchos envíos regresan a la fábrica sin venderse.",
        "Una revista danesa de juguetes asegura que el plástico nunca va a reemplazar a la madera.",
        "Los ladrillos encajan, pero se zafan con facilidad. Las torres se caen.",
        "Para muchos, es un capricho de un viejo carpintero.",
        "Entonces, ¿cómo pasa un juguete que nadie quería a estar en casi todas las casas del mundo?",
        "La respuesta no salió de la fábrica. Salió de una conversación en un viaje.",
    ]},
    {"id": "sistema", "frases": [
        "La respuesta llega en mil novecientos cincuenta y cuatro, en un viaje a Inglaterra.",
        "Godtfred, ya convertido en subdirector, conversa con el comprador de juguetes de una gran tienda de Copenhague.",
        "El hombre le dice algo que se le queda clavado: a los juguetes les falta un sistema.",
        "Cada juguete se compra, se usa, y se olvida.",
        "Godtfred piensa: ¿y si cada pieza sirviera con todas las demás?",
        "¿Y si cada caja nueva hiciera más grande lo que el niño ya tiene?",
        "En mil novecientos cincuenta y cinco presentan el Sistema de Juego, con un plan de ciudad para construir.",
        "Por primera vez, los ladrillos no son un juguete. Son un mundo.",
    ]},
    {"id": "patente", "frases": [
        "Pero falta un detalle: que no se zafen.",
        "La solución es meter unos tubos huecos por dentro de cada ladrillo.",
        "Los botones de arriba quedan apretados entre esos tubos, y las piezas se agarran con fuerza.",
        "El veintiocho de enero de mil novecientos cincuenta y ocho registran la patente.",
        "Ese es el ladrillo que sigue encajando hoy con uno de hace casi setenta años.",
        "Ole Kirk llega a verlo.",
        "Pero seis semanas después, en marzo de mil novecientos cincuenta y ocho, muere de un ataque al corazón, a los sesenta y seis años.",
    ]},
    {"id": "page", "frases": [
        "¿Y el inglés que inventó los primeros ladrillos?",
        "Hilary Page no vio nada de esto.",
        "Su empresa se hundía en deudas, y murió en mil novecientos cincuenta y siete, convencido de que había fracasado.",
        "Su viuda contó después que él nunca supo lo que LEGO haría con su idea.",
        "En mil novecientos ochenta y uno, LEGO les compró a sus herederos los derechos que quedaban.",
    ]},
    {"id": "fuego3", "frases": [
        "Y todavía faltaba un incendio.",
        "En febrero de mil novecientos sesenta, el fuego destruye el almacén donde LEGO guardaba sus juguetes de madera.",
        "Al día siguiente, Godtfred toma la decisión más dura de la familia.",
        "LEGO deja la madera para siempre. Solo ladrillos de plástico.",
        "Dos de sus hermanos no están de acuerdo, y se van de la empresa.",
        "El taller donde empezó todo, el de los patos y las tres capas de barniz, se acaba ahí.",
        "Godtfred les compra su parte, y se queda solo al frente.",
    ]},
    {"id": "legoland", "frases": [
        "Y en Billund pasa algo raro: miles de turistas empiezan a llegar a la fábrica.",
        "Quieren ver de dónde salen los ladrillos.",
        "Así que en mil novecientos sesenta y ocho, en ese mismo pueblo de granjas, abre Legoland.",
        "Un parque con ciudades, barcos y aviones, todos hechos de ladrillos.",
        "El pueblo donde un carpintero no podía vender ni una mesa, se vuelve famoso en todo el mundo por sus juguetes.",
    ]},
    {"id": "hoy", "frases": [
        "En mil novecientos setenta y ocho llegan los muñequitos de plástico, las minifiguras.",
        "Pero la historia de perderlo todo se repite.",
        "En dos mil cuatro, la empresa pierde tanto dinero que su propio director dice después que estuvo casi en quiebra.",
        "El nieto del carpintero, que la dirigía, deja el puesto, y por primera vez LEGO queda en manos de alguien de fuera de la familia.",
        "Venden los parques, recortan, y vuelven a lo básico: el ladrillo.",
        "Al año siguiente, ya vuelve a ganar dinero. Se levanta, como su fundador.",
        "Hoy es la juguetera más grande del mundo.",
        "Fabrica unos treinta y seis mil millones de piezas al año.",
        "Y con solo seis ladrillos de dos por cuatro se pueden armar más de novecientos quince millones de combinaciones distintas.",
    ]},
    {"id": "mexico", "frases": [
        "Y una buena parte de esos ladrillos se hace muy cerca de aquí.",
        "Desde dos mil ocho, LEGO tiene una fábrica en Nuevo León, junto a Monterrey.",
        "Hoy es la fábrica más grande de LEGO en todo el mundo, con más de siete mil trabajadores.",
        "Solo en dos mil veinticinco, de ahí salieron más de ciento cuarenta y nueve millones de cajas.",
        "Y en septiembre de dos mil veintiséis, la empresa anunció cuatrocientos millones de dólares más para hacerla todavía más grande.",
        "Así que, si tienes un LEGO en casa, es posible que lo hayan armado manos mexicanas.",
    ]},
    {"id": "cierre", "post": 1.0, "frases": [
        "Todo empezó con un carpintero que se quedó sin taller, sin clientes y sin esposa.",
        "Que vio arder su trabajo tres veces.",
        "Y que, cuando su familia le pidió que dejara los juguetes, dijo que no.",
        "Ahora te pregunto a ti: después del segundo incendio, ¿tú habrías seguido, o habrías vuelto a hacer muebles?",
        "Cuéntamelo en los comentarios.",
        "Y si te gustan las historias de las cosas que tienes en casa, suscríbete a Plastitube.",
    ]},
]
