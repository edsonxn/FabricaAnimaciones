# -*- coding: utf-8 -*-
"""Guía de estudio para Amaya: la Independencia de México — video PERSONAL (sin canal, no se sube), HORIZONTAL ~5-6 min.
ESTILO: ACUARELA PINTADA A MANO POR CÓDIGO (el de Kuriox últimamente, kit copiado de videos/chicle_dentro/) + LA CARA REAL del
usuario como en Edsonxn (foto recortada animada con su voz, nucleo/jefe_canadiense.py) + SU VOZ CLONADA (ElevenLabs cuenta 2).

Pedido del usuario (7-nov-2026): «un video para mi hija Amaya, guía de estudio para su examen de este lunes sobre la historia de la
independencia de México, unos 5 minutos con mi voz, métodos para que se le guarden las cosas, háblale como "Amaya", a veces chistes
para que recuerde mejor». Amaya tiene 12 años (6.º de primaria / 1.º de secundaria).
Forma de hablar del usuario (sus notas de voz): «a ver», «o sea», «fíjate», «pues», «mega», «literal», «chido», «¿sale?»; sin groserías.

Métodos de aprendizaje para 12 años (en el guion):
  - Historia contada como chisme/aventura (narrativa > lista) y preguntas «¿por qué?» antes del dato.
  - Pocos bloques (chunking): 3 causas, 1 inicio, 4 etapas con su líder, 3 garantías.
  - Mnemotecnias: «injusticia, ideas y Napoleón»; HMGI = «Hoy Me Gusta Ir» (Hidalgo, Morelos, Guerrero, Iturbide);
    RIU = «riu, riu» (Religión, Independencia, Unión) → colores de la bandera.
  - Humor y datos curiosos que anclan el recuerdo (el Zorro, el pañuelo, la silla de Napoleón, Iturbide se regala un país).
  - Práctica de recuerdo (retrieval): «pausa y contesta» con silencio real y cuenta regresiva, y repaso exprés al final.
  - Repetición espaciada dentro del video (cada dato clave sale 2-3 veces) + consejo de repasar antes de dormir.

Datos (verificados el 7-nov-2026; los de siempre de los libros de la SEP):
  - Causas: sociedad de castas (peninsulares, criollos, mestizos, indígenas, esclavos); criollos sin altos puestos; Ilustración,
    independencia de EE. UU. (1776), Revolución francesa (1789); Napoleón invade España en 1808 y Fernando VII pierde el trono.
  - Conspiración de Querétaro (1810): Allende, Aldama, Hidalgo, Josefa Ortiz de Domínguez y su esposo el corregidor Miguel Domínguez;
    descubierta; Josefa, encerrada, manda avisar (Ignacio Pérez). Grito de Dolores, madrugada del 16-sep-1810, Dolores (Guanajuato),
    campana y estandarte de la Virgen de Guadalupe. A Hidalgo le decían «el Zorro» en el Colegio de San Nicolás.
  - Inicio 1810-1811 (Hidalgo): Alhóndiga de Granaditas (28-sep-1810, el Pípila, tradición); Monte de las Cruces (30-oct-1810), no
    entra a la Ciudad de México; derrota en Puente de Calderón (17-ene-1811); capturado en Acatita de Baján; fusilado en Chihuahua
    (30-jul-1811). Decreto de abolición de la esclavitud (Guadalajara, 6-dic-1810).
  - Organización 1811-1815 (Morelos, exalumno de Hidalgo en San Nicolás): sitio de Cuautla (feb-may 1812, 72 días); Sentimientos de
    la Nación (14-sep-1813, Congreso de Chilpancingo); Constitución de Apatzingán (22-oct-1814); «Siervo de la Nación»; fusilado
    22-dic-1815. Pañuelo: se dice que por migrañas. Leona Vicario: financió y pasó información a los insurgentes.
  - Resistencia 1815-1820: Vicente Guerrero (sur) y Guadalupe Victoria (Veracruz), guerrillas. Victoria se llamaba José Miguel Ramón
    Adaucto Fernández y Félix; primer presidente de México (1824).
  - Consumación 1821: Agustín de Iturbide (realista) se une a Guerrero; Abrazo de Acatempan (10-feb-1821, tradición); Plan de Iguala
    (24-feb-1821), tres garantías: Religión, Independencia, Unión → Ejército Trigarante, bandera blanco-verde-rojo; Tratados de Córdoba
    (24-ago-1821, con Juan O'Donojú); entrada a la Ciudad de México el 27-sep-1821, día del cumpleaños 38 de Iturbide (nació el
    27-sep-1783 en Valladolid, hoy Morelia).
  - Retratos reales: Wikimedia Commons, dominio público (los mismos de videos/independencia_mx/retratos/_config.py).
"""

