# -*- coding: utf-8 -*-
"""¿Qué pasaría si el OXÍGENO desapareciera 5 segundos? — Kuriox, ~5 min, Kurzgesagt PLANO SECUENCIA (una clase Mundo, sin cortes).
Voz Dan (Chatterbox, números en palabras), ritmo Kuriox: pausas cortas (GAP 0,35), frases cortas, mucho movimiento. Mascota Kuri.

Fórmula: la del Sol (×9,8) cambiando UNA variable (el tema); referencia viral: Ángel Hernández ×12,2 (Short).
RIGOR: la versión viral mezcla dos experimentos distintos. Aquí se separan:
  A) desaparecen las MOLÉCULAS de oxígeno (O2: aire, sangre, agua disuelta) → sobrevivible, efectos raros.
  B) desaparecen TODOS los ÁTOMOS de oxígeno (agua, roca, cuerpo) → fin del mundo. Ahí sí «el concreto se desmorona».
Regla del juego: a los 5 s cada átomo/molécula vuelve EXACTAMENTE adonde estaba (por eso el ozono no cuenta: también vuelve).

Datos verificados (14-oct-2026; nada de memoria):
  - Aire: 20,95 % de O2 en volumen → sin él la presión cae ~21 % (101,3 → ~80 kPa) = presión estándar a ~2 000 m.
  - Tímpano: rotura a partir de ~20-35 kPa de cambio brusco (onda expansiva; depende del tiempo de subida); el cambio aquí
    (~21 kPa) está en el borde bajo → «a algunos se les podría dañar» (hearinghealthmatters.org; revisión 1989; estudio ovino 2026).
  - Cerebro sin riego: pérdida de conciencia a los 6,4-6,9 s (Rossen, Kabat y Anderson, 1943, Arch. Neurol. Psychiatry;
    reanálisis Navy NAWCADWAR-92026-60). Sin O2 en sangre ni tejidos es equivalente → 5 s = al borde: mareo, quizá desmayos.
  - British Airways 9 (24-jun-1982): 747 con los 4 motores apagados por ceniza del Galunggung; planeó de 37 000 a ~12 000 pies
    (~7 600 m), reencendió y aterrizó en Yakarta sin víctimas. Planeo 15:1 (Guinness World Records; relato del capitán Moody).
  - Electricidad: ~59 % mundial de fósiles en 2024 (Ember, Global Electricity Review 2025: limpia 40,9 %). Las calderas y
    turbinas se disparan por seguridad al perder la llama (detectores de llama) → riesgo de apagones en cascada (hipótesis, «podría»).
  - El Sol no es fuego: fusión nuclear, no necesita oxígeno.
  - Oxígeno en masa: ~46 % de la corteza (CRC: 46,1 %), 88,8 % del agua, ~65 % del cuerpo humano (61-65 % según fuente).
  - Soldadura en frío: metales limpios sin capa de óxido que se tocan se pegan (fenómeno real en el vacío; ESA). En B, «podrían».
  - Hidrógeno + oxígeno = combustible de los motores principales del transbordador espacial / muchas etapas de cohete.
  - Océanos ~1,4e21 kg × 11,2 % de H = ~1,6e20 kg de hidrógeno vs atmósfera 5,1e18 kg → ~30 veces.
  - Corteza: el oxígeno es ~46 % del peso pero ~60 % de los átomos → «más de la mitad de sus átomos».
  - Gran Oxidación: hace ~2 400 millones de años, por cianobacterias. El océano produce ~la mitad del oxígeno (NOAA).
"""

TITULO = "¿Qué pasaría si el OXÍGENO desapareciera 5 segundos?"
ARCHIVO = "oxigeno_5_segundos"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 110
GAP = 0.35
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 12      # plano secuencia: 13 escenas = 12 cambios, ninguno es un corte
MUSICA = {}                                  # la música es Lyria (LYRIA), nunca la procedural

