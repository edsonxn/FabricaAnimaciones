# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por escena -> _candidatos.json (25-nov-2026,
wow_ruta_profesiones). Copiado de wow_errores_60/_buscar_fuentes.py. `--extra` corre Q_EXTRA y lo suma; `--txt` rehace
_candidatos.txt desde el json; `--dur id1 id2 ...` mide duración y capítulos de ids sueltos y los guarda en "_medidos".
Fuentes ya probadas en wow_ruta_forever / wow_errores_60 (zonas de Forever, Meisio, fwengli, Esshow, Loopy) se reutilizan:
`_busquedas.py` lee también sus _candidatos.json para las duraciones."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Q = {
    "intro": ["WoW Forever professions gameplay", "WoW Forever camp campfire", "WoW Forever heavy thorium vein Mount Hyjal",
              "WoW Forever loom tailoring", "WoW Forever camping system"],
    "reglas": ["WoW Forever profession trainer", "WoW Forever profession window K", "WoW Forever reagent bag slot",
               "WoW Forever junior trainer", "WoW Forever professions UI"],
    "overgear": ["WoW Forever leveling gameplay no commentary", "WoW Forever dungeon no commentary"],
    "p01": ["WoW Forever mining", "WoW Forever mining 1-300", "WoW Forever poor copper vein", "WoW Forever amber teldrassil mining",
            "WoW Forever heavy thorium", "WoW Forever molten foundry smelt", "WoW Forever mining gameplay no commentary",
            "WoW Forever Riverglades iron", "classic wow mining gameplay no commentary", "WoW Forever thorium farming"],
    "p02": ["WoW Forever blacksmithing", "WoW Forever blacksmithing 1-300", "WoW Forever blessed plate", "WoW Forever master forge",
            "WoW Forever favor vendor", "WoW Forever Booty Bay", "classic wow blacksmithing anvil crafting"],
    "p03": ["WoW Forever engineering", "WoW Forever engineering 1-300", "WoW Forever goblin glider", "WoW Forever reagent bot",
            "WoW Forever Gadgetzan", "classic wow engineering explosive sheep"],
    "p04": ["WoW Forever herbalism", "WoW Forever herbalism 1-300", "WoW Forever greenhouse seeds", "WoW Forever marefoil demonsage",
            "WoW Forever herb farming no commentary", "classic wow herbalism gameplay no commentary"],
    "p05": ["WoW Forever alchemy", "WoW Forever alchemy 1-300", "WoW Forever alchemy laboratory", "WoW Forever flask crafting",
            "WoW Forever Felwood Emerald Sanctuary", "classic wow alchemy crafting potions"],
    "p06": ["WoW Forever skinning", "WoW Forever skinning 1-300", "WoW Forever yeti cave Hillsbrad", "WoW Forever Feralas yeti",
            "WoW Forever pristine leather", "classic wow skinning gameplay no commentary", "WoW Forever Un'Goro devilsaur"],
    "p07": ["WoW Forever leatherworking", "WoW Forever leatherworking 1-300", "WoW Forever camp tent", "WoW Forever blue suede shoes",
            "classic wow leatherworking crafting"],
    "p08": ["WoW Forever tailoring", "WoW Forever tailoring 1-300", "WoW Forever reagent bag", "WoW Forever Pexmit",
            "WoW Forever mageweave bag", "classic wow tailoring crafting"],
    "p09": ["WoW Forever enchanting", "WoW Forever enchanting 1-300", "WoW Forever disenchant", "WoW Forever enchant necklace",
            "Uldaman Annora enchanting", "classic wow enchanting crafting"],
    "p10": ["WoW Forever cooking", "WoW Forever cooking 1-300", "WoW Forever campfire kit", "WoW Forever camp buffs",
            "WoW Forever Cookie Deadmines", "classic wow cooking campfire"],
    "p11": ["WoW Forever fishing", "WoW Forever fishing 1-300", "WoW Forever fish bowl camp", "WoW Forever fishing tournament",
            "WoW Forever Azshara fishing", "classic wow fishing gameplay no commentary", "Nat Pagle Dustwallow fishing"],
    "p12": ["WoW Forever first aid", "WoW Forever first aid 1-300", "WoW Forever healing potion first aid", "WoW Forever triage quest",
            "classic wow first aid triage", "WoW Forever Hammerfall"],
    "combos": ["WoW Forever professions which to pick", "WoW Forever crafting gameplay"],
    "cierre": ["WoW Forever level 60 gameplay no commentary", "WoW Forever camp group"],
}

