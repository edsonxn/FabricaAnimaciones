# -*- coding: utf-8 -*-
"""Escribe busquedas.json de cod_mandela2 (13-nov-2026) desde investigacion.md. «id@s» = url + desde; lista = búsquedas.
Sonidos nombrados sincronizados con el clip (ancla de la voz − t0 del beat): Gaz 1:12, Frank 15:37, SDC 0:18, botella 0:17, M1911 0:11.
Violencia (p02): Weaver y Pyle SIN el impacto (Semper Fi termina antes de 0:54; Weaver solo gameplay de Baikonur).
"""
import json
import os

NAC = ["Nacht der Untoten sniper cabinet Kar98k", "Nacht der Untoten World at War no commentary"]
KINO = ["Kino der Toten no commentary", "Kino der Toten gameplay Black Ops"]
MOON = ["Moon zombies biodome gravity lift", "Moon zombies Black Ops no commentary"]
MOTD = ["Mob of the Dead no commentary", "Mob of the Dead gameplay Black Ops 2"]
RAID = ["Raid Black Ops 2 multiplayer no commentary", "Raid Black Ops 2 gameplay"]
COD2 = ["Call of Duty 2 campaign no commentary", "Call of Duty 2 PC gameplay no commentary"]
PERROS = ["World at War attack dogs multiplayer", "World at War dogs killstreak multiplayer gameplay"]
BO1C = ["Black Ops Operation 40 no commentary", "Call of Duty Black Ops campaign Cuba no commentary"]
WAR = ["Call of Duty 4 No Fighting in the War Room no commentary", "No Fighting in the War Room Call of Duty 4"]
B = {
    # intro
    1: "vi6fek6qXfc@0", 2: "GOdXbhvMHQM@600", 3: "GO9HJR8HBXM@36", 4: "KPec3-6zo3k@67.1", 5: "2HvBkXZOCTc@60", 6: KINO,
    # 20 bomba
    7: "kvGwFk-A5ec@60", 8: "kvGwFk-A5ec@200", 9: "kvGwFk-A5ec@700", 10: WAR, 11: WAR,
    # 19 Intervention
    12: "99bRlIwtScA@30", 13: "99bRlIwtScA@120", 14: "KleJ6myTiQY@60", 15: "99bRlIwtScA@250",
    # 18 Richtofen
    16: "pQ1di7a8G7Q@0", 17: "pQ1di7a8G7Q@10", 18: "QdFmT4HIvss@0", 19: "_IYBL_shsw0@0",
    # 17 Nuketown
    20: "NR43kzj7Ngg@60", 21: ["Nuketown 2025 yellow house grass rolled", "Nuketown 2025 easter egg grass"],
    22: ["Nuketown 2025 fake grass", "Nuketown 2025 Black Ops 2 map tour"], 23: "h18qJ7LeuHs@200",
    # 16 Double Tap
    24: "7wtczLVQfxo@60", 25: "zl9mj7bZ7Jg@40", 26: "zl9mj7bZ7Jg@80",
    27: ["Ascension Zombies Chronicles Der Wunderfizz", "Ascension Black Ops 3 Zombies Chronicles gameplay"],
    # 15 Downhill
    28: "ED2IcuD7w4E@30", 29: "aBWzaMDvJjE@100", 30: "XT0pdJA6vUo@120",
    # 14 cámara Pack-a-Punch
    31: ["Kino der Toten pack a punch no commentary", "Kino der Toten pack a punch"], 32: "jtMSvvvBlmg@0", 33: "jtMSvvvBlmg@20",
    34: ["Black Ops Zombies iOS Kino der Toten", "Kino der Toten iPhone gameplay"],
    # 13 granada CoD 2
    35: COD2, 36: ["Call of Duty 2 Normandy no commentary", "Call of Duty 2 Pointe du Hoc"],
    37: ["Call of Duty 2 North Africa no commentary", "Call of Duty 2 El Alamein mission"], 38: COD2,
    # 12 perros
    39: PERROS, 40: PERROS, 41: ["World at War multiplayer Japanese announcer", "World at War multiplayer Makin gameplay"],
    # 11 armario
    42: NAC, 43: "ADqtCsaKyZI@0", 44: "uji4Jme6L_w@0", 45: ["Nacht der Untoten mystery box", "Nacht der Untoten gameplay"],
    46: NAC, 47: "ADqtCsaKyZI@10",
    # 10 Lullaby
    48: KINO, 49: ["Verruckt World at War zombies no commentary", "Verruckt zombies gameplay"], 50: "s10TSmCOWRs@0",
    51: "s10TSmCOWRs@4", 52: ["Kino der Toten 115 song easter egg", "Kino der Toten music easter egg"],
    # 9 Wunderwaffe
    53: "nlc0NHbaCnE@0", 54: ["Wunderwaffe Der Riese no commentary", "Wunderwaffe DG-2 Der Riese"], 55: "nlc0NHbaCnE@15",
    56: ["Der Riese World at War zombies no commentary", "Der Riese zombies gameplay"],
    # 8 Andrés
    57: BO1C, 58: BO1C, 59: ["Black Ops Vorkuta no commentary", "Black Ops campaign Vorkuta"],
    60: ["Black Ops Redemption mission no commentary", "Black Ops campaign final mission"], 61: "vi6fek6qXfc@4.7",
    62: ["Black Ops Victor Charlie no commentary", "Black Ops campaign Vietnam no commentary"],
    # 7 Mason y Woods
    63: "YH-rYeB_EmA@900", 64: "FVMb6ZRRu3g@918", 65: "FVMb6ZRRu3g@933.5", 66: "FVMb6ZRRu3g@942", 67: "YH-rYeB_EmA@1000",
    68: MOON,
    # 6 Moon
    69: MOON, 70: ["Moon zombies jump pads power up", "Moon biodome gravity lift"], 71: ["Moon zombies power ups biodome", "Moon zombies gameplay"],
    72: "GO9HJR8HBXM@38", 73: "4c1QwLdPNmI@4", 74: "4c1QwLdPNmI@13.3", 75: MOON,
    # 5 M1911
    76: MOTD, 77: ["Mob of the Dead Brutus", "Mob of the Dead gameplay no commentary"], 78: "nmSZcQlGBLo@9.8", 79: "IyqwPv5rpB4@60",
    # 4 Hoover
    80: RAID, 81: RAID, 82: "kvITNVFDsCQ@0", 83: "DquIYdceE9o@17.3", 84: "kvITNVFDsCQ@60", 85: RAID,
    # subs
    86: ["Black Ops 2 multiplayer Hijacked no commentary", "Black Ops 2 multiplayer gameplay"],
    87: ["Farm zombies Black Ops 2 no commentary", "Farm survival Black Ops 2"],
    # 3 AUG
    88: "GOdXbhvMHQM@300", 89: "GOdXbhvMHQM@900", 90: ["Farm zombies mystery box Black Ops 2", "Farm survival mystery box"],
    91: "s1If3v9tNvI@0", 92: "p8TwUmdWvAY@40", 93: ["MTAR Farm zombies Black Ops 2", "MTAR zombies Black Ops 2"],
    94: ["Black Ops Executive Order no commentary", "Black Ops Executive Order Baikonur"],
    # 2 Weaver (sin el impacto)
    95: ["Black Ops Executive Order Baikonur no commentary", "Black Ops Executive Order mission"],
    96: "borJbVNUquc@40", 97: "borJbVNUquc@45.5", 98: ["World at War Semper Fi no commentary", "World at War Makin mission"],
    # 1 Gaz
    99: "KPec3-6zo3k@30", 100: "KPec3-6zo3k@66", 101: "2HvBkXZOCTc@105", 102: "KPec3-6zo3k@74", 103: "KPec3-6zo3k@77",
    # cierre
    104: ["Moon zombies ending cutscene", "Moon easter egg ending"], 105: ["Pawn Takes Pawn Black Ops Cold War ARG", "Pawn Takes Pawn"],
    106: "NXC9Tm55AC8@100", 107: "2HvBkXZOCTc@300", 108: KINO,
}
# 13-nov (sesión 2): < 720p → ventana de archivo (_archivo.py: b1, b19, b53, b55, b61, b73, b74); el resto, otra fuente
B.update({43: ["Nacht der Untoten upstairs sniper cabinet", "Nacht der Untoten sniper cabinet Kar98k"], 47: "uji4Jme6L_w@60",
          50: "Yy1TxvS3O8E@20", 51: "Yy1TxvS3O8E@24", 88: "GOdXbhvMHQM@320", 102: "KPec3-6zo3k@75"})
