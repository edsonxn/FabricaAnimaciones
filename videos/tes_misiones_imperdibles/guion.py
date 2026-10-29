# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — «Las 25 misiones de Skyrim que NUNCA debes saltarte» (28-oct-2026). Meta: 22 min (el usuario), 1 sesión.
Fórmula de `tes_misiones_nunca` (22 117 vistas en < 7 días, ×10 la mediana del canal) cambiando UNA variable: la polaridad
(las que SÍ hay que hacer). Nace de dos comentarios de ese video: @sebastiannarvaez6185 (♥11, defiende la Corona de Aetherium)
y @EnriqueJVidal-ei1nk (Arniel y la Forja entre sus favoritas). SECUENCIA YT, voz Chatterbox «Sarcastica», MG `nucleo/mg_tes.py`,
pegatinas, mapas con ruta, OST oficial de Skyrim (`armar_musica_ost.py`, 18 pistas que la Fábrica no había usado en el canal).
Datos verificados el 28-oct-2026 en UESP (en.uesp.net, wikitexto) por 3 subagentes: Skyrim:The Mind of Madness, Touching the Sky,
Forbidden Legend, Discerning the Transmundane, The Man Who Cried Wolf, The Wolf Queen Awakened, Dragonborn:The Ebony Warrior,
The Break of Dawn, Dragonborn:Unearthed, Deathbrand, Black Book: The Sallow Regent, Durnehviir, Soul Cairn Horse Quest (Arvak),
Glory of the Dead, A New Source of Stalhrim, The White Phial, Repairing the Phial, Tending the Flames, Missing In Action,
In My Time Of Need, Kyne's Sacred Trials, Rebel's Cairn, The Lost Expedition, Old Friends, Served Cold, Unfathomable Depths,
A Return To Your Roots. Nombres es-ES de elderscrolls.fandom.com/es (lo no encontrado se describe sin nombre oficial: «el cráneo
de Arvak»). Lo dudoso se dice con cautela o no se dice.
Comentarios reales en pantalla (reglas 27/28-oct): gancho @sebastiannarvaez6185 + @EnriqueJVidal-ei1nk · «Oblivion»
@alcoholikmisanthroper1934 (n.º 23) · agradecimientos @amadeoamaya7606 (21), @marcocho_23 (14), @franzindriago7950 (7),
@edupiles8494 y @KRONOX-LEGEND (cierre).
"""

TITULO = "Las 25 misiones de Skyrim que NUNCA debes saltarte"
ARCHIVO = "tes_misiones_imperdibles"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# "Skyrim": "Escairim" (el usuario, 23-oct) · "jarl": "yarl" (@federicoherrera2105) · "Oblivion": "Oblívion" (@alcoholikmisanthroper1934, ♥7).
FONETICA = {
    "The Elder Scrolls": "Di Élder Escróls", "Skyrim": "Escairim", "jarl": "yarl", "Oblivion": "Oblívion",
    "@sebastiannarvaez6185": "Sebastián Narváez", "@EnriqueJVidal-ei1nk": "Enrique Vidal",
    "@alcoholikmisanthroper1934": "Alcohólik Misántroper", "@amadeoamaya7606": "Amadeo Amaya", "@marcocho_23": "Marcocho",
    "@franzindriago7950": "Franz Indriago", "@edupiles8494": "Edu Piles", "@KRONOX-LEGEND": "Krónox Léyend",
    "Aetherium": "Etérium", "Arniel": "Árniel", "Avanchnzel": "Avánshensel", "Jerall": "Yérall", "dwemer": "duémer",
    "Riften": "Ríften", "Calcelmo": "Calsélmo", "Markarth": "Márkarz", "Nchuand-Zel": "Enchuánd Sel", "Salonia": "Salónia",
    "falmer": "fálmer", "Sinderion": "Sindérion", "Skingrad": "Eskíngrad", "Avrusa Sarethi": "Avrúsa Saréthi",
    "Froki": "Fróki", "Kyne": "Káin", "skeever": "eskíver", "Viarmo": "Viármo", "Svaknir": "Esváknir", "Numinex": "Númineks",
    "alik'r": "álikr", "Saadia": "Saádia", "Taneth": "Táneth", "Hammerfell": "Jámerfel", "Neloth": "Néloth",
    "Telvanni": "Telváni", "Ildari": "Ildári", "Solstheim": "Sólsteim", "Nurelion": "Nurélion", "Curalmil": "Curálmil",
    "Fralia": "Frália", "Olfrid": "Ólfrid", "Thorald": "Tórald", "Idolaf": "Ídolaf", "thalmor": "tálmor", "Faolan": "Fáolan",
    "Baldor": "Báldor", "Skaal": "Escáal", "stalhrim": "estáljrim", "Ancarion": "Ancárion", "Veleth": "Véleth",
    "Severin": "Séverin", "Vendil": "Véndil", "Vilur Ulen": "Vílur Úlen", "Hlaalu": "Jlaálu", "Arvak": "Árvak",
    "Árvakr": "Árvaker", "Sovngarde": "Sóvngard", "Dawnguard": "Dóngard", "Haknir": "Jáknir", "Gyldenhul": "Guíldenjul",
    "horkers": "jórkers", "Hermaeus Mora": "Jermáus Móra", "Dukaan": "Dukáan", "Kolbjorn": "Kólbiorn",
    "Ralis Sedarys": "Rális Sedáris", "Ralis": "Rális", "Ahzidal": "Asídal", "Durnehviir": "Durnevír", "Qahnaarin": "Kanáarin",
    "Kodlak": "Kódlak", "Ysgramor": "Ísgramor", "Wuuthrad": "Vúzrad", "Eorlund": "Éorlund", "Glenmoril": "Glénmoril",
    "Farkas": "Fárkas", "Meridia": "Merídia", "Kilkreath": "Kílcriz", "Malkoran": "Málcoran", "Potema": "Potéma",
    "Mehrunes": "Merúnes", "Wabbajack": "Uábayak", "Oghma Infinium": "Ógma Infínium", "Mzark": "Mezárk",
    "Gauldur": "Gáuldur", "Mikrul": "Míkrul", "Jyrik": "Yírik", "Sigdis": "Sígdis", "Folgunthur": "Folgúntur",
    "Saarthal": "Sáartal", "Geirmund": "Guéirmund", "Harald": "Járald", "Serana": "Serána", "Gelebor": "Guélebor",
    "Vyrthur": "Vírzur", "Harkon": "Járkon", "Auriel": "Áuriel", "Sheogorath": "Sheógorath", "Dervenin": "Dérvenin",
    "Nerevar": "Nérevar",
}

# Transcripciones (se rellenan tras leer cada una en `seleccionar`)
# 28-oct: transcripciones leídas una a una; casi todas son nombres que Whisper escribe distinto (Kyne→Cain, Froki→Froakie,
# Hlaalu→Halalu, Arvak→Arbak, stalhrim→Stalgrim, Wuuthrad→Búzrad…). Se regeneran p22_1 («Meri Skyrim») y cierre_1 (pausa 1,3 s).
CER_MAX_POR_FRASE = {'p22_1': 0.035, 'cierre_1': 0.02, 'intro_0': 0.02, 'p25_1': 0.017, 'p25_2': 0.073, 'p25_4': 0.024, 'p25_6': 0.014, 'p24_1': 0.04, 'p23_1': 0.026, 'p23_3': 0.028, 'p23_5': 0.054, 'p22_0': 0.033, 'p22_2': 0.045, 'p22_5': 0.06, 'p22_6': 0.042, 'p21_3': 0.026, 'p20_1': 0.058, 'p20_3': 0.054, 'p20_5': 0.024, 'p19_1': 0.018, 'p19_4': 0.019, 'p18_2': 0.02, 'p17_1': 0.023, 'p15_0': 0.032, 'p15_1': 0.025, 'p15_2': 0.034, 'p15_5': 0.032, 'p14_1': 0.024, 'p14_2': 0.039, 'p14_4': 0.028, 'p13_0': 0.044, 'p13_1': 0.03, 'p13_3': 0.016, 'p13_4': 0.051, 'p13_5': 0.019, 'p12_3': 0.035, 'p11_1': 0.021, 'p11_6': 0.023, 'p10_1': 0.036, 'p10_5': 0.036, 'p10_7': 0.024, 'p9_6': 0.019, 'p8_2': 0.029, 'p8_3': 0.027, 'p8_5': 0.027, 'p7_2': 0.019, 'p7_3': 0.018, 'p6_5': 0.019, 'p5_2': 0.031, 'p4_4': 0.018, 'p3_3': 0.045, 'p2_1': 0.027, 'p2_3': 0.029, 'p1_3': 0.025, 'p1_7': 0.021}
GAP_MAX_POR_FRASE = {'p23_2': 0.68, 'p23_3': 0.76, 'p21_6': 0.92, 'p20_1': 0.73, 'p13_3': 0.62, 'p12_3': 0.63, 'p9_5': 0.65, 'p8_5': 0.64, 'p3_3': 0.64}
TAIL_MAX_POR_FRASE = {'p24_1': 0.43, 'cierre_1': 0.41, 'intro_0': 0.44, 'p25_1': 0.55, 'p25_6': 0.46, 'p23_2': 0.76, 'p21_6': 0.67, 'p15_4': 0.5, 'p13_3': 0.47, 'p11_1': 0.52, 'p9_5': 0.46, 'p7_4': 0.66, 'p7_7': 0.52}   # CER 0: acaban hablando

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen; el sonido del juego va en ambiente_por (regla 26-oct-2026)
    # sonido original solo donde el clip bajó entero con audio: con +ba yt-dlp cortó en otro keyframe y 11 beats salieron cortos
    # (33, 35, 42, 77, 104, 106, 113, 127, 133, 144, 150 → rebajados sin audio con la misma url/desde o con otra búsqueda)
    # `_sonido_original.py habla/nivel`: fuera 120 (diálogo de Elisif que no viene al caso), 61 (comentarista) y 85 (−42 LUFS)
    ambiente_por={**{f"scene-{n:03d}": .85 for n in (101,)},                 # Durnehviir
                  **{f"scene-{n:03d}": .7 for n in (139,)},                  # Gauldur fulmina a sus hijos
                  **{f"scene-{n:03d}": .6 for n in (97, 152)}},              # Ahzidal, Wabbajack
    recorte_por={"scene-047": .12, "scene-110": .07},   # letterbox de origen · logo de pata arriba a la derecha
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),   # heredados de tes_*
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (armar_musica_ost.py), nunca Lyria

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En el video de las misiones que nunca debes hacer, @sebastiannarvaez6185 nos dejó el comentario con más me gusta. Que la Forja de Aetherium es larga, sí, pero que la corona merece la pena.",
        "Y @EnriqueJVidal-ei1nk nos contó que Arniel y la Forja fueron de sus misiones favoritas. Y de paso nos corrigió dos nombres. Apuntados.",
        "Así que hoy le damos la vuelta. Hoy no hay misiones que evitar. Hoy hay misiones que NUNCA debes saltarte.",
        "Misiones secundarias que mucha gente ni empieza. Y que esconden el mejor amuleto del juego, un caballo inmortal, una casa gratis, y un bastón que convierte a tus enemigos en queso.",
        "Veinticinco misiones, todas comprobadas, de la menos a la más imprescindible, y con lo que te llevas en cada una.",
        "Y quédate hasta el final, porque el número uno empieza con un mendigo en Soledad. Y acaba dentro de la cabeza de un emperador.",
    ]},
    {"id": "p25", "frases": [
        "Número veinticinco. Simas insondables.",
        "A partir del nivel catorce, en los muelles de Riften aparece una argoniana, De la Sima, dando vueltas y hablando sola.",
        "Te pide que lleves un léxico a Avanchnzel, una ruina dwemer enorme en el sur de Skyrim, en las montañas de Jerall.",
        "Y dentro vas viendo a los fantasmas de su antigua expedición. Mercenarios que no sabían dónde se metían, y que ella convenció para quedarse.",
        "No acaba bien. Breya muere junto a un centurión, y De la Sima escapa. Y la escena que lo cuenta nunca se ve, por una errata en el código del juego.",
        "La recompensa es Conocimiento antiguo, un efecto permanente. Tenía que subir un veinticinco por ciento la armadura enana.",
        "Por un error, valía con cualquier armadura. Y cuando Bethesda lo quiso arreglar en un parche, se equivocó al revés. Ahora vale con todas, menos con la enana.",
    ]},
    {"id": "p24", "frases": [
        "En el veinticuatro, La expedición perdida.",
        "En Markarth, el mago Calcelmo excava una ruina dwemer debajo de la propia ciudad, Nchuand-Zel. Y ha perdido el contacto con su expedición.",
        "Bajas, y vas encontrando a sus miembros uno por uno. Un diario, un arsenal, un cuerpo. No sobrevive nadie.",
        "Pero lo mejor está al final. En la sala de control tiras de una palanca, y los autómatas dwemer de toda la ruina se despiertan.",
        "Y se lían a golpes con los falmer. Tú bajas tranquilamente, mientras las máquinas limpian la ruina por ti.",
        "Y un detalle que nadie explica. La nota que encuentras va dirigida a una tal Salonia. Y en todo el juego, nadie sabe quién es.",
    ]},
    {"id": "p23", "frases": [
        "Número veintitrés. Vuelta a las raíces.",
        "En el Límite Sombrío, la caverna gigante que hay debajo de Skyrim, hay una casita dwemer con un cadáver dentro. Es Sinderion.",
        "Y si jugaste a Oblivion, lo conoces. Era el alquimista de Skingrad obsesionado con la raíz de nirn. Aquí vino a estudiar una roja, la raíz de nirn carmesí.",
        "Y por cierto, @alcoholikmisanthroper1934 nos recordó que se dice Oblivion, y no Oblivión. Tiene razón. Apuntado también.",
        "La misión es terminar su trabajo. Juntar treinta raíces de nirn carmesí, que solo crecen en la oscuridad, cerca del agua.",
        "Y llevárselas a su antigua colega, Avrusa Sarethi, a su granja cerca de Riften.",
        "El premio es Descubrimiento de Sinderion, un efecto permanente. Un veinticinco por ciento de probabilidad de sacar dos pociones en vez de una. Para siempre.",
    ]},
    {"id": "p22", "frases": [
        "En el veintidós, Las pruebas sagradas de Kyne.",
        "Al sureste de Paraje de Ivar vive un viejo cazador, Froki. Y te pide que caces a los espíritus guardianes de Kyne por media Skyrim.",
        "Un cangrejo del barro, un skeever y un lobo. Luego un oso, un mamut y un gato sable. Y al final, un trol.",
        "La recompensa es el Símbolo de Kyne. Diez por ciento menos de daño de los animales, y cinco por ciento más con el arco.",
        "Pero por un error, reduce el daño de todas las criaturas. Daedra y no muertos incluidos. Es como llevar unos ochenta y tres puntos de armadura extra.",
        "En la cueva del trol, además, está el arco de Froki. Y te deja quedártelo.",
        "Eso sí. Si se la rechazas una vez, Froki no te la vuelve a ofrecer nunca.",
    ]},
    {"id": "p21", "frases": [
        "Número veintiuno. Que no se apaguen las llamas.",
        "Para entrar en el Colegio de Bardos de Soledad, Viarmo te manda a buscar el Verso del rey Olaf, en el Respiro del Muerto.",
        "Y allí descubres la verdad. Olaf Ojo Único ejecutó al bardo Svaknir por dudar de que hubiera matado él al dragón Numinex.",
        "Y el fantasma de Svaknir pelea a tu lado contra el propio Olaf.",
        "Luego recitas el verso en el Palacio Azul. Y si quieres, improvisas que Olaf era en realidad el dragón Numinex.",
        "La quema del rey Olaf vuelve, y ahora es una fiesta cada semana. Con pastel de carne gratis. Que en realidad es un pastel de manzana.",
        "Y antes de seguir. @amadeoamaya7606 nos escribió que le gusta cómo presentamos la información, de una manera muy divertida. Gracias, de verdad.",
    ]},
    {"id": "p20", "frases": [
        "En el veinte, En tiempos de necesidad.",
        "A las puertas de Carrera Blanca te paran unos guerreros alik'r. Buscan a una mujer redguard que se esconde en la ciudad.",
        "Es Saadia, que trabaja en La yegua abanderada. Y te cuenta que es una noble de Hammerfell, y que la persigue el Dominio.",
        "Los alik'r te cuentan otra historia. Que ella vendió su ciudad, Taneth, al Dominio durante la Gran Guerra.",
        "Y aquí está la gracia. El juego no te da pruebas de ninguna de las dos versiones. Ninguna. Eliges a ciegas.",
        "Para hablar con su jefe tienes que sacar a un alik'r de la cárcel. Pagas la multa, cien monedas, y no lo sueltan nunca. El guarda pierde las llaves.",
        "Y si lo tuyo es el dinero, se puede cobrar a los dos bandos. Mil cien monedas por traicionar a todo el mundo.",
    ]},
    {"id": "p19", "frases": [
        "Número diecinueve. Viejos amigos.",
        "En Solstheim, el mago Neloth, de la Casa Telvanni, te manda a buscar a una antigua aprendiz suya, Ildari.",
        "Ildari se ofreció para un experimento con corazones de piedra. Y Neloth lo resume así. Que fue bastante molesto cuando murió.",
        "Pero no está tan muerta. La encuentras en la Torre de la Cúspide, y al final, le arrancas el corazón.",
        "Neloth te da un bastón, te deja entrar en la Casa Telvanni, y te promete una cama y un cofre en su torre.",
        "Que no existen. Es un error del juego. Pero viniendo de Neloth, nadie se sorprende.",
    ]},
    {"id": "p18", "frases": [
        "En el dieciocho, El Vial Blanco.",
        "En Ventalia, el viejo alquimista Nurelion ha pasado la vida buscando el Vial Blanco, un frasco legendario.",
        "Lo encuentras en la Cueva abandonada, custodiado por un draugr, Curalmil. Y está roto.",
        "Y Nurelion muere justo después de verlo. Toda una vida buscándolo, y se va en cuanto lo tiene en las manos.",
        "Su aprendiz, Quinto Navale, quiere repararlo en su honor. Nieve que no se derrite de la Garganta del Mundo, polvo de colmillo de mamut, y un corazón de espino.",
        "Y reparado, se rellena solo cada día con el efecto que tú elijas. Por ejemplo, cien de salud, o un cincuenta por ciento más de daño a una mano.",
    ]},
    {"id": "p17", "frases": [
        "Número diecisiete. Desaparecido en acto de servicio.",
        "En el mercado de Carrera Blanca, Fralia Melena Gris discute con Olfrid Batallador. Su hijo Thorald está desaparecido, y ella cree que sigue vivo.",
        "Y tiene razón. Lo tienen preso los thalmor, en el Bastión de la Guardia del Norte.",
        "Para demostrarlo necesitas una misiva imperial de la casa de los Batallador. Con ganzúa, con chantaje, o convenciendo a Idolaf.",
        "Luego asaltas el bastión y sacas a Thorald. Y de paso, saqueas un fuerte entero lleno de armaduras thalmor.",
        "La recompensa es un arma encantada que el padre, Eorlund, forjó para su hijo.",
        "Y había una forma pacífica, pidiendo ayuda al general Tulio. El diálogo está grabado. Pero por un error, nunca se activa.",
    ]},
    {"id": "p16", "frases": [
        "En el dieciséis, La leyenda de Águila Roja.",
        "Todo empieza con un libro. La leyenda de Águila Roja, un rey rebelde de La Cuenca.",
        "Cuenta que Faolan, Águila Roja, le entregó a una bruja su corazón, su voluntad y su humanidad.",
        "Y juró que, cuando La Cuenca fuera libre, le devolvieran su espada para volver a levantarse.",
        "Recuperas la espada, Furia del Águila Roja, en las Torres Hendidas, y la llevas a su túmulo.",
        "Se la devuelves. Se levanta con sus esqueletos. Y lo matas. Le cumples la profecía, y lo que se levanta te lo cargas.",
        "Y la espada se convierte en la Perdición del Águila Roja. Diez de fuego, y los no muertos de poco nivel arden y salen huyendo.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Un nuevo yacimiento de stalhrim.",
        "En Solstheim, en la Aldea Skaal, el herrero Baldor Hierro Forjado sabe trabajar el stalhrim. El hielo encantado que nunca se derrite.",
        "Pero solo te enseña si le ayudas. Primero unos thalmor, en una cabaña abandonada. Luego un tal Ancarion, que quiere el stalhrim para él.",
        "A Ancarion puedes convencerlo, asustarlo, o con mucha elocuencia, hacerte su socio y venderle stalhrim.",
        "Y la recompensa es saber forjarlo, con herrería ochenta. Armas con el daño del ébano y menos peso. Armadura pesada como la de dragón, pero más ligera.",
        "Y los encantamientos de escarcha son un veinticinco por ciento más fuertes sobre stalhrim.",
        "Sin esta misión, el mejor material de la expansión se queda bloqueado. Para siempre.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, Se sirve mejor fría.",
        "En Roca del Cuervo, el capitán Veleth sospecha de alguien. Y la investigación te lleva a la familia más generosa del pueblo, los Severin.",
        "Que son una tapadera. Trabajan para la Casa Hlaalu, y preparan una venganza.",
        "Las pistas te llevan, de noche, a una tumba ancestral, y a la caja fuerte de su propia mansión.",
        "Al final, Vendil Severin ataca gritando por Vilur Ulen y por la Casa Hlaalu. Era su hijo, y quería vengar a su padre.",
        "Y la recompensa es su casa. La Mansión Severin, con todo lo que tiene dentro. Y oro según tu nivel. A partir del sesenta, diez mil monedas.",
        "Así que no robes nada de esa casa antes de tiempo. Te lo vas a quedar todo igual.",
        "Y aquí va otro. @marcocho_23 nos contó que se pasó el juego como cuarenta veces, y no sabía algo que contamos. Eso es justo lo que buscamos en cada video. Gracias.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. El cráneo de Arvak.",
        "En el Recordatorio de las Almas, el plano de los muertos de Dawnguard, un alma perdida grita un nombre. Arvak.",
        "Busca a su caballo. Su cráneo está en un santuario con cuatro almas arrodilladas, que en cuanto lo tocas se convierten en brumosos.",
        "Y la recompensa es Invocar a Arvak. Un caballo esqueleto en llamas, que no muere para siempre, no cuesta nada, y aparece donde estés.",
        "Y funciona donde los demás caballos no llegan. En Solstheim, y hasta en Sovngarde.",
        "Su nombre viene de Árvakr, uno de los caballos que tiran del carro del sol en la mitología nórdica.",
        "Y con la ventaja Almas gemelas, puedes invocar dos Arvak. El único establo de Skyrim que te cabe en el bolsillo.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, Estigma mortal.",
        "A partir del nivel treinta y seis, en Solstheim encuentras un libro sobre Haknir Estigma Mortal. Un pirata. Y su tesoro.",
        "Es una búsqueda del tesoro de verdad. Un mapa, cuatro cofres escondidos por la costa, sin marcadores, y en cada uno, una pieza de su armadura.",
        "Y al final, el Túmulo de Gyldenhul, en la Isla de los horkers. Con ochenta montones de oro.",
        "Y al saquear el oro, cae un rastrillo y te encierra. Porque es un tesoro pirata maldito, como debe ser.",
        "Allí está el fantasma de Haknir. Se teletransporta cuando lo hieres, y llama a su tripulación.",
        "La armadura sube tu aguante y tu capacidad de carga con cada pieza. Y te llevas dos cimitarras que absorben salud y magia, y más de seis mil cuatrocientas monedas.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Libro negro, El regente amarillento.",
        "Los libros negros de Hermaeus Mora te llevan a Apócrifa. Y este está al fondo del Túmulo de Risco Blanco, en el norte de Solstheim, detrás de un sacerdote dragón, Dukaan.",
        "Dentro, Apócrifa está a oscuras. Y la oscuridad te quita vida aunque tengas todas las resistencias. Hay que llevar luz.",
        "Al final eliges una de tres habilidades. Y las tres son permanentes.",
        "Buscador de poder, diez por ciento a las habilidades de combate. Buscador de hechicería, hechizos más baratos y encantamientos más fuertes. O Buscador de sombras, diez por ciento al sigilo.",
        "Y si te arrepientes, relees el libro y cambias. Gratis. Hermaeus Mora es el único príncipe daédrico con política de devoluciones.",
        "Y de camino, te llevas la máscara de Dukaan, y una palabra del grito Ciclón.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, Desenterrado.",
        "En el Túmulo de Kolbjorn, en Solstheim, un elfo oscuro llamado Ralis Sedarys excava. Y te pide dinero para seguir. Mil monedas.",
        "Luego dos mil, porque desaparecieron los mineros. Luego tres mil, porque murieron los mercenarios. Luego cinco mil.",
        "Cada pago, setenta y dos horas de espera. Y el mensajero que te trae las cartas empieza a decir que Ralis le da miedo.",
        "Y la última nota dice solo una cosa. Se te necesita.",
        "Llegas, y Ralis está despertando a Ahzidal, un sacerdote dragón. Once mil monedas para financiar al jefe que te quiere matar.",
        "Pero sus reliquias valen cada moneda. La máscara de Ahzidal, cincuenta por ciento de resistencia al fuego. Y con cuatro reliquias puestas, diez más a encantamiento.",
        "Y al final eliges. Matar a Ralis, o perdonarlo y llevártelo de seguidor.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Durnehviir.",
        "En el Recordatorio de las Almas te enfrentas a un dragón no muerto, Durnehviir. Y cuando lo vences, no muere. Te llama Qahnaarin. Vencedor.",
        "Hace siglos pactó con los Amos ideales que guardaría a Valérica hasta que ella muriera. Lo que no le dijeron es que Valérica era inmortal.",
        "Su nombre significa maldición que nunca muere. Y lleva atrapado ahí desde entonces.",
        "Al salir te enseña a invocarlo. Un dragón aliado, que además trae a sus propios esbirros.",
        "Y cada vez que lo invocas en Skyrim, te enseña una palabra de Desgarro del alma. Trescientos de daño, atrapa el alma, y si el enemigo muere, se levanta como tu aliado.",
        "El grito más bestia de Dawnguard. Y te lo enseña un dragón que lleva siglos sin respirar aire libre.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, La gloria de los muertos.",
        "Es el final de los Compañeros. Kodlak Melena Blanca, el Heraldo, ha muerto. Y su alma está condenada por la sangre de bestia.",
        "Para liberarla vas a la Tumba de Ysgramor, con el hacha Wuuthrad, que Eorlund ha reparado en la Forja del Cielo.",
        "En la Llama del Heraldo quemas una cabeza de bruja de Glenmoril. Y el espíritu de Kodlak queda libre para ir a Sovngarde.",
        "Con otra cabeza te puedes curar tú. Si no lo haces ahí, luego tendrás que curar antes a dos Compañeros.",
        "Te quedas con Wuuthrad, y con el Escudo de Ysgramor, veinte de resistencia a la magia y veinte de salud. Y te nombran Heraldo.",
        "Y un detalle. Farkas se para delante de las telarañas, porque les tiene pánico a las arañas. El hombre lobo más grande de Skyrim.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. Al alba.",
        "En algún cofre de Skyrim encontrarás la Luz de Meridia. Una esfera que puede salir en más de ciento cincuenta sitios distintos.",
        "Te lleva al Monte Kilkreath, a la estatua de la diosa. Y Meridia te eleva por los aires para hablarte.",
        "Te manda limpiar su templo de un nigromante, Malkoran, guiando un rayo de luz de pedestal en pedestal.",
        "Por el camino hay cuarenta y tres cadáveres profanados, cada uno con su oro. Más de cinco mil monedas en total.",
        "La recompensa es el Quebrantador de amaneceres. Fuego extra, y una explosión que destruye o ahuyenta a los no muertos. Y en Skyrim, casi todo está muerto.",
        "Y cuidado, que Meridia te puede soltar desde el cielo. Si llevas mucho peso, el golpe te mata.",
        "Y antes del podio. @franzindriago7950 nos escribió que nadie le había explicado la historia de Nerevar y la traición del Tribunal como nosotros. Comentarios así son los que nos hacen seguir.",
    ]},
    {"id": "p6", "frases": [
        "En el seis, El despertar de la Reina Loba.",
        "En Soledad, Falk Barba de Fuego te pide investigar unas luces en la Cueva Cráneo de Lobo. Parece una falsa alarma.",
        "No lo es. Unos nigromantes intentan resucitar a Potema, la Reina Loba. Reina de Soledad, y nieta de un emperador.",
        "Los paras. Y un tiempo después, un mensajero te trae una carta. Potema se les ha escapado.",
        "Bajas a las Catacumbas de Potema, debajo del templo, y su espíritu te insulta mientras levanta muertos contra ti.",
        "Las flechas no le hacen nada. La magia, sí. Y al final recuperas su calavera, para que la consagren.",
        "La recompensa es el Escudo de Soledad. Y de paso, esta misión te abre el Ala de Pelagio del Palacio Azul. Guarda ese dato para el número uno.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El guerrero de ébano. El examen final de Skyrim.",
        "Cuando llegas al nivel ochenta, al entrar en una ciudad se te acerca un guerrero con armadura de ébano. Y te reta.",
        "Ha vivido demasiado. Quiere una muerte digna para llegar a Sovngarde. Y ha decidido que se la des tú.",
        "Te espera en la Última Vigilia, al noreste de Riften. Y no te ataca hasta que le pegas tú.",
        "Tiene dos mil setenta y uno de salud, usa gritos, y tiene Reflejar golpes. Tus propios ataques poderosos te pueden matar.",
        "Es inmune al Wabbajack. Pero la Cuchilla de Mehrunes lo mata al instante.",
        "Y al morir, te da las gracias. Y te deja todo su ébano encantado, gemas perfectas, y una gema de alma negra llena.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, Descifrar lo transmundano.",
        "Al norte de Hibernalia, en un puesto en el hielo, vive Séptimo Signo. Un erudito que lleva años intentando abrir un cubo dwemer.",
        "Te manda al Límite Sombrío, a la Torre de Mzark, a leer un Pergamino antiguo. Y luego a por sangre de cuatro tipos de elfo, y de un orco.",
        "Abres el cubo. Séptimo esperaba encontrar el corazón de un dios. Y dentro hay un libro.",
        "El Oghma Infinium. Y Hermaeus Mora, que le había prometido todo, lo desintegra delante de ti. Así le paga.",
        "El libro te da cinco puntos en seis habilidades de la senda que elijas. Poder, sombra o magia. Treinta niveles de habilidad, gratis.",
        "Y cuidado. Si lo sueltas antes de leerlo, se queda como un libro normal. Sin nada.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Leyenda prohibida.",
        "Empieza leyendo un libro, Leyendas perdidas. Y cuenta un crimen que la historia borró.",
        "Gauldur era un archimago. Sus tres hijos lo asesinaron, y se repartieron su amuleto en tres pedazos. Y el rey Harald borró todo registro del crimen.",
        "Cada hijo está en una mazmorra distinta. Mikrul en Folgunthur, Jyrik en Saarthal, y Sigdis en la Sala de Geirmund, con sus clones.",
        "Juntas los tres fragmentos, y en la Roca de la Cuenca aparece el propio Gauldur. Y fulmina a sus tres hijos.",
        "El Amuleto de Gauldur. Treinta más de salud, de magia y de aguante. El mejor amuleto sin trampas de todo el juego.",
        "Y un consejo. Las cuatro mazmorras se generan al leer el libro. Si lo lees con poco nivel, el botín se queda flojo para siempre. Lo ideal, nivel treinta y seis.",
    ]},
    {"id": "p2", "frases": [
        "En el dos, Tocando el cielo.",
        "Si te saltas Dawnguard, te saltas esto. Con Serana llegas a la Cueva de Sima Negra, y un caballero, Gelebor, te abre un pasaje.",
        "Al otro lado, el Valle Olvidado. Un valle escondido entre la nieve, con lagos helados, ermitas y dragones. El rincón más bonito de Skyrim.",
        "Al final, en la Capilla de Auriel, el Archicoadjutor Vyrthur te confiesa algo. La profecía que persigue Harkon la escribió él mismo. Por venganza contra su dios.",
        "El Arco de Auriel ya salió en las armas más poderosas. Pero lo que no te contamos es el viaje para conseguirlo.",
        "Con flechas bendecidas, el sol lanza rayos durante diez segundos. Y con flechas malditas, apagas el sol hasta la mañana siguiente.",
        "Es el único arco de Skyrim con el que le disparas al sol. Y le das.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. La mente de la locura.",
        "En Soledad, un mendigo, Dervenin, te cuenta que su señor está de vacaciones. Y que necesita que lo vayas a buscar.",
        "Su señor es Sheogorath, el príncipe de la locura. Y está dentro de la mente de un emperador muerto, Pelagio el Loco.",
        "Entras por el Ala de Pelagio del Palacio Azul. Y apareces sentado a la mesa con Sheogorath, que te da el Wabbajack, sin límite de cargas.",
        "Dentro hay tres pruebas. Una pelea entre la confianza y la ira, unos terrores nocturnos, y la paranoia de Pelagio. Y todo se arregla a golpe de bastón.",
        "Cuando sales, el Wabbajack se queda contigo. Puede convertir a un enemigo en pollo, en conejo, en queso, en un bollo dulce, o en una lluvia de oro.",
        "Y si conviertes en bollo a un personaje esencial, y te lo comes, desaparece del juego para siempre.",
        "Y lo que hay en la mesa de Sheogorath no es de nadie. Todo lo que cojas, sale contigo.",
        "Por eso es el número uno. Las demás te dan oro, armaduras o un caballo. Esta te da una cena con Sheogorath. Y eso no tiene precio.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Veinticinco misiones que nunca debes saltarte, de una argoniana que habla sola, a un dios que se fue de vacaciones.",
        "Y antes de irnos. @edupiles8494 nos dijo que sigue alucinando con la cantidad de locos que adoramos el lore. Y @KRONOX-LEGEND nos dio las gracias por contarle lo de los divinos.",
        "Gracias a todos. Leemos todos los comentarios, los que nos felicitan y los que nos corrigen, y los tenemos en cuenta para mejorar cada video. Este, sin ir más lejos, nació de dos comentarios.",
        "Y ahora te toca a ti. ¿Cuál de estas te saltaste? Y si falta alguna que tú no te saltarías nunca, déjala en los comentarios.",
        "Y si quieres lo contrario, en el canal tienes las quince misiones de Skyrim que nunca debes hacer.",
    ]},
]
