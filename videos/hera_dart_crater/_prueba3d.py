"""Hoja de los planos 3D sueltos: python _prueba3d.py modulo.func t1 t2 ... --out nombre"""
import os, sys, importlib
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo")); sys.path.insert(0, AQUI)
import cv2, numpy as np
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "p3d"
args = [a for a in sys.argv[1:] if a != "--out" and a != out]
cel = []
fn = None
for a in args:
    if not a[0].isdigit():
        m, f = a.split("."); fn = getattr(importlib.import_module(m), f); continue
    t = float(a)
    r = fn(t); im = r.final(t) if hasattr(r, "final") else r
    im = (np.clip(im, 0, 1) * 255).astype(np.uint8)[..., ::-1]
    ch = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(ch, f"{fn.__name__} {t:.1f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2); cel.append(ch)
while len(cel) % 3: cel.append(np.zeros_like(cel[0]))
cv2.imwrite(f"previews/{out}.jpg", np.vstack([np.hstack(cel[i:i+3]) for i in range(0, len(cel), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok", len(cel))
