# -*- coding: utf-8 -*-
"""Reasigna los 135 clips ya bajados y revisados a los beats NUEVOS tras cambiar la voz a siete voces (3-nov-2026).
Cada beat nuevo toma el clip del beat viejo (beats_v1.json) con más palabras en común; los que no tienen pareja (presentaciones de
las voces, votación) reciben clips viejos sobrantes cercanos en el tiempo (los tapa la placa de quién narra / la papeleta).
- medios/_v1/scene-NNN.mp4 = los clips viejos (hardlinks, mismo disco E:); `vid(n)` de efectos.py apunta ahí.
- medios/scene-NNN.mp4 = hardlink al clip asignado; busquedas.json y fuentes.json re-indexados; imprime el ambiente_por nuevo.
Uso (tras `fab.py tes_sentinel_teaser beats`): python _remapear.py [--seco]"""
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
SECO = "--seco" in sys.argv
# --de v2: versión de origen (beats_<v>.json, busquedas_<v>.json, fuentes_<v>.json, medios/_<v>/); v1 = la de una sola voz
VER = sys.argv[sys.argv.index("--de") + 1] if "--de" in sys.argv else "v1"
if VER == "v1":
    AMB_V1 = {"scene-014": .8, "scene-057": .8}
else:
    sys.path.insert(0, AQUI)
    import guion
    AMB_V1 = dict(guion.SECUENCIA["ambiente_por"])


def palabras(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z0-9']+", t) if len(w) >= 4}


viejos = json.load(open(f"beats_{VER}.json", encoding="utf-8"))
nuevos = json.load(open("beats.json", encoding="utf-8"))
pv = [palabras(b["texto"]) for b in viejos]
pn = [palabras(b["texto"]) for b in nuevos]
pares = []
for i, a in enumerate(pn):
    for j, b in enumerate(pv):
        if a and b:
            s = len(a & b) / min(len(a), len(b))
            if s >= .3:
                pares.append((s, i, j))
pares.sort(reverse=True)
asig, usados = {}, set()
for s, i, j in pares:
    if i not in asig and j not in usados:
        asig[i], usados = j, usados | {j}
sobran = [j for j in range(len(viejos)) if j not in usados]
huerfanos = [i for i in range(len(nuevos)) if i not in asig]
for i in huerfanos:   # clip viejo sobrante más cercano en tiempo (proporcional a la duración total)
    tn = nuevos[i]["t0"] / nuevos[-1]["t1"]
    if not sobran:
        j = min(range(len(viejos)), key=lambda j: abs(viejos[j]["t0"] / viejos[-1]["t1"] - tn))   # repite (último recurso)
    else:
        j = min(sobran, key=lambda j: abs(viejos[j]["t0"] / viejos[-1]["t1"] - tn))
        sobran.remove(j)
    asig[i] = j
print(f"{len(nuevos)} beats nuevos · {len(viejos)} viejos · por texto {len(nuevos) - len(huerfanos)} · huérfanos {len(huerfanos)} · "
      f"clips sin usar {len(sobran)}")
for i in huerfanos:
    print(f"  huérfano {nuevos[i]['id']} ← {viejos[asig[i]]['id']}: {nuevos[i]['texto'][:80]}")
if SECO:
    raise SystemExit
bus = json.load(open(f"busquedas_{VER}.json", encoding="utf-8"))
fue = json.load(open(f"fuentes_{VER}.json", encoding="utf-8"))
os.makedirs(f"medios/_{VER}", exist_ok=True)
for b in viejos:
    src, dst = f"medios/{b['id']}.mp4", f"medios/_{VER}/{b['id']}.mp4"
    if not os.path.exists(dst):
        os.link(src, dst)
for f in os.listdir("medios"):
    if re.fullmatch(r"scene-\d{3}\.mp4", f):
        os.remove(f"medios/{f}")
bus2, fue2 = {}, {k: v for k, v in fue.items() if not k.startswith("scene-")}
amb = {}
for i, b in enumerate(nuevos):
    vid = viejos[asig[i]]["id"]
    os.link(f"medios/_{VER}/{vid}.mp4", f"medios/{b['id']}.mp4")
    if vid in bus:
        bus2[b["id"]] = bus[vid]
    if vid in fue:
        fue2[b["id"]] = fue[vid]
    if vid in AMB_V1:
        amb[b["id"]] = AMB_V1[vid]
# huérfanos: búsqueda NUEVA (se bajan aparte con `bajar <lista> --rehacer`; mientras, llevan el clip de respaldo de arriba)
#  - con pareja de texto ya usada: la misma fuente {url, desde} 12 s más adelante (otro tramo del mismo video)
#  - sin pareja (presentaciones de las voces, votación): paisajes de Skyrim, uno distinto cada uno
PAISAJES = iter(["Skyrim tavern bard no HUD", "Skyrim Solitude cinematic no HUD", "Skyrim Markarth cinematic no HUD",
                 "Skyrim Riften cinematic no HUD", "Skyrim Windhelm cinematic no HUD", "Skyrim High Hrothgar cinematic no HUD",
                 "Skyrim Bannered Mare inn no HUD", "Skyrim College of Winterhold no HUD", "Skyrim Blackreach cinematic no HUD",
                 "Skyrim sunset cinematic no HUD", "Skyrim Dragonsreach throne no HUD", "Skyrim Sovngarde cinematic no HUD",
                 "Skyrim Falkreath cinematic no HUD", "Skyrim Dawnstar cinematic no HUD", "Skyrim Morthal cinematic no HUD"])
nuevas = []
for i in huerfanos:
    b = nuevos[i]
    mejor = max(range(len(viejos)), key=lambda j: len(pn[i] & pv[j]) / max(1, min(len(pn[i]), len(pv[j]))))
    s = len(pn[i] & pv[mejor]) / max(1, min(len(pn[i]), len(pv[mejor])))
    fu = bus.get(viejos[mejor]["id"])
    if s >= .3 and isinstance(fu, dict):
        bus2[b["id"]] = dict(fu, desde=round(fu["desde"] + 12, 1))
    else:
        bus2[b["id"]] = [next(PAISAJES), "Skyrim 4k no HUD"]
    fue2.pop(b["id"], None)
    nuevas.append(int(b["id"][-3:]))
print("bajar:", ",".join(map(str, nuevas)))
json.dump(bus2, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(fue2, open("fuentes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({b["id"]: viejos[asig[i]]["id"] for i, b in enumerate(nuevos)}, open("_remapeo.json", "w", encoding="utf-8"), indent=1)
print("ambiente_por nuevo:", amb)
