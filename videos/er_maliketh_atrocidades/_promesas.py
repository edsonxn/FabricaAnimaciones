# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026) + ESCENAS IMPORTANTES (regla 18-nov-2026) de er_maliketh_atrocidades.
Cuadro real (clip + capa de efectos) en el segundo en que la voz lo dice → previews/promesas_NN.jpg (12 por hoja),
y escribe promesas.md y escenas.md.      python _promesas.py            (desde la carpeta del video)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py
import secuencia_fx as SF  # noqa: E402

from _promesas_lista import PROMESAS  # noqa: E402


def main():
    capa = SF.cargar()
    S = capa.S
    minis, filas = [], []
    mw, mh = 480, 270
    for frase, dt, que, como, esc in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except Exception as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        fuente = S._fuente(b, k, True, capa)
        f = capa.aplicar(capa.envolver(fuente, b).cuadro(t), t)
        if getattr(fuente, "cap", None) is not None:      # cerrar el clip (sin esto, 140 cuadros se quedaban sin RAM)
            fuente.cap.release()
        del fuente
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{len(filas) + 1} {int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {'E ' if esc else ''}{que}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .45, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
        filas.append((frase, t, b["id"], que, como, esc))
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    mm = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
    pm = ["# Promesas visuales — er_maliketh_atrocidades (regla del 5-nov-2026)", "",
          "Hoja: previews/promesas_NN.jpg (cuadro real clip + capa de FX en ese segundo; «E» = escena importante).", "",
          "| n | segundo | beat | qué se nombra | cómo se ve |", "|---|---|---|---|---|"]
    es = ["# Escenas importantes — er_maliketh_atrocidades (regla del 18-nov-2026)", "",
          "Cada una con el clip REAL de ese momento (sin Flow); la pegatina va encima o después.", "",
          "| segundo | beat | escena | cómo se ve |", "|---|---|---|---|"]
    for i, (frase, t, bid, que, como, esc) in enumerate(filas, 1):
        pm.append(f"| {i} | {mm(t)} | {bid[6:]} | {que} | {como} |")
        if esc:
            es.append(f"| {mm(t)} | {bid[6:]} | {que} | {como} |")
    open("promesas.md", "w", encoding="utf-8").write("\n".join(pm) + "\n")
    open("escenas.md", "w", encoding="utf-8").write("\n".join(es) + "\n")
    print(len(filas), "promesas;", sum(f[5] for f in filas), "escenas")


if __name__ == "__main__":
    main()
