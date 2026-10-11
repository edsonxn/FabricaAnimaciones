import sys, os
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, componer, a_uint8, W, H
import figuras as F
lz = Lienzo()
def frame(fn, t=1.0, bg=(50, 40, 96)):
    lz.nuevo(t, wob=0.0)
    fn(lz, t)
    b = np.zeros((H, W, 3), np.float32); b[:] = np.float32(bg) / 255.0
    return componer(b, lz.resolver(), boil=0)
def hoja(nombre, ts):
    ims = []
    for f, t in ts:
        img = frame(f, t)
        ims.append(cv2.resize(a_uint8(np.clip(img, 0, 1)), (960, 540), interpolation=cv2.INTER_AREA))
    while len(ims) % 2: ims.append(np.zeros_like(ims[0]))
    out = np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)])
    cv2.imwrite(f"previews/{nombre}.jpg", cv2.cvtColor(out, cv2.COLOR_RGB2BGR))

def A(lz, t):
    for i in range(4):
        F.soldado(lz, 180 + i * 240, 700, 2.0, t, paso=1.0, carga=i * 0.5, arma=(None, "espada", "lanza", None)[i], seed=i)
    for i in range(4):
        F.guerrero(lz, 180 + i * 240, 1000, 2.0, t + 0.3 * i, paso=1.0, arma=("lanza", "macuahuitl", "lanza", "macuahuitl")[i], plumas=i, seed=i, lado=-1 if i % 2 else 1)
def B(lz, t):
    F.caballo(lz, 400, 800, 3.0, t, paso=1.0, carga=1)
    F.caballo(lz, 1100, 800, 3.0, t + 0.5, paso=0.0, col=(96, 70, 60))
    F.tlatoani(lz, 1600, 900, 3.0, t, brazos=0.2)
def C(lz, t):
    F.canoa(lz, 400, 700, 2.0, t)
    F.bergantin(lz, 1000, 700, 2.0, t)
    F.barra_oro(lz, 1500, 400, 2.0, 0.1, 0.7)
    F.disco(lz, 200, 250, 110, t); F.disco(lz, 500, 250, 110, t, "plata")
    F.cofre(lz, 800, 400, 2.0, 1.0); F.saco(lz, 1100, 400, 1.6, brillo=1)
    F.joya(lz, 1300, 200, 2, "anillo"); F.joya(lz, 1500, 200, 2, "collar"); F.joya(lz, 1700, 200, 2, "reloj")
    F.pluma(lz, 300, 500, 1.6, 0.2); F.jade(lz, 700, 260, 2.0); F.moneda(lz, 900, 260, 30)
def D(lz, t):
    F.templo_mayor(lz, 600, 900, 1.5)
    F.palacio(lz, 1500, 900, 1.5, luz=1)
    F.brasero(lz, 200, 900, 2.0, t)
hoja("figuras", [(A, 1.0), (A, 1.35), (B, 1.0), (B, 1.3), (C, 1.0), (D, 1.0)])
print("ok")
