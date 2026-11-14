# -*- coding: utf-8 -*-
"""Busca en la biblioteca compartida de ElevenLabs voces femeninas jóvenes en español (México) para el canal de Amaya."""
import json
import sys

import requests

sys.path.insert(0, "../../nucleo")
import tts_eleven as T

k = T.cuentas()[-1][1]
vistas = {}
for q in ({"language": "es", "gender": "female", "age": "young", "accent": "mexican"},
          {"language": "es", "gender": "female", "age": "young", "search": "mexicana"},
          {"language": "es", "gender": "female", "age": "young", "search": "teen"},
          {"language": "es", "gender": "female", "age": "young", "use_cases": "social_media"},
          {"language": "es", "gender": "female", "age": "young", "accent": "latin american"}):
    r = requests.get(f"{T.URL}/shared-voices", headers={"xi-api-key": k}, params={**q, "page_size": 40, "sort": "usage_character_count_1y"},
                     timeout=30).json()
    for v in r.get("voices", []):
        vistas.setdefault(v["voice_id"], v)
out = sorted(vistas.values(), key=lambda v: -(v.get("usage_character_count_1y") or 0))
for v in out[:45]:
    print(f'{v["voice_id"]} | {v["name"][:40]} | {v.get("accent")} | {v.get("age")} | {v.get("use_case")} | '
          f'{(v.get("usage_character_count_1y") or 0)//1000}k | {(v.get("description") or "")[:110]}')
json.dump(out, open("audio/_voces_compartidas.json", "w", encoding="utf-8"), ensure_ascii=False)
print("saldos", T.saldos())
