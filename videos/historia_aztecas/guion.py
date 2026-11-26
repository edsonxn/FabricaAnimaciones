# -*- coding: utf-8 -*-
"""Toda la historia de los AZTECAS (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa con RELIEVE REAL).

Canal Cronopapel, ~16 min. Primera prueba del formato LARGO «historia COMPLETA» (análisis del 23-nov-2026 en
`canales/formula/cronopapel.md`): tema enorme contado de principio a fin, tono de amigo con burla ligera y un PERSONAJE FIJO
del canal, Xolo (xoloitzcuintle), con un chiste que se repite. Kit de `videos/historia_aguascalientes/` (pegatinas de Flow,
fotos reales con FotoPeg, mapa con relieve: Valle de México con los lagos de 1519 + centro de México).
Voz ElevenLabs «Alberto Rodríguez» (eleven_v4_turbo, corchetes de actuación sin susurros ni excitado). Datos: `_hechos.md`.
"""

TITULO = "Toda la historia de los AZTECAS"
ARCHIVO = "historia_aztecas"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural calculada por linea_tiempo
BPM = 112
GAP = 0.25
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es",
           tomas=1, stability=0.5)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Equivalencias para el control de calidad de Whisper
ALIAS_QA = {
    "aztlan": "aztlan", "aztlán": "aztlan", "mexicas": "mexicas", "huitzilopochtli": "huitzilopochtli",
    "coatepec": "coatepec", "coatlicue": "coatlicue", "coyolxauhqui": "coyolxauhqui", "chapultepec": "chapultepec",
    "culhuacan": "culhuacan", "culhuacán": "culhuacan", "tizapan": "tizapan", "tizapán": "tizapan", "huitzilihuitl": "huitzilihuitl",
    "huitzilíhuitl": "huitzilihuitl", "tenochtitlan": "tenochtitlan", "tlatelolco": "tlatelolco", "azcapotzalco": "azcapotzalco",
    "tezozomoc": "tezozomoc", "tezozómoc": "tezozomoc", "acamapichtli": "acamapichtli", "itzcoatl": "itzcoatl", "itzcóatl": "itzcoatl",
    "nezahualcoyotl": "nezahualcoyotl", "nezahualcóyotl": "nezahualcoyotl", "tlacopan": "tlacopan", "tlacaelel": "tlacaelel",
    "tlacaélel": "tlacaelel", "ilhuicamina": "ilhuicamina", "axayacatl": "axayacatl", "axayácatl": "axayacatl",
    "moquihuix": "moquihuix", "moquíhuix": "moquihuix", "ahuizotl": "ahuizotl", "ahuízotl": "ahuizotl", "xocoyotzin": "xocoyotzin",
    "tlaloc": "tlaloc", "tláloc": "tlaloc", "tzompantli": "tzompantli", "malintzin": "malintzin", "cempoala": "cempoala",
    "toxcatl": "toxcatl", "tóxcatl": "toxcatl", "cuitlahuac": "cuitlahuac", "cuitláhuac": "cuitlahuac", "cuauhtemoc": "cuauhtemoc",
    "cuauhtémoc": "cuauhtemoc", "xoloitzcuintle": "xoloitzcuintle", "mictlan": "mictlan", "mictlán": "mictlan", "xolo": "xolo",
    "chinampas": "chinampas", "telpochcalli": "telpochcalli", "calmecac": "calmecac", "calmécac": "calmecac", "macehuales": "macehuales",
    "pipiltin": "pipiltin", "tlatoani": "tlatoani", "ahuejotes": "ahuejotes", "toci": "toci", "maxtla": "maxtla",
    "purepechas": "purepechas", "purépechas": "purepechas", "teotihuacan": "teotihuacan", "xochimilco": "xochimilco",
    "iztapalapa": "iztapalapa", "ahuehuete": "ahuehuete", "ahuizote": "ahuizote",
}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[curious] El 8 de noviembre de 1519, unos cuatrocientos soldados españoles avanzaban por una calzada en medio de un lago… y no podían creer lo que veían.",
        "Una ciudad sobre el agua, con templos blancos, canales llenos de canoas y más gente que casi cualquier ciudad de Europa.",
        "Uno de ellos escribió que parecía cosa de encantamiento, como en los libros de caballerías.",
        "[short pause] Dos siglos antes, ahí no había nada. Solo un islote lleno de juncos… y una tribu que nadie quería de vecina.",
        "Esta es la historia completa de los aztecas: de una peregrinación sin rumbo al imperio más poderoso de Mesoamérica… y su caída en apenas dos años.",
        "Y nos va a acompañar alguien que estuvo ahí todo el tiempo. [short pause] Él es Xolo.",
        "[laughs] Un xoloitzcuintle: sin pelo, muy leal… y, como vas a ver, siempre a un paso de terminar en el menú.",
    ]},
    {"id": "aztlan", "frases": [
        "Primero, un detalle: los aztecas nunca se llamaron a sí mismos aztecas.",
        "Ese nombre viene de Aztlán, su tierra de origen, y se puso de moda siglos después. Ellos se llamaban mexicas.",
        "Su historia empieza cuando salen de Aztlán, un lugar rodeado de agua en algún punto del norte, allá por el siglo doce.",
        "¿Dónde estaba Aztlán? Nadie lo sabe. Hay quien lo pone en Nayarit, en el Bajío o en Estados Unidos… y quien dice que nunca existió.",
        "Los guiaba su dios, Huitzilopochtli, el colibrí del sur: dios del sol y de la guerra, cargado en un bulto por sus sacerdotes.",
        "Y él les prometió una tierra. La reconocerían cuando vieran un águila parada sobre un nopal.",
        "Así empezó una caminata de casi dos siglos.",
        "En el camino, en el cerro de Coatepec, cuenta el mito que Huitzilopochtli nació ya armado para defender a su madre, Coatlicue.",
        "Su hermana, Coyolxauhqui, venía a matarla con sus cuatrocientos hermanos. Él la venció, la despedazó y la arrojó cerro abajo.",
        "[short pause] Guarda ese nombre, Coyolxauhqui. Vamos a volver a encontrarla… en 1978, debajo de una calle de la Ciudad de México.",
        "Pasaron también por Tula, la gran ciudad de los toltecas, que para los mexicas era la cuna de todo lo civilizado.",
    ]},
    {"id": "chapultepec", "frases": [
        "A finales del siglo trece llegaron por fin al Valle de México. Y no estaba vacío.",
        "Alrededor de unos grandes lagos vivían ciudades ricas y antiguas: Azcapotzalco, Culhuacán, Texcoco, Xochimilco.",
        "Los mexicas se instalaron en el cerro de Chapultepec, el cerro del chapulín, donde brotaba agua dulce.",
        "Pero eran pobres, peleoneros y con costumbres que espantaban a los vecinos. [short pause] Así que los vecinos se juntaron y los echaron.",
        "Su jefe, Huitzilíhuitl el viejo, terminó prisionero y sacrificado en Culhuacán.",
        "Los sobrevivientes pidieron asilo al señor de Culhuacán, y él les dio una tierra: Tizapán.",
        "[curious] Un pedregal lleno de víboras de cascabel. La idea era que se murieran.",
        "Y cuenta la historia que, cuando mandó a ver cómo iban, los encontró muy contentos. [short pause] Se habían comido a las víboras.",
        "[laughs] Xolo, por esta vez, se salvó: había víboras de sobra en el menú.",
        "Los mexicas pelearon como mercenarios para Culhuacán, y le pidieron al señor una hija para casarla con su dios.",
        "Según la leyenda, él aceptó, orgulloso. Pero cuando llegó a la fiesta, encontró a un sacerdote vestido con la piel de su hija.",
        "[sighs] Para los mexicas era un honor: la princesa se volvía diosa, Toci, nuestra abuela. Para su padre, no tanto.",
        "Los persiguieron hasta el lago, y los mexicas huyeron entre los juncos, a unos islotes que nadie quería.",
    ]},
    {"id": "fundacion", "frases": [
        "Y ahí, según la tradición, en 1325, vieron la señal: un águila sobre un nopal que crecía en una piedra.",
        "[curious] Pero ojo: en los dibujos más antiguos, el águila no se come una serpiente. Se come un pájaro, o simplemente está parada.",
        "La serpiente llegó después, y es la que hoy está en la bandera de México.",
        "Llamaron a su ciudad México-Tenochtitlan, el lugar de la tuna de piedra.",
        "Era un islote pantanoso: sin piedra, sin madera y sin buena tierra. Todo lo demás lo iban a conseguir con trueque… o a la mala.",
        "Unos años después, un grupo se peleó y fundó su propia ciudad en el islote de al lado: Tlatelolco.",
    ]},
    {"id": "chinampas", "frases": [
        "Para no morirse de hambre, los mexicas hicieron algo genial: chinampas.",
        "Clavaban estacas en el fondo del lago, tejían cercas de carrizo, las rellenaban con lodo y plantas, y sembraban encima.",
        "En las orillas plantaban ahuejotes, árboles altos y delgados cuyas raíces amarraban la tierra.",
        "Eran islas de cultivo que daban varias cosechas al año, de maíz, de frijol, de calabaza y de chile.",
        "[curious] Y todavía existen. En Xochimilco te subes a una trajinera y paseas entre chinampas que son Patrimonio de la Humanidad.",
        "Pero la ciudad seguía siendo vasalla. El dueño del valle era Azcapotzalco, de los tepanecas, y su rey Tezozómoc, un viejo muy astuto.",
        "Los mexicas le pagaban tributo y peleaban sus guerras. [short pause] Y mientras, aprendían.",
        "Hacia 1376 tuvieron su primer tlatoani, que significa el que habla: Acamapichtli, con sangre noble de Culhuacán.",
        "Xolo, mientras tanto, consiguió su primer trabajo serio: cuidar los patos de la chinampa.",
    ]},
    {"id": "alianza", "frases": [
        "En 1426 murió Tezozómoc, y su hijo Maxtla quiso apretar a todos.",
        "Los mexicas, con su tlatoani Itzcóatl, se aliaron con un príncipe que vivía huyendo: Nezahualcóyotl, el heredero de Texcoco.",
        "Cuenta la leyenda que, siendo un muchacho, vio desde un árbol cómo los tepanecas mataban a su padre.",
        "En 1428, mexicas, texcocanos y la ciudad de Tlacopan derrotaron a Azcapotzalco.",
        "Así nació la Triple Alianza: tres ciudades que se repartirían el tributo de medio México… aunque la que mandaba, cada vez más, era Tenochtitlan.",
        "[curious] Y entonces, cuentan, Itzcóatl hizo algo muy moderno: mandó quemar los libros antiguos.",
        "En los viejos códices, los mexicas eran unos don nadie. En la historia nueva, eran el pueblo elegido del sol.",
        "Detrás de esa idea estaba un consejero que sirvió a varios tlatoanis: Tlacaélel.",
        "Nezahualcóyotl, por su parte, se volvió rey de Texcoco, constructor y poeta. [short pause] Es el que salía en los billetes de cien pesos.",
    ]},
    {"id": "moctezuma1", "frases": [
        "En 1440 llegó Moctezuma Ilhuicamina, el que flecha el cielo. Moctezuma primero.",
        "Con él, los ejércitos mexicas salieron del valle: hacia Morelos, Guerrero, Oaxaca y la costa del Golfo.",
        "Pero a mediados de siglo llegaron las heladas y la sequía, y con ellas años de hambruna.",
        "[sighs] Hubo familias que vendieron a sus propios hijos en la costa a cambio de maíz.",
        "Xolo pasó esos años escondido debajo de un petate. Y con razón.",
        "Moctezuma llevó agua dulce de Chapultepec a la isla con un acueducto.",
        "Y con Nezahualcóyotl levantó un dique enorme en el lago para separar el agua dulce de la salada.",
        "En esos años nació algo muy raro: la guerra florida.",
        "Batallas pactadas con Tlaxcala y sus vecinos. No para conquistar, sino para capturar prisioneros vivos… para el sacrificio.",
        "Tlaxcala nunca fue conquistada. [short pause] Y nunca lo olvidó.",
    ]},
    {"id": "vida", "frases": [
        "Vamos a pausar las guerras. ¿Cómo era vivir en Tenochtitlan?",
        "La mayoría eran macehuales, gente común: campesinos, pescadores, artesanos. Arriba de ellos, los pipiltin, los nobles.",
        "Los niños iban a la escuela. La gente común al telpochcalli, a aprender a ser guerreros; los nobles al calmécac, a estudiar con los sacerdotes.",
        "[curious] Y la disciplina era seria: en un códice hay un padre que castiga a su hijo poniéndolo sobre el humo de chiles quemados.",
        "Para comprar no había monedas. Se usaban mantas de algodón… y granos de cacao.",
        "Y sí, había falsificadores: vaciaban el cacao y lo rellenaban de tierra.",
        "Todo se movía en el mercado de Tlatelolco. Cortés le contó al rey que cada día iban más de sesenta mil personas a comprar y vender.",
        "Había oro, plumas, jade, hierbas medicinales, guajolotes… [short pause] y perritos. Sí, perritos que la gente compraba para comérselos.",
        "[laughs] Xolo, aquí, procuraba no hacer contacto visual con nadie.",
    ]},
    {"id": "tributo", "frases": [
        "Y desde todo el imperio llegaba el tributo, anotado pueblo por pueblo en dibujos.",
        "Mantas, maíz, trajes de guerrero, plumas de quetzal, pieles de jaguar.",
        "Unas provincias mandaban cacao; otras, oro en polvo; otras, pelotas de hule.",
        "A cambio, cada pueblo conservaba a sus señores, sus dioses y su idioma… mientras pagara. Si no pagaba, llegaba el ejército.",
        "[short pause] Así funcionaba el imperio: menos un país, y más una red de pueblos que pagaban de mala gana.",
    ]},
    {"id": "axayacatl", "frases": [
        "En 1473, el tlatoani Axayácatl resolvió por las malas una vieja rivalidad con la ciudad hermana: conquistó Tlatelolco.",
        "Su rey, Moquíhuix, murió cayendo de lo alto de su pirámide.",
        "Pero Axayácatl también se llevó la peor derrota de la historia mexica: contra los purépechas de Michoacán.",
        "Los purépechas trabajaban el metal y tenían su propio imperio al oeste. Los mexicas nunca pudieron con ellos.",
        "Y de estos años viene la piedra más famosa de México: la Piedra del Sol.",
        "[curious] Y no, no es un calendario para ver qué día es. Es un monumento al sol de casi 25 toneladas, con las cuatro eras que según los mexicas ya habían terminado.",
        "Después de la conquista la enterraron, y reapareció en 1790, cuando arreglaban la plaza principal de la ciudad.",
    ]},
    {"id": "ahuizotl", "frases": [
        "En 1486 llegó Ahuízotl, el más guerrero de todos. Llevó el imperio hasta la frontera de Guatemala, al Soconusco, tierra de cacao.",
        "Y en 1487 reinauguró el Templo Mayor, la gran pirámide doble: un templo para Huitzilopochtli y otro para Tláloc, el dios de la lluvia.",
        "Se dice que en esa ceremonia sacrificaron a ochenta mil personas en cuatro días.",
        "[short pause] Esa cifra casi seguro es exagerada: saldría una persona cada pocos segundos, sin parar, día y noche. Pero el sacrificio humano sí fue real.",
        "En 2015, los arqueólogos encontraron el Huey Tzompantli: un muro de cráneos de cientos de personas, hombres, mujeres y niños.",
        "Para los mexicas, el sol necesitaba sangre para seguir moviéndose. Sin sacrificios, el mundo se acababa.",
        "Ahuízotl también quiso más agua y abrió un nuevo acueducto. Funcionó demasiado bien: inundó la ciudad.",
        "[curious] Su nombre era el de un animal de agua mítico. Y nos dejó una palabra en español: ahuizote, alguien que molesta y molesta sin parar.",
    ]},
    {"id": "moctezuma2", "frases": [
        "En 1502 subió al trono Moctezuma Xocoyotzin, el joven. Moctezuma segundo.",
        "Era sacerdote y guerrero, y muy estricto con el protocolo: casi nadie podía mirarlo a la cara.",
        "Tenía un zoológico con jaguares, águilas y serpientes, y aviarios con pájaros de todo el imperio.",
        "En su tiempo, Tenochtitlan tenía entre setenta y cinco mil y doscientos mil habitantes, según quién haga la cuenta. Era más grande que Sevilla y que la Roma de aquel tiempo.",
        "El imperio cobraba tributo a decenas de provincias, del Golfo al Pacífico.",
        "Y entonces, cuentan, empezaron los presagios: un cometa, un templo que ardió solo, una mujer que lloraba de noche por sus hijos.",
        "[short pause] Ojo: esos presagios se escribieron años después de la conquista. Quizá fueron una forma de explicar lo inexplicable.",
        "Xolo, eso sí, llevaba días aullando.",
    ]},
    {"id": "cortes", "frases": [
        "En 1519 llegaron a la costa de Veracruz once barcos, con unos quinientos españoles y dieciséis caballos. Los mandaba Hernán Cortés.",
        "Con ellos venía una mujer que lo cambiaría todo: Malintzin, la Malinche. Hablaba náhuatl y maya, y pronto español. Fue la voz de Cortés.",
        "Cortés mandó hundir sus barcos para que nadie pudiera regresarse, y caminó tierra adentro.",
        "Los totonacas de Cempoala, hartos del tributo, se le unieron. Y en Tlaxcala, después de pelear contra él, también.",
        "[short pause] ¿Te acuerdas de la guerra florida? Tlaxcala tenía muchas cuentas pendientes con Tenochtitlan.",
        "En Cholula, Cortés y sus aliados mataron a miles de personas en unas horas.",
        "Y el 8 de noviembre de 1519, en la calzada de Iztapalapa, Moctezuma salió a recibirlo.",
        "Le regaló collares, lo hospedó en el palacio de su padre… y Cortés, a los pocos días, lo tomó prisionero en su propia ciudad.",
        "[curious] El famoso penacho de Moctezuma está hoy en un museo de Viena. Y ni siquiera es seguro que haya sido suyo.",
    ]},
    {"id": "caida", "frases": [
        "En mayo de 1520, Cortés salió a pelear contra otros españoles y dejó al mando a Pedro de Alvarado.",
        "En plena fiesta de Tóxcatl, junto al Templo Mayor, Alvarado atacó a los nobles que bailaban desarmados.",
        "La ciudad se levantó. Moctezuma salió a calmar a su gente y murió: los españoles dijeron que por las piedras de los suyos; los mexicas, que lo mataron los españoles.",
        "La noche del 30 de junio, los españoles huyeron por la calzada de Tlacopan cargados de oro. Muchos se ahogaron por el peso.",
        "Es la Noche Triste. Cuenta la leyenda que Cortés lloró bajo un ahuehuete.",
        "Pero el peor enemigo no traía espada. [short pause] Era la viruela.",
        "Aquí nadie la conocía. La epidemia mató a miles, y al nuevo tlatoani, Cuitláhuac, a los pocos meses de reinar.",
        "Cortés volvió en 1521 con decenas de miles de guerreros indígenas aliados, y trece bergantines que armó por piezas para pelear en el lago.",
        "Cortaron el acueducto de Chapultepec. Sin agua dulce, sin comida y con la peste, la ciudad resistió casi tres meses.",
        "La defendía el último tlatoani, Cuauhtémoc, el águila que desciende. Tenía unos veinticinco años.",
        "El 13 de agosto de 1521, Cuauhtémoc fue capturado en una canoa en el lago, y Tenochtitlan cayó.",
        "[sighs] Casi doscientos años después de aquella águila sobre el nopal.",
    ]},
    {"id": "legado", "frases": [
        "Sobre las ruinas, los españoles construyeron la Ciudad de México, con las mismas piedras de los templos.",
        "Secaron los lagos poco a poco… y por eso hoy la ciudad se hunde, varios centímetros cada año.",
        "Pero los mexicas nunca se fueron del todo. Más de un millón y medio de personas hablan náhuatl hoy.",
        "Y tú también lo hablas sin saberlo: cuando dices tomate, aguacate, cacahuate o papalote, estás diciendo palabras en náhuatl.",
        "El águila de Tenochtitlan está en la bandera, y el nombre de México viene de los mexicas.",
        "¿Y Xolo? Sus parientes casi desaparecen, hasta que en el siglo veinte los criadores mexicanos los rescataron. Y en 2026, la Ciudad de México declaró patrimonio cultural todo lo que se sabe de él.",
        "Porque para los mexicas, el xoloitzcuintle tenía un trabajo muy importante: guiar a las almas a cruzar el río hacia el Mictlán, el mundo de los muertos.",
        "[short pause] O sea que Xolo nunca terminó en el menú. Terminó siendo el guía.",
    ]},
    {"id": "ruta", "frases": [
        "Si quieres comprobarlo con tus propios ojos, empieza en el Zócalo: ahí está el Museo del Templo Mayor, con la Coyolxauhqui que unos trabajadores de la luz encontraron en 1978.",
        "Sigue al Museo Nacional de Antropología, a ver la Piedra del Sol y a la Coatlicue.",
        "Luego Tlatelolco, en la Plaza de las Tres Culturas, donde cayó la ciudad, y Xochimilco, para pasear entre chinampas.",
        "Y si tienes un día más, Teotihuacan: una ciudad que ya estaba en ruinas cuando llegaron los mexicas, y que ellos visitaban con asombro.",
        "Te dejo en la descripción cómo llegar a cada lugar.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "De una tribu que nadie quería… al imperio que le dio su nombre a un país.",
        "[short pause] ¿Qué otra civilización quieres que contemos completa? Déjamelo en los comentarios, y suscríbete a Cronopapel. Xolo te lo agradece.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# FOTOS REALES (regla del canal: ≥ 3/min). Clave de foto en `fotos/` → se asignan en la coreografía. Ver `fotos/creditos.json`.
FOTOS = {}

# SFX de ElevenLabs/biblioteca en vez del sintetizador (regla del 22-oct-2026).
SFX_ELEVEN = {
    "pop": dict(prompt="Soft paper cut-out sticker popping onto a wooden desk, light cardboard tap, dry, close", seg=0.6, variantes=4),
    "whoosh": dict(prompt="Quick soft paper whoosh, a sheet of drawing paper swept through the air, short", seg=0.8, variantes=3),
    "escribir": dict(prompt="Pencil scribbling fast on rough drawing paper, short burst", seg=1.2, variantes=3),
    "golpe_suave": dict(prompt="Soft muffled thud of a small cardboard cut-out landing on a table", seg=0.6, variantes=3),
    "crece": dict(prompt="Short magical rising shimmer, something growing quickly, soft paper rustle", seg=1.0, variantes=3),
    "pasos": dict(prompt="Footsteps walking on a dry dirt road, several people, short", seg=1.5, variantes=2),
    "papel": dict(prompt="Sheet of old paper being unrolled and handled, crisp rustle", seg=1.0, variantes=2),
    "tambor": dict(prompt="Indigenous wooden war drum beats, huehuetl, short tense pattern", seg=1.5, variantes=2),
    "caracol": dict(prompt="Aztec conch shell trumpet blown once, deep and long, ceremonial, light reverb", seg=2.5, variantes=2),
    "flauta": dict(prompt="Short melodic phrase on a pre-Hispanic clay flute, airy and mysterious", seg=2.0, variantes=2),
    "pluck": dict(prompt="Single soft plucked guitar string note, warm, short", seg=0.7, variantes=3),
    "brillo": dict(prompt="Short sparkling chime twinkle, magical glint", seg=0.8, variantes=2),
    "impacto": dict(prompt="Heavy dull impact thud with a little dust, cartoonish but serious", seg=0.8, variantes=2),
    "sello": dict(prompt="Heavy rubber stamp pressed on a paper document, firm thump", seg=0.7, variantes=2),
    "ladrido": dict(prompt="Small hairless dog giving two short friendly barks, close, clean", seg=1.0, variantes=3),
    "gemido_perro": dict(prompt="Small dog whimpering nervously, short, close", seg=1.2, variantes=2),
    "aullido": ("Single small dog howling long and mournfully at night, distant crickets", 3),
    "agua_lago": ("Calm lake water lapping against reeds, a canoe paddle dipping, birds far away", 4),
    "remo": dict(prompt="Wooden canoe paddle stroke in still lake water, single stroke", seg=1.0, variantes=3),
    "aguila": ("Eagle screech in open sky, single call", 1.5),
    "cascabel": ("Rattlesnake rattle warning, close, dry", 1.5),
    "fuego": ("Bonfire crackling, papers and old books catching fire", 3),
    "multitud": dict(prompt="Busy ancient open-air market crowd, many voices bargaining in a non-English language, no music", seg=4, bib=False),
    "guajolote": ("Turkey gobbling, single bird, outdoor", 1.2),
    "flecha": ("Arrow whistling through the air and thudding into wood", 1.2),
    "batalla": dict(prompt="Ancient battle with wooden clubs, shields clashing and warriors shouting, no guns", seg=3, variantes=2),
    "canonazo": ("Single 16th century cannon shot, booming, distant echo", 2),
    "galope": dict(prompt="Several horses galloping on a dry dirt road, passing by left to right", seg=4, variantes=2),
    "ola": ("Sea waves on a sandy beach, wooden sailing ships creaking at anchor", 4),
    "trueno": ("Distant rolling thunder over a valley", 3),
    "viento_frio": ("Cold whistling wind over dry fields, frost", 3),
    "inundacion": ("Rushing flood water pouring through streets, splashes and debris", 3),
    "cometa": ("Low eerie whoosh of a comet crossing the night sky, ominous", 3),
    "llanto": dict(prompt="Distant woman wailing sorrowfully at night, eerie echo, no words", seg=3, bib=False),
    "tos": ("Several people coughing weakly in a dark room, sickness", 2.5),
    "monedas": ("Handful of cacao beans poured into a clay bowl, dry rattling", 1.5),
    "piedra": ("Heavy stone block scraped and dropped onto stone, deep thud", 1.5),
    "cincel": ("Stone carving with chisel and hammer, rhythmic taps", 2),
    "ciudad": ("Modern Mexico City traffic and street ambience, horns far away", 3),
    "campana": dict(prompt="Single bronze church bell toll in a colonial Mexican city, warm daylight, light reverb", seg=3, bib=False),
    "fanfarria": dict(prompt="Short bright brass fanfare flourish, festive", seg=1.5, variantes=2),
    "trajinera": ("Mariachi trumpet far away over a canal, a boat pole pushing water, people chatting happily", 4),
    "patos": ("A few ducks quacking softly on a calm lake, close, short", 1.5),
    "jaguar": ("Jaguar growl, short and deep, close, outdoor", 1.5),
    "barco_hunde": ("Wooden sailing ship creaking and sinking into the sea, water gurgling and bubbling", 3),
}

# Música con Lyria: antes, la BIBLIOTECA (`python fab.py biblioteca sugerir historia_aztecas`)
LYRIA = dict(
    estilo=("Warm, cinematic animated-history documentary score inspired by ancient central Mexico: clay flutes, ocarinas, "
            "huehuetl and teponaztli drums, rattles and conch shells blended with orchestral strings and a light modern documentary "
            "pulse; playful moments with pizzicato and marimba. Instrumental only, no singing. "
            "Middle frequencies kept clear so a Spanish narrator can speak distinctly over it."),
    escenas={},
    tramos=[
        (["gancho", "aztlan"],
         "Begin with a wondrous reveal of a city on a lake, then a long mythical journey: walking drums, flute, mystery and legend."),
        (["chapultepec"],
         "Playful and a bit comic: unwanted neighbors, a rocky field of rattlesnakes eaten for dinner, then a dark twist and a chase into the reeds."),
        (["fundacion", "chinampas"],
         "Solemn and wondrous for the eagle omen on the lake, then busy, hopeful and inventive: farmers building floating gardens."),
        (["alianza", "moctezuma1"],
         "Rising imperial ambition: war drums and brass-like strings, a dark burning moment, cold famine, then the strange flower war."),
        (["vida", "tributo", "axayacatl"],
         "Lively bustling marketplace music with marimba and rattles, then proud imperial tribute march, ending with a stone carving motif."),
        (["ahuizotl", "moctezuma2"],
         "Grand and dark ceremonial temple music, sacrificial drums, then splendor of the court and growing omens, ending uneasy."),
        (["cortes", "caida"],
         "Tension of strangers arriving by sea, horses and cannons, a hopeful meeting turning into tragedy, the sad night, plague and siege, a mournful fall."),
        (["legado", "ruta", "cierre"],
         "Begin melancholic and reflective, become warm and proud (living legacy, a loyal dog guiding souls), end bright and inviting with a natural fade-out."),
    ],
)

# Whisper escribe distinto los nombres en náhuatl y a Xolo («Shono», «Cholo», «Solo»); revisadas las transcripciones el 23-nov.
CER_MAX_POR_FRASE = {k: 0.08 for k in ("chapultepec_8", "chapultepec_11", "chinampas_7", "alianza_0", "moctezuma1_0", "vida_1", "vida_2",
                                         "vida_8", "axayacatl_1", "ahuizotl_4", "moctezuma2_7", "ruta_0", "ruta_1")}

# Ubicación en México (crono_ubicacion): apertura con México entero → zoom al Valle de México.
UBICACION = {"prota": "MX-DIF", "nombre": "VALLE DE MÉXICO", "subtitulo": "centro de México"}
