# -*- coding: utf-8 -*-
"""Rejilla 4x4 de un cuadro por toma (t0 + 1.3 s): python _hoja2.py  ->  previews/rej_N.jpg"""
import sys, time
import cv2, numpy as np
import escenas as S
from escena_base import TL
m = S.CLASES[TL["escenas"][0]["id"]](TL["escenas"][0], 0)
ts = []
for d in S.SHOTS:
    ts.append((d["t0"] + min(1.3, (d["t1"] - d["t0"]) * 0.6), d["t0"]))
ini = int(sys.argv[1]) if len(sys.argv) > 1 else 0
fin = int(sys.argv[2]) if len(sys.argv) > 2 else len(ts)
sel = ts[ini:fin]
t00 = time.time()
ims = []
for t, t0 in sel:
    f = m.render(None, t)
    f8 = cv2.cvtColor((np.clip(f, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    f8 = cv2.resize(f8, (480, 270), interpolation=cv2.INTER_AREA)
    cv2.putText(f8, f"{t:.1f}", (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    ims.append(f8)
while len(ims) % 4: ims.append(np.zeros_like(ims[0]))
for k in range(0, len(ims), 16):
    blk = ims[k:k + 16]
    while len(blk) % 4: blk.append(np.zeros_like(blk[0]))
    hoja = np.vstack([np.hstack(blk[i:i + 4]) for i in range(0, len(blk), 4)])
    cv2.imwrite(f"previews/rej_{ini + k // 1 // 1}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 90])
print("listo", len(sel), "cuadros", round(time.time() - t00), "s")
