# -*- coding: utf-8 -*-
"""T1 2-0 Movistar KOI (Worlds 2026, fase suiza, ronda 4, mié 28-oct-2026, 14:00 CDMX): análisis de las MEJORES JUGADAS,
~16 min, canal «Crónicas de ligoleyen» (subida por Studio; se publica el MISMO día a las 20:00 CDMX → «hoy», «esta tarde»).
Estilo ANÁLISIS TÁCTICO como videos/cfo_kc_worlds/ (docs/estilo_analisis_tactico.md): pausas con telestrador, rutas medidas,
repeticiones, mesas 3D y capa 3D en la jugada clave (la pelea final de la partida 1).

DATOS VERIFICADOS: investigacion/muertes.txt (feed oficial, reloj del FEED), datos_g1.md y datos_g2.md (VOD + feed + narración
con Whisper; reloj del HUD), API getEventDetails (match 115660540726095061: T1 2 · MKOI 0; partida 3 «unneeded»).
- Partida 1 (gameId …062, VOD rTVyiDIg-n8): T1 azul. T1 Doran Ambessa, Oner Lee Sin, Faker Syndra, Peyz Xayah, Keria Nautilus ·
  MKOI Myrwn Gnar, Elyoya Qiyana, Jojopyun Akali, Supa Kai'Sa, Alvaro Alistar. T1 gana 20-10.
- Partida 2 (gameId …063, VOD irsYoLi62_U): T1 azul. T1 Doran Gwen, Oner Jarvan IV, Faker Orianna, Peyz Jhin, Keria Karma ·
  MKOI Myrwn Ornn, Elyoya Xin Zhao, Jojopyun Viktor, Supa Ezreal, Alvaro Seraphine. T1 gana 22-9.
- Torneo (lol_worlds_2026/guion.py, ig_lyon_worlds/investigacion/datos.md): T1 R1 > LOS, R2 < DK, R3 > CFO; KOI R1 > BLG,
  R2 > CFO, R3 0-2 DK. T1 = campeón 2023, 2024 y 2025, va por el 4.º seguido. Con 3-1 T1 está en cuartos (3-6 nov, Bo5);
  KOI 2-2 juega la ronda 5 el sábado 31 (a muerte). Sorteo de cuartos: los 3-1 entre sí.
"""

TITULO = "T1 vs KOI: las mejores jugadas analizadas | Worlds 2026"
ARCHIVO = "t1_koi_worlds"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español), la voz de la Worlds, IG-LYON y CFO-KC
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
FONETICA = {
    "Movistar KOI": "Movistar Koi", "KOI": "Koi", "T1": "Ti uan", "Dplus KIA": "Di plus Kía", "Gen.G": "Yen yi",
    "Los Grandes": "Los Grandes", "CTBC Flying Oyster": "Si Ti Bi Si Fláin Óister", "Bilibili Gaming": "Bilibili Guéiming",
    "Fearless Draft": "Fírles Draft", "Fearless": "Fírles", "Worlds": "Uórlds", "KDA": "ka de a",
    "Faker": "Féiker", "Keria": "Kéria", "Oner": "Óner", "Peyz": "Péis", "Doran": "Dóran",
    "Myrwn": "Mírwin", "Elyoya": "Elioya", "Jojopyun": "Yoyopiún", "Supa": "Súpa", "Alvaro": "Álvaro",
    "Ambessa": "Ambésa", "Lee Sin": "Li Sin", "Syndra": "Síndra", "Xayah": "Záia", "Nautilus": "Náutilus",
    "Gnar": "Nar", "Qiyana": "Kiána", "Kai'Sa": "Káisa", "Alistar": "Alístar",
    "Gwen": "Güen", "Jarvan": "Yárvan", "Orianna": "Oriána", "Jhin": "Yin", "Ornn": "Orn", "Xin Zhao": "Shin Zháo",
    "Viktor": "Víktor", "Ezreal": "Ésreal", "Seraphine": "Sérafin",
}

