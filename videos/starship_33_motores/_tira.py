# python _tira.py clip.mp4 t0 t1 paso out.jpg  -> hoja de cuadros 384x216 con el segundo
import sys, cv2, numpy as np
f, a, b, p, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cap = cv2.VideoCapture(f); cel = []
t = a
while t <= b + 1e-6:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, im = cap.read()
    if not ok: break
    im = cv2.resize(im, (384, 216)); cv2.putText(im, f"{t:.1f}", (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2); cel.append(im); t += p
c = 5
while len(cel) % c: cel.append(np.zeros_like(cel[0]))
cv2.imwrite(out, np.vstack([np.hstack(cel[i:i + c]) for i in range(0, len(cel), c)]), [cv2.IMWRITE_JPEG_QUALITY, 80])
print(out, len(cel))
