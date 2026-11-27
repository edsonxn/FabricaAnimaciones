# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026): cuadro real (clip + capa de efectos) de cada frase de la voz y lo que se ve mientras
la dice. Copiado y ampliado de wow_ruta_profesiones/_promesas.py (subagente C, 26-nov-2026):
  - promesas.md: una fila por frase con su segundo, el beat (clip scene-NNN) y TODO lo que la capa enseña durante la frase
    (mapas con sus puntos, tarjetas, tooltips de Wowhead, pegatinas, MG, rótulos, Flow).
  - previews/promesas_NN.jpg: el cuadro a +2 s de cada frase (12 por hoja; un clip que aún falta sale como tarjeta «falta»).
    python _promesas.py            (desde la carpeta del video)   ·   python _promesas.py --md   (solo promesas.md)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py

import json  # noqa: E402

import secuencia_fx as SF  # noqa: E402

capa = SF.cargar()
S = capa.S
tl = json.load(open("timeline.json", encoding="utf-8"))
FRASES = [(f["key"], f["t0"], f["t1"], f["texto"]) for e in tl["escenas"] for f in e["frases"]]
mmss = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"


def que_se_ve(t0, t1):
    """Nombres de los FX visibles durante [t0, t1) (sin el fondo de marca)."""
    out = []
    for d in capa.fx:
        if d["tipo"] in ("mg", "pantalla", "imagen", "video") and d["de"] < t1 and d["a"] > t0:
            n = d.get("nombre") or (f"apoyo {os.path.basename(d.get('ruta', ''))}" if d["tipo"] == "imagen" else d["tipo"])
            if d["tipo"] == "imagen":
                n = "tooltip/ficha de interfaz"
            out.append(n)
    out += [f"rótulo «{r['texto']}»" for r in capa.rot if r["de"] < t1 and r["a"] > t0]
    return out


def md():
    with open("promesas.md", "w", encoding="utf-8") as f:
        f.write("# Promesas visuales — wow_oro_30_50\n\nUna fila por frase de la voz: qué se ve mientras la dice (clip del beat + capa "
                "de efectos). Cuadros: `previews/promesas_NN.jpg` (a +2 s de cada frase). Lo que la voz nombra y no está en la capa "
                "lo enseña el clip del beat (subagente A, `fuentes.json`).\n\n| # | frase | s | beat | lo que se ve |\n|---|---|---|---|---|\n")
        for i, (k, t0, t1, tx) in enumerate(FRASES):
            b = capa.beat_en(t0 + .3)["id"]
            ve = " · ".join(dict.fromkeys(que_se_ve(t0, t1))) or "solo el clip"
            f.write(f"| {i + 1} | {k}: {tx[:70]}… | {mmss(t0)} | {b} | {ve} |\n")
    print("promesas.md:", len(FRASES), "frases")


def main():
    md()
    minis, mw, mh = [], 480, 270
    for i, (k, t0, t1, tx) in enumerate(FRASES):
        t = t0 + min(2.0, (t1 - t0) / 2)
        kb = next((j for j, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[kb]
        f = capa.aplicar(capa.envolver(S._fuente(b, kb, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{i + 1} {mmss(t)} {b['id'][6:]} {k} {tx[:40]}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 8), cv2.FONT_HERSHEY_SIMPLEX, .45, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)


if __name__ == "__main__":
    if "--md" in sys.argv:
        md()
    else:
        main()
