# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Messmer QUE IGNORASTE» (24-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + pantallas + MG de mg_er; docs/estilo_secuencia_yt.md).
Elegido por el usuario en el «buenos días» (de Rennala y Maliketh); pedido ≤ 10 días por Stormy, Sergio, Luis, Quaerens, Rick
(tarjetas com_*); Santiago (11-nov) y Alphonse (8-nov) solo en voz. ≈ 25 min. Voz «el Profeta» de ElevenLabs, PLANA. Sin
patrocinio. OST oficial del DLC (bajar_ost.py).
Investigación: _investigacion/dossier.md. Citas textuales = descripciones de objeto en español ([EG]/[ES-wiki]) y las líneas de
Messmer de la wiki ES; diálogos que solo existen en inglés (Anciana, Cornamentado, Leda, Queelign, almas) van PARAFRASEADOS.
Bendición de Márika: EN/JP («varias… y nunca más»), parafraseada (EG transcribe otra cosa). NO decir: Gran Runa de Messmer,
prisiones de Messmer, Aldea de las moscas quemada, «Messmer mandó quemar Rauh», «Cornudo», «Tierra de las Sombras».
Críticas con contraburla (regla 11-nov): @rico_sin_dinero (intro), @pascualvidal (p3c; nunca se niega la IA), @retos9132 (p1c).
Agradecimientos: David, Quixilero (p4b) · Shiro, Ulises, Daniel (subs) · Santiago (cierre, vota Bayle).
Sonidos nombrados = tramo audible con `post` (regla 31-oct / regla 10), voz sola de qSRYSmEx0z0 y 6m4rlHbjecA (dossier § 5):
intro («Those stripped of the Grace of Gold…», S1), p2b (Cornamentado «Messmer, foe of my beloved people…», S6),
p1b («Mother, wouldst thou truly Lordship sanction…», S2), cierre («Mother… Marika… A curse upon thee», S5).
"""

TITULO = "Las 5 peores atrocidades de Messmer QUE IGNORASTE"
ARCHIVO = "er_messmer_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
# el Profeta (ElevenLabs God - Deep, Powerful). Corchetes SOBRIOS: nada de risas ni alegría (el usuario, 11-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {"Miquella": "Miquéla", "Messmer": "Mésmer", "Queelign": "Cuílin", "Huw": "Jiu"}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={**{s: .125 for s in ("scene-007", "scene-068", "scene-071", "scene-075", "scene-076")},   # tráiler oficial con franjas negras (131 px arriba y abajo)
                 **{f"scene-{n:03d}": .075 for n in (2, 4, 6, 12, 13, 15, 23, 24, 27, 33, 69, 70, 78, 140, 142, 144, 148, 149, 153, 159, 160, 161, 162)}},   # Stride (PoTk3y9244M): marca tenue «KINGDOMKEY JT» abajo a la derecha (y ≥ 1010 px)
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=1500, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar", "Shirrako", "pgp"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "post": 11.8, "frases": [
        "Messmer el Empalador. Hijo de la reina Márika, señor del Reino de las Sombras, y el jefe que te espera en lo más alto de la Fortaleza sombría, con una lanza en llamas y una serpiente dentro.",
        "Antes de pelear, te mira desde arriba y te suelta una frase que resume su vida entera. La dice en inglés, con esa voz que no se olvida. Escúchalo.",
    ]},
    {"id": "introb", "frases": [
        "En español: quienes se ven despojados del don del oro deberán hacer frente a la muerte. En el abrazo de la llama de Messmer.",
        "Casi todo el mundo cree que lo peor de Messmer es que quemó a un pueblo entero, los cornamentados. Y es verdad. El propio juego lo anuncia: un reino purgado en una batalla olvidada, y calcinado por la llama de Messmer.",
        "Pero eso ya lo sabe todo el mundo. Hoy va lo otro. Lo que les hizo a sus propios caballeros. Lo que hizo con los dioses de otro pueblo. Una sopa fría que lleva años esperando en una mesa. [short pause] Y en el número uno, una frase en la que también estabas tú.",
        "Este video lo pidieron ustedes, y con ganas. Stormy escribió que se va a volver loco esperando las atrocidades de Messmer. Sergio las pidió dos veces, con las manos juntas. Y Luis lo dijo claro: es hora de empezar con el DLC, Messmer es el siguiente.",
        "Rick dice que es de sus personajes favoritos. Y Santiago y Alphonse lo pidieron hace semanas, cuando aquí todavía íbamos por Godrick. [short pause] Stormy, ya puedes recuperar la cordura. Aunque después de este video, no te la garantizo.",
        "Y antes de empezar, un comentario sobre el título. Rico nos preguntó: ¿por qué supones que lo ignoré, y no lo disfruté?",
        "Tienes toda la razón, Rico. No todo el mundo lo ignoró. Algunos lo disfrutaron. [short pause] Para ellos, el ejército de Messmer mandó hacer una medalla. Sale en el número uno.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. [short pause] Su propia gente, a la tumba.",
        "Antes de quemar a nadie de fuera, Messmer ya había quemado lo de dentro. Empecemos por sus caballeros más famosos, los de la armadura roja: los Caballeros de Fuego.",
        "Su casco lo cuenta. Todos los caballeros provenían de alguna importante familia de los niveles superiores del Árbol Áureo, pero fueron marginados, perseguidos y expulsados de sus hogares tras jurar lealtad a Messmer como su señor.",
        "Jurarle lealtad te costaba la casa. Y su armadura añade lo que recibían a cambio: solo ellos llegaron a conocer de verdad a Messmer. Sus llamas son como serpientes.",
        "Ese era el secreto del ejército. Su señor llevaba una serpiente dentro. Su Recuerdo lo dice sin rodeos: una serpiente malévola se retorcía dentro de Messmer, por lo que su madre le arrancó el ojo y lo sustituyó por un sello de Gracia.",
        "Y aun así, con eso dentro, su madre lo puso al frente de una guerra. El Escudo con blasón de serpiente se forjó para conmemorar los inicios de la cruzada iniciada por Messmer, hijo de Márika.",
        "Un ojo arrancado y un sello encima. [short pause] Y no todos sus hombres lo aceptaron cuando se enteraron.",
    ]},
    {"id": "p5b", "frases": [
        "Los Caballeros Negros eran la fuerza principal del ejército de Messmer. Su comandante, Andreas, había seguido a su señor desde el Árbol Áureo, y le era devoto. Hasta que se enteró.",
        "Su ceniza de espíritu lo cuenta así: se rebeló tras conocer la naturaleza reptiliana de su señor. Por ello, fue encarcelado en una tumba subterránea.",
        "Y no fue solo. Su hijo Huw, capitán de los Caballeros Negros, siguió a su padre en la rebelión contra Messmer. Y al igual que él, fue encarcelado en una tumba subterránea.",
        "Un padre y un hijo, encerrados bajo tierra por descubrir lo que era su señor. Y la descripción de Huw termina con una línea preciosa: Messmer lloró la pérdida de un hermano de armas.",
        "Lloró. Pero no lo sacó de la tumba. [short pause] Los sacaste tú. Sus cenizas son invocaciones, y los pusiste a pelear por ti.",
        "Los soldados rasos lo tenían peor. Las Cenizas de soldado de Messmer cuentan que pertenecían al vil batallón penitenciario, y que fueron enterrados fuera de la vista del Árbol Umbrío.",
        "Su armadura lleva un grabado de oro. Un pequeño consuelo, dice, para quienes están obligados a combatir sin gracia ni honor. Y el casco de los Caballeros Negros todavía apesta. Quizá a la sangre que lo salpicó. O al alma ennegrecida de su portador, tras una matanza sin fin.",
        "Por el Reino de las Sombras quedan almas de esos soldados, rezándole a Márika. Una le pide a la reina que abrace a su hijo y les mande una señal. Y le pregunta cuánto más tiene que durar esta guerra santa.",
        "Nadie le contestó. [short pause] Ni la madre, ni el hijo.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. [short pause] El sabio que quemó más que nadie.",
        "Entre los Caballeros de Fuego había un sabio. Se llamaba Salza, y era discípulo del sabio Wego. Un hombre de libros en un ejército de antorchas.",
        "Su hechizo, la Lluvia de fuego, lo describe con una frase que empieza como un elogio. Salza siempre mantuvo su desdén al barbarismo. [short pause] Incluso a pesar de quemar más aldeas y calcinar más tierras que nadie.",
        "Más que nadie en todo su ejército. En el ejército del Empalador, el que más quemó fue el que despreciaba la barbarie. Imagina cómo eran los demás.",
        "Porque en el Árbol Áureo el fuego estaba prohibido. La Chispa aromática lo recuerda: aunque el fuego estaba prohibido entre aquellos que servían al Árbol Áureo, con el avance de la guerra esta regla fue dejándose de lado.",
        "La Grasa de fuego de Messmer lo confirma: el fuego era un símbolo de la cruzada, e incluso los soldados rasos de Messmer lo usaban. Y la Botella de perfume ígneo dice que hasta los perfumistas fueron. No a curar: la cruzada fue una purga violenta en la que participaron como guerreros.",
        "Y aun así, hubo una cosa que no quiso quemar. Su capucha lo cuenta: se negó a quemar unas ruinas antiguas, incluso a pesar de jugarse la vida.",
        "Jugarse la vida. Alguien quería esas ruinas convertidas en ceniza, y decir que no podía costarte la cabeza. El juego no dice quién lo ordenó. Dice para quién quemaba Salza las aldeas.",
        "Las ruinas más famosas del reino son las Antiguas ruinas de Rauh: gigantescas, inundadas y divididas en dos por un abismo.",
        "Y la llama de Messmer acabó llegando a ellas igual. La Yesca de Messmer, la llama que arde en su interior, sirve justo para eso: quema el árbol sellado que se dice que se encuentra en las antiguas ruinas de Rauh. [short pause] ¿Y quién le prendió fuego? Tú.",
    ]},
    {"id": "p4b", "frases": [
        "Salza no estaba solo. La Caballera de Fuego Hilde era una gran amiga del sabio Salza, y se unió a quienes insistieron en preservar los especímenes. Sus cenizas se consagraron como amuleto para proteger el almacén.",
        "Ese almacén es el Almacén de especímenes, dentro de la Fortaleza sombría. Unos caballeros tuvieron que insistir para que lo que guardaba no acabara en la hoguera.",
        "Hasta una iglesia acabó en llamas. La santa del brote, Romina, alzó una vez el brote en silencio, en una iglesia que ardía. Ojo: el juego no dice quién quemó esa iglesia. Solo dice que ardía, en un reino que, según el propio juego, fue calcinado por la llama de Messmer.",
        "Y antes de seguir, dos comentarios. David escribe que, a su edad y con sus responsabilidades, ya no puede jugar leyendo descripciones de objetos e interpretándolas. Que así es como entiende la historia, y que lo agradece.",
        "Y Quixilero dice que diez videos de este canal le han enseñado más de Elden Ring que el propio Elden Ring.",
        "David, para eso estamos: nosotros leemos las descripciones, tú pones las responsabilidades. [short pause] Y Quixilero, eso no se lo digas a Miyazaki. Bastante tiene con la descripción de cierta sopa de escorpión. Ya llegaremos.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. [short pause] Los dioses colgados de sus lanzas.",
        "Quaerens nos escribió que de Messmer tenía que haber mucho de qué hablar, porque su propio apodo lo dice: el Empalador.",
        "Tiene razón. Y casi nadie sabe de dónde sale el apodo. No sale de empalar soldados. Sale de lo que hizo con los dioses de otro pueblo. En el tráiler de la expansión, Leda lo resume así: una purga sin Gracia ni honor. La tiranía de la llama de Messmer.",
        "Los cornamentados tenían bestias divinas, mensajeras de los cielos. Y en Belurat, el asentamiento de la torre, todavía queda una. La Bestia divina León Danzante.",
        "Cuando la vences, te deja un hechizo, el Tornado de bestia divina. Y la descripción de ese hechizo dice exactamente esto.",
        "La mayoría de las bestias divinas fueron destripadas y colgadas en las lanzas de Messmer, antes de ser calcinadas en sus llamas. Quienes lo vieron lo comparan con una pira funeraria para la propia torre.",
        "Las destripaban, las colgaban y después las quemaban. [short pause] Y en japonés, el verbo de esa descripción es empalar, el mismo de su título. Messmer no es el Empalador por sus enemigos. Es el Empalador por los dioses de los demás.",
    ]},
    {"id": "p3b", "frases": [
        "El León que tú mataste fue de los que quedaron. Su Recuerdo lo cuenta: al asaltar la torre el ejército del Empalador, el ritual de la danza del león tomó tintes marciales.",
        "Una danza sagrada que tuvo que aprender a pelear. [short pause] Y no bailaba sola. Antes del combate, una anciana cornamentada le canta a la bestia.",
        "Le pide que eche raíces en los guardianes esculpidos de la torre. Que baile, y que limpie todo lo que atormenta a la torre. Que limpie a la vil progenie de la ramera.",
        "La ramera es Márika. Y su progenie, los hijos de Márika. [short pause] La bestia que te tocó matar era la plegaria de una anciana contra el Empalador.",
        "Y cuando te llevas su máscara, la Cabeza de bestia divina, su descripción termina así: ya no responde a las sinceras plegarias de la anciana.",
        "Messmer colgó a sus dioses de las lanzas. Y tú te llevaste la cabeza del último.",
    ]},
    {"id": "p3c", "frases": [
        "Y hablando de cosas que no son lo que parecen, un comentario. Pascual nos escribió: con tanto uso de ejemplos modernos, no me cabe duda de que este texto lo elaboró una IA.",
        "Tienes toda la razón del mundo, Pascual. En este canal hay inteligencia artificial, y nunca se lo hemos escondido a nadie. Y lo de los ejemplos modernos, anotado: desde hoy, nada de comparaciones de este siglo.",
        "Así que no diremos que Messmer era un jefe tóxico con su plantilla. [short pause] Diremos que era un señor feudal con una política de recursos humanos muy subterránea.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. [short pause] La sopa fría de la abuela.",
        "De todo el pueblo que quemó Messmer, el juego solo te deja hablar con una víctima. Es la anciana del canto, la Anciana cornamentada. Y la encuentras encerrada en un almacén de Belurat.",
        "Cuando entras, te confunde. Por tu aspecto, cree que eres otro peón de Messmer. Te pregunta si los tuyos nunca se cansan. Qué les sigue fascinando de sus viejos huesos.",
        "Y luego lo suelta todo de una vez. Que sus tierras fueron incendiadas por los tuyos. Que su torre quedó cubierta de sombra por los tuyos. Que vinisteis a robarlo todo y a arruinarlo todo. Y que si no os habéis regodeado ya bastante.",
        "Por esa ciudad encuentras un objeto de comida. El Potaje de escorpión: escorpión cocido en una sopa negra, receta típica de los cornamentados. Y su descripción termina así.",
        "Antaño la preparaban con mimo las abuelas de la familia. Al haberse enfriado hace tiempo, esta sopa desprende un olor rancio y agrio.",
        "Una sopa que alguien hizo con cariño para una familia. Y que se enfrió hace mucho. [short pause] El juego no dice por qué nadie llegó a comérsela. No le hace falta.",
    ]},
    {"id": "p2b", "post": 8.2, "frases": [
        "La anciana tenía un hijo. Es el Cornamentado, el guerrero de los cuernos del grupo de Miquella. En aquel video le llamamos Cornudo. Mal. Se llama el Cornamentado, y lo único que busca es venganza.",
        "La anciana te pide que su hijo te acompañe a la guerra, y que te vengues de Messmer y de los suyos. Y si ayudas al Cornamentado a llegar hasta él, entra en la arena diciéndole esto. Escúchalo.",
    ]},
    {"id": "p2c", "frases": [
        "Messmer, enemigo de mi amado pueblo. En venganza por las llamas empuño mi espada.",
        "Y en plena pelea le pregunta si ahora lo entiende: el sufrimiento de su clan, su dolor, todo lo que sintieron. Tu fealdad, le dice.",
        "Cuando Messmer cae, el Cornamentado te cuenta que le vio la cara, y que era una maraña de serpientes. Y que cómo se atrevió a llamarlos salvajes, si él era el más vil de todos. En japonés no dice salvajes. Dice inmundicia.",
        "Y si no llega a vengarse, sus últimas palabras son para su familia: oh madre, oh amadísima esposa e hijo.",
        "En la Llanura de las Tumbas, junto a las Ruinas calcinadas, queda el alma de alguien de ese pueblo. Dice que todos ardieron, que los quemaron Messmer y los suyos. Que qué hicieron para merecer eso, si solo vivían su vida en paz.",
        "Ojo, que aquí no hay santos. La caballera Leda te lo recuerda: fue la reina Márika la que ordenó a Messmer purgar al pueblo de la torre, una limpieza por fuego. Pero también te dice que los cornamentados nunca fueron santos. Simplemente quedaron del lado perdedor de una guerra.",
        "Aun así, la sopa se enfrió. [short pause] Y el Mayal de serpiente, un arma de su ejército, deja claro el método: algunos del ejército de Messmer usaron estos mayales para quemar a los cornamentados y marcarlos con agonía y miedo.",
        "Y en la torre encuentras la Túnica de cordón trenzado, la ropa de los cornamentados en busca de venganza. El cordón trenzado une el juramento del vengador al rencor de las víctimas. Jamás debe deshacerse.",
    ]},
    {"id": "subs", "frases": [
        "Antes del número uno, varios comentarios que se ganaron su sitio. Shiro buscaba algo que ver para hacerse wey en el trabajo, y nos da las gracias. Runita, nos llama.",
        "Shiro, tu jefe no se va a enterar por nosotros. [short pause] Ulises entró a escuchar música mientras trabajaba, y en cinco días ya se vio todos los videos del canal. Y Daniel nos sigue desde el primer video que subimos.",
        "A día de hoy ya somos mil trescientos suscriptores en el canal. Gracias de corazón. Aun así, de cada cien vistas de estos videos, menos de nueve son de gente suscrita. El siguiente objetivo son dos mil.",
        "A los Caballeros de Fuego, jurarle lealtad a Messmer les costó la casa. Aquí solo es un botón. [short pause] Y todos los comentarios se leen, uno por uno: con ellos se decide lo que viene.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. [short pause] La medalla que llevaste colgada.",
        "Las otras cuatro las hizo él. Esta la llevaste tú.",
        "En Belurat, la misma ciudad de la anciana, te invade un espíritu rojo: el Caballero de Fuego Queelign. Cuando te mata, le grita a la reina Márika que mire, que ha extirpado a otro. Otro cáncer de su alegría. [short pause] El cáncer eras tú.",
        "Queelign quería ser como su señor. Reforjó su espadón con la forma de la lanza de su soberano, con la esperanza de ser un segundo empalador.",
        "Y si le entregas el Iris de la Gracia, te regala sus cenizas de espíritu. Dicen que empala al enemigo en fuego para alejar a la bella madre Márika de la impureza. Y que, una vez salvado, lo único que le quedaba era la guerra.",
        "Cuando lo vences, te deja un talismán. Casi todo el mundo se lo puso sin leerlo, porque el efecto es muy bueno. La Insignia de cruzada.",
        "Talismán con una lanza alzada sobre un fondo llameante, en recuerdo de los caídos en la cruzada sagrada liderada por Messmer. Aumenta la potencia de ataque tras derrotar a un enemigo.",
        "Y sigue. Los cruzados olvidaron el honor y la piedad para empalar y quemar sin misericordia a quienes consideraban impuros. Quienes se sentían estimulados por los gritos de muerte eran los mismos que abogaban por la santidad de la campaña.",
    ]},
    {"id": "p1b", "post": 8.9, "frases": [
        "Léelo otra vez. Aumenta el ataque tras derrotar a un enemigo. El efecto del talismán es la frase: cada vez que matas, te crece la fuerza. Como a ellos con los gritos. [short pause] Rico, esta era la medalla.",
        "Y ahora la pregunta importante. ¿Quiénes eran los impuros? Messmer te lo dice a la cara en cuanto entras en su sala.",
        "Te llama intruso sarnoso. Dice que eres un Sinluz, según parece. Y le pregunta a su madre si su verdadero señorío sanciona a alguien tan despojado de luz. Escúchalo.",
    ]},
    {"id": "p1c", "frases": [
        "Te llama despojado de luz. [short pause] Y ahora vuelve a la frase del principio: quienes se ven despojados del don del oro deberán hacer frente a la muerte.",
        "La cruzada no era solo contra un pueblo. Era contra todo el que no tuviera la gracia del oro. Y tú eres un Sinluz: la definición exacta. Llevabas al cuello la medalla de una cruzada que existía para matarte.",
        "Y para rematarlo. Por el Reino de las Sombras recoges la Runa de Márika: restos dorados de la Gracia concedida personalmente por la reina Márika a los héroes que se unieron a la cruzada por ella. [short pause] Y tú la rompiste para cobrar ochenta mil runas.",
        "Messmer lo dejó escrito en su propia armadura. Por deseo de su madre, se convirtió en un símbolo aterrador para llevar a cabo la cruzada purificadora que ella ansiaba. Y debajo, una frase entre comillas: centra en mí, y solo en mí, tus maldiciones, tu ira y tu pesar.",
        "Y aquí va el último comentario de hoy. Retos nos escribió: sinceramente, el juego me parece malísimo, junto con Nightreign, aunque el lore está bien.",
        "Coincidimos en lo importante, Retos: el lore está bien. Para todo lo demás, no hace falta que lo juegues; ya nos lo pasamos nosotros por ti. [short pause] Y Messmer te daría la razón. Él tampoco quería que nadie entrara en su reino.",
    ]},
    {"id": "cierre", "post": 8.0, "frases": [
        "Esa es la lista. Sus propios caballeros, encerrados en una tumba por descubrir que su señor era una serpiente. Un sabio que quemó más aldeas que nadie. Los dioses de otro pueblo, colgados de sus lanzas. Una sopa que se enfrió esperando a una familia. Y una medalla para los que disfrutaban los gritos, que te colgaste tú.",
        "Pero hay una última cosa que llevaste en el inventario. La Bendición de Márika: una medicina especial bendecida por la reina, que te cura todo de golpe. En inglés y en japonés, su descripción termina así: Márika hizo varias de estas medicinas para Messmer. Y nunca más.",
        "La madre que le arrancó el ojo y lo escondió en el Reino de las Sombras le hizo medicinas una vez. Y después de eso, nunca más volvió a hacerlo. [short pause] Y te las bebiste tú.",
        "Su Recuerdo lo cierra así: oculto junto al pecado original, su odio fue creciendo. Y cuando por fin lo vences, su último aliento no es para ti. Es para ella. Escúchalo.",
    ]},
    {"id": "cierreb", "frases": [
        "Madre. Márika. Una maldición caerá sobre ti. [short pause] Es la única vez en todo el combate que la llama por su nombre.",
        "Messmer quemó un reino entero por su madre. Y lo último que le dejó fue una maldición.",
        "Santiago, que nos pidió a Messmer hace semanas, ya está votando por el siguiente: Bayle el Temible. Ulises lleva días pidiéndolo también. Y en los comentarios siguen Rennala, Maliketh, Parches, y el Zampaheces con Gideon. Dinos cuál quieres.",
        "En el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn, Morgott, Mohg, Godrick, Godfrey, Rykard, y las tuyas. Suscríbete, que vamos por los dos mil.",
        "Y si te gustan los mundos donde hasta los dioses tienen las manos sucias, Crónicas de Tamriel, nuestro canal hermano, cuenta los secretos de Skyrim. Te lo dejo aquí al final.",
        "Y la próxima vez que un talismán te dé más fuerza por cada enemigo que matas, léelo antes de ponértelo. [long pause] A lo mejor la medalla es de los que te estaban buscando.",
    ]},
]
CER_MAX_POR_FRASE = {'introb_6': 0.01, 'p5b_2': 0.017, 'p5b_3': 0.016, 'p4_1': 0.028, 'p4_7': 0.016, 'p4b_0': 0.019, 'p4b_3': 0.002, 'p4b_4': 0.026, 'p4b_5': 0.025, 'p3_1': 0.023, 'p3b_3': 0.021, 'p2_4': 0.002, 'subs_0': 0.025, 'subs_1': 0.002, 'p1c_4': 0.036, 'cierre_2': 0.002, 'cierreb_0': 0.014, 'cierreb_2': 0.023, 'cierreb_3': 0.063}
GAP_MAX_POR_FRASE = {'introb_6': 0.94, 'p5b_2': 0.42, 'p5b_3': 0.76, 'p4_1': 0.58, 'p4_7': 0.58, 'p4b_0': 0.53, 'p4b_3': 0.52, 'p4b_4': 0.09, 'p4b_5': 0.69, 'p3_1': 0.5, 'p3b_3': 0.87, 'p2_4': 0.57, 'subs_0': 0.59, 'subs_1': 0.93, 'p1c_4': 0.52, 'cierre_2': 0.8, 'cierreb_0': 0.93, 'cierreb_2': 0.48, 'cierreb_3': 0.35}
TAIL_MAX_POR_FRASE = {'introb_6': 1.17, 'p5b_2': 0.57, 'p5b_3': 0.52, 'p4_1': 0.57, 'p4_7': 0.69, 'p4b_0': 0.74, 'p4b_3': 1.11, 'p4b_4': 0.43, 'p4b_5': 0.74, 'p3_1': 0.52, 'p3b_3': 0.63, 'p2_4': 1.1, 'subs_0': 0.96, 'subs_1': 1.03, 'p1c_4': 0.94, 'cierre_2': 1.02, 'cierreb_0': 0.7, 'cierreb_2': 0.7, 'cierreb_3': 1.06}
