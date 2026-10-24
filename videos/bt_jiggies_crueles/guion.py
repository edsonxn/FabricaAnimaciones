# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Los 10 Jiggies más CRUELES de Banjo-Tooie» (23-oct-2026).
Segundo video de Banjo-Tooie del canal (el primero, `banjo_tooie`, historia + 10 secretos, salió el 20-oct). Variable que cambia:
SOLO el ángulo (dificultad del 100 %). Motor SECUENCIA YT (docs/estilo_secuencia_yt.md), voz ElevenLabs Hope (la del primero),
música = BANDA SONORA OFICIAL del juego (regla 23-oct; armar_musica_ost.py), kit translúcido NUEVO nucleo/mg_banjo.py.
Datos verificados el 23-oct-2026 (informe del agente + cuadros de la serie Ninbanyan NSO + API de banjokazooie.fandom.com):
- 90 Jiggies: 8 mundos x 10 + 10 en Isle o' Hags; con 70 se llega a la jefa final.
- Zubbas (Cloud Cuckooland): Banjo abeja (Humba Wumba); en la entrada 20 aguijonazos en 10 s; dentro 60 s, rojo 1 / verde 2 /
  azul 3; 40 = página de Cheato, 50 = Jiggy [visto en juego: «beat 50 points»]. La wiki dice 60 (error).
- Pot 'O' Gold (CCL): danza de la lluvia de Mumbo -> arcoíris; dentro, sala forrada de Jiggies pintados; «at least 75 Jiggies in 45
  seconds» = página de Cheato [visto], 90 = Jiggy [visto].
