# -*- coding: utf-8 -*-
"""Medios del Short: imágenes de duelo_cuerpo reencuadradas a 9:16 (nucleo/vertical_desde_largo.py).
beat del Short: (medio del largo, ancho visible, foco x[, foco y]).   python medios_del_largo.py  (desde esta carpeta)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import vertical_desde_largo as vl

MAPA = {
    "scene-001": ("scene-012", .40, .52),      # ¿Se puede romper un corazón? — corazón agrietado de neón
    "scene-002": ("scene-065", .46, .55),      # los médicos lo ven en una pantalla — corazón y trazo del monitor
    "scene-003": ("scene-017", .44, .48),      # ante una noticia terrible — la señora con las manos en el pecho
    "scene-004": ("scene-013", .50, .62),      # la oleada de adrenalina — la ola
    "scene-005": ("scene-014", .42, .50),      # la punta del corazón se queda quieta
    "scene-006": ("scene-014", .30, .50, .62), # se infla como un globo (acercamiento a la punta)
    "scene-007": ("scene-015", .32, .62, .65),      # takotsubo — puerto japonés con la vasija de neón
    "scene-008": ("scene-016", .42, .50),      # la vasija para atrapar pulpos
    "scene-009": ("scene-064", .44, .62),      # igual que un infarto — la mano en el pecho
    "scene-010": ("scene-018", .50, .50),      # 9 de cada 10 — la fila de mujeres
    "scene-011": ("scene-019", .46, .50),      # mujeres después de los 50 — la plaza
    "scene-012": ("scene-020", .44, .60),      # recupera su forma
    "scene-013": ("scene-052", .44, .52),      # no es inofensivo — la señora en el sillón, corazón tenue
    "scene-014": ("scene-021", .48, .45),      # urgencias — la entrada del hospital
    "scene-015": ("scene-022", .44, .60),      # solo el primer día — la noche, la luna
    "scene-016": ("scene-039", .46, .50),      # semanas y meses — el mapa dentro del cerebro
    "scene-017": ("scene-072", .50, .55),      # el video completo — el corazón de neón en el cielo
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    vl.armar("duelo_cuerpo", MAPA)
    vl.hoja()
