# -*- coding: utf-8 -*-
"""¿Culpa de JOSEDEODO? Sus 7 partidas del Mundial 2026 · ~11-12 min · canal «Crónicas de ligoleyen» (subida por Studio).
Estilo ANÁLISIS TÁCTICO (docs/estilo_analisis_tactico.md); copia de videos/t1_blg_caida/ (tesis con datos).
Tesis: «el coach condenó a Josedeodo» (Eco Nooni, 183 mil vistas) frente a los 7 drafts y las 7 partidas.

DATOS VERIFICADOS (cero inventos):
- investigacion/stats_115660540726095{008,036,058,059,078,079,080}.json (feed oficial livestats: K/D/A, oro, dragones, torres).
- Drafts: Leaguepedia (cargo PicksAndBansS7), comprobados contra el campeón de Josedeodo en el feed:
  primera selección de jungla de TL: CFO Lee Sin (pierde), AL G1 Lee Sin (gana), LOS G1 Nocturne (pierde) = 1-2.
  jungla en la 2.ª ronda del draft: AL G2 Pantheon (gana), LOS G2 Xin Zhao (gana), LOS G3 Sejuani (pierde) = 2-1.
  vs BLG: TL azul, 1.ª selección Ezreal; BLG elige Lee Sin con su 1.ª selección; Josedeodo Jarvan IV (2.ª de TL, 1.ª ronda).
  LOS baneó el Lee Sin en las tres partidas (G1 ban 2, G2 ban 1, G3 ban 1).
- Dragones: el equipo con más dragones ganó las 7 (TL-rival: 1-5, 1-3, 4-1, 4-3, 1-3, 5-1, 2-5). Derrotas 5-16, victorias 13-5.
- Josedeodo: 19/20/41; en victorias 12/6/25, en derrotas 7/14/16. gol.gg: GD@15 +78, KP 81,1 %.
- Spawn (head coach) tras la eliminación: «hay que darnos un uno… nada de lo que hacemos funciona» (Sheep Esports).
- 2027: CoreJJ y Yeon se van a Cloud9 (no desmentido por TL); Josedeodo y Quid con contrato (Insider Gaming).
- Jugadas: datos_blg.md, datos_al.md, datos_los2.md (agentes, 25-nov), datos_lotl.md (LOS G1 12:11 y G3 34:37-34:53),
  videos/cfo_kc_worlds/investigacion/datos_cfo.md (CFO, Anciano 34:01-34:41).
La voz no cita fuentes. Sin [excited] ni [whispers].
"""
import json as _json
import os as _os

_D = _os.path.dirname(_os.path.abspath(__file__))
TITULO = "¿Culpa de JOSEDEODO? Revisé sus 7 partidas"
ARCHIVO = "tl_josedeodo"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español): la voz de siempre del canal
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.6,
           sin_etiquetas=("whisper", "excit"))
FONETICA = _json.load(open(_os.path.join(_D, "investigacion", "fonetica_lista.json"), encoding="utf-8"))
FONETICA.update({"Spawn": "Spon", "Sejuani": "Sejuáni", "Jarvan": "Yárvan", "Shad0w": "Shádou"})
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
    tramos=[(["gancho", "gancho2", "camino", "quien"], "Un juicio: tenso, expectante."),
            (["gracias", "acusacion", "blg"], "La acusación: pulso de análisis, sobrio."),
            (["drafts", "al1", "cfo"], "La prueba de los drafts: investigación que avanza."),
            (["rival", "mejor", "los2", "criticas"], "Su mejor partida: sube, luminoso."),
            (["dragones", "duelo", "los3"], "El río decide: tensión, golpe final."),
            (["numeros", "veredicto", "futuro", "cierre"], "Veredicto: reflexivo y luego firme.")])
