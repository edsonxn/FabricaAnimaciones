# -*- coding: utf-8 -*-
"""BEN Drowned: el cartucho maldito que nunca existió (Crónicas del gaming, 2.º video largo de terror, ~5 min, 16:9).
Misma fórmula que `sonic_exe` (historia en 3.ª persona + revelación «es ficción» + legado); variable: SOLO la leyenda
(canales/formula/cronicas_gaming.md, hipótesis 2). Estilo terror CRT (docs/estilo_terror_crt.md): cuarto a oscuras cuya única luz es
la TELE CRT dibujada (aquí sí tele + Nintendo 64, como la prueba `terror_ben_drowned`); el gameplay real (yt-dlp) vive SIEMPRE dentro.
Voz ElevenLabs «David» (eleven_v4) con corchetes; Lyria de terror. Sin subtítulos. Escenas NUEVAS (la prueba de 67 s solo aporta investigación).

Hechos (verificados el 18-oct-2026 en Wikipedia «Ben Drowned» y ARGN, Michael Andersen 31-oct-2020; NO de memoria):
  - FICCIÓN: ARG / serie web en tres partes de Alexander D. Hall, que firmaba «Jadusable». Primer arco publicado a diario del 7 al
    15-sep-2010 en /x/ de 4chan, con videos de YouTube («day four.wmv», «BEN.wmv») como prueba del relato en 1.ª persona.
  - Cartucho de N64 sin etiqueta, solo «MAJORA» escrito a plumón negro (ARGN); se lo vende un anciano inquietante en una venta de garaje
    (Wikipedia); la partida guardada de un antiguo dueño, «BEN», seguía ahí. Majora's Mask es de 2000.
  - En orden: inconsistencias → glitch del día cuatro (se salta el final del 3.er día, explora como en los créditos, Ciudad Reloj vacía,
    risa del vendedor de máscaras) → ahoga a Link en un estanque buscando un Game Over: Link grita, destello del vendedor, Canción de la
    Curación al revés → la estatua de la Elegía del Vacío lo sigue fuera de cámara; al girarla, vendedor, estatua y Link se quedan
    quietos mirándolo → días de sucesos (arde, queda inconsciente mientras Skull Kid observa) → quiere devolver el cartucho, el anciano se
    mudó; un vecino cuenta lo de la casa: Ben, 12 años, se ahogó unos ocho años antes → «BEN» le habla dentro y fuera del juego (fondo de
    pantalla con la estatua, Cleverbot), toma su PC, publica una versión falsa en 4chan y YouTube y escapa a internet: «Now I am everywhere».
    Epílogo del compañero de cuarto Tyler; archivo final TheTruth.rtf; Jadusable no vuelve a aparecer.
  - Kotaku (Owen Good) lo reseñó a los ~2 meses y los lectores se cuadruplicaron. Hall: «an obvious work of fiction».
  - Moon Children (17-sep-2010 → hiatus 15-jul-2011): cifra en su canal → youshouldnthavedonethat.net, foro de una secta; el sitio se
    reinicia cada tres días; las decisiones de los lectores cambian la historia; algunos lectores recibieron recortes de periódico.
  - Awakening: 17-mar-2020 → 31-oct-2020 (ARGN: «almost a decade»). Influencia: inspiración principal de Petscop (Fanbyte); influencia
    indirecta de Doki Doki Literature Club! (vía GIFfany de Gravity Falls).
  NO usar: el caso real de 2016 citado en Wikipedia (una menor; tema de suicidio), frases del anciano («goodbye then»: sin fuente
  verificada), cifras de lectores (ninguna fuente fiable da una), Clive Barker / película (fuera de la historia).
Gameplay real (clips/, créditos en clips/creditos_clips.json): por elegir con hoja de contacto (tramo 2).
"""

