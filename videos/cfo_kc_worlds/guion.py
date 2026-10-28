# -*- coding: utf-8 -*-
"""CFO vs KC (Worlds 2026, fase suiza, ronda 4, jue 29-oct-2026, 14:00 CDMX): previa para quien no conoce a los equipos,
~15 min, canal «Crónicas de ligoleyen» (subida por Studio; se publica el MISMO día del partido por la mañana → «hoy»).
Estilo ANÁLISIS TÁCTICO como videos/ig_lyon_worlds/ (docs/estilo_analisis_tactico.md), con MÁS flechas, la estrategia de
cada jugador, pausas, REPETICIONES y la RUTA de cada jugador en el mapa 3D (el usuario, 28-oct).

DATOS VERIFICADOS: investigacion/datos_cfo.md y datos_kc.md (API oficial, feed, Liquipedia, Wikipedia); narración de cada
jugada transcrita con Whisper large-v3 de los VOD (investigacion/j*_narr.txt; YouTube daba 429 a los subtítulos).
- Partido (API): match 115660540726095073, 2026-10-29T20:00Z = 14:00 CDMX, Bo3 Fearless; ambos 1-2: el perdedor queda
  eliminado (1-3); el ganador 2-2 → ronda 5 el sábado 31. CFO (LCP n.º 2) tiene la primera selección del juego 1 (LP).
  Mismo día: TES vs BLG 17:00 CDMX. Único cruce previo: First Stand 2025 (CFO 2-0 en grupos; KC 3-2 en semifinal).
- Jugadas (reloj = t del clip + N): j1 = TL-CFO (FATvv4Lk7IU desde 2470, +2000), j2 = triple de Rest (desde 2630),
  j3 = T1-CFO 24:33 (cmct78Iytg8 desde 2010, +1412), j3b = Doggo vs Doran (desde 1075, +477),
  j4 = KC-AL (8txB9yg9FNc desde 1750, +1422), j5 = C9-KC J4 (2xC2Jpk_duM desde 2640, +2131; VOD en español).
"""

TITULO = "CFO vs KC: todo lo que debes saber antes del partido | Worlds 2026 (análisis)"
ARCHIVO = "cfo_kc_worlds"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español), la voz de la Worlds y de IG-LYON
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
FONETICA = {
    "CTBC Flying Oyster": "Ci Ti Bi Ci Fláin Óister", "Flying Oyster": "Fláin Óister", "CTBC": "Ci Ti Bi Ci",
    "Karmine Corp": "Kármin Corp", "Karmine": "Kármin", "Kameto": "Kaméto", "Kotei": "Kotéi", "Blue Wall": "Blu Uól",
    "We are family": "Uí ar fámili", "family": "fámili", "Twitch": "Tuích", "EU Masters": "E U Másters",
    "Team Liquid": "Tim Lícuid", "Liquid": "Lícuid", "Anyone's Legend": "Éniuans Léyend", "Cloud9": "Claud náin",
    "Bilibili Gaming": "Bilibili Guéiming", "Movistar KOI": "Movistar Koi", "KOI": "Koi", "LYON": "Láion", "T1": "Ti uan",
    "Fearless Draft": "Fírles Draft", "Fearless": "Fírles", "Worlds": "Uórlds", "Play-In": "Pléi in", "First Stand": "Ferst Stand",
    "KDA": "ka de a", "Esports World Cup": "Ispórts Uórld Cop", "TES": "T E S", "BLG": "B L G",
    "Shad0w": "Shádou", "POUT": "Páut", "Doggo": "Dógo", "Kino": "Kíno", "Rest": "Rest",
    "Canna": "Kána", "Yike": "Yáik", "kyeahoo": "Kiéju", "Caliste": "Calíst", "Busio": "Búsio", "Reapered": "Ripérd",
    "Faker": "Féiker", "Keria": "Kéria", "Doran": "Dóran", "Peyz": "Péiz", "Oner": "Óner",
    "Josedeodo": "Josedeódo", "Quid": "Cuid", "CoreJJ": "Cor yei yei", "Morgan": "Mórgan", "Yeon": "Yon",
    "Tarzan": "Tárzan", "Kael": "Kéil", "Shanks": "Shanks", "Breathe": "Bríth", "Hope": "Jóup",
    "Tactical": "Táctical", "Vulcan": "Vúlcan", "Loki": "Lóki", "Blaber": "Bléiber",
    "Qiyana": "Kiána", "Rumble": "Rámbol", "Kai'Sa": "Káisa", "Xayah": "Záia", "Jax": "Yax", "Neeko": "Níko",
    "Lee Sin": "Li Sin", "Renata": "Renáta", "Alistar": "Alístar", "Viktor": "Víktor",
}

