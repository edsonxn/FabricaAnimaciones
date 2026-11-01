# -*- coding: utf-8 -*-
"""La historia de Jalisco en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa con RELIEVE REAL).

Canal Cronopapel. Kit v2.1 de `videos/historia_mexico/` (una rejilla Mercator "jal": del Pacífico de Nayarit y Colima al Bajío,
relieve NOAA ETOPO1, Natural Earth 10 m: estados, Lago de Chapala, Lerma y Grande de Santiago).
NOVEDAD (22-oct-2026, pedido del usuario tras `videos/crono_flow_prueba/`): los dibujos NO se escriben por código: son PEGATINAS
de Flow pintadas con la referencia del kit como ingrediente (`flow/ref_cronopapel.jpg`) y recortadas con `nucleo/pegaflow.py`;
`pegflow.py` las mete en la hoja del boceto (borde de pegatina, sombra y temblor como los dibujos del kit).
Datos verificados el 22-oct-2026: ver `_hechos.md`.
"""

TITULO = "La historia de Jalisco en 5 minutos"
ARCHIVO = "historia_jalisco_5min"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural calculada por linea_tiempo
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Solo para el TTS (Chatterbox): la grafía real queda en pantalla y en el .srt
FONETICA = {"Mixtón": "Mistón", "Tenamaxtli": "Tenamashtli", "Xalisco": "Jalisco", "Guachimontones": "Guachimontónes",
            "wixárikas": "wirárikas", "Silicon Valley": "Sílicon Váli"}

# Equivalencias para el control de calidad de Whisper
ALIAS_QA = {
    "xalisco": "jalisco", "jalisco": "jalisco", "teuchitlan": "teuchitlan", "teuchitlán": "teuchitlan", "teuchitlan": "teuchitlan",
    "guachimontones": "guachimontones", "guachimontónes": "guachimontones",
    "cazcanes": "caxcanes", "caxcanes": "caxcanes", "tecuexes": "tecuexes", "tecuejes": "tecuexes", "wixarikas": "wixarikas",
    "wirarikas": "wixarikas", "purepechas": "purepechas", "sayula": "sayula", "zapotlan": "zapotlan",
    "nuno": "nuno", "nuño": "nuno", "guzman": "guzman", "tonala": "tonala", "galicia": "galicia",
    "nochistlan": "nochistlan", "atemajac": "atemajac", "mixton": "mixton", "miston": "mixton", "tenamaxtli": "tenamaxtli",
    "tenamashtli": "tenamaxtli", "tenamastli": "tenamaxtli", "alvarado": "alvarado", "mendoza": "mendoza",
    "cabanas": "cabanas", "cabañas": "cabanas", "cuervo": "cuervo", "hidalgo": "hidalgo", "despertador": "despertador",
    "calderon": "calderon", "calleja": "calleja", "prisciliano": "prisciliano", "juarez": "juarez", "prieto": "prieto",
    "cristeros": "cristeros", "cristiada": "cristiada", "cocula": "cocula", "analco": "analco",
}

