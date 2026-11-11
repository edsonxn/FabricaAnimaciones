# -*- coding: utf-8 -*-
"""GUION v3 — «20 SECRETOS ESCONDIDOS de los primeros niveles de WoW Forever» (Crónicas de Warcraft, 10-nov-2026).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Investigación con fuentes: videos/_investigacion_wow_secretos_primeros_niveles.md (§ LISTA NUEVA + § v3 al final).
CAMBIO DE LISTA (el usuario, 10-nov): fuera las misiones que todo el mundo conoce (peones, gatos, Blanchy, Benedict, Sanders,
Cookie…). Dentro: secretos escondidos que nadie te indica (vara = ¡CLOC!), huevos de pascua del mapa (brazo de Terminator) e
historias reales detrás de PNJ conocidos (Kyle/Ezra). En ¡CLOC! se da PIENSO ESPECIAL PARA POLLOS, no avena.
Al INICIO: Gaia Eterna con 10-15 s de la Crematoria CON SU AUDIO (escena `gaia`, post); Overgear hacia el minuto 4. Sale mié 18-nov 09:00 CDMX.
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes. Textos del juego que no se oyen = «en el chat», nunca «dice/suena».
Comentarios (≤ 10 días, ninguno usado antes): gaia @zainzzgustavo @Vikussss · gracias1 @rickochetkezada @GalaxyImpact95
@Bajel_Barbossa · gracias2 @ChinoRoxs @klbcrash · gaia2 @sayhoml @Pausa_Thps (Bruno y Juan Daniel ya salieron en wow_errores_forever) · burla1 @alfredobueno4693.
"""

