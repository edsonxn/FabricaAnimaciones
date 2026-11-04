# python cap1080.py PNN t1 t2 ... -> cuadros 1080p ver_a/hd_PNN_t.jpg
import sys,subprocess,os
ids=dict(l.split() for l in open(r"C:\Users\jaire\AppData\Local\Temp\claude\C--FabricaAnimaciones\0e220f8f-881b-4085-a513-7e5850844f54\scratchpad\ids.txt") if l.strip())
p=sys.argv[1]
r=subprocess.run(["yt-dlp","--no-warnings","-g","-f","bv*[height<=1080][height>=720]","--",ids[p]],capture_output=True,text=True)
url=r.stdout.strip().splitlines()[0]
here=os.path.dirname(os.path.abspath(__file__))
for t in sys.argv[2:]:
    out=os.path.join(here,f"hd_{p}_{t}.jpg")
    for k in range(3):
        rr=subprocess.run(["ffmpeg","-y","-v","error","-ss",t,"-i",url,"-frames:v","1","-q:v","3",out],capture_output=True,text=True)
        if os.path.exists(out): break
    print(out,os.path.exists(out),rr.stderr[-100:])
