# -*- coding: utf-8 -*-
"""GUION · Las 8 pistas que Blizzard YA dejó sobre lo que viene después de WoW Forever (Crónicas de Warcraft, SECUENCIA YT).
Flujo y reglas: docs/estilo_secuencia_yt.md · estilo «gema» (lista en cuenta regresiva, moraleja absurda al final).

Casi NADA está confirmado por Blizzard: son pistas de la beta. 27-oct-2026: adaptado a «Forever ya salió» (se publica
después del 4-nov-2026 y antes de las bandas del 9-dic, el usuario); frases con el mismo índice para no renumerar. Fuentes (13-oct-2026):
- Uncas, «Blizzard Is Already Teasing What's Coming Next» https://youtu.be/DKffbULmfkc (referencia ×6,8; Gilneas y el tiburón,
  dragones «royal guard» de Grim Batol, 6 portales, 4 portales de las Cavernas del Tiempo). Lo que SOLO dice él va atribuido.
- outputlag.com, panel de la BlizzCon 13-sep-2026: citas de Josh Greenfield (Senior Game Designer) sobre Grim Batol y el
  cráter de Azshara https://outputlag.com/news/world-of-warcraft-forever-teases-red-dragons-at-grim-batol-and-azsharas-crater/
- foreverdb.net/article/gilneas-in-the-forever-client (build 1.60.1.70009: Ruins of Gilneas, Gilneas City, Gilneas, Battle
  for Gilneas; Esfand invocado dentro el 28-sep). OJO: según esta fuente la Muralla de Cringris NO cambió (Uncas dice que sí:
  no se afirma ninguna de las dos cosas).
- mmo-champion.com/threads/2670237 (portales tapiados; Karazhan Crypts con 11 jefes y Manor Mistmantle en los archivos: un
  solo post de foro, dicho así en el guion)
- lfcarry.com/guides/wow-forever-blizzcon-2026 (hoja de ruta: bandas 9-dic; primavera y verano de 2027) y
  classicquester.com/news/forever-teased-future-content (clase nueva «not off the table»)
- Legendario (datamine, build 1.60.1.69977): Icy Veins / guided.news / Wowhead — ritual con el Círculo Cenarion, Stormwraith,
  Sylvestris Dusksong, rama de Nordrassil, 3 etapas, mapa individual «Archimonde's Fall». Arma de sanador = especulación.
Sin traducción oficial confirmada se dicen en inglés: Barrow Deeps, Riverglades, Farhold Keep, Manor Mistmantle, Stormwraith.
El segmento «overgear» es narración propia, también el código: del creativo con CRONICAS10 solo se usa la imagen
(docs/migracion_googleimagenes.md). 26-oct-2026: pasado a la campaña 2 (coaching de WoW Forever con vía bandas, 10 %
CRONICAS10 por decisión del usuario); el texto de la campaña vieja está en _respaldo_campana_vieja/.
"""

TITULO = "Las 8 pistas que Blizzard YA dejó sobre lo que viene después de WoW Forever"
ARCHIVO = "wow_pistas_futuro"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")

CADENA_VOZ = "completa"   # este video se quedó con la mezcla A (el usuario, 13-oct-2026); los siguientes de Applio usan "suave"

