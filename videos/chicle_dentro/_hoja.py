"""Hoja de prueba: python _hoja.py nombre t1 t2 ... → previews/hoja_<nombre>.jpg (3 columnas, 360 px de ancho)."""
import sys, time; sys.path.insert(0, "../../nucleo")
import numpy as np, cv2
import escenas
ts = [float(x) for x in sys.argv[2:]]
t0 = time.time(); ims = []
for t in ts:
    im = escenas.cuadro(t)
    im = cv2.resize((np.clip(im, 0, 1)[..., ::-1] * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.2f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    ims.append(im)
while len(ims) % 3: ims.append(np.zeros_like(ims[0]))
filas = [np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]
cv2.imwrite(f"previews/hoja_{sys.argv[1]}.jpg", np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(f"{(time.time() - t0) / len(ts):.2f} s/cuadro")
