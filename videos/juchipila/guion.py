# -*- coding: utf-8 -*-
"""Juchipila: el lugar de las flores nobles (~8 min, 16:9, estilo kurzgesagt, canal Bitácora Perdida).

BORRADOR 1 (4-oct-2026) — pendiente de aprobación del usuario ANTES de generar voz (docs/voz.md §1).
Hilo: nombre/paisaje -> Las Ventanas -> caxcanes -> conquista -> Guerra del Mixtón -> castigo y refundación
-> Tenamaxtli ante el Consejo de Indias -> Revolución (Crispín Robles) -> hoy (fiestas que sobreviven).

Datos y fuentes (verificados con ≥ 2 fuentes salvo nota):
  - Nombre: náhuatl Xochipillan/Xuchipilan, «lugar de flores nobles/hermosas» (Wikipedia ES y EN; Imagen Zac).
  - Ubicación: SO de Zacatecas, ~160 km de la capital; cabecera a 1 249 m; río Juchipila (afluente del Río Grande de Santiago);
    Sierra de Morones al oeste, Sierra de Nochistlán al este (Wikipedia EN). 12 251 hab. (censo 2020), cabecera 5 836; mucha
    emigración a EE. UU., remesas importantes (Wikipedia EN). Cultivo: maíz.
  - Cerro de las Ventanas (INAH; La Jornada 2019; El Sol de Zacatecas): mayor desarrollo cultural del cañón, apogeo 700-1200 d. C.
    (Epiclásico), ~116 ha, ciudadela fortificada arriba, pirámide monumental, juego de pelota, 25 monolitos circulares, muro de
    piedra con huecos «ventanas» en el risco; ocupado al final por caxcanes (náhuatl); abierto al público el 2-ago-2019.
    Primeras investigaciones: Aleš Hrdlička (1898, 1902). En el siglo XVI se llamaba Tlaltan/Tlatlan (Wikipedia EN).
  - Caxcanes: llegada s. XII-XIII desde el norte (Tuitlán/La Quemada) [fuentes dan «≈1170» y «siglo XIII»: se dice «entre los siglos
    doce y trece»]. Fiesta de Xúchitl (junio, cerca del solsticio y la entrada de lluvias; Xochipilli, dios de flores, música y danza;
    patrimonio cultural intangible de Zacatecas 2015). Tastoanes: fiestas de Santiago (finales de julio); se asocian a la memoria del Mixtón.
  - Conquista: Nuño de Guzmán (1529-31; 300-400 españoles y 5 000-8 000 aliados indígenas); Cristóbal de Oñate toma Tlaltan hacia 1530-31.
    Encomienda: la Corona entrega pueblos a españoles para cobrar tributo y trabajo.
  - Rebelión 1540-41: Tlaltenango, Juchipila, Nochistlán; muerte del encomendero Juan de Arce y de dos sacerdotes; refugio en el peñol del
    Mixtón (entre Juchipila y Apozol); mensajeros anuncian el regreso de los dioses antiguos y que «los viejos serán mozos»; jefe: Tenamaxtli
    (hijo del señor de Nochistlán). Oñate fracasa.
  - Pedro de Alvarado ataca en junio de 1541 con ~400 españoles + aliados; el 24-jun un caballo cae sobre él en la retirada; muere el 4-jul-1541 en
    Guadalajara. [Las fuentes difieren en si fue en el Mixtón o en el peñol de Nochistlán: la narración no nombra el sitio.] Septiembre de 1541:
    los rebeldes atacan Guadalajara y son rechazados.
  - Virrey Antonio de Mendoza sale con cientos de españoles y «decenas de miles» de aliados (tlaxcaltecas, mexicas, tarascos) [20 000 a 60 000
    según la fuente]; 9-nov-1541 cae Nochistlán, Tenamaxtli escapa; el Mixtón cae a finales de 1541 / inicios de 1542 [dicen «dic-1541» y «1542»].
  - Castigo: ejecuciones con cañón, perros (aperreamiento) y espada; miles encadenados a las minas; pueblos arruinados.
  - Refundación: fray Antonio de Segovia y fray Miguel de Bolonia consiguen el perdón de ~6 000 caxcanes que bajan de paz; Juchipila se
    refunda hacia 1542-43. Templo de San Francisco de Asís, 1627. Alcaldía mayor de la Nueva Galicia 1548-1786; pasa a la Intendencia de
    Zacatecas en 1804.
  - Tenamaxtli: guerrillero hasta ~1550; identificado ago-1552; enviado a España; llega a Valladolid mayo de 1554; con ayuda de Bartolomé de
    las Casas presenta su memorial al Consejo de Indias el 1-jul-1555 (libertad de su pueblo, fin de la encomienda); muere en Valladolid hacia 1556.
  - Revolución: Crispín Robles Villegas, comerciante («El Nuevo Mundo»); Club Antirreeleccionista «Gral. Antonio Rosales» (1909); preso por
    sedición días después del inicio de la Revolución (Lecumberri); se alza el 15-abr-1913; coronel de caballería en la brigada de Pánfilo
    Natera; muere el 14-mar-1914 en Ocotlán, Jalisco (Alejandro Rosas; Wikipedia ES). Toma de Zacatecas: 23-jun-1914 (Villa y Natera).
  - NO se afirma que Juchipila sea «Pueblo Mágico»: las fuentes consultadas se contradicen.

Nombres difíciles para la voz/Whisper (se resuelven con ALIAS_QA tras la primera tanda): caxcanes, Tenamaxtli, Mixtón, Nochistlán, Oñate, Xochipilli
(el usuario pidió, 4-oct-2026, que la narración diga «Xochipilli»). Solo en pantalla: «Xochipillan», «Fiesta de Xúchitl».
"""

