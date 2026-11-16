# -*- coding: utf-8 -*-
"""GUION — «30 trucos para NUNCA quedarte sin ORO en WoW Forever» (Crónicas de Warcraft, 15-nov-2026).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Tema elegido por el usuario (15-nov, opción 1 de canales/formula/cronicas_warcraft.md): una variable sobre «20 errores del 30 al 60» = el tema.
Investigación: videos/_investigacion_wow_oro_forever.md. Lo que es de un solo jugador se dice «un jugador»; la voz NO cita fuentes.
SIN OVERGEAR (el usuario, 15-nov) y NADA contra comprar oro (campaña 3 de Overgear desde el 25-nov).
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras. Cifras en letra.
Comentarios (≤ 10 días, ninguno usado antes): c26 corrección @Jorge_alvarez_ · c18 ayuda @rafaelmartinezsantana7055 ·
burla0 @Ehren-03 · burla1 @vincent1785 · burla2 @CaneAttack · gracias1 @Alan-kb5iz @Leon89vlk · gracias2 @JONATHANTX111 @JotaBerttuci.
"""

TITULO = "30 trucos para NUNCA quedarte sin ORO en WoW Forever"
ARCHIVO = "wow_oro_forever"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Classic": "Clásic", "Azeroth": "Azeróth", "Crónicas de Warcraft": "Crónicas de uárcraft",
    "Ventormenta": "Ventorménta", "Remy": "Rémi", "Retail": "Rítéil",
    "Auctionator": "Ócshoneitor", "Disenchantrix": "Disenchántrix", "Waylaid Crates": "Uéileid Kréits", "Waylaid Crate": "Uéileid Kréit",
    "Shipping Label": "Shíping Léibel", "Chol'aruk": "Chólaruk", "Zephras": "Séfras", "Gelvas Grimegate": "Guélvas Gráimguéit",
    "Darkmoon": "Dárkmun", "Gizelton": "Guízelton", "Mister Graphed": "Míster Gráft", "Riverglades": "Ríverglèids",
    "Frayfeather": "Fréifeder", "Jadefire": "Yéidfáier", "Legashi": "Leguáshi", "Strahad Farsan": "Estrájad Fársan",
    "Randal Hunter": "Rándal Jánter", "Kildar": "Kíldar", "Heming": "Jéming", "Nat Pagle": "Nat Péiguel", "Marcy Baker": "Mársi Béiker",
    "Dokimi": "Dokími", "Three Corners": "Zri Kórners", "Hyjal": "Jáyal", "Onyxia": "Oníxia", "Barrow Deeps": "Bárrou Díps",
    "Gadgetzan": "Gádyetzan", "Tanaris": "Tanáris", "Desolace": "Desolás", "Arathi": "Aráti", "Azshara": "Asshára",
    "Orgrimmar": "Orgrímar", "Elwynn": "Éluin", "Mulgore": "Mulgór", "Grom'gol": "Gromgól", "Feralas": "Ferálas",
    "Gurubashi": "Gurubáshi", "Pagle": "Péiguel", "Ehren": "Éren", "Vincent": "Vínsent", "CaneAttack": "Kéin Atak",
    "Jorge": "Jórje", "Rafael": "Rafaél", "Leon": "León", "Jonathan": "Yónatan", "Berttuci": "Bertúchi",
    "JcJ": "jota ce jota", "add-on": "ádon", "add-ons": "ádons", "PNJ": "pe ene jota",
}
FONETICA = FONETICA_APPLIO
CER_MAX_POR_FRASE = {   # 15-nov: hyps leídas una a una (solo nombres propios/cifras)
    "c28_3": 0.1, "c26_5": 0.1, "c23_0": 0.1, "c22_3": 0.1, "c18_4": 0.1, "c16_0": 0.1, "c16_1": 0.1, "c13_1": 0.1, "c11_1": 0.1, "gracias2_1": 0.1, "c10_1": 0.1, "c10_2": 0.1, "c08_5": 0.1, "c07_0": 0.1, "c07_6": 0.1, "c04_4": 0.1, "c02_0": 0.1, "c02_4": 0.1, "c03_0": 0.12, "c09_3": 0.1, "c11_0": 0.16, "c17_3": 0.05, "c03_2": 0.15}
