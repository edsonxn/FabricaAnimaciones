# Hoja 4x4 de recortes de una zona del cuadro: python al_zoom.py <clip> <salida> <t0> <paso> x0 y0 x1 y1  (fracciones del cuadro)
# -> previews/cuadros/al_<salida>.jpg ; cada recorte rotulado con su t
import sys, os, cv2, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
clip, sal, t0, paso = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
x0, y0, x1, y1 = [float(v) for v in sys.argv[5:9]]
cap = cv2.VideoCapture(clip)
out = []
for k in range(16):
    t = t0 + k * paso
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok: break
    H, W = f.shape[:2]
    c = f[int(H * y0):int(H * y1), int(W * x0):int(W * x1)]
    c = cv2.resize(c, (480, int(c.shape[0] * 480 / c.shape[1])))
    cv2.putText(c, f"{t:g}", (4, 22), 0, .7, (0, 0, 0), 4); cv2.putText(c, f"{t:g}", (4, 22), 0, .7, (0, 255, 255), 2)
    out.append(c)
while len(out) < 16: out.append(np.zeros_like(out[0]))
g = np.vstack([np.hstack(out[i:i + 4]) for i in range(0, 16, 4)])
cv2.imwrite(os.path.join(D, "..", "previews", "cuadros", f"al_{sal}.jpg"), g, [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok", sal)
