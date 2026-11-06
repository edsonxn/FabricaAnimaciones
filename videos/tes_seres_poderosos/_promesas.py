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
    ("te cambia la cara por un queso", 1.2, "Sheogorath / el queso"),
    ("un dios que ve el tiempo", 1.0, "Akatosh"),
    ("Esta es la tabla que salió", 1.0, "tier list de las voces"),
    ("nos escribió: no pude con", 0.8, "comentario real @ebre1976"),
    ("lo atraviesa con un tentáculo", 0.6, "Hermaeus Mora / tentáculo"),
    ("Sotha Sil", 0.5, "Sotha Sil"),
    ("la Valla Fantasma", 0.4, "la Valla Fantasma"),
    ("flotó una roca gigante", 2.6, "roca flotante / Ministerio de la Verdad"),
    ("Y Vivec lo detuvo en el aire", 0.8, "Vivec / roca detenida"),
    ("te entrega el guantelete", 0.6, "el guantelete (Wraithguard)"),
    ("en la Garganta del Mundo", 0.5, "Garganta del Mundo / Alduin"),
    ("le dice al humano tras el telón", 0.8, "comentario real @krisstianblackgao1726"),
    ("ves sus santuarios por todas partes", 0.8, "santuario de Talos"),
    ("El Numidium", 0.4, "el Numidium"),
    ("Un gigante de cuatro brazos", 1.0, "Dagon gigante en la Ciudad Imperial"),
    ("Y pierde contra un dragón de fuego", 0.6, "Akatosh dragón de fuego vs Dagon"),
    ("el Wabbajack", 0.4, "el Wabbajack"),
    ("te da el Oghma Infinium", 0.6, "el Oghma Infinium"),
    ("Donde cayó se formó la Montaña Roja", 0.8, "Montaña Roja"),
    ("oyes a la Madre Noche", 0.6, "Madre Noche (ataúd) + su voz"),
    ("Este es el podio", 0.8, "podio Anu / Padomay / Godhead"),
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
