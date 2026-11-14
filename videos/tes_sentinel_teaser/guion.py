# -*- coding: utf-8 -*-
"""GUION — «Los 15 SECRETOS del teaser de The Elder Scrolls VI: Sentinel» (Crónicas de Tamriel, 3-nov-2026).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Noticia del día: Bethesda reveló el
nombre en el video de los 40 años de BGS (teaser mFu8t9735IY). Datos verificados en UESP: _investigacion.md.
Voz: SIETE voces de ElevenLabs que compiten, 2 secretos cada una (el usuario, 3-nov: «una narrando 2 datos cada una y compitiendo
entre ellas… que el público vote»; elegidas de audio/muestras_voces/: 1, 4, 6, 7, 9, 15 y 16, «me gusta mucho la 16: dale un poco más
de líneas» → el Profeta lleva 3 secretos y el final) + un hueco corto con la voz clonada del usuario (ag1_2). Turbo, corchetes
SIN [whispers] ni [excited]. 3-nov (el usuario): su voz ya NO es «El Jefe» sino «el Humano tras el Telón», crítico n.º 1
(o «el filtrador»), con más líneas y las demás voces burlándose de él con cariño. La v1 (todo Johnny) está en voz/_guion_v1_johnny.py.
El usuario (3-nov): ≥ 16 min (relleno con lore, curiosidades y easter eggs), ≥ 3 críticas con burla disfrazada, subida PRIVADA.
"""

TITULO = "Los 15 SECRETOS del teaser de The Elder Scrolls VI: Sentinel"
ARCHIVO = "tes_sentinel_teaser"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HMCmDsbKeaSZp5LMOYKR", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), referencia=r"C:\chatterbox_voices\Sarcastica.mp3",
           por_cuenta={2: "GUEeiSJYQQdbv0NJ86Im", 3: "hCU4QZdzzUliy58ezPBz"})   # el Humano tras el Telón (clon del usuario) en las cuentas 2 y 3
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {"Alik'r": "Álikar", "Stros M'Kai": "Stros Mekái", "4E 206": "cuarta era, doscientos seis"}

# Whisper escribe distinto nombres y @ (Zalmor, Redward, Alicar, Akorizi, Dunward): tomas oídas como buenas (3-nov)
CER_MAX_POR_FRASE = {"intro_2": 0.026, "intro_3": 0.04, "p15_3": 0.038, "p12_4": 0.043, "p11_1": 0.031, "p11_5": 0.037, "cr1_0": 0.085, "cr1_1": 0.047, "p10_1": 0.033, "p9_2": 0.032, "p9_3": 0.017, "p8_1": 0.036, "p8_4": 0.036, "ag1_0": 0.11, "ag1_1": 0.2, "p6_0": 0.04, "cr2_0": 0.07, "p5_0": 0.034, "p5_2": 0.022, "p5_3": 0.061, "p5_4": 0.03, "p5_5": 0.029, "p4_2": 0.045, "p3_2": 0.037, "cr3_0": 0.073, "p1_2": 0.027, "p1_7": 0.01,
                     "voces_0": 0.02, "cierre_6": 0.035, "cierre_3": 0.16, "p11_0": 0.02, "p12_4": 0.04, "p11_4": 0.03, "p9_3": 0.03, "p3_2": 0.02}   # siete voces: «Eduardo», «con H»

