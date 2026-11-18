# -*- coding: utf-8 -*-
"""GUION de «Cómo murió REALMENTE cada villano de Call of Duty» (motor SECUENCIA YT, Expediente 141, 17-nov-2026).
Plantilla: videos/cod_mandela2/ (misma fórmula; cambia UNA variable: el EJE, de secretos a personajes). Investigación: investigacion.md.
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo; nombres TAL CUAL (A/B del 13-nov). Queja justa de @v5x777cod_rdr_fan0
(voz frustrada/forzada en los momentos tristes): solo [serious], [deadpan] y [short pause], nada de emoción actuada.
REGLA DE ORO: cada frase nombra algo que SE VE; si la voz nombra un sonido, se OYE («post» = la voz calla y suena el clip).
Violencia: los clips se cortan ANTES del impacto (lección de cod_mandela2 puesto 2).
"""

TITULO = "Cómo murió REALMENTE cada villano de Call of Duty"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "sigh", "annoy", "frustr"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
FONETICA = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-012": .9, "scene-031": .9, "scene-044": .9, "scene-086": .9, "scene-097": .9, "scene-104": .9, "scene-115": .9},
    recorte_por={"scene-037": .14, "scene-038": .14},   # marca «ItsUniter PRESENTS» arriba a la derecha
    yt=dict(sufijo="Call of Duty", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # OST oficial (audio/ost/_catalogo.txt), nunca Lyria

# Pausas con la voz callada («si la voz nombra un sonido, se oye»), clip cortado ANTES del golpe:
#   p15 Irons «I gave you that arm» · p13 Hassan «We are not attacking… We are invading» · p05 Dragovich «Tried?» ·
#   p03 Menéndez «Martyr me… for Cordis Die» · p02 Mason «My name is Viktor Reznov!» · p01 Price «Off the list»
# Comentarios (≤ 10 días, ninguno usado antes): contraburla @thefert4229 p15 · @qtdrox p14 · @FABIANWOW p02 ·
#   @leukojb6772 p10 (pregunta de Bell) · agradecimientos en el cierre: @Prophet9205, @Daanw-k6m, @almidon809_provisional7, @v5x777cod_rdr_fan0
ESCENAS = [
    {"id": "intro", "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: los villanos de Call of Duty. Y cómo murieron de verdad.",
        "Uno murió a puñetazos en un callejón de Nueva York. Otro, colgado de un cable en un hotel de Dubái. Y otro sigue vivo, aunque le dispararon con un Magnum.",
        "Y a otro lo viste morir con tus propios ojos. Y aun así, el juego te mintió sobre quién lo mató.",
        "Veinte villanos, cada muerte con el juego en pantalla. Aviso: hay spoilers de Modern Warfare 4. Y en el número uno, un villano que tuvo que morir dos veces.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. El general Heinrich Amsel.",
        "World at War, dos mil ocho. Stalingrado, misión Vendetta: Reznov y Dimitri Petrenko, dos francotiradores rusos, cazan al general alemán que manda en la ciudad.",
        "Amsel huye de su cuartel con su escolta, y Petrenko lo derriba con el Mosin-Nagant que le dio Reznov. Reznov se ríe a carcajadas.",
        "¿Y por qué no disparó Reznov, si la venganza era suya? [short pause] Porque los alemanes le habían volado el dedo índice. El del gatillo.",
    ]},
    {"id": "p19", "post": 2.2, "frases": [
        "En el diecinueve, Khaled Al-Asad.",
        "Call of Duty 4, dos mil siete. El hombre que ejecutó al presidente Al-Fulani delante de una cámara: atado a una silla, y de un tiro.",
        "En la misión Casa franca, Price lo tiene atado a una silla y lo interroga. Entonces suena el teléfono de Al-Asad.",
    ]},
    {"id": "p19b", "frases": [
        "Del otro lado está Imran Zakhaev. Price acaba con Al-Asad con su M1911. [deadpan] Murió exactamente como mató al presidente. Atado a una silla.",
        "Y la bomba que mató a treinta mil marines la detonó él. Por orden de Makarov. Eso no lo supimos hasta Modern Warfare 3.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. Victor Zakhaev, el hijo del ultranacionalista.",
        "Misión Los pecados del padre. Soap, Gaz y Price persiguen a Victor por las afueras de Volgogrado, hasta la azotea de un edificio.",
        "Acorralado, Victor saca su M1911. Y la usa contra sí mismo, antes de que Soap se la pueda quitar.",
        "Pero en Modern Warfare 2, la versión oficial del Pentágono es otra: que Victor Zakhaev murió en un accidente de coche, a las afueras de Volgogrado. [deadpan] Un accidente de coche. En una azotea.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, Omar Sulaman. El Lobo.",
        "En el Modern Warfare de dos mil diecinueve, es el terrorista más buscado de Urzikstán, al que culpan de robar el gas de Kastovia.",
        "En La guarida del Lobo lo encuentras grabando un mensaje frente a una cámara, con un chaleco bomba puesto. Levanta el detonador, y un disparo lo detiene. El chaleco sigue contando, y hay que cortar el cable verde.",
        "Lo que pocos recuerdan: el robo del gas no lo planeó el Lobo. Lo planeó Hadir, el hermano de Farah. [deadpan] El Lobo murió con el crimen de otro en su ficha.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. El general Roman Barkov.",
        "El general ruso que invadió Urzikstán, y al que al final Moscú deja de contestarle por radio.",
        "En la misión En el horno, Barkov escapa en su propio helicóptero. Pero el piloto es Nikolai, y Farah sube a bordo con un cuchillo.",
        "Sus últimas palabras: que el país de Farah cría terroristas, y que debió hacer más. Si todavía respira, Farah lo patea fuera del helicóptero.",
        "Y un detalle del expediente: en los hombros lleva charreteras de coronel, no de general. [deadpan] Murió sin el ascenso.",
    ]},
    {"id": "p15", "post": 3.4, "frases": [
        "En el quince, Jonathan Irons.",
        "Advanced Warfare. El dueño de Atlas, el ejército privado más grande del mundo. El hombre que le dio a Jack Mitchell un brazo nuevo, después de que perdiera el suyo en Seúl.",
        "Misión final, Terminal. Una explosión tira a Irons del edificio, y se agarra del brazo de Mitchell. Del brazo artificial. Escucha.",
    ]},
    {"id": "p15b", "frases": [
        "Yo te di ese brazo. Y Mitchell se lo corta con su propio cuchillo. Irons cae con el brazo de Atlas en la mano.",
        "En el expediente anterior, thefert escribió: la voz es IA, nomás para que sepan, papus. Gracias por el aviso, thefert.",
        "[deadpan] Mitchell también tenía un brazo artificial. Y con ese brazo artificial acabó con el villano. Lo artificial también hace el trabajo.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. El almirante Salen Kotch.",
        "Infinite Warfare, dos mil dieciséis. El villano del Frente de Defensa de los Asentamientos, interpretado por Kit Harington, el Jon Snow de Juego de Tronos.",
        "En la Operación Bandera Negra, Reyes lo acorrala en el puente de la nave Olympus Mons. Kotch, herido, le suelta el discurso: matarme no es ganar.",
        "Si le cortas el discurso con el cuchillo antes de que termine, el juego te da un logro que se llama No sabes nada. [deadpan] La frase que le decían a Jon Snow en Juego de Tronos.",
        "Y lo raro: Kotch no es el jefe final. Muere en la sexta operación de siete, y el juego termina sin él, en Marte.",
        "Como qtdrox, que escribió que no llevaba ni la mitad del video anterior, que todo era IA, y que no lo iba a terminar. [short pause] Kotch tampoco terminó su juego. Y se perdió el final en Marte.",
    ]},
    {"id": "p13", "post": 4.6, "frases": [
        "En el trece, Hassan Zyani.",
        "Modern Warfare 2, dos mil veintidós. Misión Countdown, un rascacielos de Chicago. Hassan arrastra a Soap hacia una ventana que acaba de volar, para tirarlo al vacío.",
        "Y le suelta su amenaza final. Escucha.",
    ]},
    {"id": "p13b", "frases": [
        "No estamos atacando. Estamos invadiendo. Ghost no lo deja decir nada más: lo derriba con un francotirador desde el edificio de enfrente.",
        "Lo mejor: Hassan amenaza a la nación de Soap creyendo que es estadounidense. [deadpan] Soap es escocés.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Gabriel Rorke, el cazador de Ghosts.",
        "En Call of Duty Ghosts, de dos mil trece, es el antiguo líder de los Ghosts, que se pasó a la Federación.",
        "En la última misión, el tren descarrila y cae al agua. Hesh lo sujeta, y Logan le dispara con un Magnum que tiene una sola bala. Lo dan por muerto.",
        "Pero en la orilla, Rorke se levanta, le rompe el brazo a Logan y se lo lleva a rastras. Después de los créditos, Logan está en un pozo en el Amazonas, recibiendo la misma tortura que sufrió Rorke.",
        "Y nunca salió una segunda parte. [deadpan] Rorke no murió. Se quedó vivo para siempre.",
    ]},
    {"id": "p11", "frases": [
        "En el once, Edward Richtofen. El doctor de los Zombies.",
        "Murió más de una vez. En The Giant, de Black Ops 3, su versión de Primis sale del teletransportador y le dispara a su versión de Ultimis.",
        "Pero el final de verdad es Tag der Toten, en Black Ops 4. Todos alrededor de una fogata, envenenados. Richtofen dice: lo sé, y lo siento mucho. Y Nikolai, su amigo, lo remata con su revólver, para cerrar la paradoja del multiverso.",
        "[short pause] No lo mató un zombi. Lo mató su amigo.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. Perseus.",
        "Black Ops Cold War, dos mil veinte. El espía soviético que esconde bombas nucleares por toda Europa.",
        "En ningún final lo matas. En el bueno, los bombarderos arrasan su base antes de que detone las bombas, y Perseus escapa. En el malo, se burla del cadáver de Adler.",
        "¿Cómo murió entonces? De cáncer, en mil novecientos ochenta y tres. Lo revela la cinemática de la temporada seis: Adler encuentra a Stitch junto a una tumba en los bosques de Verdansk.",
        "Perseus era una idea, y Stitch la heredó. Y leukojb me preguntó si Bell está muerto, o si hay pistas de que sigue con vida. Buena pregunta. Esa da para un expediente entero.",
    ]},
    {"id": "p09", "frases": [
        "En el nueve, Jane Harrow.",
        "Black Ops 6, dos mil veinticuatro. La espía que traicionó al equipo de Adler y se unió al Panteón.",
        "En la última misión, Jaque mate, el helicóptero de la fuga se hunde en el mar Negro. Case la sujeta bajo el agua, con la toxina Cradle en la cabeza, y una voz le dice: termínalo.",
        "Ella suplica, y la pantalla se va a negro. [short pause] Nunca ves el final. Su muerte es deducida, no confirmada.",
        "Y lo más triste: justo antes, Harrow descubre que Adler no mató a sus padres. Todo su odio venía de un error.",
    ]},
    {"id": "p08", "frases": [
        "Número ocho. Lev Kravchenko, el hombre que sobrevivió a sus propias granadas.",
        "Black Ops, dos mil diez. Misión Venganza, en Laos. Woods lo apuñala, Kravchenko tira de las granadas de su cinturón, y Woods se lanza con él por la ventana. Mason los da por muertos a los dos.",
        "Pero el cinturón se soltó en la caída, y explotó lejos. Los dos sobrevivieron, y Kravchenko se llevó a Woods preso a Vietnam.",
        "Su muerte de verdad llega en Black Ops 2, misión Viejas heridas, Afganistán, mil novecientos ochenta y seis. Lo interrogan en una cueva, suelta que Menéndez tiene gente dentro de la CIA, y Woods lo ejecuta.",
        "[deadpan] Dieciocho años después, Woods cobró la deuda en persona.",
    ]},
    {"id": "p07", "frases": [
        "En el siete, Phillip Graves.",
        "Modern Warfare 2, dos mil veintidós. El jefe de Shadow Company, el que traiciona a la Fuerza Operativa 141. Soap revienta el tanque desde el que los ataca, y todos lo dan por muerto.",
        "Graves nunca estuvo dentro del tanque. [short pause] Y sobrevive a todo Modern Warfare 3.",
        "Muere en Modern Warfare 4, en la misión Hired Gun, en París. Price derriba su helicóptero, Graves sale con una armadura, Price se la perfora y lo acorrala en un taller. Graves lo reta a disparar.",
        "Y si dudas más de dos segundos, Graves te quita el arma, y el que muere es Price. [deadpan] Aquí, dudar es perder la partida.",
    ]},
    {"id": "p06", "frases": [
        "Número seis. El ultranacionalista Imran Zakhaev, el que empezó todo.",
        "El villano de Call of Duty 4. En mil novecientos noventa y seis, en Prípiat, Price le vuela el brazo izquierdo con una Barrett, a casi novecientos metros. Y el brazo se queda tirado en el suelo el resto de la misión.",
        "Quince años después, en el puente de Fin del juego, Zakhaev ejecuta a Gaz. Price, herido, le desliza a Soap su M1911 por el suelo, y Soap acaba con él.",
        "Ahora, el detalle: ¿dónde le dio Soap? En la intro de Modern Warfare 2, en el torso. En el flashback de Modern Warfare 3, en la cabeza. [deadpan] La saga no se pone de acuerdo con su propio disparo.",
    ]},
    {"id": "p05", "post": 2.4, "frases": [
        "En el cinco, Nikita Dragovich.",
        "Black Ops. El general soviético de los números y del gas Nova 6. En Baikonur, el equipo destruye su limusina, y Woods jura que quedó hecho carbón. Pero Dragovich había fingido su muerte.",
        "Su final real es en Redención, en una estación de números bajo el mar. Mason le echa en cara que intentó obligarlo a matar a Kennedy. Y Dragovich responde con una sola palabra. Escucha.",
    ]},
    {"id": "p05b", "frases": [
        "¿Intentado? [short pause] Con esa palabra deja la duda de si Mason participó en el asesinato de Kennedy. Y Mason lo ahoga en el agua que sube.",
    ]},
    {"id": "p04", "frases": [
        "Número cuatro. El general Shepherd.",
        "Modern Warfare 2, dos mil nueve. El general que traicionó a la 141: mató a Ghost y a Roach, y le clavó un cuchillo en el pecho a Soap.",
        "Misión final, Fin de partida, en Afganistán. Price derriba su helicóptero, caen por una cascada, y Shepherd va a rematar a Soap con un Magnum, hasta que Price se le echa encima.",
        "Y mientras pelean, Soap se saca del pecho el cuchillo de Shepherd, y se lo lanza. Al ojo.",
        "Lo más amargo: Shepherd fue enterrado en Arlington como héroe de guerra, y Price y Soap quedaron como fugitivos. [deadpan] Y en el reinicio, Price lo vuelve a matar, de un tiro en la frente, en su propia oficina del Pentágono.",
    ]},
    {"id": "subs", "frases": [
        "Un dato antes del podio. De cada mil personas que ven estos expedientes, solo seis están suscritas al canal.",
        "Si llegaste hasta aquí, ya eres de la unidad. Suscríbete, y el siguiente expediente te llega a ti primero.",
    ]},
    {"id": "p03", "post": 3.2, "frases": [
        "En el tres, Raúl Menéndez.",
        "Black Ops 2, el villano de los tres finales. En Haití, Section le cae encima, lo apuñala y le apunta con su propia pistola. Menéndez le pide que lo convierta en mártir. Escucha.",
    ]},
    {"id": "p03b", "frases": [
        "Si lo matas, se activa un video grabado para su muerte, y Cordis Die incendia la Casa Blanca.",
        "Si lo capturas y Chloe vive, un año después Menéndez estrella la cabeza contra una tele. Y luego se ríe.",
        "Y si lo capturas y Chloe murió, escapa, mata a Woods con el colgante de su hermana, y se prende fuego sobre la tumba de Josefina. [short pause] En ese final, el villano se elimina a sí mismo. Y aun así gana.",
    ]},
    {"id": "p02", "post": 3.0, "frases": [
        "Número dos. El doctor Friedrich Steiner, y la muerte que el juego te contó al revés.",
        "Black Ops. El científico nazi del gas Nova 6, escondido en la isla Renacimiento. Jugando como Mason, ves a Reznov entrar en la sala y ejecutarlo.",
        "Pero luego juegas como Hudson. Y a través de un cristal blindado que no se rompe ni a balazos, ves la verdad: el que mata a Steiner es Mason. Gritando esto. Escucha.",
    ]},
    {"id": "p02b", "frases": [
        "Mi nombre es Viktor Reznov. Pero Reznov nunca estuvo ahí: llevaba cinco años muerto, desde Vorkuta. Y Hudson lo dice clarito: nunca estuvo aquí.",
        "Y FABIAN me escribió que no reconoce ninguno de mis efectos Mandela, que él lo recuerda todo tal como es.",
        "[short pause] Fabian, una pregunta: ¿quién mató a Steiner? [deadpan] Si tu respuesta fue Reznov, el juego te engañó. Y lo viste con tus propios ojos.",
    ]},
    {"id": "p01", "post": 1.8, "frases": [
        "Y el número uno. Vladimir Makarov. El villano que tuvo que morir dos veces.",
        "El original, en Modern Warfare 3, dos mil once. Hotel Oasis, Dubái. Makarov le quita a Price la Desert Eagle, y mata a Yuri delante de él.",
        "Price se le echa encima, le enrolla un cable dos veces al cuello, y los dos atraviesan el techo de cristal. Price cae. Makarov se queda colgado.",
        "Price enciende un puro, al tercer intento del encendedor. Y empiezan los créditos de la trilogía.",
        "Doce años después llega el reinicio. En Modern Warfare 3 de dos mil veintitrés, el nuevo Makarov mata a Soap, y escapa.",
        "Y muere en Modern Warfare 4, en la primera misión en orden cronológico: un callejón nevado de Nueva York. Sin armas. Price lo mata a puñetazos.",
        "Después, Laswell le pregunta dónde está Makarov. Escucha.",
    ]},
    {"id": "p01b", "frases": [
        "Fuera de la lista. [short pause] Dos Makarov, dos finales, y el mismo hombre cerrando el expediente: John Price.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. Veinte villanos, y casi ninguno murió como lo recuerdas.",
        "Todos los comentarios se leen, y se toman en cuenta para el siguiente expediente. Como el de Prophet, que encontró la entrevista donde el animador de Modern Warfare 3 cuenta que el hombre de la sombra era él mismo.",
        "O el de Daan, al que el cartel de Standoff le hizo wah. O el de almidon, que recuerda la misión de Chernóbil en cooperativo. Ese, para la parte tres de los efectos Mandela.",
        "Y v5x777 aclaró que la voz sonaba forzada en los momentos tristes. Tenías razón. Este expediente va sin drama.",
        "Ahora te toca a ti: ¿qué villano de Call of Duty merece su propio expediente? Escríbelo. Suscríbete. [short pause] Retírate, soldado.",
    ]},
]

# 17-nov: Whisper escribe distinto los nombres (Zakaev, Koch, Shepard, Rourke, Al-Assad, Cassie, Leucop, DeFert): textos revisados
CER_MAX_POR_FRASE = {k: .07 for k in ('p20_1', 'p19_0', 'p19b_0', 'p18_0', 'p18_3', 'p17_0', 'p15b_1', 'p14_0', 'p13_0', 'p12_0', 'p12_3', 'p12_4', 'p11_3', 'p10_4', 'p02b_2', 'p09_2', 'p07_0', 'p06_0', 'p06_1', 'p06_2', 'p04_0', 'p04_2', 'p04_3', 'p02_0')}
TAIL_MAX_POR_FRASE = {"p10_4": 1.1}   # termina bien («expediente entero»)
GAP_MAX_POR_FRASE = {}
