# -*- coding: utf-8 -*-
"""Plan de clips POR BEAT de bt_jiggies_crueles (23-oct-2026): cada beat -> (parte de la serie Ninbanyan NSO, segundo) ya
MIRADO en hojas de contacto propias a 360p (%TEMP%/btj/scan, un cuadro cada 4-15 s con el segundo impreso; mapa de partes en
mapa_clips.md). `python plan_clips.py` escribe busquedas.json. Evitados: iris de pieza de puzle, rótulos «Subscribe/Smash that
like» del canal (P07 1372-1379, P39 318), menús de pausa.
"""
import json
import os

P = {2: "mCeQj7py8g4", 7: "5Cmj9VrrfTU", 11: "FTD7c-BfDI4", 12: "7dMWrzSckCo", 18: "3OiDVU9YnyI", 19: "0oEvo3BB6Ls",
     25: "lqZOLOE_h8A", 26: "K1dZ0qRmU1I", 31: "I_bWv3nUK5c", 32: "UmgVCgOUVeE", 39: "MKpzMtyZOK0", 41: "CDyIfCHE5lg",
     42: "7Gzu82cUN4I"}

PLAN = {   # beat: (parte, segundo)
    1: (11, 63), 2: (39, 445), 3: (31, 100), 4: (32, 914), 5: (12, 110),
    6: (11, 3), 7: (26, 50), 8: (11, 340), 9: (11, 393), 10: (11, 93),
    11: (39, 3), 12: (42, 330), 13: (42, 370), 14: (42, 410), 15: (42, 418), 16: (42, 466),
    17: (41, 1398), 18: (41, 1188), 19: (41, 1413), 20: (41, 1512), 21: (41, 1540), 22: (41, 1556),
    23: (19, 320), 24: (19, 112), 25: (19, 144), 26: (19, 192), 27: (19, 208), 28: (19, 264), 29: (19, 160),
    30: (25, 3), 31: (26, 228), 32: (26, 38), 33: (26, 20), 34: (26, 160), 35: (26, 190), 36: (26, 232),
    37: (11, 258), 38: (12, 12), 39: (12, 50), 40: (12, 105), 41: (12, 145), 42: (12, 225),
    43: (18, 328), 44: (18, 352), 45: (18, 474), 46: (18, 515), 47: (18, 605),
    48: (32, 928), 49: (32, 830), 50: (32, 858), 51: (32, 886), 52: (32, 956), 53: (32, 1040), 54: (32, 1096), 55: (32, 1208),
    56: (7, 640), 57: (7, 652), 58: (7, 664), 59: (7, 688), 60: (7, 600), 61: (7, 728),
    62: (31, 46), 63: (31, 76), 64: (31, 118), 65: (31, 160), 66: (31, 190), 67: (31, 226),
    68: (39, 258), 69: (7, 1386), 70: (39, 363), 71: (39, 438), 72: (39, 453), 73: (39, 468), 74: (39, 483), 75: (39, 330),
    76: (39, 408),
    77: (42, 480), 78: (39, 513), 79: (11, 168), 80: (12, 430),
}

if __name__ == "__main__":
    aqui = os.path.dirname(os.path.abspath(__file__))
    beats = json.load(open(os.path.join(aqui, "beats.json"), encoding="utf-8"))
    out = {}
    for b in beats:
        n = int(b["id"].split("-")[1])
        parte, s = PLAN[n]
        out[b["id"]] = {"url": f"https://youtu.be/{P[parte]}", "desde": s}
    json.dump(out, open(os.path.join(aqui, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats -> busquedas.json")
