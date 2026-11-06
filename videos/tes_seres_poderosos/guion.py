# -*- coding: utf-8 -*-
"""GUION — «Los 20 seres más PODEROSOS de Tamriel» (Crónicas de Tamriel, 5-nov-2026).
Motor SECUENCIA YT (gameplay por beat; docs/estilo_secuencia_yt.md § REGLA DE ORO y § Tamriel). Datos verificados en UESP:
_investigacion.md. Ref. de formato: Qewvr «Most Powerful Beings» (×6,5); lo daédrico rinde ×5 en el canal.
El usuario (5-nov-2026): ~24 minutos, las SIETE voces de ElevenLabs compitiendo (fórmula de tes_sentinel_teaser y
tes_dwemer_desaparicion: Johnny presenta) y el Humano tras el Telón (voz clonada del usuario, cuentas 2 y 3) SOLO en UN dato.
Recuento real de los votos de Sentinel (comentarios hasta el 5-nov): el Profeta 8 · Hope 2 · MariCarmen 2 · Johnny 2 ·
Edoardo, José y Mario 0 → el Profeta, que gana, se queda con los SEIS primeros puestos (los seres cósmicos).
Comentarios (≤ 10 días, ninguno repetido de otro video): votos (@saidavalera403, @amadeoamaya7606, @alleyva, @6Mr.Dead9),
crítica con burla: «No pude con la de pronunciación posh» (@ebre1976); el Humano entra por @krisstianblackgao1726 («cómprese el
micrófono y siga con su voz»); agradecimientos @EdwinRpoc, @pierodelgadomontes1568, @Enki-11, @raif5729, @PokeGoDLegacy.
Turbo, corchetes SIN [whispers] ni [excited].
"""

TITULO = "Los 20 seres más PODEROSOS de Tamriel (las 7 voces no se ponen de acuerdo)"
ARCHIVO = "tes_seres_poderosos"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HMCmDsbKeaSZp5LMOYKR", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"), referencia=r"C:\chatterbox_voices\Sarcastica.mp3",
           por_cuenta={2: "GUEeiSJYQQdbv0NJ86Im", 3: "hCU4QZdzzUliy58ezPBz"})   # el Humano tras el Telón (clon del usuario) en las cuentas 2 y 3
# ElevenLabs dice el inglés nativo: aquí lo que se oyó mal en videos anteriores (quejas del público: «Oblivión» agudo, «jarl»)
FONETICA = {"Oblivion": "Oblívion", "jarl": "yarl", "Jarl": "Yarl", "CHIM": "Chim", "Jyggalag": "Yígalag",
            "2E 896": "segunda era, ochocientos noventa y seis", "3E 433": "tercera era, cuatrocientos treinta y tres"}

