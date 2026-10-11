# -*- coding: utf-8 -*-
"""La historia de España en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa con RELIEVE REAL que se une, se parte y se une).
Canal Cronopapel, quinto video de la serie «historia en minutos» (motor de `videos/historia_japon/`, mejorado: relieve ETOPO1 bajo el guache,
ríos de Natural Earth, varias capas de territorio a la vez (Reconquista), fractura por fronteras REALES (independencias de América) y una
segunda rejilla para el mapa de América).
Hilo narrativo: un rincón de Europa por el que pasaron todos (fenicios, romanos, godos, árabes…) y del que salió un idioma de 600 millones.

Datos y fuentes (Britannica, Real Academia de la Historia (DB~e), RAE, Instituto Cervantes, INE, UNESCO):
  - Atapuerca: restos humanos de más de 1,1-1,4 millones de años (Sima del Elefante; Nature 2008 y 2025). UNESCO.
  - Altamira: techo de los polícromos (bisontes) ~14 500-18 500 años (Magdaleniense); UNESCO 1985.
  - Íberos (costa mediterránea y sur) y celtas/celtíberos (interior y norte), Edad del Hierro (s. VIII-I a. C.).
  - Gadir (Cádiz): fundación fenicia, tradición 1104 a. C., arqueología s. IX-VIII a. C.; Emporion (Ampurias), griega (~575 a. C.).
  - Cartago Nova (Cartagena, 227 a. C.); Aníbal sale en 218 a. C. con elefantes hacia Italia (Segunda Guerra Púnica).
  - Roma: desembarco en 218 a. C.; fin de las guerras cántabras en 19 a. C. (≈200 años). Numancia cae en 133 a. C. (Escipión Emiliano).
    Trajano (n. Itálica, 53 d. C.), primer emperador nacido fuera de Italia; Adriano, de familia de Itálica.
  - Visigodos: Toledo capital (s. VI, Leovigildo); Recaredo católico (589).
  - 711: Tariq ibn Ziyad cruza el estrecho (Gibraltar < Yabal Tariq); Guadalete; hacia 718 casi toda la península bajo dominio musulmán.
    Abderramán III se proclama califa en 929; Córdoba, una de las mayores ciudades de Europa. Arroz, caña de azúcar, naranjo amargo;
    ~4 000 arabismos en español (Lapesa): aceite, almohada, azulejo, ojalá.
  - Covadonga (722, Pelayo). Fin del califato 1031: más de veinte taifas. Toledo 1085 (Alfonso VI); el Cid toma Valencia (1094);
    Navas de Tolosa (16-jul-1212); Córdoba (1236), Sevilla (1248); reino nazarí de Granada (1238-1492).
  - Isabel y Fernando se casan en 1469; Granada se rinde el 2-ene-1492; decreto de expulsión de los judíos (31-mar-1492);
    Gramática castellana de Nebrija (ago-1492); Colón sale de Palos (3-ago) y llega a Guanahaní el 12-oct-1492.
  - Cortés y sus aliados indígenas (tlaxcaltecas) toman Tenochtitlan (13-ago-1521); Pizarro captura a Atahualpa (1532).
    Epidemias (viruela) y guerra: caída demográfica de millones de indígenas. Plata de Potosí (1545) y Zacatecas (1546).
    Felipe II: «imperio donde nunca se pone el sol»; Filipinas nombradas en su honor (1543). Lepanto (1571); Gran Armada (1588).
    Bancarrotas de la corona: 1557, 1560, 1575, 1596 (y más en el s. XVII).
  - Siglo de Oro: Quijote (1605), Las Meninas (1656). Carlos II muere sin hijos (1700) → Guerra de Sucesión; Felipe V de Borbón;
    Tratado de Utrecht (1713): Gibraltar y Menorca a Gran Bretaña; se pierden Países Bajos, Milán, Nápoles y Cerdeña.
  - 1808: Napoleón pone a su hermano José en el trono; 2 de mayo; Goya (El 3 de mayo, 1814); «guerrilla» pasa a otras lenguas.
    Constitución de Cádiz, 19-mar-1812 («la Pepa»). Independencias americanas 1810-1825 (Cuba y Puerto Rico siguen hasta 1898).
    Isabel II al exilio (1868); Amadeo I abdica (1873); Primera República (feb-1873 a ene-1874, ~11 meses); 1898: guerra con EE. UU.
  - Segunda República (14-abr-1931); golpe de 1936 y Guerra Civil (1936-1939), cientos de miles de muertos; Guernica (26-abr-1937).
    Franco, dictador 1939-1975 (36 años); «desarrollismo» y turismo en los sesenta. Muere el 20-nov-1975; Juan Carlos I.
    Constitución votada el 6-dic-1978; golpe fallido del 23-F (1981); CEE (1986); Barcelona 92.
  - Hoy: ~49 millones de habitantes (INE, 2025); >90 millones de turistas internacionales (INE Frontur 2024: 93,8 M).
    Español: casi 600 millones de hablantes (Instituto Cervantes, 2024).
"""

