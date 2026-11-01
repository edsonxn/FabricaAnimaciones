import json,os,sys
AQUI="C:/FabricaAnimaciones/videos/sociedad_1200"
sys.path[:0]=[AQUI,"C:/FabricaAnimaciones/nucleo"]
os.chdir(AQUI)
import cv2, numpy as np
TL=json.load(open("timeline.json",encoding="utf-8")); IDS=[e["id"] for e in TL["escenas"]]
import escenas as S
d=[e for e in TL["escenas"] if e["id"]=="gancho"][0]
esc=S.CLASES["gancho"](d,0)
esc.busto=type("B",(),{"dibujar":lambda *a,**k:None,"punta":lambda *a,**k:(0,0)})()
import comun as _C
_C.banda=lambda *a,**k:None
t=float(sys.argv[1]); cx,cy,z=float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
esc.cam1=lambda tt:(cx,cy,z)
esc.t_callan=-1; esc.t_orden=1e9
im=(np.clip(esc.render(None,t),0,1)*255).astype(np.uint8)
cv2.imwrite(sys.argv[5],cv2.cvtColor(im,cv2.COLOR_RGB2BGR)); print(im.shape)
