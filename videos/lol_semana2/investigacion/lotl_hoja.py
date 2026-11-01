# Hoja 2 columnas (640 px por cuadro) de una fuente: python lotl_hoja.py <fuente> <salida> t1 t2 ... -> ../previews/cuadros/lotl_<salida>.jpg
# Solo para ubicar la acción y leer el reloj; las coordenadas se miden con rejilla2.py en UN cuadro.
import cv2, os, sys
import numpy as np
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, sal, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", n + ".mp4"))
ims = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    f = cv2.resize(f, (640, 360))
    cv2.putText(f, f"{t:g}", (270, 130), 0, .9, (0, 0, 0), 4)
    cv2.putText(f, f"{t:g}", (270, 130), 0, .9, (0, 255, 255), 2)
    ims.append(f)
if len(ims) % 2:
    ims.append(np.zeros_like(ims[0]))
s = np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)])
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"lotl_{sal}.jpg"), s, [cv2.IMWRITE_JPEG_QUALITY, 85])
