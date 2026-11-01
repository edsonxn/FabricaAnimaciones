# -*- coding: utf-8 -*-
"""timeline.json PROVISIONAL (antes de la voz): palabras a ~2,55 por segundo, para ir armando y viendo tomas. `fab.py jalpa tiempo`
lo reemplaza por el real; como las escenas se anclan a palabras con T(), se reacomodan solas."""
import json

import guion as g

VEL, GAP = 2.55, g.GAP
t = 0.0
esc = []
for e in g.ESCENAS:
    t0 = t
    t += e.get("pre", 0.0)
    frs = []
    for i, fr in enumerate(e["frases"]):
        ws = []
        for w in fr.split():
            d = max(0.16, len(w) * 0.062) * (2.55 / VEL)
            ws.append(dict(w=w, s=round(t, 3), e=round(t + d, 3)))
            t += d + 0.07
            if w[-1] in ",:;":
                t += 0.18
            if w[-1] in ".?!":
                t += 0.30
        frs.append(dict(key=f"{e['id']}_{i}", texto=fr, t0=ws[0]["s"], t1=ws[-1]["e"], words=ws))
        t += GAP
    fin = t
    t += e.get("post", 0.4)
    esc.append(dict(id=e["id"], pre=e.get("pre", 0.0), t0=round(t0, 3), t1=round(t, 3), frases=frs, fin_voz=round(fin, 3)))
TL = dict(bpm=g.BPM, beat=60 / g.BPM, unidad=1, total=round(t, 3), titulo=g.TITULO, estilo=g.ESTILO_VISUAL, escenas=esc,
          transiciones=[list(x) for x in g.TRANSICIONES], provisional=True)
json.dump(TL, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("timeline provisional:", TL["total"], "s", [(e["id"], e["t0"], e["t1"]) for e in esc])
