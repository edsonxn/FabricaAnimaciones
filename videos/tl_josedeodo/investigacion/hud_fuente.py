# Tira del marcador (reloj, oro, kills) + zona de banners de una fuente cortada: python hud_fuente.py <fuente> <salida> t1 t2 ...
# -> ../previews/cuadros/<salida>.jpg (una fila por cuadro, 960 px)
import cv2, os, sys
import numpy as np
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, sal, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", n + ".mp4"))
fil = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000)
    ok, f = cap.read()
    if not ok:
        continue
    H, W = f.shape[:2]
    c = f[0:int(H * .10), int(W * .30):int(W * .70)]
    b = f[int(H * .10):int(H * .30), int(W * .30):int(W * .70)]
    c = np.vstack([c, b])
    c = cv2.resize(c, (960, int(c.shape[0] * 960 / c.shape[1])))
    cv2.putText(c, t, (4, 20), 0, .6, (0, 0, 0), 4)
    cv2.putText(c, t, (4, 20), 0, .6, (0, 255, 255), 2)
    fil.append(c)
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"{sal}.jpg"), np.vstack(fil), [cv2.IMWRITE_JPEG_QUALITY, 85])
