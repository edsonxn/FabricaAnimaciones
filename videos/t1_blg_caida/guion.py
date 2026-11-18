# -*- coding: utf-8 -*-
"""La VERDADERA razón por la que cayó T1 (BLG 3-1 T1, semifinal de la Worlds 2026, dom 8-nov) · ~15 min · canal «Crónicas de
ligoleyen» (subida por Studio). Estilo ANÁLISIS TÁCTICO (docs/estilo_analisis_tactico.md); copia de videos/lol_final_previa/.
La caída de T1 ya NO es spoiler: va en título, miniatura y gancho.

DATOS VERIFICADOS (cero inventos): investigacion/stats_g1..g4.json (feed oficial livestats: oro por jugador a los 5-25 min, K/D/A
final, dragones/torres/barones), feed_122..125.txt (muertes), datos_j4.md (G2, robo del alma 23:15 = j4b en datos_relleno.md),
datos_j5.md (G3, alma infernal 32:33-33:08), datos_j6.md (G4, pelea 32:14-32:27, Barón 29:20, nexo 37:45), datos_g1.md y
datos_g4a.md (agentes, 17-nov). OJO: en la G4 Faker hizo 2 asesinatos en la pelea de las 28 (no 3, como decía la previa): HUD 33:20
Faker 2/1/4 y antes de las 28 no tenía ninguno.
La voz no cita fuentes. Sin [excited] ni [whispers].
"""
import json as _json
import os as _os

_D = _os.path.dirname(_os.path.abspath(__file__))
TITULO = "La VERDADERA razón por la que cayó T1"
ARCHIVO = "t1_blg_caida"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español): la voz de siempre del canal
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.6)
FONETICA = _json.load(open(_os.path.join(_D, "investigacion", "fonetica_lista.json"), encoding="utf-8"))
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

TRANSICIONES = [("continua", 0.1)] * 60
LYRIA = dict(
    estilo="Modern esports broadcast analysis score: tight electronic drums, pulsing synth bass, glassy arpeggios, "
           "stadium-sized hits and tension risers, instrumental only, no vocals, energetic but unobtrusive under narration.",
    escenas={},
    tramos=[(["gancho", "serie"], "Fin de una era: oscuro, tenso, expectante."),
            (["doran", "g4a", "g3a"], "La acusación: pulso de análisis, sobrio."),
            (["oro15", "g1"], "El primer dato: investigación que avanza."),
            (["dragones", "g2"], "El río decide: vaivén."),
            (["g3r", "g3"], "La remontada y el alma: tensión que sube."),
            (["g4_ctx", "g4"], "La última pelea: drama, golpe final."),
            (["faker", "faker_e", "rivales", "veredicto", "cierre"], "Veredicto: reflexivo y luego firme.")])
ESPACIOS_VOZ = {}

