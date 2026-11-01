# -*- coding: utf-8 -*-
"""La historia de México en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa con RELIEVE REAL).

Canal Cronopapel, sexto video de la serie «historia en minutos» (kit v2.1 de `videos/historia_egipto/` y `videos/historia_espana/`:
una sola rejilla Mercator "mx" desde California y Texas hasta Centroamérica y el Caribe, relieve NOAA ETOPO1 bajo el guache,
ríos y lagos reales de Natural Earth, varias capas de territorio simultáneas, fractura territorial y alta densidad de bocetos).
Hilo narrativo: de la domesticación del maíz y las grandes metrópolis prehispánicas al choque de dos mundos, los tres siglos de la
Nueva España, la Independencia, las invasiones del siglo XIX, la Revolución y el México contemporáneo.

Datos y fuentes verificadas (El Colegio de México — Historia General de México, INAH, UNAM, INEGI, UNESCO, Britannica):
  - Domesticación del maíz en la cuenca del Balsas / Tehuacán: ~7000-5000 a. C. (Piperno et al., PNAS 2009; Matsuoka et al., PNAS 2002).
  - Olmecas (Preclásico, ~1200-400 a. C.): San Lorenzo (Veracruz) y La Venta (Tabasco); 17 cabezas colosales de basalto documentadas (hasta ~20-40 t).
  - Zapotecas: fundación de Monte Albán (~500 a. C.) en los Valles Centrales de Oaxaca; estelas de los Danzantes y primeros registros calendáricos.
  - Periodo Clásico (~200-900 d. C.): Teotihuacán (Calzada de los Muertos, Pirámide del Sol y de la Luna, >100 000 hab. en su apogeo, s. V-VI; UNESCO 1987);
    ciudades-estado mayas (Palenque, Calakmul, Tikal; Posclásico en Chichén Itzá y Uxmal), sistema vigesimal con el cero y escritura logosilábica.
  - Posclásico (~900-1521): Tula de los toltecas (s. X-XII); fundación tradicional de México-Tenochtitlan en el lago de Texcoco (1325);
    Triple Alianza (Tenochtitlan, Texcoco y Tlacopan, 1428) y sistema de chinampas.
  - Conquista (1519-1521): desembarco de Hernán Cortés en Veracruz (abr-1519), alianza con Tlaxcala y otros señoríos indígenas, epidemia de viruela (1520)
    y caída de México-Tenochtitlan (13-ago-1521).
  - Virreinato de la Nueva España (1535-1821): minas de plata de Zacatecas (1546) y Guanajuato; Galeón de Manila / Nao de China (1565-1815, Acapulco-Manila);
    Sor Juana Inés de la Cruz (1648/1651-1695).
  - Independencia (1810-1821): Grito de Dolores de Miguel Hidalgo (16-sep-1810); José María Morelos y el Congreso de Chilpancingo («Sentimientos de la Nación», 1813);
    resistencia de Vicente Guerrero; Plan de Iguala (24-feb-1821) con Agustín de Iturbide y entrada del Ejército Trigarante (27-sep-1821).
  - Siglo XIX: Primer Imperio (1822-1823) y Constitución Federal de 1824 (Guadalupe Victoria); separación de Texas (1836); guerra con Estados Unidos (1846-1848)
    y Tratado de Guadalupe Hidalgo (2-feb-1848, pérdida de más del 50 % del territorio).
  - Reforma y Segundo Imperio (1857-1867): Benito Juárez, Constitución de 1857 y Leyes de Reforma; Intervención francesa, Batalla de Puebla (5-may-1862, Ignacio Zaragoza),
    Segundo Imperio de Maximiliano de Habsburgo (1864-1867) y triunfo de la República Restaurada en Querétaro (1867).
  - Porfiriato (1876-1911): Porfirio Díaz, ~20 000 km de vías férreas, telégrafo, electricidad e industria petrolera; concentración agraria.
  - Revolución mexicana (1910-1920): Francisco I. Madero (Plan de San Luis, 20-nov-1910), Emiliano Zapata (Plan de Ayala, «Tierra y Libertad»),
    Francisco «Pancho» Villa (División del Norte), Venustiano Carranza y la Constitución del 5-feb-1917 en Querétaro (arts. 3.º, 27 y 123); muralismo (Diego Rivera) y Frida Kahlo.
  - Siglo XX y actualidad: expropiación petrolera de Lázaro Cárdenas (18-mar-1938); «milagro mexicano» (1940-1970); movimiento estudiantil de 1968 (2-oct, Tlatelolco)
    y Juegos Olímpicos de México 68; alternancia del año 2000; ~130 millones de habitantes (INEGI / CONAPO 2025) y 35 sitios Patrimonio Mundial de la UNESCO.
"""

