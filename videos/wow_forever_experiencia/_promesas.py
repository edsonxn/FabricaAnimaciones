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
    ('Hace unos días, Alberto nos escribió', 1.5, 'comentario de Alberto'),
    ('Porque no tienes que salir de Villa del Lago', 1.0, 'Villa del Lago (pegatina)'),
    ('Porque hay dos formas de jugar Forever', 2.5, 'VS Retail / 2004'),
    ('El nivel máximo es sesenta', 1.0, 'MG techo 60'),
    ('Fricción es todo lo que el juego te pone en medio', 3.0, 'MG fricción'),
    ('Normal, JcJ, Juego de rol', 1.0, 'MG conjuntos de reglas'),
    ('Un enano que se llama Brogan', 1.0, 'MG nombre y apellido'),
    ('Y ese chat es medio juego', 1.5, 'MG chat general'),
    ('El mago se hace su propia comida', 1.0, 'agua conjurada (pegatina)'),
    ('Y el druida se convierte en gato', 0.6, 'forma felina (pegatina)'),
    ('Y la raza también cuenta', 2.5, 'mapa Dun Morogh / Teldrassil'),
    ('Arnold escribió: deja a Marcos', 1.5, 'comentario de Arnold'),
    ('Una viuda en el Bosque del Ocaso', 1.0, 'mapa Ocaso'),
    ('Escucha a tu primer PNJ', 3.0, 'grabación OBS del add-on'),
    ('Fetixe escribió: fomentando', 1.5, 'comentario de Fetixe'),
    ('y sigue los postes del camino', 0.5, 'mapa Elwynn / postes'),
    ('Hogger, el gnoll de élite', 1.5, 'Hogger'),
    ('Y pasa algo muy curioso', 3.0, 'MG grupo de Hogger'),
    ('Vas a pasar por un puente', 1.0, 'mapa a pie'),
    ('Entre Orgrimmar, Entrañas y la Vega', 1.5, 'mapa zepelines'),
    ('Ver aparecer otro continente', 1.0, 'barco / zepelín en el mar (clip)'),
    ('Un cocinero enciende la hoguera', 1.5, 'MG campamento / hoguera'),
    ('Te sientas en un muelle', 1.5, 'carrusel dónde pescar'),
    ('Y el concurso de pesca de los domingos', 1.5, 'mapa Tuercespina / Bahía del Botín'),
    ('Yorsh escribió que sigue el canal', 1.5, 'comentario de Yorsh'),
    ('Cocina pescado y véndelo', 1.0, 'MG tienda'),
    ('La Alianza tiene a la Autoridad', 1.0, 'mapa Crestagrana'),
    ('Las Minas de la Muerte, en los Páramos', 1.0, 'mapa Minas de la Muerte'),
    ('El sistema de capas', 1.0, 'MG capas'),
    ('Cuando te desconectas en una posada', 1.5, 'MG descanso'),
    ('Hay un posadero, una chimenea', 1.0, 'posada (clip)'),
    ('El brujo empieza sin demonio', 1.0, 'carrusel diablillo / súcubo'),
    ('gana la forma felina', 0.5, 'forma felina'),
    ('El cazador puede domesticar casi cualquier', 1.0, 'domesticar (clip/pegatina)'),
    ('En los Páramos de Poniente, los granjeros', 2.0, 'MG cadena Defias'),
    ('Un pueblo llamado Villa Oscura', 1.5, 'mapa Ocaso / Villa Oscura'),
    ('la de Stalvan Mantoniebla', 0.8, 'Stalvan'),
    ("Mor'Ladim", 1.0, "Mor'Ladim"),
    ('En cada zona hay enemigos especiales', 2.0, 'MG raro (dragón plateado)'),
    ('World of Warcraft tiene rincones', 1.5, 'mapa sin misiones'),
    ('Alexander escribió que no se pierde', 1.5, 'comentario de Alexander'),
    ('Vas a tener que subir al zepelín', 1.5, 'mapa Durotar → Elwynn'),
    ('Y mientras corres como fantasma', 1.5, 'mundo gris de fantasma (clip)'),
    ('Esta es nueva de Forever', 1.5, 'mapa Granja Alexston'),
    ('hasta la presa de Loch Modan', 0.5, 'mapa Loch Modan'),
    ('Al final te espera la Bolsa de dormir', 1.5, 'MG bolsa de dormir'),
    ('Número siete. Ve a la Feria', 1.5, 'Feria (clip) + boleto'),
    ('La primera de Forever se instaló', 1.5, 'mapa feria + Silas'),
    ('Ahí está Sayge, un adivino', 1.5, 'Sayge (clip) + tarjeta'),
    ('Como el Molino Tarren y Costasur', 1.0, 'mapa Trabalomas'),
    ('volvamos con Alberto', 1.5, 'comentario de Alberto'),
    ('La misión se llama Perdida', 1.5, 'MG chat Mankrik / Mankrik'),
    ('Ventormenta, Forjaz, Orgrimmar', 1.5, 'carrusel capitales'),
    ('En Cima del Trueno hay ascensores', 1.0, 'ascensores Cima del Trueno (clip)'),
    ('Siéntate en la orilla del canal de Ventormenta', 1.0, 'canal de Ventormenta (clip)'),
    ('Ve y ayúdalo', 1.0, 'MG lo que cuesta ayudar'),
    ('Y el mundo tiene día y noche', 1.5, 'MG día y noche'),
    ('Las bandas abren el nueve de diciembre', 1.0, 'MG calendario bandas'),
    ('Así que no midas tus sesiones', 3.0, 'MG diario'),
    ('Y esas son las treinta cosas', 1.0, 'banda cierre'),
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
