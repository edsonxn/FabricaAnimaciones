# -*- coding: utf-8 -*-
"""Hoja de prueba de las figuras de fig.py -> previews/figs.jpg (960x540)."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo")); sys.path.insert(0, AQUI)
import cv2, numpy as np, math
import grabado as GR
import fig as F
t = float(sys.argv[1]) if len(sys.argv) > 1 else 1.3
g = GR.G(t)
GR.cielo(g, t, 300)
for i, tipo in enumerate(("capa", "guerrero", "enano", "medico", "sanador", "cazador", "mercader")):
    F.persona(g, 110 + i * 150, 560, 0.62, t, tipo, fase=i, anda=1.0 if i % 2 else 0.0, dirx=1 if i < 4 else -1,
              aura=1.0 if i == 6 else 0.0, sem=i)
F.persona(g, 1180, 560, 0.62, t, "capa", anda=2.0, fase=1.0)
F.persona(g, 1330, 560, 0.62, t, "capa", cae=0.6)
F.lobo(g, 1600, 560, 0.8, t, ojo=1.0, grune=1.0)
F.hakkar(g, 330, 1040, 0.42, t, boca=0.4)
F.cara_hakkar(g, 900, 860, 0.55, t, boca=1.0)
F.palmera(g, 1250, 1060, 0.55, t, sem=2)
F.estatua_serpiente(g, 1480, 1060, 0.5, t)
F.pino(g, 1700, 1060, 0.5, t)
F.jaula(g, 1850, 640, 0.9, t, sangre=1.0)
F.hoja_grande(g, 1600, 1080, 0.7, t, ang=-120)
s = F.reloj_arena(t, 0.4)
GR.componer(g, s, dx=0, dy=0) if False else None
im = GR.acabado(g)
cv2.imwrite("previews/figs.jpg", (cv2.resize(np.clip(im, 0, 1), (960, 540), interpolation=cv2.INTER_AREA) * 255).astype(np.uint8)[..., ::-1])
print("ok")
