# -*- coding: utf-8 -*-
"""Escribe busquedas.json (10-nov-2026) desde clips_candidatos.md + investigacion.md. «id@s» = url + desde; lista = búsquedas."""
import json
import os

B = {
    # intro
    1: "LNfT31D87bU@60", 2: "fVfS9u-GhWg@1", 3: "TS701bMxmSI@10", 4: "eW2lZ_G4gww@60", 5: "lwSMdQzAiJ0@35",
    6: "IvhI73INQRY@300", 7: "Vfh8jUFGkoI@200", 8: "De7Axarv12E@20",
    # 30 Private Eye
    9: "7eGsKqV-93A@300", 10: "ieru3rLTzQA@400", 11: "7eGsKqV-93A@900", 12: "ieru3rLTzQA@1200",
    # 29 BO3 muerto
    13: ["Black Ops 3 first mission no commentary", "Black Ops 3 campaign Black Ops mission"],
    14: ["Black Ops 3 cybernetic surgery cutscene", "Black Ops 3 campaign intro cutscene"],
    15: "zhqtK866jAU@20", 16: "zhqtK866jAU@90", 17: "tbt-nRthjXw@60",
    # 28 Russman
    18: "GkT73ylsTzQ@120", 19: "uFld4ZaGubk@200", 20: "GkT73ylsTzQ@900", 21: "uFld4ZaGubk@1100",
    22: ["Tag der Toten ending cutscene", "Tag der Toten no commentary"],
    # 27 fuego verde
    23: "IIdAefGoc9A@60", 24: "_fri1iueqNY@200", 25: "2M4ZknQZYJ0@282", 26: "IIdAefGoc9A@600",
    # 26 retratos Kino
    27: "0ZQnzC6A0uY@120", 28: "15yDXFYyWrI@6", 29: "15yDXFYyWrI@22", 30: "0ZQnzC6A0uY@700", 31: "AJT1x_bQXuA@300",
    # 25 esfera Golden Gate
    32: "LNfT31D87bU@200", 33: "Dx1logOoVng@30", 34: "ebTbiuCzvi8@20", 35: "5Gz91wrHNQo@5",
    # 24 ordenador CIA
    36: "5Gz91wrHNQo@20", 37: "IAG3kSCat30@10", 38: "nsRnpntScpU@30", 39: "SiqPRqYDj9A@20", 40: "nsRnpntScpU@120",
    # 23 libro Dr Disrespect
    41: ["Scorched Earth Modern Warfare 3 no commentary", "Modern Warfare 3 London mission no commentary"],
    42: "KmejVl0fshI@5", 43: "KmejVl0fshI@18",
    44: ["Modern Warfare 3 Scorched Earth London", "Modern Warfare 3 campaign Germany no commentary"],
    # 22 Shadowman
    45: "-nusN4tZYoo@20", 46: "-nusN4tZYoo@60", 47: "kdLqsWDl16c@30",
    48: ["Shadows of Evil ending cutscene", "Shadows of Evil Easter egg ending"],
    49: ["Shadows of Evil Easter egg no commentary", "Shadows of Evil gameplay no commentary"],
    50: ["Shadows of Evil boss fight Shadowman", "Shadows of Evil Easter egg boss"],
    51: ["Shadows of Evil ritual", "Shadows of Evil rituals no commentary"],
    # 21 aliens
    52: "lwSMdQzAiJ0@40", 53: "sXa-oeoNcKM@72", 54: "pjOonV9foZ4@10", 55: "DsUMbob0HsQ@30",
    # 20 Ghosts
    56: "l-c2ii3bov8@740", 57: "l-c2ii3bov8@754", 58: "AOGRZJ22z3w@2", 59: "yQ9w3RFhbCQ@5",
    60: ["Call of Duty Ghosts Riley dog", "Ghosts Riley dog gameplay"],
    # 19 Reznov
    61: "ottnH2JngbI@30", 62: "uPt2AXQAUjw@60", 63: "ottnH2JngbI@120", 64: "uPt2AXQAUjw@200", 65: "6lNatiH5lKI@10",
    # 18 IX
    66: "Vfh8jUFGkoI@120", 67: "GAM_EtjJzTE@10", 68: "-OCsYSM6biI@300",
    69: ["IX Easter egg shield zombies fire", "IX zombies Easter egg no commentary"], 70: "7bPc6Rx_UmA@20",
    # 17 calavera
    71: ["Black Ops 2 zombies Buried no commentary", "Black Ops 2 zombies gameplay no commentary"],
    72: "xGgkaG_0CoU@8", 73: "-47aOTzJiAs@20", 74: "xGgkaG_0CoU@29", 75: "tmT-zXmzHlw@30", 76: "-47aOTzJiAs@60",
    # 16 Alex
    77: "6YD1oPB-utQ@30", 78: "6YD1oPB-utQ@120", 79: "jkMLqRxDvIY@40", 80: "jkMLqRxDvIY@58", 81: "kRDoahkhW9k@30",
    # 15 Pawn Takes Pawn
    82: "TgQHWD2KYwY@5", 83: "TgQHWD2KYwY@40", 84: "TgQHWD2KYwY@80", 85: "zsBRGCabaog@20", 86: "zsBRGCabaog@60",
    # 14 Warzone filtrado
    87: "ibetHV_lbL0@10", 88: "0E44DClsX5Q@15", 89: "0E44DClsX5Q@45", 90: "0E44DClsX5Q@80", 91: "bdi2FNW9LJQ@30",
    # 13 búnker 11
    92: "A9d5vXOSo7w@40", 93: "-kZ0PTHeXGY@5", 94: "A9d5vXOSo7w@62", 95: "26pyGBkCYzk@60", 96: "o5RncmdurEY@30",
    # 12 Blundell Morse
    97: "dpv2bv_j49c@10", 98: "dpv2bv_j49c@40", 99: "dpv2bv_j49c@70", 100: "dpv2bv_j49c@100", 101: "TS701bMxmSI@30",
    # 11 Samantha
    102: "TS701bMxmSI@40", 103: "TS701bMxmSI@0", 104: "4BnV80YsWlw@22", 105: "ByYbMhri4Sg@30",
    106: ["Origins zombies Samantha cutscene", "Origins zombies ending cutscene"], 107: "AJT1x_bQXuA@600",
    # 10 cara de Alcatraz
    108: "fVfS9u-GhWg@0", 109: "AJT1x_bQXuA@1500", 110: "LNfT31D87bU@900", 111: "IvhI73INQRY@100",
    # 9 corazón
    112: "IvhI73INQRY@400", 113: "LqsPElwy8TA@30", 114: "LqsPElwy8TA@120", 115: "LqsPElwy8TA@200",
    116: "TPSPqrS0gG0@170", 117: "IvhI73INQRY@1200",
    # 8 Spectre
    118: "pCPsB4xdTZE@77", 119: "KksmTloMKuQ@20", 120: "KksmTloMKuQ@50",
    121: ["Black Ops 7 Spectre", "Black Ops 3 Spectre specialist gameplay"],
    # 7 Sanctuary
    122: ["Sanctuary Modern Warfare 3 gameplay", "Sanctuary MW3 multiplayer no commentary"], 123: "nfb8AVVpoXI@0",
    124: "nfb8AVVpoXI@30", 125: ["Davis Family Vacation Modern Warfare 3", "Modern Warfare 3 family video London"],
    126: ["Davis Family Vacation", "Sanctuary Modern Warfare 3 cemetery"],
    # 6 Ironclad
    127: ["Call of Duty 3 gameplay no commentary", "Call of Duty 3 campaign no commentary"],
    128: "4lCfOU8MgkA@362", 129: "4lCfOU8MgkA@400", 130: "4lCfOU8MgkA@440",
    131: ["Call of Duty 3 multiplayer Xbox 360", "Call of Duty 3 online multiplayer"],
    132: "4lCfOU8MgkA@540", 133: "4lCfOU8MgkA@560",
    # 5 fantasma de Vacant
    134: "eW2lZ_G4gww@30", 135: "eW2lZ_G4gww@58", 136: "eW2lZ_G4gww@110",
    137: ["Backlot Call of Duty 4 ghost", "Backlot Call of Duty 4 gameplay"], 138: "eW2lZ_G4gww@64",
    # 4 ADFGX
    139: ["Mob of the Dead no commentary", "Mob of the Dead gameplay"], 140: "uNfLuCMGPwk@5", 141: "uNfLuCMGPwk@20",
    142: "uNfLuCMGPwk@40", 143: "uNfLuCMGPwk@65",
    144: ["Origins zombies trailer", "Origins Black Ops 2 trailer"], 145: ["Origins giant robot", "Origins zombies robots"],
    # 3 Kennedy
    146: "k7YKGR8Ffs8@10", 147: "k7YKGR8Ffs8@40", 148: "z39GmaEIaGs@65", 149: "z39GmaEIaGs@72",
    150: ["Black Ops ending cutscene Mason", "Black Ops Revelations ending"],
    # 2 imposible
    151: "pYrtpmyROzA@60", 152: "cEkYK1hkQcA@10", 153: "pYrtpmyROzA@400", 154: "IvhI73INQRY@2000",
    155: "pYrtpmyROzA@900", 156: "IvhI73INQRY@2600", 157: "pYrtpmyROzA@1300",
    # 1 hombre de traje
    158: ["Modern Warfare 3 ending Price kills Makarov", "Modern Warfare 3 Dust to Dust ending"],
    159: ["Modern Warfare 3 Dust to Dust no commentary", "Dust to Dust Modern Warfare 3"],
    160: "De7Axarv12E@5", 161: "De7Axarv12E@15", 162: "De7Axarv12E@25", 163: "De7Axarv12E@35", 164: "De7Axarv12E@42",
    # cierre
    165: "IvhI73INQRY@3200", 166: "pYrtpmyROzA@1800",
    167: ["Advanced Warfare funeral press F", "Advanced Warfare Atlas funeral"], 168: "0E44DClsX5Q@100", 169: "6YD1oPB-utQ@300",
}

