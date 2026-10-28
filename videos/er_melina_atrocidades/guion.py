# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Melina QUE IGNORASTE» (27-oct-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md (copia del ganador, Miquella ~20 min ×18 y
46 % visto, cambiando UNA variable: el sujeto → Melina, la acompañante de todo el juego; mismo gancho «la favorita es la peor»
que Ranni, el mejor arranque del canal). El usuario pidió al menos 18 min (27-oct-2026).
Cada puesto va partido en dos escenas (pN / pNb), como Miquella y Malenia.
No repite lo ya contado: la Noche de los Cuchillos Negros, Tiche, Godwyn y Maliketh sellando la hoja (Ranni p2), el genocidio de
Mésmer (su video propio): aquí solo salen como guiño.
Citas verificadas el 27-oct-2026 en eldenring.fandom.com (wikitexto: Melina, Melina/dialogue con el texto inglés Y japonés,
Messmer's Kindling, Messmer, Blade of Calling, Minor Erdtree, Rune of Death, Leyndell Ashen Capital, Giants' Flame, Gloam-Eyed
Queen) y eldenring.fandom.com/es (nombres oficiales en español: Sinluz, Torrentera, doncella enyescada, Hoja de la invocación,
Yesca de Messmer, Forja de los gigantes, Picos de los gigantes, Cámara de la llama frenética, Leyndell capital del Reino).
Las citas en español son traducción fiel del inglés (sin inventar). Lo que es TEORÍA se dice como teoría: la Reina de ojos
del Ojo Velado (el ojo sellado) y que Melina sea hermana de Malenia y Miquella (la wiki: «hermana o media hermana»).
EVITAR: decir que la quema mató a toda la capital (el juego solo enseña la ciudad enterrada en ceniza) o que Melina «drogó» al
Sinluz (la wiki dice que lo adormece al tomarle la mano).
"""

TITULO = "Las 5 peores atrocidades de Melina QUE IGNORASTE"
ARCHIVO = "er_melina_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# 22-oct: nombre propio que Whisper escriba distinto = error REAL, regenerar (Miquella → «Mikeya» hizo burla en los comentarios).
FONETICA = {
    "Miquella": "Mikuéla", "Malenia": "Malénia", "Radahn": "Rádan", "Radagon": "Rádagon", "Godfrey": "Gódfri",
    "Messmer": "Mésmer", "Maliketh": "Málikez", "Morgott": "Mórgot", "Leyndell": "Léindel", "Farum Azula": "Fárum Azúla",
    "Godwyn": "Gódüin", "Boc": "Bok", "Enia": "Énia", "Ranni": "Ráni", "Polyanna": "Poliána", "Millicent": "Mílisent",
    "Limgrave": "Límgreiv", "Elden Ring": "Élden Ring", "Elden": "Élden",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; el audio del juego va donde conviene oírlo (regla del 26-oct-2026)
    ambiente_por={},        # {"scene-012": .8}: ese beat baja CON su audio (diálogo de Melina, el silbido); la OST se aparta ahí
    recorte_por={f"scene-{n:03d}": 0.09 for n in (4, 35, 36, 37, 51, 52, 53, 54, 70, 72, 80, 100, 113, 128, 134, 137, 140)},   # firma «SHIRRAKO»
    yt=dict(sufijo="Elden Ring", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar"]),   # heredado de Malenia
)

# Revisado el 27-oct tras la 1.ª ronda (eval.json): 58 marcadas, casi todas falsas alarmas (pausas tras punto, colas en frases
# largas y nombres que Whisper escribe a su manera: «Enya», «Morgoth», «Márica», «Buck», «Malikes»). Errores REALES: «DLC» →
# «dieque» (p4_4: «la expansión»), «Maliketh» comido a final de frase (p2_6: «…a Maliketh, su guardián»), «fremética» (p1_2),
# «Ladagon/Lani» tras «de» (cierre_3: «Márika y Radagon… la de Ranni») y tomas sueltas con palabras cambiadas → voz/_descartes/.
CER_MAX_POR_FRASE = {'p2_6': 0.011, 'p4b_1': 0.041, 'p4b_3': 0.015, 'p2_8': 0.02, 'p2_9': 0.023, 'p2b_4': 0.014}
GAP_MAX_POR_FRASE = {'p4_4': 0.7, 'intro_1': 0.72, 'intro_6': 0.78, 'p5_9': 0.81, 'p4_6': 0.76, 'p4b_10': 0.67, 'p3_4': 0.67, 'p3_5': 0.67,
                     'p3_8': 0.81, 'p3b_1': 0.66, 'p3b_4': 0.83, 'p3b_6': 0.88, 'p3b_8': 0.71, 'p2_9': 0.76, 'p1_5': 0.68,
                     'p1b_1': 0.83, 'p1b_5': 0.79, 'p1b_7': 0.76, 'cierre_1': 0.72}
TAIL_MAX_POR_FRASE = {'p4_4': 0.6, 'p2_6': 0.45, 'p1_2': 0.52, 'cierre_3': 0.61, 'intro_0': 0.39, 'intro_3': 0.41, 'intro_5': 0.6, 'p5_1': 0.57, 'p5_5': 0.58, 'p5b_7': 0.78, 'p5b_8': 0.49,
                      'p4_6': 0.56, 'p4_7': 0.78, 'p4b_0': 0.63, 'p4b_3': 0.7, 'p4b_6': 0.56, 'p4b_8': 0.53, 'p4b_10': 0.85,
                      'p3_1': 0.38, 'p3_2': 0.44, 'p3_3': 0.62, 'p3_4': 0.37, 'p3_5': 0.54, 'p3_6': 0.5, 'p3_7': 0.45, 'p3_8': 0.73,
                      'p3_10': 0.54, 'p3b_4': 0.74, 'p3b_8': 0.48, 'p3b_10': 0.39, 'p2_1': 0.39, 'p2_3': 0.53, 'p2_4': 0.53,
                      'p2_9': 0.47, 'p2b_0': 0.38, 'p2b_4': 0.56, 'p2b_5': 0.73, 'p2b_7': 0.65, 'p1_1': 0.59, 'p1_3': 0.46,
                      'p1_4': 0.75, 'p1_8': 0.6, 'p1b_1': 0.77, 'p1b_4': 0.48, 'p1b_5': 0.54, 'p1b_6': 0.42, 'p1b_7': 0.64,
                      'cierre_0': 0.63, 'cierre_1': 0.48, 'cierre_2': 0.53}

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Hay un personaje en Elden Ring que está contigo desde el primer minuto hasta casi el último. Te da el caballo, te sube de nivel, te lleva a la Mesa Redonda y se sienta a tu lado en cada lugar de gracia.",
        "Melina. La chica de la capucha. La que todo el mundo recuerda con cariño, porque es la única que nunca te pide nada raro.",
        "Bueno. Casi nada raro.",
        "Porque el día que por fin te dice lo que quiere, te lo pregunta así, con su voz tranquila de siempre: ¿estás preparado para cometer un pecado capital?",
        "Y no es una forma de hablar. Melina sabe perfectamente lo que te está pidiendo. Lo dice ella misma: sé que te estoy pidiendo que cometas un pecado capital.",
        "En el video de Ranni vimos que la favorita del público era la peor de todas. Hoy toca la otra favorita. La que nunca levanta la voz, la que nunca te traiciona, y la que, si lees con calma lo que dice, deja la lista más larga de todo el juego.",
        "Así que van las cinco peores atrocidades de Melina que ignoraste. Y te aviso desde ya: la número uno es una amenaza. Contra ti.",
        "Ponte cómodo, que este va largo. Y la próxima vez que subas de nivel, fíjate bien en lo que te dice mientras te toca el hombro.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Te eligió porque no tenías a nadie.",
        "Lo primero que hace Melina en el juego no es presentarse. Es mirarte. Cuando despiertas en el cementerio del principio, ella está ahí, montada en Torrentera, hablando de ti como si no estuvieras.",
        "Tranquilo, Torrentera, la suerte está de su lado. Lo encontramos aquí, después de todo. Alguien de su clase seguro que buscará el Círculo de Elden.",
        "Y entonces añade, en voz bajita: aunque vaya en contra del Orden Áureo.",
        "Fíjate en el orden de las cosas. Antes de saber tu nombre, antes de que tú sepas el suyo, ya ha decidido que vas a romper la ley. Y que le conviene.",
        "Luego llega el acuerdo. Te pregunta si has oído hablar de las doncellas del Dedo, las que guían a los Sinluz. Y te suelta, con toda la educación del mundo: pero a ti, me temo, no te acompaña ninguna.",
        "O sea, que estás solo. Y ella lo sabe. Por eso viene.",
        "Yo puedo hacer el papel de doncella, te dice. Convertiré tus runas en poder. Solo tienes que llevarme contigo hasta el pie del Árbol Áureo.",
        "Solo tienes que llevarme. Ese es el trato. Tú pones las piernas, las muertes y los jefes. Ella pone el viaje gratis hasta su casa.",
        "Y para que no te lo pienses mucho, te regala un anillo con un silbato, que llama a un corcel espectral. Torrentera te ha elegido, te dice. Trátalo con respeto.",
        "Al caballo le pide respeto para él. A ti no te pide nada. Tú ya estás contratado.",
    ]},
    {"id": "p5b", "frases": [
        "Y aquí viene lo bueno. Cuando sales de Necrolimbo, Melina te espera en un lugar de gracia y te pide perdón.",
        "Perdóname. Te he estado poniendo a prueba. Para ver si la gracia de verdad te guía, y si eres apto para el desafío que eso supone.",
        "Y remata con la frase más sincera que dice en todo el juego: Torrentera te tomó la medida desde el principio. Yo, en cambio, solo fingía.",
        "Solo fingía. Todo lo que hablaste con ella en Necrolimbo, toda la amabilidad, era un examen. Y el que te aprobó fue el caballo.",
        "Otra cosa que casi nadie se para a pensar. Cada vez que le pides subir de nivel, Melina te dice lo mismo: deja que pose mi mano sobre ti, solo un momento.",
        "Y luego, en voz baja: compártelos conmigo. Tus pensamientos. Tus ambiciones. Los principios que seguirías.",
        "Cada nivel que subiste en todo el juego, ella te estaba leyendo por dentro. Ochenta, cien, ciento cincuenta veces. Sabe lo que piensas mejor que tú.",
        "Y ella de sí misma no te cuenta nada. Lo admite: te he servido como doncella del Dedo, pero no puedo ofrecerte guía. No soy ninguna doncella. Mi propósito se perdió hace mucho.",
        "Y en cuanto llegas a la capital, al pie del Árbol Áureo, lo dice sin rodeos: mi más sincero agradecimiento por traerme hasta aquí. Aquí puedo gobernar mis propios movimientos. Y así, el acuerdo queda cumplido.",
        "Adiós. Te dejo a Torrentera y el poder de las runas. Y se va. Medio continente contigo, y se despide en tres frases, como quien se baja de un taxi.",
        "Pero tranquilo, que vuelve. Vuelve justo cuando te necesita otra vez. Y entonces te saluda así: hola de nuevo, viejo amigo.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. La hija que no te dijo de quién era hija.",
        "Melina habla mucho de su madre. Te dice que busca el propósito que le dio su madre, dentro del Árbol Áureo, hace mucho tiempo. Que nació al pie del árbol, donde su madre le dio ese propósito.",
        "Lo que nunca te dice es cómo se llama su madre. Ni una vez en todo el juego.",
        "Y no hace falta ser muy listo para sospecharlo. En los archivos del juego, el nombre interno de Melina es, literalmente, hija de Márika.",
        "Pero la confirmación llegó con la expansión. Cuando matas a Mésmer el Empalador, te llevas su yesca, y su descripción dice: Mésmer, al igual que su hermana menor, tenía una visión del fuego.",
        "Su hermana menor. La única persona del juego que tiene una visión del fuego es Melina. O sea que la chica de la capucha es hija de la reina Márika y hermana pequeña de Mésmer.",
        "Y ahora, con eso en la cabeza, acuérdate de lo que hace en las iglesias. Melina se ofrece a contarte los ecos de la reina Márika. Palabras de una reina que desapareció hace mucho, te dice. Como si hablara de una desconocida.",
        "En la Tercera Iglesia de Márika te recita esto: mi señor, y tus guerreros. Os despojo a cada uno de vuestra gracia. Con los ojos apagados, seréis expulsados de las Tierras Intermedias. Haréis la guerra en una tierra lejana, donde viviréis y moriréis.",
        "Esas son las palabras que te convirtieron en Sinluz. La orden que te sacó la luz de los ojos y te mandó a morir lejos.",
        "Y Melina, cuando termina, te dice: y bien, quizá te sirva en lugar de la guía de una doncella.",
        "Te lee el destierro que firmó su madre, y te lo vende como un consejo. Sin decirte que la que te desterró es su madre.",
    ]},
    {"id": "p4b", "frases": [
        "Y hay otro eco que da todavía más frío. Este te lo recita cerca de la capital: escuchadme, semidioses, mis hijos amados. Haced de vosotros lo que deseéis. Un señor, o un dios.",
        "Pero si no llegáis a ser nada en absoluto, seréis abandonados. Y no seréis más que sacrificios.",
        "Melina te está leyendo lo que su madre pensaba de sus hijos. De ella. Hijo que no sirve, sacrificio. Y te lo lee sin que le tiemble la voz.",
        "Ahora fíjate en cómo habla de las madres de los demás. Cuando le preguntas por Boc, el costurero, te dice: a veces lo veo llorar. Creo que echa de menos a su madre. Quiere que alguien le diga que es bonito.",
        "Y luego hace una pregunta que la retrata entera: ¿nacer de una madre significa comportarse así?",
        "Para ella, extrañar a una madre es raro. No lo entiende. Y en todo el juego, a la suya ni siquiera la nombra.",
        "Y en eso Mésmer y ella se parecen más de lo que parece. A los dos su madre les dio un propósito. El de Mésmer lo dice él mismo: todos los despojados de la gracia del oro hallarán la muerte, en el abrazo de la llama de Mésmer.",
        "Y su orbe cuenta que Mésmer despreciaba su propio fuego. Una y otra vez quiso librarse de él, pero siempre ardía.",
        "Ya hicimos un video entero de lo que Mésmer hizo con ese fuego en el Reino de las Sombras. La hermana pequeña tenía la misma visión. La diferencia es que ella no la desprecia. La abraza.",
        "Y hay un detalle más. Si invocas a Melina contra Morgott, en la capital, ella lanza un encantamiento secreto de la reina Márika. Un pequeño Árbol Áureo que cura a los aliados.",
        "Su descripción dice: solo la bondad del oro, sin el Orden. Márika bañó en oro la aldea de su hogar, sabiendo perfectamente que no quedaba nadie a quien curar. Ese es el truco que la hija aprendió de la madre: curar cuando ya no queda nadie.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. El pecado capital.",
        "Cuando por fin matas a Morgott y llegas a la puerta del Árbol Áureo, descubres que no puedes entrar. Un muro de espinas cierra el paso. Y entonces reaparece Melina.",
        "Hola de nuevo, viejo amigo. No pudiste entrar en el Árbol Áureo, ¿verdad? Las espinas son impenetrables. La única forma de convertirte en Señor del Círculo es atravesarlas.",
        "Y la solución que propone es esta: quiero que emprendas un nuevo viaje conmigo. Hasta la llama de la perdición, muy por encima de las nubes, en los picos nevados de los gigantes. Así podré prenderle fuego al Árbol Áureo.",
        "Prenderle fuego al Árbol Áureo. El árbol que gobierna la vida de todo el mundo. El que se ve desde cualquier punto del mapa. El árbol a cuyo pie ella misma nació.",
        "Y la llama que quiere usar no es una llama cualquiera. Un encantamiento lo explica: la llama de los gigantes es la llama de la perdición, capaz de quemar el Árbol Áureo. Por eso, tras la guerra contra los gigantes, su fuego fue sellado y vigilado.",
        "Ahora acuérdate de otro eco que te leyó Melina, en la Primera Iglesia de Márika: pasad a los gigantes por la espada, y confinad la llama en lo alto del monte. Que empiece una nueva época, una época resplandeciente de vida.",
        "Ese fue el primer gran acto de su madre: una guerra entera para apagar ese fuego y que empezara la era del Árbol Áureo. Y la hija te lleva de la mano a encenderlo otra vez.",
        "Para que funcione hace falta algo más, y te lo explica Enia, la lectora de dedos de la Mesa Redonda: para que la llama queme el Árbol Áureo, se necesita un sacrificio. El de alguien que tenga una visión de la llama, y que pueda guiarte hasta la Runa de la Muerte.",
        "Alguien con una visión de la llama. Ya sabes quién es. Y Melina te lo confirma: no te preocupes por la yesca. Yo me encargo de eso.",
        "Y luego te pide perdón por adelantado: lo sé. Te estoy pidiendo que cometas un pecado capital. Pero debe hacerse para llegar al camino de más allá. Y ese es el camino que yo quiero recorrer.",
    ]},
    {"id": "p3b", "frases": [
        "Ese es el camino que ella quiere. No el tuyo. Y por si te quedaba alguna duda, en el valle nevado de camino a los picos, te lo deja clarísimo.",
        "Mi propósito me lo dio mi madre. Pero ahora actúo por voluntad propia. He puesto mi corazón en el mundo que yo quiero, sin importar los designios de mi madre.",
        "Y añade: no permitiré que nadie hable mal de eso. Ni siquiera tú.",
        "Ni siquiera tú. Después de todo el viaje juntos, la conversación se termina ahí. Ella ya decidió cómo debe ser el mundo, y tu opinión no entra en el acuerdo.",
        "Cuando por fin llegas a la Forja de los gigantes, Melina te pregunta una última vez. He observado las Tierras Intermedias durante mucho tiempo. Este mundo necesita ser reparado. Y la muerte, indiscriminada. ¿Estás preparado para cometer un pecado capital?",
        "Le dices que sí. Y entonces te toma de la mano, como cuando subías de nivel. Y te quedas dormido. Ni siquiera te deja verlo.",
        "Mientras duermes, ella se convierte en la yesca. Oh, Árbol Áureo, arderás. Arde por el nuevo señor. Gracias por traerme hasta aquí. Quien camina junto a la llama algún día se encontrará con el camino de la muerte destinada. Adiós.",
        "Y despiertas en Farum Azula, la ciudad en ruinas, al otro lado del cielo, sin caballo y sin compañera. Otra vez sin doncella.",
        "Y cuando vuelves a la capital, lo que encuentras es esto. Leyndell, la capital de ceniza. La ciudad al pie del árbol donde nació Melina, enterrada bajo una capa tan gruesa de ceniza que solo asoman los edificios más altos.",
        "Enia lo resume sin dramatismo: la Runa de la Muerte ha sido liberada, y las Tierras Intermedias están cubiertas por el oscuro destino de la Muerte.",
        "Melina quemó el árbol de su madre, enterró su ciudad natal en ceniza, y te dejó dormido en el suelo para que no vieras cómo lo hacía. Y aun así, es la número tres.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Muerte para todos.",
        "Vuelve un momento a esa frase de la Forja, porque casi todo el mundo la escucha y sigue de largo: este mundo necesita ser reparado. Y la muerte, indiscriminada.",
        "Indiscriminada. Para todos. Sin excepciones. Eso es lo que Melina quiere devolverle al mundo.",
        "Para entender lo grave que es, hay que saber qué es la Runa de la Muerte. Enia lo cuenta así: la Runa de la Muerte tiene dos nombres. El otro es muerte destinada. La sombra prohibida, arrancada del Orden Áureo en su creación.",
        "Arrancada en su creación. Cuando Márika fundó su Orden, lo primero que hizo fue sacar la muerte del Círculo de Elden. Y se la dio a guardar a Maliketh, la Hoja Negra, que la selló dentro de su espada.",
        "En el video de Ranni vimos lo que pasó cuando alguien robó un trocito de esa muerte: una sola noche, y el semidiós más querido del mundo murió y se quedó a medias para siempre. Eso fue con un fragmento.",
        "Melina no quiere un fragmento. Quiere la runa entera, suelta, para todo el mundo. Y para soltarla, alguien tiene que matar a Maliketh, su guardián.",
        "Adivina quién. Melina te deja dormido en Farum Azula y ya no está. El que tiene que recorrerla, pelear contra la bestia y romperle la espada, eres tú.",
        "Es el patrón de todo el juego. Ella decide adónde se va, y tú haces el trabajo sucio. Con Godrick, con Morgott, y ahora con el guardián de la muerte.",
        "Y mientras peleas contra Maliketh, ten en cuenta una cosa. La sombra que guarda esa espada, la que podía matar dioses, es exactamente lo que la chica de la capucha te mandó a liberar.",
    ]},
    {"id": "p2b", "frases": [
        "Y la propia arma de Melina te lo anunciaba desde el principio. Es una daga que puedes encontrar escondida en un cuarto secreto de las Tierras Prohibidas, y se llama la Hoja de la invocación.",
        "Su descripción dice: daga entregada a quien partió hace mucho para cumplir con su deber. El poder de su antigua dueña, la doncella enyescada, aún se nota.",
        "Y debajo, otra vez, la misma frase: quien camina junto a la llama algún día se encontrará con el camino de la muerte destinada.",
        "Su deber. Desde mucho antes de conocerte, ese era el plan. No buscaba un compañero. Buscaba a alguien que la llevara hasta la llama y luego hasta la muerte.",
        "Y fíjate en el detalle más raro de esa daga. La misma hoja la lleva Poliána, una de las hermanas de Millicent, las valquirias de la putrefacción. Si viste el video de Malenia, ya sabes de qué familia te hablo.",
        "Ahora, para ser justos, Melina también dice cosas bonitas. Cuando te acercas a la llama frenética, te suplica: la vida perdura. Los nacimientos continúan. ¿No hay belleza en eso?",
        "Y suena precioso. Hasta que te das cuenta de que la misma persona que defiende los nacimientos es la que te pidió devolverle al mundo la muerte indiscriminada.",
        "En su cabeza no hay contradicción. Que todo nazca, y que todo muera. Y que nadie se libre, ni siquiera los dioses. Es un mundo más justo, sí. Pero es un mundo que decide ella.",
        "Y de esa misma escena, la de la llama frenética, sale la número uno. Porque Melina tiene un límite. Y cuando lo cruzas, deja de ser tu compañera.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. La promesa de matarte.",
        "Debajo de la capital, en lo más hondo, hay una puerta sellada que lleva a los Tres Dedos y a la llama frenética. La llama del caos, la que lo quema todo.",
        "Melina no quiere que vayas. Te lo pide una vez. Y otra. Y otra. Si pretendes reclamar esa llama, te pido que desistas. Es el caos, que devora la vida y el pensamiento sin fin. Por favor, deja en paz la llama frenética.",
        "Y en una de esas veces se le escapa algo: yo me encargo de la yesca. Es un propósito que elijo cumplir. O sea, prefiere quemarse ella antes que dejarte esa llama a ti.",
        "Hasta aquí, parece una buena amiga. El problema es lo que pasa si no le haces caso. Si bajas, te arrodillas ante los Tres Dedos y aceptas la llama, la próxima vez que descansas en un lugar de gracia, Melina aparece por última vez.",
        "Has heredado la llama frenética. Qué lástima. Ya no eres digno. Nuestro acuerdo termina aquí.",
        "Pero recuerda. Si te alzas como Señor del Caos, te mataré. Tan seguro como que la noche sigue al día.",
        "Y la frase siguiente es la que lo cambia todo: ese es mi deber, por haberte concedido el poder de las runas.",
        "Por haberte concedido el poder de las runas. Cada nivel que te subió. Cada vez que te puso la mano en el hombro. Todo eso no era un regalo. Era un préstamo. Y la letra pequeña del acuerdo decía que, si no le gustaba en qué te convertías, te lo cobraba con tu vida.",
        "Y luego se despide. Adiós, mi compañero. Adiós, Torrentera.",
    ]},
    {"id": "p1b", "frases": [
        "Y cumple. Si llegas hasta el final como Señor de la Llama Frenética, después de los créditos hay una escena que mucha gente nunca vio.",
        "Todo es ceniza. Se oye un coro de silbidos, como el silbato del caballo, y Melina aparece, cambiada. Recoge del suelo, entre las cenizas, el anillo del silbato. El de Torrentera, que ha ardido con todo lo demás.",
        "Y por primera vez abre el ojo izquierdo. Ese ojo que tuvo cerrado todo el juego, con un sello encima. Y es de color violeta.",
        "Y te dice: Señor de la Llama Frenética. Te buscaré, tan lejos como viajes. Para darte lo que es tuyo. La muerte destinada.",
        "Ahora vuelve a la frase de su daga. Quien camina junto a la llama algún día se encontrará con el camino de la muerte destinada. En el final normal, la que camina con la llama es ella. En este final, el que camina con la llama eres tú. Y la muerte que te espera, es Melina.",
        "Y aquí entra la teoría favorita de la comunidad. Hubo una reina antigua, la Reina del Ojo Velado, una Empírea elegida por los Dedos que manejaba las llamas negras de la muerte de los dioses, hasta que Maliketh la derrotó. Y tenía un ojo especial.",
        "El juego nunca dice que sean la misma persona. Pero una hija de Márika con un ojo sellado, que acaba con el poder de la muerte destinada en la mano, se parece demasiado como para ser casualidad.",
        "Así que la chica que te acompañó todo el juego, la que te subía de nivel con la mano en el hombro, guardaba debajo de la capucha la cara de la muerte. Y tú le contabas tus ambiciones cada vez que subías de nivel.",
        "Su última frase en ese final no es para el mundo, ni para su madre, ni para el caballo que murió. Es para ti. Y es una promesa.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. La compañera perfecta te eligió porque estabas solo, te puso a prueba fingiendo, te ocultó de quién era hija, quemó el árbol de su madre, enterró su propia ciudad en ceniza, le devolvió la muerte a todo el mundo, y te prometió matarte si no le gustaba el rey que eras.",
        "Y lo más inquietante es que, de todos los personajes del juego, Melina es la única que nunca te mintió. Te dijo desde el principio que te estaba pidiendo un pecado capital. Simplemente, nunca te preguntó si querías.",
        "Ahora te toca a ti: quién fue peor de las dos favoritas. Ranni, que te usó para matar a un dios, o Melina, que te usó para soltar la muerte. Te leo en los comentarios, que los leo todos, de verdad.",
        "Y si quieres al resto de la familia, en el canal tienes las atrocidades de Márika y Radagon, de Miquella y Malenia, y la de Ranni. Y el genocidio de su hermano Mésmer. Es una familia muy unida. Sobre todo para quemar cosas.",
        "Y la próxima vez que alguien te diga que solo quiere acompañarte, pregúntale hasta dónde. Y qué piensa quemar al llegar.",
    ]},
]
