# -*- coding: utf-8 -*-
"""Plastitube (alias pieza_oculta) — «Los Corn Flakes Nacieron de un ERROR (Y Separaron a Dos Hermanos Para Siempre)».
Motor SECUENCIA. Primer video de la fórmula nueva del canal (canales/formula/pieza_oculta.md, 23-oct-2026): marca con giro humano.
Ficha histórica (Wikipedia «Corn flakes» y «Kellogg's»; NPR/Fresh Air 8-ago-2017 con Howard Markel, «The Kelloggs: The Battling
Brothers of Battle Creek»; WOOD-TV y Entrepreneur sobre W. K. Kellogg; anuncios de 1907 en Michigan Tradesman (MSU); El Universal,
Forbes México y Expansión sobre Kellogg's en México):
John Harvey Kellogg (1852-1943), médico adventista, director del Sanatorio de Battle Creek (Michigan): «vida biológica», sin carne,
sin alcohol ni cafeína; escribió contra «el vicio solitario» y creía que la comida simple calmaba las pasiones. Will Keith Kellogg
(1860-1951), ocho años menor, contador y administrador del sanatorio desde ~1880 durante ~25 años, mal pagado y humillado por su
hermano «desde la infancia» (Markel); John le dictaba mientras paseaba en bicicleta y Will lo seguía a pie tomando notas.
Agosto de 1894: trigo cocido que se quedó reposando y se puso rancio; al pasarlo por los rodillos salió en hojuelas; tostadas = Granose.
Patente 558 393 (pedida en 1895, concedida el 14-abr-1896) SOLO a nombre de John; el «templado» se volvió técnica básica de la
industria. Will dijo toda su vida que merecía más crédito. Hojuelas de maíz hacia 1898. C. W. Post, antiguo paciente (1891), abrió su
propia compañía (Grape-Nuts 1897; hojuelas de maíz propias) y decenas de fábricas de cereal llenaron Battle Creek.
Pelea por el azúcar: Will quería endulzar para el gran público; John se negaba. Febrero de 1906: Will funda la Battle Creek Toasted
Corn Flake Company con malta y azúcar. 1907: «el miércoles es el día del guiño» en Nueva York (caja gratis a quien le guiñara al
tendero) y la firma de W. K. Kellogg en cada caja («Ninguna es legítima sin esta firma»); millones al año en publicidad.
John vendió sus derechos a Will, cobró con acciones y luego sacó cereal con el nombre Kellogg's: pleitos durante casi diez años hasta
la Suprema Corte de Michigan (1920): ganó Will; John pagó las costas y solo pudo poner su nombre en letra pequeña. Desde entonces
casi no se hablaron. Carta de disculpa de John (1941-43): su secretaria la consideró indigna y la guardó; Will la leyó después de la
muerte de John (1948 o en 1951, según la fuente: el guion no da fecha). 1930: Fundación W. K. Kellogg (salud y niños) con casi toda su
fortuna. Murieron los dos a los noventa y un años (John 14-dic-1943; Will 6-oct-1951).
México: Kellogg's llega en 1951; desde 1973 Querétaro, una de las plantas de cereal más grandes del mundo; «Zucaritas» (hojuelas con
azúcar, el Tigre Toño) se volvió nombre común de la hojuela azucarada.
Elementos prohibidos en imagen: cajas de cereal modernas, plástico, logotipos y letras; a las personas se las describe por oficio,
nunca por nombre (filtro de personas destacadas de Flow).
"""

TITULO = "Los Corn Flakes Nacieron de un ERROR (Y Separaron a Dos Hermanos Para Siempre)"
ARCHIVO = "corn_flakes"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 96
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

# Pronunciación para Chatterbox (solo lo que se dice en voz; subtítulos y Whisper ven la grafía real).
FONETICA = {
    "Kellogg's": "Kélogs",
    "Kellogg": "Kélog",
    "Battle Creek": "Bátel Crik",
    "Corn Flakes": "Corn Fléiks",
    "Will": "Uíl",
    "John": "Yon",
    # «Will» solo en las frases donde «Uíl» salió mal (23-oct): «Güil» con contexto para no tocar las que ya pasaron
    "menor, Will": "menor, Güil", "Will va": "Güil va", "Will no": "Güil no", "Will sabe": "Güil sabe",
    "Si Will": "Si Güil", "Will publica": "Güil publica", "Will lo": "Güil lo", "razón a Will": "razón a Güil",
    "Will la lee": "Güil la lee",
}
# Whisper escribe «Dr.», cifras o une «Las Zucaritas»: la transcripción está completa (voz/eval.json, 23-oct)
CER_MAX_POR_FRASE = {"sanatorio_4": 0.06, "patente_2": 0.08, "granos_5": 0.015, "guino_3": 0.013, "mexico_2": 0.02,
                     "mexico_8": 0.03}

