# Subtítulos automáticos YouTube (.vtt) -> líneas «seg texto» sin repeticiones: python lotl_vtt.py <entrada.vtt> <salida.txt>
import re, sys
out, ult = [], ""
t = 0
for ln in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"(\d\d):(\d\d):(\d\d)\.\d+ -->", ln)
    if m:
        t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        continue
    tx = re.sub(r"<[^>]+>", "", ln).strip()
    if not tx or tx == ult or tx.startswith(("WEBVTT", "Kind:", "Language:")):
        continue
    ult = tx
    out.append(f"{t} {tx}")
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
print(len(out), "lineas; ultimo seg", t)