# 13-nov, revisión del mosaico: explosión, logos/marcas de youtuber, texto quemado, otro mapa → otra fuente
B.update({9: ["Call of Duty 4 Shock and Awe nuke explosion Jackson death", "Shock and Awe nuke explosion Call of Duty 4 original"],
          19: ["Richtofen third person Black Ops zombies cutscene", "Ascension intro cutscene Black Ops zombies"],
          21: ["Nuketown 2025 Black Ops 2 map flyover", "Nuketown 2025 gameplay Black Ops 2 Xbox"],
          24: ["Ascension zombies 2010 gameplay", "Ascension Black Ops zombies round gameplay"],
          25: ["Ascension zombies monkeys gameplay", "Ascension space monkeys round"],
          26: ["Ascension zombies Stamin-Up PhD Flopper machine", "Ascension zombies lunar lander"],
          31: ["Kino der Toten pack a punch projector room", "Kino der Toten teleporter projector room"],
          32: ["Kino der Toten pack a punch camera TV projector", "Kino der Toten projector room TV screens"],
          33: ["Kino der Toten pack a punch gameplay 2010", "Kino der Toten round gameplay PS3"],
          35: ["Call of Duty 2 Pointe du Hoc no commentary", "Call of Duty 2 Brecourt mission"], 44: "uji4Jme6L_w@120",
          60: ["Black Ops Redemption Rebirth Island no commentary", "Black Ops campaign Rebirth no commentary"],
          70: ["Moon zombies Black Ops biodome gameplay 2011", "Moon zombies Rezurrection gameplay"],
          71: ["Moon zombies Area 51 jump pad", "Moon zombies Black Ops PS3 gameplay"],
          77: ["Mob of the Dead Brutus gameplay no commentary", "Mob of the Dead Alcatraz gameplay round"],
          79: ["Mob of the Dead mystery box gameplay", "Mob of the Dead cell block gameplay"],
          81: ["Raid Black Ops 2 search and destroy gameplay", "Raid Black Ops 2 domination gameplay"],
          82: ["Black Ops 2 multiplayer Raid team deathmatch", "Raid map Black Ops 2 no commentary"],
          84: ["Black Ops 2 Raid multiplayer PS3", "Raid Black Ops 2 kill confirmed"], 90: "GOdXbhvMHQM@1500"})
