# -*- coding: utf-8 -*-
"""Escribe busquedas.json de «¿Qué pasó con los DWEMER?» (s3, 4-nov-2026): 191 beats, búsquedas en inglés de 2-4 palabras con un solo
nombre propio + respaldo genérico de ruinas dwemer; Morrowind / ESO / Daggerfall donde la voz habla de ellos."""
import json
import os

G = "Skyrim Dwemer ruins no commentary"
M = "Morrowind gameplay no commentary"
E = "ESO Clockwork City no commentary"


def q(*s):
    return list(s) + [G]


def mw(*s):
    return list(s) + [M]


def eso(*s):
    return list(s) + [E]


B = {
 1: q("Skyrim Blackreach 4k no HUD"), 2: q("Skyrim Dwarven Centurion no commentary"), 3: q("Skyrim Dwemer ruin 4k no HUD"),
 4: q("Skyrim Blackreach cinematic"), 5: q("Skyrim Dwemer ruins 4k"), 6: q("Skyrim Arniel Gane"),
 7: q("Skyrim Markarth 4k no HUD"), 8: q("Skyrim Dwarven Sphere"), 9: q("Skyrim Dwarven Spider"), 10: q("Skyrim Markarth night no HUD"),
 11: q("Skyrim Falmer no commentary"), 12: q("Skyrim Blackreach Silent City"), 13: q("Skyrim Dwarven Centurion fight"),
 14: q("Skyrim Numidium"), 15: q("Skyrim Tower of Mzark"), 16: q("Septimus Signus outpost"), 17: q("Skyrim Arniel's Endeavor"),
 18: q("Skyrim Dwemer ruin 4k no HUD"),
 19: q("Skyrim Dwarven armor"), 20: q("Skyrim Dwemer ruin deep"), 21: q("Skyrim Dwemer architecture 4k"),
 22: q("Skyrim giant mammoth no HUD"), 23: q("Skyrim giant camp no HUD"), 24: eso("ESO Sotha Sil"),
 25: q("Skyrim Dwarven Spider fight"), 26: q("Skyrim Dwemer machinery no HUD"), 27: q("Skyrim Dwarven Sphere fight"),
 28: q("Skyrim Dwarven Centurion awakens"), 29: q("Skyrim Dwarven Centurion melee"), 30: q("Skyrim Bthardamz"),
 31: q("Skyrim Dwemer steam pipes"),
 32: q("Skyrim Markarth 4k no HUD"), 33: q("Skyrim Markarth waterfall no HUD"), 34: q("Skyrim Understone Keep no HUD"),
 35: q("Skyrim Nchuand-Zel"), 36: q("Skyrim The Lost Expedition"), 37: q("Skyrim Understone Keep throne"),
 38: q("Skyrim Calcelmo"), 39: q("Skyrim Dwemer Museum"), 40: q("Skyrim Dwemer Museum Markarth"), 41: q("Skyrim Calcelmo's Tower"),
 42: q("Skyrim Hard Answers"), 43: q("Skyrim Calcelmo laboratory"), 44: q("Skyrim Dwemer ruin interior"), 45: q("Skyrim Calcelmo dialogue"),
 46: q("Skyrim Jarl throne room no HUD"), 47: q("Skyrim Jarl Igmund Markarth"), 48: ["Oblivion Imperial City gameplay", "Oblivion gameplay no commentary"],
 49: q("Skyrim Falmer village"),
 50: q("Skyrim Snow Elf Gelebor"), 51: q("Skyrim Falmer Blackreach"), 52: q("Skyrim Blackreach mushrooms"), 53: q("Skyrim Falmer torture"),
 54: q("Skyrim Falmer hive"), 55: q("Skyrim Falmer ambush"),
 56: q("Skyrim Frozen Hearth Winterhold"), 57: q("Skyrim Winterhold no HUD"), 58: q("Skyrim Falmer warband"), 59: q("Skyrim Blackreach empty city"),
 60: q("Skyrim Falmer Gloomlurker"), 61: q("Skyrim Ysgramor tomb"), 62: q("Skyrim Falmer close up"),
 63: q("Skyrim Blackreach 4k no HUD"), 64: q("Skyrim Blackreach cavern"), 65: q("Skyrim Alftand"), 66: q("Skyrim Attunement Sphere"),
 67: q("Skyrim Blackreach lake"), 68: q("Skyrim Vulthuryol"), 69: q("Skyrim Crimson Nirnroot"),
 70: q("Skyrim Alftand glacial ruins"), 71: q("Skyrim Alftand expedition"), 72: q("Skyrim J'darr Alftand"), 73: q("Skyrim Alftand Cathedral"),
 74: q("Skyrim Alftand animonculory"), 75: q("Skyrim Dwemer ruin 4k no HUD"),
 76: q("Skyrim College of Winterhold no HUD"), 77: q("Skyrim landscape 4k no HUD"), 78: q("Skyrim Markarth 4k no HUD"),
 79: q("Skyrim aurora night no HUD"), 80: q("Skyrim library books no HUD"), 81: q("Skyrim tavern no HUD"),
 82: q("Skyrim Arkngthamz"), 83: q("Skyrim Dwarven resonator"), 84: q("Skyrim Arkngthamz tonal lock"), 85: q("Skyrim Arkngthamz resonators"),
 86: q("Skyrim tonal lock puzzle"), 87: q("Skyrim Dwarven Ballista"), 88: q("Skyrim Dwemer ruin hall"),
 89: q("Skyrim Lost to the Ages"), 90: q("Skyrim Arkngthamz earthquake"), 91: q("Skyrim Aetherium shard"), 92: q("Skyrim Katria ghost"),
 93: q("Skyrim Deep Folk Crossing"), 94: q("Skyrim Aetherium Forge"), 95: q("Skyrim Aetherial Crown"), 96: q("Skyrim Zephyr bow"),
 97: q("Skyrim Mzulft"), 98: q("Skyrim Revealing the Unseen"), 99: q("Skyrim Gavros Plinius"), 100: q("Skyrim Mzulft Oculory"),
 101: q("Skyrim Oculory map projection"), 102: q("Skyrim Nerien Psijic"), 103: q("Skyrim Dwarven metal ingot"),
 104: q("Skyrim Riften 4k no HUD"), 105: q("Skyrim Whiterun 4k no HUD"), 106: q("Skyrim Solitude 4k no HUD"), 107: q("Skyrim landscape cinematic no HUD"),
 108: q("Skyrim Elder Scroll reading"), 109: q("Skyrim Moth Priest Dexion"), 110: q("Septimus Signus Skyrim"), 111: q("Skyrim Tower of Mzark"),
 112: q("Skyrim Tower of Mzark Oculory"), 113: q("Skyrim Elder Scroll Mzark"), 114: q("Skyrim Tower of Mzark skeleton"),
 115: q("Skyrim Dwemer statue"), 116: q("Skyrim Daedric shrine no HUD"), 117: q("Skyrim Dwemer machinery no HUD"),
 118: eso("ESO Clockwork City"), 119: q("Skyrim Ancient Tales of the Dwemer"), 120: q("Skyrim Dwemer ruin hall"),
 121: ["Daggerfall Numidium", "Daggerfall Unity ending"],
 122: ["Daggerfall Unity Numidium", "Daggerfall ending"], 123: q("Skyrim Tiber Septim statue"), 124: ["ESO Summerset no commentary", "Summerset Isles ESO"],
 125: ["Daggerfall ending cinematic", "Daggerfall Unity ending"], 126: mw("Morrowind Akulakhan"), 127: mw("Morrowind Red Mountain Dagoth Ur"),
 128: q("Skyrim Dwemer treasure chest"),
 129: q("Skyrim landscape 4k no HUD"), 130: q("Skyrim Throat of the World no HUD"),
 131: q("Septimus Signus outpost"), 132: q("Skyrim Septimus Dwemer box"), 133: q("Skyrim Essence Extractor"), 134: q("Skyrim Discerning the Transmundane"),
 135: q("Skyrim Oghma Infinium"), 136: q("Skyrim Hermaeus Mora Septimus"), 137: q("Skyrim Hermaeus Mora"),
 138: mw("Morrowind Red Mountain"), 139: mw("Morrowind Heart of Lorkhan"), 140: mw("Morrowind Dagoth Ur heart chamber"),
 141: mw("Morrowind Heart Chamber"), 142: mw("Morrowind Dwemer ruins"), 143: mw("Morrowind Vivec city"), 144: mw("Morrowind Dwemer ruin"),
 145: mw("Morrowind Dwemer library"),
 146: mw("Morrowind Kagrenac's Tools"), 147: mw("Morrowind Sunder Keening"), 148: mw("Morrowind Wraithguard"), 149: mw("Morrowind Dwemer forge"),
 150: mw("Morrowind Red Mountain ash"), 151: mw("Morrowind Dwemer ruin interior"),
 152: q("Skyrim Riverwood no HUD"), 153: q("Skyrim landscape 4k no HUD"), 154: q("Skyrim Whiterun 4k no HUD"),
 155: mw("Morrowind Red Mountain"), 156: mw("Morrowind Red Mountain storm"), 157: eso("ESO Nerevar"), 158: mw("Morrowind Vivec"),
 159: mw("Morrowind Dagoth Ur fight"), 160: mw("Morrowind Azura shrine"), 161: mw("Morrowind Ashlander camp"), 162: mw("Morrowind Dagoth Ur"),
 163: q("Skyrim Time Wound"),
 164: mw("Morrowind Tel Fyr"), 165: mw("Morrowind Yagrum Bagarn"), 166: mw("Morrowind Corprusarium"), 167: mw("Morrowind Yagrum Bagarn dialogue"),
 168: mw("Morrowind Divayth Fyr"), 169: ["Morrowind Tribunal Bamz-Amschend", "Morrowind Tribunal Mournhold"], 170: ["Morrowind Mournhold", "Morrowind Tribunal gameplay"],
 171: q("Skyrim Septimus Signus ash"),
 172: q("Skyrim College of Winterhold no HUD"), 173: q("Skyrim Arniel Gane"), 174: q("Skyrim Keening dagger"), 175: q("Skyrim Dwemer Convector"),
 176: q("Skyrim Arniel's Endeavor Keening"), 177: q("Skyrim Arniel's Endeavor ending"), 178: q("Skyrim Arniel disappears"),
 179: q("Skyrim Hall of Attainment"), 180: q("Skyrim Arniel's Shade"), 181: q("Skyrim Blackreach 4k no HUD"), 182: q("Skyrim Arniel's Shade summon"),
 183: q("Skyrim Dwemer ruin 4k no HUD"),
 184: q("Skyrim landscape cinematic no HUD"), 185: q("Skyrim Blackreach cinematic"), 186: q("Skyrim tavern bard no HUD"),
 187: q("Skyrim Whiterun 4k no HUD"), 188: q("Skyrim Riften 4k no HUD"), 189: q("Skyrim Elder Scroll reading"), 190: q("Skyrim Solitude 4k no HUD"),
 191: q("Skyrim sunrise no HUD"),
}

AQUI = os.path.dirname(os.path.abspath(__file__))
beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
ids = [b["id"] for b in (beats if isinstance(beats, list) else beats["beats"])]
assert len(ids) == len(B) == 191, (len(ids), len(B))
json.dump({f"scene-{n:03d}": v for n, v in sorted(B.items())}, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("busquedas.json:", len(B))