# 25-nov (2.ª versión): silencios de las ÓRBITAS a mano (al1_2 $ini 2,5 · cfo_2 «El» 18,9 · los2_1 «Y»(1) 3,5) + investigacion/huecos.py
ESPACIOS_VOZ = {
    "gancho_0": [('y', 0, 2.64, 8.96)],
    "blg_0": [('y', 2, 4.66)],
    "blg_1": [('Y', 0, 2.0), ('el', 3, 5.82, 8.445)],
    "al1_2": [('$ini', 0, 10.2), ('Anyone', 0, 1.46), ('pero', 0, 5.12)],
    "al1_1": [('Morgan', 0, 7.79), ('Josedeodo', 1, 0.82)],
    "al1_3": [('alma', 0, 0.96)],
    "cfo_2": [('El', 0, 18.9), ('Pero', 0, 2.42), ('Rest', 0, 0.84), ('Liquid', 0, 1.38)],
    "los2_1": [('Y', 1, 3.5), ('$ini', 0, 7.92), ('persigue', 0, 6.34), ('y', 2, 3.84)],
    "los2_3": [('Liquid', 0, 0.9), ('cae', 0, 0.52), ('Josedeodo', 0, 5.84), ('y', 2, 18.72)],
    "los3_1": [('Y', 0, 2.9, 2.19)],
    "los3_3": [('Ackerman', 0, 0.84), ('Zest', 0, 0.32), ('doble', 0, 1.2), ('triple', 0, 0.84)],
    "los3_4": [("$ini", 0, 0.56)],
}