TITULO = "La historia de México en 5 minutos"
ARCHIVO = "historia_mexico_5min"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural calculada por linea_tiempo
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Equivalencias fonéticas y ortográficas para el control de calidad de Whisper
ALIAS_QA = {
    "olmecas": "olmecas", "olmeca": "olmecas",
    "zapotecas": "zapotecas", "monte alban": "monte alban", "montealban": "monte alban",
    "teotihuacan": "teotihuacan", "teotihuacán": "teotihuacan", "teotiguacan": "teotihuacan",
    "yucatan": "yucatan", "palenque": "palenque", "calakmul": "calakmul", "calacmul": "calakmul",
    "chichen itza": "chichen itza", "chichen": "chichen", "itza": "itza",
    "toltecas": "toltecas", "tula": "tula",
    "nahuas": "nahuas", "naguas": "nahuas", "nahua": "nahuas",
    "mexicas": "mexicas", "mejicas": "mexicas", "mechicas": "mexicas",
    "texcoco": "texcoco", "tescoco": "texcoco",
    "tenochtitlan": "tenochtitlan", "tenochtitlán": "tenochtitlan", "tenostitlan": "tenochtitlan",
    "chinampas": "chinampas",
    "hernan cortes": "hernan cortes", "veracruz": "veracruz",
    "tlaxcaltecas": "tlaxcaltecas", "tlascaltecas": "tlaxcaltecas", "tlaxcala": "tlaxcala",
    "zacatecas": "zacatecas", "guanajuato": "guanajuato", "manila": "manila",
    "sor juana": "sor juana", "ines": "ines",
    "miguel hidalgo": "miguel hidalgo", "hidalgo": "hidalgo",
    "morelos": "morelos", "chilpancingo": "chilpancingo",
    "vicente guerrero": "vicente guerrero",
    "iturbide": "iturbide", "itúrbide": "iturbide", "iguala": "iguala",
    "texas": "texas", "tejas": "texas",
    "benito juarez": "benito juarez", "juarez": "juarez",
    "puebla": "puebla", "maximiliano": "maximiliano", "habsburgo": "habsburgo", "absburgo": "habsburgo",
    "porfirio diaz": "porfirio diaz",
    "madero": "madero", "zapata": "zapata", "pancho villa": "pancho villa",
    "venustiano carranza": "venustiano carranza", "carranza": "carranza",
    "queretaro": "queretaro", "diego rivera": "diego rivera",
    "frida kahlo": "frida kahlo", "frida kalo": "frida kahlo", "kahlo": "kahlo", "kalo": "kahlo",
    "lazaro cardenas": "lazaro cardenas",
    "tlatelolco": "tlatelolco",
}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Pirámides entre la selva, ciudades construidas sobre un lago y el choque de dos mundos que cambió el planeta.",
        "De aquí salieron el maíz, el cacao, la plata que movió el comercio mundial y una nación de ciento treinta millones de personas.",
        "Esta es la historia de México, en cinco minutos.",
    ]},
    {"id": "origenes", "frases": [
        "Todo empieza hace más de siete mil años, cuando los primeros pueblos domestican una planta sagrada: el maíz.",
        "Hacia mil doscientos antes de Cristo, en las costas del golfo florece la cultura madre de Mesoamérica: los olmecas.",
        "Tallan colosales cabezas de piedra de veinte toneladas y levantan los primeros centros ceremoniales en La Venta.",
        "Mientras tanto, en los valles de Oaxaca, los zapotecas nivelan la cima de una montaña para fundar Monte Albán y graban los primeros calendarios.",
    ]},
    {"id": "clasico", "frases": [
        "En el altiplano central surge una metrópolis monumental: Teotihuacán, la ciudad donde los hombres se convierten en dioses.",
        "Sus grandes calzadas, presididas por las pirámides del Sol y de la Luna, llegan a albergar a más de cien mil habitantes.",
        "Al mismo tiempo, en las selvas del sur y la península de Yucatán, brillan las ciudades estado de los mayas.",
        "En Palenque, Calakmul y más tarde Chichén Itzá, sus sabios calculan eclipses, inventan el uso del cero y desarrollan una escritura jeroglífica completa.",
        "Pero entre los siglos séptimo y noveno, sequías y guerras provocan el abandono de las grandes capitales clásicas.",
    ]},
    {"id": "mexicas", "frases": [
        "Tras el esplendor tolteca en Tula, nuevos pueblos de lengua náhuatl caminan desde el norte hacia el valle central.",
        "En mil trescientos veinticinco, los mexicas encuentran la señal prometida en un islote del lago de Texcoco: un águila sobre un nopal.",
        "Allí fundan México Tenochtitlan, una ciudad flotante unida por calzadas y alimentada por islas artificiales de cultivo: las chinampas.",
        "Con la Triple Alianza, el Imperio mexica extiende su dominio de costa a costa y cobra tributo a cientos de pueblos.",
    ]},
    {"id": "conquista", "frases": [
        "En mil quinientos diecinueve, Hernán Cortés desembarca en Veracruz con quinientos soldados españoles, caballos y cañones.",
        "Los pueblos rivales de los mexicas, encabezados por los guerreros tlaxcaltecas, se unen a los recién llegados para derribar al imperio.",
        "Tras meses de asedio por agua y tierra, y golpeada por una devastadora epidemia de viruela, Tenochtitlan cae en agosto de mil quinientos veintiuno.",
        "Sobre las ruinas de los templos indígenas se levanta la capital de un nuevo reino: el Virreinato de la Nueva España.",
    ]},
    {"id": "virreinato", "frases": [
        "Durante trescientos años, la Nueva España se extiende desde Centroamérica hasta las lejanas tierras de California y Texas.",
        "Las ricas minas de Zacatecas y Guanajuato producen la plata que conecta el comercio de Europa con Asia a través del Galeón de Manila.",
        "Del encuentro entre indígenas, españoles y africanos nace una sociedad mestiza con su propio arte barroco y sus tradiciones.",
        "En las letras y el pensamiento brilla Sor Juana Inés de la Cruz, la mayor poeta del Siglo de Oro en América.",
    ]},
    {"id": "independencia", "frases": [
        "Pero la desigualdad entre los nacidos en España y los criollos de América enciende la chispa de la libertad.",
        "La madrugada del dieciséis de septiembre de mil ochocientos diez, el cura Miguel Hidalgo toca la campana del pueblo de Dolores y llama a la rebelión.",
        "Tras su muerte, José María Morelos organiza las tropas del sur y proclama en Chilpancingo la soberanía y el fin de la esclavitud.",
        "En las montañas, Vicente Guerrero mantiene viva la resistencia durante años de guerra de guerrillas.",
        "Finalmente, en mil ochocientos veintiuno, Agustín de Iturbide y Guerrero sellan el Plan de Iguala y consuman la Independencia.",
    ]},
    {"id": "perdida_norte", "frases": [
        "México nace como un breve imperio con Iturbide y en mil ochocientos veinticuatro se convierte en una República federal.",
        "Pero el joven país sufre golpes militares, deudas externas y la lucha constante entre liberales y conservadores.",
        "En mil ochocientos treinta y seis, la provincia de Texas se separa, y diez años después estalla la guerra contra Estados Unidos.",
        "El ejército estadounidense ocupa la capital y, en mil ochocientos cuarenta y ocho, México pierde más de la mitad de su territorio.",
    ]},
    {"id": "reforma", "frases": [
        "En medio de la tormenta, una generación liberal encabezada por Benito Juárez promulga la Constitución de mil ochocientos cincuenta y siete y separa la Iglesia del Estado.",
        "En mil ochocientos sesenta y dos, las tropas de Francia invaden el país, pero son derrotadas el cinco de mayo en la heroica batalla de Puebla.",
        "Aun así, los franceses regresan con refuerzos e imponen un Segundo Imperio bajo el archiduque austriaco Maximiliano de Habsburgo.",
        "Juárez resiste desde el norte hasta que, en mil ochocientos sesenta y siete, las fuerzas republicanas triunfan y restauran la República.",
    ]},
    {"id": "porfiriato", "frases": [
        "En mil ochocientos setenta y seis llega al poder el general Porfirio Díaz, quien gobierna el país durante más de treinta años.",
        "Bajo el lema de orden y progreso, se tienden veinte mil kilómetros de vías férreas, llegan el telégrafo, la electricidad y el auge petrolero.",
        "Las ciudades se visten de palacios y teatros para celebrar el primer centenario de la Independencia.",
        "Pero la riqueza se concentra en grandes haciendas, mientras millones de campesinos y obreros viven sin tierras y sin derechos.",
    ]},
    {"id": "revolucion", "frases": [
        "En mil novecientos diez, Francisco Ignacio Madero convoca al pueblo a levantarse contra la dictadura: estalla la Revolución mexicana.",
        "En el sur, Emiliano Zapata lidera a los campesinos al grito de tierra y libertad; en el norte, Pancho Villa cabalga con la División del Norte.",
        "Tras años de batallas entre facciones, Venustiano Carranza reúne al Congreso en la ciudad de Querétaro.",
        "En mil novecientos diecisiete nace una nueva Constitución, pionera en el mundo por consagrar la educación gratuita, el reparto agrario y los derechos obreros.",
        "El país reconstruye su identidad entre los grandes murales de Diego Rivera y el arte inconfundible de Frida Kahlo.",
    ]},
    {"id": "siglo20", "frases": [
        "En mil novecientos treinta y ocho, el presidente Lázaro Cárdenas acelera la entrega de tierras y nacionaliza la industria del petróleo.",
        "Durante las décadas siguientes, el llamado milagro mexicano multiplica las fábricas, las carreteras, las universidades y las grandes ciudades.",
        "En mil novecientos sesenta y ocho, México celebra los primeros Juegos Olímpicos de América Latina, marcados días antes por la tragedia estudiantil de Tlatelolco.",
        "A finales del siglo veinte, la apertura económica y las reformas electorales abren paso a la alternancia pacífica en el año dos mil.",
    ]},
    {"id": "actualidad", "frases": [
        "Hoy, México es el país hispanohablante más poblado del mundo, con ciento treinta millones de habitantes y una de las mayores economías del planeta.",
        "Puente entre América del Norte y América Latina, combina una potente industria moderna con treinta y cinco sitios declarados Patrimonio de la Humanidad.",
        "Y desde las pirámides milenarias hasta el corazón de su capital, tres mil años de historia siguen vivos en cada rincón.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "La tierra donde chocaron dos mundos y donde las raíces antiguas nunca dejaron de latir.",
        "¿Qué país o imperio quieres ver en cinco minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria.py): instrumental épica e histórica inspirada en México (flauta de barro, huehuetl, teponaztli, guitarra barroca, trompetas y cuerdas cinematográficas)
LYRIA = dict(
    estilo=("Epic, vibrant and cinematic animated-history documentary score blending traditional Mexican and Mesoamerican acoustic instruments "
            "(clay ocarina flute, huehuetl and teponaztli wooden drums, baroque vihuela and Spanish guitar, warm marimba, noble brass and orchestral strings) "
            "with a fast-moving modern documentary pulse. Adventurous, dramatic, evolving across three millennia with crisp percussion transitions. "
            "Middle frequencies kept clear so a Spanish narrator can speak distinctly over it."),
    escenas={
        "gancho": ("Hook: mystical clay flute and deep huehuetl drum pulse rising into a grand orchestral swell with a bright percussive hit.", 5),
        "origenes": ("Ancient dawn of Mesoamerica: warm wooden teponaztli marimba notes, gentle jungle shakers and earthen flute melody.", 5),
        "clasico": ("Splendor of Teotihuacan and the Maya: majestic ceremonial drums, soaring flutes and noble strings with a mysterious collapse.", 6),
        "mexicas": ("Rise of Tenochtitlan: powerful Aztec war drums, shell horn calls and an imposing imperial march over the lake.", 6),
        "conquista": ("Clash of two worlds: tense Spanish snare drums and brass colliding with indigenous percussion, dramatic siege strings.", 7),
        "virreinato": ("New Spain baroque era: elegant Spanish guitar, harpsichord and warm colonial strings with maritime trade winds.", 5),
        "independencia": ("Cry for freedom: tolling church bell resonance, heroic insurgent brass fanfare and galloping cavalry rhythm.", 6),
        "perdida_norte": ("Turbulent republic and northern war: somber military snare, tense low strings and melancholic horn motif.", 6),
        "reforma": ("Liberal reform and Battle of Puebla: resolute patriotic march, clash of French and Mexican brass, triumphant republican chords.", 6),
        "porfiriato": ("Railways and belle epoque: chugging steam-train rhythm on strings and waltz-tinged orchestral elegance with dark undertones.", 5),
        "revolucion": ("Mexican Revolution: energetic acoustic guitars, bold Adelita-style trumpet fanfare and galloping northern rhythm.", 7),
        "siglo20": ("Twentieth century transformation: industrious modern orchestral pulse, solemn mid-century strings and hopeful civic theme.", 6),
        "actualidad": ("Modern Mexico: bright marimba, festive strings and confident contemporary orchestral groove.", 6),
        "cierre": ("Warm resolving outro: the main Mexican acoustic guitar and clay flute motif returns warmly, ending on a resonant final chord and fade.", 5),
    },
)