CER_MAX_POR_FRASE = {"jugada3_rep_0": 0.044, "jugada7_rep_0": 0.057, "camino_1": 0.038, "draft1_0": 0.072, "draft1_1": 0.055, "jugada1_0": 0.042, "jugada1_1": 0.02, "jugada1_2": 0.037, "jugada1_3": 0.04, "jugada1_4": 0.095, "jugada1_5": 0.049, "jugada2_1": 0.045, "jugada2_3": 0.042, "jugada2_4": 0.06, "jugada2_5": 0.043, "jugada2_6": 0.057, "jugada3_1": 0.044, "jugada3_2": 0.06, "jugada3_3": 0.039, "jugada3_4": 0.033, "jugada3_5": 0.088, "jugada3_6": 0.077, "jugada4_2": 0.033, "jugada4_3": 0.04, "jugada4_4": 0.049, "jugada4_5": 0.096, "jugada4_6": 0.137, "jugada4_rep_1": 0.052, "curva1_0": 0.049, "draft2_1": 0.097, "draft2_2": 0.12, "jugada5_0": 0.05, "jugada5_1": 0.06, "jugada6_0": 0.037, "jugada6_2": 0.086, "jugada6_3": 0.034, "jugada6_4": 0.033, "jugada6_5": 0.083, "jugada6_rep_0": 0.033, "jugada7_1": 0.046, "claves_1": 0.092, "claves_2": 0.073, "claves_3": 0.074, "numeros_1": 0.072, "sigue_0": 0.041, "sigue_2": 0.04, "cierre_0": 0.02}
TAIL_MAX_POR_FRASE = {"jugada3_rep_0": 0.94, "jugada7_rep_0": 0.42, "camino_1": 0.67, "draft1_0": 0.83, "draft1_1": 0.62, "jugada1_0": 0.75, "jugada1_1": 1.12, "jugada1_2": 0.72, "jugada1_3": 1.04, "jugada1_4": 0.99, "jugada1_5": 0.94, "jugada2_1": 0.75, "jugada2_3": 0.86, "jugada2_4": 0.87, "jugada2_5": 0.81, "jugada2_6": 0.66, "jugada3_1": 0.96, "jugada3_2": 0.48, "jugada3_3": 0.71, "jugada3_4": 0.77, "jugada3_5": 0.84, "jugada3_6": 0.88, "jugada4_2": 0.46, "jugada4_3": 0.69, "jugada4_4": 1.13, "jugada4_5": 0.84, "jugada4_6": 0.47, "jugada4_rep_1": 0.73, "curva1_0": 0.77, "draft2_1": 0.8, "draft2_2": 0.89, "jugada5_0": 0.72, "jugada5_1": 0.58, "jugada6_0": 0.72, "jugada6_2": 0.69, "jugada6_3": 0.67, "jugada6_4": 0.61, "jugada6_5": 0.96, "jugada6_rep_0": 0.69, "jugada7_1": 0.76, "claves_1": 1.01, "claves_2": 0.82, "claves_3": 0.78, "numeros_1": 0.68, "sigue_0": 0.67, "sigue_2": 0.6, "cierre_0": 1.2}

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
    escenas={
        "gancho": ("cold open, victory hit then driving pulse, champions' swagger", 6),
        "juego": ("steady informative groove, stakes rising", 4),
        "camino": ("road-so-far montage groove, proud then a stumble then resolve", 5),
        "draft1": ("draft-phase tension, ticking pulse, cards being dealt", 4),
        "jugada1": ("analysis bed: minimal pulse, ticking hi-hats, unease, the underdog strikes first", 6),
        "jugada2": ("analysis bed building to an explosive triumphant swell", 7),
        "jugada2_rep": ("slow-motion replay, suspended, then a reflective resolve", 3),
        "jugada3": ("analysis bed, dark and threatening, the tide turns against the favourite", 6),
        "jugada3_rep": ("slow-motion replay, suspended, ominous", 3),
        "jugada4": ("do-or-die suspense building to a heroic explosive climax", 8),
        "jugada4_rep": ("slow-motion replay, suspended, then a triumphant afterglow", 3),
        "curva1": ("reflective rollercoaster recap, rising and falling synth line", 4),
        "draft2": ("draft-phase tension, confident pulse", 4),
        "jugada5": ("analysis bed, quick and punchy, confident", 5),
        "jugada5_rep": ("slow-motion replay, suspended, confident", 3),
        "jugada6": ("analysis bed, crushing momentum, big hits", 7),
        "jugada6_rep": ("slow-motion replay, suspended, then a reflective resolve", 3),
        "jugada7": ("closing out, victorious drive", 5),
        "jugada7_rep": ("slow-motion replay, triumphant afterglow", 3),
        "claves": ("tactical summary groove, focused and punchy", 5),
        "numeros": ("confident stat-card groove", 5),
        "sigue": ("forward-looking build toward the playoffs, hopeful and epic", 5),
        "cierre": ("final big hit and ring out", 4),
    },
    tramos=[
        (["gancho", "juego", "camino", "draft1"], "Begin with an impact hit and champions' swagger, then a steady groove, a proud road-so-far, then tense draft-phase ticking."),
        (["jugada1", "jugada2"], "Uneasy minimal analysis pulse, then building to an explosive triumphant swell."),
        (["jugada2_rep", "jugada3", "jugada3_rep"], "Suspended slow-motion afterglow, then a dark threatening analysis bed, then an ominous suspended replay."),
        (["jugada4", "jugada4_rep", "curva1"], "Do-or-die suspense building to a heroic explosive climax, then a triumphant afterglow and a reflective rollercoaster recap."),
        (["draft2", "jugada5", "jugada5_rep"], "Confident draft pulse, quick punchy analysis, then a suspended confident replay."),
        (["jugada6", "jugada6_rep", "jugada7"], "Crushing momentum with big hits, a suspended replay, then a victorious closing drive."),
        (["jugada7_rep", "claves", "numeros", "sigue", "cierre"], "Triumphant afterglow, focused tactical summary, confident stat groove, epic forward-looking build and a final big hit and ring out."),
    ])
