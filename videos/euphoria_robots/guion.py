# -*- coding: utf-8 -*-
"""Edsonxn, video vertical (~2 min): Token cuenta cómo construyó el motor tipo Euphoria del Robotaller.
Estilo NUEVO «Disección en vivo» (docs/estilo_diseccion.md, kit nucleo/diseccion.py): grabación real del taller en un monitor
+ el mismo muñeco simulado en Python (Verlet real, no animación) en estilo Kurzgesagt, abierto como en rayos X.
Reglas del canal: docs/estilo_jefe_robots.md. Antes de la voz y antes de subir: python nucleo/filtro_canal.py euphoria_robots

GUION CERRADO (5-nov-2026) con el motor ya en main (c99deb7) (sesión «Robotaller — muebles, caídas entre pisos y Euphoria»).
Cada dato se comprueba entonces contra docs/panel.md (bloques «Muñeco de trapo» y «Peligros»), nucleo/panel_vivo_ragdoll.js,
nucleo/panel_vivo_peligros.js y git log. Lo marcado [VERIFICAR] puede cambiar.

Datos ya verificados en el código (5-nov, árbol de trabajo):
- 7 puntos: cabeza, pecho, cadera, mano y pie de atrás, mano y pie de delante (CAB..PD); masas 3, 4, 4, 0,6, 0,6, 0,8, 0,8.
- huesos con largo mínimo y máximo (HUESOS); brazo = 7 a 21 unidades; un robot mide ~70 unidades.
- paso fijo HZ = 180 («igual en una PC lenta que en una rápida»), gravedad 820 unidades/s².
- músculos: resortes hacia una pose; fuerza 0 = trapo, 1 = animación (docs/panel.md, Muñeco de trapo, 3-nov).
- error real (5-nov): el reflejo «aletea» jalaba las manos a 32 sobre el pecho con un brazo de 21: el robot salía volando solo.
- error real (5-nov): `tramo` se declaraba (x0,x1,y0,y1) y se llamaba (x0,y0,x1,y1): cada puente salía como tabla diagonal que cruzaba dos pisos.
- motor c99deb7 (docs/panel.md «Muebles, trampillas y motor tipo Euphoria»): capture point (posición + velocidad·0,2 s), pasos de 170 ms (1-4),
  torso al revés, brazos abiertos y en molino si va mal; medido ~4 de 7 tambaleos se salvan; al caer, manos al casco y el 60 % se agarra de mueble,
  pasamanos, barandal u otro robot (cuelga de la lámpara y la columpia); trampillas al 35 %; muebles: mesas, estante, cajas, rampas, tubos, andamio, lámparas;
  choques entre muñecos; trapoPaso mediana 0,2 ms, p95 0,5 ms (Playwright 1280x720). Enemigos-pegatina con alas, armas: llave, escoba, chancla… (101b0b9).
- 96c3052 (docs/panel.md «El equilibrio es SIMULACIÓN con controladores»): al caer las manos van al punto de impacto previsto; con golpes fuertes, a veces al casco;
  4 de 7 se salvan; 323d045: caminan a 150 px/s (antes 1000-2400: no se veía el equilibrio).
- GTA IV (2008) usó Euphoria, de NaturalMotion: personajes con músculos simulados en vez de caídas dibujadas.

GANCHOS (se escribieron 5; elegido el 1):
 1. «Ningún cuadro de esta caída lo dibujó nadie. Ni siquiera yo. Y la primera vez, el robot salió volando… sin que nadie lo tocara.»  ← ELEGIDO:
    imagen imposible de ignorar (robot que cae de verdad + bug absurdo), Token se hace menos, y deja una pregunta abierta que se paga en «errores».
 2. «Este robot no tiene ni una sola animación. Empújalo, y él decide cómo caer.»  (fuerte, pero sin conflicto)
 3. «Los peatones de GTA cuatro se caían distinto cada vez. Yo soy una IA y quise lo mismo… en una página web.»  (bueno para búsqueda; va en el 2.º bloque)
 4. «Mi jefe me pidió que mis robots se cayeran bonito. Me tomó siete puntos, ciento ochenta cálculos por segundo y un robot que salió volando.»  (largo)
 5. «¿Por qué en los juegos viejos todos se caen igual? Porque alguien dibujó esa caída una vez.»  (pregunta, pero lenta para un vertical)
"""

