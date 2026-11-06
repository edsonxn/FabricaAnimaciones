# -*- coding: utf-8 -*-
"""Escribe busquedas.json de «Los 20 seres más PODEROSOS de Tamriel» (s2, 5-nov-2026): 172 beats, búsquedas en inglés de 2-4
palabras con un solo nombre propio + respaldo genérico; Oblivion / Morrowind / ESO donde la voz habla de ellos."""
import json
import os

G = "Skyrim cinematic no HUD"
O = "Oblivion gameplay no commentary"
M = "Morrowind gameplay no commentary"
E = "ESO cinematic"


def q(*s):
    return list(s) + [G]


def ob(*s):
    return list(s) + [O]


def mw(*s):
    return list(s) + [M]


def eso(*s):
    return list(s) + [E]


B = {
 # gancho
 1: eso("ESO Mannimarco cinematic"), 2: q("Skyrim Sheogorath Pelagius"), 3: q("Skyrim Alduin Throat of the World"),
 4: q("Skyrim Arcanaeum library"), 5: q("Skyrim Dragonborn shout dragon"), 6: q("Skyrim night sky stars no HUD"),
 # voces
 7: q("Skyrim Whiterun 4k no HUD"), 8: q("Skyrim tavern bard no HUD"), 9: q("Skyrim Greybeards High Hrothgar"),
 10: q("Skyrim Temple of Mara Riften"), 11: q("Skyrim Arcanaeum Urag"), 12: mw("Morrowind Vivec city"),
 13: q("Skyrim dragon fight 4k"), 14: q("Skyrim Shrine of Talos"), 15: q("Skyrim Daedric shrine Azura"),
 16: q("Skyrim aurora night no HUD"),
 # 20 Mannimarco
 17: eso("ESO Mannimarco"), 18: eso("ESO Artaeum"), 19: eso("ESO Psijic Order"), 20: ob("Oblivion Arcane University"),
 21: ob("Oblivion Mannimarco"), 22: eso("ESO Coldharbour Mannimarco"), 23: ob("Oblivion necromancer lair"),
 24: q("Skyrim night Masser Secunda"),
 # 19 Divayth Fyr
 25: mw("Morrowind Tel Fyr"), 26: mw("Morrowind Divayth Fyr"), 27: mw("Morrowind Corprusarium"), 28: mw("Morrowind Divayth Fyr cure"),
 29: mw("Morrowind Tel Fyr tower"), 30: eso("ESO Divayth Fyr"), 31: mw("Morrowind Telvanni tower"),
 # 18 Miraak
 32: q("Skyrim Miraak"), 33: q("Skyrim Solstheim 4k"), 34: q("Skyrim Bend Will dragon ride"), 35: q("Skyrim Apocrypha"),
 36: q("Skyrim Solstheim All-Maker Stone"), 37: q("Skyrim Miraak death Hermaeus Mora"), 38: q("Skyrim Apocrypha Black Book"),
 # 17 Pelinal
 39: ob("Oblivion Knights of the Nine Pelinal"), 40: ob("Oblivion Ayleid ruin"), 41: ob("Oblivion Crusader armor"),
 42: ob("Oblivion White Gold Tower"), 43: ob("Oblivion Umaril"), 44: ob("Oblivion Knights of the Nine"),
 45: ob("Oblivion Umaril final battle"),
 # cr1
 46: q("Skyrim courier letter"), 47: q("Skyrim Solitude 4k no HUD"), 48: q("Skyrim bard college"), 49: q("Skyrim Bards College Solitude"),
 50: mw("Morrowind Red Mountain"),
 # 16 Dagoth Ur
 51: mw("Morrowind Dagoth Ur"), 52: mw("Morrowind Red Mountain"), 53: mw("Morrowind Blight storm"), 54: mw("Morrowind Sixth House"),
 55: mw("Morrowind Ghostfence"), 56: mw("Morrowind Akulakhan"), 57: mw("Morrowind Vivec city"),
 # 15 Vivec
 58: mw("Morrowind Vivec god"), 59: mw("Morrowind Vivec city cantons"), 60: mw("Morrowind Ministry of Truth"),
 61: mw("Morrowind Ministry of Truth"), 62: mw("Morrowind Wraithguard"), 63: eso("ESO Vivec"), 64: eso("ESO Vivec city"),
 # 14 Alduin
 65: q("Skyrim Alduin"), 66: q("Skyrim dragon priest"), 67: q("Skyrim Throat of the World Alduin"), 68: q("Skyrim Helgen Alduin"),
 69: q("Skyrim Alduin resurrect dragon"), 70: q("Skyrim Sovngarde"), 71: q("Skyrim Dragonborn"),
 # 13 Sangre de Dragón
 72: q("Skyrim Alduin fight"), 73: q("Skyrim absorb dragon soul"), 74: q("Skyrim Dragonrend"), 75: q("Skyrim Miraak fight"),
 76: q("Skyrim Whiterun 4k no HUD"),
 # ag1 + dato
 77: q("Skyrim tavern no HUD"), 78: q("Skyrim landscape 4k no HUD"), 79: q("Skyrim Alik'r desert"), 80: q("Skyrim Riverwood no HUD"),
 81: q("Skyrim Markarth 4k no HUD"), 82: q("Skyrim Arcanaeum library"), 83: q("Skyrim bard lute"), 84: q("Skyrim Shrine of Talos"),
 85: q("Skyrim Talos statue Whiterun"), 86: q("Skyrim Heimskr Talos"),
 # 12 Talos
 87: q("Skyrim Talos statue"), 88: ob("Oblivion Imperial City"), 89: ob("Oblivion White Gold Tower"), 90: q("Skyrim Shrine of Talos"),
 91: q("Skyrim Thalmor Justiciar"), 92: q("Skyrim Blessing of Talos"), 93: q("Skyrim Stormcloak soldiers"),
 # 11 Numidium
 94: mw("Morrowind Akulakhan"), 95: mw("Morrowind Dwemer ruin"), 96: eso("ESO Summerset"), 97: eso("ESO Alinor"),
 98: q("Skyrim Dwemer ruins"), 99: mw("Morrowind Akulakhan Red Mountain"),
 # 10 Molag Bal
 100: eso("ESO Molag Bal"), 101: q("Skyrim Daedric shrine"), 102: eso("ESO Coldharbour"), 103: eso("ESO Dark Anchor"),
 104: eso("ESO Dark Anchor"), 105: q("Skyrim House of Horrors"), 106: q("Skyrim Mace of Molag Bal"),
 # 9 Mehrunes Dagon
 107: ob("Oblivion Mehrunes Dagon"), 108: ob("Oblivion Uriel Septim death"), 109: ob("Oblivion Kvatch gate"),
 110: ob("Oblivion Mehrunes Dagon Imperial City"), 111: ob("Oblivion Martin Avatar of Akatosh"), 112: q("Skyrim Mehrunes Razor"),
 113: ob("Oblivion Akatosh Dagon fight"),
 # 8 Sheogorath / Jyggalag
 114: ob("Shivering Isles Sheogorath"), 115: ob("Shivering Isles New Sheoth"), 116: ob("Shivering Isles Jyggalag"),
 117: ob("Shivering Isles Greymarch"), 118: q("Skyrim Mind of Madness Sheogorath"), 119: q("Skyrim Sheogorath Pelagius"),
 120: q("Skyrim Hermaeus Mora"),
 # 7 Hermaeus Mora
 121: q("Skyrim Apocrypha"), 122: q("Skyrim Hermaeus Mora"), 123: q("Skyrim Oghma Infinium"), 124: q("Skyrim Septimus Signus"),
 125: q("Skyrim Dragonborn Hermaeus Mora"), 126: q("Skyrim Apocrypha Black Book"),
 # campaña
 127: q("Skyrim landscape 4k no HUD"), 128: q("Skyrim sunrise no HUD"),
 # 6 Magnus
 129: q("Skyrim sun sky no HUD"), 130: q("Skyrim sunset no HUD"), 131: q("Skyrim night sky stars"), 132: q("Skyrim College of Winterhold"),
 133: q("Skyrim sun rays no HUD"), 134: q("Skyrim Eye of Magnus"),
 # 5 Akatosh
 135: ob("Oblivion Avatar of Akatosh"), 136: ob("Oblivion Temple of the One"), 137: q("Skyrim Elder Scroll time wound"),
 138: ob("Oblivion Martin Avatar of Akatosh"), 139: q("Skyrim Dragonborn shout"), 140: q("Skyrim Dragon soul absorb"),
 141: q("Skyrim Red Mountain Solstheim"),
 # 4 Lorkhan
 142: mw("Morrowind Heart of Lorkhan"), 143: mw("Morrowind Heart of Lorkhan"), 144: mw("Morrowind Red Mountain"),
 145: q("Skyrim Sovngarde"), 146: mw("Morrowind Dagoth Ur heart"), 147: q("Skyrim Shor's Stone"),
 # 3 Padomay
 148: eso("ESO Oblivion Daedra"), 149: q("Skyrim night sky aurora"), 150: q("Skyrim Daedra summon"), 151: q("Skyrim Dark Brotherhood Sanctuary"),
 152: q("Skyrim Night Mother"),
 # 2 Anu
 153: q("Skyrim aurora no HUD"), 154: q("Skyrim sunrise mountains no HUD"), 155: q("Skyrim night sky Masser"),
 156: q("Skyrim landscape cinematic"), 157: q("Skyrim Throat of the World view"),
 # 1 Godhead
 158: q("Skyrim night sky stars"), 159: q("Skyrim Elder Scroll"), 160: q("Skyrim aurora night"), 161: q("Skyrim Sovngarde"),
 162: q("Skyrim Elder Scroll reading"), 163: mw("Morrowind Vivec"), 164: q("Skyrim sunset cinematic"),
 # cierre
 165: q("Skyrim Throat of the World"), 166: q("Skyrim Azura shrine"), 167: q("Skyrim tavern no HUD"), 168: q("Skyrim Riften 4k no HUD"),
 169: q("Skyrim Solitude 4k no HUD"), 170: mw("Morrowind Vivec city"), 171: q("Skyrim landscape 4k no HUD"), 172: q("Skyrim sunrise no HUD"),
}

AQUI = os.path.dirname(os.path.abspath(__file__))
beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
ids = [b["id"] for b in (beats if isinstance(beats, list) else beats["beats"])]
assert len(ids) == len(B) == 172, (len(ids), len(B))
json.dump({f"scene-{n:03d}": v for n, v in sorted(B.items())}, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("busquedas.json:", len(B))
