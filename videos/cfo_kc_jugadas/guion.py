# -*- coding: utf-8 -*-
"""CFO 0-2 KC (Worlds 2026, fase suiza, ronda 4, Bo3 a muerte, jue 29-oct-2026, 14:00 CDMX): análisis de las jugadas clave,
~16 min, canal «Crónicas de ligoleyen» (subida por Studio; se publica el MISMO día por la noche → «hoy», «esta tarde»).
Estilo ANÁLISIS TÁCTICO como videos/t1_koi_worlds/ (docs/estilo_analisis_tactico.md): pausas con telestrador, rutas medidas,
repeticiones, mesas 3D y capa 3D en las jugadas clave. SIN SPOILER en título, miniatura y gancho.

DATOS VERIFICADOS: investigacion/datos_g1.md y datos_g2.md (feed oficial + VOD Twitch LATAM 2914166111 + Whisper; reloj del HUD),
g2_asist.txt (feed G2 con reloj de JUEGO, sin las pausas), API getEventDetails (match 115660540726095073).
- Partida 1 (gameId …074): KC azul. KC Canna Galio, Yike Wukong, kyeahoo Cassiopeia, Caliste Tristana, Busio Nautilus ·
  CFO Rest Rumble, Shad0w Jarvan IV, POUT Syndra, Doggo Kai'Sa, Kino Alistar. KC gana 19-3 en 27:39 (CFO 0 torres).
- Partida 2 (gameId …075): CFO azul. CFO Rest Ambessa, Shad0w Lee Sin, POUT Ryze, Doggo Caitlyn, Kino Karma ·
  KC Canna Camille, Yike Pantheon, kyeahoo Viktor, Caliste Yunara, Busio Lulu. KC gana 20-12 en 36:58 de juego, con ~29 min
  de pausa a los 25:06 (y 7 min a los 17:07). CFO llegó a +4,8 K (min 20), Barón 24:21, alma del océano 28:00, inhibidor 29:11;
  KC: pelea 4 por 0 (20:08-20:49), 3 por 1 (30:22-30:26), Barón 31:00, ancestral 36:01 + 5 por 1 (35:36-36:03), nexo 36:58.
- Serie (feed): KC 39 asesinatos, CFO 15. kyeahoo 12/1/19 (su única muerte: G1 14:48). Caliste 11/4/17. Doggo G1 0/3/0 (0 %),
  G2 2/6/7 con el 40 % del daño de CFO. Previa (cfo_kc_worlds/guion.py § claves): pelea de mitad de partida, objetivos (CFO ganó
  su única partida con alma + ancestral; KC salvó su serie con el ancestral), Fearless (Rest Rumble, Yike Lee Sin).
- Torneo: los dos llegaban 1-2: CFO queda 1-3, ELIMINADO; KC 2-2 juega la ronda 5 el sábado 31 (a muerte).
"""

TITULO = "CFO vs KC: las jugadas clave analizadas | Worlds 2026"
ARCHIVO = "cfo_kc_jugadas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español), la voz de la Worlds, IG-LYON, CFO-KC y T1-KOI
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
FONETICA = {
    "CTBC Flying Oyster": "Ci Ti Bi Ci Fláin Óister", "Flying Oyster": "Fláin Óister", "CTBC": "Ci Ti Bi Ci",
    "Karmine Corp": "Kármin Corp", "Karmine": "Kármin", "LYON": "Láion", "T1": "Ti uan", "Movistar KOI": "Movistar Koi",
    "Fearless Draft": "Fírles Draft", "Fearless": "Fírles", "Worlds": "Uórlds",
    "Shad0w": "Shádou", "POUT": "Páut", "Doggo": "Dógo", "Kino": "Kíno", "Rest": "Rest",
    "Canna": "Kána", "Yike": "Yáik", "kyeahoo": "Kiéju", "Caliste": "Calíst", "Busio": "Búsio",
    "Galio": "Gálio", "Wukong": "Uukóng", "Cassiopeia": "Casiopéa", "Tristana": "Tristána", "Nautilus": "Náutilus",
    "Rumble": "Rámbol", "Jarvan": "Yárvan", "Syndra": "Síndra", "Kai'Sa": "Káisa", "Alistar": "Alístar",
    "Ambessa": "Ambésa", "Lee Sin": "Li Sin", "Ryze": "Ráis", "Caitlyn": "Kéitlin", "Karma": "Kárma",
    "Camille": "Kamíl", "Pantheon": "Pánteon", "Viktor": "Víktor", "Yunara": "Iunára", "Lulu": "Lulú",
}

