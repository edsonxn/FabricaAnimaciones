# -*- coding: utf-8 -*-
"""La historia de Irán en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa que crece, se rompe y se reúne).

Canal Cronopapel, segundo video de la serie «historia en minutos». Hilo narrativo: una cultura que sobrevive a imperios que caen
(aqueménida, parto, sasánida…) porque conserva su lengua y su identidad; mismo motor que `videos/historia_china/`.

Datos y fuentes (Britannica, Cambridge History of Iran, Encyclopaedia Iranica, UNESCO):
  - Susa, capital de Elam: tablillas con escritura proto-elamita desde ~3000 a. C. Qanats: túneles subterráneos de riego, más de 3000 años (UNESCO).
  - Medos: con los babilonios destruyen Nínive, capital asiria, en 612 a. C.
  - Ciro II el Grande derrota a los medos (550 a. C.), conquista Lidia (546) y Babilonia (539); Cilindro de Ciro (Museo Británico): respeto a las
    religiones y regreso de los pueblos cautivos; la ONU distribuyó una réplica y muchos lo llaman «primera declaración de derechos humanos» (debate).
  - Darío I (522-486 a. C.): imperio de Egipto al Indo, unas veinte satrapías, dárico de oro, Camino Real de ~2500 km (Sardes-Susa), mensajeros
    a caballo en ~7 días (Heródoto); Persépolis (desde ~518 a. C., UNESCO). Guerras médicas: Maratón 490, Salamina 480.
  - Alejandro Magno derrota a Darío III (331 Gaugamela) y su ejército incendia Persépolis (330 a. C.); muere en 323 a. C.
  - Partos (247 a. C.-224 d. C.): «flecha parta»; derrota de Craso en Carras (53 a. C.).
  - Sasánidas (224-651): Shapur I captura al emperador Valeriano (260); zoroastrismo como religión de Estado; el ajedrez llega de la India (chaturanga) y
    pasa por Persia al mundo. Guerra bizantino-sasánida 602-628. Yazdgerd III muere en 651.
  - Edad de oro islámica con sabios persas: Avicena (Canon de la Medicina, texto en universidades europeas siglos), Al Juarismi (de Corasmia; «algoritmo»),
    Omar Jayam; Ferdousí termina el Shahnameh (~1010, unos 50 000 pareados) en persa.
  - Mongoles: invasión 1219-1221; Hulagu, nieto de Gengis Kan, toma Bagdad (1258). Tamerlán, campañas 1380-1405. Los conquistadores se persianizan.
  - Safávidas: Ismail I se proclama sha en 1501 (tenía 14 años); chiismo como religión oficial; Abás I traslada la capital a Isfahán (~1598),
    «Isfahán es la mitad del mundo».
  - Nader Sha saquea Delhi y se lleva el Trono del Pavo Real (1739). Qayares: pérdidas ante Rusia (Gulistán 1813, Turkmanchay 1828);
    Revolución Constitucional 1906; petróleo en Masyed Soleimán (mayo de 1908, Anglo-Persian Oil Company).
  - Reza Sha (1925, dinastía Pahlavi); en 1935 pide usar «Irán» en el extranjero; nacionalización del petróleo (1951); golpe de 1953 (la CIA lo
    reconoció en 2013); Revolución de 1979; guerra Irán-Irak 1980-1988. Población actual ~89-90 millones. Nowruz (Año Nuevo persa): más de 3000 años, UNESCO.
"""

TITULO = "La historia de Irán en 5 minutos"
ARCHIVO = "historia_iran_5min"
ESTILO_VISUAL = "boceto"
DURACION = 300
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)
# Whisper escribe a su manera los nombres persas que Dan pronuncia bien: equivalencias para el control de calidad
ALIAS_QA = {"khayyam": "jayam", "jayyam": "jayam", "khomeini": "jomeini", "jomeini": "jomeini", "ferdowsi": "ferdousi", "firdusi": "ferdousi",
            "abbas": "abas", "shah": "sha", "genghis": "gengis", "khan": "kan", "isfahan": "isfahan", "qajar": "qayar", "kayar": "qayar",
            "shapur": "shapur", "tamerlan": "tamerlan", "timur": "tamerlan",
            "caras": "carras", "cargas": "carras", "callares": "qayares", "nowruz": "nouruz", "nobruz": "nouruz", "nuruz": "nouruz", "nogruz": "nouruz"}
