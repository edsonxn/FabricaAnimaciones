# -*- coding: utf-8 -*-
"""¿Quién es Satoshi Nakamoto? (documental serio, ~14 min, 16:9). Canal: Edsonxn.
Estilo `documental` (calco de «Detrás del Enigma» + motion graphics propios, ver docs/estilo_documental.md) con TABLERO DE DETECTIVE VIVO
(tablero.py): un corcho infinito por el que la cámara viaja sin parar; las pistas se clavan, se unen con hilos y conectores, y cada polaroid
se abre en una escena dibujada. Voz Faraon, SIN subtítulos quemados. Hechos al 3-oct-2026 (texto completo de las fuentes en fuentes/*.txt).

Datos verificados:
  - Wikipedia «Satoshi Nakamoto» (fuentes/wiki_satoshi.txt): activo 31-oct-2008 – 26-abr-2011; trabajo desde el 2.º trimestre de 2007; bitcoin.org
    registrado el 18-ago-2008; white paper el 31-oct en la lista de criptografía de metzdowd.com; v0.1 el 9-ene-2009; génesis con el titular de
    The Times «Chancellor on brink of second bailout for banks» (3-ene-2009); entregó el repositorio y la clave de alertas a Gavin Andresen a mediados
    de 2010; correo a Mike Hearn en 2011: «moved on to other things»; perfil de P2P Foundation: hombre de 37 años en Japón, nacido el 5-abr-1975;
    inglés nativo con ortografía y expresiones británicas y doble espacio tras el punto; Stefan Thomas graficó la hora de >500 mensajes (casi nada
    entre 5 y 11 GMT). Dorian: Newsweek, marzo de 2014 (Leah McGrath Goodman), Temple City, físico, proyectos de defensa clasificados, nombre de
    nacimiento Satoshi Nakamoto, cita «I am no longer involved in that... It's been turned over to other people», reporteros acampados y persecución
    en auto, «I am not Dorian Nakamoto» ese día, en septiembre la cuenta dijo haber sido hackeada. Hal Finney: unas cuadras de Dorian (Forbes,
    Andy Greenberg), Juola & Associates: el estilo más parecido; Greenberg vio sus correos y su cartera y le creyó. Szabo: bit gold; julio 2014,
    correo a Frisby «I'm afraid you got it wrong doxing me as Satoshi, but I'm used to it». Craig Wright: Wired y Gizmodo (8-dic-2015); Mellor,
    14-mar-2024 (cuatro declaraciones); sentencia escrita 20-may-2024 (falsificaciones, «lied to the court extensively and repeatedly»);
    19-dic-2024: un año de prisión suspendida por desacato. Peter Todd: HBO «Money Electric» (oct-2024), corrigió un detalle técnico de uno de los
    últimos mensajes de Satoshi una hora después; lo llamó «ludicrous». Len Sassaman (1980-2011): homenaje grabado en la cadena (presentación de
    Kaminsky, Black Hat 2011); documental «Finding Satoshi» (2026): sociedad Finney-Sassaman. Adam Back: NYT 2026 (Carreyrou), Hashcash, análisis
    estilométrico, menos actividad en las listas mientras Satoshi estaba activo, entrevista en El Salvador, lo negó varias veces.
  - Wikipedia «Hal Finney»: PGP Corporation; RPOW en 2004; recibió la 1.ª transacción el 12-ene-2009 (bloque 170, 10 BTC); ELA anunciada en
    octubre de 2009; murió el 28-ago-2014; criopreservado por Alcor. «Running bitcoin» (File:First tweet about bitcoin.png, dominio público).
  - Wikipedia «History of bitcoin»: pizza del 22-may-2010, 10.000 BTC por dos pizzas.
  - Wikipedia «Craig Steven Wright»: 2-may-2016 blog con firma; «reused an old signature from a bitcoin transaction performed in 2009 by Satoshi»;
    búsqueda web: la firma era la de la transacción Satoshi→Hal Finney; Peter Todd: «like photocopying someone else's signature on a publicly
    available document»; registró derechos de autor en EE. UU. en 2019; demandas por difamación desde 2019.
  - Correos Satoshi-Back (presentados en el juicio COPA, feb-2024): 1.er correo el 20-ago-2008 para citar Hashcash; Back respondió el 21 y le
    recomendó b-money de Wei Dai. Satoshi escribió a Wei Dai el 22-ago-2008.
  - Jameson Lopp (2024, vía coingape / bitcoin.com / coin360): 18-abr-2009, Hal Finney en la carrera de 10 millas de Santa Bárbara (salida 8:00,
    78 min, fotos); Satoshi envió un correo a Mike Hearn a las 9:16 hora del Pacífico, 2 min antes de que Hal terminara.
  - Aston University (abril de 2014, sciencedaily / coindesk): ejercicio de estudiantes de lingüística forense dirigido por Jack Grieve, sin revisión
    por pares: Szabo, el autor más probable del white paper. El white paper cita a Wei Dai (b-money) y a Back (Hashcash), no a bit gold.
  - WikiLeaks (dic-2010, blockworks): Satoshi pidió a WikiLeaks no usar bitcoin («the heat you would bring would likely destroy us at this stage»);
    último mensaje público en el foro el 12-dic-2010.
  - TechCrunch (8-abr-2026): Carreyrou reunió correos de tres listas de criptografía (1992-2008) y usó IA para comparar estilos (sin guiones en
    palabras compuestas, confundía «its»/«it's»); Back fue el mejor resultado; Back en X: «i'm not satoshi», «combination of coincidence and similar
    phrases from people with similar experience and interests». coin360: lo negó más de media docena de veces en El Salvador; Back más callado en
    2008-2011 y más activo después; último correo de Satoshi el 26-abr-2011; ~1,1 millones de BTC.
  - Arkham vía cryptotimes (28-sep-2026): 1,096 millones de BTC en las carteras atribuidas a Satoshi, 90.350 millones de dólares a 82.680 USD/BTC.
    financefeeds (abr-2026): ~22.000 direcciones; patrón «Patoshi» de Sergio Lerner (2013).
  - Peter Todd y su seguridad (Wired vía cointelegraph/coindesk, oct-2024): peticiones de dinero y miedo por su seguridad (él dijo después que el
    titular de «esconderse» fue exagerado): por eso la narración NO dice que se escondió.
  - Análisis propio (datos/forum_posts.json del Satoshi Nakamoto Institute, script datos.py): 543 mensajes en foros; entre las 5:00 y las 11:59 UTC
    solo 7. Ortografía mixta (colour 2 / color 4), bloody 1, maths 1, grey 2.
  - Paul Le Roux (cryptotimes 28-sep-2026, Wikipedia «Paul Le Roux»): nacido en Bulawayo (Rodesia, hoy Zimbabue) en 1972; creó E4M (cifrado de
    disco, base de TrueCrypt); red criminal desde Filipinas; pasaporte diplomático congoleño del 5-ago-2008 a nombre de «Paul Solotshi Calder Le Roux»;
    arrestado en sept-2012 (Liberia, DEA); 25 años de prisión en 2020; Evan Ratliff no halló vínculo directo; Greg Maxwell comparó estilos de código
    de E4M y Bitcoin: distintos. La teoría volvió a circular en X la semana del 28-sep-2026.
  - FOIA (fxstreet / financefeeds): abril de 2025, James A. Murphy demanda al DHS; la demanda alega que la agente Rana Saoud dijo en 2019 que
    investigadores del DHS viajaron a California y entrevistaron a cuatro personas que estarían detrás de bitcoin; sin documentos publicados conocidos.
  - Busto de Budapest (sept-2021, Graphisoft Park; bitcoin.com / ABC): cara de compuesto bronce-aluminio pulido para que cada visitante vea su propio
    reflejo; lema «We are all Satoshi»; escultores Réka Gergely y Tamás Gilly.
Pronunciación: la voz es española; nombres ingleses fonéticos en la narración (PRON); en pantalla van con su ortografía real.
"""

