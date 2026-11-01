# -*- coding: utf-8 -*-
"""Worlds 2026: resumen de la semana decisiva (rondas 4 y 5 de la fase suiza, 28-31 oct), ~23 min, canal «Crónicas de ligoleyen»
(subida por Studio; se publica el sáb 31-oct por la tarde, ya jugadas todas las rondas: días por nombre, nunca «hoy» ni «ayer»). Fórmula de videos/lol_worlds_2026/ (40 mil
vistas), estilo ANÁLISIS TÁCTICO (docs/estilo_analisis_tactico.md). SIN SPOILER en título, miniatura y gancho.

DATOS VERIFICADOS: investigacion/datos_{t1ko,lyig,kccf,blte,lotl,g2hl}.md (feed oficial + cuadros del VOD + narración); estructura
y comentarios reales en investigacion/plan_guion.md. Relojes = HUD. LYON = organización mexicana (Liquipedia) que juega la LCS.
ACTO A = hasta `tabla4`. ACTO B (tras HLE-BLG del sáb 31-oct) se AÑADE detrás de `tabla4`: no mueve nada de lo anterior.
Comentarios: la voz IA fue la queja n.º 1 del video anterior, «sobre todo cuando quiere sonar épica»: SIN [excited] y más estable.
"""
import json as _json
import os as _os

TITULO = "Worlds 2026: TODO lo que pasó en la semana decisiva"
ARCHIVO = "lol_semana2"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 110
# JC - Energetic News Broadcaster (ElevenLabs, español), la voz de todos los videos de la Worlds
VOZ = dict(motor="elevenlabs", voice_id="4XUsiqPDK4UACIM2BILe", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.6)
FONETICA = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "investigacion", "fonetica_lista.json"),
                           encoding="utf-8"))
