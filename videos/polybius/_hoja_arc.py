# -*- coding: utf-8 -*-
"""Prueba rápida del kit arcade.py -> previews/arc.jpg"""
import cv2
import numpy as np

from arcade import *  # noqa: F401,F403

ims = []
for t in (1.0, 3.7):
    p = P()
    salon(p, t)
    cabina(p, 960, 1010, 760, t, pant_formas, color=NEGRO, borde=(0.05, 0.05, 0.07), luz=VIOL, marq=(0.5, 0.2, 0.9), rotulo="POLYBIUS")
    for k in range(4):
        x = 420 - k * 120
        persona(p, x, 1030 + k * 6, 400 - k * 12, pose_estar(t + k), SIL, 1, pelo=("corto", "afro", "largo", "corto")[k])
    vineta_p(p, 0.45)
    ims.append(p.im.copy())
    p = P()
    salon(p, t, luz=0.5, neones=False)
    sx, sy = cabina_lado(p, 1150, 1010, 780, -1, t, luz=CIAN)
    j = jugador(p, 820, 1010, 560, t, 1)
    luz_cara(p, j, 820, 1010, 1, CIAN, 560)
    vineta_p(p, 0.45)
    ims.append(p.im.copy())
    for fn in (pant_asteroides, pant_tunel, pant_tanque, pant_formas):
        p = P()
        fn(p, 260, 60, 1660, 1020, t)
        ims.append(p.im.copy())
ims = [cv2.cvtColor((np.clip(i, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR) for i in ims]
ims = [cv2.resize(i, (640, 360)) for i in ims]
cv2.imwrite("previews/arc.jpg", np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]))
print("ok")
