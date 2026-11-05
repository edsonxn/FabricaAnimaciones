# -*- coding: utf-8 -*-
"""Hoja de prueba del kit docu_antiguo con material real de Ramsés II (4 maquetas, NO son escenas del video).
python _prueba_kit.py -> previews/prueba_kit.jpg"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import cv2
import numpy as np

from motor import H, W, prog, e_inout
import docu as D
import docu_antiguo as A

IMG = "imagenes/"


def m_artefacto(t):           # piedra + busto real que gira + rótulo serif con palabra roja
    lz = A.piedra().copy()
    A.artefacto(lz, IMG + "joven_memnon_rec.png", W * 0.36, H * 0.54, 860, t, 0.0)
    A.rotulo_serif(lz, [("EL JOVEN MEMNÓN, ", A.BLANCO), ("1250 a.C.", A.ROJO)], W * 0.70, H * 0.47, t, 0.6, px=40)
    A.texto_mixto(lz, [("British Museum,", A.BLANCO), ("sala 4", A.GRIS)], W * 0.58, H * 0.56, t, 1.4, px=34)
    A.polvo(lz, t)
    return lz


def m_camafeo(t):             # negro + camafeo de la momia + líquido + neón
    lz = np.full((H, W, 3), 0.025, np.float32)
    A.liquido(lz, W * 0.5, H * 0.36 + 60, 240, 480, e_inout(prog(t, 0.6, 3.0)), t, sem=2)
    A.camafeo(lz, IMG + "momia_cara.JPG", W * 0.5, H * 0.36, 150, t, 0.0, foco=(0.28, 0.45), zoom=1.9)
    A.rotulo_serif(lz, [("3 200 AÑOS ", A.BLANCO), ("DESPUÉS", A.ROJO)], W * 0.5, H * 0.13, t, 0.3, px=40)
    return lz


def m_neon(t):
    lz = np.full((H, W, 3), 0.02, np.float32)
    A.neon(lz, "UN PASAPORTE", W * 0.5, H * 0.5, t, 0.0, px=70)
    return lz


def m_mapa(t):                # Abu Simbel oscurecido + rejilla + territorio + etiqueta + arco
    f = cv2.cvtColor(cv2.imread(IMG + "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg"), cv2.COLOR_BGR2RGB)
    lz = cv2.resize(f, (W, H)).astype(np.float32) / 255.0 * 0.45
    A.territorio(lz, [(300, 700), (900, 520), (1500, 640), (1300, 1000), (500, 1000)], (900, 820), prog(t, 0, 2.5), t, op=0.45)
    A.etiqueta(lz, "Abu Simbel", W * 0.47, H * 0.70, t, 0.8)
    A.arco_luz(lz, (200, 300), (1700, 380), 220, prog(t, 0.3, 2.0) * 1.3)
    A.cursiva_luz(lz, "Y lo consigue", W * 0.5, H * 0.18, t, 1.0)
    return lz


if __name__ == "__main__":
    os.makedirs("previews", exist_ok=True)
    cuadros = []
    for f, ts in ((m_artefacto, (0.5, 2.0, 3.2)), (m_camafeo, (0.4, 1.6, 3.2)), (m_neon, (0.12, 0.6, 1.5)), (m_mapa, (0.8, 1.6, 3.0))):
        for t in ts:
            img = A.cine_antiguo(np.clip(f(t), 0, 1), t)
            cuadros.append(cv2.resize((img * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA))
    filas = [np.hstack(cuadros[i:i + 3]) for i in range(0, len(cuadros), 3)]
    cv2.imwrite("previews/prueba_kit.jpg", cv2.cvtColor(np.vstack(filas), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("previews/prueba_kit.jpg")
