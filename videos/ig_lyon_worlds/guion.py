# -*- coding: utf-8 -*-
"""IG vs LYON (Worlds 2026, fase suiza, ronda 4, 28-oct-2026): presentación de los dos equipos para quien no los conoce,
~12 min, canal «Crónicas de ligoleyen» (subida por Studio; se publica el 28-oct a las 10:00, hora del centro de México).
Estilo ANÁLISIS TÁCTICO (docs/estilo_analisis_tactico.md) como videos/lol_worlds_2026/, con MÁS PAUSAS por jugada (el usuario,
27-oct: «agrega más pausas durante los enfrentamientos para entender posicionamiento, estrategia… más líneas, rutas, flechas»).

DATOS VERIFICADOS: investigacion/datos.md (cada dato con su URL: API oficial de LoL Esports, Liquipedia, Wikipedia).
- Horario 28-oct (API oficial): Movistar KOI vs T1 20:00 UTC = 14:00 centro de México; LYON vs IG 23:00 UTC = 17:00 CDMX
  (puede adelantarse si T1-KOI acaba pronto: el 25-oct LYON-GEN empezó 68 min antes de su hora).
- 2-1 vs 2-1, al mejor de 3 con Fearless: el ganador 3-1 → cuartos; el perdedor 2-2 → ronda 5 el sábado 31-oct.
  LYON (LCS n.º 2) tiene el derecho de primera selección en la partida 1 frente a IG (LPL n.º 4). Sin enfrentamientos
  oficiales previos registrados (API: Worlds 2023-2026 y MSI 2024-2026).
- Jugadas: muertes y relojes del feed oficial (feed.lolesports.com/livestats/v1/window/<gameId>), verificadas en el VOD
  (cuadros + narración transcrita con Whisper, investigacion/*_narr.txt):
  j1 = IG-HLE (rxkYf8BOHSQ, VOD = reloj + 463 s), j2 = TSW-IG (mva8OALSadc, + 446), j3 = LYON-TSW (feWyEjzJmKc, + 399),
  j4 = LYON-GEN partida 1 (zNTyYcB20Mg, + 421 al inicio).
"""

TITULO = "IG vs LYON: todo lo que debes saber antes del partido | Worlds 2026 (análisis)"
ARCHIVO = "ig_lyon_worlds"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español), la voz del video de la Worlds (el usuario, 27-oct: «igual que Worlds»)
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
FONETICA = {
    "Invictus Gaming": "Invíctus Guéiming", "Invictus": "Invíctus", "Team Secret Whales": "Tim Sícret Uéils",
    "Secret Whales": "Sícret Uéils", "Hanwha Life": "Janjua Laif", "Gen.G": "Yen yi", "Movistar KOI": "Movistar Koi",
    "Top Esports": "Top Ispórts", "JD Gaming": "Yei Di Guéiming", "Karmine Corp": "Kármin Corp", "Cloud9": "Claud náin",
    "Team Liquid": "Tim Lícuid", "Fnatic": "Fnátic", "Evil Geniuses": "Ivil Yínius", "FlyQuest": "Fláicuest",
    "Six Karma": "Six Karma", "Rainbow7": "Réinbou Seven", "LYON": "Láion", "Lyon Gaming": "Láion Guéiming",
    "T1": "Ti uan", "EDG": "I di yi", "Lock-In": "Lók in", "Fearless Draft": "Fírles Draft", "Fearless": "Fírles",
    "Worlds": "Uórlds", "Allen": "Álen", "KDA": "ka de a", "pentakill": "péntakil",
    "TheShy": "De Shái", "Rookie": "Rúki", "Wei": "Uéi", "JiaQi": "Yiachí", "Meiko": "Méiko", "Helper": "Jélper",
    "Dhokla": "Dókla", "Inspired": "Inspáierd", "Saint": "Séint", "Berserker": "Berserker", "Isles": "Áils",
    "Reignover": "Réinouver", "Zeus": "Zéus", "Kanavi": "Kanávi", "Zeka": "Zéka", "Gumayusi": "Gumayúsi",
    "Delight": "Diláit", "Chovy": "Chóvi", "Canyon": "Kéñon", "Ruler": "Rúler", "Kiin": "Kíin", "Duro": "Dúro",
    "Pun": "Pan", "Hizto": "Jízto", "Dire": "Dáier", "Eddie": "Édi", "Bie": "Bái",
    "Xin Zhao": "Shin Zháo", "Kalista": "Kalísta", "Lissandra": "Lisándra", "Yunara": "Yunára", "Ezreal": "Ézrial",
    "Nocturne": "Noctúrn", "K'Sante": "Kasánte", "Kai'Sa": "Káisa", "Tibbers": "Tíbers",
}

