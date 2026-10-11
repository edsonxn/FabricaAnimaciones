# Línea de tiempo SINTÉTICA (ritmo medido de Faraon: 2,37 palabras/s) para probar imágenes antes de tener la voz real. La etapa `tiempo` la reemplaza.
import json, re, math
import guion as G
BPM = G.BPM
BEAT = 60 / BPM
BAR = BEAT * 4
t = 0.0
esc = []
for e in G.ESCENAS:
    t0 = t
    t += e.get("pre", 0.0)
    frs = []
    for i, txt in enumerate(e["frases"]):
        s = t
        ws = []
        toks = txt.split()
        tot = len(toks) / 2.37
        pesos = [0.4 + len(re.sub(r"[^\wáéíóúñ]", "", w)) for w in toks]
        k = tot / sum(pesos)
        for w, p in zip(toks, pesos):
            d = p * k
            ws.append(dict(w=w, s=round(t, 3), e=round(t + d, 3)))
            t += d
        frs.append(dict(key=f"{e['id']}_{i}", texto=txt, t0=round(s, 3), t1=round(t, 3), words=ws))
        t += G.GAP
    fin_voz = t
    t += e.get("post", 0.0)
    n = max(1, math.ceil((t - t0) / BAR))
    t = t0 + n * BAR
    esc.append(dict(id=e["id"], pre=e.get("pre", 0.0), t0=round(t0, 3), t1=round(t, 3), compases=n, frases=frs, fin_voz=round(fin_voz, 3), beats=n * 4))
tr = [dict(t=esc[i]["t1"], t0=esc[i]["t1"] - .05, t1=esc[i]["t1"] + .05, tipo="continua", de=esc[i]["id"], a=esc[i + 1]["id"]) for i in range(len(esc) - 1)]
json.dump(dict(bpm=float(BPM), beat=BEAT, unidad=4, total=round(t, 3), titulo=G.TITULO, estilo=G.ESTILO_VISUAL, escenas=esc, transiciones=tr),
          open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total", round(t, 1), "s =", f"{int(t // 60)}:{int(t % 60):02d}")
for e in esc:
    print(f"  {e['id']:11s} {e['t0']:6.1f}-{e['t1']:6.1f}")
