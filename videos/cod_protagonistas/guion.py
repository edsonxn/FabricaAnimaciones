# -*- coding: utf-8 -*-
"""GUION de «Cómo acabó REALMENTE cada protagonista de Call of Duty» (motor SECUENCIA YT, Expediente 141, 24-nov-2026).
Plantilla: videos/cod_mandela_zombies/ y videos/cod_villanos/ (misma fórmula; eje personajes). Investigación: investigacion.md
(subagente, wiki de CoD por su API, 24-nov). Lo de MW4/BO6/BO7 confirmado con títulos de clips de YouTube (24-nov).
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo, PLANA (queja justa de @v5x777: nada de voz «frustrada»).
REGLA DE ORO: cada frase nombra algo que SE VE; si la voz nombra un sonido, se OYE («post» = la voz calla y suena el clip).
VIOLENCIA: toda ejecución se corta ANTES del disparo/golpe (investigacion.md marca el punto de cada una).
"""

TITULO = "Cómo acabó REALMENTE cada protagonista de Call of Duty"   # 54 caracteres (24-nov)
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "sigh", "annoy", "frustr"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
FONETICA = {}
# Whisper escribe distinto los nombres (Shepard, gas, Kingan, The Ghosts, Belle, McTavish, Jdad…; hyp en voz/eval.json, 24-nov)
CER_MAX_POR_FRASE = {k: 0.08 for k in "p19_0 p19_4 p11_1 p11_2 p11b_0 p09_0 p08_0 p06_0 p03b_0 p03b_2 p02_0 p02b_1 p01_2 cierre_1".split()}
TAIL_MAX_POR_FRASE = {"intro_1": 1.1}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Call of Duty", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = None   # OST oficial (audio/ost/_catalogo.txt), nunca Lyria

