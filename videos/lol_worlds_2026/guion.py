# -*- coding: utf-8 -*-
"""Worlds 2026 de League of Legends: TODO lo que ha pasado hasta el 27-oct-2026 (resumen de ~22 min, sin canal todavía).
Estilo ANÁLISIS TÁCTICO (docs/estilo_analisis_tactico.md): clips de los VOD completos con pausas, telestrador y tablero
3D (nucleo/mg_tactica.py) en 6 jugadas analizadas; el resto, resúmenes con clips. Prueba previa: videos/lol_worlds_tl_al/
(el Barón de Liquid = la jugada 6, condensada). Miniatura elegida: «EL FAVORITO CAYÓ» (miniatura/elegida.jpg).

DATOS VERIFICADOS (27-oct-2026). Fuentes en investigacion/: Wikipedia «2026 League of Legends World Championship»
(fechas, sedes, play-in, cruces de la ronda 4), GosuGamers (ronda 1: el LPL 0-4 por primera vez), resúmenes oficiales de
LoL Esports de los días 1-4 (subtítulos en investigacion/*.txt), descripciones de los VOD de EpicSkillshot (picks por
partida: investigacion/picks.txt) y gol.gg «Worlds 2026 Main Event» (investigacion/gol_*.csv; OJO: a 27-oct le faltan
partidas del día 4 de algunos equipos: los números se citan solo de DK y Gen.G, que están completos, o «en sus primeras»).
- Sedes: play-in en Los Ángeles (15-18 oct); suiza en Allen, Texas (23-31 oct); cuartos 3-6 nov y semis 7-8 nov en Allen;
  final el 14-nov en el Barclays Center (Nueva York). 19 equipos (15 directos + 1 del play-in = 16 en la suiza).
  Fearless Draft en todas las series al mejor de 3 y de 5. T1 = campeón 2023, 2024 y 2025 (seis títulos), va por el 4.º seguido.
- Play-in: KC 3-2 Cloud9 KIA; KC 3-0 MVK; FURIA 3-1 C9 KIA; MVK 3-1 FURIA; final KC 3-0 MVK. KC = 3.ª de la LEC, primer Mundial.
- Ronda 1 (23-oct, al mejor de 1): GEN>IG, HLE>TES, KOI>BLG, KC>AL, DK>G2 (remontada, 32 min), CFO>TLAW, T1>LOS (24 min,
  Faker LeBlanc), LYON>TSW (1.ª victoria de NA, en Allen). El LPL 0-4 en la ronda 1 por primera vez (GosuGamers).
  KC vs AL: Canna Jax, Yike Jarvan IV, kyeahoo Orianna, Caliste Kalista, Busio Renata · AL: Breathe Olaf, Tarzan Nocturne,
  Shanks Akali, Hope Miss Fortune, Kael Neeko. Pelea: definitiva de Renata + onda de choque + Cataclismo → cuádruple de
  Canna (narrador: «a one-four»), luego Barón y «el cuarto nexo del LPL en cuatro partidas».
- Ronda 2 (24-oct): TES>AL, KOI>CFO, G2>LOS (21-9, Lee Sin de SkewMond), LYON>KC, IG>TSW, GEN>HLE, DK>T1, BLG>TLAW.
  DK vs T1: DK Siwoo K'Sante, Lucid Jarvan IV, ShowMaker Viktor, Smash Kalista, Career Renata · T1 Doran Jayce, Oner Vi,
  Faker Anivia, Peyz Caitlyn, Keria Neeko. VERIFICADO con el VOD y los cuadros (27-oct): Oner mata a Lucid en el 37:08, pero
  la pelea del Anciano es en el 40:25 y Lucid está VIVO; T1 ya tenía el alma de Nube (VOD «cloud soul secured for T1») y
  +1,8K de oro; T1 tira el Anciano (12K), DK entra con los cinco: Career Destello + Definitiva de Kalista («pull out the
  Renata, Smash gets the knockup»), DK gana («from nothing they put T1 to ashes… a single team fight»), se queda con el
  Anciano («Blue team has slain the Elder Dragon», DK es azul) y la partida.
- Ronda 3 (25-26 oct): 2-0 al mejor de 3: DK 2-0 KOI (G1 pentakill de Smash con Kai'Sa: gancho de Nautilus de Career a la
  Anivia de jojopyun), GEN 2-1 LYON (G1 para LYON: Inspired con Xin Zhao al centro, cae Chovy). 1-1 al mejor de 1: IG>HLE
  (cuádruple de Rookie con Annie; MARCADOR 24:21: los 4 dragones y el alma del Infernal son de IG, +3,7K; Lulu de Meiko
  polimorfa al Olaf de Zeus), TES>G2, T1>CFO (pelea que atrapa a Doggo, 14-6 a los 27 min), BLG>KC. 0-2 al mejor de 3:
  LOS 2-0 TSW (dos remontadas), TLAW 2-0 AL (G1 Camille de Morgan; G2 = el Barón de la prueba).
  OJO: Wikipedia anota «Bo3, 2-1» en IG-HLE, TES-G2, T1-CFO y BLG-KC, pero fueron al mejor de 1 (un solo VOD y el resumen).
- Tras 3 rondas: 3-0 GEN y DK (en cuartos; DK el primero). 2-1 KOI, LYON, IG, TES, T1, BLG. 1-2 HLE, G2, CFO, KC, LOS, TLAW.
  0-3 TSW y AL (fuera). AL = campeón del LPL 2026 (3-1 a BLG, 13-sep; Sheep Esports) y primer sembrado de China.
- Ronda 4 (al mejor de 3): 28-oct KOI-T1 e IG-LYON; 29-oct KC-CFO y TES-BLG; 30-oct TLAW-LOS y HLE-G2. Ronda 5: 31-oct.
- gol.gg: Smash 4 partidas, 4 victorias, KDA 10,7, el único pentakill; ShowMaker 30 % del daño de DK, 1 muerte/partida;
  Canyon 5 partidas, KDA 10,5, 80 % de participación; Knight 89 % de participación y 35 % del daño de BLG (3 partidas);
  Gen.G +313 de oro por minuto (el mejor) y 80 % de los dragones. Lee Sin en 12 de las 29 partidas de la suiza.
"""

