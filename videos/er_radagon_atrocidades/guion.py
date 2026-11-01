# -*- coding: utf-8 -*-
"""Runa Caída — primer video del canal hecho en la Fábrica (14-oct-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat, docs/estilo_secuencia_yt.md) con voz Chatterbox «Faraon»
(la eligió el usuario el 14-oct). Sin patrocinio. Fórmula: canales/formula/runa_caida.md (repite el ×24,6 de
«Las 5 peores atrocidades de Márika QUE IGNORASTE», 5:54, cambiando UNA variable: Márika → Radagon; ~6 min).
Guion con la «gema» del canal (lista TOP, humor absurdo, moraleja final, puente al video de Márika).
No repite lo que ya contó el de Márika (exilio de los Sinluz, gigantes de fuego, Morgott y Mohg, Cornudos, Noche de
los Cuchillos Negros). Datos verificados en eldenring.wiki.fextralife.com el 14-oct-2026: Radagon of the Golden Order
(Miriel), Rennala Queen of the Full Moon (Gideon: el huevo de ámbar se lo dio Radagon; Queen's Robe/Crown), Great Rune of
the Unborn, Golden Order Greatsword, Giant's Red Braid, Radahn's Redmane Helm, Remembrance of the Rot Goddess,
Malenia's Great Rune, Radagon's Rings of Light, Law of Regression (estatua de Leyndell), Marika's Hammer, Red Wolf of Radagon.
"""

TITULO = "Las 5 peores atrocidades de Radagon QUE IGNORASTE"
ARCHIVO = "er_radagon_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube
FONETICA = {
    "Radagon": "Rádagon", "Rennala": "Renála", "Radahn": "Rádan", "Ranni": "Ráni", "Godfrey": "Gódfri",
    "Leyndell": "Léindel", "Liurnia": "Liúrnia", "Raya Lucaria": "Ráya Lucária", "Caria": "Cária",
    "Malenia": "Malénia", "Miquella": "Mikuéla", "Miriel": "Miriél", "Gideon Ofnir": "Guídeon Ófnir",
    "Elden": "Élden",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    yt=dict(sufijo="Elden Ring", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),
)

