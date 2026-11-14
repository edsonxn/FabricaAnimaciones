# -*- coding: utf-8 -*-
"""Escribe busquedas.json (3-nov-2026): teaser y video de los 40 años por {url, desde}; ESO Alik'r/Sentinel, Daggerfall Unity y
Redguard por {url, desde}; el resto, búsquedas de Skyrim con respaldo."""
import json, os
T, A, T18 = "mFu8t9735IY", "uvcfI8RPZYc", "OkFdqqyI8y4"
S1, S2, IN = "HcHnQerj81k", "oZytYzxUplg", "G-qydGkrHFc"
DU1, DU2, RG = "YbRhFZjjHlA", "F8QoNNZzQ7Y", "N7-Hup8Pqms"
G = "Skyrim 4k no HUD"
def u(i, d): return {"url": "https://youtu.be/" + i, "desde": d}
def q(*s): return list(s) + [G]
B = {
 1: u(T, 1.5), 2: u(T, 15), 3: u(T, 54), 4: q("Skyrim Thalmor justiciar no HUD"), 5: q("Skyrim landscape cinematic no HUD"),
 6: u(T, 22), 7: q("Skyrim Helgen intro cart no HUD"), 8: u(T, 2),
 9: u(A, 18), 10: u(A, 46), 11: u(A, 424), 12: u(T, 30), 13: u(A, 30), 14: u(A, 78), 15: u(A, 92), 16: u(A, 222), 17: u(A, 236), 18: u(A, 316),
 19: u(T18, 0), 20: u(T18, 9), 21: u(T18, 18), 22: u(DU1, 20), 23: u(DU1, 60),
 24: u(T, 32), 25: u(S1, 300), 26: ["Starfield character creation no commentary", "Starfield character creator"],
 27: ["Starfield intro mining no commentary", "Starfield gameplay no commentary"], 28: u(T, 24), 29: u(T, 27),
 30: u(S2, 600), 31: q("Skyrim Bannered Mare inn no HUD"),
 32: u(IN, 1200), 33: u(S1, 900), 34: u(IN, 3000), 35: u(IN, 5000), 36: u(DU1, 150), 37: u(S2, 1200), 38: u(IN, 6500),
 39: q("Skyrim Riverwood no HUD"), 40: q("Skyrim Dragonbone Dagger"), 41: q("Skyrim dagger sneak attack no HUD"),
 42: q("Skyrim Dragonsreach no HUD"), 43: q("Skyrim Whiterun 4k no HUD"),
 44: u(DU2, 200), 45: u(DU2, 500), 46: u(DU2, 900), 47: ["Daggerfall Numidium ending", "Daggerfall ending"],
 48: ["Daggerfall Unity Numidium", "Daggerfall ending"], 49: ["Daggerfall ending cinematic", "Daggerfall intro"],
 50: u(DU1, 300), 51: q("Alduin's Wall Sky Haven Temple no HUD"), 52: q("Sky Haven Temple Alduins Wall"), 53: u(T, 9),
 54: u(T, 10), 55: u(IN, 2000), 56: q("Skyrim Alikr warriors Whiterun"), 57: q("Saadia Bannered Mare Skyrim"),
 58: q("Skyrim In My Time of Need Kematu"), 59: q("Nazir Dark Brotherhood Sanctuary Skyrim"), 60: q("Skyrim Saadia Kematu choice"),
 61: u(RG, 30), 62: u(RG, 600), 63: u(S1, 1500), 64: u(RG, 1800), 65: u(RG, 3000),
 66: q("Skyrim sunrise no HUD"), 67: q("Skyrim Whiterun morning no HUD"), 68: q("Skyrim tundra 4k no HUD"),
 69: q("Skyrim aurora night no HUD"), 70: q("Skyrim campfire no HUD"),
 71: u(T, 53), 72: q("Skyrim intro Helgen no HUD"), 73: q("Skyrim Helgen execution no HUD"),
 74: q("Skyrim Season Unending Ulfric Tullius"), 75: q("Skyrim Thalmor patrol no HUD"), 76: u(S2, 1500),
 77: u(IN, 4000), 78: u(S1, 1800), 79: u(S2, 400), 80: u(IN, 7000), 81: u(IN, 7600),
 82: q("Skyrim Arcanaeum College of Winterhold no HUD"), 83: q("Skyrim library books no HUD"), 84: u(T, 53.5),
 85: q("Skyrim Thalmor embassy no HUD"), 86: q("Skyrim Elenwen Thalmor"), 87: u(S1, 2100), 88: u(IN, 7900),
 89: q("Skyrim Thalmor embassy party no HUD"), 90: q("Skyrim Legate Fasendil"), 91: u(IN, 5600), 92: u(T, 54),
 93: q("Skyrim Moth Priest Dexion Evicus"), 94: q("Skyrim Elder Scroll reading"), 95: q("Dexion Evicus Dawnguard"),
 96: ["Oblivion Imperial City White Gold Tower no commentary", "Oblivion Imperial City"], 97: u(IN, 6000),
 98: q("Skyrim Elder Scroll Throat of the World"), 99: q("Skyrim Dawnguard Elder Scroll"),
 100: q("Skyrim Elder Scroll read blind"), 101: q("Dexion blind Dawnguard"), 102: q("Skyrim Dawnguard Dexion reads scrolls"),
 103: q("Ancestor Glade Skyrim"), 104: u(T, 53.5), 105: q("Ancestor Glade moths Skyrim"), 106: q("Skyrim landscape 4k no HUD"),
 107: q("Skyrim Whiterun 4k no HUD"), 108: q("Skyrim Throat of the World no HUD"),
 109: u(T, 14), 110: u(T, 18), 111: q("Skyrim Time Wound Elder Scroll"), 112: q("Skyrim Time Wound Alduin"),
 113: q("Skyrim night sky stars no HUD"), 114: u(T, 10), 115: u(T, 26), 116: q("Skyrim Elder Scroll Dragon"),
 117: q("Skyrim Dawnstar no HUD"),
 118: q("Skyrim Bards College no HUD"), 119: q("Skyrim Riften 4k no HUD"), 120: q("Skyrim Solitude 4k no HUD"), 121: u(T, 53),
 122: u(T, 53), 123: u(S1, 2500), 124: u(T, 4), 125: q("Skyrim Time Wound"), 126: ["Daggerfall Unity ending", "Daggerfall ending"],
 127: q("Skyrim Thalmor Justiciar fight no HUD"), 128: q("Skyrim Thalmor Embassy interior no HUD"), 129: q("Skyrim Talos shrine no HUD"),
 130: q("Skyrim Sovngarde Alduin no HUD"), 131: u(T, 54), 132: u(T, 23), 133: q("Skyrim civil war battle no HUD"),
 134: q("Skyrim Solitude sunset no HUD"), 135: u(T, 21),
}
out = {f"scene-{k:03d}": v for k, v in sorted(B.items())}
assert len(out) == 135
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(out))

