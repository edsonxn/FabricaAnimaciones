"""Junta candidatos a momento gracioso: picos del heatmap («lo más repetido») + minutos citados en
comentarios con risa. Para cada candidato imprime la transcripción automática de ±25 s.
Uso: python candidatos.py [--sin-texto]  → candidatos.txt
"""
import glob, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(AQUI, "fuentes")
RISA = re.compile(r"(?i)(ja ?ja|jaja|xd|😂|🤣|lol|jsjs|me mat|me muero|me ca[ií]|risa|gracios|buen[ií]simo|jeje)")
TS = re.compile(r"(?<!\d)(\d{1,2}):(\d{2})(?::(\d{2}))?(?!\d)")


def subs(vid):
    for pat in (vid + ".es-orig.json3", vid + ".es.json3"):
        p = os.path.join(F, pat)
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            out = []
            for ev in d.get("events", []):
                txt = "".join(s.get("utf8", "") for s in ev.get("segs", []) or []).strip()
                if txt:
                    out.append((ev["tStartMs"] / 1000, txt.replace("\n", " ")))
            return out
    return []


def ventana(sub, t0, t1):
    return " ".join(x for t, x in sub if t0 <= t <= t1)


filas = []
for info in sorted(glob.glob(os.path.join(F, "*.info.json"))):
    d = json.load(open(info, encoding="utf-8"))
    vid, dur = d["id"], d.get("duration") or 0
    cands = []
    hm = d.get("heatmap") or []
    if hm:
        vals = [h["value"] for h in hm]
        orden = sorted(range(len(hm)), key=lambda i: -vals[i])
        for i in orden:
            if i < 3:  # el arranque siempre es alto
                continue
            if vals[i] < 0.35:
                break
            # máximo local
            if (i > 0 and vals[i - 1] > vals[i]) or (i + 1 < len(vals) and vals[i + 1] > vals[i]):
                continue
            cands.append(("heat%.2f" % vals[i], hm[i]["start_time"]))
            if len([c for c in cands if c[0].startswith("heat")]) >= 4:
                break
    for c in d.get("comments") or []:
        txt = c.get("text", "")
        for m in TS.finditer(txt):
            h, mnt, s = m.groups()
            seg = int(h) * 3600 + int(mnt) * 60 + int(s) if s else int(h) * 60 + int(mnt)
            if 0 < seg < dur and (RISA.search(txt) or c.get("like_count", 0) >= 2):
                cands.append(("com♥%d «%s»" % (c.get("like_count", 0), txt[:90].replace("\n", " ")), seg))
    if not cands:
        continue
    sub = subs(vid)
    filas.append("=" * 100)
    filas.append("%s  %s  (%d min, %s vistas)" % (vid, d.get("title"), dur // 60, d.get("view_count")))
    for etq, t in sorted(cands, key=lambda c: c[1]):
        filas.append("  [%d:%02d] %s" % (t // 60, t % 60, etq))
        if "--sin-texto" not in sys.argv and sub:
            filas.append("      " + ventana(sub, t - 20, t + 30)[:700])

open(os.path.join(AQUI, "candidatos.txt"), "w", encoding="utf-8").write("\n".join(filas))
print(len(filas), "líneas")
