# python vtt.py archivo.vtt desde hasta  -> texto sin repeticiones con tiempo relativo a 'desde'
import re, sys
f, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
txt = open(f, encoding="utf-8").read()
vist = set()
for blk in txt.split("\n\n"):
    m = re.search(r"(\d+):(\d+):(\d+)\.(\d+) -->", blk)
    if not m:
        continue
    t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
    if not (a <= t <= b):
        continue
    for ln in blk.split("\n")[1:]:
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if ln and "-->" not in ln and ln not in vist:
            vist.add(ln)
            print(f"{t - a:6.0f} {ln}")
