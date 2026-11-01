# -*- coding: utf-8 -*-
"""Vistas rápidas mientras se arma el video (pedido del usuario, 20-oct-2026: «quiero ver el montaje mientras vas armando»).
  python _vivo.py hoja t1 t2 ...        → previews/_hoja.jpg (cuadros de 640x360 con su tiempo)
  python _vivo.py video [fps] [procs] [t0 t1]   → previews/montaje_vivo.mp4 (960x540, con la voz y la mezcla si ya existen;
                                                con t0 t1 solo ese tramo → previews/montaje_<t0>-<t1>.mp4)"""
import glob
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw

OUT = "previews"


def _cuadro(t, ancho):
    import escenas as S
    img = S.render_mundo(t)
    im = Image.fromarray((img * 255).round().astype(np.uint8))
    return im.resize((ancho, int(ancho * 9 / 16)), Image.LANCZOS)


def hoja(ts):
    cols = 3 if len(ts) > 4 else len(ts)
    w, h = 640, 360
    filas = (len(ts) + cols - 1) // cols
    M = Image.new("RGB", (cols * w, filas * h))
    for i, t in enumerate(ts):
        im = _cuadro(t, w)
        ImageDraw.Draw(im).text((6, h - 16), f"{t:.1f}s", fill=(255, 255, 0))
        M.paste(im, ((i % cols) * w, (i // cols) * h))
    M.save(os.path.join(OUT, "_hoja.jpg"), quality=86)
    print(os.path.join(OUT, "_hoja.jpg"))


def _trozo(args):
    k0, k1, fps, t0 = args
    for k in range(k0, k1):
        _cuadro(t0 + k / fps, 960).save(os.path.join(OUT, "_vivo", f"{k:05d}.jpg"), quality=88)
    return k1 - k0


def video(fps=12, procs=6, t0=0.0, t1=None):
    import json
    total = json.load(open("timeline.json", encoding="utf-8"))["total"]
    t1 = total if t1 is None else min(t1, total)
    n = int((t1 - t0) * fps)
    os.makedirs(os.path.join(OUT, "_vivo"), exist_ok=True)
    for f in glob.glob(os.path.join(OUT, "_vivo", "*.jpg")):
        os.remove(f)
    paso = max(1, n // (procs * 4))
    with Pool(procs) as p:
        p.map(_trozo, [(a, min(a + paso, n), fps, t0) for a in range(0, n, paso)])
    salida = os.path.join(OUT, "montaje_vivo.mp4" if t0 == 0 and t1 >= total else f"montaje_{int(t0)}-{int(t1)}.mp4")
    audio = next((a for a in ("audio/final.wav", "audio/mezcla.wav", "audio/voz.wav") if os.path.exists(a)), None)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(OUT, "_vivo", "%05d.jpg")]
    if audio:
        cmd += ["-ss", f"{t0:.3f}", "-i", audio, "-c:a", "aac", "-b:a", "160k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "30", "-preset", "slow", salida]   # < 30 MB: llega al teléfono
    subprocess.run(cmd, check=True)
    print(salida, n, "cuadros", "audio:", audio)


if __name__ == "__main__":
    if sys.argv[1] == "hoja":
        hoja([float(x) for x in sys.argv[2:]])
    else:
        a = sys.argv[2:]
        video(int(a[0]) if a else 12, int(a[1]) if len(a) > 1 else 6, *(float(x) for x in a[2:4]))
