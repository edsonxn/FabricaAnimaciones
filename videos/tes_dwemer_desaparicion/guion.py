# -*- coding: utf-8 -*-
"""GUION — «¿Qué pasó con los DWEMER? Los 20 secretos de su desaparición que Skyrim te esconde» (Crónicas de Tamriel, 4-nov-2026).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Datos verificados en UESP:
_investigacion.md (36 fuentes). Tema pedido por @chuymoreno6820 en el video de Sentinel.
El usuario (4-nov-2026): 24 minutos, «a la gente le gustó el uso de varias voces como el último» → misma fórmula que
tes_sentinel_teaser: SIETE voces de ElevenLabs que compiten (Johnny presenta) + el Humano tras el Telón (voz clonada del usuario,
cuentas 2 y 3), que esta vez narra un secreto. Ronda 2 con el RECUENTO REAL de los comentarios de Sentinel (4-nov, primeras horas):
el Profeta 4 · Hope 2 · MariCarmen 2 · Johnny 2 · Edoardo, José y Mario 0 → los de cero votos se juegan el puesto; el Profeta,
que va primero, se lleva los cinco últimos. Turbo, corchetes SIN [whispers] ni [excited].
Comentarios (≤ 10 días): queja justa de @federicoherrera2105 («jarl» se dice «yarl») → corregido (FONETICA) junto con «Oblivion»
(otra queja, del 15-oct, que no se enseña por vieja); críticas con burla: «Que ridícula la voz femenina» (contestan Hope y
MariCarmen) y «se nota que kyrim no es lo tuyo»; 5 agradecimientos.
"""

TITULO = "¿Qué pasó con los DWEMER? Los 20 secretos de su desaparición que Skyrim te esconde"
ARCHIVO = "tes_dwemer_desaparicion"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HMCmDsbKeaSZp5LMOYKR", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), referencia=r"C:\chatterbox_voices\Sarcastica.mp3",
           por_cuenta={2: "GUEeiSJYQQdbv0NJ86Im", 3: "hCU4QZdzzUliy58ezPBz"})   # el Humano tras el Telón (clon del usuario) en las cuentas 2 y 3
# ElevenLabs dice el inglés nativo: aquí lo que se oyó mal en videos anteriores (quejas del público: «Oblivión» agudo, «jarl»)
FONETICA = {"Oblivion": "Oblívion", "jarl": "yarl", "Jarl": "Yarl", "Mzark": "Mzárk", "Mzulft": "Mzúlft",
            "Nchuand-Zel": "Nchuand Zel", "Bamz-Amschend": "Bamz Ámschend", "1E 700": "primera era, setecientos"}

