# -*- coding: utf-8 -*-
"""Mosaico de clips sueltos: python _hoja_nuevos.py 118 122 123 ...  -> previews/clips_nuevos.jpg (2 cuadros por clip)"""
import subprocess, sys
from PIL import Image, ImageDraw
ids = [int(a) for a in sys.argv[1:]]
W, H = 320, 180
cols = 4
rows = (len(ids) + cols - 1) // cols
hoja = Image.new("RGB", (cols * W, rows * 2 * H))
for k, i in enumerate(ids):
    f = f"medios/scene-{i:03d}.mp4"
    r = subprocess.run(["C:/ffmpeg/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    d = float(r.stdout.strip() or 8)
    for j, frac in enumerate((.25, .75)):
        o = "previews/_t.jpg"
        subprocess.run(["C:/ffmpeg/bin/ffmpeg", "-y", "-v", "error", "-ss", str(d * frac), "-i", f, "-frames:v", "1", "-vf", f"scale={W}:{H}", o], stdin=subprocess.DEVNULL)
        im = Image.open(o).convert("RGB")
        ImageDraw.Draw(im).text((4, 4), f"{i} {d:.1f}s", fill=(255, 255, 0))
        hoja.paste(im, ((k % cols) * W, ((k // cols) * 2 + j) * H))
hoja.save("previews/clips_nuevos.jpg", quality=82)
