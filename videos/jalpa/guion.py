# -*- coding: utf-8 -*-
"""Jalpa: el pueblo que echó a su encomendero — PRUEBA de 1 min del estilo nuevo «pegatina Flow» (Bitácora Perdida, 16:9).

Pedido del usuario (20-oct-2026): siguiente pueblo de la serie de la carretera 54 (Juchipila → Apozol → Jalpa) con formato, estilo y
fórmula NUEVOS: «aprovechar Flow para crear los escenarios y una serie de personajes, elementos, etc. y usarlos para la animación tipo
pegatinas con movimiento… hojas de varios elementos con Nano Banana 2.1… incluso a 1 personaje hacerle una secuencia en la misma imagen
(caminando o cualquier acción)». Prueba de 1 minuto; si gusta, es el arranque del video completo (~4 min).
Fórmula nueva: en vez de la historia enciclopédica del pueblo, UN suceso con personajes (Petacatl contra su encomendero, 1540), el detalle
humano de los videos que rompen su media en el nicho (×28-×50, «Lo Que el Corrido Calló», «El Mundo que Fue»).

Datos y fuentes:
  - Nombre: náhuatl xalli (arena) + pan (sobre, encima) = «sobre la arena» (Wikipedia ES «Jalpa (Zacatecas)»; tesis UNAM 1939; visitmexico).
  - Caxcanes: pueblo originario del cañón (Wikipedia EN; tesis UNAM 1939: fundada en el s. XII por caxcanes venidos del norte).
  - Petacatl, señor de Jalpa (nuestrosranchos.org citando a Ernesto Juárez Frías; Wikipedia EN «chief Petacatl»).
  - Diego Hernández de Proaño, primer encomendero (1540, Wikipedia EN); encomendero de Xalpa registrado en 1556 (U. de Arizona, UAMR 238765).
  - Expulsión del encomendero por los caxcanes de Petacatl al empezar la rebelión del Mixtón (Wikipedia EN, UNA sola fuente: se dice «echaron»
    sin adornos ni cifras). Mixtón 1541-1542, Tenamaxtli (coherente con videos/juchipila y videos/apozol).
  - NO se afirma: fecha exacta de la expulsión, Pueblo Mágico, ni que Proaño sea el Fernández de Proaño de Culiacán (no confirmado).
Video completo (tramo 2, 20-oct-2026):
  - Mixtón: Alvarado herido por un caballo el 24-jun-1541, muere el 4-jul; Mendoza con 450 españoles y 30-60 mil aliados; Nochistlán cae
    el 9-nov-1541; el Mixtón a inicios de 1542 (Wikipedia EN «Mixtón War»; coherente con videos/apozol). Mendoza llega a Jalpa el
    1-ene-1542 (Enciclopedia de los Municipios, INAFED, vía Wikipedia ES «Municipio de Jalpa»; blog jalpazacatecas10).
  - Final de Petacatl: Juárez Frías (1996) dice que dejó a los sitiados del peñol de Nochistlán; Dávila Garibi (1945) lo hace hermano
    de Tenamaxtli y señor de Nochistlán (nuestrosranchos.org/node/23306) → «las crónicas no se ponen de acuerdo».
  - Templo dedicado a Santiago (1635) y nombre colonial «Santiago de Xalpa» (INAFED; jalpazacatecas10). «Volvieron a fundar» = INAFED.
  - Minas La Leonera y Monroy, «Jalpa Mineral» (INAFED; Wikipedia EN).
  - Hidalgo llega el 18-ene-1811 «ya tardeando», arenga desde el balcón de la tienda de raya de la mina La Leonera, pernocta y sale el 19
    hacia el norte (La Jornada Zacatecas, La Gualdra 468, 1-mar-2021, compilación de 5 cronistas del cañón, cita a Topete del Valle;
    INAFED). Capturado en Acatita de Baján el 21-mar-1811.
  - Jalpaíta: Ag3CuS2, descrita por Breithaupt en 1858, localidad tipo mina Leonera (Museo Mineralógico U. de Hamburgo; mindat loc-14163;
    Wikipedia EN «Jalpaite»).
  - 1864: unos 300 franceses de infantería ocupan la plaza (INAFED vía Wikipedia ES y EN; jalpazacatecas10).
  - Hoy: municipio 25 296 hab., cabecera 15 291 (INEGI 2020); santuario del Señor de Jalpa y parroquia de San Antonio (Wikipedia EN;
    visitmexico); tastoanes 20-25 de julio en Santiagos y Tuitán (Wikipedia ES; Wikipedia EN cita National Geographic); guayaba y caña
    sustituidas por agave desde los 90 (Wikipedia ES; visitmexico: campos de agave).
"""

