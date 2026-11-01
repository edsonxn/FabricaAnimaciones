# -*- coding: utf-8 -*-
"""Sapiens con Wifi — «¿Cómo sobrevivían los humanos prehistóricos al FRÍO extremo?»  ~11 min, EN ESPAÑOL.
21-oct-2026 (el usuario): pasa al estilo PEGATINA FLOW (`docs/estilo_pegatina_flow.md`, como jalpa / asteroide_invisible /
wow_darrowshire): Flow pinta escenarios vacíos y hojas de personajes con ciclos; el código los anima como pegatinas. Guion
recortado de 15 a ~11 min quitando frases enteras (la voz de Dan ya grabada se reaprovecha; copia vieja en guion_15min.py.bak).
Antes (17-oct): secuencia Flow de imágenes, 15 min, hipótesis 3 de canales/formula/sapiens_con_wifi.md.
Referencias de fuera (ideas 17-oct-2026): Mango Explica SP «¿Cómo se mantienen calientes los iglús inuit a –50 °C?» (×13,6),
«Cómo sobrevivían los humanos prehistóricos a las noches lluviosas» (×5,8); Tiempos Antiguos «Edad de Piedra» (×12,3).
Gancho de segunda persona (tu calefacción / tu chamarra), mito «vivían en cuevas» anunciado al inicio y resuelto a mitad.
Nombres difíciles para Whisper (Kostenki, Sungir, Wonderwerk, Yana) se evitan en la VOZ: se dice el lugar, no el nombre.
Hechos usados (revisar DOI con Crossref al cerrar; lo que es hipótesis va con «quizá / los científicos creen»):
- Último Máximo Glacial (~20 000 años): Tierney et al. 2020, Nature — Tierra ~6 °C más fría en promedio; mar ~120 m más bajo;
  hielo de hasta ~3 km de grosor sobre Norteamérica y el norte de Europa.
- Humanos: especie de origen africano/tropical, sin pelaje y con mucho sudor (pérdida del vello corporal, Jablonski).
- Neandertales: cuerpo ancho y extremidades cortas (reglas de Bergmann y Allen), modelo de ropa de Wales 2012 (J Hum Evol:
  cubrían buena parte del cuerpo, quizá sin ropa ajustada).
- Inuit de Groenlandia: región TBX15/WARS2 heredada de denisovanos, relacionada con la grasa corporal y la grasa parda
  (Racimo et al. 2017, Mol Biol Evol); variantes FADS adaptadas a dieta rica en grasa marina (Fumagalli et al. 2015, Science).
- Fuego: cenizas y huesos quemados en una cueva de Sudáfrica ~1 millón de años (Wonderwerk; Berna et al. 2012, PNAS);
  uso habitual hace ~400 000 años; neandertales encendían fuego golpeando pirita con bifaces de sílex hace ~50 000 años
  (Sorensen et al. 2018, Scientific Reports).
- Camas: lechos de pasto sobre ceniza junto al fuego hace ~200 000 años (Border Cave, Sudáfrica; Wadley et al. 2020, Science).
- Lámparas de grasa animal: lámpara de arenisca de Lascaux (~17 000 años).
- Ropa: el piojo del cuerpo (vive en la ropa) se separó del de la cabeza hace al menos 83 000 y quizá 170 000 años
  (Toups et al. 2011, Mol Biol Evol).
- Agujas de hueso con ojo en Siberia hace > 40 000 años (Cueva Denisova; las de Europa son más tardías).
- Sungir (cerca de Vladímir, Rusia, > 30 000 años): entierros con miles de cuentas de marfil de mamut cosidas a la ropa,
  que dibujan gorros, camisas y pantalones (Trinkaus y Buzhilova; datación Marom et al. 2012, PNAS).
- Calzado: los dedos del pie se vuelven más finos con zapatos; en humanos de hace ~40 000 años (Tianyuan, China; Trinkaus y
  Shang 2008, J Archaeol Sci). Sandalias de corteza de Fort Rock (Oregón) ~9-10 000 años.
- Figurillas de Mal'ta (Siberia, ~23 000 años): algunas parecen llevar ropa con capucha (interpretación).
- Mito de las cuevas: la mayoría de los campamentos eran al aire libre o en la entrada de abrigos rocosos; el fondo de una
  cueva está oscuro y a la temperatura media del año (~10 °C en Europa templada).
- Círculo de huesos de mamut a orillas del Don, Rusia (Kostenki 11; Pryor et al. 2020, Antiquity): ~12,5 m de diámetro,
  huesos de más de 60 mamuts, ~25 000 años; dentro, carbón de coníferas y restos de plantas; uso discutido (refugio, almacén).
- Campamento por encima del círculo polar ártico hace ~32 000 años (río Yana, Siberia; Pitulko et al. 2004, Science).
- Iglú: la nieve atrapa aire y aísla; entrada en túnel más baja que el piso para que el aire frío (más pesado) se quede abajo;
  plataforma de dormir elevada; lámpara de aceite de foca; dentro puede estar decenas de grados más caliente que afuera.
- Parka inuit: dos capas de piel de caribú (pelo hacia dentro y hacia fuera), el pelo hueco del caribú atrapa aire.
- Hombre de Hielo (Alpes, ~5 300 años): zapatos con suela de piel de oso, empeine de ciervo y red interior rellena de pasto
  seco como aislante. Comer nieve gasta calor corporal (mejor derretirla). Un humano en reposo emite ~80-100 W.
- Hipotermia: por debajo de ~35 °C de temperatura corporal; tiritar; la mano se enfría primero (el cuerpo protege el centro).
"""

