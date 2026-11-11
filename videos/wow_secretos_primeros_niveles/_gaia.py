# -*- coding: utf-8 -*-
"""Clip PROPIO de la escena `gaia` (anuncio de Gaia Eterna): recortes del MASTER de la Crematoria a medios/scene-NNN.mp4,
con su AUDIO, de la duración exacta de cada beat. El beat donde cae el `post` de 13 s («…Escucha un pedazo.») se alinea para que
la voz callada coincida con 24,7 s del MASTER («Esa noche, un hijo le lanzó una espada maldita…» → «…historia de la Crematoria.»).
Además escribe sfx/oye_crematoria.mp3 (24,7-37,4 s) para la PISTA voz=True. Correr ANTES de `bajar` (bajar salta lo que existe).
  python _gaia.py   ·   python _gaia.py --ver"""
import json
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.abspath(os.path.join("..", "gaia_crematoria", "salida", "gaia_crematoria_MASTER.mp4"))
OYE, OYE_FIN = 24.7, 37.4
CLAVE = "gaia_4"                    # «Tiene otra narradora, otra música y el mismo cuidado. Escucha un pedazo.»
OTROS = [60.0, 140.0, 300.0, 420.0, 540.0, 660.0, 800.0]  # beats de `gaia` sin post: otros tramos del mismo MASTER (sin repetir)


def main(escribir=True):
    beats = json.load(open("beats.json", encoding="utf-8"))
    esc = json.load(open("_beat_escena.json", encoding="utf-8"))
    tl = json.load(open("timeline.json", encoding="utf-8"))
    tpost = {f["key"]: f["t1"] for e in tl["escenas"] for f in e["frases"]}[CLAVE] + .15
    k = 0
    for b in beats:
        dentro = b["t0"] <= tpost < b["t1"]
        if esc.get(b["id"]) != "gaia" and not dentro:
            continue
        dur = b["t1"] - b["t0"]
        if dentro:
            s = max(0.0, OYE - (tpost - b["t0"]))
        else:
            s = OTROS[min(k, len(OTROS) - 1)]
            k += 1
        print(f"{b['id']} {b['t0']:7.2f}-{b['t1']:7.2f} ({dur:4.1f} s) <- Crematoria desde {s:6.1f} s {'(OYE)' if dentro else ''}")
        if escribir:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s:.3f}", "-i", SRC, "-t", f"{dur:.3f}",
                            "-vf", "scale=1920:1080,fps=30", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac",
                            "-b:a", "192k", "-ar", "48000", os.path.join("medios", b["id"] + ".mp4")], check=True)
    if escribir:
        os.makedirs("sfx", exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{OYE}", "-to", f"{OYE_FIN}", "-i", SRC, "-vn",
                        "-af", "afade=t=in:d=0.15,afade=t=out:st=12.4:d=0.3", "-ar", "48000", "-b:a", "192k", "sfx/oye_crematoria.mp3"], check=True)


if __name__ == "__main__":
    os.makedirs("medios", exist_ok=True)
    main(escribir="--ver" not in sys.argv)
