# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — «Las 15 armas más PODEROSAS de Skyrim» (23-oct-2026). Meta: ~15 min (el usuario), 1 sola sesión.
Fórmula de `tes_cosas_inutiles` / `tes_misiones_nunca` (lista de 15, SECUENCIA YT, voz Chatterbox «Sarcastica», MG
`nucleo/mg_tes.py`, pegatinas, mapas con ruta) cambiando UNA variable: el tema pasa a ARMAS (lo que el jugador usa gana en el
canal: objetos más poderosos ×4,2, hechizos más ROTOS ×3,8). Música: OST oficial de Skyrim (regla 23-oct), `armar_musica_ost.py`.
Datos verificados el 23-oct-2026 en UESP (en.uesp.net, wikitexto) y nombres es-ES de elderscrolls.fandom.com/es; ficha por arma
con sus URL en `investigacion.md`. Lo dudoso se dice con cautela (Arco de Auriel = «según su descripción, triple contra no
muertos»; golpes y puñaladas = cálculo propio con la fórmula de UESP, Adepto, sin armadura del dragón).
"""

TITULO = "Las 15 armas más PODEROSAS de Skyrim"
ARCHIVO = "tes_armas_poderosas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# "Skyrim": "Escairim" (el usuario, 23-oct-2026).
FONETICA = {
    "The Elder Scrolls": "Di Élder Escróls", "Elder Scrolls": "Élder Escróls",
    "Skyrim": "Escairim", "Wabbajack": "Uábayak", "Sheogorath": "Shéogoraz", "Katariah": "Katarría",
    "Titus Mede": "Títus Méde", "Sithis": "Sízis", "Zahkriisos": "Sakríisos", "Solstheim": "Sólsteim",
    "Molag Bal": "Mólag Bal", "Boethiah": "Boétia", "Logrolf": "Lógrolf", "Markarth": "Márkarz", "Dawnguard": "Dóngard",
    "Dragonborn": "Drágonborn", "Malacath": "Málacaz", "Largashbur": "Lárgashbur", "Volendrung": "Bolendrung",
    "dwemer": "duémer", "Mephala": "Mefála", "Nelkir": "Nélkir", "Morokei": "Morokéi", "Morthal": "Mórzal",
    "Meridia": "Merídia", "Kilkreath": "Kílcriz", "Malkoran": "Málcoran", "Karliah": "Karlía", "Mercer Frey": "Mércer Fréi",
    "Mercer": "Mércer", "Miraak": "Miráak", "Apocrypha": "Apócrifa", "Hermaeus Mora": "Jermáus Móra", "Esbern": "Ésbern",
    "Delphine": "Délfin", "Auriel": "Áuriel", "Gelebor": "Guélebor", "Vyrthur": "Vírzur", "Serana": "Serána",
    "Riften": "Ríften", "Cidhna": "Sídna", "draugr": "dráugur",
}

# Transcripciones leídas una por una el 23-oct: Whisper escribe distinto los nombres (Catarría, Titus Medes, Uabayac,
# Sangrescal, Solstein, molagbal, Bolendrum, Carlía, Mirak, Delfin, Gélebor, Virzur, «hechizo de Aria»); el resto sale entero
CER_MAX_POR_FRASE = {"p15_1": 0.02, "p14_0": 0.06, "p13_0": 0.035, "p13_1": 0.025, "p13_6": 0.02, "p12_0": 0.045,
                     "p10_0": 0.12, "p10_2": 0.015, "p10_4": 0.085, "p6_1": 0.02, "p5_0": 0.04, "p2_2": 0.02}
# pausa larga entre dos oraciones de la misma frase
GAP_MAX_POR_FRASE = {"p15_7": 0.70, "p12_5": 0.70, "p3_7": 0.66}
# frases de > 8 s que hablan hasta el final (la transcripción acaba bien)
TAIL_MAX_POR_FRASE = {"intro_0": 0.55, "p14_1": 0.47, "p14_6": 0.72, "p12_1": 0.52, "p8_6": 0.50, "p7_1": 0.41, "p6_1": 0.51,
                      "p4_1": 0.38, "p4_4": 0.46, "p3_7": 0.95, "p2_1": 0.43, "p2_2": 0.48}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={"scene-076": 0.09, "scene-080": 0.09, "scene-069": 0.04, "scene-089": 0.04},   # 080: contador GPU/CPU/FPS arriba a la izquierda
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),   # heredados de tes_*
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (armar_musica_ost.py), nunca Lyria

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "El arma más poderosa de Skyrim no te la da ningún príncipe daédrico. No está en ningún altar, ni en ninguna tumba. Y lo más seguro es que la tengas a tu alcance desde hace años.",
        "Skyrim está lleno de armas legendarias. Espadas que paralizan, martillos que te roban las fuerzas, y arcos que hacen llover luz del cielo.",
        "Algunas son poderosas porque así las diseñaron. Y otras, por un error que nadie se molestó en arreglar.",
        "Así que hoy van las quince armas más PODEROSAS de Skyrim, con dónde se consigue cada una y con sus cifras reales.",
        "Y quédate hasta el final, porque el número uno no es lo que esperas.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Viento Cortante.",
        "Es una cimitarra que está clavada en la proa del Katariah, el barco del emperador Titus Mede segundo, frente a la costa de Soledad.",
        "Y solo puedes subir a ese barco durante Salve, Sithis, la misión de la Hermandad Oscura en la que vas a matar al emperador. Si destruyes la Hermandad, no la vas a ver nunca.",
        "Sobre el papel, su encantamiento es modesto. El golpe con la empuñadura, mientras bloqueas, a veces derriba al enemigo. Y solo si llevas la otra mano vacía.",
        "Pero por un error, ese tambaleo se aplica en cada golpe. Normal o potente. Y da igual el tamaño del enemigo.",
        "Así que el enemigo se tambalea, tú vuelves a golpear, se vuelve a tambalear, y ya no te devuelve ni uno.",
        "¿Y cuánto vale esta maravilla? Cuarenta monedas. Menos que muchas armas de hierro encantadas.",
        "Y a veces ni siquiera se queda donde debe. Puede acabar encajada donde no llegas, o en el fondo del mar. El truco es dispararle una flecha para que caiga.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, el Wabbajack.",
        "Es el bastón de Sheogorath, el príncipe de la locura. Lo consigues en La mente de la locura, una misión que empieza en el Palacio Azul de Soledad, y acaba dentro de la cabeza de un emperador muerto.",
        "Cada vez que lo usas pasa algo distinto. Y nunca sabes qué.",
        "Puede lanzar fuego, escarcha o rayos. Puede robarle al enemigo la mitad de su salud, su aguante y su magia, y dártelos a ti. O puede matarlo en el acto.",
        "O puede convertirlo en un pollo. En un cangrejo del barro. En un queso de cabra. O en un bollo dulce. Sí, ese bollo dulce.",
        "Y también puede curarlo, o volverlo invisible. Es una ruleta, y a veces la ruleta juega en tu contra.",
        "Pero tiene un secreto. Su daño elemental, sesenta puntos, no lo reduce nada. Ni la dificultad, ni las resistencias. Un enemigo inmune al frío se come sus sesenta de escarcha igual.",
        "Por eso en Legendario, cuando todas tus armas hacen cosquillas, el bastón del loco sigue pegando lo mismo.",
        "Y cuidado. Un personaje esencial convertido en bollo dulce, si te lo comes, desaparece del juego para siempre.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. La Espada de Sangreskal.",
        "Está en Solstheim, la isla de Dragonborn, al fondo del Túmulo de Sangreskal, en el cadáver de Graciano Cerelio. Y allí abajo te espera un sacerdote dragón, Zahkriisos.",
        "Es un mandoble de veintiuno de daño. Pero lo que importa es lo que hace con cada ataque potente.",
        "Lanza una onda de energía roja, horizontal o vertical según el tajo, que hace treinta de daño a distancia.",
        "Es una espada que dispara. Y nunca necesita recarga. Ni gemas de alma, ni nada.",
        "Y la hicieron a medida para ese jefe. La onda hace daño extra contra Zahkriisos. El arma está diseñada para matar al que la vigila.",
        "Además, hay una segunda Espada de Sangreskal escondida en un hueco detrás del muro de palabras. Solo se saca con un hechizo de área, y casi nadie la ha visto.",
        "Y un truco. Mientras eres etéreo por el grito, puedes atacar al aire y la onda sale igual. Un fantasma que lanza cuchillas.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, la Maza de Molag Bal.",
        "En Markarth hay una casa abandonada que nadie quiere comprar. Y con razón. Dentro te habla una voz. Es Molag Bal, el príncipe de la dominación.",
        "Te manda a buscar a un seguidor de Boethiah, Logrolf, para que lo lleves a su altar y lo mates allí. Sin preguntas.",
        "La recompensa es una maza que en cada golpe le quita veinticinco puntos de aguante y veinticinco de magia al enemigo. Y si muere enseguida, le atrapa el alma.",
        "O sea, al mago lo deja sin hechizos y al guerrero sin ataques potentes. Y encima te llena las gemas de alma.",
        "Y tiene un error precioso. Por una etiqueta mal puesta, su daño al aguante cuenta como daño de fuego.",
        "Así que las ventajas de fuego de Destrucción la potencian. Con Llamas aumentadas, sube de veinticinco a treinta y siete.",
        "El príncipe de la dominación, convertido en pirómano por un error de etiqueta.",
    ]},
    {"id": "p11", "frases": [
        "Número once. El Hacha rúnica de la Guardia del Alba.",
        "Si te unes a la Guardia del Alba, en Dawnguard, el sacerdote del fuerte, Florencio Baenio, te manda a recuperar reliquias perdidas. Una de las recompensas es esta hacha.",
        "Es la única hacha de guerra artefacto de todo el juego. Y sobre el papel, poca cosa. Once de daño.",
        "Pero cada diez no muertos que matas con ella, gana diez puntos de daño solar contra no muertos, en un área alrededor del golpe. Hasta cien.",
        "Cien puntos extra contra draugr, vampiros y esqueletos. Y en área. Un solo golpe limpia una tumba.",
        "Además, rompe al instante cualquier barrera mágica que golpee.",
        "Y el contador debía reiniciarse cada día, pero por un error nunca se reinicia. Los cien muertos son para siempre.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, Volendrung.",
        "Es el martillo de Malacath, el príncipe de los parias. Lo consigues ayudando a los orcos de Largashbur, una fortaleza de la Grieta maldita por culpa de un gigante.",
        "Matas al gigante, recuperas el martillo del jefe, y en el ritual Malacath lo convierte en Volendrung.",
        "Veinticinco de daño, y absorbe cincuenta de aguante por golpe. Tu enemigo se cansa. Tú no.",
        "Pero su verdadero secreto es la velocidad. Todos los martillos de guerra del juego tienen velocidad cero coma seis. Volendrung tiene cero coma siete.",
        "Parece poco, pero en un martillo de ese tamaño es un golpe más por cada seis. Por eso pega más por segundo que casi cualquier arma normal del juego.",
        "Según el lore, lo forjaron los dwemer, y tiene la costumbre de desaparecer y aparecer en otra parte. Igual que los propios dwemer.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. La Hoja de ébano.",
        "En el palacio de Carrera Blanca hay una puerta cerrada que te susurra. Y el que te habla de ella es un niño, Nelkir, el hijo del jarl.",
        "Detrás está la Hoja de ébano, el arma de Mephala, la príncipe de los secretos y las mentiras.",
        "Empieza siendo poca cosa. Absorbe diez puntos de salud. Pero cada vez que matas a dos amigos con ella, sube cuatro.",
        "Y no vale cualquiera. Tienen que ser personas que te aprecian. Seguidores, vecinos, gente a la que le caes bien.",
        "Diez traiciones después, absorbe treinta de salud por golpe. Y con carga infinita. Nunca se gasta.",
        "Por un error, aunque la empuñas con las dos manos, el juego la trata como una espada a una mano, y aprovecha todas sus ventajas.",
        "Eso sí, si te la quitan antes de llegar a diez, por ejemplo en la mina de Cidhna, el contador vuelve a cero.",
        "Es un arma buenísima. A cambio de quedarte sin amigos.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, el Bastón de Magnus.",
        "En el Colegio de Hibernalia te mandan a buscarlo a Laberintia, una ciudad en ruinas cerca de Morthal, llena de draugr, fantasmas y trampas.",
        "Al final te espera el sacerdote dragón Morokei, uno de los jefes más duros del juego.",
        "El bastón lanza un chorro que absorbe veinte puntos de magia por segundo. Y cuando al enemigo ya no le queda magia, empieza a absorberle la salud.",
        "Contra magos y sacerdotes dragón es una pesadilla. Los dejas secos, y su magia pasa a ser tuya. Y su alcance es mucho mayor que el de las Llamas o las Chispas.",
        "Eso sí, en el juego sin parches tiene un error. A veces, la parte de la salud no funciona nunca.",
        "Y otro error más divertido. Si llevas el bastón como única arma, tus puñetazos se aceleran muchísimo. El bastón más poderoso de los magos te convierte en boxeador.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. La Quebrantadora del amanecer.",
        "Es la espada de Meridia, la príncipe que odia a los no muertos. Primero encuentras su baliza, la Luz de Meridia, en un cofre cualquiera, y luego subes con ella al Monte Kilkreath, al oeste de Soledad.",
        "Allí la estatua de Meridia te manda a limpiar su templo de un nigromante, Malkoran, que lo ha llenado de cadáveres.",
        "La espada quema diez puntos con cada golpe.",
        "Pero cuando matas a un no muerto con ella, puede soltar una explosión de luz que hace huir o destruye a los no muertos de alrededor. Los deja en cenizas.",
        "Ni siquiera hace falta que tú des el golpe final. Si el no muerto recibió un tajo en los diez segundos anteriores, puede explotar igual.",
        "Y tiene la mayor carga de todas las armas encantadas que se gastan. Cinco mil. Te pasas una mazmorra entera sin mirar una gema de alma.",
        "Un aviso. Si eres vampiro, la explosión también te quema a ti. Meridia no hace excepciones.",
    ]},
    {"id": "p6", "frases": [
        "En el seis, la Hoja de Ruiseñor.",
        "Te la da Karliah al final de la historia del Gremio de Ladrones, en el sótano de una casa de Hibernalia. Fue de Galo, el maestro del gremio al que asesinó Mercer Frey.",
        "Cada golpe absorbe veinticinco puntos de salud y veinticinco de aguante. Te curas y le quitas las fuerzas al enemigo a la vez.",
        "Pero es un arma que sube contigo. Lo que te dan depende del nivel que tengas al acabar la misión.",
        "La mejor versión sale a partir del nivel cuarenta y seis. Y aquí viene la trampa.",
        "Esa versión, por un error, no se puede mejorar en la forja. Así que la que de verdad conviene es la anterior, la del nivel treinta y seis al cuarenta y cinco.",
        "Que, por otro error, trae veinticinco de aguante en vez de veinte. Un error que tapa otro error. Muy de ladrones.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. La Espada de Miraak.",
        "Es el arma del primer Sangre de Dragón, el villano de Dragonborn. Y solo la consigues de una forma. Matándolo a él, en Apocrypha, el reino de Hermaeus Mora.",
        "Y tiene un récord. A partir del nivel sesenta hace dieciséis de daño base. Lo más alto de todas las espadas a una mano del juego.",
        "Más que la espada daédrica, que hace catorce. Más que la de hueso de dragón, que hace quince.",
        "Y pesa tres. Tres. Menos que una daga.",
        "Cada tajo absorbe quince puntos de aguante, y suelta un tentáculo, como los de los acechadores de Apocrypha.",
        "El tentáculo no hace nada, es pura decoración. Pero si vas a ir por ahí con la espada de un dios de los tentáculos, que se note.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, el Azote de dragones.",
        "La historia principal te lleva con Esbern y Delphine, los últimos Cuchillas, hasta el Templo de Refugio Celestial, escondido tras la Aguja de Karth, al este de Markarth.",
        "En la armería del templo, encima de una mesa, está esta katana. Y mucha gente pasa de largo, porque parece una espada más de los Cuchillas.",
        "En su mejor versión, a partir del nivel cuarenta y seis, hace cuarenta puntos de daño extra a los dragones. Y a todo lo demás, diez de descarga eléctrica.",
        "Y otra vez, ojo con el nivel. Si la coges entre el veintisiete y el treinta y cinco, la descripción te promete treinta contra dragones, y en realidad hace veinte.",
        "Hice las cuentas. Con todo al máximo, para tumbar a un dragón ancestral de fuego necesitas unos treinta y ocho golpes. Los mismos que con el arma número tres de esta lista.",
        "Pero contra un dragón de escarcha, el Azote necesita catorce golpes menos. Contra el bicho para el que la forjaron, no hay espada mejor.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. La Desgarradora gélida.",
        "Es la espada de cristal de Mercer Frey, el traidor del Gremio de Ladrones. La guarda en una vitrina con cerradura experta, en los túneles de su casa de Riften, la Hacienda Bosque de la Grieta.",
        "En su mejor versión, cada golpe hace treinta puntos de daño por escarcha, además de los quince del filo.",
        "Y puede paralizar al enemigo dos segundos. No siempre. Más o menos un golpe de cada cuatro.",
        "Un enemigo paralizado no se defiende. No bloquea. No lanza hechizos. Solo espera.",
        "Según la wiki más completa de la saga, es el arma a una mano más devastadora que puedes conseguir tal cual, sin mejorarla.",
        "Y si tienes las ventajas de escarcha de Destrucción, el frío sube hasta cuarenta y cinco.",
        "Y el detalle que más me gusta. No hace falta ser ladrón para tenerla. Si saltas desde el templo de Mara al tejado, te cuelas en la casa de Mercer y se la robas sin haber pisado el gremio. Robarle al ladrón.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. El Arco de Auriel.",
        "Es el arco del dios elfo del sol, y está en el Valle Olvidado, un valle helado al que solo se llega bajando por la Cueva de Sima Negra, en la Cuenca, cerca de Markarth.",
        "Lo custodia Gelebor, el último caballero paladín de los elfos de la nieve. Y para conseguirlo tienes que matar a Vyrthur, el archicoadjutor, que también es un vampiro.",
        "Sus flechas queman con luz solar. Según su descripción, hacen el triple contra los no muertos.",
        "Y dispara rápido. El arco daédrico tarda el doble en tensarse.",
        "Pero el truco está en las flechas élficas bendecidas por el sol. Si disparas una al sol, el sol te contesta.",
        "Durante diez segundos caen rayos de luz sobre los enemigos que tienes cerca. Le disparas al cielo, y el cielo dispara por ti.",
        "Y con las flechas malditas con sangre, las que hace Serana, tapas el sol hasta la mañana siguiente. Justo lo que quería el villano de Dawnguard.",
        "Por eso es el número dos. Es la única arma de Skyrim con la que puedes apagar el sol.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. El arma más poderosa de Skyrim.",
        "No está en ningún altar daédrico. No te la da ningún dios. No la custodia ningún dragón.",
        "La forjas tú. Con los huesos de los dragones que has matado. Es una daga de hueso de dragón.",
        "Necesitas Herrería al cien, la ventaja Armadura de dragón, un hueso de dragón y unas tiras de cuero. Y tener Dawnguard.",
        "Sola, parece poca cosa. Doce de daño base. Es la más débil de toda la familia de hueso de dragón.",
        "Pero una daga tiene algo que no tiene ninguna otra arma. Con la ventaja Hoja del asesino, de Discreción, los ataques furtivos con daga hacen quince veces más daño.",
        "Y si te pones los Guantes etéreos de la Hermandad Oscura, ese multiplicador se duplica. Treinta veces.",
        "Forjada a legendaria y con las ventajas de A una mano, una sola puñalada por la espalda hace mil novecientos ochenta puntos de daño.",
        "La Desgarradora gélida, en la misma puñalada, se queda en novecientos. Porque con espada el sigilo multiplica por doce, no por treinta.",
        "Y un dragón anciano tiene unos dos mil doscientos de salud. Una sola puñalada lo deja con un hilo de vida.",
        "Y si además la mejoras con el bucle de alquimia del video de los exploits, llegas a siete mil seiscientos cincuenta. Más que la vida entera de un dragón legendario.",
        "Por eso es la número uno. Todas las demás armas de esta lista te las dio alguien. Esta te la ganaste tú, dragón a dragón.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Quince armas de Skyrim, de una cimitarra rota por un error a una daga que forjas con los huesos de tus enemigos.",
        "Si tu arma favorita no está, déjala en los comentarios y dime por qué. Y si es la Hoja de ébano, dime también cuántos amigos te costó.",
        "Y si quieres ver justo lo contrario, en el canal tienes las quince cosas más INÚTILES de Skyrim, con dos armas que no deberías tocar nunca.",
        "Y la próxima vez que pases por la armería del Refugio Celestial, mira bien encima de la mesa.",
    ]},
]
