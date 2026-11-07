# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026): cuadro real (clip + capa de efectos) en el segundo en que la voz dice cada frase.
previews/promesas_NN.jpg (12 por hoja). Las frases y lo que debería verse: PROMESAS de abajo (copiadas a promesas.md).
    python _promesas.py            (desde la carpeta del video)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py
import secuencia_fx as SF  # noqa: E402

PROMESAS = [   # (frase ancla, + s, qué debería verse)
    ("veías cuadros de Mario, de Peach", 1.0, "cuadros Mario/Peach/Bowser"),
    ("cuadros ya no están. Y Nintendo", 0.5, "ventana remake sin cuadros"),
    ("en el Rancho Lon Lon y en la Fortaleza", 0.3, "cuadros Skyward Sword 3DS"),
    ("con un ojo dibujado", 0.3, "lupa con ojo"),
    ("se pone en la cara", 0.3, "gafas en la cara (remake)"),
    ("lo entendiste?", 0.2, "Kaepora pregunta (N64)"),
    ("con flores en el suelo", 0.3, "grutas con flores"),
    ("correcto brilla en verde", 0.3, "tronco brilla verde"),
    ("Navi te interrumpía con esto", 1.2, "Hey! de Navi"),
    ("llegabas a su fuente", 0.3, "fuente Gran Hada"),
    ("pide una ofrenda de rupias", 0.5, "ofrenda de rupias"),
    ("había tres archivos de guardado", 0.5, "3 archivos de guardado"),
    ("inclinaba el cartucho", 0.5, "cartucho inclinado"),
    ("una de las cadenas y saltar al centro", 0.3, "trepar cadena N64"),
    ("Link resbala al intentar subir", 0.6, "Link resbala (remake)"),
    ("escupía sangre roja", 0.2, "sangre roja Ganon"),
    ("Ganondorf cae de rodillas", 0.5, "Ganon de rodillas habla"),
    ("guardia se asomaba", 0.8, "guardia asoma (N64)"),
    ("se va bordando con tu aventura", 0.2, "tapiz bordado"),
    ("la bomba sigue en su sitio", 0.2, "guardia sigue"),
    ("Talon en el pecho", 0.0, "broche Bowser en Talon"),
]


def main():
    capa = SF.cargar()
    S = capa.S
    minis = []
    mw, mh = 480, 270
    filas = []
    for frase, dt, que in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except Exception as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {que}"
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
    for frase, t, bid, que in filas:
        print(f"{int(t // 60)}:{t % 60:04.1f}\t{bid}\t{frase}\t{que}")


if __name__ == "__main__":
    main()
