# hojas.py <video> <ini_s> <fin_s> <paso_s> <salida_prefijo> [cols=4 rows=4]
import cv2, sys, numpy as np
v, ini, fin, paso, pref = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cols = int(sys.argv[6]) if len(sys.argv)>6 else 4
rows = int(sys.argv[7]) if len(sys.argv)>7 else 4
cap = cv2.VideoCapture(v)
fps = cap.get(cv2.CAP_PROP_FPS)
ts = np.arange(ini, fin, paso)
per = cols*rows
for k in range(0, len(ts), per):
    tiles = []
    for t in ts[k:k+per]:
        cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
        ok, f = cap.read()
        if not ok: f = np.zeros((360,534,3),np.uint8)
        f = cv2.resize(f,(480,270))
        h, m, s = int(t//3600), int(t%3600//60), int(t%60)
        cv2.putText(f, f"{int(t)}s {h}:{m:02d}:{s:02d}", (6,22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,0,0), 4)
        cv2.putText(f, f"{int(t)}s {h}:{m:02d}:{s:02d}", (6,22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,255), 1)
        tiles.append(f)
    while len(tiles)<per: tiles.append(np.zeros((270,480,3),np.uint8))
    grid = np.vstack([np.hstack(tiles[r*cols:(r+1)*cols]) for r in range(rows)])
    cv2.imwrite(f"{pref}_{int(ts[k]):05d}.jpg", grid, [cv2.IMWRITE_JPEG_QUALITY, 80])
print("ok")
