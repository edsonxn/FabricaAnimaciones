# -*- coding: utf-8 -*-
"""GUION — «La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (Crónicas de Warcraft, 25-nov-2026; dom 29-nov 09:00 CDMX).
Motor SECUENCIA YT (gameplay por beat). Flujo y reglas: docs/estilo_secuencia_yt.md (§ REGLA DE ORO, § KIT DE 4 ESTILOS).
Tema elegido por el usuario (25-nov): una variable sobre «La RUTA del 1 al 60» = el tema (profesiones en vez de niveles).
Investigación: videos/_investigacion_wow_ruta_profesiones.md (nada de cifras fuera de ahí). La voz NO cita fuentes.
OVERGEAR campaña 3, integración 2: http://overgear.s.gy/CRONICAS/7 · CRONICAS10 · texto = promo aprobado por Alice
(videos/overgear_promo_en_c3/promo.py) adaptado. Brief §7: «WoW Forever», no es temporada (ni «temporada» en el guion), sin tier
lists ni «mejor clase/profesión», sin Heroico/M+, bandas fijas, sin BiS, nada contra comprar oro.
VOZ: Remy (Applio) entero. Frases < 200 caracteres, sin corchetes, nunca de 1-3 palabras. Cifras en letra. DURACIÓN: ~27-30 min.
Comentarios (≤ 10 días, ninguno usado antes): julsi @julsikakku5276 · gracias1 @jesusizquierdoalvarez5505 @Oscar_AnV @baron_rata
@steven_p_w4279 · burla0 @Goca912 · burla1 @crisisx94 · burla2 @SoyoyoS (tarjetas en pegatinas/_comentarios.txt).
"""

TITULO = "La RUTA de PROFESIONES del 1 al 300 en WoW Forever"
ARCHIVO = "wow_ruta_profesiones"
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
    "Riverglades": "Ríverglèids", "Shen'dralas": "Shendrálas", "Theramore": "Terámor", "Auberdine": "Óberdin",
    "Gadgetzan": "Gádguetsan", "Dalaran": "Dálaran", "Hyjal": "Jáyal", "Un'Goro": "Ungóro", "Azshara": "Asshára",
    "Uldaman": "Uldáman", "Desolace": "Desolás", "Tirisfal": "Tirisfál", "Teldrassil": "Teldrásil", "Mulgore": "Múlgor",
    "Durotar": "Durotár", "Alterac": "Álterac", "Onyxia": "Oníxia", "Ventormenta": "Ventorménta", "Orgrimmar": "Orgrímar",
    "Elwynn": "Éluin", "Forjaz": "Forjáz", "Entrañas": "Entráñas", "Mojache": "Mojáche", "Darnassus": "Darnásus",
    "Loch Modan": "Lok Módan", "Khadgar": "Kádgar", "Bael'dun": "Báeldun", "Scholomance": "Escolománs", "Stratholme": "Estrázolm",
    "Saru Steelfury": "Sáru Estílfiuri", "Bengus Deepforge": "Béngus Dípforch", "Alard Schmied": "Álard Shmíd",
    "Brikk": "Brík", "Derotain": "Derotéin", "Gilnid": "Gílnid", "Argelmach": "Árguelmach", "Roxxik": "Róksik",
    "Springspindle": "Esprínspindel", "Buzzek": "Búsek", "Kayleena": "Keilína", "Kor'gar": "Kórgar", "Sneed": "Esníd",
    "Ezra Grimm": "Ésra Grím", "SAF-T": "séif ti", "Shadetooth": "Shéidtuz", "Shurome": "Shuróme", "Rogvar": "Rógvar",
    "Kylanna": "Kilána", "Lady Anacondra": "Léidi Anacóndra", "Telonis": "Telónis", "Jarael": "Yaráel",
    "Hahrana": "Jarána", "Drakk Stonehand": "Drák Estónjand", "Elvis": "Élvis", "Vectus": "Véctus",
    "Josef Gregorian": "Yósef Gregórian", "Georgio Bolero": "Yóryio Boléro", "Charles Worth": "Chárls Uórz",
    "Melanori": "Melanóri", "Daryl Stack": "Dáril Esták", "Timothy Worthington": "Tímozi Uórzinton", "Pexmit": "Péksmit",
    "Anastari": "Anastári", "Hgarth": "Gárz", "Kitta": "Kíta", "Azora": "Azóra", "Vanessa Sellers": "Vanésa Sélers",
    "Annora": "Anóra", "Nanaya": "Nanáya", "Whimsyfin": "Uímsifin", "Serpentis": "Serpéntis", "Wulan": "Uúlan",
    "Shandrina": "Shandrína", "Mystral": "Místral", "Heming": "Jéming", "Nat Pagle": "Nat Péiguel", "Gelihast": "Gélijast",
    "Jammal'an": "Yamálan", "Deneb": "Dénep", "Balai Lok'Wein": "Balái Lokuéin", "Gregory Victor": "Grégori Víctor",
    "Gustaf VanHowzen": "Gústaf Van Jáusen", "Ortak Lomgok": "Órtak Lómgok", "Steven": "Estíven", "SoyoyoS": "Soyóyos",
    "Julsikakku": "Yulsikáku", "Goca": "Góca", "Remy": "Rémi",
}
FONETICA = FONETICA_APPLIO
CER_MAX_POR_FRASE = {   # 25-nov: hyps leídas una a una (nombres propios, cifras en número, «veta/beta»)
    'intro_1': 0.030, 'p01_10': 0.032, 'p01_11': 0.036, 'p01_14': 0.030, 'p02_2': 0.034, 'p02_4': 0.046, 'p02_10': 0.028, 'p03_3': 0.049, 'p03_4': 0.059, 'p03_11': 0.063, 'gracias1_2': 0.040, 'p04_2': 0.044, 'p04_4': 0.051, 'p04_5': 0.027, 'p04_6': 0.034, 'p04_7': 0.031, 'p04_11': 0.034, 'p05_3': 0.022, 'p05_6': 0.053, 'p05_7': 0.030, 'p05_12': 0.033, 'burla1_2': 0.025, 'p06_5': 0.026, 'p06_9': 0.022, 'p06_11': 0.029, 'p07_2': 0.047, 'p07_4': 0.036, 'p07_5': 0.036, 'p07_7': 0.022, 'p07_12': 0.029, 'p08_2': 0.073, 'p08_4': 0.068, 'p08_6': 0.039, 'p08_13': 0.032, 'p09_4': 0.028, 'p09_5': 0.050, 'p09_7': 0.028, 'p10_6': 0.035, 'p10_8': 0.030, 'p11_3': 0.030, 'p11_4': 0.033, 'p11_5': 0.036, 'p11_7': 0.024, 'p12_4': 0.054, 'p12_6': 0.134, 'p12_9': 0.048, 'combos_3': 0.033, 'p02_3': 0.055, 'p11_10': 0.023, 'p06_3': 0.21, 'cierre_0': 0.025,
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
    recorte_por={},
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080, evitar_canales=[]),
)

