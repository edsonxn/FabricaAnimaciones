# Recorte con rejilla fina en coordenadas del cuadro COMPLETO: python lotl_zoom.py <fuente> <t> x0 y0 x1 y1 [resolver=1]
# -> ../previews/cuadros/z_<fuente>_<t>.jpg. Rejilla cada 0,01 (etiqueta cada 0,05). Lectura de PIES en UN cuadro.
import cv2, os, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, t = sys.argv[1], float(sys.argv[2])
x0, y0, x1, y1 = [float(v) for v in sys.argv[3:7]]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", n + ".mp4"))
cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
ok, f = cap.read()
H, W = f.shape[:2]
c = f[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
A = 1280
esc = A / c.shape[1]
c = cv2.resize(c, (A, int(c.shape[0] * esc)), interpolation=cv2.INTER_CUBIC)
def px(x): return int((x - x0) / (x1 - x0) * A)
def py(y): return int((y - y0) / (y1 - y0) * c.shape[0])
k = int(x0 * 100)
while k / 100 <= x1:
    if k / 100 >= x0:
        fuerte = k % 5 == 0
        cv2.line(c, (px(k / 100), 0), (px(k / 100), c.shape[0]), (0, 255, 255) if fuerte else (0, 110, 110), 1)
        if fuerte:
            cv2.putText(c, f"{k/100:.2f}", (px(k / 100) + 2, 12), 0, .42, (0, 255, 255), 1)
    k += 1
k = int(y0 * 100)
while k / 100 <= y1:
    if k / 100 >= y0:
        fuerte = k % 5 == 0
        cv2.line(c, (0, py(k / 100)), (A, py(k / 100)), (0, 255, 255) if fuerte else (0, 110, 110), 1)
        if fuerte:
            cv2.putText(c, f"{k/100:.2f}", (2, py(k / 100) - 2), 0, .42, (0, 255, 255), 1)
    k += 1
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"z_{n}_{t:g}.jpg"), c, [cv2.IMWRITE_JPEG_QUALITY, 88])
