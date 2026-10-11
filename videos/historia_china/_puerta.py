import numpy as np, cv2
import boceto as B, mapa as M, obj_a as A, obj_b as Bb
M.cargar()
cam=M.Cam(108,35,1.25); img=M.fondo_base(); M.pintar_tierra(img,cam,0)
h=B.Hoja(); h.limpiar(); h.fondo=img
for i,ab in enumerate((0.0,0.5,1.0)):
    A.puerta(ab).dibujar(h,400+500*i,800,0.85,0,False,1.0,0,3,peg=True)
Bb.gran_puerta_cerrada(1.0).dibujar(h,1500,420,0.6,0,False,1.0,0,3,peg=True)
Bb.gran_puerta_cerrada(0.0).dibujar(h,1000,420,0.6,0,False,1.0,0,3,peg=True)
cv2.imwrite('previews/_puerta.jpg',(np.clip(h.componer(),0,1)[...,::-1]*255).astype(np.uint8))
