# -*- coding: utf-8 -*-
"""Segundo anuncio de «Dúo · Misiones en pareja» (app de E:/CalendarioPareja, versión 24), vertical, ~60 s, sin canal.

PRIMER comercial real (el usuario, 21-oct: videos/duo_promo/ fue solo una prueba): presenta Dúo desde cero a quien no la conoce.
Estilo: el de la app (modo oscuro): fondo #17121C con manchas difusas coral/violeta, tarjetas #221B29 borde #32283B, radio 22 px,
degradado #FF8A5B -> #FF5E7E -> #8B5CF6, Plus Jakarta Sans (fuentes/), emojis de color. Kit `duo.py` (pintor, fondo, teléfono,
componentes); las escenas y los componentes nuevos (juegos, hogar isométrico, huerto, ciclo, guía) son PROPIOS de este video.
Referencias de la UI real: E:/CalendarioPareja/guia/*.webp (man-juegos, v10-cochinito, v12-hogar, v24-huerto, v21-consejos,
v11-guia, v12-embarazo) y el arreglo CHANGES de index.html.

Funciones nuevas que muestra (decisión del usuario, 21-oct-2026: las cuatro):
  - misiones a la medida (LOVE_FIT, según lo que contestó cada quien) + «📍 Estamos a distancia» (misiones FAR: tie40
    «Cenen "juntos" por videollamada: cada quien con su plato, a la misma hora.») + notificaciones
  - Juegos por turnos, asíncronos: ¿Qué tanto me conoces?, Dibújalo, 4 en línea (premio: «Le debes: masaje»), Torre al cielo,
    Asalto al cochinito (resortera contra el fuerte, cochinito-alcancía 🐷)
  - Nuestro hogar (casa 3D isométrica que decoran con 🪙 monedas que salen de su XP) + huerto (v24: crece con el tiempo
    mientras su tanque 💧 tenga agua; 17 plantas: tulipanes, girasoles, fresas, chiles, elotes, cempasúchil, nopales, piñas…)
  - Mi ciclo («💡 Para ti» por fase, avisos) / Ciclo de (nombre) con la «Guía para acompañar» estilo revista + modo embarazo
Cierre: logo + lema + «Descarga Dúo» + insignias genéricas App Store / Google Play, SIN URL (el usuario, 13 y 21-oct).
"""

TITULO = "Dúo · Misiones en pareja (lo nuevo)"
ARCHIVO = "duo_promo_60"
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
           referencia="C:/FabricaAnimaciones/videos/duo_promo_60/ref_lina.mp3", tomas=1, stability=0.5)
VOZ_POR_FRASE = {"gancho_0": ERIC, "medida_1": ERIC, "juegos_1": ERIC, "juegos_3": ERIC,
                 "hogar_1": ERIC, "ciclo_1": ERIC, "cierre_1": ERIC}
CER_MAX_POR_FRASE = {"gancho_1": 0.25, "cierre_0": 0.2, "juegos_1": 0.25}   # «Dúo», «Dibújalo»: Whisper varía acentos

LYRIA = dict(
    estilo="Warm modern feel-good pop for a couples app commercial: bright plucked guitar and ukulele, soft hand claps and "
           "finger snaps, warm synth pads, playful marimba and glockenspiel accents, romantic and cheerful, 108 BPM, "
           "instrumental only, no vocals.",
    escenas={
        "gancho": ("sparse and a little tired, a lonely plucked guitar and a soft tick, then a hopeful lift", 3),
        "medida": ("the beat kicks in with claps and a bright catchy hook, warm and personal", 6),
        "juegos": ("playful competitive groove, bouncy marimba, quick arcade-like glockenspiel blips, rising energy", 9),
        "hogar": ("cozy and sweet, softer drums, warm pad, gentle growing arpeggio like plants sprouting", 6),
        "ciclo": ("tender and caring, light percussion, warm pad and glockenspiel", 5),
        "cierre": ("full joyful chorus, big warm ending and a clean final note", 8),
    })

ESCENAS = [
    {
        "id": "gancho", "pre": 0.3, "post": 0.1,
        "frases": [
            "[sighs] Llegamos cansados, y cada quien se pierde en su celular…",
            "[laughs] Hasta que probamos Dúo.",
        ],
    },
    {
        "id": "medida", "pre": 0.1, "post": 0.3,
        "frases": [
            "Cada día nos da misiones para hacer juntos, según lo que contestó cada quien.",
            "Y si estamos lejos, cambian: cenar juntos por videollamada.",
        ],
    },
    {
        "id": "juegos", "pre": 0.1, "post": 0.1,
        "frases": [
            "[excited] ¡Y hay juegos para dos, por turnos, aunque no estemos conectados al mismo tiempo!",
            "¿Qué tanto me conoces? Dibújalo. Torre al cielo.",
            "Y en cuatro en línea… [whispers] me debes un masaje.",
            "[sighs] Revancha en el Asalto al cochinito.",
        ],
    },
    {
        "id": "hogar", "pre": 0.1, "post": 0.1,
        "frases": [
            "Con lo que ganamos en las misiones, decoramos nuestro hogar.",
            "[chuckles] Y tenemos un huerto que crece de verdad… si nos acordamos de regarlo.",
        ],
    },
    {
        "id": "ciclo", "pre": 0.1, "post": 0.1,
        "frases": [
            "Yo llevo mi ciclo, con consejos para cada fase.",
            "Y a mí me sale una guía para acompañarla. [softly] Hasta en el embarazo.",
        ],
    },
    {
        "id": "cierre", "pre": 0.1, "post": 1.3,
        "frases": [
            "Dúo. Misiones diarias para crecer en pareja.",
            "Descárguenla y jueguen hoy.",
        ],
    },
]
