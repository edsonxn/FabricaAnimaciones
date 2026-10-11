import sys, time
import numpy as np, cv2
import boceto as B, mapa as M
t0=time.time(); M.cargar(); print('carga', round(time.time()-t0,2),'s', M.FW, M.FH)
def cuadro(nombre, campo_key, cam, color):
    t=time.time()
    img=M.fondo_base()
    M.pintar_tierra(img, cam, 0)
    S=cam.proyectar(M.CAMPOS[campo_key]); M.pintar(img,S,color,1.0,0)
    h=B.Hoja(); h.limpiar(); h.fondo=img
    out=np.clip(h.componer(),0,1)
    print(nombre, round(time.time()-t,3),'s')
    cv2.imwrite(f'previews/_m_{nombre}.jpg', (out[...,::-1]*255).astype(np.uint8))
import os; os.makedirs('previews',exist_ok=True)
cuadro('prc','prc',M.Cam(104,36,1.25),M.COL['prc'])
cuadro('prc','prc',M.Cam(104,36,1.25),M.COL['prc'])
cuadro('tang','tang',M.Cam(104,37,1.25),M.COL['tang'])
cuadro('rio','shang',M.Cam(111,36,3.2),M.COL['shang'])
