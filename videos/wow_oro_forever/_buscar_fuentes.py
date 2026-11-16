# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por escena -> _candidatos.json (15-nov-2026, wow_oro_forever)."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

Q = {
    "intro": ["WoW Forever riding trainer level 40 mount", "WoW Forever broke at level 40 mount gold", "WoW Forever epic mount 1000 gold level 60", "WoW Forever gameplay no commentary"],
    "c30": ["WoW Forever class trainer cost", "WoW Forever skip spell ranks save gold", "WoW Classic class trainer spell ranks", "WoW Classic warrior trainer"],
    "c29": ["WoW Forever warlock mount quest Felsteed", "WoW Forever paladin mount quest", "WoW Classic Strahad Farsan warlock mount Ratchet", "WoW Classic paladin Tome of Nobility mount quest"],
    "c28": ["WoW Forever riding trainer 90 gold honored", "WoW Classic Randal Hunter riding trainer Elwynn", "WoW Classic Kildar wolf rider Orgrimmar", "WoW Classic reputation honored discount mount"],
    "burla0": ["WoW Forever Elwynn Forest gameplay no commentary"],
    "c27": ["WoW Forever legacy points Frequent Flier", "WoW Forever legacy Bartering", "WoW Forever legacy system explained", "WoW Forever legacy talents"],
    "c26": ["WoW Forever dual spec 50 gold", "WoW Forever how to get dual spec", "WoW Classic respec cost talent trainer", "WoW Forever talents window"],
    "c25": ["WoW Forever auction house weapons gear", "WoW Forever auction house gameplay", "WoW Classic auction house Orgrimmar browsing", "WoW Forever level 40 gold"],
    "c24": ["WoW Forever skinning gold leveling", "WoW Forever skinning mining gold", "WoW Classic skinning leveling gameplay", "WoW Forever herbalism mining farm"],
    "c23": ["Auctionator WoW Forever full scan", "WoW Forever Auctionator guide", "Auctionator classic tooltip vendor price", "WoW Classic Auctionator selling guide"],
    "c22": ["WoW Forever auction house deposit", "WoW Forever auction house tips", "WoW Classic Gadgetzan auction house neutral", "WoW Classic Booty Bay auction house"],
    "c21": ["WoW Forever auction house below vendor price", "WoW Classic auction house flipping vendor", "WoW Classic vendor flipping auction house gold", "WoW Forever auction house flipping"],
    "gracias1": ["WoW Forever Westfall gameplay no commentary"],
    "c20": ["WoW Forever bank alt enchanting disenchant", "Disenchantrix addon", "WoW Classic enchanting disenchant gold", "WoW Classic bank alt mailbox auction house"],
    "c19": ["WoW Forever Chol'aruk elite quest Barrens", "WoW Forever Zephras Isle quest rewards", "WoW Forever new quests Barrens", "WoW Forever Zephras Isle"],
    "c18": ["WoW Forever Darkmoon Storage Box 14 slot", "Red Mageweave Bag 14 slot WoW Forever", "WoW Classic Darkmoon Faire tickets turn in", "WoW Forever bags inventory"],
    "c17": ["WoW Forever silk bandage vendor profit", "WoW Forever cloth farm", "WoW Classic first aid silk bandage", "WoW Classic silk cloth farm"],
    "burla1": ["WoW Forever Stormwind gameplay no commentary"],
    "c16": ["Green Hills of Stranglethorn pages WoW Forever auction house", "Green Hills of Stranglethorn quest classic", "WoW Classic Stranglethorn Vale gameplay", "WoW Forever Stranglethorn Vale"],
    "c15": ["WoW Forever fishing trunk open water", "Tightly Sealed Trunk fishing classic", "WoW Forever fishing gold", "WoW Classic open water fishing Westfall"],
    "c14": ["Big Iron Fishing Pole Shellfish Trap Desolace", "WoW Classic Big Iron Fishing Pole", "WoW Classic Shellfish Trap Desolace", "WoW Forever Desolace"],
    "c13": ["Super-Seller 680 Desolace", "WoW Classic Supervendedor 680 Gizelton caravan", "Lean Wolf Steak recipe classic", "WoW Classic Gizelton caravan Desolace"],
    "c12": ["WoW Forever warrior charms Arathi farm", "Thundering Charm farm Classic", "WoW Classic Whirlwind Axe quest warrior", "WoW Classic Arathi Highlands Boulderfist"],
    "c11": ["Blue Pearl Vile Reef WoW Forever", "Pearl Diving quest Badlands classic", "WoW Classic Vile Reef giant clam", "WoW Classic Stranglethorn underwater clams"],
    "gracias2": ["WoW Forever Durotar gameplay no commentary"],
    "c10": ["Giant Egg farm WoW Forever Tanaris", "WoW Forever Hinterlands owlbeast farm", "WoW Classic Giant Egg roc Tanaris", "WoW Classic Gadgetzan cooking quest giant egg"],
    "c09": ["WoW Forever Feralas gray items gold farm", "WoW Forever raw gold farm vendor", "WoW Classic Feralas gryphon farm", "WoW Classic Hillsbrad farmers pitchfork"],
    "c08": ["WoW Forever Tanaris turtle gold farm Surf Glider", "Frostadamus WoW Forever gold farm", "WoW Classic Surf Glider Tanaris turtles", "WoW Classic Tanaris coast farm"],
    "c07": ["WoW Forever Waylaid Crate turn in", "WoW Forever Shipping Label quest", "WoW Forever Waylaid Crates explained", "WoW Forever Merchant's Favor"],
    "c06": ["WoW Forever Merchant's Favor recipes vendor", "WoW Forever enchant necklace formula", "WoW Forever new recipes profession", "WoW Forever new crafting recipes"],
    "burla2": ["WoW Forever Ironforge gameplay no commentary"],
    "c05": ["WoW Forever investments gold Swiftthistle", "WoW Forever Onyxia fire resistance potion", "WoW Classic Onyxia's Lair raid", "WoW Forever raids December Onyxia"],
    "c04": ["WoW Forever fishing floating wreckage trunks", "Bright Baubles Booty Bay fishing Forever", "WoW Classic floating wreckage fishing Tanaris", "WoW Classic Old Man Heming Booty Bay fishing"],
    "c03": ["WoW Forever runecloth farm satyr Felwood", "Studen Albatroz 1000 gold WoW Forever", "WoW Classic Jadefire satyrs Felwood runecloth", "WoW Classic Azshara Legashi satyr runecloth farm"],
    "c02": ["Rich Thorium Vein Burning Steppes WoW Forever", "WoW Forever black market Mister Graphed", "WoW Classic Burning Steppes thorium mining", "WoW Forever Riverglades"],
    "c01": ["WoW Forever quest gold hotfix level 48", "WoW Forever Mount Hyjal questing", "WoW Forever Mount Hyjal", "WoW Forever quests give gold"],
    "cierre": ["WoW Forever gameplay no commentary", "WoW Forever Stormwind", "WoW Forever level 60 mount"],
}

