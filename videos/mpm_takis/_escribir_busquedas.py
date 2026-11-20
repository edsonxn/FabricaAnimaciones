# -*- coding: utf-8 -*-
"""Escribe busquedas.json (114 beats). Fuentes en metraje.md. U(id, s) = {url, desde}; lista = respaldos por búsqueda."""
import json
import os


def U(i, s):
    return {"url": f"https://www.youtube.com/watch?v={i}", "desde": s}


MX, CH, CH2, HC, HIM = "FZRdk5QV1fg", "y_XpsXdGO3g", "uQyv9RdIS2Q", "2-ed6djsAWk", "YkLTUxN0GgU"
BIM, BIM2, LER = "Td6a_1Wzepw", "QWWc1kq0LmI", "mLUO_Zq3HeI"
B = {
    1: U("VZ_tD2kYGrc", 2), 2: U("Q6b1__rHFrU", 3), 3: U("WEWuxYCYOcE", 1), 4: U("jgnDqmJ-mtk", 40), 5: U(CH, 70),
    6: U(BIM, 2), 7: ["supermarket chips aisle", "grocery store snack aisle"], 8: U(LER, 26), 9: U(MX, 9), 10: U(BIM, 68),
    11: U(BIM, 35), 12: U(BIM, 13), 13: ["Sabritas comercial", "Sabritas anuncio"], 14: U(BIM, 20),
    15: ["Barcel comercial", "Barcel anuncio Mexico"], 16: ["Barcel papas comercial", "Barcel Runners comercial"], 17: U(BIM, 168),
    18: U(CH, 85), 19: ["tacos dorados receta", "flautas fritas"], 20: U("MaOjiM2gK3M", 3), 21: U("MaOjiM2gK3M", 11),
    22: U("C61HvyA0Ur4", 3), 23: U("dW5WWWg2ln4", 3), 24: U("rFi1v1OLuKo", 5), 25: U(HC, 100), 26: U("VZ_tD2kYGrc", 11),
    27: U("NeKc2uk851U", 20), 28: U("NeKc2uk851U", 200), 29: U(HIM, 35), 30: U("jgnDqmJ-mtk", 10), 31: U("6yWEs4MGhsw", 300),
    32: U("6yWEs4MGhsw", 900), 33: U(HIM, 122), 34: ["maquina tortilladora tortilleria", "tortilleria tortillas maquina"],
    35: U(HIM, 131), 36: U(HC, 52), 37: U(HIM, 139), 38: U(HC, 61), 39: U(CH, 25), 40: U(CH, 40), 41: U(CH, 70 + 1),
    42: U(CH2, 11), 43: U(CH, 79), 44: U(MX, 1), 45: U("BHXtF1s_2x0", 103), 46: U("TUDMAlF5AHs", 100), 47: U(HIM, 220),
    48: U(HIM, 229), 49: ["continuous fryer snack line", "tortilla chip fryer industrial"], 50: ["Coppell Texas drone", "Coppell Texas"],
    51: U(HC, 135), 52: U(HC, 143), 53: U("BHXtF1s_2x0", 196), 54: U("nT_TyDVpo7s", 1), 55: U("4qgRDrvimUo", 5),
    56: U("hUX-X4w7lf0", 2), 57: U(MX, 17), 58: ["Manhattan federal courthouse", "New York courthouse exterior"], 59: U(MX, 25),
    60: U(HC, 155), 61: U(MX, 44), 62: U("40JGmW3HPRk", 10), 63: U("zs3QjSIPnoc", 10), 64: U("Q6b1__rHFrU", 10),
    65: ["Takis UK advert", "Takis UK"], 66: ["paprika turmeric spices", "turmeric powder spice"], 67: U(BIM2, 58),
    68: ["trucks border crossing Laredo", "Mexico US border trucks"], 69: U(MX, 36), 70: ["Coppell Texas", "Dallas Fort Worth aerial"],
    71: U("rFi1v1OLuKo", 20), 72: ["supermarket snack aisle", "grocery store chips aisle"],
    73: ["gas station convenience store interior", "convenience store interior"], 74: ["Houston skyline drone", "Houston Texas aerial"],
    75: ["high school hallway students", "middle school students hallway"], 76: U("RzIZP3N84dk", 2), 77: U("bcYNY-aSu9U", 2),
    78: U("4qgRDrvimUo", 13), 79: U(BIM, 86), 80: U("d19GRpA5pHU", 3), 81: ["Doritos commercial", "Tostitos commercial"],
    82: ["PepsiCo headquarters Purchase New York", "PepsiCo headquarters"], 83: ["Doritos Dinamita Super Bowl commercial 2024", "Doritos Dinamita commercial"],
    84: U(BIM2, 66), 85: U(BIM, 108), 86: U("hM1Wlj17kLM", 1), 87: U("zdNi9TLQEBI", 20), 88: U("zdNi9TLQEBI", 60),
    89: U("Wx8XYFh7_LY", 20), 90: U("Wx8XYFh7_LY", 60), 91: U("v4fMtN9nxDA", 30), 92: ["Paqui One Chip Challenge", "One Chip Challenge"],
    93: ["Paqui one chip challenge pulled from shelves", "One Chip Challenge removed stores news"], 94: U("u-tF2hrc4dw", 20),
    95: U("ThOlH3P2UCs", 5), 96: U("lV-V60XCzaI", 30), 97: U("ThOlH3P2UCs", 30), 98: U("lV-V60XCzaI", 90), 99: U("d19GRpA5pHU", 12),
    100: ["London street drone", "London aerial"], 101: U(LER, 5), 102: ["Hermosillo Sonora drone", "Hermosillo Sonora"], 103: U(MX, 52),
    104: ["Coppell Texas", "Coppell Texas city"], 105: ["Rotherham drone", "Rotherham aerial"], 106: ["Takis UK", "Takis UK advert"],
    107: ["London corner shop", "London convenience store"], 108: ["Takis Fuego commercial", "Takis Fuego ad"], 109: U("TUDMAlF5AHs", 200),
    110: U(BIM2, 10), 111: ["paprika powder", "turmeric powder"], 112: U("rFi1v1OLuKo", 30), 113: U(HC, 10),
    114: ["Takis Blue Heat commercial", "Takis Blue Heat ad"],
}
assert sorted(B) == list(range(1, 115))
out = {f"scene-{k:03d}": v for k, v in sorted(B.items())}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "busquedas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("ok", len(out))
