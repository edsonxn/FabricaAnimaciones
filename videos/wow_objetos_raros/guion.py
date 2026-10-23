# -*- coding: utf-8 -*-
"""GUION · Los 12 objetos más RAROS de World of Warcraft Vanilla que podrían volver en WoW Forever (Crónicas de Warcraft,
motor SECUENCIA YT, ~14 min). Flujo y reglas: docs/estilo_secuencia_yt.md · estilo «gema» (cuenta regresiva, chistes secos).
Pedido por el usuario el 22-oct-2026: lista de armas/objetos raros de Vanilla, ≥ 12, con MAPAS REALES del juego para enseñar
dónde se obtienen y las rutas de las cadenas de misiones (MG nuevo `mg_wow.ruta`). De menos a más raro; la n.º 1 la más rara.
SIN Overgear y con música ORIGINAL de WoW (el usuario, 22-oct-2026), como Kalimdor.

Verificado el 22-oct-2026 (investigación completa con fuentes: videos/_investigacion_wow_raros.md): nombres es-MX de la API de
tooltips de Wowhead (locale=11), coordenadas Classic de la base de datos de Questie, hechos en warcraft.wiki.gg / Wowpedia.
- Forever: sale el 4-nov-2026, nivel 60 para siempre, ambientado antes del Núcleo de Magma; el 9-dic abren Barrow Deeps, Hyjal
  Summit y la Guarida de Onyxia (única banda clásica confirmada); 2027: nueva cadena legendaria (primavera) y «una banda icónica
  rehecha» sin nombre (verano). Fin de beta (22-oct): los jefes soltaban Sulfuras y Trueno Furioso y Thunderaan salió de paseo.
  Mazmorras clásicas confirmadas: Roca Negra (BRD), La Masacre, Scholomance, Stratholme, Minas, Colmillo Oscuro, Brazanegra…
- Puño de Verigan (6953, req 20): Duthorian Rall (Ventormenta) -> Daphne Fontana (Poniente) -> Jordan Fontana (Dun Morogh) ->
  madera de roble blanco (Minas), mineral de Bailor Petramano (Loch Modan), martillo de Jordan (Colmillo Oscuro), gema Kor
  (Brazanegra, la purifica Thundris Tejevientos en Costa Oscura); en honor de Bosch Verigan; Horda: Guja templada en sangre; quitado en 4.0.3.
- Sable de hielo de Cuna del Invierno (13086): 100 de oro a Rivern Ventogélido con Exaltado en los Entrenadores de Sableinvernal
  (facción de 2 PNJ, solo Alianza; Horda sin equivalente hasta 3.2); «ratones falsos y cordel» en la descripción.
- Ferromazo (11684): Emperador Dagran Thaurissan, 0,18-0,59 % (estimación); dos ataques extra; Franclorn Forjamaestro; reliquia
  familiar del Mariscal Windsor que le quitaron los Hierro Negro.
- Corcel nefasto (hechizo 23161): Mor'zul Sangredoble (Estepas Ardientes), Lord Banehollow (Guarida de Jaedenar, Frondavil),
  Cuna del Invierno; ritual en La Masacre con Campana de Dethmoora, Rueda de la Marcha Negra y Vela del Juicio Final; Lord Hel'nurath;
  2.4.0 al entrenador, cadena quitada en 4.0.1.
- Quel'Serrar (18348): Compendio de matar dragones de Nostro (antes Foror's, renombrado el 27-jul-2021), «imposible de farmear»,
  ligado al equipar; Tradicionalista Lydros (La Masacre); hoja en el suelo + Respiración profunda de Onyxia; guiño a EverQuest
  (esconderse bajo un puente, 5-15 clérigos); quitada en 3.2.2; guerreros y paladines.
- Rhok'delar (18713): Hoja petrificada vieja del Alijo del Señor del Fuego; Ancianos de Frondavil; 4 demonios SOLO y sin mascota:
  Simone la Discreta (Un'Goro), Franklin el Amistoso (Estepas Ardientes), Nelson the Nice (Silithus), Artorius el Afable (Cuna);
  tendones de Azuregos y Onyxia; echa flores.
- Riendas de destrero de la muerte (13335): Barón Osahendido, Stratholme, 0,02 % en Classic, 1 % desde 3.0.2; único caballo
  esquelético de la Alianza; parche 1.3.0 para los tauren; Osahendido condenó a su caballo favorito a la no-muerte.
- Sulfuras (17182): Ojo de Sulfuras (Ragnaros, ~3 %, puede caer a cualquier clase) + Martillo de Sulfuron; planos: lingote de
  sulfuron a Lokhtos Tratoscuro (Bar Tragapenas); martillo: 8 lingotes, 20 barras de hierro negro, 50 de arcanita, 10 Sangre de la
  Montaña; arma cuerpo a cuerpo con más DPS hasta 1.6; un jugador la terminó tras ~20 años (abril de 2026, Mein-MMO).
- Crematoria corrupta (22691): Cuatro Jinetes (Naxxramas); susurros de Mograine (12 frases, el Rey Exánime detrás); hostil con el
  Alba Argenta, amistosa con la Cruzada Escarlata; evento del Monasterio: los cruzados se arrodillan, Alexandros mata a Renault y
  libera a Fairbanks; rumor de la misión secreta que Blizzard desmintió; inalcanzable desde Wrath.
- Trueno Furioso (19019): Ataduras izquierda (Barón Geddon) y derecha (Garr), ~3 % c/u (estimación); Alto señor Demitrian
  (Silithus); 10 barras de elementium (Guarida Alanegra), Esencia del Señor del Fuego; Príncipe Thunderaan (hijo de Al'Akir);
  Wray primer portador; «Did someone say Thunderfury?»; parche 1.6.0, 12-jul-2005.
- Atiesh (22589): 40 astillas (Naxx salvo Sapphiron y Kel'Thuzad), Anacronos (Tanaris), cabeza (Kel'Thuzad) + base (C'Thun) ->
  demonio Atiesh en Stratholme (> 200 000 PV, dos Andonisus); primer legendario de lanzador; portal a Karazhan antes de Karazhan.
- Cetro del Mar de Dunas (21175) / Cristal resonador negro qiraji (21176): Baristolth (Fuerte Cenarion), Señor de linaje Capazote,
  Anacronos, fragmentos rojo (Vaelastrasz/Nefarian), azul (Narain Sabelotodo, Maws = Tiburón), verde (Fuego fatuo de Teldrassil,
  Remulos, Pesadilla en 4 zonas, Eranikus); gong; Kalahad (Medivh) 22-ene-2006; Guerra de las 10 Horas; primera montura legendaria,
  única hasta Dragonflight; reinos nuevos con puertas abiertas desde el 6-feb-2009; Classic 2019: 90 en Flamegor, 49 en Fairbanks.
"""

