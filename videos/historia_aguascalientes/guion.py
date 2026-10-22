# -*- coding: utf-8 -*-
"""La historia de Aguascalientes (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa con RELIEVE REAL).

Canal Cronopapel, 12 min. Kit de `videos/historia_jalisco/` (pegatinas de Flow con la referencia del kit como ingrediente,
recortadas con `nucleo/pegaflow.py`, sobre la rejilla Mercator del estado con ETOPO1 y Natural Earth 10 m).
Pedido del usuario (22-oct-2026): enfocado en la HISTORIA, con CURIOSIDADES, LUGARES QUE SE PUEDEN VISITAR para comprobarla
y, cuando haga falta, una FOTO REAL (personaje, lugar, objeto) como pegatina. Voz NUEVA del canal: ElevenLabs «Alberto
Rodríguez» (eleven_v4, corchetes de actuación, escritura normal sin fonética). SFX con `SFX_ELEVEN` (regla del 22-oct).
Datos verificados el 22-oct-2026: ver `_hechos.md` ([HECHO]/[LEYENDA]; El Ocote y el Museo Nacional de la Muerte NO se
recomiendan como visitables porque no consta que estén abiertos; los «túneles» de la capital no se afirman).
"""

TITULO = "La historia de Aguascalientes"
ARCHIVO = "historia_aguascalientes"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural calculada por linea_tiempo
BPM = 112
GAP = 0.25
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4", idioma="es",
           tomas=1, stability=0.5)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Equivalencias para el control de calidad de Whisper
