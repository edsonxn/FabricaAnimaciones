# -*- coding: utf-8 -*-
"""GUION — «15 FARMEOS de ORO del 30 al 50 en WoW Forever» (Crónicas de Warcraft, 25-nov-2026; vie 4-dic 09:00 CDMX).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO, § KIT DE 4 ESTILOS y
§ CAMBIOS DEL USUARIO AL KIT del 25-nov: mapas originales con ícono en cada punto, madera en vez de holograma, caras, tooltips).
Tema (el usuario, 25-nov, con datos): una variable sobre «30 trucos de ORO» (34 mil) = el tema (trucos → LUGARES del 30 al 50).
Investigación: videos/_investigacion_wow_oro_30_50.md (nada de cifras fuera de ahí; las de jugadores: «a un jugador le…»).
La voz NO cita fuentes. Nada de exploits, baneos ni el add-on de cambio de capa.
OVERGEAR campaña 3, integración 3: http://overgear.s.gy/CRONICAS/8 · CRONICAS10 · texto = promo aprobado por Alice adaptado,
DESPUÉS del primer farmeo (regla del 25-nov: min 4-5). Brief §7: «WoW Forever», nada de «temporada», sin tier lists ni «mejor
clase», sin BiS, NADA contra comprar oro.
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras. Cifras en letra. DURACIÓN: ~28-30 min.
Comentarios (≤ 10 días, ninguno usado antes; ids en ESTADO.md): gancho @mfhm5700 y @azazelzepeda8883 · justa @carlocbravo ·
burla0 @lalo260988 · burla1 @Pkponcho · gracias1 @AlexAnder-z1i7l @davidgomez7997 @Rolazabal · gracias2 @Lunatic_WP @BiNWinslou.
Cada puesto cierra con "post": 6.5 = FICHA DEL FARMEO en pantalla (nivel, zona, qué se lleva, oro, dónde vender).
"""