# Segunda pasada (15-nov-2026): huecos de la primera (huevos, almejas, grifos, páginas, señuelo, talismanes, subasta).
# `python _buscar_fuentes.py --extra` corre solo estas y las suma a _candidatos.json; `--txt` rehace _candidatos.txt desde el json.
Q_EXTRA = {
    "c10": ["Tanaris roc giant egg farm", "WoW Classic Giant Egg farm", "Hinterlands owlbeast farm classic", "Dirge Quikcleave Gadgetzan cooking"],
    "c11": ["Vile Reef Stranglethorn underwater", "WoW Classic Blue Pearl farm Stranglethorn", "Giant Clam Stranglethorn classic"],
    "c09": ["Feralas gryphon farm classic vendor", "Feralas Frayfeather gryphon", "Hillsbrad farmers farm classic gold", "Feralas gameplay no commentary"],
    "c16": ["Stranglethorn pages farm classic", "Green Hills of Stranglethorn pages auction house", "Stranglethorn Vale gameplay no commentary 4K"],
    "c04": ["Bright Baubles fishing lure classic", "Booty Bay gameplay no commentary", "Floating Wreckage Pool classic fishing"],
    "c12": ["Highland exiles Arathi Highlands classic", "Arathi Highlands gameplay no commentary", "Burning Charm Cresting Charm Arathi"],
    "c25": ["WoW Forever auction house browse weapons", "WoW Forever auction house no commentary"],
    "c22": ["WoW Forever create auction deposit duration", "Gadgetzan gameplay no commentary"],
    "c19": ["Razorfen Kraul Barrens Bael Modan Chol'aruk", "Barrens gameplay WoW Forever no commentary"],
    "c05": ["Onyxia's Lair WoW Forever", "Fire Resistance Potion classic", "Elemental Fire farm classic"],
    "c02": ["Arcane Crystal mining Burning Steppes", "Burning Steppes gameplay no commentary"],
    "c03": ["Felwood gameplay no commentary", "Azshara gameplay no commentary classic"],
    "c08": ["Tanaris gameplay no commentary", "Surf Glider turtle farm Tanaris coast"],
    "c14": ["Desolace gameplay no commentary", "Shellfish trap underwater Desolace"],
    "c28": ["WoW Forever learn riding level 40 trainer", "WoW Forever reputation window honored"],
    "c30": ["WoW Forever class trainer spells window", "WoW Forever warrior trainer"],
}


def buscar(q):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(duration)s|%(channel)s|%(title)s", f"ytsearch6:{q}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
                       env=dict(__import__("os").environ, PYTHONIOENCODING="utf-8"))
    return q, [l.split("|", 3) for l in r.stdout.splitlines() if l.count("|") >= 3]


def escribir_txt(out):
    with open("_candidatos.txt", "w", encoding="utf-8") as f:
        for e, d in out.items():
            f.write(f"== {e}\n")
            for q, l in d.items():
                f.write(f" # {q}\n")
                for x in l[:6]:
                    f.write(f"   {x[0]} {(x[1] or '?')[:6]} {x[2][:22]} | {x[3][:80]}\n")


if __name__ == "__main__":
    if "--txt" in sys.argv:
        escribir_txt(json.load(open("_candidatos.json", encoding="utf-8")))
        sys.exit(0)
    qd = Q_EXTRA if "--extra" in sys.argv else Q
    pares = [(e, q) for e, qs in qd.items() for q in qs]
    with ThreadPoolExecutor(6) as ex:
        res = dict(ex.map(lambda p: buscar(p[1]), pares))
    if "--extra" in sys.argv:
        out = json.load(open("_candidatos.json", encoding="utf-8"))
        for e, qs in qd.items():
            out.setdefault(e, {}).update({q: res[q] for q in qs})
    else:
        out = {e: {q: res[q] for q in qs} for e, qs in qd.items()}
    json.dump(out, open("_candidatos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    escribir_txt(out)
    for e in qd:
        print("==", e)
        for q in qd[e]:
            for x in out[e][q][:6]:
                print("  ", x[0], (x[1] or "?")[:6], x[2][:22], "|", x[3][:80])
    sys.exit(0)
