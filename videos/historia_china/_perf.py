import time, numpy as np, cv2
import boceto as B, mapa as M
M.cargar()
cam=M.Cam(104,36,1.25)
def tm(n,f,rep=3):
    f(); t=time.time()
    for _ in range(rep): r=f()
    print(f'{n:28s}{(time.time()-t)/rep*1000:7.1f} ms'); return r
img=tm('fondo_base',M.fondo_base)
S=tm('proyectar',lambda: cam.proyectar(M.CAMPOS['prc']))
tm('pintar prc',lambda: M.pintar(img.copy() if False else img,S,M.COL['prc'],1.0,0))
def tierra(): 
    i=M.fondo_base(); M.pintar_tierra(i,cam,0); return i
tm('tierra(total)',tierra)
h=B.Hoja(); h.limpiar(); h.fondo=img
tm('componer',lambda: h.componer())
tm('sobel',lambda: cv2.Sobel(S,cv2.CV_32F,1,0,ksize=3))
