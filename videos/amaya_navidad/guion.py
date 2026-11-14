# -*- coding: utf-8 -*-
"""CANAL DE AMAYA (etiqueta `canal_amaya`, alta 10-nov-2026) — 1.er video: las MEJORES y las PEORES cosas que pedir en Navidad.
HORIZONTAL 16:9, ~8-9 min + Short. Público: chicas de 11-15 años (preadolescentes y adolescentes) en México.

ESTILO «SCRAPBOOK COQUETTE» (referencias que eligió Amaya, canales/referencias/amaya/):
  - ref1 (WhatsApp, plantilla «Welcome to my vlog»): vichy rosa/crema, letras recortadas de revista (nota de rescate) que caen
    una por una, papel rasgado y recorte de periódico en las esquinas, cerezas con moño, sticker de gatito con gorro de fresa,
    megáfono, barras de color de TV como transición.
  - ref2 (TikTok digi.dots, 1,2 M vistas): rayas rosa pastel, stickers de productos DIBUJADOS A MANO (contorno fino, sombreado
    suave, contorno blanco de sticker) que caen en montón y se acomodan; «SUBSCRIBE» en contorno + cursor que da clic; pantalla
    final «Thanks For Watching!» con dos recuadros de video y botón rosa.
  → Kit `nucleo/coquette.py` (por código) + stickers de productos de FLOW con ese estilo (hojas de stickers recortadas con
    pegaflow.recortar_hoja). Doc: docs/estilo_scrapbook_coquette.md.

FORMATO: lista doble intercalada, 15 MEJORES (sello verde «¡SÍ PÍDELO!») y 10 PEORES (sello rojo «NI SE TE OCURRA»), cada una con
etiqueta de precio $ / $$ / $$$ y su número en letras recortadas. Termina con la peor n.º 1 y la mejor n.º 1.

Datos (10-nov-2026, guías de regalos 2026: greenweddingshoes, momgenerations, wishdeck, coppel.com/blog): lo más pedido por chicas
de esta edad = squishies/NeeDoh, Jellycat (Bartholomew Bear), botellas Owala/Stanley, bálsamos y tintas de labios, body mists,
Instax Mini, bolsas con charms, pinzas y scrunchies, pantuflas peluditas, audífonos, Switch. Retinol/antiedad a los 12 = la
Academia Americana de Dermatología dice que la piel joven no lo necesita y puede irritarse. Mascotas: los refugios piden que un
animal no sea regalo sorpresa. Humor (memoria chistes-para-ninos): pocos chistes, de observación, sin memes dudosos (el «6-7» es
de 2025 y el «¿y sí sí?» del Mundial ya pasó → no se usan).
"""

