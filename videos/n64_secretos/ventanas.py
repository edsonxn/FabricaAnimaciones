# -*- coding: utf-8 -*-
"""Clips de VENTANA para n64_secretos (receta «METRAJE DE ARCHIVO < 720p» de docs/estilo_secuencia_yt.md, ampliada): cuando la fuente trae
barras, paneles laterales o la imagen duplicada (3D lado a lado), se recorta la zona buena y se coloca a alto completo sobre ella misma
desenfocada y oscurecida a cuadro entero. Baja SOLO el tramo (yt-dlp --download-sections, ≥ 720p) y arma medios/scene-NNN.mp4 (30 fps, sin audio).
    python ventanas.py 20,21,30      (los números de beat; todo lo definido en VENT si no se pasan)
crop = (x, y, w, h) en fracciones del cuadro; estira = factor horizontal (2 para el 3D lado a lado: media imagen se estira al doble).
"""
import json
import os
import shutil
import subprocess
import sys

AQ = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(AQ, "medios", "_escaneo", "_vent")
bs = {b["id"]: b for b in json.load(open(os.path.join(AQ, "beats.json"), encoding="utf-8"))}
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

VENT = {
    # beat: (id YouTube, desde, crop, estira)
    20: ("Hz8mW7DrOxY", 1500, (.25, 0, .75, 1), 1),   # Virtual Gaming Library: todos los juegos de N64 (panel izq. con la portada fuera)
    21: ("Hz8mW7DrOxY", 2400, (.25, 0, .75, 1), 1),
    30: ("Hz8mW7DrOxY", 3000, (.25, 0, .75, 1), 1),
    36: ("Cy2PqdndtXE", 57, (.21, 0, .58, 1), 1),     # Excitebike (NES) en columna central
    39: ("Cy2PqdndtXE", 200, (.21, 0, .58, 1), 1),
    83: ("vVE1d2gBcSM", 24, (0, 0, .5, 1), 2),         # Killer Instinct arcade grabado en 3D lado a lado: media imagen estirada
}


def bajar(vid, desde, L):
    d = os.path.join(TMP, vid + f"_{int(desde)}")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for fmt in ("bv*[height<=1080][height>=720][vcodec^=avc1]/bv*[height<=1080][height>=720]",):
        subprocess.run(["yt-dlp", f"https://www.youtube.com/watch?v={vid}", "-f", fmt, "--download-sections", f"*{desde:.2f}-{desde + L + 1.5:.2f}",
                        "--force-keyframes-at-cuts", "-o", os.path.join(d, "v.%(ext)s"), "--no-warnings", "--no-playlist", "--quiet"],
                       capture_output=True, text=True, env=env, timeout=400)
    c = [f for f in os.listdir(d) if f.startswith("v.") and not f.endswith(".part")]
    return os.path.join(d, c[0]) if c else None


def armar(n):
    sid = f"scene-{n:03d}"
    vid, desde, (cx, cy, cw, ch), est = VENT[n]
    L = round(bs[sid]["t1"] - bs[sid]["t0"] + 0.3, 3)
    v = bajar(vid, desde, L)
    if not v:
        print(sid, "sin descarga")
        return
    crop = f"crop=iw*{cw}:ih*{ch}:iw*{cx}:ih*{cy}"
    if est != 1:
        crop += f",scale=iw*{est}:ih"
    fg_h = 1080
    fc = (f"[0:v]{crop},setsar=1,split[a][b];"
          f"[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=28:6,eq=brightness=-0.18[bg];"
          f"[b]scale=-2:{fg_h}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[o]")
    out = os.path.join(AQ, "medios", sid + ".mp4")
    tmp = os.path.join(os.path.dirname(v), "_o.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-t", f"{L:.3f}", "-filter_complex", fc, "-map", "[o]", "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", tmp], capture_output=True, text=True)
    if r.returncode or not os.path.exists(tmp):
        print(sid, "ffmpeg", r.stderr[-300:])
        return
    shutil.move(tmp, out)
    shutil.rmtree(os.path.dirname(v), ignore_errors=True)
    print(sid, vid, desde, "->", out)


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    nums = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else sorted(VENT)
    for n in nums:
        armar(n)