TITULO = "La historia de España en 5 minutos"
ARCHIVO = "historia_espana_5min"
ESTILO_VISUAL = "boceto"
DURACION = None                  # duración natural (~5 min)
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)
# variantes que Whisper escribe a su manera (minúsculas, sin tildes) -> como está en el guion
ALIAS_QA = {"al andalus": "al andalus", "alandalus": "al andalus", "al-andalus": "al andalus", "tarik": "tariq", "tareq": "tariq", "tarek": "tariq",
            "atapuerca": "atapuerca", "gadir": "gadir", "gadil": "gadir", "nebrija": "nebrija", "neprija": "nebrija",
            "mejicas": "mexicas", "mechicas": "mexicas", "guernika": "guernica", "gernika": "guernica", "covadonga": "covadonga"}
SUBTITULOS = False
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Fenicios, romanos, visigodos, árabes… todos quisieron este rincón de Europa.",
        "Y de aquí salió un idioma que hoy hablan casi seiscientos millones de personas.",
        "Esta es la historia de España, en cinco minutos.",
    ]},
    {"id": "origenes", "frases": [
        "Hace más de un millón de años, ya vivían humanos en Atapuerca.",
        "Hace unos quince mil años, alguien pintó bisontes en el techo de la cueva de Altamira.",
        "Después, los íberos ocupan la costa del Mediterráneo, y los celtas, el interior.",
        "Y por el mar llegan los comerciantes: hace unos tres mil años, los fenicios fundan Gadir, hoy Cádiz.",
        "Luego vienen los griegos, y los cartagineses, que hacen del sur su base.",
        "Desde aquí, Aníbal parte con sus elefantes a atacar Roma.",
    ]},
    {"id": "roma", "frases": [
        "Mala idea: Roma gana la guerra, y se queda con la península.",
        "Conquistarla le cuesta casi doscientos años: en Numancia, los sitiados prefieren morir antes que rendirse.",
        "Pero al final, Hispania se vuelve romana: calzadas, acueductos, teatros… y el latín, el abuelo del español.",
        "Hispania le da a Roma emperadores como Trajano y Adriano.",
    ]},
    {"id": "visigodos", "frases": [
        "Cuando Roma se derrumba, llegan los visigodos, que hacen de Toledo su capital.",
        "Pero viven peleándose por la corona, y eso les va a salir caro.",
    ]},
    {"id": "alandalus", "frases": [
        "En setecientos once, un ejército musulmán cruza el estrecho.",
        "Su general, Tariq, le da nombre a una roca: Gibraltar, la montaña de Tariq.",
        "En solo siete años, casi toda la península es Al Ándalus.",
        "Córdoba se convierte en una de las ciudades más grandes de Europa, y en novecientos veintinueve, su emir se proclama califa.",
        "Llegan el arroz, el azúcar y las naranjas, y miles de palabras: aceite, almohada, azulejo… y ojalá.",
    ]},
    {"id": "reconquista", "frases": [
        "Mientras tanto, en las montañas del norte, un noble llamado Pelayo vence en Covadonga.",
        "Nacen los reinos cristianos, que durante siglos empujan la frontera hacia el sur.",
        "En mil treinta y uno, el califato estalla en más de veinte reinos pequeños: las taifas.",
        "Los cristianos aprovechan: cae Toledo, y el Cid conquista Valencia.",
        "En mil doscientos doce, en las Navas de Tolosa, la balanza se rompe.",
        "Caen Córdoba y Sevilla, y de Al Ándalus solo queda el reino de Granada.",
    ]},
    {"id": "reyes", "frases": [
        "Mil cuatrocientos sesenta y nueve: Isabel de Castilla se casa con Fernando de Aragón.",
        "Juntan las dos grandes coronas, y en mil cuatrocientos noventa y dos, toman Granada.",
        "Ese mismo año expulsan a los judíos que no se bautizan, y Nebrija publica la primera gramática del castellano.",
        "Y un marino genovés, Cristóbal Colón, zarpa hacia el oeste buscando la India.",
        "El doce de octubre, llega a un mundo nuevo para Europa: América.",
    ]},
    {"id": "imperio", "frases": [
        "Empieza la conquista: Hernán Cortés, con miles de aliados indígenas, derrota a los mexicas, y Francisco Pizarro, a los incas.",
        "Es brutal: la guerra y, sobre todo, las epidemias matan a millones de indígenas.",
        "De esa mezcla nace la América hispana, y el castellano cruza el océano.",
        "Con la plata de Potosí y Zacatecas, España se vuelve la primera potencia del mundo.",
        "Felipe segundo reina sobre un imperio donde nunca se pone el sol: hasta las Filipinas llevan su nombre.",
        "Gana en Lepanto, pero su Armada Invencible fracasa contra Inglaterra.",
    ]},
    {"id": "siglo_oro", "frases": [
        "Es el Siglo de Oro: Cervantes escribe el Quijote, y Velázquez pinta Las Meninas.",
        "Pero tanta guerra sale cara, y la corona quiebra una y otra vez.",
        "En mil setecientos, el último rey de los Austrias muere sin hijos, y estalla una guerra por el trono.",
        "La gana un Borbón francés, pero España pierde sus tierras en Europa, y Gibraltar pasa a manos británicas.",
    ]},
    {"id": "ochocientos", "frases": [
        "En mil ochocientos ocho, Napoleón invade España y sienta a su hermano en el trono.",
        "El pueblo se levanta, Goya lo pinta, y el mundo aprende una palabra nueva: guerrilla.",
        "En Cádiz se firma la primera constitución española: la Pepa.",
        "Y al otro lado del mar, en apenas quince años, casi toda la América española se independiza: de ahí nacen los países que hoy conoces.",
        "El resto del siglo es un caos: guerras civiles, una reina al exilio, un rey que renuncia, y una república de once meses.",
        "Y en mil ochocientos noventa y ocho, España pierde Cuba, Puerto Rico y Filipinas en una guerra con Estados Unidos.",
    ]},
    {"id": "siglo_xx", "frases": [
        "En mil novecientos treinta y uno llega la Segunda República; cinco años después, un golpe militar desata la Guerra Civil.",
        "Tres años de horror y cientos de miles de muertos: Picasso pinta el bombardeo de Guernica.",
        "Gana el general Franco, que gobierna como dictador durante treinta y seis años.",
        "Hambre, censura y exilio; y en los años sesenta, llegan el turismo y el dinero.",
        "Franco muere en mil novecientos setenta y cinco, y el rey Juan Carlos abre paso a la democracia.",
        "En mil novecientos setenta y ocho, España vota su Constitución.",
        "Sobrevive a un golpe de Estado, entra en Europa, y en noventa y dos, el mundo entero mira a Barcelona.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Hoy, España tiene unos cuarenta y nueve millones de habitantes, y recibe más de noventa millones de turistas al año.",
        "Íberos, romanos, godos, árabes, judíos y cristianos: todos dejaron algo en este rincón de Europa.",
        "¿Qué país quieres ver en cinco minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria.py): España ilustrada y juguetona, con hueco para la voz; un bloque por escena (se genera en partes, _lyria_partes.py)
LYRIA = dict(
    estilo=("Playful yet epic animated-history documentary score with a Spanish soul: nylon-string Spanish guitar (rasgueado and light picado), "
            "castanets, cajón, palmas, a little oud and darbuka for the Al-Andalus section, and a light modern pulse, in the feel of a fast-moving "
            "illustrated history explainer. Bright, rhythmic, constantly evolving, with short stingers at scene changes. "
            "Melodies kept low and sparse so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: plucked Spanish guitar motif over a light ticking pulse and cajón, curiosity building, a cheeky rise and a bright hit at the end.", 5),
        "origenes": ("Prehistoric mystery: deep hand drums and a soft bone flute, then a warm sea breeze with plucked lyre for the Phoenician traders, ending with marching elephant drums.", 4),
        "roma": ("Roman conquest: martial snare and low brass-like strings, a heroic but heavy siege rhythm, then a proud, settled imperial theme.", 6),
        "visigodos": ("Gothic and somber: low choir pad and a slow drum, a crown motif, rising tension at the end.", 5),
        "alandalus": ("Al-Andalus: oud and qanun melody with darbuka and frame drum, elegant, flowing and luminous, a golden-age feel.", 6),
        "reconquista": ("Medieval struggle: galloping drums, hurdy-gurdy and Spanish guitar together, battle tension, a big decisive hit.", 7),
        "reyes": ("Royal wedding fanfare on Spanish guitar and bells, then a triumphant hit for Granada, then a hopeful seafaring theme with a rising horizon.", 6),
        "imperio": ("Empire and conquest: grand and dark, deep drums, a sorrowful moment for the epidemics, then majestic silver-and-gold power, ending with a storm for the Armada.", 7),
        "siglo_oro": ("Baroque golden age: elegant baroque guitar and harpsichord-like plucks, then a worried descending line, then a stately French-tinged dance.", 5),
        "ochocientos": ("Napoleonic war: snare drums and pizzicato, a fiery flamenco outburst for the uprising, then chaotic shifting rhythms, ending with a sad farewell motif.", 7),
        "siglo_xx": ("Twentieth century: a hopeful start, then dark war drums and silence, a long grey somber stretch, then light returning with optimistic modern guitar and handclaps, building to a festive Barcelona '92 celebration.", 7),
        "cierre": ("Playful resolving outro: the opening guitar motif returns brightly with palmas and castanets, friendly and inviting, a final warm chord and fade.", 5),
    },
)
