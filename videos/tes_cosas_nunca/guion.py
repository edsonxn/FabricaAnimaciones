# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — «Las 20 cosas que NUNCA debes hacer en Skyrim» (27-oct-2026). Meta: ≥ 16 min (el usuario), 1 sola sesión.
Fórmula de `tes_misiones_nunca` (19 781 vistas en 5 días, el mejor de la Fábrica en el canal) cambiando UNA variable: ACCIONES
del jugador en vez de misiones; 20 puestos para pasar de 16 min. SECUENCIA YT, voz Chatterbox «Sarcastica», MG `nucleo/mg_tes.py`,
pegatinas, mapas con ruta, OST oficial de Skyrim (`armar_musica_ost.py`, pistas no usadas en cosas_inutiles ni armas_poderosas).
Datos verificados el 27-oct-2026 en UESP (en.uesp.net, wikitexto): Skyrim:Chicken, Crime, Horses, Followers, Traps, Unarmed
Combat, Fight! Fight!, Unrelenting Force, Protected NPCs, Skeleton Key, Darkness Returns, The Black Star, Azura's Star, Dragon,
Hired Thug, A Night To Remember, Lucan Valerius, Cicero, The Cure for Madness, Giant, Lycanthropy, Vampirism, Disease, Leveling,
Containers, Respawning, Houses. Nombres es-ES de elderscrolls.fandom.com/es. Lo dudoso se dice con cautela: la gallina (UESP
no da cifra ni dice «todo el pueblo»), el vampirismo cambia con Dawnguard, la cárcel solo quita PROGRESO (nunca niveles).
Comentarios reales en pantalla (regla 27-oct): @DavidSanchez-nz2cb (gancho), @federicoherrera2105 (corrige «jarl»),
@manuelulloa4748 (FUS ROH DA a Delphine, n.º 15).
"""

TITULO = "Las 20 cosas que NUNCA debes hacer en Skyrim"
ARCHIVO = "tes_cosas_nunca"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# "Skyrim": "Escairim" (el usuario, 23-oct-2026) · "jarl": "yarl" (lo corrigió @federicoherrera2105, 27-oct-2026).
FONETICA = {
    "The Elder Scrolls": "Di Élder Escróls", "Skyrim": "Escairim", "jarl": "yarl",
    "@DavidSanchez-nz2cb": "David Sánchez", "@federicoherrera2105": "Federico Herrera", "@manuelulloa4748": "Manuel Ulloa",
    "Fus Ro Dah": "Fus Ro Dá", "FUS ROH DA": "Fus Ro Dá", "Delphine": "Délfin", "Lydia": "Lídia", "Uthgerd": "Útguerd",
    "Dawnguard": "Dóngard", "Dragonborn": "Drágonborn", "Mercer Frey": "Mércer Fréi", "Brynjolf": "Bríniolf",
    "Aranea Ienith": "Aránea Iénith", "Nelacar": "Nélacar", "Malyn Varen": "Málin Báren", "Ilinalta": "Ilinálta",
    "Azura": "Azúra", "Miraak": "Miráak", "Apocrypha": "Apócrifa", "Sam Guevenne": "Sam Guevén", "Sanguine": "Sánguin",
    "Dibella": "Dibéla", "Markarth": "Márkarz", "Senna": "Séna", "Ennis": "Énis", "Gleda": "Gléda", "Ysolda": "Isólda",
    "Moira": "Móira", "Morvunskar": "Morbúnscar", "Lucano Valerio": "Lucáno Balério", "Lucien Lachance": "Lusién Lachánce",
    "M'aiq": "Maík", "Sanguinare Vampiris": "Sanguináre Bampíris", "Falion": "Fálion", "Morthal": "Mórzal",
    "Stendarr": "Esténdar", "Harkon": "Járkon", "Pelagia": "Pelágia",
}

# Transcripciones (se rellenan tras leer cada una en `seleccionar`)
CER_MAX_POR_FRASE = {"intro_3": 0.02, "p17_0": 0.02, "p17_5": 0.02, "p16_5": 0.03, "p14_3": 0.015, "p12_2": 0.04, "p8_1": 0.02, "p8_3": 0.035, "p8_6": 0.06, "p7_2": 0.07, "p6_6": 0.04, "p16_1": 0.025}   # nombres que Whisper escribe distinto (jarl, Boethiah, Aranea, Sanguine, Lucien…); p7_2 se come «Ejemplo.»
GAP_MAX_POR_FRASE = {"p14_2": 0.95, "p14_3": 0.8, "p15_4": 0.75}   # pausa dramática antes de «Tú.»
TAIL_MAX_POR_FRASE = {k: 0.57 for k in ("intro_0", "intro_2", "p18_3", "p15_4", "p13_5", "p12_6", "p9_6", "p3_3", "p3_6", "p1_7", "p14_1", "p7_5")}   # CER 0: acaban hablando

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen; el sonido del juego va en ambiente_por (regla 26-oct-2026)
    ambiente_por={**{f"scene-{n:03d}": .85 for n in (37, 61, 99)},     # Fus Ro Dah, alma de dragón, el gigante te lanza
                  **{f"scene-{n:03d}": .6 for n in (7, 12, 26, 31, 45, 62, 105, 108)}},  # gallina, trampas, pelea, fuego… (97, 98, 102 y 28 traían narrador: fuera)
    recorte_por={},
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),   # heredados de tes_*
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (armar_musica_ost.py), nunca Lyria

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En el video de las misiones que nunca debes hacer, @DavidSanchez-nz2cb nos dejó el comentario con más me gusta. Que la mayoría de esas misiones están bien sabrosas, y que el premio es hacerlas.",
        "Y tiene razón. Así que hoy no hay misiones. Hoy hay cosas que de verdad no debes hacer nunca.",
        "Cosas pequeñas. Un botón que pulsas sin pensar, un cofre cualquiera, una gallina. Y que te pueden costar la partida, la reputación, o cien horas de trabajo.",
        "Y antes de empezar. @federicoherrera2105 nos corrigió cómo se dice jarl. Tienes razón, apuntado.",
        "Así que aquí van las veinte cosas que NUNCA debes hacer en Skyrim, todas comprobadas, y con lo que te cuesta cada una.",
        "Y quédate hasta el final, porque el número uno lo has hecho casi seguro. Y probablemente hoy mismo.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. Atacar una gallina.",
        "Parece una broma, pero las gallinas de los pueblos tienen dueño. Y pegarle a una gallina con dueño es un crimen, con su recompensa y todo.",
        "En Cauce Boscoso, el primer pueblo que pisas, hay gallinas sueltas por todas partes. Y la gente del pueblo las aprecia más que a ti.",
        "Y aquí viene lo mejor. En el juego original, los animales de granja contaban como testigos. O sea, la propia gallina podía denunciarte.",
        "Ese error lo arregló un parche hecho por fans, no el oficial. Así que en muchas partidas la gallina sigue siendo la chivata del pueblo.",
        "Y si atacas a las gallinas de fuera de Villa Melosa, tu propia casa en Riften, Iona, tu guardia personal, te recibirá con la espada en la mano la próxima vez que entres.",
        "Cien horas de leyenda, Sangre de Dragón, asesino de dioses. Y una gallina te pone precio a la cabeza.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, robar un caballo.",
        "Ves un caballo atado delante de una cuadra, te subes, y ya está. Cincuenta monedas de recompensa.",
        "Y no una vez. Cincuenta cada vez que alguien te ve montarlo. Si te bajas y te vuelves a subir delante de un guardia, otras cincuenta.",
        "Los caballos, igual que las gallinas, cuentan como testigos. El caballo que robas te está viendo robarlo.",
        "Y tus seguidores tienen principios. Se niegan a montar en un caballo robado, y se quedan quietos esperando a que te des cuenta.",
        "El truco, si lo vas a hacer igual, es subirte agachado y sin que nadie te vea. Así no hay recompensa. Pero tus seguidores siguen sin subir.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. Decirle a tu seguidor que espere, y olvidarte de él.",
        "Le dices a Lydia que te espere en la entrada de una cueva, haces tus cosas, viajas rápido a la otra punta de Skyrim, y ya no te acuerdas de que existe.",
        "Pues a las setenta y dos horas aparece un mensaje. Tu seguidor se ha cansado de esperar.",
        "Y se vuelve andando a su casa, con todo lo que le diste. Tu mejor armadura, tus flechas de ébano, todo lo que le hiciste cargar.",
        "Y si por el camino se muere, no lo pierdes todo. Su cuerpo desaparece en unos días, y sus cosas acaban en un ataúd del Salón de los Muertos de su ciudad.",
        "Y un mensajero te trae una carta de herencia, con algo de oro. Es lo más parecido a un reproche que vas a recibir en Skyrim.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, dejar que tu seguidor vaya delante en una ruina.",
        "Las trampas de Skyrim no son solo para ti. Las placas de presión las puede pisar cualquiera. Tu seguidor, cualquier otro personaje, y a veces hasta las criaturas.",
        "Y se rearman. Así que tú las esquivas con cuidado, y detrás viene tu seguidor y las pisa todas, una por una.",
        "Troncos con pinchos, lanzas en la pared, rocas que caen del techo. Y te las comes tú, que ibas delante y no habías hecho nada.",
        "Y si la trampa que activaste tú le hace mucho daño, tu seguidor puede abandonarte, y atacarte.",
        "Lo mismo con el gas inflamable. Un seguidor con una antorcha o con hechizos de fuego, y la mazmorra entera explota. Y él te culpa a ti.",
        "Por eso existe la ventaja Pies ligeros. Pisas las placas y no pasa nada. Incluso transformado en hombre lobo.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. Sacar un arma en una pelea a puñetazos.",
        "En las posadas y en las calles hay gente que te reta a pelear a puñetazos. Uthgerd la Indómita, en Carrera Blanca, es la más famosa. La apuesta suele ser de cien monedas.",
        "Si ganas, recuperas tu apuesta y te llevas otras cien. Y algunos se vuelven tus amigos, o hasta tus seguidores.",
        "Pero cualquier daño que no sea un puñetazo o un golpe de escudo rompe la pelea. Y cuenta como agresión. Cuarenta monedas, y los guardias encima.",
        "Un hechizo, una daga, lo que sea. Curarte sí puedes. Pegar con otra cosa, no.",
        "Y aquí está la trampa que casi nadie ve. Si llevas puesta la Cota de ébano, la armadura de Boethiah, su aura envenena a tu rival. Y eso también cuenta como agresión.",
        "Y cuidado con los curiosos. Corren alrededor de la pelea, y si le das a uno sin querer, también es agresión.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, gritarle a la gente.",
        "El grito Fuerza implacable, el famoso Fus Ro Dah, es lo primero que aprendes como Sangre de Dragón. Y lo primero que quieres probar con alguien.",
        "Gritar en la ciudad, sin darle a nadie, solo te gana un aviso del guardia. Que dejes de gritar, que pones nerviosa a la gente.",
        "Pero si el grito golpea a un ciudadano, es agresión. Cuarenta monedas. Y si lo mata, es asesinato. Mil.",
        "Y aquí viene lo retorcido. Las muertes por caída no cuentan como asesinato. Si lo empujas por un barranco, solo pagas la agresión. El barranco hace el resto.",
        "Y el daño por la caída llega unos segundos tarde. El pobre se levanta, y justo entonces se muere solo.",
        "@manuelulloa4748 nos dejó su plan para cuando llegue a la cima del mundo. Mirar a Delphine y gritarle Fus Ro Dah. Te entendemos. Pero son cuarenta monedas.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. Lanzar bolas de fuego cerca de tu seguidor.",
        "Tus seguidores son personajes protegidos. Los enemigos los pueden tumbar, pero no matar. Se arrodillan, se recuperan, y vuelven a la pelea.",
        "Solo hay alguien en todo Skyrim que puede matar a tu seguidor. Tú.",
        "Y tus hechizos de área no distinguen. Una bola de fuego en un pasillo estrecho le da al draugr, y le da a Lydia.",
        "Los primeros golpes los perdona, con un aviso. Pero si le das más de tres veces, se vuelve hostil y va a por ti.",
        "Y no se puede arreglar hablando. Tienes que rendirte, o huir lejos, viajar a otra parte y esperar un día entero a que se le pase.",
        "Por eso los veteranos de Skyrim tienen la misma costumbre. Antes de lanzar una bola de fuego, mirar dónde está Lydia.",
    ]},
    {"id": "p13", "frases": [
        "En el trece, quedarte la Llave maestra.",
        "En el Gremio de Ladrones recuperas la Llave maestra, el artefacto de Nocturnal. Una ganzúa que no se rompe nunca.",
        "Y la misión te pide que la devuelvas. Y mucha gente no la devuelve, porque se puede tener para siempre si nunca acabas esa misión.",
        "Pero la llave no es lo que crees. No te da ninguna bonificación a forzar cerraduras. Y por un error, tu habilidad puede no subir mientras la usas.",
        "Y no abre las cerraduras que piden una llave, ni las puertas de puzle nórdicas. Aunque Mercer Frey sí podía. En sus manos hacía cosas que en las tuyas no hace.",
        "Y lo que pierdes al no devolverla sí es real. Las bendiciones de los Ruiseñores, y la misión siguiente del gremio. Todo congelado por una ganzúa.",
        "O sea, te quedas una ganzúa irrompible a cambio de dejar a medias la historia entera del Gremio de Ladrones.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Darle la estrella a quien no debes.",
        "En la Fosa de Ilinalta encuentras una Estrella de Azura rota. Y tienes dos personas a las que llevársela.",
        "Aranea Ienith, la sacerdotisa de Azura, en la capilla de la diosa. O Nelacar, un mago altmer que vive en la posada El hogar helado, en Hibernalia.",
        "En los dos casos entras dentro de la estrella a enfrentarte a Malyn Varen, el mago que la corrompió. Pero el premio es distinto.",
        "Con Aranea, la Estrella de Azura. Una gema de alma infinita, que no admite almas de personas. Y Aranea como seguidora.",
        "Con Nelacar, la Estrella Negra. Una gema de alma negra que nunca se gasta. Hecha justo para las almas de personas.",
        "Y aquí está la gracia. Por un error del juego original, la Estrella Negra admite cualquier alma, blanca o negra. Es mejor en todo. La diosa te premia con la peor versión.",
    ]},
    {"id": "p11", "frases": [
        "En el once, moverte justo cuando muere un dragón.",
        "Matas un dragón, su cuerpo arde, y su alma viaja hacia ti. Es el momento más épico del juego. Y el más delicado.",
        "Porque si en ese instante viajas rápido, te subes a un caballo, abres un cofre o le hablas a alguien, el alma se puede perder.",
        "Sin alma no hay grito nuevo. El dragón que te costó media hora, para nada.",
        "Y si tienes Dragonborn, hay otro peligro. Entre dos misiones de esa historia, Miraak puede aparecer y robarte el alma antes que tú.",
        "Y otro error más. Si lo rematas con un rayo y la ventaja Desintegrar, las cenizas se pueden hundir en el suelo. Te quedas el alma, pero pierdes los huesos y las escamas.",
        "Así que cuando muera el dragón, quieto. Ni caballo, ni cofres, ni conversaciones. Deja que el alma llegue.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. Robarle a alguien que tiene familia.",
        "En Skyrim, si robas o matas a alguien, no siempre vienen los guardias. A veces viene otra cosa.",
        "La víctima, o algún familiar, puede contratar matones a sueldo. Normalmente tres. Y te esperan en el camino.",
        "Y da igual que nadie te viera. Basta con que el robo haya pasado.",
        "Llevan encima un contrato con el nombre de quien pagó. Pero no le puedes reclamar nada. Solo saber quién te odia.",
        "Y por un error, a veces los contrata un niño. Un niño de Skyrim con dinero para tres matones.",
        "Y hay otro error todavía mejor. Si le robas el corazón a un Corazón de espinas de los renegados y lo matas, el propio muerto te puede mandar matones.",
    ]},
    {"id": "p9", "frases": [
        "En el nueve, ir a la cárcel.",
        "Cuando un guardia te para y no puedes pagar, o no quieres, la opción fácil es ir a la cárcel. Pasas la condena, sales limpio, y ya está.",
        "Pero la cárcel no es gratis. Cada condena te quita progreso en tus habilidades. Cuanto más larga, más habilidades afectadas.",
        "No pierdes los niveles que ya tienes. Pero esa barra que tenías casi llena de herrería, o de arquería, vuelve atrás.",
        "Y además te quitan todo lo robado que llevas encima, y lo guardan en un cofre de pruebas con una cerradura muy difícil.",
        "Y aunque lo recuperes, sigue marcado como robado. Y si te escapas, son otras cien monedas.",
        "Eso sí, si un día te encierran en Carrera Blanca, en la mazmorra hay una reja con una cerradura muy fácil que lleva a una alcantarilla sin guardias. La fuga más fácil del juego.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Aceptar un concurso de bebida de un desconocido.",
        "A partir del nivel catorce, en cualquier posada se te puede acercar un tal Sam Guevenne. Te reta a beber, y si ganas te regala un bastón.",
        "Él aguanta dos tragos. Al tercero ganas. Y ahí se acaba lo que recuerdas.",
        "Te despiertas en el Templo de Dibella de Markarth. Y la sacerdotisa, Senna, te obliga a limpiar lo que hiciste anoche.",
        "Luego descubres que le robaste una cabra a un granjero, Ennis, y se la vendiste a un gigante. Que compraste un anillo de boda a crédito, y que estás prometido.",
        "Prometido con Moira. Una bruja cuervo. Ysolda dice que os conocisteis bajo la luna llena, entre luciérnagas, como en un cuento.",
        "Y Sam Guevenne en realidad es Sanguine, el príncipe del libertinaje. La resaca más larga de Skyrim, y todo por aceptar una copa.",
    ]},
    {"id": "p7", "frases": [
        "En el siete, matar a un comerciante.",
        "En Skyrim hay personajes esenciales, que no mueren nunca. Pero la mayoría de los comerciantes no lo son. Y si mueren, mueren para siempre.",
        "Ejemplo. En Cauce Boscoso, el Comerciante de Cauce Boscoso es de Lucano Valerio. Si muere, su hermana Camila se queda la tienda.",
        "Pero si mueren los dos, la tienda se queda abandonada. Para siempre. Ni el jarl puede volver a abrirla.",
        "Y no hace falta que los mates tú. Un dragón que ataca el pueblo, una flecha perdida, una bola de fuego mal apuntada.",
        "Y no solo pierdes una tienda. Hay misiones que dependen de gente que no es esencial. Antes de un parche, si ciertos personajes estaban muertos, misiones enteras no empezaban.",
        "Así que en Skyrim, cada comerciante que muere es una tienda menos para vender todo lo que robas.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. Matar a Cicerón.",
        "En la Hermandad Oscura conoces a Cicerón, el bufón que cuida a la Madre Noche. Y en la misión El remedio de la locura te mandan a acabar con él.",
        "Y casi todo el mundo lo mata. Está loco, se ríe solo, y ha intentado matarte.",
        "Pero puedes perdonarle la vida. Y si lo haces, después del gran contrato de la Hermandad, vuelve. Como guardián de la Madre Noche, y como seguidor.",
        "Y la recompensa de esa misión, Sombra, el caballo, te la dan igual hagas lo que hagas. Matarlo no te da nada extra.",
        "Cuando vuelve, te dice que fuiste un tonto al perdonarle, que ahora vas a morir. Y después de un silencio incómodo, te dice que era broma.",
        "Y si invocas al espectro de Lucien Lachance, él mismo te dirá que matar a Cicerón no es lo que Sithis desea.",
    ]},
    {"id": "p5", "frases": [
        "En el cinco, enfadar a un gigante.",
        "Los gigantes de Skyrim no son hostiles. Cuidan sus mamuts, y te ignoran mientras no te acerques demasiado.",
        "Si te acercas, levanta el garrote y lo agita. Es un aviso. Si sigues, golpea el suelo con el pie. Y luego ataca.",
        "Un gigante es de nivel treinta y dos, no importa el tuyo. Tiene quinientos noventa y uno de salud, y puede matarte de un golpe aunque estés bloqueando.",
        "Y si ese golpe te mata, no caes al suelo. Sales volando por los aires, altísimo. Los jugadores lo llaman el programa espacial de Skyrim.",
        "Y si le atacas a los mamuts, el gigante también va a por ti. Y los mamuts son de nivel treinta y ocho.",
        "Y un último aviso. Si le das a tu seguidor el garrote de un gigante, se lo equipa, y ya no hay forma de quitárselo. Solo lo arregla un parche hecho por fans.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Transformarte en hombre lobo delante de testigos.",
        "Si te unes a los Compañeros, en Carrera Blanca, acabas con la sangre de bestia. Y puedes transformarte cuando quieras.",
        "Pero si alguien te ve transformarte, aunque sea un granjero perdido en el campo, son mil monedas de recompensa. De golpe.",
        "Y no hace falta que ataques a nadie. Basta con que te vean. Y volver a forma humana delante de alguien también cuenta.",
        "La recompensa va a la comarca donde te ven. Y el guardia que lo presencia se vuelve hostil al instante.",
        "Lo mismo pasa con el Señor de los vampiros de Dawnguard. Te transformas a la vista de alguien, y mil monedas.",
        "Eso sí, hay alguien que no te atacará nunca, te transformes en lo que te transformes. M'aiq el Mentiroso.",
    ]},
    {"id": "p3", "frases": [
        "En el tres, ignorar una enfermedad.",
        "Peleas contra un vampiro, te lanza su hechizo, y en tu lista de efectos aparece una enfermedad con un nombre raro. Sanguinare Vampiris.",
        "Cada vez que un vampiro te lanza su absorción vampírica, hay un diez por ciento de que te contagie. Y de entrada solo te quita veinticinco puntos de salud. Parece nada.",
        "Pero si en tres días no te curas, te conviertes en vampiro. El juego solo te avisa con dos mensajes. Al amanecer te sientes débil. Y al anochecer, una sed extraña.",
        "Antes de esos tres días, se cura con una poción de curar enfermedad, rezando en un santuario, o comiéndote una pluma de halcón. Una sola.",
        "Después ya no. Para curarte tienes que ir a Morthal, con un mago llamado Falion, y hacer su ritual. O hacerte hombre lobo.",
        "Y la vida de vampiro tiene su precio. Al sol, en la peor etapa, pierdes sesenta de salud, magia y aguante. Y no regeneras nada. En el juego base, además, la gente te ataca nada más verte.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Subir de nivel sin pelear.",
        "Todos lo hemos hecho. Comprar hierro y cuero, y forjar cientos de dagas de hierro para subir herrería. O pasarte horas encantando y haciendo pociones.",
        "Cada habilidad que sube te da experiencia de personaje. Y sin darte cuenta pasas del nivel veinte al cuarenta sin haber blandido una espada.",
        "El problema es que el mundo sube contigo. Los enemigos y los dragones escalan con tu nivel. Y tu espada sigue siendo la de nivel veinte.",
        "Los dragones de escarcha aparecen a partir del nivel veintisiete. Y en el setenta y ocho, los dragones legendarios.",
        "La propia wiki más completa de la saga lo avisa. Subir demasiado sin combate rompe el juego. Los enemigos se vuelven demasiado duros para ti.",
        "Mucho personaje de nivel cincuenta, que muere contra un bandido porque nunca subió a una mano. Todo por cien dagas de hierro.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. Lo que casi seguro has hecho hoy mismo.",
        "Guardar tus cosas en cualquier cofre.",
        "Vacías la mochila en un barril de la posada, en el cofre de una cueva, o en un saco que tienes a mano. Y sigues tu camino tan tranquilo.",
        "Pero en Skyrim casi todos los contenedores se reinician. Pasados diez días, el cofre vuelve a su estado original. Y lo que dejaste dentro desaparece. Para siempre.",
        "En una mazmorra que ya despejaste, son treinta días. Y los cofres de los comerciantes, cada dos.",
        "Los únicos contenedores seguros son los de dentro de tus casas, y unos pocos marcados como que nunca se reinician. Y ni siquiera todo lo de tus casas. Lo de fuera de la casa, sí se reinicia.",
        "Y las estanterías de libros tienen un error. Si les metes demasiados, pierdes todos los libros.",
        "Y lo más gracioso es que el juego te lo dice. En una pantalla de carga, avisa de que lo que guardes fuera de casa puede no estar ahí después. Pero quién lee las pantallas de carga.",
        "Por eso es el número uno. Todo lo demás de esta lista te cuesta monedas, un seguidor o una noche de resaca. Este te puede costar cien horas de botín de golpe.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Veinte cosas que nunca debes hacer en Skyrim, de una gallina chivata a un cofre que se lo traga todo.",
        "Y ahora te toca a ti. ¿Cuál de estas has hecho? Y sé sincero con lo de Lydia y la bola de fuego.",
        "Si quieres ver lo contrario, cosas que sí debes hacer aunque parezcan una tontería, en el canal tienes los ocho exploits más ROTOS de Skyrim.",
        "Y la próxima vez que dejes algo en un barril, piénsalo dos veces.",
    ]},
]
