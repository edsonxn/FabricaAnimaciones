# -*- coding: utf-8 -*-
"""¿Qué pasaría si el Sol se apagara? — versión de 8 minutos, estilo Kurzgesagt, PLANO SECUENCIA (sin cortes).
Las "escenas" solo marcan secciones de narración y música; escenas.py dibuja un único mundo continuo.

Experimento: el Sol DESAPARECE (luz y gravedad). Si solo perdiera la luz, la Tierra seguiría en órbita.

Datos verificados (fuentes):
  - Más de 1,3 millones de Tierras cabrían en el Sol; 99,86 % de la masa del sistema solar;
    superficie ~5 500 °C, núcleo ~15 millones °C (NASA Sun facts).
  - ~600 millones de t de H/s fusionadas; ~4 millones de t/s convertidas en energía (E = mc²).
  - Luz: 8 min 20 s (499 s) hasta la Tierra; Mercurio 0,387 UA -> 3,2 min; Venus 0,723 UA -> 6,0 min;
    Júpiter 5,2 UA -> 43 min; Neptuno 30,07 UA -> 4,17 h.
  - Júpiter visible desde la Tierra 70-87 min más (su reflejo recorre 4,2-6,2 UA = 35-52 min).
  - Gravedad a la velocidad de la luz: GW170817 (2017), luz y ondas gravitacionales separadas 1,7 s
    tras ~130 millones de años de viaje.
  - Velocidad orbital 29,8 km/s -> 9,4e8 km/año; 4,24 años luz / 30 km/s ≈ 42 000 años.
  - Planetas errantes: podrían superar en número a las estrellas (Sumi et al. 2023, MOA-II).
  - Marea solar ≈ 46 % de la lunar: sin Sol, mareas más débiles.
  - −18 °C en una semana, −73 °C en un año, equilibrio ~−240 °C; árboles grandes aguantan décadas;
    el hielo aísla y el agua de abajo sigue líquida cientos de miles de años (D. Stevenson, Caltech;
    Popular Science). CO2 se congela a −78,5 °C; N2 a −210 °C; O2 a −218 °C.
  - Calor interno de la Tierra 47 ± 2 TW vs ~173 000 TW del Sol (≈ 3 700 veces) (Davies & Davies 2010).
  - Islandia: ~90 % de las casas con calefacción geotérmica (Islandsstofa / Gobierno de Islandia).
  - Fuentes hidrotermales con ecosistemas quimiosintéticos (descubiertas en 1977, rift de Galápagos).
  - ~70 % de las bacterias y arqueas viven bajo la superficie (Deep Carbon Observatory, 2018).
  - Fotones: 10 000 a 170 000 años del núcleo a la superficie; tiempo de Kelvin-Helmholtz ~30 millones
    de años; los neutrinos escapan del núcleo en ~2 s.
  - En ~1 000 millones de años el Sol evaporará los océanos; en ~5 000 millones, gigante roja;
    luego enana blanca que se enfría durante billones de años.
"""

TITULO = "¿Qué pasaría si el Sol se apagara?"
ARCHIVO = "si_el_sol_se_apagara_8min"
ESTILO_VISUAL = "kurzgesagt"
DURACION = 480.0
BPM = 110
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)
GAP = 0.75                                  # pausa entre frases (ritmo pausado de documental)
TRANSICIONES = [("continua", 0.1)] * 12      # plano secuencia: sin cortes
MUSICA = {
    "intro": dict(sabor="espacio"),
    "sol": dict(sabor="esperanza", raiz=41),
    "ocho": dict(sabor="tension"),
    "deriva": dict(sabor="vacio"),
    "errante": dict(sabor="espacio", raiz=38),
    "primer_dia": dict(sabor="vacio", raiz=38),
    "vida_sup": dict(sabor="tension", raiz=38),
    "frio": dict(sabor="vacio", raiz=36),
    "humanos": dict(sabor="esperanza", raiz=40),
    "profundidades": dict(sabor="espacio", raiz=40),
    "realidad": dict(sabor="esperanza", raiz=43),
    "futuro": dict(sabor="espacio", raiz=41),
    "cierre": dict(sabor="esperanza", raiz=43),
}