SECUENCIA = dict(
    video_s=60,         # el usuario (23-oct): 1 min inicial en clips de Flow
    clip_s=10,
    video_calidad="360p",
    combinar=True,      # cada clip de 10 s une dos momentos del guion con una transición dibujada
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.5,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={"scene-001": 0.0, "scene-004": 0.0},   # el 1 trae voz de conferencia y el 4 un «hmm» (Whisper, 23-oct)
    recorte_por={"scene-001": 0.09, "scene-003": 0.12},   # letterbox negro en los primeros 2-3 s (23-oct)
    carpeta_descargas="flow-corn_flakes",
)

# Ficha visual del episodio: se repite PALABRA POR PALABRA en cada prompt donde aparezca (triple anclaje).
FICHA = dict(
    estilo="Cinematic horizontal sixteen-by-nine diorama made entirely of handmade stop-motion plasticine clay, matte texture "
           "with visible fingerprints, warm window light, full-bleed scene that fills the entire frame edge to edge, no border, "
           "no frame, no vignette",
    personajes={
        "medico": "a plasticine doctor about forty-five years old, short and stocky, with short brown hair, a thick mustache and "
                  "a short goatee, round gold-rimmed glasses, an all-white three-piece suit and a white tie",
        "medico_viejo": "an elderly plasticine doctor about eighty years old, short and stocky, with short completely white "
                        "hair, a thick white mustache and white goatee, round gold-rimmed glasses, an all-white suit and a white tie",
        "contador": "a plasticine bookkeeper about thirty-five years old, thin and serious, with short brown hair parted on the "
                    "side, a thick mustache and small round metal-rimmed glasses, a charcoal gray suit with vest, a black bow "
                    "tie, holding a small notebook",
        "empresario": "a plasticine businessman about fifty years old, thin and serious, with short graying hair parted on the "
                      "side, a thick gray mustache and small round metal-rimmed glasses, a charcoal gray three-piece suit and a "
                      "black bow tie",
        "anciano": "a plasticine old man about eighty-eight years old, thin, with sparse white hair and a white mustache, round "
                   "dark glasses, a charcoal gray suit and a wooden cane",
    },
    objeto="thin wavy golden plasticine cereal flakes, toasted at the edges, on a black iron baking tray; and a machine with "
           "two steel rollers and an iron hand crank, no electric motor",
    epoca="experimental kitchen of an 1890s health sanitarium in Michigan: cast-iron stoves, copper pots, wooden tables, glass "
          "jars of grain, linen aprons, gas lamps; no plastic, no modern cereal boxes, no electric appliances",
    cierre="No text, no letters, no numbers or digits anywhere, no logos, no modern objects.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "gancho": dict(sabor="tension"), "promesa": dict(sabor="espacio"), "sanatorio": dict(sabor="espacio"),
    "granos": dict(sabor="espacio"), "hermano": dict(sabor="vacio"), "olvido": dict(sabor="tension"), "hojuelas": dict(sabor="esperanza"),
    "patente": dict(sabor="vacio"), "fiebre": dict(sabor="tension"), "azucar": dict(sabor="tension"),
    "salto": dict(sabor="esperanza"), "guino": dict(sabor="esperanza"), "pleito": dict(sabor="tension"),
    "carta": dict(sabor="vacio"), "mexico": dict(sabor="esperanza"), "cierre": dict(sabor="esperanza"),
}