CER_MAX_POR_FRASE = {"hlbl_res_0": 0.098, "hlbl_res_1": 0.05, "hlbl_j1_0": 0.077, "hlbl_j1_1": 0.125, "hlbl_j1_2": 0.052, "hlbl_j1_3": 0.063, "hlbl_g2_0": 0.051, "hlbl_g2_1": 0.083, "hlbl_fin_1": 0.156, "tabla5_0": 0.054, "tabla5_1": 0.083, "sem_jug_0": 0.02, "sem_jug_2": 0.061, "llave_0": 0.05, "llave_1": 0.065, "sem_com_1": 0.056, "sem_com_2": 0.044, "loly_j1_1": 0.049, "loly_j1_2": 0.067, "loly_j2_0": 0.033, "loly_j2_2": 0.042, "loly_j2_4": 0.034, "loly_j3_1": 0.034, "loly_j3_2": 0.053, "loly_fin_1": 0.034, "kcmk_res_0": 0.075, "kcmk_res_1": 0.043, "kcmk_j3_0": 0.05, "kcmk_j3_1": 0.043, "kcmk_j3_2": 0.048, "kcmk_j1_0": 0.052, "kcmk_j1_2": 0.041, "kcmk_j1_4": 0.101, "kcmk_j1_5": 0.05, "kcmk_j1_6": 0.063, "kcmk_j2_0": 0.048, "kcmk_j2_2": 0.093, "kcmk_j2_3": 0.034, "kcmk_j2_4": 0.04, "kcmk_peor_0": 0.037, "kcmk_mvp_0": 0.078, "kcmk_mvp_1": 0.041, "correcciones_0": 0.032, "donde_0": 0.073, "t1ko_j_2": 0.04, "t1ko_j_3": 0.091, "t1ko_rep_0": 0.083, "lyig_j1_1": 0.042, "lyig_j1_2": 0.036, "lyig_j1_3": 0.075, "lyig_j2_2": 0.034, "lyig_j2_3": 0.112, "lyig_j2_4": 0.027, "lyig_peor_0": 0.056, "kccf_res_0": 0.061, "kccf_j_1": 0.055, "kccf_j_2": 0.1, "kccf_peor_0": 0.064, "kccf_peor_1": 0.039, "blte_res_0": 0.113, "blte_peor_0": 0.029, "blte_peor_1": 0.067, "blte_peor_2": 0.096, "blte_peor_3": 0.058, "blte_j_0": 0.083, "blte_j_2": 0.084, "blte_j_3": 0.07, "lotl_res_2": 0.035, "lotl_j_2": 0.085, "lotl_j_3": 0.053, "lotl_peor_1": 0.041, "lotl_j2_0": 0.048, "lotl_j2_1": 0.044, "lotl_fin_0": 0.034, "g2hl_res_0": 0.071, "g2hl_peor_0": 0.049, "g2hl_j2_0": 0.048, "g2hl_j2_1": 0.049, "g2hl_j_1": 0.057, "g2hl_j_2": 0.034, "g2hl_j_3": 0.074, "tabla4_0": 0.072, "tabla4_1": 0.038, "tabla4_2": 0.037}
TAIL_MAX_POR_FRASE = {"hlbl_res_0": 0.96, "hlbl_res_1": 0.85, "hlbl_j1_0": 0.69, "hlbl_j1_1": 0.11, "hlbl_j1_2": 0.61, "hlbl_j1_3": 0.72, "hlbl_g2_0": 0.73, "hlbl_g2_1": 0.76, "hlbl_fin_1": 0.41, "tabla5_0": 0.99, "tabla5_1": 0.59, "sem_jug_0": 1.2, "sem_jug_2": 1.09, "llave_0": 1.03, "llave_1": 0.6, "sem_com_1": 0.36, "sem_com_2": 0.7, "loly_j1_1": 0.75, "loly_j1_2": 0.9, "loly_j2_0": 0.59, "loly_j2_2": 0.29, "loly_j2_4": 0.69, "loly_j3_1": 0.31, "loly_j3_2": 0.77, "loly_fin_1": 0.73, "kcmk_res_0": 0.94, "kcmk_res_1": 0.77, "kcmk_j3_0": 0.8, "kcmk_j3_1": 1.23, "kcmk_j3_2": 0.82, "kcmk_j1_0": 0.88, "kcmk_j1_2": 0.8, "kcmk_j1_4": 0.37, "kcmk_j1_5": 1.28, "kcmk_j1_6": 0.77, "kcmk_j2_0": 0.93, "kcmk_j2_2": 0.28, "kcmk_j2_3": 0.73, "kcmk_j2_4": 0.97, "kcmk_peor_0": 0.64, "kcmk_mvp_0": 0.89, "kcmk_mvp_1": 0.68, "correcciones_0": 1.31, "donde_0": 0.99, "t1ko_j_2": 0.2, "t1ko_j_3": 1.14, "t1ko_rep_0": 0.27, "lyig_j1_1": 0.67, "lyig_j1_2": 0.94, "lyig_j1_3": 1.19, "lyig_j2_2": 0.54, "lyig_j2_3": 1.3, "lyig_j2_4": 1.11, "lyig_peor_0": 1.09, "kccf_res_0": 1.03, "kccf_j_1": 1.04, "kccf_j_2": 1.28, "kccf_peor_0": 0.73, "kccf_peor_1": 0.8, "blte_res_0": 0.94, "blte_peor_0": 1.36, "blte_peor_1": 1.19, "blte_peor_2": 0.68, "blte_peor_3": 0.91, "blte_j_0": 1.08, "blte_j_2": 1.02, "blte_j_3": 1.1, "lotl_res_2": 0.86, "lotl_j_2": 0.71, "lotl_j_3": 1.0, "lotl_peor_1": 0.21, "lotl_j2_0": 0.58, "lotl_j2_1": 0.45, "lotl_fin_0": 0.67, "g2hl_res_0": 0.55, "g2hl_peor_0": 0.87, "g2hl_j2_0": 0.97, "g2hl_j2_1": 0.57, "g2hl_j_1": 0.91, "g2hl_j_2": 0.54, "g2hl_j_3": 0.73, "tabla4_0": 0.86, "tabla4_1": 0.33, "tabla4_2": 1.14}

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
    tramos=[(["gancho", "correcciones", "donde", "t1ko_res"], "Apertura de resumen, tensa y expectante."),
            (["t1ko_g1", "t1ko_j", "t1ko_rep", "t1ko_peor"], "Análisis con pausas, pulso constante."),
            (["lyig_res", "lyig_j1", "lyig_j2"], "Análisis con pausas, sube hacia la jugada del minuto dos."),
            (["lyig_peor", "kccf_res", "kccf_j", "kccf_peor"], "A muerte: oscuro y urgente."),
            (["blte_res", "blte_peor", "blte_j"], "La mejor serie: la más intensa."),
            (["blte_fin", "lotl_res", "lotl_j", "lotl_rep"], "Serie larga, épica contenida."),
            (["lotl_peor", "lotl_j2", "lotl_fin", "g2hl_res", "g2hl_peor"], "Vaivén y caída."),
            (["g2hl_j2", "g2hl_j", "tabla4"], "Cierre del acto: remate y expectación."),
            (["kcmk_res", "kcmk_j3", "kcmk_j1"], "Sábado, a muerte: arranque urgente, pulso de análisis."),
            (["kcmk_j2", "kcmk_peor", "kcmk_mvp"], "Remate de serie y reconocimiento."),
            (["loly_res", "loly_j1", "loly_base"], "Serie del equipo mexicano: tensión que sube."),
            (["loly_j2", "loly_j3", "loly_fin"], "Vaivén hasta el tercer juego y alivio."),
            (["hlbl_res", "hlbl_j1", "hlbl_g2", "hlbl_fin"], "Última serie: tensión, remontada y golpe final."),
            (["tabla5", "sem_jug", "sem_eq"], "Premios de la semana: triunfal y brillante."),
            (["sem_peor", "llave", "sem_com"], "Lo peor, la llave y despedida cálida.")])
# Tramos EN VIVO (narración original en español, vivos_audio.py → audio/ambiente.wav): la música baja 16 dB para oírla.
# Salen de investigacion/vivos.json (lo escribe efectos.py); los que quedan a menos de 4 s se unen para que la música no bombee.
_VIVOS = []
for _v in sorted(_json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "investigacion", "vivos.json"), encoding="utf-8")),
                 key=lambda x: x[3]):
    if _VIVOS and _v[3] - _VIVOS[-1][1] < 4.0:
        _VIVOS[-1] = (_VIVOS[-1][0], max(_VIVOS[-1][1], _v[4]))
    else:
        _VIVOS.append((_v[3], _v[4]))
MEZCLA = dict(musica_curva=[(0, 0)] + [p for a, b in _VIVOS for p in ((a, 0), (a + min(1.5, (b - a) * .4), -16), (b - min(1.0, (b - a) * .3), -16), (b + .5, 0))]
              + [(2000, 0)])
