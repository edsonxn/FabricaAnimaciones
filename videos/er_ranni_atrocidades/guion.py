# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Ranni QUE IGNORASTE» (21-oct-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md (repite «Las 5 … QUE IGNORASTE» de
Márika ×24,6, Radagon y Miquella cambiando el sujeto → Ranni; el usuario pidió ~12 min, a medio camino entre los 6-7 de
Márika/Radagon y los 20 de Miquella).
No repite lo de Miquella (Radahn/Mohg/encanto) ni lo de Radagon y Márika (Rennala abandonada, el matrimonio).
Datos verificados el 21-oct-2026 en eldenring.wiki.fextralife.com (Ranni the Witch: diálogos de la confesión, el cuerpo, los Dos
Dedos, Blaidd e Iji, final; Black Knife; Black Knife Tiche; Alecto, Black Knife Ringleader + Black Knife Armor; Godwyn the
Golden; Deathroot; Maliketh's Black Blade; Blaidd: diálogos y Royal Greatsword / Blaidd's Gauntlets; War Counselor Iji:
diálogos y su muerte; Preceptor Seluvis; Fingerslayer Blade; Endings: Age of the Stars) y eldenring.wiki.gg (Seluvis: brebaje
ámbar, muerte con la Hoja matadedos, Pidia, la tienda de marionetas en su cadáver).
"""

TITULO = "Las 5 peores atrocidades de Ranni QUE IGNORASTE"
ARCHIVO = "er_ranni_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube
FONETICA = {
    "Ranni": "Ráni", "Blaidd": "Bláid", "Iji": "Íyi", "Seluvis": "Selúvis", "Nepheli": "Néfeli", "Godwyn": "Gódüin",
    "Rennala": "Renála", "Alecto": "Alécto", "Maliketh": "Málikez", "Gurranq": "Gúrank", "Darriwil": "Dárriuil",
    "Radagon": "Rádagon", "Radahn": "Rádan", "Rykard": "Ráikard", "Mohg": "Mog", "Miquella": "Mikuéla", "Liurnia": "Liúrnia",
    "Fortissax": "Fortísax", "Elden Ring": "Élden Ring", "Elden": "Élden", "Tiche": "Tíche",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={"scene-064": 0.06,    # icono de canal en la esquina superior derecha
                 **{f"scene-{n:03d}": 0.09 for n in (22, 31, 32, 33, 34, 37, 46, 58, 82)}},   # firma «SHIRRAKO» abajo a la derecha
    yt=dict(sufijo="Elden Ring", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls"]),   # heredado de Miquella
)

# Revisado el 21-oct tras la 1.ª ronda (eval.json): 31 de 33 eran falsas alarmas — Whisper escribe «Selubis» por Seluvis,
# «Blythe/Blyde/Blight» por Blaidd, «E.G./Eiji/Iggy/Ishi» por Iji, «Malik» por Maliketh, «Rani» por Ranni, y las frases largas
# hablan hasta el final (cola) o llevan pausa tras punto. Errores reales regenerados: intro_1 (se comía «Media comunidad»)
# e intro_2 («rito» → «grito»; ahora «ritual»).
CER_MAX_POR_FRASE = {'intro_4': 0.001, 'p5_1': 0.014, 'p5_2': 0.023, 'p5_4': 0.009, 'p5_5': 0.021, 'p5_11': 0.001, 'p5_13': 0.016,
                     'p4_0': 0.14, 'p4_1': 0.031, 'p4_2': 0.051, 'p4_3': 0.045, 'p4_4': 0.022, 'p4_7': 0.063, 'p4_8': 0.034,
                     'p4_11': 0.053, 'p3_1': 0.013, 'p3_9': 0.08, 'p3_10': 0.031, 'p3_11': 0.025, 'p3_13': 0.034, 'p2_1': 0.016,
                     'p2_4': 0.014, 'p2_10': 0.014, 'p2_12': 0.006, 'p1_1': 0.001, 'p1_11': 0.04}
GAP_MAX_POR_FRASE = {'intro_0': 0.71, 'intro_2': 0.7, 'p4_3': 0.69, 'p5_4': 0.77, 'p5_11': 0.84, 'p5_13': 0.63, 'p4_6': 0.75, 'p4_7': 0.62, 'p4_8': 0.85,
                     'p4_11': 0.93, 'p2_1': 0.56, 'p2_12': 0.67, 'p1_1': 0.74, 'p1_15': 0.74, 'cierre_0': 0.79, 'cierre_2': 0.61}
TAIL_MAX_POR_FRASE = {'intro_0': 0.55, 'intro_2': 0.73, 'intro_4': 0.58, 'p5_1': 0.68, 'p5_4': 0.51, 'p4_1': 0.66, 'p4_2': 0.61, 'p4_4': 0.48,
                      'p4_6': 0.40, 'p4_7': 0.6, 'p4_8': 0.48, 'p4_11': 0.68, 'p3_10': 0.56, 'p3_11': 0.38, 'p3_13': 0.51,
                      'p2_1': 0.34, 'p2_10': 0.43, 'p2_12': 0.64, 'p1_1': 0.83, 'p1_11': 0.51, 'p1_15': 0.55, 'cierre_0': 0.72,
                      'cierre_2': 0.55}

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Dark gothic fantasy orchestral underscore like a melancholic soulslike action RPG soundtrack: cold moonlit strings, "
           "glass harmonica, low choir, harp and distant bells, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("a beloved witch under a cold blue moon, delicate harp and celesta, charm with a hidden chill underneath", 6),
        "p5": ("a puppet maker's tower, creaking music box, plucked strings like marionette strings, sly and macabre", 5),
        "p4": ("a loyal wolf companion, warm horns that slowly turn tragic, a lonely howl-like cello, sorrow and madness", 5),
        "p3": ("assassins in the night, muted low drums, hushed choir, a blacksmith's anvil fading into silence, grief", 6),
        "p2": ("a golden prince dies only in soul, solemn requiem choir, dark organ, roots spreading in the dark, dread", 7),
        "p1": ("an eternal voyage into a frozen starry night, vast cold strings and choir, beautiful and terrifying, a wedding in the dark", 8),
        "cierre": ("calm after the storm, soft moonlit harp, a wry final note fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro"], "Begin softly from near silence with a delicate harp. End on a sustained cold string tone."),
        (["p5"], "Begin on a cold string tone. End on a held, slightly unsettling music box chord."),
        (["p4"], "Begin on a soft music box chord. End on a mournful sustained low cello note."),
        (["p3"], "Begin on a low cello note. End on a quiet hollow drum and a held low choir tone."),
        (["p2"], "Begin on a low choir tone. End on a heavy, unresolved low organ drone."),
        (["p1"], "Begin on a low drone. Swell to a vast cold peak, then settle on a sustained high string."),
        (["cierre"], "Begin on a calm high string. Settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Si hay un personaje de Elden Ring al que todo el mundo adora, es la bruja Ranni. Cuatro brazos, un sombrero puntiagudo, ese ojo azul debajo del ala, y una forma de hablar sacada de un libro de caballerías.",
        "La mitad de la comunidad hizo su misión solo para volver a verla, y la otra mitad la hizo para casarse con ella. Yo hice las dos cosas, para qué te voy a mentir.",
        "Pero hay un detalle en el que casi nadie se para a pensar. Ella misma lo confiesa, con su voz tranquila, en su torre: robé un fragmento de la Runa de la Muerte, y con un ritual terrible forjé los cuchillos negros que matan dioses.",
        "Y luego lo remata con tres palabras: todo lo hice yo.",
        "Así que hoy van las cinco peores atrocidades de Ranni que ignoraste, porque la bruja más querida del juego dejó detrás de ella un rastro de cadáveres que da para llenar un cementerio entero.",
        "Y te aviso desde ya: el número uno no le pasó a un semidiós. Te pasó a ti.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El preceptor de las marionetas.",
        "Cuando entras al servicio de la bruja, en su torre de Liurnia, ella misma te presenta a su gente: allí encontrarás a Iji, mi consejero de guerra, y a Seluvis, preceptor en las artes de la hechicería.",
        "Seluvis es ese mago con cara de pocos amigos que te recibe con un desprecio que no se molesta en esconder: no sé qué es lo que la señora ve en un Sinluz de provincias como tú.",
        "Y enseguida te pide un favor. Que busques a una guerrera llamada Nepheli, y le des a beber una poción.",
        "Esa poción convierte a la gente en marionetas. Y Seluvis las colecciona. Si le compras alguna, te dice con cariño que cada una de ellas es como un hijo para él.",
        "Debajo de un suelo falso de su torre tiene un cuarto secreto, y en el suelo te espera un mensaje: marioneta de Seluvis. No tocar.",
        "Y todo eso la bruja lo sabe. Lo tiene en nómina. El hombre que convierte personas en muñecos es su profesor de magia de confianza.",
        "Pero Seluvis tiene un plan más grande. Te da un brebaje ámbar, y te dice: dáselo a la señora y asegúrate de que se lo beba. Cuando lo haga, mi plan dará fruto.",
        "Quería convertir a su propia señora en una marioneta más de su colección.",
        "Si le llevas el brebaje, ella se da cuenta enseguida, y te pide que te vayas. Y si no te vas, te mata ahí mismo.",
        "Y si no se lo llevas, y sigues con su misión, en cuanto le entregas la Hoja matadedos, Seluvis aparece muerto en su torre. Y con él muere también Pidia, su ayudante.",
        "Y lo más macabro es que su cadáver sigue ahí, y si le hablas, todavía te vende marionetas. El titiritero acabó de mostrador.",
        "Él quería una muñeca obediente, y ella, que vive dentro de un cuerpo de muñeca, le enseñó quién mueve los hilos de verdad.",
        "Y eso que Seluvis era un traidor. Lo que viene ahora le pasó a los que le fueron leales.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Blaidd, el medio lobo.",
        "Si jugaste esta misión, Blaidd fue tu mejor amigo de todo el juego. El lobo grandote que te ayuda contra Darriwil, que te espera en el festival de Radahn, y que te dice que su único propósito es luchar por el destino de su señora, con espada y colmillo.",
        "Pero Blaidd no llegó a su lado por casualidad. El consejero Iji te lo cuenta con mucha pena: los Dos Dedos le dieron a Blaidd a la señora como un seguidor fiel. Su propia sombra, incapaz de traicionarla.",
        "O sea, Blaidd era un regalo de los Dedos. Una correa con forma de lobo, para que la Empírea no se saliera del camino.",
        "Y el viejo Iji sigue: pero si la señora, como Empírea, se resiste a ser un instrumento de los Dos Dedos, la sombra enloquecerá, y pasará de ser un seguidor a ser una horrible maldición.",
        "Ahora acuérdate de lo que hizo ella. Se rebeló contra los Dos Dedos. Y lo dice sin pestañear: no me dejaría controlar por esa cosa.",
        "Es difícil creer que la bruja que planeó la noche más famosa del juego no supiera cómo funcionaba su propia sombra. Y aun así siguió adelante.",
        "Así que, a mitad de la misión, Blaidd desaparece. Lo encuentras encerrado en una celda, y te dice: el viejo Iji me encerró aquí. Soy parte de su ser. Su propia sombra.",
        "Y al final, Blaidd se escapa. Lo encuentras delante de la torre, gruñendo, hablando solo: no, soy parte de su ser, nunca podría traicionarla, pase lo que pase.",
        "Y te ataca. Y tienes que matarlo tú. Al amigo que te acompañó media partida.",
        "Su guantelete lo describe como el aliado leal que desafiaría al destino mismo, si el destino le ordenaba volverse contra su señora.",
        "Y lo desafió. Se volvió loco antes que traicionarla. Iji lo resume con una frase que duele: Blaidd se convirtió en una maldición que atormentaba a la señora, pero en su locura, se entregó a ella.",
        "La libertad se la quedó la bruja. La factura la pagó el lobo.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Las que pusieron las manos.",
        "La bruja no mató a Godwyn con sus propias manos. Para eso tuvo a las asesinas de los Cuchillos Negros.",
        "Su armadura cuenta que todas eran mujeres, y que se rumoreaba que eran numen con lazos muy estrechos con la mismísima Márika.",
        "Sí, con Márika. En esta familia hasta los asesinatos son un negocio familiar.",
        "Una de ellas se llamaba Tiche. Sus cenizas cuentan que, en la noche de la conspiración, impregnó su cuchillo con la Runa de la Muerte y mató a Godwyn el Dorado.",
        "Tiche era hija de la cabecilla, Alecto. Y murió protegiendo a su madre mientras huían de la capital.",
        "La madre sobrevivió, y acabó encerrada en una prisión eterna a la que solo puedes entrar si avanzas bastante en la misión de la bruja.",
        "O sea, para conocer a la mujer que le hizo el trabajo sucio, primero tienes que hacerle tú el trabajo sucio.",
        "Y cuando entras, Alecto te ataca, y la matas. Tu recompensa son las cenizas de su hija.",
        "Y luego está Iji, el gigante herrero que encerró a Blaidd llorando por dentro.",
        "Iji se despide de ti con una calma rarísima: mi propósito está llegando a su fin. Te alcanzaré pronto, Blaidd, y cuando lo haga, solo espero que aceptes mis disculpas.",
        "Y si vuelves a su yunque después de matar a Blaidd, lo encuentras muerto, cubierto de llamas negras. Y a su alrededor, tres asesinas de los Cuchillos Negros.",
        "El juego no te dice quién las mandó. Pero el viejo que guardaba los secretos de la bruja terminó callado para siempre, rodeado de las mismas asesinas de aquella noche.",
        "Y lo que más duele es que ella, en una conversación escondida, deja escapar: Blaidd e Iji, los dos, están dispuestos a darme demasiado. Diles que los quiero.",
        "Y lo dice en serio. Los quería. Y aun así, de los que la quisieron, no queda ninguno en pie.",
    ]},
    {"id": "p2", "frases": [
        "Ya en el podio, el número dos. La noche que lo cambió todo.",
        "Godwyn el Dorado era el primogénito de Márika, el semidiós más querido de su tiempo. Tan bondadoso que acabó haciéndose amigo del dragón contra el que peleó, Fortissax.",
        "Y en la Noche de los Cuchillos Negros, se convirtió en el primer semidiós en morir.",
        "Pero no murió del todo. Y ahí está la atrocidad, porque fue un crimen con dos víctimas a la vez.",
        "Ella misma lo cuenta así: robé la Runa de la Muerte, maté mi propia carne de Empírea, y la deseché.",
        "Esa misma noche, ella sacrificó su cuerpo y se quedó con el alma. A Godwyn le arrancaron el alma, y le dejaron el cuerpo.",
        "Un cuerpo vivo y vacío, enterrado en lo más hondo, bajo el Árbol Áureo.",
        "Y ese cadáver que no termina de morir empezó a echar raíces. De ahí brota la raíz de la muerte, que según su descripción es el origen de los que viven en la muerte.",
        "Los no muertos de las catacumbas, los que adoran a Godwyn como el Príncipe de la Muerte, todo eso sale de ese cuerpo.",
        "Y para que la muerte se pudiera robar, alguien tuvo que fallar al guardarla. Maliketh, la Espada Negra, el guardián de la Runa de la Muerte.",
        "Su espada lo cuenta: después de que robaran un fragmento de la Muerte aquella noche fatídica, Maliketh selló la hoja dentro de su propia carne, para que nadie volviera a robar la Muerte nunca más.",
        "Y aun así, el pobre terminó como Gurranq, el clérigo bestia, encerrado en una iglesia, pidiéndote raíces de la muerte para devorarlas.",
        "Y después vino lo peor. Tras la muerte de Godwyn, Márika hizo pedazos el Anillo de Elden. Los semidioses se quedaron cada uno con un trozo, y empezó la Fragmentación, la guerra que dejó las Tierras Intermedias como las recorres tú.",
        "No digo que la bruja rompiera el Anillo. Ese martillazo es de Márika. Pero la primera ficha del dominó la empujó ella.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. El que te pasa a ti.",
        "Al final de su misión, la bruja te pregunta, con esa voz que derrite a medio internet: vendrías a mí, incluso ahora, mi único señor?",
        "Y tú le pones el anillo de la Luna Oscura en el dedo, y le dices que sí. Media comunidad lloró con esa escena. Yo también.",
        "Pero escucha lo que promete el día de la boda.",
        "Delante de los restos de Márika, ella ocupa su lugar como diosa, acaba con la Orden Áurea, y arranca de las Tierras Intermedias la influencia del Árbol Áureo.",
        "Y anuncia: ahora llega la era de las estrellas. Un viaje de mil años bajo la sabiduría de la Luna. Aquí comienza la noche helada que lo abarca todo.",
        "Y describe ese viaje como un camino hacia el miedo, la duda y la soledad.",
        "Y luego se va. Con su orden nuevo, y contigo de consorte, en un viaje de mil años. Y deja las Tierras Intermedias sin señor, por primera vez en toda una era.",
        "Piénsalo. Todos los que sobrevivieron a la Fragmentación y a la putrefacción se quedan en un mundo frío, oscuro, y sin nadie al mando. Durante mil años.",
        "La gente lo llama el final bueno. Y lo es, para dos personas. Para ella, y para el que se va con ella.",
        "Y ese eres tú. Porque la última atrocidad de la bruja no es contra un semidiós. Es contra ti.",
        "Todos los que la quisieron, Blaidd, Iji, y hasta Seluvis a su manera, acabaron muertos por el camino. Y el último que queda en pie, el que se la lleva al final, es el Sinluz que le hizo todos los recados.",
        "Mi bello consorte, eterno, te dice. Eterno. En este juego no hay final de divorcio.",
        "Y si escuchaste las conversaciones escondidas de su muñequita, la última frase cambia por una más tierna: vayamos juntos.",
        "Vayamos juntos. A la oscuridad. Durante mil años.",
        "Y lo más fuerte es que mucha gente, sabiendo todo esto, la volvería a elegir. Yo incluido. Esa es su atrocidad más grande: que la quieres igual.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. La bruja más querida de Elden Ring dejó un preceptor muerto, un lobo loco, un herrero en llamas, una madre sin hija, un dios sin alma, y un mundo entero a oscuras durante mil años.",
        "Ahora te pregunto, y quiero leerlo en los comentarios: sabiendo todo esto, te volverías a casar con Ranni?",
        "Y si quieres conocer al resto de la familia, en el canal tienes las atrocidades de Márika, las de Radagon, que es su padre, y las de Miquella, su medio hermano. Ninguno sale bien parado.",
        "Y la próxima vez que una muñeca con sombrero te pida un favor, pregúntale primero qué le pasó al último que se lo hizo.",
    ]},
]
