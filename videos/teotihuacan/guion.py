# -*- coding: utf-8 -*-
"""Teotihuacán: la ciudad que se quedó sin nombre — 6 minutos, canal Bitácora Perdida, estilo Kurzgesagt,
PLANO SECUENCIA (sin cortes). Las "escenas" solo marcan narración y música; escenas.py dibuja un único mundo.

Datos verificados (fuentes):
  - Primer asentamiento hacia el 600 a. C.; ciudad hacia el 100 a. C.; monumentos principales hasta ~250 d. C.
    (Wikipedia: Teotihuacan; INAH).
  - Población: ~100 000 hacia el 300; en su apogeo (400-500) entre 100 000 y 200 000 según la estimación;
    área urbana ~21 km2 (Millon; Cowgill).
  - Calzada de los Muertos: ~40 m de ancho y ~4 km de largo. Nombre puesto por los mexicas, que creyeron que los
    montículos eran tumbas; eran templos y palacios.
  - Pirámide del Sol: base ~220 x 232 m, altura 65 m. Pirámide de la Luna al extremo norte de la calzada.
  - ~2 000 conjuntos habitacionales multifamiliares; barrio Tlailotlacan (migrantes zapotecas de Oaxaca);
    barrio de los comerciantes (Golfo). Talleres de obsidiana; obsidiana verde de Pachuca.
  - Tikal: Estela 31 y "la entrada" del 378: Sihyaj K'ahk' llega a ~1 000 km de distancia; muere el rey local
    (Chak Tok Ich'aak) y sube Yax Nuun Ayiin I, representado con atuendo teotihuacano.
  - Túnel bajo el Templo de la Serpiente Emplumada: descubierto a finales de 2003 (Sergio Gómez Chávez y Julie
    Gazzola) tras un hundimiento por lluvia; ~100 m de largo, 14 m de profundidad, sellado hace ~1 800 años;
    tres cámaras; casi 75 000 piezas catalogadas (conchas, semillas, jade, esferas metálicas de pirita) y
    un paisaje en miniatura con pozas de mercurio líquido (2015).
  - Hacia el 550: incendio y saqueo sistemático de los edificios de la élite en la Calzada; esculturas
    destrozadas; las casas comunes en gran parte intactas. Hipótesis: revuelta interna, ataque externo,
    sequía ligada a los eventos climáticos de 535-536.
  - Mexicas (siglo XIV en adelante): mito del Quinto Sol en Teotihuacán; el dios orgulloso duda cuatro veces
    y el humilde salta a la hoguera. El nombre náhuatl significa "lugar donde nacieron los dioses".
  - Patrimonio Mundial de la UNESCO: 1987. Visitantes en 2024: 1 313 321 (INAH).
"""

TITULO = "Teotihuacán: la ciudad que se quedó sin nombre"
ARCHIVO = "teotihuacan_ciudad_sin_nombre"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 92
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)
GAP = 0.7
TRANSICIONES = [("continua", 0.1)] * 10
MUSICA = {
    "intro": dict(sabor="vacio", raiz=38),
    "valle": dict(sabor="espacio", raiz=40),
    "trazo": dict(sabor="esperanza", raiz=41),
    "gente": dict(sabor="esperanza", raiz=43),
    "comercio": dict(sabor="espacio", raiz=41),
    "tunel": dict(sabor="tension", raiz=36),
    "fuego": dict(sabor="tension", raiz=38),
    "silencio": dict(sabor="vacio", raiz=36),
    "mexicas": dict(sabor="espacio", raiz=40),
    "hoy": dict(sabor="esperanza", raiz=43),
    "cierre": dict(sabor="esperanza", raiz=41),
}

