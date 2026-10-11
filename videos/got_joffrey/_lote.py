# -*- coding: utf-8 -*-
"""Hoja de prueba de varias escenas: por cada plano, cuadros a `fr` de su duración (por defecto 0.5) -> previews/lote_<k>.jpg
(4 columnas, 480x270) y los PNG completos en previews/l_<escena>_<t>.png.
    python videos/got_joffrey/_lote.py [escena ...] [--fr 0.3,0.8] [--procs 3]"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

TL = json.load(open("timeline.json", encoding="utf-8"))
IDS = [e["id"] for e in TL["escenas"]]


def _uno(arg):
    eid, t = arg
    import escenas as S
    d = [e for e in TL["escenas"] if e["id"] == eid][0]
    esc = S.CLASES[eid](d, IDS.index(eid))
    t0 = time.time()
    im = (np.clip(esc.render(None, t), 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(f"previews/l_{eid}_{t:06.2f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    sm = cv2.resize(im, (480, 270), interpolation=cv2.INTER_AREA)
    for c, g in (((0, 0, 0), 3), ((255, 255, 255), 1)):
        cv2.putText(sm, f"{eid} {t:.1f} ({time.time() - t0:.0f}s)", (6, 262), cv2.FONT_HERSHEY_SIMPLEX, 0.45, c, g, cv2.LINE_AA)
    return sm


if __name__ == "__main__":
    a = sys.argv[1:]
    fr = [0.5]
    procs = 3
    if "--fr" in a:
        fr = [float(x) for x in a[a.index("--fr") + 1].split(",")]
    if "--procs" in a:
        procs = int(a[a.index("--procs") + 1])
    ids = [x for x in a if x in IDS] or IDS
    import escenas as S
    trabajos = []
    for eid in ids:
        d = [e for e in TL["escenas"] if e["id"] == eid][0]
        esc = S.CLASES[eid](d, IDS.index(eid))
        ts = [p.t0 for p in esc.planos] + [d["t1"]]
        for i in range(len(esc.planos)):
            for f in fr:
                trabajos.append((eid, ts[i] + (ts[i + 1] - ts[i]) * f))
    from multiprocessing import Pool
    with Pool(procs) as pool:
        tiles = pool.map(_uno, trabajos)
    while len(tiles) % 4:
        tiles.append(np.zeros_like(tiles[0]))
    filas = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]
    for k in range(0, len(filas), 6):
        cv2.imwrite(f"previews/lote_{k // 6}.jpg", cv2.cvtColor(np.vstack(filas[k:k + 6]), cv2.COLOR_RGB2BGR),
                    [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(len(trabajos), "cuadros ->", (len(filas) + 5) // 6, "hojas previews/lote_*.jpg")
