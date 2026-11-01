# -*- coding: utf-8 -*-
"""Hoja de prueba de cuadros del video (tiempos GLOBALES), en paralelo:
    python _prueba.py 3 12.5 20.4 ...            -> previews/prueba.jpg (hoja 3 columnas, cuadros de 640x360)
    python _prueba.py --grande 12.5              -> previews/prueba_12.50.jpg a 1920x1080 (rigor)
    --sin-cache: dibuja todo desde cero (GR.CACHE = False), para comparar con las cachés de rendimiento
    --out nombre: previews/<nombre>.jpg en vez de prueba.jpg"""
import os
import sys
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)


def cuadro(t):
    import numpy as np
    import escenas
    import grabado as GR
    GR.CACHE = os.environ.get("FAB_SIN_CACHE") != "1"
    return t, (np.clip(escenas.cuadro(t), 0, 1) * 255).astype(np.uint8)


if __name__ == "__main__":
    import cv2
    import numpy as np
    grande = "--grande" in sys.argv
    if "--sin-cache" in sys.argv:
        os.environ["FAB_SIN_CACHE"] = "1"
    out = "prueba"
    if "--out" in sys.argv:
        out = sys.argv.pop(sys.argv.index("--out") + 1)
    ts = [float(a) for a in sys.argv[1:] if not a.startswith("--")]
    with Pool(min(len(ts), 8)) as p:
        res = dict(p.map(cuadro, ts))
    if grande:
        for t in ts:
            cv2.imwrite(f"previews/prueba_{t:.2f}.jpg", res[t][..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 92])
        print("ok")
        sys.exit()
    tiles = []
    for t in ts:
        im = cv2.resize(res[t], (640, 360), interpolation=cv2.INTER_AREA)[..., ::-1].copy()
        cv2.putText(im, f"{t:.2f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2)
        tiles.append(im)
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    filas = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
    cv2.imwrite(f"previews/{out}.jpg", np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(f"previews/{out}.jpg")