TITULO = "Worlds 2026: TODO lo que ha pasado | Las mejores jugadas, jugadores y equipos (análisis)"
ARCHIVO = "lol_worlds_2026"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español), la misma voz de la prueba: tono de analista deportivo
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
# Nombres en inglés como suenan (el usuario, 26-oct-2026: «Liquid» = «Lícuid»). Llega también a ElevenLabs; el .srt conserva
# la grafía real. Revisar oyendo la primera tanda y corregir aquí.
FONETICA = {
    "Team Liquid": "Tim Lícuid", "Liquid": "Lícuid", "Anyone's Legend": "Éniuans Léyend", "Gen.G": "Yen yi",
    "Dplus KIA": "Di plus Kía", "T1": "Ti uan", "G2": "Yi tu", "Karmine Corp": "Kármin Corp", "Cloud9 KIA": "Claud náin Kía",
    "Invictus Gaming": "Invíctus Guéiming", "Invictus": "Invíctus", "Bilibili Gaming": "Bilibili Guéiming",
    "Top Esports": "Top Ispórts", "Hanwha Life": "Janjua Laif", "Movistar KOI": "Movistar Koi", "KOI": "Koi",
    "LYON": "Láion", "Team Secret Whales": "Tim Sícret Uéils", "CTBC Flying Oyster": "Si Ti Bi Si Fláin Óister",
    "Worlds": "Uórlds", "Fearless Draft": "Fírles Draft", "Allen": "Álen", "Barclays Center": "Bárclis Center",
    "play-in": "pléi in", "pentakill": "péntakil", "KDA": "ka de a", "gol.gg": "gol punto gi gi",
    "Faker": "Féiker", "ShowMaker": "Chóumeiker", "Smash": "Smash", "Canyon": "Kéñon", "Chovy": "Chóvi", "Ruler": "Rúler",
    "Knight": "Náit", "Rookie": "Rúki", "TheShy": "De Shái", "Keria": "Kéria", "Oner": "Óner", "Peyz": "Péis",
    "Career": "Kárier", "Lucid": "Lúsid", "Siwoo": "Síu", "Canna": "Cána", "Busio": "Búsio", "Caliste": "Calíst",
    "Yike": "Yáik", "kyeahoo": "Kiajú", "Inspired": "Inspáierd", "Saint": "Séint", "Berserker": "Berserker",
    "SkewMond": "Skiúmond", "jojopyun": "Yoyopiún", "Supa": "Súpa", "Doggo": "Dógo", "Shadow": "Shádou",
    "Josedeodo": "Josedeodo", "Morgan": "Mórgan", "Yeon": "Yon", "CoreJJ": "Cor yei yei", "Breathe": "Brid",
    "Tarzan": "Tárzan", "Shanks": "Shanks", "Hope": "Jóup", "Viper": "Váiper", "Kai'Sa": "Káisa", "Lee Sin": "Li Sin",
    "Xin Zhao": "Shin Zháo", "Jax": "Yax", "Jinx": "Yinx", "K'Sante": "Kasánte", "Myrwn": "Mírwin", "Jayce": "Yéis", "Ambessa": "Ambésa",
}
# Whisper oye mal los nombres («Carmen Corp», «Genji», «Billy Billy», «varón»): transcripciones de las 49 frases revisadas el
# 27-oct (texto completo, sin cortes); umbral = lo medido + margen. ElevenLabs termina en seco (cola alta sin cortar palabra).
CER_MAX_POR_FRASE = {"jugada1_3": 0.04, "jugada2_3": 0.08, "jugada3_2": 0.045, "jugada3_3": 0.04, "jugada4_2": 0.08, "gancho_1": 0.045, "gancho_2": 0.015, "gancho_3": 0.015, "playin_1": 0.041, "playin_2": 0.04, "playin_3": 0.04, "dia1_1": 0.061, "dia1_2": 0.055, "jugada1_2": 0.094, "jugada1_4": 0.049, "jugada1_6": 0.038, "dia2_0": 0.044, "dia2_1": 0.064, "jugada2_0": 0.074, "jugada2_5": 0.027, "dia2b_0": 0.077, "dia2b_1": 0.054, "dia2b_2": 0.069, "dia2b_3": 0.098, "dia2b_5": 0.036, "jugada3_0": 0.05, "jugada3_1": 0.058, "dia3b_0": 0.076, "jugada4_0": 0.049, "jugada4_1": 0.105, "jugada4_3": 0.015, "jugada4_4": 0.057, "jugada5_0": 0.034, "dia4_2": 0.114, "dia4_3": 0.048, "dia4_4": 0.053, "dia4_5": 0.047, "jugada6_3": 0.075, "jugada6_4": 0.038, "meta_2": 0.047, "jugadores_0": 0.081, "jugadores_3": 0.047, "jugadores_6": 0.034, "equipos_1": 0.034, "equipos_2": 0.015, "equipos_6": 0.052, "queviene_1": 0.032, "queviene_2": 0.082, "queviene_4": 0.036, "lecciones_1": 0.052, "lecciones_2": 0.072, "lecciones_3": 0.076}
TAIL_MAX_POR_FRASE = {"gancho_1": 0.98, "gancho_2": 1.13, "gancho_3": 1.11, "playin_1": 0.72, "playin_2": 0.68, "playin_3": 0.91, "dia1_1": 0.76, "dia1_2": 0.93, "jugada1_2": 0.68, "jugada1_3": 0.9, "jugada1_4": 0.32, "jugada1_6": 0.5, "dia2_0": 1.0, "dia2_1": 0.78, "jugada2_0": 0.3, "jugada2_3": 1.1, "jugada2_5": 0.78, "dia2b_0": 0.57, "dia2b_1": 0.87, "dia2b_2": 0.83, "dia2b_3": 0.27, "dia2b_5": 0.93, "jugada3_0": 0.4, "jugada3_1": 0.95, "dia3b_0": 0.22, "jugada4_0": 0.33, "jugada4_1": 0.84, "jugada4_2": 0.78, "jugada4_3": 1.3, "jugada4_4": 0.83, "jugada5_0": 0.69, "dia4_2": 0.63, "dia4_3": 0.8, "dia4_4": 0.84, "dia4_5": 0.96, "jugada6_3": 0.52, "jugada6_4": 0.14, "meta_2": 0.89, "jugadores_0": 0.35, "jugadores_3": 0.78, "jugadores_6": 0.87, "equipos_1": 0.81, "equipos_2": 1.08, "equipos_6": 0.96, "queviene_1": 1.03, "queviene_2": 0.89, "queviene_4": 0.78, "lecciones_1": 1.04, "lecciones_2": 0.69, "lecciones_3": 0.79}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="fade",
    fundido=0.25,
    ambiente=0.0,
    # tramos EN VIVO de cada jugada (beat largo sin voz): bajan con el audio de la transmisión
    ambiente_por={"scene-026": .85, "scene-045": .85, "scene-065": .85, "scene-078": .85, "scene-090": .85, "scene-108": .85},
    yt=dict(sufijo="League of Legends Worlds 2026", min_s=30, max_min=400, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern esports broadcast analysis score: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "stadium-sized hits and tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={
        "gancho": ("cold open, dramatic hit then driving pulse, sense of shock", 7),
        "formato": ("steady informative groove, light arpeggios, building curiosity", 4),
        "playin": ("hopeful underdog groove, rising synths", 5),
        "dia1": ("ominous low drones, tension builds toward a fight", 6),
        "jugada1": ("analysis bed: minimal pulse, ticking hi-hats, suspense, big hit near the end", 6),
        "dia1b": ("upbeat recap groove", 5),
        "dia2": ("anticipation for a heavyweight clash, low brass synths", 6),
        "jugada2": ("analysis bed with rising tension and a triumphant swell at the comeback", 7),
        "dia2b": ("bouncy recap groove", 5),
        "dia3": ("high stakes build-up", 6),
        "jugada3": ("analysis bed, tension rising to an explosive climax", 8),
        "dia3b": ("surprise sting", 6),
        "jugada4": ("underdog anthem energy, heroic swell", 7),
        "dia3c": ("veteran mystique, slower groove", 5),
        "jugada5": ("analysis bed, cool confident pulse, climax", 7),
        "dia4": ("elimination day, darker serious drums", 6),
        "jugada6": ("analysis bed, patient tension, a final bittersweet hit", 7),
        "meta": ("light curious groove", 4),
        "jugadores": ("countdown energy, each step a little bigger", 6),
        "equipos": ("power ranking groove, confident", 5),
        "queviene": ("forward-looking anticipation, rising", 5),
        "lecciones": ("reflective, warm synth pads", 4),
        "cierre": ("final big hit and ring out", 5),
    },
    tramos=[
        (["gancho", "formato"], "Begin with an impact hit. Driving pulse, then settle under the explanation. End steady."),
        (["playin", "dia1"], "Continue the groove, turn darker and tense toward the end. End on a suspended note."),
        (["jugada1", "dia1b"], "Quiet minimal pulse for analysis, a big hit around the middle, then a lighter recap groove."),
        (["dia2", "jugada2"], "Anticipation, then analysis bed with rising tension and a triumphant swell near the end."),
        (["dia2b", "dia3", "jugada3"], "Recap groove, build stakes, analysis bed exploding into a climax at the end."),
        (["dia3b", "jugada4", "dia3c"], "Surprise sting, heroic underdog swell, then a slower cool groove."),
        (["jugada5", "dia4"], "Confident analysis pulse with a climax, then darker serious drums."),
        (["jugada6", "meta"], "Patient tension, a bittersweet final hit, then a light curious groove."),
        (["jugadores", "equipos"], "Countdown energy growing step by step, then a confident ranking groove."),
        (["queviene", "lecciones", "cierre"], "Forward-looking anticipation, warm reflective pads, final big hit and ring out."),
    ])
