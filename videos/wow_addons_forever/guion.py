# -*- coding: utf-8 -*-
"""GUION — «Los 20 ADD-ONS que necesitas en WoW Forever (y uno que hicimos nosotros)» (Crónicas de Warcraft, 7-nov-2026).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Investigación con fuentes: videos/_investigacion_wow_addons_forever.md (nada de cifras fuera de ahí).
Tema elegido por el usuario (7-nov) entre 3 propuestas; ~24 min; sale el lun 9-nov (fecha Overgear, enlace /CRONICAS/5).
MINI CATEGORÍA DE INMERSIÓN (el usuario, 7-nov): 17-13 + sus dos add-ons (escenas casa*) hacia el 30 % del video, con sus
grabaciones de OBS (D:\\wowForeverVoces\\grabaciones_obs), donación PayPal desde un mínimo y CurseForge; pregunta si sigue.
VOCES (el usuario, 7-nov): Remy (Applio, ganó la votación de los 25 errores) narra; la voz clonada del usuario (el Humano tras
el Telón, ElevenLabs) presenta SUS add-ons. Frases de Applio: < ~200 caracteres, sin corchetes; nombres ingleses en FONETICA_APPLIO.
Comentarios (≤ 10 días, ninguno usado antes): casa @zatherion1 · gracias1 @pirlo2106 @AlexAnder-z1i7l @quemaloscalor
@666nibelheim666 · gracias2 @santislpslp1595 · burla1 @FenrirMorningstar.
"""

TITULO = "Los 20 ADD-ONS que necesitas en WoW Forever (y uno que hicimos nosotros)"
ARCHIVO = "wow_addons_forever"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Narrador por defecto = el Humano tras el Telón (clon del usuario, ElevenLabs); las frases de Remy van a Applio (VOZ_POR_FRASE)
VOZ = dict(motor="elevenlabs", voice_id="GUEeiSJYQQdbv0NJ86Im", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"),
           por_cuenta={2: "GUEeiSJYQQdbv0NJ86Im", 3: "hCU4QZdzzUliy58ezPBz"})
FONETICA = {"CRONICAS10": "Crónicas diez"}
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); se aplican de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "CRONICAS10": "Crónicas diez", "Elwynn": "Éluin", "Ventormenta": "Ventorménta", "Crónicas de Warcraft": "Crónicas de uárcraft",
    "add-ons": "ádons", "add-on": "ádon", "CurseForge": "Kérsforch", "Bellular": "Béliular", "Vanilla": "Vainíla",
    "Forever Loot Sparkles": "Foréver Lut Spárkels", "Favorcraft": "Féivorcraft", "ChatGPT": "Chat yi pi tí", "Cursor": "Kérsor",
    "Warcraft Logs": "uárcraft Logs", "witchcraft": "uíchcraft", "Claude": "Clod", "Codex": "Códex",
    "Books on Map Forever": "Buks on Map Foréver", "Forever Immersion": "Foréver Imérshon", "Dialogue UI": "Dáialog iú ái",
    "Peterodox": "Píterodox", "Forever Quest Tint": "Foréver Cuest Tint", "Narcissus": "Narsísus", "Wayfarer": "Uéiferer",
    "Lore Forever": "Lor Foréver", "Team Overpowered": "Tim Overpáuerd", "Happy Camper": "Jápi Cámper",
    "Campfire Tooltips": "Cámpfaier Túltips", "GatherLite": "Gáderlait", "Forever Dual Gathering": "Foréver Dúal Gádering",
    "ForeverThreat": "Foréver Zret", "Details": "Ditéils", "Tiny Threat": "Táini Zret", "WeakAuras": "Uík Óras",
    "Midnight": "Mídnait", "DialogKey": "Dáialog Ki", "Numy Edition": "Númi Edíshon", "What's Training": "Uáts Tréining",
    "AtlasLoot": "Átlas Lut", "Baganator": "Bagáneitor", "Bagnon": "Bágnon", "plusmouse": "plás máus",
    "OpenMap": "Óupen Map", "Leatrix Maps": "Lítrix Maps", "Leatrix Plus": "Lítrix Plas", "Auctionator": "Ókshoneitor",
    "OneForAll": "Uán For Ol", "Questie": "Cuésti", "Remy Dos Veces": "Rémi Dos Veces", "Remy": "Rémi", "PayPal": "Péipal",
    "JcJ": "jota ce jota", "Reddit": "Rédit", "Forjaz": "Forjáz",
}

