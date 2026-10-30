# -*- coding: utf-8 -*-
"""Plan de clips de mario64_secretos (29-oct-2026; copia de rare_auge_caida/plan_clips.py): para cada beat (scene-001…126) un video de YouTube y el segundo donde
empieza su clip (el motor corta ~duración del beat + 0,3 s). Segundos elegidos MIRANDO las hojas de previews/_scan/
. Escribe busquedas.json e imprime recorte_por y ambiente_por para
SECUENCIA en guion.py.
    python plan_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

FUENTES_ID = {
    "SM64": "CRzjAKE2Zns", "SM3D": "m9PcTN_vSVo", "SHOSHIN": "nChnAtz6RGU", "SW95": "GjgaRzI853o", "HALFA": "X-zAWbM50JM",
    "UPWARP": "X5cwuYFUUAY", "UPW2": "vj8DzA9y8ls", "BLJ": "fDz5WfNIbJI", "BLJH": "gKf_bFNXuu8", "YOSHI": "KVnhgyZN-wE",
    "LUIGI": "cjJrbygzen0", "N64ADS": "in4X7qOUxEg", "DSVC": "xqQU2RZnRjc", "AS3D": "CPJcaGWoO2c", "TAS": "9JhYbnx_h0w",
    "WR120": "Y1a_q2AZ9pk",
}

# fracción que se recorta POR LADO (el motor recorta lo mismo en x e y y luego cubre 16:9)
RECORTE = {
    "SM64": 0.131,    # NSO: 4:3 dentro del marco gris de Switch Online (medida de zelda_oot / majora_mask)
    "SM3D": 0.125,    # 3D All-Stars: 4:3 con barras negras laterales (medido en SM3D_1.jpg)
}

PLAN = {
    1: ("SM64", 3756),        # patio: fuente y estatua con la placa
    2: ("LUIGI", 28),         # pantalla dividida Mario y Luigi
    3: ("LUIGI", 17.5),       # código del mod de Luigi (programador)
    4: ("SM3D", 2),           # 3D All-Stars: menú «1996 Super Mario 64»
    5: ("N64ADS", 62),        # anuncio 1996: logo N64 + Mario 64
    6: ("SM64", 1927),        # vuelo con la gorra alada
    7: ("SM64", 12172),       # Tiny-Huge Island
    8: ("UPW2", 1091),        # gráfico del sol / rayo cósmico
    9: ("SM64", 185),         # Bob-omb Battlefield
    10: ("SM64", 1537),        # Whomp's Fortress
    11: ("SM64", 1477),        # Whomp's Fortress: plataformas
    12: ("SHOSHIN", 33),       # beta 1995: interior sencillo
    13: ("LUIGI", 54),         # pantalla dividida Mario y Luigi
    14: ("SM64", 11541),       # Tall, Tall Mountain
    15: ("SM3D", 4049),        # Big Boo's Haunt de noche
    16: ("SM3D", 8799),        # DDD nadando
    17: ("SM64", 7035),        # Shifting Sand Land
    18: ("SM64", 6614),        # Lethal Lava Land
    19: ("SM64", 10910),       # Snowman's Land
    20: ("SM64", 9018),        # DDD con monedas
    21: ("SM64", 6855),        # volcán de LLL
    22: ("SM64", 11181),       # Snowman's Land iglú
    23: ("SM64", 11632),       # Tall, Tall Mountain ladera
    24: ("SM64", 7215),        # SSL por el aire
    25: ("SM64", 756),         # BoB pradera
    26: ("SM64", 1206),        # cartel de los Lakitu
    27: ("SM3D", 110),         # Lakitu con la cámara
    28: ("SM3D", 69.5),        # castillo y foso
    29: ("SM64", 485),         # Koopa the Quick: bandera de meta
    30: ("SM64", 12923),       # agarra una estrella
    31: ("SHOSHIN", 79),       # beta: jardines
    32: ("SHOSHIN", 172),      # beta: cuadro de nieve
    33: ("SHOSHIN", 125),      # beta: medidor y cielo liso
    34: ("SHOSHIN", 372),      # beta: patina en la lava
    35: ("SHOSHIN", 511),      # beta: Bowser
    36: ("SM64", 14035),       # Rainbow Ride
    37: ("SM64", 7425),        # SSL ruinas
    38: ("N64ADS", 114),       # Players' Choice Million Seller
    39: ("SM64", 11481),       # TTM estrella
    40: ("DSVC", 13),          # Mario 64 DS
    41: ("AS3D", 16),          # Switch y Mario 64 en el tráiler
    42: ("SM3D", 6328),        # LLL en All-Stars
    43: ("SM64", 14400),       # Rainbow Ride
    44: ("SM64", 9649),        # pasillo a la puerta de estrella
    45: ("SM3D", 4521),        # sótano en All-Stars
    46: ("SM64", 6068),        # MIPS huye
    47: ("SM64", 4497),        # persecución de MIPS
    48: ("SM3D", 4561),        # atrapa a MIPS
    49: ("SM64", 70),          # Lakitu frente al castillo
    50: ("SM64", 125),         # Lakitu: filming live
    51: ("SM64", 10631),       # sala del espejo: Lakitu reflejado
    52: ("SM64", 3062),        # entrada a Jolly Roger Bay
    53: ("SM3D", 2694),        # Mario nada hacia la cueva, asoma la anguila
    54: ("SM64", 2966),        # la anguila sale; estrella en la cola
    55: ("SM3D", 2786),        # bajo el agua de JRB con la anguila
    56: ("SM3D", 707),         # Cool Cool Mountain: cima nevada
    57: ("SM64", 2089),        # mamá pingüino en su estanque
    58: ("SM3D", 790),         # Mario junto a la mamá pingüino
    59: ("SM3D", 748),         # bajando la montaña con el bebé
    60: ("SM64", 3189),        # JRB bajo el agua
    61: ("SM64", 2796),        # Acuario Secreto
    62: ("SM64", 2755),        # pasillo del cuadro de JRB: hueco de la pared
    63: ("SM64", 4557),        # sótano: golpe sobre el pilar
    64: ("SM64", 4599),        # nivel del gorro de invisibilidad
    65: ("SM64", 8808),        # Dire Dire Docks nadando
    66: ("SM64", 8930),        # DDD: baja nadando entre monedas
    67: ("SM64", 3104),        # JRB bajo el agua
    68: ("SM64", 9108),        # DDD: el submarino de Bowser
    69: ("SM64", 3514),        # puerta de 8 estrellas → retrato de Peach
    70: ("SM3D", 3460),        # Peach se vuelve Bowser y cae
    71: ("SM3D", 3561),        # Bowser in the Dark World
    72: ("SM3D", 3648),        # Bowser de cerca
    73: ("YOSHI", 19),         # jardín con 120 estrellas, al cañón
    74: ("SM64", 16023),       # cañón al tejado
    75: ("YOSHI", 69),         # mensaje de Yoshi
    76: ("SM64", 16084),       # Yoshi y Mario en el tejado
    77: ("SM64", 3683),        # lanza a Bowser
    78: ("SM64", 8691),        # BitFS: lo gira
    79: ("SM64", 8731),        # lanzamiento y explosión
    80: ("SM3D", 8545),        # Switch: lanzamiento (otro grito)
    81: ("SM3D", 8491),        # BitFS en Switch
    82: ("SM64", 1264),        # Whomp's Fortress: rey Whomp
    83: ("SM64", 6400),        # Lethal Lava Land
    84: ("SM64", 10822),       # Snowman's Land
    85: ("SM64", 1688),        # Hoot el búho
    86: ("N64ADS", 72),        # anuncio de TV de Mario 64
    87: ("SHOSHIN", 18),       # demo de 1995
    88: ("SM3D", 29),          # cabeza de Mario (Switch)
    89: ("AS3D", 26),          # tráiler: nieve y Rainbow Ride
    90: ("SM64", 13223),       # 3.er piso hacia el reloj
    91: ("SM64", 13272),       # reloj de péndulo
    92: ("SM64", 13415),       # Tick Tock Clock engranajes
    93: ("SM64", 13684),       # TTC detenido
    94: ("SM64", 9676),        # pasillo al cuadro de WDW
    95: ("SM64", 9784),        # WDW agua alta
    96: ("SM64", 9740),        # WDW agua baja
    97: ("SM64", 10100),       # WDW
    98: ("SM64", 15235),       # 3.er piso: Peach y escaleras hacia la escalera final
    99: ("SM3D", 15788),       # escalera roja de Switch
    100: ("SM3D", 15800),       # escalera roja subiendo
    101: ("SM64", 15247),       # escalera sin fin, alfombra roja
    102: ("BLJH", 178),         # escalera sin fin real en consola (sube y no llega)
    103: ("SM64", 29.5),        # cabeza de Mario, «It's-a me», se estira
    104: ("SM3D", 16401),       # créditos: MARIO FACE PROGRAMMER Giles Goddard
    105: ("SHOSHIN", 233),      # beta 1995: valla y nubes
    106: ("SHOSHIN", 295),      # beta 1995: lava
    107: ("SM64", 15994),       # cabeza de Mario estirada al final
    108: ("AS3D", 5),           # tráiler: cabeza en la pantalla de título y la Switch
    109: ("SM3D", 2038),        # Whomp's Fortress
    110: ("SM3D", 1193),        # Cool Cool Mountain
    111: ("SM3D", 7109),        # Shifting Sand Land, pirámide
    112: ("DSVC", 33),          # Mario 64 DS: isla de Yoshi y hielo
    113: ("BLJH", 592),         # carrera de 0 estrellas
    114: ("BLJ", 270),          # BLJ en la escalera, SPD subiendo
    115: ("BLJH", 166),         # Mario sale disparado por la escalera
    116: ("SM3D", 3727),        # 3D All-Stars: alfombra roja del castillo
    117: ("BLJ", 3),            # tele CRT con el cartucho original
    118: ("BLJ", 519),          # speedrun con splits, cero estrellas
    119: ("WR120", 5747),       # final del récord 1:35:14
    120: ("WR120", 4173),       # récord de 120 a mitad
    121: ("HALFA", 7),          # Hazy Maze Cave con el contador de A
    122: ("HALFA", 47),         # empujando al bicho
    123: ("HALFA", 90),         # Standard/Scuttlebug View
    124: ("HALFA", 202),        # mapa de universos paralelos
    125: ("HALFA", 246),        # PU map
    126: ("HALFA", 291),        # la estrella con 0,5 A
    127: ("SM64", 13560),       # Tick Tock Clock
    128: ("UPWARP", 5),         # DOTA_TeaBag en TTC vs recreación
    129: ("UPWARP", 45),        # el upwarp
    130: ("UPW2", 125),         # diagrama del techo, recompensa de 1000 $
    131: ("UPW2", 647.5),       # panel de bits
    132: ("UPW2", 406),         # el rayo
    133: ("UPW2", 449),         # tele CRT de DOTA_Teabag
    134: ("SM64", 6146),        # patio con el Boo
    135: ("N64ADS", 126),       # anuncio de la época: Mario en el castillo
    136: ("SHOSHIN", 141),      # beta 1995: torre
    137: ("LUIGI", 66),         # pantalla dividida Mario / Luigi
    138: ("SHOSHIN", 187),      # beta: pasillo oscuro
    139: ("SM64", 2618),        # castillo: vitral de Peach
    140: ("LUIGI", 6),          # filtración 2020 y modelo de Luigi
    141: ("SM64", 3772),        # patio: estatua y Boo
    142: ("DSVC", 59),          # Nintendo DS con Luigi arriba
    143: ("SM64", 3764),        # Mario frente a la placa
    144: ("SM64", 15905),       # créditos: TTC, barco, acuario
    145: ("SM64", 15960),       # pastel «The End»
    146: ("SM64", 15850),       # créditos: lava, pirámide
    147: ("SM64", 16035),       # tejado: aparece Yoshi
    148: ("SM3D", 16630),       # Yoshi en el tejado (Switch)
    149: ("SM3D", 16680),       # Yoshi, bandera, castillo y lago
}

# beats donde se OYE el juego porque la voz lo nombra (volumen del audio del clip)
AMBIENTE = {
    4: 0.7,
    20: 0.7,
    48: 0.6,
    49: 0.6,
    66: 0.8,
    77: 0.8,
    78: 0.7,
    80: 0.8,
    99: 0.6,
    101: 0.8,
    103: 0.8,
    107: 0.6,
    145: 0.7,
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
    assert len(beats) == len(PLAN) == 149, (len(beats), len(PLAN))
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