ALIAS_QA = {
    "guamares": "guamares", "guachichiles": "guachichiles", "huachichiles": "guachichiles", "tecuexes": "tecuexes", "tecuanes": "tecuanes",
    "montoro": "montoro", "orozco": "orozco", "ojocaliente": "ojocaliente", "arquitos": "arquitos",
    "posada": "posada", "garbancera": "garbancera", "herran": "herran", "herrán": "herran", "guggenheim": "guggenheim",
    "soto": "soto", "gama": "gama", "eulalio": "eulalio", "calvillo": "calvillo", "inegi": "inegi",
    "rincon": "rincon", "rincón": "rincon", "gallardo": "gallardo", "tolosa": "tolosa",
}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[curious] En 1584, nueve años después de fundada, una villa del norte de la Nueva España tenía 16 soldados, un capitán… y 2 vecinos.",
        "Estuvo a punto de desaparecer. [short pause] Hoy su feria recibe 8 millones de visitantes.",
        "En su escudo hay unos labios, en uno de sus teatros Pancho Villa amenazó con balazos, y en sus calles nació la calavera más famosa de México.",
        "[short pause] Esta es la historia de Aguascalientes… y los lugares donde todavía puedes comprobarla.",
    ]},
    {"id": "origenes", "frases": [
        "Mucho antes de los españoles, estas llanuras eran tierra de cazadores y recolectores.",
        "Hacia el año 600, en el cerro de Los Tecuanes, alguien pintó figuras rojas sobre la roca: son las pinturas rupestres de El Ocote, que el INAH registró en 1985.",
        "Siglos después llegaron grupos del norte: guamares, guachichiles, zacatecos, caxcanes y tecuexes.",
        "Los mexicas y los españoles los metían a todos en una sola palabra: chichimecas. [short pause] Pero no era un pueblo, era una forma de vida: nómadas, arqueros, imposibles de someter.",
        "Y de esa época viene una leyenda que todavía se ve desde el centro de la ciudad.",
        "[whispers] Dicen que un sacerdote chichimeca, gigante, se metía en los charcos calientes para sembrar manantiales con agua y un poco de sal.",
        "Una flecha le atravesó el corazón, cayó sobre su propio pueblo, y su cuerpo se volvió montaña. El rojo del atardecer sería su sangre.",
        "Es el Cerro del Muerto. Míralo al atardecer y verás la silueta de un hombre acostado, con las manos sobre el pecho.",
    ]},
    {"id": "plata", "frases": [
        "En 1546 todo cambió: Juan de Tolosa encontró plata en Zacatecas.",
        "Para llevarla a la Ciudad de México nació el Camino Real de Tierra Adentro, la ruta de la plata.",
        "Y los chichimecas respondieron atacando las carretas. [short pause] Empezó la Guerra Chichimeca: casi 50 años de emboscadas.",
        "Los españoles levantaron presidios, pequeños fuertes, a lo largo del camino.",
        "Faltaba uno a medio camino entre Lagos y Zacatecas, junto a unos manantiales de agua caliente.",
    ]},
    {"id": "fundacion", "frases": [
        "El 22 de octubre de 1575, en Guadalajara, Jerónimo de Orozco firmó en nombre del rey Felipe II la carta de fundación.",
        "La recibió Juan de Montoro, al frente de unos 12 vecinos de Santa María de los Lagos. No venían de España: eran colonos de la frontera.",
        "El nombre era larguísimo: Villa de Nuestra Señora de la Asunción de las Aguas Calientes.",
        "[curious] Y las aguas calientes eran, literalmente, un charco: una poza termal donde la gente iba a tallarse.",
        "Un oidor la llamó la causa principal de la fundación.",
        "Pero la villa no prosperó. Con los ataques, el censo de 1584 encontró 16 soldados, un capitán y 2 vecinos.",
        "[sighs] Aguascalientes sobrevivió de milagro, y solo cuando se apagó la guerra empezó a crecer de verdad.",
    ]},
    {"id": "colonia", "frases": [
        "Al poniente de la villa nació un pueblo de indios, San Marcos. Su primer registro es una boda de 1621.",
        "En el centro se levantó la parroquia de la Asunción, terminada en 1738. Hoy es la Catedral, en la Plaza de la Patria.",
        "A su lado, una casona de la familia Rincón Gallardo, de 1665, se convirtió en el Palacio de Gobierno.",
        "[excited] Entra a su patio: los murales del chileno Osvaldo Barra cuentan toda esta historia en las paredes.",
        "Al norte, la minería hizo crecer Real de Asientos.",
        "[curious] Debajo de su parroquia, de 1705, corren túneles del siglo 18 que llevaban agua, y hoy se recorren con guía. Es Pueblo Mágico.",
        "Y en el barrio del Encino se venera un Cristo negro.",
        "[whispers] La leyenda dice que está creciendo, y que cuando toque la columna de al lado vendrá el fin del mundo.",
    ]},
    {"id": "aguas", "frases": [
        "Mientras tanto, el charco caliente seguía ahí.",
        "En 1808, el dueño de la hacienda de Ojocaliente pidió permiso al virrey para construir unos baños… y nunca le contestaron.",
        "[short pause] Estalló la guerra de Independencia.",
        "Por eso, aunque muchas guías digan 1808, los Baños de Ojocaliente abrieron en 1831.",
        "[excited] Y siguen abiertos: casi 200 años después puedes rentar una tina de agua termal en el mismo lugar que le dio nombre al estado.",
        "Los baños de Los Arquitos, de 1821, alimentados por esa misma agua, hoy son un centro cultural.",
    ]},
    {"id": "feria", "frases": [
        "En 1828, la villa estrenó algo que la haría famosa: una feria de cosechas y ganado.",
        "En 1831, el Ayuntamiento compró un terreno de 168 por 88 metros para hacer un jardín.",
        "Años después la feria se mudó al nuevo Jardín de San Marcos, con su balaustrada de cantera, y a abril, para las fiestas del santo.",
        "Hoy es la Feria Nacional de San Marcos, y en 2026 el gobierno del estado reportó cerca de 8 millones de visitantes.",
        "El jardín sigue ahí, abierto todo el año, en el corazón del antiguo pueblo de indios.",
    ]},
    {"id": "beso", "frases": [
        "En 1835, Aguascalientes dependía de Zacatecas, y Zacatecas se rebeló contra el presidente Antonio López de Santa Anna.",
        "Cuenta la leyenda que Santa Anna pasó la noche en casa de Pedro García Rojas, y que su esposa, Luisa Fernández Villa, le pidió la libertad de Aguascalientes.",
        "[whispers] Él aceptó… a cambio de un beso.",
        "El 23 de mayo de 1835, un decreto separó a Aguascalientes de Zacatecas.",
        "[curious] Y el beso quedó en el escudo del estado: desde 1946 tiene unos labios rodeados por una cadena.",
        "[short pause] Pero hay un detalle. Esa historia la escribió el ingeniero Elías L. Torres… en 1927, casi un siglo después, para un concurso literario.",
        "La separación fue, en realidad, un castigo político a Zacatecas, que había perdido la guerra.",
        "Y no duró: en 1848 volvió a anexarse, y solo con la Constitución de 1857 Aguascalientes fue estado para siempre.",
        "En 2025, el Museo Regional de Historia del INAH le dedicó al mito una exposición entera: ¿Un beso por la libertad?",
    ]},
    {"id": "posada", "frases": [
        "En 1852, en el barrio de San Marcos, nació un niño llamado José Guadalupe Posada.",
        "Aprendió a grabar en un taller de Aguascalientes, se fue a León y luego a la Ciudad de México, donde ilustró periódicos y corridos por millones.",
        "[curious] Se calcula que sus grabados superaron los 5 millones de copias: calaveras, crímenes, milagros y noticias para gente que a veces no sabía leer.",
        "[curious] Su personaje más famoso no se llamaba Catrina. Era la Calavera Garbancera, una burla de quienes negaban su origen indígena y querían parecer europeos.",
        "Décadas después, Diego Rivera la vistió de gala en un mural, y desde entonces la conocemos como la Catrina.",
        "[sighs] Posada murió pobre en 1913. Lo enterraron en una fosa sin nombre, y hoy nadie sabe dónde están sus restos.",
        "Su obra sí sabemos dónde está: en el Museo José Guadalupe Posada, junto al templo del Encino.",
    ]},
    {"id": "porfiriato", "frases": [
        "En 1884 llegó el primer tren de pasajeros, en la línea del Ferrocarril Central que unía la Ciudad de México con la frontera.",
        "Al cambio de siglo, la empresa levantó aquí sus enormes talleres, en unas 80 hectáreas, para construir y reparar locomotoras.",
        "Aguascalientes se volvió una ciudad ferrocarrilera.",
        "[excited] Esas naves hoy son el Complejo Ferrocarrilero Tres Centurias, con su museo y la estación de 1911.",
        "[curious] También llegaron los Guggenheim, con una fundición de cobre y plomo. Cerró hacia 1925 y dejó un cerro de desechos que todavía se llama el Cerro de la Grasa.",
        "En 1885 se inauguró el Teatro Morelos, y entre 1896 y 1908 se levantó el templo de San Antonio, con cúpulas que mezclan estilos de medio mundo.",
        "Neoclásico, barroco, gótico, árabe y hasta ruso, todo en el mismo templo.",
        "Lo diseñó Refugio Reyes, un arquitecto sin título. La universidad se lo dio en 1985, después de muerto.",
        "Al lado, el Museo de Aguascalientes guarda la obra de Saturnino Herrán, pintor nacido aquí en 1887.",
        "[sighs] Murió a los 31 años, sin terminar su gran tríptico, Nuestros dioses.",
    ]},
    {"id": "convencion", "frases": [
        "En 1914, la Revolución había derrocado a Victoriano Huerta, pero los ganadores no se ponían de acuerdo.",
        "Del 10 de octubre al 9 de noviembre, sus delegados se reunieron en un lugar neutral: el Teatro Morelos.",
        "El 14 de octubre se declararon Soberana Convención Revolucionaria y firmaron, uno por uno, la bandera de México.",
        "Era su forma de jurar que cumplirían lo que ahí se acordara.",
        "El 17 de octubre llegó Pancho Villa. Firmó la bandera, se abrazó con Obregón y, según un testigo, advirtió:",
        "[laughs] Ya les firmé la bandera… pero si sacan otra vez a Carranza, habrá balazos.",
        "Zapata nunca vino: mandó delegados. Y uno de ellos, Antonio Díaz Soto y Gama, tomó la bandera en la tribuna y la llamó símbolo de la reacción.",
        "[short pause] Los delegados se le echaron encima, y casi le cuesta la vida.",
        "La Convención eligió presidente a Eulalio Gutiérrez, rompió con Carranza, y México entró en otra guerra, ahora entre revolucionarios.",
        "[excited] El teatro sigue en pie, frente a la Plaza de la Patria, con un museo de la Convención.",
    ]},
    {"id": "siglo20", "frases": [
        "En 1927 empezó la Presa Calles, una de las primeras grandes obras de riego del país.",
        "Sus aguas cubrieron el viejo pueblo de San José de Gracia. Para 1930 ya estaba abandonado, y la gente tuvo que fundarlo de nuevo en otro lugar.",
        "[sighs] En años de sequía, cuando la presa baja, todavía asoman restos del pueblo viejo.",
        "En 2006, sobre una isla de la presa, se levantó el Cristo Roto: 25 metros de figura, sin un brazo y sin una pierna.",
        "[curious] Para llegar a sus pies hay que cruzar en lancha.",
        "A mediados de siglo, los viñedos llenaron el valle, y la ciudad celebró una Feria de la Uva.",
        "En Calvillo, entre huertos de guayaba, el estado cosecha casi un tercio de la guayaba de México.",
        "En 1982 llegó Nissan, y hoy de sus líneas sale un motor cada 18 segundos.",
        "[curious] Y por el terremoto de 1985, el INEGI, el instituto que cuenta a todos los mexicanos, se mudó aquí con unas 3,000 familias.",
        "Su edificio, inspirado en las pirámides, se terminó en 1989.",
        "Hoy Aguascalientes es el cuarto estado más pequeño del país: 5,616 kilómetros cuadrados, 11 municipios y más de 1.4 millones de habitantes.",
    ]},
    {"id": "ruta", "frases": [
        "Así que si vas a Aguascalientes, la historia te espera en la calle.",
        "Empieza en la Plaza de la Patria: Catedral, Palacio de Gobierno y Teatro Morelos, a unos pasos uno del otro.",
        "Sigue al Encino con Posada, a San Antonio y a San Marcos, y termina remojándote en Ojocaliente.",
        "En el camino, busca el Cerro del Muerto en el horizonte, y entra al Museo de Aguascalientes a ver a Herrán.",
        "Y si tienes un día más: los túneles de Real de Asientos, el Cristo Roto y las guayabas de Calvillo.",
        "Cuatro Pueblos Mágicos en un estado que cabe en una mañana de carretera.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "De un charco caliente y 16 soldados, a uno de los estados más pequeños de México… y con historia en cada esquina.",
        "[short pause] Y tú, ¿ya conocías la leyenda del beso? Cuéntamelo en los comentarios, y suscríbete a Cronopapel para la próxima historia.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# FOTOS REALES (pedido del usuario): pegatina de foto ~4-5 s al nombrar el personaje/lugar/objeto. Clave = "escena_i".
# Wikimedia Commons; crédito en pantalla pequeño y en la descripción (CC BY / CC BY-SA). Ver `_hechos.md` § 4.
FOTOS = {
    "origenes_1": ("Pinturas_rupestres_en_El_Ocote,_Aguascalientes_01.jpg", "Luis Alvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "origenes_7": ("Cerro_del_muerto_desde_el_centro_de_Aguascalientes_11.jpg", "Luis Alvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "colonia_1": ("Fachada_de_la_Catedral_de_Aguascalientes_01.jpg", "Foto: Luisalvaz / Wikimedia Commons / CC BY 4.0"),
    "colonia_3": ("Mural_del_Palacio_de_Gobierno_de_Aguascalientes_01.jpg", "Luisalvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "colonia_5": ("Parroquia_de_Nuestra_Señora_de_Belén_en_Real_de_Asientos,_Aguascalientes_07.jpg",
                  "Luis Alvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "aguas_4": ("Interior_de_los_antiguos_baños_de_Ojocaliente,_Aguascalientes.JPG", "Luisalvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "feria_2": ("Barandal_del_Jardín_de_San_Marcos_02.jpg", "Luis Alvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "feria_3": ("Feria_Nacional_de_San_Marcos_2025.jpg", "Cesar Martin Torres Lopez / Wikimedia Commons / CC BY 4.0"),
    "beso_0": ("Antonio_Lopez_de_Santa_Anna_c1853.png", "Meade Brothers / dominio público"),
    "posada_0": ("JOSÉ_GUADALUPE_POSADA.jpg", "Dominio público"),
    "posada_3": ("La-Calavera-Catrina-Web.jpg", "José Guadalupe Posada / dominio público"),
    "posada_6": ("Museo_Posada_y_Templo_del_Encino_2.jpg", "Luisalvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "porfiriato_3": ("Complejo_Ferrocarrilero_Tres_Centurias,_Aguascalientes_01.JPG", "Luisalvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "porfiriato_5": ("Templo_de_San_Antonio_(Aguascalientes,_Ags.)_-_cupola.jpg", "Nheyob / Wikimedia Commons / CC BY-SA 4.0"),
    "porfiriato_8": ("Autorretrato_a_los_28_años_-_1915_-_Saturnino_Herrán.jpg", "Saturnino Herrán / dominio público"),
    "porfiriato_9": ("Panel_central_de_Nuestros_dioses_(Coatlicue_transformada)_de_Saturnino_Herrán_01.jpg",
                     "Luis Alvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "convencion_1": ("Interior_del_Teatro_Morelos_en_Aguascalientes_03.jpg", "Luis Alvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "convencion_6": ("Zapatistas_at_Convention_of_Aguascalientes.jpg", "Agustín Casasola / dominio público"),
    "convencion_8": ("Pancho_Villa,_el_presidente_provisional_Eulalio_Gutiérrez_y_Emiliano_Zapata.jpg", "Dominio público"),
    "convencion_9": ("Teatro_Morelos_de_Aguascalientes_06.JPG", "Luisalvaz / Wikimedia Commons / CC BY-SA 4.0"),
    "siglo20_3": ("El_Cristo_Roto,_San_José_de_Gracias,_Aguascalientes,_Ags..jpg", "Foto: Luisalvaz / Wikimedia Commons / CC BY-SA 3.0"),
    "siglo20_6": ("Huertos_de_guayaba_en_Calvillo_01.jpg", "ProtoplasmaKid / Wikimedia Commons / CC BY 4.0"),
}

# SFX de ElevenLabs/biblioteca en vez del sintetizador (regla del 22-oct-2026). Se completan con la coreografía; luego
# `python fab.py historia_aguascalientes sfx --seco` dice cuáles siguen sintetizados y cuáles salen de la biblioteca.
SFX_ELEVEN = {
    "pop": dict(prompt="Soft paper cut-out sticker popping onto a wooden desk, light cardboard tap, dry, close", seg=0.6, variantes=4),
    "whoosh": dict(prompt="Quick soft paper whoosh, a sheet of drawing paper swept through the air, short", seg=0.8, variantes=3),
    "escribir": dict(prompt="Pencil scribbling fast on rough drawing paper, short burst", seg=1.2, variantes=3),
    "campana": dict(prompt="Single bronze church bell toll in a colonial Mexican town, warm daylight, light reverb", seg=3, bib=False),
    "galope": dict(prompt="Several horses galloping on a dry dirt road, passing by left to right", seg=4, variantes=2),
    "flecha": ("Arrow whistling through the air and thudding into wood", 1.2),
    "tren": ("Steam locomotive whistle and chugging departure, early 1900s, medium distance", 5),
    "agua_termal": ("Warm thermal spring water bubbling gently in a stone pool, soft", 4),
    "beso": ("A single soft affectionate kiss sound, close, gentle", 0.8),
    "multitud": dict(prompt="Crowded old theater hall, many men arguing and shouting angrily, 1914 assembly", seg=4, bib=False),
    "feria": ("Lively Mexican fair crowd with distant mariachi trumpets and fair rides, joyful", 5),
    "sello": dict(prompt="Heavy rubber stamp pressed on a paper document, firm thump", seg=0.7, variantes=2),
    "balazos": ("Two distant revolver gunshots, 1910s Mexican revolution, short echo", 1.5),
    "fabrica": ("Busy car factory assembly line, pneumatic tools and robotic arms whirring", 3),
    "terremoto": ("Deep earthquake rumble with rattling windows and falling debris", 2.5),
    "agua_tunel": ("Water trickling through an old stone colonial tunnel, echoing drips", 4),
    "mugido": ("Single cow moo outdoors, medium distance, rural fair", 2),
    "golpe_suave": dict(prompt="Soft muffled thud of a small cardboard cut-out landing on a table", seg=0.6, variantes=3),
    "crece": dict(prompt="Short magical rising shimmer, something growing quickly, soft paper rustle", seg=1.0, variantes=3),
    "pasos": dict(prompt="Footsteps walking on a dry dirt road, several people, short", seg=1.5, variantes=2),
    "papel": dict(prompt="Sheet of old paper being unrolled and handled, crisp rustle", seg=1.0, variantes=2),
    "tambor": dict(prompt="Indigenous wooden war drum beats, huehuetl, short tense pattern", seg=1.5, variantes=2),
    "pluck": dict(prompt="Single soft plucked guitar string note, warm, short", seg=0.7, variantes=3),
    "fanfarria": dict(prompt="Short bright brass fanfare flourish, Mexican trumpets, festive", seg=1.5, variantes=2),
    "brillo": dict(prompt="Short sparkling chime twinkle, magical glint", seg=0.8, variantes=2),
    "pincel": ("Paint brush strokes on rough paper, quick swish", 1.0),
    "crujido": ("Old wood creaking and cracking, short", 1.0),
    "clink": ("Two glass or metal objects clinking lightly", 0.6),
    "impacto": dict(prompt="Heavy dull impact thud with a little dust, cartoonish but serious", seg=0.8, variantes=2),
    "monedas": ("Pile of silver coins jingling and pouring", 1.5),
}

# Música con Lyria: antes, la BIBLIOTECA (`python fab.py biblioteca sugerir historia_aguascalientes`)
LYRIA = dict(
    estilo=("Warm, vibrant and cinematic animated-history documentary score inspired by central Mexico and the Bajío: "
            "jarana and vihuela strumming, violins and noble trumpets, clay flute and huehuetl drum for ancient times, "
            "orchestral strings and crisp percussion with a modern documentary pulse. "
            "Instrumental only, no singing. Middle frequencies kept clear so a Spanish narrator can speak distinctly over it."),
    escenas={},
    tramos=[
        (["gancho", "origenes", "plata"],
         "Begin with a curious plucked motif, move into ancient mysterious percussion and wind, end in tense frontier war drums."),
        (["fundacion", "colonia", "aguas"],
         "Begin hopeful and humble, grow into a calm colonial guitar and strings theme, end warm and bubbling."),
        (["feria", "beso"],
         "Begin with a festive fair waltz, then turn playful, romantic and a little mysterious (a legend), end on a questioning chord."),
        (["posada", "porfiriato"],
         "Begin with a bittersweet calavera-like folk dance (printmaking, Day of the Dead), then a chugging train rhythm and industrial pride, end proud and warm."),
        (["convencion"],
         "Revolutionary tension: snare drums and brass, a tense assembly, a dramatic confrontation, ending in an ominous held chord."),
        (["siglo20", "ruta", "cierre"],
         "Begin reflective and a little melancholic (a flooded town), turn modern and optimistic, end warmly with a natural fade-out."),
    ],
)
