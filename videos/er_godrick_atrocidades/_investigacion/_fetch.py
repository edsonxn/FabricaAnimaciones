import json,sys,urllib.request,urllib.parse,os
base=sys.argv[1]; out=sys.argv[2]
for t in sys.argv[3:]:
    u=base+'/api.php?action=parse&page='+urllib.parse.quote(t)+'&prop=wikitext&format=json&formatversion=2&redirects=1'
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
        w=d.get('parse',{}).get('wikitext','') or ('ERR '+json.dumps(d.get('error')))
    except Exception as e: w='EXC '+str(e)
    fn=os.path.join(out,t.replace('/','__').replace(' ','_').replace(':','_')+'.txt')
    open(fn,'w',encoding='utf-8').write(w); print(t,len(w))
