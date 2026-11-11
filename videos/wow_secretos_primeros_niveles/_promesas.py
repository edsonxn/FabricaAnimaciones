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
    ("Un brazo de Terminator sobre un pedestal", 1.0, "gancho: brazo Terminator"),
    ("este pequeño pedazo", 2.0, "MASTER Crematoria con audio"),
    ("Así suena Gaia Eterna", 1.0, "ficha Gaia Eterna"),
    ("Te contesta en el chat", 1.0, "chat /rude Pebblebitty"),
    ("a veces escribe en el chat: Eekum", 1.5, "Bom'bay + Eekum Bokum"),
    ("aparece un lobo espíritu raro", 2.0, "Coldrasp lobo azul"),
    ("la empieza un objeto del fondo del lago", 1.0, "caja de pesca hundida"),
    ("Es solo un cadáver tirado junto al camino", 1.0, "cadáver de Olgra"),
    ("Casi todos pasan a su lado sin mirarlo", 1.0, "Eitrigg"),
    ("se convierten en huargen Moonrage", 1.0, "huargen en Piroleña"),
    ("hay un muro gigantesco", 1.5, "Muro de Cringris"),
    ("buceas bajo el puente, encuentras un cadáver", 2.0, "cadáver + sobre bajo el puente"),
    ("hay un pedestal. Y encima, un brazo", 2.0, "brazo en pedestal"),
    ("Dentro, en la chimenea, hay leña tibia", 1.0, "chimenea con leña"),
    ("aparece Viktor el Vil", 1.0, "Viktor el Vil"),
    ("hay una estatua con los ojos rojos", 1.5, "estatua ojos rojos"),
    ("aparece el jefe secreto: El Abandonado", 1.0, "El Abandonado"),
    ("dos letras grabadas: M K", 0.8, "obelisco M K"),
    ("una estatua de un orco con un mandoble", 1.0, "estatua orco + Koiter"),
    ("Kyle se calma", 0.5, "Kyle el perro"),
    ("hazle el gesto de la gallina", 1.0, "pollo + /chicken"),
    ("te deja un huevo", 0.5, "huevo / mascota pollo"),
    ("Le quitas de la mano una antorcha apagada", 1.0, "guardia muerto + antorcha"),
    ("aparece una empuñadura antigua", 1.0, "empuñadura en Ban'aethal"),
    ("aparece un espíritu altonato", 1.0, "espíritu altonato Zoram"),
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
