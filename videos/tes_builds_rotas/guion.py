# -*- coding: utf-8 -*-
"""GUION — «Las 10 builds más ROTAS de Skyrim» (Crónicas de Tamriel, 10-nov-2026, sale el jue 13-nov 12:08 CDMX).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Datos de _investigacion.md (cada
build con su URL, que va en la descripción). Ref. de formato: JustMeegz builds ×20-23; el eje «lo que el jugador USA» gana en el canal.
v3 (el usuario, 12-nov-2026): (1) la voz NO cita fuentes («según UESP» 12 veces sonaba a que no sabemos): experiencia propia o el
dato a secas; (2) ganó la votación EL PROFETA → narra 8 de cada 10 datos y se burla DESDE ARRIBA por ser el ganador; Johnny,
MariCarmen y Hope (empatados en el 2.º lugar) se PELEAN entre ellos por los otros 2. v2 (Johnny narrando) en guion_v2_johnny.py.
Guiño a Roirek ELEGIDO por el usuario en p5. Críticas con contraburla (regla 11-nov: mínimo 2-3): @npc_1261 (cr1),
@edgarvillalobos1492 (cr2), @YetRise (cr3). Agradecimientos (≤ 10 días): @launionsovietica3315, @JinbeiDLuffy, @REaPEK.papulol,
@DJRaygadaVargas, @estebato2448. Campaña de suscripción antes del top 2. Turbo, corchetes SIN [whispers] ni [excited]; el Profeta
plano (sin risas ni alegría, como en Runa Caída).
"""

TITULO = "Las 10 builds más ROTAS de Skyrim"
ARCHIVO = "tes_builds_rotas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
# ElevenLabs dice el inglés nativo: aquí lo que se oyó mal en videos anteriores (quejas del público: «Oblivión» agudo, «jarl»)
FONETICA = {"Oblivion": "Oblívion", "jarl": "yarl", "Jarl": "Yarl", "Serana": "Serana", "Harkon": "Járkon",
            "Miraak": "Mirák", "Dawnguard": "Don-gard", "Dragonborn": "Drágon-born", "Ulfric": "Úlfric",
            "Fus Ro Dah": "Fus Ro Da", "Riften": "Ríften", "Falkreath": "Fálkriz", "Volkihar": "Vólkijar"}

