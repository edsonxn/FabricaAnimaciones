# -*- coding: utf-8 -*-
"""Sonic.exe: el CD maldito que nunca existió (Crónicas del gaming, primer video largo de terror, ~5 min, 16:9).
Estilo `terror` (kit pix.py + terror.py, docs/estilo_terror_crt.md): cuarto a oscuras cuya única luz es una pantalla dibujada en 2D
(aquí un MONITOR CRT de PC, no la tele de Ben: el relato es un port de PC); el gameplay real (yt-dlp) vive SIEMPRE dentro de esa pantalla.
Voz ElevenLabs «David» (eleven_v4) con corchetes; música Lyria de terror incómodo. Sin subtítulos.

Hechos (verificados el 13-oct-2026 en Wikipedia «Sonic.exe», Know Your Meme, Daily Dot y Dictionary.com; NO de memoria):
  - Es FICCIÓN: creepypasta de un usuario llamado JC-the-Hyena, enviado a la Creepypasta Wiki el 9-ago-2011. Inspirado, dijo el autor, en una
    captura de pantalla retocada de la pantalla de título de Sonic the Hedgehog (Sega Genesis, 1991). Texto original ≈ 4 149 palabras.
  - Premisa: Tom recibe de su amigo Kyle un CD-R rotulado «SONIC.EXE» con una nota (escrita bajo presión) que le pide no jugarlo / destruirlo.
    OJO: es un CD-R en PC, NO un cartucho (el Short de referencia ×8,7 lo llama «cartucho»: impreciso; aquí se corrige).
  - Pantalla de título alterada: cielo oscuro, emblema oxidado, «SEGA 1991» → «SEGA 666», el agua se vuelve roja (Daily Dot).
  - Tails, Knuckles y el villano de la saga (Eggman/Robotnik según la fuente: en el guion solo «el villano de la saga») son cazados y
    muertos por un Sonic demoníaco: ojos negros que sangran con pupilas rojas brillantes (Dictionary.com). Final: Tom se gira y hay un
    peluche de Sonic en su cama con sangre saliendo de los ojos.
  - Juego fan: MY5TCrimson en GameJolt, ago-2012 (KYM: 13-ago-2012); PewDiePie subió su partida meses después (Daily Dot).
  - 14-ene-2014: la Creepypasta Wiki borra el relato (según el autor: «badly written», «too many cliches»); el autor responde con un blog
    furioso pidiendo a los fans que se rebelaran (Daily Dot). Hoy es sobre todo una broma de internet.
  - Ben Drowned (el video anterior del kit): sept-2010, mismo género.
  NO usar: «I AM GOD» (una sola fuente), métodos de muerte concretos (sitio no fiable), cifras de vistas (ninguna fuente las da).
Gameplay real (clips/, créditos en clips/creditos_clips.json): por elegir con hoja de contacto.
"""

TITULO = "Sonic.exe: el CD maldito que nunca existió"
ARCHIVO = "sonic_exe"
ESTILO_VISUAL = "documental"     # motion graphics dibujados propios; variante «terror» (docs/estilo_terror_crt.md)
DURACION = None
BPM = 70
SUBTITULOS = False
GAP = 0.45
TRANSICIONES = [("continua", 0.5)] * 6          # plano secuencia: los cambios de escena los dibuja escenas.py
MEZCLA = dict(musica=-20.0, sfx=-24.0, fx=-17.0)
VOZ = dict(motor="elevenlabs", voice_id="0hh7H4ZVAtaGpm1VZyEN", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/sonic_exe/ref_david.mp3",
           tomas=1, stability=0.5)
LYRIA = dict(
    estilo="Disturbing horror ambient underscore: detuned music box, low sub drones, dissonant strings, reversed sounds, "
           "tape warble, floppy-disk and CD-drive noise and distant static, slow, uneasy and claustrophobic, "
           "instrumental only, no vocals, no drums.",
    escenas={
        "cd": ("almost silent, a lonely detuned music box and a cold low drone slowly fading in, patient dread", 3),
        "titulo": ("a warped, slowed-down cheerful 16-bit chiptune melody played out of tune over a deep drone", 6),
        "niveles": ("relentless, the drone grows, dissonant string clusters, glitchy tape stutters and a fast heartbeat pulse", 6),
        "final": ("everything drops out, a single high sustained dissonant tone, then a cold silence", 7),
        "autor": ("cold and sober, a bare low piano note and a faint tape hiss, uneasy calm after the storm", 4),
        "legado": ("slightly ironic, a detuned music box with distant static, the dread fading into resignation", 4),
        "cierre": ("the music box melody returns slowly, a low drone swells, ending in static and an abrupt cut to silence", 7),
    },
    # 224,6 s > lo que Lyria da de una vez: dos tramos que cortan en el giro «nada de esto ocurrió» (106,3 s)
    tramos=[(["cd", "titulo", "niveles", "final"],
             "Begin almost silent. Build slowly into relentless dread, then drop everything out into a single high held tone and a cold silence."),
            (["autor", "legado", "cierre"],
             "Begin cold and sober after silence. Stay uneasy but calm, then slowly swell and end on static and an abrupt cut to silence.")])
