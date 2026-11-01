# Tira del marcador superior de una fuente para medir K: python loly_hud.py <fuente|ruta.mp4> t1 t2 ... -> previews/cuadros/hud_<fuente>.jpg
# Recorta la franja x 0.08-0.92, y 0-0.075 de cada t (rótulo a la izquierda con el t); una por fila.
import os, sys
import cv2, numpy as np
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = sys.argv[1]
p = n if n.endswith(".mp4") else os.path.join(D, "medios", "_fuente", n + ".mp4")
cap = cv2.VideoCapture(p)
fil = []
for t in [float(x) for x in sys.argv[2:]]:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, im = cap.read()
    if not ok:
        continue
    H, W = im.shape[:2]
    c = im[0:int(.095 * H), int(.33 * W):int(.70 * W)]
    c = cv2.resize(c, (1000, int(1000 * c.shape[0] / c.shape[1])), interpolation=cv2.INTER_CUBIC)
    b = np.zeros((c.shape[0], 90, 3), np.uint8)
    cv2.putText(b, f"{t:g}", (4, 34), 0, .8, (0, 255, 255), 2)
    fil.append(np.hstack([b, c]))
s = os.path.join(D, "previews", "cuadros", "hud_" + os.path.basename(n).replace(".mp4", "") + ".jpg")
cv2.imwrite(s, np.vstack(fil), [cv2.IMWRITE_JPEG_QUALITY, 90])
print(s)