TITULO = "Los 12 objetos más RAROS de World of Warcraft Vanilla que podrían volver en Forever"
ARCHIVO = "wow_objetos_raros"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")

# Grafía que lee el TTS (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md; con traducción oficial, se usa esa)
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Classic": "Clásic", "Vanilla": "Vanila", "Azeroth": "Azeróth", "Cataclysm": "Cataclísm",
    "Wrath of the Lich King": "Raz of de lich king", "Dragonflight": "Drágonflait", "EverQuest": "Éverkuest", "Reddit": "Rédit",
    "DPS": "de pe ese",
    # lugares
    "Kalimdor": "Kálimdor", "Silithus": "Silízus", "Tanaris": "Tanáris", "Feralas": "Ferálas", "Azshara": "Asshára",
    "Teldrassil": "Teldrásil", "Un'Goro": "Un Góro", "Stratholme": "Strázolm", "Naxxramas": "Naksrámas", "Karazhan": "Karazán",
    "Ahn'Qiraj": "An Kiráj", "Dun Morogh": "Dun Moróg", "Loch Modan": "Loc Módan", "Jaedenar": "Yaédenar", "Dalaran": "Dálaran",
    "Hyjal": "Jáyal", "Barrow Deeps": "Bárou Díps", "Hyjal Summit": "Jáyal Sámit", "Medivh": "Médiv", "Flamegor": "Fléimgor",
    "Fairbanks": "Férbanks", "Scholomance": "Escolomans",
    # objetos
    "Quel'Serrar": "Kel Sérrar", "Rhok'delar": "Rok délar", "Lok'delar": "Lok délar", "Sulfuras": "Sulfúras", "Sulfuron": "Sulfúron",
    "Atiesh": "Atiésh", "Andonisus": "Andonísus", "elementium": "eleméntium", "qiraji": "kiráyi", "Thunderfury": "Zánderfiuri",
    "Did someone say": "did sámuan séi", "Foror": "Fóror", "Nostro": "Nóstro", "Kor": "Kor",
    # personajes y criaturas
    "Verigan": "Vérigan", "Duthorian Rall": "Dúzorian Ral", "Thundris": "Zúndris", "Bailor": "Báilor", "Bosch": "Bosh",
    "Rivern": "Ríbern", "Dagran Thaurissan": "Dágran Zaurísan", "Franclorn": "Fránclorn", "Windsor": "Uíndsor",
    "Mor'zul": "Mor zul", "Banehollow": "Béinjolou", "Dethmoora": "Dezmúra", "Hel'nurath": "Jel núraz", "xorothiano": "zorotiáno",
    "Lydros": "Lídros", "Onyxia": "Oníxia", "Vartrus": "Vártrus", "Stoma": "Estóma", "Hastat": "Jástat",
    "Nelson the Nice": "Nélson de Náis", "Artorius": "Artórius", "Azuregos": "Azurégos", "Osahendido": "Osajendído",
    "Ragnaros": "Rágnaros", "Lokhtos": "Lóctos", "Golemagg": "Gólemag", "Mograine": "Mogréin", "Alexandros": "Alexándros",
    "Renault": "Renól", "Fairbanks": "Férbanks", "Geddon": "Guédon", "Garr": "Gar", "Demitrian": "Demítrian",
    "Thunderaan": "Zanderán", "Al'Akir": "Al Akír", "Wray": "Réi", "Sapphiron": "Sáfiron", "Kel'Thuzad": "Kel Zúzad",
    "C'Thun": "Ce Zún", "Anacronos": "Anacrónos", "Nielas Aran": "Níelas Áran", "Baristolth": "Barístolz", "Capazote": "Capazóte",
    "Vaelastrasz": "Vaelástras", "Nefarian": "Nefárian", "Narain": "Naráin", "Maws": "Mós", "Remulos": "Rémulos",
    "Eranikus": "Eraníkus", "Kalahad": "Kálajad", "Executus": "Ekzékutus",
}