# ---- 2.ª vuelta (3-nov-2026, hojas medios_01-07): ESO longplays caían en cuadros de diálogo; webcam, marcas, menús, subtítulos
ESO = ["Sentinel ESO ambience", "Alikr Desert ambience", "Elder Scrolls Online Sentinel", "Alikr Desert ESO 4K"]
R = {25: ESO[2:], 30: ESO, 32: ESO[2:] + ESO[:1], 33: ESO[1:], 34: ESO[1:] + ESO[:1], 35: ["Sentinel docks ESO"] + ESO, 37: ESO,
     38: ESO[3:] + ESO[:2], 55: ESO[1:], 63: ["Elder Scrolls Online Hammerfell cinematic"] + ESO, 76: ESO[2:] + ESO[:1], 77: ["Sentinel palace ESO"] + ESO,
     78: ESO[:1] + ESO[3:], 79: ESO[1:], 81: ESO, 123: ESO[1:],
     22: u(DU2, 1100), 23: u(DU2, 60), 36: u(DU2, 700), 47: u(DU2, 1350), 48: ["Daggerfall Unity gameplay no commentary"], 126: u(DU1, 400),
     40: q("Skyrim Dragonbone weapons no HUD"), 58: q("Saadia Skyrim"), 82: q("Skyrim Arcanaeum no HUD"), 98: q("Throat of the World 4K"),
     105: q("Skyrim forest night no HUD"), 106: q("Skyrim Riverwood 4K no HUD"), 108: q("Skyrim Whiterun sunset no HUD"),
     121: q("High Hrothgar 4K no HUD"), 133: q("Skyrim civil war no HUD")}
B.update(R)
out = {f"scene-{k:03d}": v for k, v in sorted(B.items())}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("2.ª vuelta:", ",".join(str(k) for k in sorted(R)))
