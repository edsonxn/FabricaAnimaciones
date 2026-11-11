# -*- coding: utf-8 -*-
"""GUION — «Las 10 builds más ROTAS de Skyrim» (Crónicas de Tamriel, 10-nov-2026, sale el jue 13-nov 12:08 CDMX).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Datos verificados en UESP:
_investigacion.md (cada build con su URL). Ref. de formato: JustMeegz builds ×20-23; el eje «lo que el jugador USA» gana en el canal.
El usuario (10-nov-2026): tema elegido entre 4; voces = Johnny narra + MariCarmen y el Profeta de VISITA (1-2 datos cada uno, sin
competencia) tras la queja ♥9 de @npc_1261. Guiño a Roirek ELEGIDO por el usuario (sarcástico, burla hacia nosotros que rebota en él):
en p5, tras el libro «Testigo sagrado». Críticas con contraburla (regla 11-nov: mínimo 2-3): @npc_1261 (6-nov, ♥9) en cr1, @edgarvillalobos1492 Ugz-N2L_9u_o78TCuK94AaABAg (4-nov, ♥7) en cr2, @YetRise UgzYlJHfo9-g-E7Y6qR4AaABAg (6-nov) en cr3. Agradecimientos (≤ 10 días):
@launionsovietica3315, @JinbeiDLuffy, @REaPEK.papulol, @DJRaygadaVargas, @estebato2448 (Miguel_Salvatierra ya salió en tes_dwemer).
Campaña de suscripción antes del top 2 (86,7 % de las vistas de 28 d son de no suscritos → «solo trece de cada cien»).
Turbo, corchetes SIN [whispers] ni [excited]. Exploits marcados en voz (el parche no oficial los corrige).
"""

TITULO = "Las 10 builds más ROTAS de Skyrim"
ARCHIVO = "tes_builds_rotas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HMCmDsbKeaSZp5LMOYKR", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), referencia=r"C:\chatterbox_voices\Sarcastica.mp3")
# ElevenLabs dice el inglés nativo: aquí lo que se oyó mal en videos anteriores (quejas del público: «Oblivión» agudo, «jarl»)
FONETICA = {"Oblivion": "Oblívion", "jarl": "yarl", "Jarl": "Yarl", "Serana": "Serana", "Harkon": "Járkon",
            "Miraak": "Mirák", "Dawnguard": "Don-gard", "Dragonborn": "Drágon-born", "Ulfric": "Úlfric",
            "Fus Ro Dah": "Fus Ro Da", "Riften": "Ríften", "Falkreath": "Fálkriz", "Volkihar": "Vólkijar"}

