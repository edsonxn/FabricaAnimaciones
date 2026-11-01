# -*- coding: utf-8 -*-
"""Apozol: el pueblo de los dos nombres de agua (~4 min, 16:9, estilo kurzgesagt isométrico, canal Bitácora Perdida).

Pedido del usuario (11-oct-2026): «video de 4 minutos, solo de Apozol, su historia desde los inicios, como el de Juchipila; en videos
siguientes seguimos con otro pueblo por la ruta». Producción autónoma (el usuario ausente): guion → voz → escenas → música → render.
Hilo: «dos nombres de agua» (Apozol = agua espumosa; Atotonilco = en el agua caliente) → valle y caxcanes → conquista y fundación de
San Miguel Atotonilco → Mixtón → paz, frailes y papeles → haciendas y piloncillo → municipio, fiestas y la carretera que sigue.

Datos y fuentes (≥ 2 fuentes salvo nota):
  - Ubicación: SO de Zacatecas, cañón de Juchipila, sierra de Morones; cabecera a 1 265 m (Wikipedia ES); entre Juchipila (S) y Jalpa (N),
    sobre la carretera federal 54 (Paraíso Caxcan en el km 136 según programadestinosmexico.com). Municipio: 6 260 hab., cabecera 2 608 (censo 2020).
  - Nombre: náhuatl, «atl» (agua) + «pozolli» (espuma) = agua espumosa (Wikipedia ES). OTRAS versiones: «agua de maíz» (lista de municipios)
    y «camino quebrado donde hay agua» (guiaturisticamexico.com): la narración dice solo «agua espumosa».
    Atotonilco (topónimo náhuatl frecuente): «en el agua caliente» (atl + totonilli + -co).
  - Prehispánico: caxcanes, tributarios del señorío de Tlatlán (la antigua Xochipillan = Juchipila) (Imagenzac); asentamiento en la sierra de
    Morones, al poniente de la población actual (guiaturisticamexico).
  - Fundación: 1530 Cristóbal de Oñate; San Miguel Atotonilco «ocho años después» (1538) (Imagenzac; guía turística 1538; Wikipedia da 1530 y 1538
    para el templo de San Miguel); frailes Antonio de Segovia y Miguel de Bolonia ratifican la fundación con permiso del virrey Mendoza (Imagenzac,
    sin año fiable: la narración no lo fecha). Restos de un pequeño templo dedicado a Santo Santiago en las ruinas de San Miguel Atotonilco.
  - Mixtón 1540-42 (coherente con videos/juchipila): peñol entre Juchipila y Apozol; Tenamaxtli; Alvarado muere en la campaña (1541); virrey
    Mendoza con decenas de miles de aliados; el peñol cae a inicios de 1542. «Muchos se arrojaron al vacío» = tradición (guía turística, Imagenzac).
  - Virreinato: «Apozol de Santa María Magdalena», jurisdicción de Juchipila; cédula de 1597 que restituye al pueblo tierras de un capitán
    (Diego Flores de Altamirano: nombre solo si hace falta, en pantalla); 1806 primer alcalde Joaquín Pérez Gavilán, impulsa conservar el archivo
    y recuperar tierras (Imagenzac).
  - Haciendas: La Purísima (siglos XVII-XVIII; auge con caña y piloncillo en el Porfiriato); casa grande de San José de la Labor terminada en 1775
    (hoy hotel desde 1997) (Imagenzac; Wikipedia ES lista ambas). Piloncillo artesanal: típico del municipio.
  - 1863 municipalidad (gobierno de Jesús González Ortega); 1918 municipio libre; Leopoldo Estrada Borja (n. 3-nov-1881), ministro de la
    Suprema Corte 1923-1928 (Imagenzac).
  - Fiestas: Señor de la Ascensión (jueves de Ascensión; feria regional); tastoanes 23-26 de julio, día principal el 25 (Wikipedia ES, Imagenzac).
  - NO se afirma: fundación exacta, año de la ratificación de los frailes, Pueblo Mágico, ni cifras de migración.

Nombres difíciles para la voz/Whisper (ALIAS_QA tras la primera tanda): Apozol, Atotonilco, caxcanes, Tlatlán, Oñate, Mixtón, Tenamaxtli, Pérez Gavilán.
"""

