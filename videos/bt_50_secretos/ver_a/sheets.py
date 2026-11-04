import json,sys,os,cv2,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import plan_a
beats=json.load(open(r"C:\FabricaAnimaciones\videos\bt_50_secretos\beats.json",encoding="utf-8"))
CACHE=r"E:\FabricaAnimaciones\videos\bt_50_secretos\cache360"
OUT=r"C:\FabricaAnimaciones\videos\bt_50_secretos\ver_a"
W,H=256,144
def frames(n):
    b=beats[n-1];dur=b["t1"]-b["t0"]
    p,t0,amb,nota=plan_a.PLAN[n]
    cap=cv2.VideoCapture(os.path.join(CACHE,p+".mp4"));ims=[]
    for k in (0.3,dur*0.5,dur-0.3):
        cap.set(cv2.CAP_PROP_POS_MSEC,(t0+k)*1000);ok,f=cap.read()
        if not ok: f=np.zeros((360,640,3),np.uint8)
        f=cv2.resize(f,(W,H))
        cv2.putText(f,f"{n} {p} {t0+k:.0f}",(3,13),cv2.FONT_HERSHEY_SIMPLEX,.42,(0,0,0),3)
        cv2.putText(f,f"{n} {p} {t0+k:.0f}",(3,13),cv2.FONT_HERSHEY_SIMPLEX,.42,(0,255,255),1)
        ims.append(f)
    return ims
per=6
for si,start in enumerate(range(1,87,per)):
    ims=[]
    for n in range(start,min(start+per,87)): ims+=frames(n)
    while len(ims)%5: ims.append(np.zeros((H,W,3),np.uint8))
    rows=[np.hstack(ims[i:i+5]) for i in range(0,len(ims),5)]
    cv2.imwrite(os.path.join(OUT,f"plan_{si+1:02d}.jpg"),np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,78])
print("ok")
