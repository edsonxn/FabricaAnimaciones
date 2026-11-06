# -*- coding: utf-8 -*-
"""Paquete compacto de flow/lote.json para inyectarlo en la página de Flow (el navegador integrado no comparte el
portapapeles ni ve 127.0.0.1): los textos largos repetidos van una vez en window.__D y cada prompt los cita como ~N~.
  python videos/llamada_domingo/flow_bundle.py [kind,kind...] [desde_id]  -> flow/_bundle_<kinds>.js"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
os.chdir(AQUI)
import guion as g  # noqa: E402
import flow_lote as fl  # noqa: E402

kinds = (sys.argv[1] if len(sys.argv) > 1 else "esc").split(",")
L = [x for x in json.load(open("flow/lote.json", encoding="utf-8")) if x["kind"] in kinds and x.get("prompt")]
F = g.FICHA
piezas = [F["estilo"] + ".", F["cierre"], fl.SIN_TEXTO, g._MISMA, g._LLAMADA, fl.LUGAR_AUDITORIO, fl.VALERIA]
piezas += [f"{F['nombres'][k]} is {v}" for k, v in F["personajes"].items()]
piezas += list(g.ESC.values()) + [v.rstrip(".") + "." for v in F["objetos"].values()]
piezas += ["Empty establishing shot, no people: ", "Setting: ", "Characters: ", "says in Mexican Spanish, ",
           "character reference. ", " looks exactly like the "]
piezas = sorted(set(piezas), key=len, reverse=True)
D, P = piezas, {}          # el diccionario es SIEMPRE el mismo (varios paquetes conviven en la página)
for x in L:
    t = x["prompt"]
    for i, p in enumerate(D):
        t = t.replace(p, f"~{i}~")
    P[x["id"]] = [t, x["ing"], x.get("d", 0)]
js = ("window.__D=" + json.dumps(D, ensure_ascii=False) + ";window.__P=Object.assign(window.__P||{}," +
      json.dumps(P, ensure_ascii=False) + ");window.__get=id=>window.__P[id][0].replace(/~(\d+)~/g,(m,n)=>window.__D[+n]);" +
      "Object.keys(window.__P).length")
out = f"flow/_bundle_{'_'.join(kinds)}.js"
open(out, "w", encoding="utf-8").write(js)
print(out, len(js), "caracteres ·", len(P), "prompts")
