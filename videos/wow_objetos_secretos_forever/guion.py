# -*- coding: utf-8 -*-
"""GUION — «Los 15 OBJETOS SECRETOS de WoW Forever que nadie te explica» (Crónicas de Warcraft, 1-nov-2026).
Motor SECUENCIA YT (gameplay de YouTube por beat). Flujo y reglas: docs/estilo_secuencia_yt.md
Investigación con fuentes: videos/_investigacion_wow_objetos_secretos_forever.md (nada de cifras fuera de ahí).

Tema elegido por el usuario (1-nov) entre 3 propuestas: la fórmula de «Los 12 objetos más RAROS de Vanilla» cambiando
UNA variable (Vanilla → Forever); fuera, Kadrath ×4,0 y ×2,3 con ítems secretos. ~18 min (el usuario). Sale el jue 5-nov,
al día siguiente del lanzamiento: todo lo de la lista es de la BETA y se dice.
Overgear campaña 2 (coaching Forever + CRONICAS10) tras el n.º 12, con fondo de marca.
Comentarios: 1 agradecimiento en el gancho + 4 en dos tandas + AL MENOS 3 críticas con burla disfrazada (el usuario, 1-nov),
repartidas en pausas y nunca en plena revelación. La guasa nunca niega que la voz es IA.
Voz Applio: frases de < ~200 caracteres y nunca sueltas de 1-3 palabras; todo nombre inglés en FONETICA; cifras en letra.
"""

TITULO = "Los 15 OBJETOS SECRETOS de WoW Forever que nadie te explica"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "Vanilla": "Vanila", "CRONICAS10": "Crónicas diez", "WoW": "uórld of uárcraft", "Wowhead": "Uáujed",
    "Wrath": "Raz", "Hyjal Summit": "Jáyal Sámit", "Hyjal": "Jáyal", "Barrow Deeps": "Bárou Díps", "Onyxia": "Oníxia",
    "addons": "ádons", "Discord": "Díscord", "Reddit": "Rédit",
    # lugares
    "Zephras": "Séfras", "Riverglades": "Ríverglèids", "Powderfuse Port": "Páuderfius Port", "Mulgore": "Mulgor",
    "Stratholme": "Strátjolm", "Un'Goro": "Un Góro", "Thoradin": "Zóradin", "Kalimdor": "Kalímdor",
    # personajes y PNJ
    "Rhahk'Zor": "Rak Sor", "Mr. Smite": "Míster Smáit", "Boyle": "Bóil", "Mister Graphed": "Míster Gráfed",
    "Madam Swyndle": "Mádam Suíndel", "Rivendare": "Ríven der", "Archimonde": "Árchimond", "Cenarius": "Cenárius",
    "Sylvestris Dusksong": "Silvéstris Dásksong", "Stormwraith": "Stórm réiz", "Josh Greenfield": "Yosh Grínfild",
    "Aggrend": "Ágrend", "Skyborne": "Skáiborn", "The Broodmother": "De Brúdmader",
    # objetos y textos
    "Ocarina of Time": "Ocarina of Táim", "Fel Crystal": "Fel Crístal", "Stranglevine": "Strángelvain",
    "Shen'Serrar": "Shen Serrár", "Quel'Serrar": "Kel Serrár", "lezal melor'na adala fal": "lésal melórna adála fal",
    "Shen'Serrar lezal melor'na adala fal": "Shen Serrár, lésal melórna adála fal",
}

