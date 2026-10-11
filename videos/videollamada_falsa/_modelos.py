# -*- coding: utf-8 -*-
"""Lista los modelos de ElevenLabs de la cuenta con su costo por carácter (solo lectura)."""
import os

import requests

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
K = open(os.path.join(RAIZ, "canales", "tokens", "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
for m in requests.get("https://api.elevenlabs.io/v1/models", headers={"xi-api-key": K}, timeout=30).json():
    if not m.get("can_do_text_to_speech"):
        continue
    es = any(l.get("language_id") == "es" for l in m.get("languages") or [])
    print(f"{m['model_id']:32s} x{(m.get('model_rates') or {}).get('character_cost_multiplier')}  es={es}  "
          f"max={m.get('maximum_text_length_per_request')}  {m.get('name')}")