B.update({19: "AFaBFKUl51E@600", 21: "ZPwNjArOjRo@200", 24: "tKRfEHuEK1s@300", 25: "tKRfEHuEK1s@700", 26: "tKRfEHuEK1s@1100",
          79: "G1Y25vq1dNY@60", 82: "4kBjEId5Shw@200"})   # 2.ª revisión
B.update({38: "VHTC7llKOAw@1200", 51: ["Verruckt Zombies Chronicles gameplay no commentary", "Verruckt World at War zombies round gameplay"]})   # texto ajeno (OCR)
B.update({38: "VHTC7llKOAw@900", 18: ["Moon intro cutscene Black Ops 1 Richtofen", "Black Ops Moon opening cinematic zombies"]})   # 38 roto; 18 era BO6
B.update({18: "pQ1di7a8G7Q@19"})   # cómic de Ultimis (Kino, BO1); el clip de «Richtofen» era de BO6
B.update({80: "4kBjEId5Shw@120", 81: "4kBjEId5Shw@300", 96: "J1uvoIC5zIs@400"})   # hoja fx: menú / Slums / negro
out = {}
for n in range(1, 109):
    v = B[n]
    if isinstance(v, str):
        vid, s = v.split("@")
        out[f"scene-{n:03d}"] = {"url": "https://youtu.be/" + vid, "desde": float(s)}
    else:
        out[f"scene-{n:03d}"] = v
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "busquedas.json")
json.dump(out, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "beats")