# Whisper escribe distinto lo que Remy dice (Stratholme -> «Strassholm», Atiesh -> «Aties», Barón -> «varón», cifras en dígitos
# y versiones de parche); revisado por hyp el 22-oct, sin oír cada toma
CER_MAX_POR_FRASE = {"c01_1": 0.05, "c01_10": 0.04, "c02_8": 0.04, "c01_4": 0.02, "c01_5": 0.04, "c02_0": 0.03, "c02_1": 0.08, "c02_2": 0.07, "c02_3": 0.04, "c02_7": 0.04, "c03_1": 0.03, "c03_3": 0.03, "c03_4": 0.03, "c03_5": 0.06, "c03_6": 0.04, "c04_0": 0.05, "c05_2": 0.03, "c05_4": 0.06, "c06_0": 0.07, "c06_1": 0.11, "c06_2": 0.13, "c06_4": 0.08, "c06_6": 0.05, "c06_7": 0.05, "c06_8": 0.11, "c07_0": 0.04, "c07_2": 0.04, "c07_3": 0.03, "c07_4": 0.06, "c08_6": 0.16, "c09_1": 0.05, "c09_4": 0.03, "c09_5": 0.04, "c09_6": 0.11, "c10_0": 0.04, "c10_1": 0.07, "c10_4": 0.05, "c11_1": 0.03, "c11_5": 0.07, "c11_6": 0.05, "c12_0": 0.04, "c12_1": 0.03, "c12_2": 0.02, "c12_4": 0.03, "c12_5": 0.02, "c12_6": 0.03, "c12_7": 0.14, "cierre_1": 0.07, "cierre_3": 0.05, "cierre_5": 0.03}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # el audio del gameplay no se usa (se bajan solo imágenes)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Thraex", "Video Game Collector", "TheLtColonel", "Jansn Benchmarks", "Platinum WoW", "WoWAholics101",
                            "DCARR GAMING", "Noob2Boss", "NoobToBoss", "Esfand", "WoW Clips", "720 Zone", "Tosan Tribe", "Rotan",
                            "Tetsu", "Neuro", "hammerdance", "Whiter", "Momentumqp", "Almar Winfield", "Lothric Gaming", "Gnomica",
                            "Moegdal's WoW Videos", "Icosiol", "Bhelockharyh", "Quissy", "WillE", "MadSeasonShow", "Djente", "Muiscal", "AmmeTV",
                            "LazyTevs", "Everness"]),   # + 23-oct: webcams, logos, guías con mapa   # heredados de Reinos del Este y Kalimdor: guías con recuadros, marcas, webcams
)

