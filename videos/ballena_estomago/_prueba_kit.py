import sys, time; sys.path.insert(0, "../../nucleo")
import numpy as np, cv2
from acuarela import *
from personajes import *
t0=time.time()
for t in (1.0, 1.04, 1.09):
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("bfe9e6"), rgb("2d6f93"), 0, H)
    for k in range(6):
        lavado(im, mancha_pts(200+k*170, 300+k*260, 260, 40+k, 0.25, ry=150), rgb("4e8fb0"), 0.35, k, humedo=14)
    rayos(im, 700, -100, [1.75, 1.9, 2.05, 2.2], 1500, 120, rgb("fff6d8"), 0.22)
    for k in range(3): alga(im, 120+380*k, 1950, 600+120*k, t, seed=900+k)
    cachalote(im, 560, 1500, 0.8, t, sx=-1, boca=0.4, bulto=(0.3,0.8))
    buzo(im, 430, 760, 1.25, t, rot=-0.15, cara="normal")
    kuri(im, 800, 600, 1.1, t, cara="feliz")
    exclama(im, 800, 430, 1.0, t); nube_lluvia(im, 300, 380, 0.8, t); destello(im, 900, 900, 1, t)
    for k in range(6): burbuja(im, 470+k*9, 640-k*70, 8+k*2, t, seed=k)
    rotulo(im, "CACHALOTE", 540, 1200, 110, rgb("f6efe0"), t)
    terminar(im, t)
    cv2.imwrite(f"previews/_kit_{t}.jpg", (im[..., ::-1]*255).astype(np.uint8))
print("s/cuadro", (time.time()-t0)/3)
