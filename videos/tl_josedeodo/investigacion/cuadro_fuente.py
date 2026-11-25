# Cuadro suelto de una fuente a 1280 px: python cuadro_fuente.py <fuente> t1 t2 ... -> ../previews/cuadros/c_<fuente>_<t>.jpg
import cv2, os, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = sys.argv[1]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", n + ".mp4"))
for t in sys.argv[2:]:
    cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000)
    ok, f = cap.read()
    f = cv2.resize(f[0:int(f.shape[0] * .76)], (1280, int(1280 * .76 * 1080 / 1920)))
    cv2.imwrite(os.path.join(D, "previews", "cuadros", f"c_{n}_{t}.jpg"), f, [cv2.IMWRITE_JPEG_QUALITY, 85])
