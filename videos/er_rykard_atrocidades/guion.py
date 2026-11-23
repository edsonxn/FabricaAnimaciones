# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Rykard QUE IGNORASTE» (22-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + pantallas + MG de mg_er; docs/estilo_secuencia_yt.md).
Tema más pedido en los comentarios (≤ 10 días: @hectorsocarras3030 «7mo intento», @uueee-gt3ci «Día 4», @zoharysakiyamablue471
«trilogía de los hijos de Rennala»). ≈ 25 min. Voz «el Profeta» de ElevenLabs, PLANA. Sin patrocinio. OST oficial.
Investigación: _investigacion/dossier.md. Diálogos verificados SOLO en inglés = PARAFRASEADOS (sin comillas en pantalla); las
citas textuales son descripciones de objeto en español ([EG]/[ES-wiki]) y la línea de Rykard «Únete a la familia del Rey Serpiente».
NO repetir lo contado en er_sinluz_atrocidades (contratos, Rencor, Camafeo, Tanith comiendo, Tónico, Daedicar, Máscara de consorte).
Críticas con contraburla (regla 11-nov): @m0h4xd_727 (gigantes = Messmer, intro; dossier § 9), @yuzovnzl («¿la IA hizo la
edición?», p3c; nunca se niega la IA), @BNETDOWN («voz sin IA», p1c). Agradecimientos: Braulio, Juan José (p4b) · Andrés,
D424, Evil Ryu, Kanintor, Wsefsd (subs).
Sonidos nombrados = tramo audible con `post` (regla 31-oct / regla 10): p3b («Join the Serpent King, as family… devour the very
gods!»), p2b (Rya: «Kill me, please»), p1b («No one will hold me captive. A serpent never dies.»).
"""

TITULO = "Las 5 peores atrocidades de Rykard QUE IGNORASTE"
ARCHIVO = "er_rykard_atrocidades"
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
    recorte_por={"scene-110": .06},    # cronómetro «00:16» arriba a la izquierda (JLBgrzC55Ss; revisión 22-nov)
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
        "Pretor Rykard. Señor de la Blasfemia. Hijo de la reina Rennala y de Radagon, hermano de Radahn y de Ranni, y dueño de la Mansión del Volcán, en lo alto del monte Gelmir.",
        "Casi todo el mundo lo recuerda únicamente por una cosa: el semidiós que se dejó comer por una serpiente gigante, y que en mitad del combate te grita: únete a la familia del Rey Serpiente. Juntos devoraremos a los dioses.",
        "Pero dejarse comer es lo que menos daño hizo. Antes de la serpiente fue juez, y tenía su propio taller de tortura. Hay máquinas que secuestran gente por todo el mapa y la dejan en su sótano. Y dejó tirada la guerra más espantosa de toda la Devastación.",
        "Y la número uno la llevaste tú en el inventario. Seguramente la usaste contra uno de los jefes más difíciles del juego, sin leer de dónde salía. [short pause] Era un pago. Por la noche en que murió un dios.",
        "Este video lo pidieron ustedes, y con mucha insistencia. Héctor lleva siete intentos pidiendo las atrocidades de Rykard, señor de la Blasfemia. Lo dice él mismo en su comentario: séptimo intento.",
        "Otro usuario nos lleva la cuenta por días, con una serpiente al final: día cuatro. Y Zohar nos pidió cerrar la trilogía de los hijos de Rennala, porque según él, este es el más cruel de los tres.",
        "Héctor, no hizo falta el octavo. [short pause] Y un aviso: en el video del Sinluz ya contamos los contratos de asesinato de Tanith y la audiencia con la serpiente. Hoy va todo lo demás, que es bastante peor.",
        "Antes de empezar, una corrección. En el video de Godfrey, alguien escribió: lo de los gigantes creo que fue Messmer.",
        "Casi. Messmer también exterminaba por encargo de su madre, pero a otros: su cruzada purificadora quemó a los cornamentados en el Reino de las Sombras. Los gigantes fueron cosa de Godfrey. Lo dice su propia corona: lideró la guerra contra los gigantes.",
        "Márika repartía las guerras de exterminio como quien reparte las tareas de la casa. Una para el marido, otra para el hijo. [short pause] Y ninguno se quejó.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. [short pause] El juez con taller de tortura.",
        "Antes de ser el señor de la Blasfemia, Rykard era la ley. Su título, pretor, es el de un magistrado. En la Mesa Redonda, Gideon Ofnir, el Omnisciente, te lo describe como un juez despiadado al mando de una compañía de inquisidores.",
        "Y añade que lo aborrecían por sus maneras de serpiente. [short pause] Eso, antes de que fuera una serpiente de verdad.",
        "Su sangre era noble. El casco de sus caballeros de Gelmir lleva un penacho de plumas rojas, símbolo del pedigrí de Rykard como hijo del señor Radagon. El rojo de Radagon, en la cabeza de sus soldados.",
        "Ahora, la casa. La Mansión del Volcán parece un palacio elegante, con alfombras, velas y una anfitriona amable que te ofrece una familia. Pero fíjate en los nombres de sus lugares de gracia.",
        "Uno se llama Iglesia de la ciudad de los penados. Otro, Cámara subterránea de la inquisición. [short pause] Nadie les pone esos nombres a las habitaciones de una casa de huéspedes.",
        "Y en esa casa, el juego te deja un objeto que lo cuenta todo. El Candelabro de inquisidor.",
    ]},
    {"id": "p5b", "frases": [
        "Instrumento de tortura utilizado en secreto contra nobles en la Mansión del Volcán del monte Gelmir. Sus numerosas púas atraviesan la carne antes de hacerla arder con las llamas del arma.",
        "El olor a sangre quemada provocaba la desesperación de la víctima. Un candelabro concebido por una mente meticulosa.",
        "En secreto, y contra nobles. No contra monstruos, ni contra herejes de la calle. Contra gente con apellido, detrás de una cortina, en la casa del juez.",
        "Y la inquisición tenía empleados. Dentro de la mansión te invade uno de ellos, el inquisidor Ghiza, armado con una rueda de hierro llena de cuchillas.",
        "La Rueda de Ghiza es un instrumento de tortura usado por el inquisidor Ghiza. El giro de la rueda provoca fuertes dolores y hemorragia.",
        "Su cara va tapada con la Máscara ensangrentada, hecha de vendas muy ceñidas y empapadas en sangre. Y su ropa es el Atuendo de oficial, la túnica de los oficiales autorizados para desempeñar su macabro oficio.",
        "Esa descripción termina con una frase que podría ser el lema de la mansión entera. Ejecuciones, rituales truculentos. Las tareas más oscuras mueven los engranajes de la humanidad.",
        "Ese era Rykard antes de la blasfemia. El hombre que juzgaba a los demás. [short pause] Y la rueda de Ghiza no se quedó en la mansión. Su diseño se copió para algo mucho más grande.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. [short pause] Secuestros a domicilio.",
        "En la Academia de Raya Lucaria, en Liurnia, un personaje muy simpático te da un consejo. Es Parches, el mismo que ya te ha intentado matar más de una vez.",
        "Te habla de las vírgenes de hierro: máquinas torpes, torbellinos de hoces y ruedas con púas. Y te cuenta que hace mucho tiempo les dieron un hechizo de transposición. Que pueden llevarte muy lejos.",
        "Según Parches, en el fondo de la gran noria de la Academia queda una que todavía funciona. Si te dejas atrapar a propósito, te saca justo al pie del Árbol Áureo. [short pause] O eso dicen.",
        "Y miles de jugadores lo hicieron. Se acercaron a la máquina y se dejaron agarrar. La virgen raptora abre el pecho, te mete dentro con unos tentáculos con forma de serpiente, y no te suelta hasta que estás muerto.",
        "Y despiertas encerrado. No al pie del Árbol Áureo, sino en la Cámara subterránea de la inquisición de la Mansión del Volcán. Sin poder salir y sin poder viajar, hasta que vences a dos vírgenes raptoras más.",
        "Una gira con ruedas dentadas, y la otra balancea guadañas como un péndulo. Y cuando caen, te dejan su premio. El Candelabro de inquisidor. [short pause] El mismo instrumento de tortura de la mansión.",
    ]},
    {"id": "p4b", "frases": [
        "Y aquí se cierra el círculo. La descripción completa de la Rueda de Ghiza termina con estas palabras: su diseño se adoptó para usarlo en las emblemáticas armas blandidas por las vírgenes de hierro.",
        "La rueda del torturador del juez es la rueda de las máquinas que atrapan gente por toda la región. Y la que tú probaste te dejó en su sótano.",
        "Y no es solo la de la Academia. Hay vírgenes raptoras en la Mansión de los Caria, en el monte Gelmir, en las Afueras de la capital y dentro de la propia Leyndell. Una red de máquinas de secuestro, de punta a punta del mapa.",
        "Ojo con esto: el juego nunca dice quién las construyó. Lo que sí enseña es dónde acaban sus pasajeros. [short pause] En la cámara de la inquisición de Rykard.",
        "Y Parches lo sabía. Cuando sales del volcán, te lo dice con toda la calma del mundo: que él no había mentido en absoluto, que estabas atrapado dentro de un volcán, pero que el Árbol Áureo estaba justo ahí fuera.",
        "Más tarde, en las laderas del monte Gelmir, te empuja por un precipicio gritándote que te alejes de la Mansión del Volcán. Y luego te confiesa por qué: ha oído que los brutos de ahí cazan Sinluz como si fueran animales.",
        "Es el único consejo honesto que Parches da en todo el juego. Y te lo da después de tirarte por un barranco.",
        "Y antes de seguir, dos comentarios. Braulio dice que se volvió adicto a estos videos, la neta. Y Juan José dice que se han vuelto una parte imperdible de su día, y que ojalá algún día llegaran las atrocidades de Rykard.",
        "Juan José, ese día es hoy. [short pause] Braulio, lo tuyo no tiene cura. Pero conozco una virgen raptora que dice que te lleva directo al Árbol Áureo.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. [short pause] La guerra que abandonó.",
        "Gideon lo dice sin rodeos: el monte Gelmir, al oeste de la Meseta Altus, fue el escenario de la batalla más espantosa de toda la Devastación. De todas.",
        "Junto al noveno campamento del monte Gelmir, un monumento con una espada clavada la resume así. El asalto a la Mansión del Volcán. Lo sórdido, lo enfermizo, lo profano. Una guerra miserable interminable que no concede la gloria.",
        "El propio mapa del monte Gelmir lo advierte: sus escarpados acantilados y su clima amenazador son peligros que se agudizan aún más tras la Devastación. Todavía hoy, las laderas están llenas de campamentos en ruinas.",
        "Era su guerra. Su montaña, sus caballeros y su mansión. Y en plena guerra, el semidiós que la dirigía hizo esto. La Gran Runa de Rykard lo cuenta: Rykard se ofreció como alimento a la serpiente blasfema, runa incluida.",
        "Runa incluida. [short pause] Su fragmento del Círculo de Elden, el poder por el que todos se estaban matando, se lo entregó a la boca de una serpiente. Mientras sus hombres morían ahí fuera por él.",
        "Y sus hombres se dieron cuenta. En el camino que sube a la mansión queda el alma de uno de ellos, atrapada, hablándole a su señor. Le dice que si este campo de muerte podrido es lo que trae su blasfemia, él ya no puede seguir. Nadie puede.",
        "La Armadura de caballero de Gelmir lo deja por escrito. Muestra un emblema que ya nadie usa, puesto que representa a un señor que empezó con nobles ambiciones pero acabó cayendo en una ávida depravación. Al perder el señor su dignidad, estos caballeros también perdieron a su maestro.",
    ]},
    {"id": "p3b", "post": 10.0, "frases": [
        "Pero no todos se fueron. Algunos intentaron arreglarlo. El Cazador de serpientes, una lanza enorme, lo explica: cuando las aspiraciones heroicas del señor degeneraron hasta convertirse en mera avaricia, sus hombres buscaron un arma con la que pudieran detenerlo.",
        "Sus propios soldados, buscando un arma para matar a su señor. [short pause] ¿Y dónde está esa lanza? Clavada en un montón de cadáveres, a la entrada de la sala de Rykard. No llegaron a usarla.",
        "Y uno de ellos ni siquiera se fue después de morir. Si vuelves a la mansión varias veces, aparece el fantasma de un caballero de Gelmir. Te pide, por favor, que alguien lo mate. A esa horrible serpiente. Al pretor Rykard.",
        "Te dice que dejó la lanza matasierpes en la sala del señor. Y que las ambiciones del pretor, aunque blasfemas, lo hacían un soberano digno, pero que quedaron reducidas a una depravación glotona en cuanto se entregó a la serpiente.",
        "Y remata: lo que sea esa cosa, ya no es el pretor Rykard. Alguien tiene que matarlo, para ahorrarle a él y a sus ambiciones más deshonra. [short pause] El último leal que le quedaba te está pidiendo que lo mates.",
        "Y cuando lo haces, en el sitio donde estaba arrodillado ese caballero, te queda un gesto: dar las gracias. [short pause] Es el único habitante de esa mansión que te agradece algo de verdad.",
        "¿Y qué había dentro de la serpiente? La Hoja blasfema, la espada que Rykard saca de la boca de la bestia, lo dice: los restos de la infinidad de héroes a los que ha devorado se retuercen en la superficie de esta espada. Ahora comparten la misma sangre y están unidos como familia.",
        "En la arena, junto a la serpiente, hay un cadáver con el Sobretodo ocular. Su insignia designa a su portador como los ojos y oídos de Sir Gideon el Omnisciente. [short pause] El espía de Gideon también acabó en el menú.",
        "Y así es como Rykard te invita a su familia, en su propia voz. Escúchalo.",
    ]},
    {"id": "p3c", "frases": [
        "Familia, lo llama. Y hablando de cosas que se hacen solas, un comentario. Yuzo nos preguntó, sin odio, aclara: ¿la IA hizo la edición por ti, o soy yo?",
        "No, Yuzo, no eres tú. Aquí hay inteligencia artificial, y nunca se lo hemos escondido a nadie. [short pause] Pero no te preocupes por eso. De todo lo que sale en este video, lo más artificial sigue siendo la sonrisa de Tanith.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. [short pause] Los hijos del ritual.",
        "Rykard quería una familia. Lo repite en cada frase: familia. Y la consiguió. [short pause] Lo que nadie hizo fue preguntarle a la familia.",
        "Por las laderas del monte Gelmir y por los pasillos de la mansión se arrastran unas criaturas: los hombres serpiente, con látigos de magma. Sus cenizas de espíritu cuentan de dónde salieron.",
        "Se dice que, hace mucho tiempo, la anciana serpiente que habitaba en el Monte Gelmir devoró a un semidiós, lo cual provocó el nacimiento de los hombres serpiente.",
        "Un semidiós devorado por la serpiente del Gelmir. En todo el juego, solo sabemos de uno que se ofreció a ella. [short pause] La blasfemia de Rykard no se quedó dentro de él. Parió una especie entera.",
        "Y no salió de la nada. El Disparo de magma dice que Rykard, hijo de la reina Rennala, descubrió los antiguos maleficios de Gelmir y los volvió a poner en práctica. Resucitó una religión vieja.",
        "De esa religión queda la Espada curva de dios serpiente, una herramienta empleada en una religión olvidada que se practicaba en el Monte Gelmir. Antes, se usaba para ofrecer sacrificios.",
        "Ahora entra en el Templo de Eiglay, la iglesia de la mansión. Sobre el altar cuelga una piel de serpiente mudada. Y en el altar, después de matar al Noble sacrodermo, encuentras un objeto húmedo. El Amnios de serpiente.",
        "Amnios del útero que albergó este pobre vástago no deseado fruto de un repulsivo ritual de parto. Permanece siempre húmedo y jamás llegará a secarse.",
    ]},
    {"id": "p2b", "post": 4.5, "frases": [
        "¿De quién era ese útero? Te lo cuenta la persona que te trajo a la mansión. Rya, la chica de Liurnia que te entregó la invitación.",
        "Rya buscaba Sinluz para su señora. Y te elogió por una razón muy concreta: por tener la mano firme y el corazón firme. Despiadado, incluso con los tuyos. [short pause] Eso era justo lo que buscaban.",
        "Un día oye algo detrás de las paredes: como una respiración, o como escamas que se arrastran. Y cuando por fin se ve a sí misma, descubre que todavía es una serpiente. Que esa es su verdadera forma, y que su nombre real es Zorayas.",
        "A ella le habían contado que nació por la gracia de un rey glorioso. Y Tanith la crio como a una hija. [short pause] Pero cuando le llevas el amnios, lo reconoce. Está segura: nació dentro de eso.",
        "Lo que dice después es lo más triste de toda la mansión. Que fue una hija no deseada. Nacida no de la gracia, sino de un ritual horrible. Algo que nunca podrá ser aceptado, ni por los hombres ni por las serpientes.",
        "Que ni siquiera Tanith debería aceptarla. Y entonces te pide una única cosa, la última: que la liberes de ese cuerpo maldito. Escúchala.",
    ]},
    {"id": "p2c", "frases": [
        "Si lo haces, sus últimas palabras son para ti y para Tanith: gracias, mi adalid. Madre. [short pause] Ese es el rey glorioso por cuya gracia nació. Y esa es la hija que dejó: una criatura que solo pide morir.",
        "Y si no la matas, te deja una carta. Desea emprender un viaje, para algún día continuar el trabajo de su madre, y ser la orgullosa hija de Tanith de la Mansión del Volcán.",
        "Hasta en su mejor final, lo único que puede soñar es heredar la casa de las cámaras de tortura. [short pause] Esa es la familia del Rey Serpiente.",
        "Y la Ira de Gelmir, el hechizo que te regala Bernahl, lo resume en una frase: la arrogancia de intentar dominar el volcán es propia únicamente de hombres y víboras.",
    ]},
    {"id": "subs", "frases": [
        "Antes del número uno, varios comentarios que se ganaron su sitio. Andrés escribió que Miquella nos puso la heterosexualidad en duda. Y que le encantan estos videos.",
        "Andrés, ese es el encanto de Miquella. A Rykard, por lo menos, se le ve venir: es una serpiente gigante con la cara de un señor.",
        "Otro nos conoció con el video de Morgott, y desde entonces nos sigue. Evil Ryu dice que este fue el primer video que vio del canal, y que se va a ver los demás. Y Kanintor encontró el canal de casualidad, y se alegra mucho de haberlo hecho.",
        "Y Wsefsd celebró los mil suscriptores con una fila de letras e más larga que cualquier mensaje del suelo de las Tierras Intermedias.",
        "A día de hoy, ya somos más de mil doscientos suscriptores en el canal. Gracias de corazón. Aun así, de cada cien que ven estos videos, solo siete están suscritos. El siguiente objetivo son dos mil.",
        "Rykard te ofrecía una familia a cambio de que te devorara una serpiente. Aquí solo es un botón. [short pause] Y todos los comentarios se leen, uno por uno: con ellos se decide lo que viene.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. [short pause] La propina de la noche del complot.",
        "Las otras cuatro las hizo con el poder que ya tenía. Esta la hizo para conseguirlo. [short pause] Y tú la llevaste en el inventario.",
        "Al final del juego, en Farum Azula, la ciudad en ruinas, te invade un viejo conocido: el caballero Bernahl, el recusante de la Mansión del Volcán. Y cuando lo vences, suelta una losa con una garra grabada. La Garra blasfema.",
        "Casi todo el mundo la usó para una sola cosa: el combate contra Maliketh, la Hoja Negra. Sirve para desviar el poder de su espada. Lo que casi nadie leyó es de dónde sale.",
        "Una losa grabada con los restos de la Runa de la Muerte. En la noche del complot, Ranni recompensó con estos restos al pretor Rykard.",
        "Recompensó. En japonés la palabra es todavía más clara: es un pago en agradecimiento. [short pause] A Rykard le pagaron. ¿Y qué noche era esa?",
        "Rogier te lo contó hace mucho, en la Mesa Redonda. Alguien robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra. Y una noche funesta, asesinó a Godwyn, el Dorado.",
        "La muerte del primer semidiós. La chispa que acabó en la Devastación, y en la guerra más espantosa de todas, la de su propia montaña. [short pause] Esa noche ya la contamos en el video de Ranni. Lo que no contamos es que Rykard cobró.",
    ]},
    {"id": "p1b", "post": 10.2, "frases": [
        "El juego no dice qué hizo Rykard esa noche para merecer el pago. No dice si sujetó un cuchillo, si abrió una puerta o si solo miró hacia otro lado. Dice que le pagaron. Y que aceptó.",
        "Lo que sí dice es para qué quería el pago. La garra termina así: si algún día se revela el allanamiento, servirán como último recurso y permitirán a Rykard desafiar a Maliketh, la Hoja Negra, la oscura bestia de la Muerte Escrita.",
        "En japonés no dice allanamiento. Dice el día de la blasfemia. [short pause] El juez del Árbol Áureo, el que tenía inquisidores para castigar a los demás, ya planeaba su propia blasfemia la noche en que murió un dios.",
        "Por eso quería esa losa. Para que, el día en que la Muerte viniera por él, tuviera con qué pelearle. El mismo hombre que luego se hizo serpiente para devorar, crecer y vivir eternamente.",
        "El Recuerdo del blasfemo lo resume con una frase que nadie firma: el camino de la blasfemia es largo y peligroso, por lo que no es posible recorrerlo si no se está listo para pecar. [short pause] Rykard estaba listo desde la noche del complot.",
        "Bernahl, que cargaba la garra, te lo confirma tras la muerte de su señor: que no te guarda rencor, que los fuertes toman, y que hasta Rykard estaba preparado para un final miserable cuando abrazó la blasfemia en su propia carne.",
        "Y cuando por fin lo vences, la serpiente con la cara del pretor no te pide perdón. Te dice que nadie lo tendrá cautivo, que una serpiente nunca muere. Escúchalo.",
    ]},
    {"id": "p1c", "frases": [
        "Nunca muere, dice. Y su seguro contra la Muerte terminó en tu bolsillo, y tú lo usaste contra la Muerte en persona.",
        "Parches lo resume mejor que nadie, después de que matas a Rykard: que la mansión está acabada, que Tanith ha perdido la cabeza, y que cómo iba a acabar de otra forma, si papá ambición andaba perdidamente enamorado de la señora blasfemia.",
        "Y aquí va el último comentario de hoy. Bnet nos escribió: la verdad, estaría buena una voz sin IA.",
        "Lo pensamos, de verdad. Pero cada vez que mandábamos a un narrador de carne y hueso a la Mansión del Volcán, Tanith le ofrecía una audiencia con el señor. [short pause] Y ninguno volvió para grabar el cierre.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Un juez con un candelabro para quemar nobles en secreto. Máquinas que te secuestran a medio mapa y te dejan en su sótano. Una guerra espantosa que abandonó metiéndose en una serpiente, runa incluida. Una especie entera nacida de un ritual. Y un pago por la noche en que murió Godwyn.",
        "Y Tanith, cuando lo matas, sigue creyendo en él. Te dice que su señor aún era débil, que la derrota no es el final, y que es inmortal: que algún día volverá, más fuerte.",
        "Bernahl te deja otro recuerdo de él: el Cetro de devorador, con forma de serpiente devorando el mundo. Dicen que su diseño es una breve visión del futuro que tuvo Rykard en sus últimos momentos de vida, tras ser devorado por la gran serpiente.",
        "Una serpiente que se come el mundo. [short pause] Eso fue lo último que vio. Y le pareció bien.",
        "Con este, Zohar, la trilogía de los hijos de Rennala está completa: Ranni, Radahn y Rykard. Y en los comentarios ya está apuntada la madre, Rennala, además del Zampaheces con Gideon, Messmer y Bayle. Dinos cuál quieres que sea el siguiente.",
        "En el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn, Morgott, Mohg, Godrick, Godfrey, y las tuyas. Suscríbete, que vamos por los dos mil.",
        "Y si te gustan los mundos donde hasta los dioses tienen las manos sucias, Crónicas de Tamriel, nuestro canal hermano, cuenta los secretos de Skyrim. Te lo dejo aquí al final.",
        "Y la próxima vez que una máquina te prometa llevarte al pie del Árbol Áureo, piénsalo dos veces antes de meterte dentro. [long pause] A lo mejor tiene una rueda de Ghiza esperándote.",
    ]},
]
CER_MAX_POR_FRASE = {'intro_0': 0.04, 'intro_4': 0.021, 'p5_1': 0.03, 'p5_3': 0.027, 'p5b_3': 0.019, 'p5b_4': 0.038, 'p5b_7': 0.049, 'p4b_3': 0.028, 'p3_4': 0.049, 'p3_5': 0.016, 'p3b_2': 0.019, 'p3b_4': 0.015, 'p3b_8': 0.091, 'p3c_0': 0.029, 'p3c_1': 0.008, 'p2_1': 0.022, 'p2_4': 0.029, 'p2_5': 0.035, 'subs_1': 0.033, 'subs_3': 0.03, 'subs_5': 0.024, 'p1_4': 0.049, 'p1_5': 0.052, 'p1_6': 0.017, 'p1_7': 0.025, 'p1b_0': 0.023, 'p1b_4': 0.029, 'p1b_5': 0.018, 'p1c_2': 0.041, 'cierre_4': 0.065, 'cierre_5': 0.044, 'cierre_7': 0.017}
GAP_MAX_POR_FRASE = {'intro_0': 0.45, 'intro_4': 0.63, 'p5_1': 0.61, 'p5_3': 0.53, 'p5b_3': 0.56, 'p5b_4': 0.59, 'p5b_7': 0.93, 'p4b_3': 0.87, 'p3_4': 0.62, 'p3_5': 1.05, 'p3b_2': 0.54, 'p3b_4': 0.94, 'p3b_8': 0.48, 'p3c_0': 0.57, 'p3c_1': 0.87, 'p2_1': 0.71, 'p2_4': 0.89, 'p2_5': 0.42, 'subs_1': 0.51, 'subs_3': 0.03, 'subs_5': 0.84, 'p1_4': 0.58, 'p1_5': 0.98, 'p1_6': 0.66, 'p1_7': 0.91, 'p1b_0': 0.58, 'p1b_4': 1.09, 'p1b_5': 0.51, 'p1c_2': 0.47, 'cierre_4': 0.48, 'cierre_5': 0.15, 'cierre_7': 1.44}
TAIL_MAX_POR_FRASE = {'intro_0': 0.76, 'intro_4': 0.91, 'p5_1': 0.95, 'p5_3': 0.68, 'p5b_3': 0.55, 'p5b_4': 0.58, 'p5b_7': 0.79, 'p4b_3': 0.57, 'p3_4': 0.92, 'p3_5': 0.82, 'p3b_2': 0.78, 'p3b_4': 0.61, 'p3b_8': 0.42, 'p3c_0': 1.05, 'p3c_1': 0.83, 'p2_1': 0.62, 'p2_4': 0.72, 'p2_5': 0.78, 'subs_1': 0.65, 'subs_3': 0.4, 'subs_5': 0.88, 'p1_4': 0.64, 'p1_5': 0.73, 'p1_6': 0.72, 'p1_7': 0.93, 'p1b_0': 0.72, 'p1b_4': 0.68, 'p1b_5': 0.72, 'p1c_2': 0.97, 'cierre_4': 0.86, 'cierre_5': 0.91, 'cierre_7': 0.79}
