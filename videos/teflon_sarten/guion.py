# -*- coding: utf-8 -*-
"""Plastitube (alias pieza_oculta) — «El cilindro vacío que seguía pesando lo mismo» (teflón).  Motor SECUENCIA.
Video de PRUEBA del canal en la Fábrica: ~6 min, TODO IMAGEN (Flow sin puntos de video el 7-oct-2026).
Ficha histórica (Science History Institute, American Chemical Society, National Inventors Hall of Fame, DuPont/Chemours):
Roy J. Plunkett (1910-1994), químico, 27 años; entró a DuPont en 1936; Jackson Laboratory, Deepwater, Nueva Jersey.
6-abr-1938: con su ayudante Jack Rebok abre un cilindro de tetrafluoroetileno (había preparado ~100 libras, guardadas en
cilindros pequeños en hielo seco, para un refrigerante nuevo); no sale gas, pesa lo mismo; lo sacuden, caen escamas blancas,
lo cortan con sierra: polvo blanco ceroso y resbaloso = PTFE (el gas polimerizó solo, a presión, con el hierro del cilindro
como catalizador). Inerte a casi todo ácido y disolvente, aguanta calor, bajísima fricción. Patente pedida en 1939,
concedida en 1941; marca «Teflon» 1945. Carísimo y difícil de moldear. Proyecto Manhattan: juntas y sellos resistentes al
hexafluoruro de uranio en la planta de difusión gaseosa de Oak Ridge; la producción se reservó al gobierno.
Francia, 1954: el ingeniero Marc Grégoire lo usa en su equipo de pesca; su esposa Colette le pide ponerlo en sus sartenes;
graba el aluminio con ácido para que el PTFE agarre; funda Tefal en 1956. Después: capa exterior de los trajes Apolo
(tela Beta recubierta de teflón), Gore-Tex (1969), injertos vasculares, aislamiento de cables, y la restauración de la
Estatua de la Libertad (1984-86: barrera de teflón entre la piel de cobre y la armadura). Medalla John Scott 1951: cada
invitado recibió un molde para panecillos recubierto de teflón.
Elementos prohibidos en imagen: nada posterior a cada época (ni plásticos de colores ni pantallas en 1938); sin logotipos
ni marcas; a las personas se las describe por oficio, nunca por nombre (filtro de «personas destacadas» de Flow).
"""

TITULO = "El cilindro vacío que seguía pesando lo mismo"
ARCHIVO = "teflon_sarten"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 96
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=0,          # todo imagen: Flow sin puntos de video
    clip_s=8,
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-teflon_sarten",
)

# Ficha visual del episodio: se repite PALABRA POR PALABRA en cada prompt donde aparezca (triple anclaje).
FICHA = dict(
    estilo="Diorama cinematográfico horizontal dieciséis nueve hecho íntegramente de plastilina artesanal stop-motion, "
           "textura mate con huellas de dedos visibles, escena a sangre que llena todo el encuadre de borde a borde, "
           "sin borde, sin marco, sin viñeta",
    personajes={
        "quimico": "un químico de plastilina de veintisiete años, delgado, de pelo castaño oscuro corto peinado de lado, "
                   "cara afeitada y cejas gruesas, con bata blanca de laboratorio abierta sobre camisa blanca y corbata "
                   "granate",
        "ayudante": "un ayudante de laboratorio de plastilina de unos cuarenta años, robusto, de pelo rubio muy corto, "
                    "con overol de trabajo azul grisáceo y camisa beige arremangada",
        "ingeniero": "un ingeniero francés de plastilina de unos cincuenta años, de pelo negro peinado hacia atrás y "
                     "bigote fino, con chaleco de punto verde oliva sobre camisa blanca",
        "esposa": "una mujer francesa de plastilina de unos cuarenta y cinco años, de pelo castaño ondulado hasta la "
                  "barbilla, con vestido azul de lunares blancos y delantal amarillo",
    },
    objeto="un cilindro pequeño de acero gris para gas, del tamaño de un termo, con una válvula de latón en la punta, "
           "sin etiquetas ni manómetro",
    epoca="laboratorio químico industrial de mil novecientos treinta y ocho en Nueva Jersey: mesas de madera oscura, "
          "matraces y tubos de vidrio, mecheros, báscula de platillos de hierro, lámparas colgantes de metal; sin "
          "plásticos de colores, sin pantallas, sin aparatos electrónicos",
    cierre="Sin texto, sin letras, sin números, sin logotipos, sin objetos modernos.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "gancho": dict(sabor="tension"), "promesa": dict(sabor="espacio"), "laboratorio": dict(sabor="espacio"),
    "cilindro": dict(sabor="tension"), "sierra": dict(sabor="tension"), "polvo": dict(sabor="espacio"),
    "pruebas": dict(sabor="esperanza"), "problema": dict(sabor="vacio"), "guerra": dict(sabor="tension"),
    "pesca": dict(sabor="espacio"), "sarten": dict(sabor="esperanza"), "cascada": dict(sabor="esperanza"),
    "cierre": dict(sabor="esperanza"),
}

