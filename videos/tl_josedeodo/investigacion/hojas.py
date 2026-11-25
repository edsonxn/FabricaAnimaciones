# Hojas de contacto de un VOD: python hojas.py <video> <desde_s> <hasta_s> <paso_s> <prefijo>
# -> <prefijo>_NN.jpg con 4x4 cuadros de 480 px rotulados con su segundo del video (para leer el reloj del HUD y ubicar jugadas)
import subprocess, sys, os
import numpy as np, cv2
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
vid, a, b, paso, pre = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cap = cv2.VideoCapture(vid)
ts = list(np.arange(a, b, paso))
cuadros = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        break
    f = cv2.resize(f, (480, int(480 * f.shape[0] / f.shape[1])))
    cv2.putText(f, f"{t:.0f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(f, f"{t:.0f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cuadros.append(f)
for k in range(0, len(cuadros), 16):
    g = cuadros[k:k + 16]
    while len(g) < 16:
        g.append(np.zeros_like(cuadros[0]))
    filas = [np.hstack(g[i:i + 4]) for i in range(0, 16, 4)]
    cv2.imwrite(f"{pre}_{k // 16:02d}.jpg", np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
print(len(cuadros), "cuadros")
