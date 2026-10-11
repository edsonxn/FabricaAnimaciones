# Línea de tiempo SINTÉTICA para probar imágenes antes de tener la voz real (la etapa `tiempo` la reemplaza).
import json, re
import guion as G
t = 0.0
esc = []
for e in G.ESCENAS:
    t0 = t
    t += e.get("pre", 0.0)
    frs = []
    for i, txt in enumerate(e["frases"]):
        s = t
        ws = []
        for w in txt.split():
            d = 0.16 + 0.045 * len(re.sub(r"[^\wáéíóúñ]", "", w))
            ws.append(dict(w=w, s=round(t, 3), e=round(t + d, 3)))
            t += d
        frs.append(dict(key=f"{e['id']}_{i}", texto=txt, t0=round(s, 3), t1=round(t, 3), words=ws))
        t += G.GAP
    fin_voz = t
    t += e.get("post", 0.0)
    esc.append(dict(id=e["id"], pre=e.get("pre", 0.0), t0=round(t0, 3), t1=round(t, 3), compases=1, frases=frs, fin_voz=round(fin_voz, 3), beats=1))
tr = [dict(t=esc[i]["t1"], t0=esc[i]["t1"] - .05, t1=esc[i]["t1"] + .05, tipo="continua", de=esc[i]["id"], a=esc[i + 1]["id"]) for i in range(len(esc) - 1)]
json.dump(dict(bpm=84.0, beat=60 / 84, unidad=4, total=round(t, 3), titulo=G.TITULO, estilo=G.ESTILO_VISUAL, escenas=esc, transiciones=tr),
          open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total", round(t, 1))
