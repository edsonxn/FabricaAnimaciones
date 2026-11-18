# -*- coding: utf-8 -*-
"""GUION — «Las 15 cosas que NUNCA debes hacer en Fallout 4» (Radio Yermo, 1.er video del canal, 17-nov-2026).
Motor SECUENCIA YT (docs/estilo_secuencia_yt.md § REGLA DE ORO y § Radio Yermo). Datos verificados en Fallout Wiki:
_investigacion_A.md (misiones) y _investigacion_B.md (mecánicas), con URL (van en la descripción; la voz NO cita fuentes).
Tema elegido por el usuario entre 3 (Tamriel «15 misiones NUNCA» ×10,7; IGN «9 cosas que NO debes hacer en Fallout 4» 796 mil).
Narrador = «el Locutor» de Radio Yermo: el Profeta de ElevenLabs con el filtro de radio MODO B (elegido por el usuario):
saludo, remates, suscripción y despedida POR LA RADIO (VOZ_FX "radio" / "radio+sintonia"); los datos con el narrador cerca
del micrófono (VOZ_FX_DEFECTO = "tinte"). Plano, sarcasmo seco, sin risas ni [whispers]/[excited]. Canal sin comentarios aún.
Nombres dudosos en el juego en español evitados en la voz («Gran líder», el código del parque eólico, «Psico/Psycho»).
"""

