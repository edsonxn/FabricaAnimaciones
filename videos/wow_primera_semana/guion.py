# -*- coding: utf-8 -*-
"""GUION — «Las 10 cosas que DEBES hacer la primera semana de WoW Forever» (Crónicas de Warcraft, 28-oct-2026).
Motor SECUENCIA YT (gameplay de YouTube por beat). Flujo y reglas: docs/estilo_secuencia_yt.md
Investigación con fuentes: videos/_investigacion_wow_primera_semana.md (nada de cifras fuera de ahí; lo de la beta se dice «en la beta»).

Tema elegido por el usuario (28-oct) entre 3 propuestas: lista para quien empieza Forever; sale el dom 1-nov 09:00 CDMX,
3 días ANTES del lanzamiento (4-nov): todo en futuro, nada de «ya salió». Mínimo 14 min (el usuario).
ABRE la campaña de Overgear de noviembre (fechas 1, 4, 5, 7 y 9-nov): coaching self-play de Forever tras el n.º 8.
Comentarios reales (regla del 28-oct): @FedeArgentina en el gancho, 2 de agradecimiento tras el patrocinio, @yuno.nvn en la
cocina, 6 de Darrowshire juntos en el anuncio y 2-3 en el cierre; la voz recuerda que todos se leen y se toman en cuenta.
Anuncio del usuario (28-oct): las historias contadas (Darrowshire) se mudan a otro canal; video largo en preparación.

Voz Applio: frases de < ~200 caracteres y nunca sueltas de 1-3 palabras; todo nombre inglés en FONETICA.
"""

TITULO = "Las 10 cosas que DEBES hacer la primera semana de WoW Forever"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "Battle punto net": "Bátel punto net", "Hardcore": "Jardcor", "Burning Crusade": "Bérnin Kruséid",
    "CRONICAS10": "Crónicas diez", "WoW": "uórld of uárcraft", "MMO": "eme eme o", "addons": "ádons",
    # lugares
    "Barrow Deeps": "Bárou Díps", "Hyjal Summit": "Jáyal Sámit", "Hyjal": "Jáyal", "Onyxia": "Oníxia",
    "Loch Modan": "Loc Módan", "Thoradin": "Toradín", "Alexston": "Álexton", "Durotar": "Durotár",
    "Hall of Thanes": "Jol of Zéins", "Ruins of Lordaeron": "Rúins of Lordéron", "Darrowshire": "Dárroushair",
    # gente, sistemas y cosas
    "Clay Stone": "Cléi Stóun", "Josh Greenfield": "Yosh Grínfild", "Mein MMO": "Main eme eme o", "Method": "Mézod",
    "Cultivation": "Coltivéishon", "Durgen Dirgehammer": "Dúrguen Dérgjamer", "Legacy": "Légasi", "Wiley": "Uáili", "Shaper's Terrace": "Shéipers Térras", "Un'Goro": "Un Góro", "Legolas": "Légolas", "Auberdine": "Óberdin", "Menethil": "Menezíl",
}