SUBTITULOS = False            # los subtítulos manuscritos los dibuja la propia escena
MUSICA = {}                   # la música es de Lyria (nucleo/lyria.py), no la procedural

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Hace dos mil quinientos años, un solo imperio gobernaba desde Egipto hasta la India.",
        "Cayó, renació muchas veces, y su cultura jamás desapareció.",
        "Esta es la historia de Irán, en cinco minutos.",
    ]},
    {"id": "meseta", "frases": [
        "Todo empieza en una meseta rodeada de montañas y desiertos.",
        "En Susa, los elamitas ya escriben en tablillas de arcilla, hace cinco mil años.",
        "Para vivir en el desierto, inventan los qanats: túneles subterráneos que llevan el agua desde las montañas.",
        "Mil años antes de Cristo, llegan tribus de pastores y jinetes: los medos y los persas.",
        "Los medos se unen, y junto a Babilonia destruyen al poderoso imperio asirio.",
    ]},
    {"id": "ciro", "frases": [
        "Pero los persas esconden un secreto: un joven llamado Ciro.",
        "En quinientos cincuenta antes de Cristo, derrota a los medos y funda el Imperio aqueménida.",
        "Conquista Lidia, y después la gran Babilonia.",
        "Pero no destruye la ciudad: respeta a sus dioses, y deja volver a casa a los pueblos cautivos.",
        "Su cilindro de arcilla es llamado por muchos la primera declaración de derechos humanos.",
    ]},
    {"id": "dario", "frases": [
        "Con Darío el Grande, el imperio llega desde Egipto hasta el río Indo.",
        "Lo divide en provincias, cobra impuestos en monedas de oro, y abre un Camino Real de dos mil quinientos kilómetros.",
        "Mensajeros a caballo, de posta en posta, lo cruzan en una semana.",
        "Y en Persépolis levanta una capital de columnas gigantes, donde todos los pueblos llegan con regalos.",
        "Darío y su hijo Jerjes atacan Grecia, pero las guerras médicas terminan en derrota.",
    ]},
    {"id": "alejandro", "frases": [
        "Hasta que, en trescientos treinta antes de Cristo, llega un joven macedonio: Alejandro Magno.",
        "Derrota al último rey, y su ejército incendia Persépolis.",
        "Alejandro muere a los treinta y dos años, y su imperio se reparte.",
    ]},
    {"id": "partos", "frases": [
        "Siglos después, llegan los partos, unos jinetes arqueros.",
        "Fingen huir, y disparan hacia atrás: la famosa flecha parta.",
        "Con ella, aplastan a un ejército romano en Carras.",
        "Durante casi cinco siglos, Partia y Roma se reparten medio mundo.",
    ]},
    {"id": "sasanidas", "frases": [
        "En doscientos veinticuatro, nace el segundo gran imperio persa: los sasánidas.",
        "Su rey Shapur captura al emperador romano Valeriano, algo que jamás había ocurrido.",
        "Su religión es el zoroastrismo: el bien y el mal en combate eterno, con el fuego como símbolo sagrado.",
        "Y de la India reciben un juego de estrategia, que perfeccionan y llevan al mundo: el ajedrez.",
        "Pero tras siglos de guerras contra Bizancio, el imperio queda agotado.",
    ]},
    {"id": "islam", "frases": [
        "Entonces llegan ejércitos desde Arabia.",
        "En seiscientos cincuenta y uno muere el último rey sasánida, y llega el islam.",
        "Pero Persia no desaparece: conserva su lengua y su identidad.",
        "Sus sabios brillan en la edad de oro del mundo islámico: Avicena escribe un manual de medicina que se estudia en Europa durante siglos.",
        "Al Juarismi da nombre a los algoritmos, y Ferdousí salva el idioma con un poema épico de cincuenta mil versos.",
    ]},
    {"id": "mongoles", "frases": [
        "Pero en mil doscientos diecinueve, cruza la frontera una tormenta: los mongoles de Gengis Kan.",
        "Arrasan ciudades enteras, y su nieto conquista hasta Bagdad.",
        "Un siglo después, llega Tamerlán, otro conquistador que deja montañas de ruinas.",
        "Pero los invasores acaban hablando persa, y adoptando su cultura.",
    ]},
    {"id": "safavidas", "frases": [
        "En mil quinientos uno, un adolescente de catorce años se proclama sha: Ismail, el primer safávida.",
        "Impone una nueva rama del islam como religión oficial, y vuelve a unir Irán.",
        "Con el sha Abás, la capital Isfahán se llena de mezquitas de azulejos azules, jardines y bazares.",
        "Dicen que Isfahán es la mitad del mundo, y sus alfombras se venden hasta Europa.",
    ]},
    {"id": "qayar", "frases": [
        "Después, el guerrero Nader conquista Delhi, y se lleva el Trono del Pavo Real.",
        "Pero sus sucesores, los qayares, pierden terreno ante Rusia y el Imperio británico.",
        "En mil novecientos seis, una revolución obliga al sha a aceptar una constitución y un parlamento.",
        "Y en mil novecientos ocho, brota petróleo en el desierto.",
    ]},
    {"id": "pahlavi", "frases": [
        "El petróleo lo cambia todo, y las potencias extranjeras se disputan el país.",
        "En mil novecientos veinticinco, un oficial del ejército se corona sha, y funda la dinastía Pahlavi.",
        "En mil novecientos treinta y cinco, pide al mundo que deje de llamar al país Persia, y use su nombre propio: Irán.",
        "En mil novecientos cincuenta y uno, el gobierno nacionaliza el petróleo.",
        "Dos años después, un golpe apoyado por Estados Unidos y Reino Unido lo derriba.",
    ]},
    {"id": "moderna", "frases": [
        "Pero el descontento crece, y en mil novecientos setenta y nueve, una revolución derroca a la monarquía.",
        "Se proclama la República Islámica, dirigida por el ayatolá Jomeini.",
        "Poco después estalla una guerra de ocho años contra Irak, con cientos de miles de muertos.",
        "Hoy viven en Irán casi noventa millones de personas.",
        "Y cada primavera celebran Nouruz, el Año Nuevo persa, una fiesta de más de tres mil años.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Cayeron imperios, cambiaron reyes y religiones, y la cultura persa siguió viva.",
        "¿Qué país quieres ver en cinco minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)


# Música con Lyria (nucleo/lyria.py): estilo persa moderno y juguetón, con hueco para la voz; un bloque por escena
LYRIA = dict(
    estilo=("Playful yet epic animated-history documentary score blending traditional Persian instruments (santur, tar, setar, ney flute, "
            "daf and tombak drums) with a light modern pulse, in the feel of a fast-moving illustrated history explainer. Bright, rhythmic, "
            "constantly evolving, with short stingers at scene changes. Modal melodies kept low so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: plucked tar motif over a light ticking pulse, curiosity building, a cheeky rise and a bright hit at the end.", 5),
        "meseta": ("Dawn on a high plateau: ney flute and soft santur arpeggios, warm desert pulse, water drops, then daf drums and gathering riders.", 4),
        "ciro": ("Rise of a great king: tombak and daf, rising confident strings, a triumphant lift, then a gentle serene passage for mercy.", 6),
        "dario": ("Majestic empire: grand regal santur and strings, galloping rhythm for couriers, monumental drums for the palace, a sad fall at the end.", 6),
        "alejandro": ("Dramatic conquest: pounding war drums, a sudden crackling fire, then a mournful pause and a sad descending melody.", 6),
        "partos": ("Horse archers: fast galloping daf, bowed strings, a sly playful feint, a sudden shot and a big triumphant hit.", 6),
        "sasanidas": ("Sasanian grandeur then decline: stately tar and strings, an eternal struggle section with low drums, a playful chess motif, a tired slow ending.", 6),
        "islam": ("Turning point and golden age: a low rumble then wonder and discovery with santur, oud and ney, curious and elegant, growing warm.", 6),
        "mongoles": ("Storm of horsemen: thundering drums, urgent strings, dark power chords, then an eerie quiet and a slowly brightening ending.", 6),
        "safavidas": ("Splendid blue-tiled city: sparkling santur and tar, graceful dance rhythm, bazaar bustle, bright and proud.", 6),
        "qayar": ("Shifting fortunes: a bold brass-like entrance, a tense slow decline, a hopeful parliament motif, then a deep gush of oil and a dark groove.", 6),
        "pahlavi": ("Modernizing tension: jazzy modern groove with Persian color, scheming low strings, a solemn drop and a dramatic pause.", 6),
        "moderna": ("Upheaval and renewal: rising crowd energy, a heavy march, a solemn pause, then a warm spring-like Nowruz celebration with bells and daf.", 7),
        "cierre": ("Playful resolving outro: modal theme returns brightly, light percussion, friendly and inviting, a final warm chord and fade.", 5),
    },
)