# Tomas oídas y aceptadas (22-oct-2026): «tecuejes» y «wirárikas» son la pronunciación correcta (Whisper escribe «viráricas»);
# guadalajara_2 termina hablando («el tequila») hasta el final de la toma.
CER_MAX_POR_FRASE = {"origenes_3": 0.03}
TAIL_MAX_POR_FRASE = {"guadalajara_2": 0.40}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Tequila, mariachi y charros: buena parte de lo que el mundo imagina cuando piensa en México nació en una sola tierra.",
        "Aquí cayó un conquistador, Hidalgo decretó el fin de la esclavitud y nació el federalismo mexicano.",
        "Esta es la historia de Jalisco, en cinco minutos.",
    ]},
    {"id": "origenes", "frases": [
        "Su nombre viene del náhuatl Xalisco, que quiere decir sobre la arena.",
        "Hace más de dos mil años, junto al volcán de Tequila, la tradición Teuchitlán levantó los Guachimontones: pirámides redondas, únicas en Mesoamérica.",
        "Bajo la tierra excavaban tumbas de tiro, donde enterraban a sus muertos con figurillas de barro que hoy parecen escenas de la vida diaria.",
        "Siglos después, estas tierras eran de caxcanes, tecuexes, cocas y wixárikas, que defendieron sus salinas de los ejércitos purépechas.",
    ]},
    {"id": "conquista", "frases": [
        "En mil quinientos treinta llega Nuño de Guzmán, uno de los conquistadores más crueles, quemando pueblos y herrando esclavos.",
        "Sobre sus conquistas nace el reino de la Nueva Galicia, y en mil quinientos treinta y dos sus hombres fundan una villa llamada Guadalajara.",
        "Pero en mil quinientos cuarenta y uno los caxcanes se levantan desde el cerro del Mixtón, guiados por Tenamaxtli.",
        "El temido Pedro de Alvarado sale a aplastarlos, y muere después de que un caballo le cae encima en la retirada.",
        "Solo el virrey Mendoza, con decenas de miles de guerreros indígenas aliados, logra apagar la rebelión.",
    ]},
    {"id": "guadalajara", "frases": [
        "Después de mudarse tres veces, en mil quinientos cuarenta y dos Guadalajara se asienta para siempre en el valle de Atemajac.",
        "Se vuelve la capital del occidente: sede de un tribunal real, de una catedral y del camino hacia las minas de plata del norte.",
        "En sus haciendas se cría ganado, se doma a caballo y se destila un vino de agave que en mil setecientos noventa y cinco recibe licencia del rey: el tequila.",
        "Y en el cambio de siglo, Guadalajara estrena universidad y levanta un enorme hospicio para niños huérfanos: el Hospicio Cabañas.",
    ]},
    {"id": "independencia", "frases": [
        "En mil ochocientos diez estalla la Independencia, y el Amo Torres toma Guadalajara para los insurgentes.",
        "Miguel Hidalgo llega a la ciudad, decreta la abolición de la esclavitud y lanza el primer periódico insurgente: El Despertador Americano.",
        "Pero en enero de mil ochocientos once, en el Puente de Calderón, un ejército realista de seis mil soldados dispersa a decenas de miles de insurgentes.",
        "La guerra dura diez años más, hasta que en mil ochocientos veintiuno México es independiente.",
    ]},
    {"id": "federalismo", "frases": [
        "En mil ochocientos veintitrés, Guadalajara se adelanta a todos y proclama el Estado Libre de Jalisco.",
        "Exige que México sea una federación de estados libres, y no un gobierno centralista.",
        "Por eso a Jalisco se le llama la cuna del federalismo mexicano.",
    ]},
    {"id": "reforma", "frases": [
        "Llegan décadas de guerras entre liberales y conservadores, y en mil ochocientos cincuenta y ocho la guerra entra al palacio de gobierno.",
        "Un pelotón amotinado apunta contra el presidente Benito Juárez, y el poeta Guillermo Prieto se interpone gritando: los valientes no asesinan.",
        "Los soldados bajan las armas, y Juárez sobrevive para ganar la guerra.",
    ]},
    {"id": "porfiriato", "frases": [
        "Con la paz porfiriana, en mil ochocientos ochenta y ocho llega el ferrocarril a Guadalajara.",
        "El tequila viaja en tren a todo el país, y la ciudad se llena de fábricas, mercados y tranvías.",
    ]},
    {"id": "cristiada", "frases": [
        "En mil novecientos veintiséis, el gobierno cierra los templos y los campesinos de Los Altos se levantan en armas al grito de viva Cristo Rey.",
        "Es la Guerra Cristera: tres años de combates a caballo que dejan decenas de miles de muertos.",
        "En mil novecientos veintinueve, la Iglesia y el gobierno firman la paz, pero las heridas tardan generaciones en sanar.",
    ]},
    {"id": "siglo20", "frases": [
        "Mientras tanto, el cine de oro lleva al mundo al mariachi y al charro jalisciense, y se vuelven el símbolo de todo México.",
        "Guadalajara crece hasta ser una metrópoli de millones, sede de Mundiales de futbol en mil novecientos setenta y mil novecientos ochenta y seis.",
        "En mil novecientos noventa y dos vive su peor tragedia: la gasolina en el drenaje hace estallar las calles del barrio de Analco.",
        "Y la ciudad se reinventa con fábricas de electrónica y empresas de software, hasta ganarse el apodo de Silicon Valley mexicano.",
    ]},
    {"id": "actualidad", "frases": [
        "Hoy, Jalisco tiene más de ocho millones de habitantes: es el tercer estado más poblado del país.",
        "El mariachi, los paisajes de agave de Tequila y el Hospicio Cabañas son patrimonio de la humanidad.",
        "Y en dos mil veintiséis el Mundial volvió a Guadalajara, donde México le ganó a Corea.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "La tierra sobre la arena que le dio a México su música, su bebida y su orgullo.",
        "¿Qué estado de México quieres ver en cinco minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria: instrumental épica con instrumentos del occidente (vihuela, guitarrón, violines y trompetas de mariachi, flauta de barro)
LYRIA = dict(
    estilo=("Epic, vibrant and cinematic animated-history documentary score inspired by western Mexico and Jalisco: "
            "vihuela and guitarrón strumming, mariachi violins and noble trumpets, clay flute and huehuetl drum for ancient times, "
            "orchestral strings and crisp percussion with a fast-moving modern documentary pulse. "
            "Instrumental only, no singing. Middle frequencies kept clear so a Spanish narrator can speak distinctly over it."),
    escenas={
        "gancho": ("Hook: bright mariachi trumpet call and vihuela strum rising into a grand orchestral swell with a percussive hit.", 5),
        "origenes": ("Ancient western Mexico: clay ocarina, soft huehuetl drum, rattles and mysterious earthy marimba.", 6),
        "conquista": ("Conquest and the Mixtón war: tense Spanish snare and brass against pounding indigenous war drums, dramatic strings.", 7),
        "guadalajara": ("Colonial Guadalajara: elegant baroque guitar, harp and warm strings, a calm noble city theme.", 6),
        "independencia": ("Independence: heroic insurgent brass fanfare, galloping rhythm, then a tragic defeat chord.", 6),
        "federalismo": ("Proud civic theme: confident strings and trumpets, a resolute march of a free state.", 5),
        "reforma": ("Tension in the palace: suspenseful low strings and snare, then a noble relieved resolution.", 6),
        "porfiriato": ("Railway era: chugging steam-train rhythm on strings with a festive belle-epoque waltz touch.", 5),
        "cristiada": ("Cristero war: somber guitars, mournful trumpet solo and galloping horse rhythm, grave and sad.", 6),
        "siglo20": ("Golden age and modern city: joyful mariachi violins and trumpets, then a solemn tragic moment, then hopeful electronic pulse.", 7),
        "actualidad": ("Modern Jalisco: bright festive mariachi-orchestral groove, proud and joyful.", 6),
        "cierre": ("Warm outro: the main vihuela and trumpet motif returns softly, resolving on a resonant final chord and fade.", 5),
    },
    tramos=[
        (["gancho", "origenes", "conquista"],
         "Begin with a bright trumpet call, move into ancient mysterious percussion, end in a dramatic war climax that settles on a held chord."),
        (["guadalajara", "independencia", "federalismo", "reforma"],
         "Begin from a calm colonial guitar theme, rise to a heroic fanfare, then tension, ending on a noble resolved chord."),
        (["porfiriato", "cristiada", "siglo20", "actualidad", "cierre"],
         "Begin with a chugging train rhythm, a sad mournful middle, then joyful mariachi colors, ending warmly with a natural fade-out."),
    ],
)
