# -*- coding: utf-8 -*-
"""GUION de «Los 20 EFECTOS MANDELA de los Zombies de Call of Duty» (motor SECUENCIA YT, Expediente 141, 22-nov-2026).
Plantilla: videos/cod_mandela3/ (misma fórmula). Investigación: investigacion.md (subagente, 22-nov).
Voz: DAMIÁN de ElevenLabs (BPwS5yO6aXvwg8auqNwS), eleven_v4_turbo, PLANA (queja justa de @v5x777: nada de voz «frustrada»).
REGLA DE ORO: cada frase nombra algo que SE VE; si la voz nombra un sonido, se OYE («post» = la voz calla y suena el clip).
"""

TITULO = "Los 20 EFECTOS MANDELA de los Zombies de Call of Duty"   # provisional (22-nov)
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="BPwS5yO6aXvwg8auqNwS", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "sigh", "annoy", "frustr"),
           referencia=r"C:\FabricaAnimaciones\canales\voces_prueba\cod_mw4\s0_damian.mp3")
FONETICA = {}
# Nombres alemanes con sonido alemán, no francés (crítica de @v5x777 en cod_mandela2; no se vuelve a enseñar ni a mencionar)
FONETICA.update({"Nacht der Untoten": "Najt der Úntoten", "Kino der Toten": "Kíno der Tóten", "Verrückt": "Ferrúkt",
                 "Der Riese": "Der Ríse", "Der Eisendrache": "Der Áisendraje", "Wunderwaffe": "Vúnderváfe",
                 "Richtofen": "Ríjtofen", "Die Maschine": "Di Maschíne"})
# Whisper escribe distinto los nombres (zombies, Ferruct, Jabbernog, Neicht, Thundercat, Transit, Cabús, Hekkune…; hyp en voz/eval.json, 22-nov)
CER_MAX_POR_FRASE = {k: 0.08 for k in """intro_0 intro_b_1 p19_0 p18_0 p17_0 p17_2 p17_3 p14_1 p11_2 gracias1_0 p10_0 p10_2 p10_3 p08_0
    p08_1 p07_0 p07_1 crit2_1 p05_0 p05_1 p05_3 p04_3 p03_2 p03_3 p02_0 p01_1 cierre_0 cierre_1""".split()}
TAIL_MAX_POR_FRASE = {"p05_3": 1.1, "p03_2": 1.1, "p03_3": 1.1}

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

