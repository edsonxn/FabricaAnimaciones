# -*- coding: utf-8 -*-
"""Gen.G vs Bilibili Gaming: todo antes de la GRAN FINAL de la Worlds 2026 (~25 min), canal «Crónicas de ligoleyen»
(subida por Studio; se publica el JUEVES 12-nov; la final es el sábado 14-nov: días por nombre, nunca «hoy» ni «mañana»).
Estilo ANÁLISIS TÁCTICO (docs/estilo_analisis_tactico.md), copia de videos/lol_semana2/ + 3D de videos/lol_worlds_2026/j6_3d.py.
La caída de T1 ya NO es spoiler (el usuario, 10-nov): va en el gancho.

DATOS VERIFICADOS: investigacion/feed_*.txt (feed oficial livestats de las 13 partidas), sched.json/ko_games.json (API LoL Esports),
datos_duelos.md (K/D/A por jugador en eliminatorias), datos_j1..j6.md (cuadros del VOD + narración). Historia: Inven Global
(«primera final en 9 años, desde la era Samsung»), esports.gg (Chovy: semifinales 2022, 2024 y 2025), cara a cara 2023-2024
(Inven / bet365 / DPM): 2023 BLG elimina a Gen.G en el MSI y en cuartos del Mundial (3-2); 2024 Gen.G gana dos veces en el MSI,
final incluida (3-1). Ruler campeón 2017 (Samsung Galaxy), Canyon 2020 (DAMWON), Viper 2021 (EDG, último título chino).
Comentarios (investigacion/comentarios.json, 8-10 nov): la queja n.º 1 de los dos últimos videos es la VOZ («estaba mejor la
primera voz»): vuelve JC, la de siempre. Sin [excited] ni [whispers].
"""
import json as _json
import os as _os

_D = _os.path.dirname(_os.path.abspath(__file__))
TITULO = "Gen.G vs BLG: todo lo que debes saber antes de la GRAN FINAL"
ARCHIVO = "lol_final_previa"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español): la «primera voz» que pidió la gente
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.6)
FONETICA = _json.load(open(_os.path.join(_D, "investigacion", "fonetica_lista.json"), encoding="utf-8"))
# tomas oídas/leídas y aceptadas (solo nombres que Whisper escribe distinto: «Jenji», «Billy Billy»): voz_aceptada.json
_ACE = _json.load(open(_os.path.join(_D, "voz_aceptada.json"), encoding="utf-8")) if _os.path.exists(_os.path.join(_D, "voz_aceptada.json")) else {}
CER_MAX_POR_FRASE = {k: v[0] for k, v in _ACE.items()}
TAIL_MAX_POR_FRASE = {k: v[1] for k, v in _ACE.items()}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="fade",
    fundido=0.25,
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="League of Legends Worlds 2026", min_s=30, max_min=400, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 80
LYRIA = dict(
    estilo="Modern esports broadcast analysis score: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "stadium-sized hits and tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={},
    tramos=[(["gancho", "voz", "final", "final_publico"], "Apertura de la final: tensa, expectante, estadio."),
            (["gen_suiza", "gen_lyon", "j1", "lyon_p1", "lyon_p2"], "Gen.G arrolla: pulso firme de análisis."),
            (["gen_ig", "ig_p1", "ig_p2", "j3_ctx"], "Semifinal de Gen.G: dominio y luego problemas."),
            (["j3", "j3_fin", "ig3_cierre"], "La remontada de Ruler: tensión que sube y triunfo."),
            (["blg_suiza", "blg_dk", "j2", "dk_p2", "dk_p3"], "El camino largo de BLG: urgente, por la puerta de atrás."),
            (["t1_ctx", "t1_p1", "j4", "faker_p2"], "BLG contra T1: choque de gigantes, vaivén."),
            (["j5", "j6_ctx", "j6"], "La caída de T1: oscuro, decisivo."),
            (["j6_fin", "t1_com", "numeros"], "Fin de una era: emotivo y luego analítico."),
            (["duelos_intro", "duelo_top", "duelo_jungla", "duelo_mid", "duelo_adc", "duelo_sup", "campeones"], "Cara a cara: duelo, pulso constante."),
            (["historia", "claves", "pronostico", "cierre"], "Historia y claves: épico contenido hacia la final.")])
ESPACIOS_VOZ = {}