TAIL_MAX_POR_FRASE = {"p12_4": 1.3, "p9_3": 1.2, "ag1_0": 1.2, "p1_7": 1.2, "p11_0": 0.9, "p11_4": 0.75, "p3_2": 1.15, "cierre_10": 1.25}   # hablan hasta el final de la toma

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-001": .6, "scene-015": .6, "scene-121": .6, "scene-122": .6, "scene-018": .3},   # re-indexado por _remapear.py (siete voces)   # viento/música del teaser; Todd de fondo
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial (ESO de Brad Derrick + temas de Jeremy Soule; armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Ocho años. Ocho años esperando, y Bethesda por fin nos ha dado algo.",
        "Un montón de arena. Un pergamino con una gema azul. Una palabra: Sentinel. Y una frase firmada por un sacerdote que se está quedando ciego.",
        "[amused] Parece poco. Pero en ese minuto hay una ciudad real, una reina que nadie conocía, una fecha exacta, y una pista que apunta a la Gran Guerra contra los Thalmor.",
        "Hoy te traigo quince secretos del teaser de The Elder Scrolls seis. Todos comprobados, con sus fuentes en la descripción.",
        "[short pause] Y hoy, cambio de planes. No hay un narrador: hay siete voces. Dos secretos cada una, compitiendo entre ellas, y al final eliges tú en los comentarios cuál se queda.",
        "[amused] Te las presento, que ya se están peleando por el micro.",
    ]},
    {"id": "voces", "frases": [
        "[deadpan] Edoardo. Me tocan el trece y el doce. Y no pienso perder contra un señor que se ríe de todo.",
        "[amused] Yo soy Hope. Sentinel y Daggerfall son míos. O sea, lo mejor del video.",
        "José, para servirte. Los desiertos y los redguard. Aquí se viene a narrar, no a hacer chistes.",
        "Mario. La fecha y la reina. Y prometo ir rápido, para que no te duermas con José.",
        "[deadpan] MariCarmen. La guerra y el sacerdote. [short pause] Y al que me quite un voto, lo busco.",
        "Yo soy el Profeta. Me guardo los tres últimos. [short pause] Los secretos importantes siempre llegan al final.",
        "¿Y a mí nadie me presenta? Soy el humano tras el telón. Yo no narro: yo critico. Y ya tengo notas de todos.",
        "[sarcastic] Y nadie se las pidió. Qué humildad la de todos. Empiezo yo, que para algo abrí el video. Y quédate hasta el número uno: es una teoría sobre lo que de verdad dice esa frase, y si es cierta, lo que hiciste en Skyrim podría no haber servido de nada.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. El logo escondido en la arena.",
        "El teaser no empieza con el pergamino. Empieza con una duna, y sobre la arena aparece el engranaje de Bethesda Game Studios.",
        "No es casualidad. El anuncio llegó en el video de los cuarenta años del estudio, grabado en Bethesda, Maryland, donde todo empezó en mil novecientos ochenta y seis.",
        "Todd Howard lo presentó así: todo el mundo pregunta siempre por Elder Scrolls seis, y qué mejor momento para decirles cómo se llama.",
        "[sarcastic] Ocho años de preguntas, y la respuesta fue el nombre. Solo el nombre. Pero oye, es más de lo que teníamos ayer.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, lo que Todd contó antes del teaser.",
        "Antes de enseñar el pergamino, Todd repasa cuarenta años de juegos. Y suelta joyas.",
        "Su primer juego fue Gridiron, de fútbol americano, que él llama su primera simulación. Y antes de Fallout hicieron un juego enorme de Terminator.",
        "Cuenta que en enero de mil novecientos noventa y tres llamó a la puerta de ese mismo edificio para pedir trabajo.",
        "Y que cuando les dijeron que la Xbox trescientos sesenta tendría quinientos doce megas de memoria y no doscientos cincuenta y seis, montaron una fiesta para poder hacer Oblivion como querían.",
        "[amused] Y remata con un dato que nos toca: quince años después, Skyrim sigue siendo su juego más jugado. Que no te extrañe que el seis mire hacia él.",
    ]},
    {"id": "p13", "frases": [
        "[deadpan] Gracias, Johnny. Ahora, en serio. Número trece. El teaser de dos mil dieciocho ya apuntaba aquí.",
        "El diez de junio de dos mil dieciocho, Todd Howard cerró su conferencia del E tres con treinta segundos de paisaje: niebla, colinas, una costa y una fortaleza.",
        "Ni nombre, ni fecha. Solo el tema de la saga. Y los fans se pusieron a comparar costas con los mapas de Tamriel como si fueran detectives.",
        "La apuesta más repetida fue el oeste: la costa de Hammerfell y Roca Alta, alrededor de la bahía de Iliac.",
        "[deadpan] Ocho años después, el nombre del juego es el de la ciudad más famosa de esa bahía. Los detectives de internet, esta vez, no iban tan mal.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, el nombre se filtró cinco días antes.",
        "El veintinueve de octubre, Tom Warren, de The Verge, publicó que el juego se llamaría Sentinel y que estaría en Hammerfell.",
        "Y añadió algo más jugoso: que sería el primer juego sobre la historia de los propios Pergaminos Antiguos.",
        "Y hay una pista todavía más vieja. En Starfield, al crear tu personaje, tu número de empleado es siempre el mismo: uno nueve, cero cinco, uno cuatro, dos cero, cero nueve, uno cuatro, cero cinco, uno dos.",
        "[mischievously] Cambia cada par por su letra del alfabeto. Diecinueve, ese. Cinco, e. Catorce, ene. Y así hasta el final. Sale Sentinel. Llevaba ahí desde dos mil veintitrés.",
        "Bethesda no dijo nada. Hasta hoy. El nombre ha salido tal cual, y tras el teaser, la propia Bethesda dio por revelado el lugar.",
        "[sarcastic] Lo que no ha salido es fecha, ni consolas. Bethesda dice que aún pasará un tiempo antes de contar más. Traducido: siéntate.",
    ]},
    {"id": "p11", "frases": [
        "[amused] Precioso, Edoardo, pero en el doce me quedé dormida. Número once. Sentinel existe, y puedes ir hoy mismo.",
        "Sentinel es la capital de Hammerfell, la provincia de los redguard, al oeste de Skyrim. Está en las colinas del noroeste, con la bahía de Iliac al norte y el desierto de Alik'r al sur.",
        "Si sales de Skyrim hacia el oeste, cruzas las montañas de la Cola del Dragón, atraviesas el Alik'r y llegas al mar. Ahí está.",
        "Su nombre tiene historia. Empezó como un puesto de vigía, para proteger a pescadores y mercaderes de lo que salía del desierto. Un centinela. Sentinel.",
        "Y no es una idea nueva. Sale en Daggerfall, de mil novecientos noventa y seis, y en The Elder Scrolls Online es la capital de la región de Alik'r, con su puerto y su palacio.",
        "[amused] O sea, que si no puedes esperar, en Online ya puedes darte un paseo por el escenario de Elder Scrolls seis. Casi mil años antes, eso sí.",
    ]},
    {"id": "cr1", "frases": [
        "Una pausa, que hoy toca correo. @alcoholikmisanthroper1934 nos escribió esto en el video de las armas.",
        "Que pusimos la mejor arma en el último puesto, que ni mencionamos que no hace falta recargarla, y que es un puto video hecho con IA. Ja, ja.",
        "[amused] Lo de la recarga es verdad: la daga de hueso de dragón no lleva encantamiento, así que no se gasta nunca. Apuntado, y gracias.",
        "Lo de poner la mejor arma en el último puesto, en cambio, se llama número uno. Y que la vieras hasta ahí para quejarte, en este canal se llama retención. Gracias por eso también.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, la ciudad que se tragó a sus vecinos.",
        "En Daggerfall, Sentinel era un reino gobernado por la reina Akorithi. Y su familia es para echarse a temblar.",
        "Su primogénito, Arthago, desapareció siendo niño. Se culpó a la fiebre, o al Rey Bajo Tierra. La verdad era peor: sus propios padres lo mandaron secuestrar y dejar morir en una mazmorra.",
        "Daggerfall tenía varios finales, y cada facción quería el Numidium, el gigante de latón de Tiber Septim. Akorithi lo activó para Sentinel. Pero no fue la única: otras seis potencias lo hicieron el mismo día.",
        "Y pasó algo que solo puede pasar en esta saga: todos los finales ocurrieron a la vez. Lo llaman el Milagro de la Paz, o la Distorsión del Oeste.",
        "Antes había cuarenta y cuatro ciudades estado en la bahía de Iliac. Después, cuatro. Y la que más tierra ganó fue Sentinel.",
        "[mischievously] Y aquí va el easter egg. En el Muro de Alduin, en Skyrim, la profecía dice: cuando la torre de latón camine y el tiempo se reforme. Esa torre es el Numidium. Skyrim ya te hablaba de la gran victoria de Sentinel.",
        "Guárdate esto: un juego donde el tiempo se rompió en Sentinel, y un teaser que habla de arenas del tiempo dispersas. Volveremos a ello.",
    ]},
    {"id": "p9", "frases": [
        "[deadpan] Hope, eso de la ciudad que se traga a sus vecinos lo contaste con demasiado cariño. Número nueve. Esa arena no es de cualquier desierto.",
        "El teaser abre con dunas que el viento va arrastrando. Hammerfell es la provincia del desierto de Alik'r, uno de los más duros de Tamriel.",
        "Y si jugaste Skyrim, ya conoces a su gente. Los guerreros de Alik'r que llegan a Carrera Blanca preguntando por una mujer, justo después de que mates a tu primer dragón.",
        "Ella es Saadia, la camarera de la Yegua Abanderada. Dice ser Iman, una noble de la Casa Suda, perseguida por hablar contra los Thalmor. Kematu, el jefe de los guerreros, cuenta otra historia.",
        "Y en la Hermandad Oscura tienes a Nazir, que creció en ese mismo desierto. Curiosidad: comparte cara con el Guerrero de Ébano.",
        "[deadpan] Y sí, ya sabemos que la mitad elegiste mal en la misión de Saadia. No pasa nada. En el seis igual te lo recuerdan.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, el pueblo que llegó huyendo de un continente hundido.",
        "Los redguard no son de Tamriel. Vienen de Yokuda, un continente al oeste que se hundió en el mar.",
        "Llegaron en barcos, como guerreros. La tradición los llama los Ra Gada, la ola de guerreros, y barrieron a quien vivía allí.",
        "Entre ellos estaban los Cantores de Espadas, que podían hacer aparecer una espada de la nada con la mente. La llamaban Shehai, la espada del espíritu.",
        "[amused] Un pueblo de espadachines legendarios, con magia de espada, en un desierto, junto al mar. Si Elder Scrolls seis no aprovecha eso, que lo haga un mod.",
    ]},
    {"id": "ag1", "frases": [
        "Y otra pausa, esta para dar las gracias. @menecko985 dice que están buenísimas, que no las había visto así. Y @Josedesev necesita más y más de esta maravilla. Marchando.",
        "@ImTeKah dice que por estas misiones Skyrim es legendario. [amused] Y @blinddragon9920 nos escribió: grande, esca, irim. Así, esca, irim. Tranquilo, que aquí lo decimos bien. Casi siempre.",
        "[short pause] Y aquí salgo yo, el humano tras el telón, crítico número uno de este canal. Leemos todos los comentarios: los que nos felicitan y los que nos corrigen. Y con ellos mejoramos cada video.",
        "[deadpan] Y los suyos son los más largos. Que si el video es corto, que si es largo, que si la música está alta.",
        "Porque lo estaba. [short pause] Y tú, José, menos voz de locutor, que esto no es la radio.",
    ]},
    {"id": "p7", "frases": [
        "Gracias, señor filtrador. Y José, ya puedes despertar a la gente. Número siete. La fecha del teaser, y por qué importa.",
        "La frase final del teaser va firmada con fecha: cuarta era, doscientos seis.",
        "Skyrim empieza en la cuarta era, doscientos uno. Es decir, el sacerdote que escribe esto lo hace cinco años después de que nos subieran a aquel carro rumbo a Helgen.",
        "Cinco años después de Alduin. Después de la guerra civil entre Ulfric y el general Tullius. Con los Thalmor todavía ahí.",
        "[sighs] Y ojo: la cita es de esa fecha, pero el juego podría pasar más tarde. Aun así, es la primera vez que la saga se pone después de Skyrim. Lo que hiciste en Skyrim ya es historia de Tamriel.",
    ]},
    {"id": "p6", "frases": [
        "En el seis, una reina que no conocía nadie.",
        "El sacerdote se presenta como servidor de la Alta Reina Iradne de Hammerfell.",
        "En ningún juego anterior aparece una Iradne. Es nueva. Y fíjate en el título: Alta Reina, de toda la provincia.",
        "Hammerfell casi nunca ha estado unida. Su historia es una pelea constante entre dos bandos: las Coronas, la nobleza que mira a Yokuda, y los Antepasados, los que se abrieron al Imperio.",
        "[amused] Así que, para que haya una Alta Reina, alguien ha tenido que ganar esa pelea. O alguien ha tenido que unirlos a la fuerza.",
    ]},
    {"id": "cr2", "frases": [
        "Una pausa más, que esto se está llenando. @JoseAkua nos dejó una orden muy clara: dile a la IA que revise sus fuentes, este vídeo es un despropósito.",
        "[sarcastic] Hecho. Le hemos dado el recado. Y hoy cada dato lleva su enlace en la descripción, uno por uno, para que puedas revisarlo tú también.",
        "Hasta la fecha del teaser la hemos comprobado dos veces. Cuarta era, doscientos seis. Ya lo ves: gracias a ti, el despropósito vino con bibliografía.",
    ]},
    {"id": "p5", "frases": [
        "[deadpan] Mario, respira. Ya me toca. Número cinco. La victoria que Hammerfell ganó sola.",
        "Durante la Gran Guerra, el Imperio firmó la paz con los Thalmor en el Concordato de Oro Blanco. Y a cambio, les cedió parte del sur de Hammerfell.",
        "Hammerfell no lo aceptó. Se separó del Imperio y siguió peleando. Sin legiones, sin Emperador, sola.",
        "Y ganó. Echó a los Thalmor de su tierra, y la paz quedó firmada en el Segundo Tratado de Stros M'Kai.",
        "Y no era la primera vez que los Thalmor tocaban Sentinel. En la cuarta era, cuarenta y dos, sus agentes atacaron a los refugiados altmer de la ciudad y arrasaron su barrio entero. La Noche del Fuego Verde. En Skyrim te lo cuenta el legado Fasendil.",
        "Por eso los redguard no se fían ni del Imperio ni de los elfos. Y por eso la frase del teaser escuece tanto. Dice: una victoria deshecha.",
        "[short pause] ¿Qué victoria se puede deshacer en Hammerfell? Hay una que encaja demasiado bien.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, un sacerdote que no debería estar ahí.",
        "Quien firma es Yazar, un Sacerdote de la Polilla. Son los únicos que pueden leer los Pergaminos Antiguos sin volverse locos.",
        "Su orden servía al Imperio. Los pergaminos se guardaban en la Biblioteca Imperial, en la Torre de Oro Blanco, y Dexion Evicus, el de Dawnguard, era sacerdote de esa misma torre.",
        "Pero en la cuarta era, ciento setenta y cinco, el año en que acabó la Gran Guerra, los pergaminos desaparecieron de la biblioteca. Y se dispersaron por Tamriel.",
        "Y ahora un sacerdote de la Polilla dice servir a la reina de Hammerfell, la provincia que rompió con el Imperio.",
        "[mischievously] Así que, o la orden se ha partido, o el Imperio ha caído, o Hammerfell tiene ahora algo que antes solo tenía el Emperador. Un pergamino, y alguien que sabe leerlo.",
        "[sarcastic] Un momento, que tengo notas. MariCarmen da miedo, Mario corre demasiado, y Edoardo todavía no ha sonreído en todo el video.",
        "[deadpan] Y tú llevas medio video detrás del telón sin contar ni un secreto. Vuelve a tu sitio, filtrador.",
    ]},
    {"id": "p3", "frases": [
        "Gracias, MariCarmen. Ahora, silencio. Número tres. Lo que le cuesta leer.",
        "Leer un Pergamino Antiguo tiene un precio. Cada lectura le quita a un Sacerdote de la Polilla un poco de vista, hasta que se queda ciego del todo.",
        "Algunos esperan meses entre lectura y lectura para conservar la vista. En Dawnguard lo ves con tus propios ojos: Dexion Evicus lee tres pergaminos seguidos, con prisas, y se queda ciego. Y a partir de ahí, el que tiene que leer eres tú.",
        "Para no acabar igual, en la Arboleda Ancestral le quitas la corteza a un árbol cántico, y las polillas vienen a ti.",
        "Ahora relee la frase del teaser: el pergamino solo me ofreció un destello, un velo apenas levantado ante mis ojos.",
        "[deadpan] Un destello. Un velo. Yazar no está contando una profecía. Nos está diciendo que apenas vio nada. Y que le costó caro.",
    ]},
    {"id": "campana", "frases": [
        "Antes de los dos últimos, un dato. De cada cien que ven este canal, solo trece están suscritos.",
        "Somos seis mil cuatrocientos cincuenta. Si te suscribes, llegamos a diez mil antes de que Sentinel tenga fecha. Que, viendo a Bethesda, nos da tiempo de sobra.",
    ]},
    {"id": "p2", "frases": [
        "En el dos, el pergamino del teaser no es un adorno.",
        "Cuando el viento se lleva la arena, sale un Pergamino Antiguo con los extremos dorados, una gema azul en el centro y runas que flotan a su alrededor.",
        "Los Pergaminos Antiguos son, en esta saga, fragmentos de la creación, de fuera del tiempo y del espacio. Recogen lo que pasó y lo que podría pasar. Y mientras una profecía no se cumple, lo que dicen puede cambiar de una lectura a otra.",
        "Easter egg: el fondo del pergamino que lees en Skyrim es un mapa estelar real, el del cielo sobre el polo sur de la Tierra. El mismo que en Oblivion.",
        "Y fíjate: el teaser no lo enseña guardado en una biblioteca. Lo enseña enterrado en la arena. Justo lo que pasó en el ciento setenta y cinco: perdidos y dispersos.",
        "Si The Verge acierta, este será el primer juego sobre la historia de los propios pergaminos. Bethesda, eso sí, todavía no lo ha confirmado.",
        "[amused] Llevamos treinta años jugando a The Elder Scrolls, y por fin un juego va de los Elder Scrolls. Solo nos ha costado seis entregas.",
    ]},
    {"id": "cr3", "frases": [
        "Y la última carta del día. @nyarlathotep2265 nos escribió que están mejor los vídeos del Gerber, y que de este no entendió nada.",
        "[amused] Primero: El Gerber es muy bueno, y si no lo sigues, síguelo. Sin rencores.",
        "Y segundo: para que esta vez sí se entienda, hoy hemos traído mapas, fechas y dibujos. Si aun así se te escapa algo, pregúntalo abajo y te lo explicamos despacio. Muy despacio.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. La frase entera, y lo que podría significar.",
        "El teaser termina así: un futuro perdido. Una victoria deshecha. Arenas del tiempo dispersas por el destino.",
        "Primera lectura, la política. La victoria deshecha es la de Hammerfell contra los Thalmor. Los elfos vuelven, y lo que ganaron los redguard se pierde.",
        "Segunda lectura, la del tiempo. Arenas del tiempo dispersas por el destino. Los pergaminos se dispersaron por Tamriel en el ciento setenta y cinco. Y en Sentinel ya se rompió el tiempo una vez, cuando todos los finales de Daggerfall pasaron a la vez.",
        "Un pergamino que muestra un futuro que ya no existe suena a eso mismo: a una historia que alguien ha cambiado.",
        "Tercera lectura, la más oscura. Los Thalmor no quieren solo tierras. Quieren purificar Tamriel y volver a una nueva era merética, la de antes de los hombres. Y una de las condiciones del Concordato fue prohibir el culto a Talos.",
        "Si esa es la victoria deshecha, lo que hiciste en Skyrim, la guerra civil, Alduin, todo, podría no haber servido de nada.",
        "[short pause] Todo esto es teoría. Bethesda solo nos ha dado cuatro frases. Pero son cuatro frases escritas por alguien que se está quedando ciego para leerlas. Algo vio.",
    ]},
    {"id": "cierre", "frases": [
        "Esos son los quince secretos del teaser de Sentinel, de un logo en la arena a una frase que podría deshacer Skyrim.",
        "Ahora te toca a ti. ¿Cuál de las tres lecturas te convence más? ¿La guerra, el tiempo, o los Thalmor? Déjalo en los comentarios.",
        "[sarcastic] Y ya que estás en los comentarios, vota. ¿Qué voz se queda en el canal? Johnny, Edoardo, Hope, José, Mario, MariCarmen o el Profeta. Un nombre, y listo.",
        "[amused] Hope. Con hache, que si no, no cuenta.",
        "[deadpan] MariCarmen, todo junto. Y no me hagas repetirlo.",
        "Mario. El único que no te dejó dormir.",
        "[deadpan] Edoardo. El único que se tomó esto en serio.",
        "José, con acento. Voz de locutor, y sin chistes.",
        "Yo no pido votos. Ya leí el pergamino, y sé quién gana.",
        "Y yo voto por… [short pause] ninguna. A todas les falta algo. Por eso existo.",
        "[sarcastic] Qué miedo, los dos. Y si quieres algo para la espera, en el canal tienes las quince armas más poderosas de Skyrim. Por si en el seis te toca pelear. Suscríbete si aún no lo has hecho, que hay mucha arena por delante. Nos vemos en Tamriel.",
    ]},
]

