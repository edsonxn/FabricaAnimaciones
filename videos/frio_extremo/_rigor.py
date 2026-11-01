# -*- coding: utf-8 -*-
"""Rigor del MASTER: un cuadro cada `paso` s en hojas de 4x4 (480x270) → previews/rigor_NN.jpg, más blackdetect y freezedetect.
Uso (desde la carpeta del video): python _rigor.py [paso=3]"""
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
M = glob.glob("salida/*_MASTER.mp4")[0]
paso = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
tmp = "previews/_rigor"
os.makedirs(tmp, exist_ok=True)
for f in glob.glob(tmp + "/*.jpg"):
    os.remove(f)
subprocess.run([FF, "-loglevel", "error", "-i", M, "-vf", f"fps=1/{paso},scale=480:270", "-q:v", "4", tmp + "/%04d.jpg"], check=True)
fs = sorted(glob.glob(tmp + "/*.jpg"))
for h in range(0, len(fs), 16):
    S = Image.new("RGB", (4 * 480, 4 * 270))
    for k, f in enumerate(fs[h:h + 16]):
        im = Image.open(f)
        t = (h + k) * paso + paso / 2
        ImageDraw.Draw(im).text((5, 252), f"{int(t // 60)}:{t % 60:04.1f}", fill=(255, 255, 0))
        S.paste(im, ((k % 4) * 480, (k // 4) * 270))
    S.save(f"previews/rigor_{h // 16:02d}.jpg", quality=82)
print(len(fs), "cuadros,", (len(fs) + 15) // 16, "hojas")
for filtro in ("blackdetect=d=0.5:pix_th=0.08", "freezedetect=n=0.002:d=2.2"):
    r = subprocess.run([FF, "-hide_banner", "-i", M, "-vf", filtro, "-an", "-f", "null", "-"], capture_output=True, text=True)
    print(filtro.split("=")[0], [l.split("]")[-1].strip() for l in r.stderr.splitlines() if "black_" in l or "freeze_" in l][:40])
