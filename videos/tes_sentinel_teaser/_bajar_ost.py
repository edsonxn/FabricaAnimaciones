# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para el video de Sentinel (3-nov-2026): música de Hammerfell en ESO
(Brad Derrick), temas de la saga (Jeremy Soule) y lo que no sonó antes en Tamriel.   python _bajar_ost.py  (desde la carpeta del video)
"""
import json
import os
import subprocess

PISTAS = {   # slug: id de YouTube (canal «Brad Derrick - Topic» o «Jeremy Soule - Topic»)
    "sands_of_the_alikr": "j4YkcBOguu4", "a_land_of_war_and_poetry": "yr3vo1_Ozx4", "tombs_unremembered": "uMXmpgtIJcA",
    "past_defines_the_future": "kEgunVKfNDU", "even_paradise_has_shadows": "pnrdXWbHKkI", "virtue_betrayal": "gZLLMl7BAH4",
    "beauty_of_dawn": "X1pl8pskQ2Q", "through_gates_of_flame": "YRbX9IZxapU", "weapons_drawn": "pzzFFWgdfxM",
    "hinterlands": "teDJQfN1tYU", "reign_of_the_septims": "y-jNCOn4-SA", "nerevar_rising": "0lfCUSB4p6g",
    "isles_of_the_starry_dream": "VO0mBylS2Yk",
}
OUT = os.path.join("audio", "ost")
os.makedirs(OUT, exist_ok=True)
for slug, vid in PISTAS.items():
    dest = os.path.join(OUT, slug + ".wav")
    if not os.path.exists(dest):
        subprocess.run(["python", "-m", "yt_dlp", "-q", "-x", "--audio-format", "wav", "-o", os.path.join(OUT, slug + ".%(ext)s"),
                        "https://youtu.be/" + vid], capture_output=True)
    print("ok" if os.path.exists(dest) else "x", slug, vid)
json.dump(PISTAS, open(os.path.join(OUT, "_ids.json"), "w", encoding="utf-8"), indent=1)
