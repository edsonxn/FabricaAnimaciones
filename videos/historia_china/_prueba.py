"""Hoja de contacto: python _prueba.py t1 t2 ... [--sol ESC] -> previews/hoja.jpg (cuadros 960x540 en rejilla)"""
import sys, time, math
import numpy as np, cv2
import escenas as E
args=[a for a in sys.argv[1:]]
ts=[float(a) for a in args]
cols=3 if len(ts)>4 else 2
d=E.TL["escenas"][0]
m=E.Mundo(d,0)
tiles=[]
for t in ts:
    t0=time.time(); im=m.render(None,t); dt=time.time()-t0
    print(f't={t:6.2f}  {dt*1000:5.0f} ms')
    small=cv2.resize((im[...,::-1]*255).astype(np.uint8),(960,540),interpolation=cv2.INTER_AREA)
    cv2.putText(small,f'{t:.2f}',(10,530),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
    tiles.append(small)
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]
cv2.imwrite('previews/hoja.jpg',np.vstack(rows))
