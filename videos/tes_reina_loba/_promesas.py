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

PROMESAS = [   # (frase ancla, + s, qué debería verse) — tes_reina_loba, 12-nov-2026
 ("Afuera, dos esqueletos", 0.8, "esqueletos fuera de la cueva"),
 ("Adentro, una luz azul", 0.8, "luz azul del ritual"),
 ("Una calavera con diadema", 0.6, "calavera de Potema"),
 ("La dice Styrr", 0.5, "Styrr"),
 ("vive aterrada por un demonio hombre lobo", 1.0, "hombre lobo en Camlorn"),
 ("encierra el alma del lobo dentro de una gema", 1.0, "gema con el lobo"),
 ("la mira en la cuna", 0.5, "emperador ante la cuna"),
 ("bajo la Torre de Oro Blanco", 0.5, "Torre de Oro Blanco"),
 ("abrir lo que está cerrado", 0.5, "forzar una cerradura"),
 ("Un broche con un diamante rojo", 0.8, "diamante rojo"),
 ("se esconde detrás de un tapiz", 0.6, "niña tras el tapiz"),
 ("Corre al Salón de los Registros", 0.8, "archivo / cerradura"),
 ("El novio es Mantiarco", 0.6, "boda en Soledad"),
 ("Ella le lanza un espejo", 0.5, "espejo lanzado"),
 ("un gigante calvo con voz de trueno", 0.8, "Bathorgh"),
 ("Aguanta a nueve arqueros", 0.8, "torneo con arqueros y escorpión"),
 ("Al funeral llegan sus hijos", 0.8, "funeral imperial / mapa"),
 ("un collar con una gema de alma amarilla", 0.8, "collar con gema amarilla"),
 ("llega un barco que nadie ha visto nunca", 0.8, "barco maormer en Soledad"),
 ("una tormenta repentina hunde la flota", 0.8, "tormenta en Artaeum"),
 ("Potema se viste de luto", 0.6, "Potema de luto al espejo"),
 ("Y entra al Consejo de Ancianos", 0.6, "sala del Consejo"),
 ("Kintyra, de quince años", 0.6, "Kintyra"),
 ("bajo el estandarte del diamante rojo", 0.6, "arenga con estandarte"),
 ("Bolas de", 0.6, "batalla en la ciénaga con bolas de fuego"),
 ("una jinete redguard con bandera blanca", 0.6, "mensajera con bandera"),
 ("Una turba asaltó la caravana", 0.8, "carruaje en llamas"),
 ("Generales vampiros", 0.5, "general vampiro (cr2)"),
 ("Generales vampiros#2", 0.5, "general vampiro (c7)"),
 ("Un mes entero contra el Palacio Azul", 0.8, "asedio de Soledad"),
 ("un remolino de pelo blanquísimo", 0.5, "anciana de pelo blanco"),
 ("se ve una bestia de cuatro patas", 0.8, "lobo dentro de la gema"),
 ("le cuelga la gema al cuello", 0.6, "anciana cuelga la gema al niño"),
 ("Murió en su cama", 0.6, "Potema muerta en su cama"),
 ("se desmayó al recibir la corona", 0.6, "coronación con desmayo"),
 ("Con el embajador argoniano", 0.8, "Pelagio y el argoniano"),
 ("La orquesta toca tres horas", 0.8, "salón de baile vacío"),
 ("Bajas a la Cueva Cráneo de Lobo", 0.8, "Cueva Cráneo de Lobo"),
 ("Matas al maestro del ritual", 0.8, "maestro del ritual en la torre"),
 ("detrás de una verja", 0.5, "entrada de las catacumbas"),
 ("Trampas de aceite", 0.5, "trampas de las catacumbas"),
 ("Fuerza Implacable", 0.3, "grito de Potema"),
 ("solo queda su calavera", 0.6, "calavera en el trono"),
 ("la pelvis de Pelagio", 0.5, "pelvis de Pelagio"),
 ("tomando el té con el emperador", 0.8, "Sheogorath y Pelagio en la mesa"),
 ("Te da el Wabbajack", 0.5, "Wabbajack"),
 ("Pelagio duerme en una cama, en medio del bosque", 1.0, "cama en el bosque"),
 ("Es un lobo", 0.3, "lobo pesadilla"),
 ("@brandovelasquez957", 0.5, "comentario brando"),
 ("@rolfaso", 0.5, "comentario rolfaso"),
 ("@Eme_4r", 0.5, "comentario Eme_4r"),
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
