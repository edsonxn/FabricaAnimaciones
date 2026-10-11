import sys, cv2, numpy as np
import estilos; estilos.activar("vox")
import fondos as F, vox as V, mapa_dib as M, geo as G
from motor import Lienzo, componer, a_uint8, W, H, mat_t, mat_s
lz = Lienzo(); tiles=[]
def vista(cx, cy, z, f=None):
    lz.nuevo(0.0, wob=0.6)
    lz.M = mat_t(W/2, H/2) @ mat_s(z) @ mat_t(-cx, -cy)
    M.mar(lz); M.tierra(lz); M.chichimeca(lz); M.sierras(lz); M.nopales(lz)
    zx,zy=0,0
    M.estrella(lz, 0, 0, 22)
    x,y=G.xy(*G.CIUDADES["mexico"]); M.edificio_mexico(lz,x,y,0.5)
    if f: f(lz)
    img = componer(F.papel(0), lz.resolver(), boil=0)
    tiles.append(cv2.resize(a_uint8(np.clip(img,0,1)),(360,640),interpolation=cv2.INTER_AREA))
vista(60,-150,0.55)
vista(0,0,2.0)
vista(1800,-300,0.22, lambda lz: M.ruta(lz,1.0))
vista(3000,-400,0.13, lambda lz: M.ruta(lz,1.0))
cv2.imwrite("previews/mapa.jpg", cv2.cvtColor(np.hstack(tiles),cv2.COLOR_RGB2BGR))
