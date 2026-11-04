# tiras del texto superior: python tira.py PNN desde hasta paso salida [y0 y1]
import sys,os,cv2,numpy as np
CACHE=r"E:\FabricaAnimaciones\videos\bt_50_secretos\cache360"
p,a,b,st,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
y0=int(sys.argv[6]) if len(sys.argv)>6 else 0; y1=int(sys.argv[7]) if len(sys.argv)>7 else 44
cap=cv2.VideoCapture(os.path.join(CACHE,p+".mp4"))
fr=[];t=a
while t<=b+1e-6:
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read()
    if not ok: f=np.zeros((360,640,3),np.uint8)
    c=f[y0:y1,:].copy()
    cv2.putText(c,f"{t:g}",(560,y1-y0-4),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,255,255),1)
    fr.append(c);t+=st
if len(fr)%2: fr.append(np.zeros_like(fr[0]))
rows=[np.hstack(fr[i:i+2]) for i in range(0,len(fr),2)]
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)),out),np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
