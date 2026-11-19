# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Godfrey QUE IGNORASTE» (19-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + pantallas + MG de mg_er; docs/estilo_secuencia_yt.md).
Tema más pedido en los comentarios (John, Carl; ≤ 10 días: @iRyans y @isaackbradleyfreegamer3168). ≈ 25 min.
Voz «el Profeta» de ElevenLabs, PLANA. Sin patrocinio. OST oficial (audio/ost, armar_musica_ost.py).
Investigación: _investigacion/dossier.md. Los diálogos de Godfrey verificados SOLO en inglés se PARAFRASEAN (sin comillas en
pantalla); las citas textuales son descripciones de objeto y ecos de Márika en español verificados ([ES-wiki]/[EG]).
Críticas con contraburla (regla 11-nov, mínimo 2-3): @zzzz_19239 (Miquella «toda inocente», intro), @morenojacobo… (la Aguja
de Miquella, p3b; verificado en la wiki: se usa en la arena de Placidusax en Farum Azula), @nibaldzYTAL («flojo… con IA», p1b;
nunca se niega la IA). Agradecimientos: Antonio, Esteban (p4b) · Marcelo, Ulices, Ghost, Auren (subs).
Sonidos nombrados = tramo audible con `post` (regla 31-oct): p3b («Hace mucho tiempo, Morgott»), p1b («Hoarah Loux. ¡Guerrero!»).
"""

TITULO = "Las 5 peores atrocidades de Godfrey QUE IGNORASTE"
ARCHIVO = "er_godfrey_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
# el Profeta (ElevenLabs God - Deep, Powerful). Corchetes SOBRIOS: nada de risas ni alegría (el usuario, 11-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {"Miquella": "Miquéla"}   # 12-nov: el acento va en «que»

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={**{f"scene-{n:03d}": .06 for n in (41, 42, 50, 51, 93, 94, 106, 109)},    # contador FPS verde arriba a la derecha (Games from Mars)
                 **{f"scene-{n:03d}": .05 for n in (82, 143, 144, 145, 146, 147, 148)}},  # logo del canal abajo a la derecha + borde (Draknalor186)
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar", "Shirrako"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Primer Señor del Círculo. Rey de la era dorada. Marido de la reina Márika, padre de Godwyn, y abuelo de casi toda la familia que te pasaste el juego matando.",
        "Todo el mundo lo recuerda como el gran guerrero que vuelve a casa al final del juego. El que te llama valiente antes de caer.",
        "Pero en las descripciones de sus propias armas hay un clan entero borrado del mapa, un pueblo mandado a morir lejos, dos hijos encerrados bajo tierra y una especie entera que ya no existe.",
        "Y la número uno la comete delante de ti, en el último combate del juego. [short pause] Casi nadie se dio cuenta, porque estaba demasiado ocupado esquivando el hacha.",
        "Este video lo pidieron ustedes. Ryans lo pidió en un comentario muy corto: que el próximo video fuera de Godfrey y de su hijo Godwyn. E Isaac pidió la tragedia de Godwyn y la noche de los cuchillos negros.",
        "Godwyn tendrá su turno, Isaac. Hoy toca el padre. [short pause] Y créeme, el padre tiene mucho más que esconder.",
        "Antes de empezar, una corrección. En el video de Miquella alguien escribió: qué atrocidades va a hacer ella, si es toda inocente, la mejor waifu del gaming.",
        "Ella es él. Miquella es un chico. [short pause] Y que lo defiendas sin saber ni eso es justo su poder, el encanto. Te alcanzó a ti también, a través de la pantalla.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. [short pause] El coleccionista de reinos.",
        "Todo el mundo se acuerda de Godrick en el Castillo de Velo Tormentoso, en la Colina Tormentosa. Es el primer gran castillo del juego. Lo que nadie se pregunta es de quién era ese castillo antes de que llegaran los dorados.",
        "La corona de Godfrey lo cuenta en su descripción. La era del Árbol Áureo empezó en mitad de un enfrentamiento, cuando Godfrey era el señor de la Batalla. Se enfrentó solo al señor de la Tormenta.",
        "Del señor de la Tormenta no queda nada: no queda su nombre, no queda su cara y no queda ni siquiera una tumba. Nadie en todo el juego sabe quién era. Lo único que se sabe de él es quién lo venció.",
        "Y en el castillo, el que fue suyo, todavía cuelga un retrato enorme. Godfrey, con el león Serosh a la espalda. [short pause] Es como entrar en la casa de alguien y encontrar el retrato del que la invadió encima de la chimenea.",
        "Hasta los halcones lo recuerdan. Las cenizas de un halcón al que todos los demás veneraban como soberano hablan de los días en que los vientos de Velo Tormentoso todavía rugían como ningún otro.",
        "Todavía. [short pause] Hoy esos vientos ya no rugen. El juego no dice quién calló la tormenta. Pero el único que se enfrentó a su señor lleva corona.",
    ]},
    {"id": "p5b", "frases": [
        "Y luego está la Península del Llanto. Al sur, el Castillo de Morne, y junto a su entrada, un monumento de piedra con una espada clavada.",
        "Su inscripción dice así. El asedio al castillo de Morne. Un héroe solitario lucha en busca de venganza, solo para terminar en manos del señor Godfrey.",
        "¿Venganza de qué? La respuesta está dentro del castillo, en la espada más famosa de Morne: el Espadón de hoja injertada.",
        "Arma de vengador que carga con océanos de ira y arrepentimiento. Un solitario campeón, superviviente de un país desaparecido, reclamó las espadas de todo un clan de guerreros.",
        "Un país que desapareció, y un clan entero de guerreros. El único que quedó vivo soldó las espadas de sus muertos en una sola, para vengarlos a todos de una vez. [short pause] Y aun así, terminó en manos del señor Godfrey.",
        "Hoy esa espada la empuña el Bastardo leonino, el jefe del castillo. Y la habilidad del arma todavía se llama Juramento de venganza. El juramento sigue en pie. El clan, no.",
        "Y aquí está lo que casi nadie lee. ¿Cuándo pierde Godfrey la gracia? Su corona lo dice: al fin llegó el momento en el que cayó su último enemigo. Fue en ese instante cuando se desvaneció el color de sus ojos.",
        "No la pierde por una derrota. Un monumento en la frontera de Caelid lo confirma: sus ejércitos dorados permanecen invencibles e incólumes. [short pause] La pierde cuando ya no le queda nadie a quien matar.",
        "Sus guerreros de la Tierra Baldía llevaban en la frente la Cinta de campeón. Prueba de que el portador ha asesinado a innumerables enemigos, siguiendo el ejemplo de su líder, Hoarah Loux. [short pause] El ejemplo era él.",
        "Si te sorprendió que el primer rey del juego perdiera la gracia por quedarse sin víctimas, suscríbete. Lo que viene después es peor.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. [short pause] La Larga Marcha de los Sinluz.",
        "¿Alguna vez te preguntaste por qué eres un Sinluz? Por qué no tienes la gracia, por qué te llaman así, y por qué vuelves cada vez que mueres. [short pause] La respuesta tiene nombre propio: pregúntale a Godfrey.",
        "En Necrolimbo, en la Tercera iglesia de Márika, Melina te deja oír un eco de la reina. Y en ese eco, Márika le habla a su marido.",
        "Mi señor. Os despojo a ti y a tus hombres de la Gracia. Con la mirada teñida de oscuro, seréis expulsados de las Tierras Intermedias. Guerrearéis en una tierra lejana, donde viviréis y moriréis.",
        "No es solo él. Son él y sus hombres. El Recuerdo de Hoarah Loux lo confirma: cuando fue despojado de su Gracia y se transformó en un Sinluz, abandonó las Tierras Intermedias en compañía de los suyos.",
        "Y los suyos lo siguieron sin una queja. El Talismán con hacha cuenta que el señor que lideró la Larga Marcha portaba un hacha, y que sus leales guerreros le rindieron homenaje portando una ellos también.",
        "Un pueblo entero que se va a guerrear a otra tierra, a morir allí, porque su rey ya no tiene a nadie a quien matar en esta. [short pause] Y a ellos nadie les preguntó nada.",
    ]},
    {"id": "p4b", "frases": [
        "Pero el eco tiene una segunda parte. En la Iglesia de la peregrinación, en la Península del Llanto, Márika les hace una promesa.",
        "Tras vuestra muerte, os devolveré lo que un día quise para mí. Regresaréis a las Tierras Intermedias, guerrearéis y blandiréis el Círculo de Elden. Fortaleceos ante la amenaza de la muerte, guerreros de mi señor Godfrey.",
        "Léelo otra vez. Primero morís. Después volvéis. Y cuando volváis, a pelear otra vez. [short pause] Eso no es un premio. Es un contrato de guerra sin fecha de fin.",
        "Hasta el Ancla oxidada guarda un trozo de esa marcha: cuando los Sinluz salieron de las Tierras Intermedias con su señor, dicen que solo quedó un único barco.",
        "Y la Larga Marcha terminó como terminan las guerras de Godfrey. Su hacha se rompió en la batalla que libró como líder de los Sinluz. Y cuando la marcha tocó a su fin, renunció a la corona para ser de nuevo un simple guerrero.",
        "Al principio del juego, la intro lo nombra entre los muertos que vuelven: Hoarah Loux, el caudillo de la Tierra Baldía. Y luego te habla a ti. Alzaos, Sinluz, es el momento. Vosotros que habéis muerto, pero vivís.",
        "Ahí está la atrocidad que ignoraste. Tú eres parte de ese trato. [short pause] Cada vez que mueres y vuelves a la gracia, estás cobrando la promesa que Márika le hizo al ejército de Godfrey. Morir, volver y pelear. Para siempre.",
        "Y hablando de volver. Antonio escribió que está suscrito desde que vio el primer video. Y Esteban dice que le encanta cómo agarramos los comentarios para cerrar cada video.",
        "Esteban, hoy los agarramos desde el principio. [short pause] Todos se leen, uno por uno, y con ellos se decide lo que viene.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. [short pause] Padre del año.",
        "Godfrey y Márika tuvieron hijos. Godwyn el Dorado, el semidiós al que todos querían. Y dos gemelos, Morgott y Mohg.",
        "Los gemelos nacieron augurios, con cuernos. Y en la capital del Árbol Áureo, nacer augurio es nacer maldito.",
        "Un muñeco que encuentras en el Subsuelo de los marginados, bajo la capital, lo explica sin rodeos. A los hijos de los augurios se les extirpan los cuernos, por lo que la mayoría perecen.",
        "Y el muñeco lleva escrita la súplica de un niño: por favor, te ruego que no me odies ni me maldigas.",
        "Pero los gemelos no eran hijos de cualquiera. Eran hijos del rey. Y para ellos, hay otro muñeco: el Párvulo maldito de la realeza.",
        "A los hijos de augurios nacidos en la realeza no se les extirpan los cuernos. Se los oculta bajo tierra, sin que nadie lo sepa, encarcelados para toda la eternidad.",
        "Bajo la capital. Bajo el trono de su padre. Y el Grillete de Mohg dice con qué los ataban: un amuleto bañado en magia dorada, creado para mantener a uno en particular bajo un confinamiento muy estricto. [short pause] Magia dorada. El color de la familia.",
    ]},
    {"id": "p3b", "post": 4.0, "frases": [
        "El juego no dice quién firmó esa orden. Ni Godfrey ni Márika aparecen con la pluma en la mano. Pero hay algo que sí se sabe: dónde estaba el padre.",
        "De campaña, matando hasta quedarse sin enemigos. Y después, en el exilio, al otro lado del mar. Mientras sus hijos crecían en las cloacas de su propia capital.",
        "Morgott salió de ahí abajo y se hizo rey de los augurios. Defendió el Árbol Áureo y la capital de su padre durante toda la ausencia de su padre. Su recuerdo lo dice: jamás recibió ninguna muestra de afecto por ello, pero aun así, él amó.",
        "¿Y a quién mataba Morgott en las puertas de la capital? A los Sinluz que volvían. [short pause] La gente de su padre.",
        "Su gemelo Mohg tomó el otro camino. Su Gran Runa lo dice: Mohg y Morgott eran gemelos, por lo que sus runas son similares, pero la de Mohg está empapada en sangre maldita, desde su devoción por el condenado lodazal en el que nació. [short pause] Uno amó al reino que lo encerró. El otro se fue a adorar la sangre.",
        "Cuando Godfrey por fin regresa, al final del juego, Morgott ya está muerto. Lo mataste tú. Y su primera frase al pisar el trono no es para Márika. Es para su hijo. Escúchalo.",
    ]},
    {"id": "p3c", "frases": [
        "Hace mucho tiempo, Morgott. Eso es todo. Ni un perdón, ni un gracias por guardarle la casa.",
        "En los archivos del juego quedó una línea que nunca llegó a la versión final: perdóname, Morgott. [short pause] La cortaron.",
        "Y ya que estamos debajo de la capital, ahí abajo también está la Llama Frenética. En el video del Sinluz, Moreno nos corrigió: no se puede cancelar el final de la llama frenética con la aguja, así que solo quemaste el Árbol Áureo.",
        "Moreno, en una cosa sí tienes toda la razón del mundo. No se puede en cualquier sitio. La Aguja de Miquella solo funciona en el corazón de la tormenta, en Farum Azula, frente a un dragón antiguo. Ahí, sí se puede.",
        "Lo sabe todo el que la usó. [short pause] Los demás todavía tienen los ojos amarillos.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. [short pause] Acaba con los gigantes.",
        "Al noreste del mapa, en los Picos de los gigantes, hay nieve, ruinas enormes y un silencio muy raro. Es porque los dueños ya no están.",
        "En la Primera iglesia de Márika, arriba en los Picos, hay otro eco de la reina. Esta vez es una orden. Recuérdalo, mi señor Godfrey. Elogiamos tus actos.",
        "Acaba con los gigantes con tu espada y confina la llama en lo alto de la montaña. Permite que empiece una nueva era. Una era rebosante de vida.",
        "Una era rebosante de vida, que empieza acabando con una especie entera. Y Godfrey cumple. Su corona lo resume en una línea: lideró la guerra contra los gigantes.",
        "El Medallón de rugido dice que en la antigüedad los gigantes eran enemigos mortales del Árbol Áureo. Y el Aplastagigantes, un martillo hecho de un pedrusco para esa guerra, lo dice más corto: después de que los gigantes desaparecieran, para dar paso a las guerras de los hombres.",
        "Desaparecieran. [short pause] Esa es la palabra que eligió el juego.",
        "Y no lo hizo solo. Los caballeros de Zamor fueron aclamados como héroes en esa guerra, enemigos jurados de los gigantes de fuego. Y hasta un escudo con un rostro espantoso entre llamas tiene, según su descripción, una función instructiva: recordar el horror de enfrentarse a uno. Para que nadie olvide por qué había que exterminarlos.",
        "Cuando subes hacia la Forja de los gigantes, el campo está sembrado de cadáveres gigantescos, atravesados por estacas. Nadie te dice quién los clavó. Pero ya sabes quién dirigía esa guerra.",
    ]},
    {"id": "p2b", "frases": [
        "Y no murieron todos. Quedó uno. El Gigante de fuego, el jefe que te espera en la Forja. Su recuerdo dice que es un superviviente de la guerra contra los gigantes.",
        "Al constatar que las llamas de su forja jamás podrían extinguirse, la reina Márika lo maldijo. Oh, insignificante gigante, deberás custodiar tu llama por toda la eternidad.",
        "Mataron a su pueblo, y al último lo dejaron vivo para que hiciera de guardia. Durante eras. Solo. [short pause] Y luego subes tú, lo matas, y usas su llama para quemar el Árbol. Ni eso le dejaron.",
        "Y dentro de esa guerra hubo otra traición. Junto a la Tumba del héroe matagigantes, un monumento con espada la resume en tres líneas: los campeones combaten, los troles traicionan, el fuego es vencido y empieza la era del Árbol Áureo.",
        "Los troles descienden de los gigantes. Se pasaron al bando del Árbol. Y les pagaron con esto: la Espada dorada de trol.",
        "Espada entregada a los gigantes menores que lucharon por el Árbol Áureo durante la guerra contra los gigantes. Aunque hayan perdido la cordura, en ningún momento se separan de sus espadas, cuyo estado actual es lamentable al haberse desconchado su chapado en oro.",
        "Chapado en oro. Ni siquiera era oro de verdad. [short pause] Traicionaron a su propia sangre por una espada con baño dorado, y hoy vagan por los caminos sin cordura, sin soltarla.",
    ]},
    {"id": "subs", "frases": [
        "Antes del número uno, cuatro comentarios que se ganaron su sitio. Marcelo escribió que estos videos son magistrales, y que lo de la IA pasa a segundo plano. Ulices dice que le gustan las dos voces, pero que se queda con el profeta.",
        "Ghost los escucha como un pódcast en el trabajo, y dice que se le pasa rápido el tiempo. Y Auren dejó una reflexión: en las Tierras Intermedias solo hay víctimas y victimarios, y ni los dioses escapan del pecado. Godfrey te da la razón, Auren.",
        "Y una noticia. En estos días, Runa Caída pasó los mil suscriptores. [short pause] Mil. Gracias a cada uno de ustedes.",
        "Aun así, de cada cien que ven estos videos, solo seis están suscritos. El siguiente objetivo son dos mil. Si llevas cuatro atrocidades aguantando, suscribirte es lo menos atroz que vas a hacer hoy.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. [short pause] El finiquito de Serosh.",
        "Las otras cuatro fueron contra enemigos, contra su pueblo, contra sus hijos y contra una especie entera. Esta fue contra el único que lo aguantó durante todas esas eras. [short pause] Y encima la comete delante de ti, en tu propia cara.",
        "Serosh. El león que Godfrey lleva a la espalda en todos sus retratos. Su título es Serosh, Señor de las Bestias. Y no estaba ahí de adorno.",
        "El Icono de Godfrey lo explica. Godfrey era un feroz guerrero. Cuando juró sus votos para convertirse en Señor, comenzó a llevar a la bestia regente Serosh a sus espaldas, con el fin de calmar el incesante deseo de batalla que ardía en su interior.",
        "Y ese icono lo guarda Godefroy, el Injertado, en una prisión eterna de la Meseta Altus. Otro del linaje dorado, cosido con brazos ajenos como Godrick. Hasta para contarte quién era su abuelo, la familia lo hace con miembros robados.",
        "Serosh era su freno. El Gran martillo de garras bestiales, el que te da Gurranq, lo llama regente del rey Godfrey. Y un escudo con su blasón da el consejo que Serosh le repetía cada día: lucha con pasión, pero no seas su prisionero.",
        "Ese león dorado con su jinete se volvió el símbolo de toda una época. La Armadura leonina de Radahn dice que el león simboliza a Godfrey y a su bestia regente, y que desde su juventud Radahn quedó fascinado por el Señor de la Batalla. Un niño que creció admirando a los dos.",
        "Lo cargó desde que fue rey. Lo acompañó cuando le quitaron la gracia. Lo siguió en la Larga Marcha, al exilio, a la guerra lejana y a la muerte. [short pause] Una vida entera, y otra después, sujetando a un hombre que quería pelear contra todo el mundo.",
        "Y en el Trono de Elden, en la capital hecha ceniza, por fin lo ves. Godfrey vuelve con Serosh a la espalda y te anuncia su nombre. Por desgracia, aquí estoy de nuevo para reclamarlo una vez más. Yo, Godfrey, el primer Señor del Círculo.",
    ]},
    {"id": "p1b", "post": 7.0, "frases": [
        "Peleas. Y cuando Godfrey va perdiendo, pasa algo que casi nadie mira con atención. Serosh empieza a cambiar. Deja de ser un espíritu translúcido y se vuelve de carne. Se está preparando para pelear a su lado. [short pause] Por primera vez en eras.",
        "Y Godfrey lo interrumpe. Le agarra la cabeza y le dice, más o menos: ya basta. Me has servido bien, Serosh. Ya te he tenido demasiada cortesía.",
        "Y le rompe el cuello. [short pause] Al león que lo cuidó durante eras. Al que estaba a punto de dar la cara por él.",
        "En japonés la frase es todavía peor: dice que se acabó fingir buenos modales. [short pause] Serosh era los buenos modales.",
        "Bañado en la sangre de su regente, tira el hacha y grita el nombre que tenía antes de ser rey. Escúchalo.",
    ]},
    {"id": "p1c", "frases": [
        "Ahora pelea como Hoarah Loux. Guerrero. Sin freno, sin corona y sin nadie que lo sujete. Que es exactamente lo que Serosh llevaba eras evitando.",
        "Y la expansión ya te había avisado. Los guerreros de los altiplanos, su gente, son famosos como cazadores de osos, y para ellos no hay acto más glorioso que subyugar a una bestia salvaje. [short pause] Serosh era la bestia. Y llevaba toda la vida encima de él.",
        "Y aquí va el último comentario de hoy. Nibald nos escribió: no se puede ser tan flojo como para hacer el guion completamente con IA.",
        "Nibald, flojo de verdad es Godfrey. Tuvo un consejero durante eras, y en cuanto le tocó trabajar en serio, lo despidió de un crujido. [short pause] Aquí por lo menos seguimos leyendo cada descripción de cada arma, para que no tengas que hacerlo tú.",
        "Y lo mejor es lo que dice cuando por fin cae. Te mira y te dice que tu fuerza es digna de una corona. Y si es él quien te mata, te lo grita: la corona se gana con la fuerza.",
        "El Hacha de Godfrey ya lo había dejado escrito: antaño, la corona se afianzaba mediante la fuerza. Ese es, en una sola frase, todo su programa de gobierno. [short pause] Y tú se lo acabas de confirmar.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Un señor de la Tormenta del que no queda ni el nombre, y un país desaparecido. Un pueblo mandado a morir lejos, del que tú eres el último recibo. Dos hijos bajo tierra con grilletes dorados. Una especie borrada y un último gigante de guardia. Y un león que se volvió de carne para ayudarlo, y al que le rompió el cuello.",
        "Y su legado fue el linaje dorado. Que acabó en Godrick, cosiéndose brazos en Velo Tormentoso, el mismo castillo que su abuelo conquistó. Y cuando Godrick te mata, mira al cielo y le pregunta a Godfrey si lo ha visto.",
        "Sí, Godrick. Lo vio todo. [short pause] Lo empezó todo.",
        "La expansión lo remata con un talismán en la Fortaleza sombría: Godfrey recibiendo la savia del Árbol sin atisbo de vacilación. Y la descripción termina así: no debe sorprender que proyecte una larga sombra sobre las tierras. [short pause] No. No sorprende.",
        "Los comentarios se leen todos, y con ellos se decide cada video. Ya están apuntados Rykard, el Zampaheces con Gideon, Rennala, Messmer, Bayle y hasta la Voluntad Mayor. Dinos cuál quieres que sea el siguiente.",
        "En el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn, Morgott, Mohg, Godrick, y las tuyas. Suscríbete, que vamos por los dos mil.",
        "Y si te gustan los mundos donde hasta los dioses tienen las manos sucias, Crónicas de Tamriel, nuestro canal hermano, cuenta los secretos de Skyrim. Te lo dejo aquí al final.",
        "Y la próxima vez que llegues al Trono de Elden y Godfrey te llame valiente, fíjate en el león. [long pause] Él ya sabe cómo acaba.",
    ]},
]
CER_MAX_POR_FRASE = {'intro_4': 0.014, 'p1_1': 0.002, 'intro_5': 0.015, 'p5_6': 0.03, 'p5b_8': 0.026, 'p4_2': 0.022, 'p4_4': 0.027, 'p4b_5': 0.02, 'p3_1': 0.035, 'p3b_3': 0.015, 'p3b_4': 0.023, 'p3c_0': 0.016, 'p1_8': 0.002, 'p1b_0': 0.002, 'p1c_0': 0.037, 'p1c_1': 0.002, 'cierre_2': 0.035, 'cierre_4': 0.05, 'cierre_5': 0.039}
GAP_MAX_POR_FRASE = {'intro_4': 0.51, 'p1_1': 1.04, 'intro_5': 0.6, 'p5_6': 0.91, 'p5b_8': 1.02, 'p4_2': 0.49, 'p4_4': 0.59, 'p4b_5': 0.57, 'p3_1': 0.53, 'p3b_3': 0.83, 'p3b_4': 0.87, 'p3c_0': 0.43, 'p1_8': 0.57, 'p1b_0': 0.63, 'p1c_0': 0.48, 'p1c_1': 0.8, 'cierre_2': 0.59, 'cierre_4': 0.44, 'cierre_5': 0.32}
TAIL_MAX_POR_FRASE = {'intro_4': 0.67, 'p1_1': 1.04, 'intro_5': 0.46, 'p5_6': 0.71, 'p5b_8': 0.7, 'p4_2': 0.55, 'p4_4': 0.79, 'p4b_5': 0.76, 'p3_1': 1.0, 'p3b_3': 0.67, 'p3b_4': 0.86, 'p3c_0': 0.58, 'p1_8': 1.04, 'p1b_0': 1.05, 'p1c_0': 0.57, 'p1c_1': 1.04, 'cierre_2': 0.37, 'cierre_4': 0.86, 'cierre_5': 0.92}
