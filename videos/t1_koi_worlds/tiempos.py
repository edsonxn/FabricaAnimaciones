# python tiempos.py clave1 clave2 ... [+s] → t0 + s (por defecto +2,5) de cada frase, en una línea para ver.py
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
F = {f["key"]: f for e in t["escenas"] for f in e["frases"]}
s = 2.5
ks = [a for a in sys.argv[1:] if not a.startswith("+")]
for a in sys.argv[1:]:
    if a.startswith("+"):
        s = float(a[1:])
print(" ".join(f"{F[k]['t0'] + s:.1f}" for k in ks))
