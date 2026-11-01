# -*- coding: utf-8 -*-
"""El llamado del Mixtón — película animada tipo novela (~15 min, 16:9), estilo pegatina Flow CINEMATOGRÁFICO. Proyecto sin canal.

Pedido del usuario (21-oct-2026, tras mandar la foto de un mural municipal de la Guerra del Mixtón): «animación tipo pegatinas de
Flow como una película cinematográfica, como novela, vista desde un hombre padre de familia caxcán que es llamado a la guerra: su
trayectoria completa, de antes de la llegada hasta la guerra del Mixtón; que se sienta como novela, con diferentes voces». 15 min en
1 sesión, final con invitación a compartir y dar like, voces ElevenLabs, vista previa del primer acto con audio completo.

Ficción histórica: Tecuani, Citlali, Ollin y el abuelo son personajes inventados (nombres de raíz náhuatl, lengua hermana del caxcán);
el marco histórico es real (fuentes y fechas en _hechos.md, verificadas el 21-oct-2026). Estructura: prólogo en la cima del Mixtón la
noche antes del asalto final (dic-1541) → flashback de 5 actos → regreso a la noche → caída → epílogo de Ollin ya viejo → cierre.
ElevenLabs eleven_v4: corchetes de actuación en inglés, escritura normal. Diálogos con otra voz vía VOZ_POR_FRASE («escena_índice»).
"""

TITULO = "El llamado del Mixtón"
ARCHIVO = "caxcan_mixton"
ESTILO_VISUAL = "pegatina_flow"   # Flow pinta, el código mueve (docs/estilo_pegatina_flow.md)
DURACION = None
BPM = 70
GAP = 0.35

# Voces (biblioteca pública de ElevenLabs, acento mexicano / peninsular; 21-oct-2026)
TECUANI = "G0i2vdf60PiSodEVC261"    # MYS Octavio - Deep, Warm (mexicano, mediana edad): el padre, narrador
CITLALI = "akOBlaKhFd59YlK6xz9u"    # Lucia - Warm Conversational (mexicana, expresiva): la madre
OLLIN = "p7cwnUviDFhhX9y8sG2Q"      # Sebastian - Adolescente alegre (latinoamericano): el hijo a los 15
OLLIN_VIEJO = "68nvxRVrtyK9nd4hTKmR"  # Pablo Macias (mexicano, viejo, narrativo): Ollin anciano, epílogo y cierre
ABUELO = "Rt1JHkPO27QCUX6Nd5bV"     # Jorge (mexicano, viejo, rasposo): el abuelo
PROFETA = "4tQu251g6T1tzWGd7LSI"    # Sky - Mysterious Narration (mexicano, joven): el mensajero del tlatol
TENAMAXTLI = "t6ftGMMsNKPJUzbnYoOU"  # Marvin - Mexican accent (grave): Tenamaxtli
HERALDO = "Otf4KTIb4E5xLTCtWfye"    # Jose Conde - Firm, Confident (peninsular): el que lee el requerimiento
ENCOMENDERO = "qCpeKeRp8nkdJgckZbTo"  # Fernando - Bold, Mature (peninsular): el encomendero
FRAILE = "J5hu7rFtEb1rgdJDH30E"     # JR - Calm & friendly (peninsular): el fraile
ALVARADO = "gMKDphBYBTH1d8NfIACN"   # Álvaro - Audiobooks (peninsular, grave): Pedro de Alvarado
CORREDOR = "4rOzDieCbHQQyo9tzqZv"  # Diego - Warm & Conversational (mexicano, joven): el corredor de Tenamaxtli
# 2.º pedido del usuario (21-oct): escenas del BANDO ESPAÑOL, fechas y un NARRADOR; que provoque ira, llanto, entusiasmo,
# empoderamiento y orgullo con lágrimas. Mayormente novela con personajes.
NARRADOR = "qK97aPuDo74niFLxjFrK"   # Miguel Paz - Sophisticated & Authoritative (mexicano): fechas y contexto
CHIRINOS = "z3kTTwYbQrmL7ckdGcJi"   # Martin Osborne - Polished, castellano, suspense: Pedro Almíndez Chirinos
MENDOZA = "y3QZXBVdGkWBnlHwEtgG"    # Nestor - Deep Calm (peninsular, ~50): el virrey Antonio de Mendoza
ONATE = "zuKOnzM8OJyC1IQIhCHR"      # Kurry Caché - Smooth, Warm (peninsular): Cristóbal de Oñate
IBARRA = "Eevi69Z4Qm4eiqxJaOQt"     # Julio - Narrator, deep firm (peninsular): Miguel de Ibarra
BEATRIZ = "BkOojM1ZhtSAHgsAkMx2"    # Carolina - Warm & Expressive (peninsular): Beatriz Hernández
LASCASAS = "orF2qy9215xjwqqxqsWW"   # Rafael - Expressive and Theatrical (peninsular, viejo): fray Bartolomé de las Casas
MONTOYA = "8RjxcQ6tY1F2YZiIvWqY"    # Jasper - Gentle and Cautious (peninsular): Baltasar de Montoya, escribano de Alvarado
SOLDADO = "YKrm0N1EAM9Bw27j8kuD"    # Leónidas - rough (peninsular): soldados

