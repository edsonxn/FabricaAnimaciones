# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Los 8 mundos de Banjo-Tooie del PEOR al MEJOR (y sus Easter eggs ocultos)» (30-oct-2026, ~25 min).
Pedido del usuario: ranking de los 8 mundos, largo de 25 min, con Easter eggs de cada mundo + curiosidades y secretos, «sobre todo
Easter eggs». Tercer video de Banjo-Tooie del canal; variable que cambia: formato largo por mundos. Motor SECUENCIA YT, voz
ElevenLabs Hope, música = OST del juego (audio/ost, armar_musica_ost.py), SFX del juego (sfx/bt_*.mp3), kit mg_banjo.
Datos: investigacion_mundos.md (con sellos VERIFICADO/DUDOSO/TEORÍA y fuentes). Mapas: Guía oficial de Nintendo (2000).
Orden: media de 4 listas (MrDrBoi, Virtual Bastion, TheGamer, Super Joe Bros): GI 6,5 · JRL 6,3 · TDL 5,3 · MT 5,3 · GGM 5,0 · CCL 4,5
· WW 1,9 · HFP 1,4. TDL y MT empatan: va antes TDL por tener un voto E.
Frases cerradas contra verificacion_clips.md (30-oct-2026). NO decir: Rare fundada en 1984 (fue 1985); Weldar guiño a Nuts & Bolts; Jolly's
como bar gay confirmado; peluche de Conker en Evercade.
"""

TITULO = "Los 8 mundos de Banjo-Tooie del PEOR al MEJOR (y sus Easter eggs ocultos)"
ARCHIVO = "bt_mundos_ranking"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)
# ElevenLabs dice el inglés nativo; solo lo que leería mal
FONETICA = {}
TAIL_MAX_POR_FRASE = {"contexto_0": 1.1, "p1_6": 1.25}   # hablan hasta el final, y la transcripción termina bien
# Revisado el 30-oct leyendo voz/eval.json: Whisper escribe «Mr Doctor Boy», «Cheeto/Chito», «Hellfire», «Mombo», «Pono», «Tricross» donde Hope
# dice bien los nombres, y cifras en vez de letras: falsas alarmas, se aceptan con la CER de la toma buena.
CER_MAX_POR_FRASE = {"contexto_0": 0.042, "p8_3": 0.035, "p8_12": 0.014, "p8_13": 0.033, "p8_15": 0.015, "p8_16": 0.02, "p8_17": 0.019, "p7_3": 0.022, "p7_5": 0.036, "p7_9": 0.017, "p7_10": 0.017, "p7_11": 0.034, "p7_13": 0.025, "p7_14": 0.031, "p6_2": 0.035, "p6_6": 0.017, "p6_7": 0.038, "p5_1": 0.016, "p5_8": 0.04, "p5_9": 0.033, "p4_2": 0.029, "p4_6": 0.017, "p4_7": 0.015, "p4_9": 0.014, "p4_10": 0.021, "p4_11": 0.037, "p3_0": 0.067, "p3_4": 0.015, "p3_5": 0.03, "p3_9": 0.021, "p3_10": 0.031, "p3_12": 0.023, "p2_4": 0.019, "p2_5": 0.034, "p1_0": 0.062, "p1_1": 0.036, "p1_5": 0.029, "p1_6": 0.024, "p1_7": 0.074, "p1_10": 0.015}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    ambiente_por={'scene-031': 0.5, 'scene-034': 0.5, 'scene-042': 0.8, 'scene-044': 0.5, 'scene-046': 0.8, 'scene-054': 0.8, 'scene-055': 0.8, 'scene-062': 0.5, 'scene-063': 0.8, 'scene-065': 0.8, 'scene-079': 0.8, 'scene-081': 0.5, 'scene-089': 0.5, 'scene-090': 0.5, 'scene-097': 0.8, 'scene-098': 0.5, 'scene-102': 0.8, 'scene-103': 0.9, 'scene-104': 0.8, 'scene-110': 0.8, 'scene-122': 0.8, 'scene-123': 0.8, 'scene-137': 0.5, 'scene-138': 0.5, 'scene-141': 0.8, 'scene-142': 0.8, 'scene-143': 0.8, 'scene-144': 0.8, 'scene-148': 0.5, 'scene-149': 0.8, 'scene-151': 0.8, 'scene-152': 0.8, 'scene-156': 0.8, 'scene-158': 0.8, 'scene-159': 0.8, 'scene-160': 0.8},
    recorte_por={},         # Ninbanyan NSO con widescreen: sin marco
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora del juego (audio/ost, armar_musica_ost.py -> audio/musica.wav).

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[whispers] En Banjo-Tooie hay un baño con la puerta cerrada. Una vez de cada mil, por debajo de esa puerta sale luz. [short pause] Y si te acercas, oyes a alguien adentro.",
        "[amused] Hay un cartón de leche con el aviso de un personaje desaparecido. Una constelación escondida en el cielo de un parque de atracciones. [short pause] Y un pirata borracho que jura que un oso le robó la gloria.",
        "[sarcastic] Nada de eso te lo explica el juego. Está ahí, escondido, desde hace veintiséis años.",
        "[playful] Hoy vamos a recorrer los ocho mundos de Banjo-Tooie, del peor al mejor. Y en cada uno te voy a enseñar sus Easter eggs, sus curiosidades y sus secretos.",
    ]},
    {"id": "contexto", "frases": [
        "Antes, dos cosas. La primera: este orden no es solo mi opinión. Crucé cuatro listas, las de MrDrBoi, Virtual Bastion, TheGamer y Super Joe Bros, y saqué la media.",
        "[amused] Y vas a ver que nadie se pone de acuerdo. Hay mundos que en una lista son de lo mejor del juego, y en otra, lo peor.",
        "La segunda: por qué este juego está tan lleno de chistes escondidos. Los de Rare lo contaron en su propio documental. Querían ver cuántos dobles sentidos podían colar, [short pause] y cruzar los dedos para que no se los cortaran.",
        "[laughs] Los diálogos, según ellos, se fueron inventando sobre la marcha. Y se nota.",
        "[warm] Este video también sale de un comentario. Riuma nos escribió que Banjo-Tooie le parece muy interesante, pero que solo pudo disfrutar del primero. Leemos todos los comentarios, y los tomamos en cuenta para mejorar. Así que este recorrido también es para quien nunca entró a estos mundos.",
        "Son ocho mundos, con diez Jiggies cada uno, y casi todos conectados entre sí por túneles, pasadizos y un tren. [excited] Empezamos por el último. Y es el más polémico del juego.",
    ]},

    # ================================================================ 8. GRUNTY INDUSTRIES (6,5)
    {"id": "p8", "post": 1.5, "frases": [
        "[sarcastic] Puesto número ocho. Grunty Industries.",
        "[amused] La guía oficial de Nintendo lo explica así: como la brujería ya no vende, Gruntilda cambió de negocio. [short pause] Ahora fabrica ropa interior.",
        "Y el mundo te recibe con una broma pesada. La puerta está cerrada. No puedes entrar. Hay que salir, subirse al tren, y volver dentro de él.",
        "¿Por qué está en el último lugar? Para MrDrBoi es el peor de todos. Para Virtual Bastion, el cuarto mejor. Y en el chat de Super Joe Bros quedó en la categoría A, con la D pisándole los talones.",
        "[sighs] Las quejas se repiten: demasiadas baterías, demasiados conejos, y gris por todos lados. Es tan largo que Super Joe necesitó dos directos para terminarlo.",
        "[mischievous] Pero aquí están algunos de los mejores Easter eggs de todo el juego. Y el primero lo contó un desarrollador de Rare en persona.",
        "[whispers] Primer piso, cuartos de los trabajadores. Justo al entrar, a la izquierda, hay una puerta de baño.",
        "Steve Malpass, diseñador de Rare, contó que casi nunca pasa nada con ella. Pero más o menos una vez de cada mil, sale luz por debajo.",
        "[laughs] Y si te acercas, oyes a un conejo obrero haciendo sus necesidades, y quejándose de que los dedos le atravesaron el papel.",
        "[sarcastic] Con esas probabilidades, puedes terminar el juego entero sin haberlo visto nunca.",
        "[curious] En ese mismo cuarto hay un refrigerador lleno de pegatinas con logos de Rare. Una dice B-T, por Banjo-Tooie. Y otra, en rojo, dice DK. [short pause] Por Donkey Kong.",
        "[amused] Cuando el juego salió en Xbox, Rare ya era de Microsoft. Y ese logo cambió de DK a BK. Una letra, y problema resuelto.",
        "Sigue subiendo, y mira las cajas. Una dice: entregar en Twycross, Inglaterra. Que es donde tiene su sede Rare. [laughs] Y otra, pegada a ella, dice mercancía defectuosa. Se mandaron los defectos a su propia casa.",
        "Otra caja dice BIG-O PANTS, y trae unos calzones. Hay quien la lee como un guiño a Mister Pants, la mascota de la web de Rare. [mischievous] Guárdate ese nombre, porque va a volver.",
        "En el baño de hombres regresa Loggo, el excusado parlante del primer juego. [sarcastic] Porque este mundo tenía que tener más de un chiste de baño.",
        "Y la transformación de Humba Wumba es otro chiste viejo. En Banjo-Kazooie, Mumbo podía convertirte en lavadora por accidente. Aquí lo convierten en poder, [short pause] y disparas calzones.",
        "Cierro con el jefe, porque su historia es la mejor de todas. Steve Malpass dibujó un soplete con ojos. Le pareció malo, y lo tiró a la basura.",
        "Después lo sacó de la papelera, todavía manchado, y se lo puso enfrente a Gregg Mayles. Así nació Weldar, uno de los jefes favoritos del juego.",
        "[warm] Su moraleja es muy buena: no tires nada, porque otro puede ver lo que tú no viste.",
    ]},

    # ================================================================ 7. JOLLY ROGER'S LAGOON (6,3)
    {"id": "p7", "post": 1.5, "frases": [
        "[playful] Puesto número siete. Jolly Roger's Lagoon.",
        "Parece un pueblito pesquero con un bar, una tienda de empeños y poco más. [short pause] Hasta que te metes al agua, y descubres que debajo hay un mar entero y hasta la Atlántida.",
        "Collider lo llama el mundo que no deja de dar. Lo que lo hunde en las listas es el control bajo el agua. Apuntar buceando no es divertido, y los pulpos se meten en cada pasillo.",
        "[curious] El Easter egg más triste del juego está en el bar. En una habitación de Jolly's hay un pirata borracho, el Capitán Blackeye.",
        "Te dice que un oso le robó su gloria. [short pause] Y que, por cierto, se parecía bastante a ti. Suena a tontería de borracho. Hasta que sabes quién es.",
        "[serious] Blackeye iba a ser el villano de Project Dream, el proyecto que Rare abandonó y que terminó convertido en Banjo-Kazooie. Y Banjo salió de un personaje secundario de ese proyecto.",
        "[sighs] Literalmente, un oso le robó la gloria. Rare nunca lo ha explicado, pero cuesta creer que sea casualidad. Y ahí sigue, bebiendo.",
        "[mischievous] Bajo el agua hay un OVNI. Y cuando Kazooie conoce a los alienígenas, les pregunta si alguno se llama Elvis, que es un guiño a Perfect Dark. Después, si necesitan llamar a casa. [amused] Y eso ya es E.T.",
        "En el fondo del mar está el casillero de Davy Jones, donde vive el jefe. Y los casilleros de alrededor llevan nombres del equipo de Rare: G. Kirkhope, el compositor. G. Mayles, el diseñador. Es la firma de los desarrolladores, en el último rincón del mapa.",
        "En la tienda de empeños de Pawno hay una caja marcada con las letras B-K. [sarcastic] Banjo y Kazooie, con sus cosas en una casa de empeños. Se ve que el primer juego no les dejó tanto.",
        "Y en este pueblo vive Merry Maggie Malpass. Sí, Malpass, como Steve Malpass, el del baño secreto. Dicen que el nombre viene de él, aunque eso no está confirmado.",
        "[curious] Otro nombre con historia es el del jefe, Lord Woo Fak Fak. Según la wiki de los fans, y tómalo con pinzas, el ingeniero Paul Machacek soltaba groserías con cada error, y gritaba woo al arreglarlo.",
        "[amused] Y para respirar bajo el agua, Mumbo tiene un hechizo que se llama Sunlight, luz del sol. ¿Su efecto? Agua oxigenada. [sarcastic] Porque para qué ponerle un nombre que tenga sentido.",
        "Un truco para este mundo: en la Cámara de Códigos escribes CHEATO, y luego jukebox al revés. La rocola de Jolly's vuelve a funcionar, y te da una prueba de música.",
        "Y si te gusta buscar, una página de Cheato está dentro de unos peces transparentes, y otra te la vende Pawno por cinco doblones.",
    ]},

    # ================================================================ 6. TERRYDACTYLAND (5,3)
    {"id": "p6", "post": 1.5, "frases": [
        "[amused] Puesto número seis. Terrydactyland, Terry más pterodáctilo.",
        "Otro mundo que parte a los fans en dos. Para Super Joe Bros está en la E, de lo peor del juego. Para Virtual Bastion, es el tercero mejor.",
        "[sighs] Las críticas son fáciles de entender. Es enorme, está bastante vacío, y las cuevas se parecen demasiado por fuera. MrDrBoi contó ocho pasos para sacar un solo Jiggy de los cavernícolas.",
        "[excited] Pero tiene algo que ningún otro mundo tiene. Humba Wumba te convierte en un T-Rex. Y si Mumbo agranda su tienda primero, sales convertido en Daddy T-Rex, que no cabe en ningún lado.",
        "[mischievous] El mejor engaño está en Chompa. Una cinemática épica te hace creer que te acaba de devorar. [short pause] Y dentro de la barriga, el juego se convierte en un minijuego en primera persona.",
        "En las Llanuras del Pisotón pasa algo que Rare no se molesta en explicar. Del Stomponadon, un dinosaurio gigantesco, solo vas a ver el pie. [amused] Nada más. Un pie que baja del cielo y te aplasta.",
        "Terry, la jefa del mundo, es además el personaje que más Jiggies te da de todo el juego. Tres. [sarcastic] Tienes que cuidar a sus crías, claro. Nadie regala nada en esta isla.",
                "Lo mejor de Terrydactyland son sus conexiones. La cueva de Unga Bunga tiene una salida secreta que llega a la Cámara del Tesoro de Mayahem Temple. El cavernícola le había robado su reliquia a Targitzan.",
        "La cueva de Oogle Boogle se conecta por un pasadizo con Witchyworld, porque los cavernícolas necesitan comida chatarra del parque.",
        "[curious] Y la piscina de Dippy se llena desde otro mundo. Allá arriba, en Cloud Cuckooland, drenas una piscina con el Talon Torpedo, y el agua cae hasta aquí.",
        "Es decir: el mundo que parece más vacío es el que más cables tiene conectados al resto del juego.",
    ]},

    # ================================================================ 5. MAYAHEM TEMPLE (5,3)
    {"id": "p5", "post": 1.5, "frases": [
        "[playful] Puesto número cinco. El primero que pisas. Mayahem Temple.",
        "El nombre es el primer chiste del mundo: Maya, más mayhem, que en inglés significa caos.",
        "Para Super Joe Bros es el mejor arranque posible: grande, pero sin abrumar. Para Virtual Bastion es el último de todos, básico y olvidable. [sarcastic] Y a Stony, la transformación de este mundo, casi nadie la defiende: lento y poco divertido.",
        "[excited] Pero aquí se estrenan dos cosas enormes. La primera: por primera vez en la saga, controlas a Mumbo.",
        "La segunda es Kazooie como arma. Chris Sutherland, de Rare, contó que cuatro o cinco del equipo jugaban GoldenEye casi todas las horas de comida, durante un par de años.",
        "Y eso se coló en el juego. Separaron a los personajes, y Banjo terminó apuntando con su mejor amiga en primera persona. Se estrena aquí, en el templo de Targitzan.",
        "[amused] Targitzan, por cierto, es el dios maya del tiro al blanco. Según la wiki, el nombre juntaría target, blanco en inglés, con Tarzán. Y todo su templo va de disparar.",
        "[mischievous] Ahora el Easter egg que más gente ha usado sin saberlo. La Cámara de Códigos. Una sala con la pared llena de letras, donde escribes trucos disparándoles huevos.",
        "Todos los códigos empiezan con CHEATO, y varios van escritos al revés. CHEATO SGGE te da el doble de huevos, porque SGGE es eggs al revés. CHEATO KCABYENOH hace que la salud se recupere: honey back.",
        "[playful] Hay uno que abre todos los mundos, y otro, CHEATO JIGGYS CAST LIST, que hace desfilar a todos los personajes del juego.",
        "[whispers] Y mira la primera fila de la pared. Empieza con E, S, R, A. Al revés, ARSE. Que en el inglés británico de Rare significa culo. No está confirmado que sea a propósito. [sarcastic] Pero conociendo a Rare, yo no apostaría a que fue casualidad.",
        "Y hay más chistes en los nombres. Targitzan tiene una Cámara Ligeramente Sagrada, y otra Realmente Sagrada. Porque hasta lo sagrado tiene categorías. [amused] Y el rótulo de la primera viene con errata: le falta una letra a la palabra slightly.",
        "[curious] La música tiene su propia historia. Viene de un tema descartado de Banjo-Kazooie, y de esa misma idea salió también Angry Aztec, en Donkey Kong 64.",
        "Una sola melodía que Rare no quiso tirar, [short pause] y que terminó en dos de sus juegos.",
    ]},

    # ================================================================ 4. GLITTER GULCH MINE (5,0)
    {"id": "p4", "post": 1.5, "frases": [
        "[playful] Puesto número cuatro. Glitter Gulch Mine.",
        "[amused] La guía oficial de Nintendo lo resume mejor que nadie: en lugar de un saludo amistoso, aquí te ofrecen dinamita y gas venenoso.",
        "A MrDrBoi le encanta que los Jiggies tengan varias soluciones. A Virtual Bastion, su ambiente solitario, bajo tierra. Las quejas: cuesta orientarse, y el Detonator, la transformación de este mundo, no sirve para casi nada.",
        "[curious] Lo curioso es que este mundo iba a estar en el primer juego. Chris Sutherland le contó a Retro Gamer que Witchyworld y Glitter Gulch eran ideas de Banjo-Kazooie que se aplazaron por falta de tiempo.",
        "Los Easter eggs de aquí están en los nombres. Canary Mary, la de las carreras, no se llama así por capricho. Es una canaria en una mina, como las que bajaban los mineros para detectar el gas.",
        "[sarcastic] Sí, el personaje que hizo llorar a media generación está basado en un pájaro que avisaba si ibas a morir.",
        "El jefe es Old King Coal, un trozo de carbón con corona, dentro de la caldera del tren. Suena a Old King Cole, la canción infantil inglesa, y muy parecido a Nat King Cole.",
        "Bullion Bill, el minero, se llama como los lingotes de oro. Y su socia es Dilberta, una rata que está atrapada en otro mundo. [amused] Hay que abrir un túnel hasta Mayahem Temple para sacarla.",
                "[mischievous] Y mira la Crushing Shed. Una roca con una veta amarilla entra a la trituradora, salta hecha pedazos, [short pause] y de ahí sale tu Jiggy, entero. Esto es lo que aquí llaman minería.",
        "[excited] Ahora el secreto grande. ¿Recuerdas Bottles' Revenge, el modo en el que otro jugador controlaba a los enemigos? Rare lo confirmó en su documental: lo probaron en un jefe. [short pause] Y fue este, Old King Coal.",
        "Y otro más. Bajo el agua hay una roca que se rompe con el Talon Torpedo. El pasadizo sale, nada menos, al lado helado de Hailfire Peaks.",
        "Allí, una llave de hielo abre la caja del Mega Glowbo. Es parte del famoso Stop 'n' Swop, la promesa que unió a dos juegos separados por dos años.",
    ]},

    # ================================================================ 3. CLOUD CUCKOOLAND (4,5)
    {"id": "p3", "post": 1.5, "frases": [
        "[excited] Entramos al podio. Puesto número tres. Cloud Cuckooland.",
        "Un mundo que flota sobre la isla, sin estación de tren y sin camino normal. Es un montón de islas sin ninguna lógica entre ellas. Y por eso divide tanto: para TheGamer es el segundo mejor, para Virtual Bastion, el séptimo.",
        "[sarcastic] Empieza de maravilla. Lo primero que haces al llegar es matar a alguien. George Ice Cube, un cubo de hielo que cae de un empujón al agua hirviendo.",
        "Guarda a George, porque su historia termina en el puesto número uno.",
        "[whispers] Ahora el Easter egg más famoso del juego. Dentro del bote de basura flotante hay un cartón de leche. Y en el cartón se lee: desaparecida, Tooty. Vista por última vez en Banjo-Kazooie.",
        "[sighs] Tooty, la hermana de Banjo. La razón de toda la aventura del primer juego. Y el chiste terminó siendo verdad: nunca volvió a aparecer.",
        "[curious] El nombre del mundo es uno de los guiños más cultos de todo Rare. Cloud cuckoo land viene de Aristófanes, de la comedia griega Las aves, del año cuatrocientos catorce antes de Cristo.",
        "Allí, unos pájaros fundan una ciudad en las nubes. Y en inglés, la frase se quedó para decir que alguien vive en las nubes. [amused] Un juego con una protagonista pájaro, citando a los griegos, en un mundo con un bote de basura flotante.",
        "[mischievous] En este mundo hay una caja fuerte con ojos, el Superstash. Se abre con cuatro números: uno, nueve, ocho, cuatro.",
        "[curious] Rare se fundó en mil novecientos ochenta y cinco. Pero en mil novecientos ochenta y cuatro salió Sabre Wulf, de Ultimate, la empresa de la que nació Rare. La teoría es que el guiño va por ahí.",
        "Este mundo aislado tampoco está tan aislado. ¿Recuerdas la piscina de Dippy? Se drena aquí, y el agua baja hasta Terrydactyland.",
        "Y el jefe es de los mejores chistes de la saga. Mingy Jongo, un doble robot de Mumbo, escondido en una de las dos calaveras del mundo.",
        "[sarcastic] Sí, aquí también está la segunda carrera de Canary Mary. Super Joe confiesa que usa un mando con turbo. Y nadie lo juzga.",
    ]},

    # ================================================================ 2. WITCHYWORLD (1,9)
    {"id": "p2", "post": 1.5, "frases": [
        "[excited] Puesto número dos. Witchyworld.",
        "La guía oficial lo define como la versión de espejo de feria de un buen lugar para llevar a la familia: empleados locos con mazos, tragamonedas que te disparan, [short pause] y atracciones casi tan peligrosas como la comida.",
        "Es el mundo más fácil de entender: cuatro zonas alrededor de una carpa de circo. Espacio, Viejo Oeste, Infierno y Área 51. Y es el primero donde Banjo y Kazooie se separan con los pads.",
        "Virtual Bastion lo pone primero. Y al final, el público de Super Joe Bros también lo dejó arriba del todo.",
        "[whispers] Y aquí está la constelación del principio. Entra al vestíbulo del Dodgem Dome, en la Zona Espacial, y mira por la ventana. Las estrellas forman la figura de Mister Pants. [short pause] Ojo: esta es la versión de Xbox, donde se distingue bien. En Nintendo 64 mis tomas no me dejaron verla.",
        "[amused] Mister Pants era la mascota de la web de Rare, un monigote hecho a propósito con pésimo dibujo, que acabó teniendo su propio juego. Y aquí está, en el cielo.",
        "[mischievous] El mejor chiste del parque está en un letrero. Avisa que Witchyworld está cerrado por un historial de seguridad espantoso, [short pause] y que reabrirá en cuanto hayan sobornado a las autoridades.",
        "La comida también tiene su humor. El letrero de Big Al anuncia hamburguesas con cien por ciento de carne de origen roedor, y una rebanada de queso sintético.",
        "Y el de las papas de Salty Joe las vende como la alternativa grasosa y sin sabor. [sarcastic] Es lo más honesto que vas a leer en todo este parque.",
        "[curious] Una teoría de fans dice que Witchyworld está inspirado en Action Park, un parque real de Nueva Jersey famoso por sus lesiones. Rare nunca lo confirmó, pero ese letrero de los sobornos ayuda.",
        "La música tiene un secreto. Un pasaje de Chase, un tema de Project Dream, reaparece aquí como Witchyworld. Otra vez el juego cancelado escondido dentro de este.",
        "Y como Glitter Gulch, este mundo era una idea de Banjo-Kazooie que no llegó a tiempo. Dos años de espera que le sentaron muy bien.",
        "[excited] El punto débil son los niños Boggy. Uno de ellos exige una habilidad de varios mundos después. Legacy of Games perdió una hora entera sin saberlo.",
        "Pero hay algo que nadie olvida: la Van. Humba Wumba convierte a Banjo en una camioneta. [amused] Con claxon, y con dinero para pagar las atracciones.",
    ]},

    # ================================================================ 1. HAILFIRE PEAKS (1,4)
    {"id": "p1", "post": 2.0, "frases": [
        "[dramatic] Y llegamos al número uno. [short pause] Hailfire Peaks.",
        "[excited] Las cuatro listas lo ponen arriba. Es, para MrDrBoi, como el décimo mundo de Banjo-Kazooie: dos montañas pegadas, una de lava y otra de hielo, cada una con su jefe, su música y su clima.",
        "[curious] Y tiene historia. El lado de fuego nació como Mount Fire Eyes, un nivel cortado de Banjo-Kazooie.",
        "Gobi, el camello del primer juego, hablaba de ir a un mundo de lava. Ese mundo se canceló. Aquí, dos años después, por fin llega. [sarcastic] Y tú le vuelves a robar el agua.",
        "Con esa agua enfrías la caldera del tren, porque Chuffy no puede cruzar al lado helado sin ella.",
        "[amused] El Easter egg más viejo de todos está congelado. Sabreman, el héroe de Sabre Wulf, de mil novecientos ochenta y cuatro, está atrapado en el hielo. Hay que revivirlo y llevarlo hasta su tienda. Un guiño de Rare a su propia historia.",
        "[mischievous] Y ahora, la casa de Boggy. El oso polar del primer juego vive aquí en un iglú con su familia. Tiene sofá, y tiene tele.",
        "¿Y qué sale en la tele? Mister Pants. Sí, otra vez. Te dije que iba a volver.",
        "[laughs] Boggy te invita a quedarte, porque acaba de comprar un DVD: Bear Babes, chicas oso. Y según él, debe estar candente. [sarcastic] Esto es un juego de Nintendo sesenta y cuatro para toda la familia.",
        "Según la wiki de los fans, el título completo también cambió: de Bear Babes and Eskimos en Nintendo 64, a Bear Babes and Bigfoot en Xbox. Rare ya lo había advertido: querían ver cuántos dobles sentidos podían colar.",
        "En el cuarto de los niños Boggy cuelga un cuadro con un muñeco de nieve, como el de Freezeezy Peak, el mundo nevado del primer juego. [warm] Hasta la decoración de este iglú es nostalgia.",
        "[curious] ¿Recuerdas a George Ice Cube, el del empujón? Cae aquí. Y su pareja es Mildred Ice Cube. Son George y Mildred Roper, de una comedia británica de los años setenta. Un chiste que casi nadie fuera de Inglaterra pudo entender.",
        "Los secretos siguen. Los dos lados comparten la misma melodía, con arreglos distintos: uno de fuego, otro de hielo.",
        "Mumbo y Humba, los rivales de toda la saga, tienen sus casas conectadas por un pasadizo: de la calavera en la lava, al wigwam en el hielo.",
        "[serious] Y el hechizo de Mumbo aquí es Life Force, que devuelve la vida. Sirve para revivir a los hijos de los alienígenas de Jolly Roger, que se estrellaron. Collider lo llama extrañamente desgarrador.",
        "La caja de hielo de Glitter Gulch también termina aquí, con el Mega Glowbo que convierte a Kazooie en dragón.",
        "[warm] Por eso gana. Porque es enorme, pero se recorre fácil. Porque tiene dos mundos en uno. Y porque, si sabes dónde mirar, en cada iglú y en cada calavera, Rare dejó un chiste esperándote.",
    ]},

    # ================================================================ CIERRE
    {"id": "cierre", "frases": [
        "[warm] Esos son los ocho mundos de Banjo-Tooie. Y si los miras todos juntos en el mapa, entiendes la idea de Rare.",
        "Mayahem conecta con Glitter Gulch y con Terrydactyland. Glitter Gulch, con Hailfire. Witchyworld, con Terrydactyland. Y Cloud Cuckooland, flotando arriba, le llena la piscina a Dippy.",
        "[curious] No hicieron ocho niveles. Hicieron una sola isla, llena de chistes que no tenías que encontrar, [short pause] y que aun así están ahí veintiséis años después.",
        "[playful] ¿Tú cuál pones en el número uno? ¿Viste alguna vez la luz del baño? Y si conoces un Easter egg que me faltó, cuéntamelo en los comentarios, porque los leo todos.",
        "Si te gustó, aquí te dejo los diez Jiggies más crueles del juego, y la historia de Rare, el estudio que Nintendo dejó ir. [warm] Nos vemos en la próxima crónica.",
    ]},
]
