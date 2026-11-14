# -*- coding: utf-8 -*-
"""Utilidades de revisión.  python _util.py solapes | palabras | hoja <mp4> <sal.jpg> [n]"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

A = Path(__file__).parent


def solapes():
    ts = [4.3, 4.8, 5.2, 5.6, 6.0, 6.4, 6.8, 7.1, 14.9, 15.3, 15.9, 16.3, 18.9, 19.3, 19.9, 20.5]
    h = Image.new("RGB", (360 * 8, 275 * 2))
    for k, t in enumerate(ts):
        im = Image.open(A / f"fuente/cuadros/c_{int(t * 30) + 1:04d}.jpg").resize((360, 275))
        h.paste(im, ((k % 8) * 360, (k // 8) * 275))
    h.save(A / "previews/solapes.jpg", quality=80)


def palabras():
    d = json.load(open(A / "fuente/palabras.json", encoding="utf-8"))
    print(" ".join(f"{p['w']}@{p['t0']}" for p in d["palabras"] if p["t0"] < 20.7))


def hoja(mp4, sal, n=12, cols=6):
    """n cuadros repartidos, cada uno a 270x480."""
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]).decode().strip())
    filas = (n + cols - 1) // cols
    h = Image.new("RGB", (270 * cols, 480 * filas))
    for k in range(n):
        t = dur * (k + 0.5) / n
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=270:480", str(A / "previews/_t.jpg")], check=True)
        h.paste(Image.open(A / "previews/_t.jpg"), ((k % cols) * 270, (k // cols) * 480))
    h.save(sal, quality=85)
    print(sal)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "solapes":
        solapes()
    elif c == "palabras":
        palabras()
    else:
        hoja(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 12)
