# -*- coding: utf-8 -*-
"""La historia de Egipto en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa del Nilo).

Canal Cronopapel, cuarto video de la serie «historia en minutos» (mismo motor que `historia_china`, `historia_iran` y `historia_japon`).
Hilo narrativo: el río que dio vida a una civilización eterna; imperios que florecen, reyes que se declaran dioses, invasiones extranjeras
y una identidad que perdura a través de cinco mil años.

Datos y fuentes verificadas (Britannica, Cambridge Ancient History, UNESCO, Museo Británico, Museo Egipcio de El Cairo):
  - Época predinástica y unificación: Narmer (Menes) unifica el Alto y Bajo Egipto (~3100 a. C.); paleta de Narmer (Museo de El Cairo).
  - Reino Antiguo (dinastías III-VI, ~2686-2181 a. C.): Djoser y la pirámide escalonada de Saqqara (arquitecto Imhotep);
    pirámides de Guiza (Keops, Kefrén, Micerino, c. 2550 a. C.) y Gran Esfinge (UNESCO, 1979). Keops: ~146.6 m original, estructura más alta por 3.800 años.
  - Reino Medio (~2055-1650 a. C.): reunificación tebana (Mentuhotep II); florecimiento literario y templos de Karnak. Invasión de los hicsos (carros de guerra).
  - Reino Nuevo (~1550-1069 a. C.): expulsión de los hicsos (Ahmose I); imperio militar hasta el Éufrates y Nubia; Hatshepsut faraón (expedición a Punt);
    Tutmosis III (17 campañas militares); revolución monoteísta de Akenatón y Nefertiti (Amarna, Atón); Tutankamón (tumba KV62 de Howard Carter, 1922);
    Ramsés II el Grande (batalla de Kadesh, 1274 a. C., primer tratado de paz paritario; templos de Abu Simbel, reinado de 66 años).
  - Periodo Tardío y conquista persa: Pueblos del Mar, dinastías nubias (XXV), conquista asiria y conquista persa por Cambises II (525 a. C.).
  - Periodo Helenístico y Romano: Alejandro Magno funda Alejandría (331 a. C.); Faro (una de las 7 maravillas) y Biblioteca;
    dinastía ptolemaica (Ptolomeo I a Cleopatra VII); batalla de Accio (31 a. C.), muerte de Cleopatra (30 a. C.) y provincia romana («granero de Roma»).
  - Conquista islámica (641 d. C., Amr ibn al-As); fundación de El Cairo (969 d. C., fatimíes); Saladino (fundador de la dinastía ayubí, Ciudadela de El Cairo);
    sultanato mameluco vence a los mongoles (batalla de Ain Yalut, 1260). Dominio otomano (1517).
  - Era moderna: expedición de Napoleón (1798) y hallazgo de la Piedra de Rosetta (descifrada por Champollion, 1822); Mehmet Alí (modernización, ~1805-1848);
    Canal de Suez inaugurado en 1869 (Ferdinand de Lesseps, 164 km); protectorado británico (1882); independencia (1922); República (Nasser, 1952);
    Presa de Asuán (1960-1970); población actual ~105 millones de habitantes.
"""

