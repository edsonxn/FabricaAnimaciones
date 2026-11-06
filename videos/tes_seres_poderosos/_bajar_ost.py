# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para «Los 20 seres más poderosos» (5-nov-2026): pistas de Oblivion,
Morrowind y Skyrim (Jeremy Soule) que Tamriel NO ha usado aún (comprobado contra audio/ost de todos los tes_*).
Busca por nombre (ytsearch5) y se queda con el primer resultado de un canal «- Topic».   python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {   # slug: búsqueda
    "watchmans_ease": "Jeremy Soule Watchman's Ease", "through_the_valleys": "Jeremy Soule Through the Valleys",
    "harvest_dawn": "Jeremy Soule Harvest Dawn", "wind_from_the_depths": "Jeremy Soule Wind from the Depths",
    "king_and_country": "Jeremy Soule King and Country", "fall_of_the_hammer": "Jeremy Soule Fall of the Hammer",
    "glory_of_cyrodiil": "Jeremy Soule Glory of Cyrodiil", "peace_of_akatosh": "Jeremy Soule Peace of Akatosh",
    "auriels_ascension": "Jeremy Soule Auriel's Ascension", "minstrels_lament": "Jeremy Soule Minstrel's Lament",
    "death_knell": "Jeremy Soule Death Knell", "defending_the_gate": "Jeremy Soule Defending the Gate",
    "call_of_magic": "Jeremy Soule Call of Magic", "the_road_most_travelled": "Jeremy Soule The Road Most Travelled",
    "sunrise_of_flutes": "Jeremy Soule Sunrise of Flutes", "dusk_at_the_market": "Jeremy Soule Dusk at the Market",
    "tension": "Jeremy Soule Tension Oblivion", "alls_well": "Jeremy Soule All's Well",
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
