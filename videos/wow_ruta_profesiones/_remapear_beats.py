# -*- coding: utf-8 -*-
"""Reordenar escenas sin perder los clips (25-nov-2026: la promo de Overgear pasa de 2:20 a entre minería y herrería, y cada
parada gana una pausa de 6,5 s para su lista de compras). `secuencia reajustar` no sirve porque supone el mismo orden.

Cada beat viejo se parte en trozos por escena (un beat que cruzaba de una escena a otra queda en dos) y cada trozo se ancla
a sus palabras en el timeline NUEVO (misma frase = misma clave). Luego se ordena todo por tiempo, cada trozo dura hasta el
siguiente (las pausas nuevas las cubre el trozo anterior), se renumera scene-001… y se renombran los clips de medios/ (el
segundo trozo de un beat partido lleva una copia del mismo clip). Guarda _renumeracion_25nov.json (viejo -> nuevo).
  python _remapear_beats.py <beats_viejo.json> <timeline_viejo.json>   (lee timeline.json nuevo; escribe beats.json)"""
import json
import os
import shutil
import sys

D = os.path.dirname(os.path.abspath(__file__))
bv = json.load(open(sys.argv[1], encoding="utf-8"))
tv = json.load(open(sys.argv[2], encoding="utf-8"))
tn = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))


def palabras(tl):
    out = []
    for e in tl["escenas"]:
        for fr in e["frases"]:
            for j, w in enumerate(fr["words"]):
                out.append(dict(esc=e["id"], key=fr["key"], j=j, s=w["s"], w=w["w"]))
    return out


pv, pn = palabras(tv), {(p["key"], p["j"]): p for p in palabras(tn)}
esc_n = {e["id"]: e for e in tn["escenas"]}
trozos = []
for b in bv:
    ws = [p for p in pv if b["t0"] - 0.13 <= p["s"] < b["t1"] - 0.13]
    if not ws:
        continue
    grupos = []
    for p in ws:
        if not grupos or grupos[-1][0]["esc"] != p["esc"]:
            grupos.append([])
        grupos[-1].append(p)
    for gi, g in enumerate(grupos):
        p0 = g[0]
        nw = pn.get((p0["key"], p0["j"]))
        if nw is None:            # frase reescrita con otro número de palabras: proporcional dentro de la frase
            nw = next(q for q in pn.values() if q["key"] == p0["key"])
        lead = (p0["s"] - b["t0"]) if gi == 0 else 0.25
        t0 = max(esc_n[p0["esc"]]["t0"] if gi else 0.0, nw["s"] - lead)
        trozos.append(dict(viejo=b["id"], parte=gi, t0=round(t0, 3), b=b, n_pal=len(g)))
trozos.sort(key=lambda x: x["t0"])
total = tn["total"]
nuevos, mapa = [], {}
for i, z in enumerate(trozos):
    t1 = trozos[i + 1]["t0"] if i + 1 < len(trozos) else total
    nid = f"scene-{i + 1:03d}"
    d = {k: v for k, v in z["b"].items() if k not in ("t_medio", "texto_a", "texto_b")}
    d.update(id=nid, t0=z["t0"], t1=round(t1, 3))
    nuevos.append(d)
    mapa[nid] = dict(viejo=z["viejo"], parte=z["parte"])
nuevos[0]["t0"] = 0.0
pal_n = sorted(pn.values(), key=lambda p: p["s"])
for d in nuevos:
    d["texto"] = " ".join(p["w"] for p in pal_n if d["t0"] - 0.13 <= p["s"] < d["t1"] - 0.13)
assert all(d["t1"] > d["t0"] for d in nuevos), "beat de duración ≤ 0"
# clips: copiar a nombres temporales y luego a los definitivos (sin pisar nada a medias)
M = os.path.join(D, "medios")
tmp = os.path.join(M, "_renum")
os.makedirs(tmp, exist_ok=True)
for nid, m in mapa.items():
    shutil.copy2(os.path.join(M, m["viejo"] + ".mp4"), os.path.join(tmp, nid + ".mp4"))
os.makedirs(os.path.join(M, "_antes_renum"), exist_ok=True)
for f in os.listdir(M):
    if f.startswith("scene-") and f.endswith(".mp4"):
        shutil.move(os.path.join(M, f), os.path.join(M, "_antes_renum", f))
for f in os.listdir(tmp):
    shutil.move(os.path.join(tmp, f), os.path.join(M, f))
os.rmdir(tmp)
json.dump(nuevos, open(os.path.join(D, "beats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.copyfile(os.path.join(D, "timeline.json"), os.path.join(D, "timeline_beats.json"))
json.dump(mapa, open(os.path.join(D, "_renumeracion_25nov.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
partidos = [k for k, v in mapa.items() if v["parte"]]
print(f"{len(bv)} beats viejos -> {len(nuevos)} nuevos · partidos: {partidos} · total {total:.2f} s")
for d in nuevos:
    if d["t1"] - d["t0"] > 14:
        print("  largo:", d["id"], mapa[d["id"]]["viejo"], round(d["t1"] - d["t0"], 1), "s")
