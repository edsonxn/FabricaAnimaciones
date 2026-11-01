# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Banjo-Tooie: su historia y los 10 secretos QUE IGNORASTE» (19-oct-2026).
El canal VUELVE a Nintendo/retro (decisión del usuario, 19-oct-2026; el terror CRT queda atrás) con la fórmula de Warcraft,
Tamriel y Runa Caída: motor SECUENCIA YT (gameplay por beat, docs/estilo_secuencia_yt.md) + pegatinas + fichas + MG nuevos
(kit `nucleo/mg_gaming.py`), voz Chatterbox «Sarcastica». Ángulo pedido por el usuario: historia del desarrollo, algo de lore
y sobre todo curiosidades y secretos (lista de 10 en cuenta regresiva, empaque «QUE IGNORASTE» de Runa ×24,6).
Datos verificados el 19-oct-2026:
- Wikipedia «Banjo-Tooie»: Gregg Mayles y Steve Malpass diseño; Chris Sutherland y Paul Machacek programación; Steve Mayles arte;
  Grant Kirkhope música (doble de memoria, dos MIDI a la vez para fundir zonas); empezó en junio de 1998; meta 4.º trimestre de
  1999, retrasado; E3 2000; NA 20-nov-2000, JP 27-nov-2000, EU 12-abr-2001; campaña de 6 millones de dólares; Metacritic 90,
  GameSpot 9,6 y mejor plataformas del 2000; queja: fluidez; mundo de castillo cortado (sus recursos → Cauldron Keep);
  Bottles' Revenge cortado (único jefe controlable: Old King Coal; inspiró el Counter-Operative de Perfect Dark);
  Stop 'n' Swop quitado por límites del hardware; XBLA 4J Studios 29-abr-2009 con Stop 'n' Swop; Rare comprada por Microsoft
  en 2002 (último Banjo que publicó Nintendo); Nintendo Classics 25-oct-2024; Evercade 30-oct-2026 con Bottles' Revenge.
- Time Extension / búsqueda (sep-2026): Evercade Double Pack, código fuente original con Rare, 60 fps (Nexus/Alpha/Super Pocket),
  pistas sin usar, Bottles' Revenge por primera vez oficial.
- Wiki de Banjo en Fandom: argumento (póker, Kazooie hace trampa gritando que vuelve Grunty, Hag 1, esqueleto, Bottles se queda
  creyendo que es broma, B.O.B., Jingaling zombi, cabeza pateada, «Banjo-Threeie»); Grunty no rima por condición de sus hermanas
  y vuelve a rimar en Nuts & Bolts; Cheato y códigos (CHEATO + código al revés; NESTKING por el cartel «egg container followed
  by Jingaling»; HONEYKING, JIGGYWIGGYSPECIAL); Banjo-Kazooie Game Paks (3: cascada, rejilla con granadas, cueva por Grip Grab;
  únicos enemigos sin miel); Jinjos (9 familias de 1 a 9 = 45; familia gris aplastada; casa gris en los datos «SHOULDN'T BE
  HERE»); Mega-Glowbo (Ice Key + Talon Torpedo de Jolly Roger's → roca con la cara de Kazooie en Glitter Gulch → caja de hielo
  en Hailfire Peaks → Humba Wumba → Dragon Kazooie); Tower of Tragedy (pesas de una tonelada, hermanas eliminadas, icono de
  Devil Bottles); Stop 'n' Swop (carta de Nintendo: daño y revisiones que borran la RAM antes; Rare Witch Project; menú sin uso;
  rosa = Breegull Bash, azul = Homing, amarillo = Jinjo en multijugador).
- Chris Sutherland (Notebookcheck, nov-2025): 4-5 del equipo jugaban GoldenEye cada comida «durante un par de años».
- Gregg Mayles (Nintendo Life vía Nintenderos, 21-nov-2020): el tono oscuro fue deliberado. Fax «Splendid game» (Time Extension,
  dic-2025): la nota la añadió Mayles, era broma. Documento «Coldswap» publicado
  por Mayles (VidaExtra 24-dic-2025; Wikipedia: Stop 'n' Swop también para Donkey Kong 64). Cauldron Keep iba a ser mundo completo con 10 Jiggies (VGFacts citando a Mayles).