ESCENAS = [
    {
        "id": "intro",
        "post": 2.5,
        "frases": [
            "Hace mil quinientos años, en un valle de México, vivían más de cien mil personas.",
            "Era una de las ciudades más grandes del planeta, con pirámides gigantes y calles trazadas con regla.",
            "Pero siglos después, cuando llegaron los mexicas, ya estaba en ruinas, y nadie sabía quién la había construido.",
            "Ni siquiera cómo se llamaba.",
            "Esta es la historia de Teotihuacán, la ciudad que se quedó sin nombre.",
        ],
    },
    {
        "id": "valle",
        "post": 3.0,
        "frases": [
            "Está a unos cuarenta kilómetros al noreste de la actual Ciudad de México.",
            "En esa época, el valle era una cuenca cerrada, con lagos en el centro y montañas alrededor.",
            "Los primeros pobladores llegaron hace más de dos mil años, atraídos por los manantiales y la tierra fértil.",
            "En pocos siglos, aquel pueblo creció hasta cubrir unos veinte kilómetros cuadrados.",
            "El nombre Teotihuacán ni siquiera es suyo: se lo pusieron los mexicas, mucho después.",
            "Significa, más o menos, el lugar donde nacieron los dioses.",
            "Cómo la llamaban sus habitantes, no lo sabemos.",
        ],
    },
    {
        "id": "trazo",
        "post": 3.0,
        "frases": [
            "Lo primero que sorprende es que nada se levantó al azar.",
            "Toda la ciudad se organizó en cuadrículas, alrededor de una gran avenida de unos cuatro kilómetros.",
            "Los mexicas la bautizaron Calzada de los Muertos, porque creyeron que los montículos de sus lados eran tumbas.",
            "En realidad, eran templos y palacios.",
            "Al fondo está la Pirámide de la Luna, y a un lado, la del Sol, de sesenta y cinco metros de altura.",
            "Y se levantó sin animales de carga ni carretas: a fuerza de gente.",
        ],
    },
    {
        "id": "gente",
        "post": 3.0,
        "frases": [
            "Y había mucha gente: más de cien mil personas, y quizá muchas más en su mejor momento.",
            "Casi todas vivían en unos dos mil conjuntos de casas, con patios interiores donde convivían varias familias.",
            "Las paredes se cubrían de murales rojos y azules: jaguares, agua, plumas y sacerdotes.",
            "Había barrios enteros de extranjeros, como uno de gente venida de Oaxaca.",
            "Y talleres por todas partes, sobre todo de obsidiana, un vidrio volcánico con un filo finísimo.",
        ],
    },
    {
        "id": "comercio",
        "post": 3.0,
        "frases": [
            "Con esas navajas, Teotihuacán comerciaba con medio Mesoamérica.",
            "La obsidiana verde salía de las minas de Pachuca y llegaba hasta las selvas mayas.",
            "En Tikal, una ciudad maya a mil kilómetros de distancia, una inscripción cuenta que en el año trescientos setenta y ocho llegó un guerrero extranjero.",
            "Poco después murió el rey de Tikal, y subió al trono un joven vestido a la manera de Teotihuacán.",
            "Nadie sabe si fue una conquista, una alianza o una mezcla de las dos.",
            "Lo que sí sabemos es que su influencia llegó muy lejos.",
        ],
    },
    {
        "id": "tunel",
        "post": 3.0,
        "frases": [
            "Pero lo más extraño no estaba a la vista, sino bajo la tierra.",
            "En dos mil tres, después de una tormenta, se abrió un hueco frente al Templo de la Serpiente Emplumada.",
            "Debajo había un túnel de casi cien metros, sellado a propósito hace unos mil ochocientos años.",
            "Al final, tres cámaras y decenas de miles de objetos: conchas, semillas, figuras de jade y esferas de una piedra que brilla como el oro.",
            "Y un paisaje en miniatura, con pequeñas pozas de mercurio líquido que quizá imitaban lagos.",
            "Los arqueólogos buscan si allí está la tumba de uno de los gobernantes.",
            "Todavía no la han encontrado.",
        ],
    },
    {
        "id": "fuego",
        "post": 3.0,
        "frases": [
            "Hacia el año quinientos cincuenta, la ciudad empezó a arder.",
            "Casi todo el fuego se concentró en la Calzada de los Muertos: templos, palacios y edificios de la élite.",
            "Las esculturas fueron destrozadas, y sus pedazos, tirados.",
            "En cambio, muchos conjuntos de casas donde vivía la gente común se salvaron.",
            "¿Quién lo hizo? No hay una respuesta definitiva.",
            "Una hipótesis dice que el pueblo se rebeló contra sus gobernantes. Otra, que fue un ataque desde fuera.",
            "Y otra apunta al clima: sequías y hambre que habrían debilitado a la ciudad.",
            "Quizá fueron varias cosas al mismo tiempo.",
        ],
    },
    {
        "id": "silencio",
        "post": 3.0,
        "frases": [
            "La gente se fue marchando, y la ciudad se fue vaciando.",
            "Se dispersaron por el valle y más allá.",
            "Dejaron símbolos, pero ningún texto que sepamos descifrar.",
            "La lluvia y el viento cubrieron las pirámides de tierra y maleza.",
            "Durante siglos, nadie volvió a pronunciar su nombre.",
        ],
    },
    {
        "id": "mexicas",
        "post": 3.0,
        "frases": [
            "Siglos más tarde, llegaron los mexicas.",
            "Al ver aquellas pirámides enormes, pensaron que no las había hecho gente, sino los dioses.",
            "Y contaron una historia: en la oscuridad del mundo, los dioses se reunieron en Teotihuacán para crear un nuevo Sol.",
            "Dos de ellos debían saltar a una hoguera: uno rico y orgulloso, y otro pobre y enfermo.",
            "El rico dudó cuatro veces. El humilde saltó sin pensarlo.",
            "Y del fuego nació el Sol que conocemos.",
        ],
    },
    {
        "id": "hoy",
        "post": 3.0,
        "frases": [
            "Hoy sus ruinas son Patrimonio de la Humanidad desde mil novecientos ochenta y siete.",
            "Cada año las visitan más de un millón de personas.",
            "Y cada primavera, miles suben a la Pirámide del Sol para recibir la luz del amanecer.",
            "Bajo sus calles, la arqueología sigue encontrando túneles, murales y tumbas.",
        ],
    },
    {
        "id": "cierre",
        "post": 4.0,
        "frases": [
            "Teotihuacán fue enorme, rica y poderosa. Y aun así, su nombre, su idioma y su final siguen siendo un misterio.",
            "Quizá por eso sigue fascinando: porque es una historia que aún no termina de contarse.",
            "Esto fue Bitácora Perdida. Nos vemos en la próxima historia.",
        ],
    },
]
