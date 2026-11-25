# Subtítulos automáticos .vtt -> líneas "<seg> texto" sin repeticiones: python vtt_txt.py in.vtt out.txt
import re, sys
txt = open(sys.argv[1], encoding="utf-8").read()
out = []; vistos = set()
for bloque in txt.split("\n\n"):
    m = re.search(r"(\d+):(\d+):(\d+)\.(\d+) -->", bloque)
    if not m: continue
    s = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
    for ln in bloque.split("\n")[1:]:
        if "-->" in ln or "<c>" in ln or not ln.strip(): continue
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if ln and ln not in vistos:
            vistos.add(ln); out.append(f"{s} {ln}")
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out)); print(len(out))
