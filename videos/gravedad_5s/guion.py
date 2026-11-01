# -*- coding: utf-8 -*-
"""¿Qué pasaría si la GRAVEDAD desapareciera 5 segundos? — Kuriox, ~2 min, Kurzgesagt PLANO SECUENCIA (una clase Mundo, sin cortes).
Voz Dan (Chatterbox, números en palabras), ritmo Kuriox: pausas cortas (GAP 0,35), frases cortas, mucho movimiento. Mascota Kuri.

Fórmula: la del Sol (×9,8) y Oxígeno 5 s cambiando UNA variable (el tema: gravedad 5 s).
RIGOR: separamos dos versiones del experimento mental:
  A) Versión suave (solo desaparece el peso en la superficie de la Tierra): flotar a ras de piso o subir a ~1 m/s por el último paso
     (~5 m en 5 s), expansión brusca de la atmósfera hacia arriba (caída de presión, golpe en los oídos, viento y burbujas de agua),
     deriva tangencial por la rotación terrestre, y caída simultánea al segundo 5.
  B) Versión total (desaparece toda la gravedad del universo): el interior terrestre comprimido rebota hacia afuera rompiendo la
     corteza con lava; la Tierra y la Luna salen en línea recta tangente a su órbita; el Sol pierde el equilibrio hidrostático, se
     expande y apaga su fusión nuclear; al volver la gravedad en el segundo 5, el colapso funde la corteza.
"""

TITULO = "¿Qué pasaría si la GRAVEDAD desapareciera 5 segundos?"
ARCHIVO = "gravedad_5_segundos"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 110
GAP = 0.35
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 5       # plano secuencia: 6 escenas = 5 cambios continuos, sin cortes
MUSICA = {}                                  # la música es Lyria (LYRIA), nunca la procedural

LYRIA = dict(
    estilo=("Curious, playful yet suspenseful science-documentary score for a fast-paced animated video about gravity and "
            "floating: airy weightless synth pads, soft celesta and glockenspiel, light pizzicato strings, a gentle pulsing bass, "
            "a subtle ticking clock motif for a five-second countdown; modern and cinematic. Melodies low and sparse so a "
            "narrator can speak over it. Instrumental only."),
    escenas={
        "intro": ("Hook: a playful light bounce, a sudden weightless hush, then a curious stinger and a ticking pulse.", 4),
        "version_a": ("Weightless floating mood: airy celesta, light pizzicato drifting upward, gentle curiosity.", 5),
        "viento_mar": ("Rising urgency: rushing wind-like synth swells, tense pulsing bass, swirling arpeggios.", 7),
        "caida_a": ("Sudden drop and heavy impact thud at the five-second mark, then a warm relieved chord.", 7),
        "version_b": ("Ominous cosmic scale: deep low strings, rumbling bass, expanding brass-like synth swell, dramatic tension.", 9),
        "cierre": ("Warm and peaceful resolution of the main theme, gentle celesta and soft pads, natural fade-out.", 3),
    },
    tramos=[
        (["intro", "version_a", "viento_mar", "caida_a", "version_b", "cierre"],
         "Begin with a light playful bounce, float into weightless curiosity, build through rushing tension and a cosmic swell, "
         "then resolve into a warm, peaceful fade-out. Keep one consistent melodic theme throughout."),
    ],
)

ESCENAS = [
    {
        "id": "intro",
        "pre": 0.3,
        "frases": [
            "Da un salto pequeño.",
            "Siempre vuelves al suelo.",
            "Pero imagina que, justo ahora, la gravedad desaparece durante cinco segundos.",
            "Muchos creen que saldríamos volando al espacio como cohetes.",
            "La realidad es mucho más rara, y depende de qué gravedad apagues.",
        ],
    },
    {
        "id": "version_a",
        "frases": [
            "Primero, la versión suave: solo desaparece tu peso aquí en la superficie.",
            "Segundo cero. Si estás quieto dentro de tu casa, no sales disparado: solo flotas a ras del piso.",
            "Pero si ibas caminando, el último impulso de tu pie te empuja hacia arriba.",
            "A un metro por segundo, en cinco segundos subes hasta el techo, o a la altura de un árbol en el parque.",
            "Los perros, las bicicletas y las tazas de café suben contigo en cámara lenta.",
            "Parece divertido, hasta que miras el aire.",
        ],
    },
    {
        "id": "viento_mar",
        "frases": [
            "Segundo dos. La atmósfera solo se queda pegada a la Tierra porque su propio peso la aplasta.",
            "Sin gravedad, todo el aire rebota hacia arriba como un resorte suelto y la presión cae de golpe.",
            "Tus oídos sienten un golpe seco y el viento levanta coches, charcos y olas enteras en grandes burbujas flotantes.",
            "Además, la Tierra gira rapidísimo, y sin gravedad todo empieza a moverse de lado en línea recta.",
        ],
    },
    {
        "id": "caida_a",
        "frases": [
            "Segundo cinco. La gravedad regresa de golpe.",
            "Todo lo que flotaba a cinco o diez metros cae de lleno al mismo tiempo.",
            "Coches, agua y personas golpean el suelo a la vez.",
            "Sería un golpe durísimo, pero en la versión suave, la humanidad sobreviviría.",
        ],
    },
    {
        "id": "version_b",
        "frases": [
            "Ahora la versión total: se apaga toda la gravedad del universo.",
            "Segundo cero. El interior de la Tierra está aplastado a una presión brutal por el peso de la roca.",
            "Al soltar esa fuerza, el planeta entero rebota hacia afuera, la corteza se rompe y brota lava por todas partes.",
            "Segundo tres. La Tierra y la Luna dejan su órbita y salen en línea recta por el espacio.",
            "Y el Sol, que solo brilla porque su gravedad aprieta el núcleo, se hincha de golpe y apaga su fusión nuclear.",
            "Segundo cinco. Al volver la gravedad, la Tierra hinchada se desploma sobre sí misma y funde toda la superficie.",
        ],
    },
    {
        "id": "cierre",
        "frases": [
            "Por suerte, la gravedad no tiene interruptor.",
            "No es un cable que se pueda apagar: es la forma del espacio doblada por cada átomo de materia.",
            "Así que la próxima vez que se te caiga algo al piso, no te enojes.",
            "Ese tirón invisible es lo único que mantiene unidos el mar, el aire y las estrellas.",
        ],
    },
]
