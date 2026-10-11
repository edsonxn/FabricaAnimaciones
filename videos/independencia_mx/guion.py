# -*- coding: utf-8 -*-
"""La Independencia de México, completa (~11 min, 16:9, estilo kurzgesagt, canal Bitácora Perdida).

Prueba de formato largo: un video de 10-12 min con cambio visual constante (objetivo: retención > 40 %).
Hilo narrativo: once años de guerra, cuatro etapas (Hidalgo, Morelos, resistencia, Iturbide-Guerrero) y por qué la
independencia se consumó con una alianza improbable.

Datos (fuentes: Historia General de México, Colmex; INAH; Archivo General de la Nación; Britannica):
  - Reformas borbónicas y Consolidación de Vales Reales (1804): la Corona exige a la Iglesia y a los dueños de hipotecas pagar los créditos;
    descontento de criollos. Expulsión de los jesuitas (1767).
  - 1808: Napoleón invade España; Carlos IV y Fernando VII abdican; José Bonaparte rey. El Ayuntamiento de México, con Francisco Primo de
    Verdad, propone que la soberanía regrese al pueblo; el virrey Iturrigaray es depuesto por el golpe de Gabriel de Yermo (15-sep-1808).
  - Conspiración de Valladolid (1809). Conspiración de Querétaro (1810): Miguel Domínguez (corregidor), Josefa Ortiz, Ignacio Allende,
    Juan Aldama; descubierta a principios de septiembre; Hidalgo convocado; 16-sep-1810 en Dolores: Hidalgo (57 años, no 67) llama a la insurrección.
    [Hidalgo nació el 8-may-1753: tenía 57.]
  - Estandarte de la Virgen de Guadalupe; en pocas semanas la multitud pasa de decenas a decenas de miles.
  - Alhóndiga de Granaditas, Guanajuato, 28-sep-1810 (matanza de españoles y criollos refugiados). Monte de las Cruces, 30-oct-1810:
    victoria insurgente; a la vista de la capital, Hidalgo ordena retirarse (2-nov). Aculco (7-nov), derrota. Decreto de abolición de
    la esclavitud de Hidalgo en Guadalajara (6-dic-1810). Puente de Calderón (17-ene-1811): derrota insurgente.
  - Captura en Acatita de Baján (21-mar-1811). Fusilamientos: Allende, Aldama y Jiménez (26-jun-1811), Hidalgo (30-jul-1811) en Chihuahua;
    las cabezas fueron exhibidas en la Alhóndiga hasta 1821.
  - Morelos: cura de Carácuaro, recibe el encargo de Hidalgo (oct-1810) de levantar el sur; Sitio de Cuautla (feb-mayo de 1812);
    Congreso de Anáhuac en Chilpancingo (sep-1813), «Sentimientos de la Nación» (14-sep-1813): independencia absoluta, abolición de la
    esclavitud y de las castas; Constitución de Apatzingán (oct-1814). Capturado en Temalaca (nov-1815), fusilado en San Cristóbal
    Ecatepec el 22-dic-1815.
  - Leona Vicario, Ignacio López Rayón (Junta de Zitácuaro, 1811), Mariano Matamoros y Hermenegildo Galeana (Morelos), Vicente Guerrero y
    Guadalupe Victoria (guerra de guerrillas). Expedición de Xavier Mina (1817), fusilado en noviembre de 1817.
  - 1820: Rafael del Riego restablece la Constitución de Cádiz (liberal). Conservadores novohispanos temen el liberalismo y buscan un
    México separado bajo un rey. Agustín de Iturbide, realista, recibe el mando contra Guerrero; Plan de Iguala (24-feb-1821): tres garantías
    (religión, independencia, unión); Iturbide y Guerrero se unen (Ejército Trigarante). Tratados de Córdoba (24-ago-1821) con Juan de
    O'Donojú, nuevo jefe político. El Ejército Trigarante entra a la Ciudad de México el 27-sep-1821; el 28 se firma el Acta de Independencia.
  - Después: Imperio de Iturbide (1822-1823); República federal (1824), primer presidente Guadalupe Victoria; Vicente Guerrero presidente
    en 1829 y decreta abolir la esclavitud (16-sep-1829); fusilado en 1831.
  - El 16 de septiembre se celebra desde 1825; el Grito en la noche del 15 (Porfirio Díaz, 1896, en Palacio Nacional).
"""

