# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp ytsearch, sin bajar) candidatos de gameplay por escena -> _candidatos.json (10-nov-2026)."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

Q = {
    "intro": ["WoW Forever launch gameplay", "WoW Forever level 30 gameplay", "World of Warcraft Forever leveling 30 60"],
    "c20": ["Green Hills of Stranglethorn pages classic", "Nesingwary expedition stranglethorn classic", "Booty Bay WoW Forever"],
    "c19": ["WoW classic quest log full grey quests", "WoW Forever quest log", "Desolace WoW classic gameplay"],
    "overgear": [],
    "c18": ["WoW classic spirit healer resurrection sickness", "Tanaris WoW Forever gameplay", "Gadgetzan WoW classic"],
    "c17": ["WoW classic flight master Gadgetzan", "WoW Forever flight path", "Everlook Winterspring classic"],
    "c16": ["Stranglethorn Vale world pvp classic", "WoW Forever world pvp Stranglethorn", "Grom'gol zeppelin classic"],
    "c15": ["Whipper Root Tuber Felwood classic", "Felwood WoW classic gameplay", "Songflower Serenade classic"],
    "c14": ["WoW classic level 40 plate mail warrior trainer", "weapon master classic wow", "Edgemaster's Handguards classic"],
    "c13": ["Triage quest first aid classic Hammerfall", "First aid 300 classic triage", "WoW Forever first aid"],
    "c12": ["WoW Forever dual spec", "WoW classic talent respec cost", "Zul'Farrak dungeon classic"],
    "c11": ["WoW classic mithril ore farming Arathi", "WoW classic first mount level 40", "auction house WoW Forever"],
    "c10": ["Ravager Herod Scarlet Armory classic", "Whitemane Scarlet Cathedral classic", "WoW Forever itemization expertise"],
    "c09": ["Scarlet Key Doan library classic", "Shadowforge Key Dark Iron Legacy Franclorn", "Gahz'rilla Zul'Farrak mallet classic"],
    "c08": ["Linken quest chain Un'Goro classic", "It's Dangerous to Go Alone Linken", "Sunken Temple classic dungeon"],
    "c07": ["Timbermaw Hold tunnel classic", "Timbermaw reputation farming classic Felwood", "Winterspring classic gameplay"],
    "c06": ["Argent Dawn Commission scourgestones classic", "Western Plaguelands classic gameplay", "Light's Hope Chapel classic"],
    "c05": ["Sunken Temple class quests classic", "Azshara classic gameplay", "Swamp of Sorrows classic"],
    "c04": ["WoW classic level 50 quest gap", "Blackrock Depths classic gameplay", "WoW Forever Alcaz Island Prison dungeon"],
    "c03": ["Scholomance key quest classic Araj", "Krinkle Goodsteel Gadgetzan skeleton key", "Scholomance classic gameplay"],
    "c02": ["WoW Forever Riverglades zone", "WoW Forever Krol'dok Stronghold", "WoW Forever Drowned City dungeon", "WoW Forever Shen'dralas"],
    "c01": ["Onyxia attunement classic Windsor escort", "Warlord Goretooth Kargath Onyxia attunement", "WoW Forever Onyxia Barrow Deeps Hyjal raid"],
    "cierre": ["WoW Forever world first 60", "WoW Forever gameplay", "WoW Forever raid overview"],
    "gracias1": ["WoW Forever Elwynn gameplay"], "gracias2": ["WoW Forever Orgrimmar gameplay"], "burla1": ["WoW Forever retail vs classic"],
}


def buscar(q):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(duration)s|%(channel)s|%(title)s", f"ytsearch6:{q}"],
                       capture_output=True, text=True, encoding="utf-8", timeout=120)
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
