# muestrea N cuadros de videos de YouTube -> hoja de contacto (para elegir ingredientes)
import sys, subprocess, json, os
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
out = sys.argv[1]; n = int(sys.argv[2]); ids = sys.argv[3:]
os.makedirs(out, exist_ok=True)
def url(v):
    r = subprocess.run(['yt-dlp','-f','bv*[height<=1080][ext=mp4]/bv*[height<=1080]','-g','--print','duration','https://youtu.be/'+v],capture_output=True,text=True)
    l = r.stdout.strip().splitlines()
    return float(l[0]), l[-1]
def grab(v,u,t):
    f=f'{out}/{v}_{int(t)}.jpg'
    if not os.path.exists(f):
        subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',u,'-frames:v','1','-q:v','2','-y',f])
    return f
for v in ids:
    try: d,u = url(v)
    except Exception as e: print(v,'ERR',e); continue
    ts=[d*(i+0.5)/n for i in range(n)]
    with ThreadPoolExecutor(6) as ex: fs=list(ex.map(lambda t: grab(v,u,t), ts))
    th=[];W=4;tw=480
    for f,t in zip(fs,ts):
        if not os.path.exists(f): continue
        im=Image.open(f).convert('RGB'); im.thumbnail((tw,270)); c=Image.new('RGB',(tw,290),(30,30,30)); c.paste(im,(0,0))
        ImageDraw.Draw(c).text((4,272),f'{v} t={int(t)}',fill='yellow'); th.append(c)
    if not th: print(v,"sin cuadros"); continue
    s=Image.new('RGB',(W*tw,((len(th)+W-1)//W)*290))
    for i,c in enumerate(th): s.paste(c,((i%W)*tw,(i//W)*290))
    s.save(f'{out}/_hoja_{v}.jpg',quality=80); print(v,'ok',len(th))
