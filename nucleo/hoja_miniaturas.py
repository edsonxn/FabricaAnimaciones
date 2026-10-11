# -*- coding: utf-8 -*-
"""Hoja de miniaturas de YouTube para comparar empaques (docs/que_funciona.md, paso 3).

  python nucleo/hoja_miniaturas.py <salida.jpg> <id_video> [<id_video> ...]

Baja la miniatura pública (hqdefault, sin cuota de la API) de cada video y las pone en una cuadrícula de 4 columnas,
con el orden de los ids (pon primero los tuyos o los de mayor ×). Mírala con Read: se compara el empaque, no el texto.
"""
import os
import subprocess
import sys
import tempfile
import urllib.request

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"


def main(salida, ids):
    tmp = tempfile.mkdtemp(prefix="minis_")
    rutas = []
    for i, v in enumerate(ids):
        ruta = os.path.join(tmp, f"{i:02d}.jpg")
        try:
            urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{v}/hqdefault.jpg", ruta)
        except Exception as e:
            print(f"  {v}: sin miniatura ({e})")
            continue
        if os.path.getsize(ruta) < 3000:      # privado o programado: YouTube da un gris vacío
            print(f"  {v}: sin miniatura pública (privado o programado)")
            continue
        rutas.append(ruta)
    if not rutas:
        raise SystemExit("ninguna miniatura")
    cols = min(4, len(rutas))
    filas = -(-len(rutas) // cols)
    ent = sum((["-i", r] for r in rutas), [])
    esc = "".join(f"[{i}]scale=480:360,crop=480:270:0:45[m{i}];" for i in range(len(rutas)))
    lay = "|".join(f"{(i % cols) * 480}_{(i // cols) * 270}" for i in range(len(rutas)))
    filtro = esc + "".join(f"[m{i}]" for i in range(len(rutas))) + (
        f"xstack=inputs={len(rutas)}:layout={lay}:fill=black" if len(rutas) > 1 else "null")
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *ent, "-filter_complex", filtro, "-frames:v", "1", salida], check=True)
    print(f"{salida}: {len(rutas)} miniaturas, {cols}x{filas}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2:])
