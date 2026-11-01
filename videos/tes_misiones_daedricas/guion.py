# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — primer video del canal hecho en la Fábrica (13-oct-2026).
Motor SECUENCIA YT (gameplay de Skyrim por beat, docs/estilo_secuencia_yt.md) con voz Chatterbox «Sarcastica»
y motion graphics propios de Elder Scrolls (nucleo/mg_tes.py). Sin patrocinio (el usuario, 13-oct).
Guion con la «gema» del canal (lista TOP, humor absurdo, moraleja final, puente a un video ya publicado).
Datos verificados en UESP (en.uesp.net) el 13-oct-2026: Boethiah's Calling, The Whispering Door, The Taste of Death,
The House of Horrors, Waking Nightmare, Ill Met By Moonlight, Pieces of the Past, A Daedra's Best Friend,
Weapon_Artifacts y Armor_Artifacts (cifras de la Hoja de Ébano, Maza, Navaja, Máscara, Piel del Salvador, Anillo de Namira).
"""

TITULO = "Las 8 misiones daédricas que NUNCA deberías hacer en Skyrim"
ARCHIVO = "tes_misiones_daedricas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube
FONETICA = {
    "Mehrunes Dagon": "Merúnes Dágon", "Mehrunes": "Merúnes", "Clavicus Vile": "Clávicus Váil", "Clavicus": "Clávicus",
    "Boethiah": "Boétia", "Mephala": "Mefála", "Hircine": "Írsin", "Molag Bal": "Mólag Bal", "Vaermina": "Vaermína",
    "Skyrim": "Eskáirim", "Oblivion": "Oblívion", "Balgruuf": "Bálgruf", "Hrongar": "Rróngar", "Tyranus": "Tíranus",
    "Stendarr": "Sténdar", "Arkay": "Arkéi", "Silus Vesuius": "Sílus Vesúius", "Silus": "Sílus", "Logrolf": "Lógrolf",
    "Elisif": "Élisif", "Sheogorath": "Sheógorath", "Lydia": "Lídia", "Barbas": "Bárbas", "Sacellum": "Sacélum",
    "draugr": "dráugur", "Falkreath": "Fálkriz", "Markarth": "Márkarz", "Morthal": "Mórzal", "Bethesda": "Bezésda",
    "Cassimir": "Casimír", "Nelkir": "Nélkir", "Jorgen": "Yórguen", "Erandur": "Erandúr",
}

# Whisper escribe distinto los nombres que Chatterbox dice bien (Boecia/Boetia, Ircine, Falcreaz, Harvalgruf, Berulus,
# Arcai, Stendhal, Rongar, Mefala, «estaba Hermina» por «está Vaermina»...); se revisó cada transcripción el 13-oct.
CER_MAX_POR_FRASE = {k: 0.03 for k in "p8_1 p7_2 p7_4 p6_1 p6_2 p6_3 p5_0 p5_2 p4_1 p4_3 p3_1 p2_5 p2_6 p1_5".split()}
CER_MAX_POR_FRASE.update({"p6_1": 0.045, "p1_6": 0.045, "p1_9": 0.04, "p2_1": 0.03})
# frases de > 10 s que terminan hablando hasta el final (CER ~0 y la transcripción acaba bien)
TAIL_MAX_POR_FRASE = {k: 0.46 for k in "p7_1 p5_1 p2_6 p1_5 p1_9 p6_1".split()}
TAIL_MAX_POR_FRASE["p3_1"] = 0.52

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={"scene-065": 0.05},   # barras laterales de origen
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG"]),   # marcas de agua (Tweakedculture1, TIMENG)
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Dark nordic fantasy orchestral underscore like a classic open-world RPG soundtrack: low male choir, "
           "deep war drums, cello and viola, distant horns, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("ominous mountain shrine at night, low choir hum, slow heartbeat drum", 6),
        "p8": ("wry and mischievous, plucked strings, light frame drum, a deal with fine print", 3),
        "p7": ("dusty cult museum, harpsichord-like plucks, sly woodwinds, creeping menace", 4),
        "p6": ("moonlit hunt in a cave, tribal drums, howling horn, primal tension", 6),
        "p5": ("dreamlike and uneasy, celesta and soft choir, drifting nightmare pads", 5),
        "p4": ("haunted stone house, groaning low brass, scraping strings, cruel and heavy", 7),
        "p3": ("candlelit catacomb feast, slow sinister waltz in low strings, choir whispers", 6),
        "p2": ("palace intrigue, whispering strings, ticking percussion, quiet betrayal", 7),
        "p1": ("blood sacrifice on a mountain altar, full choir and drums, dark and grand", 9),
        "cierre": ("calm after the storm, warm low strings, a wry final note fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro", "p8", "p7"], "Begin softly from near silence with a low choir hum. End on a sustained low string tone."),
        (["p6", "p5"], "Begin on a sustained low string tone. End on a soft, eerie held chord."),
        (["p4", "p3"], "Begin on a soft eerie chord. End on a heavy, unresolved low drone."),
        (["p2"], "Begin on a low drone. End on a building held note, anticipation."),
        (["p1", "cierre"], "Begin on a building held note. Climb to a dark grand peak, then settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Hay un altar en las montañas, al noreste de Ventalia, donde una sacerdotisa te pide con toda calma que traigas a tu compañero de viaje y lo subas a una piedra.",
        "Y luego que lo mates.",
        "Ese compañero te siguió por media Skyrim cargando tu botín y metiéndose contigo en cada cueva llena de draugr.",
        "La recompensa por tanta lealtad es una piedra manchada de sangre y una armadura nueva para ti.",
        "Ese altar no es el único. Skyrim está lleno de príncipes daédricos que te ofrecen poder a cambio de algo, y ese algo casi siempre es la vida de otra persona.",
        "Así que hoy van las ocho misiones daédricas que NUNCA deberías hacer, de la que solo te quita la dignidad a la que te quita a los amigos.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Empezamos con un perro que habla.",
        "Se llama Barbas, te lo encuentras en el camino al suroeste de Falkreath, y su dueño es Clavicus Vile, el príncipe de los tratos y los deseos con letra pequeña.",
        "Los dos se pelearon, y Barbas te pide que los reconcilies. Suena tierno.",
        "Hasta que llegas al santuario y el príncipe te ofrece elegir: o le entregas el hacha que fuiste a buscar, o usas esa misma hacha para matar al perro.",
        "Ojo, que el propio Clavicus admite que gran parte de su poder vive dentro de Barbas. Sin el perro, dice, no sería más poderoso que tú.",
        "Si eliges bien, te llevas la Máscara de Clavicus Vile, que te deja los precios un veinte por ciento mejores.",
        "Un príncipe daédrico, un ser eterno de Oblivion, y su gran regalo es un cupón de descuento.",
        "Yo la primera vez maté al perro por no leer el diálogo, porque elegí la opción de arriba como elijo todo en la vida. Todavía me acuerdo cada vez que veo un perro en Carrera Blanca.",
    ]},
    {"id": "p7", "frases": [
        "En el siete aparece el único aficionado a los museos de toda la provincia.",
        "Silus Vesuius tiene en su casa un museo dedicado al Alba Mítica, el culto que casi destruye el mundo en Oblivion, y te da la visita guiada él mismo, encantado de tener público.",
        "Te pide recuperar los tres fragmentos de la Navaja de Mehrunes. Uno lo guarda una cuerva bruja en lo alto de una roca, y otro lo tiene un tal Jorgen en Morthal, que no lo suelta por las buenas.",
        "Llegas al santuario con el muchacho emocionadísimo, y Mehrunes Dagon pone una condición para reparar la navaja: que mates a Silus.",
        "Silus, en pánico, te ofrece quinientas monedas de oro por su vida. Quinientas. Es la mitad de lo que cuesta un caballo.",
        "Si lo perdonas, huye con la hoja rota mientras te atacan los drémoras. Si no, te quedas con la navaja.",
        "Y la navaja mata al instante con una probabilidad de más o menos dos por ciento. Dos golpes de cada cien.",
        "Mataste a tu único fan de los museos por un arma que funciona cuando quiere, como la impresora de la oficina.",
    ]},
    {"id": "p6", "frases": [
        "Número seis, y aquí la cosa ya no tiene nada de gracioso.",
        "En la cárcel de Falkreath hay un hombre llamado Sinding. Es un hombre lobo, y lo encerraron por matar a Lavinia, una niña de nueve años, hija de unos granjeros.",
        "Él jura que fue culpa de un anillo que le robó a Hircine, el príncipe de la caza. Hircine lo maldijo, y el anillo lo transformaba justo en el peor momento.",
        "Te da el anillo, se escapa, y Hircine te manda a una cueva entre Falkreath y Carrera Blanca para que lo caces y le arranques la piel.",
        "Si obedeces, te llevas la Piel del Salvador, una armadura ligera con quince de resistencia a la magia y cincuenta al veneno.",
        "Una armadura hecha, LITERALMENTE, de otro señor.",
        "Y si te pones el anillo maldito antes de terminar, siendo hombre lobo, cada hora tienes una posibilidad entre diez de transformarte al aire libre, y no te lo puedes quitar.",
        "Vas tranquilo por el mercado de Carrera Blanca y de pronto eres el problema de todos los guardias.",
        "Mi postura es simple. Sinding mató a una niña, pero arrancarle la piel para hacerte un chaleco tampoco te deja en el bando de los buenos.",
    ]},
    {"id": "p5", "frases": [
        "Bajando al cinco, y subiendo la incomodidad, está Vaermina, la señora de las pesadillas.",
        "En un pueblo costero del norte nadie duerme bien. Un sacerdote de Mara llamado Erandur te pide ayuda para acabar con las pesadillas, que salen de un templo abandonado sobre los acantilados.",
        "Por el camino descubres su secreto. Erandur antes se llamaba Cassimir, era sacerdote de Vaermina, y huyó cuando los orcos atacaron el templo, dejando ahí dentro a sus compañeros.",
        "Años después, por pura vergüenza, se hizo sacerdote de Mara. Es el único personaje de esta lista que intenta arreglar lo que hizo.",
        "Y justo cuando va a destruir la Calavera de la Corrupción, Vaermina te susurra que lo mates y te la quedes.",
        "La calavera es un bastón que pega veinte de daño, y hasta cincuenta si antes le robas los sueños a alguien que está dormido.",
        "O sea, un arma que funciona mejor si entras de noche a casas ajenas a mirar cómo duerme la gente. Muy de Skyrim, la verdad.",
        "Si lo perdonas, Erandur se ofrece a acompañarte. Un sacerdote arrepentido que te cura las heridas, contra un palo que da pesadillas.",
        "Elegir el palo es de las peores decisiones del juego, y te lo dice alguien que tiene cuarenta quesos guardados en un cofre.",
    ]},
    {"id": "p4", "frases": [
        "Ahora sí, entramos en la parte donde Skyrim deja de pedir permiso.",
        "En Markarth hay una casa abandonada junto a la puerta principal. Un vigilante de Stendarr llamado Tyranus te pide que entres con él a investigar. Muy valiente, el señor.",
        "Dentro, los muebles empiezan a flotar, una voz te habla, y Tyranus termina atacándote. No hay manera de salvarlo.",
        "Esa voz es Molag Bal, el príncipe de la dominación, y te encarga liberar a Logrolf, un sacerdote de Boethiah que tienen prisionero los renegados.",
        "Lo rescatas, lo llevas al altar, y Molag Bal te ordena golpearlo hasta que se rinda. Cuando se muere, Molag Bal lo revive. Y le vuelves a pegar.",
        "Lo más perturbador es un detalle técnico. Como esa muerte está dentro del guion, el juego no la cuenta como asesinato y nadie pone precio a tu cabeza.",
        "Para Skyrim, apalear a un sacerdote encadenado es papeleo.",
        "El premio es la Maza de Molag Bal, que en cada golpe quita veinticinco de aguante y veinticinco de magia, y atrapa el alma durante tres segundos.",
        "Te la vas a quedar, eso seguro. Bueno, yo me la quedé, y la usé muchísimo, pero no lo cuento con orgullo.",
    ]},
    {"id": "p3", "frases": [
        "Quedan tres, y en las tres el juego cambia de víctima. Ya no es un desconocido. Es alguien a quien acabas de ayudar.",
        "Número tres. En el Salón de los Muertos de Markarth, el hermano Verulus, sacerdote de Arkay, te pide que averigües quién anda rondando las criptas. Ahí conoces a Eola.",
        "Eola es encantadora y caníbal, y te invita a unirte al culto de Namira, la señora de la podredumbre.",
        "El plan consiste en llevar a Verulus engañado a una cueva al este de la ciudad, dormirlo sobre un altar, matarlo, y comértelo delante de todos los invitados.",
        "A Verulus. Al que le acabas de hacer un favor.",
        "La recompensa es el Anillo de Namira. Cincuenta puntos más de aguante, y cada vez que comes un cadáver ganas salud extra y regeneración durante cinco minutos.",
        "Cinco minutos. Te comiste a un sacerdote por cinco minutos de vida extra. Ni el peor menú del día te cobra tan caro.",
        "¿Tú te lo comiste? No hace falta que contestes. El juego lo sabe.",
    ]},
    {"id": "p2", "frases": [
        "Ya en el podio, el número dos ocurre en el lugar más seguro de toda la provincia, el palacio del jarl de Carrera Blanca.",
        "El jarl Balgruuf está preocupado por su hijo menor, Nelkir, un niño que se pasa el día hablando de una voz que le susurra detrás de una puerta cerrada en el sótano.",
        "La voz es Mephala, la tejedora de mentiras. Abres la puerta, y dentro te espera una espada, la Hoja de Ébano.",
        "Al principio la hoja te devuelve diez puntos de vida por golpe. Para que llegue a treinta, tienes que usarla para matar a gente que te aprecia.",
        "Cada dos amigos asesinados, suben cuatro puntos. En total son diez traiciones.",
        "Diez. Diez personas que te saludaban por la calle o te llamaban amigo, a cambio de veinte puntos más por espadazo. Y Mephala te comenta cada muerte, como si narrara un partido.",
        "Lo que casi nadie sabe es que en los archivos del juego quedaron restos de un plan descartado, donde los hijos de Balgruuf lo mataban y su hermano Hrongar se quedaba con el trono.",
        "El niño raro del sótano iba a ser, de verdad, el villano. Yo siempre lo sospeché.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. El altar del principio.",
        "El Sacellum de Boethiah está en las montañas al noreste de Ventalia, y la misión pide nivel treinta para empezar.",
        "La sacerdotisa te explica la regla sin rodeos: trae a alguien que te siga, súbelo al Pilar del Sacrificio y mátalo.",
        "No vale cualquiera. Los seguidores esenciales no activan el pilar. Tiene que ser alguien que de verdad se pueda morir.",
        "Lydia. El mercenario que contrataste en la taberna. Y, según cuenta la comunidad, hasta tu pareja, si la llevas de acompañante.",
        "Lo matas, y en ese instante los fieles de Boethiah se lanzan a pelear entre ellos hasta que queda uno solo. Boethiah se mete en el cuerpo del ganador y te habla con su boca.",
        "Después te manda a matar a su campeón, al noroeste de Falkreath, y te quedas con su cota de ébano.",
        "Ahoga el ruido de tus pasos, y le hace cinco puntos de daño de veneno cada segundo a quien se te acerque.",
        "Una armadura que envenena a los que se acercan, regalada por matar al que más cerca estuvo de ti. Bethesda no es sutil, pero es coherente.",
        "Y el dato que más me impresionó. En los archivos del juego sigue existiendo una segunda parte, nunca terminada, en la que Boethiah te mandaba asesinar a Elisif la Bella, la jarl de Soledad.",
        "Yo creía que la habían quitado por ser demasiado oscura. Investigando, resulta que nadie sabe muy bien por qué se quedó a medias. A lo mejor alguien en el estudio dijo que ya era suficiente.",
        "Por eso está en el número uno. No por el premio, que está bien, sino por lo que te pide.",
        "Que la persona que confió en ti suba a la piedra por su propio pie.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Las ocho son grandes misiones, y ninguna se puede hacer con la conciencia tranquila, que es justo lo que las vuelve inolvidables.",
        "Seguro que alguien habría puesto a Sheogorath, pero en su misión lo único que sufre de verdad es tu paciencia. Si tú habrías cambiado el orden, me interesa saber cuál subirías.",
        "Y si te quedaste con ganas de saber quiénes son todos estos príncipes y cuál de ellos manda más, tienes que ver el video de los ocho Príncipes Daédricos más poderosos de Skyrim, que ya está en el canal.",
        "La próxima vez que alguien te invite a subir a una piedra bonita en lo alto de una montaña, dile que te duelen las rodillas. Te va a salvar la vida, y de paso las rodillas.",
    ]},
]
