import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import kz_retrato as RT
import kz_mapa_dib as MD
from util import bg_grad
nombres = sys.argv[2:] or ["hidalgo", "morelos", "allende", "josefa"]
t = 1.1
lz = Lienzo(); lz.nuevo(t, wob=0.0)
n = len(nombres)
for i, q in enumerate(nombres):
    cx = 1920 * (i + 0.5) / n
    RT.retrato(lz, cx, 960, 150 if n <= 4 else 120, q, t, seed=i)
bg = bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)
img = componer(bg, lz.resolver(), boil=lz.boil)
cv2.imwrite(f"previews/{sys.argv[1]}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok")
