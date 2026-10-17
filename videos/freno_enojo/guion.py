# -*- coding: utf-8 -*-
"""Prueba de estilo SIN CANAL (16-oct-2026): «línea blanca + neón» — fondo negro, dibujo de grabado en línea blanca fina y UN
elemento protagonista en neón amarillo que brilla (u ojos rojos). Referencias del usuario: reels de Polymaths Unite/Deepstash
(ratas en el pozo, granjero con sombrero de neón, círculo de neón con gente peleando). Doc: docs/estilo_linea_neon.md.

Tema: qué pasa DENTRO del cuerpo cuando te enojas en una discusión y te callas (y por qué a los 5 minutos llega el nudo en la
garganta), y 5 formas de drenar esa carga en esos mismos 5 minutos.
Hechos (corregidos respecto al texto que pasó el usuario, que exageraba mecanismos):
- Amígdala -> hipotálamo -> sistema simpático -> médula suprarrenal: adrenalina y noradrenalina en segundos; el hígado libera
  glucosa; corazón y presión suben; sangre a los músculos grandes; pupilas dilatadas. Cortisol (eje HPA) llega en minutos.
- La adrenalina en sangre tiene vida media de ~2-3 min; lo que sostiene la alerta es que el cerebro siga viendo amenaza.
- Arritmia sinusal respiratoria: al inhalar el corazón acelera, al exhalar el nervio vago lo frena. Suspiro fisiológico (doble
  inhalación) reabre alvéolos colapsados. Balban et al. 2023, Cell Reports Medicine (Stanford): 5 min/día de «suspiro cíclico»
  mejoró el ánimo y bajó la frecuencia respiratoria en reposo más que la meditación.
- Relajación muscular progresiva (Edmund Jacobson, 1929-1938): tensar al máximo y soltar deja el músculo más relajado que antes.
- Reflejo de inmersión: frío en la cara (nervio trigémino) -> el vago baja la frecuencia cardiaca ~10-25 %.
- Movimiento: los músculos grandes consumen la glucosa movilizada. Animales que se sacuden tras escapar = observación (no se
  narra como mecanismo probado).
- Visión panorámica vs. visión de túnel: la visión de túnel acompaña a la alerta; la relación inversa (abrir la mirada calma)
  es una propuesta con poca evidencia: se narra con prudencia.
"""

TITULO = "Lo que pasa dentro de tu cuerpo cuando te callas el coraje"
ARCHIVO = "freno_enojo"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 80
GAP = 0.30

# Voz nueva (biblioteca pública de ElevenLabs): «Alejandro Durán — Warm, Deep», latinoamericano, grave con un poco de ronquera
# Falsos positivos de Whisper: transcribe «Uno.», «Dos.»… como «1.», «2.» (las tomas dicen bien la palabra)
CER_MAX_POR_FRASE = {"suspiro_0": 0.27, "musculo_0": 0.31, "frio_0": 0.26, "sacude_0": 0.21, "mirada_0": 0.36}
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    clips_s=[10] * 7,         # 7 x 10 s = 49 puntos (saldo del 16-oct-2026: 50), ~70 s de video
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.25,
    ambiente=0.0,             # el sonido de Flow no encaja con el estilo: SFX propios
    ambiente_por={},
    carpeta_descargas="flow-freno_enojo",
)

