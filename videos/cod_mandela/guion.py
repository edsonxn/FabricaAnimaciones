# -*- coding: utf-8 -*-
"""GUION de «Los 20 EFECTOS MANDELA más raros de Call of Duty» (motor SECUENCIA YT, Expediente 141, 3-nov-2026).
Plantilla: videos/cod_mw4_secretos/ (misma fórmula; solo cambia el tema). Investigación con fuentes: investigacion.md.
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo con corchetes; sin [whispers] ni [excited] (2-nov-2026).
REGLA DE ORO: cada frase nombra algo que SE VE (el clip real contra «lo que recuerdas»); si la voz nombra un sonido, se OYE
(«post» = la voz calla y suena el clip con ambiente_por). ESCENAS = una por puesto; los cortes salen de `beats`.
"""

TITULO = "Los 20 EFECTOS MANDELA más raros de Call of Duty"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Expediente 141: DAMIÁN de la biblioteca de ElevenLabs (elegida por el usuario el 2-nov-2026), por id en cualquier cuenta
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {"iLLeY": "Ílei"}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # el audio del juego solo donde la voz lo nombra (ambiente_por, tras `beats`)
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Call of Duty", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial de cada CoD (audio/ost/, armar_musica_ost.py), nunca Lyria

# Pausas con la voz callada («si la voz nombra un sonido, se oye», 31-oct-2026):
#   p17 «That's one less loose end» (Shepherd) · p14 «I think I saw his arm fly off» · p13 «The numbers, Mason» ·
#   p09 «115» de Elena Siegman · p05 los gritos de Foley a Ramírez · p03 el jingle de Juggernog · p01 «Bravo Six, going dark»
ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: tu memoria.",
        "En dos mil veintiuno, un jugador profesional juró que este letrero amarillo de Standoff era nuevo. Y miles le creyeron.",
        "La perk más famosa de Zombies tenía otro nombre, escrito en su propia botella.",
        "Medio internet pulsó F para presentar respetos. Y si jugabas en consola, nunca viste esa letra.",
        "Y el sargento Foley le gritó a Ramírez cientos de órdenes. Pero nunca la que todos citan.",
        "Veinte efectos Mandela de Call of Duty: cosas que recuerdas con total seguridad, y que el propio juego dice que nunca pasaron.",
        "Todo comprobado, con el juego en pantalla. Y el número uno es una frase del Capitán Price. [short pause] Una que juras haber oído jugando.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. El Pack-a-Punch del manicomio.",
        "Verrückt, el manicomio de World at War, de dos mil ocho. El mapa donde debutó Juggernog.",
        "Mucha gente recuerda haber mejorado sus armas ahí, en la sala de la luz. Pero en Verrückt no había Pack-a-Punch.",
        "La máquina llegó dos mapas después, en Der Riese, la fábrica de los teletransportadores. [deadpan] Si mejoraste un arma en el manicomio, no fue el juego. Fue tu cerebro, haciéndole Pack-a-Punch a tus recuerdos.",
        "Y la primera arma que todos metieron en esa máquina fue la Ray Gun, que salía convertida en la Porter's X2, de rayos rojos.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, la máquina de Double Tap de Origins.",
        "Origins, Black Ops 2, dos mil trece: la Primera Guerra Mundial, robots gigantes y barro hasta las rodillas.",
        "Seis generadores, cuatro bastones elementales, y robots gigantes que te pisan si te descuidas. Y muchos juran que compraban Double Tap en su máquina, junto a las demás. Esa máquina no existe en Origins.",
        "Double Tap solo salía de Der Wunderfizz, la máquina que te da una perk al azar. Y la confusión tiene culpable: en Revelations, de Black Ops 3, hay una zona que imita a Origins. Y ahí sí hay máquina de Double Tap.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. Las dos cajas del faro.",
        "Call of the Dead, el mapa de George Romero, con un barco encallado en el hielo y un faro al fondo.",
        "Hay quien recuerda dos cajas misteriosas juntas, arriba del faro. Arriba hay una sola.",
        "La otra está cerca, en la zona del faro, encima de PhD Flopper. Dos cajas a pocos metros, y tu memoria las metió en el mismo cuarto.",
        "Y en ese mapa hasta los personajes eran actores de verdad: Sarah Michelle Gellar, Danny Trejo, Michael Rooker y Robert Englund.",
    ]},
    {"id": "p17", "post": 4.8, "frases": [
        "En el diecisiete, ¿quién mató a Ghost?",
        "Modern Warfare 2, dos mil nueve, misión Cabos sueltos. Ghost y Roach llegan a la pista, heridos, con el disco duro de Makárov.",
        "La respuesta rápida es Makárov. Y no. El que dispara es el general Shepherd, su propio comandante. Y lo dice así.",
    ]},
    {"id": "p17b", "frases": [
        "Un cabo suelto menos. Los rocían con gasolina y les prenden fuego. [short pause] Y el traidor era el mismo que daba las órdenes.",
        "Price y Soap lo persiguen hasta Afganistán. Y es Soap quien acaba clavándole un cuchillo en el ojo.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. Zombies en la Wii.",
        "Muchos recuerdan jugar Nacht der Untoten en la Wii, apuntando a la pantalla con el mando.",
        "Pero World at War de Wii no tenía modo Zombies. Ni Nacht, ni ningún otro mapa.",
        "Los zombis llegaron a la Wii con Black Ops, en dos mil diez, con Kino der Toten, el teatro nazi, y el mando de la Wii como pistola. [deadpan] El mando era el mismo. El juego, no.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, el logro que nunca te dieron.",
        "Shadows of Evil, Black Ops 3, dos mil quince: una ciudad de los años cuarenta, cuatro desconocidos y el Hombre Sombra.",
        "El mago Nero, la bailarina Jessica, el detective Jack y el boxeador Floyd, en una ciudad infestada de monstruos.",
        "Casi todos los mapas premian el Easter egg principal con un logro. Y muchos recuerdan haber ganado el de este.",
        "No existe. El logro El principio del fin te lo dan a mitad de camino, al completar los rituales. Terminar el Easter egg entero da experiencia y una tarjeta de visita. Y nada más.",
    ]},
    {"id": "p14", "post": 3.0, "frases": [
        "Número catorce. El brazo de Zakhaev.",
        "CoD 4, dos mil siete, Prípiat. El teniente Price, joven y camuflado, dispara el tiro más famoso de la saga contra Imran Zakhaev.",
        "Con un Barrett del calibre cincuenta, a más de un kilómetro, MacMillan te pide corregir por el viento y hasta por el efecto Coriolis. Si crees que ahí murió, el propio juego te corrige en ese momento. Escucha a MacMillan.",
    ]},
    {"id": "p14b", "frases": [
        "Le vuela el brazo. Zakhaev sobrevive quince años, con una prótesis.",
        "Y al final, en el puente, no lo mata Price. Price, herido en el suelo, le desliza su pistola a Soap. Y es Soap quien lo remata.",
    ]},
    {"id": "p13", "post": 3.5, "frases": [
        "En el trece, ¿quién pregunta por los números?",
        "Black Ops, dos mil diez. Alex Mason, atado a una silla, en un cuarto lleno de pantallas. Y una voz que no deja de preguntar.",
    ]},
    {"id": "p13b", "frases": [
        "Mucha gente pone esa frase en boca de Reznov, o de Dragovich. Pero es la voz del interrogador.",
        "Y al final descubres quién es: Jason Hudson, de la CIA, con Weaver al lado. Los números los transmitía Dragovich. [short pause] El que los pedía era de tu propio bando.",
        "Y ya que estamos: Reznov, el que te acompaña media campaña, murió en la fuga de Vorkutá. Todo lo demás, estaba en tu cabeza.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Black Ops 2 no inventó los finales.",
        "Black Ops 2 se recuerda como el primer Call of Duty con decisiones que cambian la historia. Pero cuatro años antes, World at War ya te obligaba a elegir.",
        "Okinawa, el castillo de Shuri, misión Breaking Point. Unos soldados japoneses fingen rendirse y se lanzan sobre Roebuck y Polonsky. Solo puedes salvar a uno.",
        "[sighs] El que no salvas, muere. Sin cinemática que lo arregle.",
        "Y un detalle cruel: al terminar el nivel, las chapas que te dan son las de Roebuck. Aunque lo hayas salvado.",
    ]},
    {"id": "p11", "frases": [
        "En el once, las misiones perdidas de World at War.",
        "Hay jugadores que recuerdan misiones de World at War que no salen en ningún video de la campaña. Un entrenamiento disparando a muñecos. Un tramo en tren.",
        "No están locos. Jugaron otro juego. En PlayStation 2 salió World at War: Final Fronts, con su propia campaña y sus propias misiones. Lo hizo otro estudio, Rebellion, y salió el mismo año, en dos mil ocho.",
        "Mismo nombre, misma guerra, otra campaña entera. [deadpan] El efecto Mandela con mejor coartada de toda la lista.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. Las botas doradas.",
        "Volvemos al barro de Origins. Con la pala puedes cavar montones de tierra y sacar de todo: armas, potenciadores, y premios dorados.",
        "Muchos recuerdan unas botas doradas para correr por el lodo. No existen. Lo único dorado que sale es la pala dorada, y el casco dorado. La pala se gana a fuerza de cavar. Y con ella, si tienes suerte, sale el casco.",
        "[deadpan] Para el barro, lo que había era Stamin-Up. Y paciencia.",
    ]},
    {"id": "p09", "post": 6.0, "frases": [
        "En el nueve, Evanescence en Zombies.",
        "Hay quien recuerda que Bring Me to Life sonaba como Easter egg en Kino der Toten, o en algún mapa de Black Ops.",
        "Nunca estuvo. Ni en un mapa, ni en un tráiler. Venía de los montajes de YouTube de dos mil diez, que la ponían encima de las partidas.",
        "La canción real de Kino der Toten es esta. Ciento quince, de Elena Siegman.",
    ]},
    {"id": "p08", "frases": [
        "Número ocho. Menéndez en llamas.",
        "Black Ops 2, el final malo. Raúl Menéndez, el villano, llega a la tumba de su hermana Josefina.",
        "Mucha gente recuerda verlo arder, retorciéndose sobre la tumba, con el cementerio entero en llamas.",
        "Se prende fuego, sí. Pero la imagen corta a negro. Se oye, y no se ve. La escena gráfica que recuerdas, tu cabeza la rellenó sola.",
    ]},
    {"id": "p07", "frases": [
        "En el siete, la perk gratis de la Luna.",
        "Moon, el último mapa de Black Ops, de dos mil once. En el biodomo hay plataformas de salto.",
        "Muchos juran que, si saltabas perfecto, te tocaba una perk gratis. No hay nada de eso: ni en el mapa, ni en las guías, ni en el código.",
        "Lo más probable es la QED, la granada cuántica, que a veces suelta una perk al azar. Y tu memoria se la regaló a las plataformas.",
        "Lo que sí es real en Moon: al final del Easter egg, tres misiles salen disparados hacia la Tierra. [short pause] Y le dan.",
    ]},
    {"id": "p06", "frases": [
        "Número seis. Mira bien la portada.",
        "La portada de Black Ops 2: un soldado en la sombra, con una pistola junto a la cara.",
        "Ahora mira abajo. En la otra mano, casi tapado por la oscuridad, lleva un cuchillo. Casi nadie lo recuerda.",
        "Y la de Black Ops, la de dos mil diez: el soldado no lleva una pistola. Lleva dos, una en cada mano.",
    ]},
    {"id": "p05", "post": 8.5, "frases": [
        "En el cinco: ¡Ramírez, haz de todo!",
        "Modern Warfare 2, la invasión de Virginia, en Burger Town. El sargento Foley no deja de darle órdenes al soldado Ramírez. Escucha.",
    ]},
    {"id": "p05b", "frases": [
        "Órdenes, una tras otra. Pero Ramírez, haz de todo, no la dice nunca.",
        "Nació en noviembre de dos mil nueve, en un meme de internet, el mismo mes que salió el juego.",
        "[deadpan] Y diecisiete años después, sigue siendo la orden más famosa de toda la saga. Una orden que nadie dio.",
    ]},
    {"id": "p04", "frases": [
        "Número cuatro. Pulsa F.",
        "Advanced Warfare, dos mil catorce. El funeral del soldado Will Irons. Y el letrero que se volvió meme: Press F to pay respects.",
        "Medio internet pulsó F. Pero esa F solo salía en PC. En PlayStation y Xbox el letrero decía otra cosa: mantén el botón para presentar respetos.",
        "O sea: millones de jugadores de consola recuerdan una tecla que nunca vieron. [short pause] F.",
    ]},
    {"id": "p03", "post": 5.0, "frases": [
        "En el tres, la botella de Juggernog.",
        "La perk más famosa de Zombies: más vida, por dos mil quinientos puntos. Y con su propia canción.",
    ]},
    {"id": "p03b", "frases": [
        "En la máquina dice Jugger-Nog. Pero el logo de World at War y la etiqueta de las botellas de Black Ops decían otra cosa: Juggernaut Soda.",
        "En Black Ops 2 la corrigieron, y desde entonces la etiqueta dice Jugger-Nog: con ene, o, ge. [deadpan] La bebiste cientos de veces. Y nunca leíste la etiqueta.",
    ]},
    {"id": "p02", "frases": [
        "Número dos. El letrero de Standoff.",
        "Julio de dos mil veintiuno. Standoff, el mapa de Black Ops 2, ya está en Cold War. Llega una actualización, y un jugador profesional, iLLeY, publica: no puedo creer que acaban de poner este letrero.",
        "Miles le dieron la razón. Juraban que en Black Ops 2 ese letrero amarillo no existía.",
        "Pero este es un video de Standoff subido en dos mil quince. Seis años antes. Y ahí está el letrero, en su poste.",
        "El mapa de Cold War salió sin él, y una actualización lo devolvió. [deadpan] El letrero no era nuevo. Lo nuevo era que por fin lo mirabas.",
    ]},
    {"id": "p01", "post": 4.5, "frases": [
        "Y el número uno. La frase de Price.",
        "Modern Warfare, dos mil diecinueve. Si hay una frase del Price moderno, es esta.",
    ]},
    {"id": "p01b", "frases": [
        "Bravo Seis, a oscuras. La recuerdas en la campaña, con las gafas de visión nocturna, entrando a la casa.",
        "Pero es del tráiler de presentación, de mayo de dos mil diecinueve. En la campaña, en la misión de la casa, Price solo dice: Bravo seis, al primer piso. Bravo seis, al segundo.",
        "Y en la misión que se llama, literalmente, Going Dark, tampoco está. Price solo dice que usarán la oscuridad para cubrirse.",
        "[short pause] La frase más famosa del Price moderno, nunca la dijo jugando. Solo en un tráiler.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. [short pause] Y ahora, la pregunta: ¿cuál de los veinte te hizo dudar de tu memoria? Dímelo en los comentarios. Yo apuesto por el letrero.",
        "En el canal ya tienes el expediente de los veinticinco secretos de Modern Warfare 4. Y si quieres el siguiente, suscríbete: aquí abrimos los archivos de Call of Duty que nadie te contó, en español. [short pause] Retírate, soldado.",
    ]},
]

# Nombres que Whisper escribe distinto (Juggernaug, The Rucht, Derise, The Abundafist, Shepard, Nachte und Toten, Zakaev, Borkutá,
# Roboc, stamina up, Sigman): la voz los dice bien; se aceptan con CER mayor.
CER_MAX_POR_FRASE = {k: 0.10 for k in ("p20_1", "p20_2", "p20_3", "p19_3", "p17_2", "p16_1", "p14_0", "p14_1", "p14b_0", "p13b_2",
                                         "p12_4", "p10_3", "p09_3", "p05b_2", "p03_0", "p03b_0", "p03b_1")}
