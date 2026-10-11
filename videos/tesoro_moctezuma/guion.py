# -*- coding: utf-8 -*-
"""El tesoro perdido de Moctezuma: la noche en que desapareció el oro (mini documental, ~6 min, 16:9).
Estilo `documental` (motor nucleo/docu.py): fotos y grabados con parallax 2.5D, polaroids, corcho con hilo rojo, mapas,
texto sincronizado con la voz, viñeta y grano. Voz: Dan. Canal: Bitácora Perdida.

Datos verificados (fuentes):
  - Bernal Díaz del Castillo, "Historia verdadera de la conquista de la Nueva España" (1568): los españoles, alojados desde noviembre
    de 1519 en las casas de Axayácatl (padre de Moctezuma), advirtieron una puerta recién tapiada (el carpintero Alonso Yáñez); al abrirla
    hallaron una sala con oro, jade y piedras preciosas (Arqueología Mexicana nº 144).
  - Primer envío de Cortés a Carlos V (julio de 1519): Alberto Durero lo vio en Bruselas en agosto de 1520 y anotó en su diario un sol de oro
    y una luna de plata enormes y "nada que tanto alegrara mi corazón". Ninguna pieza sobrevive: todo se fundió (Metropolitan Museum of Art,
    "Gold of the Indies"; Diario de Durero, 1520-21).
  - Cortés hizo fundir el oro en barras; el quinto real para la Corona, el quinto de Cortés y el resto para la tropa (Wikipedia/Live Science/Smithsonian).
  - Noche Triste, 30 junio - 1 julio 1520: huida por la calzada de Tlacopan (Tacuba) bajo la lluvia; soldados sobrecargados de oro cayeron al
    lago y se ahogaron. Bajas españolas: Cortés 154; López de Gómara y Bernal Díaz ~450; Tlaxcaltecas: 1 000 (Díaz) a 4 000 (Gómara). Se perdieron la
    artillería, casi todos los caballos y buena parte del tesoro (Wikipedia: La Noche Triste).
  - Matanza de Toxcatl (mayo de 1520): Cortés había salido a enfrentar a Pánfilo de Narváez y dejó a Pedro de Alvarado al mando; Alvarado atacó a
    los nobles mexicas reunidos en el Templo Mayor y estalló el levantamiento; Cortés regresó y los españoles quedaron sitiados en el palacio.
  - Muerte de Moctezuma: los españoles dicen que lo apedrearon los mexicas; las fuentes indígenas, que lo mataron los españoles (ibíd.).
    Matanza del Templo Mayor (fiesta de Toxcatl, mayo de 1520) por Pedro de Alvarado: detonante del levantamiento.
  - Caída de Tenochtitlan: 13 de agosto de 1521. Cuauhtémoc y el señor de Tacuba: tormento con aceite en los pies a instancias del tesorero
    Juan Alderete; dijeron que cuatro días antes de la captura habían arrojado el oro al lago (Infobae/Ledesma Bouchan; Dialnet nº 283).
  - Barra de oro: hallada el 13-mar-1981 por obreros que excavaban junto a la Alameda de la Ciudad de México; 1,93 kg; el INAH confirmó con
    fluorescencia de rayos X (Arqueología Mexicana, enero de 2020) que su composición coincide con la del oro mexica de la época; sobre la ruta de
    la Noche Triste (Phys.org/AFP; Smithsonian Magazine). Es la única pieza certificada de aquel oro.
  - Para los mexicas el jade y las plumas de quetzal valían más que el oro (proyecto Templo Mayor/INAH; Arqueología Mexicana); al oro lo llamaban
    teocuitlatl, «excremento de los dioses». Antes de la huida Cortés cargó en caballos el quinto real y el suyo y dejó tomar el resto (Bernal Díaz, Noticonquista/UNAM).
  - Tras la Noche Triste: refugio en Tlaxcala; viruela a finales de 1520 (murió Cuitláhuac; le sucedió Cuauhtémoc); mayo de 1521 regreso con 13 bergantines;
    ~3 meses de asedio (Noticonquista, SEP, Wikipedia). Tradición: Cortés lloró bajo un árbol al amanecer.
  - Templo Mayor redescubierto el 21-feb-1978: trabajadores de la Compañía de Luz y Fuerza del Centro hallaron el monolito de Coyolxauhqui en Guatemala y Argentina (INAH; N+).
  - Palacio de Axayácatl: en 2017 aparecieron restos de basalto bajo el Nacional Monte de Piedad (casa de empeño, edificio de 1774-77 sobre el sitio del palacio); 2018: segunda sala (Wikipedia: Palace of Axayacatl).
Imágenes: Wikimedia Commons (dominio público/CC; ver imagenes/creditos.json) y video de apoyo de Pexels (clips/creditos_clips.json).
"""

