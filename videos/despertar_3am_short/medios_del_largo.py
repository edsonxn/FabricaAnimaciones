# -*- coding: utf-8 -*-
"""Medios del Short: imágenes de despertar_3am reencuadradas a 9:16 (nucleo/vertical_desde_largo.py).
beat del Short: (medio del largo, ancho visible, foco x[, foco y]).   python medios_del_largo.py  (desde esta carpeta)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import vertical_desde_largo as vl

MAPA = {
    "scene-001": ("scene-019", .42, .50),      # ¿por qué a las 3 todo parece peor? — los ojos de neón en la almohada
    "scene-002": ("scene-011", .56, .40),      # ya estás despierto — el señor y el despertador
    "scene-003": ("scene-025", .46, .55),      # empieza lo peor: la cabeza — la nube de tormenta
    "scene-004": ("scene-026", .46, .40),      # las deudas, la salud, los hijos — facturas, frasco, foto
    "scene-005": ("scene-027", .44, .42),      # aquella frase — el globo de diálogo en la ventana
    "scene-006": ("scene-028", .48, .50),      # todo parece más grave — la piedrita y su sombra gigante
    "scene-007": ("scene-020", .46, .50),      # 2022, investigadores — la mesa con revistas y la lupa
    "scene-008": ("scene-029", .44, .78),      # Arizona — el campus con la lámpara encendida
    "scene-009": ("scene-030", .56, .42),      # se inclina hacia lo negativo — la balanza con la nube
    "scene-010": ("scene-031", .46, .40),      # freno y perspectiva — el cerebro con la palanca
    "scene-011": ("scene-032", .46, .55),      # cansada, programado para dormir — el cerebro con gorro
    "scene-012": ("scene-015", .50, .48),      # no para pensar — el señor dormido y su sueño
    "scene-013": ("scene-033", .46, .45),      # parece un abismo — el borde del cañón
    "scene-014": ("scene-034", .46, .50),      # a las 9 es solo un pendiente — la piedrita junto al café
    "scene-015": ("scene-013", .44, .50),      # por qué tu cuerpo te despierta — el resorte del despertador
    "scene-016": ("scene-068", .46, .45),      # cómo volver a dormir — el señor dormido sonriendo
    "scene-017": ("scene-070", .50, .45),      # el video completo — el pueblo al amanecer
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    vl.armar("despertar_3am", MAPA)
    vl.hoja()