TITULO = "Amaya: la Independencia de México en 5 minutos (guía para tu examen)"
ARCHIVO = "amaya_independencia"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit acuarela.py; docs/estilo_acuarela_pincel.md)
DURACION = None
BPM = 200
GAP = 0.32
FPS = 24                          # la tinta «hierve» a 12 fps (en dos)
# Voz clonada del usuario (cuenta 2 de ElevenLabs). Corchetes suaves: nunca susurros ni excitado.
VOZ = dict(motor="elevenlabs", voice_id="GUEeiSJYQQdbv0NJ86Im", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-24.0, sfx=-24.0, fx=-10.0)
SUBTITULOS = False
ALIAS_QA = {}
# Whisper escribe las fechas con cifras («1810»), «R y U» y «río» por «riu»: el audio está bien (duraciones coherentes)
CER_MAX_POR_FRASE = {"truco_1": 0.09, "inicio_0": 0.08, "inicio_1": 0.03, "organizacion_0": 0.06, "resistencia_0": 0.08,
                     "consumacion_3": 0.13, "resp3_0": 0.10}
MUSICA = {}
# Música: piezas YA PAGADAS de la biblioteca (biblioteca usar), una por tramo; tierna/juguetona, escolar.
LYRIA = dict(
    estilo="Warm playful storybook score for a kid's study guide: marimba, soft guitar, music box, pizzicato; low in the mix.",
    escenas={
        "gancho": ("Playful, curious hello.", 4), "causas": ("Curious storytelling.", 4), "grito": ("Rising, bells, hopeful.", 5),
        "preg1": ("Light thinking pulse.", 3), "resp1": ("Small celebration.", 4), "truco": ("Bouncy mnemonic.", 5),
        "inicio": ("Adventure, marching.", 5), "organizacion": ("Determined, organised.", 5), "resistencia": ("Hide and seek.", 4),
        "consumacion": ("Festive Mexican, celebration.", 6), "repaso": ("Quick recap.", 4), "preg2": ("Thinking.", 3),
        "resp2": ("Celebration.", 4), "preg3": ("Thinking.", 3), "resp3": ("Celebration.", 4), "cierre": ("Tender, loving.", 3),
    },
    tramos=[(["gancho", "causas", "grito"], ""), (["preg1", "resp1", "truco", "inicio", "organizacion"], ""),
            (["resistencia", "consumacion"], ""), (["repaso", "preg2", "resp2", "preg3", "resp3", "cierre"], "")],
)
TRANSICIONES = [("continua", 0.3)] * 15   # plano secuencia: los cambios los dibuja escenas.py

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "¡Hola, Amaya! [short pause] A ver, el lunes es tu examen de la Independencia de México, ¿verdad? Pues en cinco minutos te la voy a dejar bien pegada en la cabeza.",
        "O sea, nada de memorizar como robot: te la cuento como chisme, con trucos y chistes malos de papá. [laughs]",
        "Trato: cuando te diga «pausa y contesta», pausas el video y lo dices en voz alta. ¿Sale? Arrancamos.",
    ]},
    {"id": "causas", "frases": [
        "Primero, ¿por qué? Fíjate: hace más de doscientos años, México ni se llamaba México. Era la Nueva España, y la mandaba el rey de España.",
        "La gente estaba acomodada como en una pirámide: arriba, los peninsulares, nacidos en España. Luego los criollos, hijos de españoles pero nacidos aquí.",
        "Y hasta abajo, mestizos, indígenas y esclavos, que trabajaban más y ganaban menos.",
        "Los criollos tenían estudios y dinero, pero no les daban los puestos importantes. O sea, mega injusto.",
        "Además llegaban ideas de libertad: Estados Unidos ya era independiente, y en Francia hubo una revolución.",
        "Y en mil ochocientos ocho, Napoleón invadió España y dejó al rey sin trono. Literal, como en el juego de las sillas, pero con un ejército. [laughs]",
        "Truco para las causas: injusticia, ideas y Napoleón.",
    ]},
    {"id": "grito", "frases": [
        "Entonces, en Querétaro, se juntaban a escondidas a planear la rebelión: Ignacio Allende, Juan Aldama, el cura Miguel Hidalgo, y Josefa Ortiz de Domínguez, la Corregidora.",
        "Pero los descubrieron. A Josefa la encerraron en su casa, y aun así mandó avisar a los demás. Ella salvó el plan.",
        "Y en la madrugada del dieciséis de septiembre de mil ochocientos diez, en Dolores, Guanajuato, Hidalgo tocó la campana y llamó a la gente a levantarse: el Grito de Dolores.",
        "Su bandera: un estandarte de la Virgen de Guadalupe. Dato chido: en la escuela a Hidalgo le decían «el Zorro», por listo.",
    ]},
    {"id": "preg1", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: ¿qué día empezó la Independencia?",
    ]},
    {"id": "resp1", "pre": 0.2, "frases": [
        "¡Dieciséis de septiembre de mil ochocientos diez! Eso.",
    ]},
    {"id": "truco", "frases": [
        "Ahora, el truco más importante. La guerra duró once años, en cuatro etapas: Inicio, Organización, Resistencia y Consumación.",
        "Y cada una tiene su líder: Hidalgo, Morelos, Guerrero e Iturbide. Hache, eme, ge, i. Para que se te pegue: «Hoy Me Gusta Ir».",
        "Repítelo conmigo: [short pause] Hoy... Me... Gusta... Ir.",
    ]},
    {"id": "inicio", "frases": [
        "Uno: el Inicio, con Hidalgo, de mil ochocientos diez a mil ochocientos once. Su ejército: gente del pueblo con palos, machetes y hondas.",
        "En Guanajuato tomaron la Alhóndiga de Granaditas. Cuenta la historia que un minero, el Pípila, se echó una losa en la espalda y le prendió fuego a la puerta.",
        "Ganaron en el Monte de las Cruces, pero no entraron a la Ciudad de México, y luego perdieron en Puente de Calderón.",
        "En mil ochocientos once lo capturaron y lo fusilaron. Pero antes alcanzó a decretar algo enorme: acabar con la esclavitud.",
    ]},
    {"id": "organizacion", "frases": [
        "Dos: la Organización, con José María Morelos, de mil ochocientos once a mil ochocientos quince. Fue alumno de Hidalgo, y sí, es el del pañuelo en la cabeza: dicen que le dolía mucho.",
        "Él sí era bien organizado: ejército entrenado, y aguantó más de dos meses el sitio de Cuautla.",
        "En mil ochocientos trece escribió los Sentimientos de la Nación: que fuéramos libres, sin esclavitud y sin castas. Y en mil ochocientos catorce salió la Constitución de Apatzingán.",
        "Pidió que le dijeran «Siervo de la Nación». En mil ochocientos quince también lo fusilaron.",
        "Y no olvides a Leona Vicario: con su dinero ayudaba a los insurgentes y les pasaba información en secreto. Una espía de verdad.",
    ]},
    {"id": "resistencia", "frases": [
        "Tres: la Resistencia, de mil ochocientos quince a mil ochocientos veinte. Quedaban pocos, escondidos en las montañas.",
        "Vicente Guerrero y Guadalupe Victoria peleaban en guerrillas: atacaban y se escondían. Aguantaron, como tú el último día antes de vacaciones. [laughs]",
        "Dato chido: Guadalupe Victoria después fue el primer presidente de México.",
    ]},
    {"id": "consumacion", "frases": [
        "Y cuatro: la Consumación, en mil ochocientos veintiuno, con Agustín de Iturbide. Lo curioso: Iturbide era realista. O sea, peleaba contra los insurgentes.",
        "Pero cambió de bando, se juntó con Guerrero, y cuenta la tradición que se dieron un abrazo: el Abrazo de Acatempan.",
        "Juntos hicieron el Plan de Iguala, con tres garantías: Religión, Independencia y Unión. Por eso, Ejército Trigarante. Y de ahí salieron los colores de la bandera: blanco, verde y rojo.",
        "Truco: las tres garantías son erre, i, u. Como cuando te ríes bajito: riu, riu, riu. [laughs]",
        "Se firmaron los Tratados de Córdoba, y el veintisiete de septiembre de mil ochocientos veintiuno, el Ejército Trigarante entró a la Ciudad de México.",
        "¡Y justo era el cumpleaños de Iturbide! O sea, se regaló un país. [laughs]",
    ]},
    {"id": "repaso", "frases": [
        "Repaso exprés. Empezó el dieciséis de septiembre de mil ochocientos diez y terminó el veintisiete de septiembre de mil ochocientos veintiuno. Los dos en septiembre: el mes patrio.",
    ]},
    {"id": "preg2", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: ¿cuáles son las cuatro etapas, y quién era el líder de cada una?",
    ]},
    {"id": "resp2", "pre": 0.2, "frases": [
        "Inicio, Organización, Resistencia y Consumación. Y sus líderes: Hoy Me Gusta Ir. Hidalgo, Morelos, Guerrero, Iturbide.",
    ]},
    {"id": "preg3", "pre": 0.3, "post": 3.2, "frases": [
        "Otra: ¿quién avisó que habían descubierto la conspiración? ¿Y cuáles son las tres garantías?",
    ]},
    {"id": "resp3", "pre": 0.2, "frases": [
        "Josefa Ortiz de Domínguez. Y las garantías... riu, riu: Religión, Independencia y Unión. ¡Bien!",
    ]},
    {"id": "cierre", "post": 2.0, "frases": [
        "Amaya, con esto el lunes vas a estar lista. Antes de dormir, vuelve a ver el repaso: lo que repasas antes de dormir se te queda mejor.",
        "Échale ganas. Yo sé que tú puedes. [short pause] Te quiero mucho, hija. ¡Mucho éxito en tu examen!",
    ]},
]
