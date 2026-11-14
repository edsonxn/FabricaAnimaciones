# -*- coding: utf-8 -*-
"""Hojas de revisión con 2 cuadros por clip (1 s y 6 s): previews/clips_NN.jpg (12 clips por hoja, 4 columnas de pares).
    python _hoja_clips.py [012,015,...]     sin argumento: todos"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
MED = os.path.join(AQUI, "medios")
TMP = os.path.join(AQUI, "previews", "_cuadros")
os.makedirs(TMP, exist_ok=True)
W, H = 400, 225


def cuadro(clip, t):
    out = os.path.join(TMP, f"{clip}_{t}.jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", os.path.join(MED, clip + ".mp4"), "-frames:v", "1",
                    "-vf", f"scale={W}:{H}", "-pix_fmt", "yuvj420p", "-strict", "-1", out], check=False)
    return out


def main():
    clips = sorted(f[:-4] for f in os.listdir(MED) if f.startswith("scene-") and f.endswith(".mp4"))
    if len(sys.argv) > 1:
        quiero = {f"scene-{int(x):03d}" for x in sys.argv[1].split(",")}
        clips = [c for c in clips if c in quiero]
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda a: cuadro(*a), [(c, t) for c in clips for t in (1, 6)]))
    f = ImageFont.truetype("arial.ttf", 22)
    por = 12
    for h in range(0, len(clips), por):
        grupo = clips[h:h + por]
        lien = Image.new("RGB", (4 * (2 * W + 10), 3 * (H + 4)), (0, 0, 0))
        d = ImageDraw.Draw(lien)
        for i, c in enumerate(grupo):
            x, y = (i % 4) * (2 * W + 10), (i // 4) * (H + 4)
            for k, t in enumerate((1, 6)):
                p = os.path.join(TMP, f"{c}_{t}.jpg")
                if os.path.exists(p):
                    lien.paste(Image.open(p), (x + k * W, y))
            d.rectangle((x, y, x + 70, y + 28), fill=(0, 0, 0))
            d.text((x + 4, y + 2), c[-3:], fill=(255, 255, 0), font=f)
        n = f"clips_{h // por + 1:02d}.jpg" if len(sys.argv) == 1 else f"rehechos_{h // por + 1:02d}.jpg"
        lien.save(os.path.join(AQUI, "previews", n), quality=80)
        print("previews/" + n)


if __name__ == "__main__":
    main()