- Chris P. Bacon (Jolly Roger's Lagoon, Atlantis, Temple of the Fishes): cerdo de vacaciones en una jaula; fotografía las pinturas
  con una Game Boy con cámara; sin doblones para un arpón; una sola mordida de piraña y se repite (wiki: «That nipper bite really
  hurt! Please try harder next time»); bañador con la bandera británica; nombre de un concurso de la Nintendo Official Magazine UK
  (ganó Simon Turk).
- Scrotty (Terrydactyland): Scrat enfermo («un chamán loco que vive en Cliff Top»), Scrit encogido («demasiado pequeño para ser un
  dinosaurio de verdad»), Scrut le robó dinero del monedero y se fue a la estación de tren (aparece en Witchyworld); premio: «esta
  cosa brillante que conseguí cuando pisé a uno de esos Unga Bungas»; Kazooie pide otro Jiggy y le dice que no.
- Mr. Patch (Witchyworld, carpa del circo, boletos): dinosaurio inflable lleno de parches; Kazooie lo provoca; 12 parches con
  huevos granada; tras el primer golpe sale un guante de boxeo rojo que patrulla el suelo -> pelea en el aire (Airborne Egg
  Aiming); escupe pelotas de playa.
- Lord Woo Fak Fak (JRL): pez abisal; 6 forúnculos, solo el que parpadea; luego los ojos; burbujas que atrapan; con Submarine Banjo
  (Humba) torpedos infinitos.
- Weldar (Grunty Industries, sótano del Repair Depot): soplete medio ciego; Kazooie lo confunde con un limpiador de váter; pregunta
  si Banjo es un oso y Banjo dice que no; llegar exige una cadena larga de tareas; 6 placas; huevos a la boca cuando aspira; tras
  3 golpes electrifica el suelo; su cabeza sigue viva.
- Ordnance Storage (Glitter Gulch Mine, Bullion Bill): 15 TNT, desactivar con la bayoneta del pico; un huevo lo vuela todo; 200 s
  desde el primero [visto: 15 y 194]; zona del Breegull Blaster (primera persona).
- Clinker's Cavern (Grunty Industries): 20 Clinkers en 200 s [visto: 20 y 195]; gas tóxico si se acaba el tiempo; Breegull Blaster;
  se llega con las Claw Clamber Boots.
- Canary Mary (CCL): dos carreras machacando A; la 1.ª da el Jiggy, la 2.ª (más larga) una página de Cheato; IA «de goma» (TV Tropes:
  si te pegas acelera, al final acelerón); en GGM era fácil (Rare Gamer); Switch Online = la ROM de N64 (misma carrera).
- Chris Sutherland: GoldenEye en la comida (ya dicho en banjo_tooie). Evercade Double Pack con Bottles' Revenge: 30-oct-2026.
NO usar (sin verificar): objetivos de Dodgems, la cita de «The Scribes», el origen del nombre de Woo Fak Fak, cambios en XBLA.
"""

TITULO = "Los 10 Jiggies más CRUELES de Banjo-Tooie"
ARCHIVO = "bt_jiggies_crueles"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)
# ElevenLabs dice el inglés nativo; solo lo que leería mal
FONETICA = {"Pot 'O' Gold": "Pot o Gold"}

# Revisado el 23-oct leyendo voz/eval.json: Whisper escribe «Zubas/uvas/subas», «Umba Umba», «Cheeto/Chito», «Yigi», «Cuculand»,
# «Skritt/Scrooge», «Zooey» donde Hope dice bien los nombres: falsas alarmas, se aceptan con la CER de la toma buena.
CER_MAX_POR_FRASE = {"contexto_1": .02, "contexto_2": .025, "p10_0": .03, "p10_1": .06, "p10_2": .03, "p10_3": .025,
    "p10_4": .045, "p1_2": .04, "p5_0": .04, "p5_4": .025, "p6_4": .055, "p7_0": .035, "p7_3": .025, "p7_4": .045,
    "p7_5": .035, "p7_6": .045, "p8_5": .025, "p9_4": .06}
TAIL_MAX_POR_FRASE = {"contexto_3": 1.08, "p4_5": 1.2}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    recorte_por={},        # marco NSO: se mide tras bajar (docs: fijar ~.131-.145 para toda la serie)
    yt=dict(sufijo="", min_s=30, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# MÚSICA: banda sonora oficial (audio/ost/, armar_musica_ost.py -> audio/musica.wav). Sin LYRIA.

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[mischievous] En Banjo-Tooie hay noventa Jiggies. Con setenta ya puedes ir a pelear contra la bruja. [short pause] Pero si quieres los noventa, el juego te cobra peaje.",
        "Una carrera que los jugadores siguen odiando veintiséis años después. Una cueva llena de basura, con cronómetro. [amused] Y un cerdo de vacaciones al que tienes que cuidar de las pirañas.",
        "[sarcastic] Y un jefe que es un soplete medio ciego. Que, por algún motivo, está entre los más difíciles del juego.",
        "[playful] Así que hoy te traigo los diez Jiggies más crueles de Banjo-Tooie, del menos malo al peor, y cómo sacarlos sin lanzar el mando contra la tele.",
    ]},
    {"id": "contexto", "frases": [
        "Primero, un poco de contexto. En Banjo-Kazooie, cada mundo era una caja cerrada. Los Jiggies de un nivel se conseguían en ese nivel.",
        "[curious] En Banjo-Tooie, los de Rare conectaron la isla entera. Hay mundos que se tocan, un tren que viaja de uno a otro, y Jiggies que no puedes sacar hasta aprender un movimiento en otro mundo.",
        "[amused] Súmale que Banjo y Kazooie se pueden separar, que Mumbo y Humba Wumba tienen sus propias tareas, y que media isla te manda a hacer recados.",
        "El resultado es un juego enorme, [short pause] y un cien por ciento que pone a prueba la paciencia de cualquiera. Los diez de hoy son los que más se repiten en foros, guías y listas de fans. [excited] Empezamos.",
    ]},
    {"id": "p10", "frases": [
        "[excited] Número diez. El nido de los Zubbas, en Cloud Cuckooland.",
        "Los Zubbas son abejas, y su colmena solo se abre para otra abeja. Así que Humba Wumba convierte a Banjo en una.",
        "[tense] En la puerta, un Zubba te pone a prueba. Veinte aguijonazos en diez segundos, [short pause] solo para que te deje pasar.",
        "Dentro empieza lo bueno. Sesenta segundos, Zubbas de tres colores, y cada color vale distinto. El rojo, un punto. El verde, dos. El azul, tres.",
        "Con cuarenta puntos te ganas una página de Cheato. Para el Jiggy necesitas cincuenta. [sarcastic] Y los Zubbas no se quedan quietos esperando a que les apuntes.",
        "[whispers] El truco: olvídate de los rojos. Persigue a los azules, que valen el triple.",
    ]},
    {"id": "p9", "frases": [
        "[excited] Número nueve. La olla de oro de Gruntilda, también en Cloud Cuckooland.",
        "Primero, Mumbo tiene que hacer su danza de la lluvia para que aparezca un arcoíris. [amused] Y al final del arcoíris, claro, hay una olla de oro.",
        "Ya en la olla, Banjo le dispara los cuatro tipos de huevo, uno por uno, y se abre la prueba de verdad.",
        "[tense] Una sala con las paredes forradas de Jiggies pintados. Tienes cuarenta y cinco segundos para dispararles en primera persona.",
        "Con setenta y cinco aciertos, otra página de Cheato. Para el Jiggy, noventa. [sarcastic] De cien. En cuarenta y cinco segundos.",
        "[whispers] El truco es no apuntar a lo loco. Barre la pared fila por fila, sin volver atrás.",
    ]},
    {"id": "p8", "frases": [
        "[amused] En el ocho, el más absurdo de la lista. Un cerdo de vacaciones en la Atlántida.",
        "En el fondo de Jolly Roger's Lagoon, dentro del Templo de los Peces, cuelga una jaula. Dentro está Chris P. Bacon, con gafas de buceo y un bañador con la bandera británica.",
        "[laughs] Quiere fotografiar las pinturas de las paredes con una Game Boy con cámara. El problema son las pirañas, y como se gastó todo en la cámara, no le quedó para un arpón.",
        "[tense] Así que la jaula baja, los peces atacan desde todos lados, y tú lo defiendes a huevazos. [short pause] Basta una sola mordida para fallar. Y a empezar otra vez.",
        "Chris solo te dice que le dolió mucho, y que la próxima vez te esfuerces más. [sarcastic] Y si te rindes, el Jiggy se queda guardado en su bañador.",
        "[curious] Un detalle: su nombre salió de un concurso de la Nintendo Official Magazine británica. Chris P. Bacon suena a crispy bacon, tocino crujiente.",
    ]},
    {"id": "p7", "frases": [
        "[sighs] Número siete. El Jiggy de los recados. La familia de Scrotty, en Terrydactyland.",
        "Scrotty es una dinosaurio enorme con tres hijos, y los tres tienen un problema.",
        "Scrat está enfermo, y su madre ha oído que en lo alto de un acantilado vive un chamán loco que quizá lo pueda curar. [amused] Hay que llevarlo hasta allí.",
        "Scrit se encogió. Su madre dice que ya es demasiado pequeño para ser un dinosaurio de verdad, y hay que devolverle su tamaño.",
        "[sarcastic] Y Scrut se escapó de casa. Le robó dinero del monedero a su madre, se fue a la estación de tren, [short pause] y acabó en Witchyworld, el parque de atracciones de otro mundo.",
        "Tres tareas, varios viajes en tren y medio mapa recorrido para un solo Jiggy. [laughs] Que Scrotty se encontró al pisar a un cavernícola.",
        "Y cuando Kazooie pregunta si les puede dar otro, por todo el trabajo, [short pause] la respuesta es no.",
    ]},
    {"id": "p6", "frases": [
        "[excited] Número seis. Mr. Patch, el jefe de Witchyworld.",
        "Para verlo hay que juntar los boletos del parque y entrar en la carpa del circo. Al principio parece un asiento incómodo. [amused] Hasta que Kazooie se burla de lo pequeño que es, y él se infla hasta llenar la carpa.",
        "Es un dinosaurio inflable cubierto de parches, y hay que reventarlos todos. [short pause] Doce, con huevos granada.",
        "[tense] Y aquí viene la trampa. Al primer golpe sale del suelo un guante de boxeo rojo que no te deja en paz, y el resto de la pelea es en el aire.",
        "Volando, apuntando en primera persona, esquivando las pelotas de playa que te escupe. [sarcastic] Mientras Kazooie sigue opinando.",
        "[whispers] El truco: ten los huevos granada listos antes de entrar, y apunta mientras vuelas en círculo alrededor de él.",
    ]},
    {"id": "p5", "frases": [
        "[ominous] Número cinco. Lord Woo Fak Fak, el pez abisal de Jolly Roger's Lagoon.",
        "Es un pez enorme con una luz en la cabeza y el cuerpo lleno de forúnculos. Hay seis, y solo puedes golpear el que parpadea en ese momento.",
        "[tense] Cuando revientan todos, toca ir por los ojos. Y mientras tanto, te lanza burbujas que te atrapan bajo el agua.",
        "Con Banjo nadando, el oxígeno y el pez juegan en tu contra a la vez. [short pause] Por eso el truco es otro.",
        "[excited] Humba Wumba puede convertir a Banjo en un submarino. Y el submarino tiene torpedos infinitos. Con él, el jefe se vuelve otra pelea.",
    ]},
    {"id": "p4", "frases": [
        "[amused] En el cuatro, el jefe más ridículo de la lista. [short pause] Y uno de los más difíciles. Weldar, en Grunty Industries.",
        "Antes de verlo hay que sobrevivir a la fábrica, uno de los mundos más largos del juego. Llegar a su sótano exige una cadena de tareas, hechizos de Mumbo y transformaciones.",
        "[laughs] Weldar es un soplete de soldar que casi no ve. Kazooie lo confunde con un limpiador de váter, y él pregunta si Banjo es un oso, porque aquí no se permiten osos. [short pause] Banjo le dice que no.",
        "[tense] La pelea va así. Weldar aspira aire, y en ese momento hay que meterle huevos en la boca. Tiene seis placas en el cuerpo, y cada golpe hace saltar una.",
        "Después del tercer golpe, electrifica el suelo. [sarcastic] Y él da saltos enormes para aplastarte.",
        "[whispers] El truco: no te quedes quieto, y dispara solo cuando abra la boca para aspirar. [amused] Al final explota, pero su cabeza sigue viva, y sigue hablando.",
    ]},
    {"id": "p3", "frases": [
        "[serious] Número tres, y aquí empieza lo serio. El almacén de explosivos de Glitter Gulch Mine. Ordnance Storage.",
        "¿Recuerdas que los de Rare se pasaron años jugando GoldenEye en la hora de la comida? [amused] Aquí se nota más que nunca.",
        "Banjo agarra a Kazooie como si fuera un arma, y todo se juega en primera persona, en un laberinto de túneles sin mapa.",
        "[tense] Hay quince cartuchos de dinamita escondidos, y hay que desactivarlos uno a uno con la bayoneta del pico. Desde el primero, tienes doscientos segundos.",
        "[dramatic] Y la regla de oro: nada de huevos. Un solo disparo cerca de la dinamita, y vuela el almacén entero.",
        "[whispers] El truco: date una vuelta antes de tocar el primero, para aprenderte los túneles, y luego guíate por el sonido de la dinamita.",
    ]},
    {"id": "p2", "frases": [
        "[ominous] Número dos. La cueva de Clinker, en Grunty Industries. Muchos jugadores la llaman el pico de dificultad del juego.",
        "Para llegar necesitas las botas para trepar paredes. [sarcastic] Y la recompensa por llegar es meterte en un vertedero.",
        "Otra vez en primera persona, con Kazooie como arma. Dentro viven los Clinkers, unas criaturas que viven en la basura y se esconden entre los desechos.",
        "[tense] Tienes que eliminar a veinte en doscientos segundos. Y si el tiempo se acaba, la cueva se llena de gas tóxico.",
        "El problema es que no se ven. Algunos están metidos en rincones donde nadie miraría, y el reloj no se detiene.",
        "[whispers] El truco, otra vez, es el oído. Escucha a los Clinkers antes de verlos, y no gastes ni un segundo en mirar dos veces el mismo rincón.",
    ]},
    {"id": "p1", "frases": [
        "[dramatic] Y llegamos al número uno. [short pause] El que todos sabían que iba a estar aquí. Canary Mary, en Cloud Cuckooland.",
        "[curious] Ya te la habías encontrado en Glitter Gulch Mine. Allí te retaba a una carrera, y era bastante fácil. [sarcastic] Era una trampa.",
        "En Cloud Cuckooland vuelve, y ahora tiene un Jiggy. Y también una página de Cheato. Para ganártelos, dos carreras más, cada una más larga que la anterior.",
        "[tense] La mecánica es simple: machacar el botón A lo más rápido que puedas, durante toda la carrera. Si aflojas un segundo, ella te adelanta.",
        "[sarcastic] Y aquí está lo cruel. Los jugadores juran que hace trampa. Si te le pegas, acelera. Y al final da un acelerón, pase lo que pase.",
        "[laughs] Generaciones de niños dejaron los dedos en esta carrera. Hay quien usó un mando con turbo, quien cambió de dedo a mitad de carrera, [short pause] y quien simplemente se rindió.",
        "La segunda carrera, la de la página de Cheato, es todavía peor. Y en Nintendo Switch Online sigue exactamente igual, porque es el mismo juego de Nintendo sesenta y cuatro.",
        "[whispers] El truco que más funciona: no la rebases al principio. Quédate detrás, a su ritmo, guarda fuerzas, [excited] y cuando veas la meta, machaca como si no hubiera mañana.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Esos son los diez Jiggies más crueles de Banjo-Tooie. Una abeja contrarreloj, un cerdo con una Game Boy, dos cuevas en primera persona, [laughs] y una canaria tramposa.",
        "[curious] ¿Tú le ganaste a Canary Mary sin trucos? ¿O cuál fue el Jiggy que te hizo apagar la consola? Cuéntamelo en los comentarios.",
        "Y si te perdiste nuestro video de los diez secretos de Banjo-Tooie, con el modo de juego que estuvo escondido veintiséis años, te lo dejo aquí. [warm] Nos vemos en la próxima crónica.",
    ]},
]
