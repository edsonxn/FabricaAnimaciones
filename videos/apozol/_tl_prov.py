# -*- coding: utf-8 -*-
"""Línea de tiempo PROVISIONAL (sin voz) para desarrollar las escenas: estima cuándo se dice cada palabra (≈ 3,2 palabras/s).
Cuando exista la voz real, `python fab.py apozol tiempo` la sustituye."""
import json
import re
import sys

sys.path.insert(0, ".")
import guion as G

BPM = 108.0
beat = 60 / BPM
bar = 4 * beat
t = 0.0
escenas = []
for k, e in enumerate(G.ESCENAS):
    t0 = t
    tt = t0 + e.get("pre", 0.35)
    frases = []
    for i, tx in enumerate(e["frases"]):
        ws = []
        t_f = tt
        for w in tx.split():
            dur = 0.09 + 0.036 * len(re.sub(r"\W", "", w))
            ws.append(dict(w=w, s=round(tt, 3), e=round(tt + dur, 3)))
            tt += dur
            if w.endswith((",", ".", ":", "?", "!")):
                tt += 0.22
        frases.append(dict(key=f"{e['id']}_{i}", texto=tx, t0=round(t_f, 3), t1=round(tt, 3), words=ws))
        tt += 0.25
    fin_voz = tt - 0.25
    tt += e.get("post", 0.35)
    n = max(1, int(-(-(tt - t0) // bar)))
    t1 = t0 + n * bar
    escenas.append(dict(id=e["id"], t0=round(t0, 4), t1=round(t1, 4), compases=n, frases=frases, fin_voz=round(fin_voz, 3), beats=n * 2))
    t = t1
trans = [dict(t=a["t1"], t0=round(a["t1"] - 0.065, 4), t1=round(a["t1"] + 0.035, 4), tipo="continua", de=a["id"], a=b["id"]) for a, b in zip(escenas, escenas[1:])]
out = dict(bpm=BPM, beat=beat, unidad=4, total=round(t, 2), titulo=G.TITULO, estilo=G.ESTILO_VISUAL, escenas=escenas, transiciones=trans)
json.dump(out, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False)
print("total", out["total"], "s;", len(escenas), "escenas")
