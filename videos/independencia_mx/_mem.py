import os, sys, time
import psutil
import estilos
estilos.activar("kurzgesagt")
import render as R
p = psutil.Process()
def mb(): 
    m = p.memory_info()
    return f"rss={m.rss/1e6:.0f}MB vms={m.vms/1e6:.0f}MB"
print("antes:", mb())
R._init()
print("init:", mb())
for t in (3.0, 12.0, 20.0, 31.0, 39.0, 52.0, 63.0, 20.5, 45.0):
    t0 = time.time()
    im = R._R.cuadro(t)
    print(f"t={t:5.1f} {time.time()-t0:.2f}s  {mb()}")
