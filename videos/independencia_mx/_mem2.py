import os, sys, time
import psutil
import estilos
estilos.activar("kurzgesagt")
import render as R
p = psutil.Process()
def mb():
    m = p.memory_info()
    return f"rss={m.rss/1e6:.0f}MB vms={m.vms/1e6:.0f}MB"
R._init()
for t in (100.0, 160.0, 200.0, 240.0, 285.0, 300.0, 355.0, 385.0, 430.0, 487.5, 520.0, 560.0, 600.0, 640.0):
    t0 = time.time()
    im = R._R.cuadro(t)
    print(f"t={t:6.1f} {time.time()-t0:.2f}s  {mb()}", flush=True)
