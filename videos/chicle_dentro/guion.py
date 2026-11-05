# -*- coding: utf-8 -*-
"""¿Qué pasa DENTRO de tu cuerpo si te tragas un chicle? — largo HORIZONTAL de Kuriox (~6,5 min),
ACUARELA PINTADA A MANO POR CÓDIGO (mismo formato que videos/ia_como_ve/: Kuri + la niña, «¿cómo funciona por dentro?»).

Pedido del usuario (5-nov-2026): «otro video para Kuriox igual al último», tema elegido: el chicle (datos: «¿Qué pasa si te
tragas un chicle? / El viaje dentro de tu cuerpo», Cuerpo en 3D, ×66; mito + objeto cotidiano = goma azul ×58 del canal).
Idea central: la niña se traga el chicle sin querer y alguien le dice «¡siete años!»; Kuri se encoge y viaja montado en la
bolita gris por boca → esófago → estómago (ácido, moco, «la escoba») → intestino delgado → grueso → fuera. Luego, cuándo SÍ es
peligroso (bezoar) y de dónde salió el mito.

Datos (verificados el 5-nov-2026):
  - Mito de los 7 años: falso. La goma base no se digiere pero recorre el tubo digestivo entera y sale en días
    (Nancy McGreal, gastroenteróloga de Duke: «tres días, como mucho»; Yale: 40 h a 7 días; Mayo Clinic; Scientific American 2007).
    Origen desconocido: los médicos creen que lo inventaron los papás para que los niños no se tragaran el chicle (McGreal; Simon Travis, Oxford).
  - Chicle natural = savia (látex) del chicozapote (Manilkara zapota), sureste de México y Centroamérica; se «pica» la corteza
    en zigzag (chicleros). Los mayas lo masticaban; náhuatl «tzictli» → «chicle».
  - Santa Anna, desterrado en Staten Island (Nueva York, h. 1866-1869), quería usar chicle en lugar de hule; Thomas Adams no
    logró vulcanizarlo, notó que Santa Anna lo masticaba y hacia 1869-1871 empezó a vender chicle (Britannica; historia de Mondelez).
  - Goma base moderna (FDA, 21 CFR 172.615): hule butilo, poliisobutileno (cámaras de llanta), acetato de polivinilo (base del
    pegamento blanco), ceras y resinas. Azúcar y sabor se disuelven en la saliva; la goma queda.
  - Esófago ≈ 25 cm; peristalsis (se traga hasta de cabeza). Jugo gástrico: ácido clorhídrico, pH ≈ 1,5-3,5 (limón ≈ 2-2,6);
    pepsina corta proteínas. Moco que recubre el estómago. Complejo motor migratorio: en ayunas, cada ~90-120 min, onda que
    barre los sólidos que no se digieren («housekeeper»). Intestino delgado ≈ 6 m (bilis, páncreas, vellosidades);
    grueso ≈ 1,5 m, billones de bacterias.
  - Milov, Andres, Erhart y Bailey, «Chewing Gum Bezoars of the Gastrointestinal Tract», Pediatrics 102(2):e22 (1998),
    doi:10.1542/peds.102.2.e22 (Crossref ✓): niño de 4 ½ años que se tragaba 5-7 chicles al día, dos años de estreñimiento,
    masa de chicle; niña de 1 ½ años con cuatro monedas en el esófago pegadas con chicle.
"""

TITULO = "¿Qué pasa DENTRO de tu cuerpo si te tragas un chicle? (el mito de los 7 años)"
ARCHIVO = "chicle_dentro"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit propio acuarela.py; docs/estilo_acuarela_pincel.md)
DURACION = None
BPM = 88
GAP = 0.35
FPS = 24                          # la tinta «hierve» a 12 fps (en dos)
# Voz de Kuriox (asteroide_invisible / ia_como_ve). Corchetes suaves: nunca susurros ni excitado.
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-22.0, sfx=-24.0, fx=-9.0)
SUBTITULOS = False
ALIAS_QA = {"curie": "kuri", "glup": "glub"}
CER_MAX_POR_FRASE = {"origen_2": 0.03, "origen_3": 0.02}   # Whisper escribe «sictli» y «Santa Ana»: el audio está bien
MUSICA = {}
TRANSICIONES = [("continua", 0.3)] * 7    # plano secuencia: los cambios los dibuja escenas.py

