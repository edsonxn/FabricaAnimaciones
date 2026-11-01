# -*- coding: utf-8 -*-
"""Medios del Short: imágenes de freno_enojo reencuadradas a 9:16 (nucleo/vertical_desde_largo.py).
beat del Short: (medio del largo, ancho visible, foco x[, foco y]).   python medios_del_largo.py  (desde esta carpeta)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import vertical_desde_largo as vl

MAPA = {
    "scene-001": ("scene-012", .40, .50),      # ¿Te ganan las lágrimas…? — llora, nudo de neón en la garganta
    "scene-002": ("scene-013", .46, .52),      # frenando de golpe — pie en el freno de neón
    "scene-003": ("scene-010", .40, .50),      # después de prepararse para pelear — nervio vago en el torso
    "scene-004": ("scene-017", .42, .52),      # suspiro fisiológico — sentado, pulmones de neón
    "scene-005": ("scene-018", .42, .50),      # inhala por la nariz
    "scene-006": ("scene-018", .30, .50, .40), # pulmones llenos (acercamiento a los pulmones)
    "scene-007": ("scene-019", .42, .62),      # alvéolos
    "scene-008": ("scene-020", .58, .45),      # suelta todo — la exhalación de neón
    "scene-009": ("scene-021", .62, .55),      # el doble de largo — dos ondas
    "scene-010": ("scene-022", .40, .50),      # el vago frena el corazón
    "scene-011": ("scene-023", .55, .55),      # exhalar largo es frenar largo — el latido se aplana
    "scene-012": ("scene-024", .45, .58),      # Stanford — laboratorio
    "scene-013": ("scene-025", .40, .50),      # mejoraba el ánimo — la nube sobre la cabeza
    "scene-014": ("scene-055", .40, .50),      # con dos o tres, el golpe baja
    "scene-015": ("scene-034", .45, .38),      # cuatro formas más — agua fría en la cara
    "scene-016": ("scene-056", .52, .50),      # video completo — la disculpa, desde la calma
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    vl.armar("freno_enojo", MAPA)
    vl.hoja()