VOZ = dict(motor="elevenlabs", voice_id=TECUANI, modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)
VOZ_POR_FRASE = {
    "noche_3": OLLIN,
    "rio_5": CITLALI, "fiesta_3": CITLALI,
    "teul_1": ABUELO, "teul_2": ABUELO,
    "noticias_4": ABUELO,
    "llegada_5": HERALDO,
    "hierro_4": ABUELO,
    "encomienda_2": ENCOMENDERO, "encomienda_4": FRAILE,
    "tlatol_1": PROFETA, "tlatol_2": PROFETA, "tlatol_3": PROFETA,
    "llamado_1": CORREDOR,
    "decision_0": CITLALI, "decision_2": OLLIN,
    "herida_1": OLLIN,
    "cerco_2": CITLALI,
    "ultima_2": OLLIN, "ultima_5": CITLALI,
    "cierre_0": OLLIN_VIEJO, "cierre_1": OLLIN_VIEJO,
    # ── 2.º pedido: narrador, bando español, Tenamaxtli ──
    "apertura_0": NARRADOR, "antes_0": NARRADOR,
    "chirinos_0": NARRADOR, "chirinos_1": NARRADOR, "chirinos_2": SOLDADO, "chirinos_3": CHIRINOS,
    "cedula_0": NARRADOR, "cedula_1": NARRADOR,
    "penol_3": TENAMAXTLI, "penol_4": TENAMAXTLI,
    "victoria_0": NARRADOR, "victoria_1": IBARRA, "victoria_4": OLLIN,
    "consejo_0": NARRADOR, "consejo_1": MENDOZA, "consejo_2": MENDOZA,
    "alvarado_0": NARRADOR, "alvarado_1": ONATE, "alvarado_2": ALVARADO, "alvarado_6": MONTOYA, "alvarado_7": ALVARADO,
    "alvarado_8": NARRADOR,
    "guadalajara_0": NARRADOR, "guadalajara_3": BEATRIZ,
    "virrey_0": NARRADOR, "virrey_1": NARRADOR, "virrey_4": SOLDADO, "virrey_5": MENDOZA,
    "epilogo_0": NARRADOR, "epilogo_1": OLLIN_VIEJO, "epilogo_2": OLLIN_VIEJO, "epilogo_3": OLLIN_VIEJO,
    "valladolid_0": NARRADOR, "valladolid_1": LASCASAS, "valladolid_2": TENAMAXTLI, "valladolid_3": TENAMAXTLI,
    "valladolid_4": TENAMAXTLI, "valladolid_5": NARRADOR,
    "final_0": OLLIN_VIEJO, "final_1": OLLIN_VIEJO, "final_2": NARRADOR, "final_3": OLLIN_VIEJO, "final_4": OLLIN_VIEJO,
}
MEZCLA = dict(musica=-20.0, sfx=-22.0, fx=-8.0)
SUBTITULOS = False
ALIAS_QA = {"cascanes": "caxcanes", "cajcanes": "caxcanes", "cazcanes": "caxcanes", "kaxkanes": "caxcanes", "caxcan": "caxcán",
            "cascan": "caxcán", "mixton": "mixtón", "mizton": "mixtón", "halpa": "jalpa", "penol": "peñol", "penoles": "peñoles",
            "tenamaxti": "tenamaxtli", "tenamajli": "tenamaxtli", "tenamazti": "tenamaxtli", "tenamaztli": "tenamaxtli",
            "tenamasti": "tenamaxtli", "tenamaxtle": "tenamaxtli", "tecuane": "tecuani", "olin": "ollin", "oyin": "ollin",
            "citlalli": "citlali", "tonatiu": "tonatiuh", "tlatoles": "tlatol", "nochistlan": "nochistlán"}
