# -*- coding: utf-8 -*-
"""Escribe busquedas.json de cod_villanos (17-nov-2026). «id@s» = url + desde; lista = búsquedas.
CITAS AUDIBLES (silencio de la voz − t0 del beat; tiempos medidos con faster-whisper, palabra por palabra):
  12 Safehouse «Sir, it's his cell phone» 354.0 (teléfono antes) · 31 Irons «What are you doing? I gave you that arm» 197.1 ·
  44 Hassan «We're not attacking… We are invading» 41.5-46.3 · 86 Mason «…kill my own president!» + Dragovich «Tried?» 41.5 ·
  97 Menéndez «Martyr me… for Cordis Die» 45.4-48.9 · 104 Mason «My name is Viktor Reznov!» 102.1-104.5 · 115 «Where is he now? / Off the list» 228.3-231.9
VIOLENCIA: cada clip termina ANTES del disparo/golpe; lo que pase del silencio se tapa con `vid()` en efectos.py.
"""
import json
import os

AMSEL = ["World at War Vendetta mission no commentary", "Call of Duty World at War Vendetta Stalingrad sniper"]
COUP = ["Call of Duty 4 The Coup opening no commentary", "Call of Duty 4 Remastered The Coup"]
ALASAD = ["Call of Duty 4 Safehouse mission no commentary", "Call of Duty 4 Remastered Safehouse Al-Asad"]
NUKE = ["Call of Duty 4 Shock and Awe nuke no commentary", "Call of Duty 4 Remastered Shock and Awe"]
VICTOR = ["Call of Duty 4 Sins of the Father no commentary", "Call of Duty 4 Remastered Sins of the Father Victor Zakhaev"]
WOLF = ["Modern Warfare 2019 The Wolf's Den no commentary", "Call of Duty Modern Warfare 2019 Wolf's Den mission"]
BARKOV = ["Modern Warfare 2019 Into the Furnace no commentary", "Call of Duty Modern Warfare 2019 Into the Furnace Barkov helicopter"]
IRONS = ["Advanced Warfare Terminus mission no commentary", "Call of Duty Advanced Warfare final mission Irons"]
KOTCH = ["Infinite Warfare Operation Black Flag no commentary", "Infinite Warfare Black Flag Kotch Olympus Mons"]
HASSAN = ["Modern Warfare 2 2022 Countdown mission no commentary", "MW2 2022 Countdown Chicago tower"]
RORKE = ["Call of Duty Ghosts The Ghost Killer no commentary", "Call of Duty Ghosts final mission train Rorke"]
RICHT = ["Tag der Toten ending cutscene", "Black Ops 4 Tag der Toten final cutscene campfire"]
GIANT = ["The Giant Black Ops 3 intro cutscene", "The Giant zombies intro cinematic Richtofen"]
PERSEUS = ["Black Ops Cold War ending Perseus", "Black Ops Cold War Ashes to Ashes ending"]
STITCH = ["Cold War Season 6 cinematic Adler Stitch", "Warzone season 6 cutscene Perseus grave"]
HARROW = ["Black Ops 6 Checkmate final mission no commentary", "Black Ops 6 ending Harrow Case"]
KRAV1 = ["Black Ops Payback mission no commentary", "Black Ops Payback Kravchenko Woods window"]
KRAV2 = ["Black Ops 2 Old Wounds no commentary", "Black Ops 2 Old Wounds Kravchenko interrogation"]
GRAVES1 = ["Modern Warfare 2 2022 Ghost Team mission no commentary", "MW2 2022 Ghost Team Graves tank"]
GRAVES4 = ["Modern Warfare 4 Hired Gun mission no commentary", "Modern Warfare 4 Hired Gun Graves"]
OSOK = ["Call of Duty 4 One Shot One Kill no commentary", "Call of Duty 4 Remastered One Shot One Kill Zakhaev"]
GAMEOVER = ["Call of Duty 4 Game Over mission no commentary", "Call of Duty 4 Remastered Game Over bridge"]
DRAGO = ["Black Ops Redemption mission no commentary", "Black Ops Executive Order Baikonur limousine"]
SHEP = ["Modern Warfare 2 Endgame mission no commentary", "Modern Warfare 2 Remastered Endgame boat chase"]
SHEP23 = ["Modern Warfare 3 2023 Trojan Horse Shepherd", "MW3 2023 ending Shepherd Price office"]
MEN = ["Black Ops 2 Judgment Day no commentary", "Black Ops 2 Judgment Day Menendez"]
MEN_F = ["Black Ops 2 Menendez ending prison TV", "Black Ops 2 bad ending Menendez grave"]
REB = ["Black Ops Rebirth mission no commentary", "Black Ops Rebirth Island Steiner"]
VORKUTA = ["Black Ops Vorkuta mission no commentary", "Black Ops Vorkuta escape Reznov"]
DUST = ["Modern Warfare 3 Dust to Dust no commentary", "Modern Warfare 3 Dust to Dust ending Makarov"]
MW23 = ["Modern Warfare 3 2023 campaign Makarov no commentary", "MW3 2023 Makarov train mission"]
COLD = ["Modern Warfare 4 Out in the Cold no commentary", "Modern Warfare 4 Out in the Cold Makarov chase"]
MW4 = ["Modern Warfare 4 campaign no commentary", "Call of Duty Modern Warfare 4 gameplay"]