CER_MAX_POR_FRASE = {"p10b_0": 0.005, "p9_2": 0.036, "cr1_0": 0.055, "p8_2": 0.024, "p7_0": 0.03, "p7_1": 0.059, "p6_3": 0.019, "p6b_1": 0.022, "ag1_1": 0.185, "ag1_2": 0.094, "p5_2": 0.048, "p5_5": 0.024, "p5_6": 0.021, "p5_7": 0.037, "p5_9": 0.021, "p4_2": 0.018, "p4_3": 0.005, "p4_4": 0.005, "p3_3": 0.042, "p3_4": 0.005, "p3_6": 0.02, "p2_3": 0.005, "p1_6": 0.005, "cr2_0": 0.085, "cr3_0": 0.14}   # oídas en eval.json: Whisper oye «Cajita», «Morzal», «Dungard», «Roirec»
TAIL_MAX_POR_FRASE = {"p10b_0": 1.05, "p6_3": 1.03, "p5_5": 1.1, "p4_3": 1.1, "p4_4": 1.13, "p3_4": 1.17, "p3_6": 1.04, "p2_3": 1.14, "p1_6": 1.1}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-014": .8, "scene-057": .8},   # sonido nombrado: grito Ralentizar tiempo (silencio p10b) y Úlfric reanimado gritando (silencio p6b)
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (Jeremy Soule; armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Un arquero que mata dragones sin que lo vean. Un mago con la barra de magia de adorno. Un asesino que tumba a un dragón legendario de una sola puñalada.",
        "Un nigromante con un ejército sin límite, y un alquimista que, con sal y unos peces, rompe el juego entero.",
        "[amused] Hoy toca lo que más se pelea en los comentarios después del lore. Las builds. Las diez más rotas de Skyrim.",
        "Con su raza, su piedra, sus ventajas, el equipo y dónde se consigue. Todo comprobado en UESP, con las fuentes en la descripción.",
        "[sarcastic] Y aviso: dos de ellas son trampas del propio juego. Te diré cuáles. Y quédate hasta el número uno, porque ya no es una build. Es borrar Skyrim.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. El Arquero Fantasma.",
        "[deadpan] Sí. La build que acaba haciendo todo el mundo. El noventa por ciento de los jugadores termina siendo arquero sigiloso. El otro diez por ciento lo niega en los comentarios.",
        "Raza: elfo del bosque, con más diez en Arquería. Piedra: la del Ladrón, en las piedras guardianas al suroeste de Cauce Boscoso. Y ojo, que esta es buena: la Arquería la sube la piedra del Ladrón, no la del Guerrero, aunque en el menú esté en combate.",
        "Las ventajas: Máxima tensión, que acaba doblando el daño del arco. Puntería mortífera, que triplica el ataque sigiloso con arco. Y Mano firme: al apuntar, el tiempo va a la mitad de velocidad.",
        "El arco: el de hueso de dragón, de Dawnguard. Veinte de daño, el más alto del juego. Solo se forja con Herrería cien, o se le quita a un Guardián.",
        "Y si te descubren, el grito Ralentizar tiempo. Con las tres palabras, el mundo va al diez por ciento durante dieciséis segundos. Tiempo de sobra para vaciar la aljaba.",
    ]},
    {"id": "p10b", "pre": 1.5, "frases": [
        "Hay un libro de Arquería, Cinta dorada al mérito. Un noble presume de su cinta de arquero ante un soldado veterano. El soldado tira una flecha que parece perdida en el valle. Cuando el noble llega a casa, la flecha está clavada en su cinta.",
        "[deadpan] El buen arquero era el otro. Como en todas las partidas de Skyrim.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. El Carterista Envenenador.",
        "La idea es simple. No matas a nadie. Le dejas un regalito en el bolsillo.",
        "Raza: khajiita, con más diez en Discreción. Piedra: la Sombría, al sur de Ríften: una vez al día, sesenta segundos invisible.",
        "Con la ventaja Envenenado, en Robo cuarenta, puedes meter venenos en el bolsillo de alguien. Y aquí está lo roto: según UESP, eso no cuenta como crimen. Ni delante de toda la plaza.",
        "Le metes tres venenos a un guardia, se los va tomando uno a uno, cae muerto en pleno mercado, y nadie te pone recompensa.",
        "[sarcastic] Técnicamente no es asesinato. Es entrega a domicilio sin consentimiento.",
        "Y en Robo cien, Toque perfecto: robas cualquier cosa que lleven puesta. Al jefe de los bandidos le quitas la armadura y lo dejas peleando en ropa interior.",
        "Bonus: en la misión de la Hermandad Oscura, puedes robarle a Astrid su armadura y su daga antes de hacer nada. Al final te dan otra daga igual. Una para cada mano.",
    ]},
    {"id": "cr1", "frases": [
        "Un momento, que hay correo. @npc_1261, con nueve likes: «Desagradable el asunto de las voces, mata la inmersión, suena a porquería».",
        "[deadpan] Nueve likes. Mensaje recibido. Hoy narro yo, y de siete voces solo vienen dos, y solo de visita.",
        "[sarcastic] Las otras cinco están bien. Están en un menú de pausa mirando la pared. Que es justo lo que pediste: inmersión total.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. El Titiritero.",
        "[amused] Esta build no pelea. Organiza peleas.",
        "Raza: alto elfo, con más diez en Ilusión y cincuenta de magia extra. Piedra: la del Aprendiz, en la isla del pantano al oeste de Morthal.",
        "Y aquí, un mito. La pantalla de carga dice que esa piedra duplica tu magia. Falso. Según UESP, solo duplica lo rápido que se recupera. Y a cambio te deja con el doble de debilidad a la magia.",
        "Las ventajas: Mago fraternal y Furia, que suben el nivel de enemigos que puedes controlar. Conjuros silenciosos, que hacen mudos todos tus hechizos. Y Señor de la mente, para que funcione hasta con no muertos y autómatas enanos.",
        "El hechizo clave es de nivel maestro, y lo vende Drevis Neloren en el Colegio de Hibernalia. Todo el que esté cerca, hasta nivel veinticinco, ataca a cualquiera durante sesenta segundos. Con las ventajas, hasta nivel cuarenta y siete.",
        "Entras en una mazmorra, lo lanzas, y te sientas. Un minuto de todos contra todos. Tú solo sales a recoger el botín.",
        "[deadpan] Mi build no hace daño. Hace terapia de grupo. Muy mala.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. El Señor de los Vampiros, de Dawnguard.",
        "Se consigue aceptando el regalo de Lord Járkon en el castillo Vólkijar. Eso sí: te alinea con su clan para siempre.",
        "A nivel cuarenta y seis o más, la forma de Señor tiene doscientos cincuenta de salud extra, doscientos de magia, y una Absorción vampírica que roba salud, magia y aguante a la vez.",
        "Puedes agarrar a un arquero del muro a distancia, levantarlo, y soltarlo por un precipicio. Y si te bajan la vida, te conviertes en niebla, invulnerable, y vuelves entero.",
        "Y hoy tenemos visita. MariCarmen, este dato es tuyo.",
        "[deadpan] Gracias, Johnny. Según UESP, si Serana te acompaña, el daño de tu Absorción vampírica baja a cero. Cero. Por una condición del propio hechizo.",
        "[sarcastic] Serana. La única novia que, literalmente, te quita el daño. Me voy, que tengo un ataúd esperando.",
        "Y otro dato de UESP: en el desarrollo, la forma de Señor iba a tener tiempo límite, como el hombre lobo. Járkon llegó a grabar los diálogos. Al final, nada. Sin límite.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. El Nigromante Infinito.",
        "¿Para qué subir de nivel, si puedes reclutar a los que ya lo hicieron?",
        "Raza: bretón, con más diez en Conjuración. Piedra: la Ritual, al este de Carrera Blanca, en lo alto de una atalaya con un nigromante de guardia. Una vez al día, levanta a todos los muertos cercanos hasta nivel setenta y cinco. Gigantes y mamuts incluidos.",
        "Y aquí viene lo roto. La Corona aetérica, de Dawnguard, guarda el poder de una piedra anterior. Llevas dos piedras a la vez. Y si te quitas la corona y te la vuelves a poner, puedes usar la Ritual otra vez. UESP lo resume así: ejércitos de no muertos potencialmente ilimitados.",
        "Con Almas gemelas llevas dos invocaciones, y con Conjurar a un señor dremora tienes un daedra de quinientos cuarenta y cinco de salud con un mandoble del infierno.",
        "Y el hechizo maestro Esclavo muerto reanima para siempre a cualquier humanoide de nivel cuarenta o menos. Y el segundo invitado tiene algo que decir.",
        "Los muertos únicos conservan sus poderes. Úlfric Capa de la Tormenta, reanimado, sigue usando sus gritos. Contra sus propios soldados. Estaba escrito.",
    ]},
    {"id": "p6b", "pre": 1.8, "frases": [
        "[deadpan] Gracias, Profeta. Y ojo, que hay letra pequeña: en Legendario, tus invocaciones reciben un cuarto del daño. Igual que los enemigos.",
        "Remate. El libro sobre el rey de los nigromantes, Mannimarco, rey gusano, no te sube Conjuración. Te sube Alquimia. [short pause] Bethesda, siempre coherente.",
    ]},
    {"id": "ag1", "frases": [
        "Antes del top cinco. Los comentarios de esta semana. «Este canal merece más reconocimientos, veinte de diez». Lo dice La Unión Soviética, así, con mayúsculas.",
        "«Tus videos se merecen más views, son muy buenos», de @JinbeiDLuffy. «Videazo, me encantó», de @REaPEK.papulol. Y @estebato2448, que recién se entera de cómo funciona un grito. Para eso estamos.",
        "Y @DJRaygadaVargas, que dice que, si a nosotros nos funciona, sigamos haciendo videos. Eso hacemos.",
        "Los leemos todos. Los buenos, y los que duelen. Y se toman en cuenta: uno de ellos ya se convirtió en cambio, hoy mismo.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El Asesino de la Hermandad.",
        "Un dragón, una puñalada, cero testigos.",
        "Raza: khajiita o elfo del bosque. Piedra: otra vez la Sombría, para acercarte invisible.",
        "Las ventajas: Puñalada por la espalda, que multiplica por seis los ataques sigilosos con armas de una mano. Y Hoja del asesino: con dagas, por quince.",
        "Pero falta el regalo. Al unirte a la Hermandad Oscura, Astrid te da unos guantes que doblan el daño de esas puñaladas. Por treinta. [deadpan] Recursos Humanos de la Hermandad: impecables.",
        "Las cuentas de UESP: un dragón legendario tiene cuatro mil ciento sesenta y tres de salud. Con por treinta, en dificultad Adepto, basta una daga que marque ciento treinta y nueve de daño. Una puñalada.",
        "Y si fallas, la Navaja de Mehrunes, de la misión daédrica Fragmentos del pasado, con probabilidad de matar al instante. Solo Mirák y Karstaag son inmunes.",
        "Y otro mito. Todos dicen que la Navaja mata uno de cada cien golpes. Falso. Por un descuido en el código, es casi el doble: un uno coma noventa y ocho por ciento.",
        "[short pause] Y el libro de Discreción, Testigo sagrado, de la habitación de Babette. Un poeta conoce a la Madre Noche y sirve a la Hermandad. La nota del editor dice que lo asesinaron poco después de publicarlo, y que le dejaron dos piedras en los ojos. Una negra y una blanca.",
        "[sarcastic] Libro, página y todo. Lo sé, Roirek… qué horrible: Crónicas de ChatGPT acertando.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. El Mago Sin Coste.",
        "[deadpan] La barra de magia, de adorno.",
        "Raza: elfo oscuro, con más diez en Destrucción, o alto elfo. Piedra: la del Señor, al este de Morthal, con armadura y resistencia a la magia. Porque con coste cero, lo único que importa es sobrevivir.",
        "La regla está en UESP, literal: cuatro prendas que reducen un veinticinco por ciento el coste de Destrucción, bajan el coste a cero. Cero. Y es totalmente legal.",
        "¿Cómo se llega al veinticinco por ciento? Encantamiento cien, los cinco rangos de Encantador, Encantador perspicaz y una gema de alma grande. En el gorro, el pecho, el collar y el anillo.",
        "Con Doble destrucción e Impacto, cada hechizo a dos manos desequilibra al rival. Un dragón aterriza, y se queda tambaleándose en bucle mientras tu barra azul no se mueve.",
        "Y el extra: esa reducción también vale para las armas encantadas de Destrucción. Con las cuatro prendas, una espada de escarcha tiene usos infinitos.",
        "Y un mito más, para los altos elfos. Su poder racial dice que recuperas la magia veinticinco veces más rápido. UESP lo calculó: unas nueve veces. Sigue siendo mucho. Pero no veinticinco.",
        "[sarcastic] Los magos estudian años en el Colegio de Hibernalia. Tú solo necesitaste un collar, un anillo, un gorro y una túnica.",
    ]},
    {"id": "cr2", "frases": [
        "Más correo. @edgarvillalobos1492, con siete likes: «Buenos datos, lástima tanta AI».",
        "[deadpan] Buenos datos. Lo apunto. Es la reseña más bonita que nos han hecho, con la letra pequeña al final, como un contrato daédrico.",
        "[sarcastic] Y tranquilo, que el mago sin coste también usa ayuda: cuatro prendas encantadas. Y nadie le dice que eso no es magia de verdad.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. El Pararrayos.",
        "[amused] Tu bola de fuego me recarga la barra. Gracias.",
        "La absorción de hechizos es una probabilidad de anular el efecto entero y quedarte con la magia. Y según UESP, funciona contra casi todo lo que no sea un golpe físico. Incluido el aliento de dragón.",
        "Hay tres caminos al cien por cien. El rápido: un bretón con su poder racial, más la piedra del Atronach. Cien por cien. Durante un minuto.",
        "El permanente, de Dragonborn: piedra del Atronach, cincuenta. La ventaja Atronach, treinta. La túnica de Mirák, quince. Y sus guantes o sus botas, cinco más. Cien. Con cualquier raza.",
        "[deadpan] Mirák lleva siglos preparándose para matarte. Y te deja la ropa que te hace inmune a él. Gracias, compañero.",
        "El tercero es un error: un vampiro cuenta como no muerto, así que la ventaja Necromago de Restauración te potencia a ti. Con el orden justo, cien por cien permanente.",
        "La letra pequeña: con tanta absorción puedes absorber tus propias invocaciones, y fallan. Pero un sacerdote dragón y un dragón atacándote a la vez no te quitan ni un punto de vida.",
    ]},
    {"id": "campana", "frases": [
        "Antes del top dos, un dato. De cada cien que ven este canal, solo trece están suscritos.",
        "Somos seis mil quinientos ochenta. Si te suscribes, pasamos de siete mil, camino de diez mil. Un botón. Menos esfuerzo que el bucle de alquimia que viene ahora.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. El Artesano Legendario.",
        "No hay arma más rota que la que te fabricas tú. Y esta no usa ningún error.",
        "Raza: orco, con más cinco en Encantamiento y en Herrería. Piedra: la del Amante, al noreste de Markarth: todas las habilidades suben un quince por ciento más rápido.",
        "El bucle legal: con ropa de alquimia haces una poción de encantamiento. Con esa poción, encantas mejor ropa de alquimia. Y otra vez. Hasta que deja de subir. Y con todo eso, el equipo de herrería.",
        "UESP lo midió. En el juego base, sin trampas, el equipo llega a calidad veintinueve: más cincuenta y dos de daño en un arma. Con los Libros Negros de Dragonborn, calidad cuarenta y uno: más setenta y tres.",
        "[deadpan] La etiqueta sigue diciendo «Legendario». El número sigue subiendo. La etiqueta, como siempre, miente.",
        "Y la armadura se queda clavada en el tope: ochenta por ciento menos de daño físico, con cualquier set.",
        "Ahora junta esto con el asesino del cinco. Una daga de hueso de dragón templada así, por treinta en sigilo. [short pause] No queda nada vivo en el juego base.",
    ]},
    {"id": "cr3", "frases": [
        "Y el último correo. @YetRise: «Ya no hay talento para voces reales».",
        "[deadpan] Talento real. Como el del que hace el bucle de alquimia: poción, ropa, poción, ropa… y luego dice que mató al dragón él solito.",
        "[sarcastic] Pero en algo tienes razón: lo que viene ahora no necesita talento. Necesita sal y pescado.",
    ]},
    {"id": "p1", "frases": [
        "Y el número uno. El Dios del Boticario.",
        "Aviso: esto es un error. El parche no oficial lo corrige desde hace años. Pero en consolas sin mods sigue ahí.",
        "Las pociones de Reforzar restauración potencian cualquier encantamiento de habilidad que te pongas mientras duran. Y el aumento se queda. Incluida tu ropa de alquimia, que hace pociones de restauración más fuertes.",
        "El procedimiento, literal de UESP: te pones la ropa de alquimia. Haces la poción. Te quitas la ropa. Te bebes la poción. Y repites.",
        "Cada vuelta, la ropa vale más. Y la poción, más. Y la ropa, más. Hasta que la ventana de efectos marca cifras de miles de por ciento.",
        "Los ingredientes: un montón de sal y unos peces. Los barriles del muelle de Ríften están llenos.",
        "Con esas cifras, Congelación, un hechizo de principiante, mata dragones. Y en Xbox One, pasar de diez mil por ciento cuelga el juego. El juego se rinde antes que tú.",
        "Los Barbas Grises entrenan treinta años para dominar la Voz. Tú rompiste el universo en veinte minutos, con sal y pescado.",
        "[deadpan] Gracias otra vez, Profeta. Y el libro que vigila tu mesa en el Templo Nocturnal: Mannimarco, rey gusano. El rey de los nigromantes, de ayudante de cocina.",
    ]},
    {"id": "cierre", "frases": [
        "Este es el top. Del arquero que hace todo el mundo, al alquimista que borra el juego.",
        "Ahora te toca a ti. ¿Cuál falta? ¿La Hoja de ébano, que el juego cuenta como espada de una mano? ¿El hombre lobo? Déjalo en los comentarios: los leemos todos.",
        "Y suscríbete si aún no lo has hecho. Camino de diez mil. Nos vemos en Tamriel.",
    ]},
]

# --- VOCES (el usuario, 10-nov-2026): narra Johnny; MariCarmen y el Profeta de visita, 1-2 datos cada uno, sin competencia ---
VOCES = {"Johnny": "HMCmDsbKeaSZp5LMOYKR", "MariCarmen": "YDDaC9XKjODs7hY78qEW", "el Profeta": "HNSF1CTQmub252yhXROX"}
_POR_FRASE = {"p7_5": "MariCarmen", "p7_6": "MariCarmen", "p6_6": "el Profeta", "p1_7": "el Profeta"}
NARRA = {}   # "escena_i": nombre de la voz (efectos.py pone la placa de quién narra en cada cambio)
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k, "Johnny")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items() if v != "Johnny"}
