"""python _era_test.py <id> p1 p2 ...   (p en pulsos locales; genera previews/era_<id>.jpg y un png por cuadro)"""
import sys, time, importlib
import numpy as np, cv2
import escena_base
from motor import Lienzo, a_uint8, W, H
import era as ER
import efectos as E
CLASES = {}
for m in ("epocas1", "epocas2", "epocas3", "epocas4"):
    try:
        mod = importlib.import_module(m)
    except ModuleNotFoundError:
        continue
    for n in dir(mod):
        c = getattr(mod, n)
        if isinstance(c, type) and issubclass(c, ER.Era) and c is not ER.Era:
            CLASES[n.lower()] = c
ids = [x[0] for x in ER.TABLA]
eid = sys.argv[1]
k = ids.index(eid)
cls = {n: c for n, c in CLASES.items() if n == eid or n == eid.replace("_", "")}
cl = cls.get(eid) or [c for n, c in CLASES.items() if n.startswith(eid[:4])][0]
era = cl(k)
lz = Lienzo()
tiles = []
for p in sys.argv[2:]:
    t = era.a(float(p))
    t0 = time.time()
    img = ER.img_era(lz, era, t)
    img = E.acabado(img, int(t * 10))
    im = a_uint8(np.clip(img, 0, 1))
    print(p, f"{t:.2f}s", f"{1000*(time.time()-t0):.0f} ms")
    cv2.imwrite(f"previews/era_{eid}_{float(p):04.1f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    sm = cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, f"p{p}", (8, 630), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    tiles.append(sm)
while len(tiles) % 4: tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i+4]) for i in range(0, len(tiles), 4)])
cv2.imwrite(f"previews/era_{eid}.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
