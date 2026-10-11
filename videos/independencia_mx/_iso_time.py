import sys, time
import numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import kz_iso as I
import _iso_test2 as T
from util import bg_grad
lz = Lienzo()
bg = bg_grad((150, 214, 240), (230, 240, 250))
for zoom in (1.5, 3.6):
    iso = I.Iso(150, 100, 20, zoom)
    ts = []
    for k in range(6):
        t0 = time.time()
        lz.nuevo(k * 0.1, wob=0.0)
        T.suelo_pueblo(lz, iso)
        T.escena(k * 0.1).dibujar(lz, iso)
        t1 = time.time()
        img = componer(bg, lz.resolver(), boil=lz.boil)
        t2 = time.time()
        ts.append((t1 - t0, t2 - t1))
    a = np.array(ts[1:])
    print(f"zoom {zoom}: dibujo {a[:,0].mean()*1000:.0f} ms  + composicion {a[:,1].mean()*1000:.0f} ms")
