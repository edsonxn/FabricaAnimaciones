# -*- coding: utf-8 -*-
"""Neandertales: 7 mitos que la ciencia ya derrumbó — estilo doodle (sin psicodelia), ~3:00, voz de Dan.
Datos verificados; las fuentes aparecen en pantalla y en la descripción. Números de la narración en palabras.
Cambios de escena alternados: suaves (persianas, ola, iris, burbujas) y de cámara continua (paneo, bajada, zoom_suave)."""

TITULO = "Neandertales: 7 mitos que la ciencia ya derrumbó"
ARCHIVO = "neandertales_7_mitos"
ESTILO_VISUAL = "doodle"
DURACION = None
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.0)     # narración casi continua: fondo un poco más bajo
TRANSICIONES = [("persianas", 0.8), ("paneo", 1.1), ("ola", 0.85), ("bajada", 1.1),
                ("iris", 1.0), ("zoom_suave", 1.1), ("burbujas", 0.9), ("paneo", 1.1)]
MUSICA = {
    "intro": dict(sabor="build"), "torpes": dict(sabor="funk"), "joyas": dict(sabor="brillo"),
    "cuidado": dict(sabor="lounge"), "dieta": dict(sabor="flauta"), "genes": dict(sabor="dub"),
    "extincion": dict(sabor="epico"), "habla": dict(sabor="reloj"), "cierre": dict(sabor="final"),
}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "Te dijeron que los neandertales eran brutos y torpes.",
            "Pero su cerebro era, en promedio, más grande que el tuyo.",
            "Aquí van siete mitos que la ciencia ya derrumbó.",
        ],
    },
    {
        "id": "torpes", "num": 1, "titulo": "ERAN TORPES", "fase_b": 4, "etiqueta_numero": "MITO",
        "sello": "HACE ~200.000 AÑOS", "icono": "fuego", "icono_hoy": "pegamento",
        "dato": "Alquitrán de abedul en lascas de Campitello (Italia): ~200.000 años",
        "fuente": "Mazza et al. 2006, J. Archaeological Science",
        "frases": [
            "Mito uno: eran torpes.",
            "Falso. Hace unos doscientos mil años, en Italia, ya usaban pegamento hecho con alquitrán de abedul.",
            "Lo obtenían calentando corteza, y con él pegaban piedras afiladas a mangos de madera.",
            "En el Mar del Norte apareció una herramienta de hace cincuenta mil años, todavía con su pegamento.",
            "Tú pegas cosas con un tubito. Ellos ya tenían su propia versión.",
        ],
    },
    {
        "id": "joyas", "num": 2, "titulo": "NO USABAN JOYAS", "fase_b": 4, "etiqueta_numero": "MITO",
        "sello": "HACE ~130.000 AÑOS", "icono": "collar", "icono_hoy": "tu",
        "dato": "Ocho garras de águila de Krapina (Croacia): ~130.000 años",
        "fuente": "Radovčić et al. 2015, PLOS ONE",
        "frases": [
            "Mito dos: no usaban joyas.",
            "Falso. En Krapina, en Croacia, aparecieron ocho garras de águila de hace unos ciento treinta mil años.",
            "Tienen cortes y partes pulidas, como si las hubieran colgado de un collar.",
            "Sería la joyería más antigua de Europa, hecha decenas de miles de años antes de que llegaran los humanos modernos.",
            "Tú te pones un collar para verte bien. Ellos ya lo hacían.",
        ],
    },
    {
        "id": "cuidado", "num": 3, "titulo": "NO CUIDABAN A LOS SUYOS", "fase_b": 3, "etiqueta_numero": "MITO",
        "sello": None, "icono": "corazon", "icono_hoy": "bebe",
        "dato": "Shanidar 1 (Irak): sobrevivió con graves lesiones hasta los cuarenta y tantos",
        "fuente": "Trinkaus y Villotte 2017, PLOS ONE",
        "frases": [
            "Mito tres: no cuidaban a los suyos.",
            "Falso. En la cueva de Shanidar, en Irak, vivió un neandertal con un brazo atrofiado, cojera y sordera.",
            "Aun así llegó a los cuarenta y tantos años, y los investigadores creen que su grupo lo cuidó.",
            "Y en Cova Negra, en España, un pequeño con síndrome de Down vivió al menos seis años.",
            "Cuidar a quien lo necesita no lo inventamos nosotros.",
        ],
    },
    {
        "id": "dieta", "num": 4, "titulo": "SOLO COMÍAN CARNE", "fase_b": 3, "etiqueta_numero": "MITO",
        "sello": "HACE ~49.000 AÑOS", "icono": "flor", "icono_hoy": "pastilla",
        "dato": "Sarro de El Sidrón (España): piñones, musgo, álamo y Penicillium",
        "fuente": "Weyrich et al. 2017, Nature",
        "frases": [
            "Mito cuatro: solo comían carne.",
            "Falso. En el sarro de un neandertal del Sidrón, en España, quedaron restos de piñones, musgo y hongos.",
            "Otro tenía un absceso en la muela, y su sarro guarda rastros de álamo, un analgésico natural, y del moho que produce penicilina.",
            "Tú abres el botiquín cuando te duele una muela. Él tenía el bosque.",
        ],
    },
    {
        "id": "genes", "num": 5, "titulo": "NO DEJARON DESCENDIENTES", "fase_b": 3, "etiqueta_numero": "MITO",
        "sello": None, "icono": "adn", "icono_hoy": "tu",
        "dato": "Genoma neandertal en personas con ancestros no africanos: 1–4 %",
        "fuente": "Green et al. 2010, Science",
        "frases": [
            "Mito cinco: no dejaron descendientes.",
            "Falso. Nuestros ancestros tuvieron hijos con ellos, y esos hijos sobrevivieron.",
            "Por eso, si tus antepasados vienen de fuera de África, entre el uno y el cuatro por ciento de tu genoma es neandertal.",
            "No desaparecieron del todo: una parte de ellos sigue en ti.",
        ],
    },
    {
        "id": "extincion", "num": 6, "titulo": "SE EXTINGUIERON POR DÉBILES", "fase_b": 4, "etiqueta_numero": "MITO",
        "sello": "HACE ~40.000 AÑOS", "icono": "mamut", "icono_hoy": "reloj",
        "dato": "Últimos neandertales de Europa: hace ~40.000 años",
        "fuente": "Higham et al. 2014, Nature",
        "frases": [
            "Mito seis: se extinguieron por débiles.",
            "Falso. Su linaje duró más de trescientos mil años, aguantando glaciaciones.",
            "Desaparecieron hace unos cuarenta mil años, después de convivir con nuestros ancestros durante algunos miles de años.",
            "Todavía se debate por qué: clima, enfermedades, competencia o mezcla con nuestra especie.",
            "Nuestra especie lleva más o menos el mismo tiempo. Nadie llama fracaso a eso.",
        ],
    },
    {
        "id": "habla", "num": 7, "titulo": "NO SABÍAN HABLAR", "fase_b": 3, "etiqueta_numero": "MITO",
        "sello": None, "icono": "neandertal", "icono_hoy": "chat",
        "dato": "Oído de neandertales y humanos actuales: capacidad similar",
        "fuente": "Conde-Valverde et al. 2021, Nature Ecology & Evolution",
        "frases": [
            "Mito siete: no sabían hablar.",
            "Falso. Al escanear el oído de varios neandertales, los científicos vieron que oían un rango de sonidos muy parecido al nuestro.",
            "Según sus autores, tenían capacidad para una comunicación hablada tan eficiente como la nuestra.",
            "Hoy mandas audios de un minuto. Ellos ya tenían el oído para escucharlos.",
        ],
    },
    {
        "id": "cierre",
        "cierre": "¿CUÁL CREÍAS?",
        "frases": [
            "Así que si alguien te llama neandertal, tómalo como un cumplido.",
            "Tenían cerebro grande, herramientas, joyas, medicinas y compasión.",
            "¿Cuál de estos mitos creías tú?",
        ],
    },
]
