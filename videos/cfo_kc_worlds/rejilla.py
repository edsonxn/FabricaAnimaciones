# -*- coding: utf-8 -*-
"""Cuadros con rejilla para medir la pizarra: python rejilla.py <n> <t1> <t2> ... [--ancho 960]
→ previews/cuadros/j<n>_<t>.jpg (rejilla de décimas con etiquetas; las posiciones del telestrador son fracción del cuadro)."""
import os, sys
import cv2

D = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
ancho = 960
if "--ancho" in a:
    i = a.index("--ancho"); ancho = int(a[i + 1]); a = a[:i] + a[i + 2:]
n, ts = a[0], [float(x) for x in a[1:]]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", f"j{n}.mp4"))
fps = cap.get(5)
out = os.path.join(D, "previews", "cuadros")
os.makedirs(out, exist_ok=True)
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, round(t * fps))
    ok, im = cap.read()
    if not ok:
        print("sin cuadro", t); continue
    h = round(ancho * 9 / 16)
    im = cv2.resize(im, (ancho, h))
    for k in range(1, 20):
        x = round(ancho * k / 20); y = round(h * k / 20)
        grueso = 1
        col = (0, 255, 255) if k % 2 == 0 else (0, 140, 140)
        cv2.line(im, (x, 0), (x, h), col, grueso); cv2.line(im, (0, y), (ancho, y), col, grueso)
        if k % 2 == 0:
            cv2.putText(im, f".{k // 2}", (x + 2, 12), 0, .4, (0, 255, 255), 1)
            cv2.putText(im, f".{k // 2}", (2, y - 2), 0, .4, (0, 255, 255), 1)
    cv2.putText(im, f"j{n} t={t:g}", (ancho - 150, h - 8), 0, .55, (255, 255, 255), 2)
    cv2.imwrite(os.path.join(out, f"j{n}_{t:g}.jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok", out)
