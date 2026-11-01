# -*- coding: utf-8 -*-
"""Mide DURACIÓN y BRILLO de los clips de medios/ contra beats.json, ANTES del render (lecciones de zelda_oot y bt_mundos_ranking):
un cuadro cada 0,3 s; media < 14 = negro, > 235 = blanco; dura menos que el beat = truncado (`bajar` trunca los clips con audio).
    python medir_clips.py
"""
import glob
import json
import os

import cv2

AQUI = os.path.dirname(os.path.abspath(__file__))
bs = {b["id"]: b for b in json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))}
malos, cortos, faltan = [], [], []
for sid, b in bs.items():
    f = os.path.join(AQUI, "medios", sid + ".mp4")
    if not os.path.exists(f):
        faltan.append(sid)
        continue
    L = b["t1"] - b["t0"]
    cap = cv2.VideoCapture(f)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    t, raros = 0.0, []
    while t < min(dur, L):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if ok:
            m = float(cv2.cvtColor(cv2.resize(fr, (160, 90)), cv2.COLOR_BGR2GRAY).mean())
            if m < 14 or m > 235:
                raros.append(round(t, 1))
        t += .3
    cap.release()
    if dur < L - .05:
        cortos.append(f"{sid} {dur:.1f}/{L:.1f}")
    if raros:
        malos.append(f"{sid}: {raros[0]}-{raros[-1]} ({len(raros)})")
print("FALTAN:", faltan)
print("CORTOS:", cortos)
print("OSCUROS/BLANCOS:", malos)