# Whisper escribe distinto los nombres (Gellivor, Vivek, «arroba…»): tomas comprobadas por la hipótesis (s3, 4-nov-2026)
CER_MAX_POR_FRASE = {'intro_3': 0.062, 'voces_1': 0.032, 'p19_5': 0.035, 'p18_3': 0.044, 'cr1_0': 0.056, 'cr1_2': 0.021, 'p16_3': 0.023, 'p15_5': 0.037, 'p15_6': 0.017, 'p14_2': 0.024, 'p14_4': 0.024, 'p13_3': 0.094, 'p13_4': 0.04, 'ag1_0': 0.049, 'ag1_1': 0.124, 'ag1_2': 0.086, 'p12_2': 0.028, 'p12_3': 0.06, 'p11_1': 0.028, 'p11_3': 0.041, 'p11_4': 0.055, 'p11_6': 0.026, 'p10_4': 0.02, 'cr2_0': 0.147, 'p9_0': 0.017, 'p9_3': 0.033, 'p9_5': 0.02, 'p7_5': 0.025, 'p6_1': 0.016, 'p6_5': 0.018, 'p5_1': 0.018, 'p5_5': 0.019, 'p4_2': 0.031, 'p4_3': 0.026, 'cr3_0': 0.091, 'cr3_1': 0.033, 'cr3_2': 0.018, 'p3_3': 0.017, 'p2_1': 0.029, 'p2_5': 0.021, 'p1_1': 0.022, 'p1_2': 0.035, 'cierre_3': 0.186, 'cierre_5': 0.041, 'cierre_6': 0.036, 'voces_5': 0.16}
# ElevenLabs no alucina colas: tail_ratio > 1 es medida, no error
TAIL_MAX_POR_FRASE = {'intro_3': 1.3, 'p15_4': 1.39, 'p6_3': 1.24, 'cierre_10': 1.12}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial (Morrowind y Skyrim de Jeremy Soule + ESO de Brad Derrick; armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Una raza entera. Ciudades bajo tierra, máquinas de vapor, un dios de latón. Y un día, en un solo instante, nadie.",
        "No dejaron ni una tumba. Solo sus máquinas, que siguen trabajando casi cuatro mil años después, como si el jefe fuera a volver mañana.",
        "[amused] Hoy toca el misterio más grande de The Elder Scrolls. Qué pasó con los dwemer.",
        "Nos lo pidió @chuymoreno6820 en el video de Sentinel: será interesante saber por fin qué pasó con los dwemer. Pues marchando.",
        "Veinte secretos, todos comprobados en UESP, con sus fuentes en la descripción. De por qué los llamas enanos, hasta el momento en que Skyrim te deja repetir la desaparición con tus propias manos.",
        "[short pause] Y como os gustó tanto, vuelven las siete voces. Pero esta vez hay marcador.",
    ]},
    {"id": "voces", "frases": [
        "Recuento de los comentarios de Sentinel, primeras horas. El Profeta, cuatro votos. Hope, dos. MariCarmen, dos. Yo, Johnny, dos.",
        "[deadpan] Y Edoardo, José y Mario. Cero. Ni uno. Ni su madre.",
        "[deadpan] Edoardo. Me tocan el dieciocho y el diecisiete. Cero votos, y aun así sigo siendo el único serio de este canal.",
        "José, para servirte. Dieciséis y quince, los falmer. Y hoy, sin voz de locutor, que me lo pidieron.",
        "Mario. Catorce y trece. Blackreach y la expedición maldita. Prometo correr menos. No mucho menos.",
        "[amused] Hope. Doce, once y diez. Las máquinas que hacen magia. Y sí, con hache.",
        "[deadpan] MariCarmen. Nueve, ocho y siete. El dios de latón. Y al que me robe un voto, ya sabe dónde vivo.",
        "Yo soy el Profeta. Los cinco últimos. [short pause] El que va primero se queda con el final. Así está escrito.",
        "Y el seis es mío. Por fin. El humano tras el telón narra un secreto. Uno. Y os vais a enterar de cómo se hace.",
        "[sarcastic] Qué miedo. Empiezo yo, que alguien tiene que abrir. Y quédate hasta el número uno, porque es lo único que Skyrim te deja hacer que ni los mejores magos de Tamriel consiguieron explicar.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. No eran enanos.",
        "En Skyrim todo es enano. Ruinas enanas, armadura enana, esferas enanas. Y sin embargo, los dwemer no eran bajitos.",
        "Dwemer significa algo así como el pueblo profundo, los elfos de lo hondo. Eran mer, elfos, primos de los altmer y de los elfos oscuros.",
        "Lo de enanos es el nombre que usa el Imperio, y la fábula cuenta de dónde sale: de los gigantes. Para un gigante, cualquier elfo es pequeño, y llamaban así, con cariño, a sus amigos dwemer.",
        "[amused] O sea, que el nombre de una de las razas más listas de Tamriel es un mote de gigante. Como si a ti te bautizara un mamut.",
        "Tenían más apodos. Sotha Sil, uno de los dioses de Morrowind, los llamaba los hijos del latón.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, las máquinas que nadie apagó.",
        "Las arañas, las esferas y los centuriones se llaman animunculi. Y según UESP, siguen funcionando en ciudades perdidas bajo tierra, haciendo el trabajo que les mandaron sus amos.",
        "La araña se esconde en las tuberías y salta. La esfera llega rodando, se despliega y a veces trae ballesta.",
        "Y el centurión espera inmóvil en su soporte de carga. Escupe vapor como si fuera un grito, y sus golpes están a la altura de los de un dragón.",
        "[mischievously] Truco: no puede bajar los brazos ni la cabeza. Si te pegas a sus pies, casi no te toca.",
        "Al caer, siempre suelta su núcleo dinamo y una gema de alma enorme. Y solo uno en todo Skyrim patrulla, el de Bthardamz. Los demás llevan milenios de pie, esperando.",
        "[deadpan] Casi cuatro mil años sin vacaciones. Ni un sindicato. Así cualquiera construye una civilización.",
    ]},
    {"id": "p18", "frases": [
        "[deadpan] Gracias, Johnny. Ahora, en serio. Número dieciocho. Vives dentro de una ciudad dwemer.",
        "Markarth, la capital del Reach, está construida dentro de una antigua ciudad dwemer. Las calles, las cascadas, todo es suyo.",
        "Y el castillo del yarl, Understone Keep, es el viejo palacio dwemer tallado en la montaña. Los humanos solo se mudaron.",
        "Debajo sigue la ciudad original, Nchuand-Zel. Una expedición de magos de Markarth bajó sin hacer caso al sabio de la corte.",
        "Encuentras sus cuerpos y sus diarios uno a uno. Y la última palanca que tocaron vuelve a encender las defensas de los dwemer.",
        "[deadpan] Así que la próxima vez que discutas con el yarl, recuerda que estás en el salón de otro. Y que el dueño no ha dicho que se haya ido.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, el hombre que más sabe de ellos, y la piedra que esconde.",
        "Calcelmo, el mago altmer de Markarth, es según el juego el mayor experto en los dwemer de todo Tamriel. Tiene un museo propio, y te recibe con un aviso: cuidado con las vitrinas, que algunas son muy frágiles.",
        "Su gran obra es traducir el idioma de los falmer. Y su secreto está en lo alto de su torre: una losa enorme, con las dos lenguas grabadas.",
        "En la misión del Gremio de Ladrones, Respuestas difíciles, te cuelas en su torre y le haces un calco a la piedra con carbón y papel.",
        "Pero lo mejor está en sus libros. En Enanos, tercer volumen, Calcelmo avisa: no hay prueba de que desaparecieran en un solo día. Pudieron ser años. O décadas.",
        "Y no descarta nada: una peste, magia contaminada, experimentos con Aetherius, o un viaje a Oblivion.",
        "[deadpan] El mayor experto de Tamriel, y su conclusión es que no sabe. Por eso es el mayor experto.",
    ]},
    {"id": "cr1", "frases": [
        "Una pausa, que hoy toca correo. Y esta vez, con razón. @federicoherrera2105 nos dijo que no podemos decir jarl así como se escribe.",
        "Tiene toda la razón. Se dice yarl. Y de paso hemos corregido otra que nos señalasteis: no es Oblivión, agudo. Es Oblivion.",
        "Gracias, Federico. Ya has oído a Edoardo decirlo bien dos veces. Cuéntalas.",
    ]},
    {"id": "p16", "frases": [
        "José. Número dieciséis. Los falmer no eran monstruos. Los hicieron así.",
        "Antes de ser falmer, eran los elfos de las nieves, los dueños de Skyrim. Cuando llegaron los nórdicos de Ysgramor, los fueron echando hasta casi extinguirlos.",
        "Desesperados, pidieron refugio a sus primos de bajo tierra: los dwemer. Y se lo dieron. A cambio de un precio.",
        "Según UESP, los dwemer obligaron a sus protegidos a comer solo hongos tóxicos, que los fueron convirtiendo en esclavos ciegos.",
        "Las cámaras de tortura que ves en las ruinas, probablemente servían para controlarlos. Y no está claro si bastó el hongo o si hizo falta el paso de generaciones.",
        "[sighs] Al final se rebelaron. La guerra del Risco, la llamaron. Décadas peleando bajo tierra.",
        "Y aquí viene lo bueno: esa guerra acabó de golpe. Porque un día, el enemigo dejó de estar.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, la batalla que nunca empezó.",
        "En el libro Los falmer, un estudio, que puedes leer en una posada de Hibernalia o en el museo de Calcelmo, se cuenta el final de esa guerra.",
        "Los falmer se prepararon para el golpe definitivo. Salieron a buscar a sus enemigos dwemer para la última batalla.",
        "Y se encontraron con que la raza entera había desaparecido.",
        "[deadpan] Imagina preparar durante décadas tu venganza, ensayar el discurso, afilar la espada, y que el otro no se presente. Ni avisa.",
        "Los falmer se quedaron con las ciudades, con las máquinas, y con la oscuridad. Hoy los encuentras en casi cada ruina dwemer de Skyrim, todavía ahí abajo.",
        "Una curiosidad que cuenta el folclore nórdico: Ysgramor les cortaba la nariz a los elfos de las nieves, para distinguirlos de los demás elfos. Por eso los falmer no tienen nariz, según los nórdicos.",
    ]},
    {"id": "p14", "frases": [
        "[amused] Muy bonito, José, pero casi lloro. Número catorce. Hay un mundo entero debajo de Skyrim.",
        "Blackreach. Una caverna inmensa, con luz propia, bajo la comarca de Hibernalia. Y el mapa del juego solo te enseña una parte.",
        "Se entra por tres ruinas: Alftand, al suroeste de Hibernalia; Mzinchaleft, al suroeste de Dawnstar; y Raldbthar, al oeste de Ventalia. Y para abrirlas hace falta una esfera de sintonía.",
        "Abajo hay una ciudad muerta, ahora de los falmer, un observatorio al norte, un lago con cascadas, y hongos gigantes que brillan.",
        "[mischievously] Y sobre la ciudad, un gran globo naranja. Si le lanzas el grito de Fuerza Implacable, viene un dragón: Vulthuryol. Solo una vez.",
        "Además, es el único sitio de Skyrim donde crece la raíz Nirn carmesí. Así que si alguna vez un elfo te pidió treinta, ya sabes dónde lloraste.",
    ]},
    {"id": "p13", "frases": [
        "En el trece, los que bajaron a buscarlos.",
        "Alftand, al suroeste de Hibernalia. Una expedición imperial, la de Sulla Trebatius, excavó el glaciar buscando tesoros dwemer.",
        "Lo que encuentras es su lista de muertos. Valie, en una sala de tortura. Endrast, que huyó de los falmer y murió escondido, con su diario contándolo todo.",
        "Y dos hermanos khajiit. J'zhar, muerto. Y J'darr, con un hacha, de pie sobre el cuerpo de su hermano, y hostil contigo.",
        "[sighs] Los dos últimos, Sulla y Umana, acaban peleándose entre ellos en la catedral. Y casi siempre gana Umana.",
        "[deadpan] Moraleja: los dwemer desaparecieron, y la gente que va a buscarlos tiene la mala costumbre de hacer lo mismo. Pero con menos estilo.",
    ]},
    {"id": "ag1", "frases": [
        "Y otra pausa, esta para dar las gracias. @Miguel_Salvatierra dice que fue un gran trabajo en equipo, y que con las características de cada voz se hizo más interesante.",
        "@MelVal54, muchas gracias. @MoonrakerYo79, gracias por toda la info. Y @ShadowPriestBear dice que estuvo muy, muy bien logrado. Y le da su voto a MariCarmen. Se lo apunto.",
        "[amused] Y @minecrafttv2081 se rio con las siete voces compitiendo. Esa era la idea.",
        "Y aquí salgo yo, el humano tras el telón. Leemos todos los comentarios: los que nos felicitan, los que nos corrigen, y los que votan. Con ellos mejoramos cada video.",
        "[deadpan] Y los que más corrige son los suyos. Que si la música, que si la voz, que si el ritmo.",
        "Porque hace falta. [short pause] Mario, ¿esto era correr menos?",
    ]},
    {"id": "p12", "frases": [
        "[amused] Gracias, señor filtrador. Mario, respira. Me toca. Número doce. Construían con sonido.",
        "Los dwemer tenían arquitectos tonales. La arquitectura tonal es, según UESP, manipular el sonido para cambiar la realidad. Usaban su propia voz, amplificada con collares mágicos.",
        "Y fabricaban resonadores que alteraban el cerebro de hombres y elfos: calma, placer, paranoia o terror.",
        "En Skyrim lo tocas tú. En Arkngthamz, una ruina del Reach, hay una cerradura tonal: cinco resonadores que tienes que golpear en orden.",
        "[mischievously] Cada vez que fallas, el juego te castiga: primero arañas, luego esferas, luego un centurión. Y mientras tanto, una balista dwemer te dispara.",
        "Y fíjate en esto: el jefe de esos arquitectos tonales era Kagrenac. Guárdate el nombre. Va a volver.",
    ]},
    {"id": "p11", "frases": [
        "En el once, la guerra que los dwemer perdieron contra sí mismos.",
        "En Dawnguard, un libro, Las guerras del aeterio, te cuenta que cuatro ciudades dwemer alrededor de Arkngthamz resistieron a los nórdicos durante siglos.",
        "Y se hundieron en solo tres años, peleando entre ellas por armas hechas de aeterio, un cristal azul que brilla.",
        "La misión de la forja la guía Katria, el fantasma de una aventurera que murió en un terremoto dentro de Arkngthamz. Te cuenta que su aprendiz le robó la investigación.",
        "Juntas cuatro fragmentos: de Arkngthamz, del Cruce del Pueblo Profundo, de Raldbthar y de un almacén al sur de Mzulft. Y en las ruinas de Bthalft, un ascensor baja a la forja.",
        "Pero solo puedes hacer una pieza: la corona, que te da dos piedras guardianas a la vez; el escudo, que vuelve etéreo al enemigo; o el báculo, que invoca a una araña o una esfera.",
        "[amused] Y Katria, al irse, te deja su arco, Céfiro, que dispara un treinta por ciento más rápido. Con un encargo: cuídamelo bien.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, la máquina que ve todo Skyrim.",
        "Mzulft, al sur de Ventalia. Los magos del Sínodo imperial montaron allí un proyecto secreto. Los falmer los mataron a casi todos.",
        "El último, Gavros Plinius, muere en tus brazos con una frase a medias: el cristal, ya no está, busca a Paratus, en el oculario.",
        "El oculario es una máquina dwemer de lentes que concentra la luz. Le pones el cristal, la ajustas con escarcha y con fuego, y proyecta un mapa entero de Skyrim.",
        "Y en el mapa aparece lo que el Sínodo buscaba: el bastón de Magnus, en Labyrinthian. Incluso se cuela en la proyección un monje de la Orden Psijic, Nerien.",
        "[amused] Y un dato de bonus: Mzulft es el sitio de Skyrim donde más lingotes dwemer puedes sacar. Hasta cuatrocientos noventa y ocho. Por si te sobra la capacidad de carga. Que no.",
    ]},
    {"id": "cr2", "frases": [
        "Una pausa más, que esta va por nosotras. @GalinaVenegas-d1w nos escribió: qué ridícula la voz femenina.",
        "[amused] ¿Cuál de las dos, Galina? Porque somos dos. Y yo tengo dos votos.",
        "[deadpan] Y yo otros dos. Así que, con mucho cariño, la ridícula empata con Johnny. Y le gana a tres señores.",
        "[amused] Gracias por escucharnos hasta el final, que eso también cuenta. Y si votas, vota por la menos ridícula. Que soy yo.",
        "[deadpan] Lo dejamos en los comentarios.",
    ]},
    {"id": "p9", "frases": [
        "[deadpan] MariCarmen, empiezo. Número nueve. Los dwemer leían los Pergaminos Antiguos con una máquina.",
        "¿Recuerdas al sacerdote de la Polilla que se quedaba ciego leyendo un pergamino? Los dwemer encontraron otra forma.",
        "En la búsqueda principal, Septimus Signus, un erudito que vive en una cueva helada al norte de Hibernalia, te dice que los dwemer escondieron en Blackreach un modo de leer los Pergaminos Antiguos.",
        "Ese modo es el oculario de la Torre de Mzark, en un pináculo al suroeste de Blackreach. Una máquina de lentes colgantes, con un podio de botones y una ranura para un léxico.",
        "Pulsas los botones, las lentes se alinean, y el pergamino baja a tus manos. El de la misión de Dragonrend, el que te enseña el grito para tumbar a Alduin.",
        "[deadpan] Y bajo el podio hay un esqueleto, Drokt. Su diario cuenta que se obsesionó con la máquina y murió sin conseguir enfocarla. Mal día para leer las instrucciones.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, no creían en nada.",
        "Según UESP, la cultura dwemer era agnóstica, y prefería la razón a la fe. Despreciaban a los daedra, y si había dioses para ellos, eran la razón y la lógica.",
        "Para un dwemer, un dios no era alguien a quien rezar. Era un problema de ingeniería.",
        "En Elder Scrolls Online, un cuento dwemer tiene este chiste: al menos yo no juro por un dios que no solo es imaginario, sino que encima está muerto.",
        "[amused] Ojo: esos cuentos, los Cuentos antiguos de los dwemer, los escribió un autor que firmaba con seudónimo, Marobar Sul. Así que de fiable, poco. Pero de gracioso, mucho.",
        "Y ese desprecio importa. Porque un pueblo que no cree en los dioses, tarde o temprano, intenta fabricarse uno.",
    ]},
    {"id": "p7", "frases": [
        "En el siete, el dios de latón.",
        "El Numidium. También lo llaman el dios de latón o la piel divina. Lo construyó Kagrenac para que fuera un dios nuevo, alimentado por un corazón muy especial.",
        "Más de tres mil años después, en la segunda era, ochocientos noventa y seis, Tiber Septim lo puso en marcha, con la Mantella como corazón.",
        "Y con él terminó de conquistar Tamriel: derribó a los altos elfos en las Islas de Estivalia. Un solo gólem. Un continente entero.",
        "Y en la tercera era, cuatrocientos diecisiete, siete potencias activaron su propio Numidium a la vez, y el tiempo se rompió: la Distorsión del Oeste, la de Sentinel.",
        "En Morrowind, Dagoth Ur construyó otro, el Akulakhan. Lo destruyes tú, en la tercera era, cuatrocientos veintisiete.",
        "[deadpan] Una raza desaparece, y lo que deja olvidado en un cajón le basta a un emperador para conquistar el mundo. Imagina lo que no se dejaron.",
    ]},
    {"id": "campana", "frases": [
        "Antes del final, un dato. De cada cien que ven este canal, solo once están suscritos.",
        "Somos seis mil cuatrocientos ochenta. Si te suscribes, llegamos a diez mil. Y no desaparecemos. Que aquí no somos dwemer.",
    ]},
    {"id": "p6", "frases": [
        "[deadpan] Gracias, MariCarmen. Y ahora, mi secreto. Número seis. La caja que nadie debía abrir.",
        "Septimus Signus tiene en su cueva una caja dwemer enorme. Dice que dentro está el corazón de un dios.",
        "Para abrirla te manda a la Torre de Mzark con su léxico, y luego a sacar sangre de cinco elfos: altmer, bosmer, dunmer, orco y falmer.",
        "Fíjate en la lista. Cinco clases de elfo. Falta uno, porque de ese no queda ni una gota en todo el mundo: el dwemer.",
        "La caja se abre. Y dentro no hay ningún corazón. Hay un libro: el Oghma Infinium. Septimus solo alcanza a decir: ¿es solo un libro?",
        "Hermaeus Mora lo levanta en el aire y lo deshace. De Septimus queda un montón de ceniza.",
        "[sarcastic] Y ya está. Así se narra un secreto. Con datos, con suspense, y sin presumir.",
        "[deadpan] Lo has leído de una nota.",
        "[deadpan] Y tú tienes cuatro votos y aún no has dicho nada. Adelante, Profeta.",
    ]},
    {"id": "p5", "frases": [
        "Llegamos al cinco. El corazón bajo la montaña.",
        "Bajo la Montaña Roja de Morrowind, los dwemer encontraron algo que no era de este mundo: el corazón de Lorkhan, el dios que creó Nirn y al que los demás dioses le arrancaron el corazón.",
        "Kagrenac, el arquitecto tonal, vio en él lo que todo dwemer quería: energía. La de un dios.",
        "Su plan, según el libro Metafísica divina, era crear con él un dios nuevo. Recuperar su tierra, y quizá hacer inmortales a los dwemer.",
        "Para los chimer, los antepasados de los elfos oscuros, aquello era una blasfemia. Para los dwemer, solo era un proyecto.",
        "[short pause] Y fíjate en algo. Metafísica divina está escrito en dwemeris. Ni UESP tiene una traducción legible. Lo único que explica cómo querían hacerlo, nadie lo puede leer.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, tres herramientas.",
        "Kagrenac forjó tres piezas para trabajar el corazón. Sunder, un martillo para sacarle una cantidad exacta de poder.",
        "Keening, una hoja corta, para desollar y enfocar ese poder. Y Wraithguard, un guantelete, porque sin él empuñar las otras dos suele matarte.",
        "Kagrenac era famoso por ser meticuloso y prudente. Pero un herrero suyo, Bthuand Mzahnch, escribió un tratado, El huevo del tiempo, quitándole importancia a los riesgos.",
        "Otros dwemer avisaron: los efectos secundarios podían ser enormes.",
        "[deadpan] Hubo una reunión, alguien dijo que no pasaba nada, y nadie volvió a verlos. Lo de siempre en cualquier empresa.",
    ]},
    {"id": "cr3", "frases": [
        "Y la última carta del día. @jhonfeddiszabalamoreno9056 nos escribió en el video de las cosas inútiles: se nota que Kyrim no es lo tuyo.",
        "[amused] Y es verdad. Kyrim no es lo nuestro. Nunca lo hemos jugado. Lo nuestro es Skyrim, con ese.",
        "Pero gracias por la confianza. Si algún día sale Kyrim, serás el primero en enseñárnoslo.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. El día en que pasó, y nadie se pone de acuerdo.",
        "La batalla de la Montaña Roja. Primera era, setecientos, más o menos. Una canción nórdica la pone en el seiscientos sesenta y ocho.",
        "De un lado, Nerevar, el líder de los chimer. Del otro, Dumac, el rey de los dwemer, que antes había sido su aliado.",
        "Versión de Vivec: Kagrenac usó las herramientas desesperado, en plena batalla, y los dwemer desaparecieron. Pero en otro libro, el mismo Vivec dice que Kagrenac ni siquiera estaba allí.",
        "Versión del Templo: fue Nerevar, con ayuda de Azura, quien destruyó a los dwemer. Ni herramientas, ni corazón. Y los ashlanders, los nómadas de la ceniza, acusan al Tribunal de envenenar a Nerevar.",
        "Y Dagoth Ur, en una carta, lo llama un golpe cruel, una traición amarga.",
        "[short pause] Hay una teoría para tantas versiones: que el tiempo se rompió ese día, igual que con el Numidium. Y que todas son verdad a la vez.",
    ]},
    {"id": "p2", "frases": [
        "En el dos, el último de su raza.",
        "En Morrowind, bajo la torre del mago Divayth Fyr, vive Yagrum Bagarn. El último dwemer vivo conocido.",
        "Hinchado por el corprus, la enfermedad de Dagoth Ur, se mueve sobre patas mecánicas. Lo pilló al volver a la Montaña Roja buscando respuestas.",
        "¿Por qué sigue aquí? Porque no estaba. Lo dice él: yo estaba en un reino exterior en ese momento, y cuando volví, mi pueblo ya no estaba.",
        "Su teoría: creo que Kagrenac pudo conseguir darle a nuestra raza la vida eterna, con consecuencias imprevistas. Aunque admite que también pudo destruirla entera.",
        "[short pause] Y otra pista en Morrowind. En Bamz-Amschend, bajo Mournhold, hay montones de ceniza. Como si todos se hubieran vuelto polvo al final de la batalla.",
        "Y recuerda la ceniza de Septimus. Se pierde a un erudito con una caja dwemer, y lo que queda es lo mismo: ceniza.",
    ]},
    {"id": "p1", "frases": [
        "Y llegamos al número uno. Skyrim te deja repetir la desaparición.",
        "En el Colegio de Hibernalia vive Arniel Gane, un mago que estudia en secreto qué pasó con los dwemer. Su plan: recrear el momento exacto.",
        "Con una gema de alma en lugar del corazón de Lorkhan, y Keening en lugar de Sunder. Sí. Keening. La herramienta de Kagrenac.",
        "Le llevas diez engranajes dwemer. Enthir te da una gema de alma deformada. La cargas en convectores dwemer repartidos por Skyrim, que se destruyen al usarlos.",
        "Y te toca recuperar Keening, porque el mensajero que la traía desde Morrowind aparece muerto.",
        "Arniel golpea la gema con la daga. Una vez, nada. Dos veces, nada. A la tercera, un destello. Y Arniel ya no está. Solo queda Keening en el suelo.",
        "Según UESP, el experimento funcionó. Arniel se fue como se fueron ellos. Y en todo el Colegio, nadie nota que falta.",
        "[short pause] Después puedes invocar su sombra. No cuesta magia, es invulnerable, lanza rayos, y es el único invocado del juego que te cura.",
        "Así que esta es la respuesta que Skyrim te da sin decirlo: los dwemer no murieron en una explosión. Se fueron a algún sitio. Y a Arniel, al menos, le dejaron volver a ayudarte.",
        "[short pause] La pena es que no habla. Si no, ya le habríamos preguntado dónde están.",
    ]},
    {"id": "cierre", "frases": [
        "Esos son los veinte secretos de la desaparición de los dwemer, de un mote de gigante, a un mago que se fue con ellos.",
        "Ahora te toca a ti. ¿Qué crees que les pasó? ¿Borrados, convertidos en dioses, o en algún sitio con Arniel? Déjalo en los comentarios.",
        "[sarcastic] Y vota otra vez. ¿Qué voz se queda? Johnny, Edoardo, Hope, José, Mario, MariCarmen o el Profeta. Un nombre, y listo.",
        "[amused] Hope. Con hache, y sin empate.",
        "[deadpan] MariCarmen. La menos ridícula.",
        "Mario. Ya sé que corrí. Pero vótame.",
        "[deadpan] Edoardo. Cero votos. Este es mi momento.",
        "José. Sin voz de locutor, como pediste.",
        "Yo no pido votos. Ya leí el pergamino, y sigo ganando.",
        "Y yo voto por el humano tras el telón. Que hoy ha narrado un secreto.",
        "[sarcastic] Leído de una nota. Si quieres más lore, en el canal tienes los quince secretos del teaser de Sentinel. Suscríbete si aún no lo has hecho, que de aquí no se va nadie. Nos vemos en Tamriel.",
    ]},
]

