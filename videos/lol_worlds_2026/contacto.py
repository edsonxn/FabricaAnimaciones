"""Hoja de contacto: python contacto.py <n> <desde> <hasta> <paso> [cols] [ancho] -> previews/j<n>_c<desde>.jpg"""
import sys, os, cv2, numpy as np
V = r"C:\FabricaAnimaciones\videos\lol_worlds_2026"
n, a, b, paso = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 8
W = int(sys.argv[6]) if len(sys.argv) > 6 else 240
H = W * 9 // 16
cap = cv2.VideoCapture(os.path.join(V, "medios", "_fuente", f"j{n}.mp4"))
ims = []
t = a
while t <= b + 1e-6:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        break
    f = cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA)
    cv2.rectangle(f, (0, 0), (62, 20), (0, 0, 0), -1)
    cv2.putText(f, f"{t:.1f}", (3, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1, cv2.LINE_AA)
    ims.append(f)
    t += paso
while len(ims) % cols:
    ims.append(np.zeros((H, W, 3), np.uint8))
filas = [np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]
out = os.path.join(V, "previews", f"j{n}_c{int(a)}.jpg")
cv2.imwrite(out, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
print(out, len(ims))
