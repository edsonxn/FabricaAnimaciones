import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import kz_mapa as KM
import kz_mapa_dib as MD
MP = KM.MAPA
z = float(sys.argv[1]); t = float(sys.argv[2])
cam = (-60.0, 28.0, z)
lz = Lienzo(); lz.nuevo(t, wob=0.0)
MD.mar_vivo(lz, cam, t, seed=2)
bg = MP.base(cam, t)
img = componer(bg, lz.resolver(), boil=lz.boil)
im = cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR)
cv2.imwrite("previews/olas_full.png", im[200:740, 480:1440])
print("ok")