# --- VARIAS VOCES (el usuario, 3/4-nov-2026): quién narra cada escena; las que no salen aquí, Johnny (VOZ) ---
VOCES = {   # nombre en pantalla: voice_id (biblioteca compartida de ElevenLabs, salvo el Humano tras el Telón = clon del usuario)
    "Johnny": "HMCmDsbKeaSZp5LMOYKR", "Edoardo": "YqZLNYWZm98oKaaLZkUA", "Hope": "tnSpp4vdxKPjI9w0GnoV",
    "José": "y2ijeTfmnXjzheHO6zeN", "Mario": "tomkxGQGz4b1kE0EM722", "MariCarmen": "YDDaC9XKjODs7hY78qEW",
    "el Profeta": "HNSF1CTQmub252yhXROX", "el Humano tras el Telón": "GUEeiSJYQQdbv0NJ86Im",
}
_POR_ESCENA = {"p18": "Edoardo", "p17": "Edoardo", "cr1": "Edoardo", "p16": "José", "p15": "José", "p14": "Mario", "p13": "Mario",
               "ag1": "Mario", "p12": "Hope", "p11": "Hope", "p10": "Hope", "cr2": "Hope", "p9": "MariCarmen", "p8": "MariCarmen",
               "p7": "MariCarmen", "campana": "MariCarmen", "p6": "el Humano tras el Telón", "p5": "el Profeta", "p4": "el Profeta",
               "cr3": "el Profeta", "p3": "el Profeta", "p2": "el Profeta", "p1": "el Profeta", "cierre": "el Profeta"}
_POR_FRASE = {"voces_2": "Edoardo", "voces_3": "José", "voces_4": "Mario", "voces_5": "Hope", "voces_6": "MariCarmen",
              "voces_7": "el Profeta", "voces_8": "el Humano tras el Telón",
              "ag1_3": "el Humano tras el Telón", "ag1_5": "el Humano tras el Telón",
              "cr2_2": "MariCarmen", "cr2_4": "MariCarmen",
              "p6_7": "Johnny", "p6_8": "MariCarmen",
              "cierre_2": "Johnny", "cierre_3": "Hope", "cierre_4": "MariCarmen", "cierre_5": "Mario", "cierre_6": "Edoardo",
              "cierre_7": "José", "cierre_9": "el Humano tras el Telón", "cierre_10": "Johnny"}
NARRA = {}   # "escena_i": nombre de la voz (efectos.py pone la ficha de quién narra en cada cambio)
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k) or _POR_ESCENA.get(_e["id"], "Johnny")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items() if v != "Johnny"}
