# Lee el reloj/marcador/banner de una fuente local o cuadros completos con rejilla.
# python al_tira.py tira <clip> <salida> t1 t2 ...   -> previews/cuadros/al_<salida>.jpg (franja superior-central de cada t, apilada)
# python al_tira.py rej  <clip> <salida> t           -> previews/cuadros/al_<salida>.jpg (cuadro completo 1280 px con rejilla 0,1)
import sys, os, cv2, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "..", "previews", "cuadros")
modo, clip, sal = sys.argv[1], sys.argv[2], sys.argv[3]
ts = [float(x) for x in sys.argv[4:]]
cap = cv2.VideoCapture(clip)
def cuadro(t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    return f if ok else None
if modo == "tira":
    fil = []
    for t in ts:
        f = cuadro(t)
        if f is None: continue
        H, W = f.shape[:2]
        c = f[0:int(H * .30), int(W * .22):int(W * .78)]
        c = cv2.resize(c, (960, int(c.shape[0] * 960 / c.shape[1])))
        cv2.putText(c, f"{t:g}", (4, 22), 0, .7, (0, 0, 0), 4); cv2.putText(c, f"{t:g}", (4, 22), 0, .7, (0, 255, 255), 2)
        fil.append(c)
    cv2.imwrite(os.path.join(OUT, f"al_{sal}.jpg"), np.vstack(fil), [cv2.IMWRITE_JPEG_QUALITY, 85])
else:
    f = cuadro(ts[0])
    f = cv2.resize(f, (1280, 720))
    for k in range(1, 10):
        x = int(1280 * k / 10); y = int(720 * k / 10)
        cv2.line(f, (x, 0), (x, 719), (0, 255, 255), 1); cv2.line(f, (0, y), (1279, y), (0, 255, 255), 1)
        cv2.putText(f, f".{k}", (x + 2, 12), 0, .4, (0, 255, 255), 1); cv2.putText(f, f".{k}", (2, y - 2), 0, .4, (0, 255, 255), 1)
    cv2.putText(f, f"t {ts[0]:g}", (1180, 712), 0, .6, (0, 255, 255), 2)
    cv2.imwrite(os.path.join(OUT, f"al_{sal}.jpg"), f, [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", sal)
