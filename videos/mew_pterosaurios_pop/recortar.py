# -*- coding: utf-8 -*-
"""Cuadros del reel (volteado: el original es selfie en espejo) + mate de la persona.
   python recortar.py cuadros            fuente/cuadros/c_%04d.jpg (1920x1080, todo el reel; c_0001 = t 0)
   python recortar.py mate <i> <n>       trabajador i de n: fuente/alfa/a_%04d.png (solo donde está él)
"""
import os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

AQUI = Path(__file__).parent
SRC = AQUI / "fuente" / "orig.mp4"
CU = AQUI / "fuente" / "cuadros"
AL = AQUI / "fuente" / "alfa"
MODELO = "isnet-general-use"
FPS = 30
SIN_EL = [(14.0, 22.87), (47.0, 51.5), (64.4, 70.53)]     # intro de banda e insertos a pantalla completa


def hay_el(i):
    t = i / FPS
    return not any(a - 0.1 <= t < b + 0.05 for a, b in SIN_EL)


def cuadros():
    CU.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-vf", "hflip", "-q:v", "2", str(CU / "c_%04d.jpg")], check=True)
    print(len(list(CU.glob("*.jpg"))), "cuadros")


def mate(i, n):
    try:
        import psutil; psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        pass
    from rembg import new_session, remove
    AL.mkdir(exist_ok=True)
    ses = new_session(MODELO)
    fs = [f for f in sorted(CU.glob("c_*.jpg")) if hay_el(int(f.stem[2:]) - 1)][i::n]
    for f in fs:
        sal = AL / f.name.replace("c_", "a_").replace(".jpg", ".png")
        if sal.exists():
            continue
        im = Image.open(f).convert("RGB")
        m = remove(im.resize((960, 540), Image.LANCZOS), session=ses, only_mask=True, post_process_mask=False)
        m.resize(im.size, Image.BILINEAR).save(sal)
    print("trabajador", i, "listo", len(fs))


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "cuadros":
        cuadros()
    else:
        mate(int(sys.argv[2]), int(sys.argv[3]))
