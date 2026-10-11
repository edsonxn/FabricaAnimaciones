# -*- coding: utf-8 -*-
"""Lista candidatos de Commons por consulta (título, licencia, tamaño, autor) -> fuentes/commons_busqueda.txt"""
import sys, os
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as iw

QUERIES = sys.argv[1:] or [
    "Hal Finney", "Nick Szabo", "Adam Back cryptographer", "Craig Steven Wright", "Peter Todd bitcoin developer",
    "Len Sassaman", "Gavin Andresen", "Dorian Nakamoto", "Satoshi Nakamoto statue Budapest", "Satoshi Nakamoto statue Lugano",
    "Mike Hearn bitcoin", "Wei Dai", "Rolls Building London", "Temple City California", "Bitcoin whitepaper",
    "Lehman Brothers 2008", "Royal Courts of Justice London", "Laszlo Hanyecz pizza", "Paul Le Roux", "John Carreyrou",
]
out = []
for q in QUERIES:
    try:
        r = iw.commons(q, 6)
    except Exception as e:
        out.append(f"## {q}\n  ERROR {e}")
        continue
    out.append(f"## {q}")
    for i in r:
        out.append(f"  {i['titulo']} | {i['w']}x{i['h']} | {i['licencia']} | {i['autor'][:50]}")
os.makedirs("fuentes", exist_ok=True)
open("fuentes/commons_busqueda.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
