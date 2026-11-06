# -*- coding: utf-8 -*-
"""Mide el BRILLO de todos los clips de medios/ ANTES del render (lección de zelda_oot: los negros de 0,3-0,6 s dentro de los
clips no los caza `blackdetect` sobre el MASTER y cada vuelta cuesta un render). Un cuadro cada 0,3 s; media < 14 = negro,
media > 235 = blanco. Imprime los clips con tramos sospechosos y el segundo dentro del clip.
    python medir_brillo.py
"""
import glob
import os

import cv2

AQUI = os.path.dirname(os.path.abspath(__file__))
malos = []
for f in sorted(glob.glob(os.path.join(AQUI, "medios", "scene-*.mp4"))):
    cap = cv2.VideoCapture(f)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    t, raros = 0.0, []
    while t < dur:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if ok:
            g = cv2.cvtColor(cv2.resize(fr, (160, 90)), cv2.COLOR_BGR2GRAY)
            m = float(g.mean())
            if m < 14 or m > 235:
                raros.append((round(t, 1), "negro" if m < 14 else "blanco"))
        t += .3
    if raros:
        malos.append(os.path.basename(f))
        print(f"{os.path.basename(f)} ({dur:.1f} s): " + ", ".join(f"{a}s {b}" for a, b in raros))
print(f"{len(malos)} clips con tramos negros/blancos")
