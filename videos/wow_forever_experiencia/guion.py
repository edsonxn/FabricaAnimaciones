# -*- coding: utf-8 -*-
"""GUION — «30 cosas para vivir la experiencia REAL de WoW Forever» (Crónicas de Warcraft, 12-nov-2026).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Idea del usuario (12-nov): inspirado en «No salgo del WoW Forever ni a la calle» de Joseju (PGmkWXy9ANY): Forever como EXPERIENCIA,
no como carrera al 60. Parte lista (30 → 1), parte análisis (escena `friccion`). ~30 min.
Investigación: videos/_investigacion_wow_forever_experiencia.md. Lo de Classic sin confirmar en Forever se dice «en Classic».
SIN OVERGEAR (el usuario, 12-nov-2026: «Sin Overgear, que sea así, sin promoción»).
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras.
Comentarios (≤ 10 días, ninguno usado antes; críticas ≥ 2-3 con sarcasmo): intro/burla2 @AlbertoHans-k7f8d (Ugzmf…) ·
burla0 @arnoldhowardriberth8208 (UgzPrV6T…) · burla1 @Fetixe22 (Ugw5eSQe…) · gracias1 @yorshnado8100 @pablisho6299 ·
gracias2 @AlexAnder-z1i7l @sgto.sevilla6976.
"""

TITULO = "30 cosas para vivir la experiencia REAL de WoW Forever (sin correr al 60)"
ARCHIVO = "wow_forever_experiencia"
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
    "CRONICAS10": "Crónicas diez", "Crónicas de Warcraft": "Crónicas de uárcraft", "Ventormenta": "Ventorménta",
    "Burning Crusade": "Bérnin Kruséid", "Hyjal Summit": "Jáyal Sámit", "Hyjal": "Jáyal", "Questie": "Cuésti", "Remy": "Rémi",
    "Nesingwary": "Nésinguari", "Hemingway": "Jémingüei", "Riverglades": "Ríverglèids", "Shen'dralas": "Shendrálas",
    "The Drowned City": "de Dráund Síti", "Krol'dok Stronghold": "Króldok Estrónjold", "Alcaz Island Prison": "Álcaz Áiland Prísson",
    "Blackmaw Hold": "Blákmo Jóld", "Shaper's Terrace": "Shéipers Térras", "Barrow Deeps": "Bárrou Díps",
    "Farholde Keep": "Fárjold Kíp", "Rog'mar": "Rógmar", "Steamwheedle Port": "Stímuidel Port", "Powderfuse Port": "Páuderfius Port",
    "Gadgetzan": "Gádyetzan", "Kargath": "Kárgaz", "Grom'gol": "Gromgól", "Zul'Farrak": "Zul Fárak", "Gahz'rilla": "Gazríla",
    "Jintha'Alor": "Yinza Alór", "Franclorn": "Fránclorn", "Linken": "Línken", "J.D. Collie": "Yei Di Cóli",
    "Atal'Hakkar": "Átal Jákar", "Hakkar": "Jákar", "Ogtinc": "Ógtink", "Xylem": "Sáilem", "Windsor": "Uíndsor",
    "Drakkisath": "Drákisaz", "Onyxia": "Oníxia", "Rexxar": "Réxar", "Krinkle": "Krínkel", "Araj": "Áraj", "Andorhal": "Ándorjal",
    "Scholomance": "Escolománs", "Caer Darrow": "Kéer Dárrou", "Zverenhoff": "Svérenjof", "Grazle": "Gréizel", "Nafien": "Náfien",
    "Un'Goro": "Ungóro", "Tanaris": "Tanáris", "Thrall": "Zrol", "Bolvar": "Bólvar", "Theramore": "Zéramor",
    "Gustaf VanHowzen": "Gústaf Van Jáuzen", "Jokerd": "Yókerd", "Azshara": "Asshára", "Mazthoril": "Mázzoril", "Haleh": "Jálej",
    "Betina Bigglezink": "Betína Bíguelsink", "Herod": "Jérod", "Desolace": "Desolás", "Arathi": "Aráti", "Zelda": "Sélda",
    "Teldrassil": "Teldrásil", "Elwynn": "Éluin", "Auberdine": "Óberdin", "Orgrimmar": "Orgrímar", "Menethil": "Ménezil",
    "Mankrik": "Mánkrik", "JcJ": "jota ce jota", "add-on": "ádon", "VanCleef": "Van Clíf", "Edwin": "Édwin", "Mor'Ladim": "Mórladim",
    "Hogger": "Jóguer", "Durotar": "Durotár", "Dun Morogh": "Dun Mórog", "Defias": "Defías", "Darnassus": "Darnásus",
    "CurseForge": "Kérsforch", "Stalvan": "Estálvan", "Sayge": "Séich", "Mulgore": "Mulgór", "Loch Modan": "Loj Módan", "Tarren": "Tárren", "PNJ": "pe ene jota",
    "Brogan": "Brógan", "Yorsh": "Yórsh", "Fetixe": "Fetíxe", "Arnold": "Árnold",
    "Wowhead": "Uaujéd", "Spoken": "Spóuken", "Doan": "Dóan", "Morgan": "Mórgan",
}
FONETICA = FONETICA_APPLIO
# Applio da siempre la misma toma: hipótesis de Whisper leídas el 10-nov (solo nombres propios/cifras)
CER_MAX_POR_FRASE = {   # 12-nov: transcripciones leídas una a una (Acerot, Dumorog, Questy, JCJ, Mancric, cifras en número...)
    "friccion_4": 0.08, "c30_2": 0.08, "c29_5": 0.08, "c28_4": 0.08, "c27b_0": 0.08, "burla1_2": 0.08, "c26_1": 0.08, "c25_1": 0.08, "c23_0": 0.08, "c23_1": 0.08, "c23_2": 0.08, "gracias1_1": 0.08, "gracias1_4": 0.08, "c20_5": 0.08, "c14_1": 0.08, "c12_0": 0.08, "gracias2_3": 0.08, "c10_4": 0.08, "c09_1": 0.08, "c08_3": 0.08, "c06_1": 0.08, "c05_2": 0.08, "c05_4": 0.08, "c04_1": 0.08, "c02_3": 0.08, "burla0_3": 0.05, "c11_0": 0.05, "c09_0": 0.05}
