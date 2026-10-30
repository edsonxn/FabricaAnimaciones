# -*- coding: utf-8 -*-
"""Vuelta 2 de clips (30-oct): 44 de 121 rechazados en las hojas (menús, mapa, youtuber, Elden Ring, logos, negro al inicio)."""
import json

G = "Skyrim 4k no HUD"
B = {3: "Riften 4k no HUD walk", 4: "Skyrim cinematic landscape no HUD", 7: "Fort Dunstad walkthrough no commentary", 9: "Soul Cairn walk no commentary",
     10: "Skyrim running forest no HUD", 12: "Castle Volkihar exterior no HUD", 13: "Volkihar undercroft no commentary", 16: "Skyrim werewolf transformation no HUD",
     18: "Winterhold snow no HUD", 19: "Whiterun Hall of the Dead no commentary", 20: "Skyrim temple shrine no HUD", 23: "Skyrim giant mammoth no HUD",
     27: "Skyrim power attack slow motion no HUD", 31: "Riften walk no commentary", 32: "Skyrim warhammer kill no HUD", 36: "Skyrim Winterhold shore no HUD",
     37: "Skyrim underwater shipwreck", 38: "Skyrim follower dungeon no HUD", 39: "Skyrim Lydia adventure no commentary", 42: "Solitude dungeon no commentary",
     46: "Solstheim Thirsk riekling no commentary", 47: "Heljarchen Hall no HUD", 52: "Skyrim sun eclipse no HUD", 56: "Telvanni tower Solstheim no commentary",
     57: "Solstheim ash no HUD", 58: "Raven Rock no HUD", 68: "Winterhold Arcanaeum books no commentary", 72: "Skyrim Windhelm walk no HUD",
     73: "Paarthurnax Throat World no commentary", 74: "Greybeards Throat World no commentary", 75: "Forgotten Vale walk no commentary", 76: "Falmer snow elf no commentary",
     79: "Alduin defeat Sovngarde no commentary", 80: "Falkreath walk no HUD", 87: "Frostflow Lighthouse Habd no commentary", 89: "Chaurus Reaper Frostflow no commentary",
     91: "Greybeards Way of the Voice no commentary", 94: "Riften Ratway Esbern no commentary", 97: "Windhelm no HUD walk", 107: "Dark Brotherhood sanctuary Astrid no commentary",
     111: "Night Mother coffin no commentary", 112: "Cicero Dawnstar sanctuary no commentary", 117: "Paarthurnax Esbern Delphine no commentary", 118: "Skyrim dragon battle no HUD"}
p = "videos/tes_secretos_40/busquedas.json"
d = json.load(open(p, encoding="utf-8"))
for k, q in B.items():
    d[f"scene-{k:03d}"] = [q, G]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(",".join(str(k) for k in B))
