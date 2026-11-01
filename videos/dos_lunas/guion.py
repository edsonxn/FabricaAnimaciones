# -*- coding: utf-8 -*-
"""¿Qué pasaría si la Tierra tuviera DOS Lunas? — Kuriox, ~6 min, Kurzgesagt PLANO SECUENCIA (una clase Mundo, sin cortes).
Mayormente espacio (planetas, lunas, órbitas, estrellas) con acercamientos a la Tierra en 2D (mareas, costas, cielo con dos lunas).
Voz Dan (Chatterbox, números en palabras), ritmo Kuriox: pausas cortas (GAP 0,35), frases cortas, mucho movimiento. Mascota Kuri.

Datos verificados (12-oct-2026; nada de memoria):
  - Luna: 384 400 km, 1/81 de la masa terrestre; se aleja 3,8 cm/año (Wikipedia «Tide», NASA).
  - Marea: fuerza de marea ∝ 1/distancia³ (a la mitad de distancia, 8×); la del Sol es el 46 % de la lunar; récord de rango de marea:
    bahía de Fundy, Burntcoat Head, 16,3 m (nov-1998) (Wikipedia «Tide»; Canadian Hydrographic Service).
  - Esfera de Hill de la Tierra: ≈ 1,47 millones de km (≈ 0,01 UA). Órbitas estables solo dentro de ~½ del radio de Hill
    (prógradas; las retrógradas llegan más lejos: Hamilton & Burns 1991, Icarus 92, 118).
  - Puntos de Lagrange L4/L5 de la Luna (60° delante/detrás): estables porque M_Tierra/M_Luna > 24,96; nubes de polvo de Kordylewski
    confirmadas con polarimetría (Slíz-Balogh et al., 2018, MNRAS 480, 5550) y fotografiadas en 2021-22.
  - Jano y Epimeteo (Saturno): órbitas a ~50 km de diferencia (151 441 y 151 462 km), intercambian órbita cada ~4 años
    (2006, 2010, 2014, 2018, 2022; nunca se acercan menos de ~10 000 km) (NASA/JPL Cassini).
  - Tritón: luna capturada de Neptuno, órbita retrógrada (cae lentamente). Fobos: se acerca 1,8 m por siglo; en ~50 millones de años
    chocará con Marte o se romperá en un anillo (NASA Science, Phobos).
  - 2024 PT5: capturada temporalmente del 29-sep-2024 al 25-nov-2024 (~2 meses), ~11 m (5-42 m); roca eyectada de la Luna.
  - Límite de Roche para una luna de densidad lunar (3,34 g/cm³) alrededor de la Tierra (5,51 g/cm³, R = 6 371 km):
    rígida d = R·(2ρM/ρm)^⅓ ≈ 9 500 km; fluida d ≈ 2,44·R·(ρM/ρm)^⅓ ≈ 18 400 km (ambas desde el CENTRO de la Tierra).
  - Radio de órbita síncrona terrestre: 42 164 km desde el centro (35 786 km de altura); por dentro de ella, la luna cae.
  - Ío (Júpiter): más de 400 volcanes activos por calentamiento de marea.
  - Gran impacto: la Luna se formó hace ~4 500 millones de años.
  - Jutzi y Asphaug (2011), Nature 476, 69-72, doi:10.1038/nature10289 (DOI verificado en Crossref): hipótesis de una luna compañera
    de ~1 200 km en un punto troyano de la Luna que, hace ~4 400 millones de años, se aplastó a baja velocidad sobre la cara oculta y
    explicaría la corteza gruesa de sus tierras altas. Es una HIPÓTESIS (otros, p. ej. Nimmo, proponen causas gravitatorias).
"""

TITULO = "¿Qué pasaría si la Tierra tuviera DOS Lunas?"
ARCHIVO = "dos_lunas"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 110
GAP = 0.35
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 9       # plano secuencia: 10 escenas = 9 cambios, ninguno es un corte
MUSICA = {}                                  # la música es Lyria (LYRIA), nunca la procedural

