# -*- coding: utf-8 -*-
"""Lista las voces de ElevenLabs de la cuenta (nombre, id, idioma, descripción) y el saldo. Solo lectura."""
import os
import sys

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "nucleo"))
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
K = open(os.path.join(RAIZ, "canales", "tokens", "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
H = {"xi-api-key": K}
d = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=H, timeout=30).json()
print("saldo:", d.get("character_limit", 0) - d.get("character_count", 0), "de", d.get("character_limit"), "| plan", d.get("tier"))
vs = requests.get("https://api.elevenlabs.io/v1/voices", headers=H, timeout=30).json().get("voices", [])
for v in vs:
    lab = v.get("labels") or {}
    print(f"{v['voice_id']}  {v['name'][:34]:34s} {v.get('category', ''):12s} {lab.get('language', ''):4s} {lab.get('gender', ''):7s} "
          f"{lab.get('age', ''):12s} {lab.get('descriptive', lab.get('description', ''))[:18]:18s} {lab.get('use_case', '')}")
