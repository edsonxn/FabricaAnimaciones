# -*- coding: utf-8 -*-
"""Revisa que ningún MG/pegatina/ficha/rótulo se salga del cuadro ni se encime con otro (3-nov-2026, el usuario: «hay partes donde
se corta el texto»). Evalúa cada fn a lo largo de su duración, mide la caja de lo NÍTIDO (alfa > 200 y luz > 140 = texto, cifras,
bordes de pegatina; el humo difuso no cuenta) y la coloca como la pega secuencia_fx (centro en x*W, y*H, escala 1).
    python _bordes.py            (desde la carpeta del video; escribe previews/bordes.txt)
"""
import os
import sys

import gc

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import secuencia_fx as SF  # noqa: E402

W, H, MARGEN = 1920, 1080, 20
capa = SF.cargar()


def caja(img):
    a = img[..., 3].astype(np.int16)
    luz = img[..., :3].max(axis=2).astype(np.int16)
    m = (a > 200) & (luz > 140)
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return xs.min(), ys.min(), xs.max(), ys.max()


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


items = []
for d in capa.fx:
    if d["tipo"] != "mg":
        continue
    dur = d["a"] - d["de"]
    union = None
    for u in np.linspace(.08, .92, 7):
        img = d["fn"](u * dur, dur, d["_marcas"])
        c = caja(img)
        if c is None:
            continue
        cx, cy = d.get("x", .5) * W, d.get("y", .5) * H
        x0, y0 = cx - img.shape[1] / 2 + c[0], cy - img.shape[0] / 2 + c[1]
        x1, y1 = cx - img.shape[1] / 2 + c[2], cy - img.shape[0] / 2 + c[3]
        union = (x0, y0, x1, y1) if union is None else (min(union[0], x0), min(union[1], y0), max(union[2], x1), max(union[3], y1))
    if union:
        items.append(dict(nombre=d.get("nombre", "mg"), de=d["de"], a=d["a"], caja=union))
    d["fn"] = None                      # suelta las cachés del cierre (mapas de 4000 px): sin esto, MemoryError con 300+ FX
    gc.collect()

lineas = []
for it in items:
    x0, y0, x1, y1 = it["caja"]
    fuera = {k: round(v) for k, v in (("izq", MARGEN - x0), ("der", x1 - (W - MARGEN)), ("arriba", MARGEN - y0),
                                        ("abajo", y1 - (H - MARGEN))) if v > 0}
    if fuera:
        lineas.append(f"FUERA  {mmss(it['de'])}-{mmss(it['a'])}  {it['nombre']}  {fuera}")
for i, p in enumerate(items):
    for q in items[i + 1:]:
        t = min(p["a"], q["a"]) - max(p["de"], q["de"])
        if t < .3:
            continue
        ax0, ay0, ax1, ay1 = p["caja"]
        bx0, by0, bx1, by1 = q["caja"]
        iw, ih = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
        if iw <= 0 or ih <= 0:
            continue
        menor = min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0))
        if iw * ih > .08 * menor:
            lineas.append(f"ENCIMA {mmss(max(p['de'], q['de']))} ({t:.1f} s)  {p['nombre']}  ×  {q['nombre']}  ({iw * ih / menor:.0%})")
os.makedirs("previews", exist_ok=True)
open(os.path.join("previews", "bordes.txt"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")
print(f"{len(items)} MG revisados · {sum(l.startswith('FUERA') for l in lineas)} fuera · {sum(l.startswith('ENCIMA') for l in lineas)} encimados")
print("\n".join(lineas))
