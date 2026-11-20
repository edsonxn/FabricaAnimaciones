# -*- coding: utf-8 -*-
"""GUION — «La RUTA del 1 al 60 en WoW Forever, zona por zona» (Crónicas de Warcraft, 19-nov-2026, lun 23-nov 09:00 CDMX).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Tema elegido por el usuario (19-nov, opción 2 de la conclusión del 15-nov): una variable sobre «20 errores del 30 al 60» = el formato (guía-ruta
con mapa real en cada zona). Investigación: videos/_investigacion_wow_ruta_forever.md (coordenadas de Wowhead Forever, nombres es-MX).
SIN OVERGEAR. La voz NO cita fuentes. Lo dudoso NO se dice (Incursiones de la Pesadilla, nombre del puerto de Tanaris, posadas de Dalaran).
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras. Cifras en letra.
Comentarios (≤ 10 días, ninguno usado antes): intro @j-sancomics6910 · p04 @alexafm14 · p06 @rubenlopez9451 ·
gracias1 @Sakaan07 @mateogrisalescano2147 · gracias2 @lololulu-r5w @massimoamoretti9086 @AlexAnder-z1i7l @sgto.sevilla6976 ·
burla0 @vito_232 · burla1 @SolidNano · burla2 @josejuanandrade4439.
"""

TITULO = "La RUTA del 1 al 60 en WoW Forever, zona por zona"
ARCHIVO = "wow_ruta_forever"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Classic": "Clásic", "Azeroth": "Azeróth", "Crónicas de Warcraft": "Crónicas de uárcraft",
    "Riverglades": "Ríverglèids", "Shen'dralas": "Shendrálas", "Shen'dar": "Shendár", "Zephras": "Séfras", "Valanaar": "Valanár",
    "Bandarion": "Bandárion", "Farholde": "Fárjold", "Rog'mar": "Rógmar", "Krol'dok": "Króldok", "Pedreg'ok": "Pédregok",
    "Alcaz": "Álcaz", "Menethil": "Ménezil", "Theramore": "Terámor", "Thelsamar": "Télsamar", "Auberdine": "Óberdin",
    "Astranaar": "Ástranar", "Gadgetzan": "Gádguetsan", "Grom'Gol": "Gromgól", "Kargath": "Kárgaz", "Dalaran": "Dálaran",
    "Hyjal": "Jáyal", "Un'Goro": "Ungóro", "Azshara": "Asshára", "Zul'Farrak": "Zul Fárak", "Uldaman": "Uldáman",
    "Desolace": "Desolás", "Tirisfal": "Tirisfál", "Teldrassil": "Teldrásil", "Dun Morogh": "Dun Mórog", "Mulgore": "Múlgor",
    "Durotar": "Durotár", "Silithus": "Silízus", "Taurajo": "Tauráyo", "Hogger": "Jóguer", "Nesingwary": "Nésinguari",
    "Franclorn": "Fránclorn", "Alterac": "Álterac", "Lordaeron": "Lordéron", "Zoram'gar": "Zóramgar", "Talrendis": "Talréndis",
    "Valormok": "Valórmok", "Nijel": "Níyel", "Thalanaar": "Tálanar", "Atal'Hakkar": "Atal Jákar", "Archimonde": "Árchimond",
    "Onyxia": "Oníxia", "Ventormenta": "Ventorménta", "Orgrimmar": "Orgrímar", "Elwynn": "Éluin", "Forjaz": "Forjáz",
    "Entrañas": "Entráñas", "Mojache": "Mojáche", "Sañadiente": "Sañadiénte", "Legashi": "Leguáshi", "Thalassiano": "Talasiáno",
    "Rémol": "Rémol", "Dolanaar": "Dolanár", "Gnomeregan": "Nomeréguan", "Kharanos": "Járanos", "Shari Stilwell": "Shári Estílguel", "Kaivax": "Káivax", "Vito": "Víto", "SolidNano": "Sólid Náno",
    "Sakaan": "Sakán", "Mateo": "Matéo", "Massimo": "Másimo", "Rubén": "Rubén", "alexafm": "álexa éfe éme",
    "JcJ": "jota ce jota", "add-on": "ádon", "add-ons": "ádons", "PNJ": "pe ene jota",
}
FONETICA = FONETICA_APPLIO
CER_MAX_POR_FRASE = {   # 19-nov: hyps leídas una a una (solo nombres propios/cifras)
    "intro_1": 0.06, "p01_2": 0.06, "p11_0": 0.08, "p01_1": 0.06, "p01_3": 0.06, "p01_6": 0.06, "p01_7": 0.06, "p01_8": 0.06, "p02_2": 0.06, "p02_5": 0.06, "p03_2": 0.06, "p04_0": 0.06, "p04_2": 0.06, "p04_3": 0.06, "p04_4": 0.06, "p04_6": 0.06, "p05_6": 0.06, "p06_0": 0.06, "p06_1": 0.06, "p06_2": 0.06, "p06_7": 0.06, "p07_0": 0.06, "p07_2": 0.06, "p07_3": 0.06, "p07_5": 0.06, "p08_5": 0.06, "p08_7": 0.06, "p08_10": 0.06, "gracias1_0": 0.06, "p09_0": 0.06, "p09_2": 0.06, "p09_5": 0.06, "p09_7": 0.06, "p10_3": 0.06, "p10_4": 0.06, "p10_5": 0.06, "p11_2": 0.06, "p11_6": 0.06, "p12_1": 0.06, "p12_5": 0.06, "p13_0": 0.06, "p13_2": 0.06, "p13_3": 0.06, "p13_4": 0.06, "p14_5": 0.06, "p14_7": 0.06, "cierre_1": 0.06}