TRANSICIONES = [("continua", 0.1)] * 40

# Con la música ORIGINAL de WoW (sin Lyria) el ánimo sirve para asignar un tema a cada tramo (`musica_wow.py`, como Kalimdor).
# `tramos` (<= 175 s) se escriben con la línea de tiempo real de `tiempo`.
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 22-oct, 818,1 s); con música ORIGINAL de WoW, `musica_wow.py` corta un tema por tramo
        (['intro', 'c12'], 'Ventormenta'),     # 0-105 s
        (['c11'], 'Cuna del Invierno'),        # 105-167 s
        (['c10', 'c09'], 'Núcleo de Magma'),   # 167-285 s  Roca Negra y el ritual del brujo
        (['c08'], 'Ventormenta'),              # 285-350 s  Quel'Serrar y Onyxia
        (['c07'], 'Cuna del Invierno'),        # 350-402 s  Rhok'delar, arma viva
        (['c06'], 'Naxxramas'),                # 402-460 s  Stratholme
        (['c05'], 'Núcleo de Magma'),          # 460-505 s  Sulfuras
        (['c04'], 'Naxxramas'),                # 505-562 s  Crematoria corrupta
        (['c03'], 'Núcleo de Magma'),          # 562-622 s  Trueno Furioso
        (['c02'], 'Naxxramas'),                # 622-687 s  Atiesh
        (['c01', 'cierre'], 'Ventormenta'),    # 687-818 s  el cetro y el cierre
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "El veintidós de octubre, en el evento que cerró la beta de World of Warcraft Forever, los jefes soltaban Sulfuras y Trueno Furioso como si fueran dulces de piñata.",
        "En el World of Warcraft original, esas dos armas costaban meses de banda, y hubo jugadores que esperaron veinte años para terminar una.",
        "Forever sale el cuatro de noviembre, y con él vuelve la pregunta de qué objetos del Vanilla vamos a volver a perseguir.",
        "Forever es un Classic con historia propia, con nivel sesenta para siempre, y está ambientado justo antes del Núcleo de Magma.",
        "Así que aquí va una docena de objetos, los más raros de aquella época, del más difícil de ver al que casi nadie tuvo nunca.",
        "Te voy a enseñar en el mapa del juego dónde se consiguen, y la ruta de las cadenas de misiones que los esconden.",
    ]},
    {"id": "c12", "frases": [
        "Número doce, el Puño de Verigan, una maza de dos manos que un paladín podía ganarse a nivel veinte.",
        "Suena a premio menor, hasta que ves la ruta, porque empieza con Duthorian Rall en Ventormenta, que te manda a los Páramos de Poniente a defender la casa de Daphne Fontana de los Defias.",
        "Luego vas con Jordan Fontana, a las puertas de Forjaz, y él te pide los materiales para forjarla.",
        "Madera de roble blanco de las Minas de la Muerte y un cargamento de mineral de Bailor Petramano, en Loch Modan.",
        "Además, su martillo perdido en el Castillo de Colmillo Oscuro, y una gema Kor de las Cavernas de Brazanegra.",
        "Esa gema hay que purificarla con Thundris Tejevientos, en Costa Oscura, o sea, en otro continente.",
        "Son tres mazmorras y dos continentes para un arma que dejas de usar a nivel treinta. Jordan Fontana la bautizó en honor de su amigo Bosch Verigan, un paladín enano ya muerto.",
        "La quitaron en el parche cuatro punto cero punto tres, y en Forever las tres mazmorras siguen ahí.",
    ]},
    {"id": "c11", "frases": [
        "Número once, las Riendas del sable de hielo de Cuna del Invierno, la montura que convirtió a la Alianza en la envidia de la Horda.",
        "Costaba cien de oro, que era lo de menos, porque Rivern Ventogélido solo te la vendía con reputación exaltada con los Entrenadores de Sableinvernal.",
        "Esa facción tiene exactamente dos miembros, y se sube a base de misiones contra osos, quimeras, gigantes y furbolgs en la nieve de Cuna del Invierno.",
        "La descripción del objeto dice que domar a esta raza requiere paciencia, fuerza y un buen suministro de ratones falsos y cordel.",
        "Y si no eras elfo de la noche, además tenías que ser exaltado con Darnassus, por si la paciencia no alcanzaba.",
        "La Horda no tuvo nada parecido hasta el parche tres punto dos, y se quejó todo ese tiempo, con bastante razón.",
        "En el parche cuatro punto uno cambiaron el farmeo por veinte días de misiones diarias criando un cachorro, que es otra forma de paciencia.",
        "Cuna del Invierno vuelve en Forever como zona de nivel alto, y nadie ha dicho todavía si esta vez la Horda tendrá su propio felino.",
    ]},
    {"id": "c10", "frases": [
        "Número diez, Ferromazo, una maza que cae del Emperador Dagran Thaurissan en las Profundidades de Roca Negra.",
        "La comunidad calcula que sale entre un cero coma dieciocho y un cero coma cincuenta y nueve por ciento de las veces, o sea, que puedes matar al emperador quinientas veces sin verla.",
        "Su efecto era delicioso, porque al acertar te daba dos ataques extra en el siguiente golpe.",
        "Y tiene historia, porque la forjó Franclorn Forjamaestro, y era la reliquia de la familia del Mariscal Windsor.",
        "Los Hierro Negro se la quitaron cuando lo capturaron, y Thaurissan la usó hasta el día de su muerte, que suele ser el día en que llegas tú.",
        "Para llegar hasta el emperador hay que entrar a la Montaña Roca Negra por la Garganta de Fuego y cruzar la mazmorra entera, hasta el Palacio Imperial.",
        "Las Profundidades de Roca Negra están confirmadas en Forever, así que esta podría caer desde la primera semana en el nivel máximo.",
    ]},
    {"id": "c09", "frases": [
        "Número nueve, el Corcel nefasto, la montura épica del brujo, que no se compraba, se arrancaba de otro plano.",
        "La cadena empieza en las Estepas Ardientes con Mor'zul Sangredoble, que te manda a Cuna del Invierno y luego a Frondavil, a la Guarida de Jaedenar, donde te espera Lord Banehollow.",
        "Al final hay que reunir una Campana de Dethmoora, una Rueda de la Marcha Negra y una Vela del Juicio Final, y montar un ritual dentro de La Masacre.",
        "Para eso el brujo necesita a cuatro amigos dispuestos a jugarse la vida por un caballo que ellos nunca van a montar.",
        "El ritual invoca a un corcel xorothiano, el grupo entero lo mata, y su espíritu se queda contigo, lo cual dice bastante del contrato de esta montura.",
        "Los mejores corceles son de Lord Hel'nurath, al que el juego llama el caballerizo.",
        "En el parche dos punto cuatro el corcel pasó al entrenador, y la cadena desapareció en cuatro punto cero punto uno. La Masacre está en Forever, así que el ritual tiene dónde volver.",
        "Y el paladín tenía su versión, el Destrero, con una cadena que terminaba dentro de Scholomance, redimiendo a un caballo caído.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho, Quel'Serrar, la espada que necesita que un dragón la caliente.",
        "Todo empieza con un libro, el Compendio de matar dragones de Nostro, que cae en La Masacre con una probabilidad tan baja que se consideraba imposible de farmear.",
        "Por suerte era ligado al equipar, así que el que tenía oro lo compraba en la subasta. Se lo llevas al Tradicionalista Lydros, en la biblioteca de La Masacre.",
        "Luego viene la parte que nadie más en el juego te pedía, que es dejar la hoja vieja en el suelo de la Guarida de Onyxia y esperar a que su Respiración profunda la caliente.",
        "La hoja se enfría con el tiempo, así que hay que matar a Onyxia rápido y clavarla en su cadáver.",
        "El libro, por cierto, es una burla de EverQuest, porque recomienda esconderse bajo un puente y rotar entre cinco y quince clérigos.",
        "La quitaron en el parche tres punto dos punto dos, y aún hoy es raro ver una original.",
        "Y aquí viene lo bueno, porque Onyxia es la única banda clásica confirmada en Forever, y abre el nueve de diciembre.",
        "Así que, de toda esta lista, Quel'Serrar es la candidata más seria a volver en los primeros meses.",
    ]},
    {"id": "c07", "frases": [
        "Número siete, Rhok'delar, el arco largo de los Guardianes ancianos, la misión épica del cazador.",
        "Empieza con una Hoja petrificada vieja que sale del Alijo del Señor del Fuego, el cofre del Mayordomo Executus en el Núcleo de Magma.",
        "Los Ancianos de Frondavil, Vartrus, Stoma y Hastat, te mandan a matar a cuatro demonios disfrazados, y tienes que hacerlo solo y sin tu mascota.",
        "Simone la Discreta está en el Cráter de Un'Goro, Franklin el Amistoso en las Estepas Ardientes, Nelson the Nice en Silithus y Artorius el Afable en Cuna del Invierno.",
        "Son demonios con nombre de vecino amable, repartidos por dos continentes, y antes del parche uno punto ocho el arco y el bastón gemelo, Lok'delar, se podían convertir uno en otro.",
        "Además pide tendones de dragón azul de Azuregos y de dragón negro de Onyxia. Y el arco, que está vivo, echa flores de vez en cuando.",
    ]},
    {"id": "c06", "frases": [
        "Número seis, las Riendas de destrero de la muerte, el caballo esquelético del Barón Osahendido, en Stratholme.",
        "En Classic la probabilidad era de un cero coma cero dos por ciento, una montura cada cinco mil muertes del barón.",
        "Blizzard la subió al uno por ciento en el parche tres punto cero punto dos, lo cual ya fue un acto de caridad.",
        "Era el único caballo esquelético que podía montar la Alianza, porque no pedía la habilidad de equitación no-muerta.",
        "Y en el parche uno punto tres tuvieron que arreglarlo para que los tauren pudieran subirse.",
        "En el lore, el barón condenó a su caballo favorito a la no-muerte junto con él, que es la forma más egoísta de tener mascota.",
        "Stratholme tiene dos entradas en las Tierras de la Peste del Este, y la que lleva al barón es la de servicio, la del lado no-muerto.",
        "Stratholme está confirmada en Forever, y alguien va a hacer esa mazmorra cinco mil veces.",
        "Lo que nadie ha dicho es si la probabilidad vuelve al cero coma cero dos por ciento o se queda en el uno.",
    ]},
    {"id": "c05", "frases": [
        "Número cinco, Sulfuras, Mano de Ragnaros, el martillo que hay que fabricar con el arma del propio señor del fuego.",
        "Ragnaros suelta el Ojo de Sulfuras alrededor de un tres por ciento de las veces, y puede caer para cualquier clase, aunque no sepa usar una maza.",
        "Para los planos hay que llevar un lingote de sulfuron a Lokhtos Tratoscuro, el mercader del Bar Tragapenas en las Profundidades de Roca Negra.",
        "El martillo pide ocho lingotes de sulfuron, veinte barras de hierro negro, cincuenta de arcanita y diez Sangres de la Montaña.",
        "Hasta la Guarida Alanegra fue el arma cuerpo a cuerpo con más DPS del juego, y hasta el parche uno punto once, la de más daño bruto.",
        "Y en abril de dos mil veintiséis un jugador contó en Reddit que por fin la había terminado, después de unos veinte años.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro, la Crematoria corrupta, la espada que llevaba el Alto señor Mograine en Naxxramas, y que caía del cofre de los Cuatro Jinetes.",
        "Al equiparla, el espíritu de Mograine te susurra, frase por frase, que alguna vez fue puro y que su hijo lo vio morir.",
        "Detrás se oye al Rey Exánime, y la última frase la dicen los dos a la vez. Además te vuelve hostil con el Alba Argenta y amistoso con la Cruzada Escarlata.",
        "Y tenía un evento secreto, porque si entrabas con ella a la catedral del Monasterio Escarlata los cruzados se arrodillaban.",
        "Aparecía el fantasma de Alexandros Mograine, mataba a su propio hijo Renault y liberaba a Fairbanks, que te contaba la traición.",
        "La Crematoria fue de los primeros legendarios que los jugadores sacaron de los archivos del juego, y como el Cuidador Alen la mencionaba, todo el mundo buscó una misión secreta para purificarla.",
        "Esa misión nunca existió, Blizzard lo desmintió, y desde Wrath of the Lich King la espada ya no se puede conseguir.",
    ]},
    {"id": "c03", "frases": [
        "Número tres, Trueno Furioso, espada bendita del Hijo del Viento.",
        "En el Núcleo de Magma, el Barón Geddon guarda la atadura izquierda y Garr la derecha, y la comunidad calcula que cada una cae un tres por ciento de las veces.",
        "Dentro está encerrado el Príncipe Thunderaan, hijo de Al'Akir, al que Ragnaros derrotó, y cuya esencia quedó en un talismán partido en dos.",
        "Con las dos ataduras vas a Silithus, con el Alto señor Demitrian, que te pide diez barras de elementium de la Guarida Alanegra y la Esencia del Señor del Fuego.",
        "Luego invoca a Thunderaan, la banda entera lo mata, y te llevas la espada.",
        "Llegó en el parche uno punto seis, el doce de julio de dos mil cinco, y en el lore su primer portador conocido fue un enano guerrero llamado Wray.",
        "Fue tan rara y tan presumida que su nombre se volvió un meme del chat de Los Baldíos, con la frase Did someone say Thunderfury.",
        "Y en el cierre de la beta de Forever, Thunderaan apareció de paseo fuera de las ciudades, como si supiera algo que nosotros no.",
    ]},
    {"id": "c02", "frases": [
        "Número dos, Atiesh, gran báculo del Guardián, el bastón de Medivh.",
        "Para armarlo hay que juntar cuarenta Astillas de Atiesh, que caen de todos los jefes de Naxxramas salvo Sapphiron y Kel'Thuzad.",
        "Con el armazón vas a Tanaris, con Anacronos, a la entrada de las Cavernas del Tiempo, y él te pide la cabeza del báculo de Kel'Thuzad y la base de C'Thun, en Ahn'Qiraj.",
        "Después hay que purificarlo en Stratholme, donde aparece el demonio Atiesh con más de doscientos mil puntos de vida y dos espadas en las manos.",
        "Fue el primer legendario para lanzadores de hechizos de la historia del juego.",
        "Y abría un portal a la puerta de Karazhan cuando Karazhan todavía no existía, así que el bastón conocía el futuro mejor que los jugadores.",
        "Y un personaje del juego moderno encontró treinta y nueve astillas en el almacén del vacío de un aventurero, al que le faltó una.",
        "Cuando por fin entrabas a Karazhan con él, el fantasma de Nielas Aran, el padre de Medivh, te preguntaba de dónde lo habías sacado.",
        "En Forever, Naxxramas ni siquiera está anunciada, así que de toda esta lista, el objeto que más lejos queda es Atiesh.",
    ]},
    {"id": "c01", "frases": [
        "Número uno, el Cetro del Mar de Dunas, y lo que te daba, que era el Cristal resonador negro qiraji.",
        "Esta es la cadena más larga del Vanilla, y arranca en el Fuerte Cenarion, en Silithus, con Baristolth del Mar de Dunas.",
        "Te pide la cabeza del Señor de linaje Capazote en la Guarida Alanegra, y te manda con Anacronos, en Tanaris.",
        "El fragmento rojo sale de Nefarian. Para el azul hay que descifrar un libro de dragones con Narain Sabelotodo e invocar a un tiburón gigante llamado Maws, un guiño a la película Tiburón.",
        "El verde empieza con un fuego fatuo en Teldrassil y sigue con el Guardián Remulos en Claro de la Luna, persiguiendo la corrupción de la Pesadilla por cuatro zonas hasta pelear con Eranikus.",
        "Con el cetro armado tocas el Gong del Escarabajo, en la puerta de Ahn'Qiraj, y se abre la guerra para todo el reino.",
        "El primero en tocarlo, y los que tuvieran cetro durante la Guerra de las Diez Horas, se llevaban el título de Señor del Escarabajo y el tanque negro, y después nadie más.",
        "El primero del mundo fue Kalahad, en el reino Medivh, el veintidós de enero de dos mil seis.",
        "Fue la primera montura legendaria del juego y la única hasta Dragonflight, y desde febrero de dos mil nueve los reinos nuevos nacían con la puerta ya abierta.",
        "En Classic de dos mil diecinueve hubo noventa Señores del Escarabajo en Flamegor y cuarenta y nueve en Fairbanks, en reinos con miles de jugadores.",
        "Blizzard no ha dicho nada del evento de Ahn'Qiraj en Forever, pero si vuelve, el primer gong de cada servidor va a valer más que cualquier legendario.",
    ]},
    {"id": "cierre", "frases": [
        "Y esa es la docena de objetos más raros que dejó el Vanilla.",
        "Forever todavía no confirma el Núcleo de Magma, ni Naxxramas, ni el evento de Ahn'Qiraj.",
        "Lo que sí promete es una cadena legendaria nueva en la primavera de dos mil veintisiete, y una banda icónica rehecha en el verano, sin decir cuál.",
        "Lo seguro es que Onyxia abre el nueve de diciembre, y que La Masacre, Stratholme y Roca Negra ya esperan desde el primer día.",
        "Dime en los comentarios cuál de todos vas a perseguir primero, y cuál crees que Blizzard va a dejar guardado para siempre.",
        "Al final, en el Vanilla los objetos más raros no se compraban ni se farmeaban, se ganaban recorriendo el mapa entero, y por eso hoy nadie los ha olvidado.",
    ]},
]