CER_MAX_POR_FRASE = {'p9_2': 0.046, 'cr1_0': 0.055, 'p7_0': 0.03, 'p7_1': 0.059, 'p7_6': 0.012, 'p6_3': 0.016, 'p6b_1': 0.035, 'ag1_1': 0.119, 'ag1_2': 0.106, 'p5_2': 0.062, 'p5_6': 0.021, 'p5_7': 0.035, 'p5_8': 0.019, 'p5_9': 0.021, 'cr2_0': 0.084, 'p3_3': 0.042, 'p3_6': 0.018, 'cr3_0': 0.142}   # v3 12-nov: oídas en eval.json, frases completas; Whisper oye «Cajita», «Dungard», «Becesda», «arroba», cifras. se rellena tras `seleccionar` con las falsas alarmas oídas (v2: «Cajita», «Morzal», «Dungard», «arroba»)
TAIL_MAX_POR_FRASE = {'p10_2': 1.09, 'p7_6': 1.17, 'p6_3': 1.05, 'p5_5': 1.07, 'p5_6': 0.93, 'p4_7': 1.06, 'p3_3': 1.11, 'p3_6': 0.96, 'p3_7': 1.18, 'p2_3': 1.09}   # colas: frases que hablan hasta el final (comprobado el final de cada una)

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-060": .45},   # 12-nov: scene-015 FUERA y 060 de .8 a .45 (el clip se oía fuerte y mal, el usuario: ningún clip al nivel de la voz)
      # se re-indexa con _remapear.py: grito Ralentizar tiempo (p10b) y Úlfric (p6b)
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29", "Xander Rey Gaming", "AtariGen 75", "NOB NO13", "Zephyr", "A Bard's Ballad",
                            "Cameron Marks"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de Skyrim (Jeremy Soule; armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Un arquero que mata dragones sin que lo vean. Un mago con la barra de magia de adorno. Un asesino que tumba a un dragón legendario de una sola puñalada.",
        "Un nigromante con un ejército sin límite, y un alquimista que, con sal y unos peces, rompe el juego entero.",
        "[deadpan] Hoy toca lo que más se pelea en los comentarios después del lore. Las builds. Las diez más rotas de Skyrim.",
        "Con su raza, su piedra, sus ventajas, el equipo y dónde se consigue. Cada una, probada.",
        "[sarcastic] Y aviso: dos de ellas son trampas del propio juego. Te diré cuáles. Y quédate hasta el número uno, porque ya no es una build. Es borrar Skyrim.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. El Arquero Fantasma.",
        "[deadpan] Sí. La build que acaba haciendo todo el mundo. El noventa por ciento de los jugadores termina siendo arquero sigiloso. El otro diez por ciento lo niega en los comentarios.",
        "Raza: elfo del bosque, con más diez en Arquería. Piedra: la del Ladrón, en las piedras guardianas al suroeste de Cauce Boscoso. Y ojo, que esta es buena: la Arquería la sube la piedra del Ladrón, no la del Guerrero, aunque en el menú esté en combate.",
        "Las ventajas: Máxima tensión, que acaba doblando el daño del arco. Puntería mortífera, que triplica el ataque sigiloso con arco. Y Mano firme: al apuntar, el tiempo va a la mitad de velocidad.",
        "[sarcastic] Este dato es mío, que para algo quedé segundo. El arco de hueso de dragón, de Dawnguard: veinte de daño, el más alto del juego. Solo se forja con Herrería cien, o se le quita a un Guardián.",
        "Y si te descubren, el grito Ralentizar tiempo. Con las tres palabras, el mundo va al diez por ciento durante dieciséis segundos. Tiempo de sobra para vaciar la aljaba.",
    ]},
    {"id": "p10b", "pre": 1.5, "frases": [
        "Hay un libro de Arquería, Cinta dorada al mérito. Un noble presume de su cinta de arquero ante un soldado veterano. El soldado tira una flecha que parece perdida en el valle. Cuando el noble llega a casa, la flecha está clavada en su cinta.",
        "[deadpan] El buen arquero era el otro. Como en todas las partidas de Skyrim.",
        "[annoyed] Perdón, ¿segundo? Quedamos empatados, Johnny. Tú, Hope y yo. Con dos votos cada uno.",
        "[deadpan] Ustedes votaron, y ganó el Profeta. Así que narro yo. Los tres empatados se pelean por las migajas. Es lo justo.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. El Carterista Envenenador.",
        "La idea es muy sencilla: no matas a nadie. Solo le dejas un regalito en el bolsillo.",
        "Raza: khajiita, con más diez en Discreción. Piedra: la Sombría, al sur de Ríften: una vez al día, sesenta segundos invisible.",
        "[sarcastic] Me toca, que ellos ya hablaron. Con la ventaja Envenenado, en Robo cuarenta, metes venenos en el bolsillo de alguien. Y lo roto: el juego no lo cuenta como crimen, aunque te esté mirando toda la plaza.",
        "Le metes tres venenos a un guardia, se los va tomando uno a uno, cae muerto en pleno mercado, y nadie te pone recompensa.",
        "[sarcastic] Técnicamente no es asesinato. Es entrega a domicilio sin consentimiento.",
        "Y en Robo cien, Toque perfecto: robas cualquier cosa que lleven puesta. Al jefe de los bandidos le quitas la armadura y lo dejas peleando en ropa interior.",
        "Bonus, y este me lo quedo yo: en la misión de la Hermandad Oscura, puedes robarle a Astrid su armadura y su daga antes de hacer nada. Al final te dan otra daga igual. Una para cada mano.",
    ]},
    {"id": "cr1", "frases": [
        "Un momento, que hay correo. @npc_1261, con nueve likes: «Desagradable el asunto de las voces, mata la inmersión, suena a porquería».",
        "[deadpan] Nueve likes. Mensaje recibido. Por eso ahora narra uno solo: el que ustedes eligieron.",
        "[sarcastic] Los otros tres siguen aquí, en la banca, peleándose por un dato. Si eso te saca de la inmersión, imagina lo que les saca a ellos.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. El Titiritero.",
        "[deadpan] Esta no pelea. Organiza las peleas de los demás.",
        "Raza: alto elfo, con más diez en Ilusión y cincuenta de magia extra. Piedra: la del Aprendiz, en la isla del pantano al oeste de Morthal.",
        "Este mito lo desmiento yo. La pantalla de carga dice que esa piedra duplica tu magia. Falso: solo duplica lo rápido que se recupera. Y a cambio, te deja con el doble de debilidad a la magia.",
        "Las ventajas: Mago fraternal y Furia, que suben el nivel de enemigos que puedes controlar. Conjuros silenciosos, que hacen mudos todos tus hechizos. Y Señor de la mente, para que funcione hasta con no muertos y autómatas enanos.",
        "[annoyed] MariCarmen ya tuvo su mito; el hechizo es mío. Es de nivel maestro, y lo vende Drevis Neloren en el Colegio de Hibernalia. Todo el que esté cerca, hasta nivel veinticinco, ataca a cualquiera durante sesenta segundos. Con las ventajas, hasta nivel cuarenta y siete.",
        "Entras en una mazmorra, lo lanzas, y te sientas. Un minuto de todos contra todos. Tú solo sales a recoger el botín.",
        "[deadpan] Esta build no hace daño. Hace terapia de grupo. Pregúntenle a los tres de la banca.",
    ]},
    {"id": "p7", "frases": [
        "Número siete. El Señor de los Vampiros, de Dawnguard.",
        "Se consigue aceptando el regalo de Lord Járkon en el castillo Vólkijar. Eso sí: te alinea con su clan para siempre.",
        "A nivel cuarenta y seis o más, la forma de Señor tiene doscientos cincuenta de salud extra, doscientos de magia, y una Absorción vampírica que roba salud, magia y aguante a la vez.",
        "Puedes agarrar a un arquero del muro a distancia, levantarlo, y soltarlo por un precipicio. Y si te bajan la vida, te conviertes en niebla, invulnerable, y vuelves entero.",
        "Este lo cuento yo. Si Serana te acompaña, el daño de tu Absorción vampírica baja a cero. Cero. Por una condición del propio hechizo.",
        "[sarcastic] Y el chiste lo pongo yo, que a él no le sale. Serana: la única novia que, literalmente, te quita el daño.",
        "[deadpan] Peleen más bajito, por favor, que hay vampiros durmiendo en el castillo. En el desarrollo, la forma de Señor iba a tener tiempo límite, como el hombre lobo. Járkon llegó a grabar los diálogos. Al final, nada. Sin límite.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. El Nigromante Infinito.",
        "¿Para qué subir de nivel, si puedes reclutar a los que ya lo hicieron?",
        "Raza: bretón, con más diez en Conjuración. Piedra: la Ritual, al este de Carrera Blanca, en lo alto de una atalaya con un nigromante de guardia. Una vez al día, levanta a todos los muertos cercanos hasta nivel setenta y cinco. Gigantes y mamuts incluidos.",
        "Y aquí viene lo roto. La Corona aetérica, de Dawnguard, guarda el poder de una piedra anterior. Llevas dos piedras a la vez. Y si te quitas la corona y te la vuelves a poner, puedes usar la Ritual otra vez. Ejércitos de no muertos, sin límite.",
        "Con Almas gemelas llevas dos invocaciones, y con Conjurar a un señor dremora tienes un daedra de quinientos cuarenta y cinco de salud con un mandoble del infierno.",
        "Y el hechizo maestro Esclavo muerto reanima para siempre a cualquier humanoide de nivel cuarenta o menos.",
        "[sarcastic] ¡Este es mío, que lo vi primero! Los muertos únicos conservan sus poderes. Úlfric Capa de la Tormenta, reanimado, sigue usando sus gritos. Contra sus propios soldados.",
    ]},
    {"id": "p6b", "pre": 1.8, "frases": [
        "[deadpan] Muy bien, MariCarmen, ya tienes tu dato; que no se te suba a la cabeza. Y ojo, que hay letra pequeña: en Legendario, tus invocaciones reciben un cuarto del daño. Igual que los enemigos.",
        "Remate, antes de que me lo quiten. El libro sobre el rey de los nigromantes, Mannimarco, rey gusano, no te sube Conjuración. Te sube Alquimia. [short pause] Bethesda, siempre coherente.",
    ]},
    {"id": "ag1", "frases": [
        "Antes del top cinco. Los comentarios de esta semana. «Este canal merece más reconocimientos, veinte de diez». Lo dice La Unión Soviética, así, con mayúsculas.",
        "«Tus videos se merecen más views, son muy buenos», de @JinbeiDLuffy. «Videazo, me encantó», de @REaPEK.papulol. Y @estebato2448, que recién se entera de cómo funciona un grito. Para eso estamos.",
        "Y @DJRaygadaVargas, que dice que, si a nosotros nos funciona, sigamos haciendo videos. Eso hacemos.",
        "Los leemos todos. Los buenos, y los que duelen. Y se toman en cuenta: ustedes votaron por un narrador, y aquí estoy.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El Asesino de la Hermandad.",
        "Un dragón, una puñalada, cero testigos.",
        "Raza: khajiita o elfo del bosque. Piedra: otra vez la Sombría, para acercarte invisible.",
        "Las ventajas: Puñalada por la espalda, que multiplica por seis los ataques sigilosos con armas de una mano. Y Hoja del asesino: con dagas, por quince.",
        "Pero todavía falta lo mejor: el regalo. Al unirte a la Hermandad Oscura, Astrid te da unos guantes que doblan el daño de esas puñaladas. Por treinta. [deadpan] Recursos Humanos de la Hermandad: impecables.",
        "[sarcastic] Las cuentas las hago yo, que alguien aquí tiene que saber sumar. Un dragón legendario tiene cuatro mil ciento sesenta y tres de salud. Con por treinta, en dificultad Adepto, basta una daga que marque ciento treinta y nueve de daño. Una puñalada.",
        "Y si fallas, la Navaja de Mehrunes, de la misión daédrica Fragmentos del pasado, con probabilidad de matar al instante. Solo Mirák y Karstaag son inmunes.",
        "Y el mito me lo quedo yo. Todos dicen que la Navaja mata uno de cada cien golpes. Falso. Por un descuido en el código, es casi el doble: un uno coma noventa y ocho por ciento.",
        "[short pause] Y el libro de Discreción, Testigo sagrado, de la habitación de Babette. Un poeta conoce a la Madre Noche y sirve a la Hermandad. La nota del editor dice que lo asesinaron poco después de publicarlo, y que le dejaron dos piedras en los ojos. Una negra y una blanca.",
        "[sarcastic] Libro, página y todo. Lo sé, Roirek… qué horrible: Crónicas de ChatGPT acertando.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. El Mago Sin Coste.",
        "[deadpan] La barra de magia, de adorno.",
        "Raza: elfo oscuro, con más diez en Destrucción, o alto elfo. Piedra: la del Señor, al este de Morthal, con armadura y resistencia a la magia. Porque con coste cero, lo único que importa es sobrevivir.",
        "La regla es esta: cuatro prendas que reducen un veinticinco por ciento el coste de Destrucción bajan el coste a cero. Cero. Y es totalmente legal.",
        "¿Cómo se llega al veinticinco por ciento? Encantamiento cien, los cinco rangos de Encantador, Encantador perspicaz y una gema de alma grande. En el gorro, el pecho, el collar y el anillo.",
        "Con Doble destrucción e Impacto, cada hechizo a dos manos desequilibra al rival. Un dragón aterriza, y se queda tambaleándose en bucle mientras tu barra azul no se mueve.",
        "Y el extra: esa reducción también vale para las armas encantadas de Destrucción. Con las cuatro prendas, una espada de escarcha tiene usos infinitos.",
        "[annoyed] Johnny ya dijo un mito, ahora me toca a mí. Los altos elfos: su poder racial dice que recuperas la magia veinticinco veces más rápido. Haz la cuenta: unas nueve veces. Sigue siendo mucho. Pero no veinticinco.",
        "[sarcastic] Los magos estudian años en el Colegio de Hibernalia. Tú solo necesitaste un collar, un anillo, un gorro y una túnica.",
    ]},
    {"id": "cr2", "frases": [
        "Más correo. @edgarvillalobos1492, con siete likes: «Buenos datos, lástima tanta AI».",
        "[deadpan] Buenos datos. Lo apunto. Es la reseña más bonita que nos han hecho, con la letra pequeña al final, como un contrato daédrico.",
        "[sarcastic] Y tranquilo, que el mago sin coste también usa ayuda: cuatro prendas encantadas. Y nadie le dice que eso no es magia de verdad.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. El Pararrayos.",
        "[deadpan] Tu bola de fuego me recarga la barra. Gracias.",
        "La absorción de hechizos es una probabilidad de anular el efecto entero y quedarte con la magia. Y funciona contra casi todo lo que no sea un golpe físico. Incluido el aliento de dragón.",
        "Hay tres caminos al cien por cien. El rápido: un bretón con su poder racial, más la piedra del Atronach. Cien por cien. Durante un minuto.",
        "El permanente, de Dragonborn: piedra del Atronach, cincuenta. La ventaja Atronach, treinta. La túnica de Mirák, quince. Y sus guantes o sus botas, cinco más. Cien. Con cualquier raza.",
        "[deadpan] Mirák lleva siglos preparándose para matarte. Y te deja la ropa que te hace inmune a él. Gracias, compañero.",
        "[sarcastic] ¡Y el tercero lo cuento yo, que me toca! Es un error: un vampiro cuenta como no muerto, así que la ventaja Necromago de Restauración te potencia a ti. Con el orden justo, cien por cien permanente.",
        "[deadpan] Hope, se dice por favor. La letra pequeña: con tanta absorción puedes absorber tus propias invocaciones, y fallan. Pero un sacerdote dragón y un dragón atacándote a la vez no te quitan ni un punto de vida.",
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
        "Lo medí yo, que ellos no tienen paciencia. En el juego base, sin trampas, el equipo llega a calidad veintinueve: más cincuenta y dos de daño en un arma. Con los Libros Negros de Dragonborn, calidad cuarenta y uno: más setenta y tres.",
        "[deadpan] La etiqueta sigue diciendo «Legendario». El número sigue subiendo. La etiqueta, como siempre, miente.",
        "[sarcastic] Y lo que a MariCarmen se le olvidó: la armadura se queda clavada en el tope. Ochenta por ciento menos de daño físico, con cualquier armadura que te pongas.",
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
        "El procedimiento es así: te pones la ropa de alquimia. Haces la poción. Te quitas la ropa. Te bebes la poción. Y repites.",
        "Cada vuelta, la ropa vale más. Y la poción, más. Y la ropa, más. Hasta que la ventana de efectos marca cifras de miles de por ciento.",
        "Los ingredientes: un montón de sal y unos peces. Los barriles del muelle de Ríften están llenos.",
        "Y este es mío. Con esas cifras, Congelación, un hechizo de principiante, mata dragones. Y en Xbox One, pasar de diez mil por ciento cuelga el juego. El juego se rinde antes que tú.",
        "Los Barbas Grises entrenan treinta años para dominar la Voz. Tú rompiste el universo en veinte minutos, con sal y pescado.",
        "[sarcastic] Y el último dato, para mí. El libro que vigila tu mesa en el Templo Nocturnal: Mannimarco, rey gusano. El rey de los nigromantes, de ayudante de cocina.",
    ]},
    {"id": "cierre", "frases": [
        "Este es el top. Del arquero que hace todo el mundo, al alquimista que borra el juego.",
        "Ahora te toca a ti. ¿Cuál falta? ¿La Hoja de ébano, que el juego cuenta como espada de una mano? ¿El hombre lobo? Déjalo en los comentarios: los leemos todos.",
        "Y suscríbete si aún no lo has hecho. Camino de diez mil. Y si quieres que alguno de los de la banca hable más, vota en los comentarios. [deadpan] No va a pasar. Nos vemos en Tamriel.",
    ]},
]

