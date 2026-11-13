# -*- coding: utf-8 -*-
"""Cómo vuela un Falcon 9: la misión CRS-30, etapa por etapa (~1 min, horizontal, SIN CANAL: prueba para un canal nuevo de
cohetería y exploración espacial). Kit NUEVO `nucleo/linea3d.py`: 3D de líneas blancas sobre negro (estética de transmisión de
lanzamiento): globo de alambre con costas reales, cohete por silueta de revolución, trayectorias, mapa de Cabo Cañaveral en
perspectiva y reloj de misión con arco de eventos. Voz ElevenLabs «Alberto Rodríguez» (prueba). Sin subtítulos quemados.

Datos comprobados el 13-nov-2026:
  - Cronología oficial NASA «NASA's SpaceX CRS-30: Launch Coverage Underway» (P. Bielling, 21-mar-2024):
    https://www.nasa.gov/blogs/commercialresupply/2024/03/21/nasas-spacex-crs-30-launch-coverage-underway/
    Max Q 00:00:58 · MECO 00:02:19 · separación 00:02:22 · 2.ª etapa enciende 00:02:29 · boostback 00:02:32-00:03:24 ·
    entry burn 00:06:20-00:06:40 · landing burn 00:07:26 · aterrizaje 00:07:50 · SECO-1 00:08:35 · Dragon se separa 00:11:48 ·
    apertura del morro 00:12:40. Despegue 21-mar-2024 16:55 EDT, SLC-40 (Cabo Cañaveral).
  - Everyday Astronaut «Dragon CRS-2 SpX-30» (F. Kordina, 19-mar-2024): propulsor B1080-6 (5 vuelos previos: Axiom-2, Euclid,
    Starlink 6-11, Starlink 6-24, Axiom-3), aterriza en Landing Zone 1; Dragon C209.
  - LZ-1 está a ~9 km de SLC-40 (collectSPACE, 21-dic-2015: «5.6 miles (9 km)»; comprobado con coordenadas SLC-40 28.5620 N
    80.5772 W y LZ-1 28.4858 N 80.5444 W = 9,06 km).
"""

TITULO = "Cómo vuela un Falcon 9: la misión CRS-30 etapa por etapa"
ARCHIVO = "cohete_crs30"
ESTILO_VISUAL = "documental"     # kit linea3d (3D de líneas blancas sobre negro), dibujado por código
DURACION = None
BPM = 240                        # compás de 1 s: escenas pegadas a la voz (video de ~1 min)
GAP = 0.22
SUBTITULOS = False
TRANSICIONES = [("continua", 0.5)] * 8     # plano secuencia: los cambios de plano los dibuja escenas.py
MEZCLA = dict(musica=-23.0, sfx=-22.0, fx=-17.0)
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1,
           stability=0.5)
LYRIA = dict(
    estilo="Cinematic space-launch underscore: deep pulsing analog synth bass, ticking countdown clock percussion, wide airy pads, "
           "minimal and precise like a rocket launch webcast, 100 BPM, instrumental only, no vocals.",
    escenas={
        "gancho": ("quiet ticking pulse and a low drone, anticipation", 6),
        "despegue": ("massive low swell and sub-bass rumble, drums enter", 4),
        "maxq": ("driving pulse, tension rising", 3),
        "meco": ("sudden drop to silence then a single bright synth hit", 4),
        "divide": ("two arpeggios split apart, curious and technical", 4),
        "regreso": ("tense descending figure, heavy and determined", 8),
        "aterrizaje": ("build to a triumphant resolving chord", 5),
        "orbita": ("calm floating pads, weightless and vast", 7),
        "cierre": ("warm confident outro with a clean ending", 7),
    },
    tramos=[(["gancho", "despegue", "maxq", "meco", "divide", "regreso", "aterrizaje", "orbita", "cierre"],
             "biblioteca: mods_ia_fusion__lyria_1 (otro público)")])
CER_MAX_POR_FRASE = {"despegue_0": 0.3, "maxq_0": 0.3}     # «CRS-30» y «Max Q»: Whisper los escribe a su manera