# Whisper oye mal los nombres («Lion», «Yachi», «Genji», «Janjoa»): transcripciones de las 37 frases leídas el 27-oct (la voz
# está bien); umbral = lo medido + margen. ElevenLabs termina en seco (cola alta sin cortar palabra).
CER_MAX_POR_FRASE = {"juego_1": 0.026, "ig_historia_1": 0.026, "ig_historia_2": 0.027, "ig_historia_4": 0.057, "ig_camino_1": 0.04, "ig_camino_3": 0.044, "jugada1_1": 0.026, "jugada1_2": 0.041, "ig_jugadores_0": 0.061, "ig_jugadores_1": 0.068, "ig_jugadores_3": 0.053, "jugada2_2": 0.044, "jugada2_3": 0.042, "jugada2_4": 0.051, "lyon_historia_0": 0.038, "lyon_historia_1": 0.055, "lyon_historia_2": 0.031, "lyon_historia_3": 0.025, "lyon_historia_5": 0.032, "lyon_camino_0": 0.084, "lyon_camino_1": 0.039, "lyon_camino_2": 0.024, "lyon_camino_3": 0.097, "jugada3_1": 0.048, "jugada3_2": 0.027, "jugada3_3": 0.024, "jugada3_4": 0.035, "jugada3_5": 0.096, "jugada3_6": 0.032, "jugada4_1": 0.063, "jugada4_2": 0.026, "jugada4_4": 0.04, "jugada4_6": 0.081, "claves_1": 0.074, "claves_2": 0.066, "claves_3": 0.052, "cierre_1": 0.026}
TAIL_MAX_POR_FRASE = {"juego_1": 1.1, "ig_historia_1": 0.96, "ig_historia_2": 0.89, "ig_historia_4": 0.88, "ig_camino_1": 0.98, "ig_camino_3": 0.94, "jugada1_1": 0.88, "jugada1_2": 0.79, "ig_jugadores_0": 0.81, "ig_jugadores_1": 1.04, "ig_jugadores_3": 0.76, "jugada2_2": 1.03, "jugada2_3": 0.68, "jugada2_4": 0.78, "lyon_historia_0": 0.33, "lyon_historia_1": 0.98, "lyon_historia_2": 1.03, "lyon_historia_3": 0.79, "lyon_historia_5": 1.05, "lyon_camino_0": 0.91, "lyon_camino_1": 0.95, "lyon_camino_2": 0.91, "lyon_camino_3": 0.19, "jugada3_1": 1.04, "jugada3_2": 0.57, "jugada3_3": 0.7, "jugada3_4": 0.61, "jugada3_5": 1.07, "jugada3_6": 1.06, "jugada4_1": 1.04, "jugada4_2": 0.79, "jugada4_4": 0.67, "jugada4_6": 0.79, "claves_1": 0.72, "claves_2": 0.92, "claves_3": 1.01, "cierre_1": 0.65}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="fade",
    fundido=0.25,
    ambiente=0.0,
    # tramos EN VIVO de cada jugada (beat largo sin voz): bajan con el audio de la transmisión (se fija tras `tiempo`)
    ambiente_por={"scene-022": .85, "scene-038": .85, "scene-061": .85, "scene-070": .85},
    yt=dict(sufijo="League of Legends Worlds 2026", min_s=30, max_min=400, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern esports broadcast analysis score: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "stadium-sized hits and tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={
        "gancho": ("cold open, dramatic hit then driving pulse, rivalry tension", 7),
        "juego": ("steady informative groove, light arpeggios, stakes rising", 4),
        "ig_historia": ("nostalgic triumphant synth brass, championship memory", 5),
        "ig_camino": ("determined comeback groove", 5),
        "jugada1": ("analysis bed: minimal pulse, ticking hi-hats, suspense, big hit near the end", 6),
        "ig_jugadores": ("confident stat-card groove", 5),
        "jugada2": ("analysis bed, patient tension exploding into a climax", 7),
        "lyon_historia": ("underdog story, warm Latin-tinged percussion over synths, hopeful", 5),
        "lyon_camino": ("rising underdog anthem energy", 6),
        "jugada3": ("analysis bed, tense, then a triumphant swell", 7),
        "jugada4": ("analysis bed, patient suspense, heroic explosive climax", 8),
        "claves": ("tactical preview groove, focused", 5),
        "cierre": ("hype build-up toward match day, final big hit and ring out", 6),
    },
    tramos=[
        (["gancho", "juego"], "Begin with an impact hit, driving pulse, then settle under the explanation."),
        (["ig_historia", "ig_camino"], "Nostalgic triumphant brass, then a determined comeback groove."),
        (["jugada1", "ig_jugadores"], "Quiet minimal analysis pulse, a big hit near the middle, then a confident groove."),
        (["jugada2", "lyon_historia"], "Patient tension exploding into a climax, then a hopeful underdog story groove."),
        (["lyon_camino", "jugada3"], "Rising underdog energy, then a tense analysis bed with a triumphant swell."),
        (["jugada4"], "Patient suspense building to a heroic explosive climax, then a triumphant afterglow."),
        (["claves", "cierre"], "A focused tactical preview groove, building hype toward match day, final big hit and ring out."),
    ])
