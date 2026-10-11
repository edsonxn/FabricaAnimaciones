import sys, cv2, numpy as np
import estilos; estilos.activar("vox")
import fondos as F, vox as V, locales as L
from motor import Lienzo, componer, a_uint8, W, H, mat_t, mat_s
lz = Lienzo(); tiles=[]
def vista(cx, cy, z, f, t=1.0):
    lz.nuevo(0.0, wob=0.6)
    lz.M = mat_t(W/2, H/2) @ mat_s(z) @ mat_t(-cx, -cy)
    f(lz, t)
    img = componer(F.papel(0), lz.resolver(), boil=0)
    tiles.append(cv2.resize(a_uint8(np.clip(img,0,1)),(360,640),interpolation=cv2.INTER_AREA))
def escena(lz, t):
    L.cielo(lz, "alba")
    L.sol(lz, -300, -700, 70, t)
    L.nube(lz, -200, -900, 1.2); L.nube(lz, 300, -1050, 0.9)
    L.colinas_fondo(lz, 0, 0.3, -300, 240, 1, (196,150,130), -2500, 2500)
    L.montaña_bufa(lz)
    L.suelo(lz, -1100, 1400)
    L.arroyo(lz)
    L.tienda(lz, -60, 6, 1.0, 1, 1); L.choza(lz, 90, 8, 1.0, 1, 2); L.casa_adobe(lz, 200, float(L.h(200)), 1, 1, 3)
    L.casa_piedra(lz, -240, 10, 1, 1, 4, pisos=2)
    L.iglesia(lz, 380, float(L.h(380))+30, 0.8, 1, 5)
    L.fogata(lz, 20, 20, 1.0, 0.3)
    V.figura(lz, -140, 60, 0.9, V.CAMINAR[2], "tolosa", 1)
    V.figura(lz, 30, 90, 0.9, V.IDLE[0], "indigena", -1)
    V.mula(lz, -300, 110, 0.9, 3, 1)
vista(0,-380,1.0,escena)
vista(0,-380,0.6,escena)
vista(100,-100,1.8,escena)
cv2.imwrite("previews/local.jpg", cv2.cvtColor(np.hstack(tiles),cv2.COLOR_RGB2BGR))