# Música con Lyria adaptada al guion (antes: python fab.py biblioteca sugerir corn_flakes).
LYRIA = dict(
    estilo="Warm, handmade documentary score for a stop-motion story about two brothers and an accidental breakfast: pizzicato "
           "strings, marimba, soft clarinet, felt piano, glockenspiel, light brushed percussion and an upright bass, with a touch "
           "of old American ragtime piano. Curious and human, never epic.",
    escenas={
        "gancho": ("A single questioning felt piano figure over a low held clarinet, curious and a little ironic. Almost empty.", 3),
        "promesa": ("A gentle marimba pulse begins, upright bass enters, the feeling of a family story about to unfold.", 4),
        "sanatorio": ("Orderly, slightly stiff routine: steady walking bass, tidy pizzicato, a polite old-fashioned waltz feeling.", 4),
        "granos": ("Light comic trial and error: clumsy bassoon-like clarinet, plucked strings, small stumbles and a crunchy little stop.", 4),
        "hermano": ("Quiet and melancholic: a lonely clarinet line over sparse piano, patient and tired.", 3),
        "olvido": ("Something has gone wrong in the kitchen: hesitant pizzicato, ticking glockenspiel, a small rising question.", 4),
        "hojuelas": ("Delighted surprise: bright marimba and glockenspiel flourish, a warm discovery, light and crunchy.", 6),
        "patente": ("Deflated and bitter: a slow falling clarinet phrase, low strings, one unresolved chord.", 3),
        "fiebre": ("A bustling small-town boom: quick ragtime piano, busy pizzicato, comic energy, many things happening at once.", 6),
        "azucar": ("Tension between two people: low pulsing strings and muted piano, stubborn and heavy, building slowly.", 5),
        "salto": ("Courage and a new beginning: the pulse lifts, warm strings and marimba climb together, hopeful and brave.", 6),
        "guino": ("Playful and cheeky: bouncy ragtime piano with pizzicato and glockenspiel winks, charming and fast.", 7),
        "pleito": ("Serious and cold: slow low strings, a ticking pulse, heavy and stubborn, ending on a held dark tone.", 5),
        "carta": ("Tender and sad: solo felt piano, a few soft clarinet notes, silence between phrases.", 2),
        "mexico": ("Warm and wide: flowing piano arpeggios, sustained strings, glockenspiel sparkle, a sunny morning feeling.", 6),
        "cierre": ("Return to the opening piano figure, now warm and resolved, a small smile, then a calm ending.", 4),
    },
    tramos=[
        (["gancho", "promesa", "sanatorio", "granos"],
         "Begin from near silence. End on a held tone that can flow into the next piece. No loud ending."),
        (["hermano", "olvido", "hojuelas"],
         "Begin softly with a held tone. End on a bright sustained tone that can flow into the next piece."),
        (["patente", "fiebre", "azucar"],
         "Begin softly with a low held tone. End on a sustained low tone that can flow into the next piece."),
        (["salto", "guino", "pleito"],
         "Begin gently with a held tone. End on a dark sustained tone that can flow into the next piece."),
        (["carta", "mexico", "cierre"],
         "Begin very softly with solo piano. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Este cereal lo inventó un médico que quería una comida que no supiera a casi nada.",
        "Él creía que los sabores fuertes despertaban las pasiones del cuerpo, y que un desayuno simple las calmaba.",
        "Pero el que lo convirtió en uno de los desayunos más vendidos del mundo fue su hermano menor.",
        "El hombre al que humilló durante veinticinco años.",
        "Y todo empezó con un error en la cocina.",
    ]},
    {"id": "promesa", "frases": [
        "Una olla de trigo olvidada, que debió terminar en la basura.",
        "De ahí salió una empresa que hoy vale miles de millones.",
        "Pero también una guerra entre dos hermanos que llegó hasta la Suprema Corte.",
        "Y una carta de perdón que llegó demasiado tarde.",
        "Esta es la historia de los Corn Flakes, y de los hermanos Kellogg.",
    ]},
    {"id": "sanatorio", "frases": [
        "Battle Creek, Michigan, a finales del siglo diecinueve.",
        "Aquí está uno de los hospitales más famosos de Estados Unidos.",
        "No es un hospital común. Es un sanatorio, una especie de hotel para curarse.",
        "Vienen ricos, políticos y estrellas, a bañarse, a hacer ejercicio y a comer bien.",
        "Lo dirige el doctor John Harvey Kellogg, famoso por vestirse de blanco de pies a cabeza.",
        "John tiene ideas muy firmes: nada de carne, nada de alcohol, nada de café.",
        "En su época, el desayuno típico era pesado: carne frita, papas, pan con manteca.",
        "Y muchísima gente vivía con indigestión.",
        "El doctor quiere inventar un desayuno ligero, de granos, fácil de digerir.",
    ]},
    {"id": "granos", "frases": [
        "Sus primeros intentos no son precisamente un éxito.",
        "Primero hornea una galleta de harina integral, dos veces, hasta dejarla dura como piedra.",
        "Luego la muele en pedacitos, y le pone el mismo nombre que ya usaba el cereal de otro médico.",
        "El otro médico lo demanda, y el doctor tiene que cambiarle una letra al nombre.",
        "Ese cereal acabó llamándose granola.",
        "También sirven pan tostado durísimo, porque el doctor creía que masticar mucho era sano.",
        "Cuentan que una paciente se rompió la dentadura postiza con ese pan.",
        "Y le exigió al sanatorio que le pagara una nueva.",
        "El doctor necesitaba algo nutritivo, pero que no rompiera dientes.",
    ]},
    {"id": "hermano", "frases": [
        "Pero John no trabaja solo.",
        "Detrás de él, siempre un paso atrás, está su hermano menor.",
        "Will es ocho años más joven, callado y muy bueno con los números.",
        "Lleva las cuentas del sanatorio, contrata, despide, paga y resuelve todo lo que el doctor no quiere ver.",
        "Trabaja jornadas larguísimas por un sueldo muy pequeño.",
        "Y su hermano no pierde oportunidad de recordarle quién manda.",
        "John recorre el sanatorio en bicicleta, dictando órdenes.",
        "Y Will va trotando a su lado, con la libreta en la mano, anotando cada palabra.",
        "Así pasan casi veinticinco años.",
    ]},
    {"id": "olvido", "frases": [
        "Agosto de mil ochocientos noventa y cuatro.",
        "En la cocina experimental del sanatorio, los hermanos están cociendo trigo.",
        "La idea es aplastarlo con rodillos para hacer una masa, y hornearla como pan.",
        "Pero algo los interrumpe, y tienen que salir.",
        "El trigo cocido se queda ahí, reposando, durante horas.",
        "Cuando vuelven, ya está duro y algo rancio.",
        "Lo normal sería tirarlo. El sanatorio cuidaba mucho cada centavo.",
        "Así que deciden pasarlo de todos modos por los rodillos.",
        "Y en lugar de una masa, sale algo que nunca habían visto.",
    ]},
    {"id": "hojuelas", "frases": [
        "Cada grano se aplasta y sale convertido en una hojuela delgada, separada de las demás.",
        "Las meten al horno, y salen doradas y crujientes.",
        "Sin querer, habían descubierto el templado: dejar reposar el grano cocido para que se aplaste en hojuelas.",
        "Esa técnica se volvería la base de toda una industria.",
        "Se las sirven a los pacientes, y les encantan.",
        "Tanto, que al volver a casa escriben pidiendo que se las manden por correo.",
        "Más tarde prueban con maíz, y el resultado es todavía mejor.",
        "Habían nacido las hojuelas de maíz.",
    ]},
    {"id": "patente", "frases": [
        "Llega la hora de registrar el invento.",
        "La patente sale en mil ochocientos noventa y seis.",
        "Y en ella aparece un solo nombre: el del doctor John Harvey Kellogg.",
        "Will no aparece por ningún lado.",
        "Él pasaría el resto de su vida diciendo que la idea también era suya.",
    ]},
    {"id": "fiebre", "frases": [
        "Y el invento se les escapa de las manos.",
        "Entre los pacientes del sanatorio había pasado un hombre llamado Charles Post.",
        "Ese hombre conoció los cereales del sanatorio, y al salir abrió su propia fábrica en el mismo pueblo.",
        "Se hace millonario antes que los Kellogg.",
        "Detrás de él llegan decenas de imitadores.",
        "Battle Creek se llena de fábricas de cereal, cada una con su caja y su promesa de salud.",
        "Y mientras todos se hacen ricos con su idea, Will sigue llevando las cuentas de su hermano.",
    ]},
    {"id": "azucar", "frases": [
        "Will sabe exactamente qué le falta a ese cereal para conquistar al mundo.",
        "Azúcar.",
        "Las hojuelas del doctor son sanas, pero sosas.",
        "A la gente le gustaría un poco de dulce.",
        "Para John, eso es un sacrilegio.",
        "El azúcar va contra todo lo que él predica.",
        "Si Will quiere endulzar el cereal, tendrá que hacerlo sin él.",
        "Y aquí Will tiene que tomar la decisión más difícil de su vida.",
        "Tiene cuarenta y cinco años, poco dinero, y nunca ha trabajado para nadie más que su hermano.",
        "¿Se queda a salvo, a la sombra del doctor? ¿O lo arriesga todo?",
    ]},
    {"id": "salto", "frases": [
        "En febrero de mil novecientos seis, Will renuncia.",
        "Le compra a su hermano los derechos de las hojuelas de maíz, y funda su propia compañía.",
        "Le pone malta y azúcar a la receta.",
        "Y cambia algo más: empieza a gastar en anuncios como nadie lo había hecho.",
        "Para que nadie confunda su cereal con los imitadores, pone su firma en cada caja.",
        "Debajo, una advertencia: ninguna es legítima sin esta firma.",
    ]},
    {"id": "guino", "frases": [
        "Pero su golpe maestro lo da en Nueva York, en mil novecientos siete.",
        "Will publica un anuncio con una promesa extraña.",
        "Los miércoles serán el día del guiño.",
        "Cualquier mujer que entre a su tienda y le guiñe el ojo al tendero, se lleva una caja de hojuelas gratis.",
        "En una época tan seria, aquello es casi un escándalo.",
        "Y justamente por eso, todo Nueva York habla del cereal.",
        "En poco tiempo, los trenes llevan vagones enteros de hojuelas a la ciudad cada mes.",
        "El empleado humillado se ha convertido en uno de los empresarios más exitosos del país.",
    ]},
    {"id": "pleito", "frases": [
        "Y entonces su hermano mayor vuelve a aparecer.",
        "John también empieza a vender cereal, con el mismo apellido en la caja: Kellogg's.",
        "Para los clientes, ¿cuál es el verdadero Kellogg?",
        "El menor lo demanda. El mayor contraataca con otra demanda.",
        "La pelea dura casi diez años, y llega hasta la Suprema Corte de Michigan.",
        "En mil novecientos veinte, los jueces le dan la razón al hermano menor.",
        "John tiene que pagar los gastos del juicio.",
        "Y solo puede poner su nombre en letras pequeñitas, en el fondo de sus propias cajas.",
        "Desde entonces, los dos hermanos casi no vuelven a hablarse.",
    ]},
    {"id": "carta", "frases": [
        "Muchos años después, ya anciano, John se sienta a escribirle a Will una carta.",
        "En ella le pide perdón por cómo lo trató toda la vida.",
        "Pero su secretaria la lee, decide que es indigna de un doctor tan importante, y la guarda.",
        "La carta nunca sale.",
        "El hermano menor la lee cuando John ya ha muerto.",
        "Para entonces, Will está casi ciego.",
        "Y ya no hay nadie a quien contestarle.",
    ]},
    {"id": "mexico", "frases": [
        "El hermano menor no se quedó con su fortuna.",
        "En mil novecientos treinta creó una fundación para la salud y la educación de los niños, y le dejó casi todo lo que tenía.",
        "Los dos hermanos murieron a la misma edad, a los noventa y un años.",
        "Y su cereal siguió viajando.",
        "En mil novecientos cincuenta y uno, Kellogg's llegó a México.",
        "Años después, en Querétaro, abrió una de las plantas de cereal más grandes del mundo.",
        "Y aquí pasó algo que al doctor le habría quitado el sueño.",
        "Las hojuelas que más triunfaron fueron las cubiertas de azúcar.",
        "Las Zucaritas se volvieron tan famosas, que su nombre se usa para cualquier hojuela dulce.",
    ]},
    {"id": "cierre", "frases": [
        "El doctor quería un desayuno que calmara al mundo.",
        "Su hermano lo endulzó, y el mundo entero se sentó a desayunarlo.",
        "Así que la próxima vez que sirvas un plato de hojuelas, acuérdate de aquella olla olvidada.",
        "Y de los dos hermanos que se pelearon por ella hasta el final.",
        "Ahora dime tú: ¿habrías aguantado veinticinco años a la sombra de tu hermano, o te habrías ido mucho antes?",
        "Te leo en los comentarios.",
        "Y si te gustan las historias de las marcas que tienes en tu cocina, suscríbete.",
        "La próxima ya se está moldeando.",
    ]},
]
