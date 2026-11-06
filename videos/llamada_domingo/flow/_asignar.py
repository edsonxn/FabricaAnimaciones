# -*- coding: utf-8 -*-
"""Asigna cada clip bajado (previews/originales/nNN.mp4) a su beat comparando Whisper con el diálogo de PLANOS.
  python flow/_asignar.py           -> tabla + copia a medios/scene-NNN.mp4 (solo si la asignación es clara)"""
import json, os, re, sys, shutil, difflib
sys.path.insert(0, os.getcwd())
import guion as g

W = json.load(open("flow/_whisper.json", encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-záéíóúñü ]", "", s.lower())
beats = {}
for k, pl in enumerate(g.PLANOS):
    if pl["tipo"] in ("clip", "llamada"):
        beats[f"scene-{k + 1:03d}"] = norm(" ".join(l for _, _, l in pl["dialogo"]))
hechos = {"scene-002", "scene-003", "scene-004", "scene-006", "scene-008"}
filas = []
for f, segs in sorted(W.items()):
    if not f.startswith("n"):
        continue
    txt = norm(" ".join(s[2] for s in segs))
    cands = sorted(((difflib.SequenceMatcher(None, txt, d).ratio(), b) for b, d in beats.items() if b not in hechos),
                   reverse=True)
    filas.append((f, cands[0][1], round(cands[0][0], 2), round(cands[1][0], 2), txt[:70]))
usados = {}
for f, b, r1, r2, txt in filas:
    usados.setdefault(b, []).append((r1, f))
print("archivo  beat       ratio  2.º   texto")
for f, b, r1, r2, txt in filas:
    dup = " DUP" if len(usados[b]) > 1 else ""
    print(f"{f:8} {b} {r1:5} {r2:5}{dup}  {txt}")
if "--copiar" in sys.argv:
    for b, lst in usados.items():
        r1, f = max(lst)
        shutil.copy2(f"previews/originales/{f}", f"medios/{b}.mp4")
    print("copiados:", len(usados))
faltan = [b for b in beats if b not in usados and b not in hechos]
print("sin clip:", faltan)
