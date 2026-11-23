import json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
ids=[]
for ln in open('_candidatos.txt'):
    p=ln.split(); ids+= [(p[0],i) for i in p[1:]]
def f(x):
    n,i=x
    try:
        r=subprocess.run(['yt-dlp','-j','--no-warnings','--skip-download','https://youtu.be/'+i],capture_output=True,text=True,encoding='utf-8',timeout=90)
        d=json.loads(r.stdout); h=max((fm.get('height') or 0) for fm in d['formats'])
        return n,i,h,d.get('duration'),d.get('channel'),d.get('title')[:60]
    except Exception as e: return n,i,'ERR',str(e)[:60],'',''
with ThreadPoolExecutor(6) as ex:
    res=list(ex.map(f,ids))
out=[]
for r in res: out.append(' | '.join(map(str,r)))
open('_meta.txt','w',encoding='utf-8').write('\n'.join(out)); print('\n'.join(out))
