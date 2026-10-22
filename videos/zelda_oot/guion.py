# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Zelda: Ocarina of Time: su historia y los 12 secretos QUE IGNORASTE» (22-oct-2026).
Misma fórmula que banjo_tooie (motor SECUENCIA YT + pegatinas + fichas + MG nuevos del kit `nucleo/mg_gaming.py`, voz ElevenLabs
Hope con corchetes); variable que cambia: el juego. Gancho de actualidad: el remake de Nintendo Switch 2 sale el 5-nov-2026
(Engadget / Nintendo Everything / Forbes, anunciado en el Direct de junio, fecha en el Direct del 40.º aniversario de septiembre).
Datos verificados el 22-oct-2026 (agente de verificación):
- Wikipedia «The Legend of Zelda: Ocarina of Time»: JP 21-nov-1998 / NA 23-nov / EU 11-dic; hecho a la vez que Mario 64 con su
  motor de base; pensado para 64DD (el disco no leía rápido); 5 directores (Osawa, Yamada, Aonuma -mazmorras-, Koizumi, Iwawaki);
  primera persona descartada al añadir a Link niño; 256 Mbit (el mayor de Nintendo); 7,6 M en N64; v1.2 quita el canto del Templo
  del Fuego (adhan de una biblioteca comercial) y la sangre de Ganondorf pasa a verde; GameCube cambia el símbolo gerudo.
- Iwata Asks OoT 3D: castillo de Ganon como único escenario (Miyamoto); Toei Kyoto Studio Park, enemigos de uno en uno (Koizumi).
- Time Extension (2025): primer 40/40 de Famitsu · Guinness: único 99 de Metacritic · 1101.com: Kondo, 5 notas, difícil componer.
- The Guardian 25-nov-2009 / Game Informer: Aonuma pide perdón por las botas de hierro · 3DS: botas en un botón.
- Game Developer: Miyamoto da a elegir a Aonuma entre Ura Zelda o un juego nuevo en un año -> Majora's Mask. Master Quest JP 28-nov-2002.
- Zelda Dungeon (patio): ventana de Mario + tirachinas = rupia roja; la otra = soldado que lanza bomba; 3DS = nivel de Super Mario Bros.
- Zelda Wiki / StrategyWiki: vaca de Malon (< 50 s), sombrero del pescador (adulto), Gossip Stones + bomba = cohete, canción de la
  tormenta (paradoja), 11 objetos de Biggoron (3 días, o 6 veces la canción del Sol), Casa de las Skulltulas (10/20/30/40/50/100).
