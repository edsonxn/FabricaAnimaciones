# -*- coding: utf-8 -*-
"""Plan de clips de bt_mundos_ranking (30-oct-2026; estructura de mario64_secretos/plan_clips.py): para cada beat (scene-001…170) un video de YouTube y el
segundo donde empieza su clip (el motor corta ~duración del beat + 0,3 s). Segundos elegidos MIRANDO hojas de contacto (360p, 1 cuadro cada 2-20 s) sobre
las tomas del catálogo de verificacion_clips.md. Fuente principal: serie Ninbanyan «Banjo-Tooie NSO 100 %» (PNN = parte NN, widescreen 1080p60 sin narrador:
RECORTE vacío y el audio del clip sirve para ambiente_por). Aparte: XBLA = DPadGamer «Jinjo Punch» (720p, versión Xbox 360 con voz encima: SIN ambiente) para lo
que en N64 no se ve (refrigerador BK, «Defective Goods», George y Mildred, Superstash 1-9-8-4, constelación de Mr. Pants, cartón de Tooty). Escribe
busquedas.json e imprime recorte_por y ambiente_por para SECUENCIA en guion.py.
    python plan_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

FUENTES_ID = {
    "P02": "mCeQj7py8g4", "P03": "5PjYuSAZBJQ", "P04": "XyEok8nI5tA", "P05": "YNyPK0cCfsM", "P08": "tgC5omjQgG8",
    "P09": "XA5Q0rWYKaY", "P10": "kM9ruHky3ng", "P11": "FTD7c-BfDI4", "P14": "88Y_3NvPw0Q", "P15": "nSW5HYUc0v4",
    "P17": "VxRt5CIZ43Q", "P18": "3OiDVU9YnyI", "P19": "0oEvo3BB6Ls", "P20": "cgQjeEjlscc", "P22": "apQeJq_a1c8",
    "P23": "pnXRfbIyMw0", "P24": "jtcsZvsw16I", "P26": "K1dZ0qRmU1I", "P27": "-5xyL3uwvUM", "P29": "a03FCil1wEI",
    "P31": "I_bWv3nUK5c", "P32": "UmgVCgOUVeE", "P33": "t-DIdt_HztE", "P34": "bNezbjXd27c", "P35": "3erroCDTxsE",
    "P36": "WAhi2hejiQk", "P37": "AQ7Ewsl2k4I", "P39": "MKpzMtyZOK0", "P40": "YbdR6D3TueM", "P41": "CDyIfCHE5lg",
    "P42": "7Gzu82cUN4I", "XBLA": "bcpt_BIyYsk",
}

# fracción que se recorta POR LADO: la serie Ninbanyan es widescreen de NSO, sin recorte
RECORTE = {}

PLAN = {
    1: ("P27", 1030),        # Workers' Quarters: la puerta del baño (icono de persona) al fondo del pasillo
    2: ("XBLA", 300.2),      # XBLA: cartón «MISSING TOOTY» en primer plano (versión Xbox)
    3: ("P26", 1140),        # Blackeye bebiendo en Jolly's: «I'll slit yer…», «fetch me another glass»
    4: ("P02", 240),         # Isle o' Hags, pueblo de los Jinjos, Banjo corriendo
    5: ("P03", 420),         # Jiggywiggy: el Jiggy con ojos «to prove yourself worthy»
    6: ("P02", 270),         # camino de la isla bajo la selva
    7: ("P02", 330),         # Green Jinjo Family House (título)
    8: ("P02", 600),         # rey Jingaling con corona y diálogo
    9: ("P02", 60),          # Klungo con bata
    10: ("P03", 1080),       # Jamjars frente a Banjo y Kazooie (diálogo)
    11: ("P02", 1290),       # Bottles en su casa: «Hello there, Ban…»
    12: ("P03", 1105),       # Jamjars, continuación de la charla (toma no vista a fondo)
    13: ("P34", 510),        # Chuffy en la estación del tren («Train Station»)
    14: ("P27", 164),  # Grunty Industries: camino de grava y el letrero hasta el túnel
    15: ("P27", 212),        # muro de ladrillo con Banjo trepando
    16: ("P27", 186),        # cartel «MAIN ENTRANCE»: la puerta cerrada
    17: ("P27", 476),  # Banjo junto al tren de la estación (sin el corte a negro del final)
    18: ("P27", 527),        # tuberías y rejillas grises de la fábrica
    19: ("P27", 335),        # la pila gigante (batería) verde: «demasiadas baterías»
    20: ("P27", 569),        # pasillo gris largo de la fábrica
    21: ("P27", 996),        # puerta del elevador al 1.er piso y cartel «WORKERS' QUARTERS»
    22: ("P27", 1010),       # título «Floor 1 – Workers' Quarters» y puerta del baño a la izquierda
    23: ("P27", 1020),       # Banjo junto a la puerta del baño y la tele del cuarto
    24: ("P27", 1038),       # Banjo ante la puerta del baño (con humo) y cuartos de literas
    25: ("P27", 1102),       # Banjo ve el refrigerador al fondo del cuarto
    26: ("P27", 1119),       # refrigerador de cerca: B-T, DK y el logo R de Rare
    27: ("XBLA", 239),       # XBLA: el mismo refrigerador con «BK»
    28: ("P29", 1049),       # cajas «FRAGILE» y la de «…TWYCROSS ENGLAND»
    29: ("XBLA", 252),       # XBLA: caja «DEFECTIVE GOODS» legible
    30: ("P29", 415),        # Kazooie dragón y la caja «BIG-O PANTS!»
    31: ("P27", 1168),       # Loggo, el excusado parlante, con diálogo
    32: ("P31", 1495),  # Wumba's Wigwam: Humba Wumba transforma a Banjo (sin la carga previa)
    33: ("P31", 1514),  # Banjo-lavadora en el Piso 2 (sin la carga previa)
    34: ("P32", 895),        # Weldar con su cable y diálogo: el soplete con ojos
    35: ("P32", 1025),       # Weldar encima del poste, «Where's my emergency switch»
    36: ("P32", 1100),       # pelea con Weldar: Kazooie dispara fuego
    37: ("P17", 417),        # título «Jolly Roger's Lagoon» sobre la cueva
    38: ("P18", 56),         # fondo del mar con ruinas y peces
    39: ("P18", 1200),       # interior verde de templo submarino
    40: ("P18", 6),          # pez globo enemigo bajo el agua
    41: ("P26", 1086),       # cartel «JOLLY'S» y entrada al bar
    42: ("P26", 1096),       # Blackeye: «A bear stole me glory» / «looked a bit like you»
    43: ("P26", 1122),       # Blackeye bebiendo: «splice the main brace»
    44: ("P26", 1105),       # primer plano del pirata, vaso y sonrisa
    45: ("P20", 232),        # el OVNI sobre el pueblo
    46: ("P20", 68),         # interior del OVNI: «Elvis» y «phone home»
    47: ("P18", 275),        # casilleros del fondo: «D. JONES»
    48: ("P18", 253),        # casillero «G. KIRKHOPE»
    49: ("P17", 755),        # «Pawno's Emporium» y la caja B-K
    50: ("P17", 207),        # la cerdita rosa con pelota de playa (Merry Maggie)
    51: ("P17", 178),        # camino empedrado del pueblo de Jolly Roger's
    52: ("P18", 326),        # el pez ancla Lord Woo Fak Fak llega
    53: ("P18", 340),        # Lord Woo Fak Fak: «he sleeps in his…» y el pez abre la boca
    54: ("P17", 1120),       # hechizo de Mumbo: rótulo «SUNLIGHT / OXYGENATED WATER»
    55: ("P42", 1712),       # la rocola de Jolly's
    56: ("P19", 620),        # pez traslúcido brillante bajo el agua (toma no verificada a fondo)
    57: ("P17", 790),        # mostrador de Pawno's
    58: ("P23", 1110),       # título «Terrydactyland» sobre el valle
    59: ("P22", 1169),       # título «Terrydactyland» sobre la hierba
    60: ("P23", 963),        # cuevas rojas iguales, vacías
    61: ("P24", 309),        # Wumba en su wigwam
    62: ("P24", 384),        # Daddy T-Rex en la cueva
    63: ("P23", 489),        # cinemática de Chompa: cuello, boca y tragar
    64: ("P33", 611.5),  # título «Stomping Plains» (pasada la carga)
    65: ("P33", 537),        # el pie gigante del Stomponadon en la llanura
    66: ("P24", 990),        # nido de Terry con huevos y Terry batiendo alas
    67: ("P23", 1326),       # cueva de Unga Bunga: tienda y camino
    68: ("P10", 1318),       # templo de Mayahem (domo/altar), Cámara del Tesoro
    69: ("P33", 236),        # cavernícola comiendo, feliz
    70: ("P24", 30),         # Dippy el cocodrilo en su cueva
    71: ("P24", 120),        # Banjo recorriendo la cueva
    72: ("P10", 1445),       # sendero de selva de Mayahem Temple (sin el menú de destino que sigue al título)
    73: ("P10", 1290),       # arco del templo con escalera
    74: ("P10", 330),        # torre de piedra tallada con antorcha
    75: ("P10", 480),        # Stony caminando junto a la pasarela de cuerdas
    76: ("P03", 1316),       # Mumbo's Skull: Mumbo ante el altar
    77: ("P10", 930),        # estatua roja del ídolo en el pasto
    78: ("P04", 466),        # primera persona: escalera de piedra con Kazooie
    79: ("P04", 405),        # Targitzan: «ten statues gains you entry…»
    80: ("P04", 496),        # primera persona: pasillo del templo y selva
    81: ("P05", 80),         # Cámara de Códigos: la pared de letras
    82: ("P10", 1458),       # la pared de letras al llegar el jugador
    83: ("P10", 1476),       # letras encendidas en rojo
    84: ("P10", 1486),       # más letras encendidas
    85: ("P15", 1553),       # primera fila E S R A, limpia
    86: ("P05", 92),         # la pared de letras y la fila E S R A
    87: ("P04", 422.5),      # «Targitzan's Slightly Sacred Chamber» (rótulo)
    88: ("P04", 659),        # «Targitzan's Really Sacred Chamber»
    89: ("P10", 750),        # sendero entre acantilado y arroyo
    90: ("P10", 840),        # pendiente de pasto sobre cueva
    91: ("P08", 640),        # título «Gloomy Caverns» de la mina
    92: ("P09", 525),        # Toxic Gas Cave
    93: ("P08", 90),         # Banjo en el carrito entre vías
    94: ("P08", 419),        # caja del detonador con gema verde
    95: ("P08", 300),        # canal de agua con vías
    96: ("P08", 150),        # título «Gloomy Caverns» con farol
    97: ("P08", 20),         # Canary Mary hablando con Banjo
    98: ("P08", 30),         # Canary Mary se va volando
    99: ("P09", 1410),       # título «Old King Coal»
    100: ("P08", 775),       # cabaña de la mina y vagoneta
    101: ("P10", 150),       # Prison Compound: patio de Mayahem
    102: ("P09", 443),       # Crushing Shed: la roca con veta amarilla y las ruedas
    103: ("P09", 497),       # sale el Jiggy entero, destellos amarillos
    104: ("P09", 1436),  # Old King Coal en su sala: la cara del jefe y el diálogo
    105: ("P08", 1166.5),  # Banjo-Kazooie bajo el agua (Talon Torpedo)
    106: ("P35", 1080),      # cueva de hielo de Hailfire con el huevo verde
    107: ("P39", 30),        # isla de pasto con Kazooie y nubes
    108: ("P39", 60),        # isla flotante con roca rosa
    109: ("P41", 480),       # arcoíris sobre isla azul
    110: ("P39", 716),       # George Ice Cube: «came along and blew me…»
    111: ("P39", 745),       # el cubo de hielo con la cara
    112: ("P41", 240),       # el bote de basura flotante
    113: ("P40", 626),       # cartón «MISSING TOOTY» y la botella
    114: ("P40", 590),       # dentro del bote de basura
    115: ("P41", 60),        # planta con flor sobre isla
    116: ("P39", 360),       # Canary Mary con alas
    117: ("P41", 750),       # isla morada con planta alta
    118: ("XBLA", 292),      # XBLA: Superstash cerrado y sus ruedas 1-9-8-4
    119: ("P39", 1350),      # Superstash con Banjo y Kazooie: «that might be a problem»
    120: ("P39", 1056),      # Superstash, la caja fuerte con ojos
    121: ("P41", 1020),      # plataforma naranja con tallo verde
    122: ("P40", 60),        # sala del jefe: Mingy Jongo en su trono
    123: ("P41", 1080),      # Mr. Fit: «Cloud Cuckooland… ready? 3.» la carrera
    124: ("P14", 1336),      # título «Witchyworld»
    125: ("P15", 150),       # Dodgem con coches y chispas azules
    126: ("P15", 390),       # carpa de circo a rayas con escalera
    127: ("P15", 440),       # Saucer of Peril: Banjo en el platillo
    128: ("P15", 720),       # camino con carpas azules y cielo naranja
    129: ("P14", 1414),  # Dodgem Dome Lobby con la ventana de nebulosa (Van de Banjo)
    130: ("XBLA", 309),  # XBLA: la tele de Mr. Pants y su constelación en el cielo
    131: ("P15", 120),       # pista Dodgem con puntuación
    132: ("P14", 1430),      # ventana estrellada del Dodgem Dome
    133: ("P11", 470),       # letrero del parque cerrado por seguridad
    134: ("P11", 672),       # letrero de Big Al: carne de roedor
    135: ("P11", 778),       # letrero de las papas de Salty Joe
    136: ("P15", 750),       # caseta de madera del parque
    137: ("P15", 570),       # platillo disparando a blancos verdes
    138: ("P15", 630),       # platillo cerca de la tienda de papas
    139: ("P15", 240),       # Dodgem con luces rosas
    140: ("P15", 330),       # estructura de madera junto a la carpa
    141: ("P14", 1371),      # Humba Wumba transforma a Banjo
    142: ("P14", 1397),      # la Van con humo
    143: ("P34", 660),       # título «Hailfire Peaks (Lava Side)»
    144: ("P37", 270),       # título «Hailfire Peaks (Icy Side)»
    145: ("P34", 1050),      # Gobi el camello
    146: ("P34", 240),       # lava, Banjo cruza la plataforma
    147: ("P34", 540),       # Chuffy en la estación sobre la lava
    148: ("P37", 487),       # Sabreman congelado en el hielo
    149: ("P37", 503),       # Sabreman descongelado y su diálogo
    150: ("P36", 451),       # el iglú de Boggy: la tele con Mister Pants
    151: ("P36", 479),       # Boggy habla desde el sofá
    152: ("P36", 535),       # Boggy y el DVD
    153: ("P36", 549),       # la tele encendida con el muñeco
    154: ("P36", 556),       # Mister Pants en la tele y la esposa
    155: ("P36", 612),       # cuarto de los niños: cama y cuadro con igloo
    156: ("P36", 381),       # Mildred Ice Cube: «Hey young man! I'm Mildred»
    157: ("XBLA", 280.5),    # XBLA: George, Mildred y el póster «Man About the House»
    158: ("P34", 690),       # Kazooie volando sobre lava
    159: ("P35", 1140),      # cueva de hielo con Banjo
    160: ("P36", 1084),      # interior de piedra: el wigwam de Mumbo
    161: ("P36", 646.5),  # zona alienígena y camino del lado de hielo (título Icy Side)
    162: ("P35", 1200),      # bloque de hielo
    163: ("P34", 30),        # plataforma de piedra sobre lava
    164: ("P37", 154),  # nieve y hielo con la bola de nieve (sin el menú de destino)
    165: ("P10", 1157),  # Isle o' Hags (Wooded Hollow): colinas y río de la isla
    166: ("P15", 1350),      # Isle o' Hags (Jinjo Village)
    167: ("P42", 1650),       # Isle o' Hags (Jinjo Village): el pueblo de los Jinjos
    168: ("P27", 1232),      # Banjo y Kazooie en el cuarto de los obreros
    169: ("P03", 520),       # Jiggywiggy: puzles
    170: ("P34", 570),       # Chuffy de cerca
}

# beats donde se OYE el juego porque la voz lo nombra (volumen del audio del clip; solo clips de la serie, sin narrador)
AMBIENTE = {
    31: 0.5,     # Loggo habla
    34: 0.5,     # Weldar y su cable
    42: 0.8,     # Blackeye: «a bear stole me glory»
    44: 0.5,     # Blackeye bebe
    46: 0.8,     # alienígenas: Elvis y phone home
    54: 0.8,     # Mumbo lanza Sunlight
    55: 0.8,     # la rocola de Jolly's
    62: 0.5,     # pasos de Daddy T-Rex
    63: 0.8,     # cinemática de Chompa
    65: 0.8,     # el pisotón del Stomponadon
    79: 0.8,     # Targitzan
    81: 0.5,     # Cámara de Códigos
    89: 0.5,     # música de Mayahem
    90: 0.5,     # música de Mayahem
    97: 0.8,     # Canary Mary
    98: 0.5,     # Canary Mary se va
    102: 0.8,    # el grito de la trituradora
    103: 0.9,    # jingle del Jiggy
    104: 0.8,    # Old King Coal
    110: 0.8,    # George Ice Cube
    122: 0.8,    # Mingy Jongo
    123: 0.8,    # Mr. Fit y la cuenta de la carrera
    137: 0.5,    # música de Witchyworld
    138: 0.5,    # música de Witchyworld
    141: 0.8,    # transformación de Wumba y claxon
    142: 0.8,    # claxon de la Van
    143: 0.8,    # música del lado de lava
    144: 0.8,    # música del lado de hielo
    148: 0.5,    # Sabreman congelado
    149: 0.8,    # Sabreman habla
    151: 0.8,    # Boggy habla
    152: 0.8,    # Boggy y el DVD
    156: 0.8,    # Mildred Ice Cube habla
    158: 0.8,    # melodía de los dos lados
    159: 0.8,    # música de hielo
    160: 0.8,    # Mumbo y Life Force
}

# parejas de beats que SÍ comparten toma a < 25 s porque son el mismo Easter egg o la misma escena a propósito
MISMO_HUEVO = [
    {1, 21, 22, 23, 24, 25, 26},    # Workers' Quarters: puerta del baño y refrigerador
    {3, 41, 42, 43, 44},            # Blackeye en Jolly's
    {47, 48},                       # casilleros del fondo del mar
    {52, 53},                       # Lord Woo Fak Fak
    {81, 82, 83, 84, 86},           # Cámara de Códigos
    {79, 87},                       # zona de Targitzan
    {97, 98},                       # Canary Mary
    {150, 151, 152, 153, 154, 155},  # el iglú de Boggy
    {148, 149},                     # Sabreman
    {14, 16},                       # entrada de Grunty Industries
    {32, 33},                       # Wumba y la lavadora (P31, 19 s)
    {72, 82},                       # Mayahem: selva y llegada a la Cámara de Códigos
    {129, 132, 142},                 # Dodgem Dome y la Van (P14)
    {2, 27, 29, 118, 130, 157},     # XBLA: un solo video de curiosidades
]


def sid(n):
    return f"scene-{n:03d}"


def mismo(n1, n2):
    return any(n1 in g and n2 in g for g in MISMO_HUEVO)


if __name__ == "__main__":
    beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
    assert len(beats) == len(PLAN) == 170, (len(beats), len(PLAN))
    out, usos = {}, {}
    for b in beats:
        n = int(b["id"].split("-")[1])
        nom, s = PLAN[n]
        for s2, n2 in usos.get(nom, []):
            if abs(s - s2) < 25 and not mismo(n, n2):
                print(f"AVISO {b['id']}: {nom} {s} a {abs(s - s2)} s de scene-{n2:03d}")
        usos.setdefault(nom, []).append((s, n))
        out[b["id"]] = {"url": f"https://youtu.be/{FUENTES_ID[nom]}", "desde": s}
    for n, v in AMBIENTE.items():
        if PLAN[n][0] == "XBLA":
            print(f"AVISO scene-{n:03d}: ambiente en XBLA (lleva voz encima)")
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
    print("XBLA: " + ", ".join(str(n) for n, (nom, _) in sorted(PLAN.items()) if nom == "XBLA"))
