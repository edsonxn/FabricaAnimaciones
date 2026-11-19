# -*- coding: utf-8 -*-
"""python fino.py <id> <t0> <t1> <paso> <salida.jpg>  — cuadros cada <paso> s de un video (8 por fila).
Baja primero el tramo a 360p (una sola descarga) y saca los cuadros del archivo local: sin cortes de YouTube."""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

vid, t0, t1, paso, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
tmp = tempfile.mkdtemp()
loc = os.path.join(tmp, "v.mp4")
subprocess.run(["yt-dlp", "-q", "--no-warnings", "-f", "18/best[height<=480][ext=mp4]/best[height<=480]", "--download-sections",
                f"*{max(0, t0 - 1)}-{t1 + 1}", "--force-keyframes-at-cuts", "-o", loc, f"https://youtu.be/{vid}"], check=False)
base = max(0, t0 - 1)
W, H = 240, 135
ts = []
t = t0
while t <= t1:
    ts.append(round(t, 1))
    t += paso
ims = []
for t in ts:
    p = subprocess.run([FF, "-loglevel", "error", "-ss", str(t - base), "-i", loc, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "image2pipe",
                        "-vcodec", "mjpeg", "-"], capture_output=True, timeout=60)
    from io import BytesIO
    try:
        ims.append(Image.open(BytesIO(p.stdout)).convert("RGB"))
    except Exception:
        ims.append(Image.new("RGB", (W, H)))
f = ImageFont.truetype("arial.ttf", 14)
L = Image.new("RGB", (8 * W, ((len(ts) + 7) // 8) * H))
d = ImageDraw.Draw(L)
for k, (t, im) in enumerate(zip(ts, ims)):
    x, y = (k % 8) * W, (k // 8) * H
    L.paste(im, (x, y))
    d.rectangle((x, y, x + 50, y + 17), fill=(0, 0, 0))
    d.text((x + 3, y + 1), f"@{t}", fill=(0, 255, 255), font=f)
L.save(out, quality=78)
print(out, len(ts), "ok" if os.path.exists(loc) else "SIN DESCARGA")