TITULO = "15 FARMEOS de ORO del 30 al 50 en WoW Forever"
ARCHIVO = "wow_oro_30_50"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "CRONICAS10": "Crónicas diez", "Azeroth": "Azeróth",
    "Rizz Tornillosuelto": "Ris Tornillosuélto", "Benjy Wheeler": "Bényi Uíler", "Wheeler": "Uíler",
    "Gadgetzan": "Gádguetsan", "Theramore": "Terámor", "Desolace": "Desolás", "Nethergarde": "Nézergard",
    "Nazferiti": "Nasferíti", "Lethlor": "Lézlor", "Stagalbog": "Estágalbog", "Groddoc": "Gródok", "Mojache": "Mojáche",
    "Rog'mar": "Rógmar", "Kargath": "Kárgaz", "Sootfur": "Sútfer", "Luremaster": "Lúrmaster", "Grom'Gol": "Gromgól",
    "Lo'Grosh": "Logrósh", "Scorpok": "Escórpok", "Magram": "Mágram", "Zarpósea": "Zarpósea", "Mokk": "Mók",
    "Alterac": "Álterac", "Onyxia": "Oníxia", "Pkponcho": "Pekapóncho", "Rolazabal": "Rolasabál",
    "BiNWinslou": "Bin Uínslou", "Lunatic": "Lúnatic", "Azazel": "Azazél", "Polvomecha": "Polvoméche",
    "Stranglethorn": "Estránglezorn", "Remy": "Rémi", "clip bait": "clip béit", "Número once": "Número ónse", "haters": "jéiters",
}
FONETICA = FONETICA_APPLIO
CER_MAX_POR_FRASE = {   # 26-nov: hyps leídas una a una (cifras en número, nombres propios); p05_2 y resumen_3 = Whisper se come las cifras, comprobadas con prompt
    'reglas_5': 0.088, 'p15_4': 0.038, 'p14_6': 0.036, 'p13_0': 0.024, 'p13_4': 0.021, 'p12_0': 0.028, 'p12_7': 0.024, 'p11_3': 0.02, 'p10_0': 0.017, 'burla1_0': 0.03, 'p09_0': 0.019, 'p09_4': 0.017, 'p08_0': 0.027, 'p06_4': 0.027, 'p05_2': 0.271, 'p05_6': 0.017, 'p04_6': 0.053, 'p03_0': 0.022, 'p01_8': 0.031, 'p02_5': 0.026, 'p01_9': 0.029, 'resumen_0': 0.02, 'resumen_3': 0.172,
}
TAIL_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={"scene-073": 0.05, "scene-077": 0.05, "scene-078": 0.05, "scene-080": 0.05},   # marca de agua BANDICAM arriba al centro (26-nov)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Llegas al nivel cuarenta en World of Warcraft Forever, corres al instructor de equitación y abres la bolsa. La montura cuesta cien de oro.',
        'Y tu instructor de clase te recuerda que la doble especialización son otros cincuenta. Ciento cincuenta de oro, de golpe, en el mismo nivel.',
        'A un jugador le pasó justo eso: llegó al treinta y nueve con sesenta y siete de oro, y se puso a probar farmeos con cronómetro, media hora cada uno.',
        'Mientras tanto, en un cráter negro de Las Tierras Devastadas, aparece cada pocos minutos un buitre que deja, en promedio, casi una moneda de oro por muerte.',
        'Y en una cueva de Alterac que ninguna guía de subida pisa, hay vetas de cinco minerales distintos y un vendedor encerrado en una jaula.',
        'Hoy van quince farmeos de oro del treinta al cincuenta. Lugares concretos: qué matar, dónde, a qué nivel, cuánto da y a quién vendérselo.',
        'Del que menos rinde al que más. Y el número uno, te adelanto, no necesita ninguna profesión.',
    ]},
    {"id": 'reglas', "frases": [
        'Antes, dos comentarios que nos dieron la idea. En el video de los treinta trucos de oro, un espectador nos contó que llegó al cuarenta con montura y doble especialización.',
        'Y se quedó con tres de oro. Ahora va en el cuarenta y ocho con cien de oro, y esos cien ya tienen dueño: entrenamientos y profesiones.',
        'Y otro espectador, Azazel, nos escribió que sí hay farmeos ocultos: va en el treinta y tres con trescientos de oro, farmeando una hora al día un solo objeto, en una zona vacía.',
        'No nos dijo cuál. Así que hoy te damos quince, y si el suyo está en la lista, que nos avise.',
        'Tres reglas antes de empezar. Primera: desde el veinte de noviembre, cada mazmorra se puede reiniciar como mucho cinco veces por hora. El oro del treinta al cincuenta está en el mundo abierto.',
        'Segunda: lo que todos farmean se hunde en días. Los huevos gigantes pasaron de un oro a unas quince platas en una semana.',
        'Y aquí un espectador, Carlo, nos escribió que la subasta no paga mucho, y que muchas cosas valen lo mismo que en el vendedor.',
        'Tiene razón, y por eso en cada farmeo te digo primero lo que paga el vendedor.',
        'Porque el vendedor nunca te baja el precio. Y tercera regla: cualquier clase puede hacer los quince. Unas matan más rápido que otras, pero el buitre no pregunta qué eres.',
        'Y al final de cada farmeo vas a tener su ficha: el nivel, la zona, lo que se lleva, cuánto da y dónde venderlo.',
    ]},
    {"id": 'p15', "post": 6.5, "frases": [
        'Número quince. Los centauros del Poblado Magram, en Desolace, del treinta y tres al treinta y ocho.',
        'Es un campamento grande de centauros, con retadores, cazavientos y corremanadas, repartidos en varios grupos al sureste de la zona.',
        'Y está en la lista por una razón muy concreta: el veinticinco de noviembre, Blizzard anunció que los centauros del Poblado Magram ahora reaparecen más rápido.',
        'Más centauros por hora para quien hace sus misiones y para quien se queda a farmear. Todavía nadie ha medido cuánto oro dan con el cambio, así que serías de los primeros.',
        'Son humanoides, así que sueltan monedas y paño de seda, que el vendedor paga a una plata y media. Y hacia el treinta y cinco empieza a caer el tejido mágico.',
        'Ojo con sus hienas, las Zarpósea, que ya son del treinta y siete. Si vas justo de nivel, quédate en los grupos del borde del poblado.',
        'No pide profesión ni ruta: entras al poblado, matas, y cuando la bolsa se llena, sales a vender.',
    ]},
    {"id": 'p14', "post": 6.5, "frases": [
        'Número catorce. Las arañas de la Cueva Niebla Negra, en el Marjal Revolcafango, del treinta y cinco al treinta y ocho.',
        'Están fuera y dentro de la cueva, al norte del marjal, muy juntas y sin pegar fuerte: arañas Niebla Negra y ermitañas Niebla Negra.',
        'Sueltan dos grises que se apilan: la mandíbula de araña chorreando, a casi seis platas, y la punta de pata de araña dura, a casi cinco.',
        'Pero lo bueno son las dos sedas. La seda de araña espesa, a siete platas y media en el vendedor, y la seda de las Sombras, a diez.',
        'Y esas dos mejor no las vendas al vendedor: las piden los sastres para subir, y para piezas con daño de las Sombras.',
        'Hay pocas apariciones, unas cuarenta en total. Si encuentras gente afuera, métete a la cueva, que dentro hay un raro que suelta un verde.',
        'La Horda vende al lado, en el Poblado Murohelecho. La Alianza, en la Isla Theramore.',
    ]},
    {"id": 'overgear', "post": 2.6, "frases": [
        'Y antes del número trece, algo que ningún buitre suelta: saber jugar tu personaje, para matar más rápido y morir menos. Para eso existe el patrocinador de hoy.',
        'Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.',
        'Son sesiones individuales por horas, por voz o por texto. Y juegas tú con tu personaje todo el tiempo.',
        'Un coach mira tus talentos, tu rotación y tus propios errores, con la versión del juego que está activa hoy.',
        'Porque las guías no siempre van al día. Una rama de talentos escrita antes del último ajuste ya puede estar desfasada.',
        'Y si todavía vas camino del sesenta, también te ayudan con eso.',
        'Y para las bandas del nueve de diciembre: resistencia al fuego para la Guarida de Onyxia, consumibles, y qué equipo previo a la banda vale la pena buscar.',
        'En un video de farmeos, esto cuenta doble: cuanto más rápido matas, más oro por hora te deja cada uno de estos quince lugares.',
        'Si reservas dos horas o más, ahorras un cinco por ciento, con reembolso en cada pedido. Y lo que aprendes se queda contigo para el siguiente ajuste.',
        'El enlace está en la descripción, y hay un código para ti.',
        'Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.',
    ]},
    {"id": 'p13', "post": 6.5, "frases": [
        'Número trece. Los gorilas Velo de Bruma, en la Vega de Tuercespina, del treinta y dos al treinta y cinco, y sus ancianos al cuarenta.',
        'Tienen una ventaja que casi nadie ve: no hay misión de matarlos, ni para la Alianza ni para la Horda. Así que casi siempre están vivos, y sin nadie alrededor.',
        'Los jóvenes viven al oeste del Lago Nazferiti, en el norte de la selva. Los ancianos, en el Valle del Velo de Bruma, más al sur.',
        'Sueltan pelo de gorila para el vendedor, y el colmillo de gorila, que el vendedor te paga a sesenta y siete cobres. Pero la subasta paga bastante más.',
        'Porque una misión, La fiebre de Tuercespina, pide colmillos para invocar a Mokk el Salvaje en oleadas. Quien la intenta solo suele fallar, y vuelve a comprarlos.',
        'A un jugador le salieron entre cinco y seis de oro por hora, solo matando gorilas, con los precios del doce de noviembre.',
        'Un aviso: los gorilas del norte son pocos, unas catorce apariciones, así que el farmeo rinde cuando estás solo. Y si llega alguien más, baja a los ancianos.',
    ]},
    {"id": 'burla0', "frases": [
        'Y aquí va un comentario. En el video de los treinta trucos de oro, un espectador, Lalo, nos escribió: clip bait, todos saben eso.',
        'Tienes toda la razón, Lalo, todos lo saben. Por eso los huevos gigantes pasaron de un oro a quince platas en una semana: porque todos lo sabían.',
        'Así que hoy hicimos lo contrario: quince lugares que casi nadie farmea. Y si también te los sabes todos, avísanos, que te contratamos.',
    ]},
    {"id": 'p12', "post": 6.5, "frases": [
        'Número doce. Las tortugas brillavalva del Desierto de Sal, en Las Mil Agujas, del treinta al treinta y seis.',
        'Y no, no son las tortugas de Tanaris del video anterior: es otra zona, otro nivel, y otro objeto para el vendedor.',
        'Son lentas, no pegan fuerte, y en un tercio de las muertes sueltan el fragmento de caparazón moteado. El vendedor te lo paga a nueve platas.',
        'Además caen carne de tortuga y cola escamosa espesa. La carne de tortuga la compra la gente para una misión de cocina, y en la subasta vale más que en el vendedor.',
        'En promedio son unas cuatro platas por tortuga. A unas cien muertes por hora, cuatro de oro de botín, más las monedas.',
        'Los mordedores brillavalva están al este de las salinas, junto al Cráter de la Comadreja. Y para vender, el Circuito del Espejismo, ahí mismo.',
        'Un jugador lo resumió así: unas cuantas tardes de tortugas, y tienes la montura.',
        'Y si ya vas por el cuarenta y dos, la alternativa son los cavapozos Fangorroca del Marjal Revolcafango, a unas seis platas por muerte.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y gracias a quienes nos escriben: un espectador, Alexander, nos dice que estos videos le ayudan a aprovechar el poco tiempo que tiene para jugar.',
        'Otro, David, está seguro de que esta información le va a ahorrar a mucha gente tiempo y sufrimiento, y a él ya le sirvió. Y para otro, Rolazabal, estos sí son videos de calidad.',
        'Gracias a los tres. Todos los comentarios se leen, y muchos acaban en el siguiente video. Y si este te está sirviendo, suscríbete, que lo que viene paga más.',
    ]},
    {"id": 'p11', "post": 6.5, "frases": [
        'Número once. Los reptadores de arena de Claros del Río, la zona nueva de Forever, del treinta y seis al cuarenta y uno.',
        'Son los cangrejos de la costa, al sur del Puerto Polvomecha. Y sueltan carne de cangrejo tierna en cuatro de cada diez muertes.',
        'El vendedor te paga poco más de una plata por esa carne. Pero el doce de noviembre se vendía a catorce platas en la subasta. Así que esta no va al vendedor.',
        'La compran los cocineros, que prefieren pagar antes que pasar la tarde en la playa.',
        'Y si tienes la cocina en doscientos, la puedes guisar tú: a un jugador le dejaba unas veinticinco platas por cada guiso vendido.',
        'De paso, en el mismo puerto hay una misión con estos cangrejos, Sabores de mar, que pide carne de reptador de arena y ojos de múrloc.',
        'Y si ya vas por el cuarenta, los reptadores del sur de Tuercespina, cerca de Bahía del Botín, sueltan además almejas de boca grande. Y dentro de las almejas hay perlas.',
    ]},
    {"id": 'p10', "post": 6.5, "frases": [
        'Número diez. Las crías del Barranco Lethlor, en Tierras Inhóspitas, del cuarenta al cuarenta y cuatro.',
        'Son crías de dragón que escupen fuego, al este de la zona, alrededor del barranco. Y como son dragones, también sueltan monedas.',
        'Sueltan la glándula de llamas pequeña, que va en el ají aliento de dragón: la comida que te hace escupir fuego, muy usada en mazmorras.',
        'El vendedor te paga la glándula a dos platas y media. En la subasta llegó a valer unas diez.',
        'Y sueltan una mascota, el Vástago oscuro, una cría de dragón negro que te sigue a todas partes. El vendedor la paga a veinticinco platas, y la subasta, más.',
        'Además, una misión pide el corazón de draco negro, que cae muy poco: hay gente que mata más de cien crías por un solo corazón.',
        'Y a un jugador le daban unos treinta mil puntos de experiencia por hora al cuarenta. Oro y nivel a la vez, con vetas de mitril alrededor.',
        'Cuidado con los élites en el centro del barranco: las crías se farmean por los bordes.',
    ]},
    {"id": 'burla1', "frases": [
        'Y otro comentario. Un espectador, Pkponcho, nos escribió: buen video, pero qué pereza que te picas con tus haters, cada dos minutos hablando de ellos.',
        'Tienes toda la razón, Pkponcho, y para demostrártelo, en este video solo le contestamos a dos. Tú eres el segundo.',
    ]},
    {"id": 'p09', "post": 6.5, "frases": [
        'Número nueve. Los múrlocs del Pantano de las Penas, del cuarenta y uno al cuarenta y cinco.',
        'Hay cuatro tipos en la mitad sur de la playa, y un grupo grande hacia la Cueva Stagalbog: múrlocs de marisma, vomitatintas, comecarnes y oráculos.',
        'Todos pueden soltar la almeja de boca grande. Al abrirla siempre salen de una a tres carnes de almeja sabrosa, y a veces, una perla.',
        'La perla buena es la perla de oro. El veintidós de noviembre, un jugador la vendía a un oro con treinta platas. El vendedor solo te da un oro.',
        'Las demás perlas valen menos, la negra unas doce platas y la iridiscente unas ocho. Pero se van sumando.',
        'Además sueltan monedas, serviola moteada cruda, aceite de pescado, y verdes y azules ligados al equiparse. A ese jugador le cayeron unas botas épicas, que vendió en unos trece de oro.',
        'Y los oráculos sueltan una receta nueva de Forever, el té soleado, para la cocina en doscientos.',
        'Y la carne de almeja no la tires: desde el veintitrés de noviembre, sus recetas cuentan como comida de aguante.',
        'Empieza por la playa al cuarenta, junto al Puesto Juncobruma. La parte de la cueva, mejor más tarde, que ahí hay demasiados juntos.',
    ]},
    {"id": 'p08', "post": 6.5, "frases": [
        'Número ocho. Las hienas Llagapata de las Arenas Abisales, en Tanaris, del cuarenta y cuatro al cuarenta y seis.',
        'En las Arenas Abisales hay tantos rocs de fuego, que son de misión, como hienas. Y casi nadie mata a las hienas.',
        'Sueltan la melena espesa, a ocho platas en el vendedor, y la pata de trofeo grande, a nueve. Además, cuero grueso, carne de lobo rojo y carne de lobo tierna.',
        'Esa carne de lobo tierna la piden las guías de cocina. Un jugador la vendía a casi un oro el montón, el veintitrés de noviembre. El vendedor solo te da diecisiete platas.',
        'La ruta es un triángulo por los tres esqueletos de dinosaurio de las dunas. Y si pasa un roc, mátalo también, que suelta huevos gigantes.',
        'Ese mismo día, los huevos valían poco más de veinte platas. Ya no es el farmeo de antes, pero de paso suma.',
        'Para vender, Gadgetzan, al norte de las dunas, que es neutral para los dos bandos.',
        'Y la melena espesa también la sueltan los coyotes del número cuatro. Si estas dunas están llenas, ya sabes dónde más buscarla.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y gracias también a Brasil: un espectador, Lunatic, nos escribió en portugués que le gustó el video, que ganamos un suscriptor, y nos mandó un abrazo de los brasileños.',
        'Un abrazo de vuelta para Lunatic y para todo Brasil. Y otro espectador, BiNWinslou, nos dice que estos videos son muy buenos, con mucha información útil. Gracias, de verdad.',
    ]},
    {"id": 'p07', "post": 6.5, "frases": [
        'Número siete. Los gorilas y los osos del norte de Feralas, del cuarenta y siete al cincuenta.',
        'Tronadores Groddoc y patriarcas Cueracero, en la misma zona, alrededor de Los Dos Colosos.',
        'Aquí no hace falta ninguna profesión, porque los grises que sueltan los paga bien el vendedor.',
        'El hueso de oso grande, casi quince platas, y hasta cuenta como una maza gris. El mechón de pelo de gorila, más de once. La mandíbula de oso, casi nueve.',
        'Y luego el pelo de gorila burdo, la garra de oso indómito y el costillar de oso, de cinco a seis platas cada uno.',
        'Los gorilas son de la misión previa al Templo Sumergido, así que cuando hay gente haciéndola, reaparecen más rápido.',
        'Si vas por el cuarenta y uno, los simios Groddoc y los osos Cueracero del centro de la zona sueltan casi lo mismo, a menos nivel.',
        'La Horda vende en el Campamento Mojache, y la Alianza en el Bastión Plumaluna.',
    ]},
    {"id": 'p06', "post": 6.5, "frases": [
        'Número seis. Los jaguares del Pantano de las Penas, del treinta y seis al treinta y nueve. Probablemente el farmeo de montura más famoso de todos.',
        'Sueltan colas y bigotes de felino: la cola blanda larga, a ocho platas, y el bigote de cerdas, a más de siete. Y además, cuero y carne.',
        'Con desuello rinde más. Y como el pantano está lleno de hierbas, hay quien aprovecha para subir la herboristería al mismo tiempo.',
        'La Horda vende en Rocal, en medio del pantano. Y un aviso para la Alianza: por ahí patrullan guardias de la Horda que te marcan para el combate entre jugadores.',
        'Si hay mucha gente, tienes el plan B en Claros del Río: las cazadoras llanagreste, al sur de Rog\'mar, sueltan lo mismo.',
        'A un jugador le dejaban justo por encima de diez de oro por hora. Y si una zona está llena, vas a la otra.',
    ]},
    {"id": 'p05', "post": 6.5, "frases": [
        'Número cinco. Los elementales de roca de Tierras Inhóspitas, del treinta y siete al cuarenta y cuatro.',
        'El clásico de siempre para la montura. Y en Forever trae un empujón oficial: desde el trece de noviembre, los elementales de roca inferiores aparecen más seguido.',
        'Hay tres franjas. Los inferiores, del treinta y siete al treinta y nueve, junto a Kargath. Los normales, al sur, junto a la Explanada del Espejismo. Y los superiores, del cuarenta y dos, al suroeste.',
        'Sueltan grises de piedra que el vendedor paga bien: trozos de piedra lisa y dentada, piedra inerte y sal de roca.',
        'Y tierra elemental, en una de cada diez muertes. Ahora vale poco, pero cuando empiezan las bandas, la piden para piedras de afilar y pociones de protección.',
        'A un jugador le salían unos diez de oro por hora, solo en grises. Otro dijo que con ellos te garantizas la montura, y que el único problema es la gente.',
        'Para vender, la Horda tiene a Kargath, al oeste de la zona. Y la Alianza, los campamentos goblin del centro.',
        'Si llegas y está lleno, guarda la tierra elemental en el banco. Y el nueve de diciembre, mira qué precio tiene.',
    ]},
    {"id": 'p04', "post": 6.5, "frases": [
        'Número cuatro. Los coyotes de Claros del Río, del treinta y seis al cuarenta.',
        'Están al sur del Cortijo de Wheeler, en la zona nueva. Y reaparecen a lo loco: siempre hay unos cuatro vivos, así que matas, das la vuelta, y ya volvieron.',
        'Sueltan la cola tupida suave, a más de siete platas, y la melena espesa, a ocho. Además, colmillos, carne de lobo rojo y cuero.',
        'Y la cola tupida suave tiene un segundo comprador: es uno de los objetos que se canjean en la Feria de la Luna Negra.',
        'Un jugador lo midió con cronómetro, media hora, el veinte de noviembre: seis de oro con ochenta y cuatro platas. Entre trece y catorce de oro por hora.',
        'Era el jugador del treinta y nueve con sesenta y siete de oro. Y de los farmeos que probó, este fue de los que más le dieron.',
        'Hay un coyote con nombre, Sootfur, de una misión de Benjy Wheeler, el granjero. Y la zona se puede farmear en grupo, con el botín libre.',
        'Y desde ahí pasas directo a Tierras Inhóspitas, a los elementales del número cinco.',
    ]},
    {"id": 'p03', "post": 6.5, "frases": [
        'Número tres. La pesca de valijas en la costa de Tuercespina. Y sí, en el video de los treinta trucos ya hablamos de pescar en los restos flotantes.',
        'Pero desde entonces cambiaron dos cosas, y un jugador encontró cómo duplicarlo.',
        'Las valijas reforzadas con mitril salen de los restos flotantes, y también de los bancos de anguila escama pétrea.',
        'Dentro hay tejido mágico, cuero, paño rúnico, objetos verdes, alguna receta, y hasta bolsas de catorce casillas.',
        'El truco nuevo es un talento de Legado, el Maestro del cebo. Con sus dos rangos, cada pez que sacas con señuelo tiene la mitad de probabilidad de dar uno extra, también las valijas.',
        'Y se puede encadenar: a ese jugador le salieron cuatro valijas en un solo lance. Unos cuatro de oro por sacar un pez.',
        'Sin el talento sacaba unas quince valijas por hora. Con él, unas cuarenta. Y cada valija vale, en promedio, unas setenta platas.',
        'Resultado: ciento setenta de oro en tres horas y media, mientras subía la pesca del ciento cincuenta al doscientos veinticinco.',
        'Dos detalles más. Desde el dieciséis de noviembre, el expositor de pesca del campamento da señuelos a todos. Y el jarabe de caminar sobre el agua te deja pescar lejos de la orilla.',
        'La ruta: sales del Campamento Grom\'Gol, bajas por toda la costa oeste hasta Bahía del Botín, y vuelves. Las valijas se abren, y todo va al buzón.',
    ]},
    {"id": 'p02', "post": 6.5, "frases": [
        'Número dos. Las cuevas de ogros de las Montañas de Alterac, para quien va del treinta y cuatro al treinta y ocho, más o menos.',
        'Junto a los Dominios de los Aplastacresta, la fortaleza de los ogros, hay ogros normales y dos cuevas, una al norte y otra al sur.',
        'Y dentro hay vetas de hierro, de mitril, de veraplata, de oro y de plata, que reaparecen rápido. Con minería, aquí subes casi hasta el torio.',
        'En un solo rincón del mapa hay treinta y ocho vetas: once de oro, ocho de hierro, siete de plata, seis de mitril y seis de veraplata.',
        'Los ogros sueltan plata, paño de seda, grises y verdes. Y no hace falta irse a vender: cerca de la cueva del norte hay un vendedor gnomo, Rizz Tornillosuelto, encerrado en una jaula.',
        'Y en la misma zona de las vetas ronda un raro, Lo\'Grosh, que suelta una maza, El pacificador, que en la subasta vale mucho.',
        'Un jugador encontró las cuevas vacías, porque ninguna guía de subida manda ahí. Con minería, montura y botas de velocidad, le salieron unos treinta de oro por hora.',
        'Sin montura ni botas, de veinte a veinticinco. Un aviso: cerca de la fortaleza están los aplastadores y los magos, que son élite. Quédate en las cuevas.',
    ]},
    {"id": 'p01', "post": 6.5, "frases": [
        'Y número uno. Los destripadores negros de Las Tierras Devastadas, del cuarenta y seis al cincuenta.',
        'Son buitres carroñeros que viven entre el Alto de los Rapiñadores y la Serpiente Enroscada, en un paisaje de cráteres negros.',
        'Y sueltan la molleja de buitre. A un jugador le cayó en cuatro de cada diez muertes, y el veintitrés de noviembre la vendía a más de dos de oro cada una.',
        'Tan cara porque la piden dos misiones de la misma zona: El vigor del buitre, que pide diez, y El golpe decisivo, que pide dos.',
        'Ese jugador lo midió media hora: noventa y dos objetos, unos veintiún de oro. Unos cuarenta y uno de oro por hora, antes de la comisión de la subasta.',
        'Seis mollejas fueron la mitad de todo ese oro. Y sin ninguna molleja le habrían quedado unos diecisiete de oro por hora, que sigue siendo más que casi toda la lista.',
        'En promedio, casi noventa platas cada vez que matas un buitre. Y no hace falta ninguna profesión para sacarlo.',
        'Dos avisos. Solo hay unos treinta y dos puntos de aparición, así que hay competencia, y gana quien está encima. Y el precio de la molleja puede caer como cayó el de los huevos.',
        'De paso puedes desollar a los aguijoneros Scorpok y a las hienas risitas famélicas de la zona.',
        'La Alianza llega volando al Castillo de Nethergarde. Y la Horda, desde el vuelo del Pantano de las Penas.',
    ]},
    {"id": 'resumen', "frases": [
        'Y si los juntas, te queda una ruta del oro por nivel. Del treinta al treinta y cinco: las tortugas del Desierto de Sal, los gorilas de Tuercespina y los centauros de Desolace.',
        'Del treinta y cinco al cuarenta: las arañas del marjal, las cuevas de Alterac, los jaguares del pantano, los coyotes de Claros del Río y los primeros elementales de roca.',
        'Del cuarenta al cuarenta y cinco: las crías del Barranco Lethlor, los elementales superiores, los cangrejos del sur de Tuercespina y los múrlocs del Pantano de las Penas.',
        'Y del cuarenta y cinco al cincuenta: las hienas de Tanaris, los gorilas y osos de Feralas, y los buitres de Las Tierras Devastadas. La pesca de valijas, en cualquier momento.',
        'Y un consejo para todos: antes de guardar algo para la subasta, mira lo que paga el vendedor. A veces la diferencia son dos cobres, y a veces son dos de oro.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esos son los quince farmeos de oro del treinta al cincuenta en World of Warcraft Forever, del centauro que Blizzard acaba de acelerar al buitre que deja casi un oro por muerte.',
        'Ahora cuéntame en los comentarios en qué nivel vas, cuánto oro llevas, y cuál es tu farmeo secreto, Azazel incluido, que nos debe uno.',
        'Si este video te ahorra una tarde de farmeo, suscríbete y compártelo con tu hermandad. Y si alguien de tu hermandad llegó al cuarenta sin montura, ya sabes a quién mandárselo.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # OST de WoW (musica_wow.py) por zona; timeline del 26-nov (1501,88 s); cada tramo <= 175 s
        (['intro', 'reglas'], 'Legends of Azeroth'),      # 0-145
        (['p15'], 'Baldíos'),                             # 145-210 Desolace (centauros Magram)
        (['p14'], 'Humedales'),                           # 210-272,5 Marjal Revolcafango
        (['overgear'], 'Posada'),                         # 272,5-350 (suena la música de Overgear)
        (['p13', 'burla0'], 'Tuercespina'),               # 350-450 gorilas Velo de Bruma
        (['p12'], 'Mil Agujas'),                          # 450-520 Desierto de Sal
        (['gracias1', 'p11'], 'Tierras del Interior'),    # 520-617,5 Claros del Río
        (['p10', 'burla1'], 'Garganta de Fuego'),         # 617,5-705 Tierras Inhóspitas
        (['p09'], 'Humedales'),                           # 705-785 Pantano de las Penas
        (['p08', 'gracias2'], 'Tanaris'),                 # 785-882,5
        (['p07'], 'Feralas'),                             # 882,5-945
        (['p06'], 'Bosque del Ocaso'),                    # 945-1002,5 Pantano de las Penas (jaguares)
        (['p05'], 'Garganta de Fuego'),                   # 1002,5-1082,5 Tierras Inhóspitas
        (['p04'], 'Tierras del Interior'),                # 1082,5-1152,5 Claros del Río
        (['p03'], 'Tuercespina'),                         # 1152,5-1245 pesca
        (['p02'], 'Trabalomas'),                          # 1245-1327,5 Alterac
        (['p01'], 'Estepas Ardientes'),                   # 1327,5-1415 Las Tierras Devastadas
        (['resumen', 'cierre'], 'Legends of Azeroth'),    # 1415-1501,88
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
