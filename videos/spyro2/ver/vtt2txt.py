import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
src, dst = sys.argv[1], sys.argv[2]
out=[]; last=""
txt=open(src,encoding="utf-8").read().split("\n\n")
for b in txt:
    lines=b.strip().split("\n")
    m=None
    for i,l in enumerate(lines):
        m=re.match(r"(\d+):(\d+):(\d+)\.(\d+) -->",l)
        if m: ts=int(m[1])*3600+int(m[2])*60+int(m[3])+int(m[4])/1000; body=lines[i+1:]; break
    if not m: continue
    t=" ".join(re.sub(r"<[^>]+>","",x).strip() for x in body).strip()
    if t and t!=last:
        out.append(f"[{ts:8.1f}] {t}"); last=t
open(dst,"w",encoding="utf-8").write("\n".join(out))
print(len(out))