# Silencios DENTRO de las frases ya grabadas (espaciar_voz.py, sin regenerar voz): el VOD corre a x1 y cada muerte cae cuando la voz la
# nombra (nunca cámara rápida, 31-oct-2026). (palabra, aparición, segundos antes de ella); "$ini" = antes de la primera, "$fin" = tras la última.
ESPACIOS_VOZ = {      # 4.º valor = segundo de la pausa REAL en voz/final_orig (pausas_frase.py): los tiempos de palabra fallan hasta 0,9 s
    "hlbl_j1_1": [("$ini", 0, 9.3)],
    "hlbl_j1_2": [("$ini", 0, 9.0), ("Zeus", 0, 2.4, 6.5)],
    "t1ko_g1_0": [("Cinco", 0, 7.0, 7.29), ("alma", 0, 1.2, 8.63)],
    "t1ko_j_1": [("van", 0, 2.6)],
    "t1ko_j_3": [("$ini", 0, 2.2), ("Doran", 0, .4), ("Keria", 0, .6), ("Peyz", 0, .55), ("Y", 0, 1.95), ("Cinco", 0, .35)],
    "t1ko_peor_1": [("$ini", 0, 8.6), ("Keria", 0, 6.7), ("y", 0, 6.1), ("Tres", 0, 1.5)],
    "lyig_res_0": [("cuadruple", 0, 12.2, 6.37)],
    "lyig_j1_3": [("$ini", 0, 1.0), ("Berserker", 0, 1.0, 1.74), ("Dhokla", 0, 5.0, 3.36), ("Tres", 0, 1.6, 4.87), ("De", 0, 1.8, 6.07)],
    "lyig_j2_3": [("$ini", 0, 2.85), ("JiaQi", 0, 6.1, 1.93), ("Isles", 0, .45, 4.03), ("Queda", 0, .45, 5.91)],
    "lyig_peor_1": [("$ini", 0, 3.4)],
    "kccf_j_2": [("$ini", 0, 6.2), ("Yike", 0, 4.2, 1.4), ("Canna", 0, 2.2, 3.21), ("y", 1, 2.5, 4.85), ("Cuatro", 0, 1.4, 6.82)],
    "kccf_peor_1": [("$ini", 0, 6.4), ("y", 1, 1.5, 1.27), ("Cinco", 1, 9.8, 3.93), ("dragon", 0, 1.0, 5.01)],
    "blte_peor_0": [("Ya", 0, 1.6)],
    "blte_peor_2": [("$ini", 0, 6.0), ("369", 0, .6, 1.72), ("JackeyLove", 0, 5.9, 4.01), ("y", 0, 5.2, 6.0)],
    "blte_j_2": [("Bin", 0, .9, 4.84)],
    "blte_j_3": [("$ini", 0, .6), ("Creme", 0, 1.45, 2.32), ("JackeyLove", 0, 12.3, 3.77), ("369", 1, 7.8, 5.47), ("Cuatro", 0, 1.7, 7.4)],
    "lotl_j_1": [("$fin", 0, 1.4)],
    "lotl_j_3": [("Ackerman", 0, .55), ("Zest", 0, .45), ("doble", 0, 2.3), ("triple", 0, .95)],
    "lotl_peor_0": [("Un", 0, 4.5)],
    "lotl_j2_0": [("El", 1, 2.8, 3.94), ("Ocho", 0, 2.0, 5.3), ("Alma", 0, 7.8, 9.03), ("$fin", 0, .4)],
    "g2hl_peor_1": [("y", 0, 6.5, 3.87)],
    "g2hl_peor_2": [("$ini", 0, 2.6), ("Esa", 0, 2.2)],
    "g2hl_j2_1": [("$ini", 0, 4.4)],
    "g2hl_j_1": [("Pero", 0, 2.7)],
    "g2hl_j_2": [("$ini", 0, 2.0)],
    "g2hl_j_3": [("$ini", 0, 11.8), ("y", 0, 5.2, 3.78), ("Hanwha", 0, 2.3, 6.2)],
    "kcmk_j3_2": [("$ini", 0, 1.0), ("Supa", 0, 2.2, 2.05), ("Myrwn", 0, .4, 3.63), ("Elyoya", 0, 7.4, 5.24), ("Y", 1, 1.0, 6.88), ("$fin", 0, 1.6)],
    "kcmk_j1_1": [("Los", 0, 3.2, 1.23), ("y", 0, 1.6, 3.66)],
    "kcmk_j1_3": [("Canna", 1, .4, 5.18)],
    "kcmk_j1_4": [("Y", 0, .6, 2.03), ("Canna", 0, .2, 3.97)],
    "kcmk_j1_5": [("Veinticinco", 0, 2.6, 4.78)],
    "kcmk_j2_2": [("$fin", 0, 1.0)],
    "kcmk_j2_3": [("primera", 0, .3, 1.76), ("y", 1, 1.2, 4.39), ("lo", 0, 1.2, 6.26)],
    "loly_j1_1": [("Lo", 0, 1.0, 1.92)],
    "loly_j1_2": [("Inspired", 0, 1.4, 2.04), ("doble", 0, 1.4, 6.58)],
    "loly_j1_3": [("Diez", 0, 3.6, 3.18)],
    "loly_base_0": [("Los", 0, 3.4, 5.43), ("y", 3, 9.8, 7.38)],
    "loly_j2_2": [("$ini", 0, 2.6), ("Pero", 0, .7, 1.92)],
    "loly_j2_3": [("$ini", 0, 2.4), ("doble", 0, 3.5, 3.23)],
    "loly_j3_2": [("$ini", 0, 5.3), ("doble", 0, .7, 3.31)],
}

