import json,sys,os,cv2,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import importlib,plan_a; importlib.reload(plan_a)
beats=json.load(open(r"C:\FabricaAnimaciones\videos\bt_50_secretos\beats.json",encoding="utf-8"))
CACHE=r"E:\FabricaAnimaciones\videos\bt_50_secretos\cache360"
sel=[int(a) for a in sys.argv[1:]] or list(range(1,87))
for n in sel:
    b=beats[n-1]; dur=b["t1"]-b["t0"]+0.3
    p,t0,amb,nota=plan_a.PLAN[n]
    cap=cv2.VideoCapture(os.path.join(CACHE,p+".mp4"))
    raros=[];t=0
    while t<dur+0.5:
        cap.set(cv2.CAP_PROP_POS_MSEC,(t0+t)*1000);ok,f=cap.read()
        if not ok: raros.append((round(t,1),"sinframe"));t+=.3;continue
        g=cv2.cvtColor(cv2.resize(f,(160,90)),cv2.COLOR_BGR2GRAY)
        m=float(g[:,22:138].mean())
        if m<14 or m>235: raros.append((round(t,1),"N" if m<14 else "B"))
        t+=.3
    print(n,p,t0,round(dur,1),"OK" if not raros else raros)