TITULO = "¿Cómo sobrevivían los humanos prehistóricos al FRÍO extremo?"
ARCHIVO = "frio_extremo"
ESTILO_VISUAL = "pegatina_flow"     # 21-oct-2026: Flow pinta fondos y hojas; el código anima pegatinas (docs/estilo_pegatina_flow.md)
DURACION = None
BPM = 90
GAP = 0.3
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.0, sfx=-24.0)
SUBTITULOS = False
ALIAS_QA = {}
FONETICA = {}
MUSICA = {}

# Falsos positivos de Whisper que se ajustan al oír las tomas (se llena tras `seleccionar`)
CER_MAX_POR_FRASE = {}

# Estilo común de TODOS los prompts de Flow (las pegatinas casan con los fondos). _prompts.py lo antepone a cada prompt.
FICHA = dict(
    estilo="Hand-painted 2D cut-out animation art, friendly educational cartoon picture-book style: bold clean dark-brown ink "
           "outlines, flat gouache colors with soft painted shading and visible paper grain; Ice Age palette of icy blues, snow "
           "whites, slate greys and warm fur browns with one warm campfire-orange accent; cozy, curious and a little funny, strong "
           "depth. The Ice Age, about 20,000 years ago: snowy steppes, glaciers, frozen rivers, woolly mammoths, reindeer, bone and "
           "stone tools, animal hides; no metal and no modern objects",
    personajes={
        "sapi": "Sapi, a cartoon prehistoric young man with a round peach-colored head, two big friendly dot eyes, messy brown "
                "hair, a simple brown fur tunic and fur boots, and a thin headband with a small white wifi symbol made of three "
                "curved arcs and a dot on the forehead",
        "neandertal": "a stocky cartoon Neanderthal man with a heavy brow ridge, a wide nose, long dark hair and a beard, a barrel "
                      "chest, short strong arms and legs, a rough grey fur wrap",
        "cazadora": "a cartoon Ice Age hunter woman with a round face, big dot eyes, two long black braids, a hooded light-brown "
                    "fur parka with a white fur trim, fur trousers and soft fur boots",
        "inuit": "a cartoon Inuit hunter with a round smiling face, big dot eyes, short black hair, a thick caribou-fur parka with "
                 "a wide hood ringed by white fur, fur mittens and sealskin boots",
    },
    cierre="No text, no letters, no words, no numbers, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.5)] * 10

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Warm, curious, lightly humorous documentary score for a hand-drawn cartoon about prehistoric survival in "
           "the Ice Age: wooden flute, marimba, soft hand drums, pizzicato strings, celesta, glassy bowed vibraphone "
           "for the cold, felt piano and upright bass. Playful and human, with moments of wonder and coziness. Never "
           "epic, never horror, no modern electronics.",
    escenas={
        "hook": ("Cozy modern evening turning into icy wonder: soft felt piano, then a glassy cold shimmer and a "
                 "gentle drum pulse as the question is asked.", 3),
        "hielo": ("Vast frozen world: slow bowed vibraphone and low strings like wind over ice, a small curious flute "
                  "figure, sense of scale.", 3),
        "cuerpo": ("Light explanatory groove: marimba ostinato, walking upright bass, brushed percussion, a wink of "
                   "humor.", 4),
        "fuego": ("Warmth arriving: crackling-feel hand drums, warm flute melody over pizzicato, glowing and "
                  "hopeful.", 4),
        "ropa": ("Busy and inventive: plucked strings like stitching, marimba patterns, celesta sparkles for each "
                 "discovery, playful.", 5),
        "cuevas": ("Myth-busting groove, confident and a bit cheeky: muted marimba and bass, then a big wondering "
                   "swell for the mammoth-bone house.", 4),
        "noche": ("Intimate winter night: soft wind texture, a slow lullaby on felt piano and flute, warm low strings "
                  "like people huddled together, very gentle.", 2),
        "artico": ("Brave and windy: low drums and cello, a long breath of cold air, tension, then a proud hopeful "
                   "phrase on flute.", 5),
        "iglu": ("Snug and clever: soft celesta and felt piano, a gentle groove, cozy like being inside out of the "
                 "wind.", 3),
        "tu": ("Clear friendly modern groove: light pizzicato and piano, marimba, a gentle smile.", 3),
        "outro": ("Return to the opening theme, now warm and resolved: celesta, felt piano and flute, a smile, then a "
                  "calm slow fade.", 3),
    },
    # tramos cortos (≤ ~90 s): Lyria entrega 98-100 s aunque pidas más (la_sena, 20-oct-2026)
    tramos=[
        (["hook"], "Begin from near silence. End on a held cold shimmering tone that can flow into the next piece. No loud ending."),
        (["hielo"], "Begin with a held cold tone. End on a sustained low tone that can flow into the next piece."),
        (["cuerpo"], "Begin softly with a low held tone. End on a sustained chord that can flow into the next piece."),
        (["fuego"], "Begin softly with a low held tone. End on a sustained warm chord that can flow into the next piece."),
        (["ropa"], "Begin gently with a held tone. End on a sustained chord that can flow into the next piece."),
        (["cuevas"], "Begin gently with a held tone. End on a sustained wondering chord that can flow into the next piece."),
        (["noche"], "Begin with a windy low held tone. End on a sustained calm chord that can flow into the next piece."),
        (["artico"], "Begin with a windy low held tone. End on a sustained hopeful chord that can flow into the next piece."),
        (["iglu"], "Begin gently with a held tone. End on a sustained cozy chord that can flow into the next piece."),
        (["tu", "outro"], "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "hook", "pre": 0.4, "frases": [
        "Piensa en la última vez que tuviste frío de verdad.",
        "Seguro te pusiste una chamarra, cerraste la ventana o prendiste la calefacción.",
        "Y en unos minutos, listo. El problema desapareció.",
        "Ahora imagina ese frío, pero sin chamarra, sin ventana y sin casa.",
        "Afuera hay cuarenta grados bajo cero, el viento corta la piel y la noche dura dieciocho horas.",
        "Así era el mundo de muchos de tus ancestros hace veinte mil años, en plena Edad de Hielo.",
        "Y aquí viene lo raro. El ser humano es un animal tropical.",
        "Nacimos en África, casi sin pelo y hechos para sudar, no para aguantar una ventisca.",
        "Un chimpancé tiene más abrigo natural que tú.",
        "Y aun así, nuestra especie llegó a Siberia, cruzó el Ártico y vivió junto a los glaciares durante miles de años.",
        "¿Cómo lo hizo un mono desnudo del trópico?",
        "Seguro te imaginas a esa gente metida en el fondo de una cueva, temblando junto a una fogata.",
        "Pues casi todo en esa imagen está mal. Y a mitad del video vas a ver por qué.",
        "Hoy vas a conocer los inventos que nos salvaron del frío, una casa hecha con huesos de más de sesenta mamuts, y el truco que hace que un iglú caliente.",
        "Pero primero, hay que entender a qué se enfrentaban.",
    ]},
    {"id": "hielo", "frases": [
        "Hace unos veinte mil años, la Tierra vivió el momento más frío de la última Edad de Hielo.",
        "Encima de lo que hoy es Canadá había una capa de hielo de hasta tres kilómetros de grosor.",
        "Otra cubría el norte de Europa. Donde hoy hay ciudades, había glaciares.",
        "Tanta agua estaba congelada, que el nivel del mar bajó unos ciento veinte metros.",
        "Y al sur de los glaciares se extendía una enorme pradera helada, seca y con viento constante.",
        "Era la estepa del mamut. Un paisaje lleno de mamuts lanudos, rinocerontes lanudos, renos, bisontes y caballos salvajes.",
        "Para un cazador había mucha comida. El problema era sobrevivir a la noche.",
        "Porque el frío no te mata de golpe. Te mata poco a poco.",
    ]},
    {"id": "cuerpo", "frases": [
        "Tu cuerpo funciona a unos treinta y siete grados. Si baja de treinta y cinco, empiezas a tener hipotermia.",
        "Primero tiritas. Tus músculos tiemblan solos para fabricar calor.",
        "Luego tu cuerpo hace algo cruel pero inteligente. Le quita sangre a las manos y a los pies para proteger el corazón y el cerebro.",
        "Por eso los dedos son lo primero que se congela.",
        "Si sigue bajando, te confundes, te da sueño y dejas de sentir frío. Y ese es el momento más peligroso.",
        "Ahora compáralo con los neandertales, que vivieron en Europa y Asia durante cientos de miles de años, antes que nosotros.",
        "Ellos sí tenían un cuerpo de clima frío. Eran bajitos, anchos, con el pecho como un barril y los brazos y piernas cortos.",
        "Esa forma pierde menos calor, igual que un oso es más redondo que un leopardo.",
        "Nosotros, en cambio, llegamos con cuerpos largos y delgados, perfectos para la sabana africana.",
        "Pero algunos grupos sí cambiaron con los milenios.",
        "Los inuit de Groenlandia llevan en sus genes una variante relacionada con la grasa que produce calor. Y los científicos creen que la heredaron de otra especie humana ya desaparecida.",
        "Pero la evolución es lentísima. Y el frío no espera.",
        "Así que nuestra especie hizo lo que mejor sabe hacer. No cambió el cuerpo. Inventó cosas.",
        "Y el primer invento fue el más poderoso de todos.",
    ]},
    {"id": "fuego", "frases": [
        "El fuego.",
        "En una cueva de Sudáfrica, los científicos encontraron cenizas y huesos quemados de hace un millón de años.",
        "Hace unos cuatrocientos mil años, el fuego ya era algo de todos los días en muchos campamentos.",
        "Y no solo lo aprovechaban. Sabían encenderlo.",
        "En Francia aparecieron hachas de piedra de neandertales, de hace unos cincuenta mil años, con marcas muy particulares.",
        "Los investigadores creen que las golpeaban contra un mineral llamado pirita para sacar chispas, como un encendedor de la Edad de Piedra.",
        "Una fogata no solo calentaba. También secaba la ropa mojada, que es una de las cosas más peligrosas cuando hace frío.",
        "Pero en la estepa helada había un problema enorme. Casi no había árboles.",
        "Así que en algunos campamentos quemaban lo que tenían a mano. Huesos.",
        "Los huesos de mamut tienen grasa por dentro, y arden despacio, como un tronco que no se acaba.",
        "Y con esa misma grasa fabricaban lámparas. En una famosa cueva de Francia, la de las pinturas de caballos y toros, apareció una de piedra de hace unos diecisiete mil años.",
        "Y alrededor del fuego aparece algo que tú también tienes. La cama.",
        "En otra cueva de Sudáfrica se encontraron camas de pasto de hace unos doscientos mil años, puestas sobre una capa de ceniza.",
        "La ceniza mantenía alejados a los insectos, y el pasto aislaba del suelo frío. Un colchón, básicamente.",
        "Pero el fuego tiene un defecto. No te lo puedes llevar puesto.",
    ]},
    {"id": "ropa", "frases": [
        "Para eso hacía falta el segundo gran invento. La ropa.",
        "El problema es que la ropa se pudre. Casi no queda nada de ella después de miles de años.",
        "Así que los científicos tuvieron que buscar pistas raras. Y una de las mejores fue un piojo.",
        "Hay un tipo de piojo que vive en tu cabeza, y otro que vive en la ropa y solo baja a la piel para comer.",
        "Ese piojo de la ropa no puede existir sin ropa. Así que, si averiguas cuándo apareció, sabrás cuándo empezamos a vestirnos.",
        "Al comparar sus genes, los investigadores calcularon que apareció hace al menos ochenta y tres mil años.",
        "O sea que llevamos muchísimo tiempo vistiéndonos. Y un piojo nos lo contó.",
        "Al principio, seguramente eran pieles echadas encima, como una capa.",
        "Los neandertales probablemente se cubrían así. Abrigaba, pero dejaba pasar el aire por todas partes.",
        "La gran revolución fue un objeto pequeñito. La aguja de hueso con ojo.",
        "Las más antiguas que se conocen aparecieron en Siberia, y tienen más de cuarenta mil años.",
        "Con una aguja puedes coser piezas a la medida. Mangas, capuchas, pantalones. Ropa ajustada que no deja escapar el calor.",
        "Y sabemos cómo era gracias a unas tumbas de Rusia, de hace más de treinta mil años.",
        "Ahí enterraron a un hombre y a dos niños, cubiertos con miles de cuentas de marfil de mamut.",
        "Las cuentas estaban cosidas a la ropa, y quedaron en el sitio exacto donde estuvo la tela.",
        "Al ver cómo estaban acomodadas, los arqueólogos pudieron dibujar el atuendo. Tenían gorro, camisa, pantalones y botas.",
        "Era un traje completo para la nieve, y además decorado. Hace treinta mil años ya había moda.",
    ]},
    {"id": "cuevas", "frases": [
        "Y ahora sí, el mito. ¿De verdad vivían en cuevas?",
        "No mucho. La palabra cavernícola nos engañó.",
        "Lo que pasa es que en las cuevas los restos se conservan mejor. Por eso encontramos tantos ahí.",
        "Pero el fondo de una cueva es oscuro, húmedo y está siempre a la misma temperatura, que en Europa ronda los diez grados.",
        "La gente solía acampar en la entrada, donde había luz y salía el humo, o directamente al aire libre.",
        "Y en la estepa, donde no había cuevas, hicieron algo increíble. Construyeron casas.",
        "A orillas del río Don, en Rusia, los arqueólogos excavaron un círculo gigante hecho con huesos de mamut.",
        "Mide unos doce metros y medio de diámetro. Es más grande que muchas salas de una casa moderna.",
        "Y para levantarlo usaron huesos de más de sesenta mamuts. Cráneos, mandíbulas, colmillos, apilados como ladrillos.",
        "Tiene unos veinticinco mil años, y se hizo en una de las épocas más frías de la Edad de Hielo.",
        "Los científicos todavía discuten para qué servía. Quizá era una casa, quizá un almacén de comida, o un lugar de reunión.",
        "Piénsalo. No había árboles para hacer vigas, así que usaron el material más grande que tenían. El esqueleto de un mamut.",
        "Nada se desperdiciaba. La carne era comida, la grasa era combustible, los huesos eran paredes y el marfil era joyería.",
    ]},
    {"id": "noche", "frases": [
        "Pero tener una casa no basta. Hay que pasar la noche.",
        "Imagina una noche de invierno en uno de esos campamentos, hace veinticinco mil años.",
        "El sol se fue temprano. Afuera, el viento sopla sobre la estepa y la nieve golpea las pieles de la choza.",
        "Lo primero era revisar la ropa. Si algo estaba mojado de sudor o de nieve, se ponía a secar junto al fuego.",
        "Porque la ropa mojada roba el calor del cuerpo mucho más rápido que el aire.",
        "Luego, el agua. Parece fácil, porque hay nieve por todas partes. Pero comer nieve es un error.",
        "Para derretirla dentro de ti, tu cuerpo gasta el calor que tanto le cuesta producir. Por eso la derretían junto al fuego.",
        "Y a la hora de dormir, nadie dormía solo.",
        "Todos se acostaban juntos, apretados bajo las mismas pieles, con los niños en medio, donde hace más calor.",
        "Un cuerpo humano en reposo da más o menos el mismo calor que una bombilla de cien vatios. Diez personas juntas son una pequeña estufa.",
        "Era la calefacción más antigua del mundo. La gente.",
    ]},
    {"id": "artico", "frases": [
        "Con fuego, ropa cosida y casas, nuestra especie se atrevió a ir más lejos que nunca.",
        "En el norte de Siberia, por encima del círculo polar ártico, hay un campamento de hace unos treinta y dos mil años.",
        "Ahí, en invierno, el sol no sale durante semanas. Y aun así, la gente cazaba mamuts, renos y liebres.",
        "Esa gente no sobrevivió por ser más fuerte. Sobrevivió porque llegó preparada.",
        "Y una parte clave de esa preparación estaba en el plato.",
        "En el frío extremo, el cuerpo quema muchísima energía solo para mantenerse caliente.",
        "Por eso la grasa era el alimento más valioso de todos. Más que la carne magra.",
        "Rompían los huesos para sacar el tuétano, y los hervían para soltar la grasa.",
        "Muchos miles de años después, otros grupos usaron ese conocimiento para cruzar el puente de tierra entre Siberia y Alaska.",
        "Y así, poco a poco, la especie que nació en el trópico terminó viviendo de un extremo al otro del planeta.",
        "Pero para quedarse en el Ártico de verdad, había que inventar una última cosa. Una casa hecha de frío.",
    ]},
    {"id": "iglu", "frases": [
        "El iglú.",
        "Suena absurdo. ¿Cómo te vas a calentar dentro de una casa hecha de nieve?",
        "Pero la nieve está llena de burbujas de aire. Y ya sabes lo que hace el aire quieto. Aísla.",
        "Un buen iglú se construye con bloques de nieve compacta, en espiral, hasta cerrar el techo en forma de cúpula.",
        "Y luego viene el truco más inteligente. La entrada.",
        "Se hace como un túnel, y más baja que el piso donde se duerme.",
        "El aire frío pesa más que el caliente, así que se queda abajo, atrapado en el túnel, y no sube.",
        "Y la plataforma para dormir queda en lo más alto, justo donde se junta el aire tibio.",
        "Con el calor de los cuerpos y una lámpara de aceite de foca, por dentro puede estar decenas de grados más caliente que afuera.",
        "Afuera puede haber cuarenta bajo cero, y adentro, alrededor de cero. Para alguien envuelto en pieles de caribú, eso es comodidad.",
        "Nadie estudió física para inventarlo. Fue conocimiento acumulado por generaciones, que los abuelos enseñaban a los nietos.",
        "Y es exactamente la idea de tu casa. Paredes que aíslan, poco aire frío entrando y una fuente de calor en el centro.",
    ]},
    {"id": "tu", "frases": [
        "Entonces, ¿qué tienes tú de ellos?",
        "Tu ropa con costuras existe gracias a una aguja de hueso de hace cuarenta mil años.",
        "Tu colchón es la cama de pasto sobre la ceniza.",
        "Y tu calefacción es la fogata que alguien mantuvo encendida toda la noche para que el grupo no se congelara.",
        "Pero no intentes nada de esto. Ellos también perdían dedos, se enfermaban y morían de frío.",
        "Si alguna vez te sorprende una helada, busca refugio, quítate la ropa mojada y no te quedes dormido a la intemperie.",
        "Y si ves a alguien muy confundido y temblando, llama a emergencias.",
        "Nuestros ancestros no ganaron porque fueran más duros que el frío. Ganaron porque compartían lo que sabían.",
        "Una lámpara, una aguja o un túnel de nieve no valen nada si nadie te enseña a usarlos.",
    ]},
    {"id": "outro", "post": 2.2, "frases": [
        "Así que la próxima vez que te pongas una chamarra, detente un segundo.",
        "Detrás de ella hay una aguja de hueso, una casa de mamut a orillas del Don, y un cazador del Ártico agachándose para entrar a su iglú.",
        "Tú no eres el primero en tener frío.",
        "Eres el último de una larga cadena de gente que se negó a congelarse.",
        "Eres un Homo sapiens. Con wifi.",
    ]},
]