TAIL_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Si estás subiendo en World of Warcraft Forever con la ruta de Classic de memoria, te estás saltando zonas enteras que en dos mil diecinueve no existían.',
        'Una zona nueva con ciento cincuenta y una misiones entre el treinta y seis y el cuarenta y siete. Un Monte Hyjal que no empieza en el sesenta, sino en el cincuenta y tres.',
        'Y algo que nadie te avisa: la Alianza y la Horda ya no suben igual. Unos llegan a la zona nueva caminando, y los otros, casi siempre, en barco desde el otro continente.',
        'Llegar al sesenta pide cuatro millones ochenta y cuatro mil setecientos puntos de experiencia. Y el ochenta y ocho por ciento está entre el treinta y el sesenta.',
        'El primer sesenta de Forever lo hizo un grupo de cinco en algo más de tres días. La mayoría de nosotros vamos a tardar bastante más que eso.',
        'Por eso hoy te traigo la ruta completa, del uno al sesenta, en catorce paradas. Para la Alianza y para la Horda, zona por zona.',
        'En cada parada vas a ver el mapa real: dónde está la posada, dónde está el vuelo, qué mazmorra toca y qué es nuevo de Forever en ese tramo.',
        'Y antes de empezar, un consejo de un espectador, que lo dijo mejor que nadie: si solo vas a jugar un personaje, tómatelo con calma hasta el sesenta.',
        'Pero si te gusta subir alters, apúrale el paso. Esta ruta sirve para las dos cosas: para no perderte nada, o para no perder tiempo.',
    ]},
    {"id": 'p01', "frases": [
        'Parada uno. Del nivel uno al diez: las zonas iniciales, y una isla que no estaba.',
        'Cada raza empieza en su valle y, hacia el nivel cinco o seis, baja a su primer pueblo con posada.',
        'Los humanos bajan a Villadorada, en Elwynn. Los elfos de la noche, a Dolanaar, en Teldrassil. Y los enanos y gnomos, a Kharanos, entre la nieve.',
        'En la Horda, los orcos y los trols bajan del Valle de los Retos a Cerrotajo. Los taurens, al Poblado Pezuña de Sangre. Y los renegados, a Rémol, en Tirisfal.',
        'Y la novedad de Forever es la séptima salida: la Isla Zephras, donde empiezan los cielonatos de los dos bandos. Tiene unas ciento cuarenta misiones nuevas.',
        'Es la zona inicial que más dura: del tres al doce. Los cielonatos salen hacia el trece en dirigible: los de la Alianza a Dalaran, y los de la Horda a Cima del Trueno.',
        'Pero las zonas de siempre también cambiaron. Elwynn, contando Ventormenta, tiene más de cien misiones nuevas, y Mulgore, Durotar y Dun Morogh, unas cincuenta cada una.',
        'Y si eres renegado, en Tirisfal hay una subzona nueva: el Fuerte de Bandarion. Su cadena empieza al nivel ocho con Shari Stilwell, en Rémol.',
        'Un detalle que confunde a muchos: en Forever los niveles de las zonas son fijos. Hogger sigue siendo nivel once en Elwynn, y no se adapta a ti.',
        'Y no te preocupes por el ritmo: según los creadores, llegar al veinte en Forever tarda de media veinte horas y media. Casi lo mismo que en el juego original.',
    ]},
    {"id": 'p02', "frases": [
        'Parada dos. Del diez al quince: el primer cambio de zona.',
        'En la Alianza, los humanos bajan a los Páramos de Poniente, con centro en la Colina del Centinela. Ahí tienes posada y maestro de vuelo.',
        'Los enanos y gnomos van a Loch Modan, a Thelsamar. Y los elfos de la noche toman el barco a Costa Oscura, con centro en Auberdine.',
        'En la Horda, orcos, trols y taurens se juntan en Los Baldíos, en El Cruce. Y los renegados bajan al Bosque de Argénteos, a El Sepulcro.',
        'Y aquí llega la primera mazmorra nueva de Forever, solo para la Alianza: El Salón de Señores Feudales, del trece al dieciocho, escondido bajo Forjaz.',
        'La Horda tiene la suya bajo Entrañas: las Ruinas de Lordaeron, del quince al veinte, con cinco misiones nuevas. Y es mucho más grande que la Sima Ígnea.',
        'En Los Baldíos, sube de El Cruce hacia Trinquete y el sur. En los Páramos, de la Colina al Arroyo de la Luna, y de ahí a la entrada de las Minas de la Muerte.',
        'Y desde el catorce ya puedes empezar la cadena de la Bolsa de dormir acogedora, que en Forever arranca en la Granja Alexston, en los Páramos, o en una torre quemada de Los Baldíos.',
        'Esa bolsa te deja acampar donde quieras y descansar como en una posada. Para quien sube muchas horas, es oro puro.',
    ]},
    {"id": 'p03', "frases": [
        'Parada tres. Del quince al veinte: Crestagrana y Sierra Espolón.',
        'La Alianza sube a las Montañas Crestagrana, con centro en Villa del Lago, junto al lago. Y los elfos pasan de Costa Oscura a Vallefresno.',
        'La Horda baja al sur de Los Baldíos, al Campamento Taurajo, y de ahí sube a Sierra Espolón, al Refugio Roca del Sol.',
        'En Crestagrana, la ruta va de Villa del Lago al Molino de Alther y a las cascadas del este. Y fíjate en el borde este del mapa: ahí está la Avanzada del Sur.',
        'Ese puesto es nuevo de Forever, y no es casualidad: es la puerta a la zona nueva de Claros del Río, a la que la Alianza volverá al treinta y seis.',
        'O sea, Crestagrana es la zona que la Alianza pisa dos veces: ahora, en el quince, y otra vez cuando la cruce camino a Claros del Río.',
        'La mazmorra de este tramo, para la Alianza, son las Minas de la Muerte. Y en la Colina del Centinela hay una misión nueva para ella, de nivel dieciocho.',
        'Para la Horda son las Cuevas de los Lamentos, en Los Baldíos, con sus misiones de siempre de Cima del Trueno.',
        'Y al quince llega tu primera recompensa de Legado, un juguete. Pequeña, pero es la señal de que ya no eres un novato.',
    ]},
    {"id": 'burla0', "frases": [
        'Y antes de seguir, un comentario. Vito nos escribió esto: parece el tilín usando inteligencia artificial.',
        'Vito, si así suena el tilín con inteligencia artificial, el tilín acaba de aprenderse catorce zonas, todos los maestros de vuelo y dónde está cada posada de Azeroth.',
        'Ya quisiera yo que el tilín me armara la ruta. Mientras tanto, la armamos nosotros. Sigue con nosotros, que lo bueno empieza en el treinta.',
    ]},
    {"id": 'p04', "frases": [
        'Parada cuatro. Del veinte al veinticinco: Bosque del Ocaso, Los Humedales, Vallefresno y Laderas.',
        'La Alianza tiene dos caminos: el Bosque del Ocaso, con centro en Villa Oscura, y Los Humedales, con centro en el Puerto de Menethil.',
        'Y Los Humedales son la gran sorpresa de Forever para la Alianza: unas cincuenta misiones nuevas, casi todas de la Alianza, y subzonas nuevas como el Refugio Faucedraco.',
        'Los elfos de la noche siguen en Vallefresno, con centro en Astranaar. Y la Alianza gana algo que la Horda no tiene: un barco nuevo de Menethil a Costasur, y de ahí a Auberdine.',
        'La Horda sube a las Laderas de Trabalomas, con centro en el Molino Tarren. O a Vallefresno, al Puesto del Hachazo y a la Avanzada de Zoram\'gar.',
        'Y aquí va un mensaje que nos llegó hace nada. alexafm nos escribió que es nuevo, que es renegado de nivel veintidós, que las misiones élite le superan, y que solo conoce tres zonas.',
        'alexafm, esta parada es para ti. A tu nivel, sal de Argénteos hacia el Molino Tarren, en Laderas. O toma el zepelín de Tirisfal a Orgrimmar y baja a Vallefresno.',
        'Y las élites no se hacen solas: se juntan en grupo en el chat, sobre todo si van con una mazmorra. Ánimo, que lo que buscas, explorar sin add-ons, es la mejor forma de jugar esto.',
        'Las mazmorras del tramo: el Castillo de Colmillo Oscuro, en Argénteos, para la Horda, y las Cavernas de Brazanegra, en Vallefresno, para los dos bandos.',
    ]},
    {"id": 'p05', "frases": [
        'Parada cinco. Del veinticinco al treinta: Las Mil Agujas, y la excavación de Los Humedales.',
        'La Horda baja a Las Mil Agujas, con centro en el Poblado Viento Libre, en lo alto de los pilares. Y la Alianza puede entrar por Thalanaar, en el borde con Feralas.',
        'La ruta en Las Mil Agujas baja del poblado hacia los centauros del oeste, y termina en el Desierto de Sal, donde corren los goblins y los gnomos.',
        'Y aquí está la segunda mazmorra nueva de Forever: el Sitio de Excavación de Los Humedales, de nivel veinticuatro a veintinueve, más o menos.',
        'Lo curioso es que está en tierra de la Alianza, pero tiene misiones de los dos bandos: diez en total. La Horda las recoge en Sentencia, en Orgrimmar y en Cima del Trueno.',
        'Y es de las favoritas de los jugadores, porque está llena de raptores escondidos en la hierba alta. Ten cuidado por dónde pisas.',
        'Y al cerrar los veinte llegan dos clásicas: el Horado Rajacieno, en el sur de Los Baldíos, y Gnomeregan, en Dun Morogh.',
        'Un consejo de este tramo: en Forever las mazmorras dan más experiencia por muerte que en la beta. Blizzard la subió un cincuenta por ciento el ocho de noviembre.',
        'Así que hacer cada mazmorra una vez, con todas sus misiones, es de lo más rentable que puedes hacer en estos niveles.',
    ]},
    {"id": 'p06', "frases": [
        'Parada seis. Del treinta al treinta y cinco: Arathi, Alterac con Dalaran, y Desolace.',
        'En las Tierras Altas de Arathi, la Alianza y la Horda tienen sus campamentos enfrentados: el Refugio de la Zaga en el centro, y Sentencia al este.',
        'La ruta los lleva a los dos a los mismos sitios: los círculos de vínculo, el poblado de los trols Secacorteza, y el Castillo de Stromgarde.',
        'Y aquí otro comentario. Rubén nos escribió que le encanta pasearse por Trabalomas, Arathi y las Tierras del Interior, porque le recuerdan a la tierra rural donde vive.',
        'Y que duda que se mueva de ahí cuando llegue al sesenta. Rubén, esta parada es tuya: del treinta al treinta y cinco, Arathi es justo la zona que toca.',
        'Y al norte, en las Montañas de Alterac, está la novedad grande: Dalaran vuelve a su sitio, como una ciudad con habitantes, tiendas y misiones.',
        'Y tiene mazmorra nueva: la Ciudad de Dalaran, del veintiocho al treinta y tres, con seis misiones de nivel treinta y tres para los dos bandos.',
        'En Kalimdor, toca Desolace: la Alianza en Punta de Nijel, al norte, y la Horda en Aldea Cazasombras, al suroeste. Y en medio, el Cementerio de Kodos.',
        'Y si quieres otra mazmorra, el Monasterio Escarlata, en Tirisfal, empieza aquí, con su cementerio al treinta y uno.',
    ]},
    {"id": 'p07', "frases": [
        'Parada siete. Del treinta y cinco al cuarenta: la Vega de Tuercespina, el Marjal Revolcafango y Tierras Inhóspitas.',
        'En la Vega, la Alianza entra por el Asentamiento Rebelde, al norte, y la Horda por el Campamento Grom\'Gol. Los dos acaban en Bahía del Botín, al sur.',
        'La ruta pasa por la Expedición de Nesingwary, la base de Kurzen y la Arena Gurubashi. Y sí, aquí es donde más te van a emboscar en los conjuntos JcJ.',
        'En el Marjal Revolcafango, la Alianza tiene la Isla Theramore, y la Horda el Poblado Murohelecho. En Tierras Inhóspitas, la Horda tiene Kargath. Y en el Pantano de las Penas, Rocal.',
        'Y aquí está la tercera mazmorra nueva: La Ciudad Anegada, del treinta y cinco al cuarenta. Una ciudad trol hundida, mar adentro, frente a la costa oeste de la Vega.',
        'Tiene ocho misiones: la Horda las recoge en Grom\'Gol, los dos bandos en Bahía del Botín, y la Alianza en Costasur y en Dalaran.',
        'Y de Grom\'Gol sale también la misión que lleva a la Horda a la siguiente parada. Porque al treinta y ocho, la ruta de Forever se separa de la de Classic.',
        'Y si vas a Uldaman, en Tierras Inhóspitas, guárdala para más tarde: es del cuarenta y cuatro al cincuenta.',
    ]},
    {"id": 'burla1', "frases": [
        'Y hablando de la Horda, SolidNano nos escribió: el problema del chat en el servidor JcJ en la Horda es que la gente se la pasa hablando de política.',
        'SolidNano, es la Horda. Su historia entera es política: un jefe de guerra, luego otro, luego otro, y cada uno peleado con el anterior.',
        'Lo raro sería que el chat de Orgrimmar hablara de flores. Al menos en el chat nadie quema un árbol gigante. Todavía.',
    ]},
    {"id": 'p08', "frases": [
        'Parada ocho. Del treinta y seis al cuarenta y cinco: Claros del Río, la zona nueva grande.',
        'En inglés se llama Riverglades. Es una zona disputada en la costa sureste de los Reinos del Este, entre Crestagrana, Las Estepas Ardientes y el Pantano de las Penas.',
        'Tiene ciento cincuenta y una misiones nuevas, del treinta y seis al cuarenta y siete. Y ciento ocho de ellas sirven para los dos bandos.',
        'Y aquí está la gran diferencia entre los bandos. La Alianza entra a pie: de Villa del Lago, por la carretera al norte, hasta las puertas de Las Estepas Ardientes.',
        'En el poste de los letreros, gira a la derecha, cruza las Colinas Espinosas, y baja por la carretera hasta la Fortaleza de Farholde, en una isla del sureste.',
        'La Horda llega en barco: desde un muelle al este de Gadgetzan, en Tanaris, hasta el Puerto Polvomecha, el puerto de los goblins. O a pie desde Kargath o desde Rocal.',
        'Y ojo, Horda: el Puerto Polvomecha no tiene maestro de vuelo. Al llegar, corre por la carretera hasta Rog\'mar, en el centro, en el río, y activa el vuelo ahí.',
        'Desde Rog\'mar vuelas a Rocal, a Kargath, a Las Estepas y a Arathi. Y desde Farholde, la Alianza vuela a Villa del Lago, a Thelsamar y a la Vigilia de Morgan.',
        'La ruta va por la Avanzada de Terral, el Claro Soleado, el Sudario Crepuscular, y Pedreg\'ok, el pueblo de los ogros, que son aliados de la Horda.',
        'Y al norte está la mazmorra nueva: el Bastión de Krol\'dok, del cuarenta al cuarenta y cinco, con once misiones. Hazla una vez, entre el cuarenta y dos y el cuarenta y cuatro, con todas.',
        'Un dato de los creadores: Krol\'dok iba a ser una mazmorra de gnolls. Eligieron ogros porque eran de lo más común en el juego original.',
        'Y otro dato: en Claros del Río hay tres lagos en forma de herradura, los únicos así en todo World of Warcraft.',
        'Los que ya la hicieron lo resumen así: un jugador entró al cuarenta y salió al cuarenta y cuatro. Otro dice que le dio pena quedarse sin misiones.',
        'Y otro tardó más de seis horas en pasar del cuarenta y uno al cuarenta y dos. Así que no, no es una zona de paso. Es una zona para quedarse.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y aquí quiero parar un momento para darles las gracias. Sakaan nos escribió que, después de muchos años, por fin se pasó al oficial, y que empezó con Forever.',
        'Y que siempre pone nuestros videos de fondo mientras juega. Sakaan, ese es el mejor cumplido que nos pueden hacer.',
        'Y Mateo, que lleva dieciocho años jugando, fue por primera vez a la Feria de la Luna Negra solo para disfrutarla, sin pensar en el bono de experiencia.',
        'Todos sus comentarios se leen, y nos ayudan a mejorar cada video. Así que gracias. Y ahora, a la zona que casi nadie de la Alianza conoce.',
    ]},
    {"id": 'p09', "frases": [
        'Parada nueve. Del treinta y ocho al cuarenta y cinco: Shen\'dralas, la otra zona nueva.',
        'Está entre Desolace, Feralas y Mulgore, y se entra a pie por el Valle de los Huesos, al sur de Desolace.',
        'Sus misiones van del treinta y ocho al cuarenta y nueve. Y aquí la Horda gana: tiene dos campamentos propios, con Orgrul y Nerlokh, y la Alianza, que se sepa, ninguno.',
        'La Alianza puede entrar y hacer las misiones neutrales, que son unas veinte. Pero su camino natural del cuarenta al cuarenta y cinco es Claros del Río.',
        'La ruta baja del Valle de los Huesos al Mirador de Sombrapar, sigue hasta el Frente Magram, y cruza a los Jardines Desolados.',
        'Y la historia es de las buenas: los centauros Kolkar, Gelkis y Magram, y los shen\'dralar, los elfos de La Masacre. Mordent Evenshade te espera en el centro de la zona.',
        'Un consejo práctico: deja tu piedra de hogar en Aldea Cazasombras, en Desolace, que es lo más cerca que tienes para volver.',
        'Y de aquí salen las misiones para dos mazmorras clásicas: la Zahúrda Rajacieno, al cuarenta y cinco, y Maraudon, en Desolace.',
        'Es la única zona nueva sin un rango oficial. Las guías la ponen en sitios distintos, pero sus misiones encajan justo entre Claros del Río y Feralas.',
    ]},
    {"id": 'burla2', "frases": [
        'Y ya que hablamos de lo que la Alianza no encuentra: José Juan nos escribió que las voces nuevas de los otros videos suenan falsas, y que los videos le encantan, pero con la voz clásica.',
        'José Juan, mensaje recibido: la voz clásica volvió, y aquí se queda. Las otras siguen perdidas en el Valle de los Huesos.',
        'Y como en esa zona la Alianza no tiene ni un campamento, no creo que vuelvan pronto.',
    ]},
    {"id": 'p10', "frases": [
        'Parada diez. Del cuarenta al cuarenta y ocho: Tanaris, Feralas, Tierras del Interior, y la montura.',
        'Al cuarenta llegan las dos compras grandes: la equitación, unos cien de oro, y la doble especialización, que cuesta cincuenta. Junta el oro antes de llegar.',
        'En Tanaris, los dos bandos comparten Gadgetzan, cada uno con su maestro de vuelo. Y al este está el muelle del barco a Claros del Río.',
        'En Feralas, la Alianza está en el Bastión Plumaluna, en una isla del oeste, y la Horda en el Campamento Mojache, al este.',
        'En las Tierras del Interior, la Alianza sube a Pico Nidal, el nido de los grifos, y la Horda al Poblado Sañadiente, al sureste. La ruta acaba en Jintha\'Alor, la ciudad de los trols.',
        'La mazmorra estrella es Zul\'Farrak, del cuarenta y cinco al cincuenta y uno, en Tanaris. Y tiene dos misiones nuevas: una en Cima del Trueno y otra en Dalaran.',
        'Y eso es un patrón: en Dalaran hay dos archimagos que dan a la Alianza misiones para mazmorras de todo el mapa. Y en Cima del Trueno, la Horda tiene lo mismo.',
        'Pasa por ahí antes de cada mazmorra, y que ninguna te pille sin sus misiones.',
        'Y si vienes de Claros del Río, Tanaris también tiene misiones nuevas en el muelle de los goblins. Ese es el puente entre las dos zonas.',
    ]},
    {"id": 'p11', "frases": [
        'Seguimos con la siguiente parada. Del cuarenta y ocho al cincuenta y dos: Un\'Goro, Azshara, y una prisión.',
        'Aquí estaba el famoso muro de los cincuenta, donde en el juego original se acababan las misiones. Forever lo arregló con dos cosas nuevas.',
        'La primera es Azshara renovada: unas sesenta misiones nuevas, con la Alianza en Punta Talrendis, la Horda en Valormok, y un campamento de vanguardia thalassiano.',
        'La segunda es la Prisión de Alcaz, del cuarenta y ocho al cincuenta y tres: una isla prisión en la jungla, frente a la costa del Marjal Revolcafango, con nueve misiones.',
        'La Alianza las recoge en Theramore, en Ventormenta y en Dalaran. La Horda, en el propio Marjal. Y hay una neutral en Bahía del Botín.',
        'Y el Cráter de Un\'Goro, al cuarenta y ocho, sigue siendo lo que era: dinosaurios, el Refugio de Marshal arriba, y la ruta bajando por las fosas de alquitrán hasta el volcán.',
        'Si te falta experiencia, también tienes La Garganta de Fuego, Frondavil y Las Tierras Devastadas, que se comparten casi igual entre los dos bandos.',
        'Y El Templo de Atal\'Hakkar, en el Pantano de las Penas, es la mazmorra de este tramo, con las misiones de clase del cincuenta.',
    ]},
    {"id": 'p12', "frases": [
        'Parada doce. Del cincuenta al cincuenta y cinco: Las Estepas Ardientes, las Tierras de la Peste del Oeste, y Roca Negra.',
        'En Las Estepas Ardientes, los centros están en esquinas opuestas: la Alianza en la Vigilia de Morgan, al sureste, y la Horda en el Peñasco Llamarada, al norte.',
        'Y la Alianza tiene un atajo nuevo: desde la Fortaleza de Farholde, en Claros del Río, vuela directo a la Vigilia de Morgan.',
        'En las Tierras de la Peste del Oeste, la Alianza está en el Campamento del Orvallo, al sur. La Horda tiene El Baluarte, pero ojo: El Baluarte no tiene maestro de vuelo.',
        'Y la mazmorra del tramo es una de las más grandes del juego: Profundidades de Roca Negra, del cincuenta y dos al cincuenta y seis, dentro de la Montaña Roca Negra.',
        'Hay una misión que mucha gente se pierde: Franclorn Forjador, sobre su tumba en Las Estepas. Solo lo puedes ver estando muerto.',
        'Y en este tramo hay una buena noticia para la bolsa: desde el cuarenta y ocho, la mayoría de las misiones ya dan oro, gracias a un cambio del diez de noviembre.',
        'Y al cincuenta y cinco llega otra recompensa de Legado: el Oso espectral, una montura que se cobra con el tabernero de Trinquete, en Los Baldíos.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y otro momento para la gente que nos escribe. Lololulu dice que somos de los mejores canales de WoW, y que dan ganas de seguir escuchando cada video.',
        'Massimo nos contó que es su primera vez en WoW, y que el juego tiene todo lo que buscaba en un juego de rol en línea. Y Alexander, que con su vida de hoy solo puede jugar una hora al día.',
        'Alexander, esta ruta es para ti también: con una hora al día, saber a dónde ir es la diferencia. Y al sargento Sevilla, que oyó su nombre mientras jugaba con su guerrero: gracias a ti.',
    ]},
    {"id": 'p13', "frases": [
        'Parada trece. Del cincuenta y tres al cincuenta y ocho: Cuna del Invierno, Silithus, y las Tierras de la Peste del Este.',
        'Aquí los bandos por fin se juntan: los tres centros son neutrales o tienen vuelo para los dos.',
        'En Cuna del Invierno, el centro es Vista Eterna. La ruta sube a la Aldea Estrella Fugaz, baja a la cueva de Mazthoril, y termina en la Garganta Negro Rumor, al sur.',
        'En Silithus, el centro es el Fuerte Cenarion. Y en las Tierras de la Peste del Este, la Capilla de la Esperanza de la Luz, con vuelo para los dos bandos.',
        'Y la mazmorra nueva de este tramo es el Bastión Faucenegra, del cincuenta y cinco al sesenta: una ciudad de furbolgs en el norte de Azshara, con ocho misiones.',
        'No la confundas con el Bastión Fauces de Madera, el túnel de Frondavil a Cuna del Invierno. Nombres casi iguales, sitios totalmente distintos.',
        'Y el Bastión Faucenegra tiene premio extra: es una de las entradas a las Cavernas del Túmulo, una de las bandas que abren el nueve de diciembre.',
        'En la Capilla tienes, además, unas quince misiones nuevas, del cincuenta y siete al sesenta. Así que la Peste del Este también rinde más que antes.',
    ]},
    {"id": 'p14', "frases": [
        'Parada catorce, la última. Del cincuenta y seis al sesenta: el Monte Hyjal renovado.',
        'Mucha gente cree que Hyjal es una zona para cuando ya eres sesenta, y espera a tenerlo para entrar. Es un error.',
        'Sus ciento cuarenta y tres misiones nuevas van del cincuenta y tres al sesenta. O sea, puedes entrar antes del sesenta, y terminar de subir ahí.',
        'Se entra a pie desde Cuna del Invierno, por la Garganta Negro Rumor. Y desde las Laderas Maculadas, el vuelo te lleva de vuelta a Vista Eterna.',
        'La historia es preciosa: el bosque se está recuperando de la muerte de Archimonde, con los dioses salvajes, como Aviana, de vuelta.',
        'La ruta sube de las Laderas Maculadas al Santuario de Aviana, cruza a la Flora Antigua, donde la Alianza y la Horda tienen sus campamentos casi pegados, y termina en la Cima de la Eternidad.',
        'Y hay una última mazmorra nueva: El Bancal del Creador, del cincuenta y ocho al sesenta, una instalación de los titanes junto al Cráter de Un\'Goro.',
        'Y al llegar al sesenta, el nueve de diciembre te esperan las bandas: las Cavernas del Túmulo, la Cumbre Hyjal, y la Guarida de Onyxia.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esa es la ruta completa del uno al sesenta en World of Warcraft Forever. Catorce paradas, dos bandos, y unas cuantas zonas que la ruta de siempre no conoce.',
        'Si te quedas con una sola idea, que sea esta: en Forever, del treinta y cinco en adelante, la ruta ya no es la de antes. Claros del Río, Shen\'dralas y Hyjal te están esperando.',
        'Cuéntame en los comentarios en qué parada vas, y de qué bando eres. Todos se leen, y muchos acaban en el siguiente video.',
        'Si esta ruta te ahorró aunque sea una vuelta perdida, suscríbete, y compártela con ese amigo que siempre pregunta a dónde ir.',
        'Y nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`; tema = zona de la parada
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # OST de WoW (musica_wow.py): nota = tema de la zona de la parada; cada tramo <= 175 s (comprobar tras `tiempo`)
        (['intro'], 'Legends of Azeroth'),
        (['p01'], 'Dun Morogh'),
        (['p02'], 'Páramos'),
        (['p03', 'burla0'], 'Elwynn'),
        (['p04'], 'Bosque del Ocaso'),
        (['p05'], 'Mil Agujas'),
        (['p06'], 'Baldíos'),
        (['p07', 'burla1'], 'Tuercespina'),
        (['p08'], 'Vallefresno'),
        (['gracias1'], 'Posada'),
        (['p09', 'burla2'], 'Feralas'),
        (['p10'], 'Tanaris'),
        (['p11'], "Un'Goro"),
        (['p12'], 'Roca Negra'),
        (['gracias2'], 'Taberna orca'),
        (['p13'], 'Cuna del Invierno'),
        (['p14'], 'Claro de la Luna'),
        (['cierre'], 'Legends of Azeroth'),
    ],
)

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
