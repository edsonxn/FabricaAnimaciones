# -*- coding: utf-8 -*-
"""Espera a que termine el render de Satoshi y deja una marca para retomar los arreglos de España (memoria: no se renderizan dos a la vez)."""
import os, time
LOG = r"C:\FabricaAnimaciones\videos\satoshi_nakamoto\render_log.txt"
MARCA = r"C:\FabricaAnimaciones\videos\historia_espana\_satoshi_termino.txt"
while True:
    txt = open(LOG, encoding="utf-8", errors="replace").read()
    i = txt.rfind("relanzado 2026-10-04 20:42:29")
    if i >= 0 and "=== fin" in txt[i:]:
        open(MARCA, "w").write(txt[txt.rfind("=== fin"):].strip())
        break
    time.sleep(20)
