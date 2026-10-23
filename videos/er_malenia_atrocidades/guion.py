# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Malenia QUE IGNORASTE» (22-oct-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md (copia del ganador, Miquella ~20 min ≈ ×48,
cambiando el sujeto → su gemela Malenia). Gancho: un comentario del de Miquella («¿Malenia también estaba hechizada?»).
Cada puesto va partido en dos escenas (pN / pNb) para que Lyria no pase de 175 s por escena.
No repite lo ya contado: Aeonia vs Radahn + Yelmo del joven león y «espada de Miquella» (Miquella p3), la espera al pie del
capullo y los miembros perdidos (Miquella p1b), «hijos de un solo dios» (Radagon). La Gran Runa sale solo como guiño.
Citas verificadas el 22-oct-2026 en eldenring.wiki.fextralife.com y eldenring.wiki.gg: diálogos de Malenia (entrada, fase 2,
muerte), Hand of Malenia, Malenia's Great Rune, Prosthesis-Wearer Heirloom, armadura alada (texto común), Scarlet Aeonia,
monumento de la espada (Batalla de Aeonia), mensaje de espíritu de la primera flor, Hefty Rot Pot, Cleanrot Armor, Finlay's
Ashes, Commander's Standard (O'Neil), Kindred of Rot Ashes y Kindred of Rot's Exultation, Gideon (Radahn y Malenia), Kenneth
Haight (Godrick), Jerren, Radahn's Great Rune, Remembrance of the Starscourge, Millicent, Gowry, Rotten Winged Sword
Insignia, Unalloyed Gold Needle (rota y la de Millicent), Miquella's Needle.
EVITAR (mitos): «Radahn se comió a su caballo» (Jerren dice cadáveres de amigos y enemigos) y «la flor destruyó Sellia» (sin texto).
"""

TITULO = "Las 5 peores atrocidades de Malenia QUE IGNORASTE"
ARCHIVO = "er_malenia_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# 22-oct: en Miquella Whisper oyó «Mikeya»/«Moj» y eran errores REALES (los comentarios se burlaron): nombre mal = regenerar.
FONETICA = {
    "Miquella": "Mikuéla", "Malenia": "Malénia", "Radahn": "Rádan", "Radagon": "Rádagon", "Godrick": "Gódrik",
    "Godfrey": "Gódfri", "Kenneth Haight": "Kénez Jéit", "Gowry": "Gáuri", "Millicent": "Mílisent", "Maureen": "Morín",
    "Mary": "Méri", "Amy": "Éimi", "Polyanna": "Poliána", "O'Neil": "Oníl", "Finlay": "Fínlei", "Gideon": "Guídeon",
    "Jerren": "Yérren", "Aeonia": "Eónia", "Caelid": "Caélid", "Sellia": "Sélia", "Elden Ring": "Élden Ring", "Elden": "Élden",
}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # solo imagen del gameplay
    recorte_por={f"scene-{n:03d}": 0.09 for n in (2, 7, 13, 14, 18, 22, 31, 62, 72, 74, 78, 105, 106, 119,   # firma «SHIRRAKO»
                                                  108, 109, 111)},                                           # «GAME CLIP» (ClipPlayTru)
    yt=dict(sufijo="Elden Ring", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls"]),   # heredado de Miquella/Ranni
)

# Revisado el 23-oct tras la 1.ª ronda (eval.json): 50 marcadas, casi todas falsas alarmas — cola en frases largas, pausa tras
# punto y nombres que Whisper escribe como suenan («Gauri», «Finley», «Mikuela/Miquela», «Celia», «Haidt»; ningún «Miqueya»).
# Errores REALES: «Radahn» → «arladan/Ladan» (p3_1, p3b_1: regeneradas con semillas 3-5) y tomas sueltas con «Malemia/Malena»,
# «Kaelit», «consume», «miss», «herveza», «veo», «escalata», «Miquel la», «Dradan»: movidas a voz/_descartes/.
CER_MAX_POR_FRASE = {'p5_6': 0.017, 'p5b_0': 0.019, 'p3b_4': 0.014, 'p3b_5': 0.026, 'p2_6': 0.018, 'p2_7': 0.02, 'p2b_0': 0.023,
                     'p2b_1': 0.035, 'p1b_0': 0.019, 'p1b_2': 0.016}
GAP_MAX_POR_FRASE = {'p4b_2': 0.69, 'p4b_4': 0.7, 'p3_4': 0.67, 'p2_11': 0.67, 'p2b_3': 0.73, 'p2b_5': 0.72, 'p2b_7': 0.7, 'p1_1': 0.71,
                     'p1_2': 0.71, 'p1_6': 0.71, 'p1b_0': 0.8, 'p1b_6': 0.8}
TAIL_MAX_POR_FRASE = {'intro_2': 0.52, 'p5_1': 0.43, 'p5_6': 0.4, 'p5_9': 0.55, 'p5_10': 0.57, 'p5b_1': 0.39, 'p5b_4': 0.42, 'p5b_5': 0.51,
                      'p5b_7': 0.56, 'p5b_8': 0.47, 'p4_1': 0.41, 'p4_10': 0.54, 'p4b_2': 0.52, 'p4b_4': 0.58, 'p4b_7': 0.59, 'p3_2': 0.46,
                      'p3_4': 0.62, 'p3b_2': 0.46, 'p3b_8': 0.38, 'p3b_9': 0.69, 'p2_2': 0.65, 'p2_3': 0.57, 'p2_7': 0.43, 'p2_8': 0.44,
                      'p2b_0': 0.56, 'p2b_3': 0.48, 'p2b_5': 0.4, 'p2b_6': 0.39, 'p2b_7': 0.39, 'p2b_8': 0.53, 'p1_1': 0.5, 'p1_2': 0.6,
                      'p1_6': 0.42, 'p1b_0': 0.57, 'p1b_3': 0.55, 'p1b_4': 0.67, 'p1b_6': 0.6, 'p1b_7': 0.55, 'cierre_0': 0.45,
                      'cierre_1': 0.63, 'cierre_2': 0.41}

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    # sin nombres propios: el filtro de Lyria los rechaza
    estilo="Dark gothic fantasy orchestral underscore like a melancholic soulslike action RPG soundtrack: solemn low choir, "
           "pipe organ pads, cello and harp, distant bells, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas={
        "intro": ("a swordswoman asleep beneath a giant tree, a single sustained choir note, red petals drifting, quiet dread", 6),
        "p5": ("an undefeated duelist, elegant strings and harp, proud and cold, a waltz with blades", 5),
        "p5b": ("a fallen lord kneeling in shame, low brass, a slow sinister dance in three", 5),
        "p4": ("knights in golden armor marching into a red swamp, solemn snare and low horns, a vow already doomed", 6),
        "p4b": ("a lone knight carrying a sleeping figure across a ruined continent, lonely solo cello, exhausted footsteps", 6),
        "p3": ("a kingdom swallowed by a giant crimson flower, rising dissonant choir, an explosion that never ends", 6),
        "p3b": ("an endless war against a plague, distant fires on red dunes, mournful brass, a funeral that waits for a guest", 7),
        "p2": ("an abandoned girl in a ruined church, fragile music box over low strings, an old man's sweet lies", 6),
        "p2b": ("a daughter refusing to become a goddess, bittersweet harp and viola, dignity in the rot", 7),
        "p1": ("a second bloom of crimson wings, full choir and pipe organ swelling, terror and divine beauty", 7),
        "p1b": ("one step from a goddess of plague, slow heavy organ, then a quiet final apology to a brother", 9),
        "cierre": ("calm after the storm, warm low strings, a wry final note fading out", 4),
    },
    tramos=[   # <= 175 s cada uno: AJUSTAR con la duración real tras `tiempo`
        (["intro"], "Begin softly from near silence with a single choir note. End on a sustained low string tone."),
        (["p5"], "Begin on a sustained low string tone. End on a held, proud string chord."),
        (["p5b"], "Begin on a proud string chord that darkens. End on a low brass tone."),
        (["p4"], "Begin on a low brass tone with a soft snare. End on a heavy held horn chord."),
        (["p4b"], "Begin on a lonely cello note. End on a quiet, exhausted low tone."),
        (["p3"], "Begin on a quiet low tone that swells into a dissonant choir. End on a heavy unresolved drone."),
        (["p3b"], "Begin on a low drone with distant drums. End on a mournful sustained brass note."),
        (["p2"], "Begin on a soft music box. End on a fragile held string chord."),
        (["p2b"], "Begin on a fragile harp chord. End on a bittersweet sustained viola note."),
        (["p1"], "Begin on a sustained viola note that swells to full choir and organ. End on a held, terrifying chord."),
        (["p1b"], "Begin on a slow heavy organ. Settle into a quiet sorrowful tone."),
        (["cierre"], "Begin on a calm low tone. Settle and fade out to silence at the end."),
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Si viste el video de Miquella, ya sabes que el niño del capullo era el personaje más peligroso de Elden Ring. Y en los comentarios, uno de ustedes preguntó algo que me dejó pensando.",
        "Preguntó si Malenia también estaba hechizada por Miquella. Si todo lo que hizo lo hizo bajo su encanto, igual que el resto de sus seguidores.",
        "Y es una buena pregunta, porque Malenia es la jefa que todos recordamos con respeto. La espadachina invicta, la hermana fiel, la que la putrefacción dejó sin casi nada y aun así siguió peleando.",
        "La que te mató cuarenta veces, sí, pero con mucha elegancia.",
        "El problema es que, cuando uno se pone a leer las descripciones de los objetos, la hermana fiel deja un rastro bastante más feo de lo que parece.",
        "Y no lo digo yo. Lo dice ella misma, en lo primero que te suelta cuando entras a su arena: cadáver tras cadáver dejé a mi paso, mientras esperaba su regreso.",
        "Así que hoy van las cinco peores atrocidades de Malenia que ignoraste. Y al final te respondo lo del hechizo, porque la respuesta es peor que un sí.",
        "Ponte cómodo, que este va largo. Y si te pica un poco el brazo mientras lo ves, tranquilo, es normal. Es la putrefacción.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Nunca conoció la derrota.",
        "Es lo último que te dice antes de empezar la pelea: soy Malenia, la espada de Miquella, y nunca he conocido la derrota. Y lo peor es que no está presumiendo. Te está informando.",
        "La hoja que lleva en su brazo de metal tiene una descripción que casi nadie lee: la prótesis de guerra de Malenia simbolizaba sus victorias.",
        "Sus victorias. No su brazo perdido, no su enfermedad. Lo que ese brazo representa es la lista de gente a la que le ganó.",
        "Y la descripción sigue: algunos dicen haber visto alas cuando alzaba el arma. Alas de una determinación feroz que jamás conocieron la derrota.",
        "Ahora, quién está en esa lista. Pues uno de los primeros nombres es nada menos que un semidiós: Godrick, el injertado.",
        "Lo cuenta Kenneth Haight, el noble que te encuentras en Necrolimbo pidiendo ayuda para recuperar su fuerte. Y lo cuenta con un desprecio que da gusto escuchar.",
        "Según él, Godrick insultó a Malenia, perdió contra ella en combate, y en vez de morir como un hombre, prefirió lamerle las botas.",
        "Le lamió las botas. Un semidiós de la línea de Godfrey, el primer señor del Círculo, arrodillado delante de una chica con un brazo de oro.",
        "Y no creas que Godrick se lo tomó como una lección de humildad. Se pasó el resto de su vida cosiéndose al cuerpo los brazos de otros. Que, ahora que lo pienso, es justo lo que le faltaba a ella.",
        "Gideon, el que todo lo sabe en la Mesa Redonda, la describe en pocas palabras: Malenia, la espadachina invicta. Y en un juego donde todo el mundo pierde, eso ya debería darte miedo.",
    ]},
    {"id": "p5b", "frases": [
        "Pero lo de Godrick es la parte divertida. La parte fea es cómo gana Malenia.",
        "Porque cada vez que su espada te toca, ella se cura. Aunque bloquees con el escudo. Tú pierdes vida y ella la recupera, como si cada golpe que te da fuera un trago de agua.",
        "Y su Gran Runa, la que te llevas cuando por fin la vences, tiene un efecto que parece una burla: reduce el poder curativo de tu frasco de lágrimas carmesí.",
        "O sea que Malenia no solo se cura contigo. Encima te enseña a curarte menos. Hasta muerta te sigue quitando vida.",
        "En el video de Radagon vimos que esa runa debió ser la más sagrada de todas. Lo que no vimos es lo que hace en realidad: pudrir lo único que te mantiene vivo.",
        "Y luego está su infancia. Hay un talismán que la cuenta en una línea: aunque nació en la putrefacción maldita, cuando la niña conoció a su mentor y su espada fluida, obtuvo alas de una fuerza sin igual.",
        "Una niña enferma desde que nació, a la que alguien le enseña a pelear. Hasta aquí es una historia bonita, de esas que te hacen querer al personaje.",
        "El problema es lo que hizo con esas alas. Porque una espada que nunca pierde, en manos de alguien que lleva dentro a un dios exterior, no es un talento. Es una amenaza.",
        "Un juego entero lleno de gente que pierde: semidioses que se rinden, reyes que huyen, caballeros que traicionan. Y en medio de todo eso, una sola persona a la que nadie consigue parar.",
        "Y como nadie la podía parar, nadie pudo proteger a los primeros que pagaron el precio. Que, curiosamente, eran los suyos.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Los que se pudrieron por ella.",
        "Malenia no peleaba sola. Tenía su propio ejército: caballeros de armadura dorada y lanzas largas, que todavía te encuentras por Caelid y por el Árbol Sagrado.",
        "Y la descripción de su armadura dice algo que, leído con calma, es terrible.",
        "Los caballeros juraron pelear junto a Malenia, a pesar de la inevitable, aunque gradual, putrefacción de su carne.",
        "A pesar de la putrefacción de su carne. Es decir, todos sabían que estar cerca de ella los iba a pudrir. Despacio. Y aun así firmaron.",
        "Es como entrar a trabajar a una empresa donde el contrato dice: buen ambiente, causa noble, y te vas a deshacer en vida. Firme aquí, por favor.",
        "Y Malenia los aceptó. No hay un solo objeto que diga que intentó protegerlos de su enfermedad. Se los llevó a Aeonia, que es justo donde iba a florecer.",
        "Allí, frente al ejército de Radahn, la flor escarlata se abrió por primera vez. Y sus caballeros estaban a su lado cuando pasó.",
        "De ese ejército quedó casi nada. Uno de los pocos que sigue en pie es el comandante O'Neil, al que te encuentras en mitad del pantano de Aeonia, rodeado de podredumbre.",
        "Su estandarte lo describe como el único veterano que recuerda esa batalla con orgullo, en la devastación del campo comido por la putrefacción.",
        "Con orgullo. Lo único que le queda es estar orgulloso del día en que su señora pudrió el campo donde cayeron todos sus compañeros. Y tú llegas y lo matas por una aguja rota.",
        "Guárdate esa aguja, por cierto, que en el número dos vuelve a salir. Y no para nada bueno.",
    ]},
    {"id": "p4b", "frases": [
        "Pero la historia más triste de ese ejército es la de Finlay.",
        "Finlay es una caballera cuyas cenizas puedes invocar. Y su descripción cuenta que fue de las pocas que sobrevivieron a la batalla de Aeonia.",
        "Cuando todo terminó, Malenia no despertó. Se quedó dormida después de florecer. Y Finlay la cargó ella sola, desde Caelid hasta el Árbol Sagrado, abriéndose paso contra todo lo que encontró por el camino.",
        "Medio continente. Con una diosa de la putrefacción dormida al hombro. Y pudriéndose ella también a cada paso que daba.",
        "Y cuando llegó, qué recibió. Nada. Malenia siguió durmiendo bajo el árbol. No hay un gracias, no hay una medalla, no hay ni una sola línea de diálogo dedicada a Finlay.",
        "Y luego están los que nadie quiso. Esos bichos con forma de insecto y lanzas que te encuentras en cuevas y aguas podridas. Se llaman los parientes de la putrefacción.",
        "Sus cenizas dicen que son siervos de la diosa de la putrefacción. Siervos que fueron abandonados.",
        "Y uno de sus encantamientos, que puedes aprender tú, viene con una oración: putrefacción para la diosa escarlata. Oh, flores escarlata, floreced en tierras lejanas, y volved a nosotros, los hijos no deseados.",
        "Los hijos no deseados. Así se llaman a sí mismos. Le rezan a una diosa que nunca los miró, y le piden que vuelva.",
        "Malenia tenía un ejército que se pudrió por ella, una caballera que la cargó medio mundo, y una colonia de bichos que le reza. Y a ninguno le dedicó jamás una palabra.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Caelid.",
        "En el video de Miquella te conté lo que la flor de Aeonia le hizo a Radahn. Hoy toca lo que le hizo a todos los demás.",
        "Porque Caelid no siempre fue ese desierto rojo con cielo de herida abierta que recuerdas. Era una tierra con castillos, con un ejército, y con una ciudad de hechiceros, Sellia.",
        "Tanto, que el propio Radahn fue a estudiar allí la magia de la gravedad, para no tener que abandonar nunca a su caballo, que era su favorito pero estaba flaquísimo.",
        "Y entonces dos semidioses decidieron pelear justo ahí. Hay un monumento con una espada que lo resume en tres líneas: la batalla de Aeonia. Radahn y Malenia, en un punto muerto. Y entonces, la putrefacción escarlata florece.",
        "En un punto muerto. Malenia no estaba perdiendo. Estaba empatando. Y como la que nunca conoció la derrota no sabe lo que es empatar, sacó la flor.",
        "Esta es la descripción de su técnica, la Aeonia escarlata: crea una flor gigantesca que florece en una explosión de putrefacción escarlata.",
        "Una explosión. No un hechizo contra un enemigo. Una bomba de enfermedad lanzada en mitad de una tierra donde vivía gente.",
        "Y el pantano que te encuentras hoy, ese lago rojo donde todo te enferma, es lo que quedó del sitio donde se abrió aquella flor.",
        "Hay un mensaje de un espíritu justo en ese lugar: aquí mismo floreció la primera flor de Aeonia. Malenia, que florezcas como una diosa.",
        "Fíjate en lo que dice. No llora a los muertos. Le reza a la que los mató.",
    ]},
    {"id": "p3b", "frases": [
        "Y el ejército de Radahn, qué pasó con él. Pues que nunca dejó de pelear.",
        "Gideon lo cuenta así: he oído que los supervivientes del ejército de Radahn siguen en las tierras salvajes, conteniendo la putrefacción con fuego.",
        "Conteniendo la putrefacción con fuego. Años después de la batalla, siguen quemando lo que se pudre para que no avance. Una guerra que ya nadie recuerda contra una enfermedad que no se va.",
        "Hasta la Gran Runa de Radahn tiene que pelear contra eso. Su descripción dice: la Gran Runa arde para resistir el avance de la putrefacción escarlata.",
        "Un semidiós al que llamaban el Azote Estelar, y su runa se pasa la eternidad ardiendo para no pudrirse.",
        "Y el que mejor lo resume es Jerren, el cazador de brujas que organiza el festival en el castillo de Radahn.",
        "Jerren dice que el general está maldito a vagar para siempre, comido por dentro por la putrefacción de Malenia, y que hace mucho que perdió el juicio.",
        "Y que ahora junta los cadáveres de antiguos amigos y enemigos por igual, y se atiborra de ellos, como un perro.",
        "Y luego añade la frase más triste de todo Caelid: enfermo de putrefacción y lisiado por la locura, todo lo que quería era una muerte honorable.",
        "Una muerte honorable. Por eso existe el festival. No es una fiesta. Es un funeral que necesita invitados, porque nadie en Caelid es lo bastante fuerte para darle a su general lo único que pide.",
        "Y ahí entras tú. Llamado de quién sabe dónde, para terminar el trabajo que Malenia dejó a medias hace décadas.",
        "Malenia pudrió a Radahn. Pudrió a su ejército. Pudrió la tierra entera. Y después se fue a dormir al otro lado del mapa. Y quien tuvo que limpiar el desastre, fuiste tú.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Las hijas que nunca quiso.",
        "Si hiciste la misión de Millicent, ya sabes por dónde voy. Y si no la hiciste, prepárate, porque es una de las misiones más tristes del juego, y la culpa tiene nombre.",
        "Millicent es una chica que te encuentras en Caelid, tirada en una iglesia, consumida por la putrefacción. Y lo que te dice no deja lugar a dudas: mi carne se retuerce con putrefacción escarlata. Soy de la sangre de Malenia.",
        "A ella la encontró Gowry, un viejo sabio que vive en una choza cerca del pantano. Y él lo cuenta así: fui yo quien la encontró. Un simple bebé, en el pantano de Aeonia.",
        "Un bebé en el pantano de Aeonia. En el sitio exacto donde se abrió la flor. Millicent no tiene padre ni madre que la criaran. Tiene una explosión.",
        "Y no es la única. Tiene hermanas: Mary, Maureen, Amy y Polyanna, valquirias que sirven a la diosa de la putrefacción.",
        "Y Gowry no la cuida por cariño. Gowry tiene un plan: que Malenia ascienda como diosa, y que Millicent renazca con ella, convertida en una valquiria escarlata.",
        "Para eso, Millicent tiene que florecer. Y Gowry sabe cómo conseguirlo: alimentada por la traición, su capullo florecerá con más intensidad.",
        "Alimentada por la traición. Hay que traicionarla para que florezca. Y el que te lo pide es el mismo viejo amable que te ha estado ayudando: te lo ruego, mátala. Con tus propias manos.",
        "Y lo dice con un cariño que da escalofríos: oh, Millicent, mi pequeño capullo, el más prometedor.",
        "Y en toda esta historia hay una línea, dirigida a Millicent, que lo resume todo: tú también nos repudiarás, como hizo tu madre.",
        "Como hizo tu madre. Esa madre es Malenia. Y sus hijas lo saben muy bien: su madre las repudió.",
    ]},
    {"id": "p2b", "frases": [
        "Pero Millicent tiene algo que sus hermanas no tienen. Una aguja de oro puro clavada en la carne, de las que Miquella forjó para alejar la intromisión de los dioses exteriores.",
        "Y te acuerdas de la aguja rota que le quitaste al comandante O'Neil. Pues esa es. Gowry la repara, y gracias a ti, Millicent puede frenar su putrefacción.",
        "Con esa aguja, Millicent piensa, camina, te ayuda en las peleas. Puede ser una persona, por primera vez en su vida.",
        "Y decide seguir el camino de Malenia. Lo dice ella: ahora sigo el camino que tomó Malenia, después de desatar el poder de la putrefacción escarlata. Tengo algo que devolverle.",
        "Lo que quiere devolverle es esa aguja. Quiere llegar hasta su madre y entregarle la cura que a ella le salvó la vida.",
        "Y cuando por fin llega al final de su camino, Millicent elige. Se arranca la aguja ella misma. Y te dice lo más digno que se oye en todo Elden Ring: prefiero pudrirme hasta la nada, tal como soy.",
        "Piénsalo un momento. Una hija repudiada, nacida del cráter de su madre, que podría convertirse en diosa a su lado. Y prefiere morir pudriéndose antes que ser como ella.",
        "Y la aguja te la da a ti, para que se la lleves. Tú la dejas en la flor de Aeonia, en la arena de Malenia, y el juego te da a cambio la aguja de Miquella.",
        "Y Malenia, qué hace mientras tanto. Nada. Ni se entera. Sigue soñando con su hermano bajo el árbol, a unos metros de donde su hija se pudre sola.",
        "Lo más cerca que Millicent estuvo nunca de su madre fue esa aguja que tú le llevaste. Y ni siquiera llegó a verla.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. La tercera flor.",
        "Todo lo que te he contado hasta ahora pasó con una sola flor. Una. Caelid, Radahn, su ejército, los caballeros, las hijas. Todo eso salió de la primera vez que Malenia floreció.",
        "Y aquí está la línea que casi nadie lee, en la descripción de la Aeonia escarlata: cada vez que la flor escarlata florece, la putrefacción de Malenia avanza. Con la tercera flor, se convertirá en una diosa verdadera.",
        "Con la tercera. Así que la pregunta obvia es: cuántas lleva ya.",
        "La primera fue en Aeonia, contra Radahn. Y la segunda, la viste tú con tus propios ojos. Fue en tu pelea.",
        "Cuando le bajas la primera barra de vida, Malenia se detiene, y te dice: espera. La flor escarlata florece una vez más.",
        "Una vez más. Esa es la segunda flor. Lo que ves en la segunda fase, con las alas rojas, no es un cambio de fase para lucirse. Es Malenia a una sola flor de convertirse en diosa.",
        "Y te lo dice sin rodeos: vas a presenciar el verdadero horror. Ahora, púdrete.",
        "Y si te mata, que te habrá matado unas cuantas veces, lo último que oyes es: que tu carne sea consumida por la putrefacción escarlata.",
        "Ahora piensa en lo que significa eso. Si con una sola flor convirtió una tierra entera en un pantano rojo, qué habría pasado con la tercera.",
        "Una descripción de objeto lo explica sin dramatismo: la putrefacción es uno de los elementos divinos de los dioses exteriores, y devora la vida como una plaga feroz.",
        "Una diosa de eso. No una semidiosa enferma. La plaga misma, con alas, con espada, y sin perder jamás.",
    ]},
    {"id": "p1b", "frases": [
        "Y hay gente esperándolo. El espíritu del pantano que le reza. Los hijos no deseados que le piden que vuelva. Gowry, que quiere ver a su pequeño capullo convertido en valquiria. Todos empujan hacia esa tercera flor.",
        "Y la única persona que se puso entre Malenia y esa tercera flor fuiste tú. No Miquella, no la Orden Áurea, no los dioses. Tú, con tus frascos medio podridos.",
        "Y ahora sí, lo que preguntaban en los comentarios: estaba Malenia hechizada por Miquella.",
        "Su armadura entera, el yelmo, la coraza, los guanteletes y las grebas, lleva la misma frase en su voz: mi hermano cumplirá su promesa. Posee la sabiduría y el encanto de un dios. Es el más temible de todos los Empíreos.",
        "Fíjate bien en la palabra. Ella lo llama temible. Los hechizados de Miquella hablan de su bondad. Malenia habla de su poder. Sabe perfectamente lo que es su hermano. Y lo espera igual.",
        "Así que no, no hay nada en el juego que diga que estaba hechizada. Mi lectura es otra, y es peor: Malenia no necesitaba el encanto. Estaba de acuerdo.",
        "Miquella le forjaba agujas para frenar su enfermedad, y ella dejaba cadáver tras cadáver a su paso mientras lo esperaba. Él ponía el encanto, ella ponía la espada. Y entre los dos, casi se quedan con el mundo.",
        "Y cuando por fin la vences, sus últimas palabras no son para sus caballeros, ni para Finlay, ni para Millicent. Son para él: oh, querido Miquella, mi hermano. Lo siento. Por fin encontré a mi rival.",
        "Ni al final se acordó de los suyos.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. La hermana fiel, la espadachina invicta, la que todos respetamos después de morir cien veces, dejó atrás una tierra podrida, un ejército sin descanso, unos caballeros que se deshicieron por ella, y unas hijas que prefirieron morir antes que parecérsele.",
        "Ahora te toca a ti: quién fue peor de los gemelos. Miquella, que te quería quitar la voluntad, o Malenia, que estuvo a una flor de pudrir el mundo. Te leo en los comentarios, que los leo todos, de verdad.",
        "Y si quieres al resto de la familia, en el canal tienes las atrocidades de Miquella, de Radagon, de Márika y de Ranni. Ninguno sale bien parado, y créeme, ya me estoy quedando sin dioses decentes.",
        "Y la próxima vez que alguien te diga que nunca ha perdido en nada, no lo felicites. Pregúntale qué hizo cuando iba empatando.",
    ]},
]
