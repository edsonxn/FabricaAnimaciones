import sys,re,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
L=open(sys.argv[1],encoding="utf-8").read().split("\n")
out=[]
prev_tail=""
for l in L:
    m=re.match(r"\[\s*([\d.]+)\] (.*)",l)
    if not m: continue
    t,txt=float(m[1]),m[2]
    txt=re.sub(r"\[(Music|Applause)\]","",txt).strip()
    if not txt: continue
    # quitar lo ya emitido (prefijo repetido)
    if prev_tail and txt.startswith(prev_tail): new=txt[len(prev_tail):].strip()
    else:
        # buscar solapamiento: sufijo de prev_tail igual a prefijo de txt
        new=txt
        for k in range(min(len(prev_tail),len(txt)),8,-1):
            if prev_tail.endswith(txt[:k]): new=txt[k:].strip(); break
    if new:
        out.append((t,new)); 
    prev_tail=txt
for t,x in out: print(f"[{t:8.1f}] {x}")
