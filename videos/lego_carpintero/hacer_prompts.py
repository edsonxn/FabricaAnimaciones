# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) cruzando beats.json con timeline.json POR TIEMPO: cada beat toma la descripción
(_imagenes.D) de la frase que más suena dentro de él; si esa frase ya se usó en el beat anterior, toma su siguiente variante
o, sin variantes, la misma con otro encuadre. Clips combinados: escena A = frase en [t0, t_medio], escena B = [t_medio, t1].
Sobrevive a cualquier recorte de `beats` (mejora pendiente del manual de Wild Next Door, 12-oct-2026).
   python hacer_prompts.py [--lista]"""
import json
import sys

import guion
from _imagenes import D

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
ENCUADRES = ["Seen in a close-up from a low angle", "Seen from a high wide angle", "Seen from the side in a medium shot"]
TRANS = [  # transiciones del clip combinado, una distinta por clip
    "plasticine toy bricks rain down and snap together across the frame into a wall, then the wall falls apart revealing scene two",
    "a cloud of curly wood shavings sweeps across the frame and when it passes we are in scene two",
    "the plasticine scene squashes and is remolded by clay hands into scene two",
    "the camera pushes into the round stud on top of a toy brick until the circle fills the frame and opens into scene two",
    "a sheet of plasticine peels away like a page, revealing scene two underneath",
    "a wooden pull-along toy duck rolls across the frame toward the camera, covers it, and rolls away revealing scene two",
    "orange plasticine flames lick up from the bottom of the frame and when they fall away we are in scene two",
    "the camera rushes through a small-paned workshop window into scene two",
]

tl = json.load(open("timeline.json", encoding="utf-8"))
FR = [(f["key"], f["t0"], f["t1"]) for e in tl["escenas"] for f in e["frases"]]
falt = [k for k, _, _ in FR if k not in D]
assert not falt, f"frases sin descripción: {falt}"


def frase_en(t0, t1):
    """La frase que más suena en [t0, t1]; si ya se usó y otra frase sin usar suena ≥ 0,6 s en el beat, esa (más frases distintas)."""
    sol = sorted(((min(t1, f[2]) - max(t0, f[1]), f[0]) for f in FR), reverse=True)
    if sol[0][0] <= 0:
        return min(FR, key=lambda f: abs(f[1] - t0))[0]
    for s, k in sol:
        if s >= 0.6 and k not in usos:
            return k
    return sol[0][1]


usos = {}


def desc(k):
    n = usos.get(k, 0)
    usos[k] = n + 1
    v = D[k]
    return v[n] if n < len(v) else f"{ENCUADRES[(n - len(v)) % 3]}: {v[-1]}"


beats = json.load(open("beats.json", encoding="utf-8"))
beats = beats["beats"] if isinstance(beats, dict) else beats
P, nclip = {}, 0
for b in beats:
    if b["tipo"] == "video":
        tm = b.get("t_medio") or (b["t0"] + b["t1"]) / 2
        a, c = desc(frase_en(b["t0"], tm)), desc(frase_en(tm, b["t1"]))
        P[b["id"]] = (f"{E}Scene one, first five seconds: {a}. Then {TRANS[nclip % len(TRANS)]}. "
                      f"Scene two, last five seconds: {c}.{C}")
        nclip += 1
    else:
        P[b["id"]] = f"{E}{desc(frase_en(b['t0'], b['t1']))}.{C}"
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(P), "prompts;", nclip, "clips; frases sin usar:", [k for k, _, _ in FR if k not in usos])
if "--lista" in sys.argv:
    sys.stdout.reconfigure(encoding="utf-8")
    for b in beats:
        print(b["id"][6:], f"{b['t0']:6.1f}", b["texto"][:55], "||", P[b["id"]][len(E):len(E) + 80])