# Grafía para Applio: la voz base es multilingüe y con una palabra en inglés cambia de idioma; el TTS lee esto y el guion
# conserva la grafía real (.srt, Montaje, YouTube). Grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "Forever": "Foréver", "Warcraft": "uárcraft",
    "Blizzard": "Blízard", "BlizzCon": "Blízcon", "Overgear": "Óverguir", "self-play": "sélf pléi",
    "Classic": "Clásic", "Azeroth": "Azeróth", "CRONICAS10": "Crónicas diez",
    "Josh Greenfield": "Yosh Grínfild", "Greenfield": "Grínfild", "Grim Batol": "Grim Batól", "Bael Modan": "Báel Módan",
    "Riverglades": "Ríver Gléids", "Farhold Keep": "Fárjold Kip", "Barrow Deeps": "Bárrou Dips",
    "Manor Mistmantle": "Mánor Místmantel", "Karazhan": "Kárazan", "Stormwraith": "Stórm Réiz",
    "Sylvestris Dusksong": "Silvéstris Dásk Song", "Archimonde's Fall": "Árkimonds Fol", "Archimonde": "Arquimonde",
    "Hyjal": "Jiyal", "Onyxia": "Onixia", "Un'Goro": "Ungoro", "Alexstrasza": "Alextrasa", "Gilneas": "Guílneas",
    "aqir": "akir", "Esfand": "Ésfand", "Uncas": "Úncas", "coaching": "cóuchin",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # el audio del gameplay no se usa (se bajan solo imágenes)
    recorte_por={"scene-021": 0.05, "scene-057": 0.10, "scene-061": 0.08, "scene-045": 0.13},   # barras negras de origen
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),   # canales que salen con cara/overlay y ensucian el plano
)

