# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Super Mario 64: su historia y los 20 secretos QUE IGNORASTE» (~22 min; 29-oct-2026).
Tema elegido por el usuario entre 3 propuestas con datos (`fab.py ideas cronicas_gaming`): «Nintendo BORRÓ esta estrella de
Mario 64» ×3,5 (Nachotaro), «¿Por qué Nintendo desapareció a Mario 2D?» ×3,7 (canal de 2 590 subs). Variable que cambia
respecto a zelda_oot / majora_mask: SOLO el juego (el clásico de N64 más buscado); misma fórmula historia + N secretos.
Voz Hope (`eleven_v4_turbo`). Música = banda sonora OFICIAL de Mario 64 (armar_musica_ost.py; regla del 23-oct).

Datos verificados el 29-oct-2026 (fuentes completas en fuentes_guion.md, F#):
- Gancho: oct-2026, Mochi64 «resuelve» la placa del patio: «Eternal Star / We hope so» (VGC, Time Extension, TechSpot,
  Dexerto; ~530 fuentes probadas, Palatino Bold Italic). NO es confirmación de Nintendo. Nintendo no hizo nada por los 30 años.
- Japón 23-jun-1996, EE. UU. 29-sep-1996, Europa 1-mar-1997. >2 M en 3 meses en Norteamérica; 11,89 M (Guinness).
- Iwata Asks: «Yo dirijo este» y el nado a las 2-3 de la madrugada (F25); Luigi «con lágrimas» (F27); pantalla dividida (F26).
- Shoshinkai 24-26-nov-1995 al 50 %; 32 niveles planeados -> 15 (F37). 622 días (F32). Kondo ~8 meses (F39).
- TTC: 12 detenido, 3 lento, 6 al azar, 9 rápido (Super Mario Wiki, comprobado por mí).
- Suigi 120 estrellas 1:35:14 (26-abr-2026, speedrun.com); bolsa ~10 000 US$.
- DISCUTIDO se dice como tal: el rayo cósmico (hipótesis), las pelotas de ping-pong de Goddard, la placa (estadística).
"""

TITULO = "Super Mario 64: su historia y los 20 secretos QUE IGNORASTE"
ARCHIVO = "mario64_secretos"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)

# ElevenLabs dice el inglés nativo; solo lo que una voz en español leería mal
FONETICA = {"pannenkoek": "pánenkuk", "Shindou": "Shíndou", "Suigi": "Suígui", "Mochi64": "Mochi sesenta y cuatro"}
# Revisado el 29-oct leyendo voz/eval.json: Whisper escribe «brasa», «Waiko Izumi», «Docs», «Martinette», «Shindle», «Swiggy»,
# «DotaTbag», «TikTok Clock», «Panacook», «Ella es real» (L is real): falsas alarmas de nombres.
CER_MAX_POR_FRASE = {"h1_8": 0.03, "h2_9": 0.03, "s15_1": 0.02, "s10_3": 0.03, "s09_2": 0.02, "s08_4": 0.02, "s04_4": 0.02,
                     "s04_6": 0.04, "s02_1": 0.04, "s02_3": 0.08, "s01_8": 0.05}
TAIL_MAX_POR_FRASE = {"s10_2": 1.2, "s04_6": 1.2}
GAP_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    ambiente_por={'scene-004': 0.7, 'scene-020': 0.7, 'scene-048': 0.6, 'scene-049': 0.6, 'scene-066': 0.8, 'scene-077': 0.8, 'scene-078': 0.7, 'scene-080': 0.8, 'scene-099': 0.6, 'scene-101': 0.8, 'scene-103': 0.8, 'scene-107': 0.6, 'scene-145': 0.7},
    recorte_por={'scene-001': 0.131, 'scene-004': 0.125, 'scene-006': 0.131, 'scene-007': 0.131, 'scene-009': 0.131, 'scene-010': 0.131, 'scene-011': 0.131, 'scene-014': 0.131, 'scene-015': 0.125, 'scene-016': 0.125, 'scene-017': 0.131, 'scene-018': 0.131, 'scene-019': 0.131, 'scene-020': 0.131, 'scene-021': 0.131, 'scene-022': 0.131, 'scene-023': 0.131, 'scene-024': 0.131, 'scene-025': 0.131, 'scene-026': 0.131, 'scene-027': 0.125, 'scene-028': 0.125, 'scene-029': 0.131, 'scene-030': 0.131, 'scene-036': 0.131, 'scene-037': 0.131, 'scene-039': 0.131, 'scene-042': 0.125, 'scene-043': 0.131, 'scene-044': 0.131, 'scene-045': 0.125, 'scene-046': 0.131, 'scene-047': 0.131, 'scene-048': 0.125, 'scene-049': 0.131, 'scene-050': 0.131, 'scene-051': 0.131, 'scene-052': 0.131, 'scene-053': 0.125, 'scene-054': 0.131, 'scene-055': 0.125, 'scene-056': 0.125, 'scene-057': 0.131, 'scene-058': 0.125, 'scene-059': 0.125, 'scene-060': 0.131, 'scene-061': 0.131, 'scene-062': 0.131, 'scene-063': 0.131, 'scene-064': 0.131, 'scene-065': 0.131, 'scene-066': 0.131, 'scene-067': 0.131, 'scene-068': 0.131, 'scene-069': 0.131, 'scene-070': 0.125, 'scene-071': 0.125, 'scene-072': 0.125, 'scene-074': 0.131, 'scene-076': 0.131, 'scene-077': 0.131, 'scene-078': 0.131, 'scene-079': 0.131, 'scene-080': 0.125, 'scene-081': 0.125, 'scene-082': 0.131, 'scene-083': 0.131, 'scene-084': 0.131, 'scene-085': 0.131, 'scene-088': 0.125, 'scene-090': 0.131, 'scene-091': 0.131, 'scene-092': 0.131, 'scene-093': 0.131, 'scene-094': 0.131, 'scene-095': 0.131, 'scene-096': 0.131, 'scene-097': 0.131, 'scene-098': 0.131, 'scene-099': 0.125, 'scene-100': 0.125, 'scene-101': 0.131, 'scene-103': 0.131, 'scene-104': 0.125, 'scene-107': 0.131, 'scene-109': 0.125, 'scene-110': 0.125, 'scene-111': 0.125, 'scene-116': 0.125, 'scene-127': 0.131, 'scene-134': 0.131, 'scene-139': 0.131, 'scene-141': 0.131, 'scene-143': 0.131, 'scene-144': 0.131, 'scene-145': 0.131, 'scene-146': 0.131, 'scene-147': 0.131, 'scene-148': 0.125, 'scene-149': 0.125},
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: la música es la banda sonora OFICIAL de Super Mario 64 (armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[mysterious] En el patio del castillo de Peach hay una estatua con una placa que nadie ha podido leer en treinta años.",
        "[whispers] Durante décadas, media generación juró que decía: L is real, 2401. [short pause] Y que Luigi estaba escondido en el juego.",
        "[excited] Este mes de octubre, un programador comparó millones de combinaciones de letras contra esos pocos píxeles. Y encontró una respuesta.",
        "[curious] Te la cuento al final, porque esa placa esconde mucho más de lo que parece.",
        "Super Mario 64 cumplió treinta años en 2026. Salió en Japón el 23 de junio de 1996, el mismo día que la Nintendo 64.",
        "[impressed] Y cambió los videojuegos para siempre. Marcó cómo se iba a mover todo un género en tres dimensiones.",
        "Hoy te cuento cómo se hizo, por qué casi no llega a tiempo, y los 20 secretos que seguramente ignoraste.",
        "[playful] Desde un conejo con nombre de procesador, hasta un rayo cósmico que, según algunos, cambió un solo bit del juego.",
    ]},
    {"id": "h1", "frases": [
        "[warm] Empecemos por el principio. [short pause] Un Mario en tres dimensiones.",
        "Shigeru Miyamoto ya pensaba en eso mientras su equipo hacía Star Fox, en 1993, para la Super Nintendo.",
        "[playful] Y aquí hay un mito que conviene aclarar. Mucha gente cree que existió un juego cancelado llamado Super Mario FX.",
        "Pero Dylan Cuthbert, programador de Star Fox, explicó que Super Mario FX era el nombre interno del chip de la consola. No hay pruebas de ese juego.",
        "El primer prototipo real fue mucho más sencillo. Un cuarto con bloques, donde Mario y Luigi corrían, trepaban y saltaban, para probar un mando nuevo.",
        "[amused] Yoshiaki Koizumi recuerda que un día Miyamoto llegó y dijo: este lo dirijo yo. Llevaba años sin dirigir un juego.",
        "Y lo dirigió a su manera. Casi sin documentos, explicando las cosas en persona.",
        "[laughs] Koizumi cuenta que, a las dos o tres de la madrugada, con el equipo ya en casa, Miyamoto se tiró sobre un escritorio para enseñarle cómo tenía que nadar Mario.",
        "No era ni braza ni crol. Era, en sus palabras, algo así.",
        "[curious] También quería que Mario corriera con peso, como Arale, el personaje de Akira Toriyama. Y los programadores admitieron que la física no era real. La ajustaron a mano hasta que se sintiera bien.",
        "Según un documento de copyright que se filtró en 2020, la creación del juego duró 622 días, del 7 de septiembre de 1994 al 20 de mayo de 1996.",
        "[thoughtful] Lo hizo un equipo de unas quince o veinte personas. Y el compositor Koji Kondo tardó unos ocho meses en la música, peleando siempre contra los límites de memoria.",
    ]},
    {"id": "h2", "frases": [
        "[serious] Pero un Mario en 3D tenía un problema. [short pause] ¿Cómo lo controlas?",
        "La cruceta solo tiene ocho direcciones. Para moverse en un mundo abierto hacía falta otra cosa.",
        "El mando de la Nintendo 64 se diseñó a la vez que las mecánicas de Mario 64, y Miyamoto lo probaba con el propio juego. Su primera maqueta fue de arcilla.",
        "[impressed] Y en el centro, la pieza clave. Un stick analógico que reconoce el movimiento en 360 grados.",
        "Con él, Mario podía caminar de puntillas, trotar o correr, según cuánto inclinaras el pulgar.",
        "Luego estaba la cámara. En un juego en 3D, alguien tiene que decidir desde dónde se ve todo.",
        "[playful] Y Nintendo le dio una explicación dentro del juego. La cámara la llevan los hermanos Lakitu, que filman a Mario en directo, como un equipo de televisión.",
        "[amused] Aun así, es lo más criticado del juego. Pero en 1996 nadie había resuelto ese problema.",
        "[curious] Incluso el castillo tiene historia. Miyamoto contó que ese sistema de un mundo central lo pensó primero para Zelda.",
        "Y Koizumi reveló que probaron la bandera de meta de los Mario en 2D. Pero en 3D lo divertido era explorar, así que cambiaron la bandera por estrellas.",
    ]},
    {"id": "h3", "frases": [
        "[excited] En noviembre de 1995, Nintendo enseñó el juego por primera vez, en la feria Shoshinkai de Tokio.",
        "Estaba más o menos al cincuenta por ciento. Y había 32 niveles planeados. [short pause] Al final quedaron quince.",
        "[curious] En esa demo, la vida se medía con un indicador distinto, las monedas eran las de Super Mario World, y el cielo era de un solo color.",
        "[amused] Y la gente que lo probó decía que el control se sentía tembloroso y resbaladizo. Miyamoto lo admitió: fue un reto enorme.",
        "La Nintendo 64 se retrasó de la Navidad de 1995 al año siguiente. Y según Howard Lincoln, de Nintendo of America, en buena parte fue porque Miyamoto quería más contenido.",
        "[excited] Super Mario 64 salió en Japón el 23 de junio de 1996. En Estados Unidos, el 29 de septiembre. Y en Europa, hasta marzo de 1997.",
        "Solo en Norteamérica vendió más de dos millones de copias en sus tres primeros meses.",
        "[impressed] En total, casi doce millones. Según Guinness, es el juego más vendido de toda su generación de consolas.",
        "En 1997 salió en Japón una versión nueva, la Shindou, con vibración y errores corregidos. Y en 2004, un remake para la Nintendo DS.",
        "En 2020 volvió en Super Mario 3D All-Stars para Switch, y hoy se puede jugar en Nintendo Switch Online.",
        "[sighs] Pero para sus treinta años, Nintendo no anunció nada. Ni un remake, ni una reedición.",
        "[playful] Así que los fans lo celebraron a su manera. En 2026 lo hicieron correr en una 3DO, en una 3DS, y hasta hicieron una versión para una Super Nintendo real, con el chip Super FX.",
        "[warm] Y ahora sí, vamos con los veinte secretos. Del menos sorprendente, al que te va a volar la cabeza.",
    ]},
    {"id": "s20", "frases": [
        "[curious] Número veinte. El conejo con nombre de máquina.",
        "En el sótano del castillo vive un conejo amarillo que se escapa cuando intentas atraparlo. Se llama MIPS.",
        "[impressed] Y no es un nombre al azar. MIPS es la arquitectura del procesador de la propia Nintendo 64.",
        "[playful] O sea, que cada vez que perseguías a ese conejo, estabas persiguiendo, literalmente, al cerebro de la consola. Y si lo atrapas, te da una estrella.",
    ]},
    {"id": "s19", "frases": [
        "[curious] Número diecinueve. La cámara tiene nombre y apellido.",
        "Al empezar el juego, un Lakitu con una cámara colgando de su caña te saluda frente al castillo.",
        "[amused] Y te explica que él y su hermano van a grabar toda tu aventura, como si fuera un reportaje en vivo.",
        "Si te miras en un espejo del castillo, lo puedes ver ahí, siguiéndote. [short pause] El camarógrafo más paciente de la historia.",
    ]},
    {"id": "s18", "frases": [
        "[tense] Número dieciocho. La estrella en la cola.",
        "En Jolly Roger Bay, la Bahía del Capitán, vive una anguila enorme escondida en el fondo del mar.",
        "En la segunda misión tienes que hacerla salir de su cueva. [short pause] Y la estrella no está en ningún cofre.",
        "[impressed] Brilla en la punta de su cola. Tienes que nadar detrás de ella y tocarla mientras se mueve.",
        "[playful] Es una de esas estrellas que muchos niños tardaron semanas en descubrir, solo porque no se les ocurrió mirarle la cola a un monstruo.",
    ]},
    {"id": "s17", "frases": [
        "[warm] Número diecisiete. El pingüino que no es tuyo.",
        "En Cool, Cool Mountain, la Montaña Helada, una mamá pingüino te pide que encuentres a su bebé perdido.",
        "[curious] Pero en el nivel hay otro pingüino bebé muy parecido. Y si le llevas ese, la mamá se da cuenta de inmediato.",
        "[sad] Y te dice que no es su hijo, y que sus papás deben estar preocupados por él.",
        "[playful] Y si después de recibir la estrella vuelves a cargar a su bebé, la mamá te persigue por la montaña. Nintendo pensó en todo.",
    ]},
    {"id": "s16", "frases": [
        "[mysterious] Número dieciséis. Los secretos bajo el agua.",
        "Durante años circuló el rumor de un castillo secreto escondido bajo el agua. [short pause] Ese castillo no existe.",
        "Lo que sí existe es el Acuario Secreto. Se entra por un hueco en la pared, a la derecha del cuadro de Jolly Roger Bay, y casi nadie lo ve.",
        "[impressed] Y hay más. En el sótano, si golpeas el suelo sobre dos pilares, el agua del foso del castillo se vacía.",
        "Abajo aparece la entrada a un nivel escondido, donde consigues el gorro de invisibilidad.",
    ]},
    {"id": "s15", "frases": [
        "[warm] Número quince. La música que te sigue.",
        "Dire, Dire Docks es probablemente la canción más querida del juego. Y tiene un truco.",
        "[impressed] No suena igual en todo el nivel. A medida que avanzas por el agua, se van sumando instrumentos. Primero sintetizadores, y luego la percusión.",
        "El mismo tema y el mismo sistema se usan también en Jolly Roger Bay y en el Acuario Secreto.",
        "[thoughtful] Koji Kondo hizo que la música reaccionara a dónde estás. En 1996, eso era casi magia.",
    ]},
    {"id": "s14", "frases": [
        "[ominous] Número catorce. El cuadro que te mira.",
        "Cuando abres la puerta de ocho estrellas, al fondo de un pasillo hay un retrato de la princesa Peach.",
        "[tense] Pero cuando te acercas, la cara de Peach se transforma en la de Bowser. [short pause] Y el suelo se abre bajo tus pies.",
        "Caes directo a Bowser in the Dark World. Y el cuadro, en realidad, nunca se puede tocar. Hay una pared invisible delante.",
        "[playful] Para un niño de 1996, era el susto de su vida. Para Nintendo, era una forma elegante de decir: Peach no está aquí.",
    ]},
    {"id": "s13", "frases": [
        "[excited] Número trece. El premio de las 120 estrellas.",
        "Si consigues las 120 estrellas del juego, el cañón del jardín por fin te deja subir al tejado del castillo.",
        "[warm] Y ahí te espera Yoshi, el compañero de Super Mario World.",
        "Te da un mensaje del equipo de desarrollo, te regala cien vidas, y te enseña un triple salto mejorado, que deja una estela de destellos.",
        "[amused] Cien vidas, cuando ya no te queda nada que hacer. [short pause] Pero oye, el gesto es lo que cuenta.",
    ]},
    {"id": "s12", "frases": [
        "[playful] Número doce. La frase que todos oímos mal.",
        "Cuando Mario lanza a Bowser, dice una frase en inglés. Y durante años, muchos juraban que decía algo bastante ofensivo.",
        "[amused] En 2019, Charles Martinet, la voz de Mario, lo aclaró. La frase es So long, King Bowser. Hasta luego, rey Bowser.",
        "Con su acento italiano exagerado, el King se escucha raro. Pero no hay nada más.",
        "[curious] Y en la versión de Switch, de 3D All-Stars, ese grito es otro, un simple adiós. Probablemente porque usa la versión Shindou, y no por censura.",
    ]},
    {"id": "s11", "frases": [
        "[curious] Número once. Los enemigos que nunca viste.",
        "Miyamoto contó que hicieron menos de cuarenta enemigos, cuando lo normal era el doble. No les dio tiempo.",
        "Pero en el código siguen algunos que se quedaron fuera.",
        "[impressed] Está Blargg, el monstruo de lava de Super Mario World, cargado pero sin colocar. Un saltamontes, unos Bullies pequeños de hielo, y Motos, un enemigo que agarraba a Mario y lo lanzaba.",
        "[playful] Hasta hay un huevo que todo el mundo creyó de Yoshi. Y resultó ser de Hoot, el búho.",
    ]},
    {"id": "s10", "frases": [
        "[curious] Número diez. Mario no siempre tuvo su voz.",
        "Super Mario 64 fue el primer juego de la serie principal en consola con la voz de Charles Martinet. Antes, solo lo había doblado en juegos de computadora y en ferias.",
        "[amused] Pero en la demo de 1995 todavía no estaba. Así que Mario gritaba con sonidos sacados de bibliotecas de efectos. Gritos genéricos, de vaquero.",
        "[warm] Luego llegó Martinet, con su It's-a me, Mario. Y esa voz acompañó al personaje durante casi treinta años.",
    ]},
    {"id": "s09", "frases": [
        "[mysterious] Número nueve. El reloj que obedece a la hora.",
        "Tick Tock Clock, el Reloj Tic Tac, se entra por un reloj de péndulo en el tercer piso del castillo.",
        "[impressed] Y lo que pasa dentro depende de dónde esté el minutero cuando saltas.",
        "Si entras con el minutero en las doce, todo se detiene. En las tres, se mueve lento. En las seis, se mueve al azar. Y en las nueve, todo va rápido.",
        "[playful] Muchos jugaron ese nivel durante años sin saber que podían congelarlo entero. Solo había que esperar a la hora correcta.",
    ]},
    {"id": "s08", "frases": [
        "[curious] Número ocho. El salto que cambia el agua.",
        "En Wet-Dry World, la Ciudad Esponja, el nivel del agua depende de algo que nadie te dice.",
        "[impressed] De la altura a la que saltas dentro del cuadro. Si entras por arriba, el agua está alta. Si entras por abajo, el nivel está casi seco.",
        "Todos los cuadros del castillo están divididos en tres zonas por dentro. Pero este es el único que de verdad usa esa división.",
        "[playful] Así que, si ese nivel se te hizo difícil, quizá solo estabas saltando a la altura equivocada.",
    ]},
    {"id": "s07", "frases": [
        "[ominous] Número siete. La escalera sin fin.",
        "Antes de enfrentar a Bowser por última vez, hay una escalera. Si no tienes setenta estrellas, subes y subes, y nunca llegas.",
        "[mysterious] El truco tiene dos partes. El juego te teletransporta unos escalones hacia atrás sin que lo notes, y esconde la cima con niebla.",
        "[impressed] Y la música es una ilusión. Se llama tono de Shepard. Es una escala que parece subir para siempre, aunque en realidad se repite.",
        "[thoughtful] Tus ojos y tus oídos te engañaban a la vez. Por eso esa escalera daba tanta angustia.",
    ]},
    {"id": "s06", "frases": [
        "[playful] Número seis. La cara que nació de unas pelotas de ping-pong.",
        "Al encender el juego, aparece la cabeza de Mario, y puedes estirarle la nariz, las orejas y los bigotes.",
        "Ese efecto lo programó Giles Goddard, un inglés que trabajaba en Nintendo.",
        "[amused] Según una de sus entrevistas, todo empezó como un experimento con una cámara. Se pegó pelotas de ping-pong pintadas en la cara, para que la computadora siguiera los puntos de color.",
        "[curious] Koizumi le preparó una cara de Mario que se moviera así. Miyamoto pasó, la vio, y pidió meterla en el juego. Y además, que se pudiera estirar.",
        "Ojo, en otra entrevista Goddard lo cuenta sin las pelotas, como pruebas de animación. Pero el resultado es el mismo. La pantalla de título más famosa de la consola.",
    ]},
    {"id": "s05", "frases": [
        "[impressed] Número cinco. El juego que agranda el cerebro.",
        "En 2013, el Instituto Max Planck de Alemania publicó un estudio en la revista Molecular Psychiatry.",
        "Pusieron a un grupo de adultos a jugar Super Mario 64 media hora al día durante dos meses.",
        "[curious] Y al final, tenían más materia gris en zonas del cerebro ligadas a la orientación espacial, la memoria y la planificación.",
        "[playful] Dos detalles. Jugaron la versión de Nintendo DS, y el grupo era pequeño. [short pause] Pero ya tienes una excusa científica para jugarlo otra vez.",
    ]},
    {"id": "s04", "frases": [
        "[excited] Número cuatro. Terminar el juego con cero estrellas.",
        "Mario 64 tiene un error famoso, el salto largo hacia atrás. En inglés, Backwards Long Jump.",
        "Si encadenas saltos largos de espaldas en una escalera, la velocidad se acumula sin límite. [short pause] Y Mario sale disparado.",
        "[impressed] Tan rápido, que atraviesa la escalera infinita y las puertas que piden estrellas.",
        "Nintendo lo corrigió en la versión Shindou de 1997. Y como 3D All-Stars se basa en esa versión, en Switch ya no funciona.",
        "[amused] Pero en el cartucho original sigue ahí. Y gracias a él, los speedrunners terminan el juego sin tocar una sola estrella.",
        "El récord actual con cero estrellas es de Suigi, en poco más de seis minutos. Y Suigi tiene también el de 120 estrellas, en una hora, treinta y cinco minutos y catorce segundos, de abril de este año.",
        "[playful] Tiene los cinco récords principales del juego. Y hay una bolsa de unos diez mil dólares para quien le quite uno. Nadie lo ha conseguido.",
    ]},
    {"id": "s03", "frases": [
        "[curious] Número tres. Medio botón A.",
        "En 2016, el youtuber pannenkoek subió un video sobre una estrella de Hazy Maze Cave, la Cueva del Laberinto.",
        "El reto era sacarla pulsando el botón A el menor número de veces posible. [short pause] Y la sacó con medio pulsado.",
        "[amused] ¿Medio? Sí. Contaba como medio porque el botón ya venía apretado desde antes, de otra parte del nivel.",
        "Para explicarlo, empezaba diciendo: pero primero, tenemos que hablar de universos paralelos. [short pause] Y esa frase se convirtió en uno de los memes más famosos de internet.",
        "[impressed] En 2023 bajó esa estrella a cero pulsados. Y en mayo de 2024, otro jugador terminó el juego entero sin tocar el botón A. Le llevó 86 horas.",
    ]},
    {"id": "s02", "frases": [
        "[mysterious] Número dos. El rayo cósmico.",
        "En septiembre de 2013, durante una transmisión en directo, a un jugador llamado DOTA Teabag le pasó algo imposible en Tick Tock Clock.",
        "[tense] Mario subió de golpe, como teletransportado, hasta una plataforma más alta. Sin ningún truco conocido.",
        "Nadie pudo repetirlo. Pannenkoek llegó a ofrecer mil dólares a quien lo consiguiera.",
        "[curious] Al analizar el valor de la altura de Mario, la diferencia cuadraba con un solo bit que había cambiado, un uno donde había un cero o al revés.",
        "[mysterious] Y ahí nació la teoría. Que un rayo cósmico, una partícula del espacio, atravesó la consola en ese segundo y cambió ese bit.",
        "[thoughtful] Ojo, no está probado. Otros creen que fue un cartucho mal puesto o un fallo de la consola. Pero nadie ha encontrado una explicación mejor.",
    ]},
    {"id": "s01", "frases": [
        "[dramatic] Y llegamos al número uno. [short pause] Luigi era real.",
        "Recuerda la placa del patio. En 1996, la revista IGN ofreció cien dólares a quien desbloqueara a Luigi. Nadie los cobró.",
        "Y en 1998, Nintendo of America respondió por carta que era una broma de los programadores.",
        "[serious] Pero Luigi sí estuvo en el juego. Miyamoto lo dijo en 1996: hasta febrero, estaba en el juego.",
        "[warm] Contó que la pantalla se dividía, que Mario y Luigi entraban al castillo por separado, y que cuando se encontraban en un pasillo, él era increíblemente feliz.",
        "[sad] Pero la memoria no alcanzaba. Koizumi lo resumió así: con lágrimas, tuvimos que pedirle a Luigi que se fuera.",
        "[excited] En 2020, una filtración enorme de archivos de Nintendo sacó a la luz su modelo y sus texturas. Y los fans lo hicieron funcionar sobre el esqueleto de Mario.",
        "[mysterious] Y en octubre de 2026, el programador Mochi64 analizó la placa. Probó unas 530 tipografías y millones de combinaciones de letras, contra esa textura diminuta.",
        "[impressed] La que mejor encaja no dice L is real. [short pause] Dice: Eternal Star. Y debajo: We hope so. Estrella eterna. Eso esperamos.",
        "[thoughtful] No es una confirmación de Nintendo, es la mejor coincidencia estadística. Pero después de treinta años, la placa por fin tiene una respuesta. [short pause] Y Luigi también. Estuvo ahí, solo que no llegó.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Esos son los veinte secretos de Super Mario 64. Un conejo con nombre de procesador, una escalera que mentía, medio botón A y un rayo del espacio.",
        "[thoughtful] Treinta años después, sigue siendo el juego que enseñó a todos cómo moverse en tres dimensiones.",
        "[curious] ¿Cuál de estos secretos no conocías? ¿Y llegaste a ver a Yoshi en el tejado? Cuéntamelo en los comentarios. Los leo todos, y me ayudan a mejorar cada video.",
        "[warm] Y si quieres más secretos de la Nintendo 64, aquí tienes los de Majora's Mask. Nos vemos en la próxima crónica.",
    ]},
]
