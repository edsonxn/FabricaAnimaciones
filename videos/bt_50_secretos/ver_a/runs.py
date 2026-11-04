import cv2,os,sys
CACHE=r"E:\FabricaAnimaciones\videos\bt_50_secretos\cache360"
def runs(p,a,b,st=0.3,thr=14,crop=(22,138)):
    cap=cv2.VideoCapture(os.path.join(CACHE,p+".mp4"));t=a;cur=None;out=[]
    while t<=b:
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read()
        m=0
        if ok:
            g=cv2.cvtColor(cv2.resize(f,(160,90)),cv2.COLOR_BGR2GRAY);m=float(g[:,crop[0]:crop[1]].mean())
        on=14<=m<=235 if thr==14 else m>=thr
        if on and cur is None: cur=t
        if not on and cur is not None: out.append((round(cur,1),round(t-st,1)));cur=None
        t+=st
    if cur is not None: out.append((round(cur,1),b))
    return out
if __name__=="__main__":
    p,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
    print(p,[r for r in runs(p,a,b) if r[1]-r[0]>=4])
