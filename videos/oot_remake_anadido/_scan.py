# -*- coding: utf-8 -*-
"""Hoja de contacto de un video de YouTube SIN bajarlo entero: python _scan.py <id> <salida.jpg> t1 t2 ... | a:b:paso
Un cuadro a 360p por segundo pedido (ffmpeg -ss sobre la URL del stream), con el segundo impreso. Para elegir el `desde` de cada beat."""
import os, subprocess, sys
import cv2, numpy as np

vid, out = sys.argv[1], sys.argv[2]
ts = []
for a in sys.argv[3:]:
    if ":" in a:
        x, y, p = map(float, a.split(":"))
        while x <= y:
            ts.append(x); x += p
    else:
        ts.append(float(a))
url = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height<=360]/b[height<=360]/worst", f"https://youtu.be/{vid}"],
                     capture_output=True, text=True).stdout.split("\n")[0].strip()
if not url:
    sys.exit("sin URL de stream")
minis = []
for t in ts:
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", url, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True)
    img = cv2.imdecode(np.frombuffer(r.stdout, np.uint8), cv2.IMREAD_COLOR) if r.stdout else None
    m = np.zeros((216, 384, 3), np.uint8) if img is None else cv2.resize(img, (384, 216))
    cv2.putText(m, f"{vid[:5]} {t:.0f}", (6, 208), cv2.FONT_HERSHEY_SIMPLEX, .6, (90, 214, 255), 2, cv2.LINE_AA)
    minis.append(m)
minis += [np.zeros_like(minis[0])] * (-len(minis) % 5)
cv2.imwrite(out, np.vstack([np.hstack(minis[i:i + 5]) for i in range(0, len(minis), 5)]))
print(out, len(ts))