# Tramos EN VIVO (beat sin voz con el audio de la transmisión): la música baja 16 dB para que se oiga a los narradores.
_VIVOS = [(184.9, 201.36), (317.39, 330.68), (515.54, 529.0), (592.28, 613.66)]
MEZCLA = dict(musica_curva=[(0, 0)] + [p for a, b in _VIVOS for p in ((a, 0), (a + 1.5, -16), (b - 1.0, -16), (b + .5, 0))]
              + [(900, 0)])

ESCENAS = [
    # ── GANCHO (~45 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "[excited] Hoy, en Texas, uno de estos dos equipos se mete a los cuartos de final del Mundial… y el otro se queda a una derrota de volver a casa.",
        "De un lado, Invictus Gaming: el equipo que le dio a China su primer título mundial, y que todavía juega con dos de esos campeones.",
        "Del otro, LYON: una organización nacida en México, que en 2017 tuvo que cambiar de nombre por orden de Riot… y que hoy es la gran esperanza de Norteamérica.",
        "[short pause] Si nunca los has visto jugar, en doce minutos te los presento: su historia, su camino en este Mundial, sus mejores jugadores… y cuatro jugadas analizadas pausa por pausa, para que esta tarde sepas exactamente qué mirar.",
    ]},
    # ── QUÉ ESTÁ EN JUEGO (~40 s) ──────────────────────────────────────────────────────────────────────────────────────
    {"id": "juego", "pre": 0.5, "frases": [
        "Primero, lo que está en juego. La fase suiza del Mundial tiene una regla simple: con tres victorias pasas a cuartos de final; con tres derrotas, te vas.",
        "IG y LYON llegan con dos victorias y una derrota. El que gane hoy llega a tres y se clasifica. El que pierda queda dos a dos, y se lo juega todo el sábado, en una serie a muerte.",
        "Y la serie es al mejor de tres, con Fearless Draft: un campeón que ya se usó en la serie no se puede volver a elegir. Para ganar, hay que ganar con planes distintos.",
    ]},
    # ── IG: HISTORIA (~60 s) ───────────────────────────────────────────────────────────────────────────────────────────
    {"id": "ig_historia", "pre": 1.0, "frases": [
        "Empecemos por Invictus Gaming. Para entender quiénes son, hay que volver a 2018.",
        "Incheon, Corea. Final del Mundial. IG le gana tres a cero a Fnatic y le da a China su primer título, en la final más corta de la historia: ochenta y cinco minutos de juego en total.",
        "En esa alineación estaban TheShy, en la línea superior, y Rookie, en el medio. [short pause] Ocho años después… siguen ahí. Los dos volvieron juntos a IG a finales de 2024.",
        "En soporte está el capitán, Meiko: campeón del mundo en 2021 con EDG, y el primer jugador en llegar a mil partidas en la liga china. Tres campeones del mundo en el mismo equipo.",
        "Lo completan Wei en la jungla, que fue el MVP del MSI de 2022, y el joven JiaQi como tirador. El entrenador es el coreano Helper.",
    ]},
    # ── IG: CAMINO (~45 s) ─────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "ig_camino", "pre": 0.5, "frases": [
        "Pero su 2026 no fue fácil. En la segunda etapa de la liga china ni siquiera llegaron a los playoffs.",
        "Se levantaron en la tercera: terceros. Y en la clasificación regional perdieron con Top Esports… pero le ganaron tres a uno a JD Gaming y se quedaron con el último boleto de China.",
        "Aquí, en Texas, arrancaron perdiendo con Gen.G, el día en que los cuatro equipos chinos perdieron su primera partida.",
        "Después remontaron contra Team Secret Whales… y en la tercera ronda aplastaron a Hanwha Life, el campeón del MSI: veintinueve asesinatos contra nueve.",
        "Y en esa paliza hay una pelea que explica cómo juega IG. Mírala primero tal como se vio en vivo.",
    ]},
    # ── JUGADA 1: el cuádruple de Rookie a HLE (IG-HLE, 24:2x) ─────────────────────────────────────────────────────────
    {"id": "jugada1", "pre": 16.0, "frases": [
        "[short pause] Ahora, rebobinemos. Minuto veinticuatro. IG ya tiene el alma del dragón infernal y casi cuatro mil de oro de ventaja. Hanwha acaba de robar el Barón, y necesita pelear ya.",
        "Pausa. ¿Ves esa palabra sobre los jugadores de Hanwha? «Nearsighted». Es la definitiva de Wei, con Nocturne: les apaga la visión a todos… y Rookie aprovecha para borrar a Kanavi, su jungla.",
        "Hanwha responde con todo. Zeka, con Lissandra, se mete con Destello al centro de IG… y van directo por JiaQi, el tirador. JiaQi cae.",
        "Pausa otra vez. Mira al Olaf de Zeus: «inmune al control». Mientras dure su definitiva, ningún aturdimiento le hace nada. Y aquí está la clave: IG no pelea contra eso. Retrocede… y espera.",
        "En la espera, Rookie atrapa a Gumayusi. Y en cuanto se acaba la definitiva del Olaf, le cae todo junto: el aturdimiento de Annie, el miedo de Nocturne y el polimorfo de Lulu.",
        "[excited] Cae el Olaf. Doble… triple… ¡y cuádruple para Rookie! Veinticuatro a nueve.",
        "Esa es la lección de IG para este partido: no gana por pelear más fuerte, sino por pelear en el momento justo. Si ves a IG retroceder en medio de una pelea… no es miedo. Está esperando.",
    ]},
    # ── IG: JUGADORES (~35 s) ──────────────────────────────────────────────────────────────────────────────────────────
    {"id": "ig_jugadores", "pre": 0.6, "frases": [
        "Los números de IG en este Mundial cuentan su plan. Wei, en la jungla: tres partidas, solo cinco muertes, y un KDA de nueve punto cuatro, el mejor de su equipo.",
        "Rookie, a sus veintinueve años, suma diecisiete asesinatos. JiaQi, veinte: el que remata.",
        "Y Meiko está en el ochenta y dos por ciento de los asesinatos de IG. Donde hay pelea, está el capitán.",
        "Pero IG no siempre va adelante. Contra Team Secret Whales iba perdiendo… hasta esta pelea.",
    ]},
    # ── JUGADA 2: la remontada contra TSW (TSW-IG, 24:2x) ─────────────────────────────────────────────────────────────
    {"id": "jugada2", "pre": 12.0, "frases": [
        "Rebobinemos. Minuto veintidós. Secret Whales gana diez a ocho en asesinatos y el oro está empatado. Pero IG tiene tres dragones: con el cuarto, el alma es suya.",
        "Los narradores lo explicaban así: el plan de IG es no dejarse sorprender. Que nadie atrape a su Ashe ni a la Orianna de Rookie, y pelear de frente.",
        "Pausa. Secret Whales intenta forzar: Hizto, con Qiyana, se lanza hacia Meiko… pero se queda corto. Y Wei responde con su definitiva: otra vez, el rival a ciegas.",
        "Secret Whales entra igual, pero entra por partes: uno, luego otro. Y TheShy llega con Teletransporte para cerrar el flanco.",
        "Pausa. Mira cómo quedaron: cuatro jugadores de Secret Whales, juntos, en el mismo punto. Justo lo que espera la Orianna de Rookie.",
        "[excited] ¡Onda de choque! Rookie levanta a cuatro, TheShy entra detrás, e IG gana la pelea cuatro por cero. De ahí, directo al Barón.",
    ]},
    # ── LYON: HISTORIA (~60 s) ─────────────────────────────────────────────────────────────────────────────────────────
    {"id": "lyon_historia", "pre": 1.0, "frases": [
        "Ahora, LYON. Y esta historia empieza en México.",
        "Nació en 2013 como Lyon Gaming, en la escena latinoamericana. En 2017, Riot dictaminó que el nombre y el logo no le pertenecían a su dueño: multa de doce mil quinientos dólares y cambio de nombre obligatorio.",
        "Durante siete años compitió como Rainbow7. En 2024 se fusionó con Six Karma, recuperó el nombre de LYON… y en 2026 dio el salto a la liga norteamericana, el LCS.",
        "Y en su primer año, arrasó: campeón del Lock-In, campeón de primavera, tercero en el MSI y subcampeón de verano. Hasta jugó de local en la Ciudad de México, y le ganó dos a cero a Cloud9 y a Team Liquid.",
        "Su plantilla es internacional. En la jungla, el capitán: Inspired, polaco, campeón de Norteamérica con Evil Geniuses y con FlyQuest. En 2024, con FlyQuest, llevó a Gen.G a cinco partidas en los cuartos del Mundial.",
        "En el medio, el coreano Saint, MVP de la final de primavera. El tirador, Berserker, MVP del verano. Dhokla en la línea superior, e Isles en soporte. Los dirige Reignover, exjungla de Fnatic.",
    ]},
    # ── LYON: CAMINO + JUGADORES (~45 s) ──────────────────────────────────────────────────────────────────────────────
    {"id": "lyon_camino", "pre": 0.5, "frases": [
        "En Texas, LYON le dio a Norteamérica su primera victoria del torneo, contra Team Secret Whales. Después venció a Karmine Corp, que venía de ganar el play-in.",
        "Y en la tercera ronda, contra Gen.G, el mejor equipo de Corea… le ganó la primera partida. Gen.G reaccionó y se llevó las otras dos, pero LYON ya había demostrado que puede tumbar a un gigante.",
        "Su arma más letal: Berserker. Veinticinco asesinatos, el que más en su equipo, trece de ellos en una sola partida, con Ezreal. Saint tiene el mejor KDA de LYON. Y Isles está en nueve de cada diez asesinatos.",
        "Para entender cómo pelea LYON, mira esta pelea contra Team Secret Whales.",
    ]},
    # ── JUGADA 3: Berserker contra TSW (LYON-TSW, 15:5x) ──────────────────────────────────────────────────────────────
    {"id": "jugada3", "pre": 12.0, "frases": [
        "Rebobinemos. Minuto quince. Dos minutos antes, LYON se pasó de agresivo, persiguió de más y perdió a tres jugadores. Secret Whales ya va arriba en oro.",
        "Pausa. LYON está en el Heraldo. Secret Whales lo descubre con un centinela y llega a disputarlo. Bie, con Nautilus, está listo para iniciar.",
        "Pero Inspired se adelanta: la definitiva de Nocturne. Todo Secret Whales, a oscuras.",
        "Bie le lanza su definitiva a Berserker… pero en la oscuridad nadie lo sigue. Y el primero en caer es él.",
        "Pausa. Pun llega con Teletransporte a la retaguardia de LYON, con Rumble. Es la última carta de Secret Whales.",
        "[excited] Y la carta sale mal. Berserker remata a Hizto, Dhokla a Dire, y Pun cae también. ¡Cuatro por cero para LYON!",
        "Esa es la marca de LYON: cuando se equivoca, no se esconde. Se reagrupa, gana la visión… y vuelve a pelear. Y con esa misma idea se plantó ante Gen.G. Esta es la pelea que le dio la primera partida.",
    ]},
    # ── JUGADA 4: LYON le gana la partida 1 a Gen.G (34:4x) ───────────────────────────────────────────────────────────
    {"id": "jugada4", "pre": 18.0, "frases": [
        "Rebobinemos. Minuto treinta y cuatro. LYON va tres mil arriba y tiene tres dragones: el próximo le daría el alma.",
        "Pausa. Un detalle que lo cambia todo: Berserker, Dhokla y Saint no tienen Destello. Pero del otro lado, Chovy y Ruler tampoco.",
        "Saint prueba con Ahri: entra, conecta su combo… y sale. LYON se retira y espera al dragón.",
        "Pausa. Mira las posiciones: Gen.G, junto, arriba, sobre el dragón. LYON, enfrente. Y Dhokla, con Olaf, escondido en un arbusto del flanco.",
        "Es un cincuenta-cincuenta de castigo entre Inspired y Canyon. Pero Inspired no espera.",
        "Destello… y Xin Zhao se lanza al centro de los cinco. Su definitiva empuja a todos hacia afuera y lo vuelve casi intocable para los que pegan de lejos.",
        "[excited] Dhokla entra por el flanco… ¡cae Chovy! Berserker remata a Ruler y a Duro. ¡LYON gana la pelea!",
        "LYON recorre el mapa, rompe la base… y le gana la primera partida al primer sembrado de Corea. «Se suponía que era imposible», gritaba el narrador.",
        "Esa es la amenaza de LYON: paciencia, una buena posición… y un jungla que sabe exactamente cuándo entrar.",
    ]},
    # ── CLAVES DEL DUELO (~60 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "claves", "pre": 0.6, "frases": [
        "¿Y el partido de hoy? Tres claves para verlo como un experto.",
        "Uno: la jungla. Wei contra Inspired. Wei casi no muere; Inspired es el que da las órdenes en LYON. El que lea mejor el mapa decide dónde se pelea.",
        "Dos: el medio. Rookie, campeón del mundo, contra Saint, el jugador más fino de LYON en este torneo. Si Rookie gana su línea, IG pelea con ventaja.",
        "Tres: la experiencia contra el hambre. IG tiene tres campeones del mundo; LYON, ninguno. Pero LYON elige primero en la primera partida, y ya sabe lo que es quitarle un juego al mejor de Corea.",
        "Y un dato: hasta donde hay registro, nunca se han enfrentado en un partido oficial. Hoy es la primera vez.",
    ]},
    # ── CIERRE: HORARIOS (~30 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.6, "frases": [
        "Así que prepárate, porque hoy el día viene cargado. A las dos de la tarde, hora del centro de México, juegan T1 y Movistar KOI: el tricampeón del mundo también se juega su pase a cuartos.",
        "Y después, a partir de las cinco de la tarde, o en cuanto termine esa serie… IG contra LYON.",
        "[excited] ¿Tú con quién vas? ¿Con la experiencia de IG… o con el sueño de LYON? Déjalo en los comentarios. Nos vemos en el partido.",
    ]},
]
