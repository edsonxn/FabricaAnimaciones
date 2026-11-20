# -*- coding: utf-8 -*-
"""GUION de «Los 20 EFECTOS MANDELA de Call of Duty, parte 3» (motor SECUENCIA YT, Expediente 141, 19-nov-2026).
Plantilla: videos/cod_mandela2/ (misma fórmula). Investigación: investigacion.md (subagente, 19-nov; wiki API, arctic-shift, Whisper).
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo, PLANA (queja justa de @v5x777: nada de voz «frustrada»).
REGLA DE ORO: cada frase nombra algo que SE VE; si la voz nombra un sonido, se OYE («post» = la voz calla y suena el clip).
"""

TITULO = "Los 20 EFECTOS MANDELA de Call of Duty, parte 3"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "sigh", "annoy", "frustr"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
FONETICA = {}
# Nombres que Whisper escribe distinto (Gas, Max Amo, Shepard, Transit, Goes Riley, Pripyat, Nook Town, Nuketown por Nuk3town;
# transcripciones completas comprobadas en voz/eval.json, 19-nov) y colas > 1,0 con la frase entera (p18_2, p06_1, p11_1)
CER_MAX_POR_FRASE = {k: 0.06 for k in "p20_0 p19_0 p19_1 jesus_0 p16_1 p14_3 p11_1 p07_0 p07c_0 p02_1 p02_4 p19_2".split()}
TAIL_MAX_POR_FRASE = {"p12_0": 1.3, "p18_2": 1.2, "p06_1": 1.2, "p11_1": 1.2}

# El intruso «Turbo» = H1 (Voice Design, solo en la CUENTA 4; receta de canales/voces_prueba/energia_diseno/h1_sonidos.py)
H1 = "Ialdmnw0yv1TAYIolfxE"
VOZ["por_cuenta"] = {4: H1}
VOZ["ajustes_por_voz"] = {H1: dict(stability=0.0, tomas=3, gritos=True, sin_etiquetas=("whisper", "excit", "ecstatic", "thrilled"))}
TURBO = ["p12_1", "p12_2", "p12_3", "p12_4", "p12_5", "p12p_1"]
VOZ_POR_FRASE = {k: H1 for k in TURBO}
SONIDO_INICIAL = ["p12_1", "p12_5", "p12p_1"]
TAIL_MAX_POR_FRASE.update({k: 1.6 for k in TURBO})   # Turbo termina sus frases GRITANDO: la «cola» fuerte es a propósito   # arrancan con un sonido de boca: no se silencia

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Call of Duty", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # OST oficial (audio/ost/_catalogo.txt), nunca Lyria

