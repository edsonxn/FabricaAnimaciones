"""Prueba de humo: renderiza un cuadro cada `paso` s de todo el video y reporta errores y tiempos (sin guardar imágenes)."""
import sys, time, traceback
import numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo
import escenas as S
paso = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
lz = Lienzo()
mal, lento = [], []
t = 0.05
while t < S.TOTAL:
    t0 = time.time()
    try:
        img = S.render_mundo(lz, t)
        if not np.isfinite(img).all() or img.mean() < 0.02:
            mal.append((round(t, 2), "cuadro negro o NaN"))
    except Exception as e:
        mal.append((round(t, 2), repr(e)[:160]))
    dt = time.time() - t0
    if dt > 2.5:
        lento.append((round(t, 2), round(dt, 2)))
    t += paso
print("errores:", mal)
print("lentos (>2.5 s):", lento)
