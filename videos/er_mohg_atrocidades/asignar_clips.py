# -*- coding: utf-8 -*-
"""Convierte el plan de clips POR FRASE (plan_frases.json: {"p5_3": [{"url", "desde", "nota"}, ...]}, hecho mirando hojas de
contacto) en busquedas.json POR BEAT ({"scene-012": {"url", "desde"}}), como en zelda_oot/plan_clips.py (27-oct-2026).
Cada beat toma la frase con la que más se solapa; los beats de una misma frase rotan sus opciones y, si se repite una opción,
avanzan 14 s dentro del mismo video para no repetir plano. Respeta los beats ya fijados a mano en busquedas.json (`--conservar`).
    python asignar_clips.py [--conservar]
"""
import json
import sys

SALTO = 14


def main():
    beats = json.load(open("beats.json", encoding="utf-8"))
    tl = json.load(open("timeline.json", encoding="utf-8"))
    plan = json.load(open("plan_frases.json", encoding="utf-8"))
    frases = [(f["key"], f["t0"], f["t1"]) for e in tl["escenas"] for f in e["frases"]]
    prev = {}
    if "--conservar" in sys.argv:
        try:
            prev = json.load(open("busquedas.json", encoding="utf-8"))
        except FileNotFoundError:
            pass
    usos, out, faltan = {}, {}, []
    for b in beats:
        if b["id"] in prev and isinstance(prev[b["id"]], dict) and prev[b["id"]].get("_mano"):
            out[b["id"]] = prev[b["id"]]
            continue
        sol = [(min(b["t1"], t1) - max(b["t0"], t0), k) for k, t0, t1 in frases]
        sol = [s for s in sol if s[0] > 0]
        if not sol:                                       # pausa entre frases: la frase más cercana
            k = min(frases, key=lambda f: min(abs(f[1] - b["t1"]), abs(f[2] - b["t0"])))[0]
        else:
            k = max(sol)[1]
        ops = plan.get(k) or []
        if not ops:
            faltan.append((b["id"], k))
            continue
        n = usos.get(k, 0)
        usos[k] = n + 1
        o = ops[n % len(ops)]
        out[b["id"]] = {"url": o["url"], "desde": int(o["desde"]) + SALTO * (n // len(ops)), "_frase": k}
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"busquedas.json: {len(out)} de {len(beats)} beats")
    for i, k in faltan:
        print("  SIN PLAN", i, k)


if __name__ == "__main__":
    main()
