# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Pokémon Rojo y Azul: su historia y los 20 secretos QUE IGNORASTE» (3-nov-2026, 12-15 min).
Elegido por el usuario entre 3 (Pokémon / GoldenEye / Conker). Fórmula de banjo_tooie/majora_mask (historia + N secretos, motor
SECUENCIA YT, pegatinas reales, fichas translúcidas con la interfaz del juego, mapas reales de Kanto con ruta, OST oficial del juego,
SFX del propio juego). Variable que cambia: SOLO el juego (el más buscado; deja de repetir N64).
Gancho: 30 años de Pokémon (27-feb-2026), Rojo/Fuego y Verde Hoja en Switch ese día, Winds and Waves en 2027.
Datos: investigacion.md (sellos VERIFICADO/DUDOSO/TEORÍA/FICCIÓN y fuentes). No repetir: nada de los videos N64 del canal.
Sonido nombrado (regla del 31-oct): p07 dice «esta es su música» → tramo audible del tema de Pueblo Lavanda con la voz callada
(`post` del beat + ambiente_por), decidido antes de `beats`.
"""

TITULO = "Pokémon Rojo y Azul: su historia y los 20 secretos QUE IGNORASTE"
ARCHIVO = "pokemon_rojo_azul"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo: corchetes iguales, mitad de créditos. Sin susurros ni excitado (2-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"))
# ElevenLabs dice el inglés nativo; solo lo que leería mal (oírlo antes de añadir)
FONETICA = {}
# Falsas alarmas de Whisper (Kanto→Canto, CoroCoro→Korokoro, Jynx→Jinx, Exeggutor→Executor, Victreebel, Ultraseven, Mew→EMU),
# comparadas con eval.json el 3-nov: se aceptan con la CER de la toma única.
CER_MAX_POR_FRASE = {"h1_4": .06, "h2_2": .025, "h3_2": .02, "s17_2": .04, "s12_3": .02, "s11_2": .025, "s10_1": .02,
                     "s08_1": .02, "s03_1": .02, "s03_2": .03, "s02_2": .045, "cierre_3": .02}
TAIL_MAX_POR_FRASE = {"s10_1": .9, "s02_2": .8, "h3_2": .75, "s03_1": .75, "h2_2": .7}
GAP_MAX_POR_FRASE = {"s12_3": .65}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; ambiente_por = beats donde se OYE el juego (regla del 26-oct)
    ambiente_por={"scene-077": 0.95, "scene-083": 0.7},   # 077 = 6 s del tema de Pueblo Lavanda con la voz callada
    recorte_por={},
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora OFICIAL de Pokémon Rojo/Azul (audio/ost, armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[mysterious] Hay un Pokémon que se metió en el juego a escondidas, en el último hueco que quedaba en el cartucho.",
        "[amused] Hay otro que Nintendo te pedía no tocar, porque podía borrarte la partida. Y medio mundo lo buscó igual.",
        "[curious] Y hay un combate entero contra el Profesor Oak que está programado en el juego, y que nadie podía jugar.",
        "[warm] Pokémon cumplió treinta años el veintisiete de febrero de 2026. Ese mismo día, Rojo Fuego y Verde Hoja llegaron a Switch, y se anunció la décima generación.",
        "[playful] Así que hoy volvemos al principio. Cómo nació Pokémon Rojo y Azul, cómo casi arruina a sus creadores, y los veinte secretos que seguramente ignoraste.",
    ]},

    # ================================================================ HISTORIA
    {"id": "h1", "frases": [
        "[warm] Todo empieza con un niño que cazaba insectos. Satoshi Tajiri creció en las afueras de Tokio, y se pasaba las tardes atrapando bichos en los charcos y los bosques.",
        "[sad] Pero la ciudad creció. Los campos se llenaron de casas, y los insectos desaparecieron.",
        "[curious] Años después, Tajiri fundó Game Freak, que empezó como una revista hecha a mano sobre videojuegos, junto al dibujante Ken Sugimori.",
        "Y un día vio el cable link del Game Boy, el cable que unía dos consolas. [short pause] Se imaginó a sus bichos pasando por ese cable, de una pantalla a otra.",
        "[thoughtful] La idea de intercambiar le venía de una frustración. En Dragon Quest Dos no podías pasarle un objeto a un amigo. Con ese cable, sí se podría.",
    ]},
    {"id": "h2", "frases": [
        "[serious] En 1990 le presentó el proyecto a Nintendo. Muchos no lo entendieron, pero Shigeru Miyamoto vio algo, y le dio una idea clave: hacer dos versiones, cada una con Pokémon distintos.",
        "Así, para completarlo, tenías que hablar con otros. [short pause] El juego no se acababa en tu Game Boy.",
        "[curious] Se iba a llamar Capsule Monsters, monstruos de cápsula. Las Poké Balls salieron de las cápsulas de monstruos de la serie Ultraseven. Pero el nombre estaba registrado, y tras varios intentos quedó en Pocket Monsters.",
        "[tense] El desarrollo duró seis años. A veces no había dinero ni para pagar los sueldos. Cinco personas se fueron, y Tajiri dejó de cobrar y vivía de lo que le daba su padre.",
        "Lo salvó otra empresa, Creatures, que puso dinero a cambio de un tercio de los derechos de Pokémon.",
    ]},
    {"id": "h3", "frases": [
        "[impressed] Pocket Monsters Rojo y Verde salió en Japón el veintisiete de febrero de 1996. En una consola que ya tenía siete años.",
        "Empezó despacio. Pero se fue contando de boca en boca, de patio en patio, y acabó vendiendo más de diez millones de copias solo en Japón.",
        "[warm] A América llegó como Rojo y Azul en septiembre de 1998, y a Europa en octubre de 1999. Más de treinta y un millones de copias en el mundo.",
        "[serious] La historia la conoces. Sales de Pueblo Paleta, eliges a Bulbasaur, Charmander o Squirtle, y te propones dos cosas: ganar las ocho medallas y llenar la Pokédex.",
        "[playful] Ciento cincuenta y uno, decía la caja. [short pause] Aunque, como vas a ver, eso nunca fue del todo verdad. Vamos con los secretos.",
    ]},

    # ================================================================ SECRETOS (del 20 al 1)
    {"id": "s20", "frases": [
        "[playful] Número veinte. Te pusiste el nombre del creador sin saberlo.",
        "En el Rojo japonés, uno de los nombres que te proponía el juego para el protagonista era Satoshi. Y para tu rival, Shigeru.",
        "[amused] Satoshi, por Satoshi Tajiri. Shigeru, por Shigeru Miyamoto, el padrino del proyecto. En la versión Verde, los nombres iban al revés.",
        "[warm] Por eso en el anime japonés Ash se llama Satoshi, y Gary se llama Shigeru. Un creador y su maestro, peleando en cada partida.",
    ]},
    {"id": "s19", "frases": [
        "[curious] En el diecinueve, la oficina escondida.",
        "En Ciudad Azulona, en el último piso de la Mansión Azulona, hay un cuarto lleno de gente trabajando. Es Game Freak, los que hicieron el juego.",
        "Ahí puedes hablar con el programador, con el grafista, y con el diseñador del juego.",
        "[impressed] Y si completas la Pokédex, ese diseñador te imprime un diploma. [short pause] Para muchos fue el único premio de cientos de horas de juego.",
    ]},
    {"id": "s18", "frases": [
        "[mysterious] Número dieciocho. El primer Pokémon no fue Bulbasaur.",
        "Bulbasaur es el número uno de la Pokédex. Pero dentro del código, cada Pokémon tiene otro número, uno interno.",
        "[curious] Y el número uno de ese código es Rhydon. Según Ken Sugimori, fue el primer Pokémon que se diseñó.",
        "[amused] Por eso Rhydon aparece por todas partes cuando el juego se rompe. Muchos Pokémon con glitch se convierten en Rhydon al capturarlos.",
    ]},
    {"id": "s17", "frases": [
        "[serious] En el diecisiete, los treinta y nueve Pokémon que se borraron.",
        "Según Shigeki Morimoto, uno de los programadores, el juego iba a tener ciento noventa Pokémon. Treinta y nueve se quedaron por el camino.",
        "[curious] Sus huecos siguen ahí, vacíos, dentro del código. Tanto, que el último Pokémon de la lista interna, Victreebel, está en la posición ciento noventa.",
        "[impressed] Uno de los borrados era Gorochu, la evolución de Raichu. Tres décadas después, todavía no existe.",
    ]},
    {"id": "s16", "frases": [
        "[warm] Número dieciséis. Pikachu empezó siendo un dulce.",
        "Lo dibujó Atsuko Nishida, de Game Freak. Según contó ella misma, la primera idea era un daifuku, un pastelito japonés redondo y blandito.",
        "[amused] Luego lo convirtió en algo parecido a una ardilla, porque en esa época estaba obsesionada con las ardillas. Y Sugimori le dio la forma final.",
        "[curious] Y hay una historia que se repite mucho: que la mascota iba a ser Clefairy. Algunos reportajes lo cuentan, pero nadie lo ha confirmado del todo.",
    ]},
    {"id": "s15", "frases": [
        "[mischievous] En el quince, el camión más famoso de los videojuegos.",
        "Junto al barco S.S. Anne, en Ciudad Carmín, hay un camión. Solo se puede llegar a él con trucos, y no tiene ninguna razón para estar ahí.",
        "[amused] Así que en los patios nació el rumor: si usabas Fuerza en el camión, debajo aparecía Mew.",
        "[serious] Era mentira. Debajo no había nada. [short pause] Pero el rumor fue tan grande, que en Rojo Fuego y Verde Hoja, Game Freak escondió algo debajo del camión. Una Galleta Lava.",
    ]},
    {"id": "s14", "frases": [
        "[curious] Número catorce. El dragón que hacía trampa.",
        "Lance, el último del Alto Mando, el maestro de los dragones, saca al final a su Dragonite.",
        "[amused] Y ese Dragonite usa Barrera. Un ataque que Dragonite no puede aprender de ninguna manera.",
        "[playful] Era el jefe, así que se lo permitieron. Tú, en cambio, nunca pudiste enseñárselo al tuyo.",
    ]},
    {"id": "s13", "frases": [
        "[amused] En el trece, el ataque que hacía justo lo contrario.",
        "Foco Energía prometía subir la probabilidad de dar un golpe crítico. [short pause] Pero por un error de programación, la dividía entre cuatro.",
        "[curious] Y había otro fallo escondido. Los ataques con cien por ciento de precisión podían fallar. Una vez de cada doscientas cincuenta y seis.",
        "[playful] Así que si alguna vez fallaste un ataque seguro en el peor momento, no era mala suerte. Era el juego.",
    ]},
    {"id": "s12", "frases": [
        "[serious] Número doce. Por qué los Pokémon psíquicos eran invencibles.",
        "En Rojo y Azul, el tipo Psíquico arrasaba. Casi nada le hacía daño de verdad.",
        "[curious] La respuesta estaba en un error. El tipo Fantasma tenía que ser súper eficaz contra el Psíquico. Pero en la tabla quedó al revés, y no le hacía nada.",
        "[amused] Y encima el único ataque Fantasma que hacía daño de verdad era Lengüetazo. [short pause] Así que Alakazam y Mewtwo reinaron sin rival hasta la siguiente generación.",
    ]},
    {"id": "s11", "frases": [
        "[mysterious] En el once, el combate contra el Profesor Oak.",
        "Dentro del juego hay un entrenador que nunca llegas a enfrentar. Usa el nombre y el dibujo del Profesor Oak.",
        "[impressed] Y tiene equipo. Tauros, Exeggutor, Arcanine y Gyarados, entre el nivel sesenta y seis y el setenta, más el inicial que tú no elegiste.",
        "[curious] Un equipo a la altura del campeón. No tiene ni una línea de diálogo, y solo se puede pelear con trucos o glitches. [short pause] El jefe final que nunca fue.",
    ]},
    {"id": "s10", "frases": [
        "[curious] Número diez. El Azul que jugaste no era el Azul original.",
        "En Japón no hubo Rojo y Azul. Hubo Rojo y Verde. Y meses después, en octubre de 1996, salió una edición Azul que solo se podía pedir por correo, con la revista CoroCoro.",
        "[impressed] Esa edición Azul traía gráficos nuevos y errores corregidos.",
        "[thoughtful] Y fue la base de las versiones que llegaron al resto del mundo. Tu Rojo y tu Azul eran, por dentro, el Azul japonés.",
    ]},
    {"id": "s09", "frases": [
        "[serious] En el nueve, los Pokémon musculosos que casi tuviste.",
        "Traducir el juego fue tan difícil, que hubo que reprogramarlo desde cero. El código original era demasiado frágil para tocarlo.",
        "[amused] Y el equipo de Nintendo en América propuso algo más. Rediseñar a los Pokémon, para que se vieran más fuertes y musculosos para el público americano.",
        "[dramatic] Hiroshi Yamauchi, el presidente de Nintendo, dijo que no. [short pause] Y gracias a eso, tu Pikachu sigue siendo redondito.",
    ]},
    {"id": "s08", "frases": [
        "[serious] Número ocho. El Pokémon que cambió de color.",
        "Jynx, el Pokémon de hielo con forma humana, tenía la cara negra y los labios gruesos.",
        "[thoughtful] En el año 2000, la escritora Carole Boston Weatherford publicó un ensayo diciendo que recordaba a las caricaturas racistas de antes.",
        "Nintendo la repintó. En Oro y Plata de América su cara ya salía morada. [short pause] Y en las reediciones de Amarillo para la consola virtual, también.",
    ]},
    {"id": "s07", "post": 6.0, "frases": [   # post = 6 s del tema de Pueblo Lavanda con la voz callada (regla del 31-oct)
        "[ominous] En el siete, la leyenda de Pueblo Lavanda.",
        "En 2010 empezó a circular por internet una historia. Que la música de Pueblo Lavanda tenía frecuencias que solo oían los niños. Y que en Japón les había causado dolores de cabeza y cosas peores.",
        "[serious] Todo era inventado. Es una creepypasta, una historia de terror escrita para internet. No hay ningún caso real.",
        "[soft] Pero si alguna vez entraste en ese pueblo, sabes por qué la gente se la creyó. [short pause] Esta es su música.",
    ]},
    {"id": "s06", "frases": [
        "[mysterious] Número seis. ¿Ditto es un Mew que salió mal?",
        "Es una teoría de fans, no algo oficial. Pero tiene sus pistas.",
        "[curious] Ditto y Mew comparten el mismo color rosa. Los dos pueden usar Transformación. Y en la Cueva Celeste, la guarida de Mewtwo, el clon de Mew, aparecen Dittos salvajes.",
        "[thoughtful] La idea es que los científicos intentaron clonar a Mew, y Ditto fue el resultado de los intentos fallidos. [short pause] Game Freak nunca lo ha dicho. Pero tampoco lo ha negado.",
    ]},
    {"id": "s05", "frases": [
        "[ominous] En el cinco, el Pokémon que podía borrarte la partida.",
        "Hablas con el viejo de Ciudad Verde, el que te enseña a capturar. Vuelas a Isla Canela. Y surfeas pegado a la costa del este.",
        "[mysterious] Ahí aparece una figura rota, hecha de cuadros. Se llama MissingNo, de missing number. [short pause] Un número que falta.",
        "[amused] Y te hacía un regalo. Multiplicaba el objeto que tenías en el sexto lugar de tu mochila. Miles de niños lo usaron para tener cien Caramelos Raros o Bolas Maestras.",
        "[serious] En mayo de 1999, Nintendo Power avisó que cualquier contacto con él podía borrar tu partida. [short pause] Y, claro, eso solo hizo que más gente lo buscara.",
    ]},
    {"id": "s04", "frases": [
        "[impressed] Número cuatro. El rumor de Mew que resultó ser verdad.",
        "Durante años, oficialmente solo podías conseguir a Mew en un evento de Nintendo.",
        "[curious] Pero en 2003, siete años después, los jugadores descubrieron un glitch que lo hacía aparecer en tu propia partida. Con un truco de dos entrenadores y una huida en el momento justo.",
        "[playful] Así que, después de tantos rumores falsos, uno sí acabó siendo cierto. [short pause] Mew estuvo en tu cartucho desde el primer día.",
    ]},
    {"id": "s03", "frases": [
        "[warm] En el tres, el concurso que salvó a Pokémon.",
        "Los primeros meses, Pokémon vendía, pero no era un fenómeno. Entonces la revista CoroCoro anunció algo nunca visto: un Pokémon que no salía en el juego, y que regalarían a veinte lectores.",
        "[impressed] Llegaron unas setenta y ocho mil cartas. Por veinte Mew.",
        "[thoughtful] Satoru Iwata, que luego fue presidente de Nintendo, lo contaba así: según él, ese anuncio fue el momento en que las cosas dieron la vuelta para Pokémon.",
    ]},
    {"id": "s02", "frases": [
        "[mischievous] Número dos. El Pokémon que se coló en el cartucho.",
        "Mew no estaba en los planes. Cuando el juego estaba terminado, a los programadores les habían dicho que no tocaran ni un solo bit más.",
        "[curious] Pero al quitar las herramientas de depuración, según contó Shigeki Morimoto, quedó un hueco de unos trescientos bytes. Y él metió ahí a Mew, casi como una broma.",
        "[amused] Ni siquiera Tsunekazu Ishihara, uno de los jefes del proyecto, estaba muy contento cuando se enteró.",
        "[impressed] Y esa travesura, en un hueco de trescientos bytes, acabó siendo el Pokémon más buscado de la historia.",
    ]},
    {"id": "s01", "frases": [
        "[soft] Y llegamos al número uno. El juego que casi no sale.",
        "Durante seis años, Game Freak estuvo a punto de cerrar. Mientras Tajiri terminaba Pokémon, el equipo hacía otros juegos por encargo para poder pagar las facturas.",
        "[sad] Cinco personas se fueron cuando supieron cómo estaban las cuentas. Y Tajiri seguía trabajando sin sueldo, jornadas larguísimas, con su padre pagándole la comida.",
        "[serious] Cuando por fin salió, el Game Boy ya parecía una consola del pasado. Nadie esperaba gran cosa.",
        "[warm] Hoy Pokémon es la franquicia que más dinero ha ganado en la historia del entretenimiento. [short pause] Y empezó con un niño que se quedó sin insectos que atrapar, y decidió meterlos en una pantalla.",
    ]},

    # ================================================================ CIERRE
    {"id": "cierre", "frases": [
        "[warm] Treinta años después, aquí seguimos. Rojo Fuego y Verde Hoja ya están en Switch, y la décima generación llega en 2027.",
        "[warm] Y como siempre, leemos todos los comentarios, y los tomamos en cuenta para el siguiente video. En el video de Banjo-Tooie, Riuma nos contó que solo pudo disfrutar el primer Banjo. Riuma, hoy también tocaba un primero: el primer Pokémon.",
        "[playful] Ahora dime tú. ¿Cuál fue tu primer Pokémon? ¿Y llegaste a encontrarte a MissingNo? Te leo abajo.",
        "[warm] Y si te gustó este viaje a Kanto, suscríbete a Crónicas del gaming. Nos vemos en la siguiente crónica.",
    ]},
]
