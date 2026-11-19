# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos de este video (previews/mg_<nombre>.jpg): cuadros en varios tiempos sobre fondo rojizo.
    python _prueba_mg.py [nombre ...]
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import mg_er as E

CARGOS = ["Drogaste a una guerrera", "Sicario de un caníbal", "Ladrón de almas", "Le diste de comer ojos",
          "Quemaste el mundo"]
PRUEBAS = [
    ("expediente", E.expediente(cargos=CARGOS, ya=2, titulo="Expediente del acusado"), [0.4, 2.0, 3.2], 5,
     [0.6, 1.4, 2.8, 4.4]),
    ("audiencia", E.audiencia(), [0.6, 1.6, 2.6, 3.8], 6, [0.3, 0.9, 2.2, 3.1, 5.0]),
    ("uvas", E.uvas([("Un espíritu en Velo Tormentoso", 1), ("Unas ruinas de Liurnia", 5), ("Edgar, el padre", 7),
                     ("Vyke, el caballero", 3)]), [0.3, 2.0, 2.8, 3.6, 4.4, 5.4], 7, [0.2, 1.4, 3.0, 4.8, 6.0]),
    ("paciencia", E.paciencia(icono="pegatinas/raiz_mortuoria.png"), [0.3, 2.2, 3.0, 6.5], 8, [0.5, 1.9, 2.6, 4.2, 7.0]),
]
sel = sys.argv[1:]
for nom, f, mk, dur, ts in PRUEBAS:
    if sel and nom not in sel:
        continue
    ims = []
    for t in ts:
        a = f(t, dur, mk)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        bg = Image.new("RGBA", im.size, (60, 40, 40, 255))
        bg.alpha_composite(im)
        ims.append(bg.convert("RGB").resize((im.width // 2, im.height // 2)))
    cols = 2
    W, H = ims[0].width, ims[0].height
    out = Image.new("RGB", (W * cols, H * ((len(ims) + 1) // 2)))
    for i, im_ in enumerate(ims):
        out.paste(im_, ((i % cols) * W, (i // cols) * H))
    out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews", f"mg_{nom}.jpg"), quality=82)
print("ok")
