# -*- coding: utf-8 -*-
"""Prueba del tablero vivo: unas piezas, hilos, marcas y cámara. python _demo_tablero.py t1 t2 ... -> previews/demo.jpg"""
import sys
import time

import cv2
import numpy as np

import tablero as T
import piezas as PZ
import docu_fx as X
from motor import H, W

# piezas
print('relleno', PZ.relleno(-2600, 2600, -1600, 1600, seed=3, libres=[(0, 0, 380), (-900, 260, 330), (850, -200, 330), (700, 420, 300), (-300, -650, 420), (-1000, -500, 380)]))
T.Pieza(PZ.impresion_codigo(1440, 30, 820, 18, resaltar=16), 1500, -700, 4, t_in=1.0)
hx, _ = PZ.impresion_hex()
T.Pieza(hx, -1700, 650, -3, t_in=1.2)
gh, _ = PZ.grafica_horas()
T.Pieza(gh, 1600, 900, 2, t_in=1.4)
T.Pieza(PZ.mapa_mundo(), 0, 1250, 1, t_in=1.6, chinchetas=((-700, -380, (0.8,0.1,0.1)), (700, -380, (0.8,0.1,0.1))))
cen = T.Pieza(T.silueta_card("SATOSHI NAKAMOTO", "¿QUIÉN ES?", 520), 0, 0, -2, t_in=0.5)
hal_L, _ = T.polaroid("hal_finney", 440, 0.85, (0.5, 0.35), "HAL FINNEY", gris=True)
hal = T.Pieza(hal_L, -900, 260, 4, t_in=1.5)
back_L, _ = T.polaroid("adam_back", 440, 0.9, (0.45, 0.4), "ADAM BACK")
back = T.Pieza(back_L, 850, -200, -5, t_in=2.4)
f1 = T.Pieza(T.ficha("20-AGO-2008\nPrimer correo conocido de Satoshi: a Adam Back, para citar Hashcash.", titulo="PISTA 1"), 700, 420, 3, t_in=3.2,
             chinchetas=((0, None, (0.15, 0.45, 0.9)),))
n1 = T.Pieza(T.nota("¿POR QUÉ ÉL PRIMERO?"), 1180, 300, -6, t_in=4.0, chinchetas=((0, None, None),), entrada="aparece", dur=0.3)
wp = T.Pieza(T.hoja_img("whitepaper", 760), -300, -650, 2, t_in=4.6, chinchetas=((0, None, (0.9, 0.8, 0.1)),))


def portal(t):
    img = np.zeros((540, 960, 3), np.float32)
    img[:] = (0.05, 0.07, 0.12)
    cv2.circle(img, (int(480 + 200 * np.sin(t)), 270), 80, (0.9, 0.7, 0.2), -1, cv2.LINE_AA)
    return img


pL, ven = T.polaroid(None, 520, 16 / 9, leyenda="LEHMAN · 15-SEP-2008", ventana=True)
pp = T.Pieza(pL, -1000, -500, -3, t_in=5.2, portal=portal, ventana=ven)

T.Hilo(cen, hal, 2.0, 0.9)
T.Hilo(cen, back, 2.9, 0.9, color="rojo", etiqueta=T.ficha("1er correo", 240, 90, rayada=False, px=30))
T.Hilo(back, f1, 3.6, 0.6, color="azul")
T.Hilo(hal, cen, 6.5, 0.6, color="amarillo", corte=8.0)
T.Marca(T.circulo_pts(850, -200, 300, 330, seed=2), 5.5, 0.7)
T.Marca(T.flecha_pts((1150, 180), (900, 330), 0.25), 6.2, 0.5, punta=True)
T.Punteada(cen, wp, 6.0)

C = T.CAM
C.clave(0.0, 0, 0, 1.6, 0, 6, -8)
C.clave(2.0, -400, 100, 0.8, -2, 4, 6)
C.clave(4.0, 600, 0, 0.9, 1, -4, -6)
C.clave(5.6, 700, 300, 1.5, 0, 0, 0, modo="latigo")
C.clave(6.4, -1000, -500, 1.0, -3, 0, 0)
C.clave(8.0, -1000, -480, 3.6, -3, 0, 0)
C.clave(9.0, -1000, -480, 5.5, -3, 0, 0)
C.clave(11.0, 0, 0, 0.45, 0, 8, 4)
C.clave(13.0, 1500, -700, 1.3, 2, -5, 3)
C.clave(15.0, -1700, 650, 1.2, 0, 4, -3)

ts = [float(x) for x in sys.argv[1:]] or [0.3, 1.0, 2.5, 3.5, 4.4, 5.0, 6.0, 6.8, 7.6, 8.6, 9.6, 10.8]
ims = []
for t in ts:
    t0 = time.time()
    lz = np.zeros((H, W, 3), np.float32)
    T.render_tablero(lz, t)
    t1 = time.time()
    out = X.cine(lz, t, tilt=2.5)
    print(f"t={t:5.2f} tablero {t1 - t0:.2f}s  cine {time.time() - t1:.2f}s", flush=True)
    f8 = cv2.cvtColor((np.clip(out, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"previews/demo_{t:.1f}.jpg", f8, [cv2.IMWRITE_JPEG_QUALITY, 90])
    cv2.putText(f8, f"{t:.2f}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 3)
    ims.append(cv2.resize(f8, (640, 360), interpolation=cv2.INTER_AREA))
while len(ims) % 3:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite("previews/demo.jpg", np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok")