# Whisper oye mal los nombres («Carmen Corp», «Jake», «varón»): transcripciones leídas el 28-oct (la voz está bien);
# umbral = lo medido + margen. ElevenLabs termina en seco (cola alta sin cortar palabra).
CER_MAX_POR_FRASE = {"cfo_camino_2": 0.036, "cfo_historia_0": 0.04, "cfo_jugadores_0": 0.035, "cfo_jugadores_2": 0.063, "cierre_0": 0.044, "claves_1": 0.066, "claves_2": 0.084, "claves_3": 0.073, "claves_4": 0.063, "duelos_1": 0.053, "duelos_2": 0.036, "duelos_3": 0.041, "duelos_5": 0.039, "gancho_1": 0.041, "gancho_2": 0.038, "juego_1": 0.034, "jugada1_2": 0.051, "jugada1_3": 0.035, "jugada1_5": 0.056, "jugada1_6": 0.038, "jugada1_rep_0": 0.039, "jugada2_0": 0.037, "jugada2_5": 0.032, "jugada2_rep_0": 0.042, "jugada3_1": 0.114, "jugada3_2": 0.043, "jugada3_3": 0.048, "jugada3_4": 0.033, "jugada3_5": 0.134, "jugada3_rep_0": 0.04, "jugada4_0": 0.065, "jugada4_1": 0.093, "jugada4_2": 0.091, "jugada4_3": 0.095, "jugada4_4": 0.073, "jugada4_5": 0.057, "jugada4_rep_0": 0.048, "kc_camino_1": 0.064, "kc_camino_3": 0.049, "kc_camino_4": 0.045, "kc_historia_0": 0.088, "kc_historia_1": 0.054, "kc_jugadores_0": 0.05, "kc_jugadores_1": 0.048}
TAIL_MAX_POR_FRASE = {"cfo_camino_1": 1.1, "cfo_camino_2": 1.14, "cfo_jugadores_0": 1.02, "cierre_1": 1.15, "claves_2": 1.26, "gancho_2": 1.04, "juego_2": 1.07, "jugada1_0": 1.05, "jugada1_3": 1.11, "jugada1_rep_1": 1.1, "jugada2_0": 1.2, "jugada2_2": 1.04, "jugada3_5": 1.14, "jugada4_4": 1.13, "kc_camino_1": 1.4, "kc_historia_3": 1.09, "kc_jugadores_1": 1.14}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="fade",
    fundido=0.25,
    ambiente=0.0,
    # tramos EN VIVO de cada jugada (beat largo sin voz): bajan con el audio de la transmisión (se fija tras `beats`)
    ambiente_por={"scene-023": .85, "scene-041": .85, "scene-066": .85, "scene-080": .85},
    yt=dict(sufijo="League of Legends Worlds 2026", min_s=30, max_min=400, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern esports broadcast analysis score: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "stadium-sized hits and tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={
        "gancho": ("cold open, elimination-match tension, dramatic hit then driving pulse", 7),
        "juego": ("steady informative groove, stakes rising, do-or-die feeling", 4),
        "cfo_historia": ("East Asian pentatonic synth motif, proud and warm, championship memory", 5),
        "cfo_camino": ("comeback groove, determined", 5),
        "jugada1_rep": ("slow-motion replay, suspended, then a reflective resolve", 3),
        "jugada1": ("analysis bed: minimal pulse, ticking hi-hats, suspense, big hit near the end", 6),
        "cfo_jugadores": ("confident stat-card groove", 5),
        "jugada2_rep": ("slow-motion replay, suspended, then a reflective resolve", 3),
        "jugada2": ("analysis bed, uneasy tension, a sudden collapse", 6),
        "kc_historia": ("French stadium chant energy on synths, big drums, fan-wall hype", 7),
        "kc_camino": ("rising underdog anthem", 6),
        "jugada3_rep": ("slow-motion replay, suspended, then a reflective resolve", 3),
        "jugada3": ("analysis bed, tense, then an explosive triumphant swell", 7),
        "kc_jugadores": ("confident stat-card groove, brighter", 5),
        "jugada4_rep": ("slow-motion replay, suspended, then a reflective resolve", 3),
        "jugada4": ("analysis bed, do-or-die suspense, heroic climax", 8),
        "duelos": ("head-to-head versus groove, punchy hits", 6),
        "claves": ("tactical preview groove, focused", 5),
        "cierre": ("hype build-up toward match day, final big hit and ring out", 6),
    },
    tramos=[
        (["gancho", "juego"], "Begin with an impact hit, elimination-match tension, driving pulse, then settle under the explanation."),
        (["cfo_historia", "cfo_camino"], "A proud East Asian pentatonic synth motif, then a determined comeback groove."),
        (["jugada1", "jugada1_rep", "cfo_jugadores"], "Quiet minimal analysis pulse, a big hit near the middle, then a confident groove."),
        (["jugada2", "jugada2_rep"], "Uneasy analysis tension that suddenly collapses, then a sober afterglow."),
        (["kc_historia", "kc_camino"], "Stadium chant energy on synths with big drums, then a rising underdog anthem."),
        (["jugada3", "jugada3_rep", "kc_jugadores"], "Tense analysis bed exploding into a triumphant swell, then a bright confident groove."),
        (["jugada4", "jugada4_rep"], "Do-or-die suspense building to a heroic explosive climax, then a triumphant afterglow."),
        (["duelos", "claves", "cierre"], "Punchy head-to-head groove, then a focused preview, building hype to a final big hit and ring out."),
    ])
