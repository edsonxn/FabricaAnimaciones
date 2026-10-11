# -*- coding: utf-8 -*-
"""Dos formas de fusionar videojuegos con IA (vertical, ~2 min, sin canal: prueba). Motion graphics dibujados por código
(kit propio `pix.py`, estética «tecno»: fondo oscuro, neón, circuitos, datos que fluyen) + extractos cortos de gameplay real.
Voz ElevenLabs «Ginyin» (enérgica), SFX de ElevenLabs anclados a las palabras (`fx_audio.py` -> audio/fx.wav). Sin subtítulos quemados.

Origen: el video «Los MODS de la IA se SALIERON de CONTROL» (lucasmelor, 5-oct-2026). Hechos verificados el 7-oct-2026:
  - SkyCraft (github.com/chasmlol/SkyCraft, repo del 30-sep-2026): Skyrim y Minecraft corren A LA VEZ como dos procesos separados.
    Un plugin SKSE (C++) y un mod Fabric (Java) se hablan por MEMORIA COMPARTIDA con nombre (`Local\\SkyCraft_v1`): cabecera
    (número mágico, versión, ids de proceso, latidos), casillas de «último valor» por cuadro (posición, cámara, sincronía) y dos
    colas circulares para sucesos (bloque puesto, golpe dado). Minecraft corre oculto (sin ventana ni sonido) y manda en el jugador,
    el inventario y el combate; Skyrim pone el mundo, los NPC y las colisiones y DIBUJA los bloques con su propio renderizador.
    Fuentes: heldgames.com/guides/skycraft-minecraft-inside-skyrim; guía «passthrough mods» de ai-game-modding-guides (GitHub).
  - Recompilación estática (N64Recomp, XenonRecomp): traduce el binario a C/C++ nativo SIN reconstruir el código fuente.
    Decompilación: reconstruye código legible, función por función. (readonlymemo.com, README de XenonRecomp.)
  - Skate 3 en Rust/Bevy (github.com/SK8-ENGINE/skate-3-rust-engine): reescritura; NO incluye assets (pones tu propia copia).
    Su README: «dumbad» pasó MÁS DE DOS AÑOS de ingeniería inversa; luego una recompilación y un renderizador; la IA convirtió
    ese conocimiento en una implementación nueva, no lo descubrió. «En una semana» es lo que se repite en redes.
"""

TITULO = "Dos formas de fusionar videojuegos con IA"
ARCHIVO = "mods_ia_fusion"
ESTILO_VISUAL = "documental"     # motion graphics dibujados propios (docs/estilo_documental.md), variante «tecno» vertical
FORMATO = "vertical"
DURACION = None
BPM = 120
GAP = 0.16                       # ritmo de Short: pausas cortas entre frases
SUBTITULOS = False
TRANSICIONES = [("continua", 0.5)] * 5     # plano secuencia: los cambios de escena los dibuja escenas.py
MEZCLA = dict(musica=-24.0, sfx=-24.0, fx=-17.0)
VOZ = dict(motor="elevenlabs", voice_id="nMPrFLO7QElx9wTR0JGo", modelo="eleven_multilingual_v2", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/mods_ia_fusion/ref_ginyin.mp3",
           tomas=1, stability=0.38, similarity_boost=0.8, style=0.5)
LYRIA = dict(
    estilo="Modern dark electronic explainer underscore: punchy synthwave and glitch-hop, tight drums, pulsing bass arpeggios, "
           "digital textures, energetic and addictive, 120 BPM, instrumental only, no vocals.",
    escenas={
        "gancho": ("starts immediately with a punchy beat and a catchy synth stab, high energy hook", 8),
        "puente": ("steady driving groove, curious and technical, arpeggios like data flowing, light percussion", 6),
        "limite": ("the beat drops out, dark tense bass hit and a rising sweep", 5),
        "reescribir": ("the beat returns harder, glitchy and mechanical, building in layers", 7),
        "verdad": ("half-time, more serious and thoughtful, sparse drums, warm pad", 5),
        "cierre": ("big uplifting final build, full drums and bright synths, then a clean ending", 9),
    })
CER_MAX_POR_FRASE = {"gancho_0": 0.2, "reescribir_4": 0.2}     # Minecraft, Skyrim, Skate: Whisper los escribe a su manera

ESCENAS = [
    {
        "id": "gancho", "pre": 0.25,
        "frases": [
            "Esto es Minecraft, dentro de Skyrim. Y no es un montaje.",
            "Puedes poner bloques, volar, y tirarle dinamita a tus enemigos.",
            "Lo raro es cómo funciona.",
            "Porque hay dos formas de fusionar juegos. Y la segunda da un poco de miedo.",
        ],
    },
    {
        "id": "puente",
        "frases": [
            "La primera es un puente.",
            "Los dos juegos corren al mismo tiempo, como dos programas separados.",
            "Uno de ellos está escondido: sin ventana y sin sonido.",
            "Y en medio hay un pedazo de memoria que los dos pueden leer y escribir.",
            "Ahí, cientos de veces por segundo, se pasan notas: dónde está el jugador, qué bloque puso, a quién golpeó.",
            "Minecraft manda en tu personaje. Skyrim pone el mundo, los enemigos y los choques.",
            "Y ninguno de los dos sabe que el otro existe. Cada uno cree que todo pasa en su propio mundo.",
        ],
    },
    {
        "id": "limite",
        "frases": [
            "Pero el puente tiene un límite: sigues atrapado en los motores originales.",
        ],
    },
    {
        "id": "reescribir",
        "frases": [
            "La segunda forma no conecta nada. Lo reescribe todo.",
            "Un juego no trae su código. Trae millones de instrucciones para la máquina, imposibles de leer.",
            "Recompilar es traducir esas instrucciones para otra máquina, sin entenderlas.",
            "Decompilar va más lejos: reconstruye el código, función por función, hasta que una persona puede leerlo.",
            "Así renació Skate tres: en un motor nuevo y libre, sin una sola línea del código original.",
        ],
    },
    {
        "id": "verdad",
        "frases": [
            "Dicen que una inteligencia artificial lo hizo en una semana. No es toda la verdad.",
            "Antes, una persona pasó más de dos años descifrando ese juego a mano.",
            "La máquina no descubrió nada. Convirtió ese conocimiento en código, a una velocidad absurda.",
        ],
    },
    {
        "id": "cierre", "post": 1.1,
        "frases": [
            "Y eso es lo fuerte. Si las reglas de un juego se pueden reescribir, se pueden mezclar con las de cualquier otro.",
            "El límite ya no es lo que sabes programar. Es lo que te atreves a imaginar.",
            "¿Qué dos juegos fusionarías tú?",
        ],
    },
]
