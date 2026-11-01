# -*- coding: utf-8 -*-
"""Baja la muestra pública (preview_url, sin gastar créditos) de la voz de guion.VOZ como referencia para tts_select."""
import os
import sys

import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
K = open(os.path.join(RAIZ, "canales", "tokens", "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
vid = sys.argv[1]
v = requests.get(f"https://api.elevenlabs.io/v1/voices/{vid}", headers={"xi-api-key": K}, timeout=30).json()
print(v["name"], v.get("preview_url"))
open(os.path.join(AQUI, sys.argv[2]), "wb").write(requests.get(v["preview_url"], timeout=60).content)