B = {
    # intro
    1: GAMEOVER, 2: COLD, 3: RORKE, 4: "7p22Hx9w2l4@15", 5: DUST,
    # 20 Amsel
    6: AMSEL, 7: AMSEL, 8: AMSEL, 9: AMSEL,
    # 19 Al-Asad
    10: COUP, 11: "Gt1JeMK50us@345.6", 12: "Gt1JeMK50us@350", 13: ALASAD, 14: NUKE,
    # 18 Victor
    15: VICTOR, 16: VICTOR, 17: VICTOR, 18: VICTOR,
    # 17 Lobo
    19: WOLF, 20: WOLF, 21: WOLF, 22: WOLF, 23: BARKOV,
    # 16 Barkov
    24: BARKOV, 25: BARKOV, 26: BARKOV, 27: BARKOV,
    # 15 Irons
    28: IRONS, 29: IRONS, 30: "9KLWbfLfcgM@180", 31: "9KLWbfLfcgM@196.1", 32: IRONS, 33: IRONS, 34: IRONS,
    # 14 Kotch
    35: KOTCH, 36: KOTCH, 37: KOTCH, 38: KOTCH, 39: KOTCH, 40: KOTCH, 41: KOTCH,
    # 13 Hassan
    42: HASSAN, 43: "wuEQmpxSD88@15", 44: "wuEQmpxSD88@40.7", 45: HASSAN, 46: HASSAN,
    # 12 Rorke
    47: RORKE, 48: RORKE, 49: RORKE, 50: RORKE, 51: RORKE,
    # 11 Richtofen
    52: GIANT, 53: GIANT, 54: RICHT, 55: RICHT,
    # 10 Perseus
    56: PERSEUS, 57: PERSEUS, 58: PERSEUS, 59: STITCH, 60: STITCH, 61: HARROW,
    # 9 Harrow
    62: HARROW, 63: "CkmHVSUGGe8@92", 64: HARROW, 65: HARROW, 66: KRAV1,
    # 8 Kravchenko
    67: KRAV1, 68: KRAV1, 69: KRAV2, 70: KRAV2, 71: KRAV2,
    # 7 Graves
    72: GRAVES1, 73: GRAVES1, 74: GRAVES1, 75: GRAVES4, 76: GRAVES4, 77: OSOK,
    # 6 Zakhaev
    78: OSOK, 79: "DLW7BBSknCQ@100", 80: GAMEOVER, 81: GAMEOVER, 82: GAMEOVER,
    # 5 Dragovich
    83: DRAGO, 84: ["Black Ops Executive Order limousine explosion", "Black Ops Executive Order no commentary"], 85: DRAGO,
    86: "STtBhug8JQ4@34.6", 87: DRAGO,
    # 4 Shepherd
    88: SHEP, 89: ["Modern Warfare 2 Loose Ends Shepherd betrayal", "Modern Warfare 2 Loose Ends no commentary"], 90: "SJqxbUNvuNo@262", 91: SHEP,
    92: SHEP, 93: SHEP23,
    # suscripción
    94: MW4, 95: MEN,
    # 3 Menéndez
    96: MEN, 97: "hIFud6Oeg-Y@41.7", 98: MEN_F, 99: MEN_F, 100: MEN_F, 101: REB,
    # 2 Steiner
    102: REB, 103: "7p22Hx9w2l4@40", 104: "RMSiCLsstS0@97.1", 105: VORKUTA, 106: REB, 107: REB, 108: REB,
    # 1 Makarov
    # 112 = seJxZFES8BU 702.9-712.5 recortado abajo (sin el cuerpo colgado), hecho a mano con ffmpeg
    109: DUST, 110: DUST, 111: "seJxZFES8BU@630.1", 112: DUST, 113: MW23, 114: COLD, 115: "UnCOKMJvpfo@223.9", 116: COLD,
    # cierre
    117: MW4, 118: ["Modern Warfare 3 2011 ending credits", "Modern Warfare 3 Dust to Dust Price cigar"], 119: MW4, 120: COLD,
    121: GAMEOVER, 122: MW4,
}
out = {}
for n in range(1, 123):
    v = B[n]
    if isinstance(v, str):
        vid, s = v.split("@")
        out[f"scene-{n:03d}"] = {"url": "https://youtu.be/" + vid, "desde": float(s)}
    else:
        out[f"scene-{n:03d}"] = v
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "busquedas.json")
json.dump(out, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "beats")