# Tramos EN VIVO (beat sin voz con el audio de la transmisión): la música baja 16 dB para que se oiga a los narradores.
_VIVOS = [(189.0, 207.25), (343.53, 361.16), (556.79, 572.79), (670.99, 686.25)]
MEZCLA = dict(musica_curva=[(0, 0)] + [p for a, b in _VIVOS for p in ((a, 0), (a + 1.5, -16), (b - 1.0, -16), (b + .5, 0))]
              + [(1000, 0)])

ESCENAS = [
    # ── GANCHO (~50 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "[excited] Hoy, a las dos de la tarde, uno de estos dos equipos se despide del Mundial.",
        "De un lado, CTBC Flying Oyster, de Taiwán: el equipo que el año pasado le ganó a T1… y ese T1 terminó campeón del mundo.",
        "Del otro, Karmine Corp: un club que fundaron dos streamers en Francia en 2020, que llena estadios… y que juega su primer Mundial.",
        "Y no es la primera vez que se ven. En 2025 cada uno le ganó una serie al otro. Hoy es el desempate… y el que pierda, se va a casa.",
        "[short pause] Si nunca los has visto jugar, en quince minutos te los presento: su historia, sus jugadores, cuatro jugadas analizadas pausa por pausa, con la ruta de cada jugador… y los cinco duelos que van a decidir el partido.",
    ]},
    # ── QUÉ ESTÁ EN JUEGO (~35 s) ──────────────────────────────────────────────────────────────────────────────────────
    {"id": "juego", "pre": 0.5, "frases": [
        "Primero, lo que está en juego. En la fase suiza del Mundial, con tres victorias pasas a cuartos de final; con tres derrotas, te vas.",
        "CFO y Karmine llegan con una victoria y dos derrotas. El que pierda hoy suma la tercera y queda eliminado. El que gane sigue vivo, dos y dos, y el sábado juega otra serie a muerte.",
        "La serie es al mejor de tres, con Fearless Draft: un campeón que ya se usó no se puede volver a elegir. Y CFO, por mejor sembrado, tiene la primera selección en la partida uno.",
    ]},
    # ── CFO: HISTORIA (~55 s) ──────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cfo_historia", "pre": 1.0, "frases": [
        "Empecemos por CTBC Flying Oyster. Su dueño es CTBC, un banco de Taiwán que también tiene equipos de béisbol y de básquetbol.",
        "Y el nombre tiene truco: en chino, «ostra voladora» suena casi igual que «family». Y el lema del banco es «We are family».",
        "El equipo nació en 2022, y de esa primera alineación solo queda uno: Rest, en la línea superior.",
        "Su gran año fue 2025. Ganó las tres etapas de la liga del Pacífico, en el MSI tuvo a T1 a una partida de caer… y en el Mundial le ganó a T1 y llegó a cuartos de final: el primer equipo de Asia-Pacífico en lograrlo en diez años.",
        "Y ese T1 al que le ganó… terminó campeón del mundo.",
    ]},
    # ── CFO: CAMINO (~50 s) ────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cfo_camino", "pre": 0.5, "frases": [
        "Pero 2026 empezó al revés. En las dos primeras etapas, CFO cayó en la primera ronda de los playoffs, y se quedó fuera del MSI.",
        "En abril cambió al medio y al soporte: llegaron el coreano POUT y Kino. Y con ellos el equipo revivió: subcampeón de la tercera etapa, y boleto al Mundial.",
        "Hoy juegan Rest arriba; Shad0w, un jungla italiano que pasó por Europa y por China; POUT en el medio; Kino de soporte; y el capitán y estrella, Doggo, el tirador.",
        "En Texas arrancó ganándole a Team Liquid. Después perdió con Movistar KOI y con T1.",
        "Y en esas partidas está todo lo que tienes que saber de CFO: cómo gana… y cómo pierde. Esta es la pelea que le dio su única victoria. Mírala primero tal como se vio en vivo.",
    ]},
    # ── JUGADA 1: el dragón ancestral contra Liquid (TL-CFO, 33:40-34:41) ─────────────────────────────────────────────
    {"id": "jugada1", "pre": 15.0, "frases": [
        "[short pause] Ahora, rebobinemos. Minuto treinta y cuatro. Liquid gana diez a cinco en asesinatos… pero CFO tiene cuatro dragones y el alma de montaña. Y aparece el dragón ancestral: el que lo tome, tiene la partida en la mano.",
        "Pausa. Mira a Shad0w, con Qiyana: rodeó el foso del dragón por detrás, y espera en la oscuridad. Su equipo, de frente; él, por la espalda.",
        "Liquid entra con CoreJJ, su soporte, para abrir la pelea… pero el combo no sale. Y Shad0w le cae por detrás. CoreJJ, fuera.",
        "Pausa otra vez. Cinco contra cuatro, y CFO empieza el dragón. Mira el reparto: Rest y Shad0w, dentro del foso, pegándole al ancestral. Doggo, Kino y POUT, de muro en la entrada.",
        "Josedeodo, el jungla de Liquid, espera a un lado para robar el dragón. Y el trabajo de Kino es uno solo: taparle el paso con el cuerpo y sacarlo del foso.",
        "[excited] Y lo hace: Kino lo levanta, Doggo le cae encima y Rest acaba con Josedeodo. Liquid se cobra a Shad0w… pero Quid llega tarde, y POUT lo borra.",
        "[excited] ¡El dragón ancestral es de CFO! Y medio minuto después, también el Barón.",
    ]},
    # ── REPETICIÓN de la jugada 1 (cámara lenta sin voz) + lección ──
    {"id": "jugada1_rep", "pre": 8.5, "frases": [
        "Mírala otra vez, con la ruta de cada jugador. Shad0w llegó antes que nadie al objetivo, puso su guardia de control… y desde ahí cazó a CoreJJ. Todo lo demás salió de esa posición.",
        "Esa es la lección de CFO: no gana por matar más. Iba perdiendo diez a cinco… y ganó con objetivos y posición. Dos minutos después, Rest, el veterano, cerraba la partida con un triple.",
    ]},
    # ── CFO: JUGADORES (~25 s) ─────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cfo_jugadores", "pre": 0.6, "frases": [
        "Los números de CFO en este Mundial: Doggo es el que más daño hace de su equipo, por mucho. Kino está en casi nueve de cada diez asesinatos, y Shad0w, en ocho de cada diez.",
        "Pero el problema de CFO está en otra columna: veinticinco asesinatos… y cuarenta y cuatro muertes en tres partidas.",
        "Y contra T1 se vio por qué.",
    ]},
    # ── JUGADA 2: el derrumbe ante T1 (T1-CFO, 24:33) + Doggo contra Doran ────────────────────────────────────────────
    {"id": "jugada2", "pre": 14.0, "frases": [
        "Rebobinemos. Primero, Doggo, con Kai'Sa, en el minuto ocho: Doran, el top de T1, sin Destello y sin visión… y Doggo lo caza. Un minuto después, otra vez.",
        "Minuto veinticuatro. CFO va dos mil de oro arriba, con cuatro torres. Los narradores decían que CFO estaba jugando increíblemente bien… y que T1 limpiaba la visión para forzar una pelea.",
        "Pausa. Aquí está la regla de oro de CFO: proteger a Doggo. Es el que más oro tiene, y T1 lo sabe: si lo atrapa, se acaba la pelea.",
        "Pausa otra vez. Mira el medio: Kino da un paso al frente, hacia Keria… y Doran viene por el flanco, sin que nadie lo vea.",
        "Keria conecta el primer control, Doran y Faker caen encima… y Doggo muere en el primer segundo.",
        "[excited] Sin su tirador, CFO se derrumba: cinco muertes en once segundos. T1 toma el Barón… y gana la partida.",
    ]},
    # ── REPETICIÓN de la jugada 2 + lección ──
    {"id": "jugada2_rep", "pre": 8.5, "frases": [
        "Esa es la grieta de CFO: cuando va ganando, a mitad de partida, pierde la pelea grande. Contra KOI le pasó igual: tomó el Barón… y perdió a cuatro jugadores en la pelea siguiente.",
    ]},
    # ── KC: HISTORIA (~55 s) ───────────────────────────────────────────────────────────────────────────────────────────
    {"id": "kc_historia", "pre": 1.0, "frases": [
        "Ahora, Karmine Corp. Y esta historia empieza en Twitch.",
        "En 2020, dos streamers, el francés Kameto y Kotei, fundaron un equipo para la liga francesa. Meses después pasó a llamarse Karmine Corp.",
        "Y se volvió un fenómeno. Ganó cuatro veces el EU Masters, la segunda división europea, más que nadie… y hasta el presidente de Francia, Emmanuel Macron, los felicitó.",
        "Su afición se llama el Blue Wall, y anima como en un estadio de fútbol. En 2023 y en 2024, sus eventos llenaron una arena de París con veintiocho mil personas.",
        "En 2025 se convirtió en el primer club francés en ganar la LEC, la liga europea. Y este año, por fin, llegó a su primer Mundial.",
    ]},
    # ── KC: CAMINO (~50 s) ─────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "kc_camino", "pre": 0.5, "frases": [
        "Su 2026 fue el año del casi: dos finales de la LEC perdidas tres a dos contra G2, la final de la Esports World Cup después de eliminar a T1… y en verano, nueve victorias sin derrota en la fase regular, para terminar terceros.",
        "La plantilla: Canna, coreano, excompañero de Faker en T1; Yike, el jungla sueco que ganó cuatro ligas con G2; kyeahoo en el medio; Busio, el soporte estadounidense; y la estrella: Caliste, francés, de veinte años, el MVP del verano.",
        "Al Mundial llegó por la puerta más estrecha, el Play-In. Perdió su primera partida uno a veinte contra Cloud9, estuvo dos veces a una derrota de quedar fuera… y remontó.",
        "Ya en Texas, en su primer partido, aplastó a Anyone's Legend, el número uno de China. Después perdió con LYON y con Bilibili Gaming.",
        "Y la pelea contra el número uno de China es la mejor carta de presentación de Karmine. Mírala en vivo.",
    ]},
    # ── JUGADA 3: el cuádruple de Canna (KC-AL, 24:44-24:59) ──────────────────────────────────────────────────────────
    {"id": "jugada3", "pre": 14.0, "frases": [
        "Rebobinemos. Minuto veinticuatro. Todo parejo: dos asesinatos contra uno, dos dragones por lado, y el oro casi empatado.",
        "Pausa. El objetivo de Karmine es Kael, el soporte de Anyone's Legend, con Neeko. Busio entra con Destello… pero no conecta.",
        "Yike, el jungla, se mete demasiado profundo… y cae primero. En ese momento, la pelea pinta para Anyone's Legend.",
        "Pausa. Pero mira la definitiva de Busio, con Renata: compra el tiempo justo. Y el combo de Yike, antes de caer, dejó a todos con poca vida.",
        "Y entonces Canna, con Jax, se mete hasta la retaguardia rival, donde están los que pegan de lejos.",
        "[excited] Tarzan… Kael… Shanks… kyeahoo atrapa a Breathe con su Onda de choque… ¡y cuádruple para Canna! Cinco por uno.",
    ]},
    # ── REPETICIÓN de la jugada 3 + lección ──
    {"id": "jugada3_rep", "pre": 8.5, "frases": [
        "La ruta de cada uno lo explica: Karmine perdió a su jungla en el primer segundo… y aun así ganó, porque cada uno siguió con su trabajo. Dos minutos después, el Barón; al final, la victoria.",
    ]},
    # ── KC: JUGADORES (~25 s) ──────────────────────────────────────────────────────────────────────────────────────────
    {"id": "kc_jugadores", "pre": 0.6, "frases": [
        "Los números de Karmine, sumando el Play-In: Caliste lleva sesenta asesinatos en catorce partidas, y el mejor KDA de su equipo.",
        "Busio está en siete de cada diez asesinatos. Y Yike ha jugado Lee Sin cinco veces: con Fearless, en cuanto lo saque, no lo podrá repetir.",
        "Pero a la estrella se le ve mejor en la partida más difícil de su año.",
    ]},
    # ── JUGADA 4: Caliste, ancestral y ace ante Cloud9 (Play-In, partida 4, 36:25-38:08) ──────────────────────────────
    {"id": "jugada4", "pre": 14.0, "frases": [
        "Play-In, cuarta partida contra Cloud9. Si Karmine pierde, se queda sin Mundial.",
        "Rebobinemos. Minuto treinta y seis. Karmine va casi ocho mil de oro arriba, con cuatro dragones y un Barón. Pero Cloud9 atrapa primero a kyeahoo y a Busio.",
        "Pausa. Con dos menos, cualquier error manda a Karmine a casa. Mira a Caliste, con Xayah: no huye. Se queda… y pelea.",
        "[excited] Caliste mata a Tactical… a Vulcan… Yike a Loki… y Caliste a Blaber. ¡Karmine gana la pelea con dos menos!",
        "Pausa. Con Cloud9 sin jugadores en pie, Karmine va directo al dragón ancestral… y lo toma.",
        "[excited] Y con el ancestral, a la base: Caliste borra a tres en tres segundos, Canna remata a Loki… ¡ace, y nexo! Karmine fuerza la quinta partida, y la gana.",
    ]},
    # ── REPETICIÓN de la jugada 4 + lección ──
    {"id": "jugada4_rep", "pre": 8.5, "frases": [
        "Caliste hizo seis asesinatos en el último minuto y cuarto. Esa es la amenaza de Karmine: si la pelea se alarga, su tirador la termina.",
    ]},
    # ── LOS CINCO DUELOS (~70 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "duelos", "pre": 0.6, "frases": [
        "Ahora, los cinco duelos de hoy, posición por posición.",
        "Arriba: Rest contra Canna. Rest es el veterano de CFO, y su arma de siempre es Rumble. Canna, el excompañero de Faker, fue el MVP contra el número uno de China.",
        "En la jungla: Shad0w contra Yike. Shad0w siempre busca el flanco y está en ocho de cada diez asesinatos de su equipo; Yike es el que abre las peleas de Karmine.",
        "En el medio: POUT contra kyeahoo. Los dos, coreanos, y los dos recién llegados: POUT a CFO en abril, y kyeahoo a Karmine en enero.",
        "Abajo, el duelo de estrellas: Doggo contra Caliste. El capitán que más daño hace en CFO… contra el francés de veinte años con sesenta asesinatos en el torneo.",
        "Y en soporte: Kino contra Busio. Kino, el que tiene que proteger a Doggo; Busio, el que engancha a los rivales para que entre todo Karmine.",
    ]},
    # ── CLAVES (~50 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "claves", "pre": 0.6, "frases": [
        "¿Y el partido de hoy? Tres claves para verlo como un experto.",
        "Uno: la pelea de mitad de partida. Los dos han tirado ventajas ahí: CFO contra T1 y contra KOI; Karmine contra LYON, cuando iba casi cinco mil de oro arriba en el minuto veintidós. El que no se tropiece en esa pelea, gana.",
        "Dos: los objetivos. CFO ganó su única partida con el alma y el ancestral; Karmine salvó su serie a muerte con el ancestral. Mira quién llega primero al dragón.",
        "Tres: Fearless. Rest con Rumble, Yike con Lee Sin: sus campeones favoritos solo se pueden usar una vez. El que gaste su mejor carta en la primera partida puede quedarse sin ella en la tercera.",
        "Y un dato: en el First Stand de 2025, CFO ganó dos a cero en grupos, y Karmine se vengó tres a dos en la semifinal. Hoy es el desempate.",
    ]},
    # ── CIERRE (~30 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.6, "frases": [
        "Así que prepárate: hoy, a las dos de la tarde, hora del centro de México, CTBC Flying Oyster contra Karmine Corp, al mejor de tres. Y a las cinco, TES contra BLG.",
        "[excited] ¿Tú con quién vas? ¿Con la ostra voladora de Taiwán… o con el muro azul de Francia? Déjalo en los comentarios. Nos vemos en el partido.",
    ]},
]
