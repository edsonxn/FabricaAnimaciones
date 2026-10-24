# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Zelda: Majora's Mask: su historia y los 12 secretos QUE IGNORASTE» (23-oct-2026).
Fórmula de zelda_oot (motor SECUENCIA YT + pegatinas + fichas + MG nuevos), variable que cambia: SOLO el juego. Kit NUEVO
`nucleo/mg_majora.py`: fichas TRANSLÚCIDAS con la interfaz del propio Majora (diálogo N64, cartel «Amanecer…», reloj de 3 días),
regla del usuario del 22-oct. Música = BANDA SONORA OFICIAL del juego (regla del 23-oct; recordatorio del usuario hoy):
`armar_musica_ost.py`, pistas en audio/ost/ (Nintendo Music Archive, audio original de N64). Voz ElevenLabs Hope con corchetes.
Gancho: la banda sonora entró en Nintendo Music el 8/9-oct-2026 (40.º aniversario de Zelda); llegó a América el 26-oct-2000;
el remake de Ocarina sale el 5-nov-2026.
Datos verificados el 23-oct-2026 (agente; [O] oficial, [I] implícito, [T] teoría, [F] ficción — se dicen como tales):
- Wikipedia MM: JP 27-abr-2000, NA 26-oct-2000, EU 17-nov-2000 · Expansion Pak obligatorio (4 -> 8 MB), en Japón en paquete.
- Iwata Asks MM3D «Make it in a Year» / Game Developer: Miyamoto, un juego en un año reutilizando los modelos de Ocarina; Aonuma
  no quería rehacer mazmorras (Ura Zelda) y pidió algo nuevo. Source Gaming: «Zelda Gaiden» desde el 1-feb-1999 (64DD).
- Iwata Asks / Pocket Gamer: juego de mesa de policías y ladrones de Koizumi (una semana de juego) -> ciclo de una semana
  recortado a 3 días. Run Lola Run: «una de las influencias citadas» (relatos contradictorios, BFI).
- Famitsu 37/40 · Metacritic 95 · ventas «más de 3 millones» (sin cifra oficial). Kondo; Minegishi 3 temas de batalla.
- Zelda Wiki: cartero (Madame Aroma, gorra) · canciones ocultas (invertida = 1/3 en N64; doble tiempo) · «Ellos» y Romani ·
  Kafei (Sakon, Máscara del Sol, ciclo entero) · Darmani III (alud) · Mikau (huevos de Lulu, piratas) · Fiera Deidad = 20 máscaras
  a los niños de la luna (no 24), solo jefes en N64 · Elegía del Vacío (4 estatuas, solo Ikana) · Deku Butler's Son [I] ·
  Skull Kid «huele igual» que el niño hada [I] · guardado (búho temporal; 3DS permanente) · cambios de 3DS.