CER_MAX_POR_FRASE = {"gancho_0": 0.09, "draft1_0": 0.089, "draft1_1": 0.057, "jugada1_1": 0.047, "jugada1_2": 0.071, "jugada1_3": 0.081, "jugada1_4": 0.047, "jugada1_5": 0.034, "jugada2_2": 0.074, "jugada3_0": 0.071, "jugada3_1": 0.042, "jugada3_4": 0.083, "jugada3_5": 0.043, "jugada4_0": 0.02, "jugada4_2": 0.052, "jugada4_3": 0.047, "jugada4_4": 0.062, "jugada4_rep_0": 0.038, "jugada5_0": 0.071, "jugada5_1": 0.076, "jugada5_2": 0.042, "jugada5_rep_0": 0.041, "curva1_1": 0.033, "draft2_0": 0.063, "draft2_1": 0.128, "draft2_2": 0.054, "jugada6_0": 0.032, "jugada6_1": 0.116, "jugada6_2": 0.083, "jugada6_3": 0.043, "jugada7_1": 0.049, "jugada7_2": 0.032, "jugada7_3": 0.048, "jugada7_4": 0.047, "jugada7_rep_0": 0.048, "jugada8_0": 0.046, "jugada8_1": 0.065, "jugada8_2": 0.057, "jugada9_1": 0.038, "jugada9_3": 0.121, "jugada9_4": 0.047, "jugada9_rep_0": 0.033, "jugada10_0": 0.035, "jugada10_1": 0.099, "jugada10_2": 0.086, "jugada10_4": 0.058, "jugada10_5": 0.051, "curva2_0": 0.035, "predicciones_1": 0.084, "predicciones_2": 0.107, "boleta_kc_0": 0.046, "boleta_kc_2": 0.038, "boleta_kc_3": 0.044, "boleta_cfo_0": 0.04, "numeros_0": 0.036, "sigue_1": 0.052, "cierre_0": 0.039}
TAIL_MAX_POR_FRASE = {"gancho_0": 0.59, "draft1_0": 0.91, "draft1_1": 0.66, "jugada1_1": 0.44, "jugada1_2": 0.83, "jugada1_3": 0.77, "jugada1_4": 0.92, "jugada1_5": 0.83, "jugada2_2": 0.96, "jugada3_0": 0.7, "jugada3_1": 0.79, "jugada3_4": 0.85, "jugada3_5": 0.91, "jugada4_0": 1.12, "jugada4_2": 1.06, "jugada4_3": 0.66, "jugada4_4": 0.96, "jugada4_rep_0": 0.69, "jugada5_0": 0.88, "jugada5_1": 0.83, "jugada5_2": 0.9, "jugada5_rep_0": 0.72, "curva1_1": 0.93, "draft2_0": 1.08, "draft2_1": 1.46, "draft2_2": 1.0, "jugada6_0": 0.9, "jugada6_1": 0.94, "jugada6_2": 1.02, "jugada6_3": 0.74, "jugada7_1": 0.91, "jugada7_2": 1.02, "jugada7_3": 0.86, "jugada7_4": 0.64, "jugada7_rep_0": 0.99, "jugada8_0": 0.78, "jugada8_1": 0.91, "jugada8_2": 0.67, "jugada9_1": 0.86, "jugada9_3": 0.49, "jugada9_4": 0.9, "jugada9_rep_0": 1.2, "jugada10_0": 0.9, "jugada10_1": 0.6, "jugada10_2": 0.48, "jugada10_4": 0.71, "jugada10_5": 1.02, "curva2_0": 1.14, "predicciones_1": 1.0, "predicciones_2": 0.77, "boleta_kc_0": 0.99, "boleta_kc_2": 0.66, "boleta_kc_3": 0.78, "boleta_cfo_0": 0.6, "numeros_0": 1.03, "sigue_1": 0.75, "cierre_0": 0.92}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="fade",
    fundido=0.25,
    ambiente=0.0,
    # tramos EN VIVO de cada jugada (beat largo sin voz): se cortan de medios/_fuente con su narración (se fija tras `beats`)
    ambiente_por={},
    yt=dict(sufijo="League of Legends Worlds 2026", min_s=30, max_min=400, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern esports broadcast analysis score: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "stadium-sized hits and tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={},
    # de la BIBLIOTECA (29-oct-2026: `biblioteca usar <id> cfo_kc_jugadas <tramo>`), sin Lyria nueva
    tramos=[
        (["gancho", "juego", "draft1"], "Impact hit, do-or-die stakes, then tense draft-phase ticking."),
        (["jugada1", "jugada2"], "Uneasy minimal analysis pulse, hunters in the river."),
        (["jugada3", "jugada3_rep"], "Dark analysis bed building to an explosive dragon-pit massacre, then a suspended replay."),
        (["jugada4", "jugada4_rep", "jugada5", "jugada5_rep"], "Crushing momentum with big hits, closing out game one."),
        (["curva1", "draft2", "jugada6"], "Reflective recap, then a confident underdog comeback groove."),
        (["jugada7", "jugada7_rep", "jugada8"], "The tide turns: tense mid-game fight, chaos at Baron, then a long suspended pause."),
        (["jugada9", "jugada9_rep", "jugada10", "jugada10_rep"], "Do-or-die suspense building to the Elder Dragon climax and a heroic victory."),
        (["curva2", "predicciones", "boleta_kc", "boleta_cfo"], "Focused summary groove and player report cards."),
        (["numeros", "sigue", "cierre"], "Confident stat groove, forward-looking build and a final hit."),
    ])
