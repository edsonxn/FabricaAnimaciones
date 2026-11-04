# hoja de contacto: python hoja.py PNN desde hasta paso [salida] [cols]
import sys,os,cv2,numpy as np
CACHE=r"E:\FabricaAnimaciones\videos\bt_50_secretos\cache360"
p,a,b,st=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
cols=int(sys.argv[6]) if len(sys.argv)>6 else 4
out=sys.argv[5] if len(sys.argv)>5 and sys.argv[5]!="-" else f"{p}_{int(a)}_{int(b)}.jpg"
cap=cv2.VideoCapture(os.path.join(CACHE,p+".mp4"))
ts=[];t=a
while t<=b+1e-6: ts.append(t);t+=st
W,H=int(1280/cols),int(1280/cols*9/16)
fr=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read()
    if not ok: f=np.zeros((360,640,3),np.uint8)
    f=cv2.resize(f,(W,H))
    cv2.putText(f,f"{p} {t:g}",(4,16),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),3)
    cv2.putText(f,f"{p} {t:g}",(4,16),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),1)
    fr.append(f)
while len(fr)%cols: fr.append(np.zeros((H,W,3),np.uint8))
rows=[np.hstack(fr[i:i+cols]) for i in range(0,len(fr),cols)]
img=np.vstack(rows)
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)),out),img,[cv2.IMWRITE_JPEG_QUALITY,80])
print(out,img.shape)
