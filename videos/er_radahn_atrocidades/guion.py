# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Radahn QUE IGNORASTE» (28-oct-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md (formato largo, el ganador es Miquella ~20 min
×18; el usuario pidió AL MENOS 22 min el 28-oct-2026). Tema pedido en los comentarios (@zoharysakiyamablue471 ♥4, @ConkerLord22).
Cada puesto va partido en dos escenas (pN / pNb), como Miquella, Malenia y Melina.
Investigación: investigacion.md (wikitexto de eldenring.fandom.com en inglés y español, 28-oct-2026).
NO REPITE lo ya contado en Miquella (Yelmo del joven león, «Miquella desea revivirla», el recuerdo «hermano mayor…», Luz de Miquella)
ni en Malenia (Gideon «conteniendo la putrefacción con fuego», «el festival es un funeral»): aquí se cuenta desde el lado de Radahn
con las citas que el canal no ha usado (Ansbach «esos restos no te pertenecen», «Rada…», las lanzas, Sellen inmortal, el japonés de Jerren,
«mi leal espada y campeón del festival», el monólogo cortado, el parche 1.14).
Nombre: «el Azote Estelar» (como el video de Malenia; la wiki es da «Azotestelar» para Latinoamérica; Miquella dijo «Plaga Estelar»).
TEORÍA dicha como teoría: si Radahn aceptó ser consorte (las dos posturas, comentario de @dinobotstrafe7963 ♥8), festivales anteriores
(como pregunta). EVITAR: que se comió a su caballo, que se dejó ganar contra Malenia, que detuvo las estrellas para frenar a Ranni,
que la flor destruyó Sellia, que la nota del 1.14 nombra a Radahn.
"""

TITULO = "Las 5 peores atrocidades de Radahn QUE IGNORASTE"
ARCHIVO = "er_radahn_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# 22-oct: nombre propio que Whisper escriba distinto = error REAL, regenerar. 28-oct: quejas en los comentarios por «Mojé»,
# «Miqueya» y «Micuela». «Mikuéla» (la de los videos anteriores) SUENA «Mi-cue-la» = la queja: ahora «Mikéla»; «Mog»
# salía a veces «moj/mok» → «Móg». Mohg y Miquella se revisan frase a frase en Whisper.
FONETICA = {
    "Miquella": "Mikéla", "Malenia": "Malénia", "Radahn": "Rádan", "Radagon": "Rádagon", "Godfrey": "Gódfri",
    "Mohg": "Móg", "Messmer": "Mésmer", "Morgott": "Mórgot", "Leyndell": "Léindel", "Rennala": "Renála",
    "Ranni": "Ráni", "Millicent": "Mílisent", "Limgrave": "Límgreiv", "Elden Ring": "Élden Ring", "Elden": "Élden",
    "Jerren": "Yérren", "Leonard": "Léonard", "Sellia": "Sélia", "Sellen": "Sélen", "Caelid": "Kéilid", "Iji": "Íyi",
    "Blaidd": "Bleid", "Ansbach": "Ánsbaj", "Freyja": "Fréya", "Aeonia": "Eónia", "Enir-Ilim": "Enír Ilím",
    "Gideon": "Guídeon", "Finlay": "Fínlei", "Nokron": "Nókron", "Raya Lucaria": "Ráya Lucária", "Gael": "Gáel",
    "Miyazaki": "Miyasáki", "Godrick": "Gódrik", "Maknarth": "Máknarz", "Conker": "Cónker",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; el audio del juego va donde conviene oírlo (regla del 26-oct-2026)
    ambiente_por={"scene-021": .6, "scene-024": .6, "scene-095": .7},   # lluvia de flechas, rugido, la estrella que cae: CON su audio; la OST se aparta ahí
    recorte_por={f"scene-{n:03d}": 0.09 for n in (9, 15, 18, 22, 59, 73, 78, 95, 99, 104, 106, 126, 128, 133, 134, 135, 140, 142, 147, 155, 161, 162, 163, 166, 170)},   # firma «SHIRRAKO»
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar"]),   # heredado de Melina
)

# 28-oct: 1.ª selección 27/118, casi todo falsas alarmas (colas de Chatterbox, «Radan», «Celia» por Sellia, «Blade» por Blaidd,
# «Yeren», cifras en número, «Conquerlord»). Tomas con palabras cambiadas → voz/_descartes; elegida una por frase (las demás en
# voz/_descartes/no_elegidas) y su umbral fijado aquí.
CER_MAX_POR_FRASE = {'p5b_3': 0.02, 'p1_8': 0.027, 'p1_6': 0.015, 'p5_6': 0.026, 'intro_0': 0.017, 'intro_1': 0.05, 'intro_5': 0.015, 'p5_1': 0.022, 'p5_5': 0.016, 'p5b_0': 0.018, 'p5b_5': 0.026, 'p5b_10': 0.03, 'p4_0': 0.03, 'p4_6': 0.025, 'p4_8': 0.022, 'p4b_1': 0.015, 'p4b_9': 0.015, 'p3_6': 0.037, 'p3_8': 0.026, 'p3b_1': 0.021, 'p3b_5': 0.025, 'p3b_6': 0.016, 'p3b_8': 0.018, 'p2_1': 0.018, 'p2_2': 0.022, 'p2_5': 0.023, 'p2_6': 0.02, 'p2b_2': 0.018, 'p2b_4': 0.014, 'p2b_5': 0.038, 'p2b_6': 0.02, 'p1_3': 0.017, 'p1_4': 0.014, 'p1_9': 0.018, 'p1b_0': 0.033, 'p1b_2': 0.025, 'p1b_3': 0.028, 'p1b_4': 0.028, 'p1b_6': 0.02, 'p1b_8': 0.018, 'cierre_3': 0.045, 'cierre_4': 0.016, 'cierre_5': 0.04}
GAP_MAX_POR_FRASE = {'p5_6': 0.97, 'p5_2': 0.69, 'p5_3': 0.75, 'p5b_0': 0.72, 'p5b_5': 0.71, 'p5b_10': 0.67, 'p4_3': 0.83, 'p4_9': 0.75, 'p4b_2': 0.72, 'p4b_3': 0.67, 'p4b_7': 0.71, 'p3_1': 0.7, 'p3_3': 0.68, 'p3b_4': 0.78, 'p3b_8': 0.73, 'p3b_9': 0.7, 'p2_3': 0.79, 'p2_4': 0.69, 'p2_6': 0.75, 'p2b_4': 0.73, 'p2b_6': 0.69, 'p2b_7': 0.78, 'p1_2': 0.72, 'p1b_3': 0.69, 'p1b_7': 0.79, 'cierre_4': 0.69, 'cierre_5': 0.87}
TAIL_MAX_POR_FRASE = {'p5b_3': 0.67, 'p1_8': 0.44, 'p1_6': 0.73, 'p5_6': 0.72, 'p3_5': 0.5, 'intro_0': 0.42, 'intro_2': 0.49, 'intro_5': 0.43, 'p5_1': 0.61, 'p5_3': 0.57, 'p5_4': 0.48, 'p5_5': 0.44, 'p5_7': 0.49, 'p5_9': 0.45, 'p5b_2': 0.56, 'p5b_5': 0.48, 'p5b_8': 0.53, 'p4_1': 0.48, 'p4_2': 0.47, 'p4_3': 0.55, 'p4_4': 0.54, 'p4_6': 0.44, 'p4_8': 0.45, 'p4_9': 0.52, 'p4b_0': 0.41, 'p4b_1': 0.6, 'p4b_2': 0.61, 'p4b_3': 0.52, 'p4b_5': 0.48, 'p4b_6': 0.43, 'p4b_8': 0.45, 'p4b_9': 0.39, 'p3_1': 0.58, 'p3_2': 0.45, 'p3_3': 0.69, 'p3_7': 0.74, 'p3_9': 0.71, 'p3b_1': 0.5, 'p3b_3': 0.39, 'p3b_4': 0.55, 'p3b_5': 0.53, 'p3b_7': 0.49, 'p3b_8': 0.5, 'p2_1': 0.63, 'p2_2': 0.53, 'p2_4': 0.59, 'p2_5': 0.54, 'p2_6': 0.54, 'p2_7': 0.59, 'p2_10': 0.56, 'p2b_0': 0.43, 'p2b_1': 0.48, 'p2b_3': 0.5, 'p2b_4': 0.46, 'p2b_5': 0.49, 'p2b_6': 0.72, 'p2b_7': 0.57, 'p2b_10': 0.47, 'p1_1': 0.62, 'p1_2': 0.51, 'p1_3': 0.56, 'p1_4': 0.4, 'p1_5': 0.54, 'p1_9': 0.61, 'p1b_0': 0.43, 'p1b_1': 0.51, 'p1b_2': 0.61, 'p1b_3': 0.54, 'p1b_4': 0.63, 'p1b_6': 0.52, 'p1b_7': 0.68, 'p1b_9': 0.68, 'cierre_0': 0.72, 'cierre_1': 0.4, 'cierre_2': 0.56, 'cierre_4': 0.46, 'cierre_6': 0.7}

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En el video de Miquella, alguien nos dejó este comentario: el día que publiques las atrocidades de Radahn, te vamos a caer encima. Y luego, para que no me asustara: broma, bro.",
        "Pues ese día es hoy. Y no fue el único. Conker Lord también nos pidió a Radahn. Y a Morgott, que ya está apuntado.",
        "Radahn es, probablemente, el jefe más querido de Elden Ring. El general que detuvo las estrellas con sus propias manos. El que aguantó a Malenia hasta el final. El que tiene un festival entero en su honor, con campeones de medio continente que vienen a despedirlo como se merece.",
        "Hasta Miyazaki lo ha puesto entre sus jefes favoritos. Y luego volvió en la expansión, más grande, más rápido, y con Miquella a su lado.",
        "Pero si lees con calma lo que dicen de él los que lo conocieron, su mejor amigo, su caballera más fiel, el herrero que lo admiraba, el retrato cambia mucho.",
        "Así que van las cinco peores atrocidades de Radahn que ignoraste. Y aviso: un par de ellas ya las rozamos en los videos de Malenia y de Miquella. Hoy las vemos desde el otro lado. Desde el suyo.",
        "Ponte cómodo, que este es el más largo del canal. Y la próxima vez que te llueva una flecha gigante en las dunas, fíjate bien de qué está hecha.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El banquete del general.",
        "Antes de pelear con Radahn tienes que pasar por el Castillo de la Melena Roja, al sur de Caelid. Ahí te recibe Jerren, el viejo del sombrero raro, el castellano, y te cuenta cómo está su general.",
        "El general Radahn está condenado a vagar para siempre. La putrefacción escarlata de Malenia lo devora por dentro, y hace mucho que perdió el juicio.",
        "Hasta ahí, una tragedia. Y entonces suelta la frase que casi todo el mundo se salta, porque quiere llegar ya al jefe: ahora reúne los cadáveres de antiguos amigos y enemigos, y se atiborra de ellos como un perro. Aullándole al cielo.",
        "Como un perro. Lo dice su mejor amigo. Y lo repite más tarde, por si no lo oíste: el general sigue ahí, incluso ahora. Sin juicio, devorando cadáveres. Y aullándole al cielo.",
        "Amigos y enemigos. En las dunas de Caelid solo quedaron dos ejércitos: los Melena Roja, que eran sus propios soldados, y los caballeros de Malenia. Radahn no distingue. Se come a los dos.",
        "En los comentarios del video de Malenia, Mister Jesús Pain bromeaba: Malenia, nunca conociste la derrota, pero si no fuera por la caballera que te cargó hasta el Árbol Hierático, Radahn te habría devorado. Y no le falta razón. Esa caballera, Finlay, la cargó dormida desde Caelid, sola, abriéndose paso entre enemigos todo el camino. Pero a muchos de sus caballeros nadie los cargó. Se quedaron en las dunas. Con él.",
        "Y no solo se los come. Fíjate en la lluvia de flechas gigantes que te cae en cuanto entras a las dunas. Si recoges una de la arena, su descripción dice: flechas grandes que usó el general Radahn durante el festival del combate. En realidad, son las muchas lanzas con las que lo atravesaron los Caballeros Imputrescibles.",
        "O sea, los caballeros de Malenia lo llenaron de lanzas, y él te las dispara a ti. Usa como munición a los que intentaron matarlo.",
        "Y si te fijas en sus pies durante la pelea, verás que la putrefacción se los ha comido. El semidiós más fuerte de la Devastación, caminando sobre unos pies podridos por la arena, buscando qué comer.",
    ]},
    {"id": "p5b", "frases": [
        "¿Y cómo se acaba con un semidiós así? Jerren tiene la respuesta: con una fiesta.",
        "Esta fortaleza solo alberga a los vencidos, te dice. Pero cuando las estrellas se alinean, celebramos. Cuando las estrellas se alinean, se declara el festival.",
        "Celebramos. En presente. Como algo que pasa cada cierto tiempo. El juego nunca dice que hubiera festivales antes del tuyo. Pero si los hubo, y los campeones perdieron, ya sabes dónde acabaron. En las dunas. Con el general.",
        "¿Y por qué lo organiza Jerren, que lo quiere tanto? Por un juramento. Su capucha lo cuenta: Jerren sirvió al general Radahn como comandante invitado, y se dice que se juraron mutuamente una muerte honorable.",
        "Su armadura añade que Jerren era un nómada que nunca se había atado a nada. Y que por primera vez, quedó atado por un juramento de honor. Atado a matar a su amigo.",
        "Y no es solo cosa de Jerren. En el Fuerte Gael, al oeste de Caelid, hay un alma varada, el espíritu de un soldado muerto. Su último deseo es este: convoquen el festival de la guerra. Honren al general Radahn con la gloria de un guerrero. Está en tus manos, Sir Jerren.",
        "El último deseo de su propio ejército es que alguien mate a su general. Eso te dice todo de cómo estaba Radahn.",
        "Cuando por fin lo matas, Jerren lo despide así en la versión en inglés: pudriéndose, y lisiado por la locura, todo lo que quería era una muerte honorable.",
        "Pero en el japonés original no dice eso. Dice algo como: fue, sin duda, un final mucho más honorable que pudrirse y enloquecer. No es lo que Radahn quería. Es lo que su amigo decidió que era mejor para él.",
        "Porque Radahn nunca dice nada. Literalmente. Es el único portador de una Gran Runa de todo el juego que no tiene ni una sola línea de diálogo, ni una escena de presentación.",
        "Y Blaidd, que pelea a tu lado en el festival, lo resume con cara de asco: qué forma tan enferma de pelear, ¿eh? La gloria del choque se la reparten Radahn y tú. Media docena de campeones contra un general podrido. Bonito festival.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Salvó Sellia. Y luego la pudrió.",
        "Para entender esta hay que volver a su juventud. Su recuerdo cuenta que el general conocido como el León Rojo aprendió los poderes gravitacionales en Sellia, de joven. Y la razón es preciosa: todo para no tener que abandonar nunca a su querido, aunque escuálido, corcel.",
        "El caballo se llama Leonard. Y es enano. Radahn aprendió a manejar la gravedad, la magia con la que más tarde aplastó estrellas, para poder seguir montando un caballito flaco sin partirle la espalda.",
        "Y no era su única mascota. En la primera versión del juego, el talismán del gato de cola larga decía que era la mascota querida del general Radahn. Un parche posterior lo cambió, y ahora es la gata de una fábula de Raya Lucaria. Al semidiós más fuerte le borraron el gato.",
        "La magia se la enseñó un maestro de piel de piedra, de los señores alabastrinos. Con él estudiaba también Gaius, el del jabalí, que luego conocerías en la expansión. Uno de sus hechizos lo dice: Gaius y Radahn fueron buenos rivales en su juventud.",
        "Y uno de los hechizos de Radahn guarda una frase suya de esa época: te agradezco tu tutela, maestro, porque ahora puedo desafiar a las estrellas.",
        "Y las desafió. Junto a un puente de Caelid hay un monumento con una espada clavada que dice: el conflicto del Azote de las Estrellas. Radahn mantiene Sellia segura. Un hombre que se alza para hacer pedazos las estrellas.",
        "Las estrellas caían sobre Sellia, el pueblo donde aprendió su magia, y él solo las detuvo. Por eso lo llaman el Azote Estelar.",
        "Ahora busca otro monumento, un poco más al norte, junto al camino de Caelid. Dice: la batalla de Aeonia. Radahn y Malenia en punto muerto. Y entonces florece la putrefacción escarlata.",
        "Y abre el mapa de Caelid y lee la descripción. Las vastas tierras de Caelid, conocidas por haber sido escenario del último combate entre el general Radahn y Malenia, la Espada de Miquella, han quedado devastadas por la putrefacción.",
    ]},
    {"id": "p4b", "frases": [
        "¿Y dónde fue ese último combate? Mira el mapa. El pantano de Aeonia, donde floreció la flor de Malenia, está a un paso del pueblo que él había salvado.",
        "Un alma varada de Caelid lo cuenta como puede: se pudre. Todo se pudre de escarlata. La tierra misma sobre la que descansa Caelid, y Sellia, el pueblo de la hechicería. El fin está cerca, para todos.",
        "El pueblo que lo convirtió en héroe es el que su último duelo pudrió. Y él no fue un espectador. Millicent lo dice de Malenia: el orgullo que abandonó para estar a la altura de Radahn. Para igualarlo, Malenia tuvo que soltar la flor. Él la empujó hasta ahí.",
        "Y luego está su ejército. Los soldados de la Melena Roja quemaron el emblema de sus propias armaduras. La armadura lo explica: cuando la putrefacción de Malenia los derrotó, los caballeros quemaron el blasón del pecho izquierdo para mostrar su determinación.",
        "Y debajo, la frase que llevan grabada: ay, mi hogar, no volveré a verte. Nuestro deber es quedarnos aquí, como un baluarte contra la plaga.",
        "Esos soldados con antorchas que te atacan en el Fuerte Gael, los que patrullan los puentes de Caelid, no son enemigos cualquiera. Son el ejército que su general dejó atrás, quemando una enfermedad que nunca se acaba.",
        "Y Jerren, el mismo del festival, se quedó atado a ese castillo mientras Radahn viviera. Cuando lo matas, te lo dice aliviado: por fin, mi trabajo ha terminado. Ya no estoy atado a esta fortaleza.",
        "Y luego está Freyja. La mejor caballera que tuvo, a la que él mismo reclutó después de verla pelear como gladiadora. En la expansión te cuenta lo que le pasó en Aeonia.",
        "Hace mucho, la putrefacción escarlata me alcanzó en el pantano de Aeonia. Inmóvil, con fiebre y con mucho dolor, me resigné por completo a morir. Me dejaron atrás. Y solo Miquella el Bondadoso fue capaz de venir a buscarme.",
        "Me dejaron atrás. Su general no volvió por ella. El que volvió fue Miquella. Y ya sabes lo que hace Miquella con la gente que recoge del suelo. Guárdate ese nombre, que vuelve en la número dos.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Congeló el destino de todos.",
        "Su talismán, la reliquia del Azote de las Estrellas, lo cuenta así: el más poderoso de los héroes semidioses se enfrentó solo a las estrellas que caían, y las aplastó. Su conquista selló el destino mismo de las estrellas.",
        "Selló el destino de las estrellas. Suena a hazaña. Pero en las Tierras Intermedias, las estrellas no son decoración. Son el destino de una familia entera. La suya.",
        "Iji, el herrero gigante de Liurnia, te lo explica: el destino de la familia real Caria lo guían las estrellas. Igual que el de la señora Ranni, primera heredera de la línea real. Pero el general Radahn es el conquistador de las estrellas. Se alzó contra las constelaciones y detuvo su movimiento con una victoria aplastante.",
        "Y remata: así que, si el general Radahn fuera derrotado, las estrellas volverían a moverse. Y también el destino de la señora Ranni.",
        "Ranni es su hermana. Hijos de los mismos padres: Rennala, la reina de la Luna Llena, y Radagon. Y durante toda la Devastación, el destino de su hermana estuvo congelado, porque él no se dejaba matar.",
        "Blaidd, la sombra de Ranni, lo dice sin rodeos: así que el destino de Ranni lo mantiene inmóvil el Azote Estelar.",
        "¿Lo hizo a propósito? El juego nunca lo dice. Ranni nunca lo culpa. Lo único que consta es el efecto: mientras él viviera, su hermana no podía avanzar. Y por eso, en la historia de Ranni, alguien tiene que matarlo. Ese alguien eres tú.",
        "Y fíjate en lo que pasa en cuanto cae. Blaidd lo ve en directo: una estrella cayendo, ante nuestros ojos. No me explico cómo Radahn sujetaba algo de esa escala.",
        "Una estrella entera se estrella en Necrolimbo y abre un cráter en el suelo. Iji te manda allí: baja bajo tierra, donde la estrella cayó en Necrolimbo. Y debajo está Nokron, la ciudad eterna, y el camino hacia el destino de Ranni.",
    ]},
    {"id": "p3b", "frases": [
        "Pero el destino congelado no era solo el de Ranni. Hay un detalle que casi nadie conecta, y está en la misma conversación.",
        "Cuando matas a Radahn, Iji te dice esto: con las estrellas del destino otra vez en marcha, cierta hechicera pierde su inmortalidad. Por fin podremos librarnos de una vieja mala hierba de los Caria.",
        "Esa hechicera es Sellen. La maestra que te enseña magia en Necrolimbo, la de la voz amable debajo de la capucha. Y Jerren, el mismo viejo del festival, cuenta quién es en realidad.",
        "Obsesionada por la corriente primigenia, incontables hechiceros cayeron por su mano. La maga más peligrosa de toda la historia de la academia de Raya Lucaria.",
        "Incontables hechiceros. Y mientras Radahn tuviera las estrellas quietas, Sellen no podía morir. El héroe que salvó Sellia mantenía viva, quisiera o no, a la peor asesina de magos de la academia.",
        "Y por eso el festival le importa tanto a Jerren. Iji lo dice clarísimo: ha llegado la hora de recordarle una vieja promesa. Jerren había prometido a los Caria matar a Sellen. Y no podía cumplirlo hasta que muriera su amigo.",
        "En cuanto Radahn cae, el viejo deja el castillo y se va directo a las ruinas de la Perdición de la Bruja, a cazarla. Ya no es Jerren, el castellano. Es Jerren, el cazador de brujas.",
        "Piénsalo. Un solo hombre agarraba el cielo, y con él agarraba a su hermana, a toda una familia real, a una asesina inmortal y al juramento de su mejor amigo. Toda la Devastación esperando a que alguien lo soltara.",
        "Y cuando lo sueltas, cae una estrella del tamaño de una montaña. Blaidd tenía razón. Nadie sabe cómo sujetaba algo de esa escala. Ni qué más tenía agarrado.",
        "Ya contamos en el video de Ranni lo que hizo ella con su destino una vez libre. Lo que no contamos es que la puerta se la abriste tú, matando a su hermano en una fiesta.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. El juramento.",
        "En el video de Miquella vimos la propuesta de matrimonio desde el lado del niño. Hoy, desde el lado de Radahn. Y empieza con una pregunta incómoda: ¿dijo que sí?",
        "El recuerdo de la expansión lo cuenta así: en su infancia, Miquella ya veía en Radahn a un señor. Su fuerza y su bondad contrastaban con su propia alma afligida. Y así Miquella formuló su más sincero deseo: que Radahn fuera algún día su rey consorte.",
        "En japonés, esa última línea es todavía más clara. Es un ruego: por favor, sé mi rey.",
        "Y en la Puerta de la Divinidad, el recuerdo del niño tiene una palabra que casi nadie escucha. Si cumplimos nuestra parte del juramento, prométeme que serás mi consorte.",
        "Nuestra parte. En plural. Miquella no habla solo de él. Habla de un nosotros. ¿Y quién estaba siempre con Miquella? Su hermana. La que el juego llama, literalmente, la Espada de Miquella.",
        "Y fue justo ella la que fue a buscar a Radahn a Caelid. Su espada fue la que le susurró al oído, en mitad de la batalla de Aeonia, el famoso mensaje del consorte prometido que ya contamos en el video de Miquella.",
        "Freyja confirma que el juramento existía, y que era con Radahn: Miquella el Bondadoso me habló del juramento que hizo una vez con el general Radahn. Y es aquí donde se cumplirá. Soy una Melena Roja. Debo saber la naturaleza de ese juramento.",
        "Ni siquiera su caballera más fiel sabía qué había prometido su general. Tuvo que ir hasta la Fortaleza Sombría a leer unas losas para enterarse.",
        "Y en esa misma fortaleza está el pergamino del rito secreto: un señor anunciará el regreso de un dios, y el alma del señor requerirá un recipiente.",
        "Un alma que necesita un recipiente es un alma sin cuerpo. Para que el plan funcionara, Radahn tenía que estar muerto. Y ahí todo encaja de una forma muy fea.",
    ]},
    {"id": "p2b", "frases": [
        "Cuando empieza la pelea final de la expansión, Miquella dice esto: mi leal espada. Y campeón del festival. Las hazañas de ambos se cantarán por siempre. Ahora el juramento se cumplirá, y el alma de mi hermano mayor volverá. Para que pueda ser mi consorte.",
        "Le da las gracias a dos personas. A su leal espada, que todo apunta a que es Malenia, la que pudrió a Radahn en Aeonia. Y al campeón del festival. O sea, a ti, que lo mataste.",
        "Para Miquella, pudrirlo y matarlo fueron dos favores. Dos pasos del mismo plan.",
        "Ahora, aquí entra un comentario que nos dejó Dinobot en el video de Miquella, con ocho me gusta: no hay ninguna confirmación de que Radahn aceptara ser el consorte. Y tiene razón. Así que vamos con las dos posturas, y tú decides.",
        "Primera postura: aceptó. Freyja habla de un juramento hecho con él, no de una orden. Miquella dice que el juramento se cumplirá, como quien cobra una deuda. Y en la pelea final, Radahn lucha a su lado sin resistirse.",
        "Si aceptó, la lectura más oscura de la comunidad es que Aeonia fue la parte de los hermanos. Que Malenia fue a Caelid a dejarlo listo para morir. Y Radahn, de alguna forma, lo sabía.",
        "Segunda postura: nunca aceptó. El recuerdo enseña la pregunta del niño, pero nunca la respuesta de Radahn. En Aeonia pelearon a muerte, sin trucos. Y Miquella tiene la costumbre de encantar a cualquiera que se le resista. Ansbach lo resume así: Miquella el Bondadoso es un monstruo.",
        "Y hay un detalle de los archivos del juego que inclina la balanza. Radahn iba a hablar. En un texto que se quedó sin usar, decía: soy Radahn. Hijo de Radagon de la melena roja, y de Rennala de la Luna Llena. Un león criado para la batalla.",
        "Lo quitaron. En el juego final, el consorte no dice ni una palabra. Ni para aceptar, ni para negarse.",
        "Así que esto es lo firme: hubo un juramento, tenía dos partes, y lo único que vemos de Radahn al final es esto. De consorte, mudo, y dentro de otro cuerpo.",
        "Si aceptó, prometió su alma a un niño que encantaba a la gente, y su país entero se pudrió por el camino. Si no aceptó, lo usaron como a un muñeco. Dime en los comentarios cuál de las dos te parece peor.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. Volvió en el cuerpo de Mohg.",
        "Cuando Freyja por fin descubre la naturaleza del juramento, su reacción es esta: a mí me parece bien. Sé que al viejo Jerren le dolería, pero la guerra siempre le sentó mejor al general Radahn. Mucho mejor que cualquier muerte honorable. Guerra sin fin, para avivar el alma.",
        "Fíjate en lo que acaba de hacer. Todo lo que Jerren organizó, el festival, el juramento de muerte honorable, el último deseo de los soldados del Fuerte Gael, su caballera favorita lo tira a la basura en una frase. Y Radahn vuelve.",
        "Pero el alma de Radahn necesita un cuerpo, y el suyo está podrido en las dunas. Así que Miquella toma prestado otro. Ansbach, el viejo caballero de Mohg, lo cuenta furioso.",
        "Usar a lord Mohg para entrar en la Tierra Sombría ya era bastante. Pero además planea usar su cadáver como recipiente para su rey consorte. Ha abandonado el alma de lord Mohg. Solo desea su cáscara vacía.",
        "El cuerpo que ves en la pelea final es el de Mohg, el señor de la sangre. Mira sus brazos: le salen los cuernos de augurio de Mohg. Y entre los tajos de gravedad, lanza llamas de sangre. Las de Mohg.",
        "Y si invocas a Ansbach para esa pelea, cuando ve al consorte le dice esto: General Radahn. Un placer verte después de tanto tiempo. Pero esos restos no te pertenecen. Lord Mohg tendrá su dignidad.",
        "Esos restos no te pertenecen. El héroe que tenía un festival en su honor vuelve dentro del cuerpo robado de otro semidiós. Y no dice nada. Ni una palabra para defenderse.",
        "Y ojo, que ese cuerpo no era de cualquiera. Fue Mohg el que secuestró a Miquella. Y ahora Miquella le roba el cadáver a Mohg, y mete dentro a su hermano. En esta familia nadie se queda con su propio cuerpo.",
        "Y en la segunda fase, Miquella aparece flotando sobre él, y te habla: Sinluz. Aspirante a señor del viejo orden. Si has conocido el pecado, si sufres por este mundo, cédenos el camino. A mí, Miquella, y a mi consorte prometido, Radahn.",
    ]},
    {"id": "p1b", "frases": [
        "Y aquí está su ataque más cruel. Radahn te agarra, te levanta, y te lleva hasta Miquella. Y Miquella te encanta. Te susurra: que tus pensamientos sean solo de amor.",
        "Si te vuelve a agarrar estando encantado, mueres en el acto. El juego lo llama corazón robado. Ese es el trabajo del consorte: llevarle gente a Miquella para que la ame a la fuerza. Para eso lo trajeron de vuelta.",
        "Y era tan bestia que lo tuvieron que bajar. En septiembre de dos mil veinticuatro, el parche uno punto catorce ajustó al jefe final de la expansión. Menos daño en varios ataques, menos alcance, y efectos más fáciles de ver. Las notas ni siquiera dicen su nombre. Solo, jefe final.",
        "Y no era la primera vez. En marzo de dos mil veintidós, un parche debilitó por error al Radahn de Caelid, sin anunciarlo. Unas semanas después, otro lo devolvió a su fuerza. Como recordaba Zenfaku en los comentarios, lo tocaron casi en cuanto salió el juego. Ni los parches saben qué hacer con él.",
        "¿Y Freyja, la que se alegraba de que volviera? En Enir-Ilim, al final de todo, se pone del lado de Miquella y pelea contra ti. Y en esa pelea dice: ofrezco este combate a Miquella el Bondadoso. Y a Rada...",
        "No le da tiempo a terminar el nombre. Su caballera muere por él, y él ni siquiera está ahí para oírla.",
        "Y aquí viene la ironía que cierra la lista. Su armadura dice que, desde muy pequeño, Radahn quedó cautivado por el Señor del Campo de Batalla. Por Godfrey. El primer señor del Círculo de Elden. Su ídolo de niño.",
        "Godfrey fue el rey al que su propio padre, Radagon, sustituyó. Radagon dejó a Rennala, la madre de Radahn, para convertirse en el consorte de la reina Márika. Un hombre fuerte, puesto al lado de un dios, para que el dios pudiera reinar.",
        "Y eso es exactamente en lo que acabó Radahn. El niño que soñaba con ser Godfrey terminó siendo Radagon. Consorte de un dios. En un cuerpo prestado. Sin voz.",
        "Y la recompensa por matarlo, la última que te da el juego, es el recuerdo de esa promesa entre los dos. Un dios y un señor. Fíjate en el orden del título. Primero, el dios.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. El héroe de Caelid se come a sus muertos, dispara las lanzas de sus enemigos, salvó un pueblo y luego lo pudrió, dejó a su ejército y a su mejor caballera atrás, congeló el destino de su hermana, mantuvo viva a una asesina de magos, prometió su alma a un niño que encantaba a la gente, y volvió dentro del cadáver de otro semidiós.",
        "Y lo más triste es que, en todo el juego, nunca nos dejaron oír su versión. Su amigo habla por él. Su caballera habla por él. Miquella habla por él. Y él solo ruge.",
        "Antes de irme, gracias. A Pipo, a Héctor, a Jimmy, y a todos los que nos escribieron en los videos anteriores. Barial nos contó que justo llegó ayer contra Radahn consorte, y que ahora sí entiende todo el lore. Ojalá este te llegue a tiempo para la revancha.",
        "Y Maknarth decía que le gustó el formato largo. Pues este es el más largo que hemos hecho.",
        "A los que nos dijeron que la voz pronunciaba mal Miquella o Mohg: lo leímos, y lo cuidamos en este. Los comentarios se leen todos, de verdad, y con ellos vamos mejorando el canal.",
        "Ahora te toca a ti. ¿Radahn aceptó ser el consorte, o lo usaron? Y Conker Lord, Morgott ya está en la lista.",
        "Si te quedaste con ganas de más familia, en el canal tienes las atrocidades de Márika y Radagon, de Miquella, de Malenia, de Ranni y de Melina. Es la familia más unida de las Tierras Intermedias. Sobre todo para usarse unos a otros.",
        "Y la próxima vez que te llueva una flecha gigante en las dunas, acuérdate: antes de que te la tiraran a ti, ya se la clavaron a él.",
    ]},
]