# Tramos EN VIVO (narración original en español, vivos_audio.py → audio/ambiente.wav): la música baja 16 dB para oírla.
_VIVOS = [(91.64, 106.89), (159.27, 173.29), (200.73, 217.98), (296.73, 311.98), (381.82, 396.07), (504.0, 519.25),
          (562.91, 580.01), (645.82, 660.07), (696.0, 711.25), (781.09, 798.34)]
MEZCLA = dict(musica_curva=[(0, 0)] + [p for a, b in _VIVOS for p in ((a, 0), (a + 1.5, -16), (b - 1.0, -16), (b + .5, 0))]
              + [(1000, 0)])

ESCENAS = [
    # ── GANCHO (~40 s; SIN SPOILER) ────────────────────────────────────────────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "[excited] Esta tarde, CTBC Flying Oyster y Karmine Corp se jugaron la vida en el Mundial: el que perdiera, se iba a casa.",
        "Y fue una serie con de todo: un dragón que terminó en masacre, una ventaja de casi cinco mil de oro, una pausa de casi media hora… y un dragón ancestral que lo decidió todo.",
        "[short pause] Hoy analizamos las jugadas clave, pausa por pausa: las mejores, las más inteligentes, las predicciones que se cumplieron… y los errores de cada jugador.",
    ]},
    # ── LO QUE ESTABA EN JUEGO (~30 s) ─────────────────────────────────────────────────────────────────────────────────
    {"id": "juego", "pre": 0.5, "frases": [
        "Lo que estaba en juego. En la fase suiza, con tres derrotas te vas a casa. Y los dos llegaban con una victoria y dos derrotas.",
        "Así que esta serie era a muerte: el que ganara, seguía vivo para la quinta ronda. El que perdiera, quedaba eliminado del Mundial.",
        "Al mejor de tres, con Fearless Draft: un campeón que ya se usó en la serie no se puede volver a elegir.",
    ]},
    # ── PARTIDA 1: DRAFT (~30 s; datos_g1 § alineaciones y draft) ──────────────────────────────────────────────────────
    {"id": "draft1", "pre": 0.6, "frases": [
        "Partida uno. Karmine, del lado azul: Canna con Galio, Yike con Wukong, kyeahoo con Cassiopeia, Caliste con Tristana y Busio con Nautilus.",
        "CFO, del lado rojo: Rest con Rumble, su campeón insignia, Shad0w con Jarvan Cuarto, POUT con Syndra, Doggo con Kai'Sa y Kino con Alistar.",
        "Y una duda de los narradores: no sabían si Tristana era buena idea contra esa Syndra. Guarda esa predicción.",
    ]},
    # ── JUGADA 1 · el dragón de Nube por la 1.ª sangre (05:35-05:53, g1_j1) + la respuesta de Shad0w (07:50, g1_j2) ──────
    {"id": "jugada1", "pre": 15.0, "frases": [
        "[short pause] Rebobinemos. Minuto cinco. CFO aprovecha el caos y se lleva el primer dragón, el de Nube.",
        "Pausa. Pero mira a POUT, con Syndra: está sin Destello. Karmine ya lo había emboscado dos veces.",
        "Busio y Yike revisan el arbusto, ven que no hay visión… y saben que Shad0w y Kino se fueron al dragón. Nadie va a ayudar a POUT.",
        "A la tercera, no se escapa: Yike lo remata. Primera sangre para Karmine. CFO cambió un dragón por su mago.",
        "Pausa otra vez. Minuto siete. Ahora es Busio el que se queda solo en el río… y Shad0w lo lee: si Busio no está en su carril y no hay guardia, está ahí.",
        "Shad0w y POUT le caen encima, y POUT se cobra la revancha. Uno a uno. CFO también sabe cazar.",
    ]},
    # ── JUGADA 2 · Caliste castiga a Kino, un nivel abajo (09:46, g1_j3) ───────────────────────────────────────────────
    {"id": "jugada2", "pre": 14.0, "frases": [
        "Minuto nueve. Y aquí está un detalle que casi nadie ve: Kino, con Alistar, todavía es nivel cinco. Busio ya es nivel seis.",
        "Pausa. Con la definitiva de Nautilus lista, Busio va hacia adelante… porque sabe que Kino no le puede responder.",
        "Caliste remata a Kino. Y los narradores lo dijeron en ese momento: si Caliste se alimenta, Karmine tiene asegurado el juego medio y tardío.",
    ]},
    # ── JUGADA 3 · el dragón Químico: Canna cae del cielo y 3 por 0 (11:31-11:46, g1_j4) ★ 3D ──────────────────────────
    {"id": "jugada3", "pre": 17.0, "post": 4.0, "frases": [
        "Minuto once. La jugada más importante de la primera partida. Karmine va mil de oro arriba, y Yike empieza el dragón Químico.",
        "Pausa. Mira la visión: Karmine tiene guardias cubriendo toda la entrada del foso. CFO no puede llegar sin que lo vean.",
        "Y CFO llega igual. Kino lanza su definitiva, Shad0w salta por el risco, y Rest aparece con Teleportación… en una posición comprometida.",
        "Pausa otra vez. Ahora mira a Doggo, con Kai'Sa: no ha regresado a base. No tiene ni su primer objeto. No pega.",
        "Yike asegura el dragón… y Canna, con Galio, cae encima de todos. Canna mata a Shad0w.",
        "[excited] Y kyeahoo remata a Kino… ¡y a Doggo! Tres por cero, y el dragón. CFO propuso la pelea… pero sin recursos para ganarla.",
    ]},
    {"id": "jugada3_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. La definitiva de Kino ya estaba gastada, la Kai'Sa no tenía objeto, y la Teleportación cayó donde no debía. Tres errores en una sola pelea.",
    ]},
    # ── JUGADA 4 · lo mejor de CFO (14:48, g1_j5) y las dos peleas 3 por 0 (17:19-18:36, g1_j6) ─────────────────────────
    {"id": "jugada4", "pre": 15.0, "frases": [
        "Minuto catorce. Lo mejor de CFO en esta partida. Kino se lanza bajo la torre de kyeahoo, aguanta los golpes… y tres contra uno, POUT lo remata.",
        "Guarda este dato: va a ser la única muerte de kyeahoo en toda la serie.",
        "Pero la respuesta de Karmine es brutal. Minuto diecisiete. Rest entra con Teleportación y la definitiva de Rumble…",
        "Pausa. Mira a Canna: su provocación con Galio atrapa a CFO, y kyeahoo los petrifica con Cassiopeia.",
        "[excited] Caliste remata a Kino y a Rest, kyeahoo a Shad0w. ¡Tres por cero! Y un minuto después… otra vez. Caliste, Yike y kyeahoo: tres por cero.",
        "Los narradores lo resumieron así: CFO no había hecho un solo combo en toda la partida.",
    ]},
    {"id": "jugada4_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. Dos peleas, seis muertes de CFO y ninguna de Karmine. La ventaja pasa de casi tres mil a casi seis mil quinientos en dos minutos.",
    ]},
    # ── JUGADA 5 · el pick a Shad0w + Barón (24:32-24:56, g1_j7) y el cierre (27:21-27:39, g1_j8) → 1-0 ────────────────────
    {"id": "jugada5", "pre": 14.0, "frases": [
        "Minuto veinticuatro. Canna encuentra a Shad0w con la provocación perfecta, en el momento perfecto… y Yike lo remata.",
        "CFO responde llevándose a Busio, pero no importa: sin su jungla, CFO no puede pelear el Barón. Barón para Karmine.",
        "[excited] Tres minutos después, exterminio: los cinco de CFO caen en siete segundos… ¡y cae el nexo! Uno a cero para Karmine Corp.",
    ]},
    {"id": "jugada5_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. Diecinueve asesinatos contra tres, y CFO no derribó ni una sola torre. Una partida perfecta de Karmine.",
    ]},
    # ── PARTIDA 1 EN ORO + PREDICCIONES (~30 s; datos_g1 § curva) ──────────────────────────────────────────────────────
    {"id": "curva1", "pre": 0.6, "frases": [
        "Así se ve la partida uno en oro: CFO no estuvo arriba ni un solo minuto después del primero. Quince mil de diferencia al final.",
        "¿Y las predicciones? La duda sobre Tristana: falló. Caliste terminó siete, cero y cinco. Y la otra, la de no dejar crecer a la Kai'Sa: se cumplió. Doggo terminó sin participar en un solo asesinato.",
    ]},
    # ── PARTIDA 2: DRAFT (~30 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "draft2", "pre": 0.6, "frases": [
        "Partida dos. Ahora CFO, contra las cuerdas, del lado azul: Rest con Ambessa, Shad0w con Lee Sin, POUT con Ryze, Doggo con Caitlyn y Kino con Karma.",
        "Karmine: Canna con Camille, Yike con Pantheon, kyeahoo con Viktor, Caliste con Yunara y Busio con Lulu.",
        "Y ojo con la jugada de draft: Shad0w abre con Lee Sin, el campeón que Yike se estaba guardando. Por el Fearless, en una tercera partida ya no lo podría usar nadie.",
    ]},
    # ── JUGADA 6 · el arranque de CFO: 1.ª sangre (02:15), 3 por 1 (06:13-06:29), Busio (09:52), 4 torres a 0 (g2_j1/j2/j3) ──
    {"id": "jugada6", "pre": 15.0, "frases": [
        "Y esta vez, CFO sale con todo. Minuto dos: Doggo, con Caitlyn, se cobra a Caliste. Primera sangre para CFO.",
        "Minuto seis. Pausa. Busio mata a Doggo… pero mira quién llega: Shad0w con Lee Sin, y POUT con Ryze.",
        "Shad0w remata a Busio, POUT caza a Yike. Dos por uno en la pelea, tres a uno en el marcador para CFO, y con el primer dragón.",
        "Minuto nueve, Shad0w vuelve a encontrar a Busio. Y desde ahí, CFO derriba cuatro torres sin perder ninguna.",
        "En el minuto veinte, CFO va casi cinco mil de oro arriba. La partida que nadie esperaba.",
    ]},
    # ── JUGADA 7 · la pelea de mitad de partida: 4 por 0 de KC (20:04-20:44, g2_j4) ★ 3D ──────────────────────────────
    {"id": "jugada7", "pre": 17.0, "post": 4.0, "frases": [
        "Pero en la previa dijimos que esta serie se decidía en la pelea de mitad de partida. Y aquí está. Minuto veinte, junto al foso del Barón, que acaba de aparecer.",
        "Pausa. Mira dónde está cada uno. CFO tiene el oro… pero Karmine llega a la pelea con cuatro.",
        "Canna, con Camille, va directo sobre Doggo. La tiradora de CFO cae primero… y sin ella, a CFO le falta daño.",
        "Pausa otra vez. Siete segundos después, Yike, con Pantheon, mata a Rest. Y Canna remata a Kino.",
        "[excited] Y medio minuto después, Yike remata también a POUT. ¡Cuatro por cero para Karmine! Y la ventaja de CFO baja de casi cinco mil a menos de tres mil.",
    ]},
    {"id": "jugada7_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. CFO dominó veinte minutos, y en menos de un minuto devolvió la mitad de su ventaja.",
    ]},
    # ── JUGADA 8 · el Barón de CFO (24:21), la pelea 4 por 4 y la pausa (g2_j5) ────────────────────────────────────────
    {"id": "jugada8", "pre": 14.0, "frases": [
        "Minuto veinticuatro. CFO ya tiene tres dragones. Doggo mata a Canna… y CFO va por el Barón. Lo asegura.",
        "Pausa. Karmine no se rinde y los espera a la salida del foso. Ahora mira el caos: en treinta y cinco segundos caen siete jugadores.",
        "Contando a Canna, cuatro de cada lado. Pero CFO se queda con el Barón.",
        "Y entonces… la partida se detiene. Problemas técnicos en el equipo de Doggo: casi media hora de pausa, con el Mundial en el aire.",
    ]},
    # ── JUGADA 9 · el alma del océano (28:00), el inhibidor (29:11) y la pelea 3 por 1 + Barón de KC (30:20-31:00, g2_j6/j7) ──
    {"id": "jugada9", "pre": 15.0, "post": 4.0, "frases": [
        "Se reanuda, y CFO no pierde el tiempo. Minuto veintiocho: cuarto dragón, el del océano… y con él, el alma.",
        "POUT mata a Canna, CFO derriba su primer inhibidor y va tres mil setecientos arriba, con el alma. Todo apuntaba a una tercera partida.",
        "Pausa. Minuto treinta. El Barón acaba de reaparecer, Caliste entra y Rest la mata… pero dos segundos después, la pelea se le voltea a CFO.",
        "[excited] kyeahoo, con Viktor, remata a Doggo, Yike atrapa a Kino, y kyeahoo cierra con Rest. ¡Tres por uno para Karmine!",
        "Treinta y cuatro segundos después, Barón para Karmine. Y un minuto después, el oro, que llegó a estar casi cinco mil para CFO, está empatado.",
    ]},
    {"id": "jugada9_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. Rest consigue su asesinato… y su equipo paga por él con tres muertes y un Barón.",
    ]},
    # ── JUGADA 10 · el dragón ancestral y el 5 por 1 (35:36-36:03) → nexo 36:58 (g2_j8) ★ 3D ─────────────────────────────
    {"id": "jugada10", "pre": 17.0, "post": 4.0, "frases": [
        "Minuto treinta y tres: por primera vez desde el minuto dos, Karmine va arriba en oro. Y el dragón ancestral ya está en el mapa: el que gane esta pelea, casi seguro gana la serie.",
        "Pausa. Antes de que el dragón sea de nadie, Karmine encuentra a Shad0w, con Lee Sin.",
        "Yike mata a Shad0w, y CFO tiene que pelear el ancestral cuatro contra cinco.",
        "Pausa otra vez. Y ahora entra Caliste, con Yunara.",
        "Caliste remata a Rest y a POUT en dos segundos. Kino se cobra a Canna… pero Karmine asegura el ancestral.",
        "[excited] kyeahoo caza a Doggo, Caliste remata a Kino… ¡cinco por uno, y con el ancestral! Karmine va directo a la base… ¡y cae el nexo! ¡Dos a cero, y Karmine Corp sigue vivo en el Mundial!",
    ]},
    {"id": "jugada10_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. CFO llegó a ir casi cinco mil arriba, tuvo el Barón, el alma y un inhibidor. Y perdió la partida en tres peleas.",
    ]},
    # ── PARTIDA 2 EN ORO (~20 s) ────────────────────────────────────────────────────────────────────────────────────────
    {"id": "curva2", "pre": 0.6, "frases": [
        "Así se ve la partida dos en oro: CFO arriba casi cinco mil en el minuto veinte, casi cuatro mil tras el alma y el inhibidor… y desde la pelea del minuto treinta, todo de Karmine. Siete mil abajo al final.",
    ]},
    # ── ¿SE CUMPLIERON LAS PREDICCIONES DE LA PREVIA? (~40 s; cfo_kc_worlds § claves) ───────────────────────────────────
    {"id": "predicciones", "pre": 0.6, "frases": [
        "¿Y nuestras tres claves de la previa? Uno: la pelea de mitad de partida. Se cumplió: el que iba arriba se tropezó en el minuto veinte, y esta vez fue CFO.",
        "Dos: los objetivos. Dijimos que CFO había ganado su única partida con alma y ancestral, y que Karmine salvó su serie con el ancestral. CFO consiguió el alma… pero el ancestral fue de Karmine. Otra vez.",
        "Tres: el Fearless. Rest gastó su Rumble en la primera partida y la perdió. Y Shad0w le quitó el Lee Sin a Yike… que respondió con Pantheon y doce asistencias.",
    ]},
    # ── LA BOLETA: aciertos y errores de cada jugador (~75 s; MG nuevo) ────────────────────────────────────────────────
    {"id": "boleta_kc", "pre": 0.6, "frases": [
        "Ahora, la boleta de cada jugador. Karmine. kyeahoo: doce asesinatos y una sola muerte en toda la serie. Cero muertes en la segunda partida. La figura.",
        "Caliste: le dijeron que Tristana no era buena idea, y terminó la primera partida sin morir. Su error: la primera sangre de la segunda partida, a los dos minutos.",
        "Canna: la entrada al dragón Químico y la pelea del minuto veinte. Yike: la primera sangre de la serie y el que cazó a Shad0w antes del ancestral.",
        "Y Busio: diecisiete asistencias en la segunda, pero fue el que más veces cazaron al principio: tres muertes antes del minuto diez entre las dos partidas.",
    ]},
    {"id": "boleta_cfo", "pre": 0.6, "frases": [
        "CFO. Shad0w: la mejor lectura de su equipo, la cacería de Busio, y cinco asesinatos en la segunda. Pero en la primera, seis muertes.",
        "Doggo: de cero participación en la primera, a la primera sangre y el cuarenta por ciento del daño de su equipo en la segunda.",
        "POUT: los tres únicos asesinatos de CFO en la primera partida. Kino: llegó un nivel abajo a la pelea del minuto nueve y gastó su definitiva antes del dragón.",
        "Y Rest: la Teleportación del dragón Químico, la entrada del minuto treinta… siete muertes en la serie y un solo asesinato.",
    ]},
    # ── LOS NÚMEROS (~25 s) ────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "numeros", "pre": 0.6, "frases": [
        "Los números de la serie: treinta y nueve asesinatos de Karmine contra quince de CFO. Siete torres de CFO en toda la serie… y las siete fueron en la segunda partida.",
    ]},
    # ── QUÉ SIGUE (~25 s) ──────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "sigue", "pre": 0.6, "frases": [
        "¿Y ahora? CFO queda con una victoria y tres derrotas: eliminado del Mundial.",
        "Karmine Corp queda dos y dos, y el sábado treinta y uno juega la quinta ronda, otra vez a muerte. Si gana, a cuartos de final.",
    ]},
    # ── CIERRE (~15 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.6, "frases": [
        "[excited] ¿Cuál fue para ti la jugada clave de la serie? ¿Y le alcanza a Karmine para llegar a cuartos? Déjalo en los comentarios. Nos vemos el sábado.",
    ]},
]
