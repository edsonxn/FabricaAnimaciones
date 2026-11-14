# -*- coding: utf-8 -*-
"""Guía de estudio 3 para el examen: MATEMÁTICAS (lo que viene en el cuaderno de Amaya) — video SIN canal, no se sube.
Pedido del usuario (10-nov-2026): «hagamos nuevo video para amaya y su estudio de examen… como los que hicimos ayer», con 5 fotos
del cuaderno (fuente/wa1..5.jpg; rot*.jpg = derechas). Eligió PROFE TILDE + voz ALBERTO (como amaya_estudio2, para sexto B) y
«solo estas 5 fotos»:
  wa1 decimales: 45.23 cuarenta y cinco enteros veintitrés centésimos · 3.023 tres enteros veintitrés milésimos · 0.8 ocho décimos ·
      0.08 ocho centésimos · 0.008 ocho milésimos
  wa2 lectura de números: 7,735,923 · 25,980,634 · 681,092,012
  wa3 tipos de triángulos: a) equilátero: sus tres lados iguales (trazado con compás)
  wa4 plano cartesiano: «es una hoja cuadriculada donde podemos ubicar puntos usando dos ejes (X, Y)»; eje de abscisas (X), eje de
      ordenadas (Y); el barco A(1,4) B(3,2) C(7,2) D(9,4) E(6,4) F(6,6) G(5,6) H(5,7) I(4,7) J(4,4)
  wa5 problemas con fracciones: pizza, Ana 1/4 y Luis 1/3 → 7/12, quedó 5/12 · 1/4 + 1/5 = 9/20
ERROR EN EL CUADERNO (wa2): 7,735,923 quedó «siete millones setecientos treinta dos mil…» → es «treinta y CINCO mil». Va como
pregunta trampa (preg2/resp2), con cariño, igual que «túnel» en el video de Español.
Métodos: pregunta → respuesta corta → truco; 5 «pausa y contesta» con silencio real (post 3,2 s + cuenta 3-2-1); repaso.
Trucos: contar cifras después del punto (1-2-3 = décimos-centésimos-milésimos), centavos = centésimos; grupos de 3 desde la
derecha (coma de los mil, coma de los millones); «equi» = igual como el uniforme de un equipo, escaleno = escalera chueca;
«primero caminas, luego subes» (X antes que Y, como en el abecedario); pizza en rebanadas del mismo tamaño y la mariposa.
Humor (regla: nada de memes dudosos; 3 toques cortos con lo que no caduca): la pizza que se acaban, «nivel completado».
Las cifras van ESCRITAS CON LETRA en la voz (ElevenLabs lee raro «7,735,923»); en pantalla van con número.
"""

TITULO = "Sexto B: Matemáticas para su examen (decimales, números grandes, triángulos, plano cartesiano y fracciones)"
ARCHIVO = "amaya_mate"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit acuarela.py; docs/estilo_acuarela_pincel.md)
DURACION = None
BPM = 200
GAP = 0.32
FPS = 24
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-24.0, sfx=-24.0, fx=-10.0)
SUBTITULOS = False
ALIAS_QA = {}
# Whisper escribe cifras («0.008», «25,980,634», «3, 2») y «X/Y» por «equis/ye»: el audio está bien (revisado en eval.json)
CER_MAX_POR_FRASE = {"decimales_3": 0.23, "decimales_4": 0.04, "decimales_5": 0.06, "preg1_0": 0.21, "numeros_2": 0.09,
                     "preg2_0": 0.12, "resp2_1": 0.02, "resp3_0": 0.02, "plano_0": 0.06, "plano_1": 0.08, "plano_2": 0.11,
                     "resp4_0": 0.13}
