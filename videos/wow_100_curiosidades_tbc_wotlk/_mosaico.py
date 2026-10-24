# -*- coding: utf-8 -*-
"""Mosaico propio de clips concretos (un cuadro por clip, 5 columnas) para revisar los rehechos sin regenerar las 18 hojas.
Uso: python _mosaico.py 7,11,12,...  [salida.jpg]   → previews/mosaico_rehechos.jpg (y _2.jpg… cada 60 clips)
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
ids = [int(x) for x in sys.argv[1].split(",")]
base = sys.argv[2] if len(sys.argv) > 2 else "previews/mosaico_rehechos"
W, H, COLS, POR = 480, 270, 5, 60
font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
os.makedirs("previews/_mos", exist_ok=True)
for parte in range(0, len(ids), POR):
    lote = ids[parte:parte + POR]
    filas = (len(lote) + COLS - 1) // COLS
    hoja = Image.new("RGB", (COLS * W, filas * (H + 30)), (20, 20, 20))
    d = ImageDraw.Draw(hoja)
    for k, n in enumerate(lote):
        mp4 = f"medios/scene-{n:03d}.mp4"
        png = f"previews/_mos/{n:03d}.png"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "3", "-i", mp4, "-frames:v", "1", "-vf", f"scale={W}:{H}", png])
        x, y = (k % COLS) * W, (k // COLS) * (H + 30)
        if os.path.exists(png):
            hoja.paste(Image.open(png), (x, y))
        d.text((x + 6, y + H + 4), f"{n:03d}", fill=(255, 210, 60), font=font)
    out = f"{base}{'' if parte == 0 else '_' + str(parte // POR + 1)}.jpg"
    hoja.save(out, quality=82)
    print(out, len(lote))
