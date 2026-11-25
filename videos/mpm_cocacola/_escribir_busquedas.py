# -*- coding: utf-8 -*-
"""Escribe busquedas.json (119 beats) a partir de metraje.md. U(id, s) = {url, desde}; lista = búsquedas de respaldo."""
import json
import os


def U(i, s):
    return {"url": f"https://www.youtube.com/watch?v={i}", "desde": s}


FOR, NG, HMN, KR = "zyrzswdZe2g", "wMctmMin9vM", "IUMK2LY3pIs", "fYW_-YRY5Ls"
PET1, PET2, UNR, FB = "bjXnCm56Ffo", "iDBJGpdEyTM", "hqnUohxXV0I", "1vKbdAkzOdo"
ARCA, HER, FEM, P39, P40 = "S2OuC_-QMUA", "rnpsIe1f84k", "nmO5t_RBKzw", "bcatrD251VA", "7wFEz_z0XhY"
VAULT, VAULT2, BLOOM, IMCC, DES = "o04s4TK8uLU", "gtuJx__HdpI", "VIyK6-DnUrg", "xHJQs_GlRhE", "9sWywI3oUTc"
KOFMX, KOF, RICA, BEP, VAL, LEON = "KwT0tTo-10Q", "Hb48mjM7_7Q", "NuteIxJeDUw", "eDinB9pnzhg", "MOUIthrECwQ", "GsCcOphYld4"
TL, SID, SEW, AND, ANDL, UNIV, DAN = "TcSgz8Ws_NE", "3VHBeoFd1FM", "DWXVQwxj3Q4", "yP4nzCHoVSE", "n7-XU3fNhpM", "u0rQ_7ymRo8", "jVDEicwgb4w"
ENV, PIASA, CANA, COCA, DW, EXC, CARAV = "k5rYCHnVCBs", "i6KtxJbcOQQ", "F6iqCOn2Fns", "LMDvYj73m6k", "drNnyghVWQ4", "pwkgy69eNI0", "jX811uAYkGc"
TOPO, CERRO = "TkUyPsArLa0", "7nSWQc5rSKg"

B = {
    1: ["Coca-Cola glass bottle condensation macro", "Coca-Cola bottle opening slow motion"], 2: U(P39, 285), 3: U(P39, 300),
    4: U(SID, 69), 5: U(HMN, 13), 6: U(KOFMX, 120), 7: U(FOR, 214), 8: U(ANDL, 43), 9: U(SID, 40), 10: U(FOR, 24),
    11: U(FOR, 0), 12: U(P39, 290), 13: U(P39, 305), 14: U(HER, 0), 15: U(HER, 8), 16: U(P39, 275), 17: U(P39, 580),
    18: U(P39, 600), 19: U(P40, 247), 20: U(P40, 262), 21: U(P39, 880), 22: U(HMN, 57), 23: U(BLOOM, 45), 24: U(HER, 14),
    25: U(TOPO, 29), 26: U(ARCA, 25), 27: U(FEM, 15), 28: U(KOFMX, 21), 29: U(KOFMX, 112), 30: U(DAN, 4),
    31: U(SID, 59), 32: U(FOR, 102), 33: U(NG, 211), 34: U(HMN, 33), 35: U(VAULT, 26), 36: U(VAULT, 56), 37: U(VAULT2, 3),
    38: U(NG, 168), 39: U(HMN, 71), 40: U(NG, 158), 41: U(BEP, 22),
    42: ["water well pump Mexico", "agua de pozo bomba"], 43: U(NG, 131), 44: U(NG, 192), 45: U(HMN, 51), 46: U(HMN, 76),
    47: U(TL, 7), 48: U(RICA, 389), 49: U(TL, 14), 50: U(SID, 24), 51: U(FOR, 160), 52: U(FOR, 68), 53: U(KR, 86),
    54: U(KR, 106), 55: U(UNIV, 38), 56: ["lemon juice squeeze slow motion", "squeezing lemon close up"], 57: U(NG, 23),
    58: U(NG, 266), 59: ["soda bubbles macro slow motion", "carbonated water bubbles macro"], 60: U(KR, 126), 61: U(SID, 44),
    62: U(KR, 132), 63: U(TL, 38), 64: U(HMN, 98), 65: U(FOR, 121), 66: U(NG, 99), 67: U(SEW, 138), 68: U(AND, 108),
    69: U(AND, 124), 70: U(NG, 244), 71: U(UNIV, 63), 72: U(FOR, 276), 73: U(DAN, 85), 74: U(DES, 188),
    75: ["tienda de abarrotes refrescos Mexico", "tiendita refrescos"], 76: U(NG, 43), 77: U(IMCC, 8), 78: U(ARCA, 80),
    79: U(DES, 123), 80: U(DW, 19), 81: U(RICA, 44), 82: U(LEON, 9), 83: ["Sheinbaum Coca-Cola inversión", "Sheinbaum Coca Cola"],
    84: U(VAL, 21), 85: U(UNIV, 20), 86: U(DW, 49), 87: U(COCA, 7), 88: U(COCA, 30), 89: U(P39, 669), 90: U(P39, 680),
    91: ["rusty nail in coca cola experiment", "clavo oxidado coca cola experimento"], 92: U(CANA, 0), 93: U(PIASA, 62),
    94: U(FB, 99), 95: U(FB, 35), 96: U(EXC, 124), 97: ["refrescos tienda Mexico refrigerador", "refrescos tienda Mexico"],
    98: U(ENV, 2), 99: U(ENV, 29), 100: U(UNR, 0), 101: U(UNR, 1082), 102: U(UNR, 566), 103: U(UNR, 635), 104: U(CERRO, 41),
    105: U(HER, 43), 106: U(ARCA, 49), 107: U(PET1, 5), 108: U(PET2, 110), 109: U(LEON, 3), 110: U(VAL, 83), 111: U(BEP, 53),
    112: U(DES, 104), 113: U(KOF, 100), 114: U(RICA, 392), 115: U(SID, 48), 116: ["lemon slices macro slow motion", "lemon juice close up"],
    117: U(DAN, 13), 118: U(CARAV, 13), 119: U(CARAV, 88),
}

aqui = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(aqui, "busquedas.json")
d = json.load(open(ruta, encoding="utf-8"))
for k in list(d):
    if k.startswith("scene-"):
        n = int(k.split("-")[1])
        d[k] = B[n]
json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(sum(1 for k in d if k.startswith("scene-")), "beats escritos")
