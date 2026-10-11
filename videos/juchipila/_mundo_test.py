"""Prueba de un mundo isométrico: python _mundo_test.py nombre cx cy cz zoom [u] [t]"""
import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import kz_iso as I
import paisajes as PA
import mundos_c as MC
nombre = sys.argv[1]
cx, cy, cz, zm = map(float, sys.argv[2:6])
u = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
t = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
lz = Lienzo(); lz.nuevo(t, wob=0.0)
C = MC.CerroVentanas()
iso = I.Iso(cx, cy, cz, zm)
C.suelo(lz, iso, t)
m = C.objetos(t, u)
m.dibujar(lz, iso)
img = componer(PA.cielo(0.0), lz.resolver(), boil=0)
cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok")