LYRIA = dict(
    estilo=("Wonder-filled, curious yet slightly tense space-documentary score for a fast-paced animated science video: shimmering "
            "celesta and glockenspiel, soft analog synth pads, light pulsing pizzicato, a gentle deep bass, tiny sparkling "
            "synth arpeggios; modern, playful, cosmic. Keeps moving, with short stingers at changes. Melodies low and sparse so a "
            "narrator can speak over it. Instrumental only."),
    escenas={
        "intro": ("Hook: a mysterious cosmic rise with a playful stinger on the question, then a curious ticking pulse.", 5),
        "hoy": ("Calm floating pads with a light heartbeat pulse, tides rolling softly in the low end.", 4),
        "origen": ("Playful curious pizzicato, a tiny heist-like rhythm, bright glockenspiel stabs on each idea.", 6),
        "orbita": ("Orbital waltz feel: circling arpeggios, a precise ticking clock, delicate and elegant.", 5),
        "cielo": ("Dreamy night-sky pads with celesta twinkles, warm and magical, slow shimmer.", 4),
        "mareas": ("Building tension: surging bass swells like waves, rising strings, rhythmic urgency.", 7),
        "calor": ("Deep rumbling low drones, hot pulsing synth, volcanic tension, sparse metallic hits.", 7),
        "caida": ("Dramatic descent: falling arpeggios, growing dread, a huge cinematic swell, then glittering ring-like shimmer.", 8),
        "choque": ("Mystery-reveal: hushed suspense, then a slow soft impact and a wondrous, thoughtful resolution.", 6),
        "cierre": ("Warm hopeful final theme, gentle and glowing, soft fade with one last twinkle.", 4),
    },
    # Lyria da ~3 min por pieza: 3 tramos (<= 175 s) unidos con fundido cruzado por nucleo/lyria_tramos.py
    tramos=[
        (["intro", "hoy", "origen", "orbita", "cielo"],
         "Begin from near silence with a cosmic rise. Keep one consistent melodic theme throughout. End on a held, soft, dreamy tone that can flow into the next part."),
        (["mareas", "calor", "caida"],
         "Continue the same theme and instrumentation, growing steadily in tension and energy. End on a large swelling cinematic chord."),
        (["choque", "cierre"],
         "Open with hushed suspense after the previous swell, then resolve into the warm main theme. End with a gentle natural fade-out."),
    ])

