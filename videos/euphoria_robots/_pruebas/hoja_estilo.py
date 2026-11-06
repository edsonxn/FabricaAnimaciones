"""Hoja de prueba del estilo: python _pruebas/hoja_estilo.py momento:u ... -> previews/hoja_estilo.jpg"""
import os, sys
os.environ["FAB_RESPALDO"] = "1"
sys.path.insert(0, ".")
import cv2, numpy as np
import escenas as E
tomas = [a.split(":") for a in sys.argv[1:]]
from motor import Lienzo
lz = Lienzo()
ims = []
for nom, u in tomas:
    img = E.pinta(lz, nom, float(u))
    im = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.putText(im, f"{nom} {u}", (20, 60), 0, 1.6, (255, 255, 255), 3)
    ims.append(cv2.resize(im, (540, 960), interpolation=cv2.INTER_AREA))
while len(ims) % 3: ims.append(np.zeros_like(ims[0]))
filas = [np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]
cv2.imwrite("previews/hoja_estilo.jpg", np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", len(tomas))
