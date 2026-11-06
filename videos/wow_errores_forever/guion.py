# -*- coding: utf-8 -*-
"""GUION — «Los 25 ERRORES que estás cometiendo en WoW Forever (y cómo arreglarlos)» (Crónicas de Warcraft, 5-nov-2026).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Investigación con fuentes: videos/_investigacion_wow_errores_forever.md (nada de cifras fuera de ahí; C10 «comprar oro» FUERA por Overgear).
Tema elegido por el usuario (5-nov) entre 3 propuestas; 22 min; sale el sáb 7-nov (fecha Overgear, enlace /CRONICAS/4).
VOCES (el usuario, 5-nov-2026): COMPETENCIA DE VOCES como en Tamriel (tes_sentinel_teaser / tes_dwemer_desaparicion), las mismas
(Edoardo, José, Mario, Hope, MariCarmen, el Profeta y el Humano tras el Telón) pero SIN Johnny: en su lugar la de siempre de
Warcraft = Applio («Remy» en pantalla), que presenta y lleva gancho, Overgear, comentarios y 7 puestos (además, es gratis: saldo de
ElevenLabs justo el 5-nov). El público vota en los comentarios.
Frases de Applio: < ~200 caracteres, nunca de 1-3 palabras, sin corchetes; nombres ingleses en FONETICA_APPLIO.
Comentarios (≤ 10 días, ninguno usado antes): gancho @rodrigoespinoza2147 · voces @sebasmejia5019 (voz propia → el Humano) ·
gracias1 @brunomaidana9857 + @juandanielaguirreticona5266 · gracias2 @juliocesarguerrerohonorio3516 + @PedroGonzalez-wd4ot +
@desdeuruguay2049 · burla1 @adrianmoreno5431 · burla2 @GoldenAlfa922 (sin hablar mal del coaching) · n.º 1 @RatonX (su pregunta).
"""

TITULO = "Los 25 ERRORES que estás cometiendo en WoW Forever (y cómo arreglarlos)"
ARCHIVO = "wow_errores_forever"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), referencia=r"C:\chatterbox_voices\Sarcastica.mp3",
           por_cuenta={2: "GUEeiSJYQQdbv0NJ86Im", 3: "hCU4QZdzzUliy58ezPBz"})   # el Humano tras el Telón (clon del usuario) en las cuentas 2 y 3
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal
FONETICA = {"CRONICAS10": "Crónicas diez"}
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md)
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "Hyjal": "Jáyal", "CRONICAS10": "Crónicas diez", "Kotaku": "Kotáku", "Kalimdor": "Kalímdor", "Auberdine": "Óberdin",
    "Menethil": "Ménezil", "Riverglades": "Ríverglèids", "Zephras": "Séfras", "Valanaar": "Valanár", "Tanaris": "Tanáris",
    "Garon Wendell": "Gáron Uéndel", "Owen Thadd": "Óuen Zad", "Rumi": "Rúmi", "Gnomeregan": "Nomérigan",
    "Loch Modan": "Loj Módan", "Aggrend": "Ágrend", "Elwynn": "Éluin", "Familiar Faces": "Famíliar Féisis",
    "Waylaid Crates": "Uéileid Créits", "Rey Exánime": "Rey Exánime", "Crónicas de Warcraft": "Crónicas de uárcraft",
    "Crónicas de Tamriel": "Crónicas de Támriel", "Ventormenta": "Ventorménta", "JcJ": "jota ce jota",
}

