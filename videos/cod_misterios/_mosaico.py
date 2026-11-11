# -*- coding: utf-8 -*-
"""Mosaico barato de medios/ (10-nov-2026): un cuadro por clip (a 1/3 de su duración), 10×6 por hoja, número encima.
    python _mosaico.py [n1,n2,…]   → previews/mosaico_NN.jpg
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
MED = os.path.join(AQUI, "medios")
W, H, C, F = 256, 144, 10, 6
nums = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else list(range(1, 170))
fnt = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
hojas = [nums[i:i + C * F] for i in range(0, len(nums), C * F)]
for k, grupo in enumerate(hojas, 1):
    im = Image.new("RGB", (W * C, H * F), (0, 0, 0))
    for i, n in enumerate(grupo):
        r = os.path.join(MED, f"scene-{n:03d}.mp4")
        if not os.path.exists(r):
            continue
        try:
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", r],
                                     capture_output=True, text=True).stdout.strip() or 4)
        except ValueError:
            d = 4
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{d / 3:.2f}", "-i", r, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) == W * H * 3:
            im.paste(Image.frombytes("RGB", (W, H), raw), ((i % C) * W, (i // C) * H))
        ImageDraw.Draw(im).text(((i % C) * W + 6, (i // C) * H + 4), str(n), font=fnt, fill=(255, 230, 0), stroke_width=3, stroke_fill=(0, 0, 0))
    out = os.path.join(AQUI, "previews", f"mosaico_{k:02d}.jpg")
    im.save(out, quality=82)
    print(out)