CER_MAX_POR_FRASE = {"cd_0": 0.15, "autor_0": 0.15, "autor_2": 0.12, "legado_0": 0.15, "legado_3": 0.15}   # «Sonic punto exe», «JC the Hyena», «MY5TCrimson»

ESCENAS = [
    {
        "id": "cd", "pre": 1.8, "post": 0.4,
        "frases": [
            "[whispers] Agosto de 2011. Un chico llamado Tom recibe un CD sin carátula, grabado a mano. En el disco hay una sola palabra: Sonic punto exe.",
            "Se lo manda su amigo Kyle, con una nota que parece escrita bajo presión. [serious] Le pide que no lo juegue. Que lo destruya.",
            "[short pause] Pero es Sonic. [thoughtful] Un erizo azul, un juego de siempre. ¿Qué podía salir mal? Tom lo mete en la computadora.",
        ],
    },
    {
        "id": "titulo", "pre": 0.3, "post": 0.4,
        "frases": [
            "La pantalla de título aparece, y todo está mal. [short pause] El cielo es más oscuro. El emblema parece oxidado.",
            "Donde antes decía SEGA 1991, ahora dice SEGA 666. [whispers] Y el agua del primer nivel ya no es azul. Es roja.",
            "[sighs] Cualquiera apagaría. Tom pulsa start.",
        ],
    },
    {
        "id": "niveles", "pre": 0.3, "post": 0.4,
        "frases": [
            "[serious] Lo que sigue es una cacería. Un Sonic que ya no es Sonic persigue a sus amigos, uno por uno.",
            "Tiene los ojos negros, sangrando, con la pupila roja brillando al fondo. [short pause] Tails es el primero. Después, Knuckles. Y al final, hasta el villano de la saga.",
            "[thoughtful] En cada nivel, un amigo menos. [short pause] Y cuando ya no quedan amigos, queda Tom.",
        ],
    },
    {
        "id": "final", "pre": 0.3, "post": 0.6,
        "frases": [
            "Tom apaga la computadora. [short pause] Se da la vuelta. [whispers] Sobre su cama, un peluche de Sonic lo mira... y de sus ojos sale sangre.",
            "[sighs] Fin del relato. Y ahora, lo incómodo: nada de esto ocurrió.",
        ],
    },
    {
        "id": "autor", "pre": 0.9, "post": 0.4,
        "frases": [
            "[serious] Sonic punto exe es ficción. Lo escribió un usuario que firmaba JC the Hyena, y lo subió el 9 de agosto de 2011 a la Creepypasta Wiki.",
            "No había ningún disco. No había ningún Kyle. [short pause] Había una captura de pantalla retocada del título del Sonic original, y una idea.",
            "El nombre es parte del truco. Un archivo punto exe es un programa que se ejecuta en tu computadora. [whispers] No es una historia que lees. Es algo que corres.",
            "Su estilo es amateur y está lleno de tópicos. [short pause] Pero funcionó, porque todos conocemos ese primer nivel, y verlo mal inquieta.",
        ],
    },
    {
        "id": "legado", "pre": 0.3, "post": 0.4,
        "frases": [
            "[thoughtful] La historia se hizo grande. En agosto de 2012, un usuario llamado MY5TCrimson publicó en GameJolt un juego jugable basado en el relato.",
            "Meses después, PewDiePie subió su partida a YouTube. [short pause] El disco que nunca existió se volvió un juego que cualquiera podía descargar.",
            "En enero de 2014, la Creepypasta Wiki borró el relato. [serious] Según su autor, por estar mal escrito y lleno de clichés.",
            "JC the Hyena respondió con un blog furioso, pidiendo a sus fans que se rebelaran. [sighs] Y poco a poco, Sonic punto exe pasó de leyenda de terror a broma de internet.",
        ],
    },
    {
        "id": "cierre", "pre": 0.3, "post": 2.2,
        "frases": [
            "Un año antes, Ben Drowned había hecho lo mismo con Zelda. [short pause] Un juego conocido, un detalle fuera de lugar, y la duda.",
            "Nunca hizo falta un disco real. Bastó una captura retocada, unas cuantas palabras, y mucha gente mirando una pantalla de título, esperando que cambiara.",
            "[whispers] Así que si algún día un amigo te manda un disco sin carátula... [short pause] ni se te ocurra pulsar start.",
        ],
    },
]
