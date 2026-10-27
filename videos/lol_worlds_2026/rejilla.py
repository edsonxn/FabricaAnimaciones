"""rejilla.py <salida> <n:t[:z:cx:cy]> ...  -> cuadros de jN.mp4 (con zoom opcional) a 960x540 con rejilla 0.1, en 2 columnas."""
import sys, os, cv2, numpy as np
V = r"C:\FabricaAnimaciones\videos\lol_worlds_2026"
ims = []
for arg in sys.argv[2:]:
    p = arg.split(":")
    n, t = p[0], float(p[1])
    ruta = n if os.path.sep in n else os.path.join(V, "medios", "_fuente", f"j{n}.mp4")
    cap = cv2.VideoCapture(ruta)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if len(p) > 2:
        z, cx, cy = map(float, p[2:5])
        h, w = f.shape[:2]
        cw, ch = w / z, h / z
        x0 = min(max(cx * w - cw / 2, 0), w - cw); y0 = min(max(cy * h - ch / 2, 0), h - ch)
        f = cv2.warpAffine(f, np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]]), (w, h))
    f = cv2.resize(f, (960, 540), interpolation=cv2.INTER_AREA)
    for i in range(1, 10):
        x, y = i * 96, i * 54
        cv2.line(f, (x, 0), (x, 539), (0, 255, 255), 1)
        cv2.line(f, (0, y), (959, y), (0, 255, 255), 1)
        cv2.putText(f, f".{i}", (x + 2, 12), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 255, 255), 1)
        cv2.putText(f, f".{i}", (2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 255, 255), 1)
    cv2.putText(f, arg, (400, 530), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 255), 2)
    ims.append(f)
if len(ims) % 2:
    ims.append(np.zeros_like(ims[0]))
out = np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)])
cv2.imwrite(os.path.join(V, "previews", "cuadros", sys.argv[1]), out, [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok", sys.argv[1])
