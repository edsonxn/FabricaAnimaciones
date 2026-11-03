# -*- coding: utf-8 -*-
"""Plan de clips por beat (3-nov-2026) -> busquedas.json.   python plan_clips.py
Columna vertebral: Longplay Nexus «Pokémon Blue Version (1996)» YW29l3jJXr4 (1152p60, gris de Game Boy, franjas negras limpias;
capítulos: Pallet 148, Viridian 571, Forest 1156, Pewter 1806, Mt. Moon 3672, Cerulean 6676, Route 24/25 7190/8250, Vermilion 9741,
S.S. Anne 10750, Thunder 12327, Celadon 18340, Lavender 22857, Fuchsia 24758, Safari 26879, Power Plant 27763, Saffron 28856,
Marsh 30228, Cinnabar 32397, Earth 34583, Victory Road 34962, Elite Four 38114).
Especiales (todos ≥ 720p): MissingNo _ts7X7qFnwk / 8PILbqZqaS4, Mew glitch 3yWNEaeIcN0 / GEkQ2h92wI4 / b-cGPIgxxWg, Oak bR6jiah-PRg,
diploma _XHQ7ETjSt4, camión 1egJl8Zx6Bw / Pyg8tpvxDpI, Verde japonés KMfBEtptOnA, cable link KJ1H8ng8RhI, gritos (sprites
de los 151 en orden) Kvn3kHJFKuI, Cueva Celeste fxzzuj3nKEQ, Pueblo Lavanda con audio ZMn00JblPPw, oficiales k8c_C4vfUMo (FRLG Switch)
y 38XHXMdDegg (Winds and Waves).
Rehechos el 3-nov (sesión 2) tras mirar las hojas: 009 011 030-032 036 039 040 044 048 049 054-057 067 069-078 084 085 095 103
(posiciones exactas en previews/_scan/: Alto Mando, Lavanda, diploma, cable, MissingNo, Mew; gritos ≈ 1,03 s por Pokémon).
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
N = "YW29l3jJXr4"
MISS, MISS2 = "_ts7X7qFnwk", "8PILbqZqaS4"
MEWG, MEWZ, MEWL = "3yWNEaeIcN0", "GEkQ2h92wI4", "b-cGPIgxxWg"
OAK, DIPLO, TRUCK, TRUCKE = "bR6jiah-PRg", "_XHQ7ETjSt4", "1egJl8Zx6Bw", "Pyg8tpvxDpI"
VERDE, CABLE, GRITOS, CUEVA, LAV = "KMfBEtptOnA", "KJ1H8ng8RhI", "Kvn3kHJFKuI", "fxzzuj3nKEQ", "ZMn00JblPPw"
FRLG, WW = "k8c_C4vfUMo", "38XHXMdDegg"


def grito(n):
    """segundo del Pokémon n.º n en el video de los 151 gritos (medido el 3-nov: Rhydon 138, Jynx 152, Mewtwo 184)."""
    return round(0.6 + (n - 1) * 1.23, 1)


PLAN = {
    1: (MEWG, 175), 2: (MISS, 40), 3: (OAK, 60), 4: (FRLG, 20), 5: (N, 15),
    6: (N, 1181.5), 7: (N, 1300), 8: (N, 500), 9: (CABLE, 108), 10: (CABLE, 120), 11: (CABLE, 39),
    12: (VERDE, 30), 13: (VERDE, 400), 14: (N, 400), 15: (N, 3800), 16: (N, 5004.8), 17: (N, 6700),
    18: (VERDE, 10), 19: (N, 9800), 20: (N, 12400), 21: (N, 14600), 22: (N, 300), 23: (N, 34600), 24: (VERDE, 60),
    25: (VERDE, 120), 26: (VERDE, 150), 27: (VERDE, 180), 28: (N, 420),
    29: (N, 18400), 30: (DIPLO, 118), 31: (DIPLO, 146), 32: (N, 380), 33: (MISS, 80), 34: (MISS, 100), 35: (GRITOS, grito(112)),
    36: (GRITOS, 100), 37: (N, 8300), 38: (N, 12250), 39: (MEWG, 150), 40: (MEWG, 155), 41: (N, 8400), 42: (N, 3900),
    43: (N, 10750), 44: (TRUCK, 178), 45: (TRUCK, 200), 46: (TRUCKE, 120), 47: (TRUCKE, 150),
    48: (N, 39460), 49: (N, 39466), 50: (N, 26000), 51: (N, 27000), 52: (N, 31000), 53: (N, 3000),
    54: (N, 39648), 55: (N, 38622), 56: (N, 38672), 57: (N, 39655),
    58: (OAK, 120), 59: (OAK, 200), 60: (OAK, 300), 61: (OAK, 400),
    62: (VERDE, 3000), 63: (VERDE, 5000), 64: (N, 2000), 65: (N, 6000), 66: (N, 9000), 67: (N, 38550), 68: (N, 16002.7),
    69: (N, 38214), 70: (N, 38221), 71: (N, 38229), 72: (N, 38240),
    73: (LAV, 0), 74: (N, 22856), 75: (LAV, 186), 76: (LAV, 120), 77: (LAV, 164),
    78: (CUEVA, 20), 79: (CUEVA, 60), 80: (CUEVA, 150), 81: (N, 600),
    82: (MISS, 10), 83: (MISS, 50), 84: (MISS, 85), 85: (MISS, 96), 86: (N, 32450),
    87: (MEWZ, 27.6), 88: (MEWG, 30), 89: (MEWG, 90), 90: (MEWG, 180),
    91: (VERDE, 8000), 92: (VERDE, 9000), 93: (N, 20000), 94: (N, 21000),
    95: (MEWG, 205), 96: (MEWZ, 200), 97: (MEWL, 300), 98: (N, 24000), 99: (N, 150),
    100: (VERDE, 12000), 101: (N, 26500), 102: (N, 35000), 103: (CABLE, 9), 104: (N, 39350),
    105: (FRLG, 60), 106: (N, 39500), 107: (N, 400), 108: (N, 350), 109: (N, 200),
}

if __name__ == "__main__":
    out = {f"scene-{k:03d}": {"url": f"https://youtu.be/{v}", "desde": s} for k, (v, s) in sorted(PLAN.items())}
    assert len(out) == 109
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats")