# Tramos EN VIVO (narración original en español, vivos_audio.py → audio/ambiente.wav): la música baja 16 dB para oírla.
_VIVOS = [(124.36, 141.58), (196.36, 216.61), (312.0, 329.25), (410.18, 431.43), (569.45, 586.71), (654.55, 674.6),
          (754.91, 770.99)]
MEZCLA = dict(musica_curva=[(0, 0)] + [p for a, b in _VIVOS for p in ((a, 0), (a + 1.5, -16), (b - 1.0, -16), (b + .5, 0))]
              + [(1000, 0)])

ESCENAS = [
    # ── GANCHO (~45 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "[excited] Esta tarde, T1 y Movistar KOI se jugaron un boleto a los cuartos de final del Mundial.",
        "Y fue una serie con de todo: un arranque que nadie esperaba, un dragón robado en el peor momento… y una pelea que lo decidió todo.",
        "[short pause] Hoy analizamos las mejores jugadas de la serie, pausa por pausa: dónde estaba cada jugador, qué quería hacer… y por qué salió como salió.",
    ]},
    # ── LO QUE ESTABA EN JUEGO (~35 s) ─────────────────────────────────────────────────────────────────────────────────
    {"id": "juego", "pre": 0.5, "frases": [
        "Primero, lo que estaba en juego. En la fase suiza, con tres victorias pasas a cuartos; con tres derrotas, te vas a casa.",
        "T1 y KOI llegaban con dos victorias y una derrota, y las dos derrotas, contra el mismo equipo: Dplus KIA. El que ganara hoy, a cuartos de final.",
        "Al mejor de tres, con Fearless Draft: un campeón que ya se usó en la serie no se puede volver a elegir.",
    ]},
    # ── CÓMO LLEGARON (~45 s; lol_worlds_2026/guion.py, cfo_kc_worlds/investigacion) ───────────────────────────────────
    {"id": "camino", "pre": 0.6, "frases": [
        "Cómo llegaron. T1, el campeón de los últimos tres Mundiales, va por algo que nadie ha hecho: el cuarto seguido. Debutó despachando a Los Grandes, de Brasil, en veinticuatro minutos.",
        "Después perdió con Dplus KIA, en una pelea por el dragón ancestral que se le volteó de la nada. Y se recuperó ganándole a CTBC Flying Oyster.",
        "KOI, el equipo español de Ibai y Piqué, arrancó ganándole a Bilibili Gaming en una partida apretadísima, y después a CTBC Flying Oyster, diecinueve a siete.",
        "Pero a KOI también lo frenó Dplus KIA: dos a cero, con un pentakill de Smash en la primera partida.",
    ]},
    # ── PARTIDA 1: DRAFT (~30 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "draft1", "pre": 0.6, "frases": [
        "Partida uno. T1, del lado azul: Doran con Ambessa, Oner con Lee Sin, Faker con Syndra, Peyz con Xayah y Keria con Nautilus.",
        "KOI, del lado rojo: Myrwn con Gnar, Elyoya con Qiyana, Jojopyun con Akali, Supa con Kai'Sa y Alvaro con Alistar.",
    ]},
    # ── JUGADA 1 · el arranque de KOI: 1.ª sangre a Faker (05:44, g1_j1) + doble de Elyoya (08:17-08:23, g1_j2; en vivo) ──
    {"id": "jugada1", "pre": 17.0, "frases": [
        "[short pause] Rebobinemos al principio. Minuto cinco. Jojopyun, con Akali, ya le había quemado el Destello a Faker un poco antes.",
        "Pausa. Faker está en el río, sin Destello… y por abajo viene Alvaro, el soporte de KOI, desde la jungla. Nadie en T1 lo ve venir.",
        "Lo acorralan entre los dos… y primera sangre para KOI: Jojopyun sobre Faker. Sin Destello, como dijeron los narradores, ya no había nada que hacer.",
        "Minuto ocho. Pausa otra vez. Ahora el que entra es Elyoya, con Qiyana, a la jungla de T1… donde T1 no tiene ni una guardia.",
        "[excited] Con el combo de Alistar y Qiyana derriten a Oner… y seis segundos después cae Peyz. ¡Tres a cero para KOI, y mil setecientos de oro arriba!",
        "Ese era el plan de KOI: castigar cada rincón del mapa sin visión. Y le estaba saliendo.",
    ]},
    # ── JUGADA 2 · la pelea de T1: 5 por 1 + Barón (21:42-22:33, g1_j3) ───────────────────────────────────────────────
    {"id": "jugada2", "pre": 20.0, "post": 4.0, "frases": [
        "Rebobinemos. Minuto veintiuno. T1 ya se había recuperado: siete asesinatos contra seis. Pero el oro sigue siendo de KOI, por apenas doscientos.",
        "Pausa. Mira a Doran, con Ambessa: se lanza sobre Alvaro, el soporte de KOI. Esa entrada es la que abre todo.",
        "Ambessa es un campeón hecho para eso: entra, aguanta el golpe y sale. Y detrás de Doran, su equipo está listo para seguirlo.",
        "Faker remata a Alvaro… pero KOI tenía una carta guardada: Jojopyun usa su Teleportación y aparece en la pelea.",
        "Pausa otra vez. Jojopyun y Myrwn se van sobre Faker, y Faker cae. Pero mira a Doran: en ese mismo segundo, se cobra a Jojopyun.",
        "Y desde ahí, todo es de T1. Oner remata a Elyoya, que llegó tarde a la pelea, y Doran caza a Supa. Cinco por uno.",
        "[excited] T1 va directo al Barón… lo asegura con mil cuatrocientos de vida… ¡y de regalo, dos asesinatos más!",
    ]},
    {"id": "jugada2_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. Doran entra primero, se come todo el daño… y no muere. En cincuenta segundos, T1 pasa de ir doscientos abajo a tres mil doscientos arriba.",
        "Cuatro minutos después, la ventaja ya era de casi seis mil. La partida parecía cerrada.",
    ]},
    # ── JUGADA 3 · KOI roba el dragón del alma y gana la pelea 3 por 1 + Barón (33:51-34:42, g1_j4) ─────────────────────
    {"id": "jugada3", "pre": 17.0, "frases": [
        "Pero esta partida tenía otra vuelta. Minuto treinta y tres. T1 va tres mil cuatrocientos arriba, con tres dragones. Si toma el cuarto, se queda con el alma.",
        "Pausa. T1 está en el foso del dragón infernal… y Myrwn, con Gnar, espera el momento exacto para robarlo.",
        "[excited] ¡Y se lo roba! Myrwn se queda con el dragón… y no hay alma para T1.",
        "Pausa. Ahora mira la pelea. Alvaro conecta su control sobre Faker, y Myrwn se transforma en Mega Gnar y deja servido a medio equipo.",
        "Y mira a Supa, con Kai'Sa: nadie de T1 llega hasta él. Los narradores lo dijeron: lo dejaron libre.",
        "Supa hace un doble: Oner y Peyz. Myrwn remata a Keria. Tres por uno para KOI.",
        "Y medio minuto después, KOI toma su Barón. Con él tira tres torres… y la ventaja de T1 se esfuma: ahora es KOI el que va dos mil arriba.",
    ]},
    {"id": "jugada3_rep", "pre": 8.5, "frases": [
        "Mírala en cámara lenta. El dragón está a tres mil de vida, T1 lo está tirando… y el último golpe es de Myrwn. Ese robo le dio a KOI la pelea, y después el Barón.",
    ]},
    # ── JUGADA 4 · la pelea del alma: Doran entra, 5 por 0 y nexo (39:09-39:55, g1_j5) ★ jugada clave ──────────────────
    {"id": "jugada4", "pre": 21.0, "post": 4.0, "frases": [
        "Rebobinemos. Minuto treinta y nueve. KOI va mil quinientos arriba… y aparece otra vez el dragón. Si T1 lo toma, alma.",
        "Pausa. Los narradores lo dijeron: si esta pelea termina en exterminio, se acaba la partida. Mira dónde está cada uno.",
        "Y un detalle: el Barón de KOI ya se había terminado. KOI tiene más oro… pero ya no tiene ese empujón.",
        "Pausa otra vez. Doran se lanza con todo, antes de que KOI se acomode. El mismo jugador que abrió la pelea del minuto veintiuno.",
        "Doran mata a Supa… y en el siguiente segundo, T1 asegura el dragón. ¡Alma para T1!",
        "Faker atrapa a Jojopyun, Peyz a Alvaro, Doran a Elyoya… y Oner caza al último, Myrwn. Cinco por cero.",
        "[excited] Sin nadie de KOI en pie, T1 entra a la base… ¡y cae el nexo! Uno a cero para T1.",
    ]},
    {"id": "jugada4_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. Doran terminó la partida con seis asesinatos y cero muertes. Y las dos peleas que decidieron la partida las abrió él.",
        "KOI hizo casi todo bien: el arranque, el robo, el Barón. Pero perdió las dos peleas grandes… y contra T1, eso no perdona.",
    ]},
    # ── LA PARTIDA 1 EN ORO (~25 s; datos_g1.md § curva de oro) ─────────────────────────────────────────────────────────
    {"id": "curva1", "pre": 0.6, "frases": [
        "Así se ve la partida uno en oro: KOI arriba mil setecientos en el minuto nueve. T1 arriba casi seis mil en el veintiséis. KOI otra vez arriba, dos mil, en el treinta y siete…",
        "Y la pelea del alma, que lo voltea todo en cuarenta segundos. Tres vueltas de marcador en una sola partida.",
    ]},
    # ── PARTIDA 2: DRAFT (~30 s) ───────────────────────────────────────────────────────────────────────────────────────
    {"id": "draft2", "pre": 0.6, "frases": [
        "Partida dos. Por el Fearless, ninguno de esos diez campeones se puede repetir.",
        "T1 vuelve al lado azul: Doran con Gwen, Oner con Jarvan Cuarto, Faker con Orianna, Peyz con Jhin y Keria con Karma.",
        "KOI: Myrwn con Ornn, Elyoya con Xin Zhao, Jojopyun con Viktor, Supa con Ezreal y Alvaro con Seraphine.",
    ]},
    # ── JUGADA 5 · la caza en la jungla de T1: 3 por 0 (08:50-09:18, g2_j1) ────────────────────────────────────────────
    {"id": "jugada5", "pre": 17.0, "frases": [
        "Rebobinemos. Minuto ocho. Doran ya le sacaba treinta súbditos y un nivel a Myrwn… y Peyz lo había matado bajo su propia torre.",
        "Pausa. KOI acaba de tomar las larvas… y Elyoya, con Xin Zhao, se mete a robar en la jungla de T1. Alvaro va a su lado, y se confían.",
        "Keria y Doran le caen encima. Doran remata a Elyoya.",
        "Pausa otra vez. Alvaro intenta escapar por el río… pero Keria, con Karma, lo alcanza. Segundo asesinato.",
        "[excited] Supa quema su Destello para salvarse… y Doran lo caza igual. ¡Tres por cero, y tres mil de oro antes del minuto diez!",
        "Los narradores lo dijeron en ese momento: la partida ya estaba más o menos cocinada para T1.",
    ]},
    {"id": "jugada5_rep", "pre": 8.5, "frases": [
        "Otra vez, en cámara lenta. Elyoya entró a robar, Alvaro lo siguió… y ninguno de los dos salió. Tres muertes en diecisiete segundos.",
    ]},
    # ── JUGADA 6 · el exterminio en el foso del dragón: 5 por 0 (19:05-19:41, g2_j2) ★ ─────────────────────────────────
    {"id": "jugada6", "pre": 20.0, "post": 4.0, "frases": [
        "Minuto diecinueve. T1 va cinco mil seiscientos arriba, y aparece el dragón infernal. T1 lo empieza… y KOI espera la Teleportación de Myrwn.",
        "Pausa. Mira a Oner, con Jarvan Cuarto: se lanza hacia adelante, solo… y queda en mala posición. Es la carnada perfecta.",
        "KOI muerde: Alvaro lanza su definitiva, Jojopyun entra… y todos van por Oner.",
        "Pausa otra vez. Pero mira a Faker, con Orianna: viene por el flanco, por donde nadie lo espera.",
        "Y mira a Supa: el foco de T1 también va sobre él. Con Ezreal, no puede pegar libre ni un segundo.",
        "[excited] Oner atrapa a Jojopyun, Doran a Supa, Keria a Alvaro, Peyz a Elyoya… ¡y Faker cierra con Myrwn! Exterminio. Y Oner, el que iba a morir, sobrevive.",
        "T1 se queda con el dragón… y un minuto después, la ventaja ya pasa de los diez mil de oro.",
    ]},
    {"id": "jugada6_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. KOI fue a por la carnada… y la carnada era Oner. Cinco muertes, y ninguna de T1.",
    ]},
    # ── JUGADA 7 · el final: 5 por 1 y nexo sin esperar el alma (24:48-25:40, g2_j3) ─────────────────────────────────
    {"id": "jugada7", "pre": 16.0, "frases": [
        "Minuto veinticinco. T1 tiene tres dragones y espera el alma. Faker conecta su Onda de choque, Doran entra con todo… y otro exterminio: cinco por uno.",
        "Solo cae Oner, otra vez el que entra primero. El resto de KOI, como dijeron los narradores, explota.",
        "[excited] T1 ni siquiera espera el alma: va directo a la base… y cae el nexo. ¡T1 gana dos a cero y está en los cuartos de final!",
    ]},
    {"id": "jugada7_rep", "pre": 8.5, "frases": [
        "Mírala otra vez. Faker termina con un doble, Peyz cierra el exterminio… y KOI ya no se vuelve a levantar.",
    ]},
    # ── LAS CLAVES (~40 s) ──────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "claves", "pre": 0.6, "frases": [
        "¿Qué decidió la serie? Tres claves.",
        "Uno: Doran. Abrió las dos peleas que decidieron la primera partida… y en toda la serie no murió ni una vez.",
        "Dos: las peleas grandes. KOI ganó el arranque y robó el dragón del alma, pero las peleas de cinco contra cinco que valían un Barón, un alma o la partida… fueron de T1.",
        "Tres: la jungla. En la primera partida, KOI castigó la jungla de T1 sin guardias. En la segunda, fue Elyoya el que se metió a robar a la jungla de T1… y lo pagó caro.",
    ]},
    # ── LOS NÚMEROS (~45 s) ────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "numeros", "pre": 0.6, "frases": [
        "Los números de la serie. El dato más loco es de Doran, el top de T1: diez asesinatos, trece asistencias… y cero muertes en las dos partidas.",
        "Keria estuvo en treinta asistencias, y Peyz, con Jhin, terminó la segunda partida con ocho asesinatos y una sola muerte.",
        "Y en la segunda partida, KOI no derribó ni una torre ni tomó un solo dragón. T1 terminó con más de doce mil de oro de ventaja.",
    ]},
    # ── QUÉ SIGUE (~40 s) ──────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "sigue", "pre": 0.6, "frases": [
        "¿Y ahora? T1 queda tres y uno, y espera rival para los cuartos de final, al mejor de cinco, del tres al seis de noviembre.",
        "En el sorteo, los que terminan tres y uno se cruzan entre sí. Y T1 va por algo que nadie ha hecho jamás: su cuarto título mundial seguido.",
        "KOI queda dos y dos. No está eliminado: el sábado treinta y uno juega la quinta ronda, a muerte. Si gana, a cuartos; si pierde, a casa.",
    ]},
    # ── CIERRE (~20 s) ─────────────────────────────────────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.6, "frases": [
        "[excited] ¿Cuál fue para ti la mejor jugada de la serie? ¿Y tú crees que este T1 puede ganar su cuarto Mundial seguido? Déjalo en los comentarios. Nos vemos en los cuartos.",
    ]},
]
