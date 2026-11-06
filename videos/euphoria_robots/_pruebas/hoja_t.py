"""python _pruebas/hoja_t.py t1 t2 ... -> previews/hoja_t.jpg (cuadros del video a tiempo global, grabaciones reales)"""
import sys; sys.path.insert(0, ".")
import cv2, numpy as np
import escenas as E
from motor import Lienzo
lz = Lienzo(); ims = []
for a in sys.argv[1:]:
    t = float(a); t0, nom = E.momento_en(t)
    img = E.pinta(lz, nom, t - t0, t)
    im = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.putText(im, f"{t} {nom}", (20, 60), 0, 1.6, (255, 255, 255), 3)
    ims.append(cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA))
while len(ims) % 6: ims.append(np.zeros_like(ims[0]))
cv2.imwrite("previews/hoja_t.jpg", np.vstack([np.hstack(ims[i:i + 6]) for i in range(0, len(ims), 6)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok")
