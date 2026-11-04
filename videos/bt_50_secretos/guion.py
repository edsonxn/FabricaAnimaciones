# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Los 50 SECRETOS de Banjo-Tooie QUE IGNORASTE» (3-nov-2026, ~25 min).
Pedido del usuario: video de Banjo-Tooie de ~25 min; eligió «50 secretos» entre 3 ángulos, en UNA sola sesión y viendo solo el MASTER.
Cuarto video de Banjo-Tooie del canal (banjo_tooie ×2,46 = el mejor largo; bt_jiggies_crueles; bt_mundos_ranking). Variable que cambia:
SOLO el número de secretos (10 → 50) y la duración. Nada de lo ya contado en esos 3 (lista «YA USADO» en investigacion_secretos.md).
Motor SECUENCIA YT, voz ElevenLabs Hope, música = OST del juego (audio/ost → junction a la de bt_mundos_ranking; armar_musica_ost.py),
SFX del juego (sfx/bt_*.mp3), kit mg_banjo. Datos: investigacion_secretos.md (S## = ficha; sellos ✅/⚠ y fuentes).
⚠ dichos con «según…»: S46 (los 3 nombres del concurso), S47 (delfín), S45 (Cockeye), S15 (cerdo japonés), S26 (detalles del castillo),
S30 (cita de Grunty's Lair en el tema de la Hag 1). Comprobar EN CUADRO antes de dar por bueno: S25 (letrero), S29 (placa GB),
S18 (la línea de Mario), S42 (papel tapiz), S38 (sombra del dragón), S27 (Jiggywiggy).
NO decir: cifra de ventas; voz de Jamjars = R. Lee Ermey (es el mito que se desmonta); nada de Edsonxn (el niño de Dream se llamaba Edson).
"""

TITULO = "Los 50 SECRETOS de Banjo-Tooie QUE IGNORASTE"
ARCHIVO = "bt_50_secretos"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
# Sin [whispers] ni [excited] en ninguna voz (el usuario, 2-nov-2026): sin_etiquetas los quita aunque se cuelen.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"))
# ElevenLabs dice el inglés nativo; solo lo que leería mal
FONETICA = {"Hag 1": "Hag One", "V10": "uve diez", "3D": "tres de", "E3": "E tres", "Nuts & Bolts": "Nuts and Bolts"}
# hablan hasta el final y la transcripción termina bien (revisado el 3-nov)
TAIL_MAX_POR_FRASE = {'intro_0': 1.17, 'mitad_1': 1.16, 'cierre_0': 1.11}
# 3-nov: falsas alarmas de Whisper (cifras en dígitos: «49», «2000»; nombres: «Hellfire», «Kirk Hope», «Greg Males», «Cole»,
# «Pauno», «Clumbo», «Sevaste»); comparadas palabra a palabra con textos.json: se aceptan con la CER de la toma + .0015
CER_MAX_POR_FRASE = {'s49_0': 0.0443, 's49_1': 0.0376, 's48_0': 0.0519, 's47_0': 0.0459, 's46_0': 0.0495, 's45_0': 0.0646, 's44_0': 0.0418, 's43_0': 0.0472, 's43_1': 0.0218, 's42_0': 0.0551, 's42_1': 0.0321, 's41_0': 0.0595, 's41_1': 0.0289, 's40_0': 0.0758, 's40_1': 0.0159, 's39_0': 0.0537, 's38_0': 0.0586, 's37_0': 0.0593, 's37_1': 0.0368, 's36_0': 0.0376, 's35_0': 0.0674, 's34_0': 0.0658, 's33_0': 0.0756, 's32_0': 0.0362, 's31_0': 0.036, 's30_0': 0.0466, 's29_0': 0.0615, 's29_1': 0.0199, 's28_0': 0.045, 's27_0': 0.037, 's26_0': 0.0674, 's25_0': 0.0395, 's24_0': 0.0807, 's23_0': 0.0523, 's22_0': 0.1057, 's21_0': 0.0429, 's20_0': 0.0669, 's19_0': 0.0688, 's18_0': 0.063, 's18_1': 0.0138, 's18_2': 0.0305, 's17_0': 0.063, 's16_0': 0.0488, 's15_1': 0.053, 's14_0': 0.0328, 's13_0': 0.0466, 's12_0': 0.0444, 's12_2': 0.0663, 's10_0': 0.0339, 's09_0': 0.0627, 's08_0': 0.0537, 's07_0': 0.0854, 's06_0': 0.037, 's05_1': 0.0147, 's04_0': 0.067, 's04_1': 0.0278, 's03_0': 0.0487, 's02_0': 0.0503, 's02_1': 0.0211}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    ambiente_por={'scene-018': 0.9, 'scene-032': 0.8, 'scene-033': 0.7, 'scene-041': 0.5, 'scene-042': 0.7, 'scene-055': 0.6, 'scene-056': 0.9, 'scene-058': 0.5, 'scene-061': 0.7, 'scene-069': 0.8, 'scene-070': 0.8, 'scene-072': 0.8, 'scene-073': 0.5, 'scene-074': 0.5, 'scene-078': 0.8, 'scene-079': 0.9, 'scene-080': 0.7, 'scene-102': 0.5, 'scene-104': 0.5, 'scene-105': 0.5, 'scene-107': 0.5, 'scene-114': 0.5, 'scene-115': 0.5, 'scene-121': 0.5, 'scene-127': 0.5, 'scene-128': 0.5, 'scene-138': 0.5, 'scene-139': 0.5, 'scene-140': 0.5, 'scene-155': 0.8},   # plan_clips.py (3-nov)
    recorte_por={'scene-063': 0.144, 'scene-001': (0, .04, 0, .27), 'scene-064': (0, .04, 0, .30), 'scene-167': (0, .04, 0, .30), 'scene-168': (0, .08, 0, .19), 'scene-169': (0, .08, 0, .19), 'scene-146': (.27, 0, 0, 0), 'scene-156': (.125, 0, .125, 0), 'scene-100': (0, .035, 0, 0)},   # sin marca de Censored Gaming ni panel LiveSplit (3-nov)
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 60
# Sin Lyria: banda sonora del juego (audio/ost, armar_musica_ost.py -> audio/musica.wav).

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En Japón, Banjo-Tooie tiene otro final. La cabeza de la bruja Gruntilda desaparece, y la cambian por un saco. [short pause] Y aun así, cuando la patean, se le sale el ojo.",
        "[amused] Hay un cartucho que le pregunta a la consola doscientas sesenta y ocho veces si eres un pirata. Un jefe que tenía demasiados huesos. [short pause] Y una montaña que Rare jura que salió así por accidente.",
        "[sarcastic] Ya te contamos su historia, sus Jiggies más crueles y sus ocho mundos. Creías que no quedaba nada. [short pause] Quedan cincuenta. Y algunos ni siquiera se ven en tu versión.",
        "[playful] Estos son los cincuenta secretos de Banjo-Tooie que ignoraste. Del más curioso al que de verdad no te esperas. Empezamos.",
    ]},

    # ================================================================ 50 → 41
    {"id": "s50", "post": 0.6, "frases": [   # S48
        "Número cincuenta. Banjo-Tooie da por hecho que ya jugaste el primero. Empiezas en Spiral Mountain con todos los movimientos de Banjo-Kazooie desde el minuto uno, y solo el fantasma de Bottles te los recuerda.",
        "[deadpan] Steve Malpass, uno de sus diseñadores, lo explicó así: ¿quién iba a empezar una saga por el segundo juego? [short pause] Una revista japonesa se quejó justo de eso: demasiados movimientos para alguien nuevo.",
    ]},
    {"id": "s49", "post": 0.6, "frases": [   # S28
        "Cuarenta y nueve. Cuando llamas al tren Chuffy desde una estación, Old King Coal, el rey que vive en su caldera, te dice qué está haciendo: cargando mineral, disfrutando de las atracciones, o calentando sus carbones en el lado de lava.",
        "[amused] Y si lo llamas desde la estación donde ya está, te contesta: ¿estás ciego? ¡Chuffy está justo delante de ti!",
    ]},
    {"id": "s48", "post": 0.6, "frases": [   # S43
        "Cuarenta y ocho. En los archivos del juego, la animación de disparar huevos hacia delante se llama egg head, cabeza de huevo. [short pause] Y la de dispararlos hacia atrás se llama egg ass.",
        "[amused] O sea: huevo culo. Y Japón se lo tomó al pie de la letra: en Smash Ultimate, ese ataque de Banjo y Kazooie se llama, literalmente, huevo del trasero.",
    ]},
    {"id": "s47", "post": 5.0, "frases": [   # S32 · SE OYE Atlantis
        "Cuarenta y siete. De toda la banda sonora, la canción favorita de Grant Kirkhope, el compositor, está bajo el agua. Es Atlantis, la ciudad hundida de Jolly Roger's Lagoon.",
        "Él mismo dice que resume lo que se siente al bajar ahí. Escúchala un momento.",
    ]},
    {"id": "s46", "post": 0.6, "frases": [   # S25
        "Cuarenta y seis. Al llegar a Cauldron Keep, la guarida final de la bruja, a la derecha de la entrada hay un letrero: Cauldron Keep Secret Exit. [short pause] Salida secreta.",
        "[sarcastic] O sea, Banjo y Kazooie asaltan el castillo de la villana entrando por la puerta de atrás. La entrada principal nunca la llegamos a ver.",
    ]},
    {"id": "s45", "post": 0.6, "frases": [   # S17
        "Cuarenta y cinco. En casa de Bottles, en Jinjo Village, su hijo Speccy lleva una gorra con el símbolo de la de Ash, el de Pokémon, pero al revés.",
        "Y en la casa cuelgan pósters de Juno y Vela, los héroes de Jet Force Gemini, otro juego de Rare.",
        "[amused] Una gorra de Pokémon en un juego de Rare, que siguió ahí incluso en la versión de Xbox, cuando Rare ya era de Microsoft.",
    ]},
    {"id": "s44", "post": 0.6, "frases": [   # S50
        "Cuarenta y cuatro. Cuando Banjo va solo y usa su mochila, como el Shack Pack o el Taxi Pack, hay un truco de magia. Steve Mayles, el animador, no podía animar la mochila que lleva a la espalda.",
        "Así que, en un cuadro concreto, esa mochila se apaga, y aparece otra idéntica en el mismo sitio. [short pause] Esa sí se mueve. Nunca lo notaste, porque dura un parpadeo.",
    ]},
    {"id": "s43", "post": 0.6, "frases": [   # S46 ⚠
        "Cuarenta y tres. En el video de los Jiggies te contamos que el nombre de Chris P. Bacon salió de un concurso. No fue el único. La revista oficial de Nintendo en el Reino Unido dejó que sus lectores bautizaran personajes.",
        "[amused] Según VGFacts, de ahí salen también Old King Coal, el del tren, y Bullion Bill, el de la cabaña de Glitter Gulch Mine. El premio: el juego, un póster firmado, y tu nombre dentro de un cartucho.",
    ]},
    {"id": "s42", "post": 2.5, "frases": [   # S24 · SE OYE el cambio de música
        "Cuarenta y dos. Al entrar en el Gatehouse de Cauldron Keep, Banjo dice que ahí no hay nadie. Y Kazooie le responde con algo muy de videojuego.",
        "Oh, sí que hay alguien. La música ha cambiado. Cada vez que pasa eso, acabamos peleando. [short pause] Y en ese momento, Klungo cae del techo.",
    ]},
    {"id": "s41", "post": 0.6, "frases": [   # S51 ⚠ teoría
        "Cuarenta y uno. Una teoría de los fans: el contorno de Isle O' Hags imita el icono de vida de Banjo-Kazooie. A la izquierda, la cabeza de Banjo. A la derecha, parte de la de Kazooie.",
        "[deadpan] Rare nunca lo confirmó. Te lo enseño encima del mapa, y tú decides si es diseño o casualidad.",
    ]},

    # ================================================================ 40 → 31
    {"id": "s40", "post": 0.6, "frases": [   # S37
        "Cuarenta. Los huevos misteriosos del primer juego por fin se abren aquí, en el gallinero de Heggy, en Wooded Hollow. El rosa te da el Breegull Bash: Banjo agarra a Kazooie y la usa de mazo.",
        "El azul, un truco de huevos que persiguen a los enemigos. Y el amarillo, un Jinjo jugable en el multijugador. [amused] Al incubarlo, Heggy, la gallina, pregunta muy seria: ¿quién es Jinjo?",
    ]},
    {"id": "s39", "post": 0.6, "frases": [   # S29 (placa: comprobar en cuadro)
        "Treinta y nueve. La Hag 1, la perforadora gigante de las brujas, lleva detrás una matrícula con las letras G y B, de Gran Bretaña, el país de Rare.",
        "En la pelea final, Grunty presume de motor: siente la potencia de esa bestia V10. [short pause] Y en el concurso te pregunta qué pone en la matrícula de su encantadora perforadora.",
    ]},
    {"id": "s38", "post": 0.6, "frases": [   # S49
        "Treinta y ocho. Todo el juego lo diseñaron solo dos personas: Gregg Mayles y Steve Malpass. Primero inventaban las tareas, luego hacían los mundos a su medida, y todo en papel.",
        "Para colocar notas, cámaras y disparadores usaban un editor dentro del propio juego, manejado con un mando de Nintendo 64. La cámara del Saucer of Peril, en Witchyworld, se trazó así, curva a curva. [deadpan] Malpass dice que la odia y la adora a partes iguales.",
    ]},
    {"id": "s37", "post": 0.6, "frases": [   # S45 ⚠
        "Treinta y siete. Pawno, el usurero de Jolly Roger's Lagoon, viste la ropa del Capitán Cockeye, un pirata medio científico loco pensado para Dream, el juego de Rare que nunca salió y acabó convertido en Banjo-Kazooie.",
        "Lo contó Ed Bryan, el que diseñó a los personajes. [amused] Pawno no te presta nada gratis, pero el traje sí lo heredó.",
    ]},
    {"id": "s36", "post": 0.6, "frases": [   # S20
        "Treinta y seis. En Xbox 360 hasta el examen de la bruja cambió. En Nintendo 64, el concurso pregunta cuántos botones tiene un mando oficial de Nintendo. La respuesta es diez.",
        "[sarcastic] En Xbox, con Rare ya en Microsoft, la pregunta pasó a ser por el mando de Xbox 360, con trece. Y de paso le cambiaron la letra a todos los textos del juego.",
    ]},
    {"id": "s35", "post": 5.0, "frases": [   # S31 · SE OYE la isla (respiro 1)
        "Treinta y cinco. La música de Isle O' Hags es la guarida de Grunty disfrazada. Kirkhope le dio el mismo compás de seis por ocho que Grunty's Lair, el castillo del primer juego, para que fuera el hilo entre los dos.",
        "Y dice que en Banjo-Tooie no tuvo que rehacer nada: todas fueron sus primeras ideas. Escucha ese compás.",
    ]},
    {"id": "s34", "post": 0.6, "frases": [   # S47 ⚠ teoría
        "Treinta y cuatro. En Hailfire Peaks descongelas a Sabreman, el explorador de los primeros juegos de Ultimate, y lo llevas a su tienda en el lado de lava. Y ahí divaga sobre lo mucho que le gustaría montar un delfín.",
        "[mischievously] Dolphin, delfín, era el nombre en clave de la GameCube, la consola que Nintendo preparaba ese año. Según VGFacts, puede ser un guiño. Rare nunca lo confirmó.",
    ]},
    {"id": "s33", "post": 2.5, "frases": [   # S36 · SE OYE el conjuro
        "Treinta y tres. Lo que murmura Mumbo al hacer sus hechizos está escrito en el suelo. En los costados de los Mumbo Pads pone: Eekum Bokum.",
        "Y esa voz no es de un actor: es del propio compositor, Grant Kirkhope.",
    ]},
    {"id": "s32", "post": 0.6, "frases": [   # S14
        "Treinta y dos. Rare es un estudio británico, pero Europa fue la última en jugarlo. Salió en Norteamérica el veinte de noviembre del dos mil, en Japón una semana después, [short pause] y en Europa no llegó hasta abril del dos mil uno.",
        "En Japón, además, se llama La gran aventura de Banjo y Kazooie 2.",
    ]},
    {"id": "s31", "post": 0.6, "frases": [   # S26
        "Treinta y uno. Ya te contamos que el último mundo se recortó. Lo nuevo es cómo era. En los dibujos que enseñó Gregg Mayles, Cauldron Keep era un castillo de piedra a medio convertir en fortaleza de metal, con un cementerio detrás y cañones en las almenas.",
        "Según la wiki del juego, había también una cripta con una fantasma, una armadura embrujada, y una semilla que Mumbo hacía crecer hasta Cloud Cuckooland. Del castillo grande quedaron restos: la reja de láser y el foso de ácido morado.",
    ]},

    # ================================================================ 30 → 21
    {"id": "s30", "post": 2.5, "frases": [   # S35 ⚠ · SE OYE la cadencia
        "Treinta. Jamjars, el hermano militar de Bottles, enseña cada movimiento con una cadencia de marcha que rima con los botones del mando de Nintendo 64.",
        "[amused] Según la wiki, en Xbox el botón de ataque dejó de ser la B, y varias de sus canciones se quedaron sin rima.",
    ]},
    {"id": "s29", "post": 2.5, "frases": [   # S21 · SE OYEN los abucheos
        "Veintinueve. En el concurso Tower of Tragedy, el público aplaude a las hermanas de Grunty, y abuchea a Banjo aunque acierte.",
        "[amused] Si nadie acierta, Grunty suelta: estoy rodeada de imbéciles, casi la frase de Scar en El rey león. Y presenta así a los concursantes: conozcamos a las víctimas de esta noche… [short pause] eh, quiero decir, concursantes.",
    ]},
    {"id": "s28", "post": 0.6, "frases": [   # S33
        "Veintiocho. Kirkhope tuvo que dejar Banjo-Tooie a medias dos veces. Empezó la música, pero le pidieron Donkey Kong 64, y luego Perfect Dark, que salían antes.",
        "Y a mitad del desarrollo, Rare se mudó a su nueva sede, una milla más abajo. [short pause] Según Kirkhope, toda la empresa se mudó en un solo día.",
    ]},
    {"id": "s27", "post": 5.0, "frases": [   # S30 ⚠ · SE OYE el tema de la Hag 1
        "Veintisiete. La música del jefe final esconde otra canción. Según la wiki del juego, el tema de la Hag 1 es en parte una variación de Grunty's Lair, la del primer juego, metida debajo del motor de la perforadora.",
        "Escúchala.",
    ]},
    {"id": "s26", "post": 0.6, "frases": [   # S34
        "Veintiséis. Mucha gente jura que la voz de sargento de Jamjars es de R. Lee Ermey, el de La chaqueta metálica. [short pause] Falso.",
        "Es de Grant Kirkhope, el compositor, que también pone las voces de Mumbo, del rey Jingaling y de los Jinjos. Y su nombre es un insulto: en el primer juego, Kazooie le grita a Bottles jam jars, que en inglés británico es como llamar a alguien cuatro ojos.",
    ]},
    {"id": "mitad", "post": 0.8, "frases": [   # respiro 2 · agradecimientos (comentarios reales)
        "[warm] Llevamos veinticinco. Antes de seguir: leemos todos sus comentarios, y los tomamos en cuenta para mejorar. Como el de Riuma, que nos contó que nunca sacó la máscara de la Fiera Deidad, y que fue su hermano quien le habló de ella.",
        "O el de Antilope, que nos recordó lo triste que es la historia del héroe del tiempo. Gracias por escribir. Y si conoces un secreto de Banjo-Tooie que no esté en esta lista, déjalo abajo.",
    ]},
    {"id": "s25", "post": 0.6, "frases": [   # S11
        "Veinticinco. Los warp pads, las baldosas que te teletransportan dentro de cada mundo, se metieron casi al final. Los mundos ya estaban diseñados, y los probadores se quejaban de tanto ir y volver.",
        "Según Steve Malpass, ya era tarde para simplificar el juego. Y la gran inspiración para arreglarlo fue Ocarina of Time.",
    ]},
    {"id": "s24", "post": 0.6, "frases": [   # S38 (sombra: comprobar en cuadro)
        "Veinticuatro. Cuando Kazooie se convierte en dragón, en Hailfire Peaks, su sombra la delata. Sigue teniendo forma de pájaro.",
        "Según la wiki, su retrato al hablar no cambia, y en las escenas del final vuelve a salir la Kazooie de siempre. [amused] Y los colores casi se invierten: la normal es roja con ojos verdes, y la dragón, verde con ojos oscuros.",
    ]},
    {"id": "s23", "post": 0.6, "frases": [   # S19
        "Veintitrés. El concurso de Grunty está lleno de trampas de Rare. Una pregunta: ¿en qué juego apareció Banjo por primera vez? Y no, no es Banjo-Kazooie.",
        "Es Diddy Kong Racing, de mil novecientos noventa y siete. La opción falsa es Super Banjo Land 64. [laughs softly] Y hay respuestas de broma como Perfect Grunty, o Grunty Kong 64.",
    ]},
    {"id": "s22", "post": 0.6, "frases": [   # S44
        "Veintidós. Del Stomponadon, el dinosaurio de Terrydactyland, solo ves el pie. Y ese pie viene del juego que nunca salió.",
        "En Dream, el proyecto de Rare que acabó siendo Banjo-Kazooie, al protagonista lo iba a perseguir un dinosaurio gigante que intentaba aplastarlo con las patas. Rare enseñó esas imágenes en dos mil quince.",
    ]},
    {"id": "s21", "post": 0.6, "frases": [   # S16
        "Veintiuno. En casa de Bottles, su hija Goggles juega con un peluche de Donkey Kong. En la versión de Xbox, con Rare ya en Microsoft, le quitaron la corbata y le pusieron ojos saltones.",
        "[sarcastic] En el concurso, la respuesta Donkey Kong pasó a ser: un gorila adorable. Y en Nintendo Switch Online, el peluche vuelve a ser Donkey Kong. Bienvenido a casa, Donkey.",
    ]},

    # ================================================================ 20 → 11
    {"id": "s20", "post": 0.6, "frases": [   # S27
        "Veinte. Según la wiki del juego, si abres un mundo con un código de Cheato, el maestro Jiggywiggy se da cuenta, y anuncia que otra fuerza ha abierto esa puerta.",
        "Y si fallas muchas veces sus rompecabezas, empieza a dudar de que seas el elegido, [short pause] y baja la dificultad sin decírtelo.",
    ]},
    {"id": "s19", "post": 0.6, "frases": [   # S13
        "Diecinueve. En Banjo-Tooie, Grunty deja de rimar en cuanto se lo piden. Gregg Mayles lo hizo para sorprender: le pareció gracioso.",
        "Años después admitió que no fue una de sus mejores ideas, y que probablemente debió mantener las rimas. [short pause] Pero, dijo, si no pruebas cosas distintas, nunca lo sabes.",
    ]},
    {"id": "s18", "post": 0.6, "frases": [   # S39
        "Dieciocho. Los Minjos son Jinjos falsos que te atacan cuando te acercas. En los datos del juego hay un modelo sin usar: un Jinjo enorme, musculoso y con colmillos.",
        "Lo más probable es que fuera un primer diseño del Minjo, descartado porque se le veía venir de lejos.",
        "[amused] Un Minjo de gimnasio. Menos mal que no lo usaron: ya bastantes sustos dan los normales.",
    ]},
    {"id": "s17", "post": 0.6, "frases": [   # S07
        "Diecisiete. Lord Woo Fak Fak, el pez abisal del fondo de Jolly Roger's Lagoon, le dio horas de guerra a su animador. Partes del jefe no se movían, y nadie sabía por qué.",
        "Steve Mayles descubrió que superaba el máximo de articulaciones del motor, un límite que ni sabía que existía. Tuvo que quitarle huesos. [deadpan] Según él, el pobre nunca volvió a ser el mismo.",
        "Así que, si alguna vez te pareció que ese pez se movía raro, no eras tú. Le faltaban huesos.",
    ]},
    {"id": "s16", "post": 0.6, "frases": [   # S18 (línea de N64: comprobar en cuadro)
        "Dieciséis. En Grunty Industries, Loggo, el váter que habla, está atascado. Si le hablas por segunda vez, antes de destaparlo, Kazooie le aconseja llamar a un fontanero, y en Nintendo 64 dice el nombre: Mario.",
        "[sarcastic] En Xbox, con Microsoft de por medio, a Mario no se le podía ni nombrar. Quedó como: ese italiano tan famoso.",
    ]},
    {"id": "s15", "post": 0.6, "frases": [   # S40
        "Quince. Los cuarenta y cinco Jinjos siempre están en los mismos sitios, pero el color de cada uno se sortea en cada partida nueva. Donde tú encontraste uno negro, otro encontró uno blanco. Hasta puede tocarte la familia negra, la de nueve, antes del tercer mundo, aunque es muy raro.",
        "Los speedrunners lo saben bien: en speedrun punto com hay hasta una opción para las partidas que manipulan ese sorteo.",
    ]},
    {"id": "s14", "post": 0.6, "frases": [   # S10
        "Catorce. Kirkhope compuso la música de la intro al compás del video tal como corría en la Nintendo 64, con sus tiempos de carga y sus tirones. En Xbox el juego va más fluido, y la música acaba más de treinta segundos desfasada.",
        "[amused] Y en Nintendo Switch Online, las demos de la pantalla de título van tan aceleradas que parece que Banjo se tomó tres cafés.",
    ]},
    {"id": "s13", "post": 0.6, "frases": [   # S09
        "Trece. Esa intro dura diez minutos, y montarla fue un castigo. Ed Bryan, el encargado, tenía que mover a los personajes por curvas y sincronizar cada animación a mano.",
        "Para el E3 del dos mil tenía que funcionar sin desfasarse. Él y su hermano Will se quedaron hasta pasadas las seis de la mañana, poniéndola una y otra vez. [short pause] Al final, lo lograron.",
    ]},
    {"id": "s12", "post": 0.6, "frases": [   # S22
        "Doce. A Klungo lo enfrentas tres veces, y el rótulo de su pelea cambia con su ánimo: esbirro con una misión, esbirro sediento de venganza, [short pause] y esbirro que se replantea su carrera.",
        "En la última pelea renuncia: sin ascensos, sin días libres, sin sueldo. Dice que buscará un trabajo fácil de oficina, quizá hacer juegos estúpidos.",
        "[amused] Y en Nuts & Bolts lo cumplió: tiene su propio juego, Hero Klungo Sssavesss Teh World. Es el único villano de la saga que se cambia de bando.",
    ]},
    {"id": "s11", "post": 1.0, "frases": [   # S42 ❌ en cuadro (3-nov): dicho como dato de TCRF
        "Once. Según The Cutting Room Floor, el modelo de la casa de Banjo esconde otra casa: una copia casi invisible de la casa de Banjo-Kazooie, con su viejo papel tapiz de flores amarillas.",
        "Y en la intro, el plano del póker en el que ves las cartas de Banjo usaría esa casa vieja, aunque a simple vista ni se nota. [playful] Y ahora sí: los diez que de verdad no te esperas.",
    ]},

    # ================================================================ 10 → 1
    {"id": "s10", "post": 0.6, "frases": [   # S12
        "Diez. Grunty Industries, la fábrica que casi todos odian, fue el primer mundo que diseñó Steve Malpass, que venía del departamento de pruebas. La dibujó en papel, piso a piso, con el hueco del ascensor cuadrado en todas las plantas.",
        "[deadpan] Él mismo admite que quedó demasiado complicada. Su consuelo: muchos la odian, a algunos curiosamente les encanta, y eso es mejor que la indiferencia.",
        "Por cierto, en nuestro ranking de los ocho mundos quedó en último lugar. Malpass, si nos ves: no es personal.",
    ]},
    {"id": "s09", "post": 0.6, "frases": [   # S15 ⚠
        "Nueve. En Jolly Roger's Lagoon vive Trotty, un cerdo al que le salió un tercer brazo por bañarse en la piscina contaminada.",
        "Según VGFacts, en la versión japonesa le quitaron el brazo, y ahora solo le preocupa que el agua sucia le estropee el bañador y la pelota de playa. [sarcastic] Un brazo de más era demasiado. El agua tóxica, no.",
    ]},
    {"id": "s08", "post": 0.6, "frases": [   # S06
        "Ocho. Muchos recuerdan que Banjo-Tooie necesitaba el Expansion Pak. Falso: funciona en una Nintendo 64 normal, y el equipo estaba muy orgulloso de eso.",
        "El precio: si te alejas volando de Cloud Cuckooland y te das la vuelta para verla entera, no cabe en memoria, así que el juego borra sobre la marcha la parte de atrás. [short pause] El cartucho, además, es de doscientos cincuenta y seis megabits, el doble que el de Banjo-Kazooie.",
    ]},
    {"id": "s07", "post": 0.6, "frases": [   # S41 (récords al 3-nov-2026)
        "Siete. Un jugador normal tarda decenas de horas en completarlo al cien por cien. El récord mundial, según speedrun punto com, es de Falcon: cuatro horas, diez minutos y cuarenta y seis segundos.",
        "Y llegar al final, sin buscarlo todo, le tomó veinticinco minutos y cuarenta y nueve segundos. [deadpan] Menos de lo que dura este video.",
    ]},
    {"id": "s06", "post": 0.6, "frases": [   # S08
        "Seis. El huevo Clockwork Kazooie, la bomba de cuerda que manejas a distancia, fue la mayor fábrica de bugs del juego. Podía cruzar puertas, recoger objetos y disparar escenas mientras Banjo se quedaba quieto.",
        "Chris Sutherland cuenta que en las pruebas los fallos no se acababan nunca. En el código se llama babykaz, Kazooie bebé. [amused] Y gracias a él existen glitches como entrar en Grunty Industries sin el tren, o el de los dos Banjos, en Hailfire Peaks.",
    ]},
    {"id": "s05", "post": 0.8, "frases": [   # S04
        "Cinco. Steve Mayles escondió una animación rara de Jamjars: en vez de meterse a tiempo en su silo, la tapa se cierra antes, y se da en la cabeza.",
        "Sale muy pocas veces. Años después, viendo un speedrun en el maratón Awesome Games Done Quick, Mayles la vio salir, y oyó al comentarista quejarse de que el corredor perdía unos segundos.",
        "[laughs softly] Su reacción: uno de sus momentos de mayor orgullo. Costarle unos segundos a ese speedrunner.",
    ]},
    {"id": "s04", "post": 0.8, "frases": [   # S05
        "Cuatro. Al final del juego, Grunty promete venganza en Banjo-Threeie. Durante años se creyó que era un anuncio. [short pause] Gregg Mayles confirmó que era solo un chiste: nunca hubo un tercer Banjo planeado para GameCube.",
        "¿Y el video de Space World dos mil, con Banjo, Kazooie y Mumbo perseguidos por enemigos? Era una demo técnica de GameCube hecha con los modelos de Tooie, para presumir cuántos cabían a la vez.",
        "[amused] Entre los perseguidores salen hasta Gobi y Alphette, dos personajes que no le harían daño a nadie.",
    ]},
    {"id": "s03", "post": 0.8, "frases": [   # S01
        "Tres. Banjo-Tooie desconfía de ti. Si el chip de guardado del cartucho no es el correcto, el juego te dice que no hay ningún mando conectado, y no responde a nada.",
        "Y eso no es todo. Durante la partida, le pregunta al chip de seguridad del cartucho doscientas sesenta y ocho veces si es original, y usa las respuestas para descifrar partes del juego. [short pause] Si una falla, se congela sin avisar.",
        "[deadpan] Ni el examen de la bruja era tan desconfiado.",
    ]},
    {"id": "s02", "post": 0.8, "frases": [   # S03
        "Dos. En Terrydactyland, junto al cráneo de Mumbo, hay una formación de rocas que, vista desde arriba, tiene una forma… [short pause] digamos, poco apta para todo público.",
        "Nintendo Life se lo preguntó al responsable de los escenarios, Steven Hurst. Su defensa: él solo pasó a 3D el dibujo original de Gregg Mayles, y de verdad cree que salió así por accidente.",
        "[sarcastic] Por accidente. Juzga tú.",
    ]},
    {"id": "s01", "post": 0.8, "frases": [   # S02
        "Y el número uno. En el final, Banjo, Kazooie y sus amigos juegan con la cabeza de Gruntilda en lo alto del castillo. En la versión japonesa, esa cabeza se cambió por un saco, hecho con la tela de su ropa.",
        "Lo absurdo: el ojo de Grunty sigue saliéndose del saco, igual que en el original. No hay explicación oficial. [short pause] Se cree que tuvo que ver con un crimen real muy sonado en Japón por aquellos años.",
        "[sarcastic] En Xbox, por cierto, la cabeza volvió. Y tú, toda la vida pateándola, sin saber que en Japón era un saco.",
    ]},
    {"id": "cierre", "frases": [
        "Esos son los cincuenta secretos de Banjo-Tooie que ignoraste. ¿Cuántos conocías? Dímelo en los comentarios, con número.",
        "[warm] Si te gustó, suscríbete: este canal vive de clásicos como este. Y si te quedaste con ganas de más Banjo, en el canal están su historia, sus Jiggies más crueles y el ranking de sus ocho mundos. Nos vemos en el próximo secreto.",
    ]},
]