MUSICA = {}
# Tomas oídas como buenas: Whisper escribe mal los nombres (Ollin → Olin/Ogin/Ojin, caxcán → Kashkán, Citlali → Itlali,
# Apozol → Aposol, «se van» → «Sivan») o la pausa [short pause] es larga a propósito (21-oct-2026)
CER_MAX_POR_FRASE = {k: 0.18 for k in ("noche_5", "teul_1", "chirinos_3", "hierro_4", "llamado_0", "decision_1", "penol_0",
                                       "victoria_4", "guadalajara_4", "virrey_3", "cerco_2", "valladolid_0",
                                       "diez_2")}   # diez_2: «Tensa» susurrado → Whisper oye «Pensa» en las 2 tomas
GAP_MAX_POR_FRASE = {k: 1.3 for k in ("noche_5", "chirinos_3", "decision_1", "virrey_3", "valladolid_0")}
# ElevenLabs no deja silencio al final: la última palabra cae en el 8 % de cola (se apaga limpia a −53…−89 dB, sin murmullo)
TAIL_MAX_POR_FRASE = {k: 0.95 for k in ("teul_1", "penol_0", "virrey_3", "valladolid_0")}

ESCENAS = [
    # ── PRÓLOGO: la cima del Mixtón, la noche antes del asalto (diciembre de 1541) ──
    {"id": "apertura", "pre": 2.5, "frases": [
        "Diciembre de 1541. Cerro del Mixtón, en el cañón de Juchipila, en lo que hoy es Zacatecas.",
    ]},
    {"id": "noche", "pre": 2.0, "post": 4.0, "frases": [
        "[whispers] Mira allá abajo, Ollin. [short pause] Esas luces no son estrellas.",
        "Son las fogatas del virrey. Miles, desde el río hasta donde se acaba la vista.",
        "[serious] Mañana suben.",
        "[nervous] ¿Tienes miedo, padre?",
        "[sighs] Sí. [short pause] Por eso te voy a contar todo, desde el principio. Para que, pase lo que pase mañana, tú lo sepas.",
        "Me llamo Tecuani. Soy caxcán, del cañón de Juchipila. [short pause] Y esta es la historia de cómo llegamos a la cima del Mixtón.",
    ]},
    # ── ACTO I: antes ──
    {"id": "antes", "pre": 1.0, "frases": [
        "Dieciséis años antes. [short pause] Cañón de Juchipila, hacia 1525.",
    ]},
    {"id": "rio", "pre": 1.0, "frases": [
        "[softly] Antes de todo esto, el mundo entero cabía en un cañón.",
        "Abajo corría el río, y en sus orillas sembrábamos maíz, frijol y calabaza.",
        "En tiempo de secas juntábamos las vainas del mezquite, y del maguey sacábamos fibra para tejer y aguamiel para beber.",
        "Tu madre, Citlali, molía el maíz en el metate antes de que saliera el sol. [short pause] Ese ruido de piedra contra piedra era lo primero que oía cada mañana.",
        "Un día de lluvias naciste tú. Te pusimos Ollin, que quiere decir movimiento… [laughs] porque no dejabas de patear.",
        "[laughs] Míralo, Tecuani. Tiene tus manos.",
        "Cuando aprendiste a caminar, me seguías al río. Un día sacaste del agua una piedra lisa y verde, y me la diste.",
        "Para ti, me dijiste. [short pause] Todavía la traigo colgada del cuello.",
    ]},
    {"id": "fiesta", "frases": [
        "Cuando se levantaba la cosecha, todo el pueblo se juntaba en la plaza.",
        "Sonaban los tambores de tronco y las flautas de barro, y bailábamos hasta que el fuego se hacía brasa.",
        "Tu madre bailaba mejor que nadie. [laughs] Yo la pisaba, y ella se reía.",
        "[laughs] ¡Ay, Tecuani! Me vas a dejar sin pies.",
        "[softly] Así era la vida antes. No era fácil. [short pause] Pero era nuestra.",
    ]},
    {"id": "teul", "frases": [
        "Cuando cumpliste cuatro años, tu abuelo nos llevó al Teul, el cerro sagrado, donde los nuestros subían a hablar con los dioses.",
        "[softly] Mira, Ollin. Desde aquí se ve todo: el agua, las milpas, los cerros, los pueblos de tu gente.",
        "Esta tierra no es nuestra, niño. [short pause] Nosotros somos de ella.",
        "[sad] Esa fue la última vez que subimos juntos los tres.",
    ]},
    {"id": "noticias", "post": 1.5, "frases": [
        "Por esos años empezaron a llegar noticias del sur, con los que comerciaban sal, conchas y plumas.",
        "Decían que la gran ciudad del lago, Tenochtitlan, había caído. [short pause] Que unos hombres barbados se vestían de metal…",
        "…y que montaban venados sin cuernos, más altos que un hombre.",
        "Que sus armas tronaban como el cielo en tiempo de aguas, y que mataban desde lejos.",
        "[laughs] ¡Cuentos de mercaderes! Si existieran esos venados, ya los habríamos cazado.",
        "[sighs] Tu abuelo se equivocaba. No eran cuentos.",
    ]},
    # ── ACTO II: la llegada (1530) ──
    {"id": "llegada", "pre": 2.0, "frases": [
        "Llegaron en tiempo de secas, en el año que ellos llamaban 1530.",
        "Primero fue el ruido: miles de pasos, cascos de caballo, perros que ladraban distinto a los nuestros.",
        "Venían de parte de Nuño de Guzmán, un conquistador al que hasta los suyos le tenían miedo. Los mandaba su capitán, Chirinos.",
        "Con ellos venían cientos de indios del sur, cargando sus cosas y peleando por ellos.",
        "Los nuestros habían levantado un muro de piedra en el camino. [short pause] Lo derribaron en una mañana.",
        "[shouts] ¡En nombre de Su Majestad, os requerimos que reconozcáis por señores al rey y a la santa Iglesia!",
        "Nadie entendió una sola palabra. [short pause] Y casi todo el cañón huyó a la sierra.",
    ]},
    # ── bando español: el campamento de Chirinos (primavera de 1530) ──
    {"id": "chirinos", "frases": [
        "Primavera de 1530. Pedro Almíndez Chirinos, capitán de Nuño de Guzmán, cruza el cañón con unos cincuenta españoles y quinientos aliados.",
        "Busca oro, esclavos y un camino hacia el norte.",
        "[nervous] Capitán, los pueblos están vacíos. Se han ido todos a la sierra.",
        "[cold] Pues id a por ellos. Al que bajéis, herradlo. [short pause] Que se sepa de quién es.",
    ]},
    {"id": "hierro", "frases": [
        "A los pueblos que se escondieron en los cerros les quemaron las casas y las milpas.",
        "A los que atrapaban los marcaban con un hierro caliente, como a su ganado, y se los llevaban como esclavos.",
        "Tu madre te apretaba contra su pecho para que no vieras. [short pause] Pero tú lo viste todo.",
        "A tu abuelo se lo llevaron de cargador. Le pusieron un fardo en la espalda y una cuerda al cuello.",
        "[whispers] Cuida a tu madre, Ollin. [short pause] Y acuérdate del cerro.",
        "[sad] Lo vimos irse por el camino del río. Nunca volvió.",
        "Tú me preguntaste cuándo iba a regresar. [short pause] No supe qué contestarte.",
    ]},
    {"id": "encomienda", "frases": [
        "Después vino la encomienda: una palabra suya que quería decir que ahora éramos de alguien.",
        "Nuestro pueblo se lo dieron a un español. Le pagábamos con maíz, con mantas de algodón y con trabajo.",
        "[angry] ¡Más deprisa! ¡Ese granero ha de estar lleno antes de las lluvias, o lo pagaréis!",
        "Tú, con siete años, cargabas agua para su casa. [short pause] Yo cargaba piedra para su iglesia.",
        "[softly] Yo te bautizo en el nombre del Padre… [short pause] Desde hoy te llamarás Juan.",
        "Me echaron agua en la cabeza y me pusieron otro nombre. [short pause] Pero yo seguí siendo Tecuani.",
        "Y en 1532, junto a Nochistlán, fundaron una ciudad suya: Guadalajara. [short pause] Los nuestros se negaron a levantarla.",
    ]},
    {"id": "cedula", "frases": [
        "En 1536, una orden del rey reprochaba que en estas tierras se siguiera herrando y vendiendo a mujeres y a niños menores de catorce años.",
        "[serious] La orden llegó. [short pause] El hierro siguió.",
    ]},
    # ── ACTO III: el llamado (1540) ──
    {"id": "diez", "pre": 1.5, "frases": [
        "Así pasaron diez años. [short pause] Diez años de agachar la cabeza.",
        "Tú creciste. Te enseñé a tirar con arco a escondidas, en la barranca, como me enseñó mi padre.",
        "[softly] Tensa sin miedo, Ollin. [short pause] La flecha sabe adónde va, si tú lo sabes.",
        "Hasta que en 1540 sus soldados se marcharon al norte, a buscar unas ciudades de oro que nadie había visto nunca.",
        "Se llevaron sus mejores caballos y sus mejores armas. [short pause] Y el cañón se quedó casi sin españoles.",
    ]},
    {"id": "tlatol", "frases": [
        "Entonces bajaron de la sierra unos mensajeros con un tlatol: una palabra de Tecoroli que corría de pueblo en pueblo.",
        "[mysterious] ¡Ya llega el tiempo! Los antiguos regresan, y los viejos volverán a ser jóvenes.",
        "[whispers] Las milpas crecerán solas… [short pause] y el que siga sirviendo a los cristianos, morirá.",
        "[shouts] ¡Suban a los peñoles! ¡Allá arriba nadie nos puede vencer!",
        "Esa noche bailamos alrededor del fuego hasta el amanecer. [short pause] Hacía diez años que no bailábamos.",
        "Al poco tiempo, en el cañón empezaron a echar a pedradas a los encomenderos. [short pause] Ya no había vuelta atrás.",
    ]},
    {"id": "llamado", "frases": [
        "Unos días después llegó a nuestra puerta un corredor de Nochistlán, cubierto de polvo.",
        "[out of breath] Tenamaxtli llama a todos los hombres del cañón. [short pause] Al Mixtón, con sus familias. Ya.",
        "Ese fue el llamado. [short pause] Y supe que la vida de antes se había terminado.",
    ]},
    {"id": "decision", "frases": [
        "[nervous] ¿Y si no es cierto, Tecuani? ¿Y si vuelven a subir a buscarnos, como la otra vez?",
        "[serious] Si no vamos, Citlali, Ollin va a cargar fardos toda su vida. [short pause] Como mi padre.",
        "[excited] ¡Yo voy contigo, padre! Ya sé tirar con arco.",
        "Tenías quince años. Tu madre lloró toda la noche. [short pause] Y al amanecer, preparó comida para los tres.",
    ]},
    # ── ACTO IV: la guerra (1541) ──
    {"id": "penol", "pre": 1.5, "frases": [
        "Al Mixtón subían familias de todo el cañón: de Juchipila, de Jalpa, de Apozol, de Tlaltenango.",
        "Le decimos Mixtón, el subidero de los gatos monteses: un cerro de paredes de piedra que caen derechas a la barranca.",
        "Allá arriba conocí al hombre que nos guiaba: Tenamaxtli, un principal de Nochistlán.",
        "[serious] Nos llamaron perros. Nos marcaron con hierro, como a su ganado. [short pause] Nos cambiaron hasta el nombre.",
        "[shouting] ¡Pero esta tierra todavía sabe cómo nos llamamos! ¡Aquí arriba los caballos no sirven! ¡Aquí, la montaña pelea con nosotros!",
        "Miles de voces le contestaron. [short pause] Yo grité mi nombre, Tecuani, hasta que me dolió el pecho.",
        "Levantamos muros de piedra en las orillas y juntamos montones de rocas. Las mujeres subían agua y maíz; los niños, piedras.",
    ]},
    {"id": "victoria", "frases": [
        "Abril de 1541. El capitán Miguel de Ibarra llega al pie del Mixtón a ofrecer la paz.",
        "[shouts] ¡Bajad en paz y se os perdonará! ¡Si no, no habrá piedad para nadie!",
        "Le contestamos el domingo que ellos llaman de Ramos: [short pause] le cayó encima el cerro entero, piedras, flechas, gritos.",
        "Huyeron cuesta abajo, con todo y caballos. Por primera vez en diez años, los vimos correr.",
        "[excited] ¡Padre, se van! ¡Se van!",
        "Esa noche cantamos hasta quedarnos sin voz. [short pause] Creímos que la guerra ya era nuestra.",
    ]},
    # ── bando español: el palacio del virrey ──
    {"id": "consejo", "pre": 1.0, "frases": [
        "Ciudad de México, 31 de mayo de 1541. En el palacio del virrey se decide qué hacer con los caxcanes.",
        "[serious] Que se pregone la guerra. A fuego y a sangre.",
        "[cold] Y a los que se tomen vivos, de catorce años arriba… [short pause] que se les haga esclavos.",
    ]},
    # ── bando español: Alvarado en Guadalajara y su caída ──
    {"id": "alvarado", "frases": [
        "Junio de 1541. Pedro de Alvarado, el que peleó en Tenochtitlan y conquistó Guatemala, llega a Guadalajara con sus jinetes.",
        "[nervous] Señor adelantado, esperad los refuerzos del virrey. Esos peñoles no se toman a caballo.",
        "[laughs] ¿Esperar? ¡Para cuatro indios gatillos me basto yo con mis jinetes!",
        "Los mexicas le decían Tonatiuh, el sol. [short pause] El 24 de junio subió al peñol de Nochistlán. Lo estábamos esperando.",
        "Sus caballos resbalaban en el lodo, y sus hombres no veían de dónde les llovían las piedras.",
        "Cuando huyeron, el caballo de su escribano resbaló cuesta abajo… y le cayó encima.",
        "[crying] ¡Señor! ¿Qué os duele, señor?",
        "[weak] El alma… [short pause] me duele el alma.",
        "Pedro de Alvarado murió el 4 de julio de 1541.",
        "El capitán al que nadie había podido vencer… [short pause] se murió por nuestros cerros.",
    ]},
    {"id": "guadalajara", "frases": [
        "28 de septiembre de 1541.",
        "Envalentonados, bajamos a atacar Guadalajara. Caminamos de noche, miles, sin hacer ruido. [short pause] Yo iba entre los primeros.",
        "Al amanecer caímos sobre la ciudad. Peleamos más de tres horas en sus calles… y por un momento, creímos que era nuestra.",
        "[shouts] ¡Nadie se rinde! ¡Que nadie abra esa puerta! ¡Defended a vuestros hijos!",
        "Después supe que allá dentro una mujer, Beatriz Hernández, no los dejó rendirse.",
        "Al final, sus jinetes salieron por un costado y nos partieron en dos. [short pause] Yo solo vi caer a mis amigos.",
        "Regresamos al Mixtón con menos gente… [short pause] y sin cantos.",
    ]},
    {"id": "herida", "frases": [
        "Esa noche, en el peñol, no podías dormir.",
        "[sad] Padre… ¿los dioses nos dejaron solos?",
        "[sighs] No lo sé, hijo. [short pause] Pero nosotros no nos vamos a dejar solos.",
        "Te quedaste dormido en mi hombro, como cuando eras niño. [short pause] Yo no dormí.",
    ]},
    # ── ACTO V: el virrey y la caída (oct-dic 1541) ──
    {"id": "virrey", "pre": 2.0, "frases": [
        "2 de octubre de 1541. El virrey Antonio de Mendoza sale de la Ciudad de México. Va en persona.",
        "Lleva unos cuatrocientos cincuenta españoles y decenas de miles de aliados: tlaxcaltecas, mexicas, purépechas. Uno de los ejércitos más grandes que se habían visto en la Nueva España.",
        "[sad] Gente como nosotros, peleando del otro lado.",
        "El peñol de Nochistlán cayó en cuatro días, a cañonazos. Luego el de Juchipila, nuestro pueblo.",
        "Excelencia, ya se les ha leído el requerimiento más de veinte veces.",
        "[cold] Entonces que hablen los cañones.",
        "Uno por uno, los peñoles se desgranaron como una mazorca. [short pause] Hasta a Tenamaxtli tuvimos que rescatarlo de una trampa.",
    ]},
    {"id": "cerco", "frases": [
        "Y luego nos rodearon aquí. Sin agua que bajar a buscar. Sin camino por dónde huir.",
        "Los días se hicieron largos. El maíz se acabó primero, después el agua de las pilas.",
        "[softly] Come tú, Ollin. Yo ya comí.",
        "Tu madre te daba su ración y decía que ya había comido. [short pause] Yo sabía que no.",
        "Cada noche las fogatas de abajo eran más. [short pause] Y las nuestras, menos.",
    ]},
    {"id": "ultima", "frases": [
        "[whispers] Por eso te cuento todo esto, Ollin. Escúchame bien.",
        "Hay una vereda en la barranca del norte, por donde bajan los venados. Antes del amanecer, tú y tu madre se van por ahí.",
        "[crying] ¡No! ¡Yo me quedo a pelear contigo!",
        "[softly] ¿Te acuerdas de la piedra del río que me diste cuando eras niño? [short pause] Tómala. Así me llevas contigo.",
        "[serious] Alguien tiene que acordarse de nosotros. [short pause] Ese vas a ser tú.",
        "[crying] Tecuani…",
        "[whispers] Váyanse ya.",
    ]},
    {"id": "caida", "pre": 5.0, "post": 4.0, "frases": [
        "Subieron con la primera luz, por todos lados a la vez.",
        "Primero sus aliados, trepando por las piedras como hormigas. Detrás, los españoles con sus perros.",
        "Peleamos en los muros con piedras, con macanas, con las manos.",
        "Muchos, antes que dejarse marcar con el hierro, se arrojaron a la barranca.",
        "Lo último que vi fueron sus dos figuras perdiéndose en la vereda. [short pause] Y supe que algo nuestro había ganado.",
    ]},
    # ── EPÍLOGO: Ollin, ya viejo ──
    {"id": "epilogo", "pre": 3.0, "frases": [
        "El Mixtón cayó en diciembre de 1541. Miles de caxcanes fueron herrados y vendidos como esclavos.",
        "[softly] Mi padre no bajó del Mixtón.",
        "Mi madre y yo vivimos escondidos en la sierra muchos años.",
        "Tenamaxtli escapó. Siguió peleando casi diez años más. Cuando por fin se entregó, lo mandaron preso al otro lado del mar.",
    ]},
    # ── bando español: Tenamaxtli ante el Consejo de Indias ──
    {"id": "valladolid", "pre": 1.5, "frases": [
        "Valladolid, España, 1 de julio de 1555. Ante el Consejo de Indias se presenta un caxcán de Nochistlán, con la ayuda de fray Bartolomé de las Casas.",
        "[serious] Señores del Consejo: escuchad a este hombre. Su pueblo no se rebeló. [short pause] Se defendió.",
        "[firm] Los recibimos en paz. [short pause] Y nos quemaron, nos marcaron con hierro y nos vendieron.",
        "[emotional] Lo que hicimos en nuestros cerros no fue traición. [short pause] Fue justicia natural.",
        "[pleading] Pido que me devuelvan mi tierra… a mi mujer… [short pause] y a mis hijos.",
        "Nunca volvió. [short pause] Su último rastro en los papeles es de 1556.",
    ]},
    # ── final: orgullo con lágrimas ──
    {"id": "final", "pre": 2.0, "frases": [
        "Yo me casé, tuve hijos y nietos. Y a cada uno le conté esta historia, como mi padre me la contó a mí.",
        "Ellos quisieron que olvidáramos hasta los nombres. [short pause] Pero los cerros no olvidan.",
        "Hoy, casi quinientos años después, cuatro comunidades del sur de Zacatecas siguen llamándose caxcanas.",
        "[crying] El Mixtón sigue ahí. [short pause] Y nosotros también.",
        "[softly] Todavía guardo la piedra del río. [short pause] Me llamo Ollin. Soy caxcán.",
    ]},
    {"id": "cierre", "post": 5.0, "frases": [
        "Si esta historia llegó hasta ti, ya eres parte de su memoria.",
        "Compártela con alguien que deba conocerla. [short pause] Y dale me gusta, para que podamos contar más historias como esta.",
    ]},
]
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)


