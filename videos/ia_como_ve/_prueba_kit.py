"""Prueba del kit sin timeline: cuarto + niña + Kuri + fotos, y la cabeza con neuronas → previews/prueba_kit.jpg"""
import sys, types
sys.path.insert(0, "../../nucleo")
_C = {}
m = types.ModuleType("comun")
m.cache = lambda k, f: _C[k] if k in _C else _C.setdefault(k, f())
sys.modules["comun"] = m
import numpy as np, cv2
from acuarela import terminar
import fondos_ia as F
import personajes_ia as P
from personajes import kuri

t = 0.4
im = F.cuarto()
foto = P.foto_gato(t)
P.nina(im, 620, 640, 1.5, t, brazos=(2.0, 2.0), codos=(0.9, 0.9), mira=1,
       delante=lambda im_, manos: P.pegar(im_, foto, 640, 420, 0.55, -0.05, t=t))
kuri(im, 1250, 520, 1.8, t, cara="normal")
P.globo(im, 1450, 250, 520, 150, "", t, px=34, lineas=["UN GATO NARANJA", "DORMIDO SOBRE UN TECLADO"])
a = terminar(im, t)
im2 = F.cabeza()
F.neuronas(im2, t)
for k, f in enumerate([P.dibujo_nino(t), P.radiografia(t), P.meme_gato(t)]):
    P.pegar(im2, f, 400 + k * 560, 840, 0.45, 0.04 * (k - 1), t=t)
b = terminar(im2, t)
out = np.vstack([a, b])
cv2.imwrite("previews/prueba_kit.jpg", (np.clip(out, 0, 1)[..., ::-1] * 255).astype(np.uint8)[::2, ::2])
print("ok")
