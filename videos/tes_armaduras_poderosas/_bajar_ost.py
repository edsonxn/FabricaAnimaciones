# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para «Las 20 ARMADURAS más poderosas» (18-nov-2026): pistas de
Skyrim (Jeremy Soule) que Tamriel NO ha usado aún (comprobado contra audio/ost de todos los tes_*).
Busca por nombre (ytsearch5) y se queda con el primer resultado de un canal «- Topic».   python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {   # 18-nov: pistas de combate/forja que Tamriel NO ha usado (contra audio/ost de todos los tes_* y la lista de builds); 28 min ≈ 22 secciones
    "shattered_shields": "Jeremy Soule Shattered Shields Skyrim", "blood_and_steel": "Jeremy Soule Blood and Steel Skyrim",
    "sky_above_voice_within": "Jeremy Soule Sky Above Voice Within", "silence_unbroken": "Jeremy Soule Silence Unbroken Skyrim",
    "beyond_the_wall": "Jeremy Soule Beyond the Wall Skyrim", "journeys_end": "Jeremy Soule Journeys End Skyrim",
    "around_the_fire": "Jeremy Soule Around the Fire Skyrim", "a_chance_meeting": "Jeremy Soule A Chance Meeting Skyrim",
    "kyne_and_sovngarde": "Jeremy Soule Out of the Cold Skyrim", "ancient_stones": "Jeremy Soule Ancient Stones Skyrim",
    "the_jerall_mountains": "Jeremy Soule The Jerall Mountains", "into_darkness": "Jeremy Soule Into Darkness Skyrim",
    "far_horizons": "Jeremy Soule Far Horizons Skyrim", "imperial_throne": "Jeremy Soule Imperial Throne",
    "under_an_ancient_sun": "Jeremy Soule Under an Ancient Sun", "steel_on_steel": "Jeremy Soule Steel on Steel",
    "dragonsreach": "Jeremy Soule Dragonsreach", "tooth_and_claw": "Jeremy Soule Tooth and Claw",
    "the_gathering_storm": "Jeremy Soule The Gathering Storm", "dawn": "Jeremy Soule Dawn Skyrim",
    "solitude": "Jeremy Soule Solitude Skyrim", "silent_footsteps": "Jeremy Soule Silent Footsteps Skyrim",
    "one_they_fear": "Jeremy Soule One They Fear Skyrim", "caught_off_guard": "Jeremy Soule Caught Off Guard Skyrim",
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
