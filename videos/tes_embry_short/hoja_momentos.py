"""Hoja de cuadros de los momentos con rejilla (x,y en %): inicio de cada trozo, golpe y final.
Uso: python hoja_momentos.py [desde hasta]  → previews/momentos_<a>-<b>.jpg (5 momentos por hoja)"""
import json, os, sys
import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(AQUI, "momentos.json"), encoding="utf-8"))
A = int(sys.argv[1]) if len(sys.argv) > 1 else 0
B = int(sys.argv[2]) if len(sys.argv) > 2 else len(R)
W = 480


def cuadro(cap, t, etq):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, fr = cap.read()
    if not ok:
        fr = np.zeros((1080, 1920, 3), np.uint8)
    h = int(fr.shape[0] * W / fr.shape[1])
    fr = cv2.resize(fr, (W, h))
    for k in range(1, 10):
        x, y = int(W * k / 10), int(h * k / 10)
        cv2.line(fr, (x, 0), (x, h), (0, 220, 255), 1)
        cv2.line(fr, (0, y), (W, y), (0, 220, 255), 1)
        cv2.putText(fr, str(k * 10), (x + 2, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
        cv2.putText(fr, str(k * 10), (2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
    cv2.putText(fr, etq, (6, h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return fr


for a in range(A, B, 5):
    filas = []
    for i in range(a, min(a + 5, B)):
        m = R[i]
        cap = cv2.VideoCapture(os.path.join(AQUI, "segmentos", "clips", m["c"] + ".mp4"))
        ts = [(tz[0] + 0.3, "%d %s ini%d %.1f" % (i, m["c"], k, tz[0] + .3)) for k, tz in enumerate(m["trozos"])]
        ts.append((m["t_golpe"], "%d golpe %.1f" % (i, m["t_golpe"])))
        ts.append((m["trozos"][-1][1] - 0.2, "%d fin %.1f" % (i, m["trozos"][-1][1] - .2)))
        ts = ts[:4]
        celdas = [cuadro(cap, t, e) for t, e in ts]
        while len(celdas) < 4:
            celdas.append(np.zeros_like(celdas[0]))
        filas.append(np.hstack(celdas))
    out = os.path.join(AQUI, "previews", "momentos_%02d.jpg" % a)
    cv2.imwrite(out, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(out)
