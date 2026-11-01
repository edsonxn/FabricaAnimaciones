# Hoja de cuadros de una fuente para elegir la pausa: python hoja.py <fuente> t1 t2 ... → previews/cuadros/h_<fuente>.jpg
# (3 columnas a 640x360, con el segundo de la fuente). Para MEDIR, usar rejilla2.py (UN cuadro a 1280 px).
import os, sys
import cv2, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
n, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", f"{n}.mp4"))
minis = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, im = cap.read()
    m = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(m, f"{n} t={t:g}", (8, 350), 0, .6, (0, 255, 255), 2)
    minis.append(m)
while len(minis) % 3:
    minis.append(np.zeros_like(minis[0]))
os.makedirs(os.path.join(D, "previews", "cuadros"), exist_ok=True)
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"h_{n}.jpg"), np.vstack([np.hstack(minis[i:i + 3]) for i in range(0, len(minis), 3)]))
