# -*- coding: utf-8 -*-
"""El asteroide que no vimos venir — Kuriox, 16:9, ~5 min, TERROR.

Pedido del usuario (20-oct-2026): video de Kuriox con su estilo (Kurzgesagt del espacio) FUSIONADO con el estilo nuevo «pegatina Flow»
de `videos/jalpa/` (Flow pinta escenarios y hojas; el código los anima como pegatinas). Hipótesis: qué pasaría si un asteroide que hoy
no podemos detectar cae en la Tierra; el escenario más catastrófico REALISTA, desde varias perspectivas (la astrónoma que lo ve, las
agencias que no pueden hacer nada y una persona normal). Tono de TERROR: incómodo, que dé miedo de verdad. ~5 min.
Decisiones (20-oct-2026): 4 sesiones · vista previa del primer minuto con audio completo · voz ElevenLabs con corchetes · SIN Kuri.

Datos y fuentes (verificar 2.ª fuente en el cierre):
  - ~25 000 asteroides cercanos > 140 m; descubiertos ~40-45 % (NASA, dashboard dic-2025: 11 343 hallados, ~14 000 por hallar;
    Kelly Fast, feb-2026: «about 40 %»). Guion: «menos de la mitad».
  - 2019 OK: 57-130 m (~100 m), descubierto ~1 día antes, pasó a ~73 000 km (≈ 1/5 de la distancia a la Luna) el 25-jul-2019 (Wikipedia).
  - Punto ciego: los telescopios en tierra solo ven de noche → lo que llega desde el lado del Sol no se ve (Chelyabinsk). NEO Surveyor
    (infrarrojo, en L1, mira cerca del Sol): lanzamiento PREVISTO sept-2027 (Wikipedia; Universe Today). Guion: «está previsto».
  - Chelyabinsk 15-feb-2013: ~20 m, ~500 kt, llegó desde la dirección del Sol, sin detectar; la gente fue a las ventanas tras el destello;
    la onda llegó minutos después; ~1 500 heridos, casi todos por vidrios.
  - DART: lanzada 24-nov-2021, impacto en Dimorphos 26-sep-2022 = 10 meses; única desviación hecha.
  - Objeto en curso de colisión: casi no cambia de posición contra las estrellas (rumbo constante), solo aumenta de brillo.
  - Escenario (cálculo propio con las fórmulas de Collins, Melosh y Marcus 2005 = «Impact: Earth!»): roca de 400 m, 3 000 kg/m³,
    20 km/s, 45° → ≈ 2·10¹⁹ J ≈ 4 800 Mt («unos 5 mil megatones», ~100 Bombas del Zar de 50 Mt); cráter final ≈ 7 km; magnitud
    sísmica ≈ 7,1; destrucción total (≈ 30 psi) a 30 km; a 90 km: ~3,5 psi (ventanas, techos, árboles; viento de huracán),
    ~1,2 MJ/m² de calor (quemaduras de 2.º grado al aire libre), sismo a ~15 s, onda a ~265 s ≈ 4,5 min.
  - Cometa C/2013 A1 Siding Spring: descubierto el 3-ene-2013, pasó a ~140 000 km de Marte el 19-oct-2014 (< 2 años de aviso).
  - NO se afirma: ciudad concreta, fecha, cifra de muertos (solo «millones si cae cerca de una gran ciudad»). Es una HIPÓTESIS y el
    guion lo dice («Esto no está pasando. Todavía.»).
"""

