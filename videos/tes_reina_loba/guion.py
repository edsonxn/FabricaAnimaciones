# -*- coding: utf-8 -*-
"""GUION — «La Reina Loba de Soledad» (Crónicas de Tamriel, 12-nov-2026). FORMATO NUEVO: historia de lore contada de principio a fin.
Motor SECUENCIA YT (gameplay de Skyrim por beat + escenas de Flow con gráficos de Skyrim + pegatinas + MG mg_tes + mapas tema tes).
Narra SOLO el Profeta (ganó la votación; plano, sin risas). Las demás voces SOLO interpretan a personajes de la historia (frases
sueltas marcadas con una tupla (personaje, texto) en ESCENAS; abajo se convierten en VOZ_POR_FRASE).
Lore verificado en _investigacion.md (UESP; libros «La Reina Loba» = novela dentro del juego, se dice así en la voz cuando toca).
Pregunta al público sobre el formato (el usuario, 12-nov) en `pregunta`. Críticas con contraburla: @brandovelasquez957 (cr1),
@rolfaso (cr2), @Eme_4r (cr3). Agradecimientos (≤ 10 días): @Motosauriorex, @claudiopizarro9601, @dsegurar, @JuAnK930111, @Exonik_Snk.
Corrección justa: @sinnombre5459. Campaña de suscripción antes del capítulo final (13 de cada 100; 6 660).
"""

TITULO = "La Reina Loba de Soledad: la Septim que casi se queda con Tamriel"
ARCHIVO = "tes_reina_loba"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
# Potema MUERTA (espíritu invocado y jefa de las catacumbas): voz de ultratumba tipo caballero de la muerte + eco, aplicada en la
# mezcla (nucleo/voz_fx.py; el usuario, 13-nov-2026: «me gusta la voz espíritu de Potema»). Potema viva va limpia.
VOZ_FX = {"intro_2": "espiritu", "c9_5": "espiritu", "c9_10": "espiritu", "c9_12": "espiritu"}
FONETICA = {"Oblivion": "Oblívion", "jarl": "yarl", "Jarl": "Yarl", "Sheogorath": "Sheógorath"}

CER_MAX_POR_FRASE = {"cierre_2": 0.029, "intro_5": 0.043, "c1_5": 0.023, "c1_6": 0.018, "c1_10": 0.004, "c2_6": 0.028, "c2_7": 0.018, "c2_8": 0.025, "c2_9": 0.022, "c3_2": 0.027, "c4_1": 0.03, "c4_4": 0.021, "c4_5": 0.027, "cr1_0": 0.04, "c5_1": 0.004, "c5_3": 0.028, "c5_5": 0.027, "c5_7": 0.045, "c5_10": 0.038, "c5_11": 0.031, "c5_17": 0.027, "c6_7": 0.011, "c6_8": 0.017, "c6_10": 0.029, "c6_11": 0.025, "c6_14": 0.029, "c6_15": 0.042, "ag1_0": 0.061, "ag1_1": 0.108, "ag1_2": 0.097, "ag1_4": 0.062, "cr2_0": 0.127, "c7_3": 0.004, "c7_4": 0.017, "c7_5": 0.004, "c7_6": 0.028, "cr3_0": 0.082, "c8_5": 0.016, "c8_6": 0.027, "c8_8": 0.018, "c8_9": 0.016, "c8_13": 0.027, "c9_3": 0.004, "c9_6": 0.022, "c9_8": 0.009, "c9b_2": 0.122, "c9b_3": 0.024, "c9b_5": 0.017, "c9b_6": 0.026, "cierre_1": 0.018}   # se rellena tras `seleccionar` con las falsas alarmas oídas (nombres de lore, @usuarios)
TAIL_MAX_POR_FRASE = {"intro_5": 0.554, "c1_5": 0.677, "c1_6": 0.969, "c1_10": 1.152, "c2_6": 0.706, "c2_7": 0.753, "c2_8": 0.766, "c2_9": 0.706, "c3_2": 1.08, "c4_1": 0.768, "c4_4": 0.656, "c4_5": 0.983, "cr1_0": 0.966, "c5_1": 1.053, "c5_3": 1.004, "c5_5": 0.572, "c5_7": 0.609, "c5_10": 0.685, "c5_11": 0.647, "c5_17": 0.939, "c6_7": 1.127, "c6_8": 0.377, "c6_10": 0.977, "c6_11": 0.481, "c6_14": 0.782, "c6_15": 0.224, "ag1_0": 0.961, "ag1_1": 0.878, "ag1_2": 0.783, "ag1_4": 0.69, "cr2_0": 0.721, "c7_3": 1.044, "c7_4": 0.466, "c7_5": 1.076, "c7_6": 0.808, "cr3_0": 0.771, "c8_5": 0.917, "c8_6": 0.541, "c8_8": 1.032, "c8_9": 0.764, "c8_13": 1.068, "c9_3": 1.639, "c9_6": 0.872, "c9_8": 1.187, "c9b_2": 0.024, "c9b_3": 0.917, "c9b_5": 0.805, "c9b_6": 0.784, "cierre_1": 0.49}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_palabras=["reaction", "react", "podcast", "tier list", "news", "shorts", "#shorts", "ai cine", "ai movie",
                             "ai generated", "elder scrolls online", "eso ", "(eso", "eso:", "keizaal", "mods", "mod:", "mod ", " mod",
                             "modded", "modlist", "enb", "reshade", "dlss", "4000", "lotd", "legacy of the dragonborn",
                             "skywind", "skyblivion", "high isle", "cinematic trailer", "online", "showcase", "add-on", "next gen", "remake", "twitch", "stream", "vod", "cities:", "navigator"],
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29", "Xander Rey Gaming",
                            "AtariGen 75", "NOB NO13", "Zephyr", "A Bard's Ballad", "Cameron Marks",
                            # 13-nov: marca de agua, subtítulos de guía, mods o juego en otro idioma (nucleo/texto_clips.py)
                            "Anarion Graphics", "GamerJustLikeYou", "MajorSlackAttack", "MajorSlackVideos", "Selene The Rebel Unchained",
                            "Silenced Red Mage", "Sleep Scenery", "StStrife", "Typical Pirate", "slyellow2", "Delikuzz", "ItsJabo",
                            "Farpoint Toys & Collectibles"]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # canal de videojuego: OST oficial de Skyrim y Oblivion (Jeremy Soule; armar_musica_ost.py)

