# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para «Las 10 builds más ROTAS» (10-nov-2026): pistas de
Skyrim (Jeremy Soule) que Tamriel NO ha usado aún (comprobado contra audio/ost de todos los tes_*).
Busca por nombre (ytsearch5) y se queda con el primer resultado de un canal «- Topic».   python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {   # slug: búsqueda — pistas de Skyrim/Dawnguard/Dragonborn que Tamriel NO ha usado (comprobado 10-nov contra todos los tes_*)
    "ancient_stones": "Jeremy Soule Ancient Stones Skyrim", "the_jerall_mountains": "Jeremy Soule The Jerall Mountains",
    "out_of_the_cold": "Jeremy Soule Out of the Cold Skyrim", "into_darkness": "Jeremy Soule Into Darkness Skyrim",
    "far_horizons": "Jeremy Soule Far Horizons Skyrim", "imperial_throne": "Jeremy Soule Imperial Throne",
    "under_an_ancient_sun": "Jeremy Soule Under an Ancient Sun", "steel_on_steel": "Jeremy Soule Steel on Steel",
    "death_or_sovngarde": "Jeremy Soule Death or Sovngarde", "dragonsreach": "Jeremy Soule Dragonsreach",
    "age_of_aggression": "Jeremy Soule Age of Aggression", "age_of_oppression": "Jeremy Soule Age of Oppression",
    "tooth_and_claw": "Jeremy Soule Tooth and Claw", "the_gathering_storm": "Jeremy Soule The Gathering Storm",
    "dawn": "Jeremy Soule Dawn Skyrim", "solitude": "Jeremy Soule Solitude Skyrim",
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
