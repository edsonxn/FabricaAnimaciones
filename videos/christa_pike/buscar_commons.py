# -*- coding: utf-8 -*-
"""Lista candidatos de Commons por consulta (título, licencia, tamaño, autor) -> fuentes/commons_busqueda.txt"""
import sys, os
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as iw

QUERIES = sys.argv[1:] or [
    "Christa Pike", "Riverbend Maximum Security Institution", "Tennessee State Capitol Nashville",
    "Nashville skyline night", "University of Tennessee Knoxville campus", "Knoxville Tennessee skyline",
    "Beckley West Virginia", "Orange Park Florida", "Vanderbilt University Medical Center",
    "Bill Lee governor of Tennessee", "Tennessee Department of Correction", "Tennessee Supreme Court building",
    "Supreme Court of the United States building", "Potter Stewart United States Courthouse Cincinnati",
    "lethal injection chamber", "electric chair", "Willie Francis electric chair",
    "Job Corps", "pentobarbital", "prison cell", "prison corridor", "death row", "steam plant Knoxville",
    "Swannanoa North Carolina", "gurney execution", "ambulance night", "hospital corridor",
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
os.makedirs(r"C:\FabricaAnimaciones\videos\christa_pike\fuentes", exist_ok=True)
open(r"C:\FabricaAnimaciones\videos\christa_pike\fuentes\commons_busqueda.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
