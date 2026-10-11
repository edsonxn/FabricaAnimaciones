"""Renderiza UN cuadro completo (con el acabado final): python _cuadro.py t nombre"""
import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8
import escenas as S
import efectos as E
t = float(sys.argv[1])
lz = Lienzo()
img = S.render_mundo(lz, t)
img = E.acabado(img, int(t * 10))
cv2.imwrite(f"previews/{sys.argv[2]}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok")