# --- VOCES (el usuario, 12-nov-2026): el Profeta GANÓ la votación → narra 8 de cada 10 datos y se burla desde arriba;
# Johnny, MariCarmen y Hope (empatados a 2 votos en el 2.º lugar) se pelean por el resto ---
VOCES = {"el Profeta": "HNSF1CTQmub252yhXROX", "Johnny": "HMCmDsbKeaSZp5LMOYKR", "MariCarmen": "YDDaC9XKjODs7hY78qEW",
         "Hope": "tnSpp4vdxKPjI9w0GnoV"}
_POR_FRASE = {"p10_4": "Johnny", "p10b_2": "MariCarmen", "p9_3": "Hope", "p9_7": "Johnny",
              "p8_3": "MariCarmen", "p8_5": "Johnny", "p7_4": "Johnny", "p7_5": "Hope",
              "p6_6": "MariCarmen", "p6b_1": "Johnny", "p5_5": "Hope", "p5_7": "Johnny",
              "p4_7": "MariCarmen", "p3_5": "Johnny", "p3_6": "Hope", "p2_4": "MariCarmen", "p2_6": "Hope",
              "p1_6": "Johnny", "p1_8": "Hope"}
NARRA = {}   # "escena_i": nombre de la voz (efectos.py pone la placa de quién narra en cada cambio)
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k, "el Profeta")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items() if v != "el Profeta"}
