# -*- coding: utf-8 -*-
"""Hera llega al asteroide que chocó DART y muestra el CRÁTER (~9 min, horizontal). 4.º video de T Menos Cero.
Noticia de la semana (imágenes de la ESA del 25-nov-2026) explicada en LÍNEA 3D (`nucleo/linea3d.py` + `linea3d_espacio.py`)
+ VIDEO REAL de cada suceso (yt-dlp, con crédito: `_clips.py`) + fotos reales en marcos de alambre. Voz ElevenLabs «Alberto».
Datos comprobados el 26-nov-2026: `datos.md` (fuentes y lista de lo DUDOSO que no se dice). Sin subtítulos quemados.
"""

TITULO = "La NASA chocó contra un asteroide: este es el CRÁTER"
ARCHIVO = "hera_dart_crater"
ESTILO_VISUAL = "documental"     # kit linea3d + video real con capas
DURACION = None
BPM = 240
GAP = 0.42
SUBTITULOS = False
MEZCLA = dict(musica=-24.0, sfx=-22.0, fx=-17.0)
CER_MAX_POR_FRASE = {"gancho_4": 0.06, "pregunta_4": 0.06, "sigue_1": 0.06, "cierre_1": 0.10, "impacto_8": 0.06,
                     "imagenes_8": 0.06, "imagenes_7": 0.06}   # Whisper: «ERA» (Hera), «Lysiacube», «T-Cero»