LYRIA = dict(
    estilo="Gentle hand-made animated documentary score: soft felt piano, warm celesta, music box, marimba, light pizzicato "
           "strings, a squishy bass clarinet for the inside-the-body parts; curious, playful, watercolour storybook feel. "
           "Sparse melody low in the mix so a narrator can speak over it. Instrumental only, no vocals.",
    escenas={
        "gancho": ("Playful and a bit spooky-comic: a music-box 'myth' motif, a gulp, then a curious swell.", 3),
        "origen": ("Warm Mexican-flavoured history: marimba and soft guitar, then an old-time 1870s comic shuffle.", 4),
        "bajada": ("Sliding down: a descending glissando, squishy rhythmic pulses like swallowing waves.", 6),
        "estomago": ("Bubbly and acidic: low pizzicato, fizzing textures, a comic 'nothing happens' beat, then a broom sweep.", 7),
        "intestino": ("Long winding journey: steady walking bassline, gentle wonder, a playful 'goodbye' ending.", 6),
        "peligro": ("Serious but gentle: low strings and soft piano, a little tension, then relief.", 5),
        "cierre": ("Warm, cheeky recap ending on a tender, playful final chord.", 3),
    },
    tramos=[(["gancho", "origen"], "Begin softly from silence. Clear changes of mood at each section boundary."),
            (["bajada", "estomago"], "Continue the same instrumentation. Clear changes of mood at each section boundary."),
            (["intestino", "peligro", "cierre"],
             "Continue the same instrumentation. Clear changes of mood at each section boundary. End on a short playful final chord.")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Seguro alguien te lo dijo de niño: [short pause] si te tragas un chicle, se te queda pegado en el estómago... siete años.",
        "Siete años. Ahí adentro, pegado, mientras tú creces, cumples años y terminas la primaria.",
        "¿Será cierto? [short pause] Vamos a averiguarlo de la mejor manera posible: siguiendo a un chicle por dentro del cuerpo.",
        "Desde que entra por la boca... hasta que sale. [short pause] Sí, por ahí.",
    ]},
    {"id": "origen", "frases": [
        "Pero primero: ¿de qué está hecho un chicle? Porque no es comida, aunque lo parezca.",
        "El original sale de un árbol del sur de México y Centroamérica: el chicozapote. Si le cortas la corteza, suelta una savia blanca y pegajosa.",
        "Los mayas ya la masticaban hace siglos, y los mexicas la llamaban tzictli. De ahí viene la palabra chicle.",
        "Y aquí viene lo raro: el chicle llegó a Estados Unidos gracias a Antonio López de Santa Anna.",
        "Desterrado en Nueva York, quería usarla para hacer hule. El inventor Thomas Adams lo intentó... y fracasó. Pero notó que Santa Anna la masticaba.",
        "Así nació, por mil ochocientos setenta, el chicle de tienda.",
        "Hoy casi ningún chicle lleva savia de árbol: llevan una goma base hecha en fábrica, con parientes del hule de las cámaras de llanta y del pegamento blanco.",
        "El azúcar y el sabor se disuelven en tu saliva en unos minutos. Lo que queda, esa bolita gris sin sabor, es la goma. Y esa es la que te tragaste.",
    ]},
    {"id": "bajada", "frases": [
        "Bien. [short pause] Empieza el viaje.",
        "La lengua empuja la bolita hacia atrás, una tapita llamada epiglotis cierra el camino a los pulmones, y el chicle cae al esófago.",
        "El esófago es un tubo de unos veinticinco centímetros, y no funciona por gravedad: sus músculos se aprietan en ondas, uno tras otro, como cuando exprimes un tubo de pasta de dientes.",
        "Por eso podrías tragar hasta de cabeza. En unos segundos, el chicle llega al estómago.",
    ]},
    {"id": "estomago", "frases": [
        "Y aquí es donde, según el mito, se queda pegado siete años. Veamos.",
        "El estómago es una bolsa de músculo que se llena de jugo gástrico: ácido clorhídrico, tan ácido como el jugo de limón, o más.",
        "Además tiene enzimas, como la pepsina, que cortan las proteínas de la carne en pedacitos.",
        "El estómago aprieta, revuelve y baña todo en ácido durante horas. Un pedazo de pan se deshace. Un bistec se deshace.",
        "¿Y el chicle? [short pause] Nada. Ni el ácido ni las enzimas pueden romper esa goma. Sigue igualito que entró.",
        "Pero tampoco se pega. Las paredes del estómago están cubiertas de una capa de moco resbaloso, y el chicle solo se pega en cosas secas.",
        "Y lo mejor: el estómago tiene su propio servicio de limpieza. Cuando se vacía, cada hora y media o dos horas, manda una onda fuerte que barre hacia afuera todo lo que no pudo deshacer.",
        "Los médicos le llaman complejo motor migratorio. Nosotros le vamos a decir: la escoba. [short pause] Y la escoba se lleva al chicle.",
    ]},
    {"id": "intestino", "frases": [
        "Siguiente parada: el intestino delgado. Un tubo de unos seis metros, todo enroscado en tu panza.",
        "Aquí llegan la bilis y los jugos del páncreas, y unas vellosidades diminutas absorben todo lo que sirve: azúcares, grasas, proteínas.",
        "Al chicle no le pueden sacar nada. Así que sigue avanzando, empujado por las mismas ondas, metro tras metro.",
        "Luego viene el intestino grueso, de metro y medio, donde viven billones de bacterias que se comen lo que tú no pudiste digerir.",
        "Pero tampoco pueden con el chicle. Se junta con todo lo demás que no se digirió, se le quita el agua, y...",
        "unos días después, [short pause] adiós. Sale como cualquier otra cosa que no se digiere. En días, no en siete años.",
    ]},
    {"id": "peligro", "frases": [
        "Entonces, ¿tragarse un chicle no hace nada? Uno solo, no. Pero hay una excepción.",
        "En mil novecientos noventa y ocho, unos médicos de Estados Unidos publicaron casos de niños que sí terminaron en el hospital.",
        "Uno de ellos, de cuatro años y medio, se tragaba entre cinco y siete chicles todos los días, y llevaba dos años estreñido.",
        "Tanta goma junta formó una bola dura que no podía salir. Los médicos le llaman bezoar, y tuvieron que quitársela.",
        "Otra niña, de año y medio, tenía cuatro monedas atoradas en el esófago, pegadas entre sí con chicle.",
        "La lección: un chicle tragado por accidente no pasa nada. Muchos, todos los días, y con otras cosas... ahí sí.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "¿Y de dónde salió lo de los siete años? [short pause] Nadie lo sabe.",
        "Los médicos creen que lo inventaron los papás, para que los niños dejaran de tragarse el chicle. Y funcionó: generaciones enteras con miedo a la bolita gris.",
        "Así que ya lo sabes: si se te va un chicle, tranquilo. Tu estómago tiene escoba, y tu cuerpo sabe sacar lo que no le sirve.",
        "Eso sí: mejor tíralo a la basura, y no debajo de la mesa.",
        "Y si quieres seguir viajando por dentro de las cosas con Kuri, suscríbete. [short pause] El próximo viaje ya se está cocinando.",
    ]},
]
