# -*- coding: utf-8 -*-
"""GUION — «Los 20 ERRORES del nivel 30 al 60 en WoW Forever (y cómo arreglarlos)» (Crónicas de Warcraft, 10-nov-2026).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO).
Investigación con fuentes: videos/_investigacion_wow_errores_30_60.md (nada de cifras fuera de ahí; la beta acababa en el 30:
lo de Classic sin comprobar en Forever se dice como «en Classic era así»).
Opción 1 de canales/formula/cronicas_warcraft.md (10-nov), una variable sobre «25 errores»: la etapa (30-60). 24-26 min.
Sale mié 11-nov-2026 (el usuario); Overgear hacia el min ~4 con el MISMO enlace del de add-ons: /CRONICAS/5.
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras. Textos del juego = «en el chat».
Comentarios (≤ 10 días, ninguno usado antes; CRÍTICAS mínimo 2-3 con sarcasmo, regla del usuario 11-nov): burla0 @marcosnicolascapocasa1571 · burla2 @AlbertoHans-k7f8d ×2 · gracias1 @tod6472 @rubenet5 · gracias2 @Zanafer23 @gregorypernia614
@matiasreynoso7970 · burla1 @warr.a.p742 («para jugar con prisa vete a retail»).
"""

TITULO = "Los 20 ERRORES del nivel 30 al 60 en WoW Forever (y cómo arreglarlos)"
ARCHIVO = "wow_errores_30_60"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ_APPLIO = dict(tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0)
VOZ = dict(motor="applio", **VOZ_APPLIO, idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")
# Grafía que lee Applio (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md); de la más larga a la más corta
FONETICA_APPLIO = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Overgear": "Óverguir", "self-play": "sélf pléi", "Classic": "Clásic", "Azeroth": "Azeróth",
    "CRONICAS10": "Crónicas diez", "Crónicas de Warcraft": "Crónicas de uárcraft", "Ventormenta": "Ventorménta",
    "Burning Crusade": "Bérnin Kruséid", "Hyjal Summit": "Jáyal Sámit", "Hyjal": "Jáyal", "Questie": "Cuésti", "Remy": "Rémi",
    "Nesingwary": "Nésinguari", "Hemingway": "Jémingüei", "Riverglades": "Ríverglèids", "Shen'dralas": "Shendrálas",
    "The Drowned City": "de Dráund Síti", "Krol'dok Stronghold": "Króldok Estrónjold", "Alcaz Island Prison": "Álcaz Áiland Prísson",
    "Blackmaw Hold": "Blákmo Jóld", "Shaper's Terrace": "Shéipers Térras", "Barrow Deeps": "Bárrou Díps",
    "Farholde Keep": "Fárjold Kíp", "Rog'mar": "Rógmar", "Steamwheedle Port": "Stímuidel Port", "Powderfuse Port": "Páuderfius Port",
    "Gadgetzan": "Gádyetzan", "Kargath": "Kárgaz", "Grom'gol": "Gromgól", "Zul'Farrak": "Zul Fárak", "Gahz'rilla": "Gazríla",
    "Jintha'Alor": "Yinza Alór", "Franclorn": "Fránclorn", "Linken": "Línken", "J.D. Collie": "Yei Di Cóli",
    "Atal'Hakkar": "Átal Jákar", "Hakkar": "Jákar", "Ogtinc": "Ógtink", "Xylem": "Sáilem", "Windsor": "Uíndsor",
    "Drakkisath": "Drákisaz", "Onyxia": "Oníxia", "Rexxar": "Réxar", "Krinkle": "Krínkel", "Araj": "Áraj", "Andorhal": "Ándorjal",
    "Scholomance": "Escolománs", "Caer Darrow": "Kéer Dárrou", "Zverenhoff": "Svérenjof", "Grazle": "Gréizel", "Nafien": "Náfien",
    "Un'Goro": "Ungóro", "Tanaris": "Tanáris", "Thrall": "Zrol", "Bolvar": "Bólvar", "Theramore": "Zéramor",
    "Gustaf VanHowzen": "Gústaf Van Jáuzen", "Jokerd": "Yókerd", "Azshara": "Asshára", "Mazthoril": "Mázzoril", "Haleh": "Jálej",
    "Betina Bigglezink": "Betína Bíguelsink", "Herod": "Jérod", "Desolace": "Desolás", "Arathi": "Aráti", "Zelda": "Sélda",
    "Wowhead": "Uaujéd", "Spoken": "Spóuken", "Doan": "Dóan", "Morgan": "Mórgan",
}
FONETICA = FONETICA_APPLIO
# Applio da siempre la misma toma: hipótesis de Whisper leídas el 10-nov (solo nombres propios/cifras)
CER_MAX_POR_FRASE = {'gracias1_1': 0.015, 'burla0_0': 0.021, 'burla0_3': 0.033, 'c04_6': 0.02, 'c20_1': 0.067, 'c20_8': 0.035, 'c19_1': 0.02, 'overgear_2': 0.018, 'c17_1': 0.029, 'c17_4': 0.032, 'c16_0': 0.036, 'c16_2': 0.025, 'c15_0': 0.045, 'c15_1': 0.035, 'c15_5': 0.025, 'c14_1': 0.024, 'c13_4': 0.039, 'c12_1': 0.017, 'burla1_1': 0.026, 'c09_6': 0.04, 'c08_1': 0.031, 'c08_2': 0.03, 'c08_4': 0.064, 'c07_1': 0.03, 'c07_3': 0.022, 'c07_4': 0.026, 'c06_1': 0.021, 'c06_4': 0.032, 'c05_2': 0.07, 'c05_6': 0.029, 'c04_4': 0.116, 'c03_2': 0.026, 'c02_3': 0.043, 'c02_4': 0.075, 'c02_5': 0.088, 'c02_7': 0.022, 'c01_1': 0.046, 'c01_3': 0.028, 'c01_6': 0.031, 'c01_8': 0.049, 'c01_13': 0.019}
TAIL_MAX_POR_FRASE = {'gracias1_1': 0.73, 'burla0_3': 0.46, 'c04_6': 0.47, 'c20_1': 0.47, 'c17_1': 0.37, 'c17_4': 0.58, 'c16_2': 0.36, 'c14_1': 0.55, 'c13_4': 0.88, 'c12_1': 0.63, 'burla1_1': 0.38, 'c09_6': 0.35, 'c08_1': 0.36, 'c08_4': 0.52, 'c06_1': 0.56, 'c06_4': 0.44, 'c05_2': 0.77, 'c05_6': 0.45, 'c02_3': 0.56, 'c02_5': 0.62, 'c02_7': 0.66, 'c01_1': 0.5, 'c01_3': 0.72, 'c01_6': 0.62, 'c01_8': 0.72, 'c01_13': 0.64}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # <= 175 s cada uno (timeline del 11-nov, 1535,6 s); `musica_wow.py` corta un tema de WoW por tramo (notas = _NOTA)
        (['intro', 'c20'], 'Legends of Azeroth'),          # 0-135
        (['c19'], 'Tuercespina'),                          # 135-182,5
        (['overgear'], 'Forjaz'),                          # 182,5-232,5 (suena la música de Overgear)
        (['burla0', 'c18'], 'Tanaris'),                    # 232,5-315
        (['c17', 'c16'], 'Tuercespina'),                   # 315-425
        (['c15', 'gracias1'], 'Feralas'),                  # 425-505
        (['c14', 'c13'], 'Orgrimmar'),                     # 505-620
        (['c12', 'c11', 'burla1'], 'Mil Agujas'),          # 620-765
        (['c10', 'c09'], 'Roca Negra'),                    # 765-890
        (['c08', 'c07'], "Un'Goro"),                       # 890-1005
        (['gracias2', 'c06'], 'Tierras de la Peste'),      # 1005-1087,5
        (['c05', 'burla2'], 'Feralas'),                    # 1087,5-1182,5
        (['c04', 'c03'], 'Cuna del Invierno'),             # 1182,5-1292,5
        (['c02'], 'Tanaris'),                              # 1292,5-1370
        (['c01'], 'Núcleo de Magma'),                      # 1370-1490
        (['cierre'], 'Legends of Azeroth'),                # 1490-1535,6
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'Llegaste al nivel treinta en World of Warcraft Forever y sientes que ya vas a la mitad. Pues no. Vas por el doce por ciento.',
        'Para llegar al treinta hacen falta cuatrocientos noventa y nueve mil puntos de experiencia. Para llegar al sesenta, más de cuatro millones.',
        'O sea: el ochenta y ocho por ciento de todo el juego está entre el treinta y el sesenta. Y ahí es donde la gente pierde semanas, y oro.',
        'Y hay otro detalle que casi nadie sabe: la beta de Forever se cortaba en el nivel treinta. Del treinta y uno al sesenta, nadie lo había jugado antes que tú.',
        'Así que muchas de las guías que estás siguiendo son, en el fondo, guías de un juego de dos mil diecinueve con un par de cosas nuevas encima.',
        'Ya hicimos el video de los veinticinco errores de los primeros niveles. Este es la segunda parte: lo que viene después del treinta.',
        'Hoy te traigo veinte errores que estás cometiendo del nivel treinta al sesenta, y cómo arreglar cada uno, del veinte al uno.',
        'Unos te cuestan oro, otros horas de experiencia, y el número uno te puede dejar en la puerta de la primera banda el día que abre.',
    ]},
    {"id": 'c20', "frases": [
        'Número veinte. Cargar veintisiete páginas cuando solo necesitas quince.',
        'En el norte de la Vega de Tuercespina está la Expedición de Nesingwary. Y ahí, Barnil Jarropetra te pide Las verdes colinas de Tuercespina.',
        'Las páginas del libro caen de casi todos los humanoides de la Vega, y van numeradas del uno al veintisiete.',
        'Mucha gente las guarda todas. Y de pronto tienes media bolsa llena de papel, en plena zona de nivel treinta y tantos.',
        'Pero los cuatro capítulos solo piden quince páginas concretas. Las otras doce no sirven para nada en la misión.',
        'Capítulo uno: la uno, la cuatro, la seis y la ocho. Capítulo dos: diez, once, catorce y dieciséis.',
        'Capítulo tres: dieciocho, veinte, veintiuno y veinticuatro. Y el capítulo cuatro, las tres últimas: veinticinco, veintiséis y veintisiete.',
        'El arreglo: guarda solo esas quince, vende las demás en la subasta de Bahía del Botín, y entrega cada capítulo en cuanto lo completes.',
        'Y un dato para presumir: Hemet Nesingwary es un homenaje a Ernest Hemingway, y el libro, a su obra Las verdes colinas de África.',
    ]},
    {"id": 'c19', "frases": [
        'Número diecinueve. Arrastrar misiones en el registro hasta que se ponen grises.',
        'En Forever, una misión se pone gris cuando está cinco niveles o más por debajo de ti.',
        'Y desde ahí, pierde entre un diez y un veinte por ciento de su experiencia por cada nivel de más. Esa misión que guardabas para luego, ya casi no da nada.',
        'Entre el treinta y el cuarenta y cinco pasa muchísimo: misiones de Desolace, de Arathi y de la Vega que entregas seis u ocho niveles tarde.',
        'Y en Classic el registro tenía veinte huecos. Si está lleno de misiones viejas, no te caben las nuevas, que son las que sí dan experiencia.',
        'El arreglo: cada cinco niveles, limpia el registro. Entrega lo hecho, y abandona sin pena las grises de recolectar y las élites que nunca vas a hacer.',
    ]},
    {"id": 'overgear', "post": 2.6, "frases": [
        'Y si del treinta al sesenta hay tantos errores, lo más rápido es que alguien que ya los conoce te los señale. Para eso existe el patrocinador de hoy.',
        'Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.',
        'Es self-play: juegas tú con tu personaje todo el tiempo, y un profesional verificado te guía por voz.',
        'Una guía te explica la clase en general. Un buen coach mira tu personaje, y te dice qué estás haciendo mal y cómo arreglarlo.',
        'Talentos, rotación, mazmorras nuevas, el plan para las bandas del nueve de diciembre o duelos: tú eliges, y pagas solo las horas que necesites.',
        'El enlace está en la descripción, y por el lanzamiento de Forever hay un código para ti.',
        'Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.',
    ]},
    {"id": 'burla0', "frases": [
        'Y ya que hablamos del patrocinador, una crítica que nos llegó con mucho cariño.',
        'Marcos escribió: quién puede ser tan idiota en pagar para que te digan cómo jugar.',
        'Marcos, gran pregunta. La misma gente que paga un entrenador en el gimnasio, clases de guitarra, o un instructor para no chocar el coche.',
        'Nadie te obliga, claro. También puedes aprender solo, como yo aprendí a nadar: tirándome al río de Tuercespina con un cocodrilo detrás.',
        'Y fíjate: tú dedicaste tu tiempo a escribirnos esa pregunta. Eso, Marcos, ya es asesoría gratis para el algoritmo. Gracias.',
    ]},
    {"id": 'c18', "frases": [
        'Número dieciocho. Resucitar con el Ángel de la Resurrección y pagar la reparación.',
        'Del treinta al sesenta, las reparaciones empiezan a doler: un juego de malla o de placas cuesta mucho más que en el nivel veinte.',
        'Si resucitas con el ángel, te llevas la Dolencia de resurrección durante diez minutos, y en Classic perdías un veinticinco por ciento extra de durabilidad.',
        'Y un arma rota no hace daño. Así que la muerte barata acaba saliendo carísima.',
        'Pasa sobre todo en zonas con el cementerio lejos, como Tanaris, Silithus o Desolace, donde nadie quiere correr de vuelta.',
        'El arreglo: corre a tu cadáver casi siempre, repara en cada pueblo, y si eres sacerdote, chamán, paladín o druida, resucita tú a tu grupo.',
    ]},
    {"id": 'c17', "frases": [
        'Número diecisiete. No activar los vuelos, y dejar la piedra de hogar en tu capital.',
        'Del treinta al sesenta se cruza el mundo entero: Tanaris, Un\'Goro, Feralas, Azshara, las Tierras de la Peste.',
        'Y en Forever no hay portales de ciudad, ni monturas voladoras. Las rutas largas de vuelo solo existen si activaste cada parada por el camino.',
        'La piedra de hogar tiene una hora de reutilización. Si sigue atada a tu capital, cada vuelta a la zona te cuesta veinte minutos de viaje.',
        'Los centros buenos de esta franja son Gadgetzan, Bahía del Botín, Kargath para la Horda, la Capilla de la Esperanza de la Luz y Vista Eterna.',
        'Y ojo, Horda: el Baluarte, en las Tierras de la Peste del Oeste, no tiene maestro de vuelo. Allí se llega a pie.',
        'El arreglo: activa cada maestro de vuelo que pises, y ata la piedra de hogar a la posada donde vas a pasar los próximos tres a cinco niveles.',
    ]},
    {"id": 'c16', "frases": [
        'Número dieciséis. Hacer la Vega de Tuercespina en un reino de JcJ a la hora pico.',
        'La Vega es la zona clásica del treinta al cuarenta y cinco, y también la más famosa por las emboscadas entre facciones.',
        'Horda y Alianza se cruzan en la Expedición de Nesingwary, en Bahía del Botín y en el camino a Grom\'gol, el zepelín de la Horda.',
        'Y en Forever el conjunto de JcJ es un megarreino por región. Ahí, como dijo una guía alemana, manda la ley del más fuerte.',
        'Si te matan cada cinco minutos, pierdes tiempo, durabilidad y las misiones de escolta que tenías a medias.',
        'El arreglo: si la Vega está imposible, haz otra zona del mismo nivel, como Desolace, Arathi, Alterac o el Marjal Revolcafango, y vuelve a otra hora.',
        'O entra en grupo. Cinco jugadores juntos dejan de ser presa, y pasan a ser el problema de otros.',
    ]},
    {"id": 'c15', "frases": [
        'Número quince. Pelear sin los curativos gratis de Frondavil.',
        'En Frondavil, con el Ungüento de planta Cenarion del Santuario Esmeralda, puedes limpiar plantas corruptas del bosque.',
        'Una Blancoria corrupta te da varios Tubérculos de blancoria. Curan más de mil doscientos puntos de vida, y piden nivel cuarenta y cinco.',
        'Y aquí está el truco: tienen su propio tiempo de espera, que no comparten con las pociones. O sea, una curación extra en cada pelea, gratis.',
        'De las mismas plantas sale el Aliento de Dragón nocturno, y de la Flor cantora corrupta, la Serenata Cantaflor, un beneficio que dura un buen rato.',
        'El arreglo: cuando llegues a Frondavil, consigue el ungüento, llena una pila de tubérculos, y úsalos además de tus pociones.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y antes de seguir, gracias por los comentarios del video de los veinticinco errores.',
        'Tod escribió que fue el mejor video que vio en sus dos días de juego. Dos días, y ya está aquí: bienvenido al canal, compañero.',
        'Y Rubén lo resume en una línea: buen video, el humor no decepciona. Rubén, eso es lo más difícil de mantener. Gracias.',
        'Todos los comentarios se leen, y todos se toman en cuenta para mejorar el canal. Por eso cada video sale un poquito mejor.',
    ]},
    {"id": 'c14', "frases": [
        'Número catorce. Llegar al cuarenta y no pasar por el entrenador, ni por el maestro de armas.',
        'En Classic, al nivel cuarenta, el guerrero y el paladín aprenden a llevar placas, y el cazador y el chamán, malla. Y cuesta muy poco.',
        'Pero mucha gente sigue diez niveles con la armadura de antes, porque nadie le avisó. Diez niveles recibiendo golpes de más.',
        'Y en Forever las habilidades de arma siguen existiendo. Si cambias a un hacha o un bastón nuevo, hay que aprenderla con el maestro de armas.',
        'Y empieza en uno. Así que con tu arma nueva y reluciente, fallas casi todos los golpes.',
        'Un diseñador de Classic dijo que la habilidad de arma era probablemente la estadística más fuerte. Por eso en Forever las Manoplas del Maestro de filos bajaron de siete a uno.',
        'El arreglo: entrenador en cada nivel par, armadura nueva al cuarenta, y antes de usar un arma nueva en serio, unos minutos contra enemigos fáciles.',
    ]},
    {"id": 'c13', "frases": [
        'Número trece. Dejar los primeros auxilios abandonados en ciento cincuenta.',
        'Primeros auxilios no ocupa hueco de profesión. Y en Forever, además, fabrica las pociones de sanación, que en Classic eran de alquimia.',
        'Al final del camino, entre doscientos setenta y cinco y trescientos, haces la Poción de curación sublime. Y eso vale oro.',
        'Para pasar de doscientos veinticinco necesitas la misión Atenciones médicas, con nivel treinta y cinco.',
        'La Horda la hace con el doctor Gregory Víctor, en Sentencia, en las Tierras Altas de Arathi. La Alianza, con el doctor Gustaf VanHowzen, en Theramore.',
        'Tienes que salvar a quince heridos, los más graves primero. Y entrégala en cuanto llegues a quince, porque si esperas, alguno se muere y la fallas.',
        'El arreglo: guarda la seda y la tela de paño mágico que te cae del treinta al cuarenta y cinco, haz Atenciones médicas al treinta y cinco, y súbelo a trescientos.',
    ]},
    {"id": 'c12', "frases": [
        'Número doce. Pagar reasignaciones de talentos, en vez de la doble especialización.',
        'En Classic, cada vez que reasignabas talentos el precio subía: uno, cinco, diez, hasta cincuenta de oro.',
        'Por eso la gente subía de nivel con una rama mala para mazmorras, o una mala para subir sola. No había término medio.',
        'En Forever, al nivel cuarenta, el entrenador de clase te vende la doble especialización por unas diez de oro.',
        'Cambiar entre las dos es gratis, fuera de combate. Una rama para subir sola, y otra para tanquear o curar en Zul\'Farrak.',
        'El error es seguir pagando treinta o cuarenta de oro en reasignaciones del cuarenta al sesenta, cuando con una sola compra ya lo tenías resuelto.',
        'El arreglo: al cuarenta, compra la doble especialización, deja cada rama lista, y olvídate de volver a pagar.',
    ]},
    {"id": 'c11', "frases": [
        'Vamos con el número once: vender al vendedor el cuero, el mineral y la tela, y llegar al cuarenta a pie.',
        'La montura del nivel cuarenta cuesta unas cien de oro, con la equitación incluida. Y en Forever no hay ficha de WoW para comprar oro con dinero.',
        'Y justo entre el treinta y el cuarenta caen los materiales que más se piden en la subasta estas primeras semanas.',
        'El cuero grueso de las bestias de la Vega y de Arathi, el mineral de mitril de Arathi y de las Tierras Inhóspitas, y la tela de paño mágico de los humanoides.',
        'Cada vez que pulsas vender todo en la posada, regalas oro de tu montura. A veces, monedas de plata por algo que en la subasta vale oro.',
        'El arreglo: si tienes desollar o minería, todo va a la subasta. Y aunque no las tengas, la tela y los objetos verdes, también.',
        'Y un detalle: con reputación honorable con tu facción, la equitación te sale un diez por ciento más barata.',
    ]},
    {"id": 'burla1', "frases": [
        'Y ahora, una crítica de las que nos gustan.',
        'Warr escribió: esto empieza a darme rabia, para jugar con prisa vete a retail, aquí se juega con calma, cada uno a su ritmo.',
        'Warr, tienes toda la razón: Forever se juega con calma. Por eso este video no es para ir rápido. Es para no ir en círculos.',
        'Que tomarse el tiempo y perderlo no es lo mismo. Cargar doce páginas que no sirven para nada no es calma, Warr. Es mudanza.',
        'Y si alguien aquí va con prisa, es el que corre hacia su cadáver para no pagar la reparación. Eso no es prisa. Es economía.',
    ]},
    {"id": 'c10', "frases": [
        'Número diez. Seguir la lista del mejor equipo de Classic, como si fuera dos mil diecinueve.',
        'Los veteranos suben buscando los azules de siempre: el Devastador de Herod en la Armería del Monasterio Escarlata, o el Sombrero de Melenablanca de la Catedral.',
        'Pero Forever rehízo los objetos. Los aciertos y los críticos ahora valen igual para cuerpo a cuerpo, distancia y hechizos.',
        'El equipo que sumaba habilidad de arma está muy recortado, y llega la pericia, como en Burning Crusade. Y el equipo de sanación trae poder con hechizos.',
        'Hay hasta objetos para un lugar concreto: unos guantes de piel de sable de invierno que te hacen un seis por ciento más rápido montado, pero solo en Cuna del Invierno.',
        'Y los jefes que antes soltaban objetos únicos, ahora sueltan azules. La lista que te sabes de memoria ya no es la buena.',
        'El arreglo: compara cada pieza por sus estadísticas de Forever, no por la lista de hace siete años, y mira el botín real en un diario de mazmorras de Forever.',
    ]},
    {"id": 'c09', "frases": [
        'Número nueve. Entrar a las mazmorras sin tener las llaves.',
        'Media franja del treinta al sesenta va con llavero. En Classic, la llave Escarlata salía del cofre del Arcanista Doan, en la Biblioteca del Monasterio Escarlata.',
        'Y esa llave abre la Armería y la Catedral. Si empiezas por la Armería sin ella, el grupo se queda mirando una puerta cerrada.',
        'En Profundidades de Roca Negra está la Llave Sombratiniebla. Te la da Franclorn Forjador, un fantasma que solo se ve estando muerto.',
        'Sí: para conseguir la llave de Roca Negra, primero hay que morirse. Luego vengas a Franclorn, y la llave te ahorra medio camino de la mazmorra.',
        'Y en Zul\'Farrak está la Marra sacra. Se transforma en la cima de Jintha\'Alor, en las Tierras del Interior, y con ella se invoca a Gahz\'rilla.',
        'En Classic, Gahz\'rilla soltaba la Zanahoria pinchada en un palo, un abalorio que te hace ir más rápido montado.',
        'El arreglo: recoge cada llave en la primera pasada, y si tu grupo tiene un pícaro, cuídalo: puede forzar varias de esas puertas.',
    ]},
    {"id": 'c08', "frases": [
        'Número ocho. Abandonar a la mitad las cadenas largas.',
        'Las mejores recompensas del cuarenta y cinco al cincuenta y cinco vienen de cadenas que te mandan a medio mundo. La más famosa es la de Linken.',
        'Empieza en una balsa naufragada en el Cráter de Un\'Goro, pasa por J.D. Collie en el Refugio de los Mariscales, y te lleva a Cuna del Invierno y a Tanaris.',
        'Toda la cadena es un homenaje a La leyenda de Zelda. Y la última misión se llama Ir solo es peligroso.',
        'Al final te dan la Espada de maestría de Linken, o el Bumerán de Linken. Para un personaje de cincuenta y tantos, eso es oro puro.',
        'Con el Templo Sumergido pasa igual: la Horda empieza su cadena al treinta y ocho, en el Pantano de las Penas, y la Alianza al cuarenta y uno, en Ventormenta.',
        'Mucha gente hace el primer paso, ve que el siguiente está en otro continente, y la abandona. Y con ella, la mejor recompensa de su rango.',
        'El arreglo: apunta cada cadena abierta y métela en tu recorrido. Un\'Goro, Cuna del Invierno y Tanaris ya están en tu camino del cincuenta al cincuenta y cinco.',
    ]},
    {"id": 'c07', "frases": [
        'Número siete. Llegar a Cuna del Invierno sin reputación con los Fauces de Madera.',
        'El túnel entre Frondavil y Cuna del Invierno es del Bastión de los Fauces de Madera, unos furbolgs que solo dejan pasar tranquilos a sus aliados.',
        'En el Classic original empezabas en hostil con ellos. Y cruzar ese túnel peleando no es la mejor forma de llegar a una zona nueva.',
        'La reputación sube matando a los furbolgs Muertobosque de Frondavil y a los Nevada de Cuna del Invierno, y entregando sus plumas y sus cuentas.',
        'Las Plumas de penacho Muertobosque y las Cuentas de Espíritu Nevada se llevan a Grazle y a Nafien, dentro del bastión.',
        'Si empiezas mientras subes, al llegar al sesenta ya tienes las recetas buenas de amistoso y honorable, como el encantamiento de agilidad para arma.',
        'El arreglo: no vendas ni una pluma ni una cuenta, y entrégalas cada vez que pases por el bastión.',
    ]},
    {"id": 'gracias2', "frases": [
        'Y otra ronda de comentarios, porque se la ganaron.',
        'Zanafer escribió que se enteró de cosas que no sabía. Y Gregory dice que el guion es una maravilla. Gracias a los dos: eso es justo lo que buscamos.',
        'Y Matías lo deja claro: Remy toda la vida, ya nos acostumbramos. Pues aquí sigo, Matías, del veinte al uno.',
        'Si este video te está ahorrando oro y horas, la forma de ayudar al canal es suscribirte. Es gratis, y así no te pierdes la tercera parte.',
    ]},
    {"id": 'c06', "frases": [
        'Número seis. Matar no-muertos en las Tierras de la Peste, sin llevar equipada la Comisión del Alba Argenta.',
        'Los no-muertos de las Tierras de la Peste, de Stratholme y de Scholomance sueltan Piedras de la Plaga, que se cambian por reputación con el Alba Argenta.',
        'Pero solo caen si llevas equipada la Comisión del Alba Argenta, un abalorio que te dan en el campamento de tu facción. Sin ella, no cae ni una.',
        'Así que hay gente que mata cientos de no-muertos, y no se lleva ni una piedra. Horas de reputación, tiradas a la basura.',
        'Las piedras se entregan en la Capilla de la Esperanza de la Luz, al duque Nicolás Zverenhoff, a cambio de Muestras de valor del Alba Argenta.',
        'El arreglo: en cuanto llegues al campamento de tu facción en las Tierras de la Peste del Oeste, consigue la comisión y llévala puesta contra la Plaga.',
    ]},
    {"id": 'c05', "frases": [
        'Número cinco. Saltarte las misiones de clase del nivel cincuenta.',
        'Al nivel cincuenta, cada clase tiene una misión que acaba en el Templo de Atal\'Hakkar, el Templo Sumergido, con recompensas solo para esa clase.',
        'Y nadie te avisa. El mago y el pícaro la recogen del Archimago Xylem, en Azshara. El cazador y el sacerdote, de Ogtinc, también en Azshara.',
        'El brujo, de un diablillo en Frondavil llamado Diblis. Y el guerrero, de un Héroe caído de la Horda en el Pantano de las Penas.',
        'El paladín la busca en las Tierras de la Peste del Oeste, el chamán en las Montañas de Alterac, y el druida en la entrada de Un\'Goro.',
        'Si no sabes que existe, pasas por el Templo sin ella, y te quedas sin la recompensa de tu clase para siempre en esa pasada.',
        'El arreglo: al cincuenta, busca a tu personaje de clase, y junta su misión con las del Templo, como la de Hakkar y la del profeta Jammal\'an, en una sola visita.',
    ]},
    {"id": 'burla2', "frases": [
        'Y antes del top cuatro, otra crítica, de las que se agradecen.',
        'Alberto escribió: no sé quién te dijo que era buena idea poner muchas voces en tus videos.',
        'Alberto, nos lo dijo la democracia. Pusimos siete voces, la gente votó, y ganó la de siempre por goleada.',
        'Así que tranquilo: el experimento terminó, y el único que sigue escuchando voces en este canal soy yo. Eso sí es preocupante.',
        'Y ese mismo día, Alberto también escribió que le gusta más Spoken que el nuestro. Alberto, si quieres voces planas, te leo este video otra vez, pero sin ganas.',
    ]},
    {"id": 'c04', "frases": [
        'Número cuatro. Chocar con el muro de los cincuenta sin un plan.',
        'En Classic, entre el cincuenta y el cincuenta y cinco, las misiones se acababan de golpe. Y cada nivel pide ciento cuarenta y siete mil puntos de experiencia o más.',
        'La salida de siempre era la Montaña Roca Negra, con sus mazmorras llenas de misiones, más Un\'Goro, Frondavil y Cuna del Invierno.',
        'Pero Forever añade huecos nuevos: Alcaz Island Prison, en la isla del Marjal Revolcafango, para el cuarenta y ocho al cincuenta y cinco.',
        'Y Blackmaw Hold, en el norte de Azshara, y Shaper\'s Terrace, en Un\'Goro, para el final del camino.',
        'Y una trampa: en las Tierras de la Peste del Oeste, si te saltas la misión que te lleva a la zona al nivel cincuenta, no se abre nada allí.',
        'El arreglo: guarda la experiencia de descanso para el cincuenta, junta las misiones de Roca Negra y de Alcaz antes de entrar, y ten pensado tu camino hasta el cincuenta y cinco.',
    ]},
    {"id": 'c03', "frases": [
        'Número tres. Llegar al cincuenta y ocho sin haber empezado la Llave esqueleto.',
        'En Forever, Scholomance pide la Llave esqueleto para abrir la puerta. Y la cadena para conseguirla es de las más paseadas del juego.',
        'Empieza en las Tierras de la Peste del Oeste: la Alianza, en el campamento de Ashlam Puñovalor, y la Horda, en el Baluarte.',
        'Te piden quince fragmentos esqueléticos. Los llevas con quince de oro a Krinkle Buenacero, en Gadgetzan, al otro lado del mundo.',
        'Luego forjas el molde en la lava del Cráter de Un\'Goro, con dos lingotes de torio. Y al final, en grupo, matas a Araj el Invocador, en Andorhal.',
        'Si la empiezas al cincuenta y ocho, te pasas los últimos niveles cruzando continentes mientras tus amigos ya están dentro.',
        'El arreglo: empiézala al cincuenta y cinco, y junta el paso por Gadgetzan y por Un\'Goro con tu ruta normal de esos niveles.',
    ]},
    {"id": 'c02', "frases": [
        'Número dos. Subir del treinta al sesenta con la ruta de Classic de memoria.',
        'Como la beta acababa en el treinta, mucha gente sigue la ruta de dos mil diecinueve paso a paso. Y se salta justo lo más nuevo de Forever.',
        'Riverglades es una zona nueva del treinta y cinco al cuarenta y cinco, entre Crestagrana, las Estepas Ardientes y el Pantano de las Penas.',
        'Según Blizzard, trae más de ciento cincuenta misiones nuevas. Tiene vuelos en Farholde Keep para la Alianza y en Rog\'mar para la Horda.',
        'Y desde Tanaris sale un barco: de Steamwheedle Port a Powderfuse Port. Un atajo que la ruta de Classic ni conoce.',
        'Está también Shen\'dralas, al sur de Desolace, para el cuarenta. Y mazmorras nuevas: The Drowned City, frente a la costa de la Vega, y Krol\'dok Stronghold, en Riverglades.',
        'En Forever, la experiencia gorda está en completar cada mazmorra una vez, con todas sus misiones, en cuanto llegas a su nivel. Y estas son nuevas para todos.',
        'Hasta Questie, que ya tiene versión para Forever, puede tener huecos con las misiones más nuevas. Así que no te fíes solo de las marcas del mapa.',
        'El arreglo: mete Riverglades en tu ruta del treinta y cinco al cuarenta y cinco, y haz una pasada por cada mazmorra nueva con sus misiones.',
    ]},
    {"id": 'c01', "frases": [
        'Número uno. Llegar al sesenta el nueve de diciembre sin la sintonización de Onyxia.',
        'El nueve de diciembre abren las bandas. Barrow Deeps, de diez jugadores, y Hyjal Summit, de veinte, no piden sintonización.',
        'Pero la Guarida de Onyxia, de cuarenta, exige el Amuleto de Pirodraco en tu bolsa. Y es personal: no se comparte con tus otros personajes.',
        'La Alianza tiene dieciséis misiones, desde el cuarenta y ocho. Empiezas con Helendis Rivacuerno, en las Estepas Ardientes, y pasas por Ventormenta y Bolvar.',
        'Y en medio está la más temida: rescatar al alguacil Windsor en Profundidades de Roca Negra, y escoltarlo hasta la salida. Si muere, se falla.',
        'La Horda tiene quince misiones, todas de nivel cincuenta y cinco. Y aquí viene la trampa de Forever.',
        'El que te da la primera, el Señor de la guerra Dientegore, en Kargath, no tiene el signo de misión sobre la cabeza. Hay que hablarle y leer su diálogo.',
        'Así que hay hordas enteras de jugadores pasando a su lado sin saber que ahí empieza Onyxia.',
        'Luego te toca la Cumbre de Roca Negra, Thrall, Rexxar en Desolace, Brasaliza en el Marjal Revolcafango y cuatro pruebas repartidas por el mundo.',
        'Y las dos facciones terminan igual: matando al general Drakkisath, en la Cumbre de Roca Negra superior.',
        'Y dos trampas más. El Núcleo de Magma no está en Forever de momento, así que no pierdas tiempo con su sintonización.',
        'Y en Forever, la misión del Lacre de Ascensión ya no da el lacre al final. Blizzard no ha confirmado si la puerta de la Cumbre superior lo pide, así que alguien del grupo debería empezarlo.',
        'Del cuatro de noviembre al nueve de diciembre hay cinco semanas. El que empieza tarde la sintonización, ese día se queda en la puerta mirando el portal.',
        'El arreglo: Alianza, empieza con Helendis al cuarenta y ocho, y rescata a Windsor mientras haces Roca Negra. Horda, al cincuenta y cinco, habla con Dientegore aunque no tenga signo.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esos son los veinte errores del nivel treinta al sesenta en World of Warcraft Forever, de las veintisiete páginas a la puerta de Onyxia.',
        'Y un último dato: el primer sesenta de Forever fue un grupo de tres magos, un paladín y un chamán, un poco más de tres días después del lanzamiento.',
        'No hace falta que tú lo hagas en tres días. Pero sí que no pierdas tres semanas en errores que ya conoces.',
        'Cuéntame en los comentarios en qué nivel vas, y cuál de estos errores ya cometiste. Todos se leen, y los mejores salen en el próximo video.',
        'Si este video te sirvió, suscríbete y compártelo con ese amigo que acaba de llegar al treinta. Le ahorras horas, y oro.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
