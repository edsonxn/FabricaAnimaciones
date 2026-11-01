# -*- coding: utf-8 -*-
"""Baja imágenes de Flow (URLs firmadas de flow-content.google) a medios/scene-NNN.jpg.
Entrada por stdin, una por línea:  NNN uuid expires signature   (o  NNN <url completa>)"""
import os, sys, subprocess, re
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medios")
ok = bad = 0
for ln in sys.stdin:
    p = ln.split()
    if len(p) < 2:
        continue
    n = p[0]
    url = p[1] if p[1].startswith("http") else f"https://flow-content.google/image/{p[1]}?Expires={p[2]}&KeyName=labs-flow-prod-cdn-key&Signature={p[3]}"
    dst = os.path.join(D, f"scene-{int(n):03d}.jpg")
    r = subprocess.run(["curl", "-s", "-m", "60", "-o", dst, "-w", "%{http_code} %{size_download}", url], capture_output=True, text=True)
    code, size = (r.stdout.split() + ["0", "0"])[:2]
    if code == "200" and int(size) > 50000:
        ok += 1
    else:
        bad += 1
        print("FALLO", n, code, size)
print(f"descargadas {ok}, fallos {bad}")
