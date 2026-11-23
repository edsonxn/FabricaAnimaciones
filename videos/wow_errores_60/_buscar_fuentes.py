# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por escena -> _candidatos.json (22-nov-2026, wow_errores_60).
Copiado de wow_ruta_forever/_buscar_fuentes.py. `--extra` corre Q_EXTRA y lo suma; `--txt` rehace _candidatos.txt desde el json;
`--dur id1 id2 ...` mide duración y capítulos de ids sueltos y los guarda en la escena "_medidos"."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Q = {
    "intro": ["WoW Forever level 60 dungeon no commentary", "WoW Forever raid prep level 60", "WoW Forever Upper Blackrock Spire",
              "WoW Forever Stratholme no commentary"],
    "c25": ["WoW Forever priest healer dungeon gameplay", "WoW Forever healer level 60 no commentary", "WoW Forever vendor ring exchange"],
    "c24": ["WoW Forever Warsong Gulch", "WoW Forever Warsong Gulch no commentary", "WoW Forever duels Orgrimmar gate",
            "WoW Forever PvP honor weekly"],
    "overgear": ["WoW Forever leveling gameplay 4K no commentary", "WoW Forever level 58 questing no commentary"],
    "c23": ["Onyxia 40 man raid no commentary", "Onyxia's Lair full raid classic no commentary", "Onyxia deep breath whelps classic raid",
            "Onyxia's Lair classic 2019 raid pov"],
    "c22": ["WoW Forever PvP vendor honor gear", "WoW Forever Alterac Valley", "WoW Forever battleground gameplay no commentary"],
    "c21": ["WoW Forever Alterac Valley no commentary", "WoW Forever Dustwallow Marsh", "WoW Forever Arathi Basin",
            "WoW Forever PvP rank"],
    "c20": ["WoW Forever auction house", "WoW Forever alchemy profession", "WoW Forever cooking", "WoW Forever flask potion crafting"],
    "c19": ["WoW Forever dungeon wipe", "WoW Forever epic mount 60", "WoW Forever repair armor gold"],
    "c18": ["WoW Forever Mount Hyjal", "WoW Forever Nordrassil", "WoW Forever Hyjal Summit raid entrance"],
    "c17": ["WoW Forever Barrow Deeps entrance", "WoW Forever Winterspring", "WoW Forever Blackmaw Hold"],
    "c16": ["Blackmaw Hold full run no commentary", "WoW Forever Blackmaw Hold dungeon", "WoW Forever Azshara", "WoW Forever Thunder Bluff"],
    "c15": ["Shaper's Terrace full run", "WoW Forever Shaper's Terrace", "WoW Forever Un'Goro Crater power crystals",
            "WoW Forever Un'Goro Crater no commentary"],
    "c14": ["WoW Forever epic mount riding trainer", "WoW Forever epic mount", "WoW Forever riding 60 mount vendor"],
    "c12": ["WoW Forever Blackmaw Hold farm", "Blackmaw Hold WoW Forever no commentary"],
    "c11": ["WoW Forever Upper Blackrock Spire full run", "Upper Blackrock Spire classic no commentary", "UBRS full run classic"],
    "c10": ["Onyxia attunement Drakefire Amulet", "Onyxia's Lair entrance Dustwallow Marsh", "WoW Forever Onyxia attunement"],
    "c09": ["fire resistance gear classic onyxia", "Greater Fire Protection Potion", "Onyxia Scale Cloak"],
    "c08": ["WoW Forever guild raid group", "WoW Forever 40 man raid", "classic wow 40 man raid no commentary"],
    "c07": ["WoW Forever blacksmithing", "WoW Forever tailoring", "WoW Forever leatherworking", "WoW Forever crafting profession 300"],
    "c06": ["WoW Forever Guardians of Hyjal", "WoW Forever Summit of Eternity", "WoW Forever Hyjal quests"],
    "c05": ["WoW Forever Stratholme", "WoW Forever Scholomance", "WoW Forever dungeon farm reset", "Stratholme full run no commentary",
            "Scholomance full run no commentary"],
    "c04": ["WoW Forever Lower Blackrock Spire", "Lower Blackrock Spire classic no commentary", "Seal of Ascension quest Emberstrife",
            "General Drakkisath classic", "Upper Blackrock Spire Rend classic"],
    "c03": ["WoW Forever enchanting disenchant", "classic wow disenchanting raid loot", "WoW Forever raid loot"],
    "c02": ["Rend head world buff classic", "Songflower Serenade buff", "Dire Maul tribute run classic", "Darkmoon Faire classic wow",
            "WoW Forever world buffs"],
    "c01": ["Darkmaster Gandling classic", "Baron Rivendare classic", "Dungeon Set 2 quest chain classic", "Stratholme 45 minute run Baron",
            "WoW Forever dungeon set"],
    "cierre": ["WoW Forever raid", "WoW Forever level 60 gameplay no commentary"],
}

Q_EXTRA = {
    "_series": ["DankeyKong WoW Forever Full Dungeon Clear Longplay no Commentary", "DankeyKong WoW Forever Stratholme",
                "DankeyKong WoW Forever Scholomance", "DankeyKong WoW Forever Blackrock Spire", "DankeyKong WoW Forever Blackmaw Hold",
                "DankeyKong WoW Forever Shaper's Terrace", "Meisio Vanilla Burning Steppes", "Meisio Vanilla Dustwallow Marsh",
                "Meisio Vanilla Azshara", "Meisio Vanilla Un'Goro"],
    "_zonas": ["WoW Forever Darnassus ambience", "WoW Forever Orgrimmar ambience", "WoW Forever Stormwind ambience",
               "WoW Forever Ironforge ambience", "WoW Forever Dire Maul", "WoW Forever Felwood", "WoW Forever Dustwallow Marsh questing",
               "fwengli Dustwallow Marsh WoW Forever", "fwengli Felwood WoW Forever", "fwengli Winterspring WoW Forever",
               "fwengli Azshara WoW Forever", "WoW Forever Black Lance Isles battleground", "WoW Forever auction house browsing gameplay",
               "WoW Forever enchanting disenchant gameplay", "WoW Forever blacksmith anvil crafting gameplay",
               "WoW Forever level 60 ding", "WoW Forever Stratholme full run no commentary",
               "WoW Forever Scholomance full run no commentary", "WoW Forever Upper Blackrock Spire no commentary",
               "WoW Forever Lower Blackrock Spire no commentary", "Hindenburg Onyxia No Commentary",
               "WoW Forever Rend head buff Orgrimmar", "WoW Forever duel"],
}


def buscar(q, n=8):
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
                for x in l[:8]:
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
    if "--extra" in sys.argv or os.path.exists("_candidatos.json"):
        out = json.load(open("_candidatos.json", encoding="utf-8")) if os.path.exists("_candidatos.json") else {}
        for e, qs in qd.items():
            out.setdefault(e, {}).update({q: res[q] for q in qs})
    else:
        out = {e: {q: res[q] for q in qs} for e, qs in qd.items()}
    json.dump(out, open("_candidatos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    escribir_txt(out)
    print("ok", len(pares), "búsquedas")
    sys.exit(0)