# Pausas con la voz callada («si la voz nombra un sonido, se oye»): p20 Nixon «Oh my God!» · p19 Nikolai «Some things are
#   forgotten… for a reason!» · p01 el temblor y la voz al revés de las estatuas (cortes medidos con _citas.py)
# Canciones con derechos (Shepherd of Fire, Owner of a Lonely Heart) FUERA: no se pueden oír (Content ID) → suplentes Type 100 y Quick Revive
# Comentarios (≤ 10 días, ninguno repetido): @SargentoCaboose p01 · @estebancastillo67532 p03 · @eltiorandomml8930 tras p16 (contraburla) ·
#   @ryuzakiletrasymas115 tras p07 (contraburla) · @markitos453 y @rafaeltroconis6615 tras p11 · @Heckgüne17, @AholicChaffyGRS y
#   @SargentoCaboose («Sub 106») en el cierre
ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] Expediente ciento cuarenta y uno. Asunto: tu memoria. Esta vez, en los zombis.",
        "Uno de ustedes me escribió que usó la Ray Gun en la campaña de World at War. Otro, que la Thundergun salía en una misión de Black Ops. A los dos les dijeron que estaban locos.",
        "Y todos crecimos con la misma regla: si caes, no te arrastres, que te desangras más rápido.",
    ]},
    {"id": "intro_b", "frases": [
        "Lo revisé todo, con el juego en pantalla, y hasta con su código. Hay un puente que sí se rompe, un arma que nunca existió, y una pistola de rayos que casi le cuesta el trabajo a quien la escondió.",
        "Veinte efectos Mandela de los zombis de Call of Duty. Y el número uno te lo mandó un suscriptor.",
    ]},
    {"id": "p20", "post": 3.3, "frases": [
        "Número veinte. Nixon, convertido en zombi.",
        "Black Ops, el mapa Five, el Pentágono. La intro en blanco y negro: Kennedy, Castro, McNamara y Nixon, encerrados en una sala, mientras se oyen ruidos afuera.",
        "Hay quien recuerda que Nixon se transformaba ahí mismo, delante de los otros tres. Escucha cómo termina en realidad.",
    ]},
    {"id": "p20b", "frases": [
        "Nixon grita, y se desmaya del susto. Nadie se transforma. [short pause] Un segundo después sale de la armería con dos escopetas, igual que los demás.",
        "[deadpan] Nixon no se convirtió en zombi. Solo se desmayó en el momento más dramático de su vida.",
    ]},
    {"id": "p19", "post": 6.0, "frases": [
        "En el diecinueve, las últimas palabras de Nikolai.",
        "Black Ops 3, el final de Gorod Krovi. El Nikolai de los cuatro originales, frente al grupo nuevo, con su propio Nikolai joven.",
        "Hay quien jura que gritaba «tenías que ser tú». La frase real es esta.",
    ]},
    {"id": "p19b", "frases": [
        "Algunas cosas se olvidan, por una razón. [short pause] Y tu memoria se lo tomó al pie de la letra: olvidó hasta la frase.",
    ]},
    {"id": "p18", "frases": [
        "Número dieciocho. El mapa de zombis en llamas.",
        "Alguien recuerda un mapa de zombis de Black Ops 1 dentro de un edificio que ardía: ventanas rotas, muros derrumbados, fuego por todas partes. No lo encuentra en ninguna lista.",
        "No lo va a encontrar. Ningún mapa de zombis de Black Ops 1 es así. Lo más parecido es una misión de la campaña: The Defector, la ciudad de Hue, mil novecientos sesenta y ocho.",
        "Mason y Woods entran rompiendo una ventana, y todo arde alrededor. [deadpan] Había fuego, había ventanas, y había gente queriendo matarte. Solo que eran vietnamitas, no zombis.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, el zombi misterioso de Verrückt.",
        "En World at War, en el manicomio alemán. Hay quien recuerda, de niño, un zombi especial que lo seguía por todo el mapa haciendo ruidos raros.",
        "No existe ningún zombi especial. Lo que tiene Verrückt son sonidos que se disparan según dónde estés. Si activas la silla del dentista, suena un taladro, y un paciente que grita.",
        "Y sus zombis son más rápidos y más listos que los del primer mapa. [short pause] No te seguía un zombi especial. Te seguían todos, y más rápido.",
    ]},
    {"id": "p16", "frases": [
        "Número dieciséis. La escopeta del banco de Town.",
        "Black Ops 2, Town. Un jugador recordaba una Remington ochocientos setenta colgada en la pared del banco. Se dio cuenta de que no estaba en una partida sin la caja misteriosa.",
        "El banco de Town no tiene ni un arma. Solo una máquina: Speed Cola.",
        "La Remington sí existe, pero en TranZit: en el granero de la Granja, y fuera de la estación de autobuses. [deadpan] La escopeta era real. El banco, no tanto.",
    ]},
    {"id": "crit1", "frases": [
        "Antes del quince, una pausa. En el primer expediente, alguien dejó esto: que el top lo armó una inteligencia artificial que alucinó, y que seguramente ni he jugado un Call of Duty.",
        "Gracias por el reporte. Por eso este expediente trae el clip del juego en cada efecto: la estatua, el arma, el código. [short pause] La memoria se puede discutir. El clip, no.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. Quick Revive, dos a la vez.",
        "Black Ops 1, jugando solo. La máquina azul de Quick Revive, que en solitario te levanta tú mismo. Un jugador recuerda haber tenido dos Quick Revive a la vez.",
        "Nunca fueron dos a la vez. En solitario se compra hasta tres veces, una por una. Y a la tercera, la máquina desaparece del mapa.",
        "[deadpan] Tres vidas, una detrás de otra. Tu memoria las juntó en una sola compra.",
    ]},
    {"id": "p14", "frases": [
        "En el catorce, el subfusil japonés de World at War.",
        "Un jugador recordaba una Type 100 en los zombis de World at War, y le dijeron que estaba loco.",
        "No lo estaba. La Type 100 se compra en la pared, y sale en la caja, en dos mapas: Shi No Numa, el pantano japonés, y Der Riese, la fábrica.",
        "[short pause] Esta vez el loco era el que lo corrigió.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. El escudo de Richtofen.",
        "En el mapa Origins, de Black Ops 2. En las partidas con amigos alguien siempre gritaba: que no construyeras tú el escudo, que lo armara Richtofen, porque el suyo aguantaba más.",
        "Es un mito de patio de recreo. El escudo es el mismo, lo construya quien lo construya. Lo único que cambia es la animación.",
        "[deadpan] Richtofen sabía muchas cosas. Construir escudos especiales no era una de ellas.",
    ]},
    {"id": "p12", "frases": [
        "En el doce, un recuerdo que es correcto: la Thundergun no mataba siempre.",
        "El cañón de aire de Kino der Toten. Hay quien recuerda que no tenía daño infinito, y que algunos zombis salían volando y se levantaban.",
        "Tiene razón. De cerca, el impacto directo mata siempre. Pero de media y larga distancia solo hace quince de daño: los tumba, y a los pocos segundos se levantan.",
        "Guárdala en la memoria. La Thundergun vuelve en el número tres, en un lugar donde no debería estar.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Tirarte al suelo frente a las máquinas.",
        "Unos juran que en Black Ops 1 y 2 te daban puntos por tirarte cuerpo a tierra frente a las máquinas de perks. Otros, que eso llegó con Black Ops 3.",
        "Los dos tienen algo de razón. En los juegos viejos solo funcionaba en dos mapas, Der Riese y Origins, los de las máquinas antiguas: veinticinco puntos, como quien encuentra monedas debajo de una máquina.",
        "En Black Ops 3 y en Cold War pasó a todas las máquinas, y ya daba cien. [deadpan] La inflación también llegó a los zombis.",
    ]},
    {"id": "gracias1", "frases": [
        "Y aquí, dos comentarios que se agradecen. Markitos dice que estos videos le preocupan, porque desmentía los de Modern Warfare antes de la explicación. Eso es buena memoria, Markitos. Aquí te tocan los zombis.",
        "Y Rafael, el del final de Menéndez, volvió a escribir: que no creía que su recuerdo fuera tan interesante como para salir en un video. Lo era. Todos los comentarios se leen, y se toman en cuenta para el siguiente expediente.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. ¿Cuántos golpes aguantas con Juggernog?",
        "La máquina roja. Unos dicen que caes al cuarto golpe. Otros, que aguantas cinco. Otros, que caes al sexto. La discusión llegó a una guerra de ediciones en la wiki.",
        "Con Juggernog aguantas cuatro golpes de zombi, y caes con el quinto. Sin ella, caes mucho antes.",
        "Pero en Verrückt y Shi No Numa, la de World at War funcionaba distinto. Y en TranZit, con la mejora permanente, aguantabas hasta seis. [short pause] Los tres bandos jugaron partidas distintas.",
    ]},
    {"id": "p09", "frases": [
        "En el nueve, el filtro en blanco y negro.",
        "Un jugador recuerda que Moon empezaba en blanco y negro hasta que encendías la luz. Lo jugó el día del estreno con su hermana, y los dos lo recuerdan igual.",
        "Moon empieza a todo color. El mapa en blanco y negro es Ascension, el anterior, la base soviética de cohetes: todo gris hasta que das la luz.",
        "Y un detalle de Ascension: si tienes Quick Revive y caes, el sol sale en color. [deadpan] Dos personas, el mismo recuerdo, el mapa equivocado.",
    ]},
    {"id": "p08", "frases": [
        "Número ocho. El avión del primer mapa de zombis.",
        "La intro de los zombis de World at War. Mucha gente recuerda que empezaba con el avión cayendo, y después el soldado que despierta y ve al zombi correr hacia él.",
        "La intro no enseña ningún choque. Empieza con el avión ya destrozado, entre niebla y fuego, unas siluetas al fondo, y un zombi que corre hacia la cámara.",
        "El choque que recuerdas está en la campaña: el búnker de Nacht sale del aeródromo de la misión Hard Landing, y ahí sí ves caer un bombardero. [short pause] La historia oficial dice que el avión se estrelló. Solo que nunca te lo enseñaron.",
    ]},
    {"id": "p07", "frases": [
        "En el siete, Rebirth, el mapa de zombis de Black Ops 1.",
        "Alguien recuerda un mapa de zombis llamado Rebirth, que empezaba atado a la silla de las teles.",
        "Ese mapa no existe. Rebirth es una misión de la campaña de Black Ops 1: una isla en el mar de Aral, el gas Nova 6, enemigos con máscara.",
        "La silla sí es real: en el menú de Black Ops te puedes soltar y usar el ordenador. Ahí estaba Dead Ops Arcade.",
        "Y el giro: en dos mil veinticuatro sí hubo zombis en la isla de Rebirth, en Warzone, con Zombie Royale. [deadpan] Tu memoria no se equivocó. Solo se adelantó catorce años.",
    ]},
    {"id": "crit2", "frases": [
        "Otro comentario del primer expediente. Ryuzaki dice que lo de Advanced Warfare es una fumada, que nadie tuvo ese efecto Mandela, porque todos saben que la F era de PC.",
        "Tienes toda la razón, Ryuzaki. Todos lo sabían. [short pause] Por eso medio mundo en consola sigue escribiendo una F cuando muere alguien.",
    ]},
    {"id": "p06", "frases": [
        "Número seis. Tombstone, jugando solo en Town.",
        "Unos recuerdan comprar Tombstone en solitario, en Black Ops 2, y enojarse porque no servía para nada. Otros juran que en solitario ni aparece.",
        "Los dos tienen razón. En solitario no está disponible. Pero si empiezas una partida con más gente, y todos se van, te quedas solo con las reglas de solitario. Y la puedes comprar.",
        "Es tirar dos mil puntos: con las reglas de solitario, no hace nada. [deadpan] No la soñaste. La pagaste.",
    ]},
    {"id": "p05", "frases": [
        "En el cinco, la Thundergat.",
        "Mob of the Dead, Alcatraz. La Blundergat, el trabuco. Hay quien jura que tenía una tercera mejora, la Thundergat: morada en la punta, disparando rayos.",
        "Nunca existió. La Blundergat tiene la Sweeper con Pack a Punch, la Acid Gat verde con el kit de ácido, y en el mapa de Blood of the Dead, la Magmagat, que es de color naranja. Ninguna eléctrica.",
        "La explicación más votada: Electric Cherry. La Blundergat recarga a cada disparo, y cada recarga suelta chispas. [short pause] Viste rayos. Solo que salían de una perk.",
    ]},
    {"id": "p04", "frases": [
        "Número cuatro. La regla de oro: si caes, no te arrastres.",
        "«¡No te muevas, que te desangras más rápido!». Lo gritamos todos, en todas las partidas con amigos.",
        "Es falso, y está en el código del juego. En Black Ops 2, al caer, el juego toma un tiempo fijo, y le resta uno cada segundo. A la mitad cambia la vista, y en cero, mueres.",
        "En ninguna parte mira si te mueves. [short pause] Años quedándonos quietos, por nada.",
    ]},
    {"id": "p03", "frases": [
        "En el tres, la Thundergun en la campaña.",
        "Esteban lo recuerda así: la Thundergun salía en una misión de Black Ops 1. Y es verdad. Es un secreto de la misión Numbers, en Kowloon, Hong Kong.",
        "Disparas a seis bombonas blancas hasta que sale el gas rosa, el Nova 6. Sacas una cinta de un casete, y la metes en otro, en el escondite de armas de Clarke. Y ahí está, colgada en la pared.",
        "Y en la campaña se podía recargar a medio cargador, algo que en los zombis nunca se pudo. [short pause] Esteban, tu recuerdo es real. Y no es el único: falta la pistola de rayos.",
    ]},
    {"id": "p02", "frases": [
        "Número dos. El puente de TranZit.",
        "Black Ops 2. Alguien recuerda a su hermano jugando, hacia la ronda veinte: el autobús entra al puente, el puente se rompe, el autobús cae y mueren todos.",
        "Y hasta hay videos que lo desmienten diciendo que ese puente nunca se rompe. Los dos se equivocan a medias.",
        "El puente que une Town con la estación sí se derrumba: la primera vez que el autobús pasa por encima, se hunde. Pero el autobús sigue pasando por el tramo roto, y los escombros pueden tirar a quien vaya en el techo.",
        "[deadpan] El puente cayó. El autobús, nunca. Los que caían eran los del techo.",
    ]},
    {"id": "p01", "post": 3.5, "frases": [
        "Y el número uno. La Ray Gun en la campaña de World at War.",
        "Este lo mandó Sargento Caboose: recuerda usar la Ray Gun en la campaña de World at War, de dos mil ocho. Y es verdad.",
        "Misión Little Resistance, Peleliu, la playa. Después del bombardeo bajas a la arena y te paras en tres charcos, unos segundos en cada uno. Escucha.",
    ]},
    {"id": "p01b", "frases": [
        "Tiembla el suelo, y salen de la arena cuatro estatuas, perros león de Okinawa, cada una con una Ray Gun. Revienta un tanque con dos disparos.",
        "Esa voz rara es un mensaje de radio de un soldado japonés, puesto al revés. En dos mil dieciséis la comunidad lo dio la vuelta, y un jugador japonés lo tradujo.",
        "Y lo mejor: Jesse Snyder, de Treyarch, la escondió ahí sin consultar a nadie, y casi lo despiden por eso. [short pause] No te lo inventaste, Sargento. La escondió un tipo que casi pierde su trabajo por ti.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Expediente cerrado. Veinte efectos Mandela de los zombis, y los dos mejores me los dieron ustedes.",
        "Como Heckgüne, que vio la edición y escribió una sola palabra: cine. O el de Aholic, que nunca había visto a nadie hablar de estos efectos. Y el mismo Sargento Caboose, que fue el suscriptor ciento seis.",
        "Ahora te toca a ti: ¿qué recuerdas de los zombis que nadie más recuerda? Escríbelo. Si es bueno, sale en el siguiente expediente.",
        "En el canal tienes las tres partes de los efectos Mandela de Call of Duty. Suscríbete. [short pause] Retírate, soldado.",
    ]},
]