Q_EXTRA = {
    "_zonas": ["WoW Forever Mulgore", "WoW Forever Teldrassil", "WoW Forever Hillsbrad Foothills", "WoW Forever Alterac Mountains",
               "WoW Forever Wetlands", "WoW Forever Silverpine Forest", "WoW Forever Ashenvale", "WoW Forever Loch Modan",
               "WoW Forever Darkshore", "WoW Forever Stonetalon", "WoW Forever Stranglethorn", "WoW Forever Hinterlands",
               "WoW Forever Felwood", "WoW Forever Feralas", "WoW Forever Searing Gorge", "WoW Forever Uldaman",
               "WoW Forever Dalaran", "WoW Forever Undercity", "WoW Forever Theramore", "WoW Forever Desolace",
               "WoW Forever Swamp of Sorrows", "WoW Forever Westfall", "WoW Forever Durotar", "WoW Forever Elwynn Forest",
               "WoW Forever Badlands", "WoW Forever Redridge", "WoW Forever Arathi Highlands", "WoW Forever Thousand Needles",
               "WoW Forever Eastern Plaguelands", "WoW Forever Crossroads Barrens", "WoW Forever Booty Bay fishing",
               "WoW Forever Deadmines", "WoW Forever Wailing Caverns", "WoW Forever Blackfathom Deeps", "WoW Forever Sunken Temple",
               "WoW Forever Stratholme", "WoW Forever Scholomance", "WoW Forever Blackrock Depths", "WoW Forever Dire Maul"],
    "_oficios": ["WoW Forever mining no commentary", "WoW Forever herbalism no commentary", "WoW Forever skinning no commentary",
                 "WoW Forever fishing no commentary", "WoW Forever crafting no commentary", "WoW Forever professions leveling",
                 "WoW Forever camp items", "WoW Forever campfire", "WoW Forever reagent pouch", "WoW Forever auction house"],
}


def buscar(q, n=10):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(duration)s|%(channel)s|%(title)s", f"ytsearch{n}:{q}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return q, [l.split("|", 3) for l in r.stdout.splitlines() if l.count("|") >= 3]


def medir(i):
    r = subprocess.run(["yt-dlp", "--skip-download", "--print", "%(id)s|%(duration)s|%(channel)s|%(title)s|%(chapters)j", Y(i)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    l = r.stdout.strip().splitlines()
    return l[-1].split("|", 4) if l and l[-1].count("|") >= 4 else [i, "", "", "ERR " + r.stderr[-200:], "null"]


def Y(i):
    return "https://www.youtube.com/watch?v=" + i


def escribir_txt(out):
    with open("_candidatos.txt", "w", encoding="utf-8") as f:
        for e, d in out.items():
            f.write(f"== {e}\n")
            for q, l in d.items():
                f.write(f" # {q}\n")
                for x in l[:10]:
                    f.write(f"   {x[0]} {(x[1] or '?')[:6]} {x[2][:22]} | {x[3][:80]}\n")


if __name__ == "__main__":
    if "--txt" in sys.argv:
        escribir_txt(json.load(open("_candidatos.json", encoding="utf-8")))
        sys.exit(0)
    if "--dur" in sys.argv:
        ids = sys.argv[sys.argv.index("--dur") + 1:]
        with ThreadPoolExecutor(6) as ex:
            res = list(ex.map(medir, ids))
        out = json.load(open("_candidatos.json", encoding="utf-8")) if os.path.exists("_candidatos.json") else {}
        med = out.setdefault("_medidos", {}).setdefault("ids sueltos", [])
        ya = {x[0] for x in med}
        for x in res:
            print(x[0], x[1], x[2][:22], "|", x[3][:80])
            try:
                for c in json.loads(x[4]) or []:
                    print(f"      {int(c['start_time'])} {c['title'][:70]}")
            except Exception:
                pass
            if x[1] and x[0] not in ya:
                med.append(x[:4])
        json.dump(out, open("_candidatos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        sys.exit(0)
    qd = Q_EXTRA if "--extra" in sys.argv else Q
    pares = [(e, q) for e, qs in qd.items() for q in qs]
    with ThreadPoolExecutor(6) as ex:
        res = dict(ex.map(lambda p: buscar(p[1]), pares))
    out = json.load(open("_candidatos.json", encoding="utf-8")) if os.path.exists("_candidatos.json") else {}
    for e, qs in qd.items():
        out.setdefault(e, {}).update({q: res[q] for q in qs})
    json.dump(out, open("_candidatos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    escribir_txt(out)
    print("ok", len(pares), "búsquedas")
    sys.exit(0)