# Whisper escribe distinto los nombres que Chatterbox dice bien (Liurmia/Lurnia, renalas); frases largas que hablan hasta
# el final (CER 0 y la transcripción acaba bien): cola más alta. Revisado el 14-oct tras la primera ronda.
CER_MAX_POR_FRASE = {"p2_1": 0.035, "p1_7": 0.012, "intro_2": 0.05}   # intro_2: Whisper escribe «Márica»
TAIL_MAX_POR_FRASE = {"p4_1": 0.50, "p1_1": 0.46, "p1_7": 0.50, "cierre_0": 0.40, "cierre_1": 0.52}

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Dark gothic fantasy orchestral underscore like a melancholic soulslike action RPG soundtrack: solemn low choir, "
           "pipe organ pads, cello and harp, distant bells, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("a golden statue in a silent capital, low choir hum, a single bell, a secret about to be revealed", 6),
        "p5": ("invading army on misty lakes, war drums softened into a strange romance, harp over low brass", 5),
        "p4": ("a sword of light reforged, cold metallic shimmer, sly woodwinds, quiet bitterness", 4),
        "p3": ("cursed twin children, fragile celesta and solo cello, a slow sad lullaby that rots at the edges", 7),
        "p2": ("one god with two faces, dissonant choir split in two, hammer strikes on an anvil, grand and unsettling", 8),
        "p1": ("an abandoned queen in a vast moonlit library, glassy harp, lonely mezzo hum, heartbreak", 9),
        "cierre": ("calm after the storm, warm low strings, a wry final note fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro", "p5", "p4"], "Begin softly from near silence with a low choir hum. End on a sustained low string tone."),
        (["p3", "p2"], "Begin on a sustained low string tone. End on a heavy, unresolved low drone."),
        (["p1", "cierre"], "Begin on a soft lonely harp over a low drone. Swell to a sorrowful peak, then settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En Leyndell, la Capital Real, hay una estatua dorada de un hombre de pelo largo, y a sus pies un mensaje que dice que solo la regresión revela secretos.",
        "Le lanzas el milagro de la Ley de Regresión, la estatua cambia de cara, y aparece otra frase.",
        "Dice que Radagon es Márika.",
        "El rey consorte de las Tierras Intermedias, el marido de la reina, era la reina.",
        "Y aunque suene a lo más gordo que podía esconder, ni siquiera es lo más cruel que hizo.",
        "Así que hoy van las cinco peores atrocidades de Radagon que ignoraste, porque entre tanto jefe con espadas del tamaño de un camión, el pelirrojo tranquilo de la Orden Áurea se salió con la suya.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Antes de ser rey, Radagon fue un invasor.",
        "Llegó a Liurnia de los Lagos al frente de un ejército dorado para someter a la familia real de Caria, y en el campo de batalla se encontró con su reina, Rennala.",
        "Un monumento de esa primera guerra lo presume sin ninguna pena: la gloria de Radagon arde roja como su pelo.",
        "Y luego, según cuenta Miriel, el pastor de los votos, Radagon se arrepintió de sus agresiones territoriales y le juró amor a Rennala, recién lavado con rocío celestial.",
        "Invades el reino de alguien, te das un baño a mitad de la guerra y le propones matrimonio a la dueña. Es la forma más cara de conseguir pareja de la que yo tenga noticia.",
        "Lo que casi nadie conecta es lo del pelo, porque la Trenza roja de gigante dice que todos los gigantes tienen el pelo rojo, y que Radagon despreciaba el suyo.",
        "Quizá era una maldición de su especie, remata el objeto, y ahí lo deja, como quien suelta un chisme y se va.",
        "El hombre odiaba su propio pelo, y aun así se lo heredó a su hijo Radahn, furioso y llameante, según el casco del propio Radahn.",
    ]},
    {"id": "p4", "frases": [
        "Bajamos al cuatro con un arma que a lo mejor tú vendiste sin leer la descripción.",
        "En una cueva perdida de los campos nevados, un malnacido con armadura de cruzado te suelta el Espadón de la Orden Áurea, una espada hecha de luz con la forma del mismísimo Círculo de Elden.",
        "La forjó el propio Radagon, ya como rey consorte, para presumir los principios de la Orden Áurea.",
        "Pero la descripción guarda una línea al final que lo delata todo: hay señales de que antes fue el espadón que le dejó su primera esposa, Rennala.",
        "Su PRIMERA esposa.",
        "Agarró el regalo de la mujer que dejó atrás y lo rehizo como trofeo de su matrimonio nuevo.",
        "Es como llevar el anillo de tu ex al joyero para que le graben el nombre de la nueva, y luego lucirlo en la boda.",
        "Yo la cargué en el inventario como veinte horas, golpeando lobos con ella, sin saber que traía encima un divorcio completo.",
    ]},
    {"id": "p3", "frases": [
        "Hasta aquí, Radagon parece un marido terrible con mala suerte en el pelo. Lo que sigue ya toca a sus hijos.",
        "Número tres, los gemelos.",
        "Malenia y Miquella son hijos de Márika y de Radagon, y el recuerdo de la diosa de la putrefacción lo resume con una frase que da escalofríos: los dos son hijos de un solo dios.",
        "Uno quedó maldito con la infancia eterna. La otra llevaba la putrefacción por dentro.",
        "Un solo dios. Si Radagon es Márika, esos gemelos no tienen papá y mamá, tienen a la misma persona dos veces.",
        "La Gran Runa de Malenia dice que debió ser la más sagrada de todas. Debió.",
        "Radagon le regaló al pequeño Miquella sus Anillos de luz, un milagro de la Orden Áurea, para que creciera en la fe de papá.",
        "Y la descripción de ese mismo milagro lo remata: Miquella abandonó esa fe, porque no podía hacer nada contra la putrefacción maldita de su hermana.",
        "El dios que vino a poner orden en el mundo no pudo ni curar a su propia hija, y le tocó a un niño eterno buscar la solución por su cuenta.",
    ]},
    {"id": "p2", "frases": [
        "Ya en el podio, el dos es la estatua del principio, y aquí se me rompió la cabeza la primera vez que lo entendí.",
        "Mientras Márika estaba casada con Godfrey, el primer Señor del Círculo, el mismo Radagon estaba casado con Rennala en Liurnia.",
        "Cuando Godfrey fue exiliado, Radagon dejó Liurnia, volvió a la capital del Árbol Áureo y se convirtió en el segundo marido de la reina.",
        "O sea, la reina se casó consigo misma. Y durante siglos toda la corte le aplaudió la boda.",
        "Yo pensaba que eran dos amantes que se fueron fundiendo con el tiempo. Bueno, no, lo pensé como dos años, hasta que leí la descripción del martillo de Márika.",
        "Con ese martillo la reina rompió el Círculo de Elden, y con ese mismo martillo Radagon intentó repararlo.",
        "La misma persona, rompiendo y arreglando a la vez, porque las dos mitades no comparten la misma voluntad.",
        "Es pelearte contigo mismo por el control de la tele, solo que la tele es la realidad, y la casa entera se quedó sin luz.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno, el que más duele, y el que casi todos ignoramos por estar esquivando lunas.",
        "En la Gran Biblioteca de Raya Lucaria, la reina Rennala sigue sentada en el centro, rodeada de alumnos que la protegen, abrazando un huevo de ámbar como si fuera un bebé.",
        "Según Gideon Ofnir, el omnisciente, ese huevo fue un regalo de Radagon.",
        "Es lo que le dejó al irse. Un huevo.",
        "Radagon dejó a Rennala para volver a la capital, y con ella se quedaron sus hijos, entre ellos Radahn y Ranni.",
        "Las ropas de la reina lo cuentan así: cuando Rennala perdió a su marido, su corazón se fue con él.",
        "Y entonces, los de la academia se dieron cuenta de que Rennala, al final, no era ninguna campeona.",
        "Desde entonces usa ese huevo para hacer renacer a quien se lo pida, y la Gran Runa de los no nacidos lo dice sin anestesia: todos los que renacen de Rennala son frágiles y de vida corta. Imperfectos, cada uno de ellos.",
        "Y por si fuera poco, en los pasillos de esa misma academia ronda un lobo gigante y rojo que lanza hechizos. Se llama Lobo rojo de Radagon.",
        "El tipo se fue, y dejó a su perro cuidando la casa de la ex.",
        "Mi postura es simple. Invadir un reino es horrible, pero eso por lo menos sale en los mapas.",
        "Lo de Rennala es dejarla viva y hecha pedazos, abrazando lo único que le dejaste, para siempre, sabiendo dónde está.",
        "Un huevo. Le dejó un huevo.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Radagon tiene fama de jefe final elegante, de pelo bonito y martillo dorado, y casi nadie lo pone en la misma frase que Márika. Pues son la misma frase.",
        "Ahora la pregunta incómoda, y quiero saber tu respuesta: cuál de las dos mitades fue peor, la que rompió el mundo o la que dejó a una reina abrazando un huevo.",
        "Y si quieres ver lo que hizo la otra mitad, tienes que ver el video de las cinco peores atrocidades de Márika, que ya está en el canal. Es la misma persona, así que cuenta como segunda parte.",
        "La próxima vez que alguien te regale un huevo al despedirse, no lo abraces durante siglos. Hazte unos huevos revueltos y sigue con tu vida.",
    ]},
]
