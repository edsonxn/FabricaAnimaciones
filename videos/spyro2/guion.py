# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Spyro 2: su historia y los 30 secretos QUE IGNORASTE» (30-oct-2026, ~24 min).
Pedido del usuario: video de 24 min de Spyro 2 de PSone. Elegido entre 3: historia + secretos. Variable que cambia respecto a
mario64_secretos: SOLO la consola (PS1 en vez de Nintendo). Motor SECUENCIA YT, voz ElevenLabs Hope, música = OST del juego (audio/ost,
armar_musica_ost.py), SFX del juego (sfx/sp_*.mp3), kit mg_spyro.
Datos: investigacion.md (sellos VERIFICADO/DUDOSO/TEORÍA y fuentes). Nombres de nivel en inglés: la tabla en español tiene una sola fuente.
NO decir: duración del desarrollo ni tamaño del equipo; 40 minijuegos; motivo de «Gateway to Glimmer»; Fairlight; mundo de primavera cortado;
primer papel de Kenny; fecha exacta de Europa; fecha del cumpleaños de Hunter; que la protección causó el fallo del PSN.
Verificado en imagen: verificacion_clips.md (30-oct). s21 y s11 cambiados de secreto; la moneda de s01 se ve en Jiggylookback qNBm6CYfAQs 65-74 s.
"""

TITULO = "Spyro 2: su historia y los 30 secretos QUE IGNORASTE"
ARCHIVO = "spyro2"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)
# ElevenLabs dice el inglés nativo; solo lo que leería mal
FONETICA = {}
# Falsas alarmas de Whisper (Spiro, Sparks, Idle Springs, 22-475): comparadas textos.json con eval.json el 31-oct
CER_MAX_POR_FRASE = {'s23_0': 0.056, 's02_5': 0.0255, 'intro_0': 0.0154, 'h1_4': 0.0682, 'h2_0': 0.0204, 'h3_1': 0.0197, 'h3_4': 0.0341, 'h3_6': 0.0261, 'h4_1': 0.0629,
                     'h4_4': 0.0163, 's30_1': 0.0211, 's25_0': 0.0259, 's23_1': 0.036, 's23_2': 0.0226, 's22_1': 0.0176, 's19_1': 0.015,
                     's19_3': 0.0226, 's17_3': 0.0154, 's15_1': 0.0301, 's14_2': 0.047, 's14_4': 0.0216, 's10_0': 0.0338, 's10_3': 0.0178,
                     's07_2': 0.2084, 's06_0': 0.04, 's06_4': 0.0218, 's04_2': 0.0186, 's04_4': 0.0515, 's02_2': 0.0372}
TAIL_MAX_POR_FRASE = {'s02_5': 0.75, 'intro_0': 0.45, 'h1_4': 0.67, 'h3_1': 0.92, 'h3_4': 0.78, 'h3_6': 0.9, 'h4_1': 0.99, 'h4_4': 0.92, 'h4_6': 1.01,
                      's30_1': 0.52, 's23_1': 0.44, 's23_2': 0.69, 's21_2': 1.04, 's19_1': 0.57, 's19_3': 0.68, 's17_3': 0.62,
                      's14_4': 1.09, 's10_3': 0.86, 's06_4': 0.75, 's04_2': 0.58, 's02_2': 0.42}
GAP_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    ambiente_por={'scene-008': 0.5, 'scene-015': 0.5, 'scene-016': 0.5, 'scene-017': 0.5, 'scene-022': 0.5, 'scene-023': 0.5, 'scene-044': 0.4, 'scene-045': 0.8, 'scene-046': 0.8, 'scene-054': 0.5, 'scene-055': 0.5, 'scene-056': 0.6, 'scene-057': 0.7, 'scene-058': 0.6, 'scene-059': 0.6, 'scene-060': 0.5, 'scene-061': 0.5, 'scene-062': 0.6, 'scene-073': 0.5, 'scene-074': 0.6, 'scene-075': 0.9, 'scene-076': 0.5, 'scene-077': 0.7, 'scene-091': 0.5, 'scene-092': 0.9, 'scene-093': 0.5, 'scene-094': 0.6, 'scene-100': 0.6, 'scene-101': 0.5, 'scene-102': 0.6, 'scene-103': 0.6, 'scene-105': 0.5, 'scene-124': 0.4, 'scene-126': 0.9, 'scene-127': 0.5, 'scene-128': 0.5, 'scene-129': 0.8, 'scene-130': 0.8, 'scene-131': 0.5},
    recorte_por={},
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora del juego (audio/ost, armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[whispers] En Spyro 2 hay una moneda dorada con la cara de un hombre real. Y casi nadie sabe quién es.",
        "[amused] Hay un monje que le pide a un dragón matar a un yeti, mientras el texto en pantalla dice otra cosa.",
        "[mysterious] Hay un libro de monstruos que nunca llegaron al juego, y solo se abre si superas todos los retos escondidos.",
        "[playful] Y dentro del disco había otro juego escondido. Bastaba con saber qué botones apretar.",
        "Spyro 2 salió en noviembre de 1999 en la primera PlayStation. Y veintisiete años después, sigue siendo para muchos el mejor de la saga.",
        "[excited] Hoy te cuento cómo se hizo, por qué el mismo juego tiene tres nombres distintos, y los 30 secretos que seguramente ignoraste.",
    ]},

    # ================================================================ HISTORIA
    {"id": "h1", "frases": [
        "[warm] Empecemos por el principio. Un estudio de Burbank, California, llamado Insomniac Games, y su fundador, Ted Price.",
        "En 1998 lanzaron Spyro the Dragon, un dragón morado pequeño, con mala actitud, en un mundo que parecía no terminarse nunca.",
        "[impressed] Eso venía de un motor de Alex Hastings que cambiaba el detalle de los objetos según la distancia. Lo cercano se veía nítido, y lo lejano se simplificaba sin que lo notaras.",
        "Era el juego perfecto para demostrar lo que podía hacer la PlayStation. Pero tenía un problema: casi todo consistía en recoger cosas.",
        "[curious] Según el documental de Reliable Rhubarb, la secuela empezó justo al terminar el primero. Se llamaba, simplemente, Spyro II.",
        "Y la meta la resumió Ted Price en una frase: más reto, más profundidad y más variedad.",
        "En el E3 de 1999 lo enseñaron al mundo. Ya no era un dragón que corría recogiendo gemas. Ahora tenía un mundo lleno de gente que le pedía favores.",
    ]},
    {"id": "h2", "frases": [
        "[playful] La historia arranca con un plan muy sencillo. Spyro y Sparx están hartos de la lluvia y quieren irse de vacaciones a Dragon Shores.",
        "[sarcastic] Se meten al portal y, claro, no llegan a la playa. Aparecen en Avalar, un mundo nuevo, invadido por un hechicero enano con muy mal carácter.",
        "Ese es Ripto. Y va acompañado de Crush y Gulp, dos criaturas enormes que parecen sacadas de un concurso de quién rompe más cosas.",
        "Lo que cambió fue todo lo demás. Ahora había tres mundos principales: Summer Forest, Autumn Plains y Winter Tundra.",
        "Cada nivel tiene un talismán y varias orbes. El talismán es la historia, y las orbes son retos aparte. Hay sesenta y cuatro orbes y diez mil gemas.",
        "[impressed] Spyro aprendió a nadar, a trepar escaleras y a dar cabezazos. Lo de nadar ya estaba planeado para el primer juego, pero se cayó por falta de tiempo.",
        "Y estaban los pilones. Cada enemigo derrotado suelta una partícula de espíritu, y al juntar las suficientes te dan un poder temporal: la supercarga, la supercongelación o el supervuelo.",
        "[mischievous] Hay fans con una teoría oscura sobre esto. Si las orbes y los pilones funcionan con los espíritus de criaturas derrotadas, entonces los buenos de Avalar tienen bastante que explicar.",
        "[amused] Y aparecieron Hunter, un guepardo que se cree más listo de lo que es, y Elora, una fauna que sí lo es.",
        "[sarcastic] También Moneybags, un oso que te cobra por pasar, por aprender y casi por respirar. La inflación hecha personaje.",
    ]},
    {"id": "h3", "frases": [
        "[warm] Y luego está lo que hace que este juego se sienta como se siente. La música.",
        "La compuso Stewart Copeland, el baterista de The Police. Fue uno de los primeros músicos de rock contratados para hacer un videojuego.",
        "[impressed] Y no se limitaba a mandar canciones. Le daban trucos para pasearse por cada nivel, lo jugaba, y componía sobre lo que sentía ahí.",
        "[thoughtful] Por eso cada nivel suena a un sitio. Summer Forest suena a verano, y Scorch suena a desierto, aunque Copeland nunca estuviera ahí.",
        "Oliver Wade, por su parte, montó las escenas de entrada y salida de cada nivel. Según el documental, sin storyboard.",
        "[amused] Cada nivel tiene su propio mini cuento. Pequeños dramas de gente rara con problemas absurdos, y tú llegas a arreglarlo a fuego.",
        "[impressed] Había otro truco de magia. El youtuber Shesez, de Boundary Break, sacó la cámara de su sitio y mostró cómo los portales disimulan la carga de cada nivel.",
        "[curious] Y según el mismo documental, hubo una cosa que no les dio tiempo de hacer: probar los minijuegos con jugadores de verdad. Ya vamos a llegar a eso.",
    ]},
    {"id": "h4", "frases": [
        "Spyro 2 salió el 2 de noviembre de 1999 en Estados Unidos, con el nombre de Ripto's Rage.",
        "[amused] Y aquí empieza lo raro. En Europa se llamó Gateway to Glimmer. En España, En busca de los talismanes. Y en Japón, Spyro equis Sparx: Tondemo Tours.",
        "[curious] ¿Por qué tantos nombres? Nadie lo tiene claro. He encontrado tres explicaciones, y no coinciden.",
        "Lo único seguro es que el cambio fue tardío. Una versión europea del 15 de septiembre todavía llevaba el logo de Ripto's Rage.",
        "[playful] Japón, además, se llevó un extra. Con la PocketStation, esa tarjeta de memoria con pantalla, podías desbloquear Sparx Adventure, un minijuego para criar a tu libélula.",
        "La crítica lo recibió muy bien. IGN le puso 8,8 y GameSpot 8,6. Y GameRankings lo dejó en un 87 por ciento.",
        "[impressed] Para diciembre de 1999 ya había vendido un millón de copias solo en Estados Unidos. Y con los años superó los tres millones cuatrocientos mil en todo el mundo.",
        "[playful] Pero lo mejor de este juego no está en las cifras. Está escondido. Así que vamos con los 30 secretos, del treinta al uno.",
    ]},

    # ================================================================ 30 SECRETOS (del 30 al 1)
    {"id": "s30", "frases": [
        "[curious] Número treinta. Dos niveles, una sola canción.",
        "Idol Springs y Fracture Hills están en mundos distintos y no se parecen en nada. Pero usan exactamente el mismo tema musical.",
        "[amused] Fíjate la próxima vez. El remake sí los separó con dos mezclas distintas. Se ve que alguien sí se dio cuenta.",
    ]},
    {"id": "s29", "frases": [
        "[playful] Número veintinueve. El dragón cabezón.",
        "Pausa el juego y aprieta arriba cuatro veces, R1 cuatro veces, y círculo.",
        "[laughs] Y a Spyro le sale una cabeza gigante. No sirve para nada, y por eso mismo es perfecto.",
    ]},
    {"id": "s28", "frases": [
        "[curious] Número veintiocho. El truco que ya estaba en el prototipo.",
        "Si en la pausa haces círculo cuatro veces y cuadrado, obtienes todas las habilidades del juego.",
        "[impressed] Y no parece un regalo para los jugadores. Ese mismo código ya estaba en el prototipo de agosto de 1999. En el de julio era otro: triángulo cuatro veces y círculo.",
        "[amused] Todo apunta a una herramienta del equipo que se quedó dentro. Ese prototipo incluso tenía un código para ver los créditos. Al usarlo, el juego se colgaba, porque los créditos todavía no existían.",
    ]},
    {"id": "s27", "frases": [
        "[sarcastic] Número veintisiete. Moneybags, traficante de armas.",
        "Todos recordamos a Moneybags cobrando por abrir portales y puentes. Lo que casi nadie lee es lo que dice mientras te cobra.",
        "[amused] En Autumn Plains, al abrirte el portal de Zephyr, se queja de que los pájaros de ahí nunca le pagaron las bombas y los barriles de TNT.",
        "[sarcastic] Eso es. El oso le vende explosivos a un bando de la guerra que tú vienes a resolver. Y más adelante, el propio Ripto presume de que lo convenció para venderle unas bombas.",
        "[amused] Y lo que gana lo tiene bien planeado. Habla de comprarse un condominio en Hurricos, dice que tiene casa en Aquaria Towers, y hasta quiere abrir un puesto de hamburguesas de lagarto en Skelos.",
        "Tampoco es que lo disimule. Al abrirte el portal de Shady Oasis se despide diciendo: salúdame a Ripto si lo ves.",
    ]},
    {"id": "s26", "frases": [
        "[playful] Número veintiséis. El hockey nació en la oficina.",
        "En Colossus, un monje te reta a un hockey uno contra uno: cinco goles antes que un patinador rojo. Y eso no estaba en el diseño original del nivel.",
        "[amused] Salió de los partidos de hockey que jugaba el propio equipo. Les gustó tanto que acabó dentro del juego.",
    ]},
    {"id": "s25", "frases": [
        "[curious] Número veinticinco. Elora, la centauro que no cupo.",
        "Según lo que contó Oliver Wade, Elora se iba a diseñar como una centauro. Pero un cuerpo de caballo pedía demasiados polígonos.",
        "[amused] Así que se quedó en fauna, con dos patas. Y su nombre salió de reordenar letras de Caroline, por Carolina Trujillo, del equipo de Insomniac.",
    ]},
    {"id": "s24", "frases": [
        "[amused] Número veinticuatro. Las alas mal puestas.",
        "En el primer juego, las alas de Spyro estaban mal hechas. Las costillas le salían de donde no debían.",
        "[impressed] Craig Stitt, uno de sus artistas, las corrigió para esta secuela. Sí, alguien se puso a estudiar la anatomía de un dragón morado que no existe.",
    ]},
    {"id": "s23", "frases": [
        "[surprised] Número veintitrés. Bob Esponja hace de Spyro.",
        "En este juego cambió la voz del protagonista. Sale Carlos Alazraqui, y entra Tom Kenny, la voz de Bob Esponja.",
        "[amused] Y según la wiki de la saga, también hace al Profesor y a los Electrolls de Hurricos. Los créditos no dicen quién es quién, pero escúchalos bien, porque el parecido es sospechoso.",
    ]},
    {"id": "s22", "frases": [
        "[curious] Número veintidós. Un solo actor para los dos bandos.",
        "Según esa misma wiki, Gregg Berger pone la voz de Ripto, y también la de Hunter.",
        "[amused] O sea que, cuando el villano y tu aliado discuten, es un solo señor hablando consigo mismo. Una especie de terapia con presupuesto de Sony.",
    ]},
    {"id": "s21", "frases": [
        "[sarcastic] Número veintiuno. El almuerzo de Gulp.",
        "En la primera cinemática, Gulp se traga el cetro de Ripto. Lo ves pasar. Y Ripto le grita: imbécil, te comiste mi cetro.",
        "[amused] Y ahí está el detalle que nadie mira. Cuando vuelves a verlo, en la escena en que le da de comer a Gulp, Ripto ya no lleva cetro. Y solo después de vencer a Gulp dice: esto es justo lo que necesito para un cetro nuevo. El juego no se olvidó.",
    ]},
    {"id": "s20", "frases": [
        "[curious] Número veinte. La cantante que Europa nunca oyó.",
        "En Ripto's Arena, la versión americana lleva una voz de ópera sobre la música.",
        "[short pause] Y en la versión europea, la quitaron. Escucha la diferencia.",
        "[thoughtful] Es, según el canal Calcom, el único nivel del juego con música distinta entre las dos regiones. Y no he encontrado ninguna explicación oficial.",
    ]},
    {"id": "s19", "frases": [
        "[playful] Número diecinueve. La música de las demos.",
        "Sunny Beach y Skelos Badlands tienen una versión más larga, que sonaba en la demo del juego.",
        "[warm] Es un regalo para los oídos que casi nadie escuchó, porque el juego final la recortó.",
        "[curious] Y los prototipos guardan más. Hay temas de minijuegos que nunca se usaron, para Skelos Badlands, Sunny Beach y Hurricos, y una versión temprana de la música de Crystal Glacier.",
    ]},
    {"id": "s18", "frases": [
        "[laughs] Número dieciocho. Los jinetes amish de delfines.",
        "Sí, leíste bien. Chad Dezern contó en el documental que en Aquaria Towers iba a haber jinetes amish montados en delfines.",
        "[amused] Se quedaron en caballitos de mar, que en comparación son lo más normal del mundo.",
        "Y la parte de arriba del nivel venía de un mundo submarino pensado para el primer Spyro. Nada se tira, todo se reutiliza.",
    ]},
    {"id": "s17", "frases": [
        "[amused] Número diecisiete. El volcán de papel.",
        "Según contó Michael John, Magma Cone se presentó en papel cuadriculado, con un volcán hecho de papel.",
        "[warm] Así se hacían los niveles en 1999. Con tijeras y mucha imaginación.",
        "Skelos Badlands, por cierto, fue el primer nivel creado para el juego. Lo hizo Craig Stitt.",
    ]},
    {"id": "s16", "frases": [
        "[tense] Número dieciséis. Los problemas con la vagoneta.",
        "Todos los que jugaron esto lo saben. Breeze Harbor, cincuenta engranajes, y una vagoneta que no perdona.",
        "[sarcastic] Y si vuelves a hablarle a Fisher, el que te mandó ahí, te suelta: Trouble with the trolley, eh? ¿Problemas con la vagoneta? Como si no lo supiera.",
        "[curious] Según el documental, pudo salir así de cruel por ser una adición de última hora. Y porque nunca se probó con usuarios.",
        "[amused] Si de niño lloraste aquí, no eras malo. Es que nadie lo probó antes que tú.",
    ]},
    {"id": "s15", "frases": [
        "[curious] Número quince. Los niveles se llamaban de otra forma.",
        "Durante el desarrollo, Glimmer se llamó Sparkle, e Idol Springs fue Colossus Springs.",
        "[impressed] Sunny Beach era Aquaria Beach. Breeze Harbor, Zephyr Harbor. Y Cloud Temples, Mystic City.",
        "Iban por parejas, para que dos niveles sonaran del mismo sitio. Scorch Dunes y Scorch Oasis. Metropolis Acres y Metropolis Spires. Luego alguien decidió separarlos, y los nombres cambiaron casi todos.",
    ]},
    {"id": "s14", "frases": [
        "[mischievous] Número catorce. El nombre que se les olvidó cambiar.",
        "Lo mejor es que dejaron restos en el juego final. En Zephyr, el soldado Romeo, al reunirse con Juliet, habla de irse de luna de miel a Colossus Springs.",
        "[amused] Ese lugar no existe. Es el nombre viejo de Idol Springs.",
        "Y en Cloud Temples, el mago Murgen te da un recuerdo de la tienda de regalos de Mystic City, el nombre viejo de ese nivel.",
        "[playful] Hasta en Crystal Glacier, Widgie, un constructor de hielo, dice que su jefe tiene las entradas para el hockey de Colossus Valley. Sí, otra vez Colossus. Y tú ibas ahí, sin enterarte de nada.",
    ]},
    {"id": "s13", "frases": [
        "[laughs] Número trece. Lo dejamos listo para noviembre.",
        "Según Hidden Palace, en el prototipo de julio de 1999, Moneybags le dice al jugador que Canyon Speedway sigue en obras y debería estar listo para noviembre.",
        "[amused] El oso hablándote como un jefe de obra. Y el juego salía justo en noviembre.",
        "En esa versión, varios niveles de Winter Tundra ni siquiera tenían salida. Y el juego te decía: usa el menú de pausa si quieres irte.",
    ]},
    {"id": "s12", "frases": [
        "[curious] Número doce. Las gemas que no daban la cuenta.",
        "El juego final tiene diez mil gemas exactas. Pero el prototipo de agosto, según Hidden Palace, tenía nueve mil novecientas noventa y una.",
        "[impressed] Zephyr traía una de más, y a Robotica Farms le faltaban varias. Y había sesenta y cinco orbes en lugar de sesenta y cuatro.",
        "[amused] Hasta el 100 % de un juego es algo que alguien tuvo que cuadrar a mano.",
    ]},
    {"id": "s11", "frases": [
        "[surprised] Número once. El juego sin final.",
        "En el prototipo de julio de 1999, Ripto's Arena ni siquiera existía. A cuatro meses de salir, el juego no tenía su último nivel.",
        "En esa misma versión, el marcador del hockey usaba discos rojos y azules en lugar de las cabezas. Y en Summer Forest, el que te explicaba la cámara era el Profesor, un trabajo que luego se quedó Hunter.",
    ]},
    {"id": "s10", "frases": [
        "[mysterious] Número diez. Elora iba a contarlo todo.",
        "En el prototipo de agosto de 1999, las escenas de los niveles llevan un diálogo extra. Elora le explica a Spyro qué pasa en cada sitio.",
        "[impressed] Cada lugar tenía su historia completa, con voz.",
        "Hurricos, por ejemplo, era el hogar de los Electrolls, los científicos que dan energía a Avalar, hasta que Ripto mandó robarla. Y los Water Workers de Aquaria Towers vaciaron unas cuevas y levantaron fábricas encima del coral.",
        "[amused] También te aclaraba que lo que hacen los caballitos de mar es asustarse unos a otros hasta sacarse las burbujas. Un dato vital que nos perdimos.",
        "[thoughtful] Y todo eso se borró. Ese diálogo no existe en la versión que jugaste.",
    ]},
    {"id": "s09", "frases": [
        "[curious] Número nueve. La guerra que empezó Ripto.",
        "En Breeze Harbor y Zephyr, dos pueblos se acusan de haber empezado la guerra: los Land Blubbers y los Breeze Builders.",
        "[amused] Y tú ayudas a los dos, porque Spyro es el mercenario más honesto de Avalar.",
        "[thoughtful] En el juego final parece una pelea sin villano. Pero ese diálogo cortado de Elora lo explica. Se llevaban bien hasta que llegó Ripto, y ella sospecha que los enfrentó para conquistar Avalar con menos trabajo.",
    ]},
    {"id": "s08", "frases": [
        "[amused] Número ocho. Kill the yeti.",
        "En Colossus, un monje, Brother Ned, te pide que te ocupes del yeti. Si lees el cuadro de texto, dice: torch, quémalo.",
        "[mischievous] Pero escucha lo que dice en voz alta.",
        "[laughs] Dice kill, mátalo. Un monje vegetariano, por cierto, porque lo aclara. El audio y el texto no coinciden, y todo apunta a una censura a medias.",
    ]},
    {"id": "s07", "frases": [
        "[curious] Número siete. El cumpleaños de Hunter.",
        "Antes de la mazmorra de Crush, una cinemática cuenta cómo llegó Ripto. El Profesor estaba probando su superportal, y solo le faltaban unas coordenadas.",
        "[amused] Y Hunter suelta: ¿qué tal veintidós, cuatro, siete, cinco? Es mi cumpleaños.",
        "[sarcastic] El Profesor intentó pararlo, pero ya era tarde. Por ese portal entró Ripto. Una guerra entera por usar tu cumpleaños como clave. Nunca nadie ha explicado mejor la seguridad informática.",
    ]},
    {"id": "s06", "frases": [
        "[impressed] Número seis. Ripto sale de Spyro.",
        "El logo japonés del juego dice Spyro en katakana. Los artistas lo miraban y les parecía que decía, en letras latinas, Ripto.",
        "[amused] Y así se quedó. El gran enemigo de Spyro es, literalmente, su propio nombre mal leído.",
        "Lo publicó la revista oficial de PlayStation en 1999. Y aquí está el logo, por si quieres intentar leerlo.",
        "[curious] Wade, según el documental, lo dibujó pequeño a propósito, para que contrastara con el enorme Gnasty Gnorc del primer juego. Y lo sacó casi a la primera, con un solo cuernito en la cabeza.",
    ]},
    {"id": "s05", "frases": [
        "[excited] Número cinco. El salto que nadie programó.",
        "Salta, y justo en lo más alto, aprieta cuadrado. Si lo haces en el momento exacto, Spyro se eleva todavía más.",
        "[impressed] Es el glitch del doble salto. Con él cruzas el puente de Glimmer sin pagarle a Moneybags, que es lo más satisfactorio de todo el juego.",
        "[mischievous] Y con práctica te saltas casi todo el nivel, sin saludar a nadie.",
        "No funciona ni en el primer juego ni en el tercero, así que es exclusivo de este. Muy pocos errores se sienten tan parecidos a una venganza.",
    ]},
    {"id": "s04", "frases": [
        "[tense] Número cuatro. Los dos niveles malditos.",
        "La versión europea llevaba una protección anticopia llamada LibCrypt.",
        "[mysterious] Según el documental, con una copia pirata el juego funcionaba bien hasta entrar a Colossus o a Idol Springs. Ahí la pantalla se quedaba en negro.",
        "[curious] Ahora viene lo raro. En 2007 el juego salió en la PlayStation Network europea, y lo retiraron en menos de una semana.",
        "¿Por qué? Porque había dos niveles que no cargaban. [short pause] Colossus e Idol Springs.",
        "[thoughtful] Nadie ha confirmado que las dos cosas estén relacionadas, así que esto es solo una coincidencia muy sospechosa. En 2012 volvió, ya con la versión americana.",
    ]},
    {"id": "s03", "frases": [
        "[excited] Número tres. Crash escondido dentro de Spyro.",
        "Cuando sale la pantalla de inicio, mantén L1 y R2, y aprieta cuadrado.",
        "[surprised] Se abre una demo de Crash Team Racing, con la pista Papu's Pyramid.",
        "[impressed] Y al revés también. Crash Team Racing esconde una demo de Spyro 2, con Colossus y Magma Cone, y un aviso: a la venta en noviembre de 1999.",
        "[playful] Las dos mascotas de PlayStation, cada una dentro del disco de la otra. Y en aquella época, sin internet, solo lo sabías si alguien te lo contaba en el recreo.",
    ]},
    {"id": "s02", "frases": [
        "[mysterious] Número dos. El libro de los monstruos que nunca existieron.",
        "El juego tiene dieciséis puntos de habilidad escondidos, y nunca te dice dónde están.",
        "Aterrizar en un ídolo en Idol Springs. Todos los molinos de Hurricos. Golpear a Ripto en Gulp's Overlook.",
        "[impressed] Si juntas suficientes, se abren los epílogos en la guía. Son pequeñas historias de lo que pasó después con cada personaje. Gulp, por ejemplo, acaba en un zoológico para monstruos maltratados.",
        "Y si los juntas todos, llega un libro: Faunus Mortas. Un catálogo de diez criaturas extintas de Avalar, escrito por Basil el Explorador.",
        "[curious] Son enemigos que se quedaron fuera del juego. Un gato con orejas de murciélago, un robot con pala, un armadillo azul, un troll con un puño de piedra llamado Mister Fistus, y una cosita con orejas grandes llamada Wuss.",
        "[warm] Los dejaron ahí, como una tumba cariñosa para los diseños que no sobrevivieron.",
    ]},
    {"id": "s01", "frases": [
        "[soft] Número uno. La cara de la moneda.",
        "En Mystic Marsh, el Profesor pierde su lápiz, y te toca hacer una cadena de cambios absurda. Un huevo por una semilla, la semilla por un patito de goma, el patito por un nabo, y el nabo por una moneda dorada.",
        "[whispers] Si acercas la cámara a esa moneda, verás una cara en relieve. No es de ningún personaje.",
        "[warm] Es Dan Johnson, de Insomniac Games. Sus compañeros lo metieron en el juego como una broma interna.",
        "Y la broma siguió. Su cara volvió a aparecer en Spyro 3, en carteles de Se busca, y luego en Ratchet & Clank.",
        "[sad] Dan Johnson murió en diciembre de 2006, con treinta y dos años. Ratchet & Clank: Size Matters se le dedicó.",
        "[thoughtful] El remake cambió esa cara por otro símbolo. Así que, si quieres verlo a él, tienes que volver a esta versión.",
        "[soft] Veintisiete años después, todavía hay gente que se acerca a esa moneda. No por el talismán. Por él.",
    ]},

    # ================================================================ CIERRE
    {"id": "cierre", "frases": [
        "[warm] Spyro 2 sigue vivo. En 2018 volvió con Reignited Trilogy, y Toys for Bob lo rehízo casi a ciegas, porque Insomniac ya no pudo darle ni el código ni los archivos originales.",
        "[impressed] Tuvieron que crear una herramienta propia, Spyro-scope, para mirar la geometría de los juegos de PlayStation y copiarla con cuidado. Y aun así, varios de los secretos que acabas de ver se perdieron por el camino.",
        "[excited] Y en junio de este año llegó la noticia. Spyro: A Realm Beyond, el primer juego completamente nuevo de la saga en dieciocho años, previsto para la primavera de 2027.",
        "Tom Kenny vuelve a ser Spyro. [short pause] Pero Stewart Copeland ya confirmó que él no estará. Así que parte de esa magia se queda aquí, en 1999.",
        "[playful] Ahora dime tú. ¿Pudiste con la vagoneta, o la dejaste para siempre? Te leo en los comentarios, porque leemos todos y nos sirven para mejorar.",
        "[warm] Y si te gustó este viaje, suscríbete a Crónicas del gaming. Nos vemos en el siguiente video. Y págale a Moneybags, antes de que te lo cobre él.",
    ]},
]
