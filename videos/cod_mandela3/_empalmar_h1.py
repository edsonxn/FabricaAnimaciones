# -*- coding: utf-8 -*-
"""Empalme de beats tras meter al intruso «Turbo» en el puesto 12 (19-nov-2026), SIN volver a bajar los clips ya revisados.
- beats 001-043 (antes del p12): iguales (la voz de antes no cambió).
- tramo nuevo [inicio del viejo 044, inicio del viejo 048 + D]: se corta de nuevo (~8,6 s) y lleva clips NUEVOS de OITC.
- viejos 048-110: se desplazan D segundos y se renumeran; su clip (medios/), búsqueda y fuente van con ellos.
Respaldo de todo lo anterior en _v1_antes_h1/. Uso: python _empalmar_h1.py  (desde la carpeta del video; una sola vez)."""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import secuencia as S  # noqa: E402

V1 = "_v1_antes_h1"
viejos = json.load(open(f"{V1}/beats.json", encoding="utf-8"))
tl_v = json.load(open(f"{V1}/timeline.json", encoding="utf-8"))
tl = json.load(open("timeline.json", encoding="utf-8"))
ESC_V = {e["id"]: e for e in tl_v["escenas"]}
D = round([e for e in tl["escenas"] if e["id"] == "p11"][0]["t0"] - ESC_V["p11"]["t0"], 3)
print("desplazamiento", D)
# lo de antes del p12 no se movió
for e in tl["escenas"]:
    if e["id"] == "p12":
        break
    assert abs(e["t0"] - ESC_V[e["id"]]["t0"]) < 1e-3, e["id"]

I_A, I_B = 43, 47                      # índices (0-based) del viejo 044 y del viejo 048
a, b = viejos[I_A]["t0"], round(viejos[I_B]["t0"] + D, 3)
pal = S._palabras(tl)
ts = [a] + S._cortes(pal, a, b, 8.6) + [b]
tramo = []
for i in range(len(ts) - 1):
    t0, t1 = ts[i], ts[i + 1]
    tramo.append(dict(t0=round(t0, 3), t1=round(t1, 3), tipo="video",
                      texto=" ".join(p["w"] for p in pal if t0 - 0.13 <= p["s"] < t1 - 0.13), clip_s=8))
m = len(tramo)
nuevos = [dict(x) for x in viejos[:I_A]] + tramo
mapa = {}                              # id viejo -> id nuevo (solo los desplazados)
for x in viejos[I_B:]:
    y = dict(x)
    y["t0"], y["t1"] = round(x["t0"] + D, 3), round(x["t1"] + D, 3)
    nuevos.append(y)
for k, x in enumerate(nuevos):
    nid = f"scene-{k + 1:03d}"
    if k >= I_A + m:
        mapa[x["id"]] = nid
    x["id"] = nid
nuevos[-1]["t1"] = tl["total"]
# el texto de los desplazados se recalcula con el timeline nuevo (debe ser el mismo)
for x in nuevos[I_A + m:]:
    x["texto"] = " ".join(p["w"] for p in pal if x["t0"] - 0.13 <= p["s"] < x["t1"] - 0.13)
TRAMO_IDS = [nuevos[I_A + i]["id"] for i in range(m)]
print(f"tramo: {m} beats ({TRAMO_IDS[0]}..{TRAMO_IDS[-1]}) · viejos 048-110 -> {mapa['scene-048']}..{mapa['scene-110']}")
for x in nuevos[I_A - 1:I_A + m + 1]:
    print(f"  {x['id']} {x['t0']:7.2f}-{x['t1']:7.2f} {x['texto'][:100]}")
# los desplazados deben decir lo mismo que antes
for x, y in zip(viejos[I_B:], nuevos[I_A + m:]):
    if x["texto"] != y["texto"]:
        print("  OJO texto distinto", x["id"], "->", y["id"], "|", x["texto"][:60], "|", y["texto"][:60])
if os.environ.get("SECO"):
    raise SystemExit("(seco: no se tocó nada)")

# ---- medios: los viejos 044-047 al respaldo; los desplazados se renombran de mayor a menor (suben de número)
os.makedirs(f"{V1}/medios_044_047", exist_ok=True)
for x in viejos[I_A:I_B]:
    r = S.medio_de(x)
    if r:
        shutil.move(r, os.path.join(V1, "medios_044_047", os.path.basename(r)))
for viejo in sorted(mapa, reverse=True):
    r = S.medio_de(dict(id=viejo))
    assert r, viejo
    destino = os.path.join("medios", mapa[viejo] + os.path.splitext(r)[1])
    assert not os.path.exists(destino), destino
    os.replace(r, destino)

# ---- busquedas y fuentes
bq = json.load(open(f"{V1}/busquedas.json", encoding="utf-8"))
nbq = {k: v for k, v in bq.items() if k < viejos[I_A]["id"]}
for viejo, nuevo in mapa.items():
    if viejo in bq:
        nbq[nuevo] = bq[viejo]
FIJOS = [  # OITC de Black Ops 1 (Vikkstar, ya revisado en la 1.ª vuelta: sin facecam ni marca) en tramos que no se usaron
    ("nLo5EAbkZLo", 55.0), ("nLo5EAbkZLo", 64.5), ("nLo5EAbkZLo", 86.0), ("nLo5EAbkZLo", 96.0), ("nLo5EAbkZLo", 106.0),
    ("nLo5EAbkZLo", 116.0), ("nLo5EAbkZLo", 126.0), ("nLo5EAbkZLo", 136.0), ("nLo5EAbkZLo", 145.0)]
for i, sid in enumerate(TRAMO_IDS):
    if i < len(FIJOS):
        vid, desde = FIJOS[i]
        nbq[sid] = {"url": f"https://youtu.be/{vid}", "desde": desde}
    else:
        nbq[sid] = ["Modern Warfare 2 Takedown Ghost no commentary", "Modern Warfare 2 Cliffhanger no commentary"]   # «Sigamos. En el once… Ghost»
json.dump(dict(sorted(nbq.items())), open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fu = json.load(open("fuentes.json", encoding="utf-8"))
shutil.copyfile("fuentes.json", f"{V1}/fuentes.json")
nfu = {k: v for k, v in fu.items() if k.startswith("_") or k < viejos[I_A]["id"]}
for viejo, nuevo in mapa.items():
    if viejo in fu:
        nfu[nuevo] = fu[viejo]
rech = fu.get("_rechazados", {})
nfu["_rechazados"] = {mapa.get(k, k): v for k, v in rech.items() if not (viejos[I_A]["id"] <= k < viejos[I_B]["id"])}
json.dump(nfu, open("fuentes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

json.dump(nuevos, open("beats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.copyfile("timeline.json", "timeline_beats.json")
json.dump(dict(D=D, tramo=TRAMO_IDS, mapa=mapa), open(f"{V1}/mapa_beats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"beats.json: {len(nuevos)} beats · total {tl['total']} · mapa en {V1}/mapa_beats.json")
