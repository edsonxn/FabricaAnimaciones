# -*- coding: utf-8 -*-
"""GUION de un video del motor SECUENCIA YT (gameplay de YouTube por beat).
Se crea con:  python fab.py nuevo <nombre> --yt      Flujo y reglas: docs/estilo_secuencia_yt.md

Voz desde el 2-nov-2026 (el usuario, para Warcraft Y Tamriel): JOHNNY de ElevenLabs (HMCmDsbKeaSZp5LMOYKR, la voz de la que
salió Sarcastica.mp3 de Chatterbox), eleven_v4_turbo con corchetes de actuación ([amused], [sarcastic], [laughs softly],
[deadpan], [sighs], [mischievously], [short pause]…). SIN [whispers] ni [excited] («quitemos whisper o muy emocionado»;
VOZ["sin_etiquetas"] los quita aunque se cuelen). Escritura normal: el inglés sale nativo; FONETICA solo para lo que se oiga
mal. Johnny es de la biblioteca: funciona por id en cualquier cuenta (la 1 tiene el saldo).
Tres voces para el video del cambio de voz (docs/voz.md § «Johnny»): Johnny (narrador), la de siempre con Applio (Edge TTS
Remy + RVC RemyOriginal: VOZ_POR_FRASE = "applio" → tts_gen la genera con VOZ_APPLIO, sin corchetes, con FONETICA_APPLIO;
frases de < ~200 caracteres y nunca de 1-3 palabras) y Remy Eleven (el clon de esa voz en ElevenLabs, con corchetes:
VOZ_POR_FRASE = VOZ_REMY_ELEVEN; solo cuentas 2 y 3, cuidar su saldo).
Si un canal vuelve a Applio entero: VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es",
referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav") y FONETICA = FONETICA_APPLIO.
Estilo de canal «gema»: listas «Las N … de peor a mejor», chistes secos, una cita ficticia dramática por sección.
ESCENAS = secciones del guion (en una lista: una por puesto). Aquí NO se describen imágenes: los cortes salen de
`beats` (pausas reales de la voz, ~8,6 s) y la búsqueda de gameplay de cada beat va en busquedas.json.
Cada video lleva el segmento Overgear entre secciones, NARRADO ENTERO con esta voz, código incluido («Usa el código
CRONICAS10…»): del creativo solo se usa la imagen, nunca su audio (docs/estilo_secuencia_yt.md § Patrocinio).
La pantalla final del canal (canales/<alias>.json «pantalla_final») la anexa `final` sola.
"""

