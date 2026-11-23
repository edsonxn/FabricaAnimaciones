# -*- coding: utf-8 -*-
"""GUION — «Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (Crónicas de Warcraft, 22-nov-2026; mié 25-nov 09:00 CDMX).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Tema elegido por el usuario (22-nov): una variable sobre «20 errores del 30 al 60» = la etapa (el 60, antes de las bandas del 9-dic).
Investigación: videos/_investigacion_wow_errores_60.md (nada de cifras fuera de ahí). La voz NO cita fuentes.
OVERGEAR campaña 3, integración 1: http://overgear.s.gy/CRONICAS/6 · CRONICAS10 · texto = traducción del promo aprobado por Alice
(videos/overgear_promo_en_c3/promo.py). Brief §7: «WoW Forever», sin tier lists, sin Heroico/M+, bandas fijas 10/20/40, sin BiS.
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras. Cifras en letra. DURACIÓN: MÍNIMO 25 min (el usuario).
Comentarios (≤ 10 días, ninguno usado antes): gracias1 @i.a.2.0.2.5 @Torrikus @AndresBece04 · gracias2 @ElTenienteDandadan @ZarguesRD29 ·
burla0 @alejandroquevedo5126 · burla1 @Jclothus · burla2 @rafaelvelizlazo4857 · correcciones @GespexpEkade @aztero8487 @sastakai.
"""

