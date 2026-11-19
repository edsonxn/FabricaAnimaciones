# -*- coding: utf-8 -*-
"""Clip de archivo < 720p como VENTANA DE ARCHIVO (docs/estilo_secuencia_yt.md § METRAJE DE ARCHIVO < 720p):
    python _archivo.py N ID DESDE [DUR]   → medios/scene-NNN.mp4 (1920x1080, 30 fps; clip a 860 px con marco ámbar sobre él mismo
                                           desenfocado). DUR por defecto = duración del beat + 0,6 s.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
n, vid, desde = int(sys.argv[1]), sys.argv[2], float(sys.argv[3])
bs = {b["id"]: b for b in json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))}
b = bs[f"scene-{n:03d}"]
dur = float(sys.argv[4]) if len(sys.argv) > 4 else b["t1"] - b["t0"] + 0.6
arch = os.path.join(AQUI, "medios", "_archivo")
os.makedirs(arch, exist_ok=True)
raw = os.path.join(arch, vid + ".mp4")
if not os.path.exists(raw):
    subprocess.run(["yt-dlp", "-q", "-f", "bv*+ba/b", "--merge-output-format", "mp4", "-o", raw, "https://youtu.be/" + vid], check=True)
fc = ("[0:v]trim=start={d}:duration={t},setpts=PTS-STARTPTS,fps=30,split[a][b];"
      "[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=24:2,eq=brightness=-0.22[bg];"
      "[b]scale=-2:860,pad=iw+16:ih+16:8:8:color=0xE0A030[fg];"
      "[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]").format(d=desde, t=dur)
out = os.path.join(AQUI, "medios", f"scene-{n:03d}.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
                "-af", f"atrim=start={desde}:duration={dur},asetpts=PTS-STARTPTS", "-c:v", "libx264", "-crf", "18",
                "-preset", "veryfast", "-c:a", "aac", "-shortest", out], check=True)
f = os.path.join(AQUI, "fuentes.json")
fu = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
fu[f"scene-{n:03d}"] = {"video": vid, "desde": desde, "titulo": "(archivo < 720p, ventana)", "canal": "", "q": "", "_archivo": True}
json.dump(fu, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
q = os.path.join(AQUI, "busquedas.json")
bq = json.load(open(q, encoding="utf-8"))
bq[f"scene-{n:03d}"] = {"url": "https://youtu.be/" + vid, "desde": desde, "_archivo": True}
json.dump(bq, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, round(dur, 2), "s")
