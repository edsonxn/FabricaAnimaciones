# -*- coding: utf-8 -*-
"""Coordenadas de Wowpedia ({{coords|x|y}}, coordenadas de zona del juego = fracción del mapa de Wowhead) para las paradas
de Rasganorte (tramo 7, 26-oct-2026). Escribe _coords.json y lo imprime.
    python _coords.py [Título ...]     (sin títulos: la lista de abajo)
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (coords)"}
API = "https://wowpedia.fandom.com/api.php?"

PAGINAS = [
    # Tundra Boreal
    "Warsong Hold", "Garrosh Hellscream", "Varok Saurfang", "Archdruid Lathorius", "D.E.H.T.A. Encampment",
    "Fizzcrank Airstrip", "Gearmaster Mechazod", "Keristrasza", "The Nexus", "Transitus Shield", "Amber Ledge",
    "Taunka'le Village",
    # Fiordo Aquilonal
    "Nifflevar", "Utgarde Keep", "Ingvar the Plunderer", "New Agamand",
    # Cementerio de Dragones
    "Wyrmrest Temple", "Galakrond's Rest", "Naxxramas", "Wintergarde Keep", "Angrathar the Wrathgate", "Wrathgate",
    "Orik Trueheart", "Forgotten Shore", "Frostmourne Cavern", "New Hearthglen", "Grand General Abbendis",
    "Obsidian Dragonshrine", "Azure Dragonshrine", "Ruby Dragonshrine", "Emerald Dragonshrine", "Bronze Dragonshrine",
    # Colinas Pardas
    "Grizzlemaw", "Vordrassil", "Ursoc", "Westfall Brigade Encampment", "Gryan Stoutmantle", "Silverbrook",
    "Bloodmoon Isle", "Shade of Arugal", "Drakil'jin Ruins", "Drak'Tharon Keep",
    # Zul'Drak
    "Har'koa", "Altar of Har'koa", "Altar of Rhunok", "Altar of Quetz'lun", "Altar of Sseratus", "Altar of Akali",
    "Altar of Mam'toth", "Gymer", "Drakuru", "Voltarus", "Amphitheater of Anguish",
    # Sholazar
    "Avatar of Freya", "The Avalanche", "Makers' Overlook", "Makers' Perch", "Nesingwary Base Camp", "Loque'nahak",
    "Rainspeaker Canopy", "Frenzyheart Hill",
    # Cumbres Tormentosas
    "K3", "Brunnhildar Village", "Temple of Storms", "Thorim", "Frosthold", "Ulduar", "Time-Lost Proto-Drake",
    # Canto de Cristal / Conquista / Corona
    "Dalaran", "Windrunner's Overlook", "Sunreaver's Command", "Wintergrasp Fortress", "Vault of Archavon",
    "Argent Tournament Grounds", "Sindragosa's Fall", "Onslaught Harbor", "High General Abbendis", "Orgrim's Hammer",
    "The Skybreaker", "Crusaders' Pinnacle", "Icecrown Citadel", "Crusader Bridenbrad", "The Silent Vigil",
]


def wikitext(titulo):
    q = dict(action="query", titles=titulo, prop="revisions", rvprop="content", rvslots="main", redirects=1, format="json")
    r = json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(q), headers=UA), timeout=40))
    for p in r["query"]["pages"].values():
        if "revisions" in p:
            return p["revisions"][0]["slots"]["main"]["*"]
    return ""


def main(titulos):
    sal = {}
    for t in titulos or PAGINAS:
        try:
            w = wikitext(t)
        except Exception as e:                       # noqa: BLE001
            print("ERROR", t, e)
            continue
        cs = re.findall(r"\{\{\s*co(?:ords)?\s*\|\s*([\d.]+)\s*[|,]\s*([\d.]+)([^}]*)\}\}", w, re.I)
        loc = re.search(r"\|\s*(?:location|loc)\s*=\s*([^\n]+)", w)
        sal[t] = dict(coords=[(float(a), float(b), c.strip("| ")[:40]) for a, b, c in cs][:6],
                      loc=(loc.group(1)[:140] if loc else ""))
        print(f"{t:32s} {sal[t]['coords'][:4]}  · {sal[t]['loc'][:90]}")
    ruta = os.path.join(AQUI, "_coords.json")
    viejo = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    viejo.update(sal)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(viejo, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
