# -*- coding: utf-8 -*-
"""Cuadros sueltos a tamaño completo: python _cuadro.py <escena> t1 t2 ... -> previews/c_<escena>_<t>.png (varios procesos)"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

TL = json.load(open("timeline.json", encoding="utf-8"))
IDS = [e["id"] for e in TL["escenas"]]


def _uno(a):
    eid, t = a
    import escenas as S
    d = [e for e in TL["escenas"] if e["id"] == eid][0]
    esc = S.CLASES[eid](d, IDS.index(eid))
    im = (np.clip(esc.render(None, t), 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(f"previews/c_{eid}_{t:06.2f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    return t


if __name__ == "__main__":
    eid = sys.argv[1]
    from multiprocessing import Pool
    with Pool(4) as p:
        print(p.map(_uno, [(eid, float(x)) for x in sys.argv[2:]]))