LYRIA = dict(
    estilo=("Cinematic orchestral film score for an animated historical epic about an indigenous Caxcan family in western Mexico, "
            "1525-1541: low strings, cello, solo clay flute and ocarina, rain stick, teponaztli and huehuetl log drums, soft "
            "choir hums, a recurring tender four-note flute motif for the father and son. Emotional like a feature film, never "
            "pop, no drum kit, no electronic beats; melodies kept low so dialogue sits on top."),
    escenas={
        "apertura": ("Opening title: cold wind, a deep sustained low string note, one distant war drum hit, ominous.", 2),
        "antes": ("Flashback: the sound world warms up, a gentle rising harp-like flourish into the past.", 2),
        "chirinos": ("Enemy camp at night, the Spanish side: cold, cruel, a low brass-like menace over a slow military drum, anger rising.", 6),
        "cedula": ("A royal order that changes nothing: a single cold church bell and a dark held cello note, bitter.", 4),
        "consejo": ("The viceroy's palace, a cold decision: stately but menacing low strings, a slow Spanish courtly pulse turning dark.", 5),
        "valladolid": ("A courtroom in Spain, dignity and defiance: a solemn slow build on strings, the four-note motif rising proudly, tears.", 6),
        "final": ("Pride with tears: the four-note motif swelling on full strings and choir, a heroic yet tender climax, then softening.", 7),
        "noche": ("Night on a besieged mountain: wind, a distant low drum like a heartbeat, a lonely clay flute plays the four-note motif, dread and tenderness.", 3),
        "rio": ("Peaceful canyon dawn and daily life: warm strings, flute and gentle hand drums, birdsong feeling, the four-note motif in warm major.", 3),
        "fiesta": ("Harvest festival at night: joyful log drums, rattles and flutes dancing in a circle, warm and festive.", 6),
        "teul": ("Sacred mountain at sunset: soft choir hums and flute, awe and reverence.", 3),
        "noticias": ("Rumors from the south: uneasy low strings under the flute, a quiet question.", 4),
        "llegada": ("The invaders arrive: rising dust-like tremolo strings, heavy marching low drums, cold brass-like low strings.", 7),
        "hierro": ("Burning villages and slavery: dark slow strings, a grieving cello, restrained tragedy.", 5),
        "encomienda": ("Years of servitude: a tired repeating ostinato like forced labor, a distant church bell, weary.", 4),
        "diez": ("Time passes, the son grows: the four-note motif returns on flute, hopeful but secret, then tension.", 4),
        "tlatol": ("Prophecy and ritual dance at night: hypnotic log drums and rattles accelerating, chanting choir, trance.", 8),
        "llamado": ("The call to war: a sudden drum roll, a conch-like horn, resolve.", 6),
        "decision": ("A family decision at night: intimate cello and flute, sorrow and courage.", 3),
        "penol": ("Climbing the mountain fortress: building heroic strings and drums, hope, the motif on full strings.", 6),
        "victoria": ("First victory: triumphant war drums and soaring strings, then a warm celebratory song feeling.", 8),
        "alvarado": ("The famous conquistador in the rain: thunder-like timpani, dark heroic strings turning into chaos, then a sudden stop.", 8),
        "guadalajara": ("Night march and attack on the city: stealthy pulsing drums growing into full battle, then collapse into a mournful cello.", 9),
        "herida": ("After the defeat, father and son at night: solo flute motif, very quiet and tender.", 2),
        "virrey": ("The viceroy's enormous army: overwhelming slow march of low brass-like strings and drums, despair.", 7),
        "cerco": ("The siege, hunger and thirst: sparse high violin harmonics, slow heartbeat drum, exhaustion.", 3),
        "ultima": ("Farewell between father and son: the four-note motif on cello and flute, heartbreaking, swelling then breaking.", 4),
        "caida": ("Dawn assault and the fall: thunderous war drums and choir, chaos, then a single sustained note and silence.", 9),
        "epilogo": ("Years later, an old man remembers: gentle flute and warm strings, sad but hopeful, the motif resolved.", 3),
        "cierre": ("Final invitation: the motif on flute over a warm resolved chord, natural fade-out.", 3),
    },
    # Lyria: tramos ≤ 80 s (los pedidos de > ~100 s salen cortos, docs/estilo_pegatina_flow.md §7b); 19 tramos, 41-69 s
    tramos=[
        (["apertura", "noche"], "Begin from near silence with cold wind. End on a soft held tone that opens toward a memory."),
        (["antes", "rio"], "Begin with a gentle rising flourish into the past. Warm, flowing; end gently, still warm."),
        (["fiesta", "teul"], "Begin festive in a circle of drums; settle into reverent awe on the mountain; end on a soft sad held note."),
        (["noticias"], "Begin quiet and uneasy; grow a little darker; end on an unresolved question."),
        (["llegada"], "Begin with a low rumble that grows into a heavy relentless march; end abruptly on a cold low hit."),
        (["chirinos", "hierro"], "Begin cold and cruel at night; turn into grieving tragedy; end on a broken quiet cello."),
        (["encomienda", "cedula"], "Begin weary and repetitive like forced labor; end bitter and cold with a single bell."),
        (["diez"], "Begin with the tender motif in secret; grow hopeful; end with quiet tension."),
        (["tlatol"], "Begin with a soft hypnotic pulse; accelerate into a trance dance; end at a peak, then a breath."),
        (["llamado", "decision"], "Begin with a sudden drum roll and horn; fall into an intimate night scene; end on quiet courage."),
        (["penol"], "Begin climbing, building heroic strength section by section; end proud and wide, full strings."),
        (["victoria", "consejo"], "Begin with a triumphant battle; turn into celebration; then cold and menacing in a palace; end dark."),
        (["alvarado"], "Begin arrogant and martial; turn into rain and chaos; end with a sudden stop and a lonely low note."),
        (["guadalajara", "herida"], "Begin with a stealthy night march; erupt into battle; collapse into mourning; end very quiet and tender."),
        (["virrey"], "Begin with an overwhelming slow march; grow heavier and hopeless; end on a crushing low chord."),
        (["cerco", "ultima"], "Begin sparse and exhausted; turn into a heartbreaking farewell; end breaking into silence."),
        (["caida", "epilogo"], "Begin with a thunderous dawn assault; reach chaos; one long held note and silence; then gentle memory."),
        (["valladolid"], "Begin solemn and dignified; build slowly toward defiance and tears; end strong but unresolved."),
        (["final", "cierre"], "Begin tender, swell into proud tears with the full motif; resolve warmly; natural fade-out to silence."),
    ],
)

# ── Flow (pegatina Flow cinematográfico): la FICHA y las fichas de personajes viven en _prompts.py (una sola fuente) ──
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _prompts as _PR
FICHA = dict(
    estilo=_PR.FICHA[:-1],
    cierre=" No text, no letters, no watermark.",
    personajes=dict(tecuani=_PR.TECUANI, tecuani_g=_PR.TECUANI_G, citlali=_PR.CITLALI, ollin_n=_PR.OLLIN_N,
                    ollin_j=_PR.OLLIN_J, abuelo=_PR.ABUELO, profeta=_PR.PROFETA, tenamaxtli=_PR.TENAMAXTLI,
                    guzman=_PR.GUZMAN, alvarado=_PR.ALVARADO, mendoza=_PR.MENDOZA, ollin_v=_PR.OLLIN_V),
)
