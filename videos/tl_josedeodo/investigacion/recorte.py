# Recorta y amplía una zona de un cuadro 1920x1080 con rejilla en fracciones: python recorte.py <img> <x0> <y0> <x1> <y1> <salida> [ancho=1280]
import sys, cv2
im = cv2.imread(sys.argv[1]); H, W = im.shape[:2]
x0, y0, x1, y1 = [float(v) for v in sys.argv[2:6]]; out = sys.argv[6]; w = int(sys.argv[7]) if len(sys.argv) > 7 else 1280
c = im[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)].copy()
s = w / c.shape[1]; c = cv2.resize(c, (w, int(c.shape[0] * s)))
import numpy as np
for k in range(0, 101, 5):
    f = k / 100
    if x0 <= f <= x1:
        x = int((f - x0) * W * s); cv2.line(c, (x, 0), (x, c.shape[0]), (0, 255, 255) if k % 10 == 0 else (0, 140, 140), 1)
        if k % 10 == 0: cv2.putText(c, f".{k:02d}" if k < 100 else "1", (x + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
    if y0 <= f <= y1:
        y = int((f - y0) * H * s); cv2.line(c, (0, y), (c.shape[1], y), (0, 255, 255) if k % 10 == 0 else (0, 140, 140), 1)
        if k % 10 == 0: cv2.putText(c, f".{k:02d}", (2, y - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
cv2.imwrite(out, c); print(out)
