# -*- coding: utf-8 -*-
"""Banco de SFX de Skyrim (regla del usuario, 29-oct-2026): videos cortos de un solo sonido, recortados al tramo con señal.
    python nucleo/datos/sfx_juego/skyrim/_bajar.py        baja lo que falte y deja <slug>.wav + _fuentes.txt"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
SONIDOS = {"mision_iniciada": "Skyrim quest start sound effect", "mision_completada": "Skyrim quest complete sound effect",
           "subir_nivel": "Skyrim level up sound effect", "lugar_descubierto": "Skyrim location discovered sound effect",
           "monedas": "Skyrim gold coins sound effect", "grito": "Skyrim Fus Ro Dah sound effect"}
fuentes = {}
for slug, q in SONIDOS.items():
    dest = os.path.join(AQUI, slug + ".wav")
    if os.path.exists(dest):
        continue
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "ytsearch8:" + q], capture_output=True, text=True, encoding="utf-8")
    ent = [e for e in json.loads(r.stdout)["entries"] if (e.get("duration") or 999) <= 40]
    if not ent:
        print("x", slug, "sin video corto"); continue
    e = ent[0]
    tmp = os.path.join(AQUI, "_" + slug + ".wav")
    subprocess.run(["yt-dlp", "-q", "-x", "--audio-format", "wav", "-o", os.path.join(AQUI, "_" + slug + ".%(ext)s"), "https://youtu.be/" + e["id"]], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16",
                    "-ar", "48000", "-t", "6", dest], capture_output=True)
    if os.path.exists(tmp):
        os.remove(tmp)
    fuentes[slug] = {"id": e["id"], "titulo": e.get("title"), "canal": e.get("channel") or e.get("uploader"), "dur": e.get("duration")}
    print("ok" if os.path.exists(dest) else "x", slug, e["id"], e.get("title"), e.get("duration"))
json.dump(fuentes, open(os.path.join(AQUI, "_fuentes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
