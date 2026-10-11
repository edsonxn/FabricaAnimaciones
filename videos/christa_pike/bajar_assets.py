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
    "capitolio_tn": "File:Tennessee State Capitol 2009.jpg",
    "nashville_noche": "File:Nashville Skyline at Night I-65.jpeg",
    "nashville_skyline": "File:Nashville skyline 2009.jpg",
    "ut_vista": "File:View from Middle Drive, University of Tennessee at Knoxville, Fort Sanders, Knoxville, TN.jpg",
    "ut_mccord": "File:McCord Hall at University of Tennessee, Knoxville, Tenn (83059).jpg",
    "knoxville_rio": "File:Knoxville skyline from Tennessee River.jpg",
    "beckley": "File:Beckley, West Virginia.jpg",
    "beckley_calle": "File:Beckley Main Street.jpg",
    "tn_supreme": "File:Tennessee Supreme Court.jpg",
    "scotus": "File:US Supreme Court.JPG",
    "scotus_ocaso": "File:Panorama of United States Supreme Court Building at Dusk.jpg",
    "sexto_circuito": "File:Potter Stewart US Federal Courthouse, Cincinnati, OH (32278864737).jpg",
    "bill_lee": "File:Bill Lee 2020.jpg",
    "willie1": "File:Willie Francis by AP.jpg",
    "willie2": "File:Willie Francis by International News Photos.jpg",
    "silla_tn": "File:Julius Morgan electric chair.png",
    "silla_fl": "File:Florida electric-chair.jpg",
    "camara_sq": "File:SQ new execution room.jpg",
    "camara_sq_vieja": "File:SQ old execution room.jpg",
    "camara_utah": "File:Execution Chamber at Utah State Prison.jpg",
    "jobcorps_1": "File:Job Corps. (Vocational Instruction - Members of the Job corps and the National Flag.) (ac6ddf25cb9b44deb090dcb4d85016d4).jpg",
    "celdas_eastern": "File:Interior of Cellblock Housing Death Row - Eastern State Penitentiary - Philadelphia - Pennsylvania.jpg",
    "pasillo_eastern": "File:Prison corridor eastern state penitentiary.jpg",
    "ambulancia": "File:Ambulance with lights flashing at night.jpg",
    "hospital_pasillo": "File:Corridor on the second level - NÄL hospital 1.jpg",
}
if __name__ == "__main__":
    extra = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    FOTOS.update(extra)
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