TITULO = "Las MEJORES y las PEORES cosas que pedir en Navidad 🎀 (15 sí y 10 NO)"
ARCHIVO = "amaya_navidad"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit nucleo/coquette.py)
DURACION = None
BPM = 200
GAP = 0.28
FPS = 30
VOZ = dict(motor="elevenlabs", voice_id="9Godp7dNohUvXk6qp0gS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-22.0, sfx=-22.0, fx=-10.0)
SUBTITULOS = False
ALIAS_QA = {}
# Whisper oye mal la marca NeeDoh, «le hiciste», «Hay de» y «Esos»: al oído están bien
CER_MAX_POR_FRASE = {"cierre_1": 0.03, "m15_0": 0.07, "m13_1": 0.02, "m11_2": 0.07, "p1_2": 0.04}
TAIL_MAX_POR_FRASE = {"p10_1": 1.3, "cierre_1": 1.4}
MUSICA = {}
# carácter pedido por Amaya: «Coquette playlist» (Valentine) SOLO como referencia de ambiente; provisional del avance = biblioteca
LYRIA = dict(
    estilo="Sweet coquette bedroom-pop for a teen girl's Christmas wishlist: soft felt piano, music box, light pizzicato strings, "
           "gentle sleigh bells, brushed snaps and a warm lo-fi beat; cute, dreamy, playful, never loud; instrumental only, no vocals.",
    escenas={
        "gancho": ("music box intro that blooms into a bouncy beat with sleigh bells, cheerful hello", 6),
        "bienvenida": ("bright happy groove, playful pizzicato, a little sparkle on every stamp", 6),
        "m15": ("light bouncy groove, squishy playful plucks", 5), "m14": ("same groove, sweet piano melody", 5),
        "p10": ("a cheeky detuned music box, gentle comic doubt", 4), "m13": ("crafty happy pizzicato, glockenspiel", 5),
        "m12": ("fresh new-year sparkle, upbeat piano", 5), "p9": ("comic deadpan bass plucks, awkward pause", 4),
        "m11": ("dreamy soft pads, vanilla-sweet bells", 4), "m10": ("warm sunset lo-fi, mellow and cozy", 4),
        "p8": ("silly broken toy piano, comic", 4), "m9": ("cozy winter, fireplace-warm piano and sleigh bells", 4),
        "p7": ("comic oversized tuba-like plucks then tiny celesta", 4), "m8": ("bouncy pop beat, playful snaps", 6),
        "m7": ("cute jingly charms, light glockenspiel groove", 5), "p6": ("toy-box nostalgia, slightly sad and funny", 3),
        "m6": ("glossy sweet pop, soft shimmer", 5), "p5": ("old-fashioned grandma waltz, comic", 4),
        "suscribe": ("happy uplifting break, bell sparkle, a little build of suspense at the end", 6),
        "m5": ("fresh light groove", 5), "p4": ("tinny cheap-sounding comic plucks", 4), "m4": ("soft cuddly lullaby piano", 3),
        "p3": ("gentle and sincere, warm strings, calm", 3), "m3": ("fun family game night bounce", 6),
        "p2": ("calm clean piano, sincere advice", 3), "m2": ("stylish chill beat, a little bigger", 6),
        "p1": ("comic sad trombone-like plucks then festive sleigh bells", 5),
        "m1": ("the biggest, most joyful moment: full sweet pop with bells and claps", 8),
        "cierre": ("warm happy goodbye, music box melody returns, gentle final note", 5),
    },
    tramos=[
        (["gancho", "bienvenida", "m15", "m14", "p10", "m13", "m12", "p9", "m11"],
         "Begin from a delicate music box alone, then the beat comes in. End softly on a held chord."),
        (["m10", "p8", "m9", "p7", "m8"], "Begin softly and warm. End on a gentle held chord."),
        (["m7", "p6", "m6", "p5"], "Begin cute and light. End on a gentle held chord."),
        (["suscribe", "m5", "p4", "m4", "p3"], "Begin bright and happy. End calm and tender on a held chord."),
        (["m3", "p2", "m2", "p1", "m1", "cierre"], "Begin with a playful bounce, build to the biggest joyful moment, then a sweet music box "
         "ending with a clean final note."),
    ],
)
TRANSICIONES = [("continua", 0.3)] * 29   # plano secuencia: los cambios los dibuja escenas.py

# id → (tipo, número, precio, nombre en pantalla). tipo: "m" mejor · "p" peor
LISTA = {
    "m15": ("m", 15, "$", "SQUISHY ANTIESTRÉS"),
    "m14": ("m", 14, "$", "PINZAS Y SCRUNCHIES"),
    "p10": ("p", 10, "$", "DIARIO CON CANDADO"),
    "m13": ("m", 13, "$", "KIT DE PULSERAS"),
    "m12": ("m", 12, "$$", "BLOQUEADOR + CREMA"),
    "p9": ("p", 9, "$$", "TINTES DE FANTASÍA"),
    "m11": ("m", 11, "$$", "BODY MIST"),
    "m10": ("m", 10, "$$", "PRODUCTOS PARA EL CABELLO"),
    "p8": ("p", 8, "$", "MAQUILLAJE MUY CARGADO"),
    "m9": ("m", 9, "$$", "PANTUFLAS PELUDITAS"),
    "p7": ("p", 7, "$$", "ROPA SIN PREGUNTAR LA TALLA"),
    "m8": ("m", 8, "$", "KIT DE EMERGENCIA"),
    "m7": ("m", 7, "$$", "BOLSA O MOCHILA + CHARMS"),
    "p6": ("p", 6, "$", "JUGUETES DE CUANDO TENÍAS 7"),
    "m6": ("m", 6, "$", "BÁLSAMO CON COLOR"),
    "p5": ("p", 5, "$", "SET DE BAÑO DE CANASTA"),
    "m5": ("m", 5, "$$", "TERMO BONITO"),
    "p4": ("p", 4, "$", "AUDÍFONOS PIRATA"),
    "m4": ("m", 4, "$$", "PELUCHE SUAVECITO"),
    "p3": ("p", 3, "$$$", "UNA MASCOTA SORPRESA"),
    "m3": ("m", 3, "$$$", "UN JUEGO PARA JUGAR EN FAMILIA"),
    "p2": ("p", 2, "$$$", "SKINCARE DE ADULTOS"),
    "m2": ("m", 2, "$$$", "AUDÍFONOS DE DIADEMA"),
    "p1": ("p", 1, "$", "CALCETINES BLANCOS DE PAQUETE"),
    "m1": ("m", 1, "$$$", "CÁMARA INSTANTÁNEA"),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.4, "frases": [
        "¡Hola, hola! Soy Amaya. [short pause] Ya casi es Navidad, y si este año no quieres que te vuelvan a regalar calcetines... [laughs] quédate.",
        "Hoy te traigo las quince mejores cosas que puedes pedir, y las diez peores. Las que, neta, ni se te ocurra poner en tu carta.",
        "Y ojo, porque una de las peores... seguro ya la tienes en tu cajón.",
    ]},
    {"id": "bienvenida", "frases": [
        "¡Bienvenida a Amaya Vibes! Así funciona: si sale el sello verde, ¡sí pídelo! Si sale el rojo, ni se te ocurra.",
        "Y los signos de pesos te dicen qué tan caro es: uno es barato, tres es de los que se piden con mucho cariño. [laughs]",
    ]},
    {"id": "m15", "frases": [
        "Mejor número quince: un squishy antiestrés, como los NeeDoh.",
        "Lo aplastas, lo estiras, y regresa a su forma. Perfecto para cuando estás haciendo tarea y ya no puedes más.",
        "Es barato, cabe en la mochila, y es el regalo que más guardan las chicas en sus listas este año.",
    ]},
    {"id": "m14", "frases": [
        "Mejor número catorce: pinzas de pelo y scrunchies.",
        "Una pinza grande de carey te arregla el peinado en tres segundos. Y los scrunchies no te maltratan el pelo como las ligas.",
        "Pide un set: así tienes uno para la escuela, uno para la casa, y uno que vas a perder. [laughs]",
    ]},
    {"id": "p10", "frases": [
        "Peor número diez: el diario con candadito.",
        "Se ve súper tierno... hasta que descubres que el candado se abre con un clip. O con nada.",
        "Si quieres escribir tus secretos, mejor pide una libreta bonita y guárdala donde nadie busque.",
    ]},
    {"id": "m13", "frases": [
        "Mejor número trece: un kit de cuentas para hacer pulseras.",
        "Haces una para ti, una para tu mejor amiga, y de repente ya le hiciste a todo el salón.",
        "Es barato, es creativo, y lo puedes usar en las vacaciones cuando no hay nada que hacer.",
    ]},
    {"id": "m12", "frases": [
        "Mejor número doce: bloqueador solar, con color o normal, y una crema para el cuerpo y la cara.",
        "Esta la puse yo porque es lo que más uso: el bloqueador te cuida del sol hasta en invierno, y la crema te deja la piel suavecita.",
        "Y no es aburrido: hay bloqueadores con color que se ven naturales, y cremas que huelen riquísimo.",
    ]},
    {"id": "p9", "frases": [
        "Peor número nueve: tintes de fantasía, y productos que dañan el cabello.",
        "Este lo escogí yo: el pelo rosa o azul se ve increíble en fotos, pero la decoloración lo reseca y lo quiebra, y la piel se puede irritar.",
        "Si quieres color, mejor unos clips de colores, o un gis para el pelo que se quita al lavarlo.",
    ]},
    {"id": "m11", "frases": [
        "Mejor número once: un body mist.",
        "Es como un perfume, pero más ligerito. Te lo echas en la mañana y hueles a vainilla o a fresa todo el día.",
        "Hay de todos los precios, y es de esos regalos que se ven bonitos hasta en tu tocador.",
    ]},
    {"id": "m10", "frases": [
        "Mejor número diez: productos para el cabello.",
        "Esta también es de mi lista: un cepillo que desenreda sin jalar, una crema para peinar, y un aceite que deja el pelo brillosito.",
        "Tu pelo te lo va a agradecer, y te peinas en la mitad del tiempo.",
    ]},
    {"id": "p8", "frases": [
        "Peor número ocho, y esta la puse yo: el maquillaje muy cargado, como la paleta gigante de doscientos colores.",
        "Se ve increíble en la caja. Pero los colores casi no pintan, se rompen, dan comezón, y hasta te pueden hacer daño en la piel.",
        "Mejor tres cosas buenas que doscientas que no sirven. Menos, pero bonito.",
    ]},
    {"id": "m9", "frases": [
        "Mejor número nueve: pantuflas peluditas.",
        "En diciembre hace frío, y no hay nada mejor que llegar de la escuela y meter los pies en una nube.",
        "Y de pilón: se ven lindísimas con la pijama, y con un chocolate caliente.",
    ]},
    {"id": "p7", "frases": [
        "Peor número siete: ropa que alguien escogió sin preguntarte la talla.",
        "Abres la caja y es una sudadera que te queda de casa de campaña. O tan chiquita que parece de tu muñeca.",
        "Si te van a regalar ropa, que te pregunten la talla. O mejor, que vayan contigo, y escojas ropa de tu mayor gusto. Esa sí está en mi lista.",
    ]},
    {"id": "m8", "frases": [
        "Mejor número ocho: un kit de emergencia para la escuela.",
        "Lo puse yo en mi lista: una bolsita con curitas, toallitas, desodorante, gel antibacterial, ligas y un bálsamo.",
        "No parece gran cosa... hasta el día que te salva. Y tus amigas te van a pedir de todo. [laughs]",
    ]},
    {"id": "m7", "frases": [
        "Mejor número siete, de mi lista: una bolsa cruzada o una mochila, con charms.",
        "Los charms son los llaveritos que se cuelgan de la bolsa o de la mochila: un osito, una fresa, una estrella.",
        "La bolsa es el regalo, y los charms son la parte divertida: los vas juntando, y cada uno tiene su historia.",
    ]},
    {"id": "p6", "frases": [
        "Peor número seis: los juguetes de cuando tenías siete años.",
        "Tu tía todavía te ve como de primero de primaria, y te regala una muñeca que llora. [sighs]",
        "No es su culpa: hay que ayudarle. Mándale tu lista. Literal, para eso existe la carta.",
    ]},
    {"id": "m6", "frases": [
        "Mejor número seis, también de mi lista: un bálsamo de labios con color.",
        "Hidrata, se ve brillosito, y es el maquillaje perfecto para nuestra edad: natural y sin exagerar.",
        "Es barato, y es de esas cosas que usas todos los días.",
    ]},
    {"id": "p5", "frases": [
        "Peor número cinco: el set de baño de canasta.",
        "Ya sabes cuál: un jabón, una esponja, un gel que huele a abuelita, y mucho, mucho plástico.",
        "Es el regalo de «no supe qué darte», y siempre llega con un moño gigante. Ojo: los productos de higiene que tú escoges sí valen. Lo malo es la canasta genérica.",
    ]},
    {"id": "suscribe", "frases": [
        "Antes de seguir: si ya llevas tu lista, ¡suscríbete! Es gratis, y cada semana traemos listas nuevas.",
        "Faltan las mejores... y las peores. La peor número uno, te lo prometo, la tienes en casa.",
    ]},
    {"id": "m5", "frases": [
        "Mejor número cinco: un termo bonito para el agua.",
        "Los de popote que no se derraman son los favoritos. Te lo llevas a la escuela y te acuerdas de tomar agua.",
        "Y como todas lo traen, ponle stickers o un charm, para que nadie se lleve el tuyo por accidente.",
    ]},
    {"id": "p4", "frases": [
        "Peor número cuatro: audífonos pirata del tianguis.",
        "Se ven igualitos a los originales, pero suenan como lata, y la batería dura dos semanas.",
        "Mejor unos sencillos, de una marca que exista. Barato no siempre es barato.",
    ]},
    {"id": "m4", "frases": [
        "Mejor número cuatro: un peluche suavecito, como los de Jellycat.",
        "Sí, ya no somos niñas chiquitas. Pero un osito suave en la cama nunca pasa de moda.",
        "Hay hasta de comida con carita: un croissant, un aguacate, una fresa. Y se ven preciosos en el cuarto.",
    ]},
    {"id": "p3", "frases": [
        "Peor número tres: una mascota sorpresa.",
        "Un perrito con moño suena a película. Pero un animal no es un juguete: come, se enferma, y vive muchos años.",
        "Si quieres una mascota, platícalo con tu familia y decidan juntos. Así sí. Pero sorpresa, no.",
    ]},
    {"id": "m3", "frases": [
        "Mejor número tres: un juego para jugar en familia.",
        "Si en tu casa ya hay consola, un juego como Mario Kart hace que hasta tu papá quiera jugar. Y pierda. [laughs]",
        "Y si no hay consola, un juego de mesa también cuenta. Lo importante es jugar con tu gente en vacaciones.",
    ]},
    {"id": "p2", "frases": [
        "Peor número dos, y esta también es de mi lista: el skincare de adultos, como cremas antiedad y sérums con retinol.",
        "Están de moda en internet, pero los dermatólogos lo dicen clarito: la piel a nuestra edad no las necesita, y se puede irritar.",
        "Tu piel solo necesita tres cosas: lavarla, ponerle crema hidratante, y bloqueador. Ya. Así de fácil.",
    ]},
    {"id": "m2", "frases": [
        "Mejor número dos: unos audífonos de diadema.",
        "Son la tendencia: se ven increíbles con cualquier outfit, y aíslan el ruido para escuchar música o estudiar.",
        "Son de los caros. Así que este va arriba en la carta, con letra bonita, y con mucho cariño. [laughs]",
    ]},
    {"id": "p1", "frases": [
        "Y la peor número uno: calcetines blancos de paquete.",
        "Te lo dije: ya los tienes en tu cajón. Son útiles, sí, pero como regalo de Navidad, son la tristeza.",
        "La única excepción: calcetines navideños chistosos. Esos sí. Esos son arte.",
    ]},
    {"id": "m1", "frases": [
        "Y la mejor número uno: una cámara instantánea.",
        "Tomas la foto, y en unos segundos sale impresa. Para tus amigas, para tu pared, para tu agenda.",
        "Un consejo: pide también rollos de película, porque las fotos se acaban rapidísimo. Y créeme, vas a querer más.",
    ]},
    {"id": "cierre", "post": 3.0, "frases": [
        "Y esa es la lista. Ahora dime en los comentarios: ¿cuál vas a poner en tu carta? ¿Y cuál es el peor regalo que te han dado?",
        "Esas solo son algunas de las mejores y peores cosas. ¡Espero les guste! Dale like y suscríbete. Soy Amaya, ¡y nos vemos en la próxima lista! Byeee.",
    ]},
]
