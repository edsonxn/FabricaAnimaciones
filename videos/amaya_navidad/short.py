# -*- coding: utf-8 -*-
"""Short vertical (1080x1920) de amaya_navidad: la PEOR n.º 1 y la MEJOR n.º 1 (p1 + m1 del MASTER, según timeline.json) dentro de un marco vichy
con el título en letras y el avatar de Amaya.  python short.py → salida/amaya_navidad_SHORT.mp4"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import coquette as C  # noqa: E402

T0, T1 = 508.8, 547.2
FF = r"C:\ffmpeg\bin\ffmpeg.exe"


def poner(base, rgba, cx, cy):
    h, w = rgba.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    a = rgba[..., 3:4]
    base[y0:y0 + h, x0:x0 + w] = base[y0:y0 + h, x0:x0 + w] * (1 - a) + rgba[..., :3] * a


fondo = np.ascontiguousarray(np.rot90(C.fondo("vichy_amaya", 0.0)))[:1920, :1080].copy()
for txt, y, px, col in (("Lo PEOR y lo MEJOR", 300, 92, C.ROSA_FUERTE), ("que pedir en Navidad", 420, 84, C.CIRUELA),
                        ("(el n.º 1 de cada lista)", 520, 50, C.CIRUELA)):
    poner(fondo, C.texto(txt, px=px, col=col, contorno=10), 540, y)
poner(fondo, C.texto("¡La lista completa en mi canal!", px=52, col=C.CIRUELA, contorno=8), 540, 1420)
av = C.sticker(os.path.join(AQUI, "propios", "amaya_avatar.png"), 460)
h, w = av.shape[:2]
y0, x0 = 1920 - h, 60
a = av[..., 3:4]
fondo[y0:, x0:x0 + w] = fondo[y0:, x0:x0 + w] * (1 - a) + av[..., :3] * a
for n, cx, cy in (("mono", 860, 1640), ("estrella", 980, 1500), ("cerezas", 900, 1800)):
    poner(fondo, C.sticker(os.path.join(AQUI, "stickers", n + ".png"), 150), cx, cy)
png = os.path.join(AQUI, "previews", "_short_marco.png")
Image.fromarray((np.clip(fondo, 0, 1) * 255).astype(np.uint8)).save(png)

master = next(os.path.join(AQUI, "salida", f) for f in os.listdir(os.path.join(AQUI, "salida")) if f.endswith("_MASTER.mp4"))
out = os.path.join(AQUI, "salida", "amaya_navidad_SHORT.mp4")
fc = "[0:v]scale=1080:608[v];[1:v][v]overlay=0:656:shortest=1,format=yuv420p[o];[0:a]afade=t=in:d=0.3,afade=t=out:st=%.2f:d=0.8[a]" % (T1 - T0 - 0.8)
subprocess.run([FF, "-y", "-v", "error", "-ss", str(T0), "-t", str(T1 - T0), "-i", master, "-loop", "1", "-i", png,
                "-filter_complex", fc, "-map", "[o]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
                "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
print("ok", out)
