# fr.py <archivo> <offset_abs> <salida_prefijo> t1 t2 ... (tiempos ABSOLUTOS; archivo empieza en offset_abs)
import cv2, sys
f, off, pref = sys.argv[1], float(sys.argv[2]), sys.argv[3]
cap = cv2.VideoCapture(f)
for a in sys.argv[4:]:
    t = float(a)
    cap.set(cv2.CAP_PROP_POS_MSEC, (t-off)*1000)
    ok, im = cap.read()
    if ok:
        cv2.imwrite(f"{pref}_{int(t*10):06d}.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    else: print("fallo", t)
