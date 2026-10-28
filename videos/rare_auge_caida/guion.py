# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Rare: el estudio que Nintendo DEJÓ IR» (auge y caída, ~18 min; 28-oct-2026).
Tema elegido por el usuario entre 3 propuestas con datos (`fab.py ideas cronicas_gaming`): Kilobyte Chronicles «The Rise and Fall
of Rare, the Greatest Studio Nintendo Ever Gave Away» ×9,1 en un canal de 1 910 subs. Variable que cambia respecto a zelda_oot /
majora_mask: SOLO el formato (historia de un ESTUDIO, por capítulos, en vez de un juego con secretos). Voz Hope (`eleven_v4_turbo`).
Música = banda sonora OFICIAL de los juegos de Rare de cada época (regla del 23-oct; armar_musica_ost.py).

Datos verificados el 28-oct-2026 por un agente con fuentes (lista completa en fuentes_guion.md) y por mí:
- [O] news.xbox.com 22-sep-2026, memorando de Matt Booty: «Activision will expand its remit to World's Edge, as well as Rare.»
- [W] Wikipedia «Project Dream»: el protagonista era un niño llamado Edson, con su perro Dinger y el loro Billy; lo cambiaron por
  un conejo y luego por Banjo.
- [O] Microsoft 24-sep-2002: compra por 375 M US$ en efectivo (X02, Sevilla); cita de Ed Fries.
- [P] MacDougall (NoA, 2002): «value to the future of Nintendo would be limited»; Rare = 1,5 % del software de Nintendo (AF 2002).
- [P] David Wise (Nintendo Life 2014): SGI ~80 000 £ cada una, compraron dos; renders de una noche; demo de boxeo.
- [W] Nintendo 25 % en 1994 -> 49 % después (año sin confirmar: no se dice); plantilla 84 -> 250. DKC ~9,3 M; DKC2 5,15 M;
  DKC3 3,51 M; KI (SNES) 3,2 M. GoldenEye ~8 M (Guinness 8,09: el juego de Bond más vendido). DKR 4,88 M; DK64 5,27 M;
  BK 3,65 M; BT ~3 M. Kinect Sports 3 M (abr-may 2011). PDZ > 1 M. Viva Piñata ~500 000 casi un año después. N&B 140 000 en
  EE. UU. el primer mes. Rare Replay 30 juegos / 30 US$. SoT 40 M jugadores (abr-2024, con Game Pass); PS5 n.º 1 en Europa abr-2024.
- Lo DISCUTIDO se dice como tal: Knight Lore guardado (Retro Gamer lo cree exagerado); el Expansion Pak de DK64; Activision ganando
  la puja (versión de Ed Fries); el año del 49 % (no se dice).