ESCENAS = [
    {
        "id": "intro",
        "pre": 0.3,
        "frases": [
            "La Tierra tiene una sola Luna. Pero, ¿y si tuviera dos?",
            "Y no hablo de una piedrita: hablo de otra Luna enorme, colgada en el cielo junto a la primera.",
            "Hoy vamos a averiguar de dónde saldría, dónde podría vivir y qué le haría a nuestro planeta.",
            "Te adelanto que las mareas se volverían una locura.",
            "Y al final te cuento por qué creo que quizás ya tuvimos dos.",
        ],
    },
    {
        "id": "hoy",
        "frases": [
            "Empecemos con la Luna que ya conocemos.",
            "Está a unos cuatrocientos mil kilómetros, y pesa unas ochenta veces menos que la Tierra.",
            "Parece poca cosa, pero mueve los océanos enteros dos veces al día.",
            "Eso es la marea: la Luna tira más fuerte del lado cercano de la Tierra que del lejano, y estira el agua.",
        ],
    },
    {
        "id": "origen",
        "frases": [
            "Primera pregunta: ¿de dónde sacamos otra Luna?",
            "Opción uno: capturarla. Un asteroide grande pasa cerca, y la gravedad lo atrapa.",
            "Neptuno lo hizo con su luna Tritón, que antes era una viajera de fuera.",
            "Pero atrapar algo es dificilísimo: casi todo lo que pasa cerca sigue de largo.",
            "En dos mil veinticuatro, un asteroide de unos once metros se quedó con nosotros dos meses, como una mini Luna.",
            "Y luego se fue.",
            "Opción dos: fabricarla. Un choque gigante lanza roca al espacio, y esa roca se junta en una luna.",
            "Así nació la nuestra, hace unos cuatro mil quinientos millones de años.",
            "Con un choque un poco distinto, habrían salido dos.",
        ],
    },
    {
        "id": "orbita",
        "frases": [
            "Segunda pregunta: ¿dónde la ponemos? No vale cualquier sitio.",
            "La gravedad de la Tierra solo manda hasta cierta distancia: un millón y medio de kilómetros. Más allá, el Sol se la lleva.",
            "Y las órbitas seguras están a menos de la mitad de esa distancia.",
            "Pero dos lunas en órbitas parecidas se estorban: cada una tira de la otra, y tarde o temprano chocan, o una sale disparada.",
            "Hay una excepción preciosa: Jano y Epimeteo, dos lunas de Saturno que casi comparten órbita.",
            "Cuando una alcanza a la otra, no chocan: se intercambian las órbitas, cada cuatro años.",
            "Y para nosotros hay un escondite perfecto: un punto de equilibrio, sesenta grados por delante o por detrás de la Luna.",
            "Ahí, la gravedad de la Tierra y la de la Luna se compensan, y una segunda luna se quedaría persiguiendo a la primera sin alcanzarla jamás.",
        ],
    },
    {
        "id": "cielo",
        "frases": [
            "Imagina mirar hacia arriba desde ahí abajo.",
            "Dos Lunas, separadas por unos seis puños de cielo.",
            "Cada una con sus fases: una creciente mientras la otra ya va menguando.",
            "Como van a la misma velocidad, cada fase se repetiría con casi cinco días de diferencia.",
            "Habría más noches claras, y los animales y los corales, que se reproducen siguiendo la luna llena, no sabrían a cuál obedecer.",
            "Bonito, ¿no? Pero una segunda Luna tranquila no cambiaría gran cosa. Así que vamos a ponerla mucho más cerca.",
        ],
    },
    {
        "id": "mareas",
        "frases": [
            "A la mitad de distancia, a unos ciento noventa mil kilómetros.",
            "Aquí viene lo importante: el tirón de marea crece con el cubo de la cercanía.",
            "A la mitad de distancia, la marea es ocho veces más fuerte.",
            "Los océanos subirían muchos metros más, dos veces al día, en todas las costas del planeta.",
            "Hoy el récord es de dieciséis metros, en la bahía de Fundy, en Canadá. Con esa Luna, algo así sería normal en muchas costas.",
            "Y cada vez que las dos Lunas se alinearan, los tirones se sumarían, y el mar se levantaría todavía más.",
            "La costa dejaría de ser un lugar estable: cada día entraría una ola gigante que no termina.",
        ],
    },
    {
        "id": "calor",
        "frases": [
            "Y no solo se estiraría el agua: también la roca.",
            "La Tierra sólida ya sube y baja unas decenas de centímetros con la Luna.",
            "Con una luna mucho más cercana, ese vaivén estiraría y frotaría el interior del planeta sin parar.",
            "Esa fricción genera calor. Le pasa a Ío, una luna de Júpiter, tan estirada que tiene más de cuatrocientos volcanes activos.",
            "La Tierra no se volvería como esa luna, pero tendría más terremotos y más volcanes.",
        ],
    },
    {
        "id": "caida",
        "frases": [
            "Y aquí viene el verdadero problema: las lunas no se quedan donde las dejas.",
            "La nuestra se aleja casi cuatro centímetros por año, porque la marea que levanta la empuja hacia delante.",
            "Pero una luna que gira al revés, o más rápido que el planeta, hace lo contrario: se acerca.",
            "Fobos, una luna de Marte, baja casi dos metros cada siglo.",
            "Cada vez más cerca, cada vez más tirón, hasta cruzar una frontera invisible: el límite de Roche.",
            "Dentro de ese límite, la Tierra estira a la luna más de lo que su propia gravedad la mantiene unida.",
            "Para una luna como la nuestra, está entre nueve mil y dieciocho mil kilómetros del centro de la Tierra.",
            "Al cruzarlo, la luna se estira, se parte y sus pedazos se reparten en un anillo.",
            "Tendríamos anillos como los de Saturno: preciosos, brillantes… y peligrosos, porque al principio lloverían rocas sobre la Tierra.",
        ],
    },
    {
        "id": "choque",
        "frases": [
            "Hay otro final posible para dos lunas: que choquen entre ellas.",
            "Y puede que ya haya pasado.",
            "Nuestra Luna tiene dos caras muy distintas: la que vemos es lisa, con grandes mares oscuros.",
            "La oculta está llena de montañas y cráteres, y su corteza es mucho más gruesa.",
            "En dos mil once, dos científicos propusieron una explicación: la Tierra tuvo una segunda luna, de unos mil doscientos kilómetros.",
            "Nació del mismo choque gigante y se quedó en uno de esos puntos de equilibrio.",
            "Pasaron millones de años, la órbita de la Luna cambió, y el equilibrio se rompió.",
            "Entonces chocaron, pero tan despacio que no hicieron un cráter: la luna pequeña se aplastó como un panqueque sobre la cara oculta.",
            "Es solo una hipótesis, pero encaja con lo que vemos.",
            "O sea que quizás la Tierra sí tuvo dos Lunas. Y una está pegada a la otra.",
        ],
    },
    {
        "id": "cierre",
        "post": 2.0,
        "frases": [
            "Hoy tenemos una sola, y puede que eso sea lo mejor.",
            "Una Luna estable, mareas suaves y noches oscuras para ver las estrellas.",
            "Con dos, o se estorban, o se estrellan, o nos destrozan las costas.",
            "Así que esta noche, mira la Luna.",
            "Es la única que nos quedó.",
        ],
    },
]
