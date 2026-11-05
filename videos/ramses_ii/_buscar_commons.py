# -*- coding: utf-8 -*-
"""Busca candidatas en Commons para el material del video (lista; no descarga)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import imagenes_web as IW
for q in sys.argv[1:]:
    print("==", q)
    try:
        for r in IW.commons(q, n=6):
            print("  ", r["titulo"][:95], "|", r["licencia"], "|", r.get("ancho"), "x", r.get("alto"))
    except Exception as e:
        print("  error", e)
