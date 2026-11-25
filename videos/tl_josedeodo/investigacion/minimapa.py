# Minimapa ampliado de una fuente: python minimapa.py <fuente> <salida> <por_fila> t1 t2 ... -> ../previews/cuadros/<salida>.jpg
import cv2, os, sys
import numpy as np
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, sal, k, ts = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", n + ".mp4"))
fil = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000); ok, f = cap.read()
    H, W = f.shape[:2]
    m = f[int(H * .735):H, int(W * .855):W]
    m = cv2.resize(m, (int(m.shape[1] * 2.2), int(m.shape[0] * 2.2)), interpolation=cv2.INTER_CUBIC)
    cv2.putText(m, t, (4, 26), 0, .9, (0, 0, 0), 4); cv2.putText(m, t, (4, 26), 0, .9, (0, 255, 255), 2)
    fil.append(m)
while len(fil) % k:
    fil.append(np.zeros_like(fil[0]))
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"{sal}.jpg"), np.vstack([np.hstack(fil[i:i + k]) for i in range(0, len(fil), k)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
