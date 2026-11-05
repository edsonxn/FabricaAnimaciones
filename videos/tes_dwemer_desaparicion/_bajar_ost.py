# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para el video de los Dwemer (4-nov-2026): Morrowind y Skyrim de Jeremy
Soule (pistas que Tamriel no ha usado) + ESO de Brad Derrick (Greymoor: Blackreach; Morrowind).   python _bajar_ost.py  (desde la carpeta del video)
"""
import json
import os
import subprocess

PISTAS = {   # slug: id de YouTube (canal «Jeremy Soule - Topic» o «Brad Derrick - Topic»)
    "darkened_depths": "aeCoJBmm5Kc", "peaceful_waters": "dy6lfsOX6Yo", "bright_spears_dark_blood": "ArltGs6Wufk",
    "silt_sunrise": "Ap6RRLn6evQ", "shed_your_travails": "sSaOkWXEMsE", "blessing_of_vivec": "pDgL8atxuO4",
    "stormclouds_on_the_battlefield": "OdAQ3IKOVWg", "over_the_next_hill": "_59IYSMVSPw", "kynes_peace": "LbNMvsSRThw",
    "secunda": "VPgZFgOvJDE", "aurora": "SR1HOltzolY", "tundra": "sx3aFAfQrZA", "awake": "TIVpIo49WXo",
    "death_in_the_darkness": "GyxsKkhyqzc", "one_they_fear": "ez6jJHk3X4A", "sovngarde": "c6q2t2GSJb8",
    "unbroken_road": "PAhZIQvJdlY", "skyrims_dark_secret": "TwzmfBANRSs", "ashes_over_vvardenfell": "dUdV1njsfP4",
    "blackreach_rising": "W3sm-InatIQ",
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
