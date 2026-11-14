import cv2, sys, numpy as np, os
# uso: hoja.py video t0 t1 paso salida_prefijo [cols=5] [filas=4] [ancho=256]
v, t0, t1, paso, pref = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 5
filas = int(sys.argv[7]) if len(sys.argv) > 7 else 4
w = int(sys.argv[8]) if len(sys.argv) > 8 else 256
h = int(w * 9 / 16)
cap = cv2.VideoCapture(v)
ts = []
t = t0
while t < t1: ts.append(t); t += paso
n = cols * filas
for k in range(0, len(ts), n):
    lote = ts[k:k + n]
    img = np.zeros((filas * h, cols * w, 3), np.uint8)
    for j, s in enumerate(lote):
        cap.set(cv2.CAP_PROP_POS_MSEC, s * 1000)
        ok, f = cap.read()
        if not ok: continue
        f = cv2.resize(f, (w, h))
        cv2.putText(f, f"{s:.1f}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 0, 0), 3)
        cv2.putText(f, f"{s:.1f}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 255, 255), 1)
        y, x = divmod(j, cols)
        img[y * h:(y + 1) * h, x * w:(x + 1) * w] = f
    out = f"{pref}_{int(lote[0]):05d}.jpg"
    cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(out)