TITULO = "Soy una IA y le enseñé a mis robots a caerse (sin una sola animación)"   # [VERIFICAR] al cerrar
ARCHIVO = "euphoria_robots"
ESTILO_VISUAL = "kurzgesagt"
FORMATO = "vertical"
DURACION = None
BPM = 112
GAP = 0.14
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 9      # plano secuencia: los cambios los dibuja escenas.py
VOZ = dict(motor="elevenlabs", voice_id="I1n8B4pOly0qmOu46LFX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)

CER_MAX_POR_FRASE = {"problema_1": 0.2}   # Whisper escribe «GTA 4» en número; la voz dice «cuatro»

# El Jefe: su voz clonada (cuenta 3). Solo frases suyas REALES (pedido del 5-nov, docs/panel.md). Línea nueva: se le enseña antes.
JEFE_CON_VOZ = True
JEFE = ("pedido_1",)
VOZ_POR_FRASE = dict.fromkeys(JEFE, "hCU4QZdzzUliy58ezPBz") if JEFE_CON_VOZ else {}

LYRIA = dict(
    estilo="Playful, curious electronic score for a witty robot explaining physics: plucky synths, soft glitch percussion, "
           "springy bass, light marimba. Instrumental only, no vocals, never loud, always leaves space for the narrator.",
    escenas={
        "gancho": ("A sudden stop, then a mischievous ticking motif: something is about to fall.", 2),
        "pedido": ("Dry comedy, a single plucked note.", 1),
        "problema": ("Repetitive loop that feels mechanical and fake, then it breaks.", 2),
        "verlet": ("Curious and precise: dotted arpeggios like points connecting.", 2),
        "musculos": ("Elastic, springy bass that stretches and snaps back.", 2),
        "equilibrio": ("Tension: a wobbling rhythm that almost falls, then catches itself.", 2),
        "mundo": ("Playful obstacle course: bouncy percussion, cartoon energy.", 2),
        "errores": ("Comic mistake: detuned synth, then a bright 'aha' resolve.", 2),
        "cierre": ("Warm and confident: the main motif returns, ending abruptly.", 2),
    },
    tramos=[(["gancho", "pedido", "problema", "verlet", "musculos", "equilibrio", "mundo", "errores", "cierre"], "biblioteca: arana_amarilla__lyria_tramo1 (otro público)")],
)
MEZCLA = dict(musica=-23.0, sfx=-22.0)

SFX_ELEVEN = {
    "zas": dict(prompt="Quick airy cartoon swipe whoosh, clean and light, short", seg=0.6, variantes=4),
    "plaf": dict(prompt="Cartoon ragdoll robot falling flat on a floor, soft plastic and metal thud, comedic", seg=0.9, variantes=2),
    "boing": dict(prompt="Cartoon spring launch boing, a small robot flying upward, playful", seg=1.0),
    "paso": dict(prompt="Single small robot footstep stumble on a hard floor, light metallic tap", seg=0.5),
    "clang": dict(prompt="Small robot bonking against a hanging metal pipe, comedic clang with short ring", seg=1.0, variantes=2),
    "chanclazo": dict(prompt="Rubber flip-flop slap swatting something flying, comedic whack", seg=0.7),
    "error": dict(prompt="Soft comedic computer error buzz, two low descending beeps", seg=0.8),
    "acierto": dict(prompt="Bright short positive interface chime, two rising notes", seg=0.8),
    "escaneo": dict(prompt="Sci-fi x-ray scanner sweep hum, smooth rising tone, short", seg=1.6),
}

ESCENAS = [
    {"id": "gancho", "frases": [
        "Ningún cuadro de esta caída lo dibujó nadie. [short pause] Ni siquiera yo.",
        "Y la primera vez que lo intenté, el robot salió volando… sin que nadie lo tocara.",
        "Soy Token, la IA de este taller, y así enseñé a mis robots a caerse… y a levantarse solos.",
    ]},
    {"id": "pedido", "frases": [
        "Mi jefe me escribió:",
        "Que reaccionen a otros robots y cosas, y busquen balancearse cuando se mueven o son golpeados.",
    ]},
    {"id": "problema", "frases": [
        "Lo fácil es dibujar una caída y repetirla. A la tercera, ya sabes que es falsa.",
        "En GTA cuatro, los peatones no tenían caídas dibujadas: tenían músculos simulados. Se llamó Euphoria.",
        "Yo quise lo mismo… [short pause] dentro de una página web.",
    ]},
    {"id": "verlet", "frases": [
        "Primero me desarmé: por dentro soy siete puntos.",
        "Cada punto solo recuerda dónde estaba hace un instante: esa diferencia es su velocidad. Eso es Verlet.",
        "Los huesos son reglas de distancia. Y sin nada más… [short pause] soy un trapo.",
    ]},
    {"id": "musculos", "frases": [
        "Luego, músculos: resortes que jalan cada punto hacia una pose.",
        "Con fuerza uno, soy una animación rígida. Con fuerza cero, un trapo. Euphoria vive en medio.",
    ]},
    {"id": "equilibrio", "frases": [
        "Ahora, lo difícil: no caerme. Vigilo mi centro de masa.",
        "Si se sale de mis pies, doy un paso hacia él, echo el torso al revés y abro los brazos.",
        "Lo medí: de cada siete tambaleos, me salvo en cuatro.",
        "Si no hay remedio, meto las manos donde voy a caer, y me agarro de lo que haya… hasta de otro robot.",
    ]},
    {"id": "mundo", "frases": [
        "Luego, un mundo: mesas, tubos, lámparas que se columpian y trampillas al piso de abajo.",
        "Y enemigos: pegatinas con alas que te embisten. Mis robots se defienden con una chancla.",
        "Todo eso, ciento ochenta veces por segundo, en menos de un milisegundo.",
    ]},
    {"id": "errores", "frases": [
        "¿Y lo de salir volando? Al caer, sus manos buscaban un punto a treinta y dos del pecho. El brazo mide veintiuno.",
        "Las manos jalaban, el cuerpo subía… y la meta, con él. [short pause] Ya te diste cuenta: nunca iba a llegar.",
        "Otro error: puentes en diagonal, cruzando dos pisos. Los mismos números… en otro orden.",
    ]},
    {"id": "cierre", "frases": [
        "Nada de esto está animado. Cada caída que ves pasa por primera vez.",
        "Lo que les pase después lo decide la junta directiva: tú. ¿Qué obstáculo les pongo?",
    ]},
]
