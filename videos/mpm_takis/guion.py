# -*- coding: utf-8 -*-
"""GUION — Mil por Minuto, 1.er video: cómo se fabrican los TAKIS + el negocio (19-nov-2026).
Motor SECUENCIA YT (docs/estilo_secuencia_yt.md) + kit nucleo/mg_planta.py. Fórmula: canales/formula/mil_por_minuto.md.
Datos: investigacion.md (cada cifra con su fuente; lo «NC» no se dice como hecho: el proceso genérico va como «este tipo de botana»).
Voz: Brian C de ElevenLabs (cálido, sin prisa, de quien recorrió la planta), eleven_v4_turbo, sin [whispers]/[excited]/[shouts].
"""

TITULO = "Así se FABRICAN los Takis y su negocio de 1,100 millones"
ARCHIVO = "mpm_takis"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
VOZ = dict(motor="elevenlabs", voice_id="Czw3Dn181ypdrCOnPfif", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"),
           referencia=r"C:\FabricaAnimaciones\videos\_muestras_voz_fallout\04_brian.mp3")
FONETICA = {}
# Whisper escribe «taquis/taqui», «Serviche», «Paki», «Barsel»: la voz los dice bien (revisado frase a frase el 19-nov-2026)
CER_MAX_POR_FRASE = {k: 0.07 for k in """intro_1 intro_5 intro_6 origen_0 origen_2 origen_4 origen_8 origen_9 proceso_1 proceso_4
    proceso_10 proceso_26 trivia_1 trivia_2 negocio_1 negocio_3 negocio_14 mitos_1 mitos_3 mitos_4 mitos_5 mitos_8 mitos_9 mapa_1 mapa_6
    cierre_2 proceso_9 negocio_8 mapa_5 origen_10 cierre_3""".split()}