TITULO = "El tesoro perdido de Moctezuma"
ARCHIVO = "tesoro_moctezuma"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 96
GAP = 0.42
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.3, temperature=0.75)
MEZCLA = dict(musica=-22.0, sfx=-26.0)
TRANSICIONES = [("continua", 0.1)] * 18
MUSICA = {
    "gancho": dict(sabor="tension", raiz=38),
    "llegada": dict(sabor="vacio", raiz=38),
    "puerta": dict(sabor="tension", raiz=40),
    "valor": dict(sabor="vacio", raiz=38),
    "durero": dict(sabor="espacio", raiz=38),
    "fundicion": dict(sabor="tension", raiz=36),
    "matanza": dict(sabor="tension", raiz=36),
    "muerte": dict(sabor="vacio", raiz=36),
    "antes_huida": dict(sabor="tension", raiz=40),
    "noche": dict(sabor="tension", raiz=41),
    "bajas": dict(sabor="vacio", raiz=38),
    "regreso": dict(sabor="espacio", raiz=38),
    "cuauhtemoc": dict(sabor="tension", raiz=40),
    "lago": dict(sabor="vacio", raiz=38),
    "subsuelo": dict(sabor="espacio", raiz=38),
    "barra": dict(sabor="espacio", raiz=40),
    "palacio": dict(sabor="tension", raiz=38),
    "teorias": dict(sabor="tension", raiz=41),
    "cierre": dict(sabor="vacio", raiz=38),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "Una noche de junio de mil quinientos veinte, cientos de soldados españoles huyeron de la ciudad más rica de América.",
        "Llevaban encima una fortuna en oro, joyas y plumas.",
        "Al amanecer, casi todo había desaparecido. Y cinco siglos después, nadie sabe dónde está.",
    ]},
    {"id": "llegada", "frases": [
        "En noviembre de mil quinientos diecinueve, Hernán Cortés entró a Tenochtitlan, la capital del imperio mexica.",
        "El emperador Moctezuma lo hospedó en el antiguo palacio de su padre.",
        "Sus regalos de oro, con los que esperaba que se marcharan, solo despertaron la codicia de los españoles.",
    ]},
    {"id": "puerta", "frases": [
        "Ahí, los españoles notaron algo extraño: una puerta que alguien había tapiado hacía poco.",
        "Según el soldado Bernal Díaz del Castillo, tiraron el muro y encontraron una sala llena de oro, jade y piedras preciosas.",
        "Era el tesoro que Moctezuma había heredado de sus antepasados.",
    ]},
    {"id": "valor", "frases": [
        "Curiosamente, para los mexicas el oro no era su mayor riqueza.",
        "Valoraban más el jade y las plumas de quetzal, materiales reservados a la élite.",
        "Al oro lo llamaban «excremento de los dioses».",
        "Los españoles, en cambio, solo veían metal para fundir.",
    ]},
    {"id": "durero", "frases": [
        "Cortés ya había enviado a su rey un primer cargamento de regalos.",
        "En mil quinientos veinte, el pintor alemán Alberto Durero lo vio en Bruselas.",
        "Describió un sol de oro enorme y una luna de plata igual de grande. Escribió que jamás había visto nada que le alegrara tanto el corazón.",
    ]},
    {"id": "fundicion", "frases": [
        "Pero aquel oro no se conservó como arte.",
        "Cortés ordenó fundirlo en barras: una parte para el rey, otra para él, y el resto para los soldados.",
        "Ninguna de las piezas que vio Durero ha sobrevivido.",
    ]},
    {"id": "matanza", "frases": [
        "Cortés salió de la ciudad para enfrentar a otro capitán español, y dejó al mando a Pedro de Alvarado.",
        "En mayo de mil quinientos veinte, durante una fiesta religiosa, Alvarado atacó a cientos de nobles mexicas reunidos en el Templo Mayor.",
        "La ciudad estalló de furia. Cuando Cortés regresó, los españoles ya estaban sitiados en el palacio.",
    ]},
    {"id": "muerte", "frases": [
        "Moctezuma subió al techo del palacio para calmar a su pueblo.",
        "En junio murió Moctezuma, y hasta hoy se discute cómo: los españoles culparon a su pueblo, y las fuentes indígenas, a los españoles.",
        "La ciudad se levantó en armas, y Cortés decidió escapar.",
    ]},
    {"id": "antes_huida", "frases": [
        "Antes de escapar, Cortés apartó el quinto del rey y el suyo, y ordenó cargarlos en caballos.",
        "Luego dijo a los soldados que tomaran el oro que quisieran.",
        "Muchos aceptaron, sin imaginar que aquel peso les costaría la vida.",
    ]},
    {"id": "noche", "frases": [
        "La noche del treinta de junio, bajo la lluvia, salieron en silencio por la calzada de Tacuba.",
        "Pero los descubrieron. Guerreros mexicas los atacaron desde las canoas, y la calzada se llenó de gente.",
        "Muchos soldados cargaban tanto oro que no podían pelear ni nadar.",
        "Cayeron al agua y se hundieron con su botín.",
    ]},
    {"id": "bajas", "frases": [
        "Cortés admitió ciento cincuenta y cuatro españoles muertos. Otros cronistas hablan de cuatrocientos cincuenta o más, y de entre mil y cuatro mil aliados.",
        "Se perdieron también los cañones, casi todos los caballos y buena parte del oro.",
        "Cuenta la tradición que, al amanecer, Cortés lloró bajo un árbol la pérdida de sus hombres.",
    ]},
    {"id": "regreso", "frases": [
        "Los sobrevivientes se refugiaron en Tlaxcala, la ciudad aliada, donde se recuperaron.",
        "Mientras tanto, la viruela devastó Tenochtitlan y mató al nuevo emperador.",
        "En mayo de mil quinientos veintiuno, Cortés volvió con miles de aliados y trece bergantines para dominar el lago.",
        "Tras unos tres meses de asedio, con hambre y enfermedad, la ciudad estaba destruida.",
    ]},
    {"id": "cuauhtemoc", "frases": [
        "Al final, Tenochtitlan cayó el trece de agosto de mil quinientos veintiuno, pero el tesoro no apareció.",
        "Cortés presionó a Cuauhtémoc, el último emperador mexica.",
        "Le quemaron los pies con aceite hirviendo.",
        "Según las crónicas, confesó que cuatro días antes habían arrojado todo el oro al lago.",
        "Los soldados esperaban su parte del botín, y Cortés había gastado su fortuna en la expedición.",
        "Muchos sospecharon que se había quedado con parte del oro.",
    ]},
    {"id": "lago", "frases": [
        "Esa fortuna nunca apareció. Con los siglos, el lago se secó, y sobre él se levantó la Ciudad de México.",
        "Es decir: parte del tesoro podría estar bajo el asfalto.",
    ]},
    {"id": "subsuelo", "frases": [
        "El subsuelo de la ciudad ya ha devuelto secretos antes.",
        "En mil novecientos setenta y ocho, unos electricistas que cavaban en el centro toparon con una enorme piedra tallada.",
        "Debajo estaba el Templo Mayor, enterrado durante siglos.",
    ]},
    {"id": "barra", "frases": [
        "En mil novecientos ochenta y uno, unos obreros que excavaban junto a la Alameda Central encontraron una barra de oro de casi dos kilos.",
        "En dos mil diecinueve, un análisis químico confirmó que era oro de la época de Moctezuma.",
        "Apareció justo en la ruta de la huida, y sigue siendo la única pieza identificada de aquel oro.",
        "Si una sola barra escapó de todas las manos, ¿cuántas más podrían seguir bajo tierra?",
    ]},
    {"id": "palacio", "frases": [
        "Y hay una ironía más. En dos mil diecisiete, al remodelar el Nacional Monte de Piedad, una casa de empeño del centro, aparecieron ruinas del palacio donde Cortés vio el tesoro.",
        "Hoy, en ese mismo lugar, se guardan joyas empeñadas.",
    ]},
    {"id": "teorias", "frases": [
        "¿Qué pasó, entonces, con el tesoro?",
        "Unos creen que sigue en el fondo del antiguo lago, bajo la ciudad.",
        "Otros, que los mexicas lo recuperaron y lo escondieron.",
        "Y algunos historiadores sospechan que la fortuna fue menor de lo que cuenta la leyenda.",
    ]},
    {"id": "cierre", "post": 2.0, "frases": [
        "Lo único seguro es que aquella noche, la lluvia, el lago y la codicia se tragaron una de las mayores fortunas de la historia.",
        "Quizá, bajo las calles que hoy recorremos, todavía duerme el oro de Moctezuma.",
        "¿Y si la próxima barra la encuentra alguien que solo iba a cavar unos cimientos?",
    ]},
]
