# -*- coding: utf-8 -*-
"""La historia de Estados Unidos en 6 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa con RELIEVE REAL).

Canal Cronopapel, serie «historia en minutos» (kit v2.1 de `videos/historia_mexico/` y `videos/historia_egipto/`:
una sola rejilla Mercator "us" del Pacífico al Atlántico (Estados Unidos contiguo, con el norte de México y el sur de Canadá),
relieve NOAA ETOPO1 bajo el guache, ríos y lagos reales de Natural Earth, capas de territorio simultáneas y alta densidad de bocetos).
Hilo narrativo: de los primeros pueblos y Cahokia a las colonias, la Revolución, la expansión al oeste, la Guerra Civil, la industria,
las guerras mundiales, la Guerra Fría, los derechos civiles y el país de hoy (con el hilo hispano: San Agustín, Gálvez, 1848, 1898, hispanos hoy).

Datos (Library of Congress, National Archives, National Park Service, U.S. Census Bureau, Smithsonian, Britannica):
  - Huellas humanas de White Sands (Nuevo México), ~21 000-23 000 años (Bennett et al., Science 2021); poblamiento por Beringia y la costa del Pacífico.
  - Cahokia (cultura del Misisipi, ~1050-1350): Monks Mound, mayor obra de tierra precolombina al norte de México; ~10 000-20 000 hab. en su apogeo (UNESCO 1982).
  - Pueblos ancestrales: Chaco (~850-1150) y casas en los acantilados de Mesa Verde (~1190-1300). Confederación iroquesa (Haudenosaunee), cinco naciones.
  - San Agustín (Florida), fundada por Pedro Menéndez de Avilés el 8-sep-1565: la ciudad de origen europeo habitada sin interrupción más antigua de EE. UU. (NPS).
  - Jamestown (Virginia, 1607) y el tabaco; 1619: llegada de los primeros africanos esclavizados documentados a Virginia (Point Comfort); Mayflower y Plymouth (1620);
    trece colonias con Georgia (1732).
  - Guerra franco-india / de los Siete Años (1754-1763); Ley del Timbre (1765); Motín del té de Boston (16-dic-1773); Lexington y Concord (19-abr-1775);
    Declaración de Independencia (4-jul-1776, redactada por Thomas Jefferson); Saratoga (1777) y alianza con Francia (1778); España entra en guerra (1779)
    y Bernardo de Gálvez toma Pensacola (1781); Yorktown (oct-1781); Tratado de París (1783).
  - Constitución redactada en Filadelfia (1787), vigente en 1789; George Washington, primer presidente (30-abr-1789).
  - Compra de Luisiana a Francia (1803, 15 millones de dólares, ~2,1 millones de km², duplica el país); expedición de Lewis y Clark (1804-1806).
  - Ley de Traslado Forzoso de Indios (1830); Sendero de Lágrimas cherokee (1838-1839, ~4 000 muertos).
  - Anexión de Texas (1845); guerra con México (1846-1848) y Tratado de Guadalupe Hidalgo (1848): México cede ~55 % de su territorio.
  - Oro en Sutter's Mill (ene-1848) y fiebre del oro de California (1849, ~300 000 llegados).
  - Guerra Civil (1861-1865): Lincoln elegido (1860); 11 estados forman la Confederación; Fort Sumter (12-abr-1861); Proclamación de Emancipación (1-ene-1863);
    Gettysburg (jul-1863); rendición en Appomattox (9-abr-1865); Lincoln asesinado (14-abr-1865); 13.ª Enmienda (dic-1865) abole la esclavitud;
    ~620 000-750 000 muertos (Hacker, Civil War History 2011).
  - Primer ferrocarril transcontinental (10-may-1869, Promontory Summit, Utah); Edison y la bombilla (1879); Estatua de la Libertad (1886);
    Ellis Island (1892-1954, ~12 millones de inmigrantes); acero de Carnegie y petróleo de Rockefeller.
  - Guerra hispano-estadounidense (1898): Puerto Rico, Guam y Filipinas pasan a EE. UU.; Cuba bajo ocupación hasta 1902.
  - Hermanos Wright (Kitty Hawk, 17-dic-1903); Ford Modelo T (1908) y cadena de montaje (1913).
  - Entrada en la Primera Guerra Mundial (6-abr-1917); 19.ª Enmienda, voto femenino (1920); crac del 29 (29-oct-1929) y Gran Depresión (paro ~25 % en 1933);
    Franklin D. Roosevelt y el New Deal (1933).
  - Pearl Harbor (7-dic-1941); desembarco de Normandía (6-jun-1944); Hiroshima y Nagasaki (6 y 9-ago-1945).
  - Guerra Fría: Plan Marshall (1948), Corea (1950-1953), crisis de los misiles (oct-1962), Vietnam (1955-1975); Sputnik (1957); Apolo 11 (20-jul-1969, Neil Armstrong).
  - Derechos civiles: Rosa Parks (1-dic-1955, Montgomery); «I Have a Dream», Martin Luther King (28-ago-1963); Ley de Derechos Civiles (1964) y de Derecho al Voto (1965).
  - Fin de la URSS (dic-1991); Internet y Silicon Valley; 11-sep-2001 (~3 000 muertos); Barack Obama, primer presidente afroamericano (elegido nov-2008).
  - Hoy: ~340 millones de habitantes (Census Bureau, estimación 2024), 50 estados, mayor economía del mundo por PIB nominal (FMI);
    ~65 millones de hispanos (Census 2023, ~19 %): uno de los países con más hispanohablantes del mundo (Instituto Cervantes).
"""

