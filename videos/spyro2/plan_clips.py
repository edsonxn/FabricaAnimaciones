# -*- coding: utf-8 -*-
"""Plan de clips de spyro2 (31-oct-2026; estructura de mario64_secretos/bt_mundos_ranking): para cada beat (scene-001…174) un video de YouTube y el
segundo donde empieza su clip (el motor corta duración del beat + 0,3 s). Segundos elegidos MIRANDO hojas propias de ver/mxp_360.mp4 (ModernXP,
1080p60, 5:29:06, sin narrador) y de los demás videos (ver/vid, ver/sec y cortes de 360p). Escribe busquedas.json e imprime ambiente_por y
recorte_por para SECUENCIA en guion.py.
    python plan_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

FUENTES_ID = {
    "MXP": "L9ePJJp1P8E",      # ModernXP: Spyro 2 100 %, 1080p60 (1602x1080 de imagen), sin narrador. Fuente principal
    "CYLUX": "zrJSep-l3NI",    # Cylux Trashheart: todo el diálogo (1080p30, sin narrador)
    "CHEY": "a23WEJ4Nu6A",      # CheyCorner: clip de 18 s con el cuadro «torch» de Brother Ned (1080p30)
    "JL": "qNBm6CYfAQs",       # Jiggylookback «Mysteries of Spyro 2» (2160p60, CON narrador: sin ambiente)
    "JONA": "PBvTsZbyias",     # Jona MDQ: versión PAL en español (1080p50)
    "JPN": "huN86uQ8SUU",      # RedFlameFox: Spyro x Sparx Tondemo Tours, japonés (1080p60, marca de agua pequeña)
    "ZDU": "ZDuRgueoe7A",      # Hwd405: prototipo del 15-sep-1999 (1080p30; marco y rótulo grande: SOLO fuente de ese dato)
    "OT": "O-TpCNK0iDA",       # BenDoesVariety: doble salto (1152p60; cámara web + marco; única fuente limpia de la técnica)
    "PQJ": "PQJXhyGI96w",      # resbitwo: trucos de pausa (720p30, sin voz)
    "JTO": "jtOfpZqVhok",      # CrashFan00: demo de CTR dentro del disco de Spyro 2 (2160p60)
    "XZ": "xzgjmGXpzLQ",       # MojoSiah: demo de Spyro 2 dentro del disco de CTR (720p30, grabada de pantalla)
    "U7X": "u7xYngIwvjU",      # NotRiptosFather: prototipo de agosto (1080p60; cámara web abajo a la derecha)
    "X5": "5XTOT4f9Dyw",       # CrystalFissure: recorrido de Autumn Plains del prototipo (1080p30, sin marco)
}

# fracción que se recorta POR LADO (el motor recorta lo mismo en x e y y luego cubre 16:9)
RECORTE = {}   # ModernXP viene a 1602x1080 sin barras; nada que recortar

# durations de las fuentes que no son maratones (para avisar si el clip se pasa del final)
DURS = {"CHEY": 18, "JL": 643, "JPN": 36065, "PQJ": 196, "OT": 245, "JTO": 380, "XZ": 164, "U7X": 767, "X5": 314, "ZDU": 1416, "JONA": 26280,
        "CYLUX": 5587, "MXP": 19746}

PLAN = {
    1: ("JL", 65),            # la moneda dorada de la fuente (65-74 s)
    2: ("CHEY", 1.8),         # CheyCorner (1080p, 18 s): Brother Ned con el cuadro «torch» (antes del rótulo del autor)
    3: ("JL", 335),         # guía: Epilogue + lista de puntos de habilidad «Well Done!»
    4: ("JONA", 6.0),         # logos de Sony y PlayStation en la versión PAL
    5: ("MXP", 5330),         # Summer Forest bonito
    6: ("MXP", 256),          # Glimmer (inicio)
    7: ("MXP", 11.8),          # logo de Insomniac Games
    8: ("MXP", 149),          # Spyro con actitud: «you're a dragon, got a problem with that?»
    9: ("MXP", 7500),         # Skelos Badlands: vista lejana (nivel de detalle por distancia)
    10: ("MXP", 1118),        # Hunter con Spyro en Summer Forest
    11: ("MXP", 1330),        # Idol Springs: gemas
    12: ("MXP", 4.0),           # texto de copyright «Spyro (2): Ripto's Rage!»
    13: ("MXP", 1214),        # Hunter en Summer Forest
    14: ("MXP", 984),         # Elora en Glimmer: «this is the home world called Summer Forest»
    15: ("MXP", 64),          # lluvia: «Is this rain ever going to stop?»
    16: ("MXP", 135.5),       # Spyro de cerca al aterrizar en Avalar
    17: ("MXP", 162),         # cinemática de llegada: Ripto, Crush y Gulp
    18: ("MXP", 6045),        # Autumn Plains
    19: ("MXP", 13640),       # talismán tras Gulp
    20: ("PQJ", 48),          # menú de pausa con 10 000 gemas y 64 orbes
    21: ("MXP", 1090),        # Spyro nada
    22: ("MXP", 524),         # pirámide de supervuelo en Glimmer
    23: ("MXP", 2150),        # Zoe: partículas de espíritu al vencer enemigos
    24: ("MXP", 893),        # Hunter (cinemática «I'm a Faun, You Dork!»)
    25: ("MXP", 104),          # Elora y Hunter en la cinemática de la guarida
    26: ("MXP", 1062),        # Moneybags cobrando el puente
    27: ("MXP", 1470),        # Idol Springs bonito
    28: ("MXP", 12400),       # Shady Oasis
    29: ("MXP", 16100),       # Cloud Temples
    30: ("MXP", 10300),       # Scorch (desierto)
    31: ("MXP", 3000),        # Hurricos
    32: ("MXP", 9230),        # Zephyr
    33: ("MXP", 6620),        # Glimmer (parte 2): puente de 400 gemas
    34: ("MXP", 12900),       # Metro Speedway
    35: ("MXP", 24.5),        # pantalla de título «Ripto's Rage»
    36: ("JONA", 38.5),       # título «Gateway to Glimmer» con menús en español
    37: ("JPN", 24.5),        # logo japonés Spyro x Sparx
    38: ("MXP", 4100),        # Sunny Beach
    39: ("ZDU", 34),          # prototipo PAL 15-sep-99 con el logo de Ripto's Rage (marco y rótulo: dudoso)
    40: ("MXP", 3300),        # Sparx
    41: ("MXP", 1600),        # Idol Springs (parte 2)
    42: ("MXP", 1420),        # Idol Springs
    43: ("MXP", 1560),        # Idol Springs: cueva
    44: ("MXP", 5400),        # Ocean Speedway
    45: ("MXP", 1535),        # Idol Springs (la misma canción que Fracture Hills)
    46: ("MXP", 11150),       # Fracture Hills (misma canción)
    47: ("PQJ", 150),         # pausa antes del cabezón
    48: ("PQJ", 158),         # Big Head
    49: ("PQJ", 169),         # Big Head
    50: ("PQJ", 1),           # pausa + todas las habilidades
    51: ("MXP", 6700),         # prototipo de agosto
    52: ("MXP", 6730),         # prototipo
    53: ("MXP", 18556),       # créditos
    54: ("MXP", 8002),        # Moneybags y el puente de Crystal Glacier: «I could arrange for you to cross this bridge»
    55: ("MXP", 6106),        # Autumn Plains: Moneybags, «Legend has it that there is a portal…»
    56: ("MXP", 6129),        # Moneybags: Lizard Burger, bombas y TNT de los pájaros de Zephyr (6126-6138)
    57: ("MXP", 13731),       # Ripto con una bomba: «convencí al oso Moneybags»
    58: ("MXP", 8020),        # Moneybags en Crystal Glacier: condominio en Hurricos
    59: ("MXP", 6291),        # Moneybags: «No one's been through that portal in years… say hi to Ripto»
    60: ("MXP", 2570),        # pista de hockey de Colossus
    61: ("MXP", 2594),        # Brother Kipp: cinco goles antes del patinador rojo
    62: ("MXP", 2643),        # partido
    63: ("MXP", 846),         # Elora (cinemática «I'm a Faun, You Dork!»)
    64: ("MXP", 868),         # Elora y Spyro
    65: ("MXP", 880),         # Elora
    66: ("MXP", 1296),        # alas de Spyro desde atrás
    67: ("MXP", 1002),        # alas de Spyro desde atrás
    68: ("MXP", 5938),        # Spyro con actitud en «Bring It On, Shorty!»
    69: ("MXP", 13676),       # Spyro de cerca en «Spyro, You Did It!»
    70: ("MXP", 18779),       # créditos: Character Voices By
    71: ("MXP", 3120),        # los Electrolls de Hurricos
    72: ("MXP", 1148),       # Hunter en Summer Forest
    73: ("MXP", 13760),       # Ripto y Hunter en la misma escena
    74: ("MXP", 188),         # Gulp se come el cetro
    75: ("MXP", 196.5),       # «you ate my scepter»
    76: ("MXP", 13367),       # Ripto sin cetro alimenta a Gulp
    77: ("MXP", 13746),       # «new scepter»
    78: ("MXP", 18144),       # fin de la cinemática y llegada a Ripto's Arena
    79: ("MXP", 18165),       # Ripto's Arena
    80: ("MXP", 3925),        # Sunny Beach
    81: ("MXP", 3950),        # Sunny Beach
    82: ("MXP", 7100),        # Skelos Badlands
    83: ("MXP", 7950),        # Crystal Glacier
    84: ("MXP", 4850),        # Aquaria Towers
    85: ("MXP", 4700),        # Aquaria Towers: caballitos de mar
    86: ("MXP", 5270),        # Aquaria Towers: el rey de los caballitos de mar
    87: ("MXP", 11520),       # Magma Cone: Lonnie the Faun
    88: ("MXP", 11570),       # Magma Cone
    89: ("MXP", 7450),        # Skelos Badlands
    90: ("MXP", 8530),        # Breeze Harbor
    91: ("MXP", 8899),        # vagoneta: engranajes n/50
    92: ("CYLUX", 2914),      # Fisher: «Trouble with the trolley, eh?»
    93: ("MXP", 8915),        # vagoneta
    94: ("MXP", 8940),        # vagoneta
    95: ("MXP", 6540),        # Glimmer (parte 2)
    96: ("MXP", 6760),        # Sunny Beach (parte 2)
    97: ("MXP", 15975),       # Cloud Temples
    98: ("MXP", 17300),       # Metropolis
    99: ("MXP", 9200),        # Zephyr
    100: ("CYLUX", 3177),     # Romeo y Juliet: luna de miel en Colossus Springs
    101: ("CYLUX", 3185),     # Juliet
    102: ("MXP", 16440),      # Murgen: Mystic City gift shop
    103: ("MXP", 7856),       # Widgie: entradas para el hockey de Colossus Valley
    104: ("X5", 12),          # prototipo (Autumn Plains)
    105: ("MXP", 17850),      # Canyon Speedway
    106: ("MXP", 17960),      # Canyon Speedway
    107: ("MXP", 14010),      # Winter Tundra
    108: ("PQJ", 106),      # menú de pausa con 10 000 gemas (guía)
    109: ("MXP", 16640),      # Robotica Farms
    110: ("X5", 250),         # prototipo (orbes)
    111: ("MXP", 13170),      # Icy Speedway
    112: ("MXP", 18400),      # Ripto's Arena
    113: ("MXP", 2680),       # marcador del hockey
    114: ("MXP", 1182),       # Hunter en Summer Forest
    115: ("U7X", 40),         # prototipo: Elora y Hunter
    116: ("U7X", 160),        # prototipo: Summer Forest
    117: ("U7X", 484),        # prototipo: Hurricos
    118: ("MXP", 5090),        # King Flippy: «The Water Workers have kidnapped six of my children» (versión final)
    119: ("U7X", 640),        # prototipo: caballitos de mar
    120: ("MXP", 3030),       # Hurricos de la versión final
    121: ("JL", 300),         # Breeze Builders y Land Blubbers (diálogo cortado)
    122: ("MXP", 9300),       # Zephyr
    123: ("JL", 310),         # diálogo cortado de Elora
    124: ("MXP", 2058),       # Brother Harry: «A yeti has been rampaging around our home»
    125: ("MXP", 2233.2),     # Spyro llega a Brother Ned
    126: ("MXP", 2240),       # cuadro «torch» y audio «kill»
    127: ("MXP", 2249.6),     # el yeti
    128: ("MXP", 5656),       # cinemática de Crush: llega el Profesor
    129: ("MXP", 5666.3),     # Hunter: «22475»
    130: ("MXP", 5674),       # «that's my birthday… No, Hunter, don't!»
    131: ("MXP", 5681.7),     # Ripto entra por el portal
    132: ("JPN", 40),         # logo japonés
    133: ("MXP", 18121.5),      # Ripto de cerca (único cuerno)
    134: ("MXP", 5931),       # Ripto de cerca en «Bring It On, Shorty!»
    135: ("MXP", 5949),      # Ripto pequeño junto a Gulp
    136: ("MXP", 18134),      # Ripto de cerca: un solo cuerno
    137: ("OT", 92.5),        # doble salto: la técnica
    138: ("OT", 152.5),       # puente de Glimmer
    139: ("OT", 161.3),       # puente de Glimmer
    140: ("OT", 170),         # puente
    141: ("MXP", 2090),       # Colossus
    142: ("MXP", 1750),       # Idol Springs
    143: ("MXP", 2330),       # Colossus
    144: ("MXP", 1830),       # Idol Springs
    145: ("MXP", 2420),       # Colossus
    146: ("MXP", 18810),      # Dragon Shores
    147: ("MXP", 33.5),       # pantalla de inicio y menú
    148: ("JTO", 160),        # demo de CTR: Papu's Pyramid
    149: ("XZ", 120),         # demo de Spyro 2: «On shelves November 1999», Magma Cone y Colossus
    150: ("JTO", 55),         # CTR: título
    151: ("MXP", 19540),      # guía: Skill Points
    152: ("MXP", 19577),      # puntos de habilidad 16/16
    153: ("MXP", 19588),      # puntos de habilidad (molinos, Gulp's Overlook)
    154: ("MXP", 19606),      # epílogos
    155: ("MXP", 19694),      # Faunus Mortas: portada
    156: ("MXP", 19702),      # páginas
    157: ("MXP", 19710),      # páginas
    158: ("MXP", 19722),      # páginas
    159: ("MXP", 15662),      # Mystic Marsh: el Profesor y su lápiz
    160: ("MXP", 15735),      # cambios absurdos: pato de goma y burbujas
    161: ("JL", 45),          # la fuente con la moneda
    162: ("JL", 75.5),        # Dan Johnson real (77 s) y la moneda con su cara
    163: ("JL", 82.6),        # moneda, caja del juego
    164: ("MXP", 15770),      # Mystic Marsh
    165: ("MXP", 15330),      # Mystic Marsh
    166: ("MXP", 15900),      # Mystic Marsh
    167: ("MXP", 18600),      # créditos
    168: ("MXP", 18680),      # créditos
    169: ("MXP", 18860),      # Dragon Shores
    170: ("MXP", 18920),      # Dragon Shores
    171: ("MXP", 18715),      # créditos: música
    172: ("MXP", 8780),       # Breeze Harbor
    173: ("MXP", 19000),      # Dragon Shores
    174: ("MXP", 4376),       # Moneybags
}

# beats donde se OYE el juego porque la voz lo nombra o el sonido ES el punto (volumen del audio del clip); solo fuentes sin narrador
AMBIENTE = {
    8: 0.5,      # Spyro: «you're a dragon, you got a problem with that?»
    15: 0.5,     # lluvia y «Dragon Shores»
    16: 0.5,     # aterrizaje en Avalar
    17: 0.5,     # Ripto, Crush y Gulp
    22: 0.5,     # Kanga: pirámide de supervuelo
    23: 0.5,     # Zoe: «each time you defeat an enemy…»
    44: 0.4,     # Ocean Speedway: motor y burbujas
    45: 0.8,     # Idol Springs: LA CANCIÓN es el punto (s30)
    46: 0.8,     # Fracture Hills: la misma canción (s30)
    54: 0.5,     # Moneybags y el puente
    55: 0.5,     # Moneybags
    56: 0.6,     # Moneybags: pájaros de Zephyr, bombas y TNT
    57: 0.7,     # Ripto: «I persuaded that fat bear Moneybags to sell me a few bombs»
    58: 0.6,     # Moneybags: condominio en Hurricos
    59: 0.6,     # Moneybags: «say hi to Ripto»
    60: 0.5,     # hockey: ambiente de la pista
    61: 0.5,     # Brother Kipp
    62: 0.6,     # partido
    73: 0.5,     # Ripto y Hunter en la misma escena
    74: 0.6,     # Gulp se come el cetro
    75: 0.9,     # «You ate my scepter»
    76: 0.5,     # Ripto sin cetro alimenta a Gulp
    77: 0.7,     # «This is just what I need for a new scepter!»
    91: 0.5,     # vagoneta
    92: 0.9,     # «Trouble with the trolley, eh?»
    93: 0.5,     # vagoneta
    94: 0.6,     # vagoneta
    100: 0.6,    # Romeo: luna de miel en Colossus Springs
    101: 0.5,    # Juliet
    102: 0.6,    # Murgen: Mystic City gift shop
    103: 0.6,    # Widgie: entradas para Colossus Valley
    105: 0.5,    # Canyon Speedway
    124: 0.4,    # Colossus
    126: 0.9,    # Brother Ned: dice «kill» (cuadro «torch»)
    127: 0.5,    # el yeti
    128: 0.5,    # cinemática de Crush
    129: 0.8,    # Hunter: «22475»
    130: 0.8,    # «that's my birthday… No, Hunter, don't!»
    131: 0.5,    # Ripto entra por el portal
}

# grupos de beats que SÍ comparten toma a < 25 s porque son la misma cinemática o la misma escena a propósito
MISMO_TEMA = [
    {7, 12, 35, 147},              # arranque: logos y pantalla de título
    {8, 16, 17, 74, 75},           # cinemática de llegada a Avalar (4 partes distintas, sin repetir cuadros)
    {128, 129, 130, 131},          # cinemática de Crush encadenada
    {133, 136, 78, 79},            # Ripto en «What? You again?»
    {134, 68, 135},                # Ripto y Spyro en «Bring It On, Shorty!»
    {54, 58},                      # Moneybags en Crystal Glacier
    {57, 73, 77},                  # cinemática «You Little Fools!»
    {91, 93, 94},                  # la vagoneta de Breeze Harbor
    {100, 101},                    # Romeo y Juliet
    {125, 126, 127},               # Brother Ned
    {60, 61},                      # hockey
    {14, 67},                      # Glimmer
    {37, 132},                     # logo japonés
    {55, 56},                      # Moneybags en Autumn Plains
    {138, 139, 140},               # doble salto: puente de Glimmer
    {47, 48, 49},                  # Big Head
        {1, 161, 162, 163},            # la moneda de la fuente (tramos distintos)
    {121, 123},                    # diálogo cortado
    {152, 153, 154},               # puntos de habilidad
    {155, 156, 157, 158},          # Faunus Mortas
    {63, 64, 65, 24},              # Elora y Hunter: «I'm a Faun, You Dork!»
]


def sid(n):
    return f"scene-{n:03d}"


def mismo(n1, n2):
    return any(n1 in g and n2 in g for g in MISMO_TEMA)


if __name__ == "__main__":
    beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
    assert len(beats) == len(PLAN) == 174, (len(beats), len(PLAN))
    out, usos = {}, {}
    for b in beats:
        n = int(b["id"].split("-")[1])
        nom, s = PLAN[n]
        dur = b["t1"] - b["t0"] + 0.3
        if nom in DURS and s + dur > DURS[nom]:
            print(f"AVISO {b['id']}: {nom} {s}+{dur:.1f} s se pasa del final ({DURS[nom]} s)")
        for s2, d2, n2 in usos.get(nom, []):
            if abs(s - s2) < 25 and not mismo(n, n2):
                print(f"AVISO {b['id']}: {nom} {s} a {abs(s - s2):.1f} s de scene-{n2:03d}")
        usos.setdefault(nom, []).append((s, dur, n))
        out[b["id"]] = {"url": f"https://youtu.be/{FUENTES_ID[nom]}", "desde": s}
    for n, v in AMBIENTE.items():
        if PLAN[n][0] in ("JL", "OT", "U7X", "ZDU"):
            print(f"AVISO scene-{n:03d}: ambiente en {PLAN[n][0]} (lleva voz de youtuber encima)")
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    recorte_por = {sid(n): RECORTE[nom] for n, (nom, s) in sorted(PLAN.items()) if RECORTE.get(nom)}
    ambiente_por = {sid(n): v for n, v in sorted(AMBIENTE.items())}
    print(f"busquedas.json: {len(out)} beats, {len(usos)} fuentes")
    print("recorte_por = " + repr(recorte_por))
    print("ambiente_por = " + repr(ambiente_por))
    cuenta = {}
    for nom, _ in PLAN.values():
        cuenta[nom] = cuenta.get(nom, 0) + 1
    print("beats por fuente: " + ", ".join(f"{k} {v}" for k, v in sorted(cuenta.items())))