TITULO = "La historia de Egipto en 5 minutos"
ARCHIVO = "historia_egipto_5min"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural calculada por linea_tiempo
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Equivalencias fonéticas y ortográficas para el control de calidad de Whisper
ALIAS_QA = {
    "narmer": "narmer", "menes": "menes", "imhotep": "imhotep", "djoser": "zoser", "zoser": "zoser",
    "keops": "keops", "kheops": "keops", "kefren": "kefren", "micerino": "micerino",
    "saqqara": "saqqara", "sakara": "saqqara", "guiza": "guiza", "giza": "guiza",
    "esfinge": "esfinge", "tebas": "tebas", "karnak": "karnak",
    "hicsos": "hicsos", "ixos": "hicsos", "ixsos": "hicsos",
    "memphis": "menfis",
    "hatshepsut": "hatshepsut", "tutmosis": "tutmosis", "thutmose": "tutmosis",
    "akenaton": "akenaton", "akhenaten": "akenaton", "nefertiti": "nefertiti",
    "aton": "aton", "tutankamon": "tutankamon", "tutankhamun": "tutankamon",
    "ramses": "ramses", "ramses ii": "ramses segundo", "kadesh": "kadesh", "qadesh": "kadesh",
    "abu simbel": "abu simbel", "alejandro magno": "alejandro magno", "alejandria": "alejandria",
    "ptolomeo": "ptolomeo", "cleopatra": "cleopatra", "cleopatra septimo": "cleopatra septima",
    "accio": "accio", "actium": "accio",
    "saladino": "saladino", "mamelucos": "mamelucos", "ain yalut": "ain yalut",
    "rosetta": "rosetta", "champollion": "champollion", "mehmet ali": "mehmet ali",
    "suez": "suez", "asuan": "asuan", "aswan": "asuan", "nasser": "nasser"
}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
TRANSICIONES = [("continua", 0.1)] * 14
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Un río en medio del desierto donde nació una de las civilizaciones más fascinantes de la Tierra.",
        "Construyeron monumentos que desafiaron al tiempo, y reyes que se proclamaron dioses vivientes.",
        "Esta es la historia de Egipto, en cinco minutos.",
    ]},
    {"id": "origenes", "frases": [
        "Todo empieza en una estrecha franja verde rodeada de arena, fertilizada cada año por las crecidas del Nilo.",
        "Hacia tres mil cien antes de Cristo, el rey Narmer unifica el Alto y el Bajo Egipto con la primera corona doble.",
        "Nace la primera de más de treinta dinastías, con su gran capital en Menfis.",
        "Los sacerdotes inventan los jeroglíficos para registrar las cosechas, los templos y los nombres eternos de sus faraones.",
    ]},
    {"id": "piramides", "frases": [
        "Comienza el Reino Antiguo, la edad dorada de las pirámides.",
        "El sabio Imhotep diseña la primera pirámide escalonada en Saqqara como una escalera hacia el cielo.",
        "Siglos después, en la meseta de Guiza, miles de trabajadores levantan la Gran Pirámide para el faraón Keops.",
        "A su lado, la Gran Esfinge vigila el desierto con cuerpo de león y rostro de rey.",
        "Durante casi cuatro mil años, será la estructura más alta construida por el ser humano.",
    ]},
    {"id": "intermedio1", "frases": [
        "Pero sequías severas y disputas entre gobernadores hunden al país en el caos.",
        "Los príncipes de Tebas logran reunificar las tierras e inician el Reino Medio.",
        "Florecen la literatura, el arte y los templos monumentales en Karnak.",
        "Sin embargo, desde Asia llegan invasores con carros de guerra veloces: los hicsos, que conquistan el Delta.",
    ]},
    {"id": "reino_nuevo", "frases": [
        "Los egipcios adoptan los caballos y los carros de guerra para expulsar a los invasores, y fundan el poderoso Reino Nuevo.",
        "Egipto se transforma en un imperio militar conquistador que llega hasta el río Éufrates.",
        "La reina Hatshepsut asume el poder supremo como faraón, enviando legendarias expediciones comerciales por el mar Rojo.",
        "Y su sucesor, Tutmosis Tercero, expande las fronteras del imperio como el mayor estratega de su época.",
    ]},
    {"id": "revolucion", "frases": [
        "Hacia mil trescientos cincuenta antes de Cristo, un faraón rebelde conmociona al imperio: Akenatón.",
        "Prohíbe todos los dioses tradicionales e impone un único culto al sol: Atón.",
        "Funda una nueva capital en el desierto junto a su reina, Nefertiti, y transforma el arte por completo.",
        "Pero a su muerte, los sacerdotes restauran las viejas tradiciones y borran su nombre de los templos.",
        "Su joven hijo, Tutankamón, restablece el culto tradicional y es sepultado con un tesoro deslumbrante de oro macizo.",
    ]},
    {"id": "ramses", "frases": [
        "Poco después sube al trono el faraón más célebre de todos: Ramsés Segundo.",
        "En mil doscientos setenta y cuatro antes de Cristo, combate contra el Imperio hitita en la gigantesca batalla de carros de Kadesh.",
        "Tras la batalla, firma el primer tratado de paz documentado de la historia humana.",
        "Ramsés llena Egipto de colosos y templos excavados en la roca viva, como el imponente Abu Simbel, y reina durante sesenta y seis años.",
    ]},
    {"id": "decadencia", "frases": [
        "Con los siglos, el poder faraónico se fragmenta.",
        "Egipto sufre invasiones de los pueblos del mar, faraones nubios y los guerreros asirios.",
        "En quinientos veinticinco antes de Cristo, los ejércitos persas conquistan las tierras del Nilo y lo reducen a una provincia.",
        "Las dinastías de reyes nativos se apagan para siempre.",
    ]},
    {"id": "alejandro", "frases": [
        "Hasta que, en trescientos treinta y dos antes de Cristo, entra victorioso Alejandro Magno.",
        "Los sacerdotes lo coronan hijo del dios Amón, y funda en la costa mediterránea la gran metrópolis de Alejandría.",
        "Allí se alzan el legendario Faro, maravilla del mundo, y la Biblioteca más sabia de la antigüedad.",
        "A su muerte, su general Ptolomeo funda una nueva dinastía de reyes griegos que adoptan la corona de los faraones.",
    ]},
    {"id": "cleopatra", "frases": [
        "La última soberana de esta dinastía es la astuta y culta Cleopatra Séptima.",
        "Aliada primero con Julio César y luego con Marco Antonio, intenta salvar la independencia de su reino.",
        "Pero en la batalla naval de Accio, las legiones de Octavio vencen.",
        "Cleopatra elige la muerte antes que el cautiverio, y Egipto se convierte en la joya y el granero del Imperio romano.",
    ]},
    {"id": "islam", "frases": [
        "Siglos más tarde, en el año seiscientos cuarenta y uno, llega la conquista árabe trayendo una nueva fe y una nueva lengua.",
        "Nace la ciudad de El Cairo, corazón brillante del comercio y la cultura medieval.",
        "El célebre sultán Saladino levanta su inexpugnable Ciudadela y protege la región durante las Cruzadas.",
        "Tiempo después, los bravos guerreros mamelucos gobiernan y logran detener la arrolladora invasión de los mongoles.",
    ]},
    {"id": "modernidad", "frases": [
        "En mil setecientos noventa y ocho, Napoleón desembarca con sus tropas, y sus científicos hallan la milagrosa Piedra de Rosetta.",
        "Gracias a ella, los sabios logran descifrar por fin los jeroglíficos tras mil años de silencio.",
        "El gobernante Mehmet Alí moderniza las instituciones y la agricultura, sentando las bases del Egipto contemporáneo.",
        "Y en mil ochocientos sesenta y nueve, se inaugura el Canal de Suez, uniendo el mar Mediterráneo con el océano Índico y transformando las rutas del planeta.",
    ]},
    {"id": "siglo20", "frases": [
        "Tras décadas de protectorado británico, Egipto proclama su independencia y, en mil novecientos cincuenta y dos, la República.",
        "El país nacionaliza el Canal de Suez y construye la majestuosa Presa de Asuán, domesticando para siempre las crecidas del Nilo.",
        "Hoy, más de ciento cinco millones de personas viven en una nación puente entre África y Oriente Medio.",
        "Y las pirámides siguen contemplando el desierto, erguidas tras cinco mil años de historia.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "La tierra de los faraones que vio nacer la civilización y que nunca dejó de reinventarse a orillas de su río sagrado.",
        "¿Qué país o imperio quieres ver en cinco minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria.py): estilo egipcio épico, misterioso y rítmico (ney flute, oud, qanun, darbuka y percusión orquestal)
LYRIA = dict(
    estilo=("Epic, mystical and rhythmic animated-history documentary score blending ancient Egyptian acoustic instruments "
            "(ney flute, oud, qanun, sistrum, darbuka and framed drums) with a cinematic modern pulse, in the feel of a fast-moving "
            "illustrated history explainer. Majestic, adventurous, constantly evolving, with short brass-and-percussion stingers at scene changes. "
            "Middle frequencies kept calm so a Spanish narrator can speak clearly over it."),
    escenas={
        "gancho": ("Hook: mysterious ney flute motif over deep resonant drums, a rising dramatic swell and a bright gong hit at the end.", 5),
        "origenes": ("The sacred Nile at dawn: soft harp arpeggios, gentle desert breeze, flowing water pulse, building to a stately drumbeat.", 5),
        "piramides": ("Monumental golden age: grand stone-raising rhythm, deep brass, majestic choir pads, triumphant rising chord.", 6),
        "intermedio1": ("Turmoil and invasion: sudden dissonant strings, fast galloping war-chariot drums, tense shifting winds.", 5),
        "reino_nuevo": ("Imperial expansion: triumphant martial march, confident horns and rattling sistrum, heroic royal flourish.", 6),
        "revolucion": ("Sun revolution: exotic mystical ney and shimmering qanun under burning sun rays, dramatic pause, golden mask theme.", 5),
        "ramses": ("The Great Pharaoh: thundering chariot battle drums, clashing rhythms, then an imposing regal anthem for Abu Simbel.", 7),
        "decadencia": ("Fading empire: mournful solitary flute, crumbling stone textures, distant war drums, solemn quiet ending.", 5),
        "alejandro": ("Hellenistic glory: Mediterranean maritime strings meeting Egyptian oud, bright curious fanfare for Alexandria.", 6),
        "cleopatra": ("Tragic queen: seductive regal melody on flute and strings, gathering dark storm of Roman horns, sorrowful dramatic fall.", 6),
        "islam": ("Medieval Islamic golden age: bustling bazaar rhythms, lively darbuka, stately citadel fortress theme, triumphant clash against invaders.", 6),
        "modernidad": ("Discovery and transformation: ticking clockwork pulse, awakening theme for Rosetta Stone decipherment, grand maritime ships horn for Suez Canal.", 6),
        "siglo20": ("Modern awakening: powerful modern orchestral groove, massive water-surge brass for the Aswan Dam, proud desert horizon.", 7),
        "cierre": ("Warm resolving outro: the main Nile theme returns brightly, friendly acoustic oud and light percussion, inviting final warm chord and fade.", 5),
    },
)