- Time Extension 12-2024 / Nintendo Life 1-2025: comandos de voz ocultos para el micrófono VRS (Zoinkity 2018, Skawo 12-2024).
- Wikipedia Ben Drowned [F]: Alex Hall «Jadusable», 4chan 7-sep-2010, ARG que terminó el 31-oct-2020.
- Zelda Dungeon: cinco etapas del duelo [T]; Aonuma solo habló de tonos emocionales en algunos episodios.
- Nintendo Life / Final Weapon 9-oct-2026: banda sonora en Nintendo Music (111 pistas). Remake OoT 5-nov-2026.
"""

TITULO = "Zelda: Majora's Mask: su historia y los 12 secretos QUE IGNORASTE"
ARCHIVO = "majora_mask"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
# Voz del canal desde banjo_tooie (19-oct-2026, el usuario): ElevenLabs Hope, eleven_v4 + corchetes de actuación.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)

# ElevenLabs dice el inglés nativo: solo lo que lee mal
FONETICA = {}
# Revisado el 23-oct leyendo voz/eval.json: Whisper escribe «Tattle y Tail», «Skullcat», «Café» (Kafei), «Icana», «Mujagente»:
# falsas alarmas; se aceptan con la CER de la toma única. Colas largas = ElevenLabs habla hasta el final.
CER_MAX_POR_FRASE = {"lore_1": .03, "lore_3": .03, "p11_2": .025, "p9_4": .03, "p8_1": .07, "p8_4": .02, "p6_2": .025,
                     "p1_4": .02}
TAIL_MAX_POR_FRASE = {"cierre_1": 1.05, "lore_1": .9, "p8_1": .9}
GAP_MAX_POR_FRASE = {"p8_1": .95, "lore_1": .8}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={'scene-001': 0.075, 'scene-003': 0.131, 'scene-004': 0.131, 'scene-008': 0.078, 'scene-009': 0.131, 'scene-010': 0.131, 'scene-011': 0.131, 'scene-012': 0.149, 'scene-013': 0.131, 'scene-017': 0.131, 'scene-018': 0.131, 'scene-019': 0.131, 'scene-020': 0.131, 'scene-021': 0.131, 'scene-022': 0.131, 'scene-023': 0.131, 'scene-024': 0.131, 'scene-025': 0.131, 'scene-026': 0.131, 'scene-027': 0.131, 'scene-028': 0.131, 'scene-029': 0.131, 'scene-030': 0.131, 'scene-031': 0.131, 'scene-032': 0.131, 'scene-033': 0.131, 'scene-034': 0.131, 'scene-035': 0.131, 'scene-036': 0.131, 'scene-037': 0.131, 'scene-038': 0.131, 'scene-039': 0.131, 'scene-040': 0.131, 'scene-041': 0.131, 'scene-042': 0.131, 'scene-043': 0.131, 'scene-044': 0.131, 'scene-045': 0.131, 'scene-046': 0.131, 'scene-047': 0.131, 'scene-048': 0.131, 'scene-049': 0.149, 'scene-050': 0.131, 'scene-051': 0.131, 'scene-052': 0.131, 'scene-053': 0.131, 'scene-054': 0.131, 'scene-055': 0.131, 'scene-056': 0.131, 'scene-057': 0.131, 'scene-060': 0.131, 'scene-061': 0.131, 'scene-062': 0.131, 'scene-063': 0.131, 'scene-064': 0.131, 'scene-065': 0.131, 'scene-066': 0.131, 'scene-067': 0.131, 'scene-068': 0.131, 'scene-069': 0.131, 'scene-070': 0.131, 'scene-071': 0.131, 'scene-072': 0.131, 'scene-073': 0.131, 'scene-074': 0.131, 'scene-075': 0.131, 'scene-076': 0.131, 'scene-077': 0.131, 'scene-078': 0.131, 'scene-079': 0.131, 'scene-080': 0.131, 'scene-081': 0.131, 'scene-082': 0.131, 'scene-083': 0.131, 'scene-084': 0.131, 'scene-085': 0.131, 'scene-086': 0.131, 'scene-087': 0.131, 'scene-089': 0.135, 'scene-090': 0.131, 'scene-093': 0.061, 'scene-094': 0.131, 'scene-095': 0.131, 'scene-096': 0.131, 'scene-097': 0.131, 'scene-098': 0.131, 'scene-099': 0.131, 'scene-101': 0.131, 'scene-102': 0.131, 'scene-103': 0.131, 'scene-104': 0.131, 'scene-105': 0.131, 'scene-106': 0.131, 'scene-107': 0.131},   # marco NSO de ZeldaCentral fijado a 0,131 (lección de zelda_oot); externos medidos el 23-oct
    yt=dict(sufijo="", min_s=30, max_min=1100, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: la música es la banda sonora OFICIAL de Majora's Mask (armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[mysterious] Este mes, Nintendo subió a su aplicación de música la banda sonora completa de Majora's Mask. Ciento once pistas, veintiséis años después.",
        "Y no es casualidad. El cinco de noviembre llega el remake de Ocarina of Time, y Majora's Mask es el juego que nació justo de sus restos.",
        "[curious] Un juego hecho en un solo año, con una luna que te mira desde el cielo, y tres días que se repiten una y otra vez.",
        "Un cartero que no puede huir, [whispers] unas máscaras que guardan a gente muerta, y un micrófono que nunca llegaste a usar.",
        "[playful] Así que hoy te cuento cómo se hizo, la historia de Termina, y los doce secretos de Majora's Mask que seguramente ignoraste.",
    ]},
    {"id": "origen", "frases": [
        "[curious] Cuando terminó Ocarina of Time, a Eiji Aonuma le tocaba un encargo poco emocionante. Rehacer sus mazmorras para una expansión, la que se llamaba Ura Zelda.",
        "Aonuma no quería volver a hacer las mismas mazmorras, y pidió hacer un juego nuevo. [short pause] Shigeru Miyamoto le dijo que sí, pero con una condición.",
        "[serious] Tenía que estar terminado en un año, reutilizando los modelos en tres dimensiones de Ocarina of Time.",
        "El proyecto empezó en febrero de mil novecientos noventa y nueve, con un nombre provisional. Zelda Gaiden, algo así como Zelda, la historia paralela.",
        "[amused] La idea del tiempo salió de Yoshiaki Koizumi, el otro director. Él estaba diseñando un juego de mesa de policías y ladrones, en el que había que atrapar a un criminal en una semana de juego.",
        "Al principio el ciclo de Majora's Mask también iba a durar una semana. [short pause] Pero era demasiado largo para repetirlo, y no daba tiempo a terminarlo en un año. Así que se quedó en tres días.",
        "[curious] Entre las influencias citadas está también Corre, Lola, corre, una película alemana de mil novecientos noventa y ocho donde la protagonista repite la misma carrera de veinte minutos hasta salvar a su novio.",
        "[impressed] Y el juego pedía más de lo que la consola tenía. Era obligatorio el Expansion Pak, el accesorio que doblaba la memoria de cuatro a ocho megas. [short pause] En Japón se vendía en el mismo paquete.",
        "Salió en Japón en abril del dos mil, y en América el veintiséis de octubre. Sacó un treinta y siete sobre cuarenta en Famitsu, un noventa y cinco en Metacritic, y vendió más de tres millones de copias.",
    ]},
    {"id": "lore", "frases": [
        "[serious] Ahora, la historia. Unos meses después de Ocarina of Time, Link se va de Hyrule a caballo, en un viaje secreto, buscando a un amigo querido.",
        "En un bosque, un Skull Kid con una máscara extraña y dos hadas, Tatl y Tael, le roban a Epona y la ocarina. [short pause] Link lo persigue, cae por un tronco hueco, y aparece en otro mundo.",
        "[grim] Ese mundo es Termina. Y lo primero que le pasa es que el Skull Kid lo convierte en un Deku, una criatura de madera.",
        "[curious] Allí conoce al vendedor de máscaras felices. Skull Kid le robó su tesoro, la Máscara de Majora, un objeto que da un poder terrible a quien la lleva.",
        "[ominous] Y con ese poder, el Skull Kid está tirando la luna sobre Ciudad Reloj. Una luna con cara, que caerá en tres días, justo cuando empieza el carnaval.",
        "Link recupera su ocarina, toca la Canción del Tiempo, y vuelve al amanecer del primer día. [short pause] Así empieza el ciclo. Cada tres días, todo vuelve a empezar.",
        "Para pararla, tiene que despertar a cuatro gigantes que duermen en los templos de Termina. El pantano del sur, las montañas nevadas del norte, la gran bahía del oeste y el valle de Ikana al este.",
        "[sad] Esos gigantes eran los amigos del Skull Kid. Cuando se fueron a proteger el mundo, él se sintió abandonado, y esa soledad fue lo que la máscara aprovechó.",
        "[dramatic] Con los cuatro despiertos, los gigantes sostienen la luna. La máscara abandona al Skull Kid, entra en la luna, y Link la sigue. [excited] Vamos con los secretos.",
    ]},
    {"id": "p12", "frases": [
        "[excited] Número doce. [short pause] El hombre que no puede huir.",
        "En Ciudad Reloj, cuando la luna está a punto de caer, casi todo el mundo se va. Pero el cartero sigue repartiendo cartas, mirando el reloj, como si no pasara nada.",
        "[amused] ¿Por qué no huye? [short pause] Porque su horario no se lo permite. Su vida entera es cumplir el reparto a la hora exacta.",
        "Solo se va la última noche, cuando Madame Aroma, la alcaldesa, le da permiso. [short pause] Y antes de correr, te regala su gorra de cartero.",
        "[thoughtful] Es uno de los detalles más tristes y más graciosos del juego. Un hombre al que el fin del mundo no asusta tanto como llegar tarde.",
    ]},
    {"id": "p11", "frases": [
        "[playful] En el once, las canciones que no salen en el menú.",
        "Tres días son poco tiempo, y el juego lo sabe. Por eso esconde dos canciones que no aparecen en tu lista.",
        "[curious] Si tocas la Canción del Tiempo al revés, el reloj se ralentiza. En la Nintendo sesenta y cuatro, el tiempo pasa a un tercio de su velocidad.",
        "Y si tocas cada nota dos veces, la Canción del Doble Tiempo te salta directamente a la siguiente mañana o la siguiente noche.",
        "[amused] ¿Quién te lo cuenta? [short pause] Un espantapájaros que baila. Muchos jugadores terminaron el juego sin hablar nunca con él.",
    ]},
    {"id": "p10", "frases": [
        "[mysterious] Número diez. Lo que viene del cielo al rancho Romani.",
        "En el rancho vive una niña, Romani, que te pide ayuda con algo muy raro. Dice que la primera noche, de madrugada, llegan Ellos. [short pause] Unos seres que bajan de una luz y se llevan a las vacas.",
        "[tense] Si te quedas a defender el granero con tu arco hasta el amanecer, los espantas, y Romani te regala una botella de leche.",
        "[grim] Pero si fallas, Ellos también se llevan a Romani. Al día siguiente ella vuelve, pero no recuerda nada, se agarra la cabeza, y apenas habla.",
        "[serious] Y ya no puedes acompañar a su hermana Cremia con la leche. [short pause] En un juego de Nintendo, una abducción con consecuencias. Así de raro era Majora's Mask.",
    ]},
    {"id": "p9", "frases": [
        "[curious] En el nueve, el juego que te castigaba por guardar.",
        "Para guardar de verdad en Majora's Mask tienes que tocar la Canción del Tiempo. Y eso te devuelve al primer día. [short pause] Perdiendo tus rupias y tus objetos de usar y tirar.",
        "Había otra forma, las estatuas de búho. Pero ese guardado era temporal. [sighs] Lo cargabas una vez, y se borraba.",
        "[amused] Así que si te quedaban diez minutos para la luna y tenías que irte a cenar, la decisión era dura.",
        "[impressed] En la versión de tres de ese, de dos mil quince, Nintendo cambió todo eso. Los búhos y unas estatuas nuevas guardan para siempre, y el cuaderno de los Bombers se rellena solo.",
    ]},
    {"id": "p8", "frases": [
        "[warm] Número ocho. La misión más larga del juego.",
        "Anju lleva el hotel de Ciudad Reloj, y está a punto de casarse con Kafei. [short pause] Pero Kafei ha desaparecido.",
        "[curious] Lo que nadie sabe es que el Skull Kid lo convirtió en niño, y que un ladrón, Sakon, le robó la Máscara del Sol, la que iba a usar en la boda.",
        "Para reunirlos tienes que seguirlos los tres días enteros, a horas exactas. Es la única misión del cuaderno de los Bombers que ocupa un ciclo completo.",
        "[impressed] Por el camino te llevas la máscara de Keaton, la gorra del cartero y la máscara de los novios. [short pause] Y si lo logras, Kafei llega al hotel de madrugada, en las últimas horas.",
        "[sad] Se unen con sus máscaras en el hotel, a minutos de que caiga la luna. [short pause] Saben que es el final, y deciden recibirlo juntos.",
    ]},
    {"id": "p7", "frases": [
        "[mysterious] En el siete, un viejo conocido.",
        "Al final del juego, el Skull Kid le dice a Link algo muy curioso. [short pause] Que huele igual que el niño hada que le enseñó una canción en el bosque.",
        "[curious] En Ocarina of Time, en el Bosque Perdido, hay un Skull Kid sentado en un tronco. Si le tocas la canción de Saria, te da una pieza de corazón.",
        "Ese niño hada era Link. [short pause] Así que el villano de Majora's Mask sería el mismo Skull Kid al que hiciste bailar años antes.",
        "[thoughtful] Nintendo nunca lo ha dicho con todas las letras, pero el juego deja la pista ahí. Y le da al final otro sentido. El Skull Kid solo quería un amigo, y el amigo era Link.",
    ]},
    {"id": "p6", "frases": [
        "[excited] Número seis. La máscara más poderosa.",
        "Dentro de la luna hay un prado, un árbol, y cuatro niños que llevan las máscaras de los jefes. [short pause] Corretean por el prado, y te piden máscaras a cambio de jugar con ellos.",
        "[curious] Mucha gente dice que necesitas las veinticuatro máscaras para la recompensa. Pero no es así. Necesitas las veinte que no te transforman.",
        "Cuando se las das todas, el último niño, el de la Máscara de Majora, te regala la Máscara de la Fiera Deidad.",
        "[impressed] Con ella, Link se convierte en un guerrero adulto de ojos blancos, con una espada doble que lanza rayos. [short pause] La pelea final pasa de difícil a casi injusta.",
        "[amused] Pero tiene truco. En la Nintendo sesenta y cuatro solo funciona en las peleas contra jefes. Fuera de ellas, no te la puedes poner.",
    ]},
    {"id": "p5", "frases": [
        "[serious] Número cinco. Las máscaras que guardan a un muerto.",
        "En las montañas del norte encuentras a un fantasma junto a una tumba. Es Darmani, el héroe de los Goron, que murió al caer por un barranco por culpa de un alud.",
        "[sad] Le tocas la Canción de Curación, su alma descansa, [short pause] y te deja una máscara con su cara. Con ella, Link se convierte en Darmani.",
        "En la gran bahía pasa lo mismo. Mikau, el guitarrista de una banda zora, llega a la orilla herido de muerte. Las piratas le robaron los huevos de su compañera Lulu.",
        "[grim] Tú le tocas la canción, él muere, y tú cavas su tumba. [short pause] Su lápida es su propia guitarra.",
        "[thoughtful] Así que, cada vez que te pones esas máscaras, vas por Termina con la cara de alguien que ya no está. Y los demás personajes te saludan como si fueran ellos.",
    ]},
    {"id": "p4", "frases": [
        "[mysterious] En el cuatro, ¿de quién era la máscara Deku?",
        "La primera transformación del juego es la máscara Deku. Y el juego nunca dice de quién era. [short pause] Pero deja pistas.",
        "[curious] En el palacio Deku, el mayordomo del rey te dice que le recuerdas a su hijo, que desapareció. Y en los créditos, ese mayordomo llora frente a un árbol retorcido, con forma de niño Deku.",
        "Y hay más. En el valle de Ikana aprendes la Elegía del Vacío, una canción que deja una estatua de ti mismo. [short pause] Una por cada forma de Link.",
        "[ominous] La estatua de Darmani, la de Mikau, la del propio Link, [whispers] y la de Link Deku, que tiene la cara del hijo del mayordomo.",
        "[serious] Nintendo nunca lo ha confirmado. Pero todo apunta a que la máscara Deku es el alma de ese niño, y que, cada vez que te la pones, llevas su cara.",
    ]},
    {"id": "p3", "frases": [
        "[ominous] Número tres. El cartucho maldito que nunca existió.",
        "En septiembre de dos mil diez, un usuario de 4chan contó que había comprado un cartucho de Majora's Mask en una venta de garaje. Con una partida guardada a nombre de Ben.",
        "[whispers] Según su relato, el juego se rompía de formas imposibles. Un cuarto día que no existe, una ciudad vacía, y una estatua de Link que lo seguía y lo miraba.",
        "[tense] Lo fue publicando por capítulos, con videos de la partida, y miles de personas lo siguieron en directo, día a día.",
        "[serious] Pero todo era ficción. Lo escribió Alex Hall, que firmaba como Jadusable. Era una historia de terror con forma de juego de realidad alternativa, y no terminó hasta octubre de dos mil veinte.",
        "[thoughtful] Ben Drowned se convirtió en una de las leyendas más famosas de internet. [short pause] Y no eligió Majora's Mask por casualidad. Ningún otro Zelda daba tanto miedo sin intentarlo.",
    ]},
    {"id": "p2", "frases": [
        "[curious] Número dos. Un micrófono que nunca usaste.",
        "En Japón, Nintendo vendía un micrófono para la Nintendo sesenta y cuatro. Se usaba en Hey You, Pikachu!, para hablarle a Pikachu.",
        "[impressed] Y resulta que Majora's Mask tiene, escondido en el código, soporte para ese micrófono. En todas las versiones del cartucho.",
        "Según lo que encontraron los investigadores, ibas a poder sacar fotos con tu voz, y despertar a un Deku dormido hablándole en japonés.",
        "[amused] Pero el juego lo desactiva con una variable que nunca toma el valor necesario. [short pause] El código estuvo ahí veinticuatro años sin que nadie lo usara.",
        "[excited] En diciembre de dos mil veinticuatro, un aficionado lo encendió y lo probó con el micrófono real. Y funcionaba. Majora's Mask iba a ser uno de los primeros juegos de la consola que te escuchaban.",
    ]},
    {"id": "p1", "frases": [
        "[dramatic] Y llegamos al número uno. La teoría que convirtió Termina en otra cosa.",
        "Hay una idea que los fans repiten desde hace años. [short pause] Que cada zona de Termina es una de las cinco etapas del duelo.",
        "[serious] Ciudad Reloj sería la negación, gente que sigue con el carnaval aunque la luna está encima. El pantano sería la ira, el rey Deku castigando a un mono inocente.",
        "Las montañas nevadas serían la negociación, con el fantasma de Darmani pidiendo otra oportunidad. La gran bahía, la depresión, con Lulu que perdió la voz.",
        "[ominous] Y el valle de Ikana, la aceptación. Un reino de muertos que ya no luchan contra su destino.",
        "[curious] Algunos van más allá, y dicen que Link murió al caer por el tronco, y que Termina es una especie de limbo.",
        "[thoughtful] Ojo, todo esto es una teoría. Aonuma solo ha dicho que algunos episodios tenían un tono emocional buscado a propósito, no que cada zona sea una etapa.",
        "[warm] Pero que tanta gente lo vea así dice mucho del juego. Majora's Mask habla de perder a alguien, de lo que haces cuando sabes que se acaba el tiempo. [short pause] Y eso, en un juego hecho en un año, es mucho decir.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Esos son los doce secretos de Majora's Mask. Un cartero puntual, unas máscaras con dueño, un micrófono olvidado y una luna que nunca dejó de mirarnos.",
        "[thoughtful] Es el Zelda más raro, el más triste, y para muchos el mejor. Y salió de un reto imposible, un juego entero en un año.",
        "[curious] ¿Tú llegaste a sacar la Máscara de la Fiera Deidad? ¿O sabías lo del micrófono? Cuéntamelo en los comentarios.",
        "Y si quieres más secretos de otro clásico de la Nintendo sesenta y cuatro, déjalo también abajo. [warm] Nos vemos en el amanecer de la próxima crónica.",
    ]},
]
