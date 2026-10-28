# Cuadros sueltos del video con su capa de efectos: python ver.py salida.jpg t1 t2 ... (rejilla de 3 columnas a 640x360)
import os, sys
import cv2, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import secuencia_fx as SF
capa = SF.cargar()
S = capa.S
out, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
minis = []
for t in ts:
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
    m = cv2.resize(f, (640, 360), interpolation=cv2.INTER_AREA)
    if m.dtype != np.uint8:
        m = np.clip(m * 255, 0, 255).astype(np.uint8)
    cv2.putText(m, f"{t:.1f}", (8, 350), 0, .6, (0, 255, 255), 2)
    minis.append(m)
while len(minis) % 3:
    minis.append(np.zeros_like(minis[0]))
cv2.imwrite(out, np.vstack([np.hstack(minis[i:i + 3]) for i in range(0, len(minis), 3)]))