TITULO = "Jalpa: el pueblo que echó a su encomendero"
ARCHIVO = "jalpa"
ESTILO_VISUAL = "pegatina_flow"
DURACION = None
BPM = 100
GAP = 0.3
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.65, cfg_weight=0.3, temperature=0.78)
MEZCLA = dict(musica=-22.0, sfx=-24.0)
SUBTITULOS = False
ALIAS_QA = {"cascanes": "caxcanes", "cajcanes": "caxcanes", "cazcanes": "caxcanes", "petacat": "petacatl", "petacalt": "petacatl",
            "proano": "proaño", "mixton": "mixtón", "uno": "primero",
            "halpa": "jalpa",          # Whisper escribe «Halpa» por la jota suave del español de México (se oye bien)
            "petacatel": "petacatl", "petacatil": "petacatl",   # la «tl» final con la vocal de apoyo del español (como «náhuatel»)
            "tenamaxti": "tenamaxtli", "tenamajli": "tenamaxtli", "tenamazti": "tenamaxtli", "tenamaztli": "tenamaxtli",
            "tenamasti": "tenamaxtli", "tenamastí": "tenamaxtli", "tenamaxtile": "tenamaxtli", "tenamazli": "tenamaxtli",
            "kaxkanes": "caxcanes",
            "jalpaita": "jalpaíta", "halpaita": "jalpaíta", "halpaíta": "jalpaíta", "tastuanes": "tastoanes",
            "calderon": "calderón", "penoles": "peñoles", "monrroy": "monroy"}
# Solo para el TTS (Chatterbox): la «tl» final de Petacatl salía «Petacatal / Petacátel / Petacatiri» (20-oct-2026)
FONETICA = {"Petacatl": "Petácatl", "Xalpa": "Jalpa"}
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Hay un pueblo en el cañón de Juchipila que lleva en el nombre la arena de su río.",
        "Y hace casi quinientos años, su gente hizo lo que muy pocos se atrevían: echar a un conquistador.",
        "Esta es la historia de Jalpa.",
    ]},
    {"id": "arena", "frases": [
        "Su nombre viene del náhuatl, y quiere decir sobre la arena.",
        "Aquí, junto al río, vivían los caxcanes, en un señorío que gobernaba un señor llamado Petacatl.",
        "Sembraban maíz, frijol y calabaza en las orillas del río.",
    ]},
    {"id": "encomienda", "frases": [
        "Hacia mil quinientos cuarenta, los españoles entregaron Jalpa en encomienda a Diego Hernández de Proaño.",
        "Los caxcanes debían pagarle tributo y trabajar para él.",
    ]},
    {"id": "rebelion", "post": 1.2, "frases": [
        "Pero ese mismo año, el cañón entero empezó a levantarse.",
        "Y Petacatl y su gente echaron al encomendero de Jalpa.",
        "Era el comienzo de la guerra del Mixtón. Y Jalpa la iba a pagar cara.",
    ]},
    # ---- video completo (tramo 2, 20-oct-2026) ----
    {"id": "mixton", "frases": [
        "Los caxcanes se hicieron fuertes en los peñoles, cerros de paredes casi verticales, guiados por Tenamaxtli.",
        "En mil quinientos cuarenta y uno, el conquistador Pedro de Alvarado subió a atacarlos. Un caballo le cayó encima, y murió días después.",
        "Entonces vino el mismísimo virrey, Antonio de Mendoza, con cuatrocientos cincuenta españoles y decenas de miles de aliados indígenas.",
        "Peñol tras peñol, la resistencia cayó. Y el primer día de mil quinientos cuarenta y dos, el virrey entró en Jalpa.",
        "Del final de Petacatl, las crónicas no se ponen de acuerdo.",
    ]},
    {"id": "santiago", "frases": [
        "Después de la guerra, los españoles volvieron a fundar el pueblo.",
        "Le levantaron un templo a Santiago, el santo de los conquistadores, y durante la colonia se llamó Santiago de Xalpa.",
        "Los caxcanes que sobrevivieron se mezclaron con los recién llegados. Y sobre la misma arena nació otro pueblo.",
    ]},
    {"id": "mineral", "frases": [
        "Pero debajo de los cerros había algo más: plata.",
        "Las minas de La Leonera y de Monroy dieron tanto que al municipio le decían Jalpa Mineral.",
        "Por los caminos del cañón subían y bajaban mulas cargadas de mineral.",
    ]},
    {"id": "hidalgo", "frases": [
        "En enero de mil ochocientos once, el cura Miguel Hidalgo venía huyendo. Acababa de perder la batalla de Puente de Calderón.",
        "Subió por el cañón con lo que le quedaba de ejército, y el dieciocho de enero llegó a Jalpa ya tardeando.",
        "Según los cronistas del cañón, le habló a la gente desde el balcón de la tienda de raya de la mina La Leonera.",
        "Durmió aquí, y al amanecer siguió hacia el norte. Dos meses después lo capturaron.",
    ]},
    {"id": "franceses", "frases": [
        "En mil ochocientos cincuenta y ocho, un mineralogista alemán describió una piedra nueva sacada de La Leonera, de plata y cobre.",
        "La llamó jalpaíta. Y el nombre de este pueblo quedó en los libros de mineralogía.",
        "Seis años después llegaron otros extranjeros: unos trescientos soldados franceses ocuparon la plaza de Jalpa.",
    ]},
    {"id": "hoy", "post": 1.5, "frases": [
        "Hoy, Jalpa es la cabecera de un municipio de unos veinticinco mil habitantes, en el sur de Zacatecas, sobre la carretera cincuenta y cuatro.",
        "Sus calles empedradas suben al santuario del Señor de Jalpa y a la parroquia de San Antonio.",
        "En julio, en sus comunidades bailan los tastoanes, con máscaras de madera: una danza que recuerda la guerra contra los conquistadores.",
        "El cañón que antes se llenaba de guayabos y caña hoy se llena de agave.",
        "Y la arena del río sigue ahí, como hace casi quinientos años.",
        "Esto fue Bitácora Perdida. La carretera sigue: ¿qué pueblo visitamos después?",
    ]},
]

TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Cinematic documentary score for an animated cut-out story of a small Mexican canyon town in 1540: acoustic guitar, harp, "
            "clay flutes, soft huehuetl and teponaztli drums, low strings. Warm and earthy at first, then tense and dark, melodies kept low "
            "so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: wind over sand, a lone clay flute over a warm drone, curiosity building.", 5),
        "arena": ("Peaceful river valley: harp and guitar arpeggios, gentle hand drums, daily life.", 4),
        "encomienda": ("Spanish arrival: a cold brass-like low string motif, heavier steps, unease.", 6),
        "rebelion": ("Uprising: war drums build, rising strings, ends on a dark held chord.", 8),
        "mixton": ("War on the mountain fortresses: pounding huehuetl war drums, low brass-like strings, chaos, then a sudden drop to a lonely flute.", 9),
        "santiago": ("Aftermath and rebirth: a slow church-bell-like harp motif, guitar and flute blending, sad but hopeful.", 4),
        "mineral": ("Silver mines: steady rhythmic percussion like picks on rock, guitar ostinato, mule-train trot, industrious.", 5),
        "hidalgo": ("1811 insurgent retreat at dusk: tired snare-like drum, solemn strings, a heroic but weary melody.", 6),
        "franceses": ("A curious discovery turning into foreign occupation: delicate plucked harp, then a cold military drum and a distant European march feel.", 6),
        "hoy": ("Today: warm festive Mexican small-town feeling, guitar, harp, soft flutes and dance drums, nostalgic, ending in a gentle resolved chord.", 4),
    },
    tramos=[
        (["gancho", "arena", "encomienda", "rebelion", "mixton", "santiago"],
         "Begin from silence with the clay flute. The war in the middle is the loudest part. End softly on the sad, hopeful harp motif."),
        (["mineral", "hidalgo", "franceses", "hoy"],
         "Begin from a soft held note, build the mining rhythm. End with a warm resolved chord and a natural fade-out."),
    ],
)

# Ficha de estilo para TODAS las imágenes de Flow (escenarios y hojas): mismo trazo y paleta para que las pegatinas casen con los fondos.
FICHA = dict(
    estilo=("Hand-painted 2D cut-out animation art, children's history picture book style: clean dark-brown ink outlines, flat gouache "
            "colors with soft painted shading and visible paper grain, warm earthy palette (ochre, terracotta, sand, sage green, deep teal "
            "river, dusk violet), southwestern Mexico, Caxcan people of the Juchipila canyon in the year 1540"),
    cierre=" No text, no letters, no watermark.",
)
