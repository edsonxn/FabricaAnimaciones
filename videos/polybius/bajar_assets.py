# -*- coding: utf-8 -*-
"""Descarga las fotos de Commons (dominio público / CC con crédito) que usa el video. Uso: python bajar_assets.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as I

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "imagenes")
os.makedirs(D, exist_ok=True)

FOTOS = {
    "asteroids": "File:Asteroids cabinet.jpg",
    "bradley1": "File:Bradley Trainer screenshot.png",
    "bradley2": "File:Bradley Trainer screenshot 2.PNG",
    "battlezone_cab": "File:Musée Mécanique 205.JPG",
    "tempest_logo": "File:Tempest Logo.jpg",
    "polibio_cuadrado": "File:Polybius square.png",
    "polibio_busto": "File:Gipsmodelle Wiener Historismus Hofburg-Keller 2012 33 Alois Düll, Polybios.jpg",
    "polibio_grabado": "File:Polybius carries Philopoemen's ashes to Megalopolis (engraving).jpg",
    "polibio_1548": "File:Polybius 1548.jpg",
    "polibio_papiro": "File:Polybius Histories Papyrus.jpg",
    "polyplay": "File:Poly-Play Arcade dresden 2025-04-13.jpg",
    "polyplay2": "File:PolyPlay ESC1.jpg",
    "tron": "File:Tron Arcade Game.jpg",
    "marble": "File:Marble Madness arcade cabinet.jpg",
    "donkey": "File:MIX08 Donkey Kong Machine at TAO (2315102482).jpg",
    "portland_estacion": "File:Arrivals-departures board inside Portland Union Station in Dec 1981.jpg",
}
for nombre, titulo in FOTOS.items():
    if any(x.startswith(nombre + ".") for x in os.listdir(D)):
        continue
    try:
        info = I.info_archivo(titulo, 2400)
    except Exception as e:
        print("ERROR", titulo, e)
        continue
    if not info:
        print("NO ENCONTRADA", titulo)
        continue
    ruta = I.guardar_commons(info, D, nombre)
    print(nombre, os.path.getsize(ruta) // 1024, "KB", info["licencia"])
