# -*- coding: utf-8 -*-
"""GUION — «Las 20 ARMADURAS más poderosas de Skyrim» (Crónicas de Tamriel, 18-nov-2026, sale el mié 25-nov 12:08 CDMX).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Datos de investigacion.md
(cada puesto con su URL, que van en la descripción; la voz NO cita fuentes, regla 12-nov). Secuela de tes_armas_poderosas.
Voz: SOLO EL PROFETA (18-nov: 3 quejas nuevas de que la voz cambia mucho; el usuario: «tú elige lo mejor para el canal»).
Críticas con contraburla: @frankortiz7101 + @Lagartija_Vaquera (cr1, las voces), @stratosincaster4500 (cr2, la recompensa del
3:33 de builds). Agradecimientos (≤ 10 días): @RelatorNoctambulo, @zaarondarklord6196, @Reyes3019, @Ivan-g9l2n, @CarlosLopez-x9j.
Campaña de suscripción antes del top 3 (~75 %). Radio Yermo en el cierre (R06). Turbo, corchetes SIN [whispers]/[excited];
el Profeta plano y burlón desde arriba.
"""

TITULO = "Las 20 ARMADURAS más poderosas de Skyrim"
ARCHIVO = "tes_armaduras_poderosas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {"Oblivion": "Oblívion", "jarl": "yarl", "Jarl": "Yarl", "Harkon": "Járkon", "Miraak": "Mirák",
            "Dawnguard": "Don-gard", "Dragonborn": "Drágon-born", "Riften": "Ríften", "Falkreath": "Fálkriz",
            "Volkihar": "Vólkijar", "Skyrim": "Escairim", "Boethiah": "Boétia", "Hircine": "Írsin",
            "Clavicus Vile": "Clávicus Vail", "Ysgramor": "Ísgramor", "Auriel": "Áuriel", "Peryite": "Périait",
            "Konahrik": "Konájrik", "Ahzidal": "Azídal", "Mzund": "Mzúnd", "Fahlbtharz": "Falbtarz",
            "Nchuak": "Nchúak", "Stalhrim": "Stáljrim", "stalhrim": "stáljrim", "Solstheim": "Sólsteim",
            "Apocrypha": "Apócrifa", "Karliah": "Kárlia", "Nahkriin": "Nákrin", "Skuldafn": "Skúldafn",
            "Bromjunaar": "Bromyúnar", "Haknir": "Jáknir", "Gyldenhul": "Guíldenjul", "Kolbjorn": "Kólbiorn",
            "Bthardamz": "Btárdamz", "Orchendor": "Órkendor", "Sinding": "Síndin", "Wuuthrad": "Úuzrad",
            "Sahrotaar": "Sajrotár", "Valerica": "Valérica", "Mehrunes Dagon": "Merúnes Dágon", "Ancano": "Ancáno",
            "Eorlund": "Éorlund", "Morokei": "Morokéi", "dremora": "drémora", "Rorik": "Rórik", "Haemar": "Jáemar",
            "Ralis Sedarys": "Rális Sedáris", "Kesh": "Kesh", "Tonilia": "Tonília", "Sovngarde": "Sóvengard", "Bethesda": "Bezésda", "Brynjolf": "Brínyolf", "Mercer Frey": "Mérser Frei", "Elisif": "Élisif"}