TITULO = "BEN Drowned: el cartucho maldito que nunca existió"
ARCHIVO = "ben_drowned"
ESTILO_VISUAL = "documental"     # motion graphics dibujados propios; variante «terror» (docs/estilo_terror_crt.md)
DURACION = None
BPM = 70
SUBTITULOS = False
GAP = 0.45
TRANSICIONES = [("continua", 0.5)] * 8          # plano secuencia: los cambios de escena los dibuja escenas.py
MEZCLA = dict(musica=-20.0, sfx=-24.0, fx=-17.0)
VOZ = dict(motor="elevenlabs", voice_id="0hh7H4ZVAtaGpm1VZyEN", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/ben_drowned/ref_david.mp3",
           tomas=1, stability=0.5)
LYRIA = dict(
    estilo="Disturbing horror ambient underscore: detuned music box, low sub drones, dissonant strings, reversed sounds, "
           "tape warble, cartridge hum and distant static, slow, uneasy and claustrophobic, instrumental only, no vocals, no drums.",
    escenas={
        "cartucho": ("almost silent, a lonely detuned music box and a cold low drone slowly fading in, patient dread", 3),
        "falla": ("a faint warped ocarina-like melody over a growing drone, distant mocking echoes, something is off", 5),
        "ahogo": ("a gentle lullaby melody played backwards and out of tune, sinking under water, a muffled scream of strings", 6),
        "estatua": ("very quiet and tense, a single sustained low note, tiny glitch clicks, the feeling of being watched", 6),
        "ben": ("sorrowful and wrong, child-like music box, cold, then a rising digital distortion spreading everywhere", 7),
        "final": ("everything drops out, a single high sustained dissonant tone, then a cold silence", 7),
        "autor": ("cold and sober, a bare low piano note and a faint tape hiss, uneasy calm after the storm", 4),
        "legado": ("a slow cryptic pulse, faint radio static and a looping three-note motif, mystery that keeps growing", 5),
        "cierre": ("the reversed lullaby returns slowly, a low drone swells, ending in static and an abrupt cut to silence", 7),
    },
    # ~5 min > lo que Lyria da de una vez: dos tramos que cortan en el giro «nada de esto ocurrió» (fin de `final`)
    tramos=[(["cartucho", "falla", "ahogo", "estatua", "ben", "final"],
             "Begin almost silent. Build slowly into relentless dread, then drop everything out into a single high held tone and a cold silence."),
            (["autor", "legado", "cierre"],
             "Begin cold and sober after silence. Stay uneasy but calm, then slowly swell and end on static and an abrupt cut to silence.")])
# nombres propios y en inglés: Whisper los escribe a su manera
CER_MAX_POR_FRASE = {"cartucho_1": 0.15, "cartucho_2": 0.15, "ben_2": 0.12, "final_0": 0.15, "autor_0": 0.15,
                     "legado_0": 0.2, "legado_1": 0.15, "legado_4": 0.2, "cierre_0": 0.15}