ESCENAS = [
    # ── GANCHO (~45 s; SIN SPOILER) ──────────────────────────────────────────────
    {"id": "gancho", "pre": 3.0, "frases": [
        "Seis plazas para cuartos de final. Catorce equipos vivos. Nueve series.",
        "Esta semana vimos a un equipo ir cinco mil de oro arriba, y perder en un minuto a cuatro jugadores y el Barón. Un muro que partió a un equipo por la mitad. Una pausa de veintinueve minutos en plena serie. Y una jugada en el minuto dos que decidió quién pasaba.",
        "En el video pasado, Julio nos escribió esto: el mejor resumen que he visto hasta el momento, espero seguir viendo más resúmenes así. Aquí está, Julio. Todos los comentarios se leen, y este video se hizo con ellos.",
        "[short pause] Las mejores jugadas, analizadas pausa por pausa. Lo mejor y lo peor de cada equipo. Los jugadores de la semana. Y cómo quedan los cuartos de final.",
    ]},
    # ── CORRECCIONES (~25 s) ─────────────────────────────────────────────────────
    {"id": "correcciones", "pre": 0.4, "frases": [
        "Antes, dos correcciones que nos hicieron ustedes. Rodolfo nos recordó que LYON no es un equipo de Estados Unidos: es una organización mexicana, aunque juegue en la liga de Norteamérica. Tiene toda la razón.",
        "Y a un comentario que solo dice «el primer sembrado» le dieron quince me gusta. Mensaje recibido. Esa palabra se queda en el campo.",
    ]},
    # ── DÓNDE ESTÁBAMOS (~35 s) ──────────────────────────────────────────────────
    {"id": "donde", "pre": 0.4, "frases": [
        "Así llegamos a esta semana. Dplus KIA y Gen.G ya estaban en cuartos, los dos invictos. Team Secret Whales y Anyone's Legend ya se habían ido, sin ganar una sola partida.",
        "En medio, doce equipos. Seis con dos victorias, que jugaban por el pase. Seis con dos derrotas, a una serie de irse a casa.",
        "Todo al mejor de tres, y con Fearless: un campeón que ya se usó en la serie no se puede repetir.",
    ]},
    # ── MIÉRCOLES · T1 vs MOVISTAR KOI ───────────────────────────────────────────
    {"id": "t1ko_res", "pre": 0.6, "frases": [
        "Miércoles. Abre T1, que busca su cuarto título seguido, contra Movistar KOI. El que gana, a cuartos.",
        "La primera partida duró casi cuarenta minutos y el oro cambió de manos tres veces: KOI arriba, T1 casi seis mil arriba, y otra vez KOI, dos mil arriba.",
    ]},
    {"id": "t1ko_g1", "pre": 12.0, "post": 5.0, "frases": [
        "Doran no murió en toda la serie, y en el minuto treinta y nueve, con su equipo mil quinientos abajo, se lanzó con todo. Cinco por cero, alma del dragón y nexo.",
    ]},
    {"id": "t1ko_j", "pre": 12.0, "post": 4.5, "frases": [
        "La segunda hay que verla en pausa. Minuto diecinueve, T1 va cinco mil seiscientos arriba y empieza el dragón.",
        "Oner se adelanta solo con Jarvan y queda mal parado. Los narradores lo llamaron carnada. Si fue plan, nadie lo sabe, pero KOI se la come: van todos por él.",
        "Ahora mira quién falta. Faker, con Orianna, viene por el flanco.",
        "Oner mata a Jojopyun. Doran a Supa, Keria a Alvaro, Peyz a Elyoya. Y Faker cierra con Myrwn. Cinco por cero, y Oner sigue vivo.",
    ]},
    {"id": "t1ko_rep", "pre": 7.0, "frases": [
        "T1 gana dos a cero y se mete a cuartos. KOI baja a dos victorias y dos derrotas.",
    ]},
    {"id": "t1ko_peor", "pre": 0.5, "frases": [
        "Lo peor de KOI pasó diez minutos antes. Elyoya se mete a robar a la jungla de T1. Keria y Doran le caen encima.",
        "Doran lo mata, Keria caza a Alvaro por el río, y Doran se lleva también a Supa. Tres por cero, gratis. KOI no derribó una sola torre en esa partida.",
    ]},
    # ── MIÉRCOLES · LYON vs INVICTUS ─────────────────────────────────────────────
    {"id": "lyig_res", "pre": 0.6, "frases": [
        "Esa misma tarde, LYON contra Invictus Gaming, también por el pase. La primera fue de Rookie: cuádruple y ace en el minuto veinticinco. Diecinueve a cuatro.",
    ]},
    {"id": "lyig_j1", "pre": 12.0, "frases": [
        "Pero LYON respondió. Segunda partida, minuto veintiocho. Invictus tenía el Barón y aun así iba mil cuatrocientos abajo.",
        "Invictus se junta antes del dragón. Dhokla llega por la izquierda. Y mira a Isles, con Alistar, a esta distancia.",
        "Destello, y cae encima de la línea trasera. Meiko sale volando, y JiaQi también.",
        "Inspired mata a JiaQi, Berserker a Rookie, Dhokla a Wei. Tres por cero. De mil cuatrocientos a casi cinco mil arriba, y LYON empata la serie.",
    ]},
    {"id": "lyig_j2", "pre": 12.0, "frases": [
        "Y la jugada que decidió la serie pasó en el minuto dos de la tercera partida.",
        "Inspired baja por la torre sobre la pareja de Invictus. Es una emboscada. Meiko, con Lux, no huye: va de frente.",
        "Atrapa a Berserker con la prisión de luz y se pasa al otro lado. Primera sangre para JiaQi.",
        "Inspired mata a Meiko, JiaQi mata a Inspired, Isles mata a JiaQi. Queda dos por dos. Pero los dos asesinatos son del tirador.",
        "Los narradores lo dijeron: una bola de nieve. Invictus fue arriba en oro el resto de la partida. JiaQi hizo cinco de los siete asesinatos, Invictus gana dos a uno y se va a cuartos.",
    ]},
    {"id": "lyig_peor", "pre": 0.5, "post": 1.8, "frases": [
        "Lo peor de esa serie: Inspired en la primera partida, minuto doce, pegándole a un campamento en la jungla de Invictus. Wei encima, Rookie por arriba, Meiko y JiaQi por abajo.",
        "Terminó con un asesinato y seis muertes. Un narrador lo resumió: no está muy inspirado el día de hoy.",
    ]},
    # ── JUEVES · KC vs CFO ───────────────────────────────────────────────────────
    {"id": "kccf_res", "pre": 0.6, "frases": [
        "Jueves. Karmine Corp contra CTBC Flying Oyster, los dos con dos derrotas. El que pierde se va.",
        "La primera fue una paliza: diecinueve a tres, y CFO sin una sola torre. Doggo, su tirador, terminó con cero asesinatos, tres muertes y cero asistencias.",
        "La segunda tuvo dos pausas por el equipo de Doggo: siete minutos, y luego veintinueve, porque no podía comprar un objeto. Veintinueve minutos.",
    ]},
    {"id": "kccf_j", "pre": 12.0, "frases": [
        "Pero antes de todo eso, en el minuto veinte, pasó esto. CFO va cuatro mil quinientos arriba y el Barón acaba de aparecer.",
        "Busio se adelanta, y CFO lo está esperando. Todos miran hacia él. Y Canna, con Camille, llega por la retaguardia.",
        "Va directo a Doggo. Yike mata a Rest, Canna se lleva a Kino, y Yike termina con POUT. Cuatro por cero junto al Barón.",
    ]},
    {"id": "kccf_peor", "pre": 8.0, "frases": [
        "Y lo peor de CFO llegó en el minuto treinta y cinco. Shad0w va solo al río. Un centinela lo delata, y Karmine lo espera.",
        "Yike lo mata, y CFO pelea cuatro contra cinco. Cinco por uno, dragón ancestral y nexo. CFO se va del Mundial, y con ellos, la LCP entera.",
    ]},
    # ── JUEVES · BLG vs TES ──────────────────────────────────────────────────────
    {"id": "blte_res", "pre": 12.0, "frases": [
        "Esa noche, la mejor serie de la semana. Bilibili Gaming contra Top Esports, por el pase. En la primera, Knight hizo este triple en dos segundos y Bilibili ganó veintiuno a seis.",
    ]},
    {"id": "blte_peor", "pre": 10.0, "frases": [
        "Segunda partida, minuto veintiocho. Bilibili tiene tres dragones, cinco mil doscientos de ventaja, y acaba de matar a Creme. Ya ganó la pelea.",
        "Pero se queda dentro de la jungla de TES. Míralos: cuatro grupos. Xun arriba, casi muerto. Knight solo. Bin en el centro. Viper y ON abajo.",
        "Tian cae sobre Viper. 369 mata a ON. JackeyLove se lleva a Bin, y luego a Xun.",
        "En un minuto, Bilibili pierde a cuatro jugadores y el Barón. Y Top Esports, que no había ido mil arriba en toda la serie, se pone por delante y le quita el dragón del alma.",
    ]},
    {"id": "blte_j", "pre": 10.0, "post": 2.6, "frases": [
        "Bilibili todavía volvió: dos mil arriba en el minuto treinta y seis. Entonces TES empieza el Barón.",
        "Barón en cuatro mil seiscientos. Los cinco de Bilibili se meten al río a pelearlo.",
        "Y aquí TES deja de pegarle. Lo suelta en tres mil quinientos. Bin y Xun se van detrás de JackeyLove, y al otro lado, 369, Tian y Creme caen sobre Viper y ON.",
        "369 mata a Viper. Creme a ON. JackeyLove a Bin. 369 a Knight. Cuatro muertes de Bilibili, ninguna de TES, y de ahí directo al nexo.",
    ]},
    {"id": "blte_fin", "pre": 0.6, "frases": [
        "La tercera ya no tuvo historia: diecisiete a tres. 369 no murió ni una vez en las dos últimas partidas. Viper no hizo un solo asesinato. TES a cuartos.",
    ]},
    # ── VIERNES · LOS vs TEAM LIQUID ─────────────────────────────────────────────
    {"id": "lotl_res", "pre": 0.6, "frases": [
        "Viernes. Team Liquid, el que eliminó al campeón de China, contra Los Grandes. Otra vez, el que pierde se va.",
        "En el video pasado, Felo nos reclamó: ¿y Josedeodo? Él es el mega MVP de todo el torneo. Pues esta fue su serie.",
        "La primera fue de LOS: Curse, con Trundle, siete asesinatos sin morir. Liquid empató la segunda con alma, Barón y Anciano. Todo a una tercera de cuarenta y siete minutos.",
    ]},
    {"id": "lotl_j", "pre": 10.0, "post": 4.0, "frases": [
        "Minuto treinta y cuatro. Liquid ya había recortado de siete mil abajo a tres mil trescientos, y tiene el Barón encima.",
        "Pelean el dragón en el río. Curse cae junto a su equipo. Y Feisty lanza esto.",
        "El muro de Taliyah cruza el río por encima del foso. CoreJJ y Quid se quedan al norte. Yeon y Josedeodo, al sur, dentro, con todo LOS encima.",
        "Liquid gana el dragón, pero ya está partido en dos. Ackerman mata a Yeon. Zest mata a Josedeodo, y sigue: doble, triple.",
        "Cuatro por cero. LOS tira torre e inhibidor, y vuelve casi a siete mil arriba.",
    ]},
    {"id": "lotl_rep", "pre": 8.0, "frases": [
        "Mírala otra vez. Divide al equipo completo, y entonces los van matando uno por uno.",
    ]},
    {"id": "lotl_peor", "pre": 0.5, "frases": [
        "Casi lo regalan. Minuto treinta y ocho. Duduhh no había muerto en toda la partida, se va solo por delante de su equipo y cae. Un narrador dijo que se sintió el dios.",
        "Sesenta y cuatro segundos después, Liquid tomaba el Barón.",
    ]},
    {"id": "lotl_j2", "pre": 6.0, "frases": [
        "Pero mientras Liquid mata al Barón, LOS ya está en el río. El dragón aparece. Ocho segundos después, otro muro de Feisty y es de LOS. Alma.",
        "Liquid ganó dos Barones en esa partida, y la perdió.",
    ]},
    {"id": "lotl_fin", "pre": 0.6, "frases": [
        "Zest, con Tristana en el top: diez asesinatos, una muerte. LOS gana dos a uno. Team Liquid se va del Mundial, y Felo, lo sentimos: Josedeodo terminó con nueve asesinatos y siete muertes.",
    ]},
    # ── VIERNES · G2 vs HANWHA ───────────────────────────────────────────────────
    {"id": "g2hl_res", "pre": 0.6, "frases": [
        "Y esa noche, G2 contra Hanwha Life. El que pierde se va. G2 mandó los primeros catorce minutos.",
    ]},
    {"id": "g2hl_peor", "pre": 10.0, "frases": [
        "Minuto catorce. G2 acaba de ganar una pelea, va seis a cuatro. BrokenBlade, con Olaf, se va detrás de Zeus, hacia la torre de Hanwha.",
        "Doce segundos persiguiéndolo. Las barras se van igualando, y cuando BrokenBlade ya casi no tiene vida, Zeus se da la vuelta.",
        "Lo mata solo. Esa fue la última vez que G2 estuvo arriba en el oro en toda la partida. Terminó veintidós a once.",
    ]},
    {"id": "g2hl_j2", "pre": 6.0, "post": 4.9, "frases": [
        "Segunda partida, minuto quince. Zeka, con Swain, se queda solo contra tres. Labrov lo encanta, Caps lo provoca, y Hans Sama está al lado.",
        "Su vida baja a setecientos treinta y siete. Y no muere. Zeka no murió en toda esa partida.",
    ]},
    {"id": "g2hl_j", "pre": 12.0, "frases": [
        "Aun así G2 iba novecientos arriba en el minuto veintiuno, y BrokenBlade llevaba cuatro asesinatos sin morir.",
        "G2 inicia con Labrov y BrokenBlade. Pero Hanwha se les había adelantado: Swain entra con su definitiva, y Kanavi llega por arriba.",
        "Caps se mete en medio de todos, provoca a cuatro y se lleva a Zeus. Es la única baja de Hanwha.",
        "Gumayusi hace triple, Kanavi remata a Hans Sama, y es ace. Cinco por uno. Hanwha gana dos a cero, y G2 se va del Mundial.",
    ]},
    # ── LA MESA TRAS CUATRO RONDAS (~30 s) ───────────────────────────────────────
    {"id": "tabla4", "pre": 0.6, "frases": [
        "Así quedó la mesa tras cuatro rondas. T1, Invictus y Top Esports, a cuartos, con Dplus KIA y Gen.G.",
        "CFO, Team Liquid y G2, a casa, con Team Secret Whales y Anyone's Legend.",
        "Y quedaban seis equipos para tres plazas. Tres cruces a muerte: Karmine contra Movistar KOI, Los Grandes contra LYON, Hanwha contra Bilibili.",
    ]},
    # ── ACTO B: aquí siguen las 3 series del sábado, premios, llave y cierre ─────
    # ── SÁBADO · KARMINE vs MOVISTAR KOI (datos_kcmk.md) ─────────────────────────
    {"id": "kcmk_res", "pre": 0.6, "frases": [
        "Sábado. Karmine contra KOI. Los dos llevan dos victorias y dos derrotas, y el que pierde se va.",
        "La primera pasó catorce minutos sin una sola muerte. Luego Karmine se llevó el alma del dragón y el Barón, y en el minuto veintinueve iba mil seiscientos arriba.",
    ]},
    {"id": "kcmk_j3", "pre": 12.0, "frases": [
        "Lo peor de Karmine pasó ahí. Tiene la mejora del Barón, el dragón Anciano está bajando, y kyeahoo se fue aparte a tirar una torre.",
        "Aturden a Caliste junto al Anciano. Lo levantan a él, levantan a Busio, y Myrwn, con Camille, llega por la izquierda y se le pega. Un narrador no lo podía creer: se regaló.",
        "Jojopyun mata a Caliste. Supa a kyeahoo. Myrwn a Busio. Elyoya a Yike. Y Jojopyun cierra el ace.",
        "Cinco por cero y el Anciano. En cuarenta y ocho segundos, de mil seiscientos arriba a tres mil abajo.",
    ]},
    {"id": "kcmk_j1", "pre": 12.0, "frases": [
        "Ocho minutos después, Karmine sigue tres mil abajo, y hay otro Anciano en juego.",
        "kyeahoo no está. Los narradores dicen que volvió a base, y que KOI vio su teletransporte y por eso entró: cinco contra cuatro.",
        "Myrwn encierra a Caliste con su hexágono, y dos de Karmine salen volando. Replegarse, según los narradores, era perder.",
        "Pero Canna se va al frente, solo, encima de Supa, y parte la pelea en dos. Canna y Myrwn reviven al mismo tiempo. Y por abajo entra kyeahoo, con la vida llena.",
        "Caliste mata a Elyoya. Y a Myrwn: doble. Canna cae.",
        "Y cuatro de Karmine le bajan al Anciano quince mil de vida en nueve segundos. Veinticinco segundos después, también el Barón.",
        "De tres mil abajo a dos mil quinientos arriba. Karmine ganó la primera con menos asesinatos que KOI: trece a catorce.",
    ]},
    {"id": "kcmk_j2", "pre": 12.0, "frases": [
        "La segunda empezó en el minuto cuatro. Canna, con Rumble, está solo arriba, Myrwn se le pega, y Elyoya baja por la derecha. Dos contra uno.",
        "Cuarenta por ciento de vida, y Canna no gasta el Destello. Los narradores lo vieron: están muy confiados, y él espera.",
        "Aparece Yike por la izquierda, y Canna saca el fuego.",
        "Yike mata a Myrwn: primera sangre. Elyoya huye, y Canna, casi sin vida, lo remata. Dos por cero.",
        "Desde ahí, Karmine no volvió a ir abajo en toda la partida. Veintiséis minutos, dieciocho a cuatro, quince mil de oro arriba.",
    ]},
    {"id": "kcmk_peor", "pre": 0.5, "frases": [
        "Lo peor de KOI, otra vez: Elyoya. En la segunda, un asesinato y cinco muertes, dos de ellas antes del minuto siete. Hizo menos daño que su propio soporte.",
    ]},
    {"id": "kcmk_mvp", "pre": 0.5, "post": 1.5, "frases": [
        "Y el mejor de la serie, Yike: once de los treinta y un asesinatos de Karmine. En la segunda, nueve, cinco asistencias, y ni una muerte.",
        "Karmine gana dos a cero y se mete a cuartos. Movistar KOI, que el miércoles estaba a una serie del pase, se va del Mundial.",
    ]},
    # ── SÁBADO · LOS GRANDES vs LYON (datos_loly.md) ─────────────────────────────
    {"id": "loly_res", "pre": 0.6, "frases": [
        "Esa tarde, Los Grandes contra LYON. Otra vez, el que pierde se va. La primera fue de Los Grandes: dos Barones, y nunca fueron abajo en el oro.",
        "La segunda iba igual. Los Grandes llegaron a ir ocho mil cuatrocientos arriba, con dos Barones más. Los narradores llevaban veinte minutos diciendo que tenían que cerrar.",
    ]},
    {"id": "loly_j1", "pre": 12.0, "frases": [
        "Minuto cuarenta. Siete mil ochocientos arriba, y los diez están alrededor del dragón del alma.",
        "Curse cae sobre Berserker. Lo inmovilizan a media vida, con Feisty y Curse encima. Isles está aturdido, lejos. Está solo contra todos.",
        "Berserker mata a Curse. Inspired mata a Zest. Y Berserker remata a Duduhh: doble.",
        "Tres por cero, sin una sola baja de LYON. Diez segundos después, también el alma.",
    ]},
    {"id": "loly_base", "pre": 0.5, "post": 1.5, "frases": [
        "Y el final: minuto cuarenta y seis. Berserker mata a Zest y tira un inhibidor. Los Grandes se llevan el Anciano, y quince segundos después pierden el nexo.",
        "LYON ganó con tres mil de oro menos, y con el Anciano en contra. Los narradores lo dijeron después: esa partida, Los Grandes la tenían en la mano.",
    ]},
    {"id": "loly_j2", "pre": 12.0, "frases": [
        "Tercera partida, minuto veintinueve. Los Grandes tienen el Barón y van mil cuatrocientos arriba.",
        "Berserker persigue de más, y los narradores lo llamaron un error gravísimo. Lo inmovilizan, adelantado.",
        "Duduhh mata a Berserker. Pero Dhokla cae sobre Duduhh y lo mata.",
        "Saint mata a Ackerman, y luego a Feisty: doble.",
        "Tres por uno, con el Barón en contra. Inspired ni siquiera cae: revive con su Ángel Guardián.",
    ]},
    {"id": "loly_j3", "pre": 10.0, "frases": [
        "Y lo peor de Los Grandes llegó cuatro minutos después. Zest se va de la pelea casi sin vida, y quedan cuatro.",
        "Ackerman ya estaba salvado, dicen los narradores, y usó su definitiva hacia delante.",
        "Berserker mata a Ackerman, y luego a Duduhh: doble. Y LYON se lleva el inhibidor.",
        "Ackerman terminó esa partida sin un asesinato y con cinco muertes.",
    ]},
    {"id": "loly_fin", "pre": 0.5, "post": 1.5, "frases": [
        "El mejor de la serie, Berserker: dieciséis de los treinta y cuatro asesinatos de LYON. E Inspired murió una sola vez en casi dos horas de juego.",
        "LYON gana dos a uno y se mete a cuartos. Rodolfo, ahí lo tienes. Los Grandes se va del Mundial.",
    ]},
    # ── SÁBADO · HANWHA vs BILIBILI (datos_hlbl.md) ──────────────────────────────
    {"id": "hlbl_res", "pre": 0.6, "frases": [
        "Y la última del sábado: Hanwha Life contra Bilibili. Otra vez, el que pierde se va.",
        "En la primera, Hanwha mandó desde el minuto diecisiete. Barón, siete torres contra tres, y un inhibidor. En el minuto treinta y nueve iba cinco mil seiscientos arriba.",
    ]},
    {"id": "hlbl_j1", "pre": 12.0, "frases": [
        "Minuto cuarenta y uno. Bilibili acaba de llevarse el alma, pero sigue cuatro mil abajo.",
        "Bin entra primero, y cae.",
        "Y entonces, Knight. Una onda de choque de Orianna. Kanavi. Gumayusi y Zeka. Zeus. Cuatro asesinatos en cuatro segundos.",
        "Viper remata a Delight: cinco por uno. Cuarenta segundos después, el nexo de Hanwha cae.",
    ]},
    {"id": "hlbl_g2", "pre": 0.5, "frases": [
        "La segunda fue de un solo lado. Bilibili se llevó cuatro dragones y el alma, y en el minuto veintinueve ganó una pelea cinco por uno, con tres asesinatos de Knight.",
        "Catorce a tres. Diez torres contra cero: Hanwha no tiró ni una. Lo peor de Hanwha, Zeus: cero asesinatos y cuatro muertes.",
    ]},
    {"id": "hlbl_fin", "pre": 0.5, "post": 1.5, "frases": [
        "El mejor de la serie, Knight: quince asesinatos y una sola muerte en dos partidas.",
        "Bilibili gana dos a cero y se mete a cuartos. Hanwha Life se va del Mundial.",
    ]},
    # ── CIERRE (semana.json = K/D/A de la semana) ──
    {"id": "tabla5", "pre": 0.6, "frases": [
        "Así termina la fase suiza. A cuartos: Dplus KIA y Gen.G, sin perder una serie. T1, Invictus y Top Esports. Y en la última ronda, Karmine, LYON y Bilibili.",
        "A casa: Movistar KOI, Los Grandes y Hanwha Life, con los cinco que ya se habían ido.",
    ]},
    {"id": "sem_jug", "pre": 0.5, "frases": [
        "Los jugadores de la semana. Tercero, Doran: dos partidas contra KOI, diez asesinatos, trece asistencias, y ni una sola muerte.",
        "Segundo, kyeahoo, el central de Karmine: cuatro partidas a muerte, dieciséis asesinatos y solo tres muertes.",
        "Y el primero, Knight. Treinta asesinatos en cinco partidas, más que nadie en la semana. Un triple contra Top Esports, y el cuádruple que eliminó a Hanwha.",
    ]},
    {"id": "sem_eq", "pre": 0.6, "frases": [
        "El equipo de la semana: Karmine Corp. Llegó desde la fase de entrada, y tras tres rondas tenía una victoria y dos derrotas.",
        "Desde ahí jugó dos series en las que perder era irse a casa. Cuatro partidas. Cuatro victorias.",
    ]},
    {"id": "sem_peor", "pre": 0.5, "frases": [
        "Y lo peor de la semana: Los Grandes, en la segunda partida contra LYON. Ocho mil cuatrocientos de oro arriba, dos Barones, y veinte minutos de narradores pidiéndoles que cerraran.",
        "No cerraron. Y esa partida les costó el Mundial.",
    ]},
    {"id": "llave", "pre": 0.5, "frases": [
        "Y los cuartos de final ya tienen sorteo. Dplus KIA contra Bilibili. Gen.G contra LYON. Y Karmine contra T1, que va por su cuarto título seguido.",
        "Y un duelo chino: Top Esports contra Invictus. Al mejor de cinco, del martes al viernes, en Texas.",
    ]},
    {"id": "sem_com", "pre": 0.5, "post": 2.5, "frases": [
        "Antes de irnos, gracias por cada comentario. Armando nos dijo que le gustó la edición, y que una voz humana le daría el toque final. Lo tomamos en cuenta.",
        "A quien nos dejó un «ta bueno el resumen»: corto, pero se agradece igual.",
        "Y a quien escribió «buen video, chat gpt, sigue así», con diecisiete me gusta: gracias, se lo pasamos. Aunque ChatGPT no se quedó a ver los veintinueve minutos de pausa de CFO. Esos los vimos nosotros. Enteros.",
        "Todos los comentarios se leen, y el próximo video se hace con ellos. Nos vemos en los cuartos.",
    ]},
]
