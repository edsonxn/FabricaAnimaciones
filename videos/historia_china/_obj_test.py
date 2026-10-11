import sys, numpy as np, cv2
import boceto as B, mapa as M
from obj_base import *
M.cargar()
cam=M.Cam(108,35,1.25)
img=M.fondo_base(); M.pintar_tierra(img,cam,0)
S=cam.proyectar(M.CAMPOS['han']); M.pintar(img,S,M.COL['han'],1.0,0)
h=B.Hoja(); h.limpiar(); h.fondo=img
P=[
 persona(ROJO_CH, PIEL, "corona", "feliz", (30,120), acc_d="rollo", barba=None),
 persona(MORADO, PIEL_CL, "letrado", "normal", (20,40), barba=(240,240,244), acc_i="rollo", traje="tunica"),
 persona(VERDE_OSC, PIEL, "paja", "feliz", (25,80), acc_d="azada", traje="corta"),
 persona(AZUL_IMP, PIEL, "funcionario", "serio", (30,30), acc_d="hoja", faja=ORO),
 persona((120,130,110), PIEL, "casco", "enojo", (20,140), acc_d="lanza", traje="armadura", pose=1),
 persona(ROJO_OSC, PIEL, "gorro", "miedo", (60,60), trenza=False, mirada=1),
]
for i,p in enumerate(P):
    x=200+i*300; y=520
    p.dibujar(h,x,y,0.9,0.0,False,1.0,0,i+1,peg=True)
    p.dibujar(h,x,y+420,0.6,0.0,False,0.5,0,i+1,lapiz=0.8)
out=np.clip(h.componer(),0,1)
cv2.imwrite('previews/_o_test.jpg',(out[...,::-1]*255).astype(np.uint8))
