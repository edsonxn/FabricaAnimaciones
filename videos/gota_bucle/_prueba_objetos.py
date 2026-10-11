import sys, time, cv2, numpy as np
import boceto as B, objetos as O
from motor import W, H
h = B.Hoja()
def hoja_de(fn, nombre, u=1.0):
    h.limpiar(); fn(h, u); im = (np.clip(h.componer(),0,1)*255).astype(np.uint8)
    return im
def escena1(h,u):
    O.sol(76).dibujar(h,170,470,1,u=u); O.nube().dibujar(h,560,720,1.2,u=u)
    O.gota().dibujar(h,620,410,1.0,u=u)
    O.montana().dibujar(h,540,1500,0.85,u=u)
def escena2(h,u):
    O.rio().dibujar(h,540,900,1.0,u=u); O.hoja_barca().dibujar(h,540,600,0.9,u=u)
    O.gota("feliz","abierta").dibujar(h,540,560,0.9,u=u)
def escena3(h,u):
    O.grifo().dibujar(h,700,430,1,u=u); O.vaso().dibujar(h,420,900,1,u=u)
    p=O.agua_poli(0.6); h.relleno(p+(420,900),B.AZUL,frac=1)
    O.persona().dibujar(h,780,1150,0.8,u=u)
def escena4(h,u):
    O.mar_capa(800,700,B.AZUL).dibujar(h,0,0,1,u=u)
    O.pez().dibujar(h,300,1100,0.9,u=u); O.alga().dibujar(h,800,1450,1,u=u)
    O.gota("cerrados","ronca").dibujar(h,540,1000,1.2,u=u); O.barba().dibujar(h,540,1000,1.2,u=u)
    O.bloque_hielo().dibujar(h,300,500,0.9,u=u); O.copo().dibujar(h,800,500,1.2,u=u); O.marcas().dibujar(h,700,700,1,u=u)
    O.soplo().dibujar(h,200,600,1,u=u); O.vapor().dibujar(h,850,700,1,u=u)
ims=[]
for f in (escena1,escena2,escena3,escena4):
    t0=time.time(); im=hoja_de(f,'x'); print(f.__name__, round(time.time()-t0,2),'s'); ims.append(cv2.resize(im,(540,960),interpolation=cv2.INTER_AREA))
cv2.imwrite('previews/objetos.jpg', cv2.cvtColor(np.hstack(ims),cv2.COLOR_RGB2BGR))
# parcial
ims=[]
for u in (0.15,0.4,0.7,1.0):
    ims.append(cv2.resize(hoja_de(escena1,'x',u),(540,960),interpolation=cv2.INTER_AREA))
cv2.imwrite('previews/parcial.jpg', cv2.cvtColor(np.hstack(ims),cv2.COLOR_RGB2BGR))
