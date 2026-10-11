# -*- coding: utf-8 -*-
"""Descarga las fotos de Commons (dominio público / CC con crédito) que usa el video. Uso: python bajar_assets.py [clave ...]"""
import os
import sys
import time

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as I

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "imagenes")
os.makedirs(D, exist_ok=True)

FOTOS = {
    "hal_finney": "File:Hal Finney doing math.jpg",
    "running_bitcoin": "File:First tweet about bitcoin.png",
    "szabo_escenario": "File:Blockchain Jungle 2023 stage with Nick Szabo.jpg",
    "szabo_capa": "File:Nick-Szabo-Bitcoin-capa.jpg",
    "adam_back": "File:Adam Back 2014.jpg",
    "len_sassaman": "File:Len Sassaman 27C3.jpg",
    "len_sassaman2": "File:Len Sassaman 2.jpg",
    "gavin": "File:Gavin Andresen at 2014 Web Summit.jpg",
    "peter_todd": "File:Peter Todd - 2016.jpg",
    "busto_budapest": "File:Bust of Satoshi Nakamoto in Budapest.jpg",
    "estatua_lugano": "File:Satoshi Nakamoto Statue in Lugano 001.jpg",
    "estatua_lugano2": "File:Statue of Satoshi Nakamoto.jpg",
    "whitepaper": "File:Bitcoin-whitepaper-poster page-0001.jpg",
    "genesis_hex": "File:Bitcoin-Genesis-block.jpg",
    "genesis_periodico": "File:Genesis-block-newspaper-bitcoin.jpg",
    "lehman_dia": "File:Lehman Brothers-NYC-20080915.jpg",
    "lehman_dia2": "File:Lehman Brothers-20080915.jpg",
    "lehman_times_sq": "File:Lehman Brothers Times Square by David Shankbone.jpg",
    "rolls_building": "File:HM Courts & Tribunal Service Rolls Building -01.jpg",
    "rolls_building2": "File:Rolls Building, Royal Courts of Justice.jpg",
    "temple_city": "File:Temple City, CA, USA - panoramio.jpg",
    "carreyrou": "File:John Carreyrou 9-12-2019 DSC02013 (48724580882) (cropped).jpg",
    "le_roux": "File:Paul Le Roux being escorted by DEA agents.png",
    "pizza_day": "File:Bitcoin Pizza Day Papa John’s Atlantic Ave Jacksonville FL.jpg",
    "lopp": "File:Jameson Lopp by Gage Skidmore.jpg",
    "darling_2009": "File:Darling, Lagarde, Geithner (IMF 2009).jpg",
}

if __name__ == "__main__":
    claves = sys.argv[1:] or list(FOTOS)
    for k in claves:
        try:
            info = I.info_archivo(FOTOS[k], 2400)
            if not info:
                print(k, "SIN INFO"); continue
            r = I.guardar_commons(info, D, k)
            print(k, info["w"], info["h"], info["licencia"], "|", info["autor"][:50], "->", os.path.basename(r))
        except Exception as e:
            print(k, "ERROR", e)
        time.sleep(0.6)
