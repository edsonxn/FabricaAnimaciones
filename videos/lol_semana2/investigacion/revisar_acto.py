# -*- coding: utf-8 -*-
"""Revisión barata del MP4 del acto: pistas, silencios, negros y hoja de la jugada dada (previews/rev_<frase>.jpg).
python videos/lol_semana2/investigacion/revisar_acto.py kccf_j_2"""
import json
import os
import re
import subprocess
import sys

FF, PR = r"C:\ffmpeg\bin\ffmpeg.exe", r"C:\ffmpeg\bin\ffprobe.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP4 = os.path.join(D, "salida", "lol_semana2_ACTO_A.mp4")
tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
print("timeline", tl["total"], "· MP4", round(os.path.getsize(MP4) / 1e9, 2), "GB")
print(subprocess.run([PR, "-v", "error", "-show_entries", "stream=codec_type,duration,width,height", "-of", "csv=p=0", MP4], capture_output=True, text=True).stdout)
r = subprocess.run([FF, "-hide_banner", "-i", MP4, "-map", "0:a", "-af", "silencedetect=n=-38dB:d=1.5", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
print("silencios > 1,5 s:", re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", r) or "ninguno")
r = subprocess.run([FF, "-hide_banner", "-i", MP4, "-map", "0:v", "-vf", "fps=2,scale=160:-1,blackdetect=d=1:pix_th=.08", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
print("negros:", re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r) or "ninguno")
for k in sys.argv[1:]:
    f = next(x for e in tl["escenas"] for x in e["frases"] if x["key"] == k)
    t0, t1 = f["t0"], f["t1"]
    os.makedirs(os.path.join(D, "previews"), exist_ok=True)
    salida = os.path.join(D, "previews", f"rev_{k}.jpg")
    paso = (t1 - t0) / 12
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t0:.2f}", "-i", MP4, "-t", f"{t1 - t0:.2f}", "-vf", f"fps=1/{paso:.3f},scale=640:-1,tile=4x3",
                    "-frames:v", "1", "-q:v", "4", salida], check=True)
    print(k, f"{t0:.1f}-{t1:.1f} s ({int(t0 // 60)}:{int(t0 % 60):02d}) →", salida)
