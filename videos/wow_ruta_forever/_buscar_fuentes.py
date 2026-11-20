# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por escena -> _candidatos.json (19-nov-2026, wow_ruta_forever).
Copiado de wow_oro_forever/_buscar_fuentes.py. `--extra` corre Q_EXTRA y lo suma; `--txt` rehace _candidatos.txt desde el json;
`--dur id1 id2 ...` mide duración y capítulos de ids sueltos y los guarda en la escena "_medidos"."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Q = {
    "intro": ["WoW Forever gameplay no commentary", "WoW Forever leveling 1-60 route", "WoW Forever world first level 60", "WoW Forever Riverglades gameplay"],
    "p01": ["WoW Forever Zephras Isle", "WoW Forever Zephras Isle skyborn gameplay", "WoW Forever Bandarion Keep", "WoW Forever Elwynn Forest new quests",
            "WoW Forever Durotar new quests", "WoW Forever Tirisfal Glades undead starting zone"],
    "p02": ["WoW Forever Feudal Lords Hall dungeon", "WoW Forever Ruins of Lordaeron dungeon", "WoW Forever Westfall gameplay", "WoW Forever Barrens gameplay",
            "WoW Forever Cozy Sleeping Bag quest"],
    "p03": ["WoW Forever Redridge Mountains gameplay", "WoW Forever Stonetalon Mountains", "WoW Classic Redridge Mountains Lakeshire no commentary",
            "WoW Forever Wailing Caverns", "WoW Forever Deadmines"],
    "burla0": ["WoW Forever Redridge no commentary"],
    "p04": ["WoW Forever Wetlands new quests", "WoW Forever Duskwood gameplay", "WoW Forever Hillsbrad Foothills gameplay", "WoW Forever Ashenvale gameplay",
            "WoW Forever Menethil Southshore boat"],
    "p05": ["WoW Forever Wetlands Excavation dungeon", "Wetlands Excavation Site WoW Forever", "WoW Forever Thousand Needles", "WoW Classic Thousand Needles Shimmering Flats no commentary"],
    "p06": ["WoW Forever Dalaran dungeon", "WoW Forever Dalaran city Alterac", "WoW Forever Arathi Highlands", "WoW Forever Desolace gameplay"],
    "p07": ["WoW Forever Drowned City dungeon", "Drowned City WoW Forever", "WoW Forever Stranglethorn Vale gameplay", "WoW Forever Dustwallow Marsh",
            "WoW Classic Stranglethorn Vale no commentary"],
    "burla1": ["WoW Forever Orgrimmar gameplay no commentary"],
    "p08": ["WoW Forever Riverglades", "WoW Forever Riverglades gameplay", "Krol'dok Stronghold WoW Forever", "WoW Forever Riverglades Horde Rog'mar",
            "WoW Forever Riverglades Farholde Alliance", "WoW Forever Riverglades no commentary"],
    "gracias1": ["WoW Forever Darkmoon Faire", "WoW Forever inn relaxing gameplay"],
    "p09": ["WoW Forever Shen'dralas", "WoW Forever Shen'dralas gameplay", "WoW Forever Shendralas zone", "WoW Forever new zone Desolace Feralas centaur"],
    "burla2": ["WoW Forever Desolace no commentary"],
    "p10": ["WoW Forever Tanaris gameplay", "WoW Forever Feralas gameplay", "WoW Forever Hinterlands gameplay", "WoW Forever Zul'Farrak", "WoW Forever riding level 40 mount"],
    "p11": ["Alcaz Prison WoW Forever", "WoW Forever Alcaz Prison dungeon", "WoW Forever Azshara new quests", "WoW Forever Un'Goro Crater", "WoW Forever Azshara gameplay"],
    "p12": ["WoW Forever Burning Steppes", "WoW Forever Western Plaguelands", "WoW Forever Blackrock Depths", "WoW Classic Burning Steppes no commentary"],
    "gracias2": ["WoW Forever warrior gameplay no commentary"],
    "p13": ["Blackmaw Hold WoW Forever", "WoW Forever Blackmaw Hold dungeon", "WoW Forever Winterspring", "WoW Forever Eastern Plaguelands", "WoW Forever Silithus"],
    "p14": ["WoW Forever Mount Hyjal", "Mount Hyjal WoW Forever gameplay", "WoW Forever Shaper's Terrace dungeon", "Shaper's Terrace WoW Forever", "WoW Forever Hyjal no commentary"],
    "cierre": ["WoW Forever level 60 ding", "WoW Forever no commentary leveling", "WoW Forever Stormwind gameplay"],
}

# Segunda pasada (19-nov-2026, hecha a mano con ytsearch y listas de canal; los ids elegidos están medidos en "_medidos"):
# series sin narrar con la zona en el título y ambientes de Forever sin interfaz.
Q_EXTRA = {
    "_series": ["DankeyKong WoW Forever Full Dungeon Clear Longplay no Commentary", "MatodanDLC WoW Forever Road to Level 60 Playthrough Hunter",
                "Robot89 WoW Forever Gameplay Part 4K No Commentary", "Loopy Longplays World of Warcraft Forever Longplay",
                "fwengli WoW Forever protection warrior pve leveling 1-60", "Music & Ambience World of Warcraft: Forever",
                "Azeroth Ambience World of Warcraft Forever", "NFGames 1 Hour of Music & Ambience World of Warcraft Forever"],
    "_zonas": ["Shen'dralas Music Ambience WoW Forever", "Wetlands Music Ambience World of Warcraft Forever",
               "Dalaran Alterac Music Ambience World of Warcraft Forever", "WoW Forever Hall of Feudal Lords full run",
               "Hall of Thanes WoW Forever no commentary", "WoW Forever Alcaz Prison full run no commentary",
               "WoW Forever Blackmaw Hold full run", "WoW Forever Shaper's Terrace full run no commentary",
               "WoW Forever Winterspring questing", "WoW Forever Thousand Needles questing", "WoW Forever new Azshara zone"],
}
# Listas de canal revisadas: https://www.youtube.com/@fwengli/videos (99 partes), @Meisio/videos («Vanilla …» = Classic), @GarnathanGaming,
# @BigChunkyTV, @Blizzplanet.


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