TAIL_MAX_POR_FRASE = {}
GAP_MAX_POR_FRASE = {}
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1,
           stability=0.5)

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[serious] Esto es lo último que vio una nave de la NASA antes de estrellarse, a propósito, contra un asteroide.",
        "Fue hace cuatro años. El choque lo desvió, y se midió desde la Tierra.",
        "Pero nadie había visto cómo quedó el asteroide.",
        "[short pause] Hasta esta semana.",
        "Una sonda europea, Hera, llegó por fin al lugar del choque y mandó sus primeras fotos.",
        "Y lo que encontró es un cráter tan ancho como el asteroide entero, y un asteroide que ahora da tumbos.",
        "Esto es todo lo que pasó, explicado en tres dimensiones.",
    ]},
    {"id": "sistema", "frases": [
        "Empecemos por el blanco. En realidad, son dos asteroides.",
        "El grande se llama Didymos. Mide unos setecientos treinta metros, casi la altura del edificio más alto del mundo, y tiene forma de trompo.",
        "Gira sobre sí mismo cada dos horas y cuarto. Tan rápido que, en su ecuador, una piedra suelta casi sale volando.",
        "A su alrededor da vueltas una luna pequeña, Dimorphos, de unos ciento cincuenta metros. Más o menos un estadio de fútbol.",
        "Su nombre viene del griego y significa «el que tiene dos formas». Le queda perfecto, ya vas a ver por qué.",
        "Le daba una vuelta al grande cada once horas y cincuenta y cinco minutos.",
        "[short pause] Ninguno de los dos es un peligro para la Tierra. Por eso los escogieron.",
        "Y por otra razón: al ser una pareja, desde aquí se ve cómo uno pasa por delante del otro, y su brillo baja un poquito.",
        "Si empujas a la luna, su vuelta se hace más corta, y esas bajadas de brillo llegan antes.",
        "Esa era la prueba: ¿podemos mover un asteroide si le pegamos con una nave?",
    ]},
    {"id": "dart", "frases": [
        "La nave se llamó DART: Prueba de Redirección de Asteroide Doble.",
        "Despegó en noviembre de dos mil veintiuno, en un Falcon nueve, desde California.",
        "Era una caja de unos quinientos setenta kilos, con dos paneles solares largos que se desenrollaban como alfombras.",
        "No llevaba explosivos. Su única arma era la velocidad.",
        "Y su único instrumento era una cámara, llamada DRACO.",
        "En las últimas cuatro horas, un programa la guió sola, sin esperar órdenes de la Tierra.",
        "Viajó diez meses. Y quince días antes del choque, soltó a un pequeño acompañante italiano: LICIACube.",
        "Su trabajo era quedarse atrás y fotografiar lo que pasara.",
    ]},
    {"id": "impacto", "frases": [
        "Veintiséis de septiembre de dos mil veintidós, a once millones de kilómetros de la Tierra.",
        "DART iba a más de veintidós mil kilómetros por hora.",
        "Durante horas, Dimorphos fue apenas un punto de luz junto a Didymos.",
        "Dos minutos y medio antes del choque, todavía cabían los dos en la foto.",
        "Once segundos antes, Dimorphos apareció completo: una pelota de rocas sueltas.",
        "La cámara mandaba una foto cada segundo.",
        "[short pause] La última llegó incompleta. La nave ya no existía.",
        "En el centro de control, los ingenieros saltaban de sus sillas.",
        "Menos de tres minutos después pasó LICIACube, y vio esto: chorros de rocas y polvo saliendo del asteroide.",
        "Desde la Tierra, el brillo del sistema se triplicó.",
        "Y dos días después, un telescopio en Chile vio cómo esa nube se estiraba en una cola de más de diez mil kilómetros, como la de un cometa.",
    ]},
    {"id": "resultado", "frases": [
        "Ahora, la pregunta importante: ¿se movió?",
        "La NASA se conformaba con que la vuelta de Dimorphos cambiara setenta y tres segundos.",
        "[short pause] Cambió unos treinta y tres minutos.",
        "La luna ahora da su vuelta en once horas y veintitrés minutos, y quedó unos treinta y siete metros más cerca de Didymos.",
        "Y hay un detalle: el empujón fue mucho mayor que el golpe de la nave.",
        "DART arrancó más de mil toneladas de material, y todo eso salió disparado hacia atrás.",
        "Ese chorro empujó al asteroide hacia adelante, como el retroceso de un cañón. El empujón total fue de dos a cinco veces más fuerte.",
        "El choque cambió hasta la órbita de los dos alrededor del Sol. Apenas quince centésimas de segundo, pero cambió.",
        "Era la primera vez que la humanidad cambiaba a propósito el movimiento de un cuerpo del sistema solar.",
    ]},
    {"id": "pregunta", "frases": [
        "Pero quedaba un misterio. Desde aquí, los dos asteroides son un solo punto de luz.",
        "¿Qué tan grande quedó el cráter? ¿Cuánto pesa Dimorphos de verdad? ¿Se deformó entero?",
        "Los científicos hasta hacían apuestas: unos decían que habría un cráter pequeño, de unos diez metros. Otros, que el asteroide entero se habría deshecho y vuelto a armar.",
        "Sin esas respuestas, no sabemos cuánto empujón haría falta para desviar un asteroide peligroso.",
        "Para eso había que ir a ver. Y aquí entra Hera.",
    ]},
    {"id": "hera", "frases": [
        "Hera es de la Agencia Espacial Europea. Despegó en octubre de dos mil veinticuatro, también en un Falcon nueve, desde Florida.",
        "Es del tamaño de un coche pequeño, con dos alas de paneles solares.",
        "Lleva dos cámaras, una que ve en veinticinco colores a la vez, una cámara de calor hecha en Japón, y un láser para medir distancias.",
        "En marzo de dos mil veinticinco pasó a cinco mil kilómetros de Marte, y aprovechó para fotografiar a Deimos, su luna pequeña.",
        "La gravedad de Marte le dio un empujón gratis, y la puso rumbo a los asteroides.",
        "Llegó a principios de noviembre, un mes antes de lo previsto. Mira cómo crecen en sus fotos mientras se acerca.",
        "Y lo primero que vio fue el otro lado de Didymos, el que DART nunca fotografió.",
    ]},
    {"id": "imagenes", "frases": [
        "El veinticinco de noviembre, la Agencia Espacial Europea mostró lo que vio. Y lo hizo en la sala de los dinosaurios de un museo de Berlín.",
        "Este es Dimorphos hoy.",
        "La cara que golpeó DART quedó aplanada. El cráter es tan ancho como el asteroide entero.",
        "Les habían dicho que mediría unos diez metros.",
        "Y en el centro del cráter hay algo, una estructura rara, que todavía no saben qué es.",
        "Su científico principal lo resumió así: la respuesta a las apuestas fueron las tres cosas a la vez. Un cráter enorme, una forma nueva, y el resto del asteroide igual que antes.",
        "Porque fuera del cráter, las rocas se ven tal como en las fotos de DART.",
        "Y hay más. Antes, Dimorphos le enseñaba siempre la misma cara a Didymos, como la Luna a la Tierra.",
        "Ahora da tumbos. Es el objeto que gira de forma más caótica del sistema solar. Su giro no se puede predecir ni un día.",
        "Y la sorpresa final: alrededor de los dos asteroides flotan cientos de rocas que nadie había visto, de unos cuantos metros cada una.",
        "Los ingenieros tendrán que esquivarlas. Los científicos lo llamaron una aventura de Indiana Jones.",
    ]},
    {"id": "sigue", "frases": [
        "Y esto apenas empieza.",
        "En diciembre, Hera se acercará hasta unos trece kilómetros, para fotos mucho más nítidas.",
        "En enero soltará dos satélites del tamaño de una caja de zapatos: Milani, que estudiará el polvo, y Juventas, que llevará un radar para ver por dentro del asteroide.",
        "Será la primera vez que veamos el interior de uno. Y al final, Juventas intentará aterrizar.",
        "Con todo eso, por fin se podrá calcular cuánto empujó DART de verdad.",
    ]},
    {"id": "importa", "frases": [
        "¿Y por qué importa tanto?",
        "Hace sesenta y seis millones de años, un asteroide de unos diez kilómetros cayó en lo que hoy es la península de Yucatán, en México.",
        "Acabó con los dinosaurios y con tres de cada cuatro especies del planeta.",
        "Por eso la Agencia Espacial Europea presentó las fotos junto a los dinosaurios. El jefe de la misión bromeó: ellos no tenían una agencia espacial.",
        "En mil novecientos ocho, uno de apenas decenas de metros derribó el bosque en dos mil kilómetros cuadrados de Siberia.",
        "Y en dos mil trece, sobre Rusia, uno de unos veinte metros rompió ventanas en toda una ciudad y dejó casi mil quinientos heridos.",
        "DART y Hera nos enseñaron que, si lo vemos venir con años de aviso, no hace falta una bomba ni un héroe de película.",
        "Basta un empujón pequeño, a tiempo. Unos minutos de diferencia hoy son miles de kilómetros años después.",
        "Por primera vez, tenemos un plan que sabemos que funciona.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Y la próxima cita ya tiene fecha: el viernes trece de abril de dos mil veintinueve, el asteroide Apophis pasará más cerca que muchos satélites. Se podrá ver sin telescopio.",
        "Si quieres ver cada misión explicada así, en tres dimensiones, suscríbete a T Menos Cero.",
        "Y dime en los comentarios: ¿qué misión quieres que expliquemos después?",
        "[short pause] Nos vemos en la próxima cuenta regresiva.",
    ]},
]