FICHA = dict(
    estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white "
           "chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined "
           "in glowing bright yellow neon light with a soft golden glow; cinematic horizontal sixteen by nine composition, "
           "full-bleed scene that fills the entire frame edge to edge, no border, no frame",
    personajes={
        "el hombre": "a simple stick-figure-like man with a round white head, dot eyes and a small expressive mouth, thin "
                     "white line body, plain shirt and trousers drawn in white outline",
        "la mujer": "a simple stick-figure-like woman with a round white head, short hair in a bun, dot eyes, thin white "
                    "line body, plain dress drawn in white outline",
    },
    objeto="",
    epoca="present-day home: small kitchen, living room, bathroom with sink, backyard at night",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion: solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Intimate, cinematic ambient score for a calm science explainer drawn in white chalk lines on black with glowing "
           "neon: warm analog synth pads, soft felt piano, subtle pulsing bass, light heartbeat-like percussion, airy textures. "
           "Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("Tense and suspended: low drone, a muffled heartbeat pulse, a single repeated piano note, unresolved.", 4),
        "alarma": ("Rising alarm: faster pulsing synth bass, ticking percussion, building pressure like adrenaline flooding the body.", 7),
        "rebote": ("Sudden drop into melancholy: the pulse stops, a lonely felt piano melody with soft strings, a lump in the throat.", 3),
        "truco": ("Curious and hopeful: light arpeggiated synth begins, a sense of discovering a hidden switch.", 4),
        "suspiro": ("Breathing and slowing: long swelling pads that inhale and exhale, tempo gently decelerating, calm.", 3),
        "musculo": ("Controlled tension then release: tight muted pulse building for a few bars, then opening into warm pads.", 5),
        "frio": ("Cold and crystalline: glassy bell tones, icy shimmer, heartbeat slowing down, deep calm.", 3),
        "sacude": ("Kinetic and earthy: brisk rhythmic percussion, walking pulse, energy being released, then settling.", 6),
        "mirada": ("Wide and open: expansive pads, distant piano, a feeling of space opening around you.", 3),
        "combo": ("Warm resolution: piano melody returns in major key with soft strings, steady and confident.", 4),
        "cierre": ("Peaceful ending: gentle piano and pads fading, a final soft warm chord.", 2),
    },
    tramos=[(["gancho", "alarma", "rebote", "truco", "suspiro"],
             "Begin from near silence with a heartbeat pulse. End softly on a calm sustained pad."),
            (["musculo", "frio", "sacude", "mirada", "combo", "cierre"],
             "Begin softly on a calm sustained pad. End with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[serious] Estás en medio de una discusión. Algo te dolió, y decides quedarte callado.",
        "[short pause] Pasan cinco minutos. La otra persona regresa, te pide perdón con calma…",
        "[sighs] y justo ahí, sin aviso, se te cierra la garganta y te ganan las lágrimas.",
        "[curious] No es debilidad. Es química. Tu cuerpo se preparó para una pelea que nunca ocurrió.",
    ]},
    {"id": "alarma", "frases": [
        "[serious] Todo empieza en la amígdala, una almendra de neuronas escondida en lo profundo del cerebro.",
        "En menos de un segundo decide que estás en peligro, y no espera a que tú pienses.",
        "Avisa al hipotálamo, que enciende el acelerador del cuerpo: el sistema nervioso simpático.",
        "La señal llega a las glándulas suprarrenales, encima de los riñones. [short pause] Y sueltan adrenalina.",
        "El corazón se acelera. La presión sube. El hígado libera glucosa, combustible listo para quemar.",
        "La sangre corre a brazos y piernas. Los puños se cierran.",
        "Las pupilas se dilatan y la vista se cierra en un túnel.",
        "[serious] Estás listo para pelear o huir. Pero tú… no haces ninguna de las dos.",
    ]},
    {"id": "rebote", "frases": [
        "[thoughtful] Te quedas quieto, con el tanque lleno y el motor revolucionado.",
        "Y cuando la amenaza desaparece, el cerebro pisa el freno de golpe.",
        "[sighs] Ese freno es el nervio vago. Y frenar a fondo con el motor así…",
        "[short pause] el cuerpo descarga la tensión por donde puede: la garganta y los ojos.",
    ]},
    {"id": "truco", "frases": [
        "[curious] El truco es no frenar de golpe. Tienes dos caminos.",
        "Quemar el combustible para que el cuerpo crea que la pelea ya pasó, o frenar poco a poco. Aquí van cinco formas.",
    ]},
    {"id": "suspiro", "frases": [
        "[thoughtful] Uno. El suspiro fisiológico.",
        "Inhala profundo por la nariz, y con los pulmones llenos, mete un segundo jalón corto de aire.",
        "Ese jalón vuelve a inflar los alvéolos que se habían cerrado.",
        "[exhales] Luego suelta todo despacio por la boca, el doble de largo.",
        "Cada vez que exhalas, el nervio vago frena un poco el corazón. Exhalar largo es frenar largo.",
        "En 2023, un estudio de Stanford vio que este suspiro mejoraba el ánimo más que la meditación. Con dos o tres, el golpe baja.",
    ]},
    {"id": "musculo", "frases": [
        "[serious] Dos. Tensión isométrica.",
        "Tus músculos ya tienen la orden de pelear. Dales lo que piden, sin moverte.",
        "Empuja el piso con los pies, aprieta los puños o empuja una pared.",
        "Diez segundos al máximo. [short pause] Y suelta. El músculo quema parte de esa glucosa.",
        "Y tras tensarse al máximo, se relaja más que antes. Lo describió el médico Edmund Jacobson hace casi cien años.",
    ]},
    {"id": "frio", "frases": [
        "[curious] Tres. El reflejo de inmersión.",
        "Si puedes ir al baño, échate agua bien fría en la frente, los ojos y los pómulos.",
        "Tu cara está conectada al nervio trigémino. Con el frío, el cuerpo cree que te sumergiste en el agua.",
        "Y activa un reflejo antiguo de mamífero: el corazón baja entre un diez y un veinticinco por ciento.",
    ]},
    {"id": "sacude", "frases": [
        "[thoughtful] Cuatro. Sacudirte o caminar rápido.",
        "Muchos animales, al escapar de un ataque, lo primero que hacen es sacudirse.",
        "Sal un minuto, sacude las manos, haz quince sentadillas o camina rápido.",
        "Las piernas son tus músculos más grandes: gastan el combustible de la huida. Y la adrenalina, si no la alimentas, se apaga en minutos.",
    ]},
    {"id": "mirada", "frases": [
        "[curious] Cinco. Abre la mirada.",
        "La visión de túnel va de la mano con la alerta. Sin mover la cabeza, trata de ver las esquinas del cuarto con el rabillo del ojo.",
        "Es la mirada de alguien tranquilo. Es la menos estudiada, pero mucha gente nota que el pecho se afloja.",
    ]},
    {"id": "combo", "frases": [
        "[serious] El combo para la vida real.",
        "Cuando sientas el golpe de coraje, afloja la mirada y haz dos suspiros fisiológicos. Nadie lo nota.",
        "Y si puedes, agua fría en la cara o puños apretados diez segundos.",
    ]},
    {"id": "cierre", "frases": [
        "[thoughtful] Pasan cinco minutos. La otra persona regresa y te pide perdón.",
        "[short pause] Y esta vez la garganta no se cierra. Tu cuerpo ya drenó la tormenta.",
        "[sighs] Y puedes escuchar esa disculpa… desde la calma.",
    ]},
]
