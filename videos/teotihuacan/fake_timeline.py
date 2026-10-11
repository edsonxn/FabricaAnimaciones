# -*- coding: utf-8 -*-
"""Timeline PROVISIONAL (0.075 s por carácter) para desarrollar las escenas antes de tener la voz real."""
import json, re, importlib.util
spec = importlib.util.spec_from_file_location("guion", "guion.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
t = 1.1
escenas = []
for k, e in enumerate(g.ESCENAS):
    t0 = t
    t += 0.3
    frases = []
    for i, txt in enumerate(e["frases"]):
        ws = txt.split()
        dur = max(1.0, len(txt) * 0.062)
        tot = sum(len(w) for w in ws)
        tt = t
        words = []
        for w in ws:
            d = dur * len(w) / tot
            words.append(dict(w=w, s=round(tt, 3), e=round(tt + d, 3)))
            tt += d
        frases.append(dict(key=f"{e['id']}_{i}", texto=txt, t0=round(t, 3), t1=round(t + dur, 3), words=words))
        t += dur + g.GAP
    t += e.get("post", 0.4)
    escenas.append(dict(id=e["id"], claves=[], t0=round(t0, 3), t1=round(t, 3), compases=1, frases=frases,
                        fin_voz=round(t, 3), beats=[]))
tl = dict(bpm=100, beat=0.6, unidad=2.4, total=round(t, 3), titulo=g.TITULO, estilo=g.ESTILO_VISUAL, escenas=escenas,
          transiciones=[["continua", 0.1]] * (len(escenas) - 1), provisional=True)
json.dump(tl, open("timeline.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("total", tl["total"])
