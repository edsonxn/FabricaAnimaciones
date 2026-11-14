# -*- coding: utf-8 -*-
"""Cuadros del tramo 0-20,7 s (ventana sin rótulos ni pegatinas del original) + mate de la persona.
   python recortar.py cuadros            extrae fuente/cuadros/c_%04d.jpg (1440x1100, filas 15 %-58 % del original)
   python recortar.py prueba             mate de 4 cuadros con 2 modelos → previews/mate_prueba.jpg
   python recortar.py mate <i> <n>       trabajador i de n: fuente/alfa/a_%04d.png
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

AQUI = Path(__file__).parent
SRC = AQUI / "fuente" / "fugu.mp4"
CU = AQUI / "fuente" / "cuadros"
AL = AQUI / "fuente" / "alfa"
Y0, ALTO = 384, 1100          # filas del original 2560
DUR = 20.7
MODELO = "isnet-general-use"


def cuadros():
    CU.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-t", str(DUR), "-i", str(SRC), "-vf", f"crop=1440:{ALTO}:0:{Y0}", "-q:v", "2", str(CU / "c_%04d.jpg")], check=True)
    print(len(list(CU.glob("*.jpg"))), "cuadros")


def mate_de(im, ses):
    from rembg import remove
    return remove(im, session=ses, only_mask=True, post_process_mask=False)


def prueba():
    from rembg import new_session
    ids = [45, 170, 300, 460]
    filas = []
    for mod in ("u2net_human_seg", "isnet-general-use"):
        ses = new_session(mod)
        fila = []
        for i in ids:
            im = Image.open(CU / f"c_{i:04d}.jpg").convert("RGB")
            m = mate_de(im, ses)
            a = np.asarray(im).astype(np.float32) * (np.asarray(m)[..., None] / 255.0)
            a += np.array([0, 90, 200], np.float32) * (1 - np.asarray(m)[..., None] / 255.0)
            fila.append(Image.fromarray(a.astype(np.uint8)).resize((360, 275)))
        filas.append(fila)
    hoja = Image.new("RGB", (360 * len(ids), 275 * 2))
    for r, fila in enumerate(filas):
        for c, im in enumerate(fila):
            hoja.paste(im, (c * 360, r * 275))
    hoja.save(AQUI / "previews" / "mate_prueba.jpg", quality=88)


def mate(i, n):
    from rembg import new_session
    AL.mkdir(exist_ok=True)
    ses = new_session(MODELO)
    fs = sorted(CU.glob("c_*.jpg"))[i::n]
    for f in fs:
        sal = AL / f.name.replace("c_", "a_").replace(".jpg", ".png")
        if sal.exists():
            continue
        mate_de(Image.open(f).convert("RGB"), ses).save(sal)
    print("trabajador", i, "listo", len(fs))


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "cuadros":
        cuadros()
    elif c == "prueba":
        prueba()
    else:
        mate(int(sys.argv[2]), int(sys.argv[3]))
