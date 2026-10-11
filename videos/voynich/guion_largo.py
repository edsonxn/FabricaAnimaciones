# -*- coding: utf-8 -*-
"""El libro que nadie puede leer: el manuscrito Voynich (mini documental, ~2 min, 16:9).
Estilo `documental`: fotos y escaneos con parallax 2.5D, polaroids, tablero de evidencias, mapas, texto serif
amarillo/blanco sincronizado con la voz, viñeta y grano (referencia: "Detrás del Enigma", Líneas de Nazca).

Datos verificados (fuentes):
  - Beinecke Rare Book & Manuscript Library (Yale), MS 408, "Cipher Manuscript": seis secciones (plantas, astronomía/
    astrología, baños o balneología, medallones cosmológicos, farmacia, texto sin ilustrar); escritura sin descifrar.
    Wilfrid M. Voynich lo compró en 1912 al colegio jesuita de Frascati, cerca de Roma; H. P. Kraus lo donó a Yale en 1969.
  - Carbono 14 (Universidad de Arizona, 2009, cuatro muestras de pergamino): 1404-1438 d. C. con 95 % de confianza.
  - Se conservan 240 de unas 272 páginas originales (Yale/Wikipedia: Voynich manuscript).
  - Carta de Johannes Marcus Marci a Athanasius Kircher (siglo XVII): dice que Rodolfo II (r. 1576-1612) lo compró por 600 ducados.
  - William Friedman (rompió el cifrado japonés PURPLE) trabajó en él durante décadas; en 1959 concluyó que era, probablemente,
    un lenguaje filosófico artificial (NSA). No se ha descifrado.
  - Georg Baresch, alquimista de Praga, escribió a Athanasius Kircher en 1639 (primera mención confirmada); no se sabe si Kircher
    respondió, pero intentó adquirir el libro (Wikipedia: Voynich manuscript). Eamon Duffy: al menos 14 o 15 pieles de ternero sin usar
    hacen inconcebible una falsificación posmedieval. Friedman anagramó en 1959 su conclusión: 'un intento temprano de construir un
    lenguaje artificial de tipo a priori' (Philological Quarterly). Plantas: 'ninguna identificable sin ambigüedad' (Wikipedia). ~38 000 palabras; un alfabeto de 20-25 caracteres cubre casi todo el texto.
    El grupo de Friedman (años 1940) transcribió cada línea a tarjetas perforadas IBM.
  - Montemurro y Zanette (PLOS ONE, 2013): la distribución de palabras y su agrupación por temas se parecen a las de un idioma real.
Imágenes: escaneos de dominio público (Beinecke/Yale vía Wikimedia Commons); ver videos/voynich/imagenes/creditos.json.
"""

TITULO = "El libro que nadie puede leer"
ARCHIVO = "voynich_libro_ilegible"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 84
GAP = 0.42
VOZ = dict(referencia="C:/chatterbox_voices/Enigma.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)
MEZCLA = dict(musica=-20.0, sfx=-23.0)
SUBTITULOS = False          # el estilo dibuja su propio texto sincronizado; el .srt se genera igual
TRANSICIONES = [("continua", 0.1)] * 7
MUSICA = {
    "gancho": dict(sabor="tension", raiz=38),
    "origen": dict(sabor="vacio", raiz=38),
    "contenido": dict(sabor="tension", raiz=40),
    "fecha": dict(sabor="espacio", raiz=38),
    "duenos": dict(sabor="vacio", raiz=36),
    "intentos": dict(sabor="tension", raiz=40),
    "teorias": dict(sabor="tension", raiz=41),
    "cierre": dict(sabor="vacio", raiz=38),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "Existe un libro que nadie en el mundo ha podido leer.",
        "Tiene doscientas cuarenta páginas, dibujos imposibles y un idioma que no aparece en ningún otro lado.",
        "Lo han intentado criptógrafos, militares y computadoras. Hasta hoy, nadie lo ha logrado.",
    ]},
    {"id": "origen", "frases": [
        "Nuestra historia empieza en mil novecientos doce.",
        "Un vendedor de libros antiguos, Wilfrid Voynich, compra un manuscrito en un colegio jesuita, cerca de Roma.",
        "Desde entonces, el libro lleva su apellido.",
    ]},
    {"id": "contenido", "frases": [
        "Dentro hay plantas que ningún botánico ha logrado identificar con certeza.",
        "Diagramas de estrellas, mujeres bañándose en tuberías extrañas, y página tras página de un alfabeto desconocido.",
        "Nadie sabe quién lo escribió, ni por qué.",
    ]},
    {"id": "fecha", "frases": [
        "En dos mil nueve, la Universidad de Arizona fechó su pergamino con carbono catorce.",
        "El resultado: entre mil cuatrocientos cuatro y mil cuatrocientos treinta y ocho.",
        "El pergamino es medieval. No es una falsificación moderna.",
        "El historiador Eamon Duffy señala que usó al menos catorce pieles de ternero, un lujo imposible para un falsificador moderno.",
    ]},
    {"id": "duenos", "frases": [
        "Su rastro se pierde en el pasado.",
        "En mil seiscientos treinta y nueve, un alquimista de Praga, Georg Baresch, le pidió ayuda para leerlo al sabio jesuita Atanasio Kircher.",
        "No se sabe si Kircher respondió. Lo que sí parece es que quiso quedarse con el libro.",
        "Años después, otra carta asegura que antes lo había comprado el emperador Rodolfo Segundo, por seiscientos ducados de oro.",
    ]},
    {"id": "intentos", "frases": [
        "Ya en el siglo veinte, William Friedman, el criptógrafo que rompió el código japonés Púrpura, le dedicó años.",
        "Con su grupo, copió el texto línea por línea en tarjetas perforadas.",
        "No pudo descifrarlo. Su conclusión final fue que quizá era un lenguaje artificial.",
        "Y hay algo más inquietante: el texto no es ruido al azar.",
        "Sus palabras siguen patrones estadísticos parecidos a los de un idioma real.",
        "Son unas treinta y ocho mil palabras, escritas con apenas veinte o veinticinco símbolos.",
    ]},
    {"id": "teorias", "frases": [
        "Unos creen que es un código. Otros, un idioma inventado.",
        "Y otros piensan que fue un fraude medieval muy ingenioso.",
        "Ninguna teoría ha convencido a los expertos.",
    ]},
    {"id": "cierre", "post": 1.6, "frases": [
        "Hoy el manuscrito descansa en la biblioteca de libros raros de la Universidad de Yale.",
        "Cualquiera puede verlo en internet. Unos seiscientos años después, sigue guardando su secreto.",
        "¿Será un mensaje que aún no sabemos leer... o uno que nunca quiso ser leído?",
    ]},
]
