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

PROMESAS = [   # (frase ancla, + s, qué debería verse) — tes_armaduras_poderosas, 19-nov-2026
    ("invoca a un sacerdote dragón", 0.8, "Konahrik / sacerdote espectral"),
    ("sacrificas a tu propio seguidor en un altar", 0.6, "altar de Boethiah"),
    ("Y un casco que escupe vapor", 0.8, "vapor de Mzund"),
    ("Y una túnica que hace brotar tentáculos", 0.8, "tentaculos de Miraak"),
    ("salen volando por los aires", 0.4, "enemigo volando por el vapor"),
    ("Está en el Gran Salón de Fahlbtharz", 0.8, "Fahlbtharz"),
    ("El perro habla. Se llama Barbas", 0.6, "Barbas"),
    ("le puede desaparecer la cabeza", 0.6, "personaje sin cabeza"),
    ("repara el hacha Úuzrad en la Forja del Cielo", 0.8, "Forja del Cielo / Wuuthrad"),
    ("tapa más de un tercio de la pantalla", 0.6, "escudo en primera persona"),
    ("con nueve likes", 0.4, "comentario frankortiz"),
    ("En la Gruta del Hombre Hinchado", 0.8, "Gruta / Sinding"),
    ("En la sala de los ataúdes", 0.8, "armadura sobre armario"),
    ("A los cinco bloqueos empieza a brillar", 0.8, "escudo de Auriel brillando"),
    ("a un gigante de escarcha", 0.6, "gigante de escarcha / Modelo de rubí"),
    ("Las botas: caminar sobre el agua", 0.6, "caminar sobre el agua"),
    ("el propio Azídal sale a pelear", 0.6, "Ahzidal"),
    ("puedes coger peces con la mano", 0.5, "coger peces"),
    ("@zaarondarklord6196", 0.5, "comentario zaarondarklord"),
    ("en la Ratonera bajo Ríften", 0.6, "Ratonera"),
    ("detrás del trono de Punta de la Arpía", 0.8, "palanca de Punta de la Arpia"),
    ("@stratosincaster4500", 0.5, "comentario stratosincaster"),
    ("la custodia es cóncava", 0.6, "custodia del Anulador"),
    ("contra el aliento de un dragón", 0.6, "bloquear aliento de dragon"),
    ("La Corona dentada", 0.6, "Corona dentada"),
    ("Derrotas a Ancáno en la Sala de los Elementos", 0.8, "Ancano"),
    ("en el Salón de los Ruiseñores", 0.6, "Salon de los Ruisenores"),
    ("reúnes las ocho máscaras", 0.6, "las 8 mascaras / bustos"),
    ("los tentáculos de Apócrifa", 0.5, "tentaculos de Apocrifa"),
    ("doblegas a Sajrotár", 0.5, "Sahrotaar"),
    ("en cuatro cofres por todo Sólsteim", 0.6, "mapa de cofres Solstheim"),
    ("ochenta montones de oro", 0.6, "Tumulo de Gyldenhul / oro"),
    ("una sombra negra con humo verde", 0.6, "humo de la Cota de ebano"),
    ("En el Próstilo de Boétia sacrificas", 0.6, "Prostilo de Boethiah"),
    ("solo trece están suscritos", 0.5, "rejilla campana 13/100"),
    ("Déor Tallador, en la Aldea Skaal", 0.8, "Deor Tallador / Aldea Skaal"),
    ("hay un santuario de Akatosh", 0.8, "santuario de Akatosh / escama"),
    ("te pones su cráneo de sombrero", 0.5, "yelmo de placas de dragon"),
    ("Lo sueltan los drémora", 0.6, "dremora"),
    ("la Fragua del atronach", 0.6, "Fragua del atronach"),
    ("no tienen el brillo rojo del resto", 0.6, "botas sin brillo rojo"),
    ("Hasta la de hierro", 0.6, "armadura de hierro al tope"),
    ("Radio Yermo, nuestro canal hermano", 0.8, "logo Radio Yermo"),
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