ESCENAS = [
    # ── GANCHO (~45 s) ───────────────────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "Domingo ocho de noviembre. Semifinal del Mundial. T1, campeón de los últimos tres años, cae tres a uno contra Bilibili Gaming.",
        "Y desde ese día, casi todo el mundo culpa a una sola persona. [short pause] Doran.",
        "Revisé las cuatro partidas, pausa por pausa. Y sí, Doran tiene su parte de culpa. Pero hay algo que se repite en las cuatro partidas, y que casi nadie está mirando.",
        "En este video: la acusación contra Doran, con sus números. Las dos cosas que de verdad decidieron la serie. Y la pelea que terminó con una era, en 3D.",
    ]},
    # ── LA SERIE (~25 s): marcador de las 4 partidas (feed_122..125: 18-6, 22-10 T1, 19-10, 21-9) ──
    {"id": "serie", "pre": 0.5, "frases": [
        "Primero, el marcador. Partida uno: Bilibili gana dieciocho a seis. Partida dos: T1 responde, veintidós a diez, y empata la serie.",
        "Partida tres: Bilibili, diecinueve a diez. Y en la cuarta, veintiuno a nueve. Bilibili a la final, y T1 a casa.",
    ]},
    # ── EL ACUSADO: DORAN (stats_g*.json: oro de Doran − oro de Bin al minuto 20; muertes del feed) ──
    {"id": "doran", "pre": 0.5, "frases": [
        "Empecemos por el acusado. Doran, el top de T1. En cuatro partidas murió veintidós veces. Nadie murió más en toda la serie: el siguiente es su propio jungla, Oner, con dieciséis. Del lado de Bilibili, el que más murió fue su soporte, ON, con doce.",
        "Y perdió su línea en las cuatro partidas. Al minuto veinte iba por debajo de Bin en oro: mil ciento sesenta y seis en la primera, seiscientos cuarenta y siete en la segunda, mil ochocientos cuarenta y dos en la tercera, y mil quinientos treinta y seis en la cuarta.",
        "Cuatro campeones distintos: Rumble, Olaf, Ambessa y, en la partida de la eliminación, Vayne. Con ninguno pudo con Bin.",
    ]},
    # ── G4 ARRANQUE (datos_g4a.md: g4_draft sin HUD, Vayne ≈ t 8, «¡Ay, no puede ser!» t 9-12; g4_j1 HUD = t + 485, g4_j2 = t + 637,
    #   g4_j3 = t + 1025) · Vayne = última selección del draft con el Renekton de Bin ya elegido (ficha 1,1 % de elección, 0W-1L) ·
    #   08:19-08:26 Oner solo en el foso de las larvas, FIRST BLOOD de Viper · Bin→Keria 08:48 · Viper→Peyz 08:56 · 10:44 Bin y Xun sobre
    #   Doran, 10:52 Bin lo mata bajo su torre · 17:06 Doran −1,1K contra Bin (HUD) · 17:33-17:41 ON (definitiva de Seraphine, narración)
    #   y BLG matan a Peyz, Keria, Oner y Doran → 3-10, BLG empieza el dragón 17:45 (lo toma ≈ 17:52)
    {"id": "g4a", "pre": 6.0, "post": 2.0, "frases": [
        "Partida cuatro, la de la eliminación. En el último turno del draft, con el Renekton de Bin ya elegido, T1 le da a Doran una Vayne. Los narradores no lo podían creer.",
        "Minuto ocho. Oner se mete solo en el foso de las larvas, y Viper se lo lleva: primera sangre. Después caen Keria y Peyz. Tres de T1 en treinta segundos.",
        "Minuto diez. Xun sube por el río, y con Bin atrapan a Doran bajo su torre. Bin lo remata.",
        "Minuto diecisiete: Doran ya va mil cien de oro por debajo de Bin. Y en el foso del dragón, ON atrapa a cuatro con su definitiva. Bilibili mata a cuatro de T1 y se lleva el dragón.",
    ]},
    # ── G3 ARRANQUE: Doran (datos_g3a.md A1/A2: g3_j1 HUD = t + 180, g3_j2 = t + 577) ──
    #   03:29 Xun sale del río, 03:30 Doran aturdido, 03:35 Xun lo mata (asistencia Bin) · 09:56 buceo de Bin, Viper y Xun bajo la torre,
    #   10:00 definitiva de Doran hacia Xun (narración: no lo alcanza), 10:08 Viper lo mata · 10:17 Bin +1,1K
    {"id": "g3a", "pre": 4.0, "post": 1.5, "frases": [
        "Y no fue solo la cuarta. Partida tres, minuto tres. Xun sale del río, aturde a Doran, y con Bin lo matan al pie de su propia torre.",
        "Los narradores lo dijeron en ese momento: la línea que T1 tenía que ganar, ahora la tenía en contra.",
        "Minuto diez, otra vez. Bin, Viper y Xun se le tiran encima bajo la torre. Doran salta con su definitiva para atrapar a Xun… y no lo alcanza. Viper lo remata.",
        "Dos muertes en diez minutos. Y Bin ya le sacaba más de mil de oro.",
    ]},
    # ── PRIMER DATO: oro de T1 al minuto 15 en las 4 (stats_g*.json: −419, −2 069, −731, −2 791) ──
    {"id": "oro15", "pre": 0.5, "frases": [
        "Pero si todo fuera culpa de Doran, T1 habría ido bien en las otras líneas. Y aquí está el primer dato que casi nadie menciona.",
        "Al minuto quince, T1 iba perdiendo en oro en las cuatro partidas. Cuatrocientos en la primera. Más de dos mil en la segunda. Setecientos en la tercera. Casi dos mil ochocientos en la cuarta.",
        "Sí, también en la partida que ganó. T1 no le ganó el arranque a Bilibili ni una sola vez. La única que ganó, la ganó remontando.",
    ]},
    # ── G1: cómo gana BLG la primera (datos_g1.md: g1_j1 HUD = t + 917, g1_j2 = t + 1220, g1_j3 = t + 1416) ──
    #   Heraldo robado 15:21 · Peyz→Bin 15:37 · Viper→Peyz y Knight→Faker 15:40 · Knight→Doran 15:48 (3 por 1) · Viper→Oner 20:27 ·
    #   Barón 20:35→21:00 sin disputa · Knight→Doran 21:17 · torres 3→7 de 21:00 a 23:02, inhibidor 23:15 (ON) ·
    #   pelea en la base: Faker→ON 23:53, Xun→Oner 23:56, Knight→Keria 24:15, Bin→Doran 24:19, Viper→Peyz ≈24:20 · Knight 8/0/9
    {"id": "g1", "pre": 6.0, "post": 5.0, "frases": [
        "Partida uno. Minuto quince. Xun le roba el Heraldo a T1 en su propia cara. Y empieza la primera pelea grande. Peyz abre: mata a Bin.",
        "Pero Viper responde sobre Peyz, y Knight, con Orianna, se lleva a Faker y a Doran. Tres por uno para Bilibili.",
        "Minuto veinte. Viper caza a Oner, el jungla de T1. Sin él, T1 no disputa el Barón, y Bilibili lo toma gratis. Diecisiete segundos después, Knight vuelve a cazar a Doran.",
        "Con el Barón, Bilibili tira cuatro torres en dos minutos y rompe un inhibidor. Y en el minuto veinticuatro, ya en la base de T1, Faker mata a ON… pero Bilibili responde y se lleva a cuatro de T1.",
        "Knight termina la partida con ocho asesinatos, sin morir ni una vez.",
    ]},
    # ── SEGUNDO DATO: más dragones = ganó las 4 (stats_g*.json eventos) ──
    {"id": "dragones", "pre": 0.5, "frases": [
        "Segundo dato. Y este es el que decide la serie. El equipo que se llevó más dragones ganó las cuatro partidas.",
        "Partida uno: Bilibili tres, T1 uno. Partida dos: T1 cuatro, Bilibili ninguno, con el alma y además el dragón ancestral. Partida tres: Bilibili cuatro, con el alma infernal. Partida cuatro: Bilibili cuatro, con el alma de montaña.",
        "Cuatro de cuatro. Y la única que ganó T1 es justo la única en la que fue dueño del río. Mira cómo.",
    ]},
    # ── G2: el robo del alma del océano (datos_relleno.md § j4b, VOD r9-avVeme5o, HUD = t + 1382 en j4b.mp4) ──
    #   marcador al inicio: T1 7 – BLG 6, T1 +1,1K, BARON POWERPLAY de T1 (Barón 21:27), dragones T1 3
    {"id": "g2", "pre": 6.0, "post": 6.0, "frases": [
        "Partida dos. Minuto veintitrés. T1 tiene el Barón y tres dragones. Uno más, y es el alma.",
        "Las dos se juntan en el foso. Oner, con Lee Sin, se mete… y el rótulo lo dice todo: dragón robado. Alma del océano para T1.",
        "Doran mata a ON y a Xun. Faker aguanta con el reloj de arena. Pero Viper se lleva a Oner y a Keria.",
        "Y Faker vuelve con la teleportación. Peyz mata a Viper, y Faker remata a Knight. Cuatro por dos para T1.",
        "Con el dragón ancestral y el segundo Barón, T1 cierra la partida veintidós a diez. Así se ve T1 cuando gana el río.",
    ]},
    # ── G3 REMONTADA (datos_g3a.md A3: g3_j3 HUD = t + 1320): 22:00 BLG 7-4 en el dragón infernal con el muro de Knight · 22:01 T1 se lo
    #   queda (lo roba Oner, narración) · ON cae 22:03-04 (Oner, feed) · 22:07 Bin hechizado, 22:09 Faker→Bin · 22:10-12 Peyz→Xun ·
    #   22:16 Viper→Keria · 22:28 Knight hechizado, 22:30 Faker→Knight → 8-8 a las 22:33, T1 +1,0K (HUD)
    {"id": "g3r", "pre": 2.5, "post": 4.0, "frases": [
        "Pero T1 no se rinde fácil. En esa misma partida, minuto veintidós, Bilibili va siete a cuatro y está haciendo el dragón infernal, con el muro de Knight cruzando el río.",
        "Oner entra y se lo roba. ON cae. Faker hechiza a Bin y lo mata. Peyz se lleva a Xun.",
        "Viper responde sobre Keria… pero Faker persigue a Knight hasta la jungla y lo remata. De siete a cuatro, a ocho a ocho. Y T1 se pone arriba en oro.",
    ]},
    # ── G3: la pelea del alma infernal (datos_j5.md, j5.mp4: HUD = t + 1904) ──
    {"id": "g3", "pre": 5.0, "post": 5.0, "frases": [
        "Pero la remontada no le alcanzó. Bilibili se lleva el primer Barón, y llega al minuto treinta y dos con tres dragones.",
        "Aparece el dragón infernal. Si lo toma Bilibili, es el alma. Y T1 entra al foso sin visión alrededor.",
        "Knight, con Taliyah, levanta el muro sobre el río. Viper cae… y resucita con el Ángel de la Guarda.",
        "En esa pelea, Knight empieza matando a Oner. Bin cae, pero Xun mata a Doran. Y Bilibili se lleva el alma infernal.",   # 17-nov: «Knight mata a Oner.» sola sonaba a otro idioma (idioma_voz)
        "En el centro, T1 se cobra a Knight y una torre. Pero Viper hace un doble asesinato: Peyz y Keria. Con el segundo Barón, Bilibili cierra la partida y se pone dos a uno.",
    ]},
    # ── G4: el contexto (feed_125: 3-10 y −3,6K a las 17:46; pelea 28:02-28:27; Barón T1 29:20; +0,4K BLG a las 32:16) ──
    {"id": "g4_ctx", "pre": 0.5, "frases": [
        "Partida cuatro. La de la eliminación. Al minuto dieciocho, T1 pierde diez asesinatos a tres y va casi cinco mil de oro abajo.",
        "Y aun así, T1 es T1. Minuto veintiocho: Faker y Doran hacen dos asesinatos cada uno, y T1 gana la pelea cinco por dos.",
        "Se lleva el Barón, la diferencia baja… y en el minuto treinta y dos, T1 está a cuatrocientos de oro de empatar la partida.",
    ]},
    # ── G4: LA PELEA (datos_j6.md, j6.mp4: HUD = t + 1860; 3D con pistas_j6.json, cámara NUEVA) ──
    {"id": "g4", "pre": 4.0, "post": 9.0, "frases": [
        "Al Barón le quedan dos segundos. T1 sube por el centro y tira la torre de Bilibili.",
        "Oner se lanza sobre Viper… y Viper resucita con el Ángel de la Guarda.",
        "En ese momento llegan Bin por arriba y Xun por abajo. Y Faker se va solo, detrás de Knight y ON.",
        "Primero cae Oner, a manos de Knight, y enseguida Bin mata a Doran. Y un rayo de Knight se lleva a Faker. Doble asesinato. En nueve segundos, tres de T1 muertos, y nadie de Bilibili.",
        "Los narradores lo dijeron en ese momento: quien fuerza la pelea es el mismo T1, el primero que se sobreextiende.",
        "Bilibili se lleva el alma de montaña y el Barón, y en el minuto treinta y siete cae el nexo. Se rompió la dinastía.",
    ]},
    # ── ¿Y FAKER? (stats_g*.json final: Faker 4/2/2, 4/0/13, 3/2/2, 3/1/4 = 14/5/21; Knight 18/7/30; Viper 23/11/27) ──
    {"id": "faker", "pre": 0.5, "frases": [
        "¿Y Faker? Catorce asesinatos, cinco muertes y veintiuna asistencias en la serie. Ninguna muerte en la partida que ganó T1. Faker no fue el problema.",
    ]},
    # ── FAKER G2 (datos_g3a.md B: g2_faker HUD = t + 1057): 17:45 Bin solo abajo (bajó con la teleportación a defender la torre, narración) ·
    #   17:46 E de Syndra → Bin aturdido · Doran, Keria y Oner llegan · 17:50 Oner lo mata (asist. Faker, Doran, Keria) · la repetición
    #   confirma la misma E sobre Knight a las 17:03-17:08 · narración «Faker la hace de nuevo» · Faker 0 asesinatos a las 17:56
    {"id": "faker_e", "pre": 3.0, "post": 1.5, "frases": [
        "Y mira esto. Partida dos, minuto diecisiete. Bin baja con la teleportación a defender una torre, solo.",
        "Faker llega sin que nadie lo vea, y con Syndra lo empuja y lo aturde. Llegan Doran, Keria y Oner, y Oner lo remata.",
        "Los narradores lo cantaron así: Faker la hace de nuevo. Porque minutos antes ya había atrapado a Knight igual. No se llevó el asesinato, pero la jugada fue suya.",
    ]},
    {"id": "rivales", "pre": 0.5, "frases": [
        "Del otro lado, el que pesó fue el medio de Bilibili, Knight, con dieciocho asesinatos. Y Viper, con veintitrés, el que más mató en toda la serie.",
    ]},
    # ── VEREDICTO ────────────────────────────────────────────────────────────────
    {"id": "veredicto", "pre": 0.5, "frases": [
        "Entonces, ¿cuál es la verdadera razón? No es una sola. Doran perdió su línea en las cuatro partidas, sí. Pero T1 también perdió los cuatro arranques, y perdió el río en tres de cuatro.",
        "Cuando fue dueño de los dragones, ganó veintidós a diez. Cuando no, Bilibili le ganó las otras tres. Y en la última, con la partida casi empatada, T1 forzó una pelea por una torre con el Barón a punto de acabarse.",
        "T1 no cayó por un jugador. Cayó porque nunca le ganó el arranque a Bilibili, y en el río, Bilibili fue mejor.",
    ]},
    # ── CIERRE ───────────────────────────────────────────────────────────────────
    {"id": "cierre", "pre": 0.5, "post": 2.0, "frases": [
        "Ya empezó el mercado de fichajes, y el futuro de T1 está en el aire. En el canal tienes el video con todos los movimientos.",
        "Y ahora te pregunto a ti: ¿culpa de Doran, o culpa del río? Déjalo en los comentarios, que todos se leen. Y si te gustó este análisis pausa por pausa, suscríbete, para que no te pierdas el siguiente.",
    ]},
]
