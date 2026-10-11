# -*- coding: utf-8 -*-
"""Corrige los nombres del .srt (la voz los lleva escritos como se pronuncian):  python videos/got_joffrey/_srt.py"""
import glob
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CAMBIOS = {"Yófrey": "Joffrey", "Tirion": "Tyrion", "Sérsei": "Cersei", "Olena": "Olenna"}
for ruta in glob.glob(os.path.join(AQUI, "salida", "*.srt")):
    s = open(ruta, encoding="utf-8").read()
    n = sum(s.count(a) for a in CAMBIOS)
    for a, b in CAMBIOS.items():
        s = s.replace(a, b)
    open(ruta, "w", encoding="utf-8", newline="\n").write(s)
    print(f"{os.path.basename(ruta)}: {n} nombres corregidos")