SFX_ELEVEN = {
    "hud": dict(prompt="Short soft digital interface beep, mission control telemetry readout, clean and quiet", seg=0.5, variantes=3),
    "tic": dict(prompt="Very short soft digital tick, a data row appearing on a screen", seg=0.3, variantes=2),
    "ignicion": dict(prompt="Rocket engines igniting on the launch pad: sharp crackle then a deep roar building up", seg=4.0),
    "despegue": dict(prompt="Huge rocket liftoff roar with low crackling rumble, heard from a distance, sustained", seg=5.0),
    "viento": dict(prompt="Heavy aerodynamic buffeting and low rumbling wind on a rocket going supersonic", seg=3.0),
    "corte": dict(prompt="Rocket engines shutting down abruptly: roar cuts to silence with a low thump", seg=1.5),
    "separacion": dict(prompt="Rocket stage separation in space: heavy metallic pneumatic clunk and release", seg=1.5),
    "encendido": dict(prompt="Rocket engine relight in flight: short ignition pop then a steady powerful roar", seg=2.5, variantes=2),
    "rcs": dict(prompt="Cold gas thruster puffs, short pneumatic bursts of a spacecraft turning", seg=1.2),
    "whoosh": dict(prompt="Deep smooth cinematic whoosh, camera pulling far away", seg=1.3, variantes=2),
    "caida": dict(prompt="High-speed descent wind roar, a large object falling through the atmosphere", seg=2.5),
    "estampido": dict(prompt="Double sonic boom heard from a distance, two sharp thunderous cracks", seg=1.5),
    "toque": dict(prompt="Heavy rocket booster landing on a concrete pad: deep thud, metal legs creak, engine hiss fading", seg=2.0),
    "apagado": dict(prompt="Soft engine cutoff in the vacuum of space, muffled rumble fading out", seg=1.2),
    "suelta": dict(prompt="Spacecraft separating from a rocket in orbit: soft spring release clunk", seg=1.0),
    "campana": dict(prompt="Bright clean notification chime, two rising bell notes", seg=1.0),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Unos doce minutos. Es lo que tarda un Falcon 9 en soltar una nave rumbo a la Estación Espacial.",
        "Y mientras tanto, su primera etapa vuelve a casa.",
    ]},
    {"id": "despegue", "frases": [
        "Cabo Cañaveral, misión CRS-30. Nueve motores encienden a la vez.",
    ]},
    {"id": "maxq", "frases": [
        "Casi al minuto, Max Q: la máxima presión del aire sobre el cohete.",
    ]},
    {"id": "meco", "frases": [
        "Dos minutos y diecinueve segundos: se apagan los motores, y las etapas se separan.",
    ]},
    {"id": "divide", "frases": [
        "Aquí el vuelo se parte en dos. La segunda etapa sigue hacia la órbita.",
    ]},
    {"id": "regreso", "frases": [
        "La primera da media vuelta, y quema sus motores para regresar a la costa.",
        "Cae de cola, y otra quema la frena antes del aire denso.",
    ]},
    {"id": "aterrizaje", "frases": [
        "Siete minutos y cincuenta segundos: aterriza de pie, a nueve kilómetros de donde despegó.",
    ]},
    {"id": "orbita", "frases": [
        "Arriba, la segunda etapa apaga su motor.",
        "Y casi a los doce minutos, la Dragon se suelta, rumbo a la Estación.",
    ]},
    {"id": "cierre", "post": 1.1, "frases": [
        "Ese propulsor ya había volado cinco veces. Los cohetes ya no se tiran: se reutilizan.",
        "Suscríbete, y te explico el próximo lanzamiento.",
    ]},
]

for _e in ESCENAS[1:-1]:                     # márgenes cortos: el plano secuencia no necesita aire entre escenas
    _e.setdefault("pre", 0.12)
    _e.setdefault("post", 0.12)
ESCENAS[0]["post"] = 0.15
ESCENAS[-1]["pre"] = 0.15