# Pausas con la voz callada («si la voz nombra un sonido, se oye»):
#   p08 «Fifty thousand people used to live here…» (menú) · p08b la misma frase en la misión · p14 Reznov «…to their land» ·
#   p14b Reznov «Now it is their land» · p05 «Remember… no Russian» · p05b el doblaje japonés · p04 «Everyone hang on!»
# Comentarios (≤ 10 días, ninguno repetido): @almidon809 intro · @jesuspachano3482 tras p17 (contraburla) · @gxlfredo07 p02 ·
#   @felixhd7436 p02 (contraburla) · @rafaeltroconis6615 p01 · @papelotespro y @hildas.4222 en el cierre (agradecimiento)
ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: tu memoria. Tercera parte.",
        "Uno de ustedes me escribió que de niño un zombi lo perseguía por el Nuketown de colores. Uno solo. Y que nadie le cree.",
        "Otro jura que Mason perdonó a Menéndez, y que Black Ops 2 terminaba con Menéndez en una celda.",
        "Y alguien más me dejó esto: «estoy esperando la parte tres, a ver si es mi memoria la que falló».",
    ]},
    {"id": "intro_b", "frases": [
        "Lo revisé todo, con el juego en pantalla. Hay un helicóptero que cambió en dos mil dieciséis, una frase que en Japón decía lo contrario, y una Ray Gun que llegó antes de tiempo.",
        "Veinte efectos Mandela de Call of Duty, parte tres. Y en el número uno, Black Ops 7 te mintió en la cara.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. ¿Gaz estaba en Modern Warfare 2?",
        "Hoy Gaz es del ciento cuarenta y uno: el de la gorra, el del reinicio de dos mil diecinueve, al lado de Price, Soap y Ghost.",
        "Pero en el Modern Warfare 2 original, el de dos mil nueve, Gaz ya estaba muerto. Zakhaev lo mata con una Desert Eagle en el puente, al final de Call of Duty 4.",
        "Y aun así sale. Tres segundos, en el video de introducción, el que repasa lo que pasó en Rusia. [deadpan] Gaz no estaba en Modern Warfare 2. Solo en sus recuerdos.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, Max Ammo.",
        "La lata verde de munición que cae de un zombi, con el letrero de Max Ammo en medio de la pantalla.",
        "Mucha gente jura que siempre te llenaba también el cargador que llevabas puesto. En los zombis de World at War y en los de los tres primeros Black Ops, no lo hacía: solo llenaba la reserva.",
        "El cambio llegó con Black Ops 4, en dos mil dieciocho. [short pause] Por eso hay veteranos que todavía recargan antes de agarrarla. El juego cambió. La costumbre, no.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. La nuke de Call of Duty 4.",
        "Veinticinco bajas sin morir, una cuenta atrás de diez segundos, y el mapa entero se pone blanco.",
        "Si tú la pones en Call of Duty 4, mira sus rachas: tres bajas para el UAV, cinco para el ataque aéreo, siete para el helicóptero. Y ahí se acaba la lista.",
        "La nuke táctica nació en Modern Warfare 2, en dos mil nueve. Lo que tenía Call of Duty 4 era una bomba nuclear en la campaña. [deadpan] Y tu memoria la metió en el multijugador.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, un caso abierto. El hombre del menú de Black Ops.",
        "El menú de Black Ops, dos mil diez: el cuarto de interrogatorio, las teles, la silla, y alguien detrás del cristal.",
        "Unos juran que al entrar en Zombies, un zombi aparecía y se comía al hombre de la ventana. Otros dicen que el hombre sale de la sala, y vuelve golpeando el cristal.",
        "Yo entré a ese menú, y lo que veo son las teles. [short pause] Este expediente se queda abierto. Si tienes la grabación, ya sabes dónde mandarla.",
    ]},
    {"id": "jesus", "frases": [
        "Antes de seguir, una corrección del público. Jesús escribió que el de Shepherd en la parte uno está raro, que todos sabemos que Shepherd mata a Ghost, que es icónico.",
        "Tienes toda la razón, Jesús. Lo sabemos todos. Todos menos los miles que escribieron que fue Makárov. [short pause] Felicidades: tu memoria funciona. Quédate un rato más, a ver cuánto te dura.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. Speed Cola en el balcón.",
        "TranZit, Black Ops 2: el autobús, la niebla, y la granja con su granero rojo.",
        "Hay quien recuerda la máquina de Speed Cola en el balcón de la granja, arriba, junto al granero rojo.",
        "Pero en TranZit, arriba del granero, la máquina es de Double Tap. La Speed Cola de la granja existe, pero en otro modo, el de Supervivencia, y abajo, dentro de la casa. [deadpan] Dos mapas en el mismo sitio. Una sola granja en tu cabeza.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, la carne.",
        "Uno de los recuerdos más raros de Black Ops 2: un trozo de carne cruda que lanzabas, y todos los zombis se iban detrás de él, como con el mono, pero sin explosión.",
        "Quien lo cuenta pregunta si se lo inventó. Y no. Existe. Se llama Zombie Flesh, y solo sale en el modo Grief, el de dos equipos contra los zombis.",
        "Se la tiras a un rival, y los zombis lo persiguen treinta segundos. [short pause] Esta vez la memoria no mintió. Solo nadie más jugaba Grief.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. Extinction no era de Battlefield.",
        "Cuatro jugadores, un taladro, y unos aliens enormes llamados Cryptids, saliendo del suelo.",
        "Hay quien jura que Extinction era el modo de Battlefield 4, su respuesta a los zombis de Call of Duty.",
        "Es de Call of Duty: Ghosts, dos mil trece, de Infinity Ward. [deadpan] El único modo de aliens de la saga. Y se lo regalaste a la competencia.",
    ]},
    {"id": "p13", "post": 5.8, "frases": [
        "En el trece, la frase de Reznov.",
        "En el World at War del año dos mil ocho, Viktor Reznov, el sargento del Ejército Rojo, en Stalingrado, entre las ruinas. Muchos recuerdan una sola frase. Escucha la primera parte.",
    ]},
    {"id": "p13b", "post": 5.1, "frases": [
        "Eso es en Stalingrado, en la primera misión. Y la segunda parte llega años después, ya en Alemania, en la misión que lleva su nombre.",
    ]},
    {"id": "p13c", "frases": [
        "Su tierra, su gente, su sangre. Son dos frases, en dos misiones, con años de guerra en medio. [short pause] Y tu memoria las juntó en un solo discurso.",
    ]},
    # PRUEBA DEL INTRUSO (el usuario, 19-nov-2026): «Turbo» (voz H1 de Voice Design, cuenta 4) le arrebata el micrófono a Damián,
    # narra el puesto 12 con LOS MISMOS datos verificados (investigacion.md § 12) y se pelean 10-15 s. Gritos y resoplidos SOLO en
    # sus frases (VOZ["ajustes_por_voz"], excepción a SIEMPRE_FUERA); Damián sigue plano. 19-nov, 2.ª toma: el usuario quiere UN
    # solo resoplido de cerdo (fuera caballo/jabalí/toro) y más gritón y enérgico (stability 0.0 ya es el máximo de ElevenLabs). Pregunta al público: ¿se queda el intruso?
    {"id": "p12", "frases": [
        "Número doce. El modo de una sola bala. Black Ops, dos mil diez, las partidas de...",
        "[inhales sharply through the nose] ¡DAME ESO, DAME ESO! [shouts] ¡SUÉLTALO! [clears throat loudly] Ya, ya. [laughs] ¿Qué es esto, un funeral? ¡HOLA, BANDA! [shouts] ¡AHORA NARRO YO!",
        "Black Ops, dos mil diez, ¡las partidas de apuestas! [snorts like a pig] ¡El modo se llamaba One in the Chamber, señores! Te dan una pistola... ¡UNA BALA! [shouts] ¡UNA! Y un cuchillo. ¡Y YA! [laughs] ¡Suerte, campeón!",
        "Y la gente... [inhales loudly and ugly] ¡LA GENTE JURA que era un todos contra todos a treinta bajas, SIN VIDAS! [shouts with a raspy voice] ¡Revives, revives, revives, PARA SIEMPRE! [laughs]",
        "¡MENTIRA! [screams hoarsely] ¡TRES VIDAS! [coughs] [clears throat] ¡Desde el primer día, banda! Te mueres tres veces y te vas a mirar la partida desde afuera... [laughs harder] ¡LLORANDO!",
        "[laughs harder] Una bala, tres vidas. [shouts] ¡Y TU MEMORIA TE DIO INFINITAS! [wheezes]",
    ]},
    {"id": "p12p", "frases": [
        "[deadpan] ¿Ya terminaste? Gracias. Fue como escuchar una licuadora con conexión a internet.",
        "[groans] Ya, ya, toma tu micrófono, abuelo. [shouts] ¡PERO ME VAN A EXTRAÑAR! [laughs] ¡COMENTEN SI ME QUEDO!",
        "[deadpan] No lo hagan. [short pause] Sigamos.",
    ]},
    {"id": "p11", "frases": [
        "En el once, la bufanda de Ghost.",
        "Simon Ghost Riley, Modern Warfare 2, dos mil nueve: el pasamontañas de calavera, las gafas, los auriculares.",
        "Media generación lo recuerda con una bufanda de cuadros blancos y negros al cuello. Uno lo descubrió en una foto suya, disfrazado de niño.",
        "En ninguna misión del original la lleva. La bufanda salió de los disfraces y de las fotos de los fans. [deadpan] Te disfrazaste de un Ghost que nunca existió.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. Los dos capitanes Price.",
        "Bigote enorme, boina, la Segunda Guerra Mundial. El Capitán Price de Call of Duty 1 y 2.",
        "Mucha gente cree que es el mismo Price de Call of Duty 4, el del gorro militar. Hay hasta quien dice que los alemanes lo hicieron inmortal.",
        "No es el mismo. El Price de la Segunda Guerra muere en mil novecientos cuarenta y cuatro, saboteando el acorazado Tirpitz, en la última misión británica del primer juego.",
        "¿Son familia? Nunca se confirmó. [short pause] Lo único seguro es que el bigote se heredó.",
    ]},
    {"id": "p09", "frases": [
        "En el nueve, el poste de Piccadilly.",
        "Modern Warfare, dos mil diecinueve. Piccadilly, en Londres: los autobuses rojos de dos pisos, y un semáforo entre ellos.",
        "En abril de dos mil veinte, medio Call of Duty juró que ese poste era nuevo. Hasta un jugador profesional dijo que nunca había tenido que esquivarlo.",
        "El poste estaba desde el principio. Sale en las partidas del lanzamiento, y en el tráiler de seis meses antes. [deadpan] El letrero de Standoff tiene un primo en Londres.",
    ]},
    {"id": "p08", "frases": [
        "Número ocho. La tercera arma en el primer mapa.",
        "El mapa donde empezó todo, con la casa en ruinas, las ventanas con tablas y la caja misteriosa.",
        "Unos juran que en Nacht no había ni una sola perk. Otros, que tenía Mule Kick, la máquina verde de la tercera arma.",
        "Los dos tienen razón. En World at War, ninguna. En Black Ops, un parche de dos mil once puso Mule Kick en la sala del principio. Pero solo si estabas conectado a internet. [deadpan] Sin conexión, tu Nacht no tenía perks. Con conexión, sí. Mismo mapa. Dos memorias.",
    ]},
    {"id": "p07", "post": 5.3, "frases": [
        "En el siete, la frase de Prípiat.",
        "Call of Duty 4, All Ghillied Up. El capitán MacMillan y Price, con trajes de camuflaje, cruzan la ciudad abandonada de Chernóbil. Y MacMillan dice algo que todos citan. Así suena en el menú del juego.",
    ]},
    {"id": "p07b", "post": 5.1, "frases": [
        "Cincuenta mil, no cuarenta y cinco mil, como recuerdan muchos. Y sin palabrota. Y esa versión es la del video del menú, la que ves antes del título. En la misión es otra. Escucha.",
    ]},
    {"id": "p07c", "frases": [
        "«En esta ciudad». Y la palabrota que tantos le ponen ni siquiera es suya: es del general Shepherd, en Modern Warfare 2. [short pause] Dos juegos, dos personajes. Una sola frase en tu cabeza.",
    ]},
    {"id": "p06", "frases": [
        "Número seis. El mapa soleado que no existe.",
        "Hay quien recuerda un mapa de Zombies de día, soleado, con campos de hierba, bosques y pueblitos, y un portal que te llevaba a otra zona. Su amigo no tenía ni idea. Y en internet no lo encontraba.",
        "Ese mapa existe. Se llama Outbreak, y es de Black Ops Cold War: Zombies en los mapas abiertos, como el pueblo de Golova, en pleno otoño.",
        "Él ni siquiera tenía Cold War: lo jugó un fin de semana de prueba gratis. [deadpan] Un fin de semana. Y años buscándolo.",
    ]},
    {"id": "p05", "frases": [
        "En el cinco, la Ray Gun Mark II.",
        "La Ray Gun de tres disparos, la de Black Ops 2. Mucha gente la recuerda en la caja desde el primer día, en noviembre de dos mil doce.",
        "Llegó ocho meses después, con el paquete Vengeance y el mapa Buried, en julio de dos mil trece.",
        "Pero hay un detalle. Unos días antes, un parche la coló por error en todos los mapas, y la quitaron enseguida. [short pause] Si la sacaste de la caja antes de tiempo, no lo soñaste. Fuiste testigo de un error.",
    ]},
    {"id": "p04", "post": 3.4, "frases": [
        "Número cuatro. La frase del ascensor.",
        "Modern Warfare 2, el ascensor del aeropuerto. Makárov carga su arma y dice la frase más famosa de la saga.",
    ]},
    {"id": "p04b", "post": 2.8, "frases": [
        "Mucha gente entendió «que no quede ningún ruso vivo». Significa otra cosa: nada de ruso. No hablen ruso. Que parezca un ataque de estadounidenses. Y en el doblaje japonés, la frase salió así.",
    ]},
    {"id": "p04c", "frases": [
        "«Mátenlos, son rusos». Justo lo contrario. Se corrigió once años después, en la versión remasterizada.",
        "Y otro detalle: la misión no te obliga a disparar. Tu único objetivo es seguir a Makárov. [deadpan] El juego nunca te lo pidió. Fue tu memoria.",
    ]},
    {"id": "p03", "post": 2.6, "frases": [
        "En el tres, el brazo de Jackson.",
        "Call of Duty 4, Shock and Awe. Explota la bomba, el helicóptero se ladea, y el teniente Volker sale volando por la rampa.",
        "Muchos recuerdan al sargento Jackson estirando el brazo para salvarlo. Otros juran que no hace nada. Mira el original, de dos mil siete.",
    ]},
    {"id": "p03b", "frases": [
        "Ni un gesto. Ahora el remasterizado, de dos mil dieciséis. Ahí Jackson sí estira el brazo.",
        "Los dos bandos tienen razón. Solo jugaron juegos distintos. [short pause] Infinity Ward le dio a Jackson nueve años después lo que tu memoria le dio desde el principio.",
    ]},
    {"id": "p02", "frases": [
        "Número dos. Este viene de los comentarios.",
        "Dice que de niño jugaba en el Nuketown normal, el colorido de Black Ops 1, con un solo zombi que lo seguía por todo el mapa.",
        "Primero lo malo: el Nuketown de Black Ops 1 nunca tuvo zombis. Su secreto era otro: volarles la cabeza a todos los maniquíes, uno por uno, por toda la colonia.",
        "Pero no te lo inventaste. En Black Ops 4 está Alpha Omega: Nuketown antes de la bomba, con sus casas de colores y su sol. Si les cortas la cabeza a los maniquíes robot, aparece uno solo, que te sigue por todo el mapa. Y se congela cuando lo miras.",
        "Y en Black Ops 3, en Nuk3town, los maniquíes también cobran vida y te persiguen. [short pause] Un Nuketown brillante, y un maniquí que te sigue. Lo viste. Solo que no era Black Ops 1.",
        "Félix tiene una teoría para todo esto: posiblemente los mods afectan a los recursos. Puede ser, Félix. Pero aquí no hizo falta ningún mod. Treyarch lo metió dos veces. [deadpan] El único mod de esta historia es la memoria.",
    ]},
    {"id": "p01", "frases": [
        "Y el número uno. Menéndez en la celda.",
        "Este me lo mandó Rafael: antes de Black Ops 7, juraba que Mason había perdonado a Menéndez, y que Black Ops 2 terminaba con él encerrado en prisión.",
        "Primera sorpresa: ese final existe. En la última misión, el que decide no es Alex, es su hijo, David Mason. Si le perdonas la vida, se lo llevan detenido, y un año después lo ves en su celda, con el uniforme naranja, mirando la tele.",
        "Segunda sorpresa: no es el oficial. En la línea de tiempo oficial de Treyarch, Menéndez muere el diecinueve de junio de dos mil veinticinco, al intentar escapar. Y lo mata el mismo David que lo había perdonado.",
        "Y la tercera: Black Ops 7 lo trae de vuelta. Menéndez sale amenazando al mundo otra vez, diez años después. Y no es él. Es un deepfake, una inteligencia artificial que imita su cara y su voz.",
        "[short pause] Tú no te inventaste ese final, Rafael. Lo que se inventaron fue a Menéndez.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. Veinte efectos Mandela, y otra vez, varios me los dieron ustedes.",
        "Todos los comentarios se leen, y se toman en cuenta para el siguiente expediente. Como el de papelotes, que dice que sigamos así. O el de Hilda, que lo dijo todo con dos confetis.",
        "Ahora te toca a ti: ¿qué recuerdas de Call of Duty que nadie más recuerda? Escríbelo. Si es bueno, sale en la parte cuatro.",
        "En el canal tienes la parte uno, la parte dos, y cómo murió de verdad cada villano de la saga. Suscríbete. [short pause] Retírate, soldado.",
    ]},
]