TITULO = "Las 15 cosas que NUNCA debes hacer en Fallout 4"
ARCHIVO = "fo_nunca_f4"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {}
CER_MAX_POR_FRASE = {'p14_2': 0.024, 'p13_5': 0.017, 'p10_0': 0.065, 'p10_5': 0.057, 'p8_5': 0.037, 'p7_3': 0.017, 'p5_2': 0.083, 'subs_0': 0.037, 'p3_1': 0.019, 'p2_2': 0.021}   # 17-nov: Whisper escribe rats/Voltec/Singin/Cuddy/Kremf/Emojini/vatio; tomas completas
TAIL_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Fallout 4", min_s=40, max_min=240, alto=1080,
            evitar_canales=["AdayCanarioWTF"]),   # webcam fija en todo su gameplay
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Fallout 4 (Inon Zur; armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Buenos días, Yermo. Aquí Radio Yermo, transmitiendo desde lo que queda de la Commonwealth.",
        "Hoy, un servicio a la comunidad. Las quince cosas que nunca, jamás, debes hacer en Fallout cuatro.",
        "Un niño del Refugio ochenta y uno que muere por diez puntos de vida. Una servoarmadura que se queda en el fondo de un pozo para siempre.",
        "Un viejo con corona encerrado desde mil ochocientos noventa y ocho, y un pueblo entero que desaparece en la niebla por un código en una terminal.",
        "[deadpan] Todo comprobado en el juego. Y el número uno no tiene arreglo: quédate hasta el final.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Dejar a un enemigo legendario a medias.",
        "Ves la estrella junto al nombre, le pegas fuerte, le bajas más de la mitad de la vida y piensas que ya casi está.",
        "Error. En cuanto un golpe lo deja por debajo del cincuenta por ciento sin matarlo, muta. Recupera toda la vida y se envuelve en un aura.",
        "Si es una criatura, pega el doble. Si es humano o supermutante, más daño y puntería perfecta. Solo pasa una vez, pero esa vez duele.",
        "Lo correcto es guardar el golpe gordo para después de la mutación. Primero lo provocas, luego lo rematas.",
        "[sarcastic] Es como gastar todas las balas en el primer acto. El segundo acto también existe.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. Entrar al Mar Resplandeciente sin protección.",
        "El suroeste de la Commonwealth es un desierto verde, con tormentas radiactivas casi constantes.",
        "En Fallout cuatro, cada diez rads te quitan un uno por ciento de tu vida máxima, y esa vida no vuelve sola. Con mil rads, mueres.",
        "Un personaje de nivel bajo o medio, sin traje ni servoarmadura, dura menos de dos minutos ahí dentro. Y en el centro del Cráter del Átomo la radiación llega a trescientos rads por segundo.",
        "Lleva un traje Hazmat o servoarmadura, Rad-X antes de entrar y RadAway en el bolsillo.",
        "[deadpan] El mar brilla. Tú también vas a brillar. Una sola vez.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. Dejar que el supermutante suicida llegue hasta ti.",
        "Es un supermutante que viene corriendo hacia ti con una minibomba encendida en la mano derecha.",
        "Si detona, son cuatrocientos cincuenta de daño de golpe. De cerca, sin servoarmadura, es casi imposible sobrevivir.",
        "La salida es dispararle al brazo de la bomba cuando todavía está lejos, para que reviente él solo. Y si lo matas sin tocar el brazo, la minibomba es tuya.",
        "En el hospital de Medford te espera uno en la entrada y otro sentado en el vestíbulo.",
        "[sarcastic] Y sí, hay un logro por dejar que uno te mate, y ese logro, que se llama Touchdown, te premia hasta por morir mal.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Caer desde lo alto con servoarmadura junto a gente amiga.",
        "La servoarmadura anula todo el daño por caída. Puedes saltar desde un edificio y aterrizar como un héroe de película.",
        "El problema es el aterrizaje. El impacto daña mucho a quien esté cerca, amigo o neutral, y ese personaje, o toda su facción, se vuelve hostil.",
        "Y a tus compañeros la servoarmadura no los protege de la caída. Ellos sí se rompen las piernas.",
        "[deadpan] Aterrizaje heroico, tres tenderos muertos y una ciudad entera disparándote. Bienvenido a Diamond City.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Guardar tus cosas en un baúl que no es tuyo.",
        "Encuentras una caja fuerte en una casa abandonada y dejas ahí tu munición, tus armas y tu chatarra, porque total, por esa casa nunca pasa nadie.",
        "Pues los objetos que dejas en un contenedor fuera de tus asentamientos desaparecen con el tiempo. El juego reinicia esas cajas.",
        "Solo están a salvo los contenedores de los asentamientos que controlas, como el taller de Sanctuary Hills.",
        "[deadpan] El Yermo no roba. El Yermo hace limpieza.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. Recoger un cabezón de Vault-Tec antes de tiempo.",
        "Hay un cabezón por cada atributo de S.P.E.C.I.A.L., fuerza, percepción, resistencia y el resto, y cada uno te sube un punto.",
        "Si recoges el cabezón cuando ya tienes ese atributo en diez, sube a once. Por encima del máximo.",
        "Pero si lo recoges antes, cuenta como una subida normal, y luego ya no puedes llevar ese atributo por encima de diez. El once lo perdiste.",
        "El de fuerza, por ejemplo, está en el edificio de Mass Fusion, sobre la cabeza de una estatua de metal, cinco pisos por encima del mostrador.",
        "[sarcastic] Un muñequito de plástico que castiga la impaciencia, una idea muy propia de la empresa de los refugios.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Darle a la vidente, Mamá Murphy, su quinta dosis.",
        "Mamá Murphy vive en Sanctuary Hills, en su sillón, y a cambio de drogas tiene visiones de tu futuro.",
        "Y funcionan: te da la contraseña de la banda de Skinny Malone, te dice dónde está la llave de Kellogg y hasta te da una ventaja, porque en la pelea Kellogg te hace un veinticinco por ciento menos de daño.",
        "Pero solo tiene cinco visiones. La quinta dosis es una sobredosis, y Mamá Murphy muere en su sillón. Los colonos de Sanctuary se juntan a llorarla.",
        "Hay otra salida: dos pruebas difíciles de carisma para convencerla de que lo deje. Pierde la visión, pero vive.",
        "[deadpan] La única vidente del Yermo y no vio venir la quinta dosis.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Dejar la servoarmadura con el núcleo de fusión puesto.",
        "Aparcas tu armadura en el asentamiento, te vas de viaje y vuelves. Y la armadura no está.",
        "Los colonos y los compañeros se llevan cualquier servoarmadura que tenga un núcleo puesto. La usan en los ataques de saqueadores y luego la dejan donde se acuestan o donde hacen guardia.",
        "La estación de servoarmadura solo frena a los colonos ociosos. Y un colono con láser Gatling le saca el núcleo a su propia arma para meterse en tu armadura.",
        "La regla es sencilla: al bajarte, saca el núcleo. Sin núcleo, nadie la mueve.",
        "[sarcastic] Comunismo de asentamiento. Lo tuyo es de todos, sobre todo si tiene batería.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. Matar a Sinjin de un disparo furtivo.",
        "En la misión de la Mortaja Plateada, en Goodneighbor, el saqueador Sinjin secuestra a Kent Connolly y te espera en el hospital Milton General.",
        "Lo lógico es esconderte y darle un tiro a la cabeza. Y es lo peor que puedes hacer: si matas a Sinjin con un disparo furtivo, sus saqueadores se giran y matan a Kent.",
        "Si Sinjin te descubre y lo pierdes de vista, también lo mata. Salvarlo a tiros es casi imposible.",
        "La salida segura es intimidarlo con carisma, o entrar en V.A.T.S. Si Kent muere, pierdes las tres mejoras del traje y su radio se apaga.",
        "[deadpan] El héroe de la radio, con la radio apagada. Eso sí que no lo perdono.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. Volar el Instituto sin dar la orden de evacuación.",
        "En la misión final, La opción nuclear, hay un objetivo opcional que mucha gente se salta: dar la orden de evacuación desde la terminal del director.",
        "Si no lo haces, todos los que siguen dentro mueren con la explosión.",
        "Y la próxima vez que te vea el Ferrocarril, toda la facción se vuelve hostil. Preston te reprocha haber bajado a los Minutemen al nivel del Instituto.",
        "[deadpan] Por un objetivo opcional pierdes una facción entera, así que lee la lista de tareas, que para eso está.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Quedarte la cura del Refugio ochenta y uno.",
        "En la sección secreta del Refugio ochenta y uno te muerde una rata topo y te contagias. Al mismo tiempo, un niño, Austin, se está muriendo de lo mismo.",
        "Curie solo puede hacer una dosis de la cura. Una.",
        "Si no se la das a Austin, Austin muere, y todo el refugio te culpa. Le ponen un pequeño memorial en el aula: una vela, un cochecito, un guante de béisbol y un osito.",
        "Pierdes el rifle de jeringas y tu habitación en el refugio. ¿Y qué te curaste? Diez puntos de vida máxima.",
        "[deadpan] Diez puntos. Hay estimulantes que curan más que eso.",
    ]},
    {"id": "subs", "frases": [
        "[deadpan] Una pausa en la transmisión. Radio Yermo acaba de encender la antena, y cada suscripción es un watt más de señal.",
        "Si te está sirviendo, suscríbete y activa la campana, porque todavía quedan cuatro puestos y los que vienen duelen mucho más.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Hacerte jefe de los saqueadores de Nuka-World.",
        "Nuka-World te ofrece ser el jefe de sus bandas de saqueadores, y luego te pide conquistar asentamientos en la Commonwealth.",
        "En cuanto montas tu primer puesto de saqueadores, Preston Garvey pasa a odiarte en ese mismo instante, aunque tengas su afinidad al máximo.",
        "Deja de trabajar contigo, y aunque luego te vuelvas contra los saqueadores, su confianza se pierde para siempre.",
        "[sarcastic] Y el hombre que te mandaba a defender cada asentamiento de la Commonwealth por fin deja de pedírtelo. Era la única forma.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Bajar con servoarmadura al pozo inundado de Dunwich Borers.",
        "Al fondo de la cantera, en el noreste del mapa, hay un pozo inundado, y en un túnel bajo el agua está el Diente de Kremvh, un arma única, junto a dos minibombas en un altar.",
        "Con servoarmadura no puedes nadar. Te hundes y caminas por el fondo. Y las paredes del pozo son verticales: no hay forma de subir.",
        "Tienes que salirte de la armadura bajo el agua, y el armazón se queda ahí para siempre. Solo lo recuperas si un compañero se mete dentro y luego viajas rápido, o cargando la partida.",
        "Y aunque el casco te deja respirar unos minutos bajo el agua, después te ahogas.",
        "[deadpan] Un arma por una servoarmadura. Negocio redondo para el pozo.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Liberar a Lorenzo Cabot.",
        "En el sótano del Manicomio Estatal Parsons hay un hombre encerrado por su propio hijo desde mil ochocientos noventa y ocho. Lorenzo Cabot, con una corona en la cabeza y poderes que desvían granadas.",
        "Jack Cabot te pide activar cuatro interruptores para inundar la celda con radiación y acabar con él. Si en vez de eso abres la puerta y te pones de su lado, Lorenzo va a la Casa Cabot y mata a Jack, a Wilhelmina y a Emogene.",
        "A cambio te promete suero misterioso de por vida: más fuerza, más resistencia y menos radiación durante una hora. Pero te da uno cada vez, y no se puede vender.",
        "Y pierdes para siempre el Artefacto de Lorenzo, el arma que Jack te da si haces lo correcto.",
        "[deadpan] Una familia entera por un suero que te dan de uno en uno. Ni el Instituto hace tratos tan malos.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. Meter el código en la terminal del parque eólico de La Isla.",
        "En Far Harbor, el pueblo sobrevive gracias a los condensadores de niebla, que mantienen lejos la Niebla y a sus criaturas.",
        "En los recuerdos de DiMA está el código para apagar las turbinas del parque eólico, y Tektus, el líder de los Hijos del Átomo, quiere que lo uses.",
        "Si lo metes, se corta la electricidad de los condensadores, y la Niebla se traga Far Harbor. El pueblo queda en ruinas y casi todos sus habitantes mueren. El Viejo Longfellow se vuelve tu enemigo.",
        "Fallan todas sus misiones, y la recompensa de los Hijos del Átomo es un objeto único y una ventaja. Un pueblo entero, por un objeto y una ventaja.",
        "[sighs] Así se borra un pueblo entero en Fallout cuatro: con una sola línea de código, y sin disparar ni una bala.",
    ]},
    {"id": "cierre", "frases": [
        "Esas son las quince. Y ahora dime en los comentarios cuál de estas hiciste tú, porque alguien dejó morir a Austin y alguien sigue buscando su servoarmadura en el fondo de un pozo.",
        "Todos los comentarios se leen, y los mejores salen en la próxima transmisión.",
        "Y si te gusta Skyrim, el canal hermano es Crónicas de Tamriel. Misma receta, otro fin del mundo.",
        "[deadpan] Esto fue Radio Yermo. Suscríbete, no salgas del refugio sin escucharnos, y recuerda: en el Yermo, el que no lee la lista de tareas, la repite.",
    ]},
]

# ------------------------------------------------------------------ filtro de radio (modo B, nucleo/voz_fx.py → mezcla)
VOZ_FX_DEFECTO = "tinte"                     # los datos: narrador cerca del micrófono con un toque de radio
VOZ_FX = {"intro_0": "radio+sintonia", "subs_0": "radio+sintonia", "subs_1": "radio",
          "cierre_3": "radio+sintonia"}
for _e in ESCENAS:                            # el remate de cada puesto sale por la radio del Yermo
    if _e["id"].startswith("p"):
        VOZ_FX[f"{_e['id']}_{len(_e['frases']) - 1}"] = "radio"
