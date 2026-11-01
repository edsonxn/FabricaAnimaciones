# -*- coding: utf-8 -*-
"""Sapiens con Wifi — «¿Cómo sobrevivían los humanos antiguos SIN medicina?»  Motor SECUENCIA, ~8-9 min, EN ESPAÑOL.
Primer video del canal con el sistema de Wild Next Door (imágenes y clips de Google Flow, dibujo animado de tinta gruesa
y color plano, un dibujo por frase), con mascota propia «Sapi» (diadema con el símbolo de wifi, guiño al nombre del canal).
Formato copiado de fuera (ideas 12-oct-2026): Mango Explica SP «¿Cómo sobrevivieron los humanos antiguos sin medicina?»
(×11, 40 mil vistas) y otros 3 de supervivencia del mismo canal (×3 a ×6); gancho de segunda persona («tú existes porque
todos tus ancestros sobrevivieron») y mito de «morían a los treinta» anunciado al inicio y resuelto en la escena 2.
Primeros ~70 s en VIDEO: 7 clips de 10 s = 49 puntos de Flow (el usuario tiene 50), dos escenas por clip.
Hechos usados (revisados el 12-oct-2026; los que son hipótesis llevan «quizá / los científicos creen» en el guion):
- Esperanza de vida: Gurven y Kaplan 2007 («Longevity among hunter-gatherers», Population and Development Review):
  al nacer ~30-40 años por la mortalidad infantil; ~60 % llega a los 15 (≈ 4 de cada 10 muere antes); edad modal de
  muerte adulta 68-78 años (mediana ~72).
- El Sidrón (Asturias, ~49 000 años; Weyrich et al. 2017, Nature): sarro dental de un joven neandertal con absceso en la
  mandíbula y parásito intestinal: ADN de álamo (ácido salicílico) y de Penicillium; solo él. No prueban que fuera remedio.
- Orangután Rakus (Suaq Balimbing, Sumatra; Laumer et al., Scientific Reports, junio 2024; herida en 2022): masticó hojas
  de Fibraurea tinctoria (antiinflamatoria, analgésica) y las aplicó a la herida de la cara; cerrada en < 1 semana sin infección.
- Riparo Villabruna (Italia; Oxilia et al. 2015, Scientific Reports): tercer molar de un joven de ~25 años, ~14 000 años,
  caries grande con estrías hechas EN VIDA con puntas de pedernal (limpieza/escarbado): tratamiento dental más antiguo.
- Eslovenia (Bernardini et al. 2012, PLOS ONE): canino de ~6 500 años con grieta rellena de cera de abeja, hecha poco antes
  o después de morir; si fue en vida, relleno terapéutico más antiguo.
- Trepanación en Perú (Kushner, Verano y Titelbaum 2018, World Neurosurgery; 59 cráneos…): supervivencia (hueso nuevo) 40 %
  en 400-200 a. C., hasta 75-83 % en época inca (otra cifra: 91 % en 1000-1400); mortalidad inca 17-25 % frente a 46-56 % en
  la Guerra Civil de EE. UU. (~1860).
- Shanidar 1 (Irak, neandertal; Solecki, Trinkaus): golpe en la cara, brazo derecho dañado, pierna lesionada, probable
  sordera parcial; vivió ~40-50 años: los investigadores creen que lo cuidó el grupo.
- Dmanisi (Georgia, ~1,77 millones de años; Lordkipanidze et al. 2005, Nature): cráneo con un solo diente, el resto
  perdido años antes de morir; se cree que sobrevivió con ayuda.
- Liang Tebo (Borneo, Kalimantan Oriental; Maloney et al. 2022, Nature): amputación quirúrgica de la pierna izquierda por
  debajo de la rodilla de un niño, hace ≥ 31 000 años; sin signos de infección; vivió 6-9 años más; antes, la cirugía más
  antigua conocida tenía ~7 000 años (brazo, agricultor de Francia).
- Hombre de Hielo (Ötzi, Alpes, ~5 300 años, hallado en 1991): llevaba trozos de Fomitopsis betulina (hongo del abedul) y
  tenía tricocéfalo (Trichuris); que fuera remedio es hipótesis (también sirve de yesca); tatuajes sobre articulaciones
  desgastadas, utilidad terapéutica debatida. Se evita el nombre «Ötzi» en la voz (Whisper lo deforma).
- Botiquín: la aspirina (Bayer, 1897) deriva de la salicina de la corteza de sauce; la penicilina la descubrió Fleming en
  1928 de un moho Penicillium.
"""

TITULO = "¿Cómo sobrevivían los humanos antiguos SIN medicina?"
ARCHIVO = "sin_medicina"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 100
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Falsos positivos de Whisper que se ajustan al oír las tomas (se llena tras `seleccionar`)
CER_MAX_POR_FRASE = {}