TITULO = "¿Quién es Satoshi Nakamoto?"
ARCHIVO = "satoshi_nakamoto"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 96
GAP = 0.36
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)
MEZCLA = dict(musica=-22.0, sfx=-26.0)
SUBTITULOS = False          # el estilo dibuja su propio texto sincronizado; el .srt se genera igual

# --- pronunciación: token del guion -> texto que lee la voz española -----------------------------------------------------
PRON = {
    "{HF}": "Jal Fíni", "{HA}": "Jal",
    "{NS}": "Nik Sábo", "{SZ}": "Sábo",
    "{AB}": "Ádam Bak", "{BK}": "Bak",
    "{CW}": "Kreig Rait",
    "{DN}": "Dórian Nakamoto", "{DO}": "Dórian",
    "{LS}": "Len Sásaman",
    "{PT}": "Píter Tod",
    "{JC}": "Yon Carrerú",
    "{NYT}": "Niu York Taims",
    "{TT}": "Di Taims",
    "{HC}": "jáshcash",
    "{GA}": "Gávin Ándresen",
    "{TC}": "Témpel Siti",
    "{NW}": "Niusuik",
    "{WD}": "Uei Dai",
    "{LB}": "Líman Bróders",
    "{JM}": "Yeims Mélor",
    "{WL}": "Uikiliks",
    "{BG}": "bit góld",
    "{FB}": "Forbs",
    "{TH}": "Teranos",
    "{LR}": "Pol Le Ru",
    "{SL}": "Solochi",
}
# lo que Whisper oye -> como está en el guion (minúsculas, sin tildes); lo usa qa.normaliza
ALIAS_QA = {
    "hal finney": "jal fini", "hal finny": "jal fini", "jal finney": "jal fini", "hal fini": "jal fini", "jal finni": "jal fini", "hal": "jal",
    "nick szabo": "nik sabo", "nick sabo": "nik sabo", "nic sabo": "nik sabo", "szabo": "sabo", "nik szabo": "nik sabo",
    "adam back": "adam bak", "adam bach": "adam bak", "back": "bak", "bach": "bak", "buck": "bak",
    "craig wright": "kreig rait", "craig rait": "kreig rait", "creig rait": "kreig rait", "kreig wright": "kreig rait", "craig right": "kreig rait",
    "dorian": "dorian", "len sassaman": "len sasaman", "lensasaman": "len sasaman", "sassaman": "sasaman",
    "peter todd": "piter tod", "peter tod": "piter tod", "piter todd": "piter tod", "todd": "tod",
    "john carreyrou": "yon carreru", "jon carreyrou": "yon carreru", "john carrero": "yon carreru", "yon carrero": "yon carreru", "jon carrero": "yon carreru",
    "carreyrou": "carreru", "carrerou": "carreru", "carreru": "carreru",
    "new york times": "niu york taims", "niu york times": "niu york taims", "the times": "di taims", "de times": "di taims", "di times": "di taims", "the taims": "di taims",
    "hashcash": "jashcash", "hash cash": "jashcash", "jash cash": "jashcash", "hashkash": "jashcash",
    "gavin andresen": "gavin andresen", "gavin andersen": "gavin andresen", "gavin anderson": "gavin andresen",
    "temple city": "tempel siti", "temple siti": "tempel siti", "tempel city": "tempel siti",
    "newsweek": "niusuik", "news week": "niusuik", "wei dai": "uei dai", "wei day": "uei dai", "wey dai": "uei dai", "huey dai": "uei dai",
    "lehman brothers": "liman broders", "leman brothers": "liman broders", "liman brothers": "liman broders",
    "james mellor": "yeims melor", "james melor": "yeims melor", "yeims mellor": "yeims melor",
    "wikileaks": "uikiliks", "wiki leaks": "uikiliks", "bit gold": "bit gold", "bitgold": "bit gold", "forbes": "forbs",
    "theranos": "teranos", "satoshi nakamoto": "satoshi nakamoto", "bitcoins": "bitcoins", "bitcoin": "bitcoin",
    "bitcoin org": "bitcoin punto org", "halfini": "jal fini", "jalfini": "jal fini", "hal fini": "jal fini", "weidai": "uei dai", "wedai": "uei dai",
    "menciona a bit gold": "menciona bit gold", "john carreru": "yon carreru", "jon carreru": "yon carreru", "john carrero": "yon carreru",
    "paul le roux": "pol le ru", "paul leroux": "pol le ru", "pol le roux": "pol le ru", "paul le ru": "pol le ru", "pol leru": "pol le ru",
    "le roux": "le ru", "solotshi": "solochi", "solochi": "solochi", "zimbabwe": "zimbabue",
}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "En algún lugar de la cadena de bloques hay más de un millón de bitcoins que nadie ha tocado desde hace más de quince años.",
        "A precios de finales de septiembre de dos mil veintiséis, valen unos noventa mil millones de dólares.",
        "Su dueño inventó la primera criptomoneda del mundo y la cuidó durante dos años.",
        "Y un día de abril de dos mil once escribió que se había pasado a otras cosas. Nunca volvió.",
        "Periodistas, programadores, una cadena de televisión y hasta un tribunal de Londres han intentado ponerle cara.",
        "Cada uno señaló a alguien distinto.",
        "Este es el tablero. Estas son las pistas. Y estos son los sospechosos.",
        "La pregunta sigue abierta desde hace diecisiete años: ¿quién es Satoshi Nakamoto?",
    ]},
    {"id": "origen", "frases": [
        "Para entender la primera pista, hay que volver a dos mil ocho.",
        "El quince de septiembre quiebra {LB}, uno de los bancos de inversión más grandes de Estados Unidos.",
        "El pánico recorre el mundo, y los gobiernos rescatan a los bancos con dinero público.",
        "Pero alguien ya llevaba más de un año trabajando en otra idea.",
        "El dieciocho de agosto, semanas antes de la quiebra, se había registrado un dominio en internet: bitcoin punto org.",
        "Dos días después, un desconocido le escribe a un criptógrafo británico, {AB}, para preguntarle cómo citar su trabajo.",
        "Es el primer rastro conocido de Satoshi Nakamoto.",
        "El treinta y uno de octubre envía a una lista de correo de criptografía un documento de nueve páginas.",
        "Su título: Bitcoin, un sistema de dinero electrónico de persona a persona.",
        "Dinero sin bancos. Sin nadie en medio. Protegido solo por las matemáticas.",
    ]},
    {"id": "genesis", "frases": [
        "El tres de enero de dos mil nueve, Satoshi crea el primer bloque de la cadena: el bloque génesis.",
        "Y dentro de él, escondido entre los datos, deja un mensaje.",
        "Es el titular de ese día del diario británico {TT}: el ministro de Hacienda, a punto de un segundo rescate a los bancos.",
        "Sirve como sello de fecha. Pero también parece una declaración de principios.",
        "Y es otra pista sobre su autor: eligió un periódico británico, no uno japonés ni estadounidense.",
        "El nueve de enero publica el programa. Uno de los primeros en descargarlo es un veterano de la criptografía: {HF}.",
        "{HA} escribe en internet dos palabras: corriendo bitcoin.",
        "El doce de enero, Satoshi le envía diez bitcoins. Es la primera transacción de la historia.",
    ]},
    {"id": "fantasma", "frases": [
        "Durante los dos años siguientes, Satoshi está en todas partes y en ninguna.",
        "Escribe más de quinientos mensajes en los foros, responde correos y corrige el código casi él solo.",
        "Pero nunca habla de sí mismo. Ni una llamada, ni una foto, ni una reunión.",
        "En un perfil de internet decía ser un hombre japonés, nacido en mil novecientos setenta y cinco.",
        "En mayo de dos mil diez, un programador paga dos pizzas con diez mil bitcoins. Hoy valdrían cientos de millones de dólares.",
        "En diciembre, {WL} se queda sin bancos para recibir donaciones, y en el foro muchos piden que use bitcoin.",
        "Satoshi responde alarmado: el proyecto es demasiado pequeño, y esa atención podría destruirlo.",
        "Días después publica su último mensaje en el foro.",
        "En abril de dos mil once, en un correo a otro desarrollador, escribe que se ha pasado a otras cosas.",
        "Después de eso, silencio.",
    ]},
    {"id": "fortuna", "frases": [
        "Pero Satoshi dejó algo más que código.",
        "En dos mil trece, el investigador Sergio Lérner encontró en los primeros bloques una huella: la firma de un mismo minero.",
        "Ese minero, casi con seguridad Satoshi, acumuló alrededor de un millón cien mil bitcoins.",
        "Están repartidos en unas veintidós mil direcciones, y no se han movido ni una sola vez.",
        "Y aquí está la clave de todo este tablero.",
        "Para demostrar que eres Satoshi no hace falta un documento ni un testigo. Basta con mover una de esas monedas, o firmar un mensaje con su llave.",
        "En diecisiete años, nadie lo ha hecho.",
    ]},
    {"id": "perfil", "frases": [
        "Así que los investigadores hicieron lo que haría cualquier detective: estudiar cómo escribe.",
        "Su inglés es el de alguien nativo. Y en lugar de rasgos japoneses, tiene rasgos británicos.",
        "Usa ortografía y expresiones del Reino Unido, aunque a veces las mezcla con las de Estados Unidos.",
        "Y pone dos espacios después de cada punto, una costumbre de quien aprendió a escribir a máquina.",
        "Luego están sus horarios.",
        "Para este video analizamos la hora de sus quinientos cuarenta y tres mensajes en los foros.",
        "Entre las cinco de la mañana y el mediodía, en hora universal, casi no hay ninguno. Solo siete.",
        "Si ese hueco es su sueño, en la costa este de Estados Unidos dormía de medianoche a las siete. En Japón, habría dormido toda la tarde.",
        "Con ese perfil, la prensa empezó a buscar. Y el primer nombre llegó con un titular explosivo.",
    ]},
    {"id": "dorian", "frases": [
        "Marzo de dos mil catorce. La revista {NW} publica en portada que encontró a Satoshi Nakamoto.",
        "Vive en {TC}, California. Es físico, trabajó en proyectos militares clasificados, y su nombre de nacimiento es, literalmente, Satoshi Nakamoto.",
        "En la puerta de su casa, la periodista le pregunta por bitcoin. Y él responde algo que suena a confesión.",
        "Ya no estoy involucrado en eso. Se lo entregaron a otras personas.",
        "Decenas de reporteros acampan frente a su casa y lo persiguen en auto por las calles de Los Ángeles.",
        "Él lo niega todo: dice que nunca había oído hablar de bitcoin, y que creyó que le preguntaban por su antiguo trabajo.",
        "Y entonces pasa algo extraño. La vieja cuenta de Satoshi, callada durante cinco años, publica una sola frase: no soy {DN}.",
        "Meses después, esa misma cuenta dijo haber sido hackeada. Así que ni siquiera ese mensaje es una prueba.",
        "Pero esta pista abrió otra. A unas cuadras de la casa de {DO}, en el mismo pueblo, vivía alguien mucho más interesante.",
    ]},
    {"id": "hal", "frases": [
        "{HF}. El hombre que recibió la primera transacción.",
        "Un pionero del cifrado, que trabajó durante años en una empresa de software de privacidad.",
        "En dos mil cuatro creó un sistema de prueba de trabajo reutilizable, un antecesor directo de bitcoin.",
        "Un análisis de estilo para la revista {FB} concluyó que su forma de escribir era la más parecida a la de Satoshi.",
        "Pero {HA} siempre lo negó. Y le mostró a un periodista sus correos con Satoshi y el historial de su cartera.",
        "Además, tiene algo parecido a una coartada.",
        "El dieciocho de abril de dos mil nueve corría una carrera de diez millas en Santa Bárbara. Hay fotos y registro de tiempos.",
        "Mientras corría, Satoshi le enviaba correos a otro desarrollador. Uno salió dos minutos antes de que {HA} cruzara la meta.",
        "Ese mismo año le diagnosticaron esclerosis lateral amiotrófica. Murió en agosto de dos mil catorce.",
        "Su cuerpo fue criopreservado, con la esperanza de que algún día pueda despertar.",
    ]},
    {"id": "szabo", "frases": [
        "El siguiente nombre es {NS}.",
        "Diez años antes de bitcoin, diseñó en papel algo llamado {BG}: oro digital creado con poder de cómputo.",
        "Es la idea más parecida a bitcoin que existió antes de bitcoin.",
        "En dos mil catorce, estudiantes de lingüística forense de una universidad británica concluyeron que su estilo era el más cercano al de Satoshi.",
        "Y hay un detalle curioso: el documento de Satoshi cita a {WD}, cita a {AB}, pero no menciona {BG}.",
        "¿Un descuido? ¿O alguien que no quería que lo relacionaran con su propia idea?",
        "{SZ} lo negó. A un autor que lo había señalado le respondió: te equivocaste, pero ya estoy acostumbrado.",
    ]},
    {"id": "wright", "frases": [
        "Hasta aquí, todos los sospechosos niegan ser Satoshi. El siguiente hizo exactamente lo contrario.",
        "{CW}, un informático australiano. En diciembre de dos mil quince, dos medios publicaron documentos filtrados que lo señalaban.",
        "Y en mayo de dos mil dieciséis lo anunció él mismo: yo soy Satoshi Nakamoto.",
        "Como prueba, publicó una firma digital. Pero en pocas horas, varios expertos descubrieron que era una firma vieja, copiada de la cadena.",
        "Era la de la transacción de dos mil nueve entre Satoshi y {HF}.",
        "Un desarrollador lo comparó con fotocopiar la firma de otra persona en un documento público.",
        "Aun así, durante años demandó a quienes lo llamaban mentiroso.",
        "En dos mil veinticuatro, una alianza de empresas lo llevó a juicio en Londres.",
        "El catorce de marzo, el juez {JM} fue tajante: {CW} no es el autor del documento, no es Satoshi y no creó bitcoin.",
        "En su sentencia escrita concluyó que había mentido al tribunal de forma extensa y repetida, y que sus pruebas eran falsificaciones.",
        "En diciembre lo condenaron a un año de prisión, con la pena suspendida, por desacato.",
    ]},
    {"id": "todd", "frases": [
        "Con el impostor descartado, la búsqueda tomó otro rumbo.",
        "En octubre de dos mil veinticuatro, un documental de televisión apuntó a un desarrollador canadiense: {PT}.",
        "Su gran prueba: en dos mil diez, recién llegado al foro, {PT} corrigió un detalle técnico de uno de los últimos mensajes de Satoshi, apenas una hora después.",
        "Para el director, era como si Satoshi terminara su propia frase con otra cuenta.",
        "{PT} lo llamó ridículo. Después contó que temía por su seguridad.",
        "En abril de dos mil veintiséis, otro documental propuso algo distinto: que Satoshi no era una persona, sino dos.",
        "{HF}, y un joven criptógrafo, {LS}.",
        "{LS} murió en julio de dos mil once, poco más de dos meses después del último correo de Satoshi.",
        "Poco después, alguien grabó en la cadena de bloques un homenaje a su memoria.",
        "Pero esa teoría tiene un problema: ninguno de los dos puede ya negarla, ni confirmarla.",
    ]},
    {"id": "leroux", "frases": [
        "Y la lista no deja de crecer. A finales de septiembre de este año, volvió a circular una vieja teoría.",
        "{LR}: un programador nacido en la actual Zimbabue, que creó un programa de cifrado y después dirigió una red criminal internacional.",
        "En agosto de dos mil ocho, dos semanas antes del primer correo de Satoshi, recibió un pasaporte diplomático del Congo con un segundo nombre: {SL}.",
        "En dos mil doce lo arrestaron, y desde entonces está en prisión. Eso explicaría por qué las monedas nunca se movieron.",
        "Pero el periodista que pasó años investigando su vida nunca encontró un vínculo directo con bitcoin.",
        "Y un programador que comparó el código de ambos concluyó que no se parecen.",
    ]},
    {"id": "back", "frases": [
        "Y así llegamos al último nombre del tablero. El mismo con el que empezó todo.",
        "{AB}, criptógrafo británico. En mil novecientos noventa y siete inventó {HC}, el sistema de prueba de trabajo en el que se basa la minería de bitcoin.",
        "Es el único sospechoso que aparece citado dentro del propio documento de Satoshi.",
        "Y fue la primera persona a la que Satoshi escribió. {BK} le respondió con una recomendación: leer a {WD}.",
        "En abril de dos mil veintiséis, {JC}, el periodista que destapó el fraude de {TH}, publicó en el {NYT} dieciocho meses de investigación.",
        "Reunió miles de mensajes de viejas listas de criptografía y usó inteligencia artificial para comparar cómo escribía cada participante.",
        "Satoshi tenía manías al escribir, como no poner guiones en ciertas palabras compuestas. De todos los candidatos, el que más se le parecía era {BK}.",
        "Además, {BK} estuvo inusualmente callado en esas listas mientras Satoshi estaba activo, y volvió a escribir más cuando desapareció.",
        "En un encuentro en El Salvador, {JC} se lo preguntó en persona. {BK} lo negó más de media docena de veces.",
        "Tras la publicación respondió por escrito: no soy Satoshi. Dice que todo es coincidencia: gente con la misma formación, los mismos intereses, las mismas frases.",
        "Y en algo tiene razón: no hay una firma, ni una moneda movida, ni una prueba directa.",
    ]},
    {"id": "archivo", "frases": [
        "Pero quizá la respuesta ya exista, guardada en un archivo del gobierno de Estados Unidos.",
        "Según una demanda de dos mil veinticinco, una agente del Departamento de Seguridad Nacional contó en dos mil diecinueve que su equipo viajó a California.",
        "Allí, dijo, entrevistaron a cuatro personas relacionadas con la creación de bitcoin.",
        "Un abogado demandó al gobierno para obtener las notas de esas entrevistas. Hasta donde se sabe, no se ha publicado ninguna.",
    ]},
    {"id": "espejo", "frases": [
        "En Budapest hay un busto de Satoshi con la cara de metal pulido.",
        "Quien se acerca a mirarlo no ve a nadie: ve su propio reflejo.",
        "Sus escultores lo resumieron en una frase: todos somos Satoshi.",
    ]},
    {"id": "cierre", "post": 11.0, "frases": [
        "Después de diecisiete años, este es el tablero.",
        "Un hombre que se llamaba Satoshi Nakamoto, pero no lo era. Uno que corría mientras Satoshi escribía. Uno que imaginó el oro digital.",
        "Uno que se proclamó Satoshi y falsificó las pruebas. Uno que corrigió su frase. Y uno que recibió su primer correo.",
        "En medio, un millón de bitcoins inmóviles. Y una llave que nadie ha vuelto a usar.",
        "Quizá Satoshi murió. Quizá perdió sus llaves. Quizá está viendo todo esto.",
        "O quizá desaparecer fue la última parte de su diseño.",
        "Porque mientras nadie sepa quién es Satoshi Nakamoto, bitcoin no le pertenece a nadie.",
    ]},
]

