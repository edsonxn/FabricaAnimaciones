# -*- coding: utf-8 -*-
"""Hoja de TODO el video: un cuadro cada `paso` s (previews/hoja_global_<k>.jpg, 6 columnas, 320x180)."""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)
import cv2, numpy as np
import escenas as S
TL = json.load(open("timeline.json", encoding="utf-8"))
paso = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
ini = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
fin = float(sys.argv[3]) if len(sys.argv) > 3 else TL["total"]
ids = [e["id"] for e in TL["escenas"]]
COLS = int(sys.argv[4]) if len(sys.argv) > 4 else 6
TW = int(sys.argv[5]) if len(sys.argv) > 5 else 320
FILAS = int(sys.argv[6]) if len(sys.argv) > 6 else 10
cache = {}
tiles = []
for t in np.arange(ini, fin, paso):
    d = [e for e in TL["escenas"] if e["t0"] <= t < e["t1"]][0]
    if d["id"] not in cache:
        cache[d["id"]] = S.CLASES[d["id"]](d, ids.index(d["id"]))
    img = cache[d["id"]].render(None, t)
    im = cv2.cvtColor((np.clip(img, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    sm = cv2.resize(im, (TW, TW * 9 // 16), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, f"{int(t // 60)}:{t % 60:04.1f} {d['id']}", (4, TW * 9 // 16 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 255), 1, cv2.LINE_AA)
    tiles.append(sm)
while len(tiles) % COLS:
    tiles.append(np.zeros_like(tiles[0]))
filas = [np.hstack(tiles[i:i + COLS]) for i in range(0, len(tiles), COLS)]
for k in range(0, len(filas), FILAS):
    cv2.imwrite(f"previews/hoja_global_{k // FILAS}.jpg", np.vstack(filas[k:k + FILAS]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print(len(tiles), "cuadros")
