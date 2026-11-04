# -*- coding: utf-8 -*-
"""Plan de clips de bt_50_secretos (3-nov-2026): une plan_a.json (beats 001-086) y plan_b.json (087-173), que escribieron dos agentes
MIRANDO hojas de contacto propias a 360p (ver_a/, ver_b/; caché E:/…/cache360) sobre la serie Ninbanyan «Banjo-Tooie NSO 100 %»
(widescreen, sin narrador: sin recorte, su audio sirve para ambiente_por) + otras fuentes anotadas por beat. Verificaciones en
catalogo_frases_a.md y catalogo_frases_b.md. Escribe busquedas.json e imprime ambiente_por para SECUENCIA en guion.py.
    python plan_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def _palabras(beats):
    """Lista de (palabra normalizada, i_beat, fracción dentro del beat)."""
    out = []
    for i, b in enumerate(beats):
        ws = [w.strip(".,:;¿?¡!…«»\"").lower() for w in b["texto"].split()]
        ws = [w for w in ws if w]
        out += [(w, i, k / max(1, len(ws))) for k, w in enumerate(ws)]
    return out


def remapear(plan, viejos, nuevos):
    """Los agentes planearon sobre beats_plan.json; al regrabar s24/s20/s16 los cortes cambiaron. Cada beat nuevo toma el clip del
    beat viejo donde cae su PRIMERA palabra (alineando el texto con difflib), con `desde` corrido lo que ya llevaba ese beat."""
    import difflib
    pv, pn = _palabras(viejos), _palabras(nuevos)
    sm = difflib.SequenceMatcher(None, [w for w, _, _ in pv], [w for w, _, _ in pn], autojunk=False)
    n2v = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            n2v[b + k] = a + k
    out, primera = {}, {}
    for k, (_, i, _) in enumerate(pn):
        primera.setdefault(i, k)
    for i, b in enumerate(nuevos):
        k = primera[i]
        while k not in n2v and k > 0:
            k -= 1
        _, iv, frac = pv[n2v.get(k, 0)]
        v = viejos[iv]
        p = dict(plan[v["id"]])
        corr = round(frac * (v["t1"] - v["t0"]), 2)
        if corr > .3:
            p["desde"] = round(float(p["desde"]) + corr, 2)
            p["nota"] = p.get("nota", "") + f" (remapeado de {v['id']} +{corr} s)"
        out[b["id"]] = p
    return out


# Correcciones a mano tras el remapeo: el clip de la tapa de Jamjars dura 12 s (no da para dos beats).
FIJO = {"scene-153": {"fuente": "P03", "id": "5PjYuSAZBJQ", "desde": 1105.0, "ambiente": None, "nota": "Jamjars en su silo"}}
# P01 de 0 a 878 s va en 4:3 dentro del marco NSO (aviso de la sesión 1): recorte por lado.
RECORTE = {"scene-063": .144}
# medir_brillo.py (3-nov; 062 y 076 además recortados 1,1 y 0,8 s al principio con ffmpeg: son cartelas de créditos de 8,7 s entre negros): negros de transición al final de estos clips (y uno de 2 s en medio del 091) → se corre `desde`.
AJUSTE = {"scene-001": -.8, "scene-020": -.5, "scene-046": -.4, "scene-062": -1.5, "scene-076": -1.6, "scene-081": -.4,
          "scene-091": 7.76}


def cargar():
    plan = {}
    for f in ("plan_a.json", "plan_b.json"):
        plan.update(json.load(open(os.path.join(AQUI, f), encoding="utf-8")))
    return plan


if __name__ == "__main__":
    beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
    plan = cargar()
    viejos = json.load(open(os.path.join(AQUI, "beats_plan.json"), encoding="utf-8"))
    if [b["texto"] for b in viejos] != [b["texto"] for b in beats]:
        plan = remapear(plan, viejos, beats)
        json.dump(plan, open(os.path.join(AQUI, "plan_remapeado.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("plan remapeado a los beats nuevos -> plan_remapeado.json")
    plan.update(FIJO)
    falta = [b["id"] for b in beats if b["id"] not in plan]
    assert not falta, f"faltan beats en el plan: {falta}"
    out, usos, amb = {}, {}, {}
    for b in beats:
        p = plan[b["id"]]
        vid, s = p["id"], round(float(p["desde"]) + AJUSTE.get(b["id"], 0), 2)
        for s2, i2 in usos.get(vid, []):
            if abs(s - s2) < 25:
                print(f"AVISO {b['id']}: {p.get('fuente', vid)} {s} a {abs(s - s2):.0f} s de {i2}")
        usos.setdefault(vid, []).append((s, b["id"]))
        out[b["id"]] = {"url": f"https://youtu.be/{vid}", "desde": s}
        if p.get("ambiente"):
            amb[b["id"]] = float(p["ambiente"])
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    cuenta = {}
    for p in plan.values():
        cuenta[p.get("fuente", p["id"])] = cuenta.get(p.get("fuente", p["id"]), 0) + 1
    print(f"busquedas.json: {len(out)} beats, {len(usos)} videos")
    print("ambiente_por = " + repr(amb))
    print("recorte_por = " + repr(RECORTE))
    print("beats por fuente: " + ", ".join(f"{k} {v}" for k, v in sorted(cuenta.items())))