TITULO = "Apozol: el pueblo de los dos nombres de agua"
ARCHIVO = "apozol"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 108
GAP = 0.3
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.65, cfg_weight=0.3, temperature=0.78)
MEZCLA = dict(musica=-22.0, sfx=-24.0)
SUBTITULOS = False
ALIAS_QA = {"cascanes": "caxcanes", "cajcanes": "caxcanes", "cazcanes": "caxcanes", "tenamaxti": "tenamaxtli", "tenamajli": "tenamaxtli",
            "tenamazti": "tenamaxtli", "tenamaztli": "tenamaxtli", "nochislan": "nochistlan", "uno": "primero", "ello": "ellos"}
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Entre Juchipila y Jalpa, a un lado de la carretera, hay un pueblo con dos nombres, y los dos hablan de agua.",
        "Uno quiere decir agua espumosa. El otro, en el agua caliente.",
        "Entre esos dos nombres cabe una historia de caxcanes, frailes y haciendas, y una guerra que estalló a pocos kilómetros.",
        "Esta es la historia de Apozol.",
    ]},
    {"id": "valle", "frases": [
        "Estamos en el suroeste de Zacatecas, en el fondo del cañón de Juchipila, a mil doscientos sesenta y cinco metros de altura.",
        "Aquí la sierra de Morones se asoma al valle, y el río Juchipila baja hacia el sur entre los cerros.",
        "Mucho antes de que llegaran los españoles, estas tierras eran de los caxcanes, un pueblo que hablaba náhuatl.",
        "Vivían en las laderas de la sierra, al poniente de donde hoy está el pueblo.",
        "Pagaban tributo al señorío de Tlatlán, el que hoy conocemos como Juchipila.",
        "Y le pusieron nombre al lugar en su lengua: Apozol, que mezcla las palabras agua y espuma.",
    ]},
    {"id": "atotonilco", "frases": [
        "Hacia mil quinientos treinta, llegó al cañón Cristóbal de Oñate, uno de los capitanes de Nuño de Guzmán, con soldados españoles y aliados indígenas.",
        "Los pueblos pasaron a ser encomiendas: tenían que pagar tributo y trabajar para un español.",
        "Unos ocho años después se fundó aquí San Miguel Atotonilco.",
        "Un nombre de arcángel y un nombre de agua caliente: atotonilco, en náhuatl, quiere decir en el agua caliente.",
        "Del primer templo, dedicado a Santiago, hoy solo quedan unas ruinas.",
        "Pero la tranquilidad duró poco.",
    ]},
    {"id": "mixton", "frases": [
        "En mil quinientos cuarenta, los abusos de las encomiendas hicieron estallar el cañón entero.",
        "Los caxcanes se levantaron en armas y se refugiaron en el peñol del Mixtón, un cerro de paredes casi verticales, entre Juchipila y Apozol.",
        "Miles de guerreros, dirigidos por Tenamaxtli, resistieron a los españoles.",
        "Hasta el conquistador Pedro de Alvarado murió en esa campaña.",
        "Tuvo que salir el propio virrey, Antonio de Mendoza, al frente de un ejército de decenas de miles de aliados.",
        "Dice la leyenda que, en pleno combate, el apóstol Santiago apareció montado en un caballo blanco para ayudar a los españoles.",
        "A principios de mil quinientos cuarenta y dos, el peñol cayó.",
        "Cuenta la tradición que muchos prefirieron lanzarse al vacío antes que rendirse.",
    ]},
    {"id": "paz", "frases": [
        "Después vino la paz, o algo que se le parecía.",
        "Los frailes franciscanos Antonio de Segovia y Miguel de Bolonia, los mismos que consiguieron el perdón de miles de caxcanes, confirmaron la fundación del pueblo.",
        "Durante el virreinato se llamó Apozol de Santa María Magdalena, y dependía de Juchipila.",
        "En mil quinientos noventa y siete, una cédula real mandó devolver al pueblo las tierras que un capitán se había quedado.",
        "Más de doscientos años después, en mil ochocientos seis, su primer alcalde, Joaquín Pérez Gavilán, impulsó que se cuidara el archivo y que se recuperaran sus tierras.",
        "Esta vez, el pueblo defendió lo suyo con papeles, no con flechas.",
    ]},
    {"id": "haciendas", "frases": [
        "En los siglos siguientes, el valle se llenó de haciendas.",
        "La Purísima levantó sus primeras construcciones entre los siglos diecisiete y dieciocho, y tuvo su mejor momento con la caña de azúcar, en tiempos del Porfiriato.",
        "En San José de la Labor, la casa grande quedó terminada en mil setecientos setenta y cinco.",
        "El jugo de la caña se hervía hasta volverse piloncillo, y todavía hoy se hace a mano.",
    ]},
    {"id": "hoy", "post": 1.2, "frases": [
        "En mil ochocientos sesenta y tres, durante el gobierno de Jesús González Ortega, Apozol alcanzó la categoría de municipalidad.",
        "Y en mil novecientos dieciocho, al terminar la Revolución, quedó constituido como municipio libre.",
        "Hoy, en la cabecera viven unas dos mil seiscientas personas, y en todo el municipio, unas seis mil.",
        "En el jardín principal, junto al templo, un laurel enorme da sombra a los vecinos, y un monumento recuerda a Benito Juárez.",
        "Cada año, en la fiesta del Señor de la Ascensión, el pueblo se llena de música, caballos y fuegos artificiales.",
        "Y en julio bailan los tastoanes, una danza que recuerda aquella guerra.",
        "Apozol es un pueblo pequeño, con dos nombres de agua y una historia que sigue corriendo.",
        "La carretera sigue hacia el norte, y el siguiente pueblo ya nos espera.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria_tramos.py): dos tramos de ~2 min unidos con fundido cruzado
LYRIA = dict(
    estilo=("Cinematic documentary score for an animated story of a small Mexican canyon town: acoustic guitar, vihuela, harp, violin, flutes, "
            "light folk percussion, orchestral strings. Warm and mysterious, then tense and dark, melodies kept low so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: a soft flute over a warm drone, water-like arpeggios on harp, curiosity building.", 5),
        "valle": ("Wide canyon landscape: slow plucked harp and strings, wind, a sense of space and time, gentle pulse.", 5),
        "atotonilco": ("Founding of a village: warm guitar and soft strings, a hint of colonial bells, then an unease creeping in.", 5),
        "mixton": ("War on the mountain: pounding war drums, brass hits, chaotic energy, then a sudden dramatic drop and silence.", 6),
        "paz": ("Fragile peace: gentle guitar and soft strings, quiet bells, small hope, a document being signed.", 4),
        "haciendas": ("Sunny hacienda life: lively folk guitar and light percussion, harvest and work, warm and rhythmic.", 5),
        "hoy": ("Warm resolving outro: the flute theme returns gently on guitar and strings, fiesta brass far away, a final soft chord.", 5),
    },
    tramos=[
        (["gancho", "valle", "atotonilco"], "Begin from silence with the soft flute. End on a held tense string note that can crossfade."),
        (["mixton", "paz", "haciendas", "hoy"], "Begin from a held tense note. Peace returns slowly. End with a natural fade-out on a final soft chord."),
    ],
)
