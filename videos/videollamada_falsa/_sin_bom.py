# -*- coding: utf-8 -*-
"""Quita el BOM (U+FEFF) y unifica saltos de línea a LF en los .py de este video (PowerShell 5.1 lo añade con Set-Content)."""
import glob
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
for p in glob.glob(os.path.join(AQUI, "*.py")) + [os.path.join(AQUI, "..", "..", "nucleo", "noir_pers.py")]:
    b = open(p, "rb").read()
    n = b
    while n.startswith(b"\xef\xbb\xbf"):
        n = n[3:]
    if p.startswith(AQUI):
        n = n.replace(b"\r\n", b"\n")
    if n != b:
        open(p, "wb").write(n)
        print("limpio:", os.path.basename(p))
