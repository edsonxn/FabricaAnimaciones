# -*- coding: utf-8 -*-
"""Baja a audio/ost/ las pistas de la OST oficial de Skyrim (Jeremy Soule - Topic) que NO sonaron en tes_cosas_inutiles ni en
tes_armas_poderosas (regla: no repetir música ante el mismo público). Busca cada título y se queda con el resultado del canal
«Jeremy Soule - Topic».     python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {
    "from_past_to_present": "From Past to Present", "jerall_mountains": "The Jerall Mountains",
    "silent_footsteps": "Silent Footsteps", "dragonsreach": "Dragonsreach", "watch_the_skies": "Watch the Skies",
    "masser": "Masser", "distant_horizons": "Distant Horizons", "wind_guide_you": "Wind Guide You",
    "streets_of_whiterun": "The Streets of Whiterun", "around_the_fire": "Around the Fire",
    "seven_thousand_steps": "Seven Thousand Steps", "imminence": "Imminence", "tooth_and_claw": "Tooth and Claw",
    "under_an_ancient_sun": "Under an Ancient Sun", "towers_and_shadows": "Towers and Shadows",
    "night_without_stars": "Night Without Stars", "frostfall": "Frostfall", "a_winters_tale": "A Winter's Tale",
    "caught_off_guard": "Caught off Guard", "the_city_gates": "The City Gates", "before_the_storm": "Before the Storm",
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