# --- VARIAS VOCES (el usuario, 3-nov-2026): quién narra cada escena; las que no salen aquí, Johnny (VOZ) ---
VOCES = {   # nombre en pantalla: voice_id (biblioteca compartida de ElevenLabs, salvo el Humano tras el Telón = clon del usuario)
    "Johnny": "HMCmDsbKeaSZp5LMOYKR", "Edoardo": "YqZLNYWZm98oKaaLZkUA", "Hope": "tnSpp4vdxKPjI9w0GnoV",
    "José": "y2ijeTfmnXjzheHO6zeN", "Mario": "tomkxGQGz4b1kE0EM722", "MariCarmen": "YDDaC9XKjODs7hY78qEW",
    "el Profeta": "HNSF1CTQmub252yhXROX", "el Humano tras el Telón": "GUEeiSJYQQdbv0NJ86Im",
}
_POR_ESCENA = {"p13": "Edoardo", "p12": "Edoardo", "p11": "Hope", "cr1": "Hope", "p10": "Hope", "p9": "José", "p8": "José",
               "ag1": "José", "p7": "Mario", "p6": "Mario", "cr2": "Mario", "p5": "MariCarmen", "p4": "MariCarmen",
               "p3": "el Profeta", "campana": "el Profeta", "p2": "el Profeta", "cr3": "el Profeta", "p1": "el Profeta",
               "cierre": "el Profeta"}
_POR_FRASE = {"voces_0": "Edoardo", "voces_1": "Hope", "voces_2": "José", "voces_3": "Mario", "voces_4": "MariCarmen",
              "voces_5": "el Profeta", "voces_6": "el Humano tras el Telón", "voces_7": "Johnny", "ag1_2": "el Humano tras el Telón",
              "ag1_4": "el Humano tras el Telón", "p4_6": "el Humano tras el Telón", "cierre_2": "Johnny", "cierre_3": "Hope",
              "cierre_4": "MariCarmen", "cierre_5": "Mario", "cierre_6": "Edoardo", "cierre_7": "José",
              "cierre_9": "el Humano tras el Telón", "cierre_10": "Johnny"}
NARRA = {}   # "escena_i": nombre de la voz (efectos.py pone la ficha de quién narra en cada cambio)
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k) or _POR_ESCENA.get(_e["id"], "Johnny")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items() if v != "Johnny"}
