# -*- coding: utf-8 -*-
"""Crónicas de Tamriel — «Las 15 misiones de Skyrim que NUNCA debes hacer» (19-oct-2026). Meta: ≥ 14 min (el usuario).
Fórmula de `tes_misiones_daedricas` (9 141 vistas en 5 días, ×4 la mediana del canal) cambiando UNA variable: sale de lo
daédrico (ningún príncipe; no repite ninguna misión de aquel video) y sube a 15 puestos para llegar a 14 min.
Refs. de fuera: «NÃO FAÇA ESSA MISSÃO» ×425, SmackerUnknown «Most Hated Quest» ×6,6. Motor SECUENCIA YT + MG `nucleo/mg_tes.py`,
voz Chatterbox «Sarcastica», sin patrocinio, gema del canal, puente final a «Las 8 misiones daédricas PROHIBIDAS» (O2ZsE2AFGYc).
Datos verificados el 19-oct-2026 en UESP (en.uesp.net, wikitexto por la API): No Stone Unturned (24 piedras, Vex, cueva de
Tolvald de 3 niveles con falmer, 3 fantasmas, Prowler's Profit), Arniel's Endeavor (10 engranajes de peso 10, 2-3 viajes,
gema deformada, bastón de Tandil en mazmorra al azar, convector, mensajero muerto, Keening, desaparece al 3.er golpe, Arniel's
Shade), Lost to the Ages (Aetherium Wars, temblor en Arkngthamz, Katria muerta «quite the fall», 4 fragmentos, forja de Bthalft:
corona/escudo/bastón y «only one can be made»), Blood on the Ice (Jorleif arresta a Wuunferth «without any reward whatsoever»;
3 días después otro asesinato y «you aren't such a sharp investigator»; asesino Calixto; bug del asesinato que no salta),
Dampened Spirits (Maven, Mallus, Sabjorn adelanta 500 si lo persuades, cata del capitán Caius, Mallus al mando, Sabjorn preso,
deuda de Mallus), The Forsworn Conspiracy + No One Escapes Cidhna Mine (Eltrys muerto en el santuario de Talos, «under arrest
for murder and conspiracy», ni thane ni Gremio ni soborno, «the rest of your days», sin equipo, shiv por skooma, Madanach),
The Blessings of Nature (Gildergreen, Eldergleam anterior a los atmoranos, Nettlebane de la bruja cuervo, Maurice reza y sale un
brote; si cortas: Maurice ataca, spriggans que matan a los fieles), Lights Out! (Jaree-Ra, faro de Soledad, Icerunner, «may even
be grateful», marineros muertos, Deeja, nota), With Friends Like These... («We know.», Astrid, 3 cautivos, «it doesn't matter
which captive»), Narfi + Contract: Kill Narfi + The Straw that Broke (Reyda en el río, mentirle), Laid to Rest (Hroggar, Alva,
Helgi, escondite de noche, Laelette esposa de Thonnir, quiso convertir a la niña), Bound Until Death + Vittoria Vici (prima del
Emperador, Asgeir capa de la tormenta, discurso, gárgola de Babette, el Emperador «forced to visit Skyrim»), To Kill an Empire +
Death Incarnate + Hail Sithis! (Gourmet, raíz de jarrin, doble, Maro en el puente, santuario en llamas, Astrid, Katariah,
Motierre), Destroy the Dark Brotherhood! (Maro, 3 000 monedas, lo que se pierde: Shadowmere, ≥ 20 000, maestros Babette/Nazir,
armadura antigua, Cicero), Paarthurnax (ultimátum de Delphine, sin recompensa, Arngeir «we are men of peace, and you are not»,
«beyond my powers of forgiveness», Delphine y Esbern esenciales).
"""