LYRIA = dict(
    estilo=("Curious, playful yet suspenseful science-documentary score for a fast-paced animated video about breathing and "
            "air: airy breathy synth pads, soft celesta and glockenspiel, light pizzicato, a gentle pulsing bass, a subtle "
            "ticking clock motif for a five-second countdown; modern and cinematic. Keeps moving, with short stingers at "
            "changes. Melodies low and sparse so a narrator can speak over it. Instrumental only."),
    escenas={
        "intro": ("Hook: a held breath, a sudden hush, then a playful stinger on the question and a ticking countdown pulse.", 5),
        "reglas": ("Light curious pizzicato explaining the rules of a game, bright glockenspiel on each idea.", 4),
        "aire": ("A sudden drop in pressure: a deep whoosh, muffled underwater-like pads, a tense heartbeat pulse.", 6),
        "fuego": ("Rising urgency: flames snuffing out, engines winding down, a slowing low drone with metallic hits.", 7),
        "cuerpo": ("Intimate and tense: a slow heartbeat, narrowing filtered pads like tunnel vision, a fragile celesta.", 7),
        "regreso_a": ("Relief: a big inhale, warm pads opening up, a hopeful bright melody returning.", 4),
        "atomos": ("Ominous turn: the main theme in a darker minor key, low strings, a heavier ticking pulse.", 6),
        "suelo": ("Crumbling tension: granular textures, deep rumbling bass, stone-like percussive hits.", 8),
        "agua": ("Strange and huge: shimmering bubbling synths, swelling strings, rising pressure.", 8),
        "nosotros": ("Grave and quiet: sparse low piano-like tones, a near silence, a single held note.", 6),
        "regreso_b": ("Suspense rising to a massive cinematic swell like a rocket ignition, then cut to silence.", 9),
        "realidad": ("Calm wonder: gentle pads, ocean-like swells, warm celesta, the main theme softly returning.", 4),
        "cierre": ("Warm and peaceful resolution of the main theme, a slow deep breath, gentle natural fade-out.", 3),
    },
    # Lyria da ~3 min por pieza: 3 tramos (<= 175 s) unidos con fundido cruzado por nucleo/lyria_tramos.py
    tramos=[
        (["intro", "reglas", "aire", "fuego"],
         "Begin from near silence with a held-breath hush. Keep one consistent melodic theme throughout. End on a soft held tone that can flow into the next part."),
        (["cuerpo", "regreso_a", "atomos", "suelo"],
         "Continue the same theme and instrumentation: tense, then a warm relief, then turning darker and heavier. End on a low rumbling held chord."),
        (["agua", "nosotros", "regreso_b", "realidad", "cierre"],
         "Continue the same theme growing strange and huge to a cinematic swell, a sudden silence, then resolve into the warm main theme. End with a gentle natural fade-out."),
    ])