"""

TITULO = "Banjo-Tooie: su historia y los 10 secretos QUE IGNORASTE"
ARCHIVO = "banjo_tooie"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# 19-oct-2026: el usuario pidió rehacer la voz con ElevenLabs, voz de mujer (Hope); la Chatterbox Sarcastica decía mal Tooie/Kazooie.
# Respaldo de la voz anterior: voz/_chatterbox/. Corchetes de actuación en las frases (regla global).
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía real para .srt, apoyos y YouTube
FONETICA = {"B.O.B.": "Bob", "Hag 1": "Hag One"}
FONETICA_CHATTERBOX = {   # la de la voz anterior (Chatterbox), ya no se usa
    "Banjo-Tooie": "Bányo Túi", "Banjo-Kazooie": "Bányo Kazúi", "Banjo-Threeie": "Bányo Zríi", "Banjo": "Bányo",
    "Kazooie": "Kazúi", "Tooie": "Túi", "two": "tu", "Gruntilda": "Gruntílda", "Mumbo": "Múmbo", "Bottles": "Bótels",
    "Bottles' Revenge": "Bótels Rivénch", "Rare Witch Project": "Rer Uích Próyect", "Rare": "Rer",
    "Jiggies": "Yíguis", "Jiggywiggy": "Yígui Uígui", "Jinjos": "Yínyos", "King Jingaling": "King Yíngaling",
    "Jingaling": "Yíngaling", "Mingella": "Minyéla", "Blobbelda": "Blobélda", "Hag 1": "Jag uán", "B.O.B.": "Bob",
    "Klungo": "Klúngo", "Cheato": "Chíto", "cheato": "chíto", "eggs": "egs", "Nestking": "Nést king",
    "Mayahem": "Méiajem", "Spiral Mountain": "Spáiral Máunten", "Jolly Roger's Lagoon": "Yóli Róyers Lagún",
    "Glitter Gulch Mine": "Glíter Gólch Máin", "Hailfire Peaks": "Jéilfaier Píks", "Mega-Glowbo": "Mega Glóubo",
    "Humba Wumba": "Júmba Úmba", "Cauldron Keep": "Cóldron Kíp", "Tower of Tragedy": "Táuer of Trájedi",
    "Nuts and Bolts": "Nats an Bolts", "Xbox Live Arcade": "Équis box Láiv Arkéid", "Xbox": "Équis box",
    "Super Smash Bros. Ultimate": "Súper Smash Bros Últimeit", "Nintendo Switch Online": "Nintendo Suích Onláin",
    "Stop 'n' Swop": "Estóp an Suóp", "GameShark": "Guéim Shark", "Old King Coal": "Old King Cóul",
    "Perfect Dark": "Pérfect Dark", "Evercade": "Évercaid", "Double Pack": "Dóbol Pak", "Gregg Mayles": "Greg Méils",
    "Mayles": "Méils", "Steve": "Estív", "Chris Sutherland": "Cris Sázerland", "Grant Kirkhope": "Grant Kérkjoup",
    "GoldenEye": "Góldenai", "Donkey Kong Country": "Dónki Kong Cántri", "Metacritic": "Metacrítik",
    "GameSpot": "Guéim Spot", "Chuffy": "Cháfi", "splendid game": "esplendid guéim", "E3": "E tres",
    "Treasure Trove Cove": "Tréyer Tróuv Cóuv", "Coldswap": "Cóld suóp", "Donkey Kong": "Dónki Kong",
}

# Revisado el 19-oct leyendo cada transcripción (voz/eval.json): Whisper escribe «Toye», «Kasoye», «Miles», «Hingalín», «Clungo»…
# donde la voz dice bien el nombre; las tolerancias dejan pasar SOLO la toma buena de cada frase.
CER_MAX_POR_FRASE_CHATTERBOX = {"intro_0": .025, "intro_3": .015, "intro_4": .02, "origen_2": .022, "desarrollo_3": .045,
    "desarrollo_7": .022, "desarrollo_8": .042, "lore_1": .07, "lore_2": .015, "lore_3": .03, "lore_5": .02, "lore_7": .035,
    "p10_2": .03, "p10_4": .02, "p9_2": .02, "p9_3": .04, "p7_0": .022, "p7_1": .022, "p7_3": .027, "p6_2": .04, "p6_3": .045,
    "p5_2": .042, "p3_1": .03, "p3_2": .015, "p3_3": .04, "p3_4": .015, "p2_0": .02, "p2_1": .02, "p2_6": .02,
    "p1_1": .015, "cierre_0": .015, "p2_5": .03,
    "cierre_2": .02, "desarrollo_6": .03, "origen_4": .07, "p5_1": .095}
TAIL_MAX_POR_FRASE_CHATTERBOX = {"intro_4": .46, "origen_0": .57, "origen_3": .5, "desarrollo_2": .55, "desarrollo_7": .55, "lore_1": .56,
    "lore_2": .40, "lore_6": .55, "p9_3": .38, "p7_1": .53, "p7_4": .6, "p6_2": .64, "p5_3": .42, "p4_4": .40, "p3_1": .5,
    "p3_3": .68, "p3_4": .69, "p2_4": .64, "p1_2": .49, "p1_5": .66, "p1_6": .66, "p1_7": .38, "cierre_0": .52, "p2_5": .58,
    "desarrollo_6": .51, "p8_4": .49}
# Voz Hope (ElevenLabs), revisado el 19-oct leyendo eval.json: Whisper escribe a su modo los nombres ingleses («Chito», «Tui/Kazui»,
# «Greg Males», «Hellfire», «Menguela», «Banjo 3», «Mega Globo»): falsas alarmas, se aceptan con la CER de la toma buena.
CER_MAX_POR_FRASE = {"origen_4": .06, "desarrollo_6": .03, "desarrollo_7": .015, "lore_2": .02, "p9_0": .02, "p9_1": .02,
    "p9_2": .035, "p7_2": .03, "p6_2": .02, "p6_3": .02, "p4_3": .04, "p3_1": .03, "p2_6": .02, "p1_4": .02, "p2_0": .06}
TAIL_MAX_POR_FRASE = {"desarrollo_7": 1.05, "p9_3": 1.05}
GAP_MAX_POR_FRASE_CHATTERBOX = {"origen_0": .72, "lore_7": .8, "p2_4": .66}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    # marco de Switch Online (degradado gris + «P1», ~14 % por lado) y franjas de las escenas, medidos por código el 19-oct
    recorte_por={"scene-001": 0.145, "scene-002": 0.12, "scene-004": 0.145, "scene-006": 0.13, "scene-007": 0.13, "scene-008": 0.125, "scene-009": 0.125, "scene-012": 0.125, "scene-017": 0.122, "scene-022": 0.145, "scene-023": 0.145, "scene-024": 0.145, "scene-025": 0.145, "scene-026": 0.145, "scene-027": 0.145, "scene-028": 0.122, "scene-029": 0.122, "scene-030": 0.122, "scene-031": 0.08, "scene-032": 0.145, "scene-033": 0.122, "scene-034": 0.105, "scene-036": 0.08, "scene-041": 0.035, "scene-043": 0.035, "scene-045": 0.035, "scene-052": 0.035, "scene-053": 0.035, "scene-054": 0.035, "scene-055": 0.122, "scene-059": 0.105, "scene-061": 0.078, "scene-066": 0.123, "scene-067": 0.122, "scene-072": 0.125, "scene-073": 0.125, "scene-074": 0.125, "scene-077": 0.122, "scene-079": 0.11, "scene-081": 0.145, "scene-091": 0.08, "scene-093": 0.122},
    yt=dict(sufijo="", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Whimsical late-90s 3D platformer soundtrack: bouncy tuba and bassoon, plucked banjo, marimba, kazoo-like "
           "woodwinds, playful pizzicato strings, light percussion, instrumental only, no vocals, cheerful and "
           "unobtrusive under narration.",
    escenas={
        "intro": ("mysterious music box twist on a cheerful tune, a secret hidden in a cartridge", 5),
        "origen": ("cheerful bouncy opening, sunny mountain morning, tuba and banjo", 4),
        "desarrollo": ("busy workshop, ticking percussion, inventive marimba runs, building momentum", 5),
        "lore": ("stormy night turns sinister, low bassoon, spooky organ, a witch's laugh feel, then sad", 6),
        "p10": ("comic witch theme, oom-pah tuba, mischievous", 4),
        "p9": ("sneaky tiptoe, pizzicato, a book of tricks", 4),
        "p8": ("silly hopping rhythm, xylophone, cartoon surprise", 4),
        "p7": ("tender and sad village tune, music box, slow", 3),
        "p6": ("icy cavern shimmer, then fiery brass, a dragon awakens", 6),
        "p5": ("unfinished castle, dark harpsichord, foreboding", 5),
        "p4": ("twisted game show jingle, organ and snare, darkly comic", 6),
        "p3": ("bittersweet farewell, slow brass, end of an era", 5),
        "p2": ("mysterious puzzle, ticking clock, chimes and low strings, a lost connection", 6),
        "p1": ("devilish ghost theme, spooky theremin-like woodwinds, rising to a triumphant reveal", 8),
        "cierre": ("warm nostalgic reprise, gentle banjo and tuba, fading out", 4),
    },
    tramos=[   # <= 175 s cada uno (tiempos del 19-oct: 95 / 85 / 82,5 / 127,5 / 125 / 90 / 77,5 / 119 s)
        (["intro", "origen"], "Begin from near silence with a music box. End on a warm sustained chord."),
        (["desarrollo"], "Begin on a warm chord. End on a held note, curious."),
        (["lore"], "Begin on a held note, then turn dark and stormy. End on a sad quiet note."),
        (["p10", "p9", "p8"], "Begin on a sad quiet note, then turn playful. End on a light held chord."),
        (["p7", "p6", "p5"], "Begin on a light held chord. End on a low foreboding note."),
        (["p4", "p3"], "Begin on a low foreboding note. End on a bittersweet sustained chord."),
        (["p2"], "Begin on a bittersweet chord, mysterious and ticking. End on a suspended note."),
        (["p1", "cierre"], "Begin on a suspended note, spooky. Rise to a triumphant peak, then settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[mysterious] Durante veintiséis años, dentro de cada cartucho de Banjo-Tooie, hubo un modo de juego completo que nadie podía jugar.",
        "Un fantasma con cuernos que se mete dentro de los enemigos, para que tu amigo te persiga con ellos. [short pause] Programado, probado a medias, [whispers] y escondido.",
        "[excited] Y el treinta de octubre, por fin, se va a poder jugar de forma oficial.",
        "Pero no es el único secreto que se guardó este juego. [short pause] Banjo-Tooie es la secuela que mató a un personaje en la primera escena, que escondió cartuchos vivos, y que dejó una promesa sin cumplir.",
        "[playful] Así que hoy te cuento cómo se hizo, la historia más oscura que Rare le dio a un oso y a un pájaro, y los diez secretos de Banjo-Tooie que seguramente ignoraste.",
    ]},
    {"id": "origen", "frases": [
        "[curious] A finales de los noventa, el estudio británico Rare era la joya de Nintendo. Había hecho Donkey Kong Country, GoldenEye, y en mil novecientos noventa y ocho, Banjo-Kazooie.",
        "[amused] Un oso con pantalones cortos y una pájara gruñona que vive en su mochila, contra una bruja que habla siempre en verso.",
        "El juego fue un éxito, y terminaba con una amenaza. [dramatic] Gruntilda, aplastada bajo una roca, gritaba que volvería en Banjo-Tooie.",
        "[intrigued] Y no era la única pista. Si conseguías los cien Jiggies, Mumbo te enseñaba fotos de objetos escondidos que no se podían alcanzar. Huevos de colores y una llave de hielo, guardados para la secuela.",
        "[laughs] Hasta el nombre era un chiste. Tooie suena a two, que en inglés es dos, y rima con Kazooie. La secuela tuvo nombre antes de tener juego.",
    ]},
    {"id": "desarrollo", "frases": [
        "El equipo empezó a trabajar en junio de mil novecientos noventa y ocho, justo cuando salía el primero.",
        "Al frente del diseño estaba Gregg Mayles, con su hermano Steve en los personajes, Chris Sutherland en la programación, y Grant Kirkhope otra vez en la música.",
        "[amused] Y tenían una obsesión inesperada. Chris Sutherland contó que cuatro o cinco del equipo jugaban GoldenEye a la hora de la comida, todos los días, durante un par de años.",
        "[chuckles] Eso se nota. En Banjo-Tooie puedes agarrar a Kazooie del cuello y disparar huevos en primera persona, como si fuera una ametralladora con plumas.",
        "La otra gran idea era separar al dúo, cada uno con sus movimientos, en mundos el doble de grandes que los del primero y conectados entre sí.",
        "[impressed] Grant Kirkhope tuvo el doble de memoria para la música, y mezclaba dos pistas a la vez para que cambiara sin cortes de una zona a otra.",
        "La idea de Rare era sacarlo a finales de mil novecientos noventa y nueve. [short pause] No llegó. [short pause] Salió en Norteamérica el veinte de noviembre del dos mil, con un nueve punto seis en GameSpot y el premio al mejor juego de plataformas del año.",
        "[curious] Y una curiosidad reciente. En diciembre de dos mil veinticinco, Gregg Mayles publicó el fax con el que Nintendo Japón aprobó el juego, con una nota que decía splendid game y un pulgar arriba.",
        "[sarcastic] Internet se lo creyó. Era Miyamoto aplaudiendo a Banjo-Tooie. [short pause] Hasta que Mayles confesó que esa nota la había escrito él.",
    ]},
    {"id": "lore", "frases": [
        "[serious] Ahora, la historia. Y aquí Rare hizo algo que nadie esperaba de un juego con un oso de peluche en la portada.",
        "[mysterious] Han pasado dos años. Es de noche, hay tormenta, y Banjo, Kazooie, Mumbo y Bottles, el topo que les enseñaba los movimientos, juegan al póker. [sarcastic] Kazooie hace trampa todo el rato.",
        "Mientras tanto, las hermanas de Gruntilda, Mingella y Blobbelda, llegan en una perforadora gigante, la Hag 1, y rompen la roca. [short pause] Pero a la bruja ya no le queda carne, solo un esqueleto con túnica.",
        "[tense] Furiosa, carga un hechizo contra la casa de Banjo. Todos salen corriendo, menos Bottles, que cree que es otra broma de Kazooie, se queda sentado, y la casa explota con él dentro.",
        "[sad] A la mañana siguiente lo ven arrastrarse fuera de los escombros, [short pause] y morir. Su fantasma se queda en la montaña.",
        "[serious] Gregg Mayles lo admitió veinte años después. El tono más oscuro fue a propósito. No querían repetir el primer juego, querían sorprender.",
        "[ominous] Y la cosa empeora. Las hermanas tienen una máquina, el B.O.B., que absorbe la fuerza vital de lo que toca. Con esa energía, la bruja recuperaría su cuerpo.",
        "[grim] La prueban con el rey de los Jinjos, King Jingaling, y lo dejan convertido en zombi. El plan es exprimir así la isla entera.",
        "Y el juego está lleno de detalles que casi nadie vio. [excited] Vamos con ellos.",
    ]},
    {"id": "p10", "frases": [
        "[excited] Número diez. [short pause] La bruja que tuvo que dejar de rimar.",
        "En el primer juego, Gruntilda hablaba siempre en verso. Era su seña de identidad.",
        "En Banjo-Tooie empieza rimando, y de pronto deja de hacerlo. No es un descuido de los guionistas.",
        "Sus hermanas le pusieron una condición para ayudarla. O dejaba las rimas, o no había cuerpo nuevo. [laughs] Les ponía de los nervios.",
        "[amused] Lo gracioso es que, cuando las hermanas ya no están, sigue hablando normal hasta el final. No volvió a rimar hasta Nuts and Bolts, ocho años después.",
    ]},
    {"id": "p9", "frases": [
        "[playful] En el nueve, los trucos. La bruja se vengó de Cheato, el libro de hechizos que le chivaba trucos al jugador, arrancándole las páginas.",
        "Por cada cinco páginas que le devuelves, Cheato te da un código, y los códigos se escriben pisando letras en una sala del templo de Mayahem.",
        "[whispers] Pero hay un secreto. [short pause] Casi todos funcionan aunque Cheato no te los haya dado, si escribes primero la palabra cheato y después el código al revés.",
        "Y hay uno que viene en forma de acertijo. Un cartel detrás del templo de Jiggywiggy dice: un contenedor de huevos, seguido de Jingaling. [short pause] Nido y rey. [excited] Nestking, y tienes huevos y plumas infinitos.",
    ]},
    {"id": "p8", "frases": [
        "[excited] Número ocho, [amused] y este es de los más raros. Entre la montaña del principio y la aldea de los Jinjos hay tres enemigos muy especiales.",
        "[laughs] Son cartuchos de Banjo-Kazooie. Cartuchos de Nintendo 64, vivos, que van dando saltitos felices por la zona.",
        "Están escondidos detrás de una cascada, tras una rejilla que hay que volar con granadas, y en una cueva a la que se llega colgado de una grieta.",
        "Si les pegas, sueltan su premio. [short pause] Dos huevos de colores y una llave de hielo. Los mismos objetos que Mumbo enseñaba en las fotos del primer juego.",
        "[curious] Es un chiste que solo se entiende con el secreto número dos. Esos objetos tenían que viajar desde el cartucho del primer juego. Como no pudieron, los de Rare metieron el cartucho dentro del juego.",
        "[chuckles] Y como remate, son los únicos enemigos de todo el juego que no sueltan miel al morir.",
    ]},
    {"id": "p7", "frases": [
        "[sad] En el siete, una tragedia que casi nadie notó. La de los Jinjos.",
        "En Banjo-Tooie hay cuarenta y cinco Jinjos repartidos en nueve familias de colores. La blanca tiene un miembro, la naranja dos, la amarilla tres, y así hasta la negra, que tiene nueve.",
        "[serious] Pero en la aldea hay una décima casa, destrozada. Es la de la familia gris. La Hag 1 le pasó por encima camino del castillo, [sad] y no hay supervivientes.",
        "Los fans echaron la cuenta: si cada familia tiene uno más que la de antes, los grises eran diez.",
        "[whispers] Y dentro de los datos del juego, los fans encontraron una casa gris completa, sin destruir, con una etiqueta que dice, más o menos, esto no debería estar aquí.",
    ]},
    {"id": "p6", "frases": [
        "[excited] Número seis. Kazooie puede convertirse en dragón. [short pause] Y casi nadie lo consiguió sin una guía.",
        "[curious] Primero necesitas la llave de hielo, la que suelta uno de esos cartuchos vivos. Luego, un movimiento de buceo que se aprende en Jolly Roger's Lagoon.",
        "Con él rompes una roca con la cara de Kazooie en una cueva de Glitter Gulch Mine, y llegas a la zona helada de Hailfire Peaks, donde espera una caja fuerte de hielo.",
        "[excited] Dentro está el Mega-Glowbo. Se lo llevas a Humba Wumba, la chamana rival de Mumbo, y Kazooie sale convertida en dragón, escupiendo fuego y con huevos de fuego infinitos.",
        "[impressed] Un premio enorme, escondido detrás de tres mundos distintos. [short pause] Y todo nació de una función que nunca llegó a existir.",
    ]},
    {"id": "p5", "frases": [
        "[curious] En el cinco, el mundo que se quedó a medias.",
        "Banjo-Kazooie tenía cien Jiggies. Banjo-Tooie tiene noventa. [short pause] Y esos diez que faltan tienen explicación.",
        "Cauldron Keep, el castillo de las brujas, iba a ser un mundo completo, con sus propios desafíos y sus diez piezas. [sighs] Según Gregg Mayles, el tiempo no alcanzó.",
        "Se quedó en lo que conoces. Una última pelea con Klungo, un concurso, y el combate final. Y para construirlo se aprovechó lo que había de otro mundo de castillo que también se descartó.",
    ]},
    {"id": "p4", "frases": [
        "[dramatic] Número cuatro. [short pause] El concurso de la muerte.",
        "Antes del combate final, Gruntilda te mete en un programa de preguntas, el Tower of Tragedy. [amused] Y contra ti juegan sus propias hermanas.",
        "Sobre cada concursante cuelga una pesa de una tonelada. Al final de cada ronda, [short pause] el que tiene menos puntos queda aplastado.",
        "[sarcastic] Así que la bruja termina eliminando a Mingella y a Blobbelda en su propio concurso, las mismas que la sacaron de debajo de la roca.",
        "[whispers] Y un detalle para el número uno. En ese concurso, mientras piensas la respuesta, puede asomar el icono de un Bottles con cuernos. Es el único rastro visible de un modo que fue cortado.",
    ]},
    {"id": "p3", "frases": [
        "[thoughtful] En el tres, la promesa que nunca se cumplió.",
        "Al final del juego, a Gruntilda solo le queda la cabeza. Banjo y Kazooie la usan de pelota en lo alto del castillo, y ella jura venganza en la siguiente entrega, Banjo-Threeie.",
        "[sighs] Ese juego nunca llegó como se prometió. En dos mil dos, Microsoft compró Rare por trescientos setenta y cinco millones de dólares, y Banjo-Tooie se quedó como el último Banjo que publicó Nintendo.",
        "La siguiente aventura tardó ocho años. Fue Nuts and Bolts, en Xbox, un juego de construir vehículos, [chuckles] donde la bruja es justo eso, una cabeza metida en un cuerpo de robot.",
        "[warm] Banjo regresó a una consola de Nintendo en dos mil diecinueve, como luchador de Super Smash Bros. Ultimate. Y Banjo-Tooie volvió en octubre de dos mil veinticuatro, a Nintendo Switch Online.",
    ]},
    {"id": "p2", "frases": [
        "[mysterious] Número dos. El misterio que obsesionó a los fans durante años. [short pause] Stop 'n' Swop.",
        "[curious] Encendías Banjo-Kazooie, conseguías uno de esos huevos secretos, apagabas la consola, y en unos segundos metías el cartucho de Banjo-Tooie.",
        "La Nintendo 64 tenía un defecto. Su memoria tardaba un poco en borrarse al apagarla, y en esos segundos el segundo juego podía leer lo que había dejado el primero.",
        "[serious] Pero Nintendo le pidió a Rare que lo quitara. Temía que cambiar cartuchos así dañara las consolas, y las revisiones nuevas de la Nintendo 64 borraban la memoria más rápido. El truco podía dejar de funcionar.",
        "Pero el primer juego ya estaba en las tiendas, con sus huevos escondidos. Un grupo de fans, el Rare Witch Project, encontró códigos para llegar hasta ellos, [sarcastic] y al recogerlos aparecía un menú nuevo que nunca sirvió para nada.",
        "Por eso Banjo-Tooie usa solo tres huevos y la llave, metidos en esos cartuchos vivos del número ocho. [short pause] Y en diciembre de dos mil veinticinco, Gregg Mayles enseñó el documento original. Se llamaba Coldswap, y la cadena también iba a pasar por Donkey Kong sesenta y cuatro.",
        "Stop 'n' Swop funcionó por fin en dos mil nueve, cuando los dos juegos llegaron a Xbox Live Arcade. [chuckles] Diez años tarde, y sin tener que cambiar de cartucho.",
    ]},
    {"id": "p1", "frases": [
        "[excited] Y llegamos al número uno. El modo de juego que pasó veintiséis años escondido. [dramatic] Bottles' Revenge, la venganza de Bottles.",
        "¿Recuerdas que Bottles muere al principio? [mischievously] Rare imaginó que su fantasma no se lo tomaba nada bien.",
        "En este modo, Bottles se vuelve un demonio con cuernos, te sigue por el mundo y se mete dentro del enemigo más cercano. Y ese enemigo lo maneja un segundo jugador, con otro mando.",
        "[playful] Si tu amigo te gana con ese enemigo, se cambian los papeles. Ahora él es Banjo, y tú eres el demonio.",
        "Rare quería que pudiera poseer incluso a los jefes. Cuando lo cortaron, el único jefe que se podía controlar era Old King Coal, el rey de carbón de Glitter Gulch Mine.",
        "[sighs] No hubo tiempo de pulirlo, y lo apagaron. [short pause] Pero no lo borraron. Siguió dentro de cada cartucho, y durante años solo se pudo ver con un GameShark o en un emulador. La idea, de hecho, acabó en Perfect Dark.",
        "[excited] Y ahora viene lo bueno. El treinta de octubre sale el Banjo-Kazooie Double Pack para Evercade, hecho junto a Rare con el código original, y trae, por primera vez de forma oficial, Bottles' Revenge.",
        "[warm] Veintiséis años después, el topo que murió en la primera escena por fin se va a poder vengar. [laughs] Y su víctima favorita, seguramente, va a ser Kazooie.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Esos son los diez secretos de Banjo-Tooie. Un fantasma vengativo, un concurso con pesas de una tonelada, una familia que nadie vio, y unos cartuchos que corren por el monte.",
        "[thoughtful] Es la secuela que se atrevió a ser más grande, más rara y más oscura que el original, en la última Navidad en la que Banjo fue de Nintendo.",
        "[curious] ¿Tú sabías que Bottles tenía su propio modo de venganza? ¿O llegaste a ver a Kazooie convertida en dragón? Cuéntamelo en los comentarios.",
        "Y si quieres que hagamos lo mismo con Banjo-Kazooie, el primero, o con otro clásico de la Nintendo 64, déjalo también abajo. [warm] Nos vemos en la próxima crónica.",
    ]},
]
