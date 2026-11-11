# -*- coding: utf-8 -*-
"""GUION de «Los 30 MISTERIOS más raros de Call of Duty» (motor SECUENCIA YT, Expediente 141, 9-nov-2026, ~25 min).
Plantilla: videos/cod_mandela/ (misma fórmula; cambia el tema y la duración). Investigación con fuentes: investigacion.md.
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo con corchetes; sin [whispers] ni [excited] (2-nov-2026).
REGLA DE ORO: cada frase nombra algo que SE VE; si la voz nombra un sonido, se OYE («post» = la voz calla y suena el clip).
ESCENAS = una por puesto (+ «b» tras cada sonido); los cortes salen de `beats`.
"""

TITULO = "Los 30 MISTERIOS más raros de Call of Duty"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Expediente 141: DAMIÁN de la biblioteca de ElevenLabs (elegida por el usuario el 2-nov-2026), por id en cualquier cuenta
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # el audio del juego solo donde la voz lo nombra (ambiente_por, tras `beats`)
    ambiente_por={},
    recorte_por={"scene-002": .12, "scene-108": .12},   # marca OYN (10-nov)
    yt=dict(sufijo="Call of Duty", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # canal de videojuego: OST oficial de cada CoD (audio/ost/, armar_musica_ost.py), nunca Lyria

# Pausas con la voz callada («si la voz nombra un sonido, se oye», 31-oct-2026):
#   intro: el chillido de la cara de Mob of the Dead · p18 el riff de los tambores de IX · p13 la voz rusa del teléfono ·
#   p11 las dos voces de Samantha (original y nueva) · p07 las voces del cementerio de Sanctuary
# Comentarios (≤ 10 días): @H.Hoster en p22 (Shadows of Evil) y @LDVader en el cierre (el «Press F» del de Mandela).
ESCENAS = [
    {"id": "intro", "pre": 0.3, "post": 2.2, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: lo que nadie ha podido explicar.",
        "Azotea de Alcatraz. Un rifle de francotirador, apuntando a los fuegos artificiales sobre la bahía. Mira bien.",
    ]},
    {"id": "intro_b", "frases": [
        "Trece años después, nadie sabe de quién es esa cara.",
        "Una voz que Treyarch cambió en dos días, sin decir por qué. Un fantasma sin arma, paseando por un mapa de Call of Duty 4. Un corazón escondido en un castillo nevado, que tardaron tres años y medio en encontrar.",
        "Un platillo volante en un sótano nazi. Y un hombre de traje, escondido desde hace quince años en los archivos de Modern Warfare 3.",
        "Treinta misterios y leyendas de Call of Duty. Unos resueltos años después, por gente que leyó el código del juego. Otros, todavía abiertos hoy.",
        "Todo con el juego en pantalla. Y el número uno es una escena que Infinity Ward nunca quiso que vieras.",
    ]},
    {"id": "p30", "frases": [
        "Número treinta. El chicle que nunca salió.",
        "Shadows of Evil, Black Ops 3, dos mil quince. Las máquinas de GobbleGum te dan chicles con poderes: uno te da todas las perks, otro hace que los zombis no te vean.",
        "Pero en los carteles de la ciudad aparece un chicle que no existe en el juego. En los archivos se llama Private Eye: detective privado.",
        "Se descubrió a finales de dos mil quince, y nunca llegó a salir. Nadie sabe qué hacía. [deadpan] En una ciudad llena de detectives, el único chicle detective se quedó sin caso.",
    ]},
    {"id": "p29", "frases": [
        "En el veintinueve, ¿estás muerto desde la primera misión?",
        "Black Ops 3. En la primera misión, tu soldado queda destrozado por un robot, y le ponen brazos y piernas mecánicas. Desde ahí, la campaña se vuelve cada vez más rara.",
        "Una teoría de los fans dice que casi todo lo que juegas después pasa dentro de la mente de tu personaje, que se está muriendo. La apoyan un bosque congelado que vuelve una y otra vez, y un final que nadie termina de entender.",
        "Treyarch nunca la confirmó. Y ni los que la defienden se ponen de acuerdo en cuándo empieza el sueño. [deadpan] Lo único seguro es que el bosque estaba muy frío.",
    ]},
    {"id": "p28", "frases": [
        "Número veintiocho. El viejo sin nombre.",
        "TranZit, Black Ops 2, dos mil doce. Un autobús que conduce un robot, y cuatro supervivientes: Misty, Marlton, Stuhlinger, y un anciano.",
        "Ese anciano es Russman. No recuerda nada de su pasado, y dice que cada perk le cura una enfermedad.",
        "Pero nunca se dijo su nombre de pila. Russman es su apellido. Y en los archivos del juego se llama, simplemente, oldman: el viejo.",
        "Volvió en Black Ops 4, y la historia de su grupo se cerró. [deadpan] Así que el hombre se quedó para siempre como el viejo.",
    ]},
    {"id": "p27", "frases": [
        "En el veintisiete, el fuego verde.",
        "Dead of the Night, Black Ops 4: una mansión con vampiros y hombres lobo. Su arma maravilla se mejora dos veces.",
        "Con la segunda mejora, el fuego de las trampas se vuelve azul, y sirve para encender las chimeneas de la misión principal.",
        "Pero si a la trampa le disparas con la primera mejora, el fuego se vuelve verde. Y el fuego verde no sirve para nada.",
        "Cerca del mausoleo hay una batería sin uso, y hay salas de un Easter egg que se canceló. [deadpan] Treyarch hizo un fuego verde, y se fue sin decir para qué.",
    ]},
    {"id": "p26", "frases": [
        "Número veintiséis. Los retratos en sombra.",
        "Kino der Toten, el teatro de Black Ops. Hay un cuarto con los retratos de los cuatro protagonistas: Dempsey, Nikolai, Takeo y Richtofen. Y cada uno comenta el suyo.",
        "Pero hay dos cuadros más. Uno colgado en la pared, y otro tirado en el suelo, con una figura en sombra. Y las dos parecen la misma persona.",
        "Nadie ha dicho quién es. [short pause] En un teatro lleno de zombis, lo más inquietante es un cuadro sin cara.",
    ]},
    {"id": "p25", "frases": [
        "En el veinticinco, la esfera del Golden Gate.",
        "Mob of the Dead: Alcatraz, en los años treinta. Cuatro gánsteres muertos que intentan escapar de la isla.",
        "Desde el puente donde se mejoran las armas, si miras al cielo, hay una bola naranja quieta, flotando sobre la bahía.",
        "Treyarch nunca la explicó. La teoría favorita: un foo fighter, las luces que los pilotos de la Segunda Guerra Mundial juraban ver en el cielo. [deadpan] O una farola muy ambiciosa.",
    ]},
    {"id": "p24", "frases": [
        "Número veinticuatro. El ordenador de la CIA.",
        "Black Ops, dos mil diez. En el menú principal estás atado a la silla del interrogatorio. Pero si pulsas los botones correctos, te sueltas, y te levantas.",
        "Detrás hay un ordenador de la CIA. Escribes los comandos correctos, y aparecen archivos secretos, correos, y dos juegos enteros escondidos.",
        "Dead Ops Arcade, un juego de zombis visto desde arriba. Y Zork, una aventura de texto de hace más de cuarenta años, con un trofeo por dejarte devorar por un monstruo en la oscuridad.",
        "[deadpan] El juego de guerra más vendido de su año traía una aventura de texto. Para el que se levantara de la silla.",
    ]},
    {"id": "p23", "frases": [
        "En el veintitrés, un libro en una estantería.",
        "Antes de ser Dr Disrespect, el streamer de las gafas y el bigote, Guy Beahm trabajó en Sledgehammer Games, diseñando niveles de Call of Duty.",
        "El primero de abril de dos mil veintidós, alguien enseñó que en la misión Tierra quemada, de Modern Warfare 3, hay una librería. Y en un estante, un libro firmado por Guy Beahm.",
        "Once años ahí, y nadie lo había visto. Como lo publicaron el primero de abril, el día de las bromas en Estados Unidos, medio internet pensó que era broma. Hasta que el propio Doc lo compartió.",
    ]},
    {"id": "p22", "frases": [
        "Número veintidós. El nombre del Hombre Sombra.",
        "Shadows of Evil, Morg City. El mago que guía a los cuatro protagonistas es el Shadowman. Y en la ciudad se hace llamar Tony Hale Rapt.",
        "Pon esas letras en otro orden: Nyarlathotep. El dios mensajero de los mitos de Lovecraft, el creador de Cthulhu. Un anagrama exacto.",
        "Al final se revela como un Apothicon, un dios del vacío. [short pause] Y guarda este nombre, Shadowman. Más adelante sale otro. Y no es el mismo.",
        "Por cierto: en el expediente anterior, H.Hoster escribió sobre este mapa que el Easter egg es tremendo, y que solo te den una tarjeta es feo. Lo leí. Aquí se leen todos los comentarios. Y tiene razón: tanto ritual, para una tarjeta.",
    ]},
    {"id": "p21", "frases": [
        "En el veintiuno, los aliens de Call of Duty.",
        "Finest Hour, dos mil cuatro. En un sótano secreto, un platillo volante nazi.",
        "Seis años después, Black Ops trae un mapa multijugador en el Área cincuenta y uno: Hangar dieciocho. Y en un rincón hay tres cuerpos bajo sábanas, con manos de cuatro dedos y pies azules.",
        "Al lado, una mesa de autopsias empotrada en la pared, con sangre. Como si uno se hubiera levantado.",
        "[deadpan] Call of Duty nunca confirmó a los extraterrestres. Pero tampoco les quitó la sábana.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. La historia que se quedó colgada.",
        "Call of Duty Ghosts, dos mil trece. Logan pelea con Rorke en la playa, y lo da por muerto.",
        "Pero Rorke se levanta, arrastra a Logan herido, y le dice: habrías sido un gran Ghost. El plan: lavarle el cerebro, y convertirlo en uno de los suyos.",
        "Y entonces, Ghosts 2 nunca se hizo.",
        "Trece años después, Logan sigue en manos de Rorke. Y su hermano Hesh, y Riley, el perro, siguen esperando. [sighs] El misterio no es qué pasó. Es si alguien lo va a contar algún día.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, el dedo de Reznov.",
        "Black Ops. Viktor Reznov te acompaña media campaña. Y al final descubres que murió en Vorkutá: el que estaba contigo era una alucinación de Mason.",
        "Pero hay un detalle. Al Reznov real le falta el dedo índice de la mano derecha. Y el Reznov que ve Mason, muchas veces lo tiene.",
        "Una pista escondida en una mano. O un descuido de animación, porque en algunas misiones sale sin el dedo. [deadpan] Nadie lo sabe. Y Reznov no está para preguntarle.",
        "Treyarch lo trajo de vuelta en Black Ops 4 y en Black Ops 6. Pero fuera de la historia.",
    ]},
    {"id": "p18", "post": 4.5, "frases": [
        "Número dieciocho. El concierto escondido.",
        "Nueve, el mapa del coliseo de Black Ops 4, con gladiadores zombis. Si disparabas a los tambores en ciertas rondas, sonaba esto.",
    ]},
    {"id": "p18b", "frases": [
        "Y ahí se quedaba todo el mundo. Durante novecientos treinta días, nadie supo qué más hacer.",
        "En abril de dos mil veintiuno, un modder publicó los scripts del juego, descompilados. Y ahí estaba el resto: pasos imposibles de adivinar, como golpear zombis con el escudo hasta que se prendieran fuego.",
        "Al final, un concierto de rock en el coliseo. [deadpan] El Easter egg no lo resolvió nadie jugando. Lo resolvieron leyendo el código.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, la calavera con escopetas.",
        "Black Ops 2 Zombies. En tu tarjeta salía un emblema: un hueso, dos huesos, una calavera, una calavera con cuchillo. Y la más temida: la calavera con escopetas.",
        "Treyarch nunca explicó cómo se subía. Todos pensaban que era por bajas.",
        "Más de diez años después, un modder lo sacó del código. Las bajas no cuentan nada. Cuenta cuántas rondas aguantas por cada vez que caes. Y para las escopetas hacen falta unas treinta horas jugadas.",
        "Las rayas de tiza son los días seguidos que juegas. Y si la calavera tiene los ojos azules, jugaste en los últimos cinco días. [deadpan] Diez años presumiendo una calavera. Sin saber qué significaba.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. Alex murió… hasta que no.",
        "Modern Warfare, dos mil diecinueve. Al final de la campaña, el detonador falla, y Alex se queda atrás para hacerlo volar todo él mismo. La explosión. Y nunca ves su cuerpo.",
        "Muchos sospechaban que seguía vivo. Y en abril de dos mil veinte, la cinemática de la temporada tres lo enseñó: vivo, con una pierna de metal, junto a Ghost.",
        "Activision lo sacó como operador. [deadpan] El rumor era verdad. Y la entrada le costó una pierna.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, las cintas de Pawn Takes Pawn.",
        "Agosto de dos mil veinte. Activision manda proyectores de diapositivas a creadores de contenido. Sin explicación.",
        "Las pistas llevan a una web: una oficina a oscuras, una tele vieja, y cada día una cinta VHS nueva, con transmisiones de la Guerra Fría, números y códigos.",
        "Esos códigos abrían puertas cerradas dentro de Warzone, en Verdansk. Y al resolverlo todo salió una fecha: veintiséis de agosto.",
        "Ese día, dentro de Warzone, se reveló el nuevo juego: Black Ops Cold War. [deadpan] El anuncio no lo dio Activision. Lo desenterraron los jugadores.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. Warzone existía antes de existir.",
        "Noviembre de dos mil diecinueve. Modern Warfare lleva un mes a la venta, y un dataminero, Senescallo, encuentra en los archivos un modo battle royale. Y después, el mapa entero.",
        "Archivos con el nombre Warzone. Listas de dúos y de cuartetos. Y un jugador que, por un fallo, acaba teletransportado dentro del mapa. Lo graba, y Activision le cierra la cuenta.",
        "Los filtradores dijeron: principios de marzo. Y el diez de marzo de dos mil veinte salió Warzone, gratis. [deadpan] El rumor más exacto de Call of Duty lo escribió el propio juego.",
    ]},
    {"id": "p13", "post": 4.0, "frases": [
        "En el trece, el búnker once.",
        "Verdansk, Warzone, dos mil veinte. Un búnker cerrado que nadie sabía abrir. Y por todo el mapa, teléfonos. Si contestas uno, una voz en ruso dicta números.",
    ]},
    {"id": "p13b", "frases": [
        "Cada número es otro teléfono del mapa: el nueve, en la presa. El ocho, en el hospital. El tres, en la cantera. Los llamas en orden, y el búnker se abre.",
        "Dentro: cabezas nucleares, y un plano secreto del MP7. [deadpan] La puerta más blindada de Verdansk se abría con una guía telefónica.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. El director que parpadeaba en Morse.",
        "Abril de dos mil dieciséis. Jason Blundell, el director de Zombies en Treyarch, da una entrevista rápida. Y los comentarios notan algo: parpadea demasiado.",
        "Tres usuarios de Reddit pasan los parpadeos a código Morse. Y salen frases: no pongas ciento quince. Contacta al doctor. Confía en mí, Sam.",
        "Casi seguro es casualidad: el cerebro busca mensajes donde no los hay. Pero esa misma noche, Blundell le contó al entrevistador que sabía Morse. Lo bastante para soltar una frase, si quisiera.",
        "[short pause] Nunca dijo si quiso.",
    ]},
    {"id": "p11", "post": 7.5, "frases": [
        "En el once, la voz de Samantha.",
        "Agosto de dos mil trece. Treyarch estrena la cinemática de Origins. Y la narradora, Samantha, suena así.",
    ]},
    {"id": "p11b", "post": 9.0, "frases": [
        "Dos días después, en la versión nueva, la misma frase suena así.",
    ]},
    {"id": "p11c", "frases": [
        "De una voz grave y distorsionada, a una niña estadounidense. Treyarch nunca explicó el cambio.",
        "[deadpan] La niña que controla a los zombis cambió de voz en dos días. Y nadie se atrevió a preguntarle por qué.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. La cara de Alcatraz.",
        "Ya la viste al principio. Mob of the Dead, dos mil trece. Subes a la azotea, apuntas con un francotirador a los fuegos artificiales, y esperas.",
        "Una cara deformada, durante una fracción de segundo, con un chillido.",
        "Está documentada. Lo que nadie ha documentado es de quién es. ¿El viejo Russman? ¿Nero, el mago de Shadows of Evil? ¿Samantha?",
        "Treyarch nunca lo dijo. [deadpan] Trece años después, la cara sigue ahí. Y sigue sin nombre.",
    ]},
    {"id": "p09", "frases": [
        "En el nueve, el corazón del castillo.",
        "Der Eisendrache, Black Ops 3, dos mil dieciséis: un castillo nevado en los Alpes, con arcos de fuego y dragones.",
        "En julio de dos mil diecinueve, la comunidad leyó el código del juego, y encontró una receta absurda. En la ronda dos, deja que los zombis rompan todas las barricadas. Repara exactamente dos tablas en cada una. Compra la RK5, pon otras dos tablas, cámbiala por la Shiva, una tabla más. Y abre la puerta del patio en cinco segundos.",
        "Aparece un corazón, con una foto. Un homenaje de Drew Marlowe, desarrollador de Treyarch, a su esposa y a su hijo.",
        "Tres años y medio escondido. [short pause] Nadie lo iba a encontrar jugando. Porque no estaba hecho para nosotros.",
    ]},
    {"id": "p08", "frases": [
        "Número ocho. Spectre.",
        "Black Ops 3, dos mil quince. Un especialista con máscara, una espada, y una ficha en blanco.",
        "Nombre real: desconocido. Fecha y lugar de nacimiento: desconocidos. Y en la casilla de género: desconocido. Ni siquiera se sabe si es hombre o mujer.",
        "Volvió en Black Ops 4, con su propia operación. Y en dos mil veintiséis llegó a Black Ops 7 y a Warzone. [deadpan] Once años en la saga. Y la máscara sigue puesta.",
    ]},
    {"id": "p07", "post": 8.0, "frases": [
        "En el siete, las voces del cementerio.",
        "Sanctuary, Modern Warfare 3. Un mapa de multijugador con un cementerio en el centro. Si te paras sobre los parches de césped, se oye esto.",
    ]},
    {"id": "p07b", "frases": [
        "Una niña. Y su padre. Pero no hay nadie.",
        "Esas voces son de la campaña: el video casero de la familia Davis, de vacaciones en Londres, en la misión Davis Family Vacation. La niña se llama Sarah.",
        "[sighs] Infinity Ward escondió a esa familia en un cementerio. [short pause] Y la dejó ahí, jugando.",
    ]},
    {"id": "p06", "frases": [
        "Número seis. El mensaje de amor perdido.",
        "Call of Duty 3. Ironclad, un mapa descargable solo para Xbox 360, de enero de dos mil siete.",
        "Su diseñador, Jason McCord, contó en dos mil veintiuno que le pidió a un programador esconder un mensaje para su novia. El programador le iba a decir cómo verlo. Nunca se lo dijo. Y hoy responde: estoy como noventa por ciento seguro de que lo hice.",
        "Jesse Snider, el creador del modo Zombies, ya había contado que en dos Call of Duty hay pedidas de mano secretas sin descubrir. Y que en los dos casos, la pareja rompió antes de que saliera el juego.",
        "En dos mil veinticuatro, un youtuber lo buscó durante semanas. Encontró un nombre en un barco: Juliana. Y nada más. [deadpan] Diecinueve años escondido. El Easter egg más romántico de Call of Duty. Y el más maldito.",
    ]},
    {"id": "p05", "frases": [
        "En el cinco, el fantasma de Vacant.",
        "Nueve de agosto de dos mil ocho. Un jugador sube un video: un fantasma en Vacant, el mapa de oficinas abandonadas de Call of Duty 4.",
        "Una figura sin arma cruza la oficina caminando raro, atraviesa una puerta, y desaparece. Y no se le puede matar.",
        "Más de medio millón de vistas. Secuelas, otro fantasma en Backlot, y medio internet buscándolo en partidas privadas.",
        "Era un montaje. El marcador cambia entre tomas, el video está cortado aunque dice sin editar, y el fantasma tiene nombre de jugador. [deadpan] El primer fantasma de Call of Duty tenía gamertag.",
    ]},
    {"id": "p04", "frases": [
        "Número cuatro. El cifrado de Alcatraz.",
        "Mob of the Dead, abril de dos mil trece. En la pantalla de carga, seis columnas de letras: A, D, F, G y X.",
        "Es el cifrado que usaba Alemania en la Primera Guerra Mundial. Todos sospechaban que la clave era la palabra zombie. Pero no salía nada.",
        "Hubo una solución falsa. En dos mil diecisiete, un cómic oficial de Zombies redibujó la pantalla con la palabra zombie de titular. Y en septiembre de dos mil dieciocho, un usuario de Reddit lo logró: había que quitar una fila repetida.",
        "El mensaje, en alemán: urgente. El gigante está en Francia.",
        "[short pause] Era el anuncio de Origins: un robot gigante, en la Francia de mil novecientos dieciocho. Escondido cuatro meses antes de que enseñaran el mapa. Y nadie lo leyó a tiempo.",
    ]},
    {"id": "p03", "frases": [
        "Número tres. ¿Alex Mason mató a Kennedy?",
        "Black Ops, dos mil diez. En Vorkutá, Dragovich programa a Mason para matar al presidente de Estados Unidos. Y Reznov altera esa programación.",
        "En el Pentágono, Mason se imagina apuntándole a Kennedy. Y en el final, mientras Hudson le dice que hay huecos en su memoria, momentos en los que no saben dónde estuvo, ves imágenes de archivo: Dallas, veintidós de noviembre de mil novecientos sesenta y tres.",
        "Y entre la multitud, alguien que se parece a Mason.",
        "Nunca se confirmó. Ni Black Ops 2 ni Cold War lo aclararon. [deadpan] Treyarch metió a su protagonista en el crimen más famoso del siglo veinte. Y se fue sin cerrar el expediente.",
    ]},
    {"id": "p02", "frases": [
        "En el dos, el Easter egg imposible.",
        "Agosto de dos mil quince. Jason Blundell, otra vez él, está harto: la comunidad descubre cada secreto de Zombies en días. Así que promete meter en Black Ops 3 uno que no podrán romper.",
        "Los datamineros abrieron el juego. Encontraron el corazón de Der Eisendrache, y todo lo demás. Pero el imposible, no.",
        "En dos mil veintitrés, los fans le pidieron una pista. Su respuesta: la pista está en el nombre. Es imposible.",
        "Hay teorías: un rifle dentro de un teseracto en el mapa The Giant, títulos de libros en Der Eisendrache con el estilo de un criptógrafo del siglo dieciséis. Ninguna confirmada.",
        "Blundell dejó Treyarch, y no tiene redes sociales. [short pause] Once años después, el Easter egg imposible sigue cumpliendo su promesa.",
    ]},
    {"id": "p01", "frases": [
        "Y el número uno. El hombre de traje.",
        "Modern Warfare 3, dos mil once. El final que conoces: Price mata a Makárov en el hotel de Dubái, se sienta en la azotea, y enciende un puro.",
        "Pero en mayo de dos mil veinticuatro, dos modders restauraron una escena que seguía dentro del juego. Cortada.",
        "El mismo hotel. Price, desplomado, muere por sus heridas. Y entonces entra él: un hombre de traje, en la penumbra del vestíbulo. Sin diálogo. Sin nombre.",
        "En los archivos, sus animaciones se llaman así: shadowman entra. Shadowman sale. Y no, no es el mago de Zombies del puesto veintidós.",
        "Infinity Ward nunca lo ha explicado. Nadie sabe quién iba a ser, ni qué historia preparaba. [short pause] Quince años dentro del disco de Modern Warfare 3. Y sigue de pie, en ese vestíbulo, esperando a que alguien le ponga nombre.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. Treinta misterios: unos resueltos leyendo el código, otros todavía abiertos. ¿Cuál crees que se resuelve primero? Dímelo en los comentarios. Yo apuesto a que el imposible, nunca.",
        "Y a LDVader, que en el expediente anterior escribió que lo de la tecla F era trampa: tienes razón, soldado. Trampa es que te pidan presentar respetos, y no te den la tecla.",
        "Todos los comentarios se leen, y se toman en cuenta para el siguiente expediente. En el canal tienes los efectos Mandela de Call of Duty y los veinticinco secretos de Modern Warfare 4. Y si quieres el siguiente, suscríbete. [short pause] Retírate, soldado.",
    ]},
]

# Nombres que Whisper escribe distinto: se aceptan con CER mayor (se completa tras `seleccionar`).
CER_MAX_POR_FRASE = {   # 10-nov: transcripciones completas; solo nombres (Rourke, Rusman, Eisendrage, Beam, zombies, «9.»)
    "p28_1": .03, "p28_2": .02, "p26_3": .02, "p24_3": .03, "p23_2": .06, "p23_3": .05, "p22_1": .03, "p20_1": .02,
    "p20_2": .025, "p20_4": .015, "p19_1": .03, "p18_1": .07, "p11c_1": .02, "p10_3": .05, "p06_3": .02, "p02_2": .04,
    "p02_4": .03, "p01_2": .03,
}
TAIL_MAX_POR_FRASE = {"p04_2": 1.15, "p20_4": 1.15}   # 10-nov: terminan bien («nada», «día»), la voz llega al último cuadro
