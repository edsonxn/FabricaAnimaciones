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

PROMESAS = [   # (frase ancla, + s, qué debería verse) — tes_pierdes_siempre, 26-nov-2026
    ("Un bastón que vale mil", 0.8, "baston de Nahkriin"),
    ("dos perros y un trol con armadura", 0.6, "trol acorazado / Guardia del Alba"),
    ("Y una tormenta de rayos", 0.8, "Invocar tormenta en accion"),
    ("Brynjolf te manda", 0.6, "Brynjolf"),
    ("La orden: quemar tres colmenas", 0.8, "colmenas ardiendo en Brillo Dorado"),
    ("Y el fuego se contagia", 0.8, "fuego extendiendose"),
    ("te cuelas en la fiesta de Elenwen", 0.8, "fiesta de la embajada / Elenwen"),
    ("Se juega la vida por ti", 0.6, "Malborn"),
    ("En Cauce Boscoso hay un triángulo", 0.8, "Cauce Boscoso / Camilla"),
    ("una carta de amor falsa", 0.6, "la carta / Camilla"),
    ("o un duende azul con lanza", 0.6, "riekling"),
    ("Y achezeta se acaba", 0.4, "comentario achezeta"),
    ("sientas a imperiales y capas", 0.8, "mesa de negociacion en Alto Hrothgar"),
    ("muere Ondolemar", 0.6, "Ondolemar"),
    ("Ahí está Custodia Carcette", 0.8, "Carcette"),
    ("El salón queda en ruinas", 0.6, "Salon de los Vigilantes en ruinas"),
    ("Severo Pelagia en Carrera Blanca", 0.6, "batalla de Carrera Blanca / Severo"),
    ("El stalhrim es el hielo encantado", 0.8, "stalhrim"),
    ("Un rayo mal apuntado, un grito", 0.6, "grito / Fus Ro Dah"),
    ("en un sarcófago al fondo de la ruina", 0.6, "Corona dentada en el sarcofago"),
    ("tienes que entregarla, ya sea a Tullius", 0.6, "entrega a Tullius o Ulfric"),
    ("Falion, el mago de Morthal", 0.8, "Falion / ritual de la cura"),
    ("las del Arco de Auriel", 0.4, "Arco de Auriel / flechas malditas"),
    ("Erikur es un thane de Soledad", 0.6, "Erikur"),
    ("La forma bestial", 0.8, "transformacion en hombre lobo"),
    ("Aela puede devolverte", 0.6, "Aela"),
    ("Harkon te ofrece su don", 0.8, "Harkon ofreciendo el don"),
    ("la ballesta enana y los virotes explosivos", 0.6, "ballesta enana / virotes"),
    ("y los trols con armadura", 0.4, "trol acorazado"),
    ("con rayos de ochenta de daño", 0.6, "tormenta con rayos"),
    ("a lomos de Odahviing", 0.6, "Odahviing volando a Skuldafn"),
    ("derrotas al sacerdote dragón Nahkriin", 0.8, "Nahkriin"),
    ("lo pones en el sello dragón", 0.8, "baston en el sello / portal"),
    ("puedes cruzar el portal ya abierto", 0.6, "portal de Sovngarde"),
    ("Y la máscara de Nahkriin", 0.6, "mascara de Nahkriin"),
    ("Radio Yermo, nuestro canal hermano", 0.8, "Radio Yermo"),
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
