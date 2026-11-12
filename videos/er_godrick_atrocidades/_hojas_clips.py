# -*- coding: utf-8 -*-
"""Mosaico de revisión de clips: 3 cuadros por clip (20/50/85 %) con el id, 12 clips por hoja → previews/clips_NN.jpg.
    python _hojas_clips.py [scene-001 scene-002 ...]
"""
import glob
import os
import sys

import cv2
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
fs = sorted(glob.glob(os.path.join(AQUI, "medios", "scene-*.mp4")))
if len(sys.argv) > 1:
    fs = [f for f in fs if os.path.basename(f)[:-4] in sys.argv[1:]]
W, H = 320, 180
fuente = ImageFont.truetype("arialbd.ttf", 20)
POR = 12
for h in range((len(fs) + POR - 1) // POR):
    lote = fs[h * POR:(h + 1) * POR]
    hoja = Image.new("RGB", (W * 3 * 2, H * ((len(lote) + 1) // 2)), (20, 20, 20))
    for i, f in enumerate(lote):
        cap = cv2.VideoCapture(f)
        n = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        for j, p in enumerate((.2, .5, .85)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * p))
            ok, fr = cap.read()
            if not ok:
                continue
            im = Image.fromarray(cv2.cvtColor(cv2.resize(fr, (W, H)), cv2.COLOR_BGR2RGB))
            hoja.paste(im, ((i % 2) * W * 3 + j * W, (i // 2) * H))
        d = ImageDraw.Draw(hoja)
        d.text(((i % 2) * W * 3 + 6, (i // 2) * H + 4), os.path.basename(f)[6:9], font=fuente, fill=(255, 255, 0),
               stroke_width=2, stroke_fill=(0, 0, 0))
    hoja.save(os.path.join(AQUI, "previews", f"clips_{h:02d}.jpg"), quality=78)
print("hojas:", (len(fs) + POR - 1) // POR)