ESCENAS = [
    # ── GANCHO (~55 s): la caída de T1 y la final ────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "Domingo. Semifinal. Cuarta partida. T1 empuja con el Barón, al que le quedan dos segundos, y está a menos de quinientos de oro de empatar una partida que llegó a ir perdiendo por seis mil.",
        "En nueve segundos, Oner, Doran y Faker están muertos. [short pause] Y con esa pelea se terminó la era de T1: tres Mundiales seguidos, y el cuarto se queda en semifinales.",
        "El sábado, en Nueva York, la final es otra. Gen.G contra Bilibili Gaming. Uno no llegaba a una final desde hace nueve años. El otro perdió la última que jugó, por una sola partida.",
        "En este video: el camino de los dos hasta Nueva York, las jugadas que los trajeron, varias de ellas en 3D, el cara a cara posición por posición, y lo que puede decidir la final.",
    ]},
    # ── LA VOZ (~25 s): la queja n.º 1, corregida ────────────────────────────────
    {"id": "voz", "pre": 0.5, "frases": [
        "Antes, algo que nos pidieron ustedes. Karen escribió: estaba mejor la primera voz. Diez personas le dieron la razón, y Luis lo dijo más directo: regresen la voz anterior.",
        "Mensaje recibido. La voz de siempre está de vuelta. Todos los comentarios se leen, y este video se hizo con ellos.",
    ]},
    # ── LA FINAL (~40 s) ─────────────────────────────────────────────────────────
    {"id": "final", "pre": 0.5, "frases": [
        "La gran final se juega el sábado catorce de noviembre en el Barclays Center de Brooklyn. Al mejor de cinco: el primero que gane tres partidas es campeón del mundo.",
        "Empieza a la una de la tarde en el centro de México, a las cuatro en Argentina y a las ocho de la noche en España.",
        "Y hay más en juego que un trofeo. Si gana Gen.G, Corea suma su quinto Mundial seguido. Si gana Bilibili, China vuelve a ser campeona por primera vez desde dos mil veintiuno.",
    ]},
    # ── NUEVA (ampliación 11-nov): el público y el escenario ─────────────────────
    # fuente: r_escenario t 0-33 (VOD J14ZB3Yut18 453-486, previa de IG-GEN P1, semifinal en Texas; sin HUD)
    #   _0 → t 4 (cartel «See you in NY» entre logos de IG y «GEN») · _1 → t 4 y t 6-10 (carteles con logo de IG, «GEN»/«GENG», «WEI WIN»)
    #   · _2 → t 0-2 (cabinas + splash en las pantallas) y t 26-33 (estadio a oscuras, pantalla gigante «MAKE» / «NOISE»)
    {"id": "final_publico", "pre": 2.0, "post": 5.0, "frases": [
        "Y la gente ya lo estaba esperando. En la semifinal de Gen.G, en Texas, uno de los carteles del público decía, en inglés: nos vemos en Nueva York.",
        "Había carteles de Invictus, de Gen.G, y hasta uno que pedía que ganara Wei.",
        "Las dos cabinas, los campeones elegidos en las pantallas, y el estadio entero a oscuras, con un solo mensaje en la pantalla gigante: hagan ruido.",
    ]},
    # ── GEN.G: EL CAMINO ─────────────────────────────────────────────────────────
    {"id": "gen_suiza", "pre": 0.6, "frases": [
        "Primero, Gen.G. En la fase suiza no perdió una sola serie: le ganó a Invictus, a Hanwha Life y a LYON. Tres de tres, directo a cuartos.",
        "Y en eliminatorias, todavía mejor. Seis partidas jugadas. Seis ganadas.",
        "Y el que más pesa es su tirador, Ruler: treinta y ocho asesinatos en esas seis partidas, más que nadie en el equipo. Nueve en una sola partida contra Invictus. Acuérdate de ese nombre, porque va a salir mucho en este video.",
    ]},
    {"id": "gen_lyon", "pre": 0.5, "frases": [
        "En cuartos, el miércoles cuatro de noviembre, otra vez LYON, la organización mexicana a la que ya le había ganado en la fase suiza. Gen.G ganó las dos primeras diecinueve a ocho y veintidós a seis. En la segunda, Ruler hizo ocho asesinatos.",
        "La tercera fue la única en la que LYON le pegó de verdad: ganó dos peleas seguidas y en el minuto veinte tenía más asesinatos que Gen.G.",
    ]},
    {"id": "j1", "pre": 8.0, "post": 3.0, "frases": [
        "Minuto veinticinco. Gen.G acaba de llevarse el dragón infernal. Mira a Ruler, con Xayah.",
        "Inspired entra solo sobre Canyon. Y Chovy, con Taliyah, levanta un muro que parte el río en dos.",
        "Inspired. Isles. Berserker. Tres asesinatos de Ruler en doce segundos, sin que caiga nadie de Gen.G.",
        "Gen.G empieza el Barón, y siete minutos después cierra la serie tres a cero.",
    ]},
    # ── NUEVA: GEN-LYON partida 1 (solo números del feed: MG a pantalla completa, SIN VOD: no hay clip de la P1) ──
    # fuente: feed_116 (2.ª línea 01:49: LYON Berserker → Duro = primera sangre de LYON; «final 19 8»; asesinatos: Canyon 6, Kiin 6)
    {"id": "lyon_p1", "pre": 0.5, "frases": [
        "Antes de pasar a semifinales, las otras dos partidas de esa serie. La primera, diecinueve a ocho. La primera sangre fue de LYON, pero Canyon y Kiin terminaron con seis asesinatos cada uno.",
    ]},
    # ── NUEVA: GEN-LYON partida 2, la pelea final (Ruler doble, Chovy doble, sin bajas) ──
    # fuente: r_lyon2 t 0-46 (HUD = t + 1541; feed_117 26:11-26:22, feed − HUD ≈ +3)
    #   pre = VIVO t 0-5 · _0 → t 0 (HUD 25:41: 17-6, 55,4K/47,0K = +8,4K, BARON POWERPLAY) · _1 → t 3-21 («Red turret destroyed!» t 15,
    #   pelea frente al inhibidor t 18-21) · _2 → t 26 (Ruler/Ashe → Inspired), t 27-28 (Chovy → Dhokla), t 35-37 (DOUBLE KILL Ruler → Isles)
    #   · _3 → t 38-40 (DOUBLE KILL Chovy/Viktor → Saint; 22-6 en 26:20) · post = t 40-46 (cámaras de los 5 de GEN y de LYON)
    {"id": "lyon_p2", "pre": 5.0, "post": 6.0, "frases": [
        "La segunda, la de los ocho asesinatos de Ruler. Minuto veinticinco: Gen.G tiene el Barón, y va ocho mil cuatrocientos de oro arriba.",
        "Entra a la base de LYON. Cae la torre, y la pelea se arma frente al inhibidor.",
        "Primero cae Inspired, a manos de Ruler, que juega con Ashe. Chovy se lleva a Dhokla. Y Ruler alcanza a Isles: doble.",
        "Chovy, con Víktor, hace su propio doble con Saint. Veintidós a seis, y ninguna baja de Gen.G en toda la pelea.",
    ]},
    {"id": "gen_ig", "pre": 0.5, "frases": [
        "En semifinales, el sábado siete, en Texas, Invictus Gaming, el equipo de TheShy y de Rookie, que venía de eliminar a Top Esports. Las dos primeras no tuvieron historia: veintinueve a nueve y veintisiete a nueve. Cincuenta y seis asesinatos de Gen.G contra dieciocho.",
        "La tercera es la mejor partida de Gen.G en todo el Mundial. Y no porque la dominara: porque la iba perdiendo.",
    ]},
    # ── NUEVA: GEN-IG partida 1, el cierre con ACE ───────────────────────────────
    # fuente: r_ig1 t 0-44 (HUD = t + 1978; feed_128 33:13-33:35, feed − HUD ≈ +3)
    #   _0 → t 0 (HUD 32:58: «GEN Ruler has destroyed a red inhibitor!», 24-6, +14,8K) · _1 → t 3-9 (IG defiende las torres del nexo),
    #   t 10,5 (SHUT DOWN JiaQi → Kiin), t 20 (Canyon → JiaQi), t 22-23 (Ruler → TheShy), t 25-26 (Chovy → Meiko)
    #   · _2 → t 28-32 (SHUT DOWN Wei → Duro, Wei → Canyon), t 34-36,5 («ACE!» junto al nexo) · _3 → 24-6 → 29-9 en el HUD, t 36
    #   (Ruler celebra con el brazo arriba en su cámara), t 43,5 («GEN VICTORY!» GEN 1-0 IG) · post = t 37-44 (escenario)
    {"id": "ig_p1", "pre": 0.5, "post": 5.0, "frases": [
        "Pero antes, mira cómo se ganaron las dos primeras. Primera partida, minuto treinta y tres. Gen.G va catorce mil ochocientos arriba, y Ruler acaba de tirar un inhibidor.",
        "Invictus defiende frente a las torres del nexo. JiaQi se cobra a Kiin. Pero Canyon mata a JiaQi, Ruler a TheShy, y Chovy a Meiko.",
        "Wei todavía se lleva a Duro y a Canyon. No le alcanza: cae todo Invictus junto al nexo.",
        "Cinco por tres en la última pelea. Ruler levanta el brazo, y Gen.G se pone uno a cero.",
    ]},
    # ── NUEVA: GEN-IG partida 2, la pelea del dragón hextech ─────────────────────
    # fuente: r_ig2 t 0-42 (HUD = t + 1350; feed_129 22:43-23:05, feed − HUD ≈ +2-3)
    #   pre = VIVO t 0-4 · _0 → t 0-6 (HUD 22:30: 12-5, 44,2K/37,8K = +6,4K, BARON POWERPLAY, río junto al foso del dragón)
    #   · _1 → t 8-9,5 (Chovy/Ahri → Meiko), t 18-19 («Blue team has slain the Hextech Drake!») · _2 → t 20-22 (SHUT DOWN TheShy/Rumble
    #   → Chovy), t 23-24 (TheShy → Ruler), t 25-27 (Ruler → JiaQi) · _3 → t 28-29 (Kiin/Gwen → Wei), t 31-32 (DOUBLE KILL Kiin → Rookie)
    #   · _4 → t 34-36 («ACE!» en la jungla de IG), t 37-38 (Canyon → TheShy), 17-7 en el HUD · _5 → feed_129 fin 29:10 (27-9)
    {"id": "ig_p2", "pre": 4.0, "post": 2.0, "frases": [
        "Segunda partida, minuto veintidós. Gen.G otra vez con el Barón, seis mil cuatrocientos arriba, y la pelea, junto al foso del dragón hextech.",
        "Chovy, con Ahri, abre con Meiko. Y Gen.G se lleva el dragón.",
        "TheShy, con Rumble, se cobra a Chovy y a Ruler. Pero Ruler también se lleva a JiaQi.",
        "Y entra Kiin, con Gwen: Wei, y después Rookie. Doble.",
        "Canyon remata a TheShy, y cae el equipo entero de Invictus, en su propia jungla. Diecisiete a siete.",
        "Seis minutos después, Gen.G se pone dos a cero. Y llega la tercera.",
    ]},
    {"id": "j3_ctx", "pre": 0.5, "frases": [
        "Minuto diecinueve: Invictus va diez a tres en asesinatos, y llegó a ir cuatro mil seiscientos de oro arriba. Rookie, con Locke, ya lleva seis.",
        "Gen.G aguanta. En el minuto veintiséis todavía va trece a seis abajo.",
    ]},
    {"id": "j3", "pre": 6.0, "post": 3.0, "frases": [
        "Minuto treinta. Invictus va a por su cuarto dragón, el del alma. Vamos a verla en el mapa, desde arriba.",
        "Canyon se lo roba. E Invictus queda partido en dos: Kiin aparece por la espalda y entretiene a Rookie y a TheShy.",
        "Ahora vuelve al video. Ruler mata a Meiko. Después a JiaQi, el tirador de Invictus. Y a Wei: triple.",
        "Medio minuto después cae TheShy. Cuatro asesinatos de Ruler en cuarenta y seis segundos.",
        "Y tres segundos después, Gen.G se lleva el Barón. Invictus iba casi tres mil de oro arriba. Ahora el que va mil cuatrocientos arriba es Gen.G.",
    ]},
    {"id": "j3_fin", "pre": 0.5, "post": 2.0, "frases": [
        "Invictus todavía ganó otra pelea, y la partida llegó al minuto cuarenta. En la última, Gen.G gana cuatro a cero y entra a la base.",
        "Tres a cero. Gen.G, de vuelta en una final por primera vez desde dos mil diecisiete, cuando todavía se llamaba Samsung Galaxy.",
    ]},
    # ── NUEVA: la última pelea de la semifinal y la celebración de Gen.G ─────────
    # fuente: r_ig3fin t 0-103 (HUD = t + 2342; feed_130 39:16-40:08, feed − HUD ≈ +4-5; IG azul: en el HUD IG va a la IZQUIERDA)
    #   _0 → t 0 (HUD 39:01: IG 18 – GEN 12, oro 70,8K/72,7K = GEN +1,9K) · _1 → t 9-11 («GEN Ruler has slain IG JiaQi!», Yunara → Ezreal),
    #   t 13-15 («GEN Kiin has slain IG TheShy!», Camille → Gnar), t 17-18 (DOUBLE KILL Kiin → Meiko) · _2 → t 20-32 (GEN cruza el río),
    #   t 36 y 44 («Blue turret destroyed!»), t 48 («GEN Ruler has destroyed a blue inhibitor!») · _3 → t 61,5-62,5 («GEN Ruler has slain
    #   IG Rookie!» junto al nexo = última línea de feed_130, 40:08; Ruler levanta los brazos en las cámaras) · _4 → t 68 (GEN se abraza),
    #   t 92-100 (los 5 al frente, pantallas «VICTORY» / «GEN.G VICTORY», saludan con los brazos arriba) · post = t 100-103
    #   (j3_fin puede ir sobre la Grieta 3D/oro de j3 o sobre r_ig3fin congelado en t 0: no repetir aquí el mismo tramo a x1)
    {"id": "ig3_cierre", "pre": 0.5, "post": 4.0, "frases": [
        "Así fue esa última pelea. Minuto treinta y nueve: Invictus va dieciocho a doce en asesinatos, pero Gen.G ya está arriba en oro.",
        "Ruler, con Yunara, mata a JiaQi. Kiin, con Camille, se lleva a TheShy, y después a Meiko: doble.",
        "Gen.G cruza el río, tira las torres, y Ruler rompe un inhibidor.",
        "Y el último asesinato de la semifinal también es suyo: Rookie, junto al nexo. En las cámaras, Ruler levanta los brazos.",
        "Gen.G se abraza en el escenario. Los cinco caminan al frente, con las pantallas encendidas, y saludan con los brazos arriba.",
    ]},
    # ── BLG: EL CAMINO ───────────────────────────────────────────────────────────
    {"id": "blg_suiza", "pre": 0.6, "frases": [
        "El camino de Bilibili fue mucho más largo. Empezó la fase suiza perdiendo contra Movistar KOI.",
        "Le ganó a Team Liquid y a Karmine, perdió contra Top Esports después de ir cinco mil arriba, y tuvo que jugarse el Mundial contra Hanwha Life. Ganó dos a cero, con un cuádruple de Knight.",
        "Tres victorias y dos derrotas. Entró a cuartos por la puerta de atrás. Y desde ahí, se transformó.",
    ]},
    {"id": "blg_dk", "pre": 0.5, "frases": [
        "Cuartos, jueves cinco de noviembre, contra Dplus KIA, uno de los dos equipos que había pasado invicto la fase suiza.",
        "Bilibili lo despachó tres a cero. Y la pelea que marcó la serie llegó en el minuto dieciséis de la primera partida.",
    ]},
    {"id": "j2", "pre": 8.0, "post": 3.0, "frases": [
        "Minuto dieciséis. Bilibili se acaba de llevar el Heraldo, y Dplus KIA todavía va un poco arriba en oro. Mira al jungla de Bilibili: Xun, con Naafiri.",
        "Lucid se queda demasiado adelante, y Bin se le echa encima.",
        "Xun remata a Lucid. Bin cae en el intercambio. Y Xun se lleva también a Career: doble asesinato.",
        "ShowMaker escapa con poca vida, y Xun lo persigue hasta la jungla de Bilibili. Tres asesinatos de Xun, y el oro cambia de lado.",
        "Bilibili ya no soltó la serie.",
    ]},
    # ── NUEVA: BLG-DK partida 2, la pelea del río (3 por 2) ──────────────────────
    # fuente: r_dk2 t 0-37,7 (HUD = t + 583; feed_099 10:01-10:11, feed − HUD ≈ +5-6; DESDE t 38,9 ES REPETICIÓN: no usar como vivo)
    #   pre = VIVO t 0-3 · _0 → t 0-3 (HUD 09:43, río inferior junto al foso: ON y Xun contra Lucid y Career)
    #   · _1 → t 6-9 (llegan ShowMaker, Knight, Viper), t 11-13 (Xun → Lucid), t 14-16 (ShowMaker → ON)
    #   · _2 → t 17-19 (Viper → Smash), t 20 (DOUBLE KILL ShowMaker → Xun) · _3 → t 22-24 (DOUBLE KILL Viper → ShowMaker; 3-5 en el HUD)
    #   · _4 → feed_099 «final 10 13» (DK azul; series 24-10, 13-10, 25-9) · post = t 27-30 (calma; plano del público t 27)
    {"id": "dk_p2", "pre": 3.0, "post": 2.0, "frases": [
        "Segunda partida contra Dplus KIA. Minuto nueve, en el río de abajo, junto al foso del dragón. ON y Xun se encuentran con Lucid y Career.",
        "Llegan ShowMaker, Knight y Viper. Xun mata a Lucid. ShowMaker se cobra a ON.",
        "Viper mata a Smash. ShowMaker hace un doble: también cae Xun.",
        "Y Viper lo cierra con ShowMaker. Doble de Viper, y tres por dos para Bilibili.",
        "Fue la partida de marcador más apretado de la serie, y Bilibili la ganó trece a diez.",
    ]},
    # ── NUEVA: BLG-DK partida 3, el nexo y la celebración ────────────────────────
    # fuente: r_dk3fin t 0-57 (HUD = t + 1933; feed_100 32:34-32:36)
    #   _0 → t 0 (HUD 32:13: DK 9 – BLG 22, BARON POWERPLAY, «Blue turret destroyed!», BLG dentro de la base de DK)
    #   · _1 → t 4 («BLG Xun has destroyed a blue inhibitor!»), t 12-15 («BLG Bin has destroyed a blue inhibitor!»); Bin 12 asesinatos,
    #   7 a Siwoo = feed_100 (líneas «K BLG Bin», Bin con Jax) → ficha MG con el dato · _2 → t 21,5-23,5 (recuadro: el nexo cae),
    #   t 27-36 («BLG VICTORY!» BLG 3-0 DK; BLG cruza el escenario y choca puños con DK t 32-36) · post = t 44-57 (pasarela, pantallas
    #   «BILIBILI GAMING», saludan al público)
    {"id": "dk_p3", "pre": 1.0, "post": 10.0, "frases": [
        "Y la tercera, sin discusión. Minuto treinta y dos: Bilibili con el Barón, veintidós a nueve, dentro de la base de Dplus KIA.",
        "Xun tira un inhibidor. Bin, otro. Y Bin, con Jax, terminó esa partida con doce asesinatos. Siete de ellos, sobre Siwoo, el top de Dplus KIA.",
        "Cae el nexo. Tres a cero. Bilibili cruza el escenario y choca los puños con Dplus KIA.",
    ]},
    # ── BLG vs T1 ────────────────────────────────────────────────────────────────
    {"id": "t1_ctx", "pre": 0.6, "frases": [
        "Y llegó la semifinal que todo el mundo quería ver. Domingo ocho de noviembre. Bilibili contra T1, el campeón de los últimos tres Mundiales. La revancha de la final de dos mil veinticuatro, la que Bilibili perdió tres a dos.",
        "La primera fue de Bilibili: dieciocho a seis, con nueve asesinatos de Knight. Faker, con Locke, hizo cuatro, y no alcanzó.",
    ]},
    # ── NUEVA: T1-BLG partida 1, la pelea 4 por 0 con el doble de Knight ─────────
    # fuente: r_t1g1 t 0-46 (HUD = t + 1758; feed_122 29:42-29:55, feed − HUD ≈ +3-5)
    #   pre = VIVO t 0-6 · _0 → t 0 (HUD 29:18: 14-6, 58,5K/53,4K = +5,1K), t 12 (los dos equipos se acercan en la jungla)
    #   · _1 → t 18-19 (Viper → Oner), t 20,5-22 (Knight → Keria), t 24-25 (DOUBLE KILL Knight → Doran)
    #   · _2 → t 30-32 (Xun → Peyz; 18-6 en el HUD), t 33-45 (BLG persigue a Faker, que escapa con poca vida)
    {"id": "t1_p1", "pre": 6.0, "post": 4.0, "frases": [
        "Minuto veintinueve de esa primera partida. Bilibili ya va catorce a seis, cinco mil arriba, y los dos equipos se encuentran en la jungla.",
        "Viper abre con Oner. Y Knight se lleva a Keria y a Doran: doble.",
        "Xun remata a Peyz. Cuatro por cero, y Faker se escapa con lo justo.",
    ]},
    {"id": "j4", "pre": 6.0, "post": 3.0, "frases": [
        "En la segunda, T1 respondió como responde un campeón. Minuto treinta: se lleva el Dragón Ancestral.",
        "Tira las torres del centro, el segundo inhibidor y las torres del nexo.",
        "Y en trece segundos, cinco por cero, con un doble de Faker, con Syndra.",
        "Veintidós a diez, casi diez mil de oro arriba, y T1 empata la serie.",
    ]},
    # ── NUEVA: la jugada de Faker en la partida 2 (alma del océano, Zhonya, teleportación, Knight) ──
    # fuente: j4b t 0-58 (VOD r9-avVeme5o 1830-1900; HUD = t + 1382, medido: t 0 = 23:02, t 30 = 23:32, t 60 = 24:02; feed_123, feed − HUD ≈ +5..+7)
    #   _0 → t 0-11 (HUD 23:02-23:13: 7-6, 44,1K/43,0K = +1,1K, BARON POWERPLAY de T1, 3 dragones de T1 en el HUD) y t 12-15 (tarjeta «DRAGON SOUL»)
    #   · _1 → t 13 («Blue team has stolen the Ocean Drake!»), t 14 («OCEAN DRAKE», 4.º icono) · _2 → t 15-17 («T1 Doran has slain BLG ON!»,
    #   Olaf), t 19 (barra de Faker dorada = Zhonya; narración t 18,9-21,8 «Faker con el reloj de arena de Zhonya, compra muchísimo tiempo»)
    #   · _3 → t 18-20 (DOUBLE KILL Doran → Xun/Qiyana), t 21-22 («BLG Viper has slain T1 Oner!»), t 35-37 («BLG Viper has slain T1 Keria!»)
    #   · _4 → t 36,3 (Faker entra arriba a la derecha; narración t 30,8-32,1 «teleportación, viene Faker»)
    #   · _5 → t 40-41 («T1 Peyz is on a rampage!» = Viper, feed 23:48), t 43-46 (Knight con muy poca vida, Faker detrás), t 46,2
    #   (HUD 23:48 «T1 Faker has slain BLG Knight!»; Faker 1/0/6 en el marcador) · _6 → HUD 7-6 → 11-8 (t 0 → t 46), t 60 (HUD 24:02: 47,5K/45,4K = +2,1K), datos_j4 (Faker 4/0
    #   en la partida) · post = VIVO t 47-57 («…Faker dice ah, ah, ah, y se lleva un asesinato. Faker se las sabía perfectamente…»)
    {"id": "faker_p2", "pre": 0.5, "post": 10.0, "frases": [
        "Pero esa segunda partida tuvo otra jugada que hay que ver, siete minutos antes. Minuto veintitrés. T1 tiene el Barón y tres dragones. El cuarto, el del océano, le da el alma.",
        "Los dos equipos se juntan en el foso. Y T1 se lo roba: el dragón del océano, y con él, el alma.",
        "Doran, con Olaf, mata a ON. Y mira a Faker: su barra se pone dorada. Es el reloj de arena de Zhonya. No le pueden hacer daño, y compra tiempo.",
        "Doran se lleva también a Xun: doble. Viper responde con Oner, y después con Keria.",
        "Y entonces llega Faker, con la teleportación.",
        "Peyz se lleva a Viper. Knight se escapa con muy poca vida. Faker lo sigue, y Syndra lo alcanza. Minuto veintitrés con cuarenta y ocho.",
        "Cuatro por dos para T1, con el alma del océano, y poco después la ventaja ya es de dos mil cien. Faker terminó esa partida sin morir una sola vez. Así lo cantó la transmisión.",
    ]},
    {"id": "j5", "pre": 6.0, "post": 3.0, "frases": [
        "La tercera fue la más pareja: T1 remontó hasta empatar a ocho en el minuto veintidós. Pero en el treinta y dos, con el alma del dragón en juego, Bilibili ya iba cuatro mil arriba.",
        "T1 se mete en el foso del dragón sin visión alrededor. Bilibili lo espera en el río, con el muro de Taliyah.",
        "Knight caza a Oner. Bilibili pierde a Bin, pero Xun mata a Doran, y Bilibili se lleva el alma infernal.",
        "T1 se cobra a Knight y una torre. Y Viper, que ya había resucitado una vez en la pelea, mata a Peyz y a Keria.",
        "Cuatro por dos, el alma del dragón, y Bilibili se pone dos a uno.",
    ]},
    {"id": "j6_ctx", "pre": 0.5, "frases": [
        "Y la cuarta. Bilibili domina desde el principio: diez a tres en el minuto diecisiete, seis mil de oro arriba en el veintiocho.",
        "Pero T1 no se muere. En el minuto veintiocho gana una pelea con dos asesinatos de Faker, y un minuto después se lleva el Barón.",
    ]},
    {"id": "j6", "pre": 6.0, "post": 3.0, "frases": [
        "Minuto treinta y dos. Vamos al mapa.",
        "Con el Barón, T1 se puso a menos de quinientos de oro. Pero al Barón le quedan dos segundos, y T1 sigue empujando por el centro. Cae la torre.",
        "Y aquí está la decisión que lo cambia todo. Oner se lanza sobre Viper. Y Faker se va solo al norte, detrás de Knight y de ON.",
        "Volvemos al video. Viper se salva con el Ángel de la Guarda. Bin entra por arriba, y Xun por abajo. Oner cae. Doran cae. Y Faker.",
        "Tres por cero, sin una sola baja de Bilibili. Y la ventaja vuelve a dos mil quinientos.",
    ]},
    {"id": "j6_fin", "pre": 0.5, "post": 14.0, "frases": [
        "Cinco minutos después, Bilibili toma su propio Barón, gana la última pelea, y cae el nexo.",
        "Tres a uno. T1 se despide del Mundial. Y Bilibili vuelve a una final, dos años después de perder la anterior.",
        "Y estas son las reacciones de Bilibili cuando cae el nexo. Escucha cómo se vivió.",
    ]},
    # ── COMENTARIOS DE T1 ────────────────────────────────────────────────────────
    {"id": "t1_com", "pre": 0.5, "frases": [
        "Rolnesc lo dijo así: le iba a BLG, pero Faker y Keria siempre en su corazón. Así se sintió medio planeta.",
        "Y a igcid, que en el video de cuartos nos dejó: nos vemos para cuando T1 gane el Mundial. [short pause] Aquí seguimos. Nos vemos en dos mil veintisiete.",
    ]},
    # ── NUEVA: los números del camino (MG: tabla/barras con el feed; fondo = r_escenario o el VOD sin acción) ──
    # fuente: líneas «final» de investigacion/feed_*.txt (GEN: 116 19-8, 117 22-6, 118 16-10, 128 29-9, 129 27-9, 130 IG 18-16 GEN;
    #   BLG: 098 24-10, 099 DK 10-13, 100 DK 9-25, 122 18-6, 123 T1 22-10, 124 19-10, 125 T1 9-21) y su 2.ª línea (primera sangre); mayor diferencia: GEN-IG P1 29-9 (+20; BLG máx. 25-9 = +16)
    {"id": "numeros", "pre": 0.6, "frases": [
        "Antes del cara a cara, los números del camino. Sumando los marcadores de sus seis partidas en eliminatorias, Gen.G hizo ciento veintinueve asesinatos. Le hicieron sesenta.",
        "Bilibili jugó una partida más, y llegó a ciento treinta. Le hicieron setenta y seis.",
        "La paliza más grande del camino es de Gen.G: veintinueve a nueve contra Invictus. La única vez que mató menos que su rival fue la tercera contra Invictus: dieciséis contra dieciocho. Y aun así la ganó.",
        "Y la primera sangre no le importa a ninguno de los dos. Gen.G la consiguió en tres de sus seis partidas. Bilibili, en tres de siete. Y entre los dos, perdieron una sola.",
    ]},
    # ── CARA A CARA ──────────────────────────────────────────────────────────────
    {"id": "duelos_intro", "pre": 0.6, "frases": [
        "Ahora, el cara a cara. Estos son los números de cada jugador en las eliminatorias: seis partidas de Gen.G, siete de Bilibili.",
    ]},
    {"id": "duelo_top", "pre": 0.3, "frases": [
        "Arriba, Kiin contra Bin. Kiin murió solo nueve veces en seis partidas. Bin murió diecisiete, pero también es el que más se mete: treinta asesinatos. El que juega seguro contra el que juega al límite.",
    ]},
    {"id": "duelo_jungla", "pre": 0.3, "frases": [
        "En la jungla, Canyon contra Xun. Canyon tiene la mejor marca de su equipo: veintisiete asesinatos, sesenta y cuatro asistencias, diez muertes. Xun, el de la pelea del Heraldo contra Dplus KIA, no se queda lejos: veintinueve asesinatos y sesenta y cinco asistencias.",
    ]},
    {"id": "duelo_mid", "pre": 0.3, "frases": [
        "En el centro está el duelo de la final. Chovy contra Knight. Knight es el mejor del Mundial en eliminatorias: veintinueve asesinatos, sesenta y tres asistencias, y solo nueve muertes en siete partidas.",
        "Y Chovy juega la primera final de su carrera, después de quedarse en semifinales en dos mil veintidós, en dos mil veinticuatro y en dos mil veinticinco.",
    ]},
    {"id": "duelo_adc", "pre": 0.3, "frases": [
        "Entre los tiradores, Ruler contra Viper. Los dos mataron más que nadie en su equipo: treinta y ocho Ruler, treinta y siete Viper. Los dos promedian trescientos veintidós súbditos por partida. Están empatados hasta en eso.",
        "La diferencia: Ruler murió once veces, y Viper diecisiete.",
    ]},
    {"id": "duelo_sup", "pre": 0.3, "frases": [
        "Y los soportes, Duro contra ON. Setenta y siete asistencias contra ochenta y siete. Los que mueren para que los demás vivan.",
    ]},
    # ── NUEVA: los campeones de cada uno (Fearless; MG con iconos/ de cada campeón) ──
    # fuente: investigacion/datos_duelos.md § Campeones (cuadro final del feed de las 13 partidas). Iconos en iconos/<Campeón>.png.
    #   Se VE en los clips: Chovy Víktor (r_lyon2 t 38), Ahri (r_ig2 t 8), Taliyah (j1) · Ruler Ashe (r_lyon2, r_ig2), Jhin (r_ig1 t 22),
    #   Yunara (r_ig3fin t 9) · Viper Ezreal (r_dk2), Corki (r_t1g1), Kai'Sa (j4b) · Knight LeBlanc (j4b)
    {"id": "campeones", "pre": 0.5, "frases": [
        "Y un detalle que se va a notar en la selección. En eliminatorias, Chovy jugó con cinco campeones distintos. Knight, con seis.",
        "Entre los tiradores, Ruler usó cuatro: Ashe, Jhin, Xayah y Yunara. Viper, seis, Cassiopeia incluida. Solo comparten uno: Ashe.",
        "En la jungla, Canyon y Xun comparten tres: Lee Sin, Pantheon y Qiyana. Arriba, Kiin y Bin solo comparten a Camille. Y en el soporte, Duro y ON comparten tres: Leona, Nautilus y Seraphine.",
        "En total, Bilibili sacó treinta campeones distintos en siete partidas. Gen.G, veintitrés en seis.",
    ]},
    # ── HISTORIA ─────────────────────────────────────────────────────────────────
    {"id": "historia", "pre": 0.6, "frases": [
        "Y no es la primera vez que se ven. En dos mil veintitrés, Bilibili eliminó a Gen.G dos veces: en el MSI, y en cuartos del Mundial, tres a dos.",
        "En dos mil veinticuatro, Gen.G se cobró las dos en el MSI, y la final de ese torneo la ganó tres a uno.",
        "Y en una final, la experiencia pesa. Ruler fue campeón del mundo en dos mil diecisiete con Samsung. Canyon, en dos mil veinte. Del otro lado, Viper ganó el Mundial de dos mil veintiuno: es el último campeón chino.",
    ]},
    # ── CLAVES ───────────────────────────────────────────────────────────────────
    {"id": "claves", "pre": 0.6, "frases": [
        "Tres claves para el sábado. Pero antes, una regla que cambia todo en una final: el Fearless. En una serie, el campeón que ya se usó no se puede volver a elegir. En cinco partidas, los equipos se quedan sin sus favoritos, y gana el que tenga más fondo.",
        "Y aquí hay un choque directo: en el centro, Chovy y Knight comparten cuatro campeones de las eliminatorias. Ahri, Galio, Taliyah y Víktor. El que elija primero, se los quita al otro.",
        "Ahora sí, las claves. Una: el centro. Si Knight juega como en la semifinal, Bilibili tiene ventaja en la línea más importante del mapa.",
        "Dos: la paciencia. Gen.G no ha perdido una partida en eliminatorias, pero contra Invictus estuvo cuatro mil seiscientos abajo. Sabe esperar.",
        "Y tres: los cierres. Las partidas de Gen.G en eliminatorias duraron unos treinta y dos minutos en promedio. Las de Bilibili, un poco más. El que imponga su ritmo, se lleva la copa.",
    ]},
    {"id": "pronostico", "pre": 0.5, "frases": [
        "Leonardo ya dio su pronóstico: Gen.G es muy agresivo y fuerte en el juego temprano, pero Bilibili defiende muy bien en equipo y crece al final. Tres a dos para Bilibili.",
        "Y aquí le cumplimos el deseo a Historias de un Mundo Nuevo, que escribió: quiero salir en el video. Ahí estás.",
    ]},
    # ── CIERRE ───────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.5, "post": 3.0, "frases": [
        "Gracias a todos los que comentan. A tierrarara, que nos escribió: increíble resumen, felicidades. A Mike, que le dio efe cinco a la página esperando el video. Y a Paco: sí, vamos avanzando.",
        "Si quieres el resumen de la final con las jugadas analizadas como hoy, suscríbete y activa la campanita.",
        "Y ahora te toca: ¿quién gana el sábado, Gen.G o Bilibili? ¿Y con qué marcador? Déjalo en los comentarios. Nos vemos después de la final.",
    ]},
]
