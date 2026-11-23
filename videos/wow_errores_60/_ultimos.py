# -*- coding: utf-8 -*-
"""Hoja con el PRIMER y el ÚLTIMO cuadro (a 0,3 s del final) de cada clip de medios/: caza pantallas finales de youtubers
(«THANKS FOR WATCHING», «SUBSCRIBE») que la hoja normal no alcanza (el usuario, 12-nov-2026: se veía en el 4:10 de la v2).
  python _ultimos.py [ids separados por coma]   → previews/_ultimos_NN.jpg (40 clips por hoja)"""
import glob, os, subprocess, sys
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FF = r"C:\ffmpeg\bin"
clips = sorted(glob.glob("medios/scene-*.mp4"))
if len(sys.argv) > 1:
    q = {f"scene-{int(x):03d}" for x in sys.argv[1].split(",")}
    clips = [c for c in clips if os.path.basename(c)[:-4] in q]
W, H = 240, 135


def cuadro(f, t, final):
    args = [os.path.join(FF, "ffmpeg"), "-loglevel", "error"] + (["-sseof", str(-t)] if final else ["-ss", str(t)]) + \
           ["-i", f, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "image2pipe", "-vcodec", "png", "-"]
    import io
    r = subprocess.run(args, capture_output=True)
    try:
        return Image.open(io.BytesIO(r.stdout)).convert("RGB")
    except Exception:
        return Image.new("RGB", (W, H), (255, 0, 0))


por = 40
for h in range(0, len(clips), por):
    lote = clips[h:h + por]
    hoja = Image.new("RGB", (4 * (2 * W + 10), ((len(lote) + 3) // 4) * (H + 18)), (20, 20, 20))
    d = ImageDraw.Draw(hoja)
    for i, c in enumerate(lote):
        x, y = (i % 4) * (2 * W + 10), (i // 4) * (H + 18)
        hoja.paste(cuadro(c, .2, False), (x, y + 16))
        hoja.paste(cuadro(c, .3, True), (x + W, y + 16))
        d.text((x + 3, y + 2), os.path.basename(c)[6:-4] + "  inicio | final", fill=(255, 220, 120))
    out = f"previews/_ultimos_{h // por + 1:02d}.jpg"
    hoja.save(out, quality=82)
    print(out, len(lote))
