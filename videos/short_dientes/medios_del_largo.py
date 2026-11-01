# -*- coding: utf-8 -*-
"""Medios del Short: imágenes de estres_cuerpo reencuadradas a 9:16 (nucleo/vertical_desde_largo.py).
beat del Short: (medio del largo, ancho visible, foco x[, foco y]).   python medios_del_largo.py  (desde esta carpeta)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import vertical_desde_largo as vl

MAPA = {
    "scene-001": ("scene-071", .42, .58),      # ¿tus dientes se están tocando? — frente a la compu, quijada de neón
    "scene-002": ("scene-082", .40, .50),      # ¿tus hombros cerca de las orejas?
    "scene-003": ("scene-072", .48, .55),      # no eres el único — la multitud
    "scene-004": ("scene-083", .46, .50),      # mucha gente aprieta los dientes — cara de cerca
    "scene-005": ("scene-070", .40, .50),      # de día sin darse cuenta
    "scene-006": ("scene-074", .48, .42),      # en el tráfico
    "scene-007": ("scene-076", .44, .50),      # sube por las sienes y la nuca
    "scene-008": ("scene-075", .40, .50),      # el dolor de cabeza más común
    "scene-009": ("scene-084", .48, .50),      # el arreglo — tenso contra suelto
    "scene-010": ("scene-085", .44, .50),      # posición de descanso
    "scene-011": ("scene-086", .48, .55),      # labios juntos, dientes separados, lengua
    "scene-012": ("scene-086", .30, .52, .62), # el paladar (acercamiento a la boca)
    "scene-013": ("scene-087", .40, .50),      # solo para masticar y tragar
    "scene-014": ("scene-083", .30, .50, .70), # deberían estar separados (acercamiento a la quijada)
    "scene-015": ("scene-088", .45, .72),      # una nota en tu monitor
    "scene-016": ("scene-089", .48, .58),      # revisa: ¿dientes separados?
    "scene-017": ("scene-081", .46, .50),      # ¿hombros abajo? — soltar
    "scene-018": ("scene-148", .40, .50),      # los cinco lugares — el cuerpo entero de neón
    "scene-019": ("scene-152", .50, .45),      # el recorrido completo — en el tren, el freno ya conocido
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    vl.armar("estres_cuerpo", MAPA)
    vl.hoja()