TITULO = "El asteroide que NO vimos venir"
ARCHIVO = "asteroide_invisible"
ESTILO_VISUAL = "pegatina_flow"      # fusión: pegatinas de Flow en look Kurzgesagt (FICHA) + motion graphics de Kuriox por código
DURACION = None
BPM = 70
GAP = 0.35
# ElevenLabs con corchetes de actuación (docs/voz.md). Escritura normal: cifras, sin fonética.
# 20-oct-2026: el usuario descartó BRAULIO (dQafQNlqLLJDepKplzjl; su voz quedó en voz_braulio/) y eligió esta voz de la biblioteca
# pública entre 11 muestras (previews/muestras_voz/11_*.mp3).
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-21.0, sfx=-22.0)
SUBTITULOS = False
ALIAS_QA = {"chelyabinsk": "cheliabinsk", "cheliabinks": "cheliabinsk", "chelyabinks": "cheliabinsk", "megatonnes": "megatones"}
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "[whispers] Esto no está pasando. [long pause] Todavía.",
        "[serious] Ahora mismo, miles de rocas capaces de borrar una ciudad entera cruzan cerca de la Tierra.",
        "[short pause] Y lo peor: no sabemos dónde están.",
        "Hoy vamos a imaginar qué pasaría si una de ellas viniera hacia nosotros. [short pause] Y la viéramos demasiado tarde.",
    ]},
    {"id": "ciegos", "frases": [
        "Se calcula que hay unos 25 mil asteroides cercanos de más de 140 metros. [short pause] El tamaño justo para destruir una ciudad.",
        "[serious] Hemos encontrado menos de la mitad.",
        "En 2019, uno de unos 100 metros pasó a una quinta parte de la distancia a la Luna. [short pause] Lo descubrieron un día antes.",
        "Y hay una parte del cielo que nunca podemos vigilar. [whispers] La que está junto al Sol.",
        "Nuestros telescopios solo miran de noche. Todo lo que viene desde el lado del Sol llega a ciegas.",
    ]},
    {"id": "cheliabinsk", "frases": [
        "En 2013, una roca de 20 metros salió del resplandor del Sol sobre Cheliábinsk, en Rusia. Nadie la vio venir.",
        "La gente vio el destello y corrió a las ventanas a mirar.",
        "[short pause] Minutos después llegó la onda expansiva. Más de mil heridos, casi todos por vidrios rotos.",
        "[sighs] Era una roca de 20 metros. [long pause] Ahora imagina una de 400.",
    ]},
    {"id": "punto", "frases": [
        "Una tarde cualquiera, en un observatorio de Chile, una astrónoma revisa las imágenes del atardecer, muy cerca del horizonte.",
        "Hay un punto que ayer no estaba.",
        "[nervous] Y hay algo que la inquieta: casi no se mueve.",
        "Las rocas que pasan de largo cruzan el cielo. [whispers] La que viene directo hacia ti se queda quieta. [short pause] Y solo crece.",
        "Mide unos 400 metros. [long pause] Faltan 20 horas.",
    ]},
    {"id": "numeros", "frases": [
        "La probabilidad de impacto sube cada hora. 1 por ciento. 10. 60.",
        "[short pause] 100 por ciento.",
        "[serious] Y no hay nada que lanzar. La única vez que desviamos un asteroide, la nave tardó 10 meses en llegar.",
        "Una roca de 400 metros a 20 kilómetros por segundo libera unos 5 mil megatones.",
        "[short pause] Cien veces la bomba más grande que hemos detonado jamás.",
    ]},
    {"id": "alerta", "frases": [
        "Son las 4 de la mañana cuando tu teléfono empieza a sonar como nunca lo habías oído.",
        "[whispers] Alerta de impacto. Aléjese de las ventanas. Busque refugio.",
        "Vives a 90 kilómetros del punto. [short pause] Lo bastante lejos para sobrevivir. Lo bastante cerca para verlo todo.",
        "[nervous] Las carreteras se llenan en minutos. Nadie sabe hacia dónde huir. Ni qué tan lejos es lejos.",
        "Y a las 12 del día, [short pause] el cielo se rompe.",
    ]},
    {"id": "destello", "frases": [
        "[whispers] Primero no hay ruido.",
        "La roca cruza la atmósfera en unos segundos, y aparece un segundo sol, más brillante que el de verdad.",
        "El calor te llega a la piel a través del vidrio. Afuera, la ropa tendida empieza a humear.",
        "A los 15 segundos, el suelo se sacude. Un terremoto de magnitud 7.",
        "Y luego, [long pause] nada.",
    ]},
    {"id": "silencio", "frases": [
        "[whispers] Este es el peor momento.",
        "El cielo está en calma, el temblor ya pasó, y la gente sale a mirar.",
        "Nadie entiende que lo peor todavía viene en camino, a la velocidad del sonido.",
        "[long pause] Cuatro minutos y medio de silencio.",
        "[short pause] Y entonces llega. La onda revienta todas las ventanas, arranca los techos y tumba los árboles, con un viento de huracán.",
    ]},
    {"id": "zona_cero", "frases": [
        "Donde cayó, ya no queda nada que salvar.",
        "Un cráter de unos 7 kilómetros. Todo lo que había a 30 kilómetros a la redonda desapareció.",
        "Una columna de polvo y fuego sube más alto que los aviones, y las rocas que salieron volando caen encendidas sobre los incendios.",
        "Cerca de una gran ciudad, serían millones de personas. [sighs] En menos de cinco minutos.",
        "[whispers] No es el fin del mundo. [short pause] Es el fin de tu mundo.",
    ]},
    {"id": "peor", "frases": [
        "[serious] Y esto es lo que sí sabemos buscar.",
        "Hay cuerpos que no aparecen en ninguna lista: cometas que caen desde los confines del sistema solar, más rápidos y más grandes.",
        "En 2013 descubrimos uno que iba a pasar rozando Marte. [short pause] Lo vimos menos de dos años antes.",
        "[whispers] Contra algo así, dos años no alcanzan para nada.",
    ]},
    {"id": "cierre", "post": 2.5, "frases": [
        "Está previsto que en 2027 despegue un telescopio espacial hecho para mirar hacia el Sol, justo donde hoy estamos ciegos.",
        "Hasta entonces, seguimos vigilando el cielo de noche, [short pause] y esperando que lo que venga, venga por el lado oscuro.",
        "[whispers] La próxima vez que veas un atardecer, recuérdalo. [long pause] De ahí vienen las que no vemos.",
    ]},
]

TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Cinematic space horror score for an animated science documentary about an undetected asteroid impact: deep sub-bass drones, "
            "dissonant low strings, sparse detuned piano notes, metallic scrapes, distant reversed choir, slow heartbeat-like pulses. "
            "Cold, uneasy, claustrophobic; long silences; melodies kept low so a narrator can whisper over it. No drums kit, no pop."),
    escenas={
        "gancho": ("Cold open: near silence, a single detuned piano note, a low drone creeping in.", 6),
        "ciegos": ("Vast dark space: shimmering high strings over a deep drone, a sense of something unseen out there.", 5),
        "cheliabinsk": ("Winter morning memory: a fragile music-box-like motif, then a sudden low boom and ringing silence.", 7),
        "punto": ("Discovery at an observatory: ticking pulse, tense sustained strings rising very slowly, dread.", 7),
        "numeros": ("Alarm and helplessness: pulsing low synth heartbeat speeding up, dissonant brass-like swells, cut to silence.", 8),
        "alerta": ("Panic at dawn: anxious tremolo strings, distant siren-like glissandi, fast heartbeat pulse.", 8),
        "destello": ("The flash: everything drops to a high ringing tone, then a deep rumbling quake, then dead silence.", 9),
        "silencio": ("Suspended silence: barely audible breathing drone and a slow clock-like tick building unbearably, then a huge impact hit.", 10),
        "zona_cero": ("Aftermath: mournful low choir and cello over burning ambience, grief, enormous scale.", 7),
        "peor": ("Deeper cosmic dread: icy high harmonics, slow descending bass, colder than before.", 7),
        "cierre": ("Ending: lonely detuned piano over a fading drone, unresolved, ends on an uneasy held note into silence.", 5),
    },
    tramos=[
        (["gancho", "ciegos", "cheliabinsk", "punto", "numeros"],
         "Begin from total silence. Slowly build dread; end the section on a held, unresolved dissonance."),
        (["alerta", "destello", "silencio"],
         "Begin from a tense pulse. The flash drops to a ringing tone and silence; a slow ticking build; end on a massive hit when the blast arrives."),
        (["zona_cero", "peor", "cierre"],
         "Begin from the ringing aftermath of a huge blast. Mournful and enormous, then colder; end unresolved, fading to silence."),
    ],
)

# Ficha común de Flow: la FUSIÓN = look de explicador espacial tipo Kurzgesagt (formas geométricas limpias, degradados, brillos)
# pintado como lámina de recorte para animar en pegatinas; atmósfera de terror (fría, oscura, luz enferma, acento rojo-naranja).
FICHA = dict(
    estilo=("Flat 2D vector illustration in the style of a science explainer animation (Kurzgesagt-inspired): clean geometric shapes, "
            "very thin dark outlines, smooth soft gradients, glowing rim lights and luminous highlights, subtle grain; cinematic HORROR "
            "mood: dark, cold and ominous, deep navy, indigo and desaturated teal palette with a single burning orange-red accent, "
            "long shadows, eerie atmosphere, strong depth"),
    cierre=" No text, no letters, no numbers, no watermark.",
)
