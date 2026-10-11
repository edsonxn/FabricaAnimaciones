import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "nucleo"))
import cv2, numpy as np
from noir_fondos import Lienzo, edificio
t0 = time.time()
L = Lienzo(2400, 1500, origen=(0, -1000), sem=3)
x = 20
for i, (tp, an, al) in enumerate([("ladrillo", 300, 900), ("deco", 260, 1700), ("tienda", 340, 600), ("cristal", 280, 2100), ("ladrillo", 240, 1100), ("tienda", 360, 700)]):
    edificio(L, x, 480, an, al, tipo=tp, sem=i + 5)
    x += an + 70
c = L.capa()
print("pintado", round(time.time() - t0, 1), "s")
img = (c.g.astype(np.float32) * (c.a / 255.0)).astype(np.uint8)
os.makedirs("videos/ia_noir/previews", exist_ok=True)
cv2.imwrite("videos/ia_noir/previews/prueba_ciudad.jpg", cv2.resize(img, (1200, 750)))
cv2.imwrite("videos/ia_noir/previews/_crop.png", img[700:1500, 0:1200])