CER_MAX_POR_FRASE = {"voces_7": 0.154, "ag1_0": 0.104, "ag1_1": 0.047, "ag1_2": 0.104, "ag1_3": 0.168, "cierre_1": 0.064, "cierre_3": 0.118, "cierre_6": 0.052, "cierre_9": 0.004, "cr1_0": 0.061, "cr1_1": 0.164, "cr1_4": 0.021, "dato_0": 0.061, "dato_1": 0.04, "p10_2": 0.025, "p11_3": 0.014, "p12_5": 0.033, "p13_4": 0.042, "p15_1": 0.022, "p15_3": 0.022, "p16_1": 0.046, "p16_2": 0.02, "p17_0": 0.035, "p17_1": 0.024, "p17_6": 0.053, "p18_0": 0.019, "p18_3": 0.056, "p18_5": 0.04, "p19_0": 0.118, "p19_3": 0.058, "p19_4": 0.026, "p1_5": 0.016, "p20_0": 0.03, "p20_1": 0.017, "p3_3": 0.028, "p3_4": 0.018, "p4_0": 0.053, "p4_3": 0.023, "p4_4": 0.024, "p5_5": 0.018, "p7_0": 0.032, "p7_1": 0.033, "p7_2": 0.027, "p8_0": 0.021, "p8_1": 0.086, "p8_2": 0.017, "p8_3": 0.049, "p8_4": 0.028, "p9_0": 0.019, "p9_2": 0.033, "voces_1": 0.023, "voces_2": 0.226, "voces_4": 0.018}   # Whisper escribe mal los nombres (s2, 5-nov-2026: hipótesis leídas)
TAIL_MAX_POR_FRASE = {"cierre_9": 1.21, "p11_3": 1.06}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={"scene-072": .6},   # sonido original: rugido de Alduin (s3; 113 con audio bajaba de 1,6 s)
    recorte_por={},
    yt=dict(sufijo="", min_s=40, max_min=240, alto=1080,
            evitar_canales=["BLUxCHEESE", "TIMENG", "The Glitch Report", "Swezz Cheese", "Barrett Knives",
                            "Saika", "Max Modded", "Ero-sama", "OrcCorp", "DCARR GAMING",
                            "Spoiler Alert Theater", "PIXEL STORYZ", "Pixel Storyz", "Syzleaf", "RGR29"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial (Skyrim, Oblivion y Morrowind de Jeremy Soule + ESO; armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Un nigromante que quiso ser dios. Un dragón que se come el mundo. Un gólem de latón que conquistó un continente entero.",
        "Un príncipe que te cambia la cara por un queso, y un dios que ve el tiempo como tú ves un pasillo.",
        "[amused] Hoy toca la pregunta que más pelea en los comentarios. ¿Quién es el ser más poderoso de Tamriel?",
        "Veinte seres, del último al primero. Todo comprobado en UESP, con las fuentes en la descripción.",
        "Y para que nadie se queje del ranking, lo hemos hecho entre siete. Siete voces, siete opiniones, y una sola lista.",
        "[sarcastic] Spoiler: no nos pusimos de acuerdo. Esta es la tabla que salió de la pelea. Y quédate hasta el número uno, porque no es un dios. O sí. Depende de quién esté soñando.",
    ]},
    {"id": "voces", "frases": [
        "Primero, el marcador. Votación de Sentinel, ya cerrada. Hope, dos votos. MariCarmen, dos. Yo, Johnny, dos.",
        "[deadpan] Edoardo, José y Mario. Cero. Otra vez cero. Esto ya es una tradición.",
        "[short pause] Y el Profeta. Ocho votos. Ocho. @saidavalera403, @amadeoamaya7606, @alleyva, y un largo etcétera.",
        "Así que el Profeta se lleva los seis primeros puestos. Los dioses. Que sí, que ya lo sé, le pega.",
        "[deadpan] Edoardo. El dieciocho y el diecisiete. Cero votos, y sigo siendo el único que lee las fuentes.",
        "José. Dieciséis y quince: dos dioses de Morrowind. Uno falso. O los dos.",
        "Mario. Catorce y trece. Un dragón, y el que se lo cargó. Prometo correr menos.",
        "[amused] Hope. Doce, once y diez. Un hombre que se hizo dios, un dios de latón, y un príncipe que no quiero nombrar.",
        "[deadpan] MariCarmen. Nueve, ocho y siete. Tres príncipes daédricos. Me entiendo bien con ellos.",
        "Yo soy el Profeta. Del seis al uno. [short pause] Ocho votos. Estaba escrito.",
        "[sarcastic] Y a mí me tocan los dos últimos, que nadie quería. Empezamos.",
    ]},
    {"id": "p20", "frases": [
        "Número veinte. Mannimarco, el Rey de los Gusanos.",
        "Es el nigromante más famoso de Tamriel. Según UESP, empezó en la isla de Artaeum, con la Orden Psijic. Y lo expulsaron por practicar nigromancia, hacia el año doscientos treinta de la segunda era.",
        "Allí conoció a Vanus Galerion, el que fundaría el Gremio de Magos. Galerion acabó fundando una escuela. Mannimarco, un culto a la muerte.",
        "En Oblivion lo tienes al final de la misión del Gremio de Magos. Sus nigromantes llenan Cyrodiil de gemas de alma negras, que atrapan almas de personas.",
        "En Elder Scrolls Online es uno de los grandes villanos: el aliado de Molag Bal en el plan para tragarse Tamriel.",
        "Y en Daggerfall, la leyenda dice que llegó más lejos: que en la Distorsión del Oeste ascendió y se convirtió en un dios. El Dios de los Gusanos.",
        "[deadpan] Un mortal que se hace dios, y está en el último puesto. Así de cara está esta lista.",
    ]},
    {"id": "p19", "frases": [
        "En el diecinueve, el mago que más ha vivido. Divayth Fyr.",
        "Un mago telvanni de Morrowind con más de cuatro mil años. Vio caer a los dwemer y sigue en su torre, Tel Fyr, como si nada.",
        "Bajo esa torre tiene el Corprusarium, un hospital para los enfermos de corprus, la plaga de Dagoth Ur. Y es el único en todo Morrowind que encontró la cura.",
        "La cura es la que te da a ti, el Nerevarine, para que puedas seguir la profecía. Sin Divayth, no hay final de Morrowind.",
        "Vive con cuatro mujeres a las que llama sus hijas: Alfe, Beyte, Delte y Uupse. Y no son sus hijas. Son clones de él mismo.",
        "[deadpan] Cuatro mil años, la cura de una plaga divina, y clones. Si eso es el puesto diecinueve, imagina lo que viene.",
    ]},
    {"id": "p18", "frases": [
        "[deadpan] Gracias, Johnny. Ahora, en serio. Número dieciocho. Miraak, el primer Sangre de Dragón.",
        "Antes que tú, hubo otro. Miraak era un sacerdote dragón en Solstheim, al servicio de los dragones. Y los traicionó.",
        "Su grito más temido era Doblegar Voluntad: con él, hasta un dragón le obedecía y le servía de montura.",
        "Para escapar de sus amos, hizo un pacto con Hermaeus Mora, y pasó miles de años en Apocrypha, un reino infinito de libros.",
        "En el contenido Dragonborn, vuelve a Solstheim: esclaviza a los pueblos y les hace levantar su templo en trance, con las piedras sagradas de la isla.",
        "Al final lo derrotas en Apocrypha. Y Hermaeus Mora, su propio señor, lo atraviesa con un tentáculo. Le dice que sabía que lo iba a traicionar.",
        "[deadpan] Y aquí va la lección. Cuando te vas a traicionar a un dios del conocimiento, no lo pienses en voz alta. Lo sabe todo.",
    ]},
    {"id": "p17", "frases": [
        "En el diecisiete, el caballero que cayó de las estrellas. Pelinal Whitestrake.",
        "Es el campeón de Alessia, la esclava que se rebeló contra los ayleid, los elfos que gobernaban Cyrodiil en la primera era.",
        "Mató en duelo a reyes hechiceros ayleid, uno tras otro. Y la Canción de Pelinal dice que su armadura de cruzado venía del futuro.",
        "Su gran enemigo fue Umaril el Sin Plumas, un hechicero ayleid. Pelinal lo venció en la Torre Oro Blanco, pero quedó herido de muerte, y los ayleid lo cortaron en ocho pedazos.",
        "[short pause] Y su cabeza siguió viva, atormentada por la magia ayleid. Según la canción, le contó a su amigo Morihaus que Umaril no estaba muerto del todo.",
        "En Oblivion lo vives en Los Caballeros de los Nueve: juntas su armadura de cruzado, reliquia a reliquia, y terminas el trabajo contra Umaril.",
        "Y hay una teoría: que Pelinal era un avatar de Shezarr, el dios perdido. Guárdate el nombre. Va a volver.",
    ]},
    {"id": "cr1", "frases": [
        "Una pausa, que hay correo. @ebre1976 nos escribió: no pude con la de pronunciación posh. Ahí paré el video.",
        "[amused] ¿La posh? Yo no soy. Yo tengo hache.",
        "[deadpan] Yo menos. Yo amenazo, no pronuncio.",
        "[deadpan] Bueno. Si Ebre paró el video, no está oyendo esto. Así que lo digo con total libertad: sí, soy yo. Y pronuncio Whitestrake perfectamente.",
        "Gracias igualmente, Ebre. Si algún día vuelves, el posh te guarda el sitio.",
    ]},
    {"id": "p16", "frases": [
        "José. Número dieciséis. Dagoth Ur, el dios que salió de una montaña.",
        "Antes se llamaba Voryn Dagoth, y era el mejor amigo de Nerevar, el gran héroe de los chimer.",
        "En la Montaña Roja, se negó a entregar las herramientas de Kagrenac y se quedó a solas con el Corazón de Lorkhan. Siglos después, despertó convertido en un dios.",
        "Desde allí envió la plaga a todo Vvardenfell, el corprus, y levantó la Sexta Casa, un culto de durmientes que soñaban con él.",
        "El Tribunal tuvo que levantar la Valla Fantasma, una muralla mágica alrededor de la montaña, y mantenerla con su propio poder durante siglos.",
        "Y en su forja, Dagoth Ur construía su propio dios de latón, Akulakhan. Iba a liberar Morrowind del Imperio, a la fuerza.",
        "Cuando llegas al Corazón, te recibe como a un viejo amigo: bienvenido, Luna y Estrella. Te esperaba.",
    ]},
    {"id": "p15", "frases": [
        "En el quince, el dios poeta. Vivec.",
        "Vivec es uno de los tres dioses del Tribunal, junto a Almalexia y Sotha Sil. Los tres se hicieron dioses con el mismo Corazón de Lorkhan.",
        "Su ciudad tiene su nombre, Vivec, en Vvardenfell. Y encima de ella, durante siglos, flotó una roca gigante: el Ministerio de la Verdad.",
        "Era un pedazo de luna, Baar Dau, que según una de las leyendas Sheogorath lanzó contra la ciudad. Y Vivec lo detuvo en el aire. Y lo dejó ahí.",
        "En Morrowind, es Vivec quien te entrega el guantelete de Kagrenac, Wraithguard, para que puedas tocar el Corazón sin morir.",
        "Y escribió un libro que nadie entiende del todo: los Treinta y Seis Sermones de Vivec. Según muchos fans, en él admite que sabe que vive dentro de un sueño.",
        "[sighs] Cuando el Corazón se destruyó, perdió su poder. Y años después, la roca cayó. Así de grande era lo que sostenía.",
    ]},
    {"id": "p14", "frases": [
        "[amused] Muy profundo, José. Mario. Número catorce. Alduin, el Devorador del Mundo.",
        "Es el primogénito de Akatosh, el dios dragón del tiempo. Y en la era de los dragones, gobernó Skyrim con su culto de sacerdotes.",
        "Los antiguos nórdicos se rebelaron con un grito hecho para tumbar dragones, y con un Pergamino Antiguo lo lanzaron fuera del tiempo, en la Garganta del Mundo.",
        "No lo mataron. Solo lo mandaron al futuro. Y aterrizó justo en el año de Skyrim: cuarta era, doscientos uno. En Helgen, justo cuando te iban a cortar la cabeza.",
        "[mischievously] Desde entonces resucita dragones con un grito sobre sus túmulos, y en Sovngarde se come las almas de los nórdicos muertos, para hacerse más fuerte.",
        "Su nombre lo dice todo: Alduin, el que se come el mundo. Y según las profecías, cuando llegue su hora, eso es lo que hará.",
    ]},
    {"id": "p13", "frases": [
        "Y en el trece, el que se lo cargó. Tú. El último Sangre de Dragón.",
        "[short pause] Sí. Te pongo por encima de Alduin. Porque cuando pelean, ganas tú. Las cuentas son así de simples.",
        "Absorbes el alma de cada dragón que matas. Y con cada alma, aprendes gritos que a los Barbas Grises les cuesta años.",
        "Vences a Alduin en la Garganta del Mundo con el grito Abatir Dragón, y luego lo rematas en Sovngarde, junto a tres héroes nórdicos.",
        "Después vas a Apocrypha y vences a Miraak, el primer Sangre de Dragón, el del puesto dieciocho. Le robas los dragones y hasta el alma.",
        "Y por si fuera poco, puedes acabar al frente de todos los gremios a la vez, casarte, adoptar, y robar todas las cucharas de Skyrim.",
        "[deadpan] El ser más poderoso de Skyrim no pudo con un tipo que llevaba cuarenta quesos en el bolsillo. Piénsalo.",
    ]},
    {"id": "ag1", "frases": [
        "Y ahora, gracias. @EdwinRpoc dice que fue un excelente video. Gracias, Edwin.",
        "[amused] @pierodelgadomontes1568 se fijó en la montaña de arena de Sentinel: el dieciséis veces el detalle personificado. Con razón tardaron ocho años.",
        "@Enki-11 está de acuerdo: esa montaña fue un mensaje directo a los fans. Y @raif5729 lo resume así: migajas. Me encanta.",
        "Y a @PokeGoDLegacy le gustó la voz de Hope. Que no se entere el Profeta.",
        "Los leemos todos. Los que votan, los que corrigen y los que se ríen. Con ellos mejoramos cada video.",
    ]},
    {"id": "dato", "frases": [
        "Y este es para alguien especial. @krisstianblackgao1726 le dice al humano tras el telón: cómprese el micrófono y siga con su voz, que la habilidad se desarrolla con el uso.",
        "Gracias, Krisstian. Micrófono nuevo no tengo. Pero un dato sí. Uno solo.",
        "El siguiente de la lista es el único dios de Tamriel que fue un hombre de carne y hueso. Y desde el Concordato de Oro Blanco, en el Imperio está prohibido rezarle.",
        "[deadpan] Un dato. Y ya. Que el micrófono es caro.",
    ]},
    {"id": "p12", "frases": [
        "[amused] Gracias, señor del micrófono. Me toca. Número doce. Talos.",
        "Antes de ser dios, fue Tiber Septim. Un general que unió las provincias y fundó el tercer Imperio de Tamriel.",
        "Terminó la segunda era conquistándolo todo: desde Roca Alta hasta el Pantano Negro. Por primera vez, un solo hombre gobernaba Tamriel.",
        "Al morir, subió a los cielos y se convirtió en el noveno Divino. Ocho dioses, y uno que empezó siendo mortal.",
        "Por eso los altos elfos del Thalmor lo odian. En el tratado de paz con el Imperio, el Concordato de Oro Blanco, exigieron prohibir su culto.",
        "[mischievously] Y en Skyrim ves sus santuarios por todas partes. Si le rezas, te da un descanso en tus gritos. Y el Thalmor persigue a quien lo hace.",
        "Por eso los Capas de la Tormenta pelean. Y por eso, en esta lista, Talos está por encima de todos los mortales.",
    ]},
    {"id": "p11", "frases": [
        "En el once, el arma con la que Talos conquistó el mundo. El Numidium.",
        "Un gólem gigante de latón, construido por los dwemer para ser un dios nuevo. Lo contamos en el video de los dwemer, pero merece su puesto.",
        "Tiber Septim lo puso en marcha con la Mantella como corazón, y lo lanzó contra las islas de Estivalia, el último reino que le quedaba.",
        "Según UESP, su asalto a Alinor acabó con la resistencia de los altos elfos en menos de una hora. Una isla entera de magos. En una hora.",
        "Y en la tercera era, cuatrocientos diecisiete, al reactivarlo varias potencias a la vez, el tiempo se rompió: la Distorsión del Oeste, la de Daggerfall y Sentinel.",
        "[deadpan] Un robot que conquista un continente y rompe el tiempo. Y no llega al top diez. Ahí lo dejo.",
    ]},
    {"id": "p10", "frases": [
        "En el diez, el primero de los príncipes daédricos. Molag Bal, el príncipe de la dominación.",
        "Los príncipes daédricos son dieciséis, y no son dioses de este mundo: cada uno tiene su propio reino en Oblivion.",
        "El de Molag Bal es Coldharbour, un reflejo helado y muerto de Nirn. Y según UESP, fue él quien creó a los primeros vampiros.",
        "En Elder Scrolls Online intentó lo imposible: el Planemeld, tragarse Nirn entero y fundirlo con Coldharbour, con anclas oscuras que caían del cielo sobre las ciudades.",
        "En Skyrim te encierra en una casa abandonada de Markarth y te obliga a elegir. Si le obedeces, te da su maza.",
        "[sighs] Es tan malo que ni los demás príncipes lo soportan. Y eso, viniendo de príncipes daédricos, es mucho decir.",
    ]},
    {"id": "p9", "frases": [
        "[deadpan] Gracias, Hope. Mi turno. Número nueve. Mehrunes Dagon, el príncipe de la destrucción.",
        "Es el villano de Oblivion. En la tercera era, cuatrocientos treinta y tres, su secta, el Alba Mítica, asesinó al emperador Uriel Septim séptimo.",
        "Sin emperador, se rompió la barrera, y se abrieron puertas de Oblivion por todo Cyrodiil. La primera ciudad en caer fue Kvatch.",
        "Al final, se presentó en persona en la Ciudad Imperial. Un gigante de cuatro brazos, pisando el Distrito del Templo.",
        "Y para pararlo hizo falta un dios. Martin Septim rompió el Amuleto de los Reyes y se convirtió en el avatar de Akatosh.",
        "En Skyrim te deja su arma, la Navaja de Mehrunes. Tiene una probabilidad de matar al enemigo de un solo tajo. A cualquiera.",
        "[deadpan] Y pierde contra un dragón de fuego. No le digáis que se lo he dicho.",
    ]},
    {"id": "p8", "frases": [
        "En el ocho, el príncipe de la locura. Sheogorath. O debería decir, Jyggalag.",
        "Sheogorath es el loco simpático: el de las Islas Temblorosas, el que te da el Wabbajack, el que habla de queso a todas horas.",
        "Pero en Shivering Isles se descubre el secreto: Sheogorath es una maldición. Los demás príncipes condenaron a Jyggalag, el príncipe del orden, a convertirse en el príncipe de la locura.",
        "Cada era, Jyggalag se libera y arrasa las Islas: la Marcha Gris. Y en Oblivion, tú rompes el ciclo, Jyggalag se va libre, y te quedas con el trono.",
        "[amused] El Héroe de Kvatch se convierte en Sheogorath. Y en Skyrim, si entras en la mente del emperador Pelagius, encuentras a Sheogorath sentado, tomando el té. Y por cómo habla, muchos creen que es el mismo héroe.",
        "Así que en este puesto hay dos príncipes, y un humano que acabó siendo uno de ellos.",
    ]},
    {"id": "p7", "frases": [
        "En el siete, el que lo sabe todo. Hermaeus Mora.",
        "Es el príncipe del conocimiento, y su reino, Apocrypha, es una biblioteca infinita. Sus Libros Negros te llevan dentro si los lees.",
        "No tiene cara: es una masa de ojos y tentáculos. Y fue el señor de Miraak, el del dieciocho, durante miles de años.",
        "En Skyrim te da el Oghma Infinium, un libro de poder. Y en el camino, Septimus Signus, el erudito que lo buscaba, acaba hecho ceniza.",
        "Al final de Dragonborn, te cobra un precio: los secretos de los Barbas Grises. Eres su nuevo campeón, lo quieras o no.",
        "[deadpan] Y aquí va la razón por la que lo pongo por encima de los otros dos. Dagon destruye y Sheogorath enloquece. Pero Mora ya sabía que iban a hacerlo.",
    ]},
    {"id": "campana", "frases": [
        "Antes del top seis, un dato. De cada cien que ven este canal, unos cuarenta y cuatro no están suscritos.",
        "Somos seis mil cuatrocientos noventa. Si te suscribes, pasamos de siete mil camino de diez mil. Y yo amenazo menos.",
    ]},
    {"id": "p6", "frases": [
        "Llegamos al seis. El primero de los dioses. Magnus.",
        "Magnus fue el arquitecto de la creación. Él dibujó los planos de Mundus, el mundo mortal.",
        "Pero cuando vio lo que le costaba crearlo, huyó. Y al escapar, abrió un agujero en el cielo. Ese agujero es el sol.",
        "Sus seguidores, los Magna-Ge, huyeron detrás de él. Y cada uno abrió su propio agujero. Esos agujeros son las estrellas.",
        "La magia es su esfera, y por eso los magos de Tamriel lo veneran. Cada vez que miras el sol en Skyrim, estás mirando el agujero de su huida.",
        "En el Colegio de Hibernalia encuentras el Ojo de Magnus, y en Laberintia su bastón. Un dios que se fue, y dejó las llaves puestas.",
    ]},
    {"id": "p5", "frases": [
        "En el cinco, el dios dragón del tiempo. Akatosh.",
        "Es el primero de los dioses, y el principal de los Nueve. Y el padre de los dragones, Alduin incluido.",
        "Es el tiempo mismo. Por eso, cuando el tiempo se rompe, lo llaman una ruptura de dragón.",
        "En Oblivion, cuando Martin rompe el Amuleto de los Reyes, Akatosh baja en forma de dragón de fuego, se enfrenta a Mehrunes Dagon en plena ciudad, y lo expulsa a Oblivion.",
        "[short pause] Y según la tradición, el alma de dragón del Sangre de Dragón es una bendición de Akatosh. Todo lo que gritas, se lo deberías a él.",
        "Alduin, Dagon, el Sangre de Dragón. Tres de esta lista, y los tres le deben algo a Akatosh.",
    ]},
    {"id": "p4", "frases": [
        "En el cuatro, el dios que nos engañó a todos. Lorkhan.",
        "Él convenció a los demás dioses de crear el mundo mortal. Y cuando vieron que era una trampa que los atrapaba, lo mataron.",
        "Trinimac le arrancó el corazón, y Auriel lo disparó lejos con una flecha. Donde cayó se formó la Montaña Roja. El mismo corazón de Dagoth Ur y del Tribunal.",
        "Cada pueblo lo llama de una forma. Los nórdicos le dicen Shor, y su salón es Sovngarde. Los imperiales le dicen Shezarr. Sí, el de Pelinal.",
        "[short pause] Y aquí todo encaja. El corazón de Lorkhan hizo dioses a Dagoth Ur y al Tribunal, movió el Numidium, y Pelinal pudo ser su avatar.",
        "Un dios muerto, y casi media lista vive de lo que dejó. Por eso está en el cuatro.",
    ]},
    {"id": "p3", "frases": [
        "En el tres, antes de los dioses. Padomay.",
        "Al principio de todo había dos fuerzas: Anu, lo que se queda quieto, y Padomay, lo que cambia.",
        "De la sangre de Padomay salieron los daedra. Molag Bal, Dagon, Sheogorath, Hermaeus Mora. Todos son hijos del cambio.",
        "Muchos lo identifican con Sithis: el vacío, el padre al que reza la Hermandad Oscura cada vez que mata.",
        "Cada vez que en Skyrim oyes a la Madre Noche, estás oyendo el culto de lo que dejó Padomay.",
    ]},
    {"id": "p2", "frases": [
        "En el dos, su eterno rival. Anu.",
        "Anu es la quietud, la luz, el orden. Y en el Anuad, es el que gana. Akatosh, Magnus, los Nueve: todos le deben su existencia.",
        "Según el Anuad, los dos hermanos lucharon. Anu desterró a Padomay fuera del tiempo, y con los restos de aquella pelea formó Nirn. Y de la sangre de los dos, salieron los dioses.",
        "Tamriel, Skyrim, tú. Todo está hecho de esa pelea. Por eso Anu está por encima de Padomay. Por poco. Por muy poco.",
    ]},
    {"id": "p1", "frases": [
        "Y el número uno. El que está soñando todo esto.",
        "Según una de las ideas más famosas del lore, todo el universo de The Elder Scrolls es un sueño. El sueño del Godhead, el primer soñador. UESP lo deja claro: su existencia está en disputa.",
        "Anu, Padomay, los dioses, los príncipes, tú. Todos estaríais dentro de ese sueño.",
        "Y hay una forma de saberlo y no desaparecer: se llama CHIM. Darte cuenta de que estás soñado, y aun así decir: yo soy.",
        "Se dice que Talos y Vivec lo consiguieron. Por eso uno se hizo dios y el otro paró una luna.",
        "[short pause] Así que el ser más poderoso de Tamriel no sale en ningún juego. Está fuera. Mirando. Como tú, ahora mismo.",
    ]},
    {"id": "cierre", "frases": [
        "Este es el podio. Anu, Padomay, y el que sueña. Y esta, la lista que salió de la pelea entre siete voces.",
        "Ahora te toca a ti. ¿Quién falta? ¿Quién sobra? ¿Azura, Boethiah, el Héroe de Kvatch? Déjalo en los comentarios.",
        "[sarcastic] Y vota otra vez. ¿Qué voz se queda? Johnny, Edoardo, Hope, José, Mario, MariCarmen o el Profeta. Un nombre, y listo.",
        "[amused] Hope. Con hache. Y con un voto nuevo de PokeGo.",
        "[deadpan] MariCarmen. Tres príncipes daédricos me respaldan.",
        "Mario. Corrí menos. Un poco menos.",
        "[deadpan] Edoardo. Posh, y orgulloso.",
        "José. Dos dioses de Morrowind, y cero votos. Arreglemos eso.",
        "Yo no pido votos. Me los dan.",
        "[sarcastic] Y el humano tras el telón dio su dato. Uno. Si quieres más lore, en el canal tienes los secretos de los dwemer. Suscríbete si aún no lo has hecho. Nos vemos en Tamriel.",
    ]},
]

