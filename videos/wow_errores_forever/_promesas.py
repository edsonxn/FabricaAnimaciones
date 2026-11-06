"""Hoja de PROMESAS VISUALES (regla 5-nov-2026): un cuadro con la capa de fx en el segundo de cada promesa de promesas.md."""
import os, re, sys
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
sys.path.insert(0, r"C:\FabricaAnimaciones")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())          # antes que nucleo/: si no, «efectos» es nucleo/efectos.py y la capa sale vacía
import cv2
import numpy as np
import secuencia_fx as SF

filas = []
for ln in open("promesas.md", encoding="utf-8"):
    m = re.match(r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|([^|]+)\|", ln)
    if m:
        filas.append((int(m.group(1)), float(m.group(2)), m.group(3).strip()))
capa = SF.cargar()
S = capa.S
minis = []
mw, mh, cols = 480, 270, 4
for n, t, frase in filas:
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
    m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
    cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
    txt = f"{n:02d} {t:.1f}s {frase[:34]}".encode("ascii", "replace").decode()
    cv2.putText(m, txt, (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1, cv2.LINE_AA)
    minis.append(m)
per = cols * 5
for h in range(0, len(minis), per):
    g = minis[h:h + per] + [np.zeros_like(minis[0])] * (-len(minis[h:h + per]) % cols)
    ruta = f"previews/promesas_{h // per + 1:02d}.jpg"
    cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
    print(ruta)
