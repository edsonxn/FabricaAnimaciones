# -*- coding: utf-8 -*-
"""Anuncio de «Dúo · Misiones en pareja» (app web de E:/CalendarioPareja), vertical, ~45 s, sin canal.

Estilo: el de la propia app (modo oscuro): fondo #17121C con manchas difusas coral/violeta a la deriva, tarjetas #221B29
con borde #32283B y esquinas de 22 px, degradado #FF8A5B -> #FF5E7E -> #8B5CF6, fuente Plus Jakarta Sans (fuentes/),
emojis de color, barra de XP con brillo que corre, misiones con palomita, calendario del ciclo, logo de dos círculos.
Todo dibujado por código (kit propio `duo.py`); escenas en `escenas.py` (plano secuencia).
Voz ElevenLabs eleven_v4 con corchetes: una PAREJA que se responde -> Lina (ella, narradora base) y Eric (él, VOZ_POR_FRASE).
SFX de ElevenLabs anclados a las palabras (`fx_audio.py` -> audio/fx.wav). Música Lyria. Sin subtítulos quemados.

Datos de la app (index.html, versión 5): misiones en pareja 25 XP, para el otro 15 XP, «me encantó» +5 XP, check-in +20 XP,
meta semanal 450 XP entre los dos (al llenarla suben de nivel), 6 áreas (Comunicación 💬, Tiempo de calidad ⏳,
Afecto y detalles 💝, Intimidad 🔥, Diversión 🎲, Equipo 🤝), cuestionario inicial, calendario del ciclo con misiones de
cuidado cuando ella está en su periodo. Cierre: descarga en App Store y Google Play (el usuario, 13-oct: NO mostrar el URL
provisional de clicknbusiness; la app saldrá en las tiendas).
"""

TITULO = "Dúo · Misiones en pareja"
ARCHIVO = "duo_promo"
ESTILO_VISUAL = "documental"     # motion graphics propios dibujados por código (kit duo.py), estética de la app Dúo
FORMATO = "vertical"
DURACION = None
BPM = 480                        # NO es el tempo real: cuantiza los cambios de escena a 0,5 s (Lyria no usa el BPM)
GAP = 0.14                       # anuncio: diálogo ágil, pausas cortas
SUBTITULOS = False
TRANSICIONES = [("continua", 0.5)] * 5     # plano secuencia: los cambios los dibuja escenas.py
MEZCLA = dict(musica=-22.0, sfx=-24.0, fx=-17.0)

LINA = "VmejBeYhbrcTPwDniox7"    # Lina - Sunny, Kind and Friendly (es)
ERIC = "tGjegxe7yxhGMzd3SOmH"    # Eric - Vivid & Natural (es)
VOZ = dict(motor="elevenlabs", voice_id=LINA, modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/duo_promo/ref_lina.mp3", tomas=1, stability=0.5)
VOZ_POR_FRASE = {"gancho_0": ERIC, "app_1": ERIC, "barra_0": ERIC, "detalle_0": ERIC, "ajusta_0": ERIC, "cierre_1": ERIC}
CER_MAX_POR_FRASE = {"app_0": 0.25, "cierre_0": 0.2}       # «Dúo»: Whisper puede escribirlo «Duo» o «dúo»

LYRIA = dict(
    estilo="Warm modern feel-good pop for a couples app commercial: bright plucked guitar and ukulele, soft hand claps and "
           "finger snaps, warm synth pads, playful marimba and glockenspiel accents, romantic and cheerful, 105 BPM, "
           "instrumental only, no vocals.",
    escenas={
        "gancho": ("sparse and a little wistful, a lonely plucked guitar and a soft clock-like tick, waiting", 3),
        "app": ("the beat kicks in with claps and a bright catchy hook, happy discovery", 6),
        "barra": ("building energy with a rising arpeggio, ends on a celebratory hit", 8),
        "detalle": ("tender and sweet, softer drums, warm pad and glockenspiel", 5),
        "ajusta": ("light playful groove, curious and bouncy", 6),
        "cierre": ("full joyful chorus, big warm ending and a clean final note", 8),
    })

ESCENAS = [
    {
        "id": "gancho", "pre": 0.3, "post": 0.15,
        "frases": [
            "[sighs] Siempre decimos: «a ver cuándo salimos».",
            "[laughs] Y nunca salimos.",
        ],
    },
    {
        "id": "app", "pre": 0.1, "post": 0.15,
        "frases": [
            "Hasta que llegó Dúo.",
            "[excited] Cada día nos da misiones para hacer juntos.",
            "Cenar sin celulares. Un abrazo de 20 segundos. Bailar en la sala.",
        ],
    },
    {
        "id": "barra", "pre": 0.1, "post": 0.15,
        "frases": [
            "Cada misión suma experiencia a una barra que llenamos entre los dos.",
            "[excited] ¡Y si se llena, subimos de nivel!",
        ],
    },
    {
        "id": "detalle", "pre": 0.1, "post": 0.15,
        "frases": [
            "Hay misiones para consentir al otro. Y con el calendario del ciclo, sé cuándo llevarle algo calientito.",
            "[chuckles] Y ahora sí se acuerda.",
        ],
    },
    {
        "id": "ajusta", "pre": 0.1, "post": 0.15,
        "frases": [
            "Contestan unas preguntas, y las misiones se ajustan a ustedes.",
        ],
    },
    {
        "id": "cierre", "pre": 0.15, "post": 1.3,
        "frases": [
            "Dúo. Misiones diarias para crecer en pareja.",
            "Descárguenla y empiecen hoy.",
        ],
    },
]