TITULO = "Las 15 misiones de Skyrim que NUNCA debes hacer"
ARCHIVO = "tes_misiones_nunca"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 90
VOZ = dict(referencia="C:/chatterbox_voices/Sarcastica.mp3", idioma="es",
           exaggeration=0.6, cfg_weight=0.35, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# "Skyrim": "Eskaai rim" (no «Eskáirim»: en frase se comprime a «Skirim», docs/voz.md punto 10).
FONETICA = {
    "Skyrim": "Eskaai rim", "Barenziah": "Barenzía", "Vex": "Veks", "Riften": "Ríften", "falmer": "fálmer",
    "Arniel Gane": "Árniel Guéin", "Arniel": "Árniel", "dwemer": "duémer", "Morrowind": "Mórouind",
    "Aetherium": "Etérium", "Katria": "Kátria", "Wuunferth": "Vúnferz", "Calixto": "Calíxto",
    "Maven": "Méiven", "Honningbrew": "Jóningbru", "Sabjorn": "Sábiorn", "Mallus": "Málus",
    "Markarth": "Márkarz", "Eltrys": "Éltris", "Talos": "Tálos", "Cidhna": "Sídna", "skooma": "skúma",
    "forsworn": "forsuórn", "Madanach": "Madának", "Kynareth": "Kínaret", "Danica": "Dánica",
    "Eldergleam": "Élderglim", "spriggans": "esprígans", "Jaree-Ra": "Yarí Rá", "Icerunner": "Áis raner",
    "Deeja": "Díya", "Astrid": "Ástrid", "khajiita": "kayíta", "Ivarstead": "Ívarsted", "Narfi": "Nárfi",
    "Reyda": "Réida", "Nazir": "Nazír", "Morthal": "Mórzal", "Hroggar": "Rógar", "Helgi": "Jélgui",
    "Laelette": "Laelét", "Vittoria Vici": "Vitória Víchi", "Babette": "Babét", "Gourmet": "Gurmé",
    "Maro": "Máro", "Shadowmere": "Shádoumir", "Cicero": "Chícero", "Paarthurnax": "Parzúrnax",
    "Alduin": "Álduin", "Delphine": "Delfín", "Esbern": "Ésbern", "Arngeir": "Árnguéir",
}

# Whisper escribe distinto los nombres (Armiel, Maben, Saphorn, Mayus, Cidna, Tane del Hal, Quinares, Izeruner, cajita, Rogar,
# Alba, Delfine, Svern, Argeir): transcripciones leídas una por una el 19-oct; el resto de la frase sale entero
CER_MAX_POR_FRASE = {"p15_4": 0.02, "p14_0": 0.035, "p14_7": 0.03, "p15_0": 0.065, "p11_1": 0.02, "p11_2": 0.03, "p11_6": 0.03,
                     "p11_8": 0.03, "p10_4": 0.035, "p10_6": 0.035, "p9_1": 0.045, "p8_2": 0.025, "p7_4": 0.02,
                     "p5_1": 0.015, "p5_2": 0.045, "p5_3": 0.015, "p1_3": 0.03}
# «Barenziah» = «Barenzía»: Whisper oye «Varencia/Valencia» en las 4 tomas (b = v; s4 es la más cercana)
# pausa larga a propósito antes de «Lo sabemos.»
GAP_MAX_POR_FRASE = {"p7_1": 0.70}
# frases de > 9 s que hablan hasta el final (CER ~0 y la transcripción acaba bien)
TAIL_MAX_POR_FRASE = {"p15_4": 0.36, "p14_6": 0.36, "p7_1": 0.28, "p4_7": 0.47, "p9_6": 0.43, "p1_7": 0.50, "p10_3": 0.48}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={"scene-033": 0.09},   # 21-oct: logo «msi» del video de origen arriba a la derecha (x 0,92-0,99 · y 0,01-0,05)
    yt=dict(sufijo="Skyrim", min_s=90, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives"]),   # heredados de tes_*
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Nordic fantasy orchestral underscore like a classic open-world RPG soundtrack: low male choir, "
           "frame drums, cello and viola, distant horns, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("ominous and sly, low choir hum and a single horn, a warning before a long list", 6),
        "p15": ("wry treasure hunt, plucked strings and light chimes, endless searching", 3),
        "p14": ("eccentric mage laboratory, ticking clockwork percussion, curious woodwinds", 4),
        "p13": ("ancient underground ruins, echoing drums, ghostly female choir pad", 4),
        "p12": ("cold snowy city at night, tense pizzicato and low strings, a murder mystery", 5),
        "p11": ("comic sabotage in a brewery, sneaky pizzicato, bassoon, mischief", 3),
        "p10": ("grim prison mine, heavy pickaxe-like percussion, low brass, oppression", 6),
        "p9": ("sacred cavern with an ancient tree, warm harp and soft choir, then threat", 5),
        "p8": ("stormy sea coast at night, rolling drums, a shipwreck and betrayal", 6),
        "p7": ("dark locked room, sparse heartbeat drum, whispering strings, dread", 6),
        "p6": ("sad and tender, solo cello and soft piano-like harp, mountain village", 4),
        "p5": ("ghost story of a lost child, music box tones and faint choir, eerie sorrow", 5),
        "p4": ("elegant wedding turning to tragedy, stately strings that darken", 6),
        "p3": ("grand imperial conspiracy, rising war drums, choir, then burning loss", 8),
        "p2": ("hollow victory, solemn low brass and strings, a cold reckoning", 7),
        "p1": ("mountain summit above the clouds, vast choir and deep drums, grief and awe", 9),
        "cierre": ("calm after the storm, warm low strings, a wry final note fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        # estimado con 3 026 palabras ≈ 17 min: ~115-130 s por tramo
        (["intro", "p15"], "Begin softly from near silence with a low choir hum. End on a sustained low string tone."),
        (["p14", "p13"], "Begin on a sustained low string tone. End on an echoing held note."),
        (["p12", "p11"], "Begin on an echoing held note. End on a soft held chord."),
        (["p10", "p9"], "Begin on a soft held chord. End on a quiet suspended note."),
        (["p8", "p7"], "Begin on a quiet suspended note. End on a dark held drone."),
        (["p6", "p5"], "Begin on a dark held drone. End on a fragile held note."),
        (["p4", "p3"], "Begin on a fragile held note. Build to a dramatic peak, then fall to a cold held tone."),
        (["p2"], "Begin on a cold held tone. Stay solemn and restrained. End on a low held note."),
        (["p1", "cierre"], "Begin on a low held note. Climb to a vast peak, then settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Hay una misión en Skyrim en la que el juego te pide que mates al único dragón que te ayudó a salvar el mundo. Y cuando lo haces, nadie te da ni una moneda.",
        "No es un error, ni una broma escondida de los programadores. Está en la historia principal, esperando a que digas que sí.",
        "Y no es la única. Skyrim está lleno de encargos que parecen normales y terminan con un barco en el fondo del mar, una boda arruinada, o semanas de tu vida tiradas a la basura.",
        "Así que hoy van las quince misiones de Skyrim que NUNCA deberías hacer, de las que solo te roban tiempo a las que te roban el alma.",
        "Las daédricas ya tuvieron su propio video, así que aquí no sale ningún príncipe. Esta vez los monstruos son los mortales.",
        "Y te adelanto algo. Hay una facción que va a aparecer más de una vez en esta lista, y no es la que estás pensando. Bueno, sí, probablemente sí.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Las piedras de Barenziah.",
        "Un día recoges una gema rara de un cofre o de una estantería, y el juego te apunta una misión nueva. Encontrar las otras veintitrés.",
        "Veinticuatro piedras repartidas por toda la provincia. En palacios, en templos, en guaridas y en ruinas llenas de falmer.",
        "No hay mapa, no hay marcador, no hay pistas. Y muchas están en sitios donde cogerlas cuenta como robo, así que de regalo te puedes llevar una multa.",
        "Cuando por fin tienes las veinticuatro, Vex, del Gremio de Ladrones de Riften, te manda a recuperar la corona a una cueva de tres niveles llena de falmer.",
        "Y cuando la tocas, salen tres fantasmas a darte la bienvenida.",
        "¿Y el premio? Una bendición permanente que hace que encuentres más gemas en los cofres.",
        "O sea, que después de semanas buscando gemas, el juego te premia con más gemas.",
        "Está en el último puesto porque, al menos, no le hace daño a nadie. Solo a tu calendario.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, el experimento de Arniel.",
        "En el Colegio de Hibernalia vive un mago, Arniel Gane, que tiene un proyecto secreto y se niega a decirte de qué va.",
        "Primero te pide diez engranajes dwemer. Cada uno pesa diez, así que vas a hacer dos o tres viajes con la mochila reventada.",
        "Luego te manda a por una gema de alma deformada, y para conseguirla tienes que recuperar un bastón robado del jefe de una mazmorra al azar.",
        "Después, a cargar esa gema en las máquinas de una ruina dwemer, como si fuera una batería.",
        "Y al final, a buscar a un mensajero que nunca llegó desde Morrowind. Lo encuentras muerto, junto al paquete. Dentro hay una daga legendaria de los dwemer.",
        "Arniel la agarra, golpea la gema, y no pasa nada. Golpea otra vez, y nada. Pierde la paciencia, golpea una tercera vez, y desaparece en un destello de luz. Para siempre.",
        "Querías saber qué les pasó a los dwemer. Felicidades, ahora sabes qué le pasó a Arniel.",
        "El juego te deja un hechizo para invocar su fantasma, que es lo más cerca que vas a estar de cobrarle.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. La forja de Aetherium.",
        "Todo empieza con un libro que habla de un cristal rarísimo, el Aetherium, y de una forja perdida donde los dwemer lo convertían en armas.",
        "En la primera ruina te recibe un temblor de tierra y la voz de Katria, una exploradora que llegó antes que tú.",
        "Ella misma te enseña dónde quedó su cuerpo. Se cayó. Y lo cuenta con una calma que da escalofríos.",
        "A partir de ahí, cuatro ruinas dwemer a la caza de cuatro fragmentos, con un fantasma de guía, falmer, autómatas y rompecabezas de resonadores.",
        "Y cuando por fin llegas a la forja, el juego te da a elegir entre tres objetos. Una corona que te deja usar dos piedras guardianas a la vez, un escudo y un bastón.",
        "Pero solo puedes forjar uno. El fragmento se consume, y las otras dos piezas se pierden para siempre.",
        "Horas de ruinas para una sola decisión, y sin guardar partida antes, ni siquiera puedes probar las otras dos.",
        "Katria, eso sí, se despide de ti con mucho cariño. Ella ya descansa. Tú te quedas con la duda.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, un asesino en serie en Ventalia.",
        "Al cruzar la ciudad de noche te encuentras a una mujer recién apuñalada, y a un guardia que no sabe ni por dónde empezar.",
        "Le llaman el Carnicero, y no es su primera víctima.",
        "Sigues las pistas, encuentras una casa abandonada con un altar de nigromante y un amuleto, y todo apunta a Wuunferth, el mago de la corte.",
        "Y aquí es donde cae casi todo el mundo. Si le cuentas tus sospechas al mayordomo del jarl, arrestan al mago al instante, te dan las gracias, y ni una moneda.",
        "Tres días después vuelves a la ciudad, y hay otro cadáver en la calle. El guardia te mira y te suelta que no eras tan buen investigador como creías.",
        "Porque el Carnicero era Calixto, el señor amable del museo, el que te explicó con todo detalle la historia del amuleto.",
        "Y por si fuera poco, es una misión famosa por sus errores. Si el siguiente asesinato no se dispara, se queda colgada en tu diario para siempre.",
        "Un asesino suelto, un inocente en la cárcel, y una misión rota. En Ventalia es un martes cualquiera.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Envenenar una meadería.",
        "En el Gremio de Ladrones, Maven, la dueña de media Riften, quiere hundir a su competencia, la meadería Honningbrew, al lado de Carrera Blanca.",
        "Así que te presentas ante Sabjorn, el dueño, como el exterminador que le va a limpiar el sótano de ratas.",
        "Él te da la llave, y si le hablas bonito, hasta te adelanta la mitad del pago.",
        "Tú bajas, matas a las ratas, y le echas veneno a la cuba de la cata más importante del año.",
        "Porque quien prueba ese aguamiel es, nada menos, el capitán de la guardia de Carrera Blanca.",
        "El capitán escupe, culpa a la suciedad, deja la meadería en manos de Mallus, el hombre de Maven, y se lleva a Sabjorn a la cárcel a punta de espada.",
        "Y el resto del pago ya no lo ves nunca. Es difícil cobrarle a un hombre que acabas de meter en una celda.",
        "Lo más gracioso es que Sabjorn tampoco era un santo. Tenía a Mallus trabajando gratis, atrapado en una deuda que no podía pagar.",
        "En esta historia no gana nadie limpio. Solo Maven, como siempre.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, la cárcel de la que nadie sale.",
        "En el mercado de Markarth ves un asesinato a plena luz del día, y un hombre llamado Eltrys te pide que averigües qué está pasando en la ciudad.",
        "Investigas, tiras del hilo, y descubres una conspiración que llega hasta la familia más rica de Markarth.",
        "Y cuando vas a contárselo a Eltrys, lo encuentras muerto en el santuario de Talos, rodeado de tres guardias que te arrestan por asesinato y conspiración contra la ciudad.",
        "Da igual que seas thane del jarl, que seas del Gremio, o que les ofrezcas oro. Te mandan a la mina de Cidhna para el resto de tus días.",
        "Y entras sin nada. Sin armadura, sin armas, sin las cincuenta horas de botín que llevabas encima.",
        "Para salir, tienes que conseguir un cuchillo a cambio de skooma, llegar hasta el Rey Harapiento, el líder de los forsworn, y elegir. Escapar con él, o matarlo.",
        "Es una gran misión, de verdad. El problema es que nadie te avisa de que vas a acabar picando piedra en ropa interior.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Talar el árbol más antiguo de Skyrim.",
        "En Carrera Blanca, delante del templo de Kynareth, hay un árbol sagrado que un rayo dejó seco.",
        "La sacerdotisa Danica te pide savia del árbol del que nació, el Eldergleam, un gigante de miles de años que ya estaba ahí antes de que llegaran los primeros nórdicos.",
        "Pero ese árbol no se corta con un arma cualquiera, así que te manda a quitarle a una bruja cuervo la daga que hicieron para matar spriggans.",
        "Y en la cueva, delante del árbol, el peregrino que se te pegó por el camino te ruega que no lo hagas. Dice que puede pedirle un brote a la diosa, solo rezando.",
        "Si le haces caso, del suelo sale un retoño, y todo el mundo contento.",
        "Si no, le clavas la daga al árbol más viejo de la provincia, el peregrino se te echa encima, y salen spriggans por todas partes, que suelen acabar con los fieles que vivían en paz en el santuario.",
        "Y luego vuelves a Carrera Blanca, y Danica te recibe encantada con el árbol otra vez en flor. Nadie le cuenta lo que costó.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, apagar un faro.",
        "En el puerto de Soledad, un argoniano llamado Jaree-Ra te ofrece ganar un dinero fácil. Solo tienes que apagar el fuego del faro.",
        "Un barco, el Icerunner, está a punto de llegar. Sin la luz, se estrella contra las rocas, y su banda se queda con la carga.",
        "Y te jura que a la tripulación no le va a pasar nada. Que hasta les van a hacer un rescate heroico, y que te lo van a agradecer.",
        "Subes, apagas el fuego, y cuando llegas al naufragio, todos los marineros están muertos.",
        "Abajo, en la bodega, te espera Deeja, la hermana de Jaree-Ra, que te dice que estaba deseando conocerte, y que vas a recibir lo que te mereces.",
        "En su cuerpo encuentras una nota. Su hermano le pedía que te matara en cuanto llegaras.",
        "Hundiste un barco entero para que te pagaran con una puñalada. Y al final, el que más tiene que esconder eres tú.",
    ]},
    {"id": "p7", "frases": [
        "Número siete, y aquí entra la facción que te prometí. La Hermandad Oscura.",
        "Si en Ventalia le haces el encargo a un niño que quiere ver muerta a la directora de su orfanato, un tiempo después te llega una nota con dos palabras. Lo sabemos.",
        "Te vas a dormir, y te despiertas en una cabaña abandonada, con Astrid sentada encima de un armario y tres desconocidos atados delante de ti.",
        "Le robaste un contrato a la Hermandad, y lo tienes que pagar. Una vida por otra.",
        "Uno de los tres tiene un contrato encima. Un mercenario, una madre de seis hijos que no para de gritar, y un khajiita que presume de ladrón y de asesino.",
        "La puerta está cerrada, y no sales de esa habitación hasta que alguien muera.",
        "Y lo peor viene después. Da igual a quién elijas. El juego nunca te dice quién era el del contrato.",
        "Matas a un desconocido atado, solo para que te den la contraseña de una puerta.",
        "Guárdate esta cabaña en la memoria, porque vamos a volver a ella más adelante.",
    ]},
    {"id": "p6", "frases": [
        "En el seis, el contrato más triste de todo Skyrim.",
        "Al otro lado del río de Ivarstead, en las ruinas de la casa de sus padres, vive Narfi, un mendigo que no está bien de la cabeza.",
        "Habla de sí mismo en tercera persona, y se pasa el día buscando a su hermana Reyda, que salió a recoger plantas hace un año y nunca volvió.",
        "Solo quiere encontrarla para poder despedirse de ella, como se despidió de su padre y de su madre.",
        "Y en uno de los primeros contratos de la Hermandad, Nazir te lo encarga. Te dice que es un mendigo indefenso, y que es fácil, hasta para ti.",
        "Narfi no se defiende. Ni siquiera sale corriendo.",
        "Y si antes buscas a Reyda, la encuentras en el fondo del río. Entonces puedes elegir. Decirle a Narfi la verdad, o mentirle y decirle que su hermana pronto vuelve a casa.",
        "Si le mientes, se pone feliz. Te dice que va a esperar a su hermana hasta que vuelva.",
        "Y luego vuelves con la daga, a ver si sigue esperando.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Jugar al escondite con una niña muerta.",
        "En Morthal, todo el pueblo murmura sobre la casa de Hroggar, que ardió con su mujer y su hija dentro.",
        "Y al día siguiente, Hroggar ya vivía con otra, una tal Alva.",
        "Cuando registras las cenizas, aparece el fantasma de Helgi, la hija, y te cuenta cómo murió en el fuego.",
        "Pero sigue siendo una niña. Así que te propone un juego. Si la encuentras de noche, te dice quién quemó la casa.",
        "Solo te avisa de una cosa. Hay otro jugador, y a ella le da miedo que la oiga.",
        "De noche, en su tumba, el otro jugador ya está ahí. Es Laelette, una vampira, la esposa desaparecida de un vecino del pueblo.",
        "Laelette quemó la casa obligada, e intentó salvar a la niña convirtiéndola en vampira. Pero ya era tarde.",
        "Y tú tienes que matarla, y después ir a contárselo a su marido.",
        "La culpable de verdad era Alva, otra vampira, que dormía en un ataúd en su casa, con Hroggar dispuesto a defenderla.",
        "Hay misiones que dan miedo. Esta da pena, y eso es mucho peor.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, la boda.",
        "En Soledad, frente al Templo de los Divinos, se casa Vittoria Vici, prima del mismísimo Emperador, con un capa de la tormenta de Riften.",
        "Es una boda para hacer las paces. Imperiales y capas de la tormenta celebrando juntos, como iguales.",
        "Y la novia va de invitado en invitado, repitiendo que es un día de paz y de felicidad.",
        "Tu contrato es ella. Y si la matas mientras da su discurso desde el balcón, la Hermandad te paga un extra.",
        "Babette, la vampira de la Hermandad, hasta te da una idea. Hay una gárgola muy vieja justo encima del balcón, y lo viejo se cae.",
        "Así que esperas a que la novia empiece a hablar, empujas la estatua, y la fiesta de la paz termina con todos los guardias de Soledad buscándote.",
        "Y todo esto, ¿para qué? Para que el Emperador no tenga más remedio que venir a Skyrim. La boda nunca fue el objetivo. Era el cebo.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Matar al Emperador.",
        "Te haces pasar por el Gourmet, el cocinero más famoso del Imperio, y entras en la cocina del castillo de Soledad.",
        "La cocinera está tan emocionada de trabajar contigo que te deja echarle a la sopa tu ingrediente secreto. Una raíz venenosa.",
        "El Emperador prueba la sopa, cae muerto, y sales por la puerta como el héroe de la Hermandad.",
        "Hasta que en el puente te espera el comandante Maro con sus hombres, y te suelta la verdad. El que acabas de envenenar era un doble.",
        "Alguien de la Hermandad te vendió.",
        "Y cuando vuelves al santuario, está ardiendo. Tus compañeros, muertos. Y la traidora era Astrid, la misma que te dio la bienvenida a la familia.",
        "Al final sí matas al Emperador de verdad, en su barco. Y él, antes de morir, solo te pide una cosa. Que mates también al hombre que pagó por su muerte.",
        "Es la misión más épica de la Hermandad, y la que más cara te cobra.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Destruir la Hermandad Oscura.",
        "Vuelve a la cabaña del número siete. En vez de matar a uno de los rehenes, puedes matar a Astrid.",
        "Parece lo correcto. Se lo cuentas a un guardia, te mandan con el comandante Maro, y él te da la contraseña del santuario para que entres solo y acabes con todos.",
        "Y lo haces. Limpias el santuario, vuelves, y Maro te paga tres mil monedas, y promete que el Emperador en persona va a oír hablar de ti.",
        "Suena bien, hasta que haces la cuenta de lo que acabas de tirar.",
        "Sin Hermandad no hay Shadowmere, el caballo negro de ojos rojos. No hay, como mínimo, veinte mil monedas en contratos.",
        "No hay maestros de Alquimia ni de Armadura ligera, ni la armadura antigua de la Hermandad, ni Cicero como seguidor.",
        "Tres mil monedas a cambio de todo eso.",
        "Y lo más irónico es que, por todo lo que hemos visto, la Hermandad se lo había ganado. Pero el juego castiga al que hace lo correcto, y premia al que envenena sopas.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. El dragón del principio.",
        "En lo más alto de la Garganta del Mundo vive Paarthurnax, un dragón viejísimo que te enseña a gritar como los dragones, y que lucha a tu lado contra Alduin.",
        "Es el maestro de los Barbagrises, y lleva miles de años intentando ser mejor de lo que fue.",
        "Pero las Cuchillas, Delphine y Esbern, no le perdonan lo que hizo en la guerra de los dragones, cuando era la mano derecha de Alduin.",
        "Y te dan un ultimátum. Hasta que no lo mates, no tienen nada de qué hablar contigo.",
        "Si aceptas, subes a la montaña, matas al dragón que te enseñó todo lo que sabes, y vuelves.",
        "¿La recompensa? Ninguna. Las Cuchillas no te dan nada. Lo único que sacas es lo que se le cae al dragón.",
        "Y cuando vuelves con Arngeir, el líder de los Barbagrises, te dice que así pagaste su confianza, con una venganza sin sentido. Que ellos son hombres de paz, y tú no.",
        "Y desde ese día, lo único que te dice es que el asesinato de Paarthurnax está más allá de lo que él puede perdonar.",
        "Mataste a tu maestro, a cambio de nada, para que dos personas a las que el juego ni siquiera deja morir te volvieran a dirigir la palabra.",
        "Por eso es el número uno. Las demás te cuestan oro, tiempo o un barco. Esta te cuesta lo único que Skyrim no te devuelve. Un amigo.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es mi lista. Quince misiones que Skyrim te deja hacer y que nunca deberías hacer, de una corona llena de gemas a un dragón que no pedía nada.",
        "Si hay una misión de la que tú te arrepientes, déjala en los comentarios, que los leo todos.",
        "Y si te quedaste con ganas de más, en el canal tienes las ocho misiones daédricas PROHIBIDAS de Skyrim, donde los monstruos sí son príncipes.",
        "Y la próxima vez que alguien en Skyrim te ofrezca dinero fácil, acuérdate del faro. En este juego, el dinero fácil siempre se cobra en sangre.",
    ]},
]
