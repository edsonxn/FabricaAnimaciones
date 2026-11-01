# -*- coding: utf-8 -*-
"""GUION · Las 9 clases y profesiones OCULTAS de WoW Forever (Crónicas de Warcraft, motor SECUENCIA YT).
Flujo y reglas: docs/estilo_secuencia_yt.md · estilo «gema» (lista en cuenta regresiva, moraleja absurda al final).

TODO es de la BETA de WoW Forever (sale el 4-nov-2026) y puede cambiar. Fuentes (13-oct-2026):
- Farmerfarms, «I Just Discovered a NEW CLASS in WoW Forever» https://youtu.be/iVHOPHyu-Jk  (puesto 1)
- Farmerfarms, «I Found a HIDDEN Mage Profession at Level 20» https://youtu.be/M9ITcoBN0mc  (puestos 3 y 2)
- Mobalytics, «Biggest Secrets Players Have Discovered So Far» (druida serpiente, cita de Aidan «Zirene» Moon, sable)
  https://mobalytics.gg/wow-forever/guides/biggest-secrets-wow-forever-players-have-discovered
- gamer-guides.com/warcraft-forever/professions/ (campamento, pociones en Primeros auxilios, Merchant's Favor)
- Blizzard, Class Deep Dives — Rogue and Warlock (venenos + encantamientos temporales)
- leprestore.com … 11 class concepts (encuesta de Battle.net, septiembre 2026; ninguna clase confirmada)
Nombres sin traducción oficial confirmada se dicen en inglés (Coldflame Saber, Comprehension, Merchant's Favor).
El segmento «overgear» (vía: subida de nivel en self-play) es narración propia, también el código: del creativo con
CRONICAS10 solo se usa la imagen (docs/migracion_googleimagenes.md). Texto aprobado por el usuario (13-oct).
"""

TITULO = "Las 9 clases y profesiones OCULTAS de WoW Forever"
ARCHIVO = "wow_clases_ocultas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")

# Grafía para Applio (13-oct, el usuario): la voz base es multilingüe y con una palabra en inglés cambia de idioma; el TTS lee
# esto y el guion conserva la grafía real (.srt, Montaje, YouTube). Grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "Forever": "Foréver", "Blizzard": "Blízard", "Overgear": "Óverguir",
    "self-play": "sélf pléi", "Battle punto net": "Bátel punto net", "Merchant's Favor": "Mérchants Féivor",
    "Classic": "Clásic", "Comprehension": "Comprijénshon", "Dream Venom": "Drím Vénom", "Aidan Moon": "Éidan Mun",
    "Coldflame Saber": "Cóldfleim Séiber", "Farmerfarms": "Fármer Farms", "Loch Modan": "Loc Módan", "Azeroth": "Azeróth",
    "CRONICAS10": "Crónicas diez",
}

