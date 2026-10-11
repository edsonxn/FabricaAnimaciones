# -*- coding: utf-8 -*-
"""Miniatura PROVISIONAL por código (1280x720): la cabina negra encendida en el salón + titular. -> salida/miniatura.jpg
La definitiva del canal Edsonxn es con IA (ver prompt_miniatura.md)."""
import cv2
import numpy as np
from PIL import Image, ImageDraw

from arcade import *  # noqa: F401,F403
import tablero as T

t = 7.3
p = P()
salon(p, t, n=7, luz=0.8, neones=False)
p.rect(0, 0, W, H, (0.0, 0.0, 0.03), 0.35)
cx, cy, ch = 1380, 1130, 1150
cabina(p, cx, cy, ch, t, pant_formas, color=NEGRO, borde=(0.06, 0.06, 0.085), luz=VIOL, marq=(0.6, 0.25, 1.0), rotulo="POLYBIUS")
p.glow(cx, cy - ch * 0.68, 1100, (0.5, 0.28, 1.0), 0.30)
FIG = (0.015, 0.016, 0.03)
for k, (x, h, pelo) in enumerate(((930, 640, "corto"), (760, 590, "afro"))):
    j = persona(p, x, 1100, h, pose_estar(k * 2.0, lean=0.08), FIG, 1, pelo=pelo)
    hx, hy = x + j["hd"][0], 1100 - j["hd"][1]
    p.elip(hx + j["rc"] * 0.78, hy, j["rc"] * 0.16, j["rc"] * 0.85, 0, mix(VIOL, (1, 1, 1), 0.45), 0.9)      # filo de luz, no una cara en blanco
    p.linea((x + j["cu"][0] + h * 0.09, 1100 - j["cu"][1] + h * 0.03), (x + j["cu"][0] + h * 0.07, 1100 - j["cu"][1] + h * 0.22), h * 0.010, mix(VIOL, (1, 1, 1), 0.3), 0.7)
vineta_p(p, 0.5)
im = cv2.resize(np.clip(p.im * 1.25, 0, 1), (1280, 720), interpolation=cv2.INTER_CUBIC)
pil = Image.fromarray((im * 255).astype(np.uint8))
d = ImageDraw.Draw(pil)
f1, f2 = T.fnt("oswald", 150), T.fnt("oswald", 96)
for txt, y, f, col in (("NUNCA", 70, f1, (255, 235, 40)), ("EXISTIÓ", 225, f1, (255, 255, 255)), ("¿O SÍ?", 420, f2, (255, 70, 60))):
    d.text((60, y), txt, font=f, fill=col, stroke_width=10, stroke_fill=(0, 0, 0))
pil.save("salida/miniatura.jpg", quality=93)
print("ok salida/miniatura.jpg")