# 18-nov (s2): transcripciones leídas una a una; solo cambian las grafías de nombres (Staldrin, Yagnir, Periaid) y frases que hablan hasta el final
CER_MAX_POR_FRASE = {"ag1_0": 0.081, "ag1_1": 0.069, "ag1_2": 0.052, "ag1_3": 0.079, "cr1_0": 0.071, "cr2_0": 0.097, "gema_6": 0.041, "intro_3": 0.042, "p10_4": 0.029, "p11_1": 0.025, "p11_2": 0.049, "p12_1": 0.057, "p12_4": 0.051, "p14_0": 0.04, "p14_4": 0.032, "p15_3": 0.022, "p17_4": 0.058, "p19_0": 0.036, "p19_3": 0.031, "p1_2": 0.031, "p20_4": 0.031, "p2_6": 0.067, "p3_5": 0.051, "p4_0": 0.054, "p4_2": 0.06, "p6_1": 0.13, "p6_3": 0.031, "p6_4": 0.038, "p6_5": 0.048, "p7_0": 0.048, "p8_0": 0.077, "p8_4": 0.068}
TAIL_MAX_POR_FRASE = {"ag1_0": 0.79, "ag1_1": 0.88, "ag1_2": 1.02, "ag1_3": 0.59, "cr1_0": 0.71, "cr2_0": 0.94, "gema_6": 0.59, "intro_3": 0.8, "p10_4": 0.71, "p11_1": 0.75, "p11_2": 0.9, "p12_1": 0.63, "p12_4": 0.48, "p14_4": 0.97, "p15_3": 0.92, "p17_4": 0.7, "p19_3": 0.9, "p1_2": 1.13, "p20_4": 0.72, "p3_5": 0.72, "p4_0": 0.46, "p4_2": 0.56, "p6_1": 0.64, "p6_3": 0.7, "p6_4": 0.97, "p6_5": 0.58, "p8_4": 0.75}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-009": .8, "scene-010": .7, "scene-046": .8, "scene-047": .6, "scene-110": .6, "scene-120": .8, "scene-121": .6},   # 19-nov: vapor de Nchuak, onda del escudo de Auriel, Konahrik, tentáculos de Miraak (R16/R17)
    recorte_por={"scene-001": .10, "scene-108": .10, "scene-109": .10},   # 19-nov: marca de agua SKYRIMGAMES arriba a la derecha (qFgT0Ek-0IA)
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29", "Xander Rey Gaming",
                            "AtariGen 75", "NOB NO13", "Zephyr", "A Bard's Ballad", "Cameron Marks", "Gameplay Only", "Zboy896 Twitch Stream"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (Jeremy Soule; armar_musica_ost.py), sin pistas con canto

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Una máscara que, cuando estás a punto de morir, invoca a un sacerdote dragón para que pelee por ti.",
        "Una coraza que solo te dan si sacrificas a tu propio seguidor en un altar. Y un casco que escupe vapor y manda a volar a tus enemigos.",
        "Un pirata que enterró su armadura en cuatro cofres por toda una isla. Y una túnica que hace brotar tentáculos del suelo.",
        "[deadpan] Hoy, las veinte armaduras más poderosas de Escairim. Cascos, escudos, túnicas y conjuntos enteros. Con sus cifras, dónde se consiguen y la trampa de cada una.",
        "[sarcastic] Y quédate hasta el final, porque te voy a enseñar por qué una armadura de hierro puede protegerte exactamente igual que la mejor del juego.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. El Semblante de Mzund.",
        "Un casco dwemer de Drágon-born. Veinticuatro de armadura, doce de peso y más sesenta de aguante, que ya es casi lo máximo que da un encantamiento.",
        "Pero lo importante es su poder: el Aliento de Nchuak. Una ráfaga de vapor abrasador que quita quince puntos de vida por segundo.",
        "[deadpan] Y a veces, los enemigos que mata el vapor salen volando por los aires. Como en una tetera. Una tetera con cuernos.",
        "Está en el Gran Salón de Fahlbtharz, en Sólsteim. Primero el puzle de la caldera. Luego llenas tres accionadores con núcleos dinamo, y despiertan dos centuriones guardianes.",
        "Tras la reja, el casco. Y una palanca que te sube directo a la nieve. [sarcastic] Los dwemer: desaparecieron hace miles de años, pero el ascensor funciona mejor que los de mi edificio.",
    ]},
    {"id": "p19", "frases": [
        "Número diecinueve. La Máscara de Clavicus Vile.",
        "Veintitrés de armadura y solo siete de peso. Precios un veinte por ciento mejores, más persuasión y la magia regenerándose más rápido.",
        "Para tenerla, la misión El mejor amigo de un daedra, desde el nivel diez. En Fálkriz te mandan a buscar a un perro. El perro habla. Se llama Barbas.",
        "Barbas te lleva a Vergüenza de Jáemar, el santuario de Clávicus Vail. El príncipe quiere el Hacha pesarosa. Y al final te da a elegir: la máscara, o matar al perro y quedarte el hacha.",
        "[deadpan] Las dos cosas no. Es un daedra del trato, no una tienda de descuentos.",
        "Y una trampa visual: si te la pones con la Cota de ébano, a tu personaje le puede desaparecer la cabeza. [sarcastic] Precios mejores, eso sí. Sin cabeza, pero con descuento.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. El Escudo de Ísgramor.",
        "Treinta de armadura. Un veinte por ciento de resistencia a la magia y más veinte de salud.",
        "Llega al final de los Compañeros, en La gloria de los muertos. Éorlund Melena Gris repara el hacha Úuzrad en la Forja del Cielo, y la llevas hasta la Tumba de Ísgramor.",
        "El escudo está en el cofre del jefe, cerca del final de la tumba. Y ojo: si entras antes de tiempo con algún truco, el cofre estará vacío. Solo aparece durante la misión.",
        "[deadpan] Y en primera persona, al bloquear, tapa más de un tercio de la pantalla. Te protege de los hechizos. Y de ver lo que te ataca.",
    ]},
    {"id": "cr1", "frases": [
        "Un momento, que hay correo. @frankortiz7101, con nueve likes: «Abusas mucho con las voces de IA, algunas me dan hasta grima, es mejor como estaba antes».",
        "Y Lagartija Vaquera: «Qué molesto cómo cambia la voz constantemente, no consigo relajarme».",
        "[deadpan] Mensaje recibido. Hoy la voz no cambia ni una vez. Una sola, de principio a fin. La mala noticia es que es la mía.",
        "[sarcastic] Relájate, Lagartija. Ponte una de estas armaduras. Así, por lo menos, algo te protege de mí.",
    ]},
    {"id": "p17", "frases": [
        "Número diecisiete. La Piel del salvador.",
        "Una coraza ligera de Írsin. Veintiséis de armadura y solo seis de peso. Quince por ciento de resistencia a la magia y la mitad de daño del veneno.",
        "La misión es Emboscada nocturna, desde el nivel uno. En la cárcel de Fálkriz conoces a Síndin, que se convirtió en lobo y mató a una niña. Cazas al Ciervo blanco, y Írsin te da su reto.",
        "En la Gruta del Hombre Hinchado decides: si matas y desuellas a Síndin, la Piel. Si lo perdonas, el Anillo de Írsin.",
        "[deadpan] Y sí: la Piel del salvador es, literalmente, la piel de un hombre lobo. Moda sostenible, versión Escairim.",
        "Y el truco: perdona a Síndin, mata a los cazadores con él, termina la misión y recibe el anillo. Después, mátalo. Írsin te da también la Piel. [sarcastic] Un dios de la caza que no lleva la cuenta.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. La Armadura real de vampiro.",
        "Treinta de armadura, nueve de peso, y un solo encantamiento que lo dice todo: la magia se regenera un ciento veinticinco por ciento más rápido.",
        "Está en el Castillo Vólkijar, en las Ruinas de Vólkijar, durante Persiguiendo ecos con Serana. En la sala de los ataúdes, sobre un armario, junto a una espada de plata.",
        "Y esa sala es la única fuente que reaparece. Si se te pierde, vuelves y está otra vez ahí.",
        "[deadpan] Hay una versión todavía más elegante, la del Señor vampiro. Esa no te la puedes poner. Es para los que mandan. Tú solo eres el invitado que recoge cosas de los armarios.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. El Escudo de Áuriel.",
        "Treinta y dos de armadura. Y no tiene un encantamiento normal: guarda la energía de cada golpe que bloqueas.",
        "A los cinco bloqueos empieza a brillar. A los quince está cargado del todo. Y un golpe con escudo potente suelta una onda que se parece al grito Fuerza implacable.",
        "Se consigue en el Valle Olvidado de Don-gard. Le quitas el Modelo de perfección de rubí a un gigante de escarcha, abres el portal, y en el bosque un Belígero falmer pelea contra los trols. Él lleva el escudo.",
        "[sarcastic] Y la trampa: si usas la onda cargada en una pelea a puñetazos, cuenta como agresión. Te ponen recompensa. Por pegar demasiado bien.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. Las reliquias de Azídal.",
        "Siete piezas de un antiguo sacerdote dragón. La armadura de castigo: un cinco por ciento de dejar paralizado siete segundos a quien te golpee.",
        "Las botas: caminar sobre el agua. Los guanteletes: absorben la mitad de la magia de los hechizos. Y la máscara de Azídal: más daño de fuego.",
        "Con cuatro reliquias puestas, el Genio de Azídal: más diez a Encantamiento. [deadpan] Solo con cuatro, eh. Con cinco se apaga. Un genio con problemas de matemáticas.",
        "La misión es Desenterrado, en el Túmulo de Kólbiorn. Financias la excavación de Rális Sedáris en cuatro pagos: mil, dos mil, tres mil y cinco mil. Once mil de oro en total.",
        "Y al final, el propio Azídal sale a pelear. [sarcastic] Le pagas once mil a un arqueólogo, para que te desentierre al dueño enfadado. Inversión segura.",
        "Ah, y con las botas, el salto sobre el agua es más alto, y puedes coger peces con la mano.",
    ]},
    {"id": "ag1", "frases": [
        "Antes del top trece, los comentarios de esta semana. @zaarondarklord6196: «Qué maravilla de narración y datos, por primera vez en años aprendí algo nuevo en Escairim».",
        "@Reyes3019, que encontró el canal por casualidad, se enganchó desde el primer minuto y se acaba de suscribir. Te damos la bienvenida. Y @Ivan-g9l2n: «Con este video ya sé qué hacer en mi siguiente partida». Ahora ya sabes qué ponerte.",
        "@RelatorNoctambulo, con diez likes, nos dejó su build antimagia: bretón, piedra del Señor, piel de dragón, y armadura pesada con resistencias. Buen gusto. Hoy le toca a esa armadura.",
        "Y @CarlosLopez-x9j dice que el profeta tiene mucha aura y que por eso tiene su voto. [deadpan] Lo sé. Pero gracias por decirlo en voz alta.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. La Armadura de maestre del gremio.",
        "Cuatro piezas de cuero, setenta y seis de armadura y diecisiete de peso. Y cada pieza, un encantamiento de ladrón.",
        "La armadura: más cincuenta de capacidad de carga. Botas: carterista. Guantes: ganzúas. Y la capucha: precios un veinte por ciento mejores.",
        "Te la entrega Tonília en Una nueva dirección, cuando te nombran maestre del Gremio de Ladrones, en la Ratonera bajo Ríften.",
        "[sarcastic] Más carga, mejores precios, ganzúa y carterista. Es la única armadura del juego diseñada para el trabajo de oficina. Si tu oficina es la casa de otro.",
        "[deadpan] Mercer Frey llevaba una versión con más armadura, pero sin encantar. Y no te la puedes poner. Mercer siempre se quedaba con la mejor parte.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. La Armadura etérea antigua.",
        "La de la Hermandad Oscura, pero la buena. Setenta y dos de armadura y apenas siete y medio de peso: el conjunto más ligero de esta lista.",
        "Inmunidad total al veneno. Botas silenciosas. La capucha, un treinta y cinco por ciento más de daño con arco. Y los guantes, doble daño en ataques furtivos con armas de una mano.",
        "Para encontrarla, Gabriella te da la Ficha de Olava. Olava la Débil te lee el futuro en Carrera Blanca. Y entonces, detrás del trono de Punta de la Arpía, aparece una palanca que antes no existía.",
        "[deadpan] Una palanca que solo existe cuando una adivina dice que existe. En Escairim, hasta la arquitectura se cree el horóscopo.",
    ]},
    {"id": "cr2", "frases": [
        "Otro correo. @stratosincaster4500, sobre las builds: «Tres treinta y tres: “Y nadie te pone recompensa”, cuando aparece un mensaje que dice mil de recompensa en La Grieta».",
        "Tienes toda la razón, el veneno no es crimen. Lo que de verdad es crimen es que te vean con la mano metida en el bolsillo del guardia.",
        "[sarcastic] El del clip no era yo. Era un aficionado. Los profesionales llevan la armadura de maestre del gremio. Con carterista al treinta y cinco por ciento.",
    ]},
    {"id": "p11", "frases": [
        "Número once. El Anulador de hechizos.",
        "El escudo de Périait. Treinta y ocho de armadura. Y al bloquear crea una custodia que absorbe hasta cincuenta puntos de daño mágico. Sin gemas de alma, sin gastar magia.",
        "La misión es La única cura, desde el nivel doce. En la Capilla de Périait, Kesh el Aseado te pide ingredientes para el incienso. Périait te manda a la ruina dwemer de Btárdamz, a matar a Órkendor.",
        "[deadpan] Y un detalle que casi nadie ve: la custodia es cóncava. Sigue la forma del escudo. Todas las demás son al revés.",
        "Contra un mago muy fuerte, la custodia se rompe y te tambalea. [sarcastic] Pero contra el aliento de un dragón, levantas el escudo y el dragón se queda pensando qué hizo mal.",
    ]},
    {"id": "honor", "frases": [
        "Antes del top diez, dos menciones de honor que se quedaron fuera por muy poco.",
        "La Corona dentada. Veintitrés de armadura, sin encantamiento, y no se puede templar. Pero ocupa la ranura del pelo, así que la puedes llevar a la vez que una máscara de sacerdote dragón. Dos cascos en una cabeza.",
        "Y la armadura falmer pesada, con el casco de cascarudo de Don-gard: noventa y siete de armadura por cincuenta y tres de peso. Mejor que la de ébano en las dos cosas. [deadpan] Hecha con caparazones de bicho. La mejor armadura de ébano, superada por un insecto.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. La Túnica de archimago.",
        "No tiene armadura. Pesa uno. Y aun así está en esta lista. Todos los hechizos de cinco escuelas cuestan un quince por ciento menos, más cincuenta de magia, y la magia se regenera el doble de rápido.",
        "Es tu premio al terminar El Ojo de Magnus en el Colegio de Hibernalia. Derrotas a Ancáno en la Sala de los Elementos y te nombran archimago.",
        "Y un fallo que vale oro: la túnica no ocupa la ranura de la diadema. Así que puedes llevarla con una máscara de sacerdote dragón. Con Morokéi, otro cien por ciento de regeneración.",
        "[deadpan] A veces el juego te da dos o tres túnicas, por si acaso. Y hay un héroe en Sóvengard que lleva una copia. No se la puedes robar. Lo intenté.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. La Armadura de Ruiseñor.",
        "Cuero negro y morado, capa y una capucha que te tapa la cara. Sesenta y nueve de armadura, dieciocho de peso, y más veinticinco de armadura con las cuatro piezas puestas.",
        "Aguante y resistencia a la escarcha, botas silenciosas, ganzúa y más daño a una mano en los guantes, e Ilusión más barata en la capucha.",
        "La recibes en La vuelta del triunvirato, con Kárlia y Brynjolf, en el Salón de los Ruiseñores, al sur de Ríften. Te la pones, y le juras lealtad a Nocturnal.",
        "[deadpan] Y aquí está la trampa que arruina miles de partidas. La versión de la armadura se fija con tu nivel al EMPEZAR la misión. No al recibirla.",
        "Si la empiezas antes del nivel treinta y dos, te quedas con la versión débil para siempre. [sarcastic] Nocturnal, diosa de la suerte. La tuya, no.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Konájrik. La máscara del Señor de la guerra.",
        "Veinticuatro de armadura: el casco con más armadura base de todo el juego original. Y su encantamiento solo despierta cuando tu salud baja del quince por ciento.",
        "Con un quince por ciento de probabilidad: una explosión que empuja todo, una capa de llamas y una gran curación. Y con un tres por ciento, además, aparece un sacerdote dragón espectral que pelea a tu lado durante sesenta segundos.",
        "Para tenerla, reúnes las ocho máscaras de los sacerdotes dragón. En Laberintia te pones la Máscara de madera, viajas al pasado, al Santuario de Bromyúnar, y colocas las ocho en sus bustos.",
        "[deadpan] Ahora las malas noticias. La máscara de Nákrin solo se consigue en Skúldafn, durante la misión principal. Si no la recoges, no hay segunda oportunidad. Konájrik, imposible.",
        "Y colocarlas en los bustos borra el templado que les hayas hecho. Todo el trabajo de herrería, a la basura.",
        "Y si vendes cualquiera de las ocho a un mercader, también. [sarcastic] Un dios de la guerra que depende de que no vendas tus cosas. Como un coleccionista. Con fuego.",
        "[deadpan] Y un dato de los creadores: el Santuario de Bromyúnar iba a ser una casa para el jugador. No llegó a tiempo. Te quedaste con una sala de bustos y una máscara de madera.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. El equipo de Mirák.",
        "La túnica absorbe el quince por ciento de la magia de los hechizos y del aliento de los dragones. Las botas y los guantes, un cinco cada uno. Un veinticinco por ciento en total.",
        "Y cuando te golpean, a veces brotan del suelo los tentáculos de Apócrifa. Te rodean y explotan: cien de daño de veneno a todo lo que esté cerca.",
        "Su máscara es nivelada. A nivel sesenta llega a veintisiete de armadura: el casco más protector del juego, ligero o pesado.",
        "Lo consigues matando a Mirák en En la cima de Apócrifa. Lees los libros negros, cruzas los capítulos, doblegas a Sajrotár y subes a la cima.",
        "[deadpan] Y con la túnica, la piedra del Atronach y la ventaja Atronach, llegas al cien por ciento de absorción. Inmune a los hechizos. [sarcastic] Eso sí, los tentáculos salen igual. Inmune, pero con tentáculos.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. La Armadura de Estigma Mortal.",
        "Ligera, de stáljrim. Setenta y ocho y medio de armadura, trece de peso. Y crece con cada pieza que te pones.",
        "Aguante, carga, y daño con dos armas a la vez. Y el yelmo: respiras bajo el agua y, con las cuatro piezas, más cien de armadura. Más que toda la armadura del conjunto junto.",
        "Desde el nivel treinta y seis. El pirata Jáknir Estigma Mortal mandó enterrar su armadura en cuatro cofres por todo Sólsteim. Y no hay marcadores: hay que leer el mapa del tesoro.",
        "Uno en el Bajío de Jáknir. Otro junto a Tel Mithryn. Otro al suroeste de Roca del Cuervo. Y el último, en una charca de marea al noroeste.",
        "Y el último cofre trae la llave del Túmulo de Guíldenjul, en la Isla de los horkers: ochenta montones de oro y el fantasma de Jáknir.",
        "Con sus dos cimitarras únicas. En total, por lo menos seis mil cuatrocientas monedas de oro.",
        "[deadpan] Dice la leyenda que el primero que abrió un cofre se puso el yelmo y empezó a gritar. Y que aún se le oye en el bajío. [sarcastic] Normal. Yo también grito cuando me pruebo la ropa de un muerto.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. La Cota de ébano.",
        "Una coraza pesada de Boétia. Cuarenta y cinco de armadura y veintiocho de peso. Es la coraza pesada más ligera del juego. La daédrica protege solo tres puntos más, y pesa veintidós más.",
        "Te mueves en silencio, y todo enemigo que se acerca recibe cinco de daño de veneno por segundo. Tu cuerpo se vuelve una sombra negra con humo verde.",
        "Y hasta funciona como radar: el humo sale en cuanto alguien se vuelve hostil. El veneno daña incluso a los draugr y a los vampiros.",
        "El precio: La llamada de Boétia, desde el nivel treinta. En el Próstilo de Boétia sacrificas a tu propio seguidor en el altar. Luego, en la Cresta de Punta del Cuchillo, matas al Campeón de Boétia, que la lleva puesta.",
        "Y en los archivos del juego quedan restos de una segunda misión que se cortó: Boétia te iba a mandar a matar a la yarla Elisif.",
        "[deadpan] Tu seguidor te cargó la mochila doscientas horas. Y tú lo cambiaste por una coraza. [sarcastic] A Boétia le encanta. Y a mí también, para qué mentir.",
    ]},
    {"id": "campana", "frases": [
        "Antes del top cuatro, un dato. De cada cien que ven este canal, solo trece están suscritos.",
        "Ya somos casi siete mil, y vamos camino de diez mil. Suscribirte es un botón, y cuesta mucho menos que un seguidor sacrificado en un altar.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. La Armadura de stáljrim. Pesada y ligera.",
        "El stáljrim es hielo nórdico encantado. La pesada: ciento dos de armadura, lo mismo que las placas de dragón, con cinco menos de peso. Es la armadura forjable que más protege por cada unidad de peso.",
        "La ligera: setenta y ocho y medio con solo trece de peso. Y sobre stáljrim, los encantamientos de escarcha son un veinticinco por ciento más fuertes.",
        "Para forjarla necesitas Herrería de ébano y terminar Un nuevo yacimiento de stáljrim: Déor Tallador, en la Aldea Skaal, te manda a buscar al herrero Baldor Hierro Forjado. Y se mina con el pico nórdico antiguo.",
        "[deadpan] Y la trampa: si Déor Tallador muere antes de terminar la misión, nunca podrás forjar stáljrim. Ni una pieza. Para siempre.",
        "[sarcastic] Toda una isla de hielo mágico, y el futuro de tu armadura depende de un anciano con muy mala salud.",
        "Y el nombre tiene truco: stál hrím, en islandés, significa escarcha de acero.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. La Armadura de escamas de dragón.",
        "La mejor armadura ligera del juego original. Ochenta y dos de armadura y solo veinte de peso. Con escudo, ciento once.",
        "Se forja con escamas de dragón. Y para eso, la ventaja Armadura de dragón: Herrería cien y todas las ventajas de una rama.",
        "Con Armadura ligera al máximo y todas las ventajas, sin escudo, llega a trescientos sesenta y dos de armadura en el menú. Un cincuenta y cinco por ciento menos de daño. Y templada, es la única ligera que llega al tope sin escudo.",
        "[deadpan] Y un secreto: puedes forjarla antes de que existan los dragones. En una colina al noreste del Paraje de Rórik hay un santuario de Akatosh con una escama de dragón. Y reaparece cada diez días.",
        "[sarcastic] Akatosh, dios del tiempo, dejándote escamas gratis cada diez días. Es la única suscripción de Escairim que no te cobran.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. La Armadura de placas de dragón.",
        "Placas de hueso, y un yelmo con forma de cráneo de dragón. Ciento dos de armadura y sesenta y cuatro de peso. Con escudo, ciento treinta y seis.",
        "Se forja con huesos y escamas de los dragones que matas. Y el templado, con hueso de dragón para la coraza y el escudo.",
        "Con todo al máximo, sin tocar la herrería y con escudo: quinientos veinticinco de armadura en el menú. Un setenta y ocho por ciento menos de daño. A dos puntos del máximo del juego.",
        "[deadpan] Y una vez templada, llega al tope pesando menos que la daédrica. Setenta y nueve contra noventa y seis con escudo. Y sus materiales son más fáciles de juntar.",
        "Y con Don-gard hay un hueso de dragón en el laboratorio de Valérica. Para forjar antes de que haya dragones.",
        "[sarcastic] Matas al dragón, te pones su cráneo de sombrero, y sales a pedir trabajo. Así es Escairim.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. La Armadura daédrica.",
        "Negra, con vetas rojas que brillan, y un yelmo con cuernos. Ciento ocho de armadura y ochenta y uno de peso. Con escudo, ciento cuarenta y cuatro. La armadura pesada más fuerte del juego.",
        "Cada pieza lleva un corazón de daedra. Lo sueltan los drémora, y hay algunos fijos: uno en Jorrvaskr, otro en las Ruinas de Vólkijar. Necesitas Herrería daédrica: Herrería noventa.",
        "La otra vía es la Fragua del atronach, bajo el Colegio de Hibernalia: una pieza de ébano, un corazón, un núcleo dinamo y una gema de alma negra. [deadpan] Hace todas las piezas. Menos las botas sin encantar. Porque sí.",
        "Y la razón del número uno. Con Armadura pesada al máximo y todas las ventajas, sin tocar la herrería, con su escudo, llega a quinientos sesenta de armadura. Y eso ya es el máximo: un ochenta por ciento menos de daño.",
        "[deadpan] Es la única armadura del juego que llega al tope solo con ventajas. Sin forja. Sin trucos. La única.",
        "Y los drémora, que van vestidos de daédrica de pies a cabeza, no te dejan saquearla. Te dan el corazón. La armadura, no.",
        "[sarcastic] Y un fallo de toda la vida: las botas, los guanteletes de mujer y el escudo no tienen el brillo rojo del resto. Bethesda nos dio la mejor armadura del juego, y se le olvidó enchufar los pies.",
    ]},
    {"id": "gema", "pre": 1.2, "frases": [
        "Y ahora, lo que prometí. Por qué la armadura de hierro puede protegerte igual que la daédrica.",
        "Cada punto de armadura reduce el daño físico. Solo el físico: contra la magia, la armadura no hace nada. Y el máximo del juego es un ochenta por ciento.",
        "Pero cada pieza que llevas puesta te da armadura oculta, que el menú no te enseña. Por eso, con escudo, al tope te bastan quinientos cuarenta y dos en el menú.",
        "Ahora la sorpresa. Con la herrería al máximo, cualquier armadura pesada templada llega al tope con su escudo. Hasta la de hierro: quinientos cuarenta y siete. El mismo ochenta por ciento que la daédrica.",
        "[deadpan] Y todo lo que pasa del tope, no te sirve de nada contra un golpe normal. Es desperdicio. Solo cuenta contra las armas que atraviesan armadura: ahí harían falta más de dos mil.",
        "Así que, una vez en el tope, lo único que importa es el peso. Y con la ventaja Condicionamiento, la armadura pesada no pesa. A partir de ahí, la armadura que elijas es pura moda.",
        "[sarcastic] La daédrica es la mejor de Escairim. Hasta que aprendes a forjar. Después, hasta el hierro te salva igual. Y la daédrica solo te sirve para verte bien en la foto.",
    ]},
    {"id": "cierre", "frases": [
        "Este es el top. De un casco que escupe vapor, al conjunto que llega solo al máximo del juego.",
        "Ahora te toca a ti. ¿Cuál falta? ¿Cuál te pones tú, y en qué nivel la conseguiste? Déjalo en los comentarios: los leo todos.",
        "Y suscríbete, que vamos camino de diez mil.",
        "[deadpan] Y si en vez de placas de dragón prefieres una armadura que funciona con núcleos de fusión, Radio Yermo, nuestro canal hermano, es todo Fallout. Hasta yo escucho esa radio. Nos vemos en Tamriel.",
    ]},
]
