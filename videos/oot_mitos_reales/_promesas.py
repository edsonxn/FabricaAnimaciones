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

PROMESAS = [   # (frase ancla, + s, qué debería verse) — oot_mitos_reales, 26-nov-2026 (= promesas.md)
    ("Los secretos de Ocarina of Time", 0.5, "Link a caballo, luna, pegatina N64"),
    ("Que Ganon sangraba rojo", 0.4, "fila: templo fuego, Ganon, búho"),
    ("o falso", 0.6, "los tres sellos"),
    ("en el estanque de pesca del Lago Hylia", 0.5, "estanque + mapa del lago"),
    ("Es la locha hyliana", 0.6, "la locha nadando + pegatina"),
    ("Si lo usas, te regaña", 0.2, "el dueño regaña"),
    ("Y en el remake sigue ahí", 0.4, "estanque del remake"),
    ("aparece una bandada", 0.3, "la bandada de cucos"),
    ("siguen igual de rencorosas", 0.3, "cucos del remake"),
    ("en el Rancho Lon Lon", 0.2, "corral con la potranca + mapa"),
    ("Epona es una potranca", 0.4, "potranca junto a Link (remake)"),
    ("Pero en Majora's Mask", 0.4, "Link a caballo en Majora"),
    ("Es un hombre que corre por Hyrule", 0.4, "el corredor"),
    ("Por exactamente un segundo", 0.5, "carrera + contador 1"),
    ("tienes mi apoyo total", 0.3, "comentario"),
    ("salen del suelo unos esqueletos", 0.5, "Stalchild de noche"),
    ("Y al llegar a 20, uno enorme", 0.5, "Stalchild gigante"),
    ("ni siquiera salen", 0.2, "camino de tierra de noche"),
    ("el lector de discos de la Nintendo 64", 0.5, "64DD real + pegatina"),
    ("Se llamaba Ura Zelda", 0.3, "revista Next Generation"),
    ("como Master Quest", 0.3, "título Master Quest"),
    ("Esas terminaron en Majora's Mask", 0.4, "Skull Kid, torre del reloj"),
    ("Kaepora Gaebora", 0.5, "búho del remake con rótulo"),
    ("si quieres oírlo otra vez", 0.3, "Did you get all that? No/Yes"),
    ("Una piedra chismosa del juego", 0.5, "piedra chismosa"),
    ("Es Rauru, el sabio de la luz", 0.6, "Rauru con su rótulo"),
    ("cuál granja del puente", 0.3, "comentario"),
    ("trepaba por la cadena del puente", 0.4, "Link sube la cadena"),
    ("tres rupias rojas escondidas", 0.5, "rupias + MG 60"),
    ("La historia sangrienta de Kakariko", 0.3, "rótulo Shadow Temple"),
    ("de codicia y de odio", 0.2, "inscripción de Navi + ficha"),
    ("las manchas rojas ahora son oscuras", 0.4, "Mano Muerta del remake"),
    ("en el Bosque Perdido se convertía", 0.3, "Lost Woods"),
    ("se pierde y se vuelve Stalfos", 0.3, "Fado: Everybody will become a Stalfos"),
    ("Grog, el muchacho", 0.4, "Grog + pegatinas"),
    ("Y Fado te explica qué le pasó", 0.3, "remake: la sierra / Fado"),
    ("Ganondorf escupía sangre roja", 0.3, "Ganon salpica rojo"),
    ("Desde la 1.2, es verde", 0.3, "MG sangre"),
    ("en el Escudo Espejo", 0.3, "símbolos + escudo"),
    ("en la tumba de Dampé", 0.3, "cementerio + Dampé"),
    ("La Trifuerza se puede conseguir", 0.4, "Trifuerza en la Puerta del Tiempo"),
    ("tocando una canción secreta", 0.2, "hada gigante del TAS"),
    ("Y Link tomó la Trifuerza en vivo", 0.6, "You got the Triforce!!!"),
    ("El rezo del Templo del Fuego", 0.4, "rótulo Fire Temple"),
    ("Escucha", 3.0, "Templo del Fuego (canto se oye)"),
    ("Esa voz salió de un CD comercial", 1.0, "portada Voice Spectral"),
    ("Koji Kondo, el compositor", 0.5, "Koji Kondo"),
    ("mira detrás del cartucho", 0.8, "trasera del cartucho"),
    ("los picos fuego helados", 0.2, "comentario"),
    ("Si quieres ver lo que Nintendo quitó", 0.8, "video anterior"),
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