TITULO = "Los 25 SECRETOS que Modern Warfare 4 te escondió"
# ARCHIVO = "nombre_base_de_salida"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_REMY_ELEVEN = "sm2N86ydG2QhV8LIVa9b"   # clon en ElevenLabs de la voz Applio (cuentas 2 y 3; id de cada una en por_cuenta)
# Expediente 141 (elegida por el usuario el 2-nov-2026 entre 9 pruebas, canales/voces_prueba/cod_mw4/): DAMIÁN de la biblioteca
# de ElevenLabs («Deep, Rich & Resonant», latino), tono de sargento con corchetes; por id en cualquier cuenta (la 1 tiene el saldo)
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper",),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {"CRONICAS10": "Crónicas diez"}
# Video del cambio de voz (2-nov-2026): VOZ_POR_FRASE = {"cambio_voz_1": "applio", "cambio_voz_4": VOZ_REMY_ELEVEN, ...};
# las secciones narradas por Remy Eleven también van ahí, frase a frase (dict comprehension por escena)
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md)
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "Battle punto net": "Bátel punto net", "Hardcore": "Jardcor", "Vanilla": "Vanila", "retail": "ritéil",
    "Burning Crusade": "Bérnin Kruséid", "Arthas": "Ársas", "Illidan": "Ilidán", "Hyjal": "Jáyal", "CRONICAS10": "Crónicas diez",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # por defecto solo imagen; el audio del juego va donde conviene oírlo (regla del 26-oct-2026):
    ambiente_por={},        # {"scene-012": .7}: ese beat baja CON su audio (música del juego, gritos, SFX); la OST se aparta ahí
    # ThatWasAwesome lleva su «#3/#5» arriba a la derecha (x .82-.93, y .10-.23): se recorta el lado derecho (izq, arr, der, aba)
    recorte_por={**{f"scene-{n:03d}": (0, .12, .245, .12) for n in
                    [6, 7, 8, 19, 20, 21, 27, 28, *range(36, 44), 64, 65, 67, 68, 77, 78, 82]},
                 "scene-005": 0.06,    # letrero «BETA» arriba a la derecha
                 "scene-062": 0.06, "scene-016": 0.06, "scene-017": 0.06,   # ídem (+ «ZELEXFPS»)
                 "scene-001": 0.125,   # tráiler con franjas de cine (12 % arriba y abajo)
                 "scene-022": 0.125, "scene-093": 0.125, "scene-097": 0.125, "scene-101": 0.125,
                 "scene-107": 0.125, "scene-108": 0.125, "scene-066": 0.125,  # 066: Counter Attack (DZBpDJ2I0T0), franjas
                 # Inkslasher (ViJ6PJqh5As) lleva su contador de ranking arriba a la izquierda (x .01-.07, y .02-.11)
                 **{f"scene-{n:03d}": (.07, .12, .05, 0) for n in [10, 11, 12, 100, 102, 104, 113]},
                 "scene-114": (0, .13, 0, .10)},  # final de Greater Good (VydXHzNRG-k): franjas de cine; el de antes tenía la cara de un streamer
    yt=dict(sufijo="Call of Duty Modern Warfare 4", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),   # canales que salen con cara/overlay y ensucian el plano
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de MW4 (Stephen Barton / Jason Graves) armada con armar_musica_ost.py, nunca Lyria

