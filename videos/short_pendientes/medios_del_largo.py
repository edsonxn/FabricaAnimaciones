# -*- coding: utf-8 -*-
"""Medios del Short: imágenes de agotado_cortisol reencuadradas a 9:16 (nucleo/vertical_desde_largo.py).
beat del Short: (medio del largo, ancho visible, foco x[, foco y]).   python medios_del_largo.py  (desde esta carpeta)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import vertical_desde_largo as vl

MAPA = {
    "scene-001": ("scene-021", .45, .55),      # apagas la luz y tu cabeza se enciende — sentado en la cama
    "scene-002": ("scene-016", .50, .55),      # con todos tus pendientes — remolino de papeles sobre la cama
    "scene-003": ("scene-017", .46, .62),      # Bluma Zeigarnik — el café
    "scene-004": ("scene-018", .45, .60),      # tareas interrumpidas — papeles de neón
    "scene-005": ("scene-019", .42, .50),      # de día, el ruido las tapa — la ciudad
    "scene-006": ("scene-015", .45, .40),      # en el silencio de la noche — despertador de neón
    "scene-007": ("scene-020", .55, .50),      # todas las pestañas pendientes
    "scene-008": ("scene-022", .45, .62),      # el truco toma 5 minutos — la perilla de la alarma
    "scene-009": ("scene-024", .40, .45),      # saca los pendientes de tu cabeza
    "scene-010": ("scene-025", .45, .45),      # escribe en papel
    "scene-011": ("scene-026", .46, .52),      # con detalle — la libreta
    "scene-012": ("scene-027", .50, .50),      # Universidad de Baylor
    "scene-013": ("scene-028", .45, .55),      # 5 minutos antes de dormir — laboratorio de sueño
    "scene-014": ("scene-029", .50, .40),      # se durmieron 9 minutos más rápido
    "scene-015": ("scene-030", .60, .50),      # entre más detallada la lista — el pergamino
    "scene-016": ("scene-031", .45, .50),      # al cerebro le basta — el archivero
    "scene-017": ("scene-031", .28, .50, .60), # la pestaña quedó guardada (acercamiento al cajón)
    "scene-018": ("scene-058", .45, .55),      # cuatro trucos más — la ducha
    "scene-019": ("scene-066", .50, .62),      # video completo — duerme, reloj de arena
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    vl.armar("agotado_cortisol", MAPA)
    vl.hoja()
