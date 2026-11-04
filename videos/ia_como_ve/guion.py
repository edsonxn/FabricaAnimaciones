# -*- coding: utf-8 -*-
"""¿Cómo ve una IA? — video largo HORIZONTAL de Kuriox (~10 min), ACUARELA PINTADA A MANO POR CÓDIGO.

Pedido del usuario (4-nov-2026): «con el estilo de la ballena y arenas movedizas», explicar cómo una IA (un LLM con visión)
sabe qué hay en una imagen, sea del tipo que sea; que cualquiera lo entienda, cómo se llegó a eso y cómo funciona por dentro,
a nivel de red neuronal; horizontal; «que dure lo que tenga que durar».
Idea central: Kuri (la mascota, un robot) ES la IA. Una niña chibi le enseña la foto de un gato y le pregunta cómo lo supo;
el viaje es POR DENTRO DE LA CABEZA DE KURI: una torre de pisos (las capas) con neuronas-farolito que se encienden.
Cadena que el espectador debe salir sabiendo: píxeles → números → neurona (perillas) → filtro que barre → capas (bordes,
formas, partes, objetos) → entrenamiento (error y perillas) → datos (ImageNet) → parches + atención (transformers) → mapa
de significados que une imágenes y palabras (CLIP) → el modelo de lenguaje «lee» la imagen como palabras → límites.
Kit copiado de videos/arenas_movedizas/ (docs/estilo_acuarela_pincel.md); adaptarlo a 1920x1080.

Datos (verificados el 4-nov-2026; DOI comprobados en Crossref):
  - Foto de celular de 12 megapíxeles = 12 millones de píxeles × 3 colores (rojo, verde, azul, 0-255) = 36 millones de números.
  - Hubel y Wiesel, «Receptive fields of single neurones in the cat's striate cortex», J. Physiol. 148, 574 (1959),
    doi:10.1113/jphysiol.1959.sp006308: neuronas de la corteza visual del gato que responden a líneas con una inclinación
    concreta; Nobel de Medicina 1981.
  - Fukushima, Neocognitrón, Biol. Cybern. 36, 193 (1980), doi:10.1007/BF00344251: red por capas inspirada en ellos.
  - LeCun et al., «Backpropagation Applied to Handwritten Zip Code Recognition», Neural Comput. 1, 541 (1989),
    doi:10.1162/neco.1989.1.4.541: códigos postales escritos a mano; a finales de los 90 sus redes leían cheques en EE. UU.
  - Rumelhart, Hinton y Williams, Nature 323, 533 (1986), doi:10.1038/323533a0: retropropagación (repartir la culpa del error).
  - Deng, ..., Fei-Fei Li, «ImageNet», CVPR 2009, doi:10.1109/CVPR.2009.5206848: más de 14 millones de imágenes etiquetadas a
    mano (≈ 49 000 personas de 167 países vía Mechanical Turk, según Fei-Fei Li).
  - Krizhevsky, Sutskever y Hinton (AlexNet), CACM 60(6) 2017 / NeurIPS 2012, doi:10.1145/3065386: error top-5 15,3 % frente
    a 26,2 % del segundo; 60 millones de parámetros; entrenada en dos tarjetas gráficas de videojuegos (GTX 580).
  - Zeiler y Fergus, «Visualizing and Understanding Convolutional Networks», ECCV 2014, doi:10.1007/978-3-319-10590-1_53:
    capas tempranas = bordes y colores; intermedias = texturas y partes; profundas = objetos (caras de perro, ruedas).
  - He et al. (ResNet), CVPR 2016, doi:10.1109/CVPR.2016.90: 3,57 % de error en 2015; una persona entrenada ≈ 5,1 %
    (Karpathy, 2014; Russakovsky et al., IJCV 2015).
  - Dosovitskiy et al., «An Image is Worth 16x16 Words» (ViT), arXiv:2010.11929 (2020): la imagen en parches de 16×16 px.
  - Radford et al. (CLIP), arXiv:2103.00020 (2021): 400 millones de pares imagen-texto de internet.
  - Goodfellow, Shlens y Szegedy, arXiv:1412.6572 (2014): panda 57,7 % + ruido invisible → «gibón» 99,3 %.
  - Ribeiro, Singh y Guestrin (LIME), KDD 2016, arXiv:1602.04938: un clasificador lobo/husky entrenado A PROPÓSITO con fotos
    tramposas (lobos en nieve) decidía por la nieve.
"""

