# -*- coding: utf-8 -*-
"""Variante elegida = `<clave>_a.jpg` (recortar y escenas solo leen `_a`); la descartada queda como `_b`.
Elegidas por la hoja de contacto (21-oct-2026): la `b` donde la `a` salió en 2 filas, con figuras encimadas, fondo crema o texto."""
import os

d = os.path.dirname(os.path.abspath(__file__))
B = ["c01_tecuani_camina", "c02_guerrero_corre", "c03_ollin_corre", "c06_aliado_marcha", "c08_perro_corre", "c11_tameme",
     "c12_citlali_camina", "h02_tecuani_g", "h09_corredor", "h12_soldados", "h24_lascasas"]
hecho = os.path.join(d, "hojas", "_elegidas.txt")
if os.path.exists(hecho):
    raise SystemExit("ya aplicado (hojas/_elegidas.txt)")
for c in B:
    a, b, t = (os.path.join(d, "hojas", f"{c}_{x}.jpg") for x in ("a", "b", "tmp"))
    os.replace(a, t); os.replace(b, a); os.replace(t, b)
open(hecho, "w").write("\n".join(B))
print("cambiadas a la variante b:", len(B))
