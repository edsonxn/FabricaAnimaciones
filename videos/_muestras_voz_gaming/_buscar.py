# -*- coding: utf-8 -*-
import sys, json, requests
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E
k = E.clave()
vistos = {}
for q in ["deep", "grave", "profunda", "narrator", "epic", "dark", "villain", "trailer", "documentary", ""]:
    for acc in ["", "latin american", "mexican"]:
        p = dict(language="es", gender="male", page_size=100, sort="usage_character_count_1y")
        if q: p["search"] = q
        if acc: p["accent"] = acc
        r = requests.get(f"{E.URL}/shared-voices", headers={"xi-api-key": k}, params=p, timeout=30)
        for v in r.json().get("voices", []):
            vistos.setdefault(v["voice_id"], v)
print(len(vistos))
out = []
for v in vistos.values():
    t = (v.get("name","") + " " + (v.get("description") or "") + " " + " ".join(v.get("descriptive", "") if isinstance(v.get("descriptive"), list) else [str(v.get("descriptive",""))])).lower()
    if any(w in t for w in ["deep", "grave", "profund", "dark", "oscur", "bass", "baritone", "barít", "gravel", "powerful", "epic", "épic", "villain", "authorit", "imponent", "resonan"]):
        out.append((v.get("usage_character_count_1y") or 0, v["voice_id"], v.get("name"), v.get("accent"), v.get("age"), v.get("descriptive"), (v.get("description") or "")[:110]))
out.sort(reverse=True)
out=[o for o in out if (o[3] or "") in ("latin american","mexican","peninsular","colombian","argentine","chilean","venezuelan","peruvian","castilian","spanish","neutral","latin")]
for o in out[:45]:
    print(o)
