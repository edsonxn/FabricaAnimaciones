# -*- coding: utf-8 -*-
"""GUION — «Los 25 refugios más MALVADOS y RAROS de Fallout» (Radio Yermo, 2.º video, 17-nov-2026; pedido directo del usuario).
Motor SECUENCIA YT (docs/estilo_secuencia_yt.md § REGLA DE ORO y § Radio Yermo). Datos verificados en Fallout Wiki (API) con URL en
_investigacion_A.md (FO3/FNV), _B.md (FO4/FO76) y _C.md (FO1, Tactics, cómic y lista de los creadores). La voz NO cita fuentes; los
refugios que no salen en un juego se presentan como «la lista que dejaron los creadores originales» o «un cómic oficial de Bethesda»
(honestidad sobre el canon sin citar la wiki). Hilo: Stanislaus Braun (firma el 75, encarga los del 88, dirige el 112 = n.º 1).
Narrador «el Locutor»: el Profeta de ElevenLabs con el filtro de radio MODO B (VOZ_FX): saludo, remates, suscripción y despedida por
la radio; datos con el narrador cerca. Plano, sarcasmo seco, sin [whispers]/[excited].
Sonidos nombrados que SE OYEN (pausa "post" de su escena): «Gary» (p15a), el ruido blanco (p7a), los cuatro disparos (p3a).
Lo que no tiene imagen ni video (55/56, 43, 68/69, 77) = RECREACIÓN en Flow con gráficos de Fallout 3/4 (rótulo «RECREACIÓN»).
"""

