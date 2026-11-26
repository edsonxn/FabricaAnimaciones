# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026): cuadro real (clip + capa de efectos) en el segundo en que la voz dice cada frase.
previews/promesas_NN.jpg (12 por hoja). Las frases y lo que debería verse: PROMESAS de abajo (copiadas a promesas.md).
Copiado de wow_errores_60/_promesas.py (25-nov-2026); PROMESAS automáticas, una por frase.
    python _promesas.py            (desde la carpeta del video)   ·   python _promesas.py --md   (reescribe promesas.md)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py

import re as _re
import guion as _g
PROMESAS = []   # automático (25-nov-2026): una por frase; ancla = primeras palabras únicas; «qué» = lo que nombra la frase
_vistos = set()
for _e in _g.ESCENAS:
    for _i, _f in enumerate(_e["frases"]):
        _p = _f.split()
        for _n in range(6, len(_p) + 1):
            _a = " ".join(_p[:_n])
            if sum(x.count(_a) for e in _g.ESCENAS for x in e["frases"]) == 1 and _a not in _vistos:
                break
        _vistos.add(_a)
        PROMESAS.append((_a, 2.0, f"{_e['id']}_{_i} " + _re.sub(r"\s+", " ", _f[len(_a):len(_a) + 46])))

def md():
    with open("promesas.md", "w", encoding="utf-8") as f:
        f.write("# Promesas visuales — wow_ruta_profesiones\n\n| frase | +s | cómo se ve |\n|---|---|---|\n")
        for fr, dt, q in PROMESAS:
            f.write(f"| {fr} | {dt} | {q} |\n")


def main():
    import secuencia_fx as SF
    capa = SF.cargar()
    S = capa.S
    minis = []
    mw, mh = 480, 270
    filas = []
    for frase, dt, que in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except BaseException as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{len(minis) + 1} {int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {que}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
        filas.append((frase, t, b["id"], que))
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    for i, (frase, t, bid, que) in enumerate(filas):
        print(f"{i + 1}\t{int(t // 60)}:{t % 60:04.1f}\t{bid}\t{frase}\t{que}")


if __name__ == "__main__":
    if "--md" in sys.argv:
        md()
    else:
        main()
