# -*- coding: utf-8 -*-
"""Prueba de `K.luna_dos_caras`: cara visible, giro a medias, cara oculta y oculta con el «panqueque» -> previews/luna_caras.jpg."""
import math, os
import cv2, numpy as np
import estilos
from motor import Lienzo, componer
import kz_espacio as K

estilos.activar("kurzgesagt")
os.makedirs("previews", exist_ok=True)
lz = Lienzo(); lz.nuevo(1.0, wob=0.0)
for i, (rot, pq) in enumerate(((0.0, 0.0), (math.pi * 0.55, 0.0), (math.pi, 0.0), (math.pi, 1.0))):
    K.luna_dos_caras(lz, 250 + i * 470, 540, 215, rot=rot, ang_luz=math.pi, panqueque=pq)
img = componer(K.fondo_espacio(1.0), lz.resolver(), boil=lz.boil)
cv2.imwrite("previews/luna_caras.jpg", cv2.cvtColor((np.clip(img, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
