import sys, math
import numpy as np, cv2
import escena_base  # activa el estilo
from motor import Lienzo, componer, a_uint8, W, H
import kit as K
import plano as P

lz = Lienzo()
tiles = []
for i, t in enumerate([0.0, 0.12, 0.24, 0.36, 0.48, 0.60]):
    lz.nuevo(t, wob=0.0)
    bg = K.degradado_img((70, 40, 120), (250, 150, 90))
    K.colinas(lz, 1250, (60, 40, 90))
    ph = t * 2 * math.pi / 0.72
    K.persona(lz, 300, 1300, 1.7, t, ph=ph, paso=1.0, mirar=1)
    K.persona(lz, 760, 1300, 1.7, t, ph=ph, paso=1.0, mirar=-1, piel=K.PIEL[3], pelo_t="largo", falda=0.7, ropa=(80, 170, 190), pelo=(30,24,30))
    K.persona(lz, 540, 800, 1.7, t, ph=0, paso=0.0, mirar=1, brazos=(0.2,0.3,-2.6,0.2), boca=0.8, pelo_t="moño", piel=K.PIEL[0])
    img = componer(bg, lz.resolver(), boil=0)
    im = a_uint8(np.clip(img, 0, 1))
    tiles.append(cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA))
    if i == 2:
        cv2.imwrite("previews/kit_full.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
cv2.imwrite("previews/kit_test.jpg", cv2.cvtColor(np.hstack(tiles), cv2.COLOR_RGB2BGR))
