# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — «Los 40 SECRETOS de Skyrim que nadie te contó» (30-oct-2026). Meta: 18 min (el usuario), 1 sesión.
Tema elegido por el usuario entre 3 con datos: Choa «60 Useless Skyrim Facts» ×86 (33 min), Syrric «3h de curiosidades» ×4,6.
Misma lista larga que gana en el canal (`tes_misiones_nunca` ×10), cambia UNA variable: el tema. SECUENCIA YT, voz Chatterbox
«Sarcastica», MG `nucleo/mg_tes.py`, pegatinas, mapas con ruta, OST oficial de Skyrim (`armar_musica_ost.py`).
Datos verificados el 30-oct-2026 en UESP (wikitexto) por 3 subagentes: `_investigacion_A.md` (lugares), `_investigacion_B.md`
(personajes y lore), `_investigacion_C.md` (mecánicas). Cada ficha trae su URL y lo que no casó. Lo que es deducción nuestra se
dice como pregunta (mamut, Shelly). Paarthurnax: las atrocidades son acusación de las Cuchillas, no un hecho (UESP: «supposedly»).
Corrección en voz: `tes_armas_poderosas` dijo que TODOS los martillos de guerra tienen velocidad 0,6; el Martillo largo tiene 0,8.
Comentarios reales en pantalla (reglas 27/28-oct): gancho @ericmarticorena3842 · n.º 1 @Knox8386 (pidió Paarthurnax) · corrección
@stazmadness3910 (♥16, Clarividencia) · agradecimientos @Senpai.13 (30), @AnormalProject (20), @OFSUAREZL y @daybengamers8298 (10),
@franciscobarqueromunoz1218 (cierre).
"""

TITULO = "Los 40 SECRETOS de Skyrim que nadie te contó"
ARCHIVO = "tes_secretos_40"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
FONETICA = {
    "The Elder Scrolls": "Di Élder Escróls", "Skyrim": "Escairim", "jarl": "yarl", "Oblivion": "Oblívion",
    "@ericmarticorena3842": "Éric Marticorena", "@stazmadness3910": "Estaz Mádness", "@Senpai.13": "Sempái",
    "@AnormalProject": "Anormal Próyect", "@OFSUAREZL": "Ofe Suárez", "@daybengamers8298": "Déiben Guéimers",
    "@franciscobarqueromunoz1218": "Francisco Barquero Muñoz", "@Knox8386": "Nóks",
    "Riften": "Ríften", "Markarth": "Márkarz", "dwemer": "duémer", "falmer": "fálmer", "thalmor": "tálmor", "Thalmor": "Tálmor",
    "Solstheim": "Sólsteim", "Morrowind": "Mórouind", "Bloodmoon": "Bladmún", "Cyrodiil": "Cirodíl", "Tamriel": "Támriel",
    "Vvardenfell": "Bárdenfel", "Dawnguard": "Dóngard", "Hibernalia": "Ibernália", "Falkreath": "Fálkriz", "Morthal": "Mórzal",
    "Dunstad": "Dúnstad", "Volkihar": "Bolkíjar", "Saarthal": "Sáartal", "Hroldan": "Róldan", "Moesring": "Móesring",
    "riekling": "ríkling", "Moonwalk": "múnuok", "moonwalk": "múnuok", "Castlevania": "Castlevánia", "Simon Belmont": "Símon Bélmont",
    "Drácula": "Drácula", "khajiit": "cajít", "Azura": "Azúra", "Namira": "Namíra", "Aegis": "Éguis", "Arkay": "Arkéi",
    "Goldar": "Góldar", "Margret": "Márgret", "Tullius": "Túlius", "Cidhna": "Sídna", "Bolund": "Bólund", "Galathil": "Gálazil",
    "Volendrung": "Bolendrung", "Trius": "Tríus", "Shelly": "Chéli", "Sybille Stentor": "Síbil Esténtor", "Ahtar": "Áhtar",
    "Arvak": "Árvak", "Karan": "Cáran", "Talvur": "Tálbur", "dunmer": "dúnmer", "Mara": "Mára",
    "Neloth": "Néloth", "Telvanni": "Telváni", "Tel Naga": "Tel Nága", "Redoran": "Redorán", "Nerevarino": "Nerevaríno",
    "Falx Cario": "Falks Cário", "Ildari": "Ildári", "skooma": "escúma", "Venaro Vulpin": "Benáro Bulpín",
    "Phinis Gestor": "Fínis Guéstor", "Phinis": "Fínis", "Yisra": "Ísra", "Rundi": "Rúndi", "Borvir": "Bórbir",
    "Ilas-Tei": "Ílas Téi", "Honningbrew": "Jóningbru", "Talos": "Tálos", "skeevers": "eskívers",
    "Movarth Piquine": "Móvarz Pikín", "Movarth": "Móvarz", "Alain Dufont": "Alén Difón",
    "Paarthurnax": "Parzúrnax", "Charles Martinet": "Charls Martiné", "Super Mario": "Súper Mário",
    "Urag gro-Shub": "Úrag gro Shub", "Mirtil Angoth": "Mírtil Ángot", "Alduin": "Álduin", "Hrothgar": "Rótgar",
    "Arngeir": "Árnguéir", "Runil": "Rúnil", "Skorm": "Escórm", "redguard": "rédgard", "Ramati": "Ramáti", "Mani": "Máni",
    "Habd": "Jabd", "chaurus": "cháurus", "Jurgen": "Yúrguen", "Esbern": "Ésbern", "Alinor": "Alinór", "Delphine": "Délfin",
    "Ulfric": "Úlfrik", "Elenwen": "Élenuen", "Erik West": "Érik Uést", "Erik": "Érik", "Ewing": "Iúing",
    "Make-A-Wish": "Méik a Uísh", "Brand-Shei": "Brand Shéi", "Brandyl": "Brándil", "Lymdrenn Tenvanni": "Límdren Tenváni",
    "Tel Vos": "Tel Bos", "Bravil": "Brávil", "Alisanne Dupre": "Alisán Dupré", "Garnag": "Gárnag", "Cheydinhal": "Chéidinal",
    "Rasha": "Rásha", "Paar": "Par", "Thur": "Zur", "Nax": "Naks",
    "@jhonfeddiszabalamoreno9056": "Jon Féddis", "@lukelsue4430": "Lúkel Su", "kyrim": "Kírim",
}

# Transcripciones (se rellenan tras leer cada una en `seleccionar`)
# 30-oct: transcripciones leídas una a una; casi todas son nombres que Whisper escribe distinto (Falkreath→Falkris, Arkay→Arcade…).
# p30_2: fuera s2/s3 («gaza», «glaza»). p12_1 y p17_4: «absorbes su» y «llevas sus» se unen en las 4 tomas; se aceptan.
CER_MAX_POR_FRASE = {'cr1_0': .027, 'cr1_1': .016, 'cr2_0': .054, 'p30_2': .021, 'p17_4': .06, 'p12_1': .042, 'p39_2': 0.002, 'p37_0': 0.038, 'p37_2': 0.073, 'p35_1': 0.002, 'p34_1': 0.037, 'p32_1': 0.015, 'p30_0': 0.021, 'p29_1': 0.045, 'p29_2': 0.051, 'p29_3': 0.025, 'p28_1': 0.01, 'p26_1': 0.034, 'p23_1': 0.015, 'p20_1': 0.049, 'p20_2': 0.01, 'p19_1': 0.019, 'p18_1': 0.002, 'p17_1': 0.021, 'p17_3': 0.047, 'p16_1': 0.039, 'p16_2': 0.029, 'p13_1': 0.021, 'p11_0': 0.045, 'p10_0': 0.062, 'p9_1': 0.015, 'p9_2': 0.031, 'p8_3': 0.017, 'p5_0': 0.022, 'p5_2': 0.042, 'p4_1': 0.039, 'p4_2': 0.01, 'p3_2': 0.023, 'p1_0': 0.036, 'p1_1': 0.021, 'cierre_1': 0.002}
GAP_MAX_POR_FRASE = {'p39_2': 0.77, 'p35_1': 0.55, 'p34_1': 0.56, 'p29_3': 0.54, 'p20_1': 0.54, 'p20_2': 0.73, 'p18_1': 0.78, 'p13_1': 0.65, 'p10_0': 0.69, 'p5_2': 0.68, 'p1_0': 0.63, 'cierre_1': 0.54}
TAIL_MAX_POR_FRASE = {'p35_1': 0.54, 'p29_3': 0.58, 'p28_1': 0.51, 'p10_0': 0.57, 'p4_2': 0.61, 'p1_0': 0.37, 'p1_1': 0.72, 'cierre_1': 0.57}   # CER ~0: acaban hablando

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen; el sonido del juego va en ambiente_por (regla 26-oct-2026)
    ambiente_por={"scene-016": .7, "scene-022": .7, "scene-023": .7, "scene-059": .6, "scene-062": .6, "scene-096": .6, "scene-115": .6, "scene-118": .7},   # rugidos, gigante, lucha (regla 26-oct)
    recorte_por={},
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),   # heredados de tes_*
)

TRANSICIONES = [("continua", 0.1)] * 50
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (armar_musica_ost.py), nunca Lyria

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "@ericmarticorena3842 nos dejó este comentario. Que en tantos años de jugar, no sabía que se podía mejorar un amuleto de Talos.",
        "Y ese es justo el problema de Skyrim. Llevas años jugándolo, y te sigue escondiendo cosas.",
        "Una cárcel donde peleabas por tu libertad. Un vendedor de Riften con pasado de novela. Y una sopa de cinco monedas que te da doce minutos de ataques poderosos.",
        "Hoy te traigo cuarenta secretos, todos comprobados, y con sus fuentes en la descripción.",
        "Y quédate hasta el final, porque el número uno es sobre alguien en quien confías. Y a lo mejor no deberías.",
    ]},
    {"id": "p40", "frases": [
        "Número cuarenta. La poción del arquero.",
        "La poción de Reforzar arquería dice que mejora los arcos. Pero por un error, sube el daño de todas las armas, y hasta el de los puños.",
        "Y en una letrina del Fuerte Dunstad hay una de estas pociones, al lado del retrete. Es un chiste de los desarrolladores sobre apuntar bien.",
    ]},
    {"id": "p39", "frases": [
        "En el treinta y nueve, las vacas del más allá.",
        "En el Recordatorio de las Almas hay un alma haciendo de granjero. Labra una parcela con catorce cascarones plantados.",
        "Y a su lado pastan dos almas de vaca. Nadie explica qué hacen ahí.",
    ]},
    {"id": "p38", "frases": [
        "Número treinta y ocho. Tu raza decide lo rápido que corres.",
        "La velocidad depende de la altura. Los altos elfos son los más rápidos, y las bretonas y las khajiit, las más lentas.",
        "Probablemente sea por las animaciones. Sin este ajuste, algunos parecerían hacer el moonwalk.",
    ]},
    {"id": "p37", "frases": [
        "En el treinta y siete, Castlevania.",
        "En el Castillo de Volkihar hay una vitrina con una garra, un ojo, un corazón, una caja torácica y un anillo.",
        "Son las partes de Drácula que Simon Belmont reúne en Castlevania dos. En la casa de los vampiros. Muy fino.",
    ]},
    {"id": "p36", "frases": [
        "Número treinta y seis. Los guardias te leen la mochila.",
        "Con la Estrella de Azura basta con cargarla, y el guardia te lo comenta. Con el Anillo de Namira se quejan de tu aliento.",
        "Y si eres hombre lobo, te notan pelo en las orejas y olor a perro mojado.",
    ]},
    {"id": "p35", "frases": [
        "En el treinta y cinco, el mamut congelado.",
        "Al oeste de Saarthal, sin marcador en el mapa, hay un mamut atrapado en un bloque de hielo. Lleva clavadas cinco flechas enanas y un virote de balista dwemer.",
        "Alguien lo estaba cazando. ¿Quién? El juego no lo dice.",
    ]},
    {"id": "p34", "frases": [
        "Número treinta y cuatro. Rezar a Arkay te puede matar.",
        "Cuando se acaba un efecto de Reforzar salud, el juego te deja con un punto de vida. La Bendición de Arkay no.",
        "Son veinticinco de salud durante ocho horas. Y si te quedan menos de veinticinco cuando termina, mueres. El dios de la muerte, cobrando al contado.",
    ]},
    {"id": "p33", "frases": [
        "En el treinta y tres, el gigante que pudo ser tu aliado.",
        "Se cortó una misión con un gigante, Goldar. Tu trabajo era llevarle una vaca pintada como ofrenda.",
        "Al terminar, todos los gigantes del mundo serían tus aliados. Y Goldar llama a las vacas fabricantes de leche débil.",
    ]},
    {"id": "p32", "frases": [
        "Número treinta y dos. La turista de Markarth.",
        "Tu primera escena en Markarth es un atentado contra Margret, una mujer que compra un colgante.",
        "Si la salvas y la convences en la posada, confiesa que es agente del general Tullius. Si tardas, muere delante de ti, y solo te queda su diario.",
    ]},
    {"id": "p31", "frases": [
        "En el treinta y uno, la sopa de verduras.",
        "Con un solo punto de aguante ya puedes lanzar un ataque poderoso. Y el daño no depende del aguante que te quede.",
        "La sopa de verduras te devuelve un punto por segundo durante doce minutos. O sea, nunca llegas a cero, y encadenas ataques sin parar. Por cinco monedas.",
    ]},
    {"id": "p30", "frases": [
        "Antes de seguir. @Senpai.13 nos dijo que el video le pareció muy genial, y que no hiciéramos caso a los comentarios pedorros. Gracias.",
        "Número treinta. Hacerte vampiro te cambia de raza.",
        "Para el juego, un vampiro es otra raza distinta. Si eres nórdico y te conviertes, Bolund, en Falkreath, te habla como a un extranjero.",
        "Y Galathil, la que te cambia la cara, se niega. Dice que solo trabaja con los vivos.",
    ]},
    {"id": "p29", "frases": [
        "En el veintinueve, un error nuestro.",
        "En el video de las armas dijimos que todos los martillos de guerra tienen velocidad cero coma seis. Y no es verdad.",
        "En el Retiro del Mentiroso, un cadáver sujeta el Martillo largo. Velocidad cero coma ocho. A herrería máxima, hace más daño por segundo que Volendrung.",
        "Y ya que corregimos. @stazmadness3910 nos dijo que Clarividencia le sirve en las mazmorras dwemer, porque la brújula no dice por dónde caminar. Razón no le falta.",
    ]},
    {"id": "p28", "frases": [
        "Número veintiocho. El hombre que sigue esperando un barco.",
        "En la costa de Hibernalia hay un campamento vacío, y una nota. Trius le escribe a Shelly que su barco debió llegar hace semanas, y que acampó ahí para verla pasar.",
        "Él no aparece nunca. Y justo al norte, bajo el agua, están los pecios de la Zanja del Peregrino.",
    ]},
    {"id": "p27", "frases": [
        "En el veintisiete, tu seguidor es mejor ladrón que tú.",
        "Si le mandas abrir una cerradura y acepta, lo consigue siempre, por difícil que sea, y sin gastar ganzúas.",
        "Y lleva escondidos un arco de caza y doce flechas de hierro que no salen en su inventario.",
    ]},
    {"id": "p26", "frases": [
        "Número veintiséis. La maga de la corte de Soledad.",
        "Sybille Stentor dice haber visto ir y venir a varios jarls, y sigue joven. Detectar vida no la marca. Detectar muerte, sí.",
        "El verdugo cuenta que a veces baja a la cárcel a por voluntarios. Y ella misma te encarga limpiar un nido de vampiros.",
    ]},
    {"id": "cr1", "frases": [
        "Una pausa, que nos han descubierto. @jhonfeddiszabalamoreno9056 nos escribió que se nota que kyrim no es lo nuestro.",
        "Y tiene toda la razón. De kyrim no sabemos nada. Nosotros solo hablamos de Skyrim.",
    ]},
    {"id": "p25", "frases": [
        "En el veinticinco, la nave de los rieklings.",
        "En Solstheim, los rieklings acampan alrededor de una nave volcada, con el interior boca abajo y cubierto de pinturas.",
        "En Bloodmoon, la expansión de Morrowind, ya había un dirigible estrellado en esa isla. Todo indica que es el mismo.",
    ]},
    {"id": "p24", "frases": [
        "Número veinticuatro. La semana libre que creó las expansiones.",
        "En dos mil once, Bethesda dio a sus desarrolladores una semana para crear lo que quisieran.",
        "De ahí salieron los rieklings, Arvak, el Señor de los vampiros, la adopción, y construir tu casa. Y se quedó fuera un mayordomo esqueleto. Que yo habría contratado.",
    ]},
    {"id": "p23", "frases": [
        "En el veintitrés, la capilla que aparece sola.",
        "Cerca del Viejo Hroldan está el campamento donde murieron Karan y Talvur mientras se fugaban.",
        "Algún tiempo después de descubrirlo, el campamento desaparece, y en su sitio hay una capilla de Mara, con el diario de Karan al lado.",
        "El mundo cambia solo, y casi nadie vuelve para verlo.",
    ]},
    {"id": "p22", "frases": [
        "Número veintidós. El Pergamino Antiguo esconde nuestras estrellas.",
        "Su fondo no es inventado. Es un mapa estelar real del polo sur de la Tierra, con Escorpio y la Cruz del Sur.",
        "Y leerlo te borra todos tus efectos activos. Si tenías el sol apagado con el Arco de Auriel, el sol vuelve.",
    ]},
    {"id": "p21", "frases": [
        "En el veintiuno, desde Skyrim se ve Morrowind.",
        "Desde la azotea del Archimago, en el Colegio de Hibernalia, más allá de la frontera este, se ve Morrowind.",
        "Y al sur, en un día despejado y a mucha altura, se alcanza a ver la Torre Blanca y Dorada de Cyrodiil.",
    ]},
    {"id": "p20", "frases": [
        "Otra pausa. @AnormalProject nos dijo que a veces la música no encaja con lo que se narra, pero que fuera de eso, excelente. Apuntado, y gracias.",
        "Número veinte. Neloth ya era un cretino en Morrowind.",
        "Es el mismo personaje, maestro de la Casa Telvanni. Allí le gustaba secuestrar a las hijas de los consejeros Redoran, y una misión te mandaba matarlo.",
        "Sobrevivió. Y hoy te dice con desdén que eres muy joven para acordarte del Nerevarino.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, el capitán que no se quedó muerto.",
        "En el Fuerte Polilla Helada está Falx Cario, un personaje de Bloodmoon que murió hace unos doscientos años, por los escombros de la Montaña Roja.",
        "Ildari lo reanimó con un corazón de piedra. Y tras muchas semanas, se levantó, conservó su voluntad, e intentó matarla.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. El local de skooma que es una granja de sangre.",
        "La Guarida de Aguas Rojas, cerca de Riften, parece una casucha. Bajo una trampilla, hay un local donde te venden skooma.",
        "Si bebes la muestra gratis, despiertas encerrado en una sala llena de vampiros. Todo el negocio es una tapadera.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, los cuatro aprendices que nadie buscó.",
        "Phinis Gestor menciona a cuatro aprendices desaparecidos. Y sus cadáveres existen, repartidos por la comarca de Hibernalia.",
        "Yisra está calcinada en la playa, y las llamas todavía queman a quien las pisa. Rundi yace entre runas de escarcha. Borvir, con tres flechas en la espalda.",
        "E Ilas-Tei aparece rodeado de skeevers muertos, con un pergamino de Furia al lado.",
        "La misión se cortó. Si le llevas sus objetos a Phinis, no pasa nada.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. El héroe del libro es el jefe que mataste.",
        "Sangre inmortal es un libro que ya estaba en Oblivion. Movarth Piquine caza vampiros por toda Tamriel, con los consejos de un sacerdote.",
        "Al final, el sacerdote acerca la vela a su cara. El sacerdote era el vampiro. Y el señor vampiro de la cueva de Morthal es ese mismo Movarth.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, la arena de Ventalia.",
        "Ventalia iba a tener una arena con su propia cárcel. Si te encerraban, peleabas ante el público, y si ganabas, salías libre.",
        "Se cortó, pero el recinto sigue en los archivos. Un edificio sin entrada, rodeado de espectadores mudos que debían vitorear. Nunca les programaron cómo.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. El gran maestro tiene ficha de novato.",
        "En los datos del juego, Paarthurnax es nivel diez, con novecientos cinco de salud. Lo mismo que el dragón más básico.",
        "Y en inglés lo interpreta Charles Martinet, la voz de Super Mario. Acuérdate de este dragón, porque va a volver.",
    ]},
    {"id": "p13", "frases": [
        "En el trece, los libros que nadie lee.",
        "En el Valle Olvidado hay cuatro libros en alfabeto falmer. Urag gro-Shub te paga mil monedas por cada uno, y te da una copia traducida.",
        "Cuentan los últimos días de los elfos de las nieves. Y el Diario de Mirtil Angoth acaba con él ilusionado, cuando su pueblo decide pedir ayuda a los dwemer. Ya sabes cómo acabó eso.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Nunca absorbiste el alma de Alduin.",
        "Al matarlo no absorbes su alma. Si vuelves a Alto Hrothgar, Arngeir te explica que Alduin es único, y que quizá se le permita volver al final de los tiempos.",
        "O sea, quizá no lo mataste. Quizá solo lo aplazaste. Felicidades por salvar el mundo, de momento.",
    ]},
    {"id": "p11", "frases": [
        "En el once, el cura de Falkreath.",
        "Runil, el anciano sacerdote, admite que muchos murieron por sus manos y su magia en la Gran Guerra.",
        "En su diario anota un sueño. Una sombra enorme, un rugido, y un desconocido que se le acerca durante un funeral. Y todo apunta a que ese desconocido eres tú.",
    ]},
    {"id": "p10", "frases": [
        "Y aquí, dos más. @OFSUAREZL nos dijo, tremendo video, sigue así. Y a @daybengamers8298 le encantan estos videos. Gracias, de verdad.",
        "Número diez. El pozo de la Hueste de Forel.",
        "Las tropas de Skorm Caminante de la Nieve tiraron la puerta, y encontraron a todo el culto muerto. Pero habían dejado cubos ya llenos, junto a un pozo envenenado.",
        "Al día siguiente, cuarenta soldados bebieron antes de que pudieran pararlos. Y ese pozo es justo el que tú tienes que bajar.",
    ]},
    {"id": "p9", "frases": [
        "En el nueve, el faro que se tragó a una familia.",
        "Una familia redguard compró el Faro del Flujo Helado. Y los falmer abrieron un agujero en el sótano.",
        "Nadie te lo cuenta. Encuentras a Ramati muerta, la cena en el suelo, y bajo una cama, una mochila con una carta de Mani a su hermana.",
        "Y los restos del padre están dentro del segador de chaurus más grande del lugar. Si los subes al brasero del faro, lo dejas descansar.",
    ]},
    {"id": "cr2", "frases": [
        "Y esta va con cariño. @lukelsue4430 nos dijo que no somos dignos de Skyrim, y que no entendimos nada.",
        "Lo aceptamos. Seguimos esperando a que nos llamen los Barbas Grises. Mientras tanto, te contamos ocho secretos más.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Los Barbas Grises nacieron de una humillación.",
        "La orden existe porque los nórdicos perdieron en la Montaña Roja. Jurgen Llamador del Viento meditó siete años, y concluyó que la Voz se había usado con arrogancia.",
        "Cuando lo dijo, diecisiete lo atacaron a la vez. Y se dice que él se tragó sus gritos durante tres días, hasta que cayeron agotados.",
        "Está grabado en las tablillas de Alto Hrothgar. Las que tienes delante, y nunca lees.",
    ]},
    {"id": "p7", "frases": [
        "En el siete, lo que dicen los archivos thalmor.",
        "En su informe sobre Esbern reconocen que no entienden la vuelta de los dragones. Y que el viejito paranoico de la Ratonera nunca fue un simple archivero.",
        "Al funcionario que lo descartó por viejo, lo mandaron a Alinor a ser reeducado.",
        "Y el informe de Delphine dice que esquivó tres atentados, y que en uno mató a todo el equipo de asesinos.",
    ]},
    {"id": "camp", "frases": [
        "Antes de los últimos seis, un dato. De cada cien que ven este canal, catorce están suscritos.",
        "Los otros ochenta y seis entran, se llevan todo y se van, como en cualquier casa de Skyrim. Queremos llegar a siete mil.",
        "Si llevas treinta y cuatro secretos aguantando, suscribirte es lo menos que puedes hacer.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. Ulfric cree que entregó la Ciudad Imperial.",
        "Los thalmor lo capturaron en la Gran Guerra, y le hicieron creer que lo que confesó fue clave para tomar la ciudad. La ciudad ya había caído.",
        "Luego lo dejaron escapar. Su informe dice que quieren la guerra civil estancada. Y el que presume de libertad, en sus papeles, figura como un recurso.",
    ]},
    {"id": "p5", "frases": [
        "En el cinco, y aquí voy a hablar en serio. Erik el Asesino existió.",
        "El granjero de Paraje de Rorik que sueña con ser aventurero está inspirado en Erik West, un fan de The Elder Scrolls.",
        "Le diagnosticaron un sarcoma de Ewing en dos mil nueve. Make-A-Wish lo llevó a Bethesda, y crearon un personaje con su nombre.",
        "Murió el once de mayo de dos mil once, seis meses antes de que saliera Skyrim.",
        "Cada vez que convences a su padre de dejarlo marchar, le das a ese chico la aventura que quería.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. El vendedor de Riften.",
        "Brand-Shei es un elfo oscuro con nombre argoniano, porque lo adoptó una familia de la Ciénaga Negra.",
        "En el naufragio del Orgullo de Tel Vos hay un diario de su padre, Lymdrenn Tenvanni, escrito en un sótano durante la invasión argoniana. Lo llama su único heredero.",
        "O sea, lo criaron los del pueblo que arrasó su casa. Y en el Gremio de Ladrones, tú le metes un anillo en el bolsillo para mandarlo a la cárcel.",
    ]},
    {"id": "p3", "frases": [
        "En el tres, el ataúd del carro.",
        "En Oblivion, la Madre Noche estaba en una cripta bajo una estatua de Bravil. Según el diario de Cicerón, la estatua quedó destruida.",
        "Asaltaron la cripta, la Oyente Alisanne Dupre murió quemada viva, y Garnag huyó malherido con el ataúd hasta Cheydinhal.",
        "Es el mismo ataúd del carro con la rueda rota. Trece años huyendo de la caída de la Hermandad.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Cicerón no nació loco.",
        "Sus diarios empiezan con un asesino cuerdo y metódico. Lo nombran Guardián de la Madre Noche, y le conceden un último trabajo. Matar a un bufón.",
        "Escribe cómo se rio y se rio, hasta que dejó de reír.",
        "Lava el cadáver de la Madre Noche cada semana. Ella nunca le habla. Y meses después, empieza a oír la risa de aquel bufón.",
        "Acaba escribiendo que el alma del bufón entró en él, y que Cicerón el hombre ha muerto. El bufón que te hace tanta gracia es su última víctima.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. @Knox8386 nos escribió que tras muchísimos años de jugar, se fijó en el lore. Y que Paarthurnax, como dragón, también es un villano.",
        "Lo comprobamos. Su nombre se separa en tres palabras del idioma de los dragones. Paar, Thur, Nax. Ambición, Señor supremo, Crueldad.",
        "Según las Cuchillas, fue la mano derecha de Alduin, con atrocidades que se recuerdan miles de años después. Y lo cazaron durante siglos.",
        "Y lo más fuerte lo dice él. Que hacen bien en no fiarse. Que los dragones se crearon para dominar. Y que no pasa un día sin sentir la tentación de volver a su naturaleza.",
        "Por eso es el número uno. Los demás secretos están escondidos en libros y en cuevas. Este te lo dijo a la cara, en la cima del mundo. Y tú le diste las gracias.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Cuarenta secretos, de una poción mal programada, al dragón en el que confiaste.",
        "Y antes de irnos. @franciscobarqueromunoz1218 nos dio las gracias por el video. Gracias a ti. Leemos todos los comentarios, los que nos felicitan y los que nos corrigen, y los tenemos en cuenta para mejorar.",
        "Y ahora te toca a ti. ¿Cuántos de estos cuarenta sabías? Si tienes uno mejor, déjalo en los comentarios.",
        "Y si este video te sirvió, suscríbete. Vamos por los siete mil, y prometemos no entrar a tu casa sin permiso.",
    ]},
]
