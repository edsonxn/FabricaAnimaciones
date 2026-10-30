# -*- coding: utf-8 -*-
"""Escribe busquedas.json (una lista de respaldos por beat). Reglas: inglés, 2-4 palabras, nombre propio primero, «no HUD» / «no
commentary» antes que «guide», sin apóstrofos, sin «exploit/glitch/enchanting» (traen menús). El sufijo Skyrim lo añade el motor."""
import json

G = "Skyrim 4k no HUD"
B = {
    1: ["Talos shrine no HUD"], 2: ["Skyrim landscape no HUD"], 3: ["Riften market no HUD"], 4: ["Skyrim mountain vista 4k no commentary"],
    5: ["Paarthurnax Throat of the World no HUD"], 6: ["Skyrim archer no HUD"], 7: ["Fort Dunstad no HUD"], 8: ["Soul Cairn no HUD"],
    9: ["Soul Cairn Dawnguard 4k no commentary"], 10: ["Skyrim character walking no HUD"], 11: ["Thalmor patrol no HUD"], 12: ["Castle Volkihar no HUD"],
    13: ["Volkihar Keep no HUD"], 14: ["Castle Volkihar 4k no commentary"], 15: ["Whiterun guard no HUD"], 16: ["Skyrim werewolf no HUD"],
    17: ["Saarthal no HUD"], 18: ["Skyrim snow coast no HUD"], 19: ["Hall of the Dead no HUD"], 20: ["Arkay shrine no HUD"],
    21: ["Falkreath graveyard no HUD"], 22: ["Skyrim giant no HUD"], 23: ["Giant camp no HUD"], 24: ["Markarth market no HUD"],
    25: ["Silver-Blood Inn no HUD"], 26: ["Markarth 4k no commentary"], 27: ["Skyrim two handed power attack no HUD"], 28: ["Skyrim sword combat no HUD"],
    29: ["Riverwood no HUD"], 30: ["Falkreath no HUD"], 31: ["Riften market no HUD"], 32: ["Skyrim warhammer combat no HUD"],
    33: ["Liars Retreat no HUD"], 34: ["Skyrim dwemer ruin no HUD"], 35: ["Dwemer ruin 4k no commentary"], 36: ["Winterhold coast no HUD"],
    37: ["Pilgrims Trench no HUD"], 38: ["Lydia follower no HUD"], 39: ["Skyrim follower no HUD"], 40: ["Blue Palace no HUD"],
    41: ["Solitude 4k no commentary"], 42: ["Castle Dour dungeon no HUD"], 43: ["Moesring Pass no HUD"], 44: ["Solstheim 4k no commentary"],
    45: ["Lakeview Manor no HUD"], 46: ["Riekling Solstheim no HUD"], 47: ["Hearthfire house no HUD"], 48: ["Old Hroldan no HUD"],
    49: ["Shrine of Mara no HUD"], 50: ["Blackreach no HUD"], 51: ["Blackreach 4k no commentary"], 52: ["Auriels Bow sun no HUD"],
    53: ["College of Winterhold no HUD"], 54: ["Skyrim mountain vista no HUD"], 55: ["Skyrim forest no HUD"], 56: ["Tel Mithryn no HUD"],
    57: ["Tel Mithryn 4k no commentary"], 58: ["Neloth Solstheim no HUD"], 59: ["Fort Frostmoth no HUD"], 60: ["Fort Frostmoth 4k no commentary"],
    61: ["Redwater Den no HUD"], 62: ["Redwater Den Dawnguard 4k no commentary"], 63: ["Skyrim vampire no HUD"], 64: ["College of Winterhold 4k no commentary"],
    65: ["Winterhold coast 4k no commentary"], 66: ["Journeymans Nook no HUD"], 67: ["Skyrim library no HUD"], 68: ["Arcanaeum no HUD"],
    69: ["Movarths Lair no HUD"], 70: ["Windhelm market no HUD"], 71: ["Windhelm 4k no commentary"], 72: ["Windhelm no HUD"],
    73: ["Paarthurnax no HUD"], 74: ["Throat of the World no HUD"], 75: ["Forgotten Vale no HUD"], 76: ["Forgotten Vale 4k no commentary"],
    77: ["Falmer no HUD"], 78: ["High Hrothgar no HUD"], 79: ["Alduin Sovngarde no HUD"], 80: ["Falkreath graveyard 4k no commentary"],
    81: ["Dead Mans Drink no HUD"], 82: ["Skyrim dragon sky no HUD"], 83: ["Skyrim tavern no HUD"], 84: ["Forelhost no HUD"],
    85: ["Forelhost 4k no commentary"], 86: ["Frostflow Lighthouse no HUD"], 87: ["Frostflow Lighthouse 4k no commentary"], 88: ["Frostflow Abyss no HUD"],
    89: ["Chaurus Reaper no HUD"], 90: ["High Hrothgar 4k no commentary"], 91: ["Greybeards no HUD"], 92: ["High Hrothgar interior no HUD"],
    93: ["Thalmor Embassy no HUD"], 94: ["Ratway no HUD"], 95: ["Delphine Riverwood no HUD"], 96: ["Ulfric Stormcloak no HUD"],
    97: ["Windhelm palace of the kings no HUD"], 98: ["Stormcloak camp no HUD"], 99: ["Rorikstead no HUD"], 100: ["Rorikstead 4k no commentary"],
    101: ["Frostfruit Inn no HUD"], 102: ["Skyrim follower walking no HUD"], 103: ["Riften 4k no commentary"], 104: ["Pride of Tel Vos no HUD"],
    105: ["Riften market 4k no commentary"], 106: ["Night Mother no HUD"], 107: ["Dark Brotherhood Sanctuary no HUD"], 108: ["Cicero wagon no HUD"],
    109: ["Cicero jester no HUD"], 110: ["Dawnstar Sanctuary no HUD"], 111: ["Night Mother 4k no commentary"], 112: ["Cicero no HUD"],
    113: ["Paarthurnax dialogue no HUD"], 114: ["Throat of the World 4k no commentary"], 115: ["Alduin no HUD"], 116: ["Paarthurnax Dragonborn no HUD"],
    117: ["Paarthurnax 4k no commentary"], 118: ["Skyrim dragon flying no HUD"], 119: ["Skyrim sunset no HUD"], 120: ["Skyrim landscape 4k no commentary"],
    121: ["Whiterun 4k no commentary"],
}
d = {f"scene-{k:03d}": v + [G] for k, v in B.items()}
json.dump(d, open("videos/tes_secretos_40/busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(d))
