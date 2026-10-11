import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import kz_retrato as R
from util import bg_grad
nombres = sys.argv[2:] or ["hidalgo", "morelos", "allende", "josefa", "iturbide", "calleja", "guerrero", "campesina"]
lz = Lienzo(); lz.nuevo(0.5, wob=0.0)
n = len(nombres)
cols = 4
for i, q in enumerate(nombres):
    cx = 240 + (i % cols) * 480
    cy = 410 + (i // cols) * 540
    R.retrato(lz, cx, cy, 98, q, 0.5 + i * 0.3, emocion=["neutro", "alegre", "serio", "sorpresa"][i % 4], habla=0.6 if i % 3 == 0 else 0.0, seed=i)
bg = bg_grad((60, 30, 110), (140, 60, 120))
img = componer(bg, lz.resolver(), boil=lz.boil)
cv2.imwrite(f"previews/{sys.argv[1]}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok")