TITULO = "20 SECRETOS ESCONDIDOS de los primeros niveles de WoW Forever"
ARCHIVO = "wow_secretos_primeros_niveles"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "CRONICAS10": "Crónicas diez", "Crónicas de Warcraft": "Crónicas de uárcraft", "Elwynn": "Éluin", "Ventormenta": "Ventorménta",
    "Burning Crusade": "Bérnin Kruséid", "Hyjal": "Jáyal", "Questie": "Cuésti", "Discord": "Díscord", "Wowhead": "Uaujéd",
    "Remy": "Rémi", "Zephras": "Céfras", "Dawn Waker": "Don Uéiker", "Eluvi'ana": "Elubiána", "Eluvi'tor": "Elubitór",
    "Ban'aethal": "Banéezal", "Mystmane": "Místmein", "Den'dralass": "Dendrálas", "Coldrasp": "Cóldrasp",
    "Zendraas": "Zendrás", "Kyle": "Káil", "Ahab": "Ájab", "Ezra Chatterton": "Ésra Cháterton", "Make-A-Wish": "Méik a uísh",
    "Kaivax": "Káivax", "Saldean": "Sáldin", "Thrall": "Zrol", "Eitrigg": "Éitrig", "Grommash": "Grómash",
    "Arugal": "Árugal", "Gilneas": "Guilnéas", "Viktor": "Víctor", "Khara": "Kára", "Lordaeron": "Lordéron",
    "Mograine": "Mográin", "Mor'Ladim": "Mórladim", "Shen'dralar": "Shendrálar", "Tortheldrin": "Tortéldrin",
    "Pamela": "Pámela", "Darrowshire": "Dárouchair", "Gaia Eterna": "Gáia Etérna", "Gaia": "Gáia", "Alexandros": "Alexándros",
    "Tirion": "Tírion", "Taelan": "Teílan", "Darion": "Dárion", "Renault": "Renól",
    "Ealaane": "Ialáne", "Rorian": "Rórian", "Thendal": "Téndal", "Ailee Farheart": "Áili Fárjart", "Aquanis": "Acuánis",
    "Genn": "Guen", "Akir": "Akír", "Deepwater": "Dípuoter", "Wheathoof": "Uítjuf", "Zoram": "Zóram", "Cataclysm": "Cataclísm",
    # v3 (puestos nuevos)
    "Mountaineer Pebblebitty": "montañera Pébelbiti", "Pebblebitty": "Pébelbiti", "Marsellus Wallace": "Marsélus Uálas",
    "Pulp Fiction": "Pulp Fíkshon", "Eekum Bokum": "Íkum Bókum", "Banjo-Kazooie": "Bányo Kazúi", "Mumbo Jumbo": "Múmbo Yúmbo",
    "Bom'bay": "Bombéi", "Sen'jin": "Sényin", "Gadrin": "Gádrin", "Zalazane": "Zalazán", "Mankrik": "Mánkrik", "Olgra": "Ólgra",
    "Hearthstone": "Járzston", "Michel Koiter": "Mishél Kóiter", "Koiter": "Kóiter", "Twincruiser": "Tuín crúser",
    "Sullivan Ballou": "Súlivan Balú", "Sully Balloo": "Súli Balú", "Balloo": "Balú", "Thandol": "Tándol", "Dun Modr": "Dun Módor",
    "Moonrage": "Múnreich", "Silverlaine": "Sílverlein", "Faerleia": "Faerléia", "Morrison": "Mórrison", "Skynet": "Skáinet",
    "Cyberdyne": "Sáiberdain", "StarCraft": "Estárcraft", "Terminator": "Terminátor",
}
FONETICA = FONETICA_APPLIO
# Applio da siempre la misma toma: tolerancias revisadas a mano (10-nov, sesión 3; solo nombres propios/números)
CER_MAX_POR_FRASE = {'s12_8': 0.021, 'gaia_4': 0.037, 'gaia2_1': 0.022, 'gaia2_2': 0.06, 's20_1': 0.021, 's19_1': 0.057, 's19_5': 0.017, 's19_7': 0.043, 's18_0': 0.046, 's18_1': 0.04, 's18_7': 0.043, 's18_8': 0.065, 's18_9': 0.015, 's17_3': 0.036, 's17_4': 0.128, 'overgear_2': 0.015, 's16_0': 0.07, 's16_1': 0.028, 's16_2': 0.03, 's16_4': 0.028, 's16_5': 0.023, 's15_1': 0.047, 's15_4': 0.018, 's15_6': 0.037, 's14_0': 0.054, 's14_1': 0.036, 's14_5': 0.02, 's14_8': 0.021, 's13_1': 0.048, 's13_4': 0.026, 's13_7': 0.047, 's12_4': 0.03, 's12_6': 0.021, 's11_3': 0.027, 's10_3': 0.025, 's10_5': 0.028, 's10_6': 0.022, 's09_2': 0.038, 's08_3': 0.028, 'gracias2_2': 0.02, 's06_2': 0.015, 's06_4': 0.022, 's06_6': 0.028, 's06_7': 0.025, 's06_8': 0.095, 's05_0': 0.04, 's05_1': 0.055, 's05_2': 0.025, 's05_3': 0.034, 's04_3': 0.019, 's04_8': 0.028, 's03_1': 0.026, 's03_4': 0.029, 's03_5': 0.021, 's03_6': 0.028, 's03_8': 0.029, 's02_7': 0.021, 's01_0': 0.084, 's01_1': 0.016, 's01_3': 0.036, 's01_6': 0.048, 's01_9': 0.034, 's01_11': 0.037, 's01_12': 0.023}
TAIL_MAX_POR_FRASE = {'s12_8': 0.50, 's20_1': 0.41, 's19_7': 0.5, 's18_8': 0.73, 's14_1': 0.58, 's12_4': 0.48, 's10_3': 0.53, 's10_5': 0.87, 's10_6': 0.43, 'gracias2_2': 0.62, 's06_2': 0.5, 's05_3': 0.55, 's04_3': 0.43, 's03_4': 0.38, 's03_5': 0.53, 's02_7': 0.52, 's01_6': 0.79, 's01_12': 0.47}
# IDIOMA_LIBRE quitado (REGLA 10-nov-2026: la voz nunca habla en otro idioma; nucleo/idioma_voz.py oración por oración)

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-014": 0.9},          # se llena tras `beats`: el tramo de la Crematoria lleva el AUDIO del clip
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 10-nov, 1702,5 s); música ORIGINAL de WoW: `musica_wow.py` corta un tema por tramo
        (['intro', 'gaia', 'gaia2'], 'Legends of Azeroth'),        # 0-152
        (['s20', 'overgear'], 'Elwynn'),                            # 152-265 (Overgear: su música)
        (['s19', 's18'], 'Forjaz'),                                 # 265-397   Loch Modan, Sen'jin
        (['s17', 's16'], 'Bosque del Ocaso'),                       # 397-522   Tirisfal, Zephras
        (['s15', 'gracias1', 's14'], 'Baldíos'),                    # 522-687   Loch Modan, Mankrik
        (['s13', 's12'], 'Vallefresno'),                            # 687-817   Orgrimmar, Piroleña
        (['s11', 'burla1', 's10'], 'Ventormenta'),                  # 817-977   Gilneas, la carta
        (['s09', 's08'], 'Núcleo de Magma'),                        # 977-1100  Thandol por dentro, Lordaeron
        (['s07', 'gracias2', 's06'], 'Taberna'),                    # 1100-1265 estatua, Koiter
        (['s05', 's04'], 'Páramos'),                                # 1265-1410 Kyle, ¡CLOC!
        (['s03', 's02'], 'Bosque del Ocaso'),                       # 1410-1547 anillo, antorcha
        (['s01', 'cierre'], 'Legends of Azeroth'),                  # 1547-1702
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Durante la beta de World of Warcraft Forever, Blizzard hizo algo muy raro: apagó los secretos. Sobre todo, los de los primeros niveles.',
        'Uno de sus diseñadores lo dijo sin rodeos: hay cosas muy bien enterradas, y van a tardar en encontrarlas.',
        'Forever salió el cuatro de noviembre. Y en una semana, la gente ya empezó a desenterrarlas.',
        'Pero hoy no te voy a contar las misiones que todo el mundo hace. Hoy vamos a lo que nadie te indica.',
        'En lo hondo de una montaña hay un brazo de Terminator sobre un pedestal. Una estatua con los ojos rojos. Un guardia muerto que todavía te da una misión.',
        'Un pueblo entero que cambia de noche. Una carta real de una guerra de hace más de ciento cincuenta años, en el fondo de un río.',
        'Y un par de personajes que pasas a diario, y que esconden una historia real que casi nadie conoce.',
        'Veinte secretos de los primeros niveles, del veinte al uno. Todos con fuente, y casi todos con el sitio exacto en el mapa.',
        'Y te aviso desde ya: algunos se encontraron hace apenas unos días, así que puede que cambien con un parche.',
    ]},
    {"id": 'gaia', "post": 13.0, "frases": [
        'Pero antes, una noticia. ¿Se acuerdan de Darrowshire, y de Pamela, la niña que esperaba a su padre? Les dije que las historias se mudaban de canal.',
        'Ese canal ya existe. Se llama Gaia Eterna. Y su primer gran video ya está publicado: la historia completa de la Crematoria.',
        'Cuarenta y tres minutos. Dos padres, dos hijos y una espada maldita: Alexandros, Renault, Darion, Tirion y Taelan.',
        'Y Gustavo nos lo había pedido aquí mismo, en los comentarios: la de la familia Mograine. Gustavo, ya está. Y con todo.',
        'Tiene otra narradora, otra música y el mismo cuidado. Escucha con calma este pequeño pedazo.',
    ]},
    {"id": 'gaia2', "frases": [
        'Así suena Gaia Eterna. El enlace al video y al canal está en la descripción, y si te gustan las historias de lore, suscríbete allá también.',
        'Sayho escribió que le emocionaba lo del canal de historias, y Pausa, que estaba buenísimo. Pues ya está abierto, y es para ustedes.',
        "Y Vikussss, que pidió la de Mor'Ladim: anotada. Allá se cuentan las historias, y aquí seguimos con los secretos.",
        'Ahora sí, vamos con los veinte secretos. Empezamos.',
    ]},
    {"id": 's20', "frases": [
        'Número veinte. El vendedor que desapareció.',
        'En la Isla Zephras, la zona nueva de Forever, junto al Santuario de Akir, había un elfo disfrazado de sectario. Se llamaba Brother Zendraas.',
        'Estaba más o menos en cincuenta y ocho, cincuenta y dos, junto al santuario. Fácil de ver, si sabías que existía.',
        'Y no era un enemigo: vendía equipo de nivel bajo a cambio de piedras de viento, la moneda que se junta en la isla.',
        'Un sectario que no te ataca, y que además te vende cosas, ya es raro. Por eso los que lo vieron en la beta lo recuerdan.',
        'Después del lanzamiento, los jugadores fueron a comprarle, y no estaba.',
        'En el foro oficial hay un hilo entero preguntando por él. Unos dicen que lo quitaron, otros que aparece a ciertas horas.',
        'Blizzard no ha dicho nada. Y eso, en un juego donde apagaron secretos a propósito, da para pensar.',
        'Si lo encuentras en tu reino, cuéntalo en los comentarios con la hora. Puede que seas el primero.',
    ]},
    {"id": 'overgear', "post": 2.6, "frases": [
        'Y si encontrar secretos es divertido, llegar al sesenta sin vicios es otra historia. Para eso existe el patrocinador de hoy.',
        'Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.',
        'Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado te guía por voz.',
        'Una guía te explica la clase en general. Un buen coach mira tu personaje, y te dice qué estás haciendo mal y cómo arreglarlo.',
        'Talentos, rotación, mazmorras nuevas, el plan para las bandas del nueve de diciembre o duelos: tú eliges, y pagas solo las horas que necesites.',
        'El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.',
        'Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.',
    ]},
    {"id": 's19', "frases": [
        'Número diecinueve. La enana que no aguanta groserías.',
        'En el extremo sur de Loch Modan, en el Valle de los Reyes, hay una enana montando guardia: la montañera Pebblebitty.',
        'Vigila el túnel hacia la Garganta de Fuego. En Classic, ese paso tenía una reja, y la llave te la daba ella, pero solo a nivel cuarenta y tantos.',
        'Así que durante años, miles de jugadores de nivel bajo llegaron hasta ella, y se quedaron mirando una puerta cerrada.',
        'Y aquí está el secreto: si le haces el gesto de grosero, barra rude, no se queda callada. Te contesta en el chat.',
        'A veces escribe: sigue así y te enseño modales a golpes. Otras: estás tentando a la suerte.',
        'Y la mejor: no me obligues a ponerme medieval contigo.',
        'Esa frase es un guiño a Pulp Fiction, a la famosa amenaza de Marsellus Wallace. Una enana de Loch Modan citando a Tarantino.',
        'No da objeto ni experiencia. Pero cuesta un segundo, y casi nadie sabe que esa enana tiene respuestas guardadas.',
    ]},
    {"id": 's18', "frases": [
        "Número dieciocho. El médico brujo en prácticas de Sen'jin.",
        "En Durotar, en el Poblado Sen'jin, vive un trol joven llamado Bom'bay. Es el aprendiz del maestro Gadrin.",
        'Te cuenta que hace trabajo voluntario para pagarse la escuela de médicos brujos. Y que, a cambio, te ayuda gratis.',
        'Pero su ayuda es un maleficio al azar. La mayoría de las veces te convierte en un bicho, y lo quitas con clic derecho en el aura.',
        'Otras veces te emborracha, te vuelve fantasma, o te agranda durante cinco minutos.',
        'Y a veces te lanza por los aires. Ojo con eso: si la caída llega antes que el efecto de pluma, te puedes matar. Ve con la vida llena.',
        "Para que te hechice, antes tienes que haber completado la misión de Zalazane, el brujo de las Islas del Eco.",
        'Y aquí viene el huevo de pascua: mientras te transforma, a veces escribe en el chat: Eekum Bokum.',
        'Es el conjuro de Mumbo Jumbo, el chamán de Banjo-Kazooie. Y su nombre viene del doctor Bombay, el brujo de la serie Hechizada.',
        'Y su voz es la de los médicos brujos de Warcraft tres. Puede que sea el único trol del juego que la usa.',
    ]},
    {"id": 's17', "frases": [
        'Número diecisiete. Coldrasp, el lobo que nunca existió.',
        'En el Bosque Susurrante de los Claros de Tirisfal, la zona inicial de los no-muertos, aparece un lobo espíritu raro de nivel doce.',
        'Está al oeste de los Claros, no muy lejos de donde despiertan los no-muertos. Las coordenadas que comparten son diecinueve, sesenta y cinco.',
        'Se llama Coldrasp. Y no estaba en el juego original: es exclusivo de Forever.',
        'Llegó con la versión uno punto sesenta punto uno de Forever, así que es de lo más nuevo de esta lista.',
        'Es azul, translúcido, como un fantasma. Y lo mejor: se puede domar.',
        'Para un cazador de nivel doce, tener un lobo espíritu como mascota es de lo más raro que puedes enseñar en una capital.',
        'Es un raro, así que no siempre está. Si lo ves, no lo mates: dómalo.',
        'Y como es nuevo, ninguna guía de Classic lo menciona. Si buscas en las de siempre, no lo vas a encontrar.',
    ]},
    {"id": 's16', "frases": [
        'Número dieciséis. Mystmane, el oso más rápido de Zephras.',
        'En la Isla Zephras, la zona inicial de los cielonatos, hay un oso raro de nivel trece, nuevo en Forever.',
        'Y es nuevo de verdad: en el Classic de siempre, ese oso no existía. La Isla Zephras entera es nueva.',
        'Empieza en sesenta, treinta y tres, y desde ahí camina hacia el sur, hasta cincuenta y nueve, treinta y siete.',
        'Mystmane es el único oso domable con ataque rápido: golpea cada un segundo y medio, en vez de cada dos.',
        'Y además conoce Zarpazo, que pega hasta a tres enemigos a la vez.',
        "Ahora, la trampa. Hay otro oso idéntico en la isla, Den'dralass. Mismo modelo, mismo color. Mira el nombre antes de domarlo.",
        'Y Mystmane derriba, y el derribo te corta la doma. Te recomiendo ir con nivel catorce o quince, y empezar la doma desde lejos.',
        'Reaparece cada hora y media o tres horas. Así que paciencia, y nadie te garantiza que estés solo.',
    ]},
    {"id": 's15', "frases": [
        'Número quince. Plata de las olas.',
        'En Loch Modan, en el fondo del lago, hay una caja de herramientas de pesca abandonada.',
        'La caja está en las coordenadas cuarenta y cinco, cuarenta y tres. Y no la vas a ver desde la orilla: hay que meterse al agua.',
        'Para llegar hay que bucear, y abajo nadan trillones jóvenes de más nivel. Así que entra rápido y sal más rápido.',
        'Dentro hay un pasador de pelo de plata, con dos iniciales grabadas: K punto D punto.',
        'Dos letras en un pasador perdido, y ninguna flecha en el mapa. Así se esconde un secreto de los buenos.',
        'Esas iniciales son de Khara Deepwater, que está en la orilla del lago. Y el pasador empieza una misión oculta.',
        'Es una misión que no aparece en ningún tablón ni te la da ningún personaje: la empieza un objeto del fondo del lago.',
        'Se la devuelves, y te da una muñequera con intelecto y espíritu. Para un sacerdote o un mago de nivel bajo, vale la pena el chapuzón.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y antes de seguir, gracias por los comentarios del video de los add-ons.',
        'Ricochet escribió: Remy es todo, excelente trabajo. Y Galaxy, con muchos signos de exclamación: Remy, toda la vida.',
        'Y Bajel dice que la voz de siempre es un elemento esencial del canal. Así que Remy se queda, y se queda contento.',
        'Todos los comentarios se leen, y todos se toman en cuenta para mejorar el canal. Por eso sigo aquí.',
    ]},
    {"id": 's14', "frases": [
        'Número catorce. ¿Dónde está la esposa de Mankrik?',
        'En el Cruce, en Los Baldíos, hay un orco que no descansa: Mankrik. Los jabaespines lo atacaron, y su esposa no volvió.',
        'Su misión se recoge desde nivel catorce, y te pide algo muy simple: encontrar a su esposa, Olgra.',
        'El problema es que no hay flecha, ni marca, ni nombre. Tienes que bajar al sur del Cruce, cruzar un puente, y mirar frente a unas chozas.',
        'Y lo que encuentras no se llama Olgra. Es solo un cadáver tirado junto al camino, que mucha gente pasaba sin ver.',
        'Así nació el primer gran meme de World of Warcraft. En el chat de Los Baldíos, todo el mundo preguntaba lo mismo: ¿dónde está la esposa de Mankrik?',
        'Los Baldíos abarcaban quince niveles, así que cada personaje de la Horda veía la pregunta una y otra vez. Y muchos la hacían solo para molestar.',
        'El chat de Los Baldíos se volvió un meme por sí mismo, y hasta hubo camisetas.',
        'Blizzard quitó la misión en Cataclysm, y Mankrik acabó enterrando a su esposa y levantándole un monumento. Incluso salió en Hearthstone.',
        'Pero en Forever, la misión original sigue ahí. Ahora ya sabes dónde buscar. No le digas a nadie, que el chat sin esa pregunta no sería lo mismo.',
    ]},
    {"id": 's13', "frases": [
        'Número trece. Un orco que salió en la Crematoria.',
        'En Orgrimmar, dentro del Bastión de Grommash, junto a Thrall, hay un orco viejo: Eitrigg.',
        'Casi todos pasan a su lado sin mirarlo. Pero ese orco es parte de una de las historias más importantes de Warcraft.',
        'Años atrás, un paladín humano le salvó la vida, y por defenderlo lo perdió todo: sus tierras, su título y a su familia. Ese paladín era Tirion.',
        'Hoy, Eitrigg es consejero de Thrall, y está a su lado. Y la historia de cómo llegó ahí está entera en la Crematoria.',
        'Si viste la Crematoria en Gaia Eterna, ya sabes quién es. Si no, ve a verlo y luego pasa a saludarlo.',
        'Y desde nivel uno, cualquier personaje de la Horda puede entrar al Bastión y quedarse frente a él.',
        'Así que la próxima vez que entres a hablar con Thrall, no pases de largo: saluda a Eitrigg.',
    ]},
    {"id": 's12', "frases": [
        'Número doce. El pueblo que cambia de noche.',
        'En el suroeste del Bosque de Argénteos está la Aldea Piroleña, un pueblo humano tranquilo, con su herrero, su sastre y su consejo.',
        'De día, son humanos. Pero cuando el reloj del servidor marca las nueve de la noche, el pueblo entero cambia.',
        'Ojo: las nueve de la hora del servidor, no de la tuya. Si juegas en un reino de otro país, haz la cuenta.',
        'El anciano, el centinela, el vigía y el armero de Piroleña se convierten en huargen Moonrage, y atacan a cualquiera, sea de la facción que sea.',
        'La culpa es del archimago Arugal. Desde el castillo que domina el pueblo, el que hoy es Colmillo Oscuro, maldijo a sus vecinos.',
        'Y la Horda tiene misiones ahí, de nivel quince. La acechadora Faerleia te manda a emboscar al consejo del pueblo y a su alcalde, Morrison.',
        'Ahora imagina llegar de noche a hacer esa misión, y encontrarte con un pueblo lleno de huargen en lugar de humanos.',
        'Blizzard quitó todo esto en Cataclysm, cuando los huargen pasaron a ser una raza que puedes elegir. Pero en Forever, la maldición sigue.',
        'Así que si pasas por Piroleña, mira la hora del servidor. A las nueve, los vecinos dejan de ser vecinos.',
    ]},
    {"id": 's11', "frases": [
        'Número once. Un reino entero, sellado.',
        'Al sur del Bosque de Argénteos, una zona de nivel diez a veinte, hay un muro gigantesco: el Muro de Cringris.',
        'Detrás está Gilneas, el reino que se encerró a sí mismo durante la guerra.',
        'Se llama así por Genn Cringris, el rey que prefirió encerrar a su gente antes que seguir en la Alianza.',
        'En el juego original, ese muro era solo decorado. Pero en Forever, Gilneas está en los archivos del juego, como una zona sellada.',
        'Y no está vacía: los que revisaron los archivos encontraron una fila de campo de batalla para diez jugadores.',
        'Todavía no se puede entrar. Pero a nivel quince ya puedes plantarte frente al muro, y pensar en lo que viene.',
        'Y para los que jugamos Cataclysm, ver ese muro cerrado otra vez tiene algo especial: sabemos lo que hay detrás.',
    ]},
    {"id": 'burla1', "frases": [
        'Y ahora, una crítica de las que nos gustan.',
        'Alfredo escribió: qué asco de inteligencia artificial, todos los comentarios son bots, internet está muerto.',
        'Alfredo, tranquilo. Ningún bot escribiría Maricarmen tío en una votación de voces. Esos son humanos, y bastante creativos.',
        'Y si internet está muerto, Alfredo, entonces tú acabas de comentar en un cementerio. Bienvenido. Aquí hay muchos secretos.',
    ]},
    {"id": 's10', "frases": [
        'Número diez. Una carta en el fondo del río.',
        'Entre Los Humedales y las Tierras Altas de Arathi está el Puente de Thandol, un puente enano gigantesco. Los Humedales empiezan en el nivel veinte.',
        'Si te tiras al agua y buceas bajo el puente, encuentras un cadáver. Y con él, un sobre empapado.',
        'Es la carta de un soldado, Sully Balloo, para su esposa, Sara Balloo, que vive en Forjaz. Y empieza una misión: llevársela.',
        'La carta empieza así: mi querida Sara. Y termina: Sara, no me llores muerto. Piensa que me fui, y espérame, porque nos volveremos a ver.',
        'Y aquí está la historia real. En julio de mil ochocientos sesenta y uno, un mayor del ejército de la Unión, Sullivan Ballou, le escribió a su esposa, Sarah.',
        'Fue una semana antes de la primera batalla de Bull Run, en la Guerra de Secesión de Estados Unidos. Y Sullivan murió en esa batalla.',
        'Su carta es una de las más famosas de esa guerra. Y Blizzard la convirtió en la carta de un enano ahogado bajo un puente.',
        'Y no es casualidad que sea un enano: los Hierro Negro y los de Forjaz llevan doscientos años enfrentados desde su propia guerra civil.',
        'La misión se quitó del juego actual en Cataclysm. En Forever sigue ahí, esperando a que alguien se moje.',
    ]},
    {"id": 's09', "frases": [
        'Número nueve. El brazo de Terminator, y un mito que se repite.',
        'Muchas listas dicen que está dentro del Puente de Thandol, entre Los Humedales y las Tierras Altas de Arathi.',
        'Y es verdad que el puente es hueco, y que una misión de Dun Modr te mete en sus salas a buscar a un enano desaparecido.',
        'Pero recorrí esas salas de punta a punta, y ahí no hay ningún brazo. Lo encontré en otro sitio, mucho más lejos.',
        'En la parte baja de la Cumbre de Roca Negra, en un rincón, hay un pedestal. Y encima, un brazo mecánico de metal.',
        'Es el brazo del primer Terminator. En Terminator dos, ese brazo se guarda en una vitrina, en el laboratorio de la empresa que acaba creando a Skynet.',
        'Un brazo de metal, en un juego de espadas y magia. Y nadie en el juego explica qué hace ahí.',
        'Y cuando le hice clic para cogerlo, desapareció delante de mí, y nunca llegó a mi bolsa.',
        'Es el único de esta lista que no es de nivel bajo: la Cumbre de Roca Negra es para el nivel sesenta. Pero el mito empieza en un puente de nivel veinte.',
        'Así que si llegas a la Cumbre, busca el pedestal. Y si alguien encuentra ese brazo en el Puente de Thandol, que lo cuente con captura.',
    ]},
    {"id": 's08', "frases": [
        'Número ocho. La chimenea de Viktor.',
        'Forever trae mazmorras nuevas, y una de ellas está sobre Entrañas: las Ruinas de Lordaeron, para los niveles quince a veinte.',
        'Es la capital caída donde Arthas mató a su padre. Y escondidos en sus ruinas hay dos jefes que no aparecen si no los buscas.',
        'El primero está en una casa abandonada, junto a la plaga morada, después del Barón.',
        'Dentro, en la chimenea, hay leña tibia. Le haces clic, y empiezan las oleadas.',
        'Son cinco oleadas. Y al terminar, aparece Viktor el Vil, uno de los jefes secretos de la mazmorra.',
        'Cuántas oleadas son exactamente, y cuál es la casa, todavía se discute en la comunidad. Así que, como siempre en Forever, a explorar.',
        'Es una casa más entre muchas, así que la pista es la chimenea: si ves leña rara dentro, ya la encontraste.',
    ]},
    {"id": 's07', "frases": [
        'Número siete. La estatua que te mira.',
        'El segundo jefe secreto de las Ruinas de Lordaeron está a la vista de todos. Y casi nadie lo ve.',
        'La mazmorra está arriba, en las ruinas de la ciudad. Y debajo, en las cloacas, está Entrañas, la capital de los Renegados.',
        'En una esquina del oeste de las ruinas hay una estatua con los ojos rojos, brillando.',
        'Si te acercas, llegan tres oleadas de enemigos. Y después, aparece el jefe secreto: El Abandonado.',
        'Y el nombre le queda perfecto: abandonado por todos los grupos que van con prisa.',
        'La mayoría de grupos pasan de largo. Si tu grupo va con prisa, convéncelos. Una estatua que te mira no es decoración.',
        'Dos jefes ocultos en una mazmorra de nivel quince. Eso es lo que Blizzard escondió durante la beta.',
        'Y si lo derrotas, presume: muchos grupos de Forever ni saben que existe.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y otra ronda de comentarios, porque se la ganaron.',
        'Chino, que apenas empieza en WoW, dice que estos videos son una gran guía. Bienvenido, Chino: este video es justo para ti.',
        'Y Klb nos cuenta que Favorcraft, el add-on que tenía ciento noventa y dos descargas, ya va por trescientas ochenta. Gracias por recomendarlo, dice.',
        'Así que si este canal puede duplicar las descargas de un add-on, imagínate lo que pasa si compartes este video. Todo se lee, y todo suma.',
    ]},
    {"id": 's06', "frases": [
        'Número seis. El santuario del guerrero caído.',
        'En Los Baldíos, en una loma al oeste del Cruce, hay un sitio que casi nadie visita, porque no hay misión que te lleve.',
        'Se sube por la ladera del suroeste, y arriba hay un obelisco de piedra. En su base, dos letras grabadas: M K.',
        'Junto al obelisco hay una estatua de un orco con un mandoble. Y delante, un sanador espiritual, que se llama Koiter.',
        'Michel Koiter era uno de los artistas de Blizzard. Trabajaba junto a su hermano gemelo, René, y firmaban juntos como Twincruiser.',
        'Murió en marzo de dos mil cuatro, por un fallo del corazón inesperado. Tenía diecinueve años. World of Warcraft todavía no había salido.',
        'La estatua de ese orco es una copia exacta del personaje que Michel jugaba en la beta, Twincruiser.',
        'Y el sanador lleva su apellido. Así que si mueres en esa parte de Los Baldíos, quien te devuelve a la vida es Koiter.',
        'Blizzard lo volvió a recordar en StarCraft dos: tras una batalla, Raynor recoge la placa de un marine caído. Dice M. Koiter.',
        'La próxima vez que cruces Los Baldíos, sube a la loma. Es el homenaje más silencioso de todo el juego.',
    ]},
    {"id": 's05', "frases": [
        'Número cinco. Un perrito llamado Kyle ha desaparecido de su casa.',
        'En Mulgore, en el Poblado Pezuña de Sangre, un tauren llamado Ahab Wheathoof perdió a su perro, Kyle.',
        'La misión te pide carne tierna de zancudo, para dársela a Kyle cuando lo encuentres corriendo por las praderas.',
        'Le das la carne, Kyle se calma, y vuelves con Ahab. Una misión sencilla, de las de antes. Mucha gente la hizo sin saber nada más.',
        'Y ahora, la historia de verdad. En dos mil siete, un niño de trece años, Ezra Chatterton, visitó Blizzard gracias a Make-A-Wish.',
        'Ezra tenía cáncer cerebral. Ayudó a diseñar esta misión, y le puso su propia voz a Ahab.',
        'Ezra murió poco después de su visita. Pero su misión sigue en el juego. Y ahora, también en Forever.',
        'Como la misión era de Burning Crusade, no estaba en la base de Forever. Los jugadores lo pidieron en el foro oficial.',
        'Kaivax, de Blizzard, contestó, y Kyle volvió a Mulgore en un parche de la beta. Se recoge desde nivel cinco.',
        'Así que si juegas tauren, no te la saltes. Es una misión de dos minutos, y la diseñó un niño que amaba este juego.',
    ]},
    {"id": 's04', "frases": [
        'Número cuatro. El huevo de gallina de los Páramos. Este es el secreto con el que empezó todo.',
        'Busca un pollo en una granja, y hazle el gesto de la gallina, barra chicken. Nadie en el juego te dice que lo hagas.',
        'La forma más fácil es en la granja de los Saldean, en los Páramos de Poniente: hay pollos alrededor, y el pienso lo vende el mismo granjero.',
        'Una vez, y otra, y otra. Hasta que el pollo te mira raro, y te ofrece una misión: ¡Cloc!',
        'Para cumplirla necesitas pienso especial para pollos. En la Alianza, solo lo vende el granjero Saldean, ahí mismo, en su granja.',
        'En la Horda lo vende William Saldean, en Rémol. Los Saldean están en todas partes.',
        'Le das el pienso al pollo, y te deja un huevo. Y del huevo sale tu mascota: un pollo de los Páramos.',
        'Es de nivel uno. Un personaje recién creado puede tener su pollo antes que su primera espada decente.',
        'Ojo: la misión del pollo dura poco. Si no la aceptas rápido, se va, y vuelves a empezar con los cloc cloc.',
        'Y tranquilo: los demás jugadores te van a ver raro, haciéndole cloc cloc a un pollo durante dos minutos. Vale la pena.',
    ]},
    {"id": 's03', "frases": [
        'Número tres. El anillo heredado de Zephras.',
        'Los tres primeros puestos son, en realidad, el mismo secreto: el primer gran secreto de Forever, el Dawn Waker.',
        'Lo encontró la comunidad del Discord de cazadores de secretos, y Wowhead lo publicó esta semana.',
        'Wowhead lo llama, tal cual, el primer secreto de World of Warcraft Forever. Y todavía nadie lo ha resuelto.',
        'Empieza en la Isla Zephras, en el pueblo de Thendal. Ailee Farheart te da una misión: La mayoría de edad.',
        'Las coordenadas son cuarenta y dos, veintitrés, en Thendal. Y la misión es de nivel bajo: cualquier cielonato recién creado la puede hacer.',
        'La entregas a Rorian, un poco más allá, y te da un anillo: el Ancient Heirloom, una reliquia de familia.',
        'Y hay otra forma de conseguirlo: en el piso de arriba del edificio de al lado. Así que, si alguien llegó antes, mira arriba.',
        'Más adelante en la cadena, ese anillo hace visibles cosas que nadie más ve. Así que no lo vendas.',
        'Y una teoría de la comunidad lo une con la pizarra del pódcast oficial, de la que ya te hablé en el video de los objetos secretos.',
    ]},
    {"id": 's02', "frases": [
        'Número dos. La antorcha del guardia muerto.',
        'En el Bosque del Ocaso hay un guardia de la Guardia Nocturna, muerto, destrozado por alguna bestia.',
        'Y aunque está muerto, te ofrece una misión: Un final desafortunado. Requiere nivel uno, es para las dos facciones, y se entrega al instante.',
        'Le quitas de la mano una antorcha apagada. El texto dice que te servirá para revelar lo que esconde la oscuridad.',
        'Es un objeto de nivel uno, tiene treinta segundos de reutilización, y ocupa un hueco en la bolsa.',
        'Y esa es la queja de los comentarios en Wowhead: no hay pestaña de juguetes, así que la antorcha va en la mochila, con todo lo demás.',
        'El cuerpo no está siempre en el mismo sitio. Lo han encontrado en la cima del cementerio de la Colina del Cuervo, y en otros cinco lugares del bosque.',
        'Alrededor hay necrófagos de nivel veinticinco, así que con nivel bajo, entra con cuidado. Y Questie no te lo marca hasta que estás muy cerca.',
        'La antorcha ilumina cuevas y criptas en todo el mundo, menos en posadas y capitales. Pero su verdadero uso está en una isla del cielo.',
    ]},
    {"id": 's01', "frases": [
        "Número uno. Eluvi'ana, la espada del Dawn Waker.",
        "Con el anillo puesto y la antorcha en la mano, vuelves a la Isla Zephras, a las Ruinas de Ban'aethal.",
        'Usas la antorcha, y aparece una empuñadura antigua que antes no estaba ahí. Y con ella, una misión.',
        'Se la llevas a Ealaane, y te pide encontrar la hoja: una espada antigua de los cielonatos, en algún sitio de la isla.',
        'No tiene un lugar fijo. La han encontrado en cuatro puntos distintos, así que hay que recorrer Zephras con calma.',
        "Y cuando la llevas, te dan Eluvi'ana, una espada de una mano, de calidad poco común. Todo eso, en una zona de nivel uno a doce.",
        'Pero no termina ahí. La cadena sigue por Costa Oscura, Vallefresno, Feralas, Azshara, Cuna del Invierno y Hyjal.',
        'La segunda parte llega hacia el nivel veintidós: un globo de agua corrupto. La Alianza lo saca de los nagas de Costa Oscura, y la Horda, del Barón Aquanis en Brazanegra.',
        'Con el anillo puesto, en la Playa de Zoram aparece un espíritu altonato. Y en Feralas hay una bóveda que solo se ve con ese anillo, para cinco jugadores.',
        'Wowhead calcula que hace falta nivel cuarenta o más para completar la cadena entera. Lo de Zephras es solo el principio.',
        "Y al final, el príncipe Tortheldrin, en La Masacre, habla de dos espadas: Eluvi'ana y Eluvi'tor. Y dice que ese secreto es solo para los amigos de su corte.",
        "Algunos creen que al final pide reputación honorable con los Shen'dralar. Eso todavía no está confirmado.",
        'Nadie ha terminado el Dawn Waker todavía. Así que guarda esa espada poco común. Puede que sea la primera pieza de algo enorme.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esos son veinte secretos escondidos de los primeros niveles de World of Warcraft Forever, de un vendedor que desapareció a una espada que nadie entiende.',
        'Un brazo de Terminator, una carta de la Guerra de Secesión, un niño que le puso voz a un tauren, y un artista que tiene su santuario en Los Baldíos.',
        'Cuéntame en los comentarios cuál no conocías, y cuál encontraste tú. Todos se leen, y los mejores salen en el próximo video.',
        'Si alguno de estos secretos cambió en tu reino, o encontraste uno que no está aquí, déjalo en los comentarios con las coordenadas.',
        'Y no olvides pasar por Gaia Eterna: la historia de la Crematoria te está esperando, con el enlace en la descripción.',
        'Y si este video te sirvió, compártelo con ese amigo que acaba de empezar en Forever. Le ahorras horas.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