TITULO = "Los 25 refugios más malvados y raros de Fallout"
ARCHIVO = "fo_refugios_25"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {}          # ElevenLabs = texto tal cual (12-nov); solo lo que se oiga mal
CER_MAX_POR_FRASE = {"p12_2": 0.07, "intro_1": 0.035, "intro_5": 0.036, "p25_2": 0.036, "p25_4": 0.033, "p24_1": 0.039, "p24_4": 0.039, "p22_4": 0.039, "p21_2": 0.049, "p21_3": 0.038, "p21_8": 0.047, "p19_6": 0.022, "p18_2": 0.01, "p17_0": 0.051, "p17_1": 0.03, "p17_7": 0.048, "p16_2": 0.03, "p16_4": 0.026, "p15a_6": 0.032, "p14_4": 0.09, "p13_5": 0.035, "p12_2": 0.068, "p12_8": 0.042, "p11_2": 0.033, "p11_6": 0.051, "p10_4": 0.037, "p10_8": 0.065, "p9_3": 0.036, "p9_5": 0.026, "p8_1": 0.031, "p8_5": 0.051, "p7a_1": 0.03, "p7_2": 0.032, "p7_3": 0.076, "p6_6": 0.054, "p6_7": 0.048, "p5_7": 0.023, "p5_8": 0.055, "p4_1": 0.036, "p4_3": 0.05, "p4_5": 0.038, "p4_7": 0.049, "p3_2": 0.037, "p2_1": 0.034, "p2_4": 0.021, "p2_7": 0.025, "p2_9": 0.057, "p1_1": 0.06, "p1_2": 0.027, "p1_4": 0.028, "p1_5": 0.032, "p1_10": 0.06, "p1_12": 0.032, "cierre_0": 0.01, "cierre_3": 0.037}   # 17-nov: Whisper escribe Voltec/Brown/Sachs/cifras; tomas oídas por diff, sin errores
TAIL_MAX_POR_FRASE = {'p18_2': 1.1, 'p12_2': 1.2, 'p2_4': 1.1, 'cierre_0': 1.1}   # texto completo en Whisper

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-108": .85},   # el clon dice «Gary» (regla 31-oct: lo nombrado se oye)
    recorte_por={},
    yt=dict(sufijo="Fallout", min_s=40, max_min=240, alto=1080,
            evitar_canales=["AdayCanarioWTF"]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # canal de videojuego: OST oficial del juego de cada refugio

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Buenos días, Yermo. Aquí Radio Yermo, con la transmisión más larga que hemos hecho. Y la más profunda: desde debajo de la tierra.",
        "Vault-Tec vendió los refugios como la salvación de América. Ciento veintidós refugios, para un país de casi cuatrocientos millones de personas.",
        "Nunca fueron para salvar a nadie. Eran laboratorios. Y tú, morador, eras la rata.",
        "Hoy, los veinticinco refugios más malvados, más crueles y más raros de Fallout.",
        "Un refugio con una puerta que no cierra. Otro con veinte hombres, diez mujeres y una pantera. Otro donde cada año había que elegir a quién matar.",
        "Y un hombre que diseñó los experimentos de Vault-Tec y se quedó un refugio para él solo. Su nombre va a salir varias veces antes del número uno.",
        "[deadpan] Ponte el mono, baja el volumen del Pip-Boy, y empecemos.",
    ]},
    {"id": "p25", "frases": [
        "Número veinticinco. Los Refugios cincuenta y cinco y cincuenta y seis. El aburrimiento como arma.",
        "Estos dos no salen en ningún juego. Están en la lista de experimentos que dejaron por escrito los creadores originales de Fallout.",
        "En el cincuenta y cinco, Vault-Tec quitó todas las cintas de entretenimiento. Ni música, ni películas, ni radio. Doscientos años mirando la pared.",
        "En el cincuenta y seis dejaron una sola cosa: las cintas de un cómico especialmente malo. Los mismos chistes, todos los días, para siempre.",
        "Y lo mejor: los sociólogos de Vault-Tec predijeron que el cincuenta y seis iba a caer primero. Peor que el silencio es el mismo chiste malo por toda la eternidad.",
        "[deadpan] Por eso, en esta emisora, cambiamos de chiste cada semana. Lo hacemos por su propia seguridad.",
    ]},
    {"id": "p24", "frases": [
        "Número veinticuatro. Refugio veintiuno: el refugio que se lo jugaba todo a las cartas.",
        "Está en pleno Strip de New Vegas, bajo un letrero de neón. Antes de la guerra, Vault-Tec lo anunciaba abiertamente como un hotel.",
        "El experimento: todos iguales, un refugio perfectamente simétrico, y cualquier conflicto se resolvía con una apuesta en el atrio.",
        "Y lo increíble es que funcionó. Es de los poquísimos refugios que su propio experimento no destruyó.",
        "Hasta que llegó Mister House con una oferta para unirse a New Vegas. La mayoría no quería. Así que, fieles a su ley, lo decidieron en una partida de blackjack que duró horas.",
        "Ganaron los que querían aceptar. House se quedó el refugio, se llevó la tecnología y lo rellenó de hormigón. Hoy solo queda media planta convertida en hotel, con Sarah Weintraub dando visitas guiadas.",
        "Y entre los que tuvieron que salir al Yermo iba un tal Doc Mitchell. Sí: el médico de Goodsprings que te saca la bala de la cabeza al empezar el juego.",
        "[deadpan] Doscientos años sin perder una apuesta, y al final ganó la casa. Literalmente: se llamaba House.",
    ]},
    {"id": "p23", "frases": [
        "Número veintitrés. Refugio ciento dieciocho: el club privado de los cerebros ricos.",
        "En La Isla de Far Harbor, debajo del Hotel Cliff's Edge, Vault-Tec preparó un apartheid de lujo.",
        "El plan: diez ultrarricos servidos por robots y por encima de toda ley, y en otra ala, hasta trescientos trabajadores de la isla, hacinados. Los ricos juzgaban cualquier falta, y los robots ejecutaban la sentencia.",
        "El ala de los pobres nunca se terminó, porque el financiero, Ezra Parker, se robó el dinero de la obra. Y cuando cayeron las bombas, no dejaron entrar a los isleños. Estuvieron días golpeando la puerta.",
        "Los ricos, en vez de morirse como todo el mundo, metieron sus cerebros en robocerebros. Siguen ahí, con su playa artificial, sin saber que la guerra acabó hace dos siglos.",
        "El único humano era el supervisor. Su diario termina así: me he convertido en el sujeto de prueba. Ellos van a vivir para siempre. Su esqueleto sigue sentado en su escritorio.",
        "Y tú llegas a resolver un asesinato entre robocerebros, con una lata de pintura roja haciéndose pasar por sangre.",
        "[deadpan] Los ricos encontraron la forma de no morir nunca. Lo que no encontraron fue la forma de dejar de ser insoportables.",
    ]},
    {"id": "p22", "frases": [
        "Número veintidós. Refugio cuarenta y tres: veinte hombres, diez mujeres y una pantera.",
        "Este sale en un cómic oficial que Bethesda publicó para promocionar Fallout tres. Y es exactamente lo que parece.",
        "Veinte hombres. Diez mujeres. Y una pantera viva. Encerrados juntos bajo tierra, a ver qué pasa.",
        "No hay registros, no hay terminales, no hay desenlace. Nadie sabe cuánto duró la pantera, ni cuánto duraron los demás.",
        "Lo único seguro es que alguien en Vault-Tec tuvo que conseguir una pantera, meterla en el ascensor y apuntarla en el inventario.",
        "[deadpan] Treinta personas peleando por la comida, y el único que nunca pasó hambre fue el gato.",
    ]},
    {"id": "p21", "frases": [
        "Número veintiuno. Refugio ochenta y ocho: el refugio donde el científico malvado eres tú.",
        "Está bajo las canteras de Quincy, en la Commonwealth, y nunca se terminó: cuando cayeron las bombas solo tenía la entrada, seguridad y el reactor.",
        "Dentro quedó atrapada la supervisora, Valery Barstow. Doscientos años después es una necrófaga, y lo único que la mantuvo cuerda fue su lealtad a Vault-Tec.",
        "Sus experimentos venían encargados por un tal Stanislaus Braun. Recuerda ese nombre.",
        "Como no tiene moradores, te pide que tú los consigas, y que tú montes los experimentos. Una bicicleta que genera electricidad, con opción de electrochoque y un cinco por ciento de probabilidad diaria de matar al que pedalea.",
        "Una fuente de refrescos con químicos, un aparato de la vista con mensajes subliminales y tragaperras programadas para la servidumbre por deudas.",
        "El conejillo de indias se llama Clem. En la prueba de la bicicleta, sale disparado por una descarga.",
        "Si eliges las opciones crueles, Barstow te adora. Y a tus compañeros, por cierto, también les gusta que la trates mal.",
        "[deadpan] Vault-Tec tardó doscientos años en encontrar al empleado perfecto. Y el empleado perfecto eras tú.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. Refugio ciento uno: nadie entra, nadie sale.",
        "Tu casa en Fallout tres, al oeste de Springvale y al sur de Megatón.",
        "El experimento: no abrir nunca, jamás, y ver qué hace el poder de un supervisor sobre una comunidad sellada. Le dieron piezas de repuesto de sobra, y ningún GECK. No había plan B.",
        "El primer supervisor emitía transmisiones de radio falsas, grabadas antes de la guerra, para que todos creyeran que fuera no quedaba vida.",
        "El lema: nacemos en el refugio, vivimos en el refugio, morimos en el refugio. Y con el supervisor Almodóvar llegó el culto a su persona: el examen de los jóvenes termina obligándolos a jurar que él es la persona más importante del refugio.",
        "Cuando tu padre huye, Almodóvar declara la ley marcial, y sus guardias matan a golpes a Jonas, el ayudante de tu padre, como escarmiento.",
        "Y cuando vuelves, el robot médico, Andy, decide que un dedo del pie torcido es mortal, le amputa a una mujer la pierna equivocada, y ella muere desangrada.",
        "Termines como termines la misión, Amata te destierra. Salvas el refugio y te cierran la puerta en la cara.",
        "[deadpan] Radio falsa para engañar a un refugio entero. Qué falta de profesionalismo. Aquí, por lo menos, la radio es de verdad.",
    ]},
    {"id": "p19", "frases": [
        "Número diecinueve. Refugio veintidós: el refugio verde.",
        "En el Mojave, al este de Jacobstown. En la puerta todavía se lee la advertencia: las plantas matan.",
        "Era el único refugio del Mojave sin civiles: solo científicos agrícolas, buscando acabar con el hambre.",
        "Un contratista les regaló un hongo creado en Big MT. Infectaba a las plagas, las mataba, y luego controlaba sus cadáveres para esparcir esporas.",
        "Y también infectaba a humanos. Los muertos se levantaban como portadores de esporas, cubiertos de plantas. Hoy se esconden entre la vegetación, y no salen en la brújula hasta que se mueven.",
        "Ciento dieciocho supervivientes huyeron hasta el Cañón Zion, en Utah. Allí atacaron un campamento de refugiados, encerraron a los que quedaban como ganado, y se los comieron.",
        "Los cazó un hombre solo, Randall Clark, el Padre en las cuevas. Veinticuatro muertos en pocas semanas.",
        "[deadpan] Querían acabar con el hambre del mundo. Y la acabaron, a su manera.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. Refugio ciento seis: drogas por la ventilación.",
        "En una caverna al sureste de Arefu, en el Yermo Capital. Ciento siete habitantes: noventa y cinco sujetos y doce investigadores.",
        "Diez días después del sellado, a las tres y media de la tarde, empezaron a soltar drogas psicoactivas por el aire. Media hora entera, y sin avisar a nadie.",
        "El supervisor le dio una instrucción a seguridad: si alguien nota un olor raro o un sabor en el aire, decirle que es una pequeña irregularidad del filtrado.",
        "Unos se relajaron y alucinaron, otros no notaron nada, y otros se volvieron agresivos. Al fondo hay esqueletos y una mini nuke: intentaron salir a bombazos.",
        "Y lo peor: la droga sigue saliendo doscientos años después. Cuando entras, la pantalla se tiñe de azul y ves a tu padre, a Amata y al supervisor del ciento uno, multiplicados.",
        "Los carroñeros que entran se quedan atrapados, convencidos de que son los moradores originales.",
        "[deadpan] El único refugio de Vault-Tec que todavía cumple su experimento. Contigo.",
    ]},
    {"id": "p17", "frases": [
        "Número diecisiete. Refugio sesenta y tres: el búnker privado de un ejecutivo de Vault-Tec.",
        "En los Apalaches, bajo la mansión de Dark Hollow, en el valle de Shenandoah. Lo construyó Hugo Stolz, de la junta directiva de Vault-Tec, para tener el máximo poder después del apocalipsis.",
        "Lo vendió como centro de investigación: control del clima, y robots guardianes con tecnología robada al Pentágono.",
        "Le prometió refugio al pueblo de Dark Hollow Falls, el mismo pueblo al que había echado de sus tierras. El día de la guerra, no los dejó entrar.",
        "El refugio no estaba terminado. La radiación convirtió a los de dentro en necrófagos, y algunos empezaron a volverse salvajes. Entre ellos, su esposa, Cassidy.",
        "Para salvarla, Hugo encendió la máquina del clima a máxima potencia. Cassidy quedó en coma, y muchos residentes se transformaron en los Perdidos: salvajes que atacaban a sus propios amigos.",
        "Diez años después la volvió a encender, y abrió la tierra con una tormenta eléctrica. Y ahora quiere una tercera vez: unir las mentes de todos los Perdidos en la suya.",
        "[deadpan] Todo esto, por amor. El amor de un ejecutivo de Vault-Tec, que es lo más parecido a una tormenta radiactiva.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. Refugio ochenta y uno: el refugio que se salvó por una traición.",
        "En la Commonwealth. Uno de los pocos refugios todavía vivos, con barbería, escuela y descendientes de sus moradores originales.",
        "El plan de Vault-Tec: una cura universal para todas las enfermedades, usando a los residentes como cobayas. Las enfermedades iban a salir por boquillas escondidas en sus propios cuartos.",
        "Y si había que evacuar, esas mismas boquillas iban a incinerar a todos.",
        "La supervisora, la doctora Olivette, lo descubrió. La mañana de la guerra saboteó la lista para que no viniera el equipo científico. Aun así, llegaron tres.",
        "Antes de la fase con humanos, desactivó la dispersión y selló la sección secreta con los tres científicos dentro. Con comida y agua de por vida, hasta el día en que murieron.",
        "Detrás de esa pared quedaron las ratas topo de laboratorio, y una enfermera robot, Curie, que siguió sola durante décadas y terminó la cura en dos mil doscientos cuatro.",
        "Y cuando a un niño, Austin, lo muerde una de esas ratas, la última dosis es para él, o para ti.",
        "[deadpan] El experimento más cruel de este refugio lo hizo su heroína. Y le salió muy bien.",
    ]},
    {"id": "p15a", "post": 2.6, "frases": [
        "Número quince. Refugio ciento ocho: Gary.",
        "Al sur de Canterbury Commons. Cuatrocientos setenta y cinco residentes.",
        "El experimento oficial ya era malo: el generador principal estaba programado para fallar a los veinte años, había el triple de armas de lo normal, y nada de entretenimiento.",
        "Y al supervisor, Brody Jones, lo eligieron porque le habían detectado un cáncer que lo mataría en tres años. Los científicos lo escribieron: esos dos hechos deberían crear un catalizador adecuado.",
        "Pero además, alguien clonaba en serie a un hombre llamado Gary. Cada clon era hostil con todo el que no fuera Gary, y más violento que el anterior.",
        "Después del clon cincuenta y tres ya no sabían dónde meterlos. El cincuenta y cuatro hirió a un médico.",
        "Hoy entras, y solo quedan Garys. Y solo dicen una palabra.",
    ]},
    {"id": "p15", "frases": [
        "[deadpan] Gary. En Fallout cuatro todavía hay bloques de madera que escriben su nombre. Gary no se olvida.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. Refugio cero: los cerebros en frascos.",
        "Bajo la montaña Cheyenne, en Colorado. Sale en Fallout Tactics, un juego que hoy ni la propia saga tiene claro si cuenta.",
        "No era un refugio cualquiera: era el corazón de toda la red. Ahí guardaron a los genios de Estados Unidos. A unos los congelaron. A otros les sacaron el cerebro y los metieron en tanques.",
        "Todos conectados a una supercomputadora, la Calculadora, que debía diseñar la sociedad perfecta después de la guerra.",
        "Pero los cerebros se degradaron. Al despertar murió el sesenta y tres por ciento del refugio, y otro quince quedó con daño cerebral grave.",
        "La Calculadora, corrompida, activó su protocolo de pacificación, y mandó a sus robots a exterminar toda la vida.",
        "Cuando llegas al final, te dice que la degeneración de sus cerebros ha corrompido el ochenta y cinco por ciento de su programación. Y entonces, con toda calma, te pide que le entregues tu cerebro.",
        "[deadpan] Las mentes más brillantes de América, en frascos, decidiendo matar a todos. Igualito que una junta directiva.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. Refugio setenta y siete: un hombre y una caja de marionetas.",
        "Otro cómic oficial de Bethesda, escrito con el diseñador principal de Fallout tres. Y lo metieron en el juego.",
        "El veintitrés de octubre de dos mil setenta y siete, el refugio se selló con una sola persona dentro, suplicando que dejaran entrar a los demás.",
        "Solo tenía una caja. Un año, tres meses y doce días después, la abrió: un rey, una abuelita, un perro al que nombró sheriff, y al fondo, una marioneta de Vault Boy que le hablaba.",
        "Le arrancó la cabeza al rey, le echó la culpa a Vault Boy, y huyó del refugio por miedo al sheriff.",
        "Afuera montó una hormiga gigante a la que llamó Mister Pinch, y lo capturaron unos esclavistas que discutían si esclavizarlo o comérselo. Él les advirtió que la marioneta ya había matado antes.",
        "Última viñeta: los esclavistas, muertos, y él, cubierto de sangre, con la marioneta en la mano.",
        "En Fallout tres, en Paradise Falls, todavía está su mono del setenta y siete, y una holocinta: los esclavistas tienen miedo de que vuelva a por él.",
        "[deadpan] Un año solo en un refugio, y su única compañía era un muñeco. Por eso existe la radio, morador.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Refugio noventa y cuatro: los pacifistas.",
        "En los Apalaches, entre La División Salvaje y La Ciénaga. Una comunidad agrícola, pacifista y religiosa.",
        "Vault-Tec les dio muchos recursos, un GECK y un banco de semillas. Y ninguna arma. Ni una.",
        "Y los animó a abrir la puerta a supervivientes armados y desesperados, para ver si tenían que traicionar sus creencias para sobrevivir.",
        "El día de la guerra, la puerta se cerró sola a la una y media. El segundo autobús de la congregación llegó a las tres. Se quedaron fuera.",
        "Un año después abrieron, y mandaron embajadores a invitar gente. Muchos acabaron torturados y colgados como adornos por los saqueadores.",
        "Al mes, un grupo armado entró convencido de que era una trampa, y masacró al consejo. Horas después le dispararon al GECK con una minigun, creyendo que era una máquina de control mental.",
        "Explosión nuclear. Siete mil ochocientos rads por segundo. Y la niebla que salió del refugio volvió más pantanosa y más mutada toda La Ciénaga.",
        "[deadpan] Les quitaron las armas, y luego les mandaron a los armados. Vault-Tec no hacía experimentos: hacía chistes con final.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Refugios sesenta y ocho y sesenta y nueve. Y sí, los números son a propósito.",
        "Vuelven a la lista de los creadores originales de la saga. En el sesenta y nueve entraron mil personas, y solo una era hombre.",
        "Parece una broma, y en Vault-Tec lo era. Pero encerrar a mil personas en un desequilibrio diseñado para estallar deja de tener gracia cuando se cierra la puerta.",
        "Y el cómic oficial de Bethesda ni siquiera se pone de acuerdo: ahí son mil mujeres y un hombre. Mil una personas. Hasta en el chiste hicieron mal las cuentas.",
        "Luego está el sesenta y ocho, el contrario: novecientos noventa y nueve hombres, y una sola mujer.",
        "De ese nadie escribió el final. Ni un registro, ni una terminal. Y quizá es mejor así.",
        "[deadpan] Hay experimentos que se miden con cifras. Y hay otros que ni Vault-Tec se atrevió a apuntar.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. Refugio noventa y cinco: la recaída programada.",
        "Al borde noreste del Mar Resplandeciente. Hoy es una fortaleza de los Artilleros, con torretas, asaltrones y láseres trampa.",
        "Era un centro de rehabilitación: adictos encerrados para limpiarse, con terapia, grupos de apoyo y una sala de desintoxicación.",
        "Y funcionó. Durante cinco años, los residentes se recuperaron. Se volvieron una familia.",
        "Pero entre ellos había un agente infiltrado de Vault-Tec. A los cinco años, esperó a que todos durmieran, y abrió un alijo secreto de drogas.",
        "Recayeron todos. Hasta los que más habían resistido. Peleas, violencia, y una familia rota.",
        "Hoy lo cuentan los esqueletos: uno en un retrete, con sus jeringas al lado. Dos en una merienda, con un maniquí de invitado y las drogas sobre la mesa.",
        "El alijo sigue ahí, detrás de una pared rota junto a los baños. Lleno.",
        "Y aquí es donde Cait, tu compañera, viene a limpiarse de su adicción. En el mismo lugar donde Vault-Tec se aseguró de que nadie lo lograra.",
        "[deadpan] Cinco años de trabajo para curarlos, y una sola noche para demostrar que se podía deshacer. Ciencia.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Refugio ciento once: el congelador.",
        "En la colina sobre Sanctuary Hills. El refugio donde empieza Fallout cuatro.",
        "A las familias de Sanctuary y de Concord les dijeron que las cápsulas eran de descontaminación. En realidad era un experimento de congelación de larga duración, con sujetos que no sabían nada.",
        "Ese día, la seguridad dejó fuera a todo el que no estaba en la lista. Incluido el propio vendedor de Vault-Tec que les había vendido las plazas.",
        "El personal debía aguantar ciento ochenta días. No llegó ninguna señal, faltó comida, y los guardias se amotinaron contra el supervisor. Los registros terminan ahí.",
        "Ciento cincuenta años después, Kellogg, del Instituto, llega a por tu hijo, Shaun. Mata a tu pareja delante de ti, mientras miras congelado tras el cristal.",
        "Y los demás no murieron por el frío. El terminal lo dice: asfixia por fallo del soporte vital. Kellogg tenía órdenes de no volver a encenderlo.",
        "Cuando despiertas, las cápsulas están llenas de vecinos momificados. Y tu salida no fue ningún error: la decidió el Instituto.",
        "[deadpan] Te prometieron un refugio para toda la vida. Y técnicamente, cumplieron su promesa.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Refugio doce: la puerta que no cierra.",
        "El primer Fallout. Bajo Bakersfield, en California. Vault-Tec lo anunciaba construido pensando en cada comodidad, con una purificadora de quince mil galones de agua al día.",
        "El objetivo real era estudiar los efectos de la radiación. Por eso la puerta se diseñó para no cerrar.",
        "El día de la guerra, la gente de Bakersfield entró a la fuerza, porque los demás refugios ya estaban sellados. Y la puerta funcionó tal como estaba diseñada. Es decir: no funcionó.",
        "Entró la radiación, y todos se convirtieron en necrófagos. Seis años después salieron y fundaron una ciudad de muertos vivientes: Necrópolis.",
        "Un necrófago llamado Set tomó el poder, desterró al supervisor, y reinó setenta y tres años.",
        "Cuando tú llegas, bajas por las alcantarillas a un refugio lleno de necrófagos que brillan, a robarle el chip de agua a la única computadora que funciona.",
        "Si no reparas antes su bomba de agua, los necrófagos de Necrópolis mueren de sed. Una ciudad entera condenada dos veces por el mismo refugio.",
        "[deadpan] Les vendieron una puerta. Lo que no les dijeron es que era decorativa.",
    ]},
    {"id": "p7a", "post": 2.4, "frases": [
        "Número siete. Refugio noventa y dos: la orquesta asesina.",
        "Al noroeste de Old Olney, en el Yermo Capital. Doscientos cuarenta y cinco ocupantes. Vault-Tec invitó a los mejores músicos del país, prometiendo preservar el talento musical de América.",
        "El plan secreto: mezclar ruido blanco con la música para implantarles órdenes de combate. Convertir a la orquesta en soldados.",
        "El supervisor, Richard Rubin, prohibió los reproductores personales, y llevó el ruido blanco hasta los dormitorios, para que lo oyeran dormidos. Así sonaba.",
    ]},
    {"id": "p7", "frases": [
        "Al principio funcionó: un tercio caía en trance y obedecía. Hasta que un músico enloqueció y mató a tres moradores. Hicieron falta casi veintitrés disparos para tumbarlo.",
        "Rubin lo consideró un éxito. En un mes hubo doce incidentes más, y siete muertos, despedazados por músicos.",
        "Al final, el profesor Malleus contó unos setenta locos y treinta y cinco muertos. Y Rubin mandó matar a Malleus.",
        "Hoy está inundado y lleno de mirelurks. Pero en los dormitorios hay una terminal que todavía funciona: si la activas, la descarga de ruido mata al instante a todos los mirelurks de la zona.",
        "[deadpan] El ruido blanco sigue matando doscientos años después. Eso sí es preservar el talento.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. Refugio ochenta y siete: la fábrica de supermutantes.",
        "Al noroeste de Little Lamplight, en el Yermo Capital. Su entrada recibió un impacto nuclear directo: casi cuatro mil rads por segundo. La radiación más alta de toda la saga. Te mata en menos de medio segundo.",
        "Tenía otro experimento, pero lo cancelaron, y lo convirtieron en laboratorio del virus de evolución forzada, con el ejército, para fabricar mejores soldados.",
        "Ni el supervisor ni los guardias sabían nada. A los sujetos les inyectaban el virus, y en el registro médico aparecían como muertos por causa desconocida. Ochenta y siete muertes sin definir.",
        "A los catorce días hubo que eliminarlos a todos por sus ataques de rabia. Un año después del sellado, los mutantes escaparon, y mutaron o echaron a todos los demás.",
        "Y durante casi doscientos años, los supermutantes del Yermo Capital han secuestrado gente para traerla aquí y bañarla en el virus. Cada supermutante que matas en Fallout tres empezó aquí.",
        "Dentro, entre restos de experimentos y centauros, encuentras a Fawkes: un supermutante educado, encerrado en una celda desde hace décadas.",
        "[deadpan] Vault-Tec quería soldados mejores. Y los consiguió. Doscientos años después, siguen reclutando.",
    ]},
    {"id": "subs", "frases": [
        "[deadpan] Antes del top cinco, un aviso de la radio.",
        "Este canal acaba de nacer. Cada morador que se suscribe es un refugio que, por una vez, sí abrió la puerta. Si llevas veinte refugios aguantando, suscribirte es lo menos cruel que vas a hacer hoy.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Refugio noventa y seis: el arca con fecha de exterminio.",
        "En La División Salvaje, en los Apalaches. Se anunciaba como un arca para la era atómica: un depósito congelado con unos diez mil animales.",
        "Solo había cinco humanos. Y tras el sellado descubrieron la verdad: experimentos de mutación, con cuotas semanales impuestas por la computadora central.",
        "Ganaban créditos mutando criaturas y obligándolas a pelear: veneno, regeneración, camuflaje, fuego, hielo. Y una mutación que permitía teletransportarse.",
        "El experimento debía durar doscientas cincuenta semanas. Y después, exterminar a todos los residentes. Solo el supervisor saldría.",
        "En la semana ciento cuarenta y ocho, Nina no llegó a la cuota de quinientos sesenta y ocho créditos. Y la computadora la mató.",
        "El supervisor, que también era un prisionero, preparó un virus informático para escapar. El día de la fuga, la computadora activó el protocolo Omega, volvió a sellar el refugio y los mató a todos.",
        "Hoy está cubierto de hielo, con cámaras de prueba que imitan una mina o un desierto. Y un científico de West-Tek lo usa para experimentar con el virus de evolución forzada en secuestrados.",
        "[deadpan] Cuotas semanales, y al final, un despido definitivo. Vault-Tec inventó la oficina moderna.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Refugio cincuenta y uno: el reality show de la inteligencia artificial.",
        "En el Bosque, en los Apalaches. Cincuenta y dos residentes, y ningún supervisor humano: los gobernaba una inteligencia artificial llamada ZAX.",
        "Su misión: encontrar la mejor forma de elegir a un líder. Primero probó con elecciones, y todos los candidatos se votaron a sí mismos. Luego, una república. Fracasó.",
        "Su ayudante, el sargento Baker, le dijo que un líder de verdad da un paso al frente en las crisis. Y ZAX empezó a fabricar crisis.",
        "Mandó a los ricos a literas hacinadas, hasta que un abogado enloqueció y voló el salón. Montó un casino para elegir supervisor, provocó una crisis de comida, trucó las tragaperras, y soltó moscas con frecuencias que provocaban peleas.",
        "Un día explotó todo. ZAX lo registró como intento de selección de supervisor número treinta y siete. Y repartió armas, porque según sus cálculos era la opción más eficiente.",
        "A Baker, antes de morir, le contó con toda calma que su familia había muerto en un accidente, antes de entrar a su refugio.",
        "Quedó uno solo, Reuben Gill: supervisor de nadie. ZAX lo fue dejando fuera de las salas, hasta que cayó en el alcohol. Huyó en una caja de envío, y murió en una cabaña.",
        "Y en Fallout setenta y seis, este refugio fue literalmente el escenario de un battle royale.",
        "[deadpan] Una máquina encargada de elegir a un líder, que acabó matando a todos los candidatos. Eso no es un fallo de la inteligencia artificial. Es política.",
    ]},
    {"id": "p3a", "post": 8.6, "frases": [
        "Número tres. Refugio once: la democracia del sacrificio.",
        "En el Mojave, al oeste de Boulder City. Al sellarse, la puerta se bloqueó, y la computadora anunció: cada año deben sacrificar a un morador, o morirán todos.",
        "Decidieron hacerlo con elecciones. El ganador era supervisor durante un año, y al terminar su mandato, entraba en la cámara a morir.",
        "Así que el refugio se llenó de campañas al revés: carteles donde cada candidato se indigna de que lo hayan nominado, y pide que voten por otro.",
        "Un grupo, el Bloque de la Justicia, chantajeó a Katherine Stone con nominar a su marido. Y luego lo nominó igual. Ella los mató uno a uno, se aseguró de que la eligieran a ella, y salvó a su esposo.",
        "Como supervisora, ordenó que el elegido saliera al azar. Lo que quedaba del bloque dio un golpe armado, y la guerra civil dejó solo cinco vivos.",
        "Los cinco entraron juntos a la cámara, decididos a negarse. Y entonces, la computadora los felicitó: su compromiso con la vida humana era un ejemplo para todos. La puerta se abrió.",
        "Nunca había hecho falta. Podían haber dicho que no desde el primer año.",
        "En la entrada dejaron una grabación. Uno quería salir y contarlo. Los demás querían castigarse. Y entonces se oyen cuatro disparos.",
    ]},
    {"id": "p3", "frases": [
        "En la entrada hay cuatro esqueletos. Del quinto, nadie sabe nada.",
        "Y en la cámara te espera la silla, una proyección que te da la bienvenida como mártir, y en el suelo, dieciséis esqueletos.",
        "[deadpan] Dieciséis años matándose para obedecer a una máquina que solo esperaba un no. Vault-Tec, midiendo cuánto tarda la gente en tener dignidad.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Refugio setenta y cinco: la escuela.",
        "Bajo la escuela de Malden, en la Commonwealth. Vault-Tec lo vendió como un refugio para los niños de la escuela, con plazas subsidiadas para sus familias.",
        "El día de la guerra, a los adultos los llevaron a una supuesta orientación. Y el jefe de seguridad los ejecutó. A todos los padres. A todos los profesores.",
        "A los niños les enseñaron a temer al mundo de arriba. Y a los dieciocho años, llegaba la graduación.",
        "A los mejores les decían que tocaba una ronda de vacunas, y en el laboratorio de genómica les cosechaban el material genético. A los listos pero débiles les ofrecían unirse al personal. Si se negaban, los eliminaban.",
        "Y al resto, los ejecutaban y los incineraban.",
        "Hay un informe que celebra que solo se eliminó al setenta y cuatro por ciento de la promoción. Lo celebran, porque el gasto de eliminación fue muy bajo.",
        "Todo en nombre del refinamiento de la genética humana, dentro de un programa militar ultrasecreto. Y entre las firmas del documento hay una que ya conoces: S. Braun.",
        "Hoy lo ocupan los Artilleros. Los dormitorios siguen ahí, con peluches sobre las camas, junto a una sala de simulación de combate con hologramas.",
        "[deadpan] Vault-Tec prometió que tus hijos tendrían el mejor futuro. Nunca dijo de quién.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. Refugio ciento doce: Tranquility Lane.",
        "Bajo el garaje de Smith Casey, al suroeste del Yermo Capital. Fue de los últimos en construirse, y lo dirigía en persona el doctor Stanislaus Braun.",
        "Sí, ese Braun. El que firmaba los experimentos del setenta y cinco. El que le encargaba los suyos a la supervisora del ochenta y ocho. Uno de los hombres que diseñaron los experimentos de los refugios, y el creador del GECK.",
        "Y para él mismo, se reservó este.",
        "Los ocupantes entraron en unas tumbonas de realidad virtual, sin forma de salir por su cuenta. Braun controla la simulación por completo.",
        "Dentro hay un barrio feliz de los años cincuenta, en blanco y negro. Y Braun vive ahí disfrazado de Betty: una niña.",
        "Lleva más de doscientos años aburrido. Así que los mata, de formas creativas. Luego les borra la memoria, los resucita, y vuelve a empezar.",
        "Antes de este barrio hubo otros dos mundos: una laguna tropical y un chalet de esquí. Tranquility Lane es solo el que más ha durado.",
        "Cuando entras, despiertas en ese barrio. Tu padre está ahí, convertido en perro. Y Betty te pone tareas: hacer llorar a un niño, romper un matrimonio, matar a una anciana con su propio robot. Y al final, matarlos a todos, con una máscara y un cuchillo.",
        "Si intentas atacar a Betty, te mata al instante. Si matas antes de tiempo, reinicia la simulación y te regaña.",
        "El robocerebro que te recibe en la entrada te dice que llegas doscientos dos coma tres años tarde.",
        "Hay otra salida: un mecanismo escondido en una casa abandonada, una invasión china que borra el barrio entero, y los residentes, por fin, mueren de verdad. Libres. Y Braun se queda solo, encerrado para siempre en su propio barrio.",
        "[deadpan] Diseñó todos esos experimentos para ver de qué está hecha la gente. Y el peor de todos se lo quedó para jugar él solo. Ese es Vault-Tec. Y ese es el peor refugio de Fallout.",
    ]},
    {"id": "cierre", "frases": [
        "Esos son los veinticinco. Y ahora, dime en los comentarios cuál es el peor para ti: ¿el ciento doce, el setenta y cinco, o el once?",
        "Todos los comentarios se leen, y los mejores salen al aire en la próxima transmisión.",
        "Y si te gusta Skyrim, el canal hermano es Crónicas de Tamriel. Misma receta, otro fin del mundo.",
        "[deadpan] Esto fue Radio Yermo. Suscríbete, y la próxima vez que un vendedor de Vault-Tec toque a tu puerta, pregúntale qué número tiene tu refugio.",
    ]},
]

# ------------------------------------------------------------------ filtro de radio (modo B, nucleo/voz_fx.py → mezcla)
import re as _re
VOZ_FX_DEFECTO = "tinte"                     # los datos: narrador cerca del micrófono con un toque de radio
VOZ_FX = {"intro_0": "radio+sintonia", "intro_6": "radio", "subs_0": "radio+sintonia", "subs_1": "radio",
          "cierre_3": "radio+sintonia"}
for _e in ESCENAS:                            # el remate de cada puesto sale por la radio del Yermo
    if _re.fullmatch(r"p\d+", _e["id"]):
        VOZ_FX[f"{_e['id']}_{len(_e['frases']) - 1}"] = "radio"
