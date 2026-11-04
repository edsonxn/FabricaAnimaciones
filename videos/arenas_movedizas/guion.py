# -*- coding: utf-8 -*-
"""¿Qué pasaría si cayeras en arenas movedizas? — Short vertical de Kuriox (~73 s), ACUARELA PINTADA A MANO POR CÓDIGO.

Pedido del usuario (4-nov-2026): «otro video como el de la ballena», situación de terror; eligió la opción 2 (arenas movedizas).
Fórmula: la de la ballena (situación en primera persona + ciencia paso a paso + Kuri + final aliviado) con el giro «te han
mentido» de la goma azul (×73). Kit copiado de videos/ballena_estomago/ (docs/estilo_acuarela_pincel.md).
Decisiones: 1 sesión · SIN vista previa parcial (directo al MASTER) · voz de Kuriox · SFX sintetizados por código · Lyria.
Protagonista: explorador chibi (sombrero, mochila) + Kuri flotando a su lado.

Datos (verificados el 4-nov-2026):
  - Khaldoun, Eiser, Wegdam y Bonn, «Liquefaction of quicksand under stress», Nature 437, 635 (2005), doi:10.1038/437635a:
    la arena movediza tiene ~2 g/ml, el cuerpo humano ~1 g/ml → te hundes hasta la mitad (la cintura) y flotas.
    Al moverte se licúa y luego se compacta (la viscosidad SUBE): cuanto más pataleas, más te atrapa.
    Sacar un pie a 1 cm/s exige ~10⁴ N, «lo que cuesta levantar un coche mediano» (los autores; Nature News 28-sep-2005,
    National Geographic sep-2005). Salida: movimientos lentos de las piernas para que entre agua, echarse atrás y flotar.
  - El peligro real: quedarse atrapado mucho tiempo (marea que sube en bahías, sol, frío), no ahogarse en la arena.
  - Daniel Engber (Slate, 2010, «Terra Infirma»): en los años sesenta ~3 % de las películas tenían arenas movedizas
    (≈ una de cada treinta y cinco).
"""

TITULO = "¿Qué pasaría si cayeras en arenas movedizas?"
ARCHIVO = "arenas_movedizas_short"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit propio acuarela.py; docs/estilo_acuarela_pincel.md)
FORMATO = "vertical"
DURACION = 73.0
BPM = 92
GAP = 0.16
FPS = 24                          # la tinta «hierve» a 12 fps (en dos)
# Voz de Kuriox (asteroide_invisible, elegida por el usuario el 20-oct-2026). Corchetes suaves: nunca susurros ni excitado.
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-22.0, sfx=-24.0, fx=-9.0)
SUBTITULOS = False
ALIAS_QA = {}
MUSICA = {}
TRANSICIONES = [("continua", 0.3)] * 5     # plano secuencia: los cambios los dibuja escenas.py

LYRIA = dict(
    estilo="Gentle hand-made animated short score: soft felt piano, warm celesta, music box, marimba, a little ukulele or "
           "pizzicato, curious with a touch of comic suspense, watercolour storybook feel. Sparse melody low in the mix "
           "so a narrator can speak over it. Instrumental only, no vocals.",
    escenas={
        "gancho": ("Sunny carefree beach walk (light ukulele, marimba), then a sudden comic-dread low note and a sinking glissando.", 7),
        "mito": ("Playful old-movie parody: a short melodramatic tremolo that collapses into a cheeky pizzicato 'nope'.", 13),
        "trampa": ("Sticky, tense and cartoonish: slow low bassoon-like piano, ticking, effort and strain.", 14),
        "marea": ("Ominous and slow: rising soft drone with distant wave swells, the clock is ticking.", 8),
        "cierre": ("Calm relief: gentle floating music box, warm and tender, ending on a short playful final chord.", 18),
    },
    tramos=[(["gancho", "mito", "trampa", "marea", "cierre"],
             "Begin softly from silence. Clear changes of mood at each section boundary. End on a short playful final chord.")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Vas caminando por la orilla... [short pause] y de pronto, el suelo se traga tus piernas.",
        "Caíste en arenas movedizas.",
    ]},
    {"id": "mito", "frases": [
        "En los años sesenta, una de cada treinta y cinco películas tenía arenas movedizas, y siempre hundían al héroe hasta la cabeza.",
        "[short pause] Pero te mintieron.",
        "La arena movediza pesa el doble que tú: te hundes hasta la cintura... y ahí flotas.",
    ]},
    {"id": "trampa", "frases": [
        "El problema es que no te suelta. Cuanto más pataleas, más se aprieta, como si fuera cemento.",
        "Y sacar un pie de un tirón cuesta lo mismo que levantar un coche.",
    ]},
    {"id": "marea", "frases": [
        "Lo peligroso no es la arena. [short pause] Es quedarte atrapado horas... mientras sube la marea.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Para salir, no tires. Échate hacia atrás, como si flotaras en una alberca,",
        "y mueve las piernas despacio, en círculos, para que entre el agua.",
        "Poco a poco, la arena te suelta.",
        "[sighs] Las películas mintieron en casi todo... menos en una cosa: no entres en pánico.",
    ]},
]
