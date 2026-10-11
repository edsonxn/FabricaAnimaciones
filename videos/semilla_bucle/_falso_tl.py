import json
import guion as g

t = 0.0
esc = []
for k, e in enumerate(g.ESCENAS):
    t0 = t
    cur = t + e.get("pre", 0.35 if k else 1.2)
    fr = []
    for i, txt in enumerate(e["frases"]):
        ws = []
        s = cur
        for w in txt.split():
            d = 0.15 + 0.055 * len(w)
            ws.append(dict(w=w, s=round(s, 3), e=round(s + d, 3)))
            s += d + 0.04
        fr.append(dict(key=f"{e['id']}_{i}", texto=txt, t0=round(cur, 3), t1=round(s, 3), words=ws))
        cur = s + 0.28
    t = cur + e.get("post", 0.4) + 0.25
    esc.append(dict(id=e["id"], t0=round(t0, 3), t1=round(t, 3), frases=fr, fin_voz=round(cur, 3), compases=1, beats=4))

# Ajustamos para que encaje con BPM 100
total_dur = round(t, 3)
tl_dict = dict(
    bpm=g.BPM,
    beat=round(60.0 / g.BPM, 3),
    unidad=4,
    total=total_dur,
    titulo=g.TITULO,
    estilo="boceto",
    escenas=esc,
    transiciones=[
        dict(t=esc[i]["t1"], t0=esc[i]["t1"] - 0.05, t1=esc[i]["t1"] + 0.05, tipo="continua", de=esc[i]["id"], a=esc[i + 1]["id"])
        for i in range(len(esc) - 1)
    ]
)

with open("timeline.json", "w", encoding="utf-8") as f:
    json.dump(tl_dict, f, ensure_ascii=False, indent=1)

print("Duracion total simulada:", total_dur)
for e in esc:
    print(f"  Escena {e['id']}: t0={e['t0']:.2f}, fin_voz={e['fin_voz']:.2f}, t1={e['t1']:.2f}")
