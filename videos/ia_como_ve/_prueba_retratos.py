import sys, types
sys.path.insert(0, "../../nucleo")
_C = {}
m = types.ModuleType("comun"); m.cache = lambda k, f: _C[k] if k in _C else _C.setdefault(k, f()); sys.modules["comun"] = m
import numpy as np, cv2
from acuarela import terminar
import fondos_ia as F, personajes_ia as P
im = F.papel("calido")
for k, (n, nom) in enumerate([("hubel", "DAVID HUBEL"), ("wiesel", "TORSTEN WIESEL"), ("feifei_li", "FEI-FEI LI"), ("lecun", "YANN LECUN")]):
    P.camafeo(im, P.retrato(n, 300, 380, sepia=k < 2), 260 + k * 460, 470, 1.0, 0.3, nombre=nom, seed=5200 + 10 * k)
P.pegar(im, P.retrato("hubel_wiesel_registro", 290, 390), 1700, 880, 0.4, 0.05, t=0.3)
cv2.imwrite("previews/prueba_retratos.jpg", (np.clip(terminar(im, 0.3), 0, 1)[..., ::-1] * 255).astype(np.uint8)[::2, ::2])