- Hyrule Historia (JP 21-dic-2011): tres líneas temporales. Remake Switch 2: Direct 9-jun-2026, fecha 5-nov-2026 (Direct 8-sep).
"""

TITULO = "Zelda: Ocarina of Time: su historia y los 12 secretos QUE IGNORASTE"
ARCHIVO = "zelda_oot"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
# Voz del canal desde banjo_tooie (19-oct-2026, el usuario): ElevenLabs Hope, eleven_v4 + corchetes de actuación.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)

# ElevenLabs dice el inglés nativo: solo lo que lee mal
FONETICA = {}
# Revisado el 22-oct leyendo voz/eval.json: Whisper escribe «lago Gilia», «Cacarico», «esculturas doradas», «64DD», «La Z»,
# «cambio» por «cameo»: falsas alarmas; se aceptan con la CER de la toma única. Colas largas = ElevenLabs habla hasta el final.
CER_MAX_POR_FRASE = {"p11_1": .03, "p10_0": .04, "p10_2": .03, "p10_4": .04, "p9_4": .035, "p8_0": .1, "p8_2": .035,
                     "p7_3": .045, "p6_5": .035, "p5_3": .04, "p4_1": .02, "p4_3": .03, "p2_1": .025}
TAIL_MAX_POR_FRASE = {"p11_1": .7, "p10_2": .9, "p9_4": .8, "p7_3": .9, "p6_5": 1.0, "p2_1": .9, "p5_3": .65}

# Marcos y paneles de las fichas/MG pintados en Flow (el usuario, 22-oct-2026: «esos cuadros de texto se ven muy poco
# trabajados… apóyate de Flow»): prompts.json -> nucleo/flow_integrado.py paquete -> ui/ (recortados sobre blanco).
FICHA = dict(
    estilo="High-quality hand-painted video game interface asset inspired by late-1990s fantasy adventure games: ancient "
           "temple craftsmanship, carved weathered stone, aged hammered gold trim, deep royal-blue and emerald enamel inlays, "
           "soft warm rim light, crisp painterly detail, clean silhouette, a single object centered and isolated on a plain "
           "flat pure white background, straight front view with no perspective tilt",
    cierre="No text, no letters, no numbers, no runes, no watermark.")

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={'scene-002': 0.131, 'scene-003': 0.131, 'scene-004': 0.126, 'scene-005': 0.131, 'scene-006': 0.131, 'scene-007': 0.131, 'scene-008': 0.131, 'scene-009': 0.131, 'scene-010': 0.131, 'scene-011': 0.131, 'scene-012': 0.131, 'scene-013': 0.131, 'scene-015': 0.131, 'scene-016': 0.192, 'scene-017': 0.131, 'scene-018': 0.131, 'scene-019': 0.131, 'scene-020': 0.131, 'scene-021': 0.131, 'scene-022': 0.131, 'scene-023': 0.131, 'scene-024': 0.131, 'scene-025': 0.131, 'scene-026': 0.131, 'scene-027': 0.131, 'scene-028': 0.131, 'scene-029': 0.131, 'scene-030': 0.131, 'scene-031': 0.131, 'scene-032': 0.131, 'scene-033': 0.13, 'scene-035': 0.131, 'scene-039': 0.129, 'scene-040': 0.129, 'scene-041': 0.129, 'scene-042': 0.131, 'scene-043': 0.131, 'scene-044': 0.13, 'scene-045': 0.13, 'scene-046': 0.131, 'scene-047': 0.145, 'scene-048': 0.145, 'scene-049': 0.145, 'scene-050': 0.145, 'scene-051': 0.131, 'scene-052': 0.131, 'scene-053': 0.131, 'scene-054': 0.131, 'scene-055': 0.131, 'scene-056': 0.131, 'scene-057': 0.131, 'scene-058': 0.131, 'scene-059': 0.131, 'scene-060': 0.131, 'scene-061': 0.131, 'scene-062': 0.131, 'scene-063': 0.131, 'scene-064': 0.131, 'scene-065': 0.131, 'scene-066': 0.131, 'scene-067': 0.131, 'scene-068': 0.131, 'scene-069': 0.037, 'scene-070': 0.037, 'scene-071': 0.131, 'scene-072': 0.131, 'scene-073': 0.131, 'scene-074': 0.131, 'scene-075': 0.131, 'scene-076': 0.131, 'scene-077': 0.175, 'scene-078': 0.174, 'scene-079': 0.131, 'scene-080': 0.13, 'scene-081': 0.17, 'scene-085': 0.131, 'scene-086': 0.131, 'scene-087': 0.131, 'scene-088': 0.131, 'scene-089': 0.131, 'scene-090': 0.131, 'scene-091': 0.131, 'scene-092': 0.131, 'scene-093': 0.131, 'scene-094': 0.131, 'scene-095': 0.131, 'scene-096': 0.131, 'scene-097': 0.131, 'scene-098': 0.131, 'scene-099': 0.131, 'scene-100': 0.131, 'scene-101': 0.131, 'scene-102': 0.131, 'scene-108': 0.126, 'scene-109': 0.131, 'scene-110': 0.131, 'scene-111': 0.131},   # marco NSO / pillarbox medidos el 22-oct (medir_marco.py)
    yt=dict(sufijo="", min_s=30, max_min=1100, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Late-90s fantasy adventure soundtrack: ocarina-like flute, harp arpeggios, warm strings, soft hand percussion, "
           "light choir pads, instrumental only, no vocals, gentle and unobtrusive under narration.",
    escenas={
        "intro": ("mysterious and nostalgic, a lone flute over soft harp, a legend about to be retold", 4),
        "origen": ("curious and inventive, light pizzicato strings and marimba under the flute, a studio at work", 5),
        "lore": ("forest calm turning ominous, low strings and timpani, a dark king rises, then hopeful and heroic", 7),
        "p12": ("pastoral ranch tune, gentle guitar and flute, warm and playful", 4),
        "p11": ("lazy fishing pond, plucked strings, comic and relaxed", 3),
        "p10": ("royal castle garden, delicate harp and celesta, sneaky and amused", 3),
        "p9": ("mysterious stone whispers, chimes and soft drones, then a playful pop", 3),
        "p8": ("eerie village house at night, creepy pizzicato and music box", 4),
        "p7": ("adventurous errand across the land, galloping rhythm and brass, ticking clock urgency", 6),
        "p6": ("underwater temple, slow watery bells and pads, tedious and heavy", 5),
        "p5": ("volcanic temple, hand drums and low choir, tense and secretive", 5),
        "p4": ("old machine hum turning into a mysterious masked melody, curious", 4),
        "p3": ("tender ocarina-like flute melody, warm strings, wonder", 5),
        "p2": ("whirling windmill waltz, accordion-like reed and strings, a time loop, mind-bending", 5),
        "p1": ("epic and emotional, full orchestra and choir rising, three paths of fate, majestic", 7),
        "cierre": ("warm nostalgic reprise of the flute theme, gentle harp, fading out", 4),
    },
    tramos=[   # <= 175 s cada uno (tiempos del 22-oct: 167 / 104 / 122,5 / 143,5 / 120 / 122,6 / 62,6 / 113,4 s)
        (["intro", "origen"], "Begin from near silence with a lone flute. End on a warm sustained chord."),
        (["lore"], "Begin on a warm chord in a calm forest, turn dark and ominous, end hopeful on a held note."),
        (["p12", "p11", "p10"], "Begin on a held note, playful and pastoral. End on a light held chord."),
        (["p9", "p8", "p7"], "Begin on a light chord, mysterious then eerie, then an urgent adventurous gallop. End on a held note."),
        (["p6", "p5"], "Begin on a held note, watery and slow, then volcanic and tense. End on a low foreboding note."),
        (["p4", "p3"], "Begin on a low note, mysterious and curious, then tender and full of wonder. End on a soft chord."),
        (["p2"], "Begin on a soft chord, a whirling waltz loop, mind-bending. End on a suspended note."),
        (["p1", "cierre"], "Begin on a suspended note, rise to an epic emotional peak with choir, then settle into a warm "
                           "nostalgic reprise and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[mysterious] El cinco de noviembre, Nintendo vuelve a lanzar un juego de mil novecientos noventa y ocho. Rehecho desde cero, para Nintendo Switch 2.",
        "Y no es un juego cualquiera. [short pause] Es Ocarina of Time, el juego con la nota más alta de la historia de Metacritic.",
        "[curious] Pero antes de que el remake lo cambie todo, vale la pena mirar el original. Porque ese cartucho guarda cosas que muchos no vieron en su día.",
        "Una vaca que aparece dentro de tu casa, un canto que Nintendo borró en silencio, [whispers] y una canción que nadie compuso, porque se la enseñaste tú mismo.",
        "[playful] Así que hoy te cuento cómo se hizo, la historia de Link, y los doce secretos de Ocarina of Time que seguramente ignoraste.",
    ]},
    {"id": "origen", "frases": [
        "[curious] Mientras un equipo de Nintendo hacía Super Mario sesenta y cuatro, otro, en el mismo edificio y con el mismo motor de base, se preguntaba cómo se pelea con espada en tres dimensiones.",
        "Al frente estaba Shigeru Miyamoto, como productor, con Koji Kondo en la música, y cinco directores que se repartían el trabajo. Uno de ellos era un joven Eiji Aonuma, que diseñó las mazmorras.",
        "[amused] La primera idea de Miyamoto era rara. Todo el juego iba a pasar dentro del castillo de Ganon, como Mario sesenta y cuatro dentro del castillo de Peach, saltando a otras aventuras a través de puertas y cuadros.",
        "Y pensó en hacerlo en primera persona, para lucir la gran llanura de Hyrule. [short pause] Lo descartó cuando decidieron que también habría un Link niño, porque sentía que a Link había que verlo en pantalla.",
        "[impressed] El problema más difícil fue pelear. ¿Cómo apuntas con una espada a un enemigo que se mueve a tu alrededor?",
        "Parte de la respuesta salió de un parque temático. En los estudios Toei de Kioto, el equipo vio un espectáculo de ninjas donde los enemigos rodeaban al héroe, pero atacaban de uno en uno.",
        "[excited] Así quedó el fijado con el gatillo Z. Apuntas, la cámara se centra en el enemigo, y los demás esperan su turno. Desde entonces, muchísimos juegos de acción en tercera persona lo han copiado.",
        "Al principio se pensó para un lector de discos de la consola, pero acabó en cartucho, y llegó en noviembre de mil novecientos noventa y ocho. Doscientos cincuenta y seis megabits, el juego más grande que Nintendo había hecho.",
        "[impressed] Y entonces llovieron las notas. Fue el primer juego con un cuarenta sobre cuarenta en la revista japonesa Famitsu, y todavía hoy es el único con un noventa y nueve en Metacritic.",
        "Vendió siete millones seiscientas mil copias en Nintendo sesenta y cuatro. [short pause] No estaba mal para un juego de un niño con una flauta.",
    ]},
    {"id": "lore", "frases": [
        "[serious] Ahora, la historia. Link vive en el bosque de los Kokiri, unos niños que nunca crecen y que tienen cada uno su hada. [sad] Todos menos él.",
        "Hasta que el Gran Árbol Deku, el guardián del bosque, le manda una, Navi, y le pide ayuda. [short pause] Un hombre del desierto le ha echado una maldición.",
        "[grim] Link rompe la maldición, pero llega tarde. El árbol le cuenta que ese hombre es Ganondorf, el rey de los Gerudo, y muere delante de él.",
        "[curious] En el castillo de Hyrule, la princesa Zelda le cuenta su sueño. Ganondorf busca la Trifuerza, el poder de los dioses, y para abrir su puerta hacen falta tres piedras espirituales y la Ocarina del Tiempo.",
        "[tense] Link las consigue, abre la puerta del Templo del Tiempo, y saca la Espada Maestra. [whispers] Y ese es justo el error.",
        "Ganondorf lo había seguido. Con la puerta abierta, entra al Reino Sagrado y toma la Trifuerza. Link era demasiado joven para la espada, y queda dormido durante siete años.",
        "[ominous] Cuando despierta, ya es adulto, y Hyrule es otro. El castillo es una fortaleza oscura, el pueblo está en ruinas, y los templos están malditos.",
        "Un misterioso guerrero sheikah, Sheik, le enseña canciones para viajar entre templos y despertar a los seis sabios. [short pause] Y al final se revela que Sheik era Zelda, escondida todo ese tiempo.",
        "[dramatic] Juntos sellan a Ganon, y Zelda devuelve a Link a su infancia con la ocarina. [mysterious] Un final que, como verás en el número uno, partió la historia de Zelda en tres. [excited] Vamos con los secretos.",
    ]},
    {"id": "p12", "frases": [
        "[excited] Número doce. [short pause] Una vaca en tu casa.",
        "En el Rancho Lon Lon, de adulto, Malon te reta a una carrera de obstáculos a caballo. Hay que dar la vuelta saltando vallas en menos de cincuenta segundos.",
        "Si lo consigues, el premio es raro. [short pause] Te regalan una vaca, [laughs] y no te la dan en mano.",
        "Vuelves al bosque Kokiri, entras en la casita del árbol donde Link se despertó al principio del juego, y ahí está. Una vaca, dentro de la casa, [amused] mirando a la pared.",
        "[playful] Si le tocas la canción de Epona, te da leche. Es la única recompensa del juego que se queda a vivir contigo.",
    ]},
    {"id": "p11", "frases": [
        "[playful] En el once, el pescador calvo.",
        "Junto al lago Hylia hay un estanque de pesca, y su dueño lleva siempre un sombrero de paja. [short pause] Lo que no sabías es por qué.",
        "[mischievously] Si vas de adulto y lanzas el anzuelo hacia él, con buena puntería, se lo enganchas y se lo quitas.",
        "Y debajo no hay nada. [laughs] Está completamente calvo. Te regaña, y si se lo vuelves a quitar, te vuelve a regañar.",
        "[amused] Un detalle que alguien en Nintendo programó a propósito, sabiendo que casi nadie iba a lanzarle un anzuelo a la cabeza al pescador.",
    ]},
    {"id": "p10", "frases": [
        "[excited] Número diez. Un cameo que muchos se perdieron, en el patio del castillo.",
        "Cuando encuentras a Zelda de niña, está espiando a Ganondorf por una ventana. [short pause] Pero hay otras ventanas en ese patio.",
        "[curious] Si te asomas a una de ellas, verás unos cuadros colgados. Son Mario, Luigi, la princesa Peach, Bowser y Yoshi.",
        "Si le disparas a esa ventana con el tirachinas, [short pause] alguien de dentro te tira una rupia roja. [mischievously] Pero si le disparas a la otra ventana, sale un soldado, te regaña, [laughs] y te lanza una bomba.",
        "[amused] Y en la versión de tres de ese, la ventana de Mario ya no tiene cuadros. Ahora enseña un nivel de Super Mario Bros.",
    ]},
    {"id": "p9", "frases": [
        "[playful] En el nueve, las piedras chismosas.",
        "Por todo Hyrule hay unas piedras grises con un ojo, las piedras Sheikah. Si te pones la Máscara de la Verdad, te cuentan rumores y pistas.",
        "Si les pegas con la espada, te dicen la hora del día. [short pause] Útil, pero poco más.",
        "[excited] Pero si les pones una bomba, despegan. [laughs] Salen disparadas al cielo como un cohete.",
        "Y hay más. Si les tocas la canción de la tormenta, algunas sueltan un hada. [whispers] Cada piedra de Hyrule esconde algo, si sabes cómo preguntarle.",
    ]},
    {"id": "p8", "frases": [
        "[mysterious] Número ocho. La casa maldita de Kakariko.",
        "En la aldea hay una casa con la puerta cerrada de noche. Dentro vive una familia entera convertida en arañas doradas, por culpa de su propia codicia.",
        "[serious] Por todo el juego hay cien Skulltulas doradas escondidas. Cada una que destruyes devuelve a un miembro de la familia a su forma humana.",
        "Cada diez te dan un premio. Una cartera más grande, la piedra de la agonía, otra cartera todavía mayor, bombchus y una pieza de corazón.",
        "[sarcastic] Y por las cien, el premio final es una rupia enorme de doscientas. [short pause] Que puedes volver a pedir cada vez que entras. [laughs] Para cuando la consigues, ya no tienes nada que comprar.",
    ]},
    {"id": "p7", "frases": [
        "[excited] Número siete. La cadena más larga del juego.",
        "La mejor espada de Ocarina no está en un cofre. Hay que ganarla con un intercambio de objetos que cruza todo el mapa.",
        "Empieza con un huevo de bolsillo que se convierte en un pollo, sigue con una seta mágica, una poción, una sierra, una espada rota, un frasco de colirio, y termina con un resguardo.",
        "[tense] Y algunos tienen el tiempo contado. La seta y el colirio se echan a perder en unos minutos, así que hay que cruzar Hyrule corriendo.",
        "[amused] Al final, Biggoron, un goron del tamaño de una montaña, te forja la espada. [short pause] Pero tarda tres días. [chuckles] O tocas seis veces la canción del Sol, para que pasen más rápido.",
        "[impressed] El premio es la espada de Biggoron, de dos manos, mucho más fuerte que la Espada Maestra. [short pause] Y a diferencia de la espada de los gigantes, que se rompe, esta no se rompe nunca.",
    ]},
    {"id": "p6", "frases": [
        "[sighs] En el seis, el templo más odiado de la historia de Zelda.",
        "El Templo del Agua tiene un nivel de agua que subes y bajas tocando la canción de Zelda en puntos concretos. [short pause] Y si te equivocas, toca volver atrás.",
        "Pero lo que de verdad desesperaba eran las botas de hierro. Para hundirte, te las ponías. Para salir, te las quitabas. Y cada vez, había que abrir el menú.",
        "[sarcastic] Ponte las botas, menú, quítate las botas, menú, y así decenas de veces en una sola mazmorra.",
        "[serious] Eiji Aonuma, el que la diseñó, pidió perdón en público en dos mil nueve. Dijo que lo que más lamentaba era lo difícil que era ponerse y quitarse esas botas, y que debió hacerlo mucho más fácil.",
        "[amused] Y lo arregló. En la versión de tres de ese, las botas de hierro pasaron a un botón. [short pause] Diez años cargando con un templo, y la solución era un botón.",
    ]},
    {"id": "p5", "frases": [
        "[curious] Número cinco. El juego que cambió en silencio.",
        "Ocarina of Time tiene varias versiones del cartucho, y no todas son iguales. Nintendo fue cambiando cosas sin avisar.",
        "En las primeras copias, la música del Templo del Fuego tenía un canto de voces. [short pause] Era un fragmento de la llamada islámica a la oración, sacado de una biblioteca de sonidos comercial.",
        "[serious] En la versión uno punto dos del cartucho, el canto desapareció. Y en esa misma versión cambió otra cosa. [ominous] En la pelea final, la sangre que escupe Ganondorf era roja. [short pause] Desde entonces, es verde.",
        "Y cuando el juego llegó a GameCube, Nintendo cambió también el símbolo de los Gerudo, una luna y una estrella, que estaba en el escudo espejo, en los interruptores y en los bloques del tiempo.",
        "[whispers] Así que, si tienes un cartucho de los primeros, tienes un Ocarina que Nintendo ya no quiso volver a vender.",
    ]},
    {"id": "p4", "frases": [
        "[mysterious] En el cuatro, el Zelda que iba a salir en un disco.",
        "Nintendo preparaba un accesorio para la Nintendo sesenta y cuatro, el sesenta y cuatro de de, una unidad de discos magnéticos que se conectaba debajo de la consola.",
        "Ocarina of Time se pensó en un principio para ese formato, pero el disco no leía los datos lo bastante rápido, y pasó al cartucho. Para el disco se planeó otra cosa, una expansión con las mazmorras rehechas. [short pause] Su nombre era Ura Zelda.",
        "[sighs] El sesenta y cuatro de de fue un fracaso, y casi no salió de Japón. La expansión se quedó guardada.",
        "[curious] Y aquí viene lo mejor. Miyamoto le dio a Eiji Aonuma a elegir. O terminaba Ura Zelda, o hacía un juego nuevo en un solo año, con lo que ya tenían de Ocarina. [short pause] Eligió lo segundo, y así nació Majora's Mask.",
        "[excited] Pero Ura Zelda no se perdió. En dos mil dos volvió como Master Quest, en GameCube, con las mazmorras cambiadas por completo. [chuckles] Y se regalaba al reservar The Wind Waker.",
    ]},
    {"id": "p3", "frases": [
        "[curious] Número tres. La ocarina de cinco notas.",
        "El mando de Nintendo sesenta y cuatro solo tenía cinco botones libres para tocar. El A y los cuatro botones C. [short pause] Así que la ocarina tiene cinco notas.",
        "Koji Kondo tuvo que componer con eso doce melodías. La de Saria, la de Epona, la nana de Zelda, la del Sol, la del Tiempo, y las de los templos. [short pause] Él mismo contó que con solo cinco notas fue difícil componer.",
        "[impressed] Y tenían que ser cortas, para que pudieras tocarlas tú, pero lo bastante buenas para que se te quedaran pegadas veinticinco años.",
        "[warm] Por eso la canción de Saria suena en cualquier sitio, y por eso alguien que no ha jugado nunca reconoce la nana de Zelda. [short pause] Cinco notas, y salió una de las bandas sonoras más famosas de la historia.",
    ]},
    {"id": "p2", "frases": [
        "[mysterious] Número dos. La canción que no compuso nadie.",
        "De adulto, en el molino de Kakariko, hay un hombre que toca un organillo. Está furioso. [short pause] Dice que hace siete años un niño con una ocarina tocó una canción, y desde entonces su molino gira sin control y el pozo se secó.",
        "Te enseña esa canción, la canción de la tormenta, para que no se te olvide quién tiene la culpa.",
        "[curious] Entonces vuelves al pasado con la Espada Maestra, entras al molino de niño, y se la tocas. [short pause] El molino se dispara, el pozo se seca, [whispers] y el hombre aprende la canción de ti.",
        "[intrigued] Él te la enseña porque tú se la tocaste, y tú se la tocaste porque él te la enseñó. [short pause] Nadie la compuso. La canción existe solo porque Link viajó en el tiempo.",
        "[amused] Es una paradoja de libro, metida en un juego de Nintendo sesenta y cuatro. Y es el único sitio donde el juego te hace culpable de algo que todavía no habías hecho.",
    ]},
    {"id": "p1", "frases": [
        "[dramatic] Y llegamos al número uno. El final que partió la historia de Zelda en tres.",
        "¿Recuerdas que, al final, Zelda devuelve a Link a su infancia? [short pause] Durante años, los fans discutieron qué significaba eso.",
        "Porque Hyrule seguía existiendo en el futuro, sin su héroe. Y en el pasado, Link volvía con todo lo que sabía.",
        "[serious] En dos mil once, Nintendo publicó en Japón el libro Hyrule Historia, y lo confirmó. El final de Ocarina of Time divide la cronología en tres líneas.",
        "[curious] En una, Link adulto se va, y Hyrule queda sin héroe. Esa lleva a The Wind Waker, con el reino bajo el mar. En otra, Link niño avisa del peligro, y de ahí salen Majora's Mask y Twilight Princess.",
        "[ominous] Y hay una tercera, la más rara. La línea en la que Link pierde contra Ganon. De ahí salen A Link to the Past y el primer Zelda.",
        "[impressed] Así que casi toda la saga, de un modo u otro, sale de este juego.",
        "[warm] Y el cinco de noviembre, el remake de Nintendo Switch 2 vuelve justo a ese punto de partida. [short pause] La historia de la que salió todo lo demás.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Esos son los doce secretos de Ocarina of Time. Una vaca en casa, un pescador calvo, un canto borrado en silencio, y una canción que nadie compuso.",
        "[thoughtful] Es el juego que enseñó a pelear con espada en tres dimensiones, y que todavía hoy marca cómo se cuenta una aventura.",
        "[curious] ¿Tú conocías la paradoja de la canción de la tormenta? ¿O tenías uno de esos cartuchos con el canto del Templo del Fuego? Cuéntamelo en los comentarios.",
        "Y si quieres que hagamos lo mismo con Majora's Mask, o con otro clásico de la Nintendo sesenta y cuatro, déjalo también abajo. [warm] Nos vemos en la próxima crónica.",
    ]},
]
