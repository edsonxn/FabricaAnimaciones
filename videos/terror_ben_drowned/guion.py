# -*- coding: utf-8 -*-
"""BEN Drowned: el cartucho maldito de Zelda (PRUEBA del estilo «terror 2D» para un canal de terror en videojuegos, ~1 min, 16:9).
Estilo `terror` (kit pix.py + terror.py): cuarto a oscuras donde la única luz es una tele CRT dibujada en 2D; el video real del
juego (yt-dlp) SIEMPRE vive dentro de esa tele (curvatura, scanlines, tracking de VHS) y se corrompe hasta salirse al cuarto.
Voz ElevenLabs «David» (la de LogIA) con eleven_v4 + corchetes de actuación; música Lyria de terror incómodo. Sin subtítulos.

Hechos (verificados el 12-oct-2026 en Wikipedia «Ben Drowned» y su bibliografía):
  - Es FICCIÓN: relato en serie / creepypasta con formato de ARG, de Alexander D. Hall, que firmaba «Jadusable».
  - Capítulos diarios del 7 al 15-sep-2010 en el tablero /x/ de 4chan, más videos de YouTube, sitios web y participación del público.
  - Premisa: un estudiante universitario compra un cartucho rotulado «Majora» en una venta de garaje; la partida guardada era de «Ben»,
    un niño de 12 años que se ahogó años antes. El «glitch del día cuatro»: salta el final del tercer día y Clock Town queda vacía;
    el vendedor de máscaras ríe sin parar; Link se ahoga en un estanque y la Canción de la Curación suena al revés;
    la estatua de Link (Elegía del Vacío) sigue al jugador y lo mira.
  - Legado: «una de las series web más populares» (millones de lectores); influyó en Petscop y Doki Doki Literature Club!
Gameplay real (clips/ , créditos en clips/creditos_clips.json): MojaveMyth (vendedor), ZeldaPowerVideos (estatua), 黒毛皮 (noche).
"""

TITULO = "BEN Drowned: el cartucho maldito"
ARCHIVO = "terror_ben_drowned"
ESTILO_VISUAL = "documental"     # motion graphics dibujados propios; variante «terror» (docs/estilo_terror_crt.md)
DURACION = None
BPM = 70
SUBTITULOS = False
GAP = 0.45
TRANSICIONES = [("continua", 0.5)] * 3          # plano secuencia: los cambios de escena los dibuja escenas.py
MEZCLA = dict(musica=-20.0, sfx=-24.0, fx=-17.0)
VOZ = dict(motor="elevenlabs", voice_id="0hh7H4ZVAtaGpm1VZyEN", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/terror_ben_drowned/ref_david.mp3",
           tomas=1, stability=0.5)
LYRIA = dict(
    estilo="Disturbing horror ambient underscore: detuned music box, low sub drones, dissonant strings, reversed sounds, "
           "tape warble and distant static, slow, uneasy and claustrophobic, instrumental only, no vocals, no drums.",
    escenas={
        "cartucho": ("almost silent, a lonely detuned music box and a cold low drone slowly fading in, patient dread", 3),
        "falla": ("the drone grows, dissonant string clusters, glitchy tape stutters and a faint heartbeat pulse", 6),
        "ben": ("sorrowful and wrong, the music box melody played backwards and slightly out of tune, child-like and cold", 5),
        "cierre": ("everything collapses into static and a high sustained dissonant tone, then an abrupt cut to silence", 7),
    })
CER_MAX_POR_FRASE = {"ben_1": 0.12}             # «Jadusable» y «Alex Hall»: Whisper los escribe a su manera

ESCENAS = [
    {
        "id": "cartucho", "pre": 1.8, "post": 0.4,
        "frases": [
            "[whispers] Septiembre de 2010. Un estudiante compra un cartucho usado de Zelda en una venta de garaje.",
            "[short pause] La partida guardada ya tenía dueño. [serious] Se llamaba Ben.",
        ],
    },
    {
        "id": "falla", "pre": 0.3, "post": 0.4,
        "frases": [
            "[thoughtful] Esa noche el juego empezó a fallar. El tercer día se saltaba su final, y el pueblo se quedaba vacío.",
            "El vendedor de máscaras no paraba de reír. [short pause] Y una estatua de Link lo seguía con la mirada.",
        ],
    },
    {
        "id": "ben", "pre": 0.3, "post": 0.4,
        "frases": [
            "[serious] Según el relato, Ben era un niño de 12 años que se había ahogado. [short pause] Y desde el cartucho, intentaba hablar.",
            "[sighs] Todo era ficción. Un relato por capítulos de Alex Hall, que firmaba como Jadusable.",
        ],
    },
    {
        "id": "cierre", "pre": 0.3, "post": 2.2,
        "frases": [
            "Pero lo publicó como si fuera real: con videos, páginas web y mensajes. [short pause] Y millones lo leyeron sin saber dónde terminaba el juego.",
            "[whispers] Desde entonces, cada vez que un juego hace algo que no debería... [short pause] alguien se acuerda de Ben.",
        ],
    },
]
