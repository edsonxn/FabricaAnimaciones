# -*- coding: utf-8 -*-
"""Escribe busquedas.json de «Las 10 builds más ROTAS de Skyrim» (s1, 10-nov-2026): 123 beats, búsquedas en inglés de 2-5
palabras con lo que la voz describe en ese segundo (regla «lo que dice la voz SE VE») + respaldo genérico de Skyrim."""
import json
import os

G = "Skyrim gameplay no commentary"


def q(*s):
    return list(s) + [G]


B = {
 # gancho
 1: q("Skyrim stealth archer one shot dragon", "Skyrim sneak attack dragon kill"), 2: q("Skyrim necromancer undead army"),
 3: q("Skyrim fortify restoration loop glitch"), 4: q("Skyrim character creation races"),
 5: q("Skyrim build guide gameplay"), 6: q("Skyrim alchemy potion 1000000 percent"),
 # 10 arquero
 7: q("Skyrim stealth archer sneak attack 3x"), 8: q("Skyrim Wood Elf character creation"),
 9: q("Skyrim Guardian Stones Thief Stone"), 10: q("Skyrim Archery perk tree Overdraw"),
 11: q("Skyrim Steady Hand slow motion zoom bow"), 12: q("Skyrim Dragonbone Bow"),
 13: q("Skyrim Slow Time shout"), 14: q("Skyrim Slow Time shout bow arrows"),
 15: q("Skyrim The Gold Ribbon of Merit book"), 16: q("Skyrim arrow valley archer shot"),
 17: q("Skyrim stealth archer headshot bandit"),
 # 9 carterista
 18: q("Skyrim reverse pickpocket poison"), 19: q("Skyrim Shadow Stone Riften"),
 20: q("Skyrim Poisoned perk pickpocket"), 21: q("Skyrim reverse pickpocket no bounty"),
 22: q("Skyrim reverse pickpocket poison guard dies"), 23: q("Skyrim Perfect Touch steal equipped armor"),
 24: q("Skyrim pickpocket armor bandit naked"), 25: q("Skyrim Astrid Dark Brotherhood shack"),
 # correo
 26: q("Skyrim courier letter"), 27: q("Skyrim tavern bard no HUD"), 28: q("Skyrim Whiterun no HUD"),
 29: q("Skyrim pause menu"),
 # 8 titiritero
 30: q("Skyrim Mayhem spell bandits fight each other"), 31: q("Skyrim High Elf Apprentice Stone"),
 32: q("Skyrim Apprentice Stone loading screen"), 33: q("Skyrim magicka regeneration"),
 34: q("Skyrim Illusion perk tree"), 35: q("Skyrim Master of the Mind dwarven centurion frenzy"),
 36: q("Skyrim Drevis Neloren College of Winterhold"), 37: q("Skyrim Mayhem spell dungeon"),
 38: q("Skyrim pacifist illusion build Mayhem"), 39: q("Skyrim Vampire Lord transformation"),
 # 7 vampiro
 40: q("Skyrim Harkon Castle Volkihar gift"), 41: q("Skyrim Vampire Lord stats"),
 42: q("Skyrim Vampiric Grip cliff"), 43: q("Skyrim Vampire Lord Mist Form"),
 44: q("Skyrim Serana Vampire Lord"), 45: q("Skyrim Serana follower"), 46: q("Skyrim Serana coffin"),
 47: q("Skyrim Harkon Vampire Lord"), 48: q("Skyrim necromancer build undead army"),
 # 6 nigromante
 49: q("Skyrim Ritual Stone Whiterun"), 50: q("Skyrim Ritual Stone reanimate"),
 51: q("Skyrim Ritual Stone giant mammoth reanimate", "Skyrim Aetherial Crown"), 52: q("Skyrim Aetherial Crown Aetherium Forge"),
 53: q("Skyrim undead army Ritual Stone"), 54: q("Skyrim Conjure Dremora Lord"),
 55: q("Skyrim Dead Thrall spell"), 56: q("Skyrim Ulfric dead thrall shout"),
 57: q("Skyrim Ulfric thrall Unrelenting Force soldiers"), 58: q("Skyrim Legendary difficulty summons"),
 59: q("Skyrim Mannimarco King of Worms book"),
 # agradecimientos
 60: q("Skyrim Arcanaeum library"), 61: q("Skyrim landscape 4k no HUD"), 62: q("Skyrim Riverwood no HUD"),
 63: q("Skyrim Solitude no HUD"), 64: q("Skyrim aurora no HUD"), 65: q("Skyrim sunrise mountains no HUD"),
 # 5 asesino
 66: q("Skyrim one hit dragon dagger sneak"), 67: q("Skyrim Khajiit character creation"),
 68: q("Skyrim Assassin's Blade 15x sneak attack"), 69: q("Skyrim Shrouded Gloves Astrid"),
 70: q("Skyrim Dark Brotherhood Sanctuary"), 71: q("Skyrim Legendary Dragon fight"),
 72: q("Skyrim 30x sneak attack dagger kill"), 73: q("Skyrim Mehrunes Razor instant kill"),
 74: q("Skyrim Mehrunes Razor Pieces of the Past"), 75: q("Skyrim Babette Sanctuary room"),
 76: q("Skyrim Night Mother coffin"), 77: q("Skyrim Sacred Witness book"),
 # 4 mago sin coste
 78: q("Skyrim 100% destruction cost reduction"), 79: q("Skyrim Dark Elf mage destruction"),
 80: q("Skyrim Lord Stone Morthal"), 81: q("Skyrim fortify destruction enchanting zero cost"),
 82: q("Skyrim arcane enchanter enchanting"), 83: q("Skyrim enchanting circlet ring necklace"),
 84: q("Skyrim Impact perk stagger dragon"), 85: q("Skyrim Chillrend"), 86: q("Skyrim High Elf Highborn"),
 87: q("Skyrim mage dual cast fire"), 88: q("Skyrim College of Winterhold Hall of the Elements"),
 # 3 pararrayos
 89: q("Skyrim fireball spell absorption"), 90: q("Skyrim spell absorption 100%"),
 91: q("Skyrim spell absorption dragon breath"), 92: q("Skyrim Atronach Stone"),
 93: q("Skyrim Miraak's Robes Atronach perk"), 94: q("Skyrim Miraak boss fight"),
 95: q("Skyrim Miraak death Apocrypha"), 96: q("Skyrim Necromage vampire"),
 97: q("Skyrim conjure atronach fail"), 98: q("Skyrim Dragon Priest fight"),
 # campaña
 99: q("Skyrim Dragonborn shout no HUD"), 100: q("Skyrim alchemy lab"),
 # 2 artesano
 101: q("Skyrim legendary smithing daedric"), 102: q("Skyrim Orc character creation"),
 103: q("Skyrim Lover Stone Markarth"), 104: q("Skyrim fortify enchanting potion loop"),
 105: q("Skyrim smithing grindstone legendary"), 106: q("Skyrim Black Book Dragonborn Solstheim"),
 107: q("Skyrim legendary weapon damage"), 108: q("Skyrim armor rating 567 cap"),
 109: q("Skyrim dragonbone dagger sneak kill"),
 # 1 boticario
 110: q("Skyrim fortify restoration glitch"), 111: q("Skyrim unofficial patch USSEP"),
 112: q("Skyrim fortify restoration potion"), 113: q("Skyrim fortify alchemy gear"),
 114: q("Skyrim alchemy lab potion drink"), 115: q("Skyrim fortify restoration infinite active effects"),
 116: q("Skyrim Riften docks fish barrel"), 117: q("Skyrim Frostbite one shot dragon"),
 118: q("Skyrim Greybeards High Hrothgar"), 119: q("Skyrim Greybeards Way of the Voice"),
 120: q("Skyrim Nightcaller Temple"),
 # cierre
 121: q("Skyrim stealth archer dragon"), 122: q("Skyrim Ebony Blade"), 123: q("Skyrim sunrise no HUD"),
}

AQUI = os.path.dirname(os.path.abspath(__file__))
beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
ids = [b["id"] for b in (beats if isinstance(beats, list) else beats["beats"])]
assert len(ids) == len(B) == 123, (len(ids), len(B))
json.dump({f"scene-{n:03d}": v for n, v in sorted(B.items())}, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("busquedas.json:", len(B))
