# -*- coding: utf-8 -*-
"""7 inventos antiguos que usas todos los días — estilo recortes de papel, 3:00, voz de Dan.
Datos verificados; las fuentes aparecen en pantalla. Números de la narración escritos en palabras."""

TITULO = "7 inventos antiguos que usas todos los días"
ARCHIVO = "7_inventos_antiguos"
ESTILO_VISUAL = "recortes"
DURACION = 180.0
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
# transiciones suaves (nada psicodélico)
TRANSICIONES = [("persianas", 0.8), ("ola", 0.85), ("iris", 1.0), ("mancha", 0.8), ("burbujas", 0.9),
                ("zoom", 0.9), ("persianas", 0.8), ("iris", 1.0)]
MUSICA = {
    "intro": dict(sabor="brillo"), "pan": dict(sabor="funk"), "espejo": dict(sabor="lounge"),
    "rueda": dict(sabor="disco"), "escritura": dict(sabor="flauta"), "bano": dict(sabor="dub"),
    "horas": dict(sabor="reloj"), "monedas": dict(sabor="epico"), "cierre": dict(sabor="brillo"),
}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "Crees que vives en el futuro, pero usas inventos de hace miles de años.",
            "Algunos son incluso más viejos que las pirámides de Egipto.",
            "Aquí van siete que tocas todos los días, sin saber lo antiguos que son.",
        ],
    },
    {
        "id": "pan", "num": 1, "titulo": "EL PAN", "fase_b": 4,
        "sello": "HACE ~14.400 AÑOS", "icono": "pan", "icono_hoy": "tostada",
        "dato": "Pan de Shubayqa 1 (Jordania): ~14.400 años",
        "fuente": "Arranz-Otaegui et al. 2018, PNAS",
        "frases": [
            "Número uno: el pan.",
            "En el noreste de Jordania encontraron restos de pan plano quemado de hace unos catorce mil cuatrocientos años.",
            "Lo hicieron cazadores recolectores, miles de años antes de que existiera la agricultura.",
            "Usaron cereales silvestres y tubérculos de junco, molidos a mano.",
            "Tu tostada del desayuno tiene una receta prehistórica: harina, agua y fuego.",
        ],
    },
    {
        "id": "espejo", "num": 2, "titulo": "EL ESPEJO", "fase_b": 3,
        "sello": "HACE ~8.000 AÑOS", "icono": "espejo_obsidiana", "icono_hoy": "telefono",
        "dato": "Espejos de obsidiana de Çatalhöyük (Turquía): ~8.000 años",
        "fuente": "Museo de las Civilizaciones de Anatolia, Ankara",
        "frases": [
            "Número dos: el espejo.",
            "Hace unos ocho mil años, en Anatolia, pulían obsidiana, un vidrio volcánico negro, hasta que reflejaba la cara.",
            "Algunos de esos espejos aparecieron en tumbas, junto a sus dueños.",
            "Hoy te miras al espejo cada mañana, o en la cámara frontal del celular.",
        ],
    },
    {
        "id": "rueda", "num": 3, "titulo": "LA RUEDA", "fase_b": 3,
        "sello": "HACE +5.000 AÑOS", "icono": "rueda_madera", "icono_hoy": "bici",
        "dato": "Rueda de los pantanos de Liubliana (Eslovenia): ~5.150 años",
        "fuente": "Velušček et al. 2009",
        "frases": [
            "Número tres: la rueda.",
            "La rueda de madera más antigua que se conoce apareció en unos pantanos de Eslovenia, y tiene más de cinco mil años.",
            "Las primeras ruedas de vehículos movían carretas pesadas, tiradas por bueyes.",
            "Hoy la usas en el auto, en la bicicleta, en la maleta y hasta en tu silla.",
        ],
    },
    {
        "id": "escritura", "num": 4, "titulo": "LA ESCRITURA", "fase_b": 4,
        "sello": "HACE ~5.200 AÑOS", "icono": "tablilla", "icono_hoy": "chat",
        "dato": "Tablillas de Uruk (Irak): ~3200 a. C.",
        "fuente": "Nissen, Damerow y Englund 1993, Archaic Bookkeeping",
        "frases": [
            "Número cuatro: la escritura.",
            "Los primeros textos aparecieron en Uruk, en Mesopotamia, hace unos cinco mil doscientos años.",
            "Escribían presionando un junco sobre arcilla húmeda; con el tiempo, esas marcas se volvieron cuñas: la escritura cuneiforme.",
            "Y no eran poemas: eran cuentas de cebada y cerveza. Básicamente, recibos.",
            "Hoy escribes decenas de mensajes al día con el mismo invento.",
        ],
    },
    {
        "id": "bano", "num": 5, "titulo": "EL BAÑO CON DRENAJE", "fase_b": 3,
        "sello": "HACE ~4.500 AÑOS", "icono": "drenaje", "icono_hoy": "inodoro",
        "dato": "Mohenjo-Daro (Pakistán): ~2500 a. C.",
        "fuente": "Kenoyer 1998, Ancient Cities of the Indus Valley Civilization",
        "frases": [
            "Número cinco: el baño con drenaje.",
            "Hace unos cuatro mil quinientos años, en Mohenjo-Daro, en el valle del Indo, muchas casas tenían baño conectado a drenajes bajo la calle.",
            "Y esos drenajes tenían tapas que se podían levantar para limpiarlos.",
            "Hoy vas al baño sin pensarlo, y la idea tiene cuarenta y cinco siglos.",
        ],
    },
    {
        "id": "horas", "num": 6, "titulo": "LA HORA DE 60 MINUTOS", "fase_b": 3,
        "sello": "HACE ~4.000 AÑOS", "icono": "tablilla_numeros", "icono_hoy": "reloj",
        "dato": "Sistema sexagesimal babilonio: ~2000 a. C.",
        "fuente": "Neugebauer 1957, The Exact Sciences in Antiquity",
        "frases": [
            "Número seis: la hora de sesenta minutos.",
            "Los babilonios contaban en base sesenta, y de ahí vienen los sesenta minutos de cada hora y los sesenta segundos de cada minuto.",
            "Los egipcios dividieron el día y la noche en doce partes cada uno. Total: veinticuatro horas.",
            "Cada vez que miras el reloj, usas matemáticas de hace unos cuatro mil años.",
        ],
    },
    {
        "id": "monedas", "num": 7, "titulo": "LAS MONEDAS", "fase_b": 4,
        "sello": "HACE ~2.600 AÑOS", "icono": "moneda_leon", "icono_hoy": "telefono",
        "dato": "Monedas de electro de Lidia (Turquía): ~600 a. C.",
        "fuente": "Museo Británico, monedas de Lidia",
        "frases": [
            "Número siete: las monedas.",
            "Antes de ellas se comerciaba con trueque, o pesando trozos de metal.",
            "En Lidia, en la actual Turquía, hace unos dos mil seiscientos años, se acuñaron las primeras monedas, de electro, una mezcla natural de oro y plata.",
            "Muchas llevaban la cabeza de un león.",
            "Hoy pagas con el celular, pero la idea es la misma: un valor que todos aceptan.",
        ],
    },
    {
        "id": "cierre",
        "cierre": "¿CUÁL TE SORPRENDIÓ MÁS?",
        "frases": [
            "Así que la próxima vez que desayunes pan o mires la hora, recuerda algo.",
            "Estás usando tecnología con miles de años de garantía.",
            "¿Cuál de estos inventos te sorprendió más?",
        ],
    },
]
