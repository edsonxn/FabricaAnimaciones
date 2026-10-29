# -*- coding: utf-8 -*-
"""Busca voces en la biblioteca pública de ElevenLabs para los personajes (solo lectura, no gasta créditos).
Uso: python _voces_buscar.py <gender male|female> [texto de búsqueda…]   → id, nombre, acento, edad, uso, descripción, previa."""
import os
import sys

import requests

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
K = open(os.path.join(RAIZ, "canales", "tokens", "elevenlabs_api_key_2.txt"), encoding="utf-8").read().strip()
gen = sys.argv[1] if len(sys.argv) > 1 else "male"
q = " ".join(sys.argv[2:])
p = dict(page_size=40, language="es", gender=gen, sort="usage_character_count_1y")
if q:
    p["search"] = q
r = requests.get("https://api.elevenlabs.io/v1/shared-voices", headers={"xi-api-key": K}, params=p, timeout=30).json()
for v in r.get("voices", []):
    print(f"{v['voice_id']}  {v['name'][:30]:30s} {v.get('accent', '')[:12]:12s} {v.get('age', ''):11s} "
          f"{v.get('use_case', '')[:18]:18s} {(v.get('description') or '').replace(chr(10), ' ')[:90]}")