for _e in ESCENAS[1:-1]:
    _e.setdefault("pre", 0.5)
    _e.setdefault("post", 1.2)
ESCENAS[0]["post"] = 0.4
ESCENAS[-1]["pre"] = 0.4
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo="Cinematic space-exploration explainer underscore: deep pulsing analog synth bass, precise ticking percussion, wide airy pads, "
           "curious and awe-struck like a mission control webcast, instrumental only, no vocals.",
    escenas={e["id"]: ("", 0) for e in ESCENAS},
    tramos=[(["gancho", "sistema"], "biblioteca"), (["dart", "impacto"], "biblioteca"), (["resultado", "pregunta", "hera"], "biblioteca"),
            (["imagenes", "sigue"], "biblioteca"), (["importa", "cierre"], "biblioteca")])

SFX_ELEVEN = {
    "hud": dict(prompt="Short soft digital interface beep, mission control telemetry readout, clean and quiet", seg=0.5, variantes=4),
    "tic": dict(prompt="Very short soft digital tick, a data row appearing on a screen", seg=0.3, variantes=3),
    "whoosh": dict(prompt="Deep smooth cinematic whoosh, camera moving fast through space", seg=1.3, variantes=3),
    "pulso": dict(prompt="Low cinematic sub bass hit with short reverb tail, dramatic title impact", seg=2.0, variantes=2),
    "rugido": dict(prompt="Rocket launch: engines roaring, deep crackling thunder rolling across the pad", seg=4.0),
    "impacto": dict(prompt="Massive deep cinematic impact boom with a crumbling rock debris tail, space collision", seg=3.0),
    "senal": dict(prompt="Radio telemetry signal cutting out into static, then silence", seg=1.5),
    "foto": dict(prompt="Soft digital camera shutter click with a tiny data blip", seg=0.4, variantes=3),
    "rocas": dict(prompt="Rocks and gravel tumbling and grinding, slow and heavy", seg=2.0),
    "despliegue": dict(prompt="Mechanical unrolling: a long spring-loaded panel unfurling with soft clicks", seg=1.8),
    "sello": dict(prompt="Rubber stamp slammed onto paper, firm thump", seg=0.6, variantes=2),
    "radar": dict(prompt="Low sonar radar ping pulsing slowly, deep and clean", seg=1.5),
    "alarma": dict(prompt="Low urgent warning tone, two electronic pulses", seg=1.2),
    "cristales": dict(prompt="Distant sonic boom followed by many windows shattering", seg=3.0),
}