TAIL_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={"scene-081": 0.06, "scene-186": 0.06, "scene-187": 0.06},   # puerto de Ventormenta con barras laterales
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 38   # 39 escenas (sin Overgear, el usuario 12-nov)
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # OST de WoW (musica_wow.py): nota = zona del tema
        (['intro', 'friccion'], 'Elwynn'),
        (['c30', 'c29', 'c28'], 'Dun Morogh'),
        (['burla0', 'c27', 'c27b', 'burla1'], 'Tirisfal'),
        (['c26', 'c25', 'c24'], 'Elwynn'),
        (['c23', 'c22', 'c21'], 'Durotar'),
        (['gracias1', 'c20', 'c19'], 'Baldíos'),
        (['c18', 'c17'], 'Posada'),
        (['c16', 'c15'], 'Claro de la Luna'),
        (['c14', 'c13'], 'Ocaso'),
        (['c12', 'c11', 'gracias2'], 'Teldrassil'),
        (['c10', 'c09', 'c08'], 'Durotar'),
        (['c07', 'c06', 'burla2'], 'Dun Morogh'),
        (['c05'], 'Baldíos'),
        (['c04'], 'Ventormenta'),
        (['c03', 'c02'], 'Elwynn'),
        (['c01', 'cierre'], 'Ventormenta'),
    ],
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Hace unos días, Alberto nos escribió esto: nivel treinta, sí, cómo no. No puedo ni salir de Villa del Lago, este juego es imposible.',
        'Alberto, este video es para ti. Porque no tienes que salir de Villa del Lago. Nadie te está esperando en el nivel sesenta con un cronómetro.',
        'World of Warcraft Forever salió el cuatro de noviembre, y en una semana ya vimos de todo: rutas óptimas, listas de errores, y gente que ya llegó al sesenta.',
        'Nosotros también hicimos esas listas. Y hoy vamos a hacer justo lo contrario.',
        'Porque hay dos formas de jugar Forever. Una es la de Retail: correr al máximo, saltarte los textos, y entrar a la rueda de mazmorras lo antes posible.',
        'La otra es la de dos mil cuatro. Cuando cruzar un bosque era un viaje, cuando conocías a tu hermandad en una misión de élite, y cuando cada nivel se sentía como una semana de vida.',
        'Y aquí está lo curioso: Forever se diseñó para la segunda. El nivel máximo es sesenta, y se queda en sesenta para siempre.',
        'No hay expansión que te obligue a correr. Lo nuevo va a crecer hacia los lados, no hacia arriba. Así que el leveleo no es el trámite: es el juego.',
        'Hoy te traigo treinta cosas que puedes hacer para vivir la experiencia real de World of Warcraft Forever. Del treinta al uno.',
        'No son trucos para subir más rápido. Son al revés: cosas para que, cuando llegues al sesenta, te dé un poquito de pena haber llegado.',
    ]},
    {"id": 'friccion', "frases": [
        'Pero antes de la lista, hay que entender una palabra. La palabra es fricción.',
        'Fricción es todo lo que el juego te pone en medio: caminar diez minutos, no poder hacer una misión solo, quedarte sin flechas, tener que preguntar.',
        'En Retail, casi toda esa fricción se fue quitando, expansión tras expansión, porque había que ponerte al día rápido con lo nuevo.',
        'Y el mundo, poco a poco, se volvió un pasillo hacia el contenido final. Un parque de atracciones con filas muy cortas.',
        'Pero esa fricción era la que hacía que todo pesara. Una misión de siete colas de múrloc, en grupo, se vuelve una pequeña aventura con desconocidos.',
        'Y hay un truco de la memoria: no medimos el tiempo en minutos, lo medimos en recuerdos. Un viaje con diez lugares distintos se siente como una historia.',
        'Por eso, veinte años después, nadie recuerda la mazmorra que hizo en cinco minutos. Pero todos recuerdan la primera vez que cruzaron Los Baldíos.',
        'Forever le añadió muchas comodidades, pero dejó esa fricción en su sitio. Y estas treinta cosas son formas de abrazarla, en lugar de esquivarla.',
    ]},
    {"id": 'c30', "frases": [
        'Número treinta. Ponle apellido a tu personaje.',
        'Parece una tontería, pero empieza en la pantalla de creación. En Forever no eliges un reino: eliges un conjunto de reglas.',
        'Normal, JcJ, Juego de rol y Juego de rol JcJ. Y en los de rol, la idea es que tu personaje sea alguien, no un nombre con tres equis y un número.',
        'Un enano que se llama Brogan Barbapétrea ya tiene una historia: una familia, una mina, y probablemente una deuda en la taberna de Forjaz.',
        'Y no hace falta que hables como en una obra de teatro todo el día. Basta con que, cuando alguien lea tu nombre sobre tu cabeza, se imagine algo.',
        'Además, en Forever el conjunto de reglas no se cambia libremente. Si te equivocas, toca hacer otro personaje. Así que piénsalo desde el nivel uno.',
    ]},
    {"id": 'c29', "frases": [
        'Número veintinueve. Juega en español, y habla en el chat general.',
        'En Forever no hay reinos fijos: el juego te junta con gente según tu idioma preferido en línea. Está en Opciones, en Idiomas y redes sociales.',
        'Si lo dejas en inglés, tu zona se llena de gente con la que no te entiendes. Si lo pones en español, el chat general cobra vida.',
        'Y ese chat es medio juego. Gente preguntando dónde está un PNJ, otro vendiendo agua, otro contando un chiste malísimo, y tres respondiéndole.',
        'Ojo, que el ajuste es de toda la cuenta y tiene un enfriamiento de veinticuatro horas. Así que no lo andes cambiando cada rato.',
        'Y escribe. Saluda cuando entres a una zona, pregunta aunque lo puedas buscar en internet. Una pregunta en el chat es la forma más vieja de hacer amigos en Azeroth.',
    ]},
    {"id": 'c28', "frases": [
        'Número veintiocho. Elige tu clase por la fantasía, no por la tabla de daño.',
        'En otros juegos, cambiar de clase solo cambia el color de los números. En World of Warcraft Forever, cambia tu vida entera en Azeroth.',
        'El mago se hace su propia comida y agua gratis. El cazador tiene que comprar flechas y darle de comer a su mascota. Y el brujo carga fragmentos de alma que le ocupan la bolsa.',
        'Pero el brujo también puede invocar a sus compañeros desde el otro lado del mundo. Y el druida se convierte en gato y se escabulle donde nadie más puede.',
        'Y la raza también cuenta. No es lo mismo empezar como enano en la nieve de Dun Morogh que como elfo de la noche en Teldrassil, aunque juegues la misma clase.',
        'Esas diferencias son injustas, a propósito. Y por eso cada personaje se siente distinto. Elige al que quieras ser, no al que gane la tabla.',
    ]},
    {"id": 'burla0', "frases": [
        'Y antes de seguir, alguien salió a defender a Marcos, el del video anterior.',
        'Arnold escribió: deja a Marcos en paz, tiene la razón. Qué tonto paga por que le enseñen a jugar.',
        'Arnold, me encanta que Marcos ya tenga abogado. Eso es lo más Forever que he visto: hacer grupo para una misión de élite en los comentarios.',
        'Y fíjate en lo que acabas de hacer: viste a un compañero en problemas, y fuiste a ayudarlo sin que nadie te pagara. Eso es enseñar a jugar, Arnold. Gratis.',
        'Le acabas de enseñar a Marcos a no estar solo. Lo vamos a anotar en la lista, porque es una de las treinta.',
    ]},
    {"id": 'c27', "frases": [
        'Número veintisiete. Lee las misiones. De verdad.',
        'La mayoría le damos a aceptar sin leer, y vamos a matar diez arañas. Pero detrás de esas diez arañas casi siempre hay una historia.',
        'Una viuda en el Bosque del Ocaso, un granjero de los Páramos de Poniente que lo perdió todo, un orco en Durotar que no quiere volver a la guerra.',
        'En Forever hay más de mil misiones nuevas. Nadie las ha leído todavía. Tú puedes ser de los primeros en saber de qué van.',
        'Y si te da flojera leer, nosotros hicimos un add-on gratis que le pone voz en español a las misiones de inicio, una voz para cada personaje.',
    ]},
    {"id": 'c27b', "post": 5.6, "frases": [
        'Se llama Voces en español, está en CurseForge, y el enlace está en la descripción. Escucha a tu primer PNJ hablando en tu idioma.',
    ]},
    {"id": 'burla1', "frases": [
        'Y aquí va otra crítica, de las que se contestan con cariño.',
        'Fetixe escribió: fomentando addons de paga, cuando el mismo juego prohíbe los addons de paga. La gente mata el mismo juego que juega.',
        'Fetixe, tranquilo, que el add-on que hicimos es gratis. Gratis de verdad. No cuesta ni una moneda de cobre.',
        'Lo único que pedimos es una donación voluntaria para doblar más misiones al español. Igual que el mendigo de Ventormenta, pero con un micrófono.',
        'Así que nadie está matando el juego. Lo estamos intentando hacer hablar.',
    ]},
    {"id": 'c26', "frases": [
        'Número veintiséis. Apaga las flechas.',
        'Los ayudantes de misiones como Questie te ponen cada objetivo en el mapa. Son muy cómodos, y también te convierten en un repartidor que sigue un GPS.',
        'Prueba una zona sin ellos. Lee dónde dice el texto que está el campamento de los gnolls, mira el mapa, y sigue los postes del camino.',
        'Los postes de madera de los cruces existen desde dos mil cuatro, y casi nadie los mira. Ahí dice hacia dónde queda cada pueblo.',
        'Y si te pierdes, pregunta en el chat. Alguien te va a contestar, y a veces ese alguien termina siendo tu compañero de los próximos veinte niveles.',
        'Perderse un poco no es perder el tiempo. Así es como el mapa se te queda en la cabeza, y no en el add-on.',
    ]},
    {"id": 'c25', "frases": [
        'Número veinticinco. Haz una misión de élite con desconocidos.',
        'El ejemplo perfecto está en el Bosque de Elwynn: Hogger, el gnoll de élite de nivel once que lleva veinte años humillando a los humanos.',
        'Si vas solo, Hogger te destroza en segundos, pero cuando ves a tres jugadores dando vueltas por la misma zona, mándales una invitación. No hace falta decir mucho.',
        'Y pasa algo muy curioso. A los cinco minutos ya están coordinándose, uno pone el cuerpo, otro cura, y el más valiente le hace de cebo.',
        'Cuando por fin cae Hogger, se siente como derrotar a un jefe de banda. Y muchos de esos grupos se quedan juntos para la siguiente misión.',
        'Las misiones de élite existen justo para eso: para que necesites a alguien. En Forever, Hogger no se adapta a tu nivel, y los objetos de misión se reparten por turnos en el grupo. El juego quiere que vayas acompañado.',
    ]},
    {"id": 'c24', "frases": [
        'Número veinticuatro. Viaja a pie la primera vez.',
        'En Forever no hay portales de ciudad ni monturas voladoras. Y los vuelos en grifo o en murciélago solo existen si antes descubriste cada parada.',
        'Así que la primera vez que vas a una zona nueva, ve caminando. Por el camino, no por el atajo.',
        'Vas a pasar por un puente, una granja, una torre en ruinas, un río con múrlocs. Y cada uno de esos lugares se te queda en la memoria.',
        'Ese mapa no es tan grande como el de los juegos modernos, pero está tan lleno de detalles que caminarlo se siente como cruzar un continente entero.',
        'Y cuando por fin llegas a un maestro de vuelo, el primer viaje en grifo sobre todo lo que caminaste es una de las mejores vistas del juego. Hasta hay un desafío de legado que te lo premia: explora todo el mapa del mundo con el mismo personaje.',
    ]},
    {"id": 'c23', "frases": [
        'Número veintitrés. Sube al zepelín, o al barco, y no te desconectes.',
        'Entre Orgrimmar, Entrañas y la Vega de Tuercespina vuelan los zepelines de los goblins. Y entre Menethil, Theramore y Auberdine navegan los barcos.',
        'Mucha gente aprovecha el viaje para ir por un café. Prueba quedarte. Ver aparecer otro continente en el horizonte es de los momentos más bonitos de Azeroth.',
        'Y no viajas solo: en la cubierta hay jugadores de todos los niveles. Alguien salta, alguien baila, alguien pregunta adónde va esto.',
        'Hay quien se sube a un zepelín sin saber a dónde va, solo para ver qué hay del otro lado. Y termina en un continente lleno de enemigos de nivel cuarenta.',
        'Eso, en Retail, sería un error. En Forever es una aventura.',
    ]},
    {"id": 'c22', "frases": [
        'Número veintidós. Enciende el campamento, y siéntate con otros.',
        'El campamento es de lo mejor que trae Forever. Se desbloquea muy al principio, con una misión sencilla hacia el nivel cinco.',
        'Un cocinero enciende la hoguera, y cada jugador puede sumar un objeto de su profesión: una tienda de campamento, un estandarte, una vela, hasta una pecera. Y cada objeto da un beneficio.',
        'Pero aquí está la magia: para ganarlo, hay que quedarse sentado al menos un minuto junto al fuego. Y si hay más gente, mejor.',
        'O sea, Blizzard metió una mecánica para que la gente se siente a charlar. En un juego de dos mil veintiséis. Eso es lo más de aventura de fantasía que hay.',
        'Así que cuando veas una hoguera con tres extraños, siéntate. Saluda. Pregunta de dónde vienen. Esa hoguera es la nueva posada.',
    ]},
    {"id": 'c21', "frases": [
        'Número veintiuno. Sube la pesca.',
        'Nadie sube la pesca porque tiene prisa. Y justo por eso es de las cosas más de World of Warcraft que puedes hacer.',
        'Te sientas en un muelle, lanzas la caña, y miras el agua. En Ventormenta, en los muelles de Trinquete, o en el lago de Villa del Lago, Alberto.',
        'Y en Forever, la pesca hasta suma al campamento: el pescador pone una pecera que da un beneficio a todo el grupo.',
        'Y el concurso de pesca de los domingos también volvió, en la Vega de Tuercespina. Ahora ganan los primeros cincuenta, y te llevas una moneda exclusiva que se cambia en Bahía del Botín.',
        'Pescar no te sube de nivel. Pero te regala lo que más falta le hace a este juego tan lleno de cosas: un rato de calma.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y antes de seguir, gracias por los comentarios de estos días.',
        'Yorsh escribió que sigue el canal desde el suscriptor ochenta, que nunca había comentado, y que se nota que los guiones no son de una máquina.',
        'Yorsh, ochenta suscriptores. Eso era cuando el canal cabía entero en una posada de Villadorada. Gracias por quedarte todo el viaje.',
        'Y Pablo escribió algo que me hizo mucha ilusión: yo ni juego WoW, pero siempre veo tus videos.',
        'Pablo, eso es justo lo que intento con este video: que hasta quien no juega entienda por qué tanta gente vuelve a Azeroth.',
        'Todos los comentarios se leen, y todos se toman en cuenta para mejorar el canal. Así que cuéntame en cuál de estas treinta te reconoces.',
    ]},
    {"id": 'c20', "frases": [
        'Número veinte. Vende algo hecho por ti.',
        'Mucha gente usa la casa de subastas para tirar lo que le sobra. Prueba lo contrario: hazte comerciante de tu propia zona.',
        'Cocina pescado y véndelo a los que pasan. Fabrica bolsas con sastrería y regálaselas a los novatos. Abre una tienda en la puerta de la posada.',
        'Hay jugadores que se hicieron un personaje solo para vender comida y agua por una moneda de plata, y la gente hace fila para comprarles. Por diversión.',
        'Y en Forever el comercio tiene su propio sistema: el Favor de comerciante. Lo ganas entregando cajas de materiales en el campamento de tu facción.',
        'La Alianza tiene a la Autoridad Comercial de Azeroth en los Montes Crestagrana, y la Horda, Logística y suministros de Durotar, en Los Baldíos.',
        'Ahí se compran más de seiscientas recetas nuevas. Así que ser el artesano del barrio en Forever no solo es bonito: también es negocio.',
    ]},
    {"id": 'c19', "frases": [
        'Número diecinueve. Camina hasta la mazmorra.',
        'En Forever no hay buscador de grupos que te teletransporta a la puerta. Hay que armar el grupo en el chat, y llegar caminando.',
        'Las Minas de la Muerte, en los Páramos de Poniente. Las Cuevas de los Lamentos, en Los Baldíos. Y cada una tiene su viaje antes de la primera pelea.',
        'Escribes en el chat que buscas tanque. Alguien contesta. Se juntan en el pueblo, caminan juntos, y en el camino ya están charlando.',
        'Y dentro, nadie corre. Hay que controlar, esperar el maná, y avisar antes de jalar. Y si alguien muere, todos lo esperan.',
        'Una mazmorra así dura más, sí. Pero la recuerdas. Y a veces sales de ella con tres amigos nuevos en la lista.',
    ]},
    {"id": 'c18', "frases": [
        'Número dieciocho. Únete a una hermandad de leveleo, no a una de bandas.',
        'Al principio, no hace falta la hermandad que va a limpiar Onyxia primero. Busca una de gente que sube con calma, en tu idioma, a tus horas.',
        'Y en Forever esto tiene premio extra. El sistema de capas, Caras conocidas, intenta que los miembros de una misma hermandad siempre se vean en el mundo.',
        'Y quien agrupó contigo una vez, luego te aparece con el nombre de otro color. O sea, tu hermandad no es solo un chat verde: es la gente que te vas a ir cruzando por los caminos.',
        'Así se hacen amigos de adulto: viendo una y otra vez a las mismas personas. Y World of Warcraft hace eso mejor que casi cualquier otro juego.',
    ]},
    {"id": 'c17', "frases": [
        'Número diecisiete. Descansa en la posada.',
        'Cuando te desconectas en una posada o en una ciudad, acumulas descanso. Y al volver, cada enemigo que matas te da el doble de experiencia durante un buen rato.',
        'Así que el juego te premia por irte a dormir, literalmente.',
        'Pero la posada es más que eso. Hay un posadero, una chimenea, y siempre hay alguien bailando encima de una mesa.',
        'Antes de desconectarte, siéntate con los demás y usa los gestos, como saludar, brindar, sentarte o dormir. Son tontos, y por eso funcionan.',
        'Y si tu personaje es de rol, la posada es tu escenario. Una historia contada junto a la chimenea de Villadorada vale más que diez misiones.',
    ]},
    {"id": 'c16', "frases": [
        'Número dieciséis. Haz la misión de tu clase.',
        'Hay misiones que solo existen para tu clase, y son de las mejores del juego. Porque no te dan solo un objeto: te cuentan quién eres.',
        'El brujo empieza sin demonio: su primer diablillo lo gana con una misión, y más adelante ata a su súcubo con un ritual. El chamán recorre el mundo buscando sus tótems de tierra, fuego, agua y aire.',
        'El druida aprende a convertirse en oso hablando con el Gran Espíritu del Oso, y en Forever gana la forma felina al nivel veinte con una misión nueva, en un túmulo lleno de espíritus de gato. Y el guerrero tiene que demostrar su valor en pruebas que no se olvidan.',
        'Y al nivel cuarenta, el paladín y el brujo consiguen su montura con su propia historia, sin pagarla en un establo.',
        'Mucha gente las salta porque son largas y te mandan lejos. Justo por eso hay que hacerlas. Son el momento en que tu clase deja de ser una barra de habilidades.',
    ]},
    {"id": 'c15', "frases": [
        'Número quince. Si eres cazador, domestica una bestia rara, y ponle nombre.',
        'El cazador puede domesticar casi cualquier bestia del mundo. Y algunas son únicas: tienen otro color, otro tamaño, o aparecen muy de vez en cuando.',
        'Encontrarla es una aventura en sí misma. Esperar a que aparezca, ir del nivel correcto, y llegar antes que otro cazador.',
        'Y luego viene lo mejor: el nombre. Tu brujo tiene que aguantarse con el nombre que trae su demonio. Tu cazador, no.',
        'Ponle el nombre de tu perro, de tu abuela, o el de un postre. Esa bestia te va a acompañar sesenta niveles. Que se lo gane.',
    ]},
    {"id": 'c14', "frases": [
        'Número catorce. Termina una cadena larga con historia: la Hermandad Defias.',
        'En los Páramos de Poniente, los granjeros están desesperados, y hay ladrones con pañuelo rojo por todas partes. Parece una zona más.',
        'Pero si sigues las misiones, descubres que esos ladrones eran los albañiles que reconstruyeron Ventormenta. Y que la ciudad nunca les pagó.',
        'La historia te lleva por toda la zona, hasta el corazón de las Minas de la Muerte, donde te espera su líder, Edwin VanCleef, y un barco pirata escondido bajo tierra.',
        'Y al final, la cadena te deja una pregunta incómoda sobre Ventormenta: quién era el verdadero ladrón, si los albañiles o los nobles que no les pagaron.',
        'Si haces las misiones sueltas, matas ladrones. Si haces la cadena entera, entiendes por qué hay ladrones. Y esa diferencia es todo el juego.',
    ]},
    {"id": 'c13', "frases": [
        'Número trece. Ve de noche al Bosque del Ocaso.',
        'Esta nos la pidieron en los comentarios, y con razón: el Bosque del Ocaso tiene las misiones más tétricas de los primeros niveles.',
        'Un pueblo llamado Villa Oscura, rodeado de lobos, arañas, no-muertos y un cementerio lleno de neblina. Siempre es de noche.',
        'Hay una historia de un amor que terminó en asesinato, La leyenda de Stalvan, la de Stalvan Mantoniebla, que vas descubriendo carta por carta, como un detective.',
        'Y hay un no-muerto de élite, Mor\'Ladim, que se pasea por el cementerio y mata a los que no lo vieron venir. Para esa, mejor ve en grupo de tres.',
        'Apaga la luz de tu cuarto, sube el volumen, y lee cada carta. El Bosque del Ocaso es una historia de terror. Si la corres, te la pierdes.',
    ]},
    {"id": 'c12', "frases": [
        'Número doce. Caza a los raros.',
        'En cada zona hay enemigos especiales con un dragón plateado en su retrato. Aparecen pocas veces, en sitios concretos, y a veces sueltan algo bueno.',
        'Pero lo bonito no es el botín. Es la historia de encontrarlo: ir por un camino, ver el retrato plateado, y avisar en el chat que lo encontraste.',
        'De pronto, cinco jugadores llegan corriendo, y se arma una pelea en la que nadie se conocía hace un minuto.',
        'No necesitas un add-on que te avise. Basta con caminar por los rincones de cada zona y mirar bien a quién atacas.',
    ]},
    {"id": 'c11', "frases": [
        'Número once. Explora el mundo sin misiones.',
        'Un día, en lugar de abrir el registro de misiones, elige una montaña en el horizonte y ve hacia ella. Sin objetivo.',
        'World of Warcraft tiene rincones que ninguna misión te pide visitar: ruinas, cuevas, islas, picos donde nadie debería poder subir.',
        'Y en Forever hay zonas y lugares nuevos, de los que nadie tiene todavía una guía completa. Lo que encuentres, lo encontraste tú.',
        'En dos mil cuatro, así se descubrían los secretos. Alguien se perdía, encontraba algo raro, y lo contaba en el foro. Puedes ser ese alguien.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y otra ronda de comentarios, porque se la ganaron.',
        'Alexander escribió que no se pierde ningún video del canal. Y el sargento Sevilla, simplemente: qué grande eres, muchas gracias.',
        'Sargento, a sus órdenes. Y a ti, Alexander, gracias: sin ustedes, este canal sería un orco hablando solo en Durotar.',
        'Y si este video te está dando ganas de volver a Azeroth sin prisa, la mejor forma de ayudar al canal es suscribirte, que es gratis y tarda menos que un vuelo en grifo.',
    ]},
    {"id": 'c10', "frases": [
        'Número diez. Cruza el mundo con un personaje de nivel bajo.',
        'Si eres de la Horda, prueba esto: haz un personaje nuevo e intenta llegar al Bosque de Elwynn, la tierra de los humanos.',
        'Vas a tener que subir al zepelín, cruzar zonas donde todo te mata de un golpe, esconderte, morir, revivir en el cementerio, y seguir caminando.',
        'Es una tontería, y es una de las mejores aventuras que vas a tener. Porque el mundo es tan grande y tan peligroso, que llegar se siente como una hazaña.',
        'Y si eres de la Alianza, lo mismo al revés, hasta Durotar. Y si un jugador del otro bando te encuentra en su zona de inicio, va a saber que cruzaste medio mundo para estar ahí.',
    ]},
    {"id": 'c09', "frases": [
        'Número nueve. Aprende a morir bien, como se moría en dos mil cuatro.',
        'En Retail, la muerte casi no importa. En Forever sí: cuando mueres, tu espíritu aparece en el cementerio, y tienes que correr hasta tu cuerpo.',
        'Y mientras corres como fantasma, el mundo se ve gris y en silencio. Es uno de los momentos más bonitos y más tristes del juego.',
        'Si resucitas con el ángel del cementerio, pagas con debilidad y reparaciones. Así que casi siempre vale la pena el paseo.',
        'Y si tu clase puede resucitar, hazlo por otros. Un sacerdote que revive a un desconocido en medio de un campamento enemigo hace un amigo para siempre.',
        'Morir en este juego cuesta. Y por eso sobrevivir tiene mérito.',
    ]},
    {"id": 'c08', "frases": [
        'Número ocho. Haz la búsqueda del tesoro del naufragio.',
        'Esta es nueva de Forever. Hacia el nivel catorce, en un barco hundido de los Páramos de Poniente si eres Alianza, o de Los Baldíos si eres Horda, empieza una cacería.',
        'Nadie te pone el signo de exclamación encima. Hay que acercarse a los restos y hacer clic. Y de ahí, pistas que te llevan por varias zonas, hasta la presa de Loch Modan.',
        'Al final te espera la Bolsa de dormir acogedora: un poquito más de experiencia por cada enemigo, no se pierde al morir, y cuenta como zona de descanso.',
        'Pero lo mejor no es el premio. Es que se siente como una búsqueda de piratas de verdad: una pista, un mapa, otra zona. Como en los juegos de aventura de antes.',
    ]},
    {"id": 'c07', "frases": [
        'Número siete. Ve a la Feria de la Luna Negra.',
        'Es una feria ambulante, con carpas, juegos y gente muy rara, que va cambiando de lugar y solo se queda una semana.',
        'La primera de Forever se instaló junto a Villadorada, en el Bosque de Elwynn. Y la próxima llega el siete de diciembre a Mulgore, dos días antes de que abran las bandas.',
        'Ahí está Sayge, un adivino que te hace preguntas sobre ti. Según lo que contestes, te da un beneficio de dos horas. No hay respuesta correcta: contesta tu personaje.',
        'Nadie va a la feria a optimizar. Se va a pasear, a juntar boletos y a ver gente. Y si corres al sesenta, te la pierdes.',
    ]},
    {"id": 'c06', "frases": [
        'Número seis. Vive la guerra en el mundo.',
        'Alianza y Horda están en guerra. En los conjuntos de reglas de JcJ, eso no es un decorado: si te ve alguien del otro bando, te ataca.',
        'Y hay lugares donde esa guerra se volvió leyenda desde Classic. Como el Molino Tarren y Costasur, en las Laderas de Trabalomas, dos pueblos frente a frente.',
        'O la Vega de Tuercespina, donde las emboscadas en la Expedición de Nesingwary son tan viejas como el juego.',
        'Ahí pasan cosas que ningún campo de batalla organizado te da: un rescate improvisado, una venganza, un enemigo que te perdona la vida y te saluda.',
        'Y si juegas en un conjunto normal, también puedes sentirlo: pasa por la zona del otro bando y mira cómo viven sus pueblos. Son enemigos, pero también son vecinos.',
    ]},
    {"id": 'burla2', "frases": [
        'Y antes del top cinco, volvamos con Alberto, el de Villa del Lago.',
        'Alberto, en serio: que no puedas salir de Villa del Lago no es un fracaso. Es que el juego por fin te está tratando como en dos mil cuatro.',
        'Hay gente que se pasó una semana entera en los Montes Crestagrana, y hoy lo cuenta como su mejor recuerdo del juego.',
        'Así que quédate ahí. Pesca en el lago, haz amigos en la posada, y cuando te sientas listo, cruza el puente. El nivel treinta no se va a ir a ningún lado.',
    ]},
    {"id": 'c05', "frases": [
        'Número cinco. Participa en el chat de Los Baldíos.',
        'Los Baldíos son una zona enorme de la Horda, y su chat general es una leyenda desde dos mil cuatro.',
        'Ahí nació la pregunta más famosa de World of Warcraft: dónde está la esposa de Mankrik. La misión se llama Perdida en la batalla: un orco te pide encontrar el cuerpo de su esposa, y nadie sabía dónde estaba.',
        'Durante años, la gente preguntaba lo mismo una y otra vez. Y alrededor de esa pregunta salían bromas, discusiones y chistes que todavía se cuentan.',
        'En Forever, Los Baldíos vuelven a ser paso obligado de la Horda. Así que pregunta por la esposa de Mankrik, aunque ya sepas dónde está. Es una tradición.',
    ]},
    {"id": 'c04', "post": 4.5, "frases": [
        'Número cuatro. Pasa un rato en tu capital, sin hacer nada.',
        'Ventormenta, Forjaz, Orgrimmar, Cima del Trueno, Entrañas, Darnassus. Cada una se siente completamente distinta.',
        'En Cima del Trueno hay ascensores de los que la gente se cae todo el tiempo. En Forjaz, todo el mundo está frente al banco, presumiendo su armadura.',
        'No es tiempo perdido. Es el juego recordándote que este mundo está vivo, y que tú eres parte de él.',
        'Siéntate en la orilla del canal de Ventormenta. Mira pasar a la gente. Y escucha la música de la ciudad.',
    ]},
    {"id": 'c03', "frases": [
        'Número tres. Ayuda a alguien que va más abajo que tú.',
        'Esta te la enseñó Arnold, el abogado de Marcos: ver a alguien en problemas, e ir a ayudarlo sin que te lo pida.',
        'Un novato no puede con su misión de élite. Un mago se quedó sin maná frente a tres enemigos. Alguien pregunta cómo se llega a la mazmorra.',
        'Ve y ayúdalo. Dale unas monedas de plata, o una bolsa que te sobra. A ti no te cuesta nada, y para él es medio día de juego.',
        'Así se construye una comunidad. Hoy por ti, mañana por mí. Y en Forever, con las capas que te juntan con caras conocidas, ese novato te lo vas a volver a cruzar.',
    ]},
    {"id": 'c02', "frases": [
        'Número dos. Detente, y mira.',
        'Forever trae iluminación nueva. No cambia el arte original: lo hace ver como lo recordabas. Y si pones los gráficos en Bueno o más, se enciende la iluminación secundaria, y las noches se vuelven oscuras de verdad.',
        'Y el mundo tiene día y noche. El amanecer sobre el Bosque de Elwynn, la tormenta en los Páramos, la nieve cayendo en Dun Morogh.',
        'Así que de vez en cuando, suelta el teclado. Gira la cámara. Quita la interfaz, si quieres. Y mira el lugar donde estás.',
        'Ese mundo tiene más de veinte años, y sigue siendo de los más bonitos que se han hecho. Merece que lo mires al menos una vez.',
    ]},
    {"id": 'c01', "frases": [
        'Número uno. Tómatelo con calma.',
        'Esta es la que resume todas las demás. En Forever, el nivel máximo es sesenta, y se va a quedar en sesenta.',
        'No va a llegar una expansión que te obligue a correr para alcanzar a los demás. Lo nuevo va a crecer hacia los lados, para que puedas volver cuando quieras.',
        'Es un juego hecho para gente que tiene vida fuera del juego. Para jugar una hora en la noche, sin sentir que te estás quedando atrás.',
        'Así que no midas tus sesiones en niveles. Mídelas en recuerdos. Hoy pesqué en Villa del Lago. Hoy mi grupo mató a Hogger. Hoy me perdí en el Bosque del Ocaso.',
        'Las bandas abren el nueve de diciembre, y van a seguir ahí en enero, y en marzo, porque el nivel sesenta no se va a mover de su sitio.',
        'Pero esta primera vez, tu primer viaje por Azeroth, solo pasa una vez. Así que no lo corras, mejor vívelo.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esas son las treinta cosas para vivir la experiencia real de World of Warcraft Forever.',
        'Ninguna te va a subir de nivel más rápido. Varias te van a hacer más lento. Y casi todas te van a dejar algo que ninguna guía de nivel te da: un recuerdo.',
        'Si tú prefieres correr al sesenta, también está bien. Es tu personaje y tu tiempo. Pero el sesenta no se va a mover. El camino, en cambio, solo lo recorres una vez.',
        'Cuéntame en los comentarios cuál de estas treinta ya hiciste, y cuál vas a hacer esta semana. Todos se leen, y los mejores salen en el próximo video.',
        'Si este video te dio ganas de jugar con calma, suscríbete y compártelo con ese amigo que va corriendo al sesenta. A lo mejor le sirve para frenar.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},

]

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
