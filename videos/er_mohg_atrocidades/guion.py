# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Mohg QUE IGNORASTE» (10-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md. El usuario pidió 23 MIN (10-nov-2026) y
PEDIR LA SUSCRIPCIÓN ANTES DEL MINUTO 5 (además del tramo de campaña hacia el 75 %: las reglas suman).
Tema pedido en los comentarios: @zoharysakiyamablue471 ♥5 (9-nov, «mi patrón: MOHG… NIHIL, NIHIL, NIHIL») y @JustinRivera-c9l ×2.
Cada puesto va partido en escenas (pN / pNb / pNc), como Morgott y Radahn.
Investigación: investigacion.md (wikitexto de eldenring.fandom.com en inglés, japonés y español, 10-nov-2026).
NO REPITE lo de Miquella (el encanto a fondo, el cadáver como recipiente) ni lo de Radahn: aquí el encanto sale en una frase.
Mohg «Móg» SIEMPRE ANTE VOCAL o coma (ante consonante sale «mock»). Sonidos nombrados = tramo audible con `post` (medidos con Whisper el 10-nov: PISTAS voz=True, sfx/s_*.mp3)
(regla del 31-oct-2026): p5 «maidenless» (Varré), p4b el grito y la risa de Varré, p2 «Welcome, honoured guest», p1 «Nihil!»,
p1b «Mohgwyn!».
"""

TITULO = "Las 5 peores atrocidades de Mohg QUE IGNORASTE"
ARCHIVO = "er_mohg_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# «Mikéla» (no «Mikuéla» = la burla «Micuela»); Mohg «Móg» ante vocal; Mohgwyn «Mógüin».
FONETICA = {
    "Miquella": "Mikéla", "Malenia": "Malénia", "Radahn": "Rádan", "Radagon": "Rádagon", "Godfrey": "Gódfri",
    "Mohgwyn": "Mógüin", "Mohg": "Móg", "Morgott": "Mórgot", "Leyndell": "Léindel", "Rennala": "Renála",
    "Ranni": "Ráni", "Godrick": "Gódrik", "Godwyn": "Gódwin", "Rykard": "Ráikard", "Gideon": "Guídeon",
    "Elden Ring": "Élden Ring", "Elden": "Élden", "Melina": "Melína", "Liurnia": "Liúrnia", "Nihil": "Níjil",
    "maidenless": "méidenles", "Nerijus": "Neríyus", "Okina": "Okína", "Hyetta": "Yéta", "Irina": "Irína",
    "Zohary": "Zójari", "Isaac": "Ísak", "Eternalack": "Eternálak", "Maliketh": "Málikez", "Ansbach": "Ánsbaj",
    "Varré": "Varré", "Esgar": "Esgár", "Vyke": "Váik", "Yura": "Yúra", "Eleonora": "Eleonóra",
}

CER_MAX_POR_FRASE = {'intro_0': 0.058, 'intro_1': 0.021, 'intro_2': 0.009, 'intro_3': 0.012, 'intro_4': 0.008, 'intro_5': 0.002, 'intro_6': 0.002, 'p5_1': 0.008, 'p5_2': 0.002, 'p5b_0': 0.008, 'p5b_1': 0.002, 'p5b_2': 0.002, 'p5b_4': 0.002, 'p5b_5': 0.002, 'p5b_6': 0.011, 'p5b_8': 0.018, 'p5b_10': 0.002, 'p5b_11': 0.027, 'p5b_12': 0.002, 'p5b_13': 0.002, 'p5b_14': 0.002, 'p4_1': 0.008, 'p4_2': 0.002, 'p4_4': 0.002, 'p4_5': 0.002, 'p4_6': 0.007, 'p4_7': 0.002, 'p4_8': 0.031, 'p4_9': 0.002, 'p4b_1': 0.002, 'p4c_0': 0.008, 'p4c_2': 0.024, 'p4c_3': 0.015, 'p4c_4': 0.025, 'p4c_5': 0.019, 'p4c_6': 0.012, 'p3_0': 0.028, 'p3_3': 0.01, 'p3_4': 0.002, 'p3_5': 0.002, 'p3_6': 0.002, 'p3_7': 0.007, 'p3b_0': 0.008, 'p3b_1': 0.002, 'p3b_3': 0.021, 'p3b_4': 0.002, 'p3b_5': 0.002, 'p3b_6': 0.01, 'p3b_7': 0.002, 'p3b_8': 0.002, 'p3b_9': 0.011, 'p2_0': 0.002, 'p2_1': 0.009, 'p2_3': 0.009, 'p2_4': 0.016, 'p2_5': 0.014, 'p2_6': 0.002, 'p2_7': 0.009, 'p2_8': 0.002, 'p2b_0': 0.006, 'p2b_1': 0.002, 'p2b_3': 0.009, 'p2b_4': 0.006, 'p2b_5': 0.017, 'p2b_6': 0.002, 'p1_1': 0.007, 'p1_2': 0.006, 'p1_5': 0.008, 'p1_6': 0.008, 'p1_7': 0.002, 'p1_8': 0.02, 'p1b_1': 0.002, 'p1b_2': 0.002, 'p1b_3': 0.002, 'p1b_4': 0.002, 'p1b_5': 0.002, 'p1b_6': 0.009, 'p1b_7': 0.002, 'p1b_8': 0.008, 'p1b_9': 0.002, 'p1b_10': 0.002, 'cierre_0': 0.007, 'cierre_1': 0.002, 'cierre_2': 0.03, 'cierre_4': 0.002, 'cierre_5': 0.042, 'cierre_6': 0.046, 'cierre_7': 0.022}
GAP_MAX_POR_FRASE = {'intro_0': 0.52, 'intro_1': 0.54, 'intro_2': 0.44, 'intro_3': 0.73, 'intro_4': 0.5, 'intro_5': 0.44, 'intro_6': 0.77, 'p5_1': 0.5, 'p5_2': 0.27, 'p5b_0': 0.37, 'p5b_1': 0.49, 'p5b_2': 0.57, 'p5b_4': 0.52, 'p5b_5': 0.35, 'p5b_6': 0.75, 'p5b_8': 0.55, 'p5b_10': 0.29, 'p5b_11': 0.75, 'p5b_12': 0.55, 'p5b_13': 0.64, 'p5b_14': 0.51, 'p4_1': 0.49, 'p4_2': 0.7, 'p4_4': 0.8, 'p4_5': 0.51, 'p4_6': 0.55, 'p4_7': 0.56, 'p4_8': 0.52, 'p4_9': 0.66, 'p4b_1': 0.67, 'p4c_0': 0.45, 'p4c_2': 0.56, 'p4c_3': 0.72, 'p4c_4': 0.5, 'p4c_5': 0.65, 'p4c_6': 0.84, 'p3_0': 0.45, 'p3_3': 0.61, 'p3_4': 0.78, 'p3_5': 0.73, 'p3_6': 0.56, 'p3_7': 0.6, 'p3b_0': 1.51, 'p3b_1': 0.72, 'p3b_3': 0.41, 'p3b_4': 0.62, 'p3b_5': 0.7, 'p3b_6': 0.7, 'p3b_7': 0.41, 'p3b_8': 0.59, 'p3b_9': 0.53, 'p2_0': 1.08, 'p2_1': 0.67, 'p2_3': 0.48, 'p2_4': 0.64, 'p2_5': 0.55, 'p2_6': 0.56, 'p2_7': 0.59, 'p2_8': 0.46, 'p2b_0': 0.77, 'p2b_1': 0.41, 'p2b_3': 0.53, 'p2b_4': 0.5, 'p2b_5': 0.53, 'p2b_6': 0.63, 'p1_1': 0.55, 'p1_2': 0.81, 'p1_5': 0.5, 'p1_6': 0.8, 'p1_7': 0.59, 'p1_8': 0.75, 'p1b_1': 0.63, 'p1b_2': 0.72, 'p1b_3': 0.57, 'p1b_4': 0.46, 'p1b_5': 0.7, 'p1b_6': 0.71, 'p1b_7': 0.48, 'p1b_8': 0.76, 'p1b_9': 0.71, 'p1b_10': 0.41, 'cierre_0': 0.46, 'cierre_1': 0.65, 'cierre_2': 0.67, 'cierre_4': 0.75, 'cierre_5': 0.69, 'cierre_6': 0.49, 'cierre_7': 0.31}
TAIL_MAX_POR_FRASE = {'intro_0': 0.71, 'intro_1': 0.3, 'intro_2': 0.47, 'intro_3': 0.7, 'intro_4': 0.49, 'intro_5': 0.48, 'intro_6': 0.31, 'p5_1': 0.47, 'p5_2': 0.52, 'p5b_0': 0.49, 'p5b_1': 0.4, 'p5b_2': 0.53, 'p5b_4': 1.02, 'p5b_5': 0.68, 'p5b_6': 0.42, 'p5b_8': 0.79, 'p5b_10': 0.82, 'p5b_11': 0.58, 'p5b_12': 0.85, 'p5b_13': 0.8, 'p5b_14': 0.49, 'p4_1': 0.98, 'p4_2': 0.3, 'p4_4': 0.49, 'p4_5': 0.57, 'p4_6': 0.62, 'p4_7': 0.83, 'p4_8': 0.02, 'p4_9': 0.58, 'p4b_1': 0.52, 'p4c_0': 0.45, 'p4c_2': 0.2, 'p4c_3': 0.52, 'p4c_4': 0.62, 'p4c_5': 0.77, 'p4c_6': 0.6, 'p3_0': 0.02, 'p3_3': 0.4, 'p3_4': 0.35, 'p3_5': 0.5, 'p3_6': 0.42, 'p3_7': 0.65, 'p3b_0': 0.62, 'p3b_1': 0.38, 'p3b_3': 0.44, 'p3b_4': 0.63, 'p3b_5': 0.51, 'p3b_6': 0.36, 'p3b_7': 0.47, 'p3b_8': 0.53, 'p3b_9': 0.84, 'p2_0': 0.02, 'p2_1': 0.59, 'p2_3': 0.45, 'p2_4': 0.42, 'p2_5': 0.83, 'p2_6': 0.39, 'p2_7': 0.71, 'p2_8': 0.58, 'p2b_0': 0.79, 'p2b_1': 0.4, 'p2b_3': 0.44, 'p2b_4': 0.92, 'p2b_5': 0.77, 'p2b_6': 0.56, 'p1_1': 0.46, 'p1_2': 0.67, 'p1_5': 0.47, 'p1_6': 0.53, 'p1_7': 0.65, 'p1_8': 0.22, 'p1b_1': 0.51, 'p1b_2': 0.13, 'p1b_3': 0.46, 'p1b_4': 0.44, 'p1b_5': 0.35, 'p1b_6': 0.47, 'p1b_7': 0.5, 'p1b_8': 0.53, 'p1b_9': 0.58, 'p1b_10': 0.41, 'cierre_0': 0.71, 'cierre_1': 0.59, 'cierre_2': 0.58, 'cierre_4': 0.68, 'cierre_5': 0.55, 'cierre_6': 0.27, 'cierre_7': 0.74}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; el audio del juego va donde conviene oírlo (regla del 26-oct-2026)
    ambiente_por={},
    recorte_por={"scene-098": .09},   # [SHIRRAKO] marca de agua abajo a la derecha
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar"]),   # heredado de Morgott
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En el video de Morgott, Zohary nos dejó este comentario: me gustaría que hicieras un video de las atrocidades de mi patrón. Mohg, el Señor de la Sangre. Y lo firmó como lo firmaría el propio Mohg, en su pelea: Nihil, Nihil, Nihil.",
        "Ese mismo día, Justin nos lo pidió dos veces. Así que aquí lo tienes, Zohary. Tu patrón, con palacio, tridente y lago de sangre incluidos.",
        "Mohg es, seguramente, el villano más fácil de Elden Ring. El gemelo de Morgott, con cuernos, alas negras y un pantano rojo en el sótano del mundo. Nadie necesita un video para saber que es malo.",
        "Y además, desde la expansión, tiene excusa. En el video de Miquella vimos que lo tenían encantado. Que el secuestro no fue del todo idea suya, y que su cuerpo acabó siendo el recipiente de Radahn. Media comunidad pasó de odiarlo a tenerle pena.",
        "Pero un encantamiento explica un secuestro. No explica lo demás. No explica a quién recluta, qué les pide, qué les hace, ni con quién habló allá abajo, mucho antes de que Miquella apareciera en su vida.",
        "Así que van las cinco peores atrocidades de Mohg, el Señor de la Sangre, que ignoraste. Y aviso: la número uno no es el secuestro. Tiene que ver contigo. Y es muy probable que ya la hayas hecho.",
        "Ponte cómodo. Y si alguna vez jugaste con sangrado, guárdate esta frase para el final: la madre de la verdad desea una herida.",
    ]},
    {"id": "p5", "post": 6.0, "frases": [
        "Número cinco. Te convierte en cazador de los tuyos.",
        "Sales de la cueva del principio, das tres pasos por Necrolimbo, y el primer personaje que te habla es un tipo vestido de blanco, con una máscara que apenas sonríe. Varré, el Rostro Alabastrado.",
        "Y su saludo se volvió meme. Por desgracia para ti, no tienes doncella. Sin guía, sin la fuerza de las runas y sin invitación a la Mesa Redonda. Tu destino, al parecer, es morir en el anonimato. Así suena en inglés.",
    ]},
    {"id": "p5b", "frases": [
        "Durante horas parece un pesado útil. Te manda al Castillo de Velo Tormentoso, a por Godrick y su Gran Runa. Te felicita cuando ganas. Hasta te deja un mensaje en el suelo para regalarte el gesto de bravo.",
        "Hasta que lo encuentras en Liurnia, en la puerta de la Iglesia de la Rosa, y te pregunta qué te parecieron los Dos Dedos, los dioses que guían a los Sinluz.",
        "Si le dices que te parecieron extraños, se quita la careta aunque siga con la máscara puesta. Las palabras de los Dos Dedos no son de fiar. Desvaríos seniles. Y lo peor de todo: los Dedos no sienten ningún amor por los nuestros.",
        "Y te hace un regalo. Cinco Dedos Sangrientos Infestados. Un objeto para invadir el mundo de otros Sinluz. Y matarlos.",
        "Y no te deja pensarlo mucho. No hay razón para dudar, te dice. Los Sinluz fueron despreciados por la gracia, abandonados por los Dos Dedos. ¿Y ahora te piden que arregles su mundo en ruinas?",
        "El encargo es invadir tres veces. A jugadores de verdad, o al pobre Magnus, la Garra de la Bestia, que espera en las Ruinas de Sanguifuria, en el altiplano, rodeado de criaturas infectadas de sangre maldita.",
        "Cuando vuelves, Varré está encantado. Me alegra que disfrutes de mi regalo. Lo supe desde el principio. Tienes gusto por la sangre noble.",
        "Ese es el primer oficio de la dinastía de Mohg, el Señor de la Sangre: Sinluz cazando Sinluz. Los Dedos Sangrientos.",
        "Y antes de seguir, una cosa. Varré tarda media partida en pedirte que te unas. Nosotros te lo pedimos ya, y sin dedos infestados: si llegaste por Mohg y te está gustando, suscríbete. Ya pasamos los seiscientos cincuenta, y la meta es mil.",
        "Y si ya estás suscrito, gracias. De verdad. Tú eres de la Mesa Redonda buena.",
        "Volvamos a los Dedos. Yura, el cazador que te echa una mano en Necrolimbo, los describe sin rodeos: Sinluz esclavizados por la sangre. Fanáticos que acechan a los suyos. Su locura impide cualquier parentesco. Que tus emociones no detengan tu espada.",
        "Y Yura sabe de qué habla. El primero que te sale en Necrolimbo, Nerijus, el de las dos dagas, bajo el puente donde patrulla la Caballería nocturna, es un Dedo Sangriento al que Yura conocía por su nombre.",
        "La que de verdad persigue Yura es Eleonora, la Dedo Sangriento Violeta. La más letal de todos. Una espadachina tan buena que su ataque se comparaba con un torbellino. Y ahora, dice su arma, su leyenda está manchada de sangre maldita.",
        "Hasta la espada favorita de media comunidad sale de aquí. Ríos de Sangre, la katana de Okina. Su descripción cuenta que, cuando Mohg, el Señor de la Sangre, sintió en su propia carne la espada y la locura de Okina, le hizo una propuesta: una vida de demonio. Una sed que nunca se sacia.",
        "Mohg, el Señor de la Sangre, no recluta soldados. Recluta asesinos de su propia gente. Y el primero al que le ofrece el trabajo, desde el primer paso del juego, eres tú.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Te pide la sangre de una doncella.",
        "Varré quiere algo más que un invasor. Quiero ungirte como caballero, te dice. Un caballero al servicio del Corifeo Mohg, el Señor de la Sangre, para fundar una nueva dinastía. El Corifeo tiene fuerza, visión y, por supuesto, amor.",
        "Si le dices que no, no se enfada. Solo comenta que a lo mejor lo oíste mal, y que te dará un día o dos para que se te destapen los oídos.",
        "Si le dices que sí, te entrega un paño de juramento blanco, el Favor del Señor de la Sangre. Y la prueba final: empapa el paño con la sangre de una doncella.",
        "Y lo explica con toda la calma del mundo. Normalmente, este ritual implicaría matar a tu propia doncella y renegar de la sabiduría de los Dos Dedos. Pero como no tienes doncella, sirve la sangre de la doncella de cualquiera.",
        "Normalmente. O sea, que para entrar en la orden, los caballeros de Mohg, uno a uno, mataban a la doncella que los guiaba. A la persona que se suponía que iba a acompañarlos hasta el Círculo de Elden.",
        "Y tú, como Sinluz sin doncella, sales a buscar una. El juego te da tres caminos. El cadáver de tu propia doncella, en la Capilla de la Espera, el sitio donde empieza el juego. O la doncella de Vyke, muerta en la Iglesia de la Inhibición.",
        "O el tercero. Matar a Irina, la chica ciega del Puente del Sacrificio, en la Península Llorosa. La que solo te pide que le lleves una carta a su padre. Y si Irina ya murió, sirve Hyetta, otra chica ciega que encuentras por el camino.",
        "Para Varré, da igual cuál. Mientras sangre.",
        "Cuando vuelves, el paño cambia de descripción. Paño de juramento completamente enrojecido, teñido con la sangre de una doncella. La prueba final ha terminado. El Corifeo Mohg, sin duda, te recibirá a su servicio, como un caballero que pondrá los cimientos de su dinastía.",
    ]},
    {"id": "p4b", "post": 6.0, "frases": [
        "Y entonces llega la ceremonia. Varré te pide el dedo. Esta sangre noble será una insignia de honor inmutable, en cuanto se asiente. Dentro de ti.",
        "Te la mete en el cuerpo, y se ríe del dolor. Ay, cielos. Aprieta los dientes, o algo. Nunca olvides esa sensación de agonía. Porque es lo que te une al Corifeo Mohg, a todos nosotros.",
        "Y remata con una frase que da escalofríos. Tienes el grito más dulce, mi corderito. Escúchalo de su boca.",
    ]},
    {"id": "p4c", "frases": [
        "Luego te da la Medalla de caballero de sangre pura. Prueba de que eres un glorioso caballero de la nueva Dinastía Mohgwyn. Úsala para tener audiencia con Mohg, el Señor de la Sangre. Solo que aún no es el momento.",
        "Porque Mohg aún duerme junto a la Divinidad. Ten paciencia. La nueva dinastía está cerca.",
        "Paciencia. Esa es la paga de los caballeros de Mohg, el Señor de la Sangre. Y Varré lleva mucho tiempo cobrándola.",
        "Al final, en el palacio, eres tú quien lo invade a él. Y cuando cae, se arrastra y le reza a su señor. Oh, Corifeo Mohg, por favor, concédeme la fuerza que me prometiste. Lo he dado todo. Por favor, mi señor.",
        "Respóndeme, Corifeo Mohg, le suplica. Y su señor, un poco más arriba, dormido junto a un capullo, no responde. Varré muere bendiciendo a la Dinastía Mohgwyn. Con amor.",
        "Antes del número tres, dos comentarios. Dany nos escribió en el de Morgott: me gusta cómo te papeas a los quejosos de la IA. Buenos videos. Gracias, Dany, aunque aquí no se papea a nadie. Se contesta con cariño. Mucho cariño.",
        "E Isaac nos dejó esto: nunca he apoyado el contenido con IA, pero si detrás hay alguien que la usa para crear buen contenido, seré el primero en reconocérselo. Y se suscribió. Isaac, a diferencia de Varré, aquí sí cumplimos lo que prometemos.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Rapta y corrompe a los que curaban.",
        "En el palacio, antes de llegar al capullo, te invaden tres tipos con la misma máscara blanca que Varré. Las Máscaras Blancas sin nombre.",
        "Su túnica cuenta quiénes eran. Cirujanos de guerra, que en la práctica eran verdugos piadosos. Los que daban el golpe de gracia a los heridos que ya no tenían salvación, para que dejaran de sufrir.",
        "Y la túnica sigue. De los cirujanos que raptó el Señor de la Sangre, ninguno logró domar la sangre maldita. Ninguno salvo Varré, aunque él era una excepción.",
        "Raptó. No los invitó. Se llevó a los que acababan con el sufrimiento ajeno, y los puso a trabajar para un dios que, como veremos, desea heridas.",
        "Y su máscara, la que te quedas si los matas, lo termina de contar: la maldición del Señor de la Sangre anima a quien la lleva cuando hay derramamiento de sangre. Los que antes acababan con el dolor, ahora cobran vida con él.",
        "Ahora fíjate en quién más vive en ese pantano. Albináuricos. Los seres pálidos con cara de rana que en el resto del juego son marginados. Gente creada por manos humanas, a la que la gracia nunca tocó.",
        "En el norte, camino del Árbol Hierático de Miquella, el árbol donde viven tantos repudiados, los albináuricos brillan con luz sagrada. Aquí abajo ya no son pálidos. Son rojos. Y les han crecido cuernos enredados. Cuernos de augurio.",
        "La wiki lo resume así: recibieron un don de la Madre Informe a través de la sangre de augurio de Mohg, el Señor de la Sangre. A él lo encerraron de niño por nacer con cuernos. Y ahora es él quien se los hace crecer a otros.",
    ]},
    {"id": "p3b", "frases": [
        "Y su corte no se queda abajo. Los nobles sanguinos, los de la túnica negra con bordado de oro. Las hombreras de metal, dice la túnica, son la señal del rango noble que piensan reclamar cuando llegue la nueva dinastía.",
        "Su arma, la Hélice sangrienta, está diseñada para perforar la carne. Y la sangre extraída, dice la descripción, resbala con elegancia por la hoja. Con elegancia.",
        "Y su técnica de combate, que encuentras en el propio panteón de Mohg, se llama en inglés Blood Tax. Impuesto de sangre. Un remolino de estocadas que le roba al enemigo la sangre y la vida a la vez.",
        "Uno de esos nobles te espera debajo de las Ruinas de Sanguifuria. Las mismas ruinas donde invades a Magnus por encargo de Varré.",
        "Y uno de sus sacerdotes está metido en el corazón de la capital. Esgar, Sacerdote de la Sangre, en las catacumbas de Leyndell, escondidas dentro del Subsuelo de los marginados, con dos perros que te hacen sangrar.",
        "Todo eso sale de un palacio levantado sobre una tumba. El mapa lo dice: en las más tenebrosas profundidades yace la tumba de una antigua civilización. Aquí es donde Mohg, el Señor de la Sangre, está construyendo un panteón para albergar a su futura dinastía. Junto con todas las pesadillas que puedan llegar con ella.",
        "Los dioses barbudos de piedra de esa civilización siguen ahí. Ocho estatuas sin piernas rodean hoy el capullo de Miquella, mirando un altar empapado de sangre.",
        "Y si te preguntas a qué huele esa dinastía, el encantamiento Enjambre de moscas te lo dice: el nuevo palacio del Señor de la Sangre está en un pantano de sangre putrefacta, y estas moscas nacen del excremento de esa tierra.",
        "El Excremento manchado de sangre que recoges allí lleva dentro carne a medio digerir y colonias de huevos diminutos, de origen desconocido. Y la descripción añade: pero sin duda repugnante.",
        "Por cierto, Jonathan nos corrigió en el de Morgott: Morgott no es el rey de los augurios, es el rey augurio. En la traducción oficial en español se llama así, rey de los Augurios. Pero tienes razón en lo que importa: en inglés es Omen King. El rey que es un augurio. Y su gemelo también lo era.",
    ]},
    {"id": "p2", "post": 10.0, "frases": [
        "Número dos. Roba un dios dormido.",
        "Al norte del mundo, más allá del Campo sacroníveo, está el Árbol Hierático. Y Gideon, el Omnisciente de la Mesa Redonda, cuenta lo que pasó allí: el Árbol Hierático ya no es más que un cascarón.",
        "Se rumoreaba que Miquella se había incrustado en el árbol. Pero antes de que pudiera terminar, alguien abrió el árbol y huyó con su forma infante.",
        "Alguien. Ese alguien es Mohg, el Señor de la Sangre. Y Malenia, su hermana gemela, la que juró esperarlo, se quedó en las raíces del árbol esperando a un hermano que ya no estaba.",
        "Fíjate en el camino. La otra entrada al palacio de Mohg, la que no es la medalla de Varré, es un portal escondido en un acantilado del Campo sacroníveo. En el camino al Árbol Hierático.",
        "Y luego, lo que hizo con él. Su recuerdo lo cuenta: con el deseo de convertir a Miquella en una deidad de pleno derecho, Mohg, el Señor de la Sangre, trató de convertirse en su consorte y coronarse como monarca. Sin embargo, por más que trató de compartir con él su alcoba, jamás recibió respuesta del joven empíreo.",
        "En inglés hay una palabra que la traducción se calla. No es su alcoba. Es su alcoba sangrienta. En japonés, su lecho de sangre.",
        "Entre sus frases hay una que lo resume todo: Miquella es mío, y solo mío. Y en otra que el juego nunca llegó a usar, le promete al capullo: nadie más te llevará. Nunca más, lo juro.",
        "Cuando por fin entras en su sala, Mohg está de rodillas junto al capullo, le toma la mano, y se vuelve hacia ti como un anfitrión. Demos la bienvenida a nuestro invitado de honor. Al lugar de origen de nuestra dinastía. Así lo dice él.",
    ]},
    {"id": "p2b", "frases": [
        "Y para despertarlo, la receta de Mohg es la de siempre. Sangre. El talismán Exaltación del Señor de la Sangre lleva sus palabras: rendid vuestras ofrendas de sangre a vuestro señor. Empapad la alcoba de mi consorte. Saciad la sed de su crisálida. Su despertar anunciará el alba de nuestra dinastía.",
        "Ofrendas de sangre. Y no hace falta mucha imaginación para saber de dónde sale tanta. De los Dedos Sangrientos, de los caballeros que mataron a sus doncellas, de cada Sinluz al que invaden.",
        "Su sala es eso: un capullo metido en una pelvis gigantesca, en lo alto del panteón, y alrededor, sangre.",
        "En la expansión supimos que estaba encantado. Ansbach, su antiguo comandante, dice que culpa al encantamiento más que a nada. Y eso lo vimos a fondo en el video de Miquella.",
        "Y aquí alguno dirá lo que Nikova nos escribió en el de Radahn: ¿atrocidad le atribuyes a alguien que perdió la cordura? Buena pregunta, Nikova. Por eso hoy elegimos a uno con la cabeza perfectamente en su sitio. Con plan, con escudo de armas, con uniforme, y hasta con departamento de reclutamiento.",
        "Porque el encantamiento explica por qué se llevó a Miquella. Pero la Madre Informe, los cirujanos raptados, los Dedos Sangrientos y el pantano no los puso Miquella. Y la peor de todas, la número uno, esa la eligió Mohg, él solo, en el subsuelo, mucho antes.",
        "Antes del número uno, el dato de siempre. De cada cien personas que ven este canal, solo unas cuatro están suscritas. Ya pasamos los seiscientos cincuenta, y la meta es mil.",
        "Mohg, el Señor de la Sangre, llenó un lago de sangre para que alguien le respondiera, y aun así nadie le respondió. Aquí basta con un botón. Y te respondemos en el siguiente video.",
    ]},
    {"id": "p1", "post": 11.0, "frases": [
        "Número uno. Su dios desea una herida.",
        "Volvamos al principio. Mohg y Morgott nacieron augurios, y por ser de la realeza no les cortaron los cuernos. Los encerraron bajo la capital. Lo dice el Grillete de Mohg, en su descripción: estos se hicieron para mantener a un augurio concreto bajo el más estricto encierro.",
        "Y ahí abajo, en la oscuridad, Mohg encontró a alguien. El encantamiento Favor sanguino lo cuenta: la madre de la verdad desea heridas. Cuando Mohg, en las profundidades de la tierra, se encontró ante ella, su sangre maldita estalló en llamas. Y quedó prendado de la impureza con la que había nacido.",
        "Su gemelo hizo justo lo contrario. Morgott repudió esa sangre y la encerró en una espada. Mohg, en cambio, la encendió y la adoró.",
        "La Madre Informe. Un dios exterior. No es de las Tierras Intermedias, no tiene forma, y lo único que pide es eso. Heridas.",
        "Su tridente, la Lanza sagrada de Mohgwyn, no es solo un arma. Es un instrumento de comunión con un dios exterior que concede poder a la sangre maldita. Y la descripción termina igual: la madre de la verdad desea una herida.",
        "Y el Favor sanguino consiste en meter el brazo dentro del cuerpo de la Madre Informe y esparcir su hemofuego. La técnica de la lanza es parecida: alzarla y atravesar el cuerpo de la Madre Informe. Hasta tres veces.",
        "Tres veces. Ahí está la cuenta atrás que todos recordamos. En la pelea, Mohg alza el tridente y cuenta en latín. Tres. Dos. Uno. Y con cada número, un anillo rojo se cierra a tu alrededor.",
        "Y cuando le quitas la mitad de la vida, clava la lanza en el aire tres veces y grita la palabra que Zohary escribió en su comentario. Escúchalo.",
    ]},
    {"id": "p1b", "post": 3.5, "frases": [
        "Nihil. Nada, en latín. Y cada grito te arranca la vida a ti, y se la devuelve a él.",
        "La Lágrima cristalina purificadora existe casi solo para esa pelea. Dice que purifica la maldición del terrible ritual de sangre de Mohg, el Señor de la Sangre. En japonés la llama la maldición que cuenta.",
        "No es un ataque. Es un sacrificio. Y el sacrificado eres tú. Tu herida, para la madre de la verdad.",
        "Ahora piensa en todo lo que usaste en el juego con sangre. Garras de hemofuego, Hoja de hemofuego, Enjambre de moscas. Todos dicen lo mismo: un encantamiento de juramento de sangre, concedido por el Señor de la Sangre.",
        "Y la Gran Runa de Mohg, a diferencia de las otras, no te da vida ni fuerza. Da una bendición de sangre a los espíritus que invocas, y Grandes Runas espectrales cuando invades a otro jugador.",
        "Todo el poder de Mohg está hecho para que la sangre corra. Para que haya heridas. Y la madre de la verdad desea una herida. Cada una.",
        "Ese era el plan de la Dinastía Mohgwyn. Un dios niño despertado con sangre, un rey consorte con cuernos, y detrás de los dos, una diosa sin forma que solo quiere que el mundo sangre.",
        "Sus hermanos querían un trono, una era de las estrellas, un orden nuevo. Mohg, en cambio, quería entregarle las Tierras Intermedias a una diosa que se alimenta de heridas.",
        "Y aquí viene lo de que probablemente ya lo has hecho. Si jugaste con sangrado, con la Ríos de Sangre de Okina, con hemofuego, o invadiendo con su Gran Runa, en el lore estabas haciendo exactamente lo que él quería.",
        "Media comunidad se pasó el juego a base de sangrado. Tanto, que hubo que bajarlo en varios parches. Sin saberlo, fuimos los Dedos Sangrientos más fieles que tuvo Mohg, el Señor de la Sangre.",
        "Y cuando por fin lo matas, no se arrepiente. Cae, mira hacia arriba y grita su visión: ¡Ah, lo veo, tan claro como el día! ¡La llegada de nuestra dinastía! Y su último grito es el nombre de su casa.",
    ]},
    {"id": "p1c", "frases": [
        "Mohgwyn. Y fíjate en la pose en la que muere, de rodillas, como si le arrancaran el corazón. Es la misma que pones tú cuando, en la expansión, el Radahn consorte te roba el corazón.",
        "Estaba encantado hasta el último segundo. Pero el lago de sangre que rodea ese capullo, ese, lo llenó él.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Te recluta desde el primer paso para cazar a los tuyos, te pide la sangre de una doncella, rapta a los que curaban y les hace crecer cuernos a los marginados, roba un dios dormido para empaparlo en sangre, y le ofrece el mundo entero a una diosa que desea heridas.",
        "Y aun así, de todos los hijos de Márika, es el único que amó lo que era. Su Gran Runa lo dice: amaba el lodazal en el que nació. Lástima que ese amor necesitara tanta sangre ajena.",
        "Antes de irme, gracias a los que nos escriben. José Luis nos contó que ya vio todos los videos de las atrocidades, que ya era justo suscribirse, y que cada uno es mejor que el anterior, sobre todo desde el formato largo. José Luis, este dura veintitrés minutos. Para ti.",
        "David ya lleva unos siete videos, y nos felicita. Y Eternalack lo resumió en cuatro palabras: excelente saga de videos.",
        "Y Escuadrón preguntó cuándo hacemos las cinco peores atrocidades de Torrentera. Lo estamos investigando. Por ahora solo tenemos una: te deja tirado en cuanto entras a una mazmorra.",
        "Los comentarios se leen todos, de verdad, y con ellos vamos mejorando el canal. Por eso ya están apuntados Rykard, que piden Franko y Héctor, Godwyn, que pide Carl, y Maliketh, que pide Justin.",
        "Ahora te toca a ti. ¿Fue Mohg un villano de verdad, o solo el primer encantado de Miquella? Y Zohary, espero que tu patrón haya quedado a la altura.",
        "Si te quedaste con ganas de más familia, en el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn y Morgott, su gemelo. Y si te suscribes, nos acercas a los mil.",
        "Y la próxima vez que un Dedo Sangriento te invada, acuérdate: no viene por ti. Viene por tu sangre. Para la madre de la verdad.",
    ]},
]
