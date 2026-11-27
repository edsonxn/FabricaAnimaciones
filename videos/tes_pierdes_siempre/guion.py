# -*- coding: utf-8 -*-
"""GUION — «Las 15 cosas de Skyrim que PIERDES para siempre» (Crónicas de Tamriel, 26-nov-2026, sale el sáb 28-nov 12:08 CDMX).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Datos de investigacion.md
(UESP, cada puesto con su URL, que van en la descripción; la voz NO cita fuentes, R22). Tema elegido por el usuario (R45:
canales/formula/cronicas_tamriel.md § FÓRMULA VIGENTE 26-nov). De 20 candidatos quedan 15: fuera el seguidor muerto
(tes_cosas_nunca), Arivanya (tes_misiones_nunca), la máscara de Nahkriin (tes_armaduras_poderosas, solo se recuerda en la
gema), Oghma (tes_misiones_imperdibles) y Tova (suicidio: riesgo para los anuncios).
Voz: SOLO EL PROFETA (cuenta 4), texto TAL CUAL sin FONETICA (docs/voz.md § DICCIONARIO, 12-nov). Turbo, sin [whispers]/[excited].
Comentarios (R18 + R46, ninguno usado antes; `fab.py yt repetidos tes_pierdes_siempre`):
  críticas con contraburla: @elianalera1925 (cr1, «¿no te gusta hacer nada divertido?»), @AdonsAdndna (cr2, «Eres un llorón»),
  @antonigirii (cr3, «ChatGPT, secretos que TODOS conocen»);
  agradecimientos (≤ 10 días): @SrUnknown32, @JosueAlejandroPachecoBastidas, @creepynoodlesuvu, @sebastianmerino5943, @achezeta5497.
Campaña de suscripción antes del top 3 (13 de cada 100; 7 100 → 10 000). Radio Yermo en el cierre (R06).
"""

TITULO = "Las 15 cosas de Skyrim que PIERDES para siempre"
ARCHIVO = "tes_pierdes_siempre"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {}   # ElevenLabs: texto tal cual (12-nov); solo se añade un nombre que se OIGA mal al revisar

