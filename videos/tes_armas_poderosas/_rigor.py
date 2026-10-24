# -*- coding: utf-8 -*-
"""Rigor del MASTER: un cuadro cada PASO s (cada uno con su propio -ss, para no saltarse tramos) en hojas 8x6 con la hora
(previews/master_NN.jpg) + blackdetect y freezedetect (previews/master_detect.txt).   python _rigor.py [paso]"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(AQUI, "salida", "tes_armas_poderosas_MASTER.mp4")
TMP = os.path.join(AQUI, "previews", "_master")
os.makedirs(TMP, exist_ok=True)
PASO = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
W, H = 480, 270


def dur():
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", M], capture_output=True,
                       text=True)
    return float(r.stdout.strip())


def cuadro(t):
    out = os.path.join(TMP, f"{t:07.1f}.jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", M, "-frames:v", "1", "-vf", f"scale={W}:{H}", out])
    return t, out


def main():
    D = dur()
    ts = [3 + k * PASO for k in range(int((D - 3) // PASO) + 1)]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(cuadro, ts))
    f = ImageFont.truetype("arial.ttf", 22)
    por = 48
    for h in range(0, len(res), por):
        g = res[h:h + por]
        lien = Image.new("RGB", (8 * W, 6 * H), (0, 0, 0))
        d = ImageDraw.Draw(lien)
        for i, (t, p) in enumerate(g):
            x, y = (i % 8) * W, (i // 8) * H
            if os.path.exists(p):
                lien.paste(Image.open(p), (x, y))
            else:
                d.text((x + 10, y + 100), "FALTA", fill=(255, 0, 0), font=f)
            d.rectangle((x, y, x + 92, y + 28), fill=(0, 0, 0))
            d.text((x + 4, y + 2), f"{int(t // 60)}:{t % 60:04.1f}", fill=(255, 255, 0), font=f)
        n = os.path.join(AQUI, "previews", f"master_{h // por + 1:02d}.jpg")
        lien.save(n, quality=80)
        print(n, f"{g[0][0]:.0f}-{g[-1][0]:.0f} s")
    print(f"duración {D:.1f} s, último cuadro {ts[-1]:.1f} s")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", M, "-vf", "blackdetect=d=0.25:pix_th=0.06,freezedetect=n=0.003:d=2", "-an",
                        "-f", "null", "-"], capture_output=True, text=True)
    lineas = [l for l in r.stderr.splitlines() if "black_start" in l or "freeze_start" in l or "freeze_duration" in l]
    open(os.path.join(AQUI, "previews", "master_detect.txt"), "w", encoding="utf-8").write("\n".join(lineas))
    print("\n".join(lineas) or "sin negros ni congelados")


if __name__ == "__main__":
    main()