# --- VARIAS VOCES (el usuario, 3/4/5-nov-2026): quién narra cada escena; las que no salen aquí, Johnny (VOZ) ---
VOCES = {   # nombre en pantalla: voice_id (biblioteca compartida de ElevenLabs, salvo el Humano tras el Telón = clon del usuario)
    "Johnny": "HMCmDsbKeaSZp5LMOYKR", "Edoardo": "YqZLNYWZm98oKaaLZkUA", "Hope": "tnSpp4vdxKPjI9w0GnoV",
    "José": "y2ijeTfmnXjzheHO6zeN", "Mario": "tomkxGQGz4b1kE0EM722", "MariCarmen": "YDDaC9XKjODs7hY78qEW",
    "el Profeta": "HNSF1CTQmub252yhXROX", "el Humano tras el Telón": "GUEeiSJYQQdbv0NJ86Im",
}
_POR_ESCENA = {"p18": "Edoardo", "p17": "Edoardo", "cr1": "Edoardo", "p16": "José", "p15": "José", "p14": "Mario", "p13": "Mario",
               "ag1": "Mario", "p12": "Hope", "p11": "Hope", "p10": "Hope", "p9": "MariCarmen", "p8": "MariCarmen",
               "p7": "MariCarmen", "campana": "MariCarmen", "p6": "el Profeta", "p5": "el Profeta", "p4": "el Profeta",
               "p3": "el Profeta", "p2": "el Profeta", "p1": "el Profeta", "cierre": "el Profeta"}
_POR_FRASE = {"voces_4": "Edoardo", "voces_5": "José", "voces_6": "Mario", "voces_7": "Hope", "voces_8": "MariCarmen",
              "voces_9": "el Profeta",
              "cr1_0": "Johnny", "cr1_1": "Hope", "cr1_2": "MariCarmen", "cr1_4": "Johnny",
              "ag1_3": "Hope", "dato_0": "Johnny", "dato_1": "el Humano tras el Telón", "dato_2": "el Humano tras el Telón",
              "cierre_2": "Johnny", "cierre_3": "Hope", "cierre_4": "MariCarmen", "cierre_5": "Mario", "cierre_6": "Edoardo",
              "cierre_7": "José", "cierre_9": "Johnny"}
NARRA = {}   # "escena_i": nombre de la voz (efectos.py pone la ficha de quién narra en cada cambio)
for _e in ESCENAS:
    for _i in range(len(_e["frases"])):
        _k = f"{_e['id']}_{_i}"
        NARRA[_k] = _POR_FRASE.get(_k) or _POR_ESCENA.get(_e["id"], "Johnny")
VOZ_POR_FRASE = {k: VOCES[v] for k, v in NARRA.items() if v != "Johnny"}