# --- VOCES DE PERSONAJES (muestras en salida/muestras_personajes.mp3; biblioteca compartida de ElevenLabs, por id) ---
VOCES = {
    "el Profeta": "HNSF1CTQmub252yhXROX",
    # ronda 2 (12-nov-2026): voces DISEÑADAS en ElevenLabs Voice Design (cuenta 2, `_disenar_voces.py`, estudio sin eco) donde el
    # usuario las prefirió; Potema y Kintyra se quedan con la biblioteca (Victoria, Natalia)
    "Potema": "LgUbwisMonprbdDRIOUm",          # Victoria - Elegant & Dark Aristocrat (biblioteca)
    "Kintyra II": "oK6mHoBJSrcLlTyeOykK",      # Natalia (biblioteca)
    "Pelagio III": "Xkbt99yg0wQK29ooVX1a",     # diseñada pelagio 1
    "Sheogorath": "vZLzTlgovoHkXN1eJEXk",      # diseñada sheogorath 3
    "Uriel III": "MpMMvn4yxOBf4x3txXWj",       # diseñada uriel 3
    "Antíoco": "nIH9JfY1VmHnmZHgscae",         # diseñada viejo 3
    "Uriel II": "nIH9JfY1VmHnmZHgscae",
    "Styrr": "nIH9JfY1VmHnmZHgscae",
    "Pelagio II": "lrK14T8DoOblaouKClSZ",      # diseñada pelagio2 3
    "Duque Mentin": "CgycFFFrquBH0iX00t1w",    # diseñada corte 3
    "Maestro del ritual": "CgycFFFrquBH0iX00t1w",
    "Falk Barba de Fuego": "CgycFFFrquBH0iX00t1w",
    "Mensajera": "g3uwIWz6MnYB0XXYsnyW",       # diseñada mensajera 3
}