CER_MAX_POR_FRASE = {"p14_0": 0.033, "p14_5": 0.018, "p14_6": 0.029, "p12_1": 0.021, "p12_3": 0.02, "ag1_2": 0.056, "p11_3": 0.014, "p10_1": 0.042, "p10_2": 0.051, "p10_5": 0.016, "p9_0": 0.033, "p9_1": 0.051, "p9_2": 0.018, "p9_3": 0.025, "p9_4": 0.041, "cr2_0": 0.018, "p8_0": 0.039, "p8_2": 0.018, "p8_7": 0.017, "p7_2": 0.057, "p6_1": 0.05, "p6_7": 0.061, "p5_1": 0.029, "p5_2": 0.019, "p5_6": 0.047, "p4_1": 0.03, "p4_2": 0.047, "p4_5": 0.044, "p4_6": 0.024, "p4_7": 0.021, "p3_4": 0.022, "p3_5": 0.044, "p3_8": 0.017, "p2_5": 0.022, "p2_7": 0.04, "p1_0": 0.113, "p1_1": 0.03, "p1_3": 0.035, "gema_0": 0.032, "gema_1": 0.056, "gema_2": 0.067}   # 26-nov: nombres propios que Whisper escribe distinto (Talmor, Nacrin, jarl→Harl), leídos uno a uno
TAIL_MAX_POR_FRASE = {"p14_5": 0.52, "p14_6": 0.51, "p12_1": 0.78, "p12_3": 0.93, "ag1_2": 0.67, "p11_3": 0.46, "p10_1": 0.53, "p10_2": 0.74, "p10_5": 0.67, "p9_1": 0.46, "p9_2": 0.61, "p9_3": 0.46, "p9_4": 0.5, "cr2_0": 0.54, "p8_2": 0.6, "p7_2": 0.45, "p6_1": 0.83, "p5_1": 0.45, "p5_2": 0.58, "p5_6": 0.65, "p4_1": 0.79, "p4_2": 0.47, "p4_6": 0.6, "p4_7": 0.47, "p3_4": 0.87, "p3_5": 0.76, "p2_5": 0.65, "p2_7": 0.55, "p1_1": 0.66, "p1_2": 1.12, "p1_3": 0.49, "gema_1": 0.68, "gema_2": 0.5}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-071": .8, "scene-074": .8, "scene-120": .8, "scene-127": .8},   # 26-nov: Fus Ro Dah e Invocar tormenta se OYEN (R16/R17); 003, 011 y 130 fuera: sus fuentes traen narrador (Whisper)
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["F2 Walkthrough", "Samyoline", "Nichstaroni", "PrettyTigerlilly", "BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29", "Xander Rey Gaming",
                            "AtariGen 75", "NOB NO13", "Zephyr", "A Bard's Ballad", "Cameron Marks", "Gameplay Only", "Zboy896 Twitch Stream",
                            "Ambou", "StraightUpIrish", "Imperial Knowledge", "Unique Fantasy Battles", "FudgeMuppet", "Camelworks NEW", "Systill", "VGM Vega", "Anna Castiglioni", "Mike Is Modding", "ARCTIC", "Swtor Nerd Gaming", "Magicka Addict", "StillLearning1981", "Leminox", "Master Neloth", "Ritchromatic", "TheGrizzlyNinja", "Pysix", "ThePostalGamer", "Jim", "Gaming 2 Relax"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (Jeremy Soule; armar_musica_ost.py), sin pistas con canto

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Un bastón que vale mil cuatrocientas monedas de oro. Y lo usas una sola vez: de llave.",
        "Un fuerte entero, con cuatro maestros, dos perros y un trol con armadura. Y lo pierdes por decirle que sí a un vampiro.",
        "Y una tormenta de rayos a la que le falta la última palabra, porque el muro estaba en un templo al que ya nunca vas a volver.",
        "Hoy, las quince cosas de Skyrim que pierdes para siempre. Sin consola, sin trucos y sin vuelta atrás. Dónde están, cómo se pierden, y cómo no caer.",
        "[sarcastic] Y quédate hasta el final, porque te voy a enseñar el único lugar de Skyrim que te roba tres cosas de golpe.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Las colmenas de Brillo Dorado.",
        "Es un encargo del Gremio de Ladrones. Brynjolf te manda a la Hacienda Brillo Dorado, una isla al oeste de Riften.",
        "La hacienda le da miel a Maven Black-Briar, la mujer que manda en Riften. Y el gremio quiere darle un susto.",
        "La orden: quemar tres colmenas, abrir la caja fuerte, y volver.",
        "Y aquí cae media humanidad. Si quemas más de tres, Brynjolf te dice que te olvides de tu parte. Cero monedas.",
        "Y el fuego se contagia de casa en casa: con un solo hechizo de área o un grito de fuego, ya quemaste a cinco sin querer.",
        "Si obedeces, la paga es oro que crece con tu nivel. Si no, ni una moneda.",
        "Cómo no caer: nada de hechizos de área ni gritos de fuego. Una colmena, otra, otra, y te vas.",
        "[deadpan] Es la única vez en todo Skyrim que el juego te pide moderación. Y justo con el fuego.",
    ]},
    {"id": "cr1", "frases": [
        "Y esto va para Eliana Lera, que me preguntó si no me gusta hacer nada divertido.",
        "[sarcastic] Quemar una isla entera es muy divertido. Pero en Skyrim, la diversión te la cobran. Por eso existe este video.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. La Embajada de Thalmor.",
        "En la misión principal te cuelas en la fiesta de Elenwen, al noroeste de Soledad. Un elfo del servicio, Malborn, te mete el equipo a escondidas.",
        "Es la única vez que entras al edificio por la puerta. Si vuelves después, puedes pisar el patio y el cuartel. El edificio, no.",
        "Así que lo que no saqueaste esa noche se queda ahí para siempre, y no hay ningún truco raro que lo arregle.",
        "Hay trucos para volver a entrar: con un caballo, un árbol, o un plato bien colocado. Pero eso ya es escalar paredes, no jugar.",
        "El solar de Elenwen, sus despachos, cada cofre del edificio. Esa noche, o nunca.",
        "¿Y Malborn? Se juega la vida por ti, te paga, sale corriendo hacia el este, y desaparece del juego.",
        "[sarcastic] Arriesga el cuello por ti, y su premio es evaporarse. Así se trata a los aliados en Skyrim.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. Sven, o Faendal. Uno de los dos.",
        "En Cauce Boscoso hay un triángulo amoroso: Camilla, y dos pretendientes. Sven, el bardo. Y Faendal, el elfo arquero.",
        "Uno de ellos te pide que le entregues a Camilla una carta de amor falsa, firmada por el otro. Y tú decides a quién traicionar.",
        "Hagas lo que hagas, Camilla se queda con uno de los dos. El que gana te aprecia y se puede ir contigo como seguidor, el traicionado te odia, y tener a los dos de amigos es imposible.",
        "Y no son iguales. Faendal, además, entrena Arquería. Y para un arquero que empieza, eso vale oro.",
        "Cómo no caer: decide antes de tocar la carta a quién quieres a tu lado. Después, ya no hay marcha atrás.",
        "[deadpan] La primera decisión moral de muchos en Skyrim: arruinarle una cita a alguien por veinticinco monedas.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. El salón de Thirsk, en Solstheim.",
        "Dos misiones en el mismo salón de aguamiel. En una, ayudas a los nórdicos a recuperarlo. En la otra, ayudas a los rieklings que lo ocupan.",
        "Y solo puedes terminar una: completar una hace fallar la otra. No hay forma diplomática de dejar contentos a todos.",
        "Con los nórdicos ganas un entrenador maestro de Armadura pesada, y la forja del salón. Con los rieklings, ganas un riekling. De seguidor.",
        "Hay una salida a medias: puedes hacer los dos primeros encargos del jefe riekling, y cambiarte de bando antes del tercero.",
        "[deadpan] Un maestro de Armadura pesada, o un duende azul con lanza. Y hay gente que elige al duende. Yo la respeto.",
    ]},
    {"id": "ag1", "frases": [
        "Antes de seguir, gracias a los que comentan. Los leo todos, y muchos ya cambiaron cómo hacemos estos videos.",
        "Un veterano, SrUnknown, volvió a jugar Skyrim por cuarta vez, y dice que todavía aprende cosas nuevas. Y Josué Alejandro, lo mismo: después de tanto tiempo, el juego aún tiene algo que enseñar.",
        "Otro de ustedes, que se llama Creepy Noodles, sigue el canal desde sus inicios; Sebastián Merino nos pone de fondo mientras trabaja, y achezeta se acaba de suscribir hace poco.",
        "[deadpan] Sebastián, si tu jefe pregunta, esto es capacitación.",
    ]},
    {"id": "p11", "frases": [
        "Número once. La paz de Alto Hrothgar.",
        "En la misión principal sientas a imperiales y capas de la tormenta en la misma mesa, para firmar una tregua.",
        "Y en esa mesa se reparten comarcas. Según cómo quede el reparto, un logro, el de conquistar un fuerte, puede volverse imposible.",
        "El logro pide tomar el Fuerte Sungard, si vas con los capas, o el Fuerte Greenwall, si vas con el Imperio.",
        "Y si la Cuenca pasa a los capas de la tormenta, muere Ondolemar, el justiciar thalmor de Markarth. Aunque sea por la tregua.",
        "La recompensa de la tregua es un grito, Llamar dragón. Pero el precio lo decide la mesa.",
        "Para no perder nada, toma el fuerte de tu bando antes de la reunión, y mira bien qué comarca se entrega.",
        "[deadpan] Firmas la paz, y alguien muere igual. Diplomacia nórdica.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. El Salón de los Vigilantes.",
        "Es el refugio de los Vigilantes de Stendarr, en El Pálido, al sur de Lucero del Alba. Ahí está Custodia Carcette, que entrena Restauración a nivel experto.",
        "Pero tiene fecha de caducidad. Con Dawnguard instalado, cuando llegas a nivel diez, o cuando empiezas Dawnguard, los vampiros lo arrasan. Todos mueren.",
        "El salón queda en ruinas. Y no hay forma de salvarlos: está escrito.",
        "Y con ellos se va todo: sus cofres, sus libros, y su entrenadora.",
        "Ojo: sin Dawnguard instalado, el salón sigue en pie para siempre. El problema es el DLC.",
        "Está en el camino entre Lucero del Alba y Carrera Blanca, y casi nadie pasa por ahí a tiempo para encontrarla.",
        "Si quieres su entrenamiento, o lo que guardan, tienes que ir antes del nivel diez.",
        "[sarcastic] Es el único edificio de Skyrim que caduca según tu nivel. Como un yogur.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Los encargos de los jarls.",
        "En la guerra civil, cada comarca que conquistas cambia de jarl. Y el jarl que cae se va. Con sus encargos.",
        "Igmund en Markarth, Korir en Hibernalia, Skald en Lucero del Alba, y otros más: si los destierran antes de que hagas sus misiones, esas misiones desaparecen.",
        "Y el que sube también pierde lo suyo: Dengeir y Brunwulf, al convertirse en jarls, dejan de darte sus encargos.",
        "Y con cada jarl se va su corte. En Morthal, Gorm e Idgrod la Joven también dejan de darte trabajo.",
        "Y hay dos que mueren en las batallas, sí o sí: Severo Pelagia en Carrera Blanca, y el capitán Aldis en Soledad.",
        "La regla es simple: antes de cada batalla, termina los encargos del jarl de esa ciudad. Después, ya no hay a quién entregárselos.",
        "[deadpan] Liberas Skyrim, y lo primero que pierdes es tu trabajo de recadero.",
    ]},
    {"id": "cr2", "frases": [
        "Por cierto, Adons me dejó un comentario muy profundo: «¿Sabes qué? Eres un llorón».",
        "Tiene toda la razón. Por eso hoy te traigo quince cosas para llorar. [sarcastic] Espera a ver el número tres, y luego hablamos de quién llora.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. La forja de stalhrim.",
        "El stalhrim es el hielo encantado de Solstheim. Para forjarlo tú mismo hace falta la ventaja Herrería de ébano, y una misión de la Aldea Skaal.",
        "Esa misión depende de dos personas: Deor Tallador y Fanari Voz Fuerte. Si cualquiera de los dos muere antes de terminarla, nunca aprenderás a forjar stalhrim.",
        "Y están protegidos: nadie puede matarlos, menos tú. Un rayo mal apuntado, un grito en medio de la aldea, y se acabó.",
        "Y ojo, que tus seguidores también cuentan. Un compañero con un hacha, y Deor no vuelve.",
        "Cómo no caer: haz la misión pronto, y nunca pelees con gritos de área dentro de la aldea.",
        "Las piezas se siguen vendiendo en Solstheim. Pero forjarlas tú, nunca.",
        "[deadpan] La única forja de hielo del mundo, y la pierdes por un Fus Ro Dah con mala puntería.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. La Corona dentada.",
        "Está en Korvanjund, en El Pálido, en un sarcófago al fondo de la ruina. Un casco pesado de veintitrés de armadura, que vale cinco mil monedas.",
        "Y de paso, Korvanjund tiene un muro de palabras. Ya que vas, llévatelo.",
        "Y tiene un truco muy bueno: va en el hueco del pelo, así que se lleva a la vez que una máscara de sacerdote dragón o una diadema.",
        "Pero en la guerra civil tienes que entregarla, ya sea a Tullius o a Ulfric, y ellos se la quedan para siempre.",
        "Si vas con el Imperio, ni siquiera hay recompensa. Un «buen trabajo, soldado», y a casa.",
        "Lo bueno: esa misión se puede posponer sin consecuencias. Así que úsala mientras tanto.",
        "Y existe un fallo para quedártela: meterla en el bolsillo de Hadvar o de Ralof antes de salir de la ruina. Pero eso ya es hacer trampa con estilo.",
        "[sarcastic] El casco más caro de su tipo, cambiado por una palmadita en la espalda.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. Serana, como vampira.",
        "Al final de Dawnguard puedes curarla: Falion, el mago de Morthal, se encarga, y tres días después Serana vuelve a ser humana, y hasta le cambia el color de los ojos.",
        "Pero curada, ya no puede convertir tus flechas élficas en flechas malditas de sangre, las del Arco de Auriel. Ni convertirte a ti en Señor vampiro.",
        "Y la cura solo es posible si tú no eres vampiro. Si lo eres, ni se plantea.",
        "Y hay algo peor: una pregunta a destiempo. Si cuando lleva su Pergamino Antiguo al Fuerte Guardia del Alba le preguntas si siempre ha sido vampira, y sacas lo de curarse...",
        "...ella lo llama un don, y nunca más quiere hablar del tema. La cura queda bloqueada para siempre.",
        "Cómo no caer: decide qué quieres de ella antes de hablar de la cura. Y si piensas curarla, guarda flechas malditas antes.",
        "[deadpan] Una charla de pasillo, y adiós al final más bonito de Dawnguard.",
    ]},
    {"id": "cr3", "frases": [
        "Y antonigirii me escribió: «ChatGPT, hazme un video con secretos de Skyrim que TODOS conocen, y de paso nárralo».",
        "[sarcastic] Encargo recibido. Pero si todos los conocen, explícame por qué hay tanta gente que quemó cinco colmenas.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. La armadura de maestre del gremio.",
        "Erikur es un thane de Soledad, bastante desagradable. Y es tentador quitárselo de en medio.",
        "Pero es el objetivo de un encargo especial del Gremio de Ladrones: El Sload delicado. Y solo es esencial hasta cierta misión de la Hermandad Oscura.",
        "Delvin Mallory te lo encarga, y premia con una mejora para el gremio. Pero si Erikur ya está muerto, el encargo no existe.",
        "Y si muere antes de ese encargo, el gremio se atasca y no llegas al final: adiós a la armadura de maestre, a la llave del cofre de tributos, y al Amuleto de Articulación.",
        "Y de propina, se va también un logro.",
        "Cómo no caer: haz El Sload delicado antes de meterte con la Hermandad Oscura. O, simplemente, no toques a Erikur.",
        "[deadpan] Matas a un noble pesado por gusto, y ya nunca serás el jefe de los ladrones.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Ser hombre lobo.",
        "La forma bestial: una vez al día, ciento cincuenta segundos. Más aguante que se regenera rápido. Y los aullidos de los Tótems de Hircine.",
        "Si te curas, con Dawnguard, Aela puede devolverte la licantropía. Pero una sola vez.",
        "Si te curas otra vez, con la cabeza de una bruja o haciéndote Señor vampiro, Aela ya no tiene nada que ofrecerte.",
        "Y ojo: hacerte Señor vampiro también cuenta como cura. Morder cuello, y adiós lobo.",
        "Y curado, no terminas los Tótems de Hircine, ni la misión de los cazadores de Dragonborn.",
        "Cómo no caer: termina los Tótems de Hircine antes de pensar siquiera en curarte. Y si te curas, que sea una sola vez.",
        "[sarcastic] Aela perdona una vez. La segunda, te ve como lo que eres: un indeciso.",
    ]},
    {"id": "campana", "frases": [
        "Un momento. De cada cien personas que ven este canal, solo trece están suscritas.",
        "Somos siete mil cien, y vamos camino de diez mil. Si estos videos te ahorran una partida arruinada, suscribirte es gratis. Y eso no lo pierdes nunca.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. La Guardia del Alba entera.",
        "En Dawnguard, Harkon te ofrece su don de sangre. Si dices que sí, eliges a los vampiros Volkihar, y la Guardia del Alba pasa a ser tu enemiga.",
        "Pierdes la Tecnología antigua: la ballesta mejorada, la ballesta enana y los virotes explosivos. Y los hechizos de luz solar, el hacha y el martillo rúnicos.",
        "Pierdes cuatro entrenadores maestros: Sorine, de Arquería. Isran, de Armadura pesada. Florentius, de Restauración. Y Gunmar, de Herrería, con su forja.",
        "Y pierdes seguidores, los perros Bran y Sceolang, y los trols con armadura. En la ruta vampira, hasta acabas matando a Isran.",
        "Y también pierdes para siempre a los cinco reclutas de la Guardia que te podían acompañar como seguidores, de Agmaer hasta Ingjard, todos de una vez y sin ningún aviso.",
        "A cambio, te dan el Cáliz de sangre, y unos perros de la muerte.",
        "Cómo no caer: aquí no hay doble ruta. Elige con esta lista en la mano.",
        "[deadpan] Cuatro maestros, dos perros y un trol con armadura. Por morderle el cuello al vecino.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. La tercera palabra de Invocar tormenta.",
        "Con las tres palabras es una tormenta de tres minutos, con rayos de ochenta de daño que caen cada pocos segundos. El grito con más daño bruto del juego.",
        "Con una sola palabra, la tormenta dura sesenta segundos, con rayos de cuarenta. Con dos, ciento veinte segundos, y rayos de sesenta.",
        "Y es el grito con el enfriamiento más largo de todos. Se lo ha ganado.",
        "La primera palabra está en Forelhost, la segunda en otras ruinas del norte. Esas no se van a ningún lado.",
        "Pero la última palabra está en el Templo de Skuldafn. Y ahí solo llegas una vez, a lomos de Odahviing, en la misión principal.",
        "Es el único grito con un muro de palabras en un lugar al que no puedes volver. Si no lo lees al pasar, nunca.",
        "Cómo no caer: en Skuldafn, antes del portal, barre el templo entero.",
        "Y ojo: sus rayos también les pegan a tus aliados.",
        "[sarcastic] El grito más poderoso de Skyrim, a dos palabras. Porque tenías prisa por morir en Sovngarde.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. El bastón de Nahkriin.",
        "En lo alto de Skuldafn derrotas al sacerdote dragón Nahkriin. Su bastón crea un muro de rayos de cincuenta de daño por segundo, y vale mil cuatrocientas treinta y una monedas.",
        "Pero es la llave: lo pones en el sello dragón, se abre el portal a Sovngarde... y el bastón se queda ahí.",
        "Y como a Skuldafn no se puede volver, casi todos lo pierden para siempre. La mayoría ni se entera de que era un arma.",
        "El truco: si llegas rápido, puedes cruzar el portal ya abierto sin usar el bastón, y entonces te lo quedas para siempre.",
        "Cómo no caer: en cuanto se abra el portal, no esperes a nadie. Corre.",
        "[deadpan] El único llavero de Skyrim que vale mil cuatrocientas monedas. Y lo dejas pegado en la puerta.",
    ]},
    {"id": "gema", "pre": 1.2, "frases": [
        "Y ahora, lo que prometí: el templo de Skuldafn, en lo alto de la montaña, el lugar de Skyrim que te roba tres cosas de golpe.",
        "El bastón de Nahkriin. La última palabra de Invocar tormenta. Y la máscara de Nahkriin, la que te conté en el video de las armaduras: sin ella, nunca habrá Konahrik.",
        "Así que, antes de subirte a Odahviing, haz la lista: lee el muro, saquea a Nahkriin, quédate su bastón, y corre al portal.",
        "Y ya que estás: entra a la embajada con los bolsillos vacíos, habla con Aela antes de la segunda cura, y piénsalo dos veces antes de decirle que sí a Harkon.",
        "[sarcastic] Skyrim es un juego donde puedes hacerlo todo. Una vez.",
    ]},
    {"id": "cierre", "frases": [
        "Este es el top. De unas colmenas quemadas de más, a un bastón que se queda pegado en una puerta.",
        "Ahora te toca a ti. ¿Cuál perdiste tú? ¿Y cuál no sabías? Déjalo en los comentarios: los leo todos.",
        "Y suscríbete, que vamos camino de diez mil.",
        "[deadpan] Y si prefieres un mundo donde lo que se perdió fue el planeta entero, Radio Yermo, nuestro canal hermano, es todo Fallout. Nos vemos en Tamriel.",
    ]},
]