# Música con Lyria adaptada al guion (python ../../nucleo/lyria_tramos.py): solo descripción musical, sin nombres ni palabras sensibles.
LYRIA = dict(
    estilo="Warm, curious, handmade documentary score for a stop-motion story about an accidental discovery: pizzicato strings, "
           "marimba, soft clarinet, felt piano, glockenspiel, light brushed percussion and a gentle upright bass. Playful but "
           "intelligent, never epic, never sad.",
    escenas={
        "gancho": ("A single ticking pizzicato note and a low held clarinet, puzzled and suspended, with one small questioning marimba figure. Almost empty.", 3),
        "promesa": ("The pulse appears: gentle marimba ostinato, upright bass enters, a feeling of a story about to begin.", 4),
        "laboratorio": ("Light everyday routine in a workshop: steady walking bass, pizzicato strings, small glockenspiel details, relaxed and tidy.", 4),
        "cilindro": ("The routine stops. Sparse and puzzled: isolated pizzicato notes, long quiet clarinet tone, pauses of near silence, a slow ticking.", 3),
        "sierra": ("Growing suspense with a mischievous edge: a quickening pizzicato pulse, low strings rising step by step, ending on one bright surprised chord.", 6),
        "polvo": ("Wonder and stillness after the surprise: soft felt piano arpeggio, glassy glockenspiel, then a brief deflated falling phrase.", 3),
        "pruebas": ("Playful experimenting montage: bouncy marimba and pizzicato pattern, each phrase ending on a little comic stop, growing curiosity.", 5),
        "problema": ("The energy drains away: slow solitary clarinet, sparse piano, dusty and quiet, an unanswered question at the end.", 2),
        "guerra": ("Serious and secretive: low steady pulse, muted strings, restrained snare brushes far away, tension building slowly, ending on a held tone.", 6),
        "pesca": ("A sunny change of scene: light accordion-like clarinet and pizzicato waltz, a riverside afternoon, gentle and charming.", 4),
        "sarten": ("The idea clicks: the waltz gathers momentum, marimba and piano join, bright and satisfied, a small triumphant flourish.", 6),
        "cascada": ("Open and uplifting: flowing piano arpeggios, warm sustained strings, glockenspiel sparkle, the widest and brightest moment.", 7),
        "cierre": ("Return to the opening figure, now warm and resolved: felt piano and soft pizzicato, a smile, then a calm ending.", 4),
    },
    tramos=[
        (["gancho", "promesa", "laboratorio", "cilindro", "sierra"],
         "Begin from near silence. End on a bright sustained chord that can flow into the next piece. No loud ending."),
        (["polvo", "pruebas", "problema", "guerra"],
         "Begin softly with a held tone. End on a sustained low tone that can flow into the next piece."),
        (["pesca", "sarten", "cascada", "cierre"],
         "Begin gently with a held tone. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Un químico abre la válvula de un cilindro lleno de gas.",
        "No sale nada.",
        "Lo pone en la báscula, y pesa exactamente lo mismo que cuando estaba lleno.",
        "El gas no se escapó. Sigue ahí dentro, pero ya no es un gas.",
        "Lo que encontró al partir ese cilindro terminó en una bomba atómica, en la Luna, y en tu cocina.",
    ]},
    {"id": "promesa", "frases": [
        "Y lo más extraño es que nadie lo estaba buscando.",
        "Durante años fue un material tan caro y tan raro, que casi nadie supo qué hacer con él.",
        "Esta es la historia del teflón, y del día en que un experimento fallido se negó a ir a la basura.",
    ]},
    {"id": "laboratorio", "frases": [
        "Abril de mil novecientos treinta y ocho. Nueva Jersey, Estados Unidos.",
        "Roy Plunkett tiene veintisiete años, y lleva apenas dos trabajando como químico en una gran compañía.",
        "Su tarea no tiene nada de heroica: encontrar un gas nuevo para los refrigeradores.",
        "Los primeros refrigeradores usaban gases venenosos o inflamables, y una fuga podía vaciar un edificio entero.",
        "La industria buscaba reemplazos más seguros, y cada compañía quería el suyo.",
        "Para sus pruebas, Plunkett prepara un gas incoloro, sin olor, y con un nombre casi imposible de pronunciar.",
        "Fabrica casi cincuenta kilos, y los reparte en pequeños cilindros de acero.",
        "Para que el gas no cause problemas, los guarda enterrados en hielo seco.",
    ]},
    {"id": "cilindro", "frases": [
        "La mañana del seis de abril, su ayudante conecta uno de esos cilindros al equipo.",
        "Abre la válvula.",
        "Silencio. Ni un soplo de gas.",
        "Meten un alambre por la válvula, por si está tapada. Pasa limpio.",
        "Entonces pesan el cilindro.",
        "La báscula marca lo mismo que el día en que lo llenaron.",
        "Cualquiera habría pensado en una fuga, habría tirado el cilindro y habría tomado el siguiente.",
        "Pero los números no cuadraban.",
        "Si el gas se había ido, ¿por qué el cilindro seguía pesando lo mismo?",
    ]},
    {"id": "sierra", "frases": [
        "Plunkett quita la válvula, voltea el cilindro y lo sacude.",
        "Caen unas pocas escamas blancas sobre la mesa.",
        "Nadie había metido nada blanco ahí dentro.",
        "Entonces toman una decisión muy poco elegante: cortarlo por la mitad con una sierra.",
        "No es la forma más segura de resolver una duda, pero sí la más rápida.",
        "El acero se abre, y adentro no hay gas.",
        "Las paredes están cubiertas por un polvo blanco, ceroso, tan resbaloso que se escapa entre los dedos.",
    ]},
    {"id": "polvo", "frases": [
        "El gas se había convertido, él solo, en un sólido.",
        "Encerradas a presión, sus moléculas se habían enganchado unas con otras, formando cadenas larguísimas.",
        "Y el hierro del propio cilindro había ayudado a encender la reacción.",
        "El experimento del refrigerante estaba arruinado.",
        "Meses de trabajo, convertidos en un puñado de polvo.",
        "Pero Plunkett hace lo que separa a un descubridor de alguien con mala suerte.",
        "En vez de limpiar la mesa, se pone a hacer pruebas.",
    ]},
    {"id": "pruebas", "frases": [
        "Le echa ácidos capaces de disolver metales. No pasa nada.",
        "Lo calienta. No se derrite como los demás plásticos.",
        "Intenta disolverlo en todo lo que hay en el laboratorio. No se disuelve en nada.",
        "Y además es uno de los materiales más resbalosos que alguien haya tocado.",
        "Casi nada se le pega. Ni el agua, ni el aceite, ni el pegamento.",
        "En su cuaderno, Plunkett anota con calma que ha obtenido un sólido blanco.",
        "No tiene idea de lo que acaba de encontrar.",
    ]},
    {"id": "problema", "frases": [
        "Suena como un material milagroso. Pero tenía un problema enorme.",
        "Fabricarlo costaba una fortuna, y nadie sabía cómo darle forma.",
        "No se podía fundir ni moldear como un plástico normal.",
        "La compañía registra la patente, y el polvo blanco se queda en un estante, sin un uso claro.",
        "¿Quién iba a pagar tanto por algo que no se pega a nada?",
    ]},
    {"id": "guerra", "frases": [
        "La respuesta llegó de un lugar que nadie esperaba.",
        "El proyecto más secreto de la Segunda Guerra Mundial.",
        "Para construir la bomba atómica, los científicos necesitaban separar uranio.",
        "Y para eso usaban un gas tan corrosivo, que se comía las juntas, los sellos y las válvulas de sus propias máquinas.",
        "Probaron un material tras otro. Todos se deshacían.",
        "Hasta que alguien recordó el polvo blanco que no reaccionaba con nada.",
        "De pronto, el descubrimiento sin clientes se volvió un secreto militar.",
        "Casi toda la producción se fue a fábricas escondidas, con kilómetros de tuberías.",
        "Y durante la guerra, casi nadie fuera de ahí supo que existía.",
    ]},
    {"id": "pesca", "frases": [
        "Cuando la guerra termina, el material recibe por fin un nombre comercial: teflón.",
        "Se usa en fábricas, en cables y en laboratorios.",
        "Nadie piensa en una cocina.",
        "Hasta que, en Francia, un ingeniero aficionado a la pesca lo usa para algo muy distinto.",
        "Cubre con teflón su equipo de pesca, para que el hilo no se enrede.",
        "Su esposa, Colette, lo mira trabajar, y le hace la pregunta que vale millones.",
        "Si eso evita que el hilo se pegue, ¿por qué no lo pones en mis sartenes?",
    ]},
    {"id": "sarten", "frases": [
        "El problema era evidente.",
        "¿Cómo pegas a una sartén algo que no se pega a nada?",
        "El ingeniero encuentra la forma.",
        "Graba el aluminio con ácido para dejarlo áspero, y el teflón queda atrapado en esos poros diminutos.",
        "Colette prueba la primera sartén, y el huevo se desliza como si flotara.",
        "En mil novecientos cincuenta y seis, fundan una empresa para vender la sartén a la que nada se le pega.",
        "En pocos años, vendían millones.",
    ]},
    {"id": "cascada", "frases": [
        "A partir de ahí, el polvo blanco apareció en todas partes.",
        "En los trajes de los astronautas que caminaron sobre la Luna.",
        "En telas impermeables que dejan respirar la piel.",
        "En venas artificiales que salvan vidas dentro de un quirófano.",
        "En los cables de los aviones y de las computadoras.",
        "Y hasta dentro de la Estatua de la Libertad, para separar su piel de cobre de su esqueleto de metal.",
    ]},
    {"id": "cierre", "frases": [
        "Roy Plunkett nunca encontró el gas para refrigeradores que estaba buscando.",
        "Encontró algo mejor, porque no tiró a la basura un cilindro que parecía vacío.",
        "Años después, le dieron una medalla por su descubrimiento.",
        "Y cada invitado a la ceremonia se llevó a casa un molde para panecillos cubierto de teflón.",
        "Así que la próxima vez que un huevo se deslice en tu sartén, acuérdate de aquella mañana.",
        "Una válvula abierta. Ni un soplo de gas.",
        "Y un químico que, en lugar de rendirse, tomó una sierra.",
        "Si te gustan las historias de inventos que nacieron por accidente, suscríbete.",
        "La próxima ya se está moldeando.",
    ]},
]
