import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import efectos as E
from util import bg_grad
import mini_hidalgo as MH
cx, cy, s = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
lz = Lienzo(); lz.nuevo(0.3, wob=0.0)
MH.hidalgo(lz, cx, cy, s, 0.3)
bg = bg_grad((40, 24, 90), (200, 90, 90))
img = componer(bg, lz.resolver(), boil=lz.boil)
img = E.acabado(img, 3)
cv2.imwrite("previews/t_hid.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok")