TITULO = "Los 25 ERRORES al llegar al nivel 60 en WoW Forever"
ARCHIVO = "wow_errores_60"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "The Burning Crusade": "de Bérnin Kruséid", "Blizzard": "Blízard", "Overgear": "Óverguir", "CRONICAS10": "Crónicas diez",
    "Azeroth": "Azeróth", "Kalimdor": "Kalímdor", "Onyxia": "Oníxia", "Drakkisath": "Drákisaz", "Gandling": "Gándlin",
    "Valthalak": "Valzálak", "Asharell": "Ásharel", "Nordrassil": "Nordrásil", "Archimonde": "Árchimond", "Bandalar": "Bandálar",
    "Sylvestris Dusksong": "Silvéstris Dásksong", "The Wild King": "de Uáild King", "Illidan": "Ílidan", "Sonya": "Sónia",
    "Well of Sorrow": "Uél of Sórrou", "Withermaw": "Uízermo", "Bonesnout": "Bóunsnaut", "Nara Wildmane": "Nára Uáildmein",
    "Mathrengyl Bearwalker": "Mázrenguil Béruoker", "Darnassus": "Darnásus", "Cinder": "Sínder", "Bolt": "Bólt",
    "Snowtalon": "Snóutálon", "Vitrix": "Vítrix", "Nanaya": "Nanáya", "Rhylin": "Ráilin", "Tiala": "Tiála", "Karazhan": "Kárazan",
    "Vaelan": "Váelan", "Rend": "Rénd", "Pix Xizzix": "Píks Síksiks", "Un'Goro": "Ungóro", "Azshara": "Asshára", "Hyjal": "Jáyal",
    "Stratholme": "Estrázolm", "Scholomance": "Escolománs", "Ventormenta": "Ventorménta", "Elixir": "Elixír",
    "Auctionator": "Ócsioneitor", "TSM": "te ese eme", "add-on": "ádon", "ChatGPT": "chat yi pi ti", "JcJ": "jota ce jota",
    "Gespexp": "Géspeks", "Aztero": "Aztéro", "Sastakai": "Sastakái", "Jclothus": "Yei Clózus", "Torrikus": "Tórrikus",
    "Dandadan": "Dandadán", "Zargues": "Zárgues", "Manuelito": "Manuelíto", "Remy": "Rémi",
}
FONETICA = FONETICA_APPLIO
CER_MAX_POR_FRASE = {   # 22-nov: hyps leídas una a una (nombres propios, JcJ, cifras)
    'c25_3': 0.14, 'c24_0': 0.03, 'c22_0': 0.03, 'c22_2': 0.05, 'c21_6': 0.05, 'gracias1_2': 0.03, 'c18_0': 0.06, 'c18_1': 0.08, 'c18_2': 0.035, 'c18_4': 0.055, 'c17_2': 0.06, 'c17_3': 0.04, 'c17_4': 0.03, 'c17_6': 0.04, 'c16_0': 0.055, 'c16_1': 0.045, 'c16_3': 0.085, 'c16_4': 0.045, 'burla1_1': 0.045, 'c13_3': 0.035, 'c13_5': 0.04, 'correc_1': 0.075, 'gracias2_2': 0.03, 'c08_2': 0.03, 'c08_5': 0.03, 'c06_0': 0.035, 'burla2_3': 0.035, 'c05_1': 0.095, 'c05_5': 0.025, 'c05_7': 0.025, 'c03_2': 0.03, 'c02_1': 0.035, 'c02_6': 0.03, 'c01_1': 0.065, 'c01_3': 0.05, 'c01_5': 0.05, 'c01_7': 0.025, 'c01_9': 0.035, 'burla1_2': 0.035, 'c08_1': 0.025, 'c04_1': 0.04,
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
    recorte_por={"scene-050": 0.13, "scene-051": 0.13},   # bandas negras de 135 px arriba y abajo (12,5 %) en las Islas Lanza Negra
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Faltan catorce días para que abran las tres bandas de World of Warcraft Forever. Y casi todo lo que haces hoy en el sesenta decide cómo te va a ir ese día.',
        'En la primera semana de Forever hubo ciento noventa y seis millones de muertes de jugadores. Las del nueve de diciembre van a ser las más caras.',
        'Porque las tres bandas reinician cada semana. El que llega mal preparado no pierde una noche: pierde una semana entera de botín.',
        'Y hay trampas nuevas: beneficios que se apagan en la puerta, mazmorras con tope por hora, y un botín que todavía no ha visto nadie.',
        'Blizzard dice que Forever tiene más gente jugando cada semana que World of Warcraft en quince años. Cada grupo de banda va a estar muy disputado.',
        'Ya hicimos los errores de los primeros niveles, y los del treinta al sesenta. Esta es la tercera parte: lo que pasa cuando por fin llegas al sesenta.',
        'Hoy te traigo veinticinco errores que se cometen al llegar al nivel sesenta en Forever, y cómo arreglar cada uno, del veinticinco al uno.',
        'Unos te cuestan oro, otros semanas, y el número uno te puede obligar a repetir mazmorras que ya habías terminado.',
    ]},
    {"id": 'c25', "frases": [
        'Número veinticinco. Cambiar un anillo sin leer el aviso de que no hay vuelta atrás.',
        'El trece de noviembre, Blizzard cambió dos anillos de Forever. Al Anillo de canalizador le quitó el espíritu y le puso poder con hechizos.',
        'Y a la Sortija de la Luz bendita le quitó el golpe. Y añadió algo raro: si tienes la Sortija, puedes cambiarla por el Anillo.',
        'Hasta que abran las bandas, ese cambio se hace con un vendedor, Pix Xizzix. Y Blizzard avisa que no se puede deshacer.',
        'El Anillo da intelecto, golpe y un poco de poder con hechizos. La Sortija da aguante, espíritu y hasta treinta y uno de sanación.',
        'Así que el sanador que la cambia porque el anillo es más nuevo, acaba de regalar su sanación a cambio de casi nada.',
        'El arreglo: pon los dos anillos uno junto al otro, piensa en tu especialización, y solo entonces pulsa el botón. Blizzard te avisó, y luego te puso el botón.',
    ]},
    {"id": 'c24', "frases": [
        'Número veinticuatro. Ignorar las tareas semanales del Campo de honor porque no eres de JcJ.',
        'Cada temporada de JcJ trae una ruta de tareas semanales que dan honor y puntos de rango. Y tres de ellas dan un punto de Legado.',
        'Y la primera es casi un regalo: ganar diez duelos. La segunda, completar tres batallas en la Garganta Grito de Guerra.',
        'La tercera ya pide más: matar a veinticinco jugadores de la otra facción en la misma Garganta.',
        'Mucha gente al sesenta solo mira la banda, y deja pasar semanas de tareas que se hacían en una tarde.',
        'La buena noticia es que, como van ligadas al Legado, Blizzard dice que se pueden completar en temporadas futuras.',
        'El arreglo: mira tu tarea de la semana aunque no te guste el JcJ. Diez duelos en la puerta de tu capital no le hacen daño a nadie. Bueno, a nueve personas sí.',
    ]},
    {"id": 'overgear', "post": 2.6, "frases": [
        'Y si estás llegando al sesenta, este es el momento en que un buen consejo vale más que cualquier lista. Para eso existe el patrocinador de hoy.',
        'Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.',
        'Son sesiones individuales por horas, por voz o por texto. Y juegas tú con tu personaje todo el tiempo.',
        'Un coach mira tus talentos, tu rotación y tus propios errores, con la versión del juego que está activa hoy.',
        'Porque las guías no siempre van al día. Una rama de talentos escrita antes del último ajuste ya puede estar desfasada.',
        'Y si todavía vas camino del sesenta, también te ayudan con eso.',
        'Y para las bandas del nueve de diciembre: resistencia al fuego para la Guarida de Onyxia, consumibles, y qué equipo previo a la banda vale la pena buscar.',
        'Si reservas dos horas o más, ahorras un cinco por ciento, con reembolso en cada pedido. Y lo que aprendes se queda contigo para el siguiente ajuste.',
        'El enlace está en la descripción, y hay un código para ti.',
        'Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.',
    ]},
    {"id": 'c23', "frases": [
        'Número veintitrés. Entrar a la Guarida de Onyxia sin conocer la pelea, porque es un solo jefe.',
        'La banda más grande del nueve de diciembre, la de cuarenta, se juega contra un solo jefe. Y pasa un buen rato de la pelea volando.',
        'Blizzard confirma que la pelea tiene tres fases. Y si Forever la deja como la conocíamos, cada fase tiene su trampa.',
        'En la primera, nadie se pone detrás, porque el coletazo te manda a volar. Y nadie pisa los nidos de los lados, porque de los huevos salen crías.',
        'En la segunda, Onyxia vuela. El que recibe la bola de fuego se aparta del grupo, y todos se mueven para no comerse su aliento.',
        'Y en la tercera llega el rugido que da miedo. Ahí es cuando alguien sale corriendo directo a los huevos, y la banda entera paga la cuenta.',
        'El arreglo: que los cuarenta vean la pelea antes, posiciones marcadas, y el que tenga miedo, que tenga miedo lejos de los nidos.',
    ]},
    {"id": 'c22', "frases": [
        'Número veintidós. Gastar el honor en equipo de JcJ sin entender los lacres envalentonados.',
        'El honor de Forever compra dos conjuntos de JcJ: uno azul y uno épico. Pero el épico no se compra directamente.',
        'El épico se hace con la pieza azul más un lacre envalentonado. Y cada lacre pide un rango de JcJ.',
        'Los de muñeca y cinturón piden rango ocho. El de cabeza, rango trece. Y las monturas de JcJ llegan con el rango once.',
        'El error es comprar la pieza azul, venderla porque te cayó algo mejor, y luego descubrir que el épico se construía encima de ella.',
        'El arreglo: compra las azules con honor y guárdalas en el banco. Son la base de tu conjunto épico, aunque hoy no las uses.',
    ]},
    {"id": 'burla0', "frases": [
        'Y antes de seguir, una crítica que se llevó seis me gusta.',
        'Alejandro escribió: hay un poco de video en tu inteligencia artificial.',
        'Alejandro, es lo más bonito que nos han dicho este mes. Hay inteligencias artificiales que no traen ni un poco de video.',
        'Y fíjate en las proporciones: un poco de video, mucha inteligencia. Igual que el sesenta en Forever: un poco de suerte, y mucha preparación.',
        'Seis personas te dieron la razón. Pero seis personas, Alejandro, en Forever no alcanzan ni para la banda de diez.',
    ]},
    {"id": 'c21', "frases": [
        'Número veintiuno. Creer que tu rango de JcJ es para siempre.',
        'En Forever el rango no funciona como antes. Un diseñador de Blizzard lo dijo claro: en cada temporada nueva, todo el mundo vuelve al rango uno.',
        'Además, el rango tiene un tope por semana. El que se pasa un fin de semana entero en los campos de batalla, choca con el techo.',
        'Según los datos del juego, ese tope empieza en el rango tres la primera semana, y no llega al catorce hasta la semana diez. Y el rango no baja si dejas de jugar.',
        'Y ojo con el Valle de Alterac: desde el diecisiete de noviembre, sus misiones piden nivel cincuenta y ocho.',
        'Y el campo de batalla nuevo, las Islas Lanza Negra, de quince contra quince, está frente al Marjal Revolcafango.',
        'El arreglo: JcJ un poco cada semana, mejor que atracones. El rango se reinicia, pero el equipo que compras se queda contigo.',
    ]},
    {"id": 'c20', "frases": [
        'Número veinte. Comprar los consumibles la última semana, cuando los compra todo el mundo.',
        'La economía de Forever empezó de cero el cuatro de noviembre. No hay precios de referencia, y los días antes de una banda nueva, todo sube.',
        'Y en Forever los consumibles pesan más que nunca, por un motivo que vas a ver en el número dos.',
        'Pociones de protección de fuego para Onyxia, pociones de maná y de curación sublimes, el Elixir de la mangosta, y comida con estadísticas.',
        'Y un detalle gracioso: la comida de Forever da un cinco por ciento de experiencia por muertes. Al sesenta, pagas por una experiencia que ya no existe.',
        'El arreglo: haz una lista corta para tu rol y cómprala ya. O mejor, si tienes alquimia o cocina, fabrícalo tú.',
    ]},
    {"id": 'c19', "frases": [
        'Número diecinueve. Llegar al nueve de diciembre sin oro para reparar.',
        'Nadie ha visto todavía los jefes de las dos bandas nuevas. Se van a descubrir a ciegas, y descubrir a ciegas significa morir muchas veces.',
        'En la primera semana de Forever hubo casi doscientos millones de muertes de jugadores. Cada una, con su factura de reparación.',
        'El que se gasta todo en la montura épica la semana anterior, llega a la primera noche de banda con la armadura en rojo.',
        'Y lo mismo con el botín: si el grupo no acuerda antes cómo se reparte, la primera pieza termina en discusión.',
        'El arreglo: aparta un dinero solo para reparar la primera semana, y deja escrito el reparto del botín antes del primer jefe.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y antes de seguir, gracias por los comentarios de esta semana.',
        'Un espectador nuevo nos escribió que se nota el cariño y el empeño que le ponemos a los videos, y se quedó como seguidor. Bienvenido, compañero.',
        'Torrikus dice que siempre es bueno enterarse de estos secretos. Y Andrés, después del video del treinta al sesenta, nos dejó esta: Arathi también es como Vietnam.',
        'Andrés, y eso que todavía no has hecho cola para la Cumbre de Roca Negra superior un sábado por la noche.',
    ]},
    {"id": 'c18', "frases": [
        'Número dieciocho. Ir a la Cima Hyjal creyendo que es la de The Burning Crusade.',
        'El nombre engaña a los veteranos. La Cima Hyjal era la banda de Archimonde en The Burning Crusade. Pero la de Forever es otra.',
        'Es de veinte jugadores, con trece jefes, en la cima del Monte Hyjal, junto a Nordrassil. Y Archimonde no está en ella.',
        'Empieza contra un guardián antiguo. Y luego se abren tres caminos, por las ruinas y bajo tierra, que hay que limpiar los tres antes del final.',
        'En los datos del juego hay nombres como Bandalar, Sylvestris Dusksong, o The Wild King, que probablemente es el último.',
        'Y un detalle: en los archivos de Forever existe un arma que se llama, literalmente, Arma inútil de la Cima Hyjal.',
        'El arreglo: cero tácticas de dos mil siete. Ve a descubrirla con tiempo: tres caminos, para un grupo nuevo, pueden ser tres noches.',
    ]},
    {"id": 'c17', "frases": [
        'Número diecisiete. No saber que las Cavernas del Túmulo tienen tres entradas.',
        'La banda de diez está escondida bajo Kalimdor. Fue la prisión de Illidan durante diez mil años.',
        'Y tiene tres entradas: desde el Monte Hyjal, desde Cuna del Invierno y desde el Bastión Faucenegra, que está al norte de la zona de Azshara. Cada una da a una parte distinta de la prisión.',
        'El error del nueve de diciembre ya lo estamos viendo venir: medio grupo esperando en Cuna del Invierno, y la otra mitad en Hyjal.',
        'Y dentro hay sorpresas. Según los datos, uno de los jefes es un pozo: Well of Sorrow.',
        'Y hay una moneda de oro de Sonya Sombrasanto, la jefa final, cuyo texto dice: esto no tiene sentido, ¿para qué voy a tirar una moneda a la fuente?',
        'El arreglo: decidid la entrada antes del día, y atad la piedra de hogar cerca de esa puerta.',
    ]},
    {"id": 'c16', "frases": [
        'Número dieciséis. Entrar al Bastión Faucenegra sin las misiones, y por un solo camino.',
        'Es la mazmorra nueva del cincuenta y cinco al sesenta: una ciudad furbolg en el norte de Azshara, más grande que Profundidades de Roca Negra.',
        'Cada bando tiene siete misiones para ella, que juntas dan más de ochenta mil puntos de experiencia. Y ningún dador está dentro.',
        'La primera empieza con Nara Wildmane, en Cima del Trueno, o con Mathrengyl Bearwalker, en Darnassus.',
        'Y otra misión pide un objeto de Withermaw y otro de Bonesnout, que están en caminos distintos. El que solo recorre uno, sale con la misión a medias.',
        'Y un detalle: el Bastión está en una entrada vieja de los Fauces de Madera que nunca se usó. Sus túneles más hondos llevan a las Cavernas del Túmulo.',
        'El arreglo: recoge todas las misiones antes de entrar, y recorre los dos caminos aunque tardes más.',
    ]},
    {"id": 'burla1', "frases": [
        'Y ahora, interrumpo el video para interactuar con la comunidad.',
        'Jclothus escribió: deja de interrumpir el video cada veinte segundos para interactuar con la comunidad, quiero ver el video, no saber lo que dijo Manuelito.',
        'Pues mira, Jclothus, entendido. Por eso hoy no leo a Manuelito: te leo a ti, que lo pediste con tanto cariño.',
        'Y para que veas que escuchamos: en este video los comentarios van en paradas cortas, con unos tres minutos de errores entre una y otra. Esta es una de ellas.',
        'Y ya se acabó. Manuelito, lo siento, hoy no sales.',
    ]},
    {"id": 'c15', "frases": [
        'Número quince. Entrar al Bancal del Creador sin los sesenta cristales.',
        'Es la otra mazmorra nueva, del cincuenta y ocho al sesenta: un lugar de los titanes al norte del Cráter de Un\'Goro, subiendo desde el Refugio de los Mariscales.',
        'Dentro hay cuatro consolas titánicas, una por color. Y cada una pide quince cristales de poder de su color para invocar a su jefe.',
        'Rojo para Cinder, de fuego. Amarillo para Bolt, de rayo. Azul para Snowtalon, de escarcha. Y el verde, probablemente, para Vitrix, de veneno.',
        'Con las cuatro consolas despierta la jefa final, Nanaya, que cambia de elemento cada veinticinco por ciento. Sin los cristales, te quedas en cinco jefes.',
        'Y un consejo: no metas cristales en la consola con bichos alrededor. El jefe aparece al instante, y se suma a la pelea.',
        'El arreglo: juntad quince de cada color en Un\'Goro antes de entrar. Los cristales de dos mil cuatro, por fin, sirven para algo.',
    ]},
    {"id": 'c14', "frases": [
        'Número catorce. Llegar al sesenta sin plan para la montura épica.',
        'La equitación del sesenta en Forever cuesta mil de oro, y la montura, doscientas más. Aunque hay guías que dicen que esas mil ya incluyen la primera montura.',
        'Haz la cuenta con mil doscientas, y si sobra, mejor. Con reputación honorable con tu facción, te ahorras un diez por ciento en las dos cosas.',
        'Y dos trampas de Forever. Desde el diez de noviembre, las monturas raciales de vendedor se ligan al recogerlas: ya no se compran para revender.',
        'Y hasta el diecinueve de noviembre, los cielonatos no recibían el descuento de honorable. Ya está arreglado.',
        'Para que te hagas una idea: un jugador llegó al sesenta con mil trescientas noventa y una de oro, sin farmear en serio. Llegar rico es llegar justo.',
        'El arreglo: llega a honorable antes de pagar, y empieza a juntar desde el cincuenta y cinco. Los colores extra, para después.',
    ]},
    {"id": 'c13', "frases": [
        'Número trece. Planear la banda con listas de botín sacadas de internet.',
        'En Forever, el botín de las bandas no está en las bases de datos. Los objetos de banda solo muestran sus estadísticas cuando alguien los despoja.',
        'Se calcula que hay más de doce mil quinientos objetos ocultos en los archivos del juego. Muchos, de banda.',
        'Así que si alguien te pasa la lista de lo que suelta cada jefe de la Cima Hyjal, esa lista se la inventó.',
        'Lo único que se sabe es que el primer conjunto se reparte entre las tres bandas, y que cada jefe tiene unos pocos objetos raros mucho mejores que el resto.',
        'Blizzard quiere que el botín sea una sorpresa. Así que cada primer jefe va a ser una caja sorpresa, con nueve personas mirándote.',
        'El arreglo: no te cases con ninguna lista. Acordad cómo se reparte, y descubrid el botín jugando.',
    ]},
    {"id": 'c12', "frases": [
        'Número doce. Farmear un fallo del juego creyendo que, si Blizzard lo dejó, es legal.',
        'El fin de semana del catorce al dieciséis de noviembre, en el Bastión Faucenegra, un grupo grande de enemigos normales soltaba el botín completo de un élite.',
        'Blizzard lo arregló el dieciséis. Y al día siguiente explicó que un par de cientos de jugadores, sabiendo que era un fallo, se pasaron horas farmeándolo.',
        'A esas cuentas les bloquearon la economía, les quitaron el oro, incluso el que sacaron vendiendo el botín al vendedor, y suspendieron a los que más abusaron.',
        'Eso sí, Blizzard aclaró que nadie tiene que preocuparse por aprovechar un fallo sin querer. El problema es seguir cuando ya sabes que es un fallo.',
        'El arreglo: si algo da diez veces más oro que todo lo demás, disfrútalo una tarde y repórtalo. No construyas tu montura épica sobre eso.',
    ]},
    {"id": 'correc', "frases": [
        'Y ahora, las correcciones de la semana, porque nos las mandan con razón.',
        'En el video del oro recomendé Auctionator, y en pantalla salieron imágenes de otro add-on, TSM. Gespexp nos lo marcó, y tiene toda la razón: fallo nuestro.',
        'Aztero nos recordó que el brujo también puede hacer los farmeos bajo el agua, porque tiene un hechizo para respirar durante diez minutos. Bien visto.',
        'Sastakai nos corrigió que, si te mata otro jugador, no pierdes durabilidad. Es verdad: la pierdes si te mata un bicho o un guardia, no otro jugador.',
        'Y una nuestra: en el video del treinta al sesenta dijimos que la misión del Lacre de Ascensión ya no daba el lacre. Las guías más nuevas dicen que sí lo da.',
    ]},
    {"id": 'c11', "frases": [
        'Vamos con el número once: ir a la Cumbre de Roca Negra superior con cinco y en verdes, porque un video dijo que era fácil.',
        'La Cumbre superior es especial: es la única mazmorra de diez jugadores del juego.',
        'Y en las dos primeras semanas de Forever estaba rota a favor de los jugadores. Los enemigos tenían mucha menos vida y hacían mucho menos daño de lo previsto.',
        'El diecisiete de noviembre, Blizzard lo arregló, y avisó que ahora hace falta un grupo completo de jugadores atentos para terminarla.',
        'Así que cualquier guía o video de antes del diecisiete que diga que la Cumbre superior se hace con cinco, está viejo.',
        'Y el veinte, de paso, arreglaron un pilar de piedra rebelde que dejaba atrapados a los jugadores. Un pilar rebelde, en una fortaleza de orcos.',
        'El arreglo: grupo de diez, tanques y sanadores de verdad, y alguien con el Lacre de Ascensión. De eso hablamos en el número cuatro.',
    ]},
    {"id": 'c10', "frases": [
        'Número diez. Terminar la sintonización de Onyxia y guardar el amuleto en el banco.',
        'Lo de empezar pronto la sintonización ya te lo conté. El error del sesenta es otro, y es más tonto.',
        'Terminas la cadena, te dan el Amuleto de Pirodraco, y lo metes en el banco para liberar un hueco de la bolsa.',
        'Pero para entrar a la Guarida de Onyxia, cada jugador tiene que llevar el amuleto encima. En la bolsa sirve. En el banco, no.',
        'Y es personal: no se comparte con tus otros personajes. Cada alt tiene que hacer su propia cadena.',
        'Y en Forever, el amuleto da diez de aguante y quince de resistencia al fuego. Así que la noche de Onyxia, mejor llévalo puesto.',
        'Es la única llave del juego que te puedes colgar del cuello para pelear contra la dueña de la casa.',
        'El arreglo: el amuleto vive en tu bolsa, y el día de la banda, en tu cuello.',
    ]},
    {"id": 'c09', "frases": [
        'Número nueve. Entrar a Onyxia sin resistencia al fuego, ni pociones de protección.',
        'Blizzard lo escribió en su anuncio de las bandas: hay que preparar resistencia al fuego antes de entrar, porque la pelea castiga a una banda que no está lista.',
        'Y en Forever hay resistencia al fuego en sitios que la gente vende o ignora. El Amuleto de Pirodraco da quince. El Lacre de Ascensión, diez.',
        'Y el conjunto de mazmorra, con solo dos piezas, da ocho a todas las resistencias. Sí, ese conjunto que mucha gente vende. Volvemos a él en el número uno.',
        'Y está la Poción de protección de fuego superior: absorbe entre mil novecientos cincuenta y tres mil doscientos cincuenta de daño de fuego, durante dos minutos.',
        'Y la Capa de escamas de Onyxia da dieciséis de resistencia al fuego. El problema es que se hace con una escama de Onyxia. Para protegerte de ella, primero hay que matarla.',
        'El arreglo: guarda cada pieza con resistencia, lleva el amuleto encima y varias pociones por cabeza. Cuánta resistencia hará falta, nadie lo sabe todavía: mejor que sobre.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y otra ronda de comentarios, porque se la ganaron.',
        'El Teniente Dandadan nos cuenta que antes de ver cada video se pide algo de comer y de tomar. Teniente, para este, pide para media hora.',
        'Y Zargues, con tres semanas en el juego, eligió sacerdote para curar, y ya sabe lo que es rezar para que al tanque le alcance la vida. Zargues, eso es ser sanador.',
        'Si este video te está ahorrando oro y semanas, suscríbete. Es gratis, y así no te pierdes lo que viene: las bandas del nueve de diciembre.',
    ]},
    {"id": 'c08', "frases": [
        'Número ocho. Apuntar a una banda que tu grupo no puede llenar.',
        'Las bandas de Forever son fijas. Las Cavernas del Túmulo, de diez jugadores y ocho jefes. La Cima Hyjal, de veinte y trece. Y Onyxia, de cuarenta jugadores y un solo jefe.',
        'No hay tamaño flexible. Si tu hermandad son catorce que se conectan siempre, Onyxia el nueve de diciembre es un sueño. Y la Cima Hyjal, de veinte, también.',
        'Y como las tres reinician cada semana, un grupo pequeño que siempre está vale más que uno grande que nunca se junta.',
        'Los desarrolladores dicen que las Cavernas del Túmulo se parecen más a Karazhan que a la Cumbre superior, y que un grupo armado al momento podrá terminarla tras unas semanas.',
        'El arreglo: arma un grupo fijo de diez para las Cavernas, suma gente para la Cima Hyjal, y para Onyxia, busca alianzas con otras hermandades.',
    ]},
    {"id": 'c07', "frases": [
        'Número siete. Dejar la herrería, la peletería o la sastrería por debajo de trescientos.',
        'Las recetas del conjunto de artesano de Forever, el que se fabrica, piden habilidad trescientos en una de esas tres profesiones.',
        'Los planos avanzados del campamento salen de jefes de mazmorra. Y cada profesión de fabricación da puntos de Legado a ciento cincuenta, doscientos veinticinco y trescientos.',
        'El que llegó al sesenta con la profesión en doscientos cuarenta, porque ya la sube luego, se va a encontrar el nueve de diciembre sin poder fabricar lo que su grupo necesita.',
        'La receta te pide reputación, una profesión al máximo, esencias que solo da la banda, y un encantador. Es el objeto más de equipo de todo Forever.',
        'El arreglo: sube tu profesión de fabricación a trescientos antes del nueve. Y si no tienes ninguna de las tres, busca un fabricante en tu hermandad.',
    ]},
    {"id": 'c06', "frases": [
        'Número seis. Ignorar a los Guardianes de Hyjal.',
        'Es una facción nueva de Forever, en el Monte Hyjal, para los dos bandos. Y esconde una regla que casi nadie conoce.',
        'Del conjunto de artesano, el que se fabrica, solo puedes llevar una pieza equipada. Para llevar dos, necesitas la Vaina de semilla reanimadora.',
        'Esa vaina la vende su intendente, Rhylin Espinapiedra, en la Cima de la Eternidad, por diez de oro. Pero pide reputación reverenciada.',
        'Y reverenciado son veintiún mil puntos de reputación. Hoy solo se conocen cinco misiones, que dan seiscientos cincuenta. El camino al reverenciado todavía no se sabe.',
        'Pagas diez de oro por una semilla caída de Nordrassil, solo para poder ponerte un pantalón más. Pero ese pantalón puede valer la pena.',
        'El arreglo: haz ya la cadena de Tiala Melenablanca, El bastón de la montaña, y apunta cada misión nueva de los Guardianes que aparezca.',
    ]},
    {"id": 'burla2', "frases": [
        'Y antes del top cinco, una crítica, de las que se agradecen.',
        'Rafael escribió: deja de hacer tus videos con guiones de ChatGPT, no dices nada en realidad.',
        'Rafael, en los últimos veinte minutos te he dicho cuántos cristales pide el Bancal, en qué rango sale cada lacre y cuánto absorbe una poción de fuego.',
        'Si eso es no decir nada, espera a escuchar lo que te dice la puerta de Onyxia cuando llegas sin el amuleto.',
        'Pero te doy la razón en una cosa: lo mejor está por llegar. Quédate al top cinco, y luego me dices cuál sobraba.',
    ]},
    {"id": 'c05', "frases": [
        'Número cinco. Farmear mazmorras sin contar el nuevo tope de cinco por hora.',
        'Al sesenta, todo el mundo farmea: Stratholme, Scholomance, Roca Negra, el Bancal del Creador.',
        'Y el veinte de noviembre, hace solo unos días, Blizzard cambió una regla: ahora puedes reiniciar y entrar a cada mazmorra cinco veces por hora. Antes eran diez.',
        'El que salía y reiniciaba como en las dos primeras semanas, ahora se queda en la puerta, con el aviso de que ha entrado en demasiadas estancias.',
        'Y otra regla: una mazmorra no da experiencia al grupo si alguien de él está más de doce niveles por encima de los enemigos.',
        'O sea, el sesenta que pasea a su alt de cuarenta y cinco le quita la experiencia a todo el grupo.',
        'En dos semanas, Blizzard pasó de diez a cinco. Farmear en Forever se volvió un ejercicio de puntualidad.',
        'El arreglo: pasadas completas en lugar de reiniciar cada diez minutos, y alterna mazmorras.',
    ]},
    {"id": 'c04', "frases": [
        'Número cuatro. Que nadie de tu grupo tenga el Lacre de Ascensión.',
        'La Cumbre de Roca Negra superior es la llave de medio sesenta. Dentro está el general Drakkisath, para Onyxia y para los petos del conjunto, y también Rend y Lord Valthalak.',
        'Y la puerta solo se abre si alguien del grupo tiene el Lacre de Ascensión. Basta con uno para abrirla para todos.',
        'Para conseguirlo necesitas un lacre sin adornar, que cae de los élites de la Cumbre inferior, y las tres gemas de sus generales.',
        'Y aquí está la trampa: las tres gemas en una sola pasada salen más o menos un cuatro por ciento de las veces. De media, son unas cinco pasadas.',
        'Y al final tienes que forjarlo en el Marjal Revolcafango, dominando a Brasaliza, un dragón anciano de nivel sesenta y uno. Lo apaleas hasta que te hace de soplete.',
        'Y en Forever, el lacre da además diez de resistencia al fuego, a la naturaleza y a la escarcha.',
        'El arreglo: que al menos dos de tu grupo fijo lo tengan, por si uno falta. Y empiézalo con Vaelan, en la Cumbre inferior.',
    ]},
    {"id": 'c03', "frases": [
        'Número tres. Vender al vendedor el botín de banda que nadie quiere.',
        'El conjunto de artesano de Forever, hombreras, guantes, piernas y botas, se fabrica con un material: la Esencia maleable de la Naturaleza.',
        'Y su texto en el juego es clarísimo: se consigue al desencantar objetos de la Cima Hyjal o de las Cavernas del Túmulo. Onyxia no cuenta.',
        'Las guías no se ponen de acuerdo en cuántas esencias pide cada receta: entre tres y ocho.',
        'Así que cada objeto de banda que acaba en el vendedor por unas monedas, es una esencia menos para tu conjunto.',
        'Y si la banda va sin encantador, no hay esencias para nadie. Es la primera vez que en Forever el encantador es parte del botín.',
        'El arreglo: lleva un encantador a cada banda nueva, y que todo lo que sobre se desencante. Nada de banda al vendedor.',
    ]},
    {"id": 'c02', "frases": [
        'Número dos. Farmear beneficios de mundo para la banda.',
        'El veterano llega al sesenta y hace lo de siempre: mata a Rend, se come la Serenata Cantaflor de Frondavil, pasa por La Masacre y por la Feria de la Luna Negra.',
        'Y entra a la banda brillando. Pero en Forever, los beneficios de mundo no funcionan en las bandas.',
        'El texto del de la cabeza de Onyxia lo dice al final: no surte efecto en estancias de banda.',
        'O sea: puedes matar a Onyxia, colgar su cabeza en la ciudad, y el beneficio se apaga justo cuando vuelves a entrar a su guarida.',
        'Y desde el diecisiete de noviembre, el Poderío de Ventormenta y la Bendición del Jefe de Guerra se cancelan siempre al morir.',
        'Lo bueno: Blizzard puso heraldos en Villadorada, Villa del Lago, Colina del Centinela y Cerrotajo, así que el beneficio de Rend te llega mientras subes.',
        'Y el Reubicador cronológico, que guardaba los beneficios para la banda, ahora guarda beneficios que en la banda no hacen nada.',
        'El arreglo: los beneficios de mundo, para subir alts y para farmear fuera. Para la banda, consumibles. Por eso el número veinte era tan importante.',
    ]},
    {"id": 'c01', "frases": [
        'Número uno. Vender las piezas del conjunto de mazmorra, y empezar la cadena del siguiente sin oro.',
        'El primer conjunto de mazmorra cae en Scholomance, Stratholme y Roca Negra. El casco lo suelta el Maestro oscuro Gandling, las piernas el Barón Osahendido, y el peto el general Drakkisath.',
        'Te cae un azul nuevo, mejor, y vendes la pieza del conjunto, o la desencantas, y ahí está justo el error que más cuesta.',
        'Porque la cadena del segundo conjunto, el que muchos llaman cero punto cinco, se las come. Vas entregando brazales, cinturón, guantes, botas, piernas y hombreras.',
        'Y al final, el casco y el peto. Si vendiste el casco, te toca volver a matar a Gandling hasta que lo suelte otra vez.',
        'Y la cadena es una vuelta al mundo: Tanaris, Stratholme con una carrera de cuarenta y cinco minutos, La Masacre, Roca Negra, Las Estepas Ardientes y la Cumbre superior.',
        'En total, unas doscientas veintisiete de oro. Y el brasero sagrado que necesitas pide reputación honorable con el Alba Argenta.',
        'En Forever hay un jefe nuevo en esa cadena: el Ejecutor Asharell, un élite de nivel sesenta y dos, con unos noventa y dos mil puntos de vida, en el sur de Las Estepas Ardientes.',
        'Y la novedad buena: en cada entrega eliges la versión de tu especialización. El druida elige entre cuatro, y el paladín y el chamán, entre tres.',
        'Y si matas a Lord Valthalak y sales sin usar su amuleto en el cadáver, hay que invocarlo otra vez. Terminar la cadena, eso sí, da un punto de Legado.',
        'El arreglo: guarda cada pieza del conjunto aunque no la uses, aparta unas doscientas treinta de oro, y llega a honorable con el Alba Argenta antes de empezar.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esos son los veinticinco errores al llegar al nivel sesenta en World of Warcraft Forever, del anillo que no tiene vuelta atrás al conjunto que no se vende.',
        'Faltan dos semanas para el nueve de diciembre. Y lo que hagas hoy en el sesenta decide si ese día entras a la banda, o te quedas en la puerta.',
        'Cuéntame en los comentarios en qué nivel vas, y a qué banda vas a ir primero. Todos se leen, y muchos acaban en el siguiente video.',
        'Si este video te sirvió, suscríbete y compártelo con tu hermandad. Para la banda de cuarenta, hacen falta treinta y nueve amigos más.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`; nota = tema (musica_wow.py)
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # OST de WoW (musica_wow.py): nota = tema; cada tramo <= 175 s (timeline del 22-nov, 1804,4 s)
        (['intro', 'c25'], 'Legends of Azeroth'),          # 0-120
        (['c24'], 'Orgrimmar'),                            # 120-172,5 (JcJ, duelos en la puerta)
        (['overgear'], 'Posada'),                          # 172,5-240 (suena la música de Overgear)
        (['c23', 'c22'], 'Roca Negra'),                    # 240-345 (Onyxia, lacres)
        (['burla0', 'c21'], 'Taberna orca'),               # 345-435
        (['c20', 'c19'], 'Ventormenta'),                   # 435-525 (subasta, reparar)
        (['gracias1', 'c18'], 'Claro de la Luna'),         # 525-610 (Hyjal, Nordrassil)
        (['c17', 'c16'], 'Cuna del Invierno'),             # 610-717,5 (Cavernas, Bastión Faucenegra)
        (['burla1', 'c15'], "Un'Goro"),                    # 717,5-817,5 (Bancal del Creador)
        (['c14', 'c13'], 'Elwynn'),                        # 817,5-925 (montura épica, botín)
        (['c12', 'correc'], 'Tanaris'),                    # 925-1022,5
        (['c11', 'c10'], 'Estepas Ardientes'),             # 1022,5-1130 (Cumbre de Roca Negra)
        (['c09', 'gracias2'], 'Vallefresno'),              # 1130-1227,5
        (['c08', 'c07'], 'Posada'),                        # 1227,5-1335 (hermandad, profesiones)
        (['c06', 'burla2'], 'Feralas'),                    # 1335-1425 (Guardianes de Hyjal)
        (['c05', 'c04'], 'Peste del Oeste'),               # 1425-1545 (Stratholme, Scholomance, Cumbre)
        (['c03', 'c02'], 'Roca Negra'),                    # 1545-1662,5 (Rend, beneficios)
        (['c01'], 'Estepas Ardientes'),                    # 1662,5-1765 (cadena del conjunto, Asharell)
        (['cierre'], 'Legends of Azeroth'),                # 1765-1804,4
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