TAIL_MAX_POR_FRASE = {"repaso_1": 1.25, "resp5_0": 1.25}   # terminan con énfasis («mariposa», «¡Muy bien!»)
MUSICA = {}
LYRIA = dict(
    estilo="Warm playful storybook score for a kid's study guide: marimba, ukulele, glockenspiel, pizzicato; low in the mix.",
    escenas={
        "gancho": ("Playful hello.", 4), "decimales": ("Curious, counting.", 4), "preg1": ("Thinking.", 3), "resp1": ("Small win.", 3),
        "numeros": ("Bouncy.", 4), "preg2": ("Thinking.", 3), "resp2": ("Small win.", 3), "triangulos": ("Light, clever.", 4),
        "preg3": ("Thinking.", 3), "resp3": ("Small win.", 3), "plano": ("Playful walking.", 4), "preg4": ("Thinking.", 3),
        "resp4": ("Small win.", 3), "fracciones": ("Funny, tasty.", 4), "preg5": ("Thinking.", 3), "resp5": ("Win.", 3),
        "repaso": ("Quick recap.", 4), "cierre": ("Tender, warm.", 3),
    },
    tramos=[(["gancho", "decimales", "preg1", "resp1", "numeros"], ""), (["preg2", "resp2", "triangulos", "preg3", "resp3"], ""),
            (["plano", "preg4", "resp4", "fracciones"], ""), (["preg5", "resp5", "repaso", "cierre"], "")],
)
TRANSICIONES = [("continua", 0.3)] * 17   # plano secuencia: los cambios los dibuja escenas.py

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "¡Hola otra vez, sexto B! [short pause] Soy el profe Tilde. Ahora me llegaron las fotos de su cuaderno de Matemáticas, y con eso vamos a repasar para el examen.",
        "Hoy toca: números decimales, leer números grandes, tipos de triángulos, el plano cartesiano y problemas con fracciones. Y sí: va a haber pizza.",
        "Cuando les diga «pausa y contesta», pausen el video y contesten en voz alta. ¿Listos? Arrancamos.",
    ]},
    {"id": "decimales", "frases": [
        "Primero, los decimales. Un número decimal tiene dos partes separadas por un punto: a la izquierda, la parte entera; a la derecha, la parte decimal.",
        "Y cada lugar después del punto tiene nombre. El primero son los décimos, el segundo, los centésimos, y el tercero, los milésimos.",
        "Truco: cuenten cuántas cifras hay después del punto. Una cifra, décimos. Dos cifras, centésimos. Tres cifras, milésimos.",
        "Como en su cuaderno: cero punto ocho son ocho décimos. Cero punto cero ocho, ocho centésimos. Y cero punto cero cero ocho, ocho milésimos. Es el mismo ocho, pero cada vez más chiquito.",
        "Para leerlo completo, primero la parte entera y la palabra «enteros», y luego lo de después del punto, con el nombre del último lugar. Cuarenta y cinco punto veintitrés: cuarenta y cinco enteros, veintitrés centésimos.",
        "Dato chido: los centavos son centésimos. Un peso tiene cien centavos; por eso cincuenta centavos se escriben cero punto cincuenta.",
    ]},
    {"id": "preg1", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: tres punto cero veintitrés, ¿cómo se lee?",
    ]},
    {"id": "resp1", "pre": 0.2, "frases": [
        "Tres enteros, veintitrés milésimos. Después del punto hay tres cifras, cero, dos y tres, así que son milésimos, aunque empiece con cero. ¡Eso!",
    ]},
    {"id": "numeros", "frases": [
        "Ahora, a leer números grandes, de los que dan miedo. Truco: sepárenlos en grupitos de tres cifras, empezando por la derecha.",
        "La primera coma es la de los miles, y la segunda, la de los millones. Cada grupito se lee como si estuviera solito, y luego se dice su apellido, que puede ser millones o mil.",
        "Como en su cuaderno: veinticinco, coma, novecientos ochenta, coma, seiscientos treinta y cuatro. Se lee: veinticinco millones, novecientos ochenta mil, seiscientos treinta y cuatro.",
        "Y ojo con los ceros: seiscientos ochenta y un millones, noventa y dos mil, doce. El cero de enfrente del grupito no se dice, pero tiene que estar escrito.",
    ]},
    {"id": "preg2", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta, y ojo, que hay trampa: siete, coma, setecientos treinta y cinco, coma, novecientos veintitrés. ¿Cómo se lee completo?",
    ]},
    {"id": "resp2", "pre": 0.2, "frases": [
        "Siete millones, setecientos treinta y cinco mil, novecientos veintitrés. Tres grupitos: millones, mil y el último solito.",
        "Ojo: en el cuaderno quedó «setecientos treinta dos mil». El número dice treinta y cinco, así que corríjanlo. Truco: lean la cifra en voz alta, grupito por grupito, antes de escribirla.",
    ]},
    {"id": "triangulos", "frases": [
        "Siguiente tema: los tipos de triángulos, según sus lados. Todos tienen tres lados, pero no todos son iguales.",
        "El equilátero tiene sus tres lados iguales. Su nombre viene de «igual»: como un equipo, todos con el mismo uniforme.",
        "El isósceles tiene dos lados iguales y uno diferente, como un par de tenis iguales y una chancla.",
        "Y el escaleno tiene los tres lados diferentes, como una escalera chueca donde ningún escalón mide lo mismo.",
        "Y en su cuaderno lo trazaron con compás: se abre del tamaño del lado, se marca un arco desde cada punta, y donde se cruzan está la tercera punta. Así salen los tres lados iguales.",
    ]},
    {"id": "preg3", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: un triángulo mide cinco, cinco y tres centímetros. ¿Qué tipo es?",
    ]},
    {"id": "resp3", "pre": 0.2, "frases": [
        "¡Isósceles! Tiene dos lados iguales, los de cinco, y uno diferente, el de tres. Los tenis y la chancla.",
    ]},
    {"id": "plano", "frases": [
        "Ahora, el plano cartesiano. Como dice su cuaderno: es una hoja cuadriculada donde podemos ubicar puntos usando dos ejes, el eje equis y el eje ye.",
        "El eje equis es el acostado, y se llama eje de las abscisas. El eje ye es el parado, y se llama eje de las ordenadas.",
        "Cada punto tiene dos números entre paréntesis, y siempre van en orden: primero equis, luego ye. Como en el abecedario, la equis va antes que la ye.",
        "Truco: primero caminas, luego subes. Como en el barco de su cuaderno: el punto A es uno, cuatro. Caminas uno, y subes cuatro. Ahí está la punta del barco.",
        "Y el punto D es nueve, cuatro: caminas nueve, subes cuatro, y llegas a la otra punta. Si los volteas, cuatro, nueve, caes muy arriba, fuera del barco. El orden sí importa.",
    ]},
    {"id": "preg4", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: en el barco, ¿cuáles son las coordenadas del punto B?",
    ]},
    {"id": "resp4", "pre": 0.2, "frases": [
        "Tres, dos. Caminas tres, y subes dos. Primero equis, luego ye. ¡Bien!",
    ]},
    {"id": "fracciones", "frases": [
        "Y el último tema, el más rico: problemas con fracciones. Como en su cuaderno: una pizza completa es un entero. Ana se comió un cuarto, y Luis se comió un tercio.",
        "¿Qué parte quedó para los demás? El problema es que cuartos y tercios son rebanadas de distinto tamaño, y así no se pueden sumar.",
        "Entonces partimos la pizza en rebanadas del mismo tamaño. Multiplicamos los de abajo: cuatro por tres, doce. Ahora la pizza tiene doce rebanadas.",
        "Un cuarto son tres rebanadas de doce, y un tercio son cuatro de doce. Entre los dos se comieron siete doceavos.",
        "La pizza entera son doce doceavos. Doce menos siete: quedaron cinco doceavos para los demás. Los demás, por cierto, llegaron tarde.",
        "Y para sumar más rápido, la mariposa: un cuarto más un quinto. Uno por cinco, cinco; uno por cuatro, cuatro; cinco más cuatro, nueve. Abajo, cuatro por cinco, veinte, y el resultado es nueve veinteavos.",
    ]},
    {"id": "preg5", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: si sumamos un medio más un tercio, ¿cuánto nos da?",
    ]},
    {"id": "resp5", "pre": 0.2, "frases": [
        "Cinco sextos. Con la mariposa: uno por tres da tres, uno por dos da dos, y tres más dos son cinco. Y abajo, dos por tres, seis. ¡Muy bien!",
    ]},
    {"id": "repaso", "frases": [
        "Repaso exprés. Decimales: cuenten las cifras después del punto, décimos, centésimos, milésimos. Números grandes: grupitos de tres desde la derecha, millones y mil.",
        "Triángulos: equilátero, tres iguales; isósceles, dos; escaleno, ninguno. Plano cartesiano: primero caminas, luego subes. Y fracciones: rebanadas del mismo tamaño, o la mariposa.",
    ]},
    {"id": "cierre", "post": 2.0, "frases": [
        "Sexto B: nivel completado, ya tienen todo lo de su cuaderno de Mate. Repásenlo una vez más antes de dormir.",
        "Échenle ganas. Yo sé que pueden. [short pause] ¡Mucho éxito en su examen, sexto B!",
    ]},
]