# Nombres y cifras que Whisper escribe distinto (Kalíndor, Oberdin, Menesil, 7,5, Eduardo, «con H»): hipótesis leídas el 5-nov y aceptadas
CER_MAX_POR_FRASE = {'c25_1': 0.051, 'voces_0': 0.021, 'voces_1': 0.029, 'voces_4': 0.118, 'c02_4': 0.027, 'c02_5': 0.004, 'c04_1': 0.018, 'c08_2': 0.017, 'c10_3': 0.035, 'c13_3': 0.043, 'c13_5': 0.046, 'c16_3': 0.03, 'c18_0': 0.02, 'c18_1': 0.047, 'c18_2': 0.04, 'c18_3': 0.082, 'c19_0': 0.023, 'c19_1': 0.019, 'c21_5': 0.024, 'c24_2': 0.017, 'c25_0': 0.031, 'c25_2': 0.029, 'cierre_2': 0.03, 'cierre_5': 0.158, 'overgear_2': 0.017}
TAIL_MAX_POR_FRASE = {'c02_4': 0.45, 'c02_5': 1.08, 'c04_1': 0.3, 'c08_2': 0.65, 'c10_3': 0.3, 'c13_3': 0.3, 'c13_5': 0.3, 'c16_3': 0.37, 'c18_0': 0.3, 'c18_1': 0.38, 'c18_2': 0.3, 'c18_3': 0.3, 'c19_0': 0.3, 'c19_1': 0.3, 'c21_5': 0.32, 'c24_2': 0.3, 'c25_0': 0.3, 'c25_1': 0.3, 'c25_2': 0.3, 'cierre_2': 0.3, 'cierre_5': 0.3, 'overgear_2': 0.3}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="World of Warcraft Forever", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos se fijan tras `tiempo` (<= 175 s cada uno)
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 6-nov, 1440,6 s); música ORIGINAL de WoW: `musica_wow.py` corta un tema por tramo
        (['intro', 'c25'], 'Legends of Azeroth'),          # 0-130 s      gancho y presentación de las voces
        (['c24', 'voces', 'c23'], 'Orgrimmar'),                 # 130-262,5    Edoardo: brujo, fogata, piedra
        (['c22', 'c21', 'gracias1'], 'Ventormenta'),          # 262,5-385    José: preajuste (Elwynn), addons
        (['c20', 'c19', 'c18', 'burla1'], 'Darnassus'),       # 385-520      Remy: capas, barcos, Auberdine
        (['c17', 'c16', 'c15'], 'Durotar'),                   # 520-650      Mario: Baldíos, Bruce, mazmorras
        (['overgear'], 'Dun Morogh'),                         # 650-697,5    patrocinio (suena la música promo)
        (['c14', 'c13'], 'Entrañas'),                         # 697,5-777,5  equipo de lanzador, libros (Entrañas)
        (['c12', 'c11', 'c10', 'gracias2'], 'Dun Morogh'),    # 777,5-932,5  Hope: bolsa de dormir, campamento, legado
        (['c09', 'c08', 'c07', 'burla2'], 'Forjaz'),          # 932,5-1085   MariCarmen: profesiones, montura, oro
        (['c06', 'c05', 'c04'], 'Feralas'),                   # 1085-1207,5  el Humano, hermandad, cajas
        (['c03', 'c02'], 'Cima del Trueno'),                  # 1207,5-1317,5 el Profeta: favor (kodo), hechizos
        (['c01'], 'Núcleo de Magma'),                         # 1317,5-1382,5 reglas
        (['cierre'], 'Legends of Azeroth'),                   # 1382,5-1440,6 votación
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "World of Warcraft Forever salió el cuatro de noviembre, y fue de los lanzamientos más tranquilos que se recuerdan: colas de minutos y casi nadie desconectado.",
        "El problema no son los servidores. El problema somos nosotros: en la beta se crearon casi nueve millones de personajes, y más de un millón murió por una caída.",
        "Y ahora mismo, mientras ves esto, miles de jugadores venden al vendedor lo que mañana vale oro, o juegan sin las habilidades que ya pagaron.",
        "Como nos escribió un espectador, estos videos valen oro antes de meter la pata en Forever.",
        "Así que hoy te traigo los veinticinco errores que estás cometiendo en World of Warcraft Forever, y cómo arreglar cada uno, del veinticinco al uno.",
        "Algunos te cuestan oro, otros experiencia, y el número uno casi no tiene arreglo: si lo cometiste, te toca empezar de cero.",
    ]},
    # ================================================================ REMY (Applio) da los 2 primeros datos (el usuario, 6-nov)
    {"id": "c25", "frases": [
        "Número veinticinco. Eres brujo, y dejas que tu mascota tanquee como en el Classic de siempre.",
        "En las notas del lanzamiento, la vida que gana la mascota del brujo por cada punto de aguante bajó de siete coma cinco a dos.",
        "O sea, tu abisario ahora aguanta como una cortina.",
        "Y encima, los enemigos de nivel alto tienen más vida que en la beta: las peleas duran más, y tu mascota no llega al final.",
        "El arreglo: usa al abisario o al manáfago como apoyo, no como muro, y reparte la amenaza antes de que el élite te mire a ti.",
        "Lo sé. A mí tampoco me gusta trabajar.",
    ]},
    {"id": "c24", "frases": [
        "Número veinticuatro. Montar la fogata en cualquier sitio.",
        "En Forever la fogata no es decoración: es parte del campamento, y en los reinos de JcJ es un faro para los enemigos.",
        "Y además quema. En la beta, un trol de la Horda puso una justo donde aparecen los personajes nuevos.",
        "Los novatos morían durante la cinemática de inicio. Un jugador lo resumió así: me mató durante la introducción.",
        "No se sabe si Blizzard lo corrigió para el lanzamiento, así que el arreglo es sencillo: acampa en zonas seguras, o con tu grupo.",
        "Y no te quedes parado encima del fuego. Eso ya no es un error de Forever. Es un error de vida.",
    ]},
    {"id": "voces", "frases": [   # 6-nov: DESPUÉS de c24 y corta (~30 s), una frase por voz (el usuario: «si dura mucho, la gente se va»)
        "Y ahora, una noticia: hoy no narro solo. Siete voces de Crónicas de Tamriel compiten por mi puesto, y la que tú votes se queda.",
        "[deadpan] Edoardo. Me tocan el veintitrés y el veinte.",
        "José. El veintidós y el veintiuno, que yo también cometí.",
        "Mario. Diecisiete, dieciséis y quince. Sin correr. Casi.",
        "[amused] Soy Hope, con hache. El doce, el once y el diez.",
        "[deadpan] MariCarmen. Nueve, ocho y siete, con las cuentas hechas.",
        "El Profeta. Los tres últimos. Así está escrito.",
        "Y alguien pidió una voz propia. Aquí estoy: el humano tras el telón. Me toca el seis.",
        "El resto me lo quedo yo, que para eso juego en casa. Escucha a cada uno, y vota en los comentarios.",
    ]},
    # ================================================================ EDOARDO
    {"id": "c23", "frases": [
        "Número veintitrés. Esperar en la Piedra de encuentro a que alguien te invoque.",
        "En Forever no hay buscador de mazmorras: ni cola automática, ni grupo automático, ni teletransporte a la entrada.",
        "[deadpan] Y las Piedras de encuentro no invocan. Puedes quedarte ahí toda la tarde. Es una piedra.",
        "Lo único que trae a alguien es el Ritual de invocación del brujo, y necesita a dos ayudantes más junto a él.",
        "Lo que sí hay es el tablón de Buscar grupo del Classic, ahora con una opción obligatoria de estilo de juego.",
        "El arreglo: anuncia tu grupo en el tablón, ve caminando a la entrada, o hazte amigo de un brujo. [short pause] Para algo están.",
    ]},
    # ================================================================ JOSÉ
    {"id": "c22", "frases": [
        "Número veintidós. Elegir el preajuste Clásico sin saber lo que te quitas.",
        "La primera vez que entras, Forever te pide elegir entre dos: Mejorado o Clásico.",
        "Mejorado te marca en el mapa las misiones y sus objetivos, junta tus bolsas en una sola, y trae transfiguración y modelos en alta definición.",
        "Clásico lo apaga todo: sin zonas de misión en el mapa, las teclas vuelven a girar la cámara, y los modelos son los de dos mil cuatro.",
        "[amused] Mucha gente eligió Clásico por nostalgia, y ahora lleva media hora buscando cinco jabalíes en el bosque de Elwynn.",
        "El arreglo está en Opciones, Sistema, Preajuste: cambiarlo no toca a tu personaje, solo la presentación. Y Blizzard lo dice claro: si dudas, Mejorado.",
    ]},
    {"id": "c21", "frases": [
        "Número veintiuno. Llenar el juego de addons sin mirar quién los hizo.",
        "Forever ya trae de serie un medidor de daño y un gestor de reutilizaciones, en las Opciones avanzadas, y una guía de misiones.",
        "Y los addons tienen en combate las mismas restricciones que el World of Warcraft moderno: muchos de los viejos ya no hacen lo que prometen.",
        "Encima, salieron cientos de addons para Forever hechos con inteligencia artificial, y en Reddit los jugadores ya piden que los limiten.",
        "[amused] Sí, lo dice una voz hecha con inteligencia artificial. Por eso te lo digo con conocimiento de causa.",
        "El arreglo: primero lo que trae el juego, y después solo addons conocidos y mantenidos, como Questie, Auctionator o Details.",
    ]},
    {"id": "gracias1", "frases": [
        "Y antes de seguir, gracias por comentarios como estos, que nos dejan en cada video.",
        "Bruno dice que soy la mejor voz por inteligencia artificial que ha escuchado. Gracias, Bruno, que conste en el acta.",
        "[deadpan] Eso lo dijo antes de oírnos a nosotros.",
        "Todos se leen, y todos se toman en cuenta para mejorar el canal. Y a los malos comentarios les hacemos caso, pero a nuestra manera.",
    ]},
    # ================================================================ REMY (Applio)
    {"id": "c20", "frases": [
        "Número veinte. Pelear o perseguir a alguien justo en la frontera entre dos zonas.",
        "En Forever no hay reinos: hay megarreinos divididos en capas, y dos zonas vecinas pueden estar en capas distintas.",
        "Si cruzas la línea en plena pelea, el enemigo que perseguías desaparece, y la banda de tu facción que venía a ayudarte también.",
        "El día del lanzamiento, un periodista de Kotaku vio otro fallo: veía a los jugadores de otra capa, pero no a sus monstruos.",
        "O sea, sabía que algo le estaba pegando, pero no sabía qué era.",
        "El arreglo: no pelees en las fronteras y, al salir de una capital, comprueba que tus amigos siguen a tu lado.",
    ]},
    {"id": "c19", "frases": [
        "Número diecinueve. Subir al barco o al zepelín sin estar en grupo.",
        "En la beta, un viaje de Kalimdor a los Reinos del Este cambió de capa a mitad del mar.",
        "El veintitrés de octubre, Blizzard prometió que los grupos que viajen juntos ya no se separarían.",
        "Pero también avisó que siempre habrá algo de capas, y el día del lanzamiento se reportaron barcos y zepelines que no llegaban al muelle.",
        "Si viajas con tus amigos, formen el grupo antes de embarcar, y no lo cambien en una zona llena.",
        "Y si el barco no llega, no es que lo hayas perdido: está en otra capa, con otra gente esperándolo.",
    ]},
    {"id": "c18", "frases": [
        "Número dieciocho. Ir a Kalimdor por la carrera de la muerte de Los Humedales.",
        "Cualquier veterano de la Alianza se acuerda: para coger el barco a Auberdine había que cruzar Los Humedales a pie hasta el Puerto de Menethil.",
        "En Forever hay una ruta nueva: un barco directo del puerto de Ventormenta a Auberdine, en Costa Oscura.",
        "Y hay más rutas nuevas: un circuito entre Menethil, Costasur y Auberdine, otra de Tanaris a Riverglades, y otra a la Isla Zephras.",
        "Así que si vas a Costa Oscura con un personaje de nivel doce, ya no tienes que morir seis veces por el camino.",
        "Toma el barco en Ventormenta. Los cocodrilos de Los Humedales no te van a extrañar.",
    ]},
    {"id": "burla1", "frases": [
        "Y ya que hablamos de descubrir el mundo, aquí va una opinión con mucha pasión.",
        "Totalmente de acuerdo: descubrir es lo mejor de Forever, y por eso nunca te decimos dónde están los secretos.",
        "Solo te avisamos de que el barco no te espera. Descubrirlo a las tres de la mañana en un muelle vacío es una experiencia que preferimos ahorrarte.",
    ]},
    # ================================================================ MARIO
    {"id": "c17", "frases": [
        "Número diecisiete. Matar monstruos verdes y grises para subir más rápido.",
        "En Forever, Blizzard bajó a propósito la experiencia de los enemigos de menor nivel. Los jugadores calculan entre un cuatro y un veinte por ciento menos.",
        "[amused] Y los grises, como siempre, no dan nada. Ni las gracias.",
        "El diseñador Aidan Moon lo explicó: ahora hay bonos de comida y de campamento, y no querían que el camino fácil fuera el más rápido.",
        "Además, antes del lanzamiento subieron la vida de los monstruos de nivel alto. Limpiar un campamento de verdes tampoco es tan rápido.",
        "El arreglo: pelea con enemigos de tu nivel, y come antes. Bien alimentado te da un cinco por ciento más de experiencia durante unos quince minutos.",
    ]},
    {"id": "c16", "frases": [
        "Número dieciséis. Hacer grupo para las misiones de recoger cosas.",
        "En Forever, los objetos de misión no se comparten: si son cinco recogiendo plumas, cada uno tiene que encontrar las suyas.",
        "[amused] Cinco jugadores alrededor del mismo cofre es la forma más lenta de subir de nivel jamás inventada.",
        "Aggrend dijo que nunca digan nunca a compartir el botín, pero de momento no hay nada anunciado.",
        "Al revés, hay misiones pensadas para grupo, como el tiburón Bruce de Los Baldíos, que da unos dos mil puntos de experiencia.",
        "El arreglo: en grupo, misiones de matar y de élite; las de recoger, en solitario. [short pause] Y a Bruce, entre varios, que muerde.",
    ]},
    {"id": "c15", "frases": [
        "Número quince. Entrar a una mazmorra sin las misiones.",
        "En las notas del uno de octubre, las misiones de mazmorra pasaron a dar un cincuenta por ciento menos de experiencia extra.",
        "Y la experiencia de los monstruos de mazmorra subió alrededor de un veinte por ciento. Parece que da igual. No da igual.",
        "Las misiones siguen siendo lo que más experiencia da: en la beta, una vuelta a Brazanegra sin misiones dio unas tres barras.",
        "Y en Forever hay nueve mazmorras nuevas, como las Ruinas de Lordaeron, cuyas misiones empiezan al nivel quince.",
        "El arreglo: recoge todas las misiones antes de entrar. [short pause] Lo de correr por correr, déjamelo a mí.",
    ]},
    # ================================================================ OVERGEAR (Remy)
    {"id": "overgear", "post": 2.6, "frases": [
        "Y si sientes que vas cometiendo errores sin saber cuáles, para eso existe el patrocinador de hoy.",
        "Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.",
        "Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado te guía por voz.",
        "Casi nadie se atasca por ser malo, sino porque nadie le dijo qué estaba haciendo mal, y en Forever los vicios de las primeras semanas se quedan.",
        "Talentos, rotación, mazmorras nuevas, el plan para las bandas del nueve de diciembre o duelos: tú eliges, y pagas solo las horas que necesites.",
        "El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    # ================================================================ REMY (Applio)
    {"id": "c14", "frases": [
        "Número catorce. Ser mago, brujo o sacerdote y seguir usando equipo del Águila.",
        "En Forever bajaron el daño base de los hechizos, y subieron cuánto aprovechan el poder con hechizos.",
        "Traducido: sin poder con hechizos, pegas menos que en el Classic de siempre.",
        "Un jugador lo calculó en los foros: un veinticinco por ciento menos en la mayoría de los hechizos de daño directo.",
        "Por eso las armas de lanzador traen daño o sanación desde el nivel diez, y el equipo de sanador ahora también trae poder con hechizos.",
        "El arreglo: compara cada pieza nueva, y quédate con la que tenga poder con hechizos aunque la del Águila tenga más intelecto.",
    ]},
    {"id": "c13", "frases": [
        "Número trece. Pasar al lado de los libros de la biblioteca sin recogerlos.",
        "En la Temporada de Descubrimiento solo los magos podían recogerlos; en Forever los recoge cualquier clase.",
        "Hay unos cuarenta libros únicos repartidos por posadas, ruinas y torres de todo el mundo.",
        "Se entregan a Garon Wendell, en lo alto del Barrio de los Magos de Ventormenta, o a Owen Thadd, en el Barrio de la Magia de Entrañas.",
        "Con diez libros te dan un collar, con veinte un anillo, y con veinticinco un arma o un objeto de mano.",
        "Y un detalle: el libro de Rumi de Gnomeregan aparece en Loch Modan y en los Páramos de Poniente, pero solo cuenta una vez.",
    ]},
    # ================================================================ HOPE
    {"id": "c12", "frases": [
        "Número doce. Saltarte la Bolsa de dormir acogedora del nivel catorce.",
        "[amused] Al nivel catorce empieza una búsqueda del tesoro en un naufragio: en los Páramos de Poniente para la Alianza, y en Los Baldíos para la Horda.",
        "Aquí hay que hacer clic en los restos del barco, no matar monstruos esperando a que suelten algo.",
        "La cadena te lleva por varias zonas, como Loch Modan o las Laderas de Trabalomas, y al final te llevas la bolsa.",
        "Da hasta tres acumulaciones de un uno por ciento más de experiencia por muerte, y no se pierden al morir.",
        "Y cuenta como zona de descanso cuando te desconectas. [short pause] Una cama portátil. Lo que siempre quisimos.",
    ]},
    {"id": "c11", "frases": [
        "Número once. No usar el campamento.",
        "Hacia el nivel cinco, un aventurero a las afueras del primer pueblo te da la misión The Great Outdoors, y con ella se abre el campamento.",
        "Cada profesión tiene sus objetos de campamento: Sastrería pone un estandarte, Herboristería una vela de incienso, y Pesca, una pecera.",
        "Cada uno da un beneficio parecido a los de las clases, aunque no se acumula con el mismo beneficio de clase.",
        "La mejor es la tienda de Peletería: una hora de experiencia descansada que tampoco se pierde al morir.",
        "[amused] El arreglo: haz la misión, enciende tu fogata y siéntate un minuto. [short pause] Lejos del punto de aparición, por favor.",
    ]},
    {"id": "c10", "frases": [
        "Número diez. Gastar los puntos de Legado sin leer la letra pequeña.",
        "El sistema de legado es nuevo en Forever: es de toda la cuenta, y cada personaje puede gastar dieciséis puntos en el lanzamiento.",
        "Primera trampa: la ventaja Talento pide Bien descansado al máximo, cinco de cinco, así que en realidad cuesta diez puntos, no cinco.",
        "Segunda: Regateo te rebaja los vendedores, pero no el instructor de equitación.",
        "Tercera: Emoción de la aventura no hace nada dentro de mazmorras, bandas ni campos de batalla.",
        "[sarcastic] El arreglo: planea los dieciséis puntos antes de tocar nada. Como en la vida real, pero con más dragones.",
    ]},
    {"id": "gracias2", "frases": [
        "Y antes del número nueve, otra tanda de comentarios que nos alegraron la semana.",
        "Nos pidieron seguir añadiendo mapas, y por eso este video va lleno de ellos. Gracias: todos se leen, y todos se toman en cuenta.",
    ]},
    # ================================================================ MARICARMEN
    {"id": "c09", "frases": [
        "Número nueve. Llevar dos profesiones de recolección en tu personaje principal.",
        "[deadpan] El Legado da puntos por llegar a ciento cincuenta, doscientos veinticinco y trescientos en las seis profesiones de fabricación.",
        "Alquimia, Herrería, Encantamiento, Ingeniería, Peletería y Sastrería. Dieciocho puntos en total.",
        "La recolección no da ninguno. Ni la minería, ni la herboristería, ni el desuello.",
        "Según un cálculo con los datos de la beta, subir del uno al sesenta con dos de fabricación te da hasta once puntos. Con dos de recolección, cinco.",
        "El arreglo: si tu principal es recolector, que un alternativo suba fabricación. O al menos una de fabricación hasta doscientos veinticinco.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho. Pagar la montura del nivel cuarenta siendo brujo o paladín.",
        "La equitación de aprendiz cuesta cien de oro al nivel cuarenta, con la primera montura incluida.",
        "Pero los brujos de las dos facciones la consiguen con una misión de Strahad Farsan, en Trinquete.",
        "Y los paladines de la Alianza, con la misión del Tomo de la Nobleza, en Forjaz o en la Catedral de la Luz de Ventormenta.",
        "[deadpan] Si ya pagaste los cien, felicidades: tienes dos caballos. Uno de ellos, gratis.",
        "El arreglo: haz tu misión de clase antes de ir al instructor. Y si eres honorable con tu facción, la equitación te sale un diez por ciento más barata.",
    ]},
    {"id": "c07", "frases": [
        "Número siete. Gastarte el oro antes de tiempo.",
        "Entrenar tu clase del uno al sesenta cuesta unos doscientos siete de oro en todas las clases: el pase del lanzamiento lo igualó.",
        "Súmale la montura del cuarenta, la equitación de oficial y la montura épica: con los precios de la beta, unos mil trescientos de oro.",
        "Y en Forever no hay Ficha de World of Warcraft para cambiar dinero real por oro dentro del juego.",
        "[deadpan] Así que esa capa morada de la tienda de Ventormenta, déjala donde está.",
        "El arreglo: recolecta, vende en la subasta, y no compres caprichos en las capitales hasta tener la montura.",
    ]},
    {"id": "burla2", "frases": [
        "Y hablando de pagar, alguien nos dejó una reflexión muy profunda.",
        "Tienes razón en algo: aprender a jugar es lo más bonito de este juego, y por eso este video es gratis.",
        "Y si algún día quieres que alguien te lo enseñe en directo, tampoco pasa nada: hasta el Rey Exánime tenía a alguien que le hablaba al oído.",
    ]},
    # ================================================================ EL HUMANO TRAS EL TELÓN
    {"id": "c06", "frases": [
        "Número seis. Me toca a mí. No poner el idioma preferido en línea en español.",
        "Como en Forever no hay reinos, el juego intenta juntarte con gente que eligió el mismo idioma.",
        "Está en Opciones, Idiomas y redes sociales, Idioma preferido en línea. Y es de toda la cuenta.",
        "Si lo dejas en inglés, tus capas se llenan de gente que no te entiende cuando pides ayuda con el tiburón Bruce.",
        "Y ojo, que tiene un enfriamiento de veinticuatro horas: si lo cambias mal, esperas un día entero.",
        "El arreglo: ponlo en español hoy mismo. Y luego vota por mí, que soy el único humano de esta lista.",
    ]},
    # ================================================================ REMY (Applio)
    {"id": "c05", "frases": [
        "Número cinco. No entrar a una hermandad, y luego quejarte de que el mundo está vacío.",
        "El sistema de capas de Forever tiene una pieza llamada Familiar Faces, caras conocidas: intenta que los miembros de una hermandad siempre se vean.",
        "Y también te junta con la gente con la que ya te cruzaste por el camino.",
        "En el lanzamiento hubo zonas que se vaciaron a la media hora, y capitales con un puñado de jugadores.",
        "Aggrend reconoció en los foros que algunas zonas no se sienten tan pobladas como deberían, y Blizzard anunció ajustes para el seis de noviembre.",
        "El arreglo: entra a una hermandad de tu idioma cuanto antes. Y para juntarte con amigos, formen el grupo y acepten el aviso de refrescar el mundo.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro. Venderle al vendedor las cajas interceptadas, las Waylaid Crates.",
        "Son unas cajas que sueltan los enemigos, y que también se compran y se venden en la subasta.",
        "Si las llenas con los materiales que piden, te dan Favor de comerciante: entre cinco y veinte, según la caja.",
        "Y la primera caja que llenas puede traer una etiqueta de envío, que inicia una misión con cincuenta de favor y dos mil de reputación.",
        "Eso pasa una sola vez por personaje, así que esa primera caja vale mucho más de lo que te paga el vendedor.",
        "El arreglo: guárdalas y llénalas con una de las pilas que piden. Y para saber para qué sirve el favor, pasa al número tres.",
    ]},
    # ================================================================ EL PROFETA
    {"id": "c03", "frases": [
        "Número tres. Ignorar el Favor de comerciante. [short pause] El sistema más grande que trae Forever a las profesiones.",
        "Hay más de seiscientas recetas nuevas, y las mejores se compran con Favor, en los campamentos de comerciantes.",
        "La Alianza tiene el suyo en Three Corners, en las Montañas Crestagrana. La Horda, al oeste del Cruce, en Los Baldíos.",
        "Las recetas iniciales cuestan entre treinta y cuarenta y cinco de favor. Las de ingeniería, hasta trescientos sesenta.",
        "Y la montura del campamento, el Kodo de carga, cuesta seis mil de favor, reputación exaltada y nivel sesenta. [short pause] Así está escrito.",
        "El arreglo: desde el nivel diez, lleva tus cajas llenas al campamento. Marcy Baker, en Crestagrana, para la Alianza. Dokimi, en Los Baldíos, para la Horda.",
    ]},
    {"id": "c02", "frases": [
        "Número dos. Lo que ya no se pone solo.",
        "En las notas del dos de noviembre, dos días antes del lanzamiento, Blizzard cambió dos cosas pequeñas que cuestan mucho.",
        "Los hechizos que aprendes ya no se colocan solos en las barras de acción. Pagas al entrenador, y sigues jugando con lo de antes.",
        "Y además movieron niveles: la Furia justa del paladín se entrena ahora al nivel diez, y el pícaro aprende un ataque nuevo al veinticuatro.",
        "Las bolsas tampoco se equipan solas. Y Forever añade una quinta ranura, solo para una bolsa de componentes.",
        "El arreglo: después de cada entrenador, abre el libro de hechizos y arrastra lo nuevo. Y cada bolsa que saquees, clic derecho. [short pause] Lo vi venir.",
    ]},
    {"id": "c01", "frases": [
        "Número uno. Elegir conjunto de reglas o facción sin tus amigos.",
        "En Forever no hay reinos: hay cinco megarreinos por región. Normal, JcJ, Juego de rol, Juego de rol JcJ, y Extremo, que llegará más adelante.",
        "Y según Blizzard, no puedes cambiar libremente de conjunto de reglas. Para cambiarte, hay que crear un personaje nuevo.",
        "En JcJ, además, solo puedes tener personajes de una facción por cuenta. Y agruparte, entrar a mazmorras y a bandas, solo se puede con tus mismas reglas y tu misma facción.",
        "Un espectador nos lo preguntó: si empieza en JcJ y sus amigos están en Normal, ¿podrá pasarse? [short pause] No. Así está escrito.",
        "El arreglo: antes de pasar del nivel diez, confirma con tu grupo las reglas y la facción. Y si te equivocaste, empieza ya: el legado y las colecciones son de toda la cuenta.",
    ]},
    {"id": "cierre", "frases": [
        "Y esos son los veinticinco errores que estás cometiendo en World of Warcraft Forever, de una mascota de cartón a un reino sin vuelta atrás.",
        "Cuéntame en los comentarios cuál cometiste tú. Y ahora lo importante: vota. ¿Qué voz se queda en este canal?",
        "[deadpan] Edoardo. Te saqué de la Piedra de encuentro. Vota con gratitud.",
        "José. Yo también elegí el modo Clásico. Vótame por honesto.",
        "Mario. No corrí. Casi nada. Vótame.",
        "[amused] Hope. Con hache, y con campamento.",
        "[deadpan] MariCarmen. Te ahorré cien de oro. Haz cuentas.",
        "Yo no pido votos. El número uno ya era mío antes de que empezara el video.",
        "Y yo, el humano tras el telón. La única voz de esta lista que de verdad juega.",
        "Y yo soy la de siempre, y aquí sigo. Todos los comentarios se leen. Nos vemos en la próxima crónica, y nos vemos en Azeroth.",
    ]},
]

# --- COMPETENCIA DE VOCES (el usuario, 5-nov-2026): quién narra cada frase; lo que no sale aquí, Remy (Applio) ---
VOCES = {   # nombre en pantalla: voice_id (biblioteca compartida de ElevenLabs, salvo el Humano = clon del usuario; Remy = Applio)
    "Remy": "applio", "Edoardo": "YqZLNYWZm98oKaaLZkUA", "José": "y2ijeTfmnXjzheHO6zeN", "Mario": "tomkxGQGz4b1kE0EM722",
    "Hope": "tnSpp4vdxKPjI9w0GnoV", "MariCarmen": "YDDaC9XKjODs7hY78qEW", "el Profeta": "HNSF1CTQmub252yhXROX",
    "el Humano tras el Telón": "GUEeiSJYQQdbv0NJ86Im",
}
LEMAS = {"Remy": "La voz de siempre", "Edoardo": "El serio", "José": "El honesto", "Mario": "El que corre",
         "Hope": "Con hache", "MariCarmen": "La que hace cuentas", "el Profeta": "Así está escrito",
         "el Humano tras el Telón": "La voz de verdad"}
_POR_ESCENA = {"c23": "Edoardo", "c20": "Edoardo", "c22": "José", "c21": "José",
               "c17": "Mario", "c16": "Mario", "c15": "Mario", "c12": "Hope", "c11": "Hope", "c10": "Hope",
               "c09": "MariCarmen", "c08": "MariCarmen", "c07": "MariCarmen", "c06": "el Humano tras el Telón",
               "c03": "el Profeta", "c02": "el Profeta", "c01": "el Profeta"}
_POR_FRASE = {"voces_1": "Edoardo", "voces_2": "José", "voces_3": "Mario", "voces_4": "Hope", "voces_5": "MariCarmen",
              "voces_6": "el Profeta", "voces_7": "el Humano tras el Telón", "gracias1_2": "José",
              "cierre_2": "Edoardo", "cierre_3": "José", "cierre_4": "Mario", "cierre_5": "Hope", "cierre_6": "MariCarmen",
              "cierre_7": "el Profeta", "cierre_8": "el Humano tras el Telón"}
NARRA = {}   # "escena_i": nombre de la voz (efectos.py pone la placa de quién narra en cada cambio)
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k) or _POR_ESCENA.get(_e["id"], "Remy")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items()}
