# -*- coding: utf-8 -*-
"""Descarga los folios (Yale IIIF, dominio público) y las fotos de Commons que usa el video. Uso: python bajar_assets.py"""
import json
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as I

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "imagenes")
FOL = os.path.join(D, "folios")
os.makedirs(FOL, exist_ok=True)
folios = {f["i"]: f for f in json.load(open(os.path.join(D, "yale_folios.json")))}

# índice del canvas de Yale -> nombre. (índice = número N de "Voynich Manuscript (N).jpg" en Commons)
ELEGIDOS = [1, 2, 3, 4, 7, 8, 10, 24, 32, 110, 111, 114, 121, 125, 128, 129, 133, 158, 135, 136, 139, 141, 144, 147, 148,
            153, 161, 175, 176, 187, 190, 213, 212, 17, 51, 93, 123]     # 17=f8r 51=f26r 93=f47r 123=f68r (muestras de carbono 14)
for i in ELEGIDOS:
    f = folios[i]
    ruta = os.path.join(FOL, f"f{i:03d}.jpg")
    if os.path.exists(ruta) and os.path.getsize(ruta) > 10000:
        continue
    tam = 2600
    url = f"https://collections.library.yale.edu/iiif/2/{f['id']}/full/!{tam},{tam}/0/default.jpg"
    try:
        n = I.descargar(url, ruta, I.UA_NAV)
        print("folio", i, f["label"], n // 1024, "KB")
    except Exception as e:
        print("FALLA folio", i, e)

FOTOS = {
    "voynich_retrato": "File:Michael Voynich.jpg",
    "friedman": "File:William-Friedman.jpg",
    "rodolfo_arcimboldo": "File:Giuseppe Arcimboldo - Rudolf II of Habsburg as Vertumnus - Google Art Project.jpg",
    "rodolfo_retrato": "File:Portrait of Rudolf II, Holy Roman Emperor c. 1580.jpg",
    "kircher": "File:Athanasius Kircher.jpg",
    "mondragone": "File:Frascati vila Mondragone 07.jpg",
    "beinecke_interior": "File:20170420 Beinecke Rare Book Library Interior Yale University New Haven Connecticut.jpg",
    "purple": "File:Purple code machine fragment.agr.jpg",
    "alberti": "File:AlbertiDisk2.jpg",
    "ducado": "File:Buda castle pre1686 coin find IMG 0609 Venezia ducat doge Fransesco Molin c 1650.JPG",
}
for nombre, titulo in FOTOS.items():
    if any(x.startswith(nombre + ".") for x in os.listdir(D)):
        continue
    info = I.info_archivo(titulo, 2400)
    if not info:
        print("NO ENCONTRADA", titulo)
        continue
    ruta = I.guardar_commons(info, D, nombre)
    print(nombre, os.path.getsize(ruta) // 1024, "KB", info["licencia"])