# Nombres que Whisper escribe distinto (Skyborne→Skyborn, Mister Graphed→Mr. Graffed, Stratholme→Strattholm, Shen'Serrar→Sencerrar,
# Wowhead→«Nua Ojeda», Azeroth→Acerota): transcripciones leídas una a una el 1-nov y aceptadas
CER_MAX_POR_FRASE = {"c11_0": 0.0165, "intro_2": 0.0182, "c15_4": 0.0138, "c14_1": 0.0352, "c12_3": 0.04, "overgear_2": 0.014, "c11_5": 0.0265, "c11_6": 0.0182, "c10_0": 0.0143, "c10_1": 0.0268, "c09_1": 0.0427, "c08_1": 0.153, "c08_8": 0.0202, "c07_1": 0.0523, "c06_3": 0.0551, "c06_6": 0.0259, "c05_1": 0.1068, "c05_5": 0.0256, "c03_0": 0.0297, "c03_2": 0.0338, "c03_3": 0.0356, "c03_4": 0.0364, "c03_6": 0.0282, "c02_7": 0.016, "c01_5": 0.0627, "c01_6": 0.0478, "c01_12": 0.0204}
TAIL_MAX_POR_FRASE = {"intro_2": 0.3, "c15_4": 0.3, "c14_1": 0.3, "c12_3": 0.487, "overgear_2": 0.3, "c11_5": 0.3, "c11_6": 0.3, "c10_0": 0.3, "c10_1": 0.3, "c09_1": 0.42, "c08_1": 0.3, "c08_8": 0.3, "c07_1": 0.586, "c06_3": 0.3, "c06_6": 0.3, "c05_1": 0.399, "c05_5": 0.3, "c03_0": 0.3, "c03_2": 0.3, "c03_3": 0.3, "c03_4": 0.3, "c03_6": 0.3, "c02_7": 0.3, "c01_5": 0.359, "c01_6": 0.425, "c01_12": 0.41}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-018": 0.9},   # el canto real de las ranas del n.º 14 (post de c14), CON su audio (regla del 31-oct)
    yt=dict(sufijo="World of Warcraft Forever", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos se fijan tras `tiempo` (<= 175 s cada uno)
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 1-nov, 1037,5 s); música ORIGINAL de WoW: `musica_wow.py` corta un tema por tramo
        (['intro', 'c15'], 'Ventormenta'),                 # 0-100 s      gancho y la descarrioaleta
        (['c14', 'gracias1'], 'Feralas'),                  # 100-162,5 s  ranas de Zephras (el canto va con audio del clip)
        (['c13', 'burla1'], 'Entrañas'),                   # 162,5-215 s  babosa
        (['c12'], 'Dun Morogh'),                           # 215-260 s    cocodrilo de las cloacas
        (['overgear'], 'Dun Morogh'),                      # 260-310 s    patrocinio (suena la música promo)
        (['c11', 'burla2'], 'Feralas'),                    # 310-370 s    banana
        (['c10'], 'Durotar'),                              # 370-425 s    crisálida (Mulgore)
        (['c09', 'gracias2'], 'Forjaz'),                   # 425-492,5 s  Cercenarrocas
        (['c08', 'burla3'], 'Forjaz'),                     # 492,5-567,5 s anillos
        (['c07', 'c06'], 'Orgrimmar'),                     # 567,5-680 s  mercado negro y loto
        (['c05'], 'Tierras de la Peste del Este'),         # 680-732,5 s  destrero de Stratholme
        (['c04'], 'Núcleo de Magma'),                      # 732,5-807,5 s llave de piedra (Roca Negra)
        (['c03'], 'Legends of Azeroth'),                   # 807,5-867,5 s Shen'Serrar
        (['c02'], 'Cima del Trueno'),                      # 867,5-917,5 s 75 monturas
        (['c01'], 'Darnassus'),                            # 917,5-1005 s legendario (Círculo Cenarion, Hyjal)
        (['cierre'], 'Legends of Azeroth'),                # 1005-1037,5 s
    ],
    # durante el anuncio suena la «musica promo» del canal (regla del 13-oct-2026), igualada al RMS del tramo
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "World of Warcraft Forever tiene más de treinta y un mil objetos, y Blizzard escondió las estadísticas de doce mil quinientos noventa y cuatro.",
        "Puedes ver que existen, pero no qué hacen, hasta que alguien en el mundo consigue uno y el juego se lo revela a todos.",
        "Así que en la beta los jugadores se pusieron a cazar, y encontraron un hacha que mina sin la profesión y una banana que te hace más fuerte en el bosque.",
        "También un mercado negro que vende loto negro, una llave que nadie sabe qué abre y un legendario con el nombre borrado.",
        "Como nos escribió un espectador, casi veinte años después siguen quedando cosas por descubrir en este juego.",
        "Hoy te traigo los quince objetos secretos de World of Warcraft Forever que nadie te explica, del quince al uno.",
        "Todo esto salió en la beta, así que algún número puede cambiar ahora que el juego sale hoy, pero el secreto sigue ahí.",
    ]},
    {"id": "c15", "frases": [
        "Número quince. La Delicia de descarrioaleta sabrosa, el pescado que no te quita el hambre: te cambia la cara.",
        "Es una receta nueva de la Alianza que se consigue en las Montañas Crestagrana, y pide ochenta y cinco de Cocina.",
        "Los veteranos ya la reconocen: es la hermana de la Delicia de desviada sabrosa de Los Baldíos, que te disfrazaba al comértela.",
        "Su descripción entera son dos palabras: «Cómeme».",
        "Al principio de la beta, comértela te convertía en un múrloc o en un ogro, y la gente estaba encantada.",
        "Blizzard aclaró que eso era un efecto provisional que no debía estar ahí, y ahora te convierte en un orco vestido de ninja o de pirata.",
        "Y la nota de los desarrolladores dejó la puerta abierta: puede que vuelvan a meter transformaciones parecidas en el futuro.",
        "O sea que en algún parche de Forever volverás a ser múrloc, y esta vez a propósito.",
    ]},
    {"id": "c14", "post": 3.0, "frases": [
        "Número catorce. El Saltavientos musical, la mascota que se consigue cantando.",
        "En el sur de la isla Zephras, donde empiezan los nuevos Skyborne, hay unas ranas sentadas juntas sobre una roca.",
        "No hay misión ni cartel: tienes que ponerte frente a ellas y escribir el gesto de cantar.",
        "Tiene truco: si sobre la roca queda una sola rana, no pasa nada; tienen que ser al menos dos.",
        "Y no hace falta ningún nivel ni ninguna facción: cualquiera que pise la isla puede intentarlo.",
        "Si lo haces bien, aparece una rana nueva en el tronco de al lado, la tocas y es tuya.",
        "En Wowhead, el comentario más votado lo explica: es un homenaje a Ocarina of Time, donde cantarle a las ranas te daba una pieza de corazón.",
        "Y sí: las ranas te contestan cantando, y suena así.",
    ]},
    {"id": "gracias1", "frases": [
        "Y antes de seguir, gracias por comentarios como estos, que nos dejan en cada video.",
        "Todos se leen, y todos se toman en cuenta para seguir mejorando el canal.",
    ]},
    {"id": "c13", "frases": [
        "Número trece. La Babosa agitada, la mascota que te exige bailar en las cloacas.",
        "Esta es para la Horda, y empieza en Entrañas, con un vendedor llamado Boyle.",
        "Le compras un Fango de baba nutritivo, que por su nombre ya sabes que no es un plato para invitar a nadie.",
        "Luego bajas al canal de la ciudad, buscas una de las babosas que se mueven por el agua y le bailas.",
        "Y le sigues bailando, sin vergüenza, hasta que la babosa te devuelve el baile.",
        "Ahí se abre una misión, la entregas y te llevas a tu propia babosa.",
        "Y lo mejor: si después le bailas a tu mascota, ella también te baila a ti.",
    ]},
    {"id": "burla1", "frases": [
        "Y hablando de gustos raros, también nos llegan comentarios como este.",
        "Totalmente de acuerdo en algo: el asco es algo muy personal.",
        "Por eso acabo de explicarte cómo bailarle a una babosa en una cloaca: aquí respetamos todos los gustos.",
    ]},
    {"id": "c12", "frases": [
        "Número doce. La Cría de crocolisco, la mascota de la leyenda de las cloacas de Ventormenta.",
        "En los canales de la capital de la Alianza vive, desde el juego original, la Bestia de cloaca, un crocolisco raro de nivel cincuenta.",
        "La mayoría de los jugadores nunca la vio, porque recorre los canales de la ciudad y casi nadie se mete a nadar ahí.",
        "En Forever le dieron algo que nunca tuvo: una cría que suelta al morir, con un uno coma cincuenta y dos por ciento de probabilidad.",
        "En la beta el nivel estaba limitado a veinte, así que la gente formó bandas enteras para perseguir a un cocodrilo de nivel cincuenta.",
        "Si ahora ves a alguien de nivel sesenta nadando en círculos por los canales de Ventormenta, no está perdido.",
        "Está pescando un cocodrilo.",
    ]},
    {"id": "overgear", "post": 2.6, "frases": [
        "Y si te preguntas cómo encuentran tan rápido estos secretos, la respuesta es que estudian el juego como nadie.",
        "Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.",
        "Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado te guía por voz.",
        "Casi nadie se atasca por ser malo, sino porque nadie le dijo qué estaba haciendo mal, y en Forever el equipo no caduca: los vicios de las primeras semanas se quedan.",
        "Talentos, rotación, mazmorras nuevas, el plan de equipo para las bandas del nueve de diciembre o duelos: tú eliges, y pagas solo las horas que necesites.",
        "El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    {"id": "c11", "frases": [
        "Número once: la Banana dorada, el abalorio más ridículo y más serio de esta lista.",
        "Su efecto es real: al usarla, aumenta en dieciséis puntos todos tus atributos durante quince segundos.",
        "Y luego viene la letra pequeña: el efecto y la duración se duplican en bosques y praderas.",
        "Así que en un bosque o en una pradera, esa banana te da treinta y dos a todo durante medio minuto.",
        "En una cueva o en una capital, eres alguien con una banana en la mano.",
        "Lo más curioso es que en Wowhead aparece como botín, pero todavía nadie ha dicho de qué monstruo cae.",
        "Así que si un mono te mira raro en la Vega de Tuercespina, tú ya sabes por qué.",
    ]},
    {"id": "burla2", "frases": [
        "Y ya que hablamos de cosas que se revisan con cuidado, aquí va una reseña muy detallada.",
        "Gracias, de verdad: por críticas así, cada efecto de este video está copiado letra por letra de la descripción del juego.",
        "Así que si algo sale errado, la culpa ya no es de la inteligencia artificial: es de la banana.",
    ]},
    {"id": "c10", "frases": [
        "Número diez. La Crisálida transformadora, el abalorio que primero te paraliza y luego te salva.",
        "Es la recompensa de una misión de élite nueva en Mulgore, llamada The Broodmother, para nivel treinta.",
        "Al usarla, absorbes entre doscientos sesenta y trescientos puntos de daño, pero te aturdes tú mismo durante cinco segundos.",
        "Sí, oíste bien: el objeto te deja aturdido a ti.",
        "Cuando el aturdimiento termina, sales con un sesenta por ciento más de velocidad durante ocho segundos.",
        "Según los que la probaron, mientras tanto te conviertes en araña, envuelto en tu capullo.",
        "En un combate perdido son cinco segundos para que te curen, y luego una huida que nadie alcanza.",
        "Y con cinco minutos de reutilización, es de esos objetos que guardas para cuando todo sale mal.",
        "En la Temporada de Descubrimiento esto habría sido un rumor; en Forever es una pieza de equipo de nivel treinta.",
    ]},
    {"id": "c09", "frases": [
        "Número nueve. El Cercenarrocas, el hacha que mina sin saber minar.",
        "Lo suelta Rhahk'Zor, el primer jefe de las Minas de la Muerte, con un cinco coma cuarenta y cinco por ciento de probabilidad.",
        "Es un hacha a dos manos de nivel dieciocho, y hasta ahí, nada raro.",
        "Pero tiene un uso nuevo: corta y recoge filones de cobre, estaño, plata y hierro, y no pide la habilidad de Minería.",
        "Tiene treinta cargas, y cuando se acaban te quedas con el hacha, pero ya no mina.",
        "Con un cinco por ciento, cada hacha te sale en unas dieciocho vueltas a las Minas, de media.",
        "Para que lo entiendas: un minero normal necesita ciento veinticinco de habilidad solo para tocar el hierro.",
        "Y como las cargas no aparecen en la descripción que ven los demás, en la subasta nadie sabe cuántas le quedan a la tuya.",
        "Con varias de estas hachas puedes llevar Ingeniería y Herrería juntas, algo que en dos mil cuatro casi nadie se permitía.",
    ]},
    {"id": "gracias2", "frases": [
        "Y antes del número ocho, otra tanda de comentarios que nos alegraron la semana.",
        "Gracias a los que nos ven mientras hacen sus semanales: aquí seguimos acompañándolos.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho. La Sortija de contramaestre, el anillo de nivel diecisiete que te espera en el nivel sesenta.",
        "Cae de Mr. Smite, en las Minas de la Muerte, con apenas un uno coma cero uno por ciento.",
        "Sola es un anillo flojito, pero forma parte de un conjunto de dos piezas llamado «Cómplices».",
        "La otra mitad es la Sortija de la media naranja: nivel sesenta, nivel de objeto setenta, y dieciocho de fuerza.",
        "Con las dos puestas, cada golpe cuerpo a cuerpo puede enfurecerte: cincuenta de fuerza durante diez segundos, más veintidós fijos.",
        "Sumado todo, el conjunto da cuarenta y cuatro de fuerza, y noventa y cuatro mientras dura el enfado.",
        "O sea, un anillo que sacas a los diecisiete y que sigue sirviendo en las bandas.",
        "El problema es que nadie sabe todavía dónde cae la media naranja.",
        "Y si los nombres de los anillos cuentan una historia de pareja, en algún lugar de Azeroth hay alguien esperando a su contramaestre.",
    ]},
    {"id": "burla3", "frases": [
        "Y hablando de esperar, a alguien la espera se le hizo un poco larga.",
        "Un comentario que ya venía roncando: se nota que descansaste a gusto.",
        "Si te vuelve a dar sueño, en el video de la primera semana te dijimos dónde está la Bolsa de dormir acogedora: así por lo menos dormir te da experiencia.",
    ]},
    {"id": "c07", "frases": [
        "Número siete. El Don del galope, la velocidad que se paga por quincena.",
        "En Riverglades, una de las zonas nuevas, hay un goblin de nivel sesenta con un título que no esconde nada: Mister Graphed, agente del mercado negro.",
        "Entre sus cosas vende este objeto épico por ciento cincuenta de oro.",
        "Te da un diez por ciento más de velocidad sobre la montura durante trescientas sesenta horas, quince días, y se suma a la zanahoria en un palo.",
        "La trampa está en una línea de la descripción: el tiempo corre aunque estés desconectado.",
        "Así que mantenerlo siempre activo cuesta trescientos de oro al mes, juegues o no.",
        "Y se pueden llevar hasta diez a la vez, aunque nadie ha confirmado si se suman entre ellos: la descripción solo habla de sumarse a otros bonos.",
        "Por cierto, el primer hilo que lo encontró en Reddit decía que daba ciento cincuenta por ciento de velocidad.",
        "No: ciento cincuenta era el precio. Los comentarios se lo recordaron sin piedad.",
    ]},
    {"id": "c06", "frases": [
        "Número seis. El loto negro, a la venta en una tienda.",
        "En el World of Warcraft original, el loto negro era la planta más peleada del juego: crecía en pocas zonas y se defendía a espadazos.",
        "Con él se hacían los frascos que las bandas pagaban a precio de oro.",
        "Pues el mismo Mister Graphed lo vende a cincuenta de oro, a precio fijo, junto a pellejos prístinos, escamas prístinas y cristales arcanos.",
        "La comunidad lo leyó enseguida: es un tope de precio, para que nadie pueda pedir una fortuna por un loto en la subasta.",
        "Tiene sentido en un juego que se queda en el nivel sesenta para siempre: sin expansiones que reinicien la economía, alguien tiene que poner freno a los precios.",
        "Pero también vende dos materiales que no existían en el juego original: Fel Crystal y Stranglevine.",
        "Y si un mercado negro ya vende materiales para recetas que nadie ha visto, esas recetas están escondidas en algún sitio.",
    ]},
    {"id": "c05", "frases": [
        "Número cinco. Las Riendas de destrero de la muerte, la montura de Stratholme, ahora en subasta.",
        "Unos días después apareció junto a Mister Graphed la Casa de subastas del mercado negro, atendida por Madam Swyndle.",
        "Ahí nadie vende nada: Blizzard pone los lotes al azar, y gana la puja quien ofrezca más oro.",
        "Y en la primera captura que se compartió estaba la montura del barón Rivendare, con una puja de tres mil de oro.",
        "En el mismo lote había piezas de los primeros conjuntos de mazmorra por cuatrocientos de oro, y un gato de compañía por cien.",
        "En este canal ya te contamos lo difícil que era sacarla en Stratholme, con una probabilidad ridícula.",
        "Un jugador lo resumió así en Reddit: él hizo Stratholme solo más de setenta veces en la época del Rey Exánime para conseguirla.",
        "Ahora, con oro suficiente y un poco de suerte, hay otra puerta para conseguirla sin pisar Stratholme.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro. La Llave de piedra, que nadie sabe qué abre.",
        "Todo empieza en la Muralla de Thoradin, donde termina la cadena de la Bolsa de dormir: dentro de un cubo, sobre un tapiz quemado, hay una Página quemada.",
        "La página te manda a la entrada trasera de Entrañas, por las cloacas, donde hay un libro abierto entre escombros.",
        "El libro enseña tres dibujos: la Montaña Roca Negra, el Portal Oscuro y la Cresta de la Pluma de Fuego, en el cráter de Un'Goro.",
        "Junto a él hay una Página rota que dice «página ciento cincuenta y cinco», y un cuchillo que te da un Fragmento de piedra angular.",
        "Esa página ciento cincuenta y cinco existe de verdad: es la del manual oficial impreso, con un orco guerrero mirando un mapa del sur de los Reinos del Este.",
        "La siguiente pista costó muchas muertes: en los pasillos de la Montaña Roca Negra, un saco vigilado por un gruñido que, misteriosamente, no te ataca.",
        "Con el fragmento sacas la Llave de piedra. Y ahí se acaba lo que se sabe.",
        "Según algunos sitios, en un parche de la beta la llave cambió de sitio y apareció en Riverglades, detrás de un peón del Crepúsculo dormido.",
        "Los cazadores de secretos de Discord siguen buscando qué abre, y si la encuentras tú, cuéntanoslo antes que a nadie.",
    ]},
    {"id": "c03", "frases": [
        "Número tres. Shen'Serrar, la espada que salió en el pódcast oficial antes que en el juego.",
        "En el sexto episodio del pódcast de World of Warcraft Forever, detrás de Josh Greenfield, conocido como Aggrend, había una pizarra.",
        "Y en la pizarra, escrito en élfico, decía: Shen'Serrar lezal melor'na adala fal.",
        "Los jugadores la tradujeron enseguida: Shen significa oculto, la palabra que aprendimos con los Skyborne.",
        "Y Serrar significa hoja, la misma palabra de Quel'Serrar, la espada que se forjaba con el aliento de Onyxia.",
        "El resto se parece a un dicho élfico conocido, «la verdad es una luz que guía», así que la frase podría ser «la hoja oculta es nuestra luz guía».",
        "Y Quel'Serrar era justo eso: una cadena que empezaba con un libro y terminaba frente a Onyxia.",
        "Lo inquietante es la fecha: la Guarida de Onyxia vuelve en Forever el nueve de diciembre.",
        "Una hoja oculta, un dragón y un desarrollador que justo se sentó delante de esa pizarra: no creo que sea casualidad.",
    ]},
    {"id": "c02", "frases": [
        "Número dos. Las setenta y cinco monturas que todavía no ha visto nadie.",
        "En Forever, las monturas, mascotas, juguetes y apariencias que no tienes ni siquiera salen en tu colección: están ocultas hasta que las consigues.",
        "Y al contar lo que Blizzard escondió en los datos, salieron setenta y cinco monturas que todavía no aparecen por ningún lado.",
        "También mil setecientos setenta y tres hechizos que nadie ha visto en acción.",
        "Solo del Núcleo de Magma hay ciento treinta objetos del juego original con las estadísticas escondidas.",
        "Durante la beta se revelaron cuatro mil cuatrocientos diecinueve objetos ocultos, y aún quedan más de ocho mil.",
        "O sea que lo que viste en este video es, como mucho, un tercio de lo que hay.",
        "Y cada montura que aparezca va a tener un primer dueño en el mundo, y ese podrías ser tú.",
    ]},
    {"id": "c01", "frases": [
        "Número uno. El primer legendario de Forever, escondido a plena vista.",
        "En los datos de la beta hay un objeto legendario que se consigue con una misión, pero con el nombre borrado y las estadísticas cifradas.",
        "Lo que no pudieron borrar fueron las pistas a su alrededor, y los mineros de datos las fueron juntando una a una.",
        "Hay un ritual con el Círculo Cenarion, con una facción propia de evento legendario y un efecto llamado éxito del ritual legendario.",
        "Hay efusiones de luz lunar en los pozos de la luna, un Don de Cenarius y un estado llamado cargado de tormenta.",
        "Hay encuentros en la Cima de Hyjal con Sylvestris Dusksong, y un Stormwraith que no aparece en la lista de jefes de la banda.",
        "Y una teoría muy buena: ese Stormwraith quizá solo aparece si alguien del grupo va cargado de tormenta, como un modo difícil secreto.",
        "Hay combates que se hacen en solitario, una conversación con sátiros en Claro de la Luna y un puzle de pilones en el cráter de Un'Goro.",
        "Y hay un mapa de un solo jugador llamado la caída de Archimonde, con el efecto de cielo oscurecido del propio Archimonde.",
        "El objeto que se potencia en el ritual es la Rama del Árbol del Mundo, con seis recipientes.",
        "Así que todo apunta a un bastón legendario de sanador, para druidas, chamanes y sacerdotes.",
        "Blizzard anunció la primera cadena legendaria para la primavera de dos mil veintisiete, con dos bandas nuevas.",
        "Todo esto es especulación sobre datos de la beta, pero la primera pieza ya la puedes pisar: Hyjal Summit abre el nueve de diciembre.",
    ]},
    {"id": "cierre", "frases": [
        "Y esos son los quince objetos secretos de World of Warcraft Forever que nadie te explica.",
        "Un hacha que mina, una banana que entiende de bosques, un mercado negro, una llave sin puerta y un legendario sin nombre.",
        "Ahora cuéntame en los comentarios: ¿qué secreto vas a ir a buscar primero, ahora que el juego sale hoy?",
        "Y si encuentras algo que no salió aquí, déjalo abajo: todos los comentarios se leen, y el tuyo puede ser el próximo video.",
        "Nos vemos en la próxima crónica, y nos vemos en Azeroth.",
    ]},
]
