# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Miquella QUE IGNORASTE» (18-oct-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md (repite «Las 5 … QUE IGNORASTE» de
Márika ×21,5 y Radagon ×11 cambiando el sujeto → Miquella; el usuario pidió ~20 min: PRUEBA de duración).
Cada puesto va partido en dos escenas (pN / pNb) para que Lyria no pase de 175 s por escena.
No repite lo de Márika ni Radagon (los Anillos de luz y que Miquella dejó la fe de la Orden Áurea ya salieron en Radagon).
Datos verificados en eldenring.wiki.fextralife.com el 18-oct-2026: Miquella, Bewitching Branch, Malenia's Winged Helm,
Needle Knight Leda (diálogos), Redmane Freyja (diálogos), Thiollier (diálogos), Sir Ansbach (diálogos), Remembrance of the
Blood Lord, Secret Rite Scroll, Remembrance of a God and a Lord, Young Lion's Helm, Promised Consort Radahn (frases de Miquella
en la pelea), Light of Miquella, Circlet of Light, Miquella's Great Rune, Miquella's Cross (13 cruces y sus mensajes),
St. Trina (diálogos con el néctar; Sword of St. Trina), Haligtree Crest Surcoat.
"""

TITULO = "Las 5 peores atrocidades de Miquella QUE IGNORASTE"
ARCHIVO = "er_miquella_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube
FONETICA = {
    "Miquella": "Mikuéla", "Malenia": "Malénia", "Radahn": "Rádan", "Radagon": "Rádagon", "Mohgwyn": "Mógüin",
    "Mohg": "Mog", "Ansbach": "Ánsbaj", "Thiollier": "Tioliér", "Freyja": "Fréya", "Enir-Ilim": "Enír Ilím",
    "Messmer": "Mésmer", "Aeonia": "Eónia", "Elden Ring": "Élden Ring", "Elden": "Élden", "Kalé": "Kalé",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    yt=dict(sufijo="Elden Ring", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE", "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150", "Taveris the Red", "Cravotato", "NeoJetty"]),   # 19-oct: rótulos, marcas, guías, debug, fan-art
)

# Revisado el 18-oct tras la 1.ª ronda (eval.json): Whisper escribe «Moj/Mohawk/Mojé» por Mohg, «Mikeya» por Miquella,
# «Ansback», «Teolier»; las frases largas hablan hasta el final (transcripción completa y bien terminada) y algunas llevan una
# pausa larga tras punto. Tomas con error real movidas a voz/_descartes/ (vestos, Estrato, con pasión, besaba, Corludo).
CER_MAX_POR_FRASE = {'intro_5': 0.013, 'p5_2': 0.021, 'p5_5': 0.045, 'p4_2': 0.044, 'p4_3': 0.02, 'p4_6': 0.033, 'p4_7': 0.021,
                     'p4_8': 0.035, 'p4_9': 0.048, 'p4_11': 0.015, 'p4b_1': 0.015, 'p4b_2': 0.018, 'p4b_6': 0.028, 'p4b_8': 0.015,
                     'p3_2': 0.013, 'p3_4': 0.014, 'p3_8': 0.016, 'p3b_1': 0.02, 'p3b_5': 0.049, 'p3b_6': 0.015, 'p3b_8': 0.027,
                     'p1b_2': 0.018, 'p1b_7': 0.015}
GAP_MAX_POR_FRASE = {'p5_6': 0.74, 'p5_11': 0.8, 'p4_9': 0.79, 'p4_11': 0.74, 'p4b_0': 0.83, 'p4b_5': 0.68, 'p3_8': 0.7,
                     'p2_7': 0.66, 'p2b_1': 0.69, 'p1b_8': 1.42, 'cierre_0': 0.68}
TAIL_MAX_POR_FRASE = {'intro_0': 0.44, 'intro_3': 0.38, 'intro_5': 0.51, 'p5_5': 0.61, 'p5_6': 0.54, 'p5b_2': 0.67, 'p4_2': 0.54,
                      'p4_10': 0.52, 'p4_11': 0.37, 'p4b_0': 0.44, 'p4b_10': 0.37, 'p3_5': 0.37, 'p3_7': 0.49, 'p3_8': 0.72,
                      'p3_10': 0.42, 'p3_11': 0.55, 'p3_12': 0.48, 'p3b_1': 0.42, 'p3b_6': 0.42, 'p2_2': 0.5, 'p2_7': 0.38,
                      'p2b_1': 0.37, 'p2b_12': 0.36, 'p1_4': 0.42, 'p1_5': 0.37, 'p1b_0': 0.43, 'p1b_1': 0.61, 'p1b_2': 0.56,
                      'p1b_3': 0.56, 'p1b_8': 0.56, 'cierre_1': 0.61, 'cierre_2': 0.36}

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Dark gothic fantasy orchestral underscore like a melancholic soulslike action RPG soundtrack: solemn low choir, "
           "pipe organ pads, cello and harp, distant bells, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("a golden child sleeping inside a cocoon, fragile celesta over a low choir hum, innocence with something wrong underneath", 6),
        "p5": ("a gentle warm glow that feels hypnotic, soft harp arpeggios and a sweet choir that is a little too sweet", 4),
        "p5b": ("the spell breaks, a golden flash then cold strings, followers turning on each other, tense pizzicato and low drums", 6),
        "p4": ("a blood lord in an underground palace, deep brass, ritual drums, crimson grandeur", 5),
        "p4b": ("a stolen corpse and a secret rite scroll, hollow organ, slow mourning cello, quiet betrayal", 6),
        "p3": ("a childhood promise between brothers, warm horns that slowly sour, a war memory with distant battle drums", 5),
        "p3b": ("a soul sewn into a borrowed body, dissonant choir, heavy low strings, grotesque wedding march", 8),
        "p2": ("a pilgrimage of stone crosses in a shadowed land, sparse bells, lonely solo viola, the body falling away piece by piece", 6),
        "p2b": ("an abandoned saint asleep among wilting purple lilies, lullaby on music box and harp, heartbreak and poison", 7),
        "p1": ("an age of compassion that is really a cage, radiant major choir that turns sinister, soft yet suffocating", 8),
        "p1b": ("the final plea of the last free will, solemn organ and full choir swell, then a fading golden circlet", 9),
        "cierre": ("calm after the storm, warm low strings, a wry final note fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro"], "Begin softly from near silence with a fragile celesta. End on a sustained low string tone."),
        (["p5"], "Begin on a sustained low string tone. End on a held, slightly unsettling chord."),
        (["p5b"], "Begin with a bright flash chord that turns cold. End on a tense low pulse."),
        (["p4"], "Begin on a tense low pulse. End on a heavy held brass tone."),
        (["p4b"], "Begin on a hollow organ tone. End on a quiet, mournful low cello note."),
        (["p3"], "Begin on a quiet low cello note. End on a held low horn chord."),
        (["p3b"], "Begin on a low horn chord. End on a heavy, unresolved low drone."),
        (["p2"], "Begin on a low drone with a single bell. End on a lonely sustained viola note."),
        (["p2b"], "Begin on a soft lonely music box. End on a fragile held harp chord."),
        (["p1"], "Begin on a fragile harp chord. End on a held, radiant but uneasy choir chord."),
        (["p1b"], "Begin on a radiant uneasy choir chord. Swell to a sorrowful peak, then settle on a low tone."),
        (["cierre"], "Begin on a calm low tone. Settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Durante dos años, la historia de Miquella fue la de una víctima: un niño dios eterno que fue raptado dentro de su capullo por Mohg, el Señor de la Sangre, mientras su hermana Malenia lo esperaba en el Árbol Sagrado.",
        "Todos le tuvimos pena. Yo le tenía hasta cariño, y eso que en todo el juego base nunca le vi la cara.",
        "Y entonces llegó la expansión de la Tierra de las Sombras, y el niño bondadoso resultó ser el personaje más peligroso de todo Elden Ring.",
        "Y no lo digo yo. Lo dice su propia hermana, en la descripción de su yelmo: Miquella posee la sabiduría y el encanto de un dios, y es el más temible de todos los Empíreos.",
        "Lo dice también un caballero que lo conoció de cerca, sir Ansbach, que te lo suelta en la primera conversación sin anestesia: Miquella el Bondadoso es un monstruo.",
        "Así que hoy van las cinco peores atrocidades de Miquella que ignoraste, porque mientras todos mirábamos a Mohg como el malo de la película, el niño del capullo estaba moviendo los hilos de medio mundo.",
        "Y te aviso desde ya: el número uno no es una pelea ni un cadáver robado. Es lo que Miquella quería hacer contigo. Con tu cabeza.",
        "Ponte cómodo, que este va largo. Hay mucho capullo que abrir.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El encanto.",
        "En la Tierra de las Sombras puedes conseguir la Rama hechizante, un objeto que sirve para encantar a un enemigo y que pelee de tu lado un rato.",
        "Y la descripción de esa rama, que casi nadie lee porque está ocupado esquivando cosas, dice: el Empíreo Miquella es amado por mucha gente. De hecho, ha aprendido muy bien a provocar ese afecto.",
        "Ha aprendido a provocarlo. Fíjate en la palabra. No dice que la gente lo quiere. Dice que él sabe cómo hacer que lo quieran.",
        "Esa es la diferencia entre caer bien y tener un control remoto de personas.",
        "Todo el grupo que te encuentras al llegar a la Tierra de las Sombras sigue a Miquella: Leda, la caballera de la aguja, sir Ansbach, Freyja, el Cornudo, Thiollier, y unos cuantos más.",
        "Y si te fijas, es el equipo más raro que se puede juntar. Un caballero de la sangre pura que servía a Mohg, una guerrera de la guardia de Radahn, un Cornudo que odia a Márika con toda su alma, y un envenenador perdidamente enamorado de una santa.",
        "Gente que en cualquier otra partida se mataría nada más verse.",
        "Y eso no es una teoría mía, porque lo dice la propia Leda: sin el encanto de Miquella, esos compañeros se habrían ido a los golpes a primera vista.",
        "Lo dice como si fuera algo bonito. Como cuando alguien te cuenta que su grupo de amigos solo se aguanta porque hay uno que paga todas las cervezas.",
        "Y piénsalo un segundo, porque tú también estuviste ahí. Llegaste a ese grupo, te hablaron con cariño, te pidieron ayuda, y les ayudaste sin preguntar.",
        "Nadie en ese grupo se pregunta por qué está ahí. Están, y ya. Y eso, en un juego donde todo el mundo tiene un motivo retorcido para cada paso, debería haberte dado mala espina.",
    ]},
    {"id": "p5b", "frases": [
        "El problema llega a mitad de la expansión. Cuando te acercas a la fortaleza de Messmer, una luz dorada estalla en el cielo: Miquella ha roto su Gran Runa.",
        "Y con la runa, se rompe el encanto.",
        "Freyja te lo dice con una calma que da miedo: el encantamiento del bondadoso Miquella ha expirado, y eso puede ser desorientador, por decirlo suavemente.",
        "Desorientador. Imagina despertar una mañana y darte cuenta de que llevas años sirviendo a alguien porque te lo ordenaron por dentro, y no porque lo hayas decidido tú.",
        "Thiollier, el del veneno, se queda perdido, como él mismo dice, atormentado por los recuerdos de Santa Trina.",
        "Y la que no despierta es Leda. Al contrario. Se vuelve más fiel que nunca.",
        "Para ella, la runa partida es una oportunidad para hacer limpieza: eliminar a los que no son dignos de estar junto a Miquella.",
        "Primero va por el Cornudo, porque según ella la venganza cambia a un hombre, y su espada podría acabar apuntando a Miquella el Bondadoso.",
        "Luego va por Ansbach, porque según Leda, ese hombre abrió en canal a Miquella con su espada de sangre, y no se le puede dejar suelto.",
        "Y tú, si te descuidas, acabas ayudándola a cazar a tus propios compañeros de viaje, uno por uno, en el mismo mapa donde hace unas horas compartían hoguera.",
        "Ese es el efecto real del encanto. No hace amigos. Hace una secta que, en cuanto se apaga la luz, empieza a matarse entre ella.",
        "Y lo peor es que esto es el número cinco. Es lo más suave que hizo.",
    ]},
    {"id": "p4", "frases": [
        "Bajamos al cuatro, y aquí toca defender a un villano que todos odiamos con mucho gusto.",
        "Mohg, el Señor de la Sangre. El de la cueva escondida bajo tierra, el del tridente, el que te hacía sangrar a chorros con una sola palmada.",
        "En el juego base, la historia parecía clarísima: Mohg se robó el capullo de Miquella del Árbol Sagrado y se lo llevó a su palacio de Mohgwyn para convertirse en su consorte.",
        "Su recuerdo lo cuenta así: queriendo elevar a Miquella a la divinidad plena, Mohg quiso ser su consorte, y tomar el papel de monarca.",
        "Pero por mucho que intentara compartir su sangrienta alcoba, nunca recibió respuesta del joven Empíreo.",
        "Un secuestrador, un pervertido, y encima rechazado. Facilísimo de odiar. Yo lo odié con todas mis fuerzas, y con todos mis frascos.",
        "Pero en la expansión, sir Ansbach, que fue comandante de los caballeros de la sangre pura de Mohg, cuenta otra versión.",
        "Cuando Miquella parte su runa, Ansbach te confiesa que una vez retó a Miquella para liberar a lord Mohg de su encantamiento.",
        "Liberar a Mohg. De su encantamiento.",
        "O sea, el secuestrador estaba encantado. Mohg no se llevó a Miquella. Miquella hizo que Mohg se lo llevara.",
        "Y de golpe todo cuadra. La entrada a la Tierra de las Sombras está justo ahí, en el palacio de Mohg, en ese brazo seco que asoma del capullo y que tienes que tocar para empezar la expansión.",
        "Miquella necesitaba llegar a ese sitio, y necesitaba que alguien fuerte guardara su cuerpo mientras tanto. Así que el pobre Mohg, con toda su sangre y todo su tridente, fue el taxi.",
        "Un taxi que además se creía casado con el pasajero.",
    ]},
    {"id": "p4b", "frases": [
        "Ansbach no logró liberarlo. El encanto ganó. Y la frase que dice después es de las más tristes del juego: más que a nadie, culpo al encantamiento.",
        "Y todavía falta lo peor. Porque cuando tú matas a Mohg en su palacio, su cuerpo desaparece.",
        "Ansbach también lo nota: tras la muerte de lord Mohg en su palacio, alguien se ha llevado su cuerpo. Y se pregunta qué pensarán hacer con sus restos.",
        "La respuesta está en un pergamino de corteza blanca, el Pergamino del rito secreto, que describe el rito de la puerta divina.",
        "Dice: un señor anunciará el regreso de un dios, y el alma de ese señor necesitará un recipiente.",
        "Un recipiente. Un cuerpo vacío para meterle dentro un alma ajena.",
        "Cuando le entregas ese pergamino a Ansbach, lo entiende todo: Miquella ha abandonado el alma de lord Mohg. Solo desea su cascarón vacío.",
        "Y lo remata con una frase que a mí me partió en dos: mi querido señor merecía algo mejor.",
        "Piénsalo. Mohg pasó siglos creyendo que era el elegido, el futuro rey consorte de un dios.",
        "Y para Miquella nunca fue nada. Ni siquiera un rechazo. Fue un cuerpo de repuesto, guardado en el armario hasta que hiciera falta.",
        "Yo maté a Mohg en tres partidas distintas, y en ninguna se me ocurrió que le estaba haciendo el trabajo sucio al niño del capullo. Le entregué el cadáver envuelto para regalo.",
        "Y si te preguntas para quién era ese cuerpo, ahí entra el número tres.",
    ]},
    {"id": "p3", "frases": [
        "Y si has llegado hasta aquí, ya sabes que esto va de mal en peor, así que si el video te está gustando, suscríbete, que a Miquella eso no le haría ninguna gracia.",
        "Número tres. El general Radahn, el de la Plaga Estelar, el del caballo diminuto.",
        "Un recuerdo de la expansión cuenta cómo empezó todo: en su infancia, Miquella vio en Radahn a un señor.",
        "Su fuerza y su bondad contrastaban con lo afligidos que estaban los gemelos, Miquella y su hermana Malenia.",
        "Y así, Miquella pidió su deseo de corazón: que algún día el propio Radahn fuera su rey consorte.",
        "Hasta aquí suena tierno. Un niño que admira a su hermano mayor. Bueno, medio hermano por parte de Radagon, que en esta familia ya nadie sabe quién es pariente de quién.",
        "Pero ahora acuérdate de lo que le pasó a Radahn en el juego base.",
        "Él y Malenia pelearon en la batalla de Aeonia, Malenia hizo florecer la putrefacción escarlata, y el pobre Radahn quedó podrido, sin juicio, vagando por las dunas de Caelid y comiéndose cadáveres durante años.",
        "Y aquí está el detalle que casi nadie leyó. El Yelmo del joven león, el casco de Radahn cuando era joven, cuenta que cuando Malenia, la espada de Miquella, hizo florecer la flor de la putrefacción en Aeonia, el propio Radahn escuchó un murmullo al oído.",
        "Y el murmullo decía: Miquella te espera, oh consorte prometido.",
        "En el peor momento de su vida, podrido y derrotado por la hermana de Miquella, lo primero que oye el general es la voz de Miquella apuntándolo en su agenda.",
        "El juego no dice que Miquella lo planeara todo. Pero que su espada lo destrozara justo antes del mensajito, es una coincidencia que yo no le compraría ni al mercader Kalé.",
        "Y fíjate en el título que lleva ella. Malenia no es la espada de Márika, ni la espada de la Orden Áurea. Es la espada de Miquella. Lo que ella corta, lo corta en nombre de su hermano.",
    ]},
    {"id": "p3b", "frases": [
        "Luego viene el festival de la guerra, esa fiesta que organizan sus propios soldados para que alguien por fin le dé una muerte digna.",
        "Y Freyja, que fue de su guardia, te lo explica en la expansión: al concluir el festival de la guerra, el alma del general Radahn tuvo un final honorable. Pero el bondadoso Miquella desea revivirla.",
        "Un final honorable. Lo único que le quedaba a ese hombre después de años podrido era morir con dignidad, peleando. Y Miquella se lo quita.",
        "Ahora junta las piezas. El alma de Radahn, el cuerpo vacío de Mohg, y un pergamino que dice que el alma del señor necesitará un recipiente.",
        "Al final de la expansión, en Enir-Ilim, a los pies de la puerta divina, te encuentras al Consorte prometido Radahn.",
        "El alma de Radahn, metida dentro del cadáver de Mohg.",
        "Dos hermanos de Miquella cosidos en uno. Y en los brazos y las piernas le asoman cuernos, los mismos cuernos malditos con los que nació Mohg, porque ese cuerpo nunca dejó de ser suyo.",
        "Es el regalo de bodas más espantoso de la historia de los videojuegos. Te casas, y tu marido es un rompecabezas de dos parientes muertos.",
        "Y el pobre Radahn ni siquiera eligió nada de esto. El trato, según Miquella, fue una promesa de niños.",
        "En un recuerdo, Miquella le dice: hermano mayor, voy a ser un dios. Si cumplimos nuestra parte del juramento, prométeme que serás mi consorte.",
        "Una promesa de la infancia, cobrada siglos después, con intereses, y con un cuerpo prestado.",
        "Y durante la pelea, Miquella lo deja clarísimo con su propio milagro, la Luz de Miquella: un dios y un rey consorte es todo lo que el mundo necesita.",
        "Todo lo que el mundo necesita. Los demás sobramos.",
    ]},
    {"id": "p2", "frases": [
        "Ya en el podio, el número dos es todo lo que Miquella dejó tirado por el camino. Y la lista es larga.",
        "Si recorres la Tierra de las Sombras con calma, vas a encontrar unas cruces de piedra repartidas por todo el mapa.",
        "Son las cruces de Miquella, trece en total, y cada una lleva un mensaje suyo, escrito en primera persona. Ansbach, que las va buscando contigo, dice que son como las huellas del tierno Miquella.",
        "La primera dice: aquí abandono la primera carne de mi cuerpo.",
        "Y luego siguen las demás. Aquí abandono mi brazo izquierdo. Aquí abandono mi brazo derecho. Aquí abandono mi ojo.",
        "Aquí abandono mi corazón. Aquí abandono mis dudas y mis vacilaciones. Aquí abandono todos mis miedos.",
        "Es como seguir las migas de pan de alguien que se va desarmando a pedazos para llegar más ligero a su destino.",
        "Y la Gran Runa también la dejó atrás, partida. Lo que queda de ella dice: una Gran Runa abandonada por Miquella, que está rota y despojada de su abundancia, y que solo conserva el poder de resistir encantos.",
        "O sea, lo único que quedó de su runa es la vacuna contra él mismo.",
        "Hasta aquí, podrías pensar que es un sacrificio heroico. Un niño que lo da todo por su meta, hasta su propio cuerpo.",
        "Pero hay una cruz escondida bajo tierra, en una grieta llena de ataúdes de piedra, que dice algo muy distinto.",
        "Aquí abandono mi amor.",
    ]},
    {"id": "p2b", "frases": [
        "Y ese amor tiene nombre. Santa Trina.",
        "Santa Trina era una figura misteriosa a la que se rezaba en las Tierras Intermedias. Unos decían que era una muchacha hermosa, otros juraban que era un muchacho.",
        "Y resulta que era Miquella. Su otra mitad. La parte dulce, la del sueño.",
        "Miquella la arrancó de sí mismo y la dejó en ese agujero, sola y rodeada de lirios morados a punto de marchitarse.",
        "Y si bebes de su néctar, que es veneno de sueño, Trina te habla. Y lo que te pide pone los pelos de punta.",
        "Haz que Miquella se detenga. No conviertas a la pobre criatura en un dios.",
        "La divinidad sería la prisión de Miquella. Una divinidad enjaulada ya no tiene salvación.",
        "Y al final, con la voz casi dormida: debes matar a Miquella. Concédele el perdón.",
        "La mejor parte de Miquella, lo único bueno que le quedaba, te ruega que lo mates.",
        "Y luego está Malenia.",
        "Mientras Miquella se iba a la Tierra de las Sombras a buscarse consorte, su hermana se quedó esperándolo en el Árbol Sagrado. Su yelmo lo dice: Malenia esperó a Miquella a los pies del cascarón.",
        "Y en el mismo yelmo, ella insiste: mi hermano cumplirá su promesa.",
        "Malenia perdió un brazo, una pierna y los ojos por culpa de la putrefacción. Peleó por él, se pudrió por él, y lo esperó al pie de un capullo que ya estaba vacío.",
        "Ese árbol se regó desde que era un retoño con la propia sangre de Miquella, y aun así nunca llegó a ser un Árbol Áureo.",
        "Y su guardiana sigue ahí, esperando a alguien que ya se había ido a casarse con otro. Si llegas hasta ella, la vences tú. Y Miquella nunca vuelve.",
        "Dejó a su amor en un agujero, a su hermana esperando en un árbol, y a sus seguidores con un encanto que caducaba. Y ni así es lo peor.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno, el que más miedo da, y el que pasa delante de tus narices en la pelea final sin que lo notes.",
        "Lo que Miquella quería hacer con todos nosotros.",
        "Miquella no quería solo ser un dios. Quería empezar una era nueva: la era de la compasión.",
        "Suena precioso. Hasta que lees qué significa.",
        "La Diadema de luz, la corona que llevaba al volver con su forma divina, dice que ese círculo iba a ser la base sobre la que se construiría la era de la compasión de Miquella.",
        "Y su milagro, la Luz de Miquella, explica el plan con una frase que hay que leer dos veces: Miquella quiso aceptar todo lo que era y lo que sería, pero encontró a uno que se negó a ser abrazado.",
        "Y ese alguien que se negó eres tú.",
        "Ansbach lo describe mejor que nadie: puro y radiante, Miquella usa el amor para limpiar el corazón de los hombres.",
        "Limpiar el corazón. Como quien limpia un disco duro. Lo formatea, y lo deja como nuevo, sin nada de lo que había antes.",
        "Ahora escucha lo que te dice en la pelea, cada vez que te agarra.",
        "Te lo prometo: un viaje de mil años guiado por la compasión.",
        "Señor del viejo orden, vayamos juntos.",
        "Y si llevas puesta su runa partida, la que resiste encantos, la frase cambia: que tus pensamientos sean solo de amor.",
        "Solo de amor. No de rabia, ni de dudas, ni de nada. Solo lo que él decida que sientas.",
    ]},
    {"id": "p1b", "frases": [
        "La era de la compasión de Miquella es el mundo entero convertido en su grupo de seguidores: todos tranquilos, todos unidos, todos enamorados de él, y nadie con voluntad propia.",
        "Sin encanto, Leda dice que se habrían matado a primera vista. Con encanto, se querían. Y la diferencia entre las dos cosas es que nadie pudo elegir. Es la paz de un cementerio, pero con flores, y con todos sonriendo.",
        "Por eso hasta los suyos lo quieren parar. Thiollier, que daría todo por Santa Trina, te jura antes de pelear contra Leda: vengo a cumplir el único deseo de Santa Trina. Detendré a Miquella el Bondadoso. Jamás será un dios.",
        "Y Ansbach, si cae peleando a tu lado en la batalla final, te pide una sola cosa: Sinluz justo, conviértete en nuestro nuevo señor. Un señor no para los dioses, sino para los hombres.",
        "Lo más perturbador está en las últimas palabras de Leda, que muere protegiéndolo: deseaba que Miquella hiciera del mundo un lugar más amable.",
        "Más amable. Una mujer que cazó a sus propios compañeros por él, muriendo convencida de que lo hacía por un mundo más amable.",
        "Esa es la atrocidad número uno. No quería tu cuerpo, como con Mohg. Ni tu alma, como con Radahn. Quería tu voluntad.",
        "Quería que lo quisieras sin poder evitarlo, para siempre, y llamarle a eso compasión.",
        "Y cuando lo vences, la Diadema de luz que te queda ya empieza a desvanecerse en la nada. La era de la compasión se quedó en una corona que se borra sola.",
        "Mi postura es simple. Márika rompió el mundo, y el tal Radagon dejó a una reina abrazando un huevo, pero por lo menos con ellos sabías que te estaban haciendo daño.",
        "Miquella es el único que te hace daño y encima consigue que le des las gracias.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Miquella pasó de víctima secuestrada a titiritero de media Tierra de las Sombras, y casi nadie lo vio venir porque es chiquito y tiene el pelo dorado.",
        "Ahora la pregunta, y quiero leer tu respuesta en los comentarios: quién fue peor, Miquella, que te quería quitar la voluntad, o Márika, que partió el mundo entero.",
        "Si quieres comparar, en el canal tienes las cinco peores atrocidades de Márika y las cinco de Radagon. Con este ya tienes a toda la familia, y créeme, ninguno sale bien parado.",
        "Y si este formato largo te gustó, dímelo también, porque es la primera vez que le dedico veinte minutos a un solo dios, y todavía no sé si contarlo como lore o como terapia.",
        "Y la próxima vez que alguien te diga que en su grupo todos se llevan de maravilla, pregúntale quién paga las cervezas. Y si es un niño rubio dentro de un capullo, sal corriendo.",
    ]},
]