# 10-nov: los fijos de < 720p fallan («Requested format is not available»): pasan a búsqueda
VAC = ["Vacant ghost Call of Duty 4", "Vacant Call of Duty 4 gameplay"]
B.update({3: "4BnV80YsWlw@26", 4: VAC, 134: ["Call of Duty 4 Vacant no commentary", "Vacant Call of Duty 4"], 135: VAC, 136: VAC,
          138: ["Vacant Call of Duty 4 multiplayer", "Call of Duty 4 Vacant"],
          28: ["Kino der Toten portraits", "Kino der Toten no commentary"], 29: ["Kino der Toten painting", "Kino der Toten gameplay"],
          39: ["Zork Black Ops", "Black Ops terminal Zork"], 53: ["Hangar 18 Black Ops", "Hangar 18 Annihilation gameplay"],
          55: ["Hangar 18 Annihilation gameplay", "Black Ops Hangar 18 multiplayer"]})
# 10-nov, revisión del mosaico: negros, logos de youtuber, webcam, ESRB, tienda, streamer → otro tramo/fuente
B.update({1: "LNfT31D87bU@400", 3: "whdUjvEIAVI@15", 18: "GkT73ylsTzQ@300", 40: "nsRnpntScpU@60",
          49: ["Shadows of Evil gameplay no commentary", "Shadows of Evil zombies gameplay"], 58: "AOGRZJ22z3w@12",
          86: "zsBRGCabaog@100", 95: "A9d5vXOSo7w@120", 96: "dpv2bv_j49c@25", 102: "whdUjvEIAVI@40", 103: "whdUjvEIAVI@4",
          104: "4BnV80YsWlw@28", 105: "whdUjvEIAVI@60", 128: ["Call of Duty 3 campaign no commentary", "Call of Duty 3 gameplay"],
          150: ["Black Ops Revelations ending", "Black Ops campaign ending"], 152: "pYrtpmyROzA@200", 156: "IvhI73INQRY@1500",
          165: "IvhI73INQRY@700", 168: "0E44DClsX5Q@70"})
B.update({104: "whdUjvEIAVI@80", 86: ["Black Ops Cold War reveal trailer", "Black Ops Cold War Know Your History"],
          128: ["Call of Duty 3 Xbox 360 gameplay", "Call of Duty 3 mission gameplay"]})
B.update({93: "bdi2FNW9LJQ@120", 123: "wisDIYbk-8E@60", 124: "wisDIYbk-8E@120"})   # MASTER 1: texto de youtuber encima
out = {}
for n in range(1, 170):
    v = B[n]
    if isinstance(v, str):
        vid, s = v.split("@")
        out[f"scene-{n:03d}"] = {"url": "https://youtu.be/" + vid, "desde": float(s)}
    else:
        out[f"scene-{n:03d}"] = v
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "busquedas.json")
json.dump(out, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "beats")
