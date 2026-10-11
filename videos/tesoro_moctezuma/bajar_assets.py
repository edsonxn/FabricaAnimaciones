# -*- coding: utf-8 -*-
"""Descarga las imágenes de Wikimedia Commons (dominio público / CC) que usa el documental. Créditos en imagenes/creditos.json."""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as I

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "imagenes")
os.makedirs(D, exist_ok=True)

FOTOS = {
    "noche_triste": "File:The Sad Night (Noche Triste) (Conquest of Mexico) Painting.jpg",
    "orozco_noche": "File:José Clemente Orozco, La Noche Triste.jpg",
    "suplicio": "File:Leandro Izaguirre - The Torture of Cuauhtémoc - Google Art Project.jpg",
    "bernal_portada": "File:Historia verdadera conquista Nueva España portada.jpg",
    "bernal_retrato": "File:Bernal Diaz del Castillo (cropped).jpg",
    "moctezuma_duran": "File:Moctezuma II Chapultepec Codex Duran.jpg",
    "moctezuma_valle": "File:Daniel del Valle, Moctezuma II Museo Nacional De Arte.jpg",
    "mapa_1524": "File:Map of Tenochtitlan and Gulf of Mexico, 1524.jpg",
    "durero": "File:Albrecht Dürer - 1500 self-portrait (High resolution and detail).jpg",
    "cortes": "File:Hernán Cortés anónimo.jpg",
    "encuentro": "File:The Meeting of Cortés and Moctezuma (Conquest of Mexico) Painting.jpg",
    "rivera_mercado": "File:Murales Rivera - Markt in Tlatelolco 3.jpg",
    "monte_piedad": "File:Nacional Monte de Piedad - Mexico 2024.jpg",
    "monte_piedad_placa": "File:Historical marker - Monte de Piedad building - Mexico 2024.jpg",
    "alameda_aire": "File:Alameda Central desde el aire 1.jpg",
    "alameda_hidalgo": "File:Alameda Central and Av. Hidalgo - Mexico 2024.jpg",
    "templo_mayor": "File:Ruinas del Templo Mayor - Centro Histórico de la Ciudad de México.jpg",
    "zocalo": "File:Plaza de la Constitución - Zócalo de la Ciudad de México - 1.jpg",
    "tenochtitlan_1521": "File:Tenochtitlán, 1521 WDL503.png",
    "carlos_v": "File:Titian - Portrait of Charles V Seated - WGA22964.jpg",
    "tlaxcala": "File:Lienzo de Tlaxcala panel 28.jpg",
}
for nombre, titulo in FOTOS.items():
    if any(x.startswith(nombre + ".") for x in os.listdir(D)):
        continue
    try:
        info = I.info_archivo(titulo, 2600)
        if not info:
            print("NO ENCONTRADA", titulo)
            continue
        ruta = I.guardar_commons(info, D, nombre)
        print(nombre, os.path.getsize(ruta) // 1024, "KB", info["licencia"], flush=True)
    except Exception as e:
        print("FALLA", nombre, e, flush=True)
