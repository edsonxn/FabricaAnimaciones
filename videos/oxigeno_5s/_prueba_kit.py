# -*- coding: utf-8 -*-
"""Prueba visual de piezas del kit a gran tamaño (previews/kit.jpg)."""
import cv2
import numpy as np

import estilos
estilos.activar("kurzgesagt")
import fondos as F  # noqa: E402
import plano as P  # noqa: E402
import kz_pers2d as K2  # noqa: E402
from motor import Lienzo, componer, a_uint8  # noqa: E402

t = 2.0
lz = Lienzo()
lz.nuevo(t, wob=0.0)
bg = F.degradado(t, (0.45, 0.70, 0.95), (0.80, 0.90, 1.0))
lz.relleno(np.array([[0, 900], [1920, 900], [1920, 1080], [0, 1080]]), (90, 170, 110))
K2.cuerpo(lz, 300, 900, 90, "mujer", t, piernas="idle", brazos="idle", vista="tres", mirar=1)
K2.cuerpo(lz, 760, 900, 40, "hombre", t, piernas="camina", brazos="balanceo", vista="perfil", mirar=1)
K2.cuerpo(lz, 980, 900, 40, "nino", t, piernas="idle", brazos="saluda", vista="frente", mirar=1)
K2.busto(lz, 1400, 1000, 140, "mujer", t, yaw=-0.45, emocion="sorpresa", mano="boca")
P.kuri(lz, 1780, 900, 1.6, t, mirar=(-1, 0), boca=0.5)
img = componer(bg, lz.resolver())
cv2.imwrite("previews/kit.jpg", cv2.cvtColor(a_uint8(img), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok")
