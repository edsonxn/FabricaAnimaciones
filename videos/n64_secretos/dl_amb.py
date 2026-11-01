# -*- coding: utf-8 -*-
"""Rehace clips CON audio con el segundo exacto (ffmpeg -ss por entrada, video y audio alineados).
   python dl_amb.py 104,143 [--prueba]   -> lee busquedas.json (url, desde) y beats.json; escribe medios/scene-NNN.mp4 (o scratchpad con --prueba)"""
import json, os, subprocess, sys, re, shutil
AQ = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(os.path.abspath(__file__))
bs = {b["id"]: b for b in json.load(open(os.path.join(AQ, "beats.json"), encoding="utf-8"))}
bq = json.load(open(os.path.join(AQ, "busquedas.json"), encoding="utf-8"))
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
prueba = "--prueba" in sys.argv
def sec(vid, desde, L, fmt, nombre, tmpd):
    subprocess.run(["yt-dlp", f"https://www.youtube.com/watch?v={vid}", "-f", fmt, "--download-sections", f"*{desde:.2f}-{desde + L + 1.0:.2f}",
                    "--force-keyframes-at-cuts", "-o", os.path.join(tmpd, nombre + ".%(ext)s"), "--no-warnings", "--no-playlist", "--quiet"],
                   capture_output=True, text=True, env=env, timeout=300)
    c = [f for f in os.listdir(tmpd) if f.startswith(nombre + ".") and not f.endswith(".part")]
    return os.path.join(tmpd, c[0]) if c else None
for n in [int(x) for x in sys.argv[1].split(",")]:
    sid = f"scene-{n:03d}"; b = bs[sid]; e = bq[sid]
    vid = re.search(r"youtu\.be/([\w-]{11})", e["url"]).group(1); desde = float(e["desde"])
    L = round(b["t1"] - b["t0"] + 0.3, 3)
    tmpd = os.path.join(S, "medios", "_escaneo", "_tmp_" + sid); os.makedirs(tmpd, exist_ok=True)
    for f in os.listdir(tmpd): os.remove(os.path.join(tmpd, f))
    vu = sec(vid, desde, L, "bv*[height<=1080][height>=720][vcodec^=avc1]/bv*[height<=1080][height>=720]", "v", tmpd)
    au = sec(vid, desde, L, "ba", "a", tmpd)
    if not (vu and au): print(sid, "sin descarga", vu, au); continue
    out = os.path.join(S, "medios", "_escaneo", f"{sid}_prueba.mp4") if prueba else os.path.join(AQ, "medios", sid + ".mp4")
    tmp = os.path.join(tmpd, f"_out_{sid}.mp4")
    vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vu, "-i", au, "-t", f"{L:.3f}",
        "-map", "0:v:0", "-map", "1:a:0", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", tmp], capture_output=True, text=True)
    if r.returncode or not os.path.exists(tmp): print(sid, "ffmpeg", r.stderr[-200:]); continue
    shutil.move(tmp, out)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(sid, vid, desde, "L", L, "->", d, "s", out)
    shutil.rmtree(tmpd, ignore_errors=True)