# Whisper escribe distinto lo que Remy dice bien (barón/varón, Comprehension, Loch Modan...); oído revisado por hyp el 13-oct
CER_MAX_POR_FRASE = {k: 0.06 for k in "p5_2 p1_10 p9_2 p7_4 p7_9 overgear_0 overgear_3 p5_1 p4_7 p3_1 p3_8 p2_3 p2_8 p2_10 p1_2 p1_4 p1_8 p1_9 p1_10 p1_13".split()}
CER_MAX_POR_FRASE["p5_1"] = 0.07   # «Bátel punto net» -> Whisper escribe «Battelle.net» (suena bien)

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # el audio del gameplay no se usa (se bajan solo imágenes)
    recorte_por={"scene-001": 0.05, "scene-023": 0.13},   # traen barras negras dentro del clip (franja dcha. / letterbox)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=[]),   # canales que salen con cara/overlay y ensucian el plano
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios en el prompt: el filtro de Lyria los rechaza
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("mysterious and urgent, low strings ostinato, a secret being uncovered", 6),
        "p9": ("sneaky and playful, pizzicato strings, light hand percussion", 4),
        "p8": ("wry and bubbling, woodwinds, alchemy lab curiosity", 4),
        "p7": ("bustling trade caravan, bouncy frame drums, plucked lute", 5),
        "overgear": ("confident and bright, heroic horns, forward motion", 5),
        "p6": ("warm campfire tavern feel, acoustic lute, soft flute", 3),
        "p5": ("speculative and grand, slow choir pads, distant horns", 5),
        "p4": ("jungle cave mystery, serpentine flute, shakers", 5),
        "p3": ("arcane library wonder, celesta and harp, rising curiosity", 5),
        "p2": ("long journey across the world, travelling drums, building strings", 6),
        "p1": ("tense hunt building to triumphant discovery, full orchestra and choir", 8),
        "cierre": ("resolved and a little mischievous, warm horns fading out", 4),
    },
    tramos=[   # <= 175 s cada uno (timeline 13-oct: 155 / 147,5 / 122,5 / 125 / 148,8 s)
        (["intro", "p9", "p8"], "Begin softly from near silence with a mysterious pulse. End on a sustained low string tone."),
        (["p7", "overgear", "p6"], "Begin on a sustained low string tone. End on a warm held chord, gently."),
        (["p5", "p4"], "Begin on a warm held chord. End on a soft, unresolved suspended tone."),
        (["p3", "p2"], "Begin on a soft suspended tone. End on a building held note, anticipation."),
        (["p1", "cierre"], "Begin on a building held note. Climb to a triumphant peak, then settle and fade out to silence at the end."),
    ],
    # durante el anuncio suena la música promo del canal (el usuario, 13-oct; copia de D:\Cronicas de Warcraft\musica promo.mp3)
    reemplazos={"overgear": dict(archivo=r"medios/_overgear/musica_promo.mp3", desde=0.3, db=0, cruce=1.5)},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Ciento diecinueve pergaminos. Doce veces el mismo barón, en el mismo castillo, con la misma cara de fastidio.",
        "Eso tardó un mago de nivel veinte en fabricar un arma que Blizzard nunca anunció.",
        "Un arma que, si la teoría es correcta, convierte al mago en algo que no aparece en la pantalla de creación de personaje.",
        "World of Warcraft Forever sale el cuatro de noviembre y oficialmente trae nueve clases y doce profesiones.",
        "Al menos, eso es lo oficial.",   # «Oficialmente.» suelto salía con acento portugués
        "Porque la beta lleva pocos días abierta y los jugadores ya encontraron sistemas enteros que nadie mencionó.",
        "Hay habilidades que se desbloquean juntando libros y hay una forma de druida que no está en ningún árbol de talentos.",
        "Estas son las nueve clases y profesiones ocultas de World of Warcraft Forever, de la más discreta a la más bestia.",
        "Aviso rápido: todo esto viene de la beta, así que cualquier número puede cambiar el martes que a Blizzard se le antoje.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. El pícaro, que lleva dos profesiones de contrabando y nadie le dice nada.",
        "Tú tienes dos huecos de profesión principal, como todo ciudadano decente.",
        "El pícaro abre su panel y ahí están Venenos y Ganzúa, que no ocupan ningún hueco.",
        "Hasta aquí, nostalgia pura. Lo nuevo viene de la página oficial de Blizzard.",
        "En Forever los venenos ya se pueden usar junto con los encantamientos temporales de arma.",
        "Antes tenías que elegir entre la piedra de afilar y el veneno. Ahora el arma lleva las dos cosas.",
        "Es el único personaje del juego que puede intoxicarte con una daga recién afilada, que encima es de mal gusto.",
        "Está en el último lugar porque no es un secreto, es un privilegio a plena vista.",
        "Yo llevo años pidiendo un tercer hueco de profesión y la respuesta siempre fue que hubiera nacido pícaro.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Primeros auxilios dejó de ser la profesión de las vendas.",
        "Según lo que se ha visto en la beta, las pociones de sanación ya no salen de Alquimia.",
        "Salen de Primeros auxilios.",
        "La profesión que todos subían por compromiso, con tela de lino que les sobraba, ahora fabrica lo que más se bebe en una banda.",
        "Y el alquimista se queda con las pociones de rejuvenecimiento al principio.",
        "Más adelante recibe unas pociones descoloridas que curan más, con un detalle pequeño.",
        "Te devuelven el setenta y cinco por ciento de lo curado como daño con el tiempo.",
        "Es una poción con letra chiquita. Te salva hoy y te cobra mañana, igual que una tarjeta de crédito.",
        "Solo lo he visto en una guía de la beta, así que tómalo con pinzas.",
        "Si se queda así, el enfermero del grupo pasa a ser la persona más importante de la hermandad.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. Hay una carrera de repartidor escondida dentro de las profesiones.",
        "En inglés aparece como Merchant's Favor, algo así como el favor del mercader, y no encontré traducción oficial todavía.",
        "Funciona con las cajas de suministros extraviados, que quizá recuerdes de la Temporada de Descubrimiento.",
        "Encuentras una caja y la llenas con lo que fabrica tu profesión.",
        "Luego la entregas a un vendedor de reputación, sea de la Horda o de la Alianza.",
        "A cambio se abren recetas nuevas y unos cascos raros de nivel veinte.",
        "Unos cascos, y a nivel veinte.",
        "Cualquiera que haya jugado Classic sabe que a ese nivel tu cabeza va al aire, con suerte hasta los treinta.",
        "Y al llegar a trescientos de habilidad se desbloquean títulos de certificación.",
        "O sea que Azeroth por fin tiene papeleo. Ya puedes ser herrero titulado, que es lo que tu mamá siempre quiso.",
    ]},
    # El código lo dice NUESTRA voz (el usuario, 13-oct): del creativo solo va la imagen del tramo 33,0-39,97 s, sin su audio,
    # debajo de overgear_6; el `post` estira la escena para que esos 6,97 s terminen justo en el «Número seis».
    {"id": "overgear", "post": 2.6, "frases": [
        "Ahora, varias cosas de esta lista piden nivel veinte o más antes de dejarte siquiera empezar a buscar.",
        "Y si mientras llega Forever sigues jugando la expansión actual, para eso está Overgear, que patrocina este video.",
        "Lo que me gusta es su modo self-play. Juegas tú, en tu propia cuenta, acompañado por jugadores profesionales.",
        "Subes de nivel con ellos, aprendes la ruta y nadie más toca tu personaje.",
        "Además ya se están preparando para el lanzamiento de World of Warcraft Forever del cuatro de noviembre.",
        "El enlace está en la descripción, y hay un código para ti.",
        "Usa el código CRONICAS10 y te llevas un diez por ciento de descuento.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. El campamento, que es una profesión hecha con pedazos de todas las demás.",
        "El instructor de Cocina te enseña la fogata básica y cada profesión le agrega un mueble.",
        "Minería pone una piedra imán que da poder de ataque y Sastrería planta el estandarte de tu facción.",
        "Peletería arma una tienda de campaña que da experiencia de descanso.",
        "Ingeniería trae un robot que vende componentes, porque un gnomo no sabe acampar sin enchufar algo.",
        "Te sientas un minuto junto al fuego y te llevas las mejoras durante una hora.",
        "La fogata básica aguanta tres muebles, la de oficial cinco y la de experto diez.",
        "Y mi favorito es el de Pesca, que es una pecera.",
        "Una pecera que da ocho por ciento a todas las estadísticas, según la guía que consulté.",
        "Tu hermandad va a tumbar dragones gracias a un pez de colores, y lo que no se sabe todavía es si funciona dentro de las bandas.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Las once clases que Blizzard enseñó a escondidas.",
        "En septiembre, a algunas cuentas les apareció una encuesta en el lanzador de Battle punto net, en la sección de Forever.",
        "No les salió a todas las cuentas, solo a algunas.",
        # «Después mostraba once conceptos.» suelto salía en otro idioma (el usuario, 13-oct): una sola frase larga
        "Primero preguntaba qué papel querrías en una clase futura, y después te enseñaba once conceptos de clases nuevas.",
        "Estaba el manitas, que pilota un robot, y un ilusionista que pelea con copias de sí mismo.",
        "Había un nigromante, una bruja que gasta su propia vida y un bardo que cura con canciones.",
        "También un vampiro sanléin, una celadora y un guerrero de runas al que cada filtración le pone un nombre distinto.",
        "Y de regreso el monje, el cazador de demonios y un caballero de la muerte que empezaría desde nivel uno.",
        "Iba a decir que es la lista de deseos de todo foro desde dos mil cinco. Bueno, es exactamente eso, pero con membrete oficial.",
        "La propia encuesta avisaba que algunos conceptos quizá ni se estén considerando, y ninguno está anunciado para el lanzamiento.",
        "Aun así, nadie encuesta once clases por aburrimiento.",
    ]},
    {"id": "p4", "frases": [
        "Quedan cuatro puestos, y a partir de aquí ya no hablamos de paneles ni de encuestas.",
        "Hablamos de cosas que alguien encontró jugando.",
        "Número cuatro. El druida que se convierte en serpiente.",
        "Un jugador vio en Ventormenta una víbora idéntica a las de las Cuevas de los Lamentos y pensó que era la mascota de alguien.",
        "No era una mascota. Era alguien.",
        "Si un druida feral junta las cinco piezas del conjunto de la víbora de esa mazmorra, se transforma en una.",
        "El bono de cinco piezas se llama Dream Venom y da una probabilidad de aturdir al objetivo durante un segundo.",
        "Lo confirmó Aidan Moon, diseñador sénior de Classic, con un detalle que me ganó.",
        "La serpiente es de un color distinto según la raza del druida, y al acechar se pega al suelo y repta.",
        "Yo creía que era un simple cambio de aspecto, y resulta que le animaron el sigilo a un bicho sin patas.",
        "Una forma nueva de druida escondida en una mazmorra de nivel veinte, sin avisarle a nadie.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. La profesión que solo existe para una clase.",
        "Los magos de la beta abrieron su panel y encontraron una habilidad nueva, Comprehension, que el resto de clases no tiene.",
        "Sirve para descifrar pergaminos misteriosos que van cayendo por el mundo.",
        "En los foros de la beta la describen como la ganzúa del pícaro, pero con lentes.",
        "Al principio parecía relleno, porque los pergaminos daban cosas curiosas y poco más.",
        "Hasta que empezaron a salir los buenos.",
        "Uno imbuye una daga para que tus golpes tengan probabilidad de congelar al enemigo.",
        "Otro encanta una espada durante una hora para reiniciar un hechizo de fuego cada vez que te pegan cuerpo a cuerpo.",
        "Fíjate en lo que tienen en común: dagas, espadas, recibir golpes.",
        "Son pergaminos de mago que solo sirven si el mago está donde un mago nunca debería estar.",
        "Guárdate ese dato para más adelante.",   # «Guarda ese dato.» salía en italiano
    ]},
    {"id": "p2", "frases": [
        "Número dos. Diecinueve libros, seis horas y una segunda profesión escondida dentro de la primera.",
        "Un creador llamado Farmerfarms encontró un libro en Trinquete mientras subía su mago.",
        "Reconoció el sistema de la Temporada de Descubrimiento y decidió buscar el resto, con nivel veinte.",
        "Montañas de Alterac, Arathi, Los Humedales, Loch Modan, la Montaña Roca Negra.",
        "Zonas con enemigos hasta treinta niveles por encima de él.",
        "El libro de las Tierras Inhóspitas le costó más de una hora y más de treinta muertes.",
        "El de Alterac lo sacó atravesando la pared de una torre, que es la forma más honesta de hacer trampa.",
        "Con los primeros nueve libros te dan a elegir un collar.",
        "Con los nueve siguientes aparecen dos habilidades nuevas bajo Comprehension, Estudio e Investigación.",
        "Investigación tiene una hora de reutilización, gasta plumas ligeras y le dio dos objetos por uso.",
        "Según sus pruebas, el botín mejora conforme sube tu nivel de Comprehension.",
        "Sí, son nueve más nueve, y sobra uno. Ese libro, el más cercano a Roca Negra, se entrega a un personaje distinto.",
        "Nadie sabe todavía qué da.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. La clase que no está en la pantalla de creación.",
        "Día dos de la beta. Un mago descifra pergaminos y le sale uno raro, el Pergamino del Sable.",
        "La descripción dice que hay que usarlo sobre la hoja de Filargenta para crear un arma poderosa.",
        "No dice dónde está la hoja. No dice nada más.",
        "El apellido sí suena, porque el barón Filargenta es un jefe del Castillo de Colmillo Oscuro.",
        "Un grupo de nivel veinte limpió la mazmorra entera buscando un objeto en el suelo o una misión. Nada.",
        "La repitieron cinco veces. Nada.",
        "Mientras tanto, Farmerfarms abrió pergaminos hasta que el suyo salió en el ciento diecinueve.",
        "Y entonces un amigo confirmó la teoría, porque la hoja estaba en el botín del barón.",
        "Volvieron al castillo. Reiniciar, matar al barón, reiniciar. En el reinicio número doce, cayó.",
        "Pergamino más hoja dan el Coldflame Saber, un sable de nivel veintiuno.",
        "Su efecto es que tus golpes cuerpo a cuerpo hacen noventa y ocho de daño de fuego extra a objetivos congelados.",
        "Un arma cuerpo a cuerpo. Para un mago.",
        "Ahora junta las piezas, empezando por la daga que congela al golpear, la del número tres.",
        "Súmale que el árbol de escarcha trae Dedos de Escarcha, que trata al enemigo como si estuviera congelado.",
        "Y hay pruebas preliminares de que ese daño de fuego escala con el poder de hechizos.",
        "Eso ya no es un mago de escarcha. Es un mago de batalla, armado pieza por pieza con pergaminos.",
        "Aquí toca ser honesto, porque esto es una teoría. Blizzard no ha confirmado ninguna clase ni estilo nuevo.",
        "Puede que solo sea un sable simpático de nivel veintiuno.",
        "Pero nadie esconde un arma detrás de ciento diecinueve pergaminos y un barón para que sea solo simpática.",
    ]},
    {"id": "cierre", "frases": [
        "Mi veredicto es que el mago se llevó todo el presupuesto de secretos.",
        "Tiene tres de los nueve puestos, y el druida uno muy bueno.",
        "Del guerrero, el chamán y el brujo todavía no ha aparecido nada parecido.",
        "O Blizzard se olvidó de ellos, o sus secretos siguen ahí afuera esperando a alguien con mucha paciencia.",
        "Dime cuál crees que falta, y si eres brujo y encontraste algo, con más razón.",
        "Si quieres seguir escarbando, en el canal ya tienes el video de los doce secretos que esconde World of Warcraft Forever.",
        "Al final, lo único que separa a un mago común de una leyenda son ciento diecinueve pergaminos y un barón que no aprende a cerrar la puerta.",
    ]},
]