TAIL_MAX_POR_FRASE = {"proceso_9": 1.25, "negocio_14": 1.25}   # terminan en palabra corta («se pega», «Número uno»)

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=7.5,             # canal de fábricas: cortes algo más rápidos que los de juegos (referencia: 1-2 s con MG encima)
    transicion="slideleft",
    fundido=0.30,
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern documentary underscore about factories and big business: pulsing muted synth arpeggios, light mechanical "
           "percussion like conveyor clanks, warm bass, curious and confident, instrumental only, no vocals, unobtrusive under narration.",
    escenas={
        "intro": ("curious and punchy, building momentum", 4),
        "origen": ("warm nostalgic Mexican family-business story, soft guitar texture over pulse", 3),
        "proceso": ("precise mechanical rhythm, steady and fascinating, ticking percussion", 4),
        "negocio": ("ambitious and rising, corporate growth, bigger drums", 4),
        "mitos": ("investigative and calm, slightly tense", 3),
        "mapa": ("expansive, travelling, wide", 3),
        "cierre": ("resolved and warm, gentle outro", 2),
        "suscripcion": ("light and friendly, the pulse keeps going", 3),
        "proceso_2": ("precise mechanical rhythm continues, a bit brighter, frying and packing energy", 4),
        "trivia": ("playful quiz pulse, light ticking", 3),
    },
    cortes={"proceso": [342.9]},          # «proceso» dura 276 s (> 175): se parte en la estación siete
    tramos=[(["intro"], "Begin with a punchy hit. Keep a steady pulse to the end."),
            (["origen", "suscripcion"], "Warm and nostalgic, then friendly. End on a held tone."),
            (["proceso"], "Mechanical and precise from the start. Keep the pulse; end flowing."),
            (["proceso_2", "trivia"], "Continue the mechanical pulse, brighter; the last section is a playful quiz."),
            (["negocio"], "Ambitious and rising throughout; end on a strong held chord."),
            (["mitos", "mapa"], "Calm investigative tension, then wide and travelling."),
            (["cierre"], "Resolved and warm, ending softly in the last seconds.")])

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[curious] Una bolsa morada. Un rollito de maíz del tamaño de tu dedo. Y ese polvo rojo que se te queda pegado en las uñas toda la tarde.",
        "Parece la botana más simple del mundo. [short pause] Pero solo en Estados Unidos, en un año, se vendieron mil cien millones de dólares de Takis.",
        "Mil cien millones. [short pause] De rollitos de tortilla.",
        "Para llegar a esa bolsa, el maíz pasa por una olla con cal, un molino, una máquina patentada que lo enrolla con mallas que cuelgan como cortina, aceite hirviendo y una nube de chile en polvo.",
        "Y detrás está una de las historias de negocios más raras de México: [short pause] la de una empresa de pan que no quiso comprar Sabritas, se arrepintió, y terminó inventando la botana que hoy le pelea el anaquel a Doritos.",
        "[thoughtful] Así que hoy entramos a la planta. ¿Cómo se fabrica realmente un Taki?",
        "Mira la esquina de tu pantalla: ese contador va sumando los dólares de Takis que se venden en Estados Unidos desde que empezó este video. Al final te digo cuánto juntó.",
    ]},
    {"id": "origen", "frases": [
        "Para entender los Takis primero hay que entender quién los hace: Barcel, la división de botanas de Grupo Bimbo.",
        "Sí, Bimbo. El del osito y el pan de caja.",
        "[amused] Y aquí viene la primera ironía. Roberto Servitje, uno de los fundadores de Bimbo, lo contó así en una entrevista: a Bimbo le ofrecieron comprar Sabritas. [short pause] Y no la compraron.",
        "Él mismo lo llamó un error. Sabritas terminó en manos de PepsiCo, y Bimbo tuvo que construir sus propias botanas desde cero.",
        "En los años setenta, Lorenzo y Roberto Servitje metieron a Barcel en el grupo para vender botanas y dulces, y pocos años después Barcel se separó para dedicarse solo a lo salado.",
        "Durante años, Barcel fue la competencia chica. [short pause] Nada que le quitara el sueño a Sabritas.",
        "Hasta 1999. [short pause] Lorenzo Servitje participaba en un grupo de creación de productos que cada semana votaba ideas nuevas. Un día llegó una que parecía un chiste: un totopo enrollado.",
        "Un taquito de tortilla, frito y bañado en chile y limón. Algo que cualquier mexicano reconoce en un segundo.",
        "¿Y el nombre? [amused] Según Roberto Servitje, salió de la suegra de Lorenzo, que decía que los mexicanos siempre andan comiendo taquis y tortis.",
        "Al principio se escribía con Q: en 2001 Grupo Bimbo pidió en Estados Unidos el registro de la marca TAQUIS. Con el tiempo, la Q se volvió K.",
        "Y en 2006 llegó el sabor que lo cambió todo, los Takis Fuego, de chile y limón, en su bolsa morada. Ese mismo año empezó a venderse en Estados Unidos.",
    ]},
    {"id": "suscripcion", "frases": [
        "[short pause] Antes de entrar a la planta: este es el primer video de Mil por Minuto. Aquí vamos a desarmar, pieza por pieza, cómo se fabrican las marcas que compras todos los días.",
        "Si te gusta saber qué hay detrás de las cosas, suscríbete. Es gratis, y me ayuda más de lo que crees.",
    ]},
    {"id": "proceso", "frases": [
        "Ahora sí. [short pause] Estación uno: el maíz.",
        "Todo empieza con maíz. No con harina de trigo ni con papa: maíz, como una tortilla. La etiqueta de los Takis en Estados Unidos lo dice clarito: harina de maíz procesada con cal.",
        "Y esa palabra, cal, es la clave de todo. [short pause] Estación dos: la nixtamalización.",
        "El grano se cuece en agua con cal y se deja reposar. Es la misma técnica que usaban en Mesoamérica hace miles de años.",
        "La cal afloja la cáscara del grano, le cambia la química a la masa y la vuelve elástica. Sin nixtamal no hay tortilla. [short pause] Y sin tortilla, no hay Taki.",
        "Estación tres: el molino. El maíz cocido se muele hasta volverse masa, la misma masa de la tortillería de tu colonia, pero por toneladas.",
        "Aquí la masa no tiene que ser bonita. Tiene que ser predecible. Si un lote sale más húmedo que otro, todo lo que viene después se descompone.",
        "Estación cuatro: el laminado. La masa entra a una tolva y unos rodillos de acero la aplanan hasta dejarla en una lámina delgada y continua.",
        "Estación cinco: el corte. Un rodillo cortador le da a cada pieza su forma, su tamaño y su grosor exactos. Todas iguales.",
        "Y aquí hay un truco que casi nadie conoce. Las piezas recién cortadas pasan a una banda que va más rápido que la anterior. ¿Por qué? [short pause] Para separarlas, porque la masa cruda se pega.",
        "Estación seis: el enrollado. [thoughtful] Y esta es la parte que hace a un Taki ser un Taki.",
        "En 2001, una empresa de Grupo Bimbo pidió la patente de una máquina que enrolla en crudo trozos de masa de maíz nixtamalizado en forma de taco. Sin parar.",
        "Primero, unas mallas de pre-enrollado le doblan una orilla a la pieza. Después, unas mallas de enrollado final, colgadas como una cortina, la van girando sobre sí misma hasta cerrar el rollito.",
        "Imagínalo: miles de pedacitos de masa pasando bajo una cortina de malla que los enrolla uno por uno, como alguien enrollando taquitos a mano, pero a la velocidad de una fábrica.",
        "Los inventores registrados son dos ingenieros mexicanos: Espiridión Valdés Rodríguez y Efraín Joel Peña Sánchez.",
        "Estación siete: la freidora. Los rollitos caen al aceite caliente. La etiqueta habla de aceite de palma, de soya o de canola.",
        "Ahí el agua de la masa se escapa en burbujas, el rollo se endurece y se fija para siempre. Lo que entró blando, sale crujiente.",
        "Y como freír cuesta muchísima energía, la planta de Barcel en Texas tiene un intercambiador que recupera el calor del aceite para volver a usarlo.",
        "Estación ocho: el sazonado. Y aquí es donde nace el famoso polvo.",
        "En este tipo de botanas, las piezas todavía calientes y con aceite entran a un tambor que gira, y una lluvia de sazonador las cubre por todos lados.",
        "¿Qué hay en ese polvo? Sal, maltodextrina, ácido cítrico, que es lo que te da el sabor a limón, azúcar, glutamato monosódico, cebolla, extracto de levadura, chile.",
        "[short pause] Y el color. En la bolsa de Estados Unidos dice Rojo 40 y Amarillo 6. En la de México, además, Amarillo 5. [short pause] Ese rojo que se queda en tus dedos no es solo chile.",
        "Estación nueve: el empaque. Una máquina forma la bolsa, la llena y la sella, todo en un solo movimiento.",
        "[amused] Y ojo con el aire. En 2018, un consumidor de Nueva York demandó a Barcel: alegaba que más de la mitad de la bolsa venía vacía.",
        "Ese aire, en este tipo de empaques, no está ahí para engañarte: es un colchón que protege a los rollitos para que no lleguen hechos polvo. Aunque, siendo honestos, a veces el colchón es generoso.",
        "Estación diez: las cajas y los camiones. De la línea, las bolsas van a cajas, las cajas a tarimas y las tarimas a la red de distribución de Bimbo, la misma que reparte el pan.",
        "Esa red es el arma secreta: el camión que deja el pan en la tiendita de la esquina, deja también los Takis.",
    ]},
    {"id": "trivia", "frases": [
        "Vamos con una pregunta, y la respuesta te la doy al final.",
        "Los Takis Fuego que se venden en Europa no usan el mismo color que los de México. ¿Con qué se pintan allá?",
        "¿A, con Rojo 40? ¿B, con pimentón y cúrcuma? ¿O C, con betabel? [short pause] Déjalo en los comentarios.",
    ]},
    {"id": "negocio", "frases": [
        "Ahora, el negocio. Porque fabricar un rollito es una cosa. Venderlo por miles de millones es otra.",
        "Durante años, todos los Takis que se comían en Estados Unidos se hacían en México y cruzaban la frontera.",
        "En 2011 Barcel abrió una planta en Mexicali, la planta número cien de Grupo Bimbo, pensada sobre todo para exportar.",
        "Y en 2012 dio el salto: una planta en Coppell, Texas, de unos veintiocho mil metros cuadrados, donde hoy se hace buena parte de los Takis de Estados Unidos.",
        "Pero lo interesante no es dónde los hicieron. Es dónde los vendieron.",
        "Mientras las grandes marcas peleaban por el pasillo del supermercado, los Takis se metieron por la puerta de atrás: tiendas de conveniencia y gasolineras, justo donde un adolescente gasta lo que trae en el bolsillo.",
        "Ya en 2013 un periódico de Houston escribía que en la primaria todavía mandaban los Flamin' Hot Cheetos, pero que en muchas secundarias ya mandaban los Takis.",
        "Un año después, Takis ganó el premio de Nielsen a la innovación en Estados Unidos. De más de diecisiete mil productos nuevos, solo catorce empresas lo ganaron.",
        "Y la marca habló como hablan los adolescentes: [amused] con un reto. ¿Eres lo bastante valiente para aguantar unos Takis? No era un anuncio. Era un desafío.",
        "Los números hablan solos. [short pause] En 2020, Takis vendía más de cuatrocientos millones de dólares al año en Estados Unidos.",
        "Cuatro años después, mil cien millones. Casi el triple.",
        "Para que lo dimensiones: en ese mismo año, Doritos vendió tres mil novecientos millones y Tostitos mil seiscientos. Un rollito mexicano ya juega en la misma liga que las marcas de PepsiCo.",
        "Tanto, que Doritos sacó en 2012 sus propios rollitos picantes, los Doritos Dinamita, y en 2024 los relanzó con un anuncio en el Super Bowl.",
        "Y en todo el mundo, la propia marca dice que Takis ya vende más de dos mil millones de dólares al año.",
        "[thoughtful] Roberto Servitje lo resumió en 2024 con una frase: los Takis son el producto que más vende Bimbo. [short pause] Número uno.",
        "La empresa que no compró Sabritas terminó inventando su propia estrella.",
    ]},
    {"id": "mitos", "frases": [
        "Pero con tanto picante, también llegaron los rumores. Vamos a separarlos con datos.",
        "Primero: ¿los Takis causan úlceras o cáncer? [short pause] Los verificadores de datos lo calificaron como falso.",
        "Lo que sí es real es el dolor de estómago cuando te comes de más. Un médico de un hospital infantil de Memphis dijo en 2018 que atendían fácilmente cien niños al mes con problemas de estómago ligados a botanas muy picantes.",
        "La respuesta de Barcel fue corta: los Takis son seguros, pero hay que disfrutarlos con moderación.",
        "Segundo: el famoso reto del chip más picante del mundo, el One Chip Challenge. [short pause] No era de Takis. Era de otra marca, Paqui, que retiró el producto en 2023.",
        "Tercero: en 2025 circularon videos que decían que los Takis eran mortales. Los verificadores lo desmintieron.",
        "Y cuarto, los colorantes. Aquí sí hay historia.",
        "California aprobó una ley que saca el Rojo 40, el Amarillo 5 y el Amarillo 6, entre otros, de la comida de las escuelas públicas a partir de finales de 2027. Ojo: no prohíbe venderlos en las tiendas.",
        "Y en 2026 Barcel empezó a quitar los colorantes artificiales de los Takis Fuego en Estados Unidos. Grupo Bimbo prometió hacerlo con todo su portafolio para finales de 2026.",
        "Así que el Taki rojo de toda la vida está cambiando de receta mientras ves este video. [short pause] Y en otro lugar del mundo, ya la cambiaron. Eso te lo cuento en la respuesta de la trivia.",
    ]},
    {"id": "mapa", "frases": [
        "Hagamos el mapa completo.",
        "En el Estado de México, la planta de Lerma: la dirección que viene impresa en la bolsa de Takis Fuego mexicana.",
        "En Sonora, Hermosillo, abierta en 2006, la misma temporada del Fuego.",
        "En Baja California, Mexicali, la planta de exportación, a minutos de la frontera.",
        "En Jalisco, Guadalajara, abierta en 2013.",
        "Cruzando la frontera, en el estado de Texas, la planta de Coppell, desde 2012.",
        "Y del otro lado del océano, en Inglaterra, una planta nueva en Rotherham, construida entre 2024 y 2025 para hacer Takis en Europa.",
        "De una olla con cal en México a una bolsa morada en una gasolinera de Texas o una tienda de Londres.",
    ]},
    {"id": "cierre", "frases": [
        "Así que la próxima vez que abras una bolsa morada, piensa en todo lo que pasó para llegar ahí.",
        "Maíz cocido con cal como hace miles de años. Una masa predecible. Una cortina de malla que enrolla taquitos sin parar. Aceite, polvo rojo y aire. [short pause] Y una familia que no compró Sabritas.",
        "La respuesta de la trivia: [short pause] la B. En Europa, los Takis Fuego se colorean con pimentón y cúrcuma. En México, con Rojo 40 y Amarillo 6. La misma bolsa, dos recetas.",
        "Y el contador de la esquina: mientras veías este video, en Estados Unidos se vendieron casi treinta mil dólares de Takis.",
        "Si quieres que entremos a la fábrica de otra marca, dime cuál en los comentarios. Y suscríbete a Mil por Minuto: aquí desarmamos lo que compras todos los días.",
    ]},
]
