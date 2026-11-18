# -*- coding: utf-8 -*-
"""Banco de SFX de Fallout 4 (Radio Yermo, fo_nunca_f4, 17-nov-2026; receta de cod/_bajar.py): videos cortos de un solo sonido, recortados al tramo con señal.
    python nucleo/datos/sfx_juego/fallout4/_bajar.py        baja lo que falte y deja <slug>.wav + _fuentes.txt"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
SONIDOS = {"subir_nivel": "Fallout 4 level up sound effect", "mision_completada": "Fallout 4 quest complete sound effect",
           "lugar_descubierto": "Fallout 4 location discovered sound effect", "geiger": "Fallout 4 geiger counter radiation sound effect",
           "pipboy": "Fallout 4 pip-boy sound effect", "vats": "Fallout 4 VATS sound effect",
           "logro": "Fallout 4 achievement unlocked sound", "terminal": "Fallout 4 terminal typing sound effect"}
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
viejo = json.load(open(os.path.join(AQUI, "_fuentes.json"), encoding="utf-8")) if os.path.exists(os.path.join(AQUI, "_fuentes.json")) else {}
fuentes = {**viejo, **fuentes}
json.dump(fuentes, open(os.path.join(AQUI, "_fuentes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
