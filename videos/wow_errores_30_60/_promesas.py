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
    ("Pues no. Vas por el doce", 1.0, "MG curva 12 % / 88 %"),
    ("Barnil Jarropetra te pide", 1.0, "mapa Tuercespina + Barnil"),
    ("Capítulo uno: la uno", 2.0, "MG 15 páginas por capítulo"),
    ("es un homenaje a Ernest Hemingway", 1.5, "foto real de Hemingway"),
    ("ya casi no da nada", 0.5, "MG misión gris 4700 → 1100"),
    ("Este video lo patrocina Overgear", 1.0, "Overgear: logo + fondo de marca"),
    ("Marcos escribió: quién puede", 1.5, "comentario de Marcos"),
    ("Dolencia de resurrección durante diez", 1.0, "tarjeta Dolencia / ángel"),
    ("Los centros buenos de esta franja", 3.0, "carrusel Gadgetzan, Bahía, Kargath…"),
    ("el Baluarte, en las Tierras de la Peste", 1.5, "foto del Baluarte"),
    ("en el camino a Grom'gol", 1.0, "mapa Tuercespina con Grom'gol"),
    ("Una Blancoria corrupta te da", 1.5, "Tubérculo de blancoria"),
    ("Tod escribió que fue el mejor", 1.5, "comentario de Tod"),
    ("las Manoplas del Maestro de filos", 1.0, "Manoplas (reliquia del n.º 14)"),
    ("con el doctor Gregory Víctor", 1.0, "mapa Arathi + Gregory"),
    ("unas diez de oro", 1.0, "MG doble especialización"),
    ("el mineral de mitril", 1.0, "MG subasta cuero/mitril/tela"),
    ("Warr escribió: esto empieza", 1.5, "comentario de Warr"),
    ("el Devastador de Herod", 1.0, "versus Devastador / Sombrero"),
    ("un fantasma que solo se ve estando muerto", 0.5, "Franclorn"),
    ("se invoca a Gahz'rilla", 0.5, "mapa Interior con la Marra"),
    ("en una balsa naufragada", 1.0, "mapa Un'Goro con la balsa"),
    ("Las Plumas de penacho Muertobosque", 1.5, "pluma + cuentas"),
    ("Pero solo caen si llevas equipada", 1.5, "tarjeta Comisión del Alba"),
    ("El mago y el pícaro la recogen", 1.5, "mapa Azshara Xylem/Ogtinc"),
    ("Alberto escribió: no sé quién", 1.5, "comentario de Alberto"),
    ("Alcaz Island Prison", 1.0, "mapa Marjal con Alcaz"),
    ("Krinkle Buenacero, en Gadgetzan", 1.0, "MG cadena Llave esqueleto"),
    ("Riverglades es una zona nueva", 1.0, "reliquia Riverglades"),
    ("The Drowned City, frente a la costa", 1.0, "carrusel mazmorras nuevas"),
    ("exige el Amuleto de Pirodraco", 1.0, "tarjeta Amuleto"),
    ("rescatar al alguacil Windsor", 1.5, "Windsor"),
    ("no tiene el signo de misión sobre", 1.0, "mapa Kargath + Dientegore SIN «!»"),
    ("hay cinco semanas", 1.0, "MG calendario Onyxia"),
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
