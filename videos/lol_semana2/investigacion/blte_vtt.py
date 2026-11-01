# Subtítulos automáticos (.vtt) -> texto por bloques con segundo del VOD: python blte_vtt.py <dir> -> <dir>/<vid>.txt
import glob, os, re, sys
d = sys.argv[1]
SEG = 8
for f in glob.glob(os.path.join(d, "*.es.vtt")):
    vid = os.path.basename(f).split(".")[0]
    t = None; vistos = []; out = {}
    for ln in open(f, encoding="utf-8"):
        ln = ln.strip()
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+ --> ", ln)
        if m:
            t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]); continue
        if not ln or t is None or "<c>" in ln or ln.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if ln and ln not in vistos[-3:]:
            vistos.append(ln)
            out.setdefault(t // SEG * SEG, []).append(ln)
    with open(os.path.join(d, vid + ".txt"), "w", encoding="utf-8") as w:
        for k in sorted(out):
            w.write(f"{k:5d} {' '.join(out[k])}\n")
    print(vid, len(out))
