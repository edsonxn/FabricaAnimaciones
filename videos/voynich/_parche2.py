# -*- coding: utf-8 -*-
"""Parche 2: nitidez de acercamientos, encuadres, pieles, tablero."""
import json
import os
import re
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as I

# 1) folios completos de Yale para los acercamientos
folios = {f["i"]: f for f in json.load(open("imagenes/yale_folios.json"))}
os.makedirs("imagenes/folios_hd", exist_ok=True)
for i in (1, 3, 8, 187, 190):
    ruta = f"imagenes/folios_hd/f{i:03d}.jpg"
    if not os.path.exists(ruta):
        n = I.descargar(f"https://collections.library.yale.edu/iiif/2/{folios[i]['id']}/full/full/0/default.jpg", ruta, I.UA_NAV)
        print("hd", i, n // 1024, "KB")

# 2) escenas.py
s = open("escenas.py", encoding="utf-8").read()

# los acercamientos usan la versión HD (ruta absoluta) y lado 3800
for n in ("f001", "f003", "f008", "f187", "f190"):
    s = s.replace(f'D.foto_parallax(lz, "{n}",', f'D.foto_parallax(lz, HD("{n}"),')
s = s.replace("def folio(n, alto=1000):", '''def HD(nombre):
    """Ruta al escaneo completo de Yale (2682x3740) para acercamientos nítidos."""
    return os.path.abspath(f"imagenes/folios_hd/{nombre}.jpg")


def folio(n, alto=1000):''')
s = s.replace("import json\nimport math\nimport types", "import json\nimport math\nimport os\nimport types")

# G1: polaroids más pequeñas y más arriba
s = s.replace('carta(lz, folio(187, 720), cam, t, g_240 - 0.05, cx + 420, cy - 10, 3.5,', 'carta(lz, folio(187, 700), cam, t, g_240 - 0.05, cx + 430, cy - 40, 3.5,')
s = s.replace('(("f004", -330, -195, -7, g_dib), ("f024", -90, 145, 4, g_dib + 0.28), ("f110", -455, 165, -3, g_imp + 0.1))',
              '(("f004", -300, -215, -7, g_dib), ("f024", -70, 95, 4, g_dib + 0.28), ("f110", -440, 105, -3, g_imp + 0.1))')
s = s.replace('pola(nom, 380, 1.12, (0.5, 0.42)), cam, t, ti - 0.05, cx + dx, cy + dy, r, desde=(-260, -320), fase=k * 1.7)',
              'pola(nom, 340, 1.1, (0.5, 0.42)), cam, t, ti - 0.05, cx + dx, cy + dy, r, desde=(-260, -320), fase=k * 1.7)')
s = s.replace("pts.append((cx + dx, cy + dy - 250))", "pts.append((cx + dx, cy + dy - 222))")

# portada del gancho: entera y centrada a la izquierda
s = s.replace("sp = folio(1, 1000)\n    u = prog(t, 0.0, 1.6)", "sp = folio(1, 900)\n    u = prog(t, 0.0, 1.6)")
s = s.replace("cam @ D.poner(sp.w, sp.h, 610, 560, 1.0, -3 + 1.5 * math.sin(0.4 * t), ry, 2)", "cam @ D.poner(sp.w, sp.h, 600, 540, 1.0, -3 + 1.5 * math.sin(0.4 * t), ry, 2)")

# héroes de contenido: centrados
s = s.replace("_hero(lz, t, C1_ - PAD, c_mujeres - 0.12, 125, 640, 540, -8, 2)", "_hero(lz, t, C1_ - PAD, c_mujeres - 0.12, 125, 960, 470, -6, 2, alto=860)")
s = s.replace("_hero(lz, t, c_mujeres - 0.12, c_alfabeto - 0.12, 141, 1280, 540, 6, -2, ry=(12, 4))", "_hero(lz, t, c_mujeres - 0.12, c_alfabeto - 0.12, 141, 960, 470, 5, -2, alto=860, ry=(12, 4))")
s = s.replace("""bloque([("Diagramas", T("contenido", "diagramas", frase=1)), ("De", T("contenido", "de", frase=1)), ("Estrellas", c_estrellas)], W / 2 + 320, 985, 84)""",
              """bloque([("Diagramas", T("contenido", "diagramas", frase=1)), ("De", T("contenido", "de", frase=1)), ("Estrellas", c_estrellas)], W / 2, 985, 84)""")
s = s.replace("""("Tuberías", T("contenido", "tuberias", frase=1))], W / 2 - 300, 985, 84)""", """("Tuberías", T("contenido", "tuberias", frase=1))], W / 2, 985, 84)""")

# pieles sin pisarse
s = s.replace("x = 330 + col * 210 + (fila * 100)\n        y = 470 + fila * 250", "x = 250 + col * 235 + (fila * 60)\n        y = 400 + fila * 270")
s = s.replace("D.hoja_papel(np.ascontiguousarray(im[y0:y0 + ch, x0:x0 + cw]), 250, sr=12)", "D.hoja_papel(np.ascontiguousarray(im[y0:y0 + ch, x0:x0 + cw]), 205, sr=12)")

# Kircher: encuadre sin moiré
s = s.replace('D.foto_parallax(lz, "kircher", tl, d_quiso - D2 + 0.5, 1.7, 2.1, (0.5, 0.2), (0.5, 0.17), par=(80, 10), tono=(0.75, 0.72, 0.65))',
              'D.foto_parallax(lz, "kircher", tl, d_quiso - D2 + 0.5, 1.25, 1.42, (0.5, 0.30), (0.5, 0.28), par=(80, 10), tono=(0.75, 0.72, 0.65))')
# Praga menos saturada
s = s.replace('@toma(D1 - PAD, d_sabio - 0.12, ent=("desenfoque", 0.45), grado=dict(calido=0.06))', '@toma(D1 - PAD, d_sabio - 0.12, ent=("desenfoque", 0.45), grado=dict(calido=0.06, sat=0.7))')
open("escenas.py", "w", encoding="utf-8").write(s)

# 3) tablero de corcho más oscuro y menos naranja
p = r"C:\FabricaAnimaciones\nucleo\docu.py"
d = open(p, encoding="utf-8").read()
d = d.replace("col = np.array([0.42, 0.30, 0.19], np.float32)\n    img = (0.28 + 0.9 * base)[..., None] * col[None, None, :] * 1.5",
              "col = np.array([0.36, 0.27, 0.18], np.float32)\n    img = (0.34 + 0.6 * base)[..., None] * col[None, None, :] * 1.35")
open(p, "w", encoding="utf-8").write(d)
print("ok")