"""

TITULO = "Rare: el estudio que Nintendo DEJÓ IR"
ARCHIVO = "rare_auge_caida"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)

# ElevenLabs dice el inglés nativo; solo lo que una voz en español leería mal («Rare» como «ra-re»)
FONETICA = {"Rare": "Réar", "Twycross": "Tuáicros", "Ashby-de-la-Zouch": "Áshbi de la Zuch", "Kazooie": "Kazúi",
            "Tooie": "Túi"}
# Revisado el 28-oct leyendo voz/eval.json: Whisper escribe «Ashby de la Suche», «Jetpack», «Attic Attack», «Sabrewolf»,
# «Nightlord», «Rear/real» (Rare), «Conquer», «Greg Mills», «Twicross», «300.000»: falsas alarmas de nombres y cifras.
CER_MAX_POR_FRASE = {"c1_1": 0.048, "c1_4": 0.024, "c1_5": 0.059, "c1_6": 0.042, "c1_9": 0.031, "c1_12": 0.024, "c2_5": 0.041, "c2_7": 0.026, "c3_2": 0.041, "c3_8": 0.047, "c3_12": 0.043, "c5_10": 0.043, "c5_14": 0.055, "c7_7": 0.081, "c7_9": 0.042, "c7_10": 0.07, "c7_16": 0.044, "c8_8": 0.037, "c8_10": 0.044, "cierre_2": 0.028, "cierre_4": 0.025}
TAIL_MAX_POR_FRASE = {}
GAP_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    # plan_clips.py (agente que miró las hojas de previews/_scan/): DK Rap, Battletoads, Aquatic Ambience, GoldenEye 4 jugadores…
    ambiente_por={'scene-011': 0.5, 'scene-028': 0.6, 'scene-044': 0.7, 'scene-058': 0.6, 'scene-060': 0.5, 'scene-068': 0.8, 'scene-110': 0.3, 'scene-112': 0.4},
    # SNES 8:7 = 0,18; 4:3 con franjas = 0,125; marca de IGN / borde = 0,04-0,05
    recorte_por={'scene-002': 0.18, 'scene-004': 0.17, 'scene-008': 0.05, 'scene-016': 0.125, 'scene-017': 0.125, 'scene-018': 0.125, 'scene-019': 0.125, 'scene-034': 0.05, 'scene-036': 0.18, 'scene-037': 0.05, 'scene-038': 0.05, 'scene-039': 0.18, 'scene-040': 0.18, 'scene-041': 0.05, 'scene-042': 0.18, 'scene-043': 0.18, 'scene-044': 0.18, 'scene-045': 0.18, 'scene-046': 0.18, 'scene-062': 0.125, 'scene-063': 0.125, 'scene-065': 0.11, 'scene-072': 0.125, 'scene-073': 0.125, 'scene-074': 0.125, 'scene-075': 0.125, 'scene-076': 0.125, 'scene-083': 0.18, 'scene-086': 0.18, 'scene-090': 0.18, 'scene-095': 0.05, 'scene-102': 0.04, 'scene-103': 0.04, 'scene-117': 0.18, 'scene-123': 0.18},
    yt=dict(sufijo="", min_s=30, max_min=1100, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: la música es la banda sonora OFICIAL de los juegos de Rare (armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] En septiembre de 2002, Nintendo era dueña de casi la mitad de uno de los mejores estudios de la historia. [short pause] Y lo dejó ir.",
        "Ese estudio había hecho Donkey Kong Country, GoldenEye, Banjo-Kazooie y Perfect Dark. Juegos que, juntos, vendieron decenas de millones de copias.",
        "[curious] Microsoft lo compró entero, por 375 millones de dólares. Y lo que pasó después es una de las historias más raras de los videojuegos.",
        "[playful] Y nunca mejor dicho, porque el estudio se llamaba Rare. [short pause] Que en inglés significa raro.",
        "Hoy te cuento cómo dos hermanos de un pueblo inglés llegaron a la cima de Nintendo, por qué cayeron, y qué les pasó este mismo año.",
        "[thoughtful] Porque la historia de Rare tiene un giro final que casi nadie vio venir.",
    ]},
    {"id": "c1", "frases": [
        "[warm] Capítulo 1. [short pause] Dos hermanos y un secreto.",
        "Todo empieza en 1982, en Ashby-de-la-Zouch, un pueblo del centro de Inglaterra.",
        "Tim y Chris Stamper venían de programar conversiones de máquinas recreativas. Ese año fundaron una empresa pequeña, con su amigo John Lathbury y con Carole Ward, la novia de Tim, que después sería su esposa.",
        "Sus juegos salían con un sello de nombre enorme. [short pause] Ultimate Play the Game.",
        "[excited] El primero, Jetpac, salió en mayo de 1983 para la computadora ZX Spectrum.",
        "Según la revista Retro Gamer, vendió más de 300 000 copias, y facturó más de un millón de libras.",
        "Después vino Atic Atac. Y en 1984, Sabre Wulf, que costaba casi el doble que un juego normal. [short pause] Ultimate dijo que era para frenar la piratería.",
        "[curious] Pero lo que más llamaba la atención era su silencio. Sus anuncios no enseñaban ni una captura del juego, y los Stamper casi nunca daban entrevistas.",
        "Cuando una revista les preguntó por su siguiente juego, la respuesta fue: [whispers] eso no te lo podemos decir.",
        "[mysterious] Y de ahí sale una leyenda. En 1988, Tim Stamper contó que Knight Lore ya estaba terminado antes que Sabre Wulf, y que lo guardaron para no hundir las ventas de su otro juego.",
        "Knight Lore salió en noviembre de 1984, con una vista isométrica, en falso 3D, que en la Spectrum parecía de otro planeta.",
        "[playful] Eso sí. Años después, Retro Gamer analizó el código, y concluyó que la historia probablemente es exagerada.",
        "Pero los Stamper ya miraban a otro lado. [short pause] Al otro lado del mundo, una consola japonesa estaba arrasando.",
    ]},
    {"id": "c2", "frases": [
        "[serious] Capítulo 2. [short pause] Abrir la caja de Nintendo.",
        "En abril de 1985 registraron una empresa nueva, Rare Limited. Y dejaron Ultimate en manos de otra compañía, U.S. Gold.",
        "Su objetivo era la Famicom de Nintendo, la consola que en América se llamó Nintendo Entertainment System.",
        "Pero nadie les había dado un manual. Así que la estudiaron por dentro, a ciegas.",
        "Uno de sus trabajadores, Dave Thomas, lo recordó así: era mandar valores a la memoria, uno por uno, hasta que pasara algo.",
        "[impressed] Con lo que aprendieron hicieron una demo, se la enseñaron a Nintendo, y salieron de ahí con los manuales oficiales. Y con trabajo.",
        "Entre 1987 y 1993 hicieron unos 47 juegos para la NES. Para Nintendo, para Tradewest, y para Milton Bradley.",
        "Ahí están R.C. Pro-Am, Snake Rattle 'n' Roll, y en 1991, Battletoads.",
        "[amused] Battletoads se hizo famoso por su dificultad. El nivel de las motos todavía persigue a toda una generación.",
        "No todos fueron grandes juegos. Muchos eran encargos. Pero Rare aprendió algo que valía oro: cómo sacarle todo a una máquina de Nintendo.",
        "[thoughtful] Y en 1993, se jugó el estudio entero en una sola apuesta.",
    ]},
    {"id": "c3", "frases": [
        "[excited] Capítulo 3. [short pause] La apuesta.",
        "A principios de los noventa, Silicon Graphics fabricaba las estaciones de trabajo con las que Hollywood creaba sus efectos por computadora.",
        "Rare compró esas máquinas. El compositor David Wise recuerda que costaban unas 80 000 libras cada una, y que para comprar dos, el estudio se arriesgó muchísimo.",
        "La idea era modelar personajes en 3D en esas máquinas, y convertirlos en imágenes que pudiera mover una Super Nintendo.",
        "Cada render tardaba una noche entera. Y según el equipo, había un aire acondicionado enorme solo para enfriarlas.",
        "[curious] Con esa técnica hicieron una demo de boxeo. Y cuando los directivos de Nintendo la vieron, quedaron convencidos.",
        "En 1994, Nintendo compró el 25 % de Rare. Más tarde subió al 49 %. [short pause] Casi la mitad.",
        "Con ese dinero, la plantilla pasó de 84 personas a 250.",
        "Y Nintendo les confió a uno de sus personajes más famosos. [short pause] Donkey Kong.",
        "[excited] Donkey Kong Country salió en noviembre de 1994. Parecía imposible que algo así corriera en una Super Nintendo.",
        "Vendió unos 9,3 millones de copias. Es uno de los juegos más vendidos de toda la consola.",
        "[playful] Hay una leyenda de que a Shigeru Miyamoto no le gustaba. Él mismo la desmintió: dijo que trabajó muy de cerca con Rare, y que se escribía casi a diario con Tim Stamper.",
        "El equipo también creó un compañero. Iba a ser Donkey Kong Junior rediseñado, pero Nintendo pidió usar al original o inventar uno nuevo. [short pause] Así nació Diddy Kong.",
        "Y la música de David Wise, con temas como Aquatic Ambience, sigue siendo de las más queridas de la Super Nintendo.",
        "Después llegaron Killer Instinct, que vendió 3,2 millones en Super Nintendo, Donkey Kong Country 2, con más de 5 millones, y Donkey Kong Country 3.",
        "[thoughtful] La apuesta había salido bien. Y la siguiente consola de Nintendo iba a pedirles algo todavía más difícil.",
    ]},
    {"id": "c4", "frases": [
        "[serious] Capítulo 4. [short pause] El juego que nadie esperaba.",
        "A Rare le tocó el juego de GoldenEye, la película de James Bond de 1995. Y al principio, iba a ser un juego en 2D, de desplazamiento lateral.",
        "Lo dirigió Martin Hollis, con un equipo pequeño de gente que, según él, no tenía experiencia profesional haciendo juegos.",
        "El compositor Grant Kirkhope lo contó este mismo año: probablemente eran 12 personas, y ninguno había hecho un juego antes.",
        "[amused] Hollis también recordaba que pasaban temporadas de meses sin que nadie de la dirección de Rare o de Nintendo entrara en sus oficinas.",
        "Y eso dio para mucho. El modo multijugador lo programó Steve Ellis en un mes, en 1997, sin que la dirección lo supiera.",
        "[curious] Hasta Miyamoto opinó. Envió una sugerencia: que al final, Bond visitara a sus enemigos en el hospital, y les diera la mano.",
        "Hollis no la usó. Pero de ahí salieron los créditos finales, que presentan a los enemigos como si fueran actores de la película.",
        "Cuando dejaron de corregir errores para poder sacarlo, el equipo esperaba, en palabras de Kirkhope, un desastre total.",
        "[excited] GoldenEye 007 salió en agosto de 1997, casi dos años después de la película.",
        "Vendió unos 8 millones de copias. Según Guinness, es el juego de James Bond más vendido de la historia.",
        "Y su multijugador a pantalla partida, el que se hizo a escondidas, es lo primero que muchos recuerdan de su Nintendo 64.",
        "[thoughtful] Rare ya no era un estudio inglés más. Era la gran estrella de la consola.",
    ]},
    {"id": "c5", "frases": [
        "[excited] Capítulo 5. [short pause] La fábrica de clásicos.",
        "Lo que vino después parece una lista inventada.",
        "En 1997, Diddy Kong Racing, que vendió casi 5 millones de copias.",
        "En 1998, Banjo-Kazooie. [short pause] Y aquí hay una curiosidad.",
        "Banjo nació de un proyecto cancelado llamado Dream. Un juego de rol, cuyo protagonista era un niño llamado Edson.",
        "Edson tenía un perro, Dinger, y un loro. Pero con los años, Rare sintió que el niño perdía fuerza, y lo cambió primero por un conejo, y al final, por un oso.",
        "Banjo-Kazooie vendió más de 3,6 millones, y Banjo-Tooie, en el año 2000, unos 3 millones más.",
        "Entre medias llegaron Jet Force Gemini, en 1999, y Donkey Kong 64, que superó los 5 millones.",
        "[curious] Donkey Kong 64 necesitaba el Expansion Pak, un cartucho de memoria extra para la consola. Y el porqué todavía se discute.",
        "Unos dicen que fue para esquivar un error que colgaba el juego. Otros, que se pidió desde el principio para la iluminación.",
        "[playful] Y también traía el DK Rap, de Grant Kirkhope, que acabó sonando en la película de Super Mario Bros de 2023.",
        "En el año 2000 llegó Perfect Dark, el sucesor de GoldenEye, con Joanna Dark como protagonista.",
        "Pero Martin Hollis había dejado el proyecto a los 14 meses. [short pause] Y no fue el único en irse.",
        "En 1999, cuatro miembros del equipo de GoldenEye, entre ellos David Doak y Steve Ellis, fundaron su propio estudio, Free Radical. En el año 2000 sacaron TimeSplitters, para PlayStation 2.",
        "[amused] Y en 2001, Rare hizo algo que nadie veía venir. [short pause] Conker.",
        "Conker era una ardilla tierna, de un juego familiar llamado Twelve Tales: Conker 64. Pero los avances no convencieron.",
        "Así que Rare lo convirtió en Conker's Bad Fur Day. Un juego para adultos, con palabrotas, resacas y parodias de películas.",
        "Muchos pensaron que el anuncio era una broma. Hasta hubo una gira de torneos por veinte universidades, organizada por Playboy.",
        "[sighs] Pero salió en marzo de 2001, cuando la Nintendo 64 ya se despedía. Y vendió muy por debajo de lo esperado.",
        "[thoughtful] Para entonces, Rare tenía un problema mayor. [short pause] Su socio ya no la miraba igual.",
    ]},
    {"id": "c6", "frases": [
        "[serious] Capítulo 6. [short pause] El divorcio.",
        "Rare llevaba años trabajando en un juego para Nintendo 64 llamado Dinosaur Planet.",
        "Miyamoto los convenció de convertirlo en un juego de Star Fox. Y así, ya en GameCube, nació Star Fox Adventures.",
        "Salió en Estados Unidos el 23 de septiembre de 2002. [short pause] Y fue el último juego de Rare para Nintendo.",
        "[dramatic] Porque al día siguiente, el 24 de septiembre, en un evento de Xbox en Sevilla, Microsoft anunció que había comprado Rare. [short pause] Por 375 millones de dólares, en efectivo.",
        "Nintendo, que tenía el 49 %, vendió su parte. Y la pregunta es obvia. ¿Por qué no compró el 51 % que le faltaba?",
        "Peter MacDougall, de Nintendo of America, lo explicó así: el valor de Rare para el futuro de Nintendo sería limitado.",
        "Y dio un dato. [short pause] En su último año fiscal, Rare solo había aportado el 1,5 % de las ventas de software de Nintendo.",
        "Tim Stamper lo vio de otra forma. Años después dijo que no tenía ni idea de por qué Nintendo no los compró, y que pensaba que encajaban bien.",
        "[curious] Microsoft no fue la única interesada. Según Ed Fries, el jefe de los juegos de Xbox, Activision llegó a ir ganando la puja.",
        "Nintendo tenía derecho a igualar cualquier oferta, pero no lo hizo. Y Microsoft subió la suya al final.",
        "Ed Fries lo celebró diciendo que no se emocionaba tanto desde la primera vez que jugó a un juego de Rare.",
        "[serious] Pero todo divorcio tiene un reparto.",
        "Donkey Kong, Diddy y Star Fox se quedaron con Nintendo. [short pause] Banjo, Conker y Joanna Dark se fueron con Rare.",
        "[sighs] Rare se llevaba a sus personajes. Pero dejaba atrás al gorila que la había hecho famosa.",
    ]},
    {"id": "c7", "frases": [
        "[serious] Capítulo 7. [short pause] La caída.",
        "El primer juego de Rare para Xbox fue Grabbed by the Ghoulies, en 2003. Y no funcionó.",
        "Años después, Nick Burton, de Rare, lo resumió así: quizá su estilo no encajaba en esa consola, en ese momento.",
        "En 2005, Rare puso dos juegos en el lanzamiento de Xbox 360. Kameo, y Perfect Dark Zero.",
        "Los dos equipos admitieron después que les habrían venido bien seis meses más.",
        "Perfect Dark Zero vendió más de un millón de copias. Pero no fue el fenómeno que había sido GoldenEye.",
        "[warm] En 2006 llegó Viva Piñata, que había nacido como una idea para teléfonos móviles. La crítica lo adoró, y hasta tuvo su propia serie de televisión.",
        "[sighs] Pero casi un año después de salir, llevaba unas 500 000 copias.",
        "Y el 2 de enero de 2007, Tim y Chris Stamper dejaron Rare, para dedicarse a otros proyectos.",
        "[playful] En 2008 volvió Banjo. Por fin. [short pause] Pero en Nuts and Bolts casi no había plataformas: el juego iba de construir vehículos.",
        "Vendió 140 000 copias en Estados Unidos en su primer mes. Gregg Mayles, el creador de Banjo, admitió años después que quizá fue un cambio demasiado radical.",
        "Ese mismo año, Rare hizo algo que verías en millones de consolas. [short pause] Los avatares de Xbox 360.",
        "Y en 2010, Kinect Sports, para la cámara de movimiento de Microsoft. Vendió 3 millones de copias en menos de un año.",
        "[thoughtful] Era un éxito. Pero no era el Rare de antes. Y la gente que había hecho los clásicos se seguía yendo.",
        "Unos treinta empleados se marcharon durante la venta de 2002. Y muchos más, en los años siguientes.",
        "En 2015, un grupo de veteranos de Rare, en su nuevo estudio, Playtonic, pidió dinero en Kickstarter para un sucesor de Banjo. [short pause] Yooka-Laylee.",
        "[impressed] Pedían 175 000 libras. Las consiguieron en unos 40 minutos. Y al final juntaron más de 2 millones, un récord en el Reino Unido.",
        "Mientras, en Rare, después de Kinect Sports Rivals en 2014, hubo despidos. Y muchos fans daban al estudio por muerto.",
    ]},
    {"id": "c8", "frases": [
        "[warm] Capítulo 8. [short pause] Un barco pirata.",
        "En 2015, por sus 30 años, Rare sacó Rare Replay. 30 juegos de su historia, por 30 dólares, con más de una hora de documentales.",
        "Y en 2018 lanzó algo completamente nuevo. [short pause] Sea of Thieves.",
        "Un juego de piratas en línea, donde tú y tus amigos manejan un barco de verdad. Uno al timón, otro en las velas, y otro sacando agua.",
        "[impressed] En abril de 2024, Rare dijo que ya había atraído a 40 millones de jugadores, contando Game Pass.",
        "Y ese mismo mes llegó a PlayStation 5. Fue el juego más descargado de PS5 en Europa en abril, aunque salió el último día del mes.",
        "Parecía el regreso. Rare preparaba otro juego nuevo, Everwild, anunciado en 2019.",
        "[sighs] Pero el 2 de julio de 2025, en plena ola de despidos de Microsoft, Everwild fue cancelado.",
        "Y en octubre de 2025, Gregg Mayles, el diseñador de Donkey Kong Country y de Banjo-Kazooie, dejó Rare después de unos 36 años.",
        "En junio de este año se anunció una película de acción real de Sea of Thieves.",
        "[serious] Y en julio, Xbox anunció unos 3 200 despidos, y se desprendió de cinco estudios. [short pause] Rare no estaba entre ellos.",
    ]},
    {"id": "cierre", "frases": [
        "[dramatic] Pero el 22 de septiembre de 2026, llegó un memorando de Matt Booty, el jefe de los estudios de Xbox.",
        "Y una sola frase cambiaba el destino del estudio. Activision ampliaba su responsabilidad. [short pause] También a Rare.",
        "[thoughtful] Activision. La misma empresa que, según Ed Fries, casi compra Rare en 2002.",
        "Veinticuatro años después, el estudio que Nintendo dejó ir acabó, de todas formas, dependiendo de Activision.",
        "Rare sigue en Twycross, con su barco pirata a flote. Y por ahora, sin ningún juego nuevo anunciado.",
        "[curious] Ahora dime tú en los comentarios. [short pause] ¿Cuál es tu juego favorito de Rare? ¿Y crees que Nintendo se equivocó al dejarla ir?",
        "[warm] Y si quieres más de esa época dorada, aquí tienes la historia de Banjo-Tooie y sus 10 secretos. Nos vemos en la próxima.",
    ]},
]