ESCENAS = [
    # ── GANCHO: LOS G1 (datos_los2.md § B, los1_curse: HUD = t + 690,5): 11:59 definitiva de Nocturne sobre Zest · 12:03 Josedeodo mata a
    #   Zest · 12:06 Curse mata a Morgan · 12:11 Curse (nivel 9 vs 8) gana el 1 contra 1: DOUBLE KILL · narración «José no tiene destello y
    #   ñam ñam ñam» (post de 5,5 s: se oye la narración original). NO decir «Curse lo invadió».
    {"id": "gancho", "pre": 3.0, "post": 9.5, "frases": [
        "Viernes treinta de octubre. Team Liquid juega su vida en el Mundial. Minuto doce: su jungla argentino, Josedeodo, mata a Zest… y se queda solo frente a Curse.",
    ]},
    {"id": "gancho2", "pre": 0.3, "frases": [
        "Y desde que Liquid quedó fuera, casi todos culpan a una persona. Y no es Josedeodo. Es su entrenador.",
        "La teoría dice que el coach no le dio a Josedeodo sus campeones. Así que revisé sus siete partidas del Mundial, draft por draft y pausa por pausa.",
        "Y lo que encontré no le da la razón a nadie. En este video: los siete drafts, los números de Josedeodo, y la pelea que lo sacó del Mundial, en 3D.",
    ]},
    # ── EL CAMINO (~25 s): 7 partidas, 3-4 ──
    {"id": "camino", "pre": 0.5, "frases": [
        "Primero, el camino de Liquid. Pierde la primera contra CTBC Flying Oyster, doce a once. Y la segunda contra Bilibili Gaming, diecisiete a dos.",
        "Con cero y dos, elimina dos a cero a Anyone's Legend, el campeón de China. Y en la serie a muerte, cae dos a uno contra Los Grandes. Siete partidas: tres victorias y cuatro derrotas.",
    ]},
    # ── ¿QUIÉN ES JOSEDEODO? (Leaguepedia/Upcomer: Brandon Joel Villegas, AR; Furious Gaming CLS 2018, Rainbow7 LLA, FlyQuest LCS 2021
    #   (anuncio 20-nov-2020), Estral 2024, Team Liquid 2026; Sheep Esports: LCS 2026 Spring 1st Team All-Pro) ──
    {"id": "quien", "pre": 0.5, "frases": [
        "Pero antes: ¿quién es Josedeodo? Brandon Villegas, argentino. Empezó en la liga latinoamericana, pasó por Rainbow7 en México, y en 2021 dio el salto a Estados Unidos con FlyQuest.",
        "Volvió a Latinoamérica, y en 2026 llegó a Team Liquid. Ese mismo año lo eligieron en el primer equipo ideal de la LCS de primavera. Llegó al Mundial como uno de los mejores junglas de su región.",
    ]},
    # ── AGRADECIMIENTOS (≥ 4) + la crítica justa de gasYotube (19 likes) ──
    {"id": "gracias", "pre": 0.5, "frases": [
        "Antes de seguir: gracias a Daniel Novoa, por acompañarnos en todo el Mundial hasta la final. A Argonauta y a Rei Gameplays, que llegaron como nuevos suscriptores. Y a Fede Lovera, por las felicitaciones.",
        "Y Gas, en el video de T1 nos dijiste: si el jungla no hace, perdiste la partida. Tenías razón en algo: el río es del jungla. Por eso hoy, un video entero sobre un jungla.",
    ]},
    # ── LA ACUSACIÓN (~30 s): Spawn y el draft contra BLG ──
    {"id": "acusacion", "pre": 0.5, "frases": [
        "El acusado se llama Spawn, el entrenador de Liquid. Y él mismo, después de quedar fuera, lo dijo así: nada de lo que hacemos está funcionando.",
        "La acusación tiene un ejemplo claro. Partida dos, contra Bilibili. Liquid tiene la primera selección del draft, y el Lee Sin, el campeón favorito de Josedeodo, está libre.",
        "Liquid elige Ezreal. Y Bilibili, con su primera selección, se lleva el Lee Sin para Xun.",
    ]},
    # ── BLG (datos_blg.md, blg_j1: HUD = t + 643,7): 10:52 TL empieza el 1.er dragón (Josedeodo, Yeon, CoreJJ) · Xun y ON por el este ·
    #   11:06 «Red team has stolen the Mountain Drake!» (retrato Lee Sin) · narración «era 50-50» · larvas, Heraldo: de Xun ·
    #   blg_j2 (HUD = t + 1038,6): 17:54 «BLG Xun has slain TLAW Josedeodo!» (ON lo enraíza) · final 2-17, Josedeodo 0/4/2
    {"id": "blg", "pre": 6.2, "post": 2.0, "frases": [
        "Josedeodo juega Jarvan. Minuto once: con Yeon y CoreJJ empieza el primer dragón. Xun entra por el otro lado… y con el castigo, se lo roba.",
        "Con el Lee Sin que Liquid le dejó. Y no fue lo único: las larvas y el Heraldo también fueron de Xun. En el minuto diecisiete, el que mata a Josedeodo es él.",
        "Liquid hace dos asesinatos en toda la partida. Bilibili, diecisiete. Josedeodo termina sin un solo asesinato y con cuatro muertes.",
    ]},
    # ── LOS SIETE DRAFTS (~35 s) ──
    {"id": "drafts", "pre": 0.5, "frases": [
        "Hasta aquí, la teoría se sostiene. Pero entonces revisé los otros seis drafts. Y el dato no cuadra.",
        "Tres veces Liquid eligió al jungla de Josedeodo con su primera selección: dos Lee Sin y un Nocturne. Resultado: una victoria y dos derrotas.",
        "Y tres veces lo dejó para la segunda ronda del draft, la de los últimos turnos. Resultado: dos victorias y una derrota.",
    ]},
    # ── AL G1 (datos_al.md, al_j1: HUD = t + 1696): 28:39 Morgan (TP) y Josedeodo por el flanco · 28:42 ulti de Camille sobre Hope ·
    #   Josedeodo entra con la furia del dragón (narración) · 28:44 Yeon mata a Hope · triple de Yeon · AL mata a Yeon y CoreJJ ·
    #   29:02 Josedeodo remata a Breathe = ACE (+7,8K) · 29:28 alma de nube · final 16-5, Josedeodo 3/0/8. NO decir «insec».
    {"id": "al1", "pre": 4.0, "post": 2.0, "frases": [
        "Cuando el Lee Sin sí salió, contra Anyone's Legend, Liquid lo eligió con su primera selección. Y así se vio.",
        "Minuto veintiocho. Morgan vuelve con la teleportación y entra por el flanco con Josedeodo. Morgan atrapa a Hope con su definitiva, y Josedeodo entra detrás, con la patada.",
        "Yeon hace un triple. Anyone's Legend se lleva a Yeon y a CoreJJ, pero Josedeodo remata a Breathe: los cinco de Anyone's Legend, fuera.",
        "Medio minuto después, el alma de nube. Josedeodo termina tres asesinatos, cero muertes y ocho asistencias, y Liquid gana dieciséis a cinco.",
    ]},
    # ── CFO: Lee Sin con primera selección y derrota (datos_cfo.md: Anciano 34:01-34:41, Josedeodo muere 34:29) ──
    {"id": "cfo", "pre": 4.0, "post": 2.0, "frases": [
        "Pero la otra vez que Liquid le dio el Lee Sin con su primera selección, contra CTBC Flying Oyster, perdió.",
        "Minuto treinta y cuatro. Liquid gana en asesinatos, diez a cinco. Pero CTBC tiene cuatro dragones, y empieza el ancestral.",
        "Josedeodo espera a un lado del foso para robarlo. Pero Kino lo levanta, y Rest lo remata. El ancestral es de CTBC, y medio minuto después, el Barón. Liquid pierde doce a once.",
    ]},
    # ── EL RIVAL: Curse (BR) y Ackerman (AR) (gol.gg país; stats LOS G1-G3: Curse 7/0/6, 0/5/5, 4/0/7 = 11/5/18; Josedeodo 9/7/17) ──
    {"id": "rival", "pre": 0.5, "frases": [
        "En la serie a muerte, el rival de Josedeodo fue Curse, el jungla brasileño de Los Grandes. Un duelo latino: Argentina contra Brasil. Y en el soporte de Los Grandes, otro argentino: Ackerman.",
        "En las tres partidas, Curse terminó con once asesinatos y cinco muertes. Josedeodo, con nueve y siete.",
    ]},
    # ── SU MEJOR PARTIDA: LOS G2 (datos_los2.md; Xin Zhao = pick 4 de rojo, 2.ª ronda, Leaguepedia): la de MÁS asesinatos (5) y MÁS daño
    #   (23 %) de sus 7; NO la de mejor KDA (Lee Sin 3/0/8) ──
    {"id": "mejor", "pre": 0.5, "frases": [
        "Y aquí está la parte que nadie cuenta. Su partida con más asesinatos y más daño de todo el Mundial fue con un campeón que Liquid eligió en la segunda ronda del draft.",
        "Partida dos contra Los Grandes, que ya le había quitado el Lee Sin. Josedeodo juega Xin Zhao.",
    ]},
    # ── LOS G2 (los2_j1: HUD = t + 955,8): 16:23 Heraldo de Josedeodo, Curse debajo · 16:32 definitiva de Xin Zhao, mata a Duduhh (3-6) ·
    #   16:45 persigue y mata a Feisty («is on a rampage», TL +1,9K → +3,0K) · narración «José nuevamente demostrando por qué es el mejor
    #   jugador de su equipo» · los2_j2 (HUD = t + 2105,8): 35:39-35:41 TL atrapa a Curse dentro de su propio Cataclismo, lo mata CoreJJ ·
    #   35:48 Josedeodo mata a Feisty · 36:09 Anciano sin bajas · final 15-8, 5 dragones (alma química), Josedeodo 5/1/10 ──
    {"id": "los2", "pre": 4.0, "post": 2.0, "frases": [
        "Minuto dieciséis. Josedeodo se lleva el Heraldo, con Curse justo debajo.",
        "Y entra con la definitiva de Xin Zhao: mata a Duduhh. Y no se detiene: persigue a Feisty, y también lo mata.",
        "Los narradores lo dijeron así: Josedeodo, demostrando por qué es el mejor jugador de su equipo.",
        "Minuto treinta y cinco. Liquid atrapa a Curse dentro de su propio Cataclismo, y cae. Josedeodo mata a Feisty otra vez, y Liquid se lleva el ancestral sin perder a nadie.",
        "Josedeodo termina cinco asesinatos, una muerte y diez asistencias. Liquid gana quince a ocho, con cinco dragones, y empata la serie.",
    ]},
    # ── CRÍTICAS CON BURLA (Shadow, Luis) + justas (Jorge: el staff; Mr. Jezzak: pronunciación) ──
    {"id": "criticas", "pre": 0.5, "frases": [
        "Pausa para los comentarios. Shadow escribió que hay que ser bien fraca para hacer un video entero defendiendo a Doran. Shadow, tranquilo: hoy no defiendo a nadie. Hoy traigo siete partidas, y si sale culpable, sale culpable.",
        "Luis dijo que nuestro video de fichajes llegó un día tarde. Luis, este no puede llegar tarde: estas partidas ya se jugaron, y los números no cambian.",
        "Jorge nos pidió hablar también del cuerpo técnico. Hecho: hoy el acusado es el coach. Y Mister Jezzak, gracias por la crítica de la pronunciación: los nombres de hoy van revisados uno por uno.",
    ]},
    # ── EL DATO QUE DECIDE: DRAGONES 7 DE 7 ──
    {"id": "dragones", "pre": 0.5, "frases": [
        "Entonces, si no fue el draft, ¿qué decidió las partidas de Liquid? Esto. El equipo que se llevó más dragones ganó las siete.",
        "En las tres victorias, Liquid tomó trece dragones contra cinco. En las cuatro derrotas, tomó cinco contra dieciséis.",
        "Y el río es justo el trabajo del jungla. Y aquí viene el segundo siete de siete.",
    ]},
    # ── DUELO DE JUNGLAS AL MINUTO 15 (investigacion/oro15.py, feed: −1 119 CFO, −174 BLG, +754 AL1, +958 AL2, −742 LOS1, +951 LOS2, −952 LOS3) ──
    {"id": "duelo", "pre": 0.5, "frases": [
        "Comparé el oro de Josedeodo con el del jungla rival al minuto quince, en las siete partidas.",
        "En las tres victorias, Josedeodo iba arriba de su rival: más de setecientos contra Tarzan, más de novecientos en la segunda, y casi mil contra Curse.",
        "Y en las cuatro derrotas, iba abajo: mil cien contra Shad0w, ciento setenta contra Xun, y más de setecientos y novecientos contra Curse.",
        "Cuando Josedeodo ganó su duelo, Liquid ganó. Cuando lo perdió, Liquid perdió. Siete de siete. Así que vamos a la partida que lo decidió todo.",
    ]},
    # ── LOS G3: la pelea del muro (datos_lotl.md J1, lotl_j1: HUD = t + 2063; foco en Josedeodo; 3D NUEVO) ──
    {"id": "los3", "pre": 5.0, "post": 6.0, "frases": [
        "Tercera partida, la de la eliminación. Minuto treinta y cuatro. Liquid ya había recortado de siete mil abajo a tres mil trescientos, y tiene el Barón encima.",
        "Aparece el dragón infernal. Y Josedeodo entra al foso con Yeon, a pelearlo.",
        "Feisty levanta el muro de Taliyah sobre el río. CoreJJ y Quid quedan del otro lado. Josedeodo y Yeon, dentro, con cuatro de Los Grandes encima.",
        "Liquid se lleva el dragón. Pero Ackerman mata a Yeon, y Zest mata a Josedeodo. Y sigue: doble, triple.",
        "Los narradores lo dijeron en ese momento: Liquid ya la tenía en las manos.",
        "Desde ahí, Los Grandes se lleva el alma, el ancestral y la partida. Y Liquid queda fuera del Mundial.",
    ]},
    # ── LOS NÚMEROS DE JOSEDEODO ──
    {"id": "numeros", "pre": 0.5, "frases": [
        "Los números de Josedeodo en el Mundial: diecinueve asesinatos, veinte muertes y cuarenta y una asistencias en siete partidas.",
        "En las victorias: doce asesinatos y seis muertes. En las derrotas: siete asesinatos y catorce muertes.",
    ]},
    # ── VEREDICTO ──
    {"id": "veredicto", "pre": 0.5, "frases": [
        "Entonces, ¿culpa de quién? ¿Del coach? En un draft, sí: contra Bilibili le regaló el Lee Sin al rival.",
        "Pero la idea de que con su campeón Liquid ganaba no aguanta: su mejor partida fue con un pick de la segunda ronda.",
        "La verdad es otra. Josedeodo no fue el culpable ni la víctima: fue el termómetro. Liquid llegó exactamente hasta donde llegó su jungla. Cuando ganó el río, Liquid ganó. Cuando lo perdió, Liquid se fue a casa.",
    ]},
    # ── 2027 ──
    {"id": "futuro", "pre": 0.5, "frases": [
        "Y ahora viene lo más difícil. CoreJJ y Yeon se van a Cloud9. Josedeodo se queda en Liquid, con contrato para el próximo año. El proyecto ahora es suyo.",
    ]},
    # ── CIERRE ──
    {"id": "cierre", "pre": 0.5, "post": 2.0, "frases": [
        "Y ahora te toca a ti: ¿culpa del coach, de Josedeodo, o del río? Déjalo en los comentarios, que todos se leen.",
        "Y si te gustó este análisis pausa por pausa, suscríbete, para que no te pierdas el siguiente.",
    ]},
]