ESCENAS = [
    {
        "id": "cartucho", "pre": 1.8, "post": 0.4,
        "frases": [
            "[whispers] Septiembre de 2010. Un estudiante va a una venta de garaje, y un anciano que le da mala espina le vende un cartucho de Nintendo 64.",
            "No tiene etiqueta. [short pause] Solo una palabra, escrita a mano con plumón negro: Majora.",
            "Es Zelda: Majora's Mask. Lo conecta, y ve que alguien dejó una partida guardada. [serious] Se llama BEN.",
            "[thoughtful] Lo que pasó después lo fue contando él mismo, día a día, en el foro paranormal de 4chan. Con videos como prueba.",
        ],
    },
    {
        "id": "falla", "pre": 0.3, "post": 0.4,
        "frases": [
            "Al principio son detalles. Cosas que no están donde deberían. [short pause] Nada que no explique un cartucho viejo.",
            "Hasta que provoca un error conocido como el glitch del día cuatro. El tercer día se salta su final, y el mundo sigue, como en los créditos.",
            "[whispers] La Ciudad Reloj está vacía. No queda nadie. [short pause] Solo se oye una risa: la del vendedor de máscaras.",
        ],
    },
    {
        "id": "ahogo", "pre": 0.3, "post": 0.4,
        "frases": [
            "[serious] Para salir de ahí, deja que Link se ahogue en un estanque. Quiere un Game Over. Volver a empezar.",
            "Link grita. [short pause] La pantalla salta a la cara del vendedor de máscaras. Y la Canción de la Curación empieza a sonar... [whispers] al revés.",
        ],
    },
    {
        "id": "estatua", "pre": 0.3, "post": 0.4,
        "frases": [
            "Entonces aparece ella: la Elegía del Vacío. Una estatua con la cara de Link, sin ninguna expresión.",
            "[whispers] Lo sigue por el mapa, siempre justo fuera de cámara. [short pause] Cuando gira la cámara para verla, todo se congela, y los tres lo miran a él.",
            "[nervous] En los días siguientes, Link arde sin motivo, cae inconsciente, y Skull Kid lo observa en silencio.",
        ],
    },
    {
        "id": "ben", "pre": 0.3, "post": 0.4,
        "frases": [
            "[thoughtful] Asustado, intenta devolver el cartucho. Pero el anciano ya se ha mudado.",
            "Un vecino le cuenta lo que pasó en esa casa. [short pause] Ahí vivía un niño de doce años que se ahogó, unos ocho años antes. [serious] Se llamaba Ben.",
            "Y algo que se hace llamar BEN empieza a hablarle, dentro del juego y fuera de él. Le pone la estatua de fondo de pantalla. Le escribe a través de Cleverbot.",
            "[whispers] Al final se adueña de su computadora, publica una versión falsa de la historia, y escapa a internet con una frase: ahora estoy en todas partes.",
        ],
    },
    {
        "id": "final", "pre": 0.3, "post": 0.6,
        "frases": [
            "Su compañero de cuarto, Tyler, escribe un epílogo. Queda un último archivo, llamado La Verdad. [short pause] Y Jadusable no vuelve a aparecer.",
            "[sighs] Fin del relato. Y ahora, lo incómodo: nada de esto ocurrió.",
        ],
    },
    {
        "id": "autor", "pre": 0.9, "post": 0.4,
        "frases": [
            "[serious] BEN Drowned es ficción. Lo escribió Alexander D. Hall, que firmaba como Jadusable, y lo publicó por capítulos, del 7 al 15 de septiembre de 2010.",
            "No hubo venta de garaje. Ni anciano. Ni niño ahogado. [short pause] Hubo un Zelda del año 2000, unos videos grabados con mucho cuidado, y una idea.",
            "El truco era el formato. No era un cuento que leías: era alguien publicando en vivo, con grabaciones del juego como prueba. [whispers] Y los lectores le respondían.",
            "A los dos meses, Kotaku escribió sobre la historia, y sus lectores se multiplicaron por cuatro. [short pause] Años después, el propio Hall la llamó una obra de ficción evidente.",
        ],
    },
    {
        "id": "legado", "pre": 0.3, "post": 0.4,
        "frases": [
            "[thoughtful] Pero no terminó ahí. En el canal de Jadusable apareció un mensaje cifrado, que llevaba a una web llamada You shouldn't have done that. No debiste hacer eso.",
            "Era el foro de una secta inventada, los Moon Children. [short pause] La página se reiniciaba cada tres días, como el juego, y lo que hacían los lectores cambiaba la historia.",
            "[whispers] A algunos lectores incluso les llegaron recortes de periódico. La ficción ya se había salido de la pantalla.",
            "[sighs] En julio de 2011, Hall la dejó en pausa. Casi diez años después, en marzo de 2020, el canal volvió a la vida. Y la historia terminó el 31 de octubre de 2020. En Halloween.",
            "Su sombra llega lejos: se le cita como la inspiración principal de Petscop, y como influencia indirecta de Doki Doki Literature Club.",
        ],
    },
    {
        "id": "cierre", "pre": 0.3, "post": 2.2,
        "frases": [
            "Menos de un año después, Sonic punto exe usaría la misma receta. [short pause] Un juego conocido, un detalle fuera de lugar, y la duda.",
            "Ben nunca existió. Pero durante unos días de 2010, mucha gente miró una partida de Majora's Mask, esperando ver una estatua donde no debía estar.",
            "[whispers] Así que si algún día alguien te vende un cartucho con una sola palabra escrita a mano... [short pause] no mires la partida guardada.",
        ],
    },
]