TAIL_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Nivel cuarenta. Por fin puedes aprender a montar. Vas al instructor, abres la bolsa, y tienes cuarenta y dos de oro.',
        'La equitación cuesta cien. Y la doble especialización, que también se desbloquea al cuarenta, otros cincuenta.',
        'Esa escena se está repitiendo ahora mismo en miles de personajes de World of Warcraft Forever.',
        'Y al sesenta es peor: la equitación de oficial cuesta mil de oro, y cada montura épica, doscientos más.',
        'Súmale los doscientos siete de oro que cuesta entrenar a tu clase del uno al sesenta. Son más de mil quinientos de oro solo para llegar montado.',
        'La buena noticia es que el oro en Forever no se gana con suerte. Se gana con costumbres.',
        'Hoy te traigo treinta trucos para que nunca más te quedes sin oro. Unos te ahorran, otros te pagan, y los últimos te pueden hacer rico.',
        'Y nada de esto es teoría: todo sale del juego en vivo, de los precios reales de la subasta de estos días, y de lo que han hecho jugadores que ya llegaron al sesenta con la bolsa llena.',
        'Van del más sencillo, el que puedes hacer hoy en el nivel cinco, al más rentable de todos. Del treinta al uno.',
    ]},
    {"id": 'c30', "frases": [
        'Número treinta. No compres todos los rangos de hechizo.',
        'Cada vez que vas al instructor, el juego te pone delante una lista entera, y el instinto es comprarlo todo.',
        'Pero hay hechizos que tu personaje no va a usar nunca. Un guerrero que tanquea no necesita todos los rangos de golpes que solo usa el de daño.',
        'Y un paladín que no tanquea no necesita Furia justa, ni todos los sellos que nunca pone en la barra.',
        'Un jugador que solo se saltó cuatro hechizos de guerrero se ahorró dos de oro en una sola visita. Dos de oro, en el nivel veinte, es mucho.',
        'El entrenamiento completo, del uno al sesenta, cuesta lo mismo en todas las clases: unos doscientos siete de oro. Pero eso no significa que tengas que pagarlo todo de golpe.',
        'Algunos rangos los puedes comprar más tarde, cuando el oro sobre. Y otros, simplemente, nunca.',
        'Antes de pagar, pregúntate: ¿esto lo voy a apretar? Si la respuesta es no, ese rango se queda en la tienda.',
    ]},
    {"id": 'c29', "frases": [
        'Número veintinueve. Si eres paladín o brujo, tu montura del cuarenta es gratis.',
        'Estas dos clases tienen su propia montura por misión, y no pagan los cien de oro de la equitación de aprendiz.',
        'El brujo la consigue con Strahad Farsan, en Trinquete, en Los Baldíos. El paladín de la Alianza, con la misión del Tomo de la Nobleza.',
        'Eso es dinero que los demás están juntando a duras penas, y que tú puedes guardar para la doble especialización o para lo que viene al sesenta.',
        'Y no es un atajo raro: es una misión de clase, con su historia y todo. El brujo se gana su corcel vil, y el paladín, su caballo de guerra.',
        'Y si no juegas esas clases, ojo: no las elijas solo por esto. Pero si ya eres una de ellas, no pagues lo que el juego te regala.',
    ]},
    {"id": 'c28', "frases": [
        'Número veintiocho. Llega a Honorable con tu facción antes de comprar la montura.',
        'Si tienes reputación Honorable con tu propia ciudad, el instructor de equitación te hace un diez por ciento de descuento.',
        'La equitación de aprendiz baja de cien a noventa de oro. Y la de oficial, de mil a novecientos. Son cien de oro gratis al sesenta.',
        'En la Alianza, el instructor humano es Randal Hunter, al este del Bosque de Elwynn. En la Horda, Kildar, en el Valle del Honor de Orgrimmar.',
        'Y el descuento también vale para los colores extra: cada montura de otro color baja de veinte a dieciocho de oro.',
        'Y casi siempre llegas a Honorable sin darte cuenta, haciendo las misiones de tu zona. Así que antes de pagar, revisa la pestaña de reputación.',
    ]},
    {"id": 'burla0', "frases": [
        'Y aquí, un mensaje de Ehren, que nos escribió esto: dejen jugar a la gente como quiera, sin prisa, sin seguir un meta, sin optimizar todo.',
        'Y tienes toda la razón. Por eso este video no optimiza tu juego. Lo que optimiza es tu cartera.',
        'Puedes seguir jugando sin prisa, oliendo las flores de Elwynn. Solo que ahora, cuando llegues al instructor, vas a poder pagarle.',
    ]},
    {"id": 'c27', "frases": [
        'Número veintisiete. Hay puntos de Legado que te ahorran oro.',
        'El sistema de Legado de Forever te da puntos para gastar en ventajas, y varias de ellas son, en el fondo, descuentos.',
        'Viajero frecuente hace que tus vuelos cuesten la mitad, y además van un veinte por ciento más rápido.',
        'Regateo te baja un cinco por ciento en los vendedores por cada rango. Y sí, también en las monturas.',
        'Y Reforzar hace que tu equipo pierda menos durabilidad al morir. Menos reparaciones, menos plata tirada en el herrero.',
        'Y otra de las ventajas, Economía de componentes, hace que tus habilidades de clase ya no te pidan componentes de vendedor. Otro gasto que desaparece.',
        'Ninguno te hace rico. Pero son descuentos para siempre, y en un juego de muchos meses, eso suma más que cualquier farmeo de un día.',
    ]},
    {"id": 'c26', "frases": [
        'Número veintiséis. Compra la doble especialización, y deja de pagar por cambiar de talentos.',
        'Y aquí tenemos que corregirnos. En el video anterior dijimos que la doble especialización costaba diez de oro.',
        'Jorge nos escribió: cuesta cincuenta, no diez. Y otra espectadora nos dijo lo mismo. Tienen razón: en el juego, son cincuenta de oro. Gracias por la corrección.',
        'Y aun así, valen cada moneda. Porque reespecializar cuesta uno de oro la primera vez, cinco la segunda, diez la tercera, y sigue subiendo.',
        'Y ese precio solo baja una vez por semana. Si cambias de sanador a daño cada vez que vas a una mazmorra, en un mes ya pagaste la doble varias veces.',
        'Ese diez venía de antes del lanzamiento. En el juego de verdad, el instructor te pide cincuenta, y punto.',
        'Con la doble, cambiar es gratis, solo tienes que estar fuera de combate. Cincuenta de oro una vez, en lugar de pagar para siempre.',
    ]},
    {"id": 'c25', "frases": [
        'Número veinticinco. No compres equipo en la subasta antes de tener montura.',
        'Ese arma verde de tu nivel se ve preciosa. Pero en tres o cuatro niveles la vas a cambiar por otra que te sale gratis en una misión.',
        'Un jugador confesó que se gastó dieciocho de oro en una maza y cinco más en encantarla. Veintitrés de oro que, al cuarenta, le faltaban para montar.',
        'Lo mismo pasa con las profesiones de fabricación: subirlas antes del cuarenta te come el oro en materiales que nadie te compra.',
        'Hay jugadores que llegan al cuarenta con apenas cincuenta de oro, y casi siempre es por esto: pequeños caprichos de diez y veinte de oro que, juntos, son una montura.',
        'La única excepción es la recolección, que te paga desde el primer minuto. Del resto, una mazmorra te viste mejor y gratis.',
    ]},
    {"id": 'c24', "frases": [
        'Número veinticuatro. Recolección desde el nivel uno, y desuella todo lo que veas.',
        'Aprender a recolectar es casi gratis: diez cobres el primer rango, cinco platas el segundo, cincuenta el tercero.',
        'Y en Forever cada criatura se desuella una sola vez. Pero mucha gente mata y sigue de largo, y ese cuero que deja tirado es tuyo.',
        'El cuero ligero lo paga el vendedor a quince cobres, y en la subasta casi se duplica. El medio, a cincuenta, y en la subasta se acerca a noventa.',
        'Y no tienes que farmear aparte: recolectas mientras haces tus misiones. Cada hierba y cada veta que pisas es dinero que ya tenías delante.',
        'Eso sí, mira los precios: el cuero prístino, que en la beta se vendía a más de un oro, ya bajó a unas cinco platas. Lo raro deja de ser raro cuando todos lo recogen.',
        'Si lo que quieres es oro sin complicaciones, la pareja más sencilla es minería y desuello. Y con el Legado, Cosecha abundante te da todavía más.',
    ]},
    {"id": 'c23', "frases": [
        'Número veintitrés. Instala Auctionator, para saber en el acto si algo va al vendedor o a la subasta.',
        'Es un add-on de subasta que ya tiene versión para Forever. Haces un escaneo completo en la casa de subastas, y listo.',
        'A partir de ahí, cada objeto que pasas con el ratón te dice dos precios: lo que te da el vendedor, y lo que vale en la subasta.',
        'Un ejemplo real: la carne de tortuga. El vendedor te da un cobre. En la subasta se vendía a veinte platas.',
        'Y lo mismo con la venta: en la pestaña de vender, haces clic en el objeto, le das a la barra espaciadora, y el add-on lo publica con el precio correcto. Uno tras otro.',
        'Sin el add-on, la vendías por un cobre y ni te enterabas. Con él, cada bolsa llena se convierte en una decisión fácil.',
    ]},
    {"id": 'c22', "frases": [
        'Número veintidós. En la subasta, elige la duración corta, la de tu facción, y publica por la mañana.',
        'Publicar no es gratis: pagas un depósito que sube con la duración, y si no se vende, ese depósito se pierde.',
        'Así que si hay mucha competencia, pon la duración más corta. Y si el vendedor te paga casi lo mismo, véndelo y ya.',
        'La subasta de tu facción se queda con un cinco por ciento. Las neutrales, como la de Gadgetzan o la de Bahía del Botín, con un quince.',
        'Y el truco de la hora: de noche, todo el mundo publica antes de dormir y los precios caen. Por la mañana suben.',
        'Y una buena noticia: Blizzard anunció que va a bajar el depósito mínimo de una plata a un cobre. Así publicar cosas baratas deja de doler.',
        'Un jugador vio cómo una perla de oro pasaba de dos de oro con setenta de noche, a cinco de oro por la mañana. Casi el doble por esperar.',
    ]},
    {"id": 'c21', "frases": [
        'Número veintiuno. Compra en la subasta lo que esté más barato que el vendedor.',
        'Suena absurdo, pero pasa todos los días. Hay gente que publica sin mirar, y pone objetos por debajo de lo que paga cualquier PNJ.',
        'En los foros de Forever ya hay quejas de verdes publicados a treinta platas, cuando el vendedor paga veintinueve. Y armas al precio exacto del vendedor.',
        'Si encuentras algo por debajo, lo compras, se lo vendes al PNJ, y te quedas con la diferencia. Ganancia segura, sin riesgo.',
        'Y los add-ons de subasta te avisan si tú mismo estás a punto de publicar algo por debajo del vendedor. Para no ser tú el que regala monedas.',
        'No te va a hacer rico en una tarde. Pero cada vez que abras la subasta, échale un ojo a lo barato. Son monedas que alguien te está regalando.',
    ]},
    {"id": 'gracias1', "frases": [
        'Antes de seguir, gracias a los que nos escriben. Alan nos dijo que va despacio, descubriendo el mundo a su ritmo, y que estas sugerencias le ayudan a no perderse cosas.',
        'Y León dice que ama que sea lento, que se está gozando cada día sin ningún afán. León, este video está hecho para eso: para que el oro no te meta prisa.',
        'Todos los comentarios se leen, y muchos acaban cambiando el siguiente video. Así que sigan escribiendo.',
    ]},
    {"id": 'c20', "frases": [
        'Número veinte. Hazte un personaje banco con Encantamiento.',
        'Un personaje de nivel bajo aparcado junto al buzón y la casa de subastas, en tu capital. A él le mandas todo lo que no sabes qué hacer.',
        'Y ese personaje decide con calma: esto al vendedor, esto a la subasta, y esto lo desencanto.',
        'Porque un verde que el vendedor paga a dos platas puede darte polvo de encantamiento que vale mucho más. Con un add-on como Disenchantrix, ves qué puede salir antes de romperlo.',
        'Y como está siempre junto al buzón, ese personaje también recoge el oro de tus ventas sin que tu principal tenga que volver a la ciudad.',
        'Tu personaje principal sigue jugando, sin perder tiempo en la subasta. Y si lo subes un poco, sus profesiones de fabricación también te dan puntos de Legado.',
    ]},
    {"id": 'c19', "frases": [
        'Número diecinueve. Las misiones nuevas de Forever pagan más. Hay que buscarlas.',
        'Forever añadió misiones que no existían en Classic, y varias pagan bastante mejor que las de siempre.',
        'En Los Baldíos hay una élite nueva de los jabaespines, Chol\'aruk, en una cueva de la Colina Espinosa. Una sola misión de nivel veintiuno te da ochenta platas.',
        'Ochenta platas en el nivel veinte es casi un oro entero. Y los cielonato, en la Isla Zephras, ya juntan unos dos de oro antes del nivel trece.',
        "Y Chol'aruk es una élite de nivel veinte: no la vas a poder hacer solo. Así que es también la excusa perfecta para juntar un grupo en el chat.",
        'Si una misión es nueva, mira la recompensa antes de descartarla. Muchas veces es la mejor paga de toda la zona.',
    ]},
    {"id": 'c18', "frases": [
        'Número dieciocho. Consigue bolsas grandes cuanto antes.',
        'Y este va para Rafael, que nos escribió desesperado: mi inventario está lleno de objetos de misión, ayuda.',
        'Rafael, primero lo fácil: los objetos de misión que ya entregaste se tiran sin miedo. Y en Forever hay una quinta ranura para una bolsa de componentes.',
        'Además, desde el once de noviembre la Bolsa de paño mágico roja tiene catorce casillas, y en la subasta está bastante barata.',
        'Y en la Feria de la Luna Negra hay una caja de catorce casillas por cincuenta boletos, con Gelvas Grimegate. La próxima Feria vuelve en diciembre, en Mulgore.',
        'Para conseguir esos boletos, la ruta más barata son cincuenta pelambres de oso rasgadas y cinco péndolas vibrantes. Unos tres de oro en total.',
        'Y los vendedores de la Isla Zephras ya venden bolsas de profesión de aprendiz, para que las hierbas y los minerales no te ocupen la bolsa normal.',
        'Más bolsa es más botín por cada salida. Es de las primeras inversiones que se pagan solas.',
    ]},
    {"id": 'c17', "frases": [
        'Número diecisiete. Guarda la tela de los humanoides, aunque no tengas profesión.',
        'La tela es lo que más se publica en la subasta, y no necesitas ninguna profesión para juntarla: te basta con matar a los humanoides que te cruzas por el camino.',
        'Y si tienes Primeros auxilios, hay un truco: con paño de seda haces vendas, y el vendedor te paga la venda de seda pesada a cuatro platas.',
        'Cuando el paño de seda está barato en la subasta, compras, haces vendas y se las vendes al PNJ. Poquito, pero seguro.',
        'Pero ojo con el Monasterio Escarlata: cuando medio servidor entre ahí, va a llover seda, y el precio va a bajar. Vende antes de esa ola.',
        'Y si eres sastre, las talegas pequeñas de seda se vendieron a casi ochenta platas los primeros días. Luego bajaron, como baja todo lo que todos hacen.',
    ]},
    {"id": 'burla1', "frases": [
        'Y aquí, Vincent, que comentó nuestro iceberg: mola que no haya ni un solo ejemplo, ni una foto, este video es más un acto de fe.',
        'Vincent, aceptamos la crítica, y también aceptamos que te reíste. Así que hoy cada moneda sale en pantalla, contada una por una.',
        'Esto ya no es un acto de fe. Es un acto de contabilidad.',
    ]},
    {"id": 'c16', "frases": [
        'Número dieciséis. Las páginas de Tuercespina se venden sueltas.',
        'Las verdes colinas de Tuercespina es esa misión que te pide quince páginas concretas de un libro que se ha despedazado por toda la Vega.',
        'Y a casi nadie le salen las quince seguidas. Le sobran unas y le faltan otras, y lo que le falta, lo busca en la subasta.',
        'Así que no tires las repetidas ni las vendas al vendedor. Ponlas a la venta una por una. Siempre hay alguien a quien le falta justo esa página.',
        'Y aunque no hagas la misión, las páginas te caen igual matando en la Vega. Así que, para un jugador de nivel cuarenta, son monedas que caen solas.',
        'Hay jugadores que incluso se quedan matando trols y piratas de la Vega solo para juntar páginas extra y venderlas.',
    ]},
    {"id": 'c15', "frases": [
        'Número quince. Pesca en mar abierto, y saca cofres sin subir la habilidad.',
        'En Forever, la pesca no ocupa una ranura de profesión. Así que cualquiera puede pescar sin renunciar a nada.',
        'Y en mar abierto, frente a los Páramos de Poniente, el Bosque de Argénteos o Los Baldíos, a veces sale un baúl bien sellado.',
        'Esos baúles no piden habilidad de pesca. Salen en pocos lances de cada cien, pero salen, y traen de todo un poco.',
        'Y si tu habilidad es muy baja, compra un señuelo brillante en el vendedor de pesca, y ya no se te escapa casi nada en las zonas iniciales.',
        'Es la forma más tranquila de ganar oro: una caña, una costa, y paciencia.',
    ]},
    {"id": 'c14', "frases": [
        'Número catorce. La caña que se vende: la Caña de pescar de hierro grande.',
        'Hay cañas de pescar que se ligan a ti en cuanto las tocas. Esta no: se puede vender en la subasta.',
        'Da veinte puntos de pesca, y sale de las trampas de marisco que hay bajo el agua en Desolace, al oeste de la Aldea Cazasombras.',
        'Las trampas dan mariscos casi siempre, y muy de vez en cuando, la caña. Y cada pescador del servidor quiere una.',
        'Y como la caña pide al menos cien puntos de pesca para usarla, el que la compra suele ser un pescador serio, que paga lo que haga falta.',
        'Así que si te sale, no la uses tú. Mírala en la subasta, y decide si prefieres pescar mejor, o pescar con mucho oro en la bolsa.',
    ]},
    {"id": 'c13', "frases": [
        'Número trece. El vendedor que casi nadie espera: el Supervendedor seiscientos ochenta.',
        'Es un robot que viaja con la caravana de Gizelton por el camino de Desolace. Solo puedes comprarle cuando la caravana se detiene.',
        'Y vende recetas con una sola unidad, como la de chuleta de lobo magro, a dieciséis platas.',
        'Un jugador calculó que cada chuleta deja unas dos platas y media de ganancia, porque la carne de lobo es barata y la chuleta se vende bien.',
        'Y no solo vende esa receta: también tiene chile aliento de dragón, costillas de lobo picantes y algunos esquemas de ingeniería, todo en cantidades limitadas.',
        'Y lo mejor: la mayoría no se molesta en esperar al robot. Esa pequeña espera es justo lo que hace que valga dinero.',
    ]},
    {"id": 'c12', "frases": [
        'Número doce. Los talismanes de guerrero de Arathi.',
        'Los guerreros, en el nivel treinta, tienen la misión del Hacha de torbellino, y les piden ocho talismanes de tres tipos distintos.',
        'Ardientes, del trueno y blasonados. Caen de los Exiliados de las Tierras Altas de Arathi, y muchos guerreros prefieren comprarlos.',
        'En la subasta, los del trueno y los blasonados estaban entre veinte y treinta platas cada uno. Algunos jugadores los vieron por encima de cincuenta.',
        'Los del trueno caen en el centro de Arathi, los blasonados al noreste y los ardientes al noroeste. Así que puedes ir de un campamento a otro sin dar vueltas.',
        'Pero véndelos ya. Cuando la ola de guerreros termine su hacha, ese precio se va a caer.',
    ]},
    {"id": 'c11', "frases": [
        'Número once. Las perlas azules del Arrecife Mortal.',
        'En la costa de la Vega de Tuercespina, bajo el agua, hay almejas gigantes. Y casi siempre traen una perla azul.',
        'Hay una misión en las Tierras Inhóspitas que pide nueve, y mucha gente prefiere comprarlas a bucear.',
        'Si juegas druida, con la forma acuática es un paseo. Los demás, a vigilar la barra de aire.',
        'Y cada almeja es como un pequeño cofre: aunque el precio baje, el botín de una tarde de buceo se vende mucho mejor que lo que te daría el vendedor.',
        'Ojo con el precio: la primera semana estaban a cuarenta platas, y en cuatro días bajaron a quince. El vendedor solo paga cincuenta cobres. Vende pronto.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y otro par de gracias. Jonathan nos dijo que el video era justo lo que necesitaba.',
        'Y Jota dice que muchas cosas del dos mil cuatro le sirvieron en el dos mil diecinueve, y que ahora estos videos le ayudan con todo lo que cambió.',
        'Si a ti también te están sirviendo, suscríbete. Es gratis, no cuesta ni un cobre, y es la forma de que sigamos haciendo guías como esta.',
    ]},
    {"id": 'c10', "frases": [
        'Número diez. Huevos gigantes: vende cuando están de moda.',
        'En Gadgetzan hay una misión de cocina que pide doce huevos gigantes. Y casi todos los cocineros los compran en la subasta.',
        'Caen de los rocs de Tanaris y de los lechúcicos de las Tierras del Interior. Y al principio, se vendían a un oro cada uno.',
        'Pero mira lo que pasó: un oro, luego sesenta y siete platas, luego cuarenta y nueve, luego treinta y una. Y en una semana, dieciocho platas.',
        'Porque todos vieron el mismo farmeo y todos fueron a por él. Esa es la lección más importante de la subasta: lo que todos farmean se hunde en días.',
        'Y la misión también pide carne de almeja sabrosa y queso de Alterac. Así que cuando los huevos caen, a veces la almeja es la que sube.',
        'Así que el truco no es farmear huevos. Es llegar antes, vender rápido, y saltar a otra cosa cuando el precio empiece a caer.',
    ]},
    {"id": 'c09', "frases": [
        'Número nueve. Los objetos grises que el vendedor paga caro.',
        'No todo lo gris es basura. Hay criaturas que sueltan objetos grises que el vendedor te paga a precio de oro.',
        'En Feralas, los hipogrifos sueltan picos afilados y huesos de ala que el vendedor te paga entre seis y ocho platas cada uno.',
        'En las granjas de las Laderas de Trabalomas, los granjeros sueltan horcas que valen unas quince platas. Y en Desolace, los basiliscos sueltan colas y espinas.',
        'Y como esos hipogrifos son de misión, reaparecen muy rápido. Puedes quedarte en un mismo punto y no parar de llenar la bolsa.',
        'No hay que pensar en la subasta, ni en comisiones, ni en depósitos. Matas, llenas la bolsa, y el vendedor te paga en el acto.',
    ]},
    {"id": 'c08', "frases": [
        'Número ocho. Las tortugas de Tanaris.',
        'En la costa sur de Tanaris hay unas tortugas, los Planeadores de oleaje, de nivel cuarenta y ocho a cincuenta. Y casi nadie va a por ellas.',
        'Sueltan dos grises que el vendedor paga bien, carne de tortuga, cuero, y almejas que a veces traen perlas.',
        'Un jugador se pasó una hora y veinte minutos ahí y ganó unos cincuenta y cinco de oro. En una de las almejas le salió una perla de oro.',
        'Sin profesiones, él calcula unos veinte de oro por hora solo con lo que paga el vendedor. Con desuello y minería, mucho más.',
        'Y esa perla de oro el vendedor la paga a un oro, pero en la subasta llegó a valer cinco. Por eso Auctionator siempre va primero.',
        'Y lo más curioso: en toda esa hora no vio a nadie más. Mientras medio servidor se peleaba por huevos, él tenía la playa para él solo.',
    ]},
    {"id": 'c07', "frases": [
        'Número siete. Las Waylaid Crates: llénalas, o véndelas.',
        'Son cajas interceptadas que caen de los enemigos. Las llenas con los materiales que piden y te dan Favor de comerciante.',
        'Y la primera que llenas puede traer una Shipping Label, que da cincuenta de Favor y dos mil de reputación, una vez por personaje.',
        'Ahora, el Favor no se cambia por oro. El oro está en las cajas vacías: la primera semana se vendían entre diecisiete y treinta platas.',
        'Y desde el nueve de noviembre también caen en mazmorras. Así que haz cuentas: si una caja vale más en la subasta que lo que te da llenarla, véndela.',
        'Y si no quieres hacer cuentas cada vez, una regla sencilla: llena la primera caja de cada personaje, por la Shipping Label, y vende las demás que no te salgan a cuenta.',
        'Se entregan en el campamento de Three Corners, en las Montañas Crestagrana, si eres Alianza, y al oeste del Cruce, en Los Baldíos, si eres Horda.',
    ]},
    {"id": 'c06', "frases": [
        'Número seis. Las recetas nuevas del Favor: sé el primero en fabricarlas.',
        'Forever trae más de seiscientas recetas nuevas. Y las mejores se compran con Favor de comerciante y piden reputación.',
        'Eso significa que, al principio, casi nadie las tiene. Y quien llega primero pone el precio.',
        'Un jugador ganó unos cinco de oro en un solo día vendiendo un elixir que casi nadie más podía fabricar.',
        'Hay quien piensa que el primero en tener la fórmula de encantar un collar va a poder cobrar lo que quiera. Y en un servidor nuevo, probablemente tenga razón.',
        'Esa pequeña barrera de esfuerzo, la reputación y el Favor, es justo lo que hace que valga dinero. Si la saltas antes que los demás, cobras tú.',
    ]},
    {"id": 'burla2', "frases": [
        'Y un último comentario. CaneAttack nos escribió: siento que no aprecio la información con estos tipos de voz. Pero buen video, hermano.',
        'CaneAttack, buenas noticias: hoy no hay competencia de voces, ni votaciones, ni sorpresas. Solo la voz de siempre, contando monedas.',
        'Y si aun así no la aprecias, tranquilo: el oro que vas a ganar sí lo vas a apreciar.',
    ]},
    {"id": 'c05', "frases": [
        'Número cinco. Invierte para las bandas del nueve de diciembre.',
        'El nueve de diciembre abren las bandas de Forever, entre ellas la Guarida de Onyxia. Y con las bandas, cambian los precios.',
        'Los que van a entrar necesitan pociones de resistencia al fuego, frascos y consumibles. Y los materiales para hacerlos van a subir.',
        'Un jugador compró unos dos mil cardoveloces a tres platas desde el primer día. Una semana después ya valían veinticinco.',
        'El fuego elemental es otro clásico: en Classic pasó de cuarenta platas a dos de oro cuando abrieron las bandas. Y la tierra elemental ya está subiendo poco a poco.',
        'Y el cardoveloz sube por el té de cardo de los pícaros, y ahora también de los druidas felinos. Cada clase nueva que lo usa es un comprador más.',
        'Eso sí: invertir es apostar. Compra solo lo que esté claramente barato, y nunca el oro que necesitas para la montura.',
    ]},
    {"id": 'c04', "frases": [
        'Número cuatro. Pesca de nivel alto con Adornos brillantes.',
        'Los Adornos brillantes se compran en los vendedores de pesca y suben tu habilidad setenta y cinco puntos mientras duran.',
        'Con eso, aunque tengas poca habilidad, ya puedes pescar en los bancos y restos flotantes de las zonas altas.',
        'Y de esos restos salen baúles con cuero, paño rúnico, pociones, alguna receta y, a veces, bolsas de doce y de catorce casillas.',
        'Para subir de verdad, el libro de pesca de experto te lo vende el Viejo Heming, en Bahía del Botín. Y el de artesano, Nat Pagle, en el Marjal Revolcafango.',
        'Y en la costa de Tanaris, con algo más de habilidad, los restos flotantes dan todavía más. Un jugador calculó que pescando ahí habría sacado diez o veinte de oro extra por hora.',
        'Un jugador sacó unos quince de oro en cuatro días pescando desde el nivel diez. Y una bolsa grande ya en el segundo día.',
    ]},
    {"id": 'c03', "frases": [
        'Número tres. Los sátiros de Frondavil y Azshara.',
        'Cuando llegas a los cincuenta, hay un lugar que suelta el paño más caro del juego: los sátiros.',
        'Los sátiros Jadefire de Frondavil y los Legashi de Azshara sueltan paño rúnico y tela de inferi sin parar.',
        'Un jugador se quedaba una o dos horas con ellos al terminar las misiones, y sacó un par de cientos de oro.',
        'Y la tela de inferi no es solo para sastres: los brujos y los encantadores la buscan, así que siempre tiene comprador.',
        'Y llegó al sesenta con más de mil trescientos de oro, sin farmeos raros y sin una profesión de fabricación fuerte. Solo con costumbres como estas.',
    ]},
    {"id": 'c02', "frases": [
        'Número dos. Las vetas de torio ricas, y el Cristal Arcano.',
        'Si eres minero de nivel alto, en Las Estepas Ardientes hay vetas de torio ricas. Y al principio, casi nadie las está picando.',
        'Un jugador sacó en una hora y cuarto varios montones de torio y seis Cristales Arcanos.',
        'Los vendió a unos nueve de oro cada uno, y al poco tiempo ya se vendían a doce y medio.',
        'Y aquí hay un detalle de Forever: en el mercado negro de Riverglades, Mister Graphed vende el Cristal Arcano a cincuenta de oro fijos. Ese es su techo.',
        'Y en ese mismo mercado negro, el Loto negro también tiene su techo de cincuenta de oro. Así que los dos objetos más caros de la recolección ya tienen un precio máximo conocido.',
        'Así que el cristal nunca va a valer más de cincuenta. Pero mientras esté muy por debajo, cada veta rica es oro puro.',
    ]},
    {"id": 'c01', "frases": [
        'Número uno. Las misiones del cuarenta y ocho en adelante ahora pagan oro. Y no guardes misiones para el sesenta.',
        'En Classic, al llegar al sesenta, la experiencia de las misiones se convertía en oro. Y la gente guardaba misiones para cobrarlas al máximo.',
        'Forever quitó esa conversión. Blizzard explicó que, con ella, lo más rentable era matar bichos para subir y dejar las misiones para el final.',
        'Y como en el juego original solo una de cada cuatro misiones daba oro, el diez de noviembre hicieron un cambio enorme.',
        'Ahora la mayoría de las misiones de nivel cuarenta y ocho en adelante dan oro, incluso las que nunca lo dieron.',
        'Un jugador hizo un par de cientos de oro solo con las misiones del Monte Hyjal. Y muchas recompensas, además, el vendedor las paga a tres o cinco de oro.',
        'Y la cantidad de oro no cambia aunque ya seas sesenta. Así que no hay ninguna ventaja en guardarlas: cobras lo mismo hoy que mañana.',
        'Así que haz tus misiones en cuanto las tengas. Ya no hay premio por esperar. El premio es hacerlas.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esos son los treinta trucos para nunca quedarte sin oro en World of Warcraft Forever.',
        'Si te quedas con una sola idea, que sea esta: el oro no sale de un farmeo milagroso. Sale de pequeñas costumbres repetidas todos los días.',
        'No pagues lo que no usas, vende antes que los demás, y salta de mercado cuando todos llegan.',
        'Cuéntame en los comentarios cuánto oro tenías cuando llegaste al cuarenta, y cuál de estos trucos vas a probar primero. Todos se leen.',
        'Si este video te ahorró aunque sea una moneda, suscríbete y compártelo con ese amigo que siempre te pide oro prestado.',
        'Y recuerda que la economía de Forever tiene apenas dos semanas: todo lo que hoy vale, mañana puede valer la mitad. Sigue mirando la subasta.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # OST de WoW (musica_wow.py): nota = zona del tema; cada tramo <= 175 s
        (['intro', 'c30'], 'Ventormenta'),
        (['c29', 'c28', 'burla0'], 'Elwynn'),
        (['c27', 'c26'], 'Durotar'),
        (['c25', 'c24'], 'Baldíos'),
        (['c23', 'c22', 'c21'], 'Forjaz'),
        (['gracias1', 'c20', 'c19'], 'Posada'),
        (['c18', 'c17', 'burla1'], 'Orgrimmar'),
        (['c16', 'c15', 'c14'], 'Tuercespina'),
        (['c13', 'c12'], 'Mil Agujas'),
        (['c11', 'gracias2', 'c10'], 'Tanaris'),
        (['c09', 'c08'], 'Feralas'),
        (['c07', 'c06', 'burla2'], 'Legends of Azeroth'),
        (['c05', 'c04'], 'Roca Negra'),
        (['c03', 'c02'], 'Cuna del Invierno'),
        (['c01', 'cierre'], 'Ventormenta'),
    ],
)

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