# Whisper escribe distinto los nombres de add-ons (Kersforge, Questy, agro): tolerancia por frase, revisadas a mano el 7-nov
CER_MAX_POR_FRASE = {"c15_4": 0.07, "intro_0": 0.03, "intro_1": 0.043, "c20_3": 0.035, "c19_0": 0.035, "c19_4": 0.068, "c19_6": 0.015, "c17_3": 0.099, "c17_4": 0.046, "c16_4": 0.017, "c16_6": 0.031, "casa4_0": 0.014, "casa4_5": 0.002, "c14_0": 0.094, "c13_3": 0.032, "c13_4": 0.053, "c12_0": 0.081, "c11_0": 0.202, "c11_4": 0.022, "c10_0": 0.075, "c10_2": 0.015, "c10_3": 0.039, "c10_4": 0.033, "c10_5": 0.034, "c10_7": 0.111, "c09_4": 0.068, "overgear_2": 0.015, "c07_0": 0.056, "c07_5": 0.036, "c06_0": 0.031, "c06_4": 0.063, "c06_5": 0.047, "c05_2": 0.031, "c05_5": 0.036, "c05_6": 0.021, "c04_0": 0.085, "c04_1": 0.035, "c03_0": 0.134, "c03_3": 0.022, "c02_0": 0.08, "c02_3": 0.016, "c02_4": 0.016, "c01_0": 0.059, "c01_1": 0.026, "c01_4": 0.02, "c01_6": 0.084}