TITULO = "¿Cómo VE una Inteligencia Artificial? (lo que pasa dentro de su cabeza)"
ARCHIVO = "ia_como_ve"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit propio acuarela.py; docs/estilo_acuarela_pincel.md)
DURACION = None                   # natural (~10:25)
BPM = 88
GAP = 0.35
FPS = 24                          # la tinta «hierve» a 12 fps (en dos)
# Voz de Kuriox (asteroide_invisible, elegida por el usuario el 20-oct-2026). Corchetes suaves: nunca susurros ni excitado.
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-22.0, sfx=-24.0, fx=-9.0)
SUBTITULOS = False
ALIAS_QA = {"curie": "kuri", "john": "yann", "iaa": "ia", "x": "por"}
CER_MAX_POR_FRASE = {"parches_1": 0.04, "neurona_7": 0.03, "cierre_4": 0.03, "aprender_0": 0.02}   # Whisper: «16 x 16», «John», «Curie», «IAA»
TAIL_MAX_POR_FRASE = {"capas_4": 1.1}                         # termina hablando justo hasta el final de la toma (CER 0)
MUSICA = {}
TRANSICIONES = [("continua", 0.3)] * 11    # plano secuencia: los cambios los dibuja escenas.py

LYRIA = dict(
    estilo="Gentle hand-made animated documentary score: soft felt piano, warm celesta, music box, marimba, light pizzicato "
           "strings and a few soft synth pads for the 'inside the machine' parts; curious, wonder-filled, watercolour "
           "storybook feel. Sparse melody low in the mix so a narrator can speak over it. Instrumental only, no vocals.",
    escenas={
        "gancho": ("Curious and playful: a tiny music-box question motif, then a soft 'whoosh into the head' swell.", 3),
        "pixeles": ("Gridded, plucky and digital-but-warm: pizzicato and marimba in steady eighths, like counting.", 6),
        "gato": ("Old science documentary feel: warm piano, a soft crackle of discovery, then a hopeful lift.", 4),
        "neurona": ("Small and precise: celesta plinks that light up one by one, tiny clockwork.", 6),
        "capas": ("Building and climbing: an ostinato that adds an instrument on each floor, growing wonder.", 8),
        "aprender": ("Trial and error: a comic 'wrong' figure, then patient repetition that slowly resolves.", 7),
        "imagenet": ("Epic but gentle: a crowd of plucks, then a triumphant small-orchestra moment for 2012.", 6),
        "parches": ("Puzzle-like and conversational: pieces clicking together, pads that 'listen' to each other.", 6),
        "palabras": ("Dreamy and spacious: a map of stars, soft pads, words and images drifting closer.", 6),
        "trucos": ("Mischievous: sneaky pizzicato with a comic twist, a little snow-chime for the wolf.", 4),
        "cierre": ("Warm recap that climbs back up all the floors, ending on a tender, playful final chord.", 4),
    },
    tramos=[(["gancho", "pixeles", "gato"], "Begin softly from silence. Clear changes of mood at each section boundary."),
            (["neurona", "capas"], "Continue the same instrumentation. Clear changes of mood at each section boundary."),
            (["aprender", "imagenet"], "Continue the same instrumentation. Clear changes of mood at each section boundary."),
            (["parches", "palabras"], "Continue the same instrumentation. Clear changes of mood at each section boundary."),
            (["trucos", "cierre"],
             "Continue the same instrumentation. Clear changes of mood at each section boundary. End on a short playful final chord.")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Le enseñas esta foto a una inteligencia artificial... [short pause] y en menos de un segundo te contesta: «un gato naranja dormido sobre un teclado».",
        "Y si le enseñas un dibujo, una radiografía o un meme, también sabe qué es.",
        "Pero hay un detalle: la IA no tiene ojos. Nunca ha visto un gato. Ni siquiera sabe qué es ver.",
        "Entonces, ¿cómo lo sabe? [short pause] Hoy nos vamos a meter dentro de su cabeza, neurona por neurona.",
    ]},
    {"id": "pixeles", "frases": [
        "Primero, lo que de verdad le llega. Si te acercas mucho a una foto, ves que está hecha de cuadritos: píxeles.",
        "Y cada píxel son tres números: cuánto rojo, cuánto verde y cuánto azul tiene, del cero al doscientos cincuenta y cinco.",
        "Una foto normal de celular tiene doce millones de píxeles. O sea, treinta y seis millones de números.",
        "Para la IA, tu gato es eso: una tabla gigante de números. Nada más.",
        "Y ahí está el problema. Si el gato se mueve un poquito, o se apaga la luz, casi todos esos números cambian... pero sigue siendo el mismo gato.",
        "Durante décadas, los científicos intentaron escribir reglas a mano: «si tiene orejas en triángulo, es un gato».",
        "[short pause] Pero, ¿cómo le explicas a una tabla de números qué es una oreja? No funcionó.",
    ]},
    {"id": "gato", "frases": [
        "La pista salió de un cerebro de verdad. En mil novecientos cincuenta y nueve, dos científicos, Hubel y Wiesel, midieron las neuronas que ven en el cerebro de un gato.",
        "Y descubrieron algo rarísimo: cada neurona solo se encendía con una cosa muy simple. Una línea. Y no cualquier línea: una con cierta inclinación.",
        "Unas neuronas veían líneas, otras juntaban esas líneas en esquinas, y otras más arriba juntaban esquinas en formas.",
        "O sea, el cerebro no ve un gato de golpe. Lo arma por pisos, de lo más simple a lo más complejo. Por eso les dieron el Nobel.",
        "Y los ingenieros pensaron: [short pause] ¿y si construimos eso con números?",
    ]},
    {"id": "neurona", "frases": [
        "Así nació la neurona artificial, y es mucho más simple de lo que parece.",
        "Es una calculadora diminuta: recibe unos cuantos números, multiplica cada uno por una perilla que dice cuánto importa, los suma...",
        "y si el resultado pasa de cierto nivel, se enciende. Ya. Eso es todo.",
        "Ahora imagina una neurona que mira solo un cuadrito de tres por tres píxeles, con las perillas acomodadas así: claro a la izquierda, oscuro a la derecha.",
        "Esa neurona se enciende cuando, justo ahí, hay un borde vertical. Es un detector de bordes.",
        "Y si la pasas por toda la imagen, como una lupa que barre, te dibuja un mapa de dónde hay bordes verticales.",
        "A eso se le llama filtro. Con otro filtro encuentras bordes acostados, con otro diagonales, con otro cambios de color.",
        "Con esta idea, en mil novecientos ochenta y nueve, Yann LeCun hizo una red que leía números escritos a mano, y años después leía cheques en los bancos de Estados Unidos.",
    ]},
    {"id": "capas", "frases": [
        "Y ahora viene la magia: apilar.",
        "Imagina la cabeza de la IA como una torre. En el primer piso, cientos de filtros buscan bordes y manchas de color en la foto.",
        "El segundo piso no mira la foto: mira los mapas del primero. Y junta bordes en esquinas, curvas y texturas, como el rayado del pelo.",
        "El tercer piso junta curvas y texturas en partes: un ojo, una oreja puntiaguda, una nariz rosada, bigotes.",
        "Y en los pisos de hasta arriba, las partes se juntan en cosas enteras: cara de gato, rueda de bicicleta, letrero de alto.",
        "Cuando los investigadores se asomaron a cada piso de una de estas redes, vieron justo eso: bordes, luego texturas, luego partes, luego objetos.",
        "[short pause] Y lo más impresionante: nadie le programó qué es una oreja. Lo descubrió sola.",
        "Pero... ¿cómo?",
    ]},
    {"id": "aprender", "frases": [
        "Porque al principio, todas las perillas están puestas al azar. La IA recién nacida no sabe nada.",
        "Le enseñas la foto del gato y dice: [short pause] «tostadora». Mal.",
        "Entonces se mide qué tan mal estuvo, y empieza la parte clave: el error viaja hacia atrás, piso por piso, y a cada perilla se le dice un poquito hacia dónde girar para equivocarse menos.",
        "Como el juego de frío o caliente, pero con millones de jugadores al mismo tiempo.",
        "Otra foto: «perro». Mal, pero menos mal. Giran las perillas. Otra: «gato... creo». Ya casi.",
        "Repítelo millones de veces, con millones de fotos, y las perillas solitas terminan formando detectores de bordes, de bigotes, de orejas.",
        "A esto se le llama retropropagación: repartir la culpa del error entre todas las perillas. Y es como aprenden casi todas las IA que conoces.",
        "Solo había un problema: para aprender así, necesitas una cantidad absurda de fotos.",
    ]},
    {"id": "imagenet", "frases": [
        "En dos mil nueve, la científica Fei-Fei Li reunió algo que nadie había hecho: ImageNet. Más de catorce millones de imágenes, cada una etiquetada a mano.",
        "Para lograrlo, contrató por internet a unas cuarenta y nueve mil personas de ciento sesenta y siete países, que pasaron años diciendo: esto es un gato, esto es un volcán, esto es una tostadora.",
        "Y cada año organizaron un concurso: a ver qué programa reconocía mejor las fotos.",
        "En dos mil doce llegó un equipo con una red profunda, AlexNet, entrenada en dos tarjetas gráficas de videojuegos. Tenía sesenta millones de perillas.",
        "Se equivocó en el quince por ciento de las fotos. El segundo lugar, en el veintiséis. [short pause] No ganó: los aplastó.",
        "Ese día cambió todo. Tres años después, una red ya se equivocaba menos que una persona entrenada.",
    ]},
    {"id": "parches", "frases": [
        "Pero las IA con las que platicas hoy, las que te describen cualquier foto, dieron un paso más.",
        "Primero, cortan la imagen en cuadritos, como un rompecabezas. Pedazos de dieciséis por dieciséis píxeles.",
        "Cada pedazo se convierte en una lista de números que resume lo que hay en él: «pelo naranja», «tecla», «pedazo de oreja». Una especie de palabra visual.",
        "Y luego viene la atención: cada pedazo mira a todos los demás y pregunta: «¿quién de ustedes me ayuda a entender lo que soy?».",
        "El pedazo de pelo naranja se fija en el de la oreja y en el del bigote, y juntos dicen: somos un gato.",
        "Y el pedazo de tecla se fija en el gato que tiene encima, y entienden la escena completa: un gato acostado sobre un teclado.",
        "Por eso el título del artículo que lo hizo famoso es tan bonito: una imagen vale dieciséis por dieciséis palabras.",
    ]},
    {"id": "palabras", "frases": [
        "Falta lo último: ¿cómo pasa de números a palabras?",
        "En dos mil veintiuno se entrenó un modelo con cuatrocientos millones de fotos de internet junto con el texto que las acompañaba.",
        "Su trabajo era uno solo: acercar cada foto a su frase, y alejarla de las frases equivocadas.",
        "Así, poco a poco, se formó una especie de mapa de significados, donde la foto de un gato y la palabra gato quedan vecinas. Y el perro, cerca, pero no tanto. Y el volcán, lejísimos.",
        "Eso es lo que hace un modelo de lenguaje con visión: un traductor convierte los pedazos de la imagen en puntos de ese mapa...",
        "y el modelo los lee como si fueran palabras de tu mensaje. Luego contesta como contesta todo: palabra por palabra, eligiendo la más probable.",
        "Y por eso entiende un dibujo, una radiografía o un meme: entre miles de millones de imágenes con texto, ya vio muchísimos de cada uno.",
    ]},
    {"id": "trucos", "frases": [
        "Ojo: eso no significa que vea como tú. Ve patrones. Y a veces, los patrones equivocados.",
        "En un experimento, entrenaron a propósito un modelo con fotos tramposas para distinguir lobos de perros husky... y aprendió a fijarse en la nieve del fondo, no en el animal.",
        "Y en otro, a la foto de un panda le sumaron unas manchitas que tú ni notas... y la IA juró, con noventa y nueve por ciento de seguridad, que era un gibón.",
        "[short pause] Por eso los científicos siguen asomándose a sus pisos: para entender qué está mirando de verdad.",
    ]},
    {"id": "cierre", "post": 1.5, "frases": [
        "Así que, la próxima vez que una IA te describa una foto, recuerda el viaje:",
        "píxeles que se vuelven números, filtros que encuentran bordes, pisos que arman formas, partes y objetos,",
        "millones de perillas que nadie giró a mano, y un mapa donde las imágenes y las palabras viven juntas.",
        "[sighs] No vio un gato. Encontró el patrón que, en millones de ejemplos, siempre se llamó gato.",
        "Y si quieres saber qué pasa dentro de otra cabeza, suscríbete. [short pause] Kuri todavía tiene muchos pisos por enseñarte.",
    ]},
]
