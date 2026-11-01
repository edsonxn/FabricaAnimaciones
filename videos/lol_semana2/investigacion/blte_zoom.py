# Recorte de UN cuadro de la fuente con rejilla fina (coordenadas del cuadro COMPLETO, 0..1):
# python investigacion/blte_zoom.py <fuente> <t> x0 y0 x1 y1 [paso=0.02] -> previews/cuadros/z_<fuente>_<t>.jpg
import os, sys
import cv2
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, t, x0, y0, x1, y1 = sys.argv[1], float(sys.argv[2]), *[float(v) for v in sys.argv[3:7]]
paso = float(sys.argv[7]) if len(sys.argv) > 7 else 0.02
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", f"{n}.mp4"))
cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
ok, im = cap.read()
H, W = im.shape[:2]
c = im[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
esc = 1500 / c.shape[1]
c = cv2.resize(c, None, fx=esc, fy=esc, interpolation=cv2.INTER_CUBIC)
ch, cw = c.shape[:2]
def px(x): return int((x - x0) / (x1 - x0) * cw)
def py(y): return int((y - y0) / (y1 - y0) * ch)
k = int(x0 / paso) + 1
while k * paso < x1:
    v = k * paso; cv2.line(c, (px(v), 0), (px(v), ch), (0, 255, 255), 1)
    cv2.putText(c, f"{v:.2f}", (px(v) + 2, 13), 0, .42, (0, 255, 255), 1); cv2.putText(c, f"{v:.2f}", (px(v) + 2, ch - 4), 0, .42, (0, 255, 255), 1)
    k += 1
k = int(y0 / paso) + 1
while k * paso < y1:
    v = k * paso; cv2.line(c, (0, py(v)), (cw, py(v)), (0, 255, 255), 1)
    cv2.putText(c, f"{v:.2f}", (2, py(v) - 3), 0, .42, (0, 255, 255), 1); cv2.putText(c, f"{v:.2f}", (cw - 36, py(v) - 3), 0, .42, (0, 255, 255), 1)
    k += 1
cv2.putText(c, f"{n} t={t:g}", (cw - 230, 34), 0, .7, (255, 255, 255), 2)
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"z_{n}_{t:g}.jpg"), c, [cv2.IMWRITE_JPEG_QUALITY, 88])
