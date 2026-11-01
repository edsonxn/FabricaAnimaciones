# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Los 30 SECRETOS de la Nintendo 64 QUE IGNORASTE» (31-oct-2026, ~23 min).
Pedido del usuario: video de 23 min. Elegido entre 3: secretos de toda la consola. Variable que cambia respecto a spyro2/mario64_secretos:
de UN juego a TODA la consola. Motor SECUENCIA YT, voz ElevenLabs Hope, música = OST de CADA juego por secreto (audio/ost,
armar_musica_ost.py), SFX del juego de cada secreto, kit nucleo/mg_n64.py (interfaz del hardware).
Datos: investigacion.md (sellos VERIFICADO/DUDOSO/TEORÍA y fuentes). Comprobado en fuente directa el 31-oct: Iwata Asks (prototipo, fines de
semana, figuras sin cara), CGC/cllct (175 000 US$, Heritage, nov-2024), transcripción GDC 2005 y fallecimiento de Iwata (11-jul-2015, 55 años).
NO decir: que la demo de FF corrió en N64; que Konami obligó a cambiar el nombre; que los arcades Ultra 64 usaban su hardware; que Nintendo
perdió demandas por Mario Party; cifra de unidades del 64DD; 165:1 de compresión de RE2; el último juego por región; que Columbine fue la
causa confirmada de Perfect Head; que Body Harvest inspiró GTA III como hecho.
No repetir: lo ya contado en zelda_oot, majora_mask, mario64_secretos, banjo_tooie, bt_*, rare_auge_caida y oot_remake_cambios.
"""

TITULO = "Los 30 SECRETOS de la Nintendo 64 QUE IGNORASTE"
ARCHIVO = "n64_secretos"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)
# ElevenLabs dice el inglés nativo; solo lo que leería mal
FONETICA = {"64DD": "sesenta y cuatro dedé", "iQue": "ái kiú", "SIGGRAPH": "Síggraf", "Wide-Boy64": "Uáid Boi sesenta y cuatro", "Dobutsu no Mori": "Dóbutsu no Móri"}
# Falsas alarmas de Whisper (cifras, Pak/Pack, nombres): comparadas textos.json con eval.json el 31-oct
CER_MAX_POR_FRASE = {'s14_3': 0.0565, 's24_1': 0.0295, 'h3_1': 0.0848, 'h3_2': 0.0563, 's28_1': 0.0015, 's24_3': 0.0334, 's23_3': 0.016, 's20_1': 0.014, 's19_2': 0.0419, 's18_2': 0.0415, 's16_0': 0.0556, 's15_2': 0.0295, 's14_1': 0.0149, 's14_2': 0.0189, 's13_2': 0.0265, 's12_0': 0.0215, 's11_4': 0.0314, 's09_2': 0.1053, 's08_1': 0.084, 's08_4': 0.0534, 's06_1': 0.0015, 's05_3': 0.014, 's04_2': 0.0363, 'cierre_2': 0.0182}
TAIL_MAX_POR_FRASE = {'s14_3': 0.67, 's24_1': 0.38, 'h3_1': 0.05, 'h3_2': 0.46, 's28_1': 1.09, 's24_3': 0.38, 's23_3': 0.21, 's20_1': 0.91, 's19_2': 0.46, 's18_2': 0.73, 's16_0': 0.05, 's15_2': 0.58, 's14_1': 0.87, 's14_2': 0.62, 's13_2': 0.65, 's12_0': 0.15, 's11_4': 0.69, 's09_2': 0.53, 's08_1': 0.45, 's08_4': 0.22, 's06_1': 1.03, 's05_3': 0.62, 's04_2': 0.89, 'cierre_2': 0.49}
GAP_MAX_POR_FRASE = {'s14_3': 0.22, 's24_1': 0.48, 'h3_1': 0.11, 'h3_2': 0.46, 's28_1': 0.48, 's24_3': 0.33, 's23_3': 0.21, 's20_1': 0.24, 's19_2': 0.08, 's18_2': 0.44, 's16_0': 0.37, 's15_2': 0.49, 's14_1': 0.41, 's14_2': 0.47, 's13_2': 0.4, 's12_0': 0.43, 's11_4': 0.41, 's09_2': 0.58, 's08_1': 0.29, 's08_4': 0.14, 's06_1': 0.4, 's05_3': 0.43, 's04_2': 0.31, 'cierre_2': 0.19}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    ambiente_por={'scene-001': 0.6, 'scene-019': 0.8, 'scene-022': 0.7, 'scene-025': 0.6, 'scene-026': 0.6, 'scene-032': 0.7, 'scene-033': 0.7, 'scene-038': 0.5, 'scene-040': 0.6, 'scene-041': 0.6, 'scene-042': 0.6, 'scene-043': 0.6, 'scene-052': 0.7, 'scene-066': 0.7, 'scene-067': 0.7, 'scene-068': 0.6, 'scene-069': 0.6, 'scene-077': 0.6, 'scene-078': 0.6, 'scene-079': 0.6, 'scene-080': 0.6, 'scene-084': 0.7, 'scene-112': 0.7, 'scene-113': 0.7, 'scene-114': 0.6, 'scene-125': 0.6, 'scene-126': 0.6, 'scene-131': 0.5, 'scene-132': 0.5, 'scene-134': 0.7, 'scene-135': 0.7, 'scene-139': 0.7, 'scene-142': 0.6, 'scene-144': 0.7, 'scene-150': 0.6, 'scene-152': 0.8, 'scene-153': 0.8, 'scene-158': 0.7},
    recorte_por={},
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora de cada juego (audio/ost, armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[whispers] Nintendo tuvo que repartir guantes, porque un juego de su consola les estaba abriendo las manos a los niños.",
        "[amused] Hubo un Tetris que te medía el pulso con una pinza en la oreja, y te complicaba la partida si se te aceleraba el corazón.",
        "[mysterious] Hubo una Nintendo 64 escondida dentro de un mando, y solo se vendió en China.",
        "[impressed] Y el juego de peleas más famoso de Nintendo lo programó un hombre solo, en sus fines de semana, con cuatro muñecos sin cara.",
        "Todo eso pasó en la misma consola. La Nintendo 64 cumplió treinta años en 2026, y este mes vuelve a estar en boca de todos con el remake de Ocarina of Time.",
        "[excited] Hoy te cuento cómo nació, por qué perdió la guerra, y los 30 secretos que seguramente ignoraste.",
    ]},

    # ================================================================ HISTORIA
    {"id": "h1", "frases": [
        "[warm] Empecemos en 1993. Jim Clark, el fundador de Silicon Graphics, tenía una idea: meter la tecnología de sus estaciones de trabajo en una consola de casa.",
        "Se reunió con Hiroshi Yamauchi, el presidente de Nintendo. Y el 23 de agosto de 1993 anunciaron el acuerdo, con nombre de película: Project Reality.",
        "[impressed] La promesa era enorme. Arcades para 1994, consola para finales de 1995, y por menos de 250 dólares.",
        "En 1994 la rebautizaron Ultra 64. Y al final, para usar una sola marca en todo el mundo, según Nintendo, se quedó en Nintendo 64.",
        "[sarcastic] Mientras tanto, Sega ya vendía la Saturn, y Sony la PlayStation. Y la consola que iba a llegar en 1995 se retrasó a abril de 1996. Y luego, a junio.",
        "[curious] Nintendo dijo que no podía fabricar suficientes unidades. Un exingeniero de Silicon Graphics culpó a los chips. Nadie lo ha cerrado del todo.",
    ]},
    {"id": "h2", "frases": [
        "[thoughtful] Y entonces llegó la decisión que marcó a la consola. Mientras todos se pasaban al CD, Nintendo se quedó con el cartucho.",
        "Tenía sus razones. Casi sin tiempos de carga, y mucho más difícil de piratear.",
        "[curious] Pero un CD guardaba 650 megabytes, y el cartucho más grande de la consola, 64.",
        "Cada tirada de cartuchos tardaba al menos dos semanas en fabricarse, y cada juego salía unos diez dólares más caro que en PlayStation.",
        "[mysterious] Y hubo juegos que ya no cabían. Square se llevó Final Fantasy VII a Sony. Esa historia la guardo para el final, porque tiene trampa.",
        "[amused] Yamauchi, además, anunció que limitaría los juegos para que cada uno fuera mejor. Y vaya si se limitaron: 388 juegos oficiales en toda su vida, frente a más de cuatro mil en PlayStation.",
    ]},
    {"id": "h3", "frases": [
        "El 23 de junio de 1996 salió en Japón, con solo tres juegos: Super Mario 64, Pilotwings 64 y uno de shogi.",
        "[excited] Las 300 000 consolas del primer día se agotaron.",
        "En Estados Unidos llegó en septiembre, a 199 dólares con 99. Y en tres días vendió 350 000 de las 500 000 disponibles.",
        "Traía cuatro puertos para mandos. Miyamoto explicó por qué: era la primera consola capaz de dividir la pantalla en cuatro sin arrastrarse.",
        "[playful] Y ahí nacieron las tardes enteras de Mario Kart, de GoldenEye y de perder amistades.",
    ]},
    {"id": "h4", "frases": [
        "Pero la guerra se decidía en otra parte. La Nintendo 64 vendió 32,93 millones de consolas. PlayStation, más de cien millones.",
        "[curious] Y en su propio país fue un golpe: 5,54 millones en Japón, frente a 20,63 en América.",
        "GameCube llegó en 2001, y al año siguiente la Nintendo 64 se dejó de fabricar.",
        "[warm] Perdió en las cifras, sí. Pero por eso mismo es tan interesante. Una consola con pocos juegos, muchas ideas raras, y accesorios que hoy cuesta creer que existieran.",
        "[playful] Así que vamos con lo bueno. Los 30 secretos, del treinta al uno.",
    ]},

    # ================================================================ 30 SECRETOS (del 30 al 1)
    {"id": "s30", "frases": [
        "[playful] Número treinta. El personaje que nadie pidió.",
        "Waluigi nació en Mario Tennis, en el año 2000, con un solo trabajo: que Wario tuviera pareja en los dobles.",
        "Su nombre mezcla Luigi con warui, que en japonés significa malo. Y lleva en la gorra una L invertida, que es su forma de ser malvado.",
        "[sarcastic] Un cuarto de siglo después sigue sin juego propio, y sin pisar un Mario principal. Y aun así, internet lo adora.",
    ]},
    {"id": "s29", "frases": [
        "[curious] Número veintinueve. Un juego de NES dentro de un cartucho.",
        "Excitebike 64 esconde una versión emulada del Excitebike original.",
        "[impressed] Y no solo eso. También puedes desbloquear Excite 3D, la misma idea del clásico con gráficos de la época, y un partido de fútbol con motos y un balón gigante.",
        "[amused] Un juego viejo emulado dentro de uno nuevo. Nintendo ya estaba ensayando Switch Online en el año 2000, y no lo sabía.",
    ]},
    {"id": "s28", "frases": [
        "[mischievous] Número veintiocho. El Rushmore de Mario.",
        "En Pilotwings 64, la isla Little States es Estados Unidos en miniatura. Y en su monte Rushmore, una de las caras no es de ningún presidente. Es la de Mario.",
        "[sarcastic] Si le disparas con los misiles del girocóptero, la cara cambia. Y aparece Wario.",
        "[amused] El juego lo hizo Nintendo con Paradigm, una empresa de simuladores militares. Eso explica lo de los misiles. Un juego de lanzamiento que ya te dejaba bombardear a su mascota.",
    ]},
    {"id": "s27", "frases": [
        "[curious] Número veintisiete. El stick no era lo que parecía.",
        "El famoso stick analógico no sabe dónde está. Mueve una rueda que corta un haz de luz, y un sensor cuenta los cortes. Igual que un ratón de bola.",
        "[impressed] Por eso, al encender la consola, da por hecho que está en el centro. Y por eso existe el truco de apretar L, R y Start a la vez: lo vuelve a centrar.",
        "[amused] Y con el uso, el mecanismo se aflojaba. Apunta ese detalle, porque el stick va a volver en esta lista, y no para bien.",
    ]},
    {"id": "s26", "frases": [
        "[sarcastic] Número veintiséis. Los 64 bits de la Nintendo 64.",
        "El nombre lo vendía todo. Y el procesador sí era de 64 bits.",
        "[curious] Pero casi nadie los usaba. Las instrucciones de 32 bits corrían más rápido, así que los programadores se quedaban con ellas.",
        "[amused] Es como comprar un deportivo, y que todos lo manejen en segunda porque va mejor.",
    ]},
    {"id": "s25", "frases": [
        "[excited] Número veinticinco. El temblor que cambió los mandos.",
        "En abril de 1997, Star Fox 64 llegó con un regalo en la caja: el Rumble Pak.",
        "[impressed] Cuando te daban un golpe, el mando temblaba en tus manos. Hoy lo trae cualquier consola, pero entonces era magia.",
        "[sarcastic] Eso sí, funcionaba con dos pilas AAA, y ocupaba el puerto de la tarjeta de memoria. Así que en muchos juegos, para guardar partida, te tocaba sacarlo.",
    ]},
    {"id": "s24", "frases": [
        "[curious] Número veinticuatro. El aparato que solo tenía la prensa.",
        "¿Cómo sacaban las revistas sus capturas de Game Boy? Con esto: el Wide-Boy64.",
        "Se conectaba a una Nintendo 64 y ponía los juegos de Game Boy en un monitor. No emulaba nada: llevaba hardware real de Game Boy dentro.",
        "[amused] Costaba 1 400 dólares, y solo se vendía a desarrolladores y periodistas. Y tú, soplándole al cartucho.",
    ]},
    {"id": "s23", "frases": [
        "[mysterious] Número veintitrés. El tapón que hace arrancar la consola.",
        "Si abres la tapa de arriba de una Nintendo 64, encuentras una pieza que parece no hacer nada: el Jumper Pak.",
        "[curious] No tiene memoria. Solo cierra el circuito de la RAM. Pero si la sacas y no pones nada en su lugar, la consola no arranca, y la tele se queda en negro.",
        "[amused] Así que antes de dar por muerta una Nintendo 64, mira primero ese tapón.",
    ]},
    {"id": "s22", "frases": [
        "[curious] Número veintidós. Por qué todo se veía borroso.",
        "Seguro lo recuerdas. Esos muros lavados, como vistos a través de vaselina.",
        "[impressed] La culpa la tenían cuatro kilobytes. Esa era toda la memoria para texturas de la consola. Y con el filtrado, se quedaban en la mitad.",
        "Por eso Super Mario 64 tiene tantas superficies de color liso. No era un estilo. Era supervivencia.",
        "[amused] Para que te hagas una idea: el texto de este guion no cabría ahí.",
    ]},
    {"id": "s21", "frases": [
        "[curious] Número veintiuno. La pista donde el juego se rinde.",
        "En Mario Kart 64, Yoshi Valley es un laberinto con varios caminos de distinta longitud.",
        "[amused] Tantos, que el juego no puede decirte en qué lugar vas. Lo reconoce hasta el manual: en el panel de posición solo verás un signo de interrogación.",
        "[mischievous] Mira el mapa. Dos jugadores pueden ir por caminos distintos, y no sabrás quién va ganando hasta cruzar la meta.",
    ]},
    {"id": "s20", "frases": [
        "[playful] Número veinte. Pokémon Rojo en la tele.",
        "Pokémon Stadium traía el Transfer Pak, un accesorio para enchufar cartuchos de Game Boy al mando.",
        "[impressed] Con él pasabas tus Pokémon a la consola. Y dentro del juego había una torre, la Game Boy Tower, que te dejaba jugar a Rojo y Azul en la pantalla grande.",
        "[excited] Y con la torre Doduo iba al doble de velocidad, y con la Dodrio, al triple. El sueño de cualquiera que haya subido de nivel a un Magikarp.",
    ]},
    {"id": "s19", "frases": [
        "[curious] Número diecinueve. El juego que no se podía comprar.",
        "ClayFighter sesenta y tres y un tercio tuvo una edición ampliada, Sculptor's Cut, que salió en 1998 solo para alquilar en Blockbuster.",
        "[surprised] En noviembre de 2024, un ejemplar sellado se vendió en Heritage por 175 000 dólares.",
        "[sarcastic] Seguro que tú lo devolviste a tiempo. Una lástima.",
    ]},
    {"id": "s18", "frases": [
        "[sarcastic] Número dieciocho. Los anillos de Superman 64.",
        "Superman 64 es famoso por dos cosas: ser de los peores juegos de la historia, y esos anillos.",
        "[curious] Pero ese no era el plan. Eric Caen, de Titus, quería un mundo abierto. Según lo que se ha contado, Warner Bros. pidió primero un SimCity con Superman de alcalde.",
        "Luego le limitó los poderes, le prohibió destruir edificios, y lo metió en un mundo virtual creado por Lex Luthor.",
        "[amused] Los anillos eran el tutorial. Y acabaron siendo el juego. Y la famosa niebla de kriptonita era solo una forma de no dibujar el horizonte.",
    ]},
    {"id": "s17", "frases": [
        "[curious] Número diecisiete. La consola que llegó a los arcades sin llegar.",
        "Antes de que existiera la consola, ya había máquinas con el rótulo Ultra 64: Killer Instinct y Cruis'n USA.",
        "[impressed] Las vendían como un adelanto de lo que tendrías en casa. Pero ninguna llevaba el hardware de la consola. Cada una tenía su propia placa.",
        "[sarcastic] Y lo que llegó a casa fue Killer Instinct Gold, que era otro juego. Publicidad de la buena.",
    ]},
    {"id": "s16", "frases": [
        "[playful] Número dieciséis. El quiosco de Pokémon Snap.",
        "En 1999, en los Blockbuster de Estados Unidos, había un aparato con una Nintendo 64 y una impresora.",
        "[impressed] Llevabas tu cartucho de Pokémon Snap, elegías tus mejores fotos, y por unos tres dólares te llevabas dieciséis pegatinas.",
        "En Japón se hizo lo mismo en las tiendas Lawson.",
        "[amused] Antes de las redes sociales, presumir a tu Pikachu costaba dinero.",
    ]},
    {"id": "s15", "frases": [
        "[mysterious] Número quince. La consola de los hoteles.",
        "En ciertos hoteles de Norteamérica, encendías la tele de la habitación y ahí estaba: una Nintendo 64. Y no era un regalo.",
        "Era el sistema Nintendo Gateway, con la empresa LodgeNet. En febrero del año 2000 había Nintendo 64 en 100 000 habitaciones de 620 hoteles.",
        "[amused] Pagabas por hora, y te lo cargaban a la cuenta de la habitación.",
        "[sarcastic] Imagina justificarle eso a tu empresa. Reunión con el cliente, tres horas de Mario Kart.",
    ]},
    {"id": "s14", "frases": [
        "[surprised] Número catorce. La consola dentro del mando.",
        "En noviembre de 2003, con GameCube ya en las tiendas, Nintendo lanzó en China una Nintendo 64 nueva: el iQue Player. Y la consola entera iba metida dentro del mando.",
        "[curious] China prohibía las consolas desde el año 2000, y esto sorteaba la prohibición. Tampoco había cartuchos: los juegos se bajaban en quioscos.",
        "[amused] Se calcula que vendió entre 8 000 y 12 000 unidades. Y el servicio siguió hasta finales de 2016, veinte años después de la Nintendo 64 original.",
    ]},
    {"id": "s13", "frases": [
        "[curious] Número trece. Tu cara en Perfect Dark.",
        "En el E3 de 1999, Rare enseñó algo de ciencia ficción. Con una Game Boy Camera y el Transfer Pak, te sacabas una foto y la pegabas en la cabeza de un personaje.",
        "Se llamaba Perfect Head. Y se había probado de verdad: hay capturas internas con la cara de Ken Lobb.",
        "[thoughtful] La función se eliminó poco antes de salir. Mucha gente lo atribuye al clima que dejó en Estados Unidos la matanza de Columbine, pero no hay ninguna confirmación oficial.",
    ]},
    {"id": "s12", "frases": [
        "[curious] Número doce. El Expansion Pak de Donkey Kong 64.",
        "Donkey Kong 64 es uno de los dos únicos juegos que lo exigían, y venía gratis en las primeras copias.",
        "[mysterious] El programador Chris Marlow contó que se usó para tapar un bug que colgaba el juego con la memoria normal.",
        "[amused] Suena perfecto. Pero Simon Craddick, otro ingeniero del equipo, dice que solo se usaba para la iluminación.",
        "Dos personas del mismo equipo, dos versiones. Y una historia que todo internet repite como si estuviera cerrada.",
    ]},
    {"id": "s11", "frases": [
        "[curious] Número once. El juego que Nintendo soltó.",
        "DMA Design, un estudio escocés, enseñó Body Harvest en 1995. Iba a estar entre los primeros juegos de la consola.",
        "[sarcastic] Nintendo lo vio demasiado violento, lo fue retrasando, y lo acabó soltando. Salió en 1998 con otras editoras.",
        "[impressed] Y mira lo que hacía: bajabas del personaje y te subías a los vehículos que encontraras, incluida una camioneta de helados.",
        "[mischievous] Ese estudio hoy se llama Rockstar North, y en 2001 hizo Grand Theft Auto III. Que uno llevara al otro es opinión de la prensa. Pero ponlos uno al lado del otro.",
    ]},
    {"id": "s10", "frases": [
        "[warm] Número diez. El reloj dentro del cartucho.",
        "Animal Crossing no empezó en GameCube. Empezó en Nintendo 64, solo en Japón, en abril de 2001, con el nombre de Dobutsu no Mori.",
        "[curious] Katsuya Eguchi lo diseñó para el 64DD, porque ese accesorio llevaba reloj interno.",
        "Cuando los planes del disco cambiaron, tuvieron que recortar contenido y meter un reloj en el propio cartucho.",
        "[warm] Así nació la idea de un pueblo que sigue viviendo aunque apagues la consola. Por culpa de un accesorio que no funcionó.",
    ]},
    {"id": "s09", "frases": [
        "[curious] Número nueve. Internet en la Nintendo 64.",
        "Sí, existió. El 64DD, ese accesorio de discos del que hablamos en el video de Ocarina of Time, salió en Japón en diciembre de 1999, con un servicio en línea: Randnet.",
        "[thoughtful] Costaba 2 500 yenes al mes, más la llamada. Tenía sitio para 100 000 personas. Y al cierre llegó a poco más de 15 000.",
        "El 28 de febrero de 2001 se apagó. Duró poco más de catorce meses, y el 64DD se quedó con diez discos.",
        "[mysterious] Parece un fracaso sin más. Pero de ese accesorio salieron tres de los secretos más grandes de esta lista.",
    ]},
    {"id": "s08", "frases": [
        "[impressed] Número ocho. Dos discos en un cartucho.",
        "Resident Evil 2 ocupaba dos CD en PlayStation. Y Angel Studios lo metió en un cartucho de 64 megabytes.",
        "[surprised] Nueve personas a tiempo completo, unos doce meses. Comprimieron hasta las cinemáticas, que nadie esperaba ver en esa consola.",
        "Digital Foundry lo llamó uno de los ports más ambiciosos de la historia.",
        "[sarcastic] Un milagro técnico. En Estados Unidos vendió poco más de 326 000 copias.",
    ]},
    {"id": "s07", "frases": [
        "[tense] Número siete. Los guantes de Mario Party.",
        "Mario Party tenía minijuegos que ganaba quien girara el stick más rápido.",
        "[curious] Y los niños descubrieron que, si lo girabas con la palma, ibas mucho más rápido. Con eso llegaron las ampollas y las quemaduras.",
        "[surprised] La fiscalía de Nueva York recibió unas 90 quejas. Y en el año 2000, Nintendo ofreció guantes acolchados sin dedos, hasta cuatro por familia.",
        "[sarcastic] Piénsalo. La consola que popularizó el stick analógico acabó repartiendo material de protección.",
    ]},
    {"id": "s06", "frases": [
        "[mischievous] Número seis. El Tetris que te toma el pulso.",
        "En noviembre de 1998 salió en Japón Tetris 64, con un accesorio rarísimo: el Bio Sensor, una pinza para la oreja enchufada al mando.",
        "[amused] En el modo Bio Tetris, la dificultad cambiaba con tu corazón. Si se te aceleraba el pulso, te llovían más piezas complicadas.",
        "[curious] Y había un modo al revés, que te castigaba por estar demasiado tranquilo.",
        "[impressed] En 2009, Nintendo anunció el Vitality Sensor de Wii, que nunca salió. Tetris 64 ya lo había hecho, y es el único juego que lo usó.",
    ]},
    {"id": "s05", "frases": [
        "[curious] Número cinco. Final Fantasy 64 nunca existió.",
        "Seguro la has visto. Una demo de Final Fantasy en 3D, con Terra, Locke y Shadow, que mucha gente recuerda como la prueba de que venía a Nintendo 64.",
        "[mischievous] Pero esa demo jamás corrió en una Nintendo 64.",
        "Era un experimento de Square, Final Fantasy VI: The Interactive CG Game, que se enseñó en SIGGRAPH, en Los Ángeles, en 1995. Corría en estaciones Silicon Graphics Onyx.",
        "[amused] El rumor de que era para Nintendo 64 lo lanzó la revista GameFan. Y ya no hubo quien lo parara. Square nunca anunció nada para esa consola.",
    ]},
    {"id": "s04", "frases": [
        "[thoughtful] Número cuatro. Por qué Final Fantasy VII se fue.",
        "Hironobu Sakaguchi quería cine en Final Fantasy VII. Y esas cinemáticas no cabían en un cartucho.",
        "Según contó en 2024, en cartucho habría pasado de los 10 000 yenes. Y fue con el presidente de Square a hablar con Yamauchi.",
        "[sad] Final Fantasy VII salió en tres discos, en PlayStation. Y Dragon Quest VII se fue detrás.",
        "[curious] Lo que pasó después lo cuentan de dos formas. En una, a Square le dijeron que no volviera nunca. En otra, Yamauchi lo aceptó sin más. Ninguna está cerrada.",
    ]},
    {"id": "s03", "frases": [
        "[soft] Número tres. El juego que murió al 60 por ciento.",
        "En Space World 1997, Shigesato Itoi enseñó EarthBound 64 para el 64DD. La saga iba a dar el salto al 3D.",
        "[thoughtful] El juego acabó pasando a cartucho. Y en agosto del año 2000, el propio Itoi anunció que se cancelaba. Iba por el 60 por ciento.",
        "[curious] Quien tomó la decisión fue Satoru Iwata. Quédate con ese nombre.",
        "Se rehízo en Game Boy Advance en 2006, como Mother 3.",
        "[amused] Y en 2021, un fan pagó 357 dólares por un CD con 25 segundos inéditos de aquel juego. Veinticinco segundos.",
    ]},
    {"id": "s02", "frases": [
        "[mischievous] Número dos. El juego que hicieron a espaldas del jefe.",
        "Mario Artist: Polygon Studio era un programa del 64DD para crear figuras en 3D. Y dentro tenía un modo raro: Sound Bomber, unos juegos que duraban segundos.",
        "[amused] Años después, varios empleados de Nintendo retomaron la idea y se pusieron a hacer microjuegos en secreto, sin decírselo a su jefe, apuntando ideas en notas Post-it.",
        "[impressed] Eso se convirtió en WarioWare. Y eligieron a Wario porque, según Yoshio Sakamoto, siempre anda haciendo tonterías.",
        "[warm] Una saga entera, nacida de un rincón de un accesorio que casi nadie compró.",
    ]},
    {"id": "s01", "frases": [
        "[soft] Número uno. Cuatro muñecos sin cara.",
        "Masahiro Sakurai, de HAL Laboratory, quería hacer un juego de peleas para cuatro personas. Y quien le programó el prototipo fue Satoru Iwata.",
        "[warm] Iwata llevaba otro proyecto que le ocupaba toda la semana. Así que lo programó él solo, en sus fines de semana.",
        "El prototipo se llamaba Dragon King: The Fighting Game. No tenía personajes de Nintendo. Solo cuatro figuras sin cara.",
        "[curious] Sakurai sabía que muchos juegos de peleas no se vendían. Así que propuso lo impensable: meter a Mario, Donkey Kong, Samus y Fox.",
        "Él mismo ha contado que a algunos directivos no les gustaba ver a sus personajes pegándose. Pero la demo los convenció.",
        "[impressed] Super Smash Bros. salió en enero de 1999, vendió 5,55 millones de copias, y es hoy una de las grandes sagas de Nintendo.",
        "[soft] Aquel programador de fin de semana acabó siendo presidente de Nintendo. Y en 2005, en una conferencia, se definió así.",
        "[warm] En mi tarjeta soy presidente de una empresa. En mi mente, soy desarrollador de juegos. Pero en mi corazón, soy un jugador.",
        "[sad] Satoru Iwata murió en julio de 2015, con 55 años.",
        "[soft] Y lo más grande que dejó la Nintendo 64 empezó así. Con un hombre programando en sus fines de semana, porque le encantaba.",
    ]},

    # ================================================================ CIERRE
    {"id": "cierre", "frases": [
        "[warm] Treinta años después, la Nintendo 64 sigue viva. El remake de Ocarina of Time ya está en Switch 2, y Donkey Kong 64 y Pilotwings 64 están en Switch Online.",
        "[warm] Y lo mejor sigue pasando en los comentarios. En el video de Majora's Mask, Antilopez Mexicanos escribió que el terrible destino nunca fue que cayera la luna.",
        "[amused] Y Riuma sueña con que Nintendo saque Majora's Mask para la generación actual, como el de Ocarina. Te leemos, igual que a todos, y nos sirve para mejorar.",
        "[playful] Ahora dime tú. ¿Cuál de estos treinta no conocías? Te leo abajo.",
        "[warm] Y si te gustó este viaje, suscríbete a Crónicas del gaming. Nos vemos en el siguiente video. Y ponte los guantes.",
    ]},
]
