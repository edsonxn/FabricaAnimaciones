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

PROMESAS = [   # (frase ancla, + s, qué debería verse) — tes_builds_rotas, 11-nov-2026
    ("Un arquero que mata dragones sin que lo vean", 1.0, "arquero sigiloso"),
    ("con sal y unos peces", 0.8, "sal y peces"),
    ("en las piedras guardianas al suroeste", 1.0, "piedras guardianas / mapa"),
    ("Mano firme", 1.0, "camara lenta al apuntar"),
    ("El arco de hueso de dragón, de Dawnguard", 0.8, "arco de hueso de dragon"),
    ("el grito Ralentizar tiempo", 1.0, "grito Ralentizar tiempo"),
    ("la flecha está clavada en su cinta", 0.5, "libro Cinta dorada"),
    ("Piedra: la Sombría, al sur de Ríften", 1.0, "piedra Sombria"),
    ("cae muerto en pleno mercado", 0.6, "guardia cae"),
    ("lo dejas peleando en ropa interior", 0.5, "bandido en ropa interior"),
    ("puedes robarle a Astrid", 0.6, "Astrid"),
    ("con nueve likes", 0.3, "comentario npc_1261"),
    ("lo vende Drevis Neloren", 0.6, "Drevis Neloren"),
    ("Un minuto de todos contra todos", 0.8, "enemigos peleando entre si"),
    ("en el castillo Vólkijar", 0.5, "Castillo Volkihar"),
    ("Puedes agarrar a un arquero", 1.0, "Senor vampiro agarrando"),
    ("si Serana te acompaña", 0.5, "Serana"),
    ("Gigantes y mamuts incluidos", 0.5, "gigantes y mamuts"),
    ("La Corona aetérica", 0.6, "Corona aeterica"),
    ("Conjurar a un señor dremora", 0.6, "senor dremora"),
    ("Úlfric Capa de la Tormenta, reanimado", 0.6, "Ulfric"),
    ("Mannimarco, rey gusano", 0.5, "libro Mannimarco"),
    ("Lo dice La Unión Soviética", 0.5, "comentario launionsovietica"),
    ("Un dragón, una puñalada", 0.6, "punalada sigilosa"),
    ("Astrid te da unos guantes", 0.6, "guantes de la Hermandad"),
    ("la Navaja de Mehrunes", 0.6, "Navaja de Mehrunes"),
    ("de la habitación de Babette", 0.6, "libro Testigo sagrado"),
    ("Lo sé, Roirek", 0.5, "libro en pantalla (guino)"),
    ("lástima tanta AI", 0.3, "comentario edgarvillalobos"),
    ("cuatro prendas encantadas", 0.6, "las prendas"),
    ("se queda tambaleándose en bucle", 0.6, "dragon tambaleandose"),
    ("Incluido el aliento de dragón", 0.6, "absorcion contra aliento"),
    ("la túnica de Mirák", 0.5, "tunica de Miraak"),
    ("al noreste de Markarth", 0.6, "piedra del Amante / mapa"),
    ("Ya no hay talento para voces reales", 0.3, "comentario YetRise"),
    ("Los barriles del muelle de Ríften", 0.6, "muelle de Riften"),
    ("Congelación, un hechizo de principiante", 0.8, "Congelacion / dragon"),
    ("en el Templo Nocturnal", 0.6, "Templo Nocturnal / libro"),
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
