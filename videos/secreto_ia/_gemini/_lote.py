# -*- coding: utf-8 -*-
"""Hoja de varias escenas a la vez: python _lote.py esc1 esc2 ... [--n 8]  -> previews/lote.jpg (n cuadros repartidos por escena,
uno a mitad de cada tramo; 480x270 cada uno, una fila por escena). Imprime los errores sin detenerse."""
import json, os, sys, time, traceback
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)
import cv2
import numpy as np
import escenas as S

TL = json.load(open("timeline.json", encoding="utf-8"))
n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 8
ids = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
filas = []
for eid in ids:
    d = [e for e in TL["escenas"] if e["id"] == eid][0]
    try:
        esc = S.CLASES[eid](d, [e["id"] for e in TL["escenas"]].index(eid))
    except Exception:
        traceback.print_exc(); continue
    dur = d["t1"] - d["t0"]
    fila = []
    for k in range(n):
        u = dur * (k + 0.5) / n
        try:
            t0 = time.time()
            img = esc.render(None, d["t0"] + u)
            dt = time.time() - t0
            im = (np.clip(img, 0, 1) * 255).astype(np.uint8)
        except Exception:
            print("ERROR", eid, round(u, 2)); traceback.print_exc()
            im = np.zeros((1080, 1920, 3), np.uint8); dt = 0
        sm = cv2.resize(im, (480, 270), interpolation=cv2.INTER_AREA)
        for col, gr in (((0, 0, 0), 3), ((255, 255, 255), 1)):
            cv2.putText(sm, f"{eid} u={u:.1f} {dt * 1000:.0f}ms", (6, 262), cv2.FONT_HERSHEY_SIMPLEX, 0.45, col, gr, cv2.LINE_AA)
        fila.append(sm)
    filas.append(np.vstack([np.hstack(fila[i:i + 4]) for i in range(0, len(fila), 4)]))
if filas:
    w = max(f.shape[1] for f in filas)
    hoja = np.vstack(filas)
    for k in range(0, len(filas), 2):
        cv2.imwrite(f"previews/lote_{k // 2}.jpg", cv2.cvtColor(np.vstack(filas[k:k + 2]), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", len(filas))