TITULO = "Juchipila: el lugar de las flores nobles"
ARCHIVO = "juchipila"
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
# Colas de voz que decaen a silencio (verificado en la envolvente) pero superan el umbral por defecto de 0,35
TAIL_MAX_POR_FRASE = {"hartazgo_3": 0.70, "hartazgo_5": 0.50}
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Hay un pueblo en Zacatecas con nombre de flor. Se llama Juchipila, y en náhuatl quiere decir lugar de flores nobles.",
        "Pero hace casi quinientos años, este valle tranquilo fue el centro de una de las rebeliones indígenas más grandes de la Conquista.",
        "Una guerra que estuvo a punto de borrar a un pueblo entero: los caxcanes.",
        "Esta es la historia de Juchipila. La de las flores, y la de la guerra.",
    ]},
    {"id": "canon", "frases": [
        "Para entenderla, primero hay que mirar el paisaje. Estamos en el suroeste de Zacatecas, a unos ciento sesenta kilómetros de la capital del estado.",
        "Aquí las montañas se abren para dejar pasar un río, el río Juchipila, que va hacia el sur y termina en el Río Grande de Santiago.",
        "A un lado se levanta la sierra de Morones, y al otro, la sierra de Nochistlán.",
        "El pueblo está a mil doscientos cincuenta metros de altura, en el fondo de un cañón largo y estrecho, donde el río lleva agua y la tierra da maíz.",
        "Ese cañón es un corredor natural. Por él han pasado pueblos enteros, y siglos después, el primer camino real entre Guadalajara y Zacatecas.",
    ]},
    {"id": "ventanas", "frases": [
        "Mucho antes de que llegaran los españoles, alguien eligió un cerro de este cañón para construir una ciudad: el cerro de las Ventanas.",
        "Los arqueólogos calculan que su mejor momento fue entre los años setecientos y mil doscientos de nuestra era.",
        "Arriba, una ciudadela fortificada. Más abajo, terrazas con casas, una pirámide monumental, un juego de pelota y veinticinco monolitos circulares.",
        "Todo ocupa unas ciento dieciséis hectáreas. Es el desarrollo cultural más grande que se conoce en el cañón.",
        "Los primeros en estudiarlo fueron investigadores extranjeros, a finales del siglo diecinueve. Desde entonces, cada excavación revela más piedra tallada.",
        "Su nombre viene de un muro de piedra con huecos, construido sobre el risco más alto. Desde lejos, parecen ventanas abiertas en la montaña.",
        "Y durante siglos, casi nadie pudo visitarlo: la zona arqueológica se abrió al público hasta el dos de agosto de dos mil diecinueve.",
    ]},
    {"id": "caxcanes", "frases": [
        "Los últimos en habitar la ciudad fueron los caxcanes, un pueblo que hablaba náhuatl.",
        "Llegaron al cañón desde el norte, entre los siglos doce y trece, y formaron un señorío con capital en la ciudad de la montaña.",
        "Tenían fortalezas en los cerros, juegos de pelota, y una fiesta al año para Xochipilli, el dios de las flores, la música y la danza.",
        "Se celebraba cerca del solsticio de verano, cuando empiezan las lluvias y el cañón se llena de verde.",
        "De ahí viene el nombre del pueblo: el lugar de las flores nobles.",
        "Esa fiesta no se perdió. Cada junio, Juchipila la sigue celebrando, y desde dos mil quince es patrimonio cultural de Zacatecas.",
    ]},
    {"id": "llegada", "frases": [
        "Pero alrededor de mil quinientos treinta, todo cambió.",
        "Nuño de Guzmán, un gobernador español de fama cruel, cruzó el occidente de México con cientos de soldados y miles de aliados indígenas.",
        "Dejó tras de sí pueblos quemados y miles de personas esclavizadas.",
        "Uno de sus capitanes, Cristóbal de Oñate, llegó al cañón y derrotó a los defensores de la capital caxcana.",
        "Después vino el reparto. Los españoles recibieron pueblos enteros en encomienda: la Corona les entregaba a la gente para que les pagara tributo y trabajara para ellos.",
    ]},
    {"id": "hartazgo", "frases": [
        "Durante diez años, los pueblos del cañón pagaron tributos, trabajaron para sus nuevos amos y vieron cómo derribaban sus templos.",
        "A los abusos de los encomenderos se sumó la presión de los frailes, que querían obligarlos a abandonar sus antiguas creencias.",
        "La tensión crecía, como el agua en una olla tapada.",
        "Entonces empezaron a correr mensajes. Emisarios iban de pueblo en pueblo con una promesa: los dioses antiguos volverían, y los ancianos recuperarían la juventud.",
        "Hacia mil quinientos cuarenta, los caxcanes se levantaron: en Tlaltenango, en Nochistlán y en Juchipila.",
        "Mataron a un encomendero y a dos sacerdotes. Y después se refugiaron en lo alto de un peñol, un cerro de paredes casi verticales: el Mixtón.",
    ]},
    {"id": "mixton", "frases": [
        "Los españoles intentaron aplastar la rebelión, pero fracasaron. Cristóbal de Oñate pidió ayuda a la capital.",
        "Y llegó uno de los conquistadores más temidos de América: Pedro de Alvarado, el hombre de la matanza del Templo Mayor.",
        "En junio de mil quinientos cuarenta y uno atacó con cuatrocientos españoles y sus aliados indígenas. Enfrente tenía a miles de guerreros caxcanes, dirigidos por un jefe llamado Tenamaxtli.",
        "El ataque fracasó. En la retirada, un caballo cayó sobre Alvarado y lo aplastó.",
        "Murió diez días después, el cuatro de julio, en Guadalajara.",
        "Los caxcanes se llenaron de confianza. Atacaron incluso Guadalajara, pero no lograron tomarla.",
    ]},
    {"id": "mendoza", "frases": [
        "El virrey de la Nueva España, Antonio de Mendoza, comprendió que se jugaba todo el occidente. Y salió él mismo al frente del ejército.",
        "Reunió a cientos de soldados españoles y a decenas de miles de aliados indígenas: tlaxcaltecas, mexicas y tarascos.",
        "El nueve de noviembre de mil quinientos cuarenta y uno cayó Nochistlán. Pero Tenamaxtli logró escapar.",
        "Los rebeldes se habían hecho fuertes en dos peñoles: el de Nochistlán y el del Mixtón.",
        "Entonces el ejército se dirigió al Mixtón. Lo rodeó, lo asedió, y a principios de mil quinientos cuarenta y dos, el peñol cayó.",
        "La rebelión había terminado.",
    ]},
    {"id": "castigo", "frases": [
        "Lo que siguió fue brutal. Muchos prisioneros fueron ejecutados con cañones, con perros y con espadas.",
        "Miles de personas fueron encadenadas y llevadas a las minas como esclavas.",
        "Los pueblos del cañón quedaron en ruinas, y los sobrevivientes huyeron a la sierra.",
        "Un pueblo que había levantado ciudades en los cerros, ahora vivía escondido entre ellos.",
        "La crueldad de la represión fue tal, que años después el Consejo de Indias abrió una investigación secreta sobre la conducta del propio virrey.",
        "Lo que quedó de los caxcanes tuvo que decidir si se quedaba escondido en la sierra, o si volvía a bajar al valle.",
    ]},
    {"id": "refundacion", "frases": [
        "Fue entonces cuando intervinieron dos frailes franciscanos: fray Antonio de Segovia y fray Miguel de Bolonia.",
        "Consiguieron que el virrey perdonara a unos seis mil caxcanes, que bajaron de paz desde el peñol.",
        "Con ellos se refundó Juchipila, entre mil quinientos cuarenta y dos y mil quinientos cuarenta y tres.",
        "Los franciscanos levantaron su convento, y el templo de San Francisco de Asís es de mil seiscientos veintisiete.",
        "Durante la Colonia, Juchipila fue cabeza de una alcaldía mayor de la Nueva Galicia, de mil quinientos cuarenta y ocho a mil setecientos ochenta y seis.",
        "Pasaron los siglos. Y, cuando empezó la Independencia, los descendientes de caxcanes y de españoles se sumaron a los insurgentes.",
    ]},
    {"id": "tenamaxtli", "frases": [
        "¿Y Tenamaxtli? Era hijo del señor de Nochistlán, y cacique de Nochistlán y de Juchipila.",
        "Pasó casi diez años huyendo como guerrillero, por las sierras de la región.",
        "Hacia mil quinientos cincuenta y dos lo identificaron, y las autoridades decidieron enviarlo a España, para juzgarlo.",
        "En Valladolid conoció a fray Bartolomé de las Casas, el famoso defensor de los indígenas.",
        "Con su ayuda, redactó una denuncia ante el Consejo de Indias: pedía la libertad de su pueblo y el fin de la encomienda.",
        "La presentó el primero de julio de mil quinientos cincuenta y cinco. Un jefe rebelde, pidiendo justicia ante la Corona.",
        "Murió en Valladolid, hacia mil quinientos cincuenta y seis, sin volver a su tierra.",
    ]},
    {"id": "revolucion", "frases": [
        "Cuatro siglos después, Juchipila volvió a levantarse.",
        "En mil novecientos nueve, un comerciante del pueblo, Crispín Robles, fundó un club antirreeleccionista para apoyar a Francisco Madero.",
        "Días después de que empezara la Revolución, lo arrestaron por sedición y lo llevaron a la penitenciaría de la Ciudad de México.",
        "Cuando asesinaron a Madero, el quince de abril de mil novecientos trece, Robles se levantó en armas.",
        "Llegó a coronel de caballería en la brigada del general Pánfilo Natera.",
        "Murió en combate, en marzo de mil novecientos catorce, en Ocotlán, Jalisco. Tres meses después, Villa y Natera tomaban Zacatecas.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Hoy, Juchipila tiene poco más de doce mil habitantes. Muchos de sus hijos se han ido a Estados Unidos, y el dinero que mandan sostiene a muchas familias.",
        "Pero cada junio, el pueblo se llena de flores, como hace mil años. Y cada julio, en las fiestas de Santiago, los vecinos bailan los tastoanes, y recuerdan la guerra contra los invasores.",
        "Juchipila: el lugar de las flores nobles. Un nombre hermoso, para un pueblo que sobrevivió a una guerra.",
        "¿Qué otro pueblo de México quieres que contemos? Cuéntamelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria.py): mexicana de época, con huecos para la voz
LYRIA = dict(
    estilo=("Cinematic documentary score for an animated story of a Mexican canyon town: acoustic guitar, vihuela, harp, violin, flutes, "
            "light folk percussion, orchestral strings. Warm and mysterious, then tense and dark, melodies kept low so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: a soft flute over a warm drone, curiosity building, then a gentle pulsing rhythm.", 5),
        "canon": ("Wide landscape: slow plucked harp and strings, wind, a sense of space and time.", 6),
        "ventanas": ("Ancient city: mysterious flutes, deep soft drums, wonder and awe, a slow ascending theme.", 6),
        "caxcanes": ("Festival of flowers: light joyful folk percussion, flutes and plucked strings, warm and communal.", 6),
        "llegada": ("Invasion: low ominous drums, a dissonant string rise, a sudden cold silence, unease.", 6),
        "hartazgo": ("Pressure building: ticking pulse, tense whispering strings, a restless crescendo.", 6),
        "mixton": ("War on the mountain: pounding war drums, brass hits, chaotic energy, then a sudden dramatic drop.", 6),
        "mendoza": ("A great army marches: heavy martial drums, determined strings and brass, inexorable.", 6),
        "castigo": ("Aftermath and sorrow: low mournful cello, slow somber march, a long dark final note.", 5),
        "refundacion": ("A fragile new beginning: a gentle guitar and soft strings, small hope, quiet bells.", 6),
        "tenamaxtli": ("Solemn dignity: a lone guitar and soft strings, a proud sad theme, hopeful at the end.", 6),
        "revolucion": ("Revolution: rhythmic snare, trumpets, a heroic and bittersweet folk march.", 6),
        "cierre": ("Warm resolving outro: the flute theme returns gently on guitar and strings, flowers blooming, a final soft chord.", 5),
    },
    # Lyria da ~3 min por pieza: 4 tramos (nucleo/lyria_tramos.py) unidos con fundido cruzado
    tramos=[
        (["gancho", "canon", "ventanas"], "Begin from silence with the soft flute. End on a sustained warm chord that can crossfade."),
        (["caxcanes", "llegada", "hartazgo"], "Begin softly from a sustained chord. End on a held tense string note that can crossfade."),
        (["mixton", "mendoza", "castigo"], "Begin from a held tense note. End on a long dark low note that can crossfade."),
        (["refundacion", "tenamaxtli", "revolucion", "cierre"], "Begin quietly from a low note. End with a natural fade-out on a final soft chord."),
    ],
)