TITULO = "La historia de Estados Unidos en 6 minutos"
ARCHIVO = "historia_eeuu_6min"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural calculada por linea_tiempo
BPM = 116
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Nombres en inglés leídos por Dan (Chatterbox en español): grafía solo para el TTS; el .srt y YouTube conservan la real.
FONETICA = {
    "George Washington": "Yorch Uáshington", "Washington": "Uáshington",
    "Thomas Jefferson": "Tómas Yéferson",
    "Jamestown": "Yéimstaun", "Mayflower": "Méiflauer",
    "Boston": "Bóston", "Lexington": "Léxinton", "Yorktown": "Yórktaun",
    "Lewis y Clark": "Lúis y Clark",
    "Abraham Lincoln": "Abraham Línkon", "Lincoln": "Línkon",
    "Gettysburg": "Guétisburg",
    "Edison": "Édison", "Carnegie": "Carnegui", "Rockefeller": "Rókefeler",
    "Ellis Island": "Élis Áiland",
    "Henry Ford": "Jenri Ford",
    "Franklin Roosevelt": "Fránklin Rúsvelt", "New Deal": "Niu Dil",
    "Pearl Harbor": "Perl Járbor",
    "Neil Armstrong": "Nil Ármstrong",
    "Rosa Parks": "Rosa Parks", "Martin Luther King": "Martin Lúter King",
    "Silicon Valley": "Sílicon Váli",
    "Barack Obama": "Barak Obama",
    "Cahokia": "Cajókia",
    "Wright": "Ráit", "Hollywood": "Jólibud", "rock and roll": "rocanrol",
}

