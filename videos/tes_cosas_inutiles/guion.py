# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — «Las 15 cosas más INÚTILES de Skyrim» (23-oct-2026). Meta: ~15 min (el usuario), 1 sola sesión.
Fórmula de `tes_misiones_nunca` (lista de 15, SECUENCIA YT, voz Chatterbox «Sarcastica», MG `nucleo/mg_tes.py`, pegatinas,
mapas con ruta) cambiando UNA variable: el tema pasa de «lo que no debes hacer» a «lo que no sirve». Ref. de fuera: Choa
«60 Useless Skyrim Facts» ×85,9; lo propio: exploits más ROTOS 6 034 en 5 días (el eje «lo que el jugador usa» gana).
Datos verificados el 23-oct-2026 en UESP (en.uesp.net, wikitexto por la API) y nombres en es-ES de elderscrolls.fandom.com/es:
Nazeem (Granja de Escalofrío llevada por Wilmuth, «Do you get to the Cloud District very often?», dice asesorar al jarl y nunca
pisa el palacio, duerme 8 pm-8 am en El Cazador Ebrio, 4 h en el mercado, a las 4 pm otra vez a la posada) · Hod (leña a 5
monedas; la leña vale 1) · Hogar de la Brisa 5 000 · Piedra de la Torre (entre Lucero del Alba e Hibernalia, cerradura experta o
menor una vez al día, no cuenta en estadísticas ni para el logro, cofres de la cárcel con cerradura experta) · Llave de cera
(Abrir cerraduras 50) e Irrompible (100) · Clarividencia (Ilusión novato, 25 de magia/s, la vende la tienda de Cauce Boscoso)
· bollo dulce (5 de salud; 160 en 83 sitios; 5 ingredientes con Hearthfire; «Let me guess... someone stole your sweetroll»;
poción de curación menor 25) · Telequinesia (Alteración adepto, 170/s, sin libro fijo en el juego base, Tolfdir, 25 % en una
ruina, daño que no sirve en combate, sale disparado con sonido de Fuerza implacable) · Reflejos rápidos (Bloquear 30; error de la
cámara lenta que no acaba y se rompe bloqueando otro ataque de poder) · caballos (pelean solos, combate montado desde el parche
1.6 sin magia, suben pendientes, la caída mata al caballo, cuentan como testigo, Shadowmere solo con la Hermandad) · Voz del
Emperador (calma a personas 60 s, 1/día, sin ventajas de Ilusión), Dominar animal (60 s, 1/día), suerte imperial (2-10 monedas)
· Cuchilla de Mehrunes (Silo Vesuio, museo del Amanecer Mítico en Lucero del Alba, 4 piezas, matarlo, 2/101 = 1,98 % en vez del
1 % del script, sin ventajas de Herrería, daño 11 = daga daédrica con la mitad de peso, Miraak y Karstaag inmunes) · Hacha del
arrepentimiento (Barbas cerca de Falkreath, invulnerable salvo por el hacha, máscara o hacha, 22 de daño, 20 de aguante, velocidad
0,5 = el arma cuerpo a cuerpo más lenta, sin ventajas de Herrería, no cuenta para el logro) · licantropía (150 s 1/día, +30 s
por cadáver, sin equipo/hechizos/gritos/poderes, sin recoger/cofres/cerraduras/hablar/mapa, no se deshace a voluntad, en la versión
original se reequipa a mano, árbol de ventajas solo con Dawnguard) · Proyectar voz (Punta Mellada, dragón + Krosis, una de dos con
todas sus paredes guardadas por sacerdote dragón, un alma por palabra, tres niveles iguales salvo la espera, insultos «slug-breath,
melon-nose, cheese brain, ugly», vuelve hostil a gigantes y mamuts) · Pergamino antiguo (ciego o loco, uno en el juego base, pesa
20 pero 0 como objeto de misión, valor 0, La perdición de Alduin, Urag gro-Shub 2 000, con Dawnguard se recompra a 4 000).
"""

TITULO = "Las 15 cosas más INÚTILES de Skyrim"
ARCHIVO = "tes_cosas_inutiles"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# "Skyrim": "Escairim" (el usuario, 23-oct-2026: «Eskaai rim» sonaba mal).
FONETICA = {
    "The Elder Scrolls": "Di Élder Escróls", "Elder Scrolls": "Élder Escróls", "Elder Scroll": "Élder Escról",
    "Skyrim": "Escairim", "Nazeem": "Nasím", "Wilmuth": "Uílmuz", "Hod": "Jod", "Hearthfire": "Járzfaier",
    "Tolfdir": "Tólfdir", "draugr": "dráugur", "Shadowmere": "Shádoumir", "bosmer": "bósmer",
    "Mehrunes Dagon": "Merúnes Dágon", "Mehrunes": "Merúnes", "Dagon": "Dágon", "Miraak": "Miráak", "Karstaag": "Kárstag",
    "Dragonborn": "Drágonborn", "Falkreath": "Fálkriz", "Clavicus": "Clávicus", "Dawnguard": "Dóngard",
    "Krosis": "Krósis", "Alduin": "Álduin", "Urag gro-Shub": "Úrag gro Shub",
}

# Transcripciones leídas una por una el 23-oct: Whisper escribe distinto los nombres (Nassim, Harlem/harla = jarl, «J» = Hod,
# Hartsfire, Tolvdir, Skyrvin, Besuyo, Karstak, Crocis, Urak Grosub, Dungar); el resto de la frase sale entero
CER_MAX_POR_FRASE = {"intro_1": 0.01, "p15_0": 0.06, "p15_2": 0.04, "p15_3": 0.05, "p14_5": 0.025, "p10_5": 0.025,
                     "p9_4": 0.02, "p6_1": 0.015, "p6_7": 0.015, "p5_1": 0.025, "p5_2": 0.01, "p5_7": 0.04, "p2_2": 0.03,
                     "p1_6": 0.02, "p1_7": 0.035}
# pausa larga entre dos oraciones de la misma frase
GAP_MAX_POR_FRASE = {"intro_1": 0.70, "p10_6": 0.90, "p6_4": 0.82, "p1_7": 0.75}
# frases de > 8 s que hablan hasta el final (CER ~0 y la transcripción acaba bien)
TAIL_MAX_POR_FRASE = {"intro_1": 0.44, "p15_5": 0.39, "p12_1": 0.71, "p12_4": 0.58, "p9_1": 0.61, "p9_4": 0.48, "p8_5": 0.60,
                      "p7_4": 0.45, "p6_1": 0.57, "p6_7": 0.37, "p5_1": 0.51, "p5_2": 0.41, "p4_1": 0.48, "p1_8": 0.38}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={"scene-008": 0.07, "scene-015": 0.05, "scene-023": 0.07},   # 015: marca «BANDICAM» arriba   # 23-oct: rótulos chicos arriba («JK's Dragonsreach», «The Thief Stone»)
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp"]),   # heredados de tes_*
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Nordic fantasy orchestral underscore like a classic open-world RPG soundtrack: low male choir, "
           "frame drums, cello and viola, distant horns, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("wry and mischievous, plucked strings and a sly bassoon, a comedy of disappointments", 5),
        "p15": ("pompous market town, prim harpsichord-like plucks and smug woodwinds", 3),
        "p14": ("rustic lumber mill by a river, steady wooden percussion, folk fiddle, honest toil", 3),
        "p13": ("windy snowy cliff with an ancient stone, cold airy pads, a lonely horn", 4),
        "p12": ("sneaky thief in a quiet house, light pizzicato and soft ticking", 3),
        "p11": ("mystic illusion spell, shimmering chimes and soft female choir", 3),
        "p10": ("warm cozy tavern bakery, playful flute and lute, light comedy", 3),
        "p9": ("arcane mage college, floating celesta and strings, a failed marvel", 4),
        "p8": ("slow-motion duel, stretched low strings and a heavy slow drum", 3),
        "p7": ("galloping plains, bouncy strings, comic trotting rhythm", 4),
        "p6": ("imperial court fanfare that deflates, small brass, ironic", 3),
        "p5": ("dark cult museum, ominous low choir, creeping cellos", 5),
        "p4": ("loyal dog and a cruel bargain, gentle strings that turn bitter", 5),
        "p3": ("savage beast transformation, tribal drums and growling brass", 5),
        "p2": ("mighty dragon shout reduced to a joke, big choir then a deflating tuba-like note", 4),
        "p1": ("ancient sacred scroll on a mountain summit, vast choir and deep drums, then irony", 7),
        "cierre": ("calm and wry, warm low strings, a final playful pluck fading out", 3),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro", "p15"], "Begin softly from near silence with sly plucked strings. End on a sustained low string tone."),
        (["p14", "p13"], "Begin on a sustained low string tone. End on a cold held note."),
        (["p12", "p11"], "Begin on a cold held note. End on a soft shimmering chord."),
        (["p10", "p9"], "Begin on a soft shimmering chord. End on a quiet suspended note."),
        (["p8", "p7"], "Begin on a quiet suspended note. End on a light held chord."),
        (["p6", "p5"], "Begin on a light held chord. End on a dark held drone."),
        (["p4"], "Begin on a dark held drone. Stay tender and then bitter. End on a low held note."),
        (["p3", "p2"], "Begin on a low held note. Build to a savage peak, then a grand choir. End on a deep held tone."),
        (["p1", "cierre"], "Begin on a deep held tone. Climb to a vast peak, then settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Hay un objeto en Skyrim que le da nombre a toda la saga. Y cuando por fin lo tienes en la mochila, lo más útil que puedes hacer con él es venderlo.",
        "Y no es el único. Skyrim lleva casi quince años con nosotros, y tiene una colección impresionante de cosas que no sirven absolutamente para nada.",
        "Hechizos que gastan tu magia para hacer lo que ya hace la brújula. Ventajas que te dan la llave de una puerta que acabas de abrir. Y un grito que te cuesta tres almas de dragón para insultar a un bandido.",
        "Así que hoy van las quince cosas más INÚTILES de Skyrim, de las que solo dan risa a las que te hacen sentir estafado.",
        "Y todo lo que vas a ver está en el juego, con sus cifras reales. No me lo invento. Ojalá me lo inventara.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Nazeem.",
        "Si has pasado por el mercado de Carrera Blanca, ya lo conoces. Es el señor que te pregunta si vas mucho al Distrito de la Nube, y antes de que contestes, se responde él solo. Pues claro que no.",
        "Nazeem presume de que aconseja al jarl en asuntos políticos, y de que su opinión es muy valiosa.",
        "Pero nunca pisa el palacio. Y ni el jarl ni nadie de su corte lo menciona jamás.",
        "Dice que llegó a lo más alto gracias a su granja, la Granja de Escalofrío. Y la granja la trabaja otro, un empleado suyo llamado Wilmuth.",
        "¿Y él qué hace todo el día? Duerme doce horas en la posada, El Cazador Ebrio. Se levanta, pasa cuatro horas en el mercado criticando los puestos, pasea un rato, y a las cuatro de la tarde vuelve a la posada a descansar.",
        "Es el único personaje de Skyrim con una agenda más relajada que la de un guardia con una flecha en la rodilla.",
        "Está en el último puesto porque, al menos, nos regaló el mejor meme del juego. Y porque con él puedes hacer algo que con el resto de esta lista no puedes. Ignorarlo.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, cortar leña.",
        "En Cauce Boscoso, el primer pueblo al que llegas, el leñador Hod te deja usar su tajo y te compra cada pieza de leña por cinco monedas.",
        "El juego te lo presenta como un trabajo honrado. Coges el hacha, partes un tronco, y te quedas mirando cómo tu personaje da hachazos.",
        "La casa más barata de Carrera Blanca, el Hogar de la Brisa, cuesta cinco mil monedas.",
        "O sea, mil piezas de leña. Mil veces la misma animación, para tener un techo.",
        "Y si esa leña se la vendes a cualquier otro mercader, cada pieza vale una moneda. Hod te paga cinco, probablemente por lástima.",
        "Eres el Sangre de Dragón, el héroe de la profecía, y si quieres casa sin matar a nadie, te toca ahorrar partiendo troncos.",
        "Es inútil, sí. Pero es la única forma de ganar dinero sin robar ni matar en todo Skyrim, y eso dice mucho de Skyrim.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. La Piedra de la Torre.",
        "Skyrim tiene trece piedras guardianas, y cada una te da una bendición. El Guerrero, el Mago, el Ladrón, el Amante... y luego está esta.",
        "Está a medio camino entre Lucero del Alba e Hibernalia, en lo alto de un acantilado nevado, y para llegar tienes que subir la montaña a pulso.",
        "Su poder es abrir sola, una vez al día, una cerradura de nivel experto o menor.",
        "Una vez al día, y solo hasta experto. Las de nivel maestro, que son las únicas que de verdad cuestan, esas no las abre.",
        "Mientras tanto, cualquier ganzúa, que te encuentras por todas partes, hace lo mismo cuantas veces quieras.",
        "Y encima, las cerraduras que abre la piedra no cuentan en tus estadísticas. Ni siquiera cuentan para el logro de ladrón.",
        "Su único uso de verdad es escapar de la cárcel, porque los cofres de la prisión tienen cerradura experta. O sea, que es una piedra para gente a la que arrestan todos los días.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, la Llave de cera.",
        "Es una ventaja de Abrir cerraduras, de nivel cincuenta, y suena de maravilla. Cada vez que fuerzas una cerradura, te llevas una copia de su llave.",
        "Piénsalo un segundo. Te dan la llave de una puerta que acabas de abrir.",
        "Es como si te regalaran un paraguas justo cuando deja de llover.",
        "Y en el mismo árbol, en el nivel cien, está Irrompible, la ventaja que hace que tus ganzúas no se rompan nunca. Con esa, la Llave de cera ya no sirve ni de recuerdo.",
        "Gastar un punto de ventaja en esto es elegir, con toda la calma del mundo, no mejorar en nada.",
        "Lo único que consigue es llenarte el inventario de llaves con nombre. Llave de la casa de no sé quién. Llave del cofre de no sé qué.",
        "Llaves de puertas que ya están abiertas. Si eso no es la definición de inútil, que alguien me explique cuál es.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Clarividencia.",
        "Es un hechizo de Ilusión de nivel novato, y lo vende casi cualquier mago, y hasta la tienda de Cauce Boscoso.",
        "Mientras lo mantienes, dibuja en el suelo un rastro de luz que te lleva hacia tu objetivo actual.",
        "El problema es que el juego ya tiene una brújula que te marca exactamente lo mismo, con un marcador encima, y sin gastar nada.",
        "Clarividencia hace lo que ya hace la brújula, pero gastando veinticinco puntos de magia por segundo. Es el mapa más caro de todo Tamriel.",
        "Y como solo funciona mientras lo lanzas, vas por el camino con la mano en alto, gastando magia, como quien busca señal con el teléfono.",
        "Su mayor virtud es que sube Ilusión sin ningún peligro. O sea, que lo mejor que puedes hacer con él es lanzarlo contra la nada.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, el bollo dulce.",
        "Es la comida más famosa de Skyrim. Tan famosa, que hasta los guardias se burlan de ti con ella. A ver si lo adivino, alguien te robó tu bollo dulce.",
        "Hay ciento sesenta bollos colocados a mano por el mundo, en más de ochenta sitios distintos.",
        "¿Y qué hace? Te cura cinco puntos de salud. Cinco.",
        "La poción de curación más pequeña del juego te cura veinticinco. O sea, que para igualar un frasquito tendrías que comerte cinco bollos en mitad de la pelea, mientras un draugr te espera con mucha educación.",
        "Y con Hearthfire, puedes hornearlo tú mismo con cinco ingredientes. Sal, harina, mantequilla, leche y un huevo.",
        "Cinco ingredientes para cinco puntos de salud. Un punto por ingrediente. Las cuentas de la panadería de Skyrim no fallan.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Telequinesia.",
        "En cualquier otro mundo, mover objetos con la mente sería el poder más temido. En Skyrim es un hechizo de Alteración, de nivel adepto, que te deja atraer un objeto desde lejos o lanzarlo.",
        "Y cuesta ciento setenta puntos de magia por segundo. Por segundo.",
        "Lo que lanzas apenas hace daño. Lo justo para que un aldeano se enfade contigo, y nada más. En combate, no sirve.",
        "Y encima, en el juego base no hay ni un solo sitio fijo donde encontrar el libro. O se lo compras a Tolfdir en el Colegio de Hibernalia, o tienes un veinticinco por ciento de suerte de que aparezca en una ruina.",
        "Lo más útil que hace es robar cosas desde el otro lado de la mesa sin que el dueño te vea. Que, siendo sinceros, es justo para lo que lo querías.",
        "Y si te quedas sin magia mientras sujetas algo, el objeto sale disparado con el mismo ruido que un grito de dragón. Muy discreto todo.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, Reflejos rápidos.",
        "Es una ventaja de Bloquear, de nivel treinta. Cuando un enemigo te lanza un ataque de poder, y tú estás bloqueando, el tiempo se ralentiza.",
        "Léelo otra vez. El tiempo se ralentiza, para que esquives un golpe que ya estás parando con el escudo.",
        "Es ponerle cámara lenta a un problema que ya tenías resuelto.",
        "Y por si fuera poco, tiene un error famoso. Si golpeas con el escudo justo en ese momento, y hay varios enemigos a la vez, la cámara lenta puede no terminar nunca.",
        "Al principio tiene gracia. Luego te das cuenta de que estás atrapado en una película de acción a cámara lenta, y que la única forma segura de salir es bloquear otra vez y esperar a que te vuelvan a pegar.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. Los caballos.",
        "En la tierra de los dragones, un caballo debería ser tu mejor aliado. En Skyrim, es un compañero con ideas propias.",
        "Se mete a pelear por su cuenta contra lo que se te ponga delante, y tú te pasas el combate intentando que no se muera.",
        "Desde una actualización del juego puedes luchar montado, pero solo con armas y con arco. Con magia, nada.",
        "Eso sí, sube montañas casi verticales como si fuera una cabra. Y si caes desde muy alto, a veces la caída que te iba a matar a ti, mata al caballo.",
        "Y mi favorita. El caballo cuenta como testigo. Si cometes un crimen delante de él, es como si te hubiera visto alguien.",
        "Así que tu fiel corcel, en el fondo, es un chivato de cuatro patas.",
        "Y el único caballo que de verdad vale la pena, Shadowmere, solo lo consigues con la Hermandad Oscura. Si la destruyes, no lo vas a ver nunca.",
    ]},
    {"id": "p6", "frases": [
        "En el seis, dos poderes de raza que nadie usa.",
        "Cada raza de Skyrim tiene un poder especial que puedes usar una vez al día. Los nórdicos hacen huir a sus enemigos, los bretones absorben hechizos... y luego están los imperiales y los bosmer.",
        "El imperial tiene la Voz del Emperador. Calma a la gente que tiene cerca durante sesenta segundos.",
        "Solo a la gente. Ni animales, ni monstruos, ni dragones. Que, casualmente, es casi todo lo que quiere matarte en este juego.",
        "Y aunque se parece mucho a un hechizo de Ilusión, no aprovecha ninguna ventaja de Ilusión. Un minuto de paz, y luego a pelear igual.",
        "El bosmer tiene Dominar animal. Convierte a un animal en tu aliado, también sesenta segundos, una vez al día.",
        "Un lobo amigo durante un minuto. Justo lo que tarda en morir contra el primer bandido.",
        "Lo más irónico es que el imperial tiene otra habilidad que sí funciona. Encuentra unas cuantas monedas de más en los cofres con oro. Su verdadero poder de raza es encontrar calderilla.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. La Cuchilla de Mehrunes.",
        "En Lucero del Alba vive Silo Vesuio, un hombre que tiene en su casa un museo dedicado al Amanecer Mítico, la secta que intentó traer a Mehrunes Dagon a Tamriel.",
        "Te pide que le ayudes a reunir las piezas de la daga más legendaria de su señor. El pomo, la empuñadura y los fragmentos de la hoja. La vaina ya la tiene él.",
        "Y cuando las llevas al santuario, Mehrunes Dagon te pone una condición. La daga se repara, si matas a Silo.",
        "Así que matas al único fan de Dagon que te trató bien, y a cambio te llevas una daga que puede matar a cualquier enemigo de un solo golpe.",
        "¿La probabilidad? Según el propio código del juego, tenía que ser del uno por ciento. Pero por un error, es de dos entre ciento uno. Casi un dos por ciento.",
        "Más o menos, un golpe de cada cincuenta. Y además, la daga no mejora con ninguna ventaja de Herrería.",
        "Y los dos jefes más duros de Dragonborn, Miraak y Karstaag, son inmunes a la muerte instantánea.",
        "Siendo justos, como daga no está mal. Hace lo mismo que una daga daédrica y pesa la mitad. Pero si la quieres por el milagro, prepárate para dar muchas puñaladas esperándolo.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, el Hacha del arrepentimiento.",
        "Cerca de Falkreath te encuentras con un perro que habla. Se llama Barbas, y es el compañero de Clavicus Vile, el príncipe de los tratos, con el que se acaba de pelear.",
        "Lo acompañas por media provincia hasta el santuario del príncipe, y Clavicus te manda a por un hacha.",
        "Y cuando vuelves con ella, te ofrece un trato. Si le devuelves al perro, te da su máscara. Pero si matas a Barbas con el hacha, te la puedes quedar.",
        "Barbas es invulnerable durante todo el juego. Esa hacha es lo único que puede hacerle daño.",
        "Así que matas al perro que te acompañó todo el camino, ¿y qué te llevas? Un hacha de veintidós de daño, que le quita veinte puntos de aguante al enemigo.",
        "Es el arma cuerpo a cuerpo más lenta de todo el juego. Más lenta que cualquier martillo de guerra.",
        "No mejora con ninguna ventaja de Herrería, y ni siquiera cuenta como artefacto daédrico para el logro de reunirlos todos.",
        "Mataste a un perro por un hacha que ni el propio juego considera especial. Con razón se llama del arrepentimiento.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Ser hombre lobo, en el juego original.",
        "Los Compañeros de Carrera Blanca te ofrecen la sangre de la bestia como el mayor de los honores. Y la primera vez, la verdad, impresiona.",
        "Te transformas una vez al día durante dos minutos y medio, y cada vez que te comes un cadáver, ganas treinta segundos más.",
        "Pero mientras eres lobo no puedes usar tu equipo, ni hechizos, ni gritos, ni poderes.",
        "No puedes recoger nada, ni abrir cofres, ni forzar cerraduras, ni hablar con nadie. Ni siquiera puedes mirar el mapa.",
        "Y no vuelves a ser humano cuando quieres. Te toca esperar a que se acabe, o sentarte a esperar con el menú del tiempo.",
        "En la versión original, además, al volver a ser humano te tenías que poner otra vez toda la armadura, pieza por pieza, a mano.",
        "Y antes de Dawnguard, el lobo no tenía ni un solo árbol de ventajas. Ni uno. Tu personaje podía subir cien niveles, y tu lobo seguía igual que el primer día.",
        "Era un superpoder que te dejaba sin manos, sin bolsillos y sin conversación. Una mascota muy cara, que encima eras tú.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Proyectar voz.",
        "Los gritos de dragón son lo que te hace especial. Fuerza implacable, que manda a volar a cualquiera. Y luego está Proyectar voz.",
        "Sus tres palabras están juntas en una sola pared, en Punta Mellada. Y esa pared la vigilan un dragón y un sacerdote dragón, Krosis.",
        "Es uno de los dos únicos gritos con todas sus paredes guardadas por un sacerdote dragón. O sea, de lo más difícil de conseguir.",
        "Y cada palabra te cuesta su propia alma de dragón. Tres almas, en total.",
        "¿Y qué hace? Lanza tu voz a otro sitio, para que los enemigos vayan a mirar qué fue eso. Y solo engaña a los que todavía no te han visto.",
        "Las tres palabras hacen exactamente lo mismo. La única diferencia es que esperas menos para volver a gritar.",
        "¿Y qué dice la voz del Sangre de Dragón cuando la proyectas? Insultos. Oye, cerebro de queso. Oye, nariz de melón. Oye, feo.",
        "Y si apuntas a un gigante o a un mamut que estaba tranquilo, se vuelve hostil. Su uso más práctico es enfadar a un gigante desde lejos.",
        "Tres almas de dragón para llamar cerebro de queso a un bandido. Ese es el poder de la voz, señoras y señores.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. El objeto que le da nombre a toda la saga.",
        "Un Pergamino Antiguo, un Elder Scroll. Según el lore, guardan todo lo que pasó, lo que pasa y lo que va a pasar. Y leerlos puede dejarte ciego, o loco.",
        "En el juego base solo hay uno, y para conseguirlo bajas a lo más hondo de una ciudad dwemer enterrada bajo Skyrim.",
        "Lo usas una vez, en la cima de la Garganta del Mundo, para aprender el grito que derrota a Alduin.",
        "Y después de eso, el objeto más poderoso de toda la saga se queda en tu mochila sin hacer nada.",
        "Pesa veinte, pero como es de misión, en tu inventario no pesa nada. Y vale cero monedas.",
        "Lo único que puedes hacer con él es llevárselo a Urag gro-Shub, el orco bibliotecario del Colegio de Hibernalia, que te lo compra por dos mil monedas.",
        "Y si tienes Dawnguard, lo vuelves a necesitar para otra misión. Y si ya se lo vendiste a Urag, te lo revende por cuatro mil. El doble.",
        "Piénsalo. La saga se llama The Elder Scrolls. Y en Skyrim, lo más útil que puedes hacer con un Elder Scroll es vendérselo a un orco, y luego volver a comprarlo más caro.",
        "Por eso es el número uno. Todo lo demás de esta lista es inútil por un error o por un mal diseño. Este es inútil por destino.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Quince cosas de Skyrim que no sirven para nada, de un vecino pesado en Carrera Blanca al pergamino que da nombre a la saga.",
        "Si tú conoces algo todavía más inútil, déjalo en los comentarios, que los leo todos. Y no vale decir Nazeem otra vez.",
        "Y si quieres ver justo lo contrario, en el canal tienes los ocho exploits más ROTOS de Skyrim, donde el juego sí te da demasiado.",
        "Y la próxima vez que un guardia te pregunte si alguien te robó tu bollo dulce, ya sabes qué contestarle. Que se lo quede. Cura cinco.",
    ]},
]
