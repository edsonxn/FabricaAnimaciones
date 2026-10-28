# -*- coding: utf-8 -*-
"""Plan de clips de rare_auge_caida (28-oct-2026): para cada beat (scene-001…126) un video de YouTube y el segundo donde
empieza su clip (el motor corta ~duración del beat + 0,3 s). Segundos elegidos MIRANDO las hojas de previews/_scan/
(y una hoja extra de DK64 0-288 s para el DK Rap). Escribe busquedas.json e imprime recorte_por y ambiente_por para
SECUENCIA en guion.py.
    python plan_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

FUENTES_ID = {
    "JETPAC": "gT2KFXtg4nU", "KNIGHT": "ei6UsWr0XrU", "BTOADS": "aiaXMktO0jQ", "DKC": "d4EUEsEM328",
    "KI": "pC2OXcOx67I", "GE": "rxWkLdgdcPA", "GENSO": "iwoE9sXGd_U", "BK": "0G7V7aJHWk4", "BKNSO": "RWrWuXE6RHw",
    "PD": "vcqbMXllyb0", "CONKER": "TlkMXV1Eagw", "DK64": "agg2K8K2qc0", "DKR": "3gPXyMK4Lls", "JFG": "MIgQ9NFJtzU",
    "SFA": "I-6XzVNLKDY", "GHOUL": "JrKO4Ky-k2o", "KAMEO": "U3mPs0WmTYs", "PDZ": "7lM5kZKnnzM", "VIVA": "7_WtivSGCJA",
    "NB": "QLWLdO9GLWM", "KINECT": "n8wM1aTsl7s", "REPLAY": "AaieVt3M72c", "OPENING": "iYbU1uKPaGU",
    "SOT": "gl3UiHp0sz0", "SOTL": "r5JIBaasuE8", "SOTPS5": "xKLpWOEEUxc", "EVER": "jWpcUH-tKEU",
    "EVER2": "WSWnnQMSPjc", "YOOKA": "oqmF8IgxtJ0", "TS2": "oJwvhPUbRuA", "ATIC": "Z8M4HJTRWqY",
    "SABRE": "lt4FqqLW8LI", "RCPRO": "EA-430ZNqZg", "SNAKE": "r1aFoGEWHFA", "DKC2": "VgTt5fceVTE",
    "DKC3": "HlI65icA8CM", "BLAST": "9icL00n7i2U", "JFGL": "vak_weTcVNo", "VIVAG": "ExxSfoXMUAA",
    "AVATAR": "HCnTvcrQhwU", "BT": "Vjxl_yCvc1o", "SGI": "ZDxLa6P6exc", "SGI2": "Bo3lUw9GUJA",
    "REPLAY2": "F5y_fcMOvZM", "DREAM": "w72kj20YNA0", "PDMK": "7CxpdspOV5I", "NBREV": "_R2sCzlT5Uc",
    "VIVAREV": "Sk4b4L8Da10", "KINECT2": "1xdUV3kbXWw", "KAMEOL": "fAuDjRjIlB8", "SFA2": "GHYIxHYxNOU",
    "DKCDOC": "TwWHzilbQ34",
}

# fracción que se recorta POR LADO (el motor recorta lo mismo en x e y y luego cubre 16:9)
RECORTE = {
    "DKC": 0.18,      # SNES 8:7 con franjas negras anchas a los lados
    "DKC2": 0.18,
    "KI": 0.18,
    "KNIGHT": 0.125,  # Spectrum 4:3 con franjas
    "CONKER": 0.125,  # N64 4:3 con franjas (y marca «Game Master» abajo a la izquierda)
    "BKNSO": 0.125,   # tráiler NSO en 4:3 con franjas
    "DREAM": 0.125,   # metraje del prototipo en 4:3 con franjas
    "JFGL": 0.11,     # franjas negras arriba y abajo
    "DKCDOC": 0.05,   # cuadros dentro del fondo de hojas
    "PDZ": 0.05,      # quita la marca de IGN de la esquina
    "AVATAR": 0.04,   # ídem
}

PLAN = {
    # --- gancho: los mejores planos de cada clásico
    1: ("OPENING", 15),     # luz de telón → pasillo de cuadros → telón rojo del teatro de Rare Replay
    2: ("DKC", 1531),       # DK en la jungla, follaje denso
    3: ("GE", 724),         # Surface: nieve y bosque, pistola en mano
    4: ("BKNSO", 15),       # Banjo tocando el banjo en Spiral Mountain, cascada
    5: ("PD", 4886),        # tiroteo en un pasillo industrial
    6: ("SOT", 75),         # cinemática: esqueleto dorado, abordaje en cubierta, kraken
    # --- capítulo 1: Ultimate (ZX Spectrum)
    7: ("JETPAC", 64),      # el cohete en la plataforma, Jetman
    8: ("DKCDOC", 3120),    # campiña inglesa con pueblo (centro de Inglaterra)
    9: ("ATIC", 123),       # sala azul de Atic Atac con enemigos
    10: ("JETPAC", 309),    # Jetman disparando, cohete magenta
    11: ("JETPAC", 677),    # Jetpac: lluvia de meteoros y láser
    12: ("ATIC", 409),      # Atic Atac: cueva amarilla con monstruos
    13: ("ATIC", 866),      # Atic Atac: sala con mesas y guardias (no hay Sabre Wulf ≥ 720p)
    14: ("JETPAC", 186),    # Jetpac: Jetman entre burbujas de colores
    15: ("ATIC", 980),      # Atic Atac: sala blanca, el caballero
    16: ("KNIGHT", 129),    # Knight Lore: sala isométrica cian con pinchos
    17: ("KNIGHT", 706),    # Knight Lore: sala verde con pinchos y el caballero
    18: ("KNIGHT", 1201),   # Knight Lore: bloques amarillos isométricos
    19: ("KNIGHT", 1779),   # Knight Lore: sala cian con bloques
    # --- capítulo 2: NES
    20: ("RCPRO", 1269),    # R.C. Pro-Am: carrera en curva
    21: ("BTOADS", 680),    # Battletoads: cavernas árticas moradas
    22: ("RCPRO", 462),     # R.C. Pro-Am: coches en pista
    23: ("BTOADS", 1704),   # Battletoads: tuberías por dentro
    24: ("RCPRO", 641),     # R.C. Pro-Am: pista con flechas
    25: ("BTOADS", 1960),   # Battletoads: plataformas rosas
    26: ("RCPRO", 910),     # R.C. Pro-Am: adelantando a dos coches
    27: ("RCPRO", 1538),    # R.C. Pro-Am: meta a cuadros con «PRO-AM» pintado
    28: ("BTOADS", 424),    # Battletoads: Turbo Tunnel, el sapo en la moto
    29: ("BTOADS", 1107),   # Battletoads: la guarida de las serpientes
    30: ("BTOADS", 2472),   # Battletoads: la torre giratoria (The Revolution)
    # --- capítulo 3: la apuesta (Silicon Graphics, DKC)
    31: ("SGI", 236),       # la Indigo2 morada de Silicon Graphics
    32: ("SGI2", 330),      # la Onyx de SGI en una sala
    33: ("SGI", 401),       # tarjetas y memoria de la Indigo2 por dentro
    34: ("DKCDOC", 2550),   # monitor de estación de trabajo con un modelo 3D en malla
    35: ("SGI2", 731),      # placas de la Onyx sobre la mesa
    36: ("KI", 1619),       # Killer Instinct: Combo, el boxeador renderizado
    37: ("DKCDOC", 1867),   # foto de archivo de un directivo de Nintendo
    38: ("DKCDOC", 4032),   # DK en malla 3D verde
    39: ("DKC", 653),       # DKC: jungla al atardecer
    40: ("DKC", 3162),      # DKC: bosque nevado con barril
    41: ("DKCDOC", 2095),   # Miyamoto con un peluche de Mario
    42: ("DKC", 1907),      # DKC: DK en la cuerda de la jungla
    43: ("DKC", 2158),      # DKC: templo con Diddy y enemigos
    44: ("DKC", 3288),      # DKC: nivel submarino (suena Aquatic Ambience)
    45: ("KI", 7795),       # Killer Instinct: Orchid contra Combo en la ciudad
    46: ("DKC2", 2543),     # DKC2: nivel de lava con Dixie
    # --- capítulo 4: GoldenEye
    47: ("GE", 1518),       # Bond en una lancha frente al mar
    48: ("GE", 2489),       # calles de San Petersburgo
    49: ("GE", 1077),       # pasillo con escaleras, escopeta
    50: ("GE", 3018),       # jungla cubana
    51: ("GE", 371),        # instalación con barandillas
    52: ("GE", 1783),       # guardia en la instalación blanca
    53: ("GE", 1341),       # Bond en la puerta del ascensor
    54: ("GE", 4166),       # créditos con los enemigos como actores («Natalya Simonova»)
    55: ("GE", 3813),       # cueva con pasarela metálica
    56: ("GE", 2577),       # patio de trenes de noche
    57: ("GE", 3372),       # pasarelas sobre roca roja
    58: ("GENSO", 37),      # multijugador a pantalla partida en cuatro
    59: ("BLAST", 1649),    # Blast Corps: robot sobre el muelle
    # --- capítulo 5: la fábrica de clásicos
    60: ("DKR", 2859),      # Diddy Kong Racing: aerodeslizador en la nieve
    61: ("BK", 22959),      # Banjo por el camino de Spiral Mountain
    62: ("DREAM", 187),     # prototipo Dream: Edson con la espada en el bosque
    63: ("DREAM", 393),     # prototipo Dream: Banjo en la jungla
    64: ("BT", 54065),      # Banjo-Tooie: Hailfire Peaks, lava
    65: ("JFGL", 10243),    # Jet Force Gemini: pasarela sobre lava
    66: ("DK64", 22368),    # DK64: DK en la hierba ante la puerta de bambú
    67: ("DK64", 38675),    # DK64: cuevas de cristal iluminadas
    68: ("DK64", 57),       # DK64: el DK Rap (intro, «Donkey Kong!»)
    69: ("PD", 8569),       # Joanna Dark en pose de combate
    70: ("PD", 2365),       # Perfect Dark: oficina, dos armas
    71: ("TS2", 5284),      # TimeSplitters 2: el Oeste
    72: ("CONKER", 9761),   # Conker en primer plano
    73: ("CONKER", 1348),   # Windy: Conker por el camino verde
    74: ("CONKER", 18175),  # It's War: la mira sobre un Tedi
    75: ("CONKER", 12706),  # Conker montado en un raptor (parodia de Jurassic Park)
    76: ("CONKER", 15230),  # la mansión del vampiro
    77: ("DK64", 49158),    # DK64: Fungi Forest de noche
    # --- capítulo 6: el divorcio
    78: ("SFA2", 4993),     # Fox con un dinosaurio en la pradera
    79: ("SFA2", 11482),    # el Arwing volando sobre el campo
    80: ("SFA", 2532),      # Fox con un dinosaurio en la jungla
    81: ("SFA2", 25386),    # Fox entre palmeras
    82: ("BK", 10339),      # Banjo en Freezeezy Peak
    83: ("DKC", 2660),      # DKC: bosque de árboles amarillos
    84: ("SFA", 15967),     # Fox por un sendero junto al mar
    85: ("BK", 15147),      # Mad Monster Mansion, cementerio
    86: ("DKC", 1782),      # DKC: avestruz Expresso en la jungla
    87: ("SFA2", 20751),    # Fox en la moto voladora disparando
    88: ("BK", 4329),       # Treasure Trove Cove, arena
    89: ("SFA", 34934),     # Fox y Tricky en la hierba
    90: ("DKC", 6299),      # DK y Diddy en la cubierta del galeón
    91: ("DK64", 20039),    # DK64: DK en la fábrica
    # --- capítulo 7: la caída
    92: ("GHOUL", 1906),    # Ghoulies: Cooper en la cocina de la mansión
    93: ("GHOUL", 7121),    # Ghoulies: sala con enemigos
    94: ("KAMEOL", 4774),   # Kameo: bosque con trolls
    95: ("PDZ", 16),        # PDZ: ojo de Joanna → arma → tiroteo
    96: ("GE", 900),        # GoldenEye: el túnel de la presa (el fenómeno que fue)
    97: ("VIVA", 37),       # Viva Piñata: jardín y piñatas
    98: ("VIVAG", 2155),    # Viva Piñata: el jardín en juego
    99: ("BK", 1925),       # Spiral Mountain, Banjo ante la guarida
    100: ("NBREV", 119),    # Nuts & Bolts: prototipo construyendo un vehículo
    101: ("NBREV", 346),    # Nuts & Bolts: Banjo en Showdown Town
    102: ("AVATAR", 64),    # la fila de avatares de Xbox 360
    103: ("AVATAR", 105),   # creando un avatar
    104: ("KINECT2", 103),  # Kinect Sports: atletismo a pantalla partida → edificio de Rare
    105: ("GHOUL", 13206),  # Ghoulies: cuarto de la lavadora
    106: ("YOOKA", 6),      # Yooka-Laylee: estatua dorada, bosque
    107: ("YOOKA", 88),     # Yooka-Laylee: islas flotantes
    108: ("YOOKA", 47),     # Yooka-Laylee: la burbuja
    # --- capítulo 8: un barco pirata
    109: ("SOT", 21),       # cinemática: tormenta en el barco
    110: ("OPENING", 79),   # teatro de Rare Replay: escalera, público de personajes («Over 30 years…»)
    111: ("REPLAY2", 35),   # sala de estandartes de Rare Replay
    112: ("SOTL", 13),      # Sea of Thieves: cubierta vista desde arriba, la tripulación, el timón
    113: ("SOTPS5", 100),   # Sea of Thieves: cañonazo, montaña de tesoros
    114: ("SOTPS5", 7),     # Sea of Thieves (PS5): el kraken ataca la cubierta
    115: ("EVER", 17),      # Everwild: zorros en la pradera al atardecer
    116: ("EVER2", 89),     # Everwild: bosque nocturno, colinas bajo las estrellas
    117: ("DKC", 4417),     # DKC: letras KONG en la mina
    118: ("BK", 21757),     # Banjo en el puente de Spiral Mountain
    119: ("SOTPS5", 58),    # Sea of Thieves: barco al atardecer, capitán esqueleto
    120: ("PD", 5855),      # Perfect Dark: hombre de traje en un despacho
    121: ("PD", 3723),      # Perfect Dark: pasarela en la ciudad de noche
    122: ("BK", 13344),     # Gobi's Valley, el desierto
    123: ("DKC", 5170),     # DKC: la montaña de plátanos de DK
    124: ("SOTL", 57),      # Sea of Thieves: el barco navegando al atardecer
    125: ("DKR", 5586),     # Diddy Kong Racing: Treasure Island con el barco pirata
    126: ("BT", 65103),     # Banjo-Tooie: Cloud Cuckooland
}

# beats donde se OYE el juego porque la voz lo nombra (volumen del audio del clip)
AMBIENTE = {
    11: 0.5,    # Jetpac: los pitidos de la Spectrum
    28: 0.6,    # Battletoads: el Turbo Tunnel
    44: 0.7,    # DKC: Aquatic Ambience
    58: 0.6,    # GoldenEye: el multijugador
    60: 0.5,    # Diddy Kong Racing
    68: 0.8,    # DK64: el DK Rap
    110: 0.6,   # Rare Replay: la canción del teatro
    112: 0.4,   # Sea of Thieves: el barco
}


def sid(n):
    return f"scene-{n:03d}"


if __name__ == "__main__":
    beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
    durs = {}
    p = os.path.join(AQUI, "previews", "_scan", "_alturas.txt")
    for lin in open(p, encoding="utf-8"):
        c = lin.rstrip("\n").split("\t")
        if len(c) >= 4:
            durs[c[0]] = float(c[3].split()[0])
    assert len(beats) == len(PLAN) == 126, (len(beats), len(PLAN))
    out, usos = {}, {}
    for b in beats:
        n = int(b["id"].split("-")[1])
        nom, s = PLAN[n]
        fin = s + (b["t1"] - b["t0"]) + 0.3
        if nom in durs and fin > durs[nom]:
            print(f"AVISO {b['id']}: {nom} {s}+{b['t1'] - b['t0']:.1f} s se pasa del final ({durs[nom]:.0f} s)")
        for s2, n2 in usos.get(nom, []):
            if abs(s - s2) < 40:
                print(f"AVISO {b['id']}: {nom} {s} a {abs(s - s2)} s de scene-{n2:03d}")
        usos.setdefault(nom, []).append((s, n))
        out[b["id"]] = {"url": f"https://youtu.be/{FUENTES_ID[nom]}", "desde": s}
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    recorte_por = {sid(n): RECORTE[nom] for n, (nom, s) in sorted(PLAN.items()) if RECORTE.get(nom)}
    ambiente_por = {sid(n): v for n, v in sorted(AMBIENTE.items())}
    print(f"busquedas.json: {len(out)} beats, {len(usos)} fuentes")
    print("recorte_por = " + repr(recorte_por))
    print("ambiente_por = " + repr(ambiente_por))