ESCENAS = [
    {"id": 'intro', "pre": 0.3, "frases": [
        'En World of Warcraft Forever, el alquimista ya no hace pociones de sanación. Ahora las puede hacer cualquiera, con la profesión que casi todos dejan para el final.',
        'Hay una mena nueva en Monte Hyjal que no se puede fundir en ninguna forja de Azeroth. Y una profesión que, para llegar al trescientos, te pide un telar que solo se fabrica con trescientos.',
        'En la primera semana, los jugadores pusieron más de veintiocho millones de objetos de campamento. Y sin campamento, te faltan las estaciones de media lista de recetas.',
        'Hace unos días hicimos la ruta del uno al sesenta, zona por zona. Hoy toca la otra ruta, la que vas subiendo al mismo tiempo: la de las profesiones.',
        'Son doce profesiones, y cada una tiene su camino del uno al trescientos, en cuatro tramos. Para la Alianza y para la Horda, con el mapa de dónde entrenar y dónde recoger.',
        'Y en cada parada, lo que cambió en Forever: recetas nuevas, materiales nuevos, y lo que la guía que te sabías de memoria ya no sabe.',
        'Empezamos por lo que alimenta a todas las demás, la recolección, y terminamos con la profesión que más cambió. Te adelanto que no es la que imaginas.',
    ]},
    {"id": 'reglas', "frases": [
        'Primero, las reglas del juego. Hay nueve profesiones principales y tres secundarias, y no hay joyería ni inscripción: son exactamente doce.',
        'Puedes llevar dos principales por personaje. Las tres secundarias, cocina, pesca y primeros auxilios, van aparte, y esas no se pueden olvidar.',
        'Entrenar cuesta diez de cobre el primer rango, cinco de plata el segundo, cincuenta de plata el tercero y cinco de oro el de artesano. Unas cinco de oro y media por profesión.',
        'El rango de oficial pide nivel diez, el de experto nivel veinte y el de artesano nivel treinta y cinco. Y el artesano no te lo enseña cualquiera: muchas veces hay que viajar a buscarlo.',
        'Novedad de Forever: cada zona inicial tiene entrenadores júnior de minería, herboristería y desuello, que te enseñan hasta el setenta y cinco sin pisar la capital.',
        'Las profesiones tienen ventana propia, con la tecla K, con buscador, filtros y un botón de crear todo. Y la mochila tiene una quinta ranura, solo para la bolsa de componentes.',
        'Y ninguna profesión da un bonus pasivo. Su valor está en lo que fabricas, y en algo nuevo que vas a ver en cada parada: el campamento.',
    ]},
    {"id": 'p01', "post": 6.5, "frases": [
        'Parada uno. Minería, la profesión que alimenta a la herrería y a la ingeniería.',
        'Del uno al sesenta y cinco, cobre, en cualquier zona inicial. En Forever hay vetas de cobre pobres en los valles de inicio, y un entrenador júnior en cada uno.',
        'Los elfos de la noche, que no tenían cobre en Teldrassil, ahora pican fragmentos de ámbar. Dan mena de cobre, aunque solo suben la habilidad hasta veinte.',
        'En Mulgore hay una cueva con cinco vetas de cobre que reaparecen tan rápido que casi no hace falta salir. La forja más cerca está en la Excavación de Bael\'dun.',
        'Del sesenta y cinco al ciento veinticinco, estaño y plata. La Alianza, en una cueva de Los Humedales llena de estaño, y la Horda, en el Bosque de Argénteos o en Laderas de Trabalomas.',
        'Del ciento veinticinco al ciento setenta y cinco, hierro y oro, en las Tierras Altas de Arathi o en Las Mil Agujas.',
        'Y ojo, que la zona nueva de Claros del Río tiene más vetas de hierro que ninguna otra zona del mapa, unas ciento treinta.',
        'Del ciento setenta y cinco al doscientos cuarenta y cinco, mitril y veraplata, en Tierras del Interior o en Tanaris. Aprende el rango de artesano antes de salir.',
        'Y para cerrar, torio pequeño en Un\'Goro o en Frondavil, y torio rico en Cuna del Invierno, en la Peste del Este o en Las Estepas Ardientes.',
        'Si vas con prisa, existe la opción de fundir mena comprada en la subasta: unas ciento cuarenta de cobre y setenta de estaño te llevan hasta el ciento cinco.',
        'Lo nuevo de Forever: la mena se apila de veinte en veinte, y al picar salen materiales escasos: pirita, bauxita y pecblenda. Con la pecblenda se funde la barra de azerotio.',
        'Y en Monte Hyjal está la única mena nueva: la mena de torio pesada, en unas ciento veinte vetas. Pero esa no se funde en ninguna forja de Azeroth.',
        'Para fundirla necesitas una fundición de magma, un objeto de campamento cuyo plano suelta el Embajador Latifuego, en Profundidades de Roca Negra.',
        'Los otros dos objetos de campamento del minero son la magnetita, que da poder de ataque a todo el campamento, y el jardín rocoso, que hace crecer una veta con el tiempo.',
        'Y un dato para el final de la ruta: Monte Hyjal tiene, además, más de cien vetas de torio rico. Para los últimos puntos, es el sitio.',
    ]},
    {"id": 'overgear', "post": 2.6, "frases": [
        'Y antes de la segunda parada, algo que ninguna profesión te enseña: cómo sacarle más a tu personaje en combate. Para eso existe el patrocinador de hoy.',
        'Este video lo patrocina Overgear, con su coaching para World of Warcraft Forever.',
        'Son sesiones individuales por horas, por voz o por texto. Y juegas tú con tu personaje todo el tiempo.',
        'Un coach mira tus talentos, tu rotación y tus propios errores, con la versión del juego que está activa hoy.',
        'Porque las guías no siempre van al día. Una rama de talentos escrita antes del último ajuste ya puede estar desfasada.',
        'Y si todavía vas camino del sesenta, también te ayudan con eso.',
        'Y para las bandas del nueve de diciembre: resistencia al fuego para la Guarida de Onyxia, consumibles, y qué equipo previo a la banda vale la pena buscar.',
        'Muchos de esos consumibles, por cierto, salen de las profesiones de este video.',
        'Si reservas dos horas o más, ahorras un cinco por ciento, con reembolso en cada pedido. Y lo que aprendes se queda contigo para el siguiente ajuste.',
        'El enlace está en la descripción, y hay un código para ti.',
        'Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.',
    ]},
    {"id": 'p02', "post": 6.5, "frases": [
        'Parada dos. Herrería, la que se come casi todo lo que pica el minero.',
        'Del uno al setenta y cinco, piedras de afilar y piedras de pulir. Y un ajuste del diez de noviembre: la piedra de pulir burda ahora da puntos hasta el noventa.',
        'Del setenta y cinco al ciento cuarenta, bronce: varas de plata, leotardos y brazales. Calcula unas trescientas barras de bronce hasta el ciento cincuenta.',
        'Para el rango de experto vas a la capital: en Orgrimmar lo enseña Saru Steelfury, y en Forjaz, un enano, Bengus Deepforge, junto a la gran fragua.',
        'Y la Alianza tiene una opción nueva: Alard Schmied, en Dalaran, enseña hasta el doscientos veinticinco. En Darnassus, en cambio, no hay herrero: los elfos entrenan en Auberdine.',
        'Del ciento cuarenta al doscientos diez, cuarenta brazales de hierro verde, brazales de escamas doradas y pantalones de placas de mitril.',
        'El rango de artesano lo enseña Brikk Finoficio, en Bahía del Botín, a los dos bandos. Y en Tanaris, Derotain Sorbelodo te da misiones de piezas imperiales.',
        'Y aquí viene el golpe: del doscientos setenta al trescientos, calcula entre quinientas y mil doscientas barras de torio. La diferencia es si encuentras o no un par de planos.',
        'Lo nuevo de Forever: ocho planos de placas bendecidas que suben del doscientos cuarenta al trescientos, y caen de criaturas del mundo. El peto, de unas arpías de Monte Hyjal.',
        'Y aquí entra el Favor de comerciante, el sistema nuevo más grande de las profesiones. Se gana llenando cajones de materiales para dos campamentos de mercaderes.',
        'La Horda lo tiene al oeste de El Cruce, en Los Baldíos, y la Alianza en Tres Caminos, al oeste de Crestagrana. Y los dos venden las mismas recetas.',
        'Para la herrería hay sesenta y una recetas de Favor: conjuntos de malla y de placas para cada papel del grupo.',
        'En el campamento, el herrero pone una rueda de afilar, que da fuerza. Luego un yunque, y al llegar a trescientos, la forja maestra, que piden muchas recetas.',
        'El plano del yunque lo suelta Gilnid, en Las Minas de la Muerte, y el de la forja maestra, el Señor gólem Argelmach, en Profundidades de Roca Negra.',
        'Y un detalle de combate: en Forever, las piedras de afilar ya se acumulan con los venenos y con Viento Furioso.',
    ]},
    {"id": 'julsi', "frases": [
        'Y aquí va un espectador de esta misma pareja. Nos contó Julsikakku que, jugando dos o tres horas al día, llevaba minería ciento cuarenta y cinco y herrería ciento veinte en cinco días.',
        'A su ritmo, sin correr. Y en otro comentario ya iba por el treinta y seis, como minero y herrero, rumbo a la zona nueva. Gracias por enseñarnos que la ruta se hace al paso de cada quien.',
    ]},
    {"id": 'p03', "post": 6.5, "frases": [
        'Parada tres. Ingeniería, el otro destino del mineral.',
        'Del uno al cincuenta y seis, polvo explosivo tosco y tornillos de cobre, y no te olvides de la llave de tuerca arcoluz. Empieza en Orgrimmar o en Forjaz, porque ahí está también el experto.',
        'Del cincuenta y seis al ciento cincuenta, bombas de cobre, dinamita, tubos de bronce y cacharros zumbones.',
        'Del ciento cincuenta al doscientos, con Roxxik en Orgrimmar o con Springspindle en Forjaz: marcos de bronce, granadas de hierro, y quince ovejas explosivas.',
        'El rango de artesano lo enseña, en el pueblo goblin de Gadgetzan, Buzzek Giracorchete, a los dos bandos. Y, novedad de Forever, también Kayleena Encantaflores, en Monte Hyjal.',
        'Y para el final, trastos y tubos de torio: unas ciento setenta y cinco barras de torio. El esquema del tubo se compra en Cuna del Invierno, o con Kor\'gar, en Claros del Río.',
        'Y un aviso para la Horda: en Cima del Trueno no hay ingeniero. Y en la Alianza, tampoco lo hay en Darnassus.',
        'Lo nuevo de Forever: el gnomo ya no recibe sus quince puntos gratis de ingeniería. A cambio, sus cacharros fallan menos.',
        'Hay veintiséis recetas de Favor, y la más curiosa es la versión segura de los explosivos: dinamita y bombas que puede lanzar quien no es ingeniero.',
        'También hay un arma arrojadiza nueva, una bolsa de bombas que no gasta munición. Y al trescientos, el parapente goblin ultraliviano.',
        'Y sus objetos de campamento son los únicos que no dan un beneficio, sino un servicio: un robot que vende componentes a todo el campamento, y un robot de reparación.',
        'El plano del robot de reparación lo suelta Sneed, en Las Minas de la Muerte. Y al trescientos, el banco de trabajo de anarquista, que suelta Ezra Grimm en Stratholme.',
    ]},
    {"id": 'burla0', "frases": [
        'Y antes de seguir, un comentario. En la ruta del uno al sesenta, un espectador, Goca, nos escribió: era mejor hacer un video para cada facción, me enredaste más de lo que me ayudaste.',
        'Pues hoy, Goca, tengo buenas noticias: un lingote de cobre de la Alianza pesa exactamente lo mismo que uno de la Horda. Las profesiones casi no saben de facciones.',
        'Y donde sí cambian, que es en los entrenadores, te lo digo separado y con el mapa de cada bando. Si aun así te enredo, por lo menos ya sabes dónde comprar vendas.',
    ]},
    {"id": 'gracias1', "frases": [
        'Y gracias a quienes nos escriben. Jesús, que juega desde dos mil cinco, nos dice que Forever le devolvió la nostalgia de sus inicios, y que el canal le sirve a veteranos y a nuevos.',
        'Óscar volvió al juego después de un descanso y nos dio las gracias por la ruta, porque llevaba semanas peleándose con Crestagrana.',
        'Y Barón Rata ya va por el treinta, y subiendo. Y un espectador, Steven, que ni siquiera juega, nos dejó algo muy bonito: que le alegra ver que World of Warcraft sigue vivo.',
        'Gracias a los cuatro. Todos los comentarios se leen, y muchos acaban aquí.',
    ]},
    {"id": 'p04', "post": 6.5, "frases": [
        'Parada cuatro. Herboristería, la que alimenta a la alquimia y, en Forever, también a los primeros auxilios.',
        'Del uno al setenta, flor de paz y hojaplata en cualquier zona inicial. Ahí hay también versiones marchitas y atrofiadas, y su entrenador júnior.',
        'Del setenta al ciento quince, marregal y brezospina en el Bosque de Argénteos, en Loch Modan o en Costa Oscura.',
        'Del ciento quince al ciento setenta, Laderas de Trabalomas o Sierra Espolón: hierba cardenal, acérita salvaje y sangrerregia.',
        'Del ciento setenta al doscientos cinco, la Vega de Tuercespina o Arathi, con pálida, espina de oro y mostacho de Khadgar. Y Claros del Río es una alternativa nueva, llena de espina de oro.',
        'Del doscientos cinco al doscientos treinta, Tanaris o La Garganta de Fuego. Aprende el rango de artesano antes de ir, que allí no hay entrenador.',
        'Y al final, Tierras del Interior con solea y champiñón fantasma, y Frondavil, con hojasueño, salviargenta de montaña y flor de plaga, hasta el trescientos.',
        'Lo nuevo de Forever: en Monte Hyjal hay tres hierbas nuevas, la hojapesadilla, la salvia demoníaca y el loto de la muerte.',
        'El loto de la muerte no se ve en el mapa: sale de cualquier hierba de Hyjal, pero solo si llevas un encantamiento especial en los guantes.',
        'Y algo que nunca habíamos tenido: semillas. Al recoger salen semillas de cuatro rangos, que se plantan en un invernadero del campamento.',
        'Hay también un injertador de semillas. Volvió el diecinueve de noviembre, pero ahora puede fallar, y ya no acepta las semillas escasas.',
        'El primer objeto de campamento del herbolario es una vela de incienso, que da intelecto. Y el plano del invernadero lo suelta Shadetooth, en Los Humedales.',
    ]},
    {"id": 'p05', "post": 6.5, "frases": [
        'Parada cinco, la alquimia. Y aquí empieza el cambio más grande de todo el video.',
        'Del uno al cincuenta y cinco, una receta nueva de Forever, el elixir de fuerza menor, y después el elixir de defensa menor.',
        'Del cincuenta y cinco al ciento cincuenta, pociones de maná menores, elixires de entereza y de sabiduría, y aceite de fuego.',
        'Del ciento cincuenta al doscientos veinticinco, elixir de poder de fuego, pociones de maná y pociones de protección contra la naturaleza. Esa receta se compra en Feralas, en Tuercespina o en Tanaris.',
        'Del doscientos veinticinco al trescientos, más protección contra la naturaleza, transmutaciones de paso, aceite escama pétrea y elixir de defensa superior.',
        'En total, del uno al trescientos, más de seiscientas hierbas. Por eso tanta gente la combina con la herboristería.',
        'El rango de artesano lo enseñan Rogvar, en el Pantano de las Penas, para la Horda, y Kylanna, en Feralas, para la Alianza.',
        'Y hay un tercero para los dos bandos: Shurome, en el Santuario Esmeralda de Frondavil, enseña del uno al trescientos. Y por ahora te deja aprender el artesano sin pedirte doscientos.',
        'Ahora viene el cambio de verdad. En Forever, las pociones de sanación ya no son del alquimista. Se fueron a otra profesión, y te lo cuento al final del video.',
        'Lo que ganó a cambio son tintes: tinte cerúleo, magenta y verde esmeralda, que piden la sastrería y la peletería. El alquimista tiene clientes nuevos.',
        'Y veintiocho recetas de Favor, desde pociones de treinta segundos hasta el elixir del oso pardo, que pide trescientos y reputación honorable.',
        'En el campamento, el alquimista pone un pozo de maná, luego un fermentador, y al trescientos, un laboratorio de alquimia.',
        'Con el laboratorio, los frascos ya no se hacen solo dentro de Scholomance: se hacen junto a la hoguera. Su plano lo suelta allí Ras Levescarcha, el mismo jefe del frasco de poder supremo.',
    ]},
    {"id": 'burla1', "frases": [
        'Y otro comentario, porque nos lo merecemos. En el video del oro, un espectador, Crisis, nos escribió: el video dice tómatelo con calma, y el mismo video dice vende esto ya, ya, ya.',
        'Tiene toda la razón, Crisis, y te aviso que hoy va a ser peor. Con calma subes de nivel, pero una veta de torio libre no espera a nadie.',
        'Así que tómatelo con calma, eso sí, y luego corre a la veta antes de que llegue otro.',
    ]},
    {"id": 'p06', "post": 6.5, "frases": [
        'Parada número seis, el desuello, la recolección que va pegada a la peletería.',
        'La regla es sencilla: puedes desollar a un bicho si tienes cinco veces su nivel. Uno de nivel treinta pide ciento cincuenta.',
        'Y en Forever, los bichos de las zonas iniciales dan puntos hasta el setenta y cinco: jabalíes en Durotar, o lobos en el Bosque de Elwynn.',
        'Para el tramo del setenta y cinco al ciento cincuenta, la Horda va a Los Baldíos: raptores y zancudos al oeste de Fuerte del Norte. Y la Alianza, a Loch Modan y luego a Los Humedales.',
        'Del ciento cincuenta al doscientos veinticinco, la cueva de yetis de Laderas de Trabalomas: reaparecen tan rápido que te puedes quedar dentro. O los huargos del Bosque del Ocaso.',
        'Del doscientos veinticinco al doscientos ochenta, los yetis de la Vega Cicatriz Feral, en Feralas. Y el final, los diemetradones y pterrordáctilos de Un\'Goro.',
        'Y la Horda tiene un regalo: el cuchillo para desollar afilado, que suma tres puntos, de una misión en Los Baldíos.',
        'Lo nuevo de Forever: cada criatura se desuella una sola vez. Lo que otro jugador mata y no desuella, eso sí, es tuyo.',
        'Y hay materiales escasos nuevos: cuero prístino, pellejo prístino y escama prístina. En la beta, el cuero prístino pasaba de una de oro; en la primera semana bajó a unas cinco platas.',
        'Claros del Río también sirve: tiene bestias que dan mucho cuero pesado. Y en Monte Hyjal, cuero basto.',
        'En el campamento, el desollador pone una silla de campamento, que da crítico. Y al ciento cuarenta, una guía de campo con la que cualquiera aprende a rastrear bestias.',
        'El plano de la guía lo suelta Lady Anacondra, en las Cuevas de los Lamentos. Y al trescientos llega un banco de trabajo de trampero.',
    ]},
    {"id": 'p07', "post": 6.5, "frases": [
        'Parada siete. Peletería, y el objeto de campamento que más agradece quien sube de nivel.',
        'Del uno al sesenta, cuero ligero, pellejo ligero curtido y guantes de cuero repujado. Del sesenta al ciento treinta, pantalones, cinturones de cuero oscuro y pellejo medio curtido.',
        'El rango de experto lo enseñan Una en Cima del Trueno, Telonis en Darnassus, o Jarael en Shen\'dralas, la zona nueva que es casi de la Horda.',
        'Del ciento treinta al doscientos cinco, hombreras bárbaras, guantes de guardián y cintas.',
        'El artesano está fuera de las capitales: Hahrana Pielférrea, en Feralas, para la Horda, y Drakk Stonehand, en Tierras del Interior, para la Alianza.',
        'Del doscientos cinco al trescientos, unos quinientos cueros gruesos solo para el primer tramo, y luego cientos de cueros bastos y paño rúnico.',
        'Y hay un patrón nuevo con nombre de canción de Elvis: los zapatos de gamuza azul. Sirven para subir del doscientos treinta y cinco al doscientos sesenta y cinco.',
        'Hay también brazales y un sombrero de gamuza azul. El sombrero, eso sí, necesita una máquina de coser.',
        'Lo nuevo de Forever: ochenta y una recetas de Favor, conjuntos de cuero y de malla para cada papel del grupo. Y las especializaciones ya no dan resistencias.',
        'Muchas recetas piden un expositor de curtido. Blizzard lo bajó el seis de noviembre: ahora se aprende con ciento veinticinco.',
        'Y aquí está la joya: la tienda de campamento. Da experiencia de descanso, hasta el cinco por ciento de un nivel, una vez por hora.',
        'Por eso la peletería es de las profesiones que más ayudan a subir de nivel. Y por eso, en un campamento, el peletero siempre es bienvenido.',
        'La máquina de coser, al trescientos, la suelta Vectus, en Scholomance. Y ojo: solo se coloca con trescientos, aunque la compres hecha.',
    ]},
    {"id": 'p08', "post": 6.5, "frases": [
        'Parada ocho. Sastrería, la que no necesita recolección: la tela te cae de los enemigos.',
        'Del uno al cincuenta y cinco, madejas de lino y cinturones. Del cincuenta y cinco al ciento cuarenta, lana y seda: capas, capuchas y mochilas pequeñas.',
        'El rango de experto lo enseñan Josef Gregorian en Entrañas y Georgio Bolero en Ventormenta. La Alianza tiene además a Charles Worth en Dalaran, y en Shen\'dralas está Melanori.',
        'Del ciento cuarenta al doscientos, tejido mágico, y chalecos y pantalones de seda carmesí.',
        'El artesano: Daryl Stack, en el Molino Tarren de Laderas, para la Horda, y Timothy Worthington, en Theramore, para la Alianza. Compra el hilo rúnico antes de ir.',
        'Entre el doscientos y el doscientos veinticinco, diecisiete bolsas de tejido mágico rojas, que en Forever ya son de catorce casillas.',
        'Del doscientos cincuenta al doscientos ochenta, un patrón nuevo, los puños de paño rúnico. Lo vende Pexmit, en Monte Hyjal, por diez de oro, o la Horda lo saca con una misión.',
        'Del doscientos veinticinco al doscientos ochenta, calcula unos mil cuatrocientos paños rúnicos. La sastrería se paga en tela.',
        'Lo nuevo de Forever: las bolsas de componentes, para esa quinta ranura. De lino de seis casillas, de lana de ocho, y las grandes de doce y catorce, con Favor.',
        'Y la de lana pide tinte cerúleo, que hace el alquimista. Aquí se conecta la parada cinco con la parada ocho.',
        'Hay sesenta y siete recetas de Favor, conjuntos de tela para cada escuela de magia. Y en el campamento, el sastre pone un estandarte de su facción, que da espíritu.',
        'Al ciento cuarenta, una rueca, obligatoria para muchas recetas. Su plano lo suelta un centinela inestable, en la Ciudad de Dalaran.',
        'Y la trampa: las recetas que llevan del doscientos ochenta y cinco al trescientos piden un telar. Y el telar solo lo fabrica quien ya tiene trescientos.',
        'O encuentras un campamento donde otro sastre ya puso su telar, o subes esos últimos puntos por otro camino. El plano del telar es de la Baronesa Anastari, en Stratholme.',
    ]},
    {"id": 'p09', "post": 6.5, "frases": [
        'Parada nueve. Encantamiento, que desencanta todo lo que cose el sastre.',
        'Del uno al setenta, con un reactivo nuevo de vendedor, la mota de magia: una vara de cobre rúnica y encantamientos de brazal. Y desencantar también da puntos.',
        'Forever añadió recetas de nivel bajo, así que los primeros setenta puntos salen más baratos que antes. Hay hasta una varita de práctica de novato.',
        'Del setenta al ciento cincuenta, con polvo extraño o esencia mágica inferior: absorción menor, vara de plata rúnica y varitas.',
        'El rango de experto tiene un solo entrenador por bando, y está escondido. Hgarth, en un risco sobre el Refugio Roca del Sol, en Sierra Espolón.',
        'Y Kitta Vientofuego, en lo alto de la Torre de Azora, en el Bosque de Elwynn. La Alianza tiene además a Vanessa Sellers, en Dalaran.',
        'El artesano, para los dos bandos, solo lo enseña Annora, en Uldaman. Y aparece cuando limpias todo lo que hay a su alrededor.',
        'Del doscientos veinticinco al trescientos, guantes de agilidad, aceites de maná y de zahorí, y la vara rúnica de arcanita para cerrar.',
        'Lo nuevo de Forever: los collares por fin se encantan. Pero la fórmula no la enseña ningún entrenador: se compra con Favor, entre treinta y nueve recetas.',
        'También hay encantamientos de arma nuevos, reliquias, y bastones y orbes para lanzadores de hechizos.',
        'En el campamento, el encantador pone un laúd encantado. Y al ciento cuarenta, un recuperador arcano, que mejora lo que sacas al desencantar.',
        'El plano del recuperador lo suelta la Sombra del archimago, en la Ciudad de Dalaran. Y la forja arcana, al trescientos, sale de Nanaya, en el Bancal del Creador.',
        'Y un aviso para las bandas: la esencia maleable de la naturaleza solo se consigue desencantando. Sin un encantador en el grupo, ese material no existe.',
    ]},
    {"id": 'legado', "frases": [
        'Y con el encantamiento cerramos las seis profesiones de fabricación. Cada una te da un punto de Legado al llegar a ciento cincuenta, a doscientos veinticinco y a trescientos.',
        'Son dieciocho puntos en total. La recolección y las secundarias no dan ninguno, así que si tu personaje principal lleva dos de recolección, que un alternativo suba la fabricación.',
        'Y en el árbol de Legado de profesiones hay mejoras como horas extra, que sube la probabilidad de ganar puntos, o cosecha abundante, que da más materiales escasos.',
    ]},
    {"id": 'burla2', "frases": [
        'Y un último comentario, con cariño. En el video del oro, un espectador, SoyoyoS, nos escribió: este video está lleno de imprecisiones, basura, saludos.',
        'Fíjate qué educación: nos llamó basura, pero se despidió. En Azeroth, eso ya es nivel de embajador de Ventormenta.',
        'Y lo digo en serio: si ves una imprecisión, dinos el minuto y el dato, que las correcciones justas salen en el siguiente video. El saludo, te lo devolvemos.',
    ]},
    {"id": 'p10', "post": 6.5, "frases": [
        'Parada diez. Cocina, la primera de las tres secundarias. Y en Forever, la que enciende el campamento.',
        'Porque la cocina ya no empieza con una receta: empieza con una hoguera que llevas en la mochila. La hoguera básica se aprende con cocina uno y se hace con madera simple.',
        'Y aquí te explico el campamento, que hemos visto en cada parada. Alguien enciende la hoguera, y cada jugador alrededor pone un objeto de su profesión.',
        'Te sientas un minuto y recibes los beneficios del campamento durante una hora, con todo lo que aporten esos objetos.',
        'La hoguera básica admite tres objetos, la de oficial cinco, y la de experto diez. Y en la primera semana, los jugadores pusieron más de veintiocho millones de objetos de campamento.',
        'La ruta: del uno al cincuenta, pececitos luminosos o caballa. Del cincuenta al ciento cincuenta, pargo de lodo, atún blanco, y después el siluro mostacherizo.',
        'El experto es un libro: lo vende Wulan en Aldea Cazasombras, en Desolace, para la Horda, y Shandrina en el Lago Mystral, en Vallefresno, para la Alianza.',
        'Y el artesano es una misión en Gadgetzan: doce huevos gigantes, diez carnes de almeja sabrosa y veinte quesos curados de Alterac.',
        'Del doscientos veinticinco al trescientos, serviolas moteadas o branquirrojos, y la sopa de pargo nocturno para terminar.',
        'Lo nuevo de Forever: la comida cocinada da un cinco por ciento más de experiencia por muertes. Y hay seis recetas de Favor, todas batidos de espíritu.',
        'Y la receta más rara de todas: un plato de un pez nuevo, la descarrioaleta, que solo se pesca en Crestagrana. Y su descripción dice, literalmente, cómeme.',
        'La hoguera de oficial sale de Lord Serpentis, en las Cuevas de los Lamentos, y el festín de Cocinitas, del mismísimo Cocinitas, en Las Minas de la Muerte.',
        'Y Cocinitas suelta también una varilla de remover que te hace cocinar un veinticinco por ciento más rápido.',
    ]},
    {"id": 'p11', "post": 6.5, "frases": [
        'Parada número once, la pesca, que no ocupa hueco, y que hasta sin habilidad da cofres en mar abierto.',
        'Del uno al setenta y cinco, en cualquier zona inicial, con un adorno lustroso. Todos los entrenadores de inicio están junto al agua.',
        'Del setenta y cinco al ciento cincuenta, en las capitales o en Los Baldíos, Costa Oscura, Loch Modan o los Páramos de Poniente.',
        'El experto es un libro que vende el Viejo Heming, en Bahía del Botín. Con adornos brillantes, pescas en el Marjal Revolcafango.',
        'El artesano es la misión de Nat Pagle, en el Marjal: cuatro peces en cuatro costas. Tuercespina, Desolace, el Pantano de las Penas y el Río Verdantis, en Feralas.',
        'Y para cerrar, Frondavil, Feralas, Tierras del Interior, Tanaris o Un\'Goro, hasta el trescientos.',
        'Lo nuevo de Forever: el objeto de campamento del pescador es una pecera. Y da un ocho por ciento a todas las estadísticas, casi como una Bendición de reyes.',
        'Al ciento cuarenta, un expositor de pesca, que desde el dieciséis de noviembre da señuelos a todo el campamento. Su plano lo suelta Gelihast, en las Cavernas de Brazanegra.',
        'Y al trescientos, una cabaña de pesca, que suelta el profeta Jammal\'an, en el Templo Sumergido.',
        'Hay peces poco comunes y raros nuevos, con sus propios beneficios. Y el concurso de pesca de Tuercespina, desde el trece de noviembre, tiene muchos más ganadores.',
        'Y en la costa de Azshara hay más de trescientos cincuenta bancos de almejas de boca grande y de langostas pinza oscura. Para el pescador que ya llegó al final, ahí está la siguiente parada.',
    ]},
    {"id": 'p12', "post": 6.5, "frases": [
        'Parada número doce, los primeros auxilios: la profesión que casi todos dejan para el final, y la que más cambió en Forever.',
        'Porque aquí está la sorpresa de la parada cinco: las pociones de sanación ya no son del alquimista. Ahora son de primeros auxilios, y esa la puede subir cualquier personaje.',
        'Del uno al setenta y cinco, dos caminos: vendas de lino, u ochenta y seis pociones de sanación menores, con flor de paz, especias y viales.',
        'Del setenta y cinco al ciento cincuenta, vendas de lana, o un curativo nuevo, la cataplasma simple, y treinta y una pociones de sanación.',
        'El experto es un libro: lo vende Deneb Camino en Arathi para la Alianza, y Balai Lok\'Wein en el Marjal para la Horda.',
        'Del ciento cincuenta al doscientos veinticinco, vendas de seda y de tejido mágico.',
        'Y el artesano es la misión de atenciones médicas: el doctor Gregory Victor en Sentencia, en Arathi, o el doctor Gustaf VanHowzen, en Theramore.',
        'Salvas a quince heridos, los críticos primero, y la entregas en cuanto llegas a quince. No te quedes a ver qué pasa.',
        'Luego, vendas de tejido mágico y de paño rúnico. Y la alternativa nueva: del doscientos setenta y cinco al trescientos, pociones de sanación sublimes.',
        'El manual lo vende Pexmit, en Monte Hyjal, por ocho de oro, y no es fácil de encontrar. La Horda también lo consigue con una misión de Ortak Lomgok, en Flora Antigua.',
        'Además hay curativos nuevos: un torniquete de lana para los sangrados, y recetas contra las enfermedades.',
        'En el campamento, el sanador pone un equipo de primeros auxilios que da aguante. Luego un estudio de toxinas, y al trescientos, el laboratorio de médico de la peste.',
        'Piénsalo así: la profesión que no ocupa hueco, y que puede llevar cualquiera, ahora fabrica pociones de sanación sublimes.',
        'Si tu personaje no tiene alquimia, ya no tiene excusa. Las pociones para la banda las puedes hacer tú.',
    ]},
    {"id": 'combos', "frases": [
        'Y antes de despedirnos, la pregunta de siempre: qué dos profesiones llevo. No hay una respuesta única, pero sí parejas que tienen sentido en Forever.',
        'Minería con herrería o con ingeniería, porque el último tramo de herrería se come cientos de barras de torio, y las barras nuevas salen de la minería.',
        'Herboristería con alquimia, porque son más de seiscientas hierbas, y ahora el alquimista vende tintes a sastres y peleteros.',
        'Desuello con peletería, por el expositor de curtido y por esa tienda que da descanso a todo el campamento.',
        'Sastrería con encantamiento, porque ninguna pide recolección: lo que coses, lo desencantas. Y esa pareja te hace las bolsas de componentes.',
        'Y las tres secundarias, para todo el mundo: no ocupan hueco, una enciende el campamento, y otra ya hace tus pociones.',
    ]},
    {"id": 'cierre', "frases": [
        'Y esa es la ruta de profesiones del uno al trescientos en World of Warcraft Forever, parada por parada, de la mena que no se funde en ninguna forja a la poción que ya no es del alquimista.',
        'Ahora cuéntame en los comentarios qué dos profesiones llevas, y en qué número vas. Todos se leen, y muchos acaban en el siguiente video.',
        'Si este video te sirvió, suscríbete y compártelo con tu hermandad. Y si tu hermandad no tiene encantador, ya sabes a quién mandarle el video.',
        'Nos vemos en la próxima crónica. Y nos vemos en Azeroth.',
    ]},
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
# Música ORIGINAL de WoW (canal de videojuegos, regla del 23-oct): tramos (<= 175 s) se fijan tras `tiempo`; nota = tema (musica_wow.py)
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack, instrumental only, no vocals.",
    escenas={},
    tramos=[   # OST de WoW (musica_wow.py): nota = tema; cada tramo <= 175 s (timeline del 25-nov, 1878,75 s)
        (['intro', 'reglas'], 'Legends of Azeroth'),       # 0-140
        (['p01'], 'Dun Morogh'),                           # 140-275 minería (enanos, cobre, Forjaz)
        (['overgear'], 'Posada'),                          # 275-350 (suena la música de Overgear; entre minería y herrería, 25-nov)
        (['p02'], 'Roca Negra'),                           # 350-487,5 herrería (forja, Profundidades de Roca Negra)
        (['julsi', 'p03'], 'Tanaris'),                     # 487,5-622,5 ingeniería (Gadgetzan)
        (['burla0', 'gracias1'], 'Taberna orca'),          # 622,5-690
        (['p04'], 'Vallefresno'),                          # 690-795 herboristería
        (['p05'], 'Claro de la Luna'),                     # 795-912,5 alquimia (Frondavil, Santuario Esmeralda)
        (['burla1', 'p06'], 'Baldíos'),                    # 912,5-1047,5 desuello (Los Baldíos)
        (['p07'], 'Feralas'),                              # 1047,5-1160 peletería (Feralas)
        (['p08'], 'Ventormenta'),                          # 1160-1287,5 sastrería (Georgio Bolero)
        (['p09'], 'Elwynn'),                               # 1287,5-1400 encantamiento (Torre de Azora)
        (['legado', 'burla2'], 'Posada'),                  # 1400-1462,5
        (['p10'], 'Páramos'),                              # 1462,5-1580 cocina
        (['p11'], 'Tuercespina'),                          # 1580-1677,5 pesca (concurso de Tuercespina)
        (['p12'], 'Cuna del Invierno'),                    # 1677,5-1795 primeros auxilios (Monte Hyjal, Pexmit)
        (['combos', 'cierre'], 'Legends of Azeroth'),      # 1795-1878,75
    ],
    reemplazos={"overgear": dict(archivo=r"medios\_overgear\musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

# --- VOCES: todo Remy (Applio)
VOCES = {"Remy": "applio"}
LEMAS = {"Remy": "La voz de siempre"}
NARRA = {f"{_e['id']}_{_i}": "Remy" for _e in ESCENAS for _i in range(len(_e["frases"]))}
VOZ_POR_FRASE = {k: "applio" for k in NARRA}
