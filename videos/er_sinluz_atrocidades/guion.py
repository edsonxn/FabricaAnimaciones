# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades que COMETISTE tú QUE IGNORASTE» (16-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md).
El SUJETO es el espectador (el Sinluz). Pedido por @wsefsd-n1v y @Amand4Caro. ≥ 24 MIN (pedido del usuario, 16-nov).
Voz «el Profeta» de ElevenLabs, PLANA (ganó la votación: ≈ 18 comentarios contra 4). Sin patrocinio. OST oficial.
Investigación: _investigacion/dossier.md. Los diálogos verificados SOLO en inglés se PARAFRASEAN (nunca entre comillas en pantalla);
las citas textuales de la voz son descripciones de objeto en español verificadas.
Críticas con contraburla (regla 11-nov, mínimo 2-3): @cristianrico9009 (Loquendo, voto), @jonathanvillamil9854 (el anterior, voto),
@arturoarrow9163 (atrocidades del narrador anterior, p5), @KingInsect25 ♥11 (Maliketh, p3c).
Sonidos nombrados = tramo audible con `post` (regla 31-oct): p2b (Hyetta ardiendo), p1 (Melina en la Forja).
"""

TITULO = "Las 5 peores atrocidades que COMETISTE tú QUE IGNORASTE"
ARCHIVO = "er_sinluz_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
# el Profeta (ElevenLabs God - Deep, Powerful). Corchetes SOBRIOS: nada de risas ni alegría (el usuario, 11-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {"Miquella": "Miquéla"}   # 12-nov: el acento va en «que»

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={"scene-007": .09, "scene-078": .09, "scene-148": .09, "scene-149": .09},   # [SHIRRAKO] marca de agua abajo a la derecha
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Llevamos diez videos contando las atrocidades de los semidioses, desde la reina Márika hasta el pobre Godrick. [short pause] Y en todos, había alguien más en la escena.",
        "Alguien que entró en sus casas sin llamar. Que los mató uno por uno. Y que se llevó lo que tenían dentro.",
        "Un comentario lo dijo en ocho palabras: las peores atrocidades que hicimos nosotros, el Sinluz. Y Amand lo remató: las cinco peores atrocidades, pero del Sinluz del tiznado.",
        "Así que hoy no hay semidiós. Hoy el acusado eres tú. [short pause] El que drogó a una guerrera, trabajó de sicario para un caníbal, le dio de comer ojos a una chica ciega y prendió fuego al mundo.",
        "Y la número uno no es la más cruel. Es la única que no podías evitar. [short pause] Porque si viste los créditos de Elden Ring, ya la cometiste.",
    ]},
    {"id": "voto", "frases": [
        "Antes de empezar, el resultado de la votación. En el video de Godrick preguntamos: narrador anterior, o nuevo profeta.",
        "Contamos los comentarios uno por uno. El narrador anterior sacó cuatro. [short pause] El profeta, dieciocho. Así que me quedo.",
        "Alexander lo resumió mejor que nadie: nuevo profeta y punto. Y Amand escribió que se me escucha con ganas de contar el lore que no notamos la primera vez. Para eso estoy.",
        "Jonathan votó por el anterior. Jonathan, respeto tu voto. Fue uno de cuatro. Pero no te preocupes, el anterior no se fue muy lejos. Sigue en el video de Mohg, diciendo su nombre mal para toda la eternidad.",
        "Y Cristian preguntó quién es el degenerado al que se le ocurre narrar con Loquendo. Cristian, Loquendo no se presentó a la votación. No sacó ni un voto. [short pause] Y si buscas degenerados, quédate. Hoy el protagonista de la lista eres tú.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. [short pause] El coleccionista de personas.",
        "Si sigues la historia de Ranni, la bruja de la torre, tarde o temprano subes a la Torre de Seluvis, en las Tres Hermanas, al oeste de Liurnia. Seluvis es su preceptor. Un hechicero viejo, de sonrisa torcida, que te recibe como a un socio.",
        "Y te da un regalo. Un frasquito. La Poción de Seluvis. Su descripción es corta: pequeño vial que contiene un turbio tónico de un color negro azulado. Y debajo, la orden. Encuentra a Nepheli y haz que se beba esto.",
        "La guerrera Nepheli Loux pertenece a la Mesa Redonda. La que pelea a tu lado en Velo Tormentoso. La que te trata como a un amigo. Y el juego te deja elegir: dársela a ella, dársela al Zampaheces, el asesino encadenado en las cloacas bajo Leyndell, o dársela a Gideon, que se ofrece a deshacerse de ella sin que Seluvis se entere.",
        "Mucha gente eligió a Nepheli. [short pause] Y cuando lo haces, la historia de Nepheli se acaba. Así, sin más explicaciones. Deja de ser la guerrera que conociste.",
        "Seluvis, cuando se entera, no se enfada. Al contrario. Te dice que ahora eres su cómplice. Y te pregunta si no te gustaría tener una marioneta propia.",
    ]},
    {"id": "p5b", "frases": [
        "Porque debajo de unas ruinas, al noreste de la torre de Ranni, detrás de un suelo que no existe, Seluvis tiene un sótano. Y en el sótano, figuras de pie, inmóviles, con la mirada perdida. En la entrada, un mensaje. Marioneta de Seluvis. No tocar.",
        "Te deja elegir una gratis. Las demás te las vende. Y todas son cenizas de espíritu: las invocas en la pelea, para que mueran por ti.",
        "La Marioneta de Nepheli Loux tiene su propia descripción. La marioneta de una guerrera traicionada por la pureza de su corazón. [short pause] La traicionó alguien. Y ese alguien llevaba el frasquito en el bolsillo.",
        "Las otras no son mejores. La del Zampaheces es, dice, el espíritu de un hombre que asesinó a miles de personas y profanó sus cadáveres. La del jarróntropo, el espíritu de un hombre ansioso por ser parte de las entrañas de un tarro viviente.",
        "Y la de Therolina, una doncella del dedo, termina con una frase que pesa más de lo que parece. Un Sinluz sin su doncella, una doncella sin su Sinluz, y nada ni nadie que vaya a reunirlos.",
        "Al fondo del sótano, detrás de otra pared falsa, hay una más. La de Sellen, tu maestra de hechicería. Seluvis no colecciona extraños. Colecciona a la gente que conoces.",
        "Y el plan final es peor. Te pide el Ámbar de luz estelar, un mineral que, según su descripción, puede comandar los destinos de los dioses. Con él prepara un Brebaje ámbar. La orden: haz que Ranni se lo beba para disponer de la mejor marioneta jamás creada.",
        "Tú vas, sacas el ámbar de una cueva en la Meseta Altus y se lo llevas. Lo único que te detiene es Ranni, que si insistes, te mata. [short pause] Ella fue la única con la decencia de pararte.",
        "Arturo escribió que quería las cinco atrocidades que hizo el narrador anterior. Arturo, solo tenía una. Y la repitió en cada video. Pero no se preocupen, la gente lo perdonó. A Nepheli, en cambio, nadie le pidió perdón nunca.",
    ]},
    # 16-nov: escenas NUEVAS para llegar a ≥ 24 min (no tocar las de arriba: las tomas de voz van por <id>_<índice>)
    {"id": "p5c", "frases": [
        "Y ahora, la parte en la que casi nadie se fija. Al final de la historia, Seluvis y su sirviente Pidia acaban muertos. Y en el cadáver de Pidia, en la Mansión de los Caria, encuentras la Marioneta de Nepheli Loux. No se vende en la tienda. Solo la tiene quien la drogó.",
        "Su descripción dice que era una de las marionetas favoritas de Seluvis. Y termina así: los diamantes en bruto merecen un trato especial para que su preciado interior no se eche a perder. Nepheli Loux era una guerrera hecha y derecha. [short pause] Era.",
        "¿Y qué haces con ella? La invocas contra los jefes. La guerrera que peleó contigo en Velo Tormentoso porque quería, ahora pelea contigo porque tú la llamas. Y si cae, en la siguiente pelea la vuelves a sacar. Como una herramienta más.",
        "Si elegiste al Zampaheces, la cosa no mejora. Cuando se la bebe, repite a trompicones que él es el Zampaheces, como quien se agarra a lo único que le queda. Su marioneta acaba en la tienda de Seluvis. Y de paso, pierdes un final entero del juego, la Bendición de la desesperación.",
        "La opción decente, dársela a Gideon, que se ofrece a deshacerse de ella, es la única que te deja sin marioneta. [short pause] El juego no premia la decencia. Premia el frasquito.",
        "Mientras tanto, Seluvis te va tomando cariño. Te dice que cada marioneta es como un hijo para él, y aun así te las vende. Cuando le compras otra, te felicita: vas resultando todo un titiritero. Y cuando te propone engañar a la mismísima Ranni y aceptas, te dice que ya lo sabía. [short pause] Que eres igual que él.",
        "Y en su sótano hay una marioneta que casi nadie compra. La Marioneta de Dolores, la Flecha Durmiente. Su descripción dice que fue una de las marionetas favoritas de Seluvis, y que Dolores perteneció en su día a la Mesa Redonda, donde fue crítica a la par que amiga de Gideon el Omnisciente.",
        "Y termina así: ella fue la causante de la enemistad entre este último y Seluvis. Dos viejos de la Mesa Redonda que se pelearon por la misma mujer, y uno de ellos la acabó metiendo en un frasco. [short pause] Tú solo tienes que pasar por caja.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. [short pause] Sicario de un caníbal.",
        "En la cima del Monte Gelmir, entre ríos de lava, hay una casa elegante con un recibidor muy tranquilo. La Mansión del Volcán. Te recibe una mujer con máscara, Tanith, y te ofrece algo que nadie en las Tierras Intermedias te había ofrecido. [short pause] Una familia.",
        "Lo único que tienes que hacer a cambio es un trabajito. En el despacho hay un escritorio, y en el escritorio, cartas con nombres. Cada carta es un Sinluz que, según la casa, merece morir.",
        "El primero, el viejo caballero Istvan, en la Colina Tormentosa, junto al Puente divino. El segundo, Rileigh, el holgazán, al fondo de un desfiladero de la Meseta Altus. El tercero, Juno Hoslow, caballero de la sangre, en una cabaña de los Picos de los gigantes.",
        "Los invades. Los matas. Vuelves a casa. Y Tanith te paga. Un hechizo de magma. Una espada de hueso de serpiente. Y un talismán, el Camafeo del megalómano.",
        "Su descripción es la filosofía de la casa. Cuando Rykard sucumbió a la herejía, tomar por la fuerza se convirtió en norma. Después de todo, los propios dioses lo hacían.",
        "Tanith también te avisa de que en esta casa no hay sitio para los débiles, ni para los que quieren conservar las manos limpias. Si no quieres cazar a los tuyos, te tienes que ir. [short pause] Y tú te quedaste.",
    ]},
    {"id": "p4b", "frases": [
        "Tras el tercer encargo, Tanith te ofrece el premio mayor. Una audiencia con el señor de la casa. Rykard. Te dice que las visitas del señor con sus campeones siempre son todo un espectáculo.",
        "Lo que no te dice es cómo terminan. Eso lo cuenta el hechizo que sacas de Rykard cuando lo matas, el Rencor de Rykard. El señor les concedió audiencia, tras la cual fueron recibidos por las fauces de la gran serpiente.",
        "La audiencia era el plato. Los campeones de la mansión, los que hacían el mismo trabajo que tú, terminaban en el estómago de la Serpiente devoradioses. [short pause] Tú no eras el sicario favorito. Eras el siguiente menú.",
        "Te salvaste porque ganaste la pelea. Pero los tres que mataste no tuvieron esa suerte. Eran Sinluz como tú, cazados por encargo de un hombre que se ofreció como alimento a la serpiente, runa incluida.",
        "Y cuando vuelves al salón de Rykard, ahí está Tanith. Junto al cadáver gigantesco de su señor. Comiéndoselo. Te dice que el cuerpo es enorme y no se acaba rápido. Que quiere ser su serpiente, su familia.",
        "Antes, te había dado otra tarea. Un tónico para borrarle la memoria a Rya, su hija adoptiva. La madre que te pidió envenenar a su hija ahora se está comiendo al padre. [short pause] Y tú eras de la familia.",
        "Y si en ese mismo viaje aceptaste el juramento de Varré, el de la máscara blanca, la cosa no mejora. Te da el Favor del Señor de la Sangre, una bandera blanca que tienes que empapar en sangre de doncella.",
        "Su descripción lo dice con un desprecio muy suyo. Bastará con la sangre de la doncella de cualquier otro, ya que después de todo, no sirves a ninguna. [short pause] Varré te explica que, normalmente, el rito exige matar a tu propia doncella. Tú solo tienes que usar la de otro.",
        "Puedes mancharla en el cadáver de una doncella sentada en la Iglesia de la Inhibición. O, si lo prefieres, puedes matar tú mismo a una doncella que todavía esté viva. Guarda ese detalle. Vuelve en el número dos.",
    ]},
    {"id": "p4c", "frases": [
        "Antes de dejar el volcán, tres detalles más de esa casa. El primero, el tónico que Tanith te dio para su hija. Su descripción: un regalo del blasfemo Rykard para Lady Tanith, quien por desgracia no pudo darle uso. Y debajo, una frase entre comillas. Mi señor, no podría haber mayor angustia que olvidarte.",
        "Tanith no pudo usarlo para olvidar a su señor. Pero borrarle la memoria a Rya, su hija adoptiva, una serpiente, eso sí le pareció buena idea. Y el recado se lo dio a la visita. [short pause] A ti.",
        "Le des el tónico a Rya, la mates o te niegues, te pagan con el mismo talismán, el Pesar de Daedicar. Su descripción habla de una mujer que se entregó a todos los tipos imaginables de adulterio y placer impío, dando a luz a una infinidad de grotescos hijos. [short pause] Esa es tu propina, decidas lo que decidas.",
        "El segundo detalle es la Máscara de consorte. Su descripción cuenta que Tanith fue la única humana que permaneció al lado de Rykard cuando se transformó en la serpiente blasfema. Y que fue entonces cuando quedó cautivada por él. [short pause] A unas les gustan las flores. A ella, las escamas.",
        "El tercero. Si después de verla comiéndose a su señor decides atacarla, Tanith muere de un solo golpe. Y entonces te invade el Caballero de Tanith. [short pause] Lo de la familia iba en serio.",
        "Y para que no pienses que lo de sicario era cosa de la mansión: en Elphael, tutor del Árbol Hierático, junto a un estanque de putrefacción, hay dos signos en el suelo. El signo dorado te lleva a ayudar a Millicent, y el signo rojo te manda a matarla a ella y también a sus hermanas. El pago es un talismán, la Prótesis de Millicent. [short pause] Ya ni hace falta carta. Basta con un signo rojo.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. [short pause] El ladrón de almas.",
        "En el video de Godrick te contamos cómo se cosía brazos ajenos. Y su recuerdo lo describe así: un hombre débil que ansiaba adquirir poder mediante la grotesca práctica de la realización de injertos.",
        "Ahora mira tu inventario. Llegaste a las Tierras Intermedias sin doncella, sin runas, sin nada. Y saliste con las Grandes Runas de cinco semidioses, sus recuerdos, sus armas y sus hechizos. [short pause] Godrick se cosía brazos. Tú te cosiste almas.",
        "Empieza por la Academia de Raya Lucaria. En lo alto de la Gran Biblioteca, sentada entre libros flotantes, está Rennala, la Reina de la Luna Llena. Abrazando un huevo de ámbar.",
        "Su marido, Radagon, la dejó para casarse con Márika. Y cuando se fue, el corazón de Rennala se fue con él. La academia que ella había conquistado se rebeló, y la encerró en su propia biblioteca.",
        "Tú entras, matas a sus alumnos, la tiras al suelo, y te llevas la Gran Runa de los Nonatos. Su descripción: los hijos renacidos de Rennala fueron todos frágiles y su vida efímera. Seres imperfectos, cada uno de ellos.",
        "Lo curioso es que Rennala ni siquiera es semidiosa. Gideon te lo comenta como quien no quiere la cosa. Le quitaste la runa a una madre abandonada que no tenía por qué tenerla.",
        "Y después, no la dejas en paz. Vuelves cada tanto, con unas lágrimas en la mano, para que te haga renacer y te cambie los atributos. La reina de la luna llena, convertida en tu estilista.",
    ]},
    {"id": "p3d", "frases": [
        "Y fíjate en lo que dice durante la pelea. No te habla como a un enemigo. Te habla con ternura, como a una palomita, y te promete que pronto te hará nacer de nuevo. [short pause] Tú vienes a robarle, y ella te quiere de hijo.",
        "A mitad del combate le habla a su amado. Le dice que no tenga miedo, que ella lo sostendrá. Y cuando todo termina, lo último que dice no es para ti. Es para su hija. Su pequeña Ranni. Su querida hija.",
        "Y el huevo que abraza todo el tiempo es la runa. Su descripción: huevo ámbar custodiado por Rennala, la Reina de la Luna Llena. Gran Runa de semidioses sin nacer. Era lo único que le quedaba del marido que se fue. [short pause] Y tú se lo quitaste de los brazos.",
        "Ranni lo dejó dicho así, llamándote maldito intruso: haz que corra la voz de la última reina de Caria, Rennala de la Luna Llena, y de la magnificencia de la noche que conjuró. [short pause] Y corriste la voz, sí. Le contaste a todo el mundo que la reina te cambia los atributos.",
    ]},
    {"id": "p3b", "frases": [
        "Luego está Radahn, en Caelid. El Azote de las Estrellas. El general que, según su recuerdo, aprendió la magia de gravedad en su juventud. Todo para no tener que abandonar nunca a su querido aunque escuálido corcel.",
        "Ahora es un gigante podrido por la putrefacción escarlata, que perdió la razón. Y aquí hay que ser justos: Radahn quería morir con honor, y el festival era para eso. Pero su Gran Runa hacía algo más.",
        "La Gran Runa arde para detener el avance de la putrefacción roja. Y mientras Radahn vivía, sus estrellas se quedaban quietas en el cielo. Cuando lo matas, empiezan a moverse otra vez. Una cae en Necrolimbo y abre un cráter enorme.",
        "Tú le quitaste el tapón al cielo. Y la grieta que dejó la estrella la usaste para bajar a robar en una ciudad subterránea. [short pause] Productivo, eso hay que reconocerlo.",
        "Pero lo peor no es lo que le quitas a cada semidiós. Es lo que haces con lo que te sobra. Por las Tierras Intermedias caminan unos edificios enormes con patas. Los Mausoleos errantes.",
        "Los protegen soldados sin cabeza. Su armadura cuenta que se la cortaron ellos mismos, para seguir sirviendo a sus amos en la muerte. Y el sobretodo que llevan lo dice así: la campana del mausoleo tañe en constante pesar por los semidioses sin alma.",
        "Son tumbas. Tumbas vivas de semidioses. Y tú rompes las montañas de calaveras que tienen en las patas, lo haces caer, entras, y lo usas para duplicar el recuerdo de otro semidiós. [short pause] Una tumba sagrada, usada de fotocopiadora.",
    ]},
    {"id": "p3e", "frases": [
        "Hay siete Mausoleos errantes en el juego. Solo los que cargan una campana te dejan duplicar el recuerdo de un semidiós. Uno por mausoleo. [short pause] Hasta la fotocopiadora tiene límite.",
        "Y con el recuerdo en la mano, vas con la Lectora de Dedos Enia. Cada recuerdo lo anuncia en su descripción: el poder de su homónimo puede ser liberado por la Lectora de Dedos. Le entregas el alma de un semidiós, y a cambio te llevas su arma o su hechizo. Así sacaste el Rencor de Rykard, con sus campeones dentro.",
        "Márika ya se lo había advertido a sus hijos. En un eco que encuentras en un Lugar de Gracia, les habla a los semidioses, sus hijos amados. Y les dice que, si no llegan a ser nada, serán abandonados. Que solo quedarán como sacrificios.",
        "Ellos no llegaron a ser nada. Y el que pasó a cobrar los sacrificios fuiste tú. [short pause] Márika escribió la regla. Tú la aplicaste, semidiós por semidiós.",
    ]},
    {"id": "p3f", "frases": [
        "Y ya que hablamos del Rencor de Rykard, su descripción no termina en las fauces. Sigue. Estos espíritus se manifiestan a partir del rencor de los héroes que sufrieron un final violento. Y en el interior de las entrañas de la serpiente, se convirtieron en sus semejantes.",
        "Los campeones de la mansión no solo murieron dentro de la serpiente. Se volvieron parte de ella. Y tú, cuando lanzas el hechizo, los sacas de ahí para que vuelvan a morir. [short pause] Otra vez trabajando para alguien. Ahora, para ti.",
        "Cada vez que lo lanzas, lanzas a los que fueron antes que tú a esa audiencia. Tú también ibas en esa lista. [short pause] La diferencia es que tú llegaste con más hambre que la serpiente.",
    ]},
    {"id": "p3c", "frases": [
        "Y hay un semidiós al que no le robas nada. Le das de comer. En el Santuario de la bestia, en Montedrago, al norte de Caelid, vive Gurranq, el clérigo bestia. Un lobo enorme, devorado por su propia hambre.",
        "Te pide Raíz mortuoria. Una raíz que, según su descripción, despierta a quienes viven en la muerte. Él la recoge y la devora. Hay nueve en el juego. Y por cada una, te paga.",
        "Al principio la acepta con hambre. Luego algo cambia. Tras la cuarta raíz, se lanza contra ti. Cuando se calma, te pide que la guardes. Te dice que no quiere volver a olvidar. Que ese apetito es su pecado. Que por favor, basta.",
        "Y tú vuelves. Con la quinta. Con la sexta. Hasta la novena. Porque la recompensa es buena. Y con la última, Gurranq pregunta si esto, por fin, es lo que se siente pecar. Y se va. Con el hambre como única compañía.",
        "Gurranq es Maliketh, la Hoja Negra, el que guardaba la Runa de la Muerte. Y KingInsect le dio voz en los comentarios: mi única atrocidad fue confiar en una mujer que nunca me amó.",
        "King, Maliketh tenía otra atrocidad. Confiar en ti. Te pidió por favor que pararas, y tú le llevaste cinco raíces más. [short pause] Márika le rompió el corazón. Tú le rompiste la dieta.",
        "Rennala, Radahn, Gurranq y cada tumba que pasea por ahí. No mataste para defenderte. Mataste para coleccionar. Y Oswaldo nos pidió que contáramos las historias de los personajes secundarios. Oswaldo, aquí las tienes. Todos acaban mal. Y casi siempre acaban mal por culpa tuya.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. [short pause] Le diste de comer ojos.",
        "Si la hija de Edgar, la chica ciega del Puente del Sacrificio, murió en tu partida, en Liurnia aparece otra chica. Junto al acantilado frente al humedal. Es ciega, tiene la misma cara y lleva puesta la misma ropa. Se llama Hyetta.",
        "Te pide ayuda. Quiere llegar a una luz lejana que no puede ver. Y para encontrar el camino, necesita comer una fruta muy concreta. La Uva Shabriri. Tú tienes una. Se la das.",
        "Ahora lee la descripción de la uva. Un globo ocular amarillento y supurante de lo enfermizo. Por fuera está reseco y su interior es blando, como una gran uva demasiado madura. Y abajo: dáselo a la doncella ciega para guiarla hasta la luz distante.",
        "Lo que acabas de darle es un ojo. [long pause] Le estás dando de comer ojos humanos a una chica ciega. Y no uno. Le llevas la segunda, sacada del sótano de unas ruinas. Y la tercera.",
        "La tercera la llevaba encima Edgar, el vengador. El padre de la chica ciega del puente. El hombre que enloqueció cuando su hija murió te invade, lo matas, y le quitas la uva. Para dársela a la chica idéntica a su hija.",
        "¿Y de dónde salen las uvas? En Velo Tormentoso, pasada la sala del trono, hay un espíritu sentado junto a una de ellas. Llama a una doncella, a su querida doncella, y le ruega que tome sus uvas. [short pause] Los dueños de los ojos se los ofrecen. Tú solo haces el reparto.",
    ]},
    {"id": "p2d", "frases": [
        "Con la primera uva, Hyetta te regala un gesto. Se llama Como desees. [short pause] Muy apropiado. Le diste exactamente lo que deseaba, sin preguntar qué era.",
        "Con la segunda, te cuenta cómo son los que le dan las uvas. Le ponen encima sus manos temblorosas. Aúllan sin palabras. Y le acarician los ojos con suavidad. A ti no te pareció raro. Seguiste buscando uvas.",
        "El nombre de la uva tampoco es casualidad. En las Ruinas de Zamor, en los Picos de los gigantes, aparece Shabriri, metido en el cuerpo de Yura, el cazador de Dedos Sangrientos. Y el talismán que lleva su nombre, el Pesar de Shabriri, cuenta su historia.",
        "Se dice que a este hombre, que se llamaba Shabriri, le arrancaron los ojos como castigo por sus calumnias y, con el tiempo, la plaga de la llama de la locura llegó a habitar sus cuencas vacías. [short pause] Un hombre sin ojos. Una uva que es un ojo. Y una chica ciega que se los come.",
        "Y Hyetta tiene muy claro lo que espera de ti. Te cuenta que los que le dieron las uvas deseaban no haber nacido nunca. Y te pide que seas su señor. Que lo fundas todo, como Señor del Caos. [short pause] No te pidió que la salvaras. Te pidió que acabaras con todo. Y tú le seguiste llevando fruta.",
    ]},
    {"id": "p2b", "post": 9.0, "frases": [
        "Al llegar a la tercera, el juego no te deja seguir hasta que le dices la verdad. Tú eliges decírselo: lo que se ha estado comiendo son ojos humanos.",
        "Ella no se lo cree. Balbucea que no puede ser, que todas esas personas. Que esos ruidos que oía eran eso. Y mientras te alejas, ella se dobla y vomita.",
        "Y aun así sigue. Te pide un ojo más. El del caballero Vyke. Otro Sinluz, uno al que consumió la llama frenética. Su descripción: globo ocular del caballero Vyke, inflamado y amarillento. Te invade junto a la Iglesia de la Inhibición, lo matas, y le sacas el ojo.",
        "Con ese último ojo, Hyetta te lleva a su destino. Debajo de Leyndell, en el Subsuelo de los marginados, hay una puerta sellada. La Cámara de la llama frenética. Te quitas toda la ropa, porque la puerta solo se abre así. Abres la puerta. Y unos dedos gigantes te abrazan.",
        "Los Tres Dedos. Te dan la llama del caos. La que, si la abrazas hasta el final, lo funde todo en uno. Y cuando vuelves, Hyetta te pide una última cosa. Que la toques con la llama. Que la quemes.",
        "Y tú la tocas. Ella grita que sus ojos se derriten. Y al final, te da las gracias, porque por fin pudo tocarlos. Escúchala.",
    ]},
    {"id": "p2c", "frases": [
        "Lo único que queda en el suelo es un sello y unas piedras de la llama frenética. Tú le diste los ojos. Tú le diste la verdad. Y tú la quemaste. [short pause] Y ella te dio las gracias.",
        "Y si eras de los de Varré, recuerda la bandera blanca. Hyetta es una de las doncellas que puedes matar para teñirla de rojo. La chica que vomitó por los ojos que tú le diste servía también como trapo de sangre.",
        "Hay quien dice que Hyetta es Irina, la hija de Edgar, vuelta de la muerte. El juego nunca lo confirma. Pero si lo fuera, le habrías dado de comer el ojo que llevaba su propio padre. [short pause] Mejor no pensarlo mucho.",
        "Franko escribió que los problemas de pronunciación son lo de menos al lado de todo el trabajo que tienen estos videos. Franko, gracias. Este costó más que los otros. Es difícil contar las atrocidades de alguien que está viendo el video.",
        "Y antes del número uno, algo rápido. De cada cien personas que ven estos videos, unas cinco están suscritas. Ya pasamos los novecientos, y la meta es mil. Karlos escribió que poco a poco esta comunidad va subiendo. Si llegaste hasta aquí, ayúdalo a subir un poco más. Suscribirte no te pide ningún ojo.",
    ]},
    {"id": "p1", "post": 10.0, "frases": [
        "Y llegamos al número uno. [short pause] La atrocidad que no pudiste evitar de ninguna manera.",
        "Las otras cuatro eran opcionales. Podías no beber del frasquito, no aceptar los encargos, no dar las uvas, no volver con más raíces. Esta no. [short pause] Esta la cometió cada persona que llegó al final de Elden Ring.",
        "Todo empieza con un trato. Cuando conoces a Melina, ella te ofrece ser tu doncella. Convertir tus runas en poder y ayudarte a buscar el Círculo de Elden. Y te pone una sola condición. Solo hace falta que me lleves contigo hasta el pie del Árbol Áureo.",
        "Tú aceptas. Recorres el mundo entero. Matas a Morgott en Leyndell. Y llegas al Árbol. Pero está cerrado por espinas. Para abrirlo hay que quemarlo. Y el único fuego capaz de hacerlo está en lo más alto del mundo. En la Forja de los gigantes.",
        "Subes a los Picos de los gigantes. Matas al último Gigante de fuego. Y en la Forja, Melina te pregunta si estás preparado para cometer un pecado capital.",
        "Tú dices que sí. Ella apoya la mano sobre ti un momento. Le ordena al Árbol Áureo que arda, por el nuevo señor. Te da las gracias por haberla traído hasta la Forja, hasta aquí arriba. [short pause] Y se despide. Escúchala.",
    ]},
    {"id": "p1b", "frases": [
        "La yesca era ella. Para quemar el Árbol hacía falta un sacrificio, y Melina se lanzó al fuego para que tú pudieras seguir. Su condición era que la llevaras al pie del Árbol. [short pause] La llevaste a la hoguera.",
        "Y no hay otro camino. Si te niegas, no avanzas. El juego no tiene final para quien deja el Árbol en paz. Hasta Shabriri te lo restriega. Te dice que estás a punto de sacrificar algo precioso, la vida de una doncella, para convertirte en señor. Lo quiera ella o no.",
        "Y te ofrece la otra salida. Que la yesca seas tú. Que heredes la llama frenética, la de Hyetta, y quemes el Árbol con tu propia carne. Así Melina se salva.",
        "Pero entonces quemas algo más que un árbol. La llama del caos no distingue. Lo funde todo, todo lo que separa y distingue a una cosa de otra. Y Melina te abandona. Te dice que ya no eres digno, se despide de ti y de Torrentera, y te deja una promesa.",
        "Si te alzas como Señor de la Llama Frenética, te va a matar. Y si llegas a ese final, lo cumple con sus propias palabras. Señor de la Llama Frenética. Te buscaré, por muy lejos que vayas. Para darte lo que mereces, la Muerte que está escrita.",
        "Esas eran tus dos opciones. Quemar a la chica que te ayudó, o quemar el mundo y que esa misma chica te jure la muerte. [short pause] Y elegiste. Todos elegimos.",
    ]},
    {"id": "p1d", "frases": [
        "Y Melina te lo había dicho con todas sus letras. Te he servido como doncella del dedo, pero no puedo ofrecerte enseñanzas. No soy ninguna doncella. [short pause] No era tu doncella. Era tu yesca, con contrato.",
        "Y te había avisado. Antes de la Forja te pidió que no pensaras en la yesca, que de eso se encargaba ella. Y reconoció que te estaba pidiendo cometer un pecado capital. Enia, la Lectora de Dedos, ya lo había explicado: para que la llama queme el Árbol hace falta un sacrificio. El de alguien que vislumbra la llama.",
        "Y si heredaste la llama frenética y luego te arrepientes, hay un remedio. La Aguja de Miquella. Se usa en la arena del Señor dragón Placidusax, en Farum Azula. Su descripción: capaz de subyugar a la llama frenética una vez heredada, lo cual permite engañar al destino.",
        "Engañar al destino, sí. Al Árbol, no. Para llegar a esa arena ya tuviste que pasar por la Forja. La aguja te quita la llama de encima. [short pause] El incendio se queda donde estaba.",
        "Y eso vale para todos los finales del juego, sin excepción. Era de fragilidad. Era de los nacidos en la oscuridad. Era del orden. Bendición de la desesperación. Señor de la Llama Frenética. Era estelar. Seis finales. [short pause] Y en los seis, el Árbol ya ardió.",
    ]},
    {"id": "p1c", "frases": [
        "Y cuando bajas de Farum Azula, ves lo que dejaste. Leyndell, la capital del Reino, la que defendía Morgott, la que tenía al Árbol de techo, se llama ahora Leyndell, capital cinérea. Calles cubiertas de ceniza. Todo gris.",
        "Ni siquiera el final más oscuro se libra. El del Zampaheces, el asesino del sótano, se llama Bendición de la desesperación. Le entregas cinco Maldiciones del semillero, las mismas que él dejaba en los cadáveres para que sus almas no volvieran al Árbol, y él crea una runa que lo maldice todo.",
        "Su descripción: la maldición vilipendiada durará eternamente, y los hijos del mundo, sus nietos y todas las generaciones venideras serán sus pústulas. Y para llegar a ese final también tuviste que pasar por la Forja.",
        "Así que hagas lo que hagas, el camino pasa por la hoguera. La doncella, o el mundo. Las Tierras Intermedias no se salvan contigo. Se queman contigo.",
        "Isaac escribió que cada video le gusta más que el anterior. Isaac, este es el único en el que el villano también deja comentarios. [short pause] Así que, ojo con lo que escribes.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. Drogaste a una guerrera y te quedaste con su marioneta. Mataste por encargo a tres Sinluz para una casa que se comía a sus campeones. Le robaste el alma a una madre abandonada y le seguiste dando raíces a un lobo que te pedía parar. Le diste de comer ojos a una chica ciega y la quemaste. Y prendiste fuego al Árbol con tu doncella de yesca.",
        "Y todo, para sentarte en un trono. Godrick quería coserse el poder de otros. Tú lo conseguiste. [short pause] Por eso a ti te llaman Señor del Círculo, y a él, el Injertado.",
        "Los comentarios se leen todos, de verdad, y con ellos se decide cada video. Este existe porque dos personas pidieron que el acusado fueras tú. Y esta voz se queda porque ustedes la votaron.",
        "Ya están apuntados Rykard, Godfrey y Godwyn, Maliketh, Rennala, el Zampaheces con Gideon, Midra, y hasta Bayle el Temible. Dinos en los comentarios cuál quieres que sea el siguiente.",
        "En el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn, Morgott, Mohg y Godrick. Y si te suscribes, nos acercas a los mil.",
        "Y la próxima vez que empieces una partida nueva y una voz te llame Sinluz, recuerda lo que hiciste la última vez. [long pause] Ellos sí se acuerdan.",
    ]},
]
CER_MAX_POR_FRASE = {'intro_0': 0.035, 'voto_3': 0.015, 'p5_1': 0.018, 'p5_2': 0.026, 'p5_3': 0.042, 'p5_4': 0.036, 'p5b_2': 0.02, 'p5b_5': 0.017, 'p5b_8': 0.014, 'p5c_0': 0.026, 'p5c_1': 0.023, 'p5c_2': 0.002, 'p5c_3': 0.029, 'p5c_6': 0.011, 'p4_3': 0.026, 'p4_4': 0.002, 'p4_5': 0.039, 'p4b_0': 0.022, 'p4b_1': 0.037, 'p4b_4': 0.021, 'p4c_0': 0.006, 'p4c_1': 0.031, 'p4c_2': 0.023, 'p4c_3': 0.02, 'p3_4': 0.015, 'p3b_1': 0.008, 'p3b_3': 0.002, 'p3e_0': 0.002, 'p3e_1': 0.022, 'p3e_2': 0.024, 'p3e_3': 0.037, 'p3f_0': 0.016, 'p3c_0': 0.015, 'p3c_3': 0.008, 'p3c_6': 0.02, 'p2_0': 0.039, 'p2d_0': 0.02, 'p2d_4': 0.016, 'p2b_3': 0.026, 'p2b_4': 0.023, 'p2c_1': 0.026, 'p2c_2': 0.021, 'p2c_4': 0.006, 'p1_3': 0.018, 'p1b_2': 0.036, 'p1b_3': 0.002, 'p1d_1': 0.006, 'p1d_2': 0.002, 'p1c_0': 0.037, 'p1c_1': 0.015, 'cierre_3': 0.07, 'cierre_4': 0.041}
GAP_MAX_POR_FRASE = {'intro_0': 0.73, 'voto_3': 0.51, 'p5_1': 0.63, 'p5_2': 0.54, 'p5_3': 0.52, 'p5_4': 0.73, 'p5b_2': 0.8, 'p5b_5': 0.57, 'p5b_8': 0.58, 'p5c_0': 0.61, 'p5c_1': 0.9, 'p5c_2': 0.51, 'p5c_3': 0.59, 'p5c_6': 0.54, 'p4_3': 0.51, 'p4_4': 0.48, 'p4_5': 0.57, 'p4b_0': 0.62, 'p4b_1': 0.69, 'p4b_4': 0.63, 'p4c_0': 0.61, 'p4c_1': 0.64, 'p4c_2': 0.82, 'p4c_3': 0.86, 'p3_4': 0.7, 'p3b_1': 0.59, 'p3b_3': 0.85, 'p3e_0': 1.1, 'p3e_1': 0.62, 'p3e_2': 0.51, 'p3e_3': 0.82, 'p3f_0': 0.73, 'p3c_0': 0.7, 'p3c_3': 0.5, 'p3c_6': 0.59, 'p2_0': 0.57, 'p2d_0': 0.61, 'p2d_4': 0.94, 'p2b_3': 0.79, 'p2b_4': 0.58, 'p2c_1': 0.51, 'p2c_2': 1.0, 'p2c_4': 0.48, 'p1_3': 0.46, 'p1b_2': 0.5, 'p1b_3': 0.6, 'p1d_1': 0.57, 'p1d_2': 0.52, 'p1c_0': 0.55, 'p1c_1': 0.5, 'cierre_3': 0.47, 'cierre_4': 0.39}
TAIL_MAX_POR_FRASE = {'intro_0': 1.08, 'voto_3': 0.86, 'p5_1': 0.95, 'p5_2': 0.8, 'p5_3': 0.94, 'p5_4': 0.63, 'p5b_2': 0.61, 'p5b_5': 0.63, 'p5b_8': 0.82, 'p5c_0': 0.93, 'p5c_1': 0.43, 'p5c_2': 1.09, 'p5c_3': 0.99, 'p5c_6': 1.05, 'p4_3': 0.87, 'p4_4': 1.08, 'p4_5': 0.87, 'p4b_0': 0.7, 'p4b_1': 0.86, 'p4b_4': 0.75, 'p4c_0': 1.04, 'p4c_1': 0.45, 'p4c_2': 0.8, 'p4c_3': 0.52, 'p3_4': 0.65, 'p3b_1': 1.05, 'p3b_3': 1.07, 'p3e_0': 1.09, 'p3e_1': 0.86, 'p3e_2': 0.69, 'p3e_3': 0.78, 'p3f_0': 0.61, 'p3c_0': 0.83, 'p3c_3': 1.03, 'p3c_6': 0.96, 'p2_0': 0.18, 'p2d_0': 1.13, 'p2d_4': 1.04, 'p2b_3': 0.93, 'p2b_4': 0.73, 'p2c_1': 0.74, 'p2c_2': 0.66, 'p2c_4': 1.1, 'p1_3': 0.83, 'p1b_2': 0.62, 'p1b_3': 1.1, 'p1d_1': 1.02, 'p1d_2': 1.06, 'p1c_0': 0.67, 'p1c_1': 0.92, 'cierre_3': 0.78, 'cierre_4': 0.81}

# 16-nov (relevo 1): estas 7 escenas se escribieron creyendo que faltaban minutos (la cifra de `seleccionar` solo contaba las
# frases aceptadas); con las 103 originales el video ya pasa de 24 min (~29). Se guardan aquí, fuera del video, por si sirven.
_EXTRA = {"p5c", "p4c", "p3d", "p3e", "p3f", "p2d", "p1d"}
ESCENAS_EXTRA = [e for e in ESCENAS if e["id"] in _EXTRA]
ESCENAS = [e for e in ESCENAS if e["id"] not in _EXTRA]
