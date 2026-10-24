# -*- coding: utf-8 -*-
"""Genera busquedas.json (una búsqueda de YouTube por beat) a partir de una tabla por curiosidad.
Reglas (docs/estilo_secuencia_yt.md § busquedas): 2-4 palabras en inglés, nombre propio primero, «no commentary» mejor que «guide»,
lista = respaldos en orden; el sufijo «World of Warcraft» lo añade el motor. Cada beat se asigna a la escena cuyo texto contiene el
centro del texto del beat; dentro de una escena las búsquedas rotan para variar el plano. Uso: python _busquedas_gen.py
"""
import json
import sys

sys.path.insert(0, ".")
import guion  # noqa: E402

ZONA_GEN = {   # respaldo por zona (limpio: ambiente / no commentary)
    "fuego": "Hellfire Peninsula no commentary", "zangar": "Zangarmarsh no commentary", "terokkar": "Shattrath City no commentary",
    "nagrand": "Nagrand Outland no commentary", "filospada": "Blade's Edge Mountains no commentary", "tormenta": "Netherstorm no commentary",
    "sombraluna": "Shadowmoon Valley Outland no commentary", "quelthalas": "Eversong Woods no commentary", "azuremyst": "Azuremyst Isle no commentary",
    "karazhan": "Karazhan no commentary", "cavernas": "Caverns of Time no commentary", "boreal": "Borean Tundra no commentary",
    "fiordo": "Howling Fjord no commentary", "dragones": "Dragonblight no commentary", "pardas": "Grizzly Hills no commentary",
    "zuldrak": "Zul'Drak no commentary", "sholazar": "Sholazar Basin no commentary", "cumbres": "Storm Peaks no commentary",
    "dalaran": "Dalaran Northrend no commentary", "invierno": "Wintergrasp no commentary", "corona": "Icecrown no commentary",
}
B = {
    "intro": ["Outland flyover", "Northrend flyover", "Dark Portal Outland", "Icecrown Citadel exterior", "Shattrath City flyover"],
    "c100": ["Honor Hold TBC", "Danath Trollbane", "Hellfire Peninsula TBC Classic"],
    "c099": ["Path of Glory Hellfire", "Dark Portal Outland side", "Hellfire Peninsula TBC Classic"],
    "c098": ["Fel Reaver Hellfire", "Fel Reaver TBC Classic", "Hellfire Peninsula TBC Classic"],
    "c097": ["Pools of Aggonar", "Temple of Telhamat", "Hellfire Peninsula TBC Classic"],
    "c096": ["Doom Lord Kazzak", "Throne of Kil'jaeden", "Doom Lord Kazzak TBC Classic"],
    "c095": ["Magtheridon's Lair", "Blood Furnace TBC", "Hellfire Citadel TBC"],
    "c094": ["Shattered Halls heroic", "Kargath Bladefist", "Shattered Halls TBC"],
    "c093": ["Telredor Zangarmarsh", "Zangarmarsh TBC Classic", "Zangarmarsh mushrooms night"],
    "c092": ["Dead Mire Zangarmarsh", "Zangarmarsh steam pump", "Zangarmarsh TBC Classic"],
    "c091": ["Sporeggar Zangarmarsh", "Sporeggar reputation", "Zangarmarsh TBC Classic"],
    "c090": ["Coilfang Reservoir entrance", "Lurker Below fishing", "Serpentshrine Cavern"],
    "c089": ["Auchindoun Bone Wastes", "Shadow Labyrinth Murmur", "Terokkar Forest no commentary"],
    "c088": ["Skettis Terokkar", "Sha'tari Skyguard dailies", "Terokk summon"],
    "c087": ["Haris Pilton", "World's End Tavern", "Shattrath City TBC Classic"],
    "c086": ["Griftah Shattrath", "Lower City Shattrath", "Shattrath City TBC Classic"],
    "c085": ["L70ETC concert", "Elite Tauren Chieftain WoW", "World's End Tavern"],
    "c084": ["Scryers Tier Shattrath", "Aldor Rise", "Shattrath City TBC Classic"],
    "c083": ["Terrace of Light Shattrath", "Caverns of Time entrance", "Zephyr Keepers of Time"],
    "c082": ["Oshu'gun Nagrand", "Oshu'gun interior", "Nagrand TBC Classic"],
    "c081": ["Garadar Nagrand", "Garrosh Garadar", "Hero of the Mag'har"],
    "c080": ["Corki Nagrand", "Warmaul Hill Nagrand", "Nagrand TBC Classic"],
    "c079": ["Ring of Blood Nagrand", "Mogor the Ogre", "Nagrand TBC Classic"],
    "c078": ["Elemental Plateau Nagrand", "Twilight Ridge Nagrand", "Nagrand flying no commentary"],
    "c077": ["Halaa Nagrand", "Halaa PvP", "Nagrand TBC Classic"],
    "c076": ["Blade's Edge dragon skeleton", "Gruul's Lair", "Blade's Edge Mountains TBC Classic"],
    "c075": ["Baron Sablemane", "Gorgrom the Dragon-Eater", "Blade's Edge Mountains TBC Classic"],
    "c074": ["Rexxar Outland", "Mok'Nathal Village", "Blade's Edge Mountains TBC Classic"],
    "c073": ["Ogri'la dailies", "Apexis relic Simon", "Blade's Edge Mountains TBC Classic"],
    "c072": ["Vim'gol the Vile", "Vim'gol's Circle", "Blade's Edge Mountains TBC Classic"],
    "c071": ["Toshley's Station", "Sylvanaar TBC", "Blade's Edge Mountains TBC Classic"],
    "c070": ["Area 52 Netherstorm", "Area 52 TBC", "Netherstorm TBC Classic"],
    "c069": ["Eco-Dome Midrealm", "Netherstorm eco dome", "Netherstorm TBC Classic"],
    "c068": ["Manaforge Ultris", "Netherstorm manaforge", "Netherstorm TBC Classic"],
    "c067": ["Kirin'Var Village", "Archmage Vargoth", "Netherstorm TBC Classic"],
    "c066": ["Dimensius the All-Devouring", "Stormspire Netherstorm", "Netherstorm TBC Classic"],
    "c065": ["Hand of Gul'dan volcano", "Shadowmoon Valley TBC", "Shadowmoon Valley Outland flyover"],
    "c064": ["Black Temple entrance", "Doomwalker world boss", "Shadowmoon Valley TBC"],
    "c063": ["Warden's Cage Maiev", "Maiev Shadowsong TBC", "Shadowmoon Valley TBC"],
    "c062": ["Netherwing Ledge dailies", "Netherwing race Skyshatter", "Netherwing drake mount"],
    "c061": ["Teron Gorefiend quest", "Teron Gorefiend I am", "Shadowmoon Valley TBC"],
    "c060": ["M'uru Silvermoon", "Blood Knight Silvermoon", "Silvermoon City no commentary"],
    "c059": ["Dead Scar Eversong", "Deatholme Ghostlands", "Ghostlands no commentary"],
    "c058": ["Windrunner Spire Ghostlands", "Lament of the Highborne", "Ghostlands no commentary"],
    "c057": ["Harrison Jones Zul'Aman", "Zul'Aman gong", "Zul'Aman TBC"],
    "c056": ["Isle of Quel'Danas", "Magisters' Terrace Kael'thas", "Shattered Sun Offensive"],
    "c055": ["Kessel Run quest", "Exodar crash site", "Azuremyst Isle no commentary"],
    "c054": ["Bloodmyst Isle no commentary", "Vector Coil Bloodmyst", "Bloodmyst Isle TBC"],
    "c053": ["Shade of Aran", "Karazhan Opera event", "Karazhan no commentary"],
    "c052": ["Karazhan Crypt", "Upside Down Sinners", "Deadwind Pass Karazhan"],
    "c051": ["Old Hillsbrad Foothills", "Escape from Durnholde", "Old Hillsbrad Southshore"],
    "c050": ["Warsong Hold Borean Tundra", "Garrosh Warsong Hold", "Borean Tundra WotLK"],
    "c049": ["D.E.H.T.A. Borean Tundra", "DEHTA quests", "Borean Tundra WotLK"],
    "c048": ["Fizzcrank Airstrip", "Gearmaster Mechazod", "Borean Tundra WotLK"],
    "c047": ["Keristrasza Nexus", "Nexus dungeon WotLK", "Coldarra Borean Tundra"],
    "c046": ["Transitus Shield Coldarra", "Coldarra Nexus", "Amber Ledge Borean Tundra"],
    "c045": ["Taunka'le Village", "Taunka Borean Tundra", "Borean Tundra WotLK"],
    "c044": ["Nifflevar Howling Fjord", "Echo of Ymiron", "Howling Fjord WotLK"],
    "c043": ["Ingvar the Plunderer", "Utgarde Keep WotLK", "Howling Fjord WotLK"],
    "c042": ["New Agamand Howling Fjord", "Howling Fjord Forsaken quests", "Howling Fjord WotLK"],
    "c041": ["Wyrmrest Temple", "Obsidian Dragonshrine", "Dragonblight WotLK"],
    "c040": ["Galakrond's Rest", "Dragonblight WotLK", "Dragonblight flyover"],
    "c039": ["Naxxramas Dragonblight", "Wintergarde Keep", "Naxxramas WotLK exterior"],
    "c038": ["Wrathgate Dragonblight", "Battle for the Undercity", "Angrathar Wrathgate"],
    "c037": ["Forgotten Shore Dragonblight", "Dragonblight WotLK", "Dragonblight flyover"],
    "c036": ["Frostmourne Cavern", "Frostmourne Cavern quest", "Dragonblight WotLK"],
    "c035": ["New Hearthglen", "Scarlet Onslaught", "Dragonblight WotLK"],
    "c034": ["Grizzlemaw Grizzly Hills", "Ursoc Grizzly Hills", "Vordrassil"],
    "c033": ["Westfall Brigade Encampment", "Amberpine Lodge", "Grizzly Hills WotLK"],
    "c032": ["Silverbrook Grizzly Hills", "Shade of Arugal", "Bloodmoon Isle"],
    "c031": ["Drakil'jin Ruins", "Harrison Jones Grizzly Hills", "Grizzly Hills WotLK"],
    "c030": ["Har'koa Zul'Drak", "Zul'Drak WotLK", "Zul'Drak flyover"],
    "c029": ["Altar of Mam'toth", "Zul'Drak WotLK", "Zul'Drak flyover"],
    "c028": ["Gymer Zul'Drak", "Storm King's Vengeance", "Zul'Drak WotLK"],
    "c027": ["Drakuru Voltarus", "Overlord Drakuru", "Zul'Drak WotLK"],
    "c026": ["Amphitheater of Anguish", "Zul'Drak WotLK", "Zul'Drak flyover"],
    "c025": ["Prophet Tharon'ja", "Drak'Tharon Keep", "Zul'Drak WotLK"],
    "c024": ["Avatar of Freya", "Sholazar Basin WotLK", "Avalanche Sholazar"],
    "c023": ["Sholazar Waygate", "Waygate Un'Goro", "Sholazar Basin WotLK"],
    "c022": ["Nesingwary Base Camp", "Loque'nahak", "Sholazar Basin WotLK"],
    "c021": ["Oracles Sholazar", "Frenzyheart Sholazar", "Green Proto-Drake egg"],
    "c020": ["K3 Storm Peaks", "Storm Peaks WotLK", "Storm Peaks flyover"],
    "c019": ["Brunnhildar Village", "Hyldnir quests", "Storm Peaks WotLK"],
    "c018": ["Thorim Temple of Storms", "Temple of Storms", "Storm Peaks WotLK"],
    "c017": ["Time-Lost Proto-Drake", "Vyragosa Storm Peaks", "Storm Peaks WotLK"],
    "c016": ["Yorg Stormheart", "Frosthold Storm Peaks", "Brothers Bronzebeard quest"],
    "c015": ["Algalon the Observer", "Celestial Planetarium Ulduar", "Ulduar no commentary"],
    "c014": ["Mimiron's Head mount", "Yogg-Saron zero keepers", "Ulduar no commentary"],
    "c013": ["Dalaran Crater Hillsbrad", "Dalaran Northrend flyover", "Dalaran WotLK"],
    "c012": ["Krasus' Landing", "Violet Citadel Dalaran", "Dalaran WotLK"],
    "c011": ["Purple Parlor Dalaran", "Higher Learning achievement", "Archmage Vargoth's Retreat"],
    "c010": ["Minigob Manabonk", "Dalaran bank", "Dalaran WotLK"],
    "c009": ["Crystalsong Forest", "Crystalsong Forest no commentary", "Dalaran flyover"],
    "c008": ["Wintergrasp battle", "Vault of Archavon", "Wintergrasp WotLK"],
    "c007": ["Argent Tournament grounds", "Argent Tournament jousting", "Trial of the Champion"],
    "c006": ["Sindragosa's Fall", "Sindragosa Icecrown", "Icecrown WotLK"],
    "c005": ["Onslaught Harbor Icecrown", "Admiral Revealed quest", "Icecrown WotLK"],
    "c004": ["Orgrim's Hammer gunship", "The Skybreaker Icecrown", "Gunship Battle Icecrown Citadel"],
    "c003": ["Crusaders' Pinnacle", "Argent Vanguard Icecrown", "Icecrown WotLK"],
    "c002": ["Halls of Reflection escape", "Halls of Reflection Lich King", "Frozen Halls WotLK"],
    "c001": ["Crusader Bridenbrad", "Silent Vigil Icecrown", "Boon of A'dal"],
    "cierre": ["Icecrown Citadel exterior", "Dalaran Crater Hillsbrad", "Northrend flyover", "Frozen Throne"],
}
assert set(B) == set(guion.ZONA_DE), set(B) ^ set(guion.ZONA_DE)

beats = json.load(open("beats.json", encoding="utf-8"))
textos = {e["id"]: " ".join(e["frases"]) for e in guion.ESCENAS}
orden = [e["id"] for e in guion.ESCENAS]


def escena_de(texto, desde):
    """Escena cuyo texto contiene el centro del texto del beat (buscando desde la última escena asignada)."""
    c = len(texto) // 2
    frag = texto[max(0, c - 12):c + 12]
    for i in range(desde, len(orden)):
        if frag in textos[orden[i]]:
            return i
    for i in range(len(orden)):
        if frag in textos[orden[i]]:
            return i
    return desde


out, i, k = {}, 0, 0
for b in beats:
    j = escena_de(b["texto"], i)
    k = k + 1 if j == i else 0
    i = j
    eid = orden[i]
    lista = B[eid]
    rot = lista[k % len(lista):] + lista[:k % len(lista)]
    gen = ZONA_GEN[guion.ZONA_DE[eid]]
    out[b["id"]] = rot + ([gen] if gen not in rot else []) + ["WoW gameplay no commentary"]
json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), "beats ·", Counter(escena_de(b["texto"], 0) for b in beats).most_common(3))
print({b["id"]: out[b["id"]][0] for b in beats[:8]})
