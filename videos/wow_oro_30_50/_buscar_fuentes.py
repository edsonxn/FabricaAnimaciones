# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por puesto -> _candidatos.json / _candidatos.txt
(26-nov-2026, wow_oro_30_50). Copiado de wow_ruta_profesiones/_buscar_fuentes.py. Sirve para ESCRIBIR busquedas.json con
consultas que de verdad devuelven la criatura/lugar (y para leer títulos: una búsqueda de zona puede devolver otra zona).
`--extra` corre Q_EXTRA y lo suma; `--txt` rehace _candidatos.txt desde el json."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

os.chdir(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

Q = {
    "intro": ["WoW Forever riding trainer level 40", "WoW Forever gold farms tested", "WoW Forever gold farming no commentary",
              "WoW Forever dual spec class trainer"],
    "reglas": ["WoW Forever auction house", "classic wow vendor selling grays", "WoW Forever dungeon reset lockout"],
    "p15": ["Magram Village Desolace", "Desolace centaur grind", "Magram centaurs WoW", "Desolace no commentary classic",
            "WoW Forever Desolace"],
    "p14": ["Darkmist Cavern", "Dustwallow Marsh spiders", "Darkmist spider farm", "Brackenwall Village", "WoW Forever Dustwallow Marsh",
            "Theramore Isle classic"],
    "p13": ["Stranglethorn gorilla farm", "Mistvale Valley gorillas", "Mokk the Savage", "Stranglethorn Fever quest classic",
            "Lake Nazferiti"],
    "p12": ["Shimmering Flats turtles", "Sparkleshell Snapper", "Shimmering Flats classic wow", "Mirage Raceway",
            "Mudrock tortoise Dustwallow", "WoW Forever Thousand Needles"],
    "p11": ["Riverglades sand crawler", "Riverglades crab farm", "WoW Forever Riverglades", "Powderfuse Port",
            "Stranglethorn crab farm Booty Bay", "Big-mouth clam pearl", "Tender Crab Meat farm"],
    "p10": ["Scalding Whelp Badlands", "Badlands whelp farm", "Lethlor Ravine", "Dark Whelpling pet classic", "WoW Forever Badlands"],
    "p09": ["Swamp of Sorrows murlocs", "Marsh Oracle murloc", "Swamp of Sorrows murloc farm", "Stagalbog Cave",
            "golden pearl drop classic wow", "WoW Forever Swamp of Sorrows"],
    "p08": ["Blisterpaw Hyena", "Tanaris hyena farm", "Abyssal Sands Tanaris", "Fire Roc Tanaris giant egg", "Gadgetzan classic",
            "WoW Forever Tanaris"],
    "p07": ["Groddoc Thunderer Feralas", "Feralas gorilla farm", "Ironfur Patriarch", "Twin Colossals Feralas", "Camp Mojache",
            "Feathermoon Stronghold", "WoW Forever Feralas"],
    "p06": ["Swamp Jaguar farm", "Swamp of Sorrows jaguar", "Swamp of Sorrows skinning", "Stonard classic wow",
            "Riverglades huntress"],
    "p05": ["Badlands rock elementals", "Lesser Rock Elemental farm", "Badlands elemental farm", "Kargath Badlands",
            "Elemental Earth farm classic", "Badlands no commentary"],
    "p04": ["Riverglades coyote farm", "Riverglades gold farm", "Wheeler Homestead Riverglades", "Studen Albatroz Riverglades",
            "Darkmoon Faire classic wow"],
    "p03": ["Mithril Bound Trunk fishing", "Stranglethorn floating wreckage", "Stonescale Eel fishing", "Stranglethorn fishing classic",
            "WoW Forever fishing gold", "Grom'Gol classic", "Booty Bay classic no commentary"],
    "p02": ["Alterac Mountains ogre cave", "Crushridge Hold", "Alterac Mountains mining", "Lo'Grosh rare", "Rizz Loosebolt",
            "Alterac mining gold farm", "WoW Forever Alterac Mountains"],
    "p01": ["Black Slayer Blasted Lands", "Vulture Gizzard farm", "Blasted Lands gold farm", "Blasted Lands vulture farm",
            "Nethergarde Keep", "WoW Forever Blasted Lands", "Blasted Lands no commentary", "Scorpok Blasted Lands"],
    "neutro": ["WoW Forever gameplay no commentary", "WoW Forever leveling no commentary", "WoW Forever dungeon no commentary",
               "WoW Forever level 40 mount", "Onyxia's Lair classic no commentary"],
}

Q_EXTRA = {
    "_zonas": ["Alterac Mountains Meisio", "Blasted Lands Meisio", "Badlands Meisio", "Dustwallow Marsh Meisio",
               "Thousand Needles no commentary classic", "Stranglethorn Vale no commentary classic", "Feralas Meisio",
               "Swamp of Sorrows no commentary", "Booty Bay fishing classic", "WoW Forever Booty Bay", "WoW Forever Gadgetzan",
               "Alterac Mountains classic no commentary", "Blasted Lands classic wow questing", "Hillsbrad Foothills Meisio",
               "Desolace Meisio", "Tanaris no commentary classic", "WoW Forever Stranglethorn", "Dustwallow Marsh no commentary classic",
               "WoW Forever Hillsbrad", "Badlands classic questing no commentary", "WoW Forever fishing no commentary",
               "WoW Forever mining no commentary", "WoW Forever skinning gameplay", "WoW Forever vendor selling"],
}


def buscar(q, n=10):
    qq = q if ("wow" in q.lower().split() or "world of warcraft" in q.lower()) else q + " World of Warcraft"
    r = subprocess.run(["yt-dlp", f"ytsearch{n}:{qq}", "--flat-playlist", "--dump-json", "--no-warnings"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=120)
    out = []
    for ln in r.stdout.splitlines():
        try:
            j = json.loads(ln)
        except ValueError:
            continue
        out.append([j.get("id"), j.get("duration") or 0, j.get("channel") or j.get("uploader") or "", j.get("title") or ""])
    return qq, out


def txt(c):
    lineas = []
    for g, qs in c.items():
        if g.startswith("_"):
            continue
        lineas.append(f"== {g}")
        for q, lst in qs.items():
            lineas.append(f" # {q}")
            for i, d, ch, t in lst:
                lineas.append(f"   {i} {int(float(d or 0))} {ch[:22]} | {t[:90]}")
    open("_candidatos.txt", "w", encoding="utf-8").write("\n".join(lineas) + "\n")


if __name__ == "__main__":
    c = json.load(open("_candidatos.json", encoding="utf-8")) if os.path.exists("_candidatos.json") else {}
    if "--txt" in sys.argv:
        txt(c)
        raise SystemExit("ok")
    grupos = Q_EXTRA if "--extra" in sys.argv else Q
    trabajos = [(g, q) for g, qs in grupos.items() for q in qs if q not in c.get(g, {})]
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda gq: (gq[0], gq[1], buscar(gq[1])), trabajos))
    for g, q, (qq, out) in res:
        c.setdefault(g, {})[q] = out
    json.dump(c, open("_candidatos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    txt(c)
    print(len(trabajos), "busquedas -> _candidatos.txt")
