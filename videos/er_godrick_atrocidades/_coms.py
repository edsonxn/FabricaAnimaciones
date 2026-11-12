# -*- coding: utf-8 -*-
"""Lista los comentarios candidatos de Runa Caída (fecha, likes, id, si ya se usaron en otro video)."""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = r"C:\FabricaAnimaciones"
d = json.load(open(os.path.join(RAIZ, "canales/comentarios/runa_caida.json"), encoding="utf-8"))
cs = d["comentarios"]
print(list(cs[0].keys()))
usados = set()
for g in glob.glob(os.path.join(RAIZ, "videos", "er_*", "pegatinas", "com_*.png")):
    usados.add(re.search(r"com_(.+)\.png", os.path.basename(g)).group(1))
quiero = sys.argv[1:]
for c in cs:
    a = str(c.get("autor", ""))
    if not quiero or any(q.lower() in a.lower() for q in quiero):
        txt = str(c.get("texto", "")).replace("\n", " ")
        print("USADO" if c["id"] in usados else "libre", str(c.get("fecha", ""))[:10], "♥", c.get("likes"), c["id"], a, "|", txt[:300])
