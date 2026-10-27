"""cuadros_fx.py <salida.jpg> t1 t2 ... : cuadros del video CON efectos en esos segundos (640x360, 3 columnas)."""
import os
import sys

V = r"C:\FabricaAnimaciones\videos\lol_worlds_2026"
os.chdir(V)
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo"); sys.path.insert(0, V)
import cv2
import numpy as np
import secuencia_fx as F

capa = F.cargar()
S = capa.S
minis = []
for a in sys.argv[2:]:
    t = float(a)
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
    m = cv2.resize(f, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.rectangle(m, (0, 334), (150, 360), (20, 18, 18), -1)
    cv2.putText(m, f"{t:.1f}s", (6, 353), cv2.FONT_HERSHEY_SIMPLEX, .6, (90, 214, 255), 1, cv2.LINE_AA)
    minis.append(m)
while len(minis) % 3:
    minis.append(np.zeros_like(minis[0]))
cv2.imwrite(os.path.join(V, "previews", sys.argv[1]), np.vstack([np.hstack(minis[i:i + 3]) for i in range(0, len(minis), 3)]),
            [cv2.IMWRITE_JPEG_QUALITY, 82])
print("ok", sys.argv[1])

