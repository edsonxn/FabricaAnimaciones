# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por escena -> _candidatos.json (10-nov-2026)."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

Q = {
    "intro": ["WoW Forever launch crowded starting zone", "WoW Forever Elwynn Forest gameplay no commentary", "World of Warcraft Forever cinematic trailer"],
    "friccion": ["WoW classic Barrens walking no commentary", "WoW Forever retail vs classic", "World of Warcraft retail dungeon finder speed"],
    "c30": ["WoW Forever character creation", "WoW Forever ruleset selection roleplay realm", "WoW classic roleplay tavern Goldshire"],
    "c29": ["WoW Forever general chat spanish", "WoW Forever preferred language setting", "WoW classic trade chat city"],
    "c28": ["WoW Forever all classes overview", "warlock summon ritual classic", "mage conjure water food classic", "druid cat form stealth classic"],
    "overgear": [],
    "burla0": ["WoW Forever group quest elite gameplay"],
    "c27": ["WoW classic reading quest text Duskwood", "WoW Forever new quests gameplay", "Westfall quest Saldean farm classic"],
    "burla1": ["WoW Forever Stormwind beggar", "WoW Forever addons"],
    "c26": ["WoW classic signpost crossroads", "WoW classic map exploring no addons", "Questie addon classic"],
    "c25": ["Hogger elite group kill classic", "WoW Forever Hogger", "Hogger Elwynn Forest classic"],
    "c24": ["WoW classic walking Elwynn to Westfall", "WoW classic gryphon flight Stormwind Ironforge", "WoW Forever flight master"],
    "c23": ["WoW classic zeppelin ride Orgrimmar Undercity", "WoW classic boat Menethil Theramore", "WoW classic zeppelin Grom'gol"],
    "c22": ["WoW Forever campfire camp", "WoW Forever camp tent buff", "WoW Forever The Great Outdoors quest"],
    "c21": ["WoW classic fishing Stormwind docks", "Stranglethorn fishing extravaganza classic", "WoW Forever fishing"],
    "c20": ["WoW classic auction house Stormwind", "WoW Forever merchant's favor crate", "WoW classic tailoring bags", "WoW classic cooking fish"],
    "c19": ["Deadmines classic full run", "Wailing Caverns classic full run", "WoW Forever dungeon group walk"],
    "c18": ["WoW Forever guild leveling", "WoW classic guild charter", "WoW Forever layering guild together"],
    "c17": ["WoW classic Goldshire inn", "WoW classic dance on table inn", "WoW classic rested xp inn"],
    "c16": ["warlock succubus quest classic", "shaman totem quests classic fire totem", "druid bear form quest Moonglade classic", "paladin mount quest classic"],
    "c15": ["hunter tame rare pet classic", "Broken Tooth tame classic Badlands", "hunter tame Humar classic"],
    "c14": ["Defias Brotherhood quest chain classic", "Edwin VanCleef Deadmines classic", "Westfall classic gameplay"],
    "c13": ["Duskwood night classic gameplay", "Stalvan Mistmantle quest classic", "Mor'Ladim Duskwood classic"],
    "c12": ["WoW classic rare elite spawn silver dragon", "Mother Fang rare classic", "WoW classic rare spawn Barrens"],
    "gracias1": ["WoW Forever Goldshire gameplay"],
    "c11": ["WoW classic exploring hidden places", "WoW Forever new zone exploration", "WoW classic mountain climbing"],
    "gracias2": ["WoW Forever Durotar gameplay"],
    "c10": ["horde lowbie run to Elwynn Forest", "level 1 run across world WoW classic", "WoW classic dying crossing Wetlands lowbie"],
    "c09": ["WoW classic ghost run corpse", "WoW classic spirit healer graveyard", "priest resurrect classic"],
    "c08": ["WoW Forever treasure hunt shipwreck", "WoW Forever This Must Be The Place quest", "WoW Forever treasure sack"],
    "c07": ["WoW Forever book reading", "WoW classic library books lore", "WoW Forever inn book glowing"],
    "c06": ["Tarren Mill vs Southshore world pvp classic", "Stranglethorn world pvp classic Nesingwary", "WoW Forever world pvp"],
    "burla2": ["Lakeshire Redridge classic gameplay"],
    "c05": ["Barrens chat Mankrik wife", "Mankrik's wife quest classic", "Barrens Crossroads classic"],
    "c04": ["Thunder Bluff elevator classic", "Ironforge bank classic players", "Stormwind canals classic"],
    "c03": ["WoW classic helping lowbie", "WoW classic buff strangers", "WoW Forever community"],
    "c02": ["WoW Forever new lighting comparison", "WoW Forever sunrise Elwynn", "WoW classic day night cycle Dun Morogh snow"],
    "c01": ["WoW Forever level 60 cap horizontal progression", "WoW Forever cozy gameplay no commentary", "WoW classic relaxing walk"],
    "cierre": ["WoW Forever gameplay no commentary", "WoW Forever Stormwind"],
}


def buscar(q):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(duration)s|%(channel)s|%(title)s", f"ytsearch6:{q}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
                       env=dict(__import__("os").environ, PYTHONIOENCODING="utf-8"))
    return q, [l.split("|", 3) for l in r.stdout.splitlines() if l.count("|") >= 3]


if __name__ == "__main__":
    pares = [(e, q) for e, qs in Q.items() for q in qs]
    with ThreadPoolExecutor(6) as ex:
        res = dict(ex.map(lambda p: buscar(p[1]), pares))
    out = {e: {q: res[q] for q in qs} for e, qs in Q.items()}
    json.dump(out, open("_candidatos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e, d in out.items():
        print("==", e)
        for q, l in d.items():
            for x in l[:6]:
                print("  ", x[0], (x[1] or "?")[:6], x[2][:22], "|", x[3][:80])
    sys.exit(0)
