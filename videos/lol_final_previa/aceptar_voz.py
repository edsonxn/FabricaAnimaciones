# -*- coding: utf-8 -*-
"""Acepta la mejor toma de las frases dadas (tras LEER su transcripción en voz/eval.json): guarda cer/tail medidos en voz_aceptada.json.
uso: python aceptar_voz.py clave1 clave2 ...   (o --todas-menos j1 j2 ... para las de regenerar.json salvo esas escenas)"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__))
ev = json.load(open(os.path.join(D, "voz", "eval.json"), encoding="utf-8"))
p = os.path.join(D, "voz_aceptada.json")
ace = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
keys = sys.argv[1:]
if keys and keys[0] == "--todas-menos":
    fuera = set(keys[1:])
    keys = [k for k in json.load(open(os.path.join(D, "voz", "regenerar.json"))) if k.rsplit("_", 1)[0] not in fuera]
for k in keys:
    c = [m for m in ev.values() if m["key"] == k]
    if not c:
        print("sin toma:", k); continue
    m = min(c, key=lambda m: m["cer"])
    ace[k] = [round(m["cer"] + .002, 3), round(max(m["tail_ratio"] + .02, .35), 2)]
    print(k, ace[k], m["hyp"][:90])
json.dump(ace, open(p, "w", encoding="utf-8"), indent=0)