# aplica la pronunciación a todas las frases (la voz y el QA leen estos textos)
for _e in ESCENAS:
    _e["frases"] = [__import__("functools").reduce(lambda s, kv: s.replace(*kv), PRON.items(), f) for f in _e["frases"]]

# todd_2 termina hablando hasta el final («...apenas una hora después.»): 16 tomas con CER 0 y cola 0,36-0,64 -> se acepta hasta 0,38
TAIL_MAX_POR_FRASE = {"todd_2": 0.38}

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Dark, propulsive investigative documentary score, modern and cinematic: a steady pulsing synth bass, ticking hi-hat clock, "
            "low cello ostinatos, glassy digital textures and soft data-like arpeggios, occasional deep impacts on discoveries. "
            "Addictive forward momentum, like a detective connecting clues. No vocals, no big orchestral melody, never cheerful."),
    escenas={
        "gancho": ("Hook: low drone, a pulse that starts and builds tension, ticking clock, glassy arpeggio, a deep hit and sudden stop.", 5),
        "origen": ("2008 crisis: tense low strings, a news-like urgent pulse, then a quiet curious motif as an idea is born.", 4),
        "genesis": ("Discovery: a mysterious digital arpeggio, a soft reveal swell, wonder and secrecy.", 4),
        "fantasma": ("A ghost: sparse piano notes over a cold pad, a steady pulse fading out into near silence at the end.", 4),
        "fortuna": ("Weight of a hidden fortune: deep sub bass, slow heavy pulses, a sense of something enormous and untouched.", 5),
        "perfil": ("Analysis: a clean rhythmic pulse, ticking, data arpeggios, focused and methodical, rising slightly.", 5),
        "dorian": ("Media frenzy: quicker pulse, rising tension, a chase feeling, then an eerie twist at the end.", 6),
        "hal": ("Human and melancholic: soft felt piano over a warm pulse, a running rhythm in the middle, then a tender sad close.", 4),
        "szabo": ("Puzzle: mysterious plucked motif, curious and questioning, steady pulse.", 4),
        "wright": ("The impostor: confident swagger that turns sour, distorted bass, courtroom gravity, a final heavy verdict hit.", 7),
        "todd": ("Shifting theories: unsettled pulse, two alternating motifs, ghostly pads, unresolved.", 5),
        "back": ("Final suspect: tension builds steadily to the peak of the video, relentless pulse, rising strings, no release.", 8),
        "cierre": ("Resolution without answer: the pulse drops away, ethereal pad, a slow solitary piano motif, haunting final note.", 3),
    },
)
MUSICA = {k["id"]: dict(sabor="tension", raiz=38) for k in ESCENAS}   # solo por si se corriera la música procedural (NO se usa: va Lyria)
