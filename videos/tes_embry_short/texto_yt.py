"""Transcripción palabra por palabra de cada clip a partir de los subtítulos automáticos de YouTube (json3),
con tiempos RELATIVOS al clip (sin GPU). → segmentos/clips/<clave>.yt.json  e imprime líneas con tiempo.
Uso: python texto_yt.py [clave ...]"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from bajar_clips import CAND, ANTES, DESPUES  # noqa: E402

F = os.path.join(AQUI, "fuentes")
D = os.path.join(AQUI, "segmentos", "clips")


def palabras(vid):
    for pat in (vid + ".es-orig.json3", vid + ".es.json3"):
        p = os.path.join(F, pat)
        if os.path.exists(p):
            out = []
            for ev in json.load(open(p, encoding="utf-8")).get("events", []):
                t0 = ev.get("tStartMs", 0)
                for s in ev.get("segs") or []:
                    w = s.get("utf8", "").strip()
                    if w:
                        out.append(((t0 + s.get("tOffsetMs", 0)) / 1000, w))
            return out
    return []


for c in sys.argv[1:] or list(CAND):
    vid, t = CAND[c]
    a = max(0, t - ANTES)
    ws = [(round(x - a, 2), w) for x, w in palabras(vid) if a <= x <= t + DESPUES]
    json.dump(ws, open(os.path.join(D, c + ".yt.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("=====", c, vid, "(clip desde %d:%02d)" % (a // 60, a % 60))
    linea, t0 = [], None
    for x, w in ws:
        if t0 is None:
            t0 = x
        linea.append(w)
        if len(linea) >= 14:
            print("  %5.1f  %s" % (t0, " ".join(linea))); linea, t0 = [], None
    if linea:
        print("  %5.1f  %s" % (t0, " ".join(linea)))