# Tramos EN VIVO (beat largo sin voz con el audio de la transmisión): la música baja 16 dB para que se oiga a los narradores.
# Calculado de beats.json el 27-oct (beats > 40 s); rehacer si cambia la línea de tiempo.
_VIVOS = [(209.7, 263.8), (377.4, 433.9), (549.2, 606.3), (656.8, 711.0), (759.5, 813.5), (918.7, 974.8)]
MEZCLA = dict(musica_curva=[(0, 0)] + [p for a, b in _VIVOS for p in ((a, 0), (a + 1.5, -16), (b - 1.0, -16), (b + .5, 0))]
              + [(1400, 0)])

# «pre» de 52 s en cada jugada: la jugada se ve PRIMERO en vivo con el audio de la transmisión (SECUENCIA["ambiente_por"]),
# y luego la voz rebobina y la analiza. Así el video llega a ~22 min (la voz sola son 15:26).
ESCENAS = [
    # ── GANCHO (~50 s) ────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "[excited] Llegaron a Texas como campeones de China… y se fueron sin ganar una sola partida.",
        "Anyone's Legend, el primer sembrado del LPL, eliminado cero a tres en la fase suiza del Mundial 2026. Y el último golpe se lo dio un equipo de Norteamérica.",
        "[short pause] Pero esa no fue la única sorpresa. En cuatro días vimos a China perder sus cuatro partidas del arranque, el primer pentakill del torneo, una remontada imposible contra T1… y a un equipo de Estados Unidos quitándole una partida al mejor de Corea.",
        "Si no has visto nada, tranquilo. En los próximos veinte minutos te pongo al día con todo: las mejores jugadas, analizadas pausa por pausa, los mejores jugadores, los mejores equipos… y lo que viene esta semana.",
    ]},
    # ── FORMATO (~80 s) ───────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "formato", "pre": 0.4, "frases": [
        "Primero, cómo funciona este Mundial, porque el formato lo explica casi todo.",
        "Son diecinueve equipos. Cuatro empezaron en Los Ángeles, en el play-in, y solo uno sobrevivió.",
        "Los otros dieciséis se juegan todo en la fase suiza, en Allen, Texas. La regla es simple: tres victorias y estás en cuartos de final. Tres derrotas y te vas a casa.",
        "En cada ronda te toca un rival con tu mismo récord. Las primeras rondas se juegan a una sola partida, sin margen de error… y cuando hay algo en juego, el pase o la eliminación, se juega al mejor de tres.",
        "Y hay una regla que lo cambia todo: el Fearless Draft. Dentro de una serie, un campeón que ya se usó no se puede volver a elegir. Nadie puede esconderse en sus favoritos.",
        "Ocho equipos pasan a cuartos. La final es el 14 de noviembre, en el Barclays Center de Nueva York.",
        "El lema de este año es «Este es nuestro momento», y el himno, Know My Name, de True Damage, viene con un video sobre la carrera de Faker.",
        "Y antes de empezar hubo un minuto de silencio por Cyanide, campeón del primer Mundial, en 2011, con Fnatic.",
        "[short pause] Y ahí quiere llegar T1, el campeón de 2023, 2024 y 2025, que va por algo que nadie ha hecho jamás: su cuarto título seguido.",
    ]},
    # ── PLAY-IN (~55 s) ───────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "playin", "pre": 0.4, "frases": [
        "Todo empezó el 15 de octubre en Los Ángeles.",
        "Karmine Corp, el tercer equipo de Europa, jugando el primer Mundial de su historia, casi se queda en la primera puerta: necesitó las cinco partidas para ganarle 3 a 2 a Cloud9 KIA.",
        "Después ya no soltó ni una. 3 a 0 a MVK… y otra vez 3 a 0 a MVK en la serie final por el boleto.",
        "Cloud9 KIA, FURIA y MVK se quedaron en el camino. [short pause] Y Karmine Corp viajó a Texas con un premio envenenado: estrenarse contra el campeón de China.",
    ]},
    # ── DÍA 1 (23-oct) ────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "dia1", "pre": 2.5, "frases": [
        "23 de octubre. Día uno de la fase suiza. Y China se despierta con una pesadilla.",
        "Gen.G le gana a Invictus Gaming. Hanwha Life le gana a Top Esports. Movistar KOI le gana a Bilibili Gaming en una partida apretadísima.",
        "Y Karmine Corp… aplasta a Anyone's Legend. Cuatro equipos chinos, cuatro derrotas. Nunca había pasado que el LPL no ganara ni una partida en la primera ronda.",
        "Y la pelea que lo resume todo está en esa última partida. Vamos a verla de cerca.",
    ]},
    {"id": "jugada1", "pre": 52.0, "post": 1.8, "frases": [
        "AL busca la pelea. Y tiene con qué: Olaf, Nocturne, Akali y Miss Fortune. Una composición hecha para entrar de frente.",
        "[short pause] Pausa. Mira a Busio. Juega Renata, y su definitiva hace algo cruel: los enemigos que toca… se atacan entre ellos.",
        "La ola de Renata cae encima de AL. Kyeahoo conecta la onda de choque de Orianna, Yike los encierra con la definitiva de Jarvan… y AL queda atrapado, peleándose consigo mismo.",
        "Ahí entra Canna. Con Jax, directo a la línea de atrás, donde están los que hacen el daño.",
        "[excited] ¡Cuádruple asesinato para Canna! Karmine Corp gana la pelea cuatro por uno.",
        "Después llega el Barón, la partida… y el cuarto nexo chino que cae en las cuatro primeras partidas de la fase suiza.",
        "[short pause] La lección: AL no perdió por falta de nivel. Perdió por pelear justo donde Karmine Corp lo estaba esperando.",
    ]},
    {"id": "dia1b", "pre": 0.4, "frases": [
        "Ese mismo día, CTBC Flying Oyster, de Taiwán, sorprende a Team Liquid con una gran partida de Shadow en la jungla.",
        "LYON le da a Norteamérica su primera victoria, y el estadio de Allen explota.",
        "T1 debuta con Faker en LeBlanc y despacha a Los Grandes, de Brasil, en veinticuatro minutos.",
        "Y Dplus KIA voltea una partida que iba perdiendo contra G2. [short pause] Guarda ese nombre: Dplus KIA. Va a aparecer mucho en este video.",
    ]},
    # ── DÍA 2 (24-oct) ────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "dia2", "pre": 2.5, "frases": [
        "24 de octubre. Día dos. Y el partido que todos marcaron en el calendario: Dplus KIA contra T1, los dos con una victoria.",
        "Durante buena parte de la partida, T1 parecía tener la medida de DK: Faker con Anivia controlando el centro, Peyz castigando desde lejos con Caitlyn.",
        "Hasta el dragón Anciano. Míralo primero en vivo.",
    ]},
    # post: las frases corregidas el 27-oct duran 1,2 s menos; con este margen la escena conserva sus 46 compases y nada se mueve
    {"id": "jugada2", "pre": 52.0, "post": 1.6, "frases": [
        "T1 ya tiene el alma de Nube, y empieza a tirar el Anciano.",
        "[short pause] Pausa. T1 va arriba en oro y tiene el alma. Si además termina el Anciano, con su bufo la partida prácticamente se acaba.",
        "DK tiene una sola salida: pelear. Ya. Antes de que caiga el dragón.",
        "Keria se lanza con Destello y la definitiva de Neeko sobre DK. Pero Smash usa la definitiva de Kalista para sacar a Career de ahí… y Career responde con la definitiva de Renata.",
        "[excited] ¡Y DK voltea la pelea entera! ¡De la nada, DK reduce a cenizas a T1… y se queda con el Anciano!",
        "Una pelea. Eso fue todo. DK se pone dos a cero… y T1, el tricampeón, conoce su primera derrota del Mundial.",
    ]},
    {"id": "dia2b", "pre": 0.4, "frases": [
        "Ese día también: Gen.G le gana a Hanwha Life en el clásico coreano, con Canyon imparable en la jungla.",
        "SkewMond firma una partida enorme con Lee Sin, y G2 aplasta a Los Grandes, veintiuno a nueve.",
        "Rookie y TheShy, los veteranos que hicieron campeón a Invictus en 2018, le ganan a Team Secret Whales.",
        "LYON vence a Karmine Corp, y Norteamérica se pone dos a cero.",
        "Y Anyone's Legend pierde otra vez, ahora contra Top Esports. El campeón de China ya está contra la pared: cero a dos.",
        "Así queda la tabla tras dos días. Con dos a cero: Gen.G, Dplus KIA, Movistar KOI… y LYON. Con cero a dos, a una derrota de irse: Anyone's Legend, Team Liquid, Los Grandes y Team Secret Whales.",
    ]},
    # ── DÍA 3 (25-oct) ────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "dia3", "pre": 2.5, "frases": [
        "25 de octubre. Día tres. Hoy se reparten los primeros boletos a cuartos: los que van dos a cero juegan al mejor de tres.",
        "Dplus KIA contra Movistar KOI. Y en la primera partida llega el momento del torneo hasta ahora.",
    ]},
    {"id": "jugada3", "pre": 52.0, "frases": [
        "KOI había llegado a ponerse a menos de mil de oro. Pero Jojopyun, con Anivia, da un paso de más.",
        "[short pause] Pausa. Mira la distancia: Jojopyun está adelantado, lejos de su equipo… y Career, con Nautilus, tiene el ancla lista.",
        "El ancla atrapa a la Anivia. Pero el primero en caer es el Jayce de Myrwn, y DK se mete hasta la línea de atrás de KOI.",
        "Ahora mira a Smash, con Kai'Sa. Entra a la pelea… y Supa cae. El Agotamiento que le lanzan no sirve de nada.",
        "[excited] ¡Triple! ¡Cuádruple! ¡Y pentakill para Smash!",
        "El primer y único pentakill del Mundial hasta ahora. DK gana la serie dos a cero y se convierte en el primer equipo clasificado a cuartos.",
    ]},
    {"id": "dia3b", "pre": 0.4, "frases": [
        "Y en la otra serie… LYON le hace a Gen.G lo que nadie esperaba.",
    ]},
    {"id": "jugada4", "pre": 52.0, "frases": [
        "Primera partida. El plan de Gen.G es acumular dragones.",
        "[short pause] Pausa. En el minuto veinte, LYON le gana el Barón a Gen.G. Pero la pelea que decide la partida llega catorce minutos después. Mira a Inspired, con Xin Zhao.",
        "Inspired se mete con Xin Zhao al centro del equipo coreano, sin dudar.",
        "[excited] ¡Chovy cae! ¡Y LYON gana la pelea! El estadio de Texas no lo puede creer: Norteamérica le gana una partida al primer sembrado de Corea.",
        "[short pause] Pero Gen.G es Gen.G. Ajusta, gana la segunda y la tercera, y se clasifica tres a cero. LYON cae, pero con la cabeza en alto.",
    ]},
    {"id": "dia3c", "pre": 0.4, "frases": [
        "Los que iban uno a uno se jugaron todo a una sola partida. Y ahí apareció un viejo conocido.",
    ]},
    {"id": "jugada5", "pre": 52.0, "post": 2.6, "frases": [
        "Invictus contra Hanwha Life. Invictus va arriba en oro y acaba de llevarse el alma del dragón Infernal… pero Hanwha sigue viva.",
        "[short pause] Pausa. Mira dónde está Rookie: con Annie, detrás de su equipo.",
        "Gumayusi se queda sin salida. Rookie lo remata. Y en el tres contra tres que queda, la transformación de Lulu deja a Olaf sin poder hacer nada.",
        "[excited] ¡Triple para Rookie… y cuádruple!",
        "Invictus gana. El equipo que perdió el primer día ahora va dos a uno, a una serie de cuartos. Y Top Esports también gana, contra G2.",
    ]},
    # ── DÍA 4 (26-oct) ────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "dia4", "pre": 2.5, "frases": [
        "26 de octubre. Día cuatro. El más cruel, porque los que van cero a dos se juegan la vida.",
        "Primero, T1. Contra CTBC arma la pelea perfecta: atrapa a Doggo, el tirador que estaba cargando a su equipo, y no deja a nadie de pie. Partida terminada en veintisiete minutos.",
        "Bilibili, con Knight en gran forma, le gana a Karmine Corp con una pelea de cinco por cero.",
        "Los Grandes remonta otra vez, ahora contra Team Secret Whales. Dos a cero, y los de Vietnam se van a casa sin ganar.",
        "Y la última serie del día… es la que le da título a este video. Team Liquid contra Anyone's Legend. Los dos, cero a dos. El que pierda, se va.",
        "Recuerda quién es AL: en septiembre ganó la liga china, 3 a 1 a Bilibili en la final. En la transmisión llamaron a Tarzan, su jungla, uno de los mejores del mundo. Nadie los veía cayendo aquí.",
        "Liquid gana la primera con una Camille de Morgan que se come la línea de atrás de AL. Y en la segunda, llega el Barón que lo decide todo.",
    ]},
    {"id": "jugada6", "pre": 52.0, "frases": [
        "Minuto 40. Liquid pierde en asesinatos, 11 a 17… pero va arriba en oro y en torres.",
        "Toma el tercer dragón y le quita a AL el alma. [short pause] Pausa. Mira arriba: una oleada de Liquid empuja sola hacia el inhibidor, y Morgan se teletransporta para presionar.",
        "AL tiene que soltar el dragón y volver a su base. Intenta encerrar a Liquid por un flanco… pero Liquid se retira a tiempo, y AL se queda a oscuras.",
        "Liquid empieza el Barón. Y Hope dispara el cohete de Jinx buscando el robo…",
        "[excited] ¡Pero Josedeodo no falla el castigo! ¡Barón para Liquid!",
        "Minutos después, Liquid termina la partida. [short pause] Anyone's Legend, campeón de China, se despide cero a tres. Sin ganar una sola partida.",
        "[short pause] El favorito cayó.",
    ]},
    # ── EL META (~60 s) ───────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "meta", "pre": 0.5, "frases": [
        "Antes de los nombres, un dato del juego. Con el Fearless Draft, los equipos no pueden repetir campeones en una serie… y aun así, hay uno que nadie suelta.",
        "Lee Sin apareció en doce de las veintinueve partidas de la fase suiza. Detrás vienen Orianna, Renata, Alistar y Nocturne, con diez cada uno.",
        "Y fíjate en Renata: estuvo en las dos peleas que acabamos de ver, la de Karmine Corp y la de DK. Este Mundial se está ganando con peleas en equipo, no con duelos.",
    ]},
    # ── MEJORES JUGADORES (~2:30) ─────────────────────────────────────────────────────────────────────────────────────
    {"id": "jugadores", "pre": 0.6, "frases": [
        "Ahora sí. Los cinco jugadores que más han brillado, con los números de gol.gg.",
        "Número cinco: Knight, de Bilibili. En sus primeras tres partidas participó en casi nueve de cada diez asesinatos de su equipo, y hace más del treinta por ciento de su daño. Si Bilibili llega lejos, será por él.",
        "Número cuatro: Rookie, de Invictus. Ocho años después de ser campeón del mundo, sigue decidiendo partidas. Su cuádruple con Annie sacó a Invictus del hoyo.",
        "Número tres: Canyon, de Gen.G. Cinco partidas, un KDA de 10,5, y presente en ocho de cada diez asesinatos de su equipo. Gen.G pelea donde Canyon decide.",
        "Número dos: ShowMaker, de DK. El veterano sigue siendo el cerebro: hace el treinta por ciento del daño de su equipo y muere, en promedio, una vez por partida.",
        "[short pause] Y número uno: Smash. Cuatro partidas, cuatro victorias, un KDA de 10,7… y el único pentakill del torneo. Es el tirador del momento.",
        "Menciones honoríficas: Keria y Faker, que tienen a T1 a una serie de cuartos, y SkewMond, que con Lee Sin hizo la mejor partida de G2.",
    ]},
    # ── MEJORES EQUIPOS (~2 min) ──────────────────────────────────────────────────────────────────────────────────────
    {"id": "equipos", "pre": 0.6, "frases": [
        "¿Y los equipos? Este es mi ranking después de cuatro días.",
        "Primero, Gen.G. Tres a cero, la mejor diferencia de oro por minuto del torneo, y el dueño de los dragones: se llevó ocho de cada diez. Perdió una partida contra LYON… y la convirtió en una lección.",
        "Segundo, Dplus KIA. Tres a cero sin perder una sola partida: cuatro de cuatro. Remontó contra G2, le ganó a T1 con una sola pelea y tiene al tirador más en forma del Mundial.",
        "Tercero, T1. Solo ha perdido contra DK, y el tricampeón sabe ganar cuando importa. Pero en la ronda cuatro se juega el pase.",
        "Cuarto, Invictus Gaming. Empezó perdiendo y ganó dos seguidas, con Rookie y TheShy jugando como en 2018.",
        "Y la sorpresa: LYON. Dos victorias y una partida robada a Gen.G. Norteamérica no se veía así de bien en mucho tiempo.",
        "¿China? Tres equipos siguen vivos con dos a uno: Invictus, Top Esports y Bilibili. Pero el campeón ya no está. Y Europa: Movistar KOI respira con dos a uno, mientras G2 y Karmine Corp están contra la pared.",
    ]},
    # ── LO QUE VIENE (~90 s) ──────────────────────────────────────────────────────────────────────────────────────────
    {"id": "queviene", "pre": 0.6, "frases": [
        "¿Qué viene? El 28 de octubre arranca la ronda cuatro, todo al mejor de tres.",
        "Los que van dos a uno juegan por el pase a cuartos: Movistar KOI contra T1, Invictus contra LYON, y Top Esports contra Bilibili, en un duelo chino.",
        "Los que van uno a dos juegan por no irse a casa: Karmine Corp contra CTBC, Team Liquid contra Los Grandes, y Hanwha Life contra G2.",
        "La ronda cinco es el 31 de octubre, y ahí sabremos los ocho de cuartos. Cuartos del 3 al 6 de noviembre, semifinales el 7 y el 8 en Texas… y la final, el 14, en Nueva York.",
        "[short pause] Si tienes que ver una sola serie, que sea T1 contra KOI. Si T1 cae, su camino al cuarto título se complica. Y Hanwha Life, uno de los gigantes de Corea, podría irse en la fase suiza.",
    ]},
    # ── LO QUE APRENDIMOS (~50 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "lecciones", "pre": 0.6, "frases": [
        "Tres cosas que nos dejan estos cuatro días.",
        "Una: Corea manda. Gen.G y DK son los únicos invictos, y T1 sigue vivo.",
        "Dos: China está en crisis. Perdió sus cuatro partidas del primer día y a su campeón, aunque todavía le quedan tres equipos con vida.",
        "Y tres: Occidente llegó con hambre. LYON le quitó una partida a Gen.G, Movistar KOI le ganó a Bilibili, y Team Liquid eliminó al campeón de China.",
    ]},
    # ── CIERRE (~30 s) ────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.5, "frases": [
        "Así va el Mundial. El campeón de China, fuera. Corea, con dos equipos invictos. Y T1, a una serie de seguir soñando.",
        "¿Quién crees que levanta la Copa del Invocador en Nueva York? Déjamelo en los comentarios… y nos vemos en cuartos.",
    ]},
]