ESCENAS = [
    {
        "id": "intro",
        "pre": 0.3,
        "frases": [
            "Respira hondo.",
            "Ahora imagina que, justo en este instante, todo el oxígeno de la Tierra desaparece.",
            "No para siempre: solo cinco segundos.",
            "Cinco segundos parece nada. Es más o menos lo que tardas en respirar una vez.",
            "Pero el oxígeno está en muchos más sitios de los que crees.",
            "Y en cinco segundos, el mundo cambiaría muchísimo.",
        ],
    },
    {
        "id": "reglas",
        "frases": [
            "Primero, las reglas del juego.",
            "Durante cinco segundos, el oxígeno deja de existir, y luego vuelve exactamente al lugar donde estaba.",
            "Y hay dos formas de jugar.",
            "En la primera, solo desaparece el oxígeno que respiramos: el gas del aire.",
            "En la segunda, desaparece todo el oxígeno, hasta el último átomo, esté donde esté.",
            "Empecemos por la fácil.",
        ],
    },
    {
        "id": "aire",
        "frases": [
            "Segundo cero. Una de cada cinco moléculas del aire se esfuma de golpe.",
            "El aire se vuelve más ligero, y la presión cae una quinta parte.",
            "Es como si te subieran en un instante a lo alto de una montaña de dos mil metros.",
            "Tus oídos sentirían un golpe seco, mucho más brusco que al despegar en avión.",
            "Para algunos tímpanos, un cambio así de brusco podría ser demasiado.",
            "Y el cielo seguiría siendo azul: ese color lo pinta sobre todo el nitrógeno, que sigue ahí.",
        ],
    },
    {
        "id": "fuego",
        "frases": [
            "Segundo uno. Todos los fuegos del planeta se apagan a la vez.",
            "Velas, fogones, incendios forestales, todo. Sin oxígeno, nada puede arder.",
            "Los motores de los coches se apagan, pero los coches siguen rodando un buen trecho.",
            "Los motores de los miles de aviones que están en el aire también se apagan.",
            "Pero un avión no cae como una piedra: planea.",
            "En mil novecientos ochenta y dos, un jumbo británico lleno de pasajeros perdió sus cuatro motores por ceniza volcánica.",
            "Planeó más de siete kilómetros hacia abajo, los volvió a encender y aterrizó sin una sola víctima.",
            "El problema serían las centrales eléctricas: casi el sesenta por ciento de la electricidad del mundo sale de quemar combustibles.",
            "Al perder la llama, muchas se apagarían solas por seguridad, y podría haber apagones enormes.",
            "¿Y el Sol? Sigue brillando. El Sol no es fuego: es fusión nuclear, y no necesita oxígeno.",
        ],
    },
    {
        "id": "cuerpo",
        "frases": [
            "Segundo dos. Y ahora, lo que pasa dentro de ti.",
            "El oxígeno de tu sangre también es ese mismo gas, así que también desaparece.",
            "Tus células se quedan de pronto sin lo que necesitan para quemar su comida y fabricar energía.",
            "Y el que más lo nota es tu cerebro, que gasta energía como ningún otro órgano.",
            "En mil novecientos cuarenta y tres, unos médicos midieron cuánto aguanta despierta una persona cuando a su cerebro le cortan la sangre.",
            "La respuesta: unos seis o siete segundos.",
            "Cinco segundos está justo al borde.",
            "Casi todos sentiríamos un mareo extraño, la vista se cerraría como un túnel, y algunas personas podrían desmayarse.",
        ],
    },
    {
        "id": "regreso_a",
        "post": 1.5,
        "frases": [
            "Segundo cinco. El oxígeno vuelve.",
            "La presión sube de golpe, y tus oídos reciben otro golpe, ahora en sentido contrario.",
            "Las brasas calientes podrían volver a prender, y los pilotos encenderían de nuevo los motores.",
            "Habría choques, apagones y mucho susto, pero casi todos sobreviviríamos.",
            "Esa era la versión fácil.",
        ],
    },
    {
        "id": "atomos",
        "frases": [
            "Ahora, la versión difícil: desaparece cada átomo de oxígeno, esté donde esté.",
            "Y aquí está la sorpresa: el oxígeno no es solo un gas.",
            "Casi la mitad del peso de las rocas de la corteza terrestre es oxígeno.",
            "El agua es casi un noventa por ciento oxígeno, si cuentas su peso.",
            "Y tu propio cuerpo es oxígeno en dos terceras partes.",
            "El oxígeno es el pegamento que mantiene unido casi todo lo que tocas.",
        ],
    },
    {
        "id": "suelo",
        "frases": [
            "Segundo cero. Las rocas, la arena, el vidrio y el concreto pierden de golpe más de la mitad de sus átomos.",
            "Sin ese pegamento, no pueden seguir siendo sólidos.",
            "Los edificios se deshacen en polvo, las carreteras se desmoronan y el suelo bajo tus pies se hunde.",
            "Los metales, en cambio, siguen ahí, pero pierden la fina capa de óxido que los cubre.",
            "Y dos piezas de metal desnudo que se tocan se pueden pegar solas, como si las hubieran soldado.",
            "No es un invento: a eso se le llama soldadura en frío, y es un problema real en las naves espaciales.",
        ],
    },
    {
        "id": "agua",
        "frases": [
            "Segundo uno. El agua deja de ser agua.",
            "Sin su oxígeno, de cada molécula solo queda hidrógeno, el gas más ligero que existe.",
            "Los océanos, los ríos, las nubes, todo se convierte en hidrógeno.",
            "En el fondo del mar, aplastado por el peso de kilómetros de agua, ese gas se expandiría con una fuerza brutal.",
            "Y todo ese hidrógeno pesaría unas treinta veces más que nuestra atmósfera entera.",
        ],
    },
    {
        "id": "nosotros",
        "post": 1.5,
        "frases": [
            "¿Y nosotros?",
            "Si dos terceras partes de tu cuerpo desaparecen, no hay forma de sobrevivir.",
            "El agua de tus células, tus proteínas y hasta tu material genético llevan oxígeno.",
            "En esta versión, en un solo segundo, no quedaría ni un ser vivo en la superficie.",
        ],
    },
    {
        "id": "regreso_b",
        "post": 2.0,
        "frases": [
            "Y luego, en el segundo cinco, el oxígeno vuelve.",
            "Pero vuelve a un planeta revuelto, lleno de hidrógeno que ya se ha movido de su sitio.",
            "Y el hidrógeno mezclado con oxígeno es justo el combustible de muchos cohetes.",
            "Qué pasaría exactamente, nadie lo puede calcular. Pero no sería nada bonito.",
        ],
    },
    {
        "id": "realidad",
        "frases": [
            "Por suerte, el oxígeno no tiene un interruptor.",
            "Y no siempre estuvo aquí: hace unos dos mil cuatrocientos millones de años, la atmósfera casi no tenía.",
            "Lo fabricaron unas bacterias diminutas que aprendieron a vivir de la luz del Sol.",
            "Hoy, más o menos la mitad del oxígeno que respiras sale del océano, de seres tan pequeños que no se ven.",
        ],
    },
    {
        "id": "cierre",
        "frases": [
            "Así que la próxima vez que respires hondo, recuerda.",
            "Ese aire tardó miles de millones de años en existir.",
            "Y el planeta te lo regala, una vez cada pocos segundos.",
        ],
    },
]
