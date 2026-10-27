# -*- coding: utf-8 -*-
"""GUION — «Los 10 jugadores REALES que ROMPIERON WoW Vanilla (y qué pasará en Forever)» (Crónicas de Warcraft, 27-oct-2026).
Motor SECUENCIA YT (gameplay de YouTube por beat). Flujo y reglas: docs/estilo_secuencia_yt.md
Investigación con fuentes: videos/_investigacion_wow_jugadores.md (nada de cifras fuera de ahí).

Tema elegido por el usuario entre 3 propuestas con datos: el eje «jugadores reales» es el más fuerte del canal (Kungen ×50,
Angwe ×16,6, «12 Legendarios» ×2,54 con 53 % visto). Cuenta regresiva de 10, de lo social a lo que acabó en un tribunal.
No repite a los protagonistas de «12 Legendarios», «5 de BC», «Cuenta más vieja» ni del especial de Halloween.
Overgear campaña 2 (coaching self-play de WoW Forever) tras el n.º 8: los que estudian jefes antes que nadie también dan clases.

Voz Applio: frases de < ~200 caracteres y nunca sueltas de 1-3 palabras; todo nombre inglés en FONETICA.
"""

TITULO = "Los 10 jugadores REALES que ROMPIERON WoW Vanilla (y qué pasará en Forever)"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "Vanilla": "Vanila", "Burning Crusade": "Bérnin Kruséid", "Hyjal Summit": "Jáyal Sámit", "Hyjal": "Jáyal",
    "CRONICAS10": "Crónicas diez", "eBay": "íbei", "DKP": "de ka pe", "WoW": "uórld of uárcraft",
    # lugares
    "Barrow Deeps": "Bárou Díps", "Teldrassil": "Teldrásil", "Gilneas": "Guílneas", "Zul'Gurub": "Zul Gurúb",
    "Ahn'Qiraj": "An Kiráj", "Naxxramas": "Naksrámas", "Silithus": "Silízus", "Onyxia": "Oníxia", "qiraji": "kiráyi",
    "Les Sentinelles": "Le Santinél", "Jubei'Thos": "Yubéi Zos", "Azgalor": "Ázgalor", "Medivh": "Médiv",
    "Mannoroth": "Mánoroz", "Kel'Thuzad": "Kel Zúzad",
    # jefes
    "Lord Kazzak": "Lord Kásak", "Kazzak": "Kásak", "Highlord Kruul": "Jáilord Krul", "C'Thun": "Ce Zún",
    "Patchwerk": "Páchuerk", "Firemaw": "Fáiermo", "Vaelastrasz": "Vaelástras", "Viscidus": "Vísidus",
    "Loatheb": "Lóuzeb", "Chromaggus": "Cromágus",
    # jugadores, hermandades y cosas
    "Many Whelps! Handle It!": "méni uélps, jándel it", "She Deep Breaths More": "shi dip brezs mor",
    "Wipe Club": "Uáip Club", "Dives": "Dáivs", "Deluthor": "Delúzor", "Jokerd": "Yókerd",
    "Death and Taxes": "Dez and Táxes", "Joana": "Yoána", "Paul Lucas": "Pol Lúcas", "RIdPEF": "Ridpéf",
    "Kalahad": "Kálajad", "Ascent": "Asént", "Fury": "Fiúri", "Fortis": "Fórtis", "Overrated": "Ouverréited",
    "Patch-5.MPQ": "Pach cinco punto eme pe cu", "Karmerr": "Kármer", "Reckoning": "Rékoning", "Michael Donnelly": "Máicol Dóneli",
    "Glider": "Gláider", "Warden": "Uórden",
}

