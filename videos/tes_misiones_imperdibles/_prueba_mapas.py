# -*- coding: utf-8 -*-
"""Hojas de los mapas de este video (MP.hoja) -> previews/mapa_kyne.jpg y previews/mapa_gauldur.jpg"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)
import efectos as E  # noqa: E402
import mg_mapa as MP  # noqa: E402

mapas = [d for d in E.FX if d.get("nombre") == "mapa skyrim"]
for nombre, d, dur, marcas in (("kyne", mapas[0], 7.9, [0.1, 1.6, 2.6, 5.0]), ("gauldur", mapas[1], 15.0, [0.5, 3.0, 5.5, 10.0])):
    MP.hoja(d["fn"], dur, marcas, os.path.join(AQUI, "previews", f"mapa_{nombre}.jpg"))
    print("previews/mapa_" + nombre + ".jpg")
