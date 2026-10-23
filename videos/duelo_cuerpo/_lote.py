# -*- coding: utf-8 -*-
"""Baja un lote de imágenes de Flow (líneas «uuid expires firma» de __col por stdin, en orden de envío) a partir de la
escena N y arma la hoja previews/lote_N.jpg (4 columnas, 320x180) para revisarlas.
   python _lote.py <primera_escena>  < lineas.txt"""
import os
import subprocess
import sys

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
n0 = int(sys.argv[1])
ls = [l.split() for l in sys.stdin.read().replace("\\n", "\n").splitlines() if len(l.split()) == 3]
entrada = "\n".join(f"{n0 + i} {' '.join(p)}" for i, p in enumerate(ls))
r = subprocess.run([sys.executable, os.path.join(D, "..", "..", "nucleo", "flow_integrado.py"), "bajar", "duelo_cuerpo"],
                   input=entrada, capture_output=True, text=True, cwd=os.path.join(D, "..", ".."))
print(r.stdout.strip(), r.stderr.strip()[-300:])
W, H = 320, 180
fs = [os.path.join(D, "medios", f"scene-{n0 + i:03d}.jpg") for i in range(len(ls))]
hoja = Image.new("RGB", (W * 4, H * ((len(fs) + 3) // 4)))
for i, f in enumerate(fs):
    if os.path.exists(f):
        hoja.paste(Image.open(f).convert("RGB").resize((W, H)), ((i % 4) * W, (i // 4) * H))
hoja.save(os.path.join(D, "previews", f"lote_{n0}.jpg"))
print("hoja", f"previews/lote_{n0}.jpg", len(fs))
