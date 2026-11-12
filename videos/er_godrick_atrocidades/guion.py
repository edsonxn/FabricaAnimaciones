# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Godrick QUE IGNORASTE» (11-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md).
VOZ NUEVA (el usuario, 11-nov-2026): «el Profeta» de ElevenLabs, PLANA: sin risas ni emociones alegres; a veces enojón o un gruñido.
Al inicio, VOTACIÓN en comentarios: «narrador anterior» o «nuevo profeta» (el que tenga más comentarios se queda); se OYE el anterior
(sfx/s_faraon.mp3 = toma real de Faraon en Mohg). 25 MIN (pedido del usuario). Sin patrocinio. Fórmula: canales/formula/runa_caida.md.
Tema pedido en los comentarios: @JustinRivera-c9l ♥3 («Las atrocidades de godrick») y @Ádolf777-t5u («Godrick porfa»).
Críticas con contraburla (regla 11-nov, mínimo 3): @JoseDuranRM (p5b), @GonzaloCabral-el5yb (p4b), @madrizu6186 (cierre) + @DiegoFlores-ed3yx (voto2, p3).
Investigación: _investigacion/dossier.md (citas verificadas; lo CORTADO del juego se dice como tal y lleva rótulo en pantalla).
Sonidos nombrados = tramo audible con `post` al final de su escena (regla del 31-oct-2026): voto (Faraon), p3 («I command thee,
kneel!»), p1 (monólogo cortado de la cacería), p1b (Gostoc cortado, «A fine branch!»).
"""

TITULO = "Las 5 peores atrocidades de Godrick QUE IGNORASTE"
ARCHIVO = "er_godrick_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
# el Profeta (ElevenLabs God - Deep, Powerful). Corchetes SOBRIOS: nada de risas ni alegría (el usuario, 11-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
CER_MAX_POR_FRASE = {'p4b_6': 0.016, 'p1_1': 0.024, 'intro_1': 0.017, 'intro_2': 0.019, 'voto_1': 0.015, 'p5_2': 0.022, 'p5_3': 0.016, 'p5_5': 0.014, 'p5b_2': 0.024, 'p5b_3': 0.02, 'p4_1': 0.019, 'p4_2': 0.017, 'p4b_0': 0.017, 'p4b_3': 0.018, 'p4b_5': 0.014, 'p4b_7': 0.025, 'p4b_8': 0.016, 'p3_1': 0.017, 'p3b_4': 0.002, 'p3c_2': 0.055, 'p2_0': 0.036, 'p2b_5': 0.014, 'p1_3': 0.02, 'p1b_2': 0.02, 'p1b_3': 0.014, 'p1c_2': 0.014, 'cierre_2': 0.018, 'cierre_6': 0.031, 'cierre_7': 0.043}
GAP_MAX_POR_FRASE = {'p4b_6': 0.58, 'p1_1': 0.6, 'intro_1': 0.65, 'intro_2': 0.5, 'voto_1': 0.58, 'p5_2': 0.65, 'p5_3': 0.65, 'p5_5': 0.65, 'p5b_2': 0.6, 'p5b_3': 0.64, 'p4_1': 0.71, 'p4_2': 0.58, 'p4b_0': 0.58, 'p4b_3': 0.52, 'p4b_5': 0.55, 'p4b_7': 0.9, 'p4b_8': 0.53, 'p3_1': 0.57, 'p3b_4': 0.56, 'p3c_2': 0.61, 'p2_0': 0.76, 'p2b_5': 1.36, 'p1_3': 0.6, 'p1b_2': 0.52, 'p1b_3': 0.79, 'p1c_2': 0.62, 'cierre_2': 0.58, 'cierre_6': 0.55, 'cierre_7': 0.48}
TAIL_MAX_POR_FRASE = {'p4b_6': 0.71, 'p1_1': 0.75, 'intro_1': 0.84, 'intro_2': 0.79, 'voto_1': 0.73, 'p5_2': 0.91, 'p5_3': 0.8, 'p5_5': 1.08, 'p5b_2': 0.83, 'p5b_3': 0.55, 'p4_1': 0.97, 'p4_2': 1.07, 'p4b_0': 0.71, 'p4b_3': 0.73, 'p4b_5': 0.86, 'p4b_7': 1.01, 'p4b_8': 0.59, 'p3_1': 0.76, 'p3b_4': 1.05, 'p3c_2': 0.65, 'p2_0': 0.06, 'p2b_5': 0.76, 'p1_3': 0.76, 'p1b_2': 0.8, 'p1b_3': 0.71, 'p1c_2': 0.75, 'cierre_2': 1.07, 'cierre_6': 0.83, 'cierre_7': 0.83}
FONETICA = {"Miquella": "Miquéla"}   # 12-nov: el Profeta decía MÍ-que-lla; el acento va en «que» (ミケラ, inglés mi-KEL-la)

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={"scene-002": .09, "scene-003": .09, "scene-012": .09, "scene-076": .09, "scene-078": .09, "scene-080": .09, "scene-085": .09, "scene-089": .09, "scene-105": .09, "scene-108": .09, "scene-144": .09, "scene-152": .09, "scene-153": .09, "scene-172": .09},   # [SHIRRAKO] marca de agua abajo a la derecha
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "El primer jefe que te mató en Elden Ring tenía cara de niño. Pelo plateado, un montón de brazos, y un escudo dorado del linaje de Godfrey. [short pause] Y, según todo indica, salió del taller del hombre de hoy.",
        "Justin nos dejó un comentario de cuatro palabras: las atrocidades de Godrick. Y Ádolf lo remató: uno de mi favorito, Godrick, porfa. Pues aquí está, Ádolf. [short pause] Tu favorito.",
        "Godrick el Injertado tiene fama de chiste. El primer semidiós, el gordo de los brazos cosidos, el que se cae en dos intentos y ya nadie se acuerda de él.",
        "Pero ese chiste tenía un castillo lleno de miembros colgados en el comedor, un trol crucificado sobre el patio y una pila de cadáveres a la que tú también ibas a ir a parar.",
        "Así que van las cinco peores atrocidades de Godrick el Injertado, que ignoraste. [short pause] Y la número uno no es lo que les hizo a otros. Es lo que tenía pensado hacer contigo.",
    ]},
    {"id": "voto", "post": 12.4, "frases": [
        "Antes de empezar, algo ha cambiado en el canal. Y ya lo notaste: [short pause] yo.",
        "Muchos de ustedes se quejaron de la voz. Con razón. Lo de Miqueya y Mojé no tiene defensa. Así que hoy estrenamos un sistema de voz nuevo, un poco más profesional. Pero la decisión no es mía. Es tuya.",
        "Para que compares, el narrador anterior sonaba así.",
    ]},
    {"id": "voto2", "frases": [
        "Y yo sueno así. [long pause] Ahora vota. Escribe en los comentarios: narrador anterior, o nuevo profeta. El que tenga más comentarios gana, y se queda en el canal.",
        "Diego escribió que en estos videos la inteligencia artificial está de más. Diego, por eso votamos. Si gana el anterior, vuelve el anterior. Si gana el profeta, se queda el profeta. Lo único que no puede ganar es Loquendo. Lo pidieron tres personas, y sigue sin presentarse.",
        "Wolfdragon nos escribió que le encanta cómo narramos. Wolfdragon, ahora tienes dos para elegir. Y lksdmn pidió más videos de formato largo, porque se aprende muchísimo. Este dura veinticinco minutos. Ponte cómodo.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. [short pause] El cobarde dorado.",
        "Para entender a Godrick hay que empezar por la Devastación, la guerra que estalló cuando se rompió el Círculo de Elden. Los semidioses se pelearon por los pedazos, y cada uno eligió un bando.",
        "Godrick eligió el suyo: el de la puerta de atrás. Kenneth Haight, el noble que te encuentras en Necrolimbo, lo cuenta sin ningún respeto. Primero se escondió entre las mujeres para huir de la capital. Luego se escondió de Radahn en ese castillo.",
        "Y no huyó con las manos vacías. En el Castillo de Velo Tormentoso, en la sala del Vástago injertado, hay un cofre con el Velo de imitador. Su descripción dice que, cuando a Godrick lo echaron de Leyndell, la capital del reino, ese fue uno de los muchos tesoros que se llevó consigo.",
        "Hasta su ejército es un ejército de fugitivos. Las Cenizas de soldado de Godrick lo dicen claro: los soldados que sirven a Godrick el Injertado son lo que queda del ejército que huyó de la capital del Árbol Áureo.",
        "La Lectora de Dedos Enia, la que te cambia los recuerdos de los jefes en la Mesa Redonda, lo resume peor. Godrick no era más que un pariente lejano. El enclenque de la camada, con la sangre divina muy diluida.",
        "Y aun así, en su sala del trono, Godrick se sienta bajo una estatua de Godfrey, el primer Señor del Círculo. El antepasado al que no se parece en nada. [short pause] Y al que le habla mientras pelea.",
    ]},
    {"id": "p5b", "frases": [
        "Pero lo peor no es que huyera. Es lo que hizo cuando tuvo que dar la cara. Kenneth sigue: luego insultó a Malenia, perdió contra ella, y le lamió las botas en vez de morir como un hombre.",
        "En el japonés original es todavía peor. No le lamió las botas. Le lamió los dedos de los pies y le juró obediencia.",
        "Y no es un rumor de taberna. Está grabado en piedra. Junto al Lago de Agheel, en el oeste de Necrolimbo, hay un monumento con una espada clavada. Si te acercas, lo puedes leer.",
        "La humillación de Godrick el Dorado. Tras haber saboreado la derrota bajo la espada de Miquella, ahora se arrodilla y suplica clemencia.",
        "[sighs] Alguien se tomó la molestia de tallar eso en una roca, a la vista de todo el que pase por el camino. Godrick el Dorado, el que en su pelea te ordena que te arrodilles, tiene un monumento público que recuerda la vez que se arrodilló él.",
        "Y aquí, una aclaración para José. En el video de Radahn escribió: ¿cómo que aguantó a Malenia? Si la tenía de hija.",
        "José, el que la tenía de hija terminó podrido en Caelid, vagando sin juicio entre cadáveres. Si eso es tenerla de hija, prefiero no ver cómo se pierde. [short pause] Aunque, bueno, sí lo vimos. Se llama Godrick, y tiene monumento.",
        "Kenneth cierra su opinión con una frase que lo dice todo. Y pensar que es sangre de Godfrey. El último del linaje dorado, aunque al verlo casi no lo dirías.",
        "Un cobarde que huye de todas las guerras no parece gran cosa en una lista de atrocidades. Hasta que te preguntas qué hizo con todo ese tiempo libre, escondido en su castillo. [short pause] La respuesta está en los cuatro puestos que quedan.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. [short pause] Sus feudos del terror.",
        "Godrick no gobernaba solo Velo Tormentoso. Al sur, en la punta de la Península del Llanto, está el Castillo de Morne. Y quien lo manda se presenta así: soy Edgar, alcaide de este castillo por mandato del propio Lord Godrick.",
        "Cuando llegas, Morne está en llamas. Los Bastardos, esas criaturas peludas con cara de león, se han rebelado. Edgar no lo entiende. Me servían bien, dice, o eso creía.",
        "Y tú bajas a las celdas a ver cómo los servían. En la segunda zona de celdas, entre ratas y un Bastardo encerrado, hay un objeto en el suelo. Un látigo.",
        "Su descripción no deja dudas: es un látigo de cuero que no se usaba para combatir, sino como instrumento de dolor.",
        "Ese era el servicio. Esclavos encerrados con las ratas y un látigo para que trabajaran. Y en lo más alto del castillo te espera el Bastardo leonino, el jefe que defiende la espada de Morne.",
        "La espada se llama Espadón de hoja injertada. Hoy su descripción habla de océanos de ira y arrepentimiento. Pero en la primera versión del juego, en chino y en coreano, decía otra cosa: una espada hecha uniendo las espadas de los guerreros que sirvieron a Godfrey. Hasta las armas de su castillo estaban injertadas.",
        "Tristán nos escribió que cada vez mejoramos más. Tristán, a Godrick le pasaba lo mismo con su castillo. Cada vez más miembros. Cada vez más cosidos.",
    ]},
    {"id": "p4b", "frases": [
        "Lo que Morne le costó a la gente de Morne tiene nombre. Irina, la hija de Edgar. Una chica ciega que encuentras junto al Puente del Sacrificio, con una carta para su padre.",
        "Edgar se quedó en el castillo porque el deber se lo exigía. El deber con Godrick. Y la siguiente vez que pasas por el puente, Irina está muerta.",
        "Edgar lo reconoce, roto: elegí el deber antes que la seguridad de mi hija. Y no se queda ahí. Más adelante enloquece y te invade en la Choza del Vengador, en Liurnia, convertido en eso: un vengador.",
        "Godrick ni se entera. Para él, Morne era una pieza más del mapa. Igual que el Fuerte de Haight, en la costa este de Necrolimbo, el fuerte de la familia de Kenneth.",
        "Kenneth te cuenta quién se lo quitó. Un caballero comandante de Velo Tormentoso. Un necio, y loco de remate. Obsesionado con la sangre.",
        "Y cuando subes a matarlo, el comandante usa Tajo sangriento y lleva colgada la Exultación del Señor de la Sangre. El talismán de Mohg. Uno de los caballeros de Godrick, rezándole al Señor de la Sangre.",
        "Por cierto, Gonzalo. En el video de Mohg dijiste que, en comparación con otros semidioses, ni tan mal. Que sus peores atrocidades las hizo estando podrido, o controlado por Miquella.",
        "Gonzalo, este caballero nunca vio a Miquella. Y ya llevaba la Exultación de Mohg al cuello, en Necrolimbo, al principio del juego. Mohg no necesitaba un encantamiento para tener fieles. [short pause] Ni tan mal, dice. Es como decir que el lago de sangre de Mohgwyn está ni tan mojado.",
        "Esclavos con látigo en Morne. Un comandante adorador de la sangre en Haight. Y una chica ciega muerta en un puente. Ese era el reino de Godrick. Y todavía no hemos entrado en su castillo.",
    ]},
    {"id": "p3", "post": 11.8, "frases": [
        "Número tres. [short pause] El dragón y su propio brazo.",
        "Antes de llegar a él, Varré, el del Rostro Alabastrado, te avisa: dicen que el viejo Godrick tiene un juguete nuevo y feroz que injertarse. Así que prepárate para lo peor.",
        "El juguete está en la arena. Un patio de tumbas donde, sobre una estatua, hay un dragón muerto, atravesado de lado a lado. Y Godrick le habla como a un pariente.",
        "Poderoso dragón, eres un heredero de verdad. Préstame tu fuerza. En japonés, la frase es más reveladora: le llama dragón, descendiente como yo. [short pause] Y luego se gira hacia ti.",
        "Un Sinluz miserable, jugando a ser señor. Y suelta la frase que lleva grabada su propia hacha, en la traducción oficial: ¡Te ordeno que te arrodilles! ¡Soy señor de todo cuanto es dorado! Escúchalo de su boca.",
    ]},
    {"id": "p3b", "frases": [
        "Y cuando le quitas algo más de la mitad de la vida, Godrick hace lo que hace siempre que pierde. Busca algo de otro para pegárselo.",
        "Levanta el hacha y se corta el brazo izquierdo. Él mismo. De un golpe. Y en el muñón se cose la cabeza del dragón muerto. [short pause] Ahh, el más auténtico de los dragones, préstame tu fuerza. Antepasados, todos vosotros. Sed testigos.",
        "La descripción del Dragón injertado, el arma que sale de su recuerdo, lo confirma: la encarnación del poder que aún quedaba en la cabeza de dragón injertada en el brazo izquierdo de Godrick. Y su habilidad se llama Sed testigos.",
        "Fíjate en lo que está pasando. Un hombre que se mutila delante de ti para coserse el cadáver de una criatura que, según él, era como él. Un descendiente menor. Y lo usa para escupir fuego.",
        "Diego, también preguntaste para cuándo los dragones. Aquí tienes uno. Muerto, empalado y cosido a un muñón. No es el video que pediste, pero es el dragón que hay.",
        "Y cuando te mata en esta fase, Godrick no te habla a ti. Le habla a la estatua del trono. Gran Godfrey, ¿lo has visto? [short pause] Todo lo que hace es para un antepasado que nunca lo miró.",
    ]},
    {"id": "p3c", "frases": [
        "Y lo peor es que no es un caso aislado. Es cosa de familia. En la Meseta Altus, al sur, hay una cárcel eterna. La del linaje dorado. Y dentro hay otro hombre con la misma cara, los mismos brazos y los mismos ataques de Godrick.",
        "Se llama Godefroy, el Injertado. El juego no dice exactamente qué parentesco tenía con Godrick. Solo que era de su sangre, y que también se injertaba.",
        "Lo que sí cuenta son las Cenizas de Kristoff, un caballero del dragón antiguo. Tras la primera defensa de Leyndell, Kristoff se ganó el honor de un entierro en el Árbol Áureo por capturar a Godefroy el Injertado.",
        "Un pariente que atacó la capital, y al que encerraron para siempre por lo que era. Cuando lo matas, deja caer el Icono de Godfrey. [short pause] Otra vez, todo vuelve a Godfrey.",
        "El linaje dorado no solo perdió su gracia. Una parte de él se dedicó a coserse a otros para recuperarla. Y Godrick, el enclenque de la camada, es el que más lejos llegó.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. [short pause] Los hombres de Roderika.",
        "En la Colina Tormentosa, en una cabaña junto al camino al castillo, hay una chica sentada en el suelo. Se llama Roderika. Viene de otra tierra, cruzó el mar con un séquito, y está sola.",
        "Si le preguntas, te dice lo que pasó con los demás. A todos los injertaron. A todos los que vinieron conmigo. Cruzaron el mar por mí. Lucharon por mí.",
        "Solo para que les quitaran los brazos. Las piernas. Hasta la cabeza. Se los quitaron, y se los pegaron a la araña.",
        "Y añade, como si no pesara nada: ¿sabías que si la araña te injerta te conviertes en crisálida? Tiene gracia, si lo piensas.",
        "La araña es el Vástago injertado. Esa criatura con muchas extremidades, rostro de joven noble y pelo plateado. En japonés, su nombre significa el príncipe injertado. Las wikis lo atribuyen a la técnica de Godrick, aunque el juego nunca lo dice con esas palabras.",
        "Roderika no fue injertada porque tuvo miedo. Da miedo, ¿sabes?, te dice. Que te corten los brazos. O las piernas. O la cabeza. Quiero ser como los demás, pero me da demasiado miedo.",
        "Y te hace un encargo. Diles que los quiero. Y que, aunque tenga un corazón cobarde, seguro que pronto me uniré a su club.",
    ]},
    {"id": "p2b", "frases": [
        "Ese club existe. Lo encuentras en Velo Tormentoso, cerca de la Torre de defensa, en el patio que da a la sala del Vástago. Una pila de cadáveres. Y encima, un trol crucificado.",
        "Bajo el trol, tirado entre los muertos, hay un broche. El Recuerdo de las crisálidas. Su descripción: recuerdo que dejaron las crisálidas sacrificadas para el injerto. Un broche envuelto en terciopelo rojo, con restos de sangre.",
        "Espíritus apenas visibles intentan decir algo. Pero no se oyen sus voces.",
        "Eso es lo que queda de los hombres que cruzaron el mar por Roderika. Un broche, en un montón de cuerpos, debajo de un trol. Y para los halcones de guerra del castillo, ni eso. Sus cenizas cuentan que les cortaron las garras para injertarles espadas finísimas en su lugar.",
        "Y aquí viene lo que casi nadie vio. Cuando Roderika ya se ha convertido en afinadora de espíritus en la Mesa Redonda, o si nunca hiciste su misión, al llegar a Farum Azula, aparece algo nuevo en esa misma pila de cadáveres.",
        "Su capucha carmesí. [long pause] La de Roderika. El juego no dice qué le pasó. Solo deja su ropa donde están los suyos.",
        "Amand escribió que cuando crees que ya lo sabes todo y lo exploraste todo, encuentras algo así, y el juego se vuelve un descubrimiento interminable. Amand, este es de los que no se olvidan.",
        "Y antes del número uno, algo rápido. De cada cien personas que ven estos videos, menos de cinco están suscritas. Ya pasamos los setecientos cuarenta, y la meta es mil. Gun-chikito nos escribió que nos ganamos una persona suscrita. Si llegaste hasta aquí, sé la siguiente. No pide injertarte nada.",
    ]},
    {"id": "p1", "post": 12.8, "frases": [
        "Número uno. [short pause] Tú eras el ingrediente.",
        "Piensa en cómo llegas a Velo Tormentoso. Varré te recibe en Necrolimbo y te manda allí: a Godrick, donde la gracia te guía. Y Roderika, cuando le cuentas de dónde vienes, suelta una frase: te convenció el de la máscara blanca, supongo.",
        "Lo que dice es que a su grupo lo mandaron igual. El mismo camino, el mismo castillo, el mismo final.",
        "Y por el camino, todos te avisan. Kenneth Haight: yo de ti me cuidaría mucho de las cacerías de Sinluz de Godrick. Esa panda de depravados está obsesionada con sacrificar a Sinluz como tú en nombre del injerto.",
        "En japonés, lo dice más claro todavía: para ellos, los Sinluz no son más que ofrendas para su abominable injerto. Y Rogier, el hechicero que encuentras dentro del castillo, lo repite: este sitio está plagado de cazadores de Sinluz. Sacrifican a los nuestros para injertarlos.",
        "En los archivos del juego hay un monólogo de Godrick que no llegó a la versión final. En él, Godrick reúne a sus caballeros y ordena la cacería. Pide una rama poderosa, una ofrenda fresca que injertar. Y termina con una orden. [short pause] Traedme un Sinluz. Escúchalo.",
    ]},
    {"id": "p1b", "post": 9.0, "frases": [
        "Rama. Así llama a la gente. Su nombre japonés, tsugiki, es la palabra de jardinería para el injerto de árboles. Para Godrick, tú no eres un rival. Eres una rama.",
        "Y en la puerta del castillo te espera alguien para cortarla. Gostoc, el guardián. Te abre una entrada lateral para que no entres por la principal, y luego te encierra en una sala oscura con un Caballero proscrito. Si mueres, te roba las runas.",
        "Si lo espías, lo encuentras revolviendo cadáveres. Basura. Otro que es todo piel y huesos. Ahh, este tampoco tiene ni un músculo. Y si te mata, te consuela: tranquilo, tengo grandes planes para lo que queda de ti.",
        "Las wikis no se ponen de acuerdo en para qué quería los cuerpos. Pero en los archivos cortados del juego, Gostoc tenía otra presentación. Soy hijo de Godrick, sin duda. Elegido por la sangre para injertar.",
        "Y al matarte, en esas líneas cortadas, no decía tranquilo. Gritaba de alegría por haber encontrado material. Escúchalo tú mismo.",
    ]},
    {"id": "p1c", "frases": [
        "Una rama magnífica. Que empiece el injerto. [short pause] Así te veían en Velo Tormentoso.",
        "Y lo más humillante llega en la pelea. Si Godrick te mata en la primera fase, te mira desde arriba y te lo dice a la cara. Sinluz miserable. No vales ni para injertarte.",
        "Ni para eso. Los hombres de Roderika sirvieron. Los halcones sirvieron. El dragón muerto sirvió. Y tú, según él, no servías para nada.",
        "Y ahora vuelve al principio del juego. A la Capilla de la espera. A la criatura de muchos brazos, cara de niño y escudo dorado que te mató antes de que supieras ni dónde estabas. La que te arrastró a la Tumba abandonada.",
        "Las wikis la cuentan entre las obras del injerto del linaje dorado. Tu primera muerte en Elden Ring fue a manos de un producto terminado. [long pause] Y tú eras la siguiente materia prima.",
        "Cuando por fin cae, Godrick no se arrepiente de nada. Sus últimas palabras las repite su recuerdo: algún día volveremos juntos a nuestro hogar bañado en rayos de oro. En japonés, se lo dice a sus soldados. El mismo ejército de fugitivos con el que huyó de ese hogar.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Huye de todas las guerras con un botín y le lame los pies a Malenia. Gobierna esclavos con látigo y deja morir a una chica ciega por deber. Se corta su propio brazo para coserse un dragón muerto. Convierte un séquito entero en piezas de una araña. Y te espera en su castillo como a una rama más.",
        "Y aun así, de todos los semidioses, fue el único que te mandaron a matar primero. Porque era el más débil. [short pause] Lo que nadie te dijo es que el débil también tenía hambre.",
        "Antes de irme, una respuesta para Madrizu, que en el video de Ranni escribió: ¿Ranni la peor de todas? Lo único que entendiste es a usar la IA para crear contenido.",
        "Madrizu, te doy la razón en una cosa. Aprendí a usar la inteligencia artificial. Tanto, que ahora te habla un profeta. Lo de Ranni no lo retiro. Planeó la Noche de los Cuchillos Negros, donde murió Godwyn, y al final se lleva el Círculo de Elden lejos de todos. Pero claro, la atrocidad es la mía, por contarlo.",
        "Los comentarios se leen todos, de verdad, y con ellos vamos mejorando el canal. Este video existe porque Justin y Ádolf lo pidieron, y esta voz existe porque muchos de ustedes se quejaron de la anterior.",
        "Así que no te olvides de votar. Narrador anterior, o nuevo profeta. El que tenga más comentarios se queda.",
        "Ya están apuntados Godfrey y Godwyn, que piden John y Carl, Messmer, que piden Santiago y Alphonse, Rennala, y hasta Bayle el Temible. Dinos cuál quieres que sea el siguiente.",
        "En el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn, Morgott y Mohg. Y si te suscribes, nos acercas a los mil.",
        "Y la próxima vez que un Vástago injertado te mate al empezar una partida nueva, recuerda de dónde viene. [short pause] Y que, para Godrick, ni siquiera valías como rama.",
    ]},
]
