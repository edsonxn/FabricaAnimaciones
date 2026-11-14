# -*- coding: utf-8 -*-
"""GUION de «Los 20 EFECTOS MANDELA de Call of Duty que TÚ recordaste (parte 2)» (motor SECUENCIA YT, Expediente 141, 13-nov-2026).
Plantilla: videos/cod_mandela/ (misma fórmula; cambia UNA variable: muchos efectos los mandó la gente). Investigación: investigacion.md.
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo; nombres alemanes TAL CUAL (el usuario eligió la muestra A, 13-nov).
Queja de @v5x777cod_rdr_fan0 (voz «frustrada, forzada»): menos corchetes de emoción; solo [serious], [deadpan] y [short pause].
REGLA DE ORO: cada frase nombra algo que SE VE; si la voz nombra un sonido, se OYE («post» = la voz calla y suena el clip).
"""

TITULO = "Los 20 EFECTOS MANDELA de Call of Duty que TÚ recordaste (parte 2)"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "sigh", "annoy", "frustr"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
# ElevenLabs dice el inglés nativo; los mapas alemanes TAL CUAL (prueba A/B/C del 13-nov, ganó A)
FONETICA = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Call of Duty", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # OST oficial (audio/ost/_catalogo.txt), nunca Lyria

# Pausas con la voz callada («si la voz nombra un sonido, se oye»):
#   intro: Gaz «Remember, switching to your…» (cortado ANTES de «pistol») · p12 «The savages send dogs…» ·
#   p10 la cadena del retrete + arranque de «Lullaby of a Deadman» · p07 «Frank, soy yo, Mason» (doblaje latino) ·
#   p04 «Our generals will be pleased» (SDC) · p01 Gaz completo «…pistol is always faster than reloading»
# Comentarios (≤ 10 días): @brexxy7369 p03 · @Rafa-xe3pw p07 · @metal9208 p06 · @AndrésRíos-v8y p08 (contraburla) ·
#   @v5x777cod_rdr_fan0 p11 (contraburla de la voz) · @mr_brigthside21 y @lycanroc8806 en el cierre (agradecimiento)
ESCENAS = [
    {"id": "intro", "pre": 0.3, "post": 2.8, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: tu memoria. Otra vez.",
        "En el expediente anterior les pedí sus efectos Mandela. Y me llegaron estos: la AUG en la granja de Zombies, una frase de Alex Mason, y un Black Ops que salió en dos mil siete.",
        "Los revisé todos, con el juego en pantalla. Y uno de ustedes tiene razón. A medias.",
        "Pero antes, escucha al sargento Gaz, en el primer entrenamiento de Call of Duty 4.",
    ]},
    {"id": "intro_b", "frases": [
        "¿Cómo termina esa frase? Seguro que lo sabes. Medio internet también cree saberlo. [short pause] Te lo enseño en el número uno.",
        "Veinte efectos Mandela de Call of Duty, parte dos. Y esta vez, cuatro me los mandaste tú.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. La bomba que nunca desactivaste.",
        "Call of Duty 4, dos mil siete. Misión Shock and Awe: los marines entran en la capital de Al-Asad, y aparece una bomba nuclear en la ciudad.",
        "Mucha gente recuerda una misión para desactivarla a tiempo. No existe. El helicóptero despega, la bomba explota, y el sargento Jackson muere arrastrándose entre las ruinas.",
        "Lo que sí desactivas es otra cosa, al final del juego: en la penúltima misión, la del cuarto de control de los misiles, subes los códigos de aborto, y los misiles nucleares de Zakhaev se destruyen en el aire. [deadpan] Tu cabeza juntó las dos misiones, y salvó a Jackson.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, la mira de la Intervention.",
        "Modern Warfare 2, dos mil nueve. El francotirador de los montajes, de los quickscopes, de los vídeos con dubstep.",
        "En dos mil veintidós alguien publicó esta imagen: un semicírculo negro debajo de la mira. Y miles juraron que eso no estaba en el original.",
        "Siempre estuvo. Es la sombra del soporte de la mira, y aparece en cada partida de dos mil nueve. [deadpan] Miraste por ese visor miles de veces. Y nunca miraste el visor.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. El uniforme de Richtofen.",
        "Edward Richtofen, el doctor loco de los Zombies originales, el que habla con las voces de su cabeza.",
        "Mucha gente lo recuerda de uniforme verde militar. Pero en World at War y en Black Ops, su uniforme es caqui, tirando a marrón. Con su gorra de oficial y sus guantes.",
        "[short pause] Lo tuviste delante en cada partida. Y tu memoria lo pintó de otro color.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, el césped de Nuketown.",
        "Nuketown dos mil veinticinco, Black Ops 2: dos casas, un autobús, y maniquíes por todas partes.",
        "Casi todos lo recuerdan como un jardín de verdad. Pero junto a la casa amarilla el césped está enrollado, como una alfombra. Es césped artificial.",
        "En dos mil veinticinco ya no quedaba césped de verdad en el pueblo nuclear. [deadpan] Ni vecinos de verdad.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. Double Tap, segunda parte.",
        "En el expediente anterior te enseñé que en Origins no había máquina de Double Tap. Pues hay más.",
        "Ascension, Black Ops, dos mil diez: la base soviética de los cohetes y los monos espaciales. Muchos recuerdan Double Tap junto a Mule Kick.",
        "En el Ascension original no hay Double Tap. Ese mapa trajo dos perks nuevas: PhD Flopper y Stamin-Up. Double Tap solo llegó con la versión de Black Ops 3, y dentro de Der Wunderfizz.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, la montaña que nunca volvió.",
        "Downhill, Black Ops 2: una estación de esquí en los Alpes franceses, con góndolas que cruzan el mapa por el aire.",
        "Hay quien jura haberlo jugado remasterizado en un Call of Duty más nuevo. Downhill solo existe en Black Ops 2.",
        "Lo que tienes en la cabeza probablemente es Alpine, de Cold War: otra estación de esquí, con nieve y cabañas. [deadpan] Mismo frío. Otro mapa.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. La cámara del Pack-a-Punch.",
        "En el teatro de Kino der Toten, cuando mejoras un arma, en las teles del cuarto de proyección te ves a ti mismo, esperando junto a la máquina.",
        "Unos juran que esa cámara nunca existió. Otros juran que siempre estuvo. Y los dos tienen razón.",
        "La cámara está en el juego. Pero en pantalla dividida se apaga, y en la versión de iPhone ni siquiera existe. [short pause] Depende de con quién jugabas, y en qué pantalla.",
    ]},
    {"id": "p13", "frases": [
        "En el trece, devolver la granada.",
        "Call of Duty 2, dos mil cinco. Normandía, el norte de África, y granadas de palo alemanas cayendo a tus pies.",
        "Mucha gente recuerda agarrarlas y devolverlas. En Call of Duty 2, eso no se podía hacer. Solo te quedaba correr, o tirarte al suelo.",
        "Devolver la granada llegó después. [deadpan] Si alguna vez se la devolviste a un alemán en Call of Duty 2, fue en otro juego.",
    ]},
    {"id": "p12", "post": 3.5, "frases": [
        "Número doce. Los perros de World at War.",
        "Zombies no, multijugador. Cuando un rival consigue los perros, el anunciador japonés te avisa. Y muchos recuerdan que decía: los cobardes mandan perros. Escucha.",
    ]},
    {"id": "p12b", "frases": [
        "Los salvajes mandan perros a hacer su trabajo. [short pause] Ni cobardes, ni nada. Salvajes.",
    ]},
    {"id": "p11", "frases": [
        "En el once, el armario del primer mapa de los zombis.",
        "Nacht der Untoten, de World at War, dos mil ocho: un búnker, cuatro ventanas, y en el piso de arriba, un armario en la pared.",
        "Muchos recuerdan que de ese armario salía el PTRS-41, el antitanque que tumba a cualquier zombi. Del armario sale un Kar98k con mira, por mil quinientos puntos. El PTRS solo salía de la caja misteriosa.",
        "Y ya que hablamos de mapas alemanes: un espectador me escribió que digo Kino der Toten con acento francés, y que mi voz suena victimista y manipuladora.",
        "[deadpan] Lo de victimista, no lo sé. Lo de manipuladora, sí: te manipulé para que vieras este armario durante treinta segundos. Y te voy a manipular para que veas los otros diez. Merci.",
    ]},
    {"id": "p10", "post": 9.2, "frases": [
        "Número diez. La canción que no era de Kino.",
        "Lullaby of a Deadman. Mucha gente la recuerda sonando en Kino der Toten, al perder la partida.",
        "Pero esa canción es de Verrückt, el manicomio. Y para oírla había que hacer esto: tirar tres veces de la cadena del retrete, en el baño del lado alemán.",
    ]},
    {"id": "p10b", "frases": [
        "La canción de Kino es otra: Ciento quince. Lo de Lullaby en el teatro venía de los montajes de YouTube de dos mil diez.",
    ]},
    {"id": "p09", "frases": [
        "En el nueve, la Wunderwaffe.",
        "La Wunderwaffe DG-2, el arma de rayos de Der Riese. Un disparo, y la electricidad salta de zombi en zombi.",
        "La leyenda dice que con Pack-a-Punch mataba veinticuatro zombis de un tiro. Mata hasta diez. Con Pack-a-Punch o sin él: la mejora solo le da más munición.",
        "¿Y de dónde sale el veinticuatro? De dos sitios: la Wunderwaffe trae veinticuatro cargas de reserva. Y en los mapas de World at War, nunca hay más de veinticuatro zombis a la vez. [deadpan] El número era real. Lo pegaste en el sitio equivocado.",
    ]},
    {"id": "p08", "frases": [
        "Número ocho. Este me lo mandó Andrés.",
        "Me escribió que Black Ops salió en dos mil siete, y que tenía trece misiones. Andrés, gracias. Acabas de hacer un efecto Mandela en vivo, en los comentarios de un video de efectos Mandela.",
        "Black Ops salió el nueve de noviembre de dos mil diez. Y la campaña tiene quince misiones, de Operación cuarenta a Redención.",
        "En dos mil siete salió Call of Duty 4. Y lo mejor: la fecha está escrita en el propio juego. En la intro, junto al logo de Treyarch, se lee once, nueve, diez.",
        "[deadpan] El juego te dijo cuándo salió en el primer segundo. Y aun así lo mandaste tres años atrás.",
    ]},
    {"id": "p07", "post": 3.6, "frases": [
        "En el siete, el reencuentro de Mason y Woods.",
        "Black Ops 2, misión Victoria pírrica. Mason y Hudson abren un contenedor en Angola, y dentro está Frank Woods, amarrado y destrozado.",
        "Rafa recuerda que Mason le decía: Frank, soy yo, Mason, ¿me recuerdas? Escucha lo que dice de verdad.",
    ]},
    {"id": "p07b", "frases": [
        "Frank, soy yo, Mason. Y ya. Ni en el doblaje latino, ni en inglés, hay un me recuerdas.",
        "Lo que tu cabeza añadió tiene sentido: Woods llevaba años preso, y Mason no sabía si su amigo lo iba a reconocer. [short pause] Pero eso lo pensaste tú. El juego no lo dice.",
    ]},
    {"id": "p06", "frases": [
        "Número seis. La perk de Moon, otra vez.",
        "En el expediente anterior dije que en las plataformas de Moon nunca te regalaban una perk. Y metal me escribió que tenía dudas. Que recordaba a gente consiguiéndola.",
        "Tiene razón en algo. Encima de las plataformas del biodomo sí aparecen potenciadores, que cambian cada pocos segundos: doble puntos, carpintero, nuke, insta-kill. Y se agarran saltando.",
        "Y en dos mil once alguien subió este video: un destello verde, borroso, que según su amigo se convertía en una botella de perk.",
        "Ese recuerdo existe por una razón: en Shangri-La, el mapa anterior, si un mono roba un Max Ammo, el potenciador va cambiando. Y durante una fracción de segundo, se convierte en esto: una botella de perk.",
        "Así que no, en Moon no había perk gratis en las plataformas. Pero no lo soñaste: lo viste. [short pause] En otro mapa.",
    ]},
    {"id": "p05", "frases": [
        "En el cinco, el M1911 de Alcatraz.",
        "Mob of the Dead, Black Ops 2: la prisión de Alcatraz, cuatro gánsteres y Brutus, el guardia que te bloquea la caja y las máquinas.",
        "Mucha gente recuerda haber sacado el M1911 de la caja misteriosa. Y aquí está, girando dentro de la caja.",
        "Pero no se puede sacar. Sale en la ruleta, solo para verse. Hay jugadores que han gastado millones de puntos sin conseguirlo. [deadpan] Los que lo vieron, lo vieron de verdad. Los que lo sacaron, no.",
    ]},
    {"id": "p04", "post": 3.7, "frases": [
        "Número cuatro. El director Hoover.",
        "Black Ops 2, multijugador, el mapa Raid. Muchos recuerdan al anunciador del FBI diciendo al ganar: Buen trabajo, equipo. El director Hoover estará complacido.",
        "El FBI no tiene esa frase. La que existe es de otro bando: el SDC, el ejército chino. Escucha.",
    ]},
    {"id": "p04b", "frases": [
        "Nuestros generales estarán complacidos. Generales, no Hoover.",
        "Y hay otro detalle: J. Edgar Hoover murió en mil novecientos setenta y dos. El multijugador de Black Ops 2 pasa en dos mil veinticinco. [deadpan] Habría sido complacido desde la tumba.",
    ]},
    {"id": "subs", "frases": [
        "Un dato antes del podio. De cada cien personas que ven estos expedientes, ni una está suscrita al canal.",
        "Si llegaste hasta aquí, ya eres de la unidad. Suscríbete, y el siguiente expediente te llega a ti primero.",
    ]},
    {"id": "p03", "frases": [
        "Número tres. La AUG en la granja.",
        "Este me lo mandó brexxy: recuerda perfectamente la AUG en la Granja de Black Ops 2. Y sus hermanos también la recuerdan.",
        "La Granja, el mapa de Zombies con el granero, la casa y el tractor. Esta es la lista de la caja: pistolas, la MTAR, la Galil, la Ray Gun. La AUG no está. Y no está en ningún modo de Black Ops 2.",
        "¿Entonces de dónde sale? De Black Ops 1. Ahí la AUG salía de la caja en todos los mapas, con mira Swarovski. Y con Pack-a-Punch se convertía en la AUG-50M3, con escopeta debajo.",
        "Y en la Granja sí está la MTAR: un fusil compacto, con el cargador detrás del gatillo, que de lejos parece una AUG. [short pause] Tú y tus hermanos no están locos. Jugaron mucho Black Ops 1.",
    ]},
    {"id": "p02", "frases": [
        "En el dos, el ojo de Weaver.",
        "Black Ops, dos mil diez. Grigori Weaver, el agente ruso del parche en el ojo. En Baikonur, Kravchenko lo tiene en el suelo.",
        "Mucha gente recuerda que Kravchenko le apagó un puro en el ojo. Fue un cuchillo.",
        "Y el cigarro existe, pero en otro juego: World at War, dos mil ocho. La primera misión. Un oficial japonés interroga al soldado Pyle, le da una calada al cigarro, y se lo apaga en el ojo.",
        "Dos juegos de Treyarch, dos ojos, dos años de diferencia. [deadpan] Y tu memoria los fusionó en una sola tortura.",
    ]},
    {"id": "p01", "post": 4.7, "frases": [
        "Y el número uno. La frase de Gaz.",
        "Call of Duty 4, el campo de tiro, el primer minuto de la saga moderna. Medio internet la cita así: cambiar a tu sidearm siempre es más rápido que recargar. Escucha el final.",
    ]},
    {"id": "p01b", "frases": [
        "La palabra que dice Gaz es pistol, o sea, pistola. No dice sidearm, y tampoco dice arma secundaria. Dice pistola.",
        "Y no acaba ahí: Gaz sigue diciendo que el cuchillo es todavía más rápido, y te manda a acuchillar una sandía.",
        "[short pause] La primera lección de Call of Duty moderno. La oíste cien veces. Y la recuerdas con otra palabra.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. Veinte efectos Mandela, y cuatro me los dieron ustedes.",
        "Todos los comentarios se leen, y se toman en cuenta para el siguiente expediente. Como el de lycanroc, que todavía guarda la carta física de Pawn Takes Pawn. O el que dijo que los jugadores de Black Ops 2 cumplieron dieciocho años y encontraron chamba.",
        "Ahora te toca a ti: ¿qué recuerdas de Call of Duty que nadie más recuerda? Escríbelo. Si es bueno, sale en la parte tres.",
        "En el canal tienes la parte uno, y los treinta misterios más raros de la saga. Suscríbete. [short pause] Retírate, soldado.",
    ]},
]

# 13-nov: Whisper escribe distinto los nombres (Gas, Richthofen, khaki, The Abundafizz, PH de Flopper, Simel = «sin él»)
CER_MAX_POR_FRASE = {k: .06 for k in ("intro_3", "p18_0", "p18_2", "p16_3", "p09_1", "p09_2", "p07b_1", "p04_2", "p01_0",
                                       "p01b_0", "p01b_2", "p11_0", "p11_1")}   # p11: «zombies», «2008» en cifra
TAIL_MAX_POR_FRASE = {"p04_2": 1.0, "p01b_0": 1.0, "p09_1": 1.0, "p07b_1": 1.1}   # terminan bien («Escucha.», «pistola.», «zombi.»)
GAP_MAX_POR_FRASE = {"p07b_1": 1.0}