# Equivalencias fonéticas y ortográficas para el control de calidad de Whisper
ALIAS_QA = {
    "cahokia": "cahokia", "cajokia": "cahokia", "kahokia": "cahokia",
    "misisipi": "misisipi", "mississippi": "misisipi",
    "mesa verde": "mesa verde", "iroqueses": "iroqueses",
    "san agustin": "san agustin", "florida": "florida",
    "jamestown": "jamestown", "jeimstaun": "jamestown", "yeimstaun": "jamestown",
    "mayflower": "mayflower", "meiflauer": "mayflower", "mayflawer": "mayflower",
    "boston": "boston", "lexington": "lexington", "lexinton": "lexington",
    "thomas jefferson": "thomas jefferson", "jefferson": "jefferson", "yeferson": "jefferson",
    "george washington": "george washington", "washington": "washington", "uashington": "washington",
    "galvez": "galvez", "bernardo de galvez": "bernardo de galvez", "pensacola": "pensacola",
    "yorktown": "yorktown", "yorktaun": "yorktown",
    "filadelfia": "filadelfia", "luisiana": "luisiana", "napoleon": "napoleon",
    "lewis": "lewis", "luis": "lewis", "clark": "clark",
    "cherokees": "cherokees", "cheroquis": "cherokees", "cheroquees": "cherokees",
    "guadalupe hidalgo": "guadalupe hidalgo", "california": "california",
    "lincoln": "lincoln", "linkon": "lincoln", "abraham lincoln": "abraham lincoln",
    "gettysburg": "gettysburg", "guetisburg": "gettysburg", "getisburg": "gettysburg",
    "edison": "edison", "carnegie": "carnegie", "carnegui": "carnegie", "rockefeller": "rockefeller", "rokefeler": "rockefeller",
    "ellis island": "ellis island", "elis ailand": "ellis island", "ellis": "ellis",
    "henry ford": "henry ford", "jenri ford": "henry ford", "ford": "ford",
    "roosevelt": "roosevelt", "rusvelt": "roosevelt", "franklin roosevelt": "franklin roosevelt",
    "new deal": "new deal", "niu dil": "new deal",
    "pearl harbor": "pearl harbor", "perl jarbor": "pearl harbor", "perl harbor": "pearl harbor",
    "normandia": "normandia", "hiroshima": "hiroshima", "nagasaki": "nagasaki",
    "neil armstrong": "neil armstrong", "nil armstrong": "neil armstrong", "armstrong": "armstrong",
    "rosa parks": "rosa parks", "martin luther king": "martin luther king", "martin luter king": "martin luther king",
    "silicon valley": "silicon valley", "silicon vali": "silicon valley",
    "barack obama": "barack obama", "barak obama": "barack obama", "obama": "obama",
    "puerto rico": "puerto rico", "filipinas": "filipinas",
    "wright": "wright", "rait": "wright", "hollywood": "hollywood", "jolibud": "hollywood",
    "rock and roll": "rock and roll", "rocanrol": "rock and roll", "plan marshall": "plan marshall",
}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Trece colonias pegadas al Atlántico que en dos siglos se convirtieron en la mayor potencia del planeta.",
        "Un país de revoluciones, guerras, inventos y sueños, donde hoy viven más de sesenta y cinco millones de hispanos.",
        "Esta es la historia de Estados Unidos, en seis minutos.",
    ]},
    {"id": "originarios", "frases": [
        "Hace más de veinte mil años, los primeros humanos dejan sus huellas en lo que hoy es Nuevo México.",
        "Junto al río Misisipi crece Cahokia, una ciudad de miles de personas coronada por una enorme pirámide de tierra.",
        "En el suroeste, los pueblos ancestrales construyen aldeas enteras dentro de los acantilados de Mesa Verde.",
        "Y al noreste, cinco naciones iroquesas se unen en una confederación gobernada por un gran consejo.",
    ]},
    {"id": "colonias", "frases": [
        "Los primeros europeos en llegar son españoles: en mil quinientos sesenta y cinco fundan San Agustín, en Florida.",
        "En mil seiscientos siete, los ingleses levantan Jamestown, en Virginia, y se enriquecen cultivando tabaco.",
        "Pocos años después llegan los primeros africanos esclavizados y, en mil seiscientos veinte, el Mayflower trae a los peregrinos.",
        "A lo largo de la costa nacen trece colonias británicas, rodeadas por los dominios de Francia y España.",
    ]},
    {"id": "revolucion", "frases": [
        "Tras vencer a Francia, Londres llena de impuestos a sus colonos, y en Boston arrojan al mar cargamentos enteros de té.",
        "En mil setecientos setenta y cinco suenan los primeros disparos en Lexington: empieza la guerra de independencia.",
        "El cuatro de julio de mil setecientos setenta y seis firman la Declaración redactada por Thomas Jefferson.",
        "George Washington dirige el ejército continental, con la ayuda de Francia y del español Bernardo de Gálvez.",
        "En mil setecientos ochenta y uno, los británicos se rinden en Yorktown, y nace un país nuevo.",
    ]},
    {"id": "republica", "frases": [
        "En Filadelfia redactan una Constitución que reparte el poder entre un presidente, un congreso y los tribunales.",
        "En mil setecientos ochenta y nueve, Washington jura como el primer presidente de la nueva república.",
        "Trece estados quedan unidos bajo una sola bandera de barras y estrellas.",
    ]},
    {"id": "oeste", "frases": [
        "En mil ochocientos tres, Napoleón vende Luisiana por quince millones de dólares, y el país duplica su tamaño.",
        "Lewis y Clark cruzan las Montañas Rocosas hasta llegar al océano Pacífico.",
        "La expansión arrasa a los pueblos nativos: miles de cherokees mueren en el Sendero de Lágrimas.",
        "Tras anexar Texas y ganar la guerra contra México, en mil ochocientos cuarenta y ocho se queda con la mitad de su territorio.",
        "Ese mismo año aparece oro en California, y miles de buscadores cruzan el continente.",
    ]},
    {"id": "civil", "frases": [
        "Pero el país está partido en dos: un norte industrial y un sur cuyas plantaciones de algodón dependen de la esclavitud.",
        "Cuando Abraham Lincoln gana la presidencia, once estados del sur se separan y forman la Confederación.",
        "En mil ochocientos sesenta y uno estalla la Guerra Civil, la más sangrienta de su historia.",
        "Lincoln proclama la libertad de los esclavos, y en Gettysburg la Unión frena el avance del sur.",
        "En mil ochocientos sesenta y cinco, el sur se rinde, Lincoln es asesinado y la esclavitud queda abolida.",
    ]},
    {"id": "industria", "frases": [
        "En mil ochocientos sesenta y nueve, el primer ferrocarril transcontinental une el Atlántico con el Pacífico.",
        "El acero de Carnegie, el petróleo de Rockefeller y la bombilla de Edison convierten al país en una fábrica gigante.",
        "Bajo la Estatua de la Libertad, doce millones de inmigrantes llegan al puerto de Nueva York en busca de una vida nueva.",
        "En mil ochocientos noventa y ocho vence a España y se queda con Puerto Rico, Guam y Filipinas.",
        "Y en mil novecientos tres, los hermanos Wright logran el primer vuelo con motor en las dunas de Carolina del Norte.",
    ]},
    {"id": "guerras", "frases": [
        "Henry Ford pone el automóvil al alcance de todos, y en mil novecientos diecisiete el país entra en la Primera Guerra Mundial.",
        "Llegan los locos años veinte, con el jazz y el voto de las mujeres, hasta que la bolsa se desploma en mil novecientos veintinueve.",
        "En la Gran Depresión, uno de cada cuatro trabajadores pierde su empleo, y Franklin Roosevelt responde con el New Deal.",
        "En mil novecientos cuarenta y uno, Japón ataca Pearl Harbor, y Estados Unidos entra en la Segunda Guerra Mundial.",
        "Sus tropas desembarcan en Normandía y la guerra termina con las bombas atómicas sobre Hiroshima y Nagasaki.",
    ]},
    {"id": "guerra_fria", "frases": [
        "Del conflicto salen dos superpotencias: Estados Unidos y la Unión Soviética, enfrentadas en la Guerra Fría.",
        "Combaten de forma indirecta en Corea y Vietnam, y en mil novecientos sesenta y dos los misiles de Cuba ponen al mundo al borde de la guerra nuclear.",
        "Con el Plan Marshall ayuda a reconstruir Europa, y su cultura, del cine de Hollywood al rock and roll, conquista el mundo.",
        "La carrera espacial culmina en mil novecientos sesenta y nueve, cuando Neil Armstrong pisa la Luna.",
    ]},
    {"id": "derechos", "frases": [
        "Mientras tanto, en el sur, Rosa Parks se niega a ceder su asiento en un autobús a un pasajero blanco.",
        "Martin Luther King encabeza la marcha sobre Washington y comparte su sueño de igualdad ante doscientas cincuenta mil personas.",
        "En mil novecientos sesenta y cuatro, la ley prohíbe la segregación, y un año después garantiza el derecho al voto.",
    ]},
    {"id": "moderno", "frases": [
        "En mil novecientos noventa y uno se derrumba la Unión Soviética, y desde Silicon Valley Internet conecta al planeta.",
        "El once de septiembre de dos mil uno, los atentados contra las Torres Gemelas abren una nueva era de guerras.",
        "Y en dos mil ocho, mientras una crisis financiera sacude al mundo, Barack Obama se convierte en el primer presidente afroamericano.",
    ]},
    {"id": "actualidad", "frases": [
        "Hoy, Estados Unidos tiene trescientos cuarenta millones de habitantes, cincuenta estados y la mayor economía del mundo.",
        "Y con sus sesenta y cinco millones de hispanos, es uno de los países donde más se habla español.",
        "De Florida a California, ciudades como San Antonio, Santa Fe o Los Ángeles recuerdan que parte de esta historia se escribió en nuestra lengua.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "La nación que nació de trece colonias y que, para bien y para mal, cambió la historia del mundo.",
        "¿Qué país o imperio quieres ver en pocos minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria.py): instrumental épica americana (fife and drum, violín folk, banjo, armónica, metales de marcha, jazz, cuerdas cinematográficas)
LYRIA = dict(
    estilo=("Epic, vibrant and cinematic animated-history documentary score of American history: colonial fife and snare drum, "
            "folk fiddle, banjo and harmonica, noble brass, orchestral strings and timpani, with a fast-moving modern documentary pulse. "
            "Adventurous and dramatic, evolving across centuries with crisp percussion transitions. "
            "Middle frequencies kept clear so a Spanish narrator can speak distinctly over it."),
    escenas={
        "gancho": ("Hook: lone snare roll and fife call rising into a grand Americana orchestral swell with a bright percussive hit.", 5),
        "originarios": ("Ancient North America: deep frame drums, wooden flute and wide open plains strings, mysterious and earthy.", 5),
        "colonias": ("Colonial era: Spanish guitar motif then English fife, harpsichord and gentle maritime strings of ships arriving.", 5),
        "revolucion": ("American Revolution: fife and drum corps march, tense snare and muskets, heroic brass fanfare of independence.", 7),
        "republica": ("Founding of the republic: noble, stately strings and solemn brass hymn, hopeful and civic.", 5),
        "oeste": ("Westward expansion: galloping banjo and fiddle, wide open frontier strings, a sorrowful turn for the Trail of Tears, then gold-rush excitement.", 6),
        "civil": ("Civil War: somber military snare, mournful solo fiddle, heavy low strings and cannon-like timpani, tragic and grand.", 8),
        "industria": ("Gilded Age industry: chugging steam-train rhythm on strings, clanking metallic percussion, optimistic immigrant theme.", 6),
        "guerras": ("Roaring twenties into war: brief jazzy brass and swing, crash into dark depression strings, then massive WWII war drums and brass.", 8),
        "guerra_fria": ("Cold War and space race: tense pulsing synth-like strings, nuclear dread, soaring triumphant moon-landing theme.", 7),
        "derechos": ("Civil rights movement: soulful gospel-tinged organ and warm strings, dignified and hopeful, building to a uplifting swell.", 6),
        "moderno": ("Modern era: sleek electronic-orchestral pulse, a sudden somber drop for 2001, then hopeful rising chords.", 6),
        "actualidad": ("Contemporary America: bright confident orchestral groove with Latin guitar touches and modern percussion.", 6),
        "cierre": ("Warm resolving outro: the main Americana fiddle and brass motif returns, ending on a resonant final chord and fade.", 5),
    },
)
