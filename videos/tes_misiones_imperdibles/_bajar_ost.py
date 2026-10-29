# -*- coding: utf-8 -*-
"""Baja a audio/ost/ las pistas de la OST oficial de Skyrim (Jeremy Soule - Topic) que NO sonaron en ningún video de la Fábrica en
Tamriel (28-oct-2026; regla: no repetir música ante el mismo público). Busca cada título y se queda con el resultado del canal
«Jeremy Soule - Topic».     python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {
    "ancient_stones": "Ancient Stones", "the_bannered_mare": "The Bannered Mare", "dawn": "Dawn",
    "the_frozen_hearth": "The Frozen Hearth", "chill_of_the_shadows": "Chill of the Shadows", "shattered_shields": "Shattered Shields",
    "far_horizons": "Far Horizons", "into_darkness": "Into Darkness", "out_of_the_cold": "Out of the Cold", "solitude": "Solitude",
    "silence_unbroken": "Silence Unbroken", "journeys_end": "Journey's End", "imperial_throne": "Imperial Throne",
    "beneath_the_ice": "Beneath the Ice", "standing_stones": "Standing Stones", "the_white_river": "The White River",
    "sky_above_voice_within": "Sky Above, Voice Within", "the_gathering_storm": "The Gathering Storm",
    "unbound": "Unbound", "skyrim_atmospheres": "Skyrim Atmospheres",
}
OUT = os.path.join("audio", "ost")
os.makedirs(OUT, exist_ok=True)
ids = {}
for slug, titulo in PISTAS.items():
    dest = os.path.join(OUT, slug + ".wav")
    if os.path.exists(dest):
        continue
    q = "ytsearch6:Jeremy Soule " + titulo.replace("'", "") + " Skyrim"
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", q], capture_output=True, text=True, encoding="utf-8")
    try:
        ent = json.loads(r.stdout)["entries"]
    except Exception:
        print("x", slug, "búsqueda falló"); continue
    elegido = None
    for e in ent:
        canal = (e.get("channel") or e.get("uploader") or "")
        if "Jeremy Soule" in canal and "Topic" in canal and titulo.lower().replace("'", "") in (e.get("title") or "").lower().replace("'", ""):
            elegido = e; break
    if not elegido:
        print("?", slug, [(e.get("title"), e.get("channel")) for e in ent[:3]]); continue
    ids[slug] = elegido["id"]
    subprocess.run(["yt-dlp", "-x", "--audio-format", "wav", "-o", os.path.join(OUT, slug + ".%(ext)s"),
                    "https://youtu.be/" + elegido["id"]], capture_output=True)
    print("ok" if os.path.exists(dest) else "x", slug, elegido["id"], elegido.get("title"))
json.dump(ids, open(os.path.join(OUT, "_ids.json"), "w", encoding="utf-8"), indent=1)
