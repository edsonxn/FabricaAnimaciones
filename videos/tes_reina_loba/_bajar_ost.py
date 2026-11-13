# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para «La Reina Loba» (12-nov-2026): historia de lore; Skyrim + Oblivion (Ciudad Imperial): pistas de
Skyrim (Jeremy Soule) que Tamriel NO ha usado aún (comprobado contra audio/ost de todos los tes_*).
Busca por nombre (ytsearch5) y se queda con el primer resultado de un canal «- Topic».   python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {   # historia de lore: ambiente y drama (Skyrim) + Ciudad Imperial / Septim (Oblivion)
    "reign_of_the_septims": "Jeremy Soule Reign of the Septims Oblivion", "harvest_dawn": "Jeremy Soule Harvest Dawn Oblivion",
    "wind_from_the_depths": "Jeremy Soule Wind from the Depths Oblivion", "king_and_country": "Jeremy Soule King and Country Oblivion",
    "auriels_ascension": "Jeremy Soule Auriel's Ascension Oblivion", "glory_of_cyrodiil": "Jeremy Soule Glory of Cyrodiil",
    "silence_unbroken": "Jeremy Soule Silence Unbroken Skyrim", "night_without_stars": "Jeremy Soule Night Without Stars",
    "silent_footsteps": "Jeremy Soule Silent Footsteps Skyrim", "kynes_peace": "Jeremy Soule Kyne's Peace",
    "secunda": "Jeremy Soule Secunda Skyrim", "aurora": "Jeremy Soule Aurora Skyrim", "frostfall": "Jeremy Soule Frostfall",
    "unbroken_road": "Jeremy Soule Unbroken Road", "masser": "Jeremy Soule Masser Skyrim", "tundra": "Jeremy Soule Tundra Skyrim",
    "journeys_end": "Jeremy Soule Journey's End Skyrim", "a_winters_tale": "Jeremy Soule A Winter's Tale Skyrim",
    "shattered_shields": "Jeremy Soule Shattered Shields", "blood_and_steel": "Jeremy Soule Blood and Steel Skyrim",
    "caught_off_guard": "Jeremy Soule Caught off Guard Skyrim", "watch_the_skies": "Jeremy Soule Watch the Skies Skyrim",
    "awake": "Jeremy Soule Awake Skyrim", "the_road_most_travelled": "Jeremy Soule The Road Most Travelled",
    "into_darkness": "Jeremy Soule Into Darkness Skyrim", "imperial_throne": "Jeremy Soule Imperial Throne",
    "solitude": "Jeremy Soule Solitude Skyrim", "dawn": "Jeremy Soule Dawn Skyrim", "the_gathering_storm": "Jeremy Soule The Gathering Storm",
}
OUT = os.path.join("audio", "ost")
os.makedirs(OUT, exist_ok=True)
ids = {}
for slug, q in PISTAS.items():
    dest = os.path.join(OUT, slug + ".wav")
    r = subprocess.run(["python", "-m", "yt_dlp", "--flat-playlist", "-J", f"ytsearch6:{q}"], capture_output=True, text=True,
                       encoding="utf-8")
    try:
        ents = json.loads(r.stdout).get("entries", [])
    except ValueError:
        ents = []
    ent = next((e for e in ents if "topic" in (e.get("channel") or e.get("uploader") or "").lower()), None)
    if not ent:
        print("x (sin Topic)", slug)
        continue
    ids[slug] = dict(id=ent["id"], titulo=ent.get("title"), canal=ent.get("channel"))
    if not os.path.exists(dest):
        subprocess.run(["python", "-m", "yt_dlp", "-q", "-x", "--audio-format", "wav", "-o", os.path.join(OUT, slug + ".%(ext)s"),
                        "https://youtu.be/" + ent["id"]], capture_output=True)
    print("ok" if os.path.exists(dest) else "x", slug, ent["id"], ent.get("title"), "|", ent.get("channel"))
json.dump(ids, open(os.path.join(OUT, "_ids.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