# Pausas con la voz callada (regla del 31-oct-2026, «si la voz nombra un sonido, se oye»): "post" de la escena =
# el sonido del juego a 0,9-1,0 (ambiente_por) con la OST apartada.
#   p12 «sentido arácnido» de Dunn · p09 la radio con los indicativos · p02/p02b «Bravo 6, going dark» y «You broken, John?» ·
#   p01/p01b la música de la post-créditos de MW4 y la del final de CoD 4 (2007) · p01c «Welcome to the Watcher program»
# Voz: sin susurros ni emoción fuerte de excitado (el usuario, 2-nov-2026, todos los canales): solo [serious], [deadpan], [short pause].
ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Clasificación: secreto. Asunto: Modern Warfare 4.",
        "Le disparas a un cuadro en Corea del Norte, y tu propio compañero te ejecuta.",
        "Te asomas a una tele en Nueva York, y alguien está jugando GTA seis. [deadpan] Sí. Antes que tú.",
        "Infinity Ward escondió todo esto en el último capítulo de la saga, que salió hace apenas unas semanas.",
        "Hoy abrimos veinticinco secretos. Todos comprobados, y con sus fuentes en la descripción.",
        "Y el número uno no se ve. Se oye. [short pause] Así que quédate hasta el final, soldado.",
    ]},
    {"id": "p25", "frases": [
        "Número veinticinco. La tele que nadie mira.",
        "En la segunda misión persigues a Makarov por un edificio de Nueva York. Y en una pantalla está la guía de televisión.",
        "La programación es inventada: Princess Starfish dos, el regreso al trono. Operation Saber tres. Y Excessive Cakes, o sea, Pasteles excesivos.",
        "Y al final de la misión hay una pizzería de parodia, Joe's Pizza House. Alguien escribió una programación entera para una pantalla que ves medio segundo. Mientras persigues a un terrorista.",
    ]},
    {"id": "p24", "frases": [
        "En el veinticuatro, pulsa E para despedirte.",
        "En la misión Atrapados, en el norte nevado, el soldado Chow se desangra en el refugio mientras tú sales a explorar.",
        "Cuando vuelves, ya murió. Y el juego te deja acercarte y pulsar E para despedirte de él.",
        "[deadpan] Es el famoso Press F to pay respects de Advanced Warfare, el meme del que se rio internet entero en dos mil catorce. Solo que esta vez nadie se ríe.",
    ]},
    {"id": "p23", "frases": [
        "Número veintitrés. El pato armado.",
        "En DMZ, dentro de un departamento de Hajan River Heights, hay un patito de goma. Con un cuchillo.",
        "Nadie sabe por qué está ahí. Nadie lo explica. [short pause] En Modern Warfare 4, hasta los patos van armados. Si lo encuentras, no le des la espalda.",
    ]},
    {"id": "p22", "frases": [
        "En el veintidós, la física que nunca habíamos tenido.",
        "Dispara a través de una granada de humo, y las balas le abren agujeros. Se ve el túnel de cada tiro.",
        "Agáchate a disparar junto al barro, y el arma se salpica. Y si te disparan, se mancha de sangre.",
        "Son detalles que la saga nunca tuvo. Y casi todos los pasamos corriendo.",
    ]},
    {"id": "p21", "frases": [
        "Número veintiuno. Las armas que se acuerdan de dos mil nueve.",
        "En la misión de Bombay, el Patriot XMR, la versión de este juego del ACR, recarga casi igual que el ACR del Modern Warfare dos original.",
        "Y en la misión final, el AK setenta y cuatro u lleva camuflaje de cinta blanca. Como la FAMAS de cinta blanca de la misión en la nieve de dos mil nueve.",
        "Si eso no te dice nada, eres muy joven. [short pause] Y nosotros, muy viejos.",
    ]},
    {"id": "p20", "frases": [
        "En el veinte, tu soldado hace de Neo.",
        "Si haces la animación de inspeccionar el arma con las manos vacías, a veces el personaje se inventa otra cosa.",
        "Esquiva balas echándose hacia atrás como en Matrix, hace el gesto de Neo con la mano, o se truena el cuello.",
        "Es la tradición de Modern Warfare dos Remastered, donde tu soldado jugaba piedra, papel o tijera. [deadpan] Él solo.",
    ]},
    {"id": "p19", "frases": [
        "Número diecinueve. Un periódico con la caja mágica.",
        "En la misión Cumpliendo órdenes juegas como soldado norcoreano. Y bajo los pies de la primera familia hay un periódico.",
        "En la foto sale la caja mágica de Zombies, la de Infinite Warfare, de dos mil dieciséis.",
        "[deadpan] Detalle: Modern Warfare 4 no tiene modo Zombies. Pero el periódico de la aldea, por lo visto, sí.",
    ]},
    {"id": "p18", "frases": [
        "En el dieciocho, no te tumbes.",
        "En la última misión, Price persigue al Arquero con un trozo de metal clavado en el estómago.",
        "Si te tiras al suelo, Price recibe daño. Lo probaron en dificultad Realismo: duele, pero no te mata.",
        "Alguien en Infinity Ward pensó en el jugador que se tira al piso por costumbre. Y decidió castigarlo. Un poco.",
    ]},
    {"id": "p17", "frases": [
        "Número diecisiete. El contrabando de Occidente.",
        "Al registrar casas en Cumpliendo órdenes encuentras lo prohibido: una novela occidental, un reproductor con música de fuera.",
        "Y la medicina del corazón de un hombre. Él dice que morirá sin ella. Y la respuesta es que morirá por eso de todos modos.",
        "Son los mismos objetos que se castigan de verdad en Corea del Norte. Y una caja de herramientas con candado, código dos, uno, cuatro, guarda otro más, con una nota para un logro.",
    ]},
    {"id": "p16", "frases": [
        "En el dieciséis, los trucos de los desarrolladores.",
        "En la primera misión, tras el apagón, la pantalla se va a negro. Y en ese segundo te teletransportan a una copia destruida del barrio.",
        "Si miras bien, una camioneta que tapaba un callejón desaparece, y de pronto se ve un mapa abierto que no debías ver.",
        "En la misión del tren, los rehenes se esfuman en cuanto dejas de mirarlos. Y si retrocedes en las trincheras, te aparecen granadas a los pies, como los morteros invisibles de CoD 4.",
        "[deadpan] El juego no tiene muros invisibles. Tiene castigos invisibles.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Los dos de relleno que no son de relleno.",
        "En Bombay, Gaz va con dos soldados del SAS: Wallcroft y Griffin. Parecen genéricos.",
        "No lo son. Pelearon a tu lado en el metro de Londres, en Modern Warfare 3, de dos mil once. Y Griffin, según los fans, ya estaba en el entrenamiento de CoD 4.",
        "Personajes de la saga original, metidos en el reboot, que es otra línea temporal. Diecinueve años de servicio. [short pause] Y siguen sin ascenso.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, no puedes perdonar a Graves.",
        "En la misión Hired Gun derribas el helicóptero de Phillip Graves, el de Shadow Company. Y Graves te suplica por su vida.",
        "No hay botón para perdonarlo. Y si tardas en rematarlo, aprovecha la duda, y te mata.",
        "[deadpan] En Modern Warfare, la piedad es una mecánica. Y es una trampa.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. La estatua que puedes escalar.",
        "En el norte nevado hay una estatua gigante del Líder Supremo. Márcala por radio, y alguien te cuenta su leyenda.",
        "Que derrotó él solo a un batallón japonés entero. Imposible, admite el propio personaje. Pero ahí se habrían bebido la tierra como agua si él lo decía.",
        "Y se puede escalar. Arriba hay suministros y la nota de un ciudadano que se pregunta si en el Sur alguien hace lo mismo.",
        "Acuérdate de esta estatua. Porque en el puesto tres, al mismo Líder, mejor ni tocarlo.",
    ]},
    {"id": "p12", "post": 2.5, "frases": [
        "En el doce, el fideo de Spider-Man.",
        "Primera misión, una tienda de Hajin, en Corea del Sur. Antes del primer disparo de la guerra, el cabo Dunn te lanza un bol de fideos instantáneos.",
        "Si lo atrapas, te dice que se te activó el sentido arácnido.",
    ]},
    {"id": "p12b", "frases": [
        "Si lo dejas caer, te regaña por dejar eso tirado. Y si tardas en recogerlo, te lo vuelve a reclamar.",
        "Diálogo distinto para un bol de fideos. [short pause] En un juego de guerra.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Soap no sale en el juego.",
        "Soap MacTavish, el de siempre, no aparece en la campaña. Pero lo escondieron dos veces.",
        "Un grafiti con una pastilla de jabón azul y la palabra SOAP, con un símbolo radiactivo en la O.",
        "Y un letrero digital en una ciudad nevada que dice KR-SOAP. Y junto a él, ciento cuarenta y uno. El número de la Task Force. [short pause] Y el de este canal.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, la impresora 3D de Cachette.",
        "Pasamos al multijugador. En el mapa Cachette, en el piso de arriba de la Armería, tras un cristal, hay una impresora 3D.",
        "Si en vez de usarla la golpeas, rompes la pantalla, y sale un arma completa, con cinco accesorios y aspecto de resina impresa.",
        "Cambia en cada partida. La descubrió un usuario de Reddit, muggs, uno dos uno tres. Y la impresora es una mecánica de DMZ, colada en el multijugador como secreto.",
    ]},
    {"id": "p09", "post": 4.0, "frases": [
        "Número nueve. La radio de dos mil siete.",
        "En el contraataque en la costa de Hajin, los vehículos aliados usan indicativos que ya conoces. Si jugaste en dos mil siete.",
        "War Pig, el tanque atascado en el pantano de CoD 4. Y Gold Eagle, el indicativo del general Shepherd. Escucha la radio.",
    ]},
    {"id": "p09b", "frases": [
        "Y en Decapitation entras disparando desde un helicóptero con indicativo Outlaw dos cinco. El mismo helicóptero de Jackson en CoD 4.",
        "Solo se oyen por radio. [deadpan] Y si los reconociste, ya tienes edad para que te duela la espalda.",
    ]},
    {"id": "p08", "frases": [
        "En el ocho, Ghost muere si eres curioso.",
        "En la misión Huida ves por una ventana cómo dos soldados interrogan y golpean a Ghost.",
        "Si te quedas mirando en vez de entrar, uno le dispara en la cabeza. Y la misión fracasa al instante.",
        "El personaje más querido de la saga, muerto porque te quedaste mirando. [short pause] Muévete, soldado.",
    ]},
    {"id": "p07", "frases": [
        "Número siete. La comandante Ri no perdona.",
        "Volvemos a Cumpliendo órdenes. Si le apuntas demasiado tiempo a la comandante Ri Ju-Young, la hermana del Líder, ella y sus soldados te disparan.",
        "Si escondes a la familia del sótano y dices que en esa casa no hay nadie, más tarde Ri lo descubre. Y ordena preparar otra soga. Para el que mintió.",
        "Y si al final te niegas a ahorcar al desertor, Ri te ejecuta por traidor. [short pause] El juego no te deja ser el bueno. Ni con la mirada.",
    ]},
    {"id": "p06", "frases": [
        "En el seis, pixel art en París.",
        "En la misión Tráfico, en las esquinas de los edificios de París, hay mosaicos de pixel art.",
        "Price con su sombrero clásico. Ghost. Y un pastor alemán con chaleco y gafas: Riley, el perro de Call of Duty Ghosts, de dos mil trece.",
        "Es un homenaje a Invader, el artista callejero francés que llena París de mosaicos de videojuegos. [deadpan] Riley no sale en esta saga. Pero tiene su pared.",
    ]},
    {"id": "p05", "frases": [
        "Número cinco. Los perros de Prípiat.",
        "En el garaje de Huida, unos perros atacan a Price y a Ghost. Y después Price suelta una frase: no son nada comparados con los de Prípiat.",
        "Es la misión All Ghillied Up de CoD 4. Price joven y MacMillan cruzando Prípiat en mil novecientos noventa y seis, con perros salvajes encima.",
        "El reboot es otra línea temporal. Pero Price se acuerda de Prípiat. O sea: la misión favorita de media saga sigue siendo canon.",
    ]},
    {"id": "p04", "frases": [
        "En el cuatro, GTA seis salió primero. Dentro de Call of Duty.",
        "En la segunda misión persigues a Makarov por las azoteas de Nueva York, atravesando departamentos.",
        "Si te detienes antes del pasillo y miras la tele, alguien está jugando algo idéntico a GTA seis. El personaje, los autos, el minimapa abajo a la izquierda.",
        "En una consola falsa de Activision, con guiños a Pitfall, su clásico de los ochenta. [deadpan] Para verlo, tienes que dejar que Makarov se aleje. Prioridades, soldado.",
    ]},
    {"id": "p03", "frases": [
        "Número tres. Dispárale al retrato del Líder.",
        "En Cumpliendo órdenes buscas a un desertor casa por casa. Puedes disparar tiros de advertencia a los civiles, y no pasa nada.",
        "Pero si le disparas al retrato del Líder Supremo colgado en la pared, tu compañero te elimina al instante.",
        "Y la pantalla de muerte lo explica: deshonraste a tu país dañando un retrato del Líder Supremo. Con el botón de reintentar, en coreano.",
        "Y no es del todo un chiste: en Corea del Norte, dañar un retrato del líder es un delito político real. [short pause] La estatua la puedes escalar. El cuadro, ni lo mires feo.",
    ]},
    {"id": "spoilers", "frases": [
        "[serious] Alto ahí. Lo que sigue es el final de la campaña. Si no lo has terminado, este es tu momento de retirarte. [short pause] Los que se quedan, conmigo.",
    ]},
    {"id": "p02", "post": 3.0, "frases": [
        "Número dos. La caída de Gaz.",
        "En Bombay, Gaz, ya capitán de la ciento cuarenta y uno, aterriza en una azotea para cazar a Price. Y dice esto.",
    ]},
    {"id": "p02b", "post": 3.0, "frases": [
        "Bravo seis, going dark. Es la frase de Price en el tráiler de Modern Warfare de dos mil diecinueve. La primera que le oímos. Ahora la usa Gaz, para cazar al hombre que la dijo.",
        "Y hay más. En dos mil diecinueve, Price conoció a Gaz con una pregunta: ¿estás roto? La frase se repitió en las dos entregas siguientes.",
        "En Modern Warfare 4, cuando los capturan, es Gaz quien se la grita a Price.",
    ]},
    {"id": "p02c", "frases": [
        "El roto, ahora, es Price. Y Gaz se lo echa en cara con sus propias frases: cortamos cabezas de serpiente, no nos unimos al nido.",
        "Al inicio de Huida, el Arquero, el villano de Mads Mikkelsen, ejecuta a Gaz. Igual que Zakhaev mató a Gaz en el final de CoD 4, en dos mil siete.",
        "Y aquí está el secreto. En la prisión, una nota dice que lo confiscado va a una caja fuerte. Otra nota, en una recepción que cruzas desarmado, da el código: ocho, cuatro, uno, cero.",
        "Dentro están las chapas de identificación de Gaz. Y el logro se llama Jamás te olvidaremos.",
        "[short pause] Si no abres esa caja, puedes seguir creyendo que Gaz está vivo. El juego te deja elegir no saberlo.",
    ]},
    {"id": "p01", "post": 6.0, "frases": [
        "Y el número uno. El secreto que no se ve.",
        "La saga termina en un lago helado. Price mata al Arquero, y muere junto a Ghost. Sus últimas palabras: mantén la línea.",
        "Pero no acaba ahí. Después de los créditos, Kate Laswell borra con una USB los archivos de la Task Force ciento cuarenta y uno.",
        "Y de fondo suena esto.",
    ]},
    {"id": "p01b", "post": 6.0, "frases": [
        "Es una versión nueva de la música del final de CoD 4. La del puente, cuando Price, herido, acaba de matar a Zakhaev. Así sonaba en dos mil siete.",
    ]},
    {"id": "p01c", "post": 2.5, "frases": [
        "La música de CoD 4 la escribió Stephen Barton junto a Harry Gregson-Williams. Y Stephen Barton compuso también Modern Warfare 4.",
        "La misma persona cerró las dos sagas, diecinueve años después, con la misma música.",
        "Y el último detalle. En el tráiler de dos mil diecinueve, Laswell usaba el indicativo Watcher seis. Aquí recluta a una mujer a la que nunca le vemos la cara.",
        "Y le dice: bienvenida al programa Watcher.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "La saga empieza y termina con el mismo nombre. Y la que sigue no tiene rostro. [short pause] Expediente cerrado. Por ahora.",
        "Este es el primer expediente del canal. Si quieres el siguiente, suscríbete: aquí abrimos los archivos de Call of Duty que nadie te contó, en español.",
        "Y dime en los comentarios cuál de los veinticinco no conocías. Yo apuesto por el pato. [short pause] Retírate, soldado.",
    ]},
]

# Nombres que Whisper escribe distinto (GTA VI, Hadgen, Warcroft, McTavish, Cachet, Mugs1213, Shepard, Rhee, Pripyat, Gas): la voz
# está bien; se aceptan con CER mayor. Revisadas al oído las que no (p20_0, p02_0, p01_0, p02c_0 se regeneraron).
CER_MAX_POR_FRASE = {k: 0.10 for k in ("intro_2", "p23_1", "p17_3", "p15_1", "p11_1", "p11_2", "p10_0", "p10_1", "p10_3",
                                         "p09_2", "p07_0", "p05_0", "p04_0", "p04_2", "p02_1", "p02b_1", "p02c_3", "p02_0")}
