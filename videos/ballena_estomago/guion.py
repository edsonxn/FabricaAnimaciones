# -*- coding: utf-8 -*-
"""¿Qué pasaría si una ballena te tragara? — Short vertical de Kuriox (~60 s), ACUARELA PINTADA A MANO POR CÓDIGO.

Pedido del usuario (4-nov-2026): Short con animación procedural, cada cuadro dibujado por código, SFX hechos por Claude (síntesis
propia, sin ElevenLabs SFX), con el estilo y la forma de animar de un corto de referencia en X (@mablesjoseph, 25-sep-2026):
acuarela con grano de papel, manchas húmedas con borde oscuro, contorno de tinta a pincel que «hierve», personajes chibi,
iconos de emoción (!, ?, nubecita, destellos), brillo cálido. Supuesto: llevas tanque porque estabas buceando.
Decisiones: canal Kuriox · voz ElevenLabs (voz de Kuriox) · vertical 9:16 · vista previa de ~10 s con audio completo antes del resto.
Kuri (mascota de Kuriox) hace de compañero flotante, como la linterna de la referencia.

Datos (verificar 2.ª fuente en el cierre):
  - Michael Packard, buzo de langostas, Provincetown (Massachusetts), 11-jun-2021: una ballena jorobada lo atrapó en la boca
    ~30-40 s y lo escupió (Cape Cod Times; BBC). Las ballenas barbadas (jorobada, azul) tienen el esófago estrecho: no tragan a una persona.
  - El cachalote (odontoceto) traga presas grandes enteras, calamares gigantes incluidos; su esófago podría con una persona.
  - Estómago de cetáceo en cámaras: la 1.ª (preestómago) es muscular y sin glándulas: tritura; la 2.ª (principal) segrega ácido y enzimas.
  - Temperatura corporal de un cachalote ≈ 36-37 °C.
  - Inmersiones del cachalote: típicamente 400-1 200 m, hasta ~2 000 m, 45-60 min.
  - Tanque de 12 L a 200 bar ≈ 2 400 L de aire; ~20 L/min en superficie. A 1 000 m (≈ 101 bar) cada respiración gasta ~100 veces
    más y solo queda gas útil mientras el tanque supere la presión del agua → menos de un minuto. pO2 del aire a 1 000 m ≈ 21 bar
    (tóxico por encima de ~1,6 bar: convulsiones).
  - Los cachalotes regurgitan lo indigerible (picos de calamar); de ahí, en parte, el ámbar gris.
"""

TITULO = "¿Qué pasaría si una ballena te tragara?"
ARCHIVO = "ballena_estomago_short"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit propio acuarela.py; docs/estilo_acuarela_pincel.md)
FORMATO = "vertical"
DURACION = 75.0
BPM = 92
GAP = 0.16
FPS = 24                          # como la referencia: la tinta «hierve» a 12 fps (en dos)
# Voz de Kuriox (asteroide_invisible, elegida por el usuario el 20-oct-2026). Corchetes suaves: nunca susurros ni excitado.
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-22.0, sfx=-24.0, fx=-9.0)
SUBTITULOS = False
ALIAS_QA = {}
MUSICA = {}
TRANSICIONES = [("continua", 0.3)] * 5     # plano secuencia: los cambios los dibuja escenas.py

LYRIA = dict(
    estilo="Gentle hand-made animated short score: soft felt piano, warm celesta, music box, airy pads, a little ukulele or "
           "pizzicato, tender and curious with a touch of comic suspense, watercolour storybook feel. Sparse melody low in the mix "
           "so a narrator can speak over it. Instrumental only, no vocals.",
    escenas={
        "gancho": ("Calm underwater wonder (soft pads, bubbly celesta), then a sudden dark low swell and silence as everything goes black.", 7),
        "garganta": ("Light comic relief: plucky pizzicato and a cheeky music box, relieved.", 10),
        "estomago": ("Murky, tense and squishy: low muffled heartbeat-like bass, slow dissonant celesta, dark and claustrophobic but cartoonish.", 14),
        "inmersion": ("Descending, deep and ominous: slow low piano notes falling, pressure building, a creeping drone.", 11),
        "cierre": ("Release and comic relief: bright playful resolution with a little wink at the end.", 9),
    },
    tramos=[(["gancho", "garganta", "estomago", "inmersion", "cierre"],
             "Begin softly from silence. Clear changes of mood at each section boundary. End on a short playful final chord.")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Estás buceando, con tu tanque lleno de aire...",
        "[short pause] y de pronto, todo se vuelve negro.",
        "Una ballena te acaba de tragar.",
    ]},
    {"id": "garganta", "frases": [
        "La buena noticia: casi ninguna ballena puede tragarte. Su garganta es demasiado estrecha.",
        "En 2021, una jorobada atrapó a un buzo en su boca... y lo escupió.",
        "Pero hay una que sí puede: el cachalote. Traga calamares gigantes enteros.",
    ]},
    {"id": "estomago", "frases": [
        "Caes en su estómago: oscuridad total, 37 grados, y paredes de músculo que te aprietan.",
        "Más adentro te espera el ácido. Tu traje aguanta un rato. [short pause] Tu piel, no tanto.",
    ]},
    {"id": "inmersion", "frases": [
        "Pero lo peor no está dentro. [short pause] El cachalote baja a mil metros.",
        "Ahí la presión es cien veces mayor: tu tanque se vacía en menos de un minuto, y el oxígeno se vuelve veneno.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Tu única salida: que te vomite, como vomita los picos de calamar que no puede digerir.",
        "[sighs] Y tú, buzo, eres muy difícil de digerir.",
    ]},
]