SECUENCIA = dict(
    clips_s=[10] * 6,         # 6 x 10 s = 42 puntos (el saldo real dio para 6), 60 s de video al inicio
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    recorte_por={"scene-002": 0.035, "scene-003": 0.04, "scene-005": 0.035},   # marcos de viñeta medidos en el MASTER (12-oct)
    carpeta_descargas="flow-sin_medicina",
)

FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "sapi": "Sapi, a cartoon prehistoric human with a round peach-colored head, two big friendly dot eyes, messy "
                "brown hair, a simple brown fur tunic, and a thin headband with a small white wifi symbol made of "
                "three curved arcs and a dot",
        "neandertal": "a stocky cartoon Neanderthal with a heavy brow ridge, a wide nose, long dark hair and a beard, "
                      "a rough gray fur wrap, and a tiny red feather in the hair",
        "nino": "a cartoon young boy of the Stone Age in a tropical rainforest cave, with a round face, big dot eyes, "
                "black hair, a short leaf and hide wrap, and his left leg ending just below the knee, walking with "
                "a wooden crutch",
    },
    objeto="a simple pill, drawn as a small white-and-pink capsule, only when the scene is about modern medicine",
    epoca="the Stone Age: caves, rock shelters, campfires, forests, stone tools, animal hides; no metal, no modern "
          "objects except in the scenes about the present-day medicine cabinet",
    cierre="No text, no letters, no words, no logos, no watermark. Every box, jar and bag is plain and unlabeled.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Warm, curious, lightly humorous documentary score for a hand-drawn cartoon about prehistoric survival: "
           "marimba, wooden flute, soft hand drums, pizzicato strings, celesta, upright bass and brushed percussion. "
           "Playful and human, with moments of wonder and tenderness. Never epic, never horror, no modern electronics.",
    escenas={
        "hook": ("Quiet modern morning feel turning to wonder: soft felt piano and pizzicato, then a gentle drum pulse "
                 "arrives as the question is asked, a small mysterious flute figure.", 3),
        "mito": ("Light debunking groove: marimba ostinato, walking upright bass and brushed percussion, a wink of "
                 "humor, steady and confident.", 4),
        "plantas": ("Forest and cave atmosphere: wooden flute over soft hand drums, curious celesta sparkles when the "
                    "discovery is revealed, a little playful for the orangutan.", 4),
        "otzi": ("Icy and mysterious then warm: a held celesta tone like frozen air, soft flute, a gentle curious "
                 "groove with pizzicato.", 3),
        "dientes": ("Slightly nervous and comic: tiptoeing pizzicato, muted marimba, a small wince, then relief and "
                    "warmth.", 4),
        "trepanacion": ("Dramatic but wondering: low drums and cello, tension building slowly, then resolving to a hopeful "
                        "major phrase on flute.", 5),
        "cuidado": ("Tender and gentle: felt piano and soft strings, warm and caring, almost a lullaby with a quiet "
                    "flute melody.", 2),
        "amputacion": ("Quiet mystery growing into awe: sparse flute and soft low drums, a patient build to one "
                       "luminous, moving moment, then a calm human warmth.", 5),
        "botiquin": ("Clear and friendly modern groove: light pizzicato and piano, marimba, a gentle smile in the "
                     "music.", 3),
        "outro": ("Return to the opening theme, now warm and resolved: celesta, felt piano and flute, a smile, then a "
                  "calm slow fade.", 3),
    },
    tramos=[
        (["hook", "mito"],
         "Begin from near silence. End on a held suspenseful tone that can flow into the next piece. No loud ending."),
        (["plantas", "otzi", "dientes"],
         "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["trepanacion", "cuidado"],
         "Begin gently with a held tone. End on a sustained calm chord that can flow into the next piece."),
        (["amputacion", "botiquin", "outro"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "Piensa en lo último que te dolió. Una muela, una herida, una fiebre.",
        "Hoy vas a la farmacia, tomas una pastilla, y en dos días estás como nuevo.",
        "Ahora imagina ese mismo dolor hace treinta mil años.",
        "Sin farmacia. Sin doctor. Sin anestesia. Sin saber siquiera que las bacterias existen.",
        "Seguro has escuchado que los humanos de esa época morían a los treinta años, porque no había medicina.",
        "Pero entonces hay una pregunta incómoda.",
        "Tú estás vivo. Y eso significa que todos tus ancestros sobrevivieron.",
        "Todos. Sin una sola excepción. Durante trescientos mil años.",
        "Sobrevivieron a huesos rotos, infecciones, parásitos y partos complicados.",
        "Y sin una sola pastilla.",
        "¿Cómo lo hicieron?",
        "En este video vas a conocer cuatro historias reales, descubiertas por arqueólogos.",
        "Una de ellas cambió lo que la ciencia creía sobre quién inventó la cirugía.",
        "Pero antes, vamos a desmontar ese mito de los treinta años.",
    ]},
    {"id": "mito", "frases": [
        "Primero, el mito. ¿De verdad la gente moría a los treinta años?",
        "No exactamente. Ese número sale de un promedio, y los promedios engañan.",
        "En los grupos de cazadores recolectores que se han estudiado, la esperanza de vida al nacer era de treinta o cuarenta años.",
        "Pero eso pasaba porque morían muchísimos bebés y niños. Cuatro de cada diez no llegaban a los quince años.",
        "Esas muertes tempranas bajan el promedio de todos.",
        "En cambio, quien llegaba a los quince tenía muy buenas probabilidades de vivir muchos años más.",
        "En esos grupos, la edad en que más adultos morían estaba entre los sesenta y ocho y los setenta y ocho años.",
        "No eran inmortales. Pero tampoco eran jóvenes condenados. Sabían arreglárselas.",
        "Y su primera botica estaba en el bosque.",
    ]},
    {"id": "plantas", "frases": [
        "Primera historia. Una cueva en el norte de España, llamada El Sidrón.",
        "Hace casi cincuenta mil años vivía ahí un grupo de neandertales.",
        "Los científicos analizaron el sarro de sus dientes, esa capa dura que el dentista te quita.",
        "Ahí quedan atrapados restos de todo lo que alguien masticó.",
        "Un joven tenía un absceso en la mandíbula, una infección dolorosísima, y además un parásito en el estómago.",
        "En su sarro apareció ADN de álamo, un árbol que contiene ácido salicílico, el ingrediente base de la aspirina.",
        "Y también un moho llamado Penicillium, el mismo hongo del que sale la penicilina.",
        "Los otros neandertales de la cueva no tenían ni una cosa ni la otra.",
        "Los investigadores son cautelosos, porque no pueden demostrar que fuera un remedio. Pero el álamo no es comida, y ese joven estaba enfermo.",
        "Y esto no es solo cosa nuestra. En dos mil veintidós, unos científicos vieron a un orangután de Sumatra llamado Rakus con una herida abierta en la cara.",
        "Masticó hojas de una liana que calma la inflamación, y se las puso sobre la herida como una pasta.",
        "La herida se cerró en menos de una semana, sin infectarse.",
        "Fue la primera vez que se vio a un animal salvaje curarse así. Quizá esa habilidad es más vieja que nuestra especie.",
    ]},
    {"id": "otzi", "frases": [
        "Y hay otro botiquín, mucho más famoso, que aguantó cinco mil trescientos años congelado.",
        "En mil novecientos noventa y uno, unos excursionistas encontraron en los Alpes el cuerpo de un hombre momificado por el hielo.",
        "Lo llamaron el Hombre de Hielo. Y entre sus cosas llevaba trozos de un hongo que crece en los abedules.",
        "Su cuerpo tenía parásitos intestinales, y ese hongo se ha usado en la medicina popular contra ellos.",
        "Los científicos creen que quizá lo cargaba como remedio, aunque ese mismo hongo también sirve para encender fuego.",
        "Además tenía tatuajes en las rodillas y en la espalda, justo donde le dolían las articulaciones. ¿Una terapia? Nadie lo sabe.",
    ]},
    {"id": "dientes", "frases": [
        "Segunda historia. Las muelas.",
        "Hoy un dolor de muelas te manda corriendo con el dentista. Hace catorce mil años no había dentistas. O eso creíamos.",
        "En una cueva de Italia, llamada Riparo Villabruna, apareció la muela de un joven de unos veinticinco años.",
        "Tenía una caries enorme. Y alrededor de ella, rayones diminutos.",
        "Los investigadores los repitieron en el laboratorio y concluyeron que alguien rascó y limpió esa caries con puntas de piedra afilada, cuando él todavía estaba vivo.",
        "Es el tratamiento dental más antiguo que se conoce. Un dentista de la Edad de Hielo, con un pedazo de pedernal.",
        "Mucho después, hace seis mil quinientos años, en lo que hoy es Eslovenia, alguien rellenó la grieta de un colmillo con cera de abeja.",
        "Si lo hicieron cuando la persona estaba viva, sería el relleno dental más antiguo del mundo, quizá para aliviar el dolor al masticar.",
        "Nadie sabía qué era una caries. Pero sabían que el dolor se podía calmar.",
    ]},
    {"id": "trepanacion", "frases": [
        "Tercera historia. La más impresionante, o la más aterradora.",
        "Hace miles de años, en muchas partes del mundo, a algunas personas les hacían un agujero en el cráneo. Los arqueólogos lo llaman trepanación.",
        "Y lo sorprendente es que muchos de esos cráneos muestran hueso nuevo creciendo alrededor del agujero. Es decir, la persona siguió viviendo.",
        "En la costa sur de Perú, hace unos dos mil cuatrocientos años, sobrevivían cuatro de cada diez pacientes.",
        "Pero con los siglos los cirujanos fueron perfeccionando la técnica. En la época inca, sobrevivían más de siete de cada diez.",
        "Para comparar, en la Guerra Civil de Estados Unidos, hace unos ciento sesenta años, moría más o menos la mitad de los soldados operados del cráneo.",
        "Sin microscopios y sin conocer los gérmenes, aquellos cirujanos de los Andes lograron mejores resultados.",
        "Los expertos creen que lo hacían sobre todo para tratar fracturas del cráneo tras golpes en combate, aunque quizá también por dolores o por rituales.",
    ]},
    {"id": "cuidado", "frases": [
        "Pero la medicina más poderosa de la prehistoria quizá no fue una planta ni un cuchillo.",
        "Fue algo mucho más simple. Que alguien cuidara de ti.",
        "En una cueva del norte de Irak se encontró el esqueleto de un neandertal con heridas terribles.",
        "Había recibido un golpe fuerte en la cara, tenía un brazo derecho dañado, una pierna lesionada y probablemente oía muy mal.",
        "Con esas heridas no podía cazar ni correr. Y aun así llegó a los cuarenta o cincuenta años, que entonces era mucho.",
        "Los investigadores creen que no habría sobrevivido solo. Su grupo lo alimentó y lo cuidó durante años.",
        "Y hay un caso todavía más antiguo. En Dmanisi, en Georgia, hay un cráneo de hace un millón setecientos setenta mil años.",
        "Pertenecía a alguien que había perdido casi todos los dientes años antes de morir. Solo le quedaba uno.",
        "Así no podía masticar carne dura ni raíces. Probablemente alguien le ayudó, ablandando la comida.",
        "O sea que cuidar a un enfermo no es un invento moderno. Es más viejo que nuestra propia especie.",
    ]},
    {"id": "amputacion", "frases": [
        "Y ahora, la cuarta historia. La que cambió la ciencia.",
        "Estamos en dos mil veinte, en una cueva de la selva de Borneo, en Indonesia, llamada Liang Tebo.",
        "Un equipo de arqueólogos excava una tumba de hace más de treinta y un mil años.",
        "Dentro hay el esqueleto de un adulto joven. Y le falta algo.",
        "Su pierna izquierda termina por debajo de la rodilla. Y los huesos acaban en un corte limpio, ya cicatrizado.",
        "Según los científicos, no fue un accidente ni la mordida de un animal. Fue un corte hecho a propósito, con una herramienta de piedra afilada.",
        "Esa persona fue operada cuando era un niño. Y la herida sanó sin infección.",
        "Y sobrevivió. Vivió entre seis y nueve años más, moviéndose por una selva llena de pendientes y ríos, con una sola pierna.",
        "Hasta ese día se pensaba que la cirugía había aparecido con la agricultura, hace unos siete mil años.",
        "Este hallazgo la adelantó veinticuatro mil años. Y lo hizo un grupo de cazadores recolectores, sin hospitales.",
        "Para sobrevivir a una operación así hay que conocer la anatomía, cortar con cuidado, parar la sangre y evitar la infección.",
        "Y después, alguien tuvo que cuidar al niño durante meses, y ayudarlo a caminar durante años.",
        "Cuando murió, lo enterraron en esa misma cueva.",
    ]},
    {"id": "botiquin", "frases": [
        "Entonces, ¿en qué se parece tu botiquín al de ellos?",
        "La aspirina nació de la corteza del sauce, un árbol que se usa para el dolor desde hace miles de años.",
        "La penicilina, el primer antibiótico, salió de un moho, en mil novecientos veintiocho.",
        "La miel se sigue usando hoy para tratar algunas heridas.",
        "Nuestros ancestros no tenían laboratorios. Tenían miles de años de pruebas, errores y gente que se contaba lo que funcionaba.",
        "Pero no los imites. Ellos también se envenenaban, se infectaban y se morían. Si algo te duele de verdad, ve con un médico.",
        "No sobrevivieron por ser más fuertes. Sobrevivieron aprendiendo, y cuidándose unos a otros.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "Así que la próxima vez que tomes una pastilla, detente un segundo.",
        "Detrás de ella hay un neandertal masticando corteza, un dentista de la Edad de Hielo con un pedazo de pedernal, y un niño en Borneo al que todo un grupo ayudó a caminar.",
        "Tú no eres el primero en sobrevivir a un dolor.",
        "Eres el último eslabón de una cadena de supervivientes que nunca se rindió.",
        "Eres un Homo sapiens. Con wifi.",
    ]},
]