# Nombres propios que Whisper escribe distinto (Barrow Deeps→Barodips, Hall of Thanes→Hall of Saints, Wiley→Uahili…): aceptados (28-oct)
CER_MAX_POR_FRASE = {k: 0.15 for k in ['c08_5', 'c08_6', 'overgear_0', 'overgear_1', 'c07_6', 'c06_3', 'c05_0', 'c05_1', 'c05_7', 'c05_8', 'c04_2', 'c04_3', 'c03_6', 'c03_9', 'anuncio_1', 'c04_5', 'cierre_4']}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos se fijan tras `tiempo`; en el anuncio, música promo
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 28-oct, 875,6 s); OST ORIGINAL de WoW que el canal no ha usado: `musica_wow.py`
        (['intro', 'c10'], 'Legends of Azeroth'),   # 0-105 s     gancho e invitación
        (['c09'], 'Dun Morogh'),                    # 105-182 s   la hora y la cola
        (['c08'], 'Durotar'),                       # 182-245 s   la bolsa de dormir
        (['overgear'], 'Durotar'),                  # 245-302 s   patrocinio (suena la música promo)
        (['gracias', 'c07'], 'Feralas'),            # 302-382 s   comentarios y libros
        (['c06'], 'Dun Morogh'),                    # 382-458 s   cocina
        (['c05'], 'Durotar'),                       # 458-533 s   recolección y oro
        (['c04'], "Un'Goro"),                       # 533-608 s   mazmorras nuevas
        (['c03'], 'Feralas'),                       # 608-680 s   Legacy
        (['c02'], "Un'Goro"),                       # 680-747 s   tipo de servidor
        (['c01'], 'Dun Morogh'),                    # 747-810 s   nombre y apellido
        (['anuncio'], 'Tierras de la Peste del Este'),  # 810-847 s   Darrowshire se muda
        (['cierre'], 'Legends of Azeroth'),         # 847-876 s
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "El miércoles cuatro de noviembre abre World of Warcraft Forever, y la primera semana va a decidir cómo te va el resto del año.",
        "Porque en Forever no hay expansiones: el nivel sesenta es para siempre, y lo que hagas mal al principio se queda contigo.",
        "Hace unos días Fede nos escribió pidiendo ayuda para dar el primer paso en Forever, y no fue el único.",
        "Así que este video es para él y para todos los que nos lo pidieron en los comentarios.",
        "Y no son consejos genéricos: todo sale de lo que Blizzard ha confirmado y de lo que se vio en la beta, que terminó la semana pasada.",
        "Hoy te traigo las diez cosas que debes hacer la primera semana de World of Warcraft Forever, de la décima a la más importante.",
        "Y la número uno tiene fecha de caducidad: si no la haces antes del martes, ya no hay vuelta atrás.",
    ]},
    {"id": "c10", "frases": [
        "Número diez. Usa tu código de invitación, porque tu amigo puede jugar gratis justo la semana del lanzamiento.",
        "Los paquetes de Forever traen códigos de Invita a un amigo: el paquete Heroico trae uno, y el Épico y la colección traen tres.",
        "Con ese código, tu amigo juega sin suscripción del cuatro al once de noviembre.",
        "Siete días gratis para que descubra si lo suyo es la Alianza, la Horda o salir corriendo de Los Baldíos.",
        "Y si tu amigo ya juega, úsalo con ese otro que lleva años diciendo que vuelve en la próxima expansión. Esta vez no hay expansión que esperar.",
        "Y no es un detalle menor: en World of Warcraft casi nadie aguanta solo, y subir de nivel con alguien conocido lo cambia todo.",
        "Eso sí, elijan juntos el tipo de servidor antes de crear personaje, porque luego no se pueden mudar, y en el número dos te explico por qué.",
        "Pasado el día once, tu amigo tiene dos opciones: pagar la suscripción o convertirse en esa persona que nunca volvió a conectarse.",
    ]},
    {"id": "c09", "frases": [
        "Número nueve. Llega con la hora clara, el juego descargado y un plan B para la cola.",
        "Forever abre una sola vez para todo el mundo: el miércoles cuatro, a las tres de la tarde, hora del Pacífico.",
        "Eso son las cinco de la tarde en Ciudad de México, las seis en Bogotá y Lima, y las ocho en Buenos Aires y Santiago.",
        "En España será la medianoche del jueves cinco, así que si ves medios europeos diciendo cinco de noviembre, no se equivocaron.",
        "Y esa hora ya es la definitiva, porque Estados Unidos deja el horario de verano justo el uno de noviembre.",
        "Deja todo listo desde antes, porque ese miércoles medio planeta va a intentar entrar en el mismo minuto.",
        "La prueba de estrés del veintiuno de octubre empezó con errores para iniciar sesión, y Clay Stone, de Blizzard, ya avisó que la apertura puede tener tropiezos técnicos.",
        "Y las capas se quedan: Blizzard dice que siempre habrá algo de capas en sus servidores de gran capacidad.",
        "La buena noticia es que prometieron que ya no te separarán de tu grupo en el barco o el zepelín, ni al entrar a las capitales.",
        "La mala es que al cruzar de una zona a otra todavía puedes cambiar de capa, así que si el jabalí que perseguías desaparece, no fue magia.",
        "Y si la cola es eterna, aprovecha para leer los talentos rehechos de tu clase. Por lo menos que la espera te sirva de algo.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho. Consigue la Bolsa de dormir acogedora en cuanto llegues al nivel catorce.",
        "Es uno de los sistemas de la Temporada de Descubrimiento que vuelven en Forever, y en la beta funcionaba así.",
        "Duermes en ella y ganas un uno por ciento más de experiencia por cada minuto, hasta un tres por ciento.",
        "Se puede usar cada hora, cuenta como zona de descanso, y se suma a la comida y al campamento.",
        "Lo divertido es cómo se consigue: todo empieza con una nota clavada en una tabla, como si alguien hubiera perdido su lista del súper.",
        "Son seis misiones repartidas por cinco zonas, con un salto a la cornisa de la presa de Loch Modan y una escalada a la Muralla de Thoradin subido a una carreta.",
        "En la beta, la Alianza la empezaba en la granja de Alexston, en los Páramos de Poniente, y la Horda en unas ruinas al sur de Los Baldíos.",
        "Y la Horda la tiene peor, porque en Loch Modan la esperan guardias de nivel treinta que no aprecian a los turistas.",
        "Tres por ciento parece poco, pero sumado a lo demás de esta lista es la diferencia entre llegar al sesenta antes de las bandas o llegar tarde.",
    ]},
    {"id": "overgear", "post": 2.6, "frases": [
        "Y hablando de llegar a tiempo: el nueve de diciembre abren Barrow Deeps, Hyjal Summit y la Guarida de Onyxia.",
        "Entre el lanzamiento y esa fecha hay apenas cinco semanas, y casi nadie se atasca por ser malo, sino porque nadie le dijo qué estaba haciendo mal.",
        "Para eso está Overgear, que patrocina este video, con su coaching para World of Warcraft Forever.",
        "Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado te explica por voz en qué fallas y por qué.",
        "Talentos, rotación, addons, mazmorras nuevas, el plan de equipo antes de las bandas o duelos: tú eliges, y pagas solo las horas que necesites.",
        "Y como en Forever el equipo no caduca, los vicios de las primeras semanas se quedan contigo: corregirlos pronto sale más barato.",
        "El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    {"id": "gracias", "frases": [
        "Y antes de seguir, gracias por comentarios como estos, que nos dejan en cada video.",
        "Todos se leen, y todos se toman en cuenta para seguir mejorando el canal.",
    ]},
    {"id": "c07", "frases": [
        "Número siete. Empieza a juntar los libros de la biblioteca, porque ya no son solo cosa de magos.",
        "En la Temporada de Descubrimiento solo los magos los entregaban; en Forever, cualquier clase puede hacerlo.",
        "Hay cuarenta libros únicos repartidos por el mundo, y entregarlos da premios: a los diez, un collar, y a los veinte, un anillo.",
        "Y a los veinticinco, recompensas todavía mejores, así que cada libro cuenta.",
        "Si se repiten los sitios de la Temporada de Descubrimiento, uno está en las catacumbas del Bosque del Ocaso, rodeado de muertos vivientes de nivel veintiocho.",
        "Y otro, una guía para cuidar a tu mascota demoníaca, se podía despojar a través de los barrotes de una jaula sin abrirla.",
        "Pero hay un consejo que duele: si borras un libro, no vuelve a caer.",
        "Así que la primera semana, cuando la bolsa se te llene, tira cualquier cosa menos un libro.",
        "En la Temporada de Descubrimiento se entregaban en Ventormenta, en el Sanctum del Mago, y en Entrañas, en el Barrio Mágico.",
        "Cada libro que encuentras de paso mientras subes de nivel es un libro que no tendrás que salir a buscar cuando ya seas sesenta.",
    ]},
    {"id": "c06", "frases": [
        "Número seis. Cocina siempre, y come todavía más.",
        "En Forever, la comida cocinada da un cinco por ciento más de experiencia por cada monstruo que matas.",
        "Ojo, que es por muertes y no por misiones, pero en una subida del uno al sesenta se nota muchísimo.",
        "Según los cálculos de la web alemana Mein MMO, mantener ese bonus todo el tiempo te ahorra entre uno y uno y medio niveles.",
        "Hay quien nos cuenta que ve estos videos mientras come. Pues en Forever, comer también va a contar como progreso.",
        "A cambio, Blizzard bajó las estadísticas de la comida, y en el foro oficial ya hay quejas: ahora se come por la experiencia, no por la fuerza.",
        "Así que no vendas la carne de jabalí: cocínala.",
        "Y si vas a subir profesiones, en Forever hay más de seiscientas recetas nuevas repartidas entre todas.",
        "Y súmale el campamento: hacia el nivel cinco, un aventurero te enseña a encender una hoguera básica con espacio para tres objetos de profesión.",
        "Con las mejoras de Cocina, esa hoguera aguanta cinco y hasta diez objetos.",
        "Te sientas junto al fuego y ganas una mejora de una hora. En el MMO más famoso del mundo, descansar también es una estrategia.",
        "Comida, hoguera y bolsa de dormir juntas: ahí tienes la base de una subida más rápida que la de cualquiera que corra sin parar.",
    ]},
    {"id": "c05", "frases": [
        "Número cinco. Recolecta desde la zona inicial, y empieza a ahorrar desde el primer día.",
        "En Forever no hay Ficha de WoW ni subidas de nivel de pago, así que el oro de la primera semana sale literalmente del suelo.",
        "Minería, herboristería y desuello desde el primer día, porque al abrir la casa de subastas está vacía y todo se vende.",
        "Si eres tauren, tienes ventaja: su habilidad Cultivation duplica los nodos de hierbas.",
        "Y desollar los bichos que matan los demás también cuenta: el carroñero más rico de Durotar puedes ser tú.",
        "La meta es la montura, que en Forever se paga como en Burning Crusade: aprendes a montar y te dan la montura.",
        "En la beta costaba unos cien de oro a nivel cuarenta, y el paladín y el brujo la conseguían gratis con una misión.",
        "Mientras llegas a ella, activa cada maestro de vuelo que pases, porque en Forever no hay salas de portales como en el WoW moderno.",
        "Y hay barcos nuevos, como el de Ventormenta a Auberdine, sin tener que pasar por Menethil.",
        "Y guarda lo que te sobre, porque en la beta la montura épica de nivel sesenta costaba mil de oro, más doscientos por la montura.",
        "Y un truco para la de nivel cuarenta: si eres Honorable con tu facción, en la beta te salía un diez por ciento más barata.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro. Haz las mazmorras nuevas, y hazlas con todas sus misiones en una sola pasada.",
        "Forever trae nueve mazmorras nuevas, y la primera llega muy pronto.",
        "Para la Alianza es Hall of Thanes, de nivel trece a dieciocho, escondida debajo del salón del trono de Forjaz.",
        "Su jefe final, Durgen Dirgehammer, pelea acompañado de dos gólems de piedra, para que nadie diga que los enanos no saben decorar.",
        "La Horda tiene Ruins of Lordaeron, de nivel quince a veintidós, justo debajo de Entrañas.",
        "Y hay mazmorras nuevas hasta el sesenta, como Shaper's Terrace, en el cráter de Un'Goro.",
        "Y el cambio importante: los jefes que antes soltaban objetos únicos ahora sueltan azules.",
        "Además, la apariencia de un azul ligado de mazmorra se la quedan todos los que podían despojarlo, no solo el que gana la tirada.",
        "Entra con las misiones recogidas, porque según una guía de lanzamiento la experiencia buena está en las misiones y no en los monstruos de adentro.",
        "Una pasada bien hecha te da equipo, apariencia y experiencia de golpe, y te ahorra volver tres veces.",
        "Y apunta esto para después: Onyxia vuelve a pedir sintonización, personal y no de cuenta, así que en cuanto seas sesenta, empieza esa cadena.",
    ]},
    {"id": "c03", "frases": [
        "Número tres. Planea tus personajes secundarios desde el primer día, porque el sistema Legacy los premia.",
        "Legacy sustituye a los logros, y sus puntos son de cuenta: al lanzar hay sesenta y cinco, y cada personaje puede gastar dieciséis.",
        "Los ganas, por ejemplo, llevando cada clase a ciertos niveles, subiendo profesiones o explorando Azeroth.",
        "Y sirven en todos los tipos de servidor, menos en Hardcore, que va por su cuenta.",
        "Y en la beta las mejoras eran muy jugosas: vuelos a mitad de precio y más rápidos, talentos desde el nivel nueve, o habilidades sin componentes de vendedor.",
        "La recompensa de cincuenta y cinco puntos es una montura, el Oso espectral, y no te la entrega un héroe ni un rey.",
        "Te la da el tabernero Wiley, en Trinquete, como quien te cobra la cerveza.",
        "Y antes de esa montura hay más premios: un cachorro de oso espectral a los veinticinco puntos y un tabardo a los cuarenta.",
        "Es el único sistema de un MMO donde dejar a tu personaje principal en el nivel veinticinco cuenta como progreso.",
        "Así que si en la primera semana te aburres de tu clase, no la borres: ese personaje ya te está dando puntos.",
    ]},
    {"id": "c02", "frases": [
        "Número dos. Elige bien el tipo de servidor, porque en Forever no hay vuelta atrás.",
        "No hay lista de reinos: eliges un tipo de reglas, y cada uno es un solo reino enorme por región.",
        "Normal, jugador contra jugador, rol, y rol con jugador contra jugador, que Blizzard añadió el veintidós de octubre.",
        "El modo Hardcore llegará después del lanzamiento, así que no lo esperes el miércoles.",
        "Solo puedes agruparte y hacer mazmorras y bandas con gente de tu mismo tipo de servidor; los campos de batalla sí se mezclan.",
        "Y no hay transferencias: si te equivocas, toca empezar con un personaje nuevo.",
        "En Normal y en rol, en cambio, puedes tener personajes de la Alianza y de la Horda en la misma cuenta.",
        "En los servidores jugador contra jugador hay una regla todavía más dura: una sola facción por cuenta.",
        "Si creas un personaje de la Alianza, la Horda deja de existir para ti en ese servidor, y el motivo es que nadie haga un espía de la otra facción.",
        "La única forma de mudarse es morir en Hardcore, que ni siquiera está al lanzar. Así que pónganse de acuerdo en su grupo de amigos antes del miércoles.",
    ]},
    {"id": "c01", "frases": [
        "Y número uno. Reserva tu nombre y tu apellido antes del martes, o el miércoles en el primer minuto.",
        "En Forever los nombres tienen dos partes, nombre y apellido, y el ejemplo oficial de Blizzard es Ana Forever.",
        "Lo importante es que son únicos en toda la región, sin importar el tipo de servidor, y por ahora no hay cambio de nombre.",
        "Si compraste un paquete, puedes reservar hasta tres personajes hasta el tres de noviembre, en la cuenta donde lo compraste.",
        "Después de eso, gana el que llega primero, y media América quiere llamarse igual que tú.",
        "Las reglas, según la guía de Method: cada parte de dos a doce letras, sin números, guiones ni apóstrofos, y con acentos permitidos.",
        "Así que un Ramírez entra perfecto, pero nada de alargar la e de Legolas para colarte: la misma letra tres veces seguidas no está permitida.",
        "Y en los servidores de rol, el nombre tiene que sonar a una persona real, así que olvídate de Matajabalíes Supremo.",
        "Es lo único de esta lista que no se puede arreglar después, y por eso es el número uno.",
    ]},
    {"id": "anuncio", "frases": [
        "Y antes de despedirme, una noticia importante para el canal.",
        "Muchos de ustedes nos escribieron por la historia de Darrowshire, la de la niña que sigue esperando a su padre.",
        "Nos dijeron que les encantó el formato, que querían más historias así, y hasta nos pidieron el siguiente capítulo.",
        "Por eso tomamos una decisión: el formato de historias contadas se va a mudar a otro canal.",
        "Estamos preparando un gran video de larga duración con ese formato, y muy pronto les daremos noticias del canal donde se publicará.",
        "Y aquí, en Crónicas de Warcraft, seguimos con las listas, las curiosidades y todo lo que traiga Forever.",
    ]},
    {"id": "cierre", "frases": [
        "Y esas son las diez cosas que debes hacer la primera semana de World of Warcraft Forever.",
        "Gracias de verdad a todos los que comentan, como estos que nos dejaron hace poco.",
        "Todos los comentarios se leen, y todos se toman en cuenta para seguir mejorando.",
        "Ahora cuéntame abajo: ¿cuál va a ser tu nombre y apellido en Forever, y en qué tipo de servidor vas a jugar?",
        "Nos vemos en la próxima crónica, y el miércoles nos vemos en Azeroth.",
    ]},
]
