# -*- coding: utf-8 -*-
"""Escribe busquedas.json por rangos de beats (pools rotados para variar el plano entre beats seguidos)."""
import json

R = [
    ((1, 3), ["Wolfskull Cave Skyrim no commentary", "Wolfskull Cave ritual Potema", "Skyrim necromancer ritual cave"]),
    ((4, 4), ["Potema boss fight Skyrim", "Wolf Queen Awakened Potema fight"]),
    ((5, 7), ["Potema's Catacombs Skyrim", "Skyrim Solitude catacombs walkthrough", "Skyrim draugr crypt no commentary"]),
    ((8, 9), ["Styrr Hall of the Dead Solitude", "Solitude Hall of the Dead Skyrim"]),
    ((10, 11), ["Solitude Skyrim no commentary 4K", "Blue Palace Solitude Skyrim", "Solitude arch Skyrim"]),
    ((12, 16), ["Skyrim werewolf transformation night", "Skyrim werewolf hunt no commentary", "Skyrim soul trap soul gem",
                "Skyrim Breton town night", "Skyrim werewolf vs mage"]),
    ((17, 18), ["Oblivion Imperial Palace no commentary", "White-Gold Tower Oblivion", "Oblivion Imperial City 4K"]),
    ((19, 23), ["Oblivion Imperial City no commentary", "Skyrim lockpicking no commentary", "Arcane University Oblivion",
                "Oblivion lockpicking", "Skyrim khajiit caravan", "Oblivion Imperial Palace throne room"]),
    ((24, 30), ["Oblivion Imperial City rain", "Skyrim sneaking castle no commentary", "Oblivion Elder Council chamber",
                "Skyrim Arcanaeum library", "Skyrim Elder Scroll reading", "Oblivion Imperial Palace library"]),
    ((31, 34), ["Skyrim wedding Temple of Mara", "Blue Palace throne room Skyrim", "Solitude Skyrim no commentary 4K",
                "Skyrim Solitude streets"]),
    ((35, 52), ["Blue Palace Solitude interior", "Solitude Skyrim no commentary 4K", "Skyrim Solitude streets night",
                "Skyrim Solitude docks", "Skyrim Solitude market", "Skyrim nord noble court", "Skyrim healer temple",
                "Skyrim archers battle no commentary", "Skyrim Solitude castle Dour", "Skyrim Solitude snow walk"]),
    ((53, 58), ["Skyrim scenic no commentary 4K", "Skyrim ambience Solitude coast", "Skyrim relaxing walk 4K"]),
    ((59, 76), ["Oblivion Imperial City night", "Oblivion Temple of the One", "White-Gold Tower Oblivion",
                "Oblivion Imperial Palace no commentary", "Skyrim sneak no commentary", "Skyrim illusion spell calm",
                "Oblivion Ruby Throne", "Oblivion Elder Council chamber", "Oblivion Imperial City 4K",
                "Skyrim Blue Palace Elisif throne"]),
    ((77, 91), ["Oblivion Imperial City no commentary", "Skyrim Solitude docks ship", "Skyrim ship sailing sea",
                "Skyrim Psijic Quaranir", "Skyrim sea storm", "Blue Palace Solitude interior", "Skyrim ocean coast ice",
                "Skyrim Solitude arch view"]),
    ((92, 95), ["Skyrim inn night ambience", "Skyrim campfire night no commentary", "Skyrim sleeping bed inn"]),
    ((96, 117), ["Oblivion Imperial Palace rain", "Oblivion Elder Council chamber", "Oblivion Imperial City 4K",
                 "Skyrim castle tower no commentary", "Skyrim Reach mountains no commentary", "Skyrim ambush mountain pass",
                 "Markarth Skyrim no commentary", "Skyrim prison cell", "Skyrim dungeon prison no commentary",
                 "Skyrim snow mountains 4K"]),
    ((118, 137), ["Skyrim Civil War battle", "Battle for Whiterun Skyrim", "Skyrim army march", "Oblivion Ruby Throne",
                  "Skyrim marsh Hjaalmarch no commentary", "Skyrim fireball battle", "Skyrim argonian", "Skyrim horse riding 4K",
                  "Skyrim tundra sunrise", "Skyrim dragon burning village", "Skyrim legion vs stormcloak battle"]),
    ((138, 144), ["Skyrim scenic no commentary 4K", "Skyrim relaxing walk 4K", "Skyrim ambience Riverwood"]),
    ((145, 146), ["Miraak Hermaeus Mora ending", "Dragonborn ending Hermaeus Mora"]),
    ((147, 149), ["Skyrim scenic no commentary 4K", "Skyrim Solitude snow walk"]),
    ((150, 175), ["Battle for Solitude Skyrim", "Skyrim siege Solitude Civil War", "Skyrim necromancer raising dead",
                  "Skyrim draugr horde", "Skyrim vampire lord", "Wolfskull Cave Skyrim no commentary", "College of Winterhold no commentary",
                  "Skyrim enchanting table", "Skyrim soul gem", "Skyrim tunnel cave no commentary", "Skyrim necromancer lair",
                  "Blue Palace Solitude interior"]),
    ((176, 201), ["Pelagius Wing Blue Palace", "Blue Palace Solitude interior", "Skyrim nightmare dream", "Skyrim argonian",
                  "Skyrim banquet hall feast", "Skyrim bard music Solitude", "Oblivion Imperial Palace no commentary",
                  "Skyrim Solitude streets night", "Skyrim haunted wing", "Oblivion Ruby Throne"]),
    ((202, 203), ["Skyrim Solitude no commentary 4K", "Skyrim level up perks"]),
    ((204, 213), ["The Man Who Cried Wolf Skyrim", "Wolfskull Cave Skyrim no commentary", "Falk Firebeard Skyrim",
                  "Wolfskull Cave ritual Potema", "Skyrim necromancer ritual cave"]),
    ((214, 225), ["Wolf Queen Awakened Skyrim", "Potema's Catacombs Skyrim", "Styrr Hall of the Dead Solitude",
                  "Potema boss fight Skyrim", "Skyrim oil trap"]),
    ((226, 238), ["Pelagius Wing Blue Palace", "The Mind of Madness Skyrim", "Sheogorath Pelagius tea", "Wabbajack Skyrim",
                  "Mind of Madness confidence anger", "Mind of Madness night terrors"]),
    ((239, 244), ["Solitude Skyrim sunset", "Wolfskull Cave Skyrim no commentary", "Skyrim Solitude arch view", "Potema's Catacombs Skyrim"]),
]

d = {}
for (a, b), pool in R:
    for i, n in enumerate(range(a, b + 1)):
        k = i % len(pool)
        d[f"scene-{n:03d}"] = pool[k:] + pool[:k]
falta = [f"scene-{n:03d}" for n in range(1, 245) if f"scene-{n:03d}" not in d]
assert not falta, falta
json.dump(d, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(d), "busquedas")
