# -*- coding: utf-8 -*-
"""Tiras de 5 cuadros por clip (violencia y rehechos, 24-nov-2026): python _tiras.py 50,92 [salida] -> previews/tiras_<salida>.jpg"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H, N = 240, 135, 5
nums = [int(x) for x in sys.argv[1].split(",")]
nom = sys.argv[2] if len(sys.argv) > 2 else "x"
fnt = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
im = Image.new("RGB", (W * N, H * len(nums)), (0, 0, 0))
for f, n in enumerate(nums):
    r = os.path.join(AQUI, "medios", f"scene-{n:03d}.mp4")
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", r],
                             capture_output=True, text=True).stdout.strip() or 4)
    for k in range(N):
        t = d * (k + .5) / N
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", r, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) == W * H * 3:
            im.paste(Image.frombytes("RGB", (W, H), raw), (k * W, f * H))
        ImageDraw.Draw(im).text((k * W + 4, f * H + 2), f"{n} {t:.1f}s", font=fnt, fill=(255, 230, 0), stroke_width=2,
                                stroke_fill=(0, 0, 0))
out = os.path.join(AQUI, "previews", f"tiras_{nom}.jpg")
im.save(out, quality=80)
print(out, im.size)