TAIL_MAX_POR_FRASE = {"casa4_5": 1.05}   # ElevenLabs: cola de 1,009 (la frase está completa)

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},          # se llena tras `beats`: los huecos de casa1/casa3/c15/c13 llevan el AUDIO del clip (PNJ que habla)
    yt=dict(sufijo="World of Warcraft Forever", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos se fijan tras `tiempo` (<= 175 s cada uno)
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 7-nov, 1305,6 s); música ORIGINAL de WoW: `musica_wow.py` corta un tema por tramo
        (['intro', 'serie', 'c20'], 'Legends of Azeroth'),               # 0-112      gancho, de serie, brillo
        (['c19', 'c18', 'overgear'], 'Ventormenta'),                     # 112-260    Favorcraft, libros (Overgear: su música)
        (['inm', 'c17', 'c16', 'c15'], 'Elwynn'),                        # 212-372    inmersión
        (['casa1', 'casa2', 'casa3'], 'Taberna'),
        (['casa4'], 'Taberna'),               # 372-525    los nuestros (Villadorada, la posada)
        (['c14', 'c13', 'gracias1'], 'Baldíos'),                         # 525-650    Wayfarer (perderse en Los Baldíos), Lore
        (['c12', 'c11', 'burla1', 'c10'], 'Vallefresno'),                # 650-800    campamento, recolección, amenaza
        (['c09', 'c08'], 'Páramos'),                                     # DialogKey, What's Training
        (['c07', 'gracias2', 'c06', 'c05'], 'Bosque del Ocaso'),         # 932-1078   botín, bolsas, mapa
        (['c04', 'c03', 'c02'], 'Forjaz'),                               # 1078-1212  subastas, todo en uno, Leatrix
        (['c01', 'cierre'], 'Legends of Azeroth'),                       # 1212-1306  Questie y cierre
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Si buscas un medidor de amenaza para World of Warcraft Forever en CurseForge, te salen setenta resultados que se llaman casi igual.",
        "Forever Threat, ForeverThreat, Threat Meter Forever. Setenta add-ons, para hacer lo mismo.",
        "Desde que salió Forever, el cuatro de noviembre, llueven add-ons. Algunos son joyas, y otros, mejor ni instalarlos.",
        "Así que hoy te traigo los veinte add-ons que de verdad necesitas en World of Warcraft Forever, del veinte al uno, y todos funcionan en Forever.",
        "El número uno lleva más de doscientos millones de descargas. El diecinueve, menos de doscientas.",
        "En medio hay una categoría especial, la de inmersión, y dentro, uno que hicimos nosotros.",
        "Y antes de empezar: la votación de voces ya terminó. Ganó la de siempre, así que aquí sigo. Gracias a todos los que votaron.",
    ]},
    {"id": "serie", "frases": [
        "Pero antes del veinte, dos cosas que Forever ya trae de serie, y que casi nadie enciende.",
        "Un medidor de daño, en Opciones avanzadas, y un gestor de reutilizaciones, que también se abre con el comando barra c d m.",
        "Los dos vienen apagados. Enciéndelos, y te ahorras dos add-ons antes de empezar.",
    ]},
    {"id": "c20", "frases": [
        "Número veinte. Forever Loot Sparkles, el brillo que Blizzard escondió.",
        "En Forever, los objetos de misión que recoges del suelo solo brillan si el modo contorno está apagado.",
        "Y los preajustes de gráficos lo vuelven a encender. Resultado: buscas la flor de la misión a ciegas, en medio del pasto.",
        "Este add-on le devuelve el brillo a los objetos de misión, y además hace brillar las hierbas y las vetas de mineral.",
        "Ya lleva más de seiscientas mil descargas, y hay quien lo recomienda también a la gente con problemas de vista.",
        "Un aviso: cambia ajustes del juego que se quedan aunque lo quites. Antes de borrarlo, desmarca sus casillas.",
    ]},
    {"id": "c19", "frases": [
        "Número diecinueve. Favorcraft. El más nuevo de la lista, y el más arriesgado.",
        "Es un planificador del Favor de comerciante, la moneda nueva de Forever con la que se compran las recetas nuevas.",
        "Eliges las recetas que quieres, te suma todo el favor que cuestan, y te arma la lista de materiales comparada con tus bolsas.",
        "Cubre trescientas nueve recetas de siete profesiones. Y tiene ciento noventa y dos descargas. Ciento noventa y dos.",
        "Su autor lo dice en la página: lo hace con ChatGPT y con Cursor. Y no es el único.",
        "Según 404 Media, Warcraft Logs pasó de unos doscientos programadores en su sistema a unos diez mil, y unos mil abusan de él.",
        "Hasta existe una herramienta, witchcraft, que le pide add-ons a Claude o a Codex sin salir del juego.",
        "Así que úsalo, pero con cuidado. Y si no te fías, el número tres de esta lista trae lo mismo y mucho más.",
    ]},
    {"id": "c18", "frases": [
        "Número dieciocho. Books on Map Forever, para los que leen.",
        "Los libros de biblioteca son un sistema nuevo de Forever: los encuentras por el mundo y los entregas en la biblioteca de la capital.",
        "Con diez libros te dan un collar, con veinte un anillo, y con veinticinco eliges un arco, un escudo o un objeto de mano izquierda.",
        "Este add-on pone en el mapa todos los libros conocidos, y quita cada uno en cuanto lo recoges. Ya pasa de ciento noventa mil descargas.",
        "Y como dan un collar, un anillo y un arma, conviene juntarlos desde los primeros niveles.",
        "Eso sí, dice que hay treinta y ocho libros. Otros dos add-ons dicen que hay cuarenta. Ni los add-ons se ponen de acuerdo.",
    ]},
    {"id": "overgear", "post": 2.6, "frases": [
        "Y si los add-ons te enseñan lo que pasa, pero nadie te dice qué hacer con eso, para eso existe el patrocinador de hoy.",
        "Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.",
        "Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado te guía por voz.",
        "Un medidor te dice que te robaron el aggro. Un buen coach te dice por qué, y cómo no repetirlo en la siguiente mazmorra.",
        "Talentos, rotación, mazmorras nuevas, el plan para las bandas del nueve de diciembre o duelos: tú eliges, y pagas solo las horas que necesites.",
        "El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    # ================================================================ MINI CATEGORÍA: INMERSIÓN (17-13 + los nuestros)
    {"id": "inm", "frases": [
        "Y aquí empieza la categoría especial de hoy: los add-ons de inmersión.",
        "El que está detrás de este canal juega así: despacio, leyendo cada misión, escuchando el lore, sin prisa por llegar al sesenta.",
        "Si tú también juegas así, estos cinco son para ti. Y en medio, una sorpresa.",
    ]},
    {"id": "c17", "frases": [
        "Número diecisiete. Forever Immersion, la interfaz que desaparece.",
        "Mientras exploras, desvanece la interfaz: las barras de acción, el minimapa, el chat y los marcos de los personajes.",
        "Y todo vuelve solo cuando entras en combate, fijas un objetivo, pasas el ratón por encima, o mantienes una tecla.",
        "Así, cuando cruzas el bosque de Elwynn, lo único que ves es el bosque de Elwynn.",
        "Bigbillygames lo resume así: menos basura de interfaz alrededor mientras paseas.",
        "Tiene casi diecisiete mil descargas, y su autor lo sigue actualizando.",
    ]},
    {"id": "c16", "frases": [
        "Número dieciséis. Dialogue UI, las misiones como en un juego de rol.",
        "Cambia la ventana de misiones por una página completa, en modo claro u oscuro, y la cámara se acerca al personaje que te habla.",
        "Se maneja con teclado o con mando, la letra se ajusta, y también sirve para los libros y los textos del mundo.",
        "Bellular dice que cada vez que sale en sus videos, la gente pregunta qué es. Ya va por más de ocho millones y medio de descargas.",
        "Su consejo: pulsa F uno al empezar, y quita el acercamiento de cámara más agresivo.",
        "Y además, antes de aceptar, te dice cuánta experiencia te da cada misión.",
        "Y si lo juntas con Forever Quest Tint, las misiones nuevas de Forever salen teñidas de otro color, para que no se te escape ninguna.",
    ]},
    {"id": "c15", "frases": [
        "Número quince. Narcissus, tu personaje como en un juego de rol.",
        "Cambia la ventana de personaje por una pantalla completa: tu héroe en grande, con la cámara a su alrededor, y el equipo a los lados.",
        "Trae un modo foto que esconde la interfaz, los nombres y los textos de daño, y sube los gráficos al máximo para la captura perfecta.",
        "También tiene panel de logros, títulos ordenados, y gestos con animaciones propias para tu personaje.",
        "Bigbillygames también lo recomienda en su lista de add-ons de inmersión.",
        "Ya pasa de trece millones de descargas, y tiene versión para Forever.",
        "Un aviso: cambia dos de las vistas de cámara guardadas. Si las usas, vuelve a ponerlas después.",
    ]},
    # ---------------------------------------------------------------- LOS NUESTROS (el Humano tras el Telón presenta)
    {"id": "casa1", "post": 16.0, "frases": [
        "Y ahora, la sorpresa. Algo que no vas a encontrar en ninguna otra lista, porque lo hicimos aquí, en casa.",
        "Como lo hizo él, que lo presente él. Y alguien en los comentarios dijo que su voz, con un buen micrófono, sería increíble.",
        "[amused] Gracias. El micrófono todavía no lo tengo, pero traigo algo mejor.",
        "Yo juego así: despacio, leyendo cada misión, escuchando el lore. Y siempre me faltó algo: que los personajes hablaran.",
        "Así que hice WoW Forever Voces: las misiones con voz en español, y cada personaje con su propia voz. [short pause] Escucha.",
    ]},
    {"id": "casa2", "frases": [
        "Cuando tomas una misión, la interfaz se esconde, bajan barras negras, y la cámara gira despacio, como en una cinemática.",
        "Abajo aparece el retrato del personaje, hablando, y sigue hablando aunque cierres la ventana o te vayas caminando.",
    ]},
    {"id": "casa3", "post": 13.0, "frases": [
        "Mientras habla, la música y los efectos bajan, para que se entienda. Y si abres otra misión, esa voz espera su turno.",
        "Aquí, en la posada de Villadorada.",
    ]},
    {"id": "casa4", "frases": [
        "[amused] Y sí: en Villadorada hay un personaje que se llama Remy Dos Veces. No fue idea mía. Así lo hizo Blizzard.",
        "Por fin alguien en Azeroth con un nombre decente.",
        "El segundo se llama Necesidades: barras de hambre, sueño, campamento y descanso, para no perder los bonos de experiencia de Forever.",
        "Se vacían con el tiempo de cada bono, y te avisan antes de que se acabe. Todo se ajusta desde la fogata del minimapa.",
        "Los dos son gratis, y lo van a seguir siendo. Por ahora hice las voces de todas las misiones de inicio de los humanos, en Villanorte, y las de Villadorada.",
        "Y ya estoy por crear las voces de todo el juego. Pero cada voz se paga, así que, si te gusta, en la descripción hay un enlace de PayPal para donar, desde un dólar.",
        "Nadie tiene que pagar para usarlo. La idea es juntar entre todos, y doblar Azeroth entero.",
        "Los dos están en CurseForge, y ese enlace también va en la descripción. Y dime en los comentarios si quieres que siga con las voces.",
        "Lo siguiente es terminar todas las misiones del bosque de Elwynn. Y después, tú eliges: escribe en los comentarios qué zona quieres oír con voz, y vamos zona por zona.",
        "Gracias, humano. Ahora vuelve tras el telón, que la categoría de inmersión todavía no termina.",
    ]},
    {"id": "c14", "frases": [
        "Número catorce. Wayfarer. Lo contrario a todo lo que viene después en esta lista.",
        "Su idea es jugar a Forever sin mapa y sin flecha. En vez de mapa, una brújula que te da direcciones con palabras.",
        "Le preguntas el camino a un guardia, y la respuesta aparece en la brújula. Las misiones te dicen adónde ir, en texto, como en dos mil cuatro.",
        "No trae datos cargados: solo aprende lo que tus personajes han visto, y lo apunta en un diario de viaje.",
        "Tiene poco más de siete mil descargas. Es para valientes. O para gente que disfruta perderse en Los Baldíos.",
        "Como dice Bellular, saberlo todo le quita el misterio al mundo.",
    ]},
    {"id": "c13", "post": 3.6, "frases": [
        "Número trece. Lore Forever. El último de la categoría de inmersión, y el que más se acerca a lo que hacemos aquí.",
        "Te cuenta la historia de cada zona, de las misiones y de las mazmorras, con relatos narrados de las zonas de inicio.",
        "Y desde un panel puedes preguntarle por cualquier lugar, personaje o misión, sin salir del juego.",
        "Team Overpowered lo resume así: puedes pasar cientos de horas en Azeroth sin saber por qué importa la mitad de los sitios.",
        "Bigbillygames dice que te sumerge más que casi todo lo demás de su lista.",
        "Ya pasa de doscientas cincuenta mil descargas, y tiene paquetes de narración en español, con voz de hombre y de mujer.",
        "Y si quieres probarlo, empieza por una de sus historias. Escucha.",
    ]},
    {"id": "gracias1", "frases": [
        "Y antes de seguir, gracias por los comentarios del video de los veinticinco errores.",
        "Pirlo dice que nos escucha siempre de camino al trabajo, y que su cerebro ya se acostumbró a esta voz. Gracias por el viaje, Pirlo.",
        "Alex dice que esta voz es la esencia del canal. Y otro nos recordó que lo que importa es el dato. Los dos tienen razón.",
        "Todos los comentarios se leen, y todos se toman en cuenta para mejorar el canal. Esta voz se queda porque ustedes lo pidieron.",
    ]},
    {"id": "c12", "frases": [
        "Número doce. Happy Camper, para los que acampan.",
        "El campamento es uno de los sistemas nuevos de Forever, y sus beneficios importan cuando subes de nivel.",
        "Este add-on comparte en el mapa las fogatas de los jugadores que también lo tienen, y sigue los beneficios que te dan.",
        "Te ayuda a encontrar o a montar un campamento con los beneficios que quieres, y trae planificación en grupo, insignias, y hasta música de campamento.",
        "Todavía está en beta y lleva unas nueve mil descargas. Si buscas algo más sencillo, Campfire Tooltips te explica treinta y nueve objetos de campamento.",
    ]},
    {"id": "c11", "frases": [
        "Número once. GatherLite, para los que recolectan.",
        "Pone en el mapa y en el minimapa más de veintiséis mil puntos conocidos de hierbas, vetas, cofres y bancos de peces.",
        "Y calcula rutas de recolección por zona, para que no des vueltas a ciegas.",
        "En Forever importa más que nunca, porque las cajas del Favor de comerciante se llenan con materiales que tú recolectas.",
        "Bellular lo recomienda por todo el contenido nuevo de profesiones que trae Forever. Y ya pasa de dos millones de descargas.",
        "Y un truco extra: si llevas Herboristería y Minería, el juego solo rastrea una a la vez. Forever Dual Gathering las alterna solo.",
    ]},
    {"id": "burla1", "frases": [
        "Y ahora, una crítica de las que nos gustan, sobre la votación de voces.",
        "Voz original, por favor, las demás son caca. Hope suena bien. Gracias por un análisis tan matizado.",
        "Todas las demás son caca, excepto una. Un crítico exigente, pero justo. Ya le pasamos el recado a Hope, que está encantada.",
    ]},
    {"id": "c10", "frases": [
        "Número diez. ForeverThreat. El medidor de amenaza.",
        "Forever trae de serie un medidor de daño, pero solo mide daño. La amenaza, no.",
        "Y la opción de las placas de nombre que marca el aggro no te enseña la amenaza de todo el grupo.",
        "Bellular lo dijo mejor: robarle el aggro al tanque y morir en una mazmorra temprana es un rito de paso.",
        "ForeverThreat te enseña la amenaza del grupo en vivo, detecta quién tanquea, y te avisa antes de que el jefe te mire a ti.",
        "Tiene unas setenta mil descargas. Y si prefieres lo de siempre, Details con el complemento Tiny Threat hace lo mismo.",
        "Ojo: Forever usa las reglas de add-ons del World of Warcraft moderno. En combate pueden enseñarte datos, pero no hacer cuentas libremente con ellos.",
        "Por eso WeakAuras, por ejemplo, todavía no tiene versión oficial para Forever.",
    ]},
    {"id": "c09", "frases": [
        "Número nueve. DialogKey, el más pequeño de la lista.",
        "Aceptas misiones, diálogos y ventanas con la barra espaciadora, y eliges las opciones de los personajes con los números.",
        "Suena a poca cosa, hasta que aceptas tu misión número trescientos sin tocar el ratón.",
        "Bellular lo llama el add-on de una sola función perfecto, y dice que, si solo vas a instalar uno, que sea este.",
        "Pero ojo con cuál bajas: el DialogKey original está parado desde dos mil diecinueve. El que funciona en Forever es la Numy Edition.",
        "Lleva más de doscientas mil descargas. Y en combate no funciona, así que no intentes aceptar misiones mientras te comen.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho. What's Training, el que te ahorra viajes al instructor.",
        "Añade una pestaña al libro de hechizos con todo lo que tu instructor te puede enseñar, a qué nivel, y cuánto cuesta.",
        "Y en Forever trae además una pestaña de profesiones, con las recetas de instructores, botines y misiones.",
        "Según Bellular, a niveles bajos conviene ir al instructor cada dos niveles, para ahorrarte viajes. Y llegar sin dinero duele.",
        "También tiene en cuenta tu reputación, para decirte dónde entrenar más barato, y sirve para las mascotas del brujo y las armas.",
        "Lleva casi once millones de descargas.",
        "Y recuerda: en Forever los hechizos nuevos ya no se ponen solos en la barra. Aprende, y arrastra.",
    ]},
    {"id": "c07", "frases": [
        "Número siete. AtlasLoot, el botín de cada jefe.",
        "Tablas de botín de cada jefe, mazmorra y banda, el mejor equipo por clase, profesiones, reputaciones y JcJ.",
        "En Forever no hay buscador de mazmorras, así que vale la pena llegar sabiendo qué suelta cada jefe, y con las misiones recogidas.",
        "Su versión para Forever se llama AtlasLoot Classic Forever, y se irá actualizando con el botín de las bandas nuevas.",
        "Pero tiene un límite: no puede enseñarte botín que nadie ha visto todavía. Y Blizzard escondió mucho botín nuevo.",
        "Y si quieres un diario de mazmorras con misiones y mapas, hay treinta y cuatro en CurseForge. Elige con calma.",
    ]},
    {"id": "gracias2", "frases": [
        "Y un comentario que nos hizo reír esta semana.",
        "Solo he jugado una tarde, y ya he cometido veinticinco errores. Tranquilo: con estos add-ons, a lo mejor solo cometes veinte.",
    ]},
    {"id": "c06", "frases": [
        "Número seis. Baganator, tus bolsas en orden.",
        "Ordena tus bolsas por categorías, o en una sola vista, y guarda lo que tienes en el banco y en tus otros personajes.",
        "Así ves qué lleva tu alter sin tener que cambiar de personaje.",
        "Forever ya trae la opción de combinar bolsas, pero esa bolsa no se puede mover, y no tiene categorías.",
        "Lleva más de cuarenta y un millones de descargas. Y un creador cuenta que Bagnon le congelaba el juego, y Baganator nunca.",
        "Dato curioso: es del mismo autor que el número cuatro de esta lista, un programador que firma como plusmouse.",
    ]},
    {"id": "c05", "frases": [
        "Número cinco. OpenMap, el mapa que Forever no trae.",
        "Cose todos los mapas de zona en un solo mapa continuo, con zoom, desde un callejón hasta el continente entero.",
        "Con el arte original de Vanilla, y con las entradas de mazmorra y su rango de nivel, los puntos de vuelo, los barcos y los zepelines.",
        "Salió el once de octubre, en unos días pasó las ciento sesenta mil descargas, y hoy va por casi setecientas mil.",
        "Su autor lo dice abiertamente: usa a Claude para escribir y revisar el código, pero todo el arte sale de los archivos de Blizzard.",
        "Bellular lo enseña como ejemplo de add-on hecho con inteligencia artificial, y bien hecho. Bigbillygames dice que es de los mejores que ha visto.",
        "O sea, también se pueden hacer bien las cosas con inteligencia artificial. Un consejo: apaga Leatrix Maps si lo tienes, porque chocan.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro. Auctionator. La casa de subastas, sin sufrir.",
        "Listas de compra, búsqueda por recetas, y una pestaña de venta: clic en el objeto, barra espaciadora, y al siguiente.",
        "Te avisa si estás vendiendo demasiado barato, o si el vendedor te paga más que la subasta.",
        "Y en la ventana de profesiones te dice cuánto cuestan los materiales y por cuánto se vende cada receta. Con tantas recetas nuevas, se agradece.",
        "Bellular dice que te acompaña hasta los mil doscientos de oro de la montura épica. Y lleva más de doscientos cinco millones de descargas.",
    ]},
    {"id": "c03", "frases": [
        "Número tres. OneForAll. El que te prometí en el número diecinueve.",
        "Es un compañero todo en uno para Forever: planificador de equipo, mazmorras y bandas, profesiones, talentos, libros de biblioteca y mascotas de cazador.",
        "Y trae una guía del Favor de comerciante y de todos los objetos y beneficios del campamento: los dos sistemas nuevos de Forever, en un solo add-on.",
        "Scottejaye cuenta que no lo conocía, y que ahora no puede vivir sin él. Hasta te avisa cuando hay un libro de biblioteca cerca.",
        "En profesiones, hasta te dice quién de tu hermandad sabe hacer cada receta. Y si llevas la bolsa llena, te propone tirar lo más barato.",
        "El tres de noviembre tenía unas noventa y cuatro mil descargas. Hoy pasa de quinientas noventa mil. Se multiplicó por seis en cuatro días.",
        "Todo viene apagado, y su autor avisa que hay datos incompletos. Enciende solo lo que vayas a usar.",
    ]},
    {"id": "c02", "frases": [
        "Número dos. Leatrix Plus, ochenta comodidades en un solo add-on.",
        "Unas ochenta opciones de comodidad, y ninguna viene encendida. No cambia nada hasta que tú lo decidas.",
        "Vender la basura y reparar solos, filtros de chat, bloquear duelos e invitaciones de desconocidos, y mucho más.",
        "El consejo de casi todos: marca vender basura y reparar, y ya estás jugando mejor que ayer.",
        "Y bloquear las invitaciones a duelo de desconocidos, sinceramente, es salud mental.",
        "Pesa poco, lo recomiendan casi todas las guías de Forever, y lleva más de setenta y seis millones de descargas.",
    ]},
    {"id": "c01", "frases": [
        "Número uno. Questie. El de siempre, y por algo.",
        "Forever marca en el mapa las misiones que ya tienes. Pero no las que puedes recoger. Eso lo hace Questie.",
        "Te enseña quién da cada misión, dónde se entrega, y dónde están los objetivos, con un buscador de toda su base de datos.",
        "En la beta le faltaban misiones nuevas. Ya se actualizó, pero mira igual aunque no veas el signo de exclamación.",
        "En el foro oficial alguien escribió que Questie ya no hace falta, porque viene integrado. Otro le contestó quejándose de sus FPS. Clásico.",
        "Un consejo de Bellular: apaga su rastreador de la derecha, que por defecto es bastante feo.",
        "Y otros add-ons de Forever se apoyan en él: Forever Quest Tint usa la lista de Questie para saber qué misiones son nuevas.",
        "Más de doscientos quince millones de descargas. El add-on más descargado de esta lista, y el número uno.",
    ]},
    {"id": "cierre", "frases": [
        "Y esos son los veinte add-ons que necesitas en World of Warcraft Forever, de un brillo en el pasto hasta el mapa de misiones de siempre.",
        "Cuéntame en los comentarios cuál usas tú, y cuál me faltó. Todos se leen, y los mejores salen en el próximo video.",
        "Y si quieres que sigamos doblando las misiones en español, comenta, y si puedes, apoya con lo que quieras en el enlace de la descripción.",
        "[amused] Yo vuelvo tras el telón. Pero si ustedes lo piden, vuelvo con más voces.",
        "Y yo me quedo, que para eso ganó la de siempre. Nos vemos en la próxima crónica, y nos vemos en Azeroth.",
    ]},
]

# --- VOCES: quién narra cada frase; lo que no sale aquí, Remy (Applio) ---
VOCES = {"Remy": "applio", "el Humano tras el Telón": "GUEeiSJYQQdbv0NJ86Im"}
LEMAS = {"Remy": "La voz de siempre", "el Humano tras el Telón": "El que hizo el add-on"}
_POR_ESCENA = {"casa1": "el Humano tras el Telón", "casa2": "el Humano tras el Telón", "casa3": "el Humano tras el Telón",
               "casa4": "el Humano tras el Telón"}
_POR_FRASE = {"casa1_0": "Remy", "casa1_1": "Remy", "casa4_1": "Remy", "casa4_9": "Remy", "cierre_3": "el Humano tras el Telón"}
NARRA = {}
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k) or _POR_ESCENA.get(_e["id"], "Remy")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items()}