# Pausas con la voz callada («si la voz nombra un sonido, se oye»; cortes medidos con _citas.py): p11 Shepherd «one less loose end» ·
#   p09 Reznov «For you, Mason… not for me» · p08 Soap «Makarov… knows… Yuri» · p06 Adler «it was never personal» · p03 Gaz «There is a
#   line…» · p02 Ghost/Price en el funeral de Soap · p01 Price «Gaz was right… Hold the line»
# Comentarios (≤ 10 días, ninguno repetido): @Keengan12239 p19 · @andreshico1220 tras p16 (contraburla) · @TMPLR5 p10 ·
#   @HdadDelJubileoensuEsperanza antes del p03 (contraburla) · @itsmaibel7486 p01 · @v5x777cod_rdr_fan0 en el cierre
ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: los protagonistas.",
        "El capitán Price, el sargento Soap, Gaz y el teniente Ghost. El agente Mason, el sargento Woods y el viejo Reznov. Los manejaste a todos. Les salvaste la vida cien veces.",
        "Y casi ninguno terminó como crees. Uno estaba muerto desde la segunda misión. Otro murió de viejo, con ciento cuatro años. Y al capitán Price lo mataron este mismo año.",
    ]},
    {"id": "intro_b", "frases": [
        "Revisé el destino de cada uno, juego por juego, con la escena en pantalla. Aviso: hay spoilers de Modern Warfare 4 y de Black Ops 7.",
        "Veinte protagonistas de Call of Duty, y cómo acabó realmente cada uno. Empezamos por el que llegó más lejos: al espacio.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. Nick Reyes, Infinite Warfare.",
        "Capitán de la nave Retribution, y el personaje jugable de mayor rango de toda la saga.",
        "En la última operación, sobre Marte, se queda dentro del astillero enemigo, y le ordena a Salter que dispare de todos modos.",
        "Sale despedido al vacío. Ve explotar el astillero. Y tres trozos de metralla le van rompiendo el visor del casco, hasta que la pantalla se va a negro.",
        "[deadpan] Antes ya se había salvado dos veces: en la Luna, y a la deriva sobre Titán. A la tercera, nadie fue a buscarlo.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, Logan Walker, de Ghosts.",
        "El final: un tren que cae al agua, una sola bala, y Rorke en el suelo. Logan saca a su hermano Hesh a la orilla. Empiezan los créditos.",
        "Y la escena vuelve. Rorke está vivo, le rompe el brazo a Logan y se lo lleva arrastrando. Logan despierta en un pozo, bajo la lluvia.",
        "Han pasado trece años. No hubo secuela. Logan sigue en ese pozo.",
        "Keengan lo dijo así: que Rorke era muy buen villano, y quedó en el olvido por el hype de Modern Warfare 4. [short pause] Rorke ganó. Y ni siquiera le dieron el crédito.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. Alex Keller, el agente de la CIA de Modern Warfare dos mil diecinueve.",
        "En la fábrica de Barkov, en Georgia, el detonador se rompe. Alex le pide la orden a Farah, y entra solo a volar el horno.",
        "Todos lo dieron por muerto. No lo estaba.",
        "Sobrevivió a la explosión sin la pierna izquierda, pasó cinco meses escondido, y volvió con una prótesis. [deadpan] El sacrificio más heroico de la saga, y le costó una pierna.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, el sargento Paul Jackson, de Call of Duty 4.",
        "El helicóptero está en el aire cuando estalla la bomba nuclear. Despiertas entre los restos, sales arrastrándote, y caminas entre ruinas rojas, con el hongo al fondo.",
        "Te desplomas. Sin cinemática. Todo en primera persona.",
        "Pero en el código del juego quedaron tres objetivos cortados: buscar equipo contra la radiación, localizar al oficial al mando, y ponerte a cubierto. [short pause] Jackson iba a sobrevivir. Alguien decidió que no.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. El presidente Al-Fulani, la primera misión de Call of Duty 4.",
        "Lo controlas, pero no puedes hacer nada. Te llevan en el asiento de atrás de un coche, por una ciudad en pleno golpe de Estado, hasta un poste en un patio lleno de soldados.",
        "Y el que va de copiloto, dándole órdenes al chofer, es Victor Zakhaev, el hijo del villano, el mismo al que acorralan en una azotea misiones después.",
        "[deadpan] El primer protagonista del Modern Warfare original duró una misión, y la pasó sentado.",
    ]},
    {"id": "crit1", "frases": [
        "Antes del quince, un comentario. Andrés vio el expediente de Modern Warfare 4 y escribió: lo único que rescato es que Riley sí existe: el perro de una familia, en una misión encubierta.",
        "Gracias, Andrés. Es un buen dato. [short pause] Y de todo el expediente, lo único que se salvó fue el perro. Como en las películas.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Joseph Allen, el ranger de Modern Warfare 2.",
        "Entra encubierto con la banda de Makarov, con otro nombre, a la misión del aeropuerto.",
        "Al final, en el estacionamiento, Makarov le tiende la mano para subirlo a la ambulancia. Y ya sabía quién era.",
        "Makarov lo supo desde el principio. El cuerpo de un estadounidense en ese aeropuerto era justo el mensaje que necesitaba para empezar la guerra. [deadpan] Allen no fue el infiltrado. Fue la carta.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, Yuri, de Modern Warfare 3.",
        "En la misión Blood Brothers, con sus recuerdos, descubres que Yuri estuvo en todas partes: en Prípiat en mil novecientos noventa y seis, viendo la bomba nuclear desde lejos, y en el aeropuerto, intentando detener a Makarov.",
        "Muere en la última misión, en el hotel de Dubái. Atravesado por una barra de hierro, le grita a Price que lo deje y que no deje escapar a Makarov.",
        "Y aun así se levanta, y le dispara a Makarov justo cuando iba a matar a Price. [short pause] Le salvó la vida, y le costó la suya.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. Case, el protagonista de Black Ops 6.",
        "El final: el helicóptero de Jane Harrow cae al mar Negro. Case, con una voz en la cabeza que le dice que termine, pelea con ella bajo el agua. Corte a negro.",
        "Por la radio, Marshall grita que lo lograron. Y nadie dice qué pasó con Case.",
        "Lo responde Black Ops 7: diez años después, el villano recupera una muestra de sus restos. [deadpan] El final abierto se cerró con una muestra de laboratorio.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, David Mason, Section, de Black Ops 2 y Black Ops 7.",
        "El final bueno de Black Ops 2: Section deja su pistola frente a la tumba de su padre, y le dice a Woods que ya terminó.",
        "No terminó. En Black Ops 7 vuelve a mandar un equipo, en dos mil treinta y cinco. Y ese juego volvió oficial el final de Black Ops 2: Harper vivo, Karma viva, y Alex Mason muerto.",
        "Section sobrevive a todo. [short pause] Lo que no sobrevive es su familia. Ya lo verás en el número cinco.",
    ]},
    {"id": "p11", "post": 3.2, "frases": [
        "Número once. Roach y Ghost, los originales, de Modern Warfare 2.",
        "Roach acaba de cargar el disco con la información de Makarov. Ghost lo arrastra, herido, hasta el helicóptero del general Shepherd. Shepherd le pregunta si lo tienen.",
        "Ghost dice que sí. Escucha lo que contesta Shepherd.",
    ]},
    {"id": "p11b", "frases": [
        "Un cabo suelto menos. Un disparo, una zanja, gasolina, y el puro de Shepherd.",
        "En el remaster agregaron dos detalles: Ghost mira a Roach confundido, y Roach intenta agarrarle la muñeca a Shepherd. [deadpan] Lo que nunca le dieron a Roach fue voz: su único grito en todo el juego es si te caes de un acantilado.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, el otro Ghost: el del reinicio.",
        "Modern Warfare dos mil diecinueve, Modern Warfare 2, 3 y 4. Y al final de Modern Warfare 4, es el único de la fuerza ciento cuarenta y uno que sigue vivo.",
        "TMPLR5 lo vio venir: escribió que, como Ghost quedó vivo, seguramente iba a dirigir su propio equipo. [short pause] Casi. Al final de Modern Warfare 4, Laswell borra su expediente. Oficialmente, Ghost ya no existe.",
        "[deadpan] De la fuerza ciento cuarenta y uno, el que nunca enseñó la cara es el único que sigue de pie.",
    ]},
    {"id": "p09", "post": 3.3, "frases": [
        "Número nueve. Viktor Reznov, de World at War y Black Ops.",
        "Vorkuta, mil novecientos sesenta y tres. La fuga de la prisión. Reznov se queda atrás para que Mason pueda subir al tren. Escucha su despedida.",
    ]},
    {"id": "p09b", "frases": [
        "Muere en Vorkuta. Y todo el Reznov que acompaña a Mason después, en Vietnam, en la isla Rebirth, nunca estuvo ahí.",
        "Era una alucinación del condicionamiento. Hudson se lo dice a Mason en el interrogatorio: Reznov llevaba cinco años muerto.",
        "[deadpan] Y aun así se vengó de Dragovich, de Kravchenko y de Steiner. Muerto, y a través de otro.",
    ]},
    {"id": "p08", "post": 5.4, "frases": [
        "En el ocho, John Soap MacTavish. El original.",
        "Mataste a Zakhaev con él en Call of Duty 4, y sobreviviste a un cuchillo en el pecho en Modern Warfare 2.",
        "En Modern Warfare 3, en Praga, Makarov vuela el edificio donde estaba de francotirador. Soap empuja a Yuri por un hueco para salvarlo. Lo tienden sobre una mesa, y Price le pide que aguante. Estas son sus últimas palabras.",
    ]},
    {"id": "p08b", "frases": [
        "Makarov sabe. Yuri. Y muere.",
        "Price le deja sobre el pecho la misma pistola M1911 con la que Soap mató a Zakhaev. [short pause] Solo lo controlaste en la primera misión de Modern Warfare 3. El resto, solo pudiste verlo morir.",
    ]},
    {"id": "p07", "frases": [
        "Número siete. Frank Woods.",
        "Murió tres veces. En Black Ops 1 se lanza por una ventana con Kravchenko y un cinturón de granadas. Sobrevive.",
        "En Black Ops 2, en un final, Menéndez lo mata. En Cold War, en otro, lo ejecuta Bell. Ninguna de las dos cuenta.",
        "Black Ops 7 cerró la cuenta: Woods murió en dos mil treinta y cuatro, de viejo, con ciento cuatro años, y está enterrado en Arlington. [deadpan] Sobrevivió a Vietnam, a Kravchenko, a Menéndez y a Bell. Lo único que lo pudo matar fue el calendario.",
    ]},
    {"id": "p06", "post": 2.6, "frases": [
        "En el seis, Bell, el protagonista de Black Ops Cold War.",
        "Lo creas tú: nombre, origen, todo. Y al final eliges. Si dices la verdad, salvas Europa, y Adler te lleva a un acantilado.",
        "Los dos sacan la pistola, cámara lenta, y todo se va a negro antes del disparo. Antes, Adler le dice esto.",
    ]},
    {"id": "p06b", "frases": [
        "En el juego nunca se sabe quién disparó. En dos mil veinticuatro, Treyarch lo dijo en su podcast oficial: disparó Adler primero.",
        "[deadpan] Elegiste el final bueno. El final bueno también te mata.",
    ]},
    {"id": "p05", "frases": [
        "Número cinco. Alex Mason.",
        "Black Ops 2, Panamá, mil novecientos ochenta y nueve. Juegas como Woods. Noriega te entrega a un hombre con una bolsa en la cabeza, y Hudson te ordena dispararle.",
        "Tú decides dónde apuntar. Woods le quita la bolsa, y es Mason.",
        "El juego te dejaba salvarlo. Pero en dos mil veinticuatro, Treyarch eligió: Mason está muerto. Lo mató Woods. Y Hudson, también muerto.",
        "[deadpan] Durante años, Woods le dijo a David que a su padre lo había matado un vagabundo.",
    ]},
    {"id": "p04", "frases": [
        "En el cuatro, el protagonista de Black Ops 3. El que no tiene nombre.",
        "En la segunda misión te operan para ponerte implantes. Falla el soporte vital, y mueres en la camilla. Taylor se conecta a tu cerebro, y tu conciencia pasa al suyo.",
        "Todo lo que juegas después es una simulación, hecha con los recuerdos de Taylor.",
        "Y en esa misma operación, el doctor dice que el paciente puede quedar con muerte cerebral. El protagonista contesta que de todos modos es hombre muerto. [short pause] Hablaba de sí mismo, y no lo sabía.",
        "Al final, en blanco y negro, un soldado le pregunta su nombre. Y responde: Taylor.",
    ]},
    {"id": "crit2", "frases": [
        "Antes del tres, un comentario del expediente de los villanos. Tres palabras: ¿y Archer?",
        "Es el reporte más corto que ha llegado a este canal, y el más justo. Faltó. [short pause] Hoy sí sale. Y no le va a gustar cómo.",
    ]},
    {"id": "p03", "post": 4.2, "frases": [
        "Número tres. Gaz. Los dos.",
        "Modern Warfare 4, Corea del Norte. Price, Ghost y Gaz, atados a unas sillas. Gaz ya es capitán, y le reprocha a Price haberse vuelto un fugitivo. Escucha lo que le dice.",
    ]},
    {"id": "p03b", "frases": [
        "Entra el Archer, el ministro ruso, el padre de Makarov. Se burla de Gaz, y pasa por detrás de su silla.",
        "Lo ejecuta delante de Price. Y el Gaz original, el de Call of Duty 4, murió igual: herido, desarmado, en el puente, a manos de Zakhaev.",
        "[deadpan] Dos Gaz, dos villanos, la misma muerte. Y en las dos, lo vengó Price.",
    ]},
    {"id": "p02", "post": 4.6, "frases": [
        "En el dos, Johnny Soap MacTavish. El del reinicio.",
        "Modern Warfare 3, dos mil veintitrés. El túnel bajo el canal de la Mancha. Soap, herido, sostiene la bomba y guía a Price para cortar los cables.",
        "Entra Makarov. Soap se levanta y le clava un cuchillo en el hombro. Makarov lo remata. Después, en las montañas de Escocia, Ghost esparce sus cenizas.",
    ]},
    {"id": "p02b", "frases": [
        "El reinicio mató a Soap. Murió salvando a Price.",
        "Y fue su muerte la que llevó a Price a matar a Shepherd en su propia oficina. [deadpan] La comunidad se lo tomó tan mal que un aspecto del juego dice: yo no estaba en ese túnel.",
    ]},
    {"id": "p01", "post": 8.0, "frases": [
        "Y el número uno. El capitán John Price.",
        "Modern Warfare 4, la última misión. Price va preso en un convoy con el Archer. Ghost lo embosca, el camión choca, y una varilla de acero le atraviesa el abdomen.",
        "Herido, persigue al Archer por un bosque nevado, hasta un lago helado. Y ahí acaba con él, con la misma varilla. El Archer, el que preguntaba Hdad.",
        "Llega Ghost. Le pregunta si valió la pena. Escucha lo que contesta Price.",
    ]},
    {"id": "p01b", "frases": [
        "Gaz tenía razón. Hay que mantener la línea. Ghost le toma la mano, y le cierra los ojos.",
        "Y a mitad de los créditos, Laswell borra los expedientes de Gaz, de Ghost y de Price. Bienvenidos al programa Watcher.",
        "Maibel lo notó: Watcher 2 es la que da las órdenes en el modo DMZ, sin nombre, solo con su cara. [short pause] El programa sigue. Price, no.",
        "Y hay tres Price en la saga. El de la Segunda Guerra Mundial murió en el primer Call of Duty, en un acorazado alemán. El del reinicio, en un lago helado. [deadpan] El único que sobrevive es el del puro. El de dos mil siete.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. Veinte protagonistas, y la mayoría no salió viva.",
        "Gracias a Keengan, a TMPLR5, a Maibel, a Andrés y a Hdad por los datos de este expediente. Y v5x777 votó que se quede el intruso: el voto está anotado, y la votación sigue abierta.",
        "Ahora te toca a ti: ¿qué protagonista crees que merecía otro final? Escríbelo. Los mejores comentarios salen en el siguiente expediente.",
        "Y si te gustó, en el canal tienes cómo murió cada villano. Suscríbete. [short pause] Retírate, soldado.",
    ]},
]