# Nombres propios que Whisper escribe distinto (Kazzak→Kazakh, Joana→Johanna, Ahn'Qiraj→Anquiraj): oídas y aceptadas (27-oct)
CER_MAX_POR_FRASE = {k: 0.15 for k in ['intro_4', 'c10_1', 'c10_4', 'c10_5', 'c10_6', 'c10_9', 'c10_11', 'c09_0', 'c09_1', 'c09_2', 'c08_0', 'c08_2', 'c08_3', 'c08_4', 'c08_7', 'c07_0', 'c07_1', 'c07_8', 'c06_0', 'c06_1', 'c06_3', 'c06_4', 'c06_8', 'c05_0', 'c05_1', 'c05_5', 'c05_8', 'c05_9', 'c04_0', 'c04_3', 'c04_7', 'c04_9', 'c03_0', 'c03_1', 'c03_2', 'c03_3', 'c03_9', 'c02_0', 'c02_3', 'c02_4', 'c02_9', 'c01_9', 'cierre_0']}
IDIOMA_LIBRE = ["c03_5"]   # p(es) 0,87 pero la transcripción es exacta

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-008": .6},   # el grito real de Dives («many whelps… now handle it», 166,5-174,6 s del video; corta antes del taco)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos se fijan tras `tiempo`
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 27-oct, 793,1 s); música ORIGINAL de WoW: `musica_wow.py` corta un tema por tramo
        (['intro', 'c10'], 'Orgrimmar'),        # 0-110 s     gancho y Onyxia
        (['c09', 'c08'], 'Forjaz'),             # 110-237 s   Jokerd y Death and Taxes
        (['overgear'], 'Forjaz'),               # 237-290 s   patrocinio (sigue el mismo tema)
        (['c07'], 'Cima del Trueno'),           # 290-350 s   Joana (respetuoso)
        (['c06'], 'Darnassus'),                 # 350-415 s   RIdPEF: Hyjal desde Teldrassil
        (['c05'], "Ahn'Qiraj"),                 # 415-482 s   el gong
        (['c04'], 'Orgrimmar'),                 # 482-555 s   la Horda arrastra a Kazzak
        (['c03'], "Ahn'Qiraj"),                 # 555-620 s   Overrated atraviesa AQ
        (['c02'], 'Forjaz'),                    # 620-685 s   Karmerr
        (['c01'], 'Entrañas'),                  # 685-762 s   Glider y el juicio
        (['cierre'], 'Orgrimmar'),              # 762-793 s
    ],
    # durante el anuncio suena la «musica promo» del canal (regla del 13-oct-2026), igualada al RMS del tramo
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En World of Warcraft hay jugadores que terminan el juego, y hay jugadores que lo rompen.",
        "Uno mató a un jefe pensado para cuarenta personas él solo, en segundos, gracias a un talento que no tenía límite.",
        "Otros arrastraron a un demonio hasta la capital de la Alianza y lo volvieron inmortal.",
        "Y uno terminó frente a un tribunal federal de Estados Unidos, con una cuenta de seis millones de dólares.",
        "Hoy te traigo a los diez jugadores reales que rompieron WoW Vanilla, del décimo al primero.",
        "Y como World of Warcraft Forever vuelve a abrir esa época, en cada uno te digo si eso podría repetirse.",
    ]},
    {"id": "c10", "frases": [
        "Número diez. Dives, el líder de banda que gritó más fuerte que un dragón.",
        "En dos mil seis, la hermandad Wipe Club entró a la guarida de Onyxia con el chat de voz grabando.",
        "La fase dos de Onyxia tiene una trampa famosa: si alguien se acerca a las cuevas, salen decenas de crías de dragón.",
        "Y, como en toda banda de Vanilla, alguien se acercó a las cuevas.",
        "Dives perdió la paciencia en directo con un grito que todavía se cita: «Many Whelps! Handle It!».",
        "Y luego la amenaza más temida de la época, la que dolía más que morir: «cincuenta DKP menos».",
        "El grupo murió entero, claro, y un jugador llamado Deluthor le puso dibujos animados a la grabación.",
        "El clip se volvió uno de los memes más famosos de la historia del juego.",
        "Ellos no rompieron el código: rompieron la paciencia de su líder, que en una banda de cuarenta es más difícil.",
        "Y Blizzard, en vez de castigarlos, los convirtió en logro: en el parche tres punto dos llegaron «Many Whelps! Handle It!» y «She Deep Breaths More».",
        "Onyxia vuelve en Forever a nivel sesenta, así que en algún servidor alguien va a volver a acercarse a esas cuevas.",
        "Y alguien más va a perder cincuenta DKP por su culpa.",
    ]},
    {"id": "c09", "frases": [
        "Número nueve. Jokerd, el mago que no pudo borrar a su propio personaje.",
        "Cuando Blizzard relanzó Vanilla como WoW Classic en dos mil diecinueve, el mundo entero corrió hacia el nivel sesenta.",
        "Jokerd, un mago gnomo, llegó primero en menos de cuatro días de tiempo jugado.",
        "Su método era la técnica de los magos de Vanilla llevada al extremo: juntar enormes grupos de monstruos, congelarlos con Nova de escarcha y barrerlos con Ventisca.",
        "Decenas de enemigos pegados a él, y ninguno alcanzándolo.",
        "Y entonces, en directo y con miles de personas mirando, anunció que iba a borrar al personaje, porque lo importante era llegar.",
        "Le dio a borrar y el juego no lo dejó: tenía correo sin leer en el buzón.",
        "El primer nivel sesenta de Classic, el más rápido del planeta, derrotado por una carta.",
        "Blizzard no tuvo que castigar nada; todo era legal, solo que absurdamente eficiente.",
        "En Forever la carrera al sesenta empieza otra vez desde cero, y los magos ya están ensayando sus rutas de grupos.",
        "Si vas a correrla, un consejo de alguien que lo vio todo: revisa el buzón antes de hacer locuras.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho. Death and Taxes, la hermandad que leía cada jefe buscando el agujero.",
        "En Vanilla los primeros del mundo no siempre ganaban por jugar mejor, sino por encontrar lo que Blizzard no había probado.",
        "Contra Firemaw, en la Guarida Alanegra, arrastraron al dragón hasta la sala de Vaelastrasz y lo atacaron desde un ángulo donde casi no los alcanzaba.",
        "Contra Viscidus, en Ahn'Qiraj, llevaron magos de escarcha con varitas y tantas cargas de zapador que el servidor se llenaba de lag, y el jefe se curaba menos de lo que debía.",
        "Contra Loatheb, que casi no deja curar, usaron sacerdotes de sombras que se curaban solos con Abrazo vampírico.",
        "Blizzard fue tapando cada truco, y en Chromaggus los maestros de juego llegaron a intervenir para prohibir un ángulo de ataque.",
        "Cada primer puesto suyo venía con una nota al pie que decía: corregido en el parche siguiente.",
        "En Forever habrá carrera por los primeros del mundo en Hyjal Summit desde el nueve de diciembre.",
        "Y las hermandades de élite ya están estudiando cada jefe antes que nadie.",
    ]},
    {"id": "overgear", "post": 2.6, "frases": [
        "Y esa gente que estudia jefes antes que nadie, curiosamente, también da clases.",
        "Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.",
        "Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado, a veces de hermandades que pelean primeros del mundo, te guía por voz.",
        "Casi nadie se atasca por ser malo, sino porque nadie le dijo qué estaba haciendo mal, y en Forever el equipo no caduca: los vicios de las primeras semanas se quedan.",
        "Tácticas de jefes, mazmorras nuevas, el plan de equipo antes de las bandas, o duelos y campos de batalla: tú eliges, y pagas solo las horas que necesites.",
        "El enlace está en la descripción, y por el lanzamiento de Forever el descuento es mayor que el habitual, solo durante un mes.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    {"id": "c07", "frases": [
        "Número siete. Joana, el hombre que llegó a sesenta mientras los demás seguían en los Baldíos.",
        "Paul Lucas jugaba con un cazador llamado Joana en el servidor Jubei'Thos.",
        "En enero de dos mil seis subió de nivel uno a sesenta en cuatro días y veinte horas de tiempo jugado, y lo grabó todo.",
        "Para que te des una idea, un jugador normal tardaba semanas, y muchos tardaban meses.",
        "Fue el primer sesenta de su servidor siete veces seguidas, y ganó el concurso oficial de Blizzard por llegar primero a nivel cincuenta.",
        "No usó ningún error del juego: rompió la idea de lo que era posible, con rutas medidas al segundo.",
        "Su récord no lo tocó nadie hasta después de Burning Crusade.",
        "Trece años más tarde, cuando volvió Classic, lo bajó todavía más: cuatro días y once horas.",
        "Joana murió en abril de dos mil veinticuatro, a los cuarenta y tres años, por un problema del corazón.",
        "Forever abre una nueva carrera al sesenta, y quien intente romper un récord va a correr contra su sombra.",
    ]},
    {"id": "c06", "frases": [
        "Número seis. La RIdPEF, los exploradores que entraron donde Blizzard no quería.",
        "Era una comunidad francesa del servidor Les Sentinelles, fundada en mayo de dos mil seis.",
        "Su deporte era cruzar paredes sin programas de trampa: saltos milimétricos por las rocas y texturas que no eran tan sólidas como parecían.",
        "Así pisaron el monte Hyjal desde Teldrassil, cuando en el mapa era una montaña de decorado.",
        "Encontraron el viejo Forjaz, el famoso aeropuerto de Forjaz, los túneles bajo Ventormenta, Gilneas detrás de su muralla y Zul'Gurub por fuera.",
        "Blizzard lo toleraba mientras nadie sacara ventaja, pero fue cerrando cada camino.",
        "Y desde un parche de Burning Crusade, entrar a una zona prohibida te teletransportaba de vuelta al mundo normal.",
        "Lo bonito es que sus capturas fueron la prueba de que esos lugares existían, años antes de que se volvieran zonas de verdad.",
        "Y en Forever pasa algo casi poético: Hyjal Summit es una de las dos primeras bandas.",
        "Lo que ellos pisaron a escondidas hace veinte años, tú lo vas a pisar con misión y con jefe.",
    ]},
    {"id": "c05", "frases": [
        "Número cinco. Kalahad, el enano que hizo sonar el gong y tumbó el servidor.",
        "Para abrir las puertas de Ahn'Qiraj, todo un servidor tenía que juntar materiales de guerra durante semanas.",
        "Y un jugador tenía que completar una cadena de misiones larguísima para conseguir el cetro que hacía sonar el gong.",
        "Medivh fue el primer servidor del mundo en lograrlo, en enero de dos mil seis.",
        "La hermandad Ascent organizó a las dos facciones, y el cetro lo usó Kalahad, un guerrero enano, líder de la hermandad Fury.",
        "Miles de jugadores se juntaron en Silithus para ver el momento.",
        "Y en el instante exacto en que sonó el gong, el servidor se cayó.",
        "No fue la única vez esa noche, aunque Blizzard había reforzado el hardware para el evento.",
        "Mientras tanto, jugadores de Mannoroth, el servidor rival, se habían creado personajes en Medivh solo para meter lag y retrasarlos.",
        "Quien completaba la cadena a tiempo se llevaba el título de Señor de los Escarabajos y el tanque qiraji negro del que ya hablamos en este canal.",
        "Si Blizzard repite un evento así en Forever para abrir alguna banda, solo pido una cosa: servidores el doble de grandes.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro. El día que Lord Kazzak se mudó a Ventormenta.",
        "Kazzak era un jefe de mundo de las Tierras Devastadas, pensado para cuarenta jugadores, con una regla muy peligrosa.",
        "Cada vez que un jugador moría cerca de él, se curaba.",
        "Jugadores de la Horda, en el servidor Kel'Thuzad se atribuye a la hermandad Fortis, lo provocaron y lo fueron arrastrando, zona tras zona, hasta la capital de la Alianza.",
        "Y Ventormenta estaba llena de lo peor que le puedes dar a Kazzak: jugadores de bajo nivel, vendedores y gente mirando la subasta.",
        "Cada uno que caía lo curaba, así que el demonio se volvió prácticamente inmortal y vació la ciudad.",
        "Hasta que apareció un maestro de juego y se lo llevó como quien saca a un perro de la cocina.",
        "Blizzard corrigió a Kazzak para que no saliera de las Tierras Devastadas, pero la idea ya se había contagiado.",
        "Antes de Burning Crusade apareció Highlord Kruul, con el mismo modelo, y los jugadores lo pasearon por todas las capitales hasta que los maestros de juego lo retiraron.",
        "Ese video, con Kazzak paseando por la capital de la Alianza, pasa del millón y medio de vistas.",
        "Forever tendrá sus propios jefes de mundo, y te aseguro que alguien ya está midiendo hasta dónde se pueden arrastrar.",
    ]},
    {"id": "c03", "frases": [
        "Número tres. Overrated, la hermandad que atravesó las paredes de Ahn'Qiraj.",
        "En noviembre de dos mil seis eran de las mejores hermandades de la Horda en Estados Unidos, y estaban avanzando en Naxxramas.",
        "El problema era que limpiar Ahn'Qiraj cada semana les quitaba horas, así que buscaron un atajo.",
        "Usaron un archivo del juego modificado, llamado Patch-5.MPQ, que les dejaba atravesar los muros de la banda y caminar directo hasta C'Thun.",
        "Según ellos mismos, lo hicieron dos o tres veces.",
        "Blizzard respondió con lo más duro que tenía: baneo permanente de toda la hermandad.",
        "Ellos mismos calcularon que las cuentas perdidas valían más de sesenta mil dólares en eBay.",
        "Y en su respuesta pública reconocieron además que habían aprovechado un error de un conjunto de guerrero contra Patchwerk, antes de que lo corrigieran.",
        "Fue la lección más clara de Vanilla: un error del juego se arregla con un parche, pero modificar el cliente se paga con la cuenta.",
        "En Forever, con bandas nuevas como Barrow Deeps y Hyjal Summit, esa advertencia ya está escrita con su nombre.",
    ]},
    {"id": "c02", "frases": [
        "Número dos. Karmerr, el paladín que mató él solo a un jefe de cuarenta personas.",
        "El talento Reckoning daba al paladín un golpe extra cada vez que un enemigo le acertaba un golpe crítico.",
        "El detalle es que esas cargas no tenían límite.",
        "En mayo de dos mil cinco, en el servidor Azgalor, Karmerr apagó su ataque automático y se quedó quieto recibiendo golpes, guardando carga tras carga.",
        "Cuando juntó mil ochocientas dieciséis, buscó a Lord Kazzak, sí, el mismo demonio de hace un momento, y lo golpeó una vez.",
        "Mil ochocientos golpes salieron de golpe, y un jefe pensado para cuarenta jugadores murió en segundos.",
        "Lo llamaron la bomba de Reckoning, y el video corrió por todos los foros.",
        "Blizzard sacó una corrección urgente el doce de mayo: desde entonces, el máximo fueron cuatro cargas.",
        "No hay constancia de que lo banearan; técnicamente usó un talento tal como estaba escrito, que en Vanilla era casi un deporte.",
        "Forever trae talentos y clases nuevos, y cualquier talento sin tope que se les escape va a tener su propio Karmerr en menos de una semana.",
    ]},
    {"id": "c01", "frases": [
        "Número uno. Michael Donnelly, el hombre que rompió World of Warcraft sin estar frente a la pantalla.",
        "En junio de dos mil cinco lanzó Glider, un programa que jugaba por ti: subía de nivel, mataba monstruos y juntaba oro solo, toda la noche.",
        "Costaba veinticinco dólares y vendió unas cien mil copias.",
        "Y el contexto era un incendio: solo en un mes de dos mil seis, Blizzard baneó cincuenta y nueve mil cuentas de granjeros de oro y sacó más de veintidós millones de oro de la economía.",
        "Blizzard demandó a Donnelly, y el juicio giró alrededor de algo concreto: Glider estaba hecho para esconderse de Warden, el antitrampas del juego.",
        "En julio de dos mil ocho se fijó una indemnización de seis millones de dólares.",
        "Y en marzo de dos mil nueve, por orden judicial, Glider se apagó para siempre.",
        "Pero lo más grande llegó en dos mil diez, cuando un tribunal de apelaciones de Estados Unidos dejó por escrito algo que todavía nos afecta a todos.",
        "El jugador no es dueño del juego: solo tiene una licencia para usarlo.",
        "Donnelly nunca pisó Ahn'Qiraj ni mató a Kazzak, pero rompió la economía, el antitrampas y, de paso, lo que creíamos que era nuestro.",
        "Forever arranca con la economía en cero y los bots van a estar ahí desde el primer minuto, así que la pregunta de dos mil cinco vuelve: ¿aguantará Warden?",
    ]},
    {"id": "cierre", "frases": [
        "Y esos son los diez jugadores reales que rompieron WoW Vanilla.",
        "Unos lo rompieron con talento, otros con paredes, otros con gritos, y uno con un abogado de por medio.",
        "Ahora cuéntame en los comentarios: ¿cuál crees que va a ser el primer escándalo de World of Warcraft Forever?",
        "Y si conoces a un jugador que rompió el juego y no salió aquí, déjalo abajo, que puede ser el próximo video.",
        "Nos vemos en la próxima crónica, y nos vemos en Azeroth.",
    ]},
]
