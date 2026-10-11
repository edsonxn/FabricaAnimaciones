# -*- coding: utf-8 -*-
"""Prueba del mapa con relieve: python _mk.py nombre lon lat z [lon lat z ...]  -> previews/<nombre>.jpg (hoja) """
import sys, time
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
import kz_mapa
M = kz_mapa.MAPA
nombre = sys.argv[1]
v = [float(a) for a in sys.argv[2:]]
cams = [tuple(v[i:i+3]) for i in range(0, len(v), 3)]
tiles = []
for c in cams:
    t0 = time.time()
    import os; img = M.base(c, 0.0, exag=float(os.environ.get("MK_EXAG","7")), rios_umbral=float(os.environ.get("MK_RIOS","1.5")))
    print(c, f"{time.time()-t0:.2f}s", flush=True)
    im = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    if len(cams) == 1:
        cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    tiles.append(cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA))
while len(tiles) % 2: tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i+2]) for i in range(0, len(tiles), 2)])
cv2.imwrite(f"previews/{nombre}.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