TITULO = "La Independencia de México, completa"
ARCHIVO = "independencia_mexico"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 112
GAP = 0.3
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.65, cfg_weight=0.3, temperature=0.78)
MEZCLA = dict(musica=-22.0, sfx=-24.0)
SUBTITULOS = False
ALIAS_QA = {"yermo": "yermo", "ermo": "yermo", "iturrigaray": "iturrigaray", "iturbide": "iturbide", "itúrbide": "iturbide",
            "zitacuaro": "zitacuaro", "apatzingan": "apatzingan", "trigarante": "trigarante"}
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Septiembre de mil ochocientos diez. Un cura de cincuenta y siete años toca la campana de una iglesia, en un pueblo pequeño.",
        "Nadie imagina que ese repique va a desatar once años de guerra.",
        "Esta es la historia completa de la Independencia de México.",
    ]},
    {"id": "nueva_espana", "frases": [
        "Hace más de dos siglos, México no se llamaba México. Se llamaba la Nueva España, y pertenecía al rey de España.",
        "Sus minas de plata llenaban de riqueza a la Corona, pero esa riqueza casi nunca se quedaba aquí.",
        "En lo más alto estaban los peninsulares, nacidos en España. Ellos ocupaban los mejores cargos.",
        "Debajo, los criollos: hijos de españoles nacidos en América, con dinero, pero sin poder.",
        "Y más abajo, los indígenas, los mestizos y los esclavos, que trabajaban la tierra y las minas.",
        "Los criollos empezaron a preguntarse por qué mandaban otros en su propia tierra.",
        "En mil ochocientos cuatro, el rey exigió a la Iglesia y a muchos propietarios que pagaran de golpe sus deudas, para financiar sus guerras en Europa.",
        "Miles de familias quedaron al borde de la ruina. El descontento ya estaba sembrado.",
    ]},
    {"id": "napoleon", "frases": [
        "Y entonces, al otro lado del océano, ocurrió algo que lo cambió todo.",
        "En mil ochocientos ocho, Napoleón invadió España, y obligó al rey a abdicar.",
        "Puso en el trono a su propio hermano. De pronto, el rey al que todos obedecían estaba prisionero.",
        "En la capital de la Nueva España, el ayuntamiento propuso algo inaudito: que, sin rey, el poder volviera al pueblo.",
        "El virrey Iturrigaray aceptó escuchar. Y un grupo de ricos españoles lo vio como una traición.",
        "Una noche de septiembre, lo arrestaron y lo mandaron de regreso a España.",
        "Fue un golpe de Estado. Y demostró que, en la Nueva España, el poder podía cambiar de manos por la fuerza.",
    ]},
    {"id": "conspiracion", "frases": [
        "Los criollos empezaron a reunirse en secreto, bajo la apariencia de tertulias literarias.",
        "La más importante fue en Querétaro, en la casa del corregidor Miguel Domínguez y su esposa, Josefa Ortiz.",
        "Ahí se juntaron oficiales del ejército, como Ignacio Allende y Juan Aldama, con el plan de levantarse en armas.",
        "Les faltaba un líder con el que el pueblo se identificara. Y lo encontraron en Dolores, en un cura llamado Miguel Hidalgo.",
        "Hidalgo era un hombre culto, que hablaba lenguas indígenas, y enseñaba a los campesinos oficios para salir de la pobreza.",
        "La fecha del levantamiento sería en octubre. Pero alguien los delató.",
        "Josefa Ortiz, encerrada en su casa, logró avisar a los conspiradores de que habían sido descubiertos.",
    ]},
    {"id": "grito", "frases": [
        "Allende llegó a Dolores, en la madrugada del dieciséis de septiembre de mil ochocientos diez, con la noticia.",
        "Según la tradición, Hidalgo respondió que ya no había remedio, y que había que actuar de inmediato.",
        "Mandó tocar la campana de la parroquia, y llamó a todos los que quisieran unirse.",
        "Ese es el famoso Grito de Dolores. No fue un discurso escrito, sino una llamada a las armas.",
        "Tomaron como bandera una imagen de la Virgen de Guadalupe, muy querida por el pueblo.",
        "Salieron con unos cientos de hombres, armados con machetes, palos y piedras.",
        "En pocos días, eran miles. En pocas semanas, decenas de miles.",
        "La mayoría eran indígenas y mestizos, que vieron en ese levantamiento una esperanza de recuperar sus tierras y de acabar con los tributos.",
    ]},
    {"id": "guanajuato", "frases": [
        "Su primera gran ciudad fue Guanajuato, el centro de las minas de plata.",
        "Los defensores españoles se encerraron en un enorme almacén de granos: la Alhóndiga de Granaditas.",
        "El ejército insurgente la rodeó, y el combate fue brutal. Cuenta la leyenda que un minero, el Pípila, cruzó la puerta con una losa a la espalda, y le prendió fuego.",
        "Los insurgentes entraron, y lo que siguió fue una matanza y un saqueo terribles.",
        "Esa violencia asustó a muchos criollos ricos, que hasta entonces simpatizaban con la causa, y se pasaron al bando del rey.",
        "Aun así, el ejército de Hidalgo creció y creció, y avanzó hacia la capital.",
    ]},
    {"id": "capital", "frases": [
        "En octubre, en el monte de las Cruces, a las puertas de la Ciudad de México, derrotaron al ejército del virrey.",
        "Tenían a la capital a la vista, casi indefensa. Eran unos ochenta mil hombres.",
        "Y entonces, Hidalgo hizo algo que hasta hoy divide a los historiadores: ordenó retirarse.",
        "Quizás temía una matanza. Quizás pensó que no tenían municiones. Nadie lo sabe.",
        "Esa decisión cambió la historia. El ejército realista se reorganizó, y empezó a perseguirlos.",
        "Los insurgentes fueron derrotados en Aculco. Allende e Hidalgo discutieron, y se separaron.",
    ]},
    {"id": "guadalajara", "frases": [
        "Hidalgo se estableció en Guadalajara, y ahí dio pasos muy importantes.",
        "Publicó un decreto para abolir la esclavitud, con pena de muerte para quien no lo cumpliera.",
        "Fundó un periódico insurgente, El Despertador Americano, y nombró ministros.",
        "Pero en enero de mil ochocientos once, en el puente de Calderón, unos seis mil soldados realistas bien armados derrotaron a una multitud enorme, pero mal equipada.",
        "Un proyectil hizo estallar su depósito de pólvora, y la batalla se perdió en minutos.",
    ]},
    {"id": "captura", "frases": [
        "Los jefes insurgentes huyeron hacia el norte, con la esperanza de llegar a Estados Unidos.",
        "Pero en marzo, un traidor los esperó en un camino del desierto, y fueron capturados.",
        "Los llevaron encadenados hasta Chihuahua. Allende, Aldama y Jiménez fueron fusilados en junio.",
        "A Hidalgo, por ser sacerdote, primero lo degradaron. Lo fusilaron el treinta de julio de mil ochocientos once.",
        "Sus cabezas fueron colgadas en las esquinas de la Alhóndiga de Granaditas, en Guanajuato.",
        "Ahí permanecieron diez años, como una advertencia. Pero la revolución no había muerto.",
    ]},
    {"id": "morelos", "frases": [
        "Antes de morir, Hidalgo había enviado a un viejo amigo, José María Morelos, a levantar el sur.",
        "Morelos era cura, hijo de un carpintero, y tenía un talento que nadie esperaba: era un genio militar.",
        "Con un ejército pequeño, organizado y disciplinado, ganó batalla tras batalla.",
        "En mil ochocientos doce resistió durante más de setenta días el sitio de la ciudad de Cuautla, rodeado por miles de soldados.",
        "Cuando ya no quedaba comida, sacó a todos sus hombres, en plena noche, y los salvó.",
        "Junto a él, peleaban hombres como Mariano Matamoros y Hermenegildo Galeana. Y desde la capital, la espía Leona Vicario les enviaba información y dinero.",
        "En poco tiempo, tomó Oaxaca y Acapulco, y llegó a controlar buena parte del sur del país.",
    ]},
    {"id": "congreso", "frases": [
        "En mil ochocientos trece, Morelos reunió en Chilpancingo al primer congreso de la historia de México.",
        "Declaró que el país sería independiente, sin importar lo que pasara en España.",
        "Y presentó un documento que aún se estudia: los Sentimientos de la Nación.",
        "Ahí dice que la soberanía viene del pueblo, que la esclavitud debe abolirse para siempre, y que desaparecen las castas.",
        "Todos los habitantes serían simplemente americanos, sin importar el color de su piel.",
        "Al año siguiente se publicó la Constitución de Apatzingán, la primera de México independiente.",
    ]},
    {"id": "fusilamiento", "frases": [
        "Pero el ejército realista cambió de estrategia. El virrey Calleja, el mismo que había vencido a Hidalgo, los persiguió sin descanso.",
        "Uno por uno, fue cayendo el círculo de Morelos. Matamoros fue capturado y fusilado. Galeana murió en combate.",
        "El Congreso tuvo que huir de pueblo en pueblo, cargando con sus papeles, hasta que Morelos se ofreció a protegerlo.",
        "En noviembre de mil ochocientos quince, cayó prisionero. Lo juzgaron, lo degradaron como sacerdote, y lo fusilaron en diciembre.",
        "Con él, parecía que la insurgencia se había terminado.",
    ]},
    {"id": "guerrillas", "frases": [
        "Pero no se terminó. Se escondió en las montañas.",
        "Vicente Guerrero, un arriero de origen humilde, mantuvo viva la guerra en las sierras del sur.",
        "Guadalupe Victoria resistió durante años en la selva de Veracruz, casi solo, comiendo lo que encontraba.",
        "En mil ochocientos diecisiete, desembarcó un joven español, Francisco Xavier Mina, con la idea de unirse a la lucha. Lo capturaron y lo fusilaron ese mismo año.",
        "En mil ochocientos veinte, la guerra llevaba diez años. El país estaba agotado, y los insurgentes, acorralados. Pocos pensaban que se pudiera ganar.",
        "Los realistas quemaban pueblos enteros, y los insurgentes cortaban los caminos. Las minas se inundaban, y los campos quedaban sin cultivar.",
    ]},
    {"id": "giro", "frases": [
        "Y entonces, de nuevo, un acontecimiento en España lo cambió todo.",
        "En mil ochocientos veinte, un golpe militar obligó al rey a aceptar una constitución liberal.",
        "Esa constitución recortaba poderes a la Iglesia y al ejército.",
        "En la Nueva España, los obispos, los ricos y los oficiales conservadores se asustaron.",
        "Y hicieron algo increíble: los defensores del rey comenzaron a pensar que sería mejor separarse de España.",
        "Querían una independencia a su manera, que protegiera sus privilegios.",
    ]},
    {"id": "iturbide", "frases": [
        "Para dirigirla eligieron a un militar realista, que había combatido a los insurgentes con dureza: Agustín de Iturbide.",
        "Lo enviaron al sur para acabar con Guerrero. Pero Iturbide tenía otro plan.",
        "En febrero de mil ochocientos veintiuno, lanzó el Plan de Iguala, con tres garantías: religión, independencia y unión.",
        "Un mensaje para todos: católicos, españoles y criollos, insurgentes y realistas.",
        "Escribió a Guerrero, y le ofreció unirse. Guerrero aceptó, y los dos enemigos se abrazaron.",
        "Nació el Ejército de las Tres Garantías, con sus colores: blanco, verde y rojo.",
    ]},
    {"id": "consumacion", "frases": [
        "La noticia corrió como pólvora. Ciudad tras ciudad, los realistas cambiaban de bando, casi sin disparar.",
        "El nuevo representante del rey, recién llegado de España, vio que ya no había nada que hacer. Y firmó un tratado con Iturbide en Córdoba.",
        "El veintisiete de septiembre de mil ochocientos veintiuno, el ejército entró a la Ciudad de México, con Iturbide al frente.",
        "Al día siguiente, se firmó el Acta de Independencia. México era libre.",
        "Once años de guerra y un país devastado, para llegar a ese momento.",
    ]},
    {"id": "despues", "frases": [
        "Pero la independencia no resolvió todos los problemas.",
        "Iturbide se coronó emperador, pero duró menos de un año. En mil ochocientos veinticuatro, nació la República, con Guadalupe Victoria como primer presidente.",
        "Vicente Guerrero llegó a la presidencia, y en mil ochocientos veintinueve abolió definitivamente la esclavitud.",
        "Dos años después, sus enemigos lo capturaron por traición y lo fusilaron.",
        "Los héroes de la independencia, casi todos, terminaron de la misma manera.",
        "México empezaba a ser un país: con un territorio enorme, sin dinero, y con ideas muy distintas de cómo debía gobernarse.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Hoy celebramos el dieciséis de septiembre. Pero la independencia se consumó el veintisiete.",
        "La celebró primero el pueblo, y después la institucionalizó un presidente, Porfirio Díaz, que hizo sonar la campana desde Palacio Nacional.",
        "La independencia no la hizo un solo hombre, ni un solo bando. La hicieron insurgentes, curas, arrieros, mujeres, soldados y hasta enemigos que se dieron la mano.",
        "¿Qué otra historia de México quieres ver en el canal? Cuéntamelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Música con Lyria (nucleo/lyria.py): épica mexicana de época, con huecos para la voz
LYRIA = dict(
    estilo=("Cinematic historical documentary score for an animated Mexican independence story: acoustic guitar, vihuela, harp, violin, trumpets, "
            "snare and field drums, light folk percussion, orchestral strings. Hopeful yet tense, constantly evolving, melodies kept low so a narrator "
            "can speak over it."),
    escenas={
        "gancho": ("Hook: a single church bell, suspense building, then a pulsing rhythm lifting into curiosity.", 5),
        "nueva_espana": ("Colonial calm with an undertone of unease: plucked vihuela and harp, slow strings, a pulse of discontent growing.", 6),
        "napoleon": ("Europe in turmoil: urgent strings, marching snare, a sudden hush, then a sharp dramatic hit for the coup.", 6),
        "conspiracion": ("Secret meetings: hushed plucked guitar, whispering strings, a nervous ticking pulse, rising tension.", 6),
        "grito": ("The cry of independence: a church bell, then an explosion of brass, drums and a rising hopeful theme.", 6),
        "guanajuato": ("Siege and fire: pounding drums, tension, crackling energy, then a dark unsettling passage.", 6),
        "capital": ("Victory and hesitation: triumphant trumpets, then a puzzled suspended pause and a sinking retreat motif.", 6),
        "guadalajara": ("A hopeful moment of reform followed by a sudden catastrophe: calm strings then a crashing, chaotic drop.", 5),
        "captura": ("Capture and sorrow: low drums, mournful cello and solo guitar, slow somber march.", 6),
        "morelos": ("A rising new leader: disciplined military drums, determined strings and brass, a stirring heroic march.", 6),
        "congreso": ("Dignity and vision: a solemn noble theme with strings and soft choir, hopeful and stately.", 6),
        "fusilamiento": ("Decline and sacrifice: minor key, slow funeral drums, a long somber final note.", 5),
        "guerrillas": ("Hidden resistance: sparse plucked guitar, distant drums, quiet stubborn determination, mountain winds.", 6),
        "giro": ("A twist of fate: a mysterious questioning motif, strings rising, curious and clever.", 5),
        "iturbide": ("Unlikely alliance: a proud martial theme turning warm, a handshake moment, hopeful trumpets.", 6),
        "consumacion": ("Triumph: bright brass, bells, joyful folk percussion, a grand celebration and a big final chord.", 6),
        "despues": ("Uneasy aftermath: a sober reflective piece, rising then falling, leaving unanswered questions.", 6),
        "cierre": ("Warm resolving outro: the main hopeful theme returns gently on guitar and strings, then a final soft chord.", 5),
    },
)