ESCENAS = [
    {
        "id": "intro",
        "post": 1.5,
        "frases": [
            "Imagina que, de repente, el Sol se apaga.",
            "Y no solo su luz: desaparece por completo, con toda su gravedad, en un instante.",
            "¿Cuánto tardaríamos en notarlo? ¿Qué le pasaría a la vida? ¿Podríamos sobrevivir?",
            "Es imposible, claro, pero es un experimento mental fascinante.",
            "Porque para entender qué perderíamos, primero hay que entender qué es el Sol.",
        ],
    },
    {
        "id": "sol",
        "post": 4.0,
        "frases": [
            "El Sol es una bola de gas tan enorme que dentro cabrían más de un millón de Tierras.",
            "Contiene más del noventa y nueve por ciento de toda la masa del sistema solar.",
            "Su superficie arde a unos cinco mil quinientos grados, y su núcleo, a unos quince millones.",
            "Ahí, cada segundo, fusiona unos seiscientos millones de toneladas de hidrógeno.",
            "Y unos cuatro millones de toneladas de esa materia se convierten en pura energía.",
            "Esa energía sale en forma de luz y de calor, y es lo que mantiene viva a la Tierra.",
            "En una sola hora, a la Tierra le llega casi tanta energía solar como la que toda la humanidad usa en un año.",
        ],
    },
    {
        "id": "ocho",
        "post": 3.0,
        "frases": [
            "Así que, si el Sol desapareciera ahora mismo, ¿qué notaríamos primero?",
            "Durante unos ocho minutos y veinte segundos, absolutamente nada.",
            "Es lo que tarda su luz en llegar hasta aquí: el Sol que ves en el cielo siempre es el de hace ocho minutos.",
            "Su última luz se alejaría como una burbuja que crece en todas direcciones.",
            "Mercurio se quedaría a oscuras a los tres minutos, y Venus a los seis.",
            "Y lo mismo pasa con la gravedad: sus cambios también viajan a la velocidad de la luz.",
            "En dos mil diecisiete lo comprobamos, cuando la luz y las ondas gravitacionales de un choque de estrellas lejano llegaron casi a la vez.",
        ],
    },
    {
        "id": "deriva",
        "post": 4.5,
        "frases": [
            "Cuando la burbuja nos alcanza, la Tierra, sin nada que la sujete, sale disparada en línea recta.",
            "No sentiríamos ningún tirón: no hay frenazo ni sacudida, solo un cambio de rumbo.",
            "La Luna, eso sí, seguiría girando a nuestro alrededor, porque la gravedad de la Tierra sigue ahí.",
            "Y la burbuja sigue avanzando: Júpiter se apaga a los cuarenta y tres minutos, y Neptuno pasadas cuatro horas.",
            "Curiosamente, desde aquí veríamos a Júpiter brillar todavía más de una hora, porque su último reflejo sigue viajando hacia nosotros.",
            "Uno a uno, los planetas se escapan: el sistema solar se deshace como un collar que se rompe.",
        ],
    },
    {
        "id": "errante",
        "post": 5.0,
        "frases": [
            "Viajando a unos treinta kilómetros por segundo, recorreríamos casi mil millones de kilómetros al año.",
            "Aun así, a esa velocidad, llegar hasta la estrella más cercana llevaría más de cuarenta mil años.",
            "La Tierra seguiría dando vueltas alrededor del centro de la galaxia, igual que antes, pero ya sin compañía.",
            "Chocar con otra estrella sería increíblemente improbable: el espacio entre ellas es gigantesco.",
            "Nos convertiríamos en un planeta errante, vagando a oscuras.",
            "Y no estaríamos solos: podría haber más planetas errantes que estrellas en la Vía Láctea.",
        ],
    },
    {
        "id": "primer_dia",
        "post": 3.0,
        "frases": [
            "Y aquí abajo, el cielo se vuelve negro.",
            "Sin luz que se disperse en el aire, verías las estrellas a mediodía.",
            "Tampoco habría Luna en el cielo: sin el Sol, no tiene luz que reflejar.",
            "Las mareas se debilitarían, porque el Sol también ayudaba a moverlas.",
            "Al principio no haría tanto frío: la Tierra guarda calor en el suelo, en el aire y, sobre todo, en los océanos.",
            "Pero en una semana, la temperatura media caería por debajo de dieciocho grados bajo cero.",
        ],
    },
    {
        "id": "vida_sup",
        "post": 3.5,
        "frases": [
            "Sin luz no hay fotosíntesis, y casi toda la vida depende de ella.",
            "Las plantas pequeñas morirían en unas semanas.",
            "Los árboles grandes aguantarían más, quizás décadas, gracias al azúcar que guardan en su interior.",
            "Pero los animales que comen plantas se quedarían sin comida, y después los que se comen a esos animales.",
            "Toda la cadena se vendría abajo.",
            "En el mar, el fitoplancton, que produce buena parte del oxígeno que respiramos, se apagaría en poco tiempo.",
            "Aun así, no nos asfixiaríamos: la atmósfera guarda oxígeno de sobra para miles de años.",
        ],
    },
    {
        "id": "frio",
        "post": 4.0,
        "frases": [
            "Después de un año, la temperatura rondaría los setenta y tres grados bajo cero.",
            "El tiempo atmosférico se apagaría: sin el calor del Sol, casi no habría viento, ni nubes, ni lluvia.",
            "Los océanos se congelarían desde arriba, pero ese hielo funcionaría como una manta.",
            "Debajo, el agua seguiría líquida durante cientos de miles de años.",
            "Cerca de los setenta y ocho grados bajo cero, el dióxido de carbono del aire empezaría a caer como nieve.",
            "Y dentro de millones de años, a unos doscientos cuarenta bajo cero, hasta el nitrógeno y el oxígeno se congelarían.",
            "El aire mismo acabaría en el suelo.",
        ],
    },
    {
        "id": "humanos",
        "post": 4.0,
        "frases": [
            "¿Y nosotros? Sorprendentemente, algunas personas podrían sobrevivir bastante tiempo.",
            "La Tierra tiene su propio calor interno, que sale lentamente desde sus profundidades.",
            "Es poquísimo comparado con el Sol, que nos da unas tres mil setecientas veces más energía.",
            "Pero en Islandia, ya hoy, nueve de cada diez casas se calientan con ese calor de la Tierra.",
            "Los paneles solares dejarían de servir, pero las centrales nucleares seguirían funcionando.",
            "Con energía geotérmica, reactores nucleares y cultivos bajo luz artificial, un grupo pequeño podría aguantar.",
            "Eso sí: sería una vida muy, muy oscura.",
        ],
    },
    {
        "id": "profundidades",
        "post": 4.5,
        "frases": [
            "Pero los verdaderos supervivientes ni siquiera se enterarían.",
            "En el fondo del mar, junto a fuentes hidrotermales, hay ecosistemas enteros que nunca han visto el Sol.",
            "Viven de la química de las rocas y del calor del interior del planeta.",
            "Allí hay gusanos gigantes de color rojo, alimentados por bacterias que llevan dentro.",
            "Y bajo nuestros pies, a kilómetros de profundidad, vive cerca del setenta por ciento de las bacterias y arqueas del planeta.",
            "Para ellos, la desaparición del Sol sería solo una noticia lejana.",
        ],
    },
    {
        "id": "realidad",
        "post": 4.0,
        "frases": [
            "Por suerte, nada de esto puede pasar.",
            "La materia y la energía no desaparecen sin más, y el Sol no tiene un interruptor.",
            "De hecho, la luz que te calienta hoy nació en su núcleo hace decenas de miles de años, o incluso más.",
            "Tarda todo ese tiempo en abrirse paso, rebotando de átomo en átomo, antes de escapar.",
            "Así que, aunque su núcleo se detuviera hoy, el Sol seguiría brillando durante millones de años.",
            "Solo lo notaríamos por los neutrinos, unas partículas fantasma que escapan del núcleo en segundos.",
        ],
    },
    {
        "id": "futuro",
        "post": 5.0,
        "frases": [
            "El Sol sí cambiará, pero muy despacio.",
            "Dentro de unos mil millones de años brillará tanto que evaporará nuestros océanos.",
            "En unos cinco mil millones de años se hinchará hasta convertirse en una gigante roja.",
            "La Tierra podría acabar dentro de ella, o quedarse como una roca calcinada.",
            "Y al final se encogerá en una enana blanca, que se irá apagando durante billones de años.",
        ],
    },
    {
        "id": "cierre",
        "frases": [
            "Hasta entonces, cada amanecer es un pequeño regalo.",
            "Porque casi todo lo que somos, la comida, el aire y el clima, funciona gracias a su luz.",
            "Así que mañana, cuando salga, dale las gracias.",
        ],
    },
]