# Whisper escribe distinto los nombres propios que Remy dice en español (Azshara, Alexstrasza, Uncas, huargen, Hyjal,
# Stormwraith...): p(es) >= 0,997 en todas. PENDIENTE de oído del usuario en Montaje (13-oct).
CER_MAX_POR_FRASE = {k: 0.06 for k in "p8_1 p7_0 p7_2 p4_7 p2_2 p2_6 p2_8 p1_11".split()}
CER_MAX_POR_FRASE.update({"p2_0": 0.10, "p3_4": 0.12, "cierre_1": 0.12})

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios en el prompt: el filtro de Lyria los rechaza
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("conspiratorial and urgent, low strings ostinato, a secret slipping out on a stage", 6),
        "p8": ("dry and bureaucratic curiosity, pizzicato strings, light woodwinds", 3),
        "p7": ("vast empty coastline, lonely horn, slow swelling strings", 4),
        "p6": ("sneaky exploration of sealed doors, plucked lute, soft hand percussion", 5),
        "overgear": ("confident and bright, heroic horns, forward motion", 5),
        "p5": ("haunted crypt and gothic manor, low choir, celesta, eerie but playful", 5),
        "p4": ("timeless desert cavern, shimmering harp, ticking percussion, wonder", 5),
        "p3": ("sacred forest ritual, flutes and choir rising, ancient tree, growing awe", 6),
        "p2": ("ominous mountain fortress, deep drums, dragon horns, building menace", 7),
        "p1": ("gothic walled kingdom revealed, full orchestra and choir, tense then triumphant", 8),
        "cierre": ("resolved and a little mischievous, warm horns fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro", "p8", "p7"], "Begin softly from near silence with a mysterious pulse. End on a sustained low string tone."),
        (["p6", "overgear", "p5"], "Begin on a sustained low string tone. End on a soft, eerie held chord."),
        (["p4", "p3"], "Begin on a soft held chord. End on a building held note, anticipation."),
        (["p2"], "Begin on a building held note. End on a tense, unresolved low drone."),
        (["p1", "cierre"], "Begin on a tense low drone. Climb to a triumphant peak, then settle and fade out to silence at the end."),
    ],
    # durante el anuncio suena la música promo del canal (copia de D:\Cronicas de Warcraft\musica promo.mp3)
    reemplazos={"overgear": dict(archivo=r"medios/_overgear/musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Trece de septiembre, en plena BlizzCon. Un diseñador de Blizzard toma el micrófono y les pide a los jugadores que vayan a morirse a propósito.",
        "Les dice que en la beta hagan una carrera de cadáveres hasta la puerta de Grim Batol, al este de Los Humedales.",
        "Y que, si llegan, tal vez noten muchos más dragones rojos de los que debería haber fuera de esa montaña.",
        "No enseñó ninguna diapositiva ni dio una fecha, y después siguió hablando como quien no ha dicho nada.",
        "World of Warcraft Forever ya salió, y Blizzard lleva semanas dejando migajas de lo que viene después.",
        "Algunas las soltó en un escenario, otras están tapiadas en mitad del mapa y otras salieron de los archivos de la beta.",
        "Estas son las ocho pistas que Blizzard ya dejó sobre el futuro de World of Warcraft Forever, de la más tímida a la más descarada.",
        "Aviso rápido: casi nada de esto está confirmado, así que trátalo como lo que es, un montón de puertas cerradas con luz por debajo.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. El calendario oficial, que es la única pista con membrete y la que menos gente leyó.",
        "El nueve de diciembre abren las primeras bandas, que son Barrow Deeps, la Cima Hyjal y la Guarida de Onyxia.",
        "Hasta ahí llega lo que todo el mundo sabe, y lo interesante viene en la letra pequeña de la hoja de ruta.",
        "Para la primavera de dos mil veintisiete promete dos bandas nuevas, dos mazmorras, una zona nueva y una cadena de misiones legendaria.",
        "Y para el verano anuncia otra banda nueva y el regreso de una banda icónica renovada.",
        "No dice cuál es esa banda icónica, y Blizzard lo dejó en blanco como si no fuéramos a pasar ocho meses discutiéndolo.",
        "Tampoco descartaron una clase nueva, porque cuando les preguntaron dijeron que la idea no está fuera de la mesa.",
        "Está en el último lugar porque aquí no hay que escarbar nada, solo hay que leer.",
        "Pero guárdate dos cosas, la zona nueva y el legendario, porque el resto de la lista intenta adivinar a qué se refieren.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. El agujero de Azshara, que Blizzard admitió en voz alta.",
        "El que habló fue Josh Greenfield, diseñador sénior del juego, el mismo del micrófono de hace un momento.",
        "Contó que Azshara recibe muchas misiones nuevas en Forever, y luego soltó la frase que importa.",
        "Dijo que quizá hay un hueco del tamaño de un cráter en el contenido de esa zona.",
        "Y remató preguntándose si tal vez, en algún momento, lo van a rellenar.",
        "Si jugaste Classic conoces ese cráter, porque está en mitad del mapa y nunca tuvo absolutamente nada adentro.",
        "Son veintidós años con un hoyo en el suelo, y ahora resulta que era un espacio reservado.",
        "Greenfield no dijo si será una mazmorra, una banda o un campo de batalla, y cada frase la envolvió en un quizá.",
        "Yo solo digo que nadie menciona un cráter vacío en un escenario por hacer conversación.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. Los portales de mazmorra que están tapiados a plena vista.",
        "Los jugadores de la beta se pasaron semanas encontrando entradas de instancia que no llevaban a ningún lado.",
        "Hay una en Los Baldíos, junto a Bael Modan, y otra en Sierra Espolón, en el Risco Cortaviento.",
        "Hay una más en las montañas del sur de Los Humedales, y otra en las Tierras Altas de Arathi que todavía nadie ubica bien.",
        "La quinta está en Farhold Keep, dentro de la zona nueva de Riverglades, y baja por debajo de la fortaleza.",
        "Y la sexta es la vieja conocida de Ventormenta, el portal sellado que lleva ahí desde el juego original.",
        "Blizzard ya había dicho que quiere mazmorras para todos los rangos de nivel, así que estas puertas son, casi seguro, las que tiene a medio construir.",
        "La teoría más repetida es que Bael Modan será algo parecido a Uldaman y que la de Sierra Espolón será de la Ventura y Compañía.",
        "Un creador llamado Uncas las fue visitando una por una, y sospecha que hay más portales escondidos que nadie ha encontrado.",
        "Es la única obra del mundo donde primero ponen la puerta y ya luego, si eso, el edificio.",
    ]},
    # El código lo dice NUESTRA voz: del creativo solo va la imagen del tramo 33,0-39,97 s, sin su audio, debajo de
    # overgear_6; el `post` estira la escena para que esos 6,97 s terminen justo en el «Número cinco».
    {"id": "overgear", "post": 2.6, "frases": [
        "Ahora, casi todo lo que viene en esta lista apunta a bandas, y las bandas no perdonan al que llega sin saber qué hacer.",
        "Forever ya salió, las bandas abren el nueve de diciembre, y para llegar preparado está Overgear, que patrocina este video con su coaching para World of Warcraft Forever.",
        "Es self-play: juegas tú con tu personaje, y un profesional verificado te explica por voz en qué fallas y por qué.",
        "Tácticas de jefes, mazmorras nuevas y qué equipo conseguir antes de la banda, y pagas solo las horas que necesites.",
        "Como en Forever el equipo no caduca, lo que corrijas en estas primeras semanas te sirve durante mucho tiempo.",
        "El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Las dos mazmorras que ya están dentro de los archivos del juego.",
        "Aquí ya no hablamos de puertas, hablamos de lo que hay detrás, porque alguien abrió los archivos de la beta.",
        "Un usuario de los foros encontró ahí una entrada para las Criptas de Karazhan, con once jefes ya listados.",
        "Si te suena es porque esa mazmorra existió en la Temporada de Descubrimiento, así que traerla de vuelta es casi un trámite.",
        "La segunda es más rara, porque se llama Manor Mistmantle y aparece como mazmorra de cinco jugadores, todavía sin jefes.",
        "Es la mansión del Bosque del Ocaso, la de la historia de Stalvan, ese tutor al que el despecho le salió carísimo a todos los demás.",
        "Once jefes para una cripta es mucha gente enterrada, incluso para los estándares de Karazhan.",
        "Ojo, que esto sale de una sola publicación en un foro, y que algo esté en los archivos no significa que llegue al juego.",
        "Pero tampoco conozco a nadie que le ponga once jefes a una mazmorra que piensa tirar a la basura.",
    ]},
    {"id": "p4", "frases": [
        "Quedan cuatro puestos, y a partir de aquí las pistas ya no son puertas sueltas, son lugares enteros.",
        "Número cuatro. Las Cavernas del Tiempo, que tienen cuatro portales y ninguno funciona.",
        "En el juego original las Cavernas eran una cueva cerrada en Tanaris, con un dragón en la puerta y nada que hacer.",
        "En la beta de Forever, algunos jugadores consiguieron colarse con un fallo y adentro encontraron cuatro portales de instancia apagados.",
        "En los foros identifican dos de ellos, que serían las Antiguas Laderas de Trabalomas y La Ciénaga Negra.",
        "De los otros dos no se sabe nada, y esos son precisamente los que importan.",
        "Porque Forever se presenta como una línea temporal alternativa, y eso le da permiso a Blizzard de contar lo que nunca nos dejó jugar.",
        "Uncas sueña con la guerra entre los trols y los aqir, o con la caída de Ventormenta del primer Warcraft.",
        "Eso ya es un deseo y no una pista, pero cuatro portales construidos y apagados sí son una pista.",
        "Blizzard dejó una mazmorra de viajes en el tiempo para más adelante, y hay que reconocer que el chiste está bien pensado.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. El legendario que Blizzard escondió y que los mineros de datos encontraron igual.",
        "La hoja de ruta solo dice cadena de misiones legendaria, primavera de dos mil veintisiete, y de ahí no pasa.",
        "Blizzard cifró las estadísticas del objeto, pero se le quedaron sueltos los textos de las misiones.",
        "Lo primero que apareció fue un ritual que se hace con ayuda del Círculo Cenarion y que deja una mejora llamada éxito del ritual legendario.",
        "Después salió una criatura, un Stormwraith, ligada a Sylvestris Dusksong, que aparece como jefe de la Cima Hyjal.",
        "Los textos hablan de cargar una rama con el poder de esa criatura, y todo apunta a que es una rama de Nordrassil.",
        "Serían tres etapas, con paradas en los túmulos de Claro de la Luna y un acertijo de pilones en el Cráter de Un'Goro.",
        "Y la última pieza es un mapa para un solo jugador que se llama Archimonde's Fall, la caída de Archimonde.",
        "O sea que el final de tu legendario podrías ser tú, sin nadie más, frente al demonio que casi se come el Árbol del Mundo.",
        "La teoría de moda es que será un arma solo para sanadores, y eso sí es pura especulación de la comunidad.",
        "Si se cumple, los sanadores van a tener por fin algo que presumir, además de la culpa cuando muere el tanque.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Grim Batol, la puerta que lleva cerrada desde dos mil cuatro.",
        "Es la fortaleza de los enanos Martillo Salvaje que acabó en manos de los orcos Faucedraco.",
        "Ahí tuvieron presa a Alexstrasza, la reina de los dragones rojos, para criar monturas de guerra con sus hijos.",
        "En el juego original llegabas a la puerta, veías un par de dragones y te ibas a tu casa, porque no había nada más.",
        "Por eso importa lo de la BlizzCon, porque Greenfield no eligió un sitio cualquiera cuando mandó a todos a morir ahí.",
        "Dijo, palabra por palabra, que habría una presencia de dragones rojos mucho mayor fuera de la montaña.",
        "Uncas hizo el viaje, cuenta que le costó más de media hora de carreras de cadáveres, y encontró la entrada llena de dragones.",
        "Según él, la mayoría lleva el título de guardia real, y un guardia real, por definición, está cuidando a alguien de la realeza.",
        "Si Alexstrasza sigue ahí adentro en esta línea temporal, la pregunta incómoda es si vamos a rescatarla o a pelear contra ella.",
        "Blizzard no ha confirmado ni mazmorra ni banda, pero es la única pista de esta lista que te pidieron ir a ver en persona.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. Gilneas, el reino que ya está construido detrás de la muralla.",
        "En el juego original, la Muralla de Cringris era una puerta gigante al sur del Bosque de Argénteos que no se abría nunca.",
        "En los archivos de la beta de Forever aparecieron tres registros de zona nuevos, que son Ruinas de Gilneas, Ciudad de Gilneas y Gilneas a secas.",
        "Ninguno tiene música ni rango de nivel, que es justo como se ve un contenido construido y todavía apagado.",
        "También hay un campo de batalla llamado Batalla por Gilneas, y su descripción habla de la muralla derrumbándose.",
        "Y no son solo nombres en una tabla, porque el veintiocho de septiembre el creador Esfand publicó un video desde adentro.",
        "Lo invocaron al otro lado y se encontró los canales, la arquitectura gótica y hasta una criatura parada en un tejado.",
        "La ciudad está ahí, con sus calles y sus edificios, esperando detrás de una puerta que oficialmente no existe.",
        "Uncas intentó llegar nadando desde Los Humedales, y cuenta que un tiburón lo mató antes de tocar la orilla.",
        "Blizzard puso un tiburón de seguridad, y eso es tener mucho que esconder.",
        "Lo que nadie sabe es para qué la quieren, si será zona para subir de nivel, una actualización grande o solo el decorado del campo de batalla.",
        "Y hay una pregunta mejor, porque en esta línea temporal la maldición huargen quizá todavía se puede detener.",
        "Blizzard no ha dicho una sola palabra sobre Gilneas, y aun así construyó la ciudad entera.",
        "Yo no levanto una ciudad con canales para usarla de fondo de pantalla.",
    ]},
    {"id": "cierre", "frases": [
        "Mi veredicto es que el mapa de Forever está lleno de puertas, y Blizzard dejó casi todas entreabiertas a propósito.",
        "Si tuviera que apostar, la zona nueva de primavera es Gilneas y el legendario pasa por la Cima Hyjal.",
        "La banda icónica del verano no me atrevo a adivinarla, y eso que llevo todo el video adivinando.",
        "Dime en los comentarios cuál crees que es, y ahora que ya puedes jugarlo, si encuentras otro portal tapiado, con más razón.",
        "Si quieres seguir escarbando, en el canal ya tienes el video de las clases y profesiones ocultas de World of Warcraft Forever.",
        "Al final, lo único que separa a Blizzard de anunciar todo esto es una diapositiva, y prefirieron poner un tiburón.",
    ]},
]
