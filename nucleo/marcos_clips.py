# -*- coding: utf-8 -*-
"""Detecta marcos de tarjeta (esquinas blancas redondeadas) en los clips de Flow de un video del motor SECUENCIA y
sugiere `SECUENCIA["recorte_por"]` para guion.py. Desde la carpeta del video:  python ../../nucleo/marcos_clips.py

Mira las 4 esquinas de cada medios/scene-XXX.mp4 en t = 0,3, 2, 4, 6 y 8 s: una esquina «de marco» es casi blanca (>215)
y bastante más clara que el interior junto a ella. Con marco en ≥ 2 esquinas en algún momento → recorte 0.035 por lado.
OJO: un fondo blanco real (telaraña sobre pared blanca) también da esquinas blancas; mira a tamaño completo las dudosas.
Los rótulos pegados al borde (números, letras) no los ve: eso se revisa con la vista (`fab.py <v> medios`)."""
import glob
import os

import cv2


def esquinas_marco(f):
    h, w = f.shape[:2]
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(int)
    esq = [g[2:6, 2:6], g[2:6, w - 6:w - 2], g[h - 6:h - 2, 2:6], g[h - 6:h - 2, w - 6:w - 2]]
    cen = [g[30:40, 30:40], g[30:40, w - 40:w - 30], g[h - 40:h - 30, 30:40], g[h - 40:h - 30, w - 40:w - 30]]
    return sum(1 for a, b in zip(esq, cen) if a.mean() > 215 and a.mean() - b.mean() > 25)


def main():
    sugerido = {}
    for ruta in sorted(glob.glob("medios/scene-*.mp4")):
        sid = os.path.basename(ruta)[:-4]
        cap = cv2.VideoCapture(ruta)
        fps, tot = cap.get(cv2.CAP_PROP_FPS) or 24.0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cuentas = []
        for t in (0.3, 2, 4, 6, 8):
            cap.set(cv2.CAP_PROP_POS_FRAMES, min(tot - 1, int(t * fps)))
            ok, f = cap.read()
            if ok:
                cuentas.append(esquinas_marco(f))
        marca = "MARCO" if max(cuentas or [0]) >= 2 else ("¿fondo blanco?" if max(cuentas or [0]) == 1 else "")
        print(f"{sid}  esquinas por tiempo {cuentas}  {marca}")
        if max(cuentas or [0]) >= 2:
            sugerido[sid] = 0.035
    print("\nrecorte_por sugerido (súmale a mano los rótulos de borde que veas):")
    print("    recorte_por=" + repr(sugerido) + ",")


if __name__ == "__main__":
    main()