_ESC = [
    {"id": "intro", "pre": 0.4, "frases": [
        "[serious] Al oeste de Soledad, en la costa helada de Skyrim, hay una cueva. Afuera, dos esqueletos. Adentro, una luz azul, y voces que cantan el nombre de una mujer muerta hace quinientos años.",
        ("Maestro del ritual", "[serious] Reina Loba. Escucha nuestra llamada y despierta. ¡Invocamos a Potema!"),
        ("Potema", "[cold] ¡Sí! ¡Sí! Devuélvanme a este mundo."),
        "[deadpan] Si jugaste Skyrim, seguramente la venciste. Una calavera con diadema, sentada en un trono, en unas catacumbas debajo del Templo de los Divinos. Una misión secundaria más.",
        "Pero esa calavera fue una niña que a los doce años abrió la cerradura más difícil del palacio imperial. Una reina que hizo desaparecer a una emperatriz en una torre. Una madre que vio a su hijo morir quemado. Y una anciana que, según cuentan los libros, dejó una maldición que acabó con la cordura de un emperador.",
        "Hay una frase en Skyrim que casi nadie escucha. La dice Styrr, el sacerdote de Arkay de Soledad.",
        ("Styrr", "[thoughtful] Irónicamente, si viviera hoy, sería la única Septim viva. Por derecho, ahora sería emperatriz."),
        "[short pause] Esta es la historia de Potema Septim. La Reina Loba de Soledad. Y no es una historia de monstruos. [short pause] Es peor. Es una historia de familia.",
    ]},
    {"id": "c1", "pre": 1.2, "frases": [
        "Capítulo uno. La niña de las cerraduras.",
        "Todo empieza con un lobo. En el año sesenta y tres de la Tercera Era, la ciudad bretona de Camlorn, en Roca Alta, vive aterrada por un demonio hombre lobo.",
        "Un príncipe imperial, Pelagio, viudo y con un hijo llamado Antíoco, llega para cortejar a la princesa Quintila. Él con la espada y ella con la hechicería, matan a la bestia. Y Quintila encierra el alma del lobo dentro de una gema.",
        "Pelagio la convierte en anillo y se casa con ella. Y los libros dicen algo que hay que recordar: que el alma del lobo se quedó con la pareja hasta que nació su primer hijo.",
        "Ese primer hijo nace cuatro años después, en el sesenta y siete. Una niña. Su abuelo, el emperador Uriel Segundo, la mira en la cuna y dice que parece una loba a punto de saltar. La llaman Potema.",
        "La niña crece en el Palacio Imperial de la Ciudad Imperial, bajo la Torre de Oro Blanco. Y crece aburrida. Tan aburrida que aprende a hacer lo único que de verdad le interesa: abrir lo que está cerrado.",
        "Chantajea a la doncella de su madre, una elfa del bosque, para que le enseñe a forzar cerraduras. Le roba al archimago su libro de hechizos más antiguo. Al rey de Gilane, su corona. Y a su medio hermano Antíoco, una colección de grabados khajiitas que él prefería que nadie viera.",
        "[deadpan] Con eso último pagó un broche. Un broche con un diamante rojo. Recuerden ese diamante.",
        "Año ochenta. Llueve sobre la Ciudad Imperial desde hace semanas. Nadie recuerda cuándo salió el sol. Potema, de doce años, se esconde detrás de un tapiz, donde hay una piedra suelta en la pared. Y escucha.",
        "Del otro lado, su abuelo y su padre le explican al embajador de Soledad que la boda prometida con su tía no va a ocurrir. Y que el oro que debían devolver, tampoco. El embajador amenaza con el contrato firmado.",
        "Potema no espera al final. Corre al Salón de los Registros, donde se guardan hasta los Pergaminos Antiguos. Saca dos alfileres de su broche de diamante rojo, y abre la cerradura más difícil de su vida. Tardó casi medio minuto.",
        "Cuando el paje llega a buscar el contrato, ya no está. Y como el documento no existe, el emperador tiene que ofrecer otra cosa a cambio. Ofrece a su nieta.",
        ("Uriel II", "[thoughtful] Es, lo admito, por lo que veo de ella, muy tímida e inocente."),
        ("Pelagio II", "[serious] Tiene trece años. Edad suficiente para casarse."),
        "[short pause] El novio es Mantiarco, rey de Soledad. Sesenta y dos años. Gordo. Y Soledad está lejos, y hace frío. Potema llora. Pero se queda con el contrato. Por si acaso.",
        "Los libros lo cierran con una frase que lo dice todo: cuántas posibilidades, pensó Potema. Y se dio cuenta de que ya no estaba aburrida.",
    ]},
    {"id": "c2", "pre": 1.2, "frases": [
        "Capítulo dos. La reina de Soledad.",
        "Se casa a los catorce años, en el ochenta y uno. Al año siguiente muere su abuelo, y su padre se convierte en el emperador Pelagio Segundo. Hereda un tesoro vacío, y lo llena a su manera: disuelve el Consejo de Ancianos y obliga a cada consejero a volver a comprar su asiento.",
        "Mientras tanto, en Soledad, la niña imperial descubre que los nórdicos no la quieren. Las viejas casas de la ciudad desprecian a la forastera de Cyrodiil. Y el reino necesita un heredero que no llega.",
        "Pierde un embarazo. Y otro. Y otro. Durante quince años. Hasta que a los veintinueve, en el noventa y siete, da a luz a un hijo.",
        "El curandero, Kelmeth, la ve enseñar los dientes durante el parto y piensa en una loba pariendo. Ella le lanza un espejo a la cabeza.",
        ("Potema", "[angry] ¡Invoca a los daedra! ¡Cambio el alma de hasta el último de mis súbditos por un poco de alivio!"),
        "Pero mientras grita, no deja de trabajar. Entre contracción y contracción le da órdenes a Lord Vhokken, su mano derecha: un gigante calvo con voz de trueno.",
        "El problema se llama Bathorgh. Es el hijo del primer matrimonio del rey, dos años mayor que su madrastra, el heredero legítimo. En Soledad lo llaman el hombre al que no se puede golpear.",
        "Potema ya se había encargado del jefe guerrero del rey, Lord Thone, con pruebas falsas de traición. Ahora manda restaurar el viejo palacio de verano de la difunta reina. Y ahí, casualmente, aparecen cartas de amor entre la difunta reina y Lord Thone, fechadas justo cuando nació Bathorgh.",
        "Ese mismo día, Bathorgh gana el Torneo de Resistencia. Aguanta a nueve arqueros y a un escorpión gigante traído del Páramo del Martillo. Y esa misma noche, Mantiarco, llorando, lo deshereda y lo destierra.",
        "El bebé de Potema se llamará Uriel, como su bisabuelo. Ahora es el heredero de Soledad.",
        "Y aquí los libros aclaran algo que casi todos cuentan mal. Sus enemigos ya la llamaban la Reina Loba. Pero no por ningún parecido físico. [short pause] Ni era mujer lobo, ni lo fue nunca.",
    ]},
    {"id": "pregunta", "pre": 1.5, "frases": [
        "[serious] Un momento. Antes de seguir, una pregunta. Y la hago en serio.",
        "Esto es nuevo en el canal. Nada de listas, nada de tops. Una sola historia, contada de principio a fin, con su voz, su música y sus escenas.",
        "Al canal le hace mucha ilusión esto: que el lore de Elder Scrolls se cuente con buena edición y buena voz, para que lo disfrutemos todos. Porque este juego es de todos.",
        "Pero necesitamos saberlo de ustedes. ¿Les gusta este formato? Escríbanlo en los comentarios. Si quieren más historias así, las traemos. Si prefieren seguir solo con listas y tops, también lo vamos a saber.",
        "[deadpan] Y ahora, de vuelta a la familia. Que viene un funeral.",
    ]},
    {"id": "c3", "pre": 1.2, "frases": [
        "Capítulo tres. La gema del lobo.",
        "Año noventa y ocho. El emperador Pelagio Segundo muere en plena fiesta, y el rumor dice que lo envenenó uno de los consejeros a los que obligó a pagar por su asiento.",
        "Al funeral llegan sus hijos. Magnus, de diecinueve años, desde Almalexia. Céforo, de veintiuno, desde Gilane, con su esposa, la reina redguard Bianki. Antíoco, el heredero, de cuarenta y tres. Y la última en llegar, Potema, de treinta, radiante, con su viejo rey y su hijo de un año.",
        "El Consejo de Ancianos retrasa seis semanas la coronación de Antíoco. Seis semanas en las que Potema está en la capital. Y Antíoco lo sabe: pone a su maestro de espías a vigilarla.",
        "En un balcón, su madre, Quintila, enferma y moribunda, le predice a Potema su propia muerte, y la de Mantiarco en menos de un año. Y le hace un regalo: un collar con una gema de alma amarilla. La gema del hombre lobo de Camlorn, encantada con magia de Ilusión para hechizar a quien la mire.",
        "Potema la usa esa misma noche. Hechiza al espía de su hermano, entra en el estudio de Antíoco, usa su sello, y falsifica una carta en la que Antíoco confiesa ser hijo del mayordomo del palacio.",
        "A la mañana siguiente le da a elegir. O renuncia al trono, o el escándalo. [short pause] Y Antíoco se ríe.",
        ("Antíoco", "[deadpan] ¿Sabías que los hechizos de encanto, incluso los más poderosos, duran poco? Un buen sueldo motiva más."),
        "El espía seguía cobrando de Antíoco. Y Antíoco guardó la hoja donde Potema practicó su letra. Con eso, además, la acusa de haber falsificado las cartas de la difunta reina de Soledad.",
        ("Antíoco", "[serious] En el futuro, querida Reina Loba, no pongas dos veces la misma trampa. Yo seré emperador. Ahora vete."),
        ("Potema", "[cold] Sí, lo serás, hermano. [short pause] Pero no por mucho tiempo."),
        "Antíoco es coronado. Y la profecía de Quintila se cumple: Mantiarco muere al poco tiempo. Potema queda como regente de Soledad, en nombre de un niño de dos años. Con un collar que hechiza a quien lo mira.",
    ]},
    {"id": "c4", "pre": 1.2, "frases": [
        "Capítulo cuatro. Los elfos del mar.",
        "Antíoco reina veintiún años. Enormemente gordo, y marcado, según los libros, por todas las enfermedades venéreas conocidas. En el ciento cuatro tiene una hija con su segunda esposa: Kintyra.",
        "Y el Palacio Azul de Soledad se convierte en el lugar de moda de todos los reyes resentidos con el emperador. Potema escucha a todos. Y no le promete nada a nadie.",
        "Año ciento diez. Al puerto de Soledad llega un barco que nadie ha visto nunca. Casco de quitina, velas como membranas, y una tripulación de hombres sin color, como si su carne fuera una jalea blanca y transparente. Son maormer, los elfos del mar de Pyandonea.",
        "Viene su rey, Orgnum, a buscar aliados contra el Imperio. En el trono, Uriel, de once años, juega con su mascota. Y Potema hace lo que mejor sabe hacer.",
        "Humilla a los emisarios psijic del maestro Iachesis, los monjes de la isla de Artaeum, y les hace creer que va a aliarse con los maormer. Asustados, los psijic corren a aceptar el trato que les ofrecía Antíoco: defender la costa por doce millones. Antes pedían cincuenta.",
        "Al final lo hacen por ocho. Potema les paga los ocho, y le cobra los doce a su hermano. [deadpan] Y esa noche, el rey de los elfos del mar duerme con la regente de Soledad.",
        "Los libros dicen que a ella le encantó descubrir que su capacidad para mentir funcionaba en muchas culturas distintas.",
        ("Potema", "[cold] A veces, hacer que la gente te odie… es como se gana dinero."),
        "Tres meses después, frente a Artaeum, una tormenta repentina hunde la flota entera de Orgnum. Es la Guerra de la Isla. La gran victoria de Antíoco. [short pause] Y la pagó él dos veces.",
    ]},
    {"id": "cr1", "pre": 1.0, "frases": [
        "Un momento, que hay correo. @brandovelasquez957: «Ya basta, ya basta. ¿Cómo pretenden que duerma si a cada rato me cambian las voces? Decidan, o dejaré de poner sus videos para dormir».",
        "[deadpan] Decidimos. Hoy narra uno solo. Treinta y cinco minutos, la misma voz de principio a fin.",
        "[sarcastic] Eso sí: con una reina que se acuesta con elfos de jalea, un hijo quemado vivo y un emperador loco… no te prometo que duermas.",
    ]},
    {"id": "c5", "pre": 1.2, "frases": [
        "Capítulo cinco. La emperatriz de quince años.",
        "Año ciento diecinueve. Potema y su hijo visitan a Antíoco en la Ciudad Imperial. Y durante esa visita, el emperador cae en coma. [short pause] Muere al año siguiente. Nadie demostró nunca nada.",
        "Potema se viste de luto y se mira al espejo. Cincuenta y tres años. Una mecha plateada en el pelo caoba, y arrugas finas como una telaraña.",
        "Y entra al Consejo de Ancianos. Halaga a los consejeros. Alaba al difunto. Y luego, despacio, acusa: Kintyra no sería hija de Antíoco, sino de su esposa y del capitán de la guardia. O del chico que limpia la cisterna.",
        ("Potema", "[serious] La posteridad os juzgará. Sabéis lo que hay que hacer."),
        "El Consejo no la escucha. Esa noche, en la Sala de los Mapas, bajo una cúpula de cristal empapada por la lluvia, Kintyra, de quince años, le cierra el paso en el pasillo.",
        ("Kintyra II", "[serious] Tu presencia en la ceremonia no será bienvenida. Eso es todo. Adiós, tía."),
        "Kintyra Segunda es coronada el tres de Primera Semilla del año ciento veinte. Potema y Uriel son desterrados. Y Potema le dice a su cuñada, la reina Bianki, lo que hace mejor que hablar.",
        ("Potema", "[cold] La guerra."),
        "Empiezan disturbios en Skyrim y en el norte de Roca Alta. En otoño, el duque Mentin de La Cañada pide auxilio, y la joven emperatriz va en persona. Por el camino casi cae en una emboscada en las montañas Cola de Dragón, y la sorprende una ventisca mágica en una baronía donde nunca nieva.",
        "En la torre del castillo de La Cañada, Kintyra escribe una carta a su prometido. Y recibe una de él: ha recibido una petición de refuerzos con la letra de ella, y sale con un segundo ejército. [short pause] Kintyra nunca escribió esa carta.",
        "Desaparecen los guardias de la muralla. Se oye un forcejeo. Y cuando Kintyra se da vuelta, Potema y el duque ya están dentro de la habitación.",
        ("Kintyra II", "[angry] ¡Maldita seas, mírame! ¡Soy tu emperatriz!"),
        ("Potema", "[deadpan] Míralo así: te paso de gobernante de quinta a mártir de primera."),
        "Cuando le preguntan al duque por qué traicionó al Imperio, si fue por miedo, responde con dos palabras.",
        ("Duque Mentin", "[deadpan] Y el oro."),
        "Y sobre los rumores de que Potema tenía un ejército de muertos, el duque dice algo que casi nadie cuenta: que no es verdad. Que ella fomenta ese rumor. Porque su mejor arma es el miedo.",
        "Kintyra muere en su celda. La fecha más aceptada es el veintitrés de Fuego Hogar del año ciento veintitrés, por orden del hijo de Potema. Y todavía hoy, en Roca Alta, ese día se guarda luto. Lo llaman Diamantes Rotos.",
    ]},
    {"id": "c6", "pre": 1.2, "frases": [
        "Capítulo seis. La guerra del Diamante Rojo.",
        "El diamante rojo es el emblema de la dinastía Septim. Y ahora dos ramas de la misma familia se lo disputan.",
        "En el ciento veintiuno, Uriel asedia durante dos semanas una Ciudad Imperial mal defendida. Esa misma noche se pone la corona.",
        ("Uriel III", "[serious] Desde esta noche, soy Uriel Septim Tercero. Emperador de Tamriel."),
        "[deadpan] Su apellido de verdad era Mantiarco. Pero el apellido Septim valía más.",
        "Del otro lado quedan los dos hermanos menores de Potema. Céforo, rey de Gilane, en el Páramo del Martillo. Y Magnus, rey de Lilmoth, con un ejército de argonianos. Tamriel entero se parte en dos.",
        "En el ciento veinticinco Céforo recupera el oeste de Roca Alta. Los argonianos de Magnus cruzan Morrowind hasta Skyrim: pelean bien en verano y se retiran en invierno. Dos años de empate.",
        "Verano del ciento veintisiete. Un amanecer en una pradera de Skyrim, en un lugar llamado Estrella del Halcón. Insectos, bandadas de pájaros. Potema tiene sesenta años. Y llega un mensajero.",
        "Uriel ha sido derrotado y capturado por Céforo en la campiña de Ichidag, en el Páramo del Martillo.",
        ("Potema", "[annoyed] Ese torpe idiota."),
        "Pero no hay tiempo para llorar. Magnus está atrincherado en las ruinas del castillo de Kogmenthist. Al oeste, fuego de magos. Al este, la ciénaga, el terreno de los argonianos. Y Potema elige la ciénaga.",
        "Reúne a sus tropas, cyrodílicos, nórdicos, bretones y elfos oscuros bajo el estandarte del diamante rojo, y les habla.",
        ("Potema", "[serious] Hijos míos. He visto juego sucio, puñaladas por la espalda, salvajadas crueles y gratuitas. Y me complacen igual. Porque todos sois guerreros."),
        ("Potema", "[serious] Pero hoy, no os equivoquéis… hoy sois la guerra."),
        "Lo mira desde un cerro, con Vhokken. Dos enjambres de insectos de dos colores peleando sobre un terrón. Bolas de fuego. Nubes de ácido sobre las ruinas.",
        "Y entonces sube al cerro una jinete redguard con bandera blanca.",
        ("Mensajera", "[sad] Tu hijo está muerto. Lo quemaron dentro de su carruaje. [short pause] Está muerto."),
        "Una turba asaltó la caravana que llevaba a Uriel Tercero a juicio, y le prendió fuego al carruaje con él adentro. Céforo es proclamado emperador.",
        "Ese día, el ejército de Potema gana la batalla de Estrella del Halcón. [long pause] Ella no mira a nadie.",
    ]},
    {"id": "ag1", "pre": 1.5, "frases": [
        "Antes de lo que viene, los comentarios de esta semana. «El lore de Elder Scrolls es increíble», de @Motosauriorex. Por eso estamos aquí.",
        "«Lore de primera», de @claudiopizarro9601. «Es el primer video que veo de ustedes, nuevo sub», de @dsegurar. Bienvenido: escogiste buen día.",
        "@JuAnK930111 dice que estos videos le dan ganas de volver a Skyrim por millonésima vez. Y @Exonik_Snk, que siempre vuelve a Skyrim por creadores así, y pide la voz con acento khajiita. [deadpan] El Profeta no hace acentos.",
        "Los leemos todos. Los buenos, y los que duelen. Y se toman en cuenta para mejorar cada video.",
        "Por ejemplo, @sinnombre5459 tiene razón: al final de Dragonborn, Hermaeus Mora te cobra con los secretos de los Skaal, no de los Barbas Grises. Corregido.",
    ]},
    {"id": "cr2", "pre": 1.0, "frases": [
        "Y @rolfaso pregunta: «Buenazo el video, pero ¿está hecha con IA la voz, o qué?».",
        "[deadpan] Te contesto como contestaría Potema: con otra pregunta. Si la historia es verdad, ¿importa quién la cuenta?",
        "[sarcastic] Ella tenía generales vampiros. Y nadie les preguntó si eran naturales.",
    ]},
    {"id": "c7", "pre": 1.2, "frases": [
        "Capítulo siete. La loba sola.",
        "Después de Ichidag, los nobles de siete provincias se cambian de bando a cambio de más autonomía. A Potema solo le queda una ciudad. Soledad.",
        "Y es aquí, no antes, cuando el rumor se vuelve verdad. Durante diez años, la Reina Loba invoca daedra. Sus nigromantes levantan a los enemigos caídos y los ponen a pelear de su lado. Sus aliados la abandonan, a medida que crece su locura.",
        "Soledad se convierte en una tierra de muerte. Doncellas que son esqueletos podridos. Generales vampiros. Y en una cueva al oeste de la ciudad, rituales nigrománticos. Esa cueva todavía lleva el nombre: Cráneo de Lobo.",
        "Año ciento treinta y siete. Céforo y Magnus sitian Soledad. Un mes entero contra el Palacio Azul.",
        "Los libros lo cuentan desde los ojos de un niño: Pel, el hijo de Magnus. No puede acercarse al foso sin vomitar. Hay un olor raro, dulzón, a muerto. Podrían echar un millón de flores, dice, y no cambiaría nada.",
        "Todos sus primos han muerto en la guerra, o en las hambrunas por las cosechas quemadas. Magnus tiene cincuenta y ocho años. Céforo, sesenta. Y Potema, setenta.",
        "En la ciudad sitiada todavía funciona un gremio de magos. Pel le abre la puerta a una anciana con la cara como una manzana podrida y un remolino de pelo blanquísimo. Al cuello lleva una gema amarilla. Y dentro, a la luz de las velas, se ve una bestia de cuatro patas que da vueltas.",
        "La anciana le paga a un encantador nórdico, joven, para que le quite el encanto a la gema y le ponga otro. Una maldición. Un veneno lento, que le quita la sabiduría a quien la lleve, año tras año, hasta que pierde la razón.",
        "Y compra un anillo barato de resistencia al fuego. Al niño le dice que es un anillo de levitación, para su tío Céforo. Por si alguna vez tiene que saltar de lugares altos.",
        "Luego se agacha, y le cuelga la gema al cuello.",
        ("Potema", "[thoughtful] Algún día serás emperador, muchacho. El emperador Pelagio Septim Tercero. Y con esta gema como guía, la posteridad siempre te recordará."),
        "La anciana se va por un túnel, bajo un montón de piedras, hasta el corazón del castillo. Se acuesta en su cama. Y muere de vieja, mientras oye cómo se derrumba su castillo.",
        "Los libros dicen que, de haberla visto, se le habría notado una sonrisa sin dientes al dar su último aliento.",
        "[short pause] La Reina Loba no murió en batalla, ni la mató ningún héroe. Murió en su cama, a los setenta años, durante el asedio. Las crónicas, al menos, coinciden en eso.",
        "Tres años después, en el ciento cuarenta, el emperador Céforo muere al caerse de su caballo. [deadpan] Los libros no dicen si llevaba puesto un anillo. Tampoco hace falta.",
    ]},
    {"id": "cr3", "pre": 1.0, "frases": [
        "Y un último correo, de @Eme_4r, en el video de los Dwemer: «No hablaron del último Dwemer. ¿El Profeta está ciego?».",
        "[deadpan] Ciego, no. Selectivo. Pero ya que preguntas por gente que se pierde en su propia cabeza, déjame presentarte al sobrino de Potema.",
    ]},
    {"id": "c8", "pre": 1.2, "frases": [
        "Capítulo ocho. Pelagio el Loco.",
        "Ojo: hay dos versiones de su infancia. En la novela es un niño de doce años en el asedio. En las crónicas, un joven de dieciocho, en su primera batalla. Lo que sí coincide es lo que vino después.",
        "De joven, Pelagio es guapo, simpático, le gustan el deporte, la magia y la música. Pero desde pequeño sufre terrores nocturnos. Y tras el asedio, le dan la corona de Soledad. La misma ciudad. El mismo palacio.",
        "Primero, el peso. Un diplomático de Corazón de Ébano escribe que es un alma robusta, con un corazón tan grande que le ensancha la cintura. Cinco meses después, una princesa de Firsthold dice que abrazarlo fue como si la agarrara un esqueleto.",
        "Luego, lo raro. Encierra en su cuarto a los príncipes y princesas de Silvenar, y no los deja salir hasta que le pasan, por debajo de la puerta, una declaración de guerra. Sin firmar. Y en un discurso en una fiesta, se arranca la ropa delante de todos.",
        "En el ciento cuarenta y uno se casa con Katariah, una elfa oscura, duquesa de Vvardenfell. Y en el ciento cuarenta y cinco muere Magnus, dormido. Hay quien acusa a Pelagio de matar a su padre. Nunca se probó.",
        "Pelagio es coronado emperador. El rumor dice que se desmayó al recibir la corona, y que Katariah lo sostuvo.",
        "Con el embajador argoniano de Rosanegra, solo habla con gruñidos y chillidos, porque cree que esa es su lengua. Los invitados del palacio se despiertan al amanecer con el ruido de los criados fregando: está obsesionado con la limpieza.",
        "Al final de un gran baile imperial, intenta ahorcarse. Y cuando empieza a morder a las visitas, en el ciento cuarenta y siete, lo encierran en un asilo. Katariah gobierna en su nombre.",
        "Hay un libro, El baile del asilo, que lo cuenta mejor que nadie. Pelagio organiza un baile en su asilo, con el oro de Katariah. Se viste con una túnica de seda negra, bordada con diamantes rojos. [short pause] Diamantes rojos.",
        "No llega nadie. La orquesta toca tres horas para un salón vacío. Y al subir la escalera, Pelagio se tira al suelo.",
        ("Pelagio III", "[nervous] ¡Más vino! ¡Más vino! [short pause] ¡Vino!"),
        "Se corta a sí mismo y a los celadores con los diamantes de su propia túnica. Años después, en el escritorio de una duquesa cleptómana, aparecen cinco montones de invitaciones, firmadas con su letra de niño. [short pause] Nadie las había recibido nunca.",
        "Pelagio Tercero muere en el ciento cincuenta y tres, de una fiebre corta, en su celda del templo de Kynareth, en una isla. Tenía treinta y cuatro años. Katariah se convierte en emperatriz, y gobierna casi medio siglo.",
        "¿Fue la gema de su tía? Los libros lo insinúan. Los bretones dicen que fue culpa de su estancia en Roca Alta. Y otra leyenda dice que la locura de Potema empapó las piedras del castillo de Soledad, y se le pegó al siguiente rey. [deadpan] Elijan la que menos los deje dormir.",
    ]},
    {"id": "campana", "pre": 1.5, "frases": [
        "Antes del final, un dato. De cada cien que ven este canal, solo trece están suscritos.",
        "Somos seis mil seiscientos sesenta. Si te suscribes, nos acercas a diez mil. Y si quieres más historias como esta, ese botón también es tu voto.",
    ]},
    {"id": "c9", "pre": 1.2, "frases": [
        "Capítulo nueve. Quinientos años después.",
        "Cuarta Era, año doscientos uno. En el Palacio Azul de Soledad, un hombre de Puente del Dragón le suplica a la jarl Elisif: de una cueva al oeste de la ciudad salen luces y ruidos extraños. La hechicera de la corte dice que son supersticiones. Y Falk Barba de Fuego, el administrador, te manda a ti.",
        "Es la misión El hombre de la falsa alarma. Bajas a la Cueva Cráneo de Lobo, saltas a un pozo, y llegas a unas ruinas con rayos azules. Los nigromantes están en pleno ritual.",
        ("Maestro del ritual", "[serious] Has dormido mucho tiempo el sueño sin sueños de la muerte, Potema. Ya no. ¡Escúchanos, Reina Loba!"),
        "Pero los nigromantes no quieren solo despertarla. Quieren atarla a su voluntad, con sangre de inocentes. Y ella se da cuenta.",
        ("Potema", "[angry] ¿Qué? ¿Qué están haciendo? ¡Necios! ¡Ustedes, hormigas, no tienen poder para atarme!"),
        "Matas al maestro del ritual en lo alto de la torre. Y la luz azul se escapa por un agujero del techo. [short pause] Rompiste la atadura. Y Potema quedó libre.",
        ("Falk Barba de Fuego", "[serious] ¿Potema en persona? Por favor, dime que los detuviste."),
        "Tiempo después, llega una carta. Es El despertar de la Reina Loba. Styrr, el sacerdote del Salón de los Muertos, te explica que sigue en forma de espíritu. Que si hubiera recuperado su cuerpo, ya estaríamos todos muertos. Y te da una llave.",
        "La entrada está al fondo del Templo de los Divinos, detrás de una verja. Un siervo de Potema rompió la pared hace unos días.",
        ("Potema", "[cold] Por fin has llegado. El héroe que impidió que me ataran vuelve a mi redil. Cuando mueras, te levantaré, y ocuparás tu sitio a mi lado."),
        "Las Catacumbas de Potema. Trampas de aceite, puertas de piedra que giran con palancas, una sala inundada de la que salen draugr del agua. Y su voz acompañándote todo el camino.",
        ("Potema", "[deadpan] ¿Puedes contra mi consejo interno? Veamos."),
        "Su espíritu lanza rayos que giran. Las flechas la atraviesan. De las tumbas salen oleadas de draugr, y ella los vuelve a levantar. Y cuando aparecen sus restos, un esqueleto con ropa fina y una diadema de piedra lunar, usa la Voz. [short pause] Fuerza Implacable. Porque también ella era Sangre de Dragón.",
        "Al final, en un trono, solo queda su calavera. Se la llevas a Styrr, que la santifica. Y Falk te da las gracias, con una petición: que nadie se entere. La jarl prefiere que el regreso de Potema siga en silencio.",
        "[deadpan] Por eso casi nadie conoce esta historia. Hasta Skyrim la quiso callar.",
    ]},
    {"id": "c9b", "pre": 1.2, "frases": [
        "Pero en el Palacio Azul queda una puerta cerrada. El ala suroeste. El Ala de Pelagio. Sellada desde poco después de su muerte. Dicen que la ronda su fantasma. Una criada entra una vez al año, a quitar las telarañas.",
        "Un mendigo loco de Soledad, Dervenin, te da un hueso: la pelvis de Pelagio. Y con ella entras en su mente. Un bosque con niebla, arcos de piedra, y una mesa servida. Y ahí, tomando el té con el emperador muerto, está el Príncipe de la Locura.",
        ("Sheogorath", "[playful] ¿Más té, Pelly, querido?"),
        ("Pelagio III", "[nervous] Oh, no podría. Me pasa directo. Además, tengo tantas cosas que hacer. Tantos indeseables. ¡Mi verdugo lleva tres días sin dormir!"),
        ("Sheogorath", "[playful] Bienvenido a la engañosamente verde mente del emperador Pelagio Tercero. Sí, así es. Estás dentro de la cabeza de un monarca muerto y homicidamente demente."),
        "Te da el Wabbajack. Y tienes que curar tres partes de esa mente. La Paranoia, donde Pelagio cree que cualquiera puede matarlo. La Confianza, una figura diminuta aplastada por la Ira. Y los Terrores Nocturnos: Pelagio duerme en una cama, en medio del bosque, y sus pesadillas lo rodean.",
        "Con el Wabbajack conviertes cada pesadilla en algo inofensivo. Un sacerdote dragón, en un cofre. Un atronach de llamas, en una hoguera. Un jefe bandido, en Pelagio de niño.",
        "[short pause] Y la primera pesadilla de Pelagio el Loco. La primera que aparece junto a su cama. [long pause] Es un lobo.",
    ]},
    {"id": "cierre", "pre": 1.5, "frases": [
        "La Reina Loba nunca se sentó en el Trono Rubí. Lo tuvo su hermano, que se rió de ella. Lo tuvo su sobrina, que la echó de un pasillo. Lo tuvo su hijo una sola noche, y lo pagó con fuego. Y lo tuvo el niño al que le colgó una gema al cuello.",
        "Quinientos años después, unos nigromantes intentaron usarla. Y ni muerta se dejó atar.",
        "Ahora te toca a ti. ¿Qué historia quieres que cuente el Profeta la próxima vez? ¿Los Sload, que pidió Exonik? ¿Olaf Ojo Único y el dragón que quizá nunca venció? ¿Los hijos de Gauldur? Déjalo en los comentarios.",
        "Y si te gustó este formato, dilo también. Suscríbete si aún no lo has hecho. [deadpan] Y si encuentras una gema amarilla con un lobo adentro… no te la pongas. Nos vemos en Tamriel.",
    ]},
]

# --- conversión: (personaje, texto) → frase + VOZ_POR_FRASE ---
ESCENAS = []
NARRA = {}   # "escena_i": quién habla (efectos.py pone la placa del personaje en sus frases)
for _e in _ESC:
    _fr = []
    for _i, _f in enumerate(_e["frases"]):
        _k = f"{_e['id']}_{_i}"
        if isinstance(_f, tuple):
            NARRA[_k] = _f[0]
            _fr.append(_f[1])
        else:
            NARRA[_k] = "el Profeta"
            _fr.append(_f)
    ESCENAS.append({**{k: v for k, v in _e.items() if k != "frases"}, "frases": _fr})
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items() if v != "el Profeta"}
